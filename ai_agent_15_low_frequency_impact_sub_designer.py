import os
import re
import sys
import json
import time
import urllib.request
import urllib.error

class Ai_Agent_15_Low_Frequency_Impact_Sub_Designer:
    def __init__(self):
        self.agent_name = "Ai_Agent_15_Low_Frequency_Impact_Sub_Designer"
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
                {"role": "system", "content": "You are a master Audio DSP Architect. Generate strict raw JSON."},
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
        if not isinstance(data, dict) or "sub_profiles" not in data:
            return False
        for prof in data["sub_profiles"]:
            if not all(k in prof for k in ["timestamp_sec", "start_frequency_hz", "end_frequency_hz", "sweep_duration_seconds", "waveform_type", "ffmpeg_aevalsrc"]):
                return False
        return True

    def _execute_procedural_fallback(self, heavy_events: list, kinetic_framing: str) -> list:
        profiles = []
        is_aggressive = any(k in kinetic_framing.lower() for k in ["fast", "action", "hyper", "phonk"])
        
        for trig in heavy_events:
            ts = float(trig.get("timestamp_sec", 0.0))
            intensity = float(trig.get("impact_intensity", 0.8))

            if not is_aggressive:
                start_freq = int(50 + (intensity * 10))
                end_freq = int(20 + ((1.0 - intensity) * 5))
                decay = round(1.5 + (intensity * 1.5), 2)
                waveform = "pure-sine"
                aeval_str = f"aevalsrc='sin(2*PI*({start_freq}-({start_freq}-{end_freq})*t/{decay})*t)':d={decay}"
            else:
                start_freq = int(80 + (intensity * 20))
                end_freq = int(30 + ((1.0 - intensity) * 10))
                decay = round(0.5 + (intensity * 0.5), 2)
                waveform = "hard-saw"
                aeval_str = f"aevalsrc='(2/PI)*asin(sin(2*PI*({start_freq}-({start_freq}-{end_freq})*t/{decay})*t))':d={decay}"

            profiles.append({
                "timestamp_sec": ts,
                "start_frequency_hz": start_freq,
                "end_frequency_hz": end_freq,
                "sweep_duration_seconds": decay,
                "waveform_type": waveform,
                "ffmpeg_aevalsrc": aeval_str
            })
        return profiles

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")

        if target_agent and "15" not in target_agent and target_agent != self.agent_name:
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

        beat_map_data = module_audio.get("agent_14_beat_map", {})
        if not beat_map_data:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: 'agent_14_beat_map' missing.")

        all_events = beat_map_data.get("beat_sync_events", [])
        heavy_events = [ev for ev in all_events if ev.get("impact_intensity", 0.0) >= 0.7]

        if not heavy_events and all_events:
            heavy_events = [all_events[0]]

        if not heavy_events:
            print(f"[{self.agent_name}] No heavy impact points found to design sub-bass for.", flush=True)
            pipeline_status["last_active_agent"] = self.agent_name
            pipeline_status[self.agent_name] = "COMPLETED"
            return state

        global_config = state.get("global_config", {})
        kinetic_framing = global_config.get("kinetic_framing", "Dynamic/Unbound")

        print(f"[{self.agent_name}] Designing mathematical sub-bass architecture for {len(heavy_events)} impact points...", flush=True)

        prompt = (
            f"You are an expert Audio DSP Synthesizer Engineer for OmniMatrix.\n"
            f"Your task is to design low-frequency sub-bass sweeps/drops based on these heavy visual impact points.\n\n"
            f"Kinetic Framing Context: '{kinetic_framing}'\n"
            f"If context is 'Cinematic/Dramatic', design deep pure-sine rumbles (50Hz -> 20Hz, 1.5s+).\n"
            f"If context is 'Phonk/Action', design aggressive short-burst distorted/saw waveforms (80Hz -> 30Hz, 0.5s).\n\n"
            f"Impact Points to Synthesize:\n{json.dumps(heavy_events, indent=2)}\n\n"
            f"CRITICAL DIRECTIVES:\n"
            f"1. Generate an exact 'ffmpeg_aevalsrc' string that can natively synthesize this sound without any audio files.\n"
            f"   - For Pure-Sine sweep: \"aevalsrc='sin(2*PI*(START_FREQ-(START_FREQ-END_FREQ)*t/DUR)*t)':d=DUR\"\n"
            f"   - For Saw/Distorted sweep: \"aevalsrc='(2/PI)*asin(sin(2*PI*(START_FREQ-(START_FREQ-END_FREQ)*t/DUR)*t))':d=DUR\"\n"
            f"2. Return ONLY valid JSON matching this exact schema:\n"
            f"{{\n"
            f"  \"sub_profiles\": [\n"
            f"    {{\n"
            f"      \"timestamp_sec\": 2.50,\n"
            f"      \"start_frequency_hz\": 60,\n"
            f"      \"end_frequency_hz\": 25,\n"
            f"      \"sweep_duration_seconds\": 1.5,\n"
            f"      \"waveform_type\": \"pure-sine\",\n"
            f"      \"ffmpeg_aevalsrc\": \"aevalsrc='sin(2*PI*(60-(60-25)*t/1.5)*t)':d=1.5\"\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        generated_data = None
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{self.agent_name}] Prompting DSP Architect AI (Attempt {attempt})...", flush=True)
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
            print(f"[{self.agent_name}] ALL AI CORES FAILED. Engaging Procedural DSP Math Engine. Traceback: {last_error}", flush=True)
            procedural_profiles = self._execute_procedural_fallback(heavy_events, kinetic_framing)
            generated_data = {"sub_profiles": procedural_profiles}

        for event in all_events:
            event.pop("sub_bass_dsp_blueprint", None)

        for event in all_events:
            for sub in generated_data["sub_profiles"]:
                if round(event.get("timestamp_sec", 0.0), 3) == round(sub.get("timestamp_sec", 0.0), 3):
                    event["sub_bass_dsp_blueprint"] = sub
                    break

        module_audio["agent_14_beat_map"]["beat_sync_events"] = all_events

        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution completed. Sub-bass DSP synthesis nodes locked.", flush=True)
        return state
