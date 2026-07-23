import os
import sys
import json
import re
import urllib.request
import urllib.parse
import time
import wave
import math
import struct
import random

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
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Import Gradio Client for Hugging Face MusicGen Access
try:
    from gradio_client import Client
    GRADIO_CLIENT_AVAILABLE = True
except ImportError:
    GRADIO_CLIENT_AVAILABLE = False


class AiAgent18_5NeuralOstMusicComposer:
    def __init__(self):
        self.agent_name = "Ai_Agent_18_5"
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.audio_dir = os.path.join(self.workspace_dir, "Exports", "OST_Tracks")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

        # Idempotent Workspace Creation
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)

        self.ollama_url = "http://localhost:11434/api/generate"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)
        self.hf_token = os.environ.get("HF_TOKEN", None)

        if GEMINI_AVAILABLE and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run upstream modules first.", "FATAL")
            sys.exit(1)
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.log(f"JSON Corruption detected: {e}", "FATAL")
            sys.exit(1)

    def _save_matrix_state(self, state_data):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4, ensure_ascii=False)
        self.log("OmniMatrix state successfully updated with Custom Neural OSTs.", "SUCCESS")

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

    def _scrub_old_ost_tracks(self):
        """Idempotency Rule: Cleans previous OST generations to prevent bloat."""
        for filename in os.listdir(self.audio_dir):
            file_path = os.path.join(self.audio_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                self.log(f"Failed to delete {file_path}. Reason: {e}", "WARNING")

    def generate_music_prompts_ai(self, bgm_segments, target_bpm, video_format, global_theme):
        """LIMITLESS AI CORE: Designs descriptive prompts for any imaginable genre."""
        system_prompt = (
            "You are an elite music composer and prompt engineer for AI Music Generation models. "
            f"The video format is '{video_format}' and the overarching theme is '{global_theme}'.\n"
            "Analyze the BGM segments and convert them into highly descriptive, instrument-rich text prompts.\n"
            "DO NOT LIMIT YOURSELF. Invent detailed musical soundscapes matching the exact vibe.\n"
            "Return STRICTLY a JSON object containing a list named 'ost_prompts'.\n"
            "Each prompt object must contain:\n"
            "- 'segment_index': integer matching the list order.\n"
            "- 'start_sec': float.\n"
            "- 'end_sec': float.\n"
            "- 'music_prompt': string (Detailed text for the AI. Include instruments, vibe, tempo. e.g., '1980s synthwave drive with arpeggiated bass, gated snare, neon cyberpunk atmosphere').\n"
            "- 'duration_needed_sec': float (Calculate end_sec - start_sec, minimum 10.0 seconds).\n"
        )
        
        user_prompt = f"Base Tempo: {target_bpm} BPM\nBGM Segments Automation Map:\n{json.dumps(bgm_segments, indent=2)}"

        # CORE 1: Gemini
        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for Limitless OST Prompt Architecture...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("ost_prompts", [])
            except Exception as e:
                self.log(f"Gemini Engine failed: {e}. Switching to OpenAI fallback.", "WARNING")

        # CORE 2: OpenAI
        if self.openai_api_key:
            self.log(f"Routing to Core 2: OpenAI API [{self.model_cloud}]...")
            url = self.openai_url
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"}
            payload = {
                "model": self.model_cloud,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "response_format": {"type": "json_object"}
            }
            try:
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    raw_text = res_data["choices"][0]["message"]["content"]
                    return json.loads(self._clean_json_response(raw_text)).get("ost_prompts", [])
            except Exception as e:
                self.log(f"OpenAI Engine failed: {e}. Engaging Ollama Local Core.", "WARNING")

        # CORE 3: Ollama (Local Engine)
        self.log(f"Routing to Core 3: Local Ollama [{self.model_local}]...", "STATUS")
        try:
            payload = {
                "model": self.model_local,
                "prompt": system_prompt + "\n\n" + user_prompt,
                "stream": False,
                "format": "json"
            }
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                raw_text = res_data.get("response", "")
                return json.loads(self._clean_json_response(raw_text)).get("ost_prompts", [])
        except Exception as e:
            self.log(f"Ollama Engine failed: {e}. Engaging Procedural Math Fallback.", "WARNING")

        # CORE 4: Procedural Fallback
        self.log("All AI API Cores failed. Using procedural fallback prompts.", "STATUS")
        return self._execute_procedural_fallback(bgm_segments, global_theme)

    def _execute_procedural_fallback(self, segments, global_theme):
        prompts = []
        for idx, seg in enumerate(segments):
            style = str(seg.get("bgm_vibe_style", "dark-ambient")).lower()
            dur = max((seg.get("end_sec", 15.0) - seg.get("start_sec", 0.0)), 10.0)
            
            prompt_text = f"Generative background track for {global_theme}. Style focuses on {style}. "
            if "aggressive" in style or "phonk" in style:
                prompt_text += "Heavy bass rhythm, fast tempo, dark aggressive tone."
            else:
                prompt_text += "Smooth cinematic ambient pad, low tempo, deep atmosphere."
                
            prompts.append({
                "segment_index": idx,
                "start_sec": seg.get("start_sec", 0.0),
                "end_sec": seg.get("end_sec", dur),
                "music_prompt": prompt_text,
                "duration_needed_sec": dur,
                "vibe_style_ref": style
            })
        return prompts

    def _generate_music_huggingface(self, text_prompt, duration, output_path):
        """Attempts to contact Hugging Face MusicGen via Gradio."""
        if not GRADIO_CLIENT_AVAILABLE:
            self.log("gradio_client not installed. Skipping direct HuggingFace generation.", "WARNING")
            return False
        
        self.log(f"Contacting Neural Engine for: '{text_prompt[:40]}...' (Dur: {duration}s)", "STATUS")
        try:
            client = Client("facebook/MusicGen") 
            result = client.predict(
                text_prompt,
                "none", 
                duration, 
                api_name="/predict"
            )
            
            temp_audio_path = result[1] if isinstance(result, tuple) else result
            with open(temp_audio_path, 'rb') as f_src, open(output_path, 'wb') as f_dst:
                f_dst.write(f_src.read())
            return True
        except Exception as e:
            self.log(f"Hugging Face Music API failed: {str(e)}", "WARNING")
            return False

    def _generate_procedural_dsp_music(self, prompt_data, bpm, output_path):
        """
        THE GOD-LEVEL FALLBACK:
        If all APIs fail, this engine mathematically synthesizes a background music track
        from scratch (0 bytes to WAV) using Python's math and wave libraries!
        """
        duration = min(prompt_data.get("duration_needed_sec", 15.0), 30.0)
        vibe = prompt_data.get("music_prompt", "").lower()
        
        sample_rate = 44100
        num_samples = int(duration * sample_rate)
        
        # Determine mathematical properties based on Limitless Vibe
        if "phonk" in vibe or "aggressive" in vibe or "fast" in vibe:
            base_freq = 40.0  # Deep bass
            rhythm_speed = (bpm / 60.0) * 2 # Fast pulse
            is_ambient = False
        else:
            base_freq = 65.41 # C2 Note (Deep cinematic pad)
            rhythm_speed = (bpm / 60.0) / 2 # Slow pulse
            is_ambient = True

        self.log(f"Synthesizing Procedural DSP Track. Mode: {'Ambient' if is_ambient else 'Rhythmic'}", "STATUS")
        
        try:
            with wave.open(output_path, 'w') as wav_file:
                wav_file.setnchannels(1) # Mono BGM
                wav_file.setsampwidth(2) # 16-bit
                wav_file.setframerate(sample_rate)
                
                for i in range(num_samples):
                    t = float(i) / sample_rate
                    val = 0.0
                    
                    # Layer 1: Drone Pad (Sine Wave)
                    drone = math.sin(2 * math.pi * base_freq * t)
                    drone += math.sin(2 * math.pi * (base_freq * 1.5) * t) * 0.5 # Add fifth harmonic
                    
                    # Layer 2: Rhythmic Pulse (LFO)
                    lfo = (math.sin(2 * math.pi * rhythm_speed * t) + 1.0) / 2.0
                    
                    # Layer 3: Texture/Noise
                    noise = random.uniform(-0.1, 0.1)

                    if is_ambient:
                        val = (drone * 0.4) + noise
                    else:
                        # Rhythmic Bass
                        val = (drone * lfo * 0.8) + (math.sin(2 * math.pi * base_freq * 2 * t) * (1-lfo) * 0.3)
                    
                    # Fade In / Fade Out logic (1 second smooth edges)
                    fade = 1.0
                    if t < 1.0:
                        fade = t
                    elif t > (duration - 1.0):
                        fade = max(0.0, duration - t)
                        
                    val = val * fade * 0.5 # Overall volume reduction to act as BGM
                    
                    # Hard clipping protector and 16-bit conversion
                    val = max(-1.0, min(1.0, val))
                    packed_val = struct.pack('h', int(val * 32767.0))
                    wav_file.writeframes(packed_val)
                    
            return True
        except Exception as e:
            self.log(f"Procedural DSP Synthesis failed: {e}", "ERROR")
            return False

    def process_ost_generation(self):
        state = self._load_matrix_state()
        
        # 1. Atomic Handshake Protocol
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{orchestrator.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        # 2. Extract Limitless Configuration
        global_config = state.get("global_config", {})
        video_format = global_config.get("video_format", "undefined_format")
        global_theme = global_config.get("theme", "neutral_unspecified")

        audio_module = state.get("module_b_audio", {})
        bgm_map = audio_module.get("bgm_automation_map", {})
        segments = bgm_map.get("automation_curves", [])
        
        beat_map = audio_module.get("phonk_beat_map", {})
        bpm = beat_map.get("target_bpm", 130)
        
        if not segments:
            self.log("No BGM automation segments found. Run Ai_Agent_18 first.", "FATAL")
            sys.exit(1)

        # Idempotency Scrubbing
        self._scrub_old_ost_tracks()

        self.log(f"Neural Composer Engine active. Analyzing {len(segments)} narrative scenes for Limitless OST generation...", "STATUS")
        
        ost_prompts = self.generate_music_prompts_ai(segments, bpm, video_format, global_theme)
        
        generated_tracks = []

        for ost in ost_prompts:
            idx = ost.get("segment_index", 0)
            prompt = ost.get("music_prompt", "")
            duration = min(ost.get("duration_needed_sec", 15.0), 30.0)
            
            file_name = f"ost_track_seg_{idx:03d}.wav"
            full_audio_path = os.path.join(self.audio_dir, file_name)
            
            # Step A: Try Neural AI Generation (MusicGen)
            success = self._generate_music_huggingface(prompt, duration, full_audio_path)
            
            # Step B: If AI Fails, Execute God-Level Procedural DSP Synthesis (No limits!)
            if not success:
                self.log(f"Neural Model unavailable. Engaging Offline Mathematical DSP for segment {idx}...", "WARNING")
                success = self._generate_procedural_dsp_music(ost, bpm, full_audio_path)

            if success:
                self.log(f"Successfully secured BGM Track: {file_name}")
                ost["generated_audio_path"] = full_audio_path
            else:
                self.log(f"Total Audio Failure for segment {idx}.", "ERROR")
                ost["generated_audio_path"] = "CRITICAL_FAILURE"
                
            generated_tracks.append(ost)

        # Merge results back into OmniMatrix
        state["module_b_audio"]["custom_neural_ost_tracks"] = generated_tracks
        
        # 3. OmniMatrix Pipeline Handshake
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        state["orchestrator_matrix"]["next_agent"] = "Ai_Agent_19"
        
        self._save_matrix_state(state)
        self.log("Success! Original Soundtrack synthesized and compiled into OmniMatrix. Handoff to Ai_Agent_19.", "SUCCESS")

if __name__ == "__main__":
    composer = AiAgent18_5NeuralOstMusicComposer()
    composer.process_ost_generation()
