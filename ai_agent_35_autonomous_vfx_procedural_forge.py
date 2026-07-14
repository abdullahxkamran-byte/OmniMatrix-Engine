import os
import re
import sys
import json
import urllib.request
import urllib.error

class AutonomousVFXProceduralForge:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 35: autonomous_vfx_procedural_forge"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_destruction(self):
        # Fracture Engine (Agent 30) se high-energy impact epicenters load karta hai
        fracture_path = os.path.join(self.workspace_dir, "30_environment_fracture_blueprint.json")
        energy_hotspots = []

        if os.path.exists(fracture_path):
            try:
                with open(fracture_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for ev in data.get("fracture_events", []):
                    energy_hotspots.append({
                        "timestamp_sec": ev.get("timestamp_sec", 0.0),
                        "vfx_origin_xyz": ev.get("fracture_center_xyz", [0.0, 0.0, 0.0]),
                        "impact_scale": ev.get("fracture_radius_meters", 1.0)
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream fracture load warning: {str(e)}")

        # Fallback agar koi fracture event na mile
        if not energy_hotspots:
            print(f"[{self.agent_name}] Workspace Alert: No destruction hotspots found. Injecting custom charging energy aura.")
            energy_hotspots = [
                {"timestamp_sec": 1.5, "vfx_origin_xyz": [0.0, 1.2, 0.0], "impact_scale": 2.5}
            ]

        return energy_hotspots

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

    def _save_to_workspace(self, data, filename="35_procedural_vfx_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Procedural VFX parameters saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save VFX blueprint: {str(e)}")
            return None

    def forge_procedural_vfx(self):
        hotspots = self._load_upstream_destruction()
        print(f"[{self.agent_name}] VFX Forge online. Generating lightning meshes and energy shader parameters...")

        system_prompt = (
            "You are an expert VFX technical director specialized in procedural anime shader networks and lightning generator nodes in Blender.\n"
            "Your job is to design procedurally generated magical/sci-fi effects that spawn around high-energy impact coordinates.\n"
            "For each energy hotspot, design exactly 1 procedural VFX block inside a list named 'vfx_procedural_profiles' with these parameters:\n"
            "- 'timestamp_sec': float matching the action sequence.\n"
            "- 'vfx_type': string (choose from: 'lightning_arcs', 'energy_aura_glow', 'magic_circle_grid', 'plasma_sparks').\n"
            "- 'vfx_origin_xyz': array of 3 floats indicating the world coordinates of the effect.\n"
            "- 'glow_intensity_emission': float (defines shader emission strength; scale from 10.0 for dim aura to 150.0 for screen-blinding energy blast).\n"
            "- 'noise_distortion_scale': float (erratic distortion multiplier for procedural noise textures; range 0.5 to 15.0).\n"
            "- 'color_rgb': array of 3 floats representing the color channel intensities [R, G, B] (scale from 0.0 to 1.0; use high values for anime stylization like [0.0, 0.8, 1.0] for cyan electric arcs).\n"
            "- 'particle_spawn_rate': integer (density of glowing sparks orbiting the effect origin; range 0 to 500).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'vfx_procedural_profiles'. "
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
                    {"role": "user", "content": f"Energy Hotspots Data:\n{json.dumps(hotspots, indent=2)}"}
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
                    {"role": "user", "content": f"Energy Hotspots Data:\n{json.dumps(hotspots, indent=2)}"}
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
                    "vfx_procedural_profiles": structured_output.get("vfx_procedural_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Network Exception: {str(e)}. Switching to procedural fallback generator.")
            return self._execute_procedural_fallback(hotspots)

    def _execute_procedural_fallback(self, hotspots):
        # Precise algorithmic fallback mapping impact ranges directly to electric aura and shader parameters
        profiles = []
        for hs in hotspots:
            ts = float(hs.get("timestamp_sec", 0.0))
            origin = hs.get("vfx_origin_xyz", [0.0, 0.0, 0.0])
            scale = float(hs.get("impact_scale", 1.0))

            # Dynamically compute epic aura configurations based on collision scales
            if scale > 2.0:
                v_type = "lightning_arcs"
                glow = 120.0 # Extreme power emission
                noise = 8.5 # Erratic lightning shape
                color = [0.1, 0.6, 1.0] # Electric blue
                sparks = 400
            elif scale > 1.0:
                v_type = "energy_aura_glow"
                glow = 65.0
                noise = 4.0
                color = [0.9, 0.1, 0.1] # Dark blood crimson aura
                sparks = 180
            else:
                v_type = "plasma_sparks"
                glow = 25.0
                noise = 1.2
                color = [1.0, 0.8, 0.0] # Golden spark flares
                sparks = 75

            profiles.append({
                "timestamp_sec": ts,
                "vfx_type": v_type,
                "vfx_origin_xyz": origin,
                "glow_intensity_emission": glow,
                "noise_distortion_scale": noise,
                "color_rgb": color,
                "particle_spawn_rate": sparks
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Shader Fallback)",
            "vfx_procedural_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    forge = AutonomousVFXProceduralForge()
    output = forge.forge_procedural_vfx()
    
    print("\n--- Z-NET VFX STUDIO: AGENT 35 PROCEDURAL FORGE COMPLETE ---")
    print(f"Total procedural VFX instances mapped: {len(output['vfx_procedural_profiles'])}")
    for p in output["vfx_procedural_profiles"]:
        print(f"Time: {p['timestamp_sec']}s | Type: '{p['vfx_type']}' | Origin: {p['vfx_origin_xyz']}")
        print(f"  Emission: {p['glow_intensity_emission']} | Noise Scale: {p['noise_distortion_scale']} | RGB: {p['color_rgb']} | Sparks: {p['particle_spawn_rate']}")
    print("------------------------------------------------------------")
