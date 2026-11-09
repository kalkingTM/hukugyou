import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(160),
    date: z.coerce.date(),
    category: z.enum(['経理', '事務効率化', 'データ整理', '集計・分析', '書類・帳票']),
    keyword: z.string(),
    sampleFile: z.string().optional(),      // public/files/ 配下のファイル名
    hasAffiliate: z.boolean().default(false),
    sources: z.array(z.string().url()).default([]),   // 任意。バージョン差や制度に触れる記事だけ付ける
  }),
});

export const collections = { posts };
