# --- START OF FILE ParseJsonDetails.py ---

import json, re, traceback

class BaseMetadataParser:
    CATEGORY = "Data pro"
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt", "model(s)", "lora(s)", "sampler", "steps", "cfg_scale", "seed(s)", "sampler_details", "other_text")

class ParseJsonDetails(BaseMetadataParser):
    @classmethod
    def INPUT_TYPES(cls): return {"required": {"workflow_json": ("STRING", {"multiline": True})}}
    FUNCTION = "parse_json"

    def _get_real_value(self, input_val, all_data):
        val = input_val
        for _ in range(10):
            if isinstance(val, list) and len(val) == 2 and isinstance(val[0], (str, int)):
                try:
                    source_node = all_data.get(str(val[0]))
                    if not source_node: break
                    
                    # Handle API format where values are in 'inputs'
                    source_inputs = source_node.get("inputs", {})
                    if isinstance(source_inputs, dict):
                         # In API format, value can be directly in inputs
                        found = False
                        for key in ['text', 'value', 'seed', 'INT', 'FLOAT', 'STRING']:
                            if key in source_inputs: 
                                val = source_inputs[key]
                                found = True
                                break
                        if found: continue # Continue lookup from the new value

                    # Handle UI format where widget values are in 'widgets_values'
                    if 'widgets_values' in source_node and isinstance(source_node['widgets_values'], list) and len(source_node['widgets_values']) > val[1]:
                        val = source_node['widgets_values'][val[1]]
                        break # Found the final widget value

                    # Fallback for API format (original logic)
                    if isinstance(source_inputs, dict):
                        found = False
                        for key in ['text', 'value', 'seed', 'INT', 'FLOAT', 'STRING']:
                            if key in source_inputs: 
                                val = source_inputs[key]
                                found = True
                                break
                        if not found: break
                    else: break
                except Exception: break
            else: break
        return val

    def _find_final_destination(self, start_id, connections):
        q, visited = [start_id], {start_id}
        while q:
            current_id = q.pop(0)
            for conn in connections.get(current_id, []):
                if conn['target_id'] in visited: continue
                if conn['target_input'] in ['positive', 'conditioning']: return 'positive'
                if conn['target_input'] in ['negative', 'neg_conditioning']: return 'negative'
                q.append(conn['target_id']); visited.add(conn['target_id'])
        return None
    
    def parse_json(self, workflow_json):
        try:
            if not workflow_json.strip(): return ("",) * 9 + ("Empty workflow JSON",)
            
            doc = json.loads(workflow_json)
            # Handle both UI workflow format and API format
            if 'nodes' in doc and isinstance(doc['nodes'], list):
                data = {str(node['id']): node for node in doc['nodes']}
                is_ui_format = True
            else:
                data = doc
                is_ui_format = False

            # Build connections graph correctly for both formats
            connections = {node_id: [] for node_id in data}
            if is_ui_format:
                links_list = doc.get("links", [])
                for link_info in links_list:
                    if len(link_info) < 5: continue
                    source_id, target_id, target_slot_idx = str(link_info[1]), str(link_info[3]), link_info[4]
                    target_node = data.get(target_id)
                    if not target_node: continue
                    target_inputs = target_node.get("inputs", [])
                    if isinstance(target_inputs, list) and len(target_inputs) > target_slot_idx:
                        target_input_name = target_inputs[target_slot_idx].get("name")
                        if source_id in connections and target_input_name:
                            connections[source_id].append({'target_id': target_id, 'target_input': target_input_name})
            else: # API format
                for nid, ndata in data.items():
                    node_inputs = ndata.get("inputs", {})
                    if isinstance(node_inputs, dict):
                        for iname, ival in node_inputs.items():
                            if isinstance(ival, list) and len(ival) == 2 and isinstance(ival[0], (str, int)):
                                source_node_id = str(ival[0])
                                if source_node_id in connections:
                                    connections[source_node_id].append({'target_id': nid, 'target_input': iname})
            
            p, n, m, l, s, steps, cfgs, sched, denoises, o = [], [], [], [], [], [], [], [], [], []
            for nid, ndata in data.items():
                ctype = ndata.get("class_type", ndata.get("type", "")) # Use "type" as fallback for UI format
                
                # Create a unified 'inputs' dict to simplify value retrieval
                unified_inputs = {}
                if is_ui_format:
                    # For UI format, map widget values to their names
                    widget_values = ndata.get("widgets_values", [])
                    node_inputs_list = ndata.get("inputs", [])
                    widget_idx = 0
                    if isinstance(node_inputs_list, list):
                        for item in node_inputs_list:
                            # Heuristic: if an input has a 'widget' property, it corresponds to a value in 'widgets_values'
                            if isinstance(item, dict) and 'widget' in item and widget_idx < len(widget_values):
                                unified_inputs[item.get("name")] = widget_values[widget_idx]
                                widget_idx += 1
                else: # API format
                    unified_inputs = ndata.get("inputs", {})
                
                # Fallback to widget_values for known keys if unified_inputs is insufficient
                # This helps with nodes where input names are not explicitly in the 'inputs' list
                if is_ui_format:
                     widget_values = ndata.get("widgets_values", [])
                     if "CLIPTextEncode" in ctype and "text" not in unified_inputs and len(widget_values) > 0:
                         unified_inputs["text"] = widget_values[0]

                if "CLIPTextEncode" in ctype:
                    if txt := str(self._get_real_value(unified_inputs.get("text"), data) or "").strip():
                        dest = self._find_final_destination(nid, connections)
                        if dest == 'positive': p.append(txt)
                        elif dest == 'negative': n.append(txt)
                if any(k in ctype for k in ["Loader", "Checkpoint"]):
                    for key in ["ckpt_name", "base_ckpt_name", "refiner_ckpt_name", "unet_name"]:
                         # Check both unified inputs and direct widget values for UI format
                        val_to_check = unified_inputs.get(key)
                        if is_ui_format and val_to_check is None and ndata.get("widgets_values"):
                            val_to_check = ndata["widgets_values"][0] if len(ndata["widgets_values"]) > 0 else None

                        if val := self._get_real_value(val_to_check, data):
                            if val != "None": m.append(val)

                if "CR LoRA Stack" in ctype:
                    for i in range(1, 6):
                        if self._get_real_value(unified_inputs.get(f"switch_{i}"), data) == "On":
                            if name := self._get_real_value(unified_inputs.get(f"lora_name_{i}"), data):
                                if name != "None": l.append(f"{name} (M:{self._get_real_value(unified_inputs.get(f'model_weight_{i}'), data)},C:{self._get_real_value(unified_inputs.get(f'clip_weight_{i}'), data)})")
                if any(k in ctype for k in ["Sampler", "Scheduler"]):
                    for key, lst in [("sampler_name", s), ("steps", steps), ("cfg", cfgs), ("scheduler", sched), ("denoise", denoises)]:
                        if (val := self._get_real_value(unified_inputs.get(key), data)) is not None: lst.append(str(val))
                    for key in ["seed", "noise_seed"]:
                        if (val := self._get_real_value(unified_inputs.get(key), data)) is not None: s.append(str(val))
                if "ShowText" in ctype or "ttN text" in ctype:
                    if val := self._get_real_value(unified_inputs.get("text"), data):
                        o.append(f"--- {ndata.get('_meta', {}).get('title', ndata.get('title', ctype))} ---\n{str(val).strip()}")

            details = []
            if sched: details.append(f"Scheduler(s): {', '.join(dict.fromkeys(sched))}")
            if denoises: details.append(f"Denoise(s): {', '.join(dict.fromkeys(denoises))}")
            
            # Combine seeds from sampler nodes and seed nodes
            all_seeds = [item for item in s if not isinstance(item, str) or not item.isalpha()]
            all_samplers = [item for item in s if isinstance(item, str) and item.isalpha()]

            return ("\n".join(dict.fromkeys(p)), "\n".join(dict.fromkeys(n)), "\n".join(dict.fromkeys(m)), "\n".join(dict.fromkeys(l)), ", ".join(dict.fromkeys(all_samplers)), ", ".join(dict.fromkeys(steps)), ", ".join(dict.fromkeys(cfgs)), ", ".join(dict.fromkeys(all_seeds)), ", ".join(details), "\n\n".join(dict.fromkeys(o)))
        except Exception: return ("",) * 9 + (f"CRASH! Error in node logic:\n\n{traceback.format_exc()}",)


NODE_CLASS_MAPPINGS = {"ParseJsonDetails": ParseJsonDetails}
NODE_DISPLAY_NAME_MAPPINGS = {"ParseJsonDetails": "Parse json"}

# --- END OF FILE ParseJsonDetails.py ---