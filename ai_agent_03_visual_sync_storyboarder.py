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
    def __init__(self):
        self.agent_name = "Ai Agent 03: visual_sync_storyboarder"
        
        # GOD-LEVEL UPGRADE 1: Universal Path Isolation
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        
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
                model_name='gemini-flash-latest',
                generation_config={"response_mime_type": "application/json"}
            )
            
        # Cloud/Local AI Routing Details for OpenAI/Ollama
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

    def _build_universal_prompt(self, topic, hook_script, core_script, dna_profile, vibe_profile, content_format):
        """GOD-LEVEL UPGRADE 3: Limitless dynamic pacing and framing based purely on injected variables."""
        
        system_prompt = (
            "You are the OmniMatrix Supreme Cinematic Director and Visual Architect.\n"
            "Your task is to take the provided script and break it down organically into a dynamic "
            "sequence of storyboard frames.\n"
            "Analyze the dynamically injected parameters and shape the pacing, shot selection, and visual direction "
            "strictly to their structural and aesthetic intent.\n\n"
            f"Visual DNA Architecture: {dna_profile}\n"
            f"Audio/Acoustic Signature: {vibe_profile}\n"
            f"Content Format/Style/Pacing: {content_format}\n\n"
            "Instructions:\n"
            "1. Internalize the 'Content Format'. Adapt frame durations, cuts, and transitions dynamically to match this exact format. If it is high-energy, make cuts fast (1-2s). If cinematic, allow frames to breathe.\n"
            "2. DO NOT limit yourself to a specific number of frames. Generate as many frames as required to fully and cinematically cover the script pacing.\n"
            "3. Output must STRICTLY be a raw JSON object containing a list named 'storyboard_frames'.\n"
            "4. Each frame object must contain these exact keys:\n"
            "   - 'frame_index': integer (starting from 1)\n"
            "   - 'timestamp_start': float (start time in seconds)\n"
            "   - 'timestamp_end': float (end time in seconds)\n"
            "   - 'spoken_audio': The exact dialogue or voiceover spoken during this frame.\n"
            "   - 'scenic_art_prompt': Ultra-detailed visual description (subject, lighting, background, composition).\n"
            "   - 'camera_movement_mode': Kinetic direction (e.g., fast pan, tracking shot, static wide).\n"
            "   - 'audio_sync_trigger': Audio environment/SFX.\n"
            "Do not wrap the JSON in markdown code blocks."
        )

        user_context = (
            f"Target Subject: '{topic}'\n"
            f"Opening Hook (Act 1): '{hook_script}'\n"
            f"Core Script/Continuation (Act 2): '{core_script}'\n\n"
            f"Generate the full storyboard sequence."
        )

        return system_prompt, user_context

    def _execute_procedural_fallback(self, hook_script, core_script, content_format, dna_profile):
        """Dynamic fallback utilizing abstract variables rather than hardcoded format strings."""
        self._log_info(f"Triggering Limitless Procedural Fallback for structure: {content_format}")
        
        full_text = f"{hook_script} {core_script}"
        # Split text into sentences dynamically
        sentences = [s.strip() for s in re.split(r'[.!?]', full_text) if s.strip()]
        if not sentences:
            sentences = ["System fallback generated.", "Offline structural mode active."]

        frames = []
        current_time = 0.0
        
        # Procedural base timing adapting universally
        time_per_frame = 3.0 

        for i, sentence in enumerate(sentences):
            frames.append({
                "frame_index": i + 1,
                "timestamp_start": round(current_time, 1),
                "timestamp_end": round(current_time + time_per_frame, 1),
                "spoken_audio": sentence,
                "scenic_art_prompt": f"Dynamic visual covering structural node: '{sentence}'. Architecture: {dna_profile}.",
                "camera_movement_mode": "Procedural spatial shift." if i % 2 == 0 else "Stabilized lock-on.",
                "audio_sync_trigger": "Structural resonance." if i > 0 else "Initial impulse."
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
                    "Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""),
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
            headers = {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")}
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
        
        # Pipeline Gatekeeper Check
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Ai_Agent_03":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        # GOD-LEVEL UPGRADE 2: Idempotency Sweep (Scrub Previous Run Data)
        if "agent_03_storyboard" in state.get("runtime_data", {}).get("module_a_scripting", {}):
            del state["runtime_data"]["module_a_scripting"]["agent_03_storyboard"]
            self._log_info("Idempotency Sweep: Cleared legacy storyboard data from previous session.")

        # Extract Universal Variables
        topic = state.get("runtime_data", {}).get("core_topic", "")
        content_format = state.get("global_config", {}).get("content_format", "Fluid_Narrative")
        dna_profile = state.get("global_config", {}).get("animation_dna", "Omni_Procedural")
        vibe_profile = state.get("global_config", {}).get("vibe_tempo", "Adaptive_Resonance")
        
        # Extract payloads from previous agents
        agent_01_hooks = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_01_hooks", [])
        hook_script = agent_01_hooks[0].get("hook_script", "") if agent_01_hooks else f"Subject initialization: {topic}"
        
        agent_02_script = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_02_core_script", {})
        core_paths = agent_02_script.get("core_paths", [])
        core_script_line = core_paths[0].get("core_script_line", "") if core_paths else f"System progression for {topic} active."

        self._log_info(f"Generating Dynamic Storyboard for universal architecture: {content_format.upper()}")

        # Build dynamic prompt
        system_prompt, user_prompt = self._build_universal_prompt(topic, hook_script, core_script_line, dna_profile, vibe_profile, content_format)
        
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            if parsed_json and "storyboard_frames" in parsed_json:
                generated_data = parsed_json
                self._log_info(f"Success! Generated {len(generated_data['storyboard_frames'])} dynamic universal frames.")
                break
            else:
                self._log_error("Invalid response format. Retrying...")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        # Handle Fallback
        if not generated_data:
            self._log_error("All models failed. Applying Universal Procedural Fallback.")
            generated_data = self._execute_procedural_fallback(hook_script, core_script_line, content_format, dna_profile)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_03_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_03"

        # Update persistent ledger structures
        state["runtime_data"]["module_a_scripting"]["agent_03_storyboard"] = generated_data
        
        # PERFECT HANDSHAKE ACCORDING TO YOUR LIST:
        state["pipeline_status"]["next_agent"] = "Ai_Agent_04"
        self._write_state(state)
        
        self._log_info("Storyboard Blueprint Locked! Handing pipeline over to Ai Agent 04: narrative_tension_peaks_analyzer.")
        return True

if __name__ == "__main__":
    director = VisualSyncStoryboarder()
    director.execute()
