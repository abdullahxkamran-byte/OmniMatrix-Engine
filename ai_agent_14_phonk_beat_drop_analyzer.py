import os
import sys
import json
import re
import urllib.request

# Manual .env loader utility
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

# Standardize Gemini Integration
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AiAgent14PhonkBeatDropAnalyzer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 14: phonk_beat_drop_analyzer"
        self.workspace_dir = workspace_dir
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        
        self.target_bpm = 130 # Core Phonk/Drift tempo baseline

        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if GEMINI_AVAILABLE and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        """Loads the central OmniMatrix state file."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run upstream modules first.", "ERROR")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        """Saves the synchronized beat map back to the state file."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("OmniMatrix state successfully updated with Phonk Beat-Drop topology.")

    def _clean_json_response(self, raw_text):
        """Sanitizes AI model outputs to extract raw JSON data safely."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def analyze_beats_ai(self, master_duration, timeline_data):
        """Uses AI logic cores to design highly aesthetic beat drop visual triggers."""
        system_prompt = (
            "You are an elite video editing director specialized in sync-editing Drift Phonk, House, and Dark Synth music. "
            "Generate high-impact visual FX cues based on the provided video timing boundaries and a baseline of 130 BPM.\n"
            "Return STRICTLY a JSON object containing a list named 'beat_sync_events'.\n"
            "Every event must have these exact parameters:\n"
            "- 'timestamp_sec': float (must be strictly between 0.0 and total duration).\n"
            "- 'event_type': string (choose from: 'bass-drop-flash', 'cowbell-roll-glitch', 'sub-bass-zoom', 'snare-shake').\n"
            "- 'impact_intensity': float (0.1 to 1.0).\n"
            "- 'editor_action_note': string instruction (e.g., 'Invert colors on beat', 'White flash transition').\n"
        )
        
        user_prompt = (
            f"Total Video Duration: {master_duration} seconds.\n"
            f"Core Audio/Visual Timeline Details:\n{json.dumps(timeline_data, indent=2)}"
        )

        # 1st Priority: Gemini (High Logic Speed)
        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for beat sync mapping...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("beat_sync_events", [])
            except Exception as e:
                self.log(f"Gemini Engine failed: {e}. Switching to OpenAI fallback.", "WARNING")

        # 2nd Priority: OpenAI (gpt-4o-mini)
        if self.openai_api_key:
            self.log(f"Routing to Core 2: OpenAI API [{self.model_cloud}]...")
            url = self.openai_url
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"}
            payload = {
                "model": self.model_cloud,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "response_format": {"type": "json_object"}
            }
            try:
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    raw_text = res_data["choices"][0]["message"]["content"]
                    return json.loads(self._clean_json_response(raw_text)).get("beat_sync_events", [])
            except Exception as e:
                self.log(f"OpenAI Engine failed: {e}. Switching to Mathematical Logic.", "WARNING")

        # Fallback: Procedural Math Engine
        self.log("All AI API Cores failed. Engaging Offline Mathematical Beat-Drop Generator.", "STATUS")
        return self._execute_procedural_fallback(master_duration)

    def _execute_procedural_fallback(self, master_duration):
        """Calculates beat structures using standard music theory (BPM math)."""
        beat_interval = 60.0 / self.target_bpm
        events = []
        current_time = 0.0
        beat_counter = 1

        while current_time < master_duration:
            is_eight_bar_peak = (beat_counter % 8 == 0)
            is_bar_drop = (beat_counter % 4 == 0)

            if is_eight_bar_peak:
                event_type, intensity, note = "bass-drop-flash", 0.95, "Extreme screen-shattering flash + heavy zoom out."
            elif is_bar_drop:
                event_type, intensity, note = "cowbell-roll-glitch", 0.75, "Triple-split glitch effect + rapid color shake."
            else:
                event_type, intensity, note = "snare-shake", 0.40, "Quick structural scale punch-in (105%)."

            events.append({
                "timestamp_sec": round(current_time, 3),
                "event_type": event_type,
                "impact_intensity": intensity,
                "editor_action_note": note
            })
            
            current_time += beat_interval
            beat_counter += 1

        return events

    def generate_beat_map(self):
        state = self._load_matrix_state()
        
        # Verify Pipeline Sequence
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent and target_agent != "Ai_Agent_14":
            self.log(f"Pipeline sync note: Expected {target_agent}, but executing {self.agent_name}.", "WARNING")

        audio_module = state.get("module_b_audio", {})
        master_metrics = audio_module.get("master_timeline_metrics", {})
        total_duration = master_metrics.get("total_video_duration_sec", 0.0)
        
        if total_duration == 0.0:
            self.log("Master video duration missing. Ensure Agent 12 (Timestamps) ran successfully.", "ERROR")
            return

        audio_timeline = audio_module.get("audio_timeline", [])
        
        # Prepare lightweight data for the LLM to save tokens
        lightweight_timeline = [
            {"frame": f.get("frame_index"), "character": f.get("character"), "timing": f.get("global_timing")}
            for f in audio_timeline
        ]

        self.log(f"Designing Beat Drop choreography for {total_duration}s video timeline...")
        
        ai_beat_events = self.analyze_beats_ai(total_duration, lightweight_timeline)

        # Inject beat mapping data into OmniMatrix
        state["module_b_audio"]["phonk_beat_map"] = {
            "target_bpm": self.target_bpm,
            "total_beat_events": len(ai_beat_events),
            "beat_sync_events": ai_beat_events
        }
        
        # OmniMatrix Pipeline Handshake
        state["pipeline_status"]["last_active_agent"] = "Ai_Agent_14"
        state["pipeline_status"]["next_agent"] = "Ai_Agent_15"
        
        self._save_matrix_state(state)
        self.log(f"Success! {len(ai_beat_events)} visual impact triggers synchronized with audio beats.")

if __name__ == "__main__":
    analyzer = AiAgent14PhonkBeatDropAnalyzer()
    analyzer.generate_beat_map()
    print("\n--- OMNIMATRIX MODULE B: AGENT 14 COMPLETE ---")
