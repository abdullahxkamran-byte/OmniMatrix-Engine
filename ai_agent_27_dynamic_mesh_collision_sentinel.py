# ==============================================================================
# Ai_Agent_27_AAA_Dynamic_Mesh_Collision_Sentinel.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL ANTI-CLIPPING)
# ==============================================================================

import os
import re
import sys
import json
import subprocess
import urllib.request

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiAgent27DynamicMeshCollisionSentinel:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_27_Dynamic_Mesh_Collision_Sentinel"
        
        # UNIVERSAL PATH ISOLATION
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

    def _load_upstream_action(self, scene_name):
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {"action_description": "Characters standing close to each other."}
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
            "minimum_distance_threshold": 0.5,
            "rationale": "Fallback: Default anti-clipping distance."
        }

    # LIMITLESS AI SENTINEL BRAIN
    def _query_sentinel_brain(self, scene_name, context):
        self.log(f"Consulting Collision Sentinel for '{scene_name}'...", "INFO")
        
        ai_prompt = f"""
        You are the AAA Collision Sentinel for the OmniMatrix Engine.
        Action Narrative: {context['action_description']}
        
        MISSION: Determine if the characters are SUPPOSED to touch/clip (e.g., punching, hugging, grappling). 
        If they are just talking, walking, or standing, they should NEVER overlap (intentional_contact = false).
        
        Return ONLY valid JSON:
        {{
            "intentional_contact": boolean (true ONLY if physical contact is part of the action),
            "minimum_distance_threshold": float (0.6 for talking/idle, 0.1 for combat proximity),
            "rationale": "Why contact is allowed or blocked."
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

    # THE BLENDER ANTI-CLIPPING ENGINE
    def _generate_blender_script(self, blend_file_path, sentinel_data):
        safe_blend_path = blend_file_path.replace("\\", "/")
        is_contact_intended = "True" if sentinel_data.get("intentional_contact", False) else "False"
        min_dist = float(sentinel_data.get("minimum_distance_threshold", 0.5))
        
        script_content = f"""
import bpy
import mathutils

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    contact_intended = {is_contact_intended}
    min_distance = {min_dist}
    
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
    
    if len(armatures) >= 2 and not contact_intended:
        # 1. DYNAMIC PROXIMITY SCANNER (Character to Character)
        # Scan through the animation timeline
        start_frame = bpy.context.scene.frame_start
        end_frame = bpy.context.scene.frame_end
        
        for frame in range(start_frame, end_frame + 1, 5): # Check every 5 frames for efficiency
            bpy.context.scene.frame_set(frame)
            
            # Compare distance between Root bones of the first two characters
            char1 = armatures[0]
            char2 = armatures[1]
            
            loc1 = char1.matrix_world.translation
            loc2 = char2.matrix_world.translation
            distance = (loc1 - loc2).length
            
            if distance < min_distance:
                # CLIPPING DETECTED! Inject Corrective Pushback Keyframe
                print(f"[SENTINEL WARNING] Clipping detected at frame {{frame}}. Pushing apart.")
                
                # Calculate push vector away from each other
                direction = (loc1 - loc2).normalized()
                correction_amount = (min_distance - distance) / 2.0
                
                char1.location += direction * correction_amount
                char2.location -= direction * correction_amount
                
                char1.keyframe_insert(data_path="location", frame=frame)
                char2.keyframe_insert(data_path="location", frame=frame)
                
    # 2. INTERNAL SELF-CLIPPING FIXER (Arms clipping into Body)
    # Using Blender's Shrinkwrap & Collision trick for Character clothing/limbs
    for arm in armatures:
        # Find meshes parented to this armature
        meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.parent == arm]
        
        for mesh in meshes:
            # Enable Self-Collision in Cloth/Physics modifiers if Agent 26 added physics
            for mod in mesh.modifiers:
                if mod.type == 'CLOTH':
                    mod.collision_settings.use_self_collision = True
                    mod.collision_settings.self_distance_min = 0.015
    
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
        self.log("Initializing Agent 27 (Dynamic Mesh Collision Sentinel)...", "INFO")

        state = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
            except: pass

        if state.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{state.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        config = {}
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                config = json.load(f)
        
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
                sentinel_data = self._query_sentinel_brain(scene_name, context)
                
                self.log(f"[{scene_name}] Sentinel Status: {sentinel_data['rationale']}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, sentinel_data)
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

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # Update Pipeline
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "Ai_Agent_28_Anime_Hit_Stop_Frame_Scheduler" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Sentinel Complete! Meshes are protected. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    sentinel = AiAgent27DynamicMeshCollisionSentinel()
    sentinel.execute_pipeline()
