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
                    # Force environment variables to UPPERCASE taake masla hi khatam ho!
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class FullStudioAnimeCelShader:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 24: AAA Anime Cel Shader & Battle Damage"
        
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        self.output_blueprint = os.path.join(self.env_dir, "24_cel_shader_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
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
            except:
                pass
        return context

    def _query_ai_shader_brain(self, scene_name, context):
        if not self.gemini_api_key:
            return self._fallback_shader(context)

        ai_prompt = (
            f"You are the Lead Anime Render TD.\n"
            f"Scene Name: {scene_name}\n"
            f"Vibe/Genre: {context['vibe_genre']}\n"
            f"Action: {context['action_description']}\n\n"
            "Design Cel-Shading AND Battle Damage parameters.\n"
            "If it's intense Action, use thick outlines. If the character took a hit, increase 'battle_damage_level' (0.0 to 1.0).\n"
            "Return ONLY raw JSON:\n"
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
            payload = {"contents": [{"parts": [{"text": ai_prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                return json.loads(res_text)
        except Exception as e:
            self.log_message(f"AI Shader Design failed: {str(e)}", "WARNING")
            return self._fallback_shader(context)

    def _fallback_shader(self, context):
        return {
            "outline_thickness_pixels": 2.0, "outline_color_hex": "#000000",
            "shadow_sharpness_stop": 0.5, "battle_damage_level": 0.5,
            "damage_color_hex": "#8B0000", "style_rationale": "Fallback shader"
        }

    def _generate_blender_script(self, blend_file_path, shader_data):
        safe_blend_path = blend_file_path.replace("\\", "/")
        script_content = f"""
import bpy

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return (0, 0, 0, 1)
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    sharpness = {shader_data.get('shadow_sharpness_stop', 0.45)}
    line_thick = {shader_data.get('outline_thickness_pixels', 2.0)} * 0.001
    damage_lvl = {shader_data.get('battle_damage_level', 0.0)}
    damage_color = hex_to_rgb("{shader_data.get('damage_color_hex', '#8B0000')}")

    char_objects = [obj for obj in bpy.context.scene.objects if obj.name.startswith("CH_") and obj.type == 'MESH']
    
    for obj in char_objects:
        # A. Inverted Hull Method for Anime Outline
        mod = obj.modifiers.new(name="Anime_Ink_Outline", type='SOLIDIFY')
        mod.use_flip_normals = True
        mod.thickness = -line_thick
        mod.material_offset = 100
        
        outline_mat = bpy.data.materials.new(name="MAT_Anime_Outline")
        outline_mat.use_nodes = True
        outline_mat.use_backface_culling = True
        
        nt_out = outline_mat.node_tree
        nt_out.nodes.clear()
        emit_node = nt_out.nodes.new('ShaderNodeEmission')
        emit_node.inputs['Color'].default_value = hex_to_rgb("{shader_data.get('outline_color_hex', '#000000')}")
        out_node_out = nt_out.nodes.new('ShaderNodeOutputMaterial')
        nt_out.links.new(emit_node.outputs['Emission'], out_node_out.inputs['Surface'])
        
        obj.data.materials.append(outline_mat)

        # B. Rewrite Base Materials (Cel-Shaded + Battle Damage)
        for mat_slot in obj.material_slots:
            mat = mat_slot.material
            if mat and mat.name != "MAT_Anime_Outline" and mat.use_nodes:
                nt = mat.node_tree
                base_color_node = None
                for node in nt.nodes:
                    if node.type == 'TEX_IMAGE':
                        base_color_node = node
                        break
                        
                nt.nodes.clear()
                output_node = nt.nodes.new('ShaderNodeOutputMaterial')
                
                diff_node = nt.nodes.new('ShaderNodeBsdfDiffuse')
                if base_color_node:
                    nt.nodes.active = base_color_node
                    nt.nodes.get(base_color_node.name)
                else:
                    diff_node.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1)

                s2rgb_node = nt.nodes.new('ShaderNodeShaderToRGB')
                nt.links.new(diff_node.outputs['BSDF'], s2rgb_node.inputs['Shader'])
                
                ramp_node = nt.nodes.new('ShaderNodeValToRGB')
                ramp_node.color_ramp.interpolation = 'CONSTANT'
                ramp_node.color_ramp.elements[0].position = sharpness - 0.05
                ramp_node.color_ramp.elements[0].color = (0.4, 0.4, 0.4, 1.0)
                ramp_node.color_ramp.elements[1].position = sharpness
                ramp_node.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
                
                nt.links.new(s2rgb_node.outputs['Color'], ramp_node.inputs['Fac'])
                
                mix_node = nt.nodes.new('ShaderNodeMixRGB')
                mix_node.blend_type = 'MULTIPLY'
                mix_node.inputs['Fac'].default_value = 1.0
                nt.links.new(ramp_node.outputs['Color'], mix_node.inputs[1])
                
                # --- INJECT BATTLE DAMAGE LAYER ---
                if damage_lvl > 0.0:
                    blood_mix = nt.nodes.new('ShaderNodeMixRGB')
                    blood_mix.inputs[2].default_value = damage_color
                    
                    noise = nt.nodes.new('ShaderNodeTexNoise')
                    noise.inputs['Scale'].default_value = 15.0
                    
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

                mat.blend_method = 'OPAQUE'
                mat.shadow_method = 'NONE'

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS: Full Studio Cel-Shading & Damage applied.")
except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_celshader_script.py")
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
                subprocess.run([self.blender_path, "-b", "-P", script_path])
                self.log_message(f"Damage {shader_data['battle_damage_level']} & Cel-Shade applied to {filename}", "INFO")
                master_blueprint[scene_name] = shader_data

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)

if __name__ == "__main__":
    FullStudioAnimeCelShader().bake_cel_shading()
