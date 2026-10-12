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

## 操作方法

- キーボード: 左右矢印キーまたは `A` / `D` で移動、`Space` で発射・決定
- バーチャルパッド / ゲームパッド: 方向パッドで移動、`A` / `B` ボタンで発射・決定

## GitHub Pages で公開

1. GitHub にこのフォルダーをリポジトリとして push します。
2. リポジトリの **Settings > Pages** を開きます。
3. **Deploy from a branch** を選び、ブランチとフォルダーに `main` と `/ (root)` を指定して保存します。
4. 表示された URL を開きます。

`index.html` がブラウザー版の Pyxel を読み込み、`main.py` と `my_resource.pyxres` を使ってゲームを実行します。
