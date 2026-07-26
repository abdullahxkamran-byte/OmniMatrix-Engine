import os
import re
import sys
import glob
import json
import time
import base64
import shutil
import platform
import urllib.request
import urllib.error
from datetime import datetime
from io import BytesIO

# Attempt importing local image processing libraries
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

# =====================================================================
# RULE 2 & 14: UNIVERSAL ENVIRONMENT & DUAL API CONFIGURATION
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

class Ai_Agent_55_Universal_Vision_Comprehender:
    """
    OMNIMATRIX V2.0 GOD-LEVEL UNIVERSAL VISION COMPREHENDER
    Acts as the master computer vision and scene decomposition engine.
    Ingests flat 2D artwork, manga panels, or scouted stock frames, deploying
    multimodal vision models (Gemini/GPT-4o/LLaVA) to extract lighting geometry,
    camera focal lengths, and layering matrices. Synthesizes transparent
    character sprites, clean background plates, and 2.5D mathematical depth maps
    to feed downstream 3D mesh and world forging nodes.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "Ai_Agent_55_Universal_Vision_Comprehender"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        self.module_h_dir = os.path.join(self.workspace_dir, "Module_H_Generative")
        self.inputs_dir = os.path.join(self.module_h_dir, "inputs_raw")
        self.outputs_dir = os.path.join(self.module_h_dir, "outputs_vision_layers")
        self.overrides_dir = os.path.join(self.workspace_dir, "Global_Overrides")
        self.config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        
        self.max_image_dimension_px = 2048
        
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        self.hf_key = os.environ.get("HF_API_KEY", None)
        
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_local = "llava"
        self.model_cloud = "gpt-4o"

        for directory in [self.workspace_dir, self.module_h_dir, self.inputs_dir, self.outputs_dir, self.overrides_dir]:
            os.makedirs(directory, exist_ok=True)
            
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        formatted = f"[{level}] [{self.agent_name}] {message}"
        print(formatted)

    def _scrub_legacy_assets(self):
        if os.path.exists(self.outputs_dir):
            for file_name in os.listdir(self.outputs_dir):
                file_path = os.path.join(self.outputs_dir, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as error:
                    self.log(f"Failed to scrub legacy vision file {file_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & PIPELINE ROUTING
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS", payload_manifest=None):
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
        if payload_manifest:
            data["orchestrator_matrix"]["Module_H_Vision_Data"] = payload_manifest
            
        if status == "COMPLETED":
            data["orchestrator_matrix"]["next_agent"] = "ai_agent_56_rgb_image_to_3d_mesh_converter"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_global_config(self):
        default_config = {"vision_mode": "exact_clone", "target_style": "preserve_original", "enforce_sakuga_motion": "auto"}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except Exception:
                pass
        return default_config

    def _clean_json(self, raw_text):
        cleaned = re.sub(r"^```(json)?\s*|\s*```$", "", raw_text.strip(), flags=re.IGNORECASE)
        start_index = cleaned.find('{')
        end_index = cleaned.rfind('}')
        if start_index != -1 and end_index != -1:
            return cleaned[start_index:end_index + 1]
        return cleaned

    def _api_call(self, url, payload, headers):
        request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14, 15: QUAD-CORE VISION BLUEPRINT EXTRACTOR
    # =====================================================================
    def _extract_vision_blueprint(self, image_path, config):
        if os.path.exists(image_path) and os.path.isfile(image_path):
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
        else:
            img_b64 = ""

        prompt = (
            f"You are OMNIMATRIX AAA Computer Vision & 3D Layout Architect. Mode: '{config.get('vision_mode', 'exact_clone')}'.\n"
            "Analyze this artwork/image to formulate an actionable 3D Blender translation blueprint.\n"
            "CRITICAL VISION RULES:\n"
            "1. Evaluate lighting direction, camera angle, character pose, and spatial layering.\n"
            "2. Identify if this is a high-kinetic combat frame requiring motion blur or a static atmospheric establishing shot.\n"
            "Output STRICTLY a JSON object containing:\n"
            "- 'art_style': string ('anime_cel_shaded', 'manga_bw', 'photorealistic_pbr', 'western_comic', or 'cyberpunk_pixel').\n"
            "- 'camera_angle': string ('dutch_angle', 'close_up', 'wide_establishing', or 'eye_level').\n"
            "- 'lighting_blueprint': object with keys 'direction' ('top_right', 'back_lit', 'flat'), 'time_of_day' ('golden_hour', 'night_neon', 'noon'), and 'intensity' ('harsh', 'soft').\n"
            "- 'character_present': boolean.\n"
            "- 'pose_intent': string (detailed movement description like 'supersonic_sword_slash_sakuga').\n"
            "- 'is_action_frame': boolean.\n"
            "- 'environment_description': string (detailed spatial background elements).\n"
            "- 'has_speech_bubbles': boolean.\n"
            "- 'recommended_layering': string ('foreground_midground_background_split').\n"
            "Zero conversational text or markdown code wraps allowed."
        )

        output = None

        # Core 1: Gemini Vision Pro
        if self.gemini_key and not output and img_b64:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {"contents": [{"parts": [{"text": prompt}, {"inlineData": {"mimeType": "image/jpeg", "data": img_b64}}]}]}
                res = self._api_call(url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini Vision] Formulated 3D visual translation blueprint!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 1: Gemini Vision] Failed: {e}", "WARNING")

        # Core 2: OpenAI GPT-4o Vision Failsafe
        if self.openai_key and not output and img_b64:
            try:
                headers = {"Authorization": f"Bearer {self.openai_key}", "Content-Type": "application/json"}
                payload = {"model": self.model_cloud, "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}]}]}
                res = self._api_call(self.openai_url, payload, headers)
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"]))
                self.log("[Core 2: OpenAI GPT-4o] Formulated 3D visual translation blueprint!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 2: OpenAI Vision] Failed: {e}", "WARNING")

        # Core 3: Ollama Local LLaVA Vision Fallback
        if not output and img_b64:
            try:
                payload = {"model": self.model_local, "prompt": prompt, "images": [img_b64], "stream": False}
                res = self._api_call(self.ollama_url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res.get("response", "{}")))
                self.log("[Core 3: Ollama LLaVA] Generated local visual blueprint!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama LLaVA] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Algorithmic HSV Alchemist (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline algorithmic HSV luminance vision analysis...", "WARNING")
            is_bw, has_high_contrast = False, False
            if PIL_AVAILABLE and os.path.exists(image_path) and os.path.isfile(image_path):
                try:
                    img = Image.open(image_path).convert('HSV')
                    stat = ImageStat.Stat(img.split()[1])
                    is_bw = stat.mean[0] < 18.0
                    lum = ImageStat.Stat(img.split()[2])
                    has_high_contrast = (lum.stddev[0] > 55.0)
                except Exception:
                    pass
            
            output = {
                "art_style": "manga_bw" if is_bw else "anime_cel_shaded",
                "camera_angle": "eye_level",
                "lighting_blueprint": {"direction": "top_right", "time_of_day": "night_neon" if has_high_contrast else "noon", "intensity": "harsh" if has_high_contrast else "soft"},
                "character_present": True,
                "pose_intent": "high_kinetic_action_stance" if has_high_contrast else "neutral_atmospheric_stance",
                "is_action_frame": has_high_contrast,
                "environment_description": "Algorithmic spatial background extraction.",
                "has_speech_bubbles": False,
                "recommended_layering": "foreground_midground_background_split"
            }

        return output

    # =====================================================================
    # LAYER DECOMPOSITION: CHARACTER vs BACKGROUND vs 2.5D DEPTH
    # =====================================================================
    def _execute_layer_separation(self, image_path, base_name, config):
        out_char = os.path.join(self.outputs_dir, f"{base_name}_character.png")
        out_bg = os.path.join(self.outputs_dir, f"{base_name}_background.png")
        out_depth = os.path.join(self.outputs_dir, f"{base_name}_depth.png")
        
        user_char = os.path.join(self.overrides_dir, "custom_character.png")
        user_bg = os.path.join(self.overrides_dir, "custom_background.png")

        if os.path.exists(user_char) and config.get("vision_mode") == "inspiration_mashup":
            self.log("Manual override detected: Injecting custom character sprite.", "INFO")
            shutil.copy(user_char, out_char)
            has_char = True
        else:
            self.log("Executing character foreground layer separation...", "INFO")
            has_char = self._run_rembg_or_offline_mask(image_path, out_char)

        if os.path.exists(user_bg) and config.get("vision_mode") == "inspiration_mashup":
            self.log("Manual override detected: Injecting custom background plate.", "INFO")
            shutil.copy(user_bg, out_bg)
        else:
            self.log("Synthesizing clean background plate...", "INFO")
            self._generate_clean_background_plate(image_path, out_bg)

        self.log("Synthesizing 2.5D mathematical luminance depth map...", "INFO")
        self._synthesize_25d_depth_map(out_bg, out_depth)

        return {"character_layer_png": out_char, "background_plate_png": out_bg, "depth_map_png": out_depth}

    def _run_rembg_or_offline_mask(self, image_path, output_path):
        if not os.path.exists(image_path) or not os.path.isfile(image_path):
            return False

        if REMBG_AVAILABLE and PIL_AVAILABLE:
            try:
                img = Image.open(image_path)
                if max(img.size) > self.max_image_dimension_px:
                    img.thumbnail((self.max_image_dimension_px, self.max_image_dimension_px), Image.Resampling.LANCZOS)
                out = remove(img)
                out.save(output_path, "PNG")
                return True
            except Exception as error:
                self.log(f"Rembg neural separation exception: {error}. Engaging offline procedural mask.", "WARNING")
        
        if PIL_AVAILABLE:
            try:
                img = Image.open(image_path).convert("RGBA")
                if max(img.size) > self.max_image_dimension_px:
                    img.thumbnail((self.max_image_dimension_px, self.max_image_dimension_px), Image.Resampling.LANCZOS)
                gray = img.convert("L")
                mask = gray.point(lambda p: 255 if p < 210 else 0)
                img.putalpha(mask)
                img.save(output_path, "PNG")
                return True
            except Exception:
                pass
        return False

    def _generate_clean_background_plate(self, original_path, output_path):
        if not os.path.exists(original_path) or not os.path.isfile(original_path):
            return

        if PIL_AVAILABLE:
            try:
                img = Image.open(original_path).convert("RGBA")
                if max(img.size) > self.max_image_dimension_px:
                    img.thumbnail((self.max_image_dimension_px, self.max_image_dimension_px), Image.Resampling.LANCZOS)
                bg = img.filter(ImageFilter.GaussianBlur(radius=18))
                bg.save(output_path, "PNG")
            except Exception:
                shutil.copy(original_path, output_path)
        else:
            shutil.copy(original_path, output_path)

    def _synthesize_25d_depth_map(self, background_path, output_path):
        if PIL_AVAILABLE and os.path.exists(background_path) and os.path.isfile(background_path):
            try:
                img = Image.open(background_path).convert("L")
                if max(img.size) > self.max_image_dimension_px:
                    img.thumbnail((self.max_image_dimension_px, self.max_image_dimension_px), Image.Resampling.LANCZOS)
                depth = ImageOps.invert(img)
                depth = depth.filter(ImageFilter.GaussianBlur(radius=6))
                depth.save(output_path, "PNG")
            except Exception:
                pass

    def execute_vision_pipeline(self):
        self._handshake("IN_PROGRESS")
        self.log("Activating Universal Vision Comprehender & Scene Decomposition...")
        
        config = self._load_global_config()
        master_payload = {}

        input_files = glob.glob(os.path.join(self.inputs_dir, "*.*"))
        valid_exts = ['.png', '.jpg', '.jpeg', '.webp']
        images = [f for f in input_files if os.path.splitext(f)[1].lower() in valid_exts and os.path.isfile(f)]

        if not images:
            self.log(f"No artwork detected in '{self.inputs_dir}'. Synthesizing dummy verification payload.", "WARNING")
            dummy_bp = self._extract_vision_blueprint("dummy_path.png", config)
            master_payload["scene_001"] = {
                "source_image": "none",
                "layers": {"character_layer_png": "none", "background_plate_png": "none", "depth_map_png": "none"},
                "blender_3d_blueprint": {
                    "shader_type": "toon_shader", "lighting_setup": dummy_bp.get("lighting_blueprint", {}),
                    "camera_fov": 50, "compositor_motion_blur": 1.5 if dummy_bp.get("is_action_frame", False) else 0.1
                }
            }
        else:
            for idx, img_path in enumerate(sorted(images)):
                base_name = f"scene_{idx+1:03d}"
                self.log(f"--- Processing Visual Asset: {base_name} ({os.path.basename(img_path)}) ---", "INFO")
                
                blueprint = self._extract_vision_blueprint(img_path, config)
                self.log(f"[{base_name}] Vision Verdict -> Style: [{blueprint.get('art_style')}] | Action: {blueprint.get('is_action_frame')}", "INFO")
                
                layers = self._execute_layer_separation(img_path, base_name, config)
                
                master_payload[base_name] = {
                    "source_image": img_path,
                    "layers": layers,
                    "blender_3d_blueprint": {
                        "shader_type": "toon_shader" if "manga" in str(blueprint.get("art_style", "")).lower() or "cel" in str(blueprint.get("art_style", "")).lower() else "principled_bsdf",
                        "lighting_setup": blueprint.get("lighting_blueprint", {}),
                        "camera_fov": 24 if blueprint.get("camera_angle", "") == "close_up" else 50,
                        "compositor_motion_blur": 1.5 if blueprint.get("is_action_frame", False) else 0.1
                    }
                }
                
                json_path = os.path.join(self.outputs_dir, f"{base_name}_vision_manifest.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(master_payload[base_name], f, indent=4)

        self._handshake("COMPLETED", master_payload)
        self.log("Universal Vision Comprehension & Decomposition Concluded Flawlessly!", "SUCCESS")
        return master_payload

if __name__ == "__main__":
    comprehender = Ai_Agent_55_Universal_Vision_Comprehender()
    comprehender.execute_vision_pipeline()