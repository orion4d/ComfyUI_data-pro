# --- START OF FILE variable_nodes.py (Approche "Bus de Variables") ---

# Le dictionnaire reste notre "mémoire" pour la durée d'une exécution.
WORKFLOW_VARIABLES = {}

class VariableBus:
    """
    Ce nœud crée le "bus" initial. C'est le point de départ de votre chaîne de variables.
    Il ne fait rien d'autre que de créer un objet "pipe" vide.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}}

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("bus",)
    FUNCTION = "create_bus"
    CATEGORY = "Data pro/variables"

    def create_bus(self):
        # On initialise notre mémoire à chaque fois qu'un bus est créé.
        WORKFLOW_VARIABLES.clear() 
        # L'objet retourné n'a pas d'importance, sa seule existence force la connexion.
        return ({},)

class SetVariableOnBus:
    """
    Ce nœud se branche sur le bus, écrit une variable, et fait passer le bus.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "bus": ("*",),
                "variable_name": ("STRING", {"multiline": False, "default": "my_variable"}),
                "value": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("bus",)
    FUNCTION = "set_variable"
    CATEGORY = "Data pro/variables"

    def set_variable(self, bus, variable_name, value):
        WORKFLOW_VARIABLES[variable_name] = value
        print(f"[Data pro] BUS: Var '{variable_name}' set.")
        # On fait passer le bus pour pouvoir chaîner d'autres nœuds.
        return (bus,)

class GetVariableFromBus:
    """
    Ce nœud se branche sur le bus et récupère la valeur d'une variable.
    Il ne nécessite pas de sortie "bus" car il est souvent en fin de chaîne.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "bus": ("*",),
                "variable_name": ("STRING", {"multiline": False, "default": "my_variable"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_variable"
    CATEGORY = "Data pro/variables"

    def get_variable(self, bus, variable_name):
        value = WORKFLOW_VARIABLES.get(variable_name, "")
        if not value:
             print(f"[Data pro] BUS: Var '{variable_name}' not found.")
        return (value,)

# --- Enregistrement ---
NODE_CLASS_MAPPINGS = {
    "VariableBus": VariableBus,
    "SetVariableOnBus": SetVariableOnBus,
    "GetVariableFromBus": GetVariableFromBus,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VariableBus": "Variable Bus (Start)",
    "SetVariableOnBus": "Set Variable on Bus",
    "GetVariableFromBus": "Get Variable from Bus",
}