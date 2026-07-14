import os
import sys
import json
import subprocess
import shutil

class GpuHardwareAcceleratedEncoder:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 44: gpu_hardware_accelerated_encoder"
        self.workspace_dir = workspace_dir
        self.merger_blueprint_path = os.path.join(self.workspace_dir, "43_merged_av_blueprint.json")
        self.output_gpu_video = os.path.join(self.workspace_dir, "44_gpu_accelerated_output.mp4")

    def _detect_gpu_encoder(self):
        print(f"[{self.agent_name}] Scanning system hardware drivers for GPU encoder support...")
        
        # FFmpeg static help commands chalakar supported encoders check karte hain
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            print(f"[{self.agent_name}] Warning: FFmpeg not detected in path. Defaulting to CPU baseline.")
            return "libx264" # CPU standard fallback

        try:
            # Querying FFmpeg to list available video encoders
            process = subprocess.run(
                ["ffmpeg", "-encoders"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                check=True
            )
            encoders_list = process.stdout

            # Priority 1: Nvidia NVENC (Sabse fast aur high-quality)
            if "h264_nvenc" in encoders_list:
                print(f"[{self.agent_name}] NVIDIA NVENC Hardware Accelerator Detected!")
                return "h264_nvenc"
            
            # Priority 2: Intel QuickSync (QSV)
            elif "h264_qsv" in encoders_list:
                print(f"[{self.agent_name}] Intel QuickSync (QSV) Hardware Accelerator Detected!")
                return "h264_qsv"
            
            # Priority 3: AMD Advanced Media Framework (AMF)
            elif "h264_amf" in encoders_list:
                print(f"[{self.agent_name}] AMD AMF Hardware Accelerator Detected!")
                return "h264_amf"
            
            # Priority 4: Apple Silicon / macOS VideoToolbox
            elif "h264_videotoolbox" in encoders_list:
                print(f"[{self.agent_name}] macOS VideoToolbox Hardware Accelerator Detected!")
                return "h264_videotoolbox"
            
            else:
                print(f"[{self.agent_name}] No hardware encoder detected. Falling back to standard CPU [libx264].")
                return "libx264"

        except Exception as e:
            print(f"[{self.agent_name}] Driver scan exception: {str(e)}. Defaulting safely to CPU [libx264].")
            return "libx264"

    def execute_acceleration(self):
        print(f"[{self.agent_name}] Fetching upstream multiplexed streams from Agent 43...")
        
        # GPU detection run karte hain
        gpu_codec = self._detect_gpu_encoder()

        # Load dynamic merger configurations
        if not os.path.exists(self.merger_blueprint_path):
            print(f"[{self.agent_name}] Upstream blueprint missing. Constructing autonomous baseline paths.")
            base_cmd = "ffmpeg -y -framerate 24 -i znet_workspace/render_output/frame_%04d.png -c:v libx264"
        else:
            try:
                with open(self.merger_blueprint_path, "r", encoding="utf-8") as f:
                    blueprint = json.load(f)
                base_cmd = blueprint.get("command_assembled", "")
            except Exception:
                base_cmd = ""

        if not base_cmd:
            print(f"[{self.agent_name}] Blueprint command layout invalid. Setting up raw CPU encoder preset.")
            base_cmd = f"ffmpeg -y -i raw_frames -c:v libx264 {self.output_gpu_video}"

        # Dynamic command parser: Replaces standard CPU libx264 with GPU specific codec
        # Also injects high-speed GPU-presets like '-preset fast' or '-preset p4' for NVENC
        accelerated_cmd_str = base_cmd
        if gpu_codec != "libx264":
            accelerated_cmd_str = accelerated_cmd_str.replace("-c:v libx264", f"-c:v {gpu_codec}")
            
            # NVIDIA NVENC optimization preset addition
            if gpu_codec == "h264_nvenc":
                accelerated_cmd_str = accelerated_cmd_str.replace(self.output_gpu_video, f"-preset p4 -tune hq {self.output_gpu_video}")
            # AMD/Intel optimization preset addition
            elif gpu_codec in ["h264_amf", "h264_qsv"]:
                accelerated_cmd_str = accelerated_cmd_str.replace(self.output_gpu_video, f"-preset fast {self.output_gpu_video}")
        
        # Workspace video path safety override
        accelerated_cmd_str = accelerated_cmd_str.replace("43_temp_merged_output.mp4", "44_gpu_accelerated_output.mp4")
        cmd_list = accelerated_cmd_str.split()

        print(f"[{self.agent_name}] Optimized GPU Execution Command:\n{' '.join(cmd_list)}")

        # Checking binary before execution call
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            print(f"[{self.agent_name}] System testing dry-run. GPU configurations locked in workspace registry.")
            result_data = {
                "agent_executed": self.agent_name,
                "hardware_acceleration_active": gpu_codec != "libx264",
                "detected_hardware_codec": gpu_codec,
                "accelerated_command": " ".join(cmd_list),
                "output_video_path": self.output_gpu_video,
                "execution_status": "DRY_RUN_SUCCESS"
            }
            self._save_acceleration_blueprint(result_data)
            return result_data

        try:
            print(f"[{self.agent_name}] Spawning hardware process. Sending frame chunks directly to GPU video memory...")
            subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print(f"[{self.agent_name}] Hardware accelerated encode completed successfully!")
            
            result_data = {
                "agent_executed": self.agent_name,
                "hardware_acceleration_active": gpu_codec != "libx264",
                "detected_hardware_codec": gpu_codec,
                "accelerated_command": " ".join(cmd_list),
                "output_video_path": self.output_gpu_video,
                "execution_status": "SUCCESS"
            }
            self._save_acceleration_blueprint(result_data)
            return result_data

        except subprocess.CalledProcessError as e:
            print(f"[{self.agent_name}] Critical GPU Encoding Error: {e.stderr}. Triggering immediate safe CPU recovery mode...")
            
            # Fallback to standard safe CPU command
            fallback_cmd_str = base_cmd.replace("43_temp_merged_output.mp4", "44_gpu_accelerated_output.mp4")
            fallback_list = fallback_cmd_str.split()
            
            try:
                subprocess.run(fallback_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                print(f"[{self.agent_name}] Safe CPU fallback render completed successfully.")
                result_data = {
                    "agent_executed": self.agent_name,
                    "hardware_acceleration_active": False,
                    "detected_hardware_codec": "libx264 (CPU Fallback Applied)",
                    "accelerated_command": " ".join(fallback_list),
                    "output_video_path": self.output_gpu_video,
                    "execution_status": "CPU_FALLBACK_SUCCESS"
                }
                self._save_acceleration_blueprint(result_data)
                return result_data
            except Exception as ex:
                print(f"[{self.agent_name}] Absolute system failure. Render pipeline halted: {str(ex)}")
                failed_data = {
                    "agent_executed": self.agent_name,
                    "execution_status": "FAILED",
                    "error_details": str(ex)
                }
                self._save_acceleration_blueprint(failed_data)
                return failed_data

    def _save_acceleration_blueprint(self, data, filename="44_gpu_acceleration_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Accelerate blueprint saved to '{file_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing config logs: {str(e)}")

if __name__ == "__main__":
    encoder = GpuHardwareAcceleratedEncoder()
    result = encoder.execute_acceleration()
    
    print("\n--- Z-NET HARDWARE ACCELERATION: AGENT 44 PROCESS COMPLETE ---")
    print(f"Render Engine Status: {result['execution_status']}")
    print(f"Hardware Codec Selected: {result.get('detected_hardware_codec', 'N/A')}")
    print(f"Video Acceleration Active: {result.get('hardware_acceleration_active', False)}")
    print(f"Destination Path: '{result.get('output_video_path', 'N/A')}'")
    print("---------------------------------------------------------------")
