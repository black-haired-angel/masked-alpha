import gradio as gr
import modules.scripts as scripts
import os

from modules import scripts, script_callbacks
from modules import images
from modules.processing import process_images, Processed
from modules.processing import Processed
from PIL import ImageEnhance

from modules.shared import opts, cmd_opts, state


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
            angle = gr.Slider(minimum=0.0, maximum=360.0, step=1, value=0,
            label="Angle")
            hflip = gr.Checkbox(False, label="Horizontal flip")
            vflip = gr.Checkbox(False, label="Vertical flip")
            overwrite = gr.Checkbox(False, label="Overwrite existing files")
        return [
            is_active,
            mask_prompt,
            angle,
            hflip,
            vflip,
            overwrite,
        ]
        
    def testrun(self, p, is_active, mask_prompt):
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


        for i, img in enumerate(p.images):
            img.save(f"{p.outpath_samples}/imageA_{i}.png")
        
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

    def test2run(self, p, is_active, mask_prompt):
    
    # 生成された画像の左半分を白くする
        for img in p.images:
            img = img.convert("RGBA")
            width, height = img.size
            for x in range(width // 2):
                for y in range(height):
                    img.putpixel((x, y), (255, 255, 255, 255))

        return p

    def run(self, p, is_active, mask_prompt, angle, hflip, vflip, overwrite):

        # function which takes an image from the Processed object, 
        # and the angle and two booleans indicating horizontal and
        # vertical flips from the UI, then returns the 
        # image rotated and flipped accordingly
        def rotate_and_flip(im, angle, hflip, vflip):
            from PIL import Image
            
            raf = im
            
            if angle != 0:
                raf = raf.rotate(angle, expand=True)
            if hflip:
                raf = raf.transpose(Image.FLIP_LEFT_RIGHT)
            if vflip:
                raf = raf.transpose(Image.FLIP_TOP_BOTTOM)
            return raf

  

        # If overwrite is false, append the rotation information to the filename
        # using the "basename" parameter and save it in the same directory.
        # If overwrite is true, stop the model from saving its outputs and
        # save the rotated and flipped images instead.
        basename = ""
        if(not overwrite):
            if angle != 0:
                basename += "rotated_" + str(angle)
            if hflip:
                basename += "_hflip"
            if vflip:
                basename += "_vflip"
        else:
            p.do_not_save_samples = True


        proc = process_images(p)

        # rotate and flip each image in the processed images
        # use the save_images method from images.py to save
        # them.
        for i in range(len(proc.images)):

            proc.images[i] = rotate_and_flip(proc.images[i], angle, hflip, vflip)

            images.save_image(proc.images[i], p.outpath_samples, basename,
            proc.seed + i, proc.prompt, opts.samples_format, info= proc.info, p=p)

        return proc

# コールバック関数を定義
def on_ui_settings_callback():
    # 必要な設定をここに追加
    pass

script_callbacks.on_ui_settings(on_ui_settings_callback)

# スクリプトを登録
# def on_ui_tabs():
    #script = MaskedAlphaScript()
    #return [(script.ui(is_img2img=False), "Masked Alpha", "masked_alpha")]
