import os
import re
import sys
import json
import time
import math
import struct
import random
import wave
import urllib.request
import urllib.error

class Ai_Agent_17_Autonomous_SFX_Alchemist_Synthesizer:
    def __init__(self):
        self.agent_name = "Ai_Agent_17_Autonomous_SFX_Alchemist_Synthesizer"
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
                {"role": "system", "content": "You are a master Audio Synthesizer Alchemist. Generate strict raw JSON."},
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
        if not isinstance(data, dict) or "synthesized_sfx_parameters" not in data:
            return False
        for sfx in data["synthesized_sfx_parameters"]:
            if not all(k in sfx for k in ["timestamp_sec", "duration", "start_freq", "end_freq", "waveform", "noise_mix", "fm_mod"]):
                return False
        return True

    def _synthesize_advanced_wav(self, profile: dict, filepath: str) -> bool:
        duration = float(profile.get("duration", 1.0))
        start_freq = float(profile.get("start_freq", 200.0))
        end_freq = float(profile.get("end_freq", 50.0))
        waveform = str(profile.get("waveform", "sine")).lower()
        noise_mix = float(profile.get("noise_mix", 0.0))
        fm_mod = float(profile.get("fm_mod", 0.0))

        sample_rate = 44100
        num_samples = int(duration * sample_rate)

        try:
            with wave.open(filepath, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)

                for i in range(num_samples):
                    t = float(i) / sample_rate
                    progress = t / duration

                    if progress < 0.02:
                        env = progress / 0.02
                    else:
                        env = math.exp(-6.0 * (progress - 0.02))

                    current_freq = start_freq * (1.0 - progress) + end_freq * progress

                    modulator = 0.0
                    if fm_mod > 0:
                        modulator = math.sin(2 * math.pi * (current_freq * fm_mod) * t)

                    phase = 2 * math.pi * current_freq * t + (modulator * fm_mod)

                    if waveform == "sawtooth":
                        val = 2.0 * (phase / (2 * math.pi) - math.floor(0.5 + phase / (2 * math.pi)))
                    elif waveform == "square":
                        val = 1.0 if math.sin(phase) > 0 else -1.0
                    else:
                        val = math.sin(phase)

                    if noise_mix > 0:
                        val = (val * (1.0 - noise_mix)) + (random.uniform(-1.0, 1.0) * noise_mix)

                    val *= env

                    val = max(-1.0, min(1.0, val))
                    packed_val = struct.pack('h', int(val * 32767.0))
                    wav_file.writeframes(packed_val)

            return True
        except Exception as e:
            print(f"[{self.agent_name}] Wav synthesis failed: {str(e)}", flush=True)
            return False

    def _execute_procedural_fallback(self, action_cues: list) -> list:
        sfx_list = []
        for cue in action_cues:
            sfx_list.append({
                "timestamp_sec": float(cue.get("timestamp_sec", 0.0)),
                "duration": 1.0,
                "start_freq": 150.0,
                "end_freq": 30.0,
                "waveform": "square",
                "noise_mix": 0.4,
                "fm_mod": 0.2
            })
        return sfx_list

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")

        if target_agent and "17" not in target_agent and target_agent != self.agent_name:
            print(f"[{self.agent_name}] Execution skipped. Queue targeted to: {target_agent}", flush=True)
            return state

        workspace_dir = state.get("workspace_dir", "")
        if not workspace_dir:
            workspace_dir = state.get("state_file_path", "")
            if workspace_dir:
                workspace_dir = os.path.dirname(workspace_dir)
            else:
                raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: workspace_dir missing.")

        sfx_export_dir = os.path.join(workspace_dir, "exports", "sfx_assets")
        os.makedirs(sfx_export_dir, exist_ok=True)

        for filename in os.listdir(sfx_export_dir):
            file_path = os.path.join(sfx_export_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"[{self.agent_name}] Idempotency sweep executed. Legacy SFX assets purged.", flush=True)

        runtime_data = state.setdefault("runtime_data", {})
        module_audio = runtime_data.setdefault("module_b_audio", {})

        beat_map_data = module_audio.get("agent_14_beat_map", {})
        events = beat_map_data.get("beat_sync_events", [])
        
        action_cues = []
        for ev in events:
            if ev.get("impact_intensity", 0.0) >= 0.5:
                action_cues.append({
                    "timestamp_sec": ev.get("timestamp_sec"),
                    "action_note": ev.get("editor_action_note", "Visual Impact")
                })

        if not action_cues:
            print(f"[{self.agent_name}] No dynamic action cues found for SFX generation.", flush=True)
            pipeline_status["last_active_agent"] = self.agent_name
            pipeline_status[self.agent_name] = "COMPLETED"
            return state

        global_config = state.get("global_config", {})
        medium = global_config.get("medium", "Dynamic")
        rendering = global_config.get("rendering_engine", "Dynamic")
        color = global_config.get("color_lighting", "Dynamic")
        kinetic = global_config.get("kinetic_framing", "Dynamic")

        print(f"[{self.agent_name}] AI Alchemist designing DSP blueprints for {len(action_cues)} visual cues based on 4-Axis DNA...", flush=True)

        prompt = (
            f"You are the OmniMatrix SFX Alchemist Engineer.\n"
            f"Design purely mathematical sound effect parameters for the following action triggers.\n\n"
            f"4-Axis Visual DNA Context:\n"
            f"- Medium: '{medium}'\n"
            f"- Rendering: '{rendering}'\n"
            f"- Color: '{color}'\n"
            f"- Kinetic Framing: '{kinetic}'\n\n"
            f"Action Cues:\n{json.dumps(action_cues, indent=2)}\n\n"
            f"CRITICAL DIRECTIVES:\n"
            f"Output a DSP recipe for EACH cue using these parameter bounds:\n"
            f"- 'duration': 0.2 to 3.0 seconds.\n"
            f"- 'start_freq' & 'end_freq': 20.0 to 3000.0 Hz.\n"
            f"- 'waveform': strictly one of ['sine', 'sawtooth', 'square'].\n"
            f"- 'noise_mix': 0.0 to 1.0 (0.0 is pure tone, 1.0 is pure white noise. Use high noise for explosions/impacts).\n"
            f"- 'fm_mod': 0.0 to 5.0 (Use high for lasers, metallic sounds, and glitches).\n\n"
            f"Return ONLY valid JSON matching this schema:\n"
            f"{{\n"
            f"  \"synthesized_sfx_parameters\": [\n"
            f"    {{\n"
            f"      \"timestamp_sec\": 1.5,\n"
            f"      \"duration\": 0.8,\n"
            f"      \"start_freq\": 800,\n"
            f"      \"end_freq\": 40,\n"
            f"      \"waveform\": \"sawtooth\",\n"
            f"      \"noise_mix\": 0.5,\n"
            f"      \"fm_mod\": 0.2\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        generated_data = None
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{self.agent_name}] Prompting SFX AI (Attempt {attempt})...", flush=True)
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
            procedural_blueprints = self._execute_procedural_fallback(action_cues)
            generated_data = {"synthesized_sfx_parameters": procedural_blueprints}

        final_sfx_assets = []
        print(f"[{self.agent_name}] DSP Engine Active: Baking {len(generated_data['synthesized_sfx_parameters'])} .wav files from scratch...", flush=True)

        for idx, sfx in enumerate(generated_data["synthesized_sfx_parameters"]):
            ts = sfx.get("timestamp_sec")
            filename = f"sfx_synth_{idx:03d}_{str(ts).replace('.', '_')}.wav"
            filepath = os.path.join(sfx_export_dir, filename)
            
            if self._synthesize_advanced_wav(sfx, filepath):
                sfx["synthesized_file_path"] = filepath
                final_sfx_assets.append(sfx)

        module_audio["agent_17_synthesized_sfx"] = final_sfx_assets

        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Execution complete. {len(final_sfx_assets)} high-quality pure .wav assets generated from mathematical code.", flush=True)
        return state
