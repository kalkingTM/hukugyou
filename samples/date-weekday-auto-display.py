"""見本: 日付から曜日を自動表示する（TEXT関数・表示形式・CHOOSE+WEEKDAY）"""
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/date-weekday-auto-display.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "曜日表示"

heads = ["日付(入力)", "TEXT aaa", "TEXT aaaa", "日付+曜日(1セル)", "表示形式だけ", "WEEKDAY", "CHOOSE(独自表記)"]
for c, h in enumerate(heads, start=1):
    cell = ws.cell(1, c, h)
    cell.font = Font(bold=True)
    cell.fill = PatternFill("solid", fgColor="DDEBF7")

dates = [date(2026, 11, d) for d in (1, 2, 3, 4, 5, 6, 7)]
for r, d in enumerate(dates, start=2):
    ws.cell(r, 1, d).number_format = "yyyy/m/d"
    ws.cell(r, 2, f'=TEXT(A{r},"aaa")')
    ws.cell(r, 3, f'=TEXT(A{r},"aaaa")')
    ws.cell(r, 4, f'=TEXT(A{r},"yyyy/m/d(aaa)")')
    ws.cell(r, 5, f"=A{r}").number_format = "m/d(aaa)"
    ws.cell(r, 6, f"=WEEKDAY(A{r})")
    ws.cell(r, 7, f'=CHOOSE(WEEKDAY(A{r}),"日(休)","月","火","水","木","金","土(休)")')

ws["A10"] = "空白セル対策"
ws["A11"] = None
ws["B11"] = '=IF(A11="","未入力",TEXT(A11,"aaa"))'
ws["A13"] = "※ A列の日付を書き換えると、B〜G列が自動で変わります。"
for col, w in zip("ABCDEFG", (13, 10, 11, 20, 14, 10, 18)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
