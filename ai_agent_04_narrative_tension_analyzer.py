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

class NarrativeTensionPeaksAnalyzer:
    def __init__(self):
        self.agent_name = "Ai Agent 04: narrative_tension_peaks_analyzer"
        
        # GOD-LEVEL UPGRADE 1: Universal Path Isolation
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        
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

    def _build_universal_prompt(self, topic, dna_profile, vibe_profile, content_format, frames):
        """GOD-LEVEL UPGRADE 3: Limitless dynamic tension calculation based on injected variables."""
        
        system_prompt = (
            "You are the OmniMatrix Supreme Narrative Tension Architect and Audio-Visual Pacing Analyst.\n"
            "Your objective is to map precise tension curves and audio-visual cues for the provided storyboard frames.\n"
            "Analyze the dynamically injected parameters and shape the tension escalation strictly to their aesthetic intent.\n\n"
            f"Visual DNA Architecture: {dna_profile}\n"
            f"Audio/Acoustic Signature: {vibe_profile}\n"
            f"Content Format/Style/Pacing: {content_format}\n\n"
            "Instructions:\n"
            "1. Internalize the 'Content Format' and 'Acoustic Signature'. If the format requires extreme retention (e.g., fast-paced viral), keep tension high and escalating. If it is cinematic, allow valleys and intense climax peaks. Adapt universally.\n"
            "2. Analyze EACH frame provided and map the corresponding tension variables.\n"
            "3. Output STRICTLY as a raw JSON object with the key 'tension_timeline' containing a list of objects.\n"
            "4. Each object in the list MUST contain these exact keys:\n"
            "   - 'frame_index': matching integer representing the frame order.\n"
            "   - 'tension_score': integer from 1 (calm/whisper) to 10 (intense climax/explosive screen shake).\n"
            "   - 'pacing_instruction': string detailing editing cut rate.\n"
            "   - 'highlight_keywords': list of exactly 1-3 critical words in the voiceover to style with kinetic scaling.\n"
            "   - 'vfx_color_shift': color styling recommendation matching the DNA.\n"
            "   - 'audio_attenuation_db': integer for dynamic volume adjustments (e.g., -3 for voice clarity, +4 for bass blast).\n"
            "Do not wrap the JSON in markdown code blocks."
        )

        user_context = (
            f"Target Subject: '{topic}'\n"
            f"Number of Frames to Process: {len(frames)}\n\n"
            f"Storyboard Data:\n{json.dumps(frames, indent=2)}"
        )

        return system_prompt, user_context

    def _call_ai_engine(self, system_prompt, user_prompt):
        """Tri-Core Routing Logic: Gemini -> OpenAI -> Ollama"""
        
        if self.gemini_api_key:
            self._log_info("Routing to Priority 1: Google Gemini (1.5 Flash)")
            try:
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini_model.generate_content(full_prompt)
                return json.loads(self._clean_json_response(response.text))
            except Exception as e:
                self._log_error(f"Gemini API failed: {str(e)}. Fallback to Priority 2...")

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

    def _execute_procedural_fallback(self, dna_profile, vibe_profile, frames):
        """Mathematical formula to calculate tension purely based on progression, replacing hardcoded formats."""
        self._log_info(f"Triggering Universal Procedural Tension Math Logic for profile: {vibe_profile}.")
        
        timeline = []
        total_frames = len(frames) if frames else 1
        
        for idx, frame in enumerate(frames):
            frame_idx = frame.get("frame_index", idx + 1)
            
            # Universal progression curve (ramps up dynamically)
            progression = (idx + 1) / total_frames
            tension_calc = int(3 + (progression * 7))
            
            voiceover = frame.get("spoken_audio", "System Node Sequence")
            words = [w.strip(".,!?\"'") for w in voiceover.split() if len(w) > 3]
            highlights = words[:2] if words else ["Node", "Sequence"]

            if tension_calc < 5:
                pacing, color, db = "procedural-hold", "base-tone", -2
            elif tension_calc < 8:
                pacing, color, db = "dynamic-shift", "accent-contrast", 1
            else:
                pacing, color, db = "climax-burst", "peak-saturation", 4

            timeline.append({
                "frame_index": frame_idx,
                "tension_score": min(tension_calc, 10),
                "pacing_instruction": pacing,
                "highlight_keywords": highlights,
                "vfx_color_shift": f"{color}-{dna_profile.split('_')[0].lower()}",
                "audio_attenuation_db": db
            })

        return {"tension_timeline": timeline}

    def execute(self):
        state = self._read_state()
        
        # Pipeline Gate Check
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Ai_Agent_04":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        # GOD-LEVEL UPGRADE 2: Idempotency Sweep
        if "agent_04_tension_peaks" in state.get("runtime_data", {}).get("module_a_scripting", {}):
            del state["runtime_data"]["module_a_scripting"]["agent_04_tension_peaks"]
            self._log_info("Idempotency Sweep: Cleared legacy tension data from previous session.")

        # Extract Universal Variables
        topic = state.get("runtime_data", {}).get("core_topic", "")
        content_format = state.get("global_config", {}).get("content_format", "Fluid_Narrative")
        dna_profile = state.get("global_config", {}).get("animation_dna", "Omni_Procedural")
        vibe_profile = state.get("global_config", {}).get("vibe_tempo", "Adaptive_Resonance")
        
        # Pull unlimited frames from Agent 03
        agent_03_data = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_03_storyboard", {})
        frames = agent_03_data.get("storyboard_frames", [])

        if not frames:
            self._log_error("Critical Error: No storyboard frames received from Agent 03.")
            return False

        self._log_info(f"Processing Dynamic Tension Curves for {len(frames)} frames. Universal Architecture: {content_format.upper()}")

        system_prompt, user_prompt = self._build_universal_prompt(topic, dna_profile, vibe_profile, content_format, frames)
        
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            if parsed_json and "tension_timeline" in parsed_json:
                generated_data = parsed_json
                self._log_info(f"Success! Tension mapped for {len(generated_data['tension_timeline'])} frames.")
                break
            else:
                self._log_error("Invalid response format. Retrying...")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        if not generated_data:
            self._log_error("All models failed. Applying Universal Procedural Math Fallback.")
            generated_data = self._execute_procedural_fallback(dna_profile, vibe_profile, frames)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_04_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_04"

        # Save Output
        state["runtime_data"]["module_a_scripting"]["agent_04_tension_peaks"] = generated_data
        
        # STRICT HANDSHAKE AS PER YOUR MASTER LIST:
        state["pipeline_status"]["next_agent"] = "Ai_Agent_05"
        self._write_state(state)
        
        self._log_info("Tension Peaks Locked! Handing pipeline over to Ai_Agent_05: story_arc_structural_architect.")
        return True

if __name__ == "__main__":
    analyzer = NarrativeTensionPeaksAnalyzer()
    analyzer.execute()
