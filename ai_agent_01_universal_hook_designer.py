import os
import sys
import json
import time
import google.generativeai as genai

class Ai_Agent_01_Universal_Hook_Designer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("[Ai_Agent_01] CRITICAL ERROR: GEMINI_API_KEY missing from environment variables.")
            
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name='gemini-flash-latest',
            generation_config={"response_mime_type": "application/json"}
        )
        self.max_retries = 3

    def execute(self, state: dict) -> dict:
        target_agent = state.get("pipeline_status", {}).get("next_agent", "Ai_Agent_01")
        if target_agent != "Ai_Agent_01":
            print(f"[Ai_Agent_01] Skipped. System pipeline queue is targeted to: {target_agent}")
            return state

        if "module_a_scripting" not in state.setdefault("runtime_data", {}):
            state["runtime_data"]["module_a_scripting"] = {}

        if "agent_01_hooks" in state["runtime_data"]["module_a_scripting"]:
            del state["runtime_data"]["module_a_scripting"]["agent_01_hooks"]
            print("[Ai_Agent_01] Idempotency Sweep: Scrubbed legacy hook data from state.")

        topic = state.get("runtime_data", {}).get("core_topic", "")
        master_theme = state.get("runtime_data", {}).get("master_theme_blueprint", "Cinematic Dark Action")

        if not topic:
            raise ValueError("[Ai_Agent_01] ERROR: 'core_topic' not found in state data. Execution aborted.")

        prompt = (
            f"You are the OmniMatrix Supreme Cinematic Director.\n"
            f"Analyze the core topic: '{topic}' and the aesthetic theme: '{master_theme}'.\n"
            f"Generate EXACTLY 3 highly distinct, theme-adaptive 3-second opening cinematic hooks to maximize audience retention.\n"
            f"Rule 1: Do not use generic labels. Output must be raw technical execution directives.\n"
            f"Rule 2: Option 1 MUST always be a Pure Environmental/Foley hook with ZERO dialogue (relying entirely on visual shock and soundscape).\n"
            f"Return the output strictly matching this JSON schema:\n"
            f"{{\n"
            f"  \"agent_01_hooks\": [\n"
            f"    {{\n"
            f"      \"hook_approach\": \"String (e.g., Pure Environmental Silence, Kinetic Impact, High Tension Dialogue)\",\n"
            f"      \"visual_camera_action\": \"String (Precise 3D spatial camera movement, lighting shockers, and object fracturing)\",\n"
            f"      \"foley_sfx_audio\": \"String (Specific Hz drops, wind howling, concrete breaking, or ambient sounds)\",\n"
            f"      \"verbal_text_overlay\": \"String (Specific dialogue or cinematic onscreen text. Use 'None' for purely environmental hooks)\"\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        generated_data = None
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[Ai_Agent_01] Triggering Neural Graph (Gemini API) - Attempt {attempt}/{self.max_retries}...")
                response = self.model.generate_content(prompt)
                
                parsed_json = json.loads(response.text)
                
                if "agent_01_hooks" in parsed_json and len(parsed_json["agent_01_hooks"]) == 3:
                    generated_data = parsed_json
                    print("[Ai_Agent_01] API payload structural mapping validated successfully.")
                    break
                else:
                    raise ValueError("Schema validation failed: Did not receive exactly 3 cinematic hooks.")
                    
            except Exception as e:
                last_error = str(e)
                print(f"[Ai_Agent_01] ERROR on attempt {attempt}: {last_error}")
                if attempt < self.max_retries:
                    time.sleep(2)

        if not generated_data:
            raise RuntimeError(f"[Ai_Agent_01] CRITICAL FAILURE: API Generation failed after {self.max_retries} attempts. Last Error Traceback: {last_error}")

        state["runtime_data"]["module_a_scripting"]["agent_01_hooks"] = generated_data["agent_01_hooks"]
        
        state.setdefault("pipeline_status", {})["Ai_Agent_01"] = "COMPLETED"

        state_file_path = state.get("state_file_path")
        if state_file_path:
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print("[Ai_Agent_01] Transaction Ledger Committed. 3 Cinematic Hooks Injected. Task Completed.")
        return state
