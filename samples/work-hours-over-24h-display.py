"""見本: 勤務時間の合計が24時間を超えても正しく表示する"""
from datetime import time
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/work-hours-over-24h-display.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "合計時間"
hd = PatternFill("solid", fgColor="DDEBF7")
for c, h in enumerate(["日", "実働時間"], 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
days = [("11/2(月)", time(8, 0)), ("11/3(火)", time(8, 30)), ("11/4(水)", time(9, 15)),
        ("11/5(木)", time(7, 45)), ("11/6(金)", time(10, 0)), ("11/7(土)", time(8, 50))]
for r, (d, t) in enumerate(days, 2):
    ws.cell(r, 1, d)
    ws.cell(r, 2, t).number_format = "h:mm"

ws["D1"] = "合計の出し方"; ws["D1"].font = Font(bold=True); ws["D1"].fill = hd
ws["E1"] = "結果"; ws["E1"].font = Font(bold=True); ws["E1"].fill = hd
ws["F1"] = "数式"; ws["F1"].font = Font(bold=True); ws["F1"].fill = hd
items = [
    ("表示形式 h:mm（24時間を超えるとずれる）", "=SUM(B2:B7)", "h:mm", "=SUM(B2:B7)"),
    ("表示形式 [h]:mm（正しい）", "=SUM(B2:B7)", "[h]:mm", "=SUM(B2:B7)"),
    ("小数の時間", "=ROUND(SUM(B2:B7)*24,2)", "0.00", "=ROUND(SUM(B2:B7)*24,2)"),
    ("文字列「○時間○分」", '=INT(ROUND(SUM(B2:B7)*1440,0)/60)&"時間"&MOD(ROUND(SUM(B2:B7)*1440,0),60)&"分"', "General",
     '=INT(ROUND(SUM(B2:B7)*1440,0)/60)&"時間"&MOD(ROUND(SUM(B2:B7)*1440,0),60)&"分"'),
]
for i, (lab, f, fmt, shown) in enumerate(items, 2):
    ws.cell(i, 4, lab)
    ws.cell(i, 5, f).number_format = fmt
    ws.cell(i, 6, "'" + shown if False else shown.replace("=", "", 1)).number_format = "@"

ws["D7"] = "時給"; ws["E7"] = 1200
ws["D8"] = "金額（円）"; ws["E8"] = "=ROUND(SUM(B2:B7)*24*E7,0)"; ws["E8"].number_format = "#,##0"
ws["A9"] = "※ 時間の合計は、セルの表示形式を [h]:mm にすると24時間を超えても表示が崩れません。"
for col, w in zip("ABCDEF", (10, 10, 3, 38, 14, 70)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
