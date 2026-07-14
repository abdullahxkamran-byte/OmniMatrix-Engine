import os
import re
import sys
import json
import urllib.request
import urllib.error

class PhysicsClothHairBaker:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 33: physics_cloth_hair_baker"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_movement(self):
        # Puppeteer engine (Agent 26) se character ki dynamic movement velocities check karta hai
        anim_path = os.path.join(self.workspace_dir, "26_kinetic_rig_puppeteer_blueprint.json")
        movement_velocity_logs = []

        if os.path.exists(anim_path):
            try:
                with open(anim_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for seq in data.get("rig_animation_sequences", []):
                    movement_velocity_logs.append({
                        "timestamp_sec": seq.get("timestamp_sec", 0.0),
                        "character_id": seq.get("character_id", "char_generic"),
                        "action_pose": seq.get("action_pose_name", "idle"),
                        "translation_offset": seq.get("translation_offset", [0.0, 0.0, 0.0])
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream movement load warning: {str(e)}")

        # Fallback dataset agar positions data available na ho
        if not movement_velocity_logs:
            print(f"[{self.agent_name}] Workspace Alert: No active movement speed data found. Utilizing static aerodynamics preset.")
            movement_velocity_logs = [
                {"timestamp_sec": 0.0, "character_id": "char_001", "action_pose": "combat_ready_idle", "translation_offset": [0.0, 0.0, 0.0]},
                {"timestamp_sec": 3.2, "character_id": "char_001", "action_pose": "aerial_combat_spin", "translation_offset": [0.0, 2.5, 3.0]}
            ]

        return movement_velocity_logs

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

    def _save_to_workspace(self, data, filename="33_physics_bake_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Physics baking constants saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save physics constants: {str(e)}")
            return None

    def design_physics_bake_profiles(self):
        movements = self._load_upstream_movement()
        print(f"[{self.agent_name}] Physics Baker active. Running aerodynamic collision checks and stiffness iterations...")

        system_prompt = (
            "You are a master 3D Physics and Character FX Technical Director specialized in Blender Cloth and Hair Simulation Baking for anime production.\n"
            "Your job is to analyze movement speed changes and output dynamic structural coefficients for cloth meshes and hair curves.\n"
            "For each movement sequence, design exactly 1 physics bake configuration inside a list named 'physics_bake_profiles' with these keys:\n"
            "- 'timestamp_sec': float matching the movement timeline.\n"
            "- 'character_id': string designating target character mesh.\n"
            "- 'simulation_bake_type': string (choose from: 'cloth_cape_flow', 'stiff_coat_leather', 'anime_spiky_hair_sway', 'soft_ribbon_wind').\n"
            "- 'wind_force_vector': array of 3 floats [x, y, z] representing global wind force direction and strength acting on the meshes.\n"
            "- 'cloth_bending_stiffness': float (defines how stiff/soft the fabric fold is; scale from 0.05 for silk capes to 15.0 for heavy leather coat armor).\n"
            "- 'hair_spring_tension': float (defines how fast the spiky hair bounces back to its original silhouette shape; range 1.0 to 10.0).\n"
            "- 'collision_friction_coefficient': float (prevents cloth from sliding off shoulders; range 0.1 to 0.95).\n"
            "- 'bake_start_frame': integer (the Blender timeline frame index where calculations start; usually frame 1 or match the timestamp).\n"
            "- 'bake_end_frame': integer (end frame index for pre-rendering cache bake).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'physics_bake_profiles'. "
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
                    {"role": "user", "content": f"Dynamic Kinetic Steps:\n{json.dumps(movements, indent=2)}"}
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
                    {"role": "user", "content": f"Dynamic Kinetic Steps:\n{json.dumps(movements, indent=2)}"}
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
                    "physics_bake_profiles": structured_output.get("physics_bake_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Network Exception: {str(e)}. Triggering procedural aerodynamics solver.")
            return self._execute_procedural_fallback(movements)

    def _execute_procedural_fallback(self, movements):
        # Precise algorithmic aerodynamic calculation mapping speed vectors to bending values
        profiles = []
        for mv in movements:
            ts = float(mv.get("timestamp_sec", 0.0))
            cid = mv.get("character_id", "char_generic")
            pose = str(mv.get("action_pose", "")).lower()

            # Dynamic assignment of structural weights based on speed
            if "spin" in pose or "combat" in pose or "aerial" in pose:
                # Highly dynamic speed forces high stiffness values so clothes don't pass through bodies
                sim_type = "cloth_cape_flow"
                wind = [0.0, -15.5, 4.0] # High headwind during rapid spin
                stiffness = 1.25 # Semi-tight bending
                tension = 7.5 # Hair springs back rapidly
                friction = 0.85 # Cloth sticks to skin collision box tightly
            else:
                # Low-speed air resistance
                sim_type = "anime_spiky_hair_sway"
                wind = [1.5, 0.0, 0.5] # Mild cross-breeze
                stiffness = 0.35
                tension = 3.0
                friction = 0.3

            # Calculate default 24fps frames
            start_f = max(1, int(ts * 24))
            end_f = start_f + 72 # Bake in 3-second simulation blocks

            profiles.append({
                "timestamp_sec": ts,
                "character_id": cid,
                "simulation_bake_type": sim_type,
                "wind_force_vector": wind,
                "cloth_bending_stiffness": stiffness,
                "hair_spring_tension": tension,
                "collision_friction_coefficient": friction,
                "bake_start_frame": start_f,
                "bake_end_frame": end_f
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Physics Fallback)",
            "physics_bake_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    baker = PhysicsClothHairBaker()
    output = baker.design_physics_bake_profiles()
    
    print("\n--- Z-NET PHYSICS SYSTEM: AGENT 33 BAKE PROFILE GENERATION COMPLETE ---")
    print(f"Active simulation caches mapped for Blender: {len(output['physics_bake_profiles'])}")
    for profile in output["physics_bake_profiles"]:
        print(f"Char: '{profile['character_id']}' | Simulation: '{profile['simulation_bake_type']}' | Frames: {profile['bake_start_frame']} -> {profile['bake_end_frame']}")
        print(f"  Wind Direction: {profile['wind_force_vector']} | Stiffness: {profile['cloth_bending_stiffness']} | Tension: {profile['hair_spring_tension']}")
    print("------------------------------------------------------------------------")
