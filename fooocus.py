from gradio_client import Client
import random
import time
import os
import json
import upyun_util
from bs4 import BeautifulSoup

deal_cache = {}
clients = {}
in_use = False


def generate_in_paint_mode(prompts, base_model, refiner, refiner_weight, paint_url, mask_url, face_url, mode, cnt,
                           key, client_key):
    in_use = True
    # print("some one gen ")
    if mode == 0:
        # default
        in_paint_engine = "v2.6"
        in_paint_ds = 1
        in_paint_rf = 0.618
    else:
        # detail
        in_paint_engine = "None"
        in_paint_ds = 0.5
        in_paint_rf = 0

    MIN_SEED = 0
    MAX_SEED = 2 ** 63 - 1
    generate(prompts, base_model, refiner, refiner_weight, paint_url, mask_url, face_url, in_paint_engine, in_paint_ds,
             in_paint_rf, str(random.randint(MIN_SEED, MAX_SEED)), cnt, key, client_key)


def generate(prompts, base_model, refiner, refiner_weight, paint_url, mask_url, face_url, in_paint_engine, in_paint_ds,
             in_paint_rf, seed, cnt, key, client_key):

    if client_key not in clients:
        clients[client_key] = Client(client_key)

    client = clients[client_key]
    swap_face_str = "FaceSwap"
    stop_at = 0.9
    weight = 0.75

    if face_url is None or face_url == "":
        face_url = ""
        swap_face_str = "ImagePrompt"
        stop_at = 0
        weight = 0

    client.predict(
        False,  # bool in 'Generate Image Grid for Each Batch' Checkbox component
        prompts,  # str in 'parameter_11' Textbox component
        "unrealistic, saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
        # str in 'Negative Prompt' Textbox component
        ["Fooocus V2", "Fooocus Photograph"],  # List[str] in 'Selected Styles' Checkboxgroup component
        "Speed",  # str in 'Performance' Radio component
        "704×1408 <span style='color: grey;'> ∣ 1:2</span>",  # str in 'Aspect Ratios' Radio component
        cnt,  # int | float (numeric value between 1 and 32)in 'Image Number' Slider component
        "png",  # str in 'Output Format' Radio component
        seed,  # str in 'Seed' Textbox component
        False,  # bool in 'Read wildcards in order' Checkbox component
        2,  # int | float (numeric value between 0.0 and 30.0) in 'Image Sharpness' Slider component
        3,  # int | float (numeric value between 1.0 and 30.0) in 'Guidance Scale' Slider component
        base_model,
        # str (Option from: ['animaPencilXL_v100.safetensors', 'asianrealisticSdlife_v60.safetensors', 'copaxTimelessxlSDXL1_v11Lightning.safetensors', 'epicrealismXL_v5Ultimate.safetensors', 'iniverseMixXLSFWNSFW_74Real.safetensors', 'juggernautXL_v8Rundiffusion.safetensors', 'majicmixRealistic_v7.safetensors', 'newrealityxlAllInOne_30Experimental.safetensors', 'realisticStockPhoto_v20.safetensors', 'realvisxlV40_v40LightningBakedvae.safetensors']) in 'Base Model (SDXL only)' Dropdown component
        refiner,
        # str (Option from: ['None', 'animaPencilXL_v100.safetensors', 'asianrealisticSdlife_v60.safetensors', 'copaxTimelessxlSDXL1_v11Lightning.safetensors', 'epicrealismXL_v5Ultimate.safetensors', 'iniverseMixXLSFWNSFW_74Real.safetensors', 'juggernautXL_v8Rundiffusion.safetensors', 'majicmixRealistic_v7.safetensors', 'newrealityxlAllInOne_30Experimental.safetensors', 'realisticStockPhoto_v20.safetensors', 'realvisxlV40_v40LightningBakedvae.safetensors']) in 'Refiner (SDXL or SD 1.5)' Dropdown component
        refiner_weight,  # int | float (numeric value between 0.1 and 1.0) in 'Refiner Switch At' Slider component
        False,  # bool in 'Enable' Checkbox component
        "None",
        # str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'SDXL_FILM_PHOTOGRAPHY_STYLE_BetaV0.4.safetensors']) in 'LoRA 1' Dropdown component
        - 2,  # int | float (numeric value between -2 and 2) in 'Weight' Slider component
        False,  # bool in 'Enable' Checkbox component
        "None",
        # str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'SDXL_FILM_PHOTOGRAPHY_STYLE_BetaV0.4.safetensors']) in 'LoRA 2' Dropdown component
        - 2,  # int | float (numeric value between -2 and 2) in 'Weight' Slider component
        False,  # bool in 'Enable' Checkbox component
        "None",
        # str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'SDXL_FILM_PHOTOGRAPHY_STYLE_BetaV0.4.safetensors']) in 'LoRA 3' Dropdown component
        - 2,  # int | float (numeric value between -2 and 2) in 'Weight' Slider component
        False,  # bool in 'Enable' Checkbox component
        "None",
        # str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'SDXL_FILM_PHOTOGRAPHY_STYLE_BetaV0.4.safetensors'])in 'LoRA 4' Dropdown component
        - 2,  # int | float (numeric value between -2 and 2) in 'Weight' Slider component
        False,  # bool in 'Enable' Checkbox component
        "None",
        # str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'SDXL_FILM_PHOTOGRAPHY_STYLE_BetaV0.4.safetensors']) in 'LoRA 5' Dropdown component
        - 2,  # int | float (numeric value between -2 and 2) in 'Weight' Slider component
        True,  # bool in 'Input Image' Checkbox component
        "inpaint",  # str in 'parameter_91' Textbox component
        "Disabled",  # str in 'Upscale or Variation:' Radio component
        "",  # str (filepath or URL to image) in 'Drag above image to here' Image component
        [],  # List[str] in 'Outpaint Direction' Checkboxgroup component
        paint_url,  # str (filepath or URL to image) in 'Drag inpaint or outpaint image to here' Image component
        "",  # str in 'Inpaint Additional Prompt' Textbox component
        mask_url,  # str (filepath or URL to image) in 'Mask Upload' Image component
        True,  # bool in 'Disable Preview' Checkbox component
        True,  # bool in 'Disable Intermediate Results' Checkbox component
        False,  # bool in 'Disable seed increment' Checkbox component
        1.5,  # int | float (numeric value between 0.1 and 3.0) in 'Positive ADM Guidance Scaler' Slider component
        0.8,  # int | float (numeric value between 0.1 and 3.0) in 'Negative ADM Guidance Scaler' Slider component
        0.3,  # int | float (numeric value between 0.0 and 1.0) in 'ADM Guidance End At Step' Slider component
        7,  # int | float (numeric value between 1.0 and 30.0) in 'CFG Mimicking from TSNR' Slider component
        "dpmpp_2m_sde_gpu",
        # str (Option from: ['euler', 'euler_ancestral', 'heun', 'heunpp2', 'dpm_2', 'dpm_2_ancestral', 'lms', 'dpm_fast', 'dpm_adaptive', 'dpmpp_2s_ancestral', 'dpmpp_sde', 'dpmpp_sde_gpu', 'dpmpp_2m', 'dpmpp_2m_sde', 'dpmpp_2m_sde_gpu', 'dpmpp_3m_sde', 'dpmpp_3m_sde_gpu', 'ddpm', 'lcm', 'ddim', 'uni_pc', 'uni_pc_bh2']) in 'Sampler' Dropdown component
        "karras",
        # str (Option from: ['normal', 'karras', 'exponential', 'sgm_uniform', 'simple', 'ddim_uniform', 'lcm', 'turbo']) in 'Scheduler' Dropdown component
        - 1,  # int | float (numeric value between -1 and 200) in 'Forced Overwrite of Sampling Step' Slider component
        - 1,
        # int | float (numeric value between -1 and 200) in 'Forced Overwrite of Refiner Switch Step' Slider component
        - 1,
        # int | float (numeric value between -1 and 2048) in 'Forced Overwrite of Generating Width' Slider component
        - 1,
        # int | float (numeric value between -1 and 2048) in 'Forced Overwrite of Generating Height' Slider component
        - 1,
        # int | float (numeric value between -1 and 1.0) in 'Forced Overwrite of Denoising Strength of "Vary"' Slider component
        - 1,
        # int | float (numeric value between -1 and 1.0) in 'Forced Overwrite of Denoising Strength of "Upscale"' Slider component
        False,  # bool in 'Mixing Image Prompt and Vary/Upscale' Checkbox component
        True,  # bool in 'Mixing Image Prompt and Inpaint' Checkbox component
        False,  # bool in 'Debug Preprocessors' Checkbox component
        False,  # bool in 'Skip Preprocessors' Checkbox component
        64,  # int | float (numeric value between 1 and 255) in 'Canny Low Threshold' Slider component
        128,  # int | float (numeric value between 1 and 255) in 'Canny High Threshold' Slider component
        "joint",  # str (Option from: ['joint', 'separate', 'vae']) in 'Refiner swap method' Dropdown component
        0.25,  # int | float (numeric value between 0.0 and 1.0) in 'Softness of ControlNet' Slider component
        False,  # bool in 'Enabled' Checkbox component
        0,  # int | float (numeric value between 0 and 2) in 'B1' Slider component
        0,  # int | float (numeric value between 0 and 2) in 'B2' Slider component
        0,  # int | float (numeric value between 0 and 4) in 'S1' Slider component
        0,  # int | float (numeric value between 0 and 4) in 'S2' Slider component
        False,  # bool in 'Debug Inpaint Preprocessing' Checkbox component
        False,  # bool in 'Disable initial latent in inpaint' Checkbox component
        in_paint_engine,  # str (Option from: ['None', 'v1', 'v2.5', 'v2.6']) in 'Inpaint Engine' Dropdown component
        in_paint_ds,  # int | float (numeric value between 0.0 and 1.0) in 'Inpaint Denoising Strength' Slider component
        in_paint_rf,  # int | float (numeric value between 0.0 and 1.0) in 'Inpaint Respective Field' Slider component
        True,  # bool in 'Enable Mask Upload' Checkbox component
        False,  # bool in 'Invert Mask' Checkbox component
        0,  # int | float (numeric value between -64 and 64) in 'Mask Erode or Dilate' Slider component
        False,  # bool in 'Save Metadata to Images' Checkbox component
        "fooocus",  # str in 'Metadata Scheme' Radio component
        face_url,  # str (filepath or URL to image) in 'Image' Image component
        stop_at,  # int | float (numeric value between 0.0 and 1.0) in 'Stop At' Slider component
        weight,  # int | float (numeric value between 0.0 and 2.0) in 'Weight' Slider    component
        swap_face_str,  # str in 'Type' Radio component
        "",  # str (filepath or URL to image) in 'Image' Image component
        0,  # int | float (numeric value between 0.0 and 1.0) in 'Stop At' Slider component
        0,  # int | float (numeric value between 0.0 and 2.0) in 'Weight' Slider component
        "ImagePrompt",  # str in 'Type' Radio component
        "",  # str (filepath or URL to image) in 'Image' Image component
        0,  # int | float (numeric value between 0.0 and 1.0) in 'Stop At' Slider component
        0,  # int | float (numeric value between 0.0 and 2.0) in 'Weight' Slider component
        "ImagePrompt",  # str in 'Type' Radio component
        "",  # str (filepath or URL to image) in 'Image' Image component
        0,  # int | float (numeric value between 0.0 and 1.0) in 'Stop At' Slider component
        0,  # int | float (numeric value between 0.0 and 2.0) in 'Weight' Slider component
        "ImagePrompt",  # str in 'Type' Radio component
        fn_index=40
    )

    # result = client.predict(fn_index=41)

    job = client.submit(fn_index=41)
    while not job.done():
        size = len(job.outputs())
        if size > 0:
            rst = job.outputs()[size - 1][0]
            # print(rst)
            if 'value' in rst:
                htlm = rst['value']
                soup = BeautifulSoup(htlm, 'lxml')
                # 找到 progress 标签
                progress = soup.find('progress')
                # 获取 value 属性
                value = progress.get('value') if progress else None
                deal_cache[key] = {
                    "finish": False,
                    "progress": value,
                    "cnt": f"0/{cnt}"
                }
        time.sleep(1)

    size = len(job.outputs())

    # print(paint_url)
    # print(job.outputs()[size - 1])
    path = job.outputs()[size - 1][3]
    print(path)
    full_path = os.path.join(path, "captions.json")
    with open(full_path, 'r') as file:
        file_content = file.read()
        data = json.loads(file_content)
        img_path = []
        for k in data:
            url = upyun_util.upload(k)
            img_path.append(url)
        print(img_path)
        deal_cache[key] = {
            "finish": True,
            "list": img_path,
            "progress": 100,
            "cnt": f"0/{cnt}"
        }
        in_use = False

