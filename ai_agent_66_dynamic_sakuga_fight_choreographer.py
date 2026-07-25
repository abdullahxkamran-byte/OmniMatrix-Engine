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

class Ai_Agent_66_Dynamic_Sakuga_Fight_Choreographer:
    """
    OMNIMATRIX V2.0 GOD-LEVEL DYNAMIC SAKUGA FIGHT CHOREOGRAPHER
    Acts as an absolute being of action direction, synthesizing MAPPA and Ufotable
    combat aesthetics. Evaluates kinetic trajectories to generate actionable
    directives for hit-stop frame freezing, dynamic mesh smearing, camera impact
    shaking, and procedural debris velocities across high-octane battle sequences.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_66_Dynamic_Sakuga_Fight_Choreographer"
        self.workspace_dir = workspace_dir
        self.storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        self.animation_dna_path = os.path.join(self.workspace_dir, "62_animation_dna_blueprint.json")
        self.output_blueprint_path = os.path.join(self.workspace_dir, "66_sakuga_choreography_blueprint.json")
        
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
        """Rule 3: Idempotency scrubbing of previous combat choreography blueprints."""
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
            # Hand off to Ai Agent 67 (Vibe Tempo Style Conductor)
            data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_67_Vibe_Tempo_Style_Conductor"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_combat_context(self):
        """Ingests storyboard sequences and Animation DNA stylistic constraints."""
        scenes = []
        style_mode = "anime_cel_shaded"

        if os.path.exists(self.storyboard_path):
            try:
                with open(self.storyboard_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                scenes = data.get("storyboard_panels", [])
            except Exception as error:
                self.log(f"Storyboard ingestion exception: {error}", "WARNING")

        if os.path.exists(self.animation_dna_path):
            try:
                with open(self.animation_dna_path, "r", encoding="utf-8") as f:
                    dna = json.load(f)
                style_mode = dna.get("animation_dna_matrix", {}).get("global_aesthetic_mode", "anime_cel_shaded").lower()
            except Exception:
                pass

        if not scenes:
            self.log("Storyboard sequence absent. Injecting baseline high-octane combat scenes.", "INFO")
            scenes = [
                {"panel_id": 1, "description": "Protagonist executes a supersonic sword draw, shattering the sonic barrier with violet lightning.", "emotional_tone": "HYPED_CLIMAX"},
                {"panel_id": 2, "description": "Colossal brutal fist collision erupts into a spherical kinetic shockwave across the arena.", "emotional_tone": "EPIC_SHOWDOWN"}
            ]

        return scenes, style_mode

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
    # RULE 6, 14, 15, 17: QUAD-CORE SAKUGA CHOREOGRAPHER SYNTHESIZER
    # =====================================================================
    def choreograph_fight_sequence(self):
        self._handshake("IN_PROGRESS")
        scenes, style_mode = self._load_combat_context()
        
        self.log(f"Quad-Core Sakuga Combat Forge Initiated. Scenes to Choreograph: {len(scenes)} | Style: [{style_mode.upper()}]")

        # Rule 15: Limitless continuous combat parameter formulation
        prompt = (
            f"You are OMNIMATRIX Chief Action Choreographer and Keyframe Director. Global Aesthetic Enforced: '{style_mode}'.\n"
            "Take raw visual combat scenes and synthesize a 'Sakuga Choreography Blueprint' to guide 3D rigging, camera jitter, and physics.\n"
            "CRITICAL COMBAT RULES:\n"
            "1. Evaluate physical impact, weapon speed, and shockwave intensity.\n"
            "2. If action is intense: Enforce hit-stop freezing ('impact_freeze_duration_frames' between 4 and 12) to deliver bone-crushing weight.\n"
            "3. Enforce dynamic mesh stretching ('smear_frame_intensity' 0.5 to 1.0) for rapid dashes to mimic classic 2D sakuga blur.\n"
            "Output STRICTLY a JSON object with key 'sakuga_sequences' containing a list of objects with:\n"
            "- 'target_segment_id': integer matching the scene/panel ID.\n"
            "- 'pose_velocity_multiplier': float (1.0 to 5.0 defining physical dash/strike speed).\n"
            "- 'impact_freeze_duration_frames': integer (0 to 12 defining exact hit-stop frame holds).\n"
            "- 'camera_impact_shake_amplitude': float (0.0 to 4.5 defining F-curve screen distortion).\n"
            "- 'inverse_color_impact_frame': boolean (true/false triggering 1-frame black/white inversion on major power releases).\n"
            "- 'smear_frame_intensity': float (0.0 to 1.0 defining procedural geometry stretching).\n"
            "- 'speed_lines_density': string ('none', 'low_radial', 'heavy_linear_horizontal', or 'explosive_spherical').\n"
            "- 'physics_debris_velocity_vector': array of exactly 3 floats [X, Y, Z] representing shattering stone/particle force directions.\n"
            "Zero compression or placeholders allowed."
        )

        user_msg = json.dumps({"style_mode_enforced": style_mode, "combat_scenes_sequence": scenes})
        output = None

        # Core 1: Gemini (Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"{prompt}\n\nUser Context:\n{user_msg}"}]}],
                    "generationConfig": {"temperature": 0.88, "responseMimeType": "application/json"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Synthesized master Sakuga combat choreography!", "SUCCESS")
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
                self.log("[Core 2: OpenAI] Synthesized master Sakuga combat choreography!", "SUCCESS")
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
                self.log("[Core 3: Ollama] Generated local Sakuga combat choreography!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Math & Combat Alchemist Autonomy (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline algorithmic Sakuga physics synthesis...", "WARNING")
            sequences = []

            for idx, scene in enumerate(scenes):
                s_id = scene.get("panel_id", idx + 1)
                desc = str(scene.get("description", "")).upper()
                tone = str(scene.get("emotional_tone", "")).upper()
                
                is_heavy_impact = any(k in desc or k in tone for k in ["SHOCKWAVE", "EXPLOSION", "COLLISION", "SMASH", "BLAST", "CLIMAX", "SHOWDOWN"])
                is_fast_slash = any(k in desc for k in ["DASH", "SLASH", "SWORD", "SPEED", "LIGHTNING", "SUPERSONIC"])

                if is_heavy_impact:
                    vel, freeze, shake, inv, smear, lines, vec = 4.2, 10, 3.8, True, 0.65, "explosive_spherical", [0.0, 22.5, 8.0]
                elif is_fast_slash:
                    vel, freeze, shake, inv, smear, lines, vec = 4.8, 6, 2.4, False, 0.95, "heavy_linear_horizontal", [15.0, 0.0, 2.0]
                else:
                    vel, freeze, shake, inv, smear, lines, vec = 1.6, 0, 0.5, False, 0.15, "low_radial", [0.0, 0.0, 0.0]

                sequences.append({
                    "target_segment_id": s_id,
                    "pose_velocity_multiplier": vel,
                    "impact_freeze_duration_frames": freeze,
                    "camera_impact_shake_amplitude": shake,
                    "inverse_color_impact_frame": inv,
                    "smear_frame_intensity": smear,
                    "speed_lines_density": lines,
                    "physics_debris_velocity_vector": vec
                })
            output = {"sakuga_sequences": sequences}

        # Rule 17 Safeguard: Cap at 50 combat segments and enforce safe frame freeze ceilings
        sequences_list = output.get("sakuga_sequences", [])[:50]
        for seq in sequences_list:
            if int(seq.get("impact_freeze_duration_frames", 0)) > 12:
                self.log(f"Safeguard Triggered: Capping impact freeze from {seq['impact_freeze_duration_frames']} down to 12 frames to prevent timing lockup!", "WARNING")
                seq["impact_freeze_duration_frames"] = 12

        final_blueprint = {
            "agent_executed": self.agent_name,
            "execution_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "aesthetic_mode_evaluated": style_mode,
            "total_combat_segments_choreographed": len(sequences_list),
            "sakuga_sequences": sequences_list
        }

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=4)

        self.log(f"Sakuga combat choreography blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return final_blueprint

if __name__ == "__main__":
    choreographer = Ai_Agent_66_Dynamic_Sakuga_Fight_Choreographer()
    choreographer.choreograph_fight_sequence()
