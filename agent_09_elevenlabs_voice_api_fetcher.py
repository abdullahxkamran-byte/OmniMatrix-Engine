import os
import sys
import json
import subprocess
import asyncio

# Manual .env loader utility
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

# Standardize Gemini Integration
try:
    import google.generativeai as genai
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False

# Import Edge-TTS for the ultimate free fallback
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# Import Gradio Client for Hugging Face RVC Model Access
try:
    from gradio_client import Client
    GRADIO_CLIENT_AVAILABLE = True
except ImportError:
    GRADIO_CLIENT_AVAILABLE = False


class AiAgent09HuggingFaceRVCVoiceGenerator:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 09: HuggingFace RVC Voice Generator"
        self.workspace_dir = workspace_dir
        self.audio_dir = os.path.join(self.workspace_dir, "audio_tracks")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.hf_token = os.environ.get("HF_TOKEN", None)
        
        if GEMINI_SDK_AVAILABLE and self.gemini_key:
            genai.configure(api_key=self.gemini_key)

        os.makedirs(self.audio_dir, exist_ok=True)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        """Loads the master OmniMatrix state."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run Agent 10 first.", "ERROR")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        """Saves the updated state back to OmniMatrix."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("Matrix state successfully updated with generated audio file paths.")

    def get_audio_duration(self, file_path):
        """Calculates exact duration using ffprobe for perfect Video synchronization."""
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries",
                 "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            return round(float(result.stdout.strip()), 2)
        except Exception:
            self.log("ffprobe not found. Using duration estimation fallback.", "WARNING")
            return 2.0 

    def perform_ai_voice_casting(self, characters_list):
        """Maps characters to Hugging Face Models and Edge-TTS voices."""
        if not (GEMINI_SDK_AVAILABLE and self.gemini_key):
            return self._offline_rule_based_casting(characters_list)

        self.log("Consulting AI Casting Director for free character mapping...", "STATUS")
        
        prompt = (
            f"You are the AI Voice Casting Director. Analyze these characters: {list(characters_list)}.\n"
            "We are using 100% free open-source audio. Provide a theoretical 'hf_rvc_model_id' (e.g., 'Gojo_English_v2') "
            "for Hugging Face Spaces, and an 'edge_tts_voice' for fallback.\n"
            "Return STRICTLY a JSON object:\n"
            "{\n"
            "  \"mappings\": {\n"
            "    \"CharacterName\": {\n"
            "      \"hf_rvc_model_id\": \"Gojo_Satoru_Dub\",\n"
            "      \"edge_tts_voice\": \"en-US-ChristopherNeural\"\n"
            "    }\n"
            "  }\n"
            "}"
        )

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text.strip()).get("mappings", {})
        except Exception as e:
            self.log(f"AI Casting failed: {str(e)}.", "ERROR")
            return self._offline_rule_based_casting(characters_list)

    def _offline_rule_based_casting(self, characters_list):
        """Hardcoded fallback for exact anime/movie mappings."""
        mappings = {}
        for char in characters_list:
            char_lower = char.lower()
            if "gojo" in char_lower:
                mappings[char] = {"hf_rvc_model_id": "Gojo_Eng_Dub", "edge_tts_voice": "en-US-GuyNeural"}
            elif "sukuna" in char_lower:
                mappings[char] = {"hf_rvc_model_id": "Sukuna_Eng_Dub", "edge_tts_voice": "en-GB-RyanNeural"}
            else:
                mappings[char] = {"hf_rvc_model_id": "Generic_Male", "edge_tts_voice": "en-US-ChristopherNeural"}
        return mappings

    def _fetch_huggingface_audio(self, text, output_path, hf_model_id):
        """
        Primary Engine: Contacts a Hugging Face Space running RVC via Gradio Client.
        Sends TAGGED text -> Gets exact character voice -> Saves MP3.
        """
        if not GRADIO_CLIENT_AVAILABLE:
            self.log("gradio_client not installed. Run: pip install gradio_client", "WARNING")
            return False

        self.log(f"Attempting Hugging Face Generation for: {hf_model_id}", "STATUS")
        
        try:
            # Note: "rvc-space/anime-tts" is a placeholder for a public RVC space on HF.
            # Replace with an active Gradio Space URL from Hugging Face that supports text-to-speech RVC.
            client = Client("rvc-space/anime-tts") 
            result = client.predict(
                text=text,
                model_name=hf_model_id,
                api_name="/predict"
            )
            
            temp_audio_path = result[0] if isinstance(result, list) else result
            
            with open(temp_audio_path, 'rb') as f_src, open(output_path, 'wb') as f_dst:
                f_dst.write(f_src.read())
                
            return True
        except Exception as e:
            self.log(f"Hugging Face API failed (Space might be asleep/busy): {str(e)}", "WARNING")
            return False

    def _fetch_edge_tts_fallback(self, text, output_path, voice_name):
        """Ultimate Free Failsafe: Microsoft Edge TTS."""
        if not EDGE_TTS_AVAILABLE:
            return False

        async def _generate():
            communicate = edge_tts.Communicate(text, voice_name)
            await communicate.save(output_path)
            
        try:
            asyncio.run(_generate())
            return True
        except Exception as e:
            self.log(f"Edge-TTS failed: {str(e)}", "ERROR")
            return False

    def process_script_audio(self):
        state = self._load_matrix_state()
        
        # NOTE: Now reading from module_b_audio because Agent 10 already created it!
        audio_module = state.get("module_b_audio", {})
        audio_timeline = audio_module.get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("No audio timeline found. Run Agent 10 first to map emotions!", "ERROR")
            return

        unique_characters = set(frame.get("character", "Narrator") for frame in audio_timeline)
        casting_map = self.perform_ai_voice_casting(unique_characters)

        for frame in audio_timeline:
            f_idx = frame.get("frame_index", 1)
            character = frame.get("character", "Narrator")
            
            # CORE LOGIC CHANGE: Read the TAGGED voiceover first. Fallback to spoken_voiceover.
            text = frame.get("tagged_voiceover", frame.get("spoken_voiceover", "")).strip()
            
            if not text:
                continue

            char_profile = casting_map.get(character, {})
            file_name = f"frame_{f_idx:03d}_{character.replace(' ', '_').lower()}.mp3"
            full_audio_path = os.path.join(self.audio_dir, file_name)
            
            success = False

            # Tier 1: Hugging Face (Free & High Quality Anime Voices)
            hf_model = char_profile.get("hf_rvc_model_id", "Generic")
            success = self._fetch_huggingface_audio(text, full_audio_path, hf_model)

            # Tier 2: Edge TTS Failsafe (If Hugging Face is down)
            if not success:
                edge_v = char_profile.get("edge_tts_voice", "en-US-ChristopherNeural")
                self.log(f"Falling back to Edge-TTS for Frame {f_idx} [{character}]")
                success = self._fetch_edge_tts_fallback(text, full_audio_path, edge_v)

            if success:
                duration = self.get_audio_duration(full_audio_path)
                self.log(f"Frame {f_idx} Audio Generated: {duration} seconds.")
                
                # Append audio data to the frame
                frame["audio_file_path"] = full_audio_path
                frame["audio_duration_seconds"] = duration

        # Update OmniMatrix State
        state["module_b_audio"]["audio_timeline"] = audio_timeline
        state["module_b_audio"]["voice_generation_status"] = "completed"
        
        self._save_matrix_state(state)
        self.log("Module B - Agent 09 processing complete. Audio files are ready.")

if __name__ == "__main__":
    fetcher = AiAgent09HuggingFaceRVCVoiceGenerator()
    fetcher.process_script_audio()
