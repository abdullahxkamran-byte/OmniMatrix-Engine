import os
import re
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

# Manual .env loader utility (In case python-dotenv is not installed)
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

class OpticalFlowFrameInterpolator:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 46: optical_flow_frame_interpolator"
        self.workspace_dir = workspace_dir
        
        # Gemini API Configs
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        # Local fallback config
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_local = "llama3"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_data(self):
        comp_path = os.path.join(self.workspace_dir, "45_bitrate_compression_blueprint.json")
        storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        
        video_metadata = {"source_video": "", "source_fps": 30.0}
        has_high_action = False

        if os.path.exists(comp_path):
            try:
                with open(comp_path, "r", encoding="utf-8") as f:
                    comp_data = json.load(f)
                video_metadata["source_video"] = comp_data.get("output_video_path", "")
                video_metadata["source_fps"] = 30.0
            except Exception:
                pass

        if os.path.exists(storyboard_path):
            try:
                with open(storyboard_path, "r", encoding="utf-8") as f:
                    sb_data = json.load(f)
                for panel in sb_data.get("storyboard_panels", []):
                    if "dynamic" in panel.get("camera_movement_type", "").lower():
                        has_high_action = True
                        break
            except Exception:
                pass

        return video_metadata, has_high_action

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

    def _save_to_workspace(self, data, filename="46_frame_interpolation_blueprint.json"):
        # SAFEGUARD: Prevent high CPU lockups due to exhaustive search ('esa') during high action
        settings = data.get("interpolation_settings", {})
        if settings:
            if settings.get("target_fps", 60) > 60:
                print(f"[{self.agent_name}] Safeguard Active: Capping FPS to 60 to prevent massive processing load!")
                settings["target_fps"] = 60
            
            if settings.get("motion_estimation_algorithm", "") == "esa":
                print(f"[{self.agent_name}] Safeguard Active: Downgrading 'esa' (Exhaustive Search) to 'epzs' (Fast Search) to save Colab RAM!")
                settings["motion_estimation_algorithm"] = "epzs"
                # Re-adjust filter string dynamically to match safeguard
                filter_str = settings.get("ffmpeg_filter_string", "")
                if "me_method=esa" in filter_str:
                    settings["ffmpeg_filter_string"] = filter_str.replace("me_method=esa", "me_method=epzs")

        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Interpolation blueprint saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Error saving interpolation configurations: {str(e)}")
            return None

    def design_smoothness_parameters(self):
        video_meta, high_action = self._load_upstream_data()
        print(f"[{self.agent_name}] AI Engine active. Formulating optical flow motion vectors...")

        system_prompt = (
            "You are an elite video encoding AI and optical flow interpolation specialist.\n"
            "Your task is to analyze the video metadata and output optimal motion-compensated interpolation parameters for FFmpeg's minterpolate filter.\n"
            "Output a raw JSON object with the following keys:\n"
            "- 'target_fps': integer (always set to 60 for ultra-smooth rendering).\n"
            "- 'interpolation_mode': string (choose 'mci' for Motion Compensated Interpolation, or 'blend' if sudden fast cuts occur).\n"
            "- 'motion_estimation_algorithm': string (choose 'epzs' for fast search, or 'tss' for three-step search).\n"
            "- 'motion_compensation_method': string (choose 'obmc' for Overlapped Block Motion Compensation, or 'mci').\n"
            "- 'macroblock_size': integer (16 or 8; larger is faster, smaller is cleaner).\n"
            "- 'search_parameter': integer (range 4 to 32; search window range for motion vector).\n"
            "- 'ffmpeg_filter_string': string containing the constructed minterpolate filter (e.g., 'minterpolate=fps=60:mi_mode=mci:mc_mode=obmc:me_method=epzs').\n"
            "Format your output STRICTLY as a raw JSON object with only the keys listed above. Do not include markdown formatting or backticks."
        )

        user_content = (
            f"Input Video: '{video_meta['source_video']}'\n"
            f"Current Frame Rate: {video_meta['source_fps']} FPS\n"
            f"High-Action/Fast Cuts Detected: {high_action}\n"
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
                    "input_video_tracked": video_meta['source_video'],
                    "interpolation_settings": structured_output
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] AI query failed: {str(e)}. Triggering procedural fallback motion engine.")
            return self._execute_procedural_fallback(video_meta, high_action)

    def _execute_procedural_fallback(self, video_meta, high_action):
        if high_action:
            interpolated_mode = "mci"
            mc_method = "obmc"
            me_algo = "epzs"
            mb_size = 16
            search_param = 16
        else:
            interpolated_mode = "mci"
            mc_method = "mci"
            me_algo = "epzs" # Fallback safe algorithm
            mb_size = 8
            search_param = 16

        filter_str = f"minterpolate=fps=60:mi_mode={interpolated_mode}:mc_mode={mc_method}:me_method={me_algo}:mb_size={mb_size}:search_param={search_param}"

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Fallback)",
            "input_video_tracked": video_meta['source_video'],
            "interpolation_settings": {
                "target_fps": 60,
                "interpolation_mode": interpolated_mode,
                "motion_estimation_algorithm": me_algo,
                "motion_compensation_method": mc_method,
                "macroblock_size": mb_size,
                "search_parameter": search_param,
                "ffmpeg_filter_string": filter_str
            }
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    interpolator = OpticalFlowFrameInterpolator()
    result = interpolator.design_smoothness_parameters()
    print("\n--- Z-NET OPTICAL FLOW INTERPOLATOR SYSTEM COMPLETE ---")
