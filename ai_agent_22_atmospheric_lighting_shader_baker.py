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
                    os.environ[key.strip()] = val.strip()

load_env_file()

class AtmosphericLightingShaderBaker:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 22: Autonomous Atmospheric Lighting DoP"
        
        # Upstream Inputs
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments") # Modifies existing _stage.blend files
        
        # Outputs
        self.output_blueprint = os.path.join(self.env_dir, "22_lighting_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_vibe(self, scene_name):
        """Reads the emotional context and action of the scene for autonomous lighting decisions."""
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

    def _query_autonomous_lighting_brain(self, scene_name, context):
        if not self.gemini_api_key:
            return self._get_fallback_lighting()

        ai_prompt = (
            f"You are a Master Cinematic DoP and Lighting Director.\n"
            f"Design the atmospheric lighting for scene '{scene_name}' based on this context:\n"
            f"Genre/Vibe: {context['vibe_genre']}\n"
            f"Time of Day: {context['time_of_day']}\n"
            f"Action: {context['action_description']}\n\n"
            "Decide the exact lighting colors, fog density, and strength. If it's Phonk/Cyberpunk, use extreme neon rim lights. If it's Dark Realism, use heavy volumetric fog and dim lighting. If Anime Action, use high contrast colors.\n"
            "Return ONLY raw JSON in this exact format:\n"
            "{\n"
            "  \"world_tint_hex\": \"#0A0514\",\n"
            "  \"world_hdri_strength\": 0.1,\n"
            "  \"volumetric_fog_density\": 0.08,\n"
            "  \"key_light_type\": \"SPOT\",\n"
            "  \"key_light_color_hex\": \"#00FFFF\",\n"
            "  \"key_light_power_watts\": 1500.0,\n"
            "  \"rim_light_color_hex\": \"#FF0055\",\n"
            "  \"rim_light_power_watts\": 3000.0,\n"
            "  \"bloom_intensity\": 1.2,\n"
            "  \"cinematic_rationale\": \"Short explanation of why you chose these settings\"\n"
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
            self.log_message(f"Gemini AI Brain failed: {str(e)}. Using fallback.", "WARNING")
            return self._get_fallback_lighting()

    def _get_fallback_lighting(self):
        return {
            "world_tint_hex": "#05050A", "world_hdri_strength": 0.2, "volumetric_fog_density": 0.05,
            "key_light_type": "AREA", "key_light_color_hex": "#FFFFFF", "key_light_power_watts": 800.0,
            "rim_light_color_hex": "#FF4400", "rim_light_power_watts": 2000.0, "bloom_intensity": 1.0,
            "cinematic_rationale": "Fallback standard action lighting setup"
        }

    def _generate_blender_script(self, blend_file_path, lighting_data):
        """Injects procedural Node setups for Volumetrics and Lighting directly into the Blend file."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return (1.0, 1.0, 1.0, 1.0)
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    # 1. Clean existing default lights to avoid blowing out the scene
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)

    # 2. World Background & Volumetrics Setup
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("AAA_World")
        bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    
    bg_node = nt.nodes.get("Background")
    out_node = nt.nodes.get("World Output")
    
    if bg_node:
        bg_node.inputs['Color'].default_value = hex_to_rgb("{lighting_data.get('world_tint_hex', '#000000')}")
        bg_node.inputs['Strength'].default_value = {lighting_data.get('world_hdri_strength', 0.1)}
    
    # Atmospheric Fog / God Rays
    fog_density = {lighting_data.get('volumetric_fog_density', 0.0)}
    if fog_density > 0.0:
        vol_node = nt.nodes.new(type="ShaderNodeVolumePrincipled")
        vol_node.inputs['Density'].default_value = fog_density
        vol_node.inputs['Anisotropy'].default_value = 0.6 # Good for God Rays
        nt.links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])

    # 3. Key Light Creation
    key_data = bpy.data.lights.new(name="AAA_Key_Light", type="{lighting_data.get('key_light_type', 'SPOT')}")
    key_data.energy = {lighting_data.get('key_light_power_watts', 1000.0)}
    key_data.color = hex_to_rgb("{lighting_data.get('key_light_color_hex', '#FFFFFF')}")[:3]
    if key_data.type == 'SPOT':
        key_data.spot_size = 1.04 # ~60 degrees
        key_data.spot_blend = 0.5
        
    key_obj = bpy.data.objects.new(name="AAA_Key_Light", object_data=key_data)
    bpy.context.scene.collection.objects.link(key_obj)
    key_obj.location = (2.0, -4.0, 5.0) # Standard dramatic front-top right

    # 4. Rim Light Creation (Crucial for Anime & Cinematic Edges)
    rim_data = bpy.data.lights.new(name="AAA_Rim_Light", type="AREA")
    rim_data.energy = {lighting_data.get('rim_light_power_watts', 2000.0)}
    rim_data.color = hex_to_rgb("{lighting_data.get('rim_light_color_hex', '#FF0000')}")[:3]
    rim_data.shape = 'RECTANGLE'
    rim_data.size = 5.0
    rim_data.size_y = 1.0
    
    rim_obj = bpy.data.objects.new(name="AAA_Rim_Light", object_data=rim_data)
    bpy.context.scene.collection.objects.link(rim_obj)
    rim_obj.location = (-3.0, 4.0, 1.0) # Placed behind character
    
    # Point lights to center (origin)
    track_key = key_obj.constraints.new(type='TRACK_TO')
    track_key.target = bpy.data.objects.get("Focus_Tracker") # Created by Agent 21
    track_rim = rim_obj.constraints.new(type='TRACK_TO')
    track_rim.target = bpy.data.objects.get("Focus_Tracker")

    # 5. Enable Render Settings (Eevee Bloom & Volumetrics)
    if bpy.context.scene.render.engine == 'BLENDER_EEVEE':
        bpy.context.scene.eevee.use_bloom = True
        bpy.context.scene.eevee.bloom_intensity = {lighting_data.get('bloom_intensity', 1.0)}
        bpy.context.scene.eevee.use_volumetric = True
        bpy.context.scene.eevee.volumetric_tile_size = '4' # High Quality
        bpy.context.scene.eevee.use_volumetric_shadows = True

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS: Lighting baked into scene.")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_lighting_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_scene_lighting(self):
        self.log_message("Waking up Autonomous DoP (Director of Photography)...", "INFO")
        
        master_blueprint = {}
        
        # Run through all stage files
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                self.log_message(f"--- Lighting Scene: {scene_name} ---", "INFO")
                
                context = self._load_upstream_vibe(scene_name)
                self.log_message(f"Vibe Detected: {context['vibe_genre']} | Action: {context['action_description'][:30]}...", "INFO")
                
                # Let Gemini decide the lighting palette
                lighting_data = self._query_autonomous_lighting_brain(scene_name, context)
                self.log_message(f"AI Decision: {lighting_data.get('cinematic_rationale', 'Custom Lighting Applied')}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, lighting_data)
                
                self.log_message(f"Executing Headless Blender to inject volumetric lighting...", "INFO")
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_message(f"Atmosphere successfully baked into {filename}", "INFO")
                        master_blueprint[scene_name] = lighting_data
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
        
        self.log_message("Agent 22 Lighting Pipeline Complete.", "INFO")

if __name__ == "__main__":
    baker = AtmosphericLightingShaderBaker()
    baker.process_scene_lighting()
