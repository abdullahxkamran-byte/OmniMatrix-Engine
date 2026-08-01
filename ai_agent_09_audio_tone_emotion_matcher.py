import os
import re
import sys
import json
import time
import urllib.request
import urllib.error

class Ai_Agent_09_Audio_Tone_Emotion_Matcher:
    def __init__(self):
        self.agent_name = "Ai_Agent_09_Audio_Tone_Emotion_Matcher"
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
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
            raise ValueError(f"[{self.agent_name}] CRITICAL: GEMINI_API_KEY missing or invalid.")

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
                    raise RuntimeError(f"Invalid Gemini REST payload structure: {json.dumps(res_json)}")
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
                {"role": "system", "content": "You are a master audio director. Generate strict raw JSON."},
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

    def _validate_schema(self, data: dict) -> bool:
        if not isinstance(data, dict) or "audio_emotion_matrix" not in data:
            return False
        frames = data["audio_emotion_matrix"]
        if not isinstance(frames, list) or len(frames) == 0:
            return False

        required_keys = [
            "frame_index",
            "character_voice",
            "tagged_voiceover",
            "tone_category",
            "pitch_shift_semitones",
            "delivery_speed_multiplier",
            "reverb_mix",
            "acoustic_environment"
        ]

        for frame in frames:
            if not isinstance(frame, dict):
                return False
            for key in required_keys:
                if key not in frame:
                    return False
        return True

    def execute(self, state: dict) -> dict:
        target_agent = state.get("pipeline_status", {}).get("next_agent", "Ai_Agent_09")
        if target_agent != "Ai_Agent_09":
            print(f"[{self.agent_name}] Execution skipped. Pipeline queue targeted to: {target_agent}", flush=True)
            return state

        runtime_data = state.setdefault("runtime_data", {})
        module_scripting = runtime_data.get("module_a_scripting", {})
        module_audio = runtime_data.setdefault("module_b_audio", {})

        if "agent_09_audio_emotions" in module_audio:
            del module_audio["agent_09_audio_emotions"]
            print(f"[{self.agent_name}] Idempotency sweep executed.", flush=True)

        master_playbook = module_scripting.get("final_master_playbook", [])
        if not master_playbook:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: Incomplete pipeline data (Master Playbook missing).")

        core_topic = runtime_data.get("core_topic", state.get("user_prompt", "Unknown Target"))
        global_config = state.get("global_config", {})
        
        medium = global_config.get("medium", "Dynamic/Unbound")
        rendering_engine = global_config.get("rendering_engine", "Dynamic/Unbound")
        color_lighting = global_config.get("color_lighting", "Dynamic/Unbound")
        kinetic_framing = global_config.get("kinetic_framing", "Dynamic/Unbound")

        print(f"[{self.agent_name}] Analyzing Tone and Emotion for {len(master_playbook)} frames...", flush=True)

        prompt = (
            f"You are the OmniMatrix Audio & Emotional Tone Director.\n"
            f"Your objective is to analyze the Final Master Playbook and assign exact emotional delivery vectors, pitch shifts, speeds, and acoustic environments for every spoken line.\n\n"
            f"4-Axis Visual DNA Context:\n"
            f"- Medium: '{medium}'\n"
            f"- Rendering Engine: '{rendering_engine}'\n"
            f"- Color & Lighting: '{color_lighting}'\n"
            f"- Kinetic Framing: '{kinetic_framing}'\n\n"
            f"Final Master Playbook Data:\n{json.dumps(master_playbook)}\n\n"
            f"CRITICAL DIRECTIVES:\n"
            f"1. Tagged Voiceover: Inject natural expressive tags into 'tagged_voiceover' (e.g., '[gasps] Reversal: Red!' or '[laughs] Open.'). Do not drop any core terminology.\n"
            f"2. Mathematical Audio Precision: Provide exact 'pitch_shift_semitones' (-4 to +4) and 'delivery_speed_multiplier' (0.80 to 1.30).\n"
            f"3. Acoustic Matching: Match 'reverb_mix' (0.0 to 1.0) and 'acoustic_environment' (e.g., 'Open Shibuya Street', 'Cosmic Void') based on the visual context of the scene.\n\n"
            f"Return ONLY valid JSON with this exact schema:\n"
            f"{{\n"
            f"  \"audio_emotion_matrix\": [\n"
            f"    {{\n"
            f"      \"frame_index\": 1,\n"
            f"      \"character_voice\": \"Character Name\",\n"
            f"      \"tagged_voiceover\": \"[emotion] Exact dialogue here\",\n"
            f"      \"tone_category\": \"aggressive/cocky/sadistic/neutral\",\n"
            f"      \"pitch_shift_semitones\": 0,\n"
            f"      \"delivery_speed_multiplier\": 1.05,\n"
            f"      \"reverb_mix\": 0.25,\n"
            f"      \"acoustic_environment\": \"Environment description\"\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        generated_data = None
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{self.agent_name}] Attempt {attempt}/{self.max_retries}: Triggering Primary Gemini REST API...", flush=True)
                parsed_json = self._call_gemini_rest(prompt)
                if self._validate_schema(parsed_json) and len(parsed_json["audio_emotion_matrix"]) == len(master_playbook):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Primary Gemini API payload validated successfully.", flush=True)
                    break
                else:
                    raise ValueError("JSON payload schema validation failed or array length mismatch.")
            except Exception as e:
                last_error = str(e)
                print(f"[{self.agent_name}] Primary API attempt {attempt} failed: {last_error}", flush=True)
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        if not generated_data and self.openai_api_key:
            print(f"[{self.agent_name}] Primary API failed. Activating Dual API Failsafe (OpenAI gpt-4o-mini)...", flush=True)
            try:
                parsed_json = self._call_openai_failsafe(prompt)
                if self._validate_schema(parsed_json) and len(parsed_json["audio_emotion_matrix"]) == len(master_playbook):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Failsafe OpenAI API payload validated successfully.", flush=True)
            except Exception as e:
                last_error = f"Gemini Error: {last_error} | OpenAI Failsafe Error: {str(e)}"
                print(f"[{self.agent_name}] Failsafe OpenAI API execution failed: {str(e)}", flush=True)

        if not generated_data:
            raise RuntimeError(f"[{self.agent_name}] CRITICAL EXECUTION FAILURE: All API channels failed. Traceback: {last_error}")

        module_audio["agent_09_audio_emotions"] = generated_data["audio_emotion_matrix"]

        pipeline_status = state.setdefault("pipeline_status", {})
        pipeline_status["last_active_agent"] = "Ai_Agent_09"
        pipeline_status["Ai_Agent_09"] = "COMPLETED"

        state_file_path = state.get("state_file_path")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution completed successfully. Emotional Audio Matrix locked.", flush=True)
        return state
