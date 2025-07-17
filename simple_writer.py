# simple_writer.py
import os

class SimpleFileWriter:
    """
    Un node pour enregistrer du texte brut dans un fichier avec une extension choisie (y compris personnalisée).
    """
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        # Liste des extensions communes
        common_extensions = ["txt", "json", "md", "csv", "py", "svg", "html", "css", "js", "log"]
        
        # On ajoute l'option 'custom' au début pour la rendre visible
        extension_options = ["custom"] + common_extensions
        
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "filename_prefix": ("STRING", {
                    "multiline": False,
                    "default": "output/my_text_file"
                }),
                "extension_choice": (extension_options,),
                "mode": (["Overwrite", "Append"],),
            },
            # Le champ 'custom_extension' est optionnel car il ne sera utilisé
            # que si 'extension_choice' est réglé sur 'custom'.
            "optional": {
                "custom_extension": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "save_file"
    CATEGORY = "Data pro/files"  # Catégorie mise à jour pour correspondre à votre pack

    def save_file(self, text, filename_prefix, extension_choice, mode, custom_extension=""):
        # Déterminer quelle extension utiliser
        if extension_choice == "custom":
            # On utilise l'extension personnalisée, en s'assurant qu'elle n'est pas vide
            final_extension = custom_extension.strip().lstrip('.')
            if not final_extension:
                print("⚠️ WARNING: Custom extension selected but field is empty. Defaulting to .txt")
                final_extension = "txt"
        else:
            # On utilise le choix du menu déroulant
            final_extension = extension_choice
        
        full_filename = f"{filename_prefix}.{final_extension}"
        
        directory = os.path.dirname(full_filename)
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)
            
        write_mode = 'a' if mode == "Append" else 'w'
        
        try:
            with open(full_filename, write_mode, encoding='utf-8') as f:
                f.write(text)
            
            message = f"File appended to: {full_filename}" if write_mode == 'a' else f"File saved to: {full_filename}"
            print(f"✅ {message}")
            
        except Exception as e:
            print(f"❌ Error saving file {full_filename}: {e}")
            
        return {"ui": {}}

# Le reste du fichier pour l'enregistrement reste le même, mais sera géré par __init__.py
# Vous pouvez laisser ces dictionnaires ici ou les supprimer si __init__.py les gère entièrement.
NODE_CLASS_MAPPINGS = {
    "SimpleFileWriter": SimpleFileWriter
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleFileWriter": "Simple File Writer"
}