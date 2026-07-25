import os
import re
import sys
import json
import time
import shutil
import platform
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

# Attempt importing Google Gemini SDK for supreme narrative architecture
try:
    import google.generativeai as genai
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False

# =====================================================================
# RULE 2: UNIVERSAL ENVIRONMENT CONFIGURATION (PURE UTILITY)
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

class Ai_Agent_65_Supreme_Creative_Script_Conductor:
    """
    OMNIMATRIX V2.0 GOD-LEVEL SUPREME CREATIVE SCRIPT CONDUCTOR
    Acts as the commander-in-chief and master visual art director for the entire
    67-agent network. Ingests raw story scripts and user direction prompts,
    decomposing narrative arcs into chronological execution timelines. Synthesizes
    actionable directives for 3D lighting, kinetic rigging, phonk audio beats,
    and procedural mesh destruction across all downstream specialized engines.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_65_Supreme_Creative_Script_Conductor"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        # System IO paths
        self.input_script_path = os.path.join(self.workspace_dir, "08_formatted_script.json")
        self.output_directive_path = os.path.join(self.workspace_dir, "65_master_conductor_timeline.json")
        self.log_file_path = os.path.join(self.workspace_dir, "65_conductor_telemetry.log")
        
        # Rule 17: Memory and timeline segment ceiling safeguard
        self.max_timeline_slices = 40
        
        # API credentials & configurations
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        
        if GEMINI_SDK_AVAILABLE and self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o"

        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        formatted = f"[{level}] [{self.agent_name}] {message}"
        print(formatted)
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")
        except Exception:
            pass

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous master conductor timelines."""
        if os.path.exists(self.output_directive_path):
            try:
                os.remove(self.output_directive_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy timeline {self.output_directive_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & PIPELINE ROUTING
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS", total_segments=0):
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
            "master_timeline_segments_mapped": total_segments,
            "agent_status": {self.agent_name: status}
        })
        
        if status == "COMPLETED":
            # Hand off to THE FINAL BOSS: Agent 00 (Universal Pipeline Orchestrator)
            data["orchestrator_matrix"]["next_agent"] = "Agent_00_Universal_Pipeline_Orchestrator"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_raw_script(self):
        """Ingests pre-compiled narrative scripts from Module A."""
        if os.path.exists(self.input_script_path):
            try:
                with open(self.input_script_path, "r", encoding="utf-8") as f:
                    self.log("Upstream narrative script ingested successfully from Module A.", "SUCCESS")
                    return json.load(f)
            except Exception as error:
                self.log(f"Script ingestion exception: {error}. Synthesizing baseline combat structure.", "WARNING")
        
        return {
            "title": "Dimensional Convergence Showdown",
            "voice_over_script": "The celestial barrier shatters as supreme forces collide. There is no retreat, only absolute dominion.",
            "duration_seconds": 16.0
        }

    def _clean_json(self, raw_text):
        """Rule 5: Bulletproof JSON scrubber."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            return cleaned[start_idx:end_idx + 1]
        return cleaned

    def _heal_broken_json(self, json_string):
        """Executes structural repairs on malformed LLM responses to ensure compilation."""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as error:
            self.log(f"JSON structural integrity bug detected: {error}. Engaging bracket balancing repairs...", "WARNING")
            repaired = json_string.strip()
            if not repaired.endswith("}"):
                if repaired.count("[") > repaired.count("]"):
                    repaired += "]"
                if repaired.count("{") > repaired.count("}"):
                    repaired += "}"
            try:
                return json.loads(repaired)
            except Exception:
                self.log("Automatic JSON bracket balancing failed. Routing to procedural fallback engine.", "ERROR")
                return None

    def build_creative_prompt(self, raw_script, user_prompt):
        """Formulates an exhaustive system instruction sequence for multi-model intelligence."""
        system_instruction = (
            "You are OMNIMATRIX Supreme Creative Script Conductor, Cinematographer, and Combat Choreographer.\n"
            "Your objective is to decompose a narrative script and user visual instructions into a chronological master execution timeline.\n"
            "CRITICAL DIRECTIVES:\n"
            "1. Allocate precise action choreography, lighting themes, and camera F-curve behaviors for every scene slice.\n"
            "2. Dictate explicit commands for downstream specialized agents (e.g., Agent 14 phonk beat drops, Agent 22 lighting shaders, Agent 30 mesh fractures).\n"
            "3. Ensure the sum of all 'duration_slice' fields matches the target video duration.\n"
            "Output STRICTLY a JSON object matching this exact structural template:\n"
            "{\n"
            "  \"scenario_title\": \"The Ultimate Climax - Battle of the Heavens\",\n"
            "  \"global_parameters\": {\n"
            "    \"primary_lighting_theme\": \"Dark gothic midnight blue with vivid cyan and violet rim lighting\",\n"
            "    \"environment_geometry\": \"Shattered urban megalopolis with suspended concrete fragments in anti-gravity\",\n"
            "    \"vfx_atmosphere\": \"Volumetric plasma dust, spatial optical distortion, high-frequency kinetic sparks\"\n"
            "  },\n"
            "  \"character_set\": [\n"
            "    {\"character_name\": \"Gojo Satoru\", \"clothing_details\": \"Black high-collar Jujutsu uniform\", \"initial_pose\": \"Floating calmly three feet off the ground, fingers crossed in the Unlimited Void sign\"},\n"
            "    {\"character_name\": \"Ryomen Sukuna\", \"clothing_details\": \"Ripped kimono with cursed markings\", \"initial_pose\": \"Standing on ruined concrete, four arms active, expressions of pure shock\"}\n"
            "  ],\n"
            "  \"master_directives\": [\n"
            "    {\n"
            "      \"segment_id\": 1,\n"
            "      \"duration_slice\": 8.0,\n"
            "      \"action_choreography\": \"Gojo triggers Red and Blue simultaneously. Swirling gravitational vortex erupts between his hands. Sukuna attempts supersonic slash but is pulled off balance by spatial curvature.\",\n"
            "      \"environment_state\": \"Floating concrete chunks accelerate into orbital velocity around Gojo. Ground collapses inward into an abyssal crater.\",\n"
            "      \"camera_rig_behavior\": \"dramatic_orbital_zoom\",\n"
            "      \"orchestrated_agent_commands\": {\n"
            "        \"agent_14_phonk_beat_sync\": \"slow_mo_rise\",\n"
            "        \"agent_22_lighting_shader\": \"ambient_dark_purple\",\n"
            "        \"agent_30_fracture_engine\": \"ground_cracking_frame_24\"\n"
            "      }\n"
            "    },\n"
            "    {\n"
            "      \"segment_id\": 2,\n"
            "      \"duration_slice\": 8.0,\n"
            "      \"action_choreography\": \"Gojo unleashes Hollow Purple, obliterating the central spatial plane. Sukuna is engulfed in a blinding violet singularity blast. Gojo touches down effortlessly.\",\n"
            "      \"environment_state\": \"Intense purple plasma reflecting across all debris. Background structures vaporize into glowing sub-atomic ash particles.\",\n"
            "      \"camera_rig_behavior\": \"shaky_handheld_track\",\n"
            "      \"orchestrated_agent_commands\": {\n"
            "        \"agent_14_phonk_beat_sync\": \"bass_drop_shake\",\n"
            "        \"agent_22_lighting_shader\": \"high_contrast_rim_light\",\n"
            "        \"agent_30_fracture_engine\": \"absolute_destruction\"\n"
            "      }\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "Zero conversational text or markdown code wraps allowed."
        )
        user_context = f"Target Narrative Script:\n{json.dumps(raw_script, indent=2)}\n\nUser Choreography Override:\n{user_prompt}"
        return system_instruction, user_context

    # =====================================================================
    # RULE 6, 14, 16: QUAD-CORE CREATIVE INTELLIGENCE NODE
    # =====================================================================
    def query_creative_intelligence(self, system_prompt, user_prompt):
        # Core 1: Gemini SDK Pro
        if GEMINI_SDK_AVAILABLE and self.gemini_key:
            self.log("Querying Primary Cloud Intelligence Node (Gemini 1.5 Pro)...", "INFO")
            try:
                model = genai.GenerativeModel("gemini-1.5-pro")
                res = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
                self.log("[Core 1: Gemini] Synthesized master conductor timeline!", "SUCCESS")
                return self._clean_json(res.text)
            except Exception as error:
                self.log(f"[Core 1: Gemini] Exception: {error}. Routing to OpenAI...", "WARNING")

        # Core 2: OpenAI Failsafe
        if self.openai_key:
            self.log("Querying Secondary Cloud Intelligence Node (OpenAI GPT-4o)...", "INFO")
            try:
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"}
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "response_format": {"type": "json_object"}}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_body = json.loads(response.read().decode("utf-8"))
                    self.log("[Core 2: OpenAI] Synthesized master conductor timeline!", "SUCCESS")
                    return self._clean_json(res_body["choices"][0]["message"]["content"])
            except Exception as error:
                self.log(f"[Core 2: OpenAI] Exception: {error}. Routing to Ollama...", "WARNING")

        # Core 3: Ollama Local Fallback
        self.log("Querying Local Hardware Intelligence Node (Ollama Llama3)...", "INFO")
        try:
            headers = {"Content-Type": "application/json"}
            payload = {"model": self.model_local, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "stream": False, "format": "json"}
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=50) as response:
                res_body = json.loads(response.read().decode("utf-8"))
                self.log("[Core 3: Ollama] Generated local conductor timeline!", "SUCCESS")
                return self._clean_json(res_body["message"]["content"])
        except Exception as error:
            self.log(f"[Core 3: Ollama] Offline: {error}. Reverting to offline procedural Alchemist backup.", "ERROR")
            return None

    # =====================================================================
    # RULE 10: OFFLINE PROCEDURAL BATTLE ALCHEMIST FALLBACK
    # =====================================================================
    def execute_procedural_fallback(self, raw_script, user_prompt):
        """Synthesizes a high-octane battle timeline when all cloud and local AI endpoints are offline."""
        self.log("Engaging offline procedural Battle Alchemist timeline generator...", "WARNING")
        total_duration = float(raw_script.get("duration_seconds", 16.0))
        half_dur = round(total_duration / 2.0, 2)
        
        return {
            "scenario_title": f"Procedural Showdown — {raw_script.get('title', 'Apex Override')}",
            "global_parameters": {
                "primary_lighting_theme": "High-contrast neon crimson and plasma orange flares",
                "environment_geometry": "Shattering basalt monoliths with reflective aqueous surfaces",
                "vfx_atmosphere": "Volumetric smoke columns, directional tempest currents, glowing embers"
            },
            "character_set": [
                {"character_name": "Apex Vanguard", "clothing_details": "Armored cybernetic battlesuit", "initial_pose": "Crouched in low kinetic launch stance"},
                {"character_name": "Abyssal Sovereign", "clothing_details": "Dark obsidian plate armor", "initial_pose": "Levitating with gravitational aura emanating"}
            ],
            "master_directives": [
                {
                    "segment_id": 1,
                    "duration_slice": half_dur,
                    "action_choreography": f"Vanguard initiates supersonic linear dash. Sovereign channels sphere of destruction. Context: '{user_prompt}'",
                    "environment_state": "Monoliths begin fracturing from acoustic pressure; water rippling violently.",
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
                    "action_choreography": "Kinetic collision erupts into hemispherical shockwave. Vanguard pierces defensive singularity to secure victory.",
                    "environment_state": "Pillars completely disintegrate into orbital rubble; sky illuminates with plasma beams.",
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
    # ACTIONABLE TIMELINE COMPILER & TERMINAL PRESENTATION
    # =====================================================================
    def run_choreography_pipeline(self, override_prompt=None):
        self._handshake("IN_PROGRESS")
        self.log("System Operational. Initiating Supreme Creative Script Conductor...")
        
        raw_script = self._load_raw_script()
        
        if override_prompt:
            user_prompt = override_prompt
        else:
            print("\n" + "=" * 75)
            user_prompt = input("Enter custom action choreography or lore directives [Press Enter for Auto-Climax]: ").strip()
            print("=" * 75)
            
        if not user_prompt:
            user_prompt = "Generate an ultra-cinematic, high-octane action showdown with extreme sakuga choreography."
            
        sys_prompt, user_context = self.build_creative_prompt(raw_script, user_prompt)
        raw_response = self.query_creative_intelligence(sys_prompt, user_context)
        
        timeline_data = None
        if raw_response:
            timeline_data = self._heal_broken_json(raw_response)
            
        if not timeline_data:
            timeline_data = self.execute_procedural_fallback(raw_script, user_prompt)

        # Rule 17 Safeguard: Cap timeline slices to prevent downstream memory overflow
        directives = timeline_data.get("master_directives", [])[:self.max_timeline_slices]
        timeline_data["master_directives"] = directives

        # Save Master Timeline Blueprint
        with open(self.output_directive_path, "w", encoding="utf-8") as f:
            json.dump(timeline_data, f, indent=4)
            
        self.log(f"Master Conductor timeline blueprint locked: '{self.output_directive_path}'", "SUCCESS")

        # --- FULL TERMINAL UI PRESENTATION (FIXED TRUNCATION) ---
        print("\n" + "=" * 75)
        print("               OMNIMATRIX V2.0 — SUPREME CONDUCTOR DIRECTIVES")
        print("=" * 75)
        print(f"SCENARIO TITLE:  {timeline_data.get('scenario_title', 'Untitled Climax')}")
        
        global_params = timeline_data.get("global_parameters", {})
        print(f"LIGHTING THEME:  {global_params.get('primary_lighting_theme', 'Standard PBR')}")
        print(f"SCENE GEOMETRY:  {global_params.get('environment_geometry', 'Standard Spatial Plane')}")
        print(f"VFX ATMOSPHERE:  {global_params.get('vfx_atmosphere', 'Nominal Fog/Particles')}")
        print("-" * 75)
        
  print("CHRONOLOGICAL CHOREOGRAPHY & AGENT ORCHESTRATION LEDGER:")
        for slice_item in directives:
            seg_id = slice_item.get("segment_id", 0)
            dur = slice_item.get("duration_slice", 0.0)
            action = slice_item.get("action_choreography", "Nominal Action")
            cam = slice_item.get("camera_rig_behavior", "static_camera")
            cmds = slice_item.get("orchestrated_agent_commands", {})
            
            print(f"\n  >> SEGMENT #{seg_id:02d} [{dur:.1f} sec] | Camera: {cam.upper()}")
            print(f"     Action: {action}")
            if cmds:
                print("     Downstream Agent Directives:")
                for agent_key, command_val in cmds.items():
                    print(f"       -> {agent_key}: [{command_val}]")
                    
        print("\n" + "=" * 75)
        print("  TIMELINE COMPILED. HANDING OFF TO MASTER TRAFFIC ORCHESTRATOR (AGENT 00)...")
        print("=" * 75 + "\n")

        self._handshake("COMPLETED", len(directives))
        return timeline_data

if __name__ == "__main__":
    conductor = Ai_Agent_65_Supreme_Creative_Script_Conductor()
    conductor.run_choreography_pipeline()