# --- START OF FILE PyCodePro_custom.py ---

import os
import torch
import numpy as np
from PIL import Image
import traceback
import io
from contextlib import redirect_stdout

PY_SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pyscripts")
if not os.path.exists(PY_SCRIPTS_DIR):
    os.makedirs(PY_SCRIPTS_DIR)

class PyCodePro_custom:

    # -----------------------------------------------------------------------------------
    # ▼▼▼ SECTION DE CONFIGURATION CENTRALE (MODIFIEZ ICI) ▼▼▼
    # -----------------------------------------------------------------------------------
    # Toutes les entrées/sorties sont définies ici dans un format unifié.
    # Pour changer le nombre d'une entrée/sortie, modifiez simplement sa valeur 'count'.

    # DÉFINITION DES ENTRÉES
    # Format: (préfixe, type_comfy, count, {options_dict})
    INPUT_CONFIG = [
        ("txt_in", "STRING", 10, {"forceInput": True}),
        ("int_in", "INT", 10, {"forceInput": True, "default": 0}),
        ("float_in", "FLOAT", 10, {"forceInput": True, "default": 0.0}),
        ("img_in", "IMAGE", 5, {}),
        ("mask_in", "MASK", 2, {}),
        ("latent_in", "LATENT", 1, {}),
        ("positive", "CONDITIONING", 1, {}),
        ("negative", "CONDITIONING", 1, {}),
        ("model", "MODEL", 2, {}),
        ("clip", "CLIP", 1, {}),
        ("vae", "VAE", 1, {}),
        ("audio_in", "*", 1, {}),
        ("video_in", "*", 1, {}),
        ("custom_in", "*", 4, {}),
    ]

    # DÉFINITION DES SORTIES
    # Format: (préfixe, type_comfy, count)
    OUTPUT_CONFIG = [
        ("txt_out", "STRING", 10),
        ("int_out", "INT", 10),
        ("float_out", "FLOAT", 10),
        ("img_out", "IMAGE", 5),
        ("mask_out", "MASK", 2),
        ("latent_out", "LATENT", 1),
        ("positive", "CONDITIONING", 1),
        ("negative", "CONDITIONING", 1),
        ("model", "MODEL", 2),
        ("clip", "CLIP", 1),
        ("vae", "VAE", 1),
        ("audio_out", "*", 1),
        ("video_out", "*", 1),
        ("custom_out", "*", 4),
    ]
    # -----------------------------------------------------------------------------------
    # ▲▲▲ FIN DE LA SECTION DE CONFIGURATION ▲▲▲
    # -----------------------------------------------------------------------------------


    # --- Génération dynamique des entrées/sorties (ne pas modifier) ---
    RETURN_TYPES = []
    RETURN_NAMES = []
    for prefix, comfy_type, count in OUTPUT_CONFIG:
        if count == 1:
            RETURN_NAMES.append(prefix)
            RETURN_TYPES.append(comfy_type)
        else:
            for i in range(1, count + 1):
                RETURN_NAMES.append(f"{prefix}_{i}")
                RETURN_TYPES.append(comfy_type)

    RETURN_TYPES += ("STRING",)
    RETURN_NAMES += ("Console",)
    RETURN_TYPES = tuple(RETURN_TYPES)
    RETURN_NAMES = tuple(RETURN_NAMES)

    FUNCTION = "execute_code"
    CATEGORY = "Data pro/advanced"

    @classmethod
    def INPUT_TYPES(s):
        script_files = ["None"] + [f for f in os.listdir(PY_SCRIPTS_DIR) if f.endswith(".py")]

        inputs = {
            "required": {
                "source": (["text_input", "file"],),
                "code": ("STRING", {"multiline": True, "default": "# Votre code Python ici"}),
                "script_file": (script_files,),
            },
            "optional": {}
        }

        for prefix, comfy_type, count, opts in s.INPUT_CONFIG:
            if count == 1:
                inputs["optional"][prefix] = (comfy_type, opts)
            else:
                for i in range(1, count + 1):
                    inputs["optional"][f"{prefix}_{i}"] = (comfy_type, opts)

        inputs["optional"]["trigger"] = ("*",)
        return inputs

    def _tensor_to_pil(self, tensor):
        if tensor is None: return None
        if tensor.ndim == 4 and tensor.shape[0] == 1: tensor = tensor.squeeze(0)
        return Image.fromarray(np.clip(255. * tensor.cpu().numpy(), 0, 255).astype(np.uint8))

    def _pil_to_tensor(self, pil_image):
        if pil_image is None: return None
        if pil_image.mode != 'RGB': pil_image = pil_image.convert('RGB')
        return torch.from_numpy(np.array(pil_image).astype(np.float32) / 255.0).unsqueeze(0)

    def execute_code(self, source, code, script_file, trigger=None, **kwargs):
        security_warning = "WARNING: Executing arbitrary Python code is a security risk...\n\n"
        user_code = ""
        if source == 'text_input': user_code = code
        elif source == 'file' and script_file != "None":
            filepath = os.path.join(PY_SCRIPTS_DIR, script_file)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f: user_code = f.read()
            else:
                return (*(None for _ in self.RETURN_NAMES), f"{security_warning}ERROR: File not found: {filepath}")

        IN = {}
        for key, value in kwargs.items():
            if key.startswith('img_in'):
                IN[key] = self._tensor_to_pil(value)
            else:
                IN[key] = value

        OUT = {}
        execution_scope = {'IN': IN, 'OUT': OUT, 'torch': torch, 'np': np, 'Image': Image}

        stdout_capture = io.StringIO()
        try:
            with redirect_stdout(stdout_capture):
                exec(user_code, execution_scope)
        except Exception:
            # Correction pour imprimer le traceback dans la capture de stdout
            # afin qu'il apparaisse dans la console du noeud
            traceback.print_exc(file=stdout_capture)
            final_stdout = security_warning + "--- EXECUTION FAILED ---\n" + stdout_capture.getvalue()
            # Retourner des None pour toutes les sorties attendues, plus le message d'erreur
            results = [None] * (len(self.RETURN_NAMES) -1)
            results.append(final_stdout)
            return tuple(results)


        final_stdout = security_warning + stdout_capture.getvalue()

        results = []
        output_names = self.RETURN_NAMES[:-1]

        for name in output_names:
            value = OUT.get(name)

            if name.startswith('txt_out'):
                results.append(str(value) if value is not None else "")
            elif name.startswith('int_out'):
                results.append(int(value) if value is not None else 0)
            elif name.startswith('float_out'):
                results.append(float(value) if value is not None else 0.0)
            elif name.startswith('img_out'):
                results.append(self._pil_to_tensor(value))
            else: # Cas générique pour MASK, LATENT, VAE, AUDIO, VIDEO, CUSTOM, etc.
                results.append(value)

        results.append(final_stdout)
        return tuple(results)

NODE_CLASS_MAPPINGS = { "PyCodePro_custom": PyCodePro_custom }
NODE_DISPLAY_NAME_MAPPINGS = { "PyCodePro_custom": "PyCode Pro (Custom)" }