import gradio as gr
from PIL import Image, ImageDraw, ImageFont
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
    detections = [(1, 1, 200, 200)]  # (x1, y1, x2, y2)

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

with gr.Blocks() as demo:
    prompt = gr.Textbox(label="プロンプト")
    mask_prompt = gr.Textbox(label="マスクプロンプト")
    output_image = gr.Image(label="生成画像")

    generate_button = gr.Button("画像生成")
    generate_button.click(process_image, inputs=[prompt, mask_prompt], outputs=output_image)

demo.launch()
