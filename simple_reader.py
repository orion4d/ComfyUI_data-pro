# simple_reader.py
import os

class SimpleFileReader:
    """
    Un node simple pour lire le contenu brut d'un fichier et le sortir en tant que chaîne de caractères.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # Le chemin du fichier à lire.
                # Par défaut, il pointe vers le dossier 'input' de ComfyUI, une convention courante.
                "filepath": ("STRING", {
                    "multiline": False,
                    "default": "input/my_file.txt"
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "read_file"
    CATEGORY = "Data pro/files"

    def read_file(self, filepath):
        # Vérifie si le fichier existe avant d'essayer de le lire
        if not os.path.exists(filepath):
            error_message = f"❌ ERROR: File not found at path: {filepath}"
            print(error_message)
            # Renvoie une chaîne vide si le fichier n'existe pas pour ne pas bloquer le workflow
            return ("",)

        try:
            # Ouvre le fichier en mode lecture ('r') avec l'encodage UTF-8
            with open(filepath, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            print(f"✅ Successfully read file: {filepath}")
            return (file_content,)

        except Exception as e:
            error_message = f"❌ ERROR: Could not read file {filepath}. Reason: {e}"
            print(error_message)
            # Renvoie une chaîne vide en cas d'autre erreur de lecture
            return ("",)

# Dictionnaires pour l'enregistrement du node
NODE_CLASS_MAPPINGS = {
    "SimpleFileReader": SimpleFileReader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleFileReader": "Simple File Reader"
}