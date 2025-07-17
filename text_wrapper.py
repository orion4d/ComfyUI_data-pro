# --- START OF FILE text_wrapper.py ---

class TextWrapper:
    """
    Un nœud pour encadrer un texte avec des caractères prédéfinis 
    (parenthèses, crochets, etc.) ou avec un préfixe et un suffixe manuels.
    """
    @classmethod
    def INPUT_TYPES(s):
        # Liste des options pour le menu déroulant
        wrapping_styles = [
            "Parentheses ()",
            "Brackets []",
            "Braces {}",
            "Backslashes \\",  # Le double backslash est nécessaire pour représenter un seul \ dans la chaîne
            "Slashes //",
            "Manual",
        ]

        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                # Le widget COMBO crée un menu déroulant
                "style": (wrapping_styles, ),
                # Les champs manuels sont toujours présents, mais utilisés uniquement si "Manual" est sélectionné
                "manual_prefix": ("STRING", {"multiline": False, "default": ""}),
                "manual_suffix": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("wrapped_text",)
    FUNCTION = "wrap"
    CATEGORY = "Data pro/text"

    def wrap(self, text, style, manual_prefix, manual_suffix):
        # Initialise le préfixe et le suffixe
        prefix = ""
        suffix = ""

        # Définit le préfixe/suffixe en fonction du style choisi
        if style == "Parentheses ()":
            prefix, suffix = "(", ")"
        elif style == "Brackets []":
            prefix, suffix = "[", "]"
        elif style == "Braces {}":
            prefix, suffix = "{", "}"
        elif style == "Backslashes \\":
            prefix, suffix = "\\", "\\"
        elif style == "Slashes //":
            prefix, suffix = "//", "//"
        elif style == "Manual":
            prefix, suffix = manual_prefix, manual_suffix
            
        # N'applique l'encadrement que si le texte n'est pas vide
        # pour éviter d'avoir "()" ou "[]" tout seuls.
        if text and text.strip():
            final_text = f"{prefix}{text}{suffix}"
        else:
            final_text = "" # Retourne une chaîne vide si l'entrée est vide

        # Retourne le résultat sous forme de tuple, comme requis par ComfyUI
        return (final_text,)

# --- Enregistrement du Nœud pour ComfyUI ---
NODE_CLASS_MAPPINGS = {
    "TextWrapper": TextWrapper
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextWrapper": "Text Wrapper"
}