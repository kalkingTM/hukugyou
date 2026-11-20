"""見本: 生年月日から基準日時点の満年齢を出す（DATEDIF）"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/age-from-birthdate-datedif.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "年齢計算"
hd = PatternFill("solid", fgColor="DDEBF7")
heads = ["名前", "生年月日", "満年齢", "年齢(年とヶ月)", "次の誕生日", "誕生日まで(日)", "365日で割った場合(誤り)"]
for c, h in enumerate(heads, 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    ("田中", date(1990, 4, 15)),
    ("佐藤", date(1985, 11, 21)),
    ("鈴木", date(1998, 12, 1)),
    ("高橋", date(2003, 3, 31)),
    ("伊藤", date(1972, 1, 5)),
    ("山本", date(1990, 11, 25)),
]
for r, (n, b) in enumerate(rows, 2):
    ws.cell(r, 1, n)
    ws.cell(r, 2, b).number_format = "yyyy/m/d"
    ws.cell(r, 3, f'=DATEDIF(B{r},$J$2,"Y")').number_format = "0"
    ws.cell(r, 4, f'=DATEDIF(B{r},$J$2,"Y")&"歳"&DATEDIF(B{r},$J$2,"YM")&"ヶ月"')
    ws.cell(r, 5, f"=EDATE(B{r},12*(C{r}+1))").number_format = "yyyy/m/d"
    ws.cell(r, 6, f"=E{r}-$J$2").number_format = "0"
    ws.cell(r, 7, f"=INT(($J$2-B{r})/365)").number_format = "0"
ws["I1"] = "設定"; ws["I1"].font = Font(bold=True); ws["I1"].fill = hd
ws["J1"] = "値"; ws["J1"].font = Font(bold=True); ws["J1"].fill = hd
ws["I2"] = "基準日"; ws["J2"] = date(2026, 11, 21); ws["J2"].number_format = "yyyy/m/d"
ws["A9"] = "※ 基準日(J2)を =TODAY() に替えると、開くたびに今日の日付で再計算されます。"
for col, w in zip("ABCDEFGHIJ", (8, 12, 8, 16, 12, 14, 24, 3, 8, 12)):
    ws.column_dimensions[col].width = w
wb.save(OUT)
