# --- START OF FILE ParseMetadata.py ---

import json, re, traceback
from .ParseJsonDetails import BaseMetadataParser # Import the shared base class

class ParseMetadata(BaseMetadataParser):
    @classmethod
    def INPUT_TYPES(cls): return {"required": {"metadata_raw": ("STRING", {"multiline": True})}}
    FUNCTION = "parse_metadata"

    def parse_metadata(self, metadata_raw):
        try:
            param_text = ""
            try: param_text = json.loads(metadata_raw).get("parameters", "")
            except Exception: param_text = metadata_raw
            if not param_text or not param_text.strip(): return ("",) * 9 + ("Empty metadata",)
            
            prompt_lines = []
            for line in param_text.strip().split("\n"):
                if line.strip().lower().startswith("negative prompt:"): break
                prompt_lines.append(line.strip())
            prompt = " ".join(prompt_lines).strip()
            neg_match = re.search(r"negative prompt:\s*(.*?)(?:\n\w+:|$)", param_text, re.IGNORECASE | re.DOTALL)
            negative_prompt = neg_match.group(1).strip() if neg_match else ""

            def extract(key):
                match = re.search(rf"{key}:\s*([^\n,]+)", param_text, re.IGNORECASE)
                return match.group(1).strip() if match else ""
            
            sampler, steps, cfg, seed, model = extract("sampler"), extract("steps"), extract("cfg scale"), extract("seed"), extract("model")
            loras_found = re.findall(r"<lora:([^>]+)>", param_text)
            if lora_hashes := extract("lora hashes"):
                if lora_hashes.lower() != 'none':
                    loras_found.extend([f"{h.split(':')[0].strip()} (hash:{h.split(':')[1].strip()})" for h in lora_hashes.split(',') if ':' in h])
            loras = "\n".join(dict.fromkeys(loras_found))
            
            details = []
            if size := extract("size"): details.append(f"Size: {size}")
            for key in ["Denoising strength", "Hires upscaler", "Hires upscale", "Hires steps"]:
                if val := extract(key): details.append(f"{key}: {val}")
            
            other = f"Model hash: {extract('model hash')}" if extract('model hash') else ""
            return (prompt, negative_prompt, model, loras, sampler, steps, cfg, seed, ", ".join(details), other)
        except Exception: return ("",) * 9 + (f"CRASH! Error in node logic:\n\n{traceback.format_exc()}",)

NODE_CLASS_MAPPINGS = {"ParseMetadata": ParseMetadata}
NODE_DISPLAY_NAME_MAPPINGS = {"ParseMetadata": "Parse metadata"}