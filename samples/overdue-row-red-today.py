"""見本: 期限を過ぎた未完了の行を自動で赤くするタスク表"""
from datetime import date

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Font, PatternFill

OUT = "public/files/overdue-row-red-today.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "タスク表"
hd = PatternFill("solid", fgColor="DDEBF7")
inp = PatternFill("solid", fgColor="FFF2CC")
bold = Font(bold=True)

ws["A1"], ws["B1"] = "基準日", date(2026, 11, 27)
ws["B1"].number_format = "yyyy/m/d"; ws["B1"].fill = inp
ws["C1"] = "← 見本は動きを固定するため日付を直接入力。実際に使うときは =TODAY() に置き換えます"
ws["A2"], ws["B2"] = "期限切れの件数", '=COUNTIF(E5:E11,"期限切れ")'
ws["A3"], ws["B3"] = "今日が期限の件数", '=COUNTIF(E5:E11,"今日まで")'

for c, h in enumerate(["作業", "担当", "期限", "完了", "状態", "超過日数"], 1):
    x = ws.cell(4, c, h); x.font = bold; x.fill = hd
rows = [
    ("見積書の送付", "佐藤", date(2026, 11, 20), None),
    ("請求書の発行", "鈴木", date(2026, 11, 26), None),
    ("月次報告の提出", "高橋", date(2026, 11, 27), None),
    ("備品の発注", "田中", date(2026, 11, 30), None),
    ("契約更新の確認", "伊藤", date(2026, 11, 18), "完了"),
    ("交通費の精算", "佐藤", None, None),
    ("会議資料の準備", "鈴木", date(2026, 12, 3), None),
]
for i, (a, b, c, d) in enumerate(rows):
    r = 5 + i
    ws.cell(r, 1, a); ws.cell(r, 2, b)
    ws.cell(r, 3, c).number_format = "yyyy/m/d"
    ws.cell(r, 4, d)
    ws.cell(r, 5, f'=IF(D{r}="完了","完了",IF(C{r}="","期限なし",IF(C{r}<$B$1,"期限切れ",IF(C{r}=$B$1,"今日まで","余裕あり"))))')
    ws.cell(r, 6, f'=IF(E{r}="期限切れ",$B$1-C{r},"")')

red = PatternFill("solid", bgColor="F8CBAD")
yellow = PatternFill("solid", bgColor="FFE699")
grey = PatternFill("solid", bgColor="D9D9D9")
rng = "A5:F11"
ws.conditional_formatting.add(rng, FormulaRule(formula=['$D5="完了"'], fill=grey, font=Font(color="808080"), stopIfTrue=True))
ws.conditional_formatting.add(rng, FormulaRule(formula=['AND($C5<>"",$C5<$B$1)'], fill=red, stopIfTrue=True))
ws.conditional_formatting.add(rng, FormulaRule(formula=['$C5=$B$1'], fill=yellow))
for col, w in zip("ABCDEF", (18, 8, 12, 8, 10, 10)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
