import os
import sys
import json

# Check if Pillow (PIL) is installed for real image composition
try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class ThumbnailCanvasCompiler:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 51: thumbnail_canvas_compiler"
        self.workspace_dir = workspace_dir
        self.extractor_blueprint_path = os.path.join(self.workspace_dir, "50_extracted_frames_blueprint.json")
        self.output_thumbnail_path = os.path.join(self.workspace_dir, "51_compiled_thumbnail.png")

    def _load_best_frame_path(self):
        # Agent 50 ke blueprint se sabse highest ranked ya primary thumbnail frame search karta hai
        extracted_frame = None
        
        if os.path.exists(self.extractor_blueprint_path):
            try:
                with open(self.extractor_blueprint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                metrics = data.get("extracted_frames_metrics", [])
                # Sabse pehle 'Primary Thumbnail Focus' ya highest index frame select karo
                for item in metrics:
                    if "primary" in item.get("use_case", "").lower() and item.get("status") == "SUCCESS":
                        extracted_frame = item.get("saved_path")
                        break
                
                # Fallback to any successfully extracted frame
                if not extracted_frame and metrics:
                    for item in metrics:
                        if item.get("status") == "SUCCESS":
                            extracted_frame = item.get("saved_path")
                            break
            except Exception as e:
                print(f"[{self.agent_name}] Error parsing extractor blueprint: {str(e)}")

        # Hard local file fallback logic if blueprint empty or file doesn't exist on disk
        if not extracted_frame or not os.path.exists(extracted_frame):
            # Scan directory for any .png extracted by previous module
            frames_dir = os.path.join(self.workspace_dir, "extracted_ctr_frames")
            if os.path.exists(frames_dir):
                files = [os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")]
                if files:
                    extracted_frame = files[0]

        return extracted_frame

    def compile_thumbnail(self, title_text="CLIMAX!", accent_color=(255, 0, 85)):
        # Title Text: High CTR Bold hooks (e.g. "CLIMAX!", "UNBELIEVABLE!", "GOKU 100%")
        # Accent Color: Neon Pink/Red RGB outline by default for modern anime aesthetics
        
        print(f"[{self.agent_name}] Initializing image composite compiler engine...")
        frame_path = self._load_best_frame_path()

        canvas_width = 1280
        canvas_height = 720

        # Output dynamic details
        composition_details = {
            "agent_executed": self.agent_name,
            "canvas_resolution": f"{canvas_width}x{canvas_height}",
            "base_image_used": frame_path if frame_path else "Generated Procedural Gradient Background",
            "applied_title_overlay": title_text,
            "pillow_processing": "ACTIVE" if PIL_AVAILABLE else "BYPASSED (No PIL installed)",
            "output_image_path": self.output_thumbnail_path
        }

        if not PIL_AVAILABLE:
            print(f"[{self.agent_name}] WARNING: Pillow (PIL) library missing. Please run 'pip install pillow' to enable physical drawing.")
            print(f"[{self.agent_name}] Dry-run simulation: Saving metadata configurations.")
            self._save_blueprint(composition_details)
            return composition_details

        try:
            # 1. Base Image Setup
            if frame_path and os.path.exists(frame_path):
                print(f"[{self.agent_name}] Processing base frame layer: '{frame_path}'")
                base_img = Image.open(frame_path).convert("RGBA")
                base_img = base_img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            else:
                print(f"[{self.agent_name}] Base frame not found. Generating dramatic synthwave backdrop.")
                # Procedural background: Linear gradient
                base_img = Image.new("RGBA", (canvas_width, canvas_height), (15, 15, 25, 255))
                draw = ImageDraw.Draw(base_img)
                # Create a simple vertical red-to-dark gradient
                for y in range(canvas_height):
                    r = int(15 + (y / canvas_height) * 40)
                    g = int(15 + (y / canvas_height) * 10)
                    b = int(25 + (y / canvas_height) * 50)
                    draw.line([(0, y), (canvas_width, y)], fill=(r, g, b, 255))

            # 2. Anime-style Contrast & Saturation Boost (Makes thumbnails POP!)
            enhancer_contrast = ImageEnhance.Contrast(base_img)
            base_img = enhancer_contrast.enhance(1.25) # 25% Boost contrast
            enhancer_color = ImageEnhance.Color(base_img)
            base_img = enhancer_color.enhance(1.35) # 35% Boost saturation

            # 3. Create Overlay/Draw Context
            overlay = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            # Draw vignette/shadow box at bottom & left edge to make text readable
            for y in range(canvas_height - 300, canvas_height):
                alpha = int(((y - (canvas_height - 300)) / 300) * 180) # Dynamic gradient alpha
                draw.line([(0, y), (canvas_width, y)], fill=(0, 0, 0, alpha))

            for x in range(0, 450):
                alpha = int(((450 - x) / 450) * 150)
                draw.line([(x, 0), (x, canvas_height)], fill=(0, 0, 0, alpha))

            # 4. Neon Dramatic Red/Pink Border
            border_thickness = 14
            draw.rectangle(
                [border_thickness//2, border_thickness//2, canvas_width - border_thickness//2, canvas_height - border_thickness//2],
                outline=accent_color,
                width=border_thickness
            )

            # 5. Adding High-CTR Text Layer
            # Fallback to default PIL font if custom fonts aren't loaded yet
            font = None
            font_candidates = [
                "C:/Windows/Fonts/Impact.ttf", # Standard impact font for high CTR
                "/System/Library/Fonts/Impact.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            ]
            for fc in font_candidates:
                if os.path.exists(fc):
                    try:
                        font = ImageFont.truetype(fc, 110) # Massive bold scale
                        break
                    except Exception:
                        pass
            
            if not font:
                font = ImageFont.load_default()

            # Text Position: Dynamic left-aligned center
            text_x = 60
            text_y = canvas_height - 210

            # Draw dynamic heavy drop-shadow for 3D effect
            draw.text((text_x + 6, text_y + 6), title_text, fill=(0, 0, 0, 255), font=font)
            draw.text((text_x - 3, text_y - 3), title_text, fill=(255, 255, 255, 255), font=font)
            # Accent stroke
            draw.text((text_x, text_y), title_text, fill=accent_color, font=font)

            # 6. Final Render Layer Flattening
            final_composite = Image.alpha_composite(base_img, overlay).convert("RGB")
            final_composite.save(self.output_thumbnail_path, "PNG")

            print(f"[{self.agent_name}] Thumbnail compiled & rendered successfully at '{self.output_thumbnail_path}'")
            self._save_blueprint(composition_details)
            return composition_details

        except Exception as e:
            print(f"[{self.agent_name}] Critical composite pipeline error: {str(e)}")
            composition_details["pillow_processing"] = f"FAILED: {str(e)}"
            self._save_blueprint(composition_details)
            return composition_details

    def _save_blueprint(self, data, filename="51_thumbnail_compiler_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Blueprint saved to '{file_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing compilation blueprint: {str(e)}")

if __name__ == "__main__":
    compiler = ThumbnailCanvasCompiler()
    result = compiler.compile_thumbnail(title_text="ANIME GOD MODE!", accent_color=(0, 220, 255))
    
    print("\n--- Z-NET THUMBNAIL CANVAS COMPILER: AGENT 51 COMPLETE ---")
    print(f"Pillow Integration Status: {result['pillow_processing']}")
    print(f"Final Render Output Location: '{result['output_image_path']}'")
    print("-----------------------------------------------------------")
