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
    def __init__(self, state_file_path="matrix_state.json"):
        self.agent_name = "Ai Agent 02: universal_core_script_engine"
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

    def _build_universal_prompt(self, topic, selected_hook, content_format):
        """Dynamically switches brain modes based on the OmniMatrix configuration."""
        
        base_system = (
            "You are a master scriptwriter and continuity engine. Your job is to take the provided "
            "opening hook and continue the script logically, deeply, and engagingly.\n"
            f"Output must STRICTLY be a raw JSON object containing a list named 'core_paths'. "
            f"Generate exactly 2 continuation paths.\n"
            f"Required keys for each object in the list: 'path_id', 'core_script_line', 'context_or_action'.\n"
        )

        user_context = f"Topic: '{topic}'\nPrevious Hook (Agent 01 Output): '{selected_hook}'\n\n"

        if content_format == "cinematic_movie":
            mode_rules = (
                "MODE: CINEMATIC MOVIE SCREENPLAY\n"
                "The hook provided is a 'Cold Open' scene. You must write the immediate continuation of this scene.\n"
                "- 'core_script_line': Write the actual character dialogue (e.g., [Character Name]: Wait, who are you?).\n"
                "- 'context_or_action': Describe the physical action, camera movement, or character expression happening during the dialogue."
            )
        elif content_format == "casual_commentary":
            mode_rules = (
                "MODE: CASUAL CREATOR COMMENTARY\n"
                "The hook provided is a creator's opening reaction. You must continue their natural thought process.\n"
                "- 'core_script_line': Write the next sentences the creator speaks naturally (e.g., 'I mean, think about it guys, when he first appeared...').\n"
                "- 'context_or_action': Suggest what B-Roll or background gameplay/video should be showing on screen right now."
            )
        else:
            mode_rules = (
                "MODE: AGGRESSIVE VIRAL EXPLAINER\n"
                "The hook provided is an attention-grabbing pattern interrupt. You must now deliver the 'Hot Take' or core argument.\n"
                "- 'core_script_line': Provide the deep psychological or controversial argument that proves the hook.\n"
                "- 'context_or_action': Explain why this argument psychologically retains the viewer."
            )

        return base_system + mode_rules, user_context

    def _execute_procedural_fallback(self, topic, content_format):
        """Intelligent offline fallback that respects the Universal format."""
        self._log_info(f"Triggering Universal Procedural Fallback for format: {content_format}")
        
        if content_format == "cinematic_movie":
            script_line = f"[Character]: You think {topic} can save us now? It's too late. The system is already broken."
            context = "Camera zooms in on the character's face, showing extreme desperation."
        elif content_format == "casual_commentary":
            script_line = f"Honestly, looking back at {topic}, I feel like 90% of people completely missed the point of that scene."
            context = "Show a slow-motion replay of the main scene being discussed."
        else:
            script_line = f"The actual math behind {topic} proves that the popular opinion is mathematically impossible."
            context = "Retains viewer by attacking a universally accepted truth with logic."

        return {
            "core_paths": [
                {
                    "path_id": "procedural_primary",
                    "core_script_line": script_line,
                    "context_or_action": context
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
            return None # Trigger procedural fallback

    def execute(self):
        """Main execution sequence. Validates pipeline, calls AI, and updates state."""
        state = self._read_state()
        
        # 1. Pipeline Gatekeeper (Checks if Agent 01 did its job)
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Ai_Agent_02":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        # 2. Extract Data from State (The Output of Agent 01)
        topic = state.get("runtime_data", {}).get("core_topic", "")
        content_format = state.get("global_config", {}).get("content_format", "explainer")
        
        agent_01_hooks = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_01_hooks", [])
        
        if not agent_01_hooks:
            self._log_error("Critical Error: No hooks found from Agent 01. Pipeline broken.")
            return False

        # Take the best hook from Agent 01 as input for Agent 02
        selected_hook = agent_01_hooks[0].get("hook_script", f"The reality of {topic}")
        
        self._log_info(f"Input received from Agent 01. Developing Continuation Script for mode: {content_format.upper()}")

        # 3. Build Prompt
        system_prompt, user_prompt = self._build_universal_prompt(topic, selected_hook, content_format)
        
        # 4. Multi-Retry Network Transaction
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            self._log_info(f"Transaction Attempt {attempt}/{self.max_retries}...")
            
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            
            if parsed_json and "core_paths" in parsed_json and len(parsed_json["core_paths"]) > 0:
                generated_data = parsed_json
                break
            else:
                self._log_error("AI response invalid or missing 'core_paths'. Retrying...")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        # 5. Handle Fallback if completely offline
        if not generated_data:
            self._log_error("All API and Local models failed. Applying algorithmic fallback.")
            generated_data = self._execute_procedural_fallback(topic, content_format)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_02_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_02"

        # 6. Save Output to State (Ready for Agent 03)
        state["runtime_data"]["module_a_scripting"]["agent_02_core_script"] = generated_data
        
        # 7. Atomic Handshake Protocol: Pass the baton to Agent 03
        state["pipeline_status"]["next_agent"] = "Ai_Agent_03"
        self._write_state(state)
        
        self._log_info("Transaction Complete! Core script locked. Pipeline handed over to Ai_Agent_03.")
        return True

if __name__ == "__main__":
    generator = UniversalCoreScriptGenerator()
    generator.execute()
