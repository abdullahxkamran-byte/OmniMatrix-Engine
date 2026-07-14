import os
import re
import sys
import json
import urllib.request
import urllib.error

class VisualSyncStoryboarder:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 03: visual_sync_storyboarder"
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
        Dynamically imports structural states from stage 2. If absent, 
        prompts the user to declare a topic, keeping processing universal.
        """
        input_file_path = os.path.join(self.workspace_dir, "02_hot_takes.json")
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Stage 2 state detected and imported from '{input_file_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: File read error ({str(e)}). Transitioning to terminal input.")
        
        # Interactive fallback prompt if workspace has no active upstream data
        print(f"[{self.agent_name}] Pipeline Gap: Upstream data file '{input_file_path}' is missing.")
        user_input = input("Enter any topic to execute storyboard mapping: ").strip()
        if not user_input:
            print("[System Error] Empty target value. Halting engine run.")
            sys.exit(1)
            
        return {
            "source_topic": user_input,
            "referenced_hook": f"The hidden mechanism behind {user_input}",
            "hot_takes": [
                {
                    "take_id": "manual_bypass",
                    "statement": f"Everything you knew about {user_input} was designed to keep you blind.",
                    "argument_backing": "Mainstream summaries skip the mechanical physics driving this issue."
                }
            ]
        }

    def _clean_json_response(self, raw_text):
        """
        Cleans wrapping, backticks, and markdown decorators to secure raw JSON strings.
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

    def _save_to_workspace(self, data, filename="03_visual_storyboard.json"):
        """
        Persists the structured storyboarding database file to the shared Z-Net workspace.
        """
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Visual storyboard matrix persisted to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save state files: {str(e)}")
            return None

    def generate_storyboard(self):
        """
        Synthesizes core narrative arguments into chronological, multi-track visual 
        and audio-synced production blueprints.
        """
        input_data = self._load_previous_stage()
        topic = input_data.get("source_topic", "General Topic")
        referenced_hook = input_data.get("referenced_hook", f"The reality of {topic}")
        
        # Load available arguments to structure storyboard pacing
        hot_takes = input_data.get("hot_takes", [])
        chosen_statement = hot_takes[0]["statement"] if hot_takes else f"We have been fooled regarding {topic}"
        chosen_argument = hot_takes[0]["argument_backing"] if hot_takes else "The standard data does not support common assumptions."

        print(f"[{self.agent_name}] Processing cinematic storyboard timelines for target: '{topic}'")

        system_prompt = (
            "You are an expert anime-style visual designer, director, and editor. "
            "Your task is to take a core topic, hook, and argumentative script block, "
            "then break them down into a sequence of exactly 4 sequential storyboard frames for a short-form video.\n"
            "Each frame must contain these exact parameter keys:\n"
            "- 'frame_index': integer representing chronological order (1 to 4)\n"
            "- 'timestamp_start': calculated video start time (float, in seconds)\n"
            "- 'timestamp_end': calculated video end time (float, in seconds)\n"
            "- 'spoken_voiceover': the concise voiceover script to be read out loud in this frame (1 direct sentence in English)\n"
            "- 'scenic_art_prompt': ultra-detailed descriptive visual style prompt (cel-shaded, dark cyberpunk, anime realism, camera positioning) "
            "suitable for generative models or Blender assembly reference.\n"
            "- 'camera_movement_mode': kinetic direction (e.g., dynamic push, orbital tilt, fast pan, speed line stretch)\n"
            "- 'audio_sync_trigger': audio environment description (e.g., high bass slam, sidechain compression pumping, dark phonk kick rise).\n"
            "Format your output STRICTLY as a raw JSON object containing a list named 'storyboard_frames'. "
            "Do not include conversational greetings, markdown formatting blocks, or warnings. Output only valid JSON."
        )

        user_prompt = (
            f"Core Topic: {topic}\n"
            f"Intro Hook Context: {referenced_hook}\n"
            f"Primary Argument Block: {chosen_statement} {chosen_argument}"
        )

        if self.openai_api_key:
            print(f"[{self.agent_name}] Status: Querying Cloud API Network [{self.model_cloud}]")
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
            print(f"[{self.agent_name}] Status: Querying Local LLM Engine [{self.model_local}]")
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
                    "underlying_hook": referenced_hook,
                    "target_argument": f"{chosen_statement} {chosen_argument}",
                    "agent_executed": self.agent_name,
                    "storyboard_frames": structured_output.get("storyboard_frames", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except urllib.error.URLError as e:
            print(f"[{self.agent_name}] Interface Offline: Local/Cloud engines unreachable. Generating algorithmic storyboard fallback.")
            return self._execute_procedural_fallback(topic, referenced_hook, chosen_statement, chosen_argument)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[{self.agent_name}] Logic Error: Parsing sequence failed. Running mathematical safety fallback.")
            return self._execute_procedural_fallback(topic, referenced_hook, chosen_statement, chosen_argument)

    def _execute_procedural_fallback(self, topic, referenced_hook, chosen_statement, chosen_argument):
        """
        Creates structurally aligned timeline plans containing dynamic, context-specific cues 
        and animation parameters when APIs fail to answer.
        """
        fallback_data = {
            "source_topic": topic,
            "underlying_hook": referenced_hook,
            "target_argument": f"{chosen_statement} {chosen_argument}",
            "agent_executed": f"{self.agent_name} (Procedural Fallback Mode)",
            "storyboard_frames": [
                {
                    "frame_index": 1,
                    "timestamp_start": 0.0,
                    "timestamp_end": 3.0,
                    "spoken_voiceover": f"Listen very carefully to this secret about {topic}.",
                    "scenic_art_prompt": f"Dramatic extreme close up of character face, high contrast cel-shading, dark crimson glow, dark fog background.",
                    "camera_movement_mode": "Rapid push in zoom matching primary subject eye alignment.",
                    "audio_sync_trigger": "Muffled ambient frequencies, suddenly interrupted by a heavy dark phonk bass drop."
                },
                {
                    "frame_index": 2,
                    "timestamp_start": 3.0,
                    "timestamp_end": 6.5,
                    "spoken_voiceover": f"Mainstream analysis completely ignores the core variables involved in {topic}.",
                    "scenic_art_prompt": f"Splitscreen manga panel sequence, character silhouette, intense glowing energy sparks, detailed tech background.",
                    "camera_movement_mode": "Constant slow panning to the right on a horizontal axis.",
                    "audio_sync_trigger": "Constant rhythmic sidechain compressor kick pump with ticking hats."
                },
                {
                    "frame_index": 3,
                    "timestamp_start": 6.5,
                    "timestamp_end": 10.0,
                    "spoken_voiceover": f"When you study the raw mathematical parameters, the conventional stories crumble.",
                    "scenic_art_prompt": f"Atmospheric dark domain expansion sphere opening, fractured crystalline structures floating, stylized speed lines.",
                    "camera_movement_mode": "Rotational dolly zoom moving downwards into an abyss warp.",
                    "audio_sync_trigger": "Deep synthesizer sound effect riser, leading into high frequency snare roll patterns."
                },
                {
                    "frame_index": 4,
                    "timestamp_start": 10.0,
                    "timestamp_end": 13.5,
                    "spoken_voiceover": f"Now, you must decide if you will follow facts or comfortable lies.",
                    "scenic_art_prompt": f"Wide angle static camera, glowing anime character hand, dark dust clouds rising, hyper realistic lighting bloom.",
                    "camera_movement_mode": "Slow camera drift upwards with subtle lens wobble vibrations.",
                    "audio_sync_trigger": "Phonk melody fade out leaving behind sub-woofer bass vibration tones."
                }
            ]
        }
        self._save_to_workspace(fallback_data)
        return fallback_data

if __name__ == "__main__":
    storyboarder = VisualSyncStoryboarder()
    output = storyboarder.generate_storyboard()
    
    print("\n--- Z-NET CORE MODULE A: AGENT 03 STORYBOARD GENERATED ---")
    print(json.dumps(output, indent=4))
    print("----------------------------------------------------------")
