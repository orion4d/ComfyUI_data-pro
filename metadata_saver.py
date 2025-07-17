# --- START OF FILE metadata_saver.py ---

import os
import json
import re
import time
import torch
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from folder_paths import get_output_directory

class SaveImageWithRichMetadata:
    def __init__(self):
        self.output_dir = get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "optional": {
                "save_path": ("STRING", {"default": ""}),
                "datetime_format": (["False", "date_folder", "prefix_datetime"],),
                "positive_prompt": ("STRING", {"multiline": True, "default": ""}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "models": ("STRING", {"multiline": True, "default": ""}),
                "loras": ("STRING", {"multiline": True, "default": ""}),
                "extra_data": ("STRING", {"multiline": True, "default": ""}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Data pro"

    def save_images(self, images, filename_prefix="ComfyUI", save_path="", datetime_format="False",
                    positive_prompt="", negative_prompt="", models="", loras="", extra_data="",
                    prompt=None, extra_pnginfo=None):
        
        # --- NEW PATH LOGIC - INSPIRED BY YOUR WORKING CODE ---
        
        # 1. Determine the final output directory
        if save_path and save_path.strip():
            # Allow absolute paths or paths relative to the output directory
            if os.path.isabs(save_path):
                 full_save_path = save_path
            else:
                full_save_path = os.path.join(self.output_dir, save_path)
        else:
            full_save_path = self.output_dir

        # 2. Handle datetime formatting
        final_prefix = filename_prefix
        if datetime_format == "date_folder":
            date_folder = time.strftime("%Y-%m-%d")
            full_save_path = os.path.join(full_save_path, date_folder)
        elif datetime_format == "prefix_datetime":
            datetime_prefix = time.strftime("%Y-%m-%d_%H%M%S")
            final_prefix = f"{datetime_prefix}-{filename_prefix}"

        os.makedirs(full_save_path, exist_ok=True)

        # 3. Handle file counter
        counter = 1
        try:
            existing_files = os.listdir(full_save_path)
            pattern = re.compile(f"^{re.escape(final_prefix)}_(\\d{{5,}})_")
            max_num = 0
            for f in existing_files:
                match = pattern.match(f)
                if match: max_num = max(max_num, int(match.group(1)))
            counter = max_num + 1
        except OSError as e: print(f"[Data pro] Warning: Could not read directory for counter: {e}")
        
        # --- END OF NEW PATH LOGIC ---

        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            metadata = PngInfo()
            if prompt is not None: metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for key, value in extra_pnginfo.items(): metadata.add_text(key, json.dumps(value))

            parameters_text = ""
            if positive_prompt: parameters_text += f"{positive_prompt}\n"
            if negative_prompt: parameters_text += f"Negative prompt: {negative_prompt}\n"
            details_parts = []
            if models: details_parts.append(f"Models: {models.replace(chr(10), ', ')}")
            if loras: details_parts.append(f"Loras: {loras.replace(chr(10), ', ')}")
            if extra_data: details_parts.append(f"Extra: {extra_data.replace(chr(10), ' | ')}")
            if details_parts: parameters_text += ", ".join(details_parts)
            if parameters_text: metadata.add_text("parameters", parameters_text)

            file = f"{final_prefix}_{counter:05}_.png"
            full_path = os.path.join(full_save_path, file)
            img.save(full_path, pnginfo=metadata, compress_level=4)
            
            # --- ROBUST SUBFOLDER LOGIC FOR UI PREVIEW ---
            subfolder = ""
            try:
                # Check if the save path is within the ComfyUI output directory tree
                # This prevents ValueError on different drives (e.g., C: vs D:)
                if os.path.commonpath([full_save_path, self.output_dir]) == self.output_dir:
                    subfolder = os.path.relpath(full_save_path, self.output_dir)
                    if subfolder == '.': subfolder = ''
            except ValueError:
                # This happens if paths are on different drives on Windows.
                # In this case, we can't show a relative path, but the file is saved correctly.
                print(f"[Data pro] Note: Image saved to absolute path '{full_path}'. UI preview may not show relative path.")

            results.append({ "filename": file, "subfolder": subfolder, "type": self.type })
            counter += 1

        return { "ui": { "images": results } }

# --- Node Mappings ---
NODE_CLASS_MAPPINGS = { "SaveImageWithRichMetadata": SaveImageWithRichMetadata }
NODE_DISPLAY_NAME_MAPPINGS = { "SaveImageWithRichMetadata": "Save Image with Rich Metadata" }