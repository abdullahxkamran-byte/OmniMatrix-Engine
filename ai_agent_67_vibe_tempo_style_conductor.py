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

class Ai_Agent_67_Vibe_Tempo_Style_Conductor:
    """
    OMNIMATRIX V2.0 GOD-LEVEL VIBE TEMPO & AUDIO-VISUAL STYLE CONDUCTOR
    Acts as the master acoustic and pacing director bridging Phonk action beats
    with atmospheric storytelling soundscapes. Synthesizes actionable parameter
    matrices for BPM tempo scaling, sidechain compression pumping, video cut
    cadence, and low-frequency impact drops across all audio-visual rendering nodes.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_67_Vibe_Tempo_Style_Conductor"
        self.workspace_dir = workspace_dir
        self.storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        self.animation_dna_path = os.path.join(self.workspace_dir, "62_animation_dna_blueprint.json")
        self.sakuga_path = os.path.join(self.workspace_dir, "66_sakuga_choreography_blueprint.json")
        self.output_blueprint_path = os.path.join(self.workspace_dir, "67_vibe_tempo_style_blueprint.json")
        
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
        """Rule 3: Idempotency scrubbing of previous tempo style blueprints."""
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
            # Hand off to Agent 68 (Visual Slots Panel Calculator - Pure Utility)
            data["orchestrator_matrix"]["next_agent"] = "Agent_68_Visual_Slots_Panel_Calculator"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_upstream_flow_context(self):
        """Ingests storyboard scenes, Animation DNA, and Sakuga combat directives."""
        context = {
            "scenes": [],
            "global_style": "anime_cel_shaded",
            "has_extreme_combat": False
        }

        if os.path.exists(self.storyboard_path):
            try:
                with open(self.storyboard_path, "r", encoding="utf-8") as f:
                    context["scenes"] = json.load(f).get("storyboard_panels", [])
            except Exception:
                pass

        if os.path.exists(self.animation_dna_path):
            try:
                with open(self.animation_dna_path, "r", encoding="utf-8") as f:
                    dna = json.load(f)
                context["global_style"] = dna.get("animation_dna_matrix", {}).get("global_aesthetic_mode", "anime_cel_shaded")
            except Exception:
                pass

        if os.path.exists(self.sakuga_path):
            try:
                with open(self.sakuga_path, "r", encoding="utf-8") as f:
                    sakuga = json.load(f)
                if len(sakuga.get("sakuga_sequences", [])) > 0:
                    context["has_extreme_combat"] = True
            except Exception:
                pass

        if not context["scenes"]:
            self.log("Storyboard sequence absent. Injecting baseline acoustic narrative scenes.", "INFO")
            context["scenes"] = [
                {"panel_id": 1, "description": "Atmospheric rain falling on a neon rooftop, quiet dialogue before the storm.", "emotional_tone": "AMBIENT_CHILL"},
                {"panel_id": 2, "description": "Explosive phonk beat drop as protagonist dashes forward into high-speed combat.", "emotional_tone": "BURNING_PHONK_ACTION"}
            ]

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
    # RULE 6, 14, 15, 17: QUAD-CORE TEMPO & STYLE SYNTHESIZER
    # =====================================================================
    def synthesize_tempo_style_matrix(self):
        self._handshake("IN_PROGRESS")
        context = self._load_upstream_flow_context()
        
        self.log(f"Quad-Core Vibe Tempo Forge Initiated. Scenes: {len(context['scenes'])} | Combat Mode: {context['has_extreme_combat']}")

        # Rule 15: Limitless continuous audio-visual flow parameter formulation
        prompt = (
            f"You are OMNIMATRIX Chief Audio-Visual Flow Conductor. Global Style: '{context['global_style']}', Extreme Combat: {context['has_extreme_combat']}.\n"
            "Take storyboard scenes and synthesize a 'Vibe Tempo & Style Blueprint' to orchestrate audio BPM, video cuts, and sidechain compression.\n"
            "CRITICAL FLOW RULES:\n"
            "1. If mood is PHONK / ACTION: Enforce high BPM (135 to 175), aggressive sidechain pumping ('sidechain_compression_ratio' 4.0 to 8.0), fast video cuts every 12 to 24 frames, and heavy sub-bass impact drops (30Hz to 60Hz).\n"
            "2. If mood is AMBIENT / CHILL: Enforce slower BPM (65 to 95), atmospheric reverb, long cinematic takes (96 to 240+ frames), and zero sidechain pumping (1.0).\n"
            "Output STRICTLY a JSON object with key 'tempo_flow_sequences' containing a list of objects with:\n"
            "- 'target_scene_id': integer matching panel ID.\n"
            "- 'acoustic_genre_mode': string ('phonk_aggressive', 'ambient_cinematic', 'orchestral_epic', or 'synthwave_retro').\n"
            "- 'target_bpm_tempo': integer (60 to 180 defining musical speed).\n"
            "- 'video_cut_cadence_frames': integer (8 to 240 defining editing cut speed at 24fps baseline).\n"
            "- 'sidechain_compression_ratio': float (1.0 for flat, 2.0 to 8.0 for heavy beat pumping against voiceover).\n"
            "- 'sub_bass_impact_freq_hz': integer (20 to 80 defining low-frequency drop triggers).\n"
            "- 'reverb_space_depth': float (0.0 for dry studio, 0.5 to 1.0 for massive cathedral/cyberpunk space).\n"
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
                    "generationConfig": {"temperature": 0.84, "responseMimeType": "application/json"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Synthesized master Vibe Tempo flow choreography!", "SUCCESS")
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
                self.log("[Core 2: OpenAI] Synthesized master Vibe Tempo flow choreography!", "SUCCESS")
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
                self.log("[Core 3: Ollama] Generated local Vibe Tempo flow choreography!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Math & Tempo Alchemist Autonomy (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline algorithmic tempo flow synthesis...", "WARNING")
            sequences = []

            for idx, scene in enumerate(context["scenes"]):
                s_id = scene.get("panel_id", idx + 1)
                desc = str(scene.get("description", "")).upper()
                tone = str(scene.get("emotional_tone", "")).upper()
                
                is_phonk_action = any(k in desc or k in tone for k in ["PHONK", "ACTION", "FIGHT", "DASH", "CLIMAX", "SHOWDOWN", "FAST"])
                is_epic_orch = any(k in desc or k in tone for k in ["EPIC", "REVEAL", "ORCHESTRAL", "HERO", "TRANSFORMATION"])

                if is_phonk_action or context["has_extreme_combat"]:
                    genre, bpm, cuts, ratio, sub, rev = "phonk_aggressive", 155, 14, 5.5, 38, 0.15
                elif is_epic_orch:
                    genre, bpm, cuts, ratio, sub, rev = "orchestral_epic", 115, 60, 2.5, 45, 0.65
                else:
                    genre, bpm, cuts, ratio, sub, rev = "ambient_cinematic", 75, 144, 1.0, 60, 0.85

                sequences.append({
                    "target_scene_id": s_id,
                    "acoustic_genre_mode": genre,
                    "target_bpm_tempo": bpm,
                    "video_cut_cadence_frames": cuts,
                    "sidechain_compression_ratio": ratio,
                    "sub_bass_impact_freq_hz": sub,
                    "reverb_space_depth": rev
                })
            output = {"tempo_flow_sequences": sequences}

        # Rule 17 Safeguard: Cap at 50 flow segments and prevent hyper-fast strobe cuts (< 6 frames)
        flow_list = output.get("tempo_flow_sequences", [])[:50]
        for seq in flow_list:
            if int(seq.get("video_cut_cadence_frames", 24)) < 6:
                self.log(f"Safeguard Triggered: Capping cut cadence from {seq['video_cut_cadence_frames']} up to 6 frames to prevent strobe seizure / buffer overflow!", "WARNING")
                seq["video_cut_cadence_frames"] = 6

        final_blueprint = {
            "agent_executed": self.agent_name,
            "execution_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "style_mode_evaluated": context["global_style"],
            "total_tempo_segments_mapped": len(flow_list),
            "tempo_flow_sequences": flow_list
        }

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=4)

        self.log(f"Vibe Tempo flow blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return final_blueprint

if __name__ == "__main__":
    conductor = Ai_Agent_67_Vibe_Tempo_Style_Conductor()
    conductor.synthesize_tempo_style_matrix()
