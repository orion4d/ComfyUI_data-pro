# __init__.py for the 'data-pro' custom node pack
# This file dynamically discovers and loads all nodes from the specified python files.

import importlib
import traceback

# This tells ComfyUI to look for a 'js' folder in this directory for any web-related files.
# This is crucial for nodes that have a custom frontend component (e.g., SimpleFileWriter).
WEB_DIRECTORY = "js"

# Dictionaries to hold all the node mappings, which will be populated dynamically.
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# --- List of node modules to load ---
# Add the filename (without .py) of any new node file you create to this list.
# The list is alphabetized for easier maintenance.
node_files_to_load = [
    "exif_reader",
    "LoadImageAndExtractWorkflow",
    "metadata_saver",
    "ParseJsonDetails",
    "ParseMetadata",
    "PyCodePro",
    "PyCodePro_custom",
    "simple_reader",
    "simple_writer",
    "text_multiconcat",
    "text_simple_concat",
    "text_switch_nodes",
    "text_utility_nodes",
    "text_wrapper",
    "txtplus",
    "variable_nodes",
    "workflow_converter",
]

# --- Dynamic Import Logic ---
for module_name in node_files_to_load:
    try:
        # The '.' in '.{module_name}' is crucial for relative imports within a package.
        module = importlib.import_module(f".{module_name}", __name__)
        
        if hasattr(module, "NODE_CLASS_MAPPINGS"):
            NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
        
        if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
            NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)

        print(f"✅ [Data pro] Loaded nodes from: {module_name}.py")

    except Exception as e:
        print(f"❌ [Data pro] Failed to load nodes from {module_name}.py. Reason: {e}")
        traceback.print_exc()

print("🐍 [Data pro] All nodes loaded successfully.")

# This is what ComfyUI will look for and use.
__all__ = [
    'NODE_CLASS_MAPPINGS',
    'NODE_DISPLAY_NAME_MAPPINGS',
    'WEB_DIRECTORY'
]