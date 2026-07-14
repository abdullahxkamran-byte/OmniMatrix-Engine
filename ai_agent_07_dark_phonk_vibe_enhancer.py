import os
import re
import sys
import json
import urllib.request
import urllib.error

class DarkPhonkVibeEnhancer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 07: dark_phonk_vibe_enhancer"
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
        Attempts to read Stage 6 audited word guard scripts.
        If missing, tries to load Stage 4 tension timeline data.
        If both are missing, prompts user for topic input.
        """
        paths_to_try = [
            os.path.join(self.workspace_dir, "06_word_count_guard.json"),
            os.path.join(self.workspace_dir, "04_tension_peaks.json")
        ]

        for file_path in paths_to_try:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    print(f"[{self.agent_name}] Success: Loaded upstream state from '{file_path}'")
                    return data
                except Exception as e:
                    print(f"[{self.agent_name}] Warning: Cannot load '{file_path}' ({str(e)}). Trying next fallback.")

        print(f"[{self.agent_name}] Pipeline Gap: Active upstream timeline structures are missing.")
        user_input = input("Enter an anime character or aesthetic topic for Dark Phonk mapping: ").strip()
        if not user_input:
            print("[System Error] Empty target value. Halting engine.")
            sys.exit(1)

        return {
            "source_topic": user_input,
            "timeline_frames": [
                {
                    "frame_index": 1,
                    "optimized_voiceover": f"Unleash the ultimate dark power of {user_input}."
                }
            ]
        }

    def _clean_json_response(self, raw_text):
        """
        Extracts raw JSON boundaries from LLM text blocks to shield parser runtime.
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

    def _save_to_workspace(self, data, filename="07_dark_phonk_vibe.json"):
        """
        Saves the styled aesthetic configurations to the workspace directory.
        """
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Dark Phonk aesthetic config written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save state files: {str(e)}")
            return None

    def enhance_vibe(self):
        """
        Injects intense, aggressive dark phonk style parameters, camera metrics,
        and high-contrast neon visual styles into every frame sequence.
        """
        input_data = self._load_previous_stage()
        topic = input_data.get("source_topic", "Dark Phonk Theme")
        
        # Adapt keys based on whether Stage 6 or Stage 4 was successfully loaded
        frames = input_data.get("timeline_frames", input_data.get("tension_timeline", []))

        print(f"[{self.agent_name}] Injecting aggressive dark phonk styling aesthetics into: '{topic}'")

        system_prompt = (
            "You are a master of Phonk aesthetic style guidelines and dark cinematic editing. "
            "Your job is to read storyboard frames/text inputs and output synchronized dark phonk visual stylings.\n"
            "For each frame, generate styling elements under a list key named 'phonk_frames' with these exact parameters:\n"
            "- 'frame_index': matching integer representing the sequence flow.\n"
            "- 'visual_style_prompt': highly specific, visual description emphasizing extreme contrasts, "
            "heavy grain, dark shadows, and toxic neon accents (purple, blood red, emerald green, neon yellow).\n"
            "- 'color_palette_hex': a list of exactly three HEX color codes representing the dominant grading theme.\n"
            "- 'camera_shake_intensity': float scaling from 0.0 (calm cinematic float) to 1.5 (maximum extreme violent shockwave vibration).\n"
            "- 'bass_drop_sync': boolean (true if this frame represents a visual slam, impact, or high-vibe rhythm hit point).\n"
            "- 'ambient_glitch_rate': float from 0.0 to 1.0 mapping screen distortions, chromatic aberration, or signal loss.\n"
            "Format your output STRICTLY as a raw JSON object containing the key 'phonk_frames'. "
            "Do not write conversational intro notes, explanations, warnings, or markdown code blocks. Only raw JSON."
        )

        user_prompt = f"Phonk Theme Subject: {topic}\nInput Sequence Data:\n" + json.dumps(frames, indent=2)

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
                    "phonk_frames": structured_output.get("phonk_frames", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except urllib.error.URLError as e:
            print(f"[{self.agent_name}] Engine Connection Offline: Running local math-procedural Phonk generator.")
            return self._execute_procedural_fallback(topic, frames)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[{self.agent_name}] Schema Alignment Error: Executing clean safety Phonk styling fallback.")
            return self._execute_procedural_fallback(topic, frames)

    def _execute_procedural_fallback(self, topic, frames):
        """
        Procedural mathematical backup engine to generate dark aggressive styling 
        without network or model dependencies.
        """
        phonk_frames = []
        total = len(frames) if frames else 1

        for idx, frame in enumerate(frames):
            frame_idx = frame.get("frame_index", idx + 1)
            progression = (idx + 1) / total
            
            # Heavy Phonk style progression
            if progression < 0.3:
                visual_prompt = f"Deep shadows, heavy film grain, dark mist shrouding {topic}, cold ambient blue light."
                palette = ["#0d0d0d", "#1a1a1a", "#0055ff"]
                shake = 0.2
                bass = False
                glitch = 0.15
            elif progression < 0.7:
                visual_prompt = f"Extreme high contrast, glowing neon purple particles erupting around {topic}, aggressive backlighting."
                palette = ["#000000", "#7f00ff", "#ffffff"]
                shake = 0.8
                bass = True if idx % 2 == 0 else False
                glitch = 0.4
            else:
                # The Climax Vibe
                visual_prompt = f"Vandalized glitch aesthetics, blinding scarlet red glow, dark vignette, kinetic speed line impacts on {topic}."
                palette = ["#ff003c", "#000000", "#ffea00"]
                shake = 1.4
                bass = True
                glitch = 0.9

            phonk_frames.append({
                "frame_index": frame_idx,
                "visual_style_prompt": visual_prompt,
                "color_palette_hex": palette,
                "camera_shake_intensity": shake,
                "bass_drop_sync": bass,
                "ambient_glitch_rate": glitch
            })

        fallback_data = {
            "source_topic": topic,
            "agent_executed": f"{self.agent_name} (Procedural Fallback Mode)",
            "phonk_frames": phonk_frames
        }
        self._save_to_workspace(fallback_data)
        return fallback_data

if __name__ == "__main__":
    enhancer = DarkPhonkVibeEnhancer()
    output = enhancer.enhance_vibe()
    
    print("\n--- Z-NET CORE MODULE A: AGENT 07 DARK PHONK VIBE COMPLETED ---")
    print(json.dumps(output, indent=4))
    print("-----------------------------------------------------------------")
