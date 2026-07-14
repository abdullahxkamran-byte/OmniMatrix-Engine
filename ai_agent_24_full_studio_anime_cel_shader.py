import os
import re
import sys
import json
import urllib.request
import urllib.error

class FullStudioAnimeCelShader:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 24: full_studio_anime_cel_shader"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_data(self):
        # Character selection aur lighting data ko load karta hai taake cel-shading adapt ho sake
        character_path = os.path.join(self.workspace_dir, "23_character_asset_selector_blueprint.json")
        lighting_path = os.path.join(self.workspace_dir, "22_atmospheric_lighting_blueprint.json")
        
        compiled_meta = {
            "characters_detected": [],
            "lighting_styles": []
        }

        # 1. Load Selected Characters
        if os.path.exists(character_path):
            try:
                with open(character_path, "r", encoding="utf-8") as f:
                    char_data = json.load(f)
                for alloc in char_data.get("character_allocations", []):
                    compiled_meta["characters_detected"].append({
                        "timestamp_sec": alloc.get("timestamp_sec"),
                        "demanded_description": alloc.get("demanded_description", "")
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Character allocation load warning: {str(e)}")

        # 2. Load Lighting Environments
        if os.path.exists(lighting_path):
            try:
                with open(lighting_path, "r", encoding="utf-8") as f:
                    light_data = json.load(f)
                for setup in light_data.get("ambient_lighting_setups", []):
                    pk = setup.get("primary_key_light", {})
                    compiled_meta["lighting_styles"].append({
                        "start_sec": setup.get("start_sec"),
                        "end_sec": setup.get("end_sec"),
                        "key_color": pk.get("color_hex", "#FFFFFF"),
                        "fog_density": setup.get("volumetric_fog_density", 0.0)
                    })
            except Exception:
                pass

        # Fallbacks if files do not exist yet
        if not compiled_meta["characters_detected"]:
            print(f"[{self.agent_name}] Workspace Alert: Upstream maps missing. Instantiating default visual sync targets.")
            compiled_meta["characters_detected"] = [
                {"timestamp_sec": 0.0, "demanded_description": "Gojo Satoru close-up action pose"}
            ]
        if not compiled_meta["lighting_styles"]:
            compiled_meta["lighting_styles"] = [
                {"start_sec": 0.0, "end_sec": 5.0, "key_color": "#FF0055", "fog_density": 0.1}
            ]

        return compiled_meta

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

    def _save_to_workspace(self, data, filename="24_anime_cel_shader_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Cel-Shader parameters saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save shader blueprint: {str(e)}")
            return None

    def design_anime_cel_shader(self):
        compiled_meta = self._load_upstream_data()
        print(f"[{self.agent_name}] Cel-Shading Engine active. Generating sharp shadow maps and ink outline nodes...")

        system_prompt = (
            "You are a legendary 3D non-photorealistic rendering (NPR) TD specialized in anime cel-shading (Guilty Gear / Arcane / Kyoto Animation style).\n"
            "Your job is to analyze character/lighting structures and output exact parameters for Blender's Shader Nodes "
            "(Shader-to-RGB, ColorRamp, and Line Art Grease Pencil modifiers).\n"
            "For each character segment, design exactly 1 shader configuration block inside a list named 'cel_shader_profiles' with these keys:\n"
            "- 'timestamp_sec': float matching the trigger segment.\n"
            "- 'outline_thickness_pixels': float (scale from 1.0 for delicate shojo to 4.5 for heavy aggressive action lines).\n"
            "- 'outline_color_hex': string representing the ink outline (usually '#000000', or '#210B0B' for warm blended styles).\n"
            "- 'color_ramp_stops': array of floats (usually 2 or 3 stops between 0.0 and 1.0 to clamp diffuse into sharp shadow zones, e.g., [0.45, 0.48]).\n"
            "- 'shadow_tint_multiplier': float representing shadow color warmth (scale from 0.6 to 0.9; lower values darken shadows drastically).\n"
            "- 'specular_glossiness_cutoff': float representing anime hair glossy sheen cutoffs (scale from 0.05 to 0.3).\n"
            "- 'rim_light_intensity': float (scale from 0.0 to 5.0; higher values pop characters out of dark background plates).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'cel_shader_profiles'. "
            "Do not output markdown code blocks, backticks, or any conversational text. Return valid JSON only."
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
                    {"role": "user", "content": f"Scene Meta & Lights:\n{json.dumps(compiled_meta, indent=2)}"}
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
                    {"role": "user", "content": f"Scene Meta & Lights:\n{json.dumps(compiled_meta, indent=2)}"}
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
                    "cel_shader_profiles": structured_output.get("cel_shader_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Network Exception: {str(e)}. Running procedural cel-shading math engine.")
            return self._execute_procedural_fallback(compiled_meta)

    def _execute_procedural_fallback(self, compiled_meta):
        # Generates industry standard 2D cel-shaded vectors algorithmically
        profiles = []
        for char in compiled_meta["characters_detected"]:
            ts = float(char.get("timestamp_sec", 0.0))
            desc = char.get("demanded_description", "").lower()

            # Dynamic adjustments based on description intensity
            if "action" in desc or "fight" in desc or "combat" in desc:
                thickness = 3.0
                outline_color = "#0A0202" # Dark blood-rust outline
                stops = [0.35, 0.38] # Extremely sharp high-contrast shadow line
                shadow_mult = 0.65
                specular = 0.1
                rim = 4.0 # High pop rim light for action depth
            else:
                thickness = 1.8
                outline_color = "#111111"
                stops = [0.48, 0.50]
                shadow_mult = 0.8
                specular = 0.2
                rim = 1.5

            profiles.append({
                "timestamp_sec": ts,
                "outline_thickness_pixels": thickness,
                "outline_color_hex": outline_color,
                "color_ramp_stops": stops,
                "shadow_tint_multiplier": shadow_mult,
                "specular_glossiness_cutoff": specular,
                "rim_light_intensity": rim
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural NPR Fallback)",
            "cel_shader_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    shader = FullStudioAnimeCelShader()
    output = shader.design_anime_cel_shader()
    
    print("\n--- Z-NET BLENDER ENGINE: AGENT 24 NPR CEL-SHADER BAKE COMPLETE ---")
    print(f"Generated cel-shading profiles: {len(output['cel_shader_profiles'])}")
    if output["cel_shader_profiles"]:
        sample = output["cel_shader_profiles"][0]
        print(f"Target Time: {sample['timestamp_sec']}s | Ink Outline: {sample['outline_thickness_pixels']}px (Hex: {sample['outline_color_hex']})")
        print(f"ColorRamp Shading Stops: {sample['color_ramp_stops']} | Rim pop intensity: {sample['rim_light_intensity']}")
    print("-------------------------------------------------------------------")
