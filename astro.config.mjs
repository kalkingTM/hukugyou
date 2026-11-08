import { defineConfig } from 'astro/config';

// GitHub Pages（プロジェクトサイト）: https://kalkingtm.github.io/hukugyou/
export default defineConfig({
  site: 'https://kalkingtm.github.io',
  base: '/hukugyou',
  trailingSlash: 'always',
  // Excelの数式ブロックが中心なので構文ハイライトは使わない（配色はCSSで統一）
  markdown: { syntaxHighlight: false },
});
