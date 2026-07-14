import os
import re
import sys
import json
import urllib.request
import urllib.error

class NarrativeTensionPeaksAnalyzer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 04: narrative_tension_peaks_analyzer"
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
        Dynamically imports structural states from stage 3. If missing, 
        prompts the user to declare a topic and runs a universal emergency generator.
        """
        input_file_path = os.path.join(self.workspace_dir, "03_visual_storyboard.json")
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Stage 3 storyboard state imported from '{input_file_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: File read error ({str(e)}). Switching to prompt bypass.")
        
        # Interactive fallback prompt if workspace upstream data is absent
        print(f"[{self.agent_name}] Pipeline Gap: Upstream storyboard file is missing.")
        user_input = input("Enter any topic to execute tension peaks mapping: ").strip()
        if not user_input:
            print("[System Error] Empty topic value. Halting execution.")
            sys.exit(1)
            
        return {
            "source_topic": user_input,
            "storyboard_frames": [
                {
                    "frame_index": 1,
                    "spoken_voiceover": f"Do not ignore this universal warning about {user_input}.",
                    "scenic_art_prompt": f"Dynamic silhouette standing in front of cosmic distortion."
                }
            ]
        }

    def _clean_json_response(self, raw_text):
        """
        Strips backticks, markdown markers, and extraneous symbols to isolate raw JSON.
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

    def _save_to_workspace(self, data, filename="04_tension_peaks.json"):
        """
        Persists the final processed tension timeline JSON inside the Z-Net workspace folder.
        """
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Tension peak configuration written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save state files: {str(e)}")
            return None

    def analyze_tension(self):
        """
        Processes voiceovers and visual cues to compute dynamic keyframes for typography,
        editing pacing, audio compression, and color shifts.
        """
        input_data = self._load_previous_stage()
        topic = input_data.get("source_topic", "Dynamic Target")
        frames = input_data.get("storyboard_frames", [])

        print(f"[{self.agent_name}] Mapping visual and auditory stress curves for: '{topic}'")

        system_prompt = (
            "You are an expert anime sound director and cinematic editor. "
            "Your job is to read a video storyboard and output a precise, synchronized list of dynamic tension curves.\n"
            "Analyze each frame and provide the following variables strictly mapped inside a list named 'tension_timeline':\n"
            "- 'frame_index': matching integer representing the frame order.\n"
            "- 'tension_score': integer from 1 (calm/whisper) to 10 (intense climax/explosive screen shake).\n"
            "- 'pacing_instruction': string detailing editing cut rate (e.g., 'slow-hold', 'double-time-cuts', 'glitch-jump').\n"
            "- 'highlight_keywords': list of strings of exactly 1-3 highly critical words in the voiceover that should be styled with explosive kinetic scaling.\n"
            "- 'vfx_color_shift': color styling recommendation (e.g., 'crimson-saturation', 'monochrome-glitch', 'high-contrast-gold').\n"
            "- 'audio_attenuation_db': integer representing dynamic volume level adjustments (e.g., -3 for voice clearance, +4 for peak bass blast).\n"
            "Format your output STRICTLY as a raw JSON object with the key 'tension_timeline'. "
            "Do not output markdown code formatting wrapper tags, introductory chat, or conversational notes. Only valid JSON."
        )

        user_prompt = f"Storyboard Target: {topic}\nFrames Data:\n" + json.dumps(frames, indent=2)

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
                    "tension_timeline": structured_output.get("tension_timeline", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except urllib.error.URLError as e:
            print(f"[{self.agent_name}] Engine Connection Offline: Executing procedural tension calculation module.")
            return self._execute_procedural_fallback(topic, frames)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[{self.agent_name}] Schema Alignment Error: Executing clean mathematical peak fallback mapping.")
            return self._execute_procedural_fallback(topic, frames)

    def _execute_procedural_fallback(self, topic, frames):
        """
        Calculates mathematical, context-relative tension curves dynamically 
        for any arbitrary list of frames when API nodes fail.
        """
        timeline = []
        # Calculate dynamic tension curve over the array size
        total_frames = len(frames) if frames else 1
        
        for idx, frame in enumerate(frames):
            frame_idx = frame.get("frame_index", idx + 1)
            # Procedural tension ramp formula: curve builds up towards the climax frame
            progression = (idx + 1) / total_frames
            tension_calc = int(2 + (progression * 7.5)) # Dynamic ramp between 2 and 10
            
            voiceover = frame.get("spoken_voiceover", "Warning detected.")
            words = [w.strip(".,!?\"'") for w in voiceover.split() if len(w) > 4]
            highlights = words[:2] if words else ["Warning"]

            if tension_calc < 5:
                pacing = "slow-hold"
                color = "desaturated-grey"
                db = -2
            elif tension_calc < 8:
                pacing = "dynamic-jump"
                color = "high-contrast-gold"
                db = 0
            else:
                pacing = "climax-glitch"
                color = "crimson-saturation"
                db = 4

            timeline.append({
                "frame_index": frame_idx,
                "tension_score": min(tension_calc, 10),
                "pacing_instruction": pacing,
                "highlight_keywords": highlights,
                "vfx_color_shift": color,
                "audio_attenuation_db": db
            })

        fallback_data = {
            "source_topic": topic,
            "agent_executed": f"{self.agent_name} (Procedural Fallback Mode)",
            "tension_timeline": timeline
        }
        self._save_to_workspace(fallback_data)
        return fallback_data

if __name__ == "__main__":
    analyzer = NarrativeTensionPeaksAnalyzer()
    output = analyzer.analyze_tension()
    
    print("\n--- Z-NET CORE MODULE A: AGENT 04 TENSION CURVE COMPLETED ---")
    print(json.dumps(output, indent=4))
    print("-------------------------------------------------------------")
