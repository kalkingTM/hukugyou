import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';
import { CATEGORIES } from '../site';
export const GET: APIRoute = async ({ site }) => {
  const base = import.meta.env.BASE_URL;
  const posts = await getCollection('posts');
  const paths = ['', 'about/', 'privacy/', 'contact/', ...CATEGORIES.map((c) => `category/${c.slug}/`), ...posts.map((p) => `posts/${p.id}/`)];
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${paths
    .map((p) => `  <url><loc>${new URL(base + p, site)}</loc></url>`)
    .join('\n')}\n</urlset>\n`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
};
