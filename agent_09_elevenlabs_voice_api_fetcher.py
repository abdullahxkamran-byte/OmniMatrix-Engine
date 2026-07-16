import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error

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

class DynamicVoiceAiAgent:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 09: dynamic_voice_ai_agent"
        self.workspace_dir = workspace_dir
        self.audio_dir = os.path.join(self.workspace_dir, "audio_tracks")
        
        # Cloud AI Config (Gemini for Dynamic Voice Casting)
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        # Hugging Face Config
        self.hf_token = os.environ.get("HF_TOKEN", None)
        self.default_hf_model = "facebook/mms-tts-eng"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)

    def _load_master_script(self):
        """Loads the final formatted master timeline script from Stage 8."""
        input_file_path = os.path.join(self.workspace_dir, "08_final_master_script.json")
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Master script loaded from '{input_file_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Cannot read Stage 8 file: {str(e)}")

        # Safe programmatic anime script fallback if empty
        print(f"[{self.agent_name}] Workspace Alert: Upstream script missing. Generating simulated anime duel script.")
        return {
            "source_topic": "Simulated Battle",
            "master_timeline": [
                {
                    "frame_index": 1,
                    "character": "Narrator",
                    "spoken_voiceover": "The ultimate showdown of the century begins now!"
                },
                {
                    "frame_index": 2,
                    "character": "Gojo",
                    "spoken_voiceover": "Don't worry. I am literally the strongest."
                },
                {
                    "frame_index": 3,
                    "character": "Sukuna",
                    "spoken_voiceover": "Foolish brat. I will rip your domain to shreds."
                }
            ]
        }

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

    def perform_ai_voice_casting(self, characters_list):
        """
        Uses Gemini to dynamically design a voice casting map for any characters 
        found in the script. Eliminates all hardcoding.
        """
        if not self.gemini_key:
            print(f"[{self.agent_name}] Warning: No GEMINI_API_KEY. Activating smart offline rule casting...")
            return self._offline_rule_based_casting(characters_list)

        print(f"[{self.agent_name}] Status: Consulting Z-Net Gemini AI Casting Director...")
        
        system_prompt = (
            "You are the Z-Net AI Voice Casting Director.\n"
            "Your job is to design dynamic voice configuration maps for unique characters in a video script.\n"
            "For each character name provided, analyze who they are (especially anime characters like Gojo, Sukuna, Naruto, Sasuke, Goku, etc.).\n"
            "Map them to the best acoustic styles. Provide your output strictly as a RAW JSON object with the following structure:\n"
            "{\n"
            "  \"voice_mappings\": {\n"
            "    \"Gojo\": {\n"
            "      \"hf_model\": \"facebook/mms-tts-eng\",\n"
            "      \"google_locale\": \"en-gb\",\n"
            "      \"pitch_accent\": \"charismatic, confident male, slow-paced\"\n"
            "    },\n"
            "    \"Sukuna\": {\n"
            "      \"hf_model\": \"facebook/mms-tts-eng\",\n"
            "      \"google_locale\": \"en-au\",\n"
            "      \"pitch_accent\": \"deep, evil demonic male, rough tone\"\n"
            "    }\n"
            "  }\n"
            "}\n"
            "Rules:\n"
            "- Use 'en-us' for standard voices, 'en-gb' for deep/refined voices, 'en-au' for rough/raspy voices, and 'en-in' for softer voices.\n"
            "- Do not include markdown formatting or backticks."
        )

        user_content = f"Characters to cast voices for: {list(characters_list)}"
        
        url = f"{self.gemini_url}?key={self.gemini_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{system_prompt}\n\nInput Characters:\n{user_content}"
                }]
            }],
            "generationConfig": {"responseMimeType": "application/json"}
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                result = response.read().decode("utf-8")
                response_json = json.loads(result)
                raw_ai_message = response_json["candidates"][0]["content"]["parts"][0]["text"]
                cleaned_message = self._clean_json_response(raw_ai_message)
                casting_blueprint = json.loads(cleaned_message)
                
                print(f"[{self.agent_name}] Success: AI Dynamic Casting completed!")
                return casting_blueprint.get("voice_mappings", {})
        except Exception as e:
            print(f"[{self.agent_name}] AI Casting failed: {str(e)}. Reverting to smart offline casting...")
            return self._offline_rule_based_casting(characters_list)

    def _offline_rule_based_casting(self, characters_list):
        """Offline backup parser that matches anime names to dynamic audio profiles."""
        mappings = {}
        for char in characters_list:
            char_lower = char.lower()
            if any(name in char_lower for name in ["gojo", "goku", "sasuke", "hero"]):
                mappings[char] = {
                    "hf_model": "facebook/mms-tts-eng",
                    "google_locale": "en-gb",
                    "pitch_accent": "charismatic hero male"
                }
            elif any(name in char_lower for name in ["sukuna", "madara", "villain", "monster"]):
                mappings[char] = {
                    "hf_model": "facebook/mms-tts-eng",
                    "google_locale": "en-au",
                    "pitch_accent": "deep rough demonic male"
                }
            elif any(name in char_lower for name in ["hinata", "girl", "female", "sakura"]):
                mappings[char] = {
                    "hf_model": "facebook/mms-tts-eng",
                    "google_locale": "en-us",
                    "pitch_accent": "soft feminine voice"
                }
            else:
                # Standard default Narrator accent
                mappings[char] = {
                    "hf_model": "facebook/mms-tts-eng",
                    "google_locale": "en-us",
                    "pitch_accent": "neutral narrator voice"
                }
        return mappings

    def _fetch_huggingface_audio(self, text, output_path, hf_model):
        """Calls dynamic Hugging Face Model to synthesize character voice."""
        url = f"[https://api-inference.huggingface.co/models/](https://api-inference.huggingface.co/models/){hf_model}"
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": text}
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=40) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
                return True
        except Exception as e:
            print(f"[{self.agent_name}] HF Model '{hf_model}' failed: {str(e)}")
            return False

    def _fetch_free_tts_audio(self, text, output_path, locale):
        """Fetches voice from Google translate with dynamically selected regional accents."""
        encoded_text = urllib.parse.quote(text)
        free_url = f"[https://translate.google.com/translate_tts?ie=UTF-8&tl=](https://translate.google.com/translate_tts?ie=UTF-8&tl=){locale}&client=tw-ob&q={encoded_text}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            req = urllib.request.Request(free_url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
                return True
        except Exception as e:
            print(f"[{self.agent_name}] Google Fallback ({locale}) failed: {str(e)}")
            return False

    def process_voiceovers(self):
        script_data = self._load_master_script()
        timeline = script_data.get("master_timeline", [])
        topic = script_data.get("source_topic", "Dynamic Audio")

        # Extract unique characters from script dynamically
        unique_characters = set(frame.get("character", "Narrator") for frame in timeline)
        print(f"[{self.agent_name}] Detected characters for casting: {unique_characters}")

        # Execute AI Casting Call
        voice_casting_map = self.perform_ai_voice_casting(unique_characters)

        audio_assets = []
        use_premium = self.hf_token is not None

        for frame in timeline:
            f_idx = frame.get("frame_index", 1)
            character = frame.get("character", "Narrator")
            text = frame.get("spoken_voiceover", "").strip()
            
            if not text:
                continue

            # SAFEGUARD: Word Cap (consistent with Z-Net limitations)
            if len(text) > 300:
                text = text[:297] + "..."

            # Get dynamic casting profile for this frame's character
            char_profile = voice_casting_map.get(character, {
                "hf_model": self.default_hf_model,
                "google_locale": "en-us",
                "pitch_accent": "default narrator voice"
            })

            # Use different extension based on active engine to prevent file corruption
            ext = ".wav" if use_premium else ".mp3"
            file_name = f"voiceover_frame_{f_idx:02d}_{character.lower()}{ext}"
            full_audio_path = os.path.join(self.audio_dir, file_name)

            success = False
            if use_premium:
                hf_model = char_profile.get("hf_model", self.default_hf_model)
                print(f"[{self.agent_name}] Frame {f_idx}: Generating [{character}] using HF Model '{hf_model}' ({char_profile['pitch_accent']})")
                success = self._fetch_huggingface_audio(text, full_audio_path, hf_model)
                if not success:
                    print(f"[{self.agent_name}] Warning: HF failed. Recovering with localized Free Google TTS.")
                    fallback_file_name = f"voiceover_frame_{f_idx:02d}_{character.lower()}.mp3"
                    full_audio_path = os.path.join(self.audio_dir, fallback_file_name)
                    success = self._fetch_free_tts_audio(text, full_audio_path, char_profile.get("google_locale", "en-us"))
            else:
                locale = char_profile.get("google_locale", "en-us")
                print(f"[{self.agent_name}] Frame {f_idx}: Generating [{character}] using Fallback Locale '{locale}' ({char_profile['pitch_accent']})")
                success = self._fetch_free_tts_audio(text, full_audio_path, locale)

            if success:
                print(f"[{self.agent_name}] Success: Saved track -> '{full_audio_path}'")
                audio_assets.append({
                    "frame_index": f_idx,
                    "character": character,
                    "audio_file": full_audio_path,
                    "casting_profile": char_profile,
                    "spoken_voiceover": text
                })
            else:
                print(f"[{self.agent_name}] Fatal Error: Voice pipeline completely failed for Frame {f_idx}.")

        output_metadata = {
            "source_topic": topic,
            "agent_executed": self.agent_name,
            "engine_mode": "Hugging Face Cloud Multi-Model" if use_premium else "Free Regional Google TTS",
            "voice_casting_map": voice_casting_map,
            "total_tracks": len(audio_assets),
            "audio_tracks": audio_assets
        }

        output_path = os.path.join(self.workspace_dir, "09_vocal_audio_assets.json")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_metadata, f, indent=4)
            print(f"[{self.agent_name}] Success: Dynamic audio track manifest saved to '{output_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error saving metadata manifest: {str(e)}")

        return output_metadata

if __name__ == "__main__":
    fetcher = DynamicVoiceAiAgent()
    output = fetcher.process_voiceovers()
    print("\n--- Z-NET VOCAL MODULE B: AGENT 09 COMPLETE ---")
