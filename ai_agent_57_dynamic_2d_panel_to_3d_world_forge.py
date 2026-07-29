# ==============================================================================
# Ai_Agent_57_Dynamic_2D_Panel_To_3D_World_Forge.py
# MODULE H: Omni Generative Matrix (3D World Forge)
# ==============================================================================

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

class AiAgent57Dynamic2DPanelTo3DWorldForge:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_57_Dynamic_2D_Panel_To_3D_World_Forge"
        
        # RULE 2: UNIVERSAL PATH ISOLATION (No C:/, D:/, G:/ hardcoding)
        self.workspace_root = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.module_h_dir = os.path.join(self.workspace_root, "Module_H_Generative")
        
        # Upstream Inputs
        self.vision_outputs_dir = os.path.join(self.module_h_dir, "outputs_vision_layers")
        self.meshes_dir = os.path.join(self.module_h_dir, "3d_meshes")
        self.input_mesh_blueprint = os.path.join(self.meshes_dir, "56_master_mesh_blueprint.json")
        
        # Outputs
        self.output_dir = os.path.join(self.module_h_dir, "3d_worlds")
        self.output_world_blueprint = os.path.join(self.output_dir, "57_master_world_blueprint.json")
        
        # System States
        self.state_file = os.path.join(self.workspace_root, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_root, "global_config.json")
        
        # API Keys
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        self._initialize_directories()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _initialize_directories(self):
        for d in [self.workspace_root, self.module_h_dir, self.output_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    # RULE 3: IDEMPOTENCY SCRUBBING
    def scrub_workspace(self):
        self.log("Scrubbing legacy 3D worlds to ensure idempotency...", "INFO")
        for filename in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                self.log(f"Failed to delete {file_path}. Reason: {e}", "WARNING")

    # RULE 4: LIMITLESS FLUIDITY
    def load_global_config(self):
        default_config = {
            "video_format": "long_form",
            "theme": "dark_cinematic",
            "blender_executable": "blender" # Can be overridden to specific path like "C:/Program Files/Blender..."
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception:
                pass
        return default_config

    # RULE 5: BULLETPROOF JSON CLEANER
    def clean_json_response(self, raw_response):
        try:
            cleaned = re.sub(r'```(?:json)?\n(.*?)```', r'\1', raw_response, flags=re.DOTALL)
            cleaned = cleaned.strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            start = raw_response.find("{")
            end = raw_response.rfind("}")
            if start != -1 and end != -1:
                try: return json.loads(raw_response[start:end+1])
                except: pass
            return None

    # RULE 10: 100% OFFLINE AUTONOMY FALLBACK
    def _get_procedural_fallback_config(self, scene_name, config):
        self.log(f"Engaging Procedural Fallback Lighting for {scene_name}...", "STATUS")
        
        # Adapt math to fluidity rules
        bg_hex = "#07070B" if config.get("theme") == "dark_cinematic" else "#87CEEB"
        main_light = "#FFEFE0" if config.get("theme") == "dark_cinematic" else "#FFFFFF"
        
        return {
            "camera": {
                "location": [0.0, -6.5, 1.2],
                "rotation_euler": [85.0, 0.0, 0.0],
                "focal_length": 35.0
            },
            "lights": [
                {"type": "SUN", "energy": 5.0, "color_hex": main_light, "direction": [0.5, -0.3, -1.0]},
                {"type": "POINT", "energy": 25.0, "color_hex": "#FF00FF", "location": [-1.0, -1.5, 1.8]},
                {"type": "POINT", "energy": 12.0, "color_hex": "#00FFFF", "location": [1.5, -0.5, 0.8]}
            ],
            "world_ambient": {
                "background_color_hex": bg_hex,
                "ambient_strength": 0.15
            }
        }

    # RULE 6: QUAD-CORE FALLBACK MATRIX FOR LIGHTING
    def _query_lighting_blueprint(self, vision_data, scene_name, config):
        bg_desc = vision_data.get("environment_description", "Dark empty space")
        char_name = vision_data.get("character_name", "Character")
        blueprint = vision_data.get("lighting_blueprint", {})
        time_of_day = blueprint.get("time_of_day", "Unknown")
        theme = config.get("theme", "standard")

        ai_prompt = f"""
        You are a AAA Cinematic Lighting Director. Design a 3D Blender lighting and camera setup for scene '{scene_name}'.
        Character: {char_name}
        Background Context: {bg_desc}
        Time of Day: {time_of_day}
        Overall Theme: {theme}

        Return ONLY raw JSON, no markdown blocks. Format exactly like this:
        {{
          "camera": {{"location": [0.0, -5.0, 1.5], "rotation_euler": [80.0, 0.0, 0.0], "focal_length": 50.0}},
          "lights": [
            {{"type": "SUN", "energy": 4.0, "color_hex": "#FFFFFF", "direction": [0.2, -0.5, -1.0]}},
            {{"type": "POINT", "energy": 15.0, "color_hex": "#FF5500", "location": [1.5, -1.0, 2.0]}}
          ],
          "world_ambient": {{"background_color_hex": "#0A0A0F", "ambient_strength": 0.2}}
        }}
        """

        # Core 1: Gemini
        if self.gemini_api_key:
            try:
                self.log("Executing Core 1 (Gemini) for Lighting Blueprint...", "INFO")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self.clean_json_response(res_text)
                    if parsed: return parsed
            except Exception as e:
                self.log(f"Core 1 Failed: {e}", "WARNING")

        # Core 2: OpenAI
        if self.openai_api_key:
            try:
                self.log("Executing Core 2 (OpenAI) for Lighting Blueprint...", "INFO")
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")}
                payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": ai_prompt}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
                    parsed = self.clean_json_response(res_text)
                    if parsed: return parsed
            except Exception as e:
                self.log(f"Core 2 Failed: {e}", "WARNING")

        # Core 3: Ollama Local API
        try:
            self.log("Executing Core 3 (Ollama Local) for Lighting Blueprint...", "INFO")
            url = "http://127.0.0.1:11434/api/generate"
            payload = {"model": "llama3", "prompt": ai_prompt, "stream": False}
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
            with urllib.request.urlopen(req, timeout=20) as response:
                res_text = json.loads(response.read().decode("utf-8"))["response"]
                parsed = self.clean_json_response(res_text)
                if parsed: return parsed
        except Exception as e:
            self.log(f"Core 3 Failed: {e}", "WARNING")

        # Core 4: Procedural Math Fallback
        return self._get_procedural_fallback_config(scene_name, config)

    # RULE 9: ACTIONABLE ABSTRACTION (Injects exact paths into a Blender Python Script)
    def _generate_blender_python_script(self, scene_name, scene_data, out_blend_path):
        safe_mesh_path = scene_data["mesh"].replace("\\", "/") if scene_data["mesh"] else ""
        safe_bg_path = scene_data["bg_image"].replace("\\", "/") if scene_data["bg_image"] else ""
        safe_depth_path = scene_data["depth_image"].replace("\\", "/") if scene_data["depth_image"] else ""
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
    if not os.path.exists(bg_path): return
        
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
    except: pass
    plane.data.materials.append(mat)

    if os.path.exists(depth_path):
        disp_mod = plane.modifiers.new(name="DepthDisplacement", type='DISPLACE')
        disp_tex = bpy.data.textures.new("DepthTexture", type='IMAGE')
        try:
            disp_tex.image = bpy.data.images.load(depth_path)
            disp_mod.texture = disp_tex
            disp_mod.strength = 1.5
            disp_mod.mid_level = 0.5
        except: pass

try:
    clear_scene()

    # 1. Mesh Import Pipeline
    mesh_path = "{safe_mesh_path}"
    if mesh_path and os.path.exists(mesh_path):
        try: bpy.ops.wm.obj_import(filepath=mesh_path)
        except AttributeError: bpy.ops.import_scene.obj(filepath=mesh_path)

    # 2. Universal 2.5D Environment Pipeline
    create_2point5d_background("{safe_bg_path}", "{safe_depth_path}")

    # 3. Dynamic Camera Rigging
    cam_data = bpy.data.cameras.new(name="Cinematic_Camera")
    cam_obj = bpy.data.objects.new("Cinematic_CamObj", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    cam_obj.location = {cam.get('location', [0.0, -6.5, 1.2])}
    cam_obj.rotation_euler = [math.radians(r) for r in {cam.get('rotation_euler', [85.0, 0.0, 0.0])}]
    cam_data.lens = {cam.get('focal_length', 35.0)}
    bpy.context.scene.camera = cam_obj

    # 4. Neural-Guided Lighting
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

    world = bpy.context.scene.world
    if world:
        world.use_nodes = False
        world.color = hex_to_rgb("{bg_color}")[:3]

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")
except Exception as e:
    print(f"OMNIMATRIX_BLENDER_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.output_dir, f"temp_{scene_name}_forge.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute(self):
        self.log("System Initializing...", "INFO")
        
        # RULE 7: ATOMIC HANDSHAKE (Validation)
        state = {}
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                try: state = json.load(f)
                except: pass
                
        if state.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{state.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        self.scrub_workspace()
        config = self.load_global_config()
        blender_executable = config.get("blender_executable", "blender")
        
        if not os.path.exists(self.input_mesh_blueprint):
            self.log("Agent 56 Blueprint not found. Run Agent 56 first.", "FATAL")
            sys.exit(1)
            
        with open(self.input_mesh_blueprint, "r", encoding="utf-8") as f:
            mesh_blueprint = json.load(f)
            
        master_world_config = {}

        for scene_name, mesh_data in mesh_blueprint.items():
            self.log(f"--- Forging 3D Stage for: {scene_name} ---", "INFO")
            
            vision_json_path = os.path.join(self.vision_outputs_dir, f"{scene_name}_blueprint.json")
            
            vision_data = {}
            if os.path.exists(vision_json_path):
                try:
                    with open(vision_json_path, "r", encoding="utf-8") as vf:
                        vision_data = json.load(vf)
                except Exception as e:
                    self.log(f"Error reading vision data: {e}", "WARNING")

            layers = vision_data.get("layers", {})
            bg_path = layers.get("bg_layer", "")
            depth_path = layers.get("depth_map", "")
            mesh_path = mesh_data.get("mesh", "")

            # Blueprint Extraction via AI (or Fallback)
            layout_config = self._query_lighting_blueprint(vision_data, scene_name, config)
            out_blend_path = os.path.join(self.output_dir, f"{scene_name}_stage.blend")

            # Actionable Abstraction
            script_path = self._generate_blender_python_script(scene_name, {
                "mesh": mesh_path,
                "bg_image": bg_path,
                "depth_image": depth_path,
                "layout": layout_config
            }, out_blend_path)
            
            # Headless Execution (Rule 10 resilience applies here too, script won't crash if paths are empty)
            self.log(f"Executing Headless Blender for {scene_name}...", "INFO")
            command = [blender_executable, "-b", "-P", script_path]
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                    self.log(f"Stage saved: {scene_name}_stage.blend", "SUCCESS")
                    master_world_config[scene_name] = {
                        "environment_blend": out_blend_path,
                        "layout_config": layout_config
                    }
                else:
                    self.log(f"Blender failed. Log snippet: {result.stdout[-300:]}", "ERROR")
            except Exception as e:
                self.log(f"Subprocess failed to launch blender: {e}", "CRITICAL")
                self.log("Ensure 'blender' is in system PATH or set 'blender_executable' in global_config.json", "WARNING")
                
            if os.path.exists(script_path):
                os.remove(script_path)

        with open(self.output_world_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_world_config, f, indent=4)
        
        # RULE 7: ATOMIC HANDSHAKE (Advance State)
        state["last_active_agent"] = self.agent_name
        # Heading to Animation!
        state["next_agent"] = "Ai_Agent_58_Animation_And_Camera_Director" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Module H Vision/Forge Complete. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    forger = AiAgent57Dynamic2DPanelTo3DWorldForge()
    forger.execute()

# ==============================================================================
# END OF FILE
# ==============================================================================
