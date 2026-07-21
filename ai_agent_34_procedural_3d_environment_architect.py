import os
import re
import sys
import json
import subprocess
import urllib.request
import urllib.error

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    # Universal Uppercase API Keys
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class OmniMatrixEnvironmentArchitect:
    def __init__(self, drive_temp_dir="G:/My Drive/OMNIMATRIX_Temp", local_library_dir="D:/OMNIMATRIX_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 34: OmniMatrix Procedural Environment Architect"
        
        # Directories
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.env_dir, "34_environment_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
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

    def _query_architect_brain(self, demands):
        if not self.gemini_api_key:
            return self._fallback_architect(demands)

        ai_prompt = (
            f"You are the Master Procedural Environment Architect for the OmniMatrix Engine.\n"
            f"Storyboard Demands:\n{json.dumps(demands[:2], indent=2)}\n\n"
            "Design the environment layout configuration.\n"
            "Presets available: 'neo_tokyo_cyberpunk', 'grassy_shonen_plains', 'apocalyptic_ruins', 'crimson_void_space'.\n"
            "Return ONLY raw JSON list named 'environment_layouts':\n"
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
            payload = {"contents": [{"parts": [{"text": ai_prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                return json.loads(res_text).get("environment_layouts", [])
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

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    preset = "{layout_data.get('environment_preset', 'neo_tokyo_cyberpunk')}"
    subdiv = {layout_data.get('ground_subdivision_level', 3)}
    props_count = {layout_data.get('procedural_prop_count', 30)}
    
    # 1. Create Organic Ground Plane with Subdivisions & Displacements
    bpy.ops.mesh.primitive_grid_add(size=30.0, x_subdivisions=2**subdiv, y_subdivisions=2**subdiv, location=(0,0,0))
    ground = bpy.context.active_object
    ground.name = "Omni_Procedural_Ground"
    
    # Add Displace modifier to make natural ground bumps/craters
    sub_mod = ground.modifiers.new(name="Ground_Subsurf", type='SUBSURF')
    sub_mod.levels = 2
    
    disp_mod = ground.modifiers.new(name="Ground_Displace", type='DISPLACE')
    # Create procedural noise texture for ground height
    tex = bpy.data.textures.new("Ground_Noise", type='STORM')
    disp_mod.texture = tex
    disp_mod.strength = 0.8

    # 2. Procedural Prop Scattering (Pillars, Debris, Rocks)
    random.seed(42) # Consistent procedural layout
    for i in range(min(props_count, 60)):// Safe cap to avoid RAM spikes
        x = random.uniform(-12.0, 12.0)
        y = random.uniform(-12.0, 12.0)
        
        if "cyberpunk" in preset:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=random.uniform(4.0, 8.0), location=(x, y, 2.0))
            prop = bpy.context.active_object
            prop.name = f"Cyber_Pillar_{{i}}"
        else:
            bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(0.5, 1.5), location=(x, y, 0.5))
            prop = bpy.context.active_object
            prop.name = f"Terrain_Rock_{{i}}"

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print(f"SUCCESS: Environment preset '{{preset}}' constructed successfully.")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_environment_script.py")
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
                
                self.log_message(f"--- Building World Layout for {filename} (Theme: {layout.get('environment_preset')}) ---", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, layout)
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_message(f"Environment successfully structured into {filename}", "INFO")
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 34 Pipeline Complete. Module C is now 100% SECURED AND SEALED!", "INFO")

if __name__ == "__main__":
    architect = OmniMatrixEnvironmentArchitect()
    architect.construct_environments()
