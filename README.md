# 測度論・ルベーグ積分勉強会資料

`lambda-b/self_seminar` の Slidev 構成を踏襲して作る, 測度論・ルベーグ積分勉強会用の資料です.

メイン資料は `slides.md` にまとめます.PDF 出力を前提に, 1 ページごとに読める構成を基本にします.

## 前提条件

- Node.js
- pnpm

Dev Container を使う場合は, このディレクトリを VS Code で開いて `Dev Containers: Reopen in Container` を実行してください.

## セットアップ

```bash
pnpm install
```

## プレビュー

```bash
pnpm dev
```

## PDF 出力

```bash
pnpm export
```

出力先:

```text
dist/measure-theory-seminar.pdf
```

## GitHub Pages

`main` に push されると GitHub Actions で Slidev をビルドし, GitHub Pages に公開する想定です.

公開ページ:

https://teruyuki-yamasaki.github.io/self_seminar_measure/

初回の Pages 設定手順は `docs/github_pages.md` を参照してください.

## Format / Check

```bash
pnpm format
pnpm check
```

## 章別原稿

`docs/chapters/` には, スライド化の前段階として各章の本文原稿を置いています.

### [第0章 導入：測度論は何を拡張するのか](./docs/chapters/00_introduction.md)
### [第1章 古典的面積概念と Jordan 測度](./docs/chapters/01_classical_area_jordan_measure.md)
### [第2章 可算操作への移行：Lebesgue 外測度](./docs/chapters/02_lebesgue_outer_measure.md)
### [第3章 Carathéodory 可測性と Lebesgue 測度](./docs/chapters/03_caratheodory_lebesgue_measure.md)
### [第4章 抽象的測度空間](./docs/chapters/04_measure_space.md)
### [第5章 Riemann 積分から Lebesgue 積分へ](./docs/chapters/05_riemann_to_lebesgue.md)
### [第6章 可測函数と単函数](./docs/chapters/06_measurable_simple_functions.md)
### [第7章 Lebesgue 積分](./docs/chapters/07_lebesgue_integral.md)
### [第8章 極限と積分の交換](./docs/chapters/08_limits_and_integrals.md)
### [Appendix Radon-Nikodym の定理](./docs/chapters/appendix_radon_nikodym.md)

## 構成メモ

- `slides.md`: 本文
- `components/`: MDC / Comark から呼ぶ小コンポーネント
- `setup/main.ts`: GitHub Pages 配信用の hash 補正
- `style.css`: 全体スタイル
- `docs/`: 方針メモ
