import os
import sys
import json
import time
import urllib.request
import urllib.error

class Ai_Agent_05_Story_Arc_Architect:
    def __init__(self):
        self.agent_name = "Ai_Agent_05_Story_Arc_Architect"
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
                    "content": "You are a master narrative arc architect. Generate strict raw JSON matching the requested schema."
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

    def _validate_arc_schema(self, data: dict) -> bool:
        if not isinstance(data, dict) or "arc_phases" not in data:
            return False
        phases = data["arc_phases"]
        if not isinstance(phases, list) or len(phases) == 0:
            return False

        required_keys = [
            "phase_index",
            "phase_name",
            "target_duration_ratio",
            "pacing_frequency",
            "audience_psychology_goal"
        ]

        total_ratio = 0.0
        for phase in phases:
            if not isinstance(phase, dict):
                return False
            for key in required_keys:
                if key not in phase:
                    return False
            
            try:
                total_ratio += float(phase["target_duration_ratio"])
            except ValueError:
                return False

        # Allow slight floating point tolerance around 1.0 (e.g. 0.99 to 1.01)
        if total_ratio < 0.95 or total_ratio > 1.05:
            print(f"[{self.agent_name}] Warning: target_duration_ratio sum is {total_ratio}, expected 1.0", flush=True)

        return True

    def execute(self, state: dict) -> dict:
        target_agent = state.get("pipeline_status", {}).get("next_agent", "Ai_Agent_05")
        if target_agent != "Ai_Agent_05":
            print(f"[{self.agent_name}] Execution skipped. Pipeline queue targeted to: {target_agent}")
            return state

        runtime_data = state.setdefault("runtime_data", {})
        module_scripting = runtime_data.setdefault("module_a_scripting", {})

        if "agent_05_story_arc" in module_scripting:
            del module_scripting["agent_05_story_arc"]
            print(f"[{self.agent_name}] Idempotency Sweep: Cleared legacy arc phase data.")

        core_topic = runtime_data.get("core_topic", state.get("user_prompt", ""))
        global_config = state.get("global_config", {})
        content_format = global_config.get("content_format", runtime_data.get("content_format", "Dynamic Short Narrative"))
        vibe_tempo = global_config.get("vibe_tempo", runtime_data.get("vibe_tempo", "Adaptive Dynamic Rhythm"))
        animation_dna = global_config.get("animation_dna", runtime_data.get("animation_dna", "Procedural Graphics Engine"))
        
        agent_04_data = module_scripting.get("agent_04_tension_peaks", [])
        if not agent_04_data:
            raise ValueError(f"[{self.agent_name}] ERROR: No tension timeline found from Agent 04. Pipeline broken.")

        print(f"[{self.agent_name}] Architecting Story Arc Phases...", flush=True)

        prompt = (
            f"You are the OmniMatrix Supreme Narrative Arc Architect.\n"
            f"Your objective is to analyze the provided tension timeline and structure a multi-stage story arc mapped out chronologically.\n\n"
            f"Context Parameters:\n"
            f"- Topic: '{core_topic}'\n"
            f"- Format/Style: '{content_format}'\n"
            f"- Visual DNA: '{animation_dna}'\n"
            f"- Acoustic Signature: '{vibe_tempo}'\n\n"
            f"Input Tension Timeline:\n{json.dumps(agent_04_data)}\n\n"
            f"Instructions:\n"
            f"1. Dynamically generate the appropriate number of chronological phases/acts (e.g., 3 acts for standard, 5 for cinematic). Do not restrict yourself to hardcoded templates.\n"
            f"2. Define the 'target_duration_ratio' as a decimal float for each phase. THE SUM OF ALL RATIOS MUST EXACTLY EQUAL 1.0 (e.g., 0.2, 0.5, 0.3).\n"
            f"3. Return ONLY valid JSON with this exact schema:\n"
            f"{{\n"
            f"  \"arc_phases\": [\n"
            f"    {{\n"
            f"      \"phase_index\": 1,\n"
            f"      \"phase_name\": \"The Hook / Initialization\",\n"
            f"      \"target_duration_ratio\": 0.15,\n"
            f"      \"pacing_frequency\": \"Fast edit speed, high frequency cuts\",\n"
            f"      \"audience_psychology_goal\": \"Curiosity and pattern interrupt\"\n"
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
                if self._validate_arc_schema(parsed_json):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Primary Gemini REST API payload validated successfully.")
                    break
                else:
                    raise ValueError("JSON payload schema validation failed (missing keys or invalid ratio sums).")
            except Exception as e:
                last_error = str(e)
                print(f"[{self.agent_name}] Primary Gemini REST API attempt {attempt} failed: {last_error}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        if not generated_data and self.openai_api_key:
            print(f"[{self.agent_name}] Primary API failed. Activating Dual API Failsafe (OpenAI gpt-4o-mini)...")
            try:
                parsed_json = self._call_openai_failsafe(prompt)
                if self._validate_arc_schema(parsed_json):
                    generated_data = parsed_json
                    print(f"[{self.agent_name}] Failsafe OpenAI API payload validated successfully.")
            except Exception as e:
                last_error = f"Gemini Error: {last_error} | OpenAI Failsafe Error: {str(e)}"
                print(f"[{self.agent_name}] Failsafe OpenAI API execution failed: {str(e)}")

        if not generated_data:
            raise RuntimeError(f"[{self.agent_name}] CRITICAL EXECUTION FAILURE: All API channels failed. Traceback: {last_error}")

        module_scripting["agent_05_story_arc"] = generated_data["arc_phases"]

        pipeline_status = state.setdefault("pipeline_status", {})
        pipeline_status["last_active_agent"] = "Ai_Agent_05"
        pipeline_status["Ai_Agent_05"] = "COMPLETED"

        state_file_path = state.get("state_file_path")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution completed successfully. Arc Phases Locked!")
        return state
