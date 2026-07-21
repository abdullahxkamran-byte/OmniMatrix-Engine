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
                    # Har kisam ki key (gemini_api_key, Gemini_Api_Key) ko GEMINI_API_KEY mein badal dega
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class MiniRealPBRFastShader:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 25: AAA Real PBR Fast Shader"
        
        # Upstream Inputs
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments") # Modifies existing _stage.blend files
        
        # Outputs
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
        """
        Engine ka Asal Dimagh: Check karega ke style 'Realistic' hai ya 'Anime'.
        Agar Anime hai, toh Agent 25 so jayega.
        """
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {
            "visual_style": "realistic", # Defaulting to realistic for this agent's testing
            "vibe_genre": "Cyberpunk Action",
            "action_description": "Rainy street fight with metal swords"
        }
        
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "realistic").lower()
                    context["vibe_genre"] = data.get("genre_vibe", "Action")
                    context["action_description"] = data.get("action_description", "")
            except Exception as e:
                pass
                
        return context

    def _query_pbr_ai_brain(self, scene_name, context):
        if not self.gemini_api_key:
            return self._fallback_pbr_shader(context)

        ai_prompt = (
            f"You are the Lead Texture & PBR Shader Artist for a Realistic AAA Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Vibe/Genre: {context['vibe_genre']}\n"
            f"Action: {context['action_description']}\n\n"
            "Design the exact Principled BSDF parameters for the environment and characters.\n"
            "If it's dark/wet, increase specular and lower roughness. If it's sci-fi, add neon emission.\n"
            "Return ONLY raw JSON:\n"
            "{\n"
            "  \"base_color_hex\": \"#2E2E2E\",\n"
            "  \"metallic_value\": 0.8,\n"
            "  \"roughness_value\": 0.15,\n"
            "  \"specular_value\": 0.9,\n"
            "  \"emission_color_hex\": \"#00FFAA\",\n"
            "  \"emission_strength\": 5.0,\n"
            "  \"material_rationale\": \"Wet metallic surfaces reflecting neon lights.\"\n"
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
            return self._fallback_pbr_shader(context)

    def _fallback_pbr_shader(self, context):
        return {
            "base_color_hex": "#333333", "metallic_value": 0.5, "roughness_value": 0.3,
            "specular_value": 0.5, "emission_color_hex": "#000000", "emission_strength": 0.0,
            "material_rationale": "Fallback standard PBR realistic surface"
        }

    def _generate_blender_script(self, blend_file_path, shader_data):
        """Python script to inject Realistic Principled BSDF Settings and Eevee Realism."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return (0.5, 0.5, 0.5, 1)
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    # 1. Enable Realistic Engine Features in Eevee (Reflections & Ambient Occlusion)
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.eevee.use_ssr = True # Screen Space Reflections (crucial for wet/metal looks)
    bpy.context.scene.eevee.use_ssr_refraction = True
    bpy.context.scene.eevee.use_gtao = True # Ambient Occlusion for realistic shadows

    # Settings from AI
    color = hex_to_rgb("{shader_data.get('base_color_hex', '#555555')}")
    metallic = {shader_data.get('metallic_value', 0.0)}
    roughness = {shader_data.get('roughness_value', 0.5)}
    emission_color = hex_to_rgb("{shader_data.get('emission_color_hex', '#000000')}")
    emission_strength = {shader_data.get('emission_strength', 0.0)}

    # 2. Material Rewrite Loop (Using Principled BSDF for Realism)
    # We apply this to both Characters (CH_) and Environment (ENV_) objects
    target_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    for obj in target_objects:
        for mat_slot in obj.material_slots:
            mat = mat_slot.material
            if mat and mat.use_nodes:
                nt = mat.node_tree
                
                # Try to find Principled BSDF
                bsdf_node = None
                for node in nt.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        bsdf_node = node
                        break
                
                # If no Principled BSDF exists, recreate it
                if not bsdf_node:
                    nt.nodes.clear()
                    bsdf_node = nt.nodes.new('ShaderNodeBsdfPrincipled')
                    out_node = nt.nodes.new('ShaderNodeOutputMaterial')
                    nt.links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

                # Apply Realistic Properties
                # Only overwrite Base Color if there's no Image Texture hooked up
                if not bsdf_node.inputs['Base Color'].is_linked:
                    bsdf_node.inputs['Base Color'].default_value = color
                
                bsdf_node.inputs['Metallic'].default_value = metallic
                bsdf_node.inputs['Roughness'].default_value = roughness
                
                # Emission for glowing neon/sci-fi parts
                if emission_strength > 0:
                    bsdf_node.inputs['Emission Color'].default_value = emission_color
                    bsdf_node.inputs['Emission Strength'].default_value = emission_strength

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS: Realistic PBR Materials applied to scene.")

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
        
        # Process all Stage .blend files
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                # --- THE ROUTING LOGIC ---
                context = self._check_style_routing(scene_name)
                style = context.get("visual_style", "realistic").lower()
                
                if "anime" in style or "cel" in style or "2d" in style:
                    self.log_message(f"Scene '{scene_name}' is set to '{style}' mode.", "WARNING")
                    self.log_message(f"Going to SLEEP mode. (Agent 24 will handle the shading for this scene).", "INFO")
                    continue # Skips this scene completely!
                # -------------------------

                self.log_message(f"--- Applying Realistic PBR to: {scene_name} ---", "INFO")
                
                shader_data = self._query_pbr_ai_brain(scene_name, context)
                self.log_message(f"AI Decision: Metallic: {shader_data['metallic_value']} | Roughness: {shader_data['roughness_value']} | Reason: {shader_data['material_rationale']}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, shader_data)
                
                self.log_message("Executing Headless Blender to bake Realistic Materials...", "INFO")
                command = [self.blender_path, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_message(f"PBR Realism successfully injected into {filename}", "INFO")
                        master_blueprint[scene_name] = shader_data
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 25 Pipeline Complete. (All Realistic scenes processed, Anime scenes skipped).", "INFO")

if __name__ == "__main__":
    baker = MiniRealPBRFastShader()
    baker.process_realistic_shading()
