import os
import re
import sys
import json
import urllib.request
import urllib.error

class MiniRealPBRFastShader:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 25: mini_real_pbr_fast_shader"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_assets_and_scene(self):
        # Local character aur storyboards check karta hai taake environmental materials match ho sakein
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        asset_path = os.path.join(self.workspace_dir, "23_character_asset_selector_blueprint.json")
        
        scene_demands = []

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for panel in data.get("storyboard_panels", []):
                    desc = panel.get("visual_prompt", "")
                    scene_demands.append({
                        "timestamp_sec": panel.get("timestamp_sec", 0.0),
                        "description": desc
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream storyboard parse warning: {str(e)}")

        if not scene_demands:
            print(f"[{self.agent_name}] Workspace Alert: Storyboard missing. Initializing default surface materials.")
            scene_demands = [
                {"timestamp_sec": 0.0, "description": "Rainy neon-lit concrete street with metal barricades"},
                {"timestamp_sec": 4.5, "description": "Metallic sword collision causing sparks in a dark brick warehouse"}
            ]

        return scene_demands

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

    def _save_to_workspace(self, data, filename="25_mini_real_pbr_fast_shader_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: PBR Fast Shader blueprints written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save shader blueprint: {str(e)}")
            return None

    def design_fast_pbr_shaders(self):
        demands = self._load_upstream_assets_and_scene()
        print(f"[{self.agent_name}] PBR Engine active. Generating low-overhead material shader networks...")

        system_prompt = (
            "You are an expert technical director specialized in lightweight real-time PBR material networks for Blender.\n"
            "Your job is to generate exact shader values compatible with Blender's Principled BSDF node to create fast, semi-realistic textures (like concrete, metals, brick, glass, or rain-slicked surfaces) without heavy rendering overhead.\n"
            "For each scene description, generate exactly 1 material design block inside a list named 'pbr_material_profiles' with these exact parameters:\n"
            "- 'timestamp_sec': float matching the scene change.\n"
            "- 'material_target_name': string (e.g., 'wet_concrete', 'brushed_steel_sword', 'rough_brick_wall').\n"
            "- 'base_color_hex': string representing base color (e.g., '#2E2E2E' for asphalt).\n"
            "- 'metallic': float (scale from 0.0 for stone/concrete to 1.0 for weapons/robots).\n"
            "- 'roughness': float (scale from 0.05 for wet reflections to 0.95 for dry dirt).\n"
            "- 'specular': float (default 0.5; range from 0.0 to 1.0).\n"
            "- 'normal_map_strength': float representing depth intensity (scale from 0.1 to 2.0).\n"
            "- 'emission_color_hex': string representing self-illuminating colors (e.g. '#000000' for none, '#00FFAA' for glowing indicators).\n"
            "- 'emission_strength': float (scale from 0.0 for standard surfaces to 15.0 for intense neon signs).\n"
            "- 'use_anisotropic_sheen': boolean (set to true ONLY for brushed metal or hair meshes to optimize shader paths, false otherwise).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'pbr_material_profiles'. "
            "Do not write explanations, markdown blocks, backticks, or talk to the user. Return valid JSON only."
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
                    {"role": "user", "content": f"Scene Demands:\n{json.dumps(demands, indent=2)}"}
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
                    {"role": "user", "content": f"Scene Demands:\n{json.dumps(demands, indent=2)}"}
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
                    "pbr_material_profiles": structured_output.get("pbr_material_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Network Exception: {str(e)}. Running mathematical fast-PBR calculations.")
            return self._execute_procedural_fallback(demands)

    def _execute_procedural_fallback(self, demands):
        # Algorithmically maps description tags to physical material equations
        profiles = []
        for d in demands:
            ts = float(d.get("timestamp_sec", 0.0))
            desc = str(d.get("description", "")).lower()

            # Dynamic surface property detection
            if "metal" in desc or "sword" in desc or "steel" in desc or "blade" in desc:
                name = "brushed_steel_weapon"
                color = "#8A8D8F"
                metallic = 1.0
                roughness = 0.22
                specular = 0.8
                normal_strength = 0.3
                emission_color = "#000000"
                emission_strength = 0.0
                aniso = True
            elif "neon" in desc or "glow" in desc or "cyber" in desc:
                name = "cyber_neon_emission"
                color = "#0C091A"
                metallic = 0.2
                roughness = 0.15
                specular = 0.6
                normal_strength = 0.5
                emission_color = "#FF00AA" # Extreme cyberpunk pink
                emission_strength = 12.0
                aniso = False
            elif "wet" in desc or "rain" in desc:
                name = "wet_asphalt_ground"
                color = "#1D2022"
                metallic = 0.0
                roughness = 0.08 # Extremely shiny reflections
                specular = 0.9
                normal_strength = 1.2
                emission_color = "#000000"
                emission_strength = 0.0
                aniso = False
            else:
                name = "generic_pbr_surface"
                color = "#5C5C5C"
                metallic = 0.0
                roughness = 0.7
                specular = 0.5
                normal_strength = 0.8
                emission_color = "#000000"
                emission_strength = 0.0
                aniso = False

            profiles.append({
                "timestamp_sec": ts,
                "material_target_name": name,
                "base_color_hex": color,
                "metallic": metallic,
                "roughness": roughness,
                "specular": specular,
                "normal_map_strength": normal_strength,
                "emission_color_hex": emission_color,
                "emission_strength": emission_strength,
                "use_anisotropic_sheen": aniso
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural PBR Fallback)",
            "pbr_material_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    baker = MiniRealPBRFastShader()
    output = baker.design_fast_pbr_shaders()
    
    print("\n--- Z-NET BLENDER ENGINE: AGENT 25 REAL PBR SHADER DESIGN COMPLETE ---")
    print(f"Engineered PBR surface profiles: {len(output['pbr_material_profiles'])}")
    if output["pbr_material_profiles"]:
        sample = output["pbr_material_profiles"][0]
        print(f"Target Surface: '{sample['material_target_name']}' at {sample['timestamp_sec']}s")
        print(f"Base Color: {sample['base_color_hex']} | Metallic: {sample['metallic']} | Roughness: {sample['roughness']}")
        print(f"Normal depth power: {sample['normal_map_strength']} | Glowing Force: {sample['emission_strength']} (Color: {sample['emission_color_hex']})")
    print("----------------------------------------------------------------------")
