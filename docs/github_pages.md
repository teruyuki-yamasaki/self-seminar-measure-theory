# GitHub Pages 公開手順

このリポジトリでは `main` に push されたタイミングで GitHub Actions が Slidev と章別 HTML をビルドし、`dist/` を GitHub Pages にデプロイします。

公開 URL は通常、次の形式になります。

```text
https://teruyuki-yamasaki.github.io/self-seminar-measure-theory/
```

章別 HTML は次の URL で公開されます。

```text
https://teruyuki-yamasaki.github.io/self-seminar-measure-theory/chapters/
```

## 初回の Pages 設定

GitHub Pages の公開元を GitHub Actions に設定します。これは初回だけ実行すればよい設定です。

```bash
gh api \
  --method POST \
  repos/teruyuki-yamasaki/self-seminar-measure-theory/pages \
  -f build_type=workflow
```

すでに Pages が有効化済みで、公開元だけを GitHub Actions に揃える場合は次を実行します。

```bash
gh api \
  --method PUT \
  repos/teruyuki-yamasaki/self-seminar-measure-theory/pages \
  -f build_type=workflow
```

設定確認:

```bash
gh api repos/teruyuki-yamasaki/self-seminar-measure-theory/pages
```

## 補足

`setup/main.ts` は Pages 配下の hash ルーティング補正用です。リポジトリ名を変えるなら、その正規表現も合わせて更新してください。
