import gradio as gr
from PIL import Image, ImageDraw, ImageFont
from modules import scripts, script_callbacks
import numpy as np
import cv2

def generate_image(prompt):
    # ここでStable Diffusionを使って画像を生成するコードを追加
    # 例: generated_image = stable_diffusion_generate(prompt)
    generated_image = Image.new('RGBA', (512, 512), (255, 255, 255, 255))  # 仮の生成画像
    return generated_image

def detect_and_transparent_apple(image, mask_prompt):
    # OpenCVを使って画像を読み込み
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)

    # ここでYOLOやMask R-CNNを使ってりんごを検出するコードを追加
    # 例: detections = detect_apples(image_bgr)

    # 仮の検出結果（りんごの位置を矩形で指定）
    detections = [(100, 100, 200, 200)]  # (x1, y1, x2, y2)

    # アルファチャンネルを編集してりんごの部分を透過
    for (x1, y1, x2, y2) in detections:
        image_np[y1:y2, x1:x2, 3] = 0  # アルファチャンネルを0に設定

    return Image.fromarray(image_np)

def process_image(prompt, mask_prompt):
    generated_image = generate_image(prompt)
    if mask_prompt.lower() == "apple":
        result_image = detect_and_transparent_apple(generated_image, mask_prompt)
    else:
        result_image = generated_image
    return result_image


class MaskedAlphaScript(scripts.Script):
    def title(self):
        return "Masked Alpha"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion("Masked Alpha Extension", open=False):
            is_active = gr.Checkbox(
                label="Active",
                value=False,
            )
            mask_prompt = gr.Textbox(
                label="mask prompt"
            )
        return [
            is_active,
            mask_prompt,
        ]

    

    def run(self, p, mask_prompt):
        if not mask_prompt:
            return p

        try:
            alpha_value = float(mask_prompt)
            if alpha_value < 0.0 or alpha_value > 1.0:
                raise ValueError("透明度は0.0から1.0の間で指定してください。")
        except ValueError as e:
            print(f"エラー: {e}")
            return p

        # 生成された画像の透明度を変更
        for img in p.images:
            img = img.convert("RGBA")
            alpha = img.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(alpha_value)
            img.putalpha(alpha)

        return p

# コールバック関数を定義
def on_ui_settings_callback():
    # 必要な設定をここに追加
    pass



script_callbacks.on_ui_settings(on_ui_settings_callback)

# スクリプトを登録
# def on_ui_tabs():
    #script = MaskedAlphaScript()
    #return [(script.ui(is_img2img=False), "Masked Alpha", "masked_alpha")]
