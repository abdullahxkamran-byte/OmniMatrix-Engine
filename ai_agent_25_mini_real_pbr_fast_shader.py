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
                    # Force environment variables to UPPERCASE
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class MiniRealPBRFastShader:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 25: aaa_real_pbr_shader_grime_maker"
        
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        self.output_blueprint = os.path.join(self.workspace_dir, "25_pbr_shader_blueprint.json")
        self.blender_path = blender_path
        
        # GEMINI API INTEGRATION RESTORED
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.workspace_dir, self.script_dir, self.env_dir]:
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

    def _query_pbr_ai_brain(self, scene_name, context):
        self.log_message(f"Calculating PBR Realism vectors for '{scene_name}'...", "INFO")
        
        if not self.gemini_api_key:
            self.log_message("No Gemini API Key found. Using procedural fallback.", "WARNING")
            return self._fallback_pbr_shader(context)

        ai_prompt = (
            f"You are the Lead Texture & PBR Shader Artist.\n"
            f"Scene Name: {scene_name}\n"
            f"Action: {context['action_description']}\n\n"
            "Design PBR and Realistic Dirt/Blood parameters.\n"
            "If character takes damage, increase 'grime_damage_level' (0.0 to 1.0).\n"
            "Return EXACTLY 1 raw JSON object containing:\n"
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
            # GEMINI NATIVE JSON PAYLOAD
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
            return self._fallback_pbr_shader(context)

    def _fallback_pbr_shader(self, context):
        return {
            "base_color_hex": "#333333", "metallic_value": 0.5, "roughness_value": 0.3,
            "emission_color_hex": "#000000", "emission_strength": 0.0, 
            "grime_damage_level": 0.5, "grime_color_hex": "#3B1F1F"
        }

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

    # 1. Enable Realistic Engine Features in Eevee (Reflections & AO)
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    if hasattr(bpy.context.scene.eevee, "use_ssr"):
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
    print(f"ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_pbrshader_script.py")
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
                
                # Routing check (Universal Compatibility)
                context = self._check_style_routing(scene_name)
                style = context.get("visual_style", "realistic").lower()
                
                if "anime" in style or "cel" in style or "2d" in style:
                    self.log_message(f"[{scene_name}] Routing: Style is '{style}'. Going to SLEEP (Agent 24 handles this).", "INFO")
                    continue
                
                shader_data = self._query_pbr_ai_brain(scene_name, context)
                script_path = self._generate_blender_script(blend_file_path, shader_data)
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        self.log_message(f"PBR + Grime Level {shader_data.get('grime_damage_level')} applied to {filename}", "SUCCESS")
                        master_blueprint[scene_name] = shader_data
                    else:
                        self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Realistic PBR Pipeline Complete.", "INFO")

if __name__ == "__main__":
    shader_dop = MiniRealPBRFastShader()
    shader_dop.process_realistic_shading()
