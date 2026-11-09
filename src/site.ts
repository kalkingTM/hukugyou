export const SITE = {
  name: 'しごとExcelレシピ',
  tagline: '仕事で使うExcelの数式と手順',
  description:
    '会社で使うExcelの困りごとを、1記事1問題で解説します。各記事に数式入りの見本ファイルが付き、掲載前に数式を計算し直して確認しています。',
};

// Search Console / Bing Webmaster の所有確認トークン（取得したらここに貼る）
export const VERIFY = { google: 'O3u0-Jq7lQOlQ3Week93jbpwS8OP0YdYJByAiMrglyM', bing: '' };

export const url = (p: string) => `${import.meta.env.BASE_URL}${p.replace(/^\//, '')}`;

export const CATEGORIES = [
  { name: '事務効率化', slug: 'jimu', lead: 'シフト表・日付・勤怠・期限管理など、毎日の事務作業' },
  { name: 'データ整理', slug: 'data', lead: '重複・表記ゆれ・CSV・名簿の突き合わせなど、データの整形' },
  { name: '集計・分析', slug: 'shukei', lead: '条件付き集計・順位・前年比・在庫など、数字のまとめ方' },
  { name: '書類・帳票', slug: 'chohyo', lead: '請求書・見積書・精算書・印刷設定など、書類づくり' },
  { name: '経理', slug: 'keiri', lead: '売掛金・減価償却・資金繰り・消費税など、経理実務' },
] as const;

export type CategoryName = (typeof CATEGORIES)[number]['name'];
export const catOf = (name: string) => CATEGORIES.find((c) => c.name === name) ?? CATEGORIES[0];

const jst = (d: Date) => new Date(d.getTime() + 9 * 3600 * 1000);
export const fmtDate = (d: Date) => {
  const j = jst(d);
  return `${j.getUTCFullYear()}年${j.getUTCMonth() + 1}月${j.getUTCDate()}日`;
};
export const fmtDateShort = (d: Date) => {
  const j = jst(d);
  return `${j.getUTCFullYear()}.${String(j.getUTCMonth() + 1).padStart(2, '0')}.${String(j.getUTCDate()).padStart(2, '0')}`;
};
