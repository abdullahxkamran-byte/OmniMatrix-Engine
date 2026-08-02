import os
import re
import sys
import json
import time
import subprocess
import urllib.request
import urllib.error

class Ai_Agent_10_HuggingFace_RVC_Voice_Generator:
    def __init__(self):
        self.agent_name = "Ai_Agent_10_HuggingFace_RVC_Voice_Generator"
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.hf_api_key = os.getenv("HF_API_KEY", "")
        self.max_retries = 3
        self.retry_delay = 2

    def _clean_json_response(self, raw_text: str) -> dict:
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
        return json.loads(cleaned)

    def _call_gemini_rest(self, prompt: str) -> dict:
        if not self.gemini_api_key or self.gemini_api_key.startswith("YOUR_"):
            raise ValueError(f"[{self.agent_name}] CRITICAL: GEMINI_API_KEY missing.")

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.gemini_api_key
        }
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                try:
                    text_content = res_json['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError):
                    raise RuntimeError(f"[{self.agent_name}] Invalid Gemini REST payload structure.")
                return self._clean_json_response(text_content)
        except urllib.error.HTTPError as http_err:
            raise RuntimeError(f"[{self.agent_name}] Gemini API HTTP Error [{http_err.code}]: {http_err.read().decode('utf-8')}")
        except Exception as e:
            raise RuntimeError(f"[{self.agent_name}] Gemini Connection Exception: {str(e)}")

    def _call_openai_failsafe(self, prompt: str) -> dict:
        if not self.openai_api_key:
            raise ValueError(f"[{self.agent_name}] OPENAI_API_KEY missing for Dual API Failsafe.")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a master voice casting director. Generate strict raw JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                content = res_json["choices"][0]["message"]["content"]
                return self._clean_json_response(content)
        except urllib.error.HTTPError as http_err:
            raise RuntimeError(f"[{self.agent_name}] OpenAI API Error [{http_err.code}]: {http_err.read().decode('utf-8')}")
        except Exception as e:
            raise RuntimeError(f"[{self.agent_name}] OpenAI Failsafe Error: {str(e)}")

    def _validate_casting_schema(self, data: dict) -> bool:
        if not isinstance(data, dict) or "voice_casting" not in data:
            return False
        for cast in data["voice_casting"]:
            if not all(k in cast for k in ["character", "elevenlabs_voice_id", "hf_tts_model", "edge_tts_voice"]):
                return False
        return True

    def _generate_elevenlabs_rest(self, text: str, voice_id: str, output_path: str) -> bool:
        if not self.elevenlabs_api_key:
            return False
            
        clean_vid = str(voice_id).strip()
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{clean_vid}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
        }
        
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
            return True
        except Exception as e:
            print(f"[{self.agent_name}] ElevenLabs API Failed: {str(e)}", flush=True)
            return False

    def _generate_huggingface_rest(self, text: str, model_id: str, output_path: str) -> bool:
        if not self.hf_api_key:
            print(f"[{self.agent_name}] HF_API_KEY missing. Skipping Hugging Face REST.", flush=True)
            return False
            
        clean_model = str(model_id).strip()
        url = f"https://api-inference.huggingface.co/models/{clean_model}"
        headers = {
            "Authorization": f"Bearer {self.hf_api_key}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": text}
        
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
            return True
        except Exception as e:
            print(f"[{self.agent_name}] HuggingFace API Failed for model {clean_model}: {str(e)}", flush=True)
            return False

    def _generate_edge_tts_cli(self, text: str, voice_id: str, output_path: str) -> bool:
        try:
            clean_vid = str(voice_id).strip()
            subprocess.run(
                ["edge-tts", "--voice", clean_vid, "--text", text, "--write-media", output_path],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return True
        except Exception as e:
            print(f"[{self.agent_name}] Edge-TTS CLI Failed: {str(e)}", flush=True)
            return False

    def _get_audio_duration(self, file_path: str) -> float:
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            return round(float(result.stdout.strip()), 2)
        except Exception:
            return 3.0

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")
        
        if target_agent and "Ai_Agent_10" not in target_agent and target_agent != self.agent_name:
            print(f"[{self.agent_name}] Execution skipped. Pipeline queue targeted to: {target_agent}", flush=True)
            return state

        workspace_dir = state.get("workspace_dir", "")
        if not workspace_dir:
            workspace_dir = state.get("state_file_path", "")
            if workspace_dir:
                workspace_dir = os.path.dirname(workspace_dir)
            else:
                raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: workspace_dir missing.")

        runtime_data = state.setdefault("runtime_data", {})
        module_audio = runtime_data.setdefault("module_b_audio", {})
        
        emotion_matrix = module_audio.get("agent_09_audio_emotions", [])
        if not emotion_matrix:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: 'agent_09_audio_emotions' not found. Agent 09 execution required.")

        audio_output_dir = os.path.join(workspace_dir, "audio_tracks")
        os.makedirs(audio_output_dir, exist_ok=True)

        if "agent_10_audio_files" in module_audio:
            for audio_entry in module_audio["agent_10_audio_files"]:
                file_path = audio_entry.get("file_path", "")
                if os.path.exists(file_path):
                    os.remove(file_path)
            del module_audio["agent_10_audio_files"]
            print(f"[{self.agent_name}] Idempotency sweep executed. Legacy tracks purged.", flush=True)

        unique_characters = list(set([frame.get("character_voice", "Narrator") for frame in emotion_matrix]))
        
        prompt = (
            f"You are the OmniMatrix Voice Casting Architect.\n"
            f"Assign accurate AI voice profiles for the following characters: {json.dumps(unique_characters)}\n\n"
            f"For EACH character, provide:\n"
            f"1. 'elevenlabs_voice_id': A theoretical/realistic 20-character ElevenLabs Voice ID for cloning (e.g., 'ErXwobaYiN019PkySvjV').\n"
            f"2. 'hf_tts_model': A valid Hugging Face inference model for voice synthesis (e.g., 'espnet/kan-bayashi_ljspeech_vits', 'facebook/mms-tts-eng').\n"
            f"3. 'edge_tts_voice': A valid Edge TTS code (e.g., 'en-US-GuyNeural', 'en-US-ChristopherNeural', 'en-GB-RyanNeural').\n\n"
            f"Return ONLY valid JSON with this exact schema:\n"
            f"{{\n"
            f"  \"voice_casting\": [\n"
            f"    {{\n"
            f"      \"character\": \"Character Name\",\n"
            f"      \"elevenlabs_voice_id\": \"ID\",\n"
            f"      \"hf_tts_model\": \"Model Name\",\n"
            f"      \"edge_tts_voice\": \"Voice Code\"\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        generated_data = None
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{self.agent_name}] Prompting Voice Casting AI (Attempt {attempt})...", flush=True)
                parsed_json = self._call_gemini_rest(prompt)
                if self._validate_casting_schema(parsed_json):
                    generated_data = parsed_json
                    break
                else:
                    raise ValueError("Schema validation failed.")
            except Exception as e:
                last_error = str(e)
                time.sleep(self.retry_delay)

        if not generated_data and self.openai_api_key:
            print(f"[{self.agent_name}] Fallback to OpenAI Dual Failsafe...", flush=True)
            try:
                parsed_json = self._call_openai_failsafe(prompt)
                if self._validate_casting_schema(parsed_json):
                    generated_data = parsed_json
            except Exception as e:
                last_error = f"Gemini: {last_error} | OpenAI: {str(e)}"

        if not generated_data:
            raise RuntimeError(f"[{self.agent_name}] Voice Casting AI Failed. Traceback: {last_error}")

        casting_map = {cast["character"]: cast for cast in generated_data["voice_casting"]}
        final_audio_entries = []

        print(f"[{self.agent_name}] Initiating Triple-Layer Synthesis for {len(emotion_matrix)} frames...", flush=True)

        for frame in emotion_matrix:
            idx = frame.get("frame_index", 1)
            char = frame.get("character_voice", "Narrator")
            text = frame.get("tagged_voiceover", "").strip()

            if not text or text.lower() == "none":
                continue

            cast_data = casting_map.get(char, {"elevenlabs_voice_id": "ErXwobaYiN019PkySvjV", "hf_tts_model": "espnet/kan-bayashi_ljspeech_vits", "edge_tts_voice": "en-US-ChristopherNeural"})
            output_file = os.path.join(audio_output_dir, f"frame_{idx:03d}_{char.replace(' ', '_').lower()}.mp3")
            
            success = False
            
            print(f"[{self.agent_name}] Frame {idx} [{char}] -> Attempting ElevenLabs", flush=True)
            success = self._generate_elevenlabs_rest(text, cast_data["elevenlabs_voice_id"], output_file)
            
            if not success:
                print(f"[{self.agent_name}] Frame {idx} [{char}] -> Attempting Hugging Face: {cast_data['hf_tts_model']}", flush=True)
                success = self._generate_huggingface_rest(text, cast_data["hf_tts_model"], output_file)
                
            if not success:
                print(f"[{self.agent_name}] Frame {idx} [{char}] -> Fallback Edge-TTS: {cast_data['edge_tts_voice']}", flush=True)
                success = self._generate_edge_tts_cli(text, cast_data["edge_tts_voice"], output_file)

            if success:
                duration = self._get_audio_duration(output_file)
                final_audio_entries.append({
                    "frame_index": idx,
                    "character_voice": char,
                    "file_path": output_file,
                    "duration_seconds": duration,
                    "reverb_mix": frame.get("reverb_mix", 0.0),
                    "pitch_shift_semitones": frame.get("pitch_shift_semitones", 0),
                    "delivery_speed_multiplier": frame.get("delivery_speed_multiplier", 1.0)
                })
            else:
                print(f"[{self.agent_name}] CRITICAL: All Voice APIs failed for Frame {idx}", flush=True)

        module_audio["agent_10_audio_files"] = final_audio_entries

        pipeline_status = state.setdefault("pipeline_status", {})
        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution completed. Voice generation locked.", flush=True)
        return state
