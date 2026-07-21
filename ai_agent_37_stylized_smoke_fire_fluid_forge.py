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

class StylizedSmokeFireFluidForge:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 37: stylized_smoke_fire_fluid_forge"
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

    def _load_upstream_vfx(self):
        vfx_path = os.path.join(self.workspace_dir, "35_procedural_vfx_blueprint.json")
        fluid_emitters = []

        if os.path.exists(vfx_path):
            try:
                with open(vfx_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for profile in data.get("vfx_procedural_profiles", []):
                    fluid_emitters.append({
                        "timestamp_sec": profile.get("timestamp_sec", 0.0),
                        "origin_xyz": profile.get("vfx_origin_xyz", [0.0, 0.0, 0.0]),
                        "base_intensity": profile.get("glow_intensity_emission", 50.0)
                    })
            except Exception as e:
                self.log_message(f"Upstream VFX data load warning: {str(e)}", "WARNING")

        if not fluid_emitters:
            self.log_message("No active VFX targets found. Deploying default stylized fireball.", "INFO")
            fluid_emitters = [{"timestamp_sec": 2.1, "origin_xyz": [0.0, 2.0, -1.0], "base_intensity": 100.0}]

        return fluid_emitters

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

    def _save_to_workspace(self, data, filename="37_stylized_fluid_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log_message(f"Stylized fluid blueprint saved to '{file_path}'", "INFO")
            return file_path
        except Exception as e:
            self.log_message(f"Critical Error: Unable to save fluid metadata: {str(e)}", "CRITICAL")
            return None

    def forge_stylized_fluid_parameters(self):
        emitters = self._load_upstream_vfx()
        self.log_message("Resolving stylized mesh boundaries and ramp shaders...", "INFO")

        system_prompt = (
            "You are an elite Anime FX Animator and fluid simulation pipeline director.\n"
            "Design physical parameters for high-velocity stylized smoke, fire, and water animations.\n"
            "For each emitter hotspot, design exactly 1 fluid configuration inside a list named 'fluid_simulation_profiles':\n"
            "- 'timestamp_sec': float matching the simulation cue.\n"
            "- 'origin_xyz': array of 3 floats [x,y,z] from the emitter.\n"
            "- 'simulation_domain_type': string ('bubbly_impact_smoke', 'cel_shaded_fireblast', 'ink_splash_fluid').\n"
            "- 'dissipation_rate_frames': integer (range 15 to 120).\n"
            "- 'buoyancy_density_force': float (range -2.0 to 5.0).\n"
            "- 'cel_shader_border_threshold': float (range 0.05 to 0.75).\n"
            "- 'vorticity_swirl_strength': float (range 0.0 to 4.5).\n"
            "- 'fluid_viscosity_multiplier': float (default 1.0).\n"
            "Format strictly as JSON with key 'fluid_simulation_profiles'."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": json.dumps(emitters)}], "response_format": {"type": "json_object"}}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=50) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    final_output = {"fluid_simulation_profiles": json.loads(cleaned).get("fluid_simulation_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Failed: {str(e)}", "WARNING")

        if not final_output:
            self.log_message("Directing procedural fluid solver fallback.", "INFO")
            final_output = self._execute_procedural_fallback(emitters)
            
        self._save_to_workspace(final_output)
        self._bake_stylized_fluids_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, emitters):
        profiles = []
        for em in emitters:
            ts = float(em.get("timestamp_sec", 0.0))
            origin = em.get("origin_xyz", [0.0, 0.0, 0.0])
            intensity = float(em.get("base_intensity", 50.0))

            if intensity > 80.0:
                profiles.append({"timestamp_sec": ts, "origin_xyz": origin, "simulation_domain_type": "cel_shaded_fireblast", "dissipation_rate_frames": 35, "buoyancy_density_force": 3.8, "cel_shader_border_threshold": 0.55, "vorticity_swirl_strength": 2.8, "fluid_viscosity_multiplier": 1.0})
            elif intensity > 30.0:
                profiles.append({"timestamp_sec": ts, "origin_xyz": origin, "simulation_domain_type": "bubbly_impact_smoke", "dissipation_rate_frames": 85, "buoyancy_density_force": -0.5, "cel_shader_border_threshold": 0.15, "vorticity_swirl_strength": 4.2, "fluid_viscosity_multiplier": 1.0})
            else:
                profiles.append({"timestamp_sec": ts, "origin_xyz": origin, "simulation_domain_type": "ink_splash_fluid", "dissipation_rate_frames": 45, "buoyancy_density_force": 0.2, "cel_shader_border_threshold": 0.70, "vorticity_swirl_strength": 0.5, "fluid_viscosity_multiplier": 4.5})
        return {"fluid_simulation_profiles": profiles}

    def _bake_stylized_fluids_in_blender(self, fluid_data):
        """God Level Feature: Creates Procedural Displaced Meshes with Cel Shading mapped to Animation Curves"""
        self.log_message("Connecting to Engine Core: Forging Anime Fluids in Blender...", "INFO")
        
        script_content = f"""
import bpy
import math

profiles = {json.dumps(fluid_data.get('fluid_simulation_profiles', []))}
fps = bpy.context.scene.render.fps

bpy.context.scene.render.engine = 'BLENDER_EEVEE'

for idx, p in enumerate(profiles):
    sim_type = p['simulation_domain_type']
    spawn_frame = int(p['timestamp_sec'] * fps)
    dissolve_frames = p['dissipation_rate_frames']
    buoyancy = p['buoyancy_density_force']
    vorticity = p['vorticity_swirl_strength']
    threshold = p['cel_shader_border_threshold']
    loc = tuple(p['origin_xyz'])
    
    # 1. GENERATE PROCEDURAL MESH (Instead of heavy Mantaflow)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=1.0, location=loc)
    obj = bpy.context.active_object
    obj.name = f"VFX_Fluid_{{sim_type}}_{{idx}}"
    
    # Add displacement for bubbly/spiky look
    mod_sub = obj.modifiers.new(name="FluidSubdiv", type='SUBSURF')
    mod_sub.levels = 2
    
    mod_disp = obj.modifiers.new(name="FluidDisplace", type='DISPLACE')
    tex = bpy.data.textures.new(f"Tex_FluidNoise_{{idx}}", type='CLOUDS')
    tex.noise_scale = 1.5 if sim_type == 'bubbly_impact_smoke' else 0.8
    mod_disp.texture = tex
    mod_disp.strength = 1.2
    
    # 2. CREATE ANIME CEL-SHADER
    mat = bpy.data.materials.new(name=f"MAT_{{obj.name}}")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    nt = mat.node_tree
    nt.nodes.clear()
    
    out_node = nt.nodes.new('ShaderNodeOutputMaterial')
    mix_node = nt.nodes.new('ShaderNodeMixShader')
    trans_node = nt.nodes.new('ShaderNodeBsdfTransparent')
    emit_node = nt.nodes.new('ShaderNodeEmission')
    
    # Noise to control Cel Edges
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 3.0
    
    # The God-Level Cel Ramp
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.interpolation = 'CONSTANT'
    ramp.color_ramp.elements[0].position = threshold
    ramp.color_ramp.elements[0].color = (0,0,0,0) # Transparent shadow
    
    if sim_type == 'cel_shaded_fireblast':
        ramp.color_ramp.elements[1].color = (1.0, 0.2, 0.0, 1.0) # Bright Fire
        emit_node.inputs['Strength'].default_value = 15.0
    elif sim_type == 'bubbly_impact_smoke':
        ramp.color_ramp.elements[1].color = (0.7, 0.7, 0.7, 1.0) # Ash Smoke
        emit_node.inputs['Strength'].default_value = 1.0
    else:
        ramp.color_ramp.elements[1].color = (0.01, 0.01, 0.01, 1.0) # Dark Ink
        emit_node.inputs['Strength'].default_value = 0.5

    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], emit_node.inputs['Color'])
    
    # Transparency Dissolve setup
    alpha_value = nt.nodes.new('ShaderNodeValue')
    alpha_value.outputs[0].default_value = 1.0
    
    nt.links.new(alpha_value.outputs[0], mix_node.inputs['Fac'])
    nt.links.new(trans_node.outputs['BSDF'], mix_node.inputs[1])
    nt.links.new(emit_node.outputs['Emission'], mix_node.inputs[2])
    nt.links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
    
    obj.data.materials.append(mat)
    
    # 3. ANIMATION LORE (Spawning, Buoyancy, Vorticity, Dissipation)
    
    # Spawn visibility
    obj.hide_viewport = True; obj.hide_render = True
    obj.keyframe_insert(data_path="hide_viewport", frame=max(1, spawn_frame - 1))
    obj.keyframe_insert(data_path="hide_render", frame=max(1, spawn_frame - 1))
    obj.hide_viewport = False; obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=spawn_frame)
    obj.keyframe_insert(data_path="hide_render", frame=spawn_frame)
    
    # Explosion Scale Curve
    obj.scale = (0.1, 0.1, 0.1)
    obj.keyframe_insert(data_path="scale", frame=spawn_frame)
    obj.scale = (2.5, 2.5, 2.5) if sim_type == 'bubbly_impact_smoke' else (1.5, 1.5, 1.5)
    obj.keyframe_insert(data_path="scale", frame=spawn_frame + 10) # 10 frames to max size
    
    # Buoyancy (Rising) & Vorticity (Spinning)
    end_frame = spawn_frame + dissolve_frames
    obj.location[2] += buoyancy * 2.0
    obj.keyframe_insert(data_path="location", index=2, frame=end_frame)
    
    obj.rotation_euler[2] += vorticity * 3.14 # Spin in Z axis
    obj.keyframe_insert(data_path="rotation_euler", index=2, frame=end_frame)
    
    # Dissolve Alpha Curve
    alpha_value.outputs[0].default_value = 1.0
    alpha_value.outputs[0].keyframe_insert(data_path="default_value", frame=spawn_frame + int(dissolve_frames/2))
    alpha_value.outputs[0].default_value = 0.0
    alpha_value.outputs[0].keyframe_insert(data_path="default_value", frame=end_frame)

bpy.ops.wm.save_mainfile()
"""
        script_path = os.path.join(self.workspace_dir, "temp_fluid_forge.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Baking stylized smoke & fire into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Anime Smoke, Fire, and Fluids successfully injected.", "INFO")

if __name__ == "__main__":
    forge = StylizedSmokeFireFluidForge()
    forge.forge_stylized_fluid_parameters()
    print("--- OMNIMATRIX VFX STUDIO: AGENT 37 COMPLETE ---")
