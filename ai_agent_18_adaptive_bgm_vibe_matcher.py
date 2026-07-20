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


class AiAgent18AdaptiveBgmVibeMatcher:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 18: adaptive_bgm_vibe_matcher"
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
        """Saves the BGM automation blueprint back to the central state."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("OmniMatrix state successfully updated with BGM Automation Curves.")

    def _clean_json_response(self, raw_text):
        """Strips markdown and extracts pure JSON string."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def fetch_bgm_automation_ai(self, narrative_cues):
        """Uses AI logic cores to design cinematic music automation maps."""
        system_prompt = (
            "You are a cinematic music supervisor and dynamic video editor. "
            "Analyze video narration emotional curves and build dynamic volume/genre automation parameters for the Background Music (BGM).\n"
            "Return STRICTLY a JSON object containing a list named 'bgm_automation_segments'.\n"
            "Each segment must contain:\n"
            "- 'start_sec': float matching the narration block start.\n"
            "- 'end_sec': float matching the narration block end.\n"
            "- 'bgm_vibe_style': string (choose from: 'dark-ambient-pad', 'aggressive-phonk-drill', 'cyberpunk-chiptune', 'orchestral-epic-riser').\n"
            "- 'target_bgm_volume_db': float (-24.0 dB for talking/focus, up to -6.0 dB during action/silence).\n"
            "- 'filter_cutoff_hz': integer (400-20000 Hz. Use ~800 Hz to muffle music during intense dialogue).\n"
            "- 'tempo_multiplier': float (0.75, 1.0, 1.25).\n"
            "- 'vibe_shift_note': string explaining the musical transition logic.\n"
        )
        
        user_prompt = f"Vocal Narrative Flow:\n{json.dumps(narrative_cues, indent=2)}"

        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for BGM automation mapping...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("bgm_automation_segments", [])
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
                    return json.loads(self._clean_json_response(raw_text)).get("bgm_automation_segments", [])
            except Exception as e:
                self.log(f"OpenAI Engine failed: {e}. Engaging Offline Math Logic.", "WARNING")

        self.log("All AI API Cores failed. Engaging Offline Procedural Vibe Mapper.", "STATUS")
        return self._execute_procedural_fallback(narrative_cues)

    def _execute_procedural_fallback(self, cues):
        """Mathematical fallback for BGM adjustments without LLM."""
        segments = []
        for cue in cues:
            start = float(cue.get("start_sec", 0.0))
            end = float(cue.get("end_sec", 3.0))
            tone = cue.get("emotional_tone", "neutral").lower()

            if "dark" in tone or "sad" in tone:
                style, vol, cutoff, mult, note = "dark-ambient-pad", -20.0, 1200, 0.75, "Low-pass filtered pad for tense atmosphere."
            elif "high" in tone or "rage" in tone or "action" in tone:
                style, vol, cutoff, mult, note = "aggressive-phonk-drill", -10.0, 20000, 1.25, "Energy spike. Unfiltered heavy beat."
            elif "epic" in tone or "climax" in tone:
                style, vol, cutoff, mult, note = "orchestral-epic-riser", -8.0, 18000, 1.0, "High intensity build up."
            else:
                style, vol, cutoff, mult, note = "cyberpunk-chiptune", -16.0, 5000, 1.0, "Standard mid-tempo background volume."

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
        
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent and target_agent != "Ai_Agent_18":
            self.log(f"Pipeline sequence mismatch. Expected {target_agent}, but executing {self.agent_name}.", "WARNING")

        # Fetch Voiceover Timeline from Module B or Visual Storyboard from Module A
        audio_module = state.get("module_b_audio", {})
        voiceover_timeline = audio_module.get("audio_timeline", [])
        
        narrative_cues = []
        
        # Method 1: Extract from active audio timeline
        if voiceover_timeline:
            for block in voiceover_timeline:
                narrative_cues.append({
                    "start_sec": block.get("global_timing", {}).get("start_sec", 0.0),
                    "end_sec": block.get("global_timing", {}).get("end_sec", 3.0),
                    "emotional_tone": block.get("emotion", "neutral"),
                    "text_context": block.get("dialogue_text", "")
                })
        else:
            self.log("Voiceover timeline not found. Searching for Module A Storyboard cues...", "WARNING")
            storyboard = state.get("module_a_scripting", {}).get("storyboard_mapping", {})
            if storyboard:
                for idx, panel in enumerate(storyboard.get("panels", [])):
                    narrative_cues.append({
                        "start_sec": panel.get("timestamp_sec", float(idx * 3.0)),
                        "end_sec": panel.get("timestamp_sec", float(idx * 3.0)) + 3.0,
                        "emotional_tone": "epic-climax" if "fight" in panel.get("prompt", "").lower() else "neutral",
                        "text_context": panel.get("prompt", "")
                    })

        # Final Fallback
        if not narrative_cues:
            self.log("No upstream data found. Using default timeline structure.", "WARNING")
            narrative_cues = [
                {"start_sec": 0.0, "end_sec": 3.0, "emotional_tone": "dark-suspense", "text_context": "Introduction"}
            ]

        self.log(f"Vibe Engine active. Generating BGM automation curves for {len(narrative_cues)} segments...")
        
        bgm_automation_map = self.fetch_bgm_automation_ai(narrative_cues)

        state["module_b_audio"]["bgm_automation_map"] = {
            "total_segments": len(bgm_automation_map),
            "automation_curves": bgm_automation_map
        }
        
        # Pipeline Handshake
        state["pipeline_status"]["last_active_agent"] = "Ai_Agent_18"
        state["pipeline_status"]["next_agent"] = "Ai_Agent_19"
        
        self._save_matrix_state(state)
        self.log("Success! Adaptive BGM parameters mapped into OmniMatrix. Handoff to Agent 19.")

if __name__ == "__main__":
    matcher = AiAgent18AdaptiveBgmVibeMatcher()
    matcher.process_bgm_vibe_automation()
    print("\n--- OMNIMATRIX MODULE B: AGENT 18 COMPLETE ---")
