import os
import re
import sys
import json
import urllib.request
import urllib.error

class CameraSpaceDebrisInstancer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 31: camera_space_debris_instancer"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_fractures(self):
        # Fracture Engine (Agent 30) se destruction points aur intensity load karta hai
        fracture_path = os.path.join(self.workspace_dir, "30_environment_fracture_blueprint.json")
        destruction_anchors = []

        if os.path.exists(fracture_path):
            try:
                with open(fracture_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for ev in data.get("fracture_events", []):
                    destruction_anchors.append({
                        "timestamp_sec": ev.get("timestamp_sec", 0.0),
                        "epicenter": ev.get("fracture_center_xyz", [0.0, 0.0, 0.0]),
                        "chunk_count": ev.get("shatter_chunk_count", 50),
                        "radius": ev.get("fracture_radius_meters", 2.0)
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream fracture data load warning: {str(e)}")

        # Fallback agar fracture data na mile
        if not destruction_anchors:
            print(f"[{self.agent_name}] Workspace Alert: No fracture points found. Initializing default camera fly-by parameters.")
            destruction_anchors = [
                {"timestamp_sec": 4.5, "epicenter": [0.0, 1.5, -2.0], "chunk_count": 80, "radius": 3.0}
            ]

        return destruction_anchors

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

    def _save_to_workspace(self, data, filename="31_camera_space_debris_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Camera debris instances written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save debris metadata: {str(e)}")
            return None

    def design_camera_debris_instances(self):
        anchors = self._load_upstream_fractures()
        print(f"[{self.agent_name}] Debris Instancer active. Calculating camera-relative frustum depth projections...")

        system_prompt = (
            "You are an expert VFX technical director specialized in camera-frustum particle simulation and screen-space optimization in Blender.\n"
            "Your job is to generate lightweight debris particle instances that fly directly towards the active camera space to simulate intense impact proximity.\n"
            "Assume a standard camera positioned at coordinates [0.0, -5.0, 1.5] looking at the scene center.\n"
            "For each fracture anchor, design exactly 1 camera-relative debris instance sequence inside a list named 'camera_space_debris_profiles' with these parameters:\n"
            "- 'timestamp_sec': float matching the impact time.\n"
            "- 'debris_instance_type': string (choose from: 'micro_pebbles', 'coarse_dust_cloud', 'screen_crack_glass', 'shattered_concrete_chunks').\n"
            "- 'velocity_towards_camera_vector': array of 3 floats [x, y, z] pointing directly from the fracture epicenter towards the camera lens path.\n"
            "- 'debris_scale_multiplier': float (defines visual size; scale from 0.1 for subtle dust to 2.5 for massive chunks flying past the camera lens).\n"
            "- 'depth_proximity_limit_meters': float (stops rendering or fades out particles when they get too close to prevent lens clipping; default 0.15).\n"
            "- 'turbulence_noise_frequency': float (adds wild anime-style aerodynamic wobbling/turbulence to debris path; scale from 0.0 to 12.0 Hz).\n"
            "- 'motion_blur_trail_length': float (how much speed-streak the particles leave behind; range 0.05 to 0.50).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'camera_space_debris_profiles'. "
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
                    {"role": "user", "content": f"Fracture Anchor Logs:\n{json.dumps(anchors, indent=2)}"}
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
                    {"role": "user", "content": f"Fracture Anchor Logs:\n{json.dumps(anchors, indent=2)}"}
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
                    "camera_space_debris_profiles": structured_output.get("camera_space_debris_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Triggering procedural frustum particle projector.")
            return self._execute_procedural_fallback(anchors)

    def _execute_procedural_fallback(self, anchors):
        # Computes direct translation vectors from impact point straight to camera coordinate [0, -5, 1.5]
        profiles = []
        for anc in anchors:
            ts = float(anc.get("timestamp_sec", 0.0))
            epi = anc.get("epicenter", [0.0, 0.0, 0.0])
            count = int(anc.get("chunk_count", 50))

            # Direct vector pointing towards standard camera placement
            cam_pos = [0.0, -5.0, 1.5]
            dir_x = cam_pos[0] - epi[0]
            dir_y = cam_pos[1] - epi[1]
            dir_z = cam_pos[2] - epi[2]
            
            # Normalize vector to simulate constant speed force
            length = (dir_x**2 + dir_y**2 + dir_z**2)**0.5
            norm_vector = [dir_x/length * 8.5, dir_y/length * 8.5, dir_z/length * 8.5] if length > 0 else [0.0, -5.0, 1.5]

            # Assign debris parameters dynamically based on chunk counts
            if count > 80:
                dtype = "shattered_concrete_chunks"
                scale = 1.8
                turb = 6.5
                trail = 0.35
            elif count > 40:
                dtype = "micro_pebbles"
                scale = 0.6
                turb = 4.0
                trail = 0.20
            else:
                dtype = "coarse_dust_cloud"
                scale = 0.15
                turb = 10.0
                trail = 0.12

            profiles.append({
                "timestamp_sec": ts,
                "debris_instance_type": dtype,
                "velocity_towards_camera_vector": norm_vector,
                "debris_scale_multiplier": scale,
                "depth_proximity_limit_meters": 0.12,
                "turbulence_noise_frequency": turb,
                "motion_blur_trail_length": trail
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Frustum Fallback)",
            "camera_space_debris_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    instancer = CameraSpaceDebrisInstancer()
    output = instancer.design_camera_debris_instances()
    
    print("\n--- Z-NET RENDER ENGINE: AGENT 31 DEBRIS INSTANCER COMPLETE ---")
    print(f"Debris profiles successfully projected to camera space: {len(output['camera_space_debris_profiles'])}")
    for profile in output["camera_space_debris_profiles"]:
        print(f"Time: {profile['timestamp_sec']}s | Particle Type: '{profile['debris_instance_type']}' | Projectile Vector: {profile['velocity_towards_camera_vector']}")
        print(f"Proximity Limit: {profile['depth_proximity_limit_meters']}m | Turb. Freq: {profile['turbulence_noise_frequency']}Hz | Motion Streak: {profile['motion_blur_trail_length']}")
    print("----------------------------------------------------------------")
