"""見本: 請求一覧と入金一覧を請求番号で突き合わせる（入金消込）"""
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = "public/files/payment-reconcile-match.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "請求一覧"
hd = PatternFill("solid", fgColor="DDEBF7")
heads = ["請求番号", "取引先", "請求額", "入金合計", "差額", "状態"]
for c, h in enumerate(heads, 1):
    x = ws.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
inv = [("INV-001", "青山商事", 110000), ("INV-002", "大和工業", 55000),
       ("INV-003", "北斗物産", 220000), ("INV-004", "みなと食品", 33000),
       ("INV-005", "山田設計", 88000), ("INV-006", "光洋運輸", 143000)]
for r, (n, t, a) in enumerate(inv, 2):
    ws.cell(r, 1, n); ws.cell(r, 2, t)
    ws.cell(r, 3, a).number_format = "#,##0"
    ws.cell(r, 4, f"=SUMIF(入金一覧!$B$2:$B$8,A{r},入金一覧!$C$2:$C$8)").number_format = "#,##0"
    ws.cell(r, 5, f"=C{r}-D{r}").number_format = "#,##0"
    ws.cell(r, 6, f'=IF(D{r}=0,"未入金",IF(E{r}=0,"消込済",IF(E{r}>0,"不足あり","過入金")))')
ws["A8"] = "合計"; ws["A8"].font = Font(bold=True)
for col in "CDE":
    ws[f"{col}8"] = f"=SUM({col}2:{col}7)"; ws[f"{col}8"].number_format = "#,##0"
ws["H1"] = "集計"; ws["H1"].font = Font(bold=True); ws["H1"].fill = hd
for i, s in enumerate(["消込済", "不足あり", "過入金", "未入金"], 2):
    ws.cell(i, 8, s); ws.cell(i, 9, f'=COUNTIF($F$2:$F$7,H{i})')

w2 = wb.create_sheet("入金一覧")
for c, h in enumerate(["入金日", "請求番号", "入金額", "照合"], 1):
    x = w2.cell(1, c, h); x.font = Font(bold=True); x.fill = hd
dep = [(date(2026, 11, 5), "INV-001", 110000), (date(2026, 11, 8), "INV-002", 54450),
       (date(2026, 11, 10), "INV-003", 100000), (date(2026, 11, 12), "INV-003", 120000),
       (date(2026, 11, 15), "INV-005", 88000), (date(2026, 11, 18), "INV-007", 66000),
       (date(2026, 11, 25), "INV-005", 88000)]
for r, (d, n, a) in enumerate(dep, 2):
    w2.cell(r, 1, d).number_format = "m/d"
    w2.cell(r, 2, n)
    w2.cell(r, 3, a).number_format = "#,##0"
    w2.cell(r, 4, f'=IF(COUNTIF(請求一覧!$A$2:$A$7,B{r})=0,"請求なし","照合済み")')
w2["A9"] = "合計"; w2["A9"].font = Font(bold=True)
w2["C9"] = "=SUM(C2:C8)"; w2["C9"].number_format = "#,##0"
for ws_ in (ws, w2):
    for col, w in zip("ABCDEFGHI", (12, 14, 12, 12, 12, 12, 3, 10, 6)):
        ws_.column_dimensions[col].width = w
wb.save(OUT)
