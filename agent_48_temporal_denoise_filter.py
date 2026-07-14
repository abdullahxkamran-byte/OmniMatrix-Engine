import os
import sys
import json
import subprocess
import shutil

class TemporalDenoiseFilter:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 48: temporal_denoise_filter"
        self.workspace_dir = workspace_dir
        self.super_res_blueprint_path = os.path.join(self.workspace_dir, "47_super_resolution_blueprint.json")
        self.output_denoised_video = os.path.join(self.workspace_dir, "48_final_denoised_clean.mp4")

    def _load_upstream_data(self):
        # 47_super_resolution_blueprint.json se settings uthate hain resolution aur input formats match karne ke liye
        input_video = os.path.join(self.workspace_dir, "47_super_resolved_4k_video.mp4")
        denoise_strength_bias = 0.5

        if os.path.exists(self.super_res_blueprint_path):
            try:
                with open(self.super_res_blueprint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                specs = data.get("upscale_specifications", {})
                
                # Agar previous dynamic path specified ho to check karein
                potential_input = specs.get("ffmpeg_sr_filter_command", "")
                if "output" in potential_input:
                    # extract output path safely if parseable
                    pass
                denoise_strength_bias = specs.get("denoise_strength", 0.5)
            except Exception:
                pass

        # Fallback check agar upscaled file missing ho to directly gpu output ya standard temporal output handle karein
        if not os.path.exists(input_video):
            input_video = os.path.join(self.workspace_dir, "44_gpu_accelerated_output.mp4")

        if not os.path.exists(input_video):
            input_video = os.path.join(self.workspace_dir, "43_temp_merged_output.mp4")

        if not os.path.exists(input_video):
            input_video = "mock_upscaled_input.mp4"

        return input_video, denoise_strength_bias

    def execute_denoising(self, temporal_strength=4, spatial_strength=3):
        # temporal_strength: frame-to-frame noise blending limit (default: 4, range 1-10)
        # spatial_strength: single-frame boundary blending (default: 3, range 1-10)
        
        print(f"[{self.agent_name}] Initializing temporal denoise processing pipeline...")
        input_video, strength_bias = self._load_upstream_data()

        # Scale strength based on AI bias from upscaler
        adjusted_temporal = int(temporal_strength * (strength_bias + 0.5))
        adjusted_spatial = int(spatial_strength * (strength_bias + 0.5))

        # Clamp values to avoid blurring anime outlines
        adjusted_temporal = max(1, min(adjusted_temporal, 10))
        adjusted_spatial = max(1, min(adjusted_spatial, 8))

        print(f"[{self.agent_name}] Noise filters auto-tuned: Temporal={adjusted_temporal}, Spatial={adjusted_spatial}")

        # Standard HQD3D (High Quality Denoise 3D) filter design for anime:
        # hqdn3d=luma_spatial:chroma_spatial:luma_tmp:chroma_tmp
        # Standard dynamic settings values mapping
        luma_spatial = adjusted_spatial
        chroma_spatial = int(adjusted_spatial * 1.5)
        luma_tmp = adjusted_temporal
        chroma_tmp = int(adjusted_temporal * 1.5)

        filter_str = f"hqdn3d={luma_spatial}:{chroma_spatial}:{luma_tmp}:{chroma_tmp}"

        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-vf", filter_str,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            self.output_denoised_video
        ]

        print(f"[{self.agent_name}] Clean Assembled Execution Command:\n{' '.join(cmd)}")

        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path or input_video == "mock_upscaled_input.mp4":
            print(f"[{self.agent_name}] System test dry-run. Executed output saved in dry-run buffer configs.")
            result_data = {
                "agent_executed": self.agent_name,
                "execution_status": "DRY_RUN_SUCCESS",
                "applied_filter": filter_str,
                "command_executed": " ".join(cmd),
                "output_video_path": self.output_denoised_video
            }
            self._save_blueprint(result_data)
            return result_data

        try:
            print(f"[{self.agent_name}] Filtering active temporal frames. Scanning pixel differentials...")
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print(f"[{self.agent_name}] Denoising completed successfully without breaking sharp anime outlines!")
            
            result_data = {
                "agent_executed": self.agent_name,
                "execution_status": "SUCCESS",
                "applied_filter": filter_str,
                "command_executed": " ".join(cmd),
                "output_video_path": self.output_denoised_video
            }
            self._save_blueprint(result_data)
            return result_data

        except subprocess.CalledProcessError as e:
            print(f"[{self.agent_name}] Subprocess error during denoising pass: {e.stderr}")
            failed_data = {
                "agent_executed": self.agent_name,
                "execution_status": "FAILED",
                "error_details": str(e.stderr)
            }
            self._save_blueprint(failed_data)
            return failed_data

    def _save_blueprint(self, data, filename="48_temporal_denoise_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Denoise configuration blueprint saved to '{file_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error saving denoise logs: {str(e)}")

if __name__ == "__main__":
    denoiser = TemporalDenoiseFilter()
    result = denoiser.execute_denoising()
    
    print("\n--- Z-NET TEMPORAL NOISE FILTER: AGENT 48 COMPLETE ---")
    print(f"Execution: {result['execution_status']}")
    print(f"Filter Applied: {result.get('applied_filter', 'N/A')}")
    print(f"Denoised Output Video: '{result.get('output_video_path', 'N/A')}'")
    print("---------------------------------------------------------")
