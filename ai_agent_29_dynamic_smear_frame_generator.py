# ==============================================================================
# Ai_Agent_29_Dynamic_Smear_Frame_Generator.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL MOTION & SMEAR DIRECTOR)
# ==============================================================================

import os
import re
import sys
import json
import subprocess
import urllib.request
import urllib.error
import math

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    # RULE 6: UNIVERSAL UPPERCASE FIX
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiAgent29DynamicSmearFrameGenerator:
    def __init__(self):
        # RULE 8: STRICT AI NAMING
        self.agent_name = "Ai_Agent_29_Dynamic_Smear_Frame_Generator"
        
        # RULE 2: UNIVERSAL PATH ISOLATION (No Hardcoded D:/ Drives)
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "29_motion_dynamics_blueprint.json")
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
        context = {
            "action_description": "Standard high-speed movement",
            "fast_motion_frame": 24,
            "impact_frame": 0
        }
        
        # Load Narrative Context
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["action_description"] = data.get("action_description", context["action_description"])
            except: pass

        # Load Animation / Impact Data (From Agent 27 & 28)
        collision_file = os.path.join(self.module_c_dir, "27_collision_blueprint.json")
        if os.path.exists(collision_file):
            try:
                with open(collision_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        context["impact_frame"] = data[scene_name].get("impact_frame", 0)
                        context["fast_motion_frame"] = max(1, context["impact_frame"] - 2) # Motion peaks right before impact
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

    def _fallback_motion(self, frame, style):
        is_anime = "anime" in style
        return {
            "motion_handling_mode": "stylized_smear" if is_anime else "realistic_blur",
            "target_frame": frame,
            "camera_shutter_speed": 0.2 if is_anime else 0.5,
            "motion_blur_steps": 2 if is_anime else 8,
            "mesh_stretch_factor": 2.5 if is_anime else 0.0,
            "ghost_trail_count": 3 if is_anime else 0,
            "rationale": "Fallback applied based on global style."
        }

    # LIMITLESS AI MOTION BRAIN
    def _query_motion_brain(self, scene_name, context, style):
        self.log(f"Calculating Motion & Smear Vectors for '{scene_name}' (Style: {style.upper()})...", "INFO")
        
        ai_prompt = f"""
        You are the Motion Dynamics & Sakuga Technical Director for the OmniMatrix Engine.
        Scene: {scene_name} | Style: {style.upper()} | Action: {context['action_description']}
        Fast Motion Target Frame: {context['fast_motion_frame']}
        
        MISSION:
        Determine how high-speed motion should be rendered.
        - If REALISTIC/CINEMATIC: Use 'realistic_blur'. High shutter speed, NO stretching, NO ghosting.
        - If ANIME/SAKUGA: Use 'stylized_smear'. Exaggerate `mesh_stretch_factor` (1.5 to 3.0), and add `ghost_trail_count` (2 to 5) for that classic Naruto/DragonBall after-image effect.
        
        Return ONLY valid JSON:
        {{
            "motion_handling_mode": "stylized_smear" or "realistic_blur",
            "target_frame": {context['fast_motion_frame']},
            "camera_shutter_speed": float,
            "motion_blur_steps": integer,
            "mesh_stretch_factor": float,
            "ghost_trail_count": integer,
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
                    if parsed: return parsed
            except: pass

        return self._fallback_motion(context["fast_motion_frame"], style)

    # GOD-LEVEL BLENDER SCRIPT: VELOCITY-ALIGNED SMEAR & GHOSTING
    def _generate_blender_script(self, blend_file_path, motion_data, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        is_anime = "True" if "anime" in style else "False"
        
        script_content = f"""
import bpy
import mathutils

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    mode = "{motion_data.get('motion_handling_mode', 'realistic_blur')}"
    target_frame = {motion_data.get('target_frame', 24)}
    shutter = {motion_data.get('camera_shutter_speed', 0.5)}
    steps = {motion_data.get('motion_blur_steps', 4)}
    stretch_factor = {motion_data.get('mesh_stretch_factor', 0.0)}
    ghost_count = {motion_data.get('ghost_trail_count', 0)}
    is_anime = {is_anime}

    # 1. BASE CAMERA MOTION BLUR
    bpy.context.scene.render.use_motion_blur = True
    bpy.context.scene.render.motion_blur_shutter = shutter
    if hasattr(bpy.context.scene, "eevee") and hasattr(bpy.context.scene.eevee, "use_motion_blur"):
        bpy.context.scene.eevee.use_motion_blur = True
        bpy.context.scene.eevee.motion_blur_steps = steps

    # 2. AAA ANIME VELOCITY-ALIGNED SMEAR & GHOSTING
    if mode == "stylized_smear" and (stretch_factor > 0 or ghost_count > 0):
        armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
        
        for arm in armatures:
            # A. Calculate Velocity Vector (Where is it moving?)
            bpy.context.scene.frame_set(target_frame - 2)
            loc_prev = arm.matrix_world.translation.copy()
            bpy.context.scene.frame_set(target_frame)
            loc_curr = arm.matrix_world.translation.copy()
            
            velocity = loc_curr - loc_prev
            speed = velocity.length
            
            if speed > 0.1: # Only smear if actually moving fast
                direction = velocity.normalized()
                
                # B. Create Axis Empty for Directional Deform
                bpy.ops.object.empty_add(type='ARROWS', location=loc_curr)
                smear_empty = bpy.context.active_object
                smear_empty.name = f"OMNI_SMEAR_AXIS_{{arm.name}}"
                # Align empty to velocity vector
                smear_empty.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
                
                # Setup Ghost Trail Empty
                bpy.ops.object.empty_add(type='PLAIN_AXES', location=loc_curr - (velocity * 0.5))
                ghost_empty = bpy.context.active_object
                ghost_empty.name = f"OMNI_GHOST_AXIS_{{arm.name}}"
                
                # C. Apply Modifiers to Child Meshes
                meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.parent == arm]
                for mesh in meshes:
                    
                    # --- SMEAR DEFORM ---
                    if stretch_factor > 0:
                        mod_smear = mesh.modifiers.new(name="Omni_Velocity_Smear", type='SIMPLE_DEFORM')
                        mod_smear.deform_method = 'STRETCH'
                        mod_smear.origin = smear_empty
                        
                        # Keyframe it so it ONLY happens on the fast frames
                        mod_smear.factor = 0.0
                        mod_smear.keyframe_insert(data_path="factor", frame=target_frame - 2)
                        
                        mod_smear.factor = stretch_factor * speed # Stretch scales with speed!
                        mod_smear.keyframe_insert(data_path="factor", frame=target_frame)
                        
                        mod_smear.factor = 0.0
                        mod_smear.keyframe_insert(data_path="factor", frame=target_frame + 2)
                        
                    # --- GHOST TRAILS (ARRAY) ---
                    if ghost_count > 0:
                        mod_ghost = mesh.modifiers.new(name="Omni_Ghost_Trails", type='ARRAY')
                        mod_ghost.count = ghost_count
                        mod_ghost.use_relative_offset = False
                        mod_ghost.use_object_offset = True
                        mod_ghost.offset_object = ghost_empty
                        
                        # Keyframe ghosting visibility
                        mod_ghost.show_viewport = False
                        mod_ghost.show_render = False
                        mod_ghost.keyframe_insert(data_path="show_render", frame=target_frame - 2)
                        mod_ghost.keyframe_insert(data_path="show_viewport", frame=target_frame - 2)
                        
                        mod_ghost.show_viewport = True
                        mod_ghost.show_render = True
                        mod_ghost.keyframe_insert(data_path="show_render", frame=target_frame)
                        mod_ghost.keyframe_insert(data_path="show_viewport", frame=target_frame)
                        
                        mod_ghost.show_viewport = False
                        mod_ghost.show_render = False
                        mod_ghost.keyframe_insert(data_path="show_render", frame=target_frame + 2)
                        mod_ghost.keyframe_insert(data_path="show_viewport", frame=target_frame + 2)

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_smear_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 29 (Dynamic Smear Frame Generator)...", "INFO")

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
                
                self.log(f"[{scene_name}] Generating Motion Dynamics Profile...", "INFO")
                motion_data = self._query_motion_brain(scene_name, context, global_style)
                
                self.log(f"AI Decision: Mode [{motion_data.get('motion_handling_mode')}] | Stretch: {motion_data.get('mesh_stretch_factor')} | Ghosts: {motion_data.get('ghost_trail_count')}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, motion_data, global_style)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                        self.log(f"Smear frames and Motion Blur baked into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = motion_data
                    else:
                        self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: STATE UPDATE FOR THE NEXT AGENT
        state["last_active_agent"] = self.agent_name
        # Heading to Environment Fracturing next!
        state["next_agent"] = "Ai_Agent_30_Procedural_Environment_Fracture_Engine" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Motion Dynamics Complete. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    generator = AiAgent29DynamicSmearFrameGenerator()
    generator.execute_pipeline()
