import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';
import { SITE } from '../site';

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export const GET: APIRoute = async ({ site }) => {
  const base = import.meta.env.BASE_URL;
  const posts = (await getCollection('posts')).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf()).slice(0, 50);
  const home = new URL(base, site).href;
  const items = posts
    .map((p) => {
      const link = new URL(`${base}posts/${p.id}/`, site).href;
      return `    <item>\n      <title>${esc(p.data.title)}</title>\n      <link>${link}</link>\n      <guid isPermaLink="true">${link}</guid>\n      <pubDate>${p.data.date.toUTCString()}</pubDate>\n      <category>${esc(p.data.category)}</category>\n      <description>${esc(p.data.description)}</description>\n    </item>`;
    })
    .join('\n');
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n  <channel>\n    <title>${esc(SITE.name)}</title>\n    <link>${home}</link>\n    <description>${esc(SITE.description)}</description>\n    <language>ja</language>\n${items}\n  </channel>\n</rss>\n`;
  return new Response(body, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
};
