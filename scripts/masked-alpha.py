import gradio as gr
from modules import scripts, script_callbacks
from modules import images
from modules.processing import process_images, Processed
from modules.processing import Processed

class Script(scripts.Script): 
    def title(self):
        return "Masked Alpha"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion("Masked Alpha", open=False):
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
        
    def run(self, p, is_active, mask_prompt):
        if not is_active:
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

        #proc = process_images(p)

        # rotate and flip each image in the processed images
        # use the save_images method from images.py to save
        # them.
        #for i in range(len(proc.images)):

            #proc.images[i] = rotate_and_flip(proc.images[i], angle, hflip, vflip)

            #images.save_image(proc.images[i], p.outpath_samples, basename,
            #proc.seed + i, proc.prompt, opts.samples_format, info= proc.info, p=p)
        #return proc
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
