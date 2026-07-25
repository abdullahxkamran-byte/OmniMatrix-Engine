import os
import re
import sys
import json
import time
import random

# Attempt importing Pillow (PIL) for high-performance image manipulation
try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

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

class Agent_51_Thumbnail_Canvas_Compiler:
    """
    OMNIMATRIX V2.0 PURE UTILITY: THUMBNAIL CANVAS & CARD COMPILER
    Ingests extracted high-CTR Hero Frames. Deploys deterministic Pillow (PIL)
    image processing math to apply style-aware contrast boosts, saturation scaling,
    cinematic vignettes, neon borders, and high-impact typography overlays.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: Pure Non-AI Naming enforcement (Agent_XX instead of Ai_Agent_XX)
        self.agent_name = "Agent_51_Thumbnail_Canvas_Compiler"
        self.workspace_dir = workspace_dir
        self.extractor_manifest = os.path.join(self.workspace_dir, "50_extracted_frames_blueprint.json")
        self.output_thumbnail_path = os.path.join(self.workspace_dir, "51_compiled_master_thumbnail.png")
        self.output_blueprint_path = os.path.join(self.workspace_dir, "51_thumbnail_compiler_blueprint.json")
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of legacy thumbnail outputs and compilation manifests."""
        for filename in ["51_compiled_master_thumbnail.png", "51_thumbnail_compiler_blueprint.json"]:
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
            # Hand off to Agent 52 (Local VFX Asset Manager - Pure Utility)
            data["orchestrator_matrix"]["next_agent"] = "Agent_52_Local_VFX_Asset_Manager"
            
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
                        "title": data.get("project_title", "FINAL SHOWDOWN!"),
                        "width": min(1920, int(data.get("target_width", 1280))),
                        "height": min(1080, int(data.get("target_height", 720)))
                    }
            except Exception:
                pass
        return {"style": "realistic", "title": "FINAL SHOWDOWN!", "width": 1280, "height": 720}

    def _resolve_base_frame(self):
        """Locates the highest ranked extracted Hero Frame from Agent 50."""
        if os.path.exists(self.extractor_manifest):
            try:
                with open(self.extractor_manifest, "r", encoding="utf-8") as f:
                    data = json.load(f)
                metrics = data.get("extracted_frames_registry", [])
                
                # Prioritize primary thumbnail focused frames
                for item in metrics:
                    if "primary" in str(item.get("intended_use_case", "")).lower() and "SUCCESS" in str(item.get("execution_status", "")):
                        path = item.get("extracted_image_path")
                        if path and os.path.exists(path):
                            self.log(f"Resolved primary extracted Hero Frame: '{path}'", "SUCCESS")
                            return path
                
                # Fallback to any valid extracted frame
                for item in metrics:
                    if "SUCCESS" in str(item.get("execution_status", "")):
                        path = item.get("extracted_image_path")
                        if path and os.path.exists(path):
                            return path
            except Exception as error:
                self.log(f"Extractor manifest inquiry exception: {error}", "WARNING")

        # Scan filesystem extraction directory directly
        frames_dir = os.path.join(self.workspace_dir, "extracted_ctr_frames")
        if os.path.exists(frames_dir):
            files = [os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")]
            if files:
                self.log(f"Resolved fallback filesystem extracted frame: '{files[0]}'", "INFO")
                return files[0]

        self.log("No physical Hero Frames detected. Will synthesize procedural mathematical backdrop.", "WARNING")
        return None

    # =====================================================================
    # PROCEDURAL MATHEMATICAL BACKDROP & STYLE ENHANCER (RULE 10 & 15)
    # =====================================================================
    def _generate_procedural_backdrop(self, width, height, style):
        """Rule 10: Constructs mathematical RGB gradients if physical frames are absent."""
        base_image = Image.new("RGBA", (width, height), (15, 15, 25, 255))
        draw = ImageDraw.Draw(base_image)

        for y in range(height):
            ratio = y / float(max(1, height))
            if style == "anime":
                # Synthwave neon magenta to dark purple gradient
                r = int(25 + ratio * 180)
                g = int(15 + ratio * 20)
                b = int(60 + ratio * 140)
            else:
                # Cinematic teal to deep midnight charcoal gradient
                r = int(10 + ratio * 30)
                g = int(25 + ratio * 60)
                b = int(35 + ratio * 90)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        return base_image

    def _apply_style_enhancements(self, image, style):
        """Rule 4 & 15: Tunes contrast, color saturation, and edge sharpness mathematically."""
        if style == "anime":
            # High-octane cel-shaded vibrancy
            image = ImageEnhance.Contrast(image).enhance(1.35)
            image = ImageEnhance.Color(image).enhance(1.45)
            image = ImageEnhance.Sharpness(image).enhance(1.20)
        else:
            # Theatrical filmic depth
            image = ImageEnhance.Contrast(image).enhance(1.15)
            image = ImageEnhance.Color(image).enhance(1.05)
            image = ImageEnhance.Sharpness(image).enhance(1.08)
        return image

    def _render_typography_and_overlays(self, base_image, width, height, style, title_text):
        """Renders cinematic shadow vignettes, neon borders, and high-impact typography."""
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 1. Lower and left-edge gradient shadow boxes for text legibility
        for y in range(int(height * 0.55), height):
            alpha = int(((y - (height * 0.55)) / (height * 0.45)) * 210)
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, min(255, alpha)))

        for x in range(0, int(width * 0.4)):
            alpha = int(((int(width * 0.4) - x) / (width * 0.4)) * 160)
            draw.line([(x, 0), (x, height)], fill=(0, 0, 0, min(255, alpha)))

        # 2. Style-aware border framing
        border_thickness = max(8, int(width * 0.012))
        if style == "anime":
            accent_color = (0, 240, 255, 255) # Neon cyan
            draw.rectangle([border_thickness//2, border_thickness//2, width - border_thickness//2, height - border_thickness//2], outline=accent_color, width=border_thickness)
        else:
            accent_color = (255, 215, 0, 255) # Cinematic gold
            # Letterbox top and bottom bars for widescreen theatrical feel
            bar_height = int(height * 0.06)
            draw.rectangle([0, 0, width, bar_height], fill=(5, 5, 5, 255))
            draw.rectangle([0, height - bar_height, width, height], fill=(5, 5, 5, 255))

        # 3. Typography loading with system font discovery
        font = None
        font_size = max(48, int(height * 0.14))
        font_candidates = [
            "C:/Windows/Fonts/Impact.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "/System/Library/Fonts/Supplemental/Impact.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ]
        
        for candidate in font_candidates:
            if os.path.exists(candidate):
                try:
                    font = ImageFont.truetype(candidate, font_size)
                    break
                except Exception:
                    pass
        
        if not font:
            font = ImageFont.load_default()

        # 4. Text positioning and 3D drop-shadow rendering
        text_x = int(width * 0.05)
        text_y = int(height * 0.76)
        
        # Heavy black drop shadow
        draw.text((text_x + 5, text_y + 5), title_text, fill=(0, 0, 0, 255), font=font)
        # White inner stroke
        draw.text((text_x - 2, text_y - 2), title_text, fill=(255, 255, 255, 255), font=font)
        # Master colored fill
        draw.text((text_x, text_y), title_text, fill=accent_color, font=font)

        return Image.alpha_composite(base_image.convert("RGBA"), overlay).convert("RGB")

    def execute_compilation(self, override_title=None):
        self._handshake("IN_PROGRESS")
        self.log("Initiating thumbnail canvas compilation and overlay rendering...")

        config = self._load_config()
        width, height = config["width"], config["height"]
        style = config["style"]
        title_text = override_title if override_title else config["title"]

        self.log(f"Canvas Profile Mapped: {width}x{height} | Aesthetic: {style.upper()} | Title: '{title_text}'")

        if not PIL_AVAILABLE:
            self.log("CRITICAL: Pillow (PIL) library absent from python environment. Recording dry-run blueprint.", "WARNING")
            dry_run_data = {
                "agent_executed": self.agent_name,
                "execution_timestamp": time.time(),
                "execution_status": "DRY_RUN_SUCCESS_PIL_MISSING",
                "canvas_dimensions": f"{width}x{height}",
                "style_enforced": style,
                "title_rendered": title_text,
                "output_image_path": self.output_thumbnail_path
            }
            self._save_blueprint(dry_run_data)
            self._handshake("COMPLETED")
            return dry_run_data

        try:
            frame_path = self._resolve_base_frame()
            if frame_path and os.path.exists(frame_path):
                self.log(f"Ingesting physical base frame: '{frame_path}'")
                base_img = Image.open(frame_path).convert("RGBA")
                base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)
            else:
                self.log("Synthesizing procedural mathematical gradient backdrop.")
                base_img = self._generate_procedural_backdrop(width, height, style)

            enhanced_img = self._apply_style_enhancements(base_img, style)
            master_thumbnail = self._render_typography_and_overlays(enhanced_img, width, height, style, title_text)
            
            master_thumbnail.save(self.output_thumbnail_path, "PNG")
            self.log(f"Master promotional thumbnail compiled successfully -> '{self.output_thumbnail_path}'", "SUCCESS")

            output_data = {
                "agent_executed": self.agent_name,
                "execution_timestamp": time.time(),
                "execution_status": "SUCCESS",
                "canvas_dimensions": f"{width}x{height}",
                "style_enforced": style,
                "base_frame_referenced": frame_path if frame_path else "SYNTHETIC_PROCEDURAL_GRADIENT",
                "title_rendered": title_text,
                "output_image_path": self.output_thumbnail_path
            }
            self._save_blueprint(output_data)
            self._handshake("COMPLETED")
            return output_data

        except Exception as error:
            self.log(f"CRITICAL: Thumbnail compilation exception encountered: {error}", "ERROR")
            failed_data = {
                "agent_executed": self.agent_name,
                "execution_timestamp": time.time(),
                "execution_status": "FAILED",
                "error_details": str(error),
                "output_image_path": None
            }
            self._save_blueprint(failed_data)
            return failed_data

    def _save_blueprint(self, data, filename="51_thumbnail_compiler_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log(f"Compilation blueprint locked: '{file_path}'", "SUCCESS")
        except Exception as error:
            self.log(f"Failed to record compilation blueprint: {error}", "ERROR")

if __name__ == "__main__":
    compiler = Agent_51_Thumbnail_Canvas_Compiler()
    compiler.execute_compilation()
