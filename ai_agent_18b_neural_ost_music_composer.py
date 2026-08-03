import os
import re
import sys
import json
import time
import math
import wave
import struct
import random
import urllib.request
import urllib.error

class Ai_Agent_18b_Neural_OST_Music_Composer:
    def __init__(self):
        self.agent_name = "Ai_Agent_18b_Neural_OST_Music_Composer"
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.hf_api_key = os.getenv("HF_API_KEY", os.getenv("HF_TOKEN", ""))
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
                {"role": "system", "content": "You are a master music prompt engineer. Generate strict raw JSON."},
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
        if not isinstance(data, dict) or "ost_prompts" not in data:
            return False
        for ost in data["ost_prompts"]:
            if not all(k in ost for k in ["segment_index", "start_sec", "end_sec", "music_prompt", "duration_needed_sec"]):
                return False
        return True

    def _generate_music_huggingface_rest(self, prompt_text: str, output_path: str) -> bool:
        if not self.hf_api_key:
            print(f"[{self.agent_name}] HF_API_KEY missing. Skipping Hugging Face REST MusicGen.", flush=True)
            return False

        url = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
        headers = {
            "Authorization": f"Bearer {self.hf_api_key.strip()}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": prompt_text}

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

        try:
            print(f"[{self.agent_name}] Prompting Hugging Face MusicGen REST API...", flush=True)
            with urllib.request.urlopen(req, timeout=120) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
            return True
        except Exception as e:
            print(f"[{self.agent_name}] Hugging Face MusicGen API Failed: {str(e)}", flush=True)
            return False

    def _synthesize_procedural_dsp_music(self, prompt_data: dict, bpm: float, output_path: str) -> bool:
        duration = min(float(prompt_data.get("duration_needed_sec", 15.0)), 30.0)
        vibe = str(prompt_data.get("music_prompt", "")).lower()

        sample_rate = 44100
        num_samples = int(duration * sample_rate)

        if any(k in vibe for k in ["phonk", "aggressive", "fast", "action", "combat"]):
            base_freq = 40.0
            rhythm_speed = (bpm / 60.0) * 2.0
            is_ambient = False
        else:
            base_freq = 65.41
            rhythm_speed = (bpm / 60.0) / 2.0
            is_ambient = True

        print(f"[{self.agent_name}] Synthesizing DSP Track. Mode: {'Ambient' if is_ambient else 'Rhythmic Pulse'}", flush=True)

        try:
            with wave.open(output_path, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)

                for i in range(num_samples):
                    t = float(i) / sample_rate

                    drone = math.sin(2 * math.pi * base_freq * t)
                    drone += math.sin(2 * math.pi * (base_freq * 1.5) * t) * 0.5

                    lfo = (math.sin(2 * math.pi * rhythm_speed * t) + 1.0) / 2.0
                    noise = random.uniform(-0.05, 0.05)

                    if is_ambient:
                        val = (drone * 0.4) + noise
                    else:
                        val = (drone * lfo * 0.8) + (math.sin(2 * math.pi * base_freq * 2 * t) * (1.0 - lfo) * 0.3)

                    fade = 1.0
                    if t < 1.0:
                        fade = t
                    elif t > (duration - 1.0):
                        fade = max(0.0, duration - t)

                    val = val * fade * 0.4
                    val = max(-1.0, min(1.0, val))

                    packed_val = struct.pack('h', int(val * 32767.0))
                    wav_file.writeframes(packed_val)

            return True
        except Exception as e:
            print(f"[{self.agent_name}] Procedural DSP Synthesis failed: {str(e)}", flush=True)
            return False

    def _execute_procedural_fallback(self, bgm_segments: list) -> list:
        prompts = []
        for idx, seg in enumerate(bgm_segments):
            style = str(seg.get("bgm_vibe_style", "cinematic-ambient")).lower()
            start = float(seg.get("start_sec", 0.0))
            end = float(seg.get("end_sec", 15.0))
            dur = max(end - start, 10.0)

            prompt_text = f"Generative background track in style of {style}. "
            if any(k in style for k in ["aggressive", "phonk", "fast"]):
                prompt_text += "Heavy bass rhythm, fast tempo, dark distorted 808 pulse."
            else:
                prompt_text += "Smooth cinematic ambient pad, low tempo, deep emotional atmosphere."

            prompts.append({
                "segment_index": idx,
                "start_sec": start,
                "end_sec": end,
                "music_prompt": prompt_text,
                "duration_needed_sec": dur
            })
        return prompts

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

        audio_export_dir = os.path.join(workspace_dir, "exports", "ost_tracks")
        os.makedirs(audio_export_dir, exist_ok=True)

        for filename in os.listdir(audio_export_dir):
            file_path = os.path.join(audio_export_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"[{self.agent_name}] Idempotency sweep executed. Legacy OST tracks purged.", flush=True)

        runtime_data = state.setdefault("runtime_data", {})
        module_audio = runtime_data.setdefault("module_b_audio", {})

        bgm_map = module_audio.get("agent_18_bgm_automation_map", {})
        bgm_segments = bgm_map.get("bgm_automation_segments", [])

        beat_map = module_audio.get("agent_14_beat_map", {})
        bpm = float(beat_map.get("target_bpm", 130))

        if not bgm_segments:
            print(f"[{self.agent_name}] WARNING: 'agent_18_bgm_automation_map' missing. Using baseline fallback segment.", flush=True)
            bgm_segments = [{"start_sec": 0.0, "end_sec": 30.0, "bgm_vibe_style": "cinematic-ambient-hybrid"}]

        global_config = state.get("global_config", {})
        medium = global_config.get("medium", "Dynamic")
        rendering = global_config.get("rendering_engine", "Dynamic")
        color = global_config.get("color_lighting", "Dynamic")
        kinetic = global_config.get("kinetic_framing", "Dynamic")

        print(f"[{self.agent_name}] Neural Music Composer designing prompts for {len(bgm_segments)} segments...", flush=True)

        prompt = (
            f"You are the OmniMatrix Neural OST Composer Prompt Architect.\n"
            f"Convert the following BGM automation segments into hyper-descriptive prompts for Meta MusicGen.\n\n"
            f"4-Axis Visual DNA Context:\n"
            f"- Medium: '{medium}'\n"
            f"- Rendering: '{rendering}'\n"
            f"- Color: '{color}'\n"
            f"- Kinetic Framing: '{kinetic}'\n"
            f"Base BPM: {bpm}\n\n"
            f"BGM Automation Segments:\n{json.dumps(bgm_segments, indent=2)}\n\n"
            f"CRITICAL DIRECTIVES:\n"
            f"1. For EACH segment, craft a highly descriptive 'music_prompt' detailing instruments, mood, tempo, and acoustic texture (e.g. 'dark aggressive drift phonk, distorted 808 bass, 130 bpm, fast gated snare').\n"
            f"2. Calculate 'duration_needed_sec' as (end_sec - start_sec).\n"
            f"3. Return ONLY valid JSON matching this schema:\n"
            f"{{\n"
            f"  \"ost_prompts\": [\n"
            f"    {{\n"
            f"      \"segment_index\": 0,\n"
            f"      \"start_sec\": 0.0,\n"
            f"      \"end_sec\": 12.5,\n"
            f"      \"music_prompt\": \"dark synthwave pulse, heavy 808 bass, gated drums, cinematic tension\",\n"
            f"      \"duration_needed_sec\": 12.5\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        generated_data = None
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{self.agent_name}] Prompting Music Composer AI (Attempt {attempt})...", flush=True)
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
                last_error = f"Gemini: {last_error} | OpenAI: {str(e)}"

        if not generated_data:
            print(f"[{self.agent_name}] ALL AI CORES FAILED. Engaging Procedural Fallback. Traceback: {last_error}", flush=True)
            procedural_prompts = self._execute_procedural_fallback(bgm_segments)
            generated_data = {"ost_prompts": procedural_prompts}

        generated_tracks = []

        for ost in generated_data["ost_prompts"]:
            idx = ost.get("segment_index", 0)
            prompt_text = ost.get("music_prompt", "")
            file_name = f"ost_track_seg_{idx:03d}.wav"
            full_audio_path = os.path.join(audio_export_dir, file_name)

            success = self._generate_music_huggingface_rest(prompt_text, full_audio_path)

            if not success:
                print(f"[{self.agent_name}] HF API failed for segment {idx}. Engaging Offline Mathematical DSP Engine...", flush=True)
                success = self._synthesize_procedural_dsp_music(ost, bpm, full_audio_path)

            if success:
                ost["generated_audio_path"] = full_audio_path
                generated_tracks.append(ost)
                print(f"[{self.agent_name}] Secured OST Track for Segment {idx}: {file_name}", flush=True)
            else:
                print(f"[{self.agent_name}] CRITICAL: Audio Generation failed completely for Segment {idx}", flush=True)

        module_audio["agent_18b_custom_ost_tracks"] = generated_tracks

        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution complete. Custom Neural OST Tracks compiled and locked.", flush=True)
        return state
