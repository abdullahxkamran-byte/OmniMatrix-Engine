import os
import re
import sys
import json
import time
import urllib.request
import urllib.error
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class UniversalScriptCompiler:
    def __init__(self, state_file_path="matrix_state.json", export_dir="znet_exports"):
        self.agent_name = "Agent 08: script_file_formatter"
        self.state_file = state_file_path
        self.export_dir = export_dir
        
        # Network Resilience
        self.max_retries = 3
        self.retry_delay = 3
        
        # API Keys Initialization
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Setup Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                generation_config={"response_mime_type": "application/json"}
            )
            
        # OpenAI/Ollama Setup
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_openai = "gpt-4o-mini"
        self.model_local = "llama3"

        # Ensure export directory exists for human-readable outputs
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def _log_info(self, message):
        print(f"[{self.agent_name}] INFO: {message}")

    def _log_error(self, message):
        print(f"[{self.agent_name}] ERROR: {message}", file=sys.stderr)

    def _read_state(self):
        if not os.path.exists(self.state_file):
            self._log_error("Critical Error: matrix_state.json not found.")
            sys.exit(1)
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self._log_error(f"Failed to read state file: {str(e)}")
            sys.exit(1)

    def _write_state(self, state_data):
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=4)
        except Exception as e:
            self._log_error(f"Failed to persist state: {str(e)}")

    def _clean_json_response(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
        return cleaned

    def _build_compiler_prompt(self, raw_merged_data):
        system_prompt = (
            "You are the Final Video Continuity Director. Your job is to compile, review, and align raw timeline data into a Master Playbook.\n"
            "Analyze the voiceover for each frame and intelligently assign a 'character_voice' (e.g., 'Narrator', 'Protagonist', 'Expert', 'Gojo', 'Villain' etc.) based on the context.\n"
            "Format your output EXACTLY as a JSON object with the key 'master_timeline' containing a list of frames.\n"
            "Each frame must contain these keys:\n"
            "- 'frame_index': integer\n"
            "- 'character_voice': string (The detected speaker)\n"
            "- 'spoken_audio': string (The final confirmed voiceover text)\n"
            "- 'vfx_style_prompt': string (The visual description)\n"
            "- 'camera_shake_intensity': float\n"
            "- 'bass_drop_sync': boolean\n"
            "- 'color_palette': list of 3 hex codes\n"
        )
        user_prompt = f"Raw Unaligned Timeline Data:\n{json.dumps(raw_merged_data, indent=2)}"
        return system_prompt, user_prompt

    def _call_ai_engine(self, system_prompt, user_prompt):
        if self.gemini_api_key:
            self._log_info("Routing to Priority 1: Google Gemini (Fast Compilation)")
            try:
                response = self.gemini_model.generate_content(f"{system_prompt}\n\n{user_prompt}")
                return json.loads(self._clean_json_response(response.text))
            except Exception as e:
                self._log_error(f"Gemini failed: {str(e)}. Switching to OpenAI...")

        if self.openai_api_key:
            self._log_info("Routing to Priority 2: OpenAI (Deep Alignment)")
            try:
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"}
                payload = {"model": self.model_openai, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "response_format": {"type": "json_object"}}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=45) as response:
                    return json.loads(self._clean_json_response(json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]))
            except Exception as e:
                self._log_error(f"OpenAI failed: {str(e)}. Switching to Ollama...")

        self._log_info("Routing to Priority 3: Local Engine (Ollama)")
        try:
            headers = {"Content-Type": "application/json"}
            payload = {"model": self.model_local, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "stream": False, "format": "json"}
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=50) as response:
                return json.loads(self._clean_json_response(json.loads(response.read().decode("utf-8"))["message"]["content"]))
        except Exception as e:
            self._log_error(f"Ollama failed: {str(e)}.")
            return None

    def _procedural_compile(self, raw_data):
        self._log_info("Executing Procedural Offline Compilation.")
        master_timeline = []
        for frame in raw_data:
            master_timeline.append({
                "frame_index": frame.get("frame_index", 1),
                "character_voice": "Narrator",
                "spoken_audio": frame.get("spoken_audio", ""),
                "vfx_style_prompt": frame.get("vfx_style_prompt", "Cinematic Scene"),
                "camera_shake_intensity": frame.get("camera_shake_intensity", 0.0),
                "bass_drop_sync": frame.get("bass_drop_sync", False),
                "color_palette": frame.get("color_palette", ["#000000", "#FFFFFF", "#888888"])
            })
        return {"master_timeline": master_timeline}

    def _generate_human_readable_txt(self, topic, timeline):
        txt_path = os.path.join(self.export_dir, "08_master_playbook_preview.txt")
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("=== Z-NET MASTER VIDEO PLAYBOOK ===\n")
                f.write(f"Topic: {topic}\n")
                f.write(f"Total Frames: {len(timeline)}\n")
                f.write("===================================\n\n")
                
                for frame in timeline:
                    f.write(f"FRAME {frame['frame_index']} | CHARACTER: {frame['character_voice']}\n")
                    f.write(f"AUDIO: \"{frame['spoken_audio']}\"\n")
                    f.write(f"VISUALS: {frame['vfx_style_prompt']}\n")
                    f.write(f"VFX SETTINGS -> Shake: {frame['camera_shake_intensity']} | Bass Drop: {frame['bass_drop_sync']} | Palette: {', '.join(frame['color_palette'])}\n")
                    f.write("-" * 60 + "\n")
            self._log_info(f"Human-readable playbook saved to: {txt_path}")
        except Exception as e:
            self._log_error(f"Failed to generate text playbook: {str(e)}")

    def execute(self):
        state = self._read_state()
        
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Agent_08":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        topic = state.get("runtime_data", {}).get("core_topic", "Unknown")
        
        scripting_module = state.get("runtime_data", {}).get("module_a_scripting", {})
        storyboard_frames = scripting_module.get("agent_03_storyboard", {}).get("storyboard_frames", [])
        vibe_data = scripting_module.get("agent_07_vibe_enhancer", {}).get("phonk_frames", [])

        if not storyboard_frames:
            self._log_error("Critical Error: Storyboard data missing. Cannot compile.")
            return False

        self._log_info(f"Compiling Final Master Playbook for: {topic}")

        raw_merged = []
        vibe_map = {item["frame_index"]: item for item in vibe_data}
        
        for frame in storyboard_frames:
            f_idx = frame.get("frame_index", 1)
            v_meta = vibe_map.get(f_idx, {})
            raw_merged.append({
                "frame_index": f_idx,
                "spoken_audio": frame.get("spoken_audio", ""),
                "vfx_style_prompt": v_meta.get("visual_style_prompt", ""),
                "camera_shake_intensity": v_meta.get("camera_shake_intensity", 0.0),
                "bass_drop_sync": v_meta.get("bass_drop_sync", False),
                "color_palette": v_meta.get("color_palette_hex", [])
            })

        system_prompt, user_prompt = self._build_compiler_prompt(raw_merged)
        
        compiled_data = None
        for attempt in range(1, self.max_retries + 1):
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            if parsed_json and "master_timeline" in parsed_json:
                compiled_data = parsed_json
                self._log_info(f"Success! Master Timeline aligned with {len(compiled_data['master_timeline'])} frames.")
                break
            else:
                self._log_error("Alignment schema error. Retrying...")
                time.sleep(self.retry_delay)

        if not compiled_data:
            self._log_error("AI Alignment failed. Triggering Procedural Compile.")
            compiled_data = self._procedural_compile(raw_merged)
            state["pipeline_status"]["last_active_agent"] = "Agent_08_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Agent_08"

        # Export human-readable TXT file for the user
        self._generate_human_readable_txt(topic, compiled_data["master_timeline"])

        state["runtime_data"]["module_a_scripting"]["FINAL_MASTER_PLAYBOOK"] = compiled_data
        
        # CRITICAL PIPELINE JUMP: MODULE A TO MODULE B
        state["pipeline_status"]["current_module"] = "Module_B_Audio"
        state["pipeline_status"]["next_agent"] = "Ai_Agent_09"
        
        self._write_state(state)
        
        self._log_info("MODULE A COMPLETED! Scripting finalized. Handoff to Module B (Agent 09).")
        return True

if __name__ == "__main__":
    compiler = UniversalScriptCompiler()
    compiler.execute()
