import os
import sys
import json
import base64
import urllib.request
import urllib.error

try:
    from PIL import Image, ImageDraw, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class MangaPanelVisionComprehenderColorizer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 55: manga_panel_vision_comprehender_colorizer"
        self.workspace_dir = workspace_dir
        self.input_manga_path = os.path.join(self.workspace_dir, "input_manga_panel.png")
        self.output_colorized_path = os.path.join(self.workspace_dir, "55_colorized_manga_panel.png")
        self.output_blueprint_path = os.path.join(self.workspace_dir, "55_manga_comprehend_blueprint.json")
        
        # [SECURE] Hardcoded API key removed to prevent repository secret scanning blocks.
        # Aap apni API key ko terminal me 'GEMINI_API_KEY' environment variable ke zariye set kar sakte hain.
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _ensure_input_manga_exists(self):
        if os.path.exists(self.input_manga_path):
            print(f"[{self.agent_name}] Input manga panel found.")
            return True

        print(f"[{self.agent_name}] Warning: No input manga image found. Creating a procedural mock manga panel...")
        if not PIL_AVAILABLE:
            return False

        try:
            width, height = 800, 1000
            manga_img = Image.new("RGB", (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(manga_img)

            # Draw action speed lines (Manga style)
            import math
            cx, cy = width // 2, height // 2
            for i in range(0, 360, 6):
                rad = math.radians(i)
                x = int(cx + 600 * math.cos(rad))
                y = int(cy + 600 * math.sin(rad))
                draw.line([(cx, cy), (x, y)], fill=(30, 30, 30), width=2)

            # Character silhouette
            draw.ellipse([cx - 100, cy - 100, cx + 100, cy + 100], fill=(255, 255, 255))
            draw.line([(cx, cy - 50), (cx, cy + 120)], fill=(0, 0, 0), width=10) # Body
            draw.ellipse([cx - 30, cy - 90, cx + 30, cy - 30], fill=(0, 0, 0)) # Head
            draw.line([(cx, cy - 20), (cx - 80, cy - 70)], fill=(0, 0, 0), width=7) # Arms
            draw.line([(cx, cy - 20), (cx + 80, cy - 30)], fill=(0, 0, 0), width=7)
            draw.line([(cx, cy + 120), (cx - 40, cy + 220)], fill=(0, 0, 0), width=7) # Legs
            draw.line([(cx, cy + 120), (cx + 40, cy + 220)], fill=(0, 0, 0), width=7)

            # Thick border
            draw.rectangle([10, 10, width-10, height-10], outline=(0, 0, 0), width=10)

            manga_img.save(self.input_manga_path, "PNG")
            print(f"[{self.agent_name}] Procedural anime panel fallback created at '{self.input_manga_path}'")
            return True
        except Exception as e:
            print(f"[{self.agent_name}] Fallback draw failed: {str(e)}")
            return False

    def _get_image_base64(self):
        try:
            with open(self.input_manga_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            print(f"[{self.agent_name}] Base64 conversion failed: {str(e)}")
            return None

    def comprehend_and_colorize(self):
        print(f"[{self.agent_name}] Running Real-time Gemini Vision Integration...")
        self._ensure_input_manga_exists()

        system_prompt = (
            "You are an AI Manga Specialist. Analyze this black and white manga panel and output colorization data.\n"
            "Return ONLY a clean JSON object with no markdown backticks, explanations, or notes. Format:\n"
            "{\n"
            "  \"detected_characters\": [\n"
            "    {\"name\": \"Anime Character\", \"pose_coordinates\": [300, 300, 200, 400], \"depth_estimate\": 0.85}\n"
            "  ],\n"
            "  \"segmented_elements\": [\"action_lines\", \"subject\"],\n"
            "  \"colorization_palette\": {\n"
            "    \"hair\": \"#FFCC00\",\n"
            "    \"skin\": \"#FFE0BD\",\n"
            "    \"aura\": \"#00FFFF\",\n"
            "    \"background\": \"#1A1A24\"\n"
            "  },\n"
            "  \"vfx_glow_trigger\": true\n"
            "}"
        )

        structured_data = None

        if self.gemini_api_key:
            print(f"[{self.agent_name}] Connecting to Gemini 1.5 Flash Cloud Network...")
            base64_image = self._get_image_base64()

            if base64_image:
                try:
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": system_prompt},
                                {
                                    "inlineData": {
                                        "mimeType": "image/png",
                                        "data": base64_image
                                    }
                                }
                            ]
                        }],
                        "generationConfig": {
                            "responseMimeType": "application/json"
                        }
                    }

                    data_bytes = json.dumps(payload).encode("utf-8")
                    req = urllib.request.Request(
                        self.gemini_url, 
                        data=data_bytes, 
                        headers={"Content-Type": "application/json"}
                    )

                    with urllib.request.urlopen(req, timeout=30) as response:
                        res_body = response.read().decode("utf-8")
                        raw_response = json.loads(res_body)
                        raw_text = raw_response["candidates"][0]["content"]["parts"][0]["text"]
                        structured_data = json.loads(raw_text.strip())
                        print(f"[{self.agent_name}] Success: Gemini API parsed panel correctly!")

                except Exception as e:
                    print(f"[{self.agent_name}] Cloud Error: {str(e)}. Shifting to local fallback...")
                    structured_data = self._execute_procedural_vision()
            else:
                structured_data = self._execute_procedural_vision()
        else:
            print(f"[{self.agent_name}] No API key detected in environment. Shifting to local fallback...")
            structured_data = self._execute_procedural_vision()

        # Build Blueprint
        blueprint_data = {
            "agent_executed": self.agent_name,
            "api_used": "Google Gemini Cloud Node" if self.gemini_api_key else "Procedural Fallback Engine",
            "source_manga_panel": self.input_manga_path,
            "analysis_metrics": structured_data,
            "colorized_output_file": self.output_colorized_path
        }
        
        self._save_blueprint(blueprint_data)
        self._execute_physical_colorization(structured_data)
        return blueprint_data

    def _execute_procedural_vision(self):
        return {
            "detected_characters": [
                {"name": "Hero Silhouette (Procedural)", "pose_coordinates": [250, 250, 300, 500], "depth_estimate": 0.9}
            ],
            "segmented_elements": ["manga_speed_lines", "character_torso"],
            "colorization_palette": {
                "hair": "#00FF66",      # Radioactive Green
                "skin": "#FFE5C4",      # Warm Tone
                "aura": "#FF00FF",      # Magenta Aura
                "background": "#0C0C14" # Void
            },
            "vfx_glow_trigger": True
        }

    def _execute_physical_colorization(self, vision_data):
        if not PIL_AVAILABLE or not os.path.exists(self.input_manga_path):
            return

        try:
            img = Image.open(self.input_manga_path).convert("RGBA")
            color_overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(color_overlay)
            palette = vision_data.get("colorization_palette", {})
            
            for char in vision_data.get("detected_characters", []):
                coords = char.get("pose_coordinates", [250, 250, 300, 500])
                # Neon cyan background glow
                draw.ellipse(
                    [coords[0]-40, coords[1]-40, coords[0]+coords[2]+40, coords[1]+coords[3]+40],
                    fill=(255, 0, 255, 45) # Soft magenta aura
                )
                # Skin fill tint
                draw.rectangle(
                    [coords[0], coords[1], coords[0]+coords[2], coords[1]+coords[3]],
                    fill=(0, 255, 255, 55) # Cyber cyan core tint
                )

            final_img = Image.alpha_composite(img, color_overlay).convert("RGB")
            enhancer = ImageEnhance.Contrast(final_img)
            final_img = enhancer.enhance(1.3)
            final_img.save(self.output_colorized_path, "PNG")
            print(f"[{self.agent_name}] Colored image saved to '{self.output_colorized_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Colorizer failed: {str(e)}")

    def _save_blueprint(self, data):
        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    comprehender = MangaPanelVisionComprehenderColorizer()
    comprehender.comprehend_and_colorize()
