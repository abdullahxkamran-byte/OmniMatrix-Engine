import os
import sys
import json
import re
import urllib.request
import urllib.parse

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

# Standardize Gemini Integration as per Registry Specs
try:
    import google.generativeai as genai
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False

# Import Edge-TTS library if available for advanced failsafe
try:
    import edge_tts
    import asyncio
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

class ElevenlabsVoiceApiFetcher:
    def __init__(self, workspace_dir="znet_workspace"):
        # Name matched with Z-Net Master Compendium Specification
        self.agent_name = "Agent 09: elevenlabs_voice_api_fetcher"
        self.workspace_dir = workspace_dir
        self.audio_dir = os.path.join(self.workspace_dir, "audio_tracks")
        
        # API Keys loading
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY", None)
        
        # Configure Gemini SDK directly if available
        if GEMINI_SDK_AVAILABLE and self.gemini_key:
            genai.configure(api_key=self.gemini_key)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_master_script(self):
        """Loads the final formatted master timeline script from Stage 8."""
        input_file_path = os.path.join(self.workspace_dir, "08_final_master_script.json")
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.log_message(f"Cannot read Stage 8 file: {str(e)}", "WARNING")

        self.log_message("Upstream script missing. Activating simulated anime duel script.", "ALERT")
        return {
            "source_topic": "Simulated Battle",
            "master_timeline": [
                {"frame_index": 1, "character": "Narrator", "spoken_voiceover": "The ultimate showdown begins now!"},
                {"frame_index": 2, "character": "Gojo", "spoken_voiceover": "Don't worry. I am literally the strongest."},
                {"frame_index": 3, "character": "Sukuna", "spoken_voiceover": "Foolish brat. I will rip your domain to shreds."}
            ]
        }

    def perform_ai_voice_casting(self, characters_list):
        """Uses Gemini SDK to dynamically map characters to ElevenLabs Voice IDs and Edge-TTS locales."""
        if not (GEMINI_SDK_AVAILABLE and self.gemini_key):
            self.log_message("Gemini SDK missing or key absent. Activating smart offline casting...", "WARNING")
            return self._offline_rule_based_casting(characters_list)

        self.log_message("Consulting Z-Net Gemini AI Casting Director...", "STATUS")
        
        prompt = (
            f"You are the Z-Net AI Voice Casting Director. Analyze these characters: {list(characters_list)}.\n"
            "Map each to the best ElevenLabs pre-made Voice ID (e.g., Rachel='21m00Tcm4TlvDq8ikWAM', Clyde='2EiwXgHQaoKC5u4vEe9b', "
            "Antoni='ERXwobaYiN019vkySvjV', Adam='pNInz6obpgmo512wG1ei', Nicole='piTKgcLEGmPEeToec5ms') "
            "and an Edge-TTS locale variant (like 'en-US-ChristopherNeural', 'en-GB-RyanNeural', 'en-AU-WilliamNeural').\n"
            "Return STRICTLY a JSON object with this exact structure, nothing else:\n"
            "{\n"
            "  \"voice_mappings\": {\n"
            "    \"CharacterName\": {\n"
            "      \"elevenlabs_voice_id\": \"pNInz6obpgmo512wG1ei\",\n"
            "      \"edge_tts_voice\": \"en-US-ChristopherNeural\",\n"
            "      \"description\": \"confident male tone\"\n"
            "    }\n"
            "  }\n"
            "}"
        )

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            raw_text = response.text.strip()
            casting_blueprint = json.loads(raw_text)
            return casting_blueprint.get("voice_mappings", {})
        except Exception as e:
            self.log_message(f"AI Casting failed: {str(e)}. Reverting to offline rule matrix.", "ERROR")
            return self._offline_rule_based_casting(characters_list)

    def _offline_rule_based_casting(self, characters_list):
        """Offline safety matrix to map typical anime archetypes to secure audio tracks."""
        mappings = {}
        for char in characters_list:
            char_lower = char.lower()
            if any(name in char_lower for name in ["gojo", "goku", "hero"]):
                mappings[char] = {
                    "elevenlabs_voice_id": "pNInz6obpgmo512wG1ei", # Adam
                    "edge_tts_voice": "en-GB-RyanNeural",
                    "description": "Charismatic Male Lead"
                }
            elif any(name in char_lower for name in ["sukuna", "madara", "villain"]):
                mappings[char] = {
                    "elevenlabs_voice_id": "2EiwXgHQaoKC5u4vEe9b", # Clyde
                    "edge_tts_voice": "en-AU-WilliamNeural",
                    "description": "Deep Raspy Antagonist"
                }
            elif any(name in char_lower for name in ["girl", "female", "sakura", "hinata"]):
                mappings[char] = {
                    "elevenlabs_voice_id": "21m00Tcm4TlvDq8ikWAM", # Rachel
                    "edge_tts_voice": "en-US-JennyNeural",
                    "description": "Soft Female Voice"
                }
            else:
                mappings[char] = {
                    "elevenlabs_voice_id": "ERXwobaYiN019vkySvjV", # Antoni
                    "edge_tts_voice": "en-US-ChristopherNeural",
                    "description": "Neutral Voiceover Narrator"
                }
        return mappings

    def _fetch_elevenlabs_audio(self, text, output_path, voice_id):
        """Synthesizes premium audio using ElevenLabs API endpoints."""
        if not self.elevenlabs_key:
            return False
            
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": self.elevenlabs_key,
            "Content-Type": "application/json",
            "accept": "audio/mpeg"
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
                return True
        except Exception as e:
            self.log_message(f"ElevenLabs generation failed for voice {voice_id}: {str(e)}", "WARNING")
            return False

    def _fetch_edge_tts_fallback(self, text, output_path, voice_name):
        """Asynchronous Failsafe: Generates voice using high-quality free Edge-TTS."""
        if not EDGE_TTS_AVAILABLE:
            # Low-tier HTTP translation scraper fallback if edge-tts library isn't globally active
            try:
                encoded_text = urllib.parse.quote(text)
                clean_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={encoded_text}"
                req = urllib.request.Request(clean_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=15) as response:
                    with open(output_path, "wb") as f:
                        f.write(response.read())
                return True
            except Exception:
                return False

        async def _generate():
            communicate = edge_tts.Communicate(text, voice_name)
            await communicate.save(output_path)
            return True

        try:
            asyncio.run(_generate())
            return True
        except Exception as e:
            self.log_message(f"Failsafe Edge-TTS layer failed: {str(e)}", "ERROR")
            return False

    def process_voiceovers(self):
        script_data = self._load_master_script()
        timeline = script_data.get("master_timeline", [])
        topic = script_data.get("source_topic", "Dynamic Production")

        unique_characters = set(frame.get("character", "Narrator") for frame in timeline)
        self.log_message(f"Detected script characters for casting: {unique_characters}")

        # Execute Dynamic Studio Casting Call
        voice_casting_map = self.perform_ai_voice_casting(unique_characters)
        audio_assets = []
        
        # Token Management: Count total script characters to proactively guard limits
        total_script_chars = sum(len(frame.get("spoken_voiceover", "")) for frame in timeline)
        self.log_message(f"Total script size: {total_script_chars} characters.", "INFO")

        # Force token protection failover if script is unsafely long for a free tier tier
        use_premium = self.elevenlabs_key is not None and total_script_chars < 5000

        for frame in timeline:
            f_idx = frame.get("frame_index", 1)
            character = frame.get("character", "Narrator")
            text = frame.get("spoken_voiceover", "").strip()
            
            if not text:
                continue

            # SAFEGUARD: Protect ElevenLabs quota limits from heavy/runaway scripts
            if len(text) > 300:
                text = text[:297] + "..."

            char_profile = voice_casting_map.get(character, {
                "elevenlabs_voice_id": "ERXwobaYiN019vkySvjV",
                "edge_tts_voice": "en-US-ChristopherNeural",
                "description": "Default Voice Profile"
            })

            file_name = f"voiceover_frame_{f_idx:02d}_{character.lower()}.mp3"
            full_audio_path = os.path.join(self.audio_dir, file_name)
            success = False

            if use_premium:
                v_id = char_profile.get("elevenlabs_voice_id", "ERXwobaYiN019vkySvjV")
                self.log_message(f"Frame {f_idx}: Processing [{character}] via ElevenLabs (ID: {v_id})")
                success = self._fetch_elevenlabs_audio(text, full_audio_path, v_id)
                
                if not success:
                    self.log_message(f"ElevenLabs Token Exhausted/Failed. Activating Free HF Edge-TTS Failsafe Guard.", "WARNING")
                    edge_v = char_profile.get("edge_tts_voice", "en-US-ChristopherNeural")
                    success = self._fetch_edge_tts_fallback(text, full_audio_path, edge_v)
            else:
                edge_v = char_profile.get("edge_tts_voice", "en-US-ChristopherNeural")
                self.log_message(f"Frame {f_idx}: Processing [{character}] via Failsafe Edge-TTS Mode ({edge_v})")
                success = self._fetch_edge_tts_fallback(text, full_audio_path, edge_v)

            if success:
                self.log_message(f"Saved synchronized track -> '{full_audio_path}'")
                audio_assets.append({
                    "frame_index": f_idx,
                    "character": character,
                    "audio_file": full_audio_path,
                    "casting_profile": char_profile,
                    "spoken_voiceover": text
                })
            else:
                self.log_message(f"Critical execution error on Frame {f_idx}.", "ERROR")

        output_metadata = {
            "source_topic": topic,
            "agent_executed": self.agent_name,
            "engine_mode": "ElevenLabs Premium Studio" if use_premium else "HF Edge-TTS Guard Active",
            "voice_casting_map": voice_casting_map,
            "total_tracks": len(audio_assets),
            "audio_tracks": audio_assets
        }

        output_path = os.path.join(self.workspace_dir, "09_vocal_audio_assets.json")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_metadata, f, indent=4)
            self.log_message(f"Dynamic voice manifest saved to '{output_path}'")
        except Exception as e:
            self.log_message(f"Failed to write audio track manifest: {str(e)}", "ERROR")

        return output_metadata

if __name__ == "__main__":
    fetcher = ElevenlabsVoiceApiFetcher()
    output = fetcher.process_voiceovers()
    print("\n--- Z-NET VOCAL MODULE B: AGENT 09 COMPLETE ---")
