# ==============================================================================
# Ai_Agent_26_Infinity_Kinetic_Rig_Puppeteer.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL V3.0 INFINITY)
# ==============================================================================

import os
import re
import sys
import json
import math
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

class AiAgent26InfinityKineticRigPuppeteer:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_26_Infinity_Kinetic_Rig_Puppeteer"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "26_animation_blueprint.json")
        
        # System States (RULE 7)
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_dir, "global_config.json")
        
        # APIs
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

    def _load_upstream_action(self, scene_name):
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {
            "vibe_genre": "General",
            "action_description": "Characters stand in idle pose.",
            "characters_in_scene": ["Character 1"]
        }
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["vibe_genre"] = data.get("genre_vibe", "General")
                    context["action_description"] = data.get("action_description", context["action_description"])
                    if "characters_in_scene" in data and isinstance(data["characters_in_scene"], list):
                        context["characters_in_scene"] = data["characters_in_scene"]
            except: pass
        return context

    def _clean_json_response(self, raw_text):
        try:
            cleaned = re.sub(r'```(?:json)?\n(.*?)```', r'\1', raw_text, flags=re.DOTALL).strip()
            return json.loads(cleaned)
        except:
            start = raw_text.find("[") if "[" in raw_text else raw_text.find("{")
            end = raw_text.rfind("]") if "]" in raw_text else raw_text.rfind("}")
            if start != -1 and end != -1:
                try: return json.loads(raw_text[start:end+1])
                except: pass
            return None

    def _fallback_animation(self, chars):
        blueprint = []
        for i, char in enumerate(chars):
            blueprint.append({
                "character_index": i,
                "action_intent": "Idle Fallback",
                "root_translation": [0.0, 0.0, 0.0],
                "semantic_bones": {
                    "spine": [5, 0, 0], "arm_L": [10, 0, 5], "arm_R": [10, 0, -5]
                },
                "physics_intensity": 0.2
            })
        return blueprint

    # LIMITLESS MULTI-ACTOR CHOREOGRAPHY AI
    def _query_choreographer_brain(self, scene_name, context, style):
        self.log(f"Calculating Multi-Actor Kinetic Choreography for '{scene_name}'...", "INFO")
        
        char_list = json.dumps(context["characters_in_scene"])
        ai_prompt = f"""
        You are the AAA Lead Choreographer / Animation Director.
        Scene: '{scene_name}' | Style: '{style.upper()}'
        Action Narrative: {context['action_description']}
        Characters involved: {char_list}
        
        MISSION: Choreograph a synchronized frame for ALL characters. 
        If Character 0 attacks, Character 1 must dodge, block, or take damage.
        Provide Semantic Bone Rotations (in degrees: [X, Y, Z]). We use Semantic Names (spine, head, arm_L, arm_R, leg_L, leg_R) so it works on ANY rig.
        
        Return EXACTLY a JSON ARRAY of objects (one for each character):
        [
            {{
                "character_index": 0,
                "action_intent": "Jumping punch forward",
                "root_translation": [0.0, 1.5, 2.0], 
                "semantic_bones": {{
                    "spine": [20, 0, 0],
                    "head": [-10, 0, 0],
                    "arm_R": [90, 0, -45],
                    "arm_L": [20, 0, 30],
                    "leg_R": [-45, 0, 0],
                    "leg_L": [15, 0, 0]
                }},
                "physics_intensity": 1.0 (High intensity triggers cloth/hair physics)
            }}
        ]
        """

        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                with urllib.request.urlopen(req, timeout=40) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self._clean_json_response(res_text)
                    if isinstance(parsed, list): return parsed
            except: pass

        self.log("AI API failed. Deploying Procedural Fallback Choreography.", "WARNING")
        return self._fallback_animation(context["characters_in_scene"])

    # LIMITLESS PYTHON BLENDER SCRIPT (Semantic Mapper + Physics)
    def _generate_blender_script(self, blend_file_path, choreo_data, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        choreo_json = json.dumps(choreo_data)
        
        script_content = f"""
import bpy
import math
import json

def find_semantic_bone(armature, semantic_name):
    # DYNAMIC RIG MAPPER: Finds correct bone regardless of skeleton type (Mixamo, Rigify, VRoid)
    bone_keywords = {{
        "spine": ["spine", "chest", "torso", "pelvis"],
        "head": ["head", "neck"],
        "arm_L": ["arm_l", "leftarm", "arm.l", "shoulder_l", "shoulder.l", "left_arm"],
        "arm_R": ["arm_r", "rightarm", "arm.r", "shoulder_r", "shoulder.r", "right_arm"],
        "leg_L": ["leg_l", "leftleg", "leg.l", "upleg_l", "thigh_l", "left_leg"],
        "leg_R": ["leg_r", "rightleg", "leg.r", "upleg_r", "thigh_r", "right_leg"]
    }}
    
    keywords = bone_keywords.get(semantic_name, [semantic_name.lower()])
    
    for bone in armature.pose.bones:
        b_name = bone.name.lower()
        if any(kw in b_name for kw in keywords):
            return bone
    return None

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    choreography = json.loads('''{choreo_json}''')
    global_style = "{style}"
    
    # Target frame setup
    frame_num = 24
    bpy.context.scene.frame_set(frame_num)
    
    # Setup Interpolation (Anime On-Twos vs Pixar Smooth)
    interp_mode = 'CONSTANT' if 'anime' in global_style else 'BEZIER'

    # Find ALL armatures associated with OMNI_CHAR_ index
    for char_data in choreography:
        idx = char_data.get("character_index", 0)
        
        # Limitless Target Finder (Agent 23 integration)
        target_rig = None
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE' and f"OMNI_CHAR_{{idx}}" in obj.name:
                target_rig = obj
                break
                
        if not target_rig:
            # Fallback if Agent 23 used a different naming scheme, grab by index
            armatures = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE']
            if len(armatures) > idx:
                target_rig = armatures[idx]
                
        if target_rig:
            print(f"Animating Actor {{idx}}: {{target_rig.name}}")
            
            bpy.context.view_layer.objects.active = target_rig
            bpy.ops.object.mode_set(mode='POSE')
            
            # 1. Root Translation
            root_trans = char_data.get("root_translation", [0,0,0])
            target_rig.location = (target_rig.location.x + root_trans[0], target_rig.location.y + root_trans[1], target_rig.location.z + root_trans[2])
            target_rig.keyframe_insert(data_path="location", frame=frame_num)
            
            # 2. Semantic Bone Rotation
            semantic_bones = char_data.get("semantic_bones", {{}})
            for s_name, rot_degrees in semantic_bones.items():
                bone = find_semantic_bone(target_rig, s_name)
                if bone:
                    bone.rotation_mode = 'XYZ'
                    bone.rotation_euler = (math.radians(rot_degrees[0]), math.radians(rot_degrees[1]), math.radians(rot_degrees[2]))
                    bone.keyframe_insert(data_path="rotation_euler", frame=frame_num)

            # 3. LIMITLESS PHYSICS (Procedural Secondary Animation - Rule 12)
            physics_int = float(char_data.get("physics_intensity", 0.0))
            if physics_int > 0.0:
                physics_keywords = ["hair", "cape", "cloth", "tail", "breast", "skirt"]
                for bone in target_rig.pose.bones:
                    if any(pk in bone.name.lower() for pk in physics_keywords):
                        bone.rotation_mode = 'XYZ'
                        # Add base keyframe
                        bone.keyframe_insert(data_path="rotation_euler", frame=frame_num)
                        
                        # Apply Kinetic Jiggle (F-Curve Noise)
                        if target_rig.animation_data and target_rig.animation_data.action:
                            for fc in target_rig.animation_data.action.fcurves:
                                if fc.data_path == f'pose.bones["{{bone.name}}"].rotation_euler':
                                    # Clear old modifiers
                                    for mod in fc.modifiers:
                                        fc.modifiers.remove(mod)
                                    # Inject Wind/Jiggle Noise
                                    mod = fc.modifiers.new('NOISE')
                                    mod.scale = 10.0 / (physics_int + 0.1)
                                    mod.strength = 0.5 * physics_int
                                    mod.phase = float(idx * 10) # Offset per character so they don't jiggle identically

            # 4. Enforce Global Interpolation Rules
            if target_rig.animation_data and target_rig.animation_data.action:
                for fcurve in target_rig.animation_data.action.fcurves:
                    for kf in fcurve.keyframe_points:
                        kf.interpolation = interp_mode
                        
            bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_infinity_animator.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 26 (Infinity Kinetic Puppeteer)...", "INFO")

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
                choreo_data = self._query_choreographer_brain(scene_name, context, global_style)
                
                self.log(f"[{scene_name}] Generating Sync Choreography for {len(choreo_data)} Actors...", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, choreo_data, global_style)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                        self.log(f"Infinity Animation & Physics injected into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = choreo_data
                    else:
                        self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # PROCEED TO CAMERAS & LIGHTING (Agent 21 & 22 will attach to these animated rigs)
        state["last_active_agent"] = self.agent_name
        # Final pipeline step in Heavy Infantry before Rendering!
        state["next_agent"] = "Ai_Agent_27_VFX_Particle_Injector"
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Infinity Animation Complete! Characters are Alive. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    animator = AiAgent26InfinityKineticRigPuppeteer()
    animator.execute_pipeline()

# ==============================================================================
# END OF FILE
# ==============================================================================
