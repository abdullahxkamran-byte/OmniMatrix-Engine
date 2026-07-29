# ==============================================================================
# Ai_Agent_31_Camera_VFX_Debris_Instancer.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL VFX & CAMERA DEBRIS)
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

class AiAgent31CameraVFXDebrisInstancer:
    def __init__(self):
        # RULE 8: STRICT AI NAMING
        self.agent_name = "Ai_Agent_31_Camera_VFX_Debris_Instancer"
        
        # RULE 2: UNIVERSAL PATH ISOLATION (No Hardcoded D:/ Drives)
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "31_camera_debris_blueprint.json")
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
        """Loads data from Agent 30 (Destruction) to align VFX perfectly."""
        context = {
            "has_destruction": False,
            "impact_frame": 0,
            "fracture_center_xyz": [0.0, 0.0, 0.0]
        }
        
        dest_file = os.path.join(self.module_c_dir, "30_destruction_blueprint.json")
        if os.path.exists(dest_file):
            try:
                with open(dest_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        scene_data = data[scene_name]
                        # Only generate debris if destruction chunk count > 0
                        context["has_destruction"] = scene_data.get("shatter_chunk_count", 0) > 0
                        context["impact_frame"] = scene_data.get("impact_frame", 24)
                        context["fracture_center_xyz"] = scene_data.get("fracture_center_xyz", [0.0, 0.0, 0.0])
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

    def _fallback_debris(self, has_impact, style, context):
        if not has_impact:
            return {
                "impact_frame": 0, "particle_count": 0, "debris_type": "none",
                "velocity_towards_camera": 0.0, "gravity_influence": 1.0, "particle_scale": 1.0,
                "rationale": "No impact. Skipped."
            }
        is_anime = "anime" in style
        return {
            "impact_frame": context.get("impact_frame", 24),
            "particle_count": 120 if is_anime else 200, 
            "epicenter_xyz": context.get("fracture_center_xyz", [0,0,0]),
            "debris_type": "sharp_shards" if is_anime else "coarse_dust",
            "velocity_towards_camera": 45.0 if is_anime else 18.0,
            "gravity_influence": 0.0 if is_anime else 1.0,
            "particle_scale": 2.5 if is_anime else 0.8,
            "rationale": "Fallback VFX applied based on global style."
        }

    # LIMITLESS AI VFX BRAIN
    def _query_debris_brain(self, scene_name, context, style):
        if not context["has_destruction"]:
            return self._fallback_debris(False, style, context)

        self.log(f"Calculating Lens-Facing VFX for '{scene_name}' (Style: {style.upper()})...", "INFO")

        ai_prompt = f"""
        You are the VFX & Sakuga Particle TD for the OmniMatrix Engine.
        Scene: {scene_name} | Style: {style.upper()}
        Impact Center: {context['fracture_center_xyz']} | Impact Frame: {context['impact_frame']}
        
        MISSION:
        Design particle debris that shoots EXACTLY towards the camera lens during impact.
        
        STYLE RULES:
        - If ANIME: `debris_type`="sharp_shards". Use ZERO gravity (`gravity_influence`: 0.0). High `velocity_towards_camera` (30.0 - 60.0) so they hit the lens instantly. Exaggerate `particle_scale` (2.0 - 4.0).
        - If REALISTIC: `debris_type`="coarse_dust". Use normal gravity (`gravity_influence`: 1.0) so debris arcs naturally. Medium velocity (10.0 - 25.0). Smaller `particle_scale` (0.5 - 1.2).
        - LIMIT `particle_count` strictly between 50 and 250 to save RAM.
        
        Return ONLY valid JSON:
        {{
            "impact_frame": {context['impact_frame']},
            "epicenter_xyz": {context['fracture_center_xyz']},
            "debris_type": "sharp_shards" or "coarse_dust",
            "particle_count": integer,
            "velocity_towards_camera": float,
            "gravity_influence": float,
            "particle_scale": float,
            "rationale": "Brief reason"
        }}
        """

        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self._clean_json_response(res_text)
                    if parsed:
                        if parsed.get("particle_count", 0) > 250: parsed["particle_count"] = 250
                        parsed["epicenter_xyz"] = context["fracture_center_xyz"]
                        return parsed
            except: pass

        return self._fallback_debris(True, style, context)

    # GOD-LEVEL BLENDER SCRIPT: CAMERA-TARGETED PARTICLES
    def _generate_blender_script(self, blend_file_path, debris_data, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        is_anime = "True" if "anime" in style else "False"
        
        script_content = f"""
import bpy
import mathutils
import math

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    count = {debris_data.get('particle_count', 0)}
    frame = {debris_data.get('impact_frame', 0)}
    vel = {debris_data.get('velocity_towards_camera', 0.0)}
    grav = {debris_data.get('gravity_influence', 1.0)}
    scale_fac = {debris_data.get('particle_scale', 1.0)}
    epicenter = {debris_data.get('epicenter_xyz', [0.0, 0.0, 0.0])}
    is_anime = {is_anime}

    if count > 0:
        cam = bpy.context.scene.camera
        if cam:
            # Cleanup previous runs
            for obj_name in ["OMNI_VFX_Emitter", "OMNI_VFX_Chunk"]:
                existing = bpy.data.objects.get(obj_name)
                if existing:
                    bpy.data.objects.remove(existing, do_unlink=True)

            # 1. CREATE INSTANCE GEOMETRY (Anime vs Realistic)
            if is_anime:
                # Anime gets sharp diamond/shards that look like speed streaks
                bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.1, depth=0.6, location=(0, 0, -10))
            else:
                # Realistic gets jagged rocks
                bpy.ops.mesh.primitive_ico_sphere_add(radius=0.15, subdivisions=2, location=(0, 0, -10))
                # Add slight displacement for rock realism
                mod = bpy.context.active_object.modifiers.new(name="RockDisplace", type='DISPLACE')
                mod.strength = 0.5
                
            debris_chunk = bpy.context.active_object
            debris_chunk.name = "OMNI_VFX_Chunk"
            debris_chunk.hide_render = True
            debris_chunk.hide_viewport = True

            # 2. CREATE EMITTER EXACTLY AT IMPACT CENTER
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=epicenter)
            emitter = bpy.context.active_object
            emitter.name = "OMNI_VFX_Emitter"
            emitter.hide_render = True
            emitter.show_instancer_for_render = False
            
            # 3. SET UP PARTICLE SYSTEM
            bpy.ops.object.particle_system_add()
            ps = emitter.particle_systems[0]
            pset = ps.settings
            
            pset.count = count
            pset.frame_start = frame
            pset.frame_end = frame + 1 # Instant burst
            pset.lifetime = 50 if is_anime else 100 # Anime particles vanish faster
            
            # Render Settings
            pset.render_type = 'OBJECT'
            pset.instance_object = debris_chunk
            pset.particle_size = scale_fac
            pset.size_random = 0.7
            
            # 4. MATH: AIM EMITTER DIRECTLY AT CAMERA LENS
            cam_loc = cam.matrix_world.translation
            emit_loc = mathutils.Vector(epicenter)
            direction = (cam_loc - emit_loc).normalized()
            
            # Rotate emitter so its Z-axis points at the camera
            rot_quat = direction.to_track_quat('Z', 'Y')
            emitter.rotation_euler = rot_quat.to_euler()
            
            # 5. VELOCITY & DYNAMICS
            pset.physics_type = 'NEWTON'
            pset.normal_factor = 0.0 
            pset.object_factor = vel # Blast speed towards camera
            pset.factor_random = vel * 0.3 # Scatter effect
            
            # If Anime, align particles to their velocity (speed lines)
            if is_anime:
                pset.use_dynamic_rotation = True
                pset.rotation_mode = 'VELOCITY'
                
            # 6. GRAVITY CONTROL
            pset.effector_weights.gravity = grav

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_debris_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 31 (Camera VFX & Debris Instancer)...", "INFO")

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
                
                if context["has_destruction"]:
                    self.log(f"[{scene_name}] Destruction Data Found. Injecting Camera VFX...", "INFO")
                    debris_data = self._query_debris_brain(scene_name, context, global_style)
                    
                    self.log(f"AI Brain: Type [{debris_data.get('debris_type')}] | Speed: {debris_data.get('velocity_towards_camera')} | Gravity: {debris_data.get('gravity_influence')}", "INFO")
                    
                    script_path = self._generate_blender_script(blend_file_path, debris_data, global_style)
                    command = [blender_executable, "-b", "-P", script_path]
                    
                    try:
                        result = subprocess.run(command, capture_output=True, text=True)
                        if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                            self.log(f"God-Level Debris VFX baked into {filename}", "SUCCESS")
                            master_blueprint[scene_name] = debris_data
                        else:
                            self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                    except Exception as e:
                        self.log(f"Execution failed: {str(e)}", "CRITICAL")
                        
                    if os.path.exists(script_path):
                        os.remove(script_path)
                else:
                    self.log(f"[{scene_name}] No impact data found. Skipping VFX.", "INFO")
                    master_blueprint[scene_name] = self._fallback_debris(False, global_style, context)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: STATE UPDATE FOR THE NEXT AGENT (Moving to Module D: Lighting or Camera Finalization?)
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "Ai_Agent_32_Atmospheric_Volumetric_Lighting_Engine" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Camera VFX Complete. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    instancer = AiAgent31CameraVFXDebrisInstancer()
    instancer.execute_pipeline()
