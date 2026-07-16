import os
import re
import sys
import json
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

class SuperResolution4kUpscaler:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 47: super_resolution_4k_upscaler"
        self.workspace_dir = workspace_dir
        
        # Gemini API Configs
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.gemini_url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent)"
        
        # Local model configs
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_local = "llama3"
        
        self.output_upscaled_video = os.path.join(self.workspace_dir, "47_super_resolved_4k_video.mp4")

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_blueprint(self):
        interp_path = os.path.join(self.workspace_dir, "46_frame_interpolation_blueprint.json")
        comp_path = os.path.join(self.workspace_dir, "45_bitrate_compression_blueprint.json")
        
        input_video = os.path.join(self.workspace_dir, "44_gpu_accelerated_output.mp4")
        current_res = "1920x1080"

        if os.path.exists(interp_path):
            try:
                with open(interp_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                input_video = data.get("input_video_tracked", input_video)
            except Exception:
                pass

        if os.path.exists(comp_path):
            try:
                with open(comp_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                current_res = data.get("resolution_set", current_res)
            except Exception:
                pass

        return input_video, current_res

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

    def _save_to_workspace(self, data, filename="47_super_resolution_blueprint.json"):
        # SAFEGUARD: Enforce tile size limits on the AI model output parameters directly to protect VRAM.
        specs = data.get("upscale_specifications", {})
        if specs:
            tile_size = specs.get("vram_tile_size", 128)
            if tile_size > 128 or tile_size <= 0:
                print(f"[{self.agent_name}] Safeguard Active: Capping upscale VRAM tile size to 128 (originally {tile_size}) to prevent CUDA OOM!")
                specs["vram_tile_size"] = 128
                
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Super-resolution parameters saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Error saving upscaler configurations: {str(e)}")
            return None

    def design_upscale_parameters(self, target_resolution="3840x2160"):
        input_video, current_res = self._load_upstream_blueprint()
        print(f"[{self.agent_name}] AI Neural Network active. Calculating 4K super-resolution matrix...")

        system_prompt = (
            "You are an expert deep-learning video upscaling AI and super-resolution engine coordinator.\n"
            "Your task is to design upscaling parameters using AI models (like Real-ESRGAN-anime or Waifu2x) to upscale cleanly to 4K.\n"
            "Output a raw JSON object containing these exact configuration keys:\n"
            "- 'target_resolution': string (always '3840x2160' for 4K).\n"
            "- 'ai_model_name': string (choose from: 'realesrgan-x4plus-anime' for cartoons/anime, 'realesrgan-x4plus' for realistic footage, 'waifu2x-vulkan' for high-speed Vulkan processing).\n"
            "- 'upscale_factor': float (usually 2.0 or 4.0).\n"
            "- 'denoise_strength': float (scale from 0.0 to 1.0).\n"
            "- 'vram_tile_size': integer (SAFE SPECIFICATION: must be set to 128 or lower to prevent Out Of Memory crashes on free GPUs).\n"
            "- 'gpu_backend': string (choose 'cuda' for Nvidia, 'vulkan' for cross-platform, or 'cpu' for safe rendering).\n"
            "- 'ffmpeg_sr_filter_command': string representing the suggested scaling command template using the selected parameters.\n"
            "Format your output STRICTLY as a raw JSON object with only the keys listed above. Do not write markdown formatting or backticks."
        )

        user_content = (
            f"Source Video Path: '{input_video}'\n"
            f"Current Resolution: {current_res}\n"
            f"Target Resolution Requested: {target_resolution}\n"
            f"Content Type Preference: Anime Style (optimized for vector lines)"
        )

        if self.gemini_key:
            print(f"[{self.agent_name}] Status: Querying Google Gemini Cloud AI Node")
            url = f"{self.gemini_url}?key={self.gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{system_prompt}\n\nUser Context:\n{user_content}"
                    }]
                }],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }
        else:
            print(f"[{self.agent_name}] Warning: Gemini Key missing! Querying Local LLM Instance [{self.model_local}]")
            url = self.ollama_url
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": self.model_local,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                "stream": False,
                "format": "json"
            }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            
            with urllib.request.urlopen(req, timeout=50) as response:
                result = response.read().decode("utf-8")
                response_json = json.loads(result)
                
                if self.gemini_key:
                    raw_ai_message = response_json["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    raw_ai_message = response_json["message"]["content"]
                
                cleaned_message = self._clean_json_response(raw_ai_message)
                structured_output = json.loads(cleaned_message)
                
                final_output = {
                    "agent_executed": self.agent_name,
                    "input_video_source": input_video,
                    "upscale_specifications": structured_output
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] AI engine lookup failed: {str(e)}. Loading fallback procedural super-resolution matrix.")
            return self._execute_procedural_fallback(input_video, current_res, target_resolution)

    def _execute_procedural_fallback(self, input_video, current_res, target_resolution):
        print(f"[{self.agent_name}] Executing local procedural fallback filter design.")
        model_fallback = "realesrgan-x4plus-anime"
        scale_factor = 2.0 if "1080" in current_res else 4.0
        tile_size = 128
        
        fallback_filter = f"ffmpeg -i {input_video} -vf scale={target_resolution.replace('x', ':')}:flags=neighbor {self.output_upscaled_video}"

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Fallback)",
            "input_video_source": input_video,
            "upscale_specifications": {
                "target_resolution": target_resolution,
                "ai_model_name": model_fallback,
                "upscale_factor": scale_factor,
                "denoise_strength": 0.5,
                "vram_tile_size": tile_size,
                "gpu_backend": "vulkan",
                "ffmpeg_sr_filter_command": fallback_filter
            }
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    upscaler = SuperResolution4kUpscaler()
    result = upscaler.design_upscale_parameters(target_resolution="3840x2160")
    print("\n--- Z-NET SUPER-RESOLUTION ENGINE COMPLETE ---")
