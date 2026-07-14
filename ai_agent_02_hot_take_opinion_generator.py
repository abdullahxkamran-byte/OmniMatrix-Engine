import os
import re
import sys
import json
import urllib.request
import urllib.error

class HotTakeOpinionGenerator:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 02: hot_take_opinion_generator"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        # Check if user has defined a premium cloud API Key in system environment
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_previous_stage(self):
        """
        Dynamically loads output from stage 1. If missing, prompts the user 
        dynamically for a topic to keep the run completely universal.
        """
        input_file_path = os.path.join(self.workspace_dir, "01_curiosity_hooks.json")
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Read previous stage data from '{input_file_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Could not read stage 1 file ({str(e)}). Transitioning to manual mode.")
        
        # Interactive universal terminal trigger if previous file is missing
        print(f"[{self.agent_name}] Active File Check: Previous stages are offline.")
        user_input = input("Enter a dynamic topic to generate controversial arguments: ").strip()
        if not user_input:
            print("[System Error] No topic provided. Terminating execution.")
            sys.exit(1)
            
        return {
            "source_topic": user_input,
            "hooks": [
                {
                    "hook_id": "direct_input",
                    "hook_text": f"The dynamic reality of {user_input}",
                    "visual_concept_cue": "Dynamic visual flash"
                }
            ]
        }

    def _clean_json_response(self, raw_text):
        """
        Strips wrapper blocks from AI model responses to isolate raw, parseable JSON.
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

    def _save_to_workspace(self, data, filename="02_hot_takes.json"):
        """
        Saves parsed structured opinions physically to workspace directory.
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

    def generate_opinions(self):
        """
        Processes dynamic topics to extract intense, contrarian arguments for viral retention.
        """
        input_data = self._load_previous_stage()
        topic = input_data.get("source_topic", "Unknown Subject")
        
        # Use first available hook to anchor the argument
        hooks = input_data.get("hooks", [])
        chosen_hook = hooks[0]["hook_text"] if hooks else f"The ultimate secret of {topic}"

        print(f"[{self.agent_name}] Generating psychological hot takes for: '{topic}'")

        system_prompt = (
            "You are an expert retention analyst and high-friction scriptwriter. "
            "Your objective is to take a core topic and construct highly controversial, "
            "mind-bending, and intellectually gripping 'Hot Takes' or contrarian opinions. "
            "Provide exactly 2 distinct hot-take options:\n"
            "1. The Outrageous Paradigm Shift (completely flips general assumptions)\n"
            "2. The Psychological Deception (argues that the audience is being actively fooled by popular narratives).\n"
            "Each take must have three parameters:\n"
            "- 'take_id': a unique string key\n"
            "- 'statement': a raw, aggressive hook statement (one powerful sentence)\n"
            "- 'argument_backing': a concise 2-sentence explanation of why this claim is logically or contextually true.\n"
            "Format your output STRICTLY as a raw JSON object containing a list named 'hot_takes'. "
            "Do not include any chat formatting, greetings, markdown blocks, or warnings. Only output valid JSON."
        )

        user_prompt = f"Topic: {topic}\nChosen Hook: {chosen_hook}"

        # Dynamic connection router: OpenAI Cloud vs Local Ollama
        if self.openai_api_key:
            print(f"[{self.agent_name}] Status: Premium Cloud Key detected. Querying OpenAI [{self.model_cloud}]")
            url = self.openai_url
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            payload = {
                "model": self.model_cloud,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "response_format": {"type": "json_object"}
            }
        else:
            print(f"[{self.agent_name}] Status: Querying Local Engine [{self.model_local}]")
            url = self.ollama_url
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

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            
            with urllib.request.urlopen(req, timeout=45) as response:
                result = response.read().decode("utf-8")
                response_json = json.loads(result)
                
                # Extract message content dynamically based on API platform format
                if self.openai_api_key:
                    raw_ai_message = response_json["choices"][0]["message"]["content"]
                else:
                    raw_ai_message = response_json["message"]["content"]
                
                cleaned_message = self._clean_json_response(raw_ai_message)
                structured_output = json.loads(cleaned_message)
                
                final_output = {
                    "source_topic": topic,
                    "referenced_hook": chosen_hook,
                    "agent_executed": self.agent_name,
                    "hot_takes": structured_output.get("hot_takes", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except urllib.error.URLError as e:
            print(f"[{self.agent_name}] Connection Error: AI Engine is unreachable. Moving to physical fallback.")
            return self._execute_procedural_fallback(topic, chosen_hook)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[{self.agent_name}] Data Error: Could not parse AI response. Launching physical fallback.")
            return self._execute_procedural_fallback(topic, chosen_hook)

    def _execute_procedural_fallback(self, topic, chosen_hook):
        """
        Generates functional, context-specific fallback arguments dynamically 
        for any topic when servers are down.
        """
        fallback_data = {
            "source_topic": topic,
            "referenced_hook": chosen_hook,
            "agent_executed": f"{self.agent_name} (Procedural Fallback Mode)",
            "hot_takes": [
                {
                    "take_id": "outrageous_paradigm_shift",
                    "statement": f"We have been completely lied to about the actual origins of {topic}.",
                    "argument_backing": f"The standard historical consensus surrounding {topic} completely ignores core mathematical anomalies. When you review the raw raw data, the conventional theories break down instantly."
                },
                {
                    "take_id": "psychological_deception",
                    "statement": f"The absolute worst mistake you can make when studying {topic} is trusting mainstream creators.",
                    "argument_backing": f"Most experts repeat identical talking points to preserve their own status. They actively hide structural details that disprove their entire narrative."
                }
            ]
        }
        self._save_to_workspace(fallback_data)
        return fallback_data

if __name__ == "__main__":
    generator = HotTakeOpinionGenerator()
    output = generator.generate_opinions()
    
    print("\n--- Z-NET CORE MODULE A: AGENT 02 OUTPUT COMPLETE ---")
    print(json.dumps(output, indent=4))
    print("------------------------------------------------------")
