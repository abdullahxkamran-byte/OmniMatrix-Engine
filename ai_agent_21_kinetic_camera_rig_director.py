import os
import re
import sys
import json
import urllib.request
import urllib.error

class KineticCameraRigDirector:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 21: kinetic_camera_rig_director"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_sync_data(self):
        # Visual cues aur beat drops ko load karta hai camera movement peaks match karne ke liye
        storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        beat_path = os.path.join(self.workspace_dir, "14_phonk_beat_drop_map.json")
        
        sync_triggers = []
        
        # Try loading storyboard timings
        if os.path.exists(storyboard_path):
            try:
                with open(storyboard_path, "r", encoding="utf-8") as f:
                    sb_data = json.load(f)
                for i, panel in enumerate(sb_data.get("storyboard_panels", [])):
                    sync_triggers.append({
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "event_type": "storyboard_cut",
                        "intensity": panel.get("camera_movement_type", "dynamic").lower()
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Storyboard parse warning: {str(e)}")

        # Try loading beat drops to inject heavy camera-shakes
        if os.path.exists(beat_path):
            try:
                with open(beat_path, "r", encoding="utf-8") as f:
                    b_data = json.load(f)
                for drop in b_data.get("beat_drops", []):
                    sync_triggers.append({
                        "timestamp_sec": drop.get("timestamp_sec"),
                        "event_type": "beat_drop_impact",
                        "intensity": "extreme"
                    })
            except Exception:
                pass

        # Sort triggers chronologically
        sync_triggers = sorted(sync_triggers, key=lambda x: x["timestamp_sec"])

        # Fallback triggers if workspace is fresh
        if not sync_triggers:
            print(f"[{self.agent_name}] Workspace Alert: Dynamic triggers missing. Designing default camera timeline.")
            sync_triggers = [
                {"timestamp_sec": 0.0, "event_type": "intro_pan", "intensity": "moderate"},
                {"timestamp_sec": 3.5, "event_type": "beat_drop_impact", "intensity": "extreme"},
                {"timestamp_sec": 7.2, "event_type": "action_cut", "intensity": "high"}
            ]

        return sync_triggers

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

    def _save_to_workspace(self, data, filename="21_kinetic_camera_rig_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Kinetic camera rig blueprints saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save camera blueprint: {str(e)}")
            return None

    def design_camera_keyframes(self):
        sync_triggers = self._load_upstream_sync_data()
        print(f"[{self.agent_name}] Rig Director active. Creating frame-perfect camera movement keyframes with dynamic DoF tracking...")

        system_prompt = (
            "You are an elite cinematic action director, depth-of-field specialist, and Blender 3D camera layout expert.\n"
            "Your job is to generate precise procedural camera keyframes with integrated dynamic focal tracking (Depth of Field) parameters compatible with Blender's animation curves.\n"
            "For each sync trigger, output exactly 1 camera movement block inside a list named 'camera_keyframe_data' with these properties:\n"
            "- 'timestamp_sec': float matching the sync trigger time.\n"
            "- 'shot_type': string representing dynamic framing (choose from: 'dolly-zoom', 'orbital-spin', 'whip-pan-transition', 'extreme-close-up', 'dramatic-tilt').\n"
            "- 'focal_length_mm': float representing zoom dynamics (choose between 18.0 for ultra-wide dynamic action to 85.0 for cinematic flat portrait-focus).\n"
            "- 'camera_location_offset': array of 3 floats [x, y, z] representing offset positions.\n"
            "- 'camera_rotation_euler': array of 3 floats [x, y, z] representing angles in degrees.\n"
            "- 'screen_shake_amplitude': float (scale from 0.0 to 1.5; high values like 1.2-1.5 should be assigned only to 'beat_drop_impact' or 'extreme' intensity).\n"
            "- 'interpolation_type': string for motion curve smoothness (choose from: 'BEZIER', 'LINEAR', 'SINE').\n"
            "- 'dof_focal_tracking_enabled': boolean (true to lock camera focus on a moving target, false for manual distance focus).\n"
            "- 'dof_focal_target_name': string (choose from: 'char_head_focus_empty' to prioritize face detail/eyes, 'combat_impact_point_empty' for action collisions, 'none' if tracking is disabled).\n"
            "- 'dof_aperture_fstop': float (simulates cinematic background bokeh blur; range 1.2 for extremely blurry background/shallow depth, to 11.0 for deep landscape sharpness).\n"
            "- 'dof_manual_focus_distance_meters': float (manual focus distance in meters when tracking is disabled; range 1.0 to 15.0).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'camera_keyframe_data'. "
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
                    {"role": "user", "content": f"Active Timeline Triggers:\n{json.dumps(sync_triggers, indent=2)}"}
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
                    {"role": "user", "content": f"Active Timeline Triggers:\n{json.dumps(sync_triggers, indent=2)}"}
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
                    "camera_keyframe_data": structured_output.get("camera_keyframe_data", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Executing procedural fallback camera engine.")
            return self._execute_procedural_fallback(sync_triggers)

    def _execute_procedural_fallback(self, sync_triggers):
        # High-action procedural mathematical model to calculate keyframes and depth parameters automatically
        keyframes = []
        for trigger in sync_triggers:
            ts = float(trigger.get("timestamp_sec", 0.0))
            event = str(trigger.get("event_type", "storyboard_cut")).lower()
            intensity = str(trigger.get("intensity", "moderate")).lower()

            if "beat_drop" in event or "extreme" in intensity:
                shot = "dolly-zoom"
                focal = 24.0
                loc = [0.0, -3.5, 1.2]
                rot = [15.0, 0.0, 0.0]
                shake = 1.4
                interp = "SINE"
                # DoF Focal Settings Integration
                dof_enabled = True
                dof_target = "char_head_focus_empty"
                fstop = 1.2  # Dynamic high-blur cinematic bokeh
                manual_dist = 2.5
            elif "high" in intensity or "cut" in event:
                shot = "orbital-spin"
                focal = 35.0
                loc = [1.5, -2.0, 0.8]
                rot = [10.0, 0.0, 45.0]
                shake = 0.4
                interp = "BEZIER"
                # DoF Focal Settings Integration
                dof_enabled = True
                dof_target = "char_head_focus_empty"
                fstop = 1.8  # Soft cinematic portrait background blur
                manual_dist = 3.2
            else:
                shot = "dramatic-tilt"
                focal = 50.0
                loc = [0.0, -5.0, 2.0]
                rot = [-5.0, 0.0, 0.0]
                shake = 0.0
                interp = "LINEAR"
                # DoF Focal Settings Integration
                dof_enabled = False
                dof_target = "none"
                fstop = 5.6  # Standard focal depth for wide narrative angles
                manual_dist = 5.0

            keyframes.append({
                "timestamp_sec": ts,
                "shot_type": shot,
                "focal_length_mm": focal,
                "camera_location_offset": loc,
                "camera_rotation_euler": rot,
                "screen_shake_amplitude": shake,
                "interpolation_type": interp,
                "dof_focal_tracking_enabled": dof_enabled,
                "dof_focal_target_name": dof_target,
                "dof_aperture_fstop": fstop,
                "dof_manual_focus_distance_meters": manual_dist
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Camera Fallback with DoF)",
            "camera_keyframe_data": keyframes
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    director = KineticCameraRigDirector()
    output = director.design_camera_keyframes()
    
    print("\n--- Z-NET BLENDER ENGINE: AGENT 21 CAMERA RIG DIRECTED ---")
    print(f"Dynamic camera movements mapped: {len(output['camera_keyframe_data'])}")
    if output["camera_keyframe_data"]:
        sample = output["camera_keyframe_data"][0]
        print(f"First Cue at {sample['timestamp_sec']}s | Shot: '{sample['shot_type']}' | Shake-Force: {sample['screen_shake_amplitude']} | Focal: {sample['focal_length_mm']}mm")
        print(f"  DoF Active: {sample['dof_focal_tracking_enabled']} | Focus Target: '{sample['dof_focal_target_name']}' | F-Stop: f/{sample['dof_aperture_fstop']}")
    print("----------------------------------------------------------")
