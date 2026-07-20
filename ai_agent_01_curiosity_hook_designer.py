import os
import sys
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class UniversalHookDesigner:
    def __init__(self, state_file_path="matrix_state.json"):
        self.agent_name = "Ai Agent 01: universal_hook_designer"
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
            self._log_info(f"State ledger '{self.state_file}' missing. Rebuilding universal master template.")
            default_state = {
                "global_config": {
                    "animation_dna": "Anime",
                    "vibe_tempo": "Dark & Suspenseful",
                    "resolution": "1080x1920",
                    "content_format": "cinematic_movie" # Options: explainer, cinematic_movie, casual_commentary
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
        
        if "global_config" not in state:
            state["global_config"] = {"animation_dna": "Anime", "vibe_tempo": "Phonk", "resolution": "1080x1920", "content_format": "explainer"}
            modified = True
        elif "content_format" not in state["global_config"]:
            state["global_config"]["content_format"] = "explainer"
            modified = True
            
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
            self._log_info("Schema drift detected and patched successfully with Universal capabilities.")

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

    def _build_contextual_prompt(self, topic, dna_profile, vibe_profile, content_format):
        """Constructs highly dynamic prompts based on the desired universal content format."""
        
        base_instructions = (
            f"You are a master creative director and writer. Generate exactly 3 variants for the opening of the content.\n"
            f"Target Topic: '{topic}'\n"
            f"Visual DNA: {dna_profile}\n"
            f"Audio Vibe: {vibe_profile}\n\n"
            f"Output Constraints:\n"
            f"Output must be a raw JSON array containing exactly 3 objects with keys: "
            f"'hook_id', 'hook_type', 'hook_script', 'visual_concept_cue', 'audio_pacing_cue'.\n"
        )

        if content_format == "cinematic_movie":
            format_rules = (
                f"FORMAT: CINEMATIC ANIME/MOVIE EPISODE\n"
                f"You are writing the 'Cold Open' scene of an episode. No YouTubers, no narration. Characters are in the world.\n"
                f"In 'hook_script', write actual screenplays (e.g., [Character Name]: Dialogue + Action).\n"
                f"1. hook_id: 'action_open' | Focus: Start immediately in the middle of a high-stakes physical or magical conflict.\n"
                f"2. hook_id: 'suspense_dialogue' | Focus: Two characters facing off, intense dialogue before the clash.\n"
                f"3. hook_id: 'world_build' | Focus: Slow environmental reveal with a single chilling line of dialogue at the end.\n"
            )
        elif content_format == "casual_commentary":
            format_rules = (
                f"FORMAT: CASUAL CREATOR COMMENTARY\n"
                f"You are a friendly, natural content creator reviewing or reacting to the topic. Keep the language natural, like talking to a friend.\n"
                f"In 'hook_script', write the opening lines of the creator.\n"
                f"1. hook_id: 'friendly_question' | Focus: Ask a relatable question to the audience about the topic.\n"
                f"2. hook_id: 'reaction_shock' | Focus: Start with genuine surprise or excitement about a specific detail.\n"
                f"3. hook_id: 'hidden_detail' | Focus: Casually point out an easter egg or detail fans might have missed.\n"
            )
        else: # Default: explainer (aggressive hooks)
            format_rules = (
                f"FORMAT: AGGRESSIVE VIRAL EXPLAINER\n"
                f"You are a short-form content retention engineer. Make the viewer stop scrolling instantly.\n"
                f"In 'hook_script', write an aggressive voiceover line.\n"
                f"1. hook_id: 'pattern_interrupt' | Focus: Complete violation of expectations within 1.2 seconds.\n"
                f"2. hook_id: 'controversial_angle' | Focus: Attack a deeply rooted historical fan premise.\n"
                f"3. hook_id: 'curiosity_loop' | Focus: Semantic frame cliffhanger withholding vital information.\n"
            )

        return base_instructions + format_rules

    def _execute_procedural_fallback(self, topic, state):
        """Algorithmic fallbacks configured by context strings if internet/API fails entirely."""
        self._log_info("Invoking algorithmic contextual local fallback sub-routines.")
        
        content_format = state.get("global_config", {}).get("content_format", "explainer")
        
        if content_format == "cinematic_movie":
            hook_script_1 = f"[Shadowy Figure]: You thought {topic} was the end. It was just the prologue. (Steps out of the smoke)"
        elif content_format == "casual_commentary":
            hook_script_1 = f"Did you guys also notice that weird thing about {topic} in the latest release? I can't stop thinking about it."
        else:
            hook_script_1 = f"Everything you understood about {topic} was constructed as a lie."

        fallback_hooks = [
            {
                "hook_id": "fallback_primary",
                "hook_type": "Primary Fallback",
                "hook_script": hook_script_1,
                "visual_concept_cue": "System default visual load.",
                "audio_pacing_cue": "System default audio bed."
            },
            {
                "hook_id": "fallback_secondary",
                "hook_type": "Secondary Fallback",
                "hook_script": f"Backup script initialized for {topic}.",
                "visual_concept_cue": "Standard frame.",
                "audio_pacing_cue": "Standard audio."
            },
            {
                "hook_id": "fallback_tertiary",
                "hook_type": "Tertiary Fallback",
                "hook_script": f"System processing {topic} offline.",
                "visual_concept_cue": "Standard frame.",
                "audio_pacing_cue": "Standard audio."
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
        content_format = state.get("global_config", {}).get("content_format", "explainer")

        prompt = self._build_contextual_prompt(topic, dna_profile, vibe_profile, content_format)
        
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            try:
                self._log_info(f"Executing cloud network transaction ({content_format.upper()} Mode). Attempt {attempt} of {self.max_retries}.")
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
        
        self._log_info(f"Transaction ledger committed in {content_format} mode. Control sequence moved to Ai_Agent_02.")
        return True

if __name__ == "__main__":
    designer = UniversalHookDesigner()
    designer.execute()
