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

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AiAgent15LowFrequencySubDesigner:
    def __init__(self):
        self.agent_name = "Ai_Agent_15"
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

        self.ollama_url = "http://localhost:11434/api/generate"
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
        """Loads the central OmniMatrix state securely."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run upstream modules first.", "FATAL")
            sys.exit(1)
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.log(f"JSON Corruption detected: {e}", "FATAL")
            sys.exit(1)

    def _save_matrix_state(self, state_data):
        """Saves the synchronized sub-bass blueprint back to the central state."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4, ensure_ascii=False)
        self.log("OmniMatrix state successfully updated with Sub-Bass synthesis profiles.", "SUCCESS")

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

    def fetch_sub_design_ai(self, target_bpm, heavy_events, video_format):
        """
        UNIVERSAL AI LOGIC CORE:
        Adapts the DSP frequencies based on Short-Form (Phonk) vs Long-Form (Cinematic).
        """
        
        if video_format == "long_form":
            style_guide = "Design deep, subtle, Hans Zimmer-style cinematic rumbles. Long reverb, low gain, pure-sine waveforms."
            freq_range = "start: 50-60Hz, end: 20-30Hz"
            gain_range = "-12.0 to -6.0 dB"
            waveform_options = "'pure-sine', 'deep-pulse'"
        else:
            style_guide = "Design aggressive, punchy, distortion-heavy 808 bass drops suitable for Drift Phonk or TikTok/Shorts."
            freq_range = "start: 80-100Hz, end: 30-40Hz"
            gain_range = "-4.0 to 0.0 dB"
            waveform_options = "'saturated-triangle', 'glitch-square', 'hard-saw'"

        system_prompt = (
            f"You are an expert audio DSP engineer. {style_guide}\n"
            "Analyze the impact points and design low-frequency sub-bass sweeps/booms.\n"
            "Return STRICTLY a JSON object containing a list named 'sub_profiles'.\n"
            "Each profile must contain:\n"
            "- 'timestamp_sec': float (must exactly match the input trigger timestamp).\n"
            f"- 'start_frequency_hz': integer ({freq_range}).\n"
            f"- 'end_frequency_hz': integer ({freq_range}).\n"
            "- 'sweep_duration_seconds': float (0.8 to 3.0 seconds).\n"
            f"- 'waveform_type': string (choose from: {waveform_options}).\n"
            f"- 'target_gain_db': float ({gain_range}).\n"
            "- 'rumble_reverb_decay': float (0.0 to 1.0 seconds).\n"
        )
        
        user_prompt = f"Format: {video_format.upper()}\nTarget Tempo: {target_bpm} BPM\nHeavy Impact Points:\n{json.dumps(heavy_events, indent=2)}"

        # CORE 1: Gemini
        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for DSP audio modeling...")
            try:
                model = genai.GenerativeModel("gemini-flash-latest")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("sub_profiles", [])
            except Exception as e:
                self.log(f"Gemini Engine failed: {e}. Switching to OpenAI fallback.", "WARNING")

        # CORE 2: OpenAI
        if self.openai_api_key:
            self.log(f"Routing to Core 2: OpenAI API [{self.model_cloud}]...")
            url = self.openai_url
            headers = {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_api_key}"}
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
                self.log(f"OpenAI Engine failed: {e}. Switching to Ollama Fallback.", "WARNING")

        # CORE 3: Ollama (Local Fallback)
        self.log(f"Routing to Core 3: Local Ollama [{self.model_local}]...", "STATUS")
        try:
            payload = {
                "model": self.model_local,
                "prompt": system_prompt + "\n\n" + user_prompt,
                "stream": False,
                "format": "json"
            }
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
            with urllib.request.urlopen(req, timeout=60) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                raw_text = res_data.get("response", "")
                return json.loads(self._clean_json_response(raw_text)).get("sub_profiles", [])
        except Exception as e:
            self.log(f"Ollama Engine failed: {e}. Switching to DSP Mathematical Fallback.", "WARNING")

        # CORE 4: Procedural Math Engine
        self.log("All AI Cores failed. Engaging Offline DSP Synthesizer Math.", "STATUS")
        return self._execute_procedural_fallback(heavy_events, video_format)

    def _execute_procedural_fallback(self, heavy_events, video_format):
        """UNIVERSAL MATH ENGINE for sub-bass DSP calculation."""
        profiles = []
        for trig in heavy_events:
            ts = float(trig.get("timestamp_sec", 0.0))
            intensity = float(trig.get("impact_intensity", 0.8))

            if video_format == "long_form":
                start_freq = int(50 + (intensity * 10))
                end_freq = int(20 + ((1.0 - intensity) * 5))
                decay = round(1.5 + (intensity * 1.5), 2)
                gain = round(-12.0 + (intensity * 6.0), 1)
                waveform, reverb = "pure-sine", 0.80
            else:
                start_freq = int(75 + (intensity * 25))
                end_freq = int(30 + ((1.0 - intensity) * 10))
                decay = round(0.5 + (intensity * 0.8), 2)
                gain = round(-4.0 + (intensity * 4.0), 1)
                waveform, reverb = "saturated-triangle", 0.20

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
        
        # 1. Atomic Handshake Protocol
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{orchestrator.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        # Extract Universal Config
        global_config = state.get("global_config", {})
        video_format = global_config.get("video_format", "short_form").lower()

        audio_module = state.get("module_b_audio", {})
        beat_map_data = audio_module.get("phonk_beat_map", {})
        
        if not beat_map_data:
            self.log("Beat Drop Map is missing. Run Ai_Agent_14 first.", "FATAL")
            sys.exit(1)

        bpm = beat_map_data.get("target_bpm", 130)
        all_events = beat_map_data.get("beat_sync_events", [])

        # Idempotency: Scrub existing DSP blueprints
        for event in all_events:
            event.pop("sub_bass_dsp_blueprint", None)

        # Filter heavy drops for sub-bass assignment (intensity >= 0.7)
        heavy_events = [ev for ev in all_events if ev.get("impact_intensity", 0.0) >= 0.7]
        
        if not heavy_events and all_events:
            heavy_events = [all_events[0]]  # Fallback to at least one impact

        self.log(f"Designing {video_format.upper()} low-frequency architecture for {len(heavy_events)} impact points at {bpm} BPM...", "STATUS")
        
        sub_profiles = self.fetch_sub_design_ai(bpm, heavy_events, video_format)

        # Merge the generated DSP profiles directly back into the Beat Map events in the state
        for event in all_events:
            for sub in sub_profiles:
                # Match timestamps to link the visual drop with the audio bass
                if round(event.get("timestamp_sec", 0.0), 3) == round(sub.get("timestamp_sec", 0.0), 3):
                    event["sub_bass_dsp_blueprint"] = sub
                    break
        
        state["module_b_audio"]["phonk_beat_map"]["beat_sync_events"] = all_events
        state["module_b_audio"]["sub_frequencies_mapped"] = True
        
        # 3. OmniMatrix Pipeline Handshake
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        # Handoff to next module (Agent 16)
        state["orchestrator_matrix"]["next_agent"] = "Agent_16"
        
        self._save_matrix_state(state)
        self.log("Success! Deep frequency logic merged into OmniMatrix. Handoff to Agent_16.", "SUCCESS")

if __name__ == "__main__":
    designer = AiAgent15LowFrequencySubDesigner()
    designer.process_sub_frequencies()
