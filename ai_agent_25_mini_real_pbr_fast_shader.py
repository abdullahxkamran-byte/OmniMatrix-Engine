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
                    os.environ[line.split("=", 1)[0].strip().upper()] = line.split("=", 1)[1].strip()

load_env_file()

class MiniRealPBRFastShader:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 25: AAA Real PBR Shader & Grime Maker"
        
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        self.output_blueprint = os.path.join(self.env_dir, "25_pbr_shader_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _check_style_routing(self, scene_name):
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {"visual_style": "realistic", "vibe_genre": "Cyberpunk Action", "action_description": "Fight"}
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "realistic").lower()
                    context["vibe_genre"] = data.get("genre_vibe", "Action")
                    context["action_description"] = data.get("action_description", "")
            except:
                pass
        return context

    def _query_pbr_ai_brain(self, scene_name, context):
        if not self.gemini_api_key:
            return self._fallback_pbr_shader(context)

        ai_prompt = (
            f"You are the Lead Texture & PBR Shader Artist.\n"
            f"Scene Name: {scene_name}\n"
            f"Action: {context['action_description']}\n\n"
            "Design PBR and Realistic Dirt/Blood parameters.\n"
            "If character takes damage, increase 'grime_damage_level' (0.0 to 1.0).\n"
            "Return ONLY raw JSON:\n"
            "{\n"
            "  \"base_color_hex\": \"#2E2E2E\",\n"
            "  \"metallic_value\": 0.8,\n"
            "  \"roughness_value\": 0.15,\n"
            "  \"emission_color_hex\": \"#00FFAA\",\n"
            "  \"emission_strength\": 5.0,\n"
            "  \"grime_damage_level\": 0.75,\n"
            "  \"grime_color_hex\": \"#3B1F1F\"\n"
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
        except:
            return self._fallback_pbr_shader(context)

    def _fallback_pbr_shader(self, context):
        return {
            "base_color_hex": "#333333", "metallic_value": 0.5, "roughness_value": 0.3,
            "emission_strength": 0.0, "grime_damage_level": 0.5, "grime_color_hex": "#3B1F1F"
        }

    def _generate_blender_script(self, blend_file_path, shader_data):
        safe_blend_path = blend_file_path.replace("\\", "/")
        script_content = f"""
import bpy

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return (0.5, 0.5, 0.5, 1)
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    # 1. Enable Realistic Engine Features in Eevee (Reflections & AO)
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.eevee.use_ssr = True 
    bpy.context.scene.eevee.use_ssr_refraction = True
    bpy.context.scene.eevee.use_gtao = True 

    color = hex_to_rgb("{shader_data.get('base_color_hex', '#555555')}")
    metallic = {shader_data.get('metallic_value', 0.0)}
    roughness = {shader_data.get('roughness_value', 0.5)}
    emission_color = hex_to_rgb("{shader_data.get('emission_color_hex', '#000000')}")
    emission_strength = {shader_data.get('emission_strength', 0.0)}
    grime_lvl = {shader_data.get('grime_damage_level', 0.0)}
    grime_color = hex_to_rgb("{shader_data.get('grime_color_hex', '#3B1F1F')}")

    target_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    for obj in target_objects:
        for mat_slot in obj.material_slots:
            mat = mat_slot.material
            if mat and mat.use_nodes:
                nt = mat.node_tree
                
                bsdf_node = None
                for node in nt.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        bsdf_node = node
                        break
                
                if not bsdf_node:
                    nt.nodes.clear()
                    bsdf_node = nt.nodes.new('ShaderNodeBsdfPrincipled')
                    out_node = nt.nodes.new('ShaderNodeOutputMaterial')
                    nt.links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

                if not bsdf_node.inputs['Base Color'].is_linked:
                    bsdf_node.inputs['Base Color'].default_value = color
                
                bsdf_node.inputs['Metallic'].default_value = metallic
                bsdf_node.inputs['Roughness'].default_value = roughness
                
                if emission_strength > 0:
                    bsdf_node.inputs['Emission Color'].default_value = emission_color
                    bsdf_node.inputs['Emission Strength'].default_value = emission_strength

                # --- INJECT REALISTIC GRIME & WET BLOOD LAYER ---
                if grime_lvl > 0.0:
                    noise = nt.nodes.new('ShaderNodeTexNoise')
                    noise.inputs['Scale'].default_value = 25.0 
                    
                    ramp = nt.nodes.new('ShaderNodeValToRGB')
                    ramp.color_ramp.elements[0].position = 1.0 - (grime_lvl * 0.8)
                    ramp.color_ramp.elements[1].position = 1.0
                    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
                    
                    mix_color = nt.nodes.new('ShaderNodeMixRGB')
                    mix_color.inputs[2].default_value = grime_color
                    
                    if bsdf_node.inputs['Base Color'].is_linked:
                        prev_color = bsdf_node.inputs['Base Color'].links[0].from_node
                        nt.links.new(prev_color.outputs[0], mix_color.inputs[1])
                    else:
                        mix_color.inputs[1].default_value = bsdf_node.inputs['Base Color'].default_value
                        
                    nt.links.new(ramp.outputs['Color'], mix_color.inputs['Fac'])
                    nt.links.new(mix_color.outputs['Color'], bsdf_node.inputs['Base Color'])
                    
                    # Wet specular roughness for blood
                    mix_rough = nt.nodes.new('ShaderNodeMixRGB')
                    mix_rough.inputs[1].default_value = (roughness, roughness, roughness, 1.0)
                    mix_rough.inputs[2].default_value = (0.1, 0.1, 0.1, 1.0)
                    nt.links.new(ramp.outputs['Color'], mix_rough.inputs['Fac'])
                    nt.links.new(mix_rough.outputs['Color'], bsdf_node.inputs['Roughness'])

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS: Realistic PBR Materials + Grime applied.")
except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_pbrshader_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_realistic_shading(self):
        self.log_message("Waking up Realistic PBR Shader Engine...", "INFO")
        master_blueprint = {}
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                # Routing check
                context = self._check_style_routing(scene_name)
                style = context.get("visual_style", "realistic").lower()
                
                if "anime" in style or "cel" in style or "2d" in style:
                    self.log_message(f"Scene '{scene_name}' is '{style}'. Going to SLEEP.", "WARNING")
                    continue
                
                shader_data = self._query_pbr_ai_brain(scene_name, context)
                script_path = self._generate_blender_script(blend_file_path, shader_data)
                
                subprocess.run([self.blender_path, "-b", "-P", script_path])
                self.log_message(f"PBR + Damage Level {shader_data['grime_damage_level']} applied to {filename}", "INFO")
                master_blueprint[scene_name] = shader_data

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)

if __name__ == "__main__":
    MiniRealPBRFastShader().process_realistic_shading()
