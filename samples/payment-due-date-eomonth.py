"""見本: 締め日と支払条件から支払予定日を出す（EOMONTH / WORKDAY）"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/payment-due-date-eomonth.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "支払予定表"
hd = PatternFill("solid", fgColor="DDEBF7")
heads = ["取引先", "請求書日付", "締め日(31=月末)", "支払月(1=翌月,2=翌々月)", "支払日(31=月末)",
         "今月の締め日", "対象の締め日", "支払予定日", "土日調整後"]
for c, h in enumerate(heads, 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    ("A社", date(2026, 10, 15), 31, 1, 31),
    ("B社", date(2026, 10, 31), 31, 1, 31),
    ("C社", date(2026, 10, 21), 20, 1, 25),
    ("D社", date(2026, 10, 10), 20, 2, 10),
    ("E社", date(2026, 11, 28), 31, 1, 31),
    ("F社", date(2026, 1, 20), 31, 1, 31),
]
for r, (n, d, c, k, p) in enumerate(rows, 2):
    ws.cell(r, 1, n)
    ws.cell(r, 2, d).number_format = "yyyy/m/d"
    ws.cell(r, 3, c); ws.cell(r, 4, k); ws.cell(r, 5, p)
    ws.cell(r, 6, f"=EOMONTH(B{r},-1)+MIN(C{r},DAY(EOMONTH(B{r},0)))").number_format = "yyyy/m/d"
    ws.cell(r, 7, f"=IF(B{r}<=F{r},F{r},EOMONTH(B{r},0)+MIN(C{r},DAY(EOMONTH(B{r},1))))").number_format = "yyyy/m/d"
    ws.cell(r, 8, f"=EOMONTH(G{r},D{r}-1)+MIN(E{r},DAY(EOMONTH(G{r},D{r})))").number_format = "yyyy/m/d"
    ws.cell(r, 9, f"=WORKDAY(H{r}-1,1)").number_format = "yyyy/m/d"
ws["A9"] = "※ 土日調整後は、支払日が土日なら次の月曜に送ります（祝日は考慮していません）。"
for col, w in zip("ABCDEFGHI", (8, 12, 16, 24, 16, 13, 13, 13, 13)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
