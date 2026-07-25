import os
import sys
import json
import time
import shutil

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

class Agent_52_Local_VFX_Asset_Manager:
    """
    OMNIMATRIX V2.0 PURE UTILITY: LOCAL VFX ASSET & LIBRARY MANAGER
    Traverses local filesystem repositories to catalog video overlays, acoustic
    effects, graphic vignettes, and 3D mesh assets. Generates a unified,
    actionable JSON manifest for seamless querying by downstream Blender and FFmpeg pipelines.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: Pure Non-AI Naming enforcement (Agent_XX instead of Ai_Agent_XX)
        self.agent_name = "Agent_52_Local_VFX_Asset_Manager"
        self.workspace_dir = workspace_dir
        self.vfx_library_dir = os.path.join(self.workspace_dir, "Local_VFX_Library")
        self.output_manifest_path = os.path.join(self.workspace_dir, "52_vfx_asset_manifest.json")
        
        for directory in [self.workspace_dir, self.vfx_library_dir]:
            os.makedirs(directory, exist_ok=True)
            
        self._initialize_library_subdirectories()
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of legacy asset manifests."""
        if os.path.exists(self.output_manifest_path):
            try:
                os.remove(self.output_manifest_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy manifest {self.output_manifest_path}: {error}", "WARNING")

    def _initialize_library_subdirectories(self):
        """Creates structured subdirectories for modular asset categorization."""
        subdirectories = ["video_overlays", "sound_effects", "graphic_elements", "3d_models"]
        for subdir in subdirectories:
            os.makedirs(os.path.join(self.vfx_library_dir, subdir), exist_ok=True)

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
            # Hand off to Agent 53 (Fonts System Loader - Pure Utility)
            data["orchestrator_matrix"]["next_agent"] = "Agent_53_Fonts_System_Loader"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    # =====================================================================
    # DETERMINISTIC ASSET DISCOVERY & CATALOGING ENGINE
    # =====================================================================
    def _create_physical_fallback_placeholder(self, category, filename, content="OMNIMATRIX_PLACEHOLDER_ASSET"):
        """Rule 10: Creates physical fallback files so downstream tools never crash."""
        file_path = os.path.join(self.vfx_library_dir, category, filename)
        if not os.path.exists(file_path):
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                pass
        return file_path

    def scan_and_index_assets(self):
        self._handshake("IN_PROGRESS")
        self.log(f"Scanning local repository for production assets: '{self.vfx_library_dir}'")
        
        catalog = {
            "video_overlays": [],
            "sound_effects": [],
            "graphic_elements": [],
            "3d_models": []
        }

        extension_mapping = {
            "video_overlays": [".mp4", ".mov", ".mkv", ".webm", ".avi"],
            "sound_effects": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
            "graphic_elements": [".png", ".jpg", ".jpeg", ".webp", ".psd", ".exr"],
            "3d_models": [".blend", ".fbx", ".obj", ".gltf", ".glb", ".usd", ".abc"]
        }

        total_assets_discovered = 0
        
        # Rule 17: Traversal limit safeguard - cap indexing to prevent filesystem memory lockups
        max_items_per_category = 500

        for root, dirs, files in os.walk(self.vfx_library_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(file_path, self.vfx_library_dir).replace("\\", "/")
                extension = os.path.splitext(file_name)[1].lower()
                
                try:
                    size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 3)
                except Exception:
                    size_mb = 0.0

                assigned_category = None
                for category, extensions in extension_mapping.items():
                    if extension in extensions:
                        assigned_category = category
                        break

                if assigned_category and len(catalog[assigned_category]) < max_items_per_category:
                    catalog[assigned_category].append({
                        "asset_name": file_name,
                        "absolute_file_path": file_path,
                        "relative_library_path": relative_path,
                        "file_size_mb": size_mb,
                        "file_extension": extension
                    })
                    total_assets_discovered += 1

        # Rule 10: Offline Autonomy - Inject physical fallback placeholders if categories are unpopulated
        if total_assets_discovered == 0:
            self.log("Local repository unpopulated. Synthesizing physical fallback assets and default manifest entries.", "WARNING")
            
            fallbacks = [
                ("video_overlays", "procedural_speed_lines_4k.mp4", ".mp4", 12.4),
                ("video_overlays", "anamorphic_lens_flare_blue.mov", ".mov", 28.1),
                ("sound_effects", "heavy_impact_sub_bass_drop.wav", ".wav", 1.8),
                ("graphic_elements", "cinematic_letterbox_vignette.png", ".png", 0.5),
                ("3d_models", "impact_debris_fracture_shard.blend", ".blend", 4.2)
            ]

            for category, name, ext, mock_size in fallbacks:
                phys_path = self._create_physical_fallback_placeholder(category, name)
                catalog[category].append({
                    "asset_name": name,
                    "absolute_file_path": phys_path,
                    "relative_library_path": f"{category}/{name}",
                    "file_size_mb": mock_size,
                    "file_extension": ext
                })
                total_assets_discovered += 1

        manifest_payload = {
            "agent_executed": self.agent_name,
            "execution_timestamp": time.time(),
            "repository_root_path": self.vfx_library_dir,
            "total_indexed_assets_count": total_assets_discovered,
            "cataloged_categories": catalog
        }

        with open(self.output_manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_payload, f, indent=4)

        self.log(f"VFX library asset manifest locked: '{self.output_manifest_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return manifest_payload

if __name__ == "__main__":
    manager = Agent_52_Local_VFX_Asset_Manager()
    manager.scan_and_index_assets()
