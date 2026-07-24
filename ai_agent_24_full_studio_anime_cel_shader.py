# ==============================================================================
# Ai_Agent_24_AAA_Anime_Cel_Shader_Battle_Damage.py
# MODULE C: Blender 3D Heavy Infantry
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
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiAgent24AAAAnimeCelShader:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_24_AAA_Anime_Cel_Shader"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "24_cel_shader_blueprint.json")
        
        # System States (RULE 7)
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_dir, "global_config.json")
        
        # APIs (RULE 6)
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

    def _load_upstream_vibe(self, scene_name):
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {"vibe_genre": "Action", "action": "Combat", "intensity": "high"}
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["vibe_genre"] = data.get("genre_vibe", "Action")
                    context["action"] = data.get("action_description", "")
                    # Auto-detect battle damage need
                    desc = context["action"].lower()
                    context["intensity"] = "high" if any(w in desc for w in ["hit", "slash", "blood", "damage", "fight", "punch"]) else "low"
            except: pass
        return context

    # RULE 5: BULLETPROOF JSON
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

    # RULE 10: PROCEDURAL FALLBACK
    def _get_procedural_fallback_shader(self, context):
        is_damaged = context.get("intensity") == "high"
        return {
            "outline_thickness_pixels": 3.0 if is_damaged else 2.0,
            "outline_color_hex": "#050505",
            "shadow_sharpness_stop": 0.45,
            "battle_damage_level": 0.7 if is_damaged else 0.0,
            "damage_color_hex": "#7A0000",
            "style_rationale": "Offline procedural fallback logic."
        }

    # RULE 6: QUAD-CORE FALLBACK
    def _query_ai_shader_brain(self, scene_name, context):
        self.log(f"Consulting AAA Render TD for '{scene_name}'...", "INFO")
        
        ai_prompt = f"""
        You are the Lead Anime Render TD. Style is STRICTLY Anime/Cel-Shaded.
        Scene: '{scene_name}' | Vibe: {context['vibe_genre']} | Action: {context['action']}
        
        Design the Cel-Shading vectors. 
        If action/intensity is HIGH (combat, hits), increase 'battle_damage_level' (0.0 to 1.0) and make outlines thicker.
        
        Return ONLY valid JSON:
        {{
            "outline_thickness_pixels": float (1.5 to 5.0),
            "outline_color_hex": "#HEXCOLOR",
            "shadow_sharpness_stop": float (0.3 to 0.6, usually 0.45 for crisp anime shadows),
            "battle_damage_level": float (0.0 for clean, 1.0 for heavily wounded),
            "damage_color_hex": "#HEXCOLOR",
            "style_rationale": "Brief reason"
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
                    if parsed: return parsed
            except: pass

        if self.openai_api_key:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
                payload = {"model": "gpt-4o", "messages": [{"role": "user", "content": ai_prompt}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
                    parsed = self._clean_json_response(res_text)
                    if parsed: return parsed
            except: pass

        self.log("AI APIs unavailable. Using Procedural Shader Matrix.", "WARNING")
        return self._get_procedural_fallback_shader(context)

    # RULE 3, RULE 11, RULE 13 APPLIED
    def _generate_blender_script(self, blend_file_path, shader_data):
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return (0, 0, 0, 1)
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    # Force EEVEE for Cel-Shading
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    try:
        bpy.context.scene.eevee.shadow_cascade_size = '2048'
    except: pass # Failsafe for Blender 4.2+

    sharpness = {shader_data.get('shadow_sharpness_stop', 0.45)}
    line_thick = {shader_data.get('outline_thickness_pixels', 2.0)} * 0.001
    damage_lvl = {shader_data.get('battle_damage_level', 0.0)}
    damage_color = hex_to_rgb("{shader_data.get('damage_color_hex', '#8B0000')}")

    # RULE 13: DYNAMIC MESH TARGETING (Find all characters dynamically)
    char_objects = []
    for obj in bpy.context.scene.objects:
        # Check if it's placed by Agent 23 OR parented to a CHAR_SOCKET
        if obj.type == 'MESH':
            if obj.name.startswith("OMNI_CHAR") or obj.name.startswith("CH_"):
                char_objects.append(obj)
            else:
                parent = obj.parent
                while parent:
                    if "CHAR_SOCKET" in parent.name:
                        char_objects.append(obj)
                        break
                    parent = parent.parent
                    
    # Remove duplicates
    char_objects = list(set(char_objects))

    if not char_objects:
        print("WARNING: No character meshes detected for cel-shading.")
        
    # LIMITLESS MATERIAL SCRUBBING & REBUILDING
    for obj in char_objects:
        # A. INVERTED HULL OUTLINE MODIFIER
        has_outline = False
        for mod in obj.modifiers:
            if mod.name == "OMNIMATRIX_Anime_Outline":
                has_outline = True
                mod.thickness = -line_thick
                break
                
        if not has_outline:
            mod = obj.modifiers.new(name="OMNIMATRIX_Anime_Outline", type='SOLIDIFY')
            mod.use_flip_normals = True
            mod.thickness = -line_thick
            mod.material_offset = 100 
            
            outline_mat = bpy.data.materials.get("MAT_OMNI_Outline")
            if not outline_mat:
                outline_mat = bpy.data.materials.new(name="MAT_OMNI_Outline")
                outline_mat.use_nodes = True
                outline_mat.use_backface_culling = True 
                
                nt_out = outline_mat.node_tree
                nt_out.nodes.clear()
                emit = nt_out.nodes.new('ShaderNodeEmission')
                emit.inputs['Color'].default_value = hex_to_rgb("{shader_data.get('outline_color_hex', '#000000')}")
                out = nt_out.nodes.new('ShaderNodeOutputMaterial')
                nt_out.links.new(emit.outputs['Emission'], out.inputs['Surface'])
                
            if outline_mat.name not in [m.name for m in obj.data.materials if m]:
                obj.data.materials.append(outline_mat)

        # B. DYNAMIC CEL SHADER REPLACEMENT
        for mat_slot in obj.material_slots:
            mat = mat_slot.material
            if mat and not mat.name.startswith("MAT_OMNI_Outline") and mat.use_nodes:
                nt = mat.node_tree
                
                if nt.nodes.get("OMNI_Cel_Ramp"):
                    continue # Already processed
                    
                base_color_node = None
                for node in nt.nodes:
                    if node.type == 'TEX_IMAGE':
                        base_color_node = node
                        break
                
                # Nuke existing complex PBR nodes
                for node in nt.nodes:
                    if node.type not in ['TEX_IMAGE', 'OUTPUT_MATERIAL']:
                        nt.nodes.remove(node)
                        
                out_node = nt.nodes.get("Material Output")
                if not out_node:
                    out_node = nt.nodes.new('ShaderNodeOutputMaterial')
                
                diffuse = nt.nodes.new('ShaderNodeBsdfDiffuse')
                if base_color_node:
                    nt.links.new(base_color_node.outputs['Color'], diffuse.inputs['Color'])
                else:
                    diffuse.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1)

                # The Eevee Cel Shading Core
                s2rgb = nt.nodes.new('ShaderNodeShaderToRGB')
                nt.links.new(diffuse.outputs['BSDF'], s2rgb.inputs['Shader'])
                
                ramp = nt.nodes.new('ShaderNodeValToRGB')
                ramp.name = "OMNI_Cel_Ramp"
                ramp.color_ramp.interpolation = 'CONSTANT'
                ramp.color_ramp.elements[0].position = sharpness - 0.05
                ramp.color_ramp.elements[0].color = (0.3, 0.3, 0.4, 1.0) # Shadow tint
                ramp.color_ramp.elements[1].position = sharpness
                ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
                
                nt.links.new(s2rgb.outputs['Color'], ramp.inputs['Fac'])
                
                multiply = nt.nodes.new('ShaderNodeMixRGB')
                multiply.blend_type = 'MULTIPLY'
                multiply.inputs['Fac'].default_value = 1.0
                nt.links.new(ramp.outputs['Color'], multiply.inputs[1])
                
                if base_color_node:
                    nt.links.new(base_color_node.outputs['Color'], multiply.inputs[2])
                else:
                    multiply.inputs[2].default_value = (0.8, 0.8, 0.8, 1)

                # LIMITLESS BATTLE DAMAGE (Voronoi Slashes + Noise Blood)
                if damage_lvl > 0.0:
                    blood_mix = nt.nodes.new('ShaderNodeMixRGB')
                    blood_mix.inputs[2].default_value = damage_color
                    
                    # Voronoi for Sword Slashes
                    voronoi = nt.nodes.new('ShaderNodeTexVoronoi')
                    voronoi.feature = 'DISTANCE_TO_EDGE'
                    voronoi.inputs['Scale'].default_value = 15.0
                    
                    # Noise for Splatters
                    noise = nt.nodes.new('ShaderNodeTexNoise')
                    noise.inputs['Scale'].default_value = 50.0
                    
                    dmg_math = nt.nodes.new('ShaderNodeMath')
                    dmg_math.operation = 'MULTIPLY'
                    nt.links.new(voronoi.outputs['Distance'], dmg_math.inputs[0])
                    nt.links.new(noise.outputs['Fac'], dmg_math.inputs[1])
                    
                    dmg_ramp = nt.nodes.new('ShaderNodeValToRGB')
                    dmg_ramp.color_ramp.interpolation = 'CONSTANT'
                    dmg_ramp.color_ramp.elements[0].position = 1.0 - (damage_lvl * 0.4)
                    dmg_ramp.color_ramp.elements[1].position = 1.0 - (damage_lvl * 0.3)
                    nt.links.new(dmg_math.outputs['Value'], dmg_ramp.inputs['Fac'])
                    
                    nt.links.new(multiply.outputs['Color'], blood_mix.inputs[1])
                    nt.links.new(dmg_ramp.outputs['Color'], blood_mix.inputs['Fac'])
                    nt.links.new(blood_mix.outputs['Color'], out_node.inputs['Surface'])
                else:
                    nt.links.new(multiply.outputs['Color'], out_node.inputs['Surface'])

                mat.blend_method = 'OPAQUE'
                mat.shadow_method = 'NONE'

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_celshader_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 24 (Anime Cel Shader)...", "INFO")

        # RULE 7: ATOMIC HANDSHAKE & SLEEP/WAKE ROUTER (LIMITLESS TOGGLE)
        state = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
            except: pass

        config = self._load_master_config()
        global_style = config.get("global_style", "anime").lower()

        # ==========================================
        # THE MUTUALLY EXCLUSIVE SLEEP ROUTER
        # ==========================================
        if global_style == "realistic":
            self.log("Style is REALISTIC. Agent 24 is going to SLEEP (Bypassed).", "WARNING")
            state["last_active_agent"] = self.agent_name
            state["next_agent"] = "Ai_Agent_25_Realistic_PBR_Shader_Baker"
            with open(self.state_file, "w") as f:
                json.dump(state, f, indent=4)
            self.log(f"Control handed over directly to {state['next_agent']}.", "SUCCESS")
            return # EXIT EXECUTION (SLEEP)
        else:
            self.log("Style is ANIME. Agent 24 is ACTIVE. Agent 25 will be put to SLEEP.", "INFO")
            state["next_agent"] = "Ai_Agent_26_Kinetic_Animation_Retargeter" # Skips 25!
        
        # --- CORE EXECUTION IF WAKE ---
        blender_executable = config.get("blender_executable", "blender")
        master_blueprint = {}
        
        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("No 3D environments found. Exiting...", "WARNING")
            sys.exit(0)
            
        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                scene_name = filename.replace("_stage.blend", "").replace(".blend", "")
                blend_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_vibe(scene_name)
                shader_data = self._query_ai_shader_brain(scene_name, context)
                
                script_path = self._generate_blender_script(blend_path, shader_data)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                        self.log(f"Damage Lvl [{shader_data.get('battle_damage_level')}] Cel-Shade applied to {filename}", "SUCCESS")
                        master_blueprint[scene_name] = shader_data
                    else:
                        self.log(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        state["last_active_agent"] = self.agent_name
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Anime Cel-Shader Pipeline Complete! Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    shader_dop = AiAgent24AAAAnimeCelShader()
    shader_dop.execute_pipeline()

# ==============================================================================
# END OF FILE
# ==============================================================================
