import os
import re
import sys
import json
import time
import urllib.request
import urllib.error

class Ai_Agent_18_Adaptive_BGM_Vibe_Matcher:
    def __init__(self):
        self.agent_name = "Ai_Agent_18_Adaptive_BGM_Vibe_Matcher"
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
                {"role": "system", "content": "You are a master cinematic music supervisor. Generate strict raw JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.8
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
        if not isinstance(data, dict) or "bgm_automation_segments" not in data:
            return False
        for seg in data["bgm_automation_segments"]:
            if not all(k in seg for k in ["start_sec", "end_sec", "bgm_vibe_style", "target_bgm_volume_db", "ffmpeg_audio_filter"]):
                return False
        return True

    def _execute_procedural_fallback(self, narrative_cues: list, kinetic_framing: str) -> list:
        segments = []
        is_action = any(k in kinetic_framing.lower() for k in ["fast", "action", "hyper", "phonk"])
        
        for cue in narrative_cues:
            start = float(cue.get("start_sec", 0.0))
            end = float(cue.get("end_sec", 5.0))
            
            if is_action:
                style = "aggressive-drift-phonk-bass"
                vol = -10.0
                filter_str = f"volume={vol}dB,highpass=f=100"
            else:
                style = "cinematic-orchestral-ambient-drone"
                vol = -18.0
                filter_str = f"volume={vol}dB,lowpass=f=8000"

            segments.append({
                "start_sec": start,
                "end_sec": end,
                "bgm_vibe_style": style,
                "target_bgm_volume_db": vol,
                "ffmpeg_audio_filter": filter_str,
                "vibe_shift_note": "Procedural fallback BGM mapping."
            })
        return segments

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")

        if target_agent and "18" not in target_agent and target_agent != self.agent_name:
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

        if "agent_18_bgm_automation_map" in module_audio:
            del module_audio["agent_18_bgm_automation_map"]
            print(f"[{self.agent_name}] Idempotency sweep executed. Legacy BGM map purged.", flush=True)

        global_timeline = module_audio.get("agent_12_global_timestamps", [])
        
        narrative_cues = []
        if global_timeline:
            for frame in global_timeline:
                narrative_cues.append({
                    "start_sec": frame.get("global_frame_start_sec", 0.0),
                    "end_sec": frame.get("global_frame_end_sec", 5.0),
                    "text_context": " ".join([w.get("word_raw", "") for w in frame.get("words_global_alignment", [])])
                })
        else:
            narrative_cues.append({"start_sec": 0.0, "end_sec": 60.0, "text_context": "Dynamic visual montage sequence."})

        global_config = state.get("global_config", {})
        medium = global_config.get("medium", "Dynamic")
        rendering = global_config.get("rendering_engine", "Dynamic")
        color = global_config.get("color_lighting", "Dynamic")
        kinetic = global_config.get("kinetic_framing", "Dynamic")

        print(f"[{self.agent_name}] AI Limitless Music Supervisor analyzing {len(narrative_cues)} narrative blocks...", flush=True)

        prompt = (
            f"You are the OmniMatrix Cinematic Music Supervisor.\n"
            f"Invent dynamic background music (BGM) vibe parameters based on the narrative tension and 4-Axis DNA.\n\n"
            f"4-Axis Visual DNA Context:\n"
            f"- Medium: '{medium}'\n"
            f"- Rendering: '{rendering}'\n"
            f"- Color: '{color}'\n"
            f"- Kinetic Framing: '{kinetic}'\n\n"
            f"Narrative Cues / Dialogues:\n{json.dumps(narrative_cues, indent=2)}\n\n"
            f"CRITICAL DIRECTIVES:\n"
            f"1. Do not use generic genres like 'Sad' or 'Happy'. Invent detailed hybrid sub-genres in 'bgm_vibe_style' (e.g., 'cyberpunk-synth-pulse', 'ethereal-orchestral-drone').\n"
            f"2. Provide target volumes (e.g., -25.0dB for heavy dialogue, -8.0dB for action drops).\n"
            f"3. Generate a pure 'ffmpeg_audio_filter' string for this track section (e.g., 'volume=-15dB,lowpass=f=6000').\n"
            f"4. Group the timeline into logical musical chapters (don't create 50 segments, group them into 3 to 5 main thematic blocks based on the time).\n"
            f"5. Return ONLY valid JSON matching this schema:\n"
            f"{{\n"
            f"  \"bgm_automation_segments\": [\n"
            f"    {{\n"
            f"      \"start_sec\": 0.0,\n"
            f"      \"end_sec\": 12.5,\n"
            f"      \"bgm_vibe_style\": \"dark-synthwave-tension-build\",\n"
            f"      \"target_bgm_volume_db\": -18.5,\n"
            f"      \"ffmpeg_audio_filter\": \"volume=-18.5dB,highpass=f=200\",\n"
            f"      \"vibe_shift_note\": \"Introduction building tension before action.\"\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        generated_data = None
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{self.agent_name}] Prompting Music AI (Attempt {attempt})...", flush=True)
                parsed_json = self._call_gemini_rest(prompt)
                if self._validate_schema(parsed_json):
                    generated_data = parsed_json
                    break
                else:
                    raise ValueError("JSON schema validation failed.")
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
                last_error = f"Gemini: {last_error} | OpenAI: {str(e)}"

        if not generated_data:
            print(f"[{self.agent_name}] ALL AI CORES FAILED. Engaging Math DSP Fallback. Traceback: {last_error}", flush=True)
            procedural_blueprints = self._execute_procedural_fallback(narrative_cues, kinetic)
            generated_data = {"bgm_automation_segments": procedural_blueprints}

        module_audio["agent_18_bgm_automation_map"] = generated_data

        pipeline_status["last_active_agent"] = self.agent_name
        
        target_agent = "Ai_Agent_18b"
        pipeline_status["next_agent"] = target_agent
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution complete. {len(generated_data['bgm_automation_segments'])} limitles BGM automation curves locked.", flush=True)
        return state
