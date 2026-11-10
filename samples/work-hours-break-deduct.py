"""見本: 出勤・退勤・休憩から実働時間を出す"""
from datetime import time
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/work-hours-break-deduct.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "勤務時間"
hd = PatternFill("solid", fgColor="DDEBF7")
heads = ["日付メモ", "出勤", "退勤", "休憩", "実働時間", "実働(時間・小数)", "休憩(分)", "実働時間(休憩を分で入力)"]
for c, h in enumerate(heads, 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    ("通常勤務", time(9, 0), time(18, 0), time(1, 0), 60),
    ("休憩45分", time(8, 30), time(17, 45), time(0, 45), 45),
    ("残業あり", time(10, 0), time(19, 30), time(1, 0), 60),
    ("日またぎ", time(22, 0), time(6, 0), time(1, 0), 60),
    ("未入力", None, None, None, None),
]
for r, (m, a, b, k, km) in enumerate(rows, 2):
    ws.cell(r, 1, m)
    for c, v in ((2, a), (3, b), (4, k)):
        if v is not None:
            ws.cell(r, c, v)
        ws.cell(r, c).number_format = "h:mm"
    ws.cell(r, 5, f'=IF(OR(B{r}="",C{r}=""),"",MOD(C{r}-B{r},1)-D{r})').number_format = "h:mm"
    ws.cell(r, 6, f'=IF(E{r}="","",ROUND(E{r}*24,2))').number_format = "0.00"
    if km is not None:
        ws.cell(r, 7, km)
    ws.cell(r, 8, f'=IF(OR(B{r}="",C{r}=""),"",MOD(C{r}-B{r},1)-G{r}/1440)').number_format = "h:mm"
ws["A8"] = "合計"; ws["A8"].font = Font(bold=True)
ws["E8"] = "=SUM(E2:E6)"; ws["E8"].number_format = "[h]:mm"
ws["F8"] = "=SUM(F2:F6)"; ws["F8"].number_format = "0.00"
ws["A10"] = "※ 退勤が出勤より早い(日またぎ)場合も MOD で正しく計算します。休憩は『時刻の形(1:00)』で入れます。"
for col, w in zip("ABCDEFGH", (12, 8, 8, 8, 12, 16, 10, 24)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
