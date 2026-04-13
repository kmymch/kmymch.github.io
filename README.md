# ブログメンテナンス作業手順

このファイルには、Jekyllブログ記事を更新・メンテナンスするための標準的な作業手順が記載されています。記事の追加、ローカルサーバでのチェック、git更新に関する手順を確認できます。

元のテーマドキュメントは [README-original.md](README-original.md) を参照してください。

## 目次
- [初期セットアップ](#初期セットアップ)
- [新しい記事を追加する](#新しい記事を追加する)
- [ローカルサーバでチェックする](#ローカルサーバでチェックする)
- [記事の編集](#記事の編集)
- [Gitで更新を保存する](#gitで更新を保存する)
- [よくある質問](#よくある質問)

## 初期セットアップ

### 1. 環境構築（初回のみ）
```bash
# Rubyと必要なGemsをインストール
bundle install
```

### 2. 依存パッケージの確認
```bash
bundle list
```

## 新しい記事を追加する

### 1. 記事ファイルを作成する

記事は `_posts/` ディレクトリまたは `_news/` ディレクトリに配置します。

**命名規則（重要）:**
```
YYYY-MM-DD-記事のタイトル.md
```

**例:**
```
_posts/2026-02-28-my-new-article.md
```

### 2. ファイルのテンプレート

```markdown
---
layout: post
title: "記事のタイトル"
date: 2026-02-28
categories: [カテゴリ1, カテゴリ2]
---

ここに記事の内容を書きます。Markdownフォーマットをサポートしています。
```

**Front Matterの主要な設定:**
| 項目 | 説明 | 必須 |
|------|------|------|
| `layout` | `post` または `page` | ✓ |
| `title` | 記事のタイトル | ✓ |
| `date` | 公開日（YYYY-MM-DD形式） | ✓ |
| `categories` | 記事のカテゴリ（複数指定可） | - |
| `feature_image` | トップに表示する画像 | - |
| `feature_text` | 上部に表示するテキスト | - |
| `aside` | サイドバーの表示（true/false） | - |

### 3. ニュース記事を追加する場合

ニュース記事は `_news/` ディレクトリに配置します：
```
_news/2026-02-28-aist-research-project.md
```

## ローカルサーバでチェックする

### 1. Jekyllサーバの起動

```bash
bundle exec jekyll serve
```

出力例:
```
Configuration file: /path/to/_config.yml
            Source: /path/to
       Destination: /path/to/_site
 Incremental build: enabled
      Generating...
                    done in 2.345 seconds.
 Auto-regeneration: enabled for '/path/to'
    Server address: http://127.0.0.1:4000/
  Server running...
  Press ctrl-c to stop the server
```

### 2. ブラウザで確認

`http://localhost:4000` にアクセスして、サイトの表示を確認します。

**確認項目:**
- [ ] 新しい記事が表示されている
- [ ] リンク（内部リンク、外部リンク）が正しく機能している
- [ ] 画像が正しく表示されている
- [ ] 日本語テキストが正しく表示されている
- [ ] モバイル表示で問題がないか（レスポンシブデザイン）

### 3. サーバの停止

```bash
Ctrl+C
```

## 記事の編集

### 1. 既存記事の更新

該当の `.md` ファイルを編集し、保存します。

```bash
# 編集ファイルの例
_posts/2026-02-28-my-new-article.md
```

### 2. ローカルで即座に確認

Jekyllサーバが起動している場合、自動的にサイトが再生成されます。ブラウザをリロードして確認してください。

### 3. 画像の追加

画像は `assets/images/` ディレクトリに配置し、記事内で以下のように参照します：

```markdown
![代替テキスト](/assets/images/image-name.jpg)

または include を使ってキャプション付きで表示:
{% include figure.html image="/assets/images/image-name.jpg" caption="画像の説明" %}
```

## Gitで更新を保存する

### 1. 変更の確認

```bash
git status
```

出力例:
```
Changes not staged for commit:
  modified:   _posts/2026-02-28-my-new-article.md
  
Untracked files:
  _news/2026-02-28-new-news.md
```

### 2. 変更をステージング

```bash
# 全ての変更をステージング
git add .

# または特定のファイルのみ
git add _posts/2026-02-28-my-new-article.md
```

### 3. コミットメッセージを作成

```bash
git commit -m "新記事を追加: 記事のタイトル"
```

**コミットメッセージの例:**
- `新記事を追加: 2026年AI論文紹介`
- `記事を更新: ロボティクス研究の最新動向`
- `ニュース記事を追加: 学会発表予定`

### 4. リモートリポジトリにプッシュ

```bash
git push origin main
```

または、使用しているブランチ名に変更してください。

### 5. 完全な流れ（例）

```bash
# 1. サーバでチェック完了後
git status

# 2. 変更をステージング
git add .

# 3. コミット
git commit -m "新記事を追加: 2026年最新の研究トピック"

# 4. プッシュ
git push origin main
```

## よくある質問

### Q1: 記事がサーバに表示されない

**A:** 以下を確認してください：
- ファイルが `_posts/` または `_news/` ディレクトリにあるか
- ファイル名の形式が `YYYY-MM-DD-title.md` であるか
- Front Matter の `layout` フィールドが `post` または `page` に設定されているか
- 日付が現在の日付以前であるか（未来の日付は非表示）

### Q2: 画像が表示されない

**A:** 以下を確認してください：
- 画像が `assets/images/` ディレクトリにアップロードされているか
- 記事内の画像パスが正しいか（例: `/assets/images/image.jpg`）
- 画像ファイルの形式が対応している（jpg, png, gif など）

### Q3: Gitでエラーが出た場合

**A:** 一般的なエラー対処：
```bash
# リモート情報を更新
git fetch origin

# ローカルとリモートの差分を確認
git diff origin/main

# ローカルの変更をリセット（注意：変更が失われます）
git reset --hard origin/main
```

### Q4: サーバが起動しない

**A:** 以下を試してください：
```bash
# Gemの再インストール
bundle install

# キャッシュをクリア
rm -rf .jekyll-cache/
bundle exec jekyll serve
```

### Q5: Jekyllのバージョンを確認したい

**A:**
```bash
bundle exec jekyll --version
```

## トラブルシューティング

### ポート4000が既に使用されている場合

別のポートを指定してサーバを起動します：
```bash
bundle exec jekyll serve --port 5000
```

その後、`http://localhost:5000` にアクセスします。

### 記事の公開日付をスケジュールしたい

Front Matterの `date` フィールドを未来の日付に設定します。その日付まで記事は非表示になります。

```yaml
---
layout: post
title: "将来の記事"
date: 2026-03-15  # この日付になると公開される
---
```

### カテゴリを追加したい

1. 記事のFront Matterに `categories` を追加
2. `categories.md` ファイルでカテゴリのインデックスページを確認

```yaml
categories: [AI, 機械学習, 深層学習]
```

