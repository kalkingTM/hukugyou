export const SITE = {
  name: 'しごとExcelレシピ',
  tagline: 'コピペで使える、検証済みの仕事用Excelレシピ集',
  description:
    '会社員の「Excelでこれやりたい」を1記事1レシピで解決。すべての数式を見本ファイルで実際に計算して確かめてから掲載しています。',
};

export const url = (p: string) => `${import.meta.env.BASE_URL}${p.replace(/^\//, '')}`;

export const CATEGORIES = [
  { name: '事務効率化', slug: 'jimu', color: 'var(--c-jimu)', lead: 'シフト表・日付・勤怠・期限管理など、毎日の事務作業をラクにするレシピ' },
  { name: 'データ整理', slug: 'data', color: 'var(--c-data)', lead: '重複・表記ゆれ・CSV・名簿の突き合わせなど、データを整えるレシピ' },
  { name: '集計・分析', slug: 'shukei', color: 'var(--c-shukei)', lead: '条件付き集計・順位・前年比・在庫など、数字をまとめるレシピ' },
  { name: '書類・帳票', slug: 'chohyo', color: 'var(--c-chohyo)', lead: '請求書・見積書・精算書・印刷設定など、書類づくりのレシピ' },
  { name: '経理', slug: 'keiri', color: 'var(--c-keiri)', lead: '売掛金・減価償却・資金繰り・消費税など、経理実務のレシピ' },
] as const;

export type CategoryName = (typeof CATEGORIES)[number]['name'];
export const catOf = (name: string) => CATEGORIES.find((c) => c.name === name) ?? CATEGORIES[0];

export const fmtDate = (d: Date) => {
  const j = new Date(d.getTime() + 9 * 3600 * 1000);
  return `${j.getUTCFullYear()}年${j.getUTCMonth() + 1}月${j.getUTCDate()}日`;
};
