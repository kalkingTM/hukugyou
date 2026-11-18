"""見本: 打刻時刻を15分単位で丸める（出勤は切り上げ・退勤は切り捨て）"""
from datetime import time
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/time-round-15min-floor.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "15分丸め"
hd = PatternFill("solid", fgColor="DDEBF7")
heads = ["日", "出勤(打刻)", "退勤(打刻)", "出勤(15分切り上げ)", "退勤(15分切り捨て)",
         "丸め後の時間", "丸めなしの時間", "差(分)"]
for c, h in enumerate(heads, 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    ("11/2(月)", time(8, 58), time(18, 7)),
    ("11/3(火)", time(9, 2), time(18, 14)),
    ("11/4(水)", time(8, 45), time(19, 0)),
    ("11/5(木)", time(9, 10), time(17, 59)),
    ("11/6(金)", time(8, 50), time(18, 29)),
]
for r, (d, a, b) in enumerate(rows, 2):
    ws.cell(r, 1, d)
    ws.cell(r, 2, a).number_format = "h:mm"
    ws.cell(r, 3, b).number_format = "h:mm"
    ws.cell(r, 4, f"=CEILING(ROUND(B{r}*1440,0),$K$2)/1440").number_format = "h:mm"
    ws.cell(r, 5, f"=FLOOR(ROUND(C{r}*1440,0),$K$2)/1440").number_format = "h:mm"
    ws.cell(r, 6, f"=E{r}-D{r}").number_format = "h:mm"
    ws.cell(r, 7, f"=C{r}-B{r}").number_format = "h:mm"
    ws.cell(r, 8, f"=ROUND((G{r}-F{r})*1440,0)").number_format = "0"
ws["A7"] = "合計"; ws["A7"].font = Font(bold=True)
ws["F7"] = "=SUM(F2:F6)"; ws["F7"].number_format = "[h]:mm"
ws["G7"] = "=SUM(G2:G6)"; ws["G7"].number_format = "[h]:mm"
ws["H7"] = "=SUM(H2:H6)"; ws["H7"].number_format = "0"
ws["A8"] = "合計だけ丸める"; ws["A8"].font = Font(bold=True)
ws["G8"] = "=FLOOR(ROUND(G7*1440,0),$K$2)/1440"; ws["G8"].number_format = "[h]:mm"
ws["J1"] = "設定"; ws["J1"].font = Font(bold=True); ws["J1"].fill = hd
ws["K1"] = "値"; ws["K1"].font = Font(bold=True); ws["K1"].fill = hd
ws["J2"] = "丸める単位(分)"; ws["K2"] = 15
ws["A10"] = "※ K2 を 30 や 10 に変えると、丸める単位が変わります。"
for col, w in zip("ABCDEFGHIJK", (14, 12, 12, 18, 18, 14, 14, 8, 3, 16, 6)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
