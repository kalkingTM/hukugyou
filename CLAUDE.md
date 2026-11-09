# しごとExcelレシピ — 自動運用ループの規則

このリポジトリは、毎日1回クラウドの定期実行（routine）で起動したClaudeが記事を1本作り、
基準を満たしたものだけを GitHub Pages に公開する、ブログ×アフィリエイトの自動運用サイトである。
公開URL: https://kalkingtm.github.io/hukugyou/ ／ ダッシュボード: /hukugyou/dashboard/

## 1回の実行でやること（`prompts/loop.md` の手順に従う）
1. ネタ選定 → 2. 調査・執筆 → 3. 見本xlsx作成と数式検証 → 4. AIレビュー → 5. 公開 or 不採用 → 6. 記録
1回の実行で公開するのは**最大1本**。迷ったら公開しない（不採用は損失ではない。誤った記事の公開が損失）。

## サイトの方針
- テーマ: 会社員の仕事で使うExcel（事務効率化・データ整理・集計・帳票・経理）。
- 狙う検索語: 「Excel シフト表 自動 土日 色分け」のような**具体的で長い検索語**。「Excel 使い方」などの広い語は狙わない。
- 1記事＝1つの困りごと。読者がその記事だけで解決できること。
- **全記事に見本の .xlsx を付ける**（`public/files/<slug>.xlsx`）。これがAIの回答との差別化要因。
- 読者像: Excelを毎日触るがVBAやマクロは書けない会社員。専門用語は初出で一言説明する。

## 絶対に守ること
- 数式は必ず見本ファイルに入れ、`scripts/verify_xlsx.py` で検証して PASS したものだけを記事に書く。
- 記事に書く計算結果の例（表）は、検証で得た値と一致させる。
- 税務・法律・社会保険の判断を断定しない。制度に触れる場合は一般論にとどめ、一次情報（国税庁・e-Gov・厚労省など）へリンクし「個別の判断は専門家へ」と書く。
- `sources`（参考にした情報）は任意。次の場合だけ付ける: ①Excelのバージョン差がある機能（XLOOKUPはExcel 2021 / Microsoft 365以降 等。Microsoft公式サポートで確認して入れる）、②祝日・税・社会保険など制度やデータが絡む内容（一次情報を入れる）。一般的なテクニックの記事には付けない（付けると水増しに見える）。付けない場合は `sources` 自体を書かない。
- 誇大表現・断定的な効果の約束（「誰でも」「絶対」「必ず稼げる」等）は使わない。
- アフィリエイトリンクを入れた記事は frontmatter `hasAffiliate: true`（記事冒頭に「PR」表示）。リンクは `affiliates.json` に登録された案件だけを使う。自分で作ったり推測したリンクは入れない。
- 記事内容に関係のない案件は入れない。1記事あたりリンクは最大2つ。
- 他サイトの文章をコピーしない。引用は必要最小限。
- 既存記事と同じ困りごとを重ねない（作成前に `src/content/posts/` の keyword/title を確認する）。

## ファイルの役割
| パス | 役割 |
|---|---|
| `topics.md` | ネタ在庫。`- [ ]` 未使用 / `- [x]` 使用済み。上から順に使う |
| `prompts/loop.md` | 1回の実行手順（routine はこれを読んで動く） |
| `prompts/write.md` | 執筆の手順と記事テンプレート |
| `prompts/review.md` | レビューの採点表と合格基準 |
| `samples/<slug>.py` | 見本xlsxを作るスクリプト（再現できるよう残す） |
| `samples/<slug>.spec.json` | 検証用の期待値 |
| `public/files/<slug>.xlsx` | 読者がダウンロードする見本 |
| `src/content/posts/<slug>.md` | 記事本体 |
| `rejected/<日付>-<slug>.md` | 不採用の記事（公開されない） |
| `data/runs.json` | 実行記録。**必ず `node scripts/log-run.mjs` で追記する** |
| `data/revenue.json` | 収益（人が手入力） |
| `affiliates.json` | 提携済みアフィリエイト案件（人が登録） |

## コマンド
- 検証: `python scripts/verify_xlsx.py samples/<slug>.spec.json`
- ビルド確認: `npm run build`
- 記録: `node scripts/log-run.mjs '<JSON>'`
