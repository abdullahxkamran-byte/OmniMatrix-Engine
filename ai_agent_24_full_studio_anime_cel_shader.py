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

class FullStudioAnimeCelShader:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 24: aaa_anime_cel_shader_battle_damage"
        
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        self.output_blueprint = os.path.join(self.workspace_dir, "24_cel_shader_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.workspace_dir, self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_vibe(self, scene_name):
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {"vibe_genre": "Action", "action_description": "Combat scene"}
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["vibe_genre"] = data.get("genre_vibe", "Action")
                    context["action_description"] = data.get("action_description", "")
            except Exception as e:
                self.log_message(f"Script parse warning: {str(e)}", "WARNING")
        return context

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

    def _query_ai_shader_brain(self, scene_name, context):
        self.log_message(f"Calculating Anime Shading vectors for '{scene_name}'...", "INFO")
        
        if not self.gemini_api_key:
            self.log_message("No Gemini API Key found. Using procedural toon fallback.", "WARNING")
            return self._fallback_shader(context)

        ai_prompt = (
            f"You are the Lead Anime Render TD.\n"
            f"Scene Name: {scene_name}\n"
            f"Vibe/Genre: {context['vibe_genre']}\n"
            f"Action: {context['action_description']}\n\n"
            "Design ONLY Pure Anime Cel-Shading AND Battle Damage parameters.\n"
            "If it's intense Action, use thick outlines. If the character took a hit, increase 'battle_damage_level' (0.0 to 1.0).\n"
            "Return EXACTLY 1 raw JSON object containing:\n"
            "{\n"
            "  \"outline_thickness_pixels\": 3.5,\n"
            "  \"outline_color_hex\": \"#0A0202\",\n"
            "  \"shadow_sharpness_stop\": 0.45,\n"
            "  \"battle_damage_level\": 0.8,\n"
            "  \"damage_color_hex\": \"#8B0000\",\n"
            "  \"style_rationale\": \"Thick lines with heavy blood decals for action impact.\"\n"
            "}"
        )

        try:
            # NATIVE GEMINI JSON PAYLOAD
            payload = {
                "contents": [{"parts": [{"text": ai_prompt}]}], 
                "generationConfig": {"responseMimeType": "application/json"}
            }
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                cleaned = self._clean_json_response(res_text)
                return json.loads(cleaned)
        except Exception as e:
            self.log_message(f"Gemini API Route Failed: {str(e)}. Using fallback shader.", "WARNING")
            return self._fallback_shader(context)

    def _fallback_shader(self, context):
        return {
            "outline_thickness_pixels": 2.5, "outline_color_hex": "#050505",
            "shadow_sharpness_stop": 0.5, "battle_damage_level": 0.4,
            "damage_color_hex": "#5A0000", "style_rationale": "Procedural Anime Action Fallback"
        }

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

    # Force Anime EEVEE rendering rules
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    if hasattr(bpy.context.scene.eevee, "shadow_cascade_size"):
        bpy.context.scene.eevee.shadow_cascade_size = '2048' # Sharp shadows

    sharpness = {shader_data.get('shadow_sharpness_stop', 0.45)}
    line_thick = {shader_data.get('outline_thickness_pixels', 2.0)} * 0.001
    damage_lvl = {shader_data.get('battle_damage_level', 0.0)}
    damage_color = hex_to_rgb("{shader_data.get('damage_color_hex', '#8B0000')}")

    # FIX: Check for Agent 23 standard prefix (OMNI_CHAR) or general CH_ 
    char_objects = [obj for obj in bpy.context.scene.objects if (obj.name.startswith("OMNI_CHAR") or obj.name.startswith("CH_")) and obj.type == 'MESH']
    
    if not char_objects:
        print("WARNING: No character meshes found. Check Agent 23 placement.")
    
    for obj in char_objects:
        # --- A. INVERTED HULL (ANIME FREESTYLE OUTLINE) ---
        # Check if already has outline to prevent duplicate stacking
        has_outline = False
        for mod in obj.modifiers:
            if mod.name == "OMNI_Anime_Outline":
                has_outline = True
                mod.thickness = -line_thick
                break
                
        if not has_outline:
            mod = obj.modifiers.new(name="OMNI_Anime_Outline", type='SOLIDIFY')
            mod.use_flip_normals = True
            mod.thickness = -line_thick
            mod.material_offset = 100 # Forces it to use the last material slot
            
            outline_mat = bpy.data.materials.new(name="MAT_OMNI_Outline")
            outline_mat.use_nodes = True
            outline_mat.use_backface_culling = True # Essential for inverted hull
            
            nt_out = outline_mat.node_tree
            nt_out.nodes.clear()
            
            emit_node = nt_out.nodes.new('ShaderNodeEmission')
            emit_node.inputs['Color'].default_value = hex_to_rgb("{shader_data.get('outline_color_hex', '#000000')}")
            
            out_node_out = nt_out.nodes.new('ShaderNodeOutputMaterial')
            nt_out.links.new(emit_node.outputs['Emission'], out_node_out.inputs['Surface'])
            
            obj.data.materials.append(outline_mat)

        # --- B. CEL-SHADING & BATTLE DAMAGE ---
        for mat_slot in obj.material_slots:
            mat = mat_slot.material
            if mat and not mat.name.startswith("MAT_OMNI_Outline") and mat.use_nodes:
                nt = mat.node_tree
                
                # Check if it's already an Omni Toon shader
                if nt.nodes.get("OMNI_Toon_Ramp"):
                    continue
                    
                # Store original base color texture if it exists
                base_color_node = None
                for node in nt.nodes:
                    if node.type == 'TEX_IMAGE' and "Color" in str(node.outputs[0].links[0].to_socket.name) if node.outputs[0].links else False:
                        base_color_node = node
                        break
                
                # Clear tree to rebuild as pure Cel-Shader
                nt.nodes.clear()
                output_node = nt.nodes.new('ShaderNodeOutputMaterial')
                
                # Base Diffuse Node catches scene light
                diff_node = nt.nodes.new('ShaderNodeBsdfDiffuse')
                
                # Plug original texture back in
                if base_color_node:
                    tex_node = nt.nodes.new('ShaderNodeTexImage')
                    tex_node.image = base_color_node.image
                    nt.links.new(tex_node.outputs['Color'], diff_node.inputs['Color'])
                else:
                    diff_node.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1)

                # Shader To RGB (The magic of Eevee Cel Shading)
                s2rgb_node = nt.nodes.new('ShaderNodeShaderToRGB')
                nt.links.new(diff_node.outputs['BSDF'], s2rgb_node.inputs['Shader'])
                
                # Hard CONSTANT Ramp
                ramp_node = nt.nodes.new('ShaderNodeValToRGB')
                ramp_node.name = "OMNI_Toon_Ramp"
                ramp_node.color_ramp.interpolation = 'CONSTANT'
                ramp_node.color_ramp.elements[0].position = sharpness - 0.05
                ramp_node.color_ramp.elements[0].color = (0.3, 0.3, 0.3, 1.0) # Shadow tint
                ramp_node.color_ramp.elements[1].position = sharpness
                ramp_node.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0) # Light tint
                
                nt.links.new(s2rgb_node.outputs['Color'], ramp_node.inputs['Fac'])
                
                mix_node = nt.nodes.new('ShaderNodeMixRGB')
                mix_node.blend_type = 'MULTIPLY'
                mix_node.inputs['Fac'].default_value = 1.0
                nt.links.new(ramp_node.outputs['Color'], mix_node.inputs[1])
                
                # The Base Texture multiplied by the Toon Ramp
                if base_color_node:
                    nt.links.new(tex_node.outputs['Color'], mix_node.inputs[2])
                else:
                    mix_node.inputs[2].default_value = (0.8, 0.8, 0.8, 1)
                
                # --- INJECT BATTLE DAMAGE LAYER ---
                if damage_lvl > 0.0:
                    blood_mix = nt.nodes.new('ShaderNodeMixRGB')
                    blood_mix.inputs[2].default_value = damage_color
                    
                    noise = nt.nodes.new('ShaderNodeTexNoise')
                    noise.inputs['Scale'].default_value = 25.0 # Sharp small details
                    noise.inputs['Roughness'].default_value = 0.8
                    
                    dmg_ramp = nt.nodes.new('ShaderNodeValToRGB')
                    dmg_ramp.color_ramp.interpolation = 'CONSTANT'
                    dmg_ramp.color_ramp.elements[0].position = 1.0 - (damage_lvl * 0.5)
                    dmg_ramp.color_ramp.elements[1].position = 1.0 - (damage_lvl * 0.4)
                    nt.links.new(noise.outputs['Fac'], dmg_ramp.inputs['Fac'])
                    
                    nt.links.new(mix_node.outputs['Color'], blood_mix.inputs[1])
                    nt.links.new(dmg_ramp.outputs['Color'], blood_mix.inputs['Fac'])
                    nt.links.new(blood_mix.outputs['Color'], output_node.inputs['Surface'])
                else:
                    nt.links.new(mix_node.outputs['Color'], output_node.inputs['Surface'])

                # Strict Anime properties
                mat.blend_method = 'OPAQUE'
                mat.shadow_method = 'NONE' # Don't cast physical shadows, rely on cel

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS: Pure Anime Cel-Shading & Damage Applied.")

except Exception as e:
    print(f"ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_celshader_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def bake_cel_shading(self):
        self.log_message("Waking up Full Studio Anime Cel-Shader...", "INFO")
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_vibe(scene_name)
                shader_data = self._query_ai_shader_brain(scene_name, context)
                
                script_path = self._generate_blender_script(blend_path, shader_data)
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        self.log_message(f"Damage lvl {shader_data.get('battle_damage_level')} & Cel-Shade applied to {filename}", "SUCCESS")
                        master_blueprint[scene_name] = shader_data
                    else:
                        self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Anime Cel-Shader Pipeline Complete.", "INFO")

if __name__ == "__main__":
    shader_dop = FullStudioAnimeCelShader()
    shader_dop.bake_cel_shading()
