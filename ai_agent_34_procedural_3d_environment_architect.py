# ==============================================================================
# Ai_Agent_34_Cinematic_Environment_Architect.py
# MODULE D: Atmosphere & Cinematography - (GOD-LEVEL TERRAIN & VOLUMETRICS)
# ==============================================================================

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
                    # RULE 6: UNIVERSAL UPPERCASE API KEYS
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiAgent34CinematicEnvironmentArchitect:
    def __init__(self):
        # RULE 8: STRICT AI NAMING
        self.agent_name = "Ai_Agent_34_Cinematic_Environment_Architect"
        
        # RULE 2: UNIVERSAL PATH ISOLATION (No Hardcoded Drives)
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_d_dir = os.path.join(self.workspace_dir, "Module_D_Atmosphere")
        
        self.output_blueprint = os.path.join(self.module_d_dir, "34_environment_lighting_blueprint.json")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_dir, "global_config.json")
        
        # RULE 6: DUAL API FAILSAFES
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        for d in [self.script_dir, self.env_dir, self.module_d_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_master_config(self):
        default_config = {"global_style": "anime", "blender_executable": "blender"}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except: pass
        return default_config

    def _load_upstream_context(self):
        """Loads story/mood data from Master Matrix State (Rule 7)"""
        context = {
            "mood": "EPIC",
            "visual_description": "Desolate battleground",
            "start_frame": 1
        }
        
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "emotion" in data:
                        context["mood"] = data["emotion"]
                    if "scene_description" in data:
                        context["visual_description"] = data["scene_description"]
            except: pass
                
        return context

    def _clean_json_response(self, raw_text):
        try:
            cleaned = re.sub(r'```(?:json)?\n(.*?)```', r'\1', raw_text, flags=re.DOTALL).strip()
            return json.loads(cleaned)
        except:
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            if start != -1 and end != -1:
                try: return json.loads(raw_text[start:end+1])
                except: pass
            return None

    def _fallback_architect(self, style):
        is_anime = "anime" in style.lower()
        return {
            "environment_preset": "neo_tokyo_cyberpunk" if is_anime else "apocalyptic_ruins",
            "sun_intensity_lux": 15.0 if is_anime else 3.5,
            "sun_color": [1.0, 0.9, 0.8] if is_anime else [0.6, 0.7, 0.9], # Warm vs Cold
            "volumetric_fog_density": 0.02 if is_anime else 0.15, # Realism has heavy fog
            "procedural_prop_count": 30,
            "ground_subdivision_level": 4,
            "emission_strength": 5.0 if is_anime else 0.5
        }

    # LIMITLESS ARCHITECT & LIGHTING AI
    def _query_architect_brain(self, scene_name, context, style):
        self.log(f"Calculating World Geometry & Cinematography for '{scene_name}'...", "INFO")

        ai_prompt = f"""
        You are the Master Procedural Environment & Lighting Architect for the OmniMatrix Engine.
        Scene Description: "{context['visual_description']}"
        Mood: {context['mood']}
        Visual Style: {style.upper()}
        
        MISSION:
        Design the procedural environment layout AND volumetric lighting settings.
        
        STYLE RULES (Rule 13):
        - If ANIME: Use high `sun_intensity_lux` (vibrant colors), low `volumetric_fog_density` (clear skies), and high `emission_strength` for glowing cyberpunk elements or bright grass.
        - If REALISTIC: Use lower `sun_intensity_lux`, higher `volumetric_fog_density` (moody atmosphere), and realistic `sun_color` (RGB format).
        
        Return EXACTLY 1 JSON object:
        {{
            "environment_preset": "neo_tokyo_cyberpunk" or "grassy_shonen_plains" or "apocalyptic_ruins",
            "sun_intensity_lux": float,
            "sun_color": [R, G, B] (floats 0.0 to 1.0),
            "volumetric_fog_density": float,
            "procedural_prop_count": integer (max 50),
            "ground_subdivision_level": integer (3 to 6),
            "emission_strength": float
        }}
        """

        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self._clean_json_response(res_text)
                    if parsed and "environment_preset" in parsed:
                        return parsed
            except: pass

        return self._fallback_architect(style)

    # GOD-LEVEL BLENDER SCRIPT: NODES, VOLUMETRICS, TERRAIN
    def _generate_blender_script(self, blend_file_path, layout_data, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        preset = layout_data.get('environment_preset', 'apocalyptic_ruins')
        is_anime = "True" if "anime" in style.lower() else "False"
        
        script_content = f"""
import bpy
import random

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    # 1. IDEMPOTENCY: STRICT GARBAGE COLLECTION (Rule 5)
    # Scrub old terrains, props, lights, and volumetrics
    for obj in bpy.data.objects:
        if any(prefix in obj.name for prefix in ["OMNI_Ground", "OMNI_Prop", "OMNI_Sun", "OMNI_Volume"]):
            bpy.data.objects.remove(obj, do_unlink=True)
            
    # Scrub unused textures and materials to free VRAM
    for mat in bpy.data.materials:
        if "OMNI_" in mat.name: bpy.data.materials.remove(mat, do_unlink=True)
    for tex in bpy.data.textures:
        if "OMNI_" in tex.name: bpy.data.textures.remove(tex, do_unlink=True)

    # 2. DYNAMIC SUN & LIGHTING
    sun_data = bpy.data.lights.new(name="OMNI_Sun_Light", type='SUN')
    sun_data.energy = {layout_data.get('sun_intensity_lux', 10.0)}
    sun_data.color = {layout_data.get('sun_color', [1.0, 1.0, 1.0])}
    
    sun_obj = bpy.data.objects.new(name="OMNI_Sun", object_data=sun_data)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (0.785, 0.0, 0.5) # Angled sunset/sunrise lighting

    # 3. ATMOSPHERE: VOLUMETRIC FOG (God Rays Setup)
    bpy.ops.mesh.primitive_cube_add(size=100.0, location=(0,0,10))
    vol_cube = bpy.context.active_object
    vol_cube.name = "OMNI_Volume_Domain"
    vol_cube.display_type = 'WIRE' # Don't block viewport
    
    vol_mat = bpy.data.materials.new(name="OMNI_Volumetric_Mat")
    vol_mat.use_nodes = True
    nodes = vol_mat.node_tree.nodes
    links = vol_mat.node_tree.links
    
    nodes.clear() # Clear default principled bsdf
    vol_node = nodes.new(type='ShaderNodeVolumePrincipled')
    vol_node.inputs['Density'].default_value = {layout_data.get('volumetric_fog_density', 0.1)}
    vol_node.inputs['Anisotropy'].default_value = 0.8 if {is_anime} else 0.4 # Anime has sharp god rays
    
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])
    vol_cube.data.materials.append(vol_mat)

    # 4. PROCEDURAL TERRAIN GENERATION
    subdiv = {layout_data.get('ground_subdivision_level', 3)}
    bpy.ops.mesh.primitive_grid_add(size=40.0, x_subdivisions=2**subdiv, y_subdivisions=2**subdiv, location=(0,0,0))
    ground = bpy.context.active_object
    ground.name = "OMNI_Ground_Mesh"
    
    sub_mod = ground.modifiers.new(name="Subsurf", type='SUBSURF')
    sub_mod.levels = 2
    
    disp_mod = ground.modifiers.new(name="Displace", type='DISPLACE')
    tex = bpy.data.textures.new("OMNI_Ground_Noise", type='CLOUDS')
    tex.noise_scale = 2.0 if {is_anime} else 1.0
    disp_mod.texture = tex
    disp_mod.strength = 1.2 if not "plains" in "{preset}" else 0.4

    # 5. PROCEDURAL SHADER NODE NETWORK (The Magic)
    ground_mat = bpy.data.materials.new(name="OMNI_Ground_Mat")
    ground_mat.use_nodes = True
    gnodes = ground_mat.node_tree.nodes
    bsdf = gnodes.get("Principled BSDF")
    
    if "cyberpunk" in "{preset}":
        # Create glowing neon grid lines
        bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1) # Dark asphalt
        bsdf.inputs['Emission Strength'].default_value = {layout_data.get('emission_strength', 5.0)}
        bsdf.inputs['Emission Color'].default_value = (0.0, 0.8, 1.0, 1) # Cyan glow
    elif "plains" in "{preset}":
        bsdf.inputs['Base Color'].default_value = (0.1, 0.5, 0.1, 1) if {is_anime} else (0.05, 0.2, 0.05, 1)
        bsdf.inputs['Roughness'].default_value = 0.9
    else: # Ruins
        bsdf.inputs['Base Color'].default_value = (0.2, 0.18, 0.15, 1)
        
    ground.data.materials.append(ground_mat)

    # 6. INSTANCE SCATTERING (Debris/Pillars)
    random.seed(42)
    prop_count = {layout_data.get('procedural_prop_count', 30)}
    for i in range(prop_count):
        x, y = random.uniform(-15.0, 15.0), random.uniform(-15.0, 15.0)
        if "cyberpunk" in "{preset}":
            bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=random.uniform(5.0, 10.0), location=(x, y, 2.5))
            bpy.context.active_object.data.materials.append(ground_mat) # Share neon material
        else:
            bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(0.5, 2.0), subdivisions=2, location=(x, y, random.uniform(0, 1)))
        
        prop = bpy.context.active_object
        prop.name = f"OMNI_Prop_Scatter_{{i}}"
        prop.rotation_euler = (random.uniform(0, 0.5), random.uniform(0, 0.5), random.uniform(0, 6.28))

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_ARCHITECT_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_d_dir, "temp_environment_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 34 (Cinematic Environment & Atmosphere)...", "INFO")

        # RULE 7: ATOMIC HANDSHAKE
        state = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
            except: pass

        if state.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{state.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        config = self._load_master_config()
        global_style = config.get("global_style", "anime").lower()
        blender_executable = config.get("blender_executable", "blender")
        master_blueprint = {}
        
        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("No 3D environments found. Exiting...", "WARNING")
            sys.exit(0)
            
        context = self._load_upstream_context()
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                scene_name = filename.replace("_stage.blend", "").replace(".blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                self.log(f"--- Sculpting Terrain & Atmosphere for: {scene_name} | Style: {global_style.upper()} ---", "INFO")
                
                layout_data = self._query_architect_brain(scene_name, context, global_style)
                
                self.log(f"AI Matrix -> Theme: {layout_data.get('environment_preset')} | Fog Density: {layout_data.get('volumetric_fog_density')} | Sun: {layout_data.get('sun_intensity_lux')} Lux", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, layout_data, global_style)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_ARCHITECT_SUCCESS" in result.stdout:
                        self.log(f"God-Level Environment & Volumetrics baked into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = layout_data
                    else:
                        self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: STATE UPDATE (Handoff to Camera Cinematography)
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "Ai_Agent_35_Camera_Cinematography_Director" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Module D (Atmosphere) Setup Complete. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    architect = AiAgent34CinematicEnvironmentArchitect()
    architect.execute_pipeline()
