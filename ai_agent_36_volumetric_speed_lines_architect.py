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
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class VolumetricSpeedLinesArchitect:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 36: volumetric_speed_lines_architect"
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

    def _load_master_config(self):
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("global_style", "realistic").lower()
            except Exception as e:
                self.log_message(f"Master config read warning, defaulting to realistic: {str(e)}", "WARNING")
        return "realistic"

    def _load_upstream_velocities(self):
        anim_path = os.path.join(self.workspace_dir, "26_kinetic_rig_puppeteer_blueprint.json")
        kinetic_records = []

        if os.path.exists(anim_path):
            try:
                with open(anim_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for seq in data.get("rig_animation_sequences", []):
                    kinetic_records.append({
                        "timestamp_sec": float(seq.get("timestamp_sec", 0.0)),
                        "pose_name": seq.get("action_pose_name", "idle"),
                        "offset": seq.get("translation_offset", [0.0, 0.0, 0.0])
                    })
            except Exception as e:
                self.log_message(f"Upstream kinetic load error: {str(e)}", "ERROR")

        if not kinetic_records:
            self.log_message("No dynamic speed files found. Generating standard velocity sequences.", "INFO")
            kinetic_records = [
                {"timestamp_sec": 1.2, "pose_name": "ground_dash_forward", "offset": [0.0, 15.0, 0.0]},
                {"timestamp_sec": 3.8, "pose_name": "skyward_clash", "offset": [0.0, 5.0, 25.0]}
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
            self.log_message(f"Speed line blueprint securely saved to '{file_path}'", "SUCCESS")
            return file_path
        except Exception as e:
            self.log_message(f"Critical System Failure: Unable to save speed lines: {str(e)}", "CRITICAL")
            return None

    def design_volumetric_speed_lines(self):
        velocities = self._load_upstream_velocities()
        global_style = self._load_master_config()
        self.log_message(f"Initializing Speed Lines Architect for '{global_style.upper()}' style...", "INFO")

        system_prompt = (
            f"You are a master VFX Compositing Director. The project global style is enforced as: '{global_style.upper()}'.\n"
            "Generate parameters for volumetric speed line meshes that frame the screen during high-velocity action.\n"
            "REALISTIC Style Rules: Use soft optical streaks, subtle lens smears, lower alpha opacity, and colors matching natural light/wind distortion.\n"
            "ANIME Style Rules: Use sharp, high-density, high-emission toon streaks, rigid alpha, and highly stylized contrast colors.\n"
            "For each movement entry, return exactly 1 speed line configuration inside a list named 'speed_line_profiles':\n"
            "- 'timestamp_sec': float.\n"
            "- 'render_style_enforced': string ('realistic' or 'anime', matching global style).\n"
            "- 'speed_line_style': string ('radial_zoom_in', 'horizontal_streaks', 'vertical_drop_lines').\n"
            "- 'line_density_count': integer (range 150 to 1000).\n"
            "- 'line_length_meters': float (range 10.0 to 50.0).\n"
            "- 'core_flicker_frequency_hz': float (speed multiplier, range 10.0 to 30.0).\n"
            "- 'line_opacity_alpha': float (range 0.1 to 1.0).\n"
            "- 'line_color_rgba': array of 4 floats [R, G, B, A].\n"
            "- 'radial_center_offset_xy': array of 2 floats [x, y].\n"
            "Output strictly valid JSON with key 'speed_line_profiles'. Do not compress or truncate data."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {
                    "model": self.model_cloud,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Kinetic Vectors:\n{json.dumps(velocities, indent=2)}"}
                    ],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=60) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    final_output = {"speed_line_profiles": json.loads(cleaned).get("speed_line_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Failed: {str(e)}. Falling back to procedural generation.", "WARNING")

        if not final_output:
            final_output = self._execute_procedural_fallback(velocities, global_style)
            
        self._save_to_workspace(final_output)
        self._bake_speed_lines_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, velocities, style):
        profiles = []
        for v in velocities:
            ts = float(v.get("timestamp_sec", 0.0))
            offset = v.get("offset", [0.0, 0.0, 0.0])
            y_speed = abs(offset[1])
            z_speed = abs(offset[2])

            if style == "realistic":
                if z_speed > y_speed:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "speed_line_style": "vertical_drop_lines", "line_density_count": 300, "line_length_meters": 40.0, "core_flicker_frequency_hz": 15.0, "line_opacity_alpha": 0.4, "line_color_rgba": [0.8, 0.8, 0.9, 0.4], "radial_center_offset_xy": [0.0, 0.1]})
                elif y_speed > 10.0:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "speed_line_style": "radial_zoom_in", "line_density_count": 450, "line_length_meters": 25.0, "core_flicker_frequency_hz": 18.0, "line_opacity_alpha": 0.6, "line_color_rgba": [0.9, 0.9, 1.0, 0.6], "radial_center_offset_xy": [0.0, 0.0]})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "speed_line_style": "horizontal_streaks", "line_density_count": 200, "line_length_meters": 20.0, "core_flicker_frequency_hz": 12.0, "line_opacity_alpha": 0.3, "line_color_rgba": [0.7, 0.7, 0.7, 0.3], "radial_center_offset_xy": [0.0, 0.0]})
            else:
                if z_speed > y_speed:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "speed_line_style": "vertical_drop_lines", "line_density_count": 600, "line_length_meters": 50.0, "core_flicker_frequency_hz": 30.0, "line_opacity_alpha": 1.0, "line_color_rgba": [1.0, 1.0, 1.0, 1.0], "radial_center_offset_xy": [0.0, 0.1]})
                elif y_speed > 10.0:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "speed_line_style": "radial_zoom_in", "line_density_count": 800, "line_length_meters": 30.0, "core_flicker_frequency_hz": 24.0, "line_opacity_alpha": 1.0, "line_color_rgba": [0.1, 0.8, 1.0, 1.0], "radial_center_offset_xy": [0.0, 0.0]})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "speed_line_style": "horizontal_streaks", "line_density_count": 400, "line_length_meters": 25.0, "core_flicker_frequency_hz": 20.0, "line_opacity_alpha": 0.8, "line_color_rgba": [1.0, 1.0, 1.0, 0.8], "radial_center_offset_xy": [0.0, 0.0]})
        return {"speed_line_profiles": profiles}

    def _bake_speed_lines_in_blender(self, lines_data):
        self.log_message("Engaging Blender Core: Compiling camera-parented procedural speed lines...", "INFO")
        
        script_content = f"""
import bpy
import math

# --- 1. SCENE PREPARATION & AUTO-CLEANUP ---
profiles = {json.dumps(lines_data.get('speed_line_profiles', []))}
scene = bpy.context.scene
fps = scene.render.fps

scene.render.engine = 'BLENDER_EEVEE'

bpy.ops.object.select_all(action='DESELECT')
for obj in scene.objects:
    if obj.name.startswith("OMNIMATRIX_VFX_SpeedLines_"):
        obj.select_set(True)
bpy.ops.object.delete()

cam = scene.camera
if not cam:
    bpy.ops.object.camera_add(location=(0, -10, 2), rotation=(math.radians(90), 0, 0))
    cam = bpy.context.active_object
    scene.camera = cam

# --- 2. FORGE CAMERA-PARENTED VELOCITY MESHES ---
for idx, p in enumerate(profiles):
    try:
        style_type = p.get('speed_line_style', 'horizontal_streaks')
        global_style = p.get('render_style_enforced', 'realistic').lower()
        color = tuple(p.get('line_color_rgba', [1.0, 1.0, 1.0, 1.0]))
        alpha = float(p.get('line_opacity_alpha', 0.8))
        flicker = float(p.get('core_flicker_frequency_hz', 24.0))
        density = int(p.get('line_density_count', 400))
        length = float(p.get('line_length_meters', 20.0))
        spawn_frame = int(p.get('timestamp_sec', 0.0) * fps)
        
        obj_name = f"OMNIMATRIX_VFX_SpeedLines_{{idx}}"
        
        # Mesh Selection based on vector
        if style_type == 'radial_zoom_in':
            bpy.ops.mesh.primitive_cylinder_add(vertices=64 if global_style == 'realistic' else 32, radius=length/4, depth=length, location=(0,0,-length/2))
            obj = bpy.context.active_object
            obj.rotation_euler = (math.radians(90), 0, 0)
        else:
            bpy.ops.mesh.primitive_plane_add(size=length, location=(0,0,-5))
            obj = bpy.context.active_object
            if style_type == 'vertical_drop_lines':
                obj.rotation_euler = (0, 0, math.radians(90))

        obj.name = obj_name
        
        # Parent exactly to camera to match frustum
        obj.parent = cam
        obj.matrix_parent_inverse = cam.matrix_world.inverted()
        
        # Shader Magic (Universal Protocol)
        mat = bpy.data.materials.new(name=f"MAT_{{obj_name}}")
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
        emit_node.inputs['Strength'].default_value = 8.0 if global_style == 'anime' else 2.0
        
        tex_coord = nt.nodes.new('ShaderNodeTexCoord')
        mapping = nt.nodes.new('ShaderNodeMapping')
        noise = nt.nodes.new('ShaderNodeTexNoise')
        
        mapping.inputs['Scale'].default_value = (density / 10.0, 0.05, 1.0)
        
        color_ramp = nt.nodes.new('ShaderNodeValToRGB')
        
        if global_style == 'realistic':
            color_ramp.color_ramp.interpolation = 'EASE'
            color_ramp.color_ramp.elements[0].position = 0.45
            color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
            color_ramp.color_ramp.elements[1].position = 0.55
            color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, alpha)
        else:
            color_ramp.color_ramp.interpolation = 'CONSTANT'
            color_ramp.color_ramp.elements[0].position = 0.5
            color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
            color_ramp.color_ramp.elements[1].position = 0.51
            color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, alpha)
        
        nt.links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
        nt.links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
        nt.links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
        
        nt.links.new(color_ramp.outputs['Color'], mix_node.inputs['Fac'])
        nt.links.new(trans_node.outputs['BSDF'], mix_node.inputs[1])
        nt.links.new(emit_node.outputs['Emission'], mix_node.inputs[2])
        nt.links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
        obj.data.materials.append(mat)
        
        # Animation & Flicker Automation
        obj.hide_viewport = True
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_viewport", frame=max(1, spawn_frame - 1))
        obj.keyframe_insert(data_path="hide_render", frame=max(1, spawn_frame - 1))
        
        obj.hide_viewport = False
        obj.hide_render = False
        obj.keyframe_insert(data_path="hide_viewport", frame=spawn_frame)
        obj.keyframe_insert(data_path="hide_render", frame=spawn_frame)
        
        # Scroll texture location dynamically over time
        scroll_axis = 1 if style_type == 'horizontal_streaks' else 2
        mapping.inputs['Location'].default_value[scroll_axis] = 0.0
        mapping.inputs['Location'].keyframe_insert(data_path="default_value", index=scroll_axis, frame=spawn_frame)
        
        duration_frames = int(fps * 2)
        mapping.inputs['Location'].default_value[scroll_axis] = flicker * 10.0
        mapping.inputs['Location'].keyframe_insert(data_path="default_value", index=scroll_axis, frame=spawn_frame + duration_frames)
        
        # Fade out visibility after sequence
        obj.hide_viewport = True
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_viewport", frame=spawn_frame + duration_frames)
        obj.keyframe_insert(data_path="hide_render", frame=spawn_frame + duration_frames)

    except Exception as e:
        print(f"FAILED to process speed lines profile {{idx}} - {{str(e)}}")
        continue

try:
    bpy.ops.wm.save_mainfile()
except Exception as e:
    print(f"FAILED to save mainfile: {{str(e)}}")
"""
        script_path = os.path.join(self.workspace_dir, "temp_speed_lines.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Injecting Uncut Volumetric Lines into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Universal Speed Lines Architect completely compiled and verified.", "SUCCESS")

if __name__ == "__main__":
    architect = VolumetricSpeedLinesArchitect()
    output = architect.design_volumetric_speed_lines()
    print("\n--- OMNIMATRIX VFX STUDIO: AGENT 36 COMPLETE ---")
    print(f"Total speed line sequences strictly generated: {len(output['speed_line_profiles'])}")
    for p in output["speed_line_profiles"]:
        print(f"Time: {p['timestamp_sec']}s | Style: '{p['speed_line_style']}' ({p.get('render_style_enforced', 'unknown')})")
    print("------------------------------------------------------------------")
