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
    def __init__(self):
        self.agent_name = "Ai_Agent_14"
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
        """Loads the central OmniMatrix state safely."""
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
        """Saves the synchronized beat map back to the state file idempotently."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4, ensure_ascii=False)
        self.log("OmniMatrix state successfully updated with Cinematic/Phonk Beat-Drop topology.", "SUCCESS")

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

    def analyze_beats_ai(self, master_duration, timeline_data, video_format, target_bpm):
        """
        UNIVERSAL AI LOGIC CORE:
        Adapts completely whether the format is a fast-paced Short or a cinematic Long-Form video.
        """
        
        # Adaptive Prompting based on Universal Format
        if video_format == "long_form":
            editing_style = "Cinematic, Lo-fi, and Documentary style."
            event_types = "'scene-fade-transition', 'soft-sub-bass-zoom', 'emotional-chapter-marker'"
            frequency_rule = "Generate impactful visual triggers sparingly (every 10-15 seconds) aligning with scene changes or long pauses in voiceover."
        else:
            editing_style = "Aggressive Drift Phonk, House, and Dark Synth music (Short-Form / Reels)."
            event_types = "'bass-drop-flash', 'cowbell-roll-glitch', 'sub-bass-zoom', 'snare-shake'"
            frequency_rule = "Generate high-frequency visual FX cues constantly (every 2-4 seconds) to retain short-attention-span viewers."

        system_prompt = (
            f"You are an elite video editing AI director specialized in {editing_style} "
            f"Generate visual FX cues based on the video timing boundaries and a baseline of {target_bpm} BPM.\n"
            f"RULE: {frequency_rule}\n"
            "Return STRICTLY a JSON object containing a list named 'beat_sync_events'.\n"
            "Every event must have these exact parameters:\n"
            "- 'timestamp_sec': float (must be strictly between 0.0 and total duration).\n"
            f"- 'event_type': string (choose from: {event_types}).\n"
            "- 'impact_intensity': float (0.1 to 1.0).\n"
            "- 'editor_action_note': string instruction detailing the VFX.\n"
        )
        
        user_prompt = (
            f"Format: {video_format.upper()}\n"
            f"Target BPM: {target_bpm}\n"
            f"Total Video Duration: {master_duration} seconds.\n"
            f"Core Audio/Visual Timeline Details:\n{json.dumps(timeline_data, indent=2)}"
        )

        # CORE 1: Gemini (Highest Speed & Context)
        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for beat sync mapping...")
            try:
                model = genai.GenerativeModel("gemini-flash-latest")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("beat_sync_events", [])
            except Exception as e:
                self.log(f"Gemini Engine failed: {e}. Switching to OpenAI fallback.", "WARNING")

        # CORE 2: OpenAI (gpt-4o-mini)
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
                    return json.loads(self._clean_json_response(raw_text)).get("beat_sync_events", [])
            except Exception as e:
                self.log(f"OpenAI Engine failed: {e}. Switching to Ollama Local Fallback.", "WARNING")

        # CORE 3: Ollama (Local LLM Fallback)
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
                return json.loads(self._clean_json_response(raw_text)).get("beat_sync_events", [])
        except Exception as e:
            self.log(f"Ollama Engine failed: {e}. Switching to Procedural Math Engine.", "WARNING")

        # CORE 4: Procedural Math Engine (Ultimate Fallback)
        self.log("All AI Cores failed. Engaging Offline Mathematical Beat-Drop Generator.", "STATUS")
        return self._execute_procedural_fallback(master_duration, video_format, target_bpm)

    def _execute_procedural_fallback(self, master_duration, video_format, target_bpm):
        """
        UNIVERSAL MATH ENGINE: Calculates structural beats mathematically.
        Adapts density of visual effects based on whether it's Long-Form or Short-Form.
        """
        beat_interval = 60.0 / target_bpm
        events = []
        current_time = 0.0
        beat_counter = 1

        # Configuration for format intensity
        if video_format == "long_form":
            peak_bar = 32  # Major transition every 32 beats
            mid_bar = 16   # Minor zoom every 16 beats
        else:
            peak_bar = 8   # Screen-shatter every 8 beats
            mid_bar = 4    # Glitch every 4 beats

        while current_time < master_duration:
            is_peak = (beat_counter % peak_bar == 0)
            is_mid = (beat_counter % mid_bar == 0)

            if is_peak:
                if video_format == "long_form":
                    event_type, intensity, note = "scene-fade-transition", 0.80, "Smooth crossfade or slow zoom-in on subject."
                else:
                    event_type, intensity, note = "bass-drop-flash", 0.95, "Extreme screen-shattering flash + heavy zoom out."
                
                events.append({
                    "timestamp_sec": round(current_time, 3),
                    "event_type": event_type,
                    "impact_intensity": intensity,
                    "editor_action_note": note
                })

            elif is_mid:
                if video_format == "long_form":
                    event_type, intensity, note = "soft-sub-bass-zoom", 0.40, "Subtle 105% scale punch-in for focus."
                else:
                    event_type, intensity, note = "cowbell-roll-glitch", 0.75, "Triple-split glitch effect + rapid color shake."
                
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
        
        # 1. Atomic Handshake Protocol
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{orchestrator.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        # 2. Extract Universal Configuration
        global_config = state.get("global_config", {})
        video_format = global_config.get("video_format", "short_form").lower() # 'long_form' or 'short_form'
        
        # Determine BPM based on format
        if video_format == "long_form":
            target_bpm = global_config.get("audio_settings", {}).get("long_form_bpm", 100)
            self.log(f"Long-Form mode detected. Setting Cinematic Tempo: {target_bpm} BPM.")
        else:
            target_bpm = global_config.get("audio_settings", {}).get("short_form_bpm", 130)
            self.log(f"Short-Form mode detected. Setting Phonk/Drift Tempo: {target_bpm} BPM.")

        audio_module = state.get("module_b_audio", {})
        master_metrics = audio_module.get("master_timeline_metrics", {})
        total_duration = master_metrics.get("total_video_duration_sec", 0.0)
        
        if total_duration == 0.0:
            self.log("Master video duration missing. Ensure Agent 12 (Timestamps) ran successfully.", "FATAL")
            sys.exit(1)

        # Idempotency Scrubbing
        if "phonk_beat_map" in audio_module:
            del audio_module["phonk_beat_map"]

        audio_timeline = audio_module.get("audio_timeline", [])
        
        # Prepare lightweight data for the LLM to save tokens and prevent context-overflow
        lightweight_timeline = [
            {"frame": f.get("frame_index"), "timing": f.get("global_timing")}
            for f in audio_timeline
        ]

        self.log(f"Designing Adaptive visual choreography for {total_duration}s video timeline...", "STATUS")
        
        ai_beat_events = self.analyze_beats_ai(total_duration, lightweight_timeline, video_format, target_bpm)

        # Inject beat mapping data into OmniMatrix
        state["module_b_audio"]["phonk_beat_map"] = {
            "video_format": video_format,
            "target_bpm": target_bpm,
            "total_beat_events": len(ai_beat_events),
            "beat_sync_events": ai_beat_events
        }
        
        # 3. OmniMatrix Pipeline Handshake
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        # Heading towards VFX or Final Compositing module
        state["orchestrator_matrix"]["next_agent"] = "Ai_Agent_15" 
        
        self._save_matrix_state(state)
        self.log(f"Success! {len(ai_beat_events)} adaptive visual impact triggers mapped. Ready for handoff to Agent 15.")

if __name__ == "__main__":
    analyzer = AiAgent14PhonkBeatDropAnalyzer()
    analyzer.generate_beat_map()
