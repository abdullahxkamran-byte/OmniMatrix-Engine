import os
import re
import sys
import json
import time
import urllib.request
import urllib.error

class Ai_Agent_06_Word_Count_Guard:
    def __init__(self):
        self.agent_name = "Ai_Agent_06_Word_Count_Guard"
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
            raise ValueError(f"[{self.agent_name}] GEMINI_API_KEY missing or invalid.")
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.gemini_api_key
        }
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                text_content = res_json['candidates'][0]['content']['parts'][0]['text']
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
                {"role": "system", "content": "You are a script pacing editor. Generate strict raw JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                content = res_json["choices"][0]["message"]["content"]
                return self._clean_json_response(content)
        except urllib.error.HTTPError as http_err:
            raise RuntimeError(f"[{self.agent_name}] OpenAI API Error [{http_err.code}]: {http_err.read().decode('utf-8')}")
        except Exception as e:
            raise RuntimeError(f"[{self.agent_name}] OpenAI Failsafe Error: {str(e)}")

    def _calculate_dynamic_wps_via_ai(self, medium: str, rendering_engine: str, color_lighting: str, kinetic_framing: str) -> float:
        prompt = (
            f"Determine the absolute optimal spoken Words-Per-Second (WPS) speed based on this 4-Axis Style Matrix:\n"
            f"Medium: {medium}\n"
            f"Rendering Engine: {rendering_engine}\n"
            f"Color & Lighting: {color_lighting}\n"
            f"Kinetic Framing: {kinetic_framing}\n\n"
            f"Return ONLY valid JSON: {{\"target_wps\": 2.8}}"
        )

        last_error = ""
        for attempt in range(1, self.max_retries + 1):
            try:
                parsed = self._call_gemini_rest(prompt)
                if "target_wps" in parsed:
                    return max(1.5, min(float(parsed["target_wps"]), 4.0))
            except Exception as e:
                last_error = str(e)
                if attempt == self.max_retries and self.openai_api_key:
                    try:
                        parsed_fail = self._call_openai_failsafe(prompt)
                        if "target_wps" in parsed_fail:
                            return max(1.5, min(float(parsed_fail["target_wps"]), 4.0))
                    except Exception as fail_e:
                        last_error += f" | Failsafe: {str(fail_e)}"
                time.sleep(self.retry_delay)
        
        raise RuntimeError(f"[{self.agent_name}] WPS Calculation failed. Traceback: {last_error}")

    def _ai_rewrite_compress(self, voiceover: str, max_words: int, medium: str, rendering_engine: str, color_lighting: str, kinetic_framing: str) -> str:
        prompt = (
            f"Compress the sentence to fit strict temporal bounds WITHOUT losing narrative impact.\n"
            f"Medium: {medium}\n"
            f"Render: {rendering_engine}\n"
            f"Color: {color_lighting}\n"
            f"Framing: {kinetic_framing}\n"
            f"Max Allowed Words: {max_words}\n"
            f"Original Text: \"{voiceover}\"\n"
            f"Return ONLY valid JSON: {{\"optimized_text\": \"...\"}}"
        )

        for attempt in range(1, self.max_retries + 1):
            try:
                parsed = self._call_gemini_rest(prompt)
                if "optimized_text" in parsed:
                    return parsed["optimized_text"]
            except Exception:
                if attempt == self.max_retries and self.openai_api_key:
                    try:
                        parsed_fail = self._call_openai_failsafe(prompt)
                        if "optimized_text" in parsed_fail:
                            return parsed_fail["optimized_text"]
                    except Exception:
                        pass
                time.sleep(self.retry_delay)
        return ""

    def execute(self, state: dict) -> dict:
        target_agent = state.get("pipeline_status", {}).get("next_agent", "Ai_Agent_06")
        if target_agent != "Ai_Agent_06":
            print(f"[{self.agent_name}] Execution skipped. Pipeline queue targeted to: {target_agent}")
            return state

        runtime_data = state.setdefault("runtime_data", {})
        module_scripting = runtime_data.setdefault("module_a_scripting", {})

        if "agent_06_word_guard" in module_scripting:
            del module_scripting["agent_06_word_guard"]
            print(f"[{self.agent_name}] Idempotency sweep executed.")

        topic = runtime_data.get("core_topic", state.get("user_prompt", "Unknown Target"))
        global_config = state.get("global_config", {})
        
        medium = global_config.get("medium", "Dynamic/Unbound")
        rendering_engine = global_config.get("rendering_engine", "Dynamic/Unbound")
        color_lighting = global_config.get("color_lighting", "Dynamic/Unbound")
        kinetic_framing = global_config.get("kinetic_framing", "Dynamic/Unbound")

        agent_03_data = module_scripting.get("agent_03_storyboard", {})
        frames = agent_03_data if isinstance(agent_03_data, list) else agent_03_data.get("storyboard_frames", [])

        if not frames:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: Storyboard frames missing from Agent 03.")

        target_wps = self._calculate_dynamic_wps_via_ai(medium, rendering_engine, color_lighting, kinetic_framing)
        print(f"[{self.agent_name}] Processed Pacing Speed: {round(target_wps, 2)} WPS")

        audit_queue = []
        optimization_applied = False

        for frame in frames:
            f_idx = frame.get("frame_index", 1)
            start = float(frame.get("timestamp_start", 0.0))
            end = float(frame.get("timestamp_end", start + 3.0))
            duration = max(end - start, 1.0)
            voiceover = frame.get("spoken_audio", "").strip()

            if voiceover.lower() == "none" or not voiceover:
                continue

            word_count = len(voiceover.split())
            max_recommended_words = max(int(duration * target_wps), 1)
            
            pacing_status = "safe"
            optimized_text = voiceover

            if word_count > max_recommended_words:
                pacing_status = "optimized_safe"
                optimization_applied = True
                
                ai_rewritten = self._ai_rewrite_compress(voiceover, max_recommended_words, medium, rendering_engine, color_lighting, kinetic_framing)
                
                if ai_rewritten and len(ai_rewritten.split()) <= (max_recommended_words + 3): 
                    optimized_text = ai_rewritten
                else:
                    words = voiceover.split()
                    optimized_text = " ".join(words[:max_recommended_words])
                    optimized_text = re.sub(r"[^\w]$", "", optimized_text) + "."
                    
                frame["spoken_audio"] = optimized_text

            audit_queue.append({
                "frame_index": f_idx,
                "duration_seconds": round(duration, 2),
                "original_word_count": word_count,
                "optimized_word_count": len(optimized_text.split()),
                "max_allowed_words": max_recommended_words,
                "pacing_status": pacing_status
            })

        audit_report = {
            "source_topic": topic,
            "target_wps_applied": round(target_wps, 2),
            "optimization_triggered": optimization_applied,
            "timeline_audits": audit_queue
        }
        
        module_scripting["agent_03_storyboard"] = frames
        module_scripting["agent_06_word_guard"] = audit_report
        
        pipeline_status = state.setdefault("pipeline_status", {})
        pipeline_status["last_active_agent"] = "Ai_Agent_06"
        pipeline_status["Ai_Agent_06"] = "COMPLETED"

        state_file_path = state.get("state_file_path")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        return state
