import os
import re
import sys
import json
import urllib.request
import urllib.error

class StylizedSmokeFireFluidForge:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 37: stylized_smoke_fire_fluid_forge"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_vfx(self):
        # VFX Forge (Agent 35) se core energy positions aur timestamps load karta hai
        vfx_path = os.path.join(self.workspace_dir, "35_procedural_vfx_blueprint.json")
        fluid_emitters = []

        if os.path.exists(vfx_path):
            try:
                with open(vfx_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for profile in data.get("vfx_procedural_profiles", []):
                    fluid_emitters.append({
                        "timestamp_sec": profile.get("timestamp_sec", 0.0),
                        "origin_xyz": profile.get("vfx_origin_xyz", [0.0, 0.0, 0.0]),
                        "base_intensity": profile.get("glow_intensity_emission", 50.0)
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream VFX data load warning: {str(e)}")

        # Fallback agar koi data na mile
        if not fluid_emitters:
            print(f"[{self.agent_name}] Workspace Alert: No active VFX targets found. Deploying default stylized fireball.")
            fluid_emitters = [
                {"timestamp_sec": 2.1, "origin_xyz": [0.0, 2.0, -1.0], "base_intensity": 100.0}
            ]

        return fluid_emitters

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

    def _save_to_workspace(self, data, filename="37_stylized_fluid_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Stylized fluid constraints saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save fluid metadata: {str(e)}")
            return None

    def forge_stylized_fluid_parameters(self):
        emitters = self._load_upstream_vfx()
        print(f"[{self.agent_name}] Fluid Forge active. Resolving stylized mesh boundaries and ramp shaders...")

        system_prompt = (
            "You are an elite Anime FX Animator and fluid simulation pipeline director. "
            "Your job is to generate physical parameters for high-velocity stylized smoke, fire, and water animations in Blender.\n"
            "For each dynamic emitter hotspot, design exactly 1 fluid configuration inside a list named 'fluid_simulation_profiles' with these parameters:\n"
            "- 'timestamp_sec': float matching the simulation cue.\n"
            "- 'simulation_domain_type': string (choose from: 'bubbly_impact_smoke', 'cel_shaded_fireblast', 'ink_splash_fluid').\n"
            "- 'dissipation_rate_frames': integer (how fast the smoke or fire vanishes from the screen; range 15 to 120 frames).\n"
            "- 'buoyancy_density_force': float (defines how fast hot air/smoke rises; range -2.0 for heavy gas to 5.0 for light blazing flames).\n"
            "- 'cel_shader_border_threshold': float (controls the hard border ramp line for stylized shading; range 0.05 to 0.75).\n"
            "- 'vorticity_swirl_strength': float (adds dynamic anime swirls and circular aerodynamic curls; range 0.0 to 4.5).\n"
            "- 'fluid_viscosity_multiplier': float (used for ink/water effects, defines stickiness; default 1.0).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'fluid_simulation_profiles'. "
            "Do not write conversational explanations, markdown code blocks, or backticks. Return valid JSON only."
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
                    {"role": "user", "content": f"VFX Hotspot Cues:\n{json.dumps(emitters, indent=2)}"}
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
                    {"role": "user", "content": f"VFX Hotspot Cues:\n{json.dumps(emitters, indent=2)}"}
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
                    "fluid_simulation_profiles": structured_output.get("fluid_simulation_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Directing procedural fluid solver.")
            return self._execute_procedural_fallback(emitters)

    def _execute_procedural_fallback(self, emitters):
        # Precise algorithmic mapping translating core VFX glow to dense smoke and fire parameters
        profiles = []
        for em in emitters:
            ts = float(em.get("timestamp_sec", 0.0))
            intensity = float(em.get("base_intensity", 50.0))

            if intensity > 80.0:
                # Highly energetic impact triggers custom cel-shaded fire
                dtype = "cel_shaded_fireblast"
                dissipation = 35 # Fire vanishes quickly
                buoyancy = 3.8 # Heat rises rapidly
                threshold = 0.55 # Sharp shader transitions
                vorticity = 2.8
                viscosity = 1.0
            elif intensity > 30.0:
                # Standard physical blast results in heavy shockwave smoke
                dtype = "bubbly_impact_smoke"
                dissipation = 85 # Smoke lingers around on set
                buoyancy = -0.5 # Heavy dense dust hangs low
                threshold = 0.15
                vorticity = 4.2 # Spiraling swirls
                viscosity = 1.0
            else:
                # Magical splashes or dark ink movements
                dtype = "ink_splash_fluid"
                dissipation = 45
                buoyancy = 0.2
                threshold = 0.70 # Extremely crisp liquid lines
                vorticity = 0.5
                viscosity = 4.5 # Thick dark ink feel

            profiles.append({
                "timestamp_sec": ts,
                "simulation_domain_type": dtype,
                "dissipation_rate_frames": dissipation,
                "buoyancy_density_force": buoyancy,
                "cel_shader_border_threshold": threshold,
                "vorticity_swirl_strength": vorticity,
                "fluid_viscosity_multiplier": viscosity
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Fluid Fallback)",
            "fluid_simulation_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    forge = StylizedSmokeFireFluidForge()
    output = forge.forge_stylized_fluid_parameters()
    
    print("\n--- Z-NET FLUID STUDIO: AGENT 37 STYLIZED FLUID FORGE COMPLETE ---")
    print(f"Total anime-style simulation layers generated: {len(output['fluid_simulation_profiles'])}")
    for profile in output["fluid_simulation_profiles"]:
        print(f"Time: {profile['timestamp_sec']}s | Preset: '{profile['simulation_domain_type']}'")
        print(f"  Bake Dissipation: {profile['dissipation_rate_frames']} frames | Buoyancy Force: {profile['buoyancy_density_force']}")
        print(f"  Cel-Shader Threshold: {profile['cel_shader_border_threshold']} | Swirl Vorticity: {profile['vorticity_swirl_strength']} | Viscosity: {profile['fluid_viscosity_multiplier']}")
    print("------------------------------------------------------------------")
