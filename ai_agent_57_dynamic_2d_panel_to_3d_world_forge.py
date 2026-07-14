import os
import sys
import json
import urllib.request
import urllib.error

class Dynamic2dPanelTo3DWorldForge:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 57: dynamic_2d_panel_to_3d_world_forge"
        self.workspace_dir = workspace_dir
        
        # Upstream Inputs
        self.input_mesh_path = os.path.join(self.workspace_dir, "56_3d_mesh.obj")
        self.input_blueprint_path = os.path.join(self.workspace_dir, "55_manga_comprehend_blueprint.json")
        
        # Outputs
        self.output_world_blueprint = os.path.join(self.workspace_dir, "57_3d_world_forge_blueprint.json")
        self.output_blender_script = os.path.join(self.workspace_dir, "57_blender_setup.py")
        
        # [SECURE] No hardcoded secret keys to prevent repo block
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_data(self):
        manga_context = {}
        if os.path.exists(self.input_blueprint_path):
            try:
                with open(self.input_blueprint_path, "r", encoding="utf-8") as f:
                    manga_context = json.load(f)
                print(f"[{self.agent_name}] Successfully imported upstream manga context from Agent 55.")
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Failed to read Agent 55 blueprint: {str(e)}")
        else:
            print(f"[{self.agent_name}] Notice: No upstream manga context blueprint found. Using defaults.")
        return manga_context

    def forge_3d_world(self):
        print(f"[{self.agent_name}] Initializing 3D World Forge and Scene Layout Engine...")
        manga_context = self._load_upstream_data()

        # Extract character/color details for lighting decisions
        analysis_metrics = manga_context.get("analysis_metrics", {})
        palette = analysis_metrics.get("colorization_palette", {})
        aura_color_hex = palette.get("aura", "#FF00FF") # Default Magenta

        ai_prompt_instructions = (
            "You are a 3D Environment Director for Anime and Cinematic CGI.\n"
            f"Analyze this 2D-to-3D scene context. Main active aura color is '{aura_color_hex}'.\n"
            "Design a cinematic 3D lighting, camera, and world setup in JSON format.\n"
            "Return ONLY a valid JSON object with absolutely no markdown wrapping, code blocks, or backticks. Format:\n"
            "{\n"
            "  \"camera\": {\n"
            "    \"location\": [0.0, -5.0, 1.5],\n"
            "    \"rotation_euler\": [80.0, 0.0, 0.0],\n"
            "    \"focal_length\": 50.0\n"
            "  },\n"
            "  \"lights\": [\n"
            "    {\"type\": \"SUN\", \"energy\": 4.0, \"color_hex\": \"#FFFFFF\", \"direction\": [0.2, -0.5, -1.0]},\n"
            "    {\"type\": \"POINT\", \"energy\": 15.0, \"color_hex\": \"#FF00FF\", \"location\": [1.5, -1.0, 2.0]}\n"
            "  ],\n"
            "  \"world_ambient\": {\n"
            "    \"background_color_hex\": \"#0A0A0F\",\n"
            "    \"ambient_strength\": 0.2\n"
            "  }\n"
            "}"
        )

        world_config = None

        if self.gemini_api_key:
            print(f"[{self.agent_name}] Consulting Gemini AI for optimized dramatic lighting angles...")
            try:
                payload = {
                    "contents": [{
                        "parts": [{"text": ai_prompt_instructions}]
                    }],
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

                with urllib.request.urlopen(req, timeout=15) as response:
                    res_body = response.read().decode("utf-8")
                    raw_response = json.loads(res_body)
                    raw_text = raw_response["candidates"][0]["content"]["parts"][0]["text"]
                    world_config = json.loads(raw_text.strip())
                    print(f"[{self.agent_name}] Success: Custom cinematic camera and lighting parameters generated.")
            except Exception as e:
                print(f"[{self.agent_name}] Cloud dynamic layout bypass ({str(e)}). Building procedural rig...")
                world_config = self._get_procedural_world_config(aura_color_hex)
        else:
            print(f"[{self.agent_name}] No API Key. Generating default high-fidelity 3D anime layout...")
            world_config = self._get_procedural_world_config(aura_color_hex)

        # Save World Forge Blueprint JSON
        self._save_world_blueprint(world_config)

        # Write out the magic Blender setup script
        self._generate_blender_python_script(world_config)

        return {
            "agent_executed": self.agent_name,
            "status": "Complete",
            "world_blueprint": self.output_world_blueprint,
            "blender_setup_script": self.output_blender_script
        }

    def _get_procedural_world_config(self, aura_color):
        return {
            "camera": {
                "location": [0.0, -6.5, 1.2],
                "rotation_euler": [85.0, 0.0, 0.0],
                "focal_length": 35.0 # Cinematic wide lens
            },
            "lights": [
                {
                    "type": "SUN",
                    "energy": 5.0,
                    "color_hex": "#FFEFE0", # Warm sunlight
                    "direction": [0.5, -0.3, -1.0]
                },
                {
                    "type": "POINT",
                    "energy": 25.0,
                    "color_hex": aura_color, # Active character aura color
                    "location": [-1.0, -1.5, 1.8]
                },
                {
                    "type": "POINT",
                    "energy": 12.0,
                    "color_hex": "#00FFFF", # Neon Rim Fill Light
                    "location": [1.5, -0.5, 0.8]
                }
            ],
            "world_ambient": {
                "background_color_hex": "#07070B",
                "ambient_strength": 0.15
            }
        }

    def _generate_blender_python_script(self, config):
        camera_cfg = config.get("camera", {})
        lights_cfg = config.get("lights", [])
        ambient_cfg = config.get("world_ambient", {})
        
        # Convert hex colors to RGB values (0.0 to 1.0) for Blender
        def hex_to_rgb(hex_str):
            hex_str = hex_str.lstrip('#')
            return [int(hex_str[i:i+2], 16)/255.0 for i in (0, 2, 4)]

        # Relative mesh path safe for blender execution
        relative_mesh_path = os.path.abspath(self.input_mesh_path).replace("\\", "\\\\")

        script_content = f"""# ==========================================
# Blender Automation Script (Z-NET Agent 57)
# Run this inside Blender Scripting Workspace!
# ==========================================
import bpy
import os

# 1. Clear existing objects to start fresh
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 2. Import generated 3D Mesh
mesh_path = "{relative_mesh_path}"
if os.path.exists(mesh_path):
    # Support for both older and newer Blender OBJ importers
    try:
        bpy.ops.wm.obj_import(filepath=mesh_path)
    except AttributeError:
        bpy.ops.import_scene.obj(filepath=mesh_path)
    print("3D Mesh successfully imported!")
else:
    print("Warning: Mesh file not found at path: " + mesh_path)

# 3. Setup Cinematic Camera
cam_data = bpy.data.cameras.new(name="Cinematic_Camera_Data")
cam_obj = bpy.data.objects.new("Cinematic_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = {camera_cfg.get('location', [0.0, -6.5, 1.2])}
# Degrees to Radians translation
import math
rot = {camera_cfg.get('rotation_euler', [85.0, 0.0, 0.0])}
cam_obj.rotation_euler = [math.radians(r) for r in rot]
cam_data.lens = {camera_cfg.get('focal_length', 35.0)}

# Set active camera
bpy.context.scene.camera = cam_obj

# 4. Spawning Lights Rig
"""
        for i, light in enumerate(lights_cfg):
            l_type = light.get("type", "POINT").upper()
            l_energy = light.get("energy", 10.0)
            rgb = hex_to_rgb(light.get("color_hex", "#FFFFFF"))
            
            if l_type == "SUN":
                script_content += f"""
# Spawn Sun Light
sun_data = bpy.data.lights.new(name="Sun_Light_{i}", type='SUN')
sun_data.energy = {l_energy}
sun_data.color = {rgb}
sun_obj = bpy.data.objects.new("Sun_Light_{i}", sun_data)
bpy.context.collection.objects.link(sun_obj)
# Align Sun direction
direction = {light.get('direction', [0.0, 0.0, -1.0])}
import mathutils
sun_obj.rotation_euler = mathutils.Vector(direction).to_track_quat('-Z', 'Y').to_euler()
"""
            else:
                loc = light.get("location", [0.0, 0.0, 2.0])
                script_content += f"""
# Spawn Point Light
point_data = bpy.data.lights.new(name="Point_Light_{i}", type='POINT')
point_data.energy = {l_energy}
point_data.color = {rgb}
point_obj = bpy.data.objects.new("Point_Light_{i}", point_data)
bpy.context.collection.objects.link(point_obj)
point_obj.location = {loc}
"""

        # World Background Setup
        bg_rgb = hex_to_rgb(ambient_cfg.get("background_color_hex", "#050505"))
        script_content += f"""
# 5. Set Environment background color
world = bpy.context.scene.world
if world:
    world.use_nodes = False
    world.color = {bg_rgb}

print("Z-NET 3D World built successfully! Check Layout Viewport.")
"""

        with open(self.output_blender_script, "w", encoding="utf-8") as f:
            f.write(script_content)
        print(f"[{self.agent_name}] Success: Blender Setup automation script generated at '{self.output_blender_script}'")

    def _save_world_blueprint(self, data):
        with open(self.output_world_blueprint, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[{self.agent_name}] 3D layout coordinates saved to '{self.output_world_blueprint}'")

if __name__ == "__main__":
    forger = Dynamic2dPanelTo3DWorldForge()
    forger.forge_3d_world()
