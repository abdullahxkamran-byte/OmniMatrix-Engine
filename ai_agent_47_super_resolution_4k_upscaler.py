import os
import re
import sys
import json
import time
import random
import shutil
import subprocess
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

class Ai_Agent_47_Super_Resolution_4k_Upscaler:
    """
    OMNIMATRIX V2.0 GOD-LEVEL AI SUPER-RESOLUTION & 4K UPSCALING ENGINE
    Evaluates source video resolution, bitrate encoding manifests, and aesthetic
    style constraints. Dynamically coordinates deep-learning upscaling architectures
    (Real-ESRGAN, Waifu2x, libplacebo) while enforcing VRAM tiling safeguards.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_47_Super_Resolution_4k_Upscaler"
        self.workspace_dir = workspace_dir
        self.interpolation_manifest = os.path.join(self.workspace_dir, "46_frame_interpolation_blueprint.json")
        self.compression_manifest = os.path.join(self.workspace_dir, "45_bitrate_compression_blueprint.json")
        self.input_fallback_video = os.path.join(self.workspace_dir, "45_final_master_compressed_output.mp4")
        self.output_upscaled_video = os.path.join(self.workspace_dir, "47_super_resolved_4k_master.mp4")
        self.output_blueprint_path = os.path.join(self.workspace_dir, "47_super_resolution_blueprint.json")
        
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous super-resolution blueprints and outputs."""
        for filename in ["47_super_resolution_blueprint.json", "47_super_resolved_4k_master.mp4"]:
            file_path = os.path.join(self.workspace_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as error:
                    self.log(f"Failed to scrub legacy asset {file_path}: {error}", "WARNING")

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
            # Hand off to Agent 48 (Temporal Denoise Filter - Pure Utility)
            data["orchestrator_matrix"]["next_agent"] = "Agent_48_Temporal_Denoise_Filter"
            
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
                        "target_res": data.get("target_upscale_resolution", "3840x2160")
                    }
            except Exception:
                pass
        return {"style": "realistic", "theme": "limitless_fidelity", "target_res": "3840x2160"}

    def _load_upstream_metadata(self):
        input_video = self.input_fallback_video
        current_res = "1920x1080"
        current_fps = 24.0

        if os.path.exists(self.interpolation_manifest):
            try:
                with open(self.interpolation_manifest, "r", encoding="utf-8") as f:
                    data = json.load(f)
                input_video = data.get("source_video_referenced", input_video)
                current_fps = float(data.get("interpolation_settings", {}).get("target_fps", 24.0))
            except Exception:
                pass

        if os.path.exists(self.compression_manifest):
            try:
                with open(self.compression_manifest, "r", encoding="utf-8") as f:
                    data = json.load(f)
                current_res = data.get("resolution_mapped", current_res)
            except Exception:
                pass

        return input_video, current_res, current_fps

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
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14, 15, 17: QUAD-CORE SUPER-RESOLUTION SYNTHESIZER
    # =====================================================================
    def design_upscale_parameters(self, override_resolution=None):
        self._handshake("IN_PROGRESS")
        config = self._load_config()
        target_res = override_resolution if override_resolution else config["target_res"]
        input_video, current_res, current_fps = self._load_upstream_metadata()
        
        self.log(f"Quad-Core Super-Resolution Forge Initiated. Style: {config['style'].upper()} | Target: {target_res}")

        # Rule 15: Pure Mathematical & Architecture Selection (Zero Preset Gulaami!)
        prompt = (
            f"You are OMNIMATRIX Lead Deep-Learning Video Specialist. Global Style: '{config['style']}', Theme: '{config['theme']}'.\n"
            "Formulate optimal AI super-resolution and neural upscaling specifications to elevate footage clean to 4K/8K.\n"
            "CRITICAL ARTISTIC RULES:\n"
            "1. If style is REALISTIC: Select models preserving organic micro-textures and film grain ('realesrgan-x4plus', 'libplacebo', or 'bicubic_sharp').\n"
            "2. If style is ANIME: Select vector line-art preservation models ('realesrgan-x4plus-anime' or 'waifu2x-vulkan') with aggressive noise removal.\n"
            "Return STRICTLY a JSON object containing:\n"
            "- 'target_resolution': string (e.g., '3840x2160' or '2160x3840').\n"
            "- 'ai_model_architecture': string ('realesrgan-x4plus-anime', 'realesrgan-x4plus', 'waifu2x-vulkan', or 'libplacebo').\n"
            "- 'upscale_multiplier_factor': float (2.0, 3.0, or 4.0 calculated from source vs target dimensions).\n"
            "- 'spatial_denoise_strength': float (0.0 to 1.0 - aggressive for anime, low for realistic texture preservation).\n"
            "- 'vram_tile_size_px': integer (MUST be set to 128 or 64 to prevent CUDA Out-Of-Memory crashes on local GPUs/Colab T4).\n"
            "- 'hardware_execution_backend': string ('cuda', 'vulkan', or 'cpu').\n"
            "- 'actionable_execution_directive': string (Constructed CLI command or FFmpeg scaling filter string to execute the upscale).\n"
            "Zero compression or placeholders allowed."
        )

        user_msg = json.dumps({
            "source_video_path": input_video,
            "source_resolution": current_res,
            "source_fps": current_fps,
            "target_resolution_requested": target_res,
            "style_enforced": config["style"]
        })

        output = None

        # Core 1: Gemini (Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"{prompt}\n\nUser Context:\n{user_msg}"}]}],
                    "generationConfig": {"temperature": 0.80, "responseMimeType": "application/json"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Synthesized neural super-resolution matrix!", "SUCCESS")
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
                res = self._api_call(self.openai_url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"})
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"]))
                self.log("[Core 2: OpenAI] Synthesized neural super-resolution matrix!", "SUCCESS")
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
                res = self._api_call(self.ollama_url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res.get("message", {}).get("content", "{}")))
                self.log("[Core 3: Ollama] Generated local super-resolution matrix!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Math Autonomy (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline continuous super-resolution formulation...", "WARNING")
            is_anime = config["style"] == "anime"
            
            # Math calculation for scale multiplier
            try:
                src_w = int(current_res.split("x")[0])
                tgt_w = int(target_res.split("x")[0])
                calc_factor = round(float(tgt_w) / float(max(1, src_w)), 1)
            except Exception:
                calc_factor = 2.0

            model_name = "realesrgan-x4plus-anime" if is_anime else "realesrgan-x4plus"
            denoise = 0.65 if is_anime else 0.15
            tile_px = 128
            
            # Construct actionable FFmpeg high-quality Lanczos/Libplacebo fallback directive
            ff_command = f"ffmpeg -y -i {input_video} -vf scale={target_res.replace('x', ':')}:flags=lanczos+accurate_rnd -c:v libx264 -preset slow -crf 16 -c:a copy {self.output_upscaled_video}"
            
            output = {
                "target_resolution": target_res,
                "ai_model_architecture": model_name,
                "upscale_multiplier_factor": max(2.0, calc_factor),
                "spatial_denoise_strength": denoise,
                "vram_tile_size_px": tile_px,
                "hardware_execution_backend": "vulkan",
                "actionable_execution_directive": ff_command
            }

        # Rule 17 Safeguard: Enforce VRAM tile size ceilings strictly to prevent CUDA OOM
        tile_size = int(output.get("vram_tile_size_px", 128))
        if tile_size > 128 or tile_size <= 0:
            self.log(f"Safeguard Triggered: Capping VRAM tile size from {tile_size}px down to 128px to prevent GPU memory overflow!", "WARNING")
            output["vram_tile_size_px"] = 128

        final_blueprint = {
            "agent_executed": self.agent_name,
            "execution_timestamp": time.time(),
            "input_video_referenced": input_video,
            "source_resolution_detected": current_res,
            "style_enforced": config["style"],
            "upscale_specifications": output
        }

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=4)

        self.log(f"Super-resolution 4K/8K blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return final_blueprint

if __name__ == "__main__":
    upscaler = Ai_Agent_47_Super_Resolution_4k_Upscaler()
    upscaler.design_upscale_parameters()
