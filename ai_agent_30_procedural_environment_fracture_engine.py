# ==============================================================================
# Ai_Agent_30_Procedural_Environment_Fracture_Engine.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL DESTRUCTION & PHYSICS)
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

class AiAgent30ProceduralEnvironmentFractureEngine:
    def __init__(self):
        # RULE 8: STRICT AI NAMING
        self.agent_name = "Ai_Agent_30_Procedural_Environment_Fracture_Engine"
        
        # RULE 2: UNIVERSAL PATH ISOLATION (No hardcoded D:/ drives)
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "30_destruction_blueprint.json")
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
        """Loads visual style, heavy collision impact data, and exact XYZ coords."""
        context = {
            "has_heavy_impact": False,
            "impact_frame": 0,
            "impact_force": 0.0,
            "impact_point": [0.0, 0.0, 0.0] # Default center
        }
        
        # Load Collision Data (from Agent 27)
        collision_file = os.path.join(self.module_c_dir, "27_collision_blueprint.json")
        if os.path.exists(collision_file):
            try:
                with open(collision_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        scene_data = data[scene_name]
                        context["has_heavy_impact"] = scene_data.get("has_major_impact", False)
                        context["impact_frame"] = scene_data.get("impact_frame", 0)
                        
                        # Derive a pseudo-force based on style/distance
                        distance = scene_data.get("minimum_distance_threshold", 0.5)
                        context["impact_force"] = 100.0 if distance < 0.2 else 40.0
                        
                        # If Agent 27 exported coordinates, use them, otherwise default to origin
                        context["impact_point"] = scene_data.get("impact_point_coordinates", [0.0, 0.0, 0.0])
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

    def _fallback_destruction(self, has_impact, style, context):
        if not has_impact:
            return {
                "impact_frame": 0, "shatter_chunk_count": 0, "physics_behavior": "none",
                "fracture_center_xyz": [0,0,0], "debris_mass_kg": 0.0, "explosion_strength": 0,
                "rationale": "No heavy impact detected. Environment kept intact."
            }
            
        is_anime = "anime" in style
        return {
            "impact_frame": context.get("impact_frame", 24),
            "shatter_chunk_count": 35 if is_anime else 60, 
            "physics_behavior": "anti_gravity_float" if is_anime else "heavy_gravity_crumble",
            "fracture_center_xyz": context.get("impact_point", [0, 0, 0]),
            "debris_mass_kg": 5.0 if is_anime else 25.0,
            "explosion_strength": 5000 if is_anime else 2000,
            "rationale": "Fallback standard fracture applied based on style."
        }

    # LIMITLESS AI DESTRUCTION BRAIN
    def _query_destruction_brain(self, scene_name, context, style):
        if not context["has_heavy_impact"]:
            return self._fallback_destruction(False, style, context)

        self.log(f"Calculating Destruction & Fracture Mechanics for '{scene_name}' (Style: {style.upper()})...", "INFO")

        ai_prompt = f"""
        You are the Procedural Destruction TD for the OmniMatrix Engine.
        Scene: {scene_name} | Style: {style.upper()} | Impact Force: {context['impact_force']}
        
        MISSION:
        Design the physical destruction of the environment upon impact at Frame {context['impact_frame']}.
        
        STYLE RULES:
        - If ANIME: `physics_behavior` MUST BE "anti_gravity_float". Use extreme `explosion_strength` (e.g., 8000), lighter `debris_mass_kg` (2.0 - 5.0), and max 40 chunks to keep the silhouette clean.
        - If REALISTIC/CINEMATIC: `physics_behavior` MUST BE "heavy_gravity_crumble". Use moderate explosion (1500 - 3000), heavy mass (20.0+), and higher chunks (50 - 70).
        - HARD LIMIT: `shatter_chunk_count` must NEVER exceed 75 to prevent RAM crashes.
        
        Return ONLY valid JSON:
        {{
            "impact_frame": {context['impact_frame']},
            "shatter_chunk_count": integer,
            "physics_behavior": "anti_gravity_float" or "heavy_gravity_crumble",
            "debris_mass_kg": float,
            "explosion_strength": float,
            "rationale": "Brief reason"
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
                    if parsed:
                        # ENFORCE HARD SAFEGUARD
                        if parsed.get("shatter_chunk_count", 0) > 75:
                            parsed["shatter_chunk_count"] = 75
                        parsed["fracture_center_xyz"] = context["impact_point"]
                        return parsed
            except: pass

        return self._fallback_destruction(True, style, context)

    # GOD-LEVEL BLENDER SCRIPT: DYNAMIC FORCE FIELDS & RIGID BODIES
    def _generate_blender_script(self, blend_file_path, dest_data, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        is_anime = "True" if "anime" in style else "False"
        
        script_content = f"""
import bpy
import addon_utils

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    chunks = {dest_data.get('shatter_chunk_count', 0)}
    frame = {dest_data.get('impact_frame', 0)}
    behavior = "{dest_data.get('physics_behavior', 'none')}"
    mass = {dest_data.get('debris_mass_kg', 1.0)}
    explosion_power = {dest_data.get('explosion_strength', 0.0)}
    impact_xyz = {dest_data.get('fracture_center_xyz', [0,0,0])}

    if chunks > 0 and frame > 0:
        # 1. Enable Cell Fracture Addon safely
        if not addon_utils.check("object_fracture_cell")[0]:
            addon_utils.enable("object_fracture_cell")
            
        # Ensure Scene has a Rigid Body World setup
        if not bpy.context.scene.rigidbody_world:
            bpy.ops.rigidbody.world_add()

        # 2. TARGET IDENTIFICATION (Find Ground/Floor)
        env_meshes = [
            obj for obj in bpy.context.scene.objects 
            if obj.type == 'MESH' 
            and not (obj.name.startswith("OMNI_CHAR") or "cell" in obj.name.lower())
            and ("floor" in obj.name.lower() or "ground" in obj.name.lower() or "wall" in obj.name.lower())
        ]
        
        if not env_meshes:
            # Fallback: Largest flat mesh in the scene
            env_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and not obj.parent and not obj.name.startswith("OMNI_")]

        if env_meshes:
            target_obj = env_meshes[0]
            bpy.context.view_layer.objects.active = target_obj
            target_obj.select_set(True)
            
            # 3. APPLY CELL FRACTURE
            # We use an exact source limit to prevent overloading RAM
            bpy.ops.object.add_fracture_cell_objects(source_limit=chunks, use_materials=True)
            
            target_obj.hide_render = True
            target_obj.hide_viewport = True
            
            # 4. RIGID BODY KINEMATIC SETUP
            bpy.ops.object.select_all(action='DESELECT')
            fractured_chunks = [obj for obj in bpy.context.scene.objects if target_obj.name + "_cell" in obj.name]
            
            for chunk in fractured_chunks:
                chunk.select_set(True)
                bpy.context.view_layer.objects.active = chunk
                
                if not chunk.rigid_body:
                    bpy.ops.rigidbody.object_add()
                
                chunk.rigid_body.mass = mass
                chunk.rigid_body.type = 'ACTIVE'
                chunk.rigid_body.collision_shape = 'CONVEX_HULL'
                chunk.rigid_body.kinematic = True # Locked in place
                
                # Release physics EXACTLY on impact frame
                chunk.rigid_body.keyframe_insert(data_path="kinematic", frame=frame - 1)
                chunk.rigid_body.kinematic = False
                chunk.rigid_body.keyframe_insert(data_path="kinematic", frame=frame)
                
            # 5. INVISIBLE EXPLOSIVE FORCE FIELD
            bpy.ops.object.effector_add(type='FORCE', location=tuple(impact_xyz))
            bomb = bpy.context.active_object
            bomb.name = "OMNI_IMPACT_BOMB"
            bomb.field.shape = 'POINT'
            bomb.field.strength = 0.0
            
            # Keyframe explosion: 0 -> MAX -> 0
            bomb.field.keyframe_insert(data_path="strength", frame=frame - 1)
            bomb.field.strength = explosion_power
            bomb.field.keyframe_insert(data_path="strength", frame=frame)
            bomb.field.strength = 0.0
            bomb.field.keyframe_insert(data_path="strength", frame=frame + 2)
                
            # 6. SAKUGA ANTI-GRAVITY MANIPULATION (ANIME ONLY)
            scene = bpy.context.scene
            if behavior == "anti_gravity_float":
                scene.use_gravity = True
                # Normal gravity before hit
                scene.gravity[2] = -9.81
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame - 1)
                
                # Zero gravity / Slight lift during hit (Chunks float up slowly)
                scene.gravity[2] = 2.0 
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame)
                
                # Slam back down after a few frames
                scene.gravity[2] = 2.0
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame + 30)
                scene.gravity[2] = -20.0 # Heavy slam
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame + 35)

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_destruction_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 30 (Procedural Environment Fracture Engine)...", "INFO")

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
                
                if context["has_heavy_impact"]:
                    self.log(f"[{scene_name}] Heavy Impact Detected. Initiating Fracture Protocol...", "INFO")
                    dest_data = self._query_destruction_brain(scene_name, context, global_style)
                    
                    self.log(f"AI Decision: Behavior [{dest_data.get('physics_behavior')}] | Chunks: {dest_data.get('shatter_chunk_count')} | Explosive Force: {dest_data.get('explosion_strength')}", "INFO")
                    
                    script_path = self._generate_blender_script(blend_file_path, dest_data, global_style)
                    command = [blender_executable, "-b", "-P", script_path]
                    
                    try:
                        result = subprocess.run(command, capture_output=True, text=True)
                        if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                            self.log(f"God-Level Destruction Physics baked into {filename}", "SUCCESS")
                            master_blueprint[scene_name] = dest_data
                        else:
                            self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                    except Exception as e:
                        self.log(f"Execution failed: {str(e)}", "CRITICAL")
                        
                    if os.path.exists(script_path):
                        os.remove(script_path)
                else:
                    self.log(f"[{scene_name}] No heavy impacts detected. Environment preserved.", "INFO")
                    master_blueprint[scene_name] = self._fallback_destruction(False, global_style, context)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: STATE UPDATE FOR THE NEXT AGENT
        state["last_active_agent"] = self.agent_name
        # After destruction, we need VFX (Auras, Dust, Particles!)
        state["next_agent"] = "Ai_Agent_31_VFX_Particle_and_Aura_Generator" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Destruction Dynamics Complete. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    engine = AiAgent30ProceduralEnvironmentFractureEngine()
    engine.execute_pipeline()
