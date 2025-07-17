# --- START OF FILE txtplus.py ---

class TextPlus:
    # This node is a simplified version inspired by a dynamic node structure
    @classmethod
    def INPUT_TYPES(s):
        # All text inputs are declared as 'hidden'.
        # The JavaScript part will create the visible widgets.
        hidden_inputs = {}
        for i in range(1, 21): # Max 20 inputs
            hidden_inputs[f"text_{i}"] = ("STRING", {"multiline": True})

        return {
            "required": {
                "delimiter": ("STRING", {"default": ", "}),
            },
            "hidden": hidden_inputs,
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("concat_text",)
    FUNCTION = "process"
    CATEGORY = "Data pro/text"

    def process(self, delimiter, **kwargs):
        # kwargs will contain all the hidden text inputs sent from the frontend
        texts = []
        # Iterate in order to ensure concatenation is correct
        for i in range(1, 21):
            text_value = kwargs.get(f"text_{i}", "")
            if text_value and text_value.strip():
                texts.append(text_value)
        
        concatenated_text = delimiter.join(texts)
        return (concatenated_text,)

# --- Node Mappings ---
NODE_CLASS_MAPPINGS = { "TextPlus": TextPlus, }
NODE_DISPLAY_NAME_MAPPINGS = { "TextPlus": "Dynamic Text (TxtPlus)", }