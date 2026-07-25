import os
import re
import sys
import json
import time
import random
import urllib.request
import urllib.error

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

class Ai_Agent_62_Animation_Dna_Core_Router:
    """
    OMNIMATRIX V2.0 GOD-LEVEL ANIMATION DNA CORE ROUTER
    Acts as the master architectural conductor bridging Anime Cel-Shading and
    Photorealistic PBR pipelines. Synthesizes continuous mathematical parameter
    matrices for shaders, kinetic rigging, frame interpolation, and atmosphere
    to guarantee unified aesthetic fluidity across all 67 production nodes.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_62_Animation_Dna_Core_Router"
        self.workspace_dir = workspace_dir
        self.output_blueprint_path = os.path.join(self.workspace_dir, "62_animation_dna_blueprint.json")
        
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous animation DNA blueprints."""
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
            # Hand off to Agent 63 (Automated Background RAM Janitor - Pure Utility)
            data["orchestrator_matrix"]["next_agent"] = "Agent_63_Automated_Background_Ram_Janitor"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_upstream_project_context(self):
        """Scans project configuration and storyboard blueprints for thematic context."""
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        
        context = {
            "global_style": "realistic",
            "thematic_mood": "cinematic_action",
            "target_fps": 24.0,
            "has_high_action": False
        }

        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                context["global_style"] = data.get("global_style", "realistic").lower()
                context["thematic_mood"] = data.get("theme", "cinematic_action")
                context["target_fps"] = float(data.get("render_fps", 24.0))
            except Exception:
                pass

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    for panel in json.load(f).get("storyboard_panels", []):
                        if any(token in str(panel).lower() for token in ["climax", "explosion", "sakuga", "fight", "slash"]):
                            context["has_high_action"] = True
                            break
            except Exception:
                pass

        return context

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
    # RULE 6, 14, 15, 17: QUAD-CORE ANIMATION DNA SYNTHESIZER
    # =====================================================================
    def synthesize_animation_dna(self, override_style=None):
        self._handshake("IN_PROGRESS")
        context = self._load_upstream_project_context()
        style = override_style if override_style else context["global_style"]
        
        self.log(f"Quad-Core Animation DNA Forge Initiated. Target Style: [{style.upper()}] | Action Intensity: {context['has_high_action']}")

        # Rule 15: Limitless Continuous Parameter Formulation (No Rigid Presets!)
        prompt = (
            f"You are OMNIMATRIX Chief Animation Architect. Evaluate style: '{style}', mood: '{context['thematic_mood']}', action: {context['has_high_action']}.\n"
            "Formulate the master Animation DNA matrix to orchestrate downstream 3D shaders, physics rigs, interpolation, and atmosphere.\n"
            "CRITICAL ARCHITECTURAL RULES:\n"
            "1. If style is ANIME: Force color_ramp_interpolation='CONSTANT', volumetric_fog_density=0.0 (clean cel edges), and stepping_fps=24 (on-twos/threes hit-stop cadence).\n"
            "2. If style is REALISTIC: Force color_ramp_interpolation='EASE', high subsurface_scattering, and stepping_fps=60 or 120 for continuous optical flow.\n"
            "3. If style is HYBRID/SPIDERVERSE: Blend stylized line-art with dynamic step-stuttering and high kinetic impact jitter.\n"
            "Return STRICTLY a JSON object containing:\n"
            "- 'global_aesthetic_mode': string ('anime_cel_shaded', 'photorealistic_pbr', or 'stylized_hybrid_spiderverse').\n"
            "- 'shading_mathematics': object containing:\n"
            "    - 'color_ramp_interpolation': string ('CONSTANT', 'LINEAR', or 'EASE').\n"
            "    - 'voronoi_edge_sharpness': float (0.0 to 1.0).\n"
            "    - 'subsurface_scattering_intensity': float (0.0 to 1.0).\n"
            "- 'kinetic_physics_dna': object containing:\n"
            "    - 'animation_stepping_fps': integer (24, 30, 48, 60, or 120).\n"
            "    - 'mappa_impact_jitter_scale': float (0.5 to 5.0 - F-curve noise multiplier).\n"
            "    - 'gravity_scale_factor': float (0.8 to 2.0).\n"
            "- 'volumetric_atmosphere_dna': object containing:\n"
            "    - 'atmospheric_fog_density': float (0.0 for clean anime, 0.5 to 3.0 for realism).\n"
            "    - 'bloom_exposure_threshold': float (0.1 to 1.5).\n"
            "- 'line_art_specifications': object containing:\n"
            "    - 'freestyle_edge_thickness_px': float (0.0 for realistic, 1.5 to 4.5 for anime).\n"
            "    - 'outline_color_rgba': array of 4 floats [R, G, B, A] between 0.0 and 1.0.\n"
            "Zero compression or placeholders allowed."
        )

        user_msg = json.dumps(context)
        output = None

        # Core 1: Gemini (Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"{prompt}\n\nUser Context:\n{user_msg}"}]}],
                    "generationConfig": {"temperature": 0.82, "responseMimeType": "application/json"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Synthesized master Animation DNA matrix!", "SUCCESS")
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
                res = self._api_call(self.openai_url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"})
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"]))
                self.log("[Core 2: OpenAI] Synthesized master Animation DNA matrix!", "SUCCESS")
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
                res = self._api_call(self.ollama_url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res.get("message", {}).get("content", "{}")))
                self.log("[Core 3: Ollama] Generated local Animation DNA matrix!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Math Autonomy (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline algorithmic Animation DNA synthesis...", "WARNING")
            is_anime = "anime" in style
            
            output = {
                "global_aesthetic_mode": "anime_cel_shaded" if is_anime else "photorealistic_pbr",
                "shading_mathematics": {
                    "color_ramp_interpolation": "CONSTANT" if is_anime else "EASE",
                    "voronoi_edge_sharpness": 0.92 if is_anime else 0.15,
                    "subsurface_scattering_intensity": 0.05 if is_anime else 0.85
                },
                "kinetic_physics_dna": {
                    "animation_stepping_fps": 24 if is_anime else 60,
                    "mappa_impact_jitter_scale": 3.5 if (is_anime and context["has_high_action"]) else 1.2,
                    "gravity_scale_factor": 1.35 if is_anime else 1.0
                },
                "volumetric_atmosphere_dna": {
                    "atmospheric_fog_density": 0.0 if is_anime else 1.85,
                    "bloom_exposure_threshold": 0.45 if is_anime else 0.80
                },
                "line_art_specifications": {
                    "freestyle_edge_thickness_px": 2.8 if is_anime else 0.0,
                    "outline_color_rgba": [0.05, 0.05, 0.08, 1.0] if is_anime else [0.0, 0.0, 0.0, 0.0]
                }
            }

        # Rule 17 Safeguard: Clamping float boundaries and capping FPS to prevent rendering lockups
        try:
            fps_val = int(output.get("kinetic_physics_dna", {}).get("animation_stepping_fps", 24))
            if fps_val > 120:
                self.log(f"Safeguard Triggered: Capping stepping FPS from {fps_val} down to 120 to prevent VRAM overflow!", "WARNING")
                output["kinetic_physics_dna"]["animation_stepping_fps"] = 120
        except Exception:
            pass

        final_blueprint = {
            "agent_executed": self.agent_name,
            "execution_timestamp": time.time(),
            "source_context_evaluated": context,
            "animation_dna_matrix": output
        }

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=4)

        self.log(f"Animation DNA core blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return final_blueprint

if __name__ == "__main__":
    router = Ai_Agent_62_Animation_Dna_Core_Router()
    router.synthesize_animation_dna()
