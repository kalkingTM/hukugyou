export const SITE = {
  name: 'しごとExcelレシピ',
  tagline: '仕事で使うExcelの数式と手順',
  description:
    '会社で使うExcelの困りごとを、1記事1問題で解説します。各記事に数式入りの見本ファイルが付き、掲載前に数式を計算し直して確認しています。',
};

// Search Console / Bing Webmaster の所有確認トークン（取得したらここに貼る）
export const VERIFY = { google: 'O3u0-Jq7lQOlQ3Week93jbpwS8OP0YdYJByAiMrglyM', bing: '' };

// アクセス解析（Cloudflare Web Analytics）。トークンは公開されるページに埋め込まれる識別子で、秘密情報ではない。
export const ANALYTICS = {
  cloudflareToken: '40e4f857e11741978bfb96bba009641c',
  dashboardUrl: 'https://dash.cloudflare.com/?to=/:account/web-analytics',
  searchConsoleUrl: 'https://search.google.com/search-console?resource_id=https%3A%2F%2Fkalkingtm.github.io%2Fhukugyou%2F',
  bingUrl: 'https://www.bing.com/webmasters/home',
};

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

// ===== 運営者情報 =====
// 実務に就いた年月（平成16年4月 = 2004年4月）。経験年数はビルド時に自動計算する。
export const OPERATOR = {
  role: '税理士',
  careerStart: { year: 2004, month: 4, label: '平成16年4月' },
};

/** 実務経験の満年数（日本時間）。毎年4月に1つ増える。サイトを作り直すたび（毎日の自動実行を含む）に更新される。 */
export const experienceYears = (now: Date = new Date()): number => {
  const j = jst(now);
  const years = j.getUTCFullYear() - OPERATOR.careerStart.year;
  return j.getUTCMonth() + 1 >= OPERATOR.careerStart.month ? years : years - 1;
};
