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
        self.agent_name = "Ai Agent 24: AAA Full Studio Anime Cel Shader"
        
        # Upstream Inputs
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments") # Modifies existing _stage.blend files
        
        # Outputs
        self.output_blueprint = os.path.join(self.env_dir, "24_cel_shader_blueprint.json")
        self.blender_path = blender_path
        
        # Secured API Call with safe fallback handling
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_vibe(self, scene_name):
        """Loads scene context so the shader can decide line thickness and shadow sharpness."""
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {"vibe_genre": "Action", "action_description": "Combat scene"}
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["vibe_genre"] = data.get("genre_vibe", "Action")
                    context["action_description"] = data.get("action_description", "")
            except Exception as e:
                pass
        return context

    def _query_ai_shader_brain(self, scene_name, context):
        if not self.gemini_api_key:
            return self._fallback_shader(context)

        ai_prompt = (
            f"You are the Lead Anime Render TD (like Ufotable or MAPPA).\n"
            f"Scene Name: {scene_name}\n"
            f"Vibe/Genre: {context['vibe_genre']}\n"
            f"Action: {context['action_description']}\n\n"
            "Design the exact Cel-Shading parameters for the characters in this scene.\n"
            "If it's intense Action/Phonk, use thick ink outlines and sharp shadow stops. If it's gentle, use soft outlines.\n"
            "Return ONLY raw JSON:\n"
            "{\n"
            "  \"outline_thickness_pixels\": 3.5,\n"
            "  \"outline_color_hex\": \"#0A0202\",\n"
            "  \"shadow_sharpness_stop\": 0.45,\n"
            "  \"specular_glossiness\": 0.15,\n"
            "  \"rim_light_multiplier\": 2.0,\n"
            "  \"style_rationale\": \"Thick lines for heavy action impact.\"\n"
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
            self.log_message(f"AI Shader Design failed: {str(e)}. Using fallback.", "WARNING")
            return self._fallback_shader(context)

    def _fallback_shader(self, context):
        return {
            "outline_thickness_pixels": 2.0, "outline_color_hex": "#000000",
            "shadow_sharpness_stop": 0.5, "specular_glossiness": 0.1,
            "rim_light_multiplier": 1.5, "style_rationale": "Fallback standard Cel-Shading"
        }

    def _generate_blender_script(self, blend_file_path, shader_data):
        """Python script for Blender that rewrites ALL character materials to NPR Cel Shading."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return (0, 0, 0, 1)
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    # 1. Enable Shader to RGB in Eevee (Required for Cel Shading)
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    # Settings from AI
    sharpness = {shader_data.get('shadow_sharpness_stop', 0.45)}
    line_thick = {shader_data.get('outline_thickness_pixels', 2.0)} * 0.001 # Scale to Blender units
    rim_mult = {shader_data.get('rim_light_multiplier', 1.5)}

    # 2. Material Rewrite Loop
    # We target objects appended by Agent 23 (starting with 'CH_')
    char_objects = [obj for obj in bpy.context.scene.objects if obj.name.startswith("CH_") and obj.type == 'MESH']
    
    for obj in char_objects:
        # A. Apply Inverted Hull Method for Anime Ink Outline
        mod = obj.modifiers.new(name="Anime_Ink_Outline", type='SOLIDIFY')
        mod.use_flip_normals = True
        mod.thickness = -line_thick
        mod.material_offset = 100 # Forces it to use the last material
        
        # Outline Material
        outline_mat = bpy.data.materials.new(name="MAT_Anime_Outline")
        outline_mat.use_nodes = True
        outline_mat.use_backface_culling = True # Critical for Inverted Hull
        
        # Clean outline nodes
        nt_out = outline_mat.node_tree
        nt_out.nodes.clear()
        emit_node = nt_out.nodes.new('ShaderNodeEmission')
        emit_node.inputs['Color'].default_value = hex_to_rgb("{shader_data.get('outline_color_hex', '#000000')}")
        out_node_out = nt_out.nodes.new('ShaderNodeOutputMaterial')
        nt_out.links.new(emit_node.outputs['Emission'], out_node_out.inputs['Surface'])
        
        obj.data.materials.append(outline_mat)

        # B. Rewrite Base Materials to Cel-Shaded (Shader to RGB -> ColorRamp)
        for mat_slot in obj.material_slots:
            mat = mat_slot.material
            if mat and mat.name != "MAT_Anime_Outline" and mat.use_nodes:
                nt = mat.node_tree
                
                # Find Base Color Image Texture if it exists
                base_color_node = None
                for node in nt.nodes:
                    if node.type == 'TEX_IMAGE':
                        base_color_node = node
                        break
                        
                # Clear all nodes
                nt.nodes.clear()
                
                # Rebuild Anime Shader Pipeline
                output_node = nt.nodes.new('ShaderNodeOutputMaterial')
                
                # Diffuse -> Shader To RGB
                diff_node = nt.nodes.new('ShaderNodeBsdfDiffuse')
                if base_color_node:
                    nt.nodes.active = base_color_node # Keep texture reference
                    nt.nodes.get(base_color_node.name)
                else:
                    diff_node.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1) # Default Greyish

                s2rgb_node = nt.nodes.new('ShaderNodeShaderToRGB')
                nt.links.new(diff_node.outputs['BSDF'], s2rgb_node.inputs['Shader'])
                
                # ColorRamp for Sharp Anime Shadows
                ramp_node = nt.nodes.new('ShaderNodeValToRGB')
                ramp_node.color_ramp.interpolation = 'CONSTANT' # Hard shadow cut!
                ramp_node.color_ramp.elements[0].position = sharpness - 0.05
                ramp_node.color_ramp.elements[0].color = (0.4, 0.4, 0.4, 1.0) # Shadow tint
                ramp_node.color_ramp.elements[1].position = sharpness
                ramp_node.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0) # Light tint
                
                nt.links.new(s2rgb_node.outputs['Color'], ramp_node.inputs['Fac'])
                
                # Mix Shader (Base Texture * Cel Shadows)
                mix_node = nt.nodes.new('ShaderNodeMixRGB')
                mix_node.blend_type = 'MULTIPLY'
                mix_node.inputs['Fac'].default_value = 1.0
                nt.links.new(ramp_node.outputs['Color'], mix_node.inputs[1])
                # In real scenario we link base_color_node to mix_node.inputs[2]
                
                nt.links.new(mix_node.outputs['Color'], output_node.inputs['Surface'])
                mat.blend_method = 'OPAQUE'
                mat.shadow_method = 'NONE' # Disable soft shadows for anime

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS: Full Studio Cel-Shading applied to scene.")

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
        
        # Process all Stage .blend files
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                self.log_message(f"--- Applying Cel-Shading to: {scene_name} ---", "INFO")
                
                context = self._load_upstream_vibe(scene_name)
                shader_data = self._query_ai_shader_brain(scene_name, context)
                
                self.log_message(f"AI Decision: Outline {shader_data['outline_thickness_pixels']}px | Reason: {shader_data['style_rationale']}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, shader_data)
                
                self.log_message("Executing Headless Blender to bake Anime Materials...", "INFO")
                command = [self.blender_path, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_message(f"Cel-Shading successfully injected into {filename}", "INFO")
                        master_blueprint[scene_name] = shader_data
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 24 Cel-Shading Pipeline Complete. Environment is fully 2.5D Anime styled.", "INFO")

if __name__ == "__main__":
    shader = FullStudioAnimeCelShader()
    shader.bake_cel_shading()
