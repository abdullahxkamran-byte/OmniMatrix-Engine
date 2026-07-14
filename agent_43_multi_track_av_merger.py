import os
import sys
import json
import subprocess
import shutil

class MultiTrackAvMerger:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 43: multi_track_av_merger"
        self.workspace_dir = workspace_dir
        self.manifest_path = os.path.join(self.workspace_dir, "42_raw_buffer_manifest.json")
        self.output_temp_video = os.path.join(self.workspace_dir, "43_temp_merged_output.mp4")

    def _verify_ffmpeg(self):
        # System path me FFmpeg tool installed hai ya nahi, check karta hai
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            print(f"[{self.agent_name}] FFmpeg binary detected at: '{ffmpeg_path}'")
            return True
        else:
            print(f"[{self.agent_name}] CRITICAL ERROR: FFmpeg is not installed or not in system PATH.")
            return False

    def _load_manifest_data(self):
        if not os.path.exists(self.manifest_path):
            print(f"[{self.agent_name}] Warning: Buffer manifest not found. Executing raw scanning fallback.")
            return None
        
        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"[{self.agent_name}] Error reading manifest file: {str(e)}")
            return None

    def execute_merging(self):
        print(f"[{self.agent_name}] Initializing multi-track assembly stream...")
        
        # FFmpeg presence check
        ffmpeg_available = self._verify_ffmpeg()
        
        manifest = self._load_manifest_data()
        if not manifest:
            # Fallback values agar previous agent file na mili ho
            fps = 24.0
            frames_pattern = os.path.join(self.workspace_dir, "render_output", "frame_%04d.png")
            audio_paths = []
        else:
            fps = manifest.get("frame_rate_fps", 24.0)
            # Find the sequential frame pattern inside the folder automatically
            first_frame = manifest.get("frame_sequence_start", "")
            if first_frame:
                # Direct folder context se template base design (e.g. frame_%04d.png)
                dir_name = os.path.dirname(first_frame)
                frames_pattern = os.path.join(dir_name, "frame_%04d.png")
            else:
                frames_pattern = os.path.join(self.workspace_dir, "render_output", "frame_%04d.png")
            
            audio_paths = manifest.get("raw_audio_buffer_paths", [])

        # Step 1: Base command formulation
        # -y automatically overrides existing temp video
        # -framerate locks frame-perfect speed calculations
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", frames_pattern
        ]

        # Step 2: Dynamic Multi-track Audio Inputs mapping
        audio_inputs_count = 0
        for audio in audio_paths:
            if os.path.exists(audio) and os.path.getsize(audio) > 100: # checking real sizes
                cmd.extend(["-i", audio])
                audio_inputs_count += 1

        # Step 3: Complex Filter Complex for Audio Mixing
        # Agar multiple sound tracks hain toh unhe sound space me mix karte hain
        if audio_inputs_count > 0:
            if audio_inputs_count > 1:
                # Multiple tracks merging (Voice + Phonk + SFX) into stereo outputs
                filter_complex_str = ""
                for i in range(1, audio_inputs_count + 1):
                    filter_complex_str += f"[{i}:a]"
                filter_complex_str += f"amix=inputs={audio_inputs_count}:duration=first[aout]"
                
                cmd.extend([
                    "-filter_complex", filter_complex_str,
                    "-map", "0:v",
                    "-map", "[aout]"
                ])
            else:
                # Single audio direct mapping without dynamic channel mixing overhead
                cmd.extend([
                    "-map", "0:v",
                    "-map", "1:a"
                ])
        else:
            # Silent output stream rendering
            cmd.extend(["-map", "0:v"])

        # Baseline fast-encoding profiles for testing stability
        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            self.output_temp_video
        ])

        print(f"[{self.agent_name}] Constructed Assembly Command:\n{' '.join(cmd)}")

        if not ffmpeg_available:
            print(f"[{self.agent_name}] Dry-Run simulated successfully. Raw file compilation script logged in database.")
            dummy_output = {
                "agent_executed": self.agent_name,
                "execution_status": "DRY_RUN_SUCCESS (FFmpeg Missing)",
                "target_fps": fps,
                "command_assembled": " ".join(cmd),
                "output_video_path": self.output_temp_video
            }
            self._save_blueprint(dummy_output)
            return dummy_output

        # Step 4: Subprocess Execution
        try:
            print(f"[{self.agent_name}] Subprocess spawned. Compiling video multiplex passes...")
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print(f"[{self.agent_name}] Multiplex rendering finished successfully.")
            
            output_data = {
                "agent_executed": self.agent_name,
                "execution_status": "SUCCESS",
                "target_fps": fps,
                "command_assembled": " ".join(cmd),
                "output_video_path": self.output_temp_video
            }
            self._save_blueprint(output_data)
            return output_data

        except subprocess.CalledProcessError as e:
            print(f"[{self.agent_name}] Critical Render Error inside subprocess execution: {e.stderr}")
            failed_output = {
                "agent_executed": self.agent_name,
                "execution_status": "FAILED",
                "error_details": str(e.stderr),
                "command_assembled": " ".join(cmd),
                "output_video_path": None
            }
            self._save_blueprint(failed_output)
            return failed_output

    def _save_blueprint(self, data, filename="43_merged_av_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Execution blueprints recorded to '{file_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error saving logs to workspace: {str(e)}")

if __name__ == "__main__":
    merger = MultiTrackAvMerger()
    result = merger.execute_merging()
    
    print("\n--- Z-NET AUDIO-VISUAL MULTIPLEXER: AGENT 43 EXECUTION COMPLETE ---")
    print(f"Render Status: {result['execution_status']}")
    print(f"Assigned Framerate: {result.get('target_fps', 'N/A')} FPS")
    print(f"Target Destination: '{result['output_video_path']}'")
    print("-------------------------------------------------------------------")
