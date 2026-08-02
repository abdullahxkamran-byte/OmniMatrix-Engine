import os
import re
import sys
import json
import time
import subprocess
import urllib.request
import urllib.error

class Ai_Agent_19_Audio_Mastering_Final_Mixer:
    def __init__(self):
        self.agent_name = "Ai_Agent_19_Audio_Mastering_Final_Mixer"
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
                {"role": "system", "content": "You are an elite Audio Mastering Console Architect. Generate strict raw JSON."},
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
        if not isinstance(data, dict) or "mastering_console_parameters" not in data:
            return False
        params = data["mastering_console_parameters"]
        required_keys = ["target_loudness_lufs", "master_true_peak_limiter_db", "stereo_widening_factor", "low_cut_filter_hz", "vocal_presence_boost_db", "glue_compressor"]
        if not all(k in params for k in required_keys):
            return False
        return True

    def _execute_procedural_fallback(self, kinetic_framing: str) -> dict:
        is_aggressive = any(k in kinetic_framing.lower() for k in ["fast", "action", "hyper", "phonk", "short"])
        
        if is_aggressive:
            lufs, peak, low_cut, widen, vocal = -9.0, -0.2, 35, 1.15, 3.0
            glue = {"threshold_db": -6.0, "ratio": 3.0, "makeup_gain_db": 2.0}
        else:
            lufs, peak, low_cut, widen, vocal = -14.0, -1.0, 25, 1.3, 1.5
            glue = {"threshold_db": -4.0, "ratio": 2.0, "makeup_gain_db": 1.0}

        return {
            "mastering_console_parameters": {
                "target_loudness_lufs": lufs,
                "master_true_peak_limiter_db": peak,
                "stereo_widening_factor": widen,
                "low_cut_filter_hz": low_cut,
                "vocal_presence_boost_db": vocal,
                "glue_compressor": glue,
                "mastering_notes": "Procedural mathematical DSP fallback applied."
            }
        }

    def _build_master_ffmpeg_command(self, audio_manifest: dict, params: dict, output_path: str) -> dict:
        p = params.get("mastering_console_parameters", {})
        lufs = float(p.get("target_loudness_lufs", -14.0))
        peak = float(p.get("master_true_peak_limiter_db", -1.0))
        widen = float(p.get("stereo_widening_factor", 1.2))
        low_cut = int(p.get("low_cut_filter_hz", 30))
        vocal_boost = float(p.get("vocal_presence_boost_db", 2.0))

        glue = p.get("glue_compressor", {})
        c_thresh = float(glue.get("threshold_db", -5.0))
        c_ratio = float(glue.get("ratio", 2.0))
        c_makeup = float(glue.get("makeup_gain_db", 1.0))

        dialogues = audio_manifest.get("dialogue_tracks", [])
        sfx_files = audio_manifest.get("sfx_tracks", [])
        ost_files = audio_manifest.get("ost_tracks", [])

        input_args = []
        filter_parts = []
        mix_inputs = []
        input_count = 0

        for diag in dialogues:
            f_path = diag.get("file_path", "")
            if os.path.exists(f_path):
                input_args.extend(["-i", f_path])
                filter_parts.append(f"[{input_count}:a]volume=1.2,equalizer=f=3000:width_type=h:width=200:g={vocal_boost}[a_diag_{input_count}];")
                mix_inputs.append(f"[a_diag_{input_count}]")
                input_count += 1

        for sfx in sfx_files:
            f_path = sfx.get("synthesized_file_path", "")
            if os.path.exists(f_path):
                input_args.extend(["-i", f_path])
                filter_parts.append(f"[{input_count}:a]volume=0.8[a_sfx_{input_count}];")
                mix_inputs.append(f"[a_sfx_{input_count}]")
                input_count += 1

        for ost in ost_files:
            f_path = ost.get("generated_audio_path", "")
            if os.path.exists(f_path):
                input_args.extend(["-i", f_path])
                filter_parts.append(f"[{input_count}:a]volume=0.6[a_ost_{input_count}];")
                mix_inputs.append(f"[a_ost_{input_count}]")
                input_count += 1

        if not mix_inputs:
            input_args = ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
            filter_chain = f"highpass=f={low_cut},extrastereo=m={widen},loudnorm=I={lufs}:TP={peak}:LRA=11"
            full_cmd = ["ffmpeg", "-y"] + input_args + ["-af", filter_chain, output_path]
            return {"command_list": full_cmd, "filter_complex_string": filter_chain}

        mix_count = len(mix_inputs)
        mix_concat = "".join(mix_inputs)
        filter_parts.append(f"{mix_concat}amix=inputs={mix_count}:duration=longest:dropout_transition=2[a_mix];")

        master_chain = (
            f"[a_mix]highpass=f={low_cut},"
            f"extrastereo=m={widen},"
            f"acompressor=threshold={c_thresh}dB:ratio={c_ratio}:makeup={c_makeup}dB:attack=10:release=100,"
            f"loudnorm=I={lufs}:TP={peak}:LRA=11[a_master]"
        )
        filter_parts.append(master_chain)

        filter_complex_str = "".join(filter_parts)

        full_cmd = ["ffmpeg", "-y"] + input_args + ["-filter_complex", filter_complex_str, "-map", "[a_master]", "-b:a", "320k", output_path]

        return {
            "command_list": full_cmd,
            "filter_complex_string": filter_complex_str
        }

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")

        if target_agent and "19" not in target_agent and target_agent != self.agent_name:
            print(f"[{self.agent_name}] Execution skipped. Queue targeted to: {target_agent}", flush=True)
            return state

        workspace_dir = state.get("workspace_dir", "")
        if not workspace_dir:
            workspace_dir = state.get("state_file_path", "")
            if workspace_dir:
                workspace_dir = os.path.dirname(workspace_dir)
            else:
                raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: workspace_dir missing.")

        master_export_dir = os.path.join(workspace_dir, "exports", "master_audio")
        os.makedirs(master_export_dir, exist_ok=True)

        for filename in os.listdir(master_export_dir):
            file_path = os.path.join(master_export_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"[{self.agent_name}] Idempotency sweep executed. Legacy master audio purged.", flush=True)

        runtime_data = state.setdefault("runtime_data", {})
        module_audio = runtime_data.setdefault("module_b_audio", {})

        audio_manifest = {
            "dialogue_tracks": module_audio.get("agent_10_audio_files", []),
            "beat_events": module_audio.get("agent_14_beat_map", {}).get("beat_sync_events", []),
            "sfx_tracks": module_audio.get("agent_17_synthesized_sfx", []),
            "ost_tracks": module_audio.get("agent_18b_custom_ost_tracks", [])
        }

        global_config = state.get("global_config", {})
        medium = global_config.get("medium", "Dynamic")
        rendering = global_config.get("rendering_engine", "Dynamic")
        color = global_config.get("color_lighting", "Dynamic")
        kinetic = global_config.get("kinetic_framing", "Dynamic")

        print(f"[{self.agent_name}] AI Audio Mastering Engineer designing 4K Master Console parameters...", flush=True)

        prompt = (
            f"You are the OmniMatrix Supreme Audio Mastering Engineer.\n"
            f"Design professional audio console parameters based on the 4-Axis Visual DNA and active audio manifest.\n\n"
            f"4-Axis Visual DNA Context:\n"
            f"- Medium: '{medium}'\n"
            f"- Rendering: '{rendering}'\n"
            f"- Color: '{color}'\n"
            f"- Kinetic Framing: '{kinetic}'\n\n"
            f"Active Audio Manifest Summary:\n"
            f"- Dialogues: {len(audio_manifest['dialogue_tracks'])}\n"
            f"- Beat/Sub-Bass Drops: {len(audio_manifest['beat_events'])}\n"
            f"- SFX Tracks: {len(audio_manifest['sfx_tracks'])}\n"
            f"- OST Music Tracks: {len(audio_manifest['ost_tracks'])}\n\n"
            f"CRITICAL DIRECTIVES:\n"
            f"1. Choose loudness 'target_loudness_lufs' (-9.0 LUFS for Fast Action/Shorts, -14.0 LUFS for YouTube, -23.0 LUFS for Cinema).\n"
            f"2. Set 'master_true_peak_limiter_db' between -0.1 and -2.0 dB.\n"
            f"3. Set 'stereo_widening_factor' between 1.0 and 1.5.\n"
            f"4. Set 'low_cut_filter_hz' between 20 and 50 Hz.\n"
            f"5. Set 'vocal_presence_boost_db' between 0.5 and 4.0 dB.\n"
            f"6. Return ONLY valid JSON matching this schema:\n"
            f"{{\n"
            f"  \"mastering_console_parameters\": {{\n"
            f"    \"target_loudness_lufs\": -10.5,\n"
            f"    \"master_true_peak_limiter_db\": -0.5,\n"
            f"    \"stereo_widening_factor\": 1.25,\n"
            f"    \"low_cut_filter_hz\": 30,\n"
            f"    \"vocal_presence_boost_db\": 2.5,\n"
            f"    \"glue_compressor\": {{\n"
            f"      \"threshold_db\": -5.0,\n"
            f"      \"ratio\": 2.5,\n"
            f"      \"makeup_gain_db\": 1.5\n"
            f"    }},\n"
            f"    \"mastering_notes\": \"High punchiness with clean 3kHz vocal presence for mobile speakers.\"\n"
            f"  }}\n"
            f"}}"
        )

        generated_data = None
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[{self.agent_name}] Prompting Mastering Console AI (Attempt {attempt})...", flush=True)
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
            print(f"[{self.agent_name}] ALL AI CORES FAILED. Engaging Procedural Fallback. Traceback: {last_error}", flush=True)
            generated_data = self._execute_procedural_fallback(kinetic)

        output_master_file = os.path.join(master_export_dir, "final_master_mix.mp3")
        ffmpeg_blueprint = self._build_master_ffmpeg_command(audio_manifest, generated_data, output_master_file)

        render_success = False
        try:
            print(f"[{self.agent_name}] Executing Master FFmpeg Audio Render...", flush=True)
            subprocess.run(ffmpeg_blueprint["command_list"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            render_success = True
            print(f"[{self.agent_name}] MASTER AUDIO MIX SUCCESSFULLY RENDERED: {output_master_file}", flush=True)
        except Exception as e:
            print(f"[{self.agent_name}] FFmpeg Native Render warning: {str(e)}. Filter graph string secured for Module E.", flush=True)

        module_audio["agent_19_final_master_mix"] = {
            "master_file_path": output_master_file if render_success else "PENDING_MODULE_E_COMPOSITING",
            "render_success": render_success,
            "mastering_parameters": generated_data["mastering_console_parameters"],
            "executable_ffmpeg_command": " ".join(ffmpeg_blueprint["command_list"]),
            "ffmpeg_filter_complex": ffmpeg_blueprint["filter_complex_string"]
        }

        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status["Ai_Agent_19"] = "COMPLETED"
        pipeline_status["MODULE_B_AUDIO"] = "COMPLETED_GOD_LEVEL"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Master Audio Console Execution Complete.", flush=True)
        return state
