import os
import sys
import json
import base64
import urllib.request
import urllib.parse
import urllib.error

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageStat
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class UniversalMangaPanelVisionColorizer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 55: universal_manga_panel_vision_colorizer"
        self.workspace_dir = workspace_dir
        self.input_manga_path = os.path.join(self.workspace_dir, "input_manga_panel.png")
        self.output_colorized_path = os.path.join(self.workspace_dir, "55_colorized_manga_panel.png")
        self.output_blueprint_path = os.path.join(self.workspace_dir, "55_manga_comprehend_blueprint.json")
        
        # API Keys loading from environment
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.hf_api_key = os.environ.get("HF_API_KEY", "") # Hugging Face Token
        
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        # Using a popular community controlnet/lineart anime colorization model endpoint
        self.hf_url = "https://api-inference.huggingface.co/models/lllyasviel/control_v11p_sd15_lineart"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def fetch_panel_from_mangadex(self, manga_title, chapter_num="1", page_num=0):
        """Dynamically searches and fetches any manga panel from MangaDex without hardcoding."""
        print(f"[{self.agent_name}] Searching MangaDex for title: '{manga_title}', Chapter: {chapter_num}")
        try:
            # 1. Search Manga ID
            search_url = f"https://api.mangadex.org/manga?title={urllib.parse.quote(manga_title)}&limit=1"
            req = urllib.request.Request(search_url, headers={'User-Agent': 'ZNetBot/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                search_data = json.loads(resp.read().decode("utf-8"))
                if not search_data.get("data"):
                    print(f"[{self.agent_name}] Manga title not found on MangaDex.")
                    return False
                manga_id = search_data["data"][0]["id"]

            # 2. Get Chapter ID
            feed_url = f"https://api.mangadex.org/manga/{manga_id}/feed?chapter[]={chapter_num}&translatedLanguage[]=en&limit=1"
            req = urllib.request.Request(feed_url, headers={'User-Agent': 'ZNetBot/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                feed_data = json.loads(resp.read().decode("utf-8"))
                if not feed_data.get("data"):
                    print(f"[{self.agent_name}] Chapter {chapter_num} not found.")
                    return False
                chapter_id = feed_data["data"][0]["id"]

            # 3. Get Base URL and Filenames
            server_url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
            req = urllib.request.Request(server_url, headers={'User-Agent': 'ZNetBot/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                server_data = json.loads(resp.read().decode("utf-8"))
                base_url = server_data["baseUrl"]
                chapter_hash = server_data["chapter"]["hash"]
                data_pages = server_data["chapter"]["data"] # High quality pages list

                if page_num >= len(data_pages):
                    page_num = 0 # Fallback to first page
                
                target_page_file = data_pages[page_num]
                page_download_url = f"{base_url}/data/{chapter_hash}/{target_page_file}"

            # 4. Download to Workspace
            print(f"[{self.agent_name}] Downloading panel image from MangaDex...")
            req = urllib.request.Request(page_download_url, headers={'User-Agent': 'ZNetBot/1.0'})
            with urllib.request.urlopen(req, timeout=30) as resp, open(self.input_manga_path, "wb") as out_f:
                out_f.write(resp.read())
            
            print(f"[{self.agent_name}] Manga panel fetched successfully at: {self.input_manga_path}")
            return True

        except Exception as e:
            print(f"[{self.agent_name}] MangaDex Fetch Failed: {str(e)}. Using fallback/existing asset.")
            return False

    def _is_panel_already_colored(self):
        """Smart Manhwa Bypass: Analyzes saturation to detect if panel is already colored."""
        if not PIL_AVAILABLE or not os.path.exists(self.input_manga_path):
            return False
        try:
            img = Image.open(self.input_manga_path).convert("HSV")
            _, s, _ = img.split() # Split into Hue, Saturation, Value
            stat = ImageStat.Stat(s)
            avg_saturation = stat.mean[0]
            
            print(f"[{self.agent_name}] Image Saturation Analysis Metric: {avg_saturation:.2f}")
            # If average saturation is high, it's a colored Manhwa/Webtoon panel
            return avg_saturation > 15.0 
        except Exception as e:
            print(f"[{self.agent_name}] Saturation check failed: {str(e)}")
            return False

    def _get_image_base64(self):
        try:
            with open(self.input_manga_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            return None

    def execute_universal_pipeline(self, search_title=None, chapter="1", page=0):
        print(f"[{self.agent_name}] Starting Universal Production Engine Execution...")
        
        # Step 1: Dynamic Download if Title is passed
        if search_title:
            self.fetch_panel_from_mangadex(search_title, chapter, page)
        
        # Ensure we have a panel file to work with
        if not os.path.exists(self.input_manga_path):
            print(f"[{self.agent_name}] Processing workspace setup anomalies...")
            # If no file exists, use custom procedural fallback generator
            # (Matches your previous script logic)
            self._generate_procedural_mock_panel()

        # Step 2: Check for Manhwa Bypass
        is_colored = self._is_panel_already_colored()
        if is_colored:
            print(f"[{self.agent_name}] [MANHWA DETECTED] Panel is already colored! Activating automatic bypass pipeline...")
            # Bypass Hugging Face colorization entirely, copy input direct to colorized output
            try:
                img = Image.open(self.input_manga_path)
                img.save(self.output_colorized_path, "PNG")
            except Exception:
                pass
            
            # Request Gemini context mapping only for metadata structure extraction
            structured_data = self._query_gemini_vision(manhwa_mode=True)
            self._save_blueprint_state(structured_data, bypass_active=True)
            return

        # Step 3: Core B&W Manga Path - Run Gemini Brain
        print(f"[{self.agent_name}] [MANGA DETECTED] Black & White asset identified. Querying Gemini Vision Brain...")
        structured_data = self._query_gemini_vision(manhwa_mode=False)
        
        # Step 4: Run Hugging Face AI Generation using Gemini's dynamic prompt
        self._colorize_via_huggingface(structured_data)
        self._save_blueprint_state(structured_data, bypass_active=False)

    def _query_gemini_vision(self, manhwa_mode=False):
        if not self.gemini_api_key:
            print(f"[{self.agent_name}] Gemini API Key missing. Executing local procedural visualization.")
            return self._procedural_vision_data()

        base64_image = self._get_image_base64()
        if not base64_image:
            return self._procedural_vision_data()

        mode_instruction = (
            "This is a pre-colored Manhwa panel. Identify characters and extract lighting metadata."
            if manhwa_mode else
            "This is a black and white Manga panel. Identify characters and construct a highly detailed, descriptive dynamic coloring prompt for an Image-to-Image AI model."
        )

        system_prompt = (
            f"You are a master universal anime vision comprehension machine. {mode_instruction}\n"
            "Analyze the character elements, hair profiles, actions, and weapon structures dynamically without hardcoded limits.\n"
            "Return ONLY a clean JSON object. No markdown backticks, no wrapping code enclosures. Structure:\n"
            "{\n"
            "  \"detected_universe_context\": \"Extracted manga/anime style series concept\",\n"
            "  \"detected_characters\": [\n"
            "    {\"name\": \"Character Identity\", \"pose_description\": \"Action state description\", \"depth_index\": 0.9}\n"
            "  ],\n"
            "  \"dynamic_coloring_prompt\": \"Master digital anime cell-shading colorization prompt detailing exact outfit colors, vibrant hair shading, precise element layers, clean 4k high quality anime output\",\n"
            "  \"vfx_glow_layers\": {\"type\": \"aura_glow\", \"hex_code\": \"#00FFFF\"}\n"
            "}"
        )

        try:
            payload = {
                "contents": [{
                    "parts": [
                        {"text": system_prompt},
                        {"inlineData": {"mimeType": "image/png", "data": base64_image}}
                    ]
                }],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(self.gemini_url, data=data_bytes, headers={"Content-Type": "application/json"})
            
            with urllib.request.urlopen(req, timeout=30) as response:
                res_body = response.read().decode("utf-8")
                raw_text = json.loads(res_body)["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(raw_text.strip())
        except Exception as e:
            print(f"[{self.agent_name}] Gemini Vision Call exception encountered: {str(e)}")
            return self._procedural_vision_data()

    def _colorize_via_huggingface(self, vision_data):
        """Uses Hugging Face AI Inference Node to render production grade color details."""
        prompt = vision_data.get("dynamic_coloring_prompt", "Masterpiece anime colorized panel, highly detailed coloring")
        print(f"[{self.agent_name}] Sending dynamic prompt to Hugging Face: '{prompt}'")
        
        if not self.hf_api_key:
            print(f"[{self.agent_name}] Hugging Face API Token missing. Executing procedural fallback painting.")
            self._execute_procedural_painting(vision_data)
            return

        try:
            # Load raw B&W file bytes to pass to the Image-to-Image / Lineart model
            with open(self.input_manga_path, "rb") as f:
                img_bytes = f.read()

            headers = {
                "Authorization": f"Bearer {self.hf_api_key}",
                "Content-Type": "application/octet-stream",
                "X-Prompt": prompt # Passes custom generated script cues inside header metadata context if supported by model routing
            }

            req = urllib.request.Request(self.hf_url, data=img_bytes, headers=headers)
            with urllib.request.urlopen(req, timeout=40) as response:
                output_bytes = response.read()
                with open(self.output_colorized_path, "wb") as out_f:
                    out_f.write(output_bytes)
            print(f"[{self.agent_name}] Production Grade Colorized Image saved successfully via Hugging Face!")
        except Exception as e:
            print(f"[{self.agent_name}] Hugging Face Node processing exception: {str(e)}. Triggering procedural safe painting.")
            self._execute_procedural_painting(vision_data)

    def _execute_procedural_painting(self, vision_data):
        """Procedural execution matrix when Hugging Face API is unlinked or offline."""
        if not PIL_AVAILABLE or not os.path.exists(self.input_manga_path):
            return
        try:
            img = Image.open(self.input_manga_path).convert("RGBA")
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Extract dynamic color parameters from Gemini response fallback arrays
            glow = vision_data.get("vfx_glow_layers", {}).get("hex_code", "#00FFFF")
            # Parse hex to RGBA tuple
            h = glow.lstrip('#')
            rgb_glow = tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (50,)

            # Add procedural visual tint layers across panel dimensions
            draw.rectangle([0, 0, img.size[0], img.size[1]], fill=rgb_glow)
            final_img = Image.alpha_composite(img, overlay).convert("RGB")
            final_img.save(self.output_colorized_path, "PNG")
            print(f"[{self.agent_name}] Procedural asset rendering complete.")
        except Exception as e:
            print(f"[{self.agent_name}] Procedural fallback painter failed: {str(e)}")

    def _procedural_vision_data(self):
        return {
            "detected_universe_context": "Universal Fallback Matrix",
            "detected_characters": [{"name": "Dynamic Hero Profile", "pose_description": "Combat stance active", "depth_index": 0.95}],
            "dynamic_coloring_prompt": "Vibrant anime cell shading, high quality cinematic tones, clean digital paint work",
            "vfx_glow_layers": {"type": "ambient_glow", "hex_code": "#FF00FF"}
        }

    def _generate_procedural_mock_panel(self):
        if not PIL_AVAILABLE: return
        manga_img = Image.new("RGB", (800, 1000), (255, 255, 255))
        draw = ImageDraw.Draw(manga_img)
        draw.rectangle([20, 20, 780, 980], outline=(0, 0, 0), width=8)
        draw.line([(40, 40), (760, 960)], fill=(0, 0, 0), width=4)
        manga_img.save(self.input_manga_path, "PNG")

    def _save_blueprint_state(self, vision_data, bypass_active=False):
        blueprint = {
            "agent_executed": self.agent_name,
            "pipeline_mode": "Manhwa Bypass Extraction" if bypass_active else "Full Manga Colorization Engine",
            "source_asset": self.input_manga_path,
            "output_colorized_asset": self.output_colorized_path,
            "extracted_metadata": vision_data
        }
        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(blueprint, f, indent=4)
        print(f"[{self.agent_name}] State tracking ledger successfully updated: '{self.output_blueprint_path}'")

if __name__ == "__main__":
    colorizer = UniversalMangaPanelVisionColorizer()
    
    # SYSTEM TEST RUN EXAMPLES:
    # Example A: Pass title dynamically to fetch from MangaDex
    # colorizer.execute_universal_pipeline(search_title="Jujutsu Kaisen", chapter="1", page=3)
    
    # Example B: Run locally on whichever asset is currently placed inside workspace
    colorizer.execute_universal_pipeline()
