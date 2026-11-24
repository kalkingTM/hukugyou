"""見本: 締め日（20日締めなど）から、取引が何月分の請求かを判定する"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/closing-day-billing-month.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "請求月判定"
hd = PatternFill("solid", fgColor="DDEBF7")
inp = PatternFill("solid", fgColor="FFF2CC")
for c, h in enumerate(["取引日", "取引先", "金額", "請求月(1日)", "請求月の表示"], 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    (date(2026, 10, 20), "A社", 100000),
    (date(2026, 10, 21), "A社", 50000),
    (date(2026, 10, 31), "B社", 30000),
    (date(2026, 11, 5), "B社", 20000),
    (date(2026, 11, 20), "A社", 40000),
    (date(2026, 11, 25), "C社", 60000),
    (date(2026, 12, 20), "C社", 10000),
    (date(2026, 12, 21), "A社", 80000),
]
for r, (d, n, a) in enumerate(rows, 2):
    ws.cell(r, 1, d).number_format = "yyyy/m/d"
    ws.cell(r, 2, n)
    ws.cell(r, 3, a).number_format = "#,##0"
    ws.cell(r, 4, f"=DATE(YEAR(A{r}),MONTH(A{r})+(DAY(A{r})>$H$1),1)").number_format = "yyyy/m/d"
    ws.cell(r, 5, f'=TEXT(D{r},"yyyy年m月分")')
ws["G1"] = "締め日(31=月末)"; ws["G1"].font = Font(bold=True)
ws["H1"] = 20; ws["H1"].fill = inp
for c, h in enumerate(["請求月", "請求額の合計"], 7):
    x = ws.cell(3, c, h); x.font = Font(bold=True); x.fill = hd
months = [date(2026, 10, 1), date(2026, 11, 1), date(2026, 12, 1), date(2027, 1, 1)]
for r, m in enumerate(months, 4):
    ws.cell(r, 7, m).number_format = 'yyyy"年"m"月分"'
    ws.cell(r, 8, f"=SUMIF($D$2:$D$9,G{r},$C$2:$C$9)").number_format = "#,##0"
for col, w in zip("ABCDEFGH", (12, 8, 11, 13, 14, 3, 16, 14)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
