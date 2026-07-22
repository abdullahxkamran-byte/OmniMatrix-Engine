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

class UniversalAtmosphericLightingDoP:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 22: universal_atmospheric_lighting_dop"
        
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        self.output_blueprint = os.path.join(self.workspace_dir, "22_universal_lighting_blueprint.json")
        self.blender_path = blender_path
        
        # Unified AI Routing
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_cloud = "gpt-4o-mini"
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        for d in [self.workspace_dir, self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_master_config(self):
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("global_style", "realistic").lower()
            except Exception as e:
                self.log_message(f"Master config read warning: {str(e)}", "WARNING")
        return "realistic"

    def _load_upstream_vibe(self, scene_name):
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {"vibe_genre": "Neutral", "action_description": "Static environment", "time_of_day": "Unknown"}
        
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["vibe_genre"] = data.get("genre_vibe", "Action")
                    context["action_description"] = data.get("action_description", "")
                    context["time_of_day"] = data.get("time_of_day", "Night")
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

    def _query_lighting_brain(self, scene_name, context, style):
        self.log_message(f"Consulting Lighting DoP for '{scene_name}' (Style: {style.upper()})...", "INFO")

        system_prompt = (
            f"You are the Master Cinematic DoP. The global project style is '{style.upper()}'.\n"
            f"Design lighting for scene '{scene_name}'. Context:\n"
            f"Genre: {context['vibe_genre']} | Time: {context['time_of_day']} | Action: {context['action_description']}\n"
            "If style is REALISTIC: Use physical values, subtle colored key/fill (e.g., orange/teal), dense volumetric fog, and soft rim lights.\n"
            "If style is ANIME: Use high-contrast vibrant colors, very low fog (to keep lines sharp), high-power colored rim lights, and bright fill light.\n"
            "Output EXACTLY 1 raw JSON object containing:\n"
            "- 'world_tint_hex': string.\n"
            "- 'volumetric_fog_density': float (0.01 to 0.1).\n"
            "- 'key_light_color_hex': string.\n"
            "- 'key_light_power_watts': float.\n"
            "- 'fill_light_color_hex': string.\n"
            "- 'fill_light_power_watts': float.\n"
            "- 'rim_light_color_hex': string.\n"
            "- 'rim_light_power_watts': float.\n"
            "- 'cinematic_rationale': string.\n"
            "Output strictly valid JSON with no backticks."
        )

        if self.openai_api_key:
            try:
                payload = {
                    "model": self.model_cloud,
                    "messages": [{"role": "system", "content": system_prompt}],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    return json.loads(cleaned)
            except Exception as e:
                self.log_message(f"Cloud API Route Failed: {str(e)}. Using procedural fallback.", "WARNING")

        return self._get_fallback_lighting(style)

    def _get_fallback_lighting(self, style):
        if style == "realistic":
            return {
                "world_tint_hex": "#050A10", "volumetric_fog_density": 0.04,
                "key_light_color_hex": "#FFE0CC", "key_light_power_watts": 1200.0,
                "fill_light_color_hex": "#AACCFF", "fill_light_power_watts": 400.0,
                "rim_light_color_hex": "#FFFFFF", "rim_light_power_watts": 2500.0,
                "cinematic_rationale": "Fallback Realistic Orange/Teal 3-Point Setup"
            }
        else:
            return {
                "world_tint_hex": "#110022", "volumetric_fog_density": 0.01,
                "key_light_color_hex": "#FF0055", "key_light_power_watts": 2000.0,
                "fill_light_color_hex": "#3300AA", "fill_light_power_watts": 1000.0,
                "rim_light_color_hex": "#00FFFF", "rim_light_power_watts": 5000.0,
                "cinematic_rationale": "Fallback Anime Cyberpunk High-Contrast Setup"
            }

    def _generate_blender_script(self, blend_file_path, lighting_data, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy
import math

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return (1.0, 1.0, 1.0, 1.0)
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")
    
    # 1. Clean old lights to prevent over-exposure
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT' or obj.name.startswith("AAA_"):
            bpy.data.objects.remove(obj, do_unlink=True)

    # 2. World & Volumetrics Setup
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("OMNIMATRIX_World")
        bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    
    bg_node = nt.nodes.get("Background")
    out_node = nt.nodes.get("World Output")
    
    if bg_node:
        bg_node.inputs['Color'].default_value = hex_to_rgb("{lighting_data.get('world_tint_hex', '#000000')}")
        bg_node.inputs['Strength'].default_value = 0.1 if '{style}' == 'realistic' else 0.5
    
    # Atmospheric Fog
    fog_density = {lighting_data.get('volumetric_fog_density', 0.0)}
    if fog_density > 0.0:
        vol_node = nt.nodes.new(type="ShaderNodeVolumePrincipled")
        vol_node.inputs['Density'].default_value = fog_density
        vol_node.inputs['Anisotropy'].default_value = 0.7 # Enhances God Rays
        nt.links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])

    # 3. Locate Tracking Target (Linked to Agent 21's new Rig)
    target = bpy.data.objects.get("OMNIMATRIX_Focus_Target")
    if not target:
        # Fallback if Agent 21 hasn't run yet
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1))
        target = bpy.context.active_object
        target.name = "OMNIMATRIX_Focus_Target"

    # --- 4. AAA 3-POINT LIGHTING SYSTEM ---
    
    # A. KEY LIGHT (Main Illumination)
    key_data = bpy.data.lights.new(name="AAA_Key_Light", type="SPOT")
    key_data.energy = {lighting_data.get('key_light_power_watts', 1500.0)}
    key_data.color = hex_to_rgb("{lighting_data.get('key_light_color_hex', '#FFFFFF')}")[:3]
    key_data.spot_size = math.radians(60)
    key_data.spot_blend = 0.8 if '{style}' == 'realistic' else 0.1 # Soft edges for realistic, hard for anime
    
    key_obj = bpy.data.objects.new(name="AAA_Key_Light", object_data=key_data)
    bpy.context.scene.collection.objects.link(key_obj)
    key_obj.location = (3.0, -4.0, 4.0) 
    
    track_key = key_obj.constraints.new(type='TRACK_TO')
    track_key.target = target
    track_key.track_axis = 'TRACK_NEGATIVE_Z'
    track_key.up_axis = 'UP_Y'

    # B. FILL LIGHT (Shadow Detail)
    fill_data = bpy.data.lights.new(name="AAA_Fill_Light", type="AREA")
    fill_data.energy = {lighting_data.get('fill_light_power_watts', 500.0)}
    fill_data.color = hex_to_rgb("{lighting_data.get('fill_light_color_hex', '#FFFFFF')}")[:3]
    fill_data.shape = 'RECTANGLE'
    fill_data.size = 4.0
    
    fill_obj = bpy.data.objects.new(name="AAA_Fill_Light", object_data=fill_data)
    bpy.context.scene.collection.objects.link(fill_obj)
    fill_obj.location = (-4.0, -2.0, 2.0) # Opposite to Key Light
    
    track_fill = fill_obj.constraints.new(type='TRACK_TO')
    track_fill.target = target
    track_fill.track_axis = 'TRACK_NEGATIVE_Z'
    track_fill.up_axis = 'UP_Y'

    # C. RIM LIGHT (Edge Separation)
    rim_data = bpy.data.lights.new(name="AAA_Rim_Light", type="SPOT")
    rim_data.energy = {lighting_data.get('rim_light_power_watts', 3000.0)}
    rim_data.color = hex_to_rgb("{lighting_data.get('rim_light_color_hex', '#FFFFFF')}")[:3]
    rim_data.spot_size = math.radians(45)
    rim_data.spot_blend = 0.2
    
    rim_obj = bpy.data.objects.new(name="AAA_Rim_Light", object_data=rim_data)
    bpy.context.scene.collection.objects.link(rim_obj)
    rim_obj.location = (-2.0, 5.0, 3.0) # Placed behind the target
    
    track_rim = rim_obj.constraints.new(type='TRACK_TO')
    track_rim.target = target
    track_rim.track_axis = 'TRACK_NEGATIVE_Z'
    track_rim.up_axis = 'UP_Y'

    # 5. Engine Specific Overrides
    if '{style}' == 'anime':
        # Eevee Next (Blender 4.0+) / Standard Eevee tweaks for Anime
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        try:
            bpy.context.scene.eevee.use_bloom = True
            bpy.context.scene.eevee.bloom_intensity = 1.2
            # Flattens shadows for anime cel shading
            bpy.context.scene.eevee.shadow_cascade_size = '2048'
        except:
            pass # Failsafe for Blender 4.2+ where Eevee Next handles bloom via compositor

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS")

except Exception as e:
    print(f"FAILED TO LIGHT SCENE: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_lighting_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_scene_lighting(self):
        global_style = self._load_master_config()
        self.log_message(f"Waking up Universal DoP [{global_style.upper()}]...", "INFO")
        
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_vibe(scene_name)
                
                lighting_data = self._query_lighting_brain(scene_name, context, global_style)
                self.log_message(f"[{scene_name}] AI Logic: {lighting_data.get('cinematic_rationale', 'Applied')}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, lighting_data, global_style)
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        self.log_message(f"AAA Lighting baked into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = lighting_data
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
        
        self.log_message("Universal Lighting Pipeline Complete.", "INFO")

if __name__ == "__main__":
    baker = UniversalAtmosphericLightingDoP()
    baker.process_scene_lighting()
