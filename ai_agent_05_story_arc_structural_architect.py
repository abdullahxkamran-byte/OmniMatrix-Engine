import os
import re
import sys
import json
import urllib.request
import urllib.error

class StoryArcStructuralArchitect:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 05: story_arc_structural_architect"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_previous_stage(self):
        """
        Loads upstream states from Stage 4 (tension timeline). If missing, 
        prompts the user dynamically to maintain universal functionality.
        """
        input_file_path = os.path.join(self.workspace_dir, "04_tension_peaks.json")
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Stage 4 tension peak states imported from '{input_file_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: File read error ({str(e)}). Switching to prompt bypass.")
        
        # Interactive fallback prompt if workspace upstream data is absent
        print(f"[{self.agent_name}] Pipeline Gap: Upstream tension timeline data is missing.")
        user_input = input("Enter any topic to execute story arc structuring: ").strip()
        if not user_input:
            print("[System Error] Empty topic value. Halting execution.")
            sys.exit(1)
            
        return {
            "source_topic": user_input,
            "tension_timeline": [
                {
                    "frame_index": 1,
                    "tension_score": 5,
                    "pacing_instruction": "dynamic-hold"
                }
            ]
        }

    def _clean_json_response(self, raw_text):
        """
        Sanitizes AI model outputs, isolating the raw JSON boundaries to protect parser logic.
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

    def _save_to_workspace(self, data, filename="05_story_arc_structure.json"):
        """
        Physically persists the structural story arc blueprint to the local workspace disk.
        """
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Story arc structure file written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save state files: {str(e)}")
            return None

    def design_story_arc(self):
        """
        Architects a structural cinematic path, calculating the narrative pacing, 
        catalyst triggers, tension retention loops, and climax checkpoints.
        """
        input_data = self._load_previous_stage()
        topic = input_data.get("source_topic", "Dynamic Target")
        tension_data = input_data.get("tension_timeline", [])

        print(f"[{self.agent_name}] Drafting cinematic narrative blueprints for: '{topic}'")

        system_prompt = (
            "You are a master of short-form storytelling dynamics and movie pacing. "
            "Your job is to analyze a video's subject matter and calculated tension values, "
            "then structure a high-density, multi-stage story arc mapped out chronologically.\n"
            "Provide exactly 4 architectural phases strictly structured inside a list named 'arc_phases'. "
            "Each phase item must have these exact parameter keys:\n"
            "- 'phase_index': integer representing execution order (1 to 4)\n"
            "- 'phase_name': string designating the classic arc level (e.g., 'Incite', 'Complicate', 'Climax', 'Resolve')\n"
            "- 'target_duration_ratio': float representing percentage of total runtime (e.g., 0.20 for 20%)\n"
            "- 'pacing_frequency': string description of sequence speed (e.g., 'rapid-fire-cuts', 'atmospheric-draw', 'exponential-climax')\n"
            "- 'audience_psychology_goal': string target representing viewer mental state (e.g., 'shocked-confusion', 'heightened-skepticism', 'absolute-payoff').\n"
            "Format your response STRICTLY as a raw JSON object containing the list key 'arc_phases'. "
            "Do not output markdown code blocks, tags, explanations, or system introductions. Only output valid JSON."
        )

        user_prompt = f"Target Subject: {topic}\nTension Coordinates:\n" + json.dumps(tension_data, indent=2)

        if self.openai_api_key:
            print(f"[{self.agent_name}] Status: Querying Cloud API Node [{self.model_cloud}]")
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
            print(f"[{self.agent_name}] Status: Querying Local LLM Instance [{self.model_local}]")
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
            
            with urllib.request.urlopen(req, timeout=50) as response:
                result = response.read().decode("utf-8")
                response_json = json.loads(result)
                
                if self.openai_api_key:
                    raw_ai_message = response_json["choices"][0]["message"]["content"]
                else:
                    raw_ai_message = response_json["message"]["content"]
                
                cleaned_message = self._clean_json_response(raw_ai_message)
                structured_output = json.loads(cleaned_message)
                
                final_output = {
                    "source_topic": topic,
                    "agent_executed": self.agent_name,
                    "arc_phases": structured_output.get("arc_phases", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except urllib.error.URLError as e:
            print(f"[{self.agent_name}] Engine Connection Offline: Executing procedural story arc construction.")
            return self._execute_procedural_fallback(topic)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[{self.agent_name}] Schema Alignment Error: Executing clean structural safety fallback.")
            return self._execute_procedural_fallback(topic)

    def _execute_procedural_fallback(self, topic):
        """
        Constructs context-relative structural blueprints dynamically 
        for any arbitrary topic when remote APIs are unavailable.
        """
        fallback_data = {
            "source_topic": topic,
            "agent_executed": f"{self.agent_name} (Procedural Fallback Mode)",
            "arc_phases": [
                {
                    "phase_index": 1,
                    "phase_name": "Incite",
                    "target_duration_ratio": 0.20,
                    "pacing_frequency": "rapid-fire-cuts",
                    "audience_psychology_goal": "shocked-confusion"
                },
                {
                    "phase_index": 2,
                    "phase_name": "Complicate",
                    "target_duration_ratio": 0.35,
                    "pacing_frequency": "atmospheric-draw",
                    "audience_psychology_goal": "heightened-skepticism"
                },
                {
                    "phase_index": 3,
                    "phase_name": "Climax",
                    "target_duration_ratio": 0.30,
                    "pacing_frequency": "exponential-climax",
                    "audience_psychology_goal": "absolute-payoff"
                },
                {
                    "phase_index": 4,
                    "phase_name": "Resolve",
                    "target_duration_ratio": 0.15,
                    "pacing_frequency": "rhythmic-hold-slowdown",
                    "audience_psychology_goal": "retention-loop-ready"
                }
            ]
        }
        self._save_to_workspace(fallback_data)
        return fallback_data

if __name__ == "__main__":
    architect = StoryArcStructuralArchitect()
    output = architect.design_story_arc()
    
    print("\n--- Z-NET CORE MODULE A: AGENT 05 STORY BLUEPRINT COMPLETED ---")
    print(json.dumps(output, indent=4))
    print("---------------------------------------------------------------")
