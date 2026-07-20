import os
import sys
import json
import re
import urllib.request

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AiAgent15LowFrequencySubDesigner:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 15: low_frequency_impact_sub_designer"
        self.workspace_dir = workspace_dir
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

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
        """Saves the synchronized sub-bass blueprint back to the central state."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("OmniMatrix state successfully updated with Sub-Bass synthesis profiles.")

    def _clean_json_response(self, raw_text):
        """Strips markdown and LLM wrappers to isolate raw JSON."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def fetch_sub_design_ai(self, target_bpm, heavy_events):
        """Queries AI logic cores to construct precise DSP sub-bass synthesis blueprints."""
        system_prompt = (
            "You are an expert low-frequency sound synthesizer and audio DSP engineer. "
            "Analyze video beat events and design precise low-frequency sub-bass impacts (sweeps and booms) "
            "to create a bone-shattering bass-drop effect.\n"
            "Return STRICTLY a JSON object containing a list named 'sub_profiles'.\n"
            "Each profile must contain:\n"
            "- 'timestamp_sec': float matching the trigger event timestamp.\n"
            "- 'start_frequency_hz': integer (choose between 60 and 90 Hz).\n"
            "- 'end_frequency_hz': integer (choose between 24 and 35 Hz for sub-bass rumble).\n"
            "- 'sweep_duration_seconds': float (0.8 to 2.2 seconds).\n"
            "- 'waveform_type': string (choose from: 'pure-sine', 'saturated-triangle', 'glitch-square').\n"
            "- 'target_gain_db': float (-6.0 to 0.0 dB based on impact intensity).\n"
            "- 'rumble_reverb_decay': float (0.0 to 0.50 seconds).\n"
        )
        
        user_prompt = f"Target Track Tempo: {target_bpm} BPM\nHeavy Impact Points:\n{json.dumps(heavy_events, indent=2)}"

        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for DSP audio modeling...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("sub_profiles", [])
            except Exception as e:
                self.log(f"Gemini Engine failed: {e}. Switching to OpenAI fallback.", "WARNING")

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
                    return json.loads(self._clean_json_response(raw_text)).get("sub_profiles", [])
            except Exception as e:
                self.log(f"OpenAI Engine failed: {e}. Switching to Mathematical Logic.", "WARNING")

        self.log("All AI API Cores failed. Engaging Offline DSP Synthesizer Math.", "STATUS")
        return self._execute_procedural_fallback(heavy_events)

    def _execute_procedural_fallback(self, heavy_events):
        """Calculates DSP low-frequency math procedurally without an LLM."""
        profiles = []
        for trig in heavy_events:
            ts = float(trig.get("timestamp_sec", 0.0))
            intensity = float(trig.get("impact_intensity", 0.8))

            start_freq = int(60 + (intensity * 25))
            end_freq = int(24 + ((1.0 - intensity) * 8))
            decay = round(0.8 + (intensity * 1.2), 2)
            gain = round(-6.0 + (intensity * 6.0), 1)
            
            if intensity > 0.85:
                waveform, reverb = "saturated-triangle", 0.40
            else:
                waveform, reverb = "pure-sine", 0.20

            profiles.append({
                "timestamp_sec": ts,
                "start_frequency_hz": start_freq,
                "end_frequency_hz": end_freq,
                "sweep_duration_seconds": decay,
                "waveform_type": waveform,
                "target_gain_db": gain,
                "rumble_reverb_decay": reverb
            })
        return profiles

    def process_sub_frequencies(self):
        state = self._load_matrix_state()
        
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent and target_agent != "Ai_Agent_15":
            self.log(f"Pipeline sequence mismatch. Expected {target_agent}, but executing {self.agent_name}.", "WARNING")

        audio_module = state.get("module_b_audio", {})
        beat_map_data = audio_module.get("phonk_beat_map", {})
        
        if not beat_map_data:
            self.log("Beat Drop Map is missing. Run Agent 14 first.", "ERROR")
            return

        bpm = beat_map_data.get("target_bpm", 130)
        all_events = beat_map_data.get("beat_sync_events", [])

        # Filter heavy drops for sub-bass assignment
        heavy_events = [ev for ev in all_events if ev.get("impact_intensity", 0.0) >= 0.7]
        
        if not heavy_events and all_events:
            heavy_events = [all_events[0]]

        self.log(f"Designing low-frequency architecture for {len(heavy_events)} impact points at {bpm} BPM...")
        
        sub_profiles = self.fetch_sub_design_ai(bpm, heavy_events)

        # Merge the generated DSP profiles directly back into the Beat Map events in the state
        for event in all_events:
            for sub in sub_profiles:
                if event.get("timestamp_sec") == sub.get("timestamp_sec"):
                    event["sub_bass_dsp_blueprint"] = sub
                    break
        
        state["module_b_audio"]["phonk_beat_map"]["beat_sync_events"] = all_events
        state["module_b_audio"]["sub_frequencies_mapped"] = True
        
        # Pipeline Handshake
        state["pipeline_status"]["last_active_agent"] = "Ai_Agent_15"
        state["pipeline_status"]["next_agent"] = "Agent_16"
        
        self._save_matrix_state(state)
        self.log("Success! Deep frequency logic merged into OmniMatrix. Handoff to Agent 16.")

if __name__ == "__main__":
    designer = AiAgent15LowFrequencySubDesigner()
    designer.process_sub_frequencies()
    print("\n--- OMNIMATRIX MODULE B: AGENT 15 COMPLETE ---")
