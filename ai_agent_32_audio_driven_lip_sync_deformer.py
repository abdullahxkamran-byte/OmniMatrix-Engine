import os
import re
import sys
import json
import urllib.request
import urllib.error

class AudioDrivenLipSyncDeformer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 32: audio_driven_lip_sync_deformer"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_dialogue(self):
        # Storyboard se text dialogue aur duration cues load karta hai sync karne ke liye
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        dialogue_tracks = []

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    dialogue = panel.get("dialogue_text", "")
                    if dialogue and dialogue.lower() != "none":
                        dialogue_tracks.append({
                            "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                            "duration_sec": 2.5, # Default segment length
                            "dialogue_text": dialogue,
                            "character_id": panel.get("active_character", "char_generic")
                        })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream storyboard dialogue load warning: {str(e)}")

        # Fallback dialogue agar upstream missing ho
        if not dialogue_tracks:
            print(f"[{self.agent_name}] Workspace Alert: No dialogue tracks found. Injecting default voice acting script.")
            dialogue_tracks = [
                {
                    "timestamp_sec": 0.5,
                    "duration_sec": 2.0,
                    "dialogue_text": "Ryoiki Tenkai: Muryokoosho!",
                    "character_id": "char_001" # Gojo's legendary line
                },
                {
                    "timestamp_sec": 3.5,
                    "duration_sec": 1.8,
                    "dialogue_text": "Chidori!",
                    "character_id": "char_002"
                }
            ]

        return dialogue_tracks

    def _clean_json_response(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def _save_to_workspace(self, data, filename="32_audio_lipsync_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Lip sync keyframes saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save lipsync data: {str(e)}")
            return None

    def generate_lip_sync_deformation(self):
        dialogue_tracks = self._load_upstream_dialogue()
        print(f"[{self.agent_name}] Lip-Sync Deformer active. Phoneme decomposition and blendshape tracking in progress...")

        system_prompt = (
            "You are a master Technical Animator specialized in 3D anime facial animation and blendshape mapping.\n"
            "Your job is to translate textual dialogue into frame-by-frame viseme values for a 3D mesh.\n"
            "Visemes should use standard facial shape key controllers: 'viseme_A_O' (mouth wide/open), 'viseme_E_I' (mouth corners stretched), "
            "'viseme_U' (rounded lips), and 'viseme_B_M_P' (lips tightly sealed/closed).\n"
            "For each dialogue segment, split the duration into 3 keyframe intervals and output them in a list named 'lip_sync_sequences' with:\n"
            "- 'timestamp_sec': float indicating precise frame timing.\n"
            "- 'character_id': string linking to the target head mesh.\n"
            "- 'active_syllable': string showing the raw syllable being spoken (e.g. 'Ryo', 'Ten', 'Kai').\n"
            "- 'shape_key_weights': object containing float weights from 0.0 (inactive) to 1.0 (fully active):\n"
            "    - 'viseme_A_O': float\n"
            "    - 'viseme_E_I': float\n"
            "    - 'viseme_U': float\n"
            "    - 'viseme_B_M_P': float\n"
            "- 'jaw_open_angle': float (rotation in degrees for the jaw bone; range 0.0 to 15.0).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'lip_sync_sequences'. "
            "Do not write conversational text, markdown blocks, or backticks. Return pure JSON only."
        )

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
                    {"role": "user", "content": f"Audio Dialogue Script:\n{json.dumps(dialogue_tracks, indent=2)}"}
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
                    {"role": "user", "content": f"Audio Dialogue Script:\n{json.dumps(dialogue_tracks, indent=2)}"}
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
                    "agent_executed": self.agent_name,
                    "lip_sync_sequences": structured_output.get("lip_sync_sequences", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Initializing procedural phoneme fallback engine.")
            return self._execute_procedural_fallback(dialogue_tracks)

    def _execute_procedural_fallback(self, dialogue_tracks):
        # Algorithmic syllable matching based on word vowels for stylized lip sync
        sequences = []
        for track in dialogue_tracks:
            start_ts = float(track.get("timestamp_sec", 0.0))
            duration = float(track.get("duration_sec", 2.0))
            cid = track.get("character_id", "char_generic")
            text = str(track.get("dialogue_text", "")).lower()

            # Clean and split words into basic syllable-like parts
            words = text.split()
            if not words:
                words = ["ah"]

            steps = len(words) * 2
            step_duration = duration / max(steps, 1)

            for step in range(steps):
                ts = start_ts + (step * step_duration)
                current_word = words[step % len(words)]
                
                # Check dominant vowel sounds in the word segment to map shape-key weights
                if any(v in current_word for v in ["a", "o"]):
                    syllable = "A/O Open"
                    weights = {"viseme_A_O": 0.85, "viseme_E_I": 0.1, "viseme_U": 0.0, "viseme_B_M_P": 0.0}
                    jaw = 12.0
                elif any(v in current_word for v in ["e", "i"]):
                    syllable = "E/I Stretch"
                    weights = {"viseme_A_O": 0.2, "viseme_E_I": 0.9, "viseme_U": 0.0, "viseme_B_M_P": 0.0}
                    jaw = 6.0
                elif any(v in current_word for v in ["u", "w"]):
                    syllable = "U Pucker"
                    weights = {"viseme_A_O": 0.1, "viseme_E_I": 0.0, "viseme_U": 0.95, "viseme_B_M_P": 0.0}
                    jaw = 4.5
                elif any(v in current_word for v in ["b", "m", "p"]):
                    syllable = "BMP Closed"
                    weights = {"viseme_A_O": 0.0, "viseme_E_I": 0.0, "viseme_U": 0.0, "viseme_B_M_P": 1.0}
                    jaw = 0.0
                else:
                    syllable = "Neutral Rest"
                    weights = {"viseme_A_O": 0.0, "viseme_E_I": 0.0, "viseme_U": 0.0, "viseme_B_M_P": 0.0}
                    jaw = 0.0

                sequences.append({
                    "timestamp_sec": round(ts, 3),
                    "character_id": cid,
                    "active_syllable": syllable,
                    "shape_key_weights": weights,
                    "jaw_open_angle": jaw
                })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Phoneme Fallback)",
            "lip_sync_sequences": sequences
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    deformer = AudioDrivenLipSyncDeformer()
    output = deformer.generate_lip_sync_deformation()
    
    print("\n--- Z-NET ANIMATION ENGINE: AGENT 32 LIP SYNC DEFORMER COMPLETE ---")
    print(f"Total dynamic lip-sync keyframes designed: {len(output['lip_sync_sequences'])}")
    if output["lip_sync_sequences"]:
        sample = output["lip_sync_sequences"][0]
        print(f"Sync Target Character: '{sample['character_id']}' at Time: {sample['timestamp_sec']}s")
        print(f"Phoneme state: {sample['active_syllable']} | Jaw Angle: {sample['jaw_open_angle']} deg")
        print(f"Mapped weights -> A_O: {sample['shape_key_weights']['viseme_A_O']} | B_M_P: {sample['shape_key_weights']['viseme_B_M_P']}")
    print("------------------------------------------------------------------")
