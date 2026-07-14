import os
import re
import sys
import json
import urllib.request
import urllib.error

class PhonkBeatDropAnalyzer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 14: phonk_beat_drop_analyzer"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        # Suggested Phonk Tempo (Beats Per Minute) range: 120 to 160 BPM
        self.target_bpm = 130 

        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_precision_timestamps(self):
        """
        Loads the final synchronized precision timeline from Stage 12.
        Falls back to manual bypass if workspace assets are empty.
        """
        input_path = os.path.join(self.workspace_dir, "12_precision_timestamps.json")
        if os.path.exists(input_path):
            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Stage 12 timestamps loaded from '{input_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: File read error ({str(e)}). Switching to manual timeline.")

        print(f"[{self.agent_name}] Workspace Alert: Upstream timing file missing. Utilizing active simulation.")
        return {
            "master_duration_sec": 12.5,
            "precision_timeline": [
                {"frame_index": 1, "global_frame_start_sec": 0.0, "global_frame_end_sec": 4.0},
                {"frame_index": 2, "global_frame_start_sec": 4.0, "global_frame_end_sec": 8.5},
                {"frame_index": 3, "global_frame_start_sec": 8.5, "global_frame_end_sec": 12.5}
            ]
        }

    def _clean_json_response(self, raw_text):
        """
        Cleans LLM response and ensures correct JSON structures.
        """
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def _save_to_workspace(self, data, filename="14_phonk_beat_drop_map.json"):
        """
        Saves the structured beat sync blueprint to the local workspace folder.
        """
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Beat-drop synchronization blueprint saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save state files: {str(e)}")
            return None

    def analyze_phonk_beats(self):
        """
        Applies AI reasoning to calculate high-impact audio beat coordinates 
        and synchronization milestones matching the video pacing boundaries.
        """
        timing_data = self._load_precision_timestamps()
        master_duration = float(timing_data.get("master_duration_sec", 10.0))
        timeline = timing_data.get("precision_timeline", [])

        print(f"[{self.agent_name}] Designing Phonk Beat & Drop choreography for {master_duration}s timeline...")

        system_prompt = (
            "You are an elite video editing director specialized in sync-editing Drift Phonk, House, and Dark Synth music. "
            "Your job is to generate high-impact visual FX cues based on beat drops, rhythm patterns, and vocal timelines.\n"
            "Produce exactly 1 JSON object containing a list named 'beat_sync_events'. "
            "Every event must have these exact parameters:\n"
            "- 'timestamp_sec': float indicating when the beat event occurs (must be strictly between 0.0 and the total video duration).\n"
            "- 'event_type': string detailing action trigger (choose only from: 'bass-drop-flash', 'cowbell-roll-glitch', 'sub-bass-zoom', 'snare-shake').\n"
            "- 'impact_intensity': float scaling from 0.1 (subtle rumble) to 1.0 (extreme screen-shattering shake and flash).\n"
            "- 'editor_action_note': string instruction for the editor (e.g., 'Invert colors on beat', 'White flash transition', 'Punch-in scale shift').\n"
            "Format your output STRICTLY as raw JSON. Do not write explanations, greetings, or backticks. Only return valid JSON."
        )

        user_prompt = (
            f"Total Video Duration: {master_duration} seconds.\n"
            f"Target Music Rhythm: {self.target_bpm} BPM (Beats Per Minute).\n"
            f"Core Video Frames Timing Details:\n{json.dumps(timeline, indent=2)}"
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
                    {"role": "user", "content": user_prompt}
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
                    {"role": "user", "content": user_prompt}
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
                    "target_bpm": self.target_bpm,
                    "agent_executed": self.agent_name,
                    "beat_sync_events": structured_output.get("beat_sync_events", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connectivity/Parsing Exception: {str(e)}. Running mathematical fallback engine.")
            return self._execute_procedural_fallback(master_duration, timeline)

    def _execute_procedural_fallback(self, master_duration, timeline):
        """
        Calculates high-precision beat structures using standard music theory 
        BPM subdivisions in the absence of an active LLM.
        """
        # Calculate time interval per beat: (60 seconds / BPM)
        beat_interval = 60.0 / self.target_bpm
        events = []
        
        current_time = 0.0
        beat_counter = 1

        # Walk through the timeline applying rhythmic beat structures
        while current_time < master_duration:
            # Standard Phonk Pattern: Every 4 beats is a Bar (Major Drop Potential)
            is_bar_drop = (beat_counter % 4 == 0)
            is_eight_bar_peak = (beat_counter % 8 == 0)

            if is_eight_bar_peak:
                event_type = "bass-drop-flash"
                intensity = 0.95
                note = "Extreme screen-shattering flash + heavy zoom out to match main bass drop."
            elif is_bar_drop:
                event_type = "cowbell-roll-glitch"
                intensity = 0.75
                note = "Triple-split glitch effect + rapid color shake."
            else:
                # Regular snare/kick timing
                event_type = "snare-shake"
                intensity = 0.40
                note = "Quick structural scale punch-in (105%)."

            events.append({
                "timestamp_sec": round(current_time, 3),
                "event_type": event_type,
                "impact_intensity": intensity,
                "editor_action_note": note
            })

            current_time += beat_interval
            beat_counter += 1

        fallback_output = {
            "target_bpm": self.target_bpm,
            "agent_executed": f"{self.agent_name} (Mathematical Fallback Mode)",
            "beat_sync_events": events
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    analyzer = PhonkBeatDropAnalyzer()
    output = analyzer.analyze_phonk_beats()
    
    print("\n--- Z-NET AUDIO ENGINE: AGENT 14 PHONK BEAT DROP COMPLETED ---")
    print(f"BPM Target: {output['target_bpm']} BPM")
    print(f"Total synced visual triggers registered: {len(output['beat_sync_events'])}")
    if output["beat_sync_events"]:
        print(f"Sample First Drop Spot: {output['beat_sync_events'][0]['timestamp_sec']}s -> {output['beat_sync_events'][0]['event_type']}")
    print("----------------------------------------------------------------")
