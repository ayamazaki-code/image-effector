# ver: v0.2.0

import gradio as gr
import numpy as np
from PIL import Image, ImageOps

def apply_effect(image, effect):
    if image is None:
        return None

    pil_image = Image.fromarray(image)

    if effect == "モノクロ":
        processed_image = pil_image.convert('L')
    elif effect == "セピア":
        grayscale = pil_image.convert('L')
        processed_image = ImageOps.colorize(grayscale, '#704214', '#C0A080')
    elif effect == "ネガポジ反転":
        if pil_image.mode == 'RGBA':
            r, g, b, a = pil_image.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted_image = ImageOps.invert(rgb_image)
            r2, g2, b2 = inverted_image.split()
            processed_image = Image.merge('RGBA', (r2, g2, b2, a))
        else:
            processed_image = ImageOps.invert(pil_image.convert('RGB'))
    else:
        processed_image = pil_image

    return processed_image

with gr.Blocks() as demo:
    gr.Markdown("# イメージ・エフェクター v0.2.0")
    gr.Markdown("画像をアップロードして、好きなエフェクトを選択してください。")
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(label="画像をアップロード", type="numpy")
            effect_selector = gr.Radio(
                ["モノクロ", "セピア", "ネガポジ反転"],
                label="エフェクトを選択"
            )
        with gr.Column():
            image_output = gr.Image(label="変換後の画像")
    
    inputs = [image_input, effect_selector]
    outputs = image_output
    
    for component in inputs:
        component.change(fn=apply_effect, inputs=inputs, outputs=outputs)

# サーバーで実行するための記述
demo.launch()
