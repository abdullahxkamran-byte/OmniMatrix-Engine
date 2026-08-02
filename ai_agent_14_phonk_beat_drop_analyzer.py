import os
import re
import sys
import json
import time
import urllib.request
import urllib.error

class Ai_Agent_14_Phonk_Beat_Drop_Analyzer:
    def __init__(self):
        self.agent_name = "Ai_Agent_14_Phonk_Beat_Drop_Analyzer"
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
            raise ValueError(f"[{self.agent_name}] CRITICAL: GEMINI_API_KEY missing.")

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
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
                {"role": "system", "content": "You are a master VFX choreography director. Generate strict raw JSON."},
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
        if not isinstance(data, dict) or "beat_sync_events" not in data:
            return False
        if not isinstance(data["beat_sync_events"], list):
            return False
        for event in data["beat_sync_events"]:
            if not all(k in event for k in ["timestamp_sec", "event_type", "impact_intensity"]):
                return False
        return True

    def _execute_procedural_fallback(self, total_duration: float, kinetic_framing: str) -> list:
        events = []
        current_time = 0.0
        
        framing_lower = kinetic_framing.lower()
        if any(keyword in framing_lower for keyword in ["fast", "action", "combat", "hyper"]):
            interval = 2.0
            event_type = "bass-drop-flash"
        else:
            interval = 5.0
            event_type = "soft-sub-bass-zoom"

        while current_time < total_duration:
            if current_time > 0:
                events.append({
                    "timestamp_sec": round(current_time, 3),
                    "event_type": event_type,
                    "impact_intensity": 0.75,
                    "editor_action_note": "Procedural fallback sync point."
                })
            current_time += interval
            
        return events

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")

        if target_agent and "14" not in target_agent and target_agent != self.agent_name:
            print(f"[{self.agent_name}] Execution skipped. Queue targeted to: {target_agent}", flush=True)
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

        if "agent_14_beat_map" in module_audio:
            del module_audio["agent_14_beat_map"]
            print(f"[{self.agent_name}] Idempotency sweep executed. Legacy beat map purged.", flush=True)

        global_timeline = module_audio.get("agent_12_global_timestamps", [])
        if not global_timeline:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: 'agent_12_global_timestamps' missing.")

        total_duration = 0.0
        if global_timeline:
            total_duration = global_timeline[-1].get("global_frame_end_sec", 0.0)

        global_config = state.get("global_config", {})
        medium = global_config.get("medium", "Dynamic/Unbound")
        rendering_engine = global_config.get("rendering_engine", "Dynamic/Unbound")
        color_lighting = global_config.get("color_lighting", "Dynamic/Unbound")
        kinetic_framing = global_config.get("kinetic_framing", "Dynamic/Unbound")

        lightweight_timeline = []
        for f in global_timeline:
            lightweight_timeline.append({
                "frame": f.get("frame_index"),
                "start": f.get("global_frame_start_sec"),
                "end": f.get("global_frame_end_sec")
            })

        print(f"[{self.agent_name}] Analyzing beat/impact topology for {total_duration}s timeline...", flush=True)

        prompt = (
            f"You are the OmniMatrix Visual-Audio Sync Director.\n"
            f"Analyze this video timeline and map exact timestamps for visual FX impacts (screen shakes, flashes, heavy bass drops, dramatic zooms).\n\n"
            f"4-Axis Visual DNA Context:\n"
            f"- Medium: '{medium}'\n"
            f"- Rendering Engine: '{rendering_engine}'\n"
            f"- Color & Lighting: '{color_lighting}'\n"
            f"- Kinetic Framing/Vibe: '{kinetic_framing}'\n\n"
            f"Total Duration: {total_duration} seconds.\n"
            f"Key Scene Boundaries:\n{json.dumps(lightweight_timeline)}\n\n"
            f"CRITICAL DIRECTIVES:\n"
            f"1. Pace the events based on the 'Kinetic Framing' vibe. If it's fast/combat, place events frequently. If sad/dramatic, place them sparingly on scene transitions.\n"
            f"2. Use event types like: 'bass-drop-flash', 'cowbell-glitch', 'sub-bass-zoom', 'snare-shake', 'scene-fade-transition'.\n"
            f"3. Return ONLY valid JSON matching this exact schema:\n"
            f"{{\n"
            f"  \"beat_sync_events\": [\n"
            f"    {{\n"
            f"      \"timestamp_sec\": 2.50,\n"
            f"      \"event_type\": \"bass-drop-flash\",\n"
            f"      \"impact_intensity\": 0.95,\n"
            f"      \"editor_action_note\": \"Heavy screen shake on word impact.\"\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        generated_data = None
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{self.agent_name}] Prompting Sync Director AI (Attempt {attempt})...", flush=True)
                parsed_json = self._call_gemini_rest(prompt)
                if self._validate_schema(parsed_json):
                    generated_data = parsed_json
                    break
                else:
                    raise ValueError("JSON payload schema validation failed.")
            except Exception as e:
                last_error = str(e)
                time.sleep(self.retry_delay)

        if not generated_data and self.openai_api_key:
            print(f"[{self.agent_name}] Fallback to OpenAI Dual Failsafe...", flush=True)
            try:
                parsed_json = self._call_openai_failsafe(prompt)
                if self._validate_schema(parsed_json):
                    generated_data = parsed_json
            except Exception as e:
                last_error = f"Gemini Error: {last_error} | OpenAI Error: {str(e)}"

        if not generated_data:
            print(f"[{self.agent_name}] ALL AI CORES FAILED. Engaging Procedural Math Fallback Engine. Traceback: {last_error}", flush=True)
            procedural_events = self._execute_procedural_fallback(total_duration, kinetic_framing)
            generated_data = {"beat_sync_events": procedural_events}

        module_audio["agent_14_beat_map"] = generated_data

        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution completed. {len(generated_data['beat_sync_events'])} beat events mapped and locked.", flush=True)
        return state
