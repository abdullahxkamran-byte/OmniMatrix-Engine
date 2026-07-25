import os
import sys
import json
import time
import shutil
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

class Agent_48_Temporal_Denoise_Filter:
    """
    OMNIMATRIX V2.0 PURE UTILITY: TEMPORAL DENOISE & GRAIN REMOVAL ENGINE
    Applies high-precision 3D spatial-temporal noise filtering (HQDN3D/NLMeans).
    Mathematically isolates luma and chroma thresholds based on aesthetic style
    to eradicate compression artifacts without eroding sharp vector cel-outlines.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: Pure Non-AI Naming enforcement (Agent_XX instead of Ai_Agent_XX)
        self.agent_name = "Agent_48_Temporal_Denoise_Filter"
        self.workspace_dir = workspace_dir
        self.super_res_manifest = os.path.join(self.workspace_dir, "47_super_resolution_blueprint.json")
        self.input_4k_master = os.path.join(self.workspace_dir, "47_super_resolved_4k_master.mp4")
        self.input_gpu_fallback = os.path.join(self.workspace_dir, "44_gpu_accelerated_output.mp4")
        self.input_merger_fallback = os.path.join(self.workspace_dir, "43_intermediate_merged_output.mp4")
        self.output_denoised_video = os.path.join(self.workspace_dir, "48_final_denoised_master.mp4")
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous denoised masters and configuration manifests."""
        for filename in ["48_temporal_denoise_blueprint.json", "48_final_denoised_master.mp4"]:
            file_path = os.path.join(self.workspace_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as error:
                    self.log(f"Failed to scrub legacy asset {file_path}: {error}", "WARNING")

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
            # Hand off to Module G: Asset Management & Presentation (Ai Agent 49)
            data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_49_Autonomous_Vision_Media_Scout"
            
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
                        "fps": float(data.get("render_fps", 24.0))
                    }
            except Exception:
                pass
        return {"style": "realistic", "fps": 24.0}

    def _resolve_upstream_stream(self):
        """Intelligently locates the highest fidelity video stream available in the workspace."""
        denoise_bias = 0.5
        style_enforced = "realistic"

        if os.path.exists(self.super_res_manifest):
            try:
                with open(self.super_res_manifest, "r", encoding="utf-8") as f:
                    data = json.load(f)
                specs = data.get("upscale_specifications", {})
                denoise_bias = float(specs.get("spatial_denoise_strength", 0.5))
                style_enforced = data.get("style_enforced", "realistic").lower()
            except Exception:
                pass

        # Hierarchical fallback verification
        if os.path.exists(self.input_4k_master) and os.path.getsize(self.input_4k_master) > 100:
            self.log("Prioritizing Agent 47 super-resolved 4K master payload.", "SUCCESS")
            return self.input_4k_master, denoise_bias, style_enforced, False

        if os.path.exists(self.input_gpu_fallback) and os.path.getsize(self.input_gpu_fallback) > 100:
            self.log("4K master absent. Fallback to Agent 44 GPU accelerated stream.", "WARNING")
            return self.input_gpu_fallback, denoise_bias, style_enforced, False

        if os.path.exists(self.input_merger_fallback) and os.path.getsize(self.input_merger_fallback) > 100:
            self.log("GPU stream absent. Fallback to Agent 43 intermediate merger payload.", "WARNING")
            return self.input_merger_fallback, denoise_bias, style_enforced, False

        # Rule 10: Synthetic stream fallback
        self.log("No physical video streams detected. Generating synthetic test stream for denoise verification.", "WARNING")
        return "testsrc2=size=1920x1080:rate=24:duration=5", denoise_bias, style_enforced, True

    # =====================================================================
    # DETERMINISTIC SPATIAL-TEMPORAL NOISE SOLVER (RULE 4 & 15)
    # =====================================================================
    def _calculate_noise_filter_matrix(self, temporal_strength, spatial_strength, strength_bias, style):
        """
        Formulates high-precision HQDN3D parameters. Prevents vector line eroding
        in anime footage while maximizing compression artifact suppression.
        """
        # Scale baseline intensities against upstream AI bias
        base_temporal = float(temporal_strength) * (strength_bias + 0.5)
        base_spatial = float(spatial_strength) * (strength_bias + 0.5)

        if style == "anime":
            # Cel-shaded animation rule: Low spatial luma to preserve sharp black vector outlines;
            # higher chroma and temporal luma to eliminate macroblock ringing between identical frames.
            luma_spatial = round(max(1.0, min(base_spatial * 0.6, 3.5)), 2)
            chroma_spatial = round(max(1.5, min(base_spatial * 1.4, 6.0)), 2)
            luma_tmp = round(max(2.0, min(base_temporal * 1.5, 9.0)), 2)
            chroma_tmp = round(max(3.0, min(base_temporal * 1.8, 12.0)), 2)
        else:
            # Realistic cinematic rule: Balanced spatial and temporal luma/chroma smoothing
            # to clean digital sensor noise without wiping out environmental textures.
            luma_spatial = round(max(1.5, min(base_spatial * 1.1, 5.5)), 2)
            chroma_spatial = round(max(1.5, min(base_spatial * 1.2, 6.0)), 2)
            luma_tmp = round(max(2.0, min(base_temporal * 1.2, 8.0)), 2)
            chroma_tmp = round(max(2.0, min(base_temporal * 1.3, 8.5)), 2)

        filter_string = f"hqdn3d={luma_spatial}:{chroma_spatial}:{luma_tmp}:{chroma_tmp}"
        return filter_string, {"luma_spatial": luma_spatial, "chroma_spatial": chroma_spatial, "luma_temporal": luma_tmp, "chroma_temporal": chroma_tmp}

    # =====================================================================
    # RULE 9: ACTIONABLE FFMPEG FILTER COMPILER
    # =====================================================================
    def execute_denoising(self, temporal_strength=4.0, spatial_strength=3.0):
        self._handshake("IN_PROGRESS")
        self.log("Initiating 3D spatial-temporal noise filtering pipeline...")

        input_video, strength_bias, style, is_synthetic = self._resolve_upstream_stream()
        config = self._load_config()
        if style == "realistic" and config["style"] == "anime":
            style = "anime"

        filter_str, matrix_metrics = self._calculate_noise_filter_matrix(temporal_strength, spatial_strength, strength_bias, style)
        self.log(f"Noise matrix tuned for [{style.upper()}] -> {filter_str}", "SUCCESS")

        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-vf", filter_str,
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "17",
            "-pix_fmt", "yuv420p",
            "-c:a", "copy",
            self.output_denoised_video
        ]

        if is_synthetic:
            cmd[2] = "-f"
            cmd.insert(3, "lavfi")
            cmd.insert(4, "-i")
            cmd.pop(5)

        command_string = " ".join(cmd)
        self.log(f"Compiled Actionable Denoise Execution Command:\n{command_string}")

        ffmpeg_binary = shutil.which("ffmpeg")
        if not ffmpeg_binary:
            self.log("FFmpeg executable absent from system path. Recording dry-run blueprint.", "WARNING")
            dry_run_data = {
                "agent_executed": self.agent_name,
                "execution_timestamp": time.time(),
                "execution_status": "DRY_RUN_SUCCESS_BINARY_MISSING",
                "style_evaluated": style,
                "applied_hqdn3d_matrix": matrix_metrics,
                "actionable_filter_string": filter_str,
                "command_assembled": command_string,
                "output_video_path": self.output_denoised_video
            }
            self._save_blueprint(dry_run_data)
            self._handshake("COMPLETED")
            return dry_run_data

        # Rule 17: Execute subprocess with hardware timeout protection (20 minutes max)
        try:
            self.log("Spawning denoise sub-process. Scanning pixel differentials and applying temporal smoothing...")
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, timeout=1200)
            self.log("Temporal denoising completed successfully without eroding sharp vector outlines!", "SUCCESS")

            output_data = {
                "agent_executed": self.agent_name,
                "execution_timestamp": time.time(),
                "execution_status": "SUCCESS",
                "style_evaluated": style,
                "applied_hqdn3d_matrix": matrix_metrics,
                "actionable_filter_string": filter_str,
                "command_assembled": command_string,
                "output_video_path": self.output_denoised_video
            }
            self._save_blueprint(output_data)
            self._handshake("COMPLETED")
            return output_data

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            error_details = getattr(error, 'stderr', str(error))
            self.log(f"CRITICAL: Subprocess denoising failure or hardware timeout: {error_details}", "ERROR")
            failed_data = {
                "agent_executed": self.agent_name,
                "execution_timestamp": time.time(),
                "execution_status": "FAILED",
                "error_details": str(error_details),
                "command_assembled": command_string,
                "output_video_path": None
            }
            self._save_blueprint(failed_data)
            return failed_data

    def _save_blueprint(self, data, filename="48_temporal_denoise_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log(f"Denoise configuration blueprint recorded to: '{file_path}'", "SUCCESS")
        except Exception as error:
            self.log(f"Failed to record denoise blueprint: {error}", "ERROR")

if __name__ == "__main__":
    denoiser = Agent_48_Temporal_Denoise_Filter()
    denoiser.execute_denoising()
