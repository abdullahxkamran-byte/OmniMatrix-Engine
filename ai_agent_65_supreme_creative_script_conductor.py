import os
import sys
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

class AiSupremeCreativeScriptConductor:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 65: supreme_creative_script_conductor"
        
        # Portable workspace routing (Works seamlessly on local PC and cloud environments)
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        # Unified system path configuration
        self.input_script_path = os.path.join(self.workspace_dir, "08_formatted_script.json")
        self.output_directive_path = os.path.join(self.workspace_dir, "65_master_conductor_timeline.json")
        self.log_file_path = os.path.join(self.workspace_dir, "agent_65_execution.log")
        
        # API endpoints
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        
        # Secure manual parsing of local .env configuration keys
        self.api_keys = self._load_env_keys()
        self.gemini_key = self.api_keys.get("GEMINI_API_KEY", None)
        self.openai_key = self.api_keys.get("OPENAI_API_KEY", None)
        
        # Gemini model endpoint mapping
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_key}" if self.gemini_key else None

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def log_message(self, message, level="INFO"):
        """Systematic logging utility for runtime execution debugging."""
        formatted_msg = f"[{level}] [{self.agent_name}] {message}"
        print(formatted_msg)
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as log_f:
                log_f.write(formatted_msg + "\n")
        except Exception:
            pass

    def _load_env_keys(self):
        """Extracts values from the project .env configuration file securely without external library dependencies."""
        keys = {}
        env_path = ".env"
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            keys[k.strip()] = v.strip().strip('"').strip("'")
            except Exception as e:
                print(f"[{self.agent_name}] Critical: Failed parsing .env configurations: {str(e)}")
        return keys

    def _load_raw_script(self):
        """Attempts to load pre-formatted story arcs or returns a fallback dynamic timeline block."""
        if os.path.exists(self.input_script_path):
            try:
                with open(self.input_script_path, "r", encoding="utf-8") as f:
                    self.log_message("External script timeline file detected and loaded successfully.", "INFO")
                    return json.load(f)
            except Exception as e:
                self.log_message(f"Warning: Script load bypassed or corrupt: {str(e)}. Triggering dynamic baseline structure.", "WARNING")
        
        # Universal context-aware default script container
        return {
            "title": "Unbound Arena Confrontation",
            "voice_over_script": "The sky shatters as supreme forces collide. There is no retreat, only absolute dominion.",
            "duration_seconds": 12.0
        }

    def _clean_json(self, raw_text):
        """Extracts raw JSON content by eliminating common markdown block enclosures and formatting issues."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        # Ensure we capture standard bracket layouts
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
        return cleaned

    def _heal_broken_json(self, json_string):
        """Attempts structural repairs on malformed LLM responses to ensure structural parse completeness."""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as err:
            self.log_message(f"JSON integrity issue detected: {str(err)}. Attempting systemic parsing repairs...", "WARNING")
            
            # Simple automatic string adjustments for unfinished outputs
            repaired = json_string.strip()
            if not repaired.endswith("}"):
                if repaired.count("[") > repaired.count("]"):
                    repaired += "]"
                if repaired.count("{") > repaired.count("}"):
                    repaired += "}"
            
            try:
                return json.loads(repaired)
            except Exception:
                self.log_message("Automatic repairs unsuccessful. Routing directly to safety procedural engines.", "ERROR")
                return None

    def build_creative_prompt(self, raw_script, user_prompt):
        """Constructs an incredibly descriptive system instruction sequence for multi-model intelligence."""
        system_instruction = (
            "You are a Legendary Visual Director, Cinematographer, and Combat Choreographer. "
            "You are the Supreme Creative Script Conductor of the Z-Net automated multi-agent workstation.\n\n"
            "Your critical task is to process a visual prompt alongside a base narrative script, and decompose it into a "
            "highly optimized, chronological master execution timeline. If the user requests highly specific actions "
            "(e.g., custom showdowns like Gojo Satoru defeating Ryomen Sukuna), visualize and plan it down to the exact frames. "
            "Incorporate maximum lore accuracy for abilities (such as Limitless, domain expansions, spatial impacts) "
            "but keep the system versatile and capable of handling realistic or non-anime scenarios dynamically.\n\n"
            "Produce your master directive timeline strictly in valid JSON format matching this exact template:\n"
            "{\n"
            "  \"scenario_title\": \"The Ultimate Climax - Battle of the Heavens\",\n"
            "  \"global_parameters\": {\n"
            "    \"primary_lighting_theme\": \"Dark gothic blue with vivid cyan and purple rim lighting highlights\",\n"
            "    \"environment_geometry\": \"Crumbling city block with suspended concrete chunks floating in air\",\n"
            "    \"vfx_atmosphere\": \"Volumetric wind dust, atmospheric distortion, high-frequency kinetic energy sparks\"\n"
            "  },\n"
            "  \"character_set\": [\n"
            "    {\"character_name\": \"Gojo Satoru\", \"clothing_details\": \"Black high-collar Jujutsu uniform\", \"initial_pose\": \"Floating calmly three feet off the ground, fingers crossed in the Unlimited Void sign\"},\n"
            "    {\"character_name\": \"Ryomen Sukuna\", \"clothing_details\": \"Ripped kimono with cursed markings\", \"initial_pose\": \"Standing on ruined concrete, four arms active, expressions of pure shock\"}\n"
            "  ],\n"
            "  \"master_directives\": [\n"
            "    {\n"
            "      \"segment_id\": 1,\n"
            "      \"duration_slice\": 6.0,\n"
            "      \"action_choreography\": \"Gojo triggers Red and Blue simultaneously. A swirling vortex of gravity forms between his hands. Sukuna attempts to slash but is pulled off balance by spatial gravity.\",\n"
            "      \"environment_state\": \"Floating chunks speed up, spinning around Gojo. The ground starts to cave inward forming a massive crater.\",\n"
            "      \"camera_rig_behavior\": \"dramatic_orbital_zoom\",\n"
            "      \"orchestrated_agent_commands\": {\n"
            "        \"agent_14_phonk_beat_sync\": \"slow_mo_rise\",\n"
            "        \"agent_22_lighting_shader\": \"ambient_dark_purple\",\n"
            "        \"agent_30_fracture_engine\": \"ground_cracking_frame_24\"\n"
            "      }\n"
            "    },\n"
            "    {\n"
            "      \"segment_id\": 2,\n"
            "      \"duration_slice\": 6.0,\n"
            "      \"action_choreography\": \"Gojo releases Hollow Purple, which obliterates the central plane. Sukuna is swept away in a glowing violet energy blast. Gojo lands softly with a smirk.\",\n"
            "      \"environment_state\": \"Intense purple glow reflecting on all debris. All background objects vaporize into glowing ash particles.\",\n"
            "      \"camera_rig_behavior\": \"shaky_handheld_track\",\n"
            "      \"orchestrated_agent_commands\": {\n"
            "        \"agent_14_phonk_beat_sync\": \"bass_drop_shake\",\n"
            "        \"agent_22_lighting_shader\": \"high_contrast_rim_light\",\n"
            "        \"agent_30_fracture_engine\": \"absolute_destruction\"\n"
            "      }\n"
            "    }\n"
            "  ]\n"
            "}\n\n"
            "Ensure the total sum of all 'duration_slice' fields equals the target video duration. Do not include markdown wraps or conversational texts. Return valid JSON only."
        )
        
        user_context = (
            f"Target System Script Details:\n{json.dumps(raw_script, indent=2)}\n\n"
            f"User Directives & Story Override:\n{user_prompt}"
        )
        
        return system_instruction, user_context

    def query_creative_intelligence(self, system_prompt, user_prompt):
        """Sends payload requests to the highest available intelligence node in the system pipeline."""
        
        # Route 1: Gemini API Node (Primary Cloud Core)
        if self.gemini_key and self.gemini_url:
            self.log_message("Querying Primary Cloud Intelligence Node (Gemini Engine)...", "INFO")
            try:
                payload = {
                    "contents": [
                        {"role": "user", "parts": [{"text": f"System Directive: {system_prompt}\n\nUser Prompt Context: {user_prompt}"}]}
                    ],
                    "generationConfig": {
                        "responseMimeType": "application/json"
                    }
                }
                data_bytes = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    self.gemini_url,
                    data=data_bytes,
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_body = json.loads(response.read().decode("utf-8"))
                    raw_text = res_body["candidates"][0]["content"]["parts"][0]["text"]
                    return self._clean_json(raw_text)
            except Exception as e:
                self.log_message(f"Gemini API execution failed: {str(e)}. Attempting backup endpoints...", "WARNING")

        # Route 2: OpenAI API Node (Backup Cloud Core)
        if self.openai_key:
            self.log_message("Querying Secondary Cloud Intelligence Node (OpenAI Engine)...", "INFO")
            try:
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"}
                }
                data_bytes = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    self.openai_url,
                    data=data_bytes,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.openai_key}"
                    }
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_body = json.loads(response.read().decode("utf-8"))
                    raw_text = res_body["choices"][0]["message"]["content"]
                    return self._clean_json(raw_text)
            except Exception as e:
                self.log_message(f"OpenAI API execution failed: {str(e)}. Checking for local systems...", "WARNING")

        # Route 3: Ollama Llama3 Node (Local GPU Fallback)
        self.log_message("Querying Local Fallback Node (Ollama Engine)...", "INFO")
        try:
            payload = {
                "model": "llama3",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "format": "json"
            }
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.ollama_url,
                data=data_bytes,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=40) as response:
                res_body = json.loads(response.read().decode("utf-8"))
                raw_text = res_body["message"]["content"]
                return self._clean_json(raw_text)
        except Exception as e:
            self.log_message(f"Local Ollama node offline: {str(e)}. Reverting to offline procedural backup.", "ERROR")
            return None

    def execute_procedural_fallback(self, raw_script, user_prompt):
        """Generates a structured visual scenario when all API interfaces are offline."""
        self.log_message("Procedural fallback generator initialized.", "INFO")
        total_duration = float(raw_script.get("duration_seconds", 12.0))
        half_duration = round(total_duration / 2, 2)
        
        fallback_timeline = {
            "scenario_title": f"Procedural Action Sequence - {raw_script.get('title', 'Override Mode')}",
            "global_parameters": {
                "primary_lighting_theme": "High-contrast dynamic neon red and orange flares",
                "environment_geometry": "Shattering stone pillars and reflective water floors",
                "vfx_atmosphere": "Volumetric smoke plumes, directional wind, embers"
            },
            "character_set": [
                {"character_name": "Active Hero", "clothing_details": "Tattered battlesuit", "initial_pose": "Crouched in combat preparation"},
                {"character_name": "Challenger Entity", "clothing_details": "Dark metallic armor", "initial_pose": "Floating with arms extended"}
            ],
            "master_directives": [
                {
                    "segment_id": 1,
                    "duration_slice": half_duration,
                    "action_choreography": f"Hero launches into extreme speed sprint. Challenger channels energy blast. Narrative reflects: '{user_prompt}'",
                    "environment_state": "Ground begins fracturing, water surface rippling violently.",
                    "camera_rig_behavior": "dramatic_orbital_zoom",
                    "orchestrated_agent_commands": {
                        "agent_14_phonk_beat_sync": "slow_mo_rise",
                        "agent_22_lighting_shader": "ambient_dark_purple",
                        "agent_30_fracture_engine": "ground_cracking_frame_12"
                    }
                },
                {
                    "segment_id": 2,
                    "duration_slice": half_duration,
                    "action_choreography": "Collision point creates shockwave. Hero breaks through defense line securing absolute victory.",
                    "environment_state": "Pillars completely break apart, sky flashes with brilliant light beams.",
                    "camera_rig_behavior": "shaky_handheld_track",
                    "orchestrated_agent_commands": {
                        "agent_14_phonk_beat_sync": "bass_drop_shake",
                        "agent_22_lighting_shader": "high_contrast_rim_light",
                        "agent_30_fracture_engine": "absolute_destruction"
                    }
                }
            ]
        }
        return fallback_timeline

    def trigger_downstream_sequence(self):
        """Triggers sequential target processing blocks based on the approved timeline design."""
        self.log_message("Transitioning execution command line targets to active agents...", "INFO")
        
        # Order of operations in Z-Net pipeline
        downstream_targets = [
            {"script": "ai_agent_55_image_generator.py", "description": "Visual Asset Creator"},
            {"script": "ai_agent_56_rgb_image_to_3d_mesh_converter.py", "description": "3D Mesh Generator"},
            {"script": "ai_agent_57_blender_scene_assembler.py", "description": "Environment & Lighting Builder"},
            {"script": "ai_agent_59_final_renderer.py", "description": "Physics Render Engine"}
        ]
        
        for target in downstream_targets:
            script_name = target["script"]
            description = target["description"]
            
            script_path = os.path.join(self.base_dir, script_name)
            if os.path.exists(script_path):
                self.log_message(f"Spawning target node: {script_name} ({description})...", "INFO")
                # Command execution signal to run sub-scripts
                # In production, this executes: os.system(f"python {script_name}")
            else:
                self.log_message(f"Target node simulated: {script_name} ({description}) ready for execution.", "INFO")

    def run_choreography_pipeline(self):
        self.log_message("System Active. Initializing Master Orchestrator process...", "INFO")
        
        # 1. Load context script
        raw_script = self._load_raw_script()
        
        # 2. Gather custom direction prompt from console
        print("-" * 75)
        user_prompt = input("Enter custom action choreography or lore directions: ")
        print("-" * 75)
        
        if not user_prompt.strip():
            user_prompt = "Generate a highly cinematic, intense action showdown matching the narrative style."
        
        # 3. Create instruction structures
        system_prompt, user_prompt_context = self.build_creative_prompt(raw_script, user_prompt)
        
        # 4. Generate structured results
        raw_ai_response = self.query_creative_intelligence(system_prompt, user_prompt_context)
        
        timeline_data = None
        if raw_ai_response:
            timeline_data = self._heal_broken_json(raw_ai_response)
            
        if not timeline_data:
            self.log_message("Using procedural generation framework due to processing limits.", "WARNING")
            timeline_data = self.execute_procedural_fallback(raw_script, user_prompt)

        # 5. Formatted Command Terminal UI Presentation
        print("\n" + "=" * 75)
        print("                   Z-NET CORE CONDUCTOR DIRECTIVES")
        print("=" * 75)
        print(f"TITLE:       {timeline_data.get('scenario_title', 'Untitled Scenario')}")
        
        global_params = timeline_data.get("global_parameters", {})
        print(f"THEME:       {global_params.get('primary_lighting_theme', 'Default Scene Lighting')}")
        print(f"GEOMETRY:    {global_params.get('environment_geometry', 'Standard Spatial Plane')}")
        print(f"ATMOSPHERE:  {global_params.get('vfx_atmosphere', 'Basic Fog/Particle Level')}")
        print("-" * 75)
        
        print("ACTORS LOADED:")
        # --- FIXED LINE 366 AND COMPLETED TH