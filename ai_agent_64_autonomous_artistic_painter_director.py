import os
import re
import sys
import json
import time
import random
import urllib.request
import urllib.error
from datetime import datetime

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

class Ai_Agent_64_Autonomous_Artistic_Painter_Director:
    """
    OMNIMATRIX V2.0 GOD-LEVEL AUTONOMOUS ARTISTIC PAINTER DIRECTOR
    Acts as the master visual art director combining Makoto Shinkai atmospheric lighting,
    MAPPA high-contrast cel-shading, and Studio Ghibli organic painterly textures.
    Synthesizes actionable paint blueprints containing color harmony palettes, ink outlines,
    and VFX brush influences to elevate 3D renders into human-like masterpieces.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_64_Autonomous_Artistic_Painter_Director"
        self.workspace_dir = workspace_dir
        self.storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        self.animation_dna_path = os.path.join(self.workspace_dir, "62_animation_dna_blueprint.json")
        self.output_blueprint_path = os.path.join(self.workspace_dir, "64_artistic_paint_blueprint.json")
        
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous artistic paint blueprints."""
        if os.path.exists(self.output_blueprint_path):
            try:
                os.remove(self.output_blueprint_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy blueprint {self.output_blueprint_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7 & 4: ATOMIC HANDSHAKE & CONFIGURATION LOADERS
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
            # Hand off to THE MAIN ORCHESTRATOR: Ai Agent 65 (Supreme Creative Script Conductor)
            data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_65_Supreme_Creative_Script_Conductor"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_upstream_context(self):
        """Ingests storyboard sequences and Animation DNA stylistic constraints."""
        panels = []
        style_mode = "realistic"

        if os.path.exists(self.storyboard_path):
            try:
                with open(self.storyboard_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                panels = data.get("storyboard_panels", [])
            except Exception as error:
                self.log(f"Storyboard ingestion exception: {error}", "WARNING")

        if os.path.exists(self.animation_dna_path):
            try:
                with open(self.animation_dna_path, "r", encoding="utf-8") as f:
                    dna = json.load(f)
                style_mode = dna.get("animation_dna_matrix", {}).get("global_aesthetic_mode", "realistic").lower()
            except Exception:
                pass

        if not panels:
            self.log("Storyboard sequence absent. Injecting baseline high-impact narrative scenes.", "INFO")
            panels = [
                {"panel_id": 1, "description": "Protagonist standing beneath a torrential cyberpunk rainstorm, crackling with violet energy.", "emotional_tone": "MELANCHOLIC_BADASS"},
                {"panel_id": 2, "description": "Antagonist unleashing an explosive crimson energy vortex across a fractured desert wasteland.", "emotional_tone": "EPIC_CLIMAX"}
            ]

        return panels, style_mode

    def _clean_json(self, raw_text):
        """Rule 5: Bulletproof JSON scrubber."""
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
    # RULE 6, 14, 15, 17: QUAD-CORE ARTISTIC PAINTER SYNTHESIZER
    # =====================================================================
    def generate_artistic_blueprint(self):
        self._handshake("IN_PROGRESS")
        panels, style_mode = self._load_upstream_context()
        
        self.log(f"Quad-Core Artistic Painter Forge Initiated. Scenes to Paint: {len(panels)} | DNA Style: [{style_mode.upper()}]")

        # Rule 15: Limitless continuous color harmony and painterly parameter formulation
        prompt = (
            f"You are OMNIMATRIX Master Art Director. Global Aesthetic Enforced: '{style_mode}'.\n"
            "Take raw storyboard scenes and design an 'Artistic Paint Blueprint' to guide 3D shaders and compositors.\n"
            "CRITICAL ARTISTIC RULES:\n"
            "1. If style is ANIME: Enforce bold cel outlines ('shadow_ink_thickness' 1.5 to 3.5), high-contrast palettes, and high 'vfx_brush_stroke_influence' (0.7 to 1.0) so smoke/fire look like digital brush strokes.\n"
            "2. If style is REALISTIC: Enforce zero ink thickness (0.0), atmospheric color bleed for Makoto Shinkai light scattering, and subtle filmic contrast curves.\n"
            "Output STRICTLY a JSON object with key 'paint_blueprints' containing a list of objects with:\n"
            "- 'scene_id': integer matching the panel number.\n"
            "- 'brush_texture_style': string ('oil_canvas_rough', 'watercolor_wash_soft', 'retro_90s_cel_ink', or 'acrylic_high_contrast').\n"
            "- 'shadow_ink_thickness': float (0.0 for realistic, 1.0 to 3.5 for anime cel outlines).\n"
            "- 'color_harmony_palette': array of exactly 5 uppercase Hex strings defining the frame's color spectrum.\n"
            "- 'ambient_color_bleed': string (Hex code representing atmospheric light scattering into shadow depth).\n"
            "- 'painterly_contrast_curve': string ('s_curve_dramatic', 'soft_matte_nostalgic', or 'crushed_shadow_aggressive').\n"
            "- 'vfx_brush_stroke_influence': float (0.0 to 1.0 defining stylized stroke vs physical realism).\n"
            "Zero compression or placeholders allowed."
        )

        user_msg = json.dumps({"style_mode_enforced": style_mode, "storyboard_scenes": panels})
        output = None

        # Core 1: Gemini (Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"{prompt}\n\nUser Context:\n{user_msg}"}]}],
                    "generationConfig": {"temperature": 0.88, "responseMimeType": "application/json"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Synthesized master artistic paint blueprints!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")

        # Core 2: OpenAI Failsafe (Rule 14 & 16)
        if self.openai_key and not output:
            try:
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                    "response_format": {"type": "json_object"}
                }
                res = self._api_call(self.openai_url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_key}"})
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"]))
                self.log("[Core 2: OpenAI] Synthesized master artistic paint blueprints!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")

        # Core 3: Ollama Local Fallback
        if not output:
            try:
                payload = {
                    "model": "llama3",
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                    "format": "json",
                    "stream": False
                }
                res = self._api_call(self.ollama_url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res.get("message", {}).get("content", "{}")))
                self.log("[Core 3: Ollama] Generated local artistic paint blueprints!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Math & Color Alchemist Autonomy (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline continuous Color Alchemist synthesis...", "WARNING")
            is_anime = "anime" in style_mode
            blueprints = []

            for idx, panel in enumerate(panels):
                p_id = panel.get("panel_id", idx + 1)
                tone = str(panel.get("emotional_tone", "")).upper()
                
                if any(k in tone for k in ["MELANCHOLIC", "SAD", "DRAMA"]):
                    palette = ["#121824", "#2A364F", "#485E78", "#8A9BA8", "#D0D8E0"]
                    bleed, curve, brush, ink = "#1C2833", "soft_matte_nostalgic", "watercolor_wash_soft", 1.8 if is_anime else 0.0
                elif any(k in tone for k in ["EPIC", "CLIMAX", "FIGHT", "ACTION"]):
                    palette = ["#0A0A0F", "#2B0B0A", "#D9251E", "#FF8C00", "#FFF8E7"]
                    bleed, curve, brush, ink = "#4A0E0D", "crushed_shadow_aggressive", "oil_canvas_rough", 2.6 if is_anime else 0.0
                else:
                    palette = ["#151E28", "#34495E", "#F39C12", "#58D68D", "#F4F6F7"]
                    bleed, curve, brush, ink = "#212F3D", "s_curve_dramatic", "retro_90s_cel_ink", 2.0 if is_anime else 0.0

                blueprints.append({
                    "scene_id": p_id,
                    "brush_texture_style": brush,
                    "shadow_ink_thickness": ink,
                    "color_harmony_palette": palette,
                    "ambient_color_bleed": bleed,
                    "painterly_contrast_curve": curve,
                    "vfx_brush_stroke_influence": 0.85 if is_anime else 0.15
                })
            output = {"paint_blueprints": blueprints}

        # Rule 17 Safeguard: Cap at 50 scene blueprints to prevent downstream shading memory overflow
        blueprints_list = output.get("paint_blueprints", [])[:50]

        final_blueprint = {
            "agent_executed": self.agent_name,
            "execution_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "aesthetic_mode_enforced": style_mode,
            "total_scenes_painted": len(blueprints_list),
            "paint_blueprints": blueprints_list
        }

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=4)

        self.log(f"Artistic painter blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return final_blueprint

if __name__ == "__main__":
    painter = Ai_Agent_64_Autonomous_Artistic_Painter_Director()
    painter.generate_artistic_blueprint()
