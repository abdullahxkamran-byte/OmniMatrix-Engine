# ==============================================================================
# Ai_Agent_25_AAA_Realistic_PBR_Shader_Grime_Maker.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL V2.1)
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
                    # Force environment variables to UPPERCASE taake masla hi khatam ho!
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiAgent25AAARealisticPBRShader:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_25_AAA_Realistic_PBR_Shader"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "25_pbr_shader_blueprint.json")
        
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
        default_config = {"global_style": "realistic", "blender_executable": "blender"}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except: pass
        return default_config

    def _load_upstream_vibe(self, scene_name):
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {"vibe_genre": "Cinematic", "action": "Idle", "intensity": "low"}
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["vibe_genre"] = data.get("genre_vibe", "Cinematic")
                    context["action"] = data.get("action_description", "")
                    desc = context["action"].lower()
                    context["intensity"] = "high" if any(w in desc for w in ["fight", "hit", "blood", "damage", "war", "grime"]) else "low"
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
            "base_color_hex": "#333333",
            "metallic_value": 0.3,
            "roughness_value": 0.4,
            "emission_color_hex": "#000000",
            "emission_strength": 0.0,
            "grime_damage_level": 0.8 if is_damaged else 0.1,
            "grime_color_hex": "#3A0B0B" if is_damaged else "#2A2A2A",
            "style_rationale": "Offline procedural logic based on action intensity."
        }

    # RULE 6: QUAD-CORE FALLBACK
    def _query_pbr_ai_brain(self, scene_name, context):
        self.log(f"Consulting AAA PBR TD for '{scene_name}'...", "INFO")
        
        ai_prompt = f"""
        You are the Lead Texture & PBR Shader Artist for a hyper-realistic cinematic engine.
        Scene: '{scene_name}' | Vibe: {context['vibe_genre']} | Action: {context['action']}
        
        Design the physical PBR vectors.
        If the scene has HIGH action or combat, increase 'grime_damage_level' (0.0 to 1.0) and use a dark red/brown for 'grime_color_hex' to simulate blood and mud.
        If it's sci-fi/cyberpunk, you can add subtle emission.
        
        Return ONLY valid JSON:
        {{
            "base_color_hex": "#HEXCOLOR",
            "metallic_value": float (0.0 to 1.0),
            "roughness_value": float (0.1 for shiny, 0.9 for matte),
            "emission_color_hex": "#HEXCOLOR",
            "emission_strength": float,
            "grime_damage_level": float (0.0 to 1.0),
            "grime_color_hex": "#HEXCOLOR",
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

        self.log("AI APIs unavailable. Using Procedural PBR Matrix.", "WARNING")
        return self._get_procedural_fallback_shader(context)

    # RULE 11 (Procedural Shader), RULE 13 (Dynamic Target Mesh)
    def _generate_blender_script(self, blend_file_path, shader_data):
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return (0.5, 0.5, 0.5, 1)
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    # --- 1. ENABLE HYPER-REALISTIC ENGINE FEATURES ---
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    try:
        bpy.context.scene.eevee.use_ssr = True 
        bpy.context.scene.eevee.use_ssr_refraction = True
        bpy.context.scene.eevee.use_gtao = True 
        bpy.context.scene.eevee.gtao_distance = 1.0
        bpy.context.scene.eevee.shadow_cascade_size = '4096' # AAA Shadows
    except: pass # Failsafe for Blender 4.2+ Eevee Next

    # Data Vectors
    color = hex_to_rgb("{shader_data.get('base_color_hex', '#555555')}")
    metallic = {shader_data.get('metallic_value', 0.0)}
    roughness = {shader_data.get('roughness_value', 0.5)}
    emission_color = hex_to_rgb("{shader_data.get('emission_color_hex', '#000000')}")
    emission_strength = {shader_data.get('emission_strength', 0.0)}
    grime_lvl = {shader_data.get('grime_damage_level', 0.0)}
    grime_color = hex_to_rgb("{shader_data.get('grime_color_hex', '#3B1F1F')}")

    # RULE 13: DYNAMIC MESH TARGETING (Same logic as Agent 24)
    char_objects = []
    for obj in bpy.context.scene.objects:
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
    
    char_objects = list(set(char_objects))

    if not char_objects:
        print("WARNING: No character meshes found. Check Agent 23 output.")
        
    for obj in char_objects:
        for mat_slot in obj.material_slots:
            mat = mat_slot.material
            if mat and mat.use_nodes:
                nt = mat.node_tree
                
                bsdf_node = None
                for node in nt.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        bsdf_node = node
                        break
                
                # If no Principled BSDF, build one!
                if not bsdf_node:
                    nt.nodes.clear()
                    bsdf_node = nt.nodes.new('ShaderNodeBsdfPrincipled')
                    out_node = nt.nodes.new('ShaderNodeOutputMaterial')
                    nt.links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

                # Preserve existing base color if linked to texture
                if not bsdf_node.inputs['Base Color'].is_linked:
                    bsdf_node.inputs['Base Color'].default_value = color
                
                bsdf_node.inputs['Metallic'].default_value = metallic
                
                if emission_strength > 0:
                    bsdf_node.inputs['Emission'].default_value = emission_color
                    bsdf_node.inputs['Emission Strength'].default_value = emission_strength

                # --- LIMITLESS: WET GRIME & BLOOD PHYSICS ---
                if grime_lvl > 0.0:
                    # Procedural Noise for Splatters
                    noise = nt.nodes.new('ShaderNodeTexNoise')
                    noise.inputs['Scale'].default_value = 12.0 
                    noise.inputs['Detail'].default_value = 15.0
                    noise.inputs['Roughness'].default_value = 0.6
                    
                    ramp = nt.nodes.new('ShaderNodeValToRGB')
                    ramp.color_ramp.elements[0].position = 1.0 - (grime_lvl * 0.9)
                    ramp.color_ramp.elements[1].position = 1.0
                    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
                    
                    # Blend Grime Color with Base Color
                    mix_color = nt.nodes.new('ShaderNodeMixRGB')
                    mix_color.inputs[2].default_value = grime_color
                    
                    if bsdf_node.inputs['Base Color'].is_linked:
                        prev_color_socket = bsdf_node.inputs['Base Color'].links[0].from_socket
                        nt.links.new(prev_color_socket, mix_color.inputs[1])
                    else:
                        mix_color.inputs[1].default_value = bsdf_node.inputs['Base Color'].default_value
                        
                    nt.links.new(ramp.outputs['Color'], mix_color.inputs['Fac'])
                    nt.links.new(mix_color.outputs['Color'], bsdf_node.inputs['Base Color'])
                    
                    # WET ROUGHNESS: Grime/Blood makes the surface wet (low roughness)
                    mix_rough = nt.nodes.new('ShaderNodeMixRGB')
                    # Input 1 is original roughness
                    if bsdf_node.inputs['Roughness'].is_linked:
                        prev_rough_socket = bsdf_node.inputs['Roughness'].links[0].from_socket
                        nt.links.new(prev_rough_socket, mix_rough.inputs[1])
                    else:
                        mix_rough.inputs[1].default_value = (roughness, roughness, roughness, 1.0)
                        
                    mix_rough.inputs[2].default_value = (0.05, 0.05, 0.05, 1.0) # Highly reflective blood
                    nt.links.new(ramp.outputs['Color'], mix_rough.inputs['Fac'])
                    nt.links.new(mix_rough.outputs['Color'], bsdf_node.inputs['Roughness'])
                    
                    # MICRO-DISPLACEMENT BUMP (Gives blood actual thickness)
                    bump_node = nt.nodes.new('ShaderNodeBump')
                    bump_node.inputs['Strength'].default_value = 0.2
                    nt.links.new(ramp.outputs['Color'], bump_node.inputs['Height'])
                    
                    if not bsdf_node.inputs['Normal'].is_linked:
                        nt.links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])

                else:
                    if not bsdf_node.inputs['Roughness'].is_linked:
                        bsdf_node.inputs['Roughness'].default_value = roughness

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")
    
except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_pbrshader_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 25 (Realistic PBR Shader)...", "INFO")

        # RULE 7: ATOMIC HANDSHAKE & INVERTED SLEEP/WAKE ROUTER
        state = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
            except: pass

        # Validating Turn (In case orchestrator messed up)
        if state.get("next_agent") not in [self.agent_name, "Ai_Agent_25_AAA_Realistic_PBR_Shader"]:
            self.log(f"Agent out of sync. Expected {state.get('next_agent')}.", "WARNING")

        config = self._load_master_config()
        global_style = config.get("global_style", "realistic").lower()

        # ==========================================
        # THE INVERTED MUTUALLY EXCLUSIVE SLEEP ROUTER
        # ==========================================
        if "anime" in global_style or "cel" in global_style:
            self.log("Style is ANIME. Agent 25 is going to SLEEP (Bypassed).", "WARNING")
            state["last_active_agent"] = self.agent_name
            state["next_agent"] = "Ai_Agent_26_Kinetic_Animation_Retargeter"
            with open(self.state_file, "w") as f:
                json.dump(state, f, indent=4)
            self.log(f"Control handed over directly to {state['next_agent']}.", "SUCCESS")
            return # EXIT EXECUTION (SLEEP)
        else:
            self.log("Style is REALISTIC. Agent 25 is ACTIVE. (Agent 24 was slept).", "INFO")
            state["next_agent"] = "Ai_Agent_26_Kinetic_Animation_Retargeter"
        
        # --- CORE EXECUTION IF WAKE ---
        blender_executable = config.get("blender_executable", "blender")
        master_blueprint = {}
        
        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("No 3D environments found. Exiting...", "WARNING")
            sys.exit(0)
            
        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                scene_name = filename.replace("_stage.blend", "").replace(".blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_vibe(scene_name)
                shader_data = self._query_pbr_ai_brain(scene_name, context)
                
                script_path = self._generate_blender_script(blend_file_path, shader_data)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                        self.log(f"AAA PBR + Wet Grime [Level {shader_data.get('grime_damage_level')}] applied to {filename}", "SUCCESS")
                        master_blueprint[scene_name] = shader_data
                    else:
                        self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        state["last_active_agent"] = self.agent_name
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Realistic PBR Pipeline Complete! Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    shader_dop = AiAgent25AAARealisticPBRShader()
    shader_dop.execute_pipeline()

# ==============================================================================
# END OF FILE
# ==============================================================================
