import os
import sys
import json
import subprocess
import shutil

class BitrateOptimizerCompressionEngine:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 45: bitrate_optimizer_compression_engine"
        self.workspace_dir = workspace_dir
        self.gpu_blueprint_path = os.path.join(self.workspace_dir, "44_gpu_acceleration_blueprint.json")
        self.output_final_video = os.path.join(self.workspace_dir, "final_compressed_output.mp4")

    def calculate_optimized_bitrate(self, width, height, fps):
        # Professional standard video bitrates for ultimate online streaming quality
        total_pixels = width * height
        
        # 4K Vertical (2160x3840) ya wide 4K
        if total_pixels >= 3840 * 2160:
            base_bitrate_kbps = 35000 if fps <= 30 else 50000
        # 2K Vertical (1440x2560)
        elif total_pixels >= 2560 * 1440:
            base_bitrate_kbps = 16000 if fps <= 30 else 24000
        # 1080p Vertical (1080x1920) - Standard High-Quality Mobile Format
        elif total_pixels >= 1920 * 1080:
            base_bitrate_kbps = 10000 if fps <= 30 else 15000
        # 720p or lower
        else:
            base_bitrate_kbps = 5000 if fps <= 30 else 7500
            
        return base_bitrate_kbps

    def execute_compression(self, target_width=1080, target_height=1920, target_fps=30.0):
        print(f"[{self.agent_name}] Initializing dynamic compression and resolution scaler...")
        print(f"[{self.agent_name}] Target Profile Configured: {target_width}x{target_height} @ {target_fps} FPS")

        # Load dynamic input configurations from Agent 44
        input_video = os.path.join(self.workspace_dir, "44_gpu_accelerated_output.mp4")
        
        if not os.path.exists(input_video):
            print(f"[{self.agent_name}] Upstream accelerated output missing. Using Temp Merged Video fallback.")
            input_video = os.path.join(self.workspace_dir, "43_temp_merged_output.mp4")

        # Fallback check agar dono me se koi file na mile
        if not os.path.exists(input_video):
            print(f"[{self.agent_name}] Warning: No physical video found to compress. Simulating process pipeline.")
            input_video = "mock_input_video.mp4"

        # Safe dynamic bitrate calculations according to platform guidelines
        recommended_bitrate_kbps = self.calculate_optimized_bitrate(target_width, target_height, target_fps)
        target_bitrate_str = f"{recommended_bitrate_kbps}k"
        max_bitrate_str = f"{int(recommended_bitrate_kbps * 1.5)}k"
        bufsize_str = f"{recommended_bitrate_kbps * 2}k"

        print(f"[{self.agent_name}] Math Engine: Recommended target bitrate: {target_bitrate_str} (Max: {max_bitrate_str})")

        # Building advanced scale and compression command
        # -vf scale locks custom resolutions cleanly without stretching ratio
        # -b:v defines average bitrate, -maxrate and -bufsize control buffer spikes
        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-vf", f"scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264",
            "-b:v", target_bitrate_str,
            "-maxrate", max_bitrate_str,
            "-bufsize", bufsize_str,
            "-pix_fmt", "yuv420p",
            "-r", str(target_fps),
            self.output_final_video
        ]

        print(f"[{self.agent_name}] Compression Command:\n{' '.join(cmd)}")

        # Checking FFmpeg binary
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path or input_video == "mock_input_video.mp4":
            print(f"[{self.agent_name}] System test dry-run. Compression targets written to blueprint configs.")
            result_data = {
                "agent_executed": self.agent_name,
                "execution_status": "DRY_RUN_SUCCESS",
                "resolution_set": f"{target_width}x{target_height}",
                "optimized_bitrate": target_bitrate_str,
                "command_executed": " ".join(cmd),
                "output_video_path": self.output_final_video
            }
            self._save_compression_blueprint(result_data)
            return result_data

        try:
            print(f"[{self.agent_name}] Compressing streams. Executing pixel decimation and bitrate allocation passes...")
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print(f"[{self.agent_name}] Compression completed successfully!")
            
            result_data = {
                "agent_executed": self.agent_name,
                "execution_status": "SUCCESS",
                "resolution_set": f"{target_width}x{target_height}",
                "optimized_bitrate": target_bitrate_str,
                "command_executed": " ".join(cmd),
                "output_video_path": self.output_final_video
            }
            self._save_compression_blueprint(result_data)
            return result_data

        except subprocess.CalledProcessError as e:
            print(f"[{self.agent_name}] FFmpeg execution failed during scale/compression: {e.stderr}")
            failed_data = {
                "agent_executed": self.agent_name,
                "execution_status": "FAILED",
                "error_details": str(e.stderr)
            }
            self._save_compression_blueprint(failed_data)
            return failed_data

    def _save_compression_blueprint(self, data, filename="45_bitrate_compression_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Compression metrics locked in '{file_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error saving logs: {str(e)}")

if __name__ == "__main__":
    optimizer = BitrateOptimizerCompressionEngine()
    # Testing standard vertical HD (1080x1920) at 30 fps
    result = optimizer.execute_compression(target_width=1080, target_height=1920, target_fps=30.0)
    
    print("\n--- Z-NET RENDER OPTIMIZER: AGENT 45 PROCESS COMPLETE ---")
    print(f"Execution: {result['execution_status']}")
    print(f"Output Resolution: {result.get('resolution_set', 'N/A')}")
    print(f"Assigned Peak Bitrate: {result.get('optimized_bitrate', 'N/A')}")
    print(f"Saved Destination: '{result.get('output_video_path', 'N/A')}'")
    print("---------------------------------------------------------")
