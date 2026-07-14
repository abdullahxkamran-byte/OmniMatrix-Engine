import os
import re
import sys
import json
import urllib.request
import urllib.error

class VolumetricSpeedLinesArchitect:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 36: volumetric_speed_lines_architect"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_velocities(self):
        # Puppeteer (Agent 26) se character ki speed aur motion displacement load karta hai
        anim_path = os.path.join(self.workspace_dir, "26_kinetic_rig_puppeteer_blueprint.json")
        kinetic_records = []

        if os.path.exists(anim_path):
            try:
                with open(anim_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for seq in data.get("rig_animation_sequences", []):
                    kinetic_records.append({
                        "timestamp_sec": seq.get("timestamp_sec", 0.0),
                        "pose_name": seq.get("action_pose_name", "idle"),
                        "offset": seq.get("translation_offset", [0.0, 0.0, 0.0])
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream kinetic load warning: {str(e)}")

        # Fallback agar velocity patterns missing hon
        if not kinetic_records:
            print(f"[{self.agent_name}] Workspace Alert: No dynamic speed files found. Generating standard dash parameters.")
            kinetic_records = [
                {"timestamp_sec": 1.2, "pose_name": "ground_dash_forward", "offset": [0.0, 8.5, 0.0]},
                {"timestamp_sec": 3.8, "pose_name": "skyward_clash", "offset": [0.0, 2.0, 15.0]}
            ]

        return kinetic_records

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

    def _save_to_workspace(self, data, filename="36_volumetric_speed_lines_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Speed line blueprint written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save speed lines: {str(e)}")
            return None

    def design_volumetric_speed_lines(self):
        velocities = self._load_upstream_velocities()
        print(f"[{self.agent_name}] Speed Lines Architect active. Designing frame flickering patterns and depth vectors...")

        system_prompt = (
            "You are a master Cel-Animation & Composition Director specialized in dynamic anime action line shaders in Blender.\n"
            "Your job is to generate parameters for speed line meshes that dynamically frame the screen based on action velocities.\n"
            "For each movement entry, design exactly 1 speed line configuration in a list named 'speed_line_profiles' with these keys:\n"
            "- 'timestamp_sec': float matching the movement timeline.\n"
            "- 'speed_line_style': string (choose from: 'radial_zoom_in' for camera-oriented focus, 'horizontal_streaks' for side-scroll runs, 'vertical_drop_lines' for aerial falls).\n"
            "- 'line_density_count': integer (defines the number of lines surrounding the viewport; range 150 to 800).\n"
            "- 'line_length_meters': float (length of individual line streaks; range 5.0 to 45.0 meters).\n"
            "- 'core_flicker_frequency_hz': float (defines how fast lines teleport to new positions to create high-velocity motion; range 12.0 to 24.0 Hz).\n"
            "- 'line_opacity_alpha': float (visibility weight of speed lines; range 0.2 to 1.0).\n"
            "- 'line_color_rgba': array of 4 floats representing [R, G, B, A] (usually solid white [1.0, 1.0, 1.0, 1.0] or dynamic charging energy like [0.0, 0.8, 1.0, 0.9]).\n"
            "- 'radial_center_offset_xy': array of 2 floats [x, y] representing screen center deviation (from -0.5 to 0.5; default [0.0, 0.0]).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'speed_line_profiles'. "
            "Do not write conversational text, markdown blocks, or backticks. Return pure JSON only."
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
                    {"role": "user", "content": f"Kinetic Movement Logs:\n{json.dumps(velocities, indent=2)}"}
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
                    {"role": "user", "content": f"Kinetic Movement Logs:\n{json.dumps(velocities, indent=2)}"}
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
                    "speed_line_profiles": structured_output.get("speed_line_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Loading procedural lines fallback generator.")
            return self._execute_procedural_fallback(velocities)

    def _execute_procedural_fallback(self, velocities):
        # Precise algorithmic line builder translating displacement coordinates directly to focal angles
        profiles = []
        for v in velocities:
            ts = float(v.get("timestamp_sec", 0.0))
            pose = str(v.get("pose_name", "")).lower()
            offset = v.get("offset", [0.0, 0.0, 0.0])

            # Determine dominant velocity dimension
            y_speed = abs(offset[1])
            z_speed = abs(offset[2])

            if z_speed > y_speed:
                # Vertical/skyward movement
                style = "vertical_drop_lines"
                density = 450
                length = 35.0
                flicker = 24.0 # Maximum flicker for rapid climbs/falls
                alpha = 0.8
                color = [1.0, 1.0, 1.0, 0.8]
                center = [0.0, 0.1]
            elif y_speed > 5.0:
                # Rapid forward dash toward screen center
                style = "radial_zoom_in"
                density = 600
                length = 20.0
                flicker = 18.0
                alpha = 0.95
                color = [0.1, 0.7, 1.0, 0.9] # Blue energy trace
                center = [0.0, 0.0]
            else:
                # Standard horizontal running
                style = "horizontal_streaks"
                density = 200
                length = 15.0
                flicker = 12.0
                alpha = 0.5
                color = [0.9, 0.9, 0.9, 0.5]
                center = [0.0, 0.0]

            profiles.append({
                "timestamp_sec": ts,
                "speed_line_style": style,
                "line_density_count": density,
                "line_length_meters": length,
                "core_flicker_frequency_hz": flicker,
                "line_opacity_alpha": alpha,
                "line_color_rgba": color,
                "radial_center_offset_xy": center
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Lines Fallback)",
            "speed_line_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    architect = VolumetricSpeedLinesArchitect()
    output = architect.design_volumetric_speed_lines()
    
    print("\n--- Z-NET VFX COMPOSITOR: AGENT 36 SPEED LINES ARCHITECT COMPLETE ---")
    print(f"Total dynamic speed line states designed: {len(output['speed_line_profiles'])}")
    for profile in output["speed_line_profiles"]:
        print(f"Time: {profile['timestamp_sec']}s | Style: '{profile['speed_line_style']}' | Density: {profile['line_density_count']}")
        print(f"  Length: {profile['line_length_meters']}m | Flicker: {profile['core_flicker_frequency_hz']}Hz | Alpha: {profile['line_opacity_alpha']}")
    print("----------------------------------------------------------------------")
