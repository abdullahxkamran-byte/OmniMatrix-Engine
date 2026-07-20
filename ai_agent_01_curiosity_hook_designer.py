import os
import sys
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class CuriosityHookDesigner:
    def __init__(self, state_file_path="matrix_state.json"):
        self.agent_name = "Ai Agent 01: curiosity_hook_designer"
        self.state_file = state_file_path
        self.max_retries = 3
        self.retry_delay = 2
        
        # Initialize and validate security layer
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            self._log_critical_error("GEMINI_API_KEY missing from environment initialization.")
            sys.exit(1)
            
        # Initialize Google GenAI configuration
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Internal state initialization check
        self._verify_and_patch_state_schema()

    def _log_info(self, message):
        print(f"[{self.agent_name}] INFO: {message}")

    def _log_error(self, message):
        print(f"[{self.agent_name}] ERROR: {message}", file=sys.stderr)

    def _log_critical_error(self, message):
        print(f"[{self.agent_name}] CRITICAL: {message}", file=sys.stderr)

    def _verify_and_patch_state_schema(self):
        """Validates matrix_state.json structural integrity, patching missing nodes on runtime."""
        if not os.path.exists(self.state_file):
            self._log_info(f"State ledger '{self.state_file}' missing. Rebuilding master template.")
            default_state = {
                "global_config": {
                    "animation_dna": "Anime",
                    "vibe_tempo": "Phonk",
                    "resolution": "1080x1920"
                },
                "pipeline_status": {
                    "current_module": "Module_A",
                    "last_active_agent": "None",
                    "next_agent": "Ai_Agent_01"
                },
                "runtime_data": {
                    "core_topic": "",
                    "module_a_scripting": {}
                }
            }
            self._write_state(default_state)
            return

        # Read and inspect existing state for schema drift
        state = self._read_state()
        modified = False
        
        if "pipeline_status" not in state:
            state["pipeline_status"] = {"current_module": "Module_A", "last_active_agent": "None", "next_agent": "Ai_Agent_01"}
            modified = True
        if "runtime_data" not in state:
            state["runtime_data"] = {"core_topic": "", "module_a_scripting": {}}
            modified = True
        if "module_a_scripting" not in state["runtime_data"]:
            state["runtime_data"]["module_a_scripting"] = {}
            modified = True
            
        if modified:
            self._write_state(state)
            self._log_info("Schema drift detected and patched successfully.")

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

    def _validate_ai_response_payload(self, payload):
        """Validates structured format profiles required by lower pipeline utility agents."""
        if not isinstance(payload, list) or len(payload) != 3:
            return False
        required_keys = ["hook_id", "hook_type", "hook_script", "visual_concept_cue", "audio_pacing_cue"]
        for item in payload:
            if not all(k in item for k in required_keys):
                return False
        return True

    def _build_contextual_prompt(self, topic, dna_profile, vibe_profile):
        """Constructs heavily contextual engineering guidelines for the LLM architecture."""
        return (
            f"You are a computational short-form content retention engineer. "
            f"Generate exactly 3 raw, highly aggressive hook variants for target topic: '{topic}'.\n"
            f"Contextual Parameters Enforced:\n"
            f"- Art/VFX Context Direction (DNA): {dna_profile}\n"
            f"- Audio Design/Pacing Rhythm (Vibe): {vibe_profile}\n\n"
            f"Execution specifications required:\n"
            f"1. hook_id: 'pattern_interrupt' | Focus: Complete violation of auditory/visual expectations to capture attention within 1.2 seconds.\n"
            f"2. hook_id: 'controversial_angle' | Focus: Attack a deeply rooted historical fan premise or objective core concept belief.\n"
            f"3. hook_id: 'curiosity_loop' | Focus: Semantic frame cliffhanger. Withhold vital information explicitly completed at the absolute final frame.\n\n"
            f"Output Constraints:\n"
            f"Your output must strictly resolve into a JSON array containing exactly 3 objects. "
            f"Required object keys: 'hook_id', 'hook_type', 'hook_script', 'visual_concept_cue', 'audio_pacing_cue'. "
            f"Do not format with Markdown code block syntax wrapper. Provide absolute raw text JSON."
        )

    def _execute_procedural_fallback(self, topic, state):
        """Algorithmic fallbacks configured by context strings if internet/API fails entirely."""
        self._log_info("Invoking algorithmic contextual local fallback sub-routines.")
        dna = state.get("global_config", {}).get("animation_dna", "Anime")
        
        # Tailor fallback visual/audio cues depending on context strings
        if dna.lower() == "anime":
            v_cue_1 = "High contrast cel-shaded lighting bloom with speedlines."
            a_cue_1 = "Aggressive Phonk sub-bass drift explosion."
        else:
            v_cue_1 = "Cinematic volumetric smoke overlay with dramatic split frame."
            a_cue_1 = "Sub-bass industrial drone impact wave."

        fallback_hooks = [
            {
                "hook_id": "pattern_interrupt",
                "hook_type": "Pattern Interrupt",
                "hook_script": f"Everything you understood about {topic} was constructed as a lie.",
                "visual_concept_cue": v_cue_1,
                "audio_pacing_cue": a_cue_1
            },
            {
                "hook_id": "controversial_angle",
                "hook_type": "Controversial Angle",
                "hook_script": f"The entire fanbase completely misunderstood {topic}, and the truth is painful.",
                "visual_concept_cue": "Rapid split-screen asset frame flashing.",
                "audio_pacing_cue": "Instant sidechained frequency drop cutout."
            },
            {
                "hook_id": "curiosity_loop",
                "hook_type": "Curiosity Loop",
                "hook_script": f"There is a single hidden reality within {topic} that changes everything. Watch closely.",
                "visual_concept_cue": "Slow atmospheric push camera move.",
                "audio_pacing_cue": "Low frequency structural atmospheric pad humming."
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

        topic = state.get("runtime_data", {}).get("core_topic", "")
        if not topic:
            self._log_error("Core execution sequence aborted: 'core_topic' not defined by Agent 65 orchestrator.")
            return False

        dna_profile = state.get("global_config", {}).get("animation_dna", "Anime")
        vibe_profile = state.get("global_config", {}).get("vibe_tempo", "Phonk")

        prompt = self._build_contextual_prompt(topic, dna_profile, vibe_profile)
        
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            try:
                self._log_info(f"Executing cloud network transaction. Attempt {attempt} of {self.max_retries}.")
                response = self.model.generate_content(prompt)
                parsed_json = json.loads(response.text)
                
                if self._validate_ai_response_payload(parsed_json):
                    generated_data = parsed_json
                    break
                else:
                    self._log_error("AI payload structural mapping validation failed. Retrying transaction.")
            except Exception as e:
                self._log_error(f"Transient error caught during processing: {str(e)}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * attempt)

        # Handle complete failure or resolution fallback pipeline transition
        if not generated_data:
            generated_data = self._execute_procedural_fallback(topic, state)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_01_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_01"

        # Update persistent ledger structures
        state["runtime_data"]["module_a_scripting"]["agent_01_hooks"] = generated_data
        
        # Atomic Handshake Protocol: Assign token pipeline execution context to Agent 02
        state["pipeline_status"]["next_agent"] = "Ai_Agent_02"
        self._write_state(state)
        
        self._log_info("Transaction ledger committed. Control sequence moved to Ai_Agent_02.")
        return True

if __name__ == "__main__":
    designer = CuriosityHookDesigner()
    designer.execute()
