# --- START OF FILE LoadImageAndExtractWorkflow.py ---

import os
import json
import torch
import numpy as np
from PIL import Image
from folder_paths import get_input_directory
import re
import traceback

def tensor_to_pil(tensor):
    if tensor.ndim == 4: tensor = tensor[0]
    image_np = tensor.squeeze().mul(255).clamp(0, 255).byte().numpy()
    return Image.fromarray(image_np, 'RGB')

def pil_to_tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class LoadImageAndExtractWorkflow:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = get_input_directory()
        supported_formats = ['.png', '.jpg', '.jpeg', '.webp', '.bmp']
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and os.path.splitext(f)[1].lower() in supported_formats]
        return {
            "required": { "image": (sorted(files), {"image_upload": True}) },
            "optional": {
                "image_in": ("IMAGE",),
                "filename_in": ("STRING", {"multiline": False, "default": ""}),
                "directory_in": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    CATEGORY = "Data pro"
    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image", "mask", "workflow_json", "metadata_raw", "size")
    FUNCTION = "load_image_and_extract"

    def load_image_and_extract(self, image, image_in=None, filename_in=None, directory_in=None):
        img_pil = None
        image_tensor = None
        workflow_json, metadata_raw = "", ""
        is_batch_mode = image_in is not None and filename_in and filename_in.strip()

        if is_batch_mode:
            image_tensor, img_pil = image_in, tensor_to_pil(image_in)
            image_path = None
            if directory_in and directory_in.strip(): image_path = os.path.join(directory_in, os.path.basename(filename_in))
            elif os.path.isabs(filename_in): image_path = filename_in
            else: image_path = os.path.join(get_input_directory(), os.path.basename(filename_in))
            if image_path and os.path.exists(image_path):
                try:
                    with Image.open(image_path) as meta_img:
                        metadata_dict = meta_img.info or {}
                        workflow_json = metadata_dict.get('workflow') or metadata_dict.get('prompt') or ''
                        metadata_raw = json.dumps(metadata_dict, indent=2)
                except Exception as e: print(f"[{self.CATEGORY}] Error reading metadata from {image_path}: {e}")
            else: print(f"[{self.CATEGORY}] Warning: File not found for metadata extraction: {image_path}")
        else:
            image_path = os.path.join(get_input_directory(), image)
            img_pil = Image.open(image_path)
            image_tensor = pil_to_tensor(img_pil.convert("RGB"))
            metadata_dict = img_pil.info or {}
            workflow_json = metadata_dict.get('workflow') or metadata_dict.get('prompt') or ''
            metadata_raw = json.dumps(metadata_dict, indent=2)

        if img_pil is None: return (torch.zeros((1, 64, 64, 3)), torch.zeros((1, 64, 64)), "", "", "Error: No image loaded")
        
        width, height = img_pil.size
        mask = torch.zeros((1, height, width), dtype=torch.float32, device="cpu")
        if 'A' in img_pil.getbands(): mask = torch.from_numpy(np.array(img_pil.getchannel('A')).astype(np.float32) / 255.0)
        if image_tensor.ndim == 3: image_tensor = image_tensor.unsqueeze(0)
        if mask.ndim == 2: mask = mask.unsqueeze(0)
        return (image_tensor, mask, workflow_json, metadata_raw, f"{width}x{height}")

    @classmethod
    def IS_CHANGED(cls, image, **kwargs): return os.path.getmtime(os.path.join(get_input_directory(), image))

NODE_CLASS_MAPPINGS = {"LoadImageAndExtractWorkflow": LoadImageAndExtractWorkflow}
NODE_DISPLAY_NAME_MAPPINGS = {"LoadImageAndExtractWorkflow": "Load Image & Get Workflow"}