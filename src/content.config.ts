import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(160),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),    // 内容を大きく直したときだけ
    category: z.enum(['経理', '事務効率化', 'データ整理', '集計・分析', '書類・帳票']),
    keyword: z.string(),
    sampleFile: z.string().optional(),      // public/files/ 配下のファイル名
    hasAffiliate: z.boolean().default(false),   // 旧設定。広告は affiliate: [id] で指定する（PR表示も自動）
    affiliate: z.array(z.string()).default([]),  // affiliates.json の id。最大2つ
    sources: z.array(z.string().url()).default([]),   // 任意。バージョン差や制度に触れる記事だけ付ける
  }),
});

export const collections = { posts };
