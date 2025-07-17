# --- START OF FILE text_multiconcat.py ---

class TextMultiConcatBase:
    """
    Classe de base pour les nœuds de concaténation de texte.
    Contient la logique partagée pour joindre les textes avec un délimiteur.
    """
    # Les classes enfants définiront INPUT_TYPES
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "concat"
    CATEGORY = "Data pro/text"

    def concat(self, delimiter, **kwargs):
        """
        Concatène tous les arguments textuels non vides fournis via kwargs.
        kwargs contiendra text_1, text_2, etc.
        """
        # On trie les clés pour s'assurer que l'ordre est text_1, text_2, ... text_10, etc.
        sorted_keys = sorted(kwargs.keys(), key=lambda k: int(k.split('_')[1]))
        
        texts_to_join = []
        for key in sorted_keys:
            text_value = kwargs.get(key, "")
            if text_value and str(text_value).strip():
                texts_to_join.append(str(text_value))
        
        # Joindre les textes avec le délimiteur
        final_text = delimiter.join(texts_to_join)
        
        # Retourner le résultat sous forme de tuple
        return (final_text,)

# --- Nœud pour 5 entrées ---
class TextConcatx5(TextMultiConcatBase):
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "delimiter": ("STRING", {"multiline": False, "default": ", "}),
            }
        }
        for i in range(1, 6):
            inputs["required"][f"text_{i}"] = ("STRING", {"multiline": True, "default": ""})
        return inputs

# --- Nœud pour 10 entrées ---
class TextConcatx10(TextMultiConcatBase):
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "delimiter": ("STRING", {"multiline": False, "default": ", "}),
            }
        }
        for i in range(1, 11):
            inputs["required"][f"text_{i}"] = ("STRING", {"multiline": True, "default": ""})
        return inputs
        
# --- Nœud pour 20 entrées ---
class TextConcatx20(TextMultiConcatBase):
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "delimiter": ("STRING", {"multiline": False, "default": ", "}),
            }
        }
        for i in range(1, 21):
            inputs["required"][f"text_{i}"] = ("STRING", {"multiline": True, "default": ""})
        return inputs

# --- Enregistrement des Nœuds pour ComfyUI ---
NODE_CLASS_MAPPINGS = {
    "TextConcatx5": TextConcatx5,
    "TextConcatx10": TextConcatx10,
    "TextConcatx20": TextConcatx20,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextConcatx5": "Text Concat (x5)",
    "TextConcatx10": "Text Concat (x10)",
    "TextConcatx20": "Text Concat (x20)",
}