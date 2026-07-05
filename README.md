# 確率論勉強会資料

測度論・Lebesgue積分の概論講義の後に実施する、確率論勉強会用の Slidev 資料です。

メイン資料は `slides.md` にまとめています。PDF出力を前提に、アニメーション依存を避けて1ページごとに読める構成にしています。

## 前提条件

- Node.js
- npm

Dev Container を使う場合は、このリポジトリを VS Code で開いて `Dev Containers: Reopen in Container` を実行してください。

## セットアップ

```bash
npm install
```

## プレビュー

```bash
npm run dev
```

既定では Slidev のローカルサーバーが起動します。

## PDF出力

```bash
npm run export
```

出力先:

```text
dist/probability-seminar.pdf
```

## 方針メモ

Slidev / LaTeX の使い分けや、40-60分想定の構成方針は `docs/slidev_plan.md` にまとめています。

## Format / Check

Biome を使います。

```bash
npm run format
npm run check
```

Vue ファイルの formatter も Biome に寄せています。構文ハイライトと言語機能は Volar が担当するため、色が付かない場合は Dev Container を rebuild するか、VS Code の拡張機能を reload してください。

## スライド記法

本文はできるだけ Markdown と Slidev の slot 記法で書きます。共通の見た目が必要な箇所は、MDC/Comark のブロックコンポーネントを使います。

```md
::note
ここに補足を書く。inline 数式 $X_n \to X$ も Markdown として処理されます。
::

::diagram
$(\Omega,\mathcal{F},P)$
$\xrightarrow{\quad X\quad}$
$(S,\mathcal{S},P_X)$
::
```

スタイルは `style.css` と `components/` 配下に寄せています。Slidev は UnoCSS を内蔵しているため、コンポーネント内では Tailwind 互換の utility class を使えます。
