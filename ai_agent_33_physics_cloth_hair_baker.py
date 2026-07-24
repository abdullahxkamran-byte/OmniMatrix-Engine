# ==============================================================================
# agent_33_physics_cloth_hair_baker.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL KINETIC PHYSICS & AURA WIND)
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
                    # RULE 6: UNIVERSAL UPPERCASE API KEYS
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class Agent33PhysicsClothHairBaker:
    def __init__(self):
        # RULE 8: STRICT AI NAMING (Fixed to match Master List)
        self.agent_name = "agent_33_physics_cloth_hair_baker"
        
        # RULE 2: UNIVERSAL PATH ISOLATION (No Hardcoded Drives)
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "33_physics_blueprint.json")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_dir, "global_config.json")
        
        # RULE 6: DUAL API FAILSAFES
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        for d in [self.script_dir, self.env_dir, self.module_c_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_master_config(self):
        default_config = {"global_style": "anime", "blender_executable": "blender"}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except: pass
        return default_config

    def _load_upstream_context(self, scene_name):
        """Loads data from Master Matrix State (Rule 7)"""
        context = {
            "action_intensity": "high",
            "start_frame": 1,
            "end_frame": 72
        }
        
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["action_intensity"] = data.get("action_intensity", "high")
                    context["start_frame"] = data.get("global_start_frame", 1)
                    context["end_frame"] = data.get("global_end_frame", 72)
            except: pass
                
        return context

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

    def _fallback_physics(self, context, style):
        is_anime = "anime" in style.lower()
        return {
            "wind_strength": 3000.0 if is_anime else 800.0,
            "wind_noise": 0.5 if is_anime else 3.5, 
            "vortex_strength": 1500.0 if is_anime else 0.0, 
            "cloth_bending_stiffness": 5.0 if is_anime else 0.2, 
            "cloth_damping": 2.0 if is_anime else 10.0,
            "hair_stiffness": 0.8 if is_anime else 0.2,
            "gravity_scale": 0.6 if is_anime else 1.0 
        }

    # LIMITLESS PHYSICS AI BRAIN WITH DUAL API FAILSAFE
    def _query_physics_brain(self, scene_name, context, style):
        self.log(f"Calculating Advanced Kinetic Physics & Turbulence for '{scene_name}'...", "INFO")

        ai_prompt = f"""
        You are the Lead 3D Physics & Simulation TD for the OmniMatrix Engine.
        Scene: {scene_name} | Style: {style.upper()}
        Action Intensity: {context['action_intensity']}
        
        MISSION:
        Design cloth, hair, and wind force field parameters.
        
        STYLE RULES:
        - If ANIME: Add high `vortex_strength` (creates a circular 'power-up' aura wind). Lower `cloth_bending_stiffness` for flow, but high stiffness for sharp folds. Gravity scale should be 0.5 - 0.7 for that 'floaty' sakuga feel.
        - If REALISTIC: `vortex_strength` MUST be 0. Use high `wind_noise` (Turbulence) so cloth ripples naturally. Normal gravity (1.0). High `cloth_damping`.
        
        Return EXACTLY 1 JSON object:
        {{
            "wind_strength": float (0-5000),
            "wind_noise": float (0-10 - Turbulence amount),
            "vortex_strength": float (0-3000 - Circular aura wind),
            "cloth_bending_stiffness": float,
            "cloth_damping": float,
            "hair_stiffness": float,
            "gravity_scale": float (0.1 to 1.0)
        }}
        """

        # PRIMARY API: GEMINI
        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self._clean_json_response(res_text)
                    if parsed and "wind_strength" in parsed:
                        return parsed
            except Exception as e:
                self.log(f"Gemini API failed: {str(e)}. Switching to OpenAI Failsafe.", "WARNING")

        # FAILSAFE API: OPENAI (Rule 6 Implementation)
        if self.openai_api_key:
             try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.openai_api_key}"
                }
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a JSON-only response bot."},
                        {"role": "user", "content": ai_prompt}
                    ],
                    "temperature": 0.2
                }
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    res_text = res_data["choices"][0]["message"]["content"]
                    parsed = self._clean_json_response(res_text)
                    if parsed and "wind_strength" in parsed:
                        self.log("OpenAI Failsafe successful.", "INFO")
                        return parsed
             except Exception as e:
                 self.log(f"OpenAI API failed: {str(e)}. Triggering Hard Fallback.", "ERROR")

        return self._fallback_physics(context, style)

    # GOD-LEVEL BLENDER SCRIPT: WIND, VORTEX, TURBULENCE & SAFE BAKING
    def _generate_blender_script(self, blend_file_path, phys_data, context):
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        start_frame = int(context.get("start_frame", 1))
        # Hard limit bake to 150 frames max to prevent VRAM overflow (Colab safety)
        end_frame = min(int(context.get("end_frame", 72)), start_frame + 150)
        
        script_content = f"""
import bpy
import json

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    start_f = {start_frame}
    end_f = {end_frame}
    
    bpy.context.scene.frame_start = start_f
    bpy.context.scene.frame_end = end_f
    
    # 1. GRAVITY MANIPULATION (Rule 13: Anime float vs Realism)
    bpy.context.scene.use_gravity = True
    bpy.context.scene.gravity[2] = -9.81 * {phys_data.get("gravity_scale", 1.0)}
    
    # 2. IDEMPOTENCY: CLEANUP OLD PHYSICS FIELDS (Rule 5)
    for obj_name in ["OMNI_Wind", "OMNI_Turbulence", "OMNI_Vortex"]:
        existing = bpy.data.objects.get(obj_name)
        if existing:
            bpy.data.objects.remove(existing, do_unlink=True)
            
    # 3. CREATE DYNAMIC FORCE FIELDS
    # A. Base Wind
    bpy.ops.object.effector_add(type='WIND', location=(0, -5, 2))
    wind = bpy.context.active_object
    wind.name = "OMNI_Wind"
    wind.field.strength = {phys_data.get("wind_strength", 1000.0)}
    wind.rotation_euler = (1.5708, 0, 0) # Point forward
    
    # B. Turbulence (The "Noise" for realistic ripples)
    if {phys_data.get("wind_noise", 0.0)} > 0:
        bpy.ops.object.effector_add(type='TURBULENCE', location=(0, 0, 1))
        turb = bpy.context.active_object
        turb.name = "OMNI_Turbulence"
        turb.field.strength = {phys_data.get("wind_noise", 0.0)} * 10.0
        turb.field.size = 0.5
        
    # C. Vortex (Anime Power-Up Aura Wind)
    if {phys_data.get("vortex_strength", 0.0)} > 0:
        bpy.ops.object.effector_add(type='VORTEX', location=(0, 0, 0.5)) # Place at character feet
        vortex = bpy.context.active_object
        vortex.name = "OMNI_Vortex"
        vortex.field.strength = {phys_data.get("vortex_strength", 0.0)}
        vortex.field.shape = 'TUBE'

    # 4. APPLY PHYSICS TO MESHES & HAIR
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    for obj in meshes:
        # Cloth Modifiers
        for mod in obj.modifiers:
            if mod.type == 'CLOTH':
                mod.settings.bending_stiffness = {phys_data.get("cloth_bending_stiffness", 1.0)}
                mod.settings.damping = {phys_data.get("cloth_damping", 5.0)}
                
                # Setup Cache Frame Limits
                mod.point_cache.frame_start = start_f
                mod.point_cache.frame_end = end_f
                
                # Scrub old cache before baking
                bpy.context.view_layer.objects.active = obj
                bpy.ops.ptcache.free_bake({{"point_cache": mod.point_cache}})
                
        # Hair/Particle Modifiers
        for ps in obj.particle_systems:
            if ps.settings.type == 'HAIR' and ps.settings.use_hair_dynamics:
                ps.settings.hair_dynamics.pin_stiffness = {phys_data.get("hair_stiffness", 1.0)}
                
                ps.point_cache.frame_start = start_f
                ps.point_cache.frame_end = end_f
                
                bpy.context.view_layer.objects.active = obj
                bpy.ops.ptcache.free_bake({{"point_cache": ps.point_cache}})

    # 5. GLOBAL BAKE EXECUTION (RAM Safe)
    print(f"Starting Kinetic Physics Bake (Frames: {{start_f}} to {{end_f}})...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("OMNIMATRIX_BAKE_SUCCESS")
                                
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_physics_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 33 (Omni Kinetic Physics Baker)...", "INFO")

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

        config = self._load_master_config()
        global_style = config.get("global_style", "anime").lower()
        blender_executable = config.get("blender_executable", "blender")
        master_blueprint = {}
        
        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("No 3D environments found. Exiting...", "WARNING")
            sys.exit(0)
            
        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                scene_name = filename.replace("_stage.blend", "").replace(".blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_context(scene_name)
                self.log(f"--- Simulating Dynamics for: {scene_name} | Style: {global_style.upper()} ---", "INFO")
                
                phys_data = self._query_physics_brain(scene_name, context, global_style)
                
                self.log(f"Applied Forces -> Wind: {phys_data.get('wind_strength')} | Turbulence: {phys_data.get('wind_noise')} | Vortex: {phys_data.get('vortex_strength')}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, phys_data, context)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BAKE_SUCCESS" in result.stdout:
                        self.log(f"God-Level Physics baked and cached for {filename}", "SUCCESS")
                        master_blueprint[scene_name] = phys_data
                    else:
                        self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: STATE UPDATE
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "ai_agent_34_procedural_3d_environment_architect" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Physics Baking Complete. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    baker = Agent33PhysicsClothHairBaker()
    baker.execute_pipeline()
