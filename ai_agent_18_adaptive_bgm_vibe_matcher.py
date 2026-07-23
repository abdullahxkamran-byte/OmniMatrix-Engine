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


class AiAgent18AdaptiveBgmVibeMatcher:
    def __init__(self):
        self.agent_name = "Ai_Agent_18"
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
        self.log("OmniMatrix state successfully updated with Limitless BGM Automation Curves.", "SUCCESS")

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

    def fetch_bgm_automation_ai(self, narrative_cues, video_format, global_theme):
        """
        LIMITLESS AI LOGIC CORE:
        No hardcoded genres. The AI invents the exact BGM style needed based on the theme and format.
        """
        system_prompt = (
            "You are a limitless cinematic music supervisor and audio automation engineer. "
            f"The current project format is '{video_format}' and the overall theme is '{global_theme}'.\n"
            "Analyze the narrative emotional curves and build dynamic volume/genre automation parameters for the Background Music (BGM).\n"
            "DO NOT RESTRICT YOURSELF TO PRESETS. Invent the perfect music sub-genre descriptor for each segment.\n"
            "Return STRICTLY a JSON object containing a list named 'bgm_automation_segments'.\n"
            "Each segment must contain:\n"
            "- 'start_sec': float matching the narration block start.\n"
            "- 'end_sec': float matching the narration block end.\n"
            "- 'bgm_vibe_style': string (Invent a highly descriptive hyphenated genre, e.g., 'dark-synthwave-pulse', 'acoustic-nostalgic-strum', 'orchestral-combat-choir').\n"
            "- 'target_bgm_volume_db': float (-30.0 dB for heavy dialogue, up to -5.0 dB for pure musical montage/silence).\n"
            "- 'filter_cutoff_hz': integer (Range 300 to 20000 Hz. Use low-pass ~800Hz to muffle BGM during talking, 20000Hz for full clarity).\n"
            "- 'tempo_multiplier': float (0.5 to 2.0. Base is 1.0).\n"
            "- 'vibe_shift_note': string explaining why this specific musical shift is happening.\n"
        )
        
        user_prompt = f"Vocal Narrative & Action Flow:\n{json.dumps(narrative_cues, indent=2)}"

        # CORE 1: Gemini
        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for Limitless BGM mapping...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("bgm_automation_segments", [])
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
                    return json.loads(self._clean_json_response(raw_text)).get("bgm_automation_segments", [])
            except Exception as e:
                self.log(f"OpenAI Engine failed: {e}. Engaging Ollama Local Core.", "WARNING")

        # CORE 3: Ollama (Local Limitless Engine)
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
                return json.loads(self._clean_json_response(raw_text)).get("bgm_automation_segments", [])
        except Exception as e:
            self.log(f"Ollama Engine failed: {e}. Engaging Procedural Math Fallback.", "WARNING")

        # CORE 4: Procedural Limitless Fallback
        self.log("All AI API Cores failed. Engaging Offline Procedural Limitless Mapper.", "STATUS")
        return self._execute_procedural_fallback(narrative_cues, video_format, global_theme)

    def _execute_procedural_fallback(self, cues, video_format, global_theme):
        """Mathematical fallback that still attempts to be limitless by using the text cues."""
        segments = []
        for cue in cues:
            start = float(cue.get("start_sec", 0.0))
            end = float(cue.get("end_sec", 3.0))
            tone = str(cue.get("emotional_tone", "neutral")).lower()
            context = str(cue.get("text_context", "")).lower()

            # Dynamic naming instead of hardcoded lists
            clean_tone = re.sub(r'[^a-z]+', '-', tone)
            clean_theme = re.sub(r'[^a-z]+', '-', str(global_theme).lower()[:10])
            
            style = f"{clean_theme}-{clean_tone}-background"
            
            # Procedural DSP rules
            if any(x in tone or x in context for x in ["sad", "dark", "quiet", "tense"]):
                vol, cutoff, mult, note = -24.0, 800, 0.8, "Muffled low-pass for tension/sadness."
            elif any(x in tone or x in context for x in ["hype", "action", "epic", "fight"]):
                vol, cutoff, mult, note = -8.0, 20000, 1.2, "Unfiltered high energy spike."
                style = f"aggressive-{style}"
            else:
                vol, cutoff, mult, note = -18.0, 10000, 1.0, "Standard dialogue backing track."

            segments.append({
                "start_sec": start,
                "end_sec": end,
                "bgm_vibe_style": style,
                "target_bgm_volume_db": vol,
                "filter_cutoff_hz": cutoff,
                "tempo_multiplier": mult,
                "vibe_shift_note": note
            })
        return segments

    def process_bgm_vibe_automation(self):
        state = self._load_matrix_state()
        
        # 1. Atomic Handshake Protocol
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{orchestrator.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        # 2. Extract Limitless Configuration Parameters
        global_config = state.get("global_config", {})
        video_format = global_config.get("video_format", "undefined_format")
        global_theme = global_config.get("theme", "neutral_unspecified")

        # Idempotency: Scrub old BGM map
        audio_module = state.get("module_b_audio", {})
        if "bgm_automation_map" in audio_module:
            del audio_module["bgm_automation_map"]

        voiceover_timeline = audio_module.get("audio_timeline", [])
        narrative_cues = []
        
        # Method 1: Extract from active audio timeline
        if voiceover_timeline:
            for block in voiceover_timeline:
                narrative_cues.append({
                    "start_sec": block.get("global_timing", {}).get("start_sec", 0.0),
                    "end_sec": block.get("global_timing", {}).get("end_sec", 3.0),
                    "emotional_tone": block.get("emotion", "neutral"),
                    "text_context": block.get("dialogue_text", "instrumental/pause")
                })
        else:
            self.log("Voiceover timeline not found. Searching for Module A Storyboard cues...", "WARNING")
            storyboard = state.get("module_a_scripting", {}).get("storyboard_mapping", {})
            if storyboard:
                for idx, panel in enumerate(storyboard.get("panels", [])):
                    narrative_cues.append({
                        "start_sec": panel.get("timestamp_sec", float(idx * 3.0)),
                        "end_sec": panel.get("timestamp_sec", float(idx * 3.0)) + 3.0,
                        "emotional_tone": "high_intensity" if "fight" in panel.get("prompt", "").lower() else "neutral",
                        "text_context": panel.get("prompt", "visual action")
                    })

        if not narrative_cues:
            self.log("No upstream data found. Generating fallback limitless baseline.", "WARNING")
            narrative_cues = [
                {"start_sec": 0.0, "end_sec": 10.0, "emotional_tone": "introductory", "text_context": "Introduction"}
            ]

        self.log(f"Limitless Vibe Engine active. Generating BGM automation for {video_format} ({global_theme})...", "STATUS")
        
        bgm_automation_map = self.fetch_bgm_automation_ai(narrative_cues, video_format, global_theme)

        state["module_b_audio"]["bgm_automation_map"] = {
            "total_segments": len(bgm_automation_map),
            "video_format": video_format,
            "global_theme": global_theme,
            "automation_curves": bgm_automation_map
        }
        
        # 3. OmniMatrix Pipeline Handshake
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        # Heading towards the Final Audio Compiler/Mixer
        state["orchestrator_matrix"]["next_agent"] = "Ai_Agent_19"
        
        self._save_matrix_state(state)
        self.log(f"Success! {len(bgm_automation_map)} limitless BGM parameters mapped into OmniMatrix. Handoff to Ai_Agent_19.", "SUCCESS")

if __name__ == "__main__":
    matcher = AiAgent18AdaptiveBgmVibeMatcher()
    matcher.process_bgm_vibe_automation()
