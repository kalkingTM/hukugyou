// 使い方: node scripts/log-run.mjs '<JSON>'
// 実行結果を data/runs.json に1件追記する（JSONを壊さないため、手で書き換えずに必ずこれを使う）
import { readFileSync, writeFileSync } from 'node:fs';
const FILE = new URL('../data/runs.json', import.meta.url);
const rec = JSON.parse(process.argv[2] ?? '');
const required = ['keyword', 'status', 'stages'];
for (const k of required) if (!(k in rec)) throw new Error(`missing field: ${k}`);
if (!['published', 'rejected', 'error'].includes(rec.status)) throw new Error('status must be published|rejected|error');
const db = JSON.parse(readFileSync(FILE, 'utf8'));
rec.id = db.runs.length + 1;
rec.at ??= new Date().toISOString();
db.runs.push(rec);
writeFileSync(FILE, JSON.stringify(db, null, 2) + '\n');
console.log(`logged run #${rec.id} (${rec.status})`);
