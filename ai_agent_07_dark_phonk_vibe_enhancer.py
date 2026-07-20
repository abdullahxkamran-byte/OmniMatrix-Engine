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

class UniversalVibeEnhancer:
    def __init__(self, state_file_path="matrix_state.json"):
        # Master List Compliance
        self.agent_name = "Ai Agent 07: dark_phonk_vibe_enhancer"
        self.state_file = state_file_path
        
        # Network Resilience Settings
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

    def _build_universal_prompt(self, topic, content_format, frames):
        """Builds a flexible prompt that adapts the 'Vibe' based on the video format."""
        
        base_system = (
            "You are a Master Cinematic Editor and Vibe Director. Your job is to read storyboard frames "
            "and output synchronized visual aesthetic parameters for each frame.\n"
            "Output must STRICTLY be a raw JSON object containing a list named 'phonk_frames' with these parameters for each frame:\n"
            "- 'frame_index': matching integer representing the sequence flow.\n"
            "- 'visual_style_prompt': specific visual description (lighting, color grading, shadows).\n"
            "- 'color_palette_hex': a list of exactly three HEX color codes representing the dominant grading theme.\n"
            "- 'camera_shake_intensity': float scaling from 0.0 (calm tripod) to 1.5 (maximum explosive shockwave).\n"
            "- 'bass_drop_sync': boolean (true if this frame represents a visual slam, impact, or key transition).\n"
            "- 'ambient_glitch_rate': float from 0.0 to 1.0 mapping screen distortions or VHS effects.\n"
        )

        user_context = f"Topic: '{topic}'\nInput Frames Data:\n" + json.dumps(frames, indent=2)

        # Dynamic Flexibility: Adjust Vibe based on Format
        if content_format == "cinematic_movie":
            mode_rules = (
                "VIBE MODE: DARK PHONK / ANIME SAKUGA\n"
                "Inject extreme contrasts, deep shadows, and toxic neon accents (purple, blood red, emerald green). "
                "Camera shakes should peak at 1.5 during action beats. Glitch rate should be high during tension peaks."
            )
        elif content_format == "casual_commentary":
            mode_rules = (
                "VIBE MODE: CLEAN CASUAL CREATOR\n"
                "Keep lighting soft, bright, and natural. Color palette should be inviting (warm oranges, clean blues). "
                "Camera shake must remain 0.0 unless there is a sudden comedic reaction (max 0.4). No glitch effects."
            )
        else:
            mode_rules = (
                "VIBE MODE: VIRAL EXPLAINER\n"
                "Use high-saturation, high-contrast, attention-grabbing colors (neon yellow, electric blue, stark white). "
                "Keep camera motion kinetic but smooth (0.1 - 0.3). Use 'bass_drop_sync' strictly on key truth reveals."
            )

        return base_system + "\n\n" + mode_rules, user_context

    def _call_ai_engine(self, system_prompt, user_prompt):
        # Tri-Core Routing
        if self.gemini_api_key:
            self._log_info("Routing to Priority 1: Google Gemini")
            try:
                response = self.gemini_model.generate_content(f"{system_prompt}\n\n{user_prompt}")
                return json.loads(self._clean_json_response(response.text))
            except Exception as e:
                self._log_error(f"Gemini failed: {str(e)}. Switching to OpenAI...")

        if self.openai_api_key:
            self._log_info("Routing to Priority 2: OpenAI")
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

    def _execute_procedural_fallback(self, content_format, frames):
        """Mathematical fallback if APIs go offline."""
        self._log_info("Executing Procedural Fallback Engine.")
        
        phonk_frames = []
        for idx, frame in enumerate(frames):
            frame_idx = frame.get("frame_index", idx + 1)
            
            if content_format == "casual_commentary":
                prompt, palette, shake, bass, glitch = "Soft studio lighting", ["#ffffff", "#e6e6e6", "#cccccc"], 0.0, False, 0.0
            elif content_format == "explainer":
                prompt, palette, shake, bass, glitch = "Bright, high contrast neon glow", ["#ffea00", "#00d4ff", "#ffffff"], 0.1, (idx % 3 == 0), 0.05
            else:
                # Phonk / Cinematic Default
                prompt, palette, shake, bass, glitch = "Deep shadows, extreme contrast, toxic purple glow", ["#7f00ff", "#0d0d0d", "#ff003c"], 0.8 if idx % 2 == 0 else 0.2, (idx % 2 == 0), 0.3

            phonk_frames.append({
                "frame_index": frame_idx,
                "visual_style_prompt": prompt,
                "color_palette_hex": palette,
                "camera_shake_intensity": shake,
                "bass_drop_sync": bass,
                "ambient_glitch_rate": glitch
            })

        return {"phonk_frames": phonk_frames}

    def execute(self):
        state = self._read_state()
        
        # Pipeline Check
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Ai_Agent_07":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        topic = state.get("runtime_data", {}).get("core_topic", "Unknown")
        content_format = state.get("global_config", {}).get("content_format", "cinematic_movie")
        
        # Pull audited frames safely
        frames = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_03_storyboard", {}).get("storyboard_frames", [])

        if not frames:
            self._log_error("Critical Error: No frames found to apply vibe aesthetics.")
            return False

        self._log_info(f"Applying Vibe Aesthetics. Mode: {content_format.upper()}")

        system_prompt, user_prompt = self._build_universal_prompt(topic, content_format, frames)
        
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            if parsed_json and "phonk_frames" in parsed_json:
                generated_data = parsed_json
                self._log_info(f"Success! Vibe applied to {len(generated_data['phonk_frames'])} frames.")
                break
            else:
                self._log_error("Invalid format. Retrying...")
                time.sleep(self.retry_delay)

        if not generated_data:
            self._log_error("All AI nodes failed. Applying Math Fallback.")
            generated_data = self._execute_procedural_fallback(content_format, frames)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_07_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_07"

        # Update State
        state["runtime_data"]["module_a_scripting"]["agent_07_vibe_enhancer"] = generated_data
        
        # HANDSHAKE TO LAST AGENT IN MODULE A
        state["pipeline_status"]["next_agent"] = "Agent_08"
        self._write_state(state)
        
        self._log_info("Aesthetics Locked! Pipeline handed to Agent 08: script_file_formatter.")
        return True

if __name__ == "__main__":
    enhancer = UniversalVibeEnhancer()
    enhancer.execute()
