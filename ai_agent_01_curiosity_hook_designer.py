import os
import sys
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class CuriosityHookDesigner:
    def __init__(self, state_file_path="matrix_state.json"):
        self.agent_name = "Agent_01_Curiosity_Hook_Designer"
        self.state_file = state_file_path
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print(f"[{self.agent_name}] CRITICAL ERROR: GEMINI_API_KEY not found in environment.")
            sys.exit(1)
            
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )

    def _read_state(self):
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[{self.agent_name}] ERROR: matrix_state.json not found. Agent 65 must initialize it first.")
            sys.exit(1)

    def _write_state(self, state_data):
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f, indent=4)
        print(f"[{self.agent_name}] SUCCESS: Hook data written to matrix_state.json")

    def execute(self):
        """
        Main worker execution sequence. Reads assigned topic from Agent 65,
        generates universal hooks, and hands over control to Agent 02.
        """
        state = self._read_state()
        
        # Verify if it is actually Agent 01's turn to run
        current_active_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if current_active_agent != "Ai_Agent_01":
            print(f"[{self.agent_name}] STANDBY: It is not my turn. Current agent in queue is {current_active_agent}.")
            return False

        # Read the core topic assigned by Agent 65
        topic = state.get("runtime_data", {}).get("core_topic", "")
        if not topic:
            print(f"[{self.agent_name}] ERROR: No topic assigned by Agent 65. Aborting task.")
            return False

        print(f"[{self.agent_name}] Booting sequence. Assigned Topic: '{topic}'")

        # Universal Prompt: Designed to handle anime, comics, movies, or abstract concepts
        system_prompt = (
            "You are an elite, universal short-form content strategist. "
            f"Your objective is to generate viral hooks for the topic: '{topic}'. "
            "This topic could be an anime battle, comic book lore, a movie theory, or a real-world concept. "
            "Adapt your tone automatically to fit the epic, mysterious, or kinetic nature of the topic. "
            "Generate exactly 3 hook variations:\n"
            "1. Pattern_Interrupt: A shocking, fast-paced opening statement that visually and audibly jolts the viewer.\n"
            "2. Controversial_Angle: A bold statement that directly challenges the fanbase's most common belief.\n"
            "3. Curiosity_Loop: An open-ended statement that introduces a hidden detail forcing them to watch until the end.\n\n"
            "Output MUST be a strictly formatted JSON array containing exactly 3 objects. "
            "Each object must contain keys: 'hook_type', 'hook_script', and 'visual_cue'. "
            "No markdown, no conversation, pure JSON data."
        )

        try:
            print(f"[{self.agent_name}] Communicating with Neural Brain (Gemini)...")
            response = self.model.generate_content(system_prompt)
            generated_hooks = json.loads(response.text)
            
            # Inject generated data into the Module A workspace within the global state
            if "module_a_scripting" not in state["runtime_data"]:
                state["runtime_data"]["module_a_scripting"] = {}
                
            state["runtime_data"]["module_a_scripting"]["agent_01_hooks"] = generated_hooks
            
            # Handoff control to the next agent in the pipeline
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_01"
            state["pipeline_status"]["next_agent"] = "Ai_Agent_02"
            
            self._write_state(state)
            print(f"[{self.agent_name}] Task complete. Passing baton to Ai_Agent_02.")
            return True

        except Exception as e:
            print(f"[{self.agent_name}] CRITICAL API FAILURE: {str(e)}")
            self._apply_fallback(state, topic)
            return False

    def _apply_fallback(self, state, topic):
        """Generates dynamic offline fallbacks so the pipeline does not break."""
        print(f"[{self.agent_name}] Engaging universal fallback protocol.")
        fallback_hooks = [
            {
                "hook_type": "Pattern_Interrupt",
                "hook_script": f"Everything you thought you knew about {topic} is completely wrong.",
                "visual_cue": "Rapid zoom-in with chromatic aberration and sub-bass impact."
            },
            {
                "hook_type": "Controversial_Angle",
                "hook_script": f"The biggest debate regarding {topic} has already been solved, and fans hate the answer.",
                "visual_cue": "Split-screen comparison with a heavy vignette."
            },
            {
                "hook_type": "Curiosity_Loop",
                "hook_script": f"There is one hidden detail in {topic} that changes the entire storyline. Watch closely.",
                "visual_cue": "Slow, cinematic pan revealing a blurred background element."
            }
        ]
        
        if "module_a_scripting" not in state["runtime_data"]:
            state["runtime_data"]["module_a_scripting"] = {}
            
        state["runtime_data"]["module_a_scripting"]["agent_01_hooks"] = fallback_hooks
        state["pipeline_status"]["last_active_agent"] = "Ai_Agent_01"
        state["pipeline_status"]["next_agent"] = "Ai_Agent_02"
        self._write_state(state)

if __name__ == "__main__":
    # This block allows Agent 01 to be triggered as a standalone script by the Conductor (Agent 65).
    worker_node = CuriosityHookDesigner()
    worker_node.execute()
