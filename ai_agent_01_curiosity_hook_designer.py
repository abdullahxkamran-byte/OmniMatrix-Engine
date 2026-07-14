import os
import re
import sys
import json
import urllib.request
import urllib.error

class CuriosityHookDesigner:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 01: curiosity_hook_designer"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_name = "llama3"
        self.workspace_dir = workspace_dir
        
        # Physical workspace directory creation
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _clean_json_response(self, raw_text):
        """
        Extracts and cleans raw JSON from the LLM response to prevent structure crashes.
        """
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def _save_to_workspace(self, data, filename="01_curiosity_hooks.json"):
        """
        Persists the generated dynamic output to physical disk storage.
        """
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: State persisted to physical file at '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Could not write state file: {str(e)}")
            return None

    def generate_hooks(self, core_topic):
        """
        Takes any dynamic topic in the universe and processes it via the local LLM matrix.
        """
        print(f"[{self.agent_name}] Initializing execution loop for dynamic topic: '{core_topic}'")

        system_prompt = (
            "You are an expert short-form video retention strategist for YouTube Shorts and TikTok. "
            "Your job is to generate highly engaging, intense, and high-retention hook variations. "
            "Provide exactly 3 distinct hook variations:\n"
            "1. Pattern Interrupt (creates dynamic shock)\n"
            "2. Controversial Angle (challenges a well-known community belief)\n"
            "3. Curiosity Loop (forces them to watch until the absolute end).\n"
            "Format your response STRICTLY as a raw JSON object containing a list named 'hooks', "
            "where each hook item has the following keys: 'hook_id', 'hook_text', and 'visual_concept_cue'. "
            "Do not include any greeting, conversational text, or explanation. Only output valid JSON."
        )

        user_prompt = f"Topic: {core_topic}"

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "format": "json"
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.ollama_url, 
                data=data, 
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=45) as response:
                result = response.read().decode("utf-8")
                response_json = json.loads(result)
                raw_ai_message = response_json["message"]["content"]
                
                cleaned_message = self._clean_json_response(raw_ai_message)
                structured_output = json.loads(cleaned_message)
                
                final_output = {
                    "source_topic": core_topic,
                    "agent_executed": self.agent_name,
                    "hooks": structured_output.get("hooks", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except urllib.error.URLError as e:
            print(f"[{self.agent_name}] Connection Failure: Local LLM engine is offline. Activating fallback handler.")
            return self._execute_procedural_fallback(core_topic)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[{self.agent_name}] Parser Failure: LLM returned malformed data. Re-routing to structured fallback.")
            return self._execute_procedural_fallback(core_topic)

    def _execute_procedural_fallback(self, core_topic):
        """
        Dynamically constructs procedural fallbacks for any topic when offline.
        """
        fallback_data = {
            "source_topic": core_topic,
            "agent_executed": f"{self.agent_name} (Procedural Fallback Mode)",
            "hooks": [
                {
                    "hook_id": "pattern_interrupt",
                    "hook_text": f"The hidden dark conspiracy surrounding {core_topic} that everyone missed.",
                    "visual_concept_cue": "Extreme rapid zoom, flash glitch effect matching sub-bass heavy frequency drop."
                },
                {
                    "hook_id": "controversial_angle",
                    "hook_text": f"Why your entire perspective on {core_topic} is completely incorrect.",
                    "visual_concept_cue": "Splitscreen visual frame comparison with high contrast cel-shaded lighting bloom."
                },
                {
                    "hook_id": "curiosity_loop",
                    "hook_text": f"Pay very close attention, because this single dynamic detail changes absolutely everything about {core_topic}.",
                    "visual_concept_cue": "Slow atmospheric pan moving into a dark, foggy environment grid."
                }
            ]
        }
        self._save_to_workspace(fallback_data)
        return fallback_data

if __name__ == "__main__":
    designer = CuriosityHookDesigner()
    
    # Check if a dynamic topic was passed via command line terminal argument
    if len(sys.argv) > 1:
        # Example: python ai_agent_01_curiosity_hook_designer.py "Dunia ki koi bhi cheez"
        input_topic = " ".join(sys.argv[1:])
    else:
        # Prompt user dynamically if no argument was passed to terminal
        print("\n--- Z-NET ABSOLUTE ENGINE CORE SETUP ---")
        input_topic = input("Enter any topic in the universe to process: ").strip()
        if not input_topic:
            print("[System Error] Topic cannot be empty. Terminating execution.")
            sys.exit(1)

    result_data = designer.generate_hooks(input_topic)
    
    print("\n--- Z-NET DYNAMIC PROCESSING COMPLETE ---")
    print(json.dumps(result_data, indent=4))
    print(f"Output stored physically in workspace directory.")
