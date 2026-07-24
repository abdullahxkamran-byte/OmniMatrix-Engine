# ==============================================================================
# Ai_Agent_22_Atmospheric_Lighting_Shader_Baker.py
# MODULE C: Blender 3D Heavy Infantry
# ==============================================================================

import os
import re
import sys
import json
import math
import random
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

class AiAgent22AtmosphericLightingShaderBaker:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_22_Atmospheric_Lighting_Shader_Baker"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_root = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_root, "Module_A_Scripting")
        self.audio_dir = os.path.join(self.workspace_root, "Module_B_Audio")
        self.module_c_dir = os.path.join(self.workspace_root, "Module_C_Heavy_Infantry")
        self.env_dir = os.path.join(self.workspace_root, "Module_H_Generative", "3d_environments")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "22_master_lighting_blueprint.json")
        
        # System States (RULE 7)
        self.state_file = os.path.join(self.workspace_root, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_root, "global_config.json")
        
        # API Keys for Quad-Core (RULE 6)
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        for d in [self.workspace_root, self.script_dir, self.audio_dir, self.module_c_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    # RULE 3: IDEMPOTENCY SCRUBBING
    def scrub_workspace(self):
        if os.path.exists(self.output_blueprint):
            try:
                os.remove(self.output_blueprint)
            except: pass

    # RULE 4: LIMITLESS FLUIDITY
    def _load_master_config(self):
        default_config = {"global_style": "anime", "fps": 24, "blender_executable": "blender"}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except: pass
        return default_config

    def _load_upstream_vibe(self, scene_name):
        context = {"vibe_genre": "Cinematic", "action": "Standby", "intensity": "low"}
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["vibe_genre"] = data.get("genre_vibe", "Cinematic")
                    context["action"] = data.get("action_description", "")
                    context["intensity"] = "high" if "fight" in context["action"].lower() or "run" in context["action"].lower() else "low"
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

    # RULE 10: 100% OFFLINE AUTONOMY (Mathematically synthesize lighting logic)
    def _get_procedural_fallback_lighting(self, context, style):
        is_action = context.get("intensity") == "high"
        
        if style == "realistic":
            return {
                "world_tint_hex": "#080b12", "volumetric_fog_density": 0.05,
                "key_light_color_hex": "#ffebd6", "key_light_power_watts": 1500.0,
                "fill_light_color_hex": "#a3ccff", "fill_light_power_watts": 300.0,
                "rim_light_color_hex": "#ffffff", "rim_light_power_watts": 2500.0,
                "light_flicker_intensity": 0.5 if is_action else 0.05,
                "cinematic_rationale": "Procedural Offline Setup: Teal/Orange"
            }
        else: # Anime
            return {
                "world_tint_hex": "#1a0033", "volumetric_fog_density": 0.01,
                "key_light_color_hex": "#ff2a6d", "key_light_power_watts": 2500.0,
                "fill_light_color_hex": "#05d9e8", "fill_light_power_watts": 800.0,
                "rim_light_color_hex": "#d1f7ff", "rim_light_power_watts": 8000.0,
                "light_flicker_intensity": 1.0 if is_action else 0.0,
                "cinematic_rationale": "Procedural Offline Setup: Cyberpunk Anime"
            }

    # RULE 6: QUAD-CORE FALLBACK
    def _query_lighting_brain(self, scene_name, context, config):
        style = config.get("global_style", "realistic")
        self.log(f"Consulting AAA Lighting DoP for '{scene_name}' [{style.upper()}]...", "INFO")

        ai_prompt = f"""
        You are the Master Cinematic DoP for a Limitless 3D Engine. Style: '{style.upper()}'.
        Design lighting for scene '{scene_name}'. 
        Context: Genre={context['vibe_genre']} | Action={context['action']} | Intensity={context['intensity']}
        
        RULES:
        - REALISTIC: Use physical watts (1000-5000), subtle complementary colors (e.g., orange key / teal fill), thick fog (0.02 - 0.08). Flicker should be subtle (0.05 - 0.2).
        - ANIME/SAKUGA: High-power watts (2000-10000), vibrant neon colors, very low fog (0.0 - 0.01) to keep cel lines sharp. Massive Rim Light power! Flicker can be extreme (0.5 - 1.5) during action.
        
        Return ONLY valid JSON:
        {{
            "world_tint_hex": "#HEXCOLOR",
            "volumetric_fog_density": float,
            "key_light_color_hex": "#HEXCOLOR",
            "key_light_power_watts": float,
            "fill_light_color_hex": "#HEXCOLOR",
            "fill_light_power_watts": float,
            "rim_light_color_hex": "#HEXCOLOR",
            "rim_light_power_watts": float,
            "light_flicker_intensity": float (0.0 to 1.5),
            "cinematic_rationale": "Brief explanation"
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

        self.log("AI APIs failed. Activating Offline Procedural Lighting Math.", "WARNING")
        return self._get_procedural_fallback_lighting(context, style)

    # RULE 9 (Abstraction), RULE 11 (Procedural Gobos), RULE 12 (Kinetic Physics), RULE 13 (Sockets)
    def _generate_blender_script(self, blend_file_path, lighting_data, config):
        safe_blend_path = blend_file_path.replace("\\", "/")
        style = config.get("global_style", "realistic")
        fps = config.get("fps", 24)
        
        script_content = f"""
import bpy
import math

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return (1.0, 1.0, 1.0, 1.0)
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")
    
    # --- 1. CLEANUP OLD LIGHTS ---
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT' or obj.name.startswith("OMNI_Light_"):
            bpy.data.objects.remove(obj, do_unlink=True)

    # --- 2. AAA WORLD ATMOSPHERE ---
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
        bg_node.inputs['Strength'].default_value = 0.05 if '{style}' == 'realistic' else 0.2
    
    # Volumetric Fog (God Rays)
    fog_density = {lighting_data.get('volumetric_fog_density', 0.0)}
    if fog_density > 0.0:
        vol_node = nt.nodes.new(type="ShaderNodeVolumePrincipled")
        vol_node.inputs['Density'].default_value = fog_density
        vol_node.inputs['Anisotropy'].default_value = 0.8 # AAA God-Rays bias
        # Remove old links to volume
        for link in out_node.inputs['Volume'].links:
            nt.links.remove(link)
        nt.links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])

    # --- RULE 13: THE SOCKET PROTOCOL (Track to Action) ---
    target = bpy.data.objects.get("OMNIMATRIX_Focus_Target")
    if not target:
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1))
        target = bpy.context.active_object
        target.name = "OMNIMATRIX_Focus_Target"

    # Helper function to inject Rule 12 Kinetic Physics
    def inject_kinetic_flicker(light_obj, base_energy, intensity):
        if intensity <= 0.01: return
        light_obj.data.keyframe_insert(data_path="energy", frame=1)
        if light_obj.data.animation_data and light_obj.data.animation_data.action:
            for fc in light_obj.data.animation_data.action.fcurves:
                if fc.data_path == 'energy':
                    mod = fc.modifiers.new('NOISE')
                    mod.scale = 2.0 if '{style}' == 'anime' else 10.0 # Faster flicker for anime
                    mod.strength = base_energy * intensity # Power variance
                    mod.phase = random.uniform(0.0, 100.0) # Offset each light

    flicker_level = {lighting_data.get('light_flicker_intensity', 0.0)}

    # --- A. KEY LIGHT (Procedural Node Gobo) ---
    k_power = {lighting_data.get('key_light_power_watts', 1500.0)}
    key_data = bpy.data.lights.new(name="OMNI_Light_Key", type="SPOT")
    key_data.energy = k_power
    key_data.color = hex_to_rgb("{lighting_data.get('key_light_color_hex', '#FFFFFF')}")[:3]
    key_data.spot_size = math.radians(70)
    key_data.spot_blend = 0.8 if '{style}' == 'realistic' else 0.0 # Hard edge for anime
    
    # RULE 11: PROCEDURAL LIGHT SHADER (Gobo)
    key_data.use_nodes = True
    l_nt = key_data.node_tree
    l_emit = l_nt.nodes.get("Emission")
    if l_emit and '{style}' == 'realistic':
        # Add math noise to simulate light passing through leaves/smoke
        l_noise = l_nt.nodes.new(type="ShaderNodeTexNoise")
        l_noise.inputs['Scale'].default_value = 15.0
        l_ramp = l_nt.nodes.new(type="ShaderNodeValToRGB")
        l_ramp.color_ramp.elements[0].position = 0.4
        l_ramp.color_ramp.elements[1].position = 0.6
        l_math = l_nt.nodes.new(type="ShaderNodeMath")
        l_math.operation = 'MULTIPLY'
        l_math.inputs[1].default_value = k_power
        
        l_nt.links.new(l_noise.outputs['Fac'], l_ramp.inputs['Fac'])
        l_nt.links.new(l_ramp.outputs['Color'], l_math.inputs[0])
        l_nt.links.new(l_math.outputs['Value'], l_emit.inputs['Strength'])

    key_obj = bpy.data.objects.new(name="OMNI_Light_Key", object_data=key_data)
    bpy.context.scene.collection.objects.link(key_obj)
    key_obj.location = (4.0, -5.0, 5.0) 
    
    track = key_obj.constraints.new(type='TRACK_TO')
    track.target = target; track.track_axis = 'TRACK_NEGATIVE_Z'; track.up_axis = 'UP_Y'
    inject_kinetic_flicker(key_obj, k_power, flicker_level)

    # --- B. FILL LIGHT ---
    f_power = {lighting_data.get('fill_light_power_watts', 500.0)}
    fill_data = bpy.data.lights.new(name="OMNI_Light_Fill", type="AREA")
    fill_data.energy = f_power
    fill_data.color = hex_to_rgb("{lighting_data.get('fill_light_color_hex', '#FFFFFF')}")[:3]
    fill_data.shape = 'RECTANGLE'
    fill_data.size = 6.0
    
    fill_obj = bpy.data.objects.new(name="OMNI_Light_Fill", object_data=fill_data)
    bpy.context.scene.collection.objects.link(fill_obj)
    fill_obj.location = (-5.0, -2.0, 2.0)
    
    track = fill_obj.constraints.new(type='TRACK_TO')
    track.target = target; track.track_axis = 'TRACK_NEGATIVE_Z'; track.up_axis = 'UP_Y'
    inject_kinetic_flicker(fill_obj, f_power, flicker_level * 0.5) # Subtler flicker on fill

    # --- C. RIM LIGHT (God-Level Anime Separation) ---
    r_power = {lighting_data.get('rim_light_power_watts', 3000.0)}
    rim_data = bpy.data.lights.new(name="OMNI_Light_Rim", type="SPOT")
    rim_data.energy = r_power
    rim_data.color = hex_to_rgb("{lighting_data.get('rim_light_color_hex', '#FFFFFF')}")[:3]
    rim_data.spot_size = math.radians(45)
    rim_data.spot_blend = 0.1
    
    rim_obj = bpy.data.objects.new(name="OMNI_Light_Rim", object_data=rim_data)
    bpy.context.scene.collection.objects.link(rim_obj)
    rim_obj.location = (-1.0, 6.0, 3.0) # Placed behind
    
    track = rim_obj.constraints.new(type='TRACK_TO')
    track.target = target; track.track_axis = 'TRACK_NEGATIVE_Z'; track.up_axis = 'UP_Y'
    inject_kinetic_flicker(rim_obj, r_power, flicker_level)

    # --- ENGINE OVERRIDES ---
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    try:
        if '{style}' == 'anime':
            bpy.context.scene.eevee.use_bloom = True
            bpy.context.scene.eevee.bloom_intensity = 1.5
            bpy.context.scene.eevee.shadow_cascade_size = '2048' # Sharp shadows
        else:
            bpy.context.scene.eevee.use_gtao = True # Ambient occlusion for realistic
            bpy.context.scene.eevee.use_ssr = True # Screen space reflections
    except:
        pass # Failsafe for Blender 4.2+ (Uses Eevee Next compositor instead)

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_lighting_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_scene_lighting(self):
        self.log("Initializing Atmospheric Lighting Matrix...", "INFO")

        # RULE 7: ATOMIC HANDSHAKE
        state = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
            except: pass
                
        if state.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{state.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        self.scrub_workspace()
        config = self._load_master_config()
        blender_executable = config.get("blender_executable", "blender")
        
        master_blueprint = {}
        
        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("No 3D environments found. DoP waiting...", "WARNING")
            sys.exit(0)
            
        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                scene_name = filename.replace("_stage.blend", "").replace(".blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_vibe(scene_name)
                lighting_data = self._query_lighting_brain(scene_name, context, config)
                self.log(f"[{scene_name}] AI Logic: {lighting_data.get('cinematic_rationale', 'Applied')}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, lighting_data, config)
                
                command = [blender_executable, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                        self.log(f"AAA Lighting baked into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = lighting_data
                    else:
                        self.log(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: ATOMIC HANDSHAKE (Advance State)
        state["last_active_agent"] = self.agent_name
        # Heading to VFX Particle System Injector!
        state["next_agent"] = "Ai_Agent_23_Procedural_VFX_Injector"
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
        
        self.log(f"Atmospheric Lighting Complete! Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    baker = AiAgent22AtmosphericLightingShaderBaker()
    baker.process_scene_lighting()

# ==============================================================================
# END OF FILE
# ==============================================================================
