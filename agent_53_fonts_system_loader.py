import os
import sys
import json
import time
import shutil
import platform

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

class Agent_53_Fonts_System_Loader:
    """
    OMNIMATRIX V2.0 PURE UTILITY: SYSTEM FONTS LOADER & TYPOGRAPHY INDEXER
    Traverses cross-platform operating system font repositories (Windows, macOS, Linux).
    Classifies typefaces into production-ready aesthetic categories (High-CTR, Anime Display,
    Cinematic Serif, Cyberpunk Tech) and enforces I/O memory caps to generate a unified,
    actionable typography manifest for downstream rendering engines.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: Pure Non-AI Naming enforcement (Agent_XX instead of Ai_Agent_XX)
        self.agent_name = "Agent_53_Fonts_System_Loader"
        self.workspace_dir = workspace_dir
        self.local_fonts_dir = os.path.join(self.workspace_dir, "Local_Fonts_Repository")
        self.output_manifest_path = os.path.join(self.workspace_dir, "53_fonts_system_manifest.json")
        
        for directory in [self.workspace_dir, self.local_fonts_dir]:
            os.makedirs(directory, exist_ok=True)
            
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous font registries and manifests."""
        if os.path.exists(self.output_manifest_path):
            try:
                os.remove(self.output_manifest_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy manifest {self.output_manifest_path}: {error}", "WARNING")

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
            # Hand off to Agent 54 (System Path & Dependency Validator - Pure Utility)
            data["orchestrator_matrix"]["next_agent"] = "Agent_54_System_Path_Dependency_Validator"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    # =====================================================================
    # CROSS-PLATFORM REPOSITORY DISCOVERY ENGINE
    # =====================================================================
    def _get_os_font_directories(self):
        """Resolves standard typography directories across Windows, macOS, and Linux."""
        current_os = platform.system().lower()
        directories = []

        if current_os == "windows":
            windir = os.environ.get("WINDIR", "C:\\Windows")
            directories.append(os.path.join(windir, "Fonts"))
            local_app_data = os.environ.get("LOCALAPPDATA", "")
            if local_app_data:
                directories.append(os.path.join(local_app_data, "Microsoft", "Windows", "Fonts"))

        elif current_os == "darwin":
            directories.extend([
                "/Library/Fonts",
                "/System/Library/Fonts",
                "/System/Library/Fonts/Supplemental",
                os.path.expanduser("~/Library/Fonts")
            ])

        else:
            # Linux and Docker container standard paths
            directories.extend([
                "/usr/share/fonts",
                "/usr/local/share/fonts",
                os.path.expanduser("~/.local/share/fonts"),
                os.path.expanduser("~/.fonts")
            ])

        # Always include project local workspace repository
        directories.append(self.local_fonts_dir)
        return [d for d in directories if os.path.exists(d)]

    # =====================================================================
    # STYLE-AWARE TYPOGRAPHY CLASSIFICATION (RULE 4 & 15)
    # =====================================================================
    def _classify_font_style(self, font_name):
        """Mathematically maps typefaces into aesthetic production categories."""
        name_lower = font_name.lower().replace(" ", "_").replace("-", "_")
        
        categories = []
        
        # Category 1: High-CTR YouTube/TikTok Impact Typefaces
        if any(k in name_lower for k in ["impact", "bebas", "montserrat", "gotham", "black", "heavy", "bold", "anton"]):
            categories.append("high_ctr_impact")
            
        # Category 2: Anime & Manga Action Typefaces
        if any(k in name_lower for k in ["bangers", "komika", "manga", "anime", "brush", "marker", "ninja", "samurai", "action"]):
            categories.append("anime_styled_display")
            
        # Category 3: Realistic Cinematic & Theatrical Serifs
        if any(k in name_lower for k in ["trajan", "garamond", "bodoni", "cinzel", "serif", "times", "georgia", "baskerville", "classic"]):
            categories.append("cinematic_theatrical")
            
        # Category 4: Cyberpunk & Sci-Fi Monospace Tech Typefaces
        if any(k in name_lower for k in ["console", "courier", "mono", "tech", "digital", "pixel", "cyber", "code", "matrix"]):
            categories.append("cyberpunk_tech")
            
        # Category 5: Clean Modern Minimalist Sans-Serifs
        if any(k in name_lower for k in ["arial", "helvetica", "roboto", "open_sans", "lato", "futura", "segoe", "tahoma"]):
            categories.append("modern_minimalist")
            
        if not categories:
            categories.append("general_purpose")
            
        return categories

    # =====================================================================
    # DETERMINISTIC FONT SCANNING & INDEXING ENGINE
    # =====================================================================
    def _create_physical_fallback_font(self, font_name):
        """Rule 10: Synthesizes physical placeholder TTF files to prevent downstream crash."""
        fallback_path = os.path.join(self.local_fonts_dir, f"{font_name}.ttf")
        if not os.path.exists(fallback_path):
            try:
                with open(fallback_path, "wb") as f:
                    # Write minimal binary signature to simulate TTF structure
                    f.write(b"\x00\x01\x00\x00\x00\x00OMNIMATRIX_FONT_PLACEHOLDER")
            except Exception:
                pass
        return fallback_path

    def scan_and_load_fonts(self):
        self._handshake("IN_PROGRESS")
        self.log("Initiating cross-platform system fonts discovery and style indexing...")
        
        font_dirs = self._get_os_font_directories()
        self.log(f"Active repositories identified for traversal: {len(font_dirs)} directories.")
        
        registered_fonts = {}
        category_counts = {
            "high_ctr_impact": 0,
            "anime_styled_display": 0,
            "cinematic_theatrical": 0,
            "cyberpunk_tech": 0,
            "modern_minimalist": 0,
            "general_purpose": 0
        }
        
        # Rule 17: I/O and memory safeguard - cap indexing at 800 fonts to prevent JSON manifest bloat
        max_fonts_to_index = 800
        total_fonts_indexed = 0

        for directory in font_dirs:
            if total_fonts_indexed >= max_fonts_to_index:
                self.log(f"Rule 17 Safeguard: Indexing ceiling ({max_fonts_to_index}) reached. Terminating traversal safely.", "WARNING")
                break
                
            for root, dirs, files in os.walk(directory):
                if total_fonts_indexed >= max_fonts_to_index:
                    break
                    
                for file_name in files:
                    if total_fonts_indexed >= max_fonts_to_index:
                        break
                        
                    extension = os.path.splitext(file_name)[1].lower()
                    if extension in [".ttf", ".otf", ".woff", ".woff2"]:
                        font_family = os.path.splitext(file_name)[0]
                        absolute_path = os.path.join(root, file_name).replace("\\", "/")
                        
                        try:
                            size_kb = round(os.path.getsize(absolute_path) / 1024.0, 2)
                        except Exception:
                            size_kb = 0.0

                        style_categories = self._classify_font_style(font_family)
                        
                        registered_fonts[font_family] = {
                            "font_family_name": font_family,
                            "file_name": file_name,
                            "absolute_file_path": absolute_path,
                            "file_extension": extension,
                            "file_size_kb": size_kb,
                            "production_style_categories": style_categories,
                            "is_high_ctr_recommended": "high_ctr_impact" in style_categories
                        }
                        
                        for cat in style_categories:
                            if cat in category_counts:
                                category_counts[cat] += 1
                                
                        total_fonts_indexed += 1

        # Rule 10: 100% Offline Autonomy - Inject physical fallbacks if system repositories are unpopulated
        if total_fonts_indexed == 0:
            self.log("No system fonts detected. Synthesizing physical fallback typefaces and default registry.", "WARNING")
            
            fallbacks = [
                ("Impact_Omni", ["high_ctr_impact", "modern_minimalist"]),
                ("Bangers_Omni", ["anime_styled_display", "high_ctr_impact"]),
                ("Cinzel_Omni", ["cinematic_theatrical"]),
                ("CyberMono_Omni", ["cyberpunk_tech"]),
                ("Arial_Omni", ["modern_minimalist", "general_purpose"])
            ]
            
            for name, cats in fallbacks:
                phys_path = self._create_physical_fallback_font(name)
                registered_fonts[name] = {
                    "font_family_name": name,
                    "file_name": f"{name}.ttf",
                    "absolute_file_path": phys_path.replace("\\", "/"),
                    "file_extension": ".ttf",
                    "file_size_kb": 1.0,
                    "production_style_categories": cats,
                    "is_high_ctr_recommended": "high_ctr_impact" in cats
                }
                for c in cats:
                    if c in category_counts:
                        category_counts[c] += 1
                total_fonts_indexed += 1

        manifest_payload = {
            "agent_executed": self.agent_name,
            "execution_timestamp": time.time(),
            "operating_system_environment": platform.system(),
            "traversed_directories": font_dirs,
            "total_fonts_cataloged": total_fonts_indexed,
            "style_category_distribution": category_counts,
            "typography_database": registered_fonts
        }

        with open(self.output_manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_payload, f, indent=4)

        self.log(f"Typography system manifest locked: '{self.output_manifest_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return manifest_payload

if __name__ == "__main__":
    loader = Agent_53_Fonts_System_Loader()
    loader.scan_and_load_fonts()
