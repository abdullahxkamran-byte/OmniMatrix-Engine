import os
import sys
import json
import re
import urllib.request
import time

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
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 18.5: neural_ost_music_composer"
        self.workspace_dir = workspace_dir
        self.audio_dir = os.path.join(self.workspace_dir, "audio_tracks", "bgm_ost")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)
        self.hf_token = os.environ.get("HF_TOKEN", None)

        if GEMINI_AVAILABLE and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

        os.makedirs(self.audio_dir, exist_ok=True)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        """Loads the central OmniMatrix state file."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run upstream modules first.", "ERROR")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        """Saves the generated OST tracks back to the central state."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("OmniMatrix state successfully updated with Custom Neural OSTs.")

    def _clean_json_response(self, raw_text):
        """Strips markdown and extracts pure JSON string."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def generate_music_prompts_ai(self, bgm_segments, target_bpm):
        """Uses AI logic cores to design highly descriptive prompts for MusicGen."""
        system_prompt = (
            "You are an elite music composer and prompt engineer for AI Music Generation models (like MusicGen). "
            "Analyze the video's BGM segments and convert them into highly descriptive, instrument-rich text prompts.\n"
            "Return STRICTLY a JSON object containing a list named 'ost_prompts'.\n"
            "Each prompt object must contain:\n"
            "- 'segment_index': integer matching the list order.\n"
            "- 'start_sec': float.\n"
            "- 'end_sec': float.\n"
            "- 'music_prompt': string (Highly detailed text for the AI. Include instruments, vibe, tempo. e.g., 'Aggressive drift phonk beat with heavy 808 bass, distorted cowbells, fast tempo, dark cinematic choir in background').\n"
            "- 'duration_needed_sec': float (Calculate end_sec - start_sec, minimum 10.0 seconds).\n"
        )
        
        user_prompt = f"Base BPM: {target_bpm}\nBGM Segments Automation Map:\n{json.dumps(bgm_segments, indent=2)}"

        if GEMINI_AVAILABLE and self.gemini_api_key:
            self.log("Routing to Core 1: Gemini AI for OST Prompt Architecture...")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    system_prompt + "\n\n" + user_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text.strip()).get("ost_prompts", [])
            except Exception as e:
                self.log(f"Gemini Engine failed: {e}. Switching to OpenAI fallback.", "WARNING")

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
                self.log(f"OpenAI Engine failed: {e}. Engaging Offline Math Logic.", "WARNING")

        self.log("All AI API Cores failed. Using procedural fallback prompts.", "STATUS")
        return self._execute_procedural_fallback(bgm_segments)

    def _execute_procedural_fallback(self, segments):
        prompts = []
        for idx, seg in enumerate(segments):
            style = seg.get("bgm_vibe_style", "dark-ambient")
            dur = seg.get("end_sec", 15.0) - seg.get("start_sec", 0.0)
            dur = max(dur, 10.0)
            
            if "phonk" in style:
                prompt_text = "Aggressive drift phonk beat with heavy 808 bass, distorted cowbells, fast tempo."
            elif "epic" in style:
                prompt_text = "Epic orchestral climax, cinematic horns, heavy percussion, dramatic choir."
            else:
                prompt_text = "Dark ambient cinematic background music, slow synth pad, suspenseful atmosphere."
                
            prompts.append({
                "segment_index": idx,
                "start_sec": seg.get("start_sec", 0.0),
                "end_sec": seg.get("end_sec", dur),
                "music_prompt": prompt_text,
                "duration_needed_sec": dur
            })
        return prompts

    def _generate_music_huggingface(self, text_prompt, duration, output_path):
        """Contacts a Hugging Face Space running MusicGen via Gradio Client."""
        if not GRADIO_CLIENT_AVAILABLE:
            self.log("gradio_client not installed. Skipping direct generation.", "WARNING")
            return False

        self.log(f"Generating OST via AI: '{text_prompt[:50]}...' (Duration: {duration}s)", "STATUS")
        
        try:
            # Note: "facebook/MusicGen" or public equivalent space. 
            # This requires a space that accepts (text, duration)
            client = Client("facebook/MusicGen") 
            result = client.predict(
                text_prompt,
                "none", # Melody conditioning (none)
                duration, # Duration in seconds
                api_name="/predict"
            )
            
            temp_audio_path = result[1] if isinstance(result, tuple) else result
            
            with open(temp_audio_path, 'rb') as f_src, open(output_path, 'wb') as f_dst:
                f_dst.write(f_src.read())
                
            return True
        except Exception as e:
            self.log(f"Hugging Face Music API failed: {str(e)}", "WARNING")
            return False

    def process_ost_generation(self):
        state = self._load_matrix_state()
        
        audio_module = state.get("module_b_audio", {})
        bgm_map = audio_module.get("bgm_automation_map", {})
        segments = bgm_map.get("automation_curves", [])
        beat_map = audio_module.get("phonk_beat_map", {})
        bpm = beat_map.get("target_bpm", 130)
        
        if not segments:
            self.log("No BGM automation segments found. Run Agent 18 first.", "ERROR")
            return

        self.log(f"Composer Engine active. Analyzing {len(segments)} narrative scenes for music generation...")
        
        ost_prompts = self.generate_music_prompts_ai(segments, bpm)
        
        generated_tracks = []

        for ost in ost_prompts:
            idx = ost.get("segment_index", 0)
            prompt = ost.get("music_prompt", "")
            duration = min(ost.get("duration_needed_sec", 15.0), 30.0) # Cap at 30s per generation for free APIs
            
            file_name = f"custom_ost_segment_{idx:03d}.wav"
            full_audio_path = os.path.join(self.audio_dir, file_name)
            
            success = self._generate_music_huggingface(prompt, duration, full_audio_path)
            
            if success:
                self.log(f"Successfully generated custom OST: {file_name}")
                ost["generated_audio_path"] = full_audio_path
            else:
                self.log(f"Could not generate track {idx}. Leaving placeholder for manual fallback.", "WARNING")
                ost["generated_audio_path"] = "MANUAL_BGM_REQUIRED"
                
            generated_tracks.append(ost)

        # Merge results back into OmniMatrix
        state["module_b_audio"]["custom_neural_ost_tracks"] = generated_tracks
        
        # Pipeline Handshake
        state["pipeline_status"]["last_active_agent"] = "Ai_Agent_18_5"
        state["pipeline_status"]["next_agent"] = "Ai_Agent_19"
        
        self._save_matrix_state(state)
        self.log("Success! Original Soundtrack compiled into OmniMatrix. Ready for Agent 19.")

if __name__ == "__main__":
    composer = AiAgent18_5NeuralOstMusicComposer()
    composer.process_ost_generation()
    print("\n--- OMNIMATRIX MODULE B: AGENT 18.5 OST COMPOSER COMPLETE ---")
