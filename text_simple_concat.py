# --- START OF FILE text_simple_concat.py ---

class TextSimpleConcat:
    """
    Un nœud simple pour concaténer deux textes avec un préfixe, un suffixe et un délimiteur.
    Pas de JavaScript, uniquement des widgets standards de ComfyUI.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_1": ("STRING", {"multiline": True, "default": ""}),
                "text_2": ("STRING", {"multiline": True, "default": ""}),
                "delimiter": ("STRING", {"multiline": False, "default": " "}),
                "prefix": ("STRING", {"multiline": False, "default": ""}),
                "suffix": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "concat"
    # Catégorie mise à jour pour correspondre à votre package
    CATEGORY = "Data pro/text" 

    def concat(self, text_1, text_2, delimiter, prefix, suffix):
        # Créer une liste avec les textes qui ne sont pas vides
        texts_to_join = []
        if text_1 and text_1.strip():
            texts_to_join.append(text_1)
        if text_2 and text_2.strip():
            texts_to_join.append(text_2)
        
        # Joindre les textes avec le délimiteur
        combined_texts = delimiter.join(texts_to_join)
        
        # Ajouter le préfixe et le suffixe
        final_text = f"{prefix}{combined_texts}{suffix}"
        
        # Retourner le résultat sous forme de tuple
        return (final_text,)

# --- Enregistrement des Nœuds pour ComfyUI ---
NODE_CLASS_MAPPINGS = {
    "TextSimpleConcat": TextSimpleConcat
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextSimpleConcat": "Simple Text Concat"
}