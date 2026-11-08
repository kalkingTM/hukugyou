"""見本: 土日祝を除いた営業日数 (NETWORKDAYS / NETWORKDAYS.INTL)"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/networkdays-holidays-exclude.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "営業日数"
hd = PatternFill("solid", fgColor="DDEBF7")
for c, h in enumerate(["祝日一覧", "名称"], 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
for r, (d, n) in enumerate([(date(2026,11,3), "文化の日"), (date(2026,11,23), "勤労感謝の日")], 2):
    ws.cell(r, 1, d).number_format = "yyyy/m/d"
    ws.cell(r, 2, n)
for c, h in enumerate(["開始日", "終了日", "土日のみ除く", "土日祝を除く", "日曜と祝日のみ除く"], 4):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [(date(2026,11,1), date(2026,11,30)), (date(2026,11,2), date(2026,11,6)), (date(2026,11,2), date(2026,11,4))]
for r, (s, e) in enumerate(rows, 2):
    ws.cell(r, 4, s).number_format = "yyyy/m/d"
    ws.cell(r, 5, e).number_format = "yyyy/m/d"
    ws.cell(r, 6, f"=NETWORKDAYS(D{r},E{r})")
    ws.cell(r, 7, f"=NETWORKDAYS(D{r},E{r},$A$2:$A$3)")
    ws.cell(r, 8, f"=NETWORKDAYS.INTL(D{r},E{r},11,$A$2:$A$3)")
ws["A6"] = "※ 祝日一覧(A2:A3)に日付を足したら、範囲を広げてください。"
for col, w in zip("ABCDEFGH", (13, 14, 3, 12, 12, 14, 14, 20)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
