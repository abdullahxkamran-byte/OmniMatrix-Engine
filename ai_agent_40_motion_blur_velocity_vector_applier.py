import os
import re
import sys
import json
import urllib.request
import urllib.error

class AiMotionBlurVelocityVectorApplier:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 40: motion_blur_velocity_vector_applier"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_kinetics(self):
        # Kinetic Puppeteer (Agent 26) aur Speed Lines (Agent 36) se velocity logs load karta hai
        kinetic_path = os.path.join(self.workspace_dir, "26_kinetic_rig_puppeteer_blueprint.json")
        speed_path = os.path.join(self.workspace_dir, "36_volumetric_speed_lines_blueprint.json")
        velocity_contexts = []

        # Pehle speed line profiles load karne ki koshish karte hain
        if os.path.exists(speed_path):
            try:
                with open(speed_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for profile in data.get("speed_line_profiles", []):
                    velocity_contexts.append({
                        "timestamp_sec": profile.get("timestamp_sec", 0.0),
                        "speed_style": profile.get("speed_line_style", "radial_zoom_in"),
                        "implied_velocity": 25.0 if "zoom" in profile.get("speed_line_style", "") else 12.0
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Speed lines blueprint read warning: {str(e)}")

        # Fallback to kinetic rig translation offsets
        if not velocity_contexts and os.path.exists(kinetic_path):
            try:
                with open(kinetic_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for seq in data.get("rig_animation_sequences", []):
                    offset = seq.get("translation_offset", [0.0, 0.0, 0.0])
                    # Calculate basic Euclidean speed
                    speed_magnitude = (offset[0]**2 + offset[1]**2 + offset[2]**2)**0.5
                    velocity_contexts.append({
                        "timestamp_sec": seq.get("timestamp_sec", 0.0),
                        "speed_style": "kinetic_displacement",
                        "implied_velocity": round(speed_magnitude, 2)
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Kinetic rig blueprint read warning: {str(e)}")

        # Absolute fallback agar koi dynamic file na mile
        if not velocity_contexts:
            print(f"[{self.agent_name}] Workspace Alert: No motion data. Injecting standard action sequence vectors.")
            velocity_contexts = [
                {"timestamp_sec": 1.2, "speed_style": "radial_zoom_in", "implied_velocity": 45.5},
                {"timestamp_sec": 3.5, "speed_style": "horizontal_streaks", "implied_velocity": 8.2}
            ]

        return velocity_contexts

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

    def _save_to_workspace(self, data, filename="40_motion_blur_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Motion blur parameters saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save blur blueprint: {str(e)}")
            return None

    def design_stylized_motion_blur(self):
        velocities = self._load_upstream_kinetics()
        print(f"[{self.agent_name}] Motion Blur Engine active. Solving vector passes and hand-drawn smear values...")

        system_prompt = (
            "You are a Senior Technical Director specialized in anime-style motion smears, vector blur compositing, and shutter angle styling.\n"
            "Your job is to translate 3D physical speed into stylized, traditional-looking motion blur commands for Blender's compositor.\n"
            "For each movement entry, generate exactly 1 configuration inside a list named 'motion_blur_profiles' with these parameters:\n"
            "- 'timestamp_sec': float matching the video timestamp.\n"
            "- 'blur_render_type': string (choose from: 'stepped_traditional_smear' for anime frame-skips, 'camera_shutter_vector' for rapid camera moves, 'background_only_haze' to keep the main character 100% sharp while blurring environment, 'none' for clean frames).\n"
            "- 'shutter_angle_degrees': float (shutter speed simulator; 0.0 for perfectly crisp, up to 360.0 for massive overlapping smears; range 45.0 to 360.0).\n"
            "- 'blur_samples': integer (defines the smoothness of the blur. For anime 'stepped' feel, keep samples extremely low (4 to 8); for smooth camera moves, raise to 16-32).\n"
            "- 'velocity_vector_multiplier': float (scale of the vector displacement blur; range 0.1 to 4.5).\n"
            "- 'smear_duplication_steps': integer (simulates cell-animation duplicates; default 0, but range 1 to 5 for fast action moves to draw duplicate offset outlines).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'motion_blur_profiles'. "
            "Do not write conversational text, markdown code blocks, or backticks. Return pure JSON only."
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
                    {"role": "user", "content": f"Velocity Logs:\n{json.dumps(velocities, indent=2)}"}
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
                    {"role": "user", "content": f"Velocity Logs:\n{json.dumps(velocities, indent=2)}"}
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
                    "motion_blur_profiles": structured_output.get("motion_blur_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Resolving procedural velocity blur fallback.")
            return self._execute_procedural_fallback(velocities)

    def _execute_procedural_fallback(self, velocities):
        # Precise mathematical fallback translating physical velocity magnitude to cartoon/anime vector styles
        profiles = []
        for v in velocities:
            ts = float(v.get("timestamp_sec", 0.0))
            style_hint = str(v.get("speed_style", "")).lower()
            velocity = float(v.get("implied_velocity", 10.0))

            if velocity > 35.0:
                # Extreme dash: traditional cell smears with duplicate outlines
                btype = "stepped_traditional_smear"
                shutter = 270.0
                samples = 6 # Low sample count creates stepped outlines, avoiding mushy gradients
                multiplier = 3.5
                smear_steps = 3
            elif "zoom" in style_hint:
                # Radial focus zooms blur the background only to protect character focus
                btype = "background_only_haze"
                shutter = 180.0
                samples = 12
                multiplier = 1.8
                smear_steps = 0
            elif velocity > 5.0:
                # Standard camera pan blur
                btype = "camera_shutter_vector"
                shutter = 90.0
                samples = 16
                multiplier = 1.0
                smear_steps = 0
            else:
                btype = "none"
                shutter = 0.0
                samples = 0
                multiplier = 0.0
                smear_steps = 0

            profiles.append({
                "timestamp_sec": ts,
                "blur_render_type": btype,
                "shutter_angle_degrees": shutter,
                "blur_samples": samples,
                "velocity_vector_multiplier": multiplier,
                "smear_duplication_steps": smear_steps
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Motion Blur Fallback)",
            "motion_blur_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    applier = AiMotionBlurVelocityVectorApplier()
    output = applier.design_stylized_motion_blur()
    
    print("\n--- Z-NET MOTION BLUR COMPOSITOR: AGENT 40 VECTOR BLUR COMPLETE ---")
    print(f"Total dynamic motion blur profiles mapped: {len(output['motion_blur_profiles'])}")
    for profile in output["motion_blur_profiles"]:
        print(f"Time: {profile['timestamp_sec']}s | Style: '{profile['blur_render_type']}'")
        print(f"  Shutter: {profile['shutter_angle_degrees']} deg | Samples: {profile['blur_samples']} steps")
        print(f"  Multiplier: {profile['velocity_vector_multiplier']}x | Smear Duplications: {profile['smear_duplication_steps']}")
    print("------------------------------------------------------------------")
