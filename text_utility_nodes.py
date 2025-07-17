# --- START OF FILE text_utility_nodes.py ---

import re

class FindAndReplaceText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "find": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "replace": ("STRING", {"multiline": False, "dynamicPrompts": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)
    FUNCTION = "find_and_replace"
    CATEGORY = "Data pro/text"

    def find_and_replace(self, text, find, replace):
        if not find: # Avoid replacing everything if 'find' is empty
            return (text,)
        
        # Simple string replacement
        new_text = text.replace(find, replace)
        return (new_text,)

class FormatText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "format_string": ("STRING", {
                    "multiline": True, 
                    "default": "A high-quality photo of {0}, in the artistic style of {1}."
                }),
            },
            "optional": {
                "input_0": ("STRING", {"forceInput": True}),
                "input_1": ("STRING", {"forceInput": True}),
                "input_2": ("STRING", {"forceInput": True}),
                "input_3": ("STRING", {"forceInput": True}),
                "input_4": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)
    FUNCTION = "format_text"
    CATEGORY = "Data pro/text"

    def format_text(self, format_string, 
                    input_0="", input_1="", input_2="", input_3="", input_4=""):
        
        # Using .format() is safe and handles missing placeholders gracefully
        # by raising an error, which is better than failing silently.
        try:
            formatted_text = format_string.format(input_0, input_1, input_2, input_3, input_4)
        except (IndexError, KeyError) as e:
            # If the format string is invalid (e.g., uses {5} but only 5 inputs exist)
            # return an error message in the output.
            formatted_text = f"FORMATTING ERROR: {e}. Check your format_string placeholders."
            
        return (formatted_text,)

# --- Node Mappings ---
NODE_CLASS_MAPPINGS = {
    "FindAndReplaceText": FindAndReplaceText,
    "FormatText": FormatText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FindAndReplaceText": "Find & Replace Text",
    "FormatText": "Format Text (f-string style)",
}