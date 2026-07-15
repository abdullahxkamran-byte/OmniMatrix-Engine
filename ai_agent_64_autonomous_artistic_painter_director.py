import os
import sys
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

class AiAutonomousArtisticPainterDirector:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 64: autonomous_artistic_painter_director"
        self.workspace_dir = workspace_dir
        self.blueprint_path = os.path.join(self.workspace_dir, "64_artistic_paint_blueprint.json")
        self.storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")

        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_storyboard_context(self):
        # Storyboard ya mood logs load karta hai taaki painter ko context mile
        if os.path.exists(self.storyboard_path):
            try:
                with open(self.storyboard_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("storyboard_panels", [])
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Storyboard load nahi ho saka: {str(e)}")
        
        # Default dramatic fallback context agar storyboard na mile
        return [
            {"panel_id": 1, "description": "Gojo standing under the rain, dark purple energy crackling", "emotional_tone": "MELANCHOLIC_BADASS"},
            {"panel_id": 2, "description": "Goku charging a massive red ki blast, dry desert soil exploding", "emotional_tone": "EPIC_CLIMAX"}
        ]

    def generate_artistic_blueprint(self):
        print(f"[{self.agent_name}] Triggering AI Painter Engine. Injecting artistic soul and human-like aesthetic logic...")
        panels = self._load_storyboard_context()

        system_prompt = (
            "You are a Legendary Anime Art Director and Master Painter (combining Makoto Shinkai's light poetry, "
            "MAPPA's gritty high-contrast shadows, and Studio Ghibli's hand-painted organic textures).\n"
            "Your task is to take raw visual scenes and design a complete 'Artistic Paint Blueprint' that guides "
            "the 3D shaders and compositors on how to paint the scene like a human masterpiece, not a cold 3D render.\n\n"
            "For each scene, output exactly one paint style configuration inside a JSON list named 'paint_blueprints' with these keys:\n"
            "- 'scene_id': matching the panel/scene number.\n"
            "- 'brush_texture_style': string (choose from: 'oil_canvas_rough' for gritty fights, 'watercolor_wash_soft' for emotional scenes, 'retro_90s_cel_ink' for vintage look, 'acrylic_high_contrast' for modern neon look).\n"
            "- 'shadow_ink_thickness': float (0.1 to 3.0, defining the thickness of the stylized cel-shading outline to give a hand-drawn manga feel).\n"
            "- 'color_harmony_palette': array of 5 Hex code strings defining the core artistic color spectrum of the frame.\n"
            "- 'ambient_color_bleed': string (Hex code representing how light scatters and bleeds into shadows to create organic atmosphere).\n"
            "- 'painterly_contrast_curve': string (e.g., 's_curve_dramatic', 'soft_matte_nostalgic', 'crushed_shadow_aggressive' to match the mood).\n"
            "- 'vfx_brush_stroke_influence': float (0.0 to 1.0, defines how much the procedural smoke/fire looks like dynamic digital paint strokes rather than realistic physics).\n\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'paint_blueprints'. "
            "Do not write any conversational intro, explanations, or markdown code blocks (```json). Just return valid raw JSON."
        )

        user_prompt = f"Target Scene/Storyboard Data:\n{json.dumps(panels, indent=2)}"

        if self.openai_api_key:
            print(f"[{self.agent_name}] Status: Querying Cloud Art Intelligence Node [{self.model_cloud}]")
            url = self.openai_url
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            payload = {
                "model": self.model_cloud,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "response_format": {"type": "json_object"}
            }
        else:
            print(f"[{self.agent_name}] Status: Querying Local Llama3 Art Node via Ollama...")
            url = self.ollama_url
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": self.model_local,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "format": "json"
            }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            
            with urllib.request.urlopen(req, timeout=50) as response:
                result = json.loads(response.read().decode("utf-8"))
                
                if self.openai_api_key:
                    raw_content = result["choices"][0]["message"]["content"]
                else:
                    raw_content = result["message"]["content"]
                
                # Clean code blocks if any
                cleaned_content = self._clean_json(raw_content)
                structured_data = json.loads(cleaned_content)
                
                final_blueprint = {
                    "agent_executed": self.agent_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "paint_blueprints": structured_data.get("paint_blueprints", [])
                }
                
                self._save_blueprint(final_blueprint)
                return final_blueprint

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Triggering Master Painter Fallback Logic...")
            return self._execute_artistic_fallback(panels)

    def _clean_json(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned

    def _execute_artistic_fallback(self, panels):
        # AI connection fail hone par dynamic algorithmic paint mapping
        blueprints = []
        for panel in panels:
            p_id = panel.get("panel_id", 1)
            tone = str(panel.get("emotional_tone", "")).upper()
            
            if "MELANCHOLIC" in tone or "SAD" in tone:
                blueprints.append({
                    "scene_id": p_id,
                    "brush_texture_style": "watercolor_wash_soft",
                    "shadow_ink_thickness": 0.8,
                    "color_harmony_palette": ["#1A2536", "#34495E", "#5D6D7E", "#AEB6BF", "#D5D8DC"],
                    "ambient_color_bleed": "#2C3E50",
                    "painterly_contrast_curve": "soft_matte_nostalgic",
                    "vfx_brush_stroke_influence": 0.35
                })
            elif "EPIC" in tone or "CLIMAX" in tone or "FIGHT" in tone:
                blueprints.append({
                    "scene_id": p_id,
                    "brush_texture_style": "oil_canvas_rough",
                    "shadow_ink_thickness": 2.2,
                    "color_harmony_palette": ["#000000", "#1C0A00", "#FF4500", "#FFD700", "#FFFFFF"],
                    "ambient_color_bleed": "#5E1914",
                    "painterly_contrast_curve": "crushed_shadow_aggressive",
                    "vfx_brush_stroke_influence": 0.85
                })
            else:
                blueprints.append({
                    "scene_id": p_id,
                    "brush_texture_style": "retro_90s_cel_ink",
                    "shadow_ink_thickness": 1.2,
                    "color_harmony_palette": ["#2E4053", "#F5B041", "#58D68D", "#FADBD8", "#17202A"],
                    "ambient_color_bleed": "#1C2833",
                    "painterly_contrast_curve": "s_curve_dramatic",
                    "vfx_brush_stroke_influence": 0.5
                })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Painter Fallback)",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "paint_blueprints": blueprints
        }
        self._save_blueprint(fallback_output)
        return fallback_output

    def _save_blueprint(self, data):
        try:
            with open(self.blueprint_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Dynamic paint blueprint saved to '{self.blueprint_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing blueprint: {str(e)}")

if __name__ == "__main__":
    painter = AiAutonomousArtisticPainterDirector()
    print("--- TESTING AI PAINTER ENGINE ---")
    report = painter.generate_artistic_blueprint()
    print("\n--- AI PAINTER BLUEPRINT OUTPUT ---")
    print(json.dumps(report, indent=4))
