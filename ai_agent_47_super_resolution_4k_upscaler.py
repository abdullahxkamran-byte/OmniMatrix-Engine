import os
import re
import sys
import json
import urllib.request
import urllib.error

class SuperResolution4kUpscaler:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 47: super_resolution_4k_upscaler"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)
        self.output_upscaled_video = os.path.join(self.workspace_dir, "47_super_resolved_4k_video.mp4")

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_blueprint(self):
        # Frame interpolation aur previous compression blueprints read karta hai resolution match karne ke liye
        interp_path = os.path.join(self.workspace_dir, "46_frame_interpolation_blueprint.json")
        comp_path = os.path.join(self.workspace_dir, "45_bitrate_compression_blueprint.json")
        
        input_video = os.path.join(self.workspace_dir, "44_gpu_accelerated_output.mp4") # Default input
        current_res = "1920x1080" # Default baseline

        if os.path.exists(interp_path):
            try:
                with open(interp_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Interpolator output ko track karta hai as primary input
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
            "Your task is to analyze the source video parameters and design the absolute best upscaling parameters using AI models (like Real-ESRGAN-anime, Waifu2x, or neural-network-based filters) to hit 4K resolution cleanly without blurry edges.\n"
            "Output a raw JSON object containing these exact configuration keys:\n"
            "- 'target_resolution': string (e.g., '3840x2160' for 4K horizontal).\n"
            "- 'ai_model_name': string (choose from: 'realesrgan-x4plus-anime' for sharp cartoon/anime lines, 'realesrgan-x4plus' for cinematic realistic footage, 'waifu2x-vulkan' for light-weight high-speed upscaling).\n"
            "- 'upscale_factor': float (e.g., 2.0 or 4.0 depending on the scale from current resolution to target resolution).\n"
            "- 'denoise_strength': float (scale from 0.0 to 1.0; defines how much compression noise to suppress before upscaling).\n"
            "- 'vram_tile_size': integer (default 128 or 256; lower tile size prevents 'Out of Memory' crashes on low-end GPUs during heavy neural passes).\n"
            "- 'gpu_backend': string (choose from: 'cuda' for Nvidia GPUs, 'vulkan' for universal cross-platform compatibility, 'cpu' for safe slow rendering).\n"
            "- 'ffmpeg_sr_filter_command': string representing the suggested scaling command template using the selected parameters.\n"
            "Format your output STRICTLY as a raw JSON object. Do not output conversational text, backticks, or markdown formatting."
        )

        user_content = (
            f"Source Video Path: '{input_video}'\n"
            f"Current Resolution: {current_res}\n"
            f"Target Resolution Requested: {target_resolution}\n"
            f"Content Type Preference: Anime Style (highly optimized for clean vector lines and high color contrast)"
        )

        if self.openai_api_key:
            print(f"[{self.agent_name}] Status: Querying Cloud API Node [{self.model_cloud}]")
            url = self.openai_url
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            payload = {
                "model": self.model_cloud,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                "response_format": {"type": "json_object"}
            }
        else:
            print(f"[{self.agent_name}] Status: Querying Local LLM Instance [{self.model_local}]")
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
                
                if self.openai_api_key:
                    raw_ai_message = response_json["choices"][0]["message"]["content"]
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
        # Safety fallback using high-performance mathematical modeling
        print(f"[{self.agent_name}] Executing local procedural fallback filter design.")
        
        # Anime-centric scaling configurations
        model_fallback = "realesrgan-x4plus-anime"
        scale_factor = 2.0 if "1080" in current_res else 4.0
        tile_size = 128  # Safe baseline to protect graphics memory
        
        # Generate safe custom scale filter for FFmpeg using libx264 backend if AI tools are offline
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
    # Testing upscale configuration targets for 4K horizontal (3840x2160)
    result = upscaler.design_upscale_parameters(target_resolution="3840x2160")
    
    print("\n--- Z-NET SUPER-RESOLUTION ENGINE: AGENT 47 COMPLETE ---")
    specs = result.get("upscale_specifications", {})
    print(f"Target Output Resolution: {specs.get('target_resolution', 'N/A')}")
    print(f"AI Model Selected: {specs.get('ai_model_name', 'N/A')} (Backend: {specs.get('gpu_backend', 'N/A')})")
    print(f"VRAM Tile Constraint: {specs.get('vram_tile_size', 'N/A')} blocks (Safe protection active)")
    print(f"Execution Command Template:\n  '{specs.get('ffmpeg_sr_filter_command', 'N/A')}'")
    print("---------------------------------------------------------")
