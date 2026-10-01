# CLAUDE.md

田中雄輝（慶應義塾大学 博士課程）の個人サイト https://kmymch.github.io のソース。
Jekyll + Alembic テーマ（コピーして直接改変済み。gem テーマではない）。

## 公開の仕組み（重要）

- `main` に push すると GitHub Pages（ブランチ公開方式）が自動ビルドして**即公開**される。push 前に必ずユーザーに確認する。
- 本番ビルドは GitHub Pages 標準の **Jekyll 3.10**、ローカルは Jekyll 4。本番では Gemfile は使われず、GitHub Pages の許可リストにあるプラグインしか動かない。プラグインを追加したり Jekyll 4 専用の機能を使ったりしない。
- `_site/` と `Gemfile.lock` は生成物（git 管理外）。

## 確認コマンド

```sh
bundle exec jekyll build      # ビルド確認。Sass の deprecation warning が大量に出るのは既知で無害
bundle exec jekyll serve      # http://localhost:4000 でプレビュー
```

変更後は最低限 `jekyll build` が通ることを確かめる。

## ディレクトリ

| パス | 内容 |
|---|---|
| `index.md` | トップ（自己紹介・学歴） |
| `publications.md` | 業績ページ。中身は `_bibliography/publications.bib` から生成。**直接書かない** |
| `_bibliography/publications.bib` | 業績の正本 |
| `_data/publications.json` | bib から生成（`tools/bib2json.py`）。**手で編集しない** |
| `_news/` | ニュース（学会発表・インターン等）。主な更新先 |
| `_posts/` | ブログ（ほぼ未使用） |
| `assets/images/news/` | ニュース用画像 |
| `assets/cv/cv_yuki_tanaka.pdf` | CV（ナビの CV リンク先。ファイル名を変えたら `_config.yml` も直す） |
| `tools/` | 補助スクリプト（`uv run` で実行。ビルド対象外） |
| `.githooks/pre-commit` | 画像の縮小と bib の変換を自動実行 |

## ニュースを追加する

1. ファイル名は `_news/YYYY-MM-DD-slug.md`（月日は 0 埋め、slug は半角英数とハイフン）。ファイル名がそのまま URL（`/news/YYYY-MM-DD-slug/`）になる。
2. 既存記事のファイル名を変えると URL が変わるので、変える場合は front matter に `redirect_from:` で旧 URL を残す。
3. front matter の書式（既存記事に揃える）:

   ```yaml
   ---
   title: 記事タイトル
   categories:
   - Research
   feature_image: "https://picsum.photos/2560/600?image=10xx"   # 既存記事と被らない番号
   excerpt: "一覧に出る短い一文"
   ---
   ```

4. 本文は日本語の一文 + 英語の段落、という既存記事の調子に合わせる。最後は `---` で締める。
5. 画像は `assets/images/news/YYYY-MM-DD.jpg` に置き、`![説明](/assets/images/news/YYYY-MM-DD.jpg)` で参照する。写真は PNG ではなく JPG にする。

## 業績を追加・修正する

1. `_bibliography/publications.bib` を編集する。冒頭コメントにある独自フィールドを使う。
   - `category` = `journal` / `international` / `domestic`（必須）
   - `award`, `award_url` … 表彰。論文の下と Awards セクションに出る
   - `url`, `url_label` … DOI 以外のリンク
2. `uv run tools/bib2json.py` で `_data/publications.json` を再生成する（pre-commit フックでも自動実行される）。
3. 著者は英語なら `Tanaka, Yuki and Katsura, Seiichiro`、日本語なら `田中 雄輝 and 桂 誠一郎`。
4. 年、ページ、DOI、共著者などの書誌情報は推測で埋めない。分からなければユーザーに聞くか、DOI や CrossRef で確認できたものだけ入れる。
5. 論文に紐づかない表彰（奨学金など）は今は扱っていない。必要になったら `_data/awards.yml` を作ることを提案する。

## 画像

- pre-commit フック（`core.hooksPath=.githooks`）が、コミットされる `assets/` 以下の jpg/png を長辺 1600px に縮小し、EXIF（GPS 位置情報を含む）を削除する。
- 新しく clone した環境ではフックの有効化が必要: `git config core.hooksPath .githooks`
- 手動で実行する場合: `uv run tools/optimize_images.py FILE...` または `--all`

## その他

- `_config.yml` の "Great Scott!" や "I have good news and bad news" は本人が意図して書いた遊びなので、テーマの残骸として消さない。

## コミット

- メッセージは日本語で、内容が分かる具体的なものにする（例: `ニュース追加: ALIFE2025`、`業績追加: IECON2025`）。
- push は確認してから。
