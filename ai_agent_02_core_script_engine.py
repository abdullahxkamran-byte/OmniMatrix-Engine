import os
import sys
import json
import time
import requests
import urllib.request
import urllib.error

class Ai_Agent_02_Core_Script_Engine:
    def __init__(self):
        self.agent_name = "Ai_Agent_02_Core_Script_Engine"
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
                    "content": "You are a core script design engine. Generate strict raw JSON matching the requested schema."
                },
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(f"OpenAI API Error [{response.status_code}]: {response.text}")

        res_json = response.json()
        content = res_json["choices"][0]["message"]["content"].strip()
        
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        return json.loads(content)

    def _validate_script_schema(self, data: dict) -> bool:
        if not isinstance(data, dict) or "core_script_sequence" not in data:
            return False
        sequence = data["core_script_sequence"]
        if not isinstance(sequence, list) or len(sequence) == 0:
            return False

        required_keys = [
            "scene_id",
            "visual_action",
            "foley_audio",
            "verbal_dialogue",
            "pacing_duration"
        ]

        for scene in sequence:
            if not isinstance(scene, dict):
                return False
            for key in required_keys:
                if key not in scene:
                    return False
        return True

    def execute(self, state: dict) -> dict:
        target_agent = state.get("pipeline_status", {}).get("next_agent", "Ai_Agent_02")
        if target_agent != "Ai_Agent_02":
            print(f"[{self.agent_name}] Execution skipped. Pipeline queue targeted to: {target_agent}")
            return state

        runtime_data = state.setdefault("runtime_data", {})
        module_scripting = runtime_data.setdefault("module_a_scripting", {})

        if "agent_02_core_script" in module_scripting:
            del module_scripting["agent_02_core_script"]
            print(f"[{self.agent_name}] Idempotency Sweep: Cleared legacy core script data.")

        core_topic = runtime_data.get("core_topic", state.get("user_prompt", ""))
        if not core_topic:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: Core topic missing in state.")

        global_config = state.get("global_config", {})
        content_format = global_config.get("content_format", runtime_data.get("content_format", "Dynamic Short Narrative"))
        vibe_tempo = global_config.get("vibe_tempo", runtime_data.get("vibe_tempo", "Adaptive Dynamic Rhythm"))
        animation_dna = global_config.get("animation_dna", runtime_data.get("animation_dna", "Procedural Graphics Engine"))
        genre_style = global_config.get("genre_style", runtime_data.get("genre_style", "Universal Genre"))
        master_theme = runtime_data.get("master_theme_blueprint", f"{genre_style} - {content_format}")

        agent_01_hooks = module_scripting.get("agent_01_hooks", [])
        if not agent_01_hooks:
            raise ValueError(f"[{self.agent_name}] ERROR: No hooks found from Agent 01. Pipeline synchronization broken.")

        selected_index = module_scripting.get("selected_hook_index", 0)
        if selected_index < 0 or selected_index >= len(agent_01_hooks):
            print(f"[{self.agent_name}] Warning: selected_hook_index {selected_index} out of bounds. Defaulting to 0.")
            selected_index = 0

        selected_hook = agent_01_hooks[selected_index]
        print(f"[{self.agent_name}] Continuing story based on Hook Index [{selected_index}]: {selected_hook.get('hook_approach', 'Primary Hook')}")

        prompt = (
            f"You are the OmniMatrix Core Script Engine.\n"
            f"Your task is to take the selected opening hook and expand it into a continuous, highly engaging chronological sequence of narrative scenes.\n\n"
            f"Context Parameters:\n"
            f"- Topic: '{core_topic}'\n"
            f"- Master Theme / Aesthetic: '{master_theme}'\n"
            f"- Content Format: '{content_format}'\n"
            f"- Vibe & Tempo: '{vibe_tempo}'\n"
            f"- Visual DNA: '{animation_dna}'\n"
            f"- Selected Hook Directive: {json.dumps(selected_hook)}\n\n"
            f"Instructions:\n"
            f"1. Do not repeat the opening hook. Start narrative continuation from the exact frame where the hook ends.\n"
            f"2. Generate a logical, seamless chronological sequence of 3 to 5 scenes matching the format '{content_format}'.\n"
            f"3. Maintain precise 3D visual directions, atmospheric Foley SFX, and pacing for every scene beat.\n\n"
            f"Return ONLY valid JSON with this exact schema:\n"
            f"{{\n"
            f"  \"core_script_sequence\": [\n"
            f"    {{\n"
            f"      \"scene_id\": \"scene_01_continuation\",\n"
            f"      \"visual_action\": \"Detailed camera movement, lighting, subject motion, and spatial framing\",\n"
            f"      \"foley_audio\": \"Exact audio frequency drop, ambient sounds, music pacing, or impact SFX\",\n"
            f"      \"verbal_dialogue\": \"Spoken lines or onscreen text overlay (Use 'None' if purely visual/audio)\",\n"
            f"      \"pacing_duration\": \"Duration directive (e.g., '2.5 seconds', 'Hyper-Kinetic Snap')\"\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        generated_data = None
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{self.agent_name}] Attempt {attempt}/{self.max_retries}: Triggering Primary Gemini REST API...")
                parsed_json = self._call_gemini_rest(prompt)
                if self._validate_script_schema(parsed_json):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Primary Gemini REST API payload validated successfully.")
                    break
                else:
                    raise ValueError("JSON payload schema validation failed (missing keys or empty array).")
            except Exception as e:
                last_error = str(e)
                print(f"[{self.agent_name}] Primary Gemini REST API attempt {attempt} failed: {last_error}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        if not generated_data and self.openai_api_key:
            print(f"[{self.agent_name}] Primary API failed. Activating Rule 14 Dual API Failsafe (OpenAI gpt-4o-mini)...")
            try:
                parsed_json = self._call_openai_failsafe(prompt)
                if self._validate_script_schema(parsed_json):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Failsafe OpenAI API payload validated successfully.")
            except Exception as e:
                last_error = f"Gemini Error: {last_error} | OpenAI Failsafe Error: {str(e)}"
                print(f"[{self.agent_name}] Failsafe OpenAI API execution failed: {str(e)}")

        if not generated_data:
            raise RuntimeError(f"[{self.agent_name}] CRITICAL EXECUTION FAILURE: All API channels failed. Traceback: {last_error}")

        module_scripting["agent_02_core_script"] = generated_data["core_script_sequence"]

        pipeline_status = state.setdefault("pipeline_status", {})
        pipeline_status["last_active_agent"] = "Ai_Agent_02"
        pipeline_status["Ai_Agent_02"] = "COMPLETED"

        state_file_path = state.get("state_file_path")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution completed successfully. Core script continuation written for format [{content_format}].")
        return state
