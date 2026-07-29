import os
import sys
import json
import re
import subprocess
import asyncio
import urllib.request
import urllib.error

# Manual .env loader utility
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

# Standardize API Integrations
try:
    import google.generativeai as genai
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    from gradio_client import Client
    GRADIO_CLIENT_AVAILABLE = True
except ImportError:
    GRADIO_CLIENT_AVAILABLE = False

class AiAgent10HuggingFaceRVCVoiceGenerator:
    def __init__(self):
        self.agent_name = "Ai_Agent_10"
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.audio_dir = os.path.join(self.workspace_dir, "audio_tracks")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        
        self.ollama_url = "http://localhost:11434/api/generate"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)
        self.hf_token = os.environ.get("HF_TOKEN", None)
        
        if GEMINI_SDK_AVAILABLE and self.gemini_key:
            genai.configure(api_key=self.gemini_key)

        os.makedirs(self.audio_dir, exist_ok=True)

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
        self.log("Matrix state successfully updated with generated audio metadata.", "SUCCESS")

    def _clean_json_response(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            return cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def get_audio_duration(self, file_path):
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries",
                 "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            return round(float(result.stdout.strip()), 2)
        except Exception:
            self.log("ffprobe not found in system PATH. Using duration estimation fallback (2.0s).", "WARNING")
            return 2.0 

    def perform_ai_voice_casting(self, characters_list, global_config):
        dna_profile = global_config.get("dna_profile", "cinematic narrative")
        
        system_prompt = (
            f"You are the AI Voice Casting Director for a project with the DNA: '{dna_profile}'.\n"
            f"Analyze these characters: {list(characters_list)}.\n"
            "Provide a theoretical 'hf_rvc_model_id' (e.g., 'Gojo_English_v2', 'Deep_Narrator') "
            "for Hugging Face Spaces, and an 'edge_tts_voice' (e.g., 'en-US-ChristopherNeural') for fallback.\n"
            "Return STRICTLY a JSON object with this exact structure:\n"
            "{\n"
            "  \"mappings\": {\n"
            "    \"CharacterName\": {\n"
            "      \"hf_rvc_model_id\": \"model_name_here\",\n"
            "      \"edge_tts_voice\": \"voice_name_here\"\n"
            "    }\n"
            "  }\n"
            "}"
        )

        # Core 1: Gemini
        if GEMINI_SDK_AVAILABLE and self.gemini_key:
            self.log("Querying Core 1 (Gemini) for voice casting...")
            try:
                model = genai.GenerativeModel("gemini-flash-latest")
                response = model.generate_content(system_prompt, generation_config={"response_mime_type": "application/json"})
                return json.loads(self._clean_json_response(response.text)).get("mappings", {})
            except Exception as e:
                self.log(f"Core 1 Failed: {e}", "WARNING")

        # Core 2: OpenAI
        if self.openai_api_key:
            self.log(f"Querying Core 2 (OpenAI - {self.model_cloud}) for voice casting...")
            try:
                headers = {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_api_key}"}
                payload = {
                    "model": self.model_cloud,
                    "messages": [{"role": "system", "content": system_prompt}],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    raw_text = res_data["choices"][0]["message"]["content"]
                    return json.loads(self._clean_json_response(raw_text)).get("mappings", {})
            except Exception as e:
                self.log(f"Core 2 Failed: {e}", "WARNING")

        # Core 3: Ollama
        self.log(f"Querying Core 3 (Ollama Local - {self.model_local}) for voice casting...")
        try:
            payload = {
                "model": self.model_local,
                "prompt": system_prompt + "\n\nProvide the JSON output now:",
                "stream": False,
                "format": "json"
            }
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
            with urllib.request.urlopen(req, timeout=120) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                raw_text = res_data.get("response", "{}")
                return json.loads(self._clean_json_response(raw_text)).get("mappings", {})
        except Exception as e:
            self.log(f"Core 3 Failed: {e}", "WARNING")

        # Core 4: Procedural Fallback
        self.log("All AI Cores failed. Using Rule-Based Procedural Casting.", "STATUS")
        return self._offline_rule_based_casting(characters_list)

    def _offline_rule_based_casting(self, characters_list):
        mappings = {}
        for char in characters_list:
            char_lower = char.lower()
            if "gojo" in char_lower:
                mappings[char] = {"hf_rvc_model_id": "Gojo_Eng_Dub", "edge_tts_voice": "en-US-GuyNeural"}
            elif "sukuna" in char_lower:
                mappings[char] = {"hf_rvc_model_id": "Sukuna_Eng_Dub", "edge_tts_voice": "en-GB-RyanNeural"}
            elif "villain" in char_lower:
                mappings[char] = {"hf_rvc_model_id": "Deep_Villain", "edge_tts_voice": "en-US-SteffanNeural"}
            else:
                mappings[char] = {"hf_rvc_model_id": "Generic_Male", "edge_tts_voice": "en-US-ChristopherNeural"}
        return mappings

    def _fetch_huggingface_audio(self, text, output_path, hf_model_id):
        if not GRADIO_CLIENT_AVAILABLE:
            self.log("gradio_client not installed. Skipping HuggingFace generation.", "WARNING")
            return False

        self.log(f"Attempting Hugging Face Generation [Model: {hf_model_id}]...", "STATUS")
        
        try:
            client = Client("rvc-space/anime-tts") 
            result = client.predict(
                text=text,
                model_name=hf_model_id,
                api_name="/predict"
            )
            
            temp_audio_path = result[0] if isinstance(result, list) else result
            
            with open(temp_audio_path, 'rb') as f_src, open(output_path, 'wb') as f_dst:
                f_dst.write(f_src.read())
                
            return True
        except Exception as e:
            self.log(f"Hugging Face API failed or Space sleeping: {str(e)}", "WARNING")
            return False

    def _fetch_edge_tts_fallback(self, text, output_path, voice_name):
        if not EDGE_TTS_AVAILABLE:
            self.log("edge_tts not installed. Cannot use fallback.", "ERROR")
            return False

        async def _generate():
            communicate = edge_tts.Communicate(text, voice_name)
            await communicate.save(output_path)
            
        try:
            asyncio.run(_generate())
            return True
        except Exception as e:
            self.log(f"Edge-TTS failed: {str(e)}", "ERROR")
            return False

    def process_script_audio(self):
        state = self._load_matrix_state()
        
        # 1. Atomic Handshake Protocol
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator requested '{orchestrator.get('next_agent')}', not {self.agent_name}.", "WARNING")
            sys.exit(0)

        # 2. Extract Global Configuration
        global_config = state.get("global_config", {})

        # 3. Retrieve Audio Timeline from Agent 09
        audio_module = state.get("module_b_audio", {})
        audio_timeline = audio_module.get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("No audio timeline found. Agent 09 must map emotions first.", "FATAL")
            sys.exit(1)

        # 4. Idempotency Sweep (Clear Ghost Audio Files)
        self.log("Initiating Idempotency Sweep...", "STATUS")
        for frame in audio_timeline:
            legacy_audio = frame.get("audio_file_path")
            if legacy_audio and os.path.exists(legacy_audio):
                try:
                    os.remove(legacy_audio)
                    self.log(f"Purged legacy audio file: {legacy_audio}")
                except Exception as e:
                    self.log(f"Failed to purge {legacy_audio}: {e}", "WARNING")
            frame.pop("audio_file_path", None)
            frame.pop("audio_duration_seconds", None)

        unique_characters = set(frame.get("character", "Narrator") for frame in audio_timeline)
        casting_map = self.perform_ai_voice_casting(unique_characters, global_config)

        # 5. Audio Generation Loop
        for frame in audio_timeline:
            f_idx = frame.get("frame_index", 1)
            character = frame.get("character", "Narrator")
            
            text = frame.get("tagged_voiceover", frame.get("spoken_voiceover", "")).strip()
            
            if not text:
                self.log(f"Frame {f_idx} has no voiceover text. Skipping.", "WARNING")
                continue

            char_profile = casting_map.get(character, {})
            file_name = f"frame_{f_idx:03d}_{character.replace(' ', '_').lower()}.mp3"
            full_audio_path = os.path.join(self.audio_dir, file_name)
            
            success = False

            # Tier 1: Hugging Face RVC
            hf_model = char_profile.get("hf_rvc_model_id", "Generic_Male")
            success = self._fetch_huggingface_audio(text, full_audio_path, hf_model)

            # Tier 2: Edge TTS Ultimate Fallback
            if not success:
                edge_v = char_profile.get("edge_tts_voice", "en-US-ChristopherNeural")
                self.log(f"Routing to Core Fallback (Edge-TTS) for Frame {f_idx} [{character}]")
                success = self._fetch_edge_tts_fallback(text, full_audio_path, edge_v)

            if success:
                duration = self.get_audio_duration(full_audio_path)
                self.log(f"Frame {f_idx} Audio Locked: {duration} seconds.")
                
                frame["audio_file_path"] = full_audio_path
                frame["audio_duration_seconds"] = duration
            else:
                self.log(f"Critical Failure: Could not generate audio for Frame {f_idx}.", "ERROR")

        # 6. Save State and Update Handshake
        state["module_b_audio"]["audio_timeline"] = audio_timeline
        state["module_b_audio"]["voice_generation_status"] = "completed"
        
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        state["orchestrator_matrix"]["next_agent"] = "Ai_Agent_11"  # Passing control to Word Aligner
        
        self._save_matrix_state(state)
        self.log(f"Agent {self.agent_name} complete. Raw vocal files ready for Agent 11 (Word Aligner).")

if __name__ == "__main__":
    fetcher = AiAgent10HuggingFaceRVCVoiceGenerator()
    fetcher.process_script_audio()
