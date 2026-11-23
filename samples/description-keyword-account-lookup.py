"""見本: 摘要のキーワードから勘定科目を自動で振り分ける（INDEX/MATCH/SEARCH）"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/description-keyword-account-lookup.xlsx"
wb = Workbook()
m = wb.active
m.title = "明細"
k = wb.create_sheet("科目表")
hd = PatternFill("solid", fgColor="DDEBF7")
for ws, heads in ((m, ["日付", "摘要", "金額", "勘定科目(自動)", "一致したキーワード"]),
                  (k, ["キーワード", "勘定科目"])):
    for c, h in enumerate(heads, 1):
        x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
kw = [("売上", "売上高"), ("家賃", "地代家賃"), ("文具", "消耗品費"), ("事務用品", "消耗品費"),
      ("電気", "水道光熱費"), ("水道", "水道光熱費"), ("電話", "通信費"), ("通信", "通信費"),
      ("振込手数料", "支払手数料"), ("切手", "通信費")]
for r, (a, b) in enumerate(kw, 2):
    k.cell(r, 1, a); k.cell(r, 2, b)
rows = [
    (date(2026, 11, 2), "ABC商事 売上入金", 330000),
    (date(2026, 11, 5), "事務所家賃 11月分", 110000),
    (date(2026, 11, 10), "文具店 事務用品", 8800),
    (date(2026, 11, 14), "電気料金", 15400),
    (date(2026, 11, 18), "携帯電話料金", 6600),
    (date(2026, 11, 20), "振込手数料", 440),
    (date(2026, 11, 22), "タクシー代", 3200),
    (date(2026, 11, 25), "北山工業 売上入金 振込手数料差引", 219560),
]
last = len(kw) + 1
n = len(rows)
for r, (d, t, v) in enumerate(rows, 2):
    m.cell(r, 1, d).number_format = "yyyy/m/d"
    m.cell(r, 2, t)
    m.cell(r, 3, v).number_format = "#,##0"
    pos = f"MATCH(1,INDEX(--ISNUMBER(SEARCH(科目表!$A$2:$A${last},B{r})),0),0)"
    m.cell(r, 4, f'=IFERROR(INDEX(科目表!$B$2:$B${last},{pos}),"要確認")')
    m.cell(r, 5, f'=IFERROR(INDEX(科目表!$A$2:$A${last},{pos}),"")')
m.cell(n + 3, 2, "要確認の件数").font = Font(bold=True)
m.cell(n + 3, 3, f'=COUNTIF(D2:D{n+1},"要確認")')
for ws, ww in ((m, (12, 34, 12, 16, 18)), (k, (14, 14))):
    for col, w in zip("ABCDE", ww):
        ws.column_dimensions[col].width = w
wb.save(OUT)
