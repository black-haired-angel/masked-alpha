import modules.scripts as scripts
import gradio as gr
import os
import numpy as np

from modules import images, script_callbacks
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state
from PIL import Image

class Script(scripts.Script):  

# The title of the script. This is what will be displayed in the dropdown menu.
    def title(self):
        print("title関数が実行されました")
        return "Extension Template"
    
    # Decide to show menu in txt2img or img2img
    # - in "txt2img" -> is_img2img is `False`
    # - in "img2img" -> is_img2img is `True`
    #
    # below code always show extension menu
    def show(self, is_img2img):
        print("show関数が実行されました")
        return scripts.AlwaysVisible
    
    # Setup menu ui detail
    def ui(self, is_img2img):
            with gr.Accordion('Extension Template', open=False):
                    with gr.Row():
                            angle = gr.Slider(
                                    minimum=0.0,
                                    maximum=360.0,
                                    step=1,
                                    value=0,
                                    label="Angle"
                            )
                            checkbox = gr.Checkbox(
                                    False,
                                    label="Checkbox"
                            )
            # TODO: add more UI components (cf. https://gradio.app/docs/#components)
            print("ui関数が実行されました")
            return [angle, checkbox]
    
    # Extension main process
    # Type: (StableDiffusionProcessing, List<UI>) -> (Processed)
    # args is [StableDiffusionProcessing, UI1, UI2, ...]
    # def run(self, p, angle, checkbox):
        # TODO: get UI info through UI object angle, checkbox
        # proc = process_images(p)
        
        # 画像の左半分を白くする処理を追加
        # for i, img in enumerate(proc.images):
            # img_array = np.array(img)
            # height, width, _ = img_array.shape
            # img_array[:, :width // 2] = [255, 255, 255]  # 左半分を白くする
            # proc.images[i] = Image.fromarray(img_array)
        
        # return proc
        
    def run(self, p, angle, checkbox):
        # TODO: get UI info through UI object angle, checkbox
        print("ui関数が実行されました1")
        from modules import images, script_callbacks
        from modules.processing import process_images, Processed
        from modules.processing import Processed
        from modules.shared import opts, cmd_opts, state
        from PIL import Image
        print("ui関数が実行されました2")
        proc = process_images(p)
        print("ui関数が実行されました3")
        # 真っ青な画像を作成してprocに渡す
        blue_image = Image.new('RGB', (512, 512), (0, 0, 255))  # 512x512ピクセルの真っ青な画像
        proc.images = [blue_image for _ in proc.images]  # すべての画像を真っ青な画像に置き換える
        
        return proc
