import os
import sys
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

class AiDynamicSakugaFightChoreographer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 66: dynamic_sakuga_fight_choreographer"
        self.workspace_dir = workspace_dir
        self.conductor_path = os.path.join(self.workspace_dir, "65_master_conductor_timeline.json")
        self.sakuga_blueprint_path = os.path.join(self.workspace_dir, "66_sakuga_choreography_blueprint.json")

        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_conductor_directives(self):
        # Master Conductor timeline load karta hai jahan se action scenes extract honge
        if os.path.exists(self.conductor_path):
            try:
                with open(self.conductor_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("master_directives", [])
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Master conductor timeline load nahi ho saki: {str(e)}")
        
        # Action sequence fallback agar previous agent ka timeline file missing ho
        return [
            {
                "segment_id": 1,
                "duration_slice": 4.5,
                "action_choreography": "Character releases violent shockwave, ground cracking under feet, camera lens cracking visual effect.",
                "camera_rig_behavior": "shaky_handheld_track"
            }
        ]

    def choreograph_fight_sequence(self):
        print(f"[{self.agent_name}] Initializing AI Sakuga Choreographer. Parsing combat frames and kinetic trajectories...")
        directives = self._load_conductor_directives()

        system_prompt = (
            "You are an Elite Action Choreographer and Keyframe Director (famous for high-octane Sakuga fight sequences in MAPPA/Ufotable style).\n"
            "Your task is to analyze action directives and output a detailed technical breakdown of dynamic movement metrics "
            "for 3D rigging, camera shakes, impact frames, and physics deformation.\n\n"
            "Generate a JSON list named 'sakuga_sequences' containing key-value pairs for each action frame with these parameters:\n"
            "- 'target_segment_id': matching the master directive's segment ID.\n"
            "- 'pose_velocity_multiplier': float (1.0 to 5.0, defines character's physical dash/strike speed to create rapid motion curves).\n"
            "- 'impact_freeze_duration_frames': integer (0 to 12, defining hit-stop frames where the animation pauses at the exact point of impact for weight delivery).\n"
            "- 'camera_impact_shake_amplitude': float (0.0 to 4.0, defining the screen shake distortion level upon hits).\n"
            "- 'inverse_color_impact_frame': boolean (true/false, triggers a stylized black/white color inversion to highlight extreme power releases).\n"
            "- 'smear_frame_intensity': float (0.0 to 1.0, defines the mesh stretch factor to generate stylized hand-drawn movement blur).\n"
            "- 'speed_lines_density': string (choose from: 'none', 'low_radial', 'heavy_linear_horizontal', 'explosive_spherical').\n"
            "- 'physics_debris_velocity': array of 3 floats [X, Y, Z] representing the force direction of shattering stones/particles.\n\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'sakuga_sequences'. "
            "Do not write conversational introduction, notes, or markdown formatting (```json). Output raw, parseable JSON."
        )

        user_prompt = f"Target Action Segments:\n{json.dumps(directives, indent=2)}"

        if self.openai_api_key:
            print(f"[{self.agent_name}] Status: Querying Cloud Action Intelligence Node [{self.model_cloud}]")
            url = self.openai_url
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            payload = {
                "model": self.model_cloud,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "response_format": {"type": "json_object"}
            }
        else:
            print(f"[{self.agent_name}] Status: Querying Local Llama3 Sakuga Node via Ollama...")
            url = self.ollama_url
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": self.model_local,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "format": "json"
            }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            
            with urllib.request.urlopen(req, timeout=50) as response:
                result = json.loads(response.read().decode("utf-8"))
                
                if self.openai_api_key:
                    raw_content = result["choices"][0]["message"]["content"]
                else:
                    raw_content = result["message"]["content"]
                
                cleaned_content = self._clean_json(raw_content)
                structured_data = json.loads(cleaned_content)
                
                final_sakuga_blueprint = {
                    "agent_executed": self.agent_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "sakuga_sequences": structured_data.get("sakuga_sequences", [])
                }
                
                self._save_blueprint(final_sakuga_blueprint)
                return final_sakuga_blueprint

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Executing procedural Sakuga fallback...")
            return self._execute_procedural_fallback(directives)

    def _clean_json(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned

    def _execute_procedural_fallback(self, directives):
        # Offline mode mein algorithmic physical impact calculation logic
        sequences = []
        for d in directives:
            seg_id = d.get("segment_id", 1)
            action_desc = str(d.get("action_choreography", "")).upper()
            
            # Agar high kinetic activity ya explosion words detect hon
            if any(word in action_desc for word in ["SHOCKWAVE", "CRACKING", "EXPLODING", "STRIKE", "FIGHT"]):
                sequences.append({
                    "target_segment_id": seg_id,
                    "pose_velocity_multiplier": 3.8,
                    "impact_freeze_duration_frames": 8,
                    "camera_impact_shake_amplitude": 3.5,
                    "inverse_color_impact_frame": True,
                    "smear_frame_intensity": 0.85,
                    "speed_lines_density": "explosive_spherical",
                    "physics_debris_velocity": [0.0, 15.0, 5.0]
                })
            else:
                sequences.append({
                    "target_segment_id": seg_id,
                    "pose_velocity_multiplier": 1.5,
                    "impact_freeze_duration_frames": 0,
                    "camera_impact_shake_amplitude": 0.5,
                    "inverse_color_impact_frame": False,
                    "smear_frame_intensity": 0.2,
                    "speed_lines_density": "low_radial",
                    "physics_debris_velocity": [0.0, 0.0, 0.0]
                })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Sakuga Fallback)",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sakuga_sequences": sequences
        }
        self._save_blueprint(fallback_output)
        return fallback_output

    def _save_blueprint(self, data):
        try:
            with open(self.sakuga_blueprint_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Sakuga combat blueprint saved to '{self.sakuga_blueprint_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing Sakuga blueprint: {str(e)}")

if __name__ == "__main__":
    choreographer = AiDynamicSakugaFightChoreographer()
    print("--- TESTING AI SAKUGA CHOREOGRAPHER ENGINE ---")
    report = choreographer.choreograph_fight_sequence()
    print("\n--- SAKUGA ACTION TIMELINE BLUEPRINT ---")
    print(json.dumps(report, indent=4))
