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
                    if 'widgets_values' in source_node and len(source_node['widgets_values']) > val[1]:
                        val = source_node['widgets_values'][val[1]]; break
                    source_inputs = source_node.get("inputs", {})
                    found = False
                    for key in ['text', 'value', 'seed', 'INT', 'FLOAT', 'STRING']:
                        if key in source_inputs: val = source_inputs[key]; found = True; break
                    if not found: break
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
            data = json.loads(workflow_json)
            if 'nodes' in data and isinstance(data['nodes'], list): data = {str(node['id']): node for node in data['nodes']}
            
            connections = {node_id: [] for node_id in data}
            for nid, ndata in data.items():
                for iname, ival in ndata.get("inputs", {}).items():
                    if isinstance(ival, list) and len(ival) == 2 and isinstance(ival[0], (int, str)):
                        if str(ival[0]) in connections: connections[str(ival[0])].append({'target_id': nid, 'target_input': iname})
            
            p, n, m, l, s, steps, cfgs, sched, denoises, o = [], [], [], [], [], [], [], [], [], []
            for nid, ndata in data.items():
                ctype, inputs = ndata.get("class_type", ""), ndata.get("inputs", {})
                if "CLIPTextEncode" in ctype:
                    if txt := str(self._get_real_value(inputs.get("text"), data) or "").strip():
                        dest = self._find_final_destination(nid, connections)
                        if dest == 'positive': p.append(txt)
                        elif dest == 'negative': n.append(txt)
                if any(k in ctype for k in ["Loader", "Checkpoint"]):
                    for key in ["ckpt_name", "base_ckpt_name", "refiner_ckpt_name", "unet_name"]:
                        if val := self._get_real_value(inputs.get(key), data):
                            if val != "None": m.append(val)
                if "CR LoRA Stack" in ctype:
                    for i in range(1, 6):
                        if self._get_real_value(inputs.get(f"switch_{i}"), data) == "On":
                            if name := self._get_real_value(inputs.get(f"lora_name_{i}"), data):
                                if name != "None": l.append(f"{name} (M:{self._get_real_value(inputs.get(f'model_weight_{i}'), data)},C:{self._get_real_value(inputs.get(f'clip_weight_{i}'), data)})")
                if any(k in ctype for k in ["Sampler", "Scheduler"]):
                    for key, lst in [("sampler_name", s), ("steps", steps), ("cfg", cfgs), ("scheduler", sched), ("denoise", denoises)]:
                        if (val := self._get_real_value(inputs.get(key), data)) is not None: lst.append(str(val))
                    for key in ["seed", "noise_seed"]:
                        if (val := self._get_real_value(inputs.get(key), data)) is not None: s.append(str(val))
                if "ShowText" in ctype or "ttN text" in ctype:
                    if val := self._get_real_value(inputs.get("text"), data):
                        o.append(f"--- {ndata.get('_meta', {}).get('title', ctype)} ---\n{str(val).strip()}")

            details = []
            if sched: details.append(f"Scheduler(s): {', '.join(dict.fromkeys(sched))}")
            if denoises: details.append(f"Denoise(s): {', '.join(dict.fromkeys(denoises))}")
            return ("\n".join(dict.fromkeys(p)), "\n".join(dict.fromkeys(n)), "\n".join(dict.fromkeys(m)), "\n".join(dict.fromkeys(l)), ", ".join(dict.fromkeys(s)), ", ".join(dict.fromkeys(steps)), ", ".join(dict.fromkeys(cfgs)), ", ".join(dict.fromkeys(s)), ", ".join(details), "\n\n".join(dict.fromkeys(o)))
        except Exception: return ("",) * 9 + (f"CRASH! Error in node logic:\n\n{traceback.format_exc()}",)

NODE_CLASS_MAPPINGS = {"ParseJsonDetails": ParseJsonDetails}
NODE_DISPLAY_NAME_MAPPINGS = {"ParseJsonDetails": "Parse json"}