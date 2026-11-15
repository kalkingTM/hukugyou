"""見本: 売掛金の年齢調べ表（請求日からの経過日数で30/60/90日超に分ける）"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/receivable-aging-table.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "年齢調べ"
hd = PatternFill("solid", fgColor="DDEBF7")
for c, h in enumerate(["請求番号", "取引先", "請求日", "金額", "経過日数", "区分"], 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    ("A-001", "東西商事", date(2026, 11, 5), 120000),
    ("A-002", "北山工業", date(2026, 10, 20), 85000),
    ("A-003", "みなと食品", date(2026, 9, 30), 230000),
    ("A-004", "青空設計", date(2026, 8, 25), 60000),
    ("A-005", "東西商事", date(2026, 10, 31), 150000),
    ("A-006", "北山工業", date(2026, 9, 1), 40000),
    ("A-007", "みなと食品", date(2026, 11, 20), 98000),
    ("A-008", "青空設計", date(2026, 10, 1), 175000),
]
for r, (n, t, d, a) in enumerate(rows, 2):
    ws.cell(r, 1, n); ws.cell(r, 2, t)
    ws.cell(r, 3, d).number_format = "yyyy/m/d"
    ws.cell(r, 4, a).number_format = "#,##0"
    ws.cell(r, 5, f"=$I$1-C{r}").number_format = "0"
    ws.cell(r, 6, f'=IF(E{r}<=30,"30日以内",IF(E{r}<=60,"31〜60日",IF(E{r}<=90,"61〜90日","90日超")))')
ws["H1"] = "基準日"; ws["H1"].font = Font(bold=True); ws["H1"].fill = hd
ws["I1"] = date(2026, 11, 30); ws["I1"].number_format = "yyyy/m/d"
for c, h in enumerate(["区分", "件数", "金額"], 8):
    x = ws.cell(4, c, h); x.font = Font(bold=True); x.fill = hd
for i, k in enumerate(["30日以内", "31〜60日", "61〜90日", "90日超"], 5):
    ws.cell(i, 8, k)
    ws.cell(i, 9, f"=COUNTIF($F$2:$F$9,H{i})")
    ws.cell(i, 10, f"=SUMIF($F$2:$F$9,H{i},$D$2:$D$9)").number_format = "#,##0"
ws["H9"] = "合計"; ws["H9"].font = Font(bold=True)
ws["I9"] = "=SUM(I5:I8)"
ws["J9"] = "=SUM(J5:J8)"; ws["J9"].number_format = "#,##0"
ws["A11"] = "※ 基準日(I1)を変えると経過日数と集計が変わります。毎回今日にしたいときは I1 を =TODAY() にします。"
for col, w in zip("ABCDEFGHIJ", (10, 12, 12, 10, 10, 10, 3, 10, 8, 12)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
