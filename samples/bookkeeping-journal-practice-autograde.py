"""見本: 仕訳の練習問題を自動採点する（自作の問題。IF/AND/TRIM/COUNTIF）"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

OUT = "public/files/bookkeeping-journal-practice-autograde.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "問題と回答"
key = wb.create_sheet("正解")
hd = PatternFill("solid", fgColor="DDEBF7")
inp = PatternFill("solid", fgColor="FFF2CC")

probs = [
    ("現金100,000円を元手に、事業を始めた", "現金", 100000, "資本金", 100000),
    ("商品30,000円を、代金後払い（掛け）で仕入れた", "仕入", 30000, "買掛金", 30000),
    ("商品50,000円を、現金で売り上げた", "現金", 50000, "売上", 50000),
    ("文房具3,000円を現金で買い、消耗品費で処理した", "消耗品費", 3000, "現金", 3000),
    ("売掛金80,000円が、普通預金に振り込まれた", "普通預金", 80000, "売掛金", 80000),
]
# 回答の見本（2問目は借方と貸方を逆に、4問目は貸方金額を誤って入力）
answers = [
    ("現金", 100000, "資本金", 100000),
    ("買掛金", 30000, "仕入", 30000),
    ("現金", 50000, "売上", 50000),
    ("消耗品費", 3000, "現金", 300),
    ("普通預金", 80000, "売掛金", 80000),
]
heads = ["No", "取引", "借方科目", "借方金額", "貸方科目", "貸方金額", "判定"]
for sh in (ws, key):
    for c, h in enumerate(heads if sh is ws else heads[:6], 1):
        x = sh.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
for i, (t, dk, dm, ck, cm) in enumerate(probs):
    r = i + 2
    ws.cell(r, 1, i + 1); ws.cell(r, 2, t)
    a = answers[i]
    for c, v in zip((3, 4, 5, 6), a):
        x = ws.cell(r, c, v); x.fill = inp
        if c in (4, 6): x.number_format = "#,##0"
    ws.cell(r, 7, f'=IF(COUNTA(C{r}:F{r})=0,"",IF(AND(TRIM(C{r})=正解!C{r},D{r}=正解!D{r},TRIM(E{r})=正解!E{r},F{r}=正解!F{r}),"○","×"))')
    key.cell(r, 1, i + 1); key.cell(r, 2, t)
    for c, v in zip((3, 4, 5, 6), (dk, dm, ck, cm)):
        x = key.cell(r, c, v)
        if c in (4, 6): x.number_format = "#,##0"
ws["I1"] = "結果"; ws["I1"].font = Font(bold=True); ws["I1"].fill = hd
ws["J1"] = "値"; ws["J1"].font = Font(bold=True); ws["J1"].fill = hd
ws["I2"] = "正解数"; ws["J2"] = '=COUNTIF(G2:G6,"○")'
ws["I3"] = "回答した問数"; ws["J3"] = '=COUNTIF(G2:G6,"○")+COUNTIF(G2:G6,"×")'
ws["I4"] = "正答率"; ws["J4"] = '=IF(J3=0,"",J2/J3)'; ws["J4"].number_format = "0%"
ws["A8"] = "※ 黄色のセルに回答を入力します。判定は「正解」シートと見比べて自動で出ます。問題は練習用に作った架空の取引です。"
dv = DataValidation(type="list", formula1='"現金,普通預金,売掛金,買掛金,資本金,売上,仕入,消耗品費"', allow_blank=True)
ws.add_data_validation(dv); dv.add("C2:C6"); dv.add("E2:E6")
for sh, w in ((ws, (5, 46, 12, 12, 12, 12, 8, 3, 14, 8)), (key, (5, 46, 12, 12, 12, 12))):
    for col, x in zip("ABCDEFGHIJ", w):
        sh.column_dimensions[col].width = x
wb.save(OUT)
