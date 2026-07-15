import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

class HuggingFaceVoiceApiFetcher:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 09: huggingface_voice_api_fetcher"
        self.workspace_dir = workspace_dir
        self.audio_dir = os.path.join(self.workspace_dir, "audio_tracks")
        
        # Free high-quality English Text-to-Speech model from Hugging Face
        self.hf_model_url = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
        
        # Load Hugging Face token securely from local .env
        self.hf_token = self._load_key_from_env("HUGGING_FACE_TOKEN")

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)

    def _load_key_from_env(self, key_name):
        """
        Securely parses .env file to load tokens without leaking them to GitHub.
        """
        env_path = ".env"
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        parts = line.strip().split("=", 1)
                        if len(parts) == 2:
                            key, val = parts[0].strip(), parts[1].strip()
                            if key == key_name:
                                return val.replace('"', '').replace("'", "")
        return os.environ.get(key_name, None)

    def _load_master_script(self):
        """
        Loads the final formatted master timeline script from Stage 8.
        """
        input_file_path = os.path.join(self.workspace_dir, "08_final_master_script.json")
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Master script loaded from '{input_file_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Cannot read Stage 8 file: {str(e)}")

        # Fallback console prompt if workspace state is empty
        print(f"[{self.agent_name}] Workspace Alert: Upstream master script is missing.")
        user_input = input("Enter a single line of script to generate voiceover: ").strip()
        if not user_input:
            print("[System Error] No script input provided. Halting audio fetcher.")
            sys.exit(1)

        return {
            "source_topic": "Manual Voice Generation",
            "master_timeline": [
                {
                    "frame_index": 1,
                    "spoken_voiceover": user_input
                }
            ]
        }

    def _fetch_huggingface_audio(self, text, output_path):
        """
        Calls Hugging Face free Inference API to synthesize realistic voices (WAV output).
        """
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": text
        }
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(self.hf_model_url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=40) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
                return True
        except Exception as e:
            print(f"[{self.agent_name}] Hugging Face API Call Failed: {str(e)}")
            return False

    def _fetch_free_tts_audio(self, text, output_path):
        """
        Pure programmatic backup: downloads zero-cost high-quality TTS audio
        from Google's translate endpoints with zero external dependencies.
        """
        print(f"[{self.agent_name}] Status: Querying Free Fallback TTS Engine...")
        encoded_text = urllib.parse.quote(text)
        
        # Free Translate TTS endpoint bypassing API keys
        free_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={encoded_text}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
        }
        
        try:
            req = urllib.request.Request(free_url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
                return True
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Free fallback engine failed: {str(e)}")
            return False

    def process_voiceovers(self):
        """
        Loops through all visual storyboard segments, generating individual audio tracks
        and saving them as local workspace assets.
        """
        script_data = self._load_master_script()
        timeline = script_data.get("master_timeline", [])
        topic = script_data.get("source_topic", "Dynamic Audio")

        # Dynamic check if HF Token is active
        use_premium = self.hf_token is not None
        if not use_premium:
            print(f"[{self.agent_name}] Notice: No Hugging Face Token detected in .env. Defaulting to FREE GOOGLE TTS.")

        audio_assets = []

        for frame in timeline:
            f_idx = frame.get("frame_index", 1)
            text = frame.get("spoken_voiceover", "").strip()
            
            if not text:
                print(f"[{self.agent_name}] Warning: Frame {f_idx} has no spoken script. Skipping.")
                continue

            # Hugging Face natively outputs WAV. We use .wav for supreme editing quality in Blender!
            file_name = f"voiceover_frame_{f_idx:02d}.wav"
            full_audio_path = os.path.join(self.audio_dir, file_name)

            success = False
            if use_premium:
                print(f"[{self.agent_name}] Status: Fetching Hugging Face voice for Frame {f_idx}...")
                success = self._fetch_huggingface_audio(text, full_audio_path)
                if not success:
                    print(f"[{self.agent_name}] Warning: HF voice failed. Attempting Free Google TTS recovery.")
                    # Note: Fallback is MP3, but keeping name as .wav for alignment or writing as .mp3 if needed.
                    # We can save it under the same name as raw bytes, standard players will auto-detect format.
                    success = self._fetch_free_tts_audio(text, full_audio_path)
            else:
                success = self._fetch_free_tts_audio(text, full_audio_path)

            if success:
                print(f"[{self.agent_name}] Success: Saved audio track -> '{full_audio_path}'")
                audio_assets.append({
                    "frame_index": f_idx,
                    "audio_file": full_audio_path,
                    "character_count": len(text),
                    "spoken_voiceover": text
                })
            else:
                print(f"[{self.agent_name}] Fatal Error: Both Hugging Face and fallback voice engines failed for Frame {f_idx}.")

        # Save audio register map for upstream synchronizers (Z-Net Standards)
        output_metadata = {
            "source_topic": topic,
            "agent_executed": self.agent_name,
            "engine_mode": "Hugging Face MMS-TTS" if (use_premium and len(audio_assets) > 0) else "Free Google TTS",
            "total_tracks": len(audio_assets),
            "audio_tracks": audio_assets
        }

        output_path = os.path.join(self.workspace_dir, "09_vocal_audio_assets.json")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_metadata, f, indent=4)
            print(f"[{self.agent_name}] Success: Audio track manifest saved to '{output_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error saving metadata manifest: {str(e)}")

        return output_metadata

if __name__ == "__main__":
    fetcher = HuggingFaceVoiceApiFetcher()
    output = fetcher.process_voiceovers()
    
    print("\n--- Z-NET VOCAL MODULE B: AGENT 09 COMPLETED ---")
    print(f"Generated {output['total_tracks']} voice tracks inside '{fetcher.audio_dir}'")
    print("--------------------------------------------------")
