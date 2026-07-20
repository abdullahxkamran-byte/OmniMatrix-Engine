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


class AiAgent19AudioMasteringFinalMixer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 19: audio_mastering_final_mixer"
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
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run upstream modules first.", "ERROR")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("OmniMatrix state successfully updated with Final Audio Mastering Blueprint.")

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

    def fetch_mastering_ai(self, audio_signals_summary):
        """Uses AI logic cores to design professional mastering chains."""
        system_prompt = (
            "You are a legendary audio mastering engineer specialized in optimizing high-energy videos for mobile platforms (TikTok/Shorts).\n"
            "Analyze the compiled audio components and output final mixing/mastering console settings to achieve maximum punch without distortion.\n"
            "Return STRICTLY a JSON object containing the mastering parameters with these keys:\n"
            "- 'target_loudness_lufs': float (choose between -11.0 and -7.0 LUFS for competitive mobile standards).\n"
            "- 'master_true_peak_limiter_db': float (-1.0 to -0.1 dB to prevent clipping during platform compression).\n"
            "- 'stereo_widening_factor': float (1.0 to 1.5; widens BGM/SFX while keeping voice central).\n"
            "- 'low_cut_filter_hz': integer (20 to 40 Hz to remove sub-harmonic mud).\n"
            "- 'vocal_presence_boost_db': float (1.0 to 4.0 dB boost in the 2kHz-4kHz range for clarity).\n"
            "- 'glue_compressor_settings': object containing 'threshold_db' (float, -2.0 to -6.0), 'ratio' (string, '1.5:1' or '2:1'), and 'makeup_gain_db' (float).\n"
        )
        
        user_prompt = f"Active Audio Elements in Mix:\n{json.dumps(audio_signals_summary, indent=2)}"

        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for Mastering Console Logic...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip())
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
                    return json.loads(self._clean_json_response(raw_text))
            except Exception as e:
                self.log(f"OpenAI Engine failed: {e}. Engaging Offline Math Mastering.", "WARNING")

        self.log("All AI API Cores failed. Engaging Procedural Fallback Mastering.", "STATUS")
        return self._execute_procedural_fallback()

    def _execute_procedural_fallback(self):
        """Mathematical fallback for industry standard mastering limits."""
        return {
            "target_loudness_lufs": -9.0,
            "master_true_peak_limiter_db": -0.5,
            "stereo_widening_factor": 1.3,
            "low_cut_filter_hz": 30,
            "vocal_presence_boost_db": 2.0,
            "glue_compressor_settings": {
                "threshold_db": -4.0,
                "ratio": "2:1",
                "makeup_gain_db": 2.0
            }
        }

    def process_final_mix(self):
        state = self._load_matrix_state()
        
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent and target_agent != "Ai_Agent_19":
            self.log(f"Pipeline sequence mismatch. Expected {target_agent}, but executing {self.agent_name}.", "WARNING")

        audio_module = state.get("module_b_audio", {})
        
        # Compile a summary of all active audio layers for the AI to analyze
        audio_signals_summary = {
            "has_sidechain_ducking": audio_module.get("sidechain_compression_applied", False),
            "total_sfx_layers": len(audio_module.get("sfx_synthesizer_blueprints", [])),
            "bgm_automation_active": "bgm_automation_map" in audio_module,
            "voiceover_tracks_count": len(audio_module.get("audio_timeline", [])),
            "beat_drops_count": len(audio_module.get("phonk_beat_map", {}).get("beat_sync_events", []))
        }

        self.log("Mastering Console active. Calculating global loudness, True Peak, and EQ curves...")
        
        mastering_parameters = self.fetch_mastering_ai(audio_signals_summary)

        state["module_b_audio"]["final_mastering_blueprint"] = {
            "signal_summary_used": audio_signals_summary,
            "mastering_parameters": mastering_parameters
        }
        
        # Pipeline Handshake - Handoff to Agent 20 (Audio Renderer / Next Module)
        state["pipeline_status"]["last_active_agent"] = "Ai_Agent_19"
        state["pipeline_status"]["next_agent"] = "Agent_20"
        
        self._save_matrix_state(state)
        self.log("Success! Final mastering parameters locked into OmniMatrix. Module B Audio logic is fully compiled.")

if __name__ == "__main__":
    mixer = AiAgent19AudioMasteringFinalMixer()
    mixer.process_final_mix()
    print("\n--- OMNIMATRIX MODULE B: AGENT 19 MASTER COMPLETE ---")
