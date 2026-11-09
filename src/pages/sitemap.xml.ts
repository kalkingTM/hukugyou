import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';
import { CATEGORIES } from '../site';

const day = (d: Date) => d.toISOString().slice(0, 10);

export const GET: APIRoute = async ({ site }) => {
  const base = import.meta.env.BASE_URL;
  const posts = (await getCollection('posts')).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  const latest = posts[0] ? day(posts[0].data.updated ?? posts[0].data.date) : undefined;
  const loc = (p: string) => new URL(base + p, site).href;
  const entries: { path: string; lastmod?: string }[] = [
    { path: '', lastmod: latest },
    ...CATEGORIES.map((c) => ({
      path: `category/${c.slug}/`,
      lastmod: day((posts.find((p) => p.data.category === c.name)?.data.date) ?? new Date()),
    })),
    { path: 'about/' },
    ...posts.map((p) => ({ path: `posts/${p.id}/`, lastmod: day(p.data.updated ?? p.data.date) })),
  ];
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries
    .map((e) => `  <url><loc>${loc(e.path)}</loc>${e.lastmod ? `<lastmod>${e.lastmod}</lastmod>` : ''}</url>`)
    .join('\n')}\n</urlset>\n`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
