# ==============================================================================
# Ai_Agent_55_Universal_Vision_Comprehender.py
# MODULE H: Omni Generative Matrix (Core Vision Brain)
# ==============================================================================

import os
import sys
import json
import re
import base64
import urllib.request
import urllib.error
import shutil
import glob
from io import BytesIO

# 100% OFFLINE AUTONOMY DEPENDENCIES (Fallback math/vision)
try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageStat, ImageOps, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

class OmniMatrixVisionComprehender:
    def __init__(self):
        self.agent_name = "Ai_Agent_55_Universal_Vision_Comprehender"
        
        # 2. UNIVERSAL PATH ISOLATION
        self.workspace_root = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.module_h_dir = os.path.join(self.workspace_root, "Module_H_Generative")
        self.inputs_dir = os.path.join(self.module_h_dir, "inputs_raw")
        self.outputs_dir = os.path.join(self.module_h_dir, "outputs_vision_layers")
        self.overrides_dir = os.path.join(self.workspace_root, "Global_Overrides")
        self.state_file = os.path.join(self.workspace_root, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_root, "global_config.json")
        
        # API Keys
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.hf_api_key = os.environ.get("HF_API_KEY", "")

        self._initialize_directories()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _initialize_directories(self):
        for d in [self.workspace_root, self.module_h_dir, self.inputs_dir, self.outputs_dir, self.overrides_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    # 3. IDEMPOTENCY SCRUBBING
    def scrub_workspace(self):
        self.log("Scrubbing legacy vision data to ensure idempotency...", "INFO")
        for filename in os.listdir(self.outputs_dir):
            file_path = os.path.join(self.outputs_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                self.log(f"Failed to delete {file_path}. Reason: {e}", "WARNING")

    # 4. LIMITLESS FLUIDITY (Configurable overrides and modes)
    def load_global_config(self):
        default_config = {
            "vision_mode": "exact_clone", # Options: exact_clone, inspiration_mashup
            "target_style": "preserve_original",
            "enforce_sakuga_motion": "auto"
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception:
                pass
        return default_config

    # 5. BULLETPROOF JSON CLEANER
    def clean_json_response(self, raw_response):
        try:
            cleaned = re.sub(r'```(?:json)?\n(.*?)```', r'\1', raw_response, flags=re.DOTALL)
            cleaned = cleaned.strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            self.log("Regex JSON parsing failed. Attempting brute-force extraction.", "WARNING")
            start = raw_response.find("{")
            end = raw_response.rfind("}")
            if start != -1 and end != -1:
                try:
                    return json.loads(raw_response[start:end+1])
                except:
                    pass
            return None

    # 6. QUAD-CORE FALLBACK MATRIX FOR VISION COMPREHENSION
    def extract_vision_blueprint(self, img_path, config):
        with open(img_path, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode('utf-8')

        prompt = f"""
        Analyze this image. We need a 3D-ready blueprint. Mode: {config.get('vision_mode', 'exact_clone')}.
        Return ONLY valid JSON. No markdown. Format:
        {{
            "art_style": "e.g., western_comic, manga_bw, realistic, anime, cyberpunk_pixel",
            "camera_angle": "e.g., dutch_angle, close_up, wide_shot, eye_level",
            "lighting_blueprint": {{
                "direction": "e.g., top_right, back_lit, flat",
                "time_of_day": "e.g., noon, golden_hour, night_neon",
                "intensity": "e.g., harsh, soft"
            }},
            "character_present": true/false,
            "pose_intent": "description of action/motion (e.g., high_speed_punch_sakuga)",
            "is_action_frame": true/false,
            "environment_description": "detailed description of background",
            "has_speech_bubbles": true/false,
            "recommended_layering": "foreground, midground, background elements"
        }}
        """

        # Core 1: Gemini
        if self.gemini_api_key:
            try:
                self.log("Executing Core 1 (Gemini) for Vision Blueprint...", "INFO")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": prompt}, {"inlineData": {"mimeType": "image/jpeg", "data": img_b64}}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    resp_text = json.loads(resp.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self.clean_json_response(resp_text)
                    if parsed: return parsed
            except Exception as e:
                self.log(f"Core 1 Failed: {e}", "WARNING")

        # Core 2: OpenAI (GPT-4o Vision fallback)
        if self.openai_api_key:
            try:
                self.log("Executing Core 2 (OpenAI) for Vision Blueprint...", "INFO")
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}]}]
                }
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=30) as resp:
                    resp_text = json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
                    parsed = self.clean_json_response(resp_text)
                    if parsed: return parsed
            except Exception as e:
                self.log(f"Core 2 Failed: {e}", "WARNING")

        # Core 3: Ollama Local (LLaVA if running)
        try:
            self.log("Executing Core 3 (Ollama/LLaVA Local)...", "INFO")
            url = "http://127.0.0.1:11434/api/generate"
            payload = {"model": "llava", "prompt": prompt, "images": [img_b64], "stream": False}
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=40) as resp:
                resp_text = json.loads(resp.read().decode("utf-8"))["response"]
                parsed = self.clean_json_response(resp_text)
                if parsed: return parsed
        except Exception as e:
            self.log(f"Core 3 Failed: {e}", "WARNING")

        # Core 4: Procedural Math (100% Offline Autonomy)
        self.log("Executing Core 4 (Procedural Offline Analysis)...", "INFO")
        return self._procedural_vision_analysis(img_path)

    # 10. 100% OFFLINE AUTONOMY FALLBACK (Math/Heuristics)
    def _procedural_vision_analysis(self, img_path):
        is_bw, has_high_contrast = False, False
        if PIL_AVAILABLE:
            try:
                img = Image.open(img_path).convert('HSV')
                stat = ImageStat.Stat(img.split()[1]) # Saturation
                is_bw = stat.mean[0] < 15
                lum = ImageStat.Stat(img.split()[2]) # Value
                has_high_contrast = (lum.stddev[0] > 60)
            except: pass
        
        return {
            "art_style": "manga_bw" if is_bw else "unknown_color_art",
            "camera_angle": "eye_level_procedural",
            "lighting_blueprint": {
                "direction": "flat_procedural",
                "time_of_day": "unknown",
                "intensity": "harsh" if has_high_contrast else "soft"
            },
            "character_present": True,
            "pose_intent": "idle_procedural",
            "is_action_frame": has_high_contrast,
            "environment_description": "Procedural extracted environment",
            "has_speech_bubbles": False,
            "recommended_layering": "flat_extraction"
        }

    # SEPARATION MODULE (API vs OFFLINE)
    def extract_layers(self, img_path, base_name, blueprint, config):
        vision_mode = config.get("vision_mode", "exact_clone")
        out_char = os.path.join(self.outputs_dir, f"{base_name}_character.png")
        out_bg = os.path.join(self.outputs_dir, f"{base_name}_background.png")
        out_depth = os.path.join(self.outputs_dir, f"{base_name}_depth.png")
        
        # --- THE OVERRIDE MATRIX (No Gulaami) ---
        user_bg = os.path.join(self.overrides_dir, "custom_bg.png")
        user_char = os.path.join(self.overrides_dir, "custom_char.png")

        if os.path.exists(user_char) and vision_mode == "inspiration_mashup":
            self.log("Manual Override Detected: Using Custom Character.", "INFO")
            shutil.copy(user_char, out_char)
            has_extracted_char = True
        else:
            self.log("Extracting Character layer...", "INFO")
            has_extracted_char = self._run_rembg_or_fallback(img_path, out_char)

        if os.path.exists(user_bg) and vision_mode == "inspiration_mashup":
            self.log("Manual Override Detected: Using Custom Background.", "INFO")
            shutil.copy(user_bg, out_bg)
        else:
            self.log("Generating Clean Plate Background...", "INFO")
            self._generate_clean_plate(img_path, out_char if has_extracted_char else None, out_bg)

        self.log("Synthesizing 2.5D Depth Map...", "INFO")
        self._generate_depth_map(out_bg, out_depth)

        return {"char_layer": out_char, "bg_layer": out_bg, "depth_map": out_depth}

    def _run_rembg_or_fallback(self, img_path, out_path):
        if REMBG_AVAILABLE and PIL_AVAILABLE:
            try:
                img = Image.open(img_path)
                out = remove(img)
                out.save(out_path, "PNG")
                return True
            except Exception as e:
                self.log(f"Rembg failed: {e}. Falling back to Procedural Mask.", "WARNING")
        
        # 100% Offline Autonomy: Procedural Threshold Masking
        if PIL_AVAILABLE:
            try:
                img = Image.open(img_path).convert("RGBA")
                gray = img.convert("L")
                mask = gray.point(lambda p: 255 if p < 200 else 0)
                img.putalpha(mask)
                img.save(out_path, "PNG")
                return True
            except: pass
        return False

    def _generate_clean_plate(self, original_path, char_mask_path, out_path):
        # In a real API context, call HuggingFace Inpainting here.
        # Fallback 100% offline autonomy (procedural blur/fill):
        if PIL_AVAILABLE:
            try:
                img = Image.open(original_path).convert("RGBA")
                # Dummy inpainting: Heavy gaussian blur of the original to serve as a backdrop
                bg = img.filter(ImageFilter.GaussianBlur(radius=20))
                bg.save(out_path, "PNG")
            except:
                shutil.copy(original_path, out_path)
        else:
            shutil.copy(original_path, out_path)

    def _generate_depth_map(self, bg_path, out_path):
        # In a real API context, call DepthAnything via HF.
        # Fallback 100% offline autonomy (Luminance to Depth):
        if PIL_AVAILABLE and os.path.exists(bg_path):
            try:
                img = Image.open(bg_path).convert("L")
                # Invert logic: darker = farther, lighter = closer (naive heuristic)
                depth = ImageOps.invert(img)
                # Soften it
                depth = depth.filter(ImageFilter.GaussianBlur(radius=5))
                depth.save(out_path, "PNG")
            except: pass

    # 7. ATOMIC HANDSHAKE (Update state)
    def update_matrix_state(self, final_payload):
        state = {}
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                try: state = json.load(f)
                except: pass
        
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "Ai_Agent_56_RGB_Image_To_3D_Mesh_Converter"
        state["Module_H_Vision_Data"] = final_payload

        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
        self.log(f"Atomic Handshake Complete. Next -> {state['next_agent']}", "INFO")

    def execute(self):
        self.log("System Initializing...", "INFO")
        self.scrub_workspace()
        config = self.load_global_config()
        
        # 9. ACTIONABLE ABSTRACTION (Creating a usable master JSON for Blender)
        master_output_data = {}

        input_files = glob.glob(os.path.join(self.inputs_dir, "*.*"))
        valid_exts = ['.png', '.jpg', '.jpeg', '.webp']
        images = [f for f in input_files if os.path.splitext(f)[1].lower() in valid_exts]

        if not images:
            self.log(f"No valid images found in {self.inputs_dir}. Waiting for assets.", "WARNING")
            return

        for idx, img_path in enumerate(images):
            base_name = f"scene_{idx:03d}"
            self.log(f"--- Processing: {base_name} ---", "INFO")
            
            # Step 1: AI Vision Comprehension
            blueprint = self.extract_vision_blueprint(img_path, config)
            self.log(f"Blueprint Extracted: Style[{blueprint.get('art_style')}] Action[{blueprint.get('is_action_frame')}]", "INFO")
            
            # Step 2: Layer Extraction & Overrides
            layers = self.extract_layers(img_path, base_name, blueprint, config)
            
            # Step 3: Bundle Actionable Data for Agent 56 (Blender/Mesh)
            master_output_data[base_name] = {
                "source_image": img_path,
                "layers": layers,
                "blender_blueprint": {
                    # This tells Blender exactly what nodes to generate
                    "shader_type": "toon_shader" if "manga" in blueprint.get("art_style", "") else "principled_bsdf",
                    "lighting_setup": blueprint.get("lighting_blueprint", {}),
                    "camera_fov": 24 if blueprint.get("camera_angle", "") == "close_up" else 50,
                    "compositor_motion_blur": 1.5 if blueprint.get("is_action_frame", False) else 0.1
                }
            }
            
            json_path = os.path.join(self.outputs_dir, f"{base_name}_blueprint.json")
            with open(json_path, "w") as f:
                json.dump(master_output_data[base_name], f, indent=4)
                
            self.log(f"Scene {base_name} processing complete.", "INFO")

        # Route to next agent
        self.update_matrix_state(master_output_data)

if __name__ == "__main__":
    agent = OmniMatrixVisionComprehender()
    agent.execute()

# ==============================================================================
# END OF FILE
# ==============================================================================
