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

class VisualSyncStoryboarder:
    def __init__(self, state_file_path="matrix_state.json"):
        self.agent_name = "Ai Agent 03: visual_sync_storyboarder"
        self.state_file = state_file_path
        
        # Network Resilience Settings
        self.max_retries = 3
        self.retry_delay = 3
        
        # Initialize API Keys from .env
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Configure Gemini if key exists
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                generation_config={"response_mime_type": "application/json"}
            )
            
        # Cloud/Local AI Routing Details for OpenAI/Ollama
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_openai = "gpt-4o-mini"
        self.model_local = "llama3"

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

    def _build_universal_prompt(self, topic, hook_script, core_script, content_format, visual_dna):
        """Builds a dynamic prompt with UNLIMITED frames based on content length."""
        
        base_system = (
            "You are a master cinematic director, visual designer, and editor. "
            "Your task is to take the provided script and break it down organically into a dynamic "
            "sequence of storyboard frames.\n"
            "DO NOT limit yourself to a specific number of frames. Generate as many frames as highly recommended "
            "to fully and cinematically cover the pacing of the script.\n"
            f"Output must STRICTLY be a raw JSON object containing a list named 'storyboard_frames'.\n"
            "Each frame object must contain these exact keys:\n"
            "- 'frame_index': integer (starting from 1)\n"
            "- 'timestamp_start': float (start time in seconds)\n"
            "- 'timestamp_end': float (end time in seconds)\n"
            "- 'spoken_audio': The exact dialogue or voiceover spoken during this frame.\n"
            "- 'scenic_art_prompt': Ultra-detailed visual description (subject, lighting, background, vibe).\n"
            "- 'camera_movement_mode': Kinetic direction (e.g., fast pan, orbital tilt, handheld shake).\n"
            "- 'audio_sync_trigger': Audio environment/SFX (e.g., bass slam, sword clash, cinematic riser).\n"
        )

        user_context = (
            f"Topic: '{topic}'\n"
            f"Visual DNA (Art Style): '{visual_dna}'\n"
            f"Opening Hook (From Agent 01): '{hook_script}'\n"
            f"Core Script/Continuation (From Agent 02): '{core_script}'\n\n"
        )

        if content_format == "cinematic_movie":
            mode_rules = (
                "MODE: CINEMATIC MOVIE EPISODE\n"
                "Pacing should feel like a high-budget anime or film. Break frames on major action beats and dialogue shifts.\n"
            )
        elif content_format == "casual_commentary":
            mode_rules = (
                "MODE: CASUAL CREATOR COMMENTARY\n"
                "Pacing matches a reaction video. Break frames when cutting between facecam and gameplay/b-roll.\n"
            )
        else:
            mode_rules = (
                "MODE: AGGRESSIVE VIRAL EXPLAINER\n"
                "Pacing must be hyper-fast (Shorts/TikTok style). Change frames rapidly every 1-2 seconds to retain attention.\n"
            )

        return base_system + mode_rules, user_context

    def _execute_procedural_fallback(self, hook_script, core_script, content_format, visual_dna):
        """Dynamic fallback that calculates frames based on the number of sentences."""
        self._log_info("Triggering Dynamic Procedural Fallback.")
        
        full_text = f"{hook_script} {core_script}"
        # Split text into sentences dynamically
        sentences = [s.strip() for s in re.split(r'[.!?]', full_text) if s.strip()]
        if not sentences:
            sentences = ["System fallback generated.", "Offline mode active."]

        frames = []
        current_time = 0.0
        time_per_frame = 2.5 if content_format == "explainer" else 3.5

        for i, sentence in enumerate(sentences):
            frames.append({
                "frame_index": i + 1,
                "timestamp_start": round(current_time, 1),
                "timestamp_end": round(current_time + time_per_frame, 1),
                "spoken_audio": sentence,
                "scenic_art_prompt": f"Dynamic visual covering: '{sentence}'. Art style: {visual_dna}.",
                "camera_movement_mode": "Slow dynamic push-in." if i % 2 == 0 else "Subtle tracking pan.",
                "audio_sync_trigger": "Ambient atmosphere." if i > 0 else "Impact bass drop."
            })
            current_time += time_per_frame

        return {"storyboard_frames": frames}

    def _call_ai_engine(self, system_prompt, user_prompt):
        # PRIORITY 1: GEMINI
        if self.gemini_api_key:
            self._log_info("Routing to Priority 1: Google Gemini (1.5 Flash)")
            try:
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini_model.generate_content(full_prompt)
                return json.loads(self._clean_json_response(response.text))
            except Exception as e:
                self._log_error(f"Gemini API failed: {str(e)}. Fallback to Priority 2...")

        # PRIORITY 2: OPENAI
        if self.openai_api_key:
            self._log_info("Routing to Priority 2: OpenAI (GPT-4o-mini)")
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.openai_api_key}"
                }
                payload = {
                    "model": self.model_openai,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=45) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    return json.loads(self._clean_json_response(result["choices"][0]["message"]["content"]))
            except Exception as e:
                self._log_error(f"OpenAI API failed: {str(e)}. Fallback to Priority 3...")

        # PRIORITY 3: OLLAMA (LOCAL)
        self._log_info("Routing to Priority 3: Local Engine (Ollama)")
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": self.model_local,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "format": "json"
            }
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=50) as response:
                result = json.loads(response.read().decode("utf-8"))
                return json.loads(self._clean_json_response(result["message"]["content"]))
        except Exception as e:
            self._log_error(f"Local Ollama failed: {str(e)}.")
            return None

    def execute(self):
        state = self._read_state()
        
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Ai_Agent_03":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        topic = state.get("runtime_data", {}).get("core_topic", "")
        content_format = state.get("global_config", {}).get("content_format", "explainer")
        visual_dna = state.get("global_config", {}).get("animation_dna", "Anime")
        
        agent_01_hooks = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_01_hooks", [])
        hook_script = agent_01_hooks[0].get("hook_script", "") if agent_01_hooks else f"The reality of {topic}"
        
        agent_02_script = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_02_core_script", {})
        core_paths = agent_02_script.get("core_paths", [])
        core_script_line = core_paths[0].get("core_script_line", "") if core_paths else f"Let's dive into {topic}"

        self._log_info(f"Generating Dynamic Storyboard for mode: {content_format.upper()}")

        system_prompt, user_prompt = self._build_universal_prompt(topic, hook_script, core_script_line, content_format, visual_dna)
        
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            if parsed_json and "storyboard_frames" in parsed_json:
                generated_data = parsed_json
                self._log_info(f"Success! Generated {len(generated_data['storyboard_frames'])} dynamic frames.")
                break
            else:
                self._log_error("Invalid response format. Retrying...")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        if not generated_data:
            self._log_error("All models failed. Applying Dynamic Sentence-based Fallback.")
            generated_data = self._execute_procedural_fallback(hook_script, core_script_line, content_format, visual_dna)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_03_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_03"

        state["runtime_data"]["module_a_scripting"]["agent_03_storyboard"] = generated_data
        
        # PERFECT HANDSHAKE ACCORDING TO YOUR LIST:
        state["pipeline_status"]["next_agent"] = "Ai_Agent_04"
        self._write_state(state)
        
        self._log_info("Storyboard Blueprint Locked! Handing pipeline over to Ai Agent 04: narrative_tension_peaks_analyzer.")
        return True

if __name__ == "__main__":
    director = VisualSyncStoryboarder()
    director.execute()
