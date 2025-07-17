# --- START OF FILE workflow_converter.py ---

import os
import json
from folder_paths import get_output_directory
import traceback

# --- Node: Convert API JSON to full, loadable Workflow JSON ---
class ConvertApiToWorkflow:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_json": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "save_to_file": ("BOOLEAN", {"default": False}),
                "filename": ("STRING", {"default": "rebuilt_workflow.json"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("workflow_json",)
    FUNCTION = "convert"
    CATEGORY = "Data pro"
    
    def convert(self, api_json, save_to_file, filename):
        try:
            api_data = json.loads(api_json)
            
            if 'nodes' in api_data and 'links' in api_data:
                rebuilt_json = json.dumps(api_data, indent=2)
                if save_to_file: self._save_file(rebuilt_json, filename)
                return (rebuilt_json,)

            nodes = []
            links = []
            link_id_counter = 1
            max_node_id = 0
            node_y_pos = 50.0

            sorted_node_ids = sorted(api_data.keys(), key=lambda x: int(x))

            for node_id_str in sorted_node_ids:
                node_id = int(node_id_str)
                node_data = api_data[node_id_str]
                max_node_id = max(max_node_id, node_id)
                
                # --- BUG FIX STARTS HERE ---
                rebuilt_inputs = []
                widgets_for_this_node = []

                input_slot_counter = 0
                for input_name, value in node_data.get("inputs", {}).items():
                    input_info = {"name": input_name, "type": "*", "link": None}
                    
                    if isinstance(value, list) and len(value) == 2 and isinstance(value[0], str):
                        # This is a link from another node
                        source_node_id = int(value[0])
                        source_output_slot = int(value[1])
                        
                        input_info["link"] = link_id_counter
                        
                        link_info = [
                            link_id_counter, source_node_id, source_output_slot,
                            node_id, input_slot_counter, "*"
                        ]
                        links.append(link_info)
                        link_id_counter += 1
                    else:
                        # This is a widget value
                        widgets_for_this_node.append(value)
                    
                    rebuilt_inputs.append(input_info)
                    input_slot_counter += 1
                # --- BUG FIX ENDS HERE ---

                new_node = {
                    "id": node_id,
                    "type": node_data.get("class_type"),
                    "pos": [100.0, node_y_pos],
                    "size": node_data.get("size", {"0": 320.0, "1": 180.0}),
                    "flags": {},
                    "order": node_id,
                    "mode": 0,
                    "inputs": rebuilt_inputs,
                    "outputs": node_data.get("outputs", []),
                    "properties": node_data.get("properties", {}),
                    "widgets_values": widgets_for_this_node, # Use the correctly populated list
                }
                
                nodes.append(new_node)
                node_y_pos += 220.0

            rebuilt_workflow = {
                "last_node_id": max_node_id,
                "last_link_id": link_id_counter,
                "nodes": nodes,
                "links": links,
                "groups": [],
                "config": {},
                "extra": {},
                "version": 0.4
            }
            
            rebuilt_json = json.dumps(rebuilt_workflow, indent=2)
            
            if save_to_file: self._save_file(rebuilt_json, filename)
                
            return (rebuilt_json,)

        except Exception:
            error_details = traceback.format_exc()
            print(f"[ERROR] ConvertApiToWorkflow failed:\n{error_details}")
            return (f"CONVERSION FAILED:\n\n{error_details}",)

    def _save_file(self, content, filename):
        output_dir = get_output_directory()
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        
        if not filename.lower().endswith('.json'): filename += '.json'
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f: f.write(content)
        print(f"Workflow saved to: {filepath}")

# --- Node Mappings ---
NODE_CLASS_MAPPINGS = { "ConvertApiToWorkflow": ConvertApiToWorkflow }
NODE_DISPLAY_NAME_MAPPINGS = { "ConvertApiToWorkflow": "Convert API to Workflow" }