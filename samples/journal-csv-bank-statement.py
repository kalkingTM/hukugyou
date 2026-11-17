"""見本: 通帳明細を仕訳(借方・貸方・金額)の形に変換するシート"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/journal-csv-bank-statement.xlsx"
wb = Workbook()
m = wb.active
m.title = "明細"
j = wb.create_sheet("仕訳")
hd = PatternFill("solid", fgColor="DDEBF7")
for ws, heads in ((m, ["日付", "摘要", "入金額", "出金額", "相手科目"]),
                  (j, ["日付", "借方科目", "借方金額", "貸方科目", "貸方金額", "摘要"])):
    for c, h in enumerate(heads, 1):
        x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
rows = [
    (date(2026, 11, 2), "ABC商事 売上入金", 330000, None, "売上高"),
    (date(2026, 11, 5), "事務所家賃", None, 110000, "地代家賃"),
    (date(2026, 11, 10), "文具店 事務用品", None, 8800, "消耗品費"),
    (date(2026, 11, 14), "電気料金", None, 15400, "水道光熱費"),
    (date(2026, 11, 20), "北山工業 売上入金", 220000, None, "売上高"),
    (date(2026, 11, 25), "通信料", None, 6600, "通信費"),
]
n = len(rows)
for r, (d, t, i, o, k) in enumerate(rows, 2):
    m.cell(r, 1, d).number_format = "yyyy/m/d"
    m.cell(r, 2, t)
    if i: m.cell(r, 3, i)
    if o: m.cell(r, 4, o)
    m.cell(r, 5, k)
    m.cell(r, 3).number_format = m.cell(r, 4).number_format = "#,##0"
    j.cell(r, 1, f'=TEXT(明細!A{r},"yyyy/mm/dd")')
    j.cell(r, 2, f'=IF(明細!C{r}>0,"普通預金",明細!E{r})')
    j.cell(r, 3, f"=明細!C{r}+明細!D{r}").number_format = "#,##0"
    j.cell(r, 4, f'=IF(明細!C{r}>0,明細!E{r},"普通預金")')
    j.cell(r, 5, f"=C{r}").number_format = "#,##0"
    j.cell(r, 6, f"=明細!B{r}")
t = n + 3
j.cell(t, 2, "合計").font = Font(bold=True)
j.cell(t, 3, f"=SUM(C2:C{n+1})").number_format = "#,##0"
j.cell(t, 5, f"=SUM(E2:E{n+1})").number_format = "#,##0"
j.cell(t, 6, f'=IF(C{t}=E{t},"借方と貸方が一致","不一致")')
for ws, ww in ((m, (12, 22, 10, 10, 12)), (j, (12, 12, 12, 12, 12, 22))):
    for col, w in zip("ABCDEF", ww):
        ws.column_dimensions[col].width = w
wb.save(OUT)
