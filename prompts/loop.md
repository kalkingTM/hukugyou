# 毎日の実行手順（routine はこのファイルを上から実行する）

まず `CLAUDE.md` を読むこと。

## 0. 準備
- `git pull` で最新にする。
- `npm ci` と `pip install -r requirements.txt` を実行する（入っていれば省略可）。
- 可能なら LibreOffice を入れる（`sudo apt-get install -y libreoffice-calc` などで入れる。入れられなければ `formulas` での検証で進めてよい）。
- 今日の日付(JST)で `src/content/posts/` に記事がすでにあれば、何もせずに終了する（1日1本の上限）。

## 1. ネタ選定
- `topics.md` の一番上の `- [ ]` を1つ選ぶ。既存記事と困りごとが重なる場合は `- [x] (重複のためスキップ)` にして次を選ぶ。
- 未使用が20件を切っていたら、同じ方針（具体的で長い検索語、1記事＝1つの困りごと）で30件を末尾に補充する。
- slug は英小文字とハイフンで作る（例: `shift-table-weekend-color`）。

## 2. 調査・執筆 → `prompts/write.md`
## 3. 見本xlsxと検証
- `samples/<slug>.py` を書いて `public/files/<slug>.xlsx` を作る（openpyxl。数式は文字列で入れる）。
- `samples/<slug>.spec.json` に、記事に書く計算結果の例を期待値として書く（最低3か所）。
- `python scripts/verify_xlsx.py samples/<slug>.spec.json` を実行する。
- FAIL なら原因を直して再実行してよい（最大2回）。それでも FAIL なら不採用。
  計算エンジンが対応していない関数で ERROR になった場合は、同じことができる別の数式に変えるか、不採用にする。

## 4. AIレビュー → `prompts/review.md`
- 執筆したときの意図に引きずられないよう、**記事ファイルと見本だけを読み直して**採点する。
- 合格基準を満たさなければ、指摘を1回だけ直して再採点してよい。それでも不合格なら不採用。

## 5. 公開 or 不採用
- 合格: 記事を `src/content/posts/<slug>.md` に置き、`npm run build` が通ることを確認する。
- 不採用: 記事を `rejected/<YYYY-MM-DD>-<slug>.md` に移し、見本xlsxは削除する。
- どちらの場合も `topics.md` の該当行を `- [x]` にする。

## 6. 記録とpush
```
node scripts/log-run.mjs '{"keyword":"<検索語>","slug":"<公開時のみ>","status":"published|rejected|error","score":<点数>,"stages":{"select":"ok","write":"ok","verify":"ok|ng","review":"pass|fail","publish":"ok|skipped"},"reasons":["<不採用やエラーの理由>"],"note":"<一言>"}'
```
- `git add -A && git commit -m "post: <slug>"`（不採用は `"reject: <slug>"`）して `main` に push する。
- 途中でエラーになっても、可能な限り status `error` で記録して push してから終了する（ダッシュボードで止まったことが分かるように）。
