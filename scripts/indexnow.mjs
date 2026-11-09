// IndexNow: 新しく公開・更新した記事のURLを Bing などの検索エンジンに知らせる。
// 使い方: node scripts/indexnow.mjs [--dry] [--all]
//   既定  … 直前のコミットで変わった記事（とトップページ）だけ通知する
//   --all … サイトマップの全URLを通知する（初回や大きな変更のあと用）
//   --dry … 送信せず、送る内容を表示するだけ
import { execSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync } from 'node:fs';

const HOST = 'kalkingtm.github.io';
const BASE = `https://${HOST}/hukugyou/`;
const dry = process.argv.includes('--dry');
const all = process.argv.includes('--all');

const keyFile = readdirSync('public').find((f) => /^[0-9a-f]{32}\.txt$/.test(f));
if (!keyFile) { console.error('鍵ファイル(public/<32桁>.txt)が見つかりません'); process.exit(1); }
const key = keyFile.replace('.txt', '');
if (readFileSync(`public/${keyFile}`, 'utf8').trim() !== key) { console.error('鍵ファイルの中身が名前と一致しません'); process.exit(1); }

let urls = [];
if (all) {
  const xml = readFileSync('dist/sitemap.xml', 'utf8');
  urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
} else {
  let changed = [];
  try {
    changed = execSync('git diff --name-only --diff-filter=AM HEAD~1 HEAD', { encoding: 'utf8' }).split('\n').filter(Boolean);
  } catch { console.log('直前のコミットが取得できないため、通知するURLはありません'); }
  const slugs = changed
    .map((f) => f.match(/^src\/content\/posts\/(.+)\.md$/)?.[1])
    .filter((s) => s && existsSync(`src/content/posts/${s}.md`));
  if (slugs.length) urls = [BASE, ...slugs.map((s) => `${BASE}posts/${s}/`)];
}

if (!urls.length) { console.log('通知する新しい記事はありません'); process.exit(0); }
console.log(`通知するURL (${urls.length}件):\n${urls.map((u) => '  ' + u).join('\n')}`);
if (dry) process.exit(0);

const res = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: HOST, key, keyLocation: `${BASE}${keyFile}`, urlList: urls }),
});
console.log(`IndexNow 応答: ${res.status} ${res.statusText}`);
// 200 = 受付済み / 202 = 受付済み（鍵の確認待ち）。それ以外は失敗として終了コードで知らせる。
if (![200, 202].includes(res.status)) { console.log(await res.text()); process.exit(1); }
