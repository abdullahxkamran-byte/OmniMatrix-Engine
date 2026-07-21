import os
import re
import sys
import json
import math
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
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class VolumetricSpeedLinesArchitect:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 36: Volumetric Speed Lines Architect"
        self.workspace_dir = workspace_dir
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        self.blender_path = blender_path
        
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        for d in [self.workspace_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_velocities(self):
        anim_path = os.path.join(self.workspace_dir, "26_kinetic_rig_puppeteer_blueprint.json")
        kinetic_records = []

        if os.path.exists(anim_path):
            try:
                with open(anim_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for seq in data.get("rig_animation_sequences", []):
                    kinetic_records.append({
                        "timestamp_sec": seq.get("timestamp_sec", 0.0),
                        "pose_name": seq.get("action_pose_name", "idle"),
                        "offset": seq.get("translation_offset", [0.0, 0.0, 0.0])
                    })
            except Exception as e:
                self.log_message(f"Upstream kinetic load warning: {str(e)}", "WARNING")

        if not kinetic_records:
            self.log_message("No dynamic speed files found. Generating standard dash parameters.", "INFO")
            kinetic_records = [
                {"timestamp_sec": 1.2, "pose_name": "ground_dash_forward", "offset": [0.0, 8.5, 0.0]},
                {"timestamp_sec": 3.8, "pose_name": "skyward_clash", "offset": [0.0, 2.0, 15.0]}
            ]

        return kinetic_records

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

    def _save_to_workspace(self, data, filename="36_volumetric_speed_lines_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log_message(f"Speed line blueprint written to '{file_path}'", "INFO")
            return file_path
        except Exception as e:
            self.log_message(f"Critical Error: Unable to save speed lines: {str(e)}", "CRITICAL")
            return None

    def design_volumetric_speed_lines(self):
        velocities = self._load_upstream_velocities()
        self.log_message("Designing frame flickering patterns and depth vectors...", "INFO")

        system_prompt = (
            "You are a master Cel-Animation & Composition Director specialized in dynamic anime action line shaders in Blender.\n"
            "Generate parameters for speed line meshes that dynamically frame the screen based on action velocities.\n"
            "For each movement entry, design exactly 1 speed line configuration in a list named 'speed_line_profiles':\n"
            "- 'timestamp_sec': float matching the movement timeline.\n"
            "- 'speed_line_style': string ('radial_zoom_in', 'horizontal_streaks', 'vertical_drop_lines').\n"
            "- 'line_density_count': integer (range 150 to 800).\n"
            "- 'line_length_meters': float (range 5.0 to 45.0).\n"
            "- 'core_flicker_frequency_hz': float (range 12.0 to 24.0).\n"
            "- 'line_opacity_alpha': float (range 0.2 to 1.0).\n"
            "- 'line_color_rgba': array of 4 floats [R, G, B, A].\n"
            "- 'radial_center_offset_xy': array of 2 floats [x, y].\n"
            "Format strictly as JSON with key 'speed_line_profiles'."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": json.dumps(velocities)}], "response_format": {"type": "json_object"}}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=50) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    final_output = {"speed_line_profiles": json.loads(cleaned).get("speed_line_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Failed: {str(e)}", "WARNING")

        if not final_output:
            self.log_message("Switching to procedural lines fallback generator.", "INFO")
            final_output = self._execute_procedural_fallback(velocities)
            
        self._save_to_workspace(final_output)
        self._bake_speed_lines_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, velocities):
        profiles = []
        for v in velocities:
            ts = float(v.get("timestamp_sec", 0.0))
            offset = v.get("offset", [0.0, 0.0, 0.0])
            y_speed = abs(offset[1])
            z_speed = abs(offset[2])

            if z_speed > y_speed:
                profiles.append({"timestamp_sec": ts, "speed_line_style": "vertical_drop_lines", "line_density_count": 450, "line_length_meters": 35.0, "core_flicker_frequency_hz": 24.0, "line_opacity_alpha": 0.8, "line_color_rgba": [1.0, 1.0, 1.0, 0.8], "radial_center_offset_xy": [0.0, 0.1]})
            elif y_speed > 5.0:
                profiles.append({"timestamp_sec": ts, "speed_line_style": "radial_zoom_in", "line_density_count": 600, "line_length_meters": 20.0, "core_flicker_frequency_hz": 18.0, "line_opacity_alpha": 0.95, "line_color_rgba": [0.1, 0.7, 1.0, 0.9], "radial_center_offset_xy": [0.0, 0.0]})
            else:
                profiles.append({"timestamp_sec": ts, "speed_line_style": "horizontal_streaks", "line_density_count": 200, "line_length_meters": 15.0, "core_flicker_frequency_hz": 12.0, "line_opacity_alpha": 0.5, "line_color_rgba": [0.9, 0.9, 0.9, 0.5], "radial_center_offset_xy": [0.0, 0.0]})
        return {"speed_line_profiles": profiles}

    def _bake_speed_lines_in_blender(self, lines_data):
        """God Level Feature: Generates Camera-Parented Volumetric Speed Lines via Python Injection"""
        self.log_message("Connecting to Engine Core: Baking Speed Lines into Stage...", "INFO")
        
        script_content = f"""
import bpy
import math

profiles = {json.dumps(lines_data.get('speed_line_profiles', []))}
fps = bpy.context.scene.render.fps

bpy.context.scene.render.engine = 'BLENDER_EEVEE'

cam = bpy.context.scene.camera
if not cam:
    bpy.ops.object.camera_add(location=(0, -10, 2), rotation=(math.radians(90), 0, 0))
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam

for idx, p in enumerate(profiles):
    style = p['speed_line_style']
    color = tuple(p['line_color_rgba'])
    alpha = p['line_opacity_alpha']
    flicker = p['core_flicker_frequency_hz']
    spawn_frame = int(p['timestamp_sec'] * fps)
    length = p['line_length_meters']
    
    # 1. GENERATE MESH (Camera Space)
    if style == 'radial_zoom_in':
        # Cylinder around camera for classic radial tunnel effect
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=length/4, depth=length, location=(0,0,-length/2))
        obj = bpy.context.active_object
        obj.rotation_euler = (math.radians(90), 0, 0)
    else:
        # Flat plane for side scrolling / vertical falling
        bpy.ops.mesh.primitive_plane_add(size=length, location=(0,0,-5))
        obj = bpy.context.active_object
        if style == 'vertical_drop_lines':
            obj.rotation_euler = (0, 0, math.radians(90))

    obj.name = f"VFX_SpeedLines_{{idx}}"
    obj.parent = cam
    
    # 2. SHADER MAGIC (Procedural Stretched Alpha)
    mat = bpy.data.materials.new(name=f"MAT_{{obj.name}}")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    
    nt = mat.node_tree
    nt.nodes.clear()
    
    out_node = nt.nodes.new('ShaderNodeOutputMaterial')
    emit_node = nt.nodes.new('ShaderNodeEmission')
    trans_node = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix_node = nt.nodes.new('ShaderNodeMixShader')
    
    emit_node.inputs['Color'].default_value = color[:3] + (1.0,)
    emit_node.inputs['Strength'].default_value = 5.0
    
    # Texture setup for streaks
    tex_coord = nt.nodes.new('ShaderNodeTexCoord')
    mapping = nt.nodes.new('ShaderNodeMapping')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    
    # Stretch noise to create lines
    mapping.inputs['Scale'].default_value = (p['line_density_count']/10, 0.1, 1.0)
    
    color_ramp = nt.nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.interpolation = 'CONSTANT'
    color_ramp.color_ramp.elements[0].position = 0.5
    
    nt.links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    nt.links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    nt.links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    
    # Connect to Alpha Mix
    nt.links.new(color_ramp.outputs['Color'], mix_node.inputs['Fac'])
    nt.links.new(trans_node.outputs['BSDF'], mix_node.inputs[1])
    nt.links.new(emit_node.outputs['Emission'], mix_node.inputs[2])
    nt.links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
    obj.data.materials.append(mat)
    
    # 3. ANIMATE FLICKER SPEED & VISIBILITY
    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_viewport", frame=max(1, spawn_frame - 1))
    obj.keyframe_insert(data_path="hide_render", frame=max(1, spawn_frame - 1))
    
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=spawn_frame)
    obj.keyframe_insert(data_path="hide_render", frame=spawn_frame)
    
    # Animate Mapping Node X/Y for that anime scroll speed
    mapping.inputs['Location'].default_value[1] = 0.0
    mapping.inputs['Location'].keyframe_insert(data_path="default_value", index=1, frame=spawn_frame)
    mapping.inputs['Location'].default_value[1] = flicker * 5.0 
    mapping.inputs['Location'].keyframe_insert(data_path="default_value", index=1, frame=spawn_frame + int(fps))

bpy.ops.wm.save_mainfile()
"""
        script_path = os.path.join(self.workspace_dir, "temp_speed_lines.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Injecting Speed Lines into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Speed Lines fully integrated into OmniMatrix Engine.", "INFO")

if __name__ == "__main__":
    architect = VolumetricSpeedLinesArchitect()
    architect.design_volumetric_speed_lines()
    print("--- OMNIMATRIX VFX STUDIO: AGENT 36 COMPLETE ---")
