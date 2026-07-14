import os
import re
import sys
import json
import urllib.request
import urllib.error

class OpticalFlowFrameInterpolator:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 46: optical_flow_frame_interpolator"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_data(self):
        # Compression metadata aur high-action cues load karta hai parameters tuning ke liye
        comp_path = os.path.join(self.workspace_dir, "45_bitrate_compression_blueprint.json")
        storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        
        video_metadata = {"source_video": "", "source_fps": 30.0}
        has_high_action = False

        if os.path.exists(comp_path):
            try:
                with open(comp_path, "r", encoding="utf-8") as f:
                    comp_data = json.load(f)
                video_metadata["source_video"] = comp_data.get("output_video_path", "")
                # Defaulting base to 30.0 if not parsed
                video_metadata["source_fps"] = 30.0
            except Exception:
                pass

        if os.path.exists(storyboard_path):
            try:
                with open(storyboard_path, "r", encoding="utf-8") as f:
                    sb_data = json.load(f)
                for panel in sb_data.get("storyboard_panels", []):
                    # Agar scene me high intensity camera movement ya action hai, toh flow adjust karenge
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
            "Your task is to analyze the video metadata and output optimal motion-compensated interpolation parameters for FFmpeg's minterpolate filter to upscale video from 24/30 FPS to ultra-smooth 60 FPS.\n"
            "Output a raw JSON object with the following keys:\n"
            "- 'target_fps': integer (always set to 60 for ultra-smooth rendering).\n"
            "- 'interpolation_mode': string (choose between 'mci' for Motion Compensated Interpolation or 'blend' if video has too many sudden visual cuts to prevent distortion).\n"
            "- 'motion_estimation_algorithm': string (choose from: 'epzs' for fast motion search, 'esa' for exhaustive slow search, 'tss' for three step search).\n"
            "- 'motion_compensation_method': string (choose from: 'obmc' for Overlapped Block Motion Compensation to smooth edge halos, or 'mci').\n"
            "- 'macroblock_size': integer (usually 16 or 8; smaller means finer motion detection but higher CPU/GPU load).\n"
            "- 'search_parameter': integer (range 4 to 32; defines search window range for motion vector tracking).\n"
            "- 'ffmpeg_filter_string': string containing the constructed minterpolate filter (e.g., 'minterpolate=fps=60:mi_mode=mci:mc_mode=obmc:me_method=epzs').\n"
            "Format your output STRICTLY as a raw JSON object. Do not output conversational text or backticks."
        )

        user_content = (
            f"Input Video: '{video_meta['source_video']}'\n"
            f"Current Frame Rate: {video_meta['source_fps']} FPS\n"
            f"High-Action/Fast Cuts Detected: {high_action}\n"
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
                    "input_video_tracked": video_meta['source_video'],
                    "interpolation_settings": structured_output
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] AI query failed: {str(e)}. Triggering procedural fallback motion engine.")
            return self._execute_procedural_fallback(video_meta, high_action)

    def _execute_procedural_fallback(self, video_meta, high_action):
        # Procedural fallback math calculations to avoid pipeline breakages
        if high_action:
            # High action scenes require safety overrides to avoid extreme warping artifacts
            interpolated_mode = "mci"
            mc_method = "obmc"  # smooth edge guards active
            me_algo = "epzs"
            mb_size = 16
            search_param = 16
        else:
            interpolated_mode = "mci"
            mc_method = "mci"
            me_algo = "esa"
            mb_size = 8
            search_param = 32

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
    
    print("\n--- Z-NET OPTICAL FLOW INTERPOLATOR: AGENT 46 COMPLETE ---")
    settings = result.get("interpolation_settings", {})
    print(f"Target Frame Rate: {settings.get('target_fps', 'N/A')} FPS")
    print(f"Estimation Method: {settings.get('motion_estimation_algorithm', 'N/A')} (Mode: {settings.get('interpolation_mode', 'N/A')})")
    print(f"Generated FFmpeg Filter:\n  '{settings.get('ffmpeg_filter_string', 'N/A')}'")
    print("-----------------------------------------------------------")
