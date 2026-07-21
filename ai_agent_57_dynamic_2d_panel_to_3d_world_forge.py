import os
import sys
import json
import re
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
                    os.environ[key.strip()] = val.strip()

load_env_file()

class DynamicBatchWorldForge:
    # 1. Aligned with AAA Storage Architecture (Drive for Temp, Local for Assets)
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 57: Dynamic Batch 3D World Forge"
        
        # Upstream Inputs (From Drive)
        self.vision_outputs_dir = os.path.join(drive_temp_dir, "outputs")
        self.meshes_dir = os.path.join(drive_temp_dir, "3d_meshes")
        self.input_mesh_blueprint = os.path.join(self.meshes_dir, "56_master_mesh_blueprint.json")
        
        # Outputs (Going straight to Fast Local Drive)
        self.output_dir = os.path.join(local_library_dir, "3d_environments")
        self.output_world_blueprint = os.path.join(self.output_dir, "57_master_world_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [drive_temp_dir, self.output_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_mesh_blueprint(self):
        if not os.path.exists(self.input_mesh_blueprint):
            self.log_message("Agent 56 Blueprint not found in Drive. Waiting for upstream.", "ERROR")
            return {}
        try:
            with open(self.input_mesh_blueprint, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.log_message(f"Failed to read Mesh blueprint: {str(e)}", "ERROR")
            return {}

    def _get_procedural_fallback_config(self, scene_name):
        return {
            "camera": {
                "location": [0.0, -6.5, 1.2],
                "rotation_euler": [85.0, 0.0, 0.0],
                "focal_length": 35.0
            },
            "lights": [
                {"type": "SUN", "energy": 5.0, "color_hex": "#FFEFE0", "direction": [0.5, -0.3, -1.0]},
                {"type": "POINT", "energy": 25.0, "color_hex": "#FF00FF", "location": [-1.0, -1.5, 1.8]},
                {"type": "POINT", "energy": 12.0, "color_hex": "#00FFFF", "location": [1.5, -0.5, 0.8]}
            ],
            "world_ambient": {
                "background_color_hex": "#07070B",
                "ambient_strength": 0.15
            }
        }

    def _query_gemini_lighting(self, vision_data, scene_name):
        if not self.gemini_api_key:
            return self._get_procedural_fallback_config(scene_name)

        bg_desc = vision_data.get("background_description", "Dark empty space")
        char_name = vision_data.get("character_name", "None (Environment Only)")
        time_of_day = vision_data.get("time_of_day", "Unknown")

        ai_prompt = (
            f"You are a Senior AAA Cinematic Lighting Director. Design a lighting and camera setup for scene '{scene_name}'.\n"
            f"Character Focus: {char_name}\n"
            f"Background Context: {bg_desc}\n"
            f"Time of Day/Vibe: {time_of_day}\n\n"
            "Return ONLY raw JSON, no markdown blocks. Format exactly like this:\n"
            "{\n"
            "  \"camera\": {\"location\": [0.0, -5.0, 1.5], \"rotation_euler\": [80.0, 0.0, 0.0], \"focal_length\": 50.0},\n"
            "  \"lights\": [\n"
            "    {\"type\": \"SUN\", \"energy\": 4.0, \"color_hex\": \"#FFFFFF\", \"direction\": [0.2, -0.5, -1.0]},\n"
            "    {\"type\": \"POINT\", \"energy\": 15.0, \"color_hex\": \"#FF5500\", \"location\": [1.5, -1.0, 2.0]}\n"
            "  ],\n"
            "  \"world_ambient\": {\"background_color_hex\": \"#0A0A0F\", \"ambient_strength\": 0.2}\n"
            "}"
        )

        try:
            payload = {"contents": [{"parts": [{"text": ai_prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                return json.loads(res_text)
        except Exception as e:
            self.log_message(f"Gemini lighting failed for {scene_name} ({str(e)}). Using fallback.", "WARNING")
            return self._get_procedural_fallback_config(scene_name)

    def _generate_blender_python_script(self, scene_name, scene_data, out_blend_path):
        """Generates the script that builds the specific scene in Blender and saves the .blend file."""
        safe_mesh_path = scene_data["mesh"].replace("\\", "/") if scene_data["mesh"] else ""
        safe_bg_path = scene_data["bg_image"].replace("\\", "/")
        safe_depth_path = scene_data["depth_image"].replace("\\", "/")
        safe_blend_path = out_blend_path.replace("\\", "/")
        
        cam = scene_data["layout"]["camera"]
        lights = scene_data["layout"]["lights"]
        ambient = scene_data["layout"]["world_ambient"]
        bg_color = ambient.get("background_color_hex", "#050505")
        
        lights_json = json.dumps(lights)

        script_content = f"""
import bpy
import os
import math
import mathutils
import json

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return [int(hex_str[i:i+2], 16)/255.0 for i in (0, 2, 4)] + [1.0]

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_2point5d_background(bg_path, depth_path, location=(0, 5, 1)):
    if not os.path.exists(bg_path):
        return
        
    bpy.ops.mesh.primitive_plane_add(size=10, location=location)
    plane = bpy.context.active_object
    plane.name = "Parallax_Background"
    plane.rotation_euler = (math.radians(90), 0, 0)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=50)
    bpy.ops.object.mode_set(mode='OBJECT')

    mat = bpy.data.materials.new(name="BG_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
    
    try:
        tex_image.image = bpy.data.images.load(bg_path)
        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
    except:
        pass
    plane.data.materials.append(mat)

    if os.path.exists(depth_path):
        disp_mod = plane.modifiers.new(name="DepthDisplacement", type='DISPLACE')
        disp_tex = bpy.data.textures.new("DepthTexture", type='IMAGE')
        try:
            disp_tex.image = bpy.data.images.load(depth_path)
            disp_mod.texture = disp_tex
            disp_mod.strength = 1.5
            disp_mod.mid_level = 0.5
        except:
            pass

try:
    clear_scene()

    # 1. Import Character Mesh (If it exists and is not an Environment-Only bypass)
    mesh_path = "{safe_mesh_path}"
    if mesh_path and os.path.exists(mesh_path):
        try:
            bpy.ops.wm.obj_import(filepath=mesh_path)
        except AttributeError:
            bpy.ops.import_scene.obj(filepath=mesh_path)

    # 2. Setup 2.5D Parallax Background
    create_2point5d_background("{safe_bg_path}", "{safe_depth_path}")

    # 3. Camera Setup
    cam_data = bpy.data.cameras.new(name="Cinematic_Camera")
    cam_obj = bpy.data.objects.new("Cinematic_CamObj", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    cam_obj.location = {cam.get('location', [0.0, -6.5, 1.2])}
    cam_obj.rotation_euler = [math.radians(r) for r in {cam.get('rotation_euler', [85.0, 0.0, 0.0])}]
    cam_data.lens = {cam.get('focal_length', 35.0)}
    bpy.context.scene.camera = cam_obj

    # 4. Cinematic Lighting Setup
    lights = json.loads('''{lights_json}''')
    for i, light in enumerate(lights):
        l_type = light.get("type", "POINT").upper()
        l_energy = light.get("energy", 10.0)
        color_hex = light.get("color_hex", "#FFFFFF")
        
        if l_type == "SUN":
            direction = light.get('direction', [0.0, 0.0, -1.0])
            sun_data = bpy.data.lights.new(name=f"Sun_Light_{{i}}", type='SUN')
            sun_data.energy = l_energy
            sun_data.color = hex_to_rgb(color_hex)[:3]
            sun_obj = bpy.data.objects.new(f"Sun_Obj_{{i}}", sun_data)
            bpy.context.scene.collection.objects.link(sun_obj)
            sun_obj.rotation_euler = mathutils.Vector(direction).to_track_quat('-Z', 'Y').to_euler()
        else:
            loc = light.get("location", [0.0, 0.0, 2.0])
            point_data = bpy.data.lights.new(name=f"Point_Light_{{i}}", type='POINT')
            point_data.energy = l_energy
            point_data.color = hex_to_rgb(color_hex)[:3]
            point_obj = bpy.data.objects.new(f"Point_Obj_{{i}}", point_data)
            bpy.context.scene.collection.objects.link(point_obj)
            point_obj.location = loc

    # 5. World Ambient
    world = bpy.context.scene.world
    if world:
        world.use_nodes = False
        world.color = hex_to_rgb("{bg_color}")[:3]

    # 6. Export ready-to-use Blender Scene to Local Library!
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_world_forge_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def forge_batch_world(self):
        self.log_message("Initializing Batch 3D World Forge...", "INFO")
        
        mesh_blueprint = self._load_mesh_blueprint()
        if not mesh_blueprint:
            return
            
        master_world_config = {}

        for scene_name, mesh_data in mesh_blueprint.items():
            self.log_message(f"--- Forging 3D Stage for: {scene_name} ---", "INFO")
            
            vision_json_path = os.path.join(self.vision_outputs_dir, f"{scene_name}_vision.json")
            bg_path = os.path.join(self.vision_outputs_dir, f"{scene_name}_04_bg.png")
            depth_path = os.path.join(self.vision_outputs_dir, f"{scene_name}_05_bg_depth.png")
            
            vision_data = {}
            if os.path.exists(vision_json_path):
                try:
                    with open(vision_json_path, "r", encoding="utf-8") as vf:
                        vision_data = json.load(vf)
                except Exception as e:
                    self.log_message(f"Error reading vision data: {e}", "WARNING")

            # Bypass mesh if pipeline is Environment Only
            mesh_path = mesh_data.get("mesh", "")
            if vision_data.get("pipeline_mode") == "Environment":
                self.log_message(f"Environment-Only mode detected. Bypassing character mesh.", "INFO")
                mesh_path = ""

            layout_config = self._query_gemini_lighting(vision_data, scene_name)
            
            out_blend_path = os.path.join(self.output_dir, f"{scene_name}_stage.blend")

            # Generate the execution script
            script_path = self._generate_blender_python_script(scene_name, {
                "mesh": mesh_path,
                "bg_image": bg_path if os.path.exists(bg_path) else "",
                "depth_image": depth_path if os.path.exists(depth_path) else "",
                "layout": layout_config
            }, out_blend_path)
            
            # Execute Headless Blender to build the stage
            self.log_message(f"Executing Headless Blender for {scene_name}...", "INFO")
            command = [self.blender_path, "-b", "-P", script_path]
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0 and os.path.exists(out_blend_path):
                    self.log_message(f"Stage saved to LOCAL DRIVE: {scene_name}_stage.blend", "INFO")
                    
                    master_world_config[scene_name] = {
                        "environment_blend": out_blend_path,
                        "layout_config": layout_config
                    }
                else:
                    self.log_message(f"Blender failed. Log: {result.stdout[-300:]}", "ERROR")
            except Exception as e:
                self.log_message(f"Subprocess failed: {str(e)}", "CRITICAL")
                
            if os.path.exists(script_path):
                os.remove(script_path)

        with open(self.output_world_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_world_config, f, indent=4)
        
        self.log_message("Agent 57 Pipeline Complete. Module H is formally SEALED!", "INFO")

if __name__ == "__main__":
    forger = DynamicBatchWorldForge()
    forger.forge_batch_world()
