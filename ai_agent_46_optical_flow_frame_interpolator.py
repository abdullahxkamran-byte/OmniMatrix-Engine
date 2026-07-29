import os
import re
import sys
import json
import time
import random
import urllib.request
import urllib.error

# =====================================================================
# RULE 2 & 14: UNIVERSAL ENVIRONMENT & DUAL API CONFIGURATION
# =====================================================================
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class Ai_Agent_46_Optical_Flow_Frame_Interpolator:
    """
    OMNIMATRIX V2.0 GOD-LEVEL OPTICAL FLOW & FRAME INTERPOLATION ENGINE
    Analyzes visual motion vectors, camera dynamics, and aesthetic style guidelines.
    Synthesizes actionable FFmpeg minterpolate directives while protecting anime
    hit-stop cadence and enabling ultra-smooth cinematic frame rates.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_46_Optical_Flow_Frame_Interpolator"
        self.workspace_dir = workspace_dir
        self.compression_manifest = os.path.join(self.workspace_dir, "45_bitrate_compression_blueprint.json")
        self.input_video_path = os.path.join(self.workspace_dir, "45_final_master_compressed_output.mp4")
        self.output_blueprint_path = os.path.join(self.workspace_dir, "46_frame_interpolation_blueprint.json")
        
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous interpolation blueprints."""
        if os.path.exists(self.output_blueprint_path):
            try:
                os.remove(self.output_blueprint_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy blueprint {self.output_blueprint_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7 & 4: ATOMIC HANDSHAKE & CONFIGURATION LOADERS
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS"):
        matrix_path = os.path.join(self.workspace_dir, "matrix_state.json")
        data = {}
        if os.path.exists(matrix_path):
            try:
                with open(matrix_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        if "orchestrator_matrix" not in data:
            data["orchestrator_matrix"] = {}
            
        data["orchestrator_matrix"].update({
            "last_active_agent": self.agent_name,
            "last_update_timestamp": time.time(),
            "agent_status": {self.agent_name: status}
        })
        
        if status == "COMPLETED":
            # Hand off to Agent 47 (Super Resolution 4K Upscaler)
            data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_47_Super_Resolution_4k_Upscaler"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_config(self):
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {
                        "style": data.get("global_style", "realistic").lower(),
                        "theme": data.get("theme", "cinematic"),
                        "target_fps": float(data.get("render_fps", 24.0))
                    }
            except Exception:
                pass
        return {"style": "realistic", "theme": "limitless_motion", "target_fps": 24.0}

    def _load_upstream_metadata(self):
        storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        beat_path = os.path.join(self.workspace_dir, "41_beat_sync_blueprint.json")
        
        has_high_action = False
        hit_stop_count = 0

        if os.path.exists(storyboard_path):
            try:
                with open(storyboard_path, "r", encoding="utf-8") as f:
                    for panel in json.load(f).get("storyboard_panels", []):
                        if any(k in str(panel).lower() for k in ["climax", "fast", "impact", "sakuga", "explosion"]):
                            has_high_action = True
                            break
            except Exception:
                pass

        if os.path.exists(beat_path):
            try:
                with open(beat_path, "r", encoding="utf-8") as f:
                    for profile in json.load(f).get("beat_sync_profiles", []):
                        if profile.get("fps_stutter_trigger", False):
                            hit_stop_count += 1
            except Exception:
                pass

        return has_high_action, hit_stop_count

    def _clean_json(self, raw_text):
        """Rule 5: Bulletproof JSON scrubber."""
        cleaned = re.sub(r"^```(json)?\s*|\s*```$", "", raw_text.strip(), flags=re.IGNORECASE)
        start_index = cleaned.find('{')
        end_index = cleaned.rfind('}')
        if start_index != -1 and end_index != -1:
            return cleaned[start_index:end_index + 1]
        return cleaned

    def _api_call(self, url, payload, headers):
        request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(request, timeout=40) as response:
            return json.loads(response.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14, 15, 17: QUAD-CORE OPTICAL FLOW SYNTHESIZER
    # =====================================================================
    def design_smoothness_parameters(self):
        self._handshake("IN_PROGRESS")
        config = self._load_config()
        has_high_action, hit_stop_count = self._load_upstream_metadata()
        
        self.log(f"Quad-Core Optical Flow Engine Initiated. Style: {config['style'].upper()} | High Action: {has_high_action}")

        # Rule 15: Pure Mathematical Optical Flow Formulation (Zero Preset Gulaami!)
        prompt = (
            f"You are OMNIMATRIX Lead Video Encoding TD. Global Style: '{config['style']}', Theme: '{config['theme']}'.\n"
            "Formulate optimal motion-compensated frame interpolation parameters for FFmpeg's minterpolate filter.\n"
            "CRITICAL ARTISTIC RULES:\n"
            "1. If style is REALISTIC: Aim for ultra-smooth cinematic motion (60 FPS or 120 FPS), mode='mci', mc_mode='obmc'.\n"
            "2. If style is ANIME: Preserve classic animation cadence! Do NOT blindly force 60 FPS if hit-stops are present.\n"
            "   Use mode='blend' or 'dup' during heavy action to prevent soap-opera artifacts, or cap at 48/60 FPS with sharp block compensation.\n"
            "Return STRICTLY a JSON object containing:\n"
            "- 'target_fps': integer (24, 30, 48, 60, or 120 based on style constraints).\n"
            "- 'interpolation_mode': string ('mci', 'blend', or 'dup').\n"
            "- 'motion_estimation_algorithm': string ('epzs' for fast search, 'hex', or 'umh'. NEVER use 'esa' to prevent RAM lockup!).\n"
            "- 'motion_compensation_method': string ('obmc' for Overlapped Block, or 'mci').\n"
            "- 'macroblock_size': integer (16 for high speed, 8 for high fidelity).\n"
            "- 'search_parameter': integer (4 to 32 - motion vector search radius).\n"
            "- 'scene_change_threshold': float (0.1 to 0.8 - threshold to prevent morphing across scene cuts).\n"
            "- 'actionable_ffmpeg_afilter': string (Constructed executable video filter, e.g., 'minterpolate=fps=60:mi_mode=mci:mc_mode=obmc:me_method=epzs:mb_size=16:search_param=16:scd=1').\n"
            "Zero compression or placeholders allowed."
        )

        user_msg = json.dumps({
            "source_fps": config["target_fps"],
            "high_action_detected": has_high_action,
            "hit_stop_markers_count": hit_stop_count,
            "style_enforced": config["style"]
        })

        output = None

        # Core 1: Gemini (Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"{prompt}\n\nUser Context:\n{user_msg}"}]}],
                    "generationConfig": {"temperature": 0.82, "responseMimeType": "application/json"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Synthesized optical flow interpolation parameters!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")

        # Core 2: OpenAI Failsafe (Rule 14 & 16)
        if self.openai_key and not output:
            try:
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                    "response_format": {"type": "json_object"}
                }
                res = self._api_call(self.openai_url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_key}"})
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"]))
                self.log("[Core 2: OpenAI] Synthesized optical flow interpolation parameters!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")

        # Core 3: Ollama Local Fallback
        if not output:
            try:
                payload = {
                    "model": "llama3",
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                    "format": "json",
                    "stream": False
                }
                res = self._api_call(self.ollama_url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res.get("message", {}).get("content", "{}")))
                self.log("[Core 3: Ollama] Generated local optical flow parameters!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Math Autonomy (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline continuous optical flow formulation...", "WARNING")
            is_anime = config["style"] == "anime"
            
            if is_anime and (has_high_action or hit_stop_count > 0):
                # Preserve anime punch and hit-stop frames
                target_fps, mode, mc, me, mb, sp, scd = 48, "blend", "mci", "epzs", 16, 16, 0.3
            else:
                # Cinematic fluid motion
                target_fps, mode, mc, me, mb, sp, scd = 60, "mci", "obmc", "epzs", 16, 24, 0.5

            filter_string = f"minterpolate=fps={target_fps}:mi_mode={mode}:mc_mode={mc}:me_method={me}:mb_size={mb}:search_param={sp}:scd=1:scd_threshold={scd}"
            
            output = {
                "target_fps": target_fps,
                "interpolation_mode": mode,
                "motion_estimation_algorithm": me,
                "motion_compensation_method": mc,
                "macroblock_size": mb,
                "search_parameter": sp,
                "scene_change_threshold": scd,
                "actionable_ffmpeg_afilter": filter_string
            }

        # Rule 17 Safeguard: Enforce VRAM and Colab RAM limits
        if output.get("motion_estimation_algorithm", "") == "esa":
            self.log("Safeguard Triggered: Downgrading exhaustive search ('esa') to fast search ('epzs') to prevent CPU lockup!", "WARNING")
            output["motion_estimation_algorithm"] = "epzs"
            output["actionable_ffmpeg_afilter"] = str(output.get("actionable_ffmpeg_afilter", "")).replace("me_method=esa", "me_method=epzs")

        final_blueprint = {
            "agent_executed": self.agent_name,
            "execution_timestamp": time.time(),
            "source_video_referenced": self.input_video_path,
            "style_evaluated": config["style"],
            "interpolation_settings": output
        }

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=4)

        self.log(f"Optical flow interpolation blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return final_blueprint

if __name__ == "__main__":
    interpolator = Ai_Agent_46_Optical_Flow_Frame_Interpolator()
    interpolator.design_smoothness_parameters()
