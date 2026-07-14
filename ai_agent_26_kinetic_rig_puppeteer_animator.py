import os
import re
import sys
import json
import urllib.request
import urllib.error

class KineticRigPuppeteerAnimator:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 26: kinetic_rig_puppeteer_animator"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_data(self):
        # Character allocations aur storyboard descriptions load karta hai movements design karne ke liye
        selector_path = os.path.join(self.workspace_dir, "23_character_asset_selector_blueprint.json")
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        
        motion_demands = []

        if os.path.exists(selector_path):
            try:
                with open(selector_path, "r", encoding="utf-8") as f:
                    char_data = json.load(f)
                for alloc in char_data.get("character_allocations", []):
                    motion_demands.append({
                        "timestamp_sec": alloc.get("timestamp_sec", 0.0),
                        "character_id": alloc.get("matched_local_asset_id", "char_generic"),
                        "action_desc": alloc.get("demanded_description", "")
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Character allocation load warning: {str(e)}")

        # Storyboard fallback
        if not motion_demands and os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    sb_data = json.load(f)
                for i, panel in enumerate(sb_data.get("storyboard_panels", [])):
                    motion_demands.append({
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "character_id": "char_generic",
                        "action_desc": panel.get("visual_prompt", "")
                    })
            except Exception:
                pass

        if not motion_demands:
            print(f"[{self.agent_name}] Workspace Alert: No upstream motion triggers. Initializing default combat movements.")
            motion_demands = [
                {"timestamp_sec": 0.0, "character_id": "char_001", "action_desc": "Gojo prepares a purple energy blast stance"},
                {"timestamp_sec": 4.5, "character_id": "char_002", "action_desc": "Sasuke does a fast aerial flip downward slash"}
            ]

        return motion_demands

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

    def _save_to_workspace(self, data, filename="26_kinetic_rig_puppeteer_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Kinetic puppet keyframes saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save animation blueprint: {str(e)}")
            return None

    def design_rig_puppeteer_animation(self):
        motion_demands = self._load_upstream_data()
        print(f"[{self.agent_name}] Rig Puppeteer active. Designing skeleton joint keyframes and bone matrices...")

        system_prompt = (
            "You are a master 3D Character Animator and Blender Rigging TD specialized in high-energy kinetic combat choreography.\n"
            "Your job is to generate precise mathematical bone rotational keyframes for a standard humanoid skeleton (Hips, Spine, Head, LeftArm, RightArm, LeftLeg, RightLeg).\n"
            "For each animation cue, output exactly 1 complex animation sequence inside a list named 'rig_animation_sequences' with these properties:\n"
            "- 'timestamp_sec': float matching the action cue.\n"
            "- 'character_id': string of the targeted character mesh.\n"
            "- 'action_pose_name': string (e.g., 'charging_energy', 'aerial_backflip_slash', 'combat_ready_stance').\n"
            "- 'translation_offset': array of 3 floats [x, y, z] representing body translation (Hips root displacement).\n"
            "- 'bone_keyframe_rotations': object containing bone-specific euler angle arrays [x, y, z] in degrees:\n"
            "    - 'Hips': array of 3 floats\n"
            "    - 'Spine': array of 3 floats\n"
            "    - 'Head': array of 3 floats\n"
            "    - 'RightArm': array of 3 floats\n"
            "    - 'LeftArm': array of 3 floats\n"
            "    - 'RightLeg': array of 3 floats\n"
            "    - 'LeftLeg': array of 3 floats\n"
            "- 'keyframe_interpolation': string (choose from: 'BEZIER' for fluid movement, 'LINEAR' for robotic/rigid, 'CONSTANT' for sudden hits/stop-frames).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'rig_animation_sequences'. "
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
                    {"role": "user", "content": f"Motion Demands:\n{json.dumps(motion_demands, indent=2)}"}
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
                    {"role": "user", "content": f"Motion Demands:\n{json.dumps(motion_demands, indent=2)}"}
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
                    "rig_animation_sequences": structured_output.get("rig_animation_sequences", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Running procedural kinetic physics generator.")
            return self._execute_procedural_fallback(motion_demands)

    def _execute_procedural_fallback(self, motion_demands):
        # Standard dynamic skeletal math calculations to map text triggers directly to biomechanical angles
        sequences = []
        for demand in motion_demands:
            ts = float(demand.get("timestamp_sec", 0.0))
            cid = demand.get("character_id", "char_generic")
            desc = str(demand.get("action_desc", "")).lower()

            # Procedural pose calculations based on textual tags
            if "charge" in desc or "energy" in desc or "stance" in desc:
                pose = "energy_charge_squat"
                trans = [0.0, 0.0, -0.3] # Slightly squatted position
                rotations = {
                    "Hips": [15.0, 0.0, 0.0],
                    "Spine": [-10.0, 0.0, 0.0],
                    "Head": [20.0, 0.0, 0.0],
                    "RightArm": [-45.0, -15.0, 0.0],
                    "LeftArm": [-45.0, 15.0, 0.0],
                    "RightLeg": [30.0, 0.0, 0.0],
                    "LeftLeg": [30.0, 0.0, 0.0]
                }
                interp = "BEZIER"
            elif "flip" in desc or "slash" in desc or "air" in desc or "jump" in desc:
                pose = "aerial_combat_spin"
                trans = [0.0, 1.8, 2.5] # Jump height offset in 3D space
                rotations = {
                    "Hips": [180.0, 0.0, 0.0], # Half spin mid-air
                    "Spine": [30.0, 0.0, 0.0],
                    "Head": [-15.0, 0.0, 0.0],
                    "RightArm": [90.0, 45.0, 0.0], # Holding sword high
                    "LeftArm": [-20.0, 0.0, 0.0],
                    "RightLeg": [-15.0, 0.0, 0.0],
                    "LeftLeg": [-15.0, 0.0, 0.0]
                }
                interp = "CONSTANT" # Anime-style sharp keyframes
            else:
                pose = "combat_ready_idle"
                trans = [0.0, 0.0, 0.0]
                rotations = {
                    "Hips": [5.0, 0.0, 10.0],
                    "Spine": [-5.0, 0.0, 0.0],
                    "Head": [0.0, 0.0, -5.0],
                    "RightArm": [-20.0, 0.0, 0.0],
                    "LeftArm": [-20.0, 0.0, 0.0],
                    "RightLeg": [10.0, 0.0, 0.0],
                    "LeftLeg": [10.0, 0.0, 0.0]
                }
                interp = "SINE"

            sequences.append({
                "timestamp_sec": ts,
                "character_id": cid,
                "action_pose_name": pose,
                "translation_offset": trans,
                "bone_keyframe_rotations": rotations,
                "keyframe_interpolation": interp
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Joint Engine Fallback)",
            "rig_animation_sequences": sequences
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    animator = KineticRigPuppeteerAnimator()
    output = animator.design_rig_puppeteer_animation()
    
    print("\n--- Z-NET BLENDER ENGINE: AGENT 26 RIG PUPPETEER COMPLETE ---")
    print(f"Humanoid bone sequences generated: {len(output['rig_animation_sequences'])}")
    if output["rig_animation_sequences"]:
        sample = output["rig_animation_sequences"][0]
        print(f"Sequence Target: '{sample['action_pose_name']}' for Character '{sample['character_id']}' at {sample['timestamp_sec']}s")
        print(f"Hips Translation: {sample['translation_offset']} | Interp Mode: {sample['keyframe_interpolation']}")
        print(f"Spine Angle Rotations: {sample['bone_keyframe_rotations']['Spine']} degrees")
    print("-------------------------------------------------------------")
