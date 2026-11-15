"""記事の自動チェック（公開前の関門）。

使い方:
    python scripts/check_article.py <slug>        # 1本をチェック。ERRORが1つでもあれば終了コード1
    python scripts/check_article.py --all         # 全記事を点検（参考用。終了コードは常に0）

AIの採点とは別に、機械で確かめられる規則（CLAUDE.md の「絶対に守ること」など）を確認する。
ERROR = 公開してはいけない / WARN = 直したほうがよいが公開は止めない。
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "src" / "content" / "posts"
CATEGORIES = ["経理", "事務効率化", "データ整理", "集計・分析", "書類・帳票"]

# 誇大表現・断定（CLAUDE.md）
BANNED_WORDS = ["絶対", "誰でも", "必ず稼", "確実に稼", "間違いなく", "最強", "魔法", "革命的"]
# 運営者の肩書き・経験を本文に書かない（CLAUDE.md）
OPERATOR_PATTERNS = [r"税理士(として|が監修|監修|の私)", r"私の経験", r"筆者の経験", r"実務経験\s*\d+\s*年"]
# 中身のない見出し
EMPTY_HEADINGS = ["まとめ", "はじめに", "おわりに", "最後に", "概要", "終わりに"]
# 書き出しの前置き
INTRO_PHRASES = ["この記事では", "本記事では", "今回は", "ここでは"]
# 制度・データが絡む言葉 → 出典(sources)が必要
INSTITUTION_WORDS = [
    "消費税", "所得税", "法人税", "源泉", "インボイス", "電子帳簿", "社会保険", "労働基準法", "割増賃金",
    "会計基準", "税率", "法定", "労災", "雇用保険", "厚生年金", "国税庁",
]
# 軽く触れるだけの言葉は、本文中に3回以上出るときだけ「制度に触れている」と見なす
WEAK_INSTITUTION_WORDS = ["祝日"]
# バージョン差のある関数 → 出典(sources)が必要
NEW_FUNCS = ["XLOOKUP", "XMATCH", "FILTER(", "UNIQUE(", "SORT(", "SORTBY", "LET(", "LAMBDA", "VSTACK", "HSTACK", "TEXTSPLIT", "SEQUENCE(", "TEXTJOIN", "IFS(", "SWITCH("]
# 本文に直接書いてはいけないアフィリエイトリンク
AFFILIATE_URL_PATTERNS = [r"px\.a8\.net", r"a8mat=", r"amzn\.to", r"amazon\.co\.jp/[^\s)]*tag=", r"moshimo", r"valuecommerce", r"af\.[a-z0-9-]+\.[a-z]+/"]


def jst_today() -> date:
    return datetime.now(timezone(timedelta(hours=9))).date()


def parse_post(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        raise ValueError("frontmatter(---)が見つかりません")
    fm_text, body = m.group(1), m.group(2)
    fm: dict = {}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        mm = re.match(r"^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$", line)
        if not mm:
            i += 1
            continue
        key, val = mm.group(1), mm.group(2)
        if val == "":
            items = []
            j = i + 1
            while j < len(lines) and re.match(r"^\s+-\s+", lines[j]):
                items.append(re.sub(r"^\s+-\s+", "", lines[j]).strip().strip("\"'"))
                j += 1
            fm[key] = items
            i = j
            continue
        if val.startswith("[") and "]" in val:
            inner = val[1 : val.index("]")]
            fm[key] = [x.strip().strip("\"'") for x in inner.split(",") if x.strip()]
        elif val[:1] in "\"'":
            q = val[0]
            end = val.find(q, 1)
            fm[key] = val[1:end] if end > 0 else val[1:]
        else:
            fm[key] = re.sub(r"\s+#.*$", "", val).strip()
        i += 1
    return fm, body


def code_blocks(body: str) -> list[str]:
    return re.findall(r"```[^\n]*\n(.*?)```", body, re.S)


def body_without_code(body: str) -> str:
    return re.sub(r"```[^\n]*\n.*?```", "", body, flags=re.S)


def norm_formula(f: str) -> str:
    return re.sub(r"[\s$]", "", f).upper()


def check(slug: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    path = POSTS / f"{slug}.md"
    if not path.exists():
        return [f"記事ファイルがありません: {path}"], []
    try:
        fm, body = parse_post(path)
    except ValueError as e:
        return [str(e)], []

    plain = body_without_code(body)
    all_posts = {p.stem for p in POSTS.glob("*.md")}

    # --- frontmatter ---
    title = fm.get("title", "")
    desc = fm.get("description", "")
    if not (15 <= len(title) <= 70):
        errors.append(f"題名の長さが範囲外です（{len(title)}字。15〜70字）")
    if len(desc) > 160 or len(desc) < 60:
        errors.append(f"説明(description)の長さが範囲外です（{len(desc)}字。60〜160字。目安は80〜120字）")
    elif not (80 <= len(desc) <= 125):
        warns.append(f"説明(description)は80〜120字が目安です（{len(desc)}字）")
    if fm.get("category") not in CATEGORIES:
        errors.append(f"category が不正です: {fm.get('category')!r}")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(fm.get("date", ""))):
        errors.append(f"date の形式が不正です: {fm.get('date')!r}（YYYY-MM-DD）")
    else:
        d = date.fromisoformat(fm["date"])
        if d > jst_today() + timedelta(days=1):
            warns.append(f"date が未来の日付です: {fm['date']}")
    if not fm.get("keyword"):
        errors.append("keyword がありません")
    if str(fm.get("hasAffiliate", "false")).lower() == "true":
        errors.append("hasAffiliate: true は使わない。広告は affiliate: [id] で指定する（PR表示は自動）")

    # --- 見本ファイルと検証ファイル ---
    sample = fm.get("sampleFile", "")
    xlsx_path = ROOT / "public" / "files" / sample if sample else None
    if not sample:
        errors.append("sampleFile がありません（全記事に見本xlsxを付ける）")
    elif sample != f"{slug}.xlsx":
        warns.append(f"sampleFile は <slug>.xlsx の形にします（{sample}）")
    if xlsx_path is not None and not xlsx_path.exists():
        errors.append(f"見本ファイルがありません: public/files/{sample}")
    spec_path = ROOT / "samples" / f"{slug}.spec.json"
    spec_checks: list[dict] = []
    if not spec_path.exists():
        errors.append(f"検証用ファイルがありません: samples/{slug}.spec.json")
    else:
        try:
            spec_checks = json.loads(spec_path.read_text(encoding="utf-8")).get("checks", [])
        except json.JSONDecodeError:
            errors.append("spec.json が壊れています")
        if len(spec_checks) < 3:
            errors.append(f"spec.json の検証箇所が少なすぎます（{len(spec_checks)}か所。3か所以上）")
    xlsx_formulas: set[str] = set()
    if xlsx_path is not None and xlsx_path.exists():
        try:
            wb = openpyxl.load_workbook(xlsx_path)
            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    for c in row:
                        if isinstance(c.value, str) and c.value.startswith("="):
                            xlsx_formulas.add(norm_formula(c.value))
            if len(xlsx_formulas) < 3:
                errors.append(f"見本ファイルに数式が少なすぎます（{len(xlsx_formulas)}個）")
        except Exception as e:  # noqa: BLE001
            errors.append(f"見本ファイルを開けません: {e}")

    # --- 本文の構造 ---
    h2s = re.findall(r"^## (.+)$", body, re.M)
    if not h2s or h2s[0].strip() != "結論":
        errors.append("最初の見出し(##)は「結論」にします")
    else:
        concl = re.search(r"^## 結論\n(.*?)(?=^## )", body, re.M | re.S)
        ctext = (concl.group(1) if concl else "").strip()
        if len(re.sub(r"\s", "", ctext)) < 40:
            errors.append("「結論」が短すぎます（答えそのものを書く）")
        if any(ctext.startswith(p) for p in INTRO_PHRASES):
            errors.append("「結論」が前置きで始まっています（答えそのものから書く）")
    for h in re.findall(r"^#{2,3} (.+)$", body, re.M):
        if h.strip() in EMPTY_HEADINGS:
            errors.append(f"中身のない見出しがあります: {h.strip()}")
    # よくある質問
    faq = re.search(r"^## よくある質問\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    if not faq:
        errors.append("「## よくある質問」がありません（2〜3個）")
    else:
        qs = re.findall(r"^### (.+)$", faq.group(1), re.M)
        if not (2 <= len(qs) <= 4):
            errors.append(f"よくある質問の数が範囲外です（{len(qs)}個。2〜3個）")
    n = len(re.sub(r"\s", "", plain))
    if n < 1500:
        errors.append(f"本文が短すぎます（約{n}字。1,500字以上）")
    elif n < 2000 or n > 7000:
        warns.append(f"本文の長さが目安（2,000〜4,000字）から外れています（約{n}字）")

    # --- 禁止表現 ---
    for w in BANNED_WORDS:
        if w in plain:
            errors.append(f"誇大・断定の表現があります: 「{w}」")
    for pat in OPERATOR_PATTERNS:
        mm = re.search(pat, plain)
        if mm:
            errors.append(f"運営者の肩書き・経験を本文に書いています: 「{mm.group(0)}」")

    # --- 広告 ---
    for pat in AFFILIATE_URL_PATTERNS:
        if re.search(pat, body):
            errors.append(f"本文にアフィリエイトのリンクが直接書かれています（{pat}）。広告は affiliate: [id] で指定する")
            break
    aff_ids = fm.get("affiliate", []) or []
    if isinstance(aff_ids, str):
        aff_ids = [aff_ids] if aff_ids else []
    if aff_ids:
        aff_data = json.loads((ROOT / "affiliates.json").read_text(encoding="utf-8"))
        items = {a["id"]: a for a in aff_data.get("items", [])}
        if len(aff_ids) > 2:
            errors.append("広告は1記事に最大2つまでです")
        for aid in aff_ids:
            a = items.get(aid)
            if not a:
                errors.append(f"affiliates.json にない広告idです: {aid}")
                continue
            if a.get("enabled") is False:
                errors.append(f"無効の広告idです: {aid}")
            if fm.get("category") not in a.get("categories", []):
                errors.append(f"広告 {aid} は、このカテゴリ（{fm.get('category')}）の記事には使えません")
            for fw in a.get("forbidden", []):
                if fw in body:
                    errors.append(f"広告 {aid} を付けた記事に、禁止語「{fw}」があります")

    # --- 出典(sources) ---
    sources = fm.get("sources", []) or []
    for s in sources:
        if not s.startswith("https://"):
            errors.append(f"sources は https のURLにします: {s}")
    # リンクの文字（別記事への案内など）は数えない
    plain_nolink = re.sub(r"\[([^\]]*)\]\([^)]*\)", "", plain)
    needs = [w for w in INSTITUTION_WORDS if w in plain_nolink]
    needs += [w for w in WEAK_INSTITUTION_WORDS if plain_nolink.count(w) >= 3]
    new_funcs = [f for f in NEW_FUNCS if f in body.upper()]
    if (needs or new_funcs) and not sources:
        what = "・".join((needs[:3] + [f.rstrip('(') for f in new_funcs[:3]]))
        errors.append(f"制度・新しい関数に触れている（{what}）のに、sources（出典）がありません")
    if sources and not needs and not new_funcs:
        warns.append("制度やバージョン差に触れていないのに sources があります（一般的なテクニックには付けない）")

    # --- 内部リンク ---
    links = re.findall(r"\(/hukugyou/posts/([a-z0-9-]+)/\)", body)
    for s in links:
        if s not in all_posts:
            errors.append(f"存在しない記事への内部リンクがあります: {s}")
        if s == slug:
            errors.append("自分自身への内部リンクがあります")
    others = all_posts - {slug}
    if not links and len(others) >= 3:
        warns.append("内部リンクがありません（関連する既存記事があれば1〜3本リンクする）")
    if len(set(links)) > 4:
        warns.append(f"内部リンクが多すぎます（{len(set(links))}本）")

    # --- 他の記事との重複 ---
    for other in sorted(others):
        try:
            ofm, _ = parse_post(POSTS / f"{other}.md")
        except ValueError:
            continue
        if ofm.get("keyword") == fm.get("keyword") or ofm.get("title") == fm.get("title"):
            errors.append(f"既存記事と検索語または題名が重複しています: {other}")

    # --- 記事の数式が見本ファイルにあるか（参考） ---
    if xlsx_formulas:
        shown = []
        for blk in code_blocks(body):
            for line in blk.splitlines():
                line = line.strip()
                if line.startswith("=") and len(line) > 3:
                    shown.append(line)
        missing = [f for f in dict.fromkeys(shown) if norm_formula(f) not in xlsx_formulas]
        if shown and len(missing) > max(3, len(set(shown)) // 2):
            warns.append(f"記事の数式のうち、見本ファイルにそのままない数式が多い（{len(missing)}/{len(set(shown))}）。例: {missing[0][:50]}")

    # --- spec の期待値が記事に出ているか（参考） ---
    if spec_checks:
        hits = 0
        for c in spec_checks:
            e = str(c.get("expected", ""))
            variants = {e}
            md = re.match(r"^(\d{4})-(\d{2})-(\d{2})", e)
            if md:  # 日付は書き方がいろいろある（2026/11/4・11月4日・11/4 など）
                y, mo, d = int(md.group(1)), int(md.group(2)), int(md.group(3))
                variants |= {f"{y}/{mo}/{d}", f"{y}/{mo:02d}/{d:02d}", f"{mo}月{d}日", f"{mo}/{d}", f"{y}年{mo}月{d}日"}
            if e and any(v in plain for v in variants):
                hits += 1
        if hits == 0:
            warns.append("検証した値（spec の期待値）が、記事の本文にひとつも出てきません")

    return errors, warns


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    audit = args[0] == "--all"
    slugs = sorted(p.stem for p in POSTS.glob("*.md")) if audit else [args[0]]
    total_err = 0
    for slug in slugs:
        errs, warns = check(slug)
        total_err += len(errs)
        status = "PASS" if not errs else "FAIL"
        print(f"[{status}] {slug}  (ERROR {len(errs)} / WARN {len(warns)})")
        for e in errs:
            print(f"   ERROR: {e}")
        for w in warns:
            print(f"   WARN : {w}")
    if audit:
        return 0
    print("RESULT:", "PASS" if total_err == 0 else f"FAIL ({total_err}件のERROR)")
    return 0 if total_err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
