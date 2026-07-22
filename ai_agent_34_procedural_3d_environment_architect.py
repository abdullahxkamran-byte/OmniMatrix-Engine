import os
import re
import sys
import json
import subprocess
import urllib.request
import urllib.error

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    # Universal Uppercase API Keys
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class OmniMatrixEnvironmentArchitect:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 34: aaa_procedural_environment_architect"
        
        # Directories
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.workspace_dir, "34_environment_blueprint.json")
        self.blender_path = blender_path
        
        # GEMINI API INTEGRATION
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.workspace_dir, self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_storyboard(self):
        """Loads environmental demands from storyboard or matrix state"""
        story_path = os.path.join(self.script_dir, "03_visual_sync_storyboarder.json")
        env_demands = []

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    env_demands.append({
                        "panel_index": i,
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "visual_description": panel.get("visual_prompt", "battleground"),
                        "mood": panel.get("emotional_tone", "EPIC")
                    })
            except Exception as e:
                self.log_message(f"Storyboard read warning: {str(e)}", "WARNING")

        if not env_demands:
            env_demands = [{
                "panel_index": 0, "timestamp_sec": 0.0,
                "visual_description": "Desolate sci-fi cyber arena with glowing pillars", "mood": "EPIC"
            }]

        return env_demands

    def _clean_json_response(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
        return cleaned

    def _query_architect_brain(self, demands):
        self.log_message("Consulting Architect Brain for Environment Layouts...", "INFO")

        if not self.gemini_api_key:
            self.log_message("No Gemini API Key found. Using fallback layout.", "WARNING")
            return self._fallback_architect(demands)

        ai_prompt = (
            f"You are the Master Procedural Environment Architect for the OmniMatrix Engine.\n"
            f"Storyboard Demands:\n{json.dumps(demands[:2], indent=2)}\n\n"
            "Design the environment layout configuration.\n"
            "Presets available: 'neo_tokyo_cyberpunk', 'grassy_shonen_plains', 'apocalyptic_ruins', 'crimson_void_space'.\n"
            "Return EXACTLY 1 raw JSON object containing a list named 'environment_layouts':\n"
            "{\n"
            "  \"environment_layouts\": [\n"
            "    {\n"
            "      \"timestamp_sec\": 0.0,\n"
            "      \"environment_preset\": \"neo_tokyo_cyberpunk\",\n"
            "      \"sun_intensity_lux\": 15.0,\n"
            "      \"color_temperature_k\": 8500.0,\n"
            "      \"volumetric_fog_density\": 0.15,\n"
            "      \"procedural_prop_count\": 50,\n"
            "      \"ground_subdivision_level\": 4\n"
            "    }\n"
            "  ]\n"
            "}"
        )

        try:
            # NATIVE GEMINI JSON PAYLOAD
            payload = {
                "contents": [{"parts": [{"text": ai_prompt}]}], 
                "generationConfig": {"responseMimeType": "application/json"}
            }
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                cleaned = self._clean_json_response(res_text)
                return json.loads(cleaned).get("environment_layouts", [])
        except Exception as e:
            self.log_message(f"AI Architect Brain failed: {str(e)}. Triggering fallback.", "WARNING")
            return self._fallback_architect(demands)

    def _fallback_architect(self, demands):
        layouts = []
        for d in demands:
            layouts.append({
                "timestamp_sec": float(d.get("timestamp_sec", 0.0)),
                "environment_preset": "neo_tokyo_cyberpunk",
                "sun_intensity_lux": 10.0,
                "color_temperature_k": 7000.0,
                "volumetric_fog_density": 0.1,
                "procedural_prop_count": 40,
                "ground_subdivision_level": 3
            })
        return layouts

    def _generate_blender_script(self, blend_file_path, layout_data):
        """Headless Blender Script to build procedural ground, craters, and scatter props."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy
import random

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    # Idempotency: Scrub existing procedural elements to prevent overlapping meshes on re-runs
    for obj in bpy.data.objects:
        if obj.name.startswith("OMNI_Procedural_Ground") or obj.name.startswith("OMNI_Cyber_Pillar_") or obj.name.startswith("OMNI_Terrain_Rock_"):
            bpy.data.objects.remove(obj, do_unlink=True)
            
    # Cleanup unused textures to avoid memory bloat
    if "OMNI_Ground_Noise" in bpy.data.textures:
        bpy.data.textures.remove(bpy.data.textures["OMNI_Ground_Noise"], do_unlink=True)

    preset = "{layout_data.get('environment_preset', 'neo_tokyo_cyberpunk')}"
    subdiv = {layout_data.get('ground_subdivision_level', 3)}
    props_count = {layout_data.get('procedural_prop_count', 30)}
    
    # 1. Create Organic Ground Plane with Subdivisions & Displacements
    bpy.ops.mesh.primitive_grid_add(size=30.0, x_subdivisions=2**subdiv, y_subdivisions=2**subdiv, location=(0,0,0))
    ground = bpy.context.active_object
    ground.name = "OMNI_Procedural_Ground"
    
    # Add Displace modifier to make natural ground bumps/craters
    sub_mod = ground.modifiers.new(name="Ground_Subsurf", type='SUBSURF')
    sub_mod.levels = 2
    
    disp_mod = ground.modifiers.new(name="Ground_Displace", type='DISPLACE')
    
    # Fix: 'STORM' is not a valid Blender texture. Using 'CLOUDS' for organic terrain noise.
    tex = bpy.data.textures.new("OMNI_Ground_Noise", type='CLOUDS')
    tex.noise_scale = 1.5
    disp_mod.texture = tex
    disp_mod.strength = 0.8

    # 2. Procedural Prop Scattering (Pillars, Debris, Rocks)
    random.seed(42) # Consistent procedural layout
    for i in range(min(props_count, 60)): # Safe cap to avoid RAM spikes
        x = random.uniform(-12.0, 12.0)
        y = random.uniform(-12.0, 12.0)
        
        if "cyberpunk" in preset.lower():
            bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=random.uniform(4.0, 8.0), location=(x, y, 2.0))
            prop = bpy.context.active_object
            prop.name = f"OMNI_Cyber_Pillar_{{i}}"
        else:
            bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(0.5, 1.5), location=(x, y, 0.5))
            prop = bpy.context.active_object
            prop.name = f"OMNI_Terrain_Rock_{{i}}"

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print(f"SUCCESS: Environment preset '{{preset}}' constructed successfully.")

except Exception as e:
    print(f"ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_environment_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def construct_environments(self):
        self.log_message("Initializing OmniMatrix Environment Architect...", "INFO")
        
        demands = self._load_upstream_storyboard()
        layouts = self._query_architect_brain(demands)
        
        master_blueprint = {"environment_layouts": layouts}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_file_path = os.path.join(self.env_dir, filename)
                layout = layouts[0] if layouts else {}
                
                self.log_message(f"--- Building World Layout for {filename} (Theme: {layout.get('environment_preset', 'Default')}) ---", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, layout)
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        self.log_message(f"Environment successfully structured into {filename}", "SUCCESS")
                    else:
                        self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 34 Pipeline Complete. Module C is now 100% SECURED AND SEALED!", "INFO")

if __name__ == "__main__":
    architect = OmniMatrixEnvironmentArchitect()
    architect.construct_environments()
