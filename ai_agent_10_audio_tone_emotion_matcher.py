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
            self.log("matrix_state.json not found. Run Module A first.", "ERROR")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        """Updates the central OmniMatrix state with new emotional audio mappings."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("Matrix state successfully updated with Emotion Tags & Audio Metadata.")

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
        """Queries the AI to rewrite text with emotion tags based on context."""
        system_prompt = (
            "You are an expert NLP audio director for a dark phonk/anime video. "
            "Your job is to read the 'spoken_voiceover' and the scene context, and inject TTS emotion tags. "
            "Rules:\n"
            "1. If the scene is calm/normal, keep the text mostly normal.\n"
            "2. If the scene has high tension/shock/rage, stretch vowels (e.g., 'what' -> 'whaaaaat!', 'no' -> 'nooooo!') and add TTS emotion tags like [gasps], [sigh], [laughs_evil].\n"
            "3. Also define post-processing parameters for the final mix.\n\n"
            "Return STRICTLY a JSON object containing a list named 'emotion_mappings'.\n"
            "Parameters required per frame:\n"
            "- 'frame_index': integer.\n"
            "- 'character': string.\n"
            "- 'tagged_voiceover': string (The modified script with emotions/tags).\n"
            "- 'tone_category': ('whisper-menace', 'screaming-rage', 'cold-assertive', 'hype-buildup', 'neutral').\n"
            "- 'pitch_shift_semitones': integer (-4 to +2).\n"
            "- 'delivery_speed_multiplier': float (0.85 to 1.15).\n"
            "- 'reverb_mix': float (0.0 to 0.60).\n"
        )
        
        user_prompt = "Audio Tracks Metadata:\n" + json.dumps(tracks, indent=2)

        # 1st Priority: Gemini AI
        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Querying Core 1: Gemini AI for script emotion tagging...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("emotion_mappings", [])
            except Exception as e:
                self.log(f"Gemini Engine failed: {e}. Switching to OpenAI fallback.", "WARNING")

        # 2nd Priority: OpenAI
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

        # Fallback: Procedural Logic
        self.log("All AI API Cores failed. Using Offline Procedural Logic Engine.", "STATUS")
        return self._execute_procedural_fallback(tracks)

    def _execute_procedural_fallback(self, tracks):
        """Offline fallback that procedurally adds tags based on character/progression."""
        mappings = []
        total = len(tracks) if tracks else 1

        for idx, track in enumerate(tracks):
            frame_idx = track.get("frame_index", idx + 1)
            char_name = track.get("character", "Unknown").lower()
            original_text = track.get("spoken_voiceover", "")
            progression = (idx + 1) / total

            tagged_text = original_text
            
            # Procedural logic for stretching words and tags
            if "sukuna" in char_name or "villain" in char_name:
                tone, pitch, speed, reverb = "screaming-rage", -3, 1.05, 0.45
                tagged_text = f"[evil_laugh] {original_text.replace('what', 'whaaaaat').replace('no ', 'nooooo ')}!"
            elif "gojo" in char_name or "hero" in char_name:
                tone, pitch, speed, reverb = "cold-assertive", 0, 1.0, 0.15
                tagged_text = f"[sigh] {original_text}"
            elif progression > 0.7:  # Climax / High tension
                tone, pitch, speed, reverb = "hype-buildup", +1, 1.10, 0.20
                tagged_text = f"[gasps] {original_text.replace('what', 'whaaaat')}"
            else:
                tone, pitch, speed, reverb = "neutral", 0, 1.0, 0.10

            mappings.append({
                "frame_index": frame_idx,
                "character": track.get("character", "Unknown"),
                "tagged_voiceover": tagged_text,
                "tone_category": tone,
                "pitch_shift_semitones": pitch,
                "delivery_speed_multiplier": speed,
                "reverb_mix": reverb
            })

        return mappings

    def process_emotions(self):
        state = self._load_matrix_state()
        
        # Checking Module A / Base Timeline instead of purely Audio Generated Timeline
        # Because this agent now runs BEFORE Agent 09 generates the actual audio files.
        audio_module = state.get("module_b_audio", {})
        audio_timeline = audio_module.get("audio_timeline", [])
        
        # If audio_timeline doesn't exist yet, fetch storyboard from Module A
        if not audio_timeline:
            self.log("No audio timeline found. Importing base storyboard from Module A...", "STATUS")
            storyboard = state.get("module_a_concept", {}).get("storyboard", [])
            if not storyboard:
                self.log("Critical Error: No storyboard found in Module A. Cannot proceed.", "ERROR")
                return
            
            # Initialize audio timeline structure from storyboard
            audio_timeline = []
            for frame in storyboard:
                audio_timeline.append({
                    "frame_index": frame.get("frame_index"),
                    "character": frame.get("character", "Narrator"),
                    "spoken_voiceover": frame.get("spoken_voiceover", "")
                })

        self.log(f"Analyzing psychology and tone matrix for {len(audio_timeline)} audio tracks...")
        
        ai_mappings = self.fetch_ai_mappings(audio_timeline)

        # Merge the generated emotional logic and tagged script back into the timeline
        for frame in audio_timeline:
            for mapping in ai_mappings:
                if frame.get("frame_index") == mapping.get("frame_index"):
                    # This is the most important part: Saving the TAGGED text for Agent 09
                    frame["tagged_voiceover"] = mapping.get("tagged_voiceover", frame.get("spoken_voiceover"))
                    
                    # Saving post-processing data for Agent 19
                    frame["audio_effects_processing"] = {
                        "tone_category": mapping.get("tone_category", "neutral"),
                        "pitch_shift_semitones": mapping.get("pitch_shift_semitones", 0),
                        "delivery_speed_multiplier": mapping.get("delivery_speed_multiplier", 1.0),
                        "reverb_mix": mapping.get("reverb_mix", 0.0)
                    }
                    break
        
        # Ensure module_b_audio exists in state
        if "module_b_audio" not in state:
            state["module_b_audio"] = {}
            
        state["module_b_audio"]["emotions_mapped"] = True
        state["module_b_audio"]["audio_timeline"] = audio_timeline
        self._save_matrix_state(state)
        self.log("Module B - Agent 10 processing complete. Tagged scripts ready for Voice Generator (Agent 09).")

if __name__ == "__main__":
    matcher = AiAgent10AudioToneEmotionMatcher()
    matcher.process_emotions()
    print("\n--- Omni Matrix VOCAL MODULE B: AGENT 10 COMPLETE ---")
