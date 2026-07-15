import os
import sys
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

class AiSupremeCreativeScriptConductor:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 65: supreme_creative_script_conductor"
        self.workspace_dir = workspace_dir
        self.script_path = os.path.join(self.workspace_dir, "08_formatted_script.json")
        self.directive_path = os.path.join(self.workspace_dir, "65_master_conductor_timeline.json")

        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_raw_script(self):
        # formatted script load karta hai jo dynamic voice and story arcs ke sath ho
        if os.path.exists(self.script_path):
            try:
                with open(self.script_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Script load nahi ho saka: {str(e)}")
        
        # Fallback raw script structured context agar real system dynamic script missing ho
        return {
            "title": "Gojo Void Decimation",
            "voice_over_script": "In the realm of infinite void, physical limits cease to exist. Prepare to witness raw distortion.",
            "duration_seconds": 15
        }

    def choreograph_master_directives(self):
        print(f"[{self.agent_name}] Initiating Supreme Artistic Director brain. Choreographing camera, environment, and physical dynamics...")
        raw_script = self._load_raw_script()

        system_prompt = (
            "You are a Legendary Anime Director (like Shingo Natsume or Sunghoo Park). You are the Supreme Creative Script Conductor.\n"
            "Your task is to analyze a raw script and construct a detailed master execution timeline for subsequent agents. "
            "You must visualize the environment space, the character actions, camera directives, and timing beats before rendering starts.\n\n"
            "Generate a JSON list named 'master_directives' with these key structures for each timeline segment:\n"
            "- 'segment_id': integer (ordered sequence).\n"
            "- 'duration_slice': float (duration in seconds, total must sum up to the script length).\n"
            "- 'action_choreography': descriptive string of exact character physical posture, expression, and speed of motion.\n"
            "- 'environment_state': descriptive string of environment geometry, weather (e.g., volumetric fog, low-poly neon lighting, spatial dust).\n"
            "- 'camera_rig_behavior': string (choose from: 'dramatic_orbital_zoom', 'ground_level_upward_pan', 'extreme_dutch_angle', 'shaky_handheld_track').\n"
            "- 'orchestrated_agent_commands': object containing targeted directions for other nodes:\n"
            "    * 'agent_14_phonk_beat_sync': action trigger (e.g., 'impact_flash', 'slow_mo_rise', 'bass_drop_shake').\n"
            "    * 'agent_22_lighting_shader': tone settings (e.g., 'high_contrast_rim_light', 'ambient_dark_purple').\n"
            "    * 'agent_30_fracture_engine': fracture timing (e.g., 'ground_cracking_frame_12', 'no_destruction').\n\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'master_directives'. "
            "Do not write conversational intro, outro, explanations, or markdown blocks (```json). Just return valid raw JSON."
        )

        user_prompt = f"Target Video Script Content:\n{json.dumps(raw_script, indent=2)}"

        if self.openai_api_key:
            print(f"[{self.agent_name}] Status: Querying Cloud Creative Intelligence Node [{self.model_cloud}]")
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
            print(f"[{self.agent_name}] Status: Querying Local Llama3 Creative Node via Ollama...")
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
                
                final_master_timeline = {
                    "agent_executed": self.agent_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "video_title": raw_script.get("title", "Untitled"),
                    "master_directives": structured_data.get("master_directives", [])
                }
                
                self._save_master_timeline(final_master_timeline)
                return final_master_timeline

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Triggering Master Conductor Fallback Logic...")
            return self._execute_procedural_fallback(raw_script)

    def _clean_json(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned

    def _execute_procedural_fallback(self, raw_script):
        # AI engine offline hone par automatic pre-choreographed cinematic timing split
        total_duration = raw_script.get("duration_seconds", 15)
        segment_duration = round(total_duration / 2, 2)
        
        fallback_timeline = {
            "agent_executed": f"{self.agent_name} (Procedural Fallback)",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "video_title": raw_script.get("title", "Untitled"),
            "master_directives": [
                {
                    "segment_id": 1,
                    "duration_slice": segment_duration,
                    "action_choreography": "Character standing tense with a dark smirk, hands in pockets, wind blowing hair vigorously.",
                    "environment_state": "Desolate landscape under high-contrast purple lightning and volumetric smoke.",
                    "camera_rig_behavior": "dramatic_orbital_zoom",
                    "orchestrated_agent_commands": {
                        "agent_14_phonk_beat_sync": "slow_mo_rise",
                        "agent_22_lighting_shader": "ambient_dark_purple",
                        "agent_30_fracture_engine": "no_destruction"
                    }
                },
                {
                    "segment_id": 2,
                    "duration_slice": segment_duration,
                    "action_choreography": "Character releases violent shockwave, ground cracking under feet, camera lens cracking visual effect.",
                    "environment_state": "Dynamic low-poly environment shattering into physical elements, high chromatic aberration.",
                    "camera_rig_behavior": "shaky_handheld_track",
                    "orchestrated_agent_commands": {
                        "agent_14_phonk_beat_sync": "bass_drop_shake",
                        "agent_22_lighting_shader": "high_contrast_rim_light",
                        "agent_30_fracture_engine": "ground_cracking_frame_12"
                    }
                }
            ]
        }
        self._save_master_timeline(fallback_timeline)
        return fallback_timeline

    def _save_master_timeline(self, data):
        try:
            with open(self.directive_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Master timeline choreographed and saved to '{self.directive_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing master timeline: {str(e)}")

if __name__ == "__main__":
    conductor = AiSupremeCreativeScriptConductor()
    print("--- TESTING AI SCRIPT CONDUCTOR ENGINE ---")
    report = conductor.run_manual_choreography = conductor.choreograph_master_directives()
    print("\n--- MASTER TIMELINE DIRECTIVES ---")
    print(json.dumps(report, indent=4))
