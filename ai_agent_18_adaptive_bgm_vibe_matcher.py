import os
import re
import sys
import json
import urllib.request
import urllib.error

class AdaptiveBgmVibeMatcher:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 18: adaptive_bgm_vibe_matcher"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_data(self):
        # Storyboard aur timing events ko scan karta hai music transitions match karne ke liye
        storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        voice_path = os.path.join(self.workspace_dir, "13_voiceover_timing_map.json")
        
        narrative_cues = []
        
        # 1. Voiceover timeline load karne ki koshish
        if os.path.exists(voice_path):
            try:
                with open(voice_path, "r", encoding="utf-8") as f:
                    voice_data = json.load(f)
                for block in voice_data.get("voiceover_segments", []):
                    narrative_cues.append({
                        "start_sec": block.get("start_sec", 0.0),
                        "end_sec": block.get("end_sec", 3.0),
                        "emotional_tone": block.get("vocal_tone", "neutral"),
                        "text_context": block.get("text", "")
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Voiceover map parse warning: {str(e)}")

        # Fallback agar upstream file na mile
        if not narrative_cues:
            print(f"[{self.agent_name}] Workspace Alert: No voiceover map found. Using defaults.")
            narrative_cues = [
                {"start_sec": 0.0, "end_sec": 2.5, "emotional_tone": "dark-suspense", "text_context": "In the shadow of the forgotten realm..."},
                {"start_sec": 2.5, "end_sec": 6.0, "emotional_tone": "high-energy", "text_context": "Suddenly, his power awakened with absolute rage!"},
                {"start_sec": 6.0, "end_sec": 9.5, "emotional_tone": "epic-climax", "text_context": "Nothing can stand in his way now."}
            ]

        return narrative_cues

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

    def _save_to_workspace(self, data, filename="18_bgm_vibe_matcher_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: BGM dynamic timeline written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save state files: {str(e)}")
            return None

    def map_bgm_vibe_timeline(self):
        cues = self._load_upstream_data()
        print(f"[{self.agent_name}] Vibe Engine active. Generating dynamic BGM automation curves...")

        system_prompt = (
            "You are a cinematic music supervisor and dynamic video editor. "
            "Your job is to analyze video narration curves and build dynamic volume/genre automation parameters for the background music (BGM).\n"
            "Generate exactly 1 music automation segment for each vocal segment inside a list named 'bgm_automation_segments' with these parameters:\n"
            "- 'start_sec': float matching the narration block start.\n"
            "- 'end_sec': float matching the narration block end.\n"
            "- 'bgm_vibe_style': string (choose from: 'dark-ambient-pad', 'aggressive-phonk-drill', 'cyberpunk-chiptune', 'orchestral-epic-riser').\n"
            "- 'target_bgm_volume_db': float representing recommended baseline music volume (scale from -24.0 dB during talking to -6.0 dB during silent heavy action peaks).\n"
            "- 'filter_cutoff_hz': integer (choose between 400 and 20000 Hz. Low values like 400-800 Hz are used to filter high-ends and make music sound underwater while vocals are very important).\n"
            "- 'tempo_multiplier': float representing track speed scaling (choose only from: 0.75, 1.0, 1.25 for slow/normal/fast pacing adjustments).\n"
            "- 'vibe_shift_note': a short dynamic description explaining the musical transition logic.\n"
            "Format your output STRICTLY as a raw JSON object containing the list key 'bgm_automation_segments'. "
            "No small talks, no explanations, no code block backticks. Output only valid JSON."
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
                    {"role": "user", "content": f"Vocal Narrative Flow:\n{json.dumps(cues, indent=2)}"}
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
                    {"role": "user", "content": f"Vocal Narrative Flow:\n{json.dumps(cues, indent=2)}"}
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
                    "bgm_automation_segments": structured_output.get("bgm_automation_segments", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connectivity Exception: {str(e)}. Running procedural vibe fallback mapping.")
            return self._execute_procedural_fallback(cues)

    def _execute_procedural_fallback(self, cues):
        segments = []
        for cue in cues:
            start = float(cue.get("start_sec", 0.0))
            end = float(cue.get("end_sec", 3.0))
            tone = cue.get("emotional_tone", "neutral").lower()

            if "dark" in tone:
                style = "dark-ambient-pad"
                vol = -20.0
                cutoff = 1200 # Muffled to make it deep
                mult = 0.75
                note = "Slow low-pass filtered pad for tense atmosphere."
            elif "high" in tone or "rage" in tone:
                style = "aggressive-phonk-drill"
                vol = -12.0
                cutoff = 20000 # Full range open
                mult = 1.25
                note = "Energy spike. Unfiltered heavy phonk beat kick-in."
            elif "epic" in tone or "climax" in tone:
                style = "orchestral-epic-riser"
                vol = -8.0
                cutoff = 18000
                mult = 1.0
                note = "High intensity build up to drop."
            else:
                style = "cyberpunk-chiptune"
                vol = -16.0
                cutoff = 5000
                mult = 1.0
                note = "Standard mid-tempo video game vibe adjustment."

            segments.append({
                "start_sec": start,
                "end_sec": end,
                "bgm_vibe_style": style,
                "target_bgm_volume_db": vol,
                "filter_cutoff_hz": cutoff,
                "tempo_multiplier": mult,
                "vibe_shift_note": note
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Vibe Fallback)",
            "bgm_automation_segments": segments
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    matcher = AdaptiveBgmVibeMatcher()
    output = matcher.map_bgm_vibe_timeline()
    
    print("\n--- Z-NET AUDIO ENGINE: AGENT 18 BGM VIBE MATCHING COMPLETED ---")
    print(f"BGM Vibe change sectors mapped: {len(output['bgm_automation_segments'])}")
    if output["bgm_automation_segments"]:
        sample = output["bgm_automation_segments"][0]
        print(f"Timeline Segment: {sample['start_sec']}s -> {sample['end_sec']}s | Style: {sample['bgm_vibe_style']} | Base Volume: {sample['target_bgm_volume_db']}dB")
    print("-----------------------------------------------------------------")
