"""見本: 日付を入れるだけで土日・祝日に色が付くシフト表"""
from datetime import date

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = "public/files/shift-table-weekend-color.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "シフト表"
hol = wb.create_sheet("祝日")

# --- 祝日シート（内閣府「国民の祝日」より。毎年ここに追記する） ---
hol["A1"], hol["B1"] = "日付", "祝日名"
holidays = [
    (date(2026, 11, 3), "文化の日"),
    (date(2026, 11, 23), "勤労感謝の日"),
    (date(2027, 1, 1), "元日"),
    (date(2027, 1, 11), "成人の日"),
]
for i, (d, n) in enumerate(holidays, start=2):
    hol.cell(i, 1, d).number_format = "yyyy/m/d"
    hol.cell(i, 2, n)
hol.column_dimensions["A"].width = 12
hol.column_dimensions["B"].width = 16

# --- シフト表 ---
ws["A1"] = "開始日"
ws["B1"] = date(2026, 11, 1)
ws["B1"].number_format = "yyyy/m/d"
ws["D1"] = "← 月初の日付を入れると表全体が切り替わります"
ws["A3"], ws["A4"], ws["A5"] = "日付", "曜日", "区分"

FIRST, LAST = 2, 32  # B〜AF（31日分）
for c in range(FIRST, LAST + 1):
    col = get_column_letter(c)
    prev = get_column_letter(c - 1)
    if c == FIRST:
        ws[f"{col}3"] = "=$B$1"
    else:
        ws[f"{col}3"] = f'=IF({prev}3="","",IF({prev}3+1>EOMONTH($B$1,0),"",{prev}3+1))'
    ws[f"{col}3"].number_format = "d"
    ws[f"{col}4"] = f'=IF({col}3="","",CHOOSE(WEEKDAY({col}3),"日","月","火","水","木","金","土"))'
    ws[f"{col}5"] = (
        f'=IF({col}3="","",IF(COUNTIF(祝日!$A$2:$A$100,{col}3)>0,"祝",'
        f'IF(WEEKDAY({col}3,2)>5,"土日","")))'
    )
    ws.column_dimensions[col].width = 4.2

staff = ["佐藤", "鈴木", "高橋", "田中", "伊藤"]
for r, name in enumerate(staff, start=6):
    ws.cell(r, 1, name)

ws["A12"] = "土日祝の日数"
ws["B12"] = '=COUNTIF(B5:AF5,"祝")+COUNTIF(B5:AF5,"土日")'
ws["A13"] = "平日の日数"
ws["B13"] = '=COUNT(B3:AF3)-B12'
ws.column_dimensions["A"].width = 13

# 見た目
thin = Side(style="thin", color="BFBFBF")
for row in ws.iter_rows(min_row=3, max_row=10, min_col=1, max_col=LAST):
    for cell in row:
        cell.border = Border(top=thin, bottom=thin, left=thin, right=thin)
        cell.alignment = Alignment(horizontal="center")
for c in ("A3", "A4", "A5"):
    ws[c].font = Font(bold=True)

# 条件付き書式（祝日 → 日曜 → 土曜 の順に優先）
area = f"B3:{get_column_letter(LAST)}10"
red = PatternFill("solid", start_color="FCE4E4", end_color="FCE4E4")
blue = PatternFill("solid", start_color="E3EEFB", end_color="E3EEFB")
ws.conditional_formatting.add(area, FormulaRule(formula=['AND(B$3<>"",COUNTIF(祝日!$A$2:$A$100,B$3)>0)'], fill=red, stopIfTrue=True))
ws.conditional_formatting.add(area, FormulaRule(formula=['AND(B$3<>"",WEEKDAY(B$3)=1)'], fill=red, stopIfTrue=True))
ws.conditional_formatting.add(area, FormulaRule(formula=['AND(B$3<>"",WEEKDAY(B$3)=7)'], fill=blue, stopIfTrue=True))
ws.freeze_panes = "B6"

wb.save(OUT)
print("saved", OUT)
