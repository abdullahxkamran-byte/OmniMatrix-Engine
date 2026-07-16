import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error

# Manual .env loader utility (consistent with Z-Net architecture)
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

class AiMasterContinuityDirector:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 08: master_continuity_director"
        self.workspace_dir = workspace_dir
        
        # Dual-Engine AI Fallback Config
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        self.ollama_url = "http://localhost:11434/api/chat"
        self.ollama_model = "llama3"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_stage_data(self):
        """Loads clean scripts from Stage 6 and aesthetic styles from Stage 7."""
        guard_path = os.path.join(self.workspace_dir, "06_word_count_guard.json")
        phonk_path = os.path.join(self.workspace_dir, "07_dark_phonk_vibe.json")

        guard_data = {}
        phonk_data = {}

        if os.path.exists(guard_path):
            try:
                with open(guard_path, "r", encoding="utf-8") as f:
                    guard_data = json.load(f)
                print(f"[{self.agent_name}] Loaded Stage 6 data successfully.")
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Cannot read Stage 6: {str(e)}")

        if os.path.exists(phonk_path):
            try:
                with open(phonk_path, "r", encoding="utf-8") as f:
                    phonk_data = json.load(f)
                print(f"[{self.agent_name}] Loaded Stage 7 data successfully.")
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Cannot read Stage 7: {str(e)}")

        return guard_data, phonk_data

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

    def _run_ai_alignment_call(self, raw_merged_timeline):
        """Uses Gemini (Cloud) or Ollama (Local) to perform intelligence-based character tagging and script alignment."""
        system_prompt = (
            "You are the Z-Net AI Master Video Director.\n"
            "Your task is to review a series of draft video frames and align them into a high-retention masterpiece.\n"
            "Specifically, you must identify and tag the correct 'character' speaking each line (e.g., 'Gojo', 'Sukuna', 'Naruto', 'Sasuke', 'Narrator') based on the context of the dialogue.\n"
            "Format your output strictly as a RAW JSON object with the following structure:\n"
            "{\n"
            "  \"master_timeline\": [\n"
            "    {\n"
            "      \"frame_index\": 1,\n"
            "      \"character\": \"Narrator\",\n"
            "      \"duration_seconds\": 3.0,\n"
            "      \"spoken_voiceover\": \"The voiceover text\",\n"
            "      \"visual_style_prompt\": \"visual description\",\n"
            "      \"camera_shake_intensity\": 0.5,\n"
            "      \"bass_drop_sync\": false,\n"
            "      \"ambient_glitch_rate\": 0.1,\n"
            "      \"color_palette_hex\": [\"#000000\", \"#ffffff\"]\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "Rules:\n"
            "- Extract correct character names from the dialogue. If it is general narrative, use 'Narrator'.\n"
            "- Do not change the general meaning of the voiceover, but ensure it flows cleanly.\n"
            "- Do not write any markdown formatting or pre-text. Only raw JSON."
        )

        user_content = json.dumps(raw_merged_timeline, indent=2)

        # ENGINE A: GEMINI (CLOUD)
        if self.gemini_key:
            print(f"[{self.agent_name}] Status: Executing Cloud Gemini Master AI Director...")
            url = f"{self.gemini_url}?key={self.gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": f"{system_prompt}\n\nInput Timeline:\n{user_content}"}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            try:
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = response.read().decode("utf-8")
                    res_json = json.loads(result)
                    raw_msg = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(self._clean_json_response(raw_msg))
            except Exception as e:
                print(f"[{self.agent_name}] Gemini alignment failed: {str(e)}. Swapping to Local Ollama...")

        # ENGINE B: OLLAMA (LOCAL FALLBACK)
        print(f"[{self.agent_name}] Status: Executing Local Ollama Llama3 Master Director...")
        payload = {
            "model": self.ollama_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze and align this timeline:\n{user_content}"}
            ],
            "stream": False,
            "format": "json"
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(self.ollama_url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=50) as response:
                result = response.read().decode("utf-8")
                res_json = json.loads(result)
                raw_msg = res_json["message"]["content"]
                return json.loads(self._clean_json_response(raw_msg))
        except Exception as e:
            print(f"[{self.agent_name}] Local Ollama alignment failed: {str(e)}. Using Procedural Merger.")
            return None

    def _procedural_merge_fallback(self, guard_frames, phonk_frames):
        """Standard backup algorithmic alignment if both AI engines fail."""
        print(f"[{self.agent_name}] Running procedural merge backup...")
        master_timeline = []
        phonk_map = {item["frame_index"]: item for item in phonk_frames}
        
        for idx, frame in enumerate(guard_frames):
            f_idx = frame.get("frame_index", idx + 1)
            phonk_meta = phonk_map.get(f_idx, {})
            voiceover = frame.get("optimized_voiceover", frame.get("spoken_voiceover", ""))
            
            # Smart Offline Name Matcher
            voiceover_lower = voiceover.lower()
            character = "Narrator"
            if "gojo" in voiceover_lower:
                character = "Gojo"
            elif "sukuna" in voiceover_lower:
                character = "Sukuna"
            elif "goku" in voiceover_lower:
                character = "Goku"

            master_timeline.append({
                "frame_index": f_idx,
                "character": character,
                "duration_seconds": frame.get("duration_seconds", 3.0),
                "spoken_voiceover": voiceover,
                "visual_style_prompt": phonk_meta.get("visual_style_prompt", "High-contrast dark cinematic style."),
                "camera_shake_intensity": phonk_meta.get("camera_shake_intensity", 0.4),
                "bass_drop_sync": phonk_meta.get("bass_drop_sync", False),
                "ambient_glitch_rate": phonk_meta.get("ambient_glitch_rate", 0.1),
                "color_palette_hex": phonk_meta.get("color_palette_hex", ["#000000", "#ffffff"])
            })
        return {"master_timeline": master_timeline}

    def align_and_format(self):
        guard_data, phonk_data = self._load_stage_data()
        topic = guard_data.get("source_topic", phonk_data.get("source_topic", "General Target"))
        
        guard_frames = guard_data.get("timeline_frames", [])
        phonk_frames = phonk_data.get("phonk_frames", [])

        # Create basic raw merge to pass to AI
        raw_merged = []
        phonk_map = {item["frame_index"]: item for item in phonk_frames}
        for idx, frame in enumerate(guard_frames):
            f_idx = frame.get("frame_index", idx + 1)
            phonk_meta = phonk_map.get(f_idx, {})
            raw_merged.append({
                "frame_index": f_idx,
                "spoken_voiceover": frame.get("optimized_voiceover", frame.get("spoken_voiceover", "")),
                "visual_style_prompt": phonk_meta.get("visual_style_prompt", "Cinematic dark anime look"),
                "duration_seconds": frame.get("duration_seconds", 3.0)
            })

        # Run alignment
        ai_aligned_data = None
        if raw_merged:
            ai_aligned_data = self._run_ai_alignment_call(raw_merged)

        if not ai_aligned_data:
            ai_aligned_data = self._procedural_merge_fallback(guard_frames, phonk_frames)

        master_timeline = ai_aligned_data.get("master_timeline", [])

        # Construct final payload
        output_json = {
            "source_topic": topic,
            "agent_executed": self.agent_name,
            "total_frames": len(master_timeline),
            "master_timeline": master_timeline
        }

        # Save Structured JSON
        json_path = os.path.join(self.workspace_dir, "08_final_master_script.json")
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(output_json, f, indent=4)
            print(f"[{self.agent_name}] Success: AI Aligned Master JSON written to '{json_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing JSON: {str(e)}")

        # Save Readable TXT Preview for editing references
        txt_path = os.path.join(self.workspace_dir, "08_final_script_preview.txt")
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"=== MASTER VIDEO SCRIPT PREVIEW ===\n")
                f.write(f"Topic: {topic}\n")
                f.write(f"Total Video Frames: {len(master_timeline)}\n")
                f.write(f"====================================\n\n")

                for frame in master_timeline:
                    f_write_block = (
                        f"Frame {frame['frame_index']} | Character: {frame.get('character', 'Narrator')} | Duration: {frame['duration_seconds']}s\n"
                        f"  [Voiceover]: \"{frame['spoken_voiceover']}\"\n"
                        f"  [VFX Style]: {frame['visual_style_prompt']}\n"
                        f"  [Colors]: {', '.join(frame.get('color_palette_hex', ['#000000']))}\n"
                        f"  [Pacing Notes]: Shake: {frame.get('camera_shake_intensity', 0.5)}x, Glitch: {int(frame.get('ambient_glitch_rate', 0.1)*100)}%, Bass Drop Sync: {frame.get('bass_drop_sync', False)}\n"
                        f"----------------------------------------------------------------------\n"
                    )
                    f.write(f_write_block)
            print(f"[{self.agent_name}] Text script preview saved to '{txt_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing Preview Text file: {str(e)}")

        return output_json

if __name__ == "__main__":
    director = AiMasterContinuityDirector()
    output = director.align_and_format()
    print("\n--- Z-NET DYNAMIC AI ALIGNMENT COMPLETE ---")
