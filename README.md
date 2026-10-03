# sample_game

Pyxel で作るゲームの練習用プロジェクトです。

## セットアップ

Python 3.12 以上と [uv](https://docs.astral.sh/uv/) を使用します。

```bash
uv sync
```

## 起動

```bash
uv run python3 main.py
```

`Q` キーで終了できます。

## GitHub Pages で公開

1. GitHub にこのフォルダーをリポジトリとして push します。
2. リポジトリの **Settings > Pages** を開きます。
3. **Deploy from a branch** を選び、ブランチとフォルダーに `main` と `/ (root)` を指定して保存します。
4. 表示された URL を開きます。

`index.html` がブラウザー版の Pyxel を読み込み、`main.py` と `my_resource.pyxres` を使ってゲームを実行します。
