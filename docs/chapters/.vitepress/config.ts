import { defineConfig } from "vitepress";

const base = process.env.VITEPRESS_BASE ?? "/self-seminar-measure-theory/chapters/";

const chapters = [
  {
    text: "第0章 導入：Riemann 積分から Lebesgue 積分へ",
    link: "/00_introduction",
  },
  {
    text: "第1章 古典的面積概念と Jordan 測度",
    link: "/01_classical_area_jordan_measure",
  },
  {
    text: "第2章 可算操作への移行：Lebesgue 外測度",
    link: "/02_lebesgue_outer_measure",
  },
  {
    text: "第3章 Carathéodory 可測性と Lebesgue 測度",
    link: "/03_caratheodory_lebesgue_measure",
  },
  {
    text: "第4章 抽象的測度空間",
    link: "/04_measure_space",
  },
  {
    text: "第5章 Lebesgue 積分の見通し",
    link: "/05_lebesgue_integral_outlook",
  },
  {
    text: "第6章 可測函数と単函数",
    link: "/06_measurable_simple_functions",
  },
  {
    text: "第7章 Lebesgue 積分",
    link: "/07_lebesgue_integral",
  },
  {
    text: "第8章 極限と積分の交換",
    link: "/08_limits_and_integrals",
  },
  {
    text: "Appendix Radon-Nikodym の定理",
    link: "/appendix_radon_nikodym",
  },
];

export default defineConfig({
  title: "測度論・ルベーグ積分勉強会",
  description: "測度論・ルベーグ積分勉強会の章別原稿",
  lang: "ja-JP",
  base,
  outDir: "../../dist/chapters",
  cleanUrls: false,
  markdown: {
    math: true,
    image: {
      lazyLoading: true,
    },
  },
  themeConfig: {
    nav: [
      { text: "章別原稿", link: "/" },
      {
        text: "スライド",
        link: "https://teruyuki-yamasaki.github.io/self-seminar-measure-theory/",
      },
      {
        text: "GitHub",
        link: "https://github.com/teruyuki-yamasaki/self-seminar-measure-theory",
      },
    ],
    sidebar: [
      {
        text: "章別原稿",
        items: [{ text: "目次", link: "/" }, ...chapters],
      },
    ],
    outline: {
      label: "このページ",
      level: [2, 3],
    },
    docFooter: {
      prev: "前へ",
      next: "次へ",
    },
    search: {
      provider: "local",
    },
  },
});
