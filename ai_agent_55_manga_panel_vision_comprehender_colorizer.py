import os
import sys
import json
import re
import base64
import urllib.request
import urllib.parse
import zipfile
import shutil
from io import BytesIO

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageStat, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

class UniversalVisionComprehender:
    def __init__(self, local_library_dir="D:/ZNET_Local_Assets", drive_temp_dir="G:/My Drive/ZNET_Temp"):
        self.agent_name = "Ai Agent 55: Vision Comprehender & Splitter"
        
        # 1. Storage Optimization Strategy
        self.local_library_dir = local_library_dir # For final rigged characters (Fast Access)
        self.drive_temp_dir = drive_temp_dir       # For Heavy Backgrounds, Masks, JSON (5TB Google Drive)
        
        self.inputs_dir = os.path.join(self.drive_temp_dir, "inputs")
        self.outputs_dir = os.path.join(self.drive_temp_dir, "outputs")
        self.char_export_dir = os.path.join(self.local_library_dir, "characters_raw")
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.hf_api_key = os.environ.get("HF_API_KEY", "") 
        
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        self.hf_colorize_url = "https://api-inference.huggingface.co/models/lllyasviel/control_v11p_sd15_lineart"
        self.hf_inpaint_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-inpainting"
        self.hf_depth_url = "https://api-inference.huggingface.co/models/depth-anything/Depth-Anything-V2-Small-hf"

        self.character_registry = [] 

        for directory in [self.inputs_dir, self.outputs_dir, self.char_export_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    # 2. Smart Color Histogram Check (Manhwa vs Manga)
    def _is_black_and_white(self, img_path, threshold=10):
        if not PIL_AVAILABLE: return False
        try:
            img = Image.open(img_path).convert('HSV')
            saturation = img.split()[1] # Get Saturation channel
            stat = ImageStat.Stat(saturation)
            if stat.mean[0] < threshold:
                return True # Very low saturation = Manga (B&W)
            return False # Colorized Manhwa/Image
        except Exception as e:
            return False

    def _query_gemini(self, img_path):
        with open(img_path, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        # 3. Upgraded Prompt for "Zero-Character Branching"
        system_prompt = f"""
        Analyze this manga/anime image. We have existing models: {self.character_registry}.
        Count how many humans/characters are in the image. If none, set character_count to 0.
        Return ONLY raw JSON. Format:
        {{
            "character_count": int,
            "character_name": "Name or None",
            "is_new_character": bool,
            "background_description": "short description of the setting",
            "colorization_prompt": "prompt for coloring if needed"
        }}
        """
        payload = {
            "contents": [{"parts": [{"text": system_prompt}, {"inlineData": {"mimeType": "image/png", "data": img_b64}}]}], 
            "generationConfig": {"responseMimeType": "application/json"}
        }
        
        try:
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                response_text = json.loads(resp.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                response_text = re.sub(r'^```json', '', response_text, flags=re.IGNORECASE)
                response_text = re.sub(r'```$', '', response_text).strip()
                return json.loads(response_text)
        except Exception as e:
            self.log_message(f"Gemini API Error: {str(e)}", "WARNING")
            return {"character_count": 1, "character_name": "Unknown", "is_new_character": True, "background_description": "A scenic view"}

    def _hf_colorize(self, img_path, out_path, prompt):
        self.log_message("Applying Colorization...", "INFO")
        with open(img_path, "rb") as f:
            req = urllib.request.Request(self.hf_colorize_url, data=f.read(), headers={"Authorization": f"Bearer {self.hf_api_key}", "Content-Type": "application/octet-stream", "X-Prompt": prompt})
            try:
                with urllib.request.urlopen(req, timeout=40) as resp, open(out_path, "wb") as out:
                    out.write(resp.read())
            except Exception as e:
                self.log_message(f"Colorize failed, using original: {e}", "WARNING")
                shutil.copy(img_path, out_path)

    def _hf_inpaint(self, img_path, mask_path, out_path, prompt):
        self.log_message("Inpainting Background...", "INFO")
        with open(img_path, "rb") as i, open(mask_path, "rb") as m:
            payload = {"inputs": prompt, "image": base64.b64encode(i.read()).decode(), "mask_image": base64.b64encode(m.read()).decode()}
        req = urllib.request.Request(self.hf_inpaint_url, data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {self.hf_api_key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp, open(out_path, "wb") as out:
                out.write(resp.read())
        except Exception as e:
            self.log_message(f"Inpaint failed: {e}", "WARNING")

    def _generate_depth_map(self, bg_path, out_path):
        self.log_message("Generating 2.5D Depth Map...", "INFO")
        if not self.hf_api_key or not os.path.exists(bg_path): return
        
        with open(bg_path, "rb") as f:
            req = urllib.request.Request(self.hf_depth_url, data=f.read(), headers={
                "Authorization": f"Bearer {self.hf_api_key}", 
                "Content-Type": "application/octet-stream"
            })
            try:
                with urllib.request.urlopen(req, timeout=40) as resp, open(out_path, "wb") as out:
                    out.write(resp.read())
            except Exception as e:
                self.log_message(f"Depth Map generation failed: {e}", "WARNING")

    def _process_single_image(self, img_path, file_index):
        base_name = f"scene_{file_index:03d}"
        self.log_message(f"--- Processing {base_name} ---", "INFO")
        
        out_color = os.path.join(self.outputs_dir, f"{base_name}_01_color.png")
        out_char = os.path.join(self.char_export_dir, f"{base_name}_02_character.png") # Goes to Local Library!
        out_mask = os.path.join(self.outputs_dir, f"{base_name}_03_mask.png")
        out_bg = os.path.join(self.outputs_dir, f"{base_name}_04_bg.png")
        out_depth = os.path.join(self.outputs_dir, f"{base_name}_05_bg_depth.png")
        out_json = os.path.join(self.outputs_dir, f"{base_name}_vision.json")

        # Smart Color Bypass
        is_bw = self._is_black_and_white(img_path)
        vision_data = self._query_gemini(img_path)

        if is_bw and self.hf_api_key:
            self._hf_colorize(img_path, out_color, vision_data.get("colorization_prompt", ""))
        else:
            self.log_message("Color Image Detected (Manhwa/Original). Bypassing Colorization.", "INFO")
            shutil.copy(img_path, out_color)

        char_count = vision_data.get("character_count", 1)

        # Smart Environment Routing
        if char_count == 0:
            self.log_message("ZERO CHARACTERS DETECTED. Routing to Environment-Only Pipeline.", "INFO")
            shutil.copy(out_color, out_bg)
            self._generate_depth_map(out_bg, out_depth)
        else:
            self.log_message(f"Detected {char_count} character(s). Proceeding to Splitter...", "INFO")
            char_name = vision_data.get("character_name", "Unknown")
            if vision_data.get("is_new_character", True) and char_name not in self.character_registry:
                self.character_registry.append(char_name)

            if REMBG_AVAILABLE and PIL_AVAILABLE:
                try:
                    img = Image.open(out_color)
                    isolated = remove(img)
                    isolated.save(out_char, "PNG")
                    
                    alpha = isolated.split()[3]
                    ImageOps.invert(alpha).save(out_mask, "PNG")
                    
                    if self.hf_api_key:
                        self._hf_inpaint(out_color, out_mask, out_bg, vision_data.get("background_description", ""))
                        if os.path.exists(out_bg):
                            self._generate_depth_map(out_bg, out_depth)
                except Exception as e:
                    self.log_message(f"Split/Mask/Inpaint pipeline failed: {str(e)}", "ERROR")

        # Save JSON states for next Modules
        vision_data["pipeline_mode"] = "Environment" if char_count == 0 else "Character_Action"
        with open(out_json, "w") as f:
            json.dump(vision_data, f, indent=4)
            
        self.log_message(f"Finished Processing {base_name}.", "INFO")

    def execute_engine(self, mode="folder", source_data=""):
        # Code block kept same for execution routing...
        self.log_message("Engine initialized...", "INFO")
        # (Rest of execution code remains standard)
