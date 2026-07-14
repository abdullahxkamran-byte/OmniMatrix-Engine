import os
import re
import sys
import json
import urllib.request
import urllib.error

class ProceduralTextMeshBuilder:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 20: procedural_text_mesh_builder"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_hook_data(self):
        # Stage 1 (Scripting) ya Stage 2 ke hook points se dynamic text read karta hai
        storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        
        text_nodes = []
        
        if os.path.exists(storyboard_path):
            try:
                with open(storyboard_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    # Extracting potential title keywords or dialogue highlights
                    raw_desc = panel.get("visual_prompt", "")
                    words = [w.strip(".,!?\"'") for w in raw_desc.split() if len(w) > 4]
                    highlight_word = words[0].upper() if words else "IMPACT"
                    
                    text_nodes.append({
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "raw_text_string": highlight_word,
                        "intensity": panel.get("camera_movement_type", "dynamic")
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Storyboard parse warning: {str(e)}")

        # Fallback dummy text triggers if no upstream storyboard exists
        if not text_nodes:
            print(f"[{self.agent_name}] Workspace Alert: Storyboard text hooks missing. Creating default 3D text nodes.")
            text_nodes = [
                {"timestamp_sec": 0.0, "raw_text_string": "WARNING", "intensity": "high"},
                {"timestamp_sec": 4.5, "raw_text_string": "UNLEASHED", "intensity": "extreme"},
                {"timestamp_sec": 8.0, "raw_text_string": "OVERLORD", "intensity": "high"}
            ]

        return text_nodes

    def _clean_json_response(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def _save_to_workspace(self, data, filename="20_procedural_text_mesh_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: 3D text mesh blueprint saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save 3D text blueprint: {str(e)}")
            return None

    def design_procedural_text_meshes(self):
        nodes = self._load_upstream_hook_data()
        print(f"[{self.agent_name}] Mesh Engine active. Formatting procedural Blender Python API variables...")

        system_prompt = (
            "You are an expert Blender technical artist and Python API script writer.\n"
            "Your task is to analyze raw text nodes and output exact 3D geometry settings "
            "compatible with bpy.ops.curve.primitive_text_add() in Blender.\n"
            "For each text node, generate exactly 1 text geometry design block inside a list named '3d_text_mesh_blueprints' with these parameters:\n"
            "- 'timestamp_sec': float matching the trigger timestamp.\n"
            "- 'text_content': string representing the actual word/sentence to spawn.\n"
            "- 'font_thickness_depth': float (scale from 0.05 to 0.45 meters based on intensity).\n"
            "- 'extrusion_depth': float (scale from 0.1 to 0.5 meters to give real 3D volume).\n"
            "- 'bevel_depth': float representing bevel smooth edges (scale from 0.01 to 0.04 meters).\n"
            "- 'geometry_resolution': integer (choose from: 12, 16, 24, 32 for vertex counts on curves).\n"
            "- 'alignment_x': string (set to 'CENTER' for layout alignment).\n"
            "- 'letter_spacing': float (scale from 0.90 to 1.35 based on typography impact style).\n"
            "- 'target_blender_collection': string (set to 'Cinematic_3D_Text_Collection').\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key '3d_text_mesh_blueprints'. "
            "No small talks, no explanations, no markdown backticks, no code blocks. Output only valid JSON."
        )

        if self.openai_api_key:
            print(f"[{self.agent_name}] Status: Querying Cloud API Node [{self.model_cloud}]")
            url = self.openai_url
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            payload = {
                "model": self.model_cloud,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Text Hook Triggers:\n{json.dumps(nodes, indent=2)}"}
                ],
                "response_format": {"type": "json_object"}
            }
        else:
            print(f"[{self.agent_name}] Status: Querying Local LLM Instance [{self.model_local}]")
            url = self.ollama_url
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": self.model_local,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Text Hook Triggers:\n{json.dumps(nodes, indent=2)}"}
                ],
                "stream": False,
                "format": "json"
            }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            
            with urllib.request.urlopen(req, timeout=50) as response:
                result = response.read().decode("utf-8")
                response_json = json.loads(result)
                
                if self.openai_api_key:
                    raw_ai_message = response_json["choices"][0]["message"]["content"]
                else:
                    raw_ai_message = response_json["message"]["content"]
                
                cleaned_message = self._clean_json_response(raw_ai_message)
                structured_output = json.loads(cleaned_message)
                
                final_output = {
                    "agent_executed": self.agent_name,
                    "3d_text_mesh_blueprints": structured_output.get("3d_text_mesh_blueprints", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Network Exception: {str(e)}. Triggering procedural fallback calculations.")
            return self._execute_procedural_fallback(nodes)

    def _execute_procedural_fallback(self, nodes):
        # Math-based fallback which translates text strings into robust geometric definitions directly
        mesh_blueprints = []
        for node in nodes:
            ts = float(node.get("timestamp_sec", 0.0))
            text = node.get("raw_text_string", "IMPACT")
            intensity = str(node.get("intensity", "high")).lower()

            # Dynamic spacing & depth adjustments
            if "extreme" in intensity or "high" in intensity:
                thickness = 0.35
                extrusion = 0.40
                bevel = 0.03
                resolution = 24
                spacing = 1.15
            else:
                thickness = 0.15
                extrusion = 0.20
                bevel = 0.015
                resolution = 12
                spacing = 1.0

            mesh_blueprints.append({
                "timestamp_sec": ts,
                "text_content": text,
                "font_thickness_depth": thickness,
                "extrusion_depth": extrusion,
                "bevel_depth": bevel,
                "geometry_resolution": resolution,
                "alignment_x": "CENTER",
                "letter_spacing": spacing,
                "target_blender_collection": "Cinematic_3D_Text_Collection"
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Geometry Fallback)",
            "3d_text_mesh_blueprints": mesh_blueprints
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    builder = ProceduralTextMeshBuilder()
    output = builder.design_procedural_text_meshes()
    
    print("\n--- Z-NET BLENDER ENGINE: AGENT 20 TEXT MESH BUILD COMPLETED ---")
    print(f"Generated procedural 3D text assets: {len(output['3d_text_mesh_blueprints'])}")
    if output["3d_text_mesh_blueprints"]:
        sample = output["3d_text_mesh_blueprints"][0]
        print(f"Asset Name: '{sample['text_content']}' | Bevel: {sample['bevel_depth']}m | Depth: {sample['font_thickness_depth']}m | Target Spot: {sample['timestamp_sec']}s")
    print("-----------------------------------------------------------------")
