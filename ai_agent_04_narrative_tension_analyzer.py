import os
import sys
import json
import time
import urllib.request
import urllib.error

class Ai_Agent_04_Narrative_Tension_Analyzer:
    def __init__(self):
        self.agent_name = "Ai_Agent_04_Narrative_Tension_Analyzer"
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.max_retries = 3
        self.retry_delay = 2

    def _call_gemini_rest(self, prompt: str) -> dict:
        if not self.gemini_api_key or self.gemini_api_key.startswith("YOUR_"):
            raise ValueError(f"[{self.agent_name}] CRITICAL: GEMINI_API_KEY missing or invalid.")

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.gemini_api_key
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)

                try:
                    text_content = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
                except (KeyError, IndexError):
                    raise RuntimeError(f"Invalid Gemini REST payload structure: {json.dumps(res_json)}")

                if text_content.startswith("```"):
                    lines = text_content.splitlines()
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    text_content = "\n".join(lines).strip()

                return json.loads(text_content)

        except urllib.error.HTTPError as http_err:
            err_msg = http_err.read().decode("utf-8")
            raise RuntimeError(f"[{self.agent_name}] Gemini API HTTP Error [{http_err.code}]: {err_msg}")
        except Exception as e:
            raise RuntimeError(f"[{self.agent_name}] Gemini Connection Exception: {str(e)}")

    def _call_openai_failsafe(self, prompt: str) -> dict:
        if not self.openai_api_key:
            raise ValueError(f"[{self.agent_name}] OPENAI_API_KEY missing for Dual API Failsafe execution.")

        url = "[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a master narrative tension and pacing analyzer. Generate strict raw JSON matching the requested schema."
                },
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                content = res_json["choices"][0]["message"]["content"].strip()
                
                if content.startswith("```"):
                    lines = content.splitlines()
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    content = "\n".join(lines).strip()

                return json.loads(content)
        except urllib.error.HTTPError as http_err:
            raise RuntimeError(f"OpenAI API Error [{http_err.code}]: {http_err.read().decode('utf-8')}")
        except Exception as e:
            raise RuntimeError(f"OpenAI Failsafe Error: {str(e)}")

    def _validate_tension_schema(self, data: dict) -> bool:
        if not isinstance(data, dict) or "tension_timeline" not in data:
            return False
        timeline = data["tension_timeline"]
        if not isinstance(timeline, list) or len(timeline) == 0:
            return False

        required_keys = [
            "frame_index",
            "tension_score",
            "pacing_instruction",
            "highlight_keywords",
            "vfx_color_shift",
            "audio_attenuation_db"
        ]

        for point in timeline:
            if not isinstance(point, dict):
                return False
            for key in required_keys:
                if key not in point:
                    return False
        return True

    def execute(self, state: dict) -> dict:
        target_agent = state.get("pipeline_status", {}).get("next_agent", "Ai_Agent_04")
        if target_agent != "Ai_Agent_04":
            print(f"[{self.agent_name}] Execution skipped. Pipeline queue targeted to: {target_agent}")
            return state

        runtime_data = state.setdefault("runtime_data", {})
        module_scripting = runtime_data.setdefault("module_a_scripting", {})

        if "agent_04_tension_peaks" in module_scripting:
            del module_scripting["agent_04_tension_peaks"]
            print(f"[{self.agent_name}] Idempotency Sweep: Cleared legacy tension data.")

        # Extract Universal Variables
        core_topic = runtime_data.get("core_topic", state.get("user_prompt", ""))
        global_config = state.get("global_config", {})
        content_format = global_config.get("content_format", runtime_data.get("content_format", "Dynamic Short Narrative"))
        vibe_tempo = global_config.get("vibe_tempo", runtime_data.get("vibe_tempo", "Adaptive Dynamic Rhythm"))
        animation_dna = global_config.get("animation_dna", runtime_data.get("animation_dna", "Procedural Graphics Engine"))
        
        # Pull frames from Agent 03
        agent_03_data = module_scripting.get("agent_03_storyboard", [])
        if not agent_03_data:
            raise ValueError(f"[{self.agent_name}] ERROR: No storyboard frames found from Agent 03. Pipeline broken.")

        print(f"[{self.agent_name}] Analyzing Narrative Tension for {len(agent_03_data)} frames...")

        prompt = (
            f"You are the OmniMatrix Supreme Narrative Tension Architect and Audio-Visual Pacing Analyst.\n"
            f"Your objective is to map precise tension curves and audio-visual cues for the provided storyboard frames.\n\n"
            f"Context Parameters:\n"
            f"- Topic: '{core_topic}'\n"
            f"- Format/Style: '{content_format}'\n"
            f"- Visual DNA: '{animation_dna}'\n"
            f"- Acoustic Signature: '{vibe_tempo}'\n"
            f"- Number of Frames: {len(agent_03_data)}\n\n"
            f"Input Storyboard Data:\n{json.dumps(agent_03_data)}\n\n"
            f"Instructions:\n"
            f"1. Analyze EACH frame provided and assign an emotional/kinetic tension score from 1 (calm/whisper) to 10 (intense climax/explosive shock).\n"
            f"2. Define dynamic editing pacing, kinetic typography keywords, VFX color shifts, and audio DB attenuation for each frame to create a cinematic emotional curve.\n"
            f"3. Return EXACTLY the same number of objects in the timeline as there are input frames.\n\n"
            f"Return ONLY valid JSON with this exact schema:\n"
            f"{{\n"
            f"  \"tension_timeline\": [\n"
            f"    {{\n"
            f"      \"frame_index\": 1,\n"
            f"      \"tension_score\": 8,\n"
            f"      \"pacing_instruction\": \"Hyper-Kinetic Snap Cut\",\n"
            f"      \"highlight_keywords\": [\"Critical\", \"Words\"],\n"
            f"      \"vfx_color_shift\": \"Peak-Saturation Red\",\n"
            f"      \"audio_attenuation_db\": 4\n"
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
                if self._validate_tension_schema(parsed_json) and len(parsed_json["tension_timeline"]) == len(agent_03_data):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Primary Gemini REST API payload validated successfully.")
                    break
                else:
                    raise ValueError("JSON payload schema validation failed (missing keys or frame count mismatch).")
            except Exception as e:
                last_error = str(e)
                print(f"[{self.agent_name}] Primary Gemini REST API attempt {attempt} failed: {last_error}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        if not generated_data and self.openai_api_key:
            print(f"[{self.agent_name}] Primary API failed. Activating Rule 14 Dual API Failsafe (OpenAI gpt-4o-mini)...")
            try:
                parsed_json = self._call_openai_failsafe(prompt)
                if self._validate_tension_schema(parsed_json):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Failsafe OpenAI API payload validated successfully.")
            except Exception as e:
                last_error = f"Gemini Error: {last_error} | OpenAI Failsafe Error: {str(e)}"
                print(f"[{self.agent_name}] Failsafe OpenAI API execution failed: {str(e)}")

        if not generated_data:
            raise RuntimeError(f"[{self.agent_name}] CRITICAL EXECUTION FAILURE: All API channels failed. Traceback: {last_error}")

        module_scripting["agent_04_tension_peaks"] = generated_data["tension_timeline"]

        pipeline_status = state.setdefault("pipeline_status", {})
        pipeline_status["last_active_agent"] = "Ai_Agent_04"
        pipeline_status["Ai_Agent_04"] = "COMPLETED"

        state_file_path = state.get("state_file_path")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution completed successfully. Tension Timeline Locked!")
        return state
