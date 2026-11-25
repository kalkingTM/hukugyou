"""見本: 定額法の減価償却費を、月割で期ごとに計算する表"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/depreciation-straight-line-monthly.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "減価償却表"
hd = PatternFill("solid", fgColor="DDEBF7")
inp = PatternFill("solid", fgColor="FFF2CC")
bold = Font(bold=True)

labels = ["取得価額", "耐用年数", "償却率", "事業供用日", "決算月", "初年度の月数", "年間償却額(満年分)"]
for r, t in enumerate(labels, 1):
    ws.cell(r, 1, t).font = bold
ws["B1"] = 600000; ws["B1"].number_format = "#,##0"
ws["B2"] = 5
ws["B3"] = "=VLOOKUP(B2,$G$2:$H$9,2,FALSE)"; ws["B3"].number_format = "0.000"
ws["B4"] = date(2026, 10, 15); ws["B4"].number_format = "yyyy/m/d"
ws["B5"] = 3
ws["B6"] = "=MOD(B5-MONTH(B4),12)+1"
ws["B7"] = "=ROUNDDOWN(B1*B3,0)"; ws["B7"].number_format = "#,##0"
for c in ("B1", "B2", "B4", "B5"):
    ws[c].fill = inp

for c, h in enumerate(["耐用年数", "償却率"], 7):
    x = ws.cell(1, c, h); x.font = bold; x.fill = hd
rates = [(3, 0.334), (4, 0.250), (5, 0.200), (6, 0.167), (7, 0.143), (8, 0.125), (9, 0.112), (10, 0.100)]
for r, (y, k) in enumerate(rates, 2):
    ws.cell(r, 7, y)
    ws.cell(r, 8, k).number_format = "0.000"

for c, h in enumerate(["期", "期末日", "期首帳簿価額", "償却額", "期末帳簿価額"], 1):
    x = ws.cell(11, c, h); x.font = bold; x.fill = hd
for i in range(1, 7):
    r = 11 + i
    ws.cell(r, 1, i)
    ws.cell(r, 2, f"=EOMONTH(DATE(YEAR($B$4)+(MONTH($B$4)>$B$5)+A{r}-1,$B$5,1),0)").number_format = "yyyy/m/d"
    ws.cell(r, 3, "=B1" if i == 1 else f"=E{r-1}").number_format = "#,##0"
    ws.cell(r, 4, f"=MIN(IF(A{r}=1,ROUNDDOWN($B$1*$B$3*$B$6/12,0),$B$7),C{r}-1)").number_format = "#,##0"
    ws.cell(r, 5, f"=C{r}-D{r}").number_format = "#,##0"
for col, w in zip("ABCDEFGH", (20, 13, 14, 12, 14, 3, 10, 8)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
