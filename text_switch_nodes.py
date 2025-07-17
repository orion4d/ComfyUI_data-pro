# --- START OF FILE text_switch_nodes.py (Version avec Logique Corrigée) ---

import random

class TextSwitch:
    """Nœud de switch booléen simple."""
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "select_true": ("BOOLEAN", {"default": True, "label_on": "Use text_true", "label_off": "Use text_false"}),
            },
            "optional": {
                "text_if_true": ("STRING", {"forceInput": True}),
                "text_if_false": ("STRING", {"forceInput": True}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)
    FUNCTION = "switch"
    CATEGORY = "Data pro/text"

    def switch(self, select_true, text_if_true="", text_if_false=""):
        return (text_if_true,) if select_true else (text_if_false,)

class DynamicInputTextSwitch:
    """Nœud de switch dynamique avec des entrées (pas des widgets)."""
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "select_mode": (["Numbered", "Random"],),
                "index": ("INT", {"default": 1, "min": 1, "max": 999, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)
    FUNCTION = "switch_text"
    CATEGORY = "Data pro/text"

    def switch_text(self, select_mode, index, seed, **kwargs):
        
        selected_text = ""

        # --- LOGIQUE CORRIGÉE ICI ---
        
        if select_mode == "Numbered":
            # On cherche directement l'entrée qui correspond au numéro de l'index.
            # kwargs.get() renverra None si l'entrée n'est pas connectée.
            key_to_find = f"text_{index}"
            value = kwargs.get(key_to_find)
            if value is not None:
                selected_text = value

        elif select_mode == "Random":
            # Pour le mode Random, l'ancienne logique de créer une liste des
            # entrées valides est correcte, car on veut choisir au hasard
            # parmi les options disponibles.
            valid_texts = []
            for key, value in kwargs.items():
                if key.startswith("text_") and value and str(value).strip():
                    valid_texts.append(value)
            
            if valid_texts:
                rng = random.Random(seed)
                selected_text = rng.choice(valid_texts)
        
        # S'assurer de toujours retourner un tuple avec une chaîne
        return (str(selected_text),)

NODE_CLASS_MAPPINGS = {
    "TextSwitch": TextSwitch,
    "DynamicInputTextSwitch": DynamicInputTextSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextSwitch": "Text Switch (Boolean)",
    "DynamicInputTextSwitch": "Dynamic Text Switch",
}