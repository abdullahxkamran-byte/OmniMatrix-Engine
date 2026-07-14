import os
import re
import sys
import json
import urllib.request
import urllib.error

class Procedural3DEnvironmentArchitect:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 34: procedural_3d_environment_architect"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_storyboard(self):
        # Storyboard (Agent 03) se shot environment details aur visual descriptions fetch karta hai
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        env_demands = []

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    env_demands.append({
                        "panel_index": i,
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "visual_description": panel.get("visual_prompt", "battleground"),
                        "mood": panel.get("emotional_tone", "EPIC")
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream storyboard read warning: {str(e)}")

        # Fallback preset agar storyboard details na milain
        if not env_demands:
            print(f"[{self.agent_name}] Workspace Alert: No storyboard environments found. Designing a default showdown battleground.")
            env_demands = [
                {
                    "panel_index": 0,
                    "timestamp_sec": 0.0,
                    "visual_description": "Desolate rocky wasteland under a dark red crimson sky, heavy dust",
                    "mood": "EPIC_CRITICAL"
                }
            ]

        return env_demands

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

    def _save_to_workspace(self, data, filename="34_procedural_environment_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Procedural environment architecture saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save environment layout: {str(e)}")
            return None

    def construct_procedural_environment(self):
        demands = self._load_upstream_storyboard()
        print(f"[{self.agent_name}] Architect Engine active. Generating procedural scattering seeds, lighting, and atmospherics...")

        system_prompt = (
            "You are a legendary 3D Environment Technical Artist specialized in procedural scene-building and stylized anime lighting in Blender.\n"
            "Your job is to translate textual environment demands into coordinate grids, lighting profiles, and atmospheric values.\n"
            "Generate exactly 1 environment setup configuration inside a list named 'environment_layouts' with these specific parameters:\n"
            "- 'environment_preset': string (choose from: 'neo_tokyo_cyberpunk', 'grassy_shonen_plains', 'apocalyptic_ruins', 'crimson_void_space').\n"
            "- 'sun_intensity_lux': float (light power scale; from 2.5 for moody nights to 25.0 for bright blinding showdowns).\n"
            "- 'color_temperature_k': float (sky color temperature; 3200 for warm sunset, 5500 for daylight, 9000 for eerie cold nights).\n"
            "- 'volumetric_fog_density': float (density coefficient for realistic light rays; scale from 0.0 to 0.45).\n"
            "- 'scatter_asset_seed': integer (randomized math seed for procedural grass, rocks, and debris scattering arrays).\n"
            "- 'procedural_prop_count': integer (defines how many debris structures, trees, or light-poles spawn automatically on the set; range 20 to 150).\n"
            "- 'ground_subdivision_level': integer (Blender ground displacement subdivisions for organic craters; choose from 3, 4, 5, or 6).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'environment_layouts'. "
            "Do not write conversational descriptions, markdown code blocks, or backticks. Return valid JSON only."
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
                    {"role": "user", "content": f"Environmental Demands:\n{json.dumps(demands, indent=2)}"}
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
                    {"role": "user", "content": f"Environmental Demands:\n{json.dumps(demands, indent=2)}"}
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
                    "environment_layouts": structured_output.get("environment_layouts", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Launching procedural fallback generator.")
            return self._execute_procedural_fallback(demands)

    def _execute_procedural_fallback(self, demands):
        # Precise algorithmic fallback matching keyword concepts to concrete atmospheric environments
        layouts = []
        for d in demands:
            desc = str(d.get("visual_description", "")).lower()
            mood = str(d.get("mood", "")).upper()

            # Smart string checks to configure world lighting and scatter matrices
            if "wasteland" in desc or "ruins" in desc or "apocalyptic" in desc:
                preset = "apocalyptic_ruins"
                lux = 4.0
                temp = 4500.0 # Warm, dusty smog
                fog = 0.28 # High dust particles
                seed = 7392
                props = 120 # Heavy ruin boulders
                subdiv = 5
            elif "cyberpunk" in desc or "tokyo" in desc or "night" in desc:
                preset = "neo_tokyo_cyberpunk"
                lux = 12.0 # Bright neon lights
                temp = 9500.0 # Cool cyber night
                fog = 0.12 # Rain mist
                seed = 4821
                props = 80 # Power-grids, neon signs
                subdiv = 3
            else:
                # Default beautiful anime grassy showdown plains (reminiscent of standard shonen battlefields)
                preset = "grassy_shonen_plains"
                lux = 18.0
                temp = 5800.0 # Soft golden hour sun
                fog = 0.05
                seed = 1054
                props = 45 # Shrubbery, trees, and grass clumps
                subdiv = 4

            layouts.append({
                "timestamp_sec": float(d.get("timestamp_sec", 0.0)),
                "environment_preset": preset,
                "sun_intensity_lux": lux,
                "color_temperature_k": temp,
                "volumetric_fog_density": fog,
                "scatter_asset_seed": seed,
                "procedural_prop_count": props,
                "ground_subdivision_level": subdiv
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Environment Fallback)",
            "environment_layouts": layouts
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    architect = Procedural3DEnvironmentArchitect()
    output = architect.construct_procedural_environment()
    
    print("\n--- Z-NET STAGE DESIGN: AGENT 34 ENVIRONMENT BUILDER COMPLETE ---")
    print(f"Total procedural environments constructed: {len(output['environment_layouts'])}")
    for layout in output["environment_layouts"]:
        print(f"Active Theme: '{layout['environment_preset']}' | Sun Power: {layout['sun_intensity_lux']} Lux | Temp: {layout['color_temperature_k']}K")
        print(f"  Volumetric Fog: {layout['volumetric_fog_density']} | Scatter Seed: {layout['scatter_asset_seed']} | Total Props: {layout['procedural_prop_count']}")
    print("------------------------------------------------------------------")
