import os
import re
import sys
import json
import time
import psutil
import urllib.request
import urllib.error
from datetime import datetime

# =====================================================================
# RULE 2 & 14: UNIVERSAL PATH ISOLATION & DUAL-CASE ENV LOADING
# =====================================================================
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key_str = key.strip()
                    val_str = val.strip().strip('"').strip("'")
                    os.environ[key_str.upper()] = val_str
                    os.environ[key_str.lower()] = val_str

load_env_file()

class Ai_Agent_65_Supreme_Creative_Script_Conductor:
    """
    OMNIMATRIX V2.0 GOD-LEVEL AGENT 65 — SUPREME CREATIVE SCRIPT CONDUCTOR
    
    Role:
    1. Ingests raw narrative script (from Module A) and custom creative overrides.
    2. Synthesizes high-level sakuga choreography, lighting themes, and camera directives.
    3. Outputs both '65_creative_brief.json' and '65_master_conductor_timeline.json'.
    4. Executes Atomic Handshake to pass directives to Agent 68 and Agent 00.
    5. Employs Quad-Core LLM Engine (Gemini -> HuggingFace -> Ollama -> Core 4 Fallback).
    """

    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "ai_agent_65_supreme_creative_script_conductor"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        os.makedirs(self.workspace_dir, exist_ok=True)

        # File IO Paths
        self.input_script_path = os.path.join(self.workspace_dir, "08_formatted_script.json")
        self.config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        self.output_brief_path = os.path.join(self.workspace_dir, "65_creative_brief.json")
        self.output_timeline_path = os.path.join(self.workspace_dir, "65_master_conductor_timeline.json")
        self.log_file_path = os.path.join(self.workspace_dir, "65_conductor_telemetry.log")
        self.matrix_state_path = os.path.join(self.workspace_dir, "matrix_state.json")

        self.max_timeline_slices = 40
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] [{level}] [{self.agent_name}] {message}"
        print(formatted)
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")
        except Exception:
            pass

    def _get_hardware_telemetry(self):
        try:
            mem = psutil.virtual_memory()
            return f"RAM: {mem.percent}% used | Avail: {mem.available / (1024**2):.1f} MB"
        except Exception:
            return "Hardware Telemetry Active"

    # =====================================================================
    # RULE 3: IDEMPOTENCY SCRUBBING
    # =====================================================================
    def _scrub_legacy_assets(self):
        for target in [self.output_brief_path, self.output_timeline_path]:
            if os.path.exists(target):
                try:
                    os.remove(target)
                    self.log(f"Scrubbed legacy output file: {target}")
                except Exception as e:
                    self.log(f"Failed to remove legacy target {target}: {e}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE SYNCHRONIZATION
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS", total_segments=0):
        data = {}
        if os.path.exists(self.matrix_state_path):
            try:
                with open(self.matrix_state_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass

        if "orchestrator_matrix" not in data:
            data["orchestrator_matrix"] = {}

        data["orchestrator_matrix"].update({
            "last_active_agent": self.agent_name,
            "last_update_timestamp": time.time(),
            "master_timeline_segments_mapped": total_segments,
            "agent_status": {self.agent_name: status}
        })

        if status == "COMPLETED":
            data["orchestrator_matrix"]["next_agent"] = "ai_agent_68_dynamic_task_architect"

        try:
            with open(self.matrix_state_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.log(f"Atomic handshake write failure: {e}", "ERROR")

    # =====================================================================
    # SCRIPT & CONFIG INGESTION
    # =====================================================================
    def _load_upstream_context(self):
        script_data = {
            "title": "Domain Expansion Climax",
            "voice_over_script": "Infinite space collapses as cursed power reaches critical mass.",
            "duration_seconds": 10.0
        }
        if os.path.exists(self.input_script_path):
            try:
                with open(self.input_script_path, "r", encoding="utf-8") as f:
                    script_data = json.load(f)
                    self.log("Upstream script successfully ingested from Module A.", "SUCCESS")
            except Exception as e:
                self.log(f"Script ingestion exception: {e}. Using baseline fallback script.", "WARNING")

        global_style = "anime_cel_shaded"
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    global_style = cfg.get("global_style", global_style)
            except Exception:
                pass

        return script_data, global_style

    # =====================================================================
    # RULE 5: BULLETPROOF JSON REGEX SCRUBBER
    # =====================================================================
    def _clean_json(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            return cleaned[start_idx:end_idx + 1]
        return cleaned

    def _heal_broken_json(self, json_string):
        try:
            return json.loads(json_string)
        except Exception as e:
            self.log(f"JSON Decode Warning: {e}. Attempting structural balance...", "WARNING")
            repaired = json_string.strip()
            if not repaired.endswith("}"):
                if repaired.count("[") > repaired.count("]"):
                    repaired += "]"
                if repaired.count("{") > repaired.count("}"):
                    repaired += "}"
            try:
                return json.loads(repaired)
            except Exception:
                return None

    # =====================================================================
    # RULE 6 & 16: QUAD-CORE CREATIVE INTELLIGENCE NODE
    # =====================================================================
    def query_creative_intelligence(self, system_prompt, user_prompt):
        gemini_key = os.environ.get("GEMINI_API_KEY", os.environ.get("gemini_api_key", ""))
        hf_token = os.environ.get("HF_TOKEN", os.environ.get("hf_token", ""))

        payload = {
            "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }

        # CORE 1: GOOGLE GEMINI API (HTTP REST)
        if gemini_key and gemini_key.startswith("AIzaSy"):
            self.log("Querying Core 1: Google Gemini AI Engine...", "INFO")
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={gemini_key}"
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                with urllib.request.urlopen(req, timeout=12) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    self.log("Core 1 (Gemini) generated creative directives successfully.", "SUCCESS")
                    return self._clean_json(raw_text)
            except Exception as e:
                self.log(f"Core 1 (Gemini) failed: {e}. Falling back to Core 2...", "WARNING")

        # CORE 2: HUGGING FACE INFERENCE ENGINE
        if hf_token:
            self.log("Querying Core 2: HuggingFace Inference LLM Engine...", "INFO")
            try:
                hf_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
                headers = {"Authorization": f"Bearer {hf_token}", "Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")}
                hf_payload = {"inputs": f"<s>[INST] {system_prompt}\n{user_prompt} Respond strictly in JSON format. [/INST]"}
                req = urllib.request.Request(hf_url, data=json.dumps(hf_payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    gen_text = data[0].get("generated_text", "")
                    self.log("Core 2 (HuggingFace) generated creative directives successfully.", "SUCCESS")
                    return self._clean_json(gen_text)
            except Exception as e:
                self.log(f"Core 2 (HuggingFace) failed: {e}. Falling back to Core 3...", "WARNING")

        # CORE 3: LOCAL OLLAMA ENGINE
        self.log("Querying Core 3: Local Hardware Intelligence (Ollama)...", "INFO")
        try:
            ollama_url = "http://localhost:11434/api/generate"
            ollama_payload = {"model": "mistral", "prompt": f"{system_prompt}\n{user_prompt}", "stream": False, "format": "json"}
            req = urllib.request.Request(ollama_url, data=json.dumps(ollama_payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self.log("Core 3 (Ollama) generated local directives.", "SUCCESS")
                return self._clean_json(data.get("response", ""))
        except Exception as e:
            self.log(f"Core 3 (Ollama) offline: {e}. Engaging Core 4 Procedural Engine.", "INFO")

        # CORE 4: PROCEDURAL FALLBACK
        return None

    # =====================================================================
    # RULE 10: PROCEDURAL CREATIVE FALLBACK SYNTHESIZER
    # =====================================================================
    def execute_procedural_fallback(self, script_data, global_style, user_prompt):
        self.log("Engaging Core 4: Procedural Creative Synthesis Engine...", "WARNING")
        total_duration = float(script_data.get("duration_seconds", 10.0))
        half_dur = round(total_duration / 2.0, 2)

        return {
            "scenario_title": script_data.get("title", "Procedural Domain Climax"),
            "global_parameters": {
                "global_style": global_style,
                "primary_lighting_theme": "High contrast cyan and violet volumetric plasma illumination",
                "environment_geometry": "Levitating basalt slabs with kinetic gravitational distortions",
                "vfx_atmosphere": "Volumetric energy particles, directional speed lines, shockwave pulses"
            },
            "character_set": [
                {
                    "character_name": "Gojo Satoru",
                    "clothing_details": "High-collar dark uniform",
                    "initial_pose": "Unlimited Void finger cross stance"
                },
                {
                    "character_name": "Sukuna",
                    "clothing_details": "Ripped kimono with cursed tattoo markings",
                    "initial_pose": "Four-armed stance with malevolent aura"
                }
            ],
            "master_directives": [
                {
                    "segment_id": 1,
                    "duration_slice": half_dur,
                    "action_choreography": f"Gojo unleashes domain expansion. Sukuna initiates supersonic counter slash. Prompt: {user_prompt}",
                    "environment_state": "Ground fractures violently under kinetic pressure.",
                    "camera_rig_behavior": "dramatic_orbital_zoom",
                    "orchestrated_agent_commands": {
                        "agent_14_phonk_beat_sync": "slow_mo_rise",
                        "agent_22_lighting_shader": "ambient_dark_purple",
                        "agent_30_fracture_engine": "ground_cracking_frame_12"
                    }
                },
                {
                    "segment_id": 2,
                    "duration_slice": half_dur,
                    "action_choreography": "Hollow Purple singularity engulfs central combat plane into annihilation.",
                    "environment_state": "Structural elements vaporize into glowing sub-atomic dust.",
                    "camera_rig_behavior": "shaky_handheld_track",
                    "orchestrated_agent_commands": {
                        "agent_14_phonk_beat_sync": "bass_drop_shake",
                        "agent_22_lighting_shader": "high_contrast_rim_light",
                        "agent_30_fracture_engine": "absolute_destruction"
                    }
                }
            ]
        }

    # =====================================================================
    # MAIN EXECUTION
    # =====================================================================
    def run_choreography_pipeline(self, override_prompt=None):
        self._handshake("IN_PROGRESS")
        self.log("=====================================================================")
        self.log("ACTIVATING AGENT 65: SUPREME CREATIVE SCRIPT CONDUCTOR")
        self.log("=====================================================================")
        self.log(f"Telemetry Check: {self._get_hardware_telemetry()}")

        script_data, global_style = self._load_upstream_context()

        if override_prompt:
            user_prompt = override_prompt
        else:
            user_prompt = "Generate an ultra-cinematic, high-octane anime sakuga fight climax with intense camera movement."

        system_instruction = (
            "You are OmniMatrix Supreme Creative Script Conductor.\n"
            "Decompose the input script into a master execution timeline.\n"
            "Output strictly valid JSON with keys: 'scenario_title', 'global_parameters', 'character_set', 'master_directives'."
        )
        user_context = f"Target Script:\n{json.dumps(script_data, indent=2)}\n\nStyle: {global_style}\nDirectives: {user_prompt}"

        raw_response = self.query_creative_intelligence(system_instruction, user_context)

        timeline_data = None
        if raw_response:
            timeline_data = self._heal_broken_json(raw_response)

        if not timeline_data or not isinstance(timeline_data, dict):
            timeline_data = self.execute_procedural_fallback(script_data, global_style, user_prompt)

        directives = timeline_data.get("master_directives", [])[:self.max_timeline_slices]
        timeline_data["master_directives"] = directives

        # 1. Output Master Timeline
        with open(self.output_timeline_path, "w", encoding="utf-8") as f:
            json.dump(timeline_data, f, indent=4)
        self.log(f"Master Conductor timeline written to: '{self.output_timeline_path}'", "SUCCESS")

        # 2. Output Creative Brief for Agent 68
        creative_brief = {
            "agent_id": "65",
            "agent_name": self.agent_name,
            "timestamp": time.time(),
            "scenario_title": timeline_data.get("scenario_title", "Untitled Climax"),
            "global_style": global_style,
            "global_parameters": timeline_data.get("global_parameters", {}),
            "character_set": timeline_data.get("character_set", []),
            "total_directives": len(directives)
        }
        with open(self.output_brief_path, "w", encoding="utf-8") as f:
            json.dump(creative_brief, f, indent=4)
        self.log(f"Creative brief written to: '{self.output_brief_path}'", "SUCCESS")

        # Atomic Handshake Completion
        self._handshake("COMPLETED", len(directives))

        # Terminal Summary Report
        print("\n=====================================================================")
        print("         OMNIMATRIX V2.0 — SUPREME CONDUCTOR DIRECTIVES LOCKED       ")
        print("=====================================================================")
        print(f"SCENARIO TITLE : {timeline_data.get('scenario_title', 'Untitled')}")
        print(f"GLOBAL STYLE   : {global_style}")
        print(f"TOTAL SLICES   : {len(directives)}")
        print("=====================================================================\n")

if __name__ == "__main__":
    conductor = Ai_Agent_65_Supreme_Creative_Script_Conductor()
    conductor.run_choreography_pipeline()