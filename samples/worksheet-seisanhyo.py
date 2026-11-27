"""見本: 試算表+修正記入から損益計算書・貸借対照表の欄を自動で振り分ける精算表（自作の架空データ）"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

OUT = "public/files/worksheet-seisanhyo.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "精算表"
hd = PatternFill("solid", fgColor="DDEBF7")
inp = PatternFill("solid", fgColor="FFF2CC")
bold = Font(bold=True)

ws["A1"] = "勘定科目"; ws["B1"] = "区分"
ws["C1"] = "試算表"; ws["E1"] = "修正記入"; ws["G1"] = "損益計算書"; ws["I1"] = "貸借対照表"
for rng in ("A1:A2", "B1:B2"):
    ws.merge_cells(rng)
for rng in ("C1:D1", "E1:F1", "G1:H1", "I1:J1"):
    ws.merge_cells(rng)
for c, h in enumerate(["借方", "貸方"] * 4, 3):
    ws.cell(2, c, h)
for row in (1, 2):
    for c in range(1, 11):
        x = ws.cell(row, c); x.font = bold; x.fill = hd
        x.alignment = Alignment(horizontal="center")

# 勘定科目, 区分, 試算借, 試算貸, 修正借, 修正貸
data = [
    ("現金", "資産", 150000, None, None, None),
    ("普通預金", "資産", 400000, None, None, None),
    ("売掛金", "資産", 300000, None, None, None),
    ("繰越商品", "資産", 80000, None, 90000, 80000),
    ("備品", "資産", 600000, None, None, 100000),
    ("買掛金", "負債", None, 200000, None, None),
    ("貸倒引当金", "資産", None, None, None, 3000),
    ("資本金", "純資産", None, 1000000, None, None),
    ("売上", "収益", None, 1350000, None, None),
    ("仕入", "費用", 700000, None, 80000, 90000),
    ("給料", "費用", 200000, None, None, None),
    ("支払家賃", "費用", 120000, None, None, None),
    ("減価償却費", "費用", None, None, 100000, None),
    ("貸倒引当金繰入", "費用", None, None, 3000, None),
]
first = 3
last = first + len(data) - 1  # 16
for i, (name, kind, c, d, e, f) in enumerate(data):
    r = first + i
    ws.cell(r, 1, name); ws.cell(r, 2, kind)
    for col, v in zip((3, 4, 5, 6), (c, d, e, f)):
        cell = ws.cell(r, col, v)
        cell.fill = inp
    pl = f'OR($B{r}="収益",$B{r}="費用")'
    ws.cell(r, 7, f"=IF({pl},MAX(C{r}+E{r}-D{r}-F{r},0),0)")
    ws.cell(r, 8, f"=IF({pl},MAX(D{r}+F{r}-C{r}-E{r},0),0)")
    ws.cell(r, 9, f"=IF({pl},0,MAX(C{r}+E{r}-D{r}-F{r},0))")
    ws.cell(r, 10, f"=IF({pl},0,MAX(D{r}+F{r}-C{r}-E{r},0))")

p = last + 1   # 17 当期純利益
t = last + 2   # 18 合計
ws.cell(p, 1, "当期純利益（損失）")
ws.cell(p, 7, f"=MAX(SUM(H{first}:H{last})-SUM(G{first}:G{last}),0)")
ws.cell(p, 8, f"=MAX(SUM(G{first}:G{last})-SUM(H{first}:H{last}),0)")
ws.cell(p, 9, f"=H{p}")
ws.cell(p, 10, f"=G{p}")
ws.cell(t, 1, "合計").font = bold
for col in "CDEFGHIJ":
    ws[f"{col}{t}"] = f"=SUM({col}{first}:{col}{p})"
    ws[f"{col}{t}"].font = bold
ws.cell(t + 2, 1, "試算表の貸借一致")
ws.cell(t + 2, 2, f'=IF(C{t}=D{t},"一致","不一致")')
ws.cell(t + 3, 1, "修正記入の貸借一致")
ws.cell(t + 3, 2, f'=IF(E{t}=F{t},"一致","不一致")')
ws.cell(t + 4, 1, "精算表の貸借一致")
ws.cell(t + 4, 2, f'=IF(AND(G{t}=H{t},I{t}=J{t}),"一致","不一致")')
for row in ws.iter_rows(min_row=first, max_row=t, min_col=3, max_col=10):
    for cell in row:
        cell.number_format = "#,##0"
ws.column_dimensions["A"].width = 22
ws.column_dimensions["B"].width = 10
for col in "CDEFGHIJ":
    ws.column_dimensions[col].width = 13
wb.save(OUT)
