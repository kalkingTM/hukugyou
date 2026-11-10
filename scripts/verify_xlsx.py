"""見本Excelの数式を実際に計算させ、記事に書いた期待値と一致するか確かめる。

使い方:
    python scripts/verify_xlsx.py samples/<slug>.spec.json

spec.json の形式:
    {
      "file": "public/files/<slug>.xlsx",
      "checks": [
        {"sheet": "シフト表", "cell": "F2", "expected": 8},
        {"sheet": "シフト表", "cell": "G2", "expected": "OK"}
      ]
    }

計算エンジン:
    1. LibreOffice (soffice) があればそれで再計算する（Excelに最も近い）
    2. なければ Python の formulas ライブラリで計算する
終了コード: 0 = 全一致 / 1 = 不一致あり / 2 = 計算できなかった
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import openpyxl

TOL = 1e-6


def find_soffice() -> str | None:
    for name in ("soffice", "libreoffice"):
        p = shutil.which(name)
        if p:
            return p
    for p in (r"C:\Program Files\LibreOffice\program\soffice.exe",):
        if Path(p).exists():
            return p
    return None


def calc_with_libreoffice(src: Path, soffice: str) -> dict[tuple[str, str], object]:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        out.mkdir()
        tmp_in = Path(td) / src.name
        shutil.copy(src, tmp_in)
        subprocess.run(
            [soffice, "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(out), str(tmp_in)],
            check=True, capture_output=True, timeout=180,
        )
        wb = openpyxl.load_workbook(out / src.name, data_only=True)
        return {(ws.title, c.coordinate): c.value for ws in wb.worksheets for row in ws.iter_rows() for c in row}


def calc_with_formulas(src: Path) -> dict[tuple[str, str], object]:
    import formulas  # noqa: PLC0415

    model = formulas.ExcelModel().loads(str(src)).finish()
    sol = model.calculate()
    values: dict[tuple[str, str], object] = {}
    for key, rng in sol.items():
        # key 例: "'[book.xlsx]SHEET1'!A1"
        k = str(key)
        if "!" not in k or ":" in k.split("!")[1]:
            continue
        sheet = k.split("]")[1].split("'")[0] if "]" in k else k.split("!")[0].strip("'")
        cell = k.split("!")[1]
        v = rng.value[0][0] if hasattr(rng, "value") else rng
        values[(sheet.upper(), cell.upper())] = v
    return values


def same(actual: object, expected: object) -> bool:
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        try:
            return abs(float(actual) - float(expected)) <= TOL
        except (TypeError, ValueError):
            return False
    if hasattr(actual, "isoformat"):
        actual = actual.isoformat()[: len(str(expected))]
    elif (
        isinstance(expected, str)
        and len(expected) >= 10
        and expected[4:5] == "-"
        and isinstance(actual, (int, float))
        and not isinstance(actual, bool)
    ):
        # 簡易エンジン(formulas)は日付を通し番号(シリアル値)で返す。1899-12-30 起点の日付に直して比べる。
        from datetime import datetime, timedelta  # noqa: PLC0415

        actual = (datetime(1899, 12, 30) + timedelta(days=float(actual))).isoformat()[: len(expected)]
    return str(actual) == str(expected)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    src = Path(spec["file"])
    if not src.exists():
        print(f"NG: ファイルがありません: {src}")
        return 2

    soffice = find_soffice()
    try:
        if soffice:
            engine = "LibreOffice"
            values = calc_with_libreoffice(src, soffice)
            lookup = lambda s, c: values.get((s, c))  # noqa: E731
        else:
            engine = "formulas(Python)"
            values = calc_with_formulas(src)
            lookup = lambda s, c: values.get((s.upper(), c.upper()))  # noqa: E731
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: 計算できませんでした ({e})")
        return 2

    print(f"engine: {engine}")
    failed = 0
    for chk in spec["checks"]:
        actual = lookup(chk["sheet"], chk["cell"])
        ok = same(actual, chk["expected"])
        failed += not ok
        print(f"{'OK' if ok else 'NG'}  {chk['sheet']}!{chk['cell']}  期待={chk['expected']!r}  実際={actual!r}")
    print("RESULT:", "PASS" if failed == 0 else f"FAIL ({failed}件不一致)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
