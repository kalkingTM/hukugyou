import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';
import { CATEGORIES, SITE, catOf } from '../site';

// AI向けのサイト案内（llms.txt 形式）。各記事の要点へのリンク集。
export const GET: APIRoute = async ({ site }) => {
  const base = import.meta.env.BASE_URL;
  const abs = (p: string) => new URL(base + p, site).href;
  const posts = (await getCollection('posts')).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  const sections = CATEGORIES.map((c) => {
    const list = posts.filter((p) => p.data.category === c.name);
    if (!list.length) return '';
    return `## ${c.name}\n\n${list.map((p) => `- [${p.data.title}](${abs(`posts/${p.id}/`)}): ${p.data.description}`).join('\n')}\n`;
  }).filter(Boolean).join('\n');
  const body = `# ${SITE.name}\n\n> ${SITE.description}\n\n` +
    `- 対象読者: 仕事でExcelを使う会社員（VBA・マクロは使わない）\n` +
    `- 各記事の数式は、見本ファイル(.xlsx)に入れて計算し直し、記事中の結果と一致することを確認して掲載している\n` +
    `- 記事は生成AI（Claude）で作成している。運営者情報: ${abs('about/')}\n\n` +
    sections;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
