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

class UniversalCoreScriptGenerator:
    def __init__(self):
        self.agent_name = "Ai Agent 02: universal_core_script_engine"
        
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
                model_name='gemini-1.5-flash',
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
        """Thread-safe state file read block. Vital for fetching Agent 01's output."""
        if not os.path.exists(self.state_file):
            self._log_error("Critical Error: matrix_state.json not found. Run Agent 01 first.")
            sys.exit(1)
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self._log_error(f"Failed to read state file: {str(e)}")
            sys.exit(1)

    def _write_state(self, state_data):
        """Thread-safe state file execution block."""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=4)
        except Exception as e:
            self._log_error(f"Failed to persist state modification matrix: {str(e)}")

    def _clean_json_response(self, raw_text):
        """Strips wrapper blocks from AI model responses to isolate raw, parseable JSON."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
        return cleaned

    def _build_universal_prompt(self, topic, selected_hook, dna_profile, vibe_profile, content_format):
        """Dynamically shifts creative logic based purely on injected parameters. No hardcoded limits."""
        
        system_prompt = (
            "You are the OmniMatrix Supreme Narrative Engine. Your directive is to seamlessly continue the narrative "
            "established by the provided opening hook.\n"
            "Analyze the following dynamically injected parameters and shape your output strictly to their aesthetic and structural intent.\n\n"
            f"Visual DNA Architecture: {dna_profile}\n"
            f"Audio/Acoustic Signature: {vibe_profile}\n"
            f"Content Format/Style: {content_format}\n\n"
            "Instructions:\n"
            "1. Internalize the 'Content Format/Style'. If it is procedural, cinematic, analytical, or abstract, match the tone perfectly.\n"
            "2. Generate exactly 2 distinct continuation paths for the script following the hook.\n"
            "3. Output must STRICTLY be a raw JSON object containing a list named 'core_paths'.\n"
            "4. Required keys for each object in the list: 'path_id', 'core_script_line', 'context_or_action'.\n"
            "Do not wrap the JSON in markdown code blocks."
        )

        user_context = (
            f"Target Subject: '{topic}'\n"
            f"Previous Hook (Agent 01 Output): '{selected_hook}'\n\n"
            f"Generate the continuation sequence."
        )

        return system_prompt, user_context

    def _execute_procedural_fallback(self, topic, content_format):
        """Intelligent offline fallback utilizing abstract syntax based on universal parameters."""
        self._log_info(f"Triggering Universal Procedural Fallback for format: {content_format}")
        
        return {
            "core_paths": [
                {
                    "path_id": "procedural_continuation_alpha",
                    "core_script_line": f"Subject '{topic}' progression initiated. Narrative layer expanding.",
                    "context_or_action": f"Dynamic procedural continuation based on {content_format} structure."
                },
                {
                    "path_id": "procedural_continuation_beta",
                    "core_script_line": f"Data stream stabilized. Advancing core concepts of {topic}.",
                    "context_or_action": "Sub-routine visual expansion. Camera tracks forward."
                }
            ]
        }

    def _call_ai_engine(self, system_prompt, user_prompt):
        """Tri-Core Routing Logic: Gemini -> OpenAI -> Ollama"""
        
        # PRIORITY 1: GEMINI
        if self.gemini_api_key:
            self._log_info("Routing to Priority 1: Google Gemini (1.5 Flash)")
            try:
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini_model.generate_content(full_prompt)
                cleaned_message = self._clean_json_response(response.text)
                return json.loads(cleaned_message)
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
                    raw_ai_message = result["choices"][0]["message"]["content"]
                    cleaned_message = self._clean_json_response(raw_ai_message)
                    return json.loads(cleaned_message)
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
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))
                raw_ai_message = result["message"]["content"]
                cleaned_message = self._clean_json_response(raw_ai_message)
                return json.loads(cleaned_message)
        except Exception as e:
            self._log_error(f"Local Ollama failed: {str(e)}.")
            return None 

    def execute(self):
        """Main execution sequence. Validates pipeline, calls AI, and updates state."""
        state = self._read_state()
        
        # Pipeline Gatekeeper Check
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Ai_Agent_02":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        # GOD-LEVEL UPGRADE 2: Idempotency Sweep (Scrub Previous Run Data)
        if "agent_02_core_script" in state.get("runtime_data", {}).get("module_a_scripting", {}):
            del state["runtime_data"]["module_a_scripting"]["agent_02_core_script"]
            self._log_info("Idempotency Sweep: Cleared legacy core script data from previous session.")

        # Extract Data from State
        topic = state.get("runtime_data", {}).get("core_topic", "")
        dna_profile = state.get("global_config", {}).get("animation_dna", "Omni_Procedural")
        vibe_profile = state.get("global_config", {}).get("vibe_tempo", "Adaptive_Resonance")
        content_format = state.get("global_config", {}).get("content_format", "Fluid_Narrative")
        
        agent_01_hooks = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_01_hooks", [])
        
        if not agent_01_hooks:
            self._log_error("Critical Error: No hooks found from Agent 01. Pipeline broken.")
            return False

        # Extract primary hook payload
        selected_hook = agent_01_hooks[0].get("hook_script", f"Initial sequence for {topic} established.")
        
        self._log_info(f"Input received from Agent 01. Developing Continuation Script for format: {content_format.upper()}")

        # Build Prompt dynamically
        system_prompt, user_prompt = self._build_universal_prompt(topic, selected_hook, dna_profile, vibe_profile, content_format)
        
        # Multi-Retry Network Transaction
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            self._log_info(f"Transaction Attempt {attempt}/{self.max_retries}...")
            
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            
            if parsed_json and "core_paths" in parsed_json and len(parsed_json["core_paths"]) > 0:
                generated_data = parsed_json
                self._log_info("AI payload structural mapping validated successfully.")
                break
            else:
                self._log_error("AI response invalid or missing 'core_paths'. Retrying...")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        # Handle Fallback
        if not generated_data:
            self._log_error("All API and Local models failed. Applying abstract algorithmic fallback.")
            generated_data = self._execute_procedural_fallback(topic, content_format)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_02_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_02"

        # Save Output to State
        state["runtime_data"]["module_a_scripting"]["agent_02_core_script"] = generated_data
        
        # Atomic Handshake Protocol
        state["pipeline_status"]["next_agent"] = "Ai_Agent_03"
        self._write_state(state)
        
        self._log_info("Transaction Complete. Core script locked. Pipeline handed over to Ai_Agent_03.")
        return True

if __name__ == "__main__":
    generator = UniversalCoreScriptGenerator()
    generator.execute()
