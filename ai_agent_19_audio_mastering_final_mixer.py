import os
import sys
import json
import re
import urllib.request
import urllib.parse

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
    def __init__(self):
        self.agent_name = "Ai_Agent_19"
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
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4, ensure_ascii=False)
        self.log("OmniMatrix state successfully updated with AI Audio Mastering Blueprint.", "SUCCESS")

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

    def _scrub_old_mastering(self, state):
        """Idempotency Rule: Cleans previous mastering data."""
        if "final_mastering_blueprint" in state.get("module_b_audio", {}):
            del state["module_b_audio"]["final_mastering_blueprint"]
        return state

    def fetch_mastering_ai(self, audio_signals_summary, video_format, global_theme):
        """
        LIMITLESS AI CORE: 
        Analyzes the theme and format to creatively design a mixing console blueprint.
        An AI understands that an 'Epic Battle' needs heavy compression, while 'Sad Lore' needs dynamic breathing room.
        """
        
        # Give the AI technical boundaries based on the limitless format
        if "short" in video_format.lower() or "tiktok" in video_format.lower() or "reel" in video_format.lower():
            lufs_guide = "-10.0 to -8.0 LUFS (Maximum punch, competitive loudness for phones)"
            widening_guide = "1.1 to 1.25 (Slight width, but must maintain mono-compatibility)"
        elif "cinema" in video_format.lower() or "documentary" in video_format.lower():
            lufs_guide = "-23.0 to -18.0 LUFS (High dynamic range, theatrical standard)"
            widening_guide = "1.3 to 1.5 (Very wide theatrical stereo spread)"
        else:
            lufs_guide = "-15.0 to -13.0 LUFS (Standard streaming/YouTube sweet spot)"
            widening_guide = "1.1 to 1.3 (Balanced stereo image)"

        system_prompt = (
            "You are an elite, AI-driven audio mastering engineer. "
            f"The video format is '{video_format}' and the emotional theme is '{global_theme}'.\n"
            "Analyze the active audio elements and design a professional mastering chain that perfectly fits the emotional tone and platform standard.\n"
            "Return STRICTLY a JSON object containing the mastering parameters with these exact keys:\n"
            f"- 'target_loudness_lufs': float (Platform guide: {lufs_guide}).\n"
            "- 'master_true_peak_limiter_db': float (-2.0 to -0.1 dB to prevent digital clipping).\n"
            f"- 'stereo_widening_factor': float ({widening_guide}).\n"
            "- 'low_cut_filter_hz': integer (20 to 50 Hz. Cut more if it's mobile to remove muddy rumble, cut less for cinema to keep sub-bass).\n"
            "- 'vocal_presence_boost_db': float (0.5 to 4.0 dB boost in the 3kHz range. Boost higher if BGM/SFX layers are dense).\n"
            "- 'glue_compressor_settings': object containing 'threshold_db' (float, e.g. -6.0 to -2.0), 'ratio' (float, e.g. 1.5, 2.0, 3.0), and 'makeup_gain_db' (float).\n"
            "- 'ai_mastering_notes': string (Briefly explain your creative mastering choices for this specific theme).\n"
        )
        
        user_prompt = f"Active Audio Elements in Mix:\n{json.dumps(audio_signals_summary, indent=2)}"

        # CORE 1: Gemini
        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for Creative Mastering Console Logic...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip())
            except Exception as e:
                self.log(f"Gemini Engine failed: {e}. Switching to OpenAI fallback.", "WARNING")

        # CORE 2: OpenAI
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
                self.log(f"OpenAI Engine failed: {e}. Engaging Ollama Local Core.", "WARNING")

        # CORE 3: Ollama
        self.log(f"Routing to Core 3: Local Ollama [{self.model_local}]...", "STATUS")
        try:
            payload = {
                "model": self.model_local,
                "prompt": system_prompt + "\n\n" + user_prompt,
                "stream": False,
                "format": "json"
            }
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                raw_text = res_data.get("response", "")
                return json.loads(self._clean_json_response(raw_text))
        except Exception as e:
            self.log(f"Ollama Engine failed: {e}. Engaging Procedural Math Mastering.", "WARNING")

        # CORE 4: Procedural Fallback
        self.log("All AI API Cores failed. Engaging Procedural Fallback Mastering.", "STATUS")
        return self._execute_procedural_fallback(video_format)

    def _execute_procedural_fallback(self, video_format):
        """Mathematical fallback if AI is completely unavailable."""
        if "short" in video_format.lower() or "tiktok" in video_format.lower():
            lufs, peak, low_cut, widen = -9.0, -0.2, 35, 1.15
        elif "cinema" in video_format.lower():
            lufs, peak, low_cut, widen = -23.0, -2.0, 20, 1.4
        else:
            lufs, peak, low_cut, widen = -14.0, -1.0, 30, 1.1

        return {
            "target_loudness_lufs": lufs,
            "master_true_peak_limiter_db": peak,
            "stereo_widening_factor": widen,
            "low_cut_filter_hz": low_cut,
            "vocal_presence_boost_db": 2.0,
            "glue_compressor_settings": {
                "threshold_db": -4.0,
                "ratio": 2.0,
                "makeup_gain_db": 1.5
            },
            "ai_mastering_notes": "Procedural fallback applied. Standard mathematical limits used."
        }

    def _generate_ffmpeg_mastering_chain(self, params):
        """
        Converts the AI's creative mastering parameters into a highly actionable
        FFmpeg audio filter string (afilter).
        """
        hz = int(params.get("low_cut_filter_hz", 30))
        widen = float(params.get("stereo_widening_factor", 1.0))
        vocal_boost = float(params.get("vocal_presence_boost_db", 0.0))
        
        comp = params.get("glue_compressor_settings", {})
        c_thresh = float(comp.get("threshold_db", -5.0))
        c_ratio = float(comp.get("ratio", 2.0))
        c_makeup = float(comp.get("makeup_gain_db", 0.0))
        
        lufs = float(params.get("target_loudness_lufs", -14.0))
        peak = float(params.get("master_true_peak_limiter_db", -1.0))

        # Build FFmpeg audio filter chain
        af_highpass = f"highpass=f={hz}"
        af_eq = f"equalizer=f=3000:width_type=h:width=200:g={vocal_boost}"
        af_stereo = f"extrastereo=m={widen}"
        af_comp = f"acompressor=threshold={c_thresh}dB:ratio={c_ratio}:makeup={c_makeup}dB:attack=5:release=50"
        af_loudnorm = f"loudnorm=I={lufs}:TP={peak}:LRA=11"

        return f"{af_highpass},{af_eq},{af_stereo},{af_comp},{af_loudnorm}"

    def process_final_mix(self):
        state = self._load_matrix_state()
        
        # 1. Atomic Handshake Protocol
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{orchestrator.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        # 2. Extract Context
        global_config = state.get("global_config", {})
        video_format = global_config.get("video_format", "undefined_format")
        global_theme = global_config.get("theme", "neutral_unspecified")

        # Idempotency
        state = self._scrub_old_mastering(state)
        
        audio_module = state.get("module_b_audio", {})
        
        # Contextual summary for the AI
        audio_signals_summary = {
            "has_sidechain_ducking": audio_module.get("sidechain_compression_applied", False),
            "total_sfx_layers": len(audio_module.get("sfx_synthesizer_blueprints", [])),
            "bgm_automation_active": "bgm_automation_map" in audio_module,
            "custom_ost_tracks_count": len(audio_module.get("custom_neural_ost_tracks", [])),
            "voiceover_tracks_count": len(audio_module.get("audio_timeline", [])),
            "beat_drops_count": len(audio_module.get("phonk_beat_map", {}).get("beat_sync_events", []))
        }

        self.log(f"AI Mastering Console active. Designing DSP blueprint for '{global_theme}' in '{video_format}' format...", "STATUS")
        
        # Call the AI Engine
        mastering_parameters = self.fetch_mastering_ai(audio_signals_summary, video_format, global_theme)
        
        if "ai_mastering_notes" in mastering_parameters:
            self.log(f"AI Note: {mastering_parameters['ai_mastering_notes']}", "SUCCESS")

        self.log("Converting AI parameters into FFmpeg executable string...")
        actionable_ffmpeg_filter = self._generate_ffmpeg_mastering_chain(mastering_parameters)

        state["module_b_audio"]["final_mastering_blueprint"] = {
            "signal_summary_used": audio_signals_summary,
            "mastering_parameters": mastering_parameters,
            "executable_ffmpeg_afilter": actionable_ffmpeg_filter
        }
        
        # 3. OmniMatrix Pipeline Handshake
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        
        # Since the list is outdated, we route to a generic "Pending Agent 20" until you define it
        state["orchestrator_matrix"]["next_agent"] = "Agent_20_Pending"
        
        self._save_matrix_state(state)
        self.log(f"Ready FFmpeg Command: {actionable_ffmpeg_filter}")
        self.log("--- MODULE B (AUDIO) IS 100% COMPLETE. READY FOR NEXT MODULE ---", "SUCCESS")

if __name__ == "__main__":
    mixer = AiAgent19AudioMasteringFinalMixer()
    mixer.process_final_mix()
