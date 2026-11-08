export const SITE = {
  name: 'しごとExcelレシピ',
  tagline: 'コピペで使える、検証済みの仕事用Excelレシピ集',
  base: import.meta.env.BASE_URL,
};
export const url = (p: string) => `${import.meta.env.BASE_URL}${p.replace(/^\//, '')}`;
