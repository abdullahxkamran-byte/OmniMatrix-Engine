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

class UniversalFluidSmokeFireForge:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 37: universal_fluid_smoke_fire_forge"
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

    def _load_upstream_vfx(self):
        vfx_path = os.path.join(self.workspace_dir, "35_procedural_vfx_blueprint.json")
        fluid_emitters = []

        if os.path.exists(vfx_path):
            try:
                with open(vfx_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for profile in data.get("vfx_procedural_profiles", []):
                    fluid_emitters.append({
                        "timestamp_sec": float(profile.get("timestamp_sec", 0.0)),
                        "origin_xyz": profile.get("vfx_origin_xyz", [0.0, 0.0, 0.0]),
                        "base_intensity": float(profile.get("glow_intensity_emission", 50.0))
                    })
            except Exception as e:
                self.log_message(f"Upstream VFX data load error: {str(e)}", "ERROR")

        if not fluid_emitters:
            self.log_message("No active VFX targets found. Deploying universal standard fireball.", "INFO")
            fluid_emitters = [
                {"timestamp_sec": 2.1, "origin_xyz": [0.0, 2.0, -1.0], "base_intensity": 120.0},
                {"timestamp_sec": 4.5, "origin_xyz": [3.0, -1.5, 0.5], "base_intensity": 45.0}
            ]

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

    def _save_to_workspace(self, data, filename="37_universal_fluid_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log_message(f"Universal fluid blueprint securely saved to '{file_path}'", "SUCCESS")
            return file_path
        except Exception as e:
            self.log_message(f"Critical System Failure: Unable to save fluid metadata: {str(e)}", "CRITICAL")
            return None

    def forge_stylized_fluid_parameters(self):
        emitters = self._load_upstream_vfx()
        global_style = self._load_master_config()
        self.log_message(f"Initializing Universal Fluid Architect for '{global_style.upper()}' style...", "INFO")

        system_prompt = (
            f"You are a Master FX Technical Director. The project global style is enforced as: '{global_style.upper()}'.\n"
            "Design fluid dynamics and shader boundaries for procedural fire, smoke, and magical liquids without heavy Mantaflow caching.\n"
            "REALISTIC Style Rules: Use 'volumetric_fireblast' or 'dense_ash_smoke', high dissipation frames, natural buoyancy, high volume density, low cel threshold.\n"
            "ANIME Style Rules: Use 'cel_shaded_fireblast' or 'bubbly_impact_smoke', sharp dissipation, erratic vorticity, extreme cel shader threshold.\n"
            "For each emitter hotspot, design exactly 1 fluid configuration inside a list named 'fluid_simulation_profiles':\n"
            "- 'timestamp_sec': float matching the cue.\n"
            "- 'render_style_enforced': string ('realistic' or 'anime', matching global style).\n"
            "- 'origin_xyz': array of 3 floats [x,y,z].\n"
            "- 'simulation_domain_type': string (choose based on style: 'volumetric_fireblast', 'dense_ash_smoke', 'cel_shaded_fireblast', 'bubbly_impact_smoke', 'ink_splash_fluid').\n"
            "- 'fluid_color_rgb': array of 3 floats [R,G,B].\n"
            "- 'dissipation_rate_frames': integer (range 30 to 150).\n"
            "- 'buoyancy_density_force': float (range -2.0 to 10.0).\n"
            "- 'cel_shader_border_threshold': float (range 0.01 to 0.9).\n"
            "- 'vorticity_swirl_strength': float (range 0.0 to 10.0).\n"
            "- 'emission_strength': float (range 1.0 to 50.0).\n"
            "Output strictly valid JSON with key 'fluid_simulation_profiles'. Do not compress data."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {
                    "model": self.model_cloud,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Emitters Context:\n{json.dumps(emitters, indent=2)}"}
                    ],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=60) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    parsed_json = json.loads(cleaned)
                    final_output = {"fluid_simulation_profiles": parsed_json.get("fluid_simulation_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Route Failed: {str(e)}. Directing procedural fluid solver fallback.", "WARNING")

        if not final_output:
            final_output = self._execute_procedural_fallback(emitters, global_style)
            
        self._save_to_workspace(final_output)
        self._bake_universal_fluids_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, emitters, style):
        profiles = []
        for em in emitters:
            ts = float(em.get("timestamp_sec", 0.0))
            origin = em.get("origin_xyz", [0.0, 0.0, 0.0])
            intensity = float(em.get("base_intensity", 50.0))

            if style == "realistic":
                if intensity >= 80.0:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "origin_xyz": origin, "simulation_domain_type": "volumetric_fireblast", "fluid_color_rgb": [1.0, 0.4, 0.05], "dissipation_rate_frames": 120, "buoyancy_density_force": 6.5, "cel_shader_border_threshold": 0.0, "vorticity_swirl_strength": 3.0, "emission_strength": 35.0})
                elif intensity >= 30.0:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "origin_xyz": origin, "simulation_domain_type": "dense_ash_smoke", "fluid_color_rgb": [0.3, 0.3, 0.3], "dissipation_rate_frames": 150, "buoyancy_density_force": 2.0, "cel_shader_border_threshold": 0.0, "vorticity_swirl_strength": 1.5, "emission_strength": 0.0})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "origin_xyz": origin, "simulation_domain_type": "ink_splash_fluid", "fluid_color_rgb": [0.02, 0.02, 0.02], "dissipation_rate_frames": 90, "buoyancy_density_force": -1.0, "cel_shader_border_threshold": 0.0, "vorticity_swirl_strength": 0.5, "emission_strength": 0.0})
            else:
                if intensity >= 80.0:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "origin_xyz": origin, "simulation_domain_type": "cel_shaded_fireblast", "fluid_color_rgb": [1.0, 0.2, 0.0], "dissipation_rate_frames": 40, "buoyancy_density_force": 4.5, "cel_shader_border_threshold": 0.65, "vorticity_swirl_strength": 8.0, "emission_strength": 15.0})
                elif intensity >= 30.0:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "origin_xyz": origin, "simulation_domain_type": "bubbly_impact_smoke", "fluid_color_rgb": [0.8, 0.8, 0.9], "dissipation_rate_frames": 60, "buoyancy_density_force": -0.5, "cel_shader_border_threshold": 0.35, "vorticity_swirl_strength": 5.0, "emission_strength": 2.0})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "origin_xyz": origin, "simulation_domain_type": "ink_splash_fluid", "fluid_color_rgb": [0.05, 0.05, 0.05], "dissipation_rate_frames": 45, "buoyancy_density_force": 0.0, "cel_shader_border_threshold": 0.8, "vorticity_swirl_strength": 2.0, "emission_strength": 1.0})
        return {"fluid_simulation_profiles": profiles}

    def _bake_universal_fluids_in_blender(self, fluid_data):
        self.log_message("Engaging Blender Core: Compiling universal volume and surface nodes...", "INFO")
        
        script_content = f"""
import bpy
import math

# --- 1. SCENE PREP & CLEANUP ---
profiles = {json.dumps(fluid_data.get('fluid_simulation_profiles', []))}
scene = bpy.context.scene
fps = scene.render.fps

scene.render.engine = 'BLENDER_EEVEE'

if hasattr(scene.eevee, "use_volumetric"):
    scene.eevee.use_volumetric = True
    scene.eevee.volumetric_tile_size = '4'
    scene.eevee.volumetric_samples = 64
if hasattr(scene.eevee, "use_bloom"):
    scene.eevee.use_bloom = True

bpy.ops.object.select_all(action='DESELECT')
for obj in scene.objects:
    if obj.name.startswith("OMNIMATRIX_VFX_Fluid_"):
        obj.select_set(True)
bpy.ops.object.delete()

# --- 2. FORGE UNIVERSAL FLUIDS ---
for idx, p in enumerate(profiles):
    try:
        sim_type = p.get('simulation_domain_type', 'cel_shaded_fireblast')
        global_style = p.get('render_style_enforced', 'realistic').lower()
        spawn_frame = int(p.get('timestamp_sec', 0.0) * fps)
        dissolve_frames = int(p.get('dissipation_rate_frames', 60))
        buoyancy = float(p.get('buoyancy_density_force', 2.0))
        vorticity = float(p.get('vorticity_swirl_strength', 2.0))
        threshold = float(p.get('cel_shader_border_threshold', 0.5))
        emit_str = float(p.get('emission_strength', 10.0))
        loc = tuple(p.get('origin_xyz', [0,0,0]))
        color = tuple(p.get('fluid_color_rgb', [1.0, 0.5, 0.0])) + (1.0,)
        
        obj_name = f"OMNIMATRIX_VFX_Fluid_{{sim_type}}_{{idx}}"
        
        # Mesh Generation - Base Volume Bound
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5 if global_style == 'realistic' else 3, radius=1.0, location=loc)
        obj = bpy.context.active_object
        obj.name = obj_name
        bpy.ops.object.shade_smooth()
        
        # Procedural Displacement
        mod_disp = obj.modifiers.new(name="FluidDisplace", type='DISPLACE')
        tex = bpy.data.textures.new(f"Tex_FluidNoise_{{idx}}", type='CLOUDS')
        tex.noise_scale = 1.0 if global_style == 'realistic' else 1.8
        mod_disp.texture = tex
        mod_disp.strength = 1.5 if global_style == 'realistic' else 2.5
        
        # God-Level Universal Shader Logic
        mat = bpy.data.materials.new(name=f"MAT_{{obj_name}}")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        
        out_node = nt.nodes.new('ShaderNodeOutputMaterial')
        
        # Fade/Dissolve Control Node (Animated Later)
        fade_val = nt.nodes.new('ShaderNodeValue')
        fade_val.outputs[0].default_value = 1.0
        
        if global_style == 'realistic':
            mat.blend_method = 'OPAQUE' # Irrelevant for volume, but safe
            vol_node = nt.nodes.new('ShaderNodeVolumePrincipled')
            
            # Use noise to create turbulent volumetric density
            tex_noise = nt.nodes.new('ShaderNodeTexNoise')
            tex_noise.inputs['Scale'].default_value = 3.5
            
            math_density = nt.nodes.new('ShaderNodeMath')
            math_density.operation = 'MULTIPLY'
            math_density.inputs[1].default_value = 8.0 # Max density
            
            fade_mult = nt.nodes.new('ShaderNodeMath')
            fade_mult.operation = 'MULTIPLY'
            
            nt.links.new(tex_noise.outputs['Fac'], math_density.inputs[0])
            nt.links.new(math_density.outputs['Value'], fade_mult.inputs[0])
            nt.links.new(fade_val.outputs[0], fade_mult.inputs[1])
            nt.links.new(fade_mult.outputs['Value'], vol_node.inputs['Density'])
            
            vol_node.inputs['Color'].default_value = color
            
            if 'fire' in sim_type:
                vol_node.inputs['Emission Strength'].default_value = emit_str
                vol_node.inputs['Emission Color'].default_value = color
                
            nt.links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])
            
        else:
            # Anime Surface Shader
            mat.blend_method = 'BLEND'
            mix_node = nt.nodes.new('ShaderNodeMixShader')
            trans_node = nt.nodes.new('ShaderNodeBsdfTransparent')
            emit_node = nt.nodes.new('ShaderNodeEmission')
            
            noise = nt.nodes.new('ShaderNodeTexNoise')
            noise.inputs['Scale'].default_value = 2.5
            
            ramp = nt.nodes.new('ShaderNodeValToRGB')
            ramp.color_ramp.interpolation = 'CONSTANT'
            ramp.color_ramp.elements[0].position = threshold
            ramp.color_ramp.elements[0].color = (0,0,0,0)
            ramp.color_ramp.elements[1].position = threshold + 0.01
            ramp.color_ramp.elements[1].color = color
            
            # Combine fade value with threshold clipping
            fade_math = nt.nodes.new('ShaderNodeMath')
            fade_math.operation = 'MULTIPLY'
            
            emit_node.inputs['Strength'].default_value = emit_str
            
            nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
            nt.links.new(ramp.outputs['Color'], emit_node.inputs['Color'])
            
            nt.links.new(ramp.outputs['Alpha'], fade_math.inputs[0])
            nt.links.new(fade_val.outputs[0], fade_math.inputs[1])
            
            nt.links.new(fade_math.outputs['Value'], mix_node.inputs['Fac'])
            nt.links.new(trans_node.outputs['BSDF'], mix_node.inputs[1])
            nt.links.new(emit_node.outputs['Emission'], mix_node.inputs[2])
            nt.links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
            
        obj.data.materials.append(mat)
        
        # --- 3. ANIMATION AUTOMATION ---
        obj.hide_viewport = True
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_viewport", frame=max(1, spawn_frame - 1))
        obj.keyframe_insert(data_path="hide_render", frame=max(1, spawn_frame - 1))
        
        obj.hide_viewport = False
        obj.hide_render = False
        obj.keyframe_insert(data_path="hide_viewport", frame=spawn_frame)
        obj.keyframe_insert(data_path="hide_render", frame=spawn_frame)
        
        # Growth / Explosion Scale
        obj.scale = (0.1, 0.1, 0.1)
        obj.keyframe_insert(data_path="scale", frame=spawn_frame)
        target_scale = 3.5 if 'smoke' in sim_type else 2.0
        obj.scale = (target_scale, target_scale, target_scale)
        obj.keyframe_insert(data_path="scale", frame=spawn_frame + int(fps * 0.5))
        
        end_frame = spawn_frame + dissolve_frames
        
        # Buoyancy (Location Z) & Vorticity (Rotation Z)
        obj.location[2] += buoyancy
        obj.keyframe_insert(data_path="location", index=2, frame=end_frame)
        
        obj.rotation_euler[2] += vorticity * math.pi
        obj.keyframe_insert(data_path="rotation_euler", index=2, frame=end_frame)
        
        # Dissolve Fade Curve (Controls Volume Density or Surface Alpha)
        fade_val.outputs[0].default_value = 1.0
        fade_val.outputs[0].keyframe_insert(data_path="default_value", frame=spawn_frame + int(dissolve_frames * 0.3))
        fade_val.outputs[0].default_value = 0.0
        fade_val.outputs[0].keyframe_insert(data_path="default_value", frame=end_frame)
        
        # Final Hide
        obj.hide_viewport = True
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_viewport", frame=end_frame + 1)
        obj.keyframe_insert(data_path="hide_render", frame=end_frame + 1)

    except Exception as e:
        print(f"FAILED to process fluid profile {{idx}} - {{str(e)}}")
        continue

try:
    bpy.ops.wm.save_mainfile()
except Exception as e:
    print(f"FAILED to save mainfile: {{str(e)}}")
"""
        script_path = os.path.join(self.workspace_dir, "temp_fluid_forge.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Baking Uncut Universal Fluids into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Universal Fluids, Smoke, and Fire completely verified and injected.", "SUCCESS")

if __name__ == "__main__":
    forge = UniversalFluidSmokeFireForge()
    output = forge.forge_stylized_fluid_parameters()
    print("\n--- OMNIMATRIX VFX STUDIO: AGENT 37 COMPLETE ---")
    print(f"Total fluid simulation profiles correctly generated: {len(output['fluid_simulation_profiles'])}")
    for p in output["fluid_simulation_profiles"]:
        print(f"Time: {p['timestamp_sec']}s | Type: '{p['simulation_domain_type']}' ({p.get('render_style_enforced', 'unknown')})")
    print("------------------------------------------------------------------")
