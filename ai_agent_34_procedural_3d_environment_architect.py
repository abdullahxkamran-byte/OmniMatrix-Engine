# ==============================================================================
# ai_agent_34_procedural_3d_environment_architect.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL TERRAIN & PROP SCATTERING)
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

class AiAgent34Procedural3DEnvironmentArchitect:
    def __init__(self):
        # RULE 8: STRICT AI NAMING (Fixed to match Roster)
        self.agent_name = "ai_agent_34_procedural_3d_environment_architect"
        
        # RULE 2: UNIVERSAL PATH ISOLATION (No Hardcoded Drives)
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        # FIXED: Brought back to Module C
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "34_procedural_env_blueprint.json")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_dir, "global_config.json")
        
        # RULE 6: DUAL API FAILSAFES
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        for d in [self.script_dir, self.env_dir, self.module_c_dir]:
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
        """Loads story/mood data from Master Matrix State"""
        context = {
            "mood": "EPIC",
            "visual_description": "Desolate battleground",
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
            "procedural_prop_count": 30,
            "ground_subdivision_level": 3 if is_anime else 5, # Realism needs more terrain detail
            "displacement_strength": 0.5 if is_anime else 1.5,
            "emission_strength": 5.0 if is_anime else 0.0
        }

    # PURE ENVIRONMENT AI BRAIN (No Lighting overlap)
    def _query_architect_brain(self, scene_name, context, style):
        self.log(f"Calculating Procedural Geometry & Layout for '{scene_name}'...", "INFO")

        ai_prompt = f"""
        You are the Master Procedural 3D Environment Architect for the OmniMatrix Engine.
        Scene Description: "{context['visual_description']}"
        Mood: {context['mood']}
        Visual Style: {style.upper()}
        
        MISSION:
        Design the procedural terrain layout and prop scattering logic ONLY. (Lighting is handled by Agent 22).
        
        STYLE RULES (Rule 13):
        - If ANIME: Use stylized/smooth terrain (lower displacement), 'neo_tokyo_cyberpunk' or 'grassy_shonen_plains'. Higher emission strength.
        - If REALISTIC: Use rough, highly displaced terrain (higher subdivision), 'apocalyptic_ruins'. Emission is 0.
        
        Return EXACTLY 1 JSON object:
        {{
            "environment_preset": "neo_tokyo_cyberpunk" or "grassy_shonen_plains" or "apocalyptic_ruins",
            "procedural_prop_count": integer (max 60 for RAM safety),
            "ground_subdivision_level": integer (2 to 6),
            "displacement_strength": float (0.1 to 2.0),
            "emission_strength": float (0.0 to 10.0)
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

    # GOD-LEVEL BLENDER SCRIPT: TERRAIN, DISPLACEMENT & INSTANCING
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
    # Scrub old terrains and props to prevent overlapping
    for obj in bpy.data.objects:
        if any(prefix in obj.name for prefix in ["OMNI_Ground", "OMNI_Prop"]):
            bpy.data.objects.remove(obj, do_unlink=True)
            
    for mat in bpy.data.materials:
        if "OMNI_Ground" in mat.name: bpy.data.materials.remove(mat, do_unlink=True)

    # 2. PROCEDURAL TERRAIN GENERATION (Core Function)
    subdiv = {layout_data.get('ground_subdivision_level', 4)}
    bpy.ops.mesh.primitive_grid_add(size=40.0, x_subdivisions=2**subdiv, y_subdivisions=2**subdiv, location=(0,0,0))
    ground = bpy.context.active_object
    ground.name = "OMNI_Ground_Mesh"
    
    sub_mod = ground.modifiers.new(name="Subsurf", type='SUBSURF')
    sub_mod.levels = 2
    
    # 3. PROCEDURAL DISPLACEMENT (Terrain Roughness)
    disp_mod = ground.modifiers.new(name="Displace", type='DISPLACE')
    tex = bpy.data.textures.new("OMNI_Ground_Noise", type='CLOUDS')
    tex.noise_scale = 1.5 if {is_anime} else 0.8 # Realism has finer noise details
    disp_mod.texture = tex
    disp_mod.strength = {layout_data.get('displacement_strength', 1.0)}

    # 4. TERRAIN SHADER NETWORK
    ground_mat = bpy.data.materials.new(name="OMNI_Ground_Mat")
    ground_mat.use_nodes = True
    gnodes = ground_mat.node_tree.nodes
    bsdf = gnodes.get("Principled BSDF")
    
    if "cyberpunk" in "{preset}":
        bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1) # Dark asphalt
        bsdf.inputs['Emission Strength'].default_value = {layout_data.get('emission_strength', 5.0)}
        bsdf.inputs['Emission Color'].default_value = (0.0, 0.8, 1.0, 1) # Cyan grid lines glow
    elif "plains" in "{preset}":
        bsdf.inputs['Base Color'].default_value = (0.1, 0.5, 0.1, 1) # Grass tone
    else: 
        bsdf.inputs['Base Color'].default_value = (0.2, 0.18, 0.15, 1) # Dirt/Ruins tone
        bsdf.inputs['Roughness'].default_value = 0.9
        
    ground.data.materials.append(ground_mat)

    # 5. INSTANCE SCATTERING (Debris/Cyber-Pillars)
    random.seed(42) # Consistent scatter seed
    prop_count = {layout_data.get('procedural_prop_count', 30)}
    for i in range(prop_count):
        x, y = random.uniform(-15.0, 15.0), random.uniform(-15.0, 15.0)
        
        # Determine prop type based on preset
        if "cyberpunk" in "{preset}":
            bpy.ops.mesh.primitive_cylinder_add(radius=random.uniform(0.2, 0.6), depth=random.uniform(3.0, 8.0), location=(x, y, 2.5))
            bpy.context.active_object.data.materials.append(ground_mat) 
        elif "plains" in "{preset}":
            # Simple rocks
            bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(0.5, 1.5), subdivisions=1, location=(x, y, 0))
        else:
            # Jagged Ruins debris
            bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(0.5, 2.0), subdivisions=2, location=(x, y, 0))
            # Distort debris to look like broken concrete
            bpy.ops.transform.resize(value=(1.0, random.uniform(0.5, 1.5), random.uniform(0.2, 0.8)))
            
        prop = bpy.context.active_object
        prop.name = f"OMNI_Prop_Scatter_{{i}}"
        prop.rotation_euler = (random.uniform(0, 0.5), random.uniform(0, 0.5), random.uniform(0, 6.28))

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_TERRAIN_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_environment_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 34 (Procedural 3D Environment Architect)...", "INFO")

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
                
                self.log(f"--- Sculpting Procedural Terrain for: {scene_name} | Style: {global_style.upper()} ---", "INFO")
                
                layout_data = self._query_architect_brain(scene_name, context, global_style)
                
                self.log(f"AI Terrain Core -> Theme: {layout_data.get('environment_preset')} | Prop Density: {layout_data.get('procedural_prop_count')} | Subdivisions: {layout_data.get('ground_subdivision_level')}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, layout_data, global_style)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_TERRAIN_SUCCESS" in result.stdout:
                        self.log(f"God-Level Environment Geometry baked into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = layout_data
                    else:
                        self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: STATE UPDATE (Handoff to Module D: VFX Forge)
        state["last_active_agent"] = self.agent_name
        # FIXED: Exact name from the Master List for Agent 35!
        state["next_agent"] = "ai_agent_35_autonomous_vfx_procedural_forge" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Module C 100% COMPLETE. Handoff to Module D ({state['next_agent']}).", "SUCCESS")

if __name__ == "__main__":
    architect = AiAgent34Procedural3DEnvironmentArchitect()
    architect.execute_pipeline()
