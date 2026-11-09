"""見本: 受注日から○営業日後の納期 (WORKDAY / WORKDAY.INTL)"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/workday-deadline-business-days.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "納期計算"
hd = PatternFill("solid", fgColor="DDEBF7")
def head(c, h):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
for c, h in enumerate(["祝日一覧", "名称"], 1): head(c, h)
for r, (d, n) in enumerate([(date(2026,11,3), "文化の日"), (date(2026,11,23), "勤労感謝の日")], 2):
    ws.cell(r, 1, d).number_format = "yyyy/m/d"
    ws.cell(r, 2, n)
for c, h in enumerate(["受注日", "営業日数", "土日のみ除く", "土日祝を除く", "日曜と祝日のみ除く"], 4): head(c, h)
rows = [(date(2026,10,30), 3), (date(2026,11,20), 3), (date(2026,11,9), 5)]
for r, (s, n) in enumerate(rows, 2):
    ws.cell(r, 4, s).number_format = "yyyy/m/d(aaa)"
    ws.cell(r, 5, n)
    ws.cell(r, 6, f"=WORKDAY(D{r},E{r})").number_format = "yyyy/m/d(aaa)"
    ws.cell(r, 7, f"=WORKDAY(D{r},E{r},$A$2:$A$3)").number_format = "yyyy/m/d(aaa)"
    ws.cell(r, 8, f"=WORKDAY.INTL(D{r},E{r},11,$A$2:$A$3)").number_format = "yyyy/m/d(aaa)"
for c, h in enumerate(["納期", "必要な営業日数", "着手期限"], 10): head(c, h)
for r, (s, n) in enumerate([(date(2026,11,26), 3), (date(2026,11,6), 2)], 2):
    ws.cell(r, 10, s).number_format = "yyyy/m/d(aaa)"
    ws.cell(r, 11, n)
    ws.cell(r, 12, f"=WORKDAY(J{r},-K{r},$A$2:$A$3)").number_format = "yyyy/m/d(aaa)"
ws["A6"] = "※ 祝日一覧(A2:A3)に日付を足したら、数式の範囲も広げてください。"
for col, w in zip("ABCDEFGHIJKL", (13, 14, 3, 16, 10, 16, 16, 20, 3, 16, 14, 16)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
