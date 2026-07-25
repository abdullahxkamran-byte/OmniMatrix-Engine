import os
import sys
import json
import shutil
import time
import subprocess

# =====================================================================
# RULE 2: UNIVERSAL ENVIRONMENT CONFIGURATION (PURE UTILITY)
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

class Agent_43_Multi_Track_AV_Merger:
    """
    OMNIMATRIX V2.0 PURE UTILITY: MULTI-TRACK AUDIO-VISUAL MULTIPLEXER
    Ingests actionable FFmpeg concatenation demuxers and multi-layered audio streams.
    Executes advanced DSP audio mixing with loudness normalization to assemble
    uncompressed master intermediate video payloads.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: Pure Non-AI Naming enforcement (Agent_XX instead of Ai_Agent_XX)
        self.agent_name = "Agent_43_Multi_Track_AV_Merger"
        self.workspace_dir = workspace_dir
        self.manifest_path = os.path.join(self.workspace_dir, "42_raw_buffer_manifest.json")
        self.concat_demuxer_path = os.path.join(self.workspace_dir, "ffmpeg_concat_demuxer.txt")
        self.output_intermediate_video = os.path.join(self.workspace_dir, "43_intermediate_merged_output.mp4")
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of legacy multiplexed payloads and execution manifests."""
        for filename in ["43_merged_av_blueprint.json", "43_intermediate_merged_output.mp4"]:
            file_path = os.path.join(self.workspace_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as error:
                    self.log(f"Failed to scrub legacy file {file_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & PIPELINE ROUTING
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
            # Advance atomic handshake to Agent 44 (GPU Hardware Accelerated Encoder)
            data["orchestrator_matrix"]["next_agent"] = "Agent_44_GPU_Hardware_Accelerated_Encoder"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _verify_ffmpeg_binary(self):
        """Validates system path dependency for FFmpeg executable binary."""
        binary_path = shutil.which("ffmpeg")
        if binary_path:
            self.log(f"FFmpeg binary verified at system path: '{binary_path}'", "SUCCESS")
            return True
        self.log("CRITICAL: FFmpeg binary not detected in system environment path.", "ERROR")
        return False

    def _load_upstream_manifest(self):
        if not os.path.exists(self.manifest_path):
            self.log("Upstream buffer manifest missing. Triggering offline fallback parameters.", "WARNING")
            return None
        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as error:
            self.log(f"Manifest read exception encountered: {error}", "ERROR")
            return None

    # =====================================================================
    # DETERMINISTIC MULTIPLEX COMMAND ASSEMBLER (RULE 9 PAYOFF)
    # =====================================================================
    def _assemble_ffmpeg_command(self, manifest):
        fps = 24.0
        audio_paths = []
        
        if manifest:
            fps = float(manifest.get("target_framerate_fps", 24.0))
            audio_paths = manifest.get("mapped_audio_buffer_paths", [])

        cmd = ["ffmpeg", "-y"]

        # Rule 9 Payoff: Utilize actionable concat demuxer from Agent 42 if available
        if os.path.exists(self.concat_demuxer_path) and os.path.getsize(self.concat_demuxer_path) > 10:
            self.log(f"Ingesting actionable concat demuxer stream: '{self.concat_demuxer_path}'", "SUCCESS")
            cmd.extend(["-f", "concat", "-safe", "0", "-i", self.concat_demuxer_path])
        else:
            # Rule 10 Autonomy Fallback: Use pattern matching or synthetic test visual stream
            fallback_pattern = os.path.join(self.workspace_dir, "render_output", "frame_%04d.png")
            if os.path.exists(os.path.dirname(fallback_pattern)):
                self.log("Concat demuxer unavailable. Fallback to sequential frame pattern.", "WARNING")
                cmd.extend(["-framerate", str(fps), "-i", fallback_pattern])
            else:
                self.log("No physical visual assets found. Generating synthetic test visual input.", "WARNING")
                cmd.extend(["-f", "lavfi", "-i", f"testsrc2=size=1920x1080:rate={int(fps)}:duration=5"])

        # Map active acoustic tracks with size validation
        valid_audio_count = 0
        for audio_file in audio_paths:
            if os.path.exists(audio_file) and os.path.getsize(audio_file) > 100:
                cmd.extend(["-i", audio_file])
                valid_audio_count += 1

        # Build advanced DSP filter complex for multi-track audio mixing
        if valid_audio_count > 0:
            if valid_audio_count > 1:
                # Prevent digital clipping during multi-track mix via normalization
                filter_chain = ""
                for idx in range(1, valid_audio_count + 1):
                    filter_chain += f"[{idx}:a]"
                filter_chain += f"amix=inputs={valid_audio_count}:duration=first:dropout_transition=2,loudnorm=I=-14:TP=-1.0:LRA=11[aout]"
                
                cmd.extend(["-filter_complex", filter_chain, "-map", "0:v", "-map", "[aout]"])
            else:
                cmd.extend(["-map", "0:v", "-map", "1:a"])
        else:
            self.log("No valid audio streams mapped. Multiplexer will render visual-only payload.", "INFO")
            cmd.extend(["-map", "0:v"])

        # Intermediate master encoding parameters (High quality, low CPU overhead for next stage GPU encoding)
        cmd.extend([
            "-c:v", "libx264",
            "-preset", "superfast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            self.output_intermediate_video
        ])

        return cmd, fps

    def execute_merging(self):
        self._handshake("IN_PROGRESS")
        self.log("Initiating multi-track audio-visual assembly sequence...")
        
        is_ffmpeg_ready = self._verify_ffmpeg_binary()
        manifest = self._load_upstream_manifest()
        cmd, fps = self._assemble_ffmpeg_command(manifest)

        command_string = " ".join(cmd)
        self.log(f"Compiled Executable FFmpeg Command:\n{command_string}")

        # Dry-run execution if binary is missing from system environment
        if not is_ffmpeg_ready:
            self.log("FFmpeg binary unavailable. Recording dry-run execution blueprint.", "WARNING")
            dry_run_data = {
                "agent_executed": self.agent_name,
                "execution_timestamp": time.time(),
                "execution_status": "DRY_RUN_SUCCESS_BINARY_MISSING",
                "target_framerate_fps": fps,
                "command_assembled": command_string,
                "output_video_path": self.output_intermediate_video
            }
            self._save_blueprint(dry_run_data)
            self._handshake("COMPLETED")
            return dry_run_data

        # Rule 17: Subprocess execution with strict hardware timeout protection (10 minutes max)
        try:
            self.log("Spawning FFmpeg sub-process. Multiplexing intermediate video payload...")
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, timeout=600)
            self.log("Audio-visual multiplexing completed successfully.", "SUCCESS")
            
            output_data = {
                "agent_executed": self.agent_name,
                "execution_timestamp": time.time(),
                "execution_status": "SUCCESS",
                "target_framerate_fps": fps,
                "command_assembled": command_string,
                "output_video_path": self.output_intermediate_video
            }
            self._save_blueprint(output_data)
            self._handshake("COMPLETED")
            return output_data

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            error_msg = getattr(error, 'stderr', str(error))
            self.log(f"CRITICAL: Subprocess rendering failure or hardware timeout: {error_msg}", "ERROR")
            failed_data = {
                "agent_executed": self.agent_name,
                "execution_timestamp": time.time(),
                "execution_status": "FAILED",
                "error_details": str(error_msg),
                "command_assembled": command_string,
                "output_video_path": None
            }
            self._save_blueprint(failed_data)
            return failed_data

    def _save_blueprint(self, data, filename="43_merged_av_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log(f"Execution blueprint recorded to: '{file_path}'", "SUCCESS")
        except Exception as error:
            self.log(f"Failed to record execution blueprint: {error}", "ERROR")

if __name__ == "__main__":
    merger = Agent_43_Multi_Track_AV_Merger()
    merger.execute_merging()
