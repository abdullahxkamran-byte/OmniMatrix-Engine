import os
import sys
import json
import time
import shutil
import platform
import importlib.util

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

class Agent_54_System_Path_Dependency_Validator:
    """
    OMNIMATRIX V2.0 PURE UTILITY: SYSTEM PATH & DEPENDENCY VALIDATOR
    Executes exhaustive cross-platform diagnostics across OS binary paths,
    Python runtime libraries, and upstream JSON blueprint continuity chains.
    Implements autonomous self-healing protocols to repair missing directory
    structures and guarantee zero-crash execution for downstream pipelines.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: Pure Non-AI Naming enforcement (Agent_XX instead of Ai_Agent_XX)
        self.agent_name = "Agent_54_System_Path_Dependency_Validator"
        self.workspace_dir = workspace_dir
        self.output_report_path = os.path.join(self.workspace_dir, "54_system_validation_report.json")
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous system validation reports."""
        if os.path.exists(self.output_report_path):
            try:
                os.remove(self.output_report_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy report {self.output_report_path}: {error}", "WARNING")

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
            # Hand off to Module H: Omni Generative Matrix (Ai Agent 55)
            data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_55_Universal_Vision_Comprehender"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    # =====================================================================
    # SYSTEM BINARY & PYTHON RUNTIME DIAGNOSTICS
    # =====================================================================
    def _validate_cli_binaries(self):
        """Verifies OS execution paths for critical production toolchains."""
        self.log("Inspecting system environment paths for CLI binary toolchains...")
        binaries_to_check = {
            "ffmpeg": {"critical": True, "description": "Audio/Video Multiplexer & Compression Engine"},
            "ffprobe": {"critical": True, "description": "Media Stream Analyzer & Metadata Inspector"},
            "blender": {"critical": False, "description": "3D Heavy Infantry & Cel-Shading Engine"},
            "git": {"critical": False, "description": "Version Control & Evolving Sync Optimizer"},
            "ollama": {"critical": False, "description": "Local LLM Fallback Reasoning Node"}
        }
        
        results = {}
        missing_critical_count = 0

        for binary, meta in binaries_to_check.items():
            resolved_path = shutil.which(binary)
            is_found = resolved_path is not None
            
            if not is_found and meta["critical"]:
                missing_critical_count += 1
                self.log(f"CRITICAL BINARY MISSING: '{binary}' ({meta['description']})", "ERROR")
            elif is_found:
                self.log(f"Verified binary '{binary}' -> '{resolved_path}'", "SUCCESS")

            results[binary] = {
                "status": "FOUND" if is_found else "MISSING",
                "resolved_path": resolved_path if resolved_path else "UNAVAILABLE",
                "is_critical": meta["critical"],
                "description": meta["description"]
            }

        return results, missing_critical_count

    def _validate_python_modules(self):
        """Tests runtime imports for mandatory Python SDKs and libraries."""
        self.log("Inspecting Python runtime environment for mandatory module dependencies...")
        modules_to_check = {
            "PIL": {"name": "Pillow", "critical": True, "description": "High-CTR Thumbnail & Canvas Compiler"},
            "google.generativeai": {"name": "Google Gemini SDK", "critical": False, "description": "Primary Cloud Reasoning Node"},
            "dotenv": {"name": "python-dotenv", "critical": False, "description": "Environment Configuration Loader"},
            "urllib.request": {"name": "urllib", "critical": True, "description": "Universal HTTP & API Communication"},
            "ssl": {"name": "ssl", "critical": True, "description": "Secure Socket Layer for Cloud Handshakes"}
        }

        results = {}
        for mod_code, meta in modules_to_check.items():
            is_installed = importlib.util.find_spec(mod_code) is not None
            if not is_installed and meta["critical"]:
                self.log(f"CRITICAL MODULE MISSING: '{meta['name']}' ({meta['description']})", "ERROR")
            elif is_installed:
                self.log(f"Verified Python module '{meta['name']}'", "SUCCESS")

            results[mod_code] = {
                "module_name": meta["name"],
                "status": "INSTALLED" if is_installed else "MISSING",
                "is_critical": meta["critical"],
                "description": meta["description"]
            }

        return results

    # =====================================================================
    # BLUEPRINT CONTINUITY & SELF-HEALING ENGINE (RULE 10)
    # =====================================================================
    def _validate_blueprint_chain(self):
        """Audits logical continuity and JSON integrity across upstream manifests."""
        self.log("Auditing upstream JSON blueprint chain continuity...")
        target_blueprints = {
            "01_omnimatrix_project_config.json": "Master Project Configuration",
            "03_visual_sync_storyboarder.json": "Storyboard Visual Cues",
            "42_raw_buffer_manifest.json": "FFmpeg Raw Buffer Manifest",
            "43_merged_av_blueprint.json": "Multi-Track AV Merger Blueprint",
            "44_gpu_acceleration_blueprint.json": "GPU Hardware Encoding Blueprint",
            "45_bitrate_compression_blueprint.json": "Bitrate Compression Blueprint",
            "46_frame_interpolation_blueprint.json": "Optical Flow Smoothness Blueprint",
            "47_super_resolution_blueprint.json": "4K Super-Resolution Blueprint",
            "48_temporal_denoise_blueprint.json": "Temporal Denoise Master Blueprint",
            "49_media_scout_blueprint.json": "Autonomous Media Scout Blueprint",
            "50_extracted_frames_blueprint.json": "High-CTR Frame Extractor Blueprint",
            "51_thumbnail_compiler_blueprint.json": "Thumbnail Canvas Blueprint",
            "52_vfx_asset_manifest.json": "Local VFX Asset Manifest",
            "53_fonts_system_manifest.json": "System Typography Manifest"
        }

        results = {}
        missing_count = 0
        corrupted_count = 0

        for filename, desc in target_blueprints.items():
            file_path = os.path.join(self.workspace_dir, filename)
            exists = os.path.exists(file_path)
            
            meta = {
                "description": desc,
                "file_path": file_path,
                "status": "EXISTS" if exists else "MISSING",
                "integrity": "UNVERIFIED"
            }

            if exists:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        json.load(f)
                    meta["integrity"] = "VALID_JSON"
                    meta["size_bytes"] = os.path.getsize(file_path)
                except Exception as error:
                    meta["integrity"] = f"CORRUPTED_JSON: {error}"
                    corrupted_count += 1
                    self.log(f"Corrupted JSON structure detected in '{filename}'", "ERROR")
            else:
                missing_count += 1
                meta["integrity"] = "N/A"
                meta["size_bytes"] = 0

            results[filename] = meta

        return results, missing_count, corrupted_count

    def _execute_self_healing_protocol(self):
        """Rule 10: Automatically repairs missing workspace directories and placeholder files."""
        self.log("Executing autonomous self-healing protocol across workspace directories...", "STATUS")
        required_directories = [
            "render_output",
            "audio_output",
            "extracted_ctr_frames",
            "Local_VFX_Library/video_overlays",
            "Local_VFX_Library/sound_effects",
            "Local_VFX_Library/graphic_elements",
            "Local_VFX_Library/3d_models",
            "Local_Fonts_Repository",
            "Local_3D_Environments"
        ]

        repaired_count = 0
        for rel_dir in required_directories:
            full_dir = os.path.join(self.workspace_dir, rel_dir)
            if not os.path.exists(full_dir):
                os.makedirs(full_dir, exist_ok=True)
                repaired_count += 1
                self.log(f"Self-Healed missing workspace directory: '{rel_dir}'", "SUCCESS")

        return repaired_count

    def execute_pipeline_validation(self):
        self._handshake("IN_PROGRESS")
        self.log("Initiating global system path and pipeline dependency verification...")

        repaired_dirs = self._execute_self_healing_protocol()
        cli_binaries, missing_cli = self._validate_cli_binaries()
        python_modules = self._validate_python_modules()
        blueprints, missing_bp, corrupted_bp = self._validate_blueprint_chain()

        # Evaluate global pipeline health verdict
        if missing_cli > 0 or corrupted_bp > 0:
            verdict = "WARNING_CRITICAL_DEPENDENCIES_MISSING_OR_CORRUPTED"
        elif missing_bp > 6:
            verdict = "INCOMPLETE_PIPELINE_SETUP_UPSTREAM_PENDING"
        else:
            verdict = "PASS_PIPELINE_FULLY_SYNCHRONIZED"

        self.log(f"Global System Diagnostic Verdict: [{verdict}]", "STATUS")

        report_payload = {
            "agent_executed": self.agent_name,
            "execution_timestamp": time.time(),
            "operating_system_environment": f"{platform.system()} ({platform.release()})",
            "global_pipeline_status": verdict,
            "self_healing_directories_repaired": repaired_dirs,
            "cli_binary_toolchains": cli_binaries,
            "python_runtime_modules": python_modules,
            "upstream_blueprint_chain": blueprints,
            "summary_metrics": {
                "missing_critical_binaries": missing_cli,
                "missing_blueprints_count": missing_bp,
                "corrupted_blueprints_count": corrupted_bp
            }
        }

        with open(self.output_report_path, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=4)

        self.log(f"System path validation report locked: '{self.output_report_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return report_payload

if __name__ == "__main__":
    validator = Agent_54_System_Path_Dependency_Validator()
    validator.execute_pipeline_validation()
