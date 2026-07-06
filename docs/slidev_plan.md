# 確率論勉強会 Slidev 方針

## 結論

最終資料は Slidev で作成する。PDF出力を前提に、アニメーションやクリック依存の説明は避け、1枚ごとに読めるスライドとして構成する。

LaTeX は補助ノート向きとする。定理の証明や細かな測度論的補足は、必要に応じて別途 `.tex` に退避する。

## 想定聴衆

- 理学部出身の4名
- 物理・生物など背景はさまざま
- 前段で測度論・Lebesgue積分の概論講義を受けている
- 確率論の厳密な定式化と応用先の両方を見たい

## 資料設計

40-60分で全テーマを深く証明するのは難しいため、今回は「測度論から確率論への地図」を主目的にする。

厚く扱う箇所:

- 確率空間、確率変数、分布
- 収束概念の違い
- 大数の法則と中心極限定理の位置づけ
- 確率過程、ブラウン運動、Markov性

応用として紹介する箇所:

- 確率微分方程式
- ブラックショールズ方程式
- 最適戦略、秘書問題

## スライド内容の編集方針

厳密性は「測度論の言葉で何を定義しているかが追える」水準を保ちつつ、証明の完備性よりも概念間の対応関係を優先する。各トピックでは、できるだけ「測度論での定式化」「直感」「確率論で何に効くか」を1セットで示す。

1スライド1論点を基本にし、1枚の中で定義・定理・例を重ねすぎない。新しい定義を出した直後は、抽象記号だけで進めず、サイコロ・分布・標本路などの小さな例を置いて読み替えを助ける。

用語と記号は一貫させる。確率空間は `(\Omega, \mathcal{F}, P)`、確率変数は可測写像、分布は push-forward measure `P_X` として説明する。収束は「概収束」「確率収束」「分布収束」「L^p 収束」を混ぜず、関係図と代表例で比較する。

大数の法則・中心極限定理・確率過程・ブラウン運動・Markov性は本編の柱として扱う。確率微分方程式、ブラックショールズ、秘書問題は応用先の見取り図として紹介し、導出や証明を厚くする場合は補助ノートに分ける。

PDF出力でも読める資料にするため、クリックで初めて意味が出る構成は避ける。図式や補足枠は `::diagram`、`::flow`、`::note` など既存のカスタム構文を使い、スライド本文に個別スタイルを増やしすぎない。

## 推奨構成

1. 測度論から確率論へ
2. 収束概念
3. 大数の法則と中心極限定理
4. 確率過程
5. 応用
6. まとめ

## PDF出力前提の注意

- `transition: none` とし、PDFで意味が欠けないようにする
- 1スライド1論点を基本にする
- 数式は KaTeX で表現する
- 証明を詰め込みすぎず、証明が必要な箇所は補助ノートに回す
- シミュレータは本体には埋め込まず、別途URLやスクリーンショットで扱う

## Markdown とスタイルの方針

- スライド本文では生の `<div>` や `<style>` をできるだけ使わない
- 2カラムは Slidev 標準の `two-cols-header` と `::left::` / `::right::` を使う
- 補足枠や図式は `::note`、`::diagram`、`::flow` のようなカスタム構文にする
- 共通スタイルは `style.css` と `components/` に分離する
- Slidev は UnoCSS を内蔵しているため、コンポーネント内では Tailwind 互換の utility class を使う

## Vite との相性

Slidev が内部で Vite/Rolldown を管理しているため、このリポジトリ側で Vite を直接追加しない。現状は `pnpm build` と `pnpm export` が通っている。

build 時に `node_modules/@vueuse/core` の pure annotation に関する Rolldown 警告が出ることがあるが、依存ライブラリ側の非致命的な警告で、PDF出力には影響していない。

## GitHub Pages 公開時のルーティング

GitHub Pages では `https://lambda-b.github.io/self_seminar/` 配下に公開する。Slidev の asset 参照は `pnpm build` で `--base ./` を指定し、Pages のサブディレクトリ配信でも CSS/JS が読めるようにする。

Slidev の `routerMode` は `hash` とする。history mode は URL が見やすい一方、presenter などの deep link で `./assets/...` が深いパス相対になり、GitHub Pages 上で asset 解決が壊れやすい。hash mode なら entry point は常に `/self_seminar/` のままになる。

ただし、Slidev v52 系では Pages の base path と hash routing の組み合わせで、矢印キー遷移時に `#/presenter/presenter/7` のような重複 hash が発生することがある。`setup/routes.ts` で presenter の重複 route だけを `#/presenter/7` へ redirect している。その他の route は Slidev 標準の挙動に任せる。GitHub Pages まわりを触る場合は、通常表示と presenter 表示の両方で矢印キー遷移を確認する。

確認観点:

- `https://lambda-b.github.io/self_seminar/#/1` から右矢印で `#/2` に進む
- `https://lambda-b.github.io/self_seminar/#/presenter/7` で `#/presenter/presenter/7` に増殖しない
- build artifact の `dist/index.html` は asset を `./assets/...` として参照する

## 今後の拡張候補

- 秘書問題シミュレータを React で作る
- ブラウン運動の標本路画像を追加する
- ブラックショールズの導出を補助ノートにする
- 複数回勉強会に分ける場合は、収束・確率過程・応用の3回構成にする
