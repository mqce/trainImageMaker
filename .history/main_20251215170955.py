import os
from PIL import Image
from rembg import remove
import numpy as np

# ========== 設定エリア ==========
INPUT_FOLDER = "input_images"      # 元画像のフォルダ
OUTPUT_FOLDER = "processed_images" # 保存先フォルダ
TARGET_SIZE = (768, 768)           # 目標解像度 (512, 512) または (768, 768)
ENABLE_REMOVE_BG = True            # 背景除去を行うか (True/False)
BG_COLOR = (255, 255, 255, 255)    # 背景色 (R, G, B, A) 
# ※LoRA学習用なら、透過PNGのままより白背景(255,255,255,255)で保存するか、
#  あるいは透過部分をキャプションでmask処理するのが一般的ですが、
#  ここでは汎用的に「白背景」にする例として記述しています。
# ==============================

def process_images():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    print(f"{len(files)} 枚の画像を処理します...")

    for i, file_name in enumerate(files):
        input_path = os.path.join(INPUT_FOLDER, file_name)
        
        try:
            # 1. 画像を開く
            img = Image.open(input_path).convert("RGBA")

            # 2. 背景除去 (rembg使用)
            if ENABLE_REMOVE_BG:
                img = remove(img) 
                # rembgの結果は透過PNGになります

            # 3. 正方形へのパディング (アスペクト比維持)
            # 現在のサイズを取得
            old_size = img.size  # (width, height)
            
            # 新しいサイズ（正方形）を一辺の最大長で作成
            new_size = max(old_size)
            
            # 背景色で新しいキャンバスを作成
            # 背景除去後の透過画像を白背景に合成したい場合はここで制御
            new_img = Image.new("RGBA", (new_size, new_size), BG_COLOR)
            
            # 中央に貼り付け
            paste_position = ((new_size - old_size[0]) // 2,
                              (new_size - old_size[1]) // 2)
            
            # 透過情報を考慮して貼り付け
            new_img.paste(img, paste_position, mask=img if ENABLE_REMOVE_BG else None)

            # 4. 指定解像度へリサイズ (Lanczosフィルタで綺麗に)
            final_img = new_img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)

            # 5. 保存 (PNG形式推奨)
            # 白背景にしたのであればJPGでも良いが、高品質維持のためPNG推奨
            save_name = os.path.splitext(file_name)[0] + ".png"
            final_img.save(os.path.join(OUTPUT_FOLDER, save_name))
            
            print(f"[{i+1}/{len(files)}] 完了: {file_name}")

        except Exception as e:
            print(f"エラー発生 ({file_name}): {e}")

    print("すべての処理が完了しました。")

if __name__ == "__main__":
    process_images()