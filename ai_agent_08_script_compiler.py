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
    def __init__(self):
        # GOD-LEVEL UPGRADE: Fixed Naming Consistency
        self.agent_name = "Ai Agent 08: script_file_formatter"
        
        # GOD-LEVEL UPGRADE 1: Universal Path Isolation
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        
        # Universal Export Directory
        self.export_dir = os.path.join(self.workspace_dir, "exports")
        os.makedirs(self.export_dir, exist_ok=True)
        
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
                model_name='gemini-flash-latest',
                generation_config={"response_mime_type": "application/json"}
            )
            
        # OpenAI/Ollama Setup
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_openai = "gpt-4o-mini"
        self.model_local = "llama3"

    def _log_info(self, message):
        print(f"[{self.agent_name}] [INFO] {message}")

    def _log_error(self, message):
        print(f"[{self.agent_name}] [ERROR] {message}", file=sys.stderr)

    def _read_state(self):
        if not os.path.exists(self.state_file):
            self._log_error("Critical Error: matrix_state.json not found. Run previous agents first.")
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

    def _build_compiler_prompt(self, raw_merged_data, content_format, vibe_tempo, dna_profile):
        """GOD-LEVEL UPGRADE 3: Context-aware script compilation."""
        system_prompt = (
            "You are the OmniMatrix Final Video Continuity Director.\n"
            "Your objective is to compile, review, and align raw timeline data into a Master Playbook.\n"
            f"Universal Architecture: {dna_profile}\n"
            f"Acoustic Signature: {vibe_tempo}\n"
            f"Content Format: {content_format}\n\n"
            "Instructions:\n"
            "1. Analyze the voiceover and aesthetic data for each frame.\n"
            "2. Intelligently assign a 'character_voice' (e.g., 'Cyber-Narrator', 'Casual Host', 'Protagonist') based on the context of the universal architecture.\n"
            "3. Format your output EXACTLY as a raw JSON object with the key 'master_timeline' containing a list of frames.\n"
            "4. Each frame must contain these exact keys:\n"
            "   - 'frame_index': integer\n"
            "   - 'character_voice': string (The detected speaker style)\n"
            "   - 'spoken_audio': string (The final confirmed voiceover text)\n"
            "   - 'vfx_style_prompt': string (The visual description)\n"
            "   - 'camera_shake_intensity': float\n"
            "   - 'bass_drop_sync': boolean\n"
            "   - 'color_palette': list of exactly 3 hex codes\n"
            "Do not wrap the JSON in markdown code blocks."
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
                headers = {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_api_key}"}
                payload = {
                    "model": self.model_openai, 
                    "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], 
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=45) as response:
                    return json.loads(self._clean_json_response(json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]))
            except Exception as e:
                self._log_error(f"OpenAI failed: {str(e)}. Switching to Ollama...")

        self._log_info("Routing to Priority 3: Local Engine (Ollama)")
        try:
            headers = {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")}
            payload = {
                "model": self.model_local, 
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], 
                "stream": False, 
                "format": "json"
            }
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=50) as response:
                return json.loads(self._clean_json_response(json.loads(response.read().decode("utf-8"))["message"]["content"]))
        except Exception as e:
            self._log_error(f"Ollama failed: {str(e)}.")
            return None

    def _procedural_compile(self, raw_data, content_format):
        self._log_info("Executing Universal Procedural Offline Compilation.")
        master_timeline = []
        default_voice = "Dynamic Host" if "commentary" in content_format.lower() else "Omniscient Narrator"
        
        for frame in raw_data:
            master_timeline.append({
                "frame_index": frame.get("frame_index", 1),
                "character_voice": default_voice,
                "spoken_audio": frame.get("spoken_audio", ""),
                "vfx_style_prompt": frame.get("vfx_style_prompt", "Universal Procedural Scene"),
                "camera_shake_intensity": frame.get("camera_shake_intensity", 0.0),
                "bass_drop_sync": frame.get("bass_drop_sync", False),
                "color_palette": frame.get("color_palette", ["#000000", "#FFFFFF", "#888888"])
            })
        return {"master_timeline": master_timeline}

    def _generate_human_readable_txt(self, topic, timeline, content_format):
        txt_path = os.path.join(self.export_dir, "08_master_playbook_preview.txt")
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("=== OMNIMATRIX MASTER VIDEO PLAYBOOK ===\n")
                f.write(f"Topic: {topic}\n")
                f.write(f"Format Architecture: {content_format}\n")
                f.write(f"Total Frames: {len(timeline)}\n")
                f.write("==========================================\n\n")
                
                for frame in timeline:
                    f.write(f"FRAME {frame['frame_index']} | CHARACTER: {frame['character_voice']}\n")
                    f.write(f"AUDIO: \"{frame['spoken_audio']}\"\n")
                    f.write(f"VISUALS: {frame['vfx_style_prompt']}\n")
                    f.write(f"VFX SETTINGS -> Shake: {frame['camera_shake_intensity']} | Bass Drop: {frame['bass_drop_sync']} | Palette: {', '.join(frame['color_palette'])}\n")
                    f.write("-" * 70 + "\n")
            self._log_info(f"Human-readable playbook saved to: {txt_path}")
        except Exception as e:
            self._log_error(f"Failed to generate text playbook: {str(e)}")

    def execute(self):
        state = self._read_state()
        
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent not in ["Ai_Agent_08", "Agent_08"]:
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        # GOD-LEVEL UPGRADE 2: Idempotency Sweep
        if "FINAL_MASTER_PLAYBOOK" in state.get("runtime_data", {}).get("module_a_scripting", {}):
            del state["runtime_data"]["module_a_scripting"]["FINAL_MASTER_PLAYBOOK"]
            self._log_info("Idempotency Sweep: Cleared legacy master playbook from previous session.")

        topic = state.get("runtime_data", {}).get("core_topic", "Unknown Target")
        content_format = state.get("global_config", {}).get("content_format", "Fluid_Narrative")
        vibe_tempo = state.get("global_config", {}).get("vibe_tempo", "Adaptive_Resonance")
        dna_profile = state.get("global_config", {}).get("animation_dna", "Omni_Procedural")
        
        scripting_module = state.get("runtime_data", {}).get("module_a_scripting", {})
        storyboard_frames = scripting_module.get("agent_03_storyboard", {}).get("storyboard_frames", [])
        vibe_data = scripting_module.get("agent_07_vibe_enhancer", {}).get("phonk_frames", [])

        if not storyboard_frames:
            self._log_error("Critical Error: Storyboard data missing. Cannot compile Master Playbook.")
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

        system_prompt, user_prompt = self._build_compiler_prompt(raw_merged, content_format, vibe_tempo, dna_profile)
        
        compiled_data = None
        for attempt in range(1, self.max_retries + 1):
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            if parsed_json and "master_timeline" in parsed_json:
                compiled_data = parsed_json
                self._log_info(f"Success! Master Timeline aligned with {len(compiled_data['master_timeline'])} universal frames.")
                break
            else:
                self._log_error("Alignment schema error. Retrying...")
                time.sleep(self.retry_delay)

        if not compiled_data:
            self._log_error("AI Alignment failed. Triggering Universal Procedural Compile.")
            compiled_data = self._procedural_compile(raw_merged, content_format)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_08_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_08"

        # Export human-readable TXT file for the user
        self._generate_human_readable_txt(topic, compiled_data["master_timeline"], content_format)

        state["runtime_data"]["module_a_scripting"]["FINAL_MASTER_PLAYBOOK"] = compiled_data
        
        # CRITICAL PIPELINE JUMP: MODULE A TO MODULE B
        state["pipeline_status"]["current_module"] = "Module_B_Audio"
        state["pipeline_status"]["next_agent"] = "Ai_Agent_09"
        
        self._write_state(state)
        
        self._log_info("MODULE A COMPLETED! Scripting sealed globally. Handoff to Module B (Ai_Agent_09).")
        return True

if __name__ == "__main__":
    compiler = UniversalScriptCompiler()
    compiler.execute()
