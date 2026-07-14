import os
import re
import sys
import json
import urllib.request
import urllib.error

class AudioToneEmotionMatcher:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 10: audio_tone_emotion_matcher"
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
        Loads the generated voice tracks and metadata from Stage 9.
        Falls back to manual dynamic prompt if pipeline is unpopulated.
        """
        input_file_path = os.path.join(self.workspace_dir, "09_vocal_audio_assets.json")
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Stage 9 audio assets loaded from '{input_file_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: File read error ({str(e)}). Switching to manual override.")
        
        # Interactive fallback prompt if workspace upstream data is absent
        print(f"[{self.agent_name}] Pipeline Gap: Upstream audio track assets are missing.")
        user_input = input("Enter a dialogue line to map emotional audio coordinates: ").strip()
        if not user_input:
            print("[System Error] Empty target value. Halting execution.")
            sys.exit(1)
            
        return {
            "source_topic": "Manual Emotion Mapping",
            "audio_tracks": [
                {
                    "frame_index": 1,
                    "audio_file": "voiceover_frame_01.mp3",
                    "spoken_voiceover": user_input
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

    def _save_to_workspace(self, data, filename="10_audio_emotion_match.json"):
        """
        Saves the structured emotional tone metadata to the workspace directory.
        """
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Audio emotion matches saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save state files: {str(e)}")
            return None

    def match_emotions(self):
        """
        Analyzes spoken dialogues to assign precise emotional multipliers,
        pitch-shifting indexes, reverb intensities, and EQ settings for dark phonk synchronization.
        """
        input_data = self._load_previous_stage()
        topic = input_data.get("source_topic", "General Audio Target")
        tracks = input_data.get("audio_tracks", [])

        print(f"[{self.agent_name}] Analyzing script psychology and tone matrix for: '{topic}'")

        system_prompt = (
            "You are an expert sound designer and cinematic audio mixing engineer. "
            "Your job is to read voiceover scripts and match each frame sequence with high-end phonk sound design controls.\n"
            "Generate exactly 1 emotion match mapping for every frame inside a list named 'emotion_mappings'. "
            "Each item must have these exact parameters:\n"
            "- 'frame_index': integer representing the correct file sequence order.\n"
            "- 'audio_file': string matching the exact source voiceover file name.\n"
            "- 'tone_category': string describing the delivery style (choose only from: 'whisper-menace', 'screaming-rage', 'cold-assertive', 'hype-buildup', 'cosmic-vibration').\n"
            "- 'pitch_shift_semitones': integer representing shifting instructions (scale from -4 for ultra-deep demonic voice to +2 for excited high-pitched intensity).\n"
            "- 'delivery_speed_multiplier': float adjusting rate of play (scale from 0.90 for slow threat pace to 1.15 for super hyper speed style).\n"
            "- 'reverb_mix': float representing environment wetness (scale from 0.0 for dry vocals to 0.60 for deep echoing cavern style).\n"
            "- 'eq_preset': string indicating frequency boost (choose only from: 'heavy-bass-boost', 'radio-vocal-mid', 'crisp-air-treble').\n"
            "Format your response STRICTLY as a raw JSON object containing the list key 'emotion_mappings'. "
            "Do not include conversational notes, code blocks, or explanations. Only output raw JSON."
        )

        user_prompt = f"Target Vibe: Aggressive Dark Phonk\nScript Dialogues:\n" + json.dumps(tracks, indent=2)

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
                    "emotion_mappings": structured_output.get("emotion_mappings", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except urllib.error.URLError as e:
            print(f"[{self.agent_name}] Engine Connection Offline: Executing procedural audio-emotion generation.")
            return self._execute_procedural_fallback(topic, tracks)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[{self.agent_name}] Schema Alignment Error: Running clean procedural fallback styling.")
            return self._execute_procedural_fallback(topic, tracks)

    def _execute_procedural_fallback(self, topic, tracks):
        """
        Procedural sound staging engine to formulate complex audio metrics 
        for vocal processing layers in the offline absence of AI models.
        """
        mappings = []
        total = len(tracks) if tracks else 1

        for idx, track in enumerate(tracks):
            frame_idx = track.get("frame_index", idx + 1)
            file_name = track.get("audio_file", f"voiceover_frame_{frame_idx:02d}.mp3")
            progression = (idx + 1) / total

            # Establish structured procedural cinematic timeline transitions
            if progression < 0.3:
                tone = "whisper-menace"
                pitch = -2
                speed = 0.95
                reverb = 0.30
                eq = "radio-vocal-mid"
            elif progression < 0.7:
                tone = "cold-assertive"
                pitch = -1
                speed = 1.0
                reverb = 0.15
                eq = "crisp-air-treble"
            else:
                tone = "screaming-rage"
                pitch = -3  # Deep demonic growl vibe
                speed = 1.05
                reverb = 0.45
                eq = "heavy-bass-boost"

            mappings.append({
                "frame_index": frame_idx,
                "audio_file": file_name,
                "tone_category": tone,
                "pitch_shift_semitones": pitch,
                "delivery_speed_multiplier": speed,
                "reverb_mix": reverb,
                "eq_preset": eq
            })

        fallback_data = {
            "source_topic": topic,
            "agent_executed": f"{self.agent_name} (Procedural Fallback Mode)",
            "emotion_mappings": mappings
        }
        self._save_to_workspace(fallback_data)
        return fallback_data

if __name__ == "__main__":
    matcher = AudioToneEmotionMatcher()
    output = matcher.match_emotions()
    
    print("\n--- Z-NET VOCAL MODULE B: AGENT 10 AUDIO EMOTION COMPLETED ---")
    print(json.dumps(output, indent=4))
    print("----------------------------------------------------------------")
