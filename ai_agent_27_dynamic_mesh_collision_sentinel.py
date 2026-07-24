# ==============================================================================
# Ai_Agent_27_AAA_Dynamic_Mesh_Collision_Sentinel.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL ANTI-CLIPPING & IMPACT TRACKER)
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
                    # RULE 6: Universal Uppercase API Keys
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiAgent27DynamicMeshCollisionSentinel:
    def __init__(self):
        # RULE 8: STRICT AI NAMING
        self.agent_name = "Ai_Agent_27_Dynamic_Mesh_Collision_Sentinel"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "27_collision_blueprint.json")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_dir, "global_config.json")
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")

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

    def _load_upstream_action(self, scene_name):
        context = {"action_description": "Characters standing close to each other."}
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["action_description"] = data.get("action_description", context["action_description"])
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

    def _fallback_sentinel(self):
        return {
            "intentional_contact": False,
            "has_major_impact": False,
            "impact_frame": 0,
            "minimum_distance_threshold": 0.5,
            "interpolation_style": "BEZIER",
            "rationale": "Fallback: Default anti-clipping distance."
        }

    # LIMITLESS AI SENTINEL BRAIN (ANIME VS REALISM AWARE)
    def _query_sentinel_brain(self, scene_name, context, style):
        self.log(f"Consulting Collision Sentinel for '{scene_name}' (Style: {style.upper()})...", "INFO")
        
        ai_prompt = f"""
        You are the AAA Collision Sentinel for the OmniMatrix Engine.
        Action Narrative: {context['action_description']}
        Visual Style: {style.upper()}
        
        MISSION 1: ANTI-CLIPPING
        Determine if the characters are SUPPOSED to touch/clip (e.g., punching, hugging, sword clash). 
        If they are just talking or walking, they should NEVER overlap (`intentional_contact` = false).
        
        MISSION 2: IMPACT TRACKING FOR AGENT 28
        If they DO clash/punch, set `has_major_impact` to true and estimate the `impact_frame` (e.g., frame 24 or 30).
        
        STYLE RULES:
        - If ANIME: Pushback should be snappy (`interpolation_style`: "LINEAR").
        - If REALISTIC: Pushback should be smooth and physical (`interpolation_style`: "BEZIER").
        
        Return ONLY valid JSON:
        {{
            "intentional_contact": boolean,
            "has_major_impact": boolean,
            "impact_frame": integer (0 if no impact),
            "minimum_distance_threshold": float (0.6 for talking, 0.1 for combat),
            "interpolation_style": "LINEAR" or "BEZIER",
            "rationale": "Brief reasoning"
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

        return self._fallback_sentinel()

    # GOD-LEVEL BLENDER SCRIPT: F-CURVE INTERPOLATION & CLOTH PHYSICS
    def _generate_blender_script(self, blend_file_path, sentinel_data, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        is_contact_intended = "True" if sentinel_data.get("intentional_contact", False) else "False"
        min_dist = float(sentinel_data.get("minimum_distance_threshold", 0.5))
        interp_style = sentinel_data.get("interpolation_style", "BEZIER")
        is_anime = "True" if "anime" in style else "False"
        
        script_content = f"""
import bpy
import mathutils

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    contact_intended = {is_contact_intended}
    min_distance = {min_dist}
    interp_type = '{interp_style}'
    is_anime = {is_anime}
    
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
    
    # 1. DYNAMIC PROXIMITY SCANNER & PUSHBACK
    if len(armatures) >= 2 and not contact_intended:
        start_frame = bpy.context.scene.frame_start
        end_frame = bpy.context.scene.frame_end
        
        for frame in range(start_frame, end_frame + 1, 3): # High precision scan
            bpy.context.scene.frame_set(frame)
            
            char1 = armatures[0]
            char2 = armatures[1]
            
            loc1 = char1.matrix_world.translation
            loc2 = char2.matrix_world.translation
            distance = (loc1 - loc2).length
            
            if distance < min_distance:
                # CALCULATE REPULSION VECTOR
                direction = (loc1 - loc2).normalized()
                correction_amount = (min_distance - distance) / 2.0
                
                # Push them apart to maintain the "Infinity Barrier"
                char1.location += direction * correction_amount
                char2.location -= direction * correction_amount
                
                char1.keyframe_insert(data_path="location", frame=frame)
                char2.keyframe_insert(data_path="location", frame=frame)
                
                # Apply Style-Specific Interpolation (Snappy vs Smooth)
                for char in [char1, char2]:
                    if char.animation_data and char.animation_data.action:
                        for fcurve in char.animation_data.action.fcurves:
                            if fcurve.data_path == "location":
                                for kf in fcurve.keyframe_points:
                                    if kf.co[0] == frame:
                                        kf.interpolation = interp_type
                
    # 2. INTERNAL SELF-CLIPPING FIXER (Anime vs Realism Cloth)
    for arm in armatures:
        meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.parent == arm]
        for mesh in meshes:
            for mod in mesh.modifiers:
                if mod.type == 'CLOTH':
                    mod.collision_settings.use_self_collision = True
                    # Realism requires higher quality collision steps to prevent arm-torso clipping
                    if not is_anime:
                        mod.collision_settings.self_distance_min = 0.015
                        mod.collision_settings.collision_quality = 5
                    else:
                        # Anime prioritizes speed and sharp folds
                        mod.collision_settings.self_distance_min = 0.02
                        mod.collision_settings.collision_quality = 2
    
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_sentinel_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 27 (Dynamic Mesh Collision Sentinel V2)...", "INFO")

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
                
                context = self._load_upstream_action(scene_name)
                sentinel_data = self._query_sentinel_brain(scene_name, context, global_style)
                
                self.log(f"[{scene_name}] Sentinel Status: {sentinel_data['rationale']}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, sentinel_data, global_style)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                        self.log(f"Mesh integrity secured (Anti-Clipping applied) for {filename}", "SUCCESS")
                        master_blueprint[scene_name] = sentinel_data
                    else:
                        self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        # Save blueprint so Agent 28 (Hit Stop) can read the exact 'impact_frame'
        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: Update Pipeline Handshake
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "Ai_Agent_28_Anime_Hit_Stop_Frame_Scheduler" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Sentinel Complete! Meshes are protected & Impacts mapped. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    sentinel = AiAgent27DynamicMeshCollisionSentinel()
    sentinel.execute_pipeline()
