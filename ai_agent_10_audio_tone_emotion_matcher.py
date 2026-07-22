import os
import sys
import json
import re
import urllib.request
import urllib.error

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
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

class AiAgent09AudioToneEmotionMatcher:
    def __init__(self):
        self.agent_name = "Ai_Agent_09"
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
            self.log("matrix_state.json not found. Pipeline must initiate from Module A.", "FATAL")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("Matrix state successfully synchronized.", "SUCCESS")

    def _clean_json_response(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            return cleaned[start_idx:end_idx + 1]
        
        start_idx_arr = cleaned.find('[')
        end_idx_arr = cleaned.rfind(']')
        if start_idx_arr != -1 and end_idx_arr != -1:
            return cleaned[start_idx_arr:end_idx_arr + 1]
            
        return cleaned

    def fetch_ai_mappings(self, tracks, global_config):
        dna_profile = global_config.get("dna_profile", "cinematic narrative")
        vibe_tempo = global_config.get("vibe_tempo", "dynamic")
        content_format = global_config.get("content_format", "standard video")

        system_prompt = (
            f"You are an expert NLP audio director for a {content_format} project. "
            f"The project DNA is '{dna_profile}' and the overall vibe is '{vibe_tempo}'.\n"
            "Your task is to analyze the 'spoken_voiceover' and inject TTS emotion tags based on pacing and tension.\n"
            "Rules:\n"
            "1. Inject tags like [gasps], [sigh], [laughs], [whispers] naturally where required by the scene context.\n"
            "2. Stretch vowels in moments of high shock or rage (e.g., 'no' -> 'nooooo').\n"
            "3. Keep text normal if the tension is low.\n"
            "Return STRICTLY a JSON object containing a list named 'emotion_mappings'.\n"
            "Parameters required per frame:\n"
            "- 'frame_index': integer.\n"
            "- 'character': string.\n"
            "- 'tagged_voiceover': string (The modified script).\n"
            "- 'tone_category': string (e.g., 'whisper', 'rage', 'neutral', 'hype', 'cold').\n"
            "- 'pitch_shift_semitones': integer (-4 to +4).\n"
            "- 'delivery_speed_multiplier': float (0.80 to 1.25).\n"
            "- 'reverb_mix': float (0.0 to 0.60)."
        )
        
        user_prompt = "Audio Tracks Metadata:\n" + json.dumps(tracks, indent=2)

        # Core 1: Gemini
        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Querying Core 1 (Gemini) for emotion extraction...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("emotion_mappings", [])
            except Exception as e:
                self.log(f"Core 1 Failed: {e}", "WARNING")

        # Core 2: OpenAI
        if self.openai_api_key:
            self.log(f"Querying Core 2 (OpenAI - {self.model_cloud})...")
            try:
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"}
                payload = {
                    "model": self.model_cloud,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    raw_text = res_data["choices"][0]["message"]["content"]
                    return json.loads(self._clean_json_response(raw_text)).get("emotion_mappings", [])
            except Exception as e:
                self.log(f"Core 2 Failed: {e}", "WARNING")

        # Core 3: Ollama (Local AI)
        self.log(f"Querying Core 3 (Ollama Local - {self.model_local})...")
        try:
            payload = {
                "model": self.model_local,
                "prompt": system_prompt + "\n\n" + user_prompt + "\n\nProvide the JSON output now:",
                "stream": False,
                "format": "json"
            }
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                raw_text = res_data.get("response", "{}")
                parsed_json = json.loads(self._clean_json_response(raw_text))
                if "emotion_mappings" in parsed_json:
                    return parsed_json["emotion_mappings"]
        except Exception as e:
            self.log(f"Core 3 Failed: {e}", "WARNING")

        # Core 4: Procedural Fallback
        self.log("All Neural Cores Failed. Engaging Procedural Audio Logic.", "STATUS")
        return self._execute_procedural_fallback(tracks, vibe_tempo)

    def _execute_procedural_fallback(self, tracks, vibe_tempo):
        mappings = []
        total = len(tracks) if tracks else 1

        for idx, track in enumerate(tracks):
            frame_idx = track.get("frame_index", idx + 1)
            original_text = track.get("spoken_voiceover", "")
            progression = (idx + 1) / total

            tagged_text = original_text
            
            # Fluid math-based emotional arc injection
            if progression < 0.3:
                tone, pitch, speed, reverb = "neutral", 0, 1.0, 0.10
            elif progression >= 0.3 and progression < 0.7:
                if "dark" in vibe_tempo.lower() or "intense" in vibe_tempo.lower():
                    tone, pitch, speed, reverb = "cold", -1, 0.95, 0.20
                    tagged_text = f"[sigh] {original_text}"
                else:
                    tone, pitch, speed, reverb = "upbeat", +1, 1.05, 0.15
            else:
                tone, pitch, speed, reverb = "hype", +2, 1.15, 0.30
                if "!" in original_text:
                    tagged_text = f"[gasps] {original_text}"

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
        
        # 1. Atomic Handshake Protocol
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator requested '{orchestrator.get('next_agent')}', not {self.agent_name}.", "WARNING")
            sys.exit(0)

        # 2. Extract Global Configuration
        global_config = state.get("global_config", {})

        # 3. Retrieve or Initialize Audio Timeline
        if "module_b_audio" not in state:
            state["module_b_audio"] = {}

        audio_timeline = state["module_b_audio"].get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("No audio timeline found. Importing base storyboard from Module A...", "STATUS")
            storyboard = state.get("module_a_concept", {}).get("storyboard", [])
            if not storyboard:
                self.log("Critical Error: No storyboard found in Module A. Cannot proceed.", "FATAL")
                sys.exit(1)
            
            audio_timeline = []
            for frame in storyboard:
                audio_timeline.append({
                    "frame_index": frame.get("frame_index"),
                    "character": frame.get("character", "Narrator"),
                    "spoken_voiceover": frame.get("spoken_voiceover", "")
                })

        # 4. Idempotency Sweep (Clear Ghost Data)
        for frame in audio_timeline:
            frame.pop("tagged_voiceover", None)
            frame.pop("audio_effects_processing", None)
        self.log("Idempotency sweep complete. Legacy emotion data purged.")

        # 5. Core Execution
        self.log(f"Analyzing tone matrix for {len(audio_timeline)} audio tracks...")
        ai_mappings = self.fetch_ai_mappings(audio_timeline, global_config)

        for frame in audio_timeline:
            for mapping in ai_mappings:
                if frame.get("frame_index") == mapping.get("frame_index"):
                    frame["tagged_voiceover"] = mapping.get("tagged_voiceover", frame.get("spoken_voiceover"))
                    frame["audio_effects_processing"] = {
                        "tone_category": mapping.get("tone_category", "neutral"),
                        "pitch_shift_semitones": mapping.get("pitch_shift_semitones", 0),
                        "delivery_speed_multiplier": mapping.get("delivery_speed_multiplier", 1.0),
                        "reverb_mix": mapping.get("reverb_mix", 0.0)
                    }
                    break
        
        # 6. Save State and Update Handshake
        state["module_b_audio"]["emotions_mapped"] = True
        state["module_b_audio"]["audio_timeline"] = audio_timeline
        
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        state["orchestrator_matrix"]["next_agent"] = "Ai_Agent_10"  # Passing control to Voice Synthesizer
        
        self._save_matrix_state(state)
        self.log(f"Agent {self.agent_name} complete. Tagged scripts ready for Voice Generator (Ai_Agent_10).")

if __name__ == "__main__":
    matcher = AiAgent09AudioToneEmotionMatcher()
    matcher.process_emotions()
