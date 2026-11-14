"""見本: 深夜帯(22:00-5:00)に働いた時間だけを取り出す"""
from datetime import time
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/night-hours-22-to-5.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "深夜時間"
hd = PatternFill("solid", fgColor="DDEBF7")
for c, h in enumerate(["日", "出勤", "退勤", "深夜時間", "深夜(時間・小数)"], 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    ("11/2(月)", time(9, 0), time(18, 0)),
    ("11/3(火)", time(13, 0), time(23, 30)),
    ("11/4(水)", time(17, 0), time(2, 0)),
    ("11/5(木)", time(22, 0), time(6, 0)),
    ("11/6(金)", time(4, 0), time(9, 0)),
]
for r, (d, a, b) in enumerate(rows, 2):
    ws.cell(r, 1, d)
    ws.cell(r, 2, a).number_format = "h:mm"
    ws.cell(r, 3, b).number_format = "h:mm"
    e = f"(C{r}+(C{r}<B{r}))"
    ws.cell(r, 4, f"=ROUND((MAX(0,MIN({e},$H$3)-B{r})+MAX(0,MIN({e},$H$3+1)-MAX(B{r},$H$2)))*1440,0)/1440").number_format = "h:mm"
    ws.cell(r, 5, f"=ROUND(D{r}*24,2)").number_format = "0.00"
ws["A7"] = "合計"; ws["A7"].font = Font(bold=True)
ws["D7"] = "=SUM(D2:D6)"; ws["D7"].number_format = "[h]:mm"
ws["E7"] = "=SUM(E2:E6)"; ws["E7"].number_format = "0.00"
ws["G1"] = "深夜帯の設定"; ws["G1"].font = Font(bold=True); ws["G1"].fill = hd
ws["H1"] = "値"; ws["H1"].font = Font(bold=True); ws["H1"].fill = hd
ws["G2"] = "深夜の開始"; ws["H2"] = time(22, 0); ws["H2"].number_format = "h:mm"
ws["G3"] = "深夜の終了"; ws["H3"] = time(5, 0); ws["H3"].number_format = "h:mm"
ws["A9"] = "※ 休憩が深夜帯に入る日は、その分を深夜時間から別に引いてください。"
for col, w in zip("ABCDEFGH", (10, 8, 8, 10, 16, 3, 14, 8)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
