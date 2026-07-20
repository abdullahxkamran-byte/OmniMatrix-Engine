import os
import re
import sys
import json
import time
import urllib.request
import urllib.error
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class UniversalWordCountGuard:
    def __init__(self, state_file_path="matrix_state.json"):
        self.agent_name = "Agent 06: word_count_guard_utility"
        self.state_file = state_file_path
        
        # Network Resilience for AI Rewriting
        self.max_retries = 2
        self.retry_delay = 2
        
        # API Keys Initialization
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Setup Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            
        # OpenAI/Ollama Setup
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_openai = "gpt-4o-mini"
        self.model_local = "llama3"

    def _log_info(self, message):
        print(f"[{self.agent_name}] INFO: {message}")

    def _log_error(self, message):
        print(f"[{self.agent_name}] ERROR: {message}", file=sys.stderr)

    def _read_state(self):
        if not os.path.exists(self.state_file):
            self._log_error("Critical Error: matrix_state.json not found.")
            sys.exit(1)
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self._log_error(f"Failed to read state file: {str(e)}")
            sys.exit(1)

    def _write_state(self, state_data):
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=4)
        except Exception as e:
            self._log_error(f"Failed to persist state: {str(e)}")

    def _get_target_wps(self, content_format):
        """Determines the optimal speaking speed (Words Per Second) based on format."""
        if content_format == "explainer":
            return 3.0  # Very fast TikTok pacing
        elif content_format == "casual_commentary":
            return 2.5  # Standard YouTuber talking speed
        elif content_format == "cinematic_movie":
            return 2.0  # Slow, dramatic pacing
        return 2.5

    def _ai_compress_text(self, original_text, max_words):
        """Uses Tri-Core AI to intelligently rewrite and compress the sentence safely."""
        system_prompt = (
            "You are a professional voiceover script editor. Your job is to strictly compress sentences.\n"
            f"Rewrite the following text to convey the EXACT same meaning and impact, but in {max_words} words or less.\n"
            "Keep the tone identical. Output ONLY the rewritten sentence without quotes, explanations, or formatting."
        )
        
        # Priority 1: Gemini
        if self.gemini_api_key:
            try:
                response = self.gemini_model.generate_content(f"{system_prompt}\n\nOriginal Text: {original_text}")
                return response.text.strip().replace('"', '')
            except Exception:
                pass # Silent fail, fallback to Priority 2

        # Priority 2: OpenAI
        if self.openai_api_key:
            try:
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"}
                payload = {"model": self.model_openai, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": original_text}]}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    return json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"].strip().replace('"', '')
            except Exception:
                pass

        # Priority 3: Ollama
        try:
            headers = {"Content-Type": "application/json"}
            payload = {"model": self.model_local, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": original_text}], "stream": False}
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))["message"]["content"].strip().replace('"', '')
        except Exception:
            return None # Trigger procedural fallback

    def _programmatic_compress(self, text, max_words):
        """Offline fallback: Regex filter for non-essential words to force compression."""
        words = text.strip().split()
        if len(words) <= max_words:
            return " ".join(words)

        filler_dictionary = {
            "absolutely", "actually", "basically", "completely", "extremely", "literally",
            "seriously", "truly", "very", "highly", "fully", "totally", "definitely", 
            "really", "quite", "just", "simply", "essentially", "ultimately"
        }

        filtered_words = [w for w in words if re.sub(r"[^\w]", "", w).lower() not in filler_dictionary]
        
        if len(filtered_words) > max_words:
            filtered_words = filtered_words[:max_words]
            if filtered_words:
                filtered_words[-1] = re.sub(r"[^\w]$", "", filtered_words[-1]) + "."

        return " ".join(filtered_words)

    def execute(self):
        state = self._read_state()
        
        # Pipeline Gate Check
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Agent_06":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        topic = state.get("runtime_data", {}).get("core_topic", "Unknown Target")
        content_format = state.get("global_config", {}).get("content_format", "explainer")
        
        # Fetch the frames from Agent 03
        agent_03_data = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_03_storyboard", {})
        frames = agent_03_data.get("storyboard_frames", [])

        if not frames:
            self._log_error("Critical Error: Storyboard frames missing. Cannot audit word count.")
            return False

        target_wps = self._get_target_wps(content_format)
        self._log_info(f"Running Semantic Word Count Guard. Target Speed: {target_wps} WPS.")

        audit_queue = []
        optimization_applied = False

        for frame in frames:
            f_idx = frame.get("frame_index", 1)
            start = float(frame.get("timestamp_start", 0.0))
            end = float(frame.get("timestamp_end", start + 3.0))
            duration = max(end - start, 1.0)
            voiceover = frame.get("spoken_audio", "").strip()

            word_count = len(voiceover.split())
            max_recommended_words = int(duration * target_wps)
            
            pacing_status = "safe"
            optimized_text = voiceover

            # If frame has too many words for its duration
            if word_count > max_recommended_words:
                pacing_status = "optimized_safe"
                optimization_applied = True
                self._log_info(f"Frame {f_idx} over limit ({word_count} > {max_recommended_words}). Rewriting via AI...")
                
                # Try AI Rewrite first for perfect grammar
                ai_rewritten = self._ai_compress_text(voiceover, max_recommended_words)
                
                if ai_rewritten and len(ai_rewritten.split()) <= (max_recommended_words + 2): # Allowing +2 buffer for AI
                    optimized_text = ai_rewritten
                    self._log_info(f"AI Rewrote: '{optimized_text}'")
                else:
                    # Fallback to math/regex logic
                    optimized_text = self._programmatic_compress(voiceover, max_recommended_words)
                    self._log_info(f"Procedural Fallback: '{optimized_text}'")
                    
                # Update the actual frame in Agent 03's data so the rest of the pipeline uses the correct text
                frame["spoken_audio"] = optimized_text

            audit_queue.append({
                "frame_index": f_idx,
                "duration_seconds": round(duration, 2),
                "original_word_count": word_count,
                "optimized_word_count": len(optimized_text.split()),
                "max_allowed_words": max_recommended_words,
                "pacing_status": pacing_status
            })

        # Save Audit Data
        audit_report = {
            "source_topic": topic,
            "target_wps_applied": target_wps,
            "optimization_triggered": optimization_applied,
            "timeline_audits": audit_queue
        }
        
        # Update State 
        state["runtime_data"]["module_a_scripting"]["agent_03_storyboard"]["storyboard_frames"] = frames # Update original frames
        state["runtime_data"]["module_a_scripting"]["agent_06_word_guard"] = audit_report
        
        # PERFECT MASTER LIST HANDSHAKE -> Module A almost complete!
        state["pipeline_status"]["last_active_agent"] = "Agent_06"
        state["pipeline_status"]["next_agent"] = "Ai_Agent_07"
        
        self._write_state(state)
        
        self._log_info("Word Guard Passed! Voiceover logic optimized. Pipeline handed to Ai_Agent_07: dark_phonk_vibe_enhancer.")
        return True

if __name__ == "__main__":
    guard = UniversalWordCountGuard()
    guard.execute()
