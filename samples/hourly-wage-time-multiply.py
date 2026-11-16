"""見本: 勤務時間（時刻形式）×時給を正しい金額にする"""
from datetime import time
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/hourly-wage-time-multiply.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "日給計算"
hd = PatternFill("solid", fgColor="DDEBF7")
heads = ["日", "出勤", "退勤", "休憩(分)", "実働時間", "誤: 時間×時給", "正: 日給(円)"]
for c, h in enumerate(heads, 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    ("11/2(月)", time(9, 0), time(18, 0), 60),
    ("11/3(火)", time(9, 30), time(17, 45), 45),
    ("11/4(水)", time(10, 0), time(15, 20), 0),
    ("11/5(木)", time(8, 50), time(17, 10), 60),
    ("11/6(金)", time(9, 0), time(12, 30), 0),
]
for r, (d, a, b, k) in enumerate(rows, 2):
    ws.cell(r, 1, d)
    ws.cell(r, 2, a).number_format = "h:mm"
    ws.cell(r, 3, b).number_format = "h:mm"
    ws.cell(r, 4, k)
    ws.cell(r, 5, f"=ROUND(((C{r}-B{r})*1440-D{r}),0)/1440").number_format = "h:mm"
    ws.cell(r, 6, f"=E{r}*$J$2").number_format = "#,##0.00"
    ws.cell(r, 7, f"=ROUNDDOWN(ROUND(E{r}*1440,0)*$J$2/60,0)").number_format = "#,##0"
ws["A7"] = "合計"; ws["A7"].font = Font(bold=True)
ws["E7"] = "=SUM(E2:E6)"; ws["E7"].number_format = "[h]:mm"
ws["F7"] = "=SUM(F2:F6)"; ws["F7"].number_format = "#,##0.00"
ws["G7"] = "=SUM(G2:G6)"; ws["G7"].number_format = "#,##0"
ws["I1"] = "設定"; ws["I1"].font = Font(bold=True); ws["I1"].fill = hd
ws["J1"] = "値"; ws["J1"].font = Font(bold=True); ws["J1"].fill = hd
ws["I2"] = "時給(円)"; ws["J2"] = 1150; ws["J2"].number_format = "#,##0"
ws["A9"] = "※ 端数（1円未満）は切り捨てています。切り上げ・四捨五入にするかは職場の規則に合わせてください。"
for col, w in zip("ABCDEFGHIJ", (10, 8, 8, 9, 10, 16, 14, 3, 10, 8)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
