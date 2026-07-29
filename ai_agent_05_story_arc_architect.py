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

class UniversalStoryArcArchitect:
    def __init__(self):
        self.agent_name = "Ai Agent 05: story_arc_structural_architect"
        
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

    def _build_universal_prompt(self, topic, dna_profile, vibe_profile, content_format, tension_data):
        """GOD-LEVEL UPGRADE 3: Dynamically architects arc phases based on universal inputs."""
        
        system_prompt = (
            "You are the OmniMatrix Supreme Narrative Arc Architect.\n"
            "Analyze the provided tension timeline and subject matter to structure a high-density, "
            "multi-stage story arc mapped out chronologically.\n"
            "Analyze the dynamically injected parameters and shape the arc phases strictly to their structural intent.\n\n"
            f"Visual DNA Architecture: {dna_profile}\n"
            f"Audio/Acoustic Signature: {vibe_profile}\n"
            f"Content Format/Style/Pacing: {content_format}\n\n"
            "Instructions:\n"
            "1. Internalize the 'Content Format'. Dynamically generate the appropriate number of phases (e.g., 3 phases for fast viral retention, 4-5 phases for cinematic/documentary pacing). Do not restrict yourself to hardcoded templates.\n"
            "2. Output must STRICTLY be a raw JSON object containing a list named 'arc_phases'.\n"
            "3. Each phase object must contain these exact keys:\n"
            "   - 'phase_index': integer representing execution order (1, 2, 3...)\n"
            "   - 'phase_name': string designating the arc level (e.g., 'The Hook', 'The Deep Dive', 'Terminal Output')\n"
            "   - 'target_duration_ratio': float representing percentage of total runtime (must sum to exactly 1.0 overall. e.g., 0.20 for 20%)\n"
            "   - 'pacing_frequency': string description of edit speed based on the audio signature.\n"
            "   - 'audience_psychology_goal': string representing target viewer mental state.\n"
            "Do not wrap the JSON in markdown code blocks."
        )

        user_context = (
            f"Target Subject: '{topic}'\n"
            f"Tension Map (from Agent 04):\n{json.dumps(tension_data, indent=2)}\n\n"
            f"Generate the universal chronological arc phases."
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

    def _execute_procedural_fallback(self, content_format, vibe_profile):
        """Universal mathematical structural breakdown replacing hardcoded cinematic/viral limits."""
        self._log_info(f"Triggering Universal Procedural Arc Architect Logic for structure: {content_format}.")
        
        phases = [
            {
                "phase_index": 1, 
                "phase_name": "System Initialization (Act I)", 
                "target_duration_ratio": 0.25, 
                "pacing_frequency": f"procedural-hook-{vibe_profile.split('_')[0].lower()}", 
                "audience_psychology_goal": "cognitive-engagement"
            },
            {
                "phase_index": 2, 
                "phase_name": "Core Processing (Act II)", 
                "target_duration_ratio": 0.50, 
                "pacing_frequency": "rhythmic-escalation", 
                "audience_psychology_goal": "sustained-retention"
            },
            {
                "phase_index": 3, 
                "phase_name": "Terminal Output (Act III)", 
                "target_duration_ratio": 0.25, 
                "pacing_frequency": "climactic-resolution", 
                "audience_psychology_goal": "absolute-resonance"
            }
        ]

        return {"arc_phases": phases}

    def execute(self):
        state = self._read_state()
        
        # Pipeline Gate Check
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Ai_Agent_05":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        # GOD-LEVEL UPGRADE 2: Idempotency Sweep
        if "agent_05_story_arc" in state.get("runtime_data", {}).get("module_a_scripting", {}):
            del state["runtime_data"]["module_a_scripting"]["agent_05_story_arc"]
            self._log_info("Idempotency Sweep: Cleared legacy story arc data from previous session.")

        topic = state.get("runtime_data", {}).get("core_topic", "")
        content_format = state.get("global_config", {}).get("content_format", "Fluid_Narrative")
        dna_profile = state.get("global_config", {}).get("animation_dna", "Omni_Procedural")
        vibe_profile = state.get("global_config", {}).get("vibe_tempo", "Adaptive_Resonance")
        
        # Pull Tension Data from Agent 04
        agent_04_data = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_04_tension_peaks", {})
        tension_data = agent_04_data.get("tension_timeline", [])

        if not tension_data:
            self._log_error("Critical Error: Tension data missing from Agent 04.")
            return False

        self._log_info(f"Architecting Story Arc for universal format: {content_format.upper()}")

        system_prompt, user_prompt = self._build_universal_prompt(topic, dna_profile, vibe_profile, content_format, tension_data)
        
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            if parsed_json and "arc_phases" in parsed_json:
                generated_data = parsed_json
                self._log_info(f"Success! Built {len(generated_data['arc_phases'])} Universal Arc Phases.")
                break
            else:
                self._log_error("Invalid response format. Retrying...")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        if not generated_data:
            self._log_error("All models failed. Applying Procedural Arc Fallback.")
            generated_data = self._execute_procedural_fallback(content_format, vibe_profile)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_05_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_05"

        # Save Output to Module A Scripting Memory
        state["runtime_data"]["module_a_scripting"]["agent_05_story_arc"] = generated_data
        
        # STRICT HANDSHAKE PROTOCOL: Hand over to Ai_Agent_06 (Fixed Naming Consistency)
        state["pipeline_status"]["next_agent"] = "Ai_Agent_06"
        self._write_state(state)
        
        self._log_info("Arc Structure Locked! Pipeline handed over to Ai_Agent_06: word_count_guard_utility.")
        return True

if __name__ == "__main__":
    architect = UniversalStoryArcArchitect()
    architect.execute()
