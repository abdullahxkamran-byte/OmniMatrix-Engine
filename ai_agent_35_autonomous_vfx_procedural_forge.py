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
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AutonomousVFXProceduralForge:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 35: autonomous_vfx_procedural_forge"
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

    def _load_upstream_destruction(self):
        fracture_path = os.path.join(self.workspace_dir, "30_environment_fracture_blueprint.json")
        energy_hotspots = []
        if os.path.exists(fracture_path):
            try:
                with open(fracture_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for ev in data.get("fracture_events", []):
                    energy_hotspots.append({
                        "timestamp_sec": ev.get("timestamp_sec", 0.0),
                        "vfx_origin_xyz": ev.get("fracture_center_xyz", [0.0, 0.0, 0.0]),
                        "impact_scale": ev.get("fracture_radius_meters", 1.0)
                    })
            except Exception as e:
                self.log_message(f"Upstream fracture load warning: {str(e)}", "WARNING")

        if not energy_hotspots:
            self.log_message("No destruction hotspots found. Injecting custom charging energy aura.", "INFO")
            energy_hotspots = [{"timestamp_sec": 1.5, "vfx_origin_xyz": [0.0, 1.2, 0.0], "impact_scale": 2.5}]
        return energy_hotspots

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

    def _save_to_workspace(self, data, filename="35_procedural_vfx_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log_message(f"Procedural VFX blueprint saved to '{file_path}'", "INFO")
            return file_path
        except Exception as e:
            self.log_message(f"Unable to save VFX blueprint: {str(e)}", "CRITICAL")
            return None

    def forge_procedural_vfx(self):
        hotspots = self._load_upstream_destruction()
        self.log_message("Generating lightning meshes and energy shader parameters...", "INFO")

        system_prompt = (
            "You are an expert VFX technical director specialized in procedural anime shader networks and lightning generator nodes in Blender.\n"
            "Your job is to design procedurally generated magical/sci-fi effects that spawn around high-energy impact coordinates.\n"
            "For each energy hotspot, design exactly 1 procedural VFX block inside a list named 'vfx_procedural_profiles' with these parameters:\n"
            "- 'timestamp_sec': float matching the action sequence.\n"
            "- 'vfx_type': string (choose from: 'lightning_arcs', 'energy_aura_glow', 'magic_circle_grid', 'plasma_sparks', 'severed_limb_blood_cap').\n"
            "- 'vfx_origin_xyz': array of 3 floats indicating the world coordinates of the effect.\n"
            "- 'glow_intensity_emission': float (defines shader emission strength; scale 10.0 to 150.0).\n"
            "- 'noise_distortion_scale': float (erratic distortion multiplier; range 0.5 to 15.0).\n"
            "- 'color_rgb': array of 3 floats representing the color [R, G, B] (scale 0.0 to 1.0).\n"
            "- 'particle_spawn_rate': integer (density of glowing sparks; range 0 to 500).\n"
            "Format strictly as JSON with key 'vfx_procedural_profiles'."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Hotspots:\n{json.dumps(hotspots)}"}], "response_format": {"type": "json_object"}}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=50) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    final_output = {"vfx_procedural_profiles": json.loads(cleaned).get("vfx_procedural_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Failed: {str(e)}", "WARNING")

        if not final_output:
            self.log_message("Switching to procedural fallback generator.", "INFO")
            final_output = self._execute_procedural_fallback(hotspots)
            
        self._save_to_workspace(final_output)
        self._bake_vfx_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, hotspots):
        profiles = []
        for hs in hotspots:
            scale = float(hs.get("impact_scale", 1.0))
            if scale > 2.0:
                profiles.append({"timestamp_sec": float(hs["timestamp_sec"]), "vfx_type": "lightning_arcs", "vfx_origin_xyz": hs["vfx_origin_xyz"], "glow_intensity_emission": 120.0, "noise_distortion_scale": 8.5, "color_rgb": [0.1, 0.6, 1.0], "particle_spawn_rate": 400})
            elif scale > 1.0:
                profiles.append({"timestamp_sec": float(hs["timestamp_sec"]), "vfx_type": "energy_aura_glow", "vfx_origin_xyz": hs["vfx_origin_xyz"], "glow_intensity_emission": 65.0, "noise_distortion_scale": 4.0, "color_rgb": [0.9, 0.1, 0.1], "particle_spawn_rate": 180})
            else:
                profiles.append({"timestamp_sec": float(hs["timestamp_sec"]), "vfx_type": "plasma_sparks", "vfx_origin_xyz": hs["vfx_origin_xyz"], "glow_intensity_emission": 25.0, "noise_distortion_scale": 1.2, "color_rgb": [1.0, 0.8, 0.0], "particle_spawn_rate": 75})
        return {"vfx_procedural_profiles": profiles}

    def _bake_vfx_in_blender(self, vfx_data):
        """God Level Feature: Actually connects to Blender to generate and animate the VFX"""
        self.log_message("Connecting to Engine Core: Baking Procedural VFX into Stage...", "INFO")
        
        # Script jo Blender ke andar run hoga
        script_content = f"""
import bpy

vfx_profiles = {json.dumps(vfx_data.get('vfx_procedural_profiles', []))}
fps = bpy.context.scene.render.fps

bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.eevee.use_bloom = True 

for idx, vfx in enumerate(vfx_profiles):
    v_type = vfx['vfx_type']
    loc = tuple(vfx['vfx_origin_xyz'])
    color = tuple(vfx['color_rgb']) + (1.0,)
    glow = vfx['glow_intensity_emission']
    noise_scale = vfx['noise_distortion_scale']
    spawn_frame = int(vfx['timestamp_sec'] * fps)
    
    # 1. GENERATE MESH BASED ON VFX TYPE
    if v_type == 'energy_aura_glow':
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=2.0, location=loc)
    elif v_type == 'lightning_arcs':
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.1, depth=5.0, location=loc)
    elif v_type == 'severed_limb_blood_cap':
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.15, depth=0.05, location=loc)
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, radius=1.0, location=loc)
        
    obj = bpy.context.active_object
    obj.name = f"VFX_Procedural_{{v_type}}_{{idx}}"
    
    # 2. ADD TURBULENT DISPLACEMENT (God Level Detail)
    mod = obj.modifiers.new(name="VFX_Distortion", type='DISPLACE')
    tex = bpy.data.textures.new(f"Tex_Noise_{{idx}}", type='CLOUDS')
    tex.noise_scale = 1.0
    mod.texture = tex
    mod.strength = noise_scale * 0.1
    
    # 3. CREATE EMISSION/BLOOD SHADER
    mat = bpy.data.materials.new(name=f"MAT_{{obj.name}}")
    mat.use_nodes = True
    mat.blend_method = 'ADD' if v_type != 'severed_limb_blood_cap' else 'OPAQUE'
    
    nt = mat.node_tree
    nt.nodes.clear()
    out_node = nt.nodes.new('ShaderNodeOutputMaterial')
    emit_node = nt.nodes.new('ShaderNodeEmission')
    
    emit_node.inputs['Color'].default_value = color
    emit_node.inputs['Strength'].default_value = glow if v_type != 'severed_limb_blood_cap' else 0.5
    nt.links.new(emit_node.outputs['Emission'], out_node.inputs['Surface'])
    obj.data.materials.append(mat)
    
    # 4. KEYFRAME ANIMATION (Sync with Timeline)
    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_viewport", frame=max(1, spawn_frame - 1))
    obj.keyframe_insert(data_path="hide_render", frame=max(1, spawn_frame - 1))
    
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=spawn_frame)
    obj.keyframe_insert(data_path="hide_render", frame=spawn_frame)
    
bpy.ops.wm.save_mainfile()
"""
        script_path = os.path.join(self.workspace_dir, "temp_vfx_forge.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Injecting VFX into {filename}...", "INFO")
                # Excuting Blender Headless Mode
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("VFX Forging completely baked into all stages.", "INFO")

if __name__ == "__main__":
    forge = AutonomousVFXProceduralForge()
    forge.forge_procedural_vfx()
    print("--- OMNIMATRIX VFX STUDIO: AGENT 35 PROCEDURAL FORGE COMPLETE ---")
