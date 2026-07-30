import os
import sys
import json
import time
import requests
import urllib.request
import urllib.error

class Ai_Agent_01_Universal_Hook_Designer:
    def __init__(self):
        self.agent_name = "Ai_Agent_01_Universal_Hook_Designer"
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
                    "content": "You are a universal hook design engine. Generate strict raw JSON matching the requested schema."
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

    def _validate_hook_schema(self, data: dict) -> bool:
        if not isinstance(data, dict) or "agent_01_hooks" not in data:
            return False
        hooks = data["agent_01_hooks"]
        if not isinstance(hooks, list) or len(hooks) != 3:
            return False

        required_keys = [
            "hook_id",
            "hook_approach",
            "visual_camera_action",
            "foley_sfx_audio",
            "verbal_text_overlay",
            "retention_psychology_trigger",
            "pacing_tempo"
        ]

        for hook in hooks:
            if not isinstance(hook, dict):
                return False
            for key in required_keys:
                if key not in hook:
                    return False
        return True

    def execute(self, state: dict) -> dict:
        target_agent = state.get("pipeline_status", {}).get("next_agent", "Ai_Agent_01")
        if target_agent != "Ai_Agent_01":
            print(f"[{self.agent_name}] Execution skipped. Pipeline queue targeted to: {target_agent}")
            return state

        runtime_data = state.setdefault("runtime_data", {})
        module_scripting = runtime_data.setdefault("module_a_scripting", {})

        if "agent_01_hooks" in module_scripting:
            del module_scripting["agent_01_hooks"]
            print(f"[{self.agent_name}] Idempotency Sweep: Cleared legacy hook data.")

        core_topic = runtime_data.get("core_topic", "")
        if not core_topic:
            core_topic = state.get("user_prompt", "")
        if not core_topic:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: Neither 'core_topic' nor 'user_prompt' found in state.")

        global_config = state.get("global_config", {})
        content_format = global_config.get("content_format", runtime_data.get("content_format", "Dynamic Short Narrative"))
        vibe_tempo = global_config.get("vibe_tempo", runtime_data.get("vibe_tempo", "Adaptive Dynamic Rhythm"))
        animation_dna = global_config.get("animation_dna", runtime_data.get("animation_dna", "Procedural Graphics Engine"))
        genre_style = global_config.get("genre_style", runtime_data.get("genre_style", "Universal Genre"))
        master_theme = runtime_data.get("master_theme_blueprint", f"{genre_style} - {content_format}")

        prompt = (
            f"You are the OmniMatrix Universal Hook Designer.\n"
            f"Adapt your creative persona, pacing, and visual directives strictly to these dynamically injected parameters:\n"
            f"- Topic: '{core_topic}'\n"
            f"- Master Theme / Aesthetic: '{master_theme}'\n"
            f"- Content Format: '{content_format}' (e.g., Phonk Short, Nostalgia Essay, Documentary, Anime, Meme, Gaming, Cinematic)\n"
            f"- Vibe & Acoustic Signature: '{vibe_tempo}'\n"
            f"- Visual DNA: '{animation_dna}'\n"
            f"- Genre Style: '{genre_style}'\n\n"
            f"Instructions:\n"
            f"1. Generate EXACTLY 3 highly tailored opening 3-second hooks optimized for maximum retention on modern digital platforms.\n"
            f"2. Adapt the psychological intensity, vocabulary, visual pacing, and sound design to match the format '{content_format}' and style '{genre_style}' dynamically.\n"
            f"3. Option 1 MUST always be a Pure Environmental/SFX/Acoustic hook with ZERO spoken dialogue (relying purely on visual shock, atmosphere, sound effects, or ambient tension).\n"
            f"4. Options 2 and 3 should explore alternative retention angles suited specifically for the requested format.\n\n"
            f"Return ONLY valid JSON with this exact schema:\n"
            f"{{\n"
            f"  \"agent_01_hooks\": [\n"
            f"    {{\n"
            f"      \"hook_id\": \"hook_option_1\",\n"
            f"      \"hook_approach\": \"Description of approach (e.g., Pure Environmental Silence, High Energy Phonk Drop, Nostalgic Memory Snap)\",\n"
            f"      \"visual_camera_action\": \"Detailed camera movement, lighting, kinetic motion, or visual distortion directive\",\n"
            f"      \"foley_sfx_audio\": \"Exact audio frequency drop, ambient Foley, bass impact, or sound effect directive\",\n"
            f"      \"verbal_text_overlay\": \"Spoken line or onscreen text overlay (Must be 'None' for Option 1)\",\n"
            f"      \"retention_psychology_trigger\": \"Specific psychological trigger used (e.g., Curiosity Gap, Shock Value, Emotional Resonance, Pattern Interrupt)\",\n"
            f"      \"pacing_tempo\": \"Pacing description (e.g., Hyper-Kinetic 140BPM, Glitch Snap, Atmospheric Slow Burn)\"\n"
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
                if self._validate_hook_schema(parsed_json):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Primary Gemini REST API payload validated successfully.")
                    break
                else:
                    raise ValueError("JSON payload schema validation failed (incorrect keys or count).")
            except Exception as e:
                last_error = str(e)
                print(f"[{self.agent_name}] Primary Gemini REST API attempt {attempt} failed: {last_error}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        if not generated_data and self.openai_api_key:
            print(f"[{self.agent_name}] Primary API failed. Activating Rule 14 Dual API Failsafe (OpenAI gpt-4o-mini)...")
            try:
                parsed_json = self._call_openai_failsafe(prompt)
                if self._validate_hook_schema(parsed_json):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Failsafe OpenAI API payload validated successfully.")
            except Exception as e:
                last_error = f"Gemini Error: {last_error} | OpenAI Failsafe Error: {str(e)}"
                print(f"[{self.agent_name}] Failsafe OpenAI API execution failed: {str(e)}")

        if not generated_data:
            raise RuntimeError(f"[{self.agent_name}] CRITICAL EXECUTION FAILURE: All API channels failed. Traceback: {last_error}")

        module_scripting["agent_01_hooks"] = generated_data["agent_01_hooks"]
        if "selected_hook_index" not in module_scripting:
            module_scripting["selected_hook_index"] = 0

        pipeline_status = state.setdefault("pipeline_status", {})
        pipeline_status["last_active_agent"] = "Ai_Agent_01"
        pipeline_status["Ai_Agent_01"] = "COMPLETED"

        state_file_path = state.get("state_file_path")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution completed successfully. 3 universal hooks written for format [{content_format}]. Default selected_hook_index set to 0.")
        return state
