import os
import re
import sys
import json
import urllib.request
import urllib.error

class AtmosphericLightingShaderBaker:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 22: atmospheric_lighting_shader_baker"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_vibe_and_story(self):
        # BGM vibe and storyboard to determine the emotional light setup
        storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        bgm_path = os.path.join(self.workspace_dir, "18_bgm_vibe_matcher_blueprint.json")
        
        narrative_moods = []
        
        # Try reading the actual musical vibe changes
        if os.path.exists(bgm_path):
            try:
                with open(bgm_path, "r", encoding="utf-8") as f:
                    bgm_data = json.load(f)
                for segment in bgm_data.get("bgm_automation_segments", []):
                    narrative_moods.append({
                        "start_sec": segment.get("start_sec", 0.0),
                        "end_sec": segment.get("end_sec", 3.0),
                        "vibe_style": segment.get("bgm_vibe_style", "neutral"),
                        "source": "bgm_vibe"
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Vibe data load warning: {str(e)}")

        # Fallback to storyboard if vibe matcher is missing
        if not narrative_moods and os.path.exists(storyboard_path):
            try:
                with open(storyboard_path, "r", encoding="utf-8") as f:
                    sb_data = json.load(f)
                for i, panel in enumerate(sb_data.get("storyboard_panels", [])):
                    narrative_moods.append({
                        "start_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "end_sec": float((i + 1) * 3.0),
                        "vibe_style": "high-energy" if "extreme" in panel.get("camera_movement_type", "") else "dark-suspense",
                        "source": "storyboard"
                    })
            except Exception:
                pass

        # Static fallback if workspace is entirely blank
        if not narrative_moods:
            print(f"[{self.agent_name}] Workspace Alert: No upstream mood data found. Generating default lighting blocks.")
            narrative_moods = [
                {"start_sec": 0.0, "end_sec": 3.5, "vibe_style": "dark-ambient-pad", "source": "fallback"},
                {"start_sec": 3.5, "end_sec": 8.0, "vibe_style": "aggressive-phonk-drill", "source": "fallback"}
            ]

        return narrative_moods

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

    def _save_to_workspace(self, data, filename="22_atmospheric_lighting_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Atmospheric lighting blueprint written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save lighting configuration: {str(e)}")
            return None

    def design_atmospheric_lighting(self):
        mood_nodes = self._load_upstream_vibe_and_story()
        print(f"[{self.agent_name}] Shader Baker active. Designing complex volumetric and key light assets...")

        system_prompt = (
            "You are a master cinematic lighting technical director and 3D shader artist for Blender (using Cycles and Eevee engines).\n"
            "Your job is to analyze video emotional segments and design exact lighting nodes, lamp structures, and world shader setups.\n"
            "For each emotional segment, generate exactly 1 lighting blueprint inside a list named 'ambient_lighting_setups' with these exact properties:\n"
            "- 'start_sec': float matching the segment start.\n"
            "- 'end_sec': float matching the segment end.\n"
            "- 'hdri_world_strength': float (ambient lighting scale from 0.0 for pitch-black void to 1.5 for outdoor skylight).\n"
            "- 'hdri_color_tint_hex': string representing the ambient tint color (e.g. '#0D051A' for deep dark purple sky).\n"
            "- 'primary_key_light': object containing:\n"
            "    - 'type': string ('SUN', 'POINT', 'SPOT', 'AREA').\n"
            "    - 'power_watts': float (scale from 100.0 to 5000.0 Watts based on intensity).\n"
            "    - 'color_hex': string representing the light color (e.g., '#FF0055' for neon pink, '#00FFFF' for cyberpunk cyan).\n"
            "    - 'coordinate_offset': array of 3 floats [x, y, z] representing placement.\n"
            "- 'fill_light_multiplier': float (ratio of back/side lighting power compared to key light, scale from 0.1 to 0.6).\n"
            "- 'volumetric_fog_density': float representing atmosphere thickness (scale from 0.0 for clean space to 0.25 for heavy dusty or smoky anime combat look).\n"
            "- 'bloom_threshold': float representing glow/glare trigger parameters (scale from 0.5 to 2.0).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'ambient_lighting_setups'. "
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
                    {"role": "user", "content": f"Vibe Timeline Segments:\n{json.dumps(mood_nodes, indent=2)}"}
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
                    {"role": "user", "content": f"Vibe Timeline Segments:\n{json.dumps(mood_nodes, indent=2)}"}
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
                    "ambient_lighting_setups": structured_output.get("ambient_lighting_setups", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Communication Exception: {str(e)}. Triggering procedural fallback shader builder.")
            return self._execute_procedural_fallback(mood_nodes)

    def _execute_procedural_fallback(self, mood_nodes):
        # Math-based procedural lighting system mapping moods to specific Kelvin/Color vectors
        setups = []
        for node in mood_nodes:
            start = float(node.get("start_sec", 0.0))
            end = float(node.get("end_sec", 3.0))
            vibe = str(node.get("vibe_style", "neutral")).lower()

            if "dark" in vibe or "suspense" in vibe:
                hdri = 0.15
                tint = "#05020B" # Dark moody blue-purple
                key_type = "SPOT"
                power = 800.0
                color = "#00FFFF" # Cyberpunk cyan spotlight
                offset = [-2.0, 3.0, 4.0]
                fill_mult = 0.2
                fog = 0.08
                bloom = 1.2
            elif "phonk" in vibe or "climax" in vibe or "high" in vibe:
                hdri = 0.0 # Extreme high-contrast black backdrop
                tint = "#000000"
                key_type = "AREA"
                power = 3500.0
                color = "#FF003C" # Violent hot magenta pink
                offset = [3.0, -2.0, 5.0]
                fill_mult = 0.45
                fog = 0.18 # Heavy volumetric dust shafts
                bloom = 0.6 # High bloom sensitivity
            else:
                hdri = 0.8
                tint = "#FFFFFF"
                key_type = "SUN"
                power = 1000.0
                color = "#FFF4E0" # Normal warm sunlight
                offset = [0.0, 0.0, 10.0]
                fill_mult = 0.5
                fog = 0.02
                bloom = 1.5

            setups.append({
                "start_sec": start,
                "end_sec": end,
                "hdri_world_strength": hdri,
                "hdri_color_tint_hex": tint,
                "primary_key_light": {
                    "type": key_type,
                    "power_watts": power,
                    "color_hex": color,
                    "coordinate_offset": offset
                },
                "fill_light_multiplier": fill_mult,
                "volumetric_fog_density": fog,
                "bloom_threshold": bloom
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Light Fallback)",
            "ambient_lighting_setups": setups
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    baker = AtmosphericLightingShaderBaker()
    output = baker.design_atmospheric_lighting()
    
    print("\n--- Z-NET BLENDER ENGINE: AGENT 22 SHADER BAKE COMPLETED ---")
    print(f"Atmospheric lighting setups engineered: {len(output['ambient_lighting_setups'])}")
    if output["ambient_lighting_setups"]:
        sample = output["ambient_lighting_setups"][0]
        pk = sample["primary_key_light"]
        print(f"First Rig: {sample['start_sec']}s -> {sample['end_sec']}s | Key Type: {pk['type']} ({pk['power_watts']}W, Color: {pk['color_hex']}) | Fog: {sample['volumetric_fog_density']}")
    print("-------------------------------------------------------------")
