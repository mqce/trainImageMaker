# trainImageMaker

画像フォルダを一括処理し、背景除去 → 正方形キャンバス化 → 指定解像度(デフォルト768x768)にリサイズしてPNGで保存するPythonスクリプトです。LoRA学習などの前処理を想定しています。

## 必要環境
- Python 3.9+（Pillowが動作するバージョン）
- pipで以下をインストール
  - `pip install pillow rembg numpy`
  - rembgは初回実行時にモデルを自動ダウンロードします。

## 使い方
1. プロジェクト直下に`input_images`フォルダを作り、`.png/.jpg/.jpeg/.webp`画像を入れる。
2. 必要に応じて`main.py`冒頭の設定を変更する（下記参照）。
3. スクリプトを実行:
   - `python main.py`
4. 処理後の画像は`processed_images`フォルダにPNGで出力されます。

## 設定（`main.py`先頭）
- `INPUT_FOLDER`: 入力フォルダ名（デフォルト`input_images`）
- `OUTPUT_FOLDER`: 出力フォルダ名（デフォルト`processed_images`）
- `TARGET_SIZE`: 出力解像度 `(768, 768)` や `(512, 512)` など
- `ENABLE_REMOVE_BG`: rembgで背景除去するか
- `BG_COLOR`: 正方形キャンバスの背景色 `(R, G, B, A)`。背景を白で埋めたい場合は `(255, 255, 255, 255)`。

## 処理の流れ
1. 入力フォルダ内の画像を順に読み込み、RGBA化
2. `ENABLE_REMOVE_BG`が有効ならrembgで背景除去（透過PNG化）
3. 元画像の縦横どちらか長い辺に合わせた正方形キャンバスを`BG_COLOR`で作成し、中央に貼り付け
4. Lanczosで`TARGET_SIZE`へリサイズ
5. 拡張子を`.png`にして出力フォルダへ保存

## よくある質問
- 入力フォルダが存在しないとエラーになるので、必ず事前に作成してください。
- rembgのモデルダウンロードに時間がかかる場合があります。初回だけお待ちください。
- 背景を残したい場合は`ENABLE_REMOVE_BG = False`にし、`BG_COLOR`は無視されます（貼り付け時に透過合成しないため）。


