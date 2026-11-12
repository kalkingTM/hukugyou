"""見本: 1日8時間を超えた分だけを残業時間として出す"""
from datetime import time
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/overtime-over-8h-calc.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "残業時間"
hd = PatternFill("solid", fgColor="DDEBF7")
heads = ["日", "出勤", "退勤", "休憩", "実働時間", "残業時間", "残業(時間・小数)"]
for c, h in enumerate(heads, 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    ("11/2(月)", time(9, 0), time(18, 0), time(1, 0)),
    ("11/3(火)", time(9, 0), time(19, 30), time(1, 0)),
    ("11/4(水)", time(8, 30), time(20, 15), time(1, 0)),
    ("11/5(木)", time(9, 0), time(17, 30), time(0, 45)),
    ("11/6(金)", time(10, 0), time(21, 0), time(1, 0)),
]
for r, (d, a, b, k) in enumerate(rows, 2):
    ws.cell(r, 1, d)
    for c, v in ((2, a), (3, b), (4, k)):
        ws.cell(r, c, v).number_format = "h:mm"
    ws.cell(r, 5, f"=MOD(C{r}-B{r},1)-D{r}").number_format = "h:mm"
    ws.cell(r, 6, f"=MAX(0,ROUND((E{r}-$J$2)*1440,0))/1440").number_format = "h:mm"
    ws.cell(r, 7, f"=ROUND(F{r}*24,2)").number_format = "0.00"
ws["A7"] = "合計"; ws["A7"].font = Font(bold=True)
ws["E7"] = "=SUM(E2:E6)"; ws["E7"].number_format = "[h]:mm"
ws["F7"] = "=SUM(F2:F6)"; ws["F7"].number_format = "[h]:mm"
ws["G7"] = "=SUM(G2:G6)"; ws["G7"].number_format = "0.00"
ws["I1"] = "基準にする時間"; ws["I1"].font = Font(bold=True); ws["I1"].fill = hd
ws["J1"] = "値"; ws["J1"].font = Font(bold=True); ws["J1"].fill = hd
ws["I2"] = "1日の基準（これを超えた分が残業）"; ws["J2"] = time(8, 0); ws["J2"].number_format = "h:mm"
ws["A9"] = "※ J2 の基準時間を変えると、残業の判定ラインが変わります（例: 所定が7:30なら 7:30 に）。"
for col, w in zip("ABCDEFGHIJ", (10, 8, 8, 8, 10, 10, 16, 3, 34, 8)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
