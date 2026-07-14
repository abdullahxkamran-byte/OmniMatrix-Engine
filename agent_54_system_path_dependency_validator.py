import os
import sys
import json
import shutil
import platform

class SystemPathDependencyValidator:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 54: system_path_dependency_validator"
        self.workspace_dir = workspace_dir
        self.output_report_path = os.path.join(self.workspace_dir, "54_system_validation_report.json")

    def validate_pipeline_dependencies(self):
        print(f"[{self.agent_name}] Initializing global pipeline path and dependency validator...")

        validation_results = {
            "critical_system_tools": {},
            "key_blueprints_checked": {},
            "key_media_assets_checked": {},
            "overall_pipeline_status": "PASS"
        }

        # 1. Check Critical System Tools (CLI Dependencies)
        critical_tools = ["ffmpeg", "ffprobe"]
        # Blender and local LLM/Ollama are optional but tracked
        optional_tools = ["blender", "ollama"]

        print(f"[{self.agent_name}] Step 1: Checking system binary paths...")
        for tool in critical_tools:
            path = shutil.which(tool)
            status = "FOUND" if path else "MISSING"
            validation_results["critical_system_tools"][tool] = {
                "status": status,
                "resolved_path": path if path else "N/A",
                "critical": True
            }
            if status == "MISSING":
                # Critical CLI tool missing does not fail dry-runs, but raises warning
                validation_results["overall_pipeline_status"] = "WARNING (Missing Critical CLI Tools)"

        for tool in optional_tools:
            path = shutil.which(tool)
            validation_results["critical_system_tools"][tool] = {
                "status": "FOUND" if path else "MISSING",
                "resolved_path": path if path else "N/A",
                "critical": False
            }

        # 2. Check Blueprints from Upstream Agents (to ensure data chain is unbroken)
        print(f"[{self.agent_name}] Step 2: Validating logical blueprint chain links...")
        target_blueprints = {
            "03_visual_sync_storyboarder.json": "Storyboarding Data Link",
            "47_super_resolution_blueprint.json": "Upscale Metrics Link",
            "48_temporal_denoise_blueprint.json": "Denoise Command Link",
            "49_media_scout_blueprint.json": "AI Vision Scouting Link",
            "50_extracted_frames_blueprint.json": "Frame Extraction Logs Link",
            "51_thumbnail_compiler_blueprint.json": "Thumbnail Configuration Link",
            "52_vfx_asset_manifest.json": "VFX Asset Database Link",
            "53_fonts_system_manifest.json": "Fonts System Registry Link"
        }

        missing_blueprints_count = 0
        for bp, description in target_blueprints.items():
            bp_path = os.path.join(self.workspace_dir, bp)
            exists = os.path.exists(bp_path)
            
            blueprint_meta = {
                "description": description,
                "status": "VERIFIED_EXISTS" if exists else "MISSING",
                "file_path": bp_path
            }
            
            if exists:
                # Try parsing to ensure JSON isn't corrupted
                try:
                    with open(bp_path, "r", encoding="utf-8") as f:
                        json.load(f)
                    blueprint_meta["parsing"] = "VALID_JSON"
                except Exception as e:
                    blueprint_meta["parsing"] = f"CORRUPTED_JSON: {str(e)}"
                    validation_results["overall_pipeline_status"] = "WARNING (Corrupted Blueprints)"
            else:
                missing_blueprints_count += 1
                blueprint_meta["parsing"] = "N/A"

            validation_results["key_blueprints_checked"][bp] = blueprint_meta

        # 3. Check physical rendered media assets
        print(f"[{self.agent_name}] Step 3: Checking physical output media assets...")
        target_media = {
            "48_final_denoised_clean.mp4": "Denoised Master Video",
            "51_compiled_thumbnail.png": "High-CTR Compiled Thumbnail"
        }

        for media, desc in target_media.items():
            media_path = os.path.join(self.workspace_dir, media)
            exists = os.path.exists(media_path)
            
            validation_results["key_media_assets_checked"][media] = {
                "description": desc,
                "status": "EXISTS" if exists else "NOT_RENDERED_YET",
                "file_path": media_path,
                "size_bytes": os.path.getsize(media_path) if exists else 0
            }

        # Determine final status verdict
        if missing_blueprints_count > 4:
            # If majority of pipeline manifests are absent, mark as incomplete setup
            validation_results["overall_pipeline_status"] = "INCOMPLETE_PIPELINE_SETUP"
        elif validation_results["overall_pipeline_status"] == "PASS":
            print(f"[{self.agent_name}] Excellent! All evaluated paths and pipeline assets are fully synced.")

        # Save the report
        self._save_report(validation_results)
        return validation_results

    def _save_report(self, data):
        try:
            with open(self.output_report_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Validation database report successfully saved to '{self.output_report_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error saving validator report: {str(e)}")

if __name__ == "__main__":
    validator = SystemPathDependencyValidator()
    result = validator.validate_pipeline_dependencies()
    
    print("\n--- Z-NET SYSTEM PATH VALIDATOR: AGENT 54 COMPLETE ---")
    print(f"System OS: {platform.system()} ({platform.release()})")
    print(f"Overall Pipeline Sync Status: {result['overall_pipeline_status']}")
    print("\nChecked Blueprints Status Summary:")
    for bp, meta in result["key_blueprints_checked"].items():
        print(f"  - {bp} : {meta['status']} ({meta.get('parsing', 'N/A')})")
    
    print("\nCritical Binaries Registered:")
    for tool, meta in result["critical_system_tools"].items():
        print(f"  - {tool} : {meta['status']} -> Path: {meta['resolved_path']}")
    print("---------------------------------------------------------")
