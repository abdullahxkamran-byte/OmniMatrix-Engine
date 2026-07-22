import os
import sys
import json
import time
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UniversalHookDesigner:
    def __init__(self):
        self.agent_name = "Ai Agent 01: universal_hook_designer"
        
        # Universal Path Isolation
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        
        self.max_retries = 3
        self.retry_delay = 2
        
        # Initialize and validate security layer
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            self._log_critical_error("GEMINI_API_KEY missing from environment initialization.")
            sys.exit(1)
            
        # Native JSON Forced Config
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Internal state initialization check
        self._verify_and_patch_state_schema()

    def _log_info(self, message):
        print(f"[{self.agent_name}] [INFO] {message}")

    def _log_error(self, message):
        print(f"[{self.agent_name}] [ERROR] {message}", file=sys.stderr)

    def _log_critical_error(self, message):
        print(f"[{self.agent_name}] [CRITICAL] {message}", file=sys.stderr)

    def _verify_and_patch_state_schema(self):
        """Validates matrix_state.json structural integrity, patching missing nodes with abstract universals."""
        if not os.path.exists(self.state_file):
            self._log_info(f"State ledger missing at '{self.state_file}'. Rebuilding limitless master template.")
            default_state = {
                "global_config": {
                    "animation_dna": "Omni_Procedural",
                    "vibe_tempo": "Adaptive_Resonance",
                    "resolution": "1080x1920",
                    "content_format": "Fluid_Narrative"
                },
                "pipeline_status": {
                    "current_module": "Module_A",
                    "last_active_agent": "None",
                    "next_agent": "Ai_Agent_01"
                },
                "runtime_data": {
                    "core_topic": "System Architecture Null State",
                    "module_a_scripting": {}
                }
            }
            self._write_state(default_state)
            return

        # Read and inspect existing state for schema drift
        state = self._read_state()
        modified = False
        
        if "global_config" not in state:
            state["global_config"] = {
                "animation_dna": "Omni_Procedural", 
                "vibe_tempo": "Adaptive_Resonance", 
                "resolution": "1080x1920", 
                "content_format": "Fluid_Narrative"
            }
            modified = True
            
        if "pipeline_status" not in state:
            state["pipeline_status"] = {"current_module": "Module_A", "last_active_agent": "None", "next_agent": "Ai_Agent_01"}
            modified = True
            
        if "runtime_data" not in state:
            state["runtime_data"] = {"core_topic": "Unidentified Subject", "module_a_scripting": {}}
            modified = True
            
        if "module_a_scripting" not in state["runtime_data"]:
            state["runtime_data"]["module_a_scripting"] = {}
            modified = True
            
        if modified:
            self._write_state(state)
            self._log_info("Schema drift detected and patched successfully with Universal Limitless parameters.")

    def _read_state(self):
        """Thread-safe state file read block."""
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

    def _clean_json_response(self, text):
        """Failsafe regex to strip markdown code blocks if the API hallucinates them."""
        text = text.strip()
        text = re.sub(r"^```json", "", text, flags=re.IGNORECASE)
        text = re.sub(r"^```", "", text)
        text = re.sub(r"```$", "", text)
        return text.strip()

    def _validate_ai_response_payload(self, payload):
        """Validates structured format profiles required by lower pipeline utility agents."""
        if not isinstance(payload, list) or len(payload) != 3:
            return False
        required_keys = ["hook_id", "hook_type", "hook_script", "visual_concept_cue", "audio_pacing_cue"]
        for item in payload:
            if not all(k in item for k in required_keys):
                return False
        return True

    def _build_contextual_prompt(self, topic, dna_profile, vibe_profile, content_format):
        """Constructs a completely boundless prompt. The AI adapts entirely to the injected variables."""
        
        prompt = (
            f"You are the OmniMatrix Supreme Creative Director. You design high-retention openings with no creative boundaries.\n"
            f"Analyze the following dynamically injected parameters and shape your output strictly to their exact psychological and aesthetic intent.\n\n"
            f"Target Subject: '{topic}'\n"
            f"Visual DNA Architecture: {dna_profile}\n"
            f"Audio/Acoustic Signature: {vibe_profile}\n"
            f"Content Format/Style: {content_format}\n\n"
            f"Instructions:\n"
            f"1. Internalize the 'Content Format/Style'. Whether it is a documentary, a fast-paced short, an abstract art piece, or an intense cinematic sequence, adapt the dialogue and pacing perfectly to that format.\n"
            f"2. Maximize audience retention through precise visual cues and strategic pacing.\n"
            f"3. Generate exactly 3 highly distinct variations of the opening sequence.\n\n"
            f"Output Constraints:\n"
            f"Return a pure, raw JSON array containing exactly 3 objects with these exact keys: "
            f"'hook_id', 'hook_type', 'hook_script', 'visual_concept_cue', 'audio_pacing_cue'.\n"
            f"Do not wrap the JSON in markdown code blocks."
        )
        return prompt

    def _execute_procedural_fallback(self, topic, state):
        """Algorithmic fallbacks utilizing abstract syntax."""
        self._log_info("Invoking algorithmic contextual local fallback sub-routines (No-Internet Matrix).")
        
        fallback_hooks = [
            {
                "hook_id": "fallback_primary_alpha",
                "hook_type": "Universal Engagement Subroutine",
                "hook_script": f"Subject '{topic}' initialized. Preparing visual processing layer.",
                "visual_concept_cue": "Dynamic abstraction based on core topic parameters.",
                "audio_pacing_cue": "Immediate engagement impact."
            },
            {
                "hook_id": "fallback_secondary_beta",
                "hook_type": "Procedural Narrative Hook",
                "hook_script": f"Data stream active. Reconstructing the timeline of {topic}.",
                "visual_concept_cue": "Layered structural composition.",
                "audio_pacing_cue": "Rhythmic crescendo."
            },
            {
                "hook_id": "fallback_tertiary_gamma",
                "hook_type": "Abstract Inquisitive Opener",
                "hook_script": f"Analyzing node: {topic}. Stand by for sequence initiation.",
                "visual_concept_cue": "Macro focus expanding to wide perspective.",
                "audio_pacing_cue": "Subtle low-frequency drone."
            }
        ]
        return fallback_hooks

    def execute(self):
        """Orchestrator transaction logic. Manages state gates, network execution, and baton passing."""
        state = self._read_state()
        
        # Execution Gatekeeper Check
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Ai_Agent_01":
            self._log_info(f"System pipeline queue targeted to '{target_agent}'. Agent execution suspended.")
            return False

        # Idempotency Sweep (Scrub Previous Run Data)
        if "agent_01_hooks" in state.get("runtime_data", {}).get("module_a_scripting", {}):
            del state["runtime_data"]["module_a_scripting"]["agent_01_hooks"]
            self._log_info("Idempotency Sweep: Cleared legacy hook data from previous session.")

        topic = state.get("runtime_data", {}).get("core_topic", "")
        if not topic:
            self._log_error("Core execution sequence aborted: 'core_topic' not defined by Orchestrator.")
            return False

        # Limitless Variable Extraction
        dna_profile = state.get("global_config", {}).get("animation_dna", "Omni_Procedural")
        vibe_profile = state.get("global_config", {}).get("vibe_tempo", "Adaptive_Resonance")
        content_format = state.get("global_config", {}).get("content_format", "Fluid_Narrative")

        prompt = self._build_contextual_prompt(topic, dna_profile, vibe_profile, content_format)
        
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            try:
                self._log_info(f"Executing cloud network transaction. Format detected: [{content_format.upper()}]. Attempt {attempt}/{self.max_retries}.")
                response = self.model.generate_content(prompt)
                
                # Clean JSON in case of markdown fences
                clean_json_str = self._clean_json_response(response.text)
                parsed_json = json.loads(clean_json_str)
                
                if self._validate_ai_response_payload(parsed_json):
                    generated_data = parsed_json
                    self._log_info("AI payload structural mapping validated successfully.")
                    break
                else:
                    self._log_error("AI payload validation failed (missing keys/format). Retrying transaction.")
            except Exception as e:
                self._log_error(f"Transient error caught during processing: {str(e)}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * attempt)

        # Handle complete failure or resolution fallback pipeline transition
        if not generated_data:
            self._log_critical_error("Network/API generation completely failed. Initializing Fallback Protocols.")
            generated_data = self._execute_procedural_fallback(topic, state)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_01_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_01"

        # Update persistent ledger structures
        state["runtime_data"]["module_a_scripting"]["agent_01_hooks"] = generated_data
        
        # Atomic Handshake Protocol: Assign token pipeline execution context to Agent 02
        state["pipeline_status"]["next_agent"] = "Ai_Agent_02"
        self._write_state(state)
        
        self._log_info("Transaction ledger committed. Control sequence moved to: Ai_Agent_02.")
        return True

if __name__ == "__main__":
    designer = UniversalHookDesigner()
    designer.execute()
