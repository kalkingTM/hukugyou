import { defineConfig } from 'astro/config';

// GitHub Pages（プロジェクトサイト）: https://kalkingtm.github.io/hukugyou/
export default defineConfig({
  site: 'https://kalkingtm.github.io',
  base: '/hukugyou',
  trailingSlash: 'always',
  // Excelの数式ブロックが中心なので構文ハイライトは使わない（配色はCSSで統一）
  markdown: { syntaxHighlight: false, rehypePlugins: [rehypeTableScroll] },
});

// 表を横スクロール用の枠で包む（スマホで表が画面からはみ出さないように）
function rehypeTableScroll() {
  return (tree) => {
    const walk = (node) => {
      if (!node.children) return;
      node.children = node.children.map((c) => {
        if (c.type === 'element' && c.tagName === 'table') {
          return { type: 'element', tagName: 'div', properties: { className: ['table-scroll'] }, children: [c] };
        }
        walk(c);
        return c;
      });
    };
    walk(tree);
  };
}
