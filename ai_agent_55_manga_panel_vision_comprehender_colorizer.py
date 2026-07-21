import os
import sys
import json
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
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 55: vision_comprehender_and_splitter"
        self.workspace_dir = workspace_dir
        
        # Directories for Batch Processing
        self.inputs_dir = os.path.join(self.workspace_dir, "inputs")
        self.outputs_dir = os.path.join(self.workspace_dir, "outputs")
        
        # API Keys loading from environment
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.hf_api_key = os.environ.get("HF_API_KEY", "") 
        
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        self.hf_colorize_url = "https://api-inference.huggingface.co/models/lllyasviel/control_v11p_sd15_lineart"
        self.hf_inpaint_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-inpainting"

        for directory in [self.inputs_dir, self.outputs_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    # ==========================================
    # INPUT MODE 1: MANGADEX FETCHER
    # ==========================================
    def fetch_panel_from_mangadex(self, manga_title, chapter_num="1", page_num=0):
        print(f"[{self.agent_name}] Searching MangaDex for: '{manga_title}', Chapter: {chapter_num}")
        try:
            search_url = f"https://api.mangadex.org/manga?title={urllib.parse.quote(manga_title)}&limit=1"
            req = urllib.request.Request(search_url, headers={'User-Agent': 'ZNetBot/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                manga_id = json.loads(resp.read().decode("utf-8"))["data"][0]["id"]

            feed_url = f"https://api.mangadex.org/manga/{manga_id}/feed?chapter[]={chapter_num}&translatedLanguage[]=en&limit=1"
            req = urllib.request.Request(feed_url, headers={'User-Agent': 'ZNetBot/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                chapter_id = json.loads(resp.read().decode("utf-8"))["data"][0]["id"]

            server_url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
            req = urllib.request.Request(server_url, headers={'User-Agent': 'ZNetBot/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                server_data = json.loads(resp.read().decode("utf-8"))
                base_url = server_data["baseUrl"]
                hash_id = server_data["chapter"]["hash"]
                pages = server_data["chapter"]["data"]
                
                target_page = pages[page_num] if page_num < len(pages) else pages[0]
                download_url = f"{base_url}/data/{hash_id}/{target_page}"

            save_path = os.path.join(self.inputs_dir, f"mangadex_{manga_title.replace(' ', '_')}.png")
            req = urllib.request.Request(download_url, headers={'User-Agent': 'ZNetBot/1.0'})
            with urllib.request.urlopen(req, timeout=30) as resp, open(save_path, "wb") as out_f:
                out_f.write(resp.read())
            return [save_path]
        except Exception as e:
            print(f"[{self.agent_name}] MangaDex Fetch Failed: {str(e)}")
            return []

    # ==========================================
    # INPUT MODE 2: ZIP EXTRACTOR
    # ==========================================
    def process_zip_upload(self, zip_filepath):
        print(f"[{self.agent_name}] Extracting ZIP file: {zip_filepath}")
        extracted_images = []
        extract_folder = os.path.join(self.inputs_dir, "extracted_zip")
        if not os.path.exists(extract_folder):
            os.makedirs(extract_folder)

        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        
        for root, _, files in os.walk(extract_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    extracted_images.append(os.path.join(root, file))
        return extracted_images

    # ==========================================
    # INPUT MODE 3: DRIVE / FOLDER BATCH
    # ==========================================
    def get_images_from_folder(self, folder_path):
        print(f"[{self.agent_name}] Scanning Drive/Folder: {folder_path}")
        images = []
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    images.append(os.path.join(folder_path, file))
        return images

    # ==========================================
    # CORE AI PIPELINE (Runs for each image)
    # ==========================================
    def _process_single_image(self, img_path, file_index):
        print(f"\n[{self.agent_name}] --- Processing Image {file_index} ---")
        base_name = f"scene_{file_index:03d}"
        
        out_color = os.path.join(self.outputs_dir, f"{base_name}_01_color.png")
        out_char = os.path.join(self.outputs_dir, f"{base_name}_02_character.png")
        out_mask = os.path.join(self.outputs_dir, f"{base_name}_03_mask.png")
        out_bg = os.path.join(self.outputs_dir, f"{base_name}_04_bg.png")
        out_json = os.path.join(self.outputs_dir, f"{base_name}_vision.json")

        # 1. Gemini Vision Analysis
        vision_data = self._query_gemini(img_path)
        
        # 2. Colorization or Direct Copy
        if vision_data.get("is_black_and_white", False) and self.hf_api_key:
            self._hf_colorize(img_path, out_color, vision_data.get("colorization_prompt", ""))
        else:
            shutil.copy(img_path, out_color)

        # 3. Local Background Removal & Masking
        if REMBG_AVAILABLE and PIL_AVAILABLE:
            try:
                img = Image.open(out_color)
                isolated = remove(img)
                isolated.save(out_char, "PNG")
                
                alpha = isolated.split()[3]
                ImageOps.invert(alpha).save(out_mask, "PNG")
                
                # 4. Inpaint Black Hole
                if self.hf_api_key:
                    self._hf_inpaint(out_color, out_mask, out_bg, vision_data.get("background_description", ""))
            except Exception as e:
                print(f"[{self.agent_name}] Split/Mask failed: {str(e)}")

        with open(out_json, "w") as f:
            json.dump(vision_data, f, indent=4)
        print(f"[{self.agent_name}] Finished Processing {base_name}.")

    def _query_gemini(self, img_path):
        # (Same logic as before for Gemini API)
        with open(img_path, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        system_prompt = "Analyze this image. JSON format: {\"is_black_and_white\": bool, \"character_description\": \"\", \"background_description\": \"\", \"colorization_prompt\": \"\"}"
        payload = {"contents": [{"parts": [{"text": system_prompt}, {"inlineData": {"mimeType": "image/png", "data": img_b64}}]}], "generationConfig": {"responseMimeType": "application/json"}}
        
        try:
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(json.loads(resp.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip())
        except:
            return {"is_black_and_white": False, "background_description": "A scenic view"}

    def _hf_colorize(self, img_path, out_path, prompt):
        # (Same HuggingFace ControlNet logic)
        with open(img_path, "rb") as f:
            req = urllib.request.Request(self.hf_colorize_url, data=f.read(), headers={"Authorization": f"Bearer {self.hf_api_key}", "Content-Type": "application/octet-stream", "X-Prompt": prompt})
            try:
                with urllib.request.urlopen(req, timeout=40) as resp, open(out_path, "wb") as out:
                    out.write(resp.read())
            except:
                shutil.copy(img_path, out_path)

    def _hf_inpaint(self, img_path, mask_path, out_path, prompt):
        # (Same HuggingFace Inpainting logic)
        with open(img_path, "rb") as i, open(mask_path, "rb") as m:
            payload = {"inputs": prompt, "image": base64.b64encode(i.read()).decode(), "mask_image": base64.b64encode(m.read()).decode()}
        req = urllib.request.Request(self.hf_inpaint_url, data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {self.hf_api_key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp, open(out_path, "wb") as out:
                out.write(resp.read())
        except Exception as e:
            print(f"Inpaint failed: {e}")

    # ==========================================
    # MASTER ORCHESTRATOR
    # ==========================================
    def execute_engine(self, mode="folder", source_data=""):
        print(f"[{self.agent_name}] Initializing Engine in '{mode}' mode...")
        images_to_process = []

        if mode == "mangadex":
            # source_data = {"title": "Naruto", "chapter": "1", "page": 0}
            images_to_process = self.fetch_panel_from_mangadex(source_data["title"], source_data.get("chapter", "1"), source_data.get("page", 0))
        elif mode == "zip":
            images_to_process = self.process_zip_upload(source_data)
        elif mode == "folder":
            images_to_process = self.get_images_from_folder(source_data)
        elif mode == "single":
            images_to_process = [source_data]

        if not images_to_process:
            print(f"[{self.agent_name}] No images found to process. Aborting.")
            return

        print(f"[{self.agent_name}] Found {len(images_to_process)} images. Starting batch processing...")
        for idx, img_path in enumerate(images_to_process, start=1):
            self._process_single_image(img_path, idx)
            
        print(f"[{self.agent_name}] Batch Processing Complete! All assets are in '{self.outputs_dir}'.")

if __name__ == "__main__":
    agent = UniversalVisionComprehender()
    
    # SYSTEM TEST EXAMPLES (UI/Engine will call like this):
    
    # 1. Drive/Folder Mode:
    # agent.execute_engine(mode="folder", source_data="C:/MyDriveSync/AnimeScenes")
    
    # 2. ZIP Mode:
    # agent.execute_engine(mode="zip", source_data="C:/Downloads/manga_chapter.zip")
    
    # 3. MangaDex Mode:
    # agent.execute_engine(mode="mangadex", source_data={"title": "Jujutsu Kaisen", "chapter": "1", "page": 3})
