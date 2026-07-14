import os
import re
import sys
import json
import urllib.request
import urllib.error

class AiBeatToFrameEffectsSyncEngine:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 41: beat_to_frame_effects_sync_engine"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_data(self):
        # Motion Blur (Agent 40) aur Storyboard (Agent 03) ke logs read karta hai visual cues ke liye
        blur_path = os.path.join(self.workspace_dir, "40_motion_blur_blueprint.json")
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        rhythm_contexts = []

        if os.path.exists(blur_path):
            try:
                with open(blur_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for profile in data.get("motion_blur_profiles", []):
                    rhythm_contexts.append({
                        "timestamp_sec": profile.get("timestamp_sec", 0.0),
                        "implied_speed": "high_intensity" if profile.get("velocity_vector_multiplier", 0.0) > 2.0 else "ambient"
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream motion blur read warning: {str(e)}")

        if not rhythm_contexts and os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    rhythm_contexts.append({
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "implied_speed": "high_intensity" if "climax" in panel.get("emotional_tone", "").lower() else "ambient"
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream storyboard read warning: {str(e)}")

        # Fallback beat points (jaise dynamic Phonk music beat map 130 BPM par hota hai)
        if not rhythm_contexts:
            print(f"[{self.agent_name}] Workspace Alert: No visual timeline context found. Injecting standard 130 BPM action beats.")
            rhythm_contexts = [
                {"timestamp_sec": 0.46, "implied_speed": "ambient"},
                {"timestamp_sec": 0.92, "implied_speed": "high_intensity"}, # Drop beat!
                {"timestamp_sec": 1.38, "implied_speed": "ambient"},
                {"timestamp_sec": 1.84, "implied_speed": "high_intensity"}  # Climax drop!
            ]

        return rhythm_contexts

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

    def _save_to_workspace(self, data, filename="41_beat_sync_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Beat-to-frame sync blueprint saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save sync blueprint: {str(e)}")
            return None

    def design_beat_sync_keyframes(self):
        rhythm_points = self._load_upstream_data()
        print(f"[{self.agent_name}] Sync Engine active. Analyzing spectrogram frequency hits and mapping dynamic keys...")

        system_prompt = (
            "You are an elite Anime Video Editor and Music Sync Specialist.\n"
            "Your job is to match visual render properties directly with audio frequencies and beats.\n"
            "For each rhythm timestamp, generate exactly 1 sync configuration inside a list named 'beat_sync_profiles' with these parameters:\n"
            "- 'timestamp_sec': float matching the frame execution.\n"
            "- 'audio_frequency_band': string (choose from: 'sub_bass_drop' for heavy kick drums/impacts, 'mid_range_melody' for voices/swords, 'high_presence_tick' for sharp hi-hats/clicks).\n"
            "- 'vfx_scale_multiplier': float (scales the intensity of glows, fire, and smoke from Agent 37 & 38; range 0.5 to 2.5).\n"
            "- 'camera_shake_amplitude': float (instantly offsets the camera position to simulate hard bass impacts; range 0.0 to 1.8).\n"
            "- 'fps_stutter_trigger': boolean (true if we want to pause/stutter the frame for 2 frames during an impact for a hand-drawn look).\n"
            "- 'rgb_split_chromatic_aberration': float (separates red/blue channels for glitchy/powerful hits; range 0.0 to 0.15).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'beat_sync_profiles'. "
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
                    {"role": "user", "content": f"Rhythm Points Logs:\n{json.dumps(rhythm_points, indent=2)}"}
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
                    {"role": "user", "content": f"Rhythm Points Logs:\n{json.dumps(rhythm_points, indent=2)}"}
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
                    "beat_sync_profiles": structured_output.get("beat_sync_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Directing procedural beat tracker fallback.")
            return self._execute_procedural_fallback(rhythm_points)

    def _execute_procedural_fallback(self, rhythm_points):
        # Precise mathematical fallback translating implied speed directly to visual sync actions
        profiles = []
        for rp in rhythm_points:
            ts = float(rp.get("timestamp_sec", 0.0))
            intensity_hint = str(rp.get("implied_speed", "")).lower()

            if "high" in intensity_hint:
                # Heavy drop impact mapping
                band = "sub_bass_drop"
                scale = 2.2 # Blow up the visual effects sizes on screen
                shake = 1.4 # Heavy screen shake
                stutter = True # Pause slightly for extreme impact weight
                chromatic = 0.12 # Intense RGB color split
            else:
                # Ambient rhythm beat
                band = "high_presence_tick"
                scale = 1.0
                shake = 0.0
                stutter = False
                chromatic = 0.01

            profiles.append({
                "timestamp_sec": ts,
                "audio_frequency_band": band,
                "vfx_scale_multiplier": scale,
                "camera_shake_amplitude": shake,
                "fps_stutter_trigger": stutter,
                "rgb_split_chromatic_aberration": chromatic
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Beat-Sync Fallback)",
            "beat_sync_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    sync_engine = AiBeatToFrameEffectsSyncEngine()
    output = sync_engine.design_beat_sync_keyframes()
    
    print("\n--- Z-NET RHYTHM COMPOSITOR: AGENT 41 BEAT SYNC COMPLETE ---")
    print(f"Total rhythm frames synchronized: {len(output['beat_sync_profiles'])}")
    for p in output["beat_sync_profiles"]:
        print(f"Time: {p['timestamp_sec']}s | Band: '{p['audio_frequency_band']}'")
        print(f"  VFX Scale: {p['vfx_scale_multiplier']}x | Camera Shake: {p['camera_shake_amplitude']}px")
        print(f"  Impact Stutter: {p['fps_stutter_trigger']} | RGB Glitch Split: {p['rgb_split_chromatic_aberration']}")
    print("------------------------------------------------------------")
