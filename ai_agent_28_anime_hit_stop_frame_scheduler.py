import os
import re
import sys
import json
import urllib.request
import urllib.error

class AnimeHitStopFrameScheduler:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 28: anime_hit_stop_frame_scheduler"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_collisions(self):
        # Stage 27 (Collision Sentinel) se dynamic impacts load karta hai
        collision_path = os.path.join(self.workspace_dir, "27_mesh_collision_blueprint.json")
        collision_events = []

        if os.path.exists(collision_path):
            try:
                with open(collision_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Filter only active conflicts to schedule freezes
                for ev in data.get("collision_resolution_events", []):
                    if ev.get("has_collision_conflict", False):
                        collision_events.append({
                            "timestamp_sec": ev.get("timestamp_sec", 0.0),
                            "severity": ev.get("conflict_severity", "LOW_CLIP"),
                            "impact_force": ev.get("impact_force_magnitude", 10.0)
                        })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream collision data load warning: {str(e)}")

        # Fallback agar collision blueprint missing ho
        if not collision_events:
            print(f"[{self.agent_name}] Workspace Alert: No collision conflicts found. Creating default hit points.")
            collision_events = [
                {"timestamp_sec": 1.5, "severity": "LOW_CLIP", "impact_force": 12.5},
                {"timestamp_sec": 4.5, "severity": "HIGH_PENETRATION", "impact_force": 45.0}
            ]

        return collision_events

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

    def _save_to_workspace(self, data, filename="28_anime_hit_stop_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Hit stop schedule written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save hit stop schedule: {str(e)}")
            return None

    def schedule_hit_stops(self):
        collisions = self._load_upstream_collisions()
        print(f"[{self.agent_name}] Scheduler active. Calculating frame multiplication and time dilation constants...")

        system_prompt = (
            "You are an expert anime post-production director and time-remapping editor.\n"
            "Your job is to design dynamic 'Hit Stop' (impact freeze) timelines for animation sequences based on physical collision force.\n"
            "Assume a standard animation base speed of 24 Frames Per Second (FPS).\n"
            "For each collision event, output exactly 1 hit-stop freeze block inside a list named 'hit_stop_schedules' with these parameters:\n"
            "- 'timestamp_sec': float matching the collision point.\n"
            "- 'freeze_duration_frames': integer (number of frames to hold the visual completely still; scale from 3 to 18 frames based on impact force).\n"
            "- 'time_dilation_factor': float (scale from 0.0 for a complete hardware absolute pause to 0.15 for extremely slow micro-creeping movement during hit).\n"
            "- 'camera_zoom_shudder_amplitude': float representing dramatic camera zoom snaps during freeze (scale from 0.0 to 0.8).\n"
            "- 'shake_frequency_hz': float representing fast camera vibration frequency during the hold (scale from 5.0 to 25.0 Hz).\n"
            "- 'editor_compositing_flash': string designating visual styling (choose only from: 'white-screen-flash', 'color-inversion-frame', 'subtle-vignette-pinch', 'none').\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'hit_stop_schedules'. "
            "Do not write explanations, greetings, markdown code blocks, or backticks. Return ONLY valid JSON."
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
                    {"role": "user", "content": f"Active Impact Cues:\n{json.dumps(collisions, indent=2)}"}
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
                    {"role": "user", "content": f"Active Impact Cues:\n{json.dumps(collisions, indent=2)}"}
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
                    "hit_stop_schedules": structured_output.get("hit_stop_schedules", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Network/Connection Exception: {str(e)}. Running procedural hit stop calculator.")
            return self._execute_procedural_fallback(collisions)

    def _execute_procedural_fallback(self, collisions):
        # Precise mathematical re-mapping of physical forces directly to 24fps frame delays
        schedules = []
        for col in collisions:
            ts = float(col.get("timestamp_sec", 0.0))
            force = float(col.get("impact_force", 10.0))
            severity = str(col.get("severity", "LOW_CLIP")).upper()

            # Dynamic calculations based on force intensity
            if severity == "HIGH_PENETRATION" or force > 30.0:
                frames = int(8 + (force * 0.2)) # Up to 18 frames hold (~0.75 seconds pause)
                dilation = 0.0 # Absolute stark freeze
                zoom = 0.6 # Dramatic crop snap
                shake = 22.0 # Violent fast camera rattle
                flash = "color-inversion-frame" # Heavy anime trademark stylization
            else:
                frames = int(3 + (force * 0.15)) # 3 to 7 frames subtle lag
                dilation = 0.1 # Dynamic micro-creep
                zoom = 0.15
                shake = 8.0
                flash = "subtle-vignette-pinch"

            # Boundary safety limits
            frames = max(2, min(frames, 20))

            schedules.append({
                "timestamp_sec": ts,
                "freeze_duration_frames": frames,
                "time_dilation_factor": dilation,
                "camera_zoom_shudder_amplitude": zoom,
                "shake_frequency_hz": shake,
                "editor_compositing_flash": flash
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Hit-Stop Fallback)",
            "hit_stop_schedules": schedules
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    scheduler = AnimeHitStopFrameScheduler()
    output = scheduler.schedule_hit_stops()
    
    print("\n--- Z-NET BLENDER ENGINE: AGENT 28 HIT-STOP SCHEDULE COMPLETE ---")
    print(f"Total dynamic hit-stop events mapped: {len(output['hit_stop_schedules'])}")
    for sched in output["hit_stop_schedules"]:
        print(f"Time: {sched['timestamp_sec']}s | Freeze Hold: {sched['freeze_duration_frames']} frames | Stylized Flash: {sched['editor_compositing_flash']} | Cam Vibration: {sched['shake_frequency_hz']}Hz")
    print("------------------------------------------------------------------")
