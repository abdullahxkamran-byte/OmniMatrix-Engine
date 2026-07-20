
import os
import sys
import json
import re
import urllib.request
import urllib.error

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


class AiAgent10AudioToneEmotionMatcher:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 10: Audio Tone Emotion Matcher"
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
        """Loads the central OmniMatrix state."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run Module A and Agent 09 first.", "ERROR")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        """Updates the central OmniMatrix state with new emotional audio mappings."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("Matrix state successfully updated with Audio Emotion Metadata.")

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

    def fetch_ai_mappings(self, tracks):
        """Queries the AI logic cores to determine pitch, reverb, and EQ for each audio track."""
        system_prompt = (
            "You are an expert cinematic audio mixing engineer for a dark phonk and anime-style video production. "
            "Analyze the voiceover script and match each frame with precise audio processing effects.\n"
            "Return STRICTLY a JSON object containing a list named 'emotion_mappings'.\n"
            "Parameters required per frame:\n"
            "- 'frame_index': integer.\n"
            "- 'character': string.\n"
            "- 'tone_category': choose from ('whisper-menace', 'screaming-rage', 'cold-assertive', 'hype-buildup', 'cosmic-vibration').\n"
            "- 'pitch_shift_semitones': integer (-4 to +2).\n"
            "- 'delivery_speed_multiplier': float (0.85 to 1.15).\n"
            "- 'reverb_mix': float (0.0 to 0.60).\n"
            "- 'eq_preset': choose from ('heavy-bass-boost', 'radio-vocal-mid', 'crisp-air-treble').\n"
        )
        
        user_prompt = "Audio Tracks Metadata:\n" + json.dumps(tracks, indent=2)

        # 1st Priority: Gemini AI (Fastest and highly capable for JSON logic)
        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Querying Core 1: Gemini AI for audio emotion mapping...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("emotion_mappings", [])
            except Exception as e:
                self.log(f"Gemini Engine failed: {e}. Switching to OpenAI fallback.", "WARNING")

        # 2nd Priority: OpenAI (GPT-4o-mini)
        if self.openai_api_key:
            self.log(f"Querying Core 2: OpenAI API [{self.model_cloud}]...")
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
                    return json.loads(self._clean_json_response(raw_text)).get("emotion_mappings", [])
            except Exception as e:
                self.log(f"OpenAI Engine failed: {e}. Switching to Ollama/Procedural.", "WARNING")

        # Fallback: Procedural Logic (If internet is down or keys are missing)
        self.log("All AI API Cores failed or keys absent. Using Offline Procedural Logic Engine.", "STATUS")
        return self._execute_procedural_fallback(tracks)

    def _execute_procedural_fallback(self, tracks):
        """Offline safety matrix for procedural cinematic audio mapping."""
        mappings = []
        total = len(tracks) if tracks else 1

        for idx, track in enumerate(tracks):
            frame_idx = track.get("frame_index", idx + 1)
            char_name = track.get("character", "Unknown").lower()
            progression = (idx + 1) / total

            # Analyze character archetype or timeline progression for audio styling
            if "gojo" in char_name or "hero" in char_name:
                tone, pitch, speed, reverb, eq = "cold-assertive", 0, 1.0, 0.15, "crisp-air-treble"
            elif "sukuna" in char_name or "villain" in char_name:
                tone, pitch, speed, reverb, eq = "screaming-rage", -3, 1.05, 0.45, "heavy-bass-boost"
            elif progression < 0.3:
                tone, pitch, speed, reverb, eq = "whisper-menace", -1, 0.95, 0.30, "radio-vocal-mid"
            else:
                tone, pitch, speed, reverb, eq = "hype-buildup", +1, 1.10, 0.20, "crisp-air-treble"

            mappings.append({
                "frame_index": frame_idx,
                "character": track.get("character", "Unknown"),
                "tone_category": tone,
                "pitch_shift_semitones": pitch,
                "delivery_speed_multiplier": speed,
                "reverb_mix": reverb,
                "eq_preset": eq
            })

        return mappings

    def process_emotions(self):
        state = self._load_matrix_state()
        audio_module = state.get("module_b_audio", {})
        audio_timeline = audio_module.get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("No audio timeline found. Run Agent 09 first.", "ERROR")
            return

        self.log(f"Analyzing psychology and tone matrix for {len(audio_timeline)} audio tracks...")
        
        # Prepare lightweight dataset for the AI prompt to save tokens
        lightweight_tracks = [
            {"frame_index": t.get("frame_index"), "character": t.get("character"), "spoken_voiceover": t.get("spoken_voiceover")} 
            for t in audio_timeline
        ]
        
        ai_mappings = self.fetch_ai_mappings(lightweight_tracks)

        # Merge the generated emotional logic back into the master state
        for frame in audio_timeline:
            for mapping in ai_mappings:
                if frame.get("frame_index") == mapping.get("frame_index"):
                    frame["audio_effects_processing"] = {
                        "tone_category": mapping.get("tone_category", "neutral"),
                        "pitch_shift_semitones": mapping.get("pitch_shift_semitones", 0),
                        "delivery_speed_multiplier": mapping.get("delivery_speed_multiplier", 1.0),
                        "reverb_mix": mapping.get("reverb_mix", 0.0),
                        "eq_preset": mapping.get("eq_preset", "standard")
                    }
                    break
        
        state["module_b_audio"]["emotions_mapped"] = True
        state["module_b_audio"]["audio_timeline"] = audio_timeline
        self._save_matrix_state(state)
        self.log("Module B - Agent 10 processing complete. Audio processing data merged.")

if __name__ == "__main__":
    matcher = AiAgent10AudioToneEmotionMatcher()
    matcher.process_emotions()
    print("\n--- Z-NET VOCAL MODULE B: AGENT 10 COMPLETE ---")
