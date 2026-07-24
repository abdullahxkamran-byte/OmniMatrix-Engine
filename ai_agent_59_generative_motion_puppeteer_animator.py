# ==============================================================================
# Ai_Agent_59_Omni_Motion_Puppeteer_Director.py
# MODULE H: Omni Generative Matrix (AAA Animation Engine)
# ==============================================================================

import os
import sys
import json
import re
import math
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

class AiAgent59OmniMotionPuppeteerDirector:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_59_Omni_Motion_Puppeteer_Director"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_root = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.module_h_dir = os.path.join(self.workspace_root, "Module_H_Generative")
        
        # Upstream Inputs
        self.vision_outputs_dir = os.path.join(self.module_h_dir, "outputs_vision_layers")
        self.script_dir = os.path.join(self.workspace_root, "Module_A_Scripting") # Adjusted to Matrix Standard
        self.inputs_dir = os.path.join(self.module_h_dir, "rigged_assets")
        self.input_rig_blueprint = os.path.join(self.inputs_dir, "58_master_rig_blueprint.json")
        
        # Outputs
        self.outputs_dir = os.path.join(self.module_h_dir, "animated_assets")
        self.output_motion_blueprint = os.path.join(self.outputs_dir, "59_master_motion_blueprint.json")
        
        # System States
        self.state_file = os.path.join(self.workspace_root, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_root, "global_config.json")
        
        # API Keys
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        self._initialize_directories()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _initialize_directories(self):
        for d in [self.workspace_root, self.module_h_dir, self.inputs_dir, self.outputs_dir, self.script_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    # RULE 3: IDEMPOTENCY SCRUBBING
    def scrub_workspace(self):
        self.log("Scrubbing legacy animation data to ensure idempotency...", "INFO")
        for filename in os.listdir(self.outputs_dir):
            file_path = os.path.join(self.outputs_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                self.log(f"Failed to delete {file_path}. Reason: {e}", "WARNING")

    # RULE 4: LIMITLESS FLUIDITY
    def load_global_config(self):
        default_config = {
            "animation_style": "anime", # Options: anime (stepped/snappy), realistic (bezier/smooth)
            "fps": 24,
            "blender_executable": "blender"
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception:
                pass
        return default_config

    # RULE 5: BULLETPROOF JSON CLEANER
    def clean_json_response(self, raw_response):
        try:
            cleaned = re.sub(r'```(?:json)?\n(.*?)```', r'\1', raw_response, flags=re.DOTALL)
            cleaned = cleaned.strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            start = raw_response.find("{")
            end = raw_response.rfind("}")
            if start != -1 and end != -1:
                try: return json.loads(raw_response[start:end+1])
                except: pass
            return None

    def _get_scene_action(self, scene_name):
        """Fetches the narrative action intent for this specific scene."""
        script_file = os.path.join(self.script_dir, f"{scene_name}_action.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    return json.load(f).get("action_description", "Breathing heavily in battle stance.")
            except: pass
        return "Aggressive battle stance, breathing heavily, preparing to attack."

    # RULE 10: 100% OFFLINE AUTONOMY FALLBACK (Math-Based Action Synthesis)
    def _get_procedural_fallback_motion(self, action_script):
        self.log("Engaging Procedural Math Motion Synthesizer...", "STATUS")
        action_lower = action_script.lower()
        
        # Mathematical Sine Wave Generator for Offline limits
        kf_data = []
        frames = 60
        for f in range(1, frames + 1):
            t = f / frames
            
            # Procedural logic based on text
            if "run" in action_lower or "dash" in action_lower:
                # Fast run cycle math
                arm_l = math.sin(t * math.pi * 4) * 45
                leg_l = math.cos(t * math.pi * 4) * 45
                kf_data.append({"frame": f, "bones": {"Arm_L": [arm_l, 0, 0], "Arm_R": [-arm_l, 0, 0], "Leg_L": [leg_l, 0, 0], "Leg_R": [-leg_l, 0, 0], "Spine": [15, 0, 0]}})
            elif "punch" in action_lower or "attack" in action_lower:
                # Anticipation and Impact math
                if f < 15: arm_r = -30 # wind up
                elif f < 20: arm_r = 80 # strike
                else: arm_r = 80 - (f-20) # follow through
                kf_data.append({"frame": f, "bones": {"Arm_R": [arm_r, 0, 0], "Spine": [arm_r/4, 0, 0]}})
            else:
                # Breathing / Idle loop math
                breath = math.sin(t * math.pi * 2) * 5
                kf_data.append({"frame": f, "bones": {"Root": [0,0,0], "Spine": [breath, 0, 0], "Arm_L": [10, 20 + breath, 0], "Arm_R": [10, -20 - breath, 0]}})
                
        return {"keyframes": kf_data}

    # RULE 6: QUAD-CORE FALLBACK MATRIX FOR MOTION GENERATION
    def _query_omni_motion(self, char_name, bone_count, action_script, config):
        """Quad-Core Brain: Translates narrative into numerical AAA keyframes."""
        ai_prompt = f"""
        You are a MAPPA/AAA Studio Lead Animator. Create a dynamic, REALISTIC 60-frame animation loop for '{char_name}'.
        Character has a custom limitless rig with {bone_count} bones. 
        CRITICAL TARGET ACTION: '{action_script}'
        
        ANIMATION PRINCIPLES REQUIRED:
        1. Anticipation & Impact: The action MUST have wind-up and a powerful release frame.
        2. Rotation limits: Return Euler angles (degrees) relative to the bone's rest pose.
        
        Provide keyframes for major bones (e.g., Spine, Arm_L, Arm_R, Leg_L, Leg_R, Jaw, Head).
        Return ONLY valid JSON. Format exactly like:
        {{
          "keyframes": [
            {{"frame": 1, "bones": {{"Root": [0,0,0], "Spine": [5,0,0], "Arm_R": [10,-45,10]}}}},
            {{"frame": 15, "bones": {{"Root": [0,0,0], "Spine": [-10,0,0], "Arm_R": [-30,-60,10]}}}}
          ]
        }}
        """

        # Core 1: Gemini
        if self.gemini_api_key:
            try:
                self.log("Executing Core 1 (Gemini) for AAA Motion...", "INFO")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self.clean_json_response(res_text)
                    if parsed and "keyframes" in parsed: return parsed["keyframes"]
            except Exception as e:
                self.log(f"Core 1 Failed: {e}", "WARNING")

        # Core 2: OpenAI
        if self.openai_api_key:
            try:
                self.log("Executing Core 2 (OpenAI) for AAA Motion...", "INFO")
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
                payload = {"model": "gpt-4o", "messages": [{"role": "user", "content": ai_prompt}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
                    parsed = self.clean_json_response(res_text)
                    if parsed and "keyframes" in parsed: return parsed["keyframes"]
            except Exception as e:
                self.log(f"Core 2 Failed: {e}", "WARNING")

        # Core 3: Ollama Local API
        try:
            self.log("Executing Core 3 (Ollama Local) for AAA Motion...", "INFO")
            url = "http://127.0.0.1:11434/api/generate"
            payload = {"model": "llama3", "prompt": ai_prompt, "stream": False}
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as response:
                res_text = json.loads(response.read().decode("utf-8"))["response"]
                parsed = self.clean_json_response(res_text)
                if parsed and "keyframes" in parsed: return parsed["keyframes"]
        except Exception as e:
            self.log(f"Core 3 Failed: {e}", "WARNING")

        # Core 4: Procedural Math Fallback
        return self._get_procedural_fallback_motion(action_script)["keyframes"]

    # RULE 9: ACTIONABLE ABSTRACTION (The AAA Blender Python Script)
    def _generate_blender_animation_script(self, fbx_in_path, fbx_out_path, keyframes_data, config):
        safe_fbx_in = fbx_in_path.replace("\\", "/")
        safe_fbx_out = fbx_out_path.replace("\\", "/")
        safe_blend_out = safe_fbx_out.replace(".fbx", ".blend")
        kf_json = json.dumps(keyframes_data)
        
        style = config.get("animation_style", "anime")
        
        # This script applies AI keyframes + Map/Spider-Verse physics
        blender_script = f"""
import bpy
import json
import math
import sys

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def apply_aaa_physics_and_micro_motions(arm_obj, style):
    if not arm_obj.animation_data or not arm_obj.animation_data.action:
        return
    
    for fcurve in arm_obj.animation_data.action.fcurves:
        bone_name = fcurve.data_path.split('"')[1] if '"' in fcurve.data_path else ""
        
        # 1. MAPPA/Anime Style Step Interpolation (Animate on 2s/3s)
        for kf in fcurve.keyframe_points:
            if style == "anime":
                kf.interpolation = 'CONSTANT' # Snappy, no smooth tweening
            else:
                kf.interpolation = 'BEZIER'
                kf.easing = 'AUTO'
            
        # 2. Secondary Jiggle Physics (Hair, Tail, Cloth, Capes)
        if any(x in bone_name.lower() for x in ['tail', 'hair', 'cloth', 'cape', 'ear']):
            mod = fcurve.modifiers.new('NOISE')
            mod.scale = 10.0
            mod.strength = 0.2
            mod.phase = hash(bone_name) % 10.0
            
        # 3. Organic Breathing (Spine & Ribs)
        if "Spine" in bone_name or "Chest" in bone_name:
            mod = fcurve.modifiers.new('NOISE')
            mod.scale = 25.0
            mod.strength = 0.03

try:
    clear_scene()
    bpy.ops.import_scene.fbx(filepath="{safe_fbx_in}")

    arm_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            arm_obj = obj
            break

    if not arm_obj:
        raise ValueError("No Armature found in FBX.")

    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    arm_obj.animation_data_clear()

    # Apply Base AI Keyframes
    keyframes_data = json.loads('''{kf_json}''')
    for kf in keyframes_data:
        frame_num = kf.get("frame", 1)
        bpy.context.scene.frame_set(frame_num)
        
        for bone_name, rot_deg in kf.get("bones", {{}}).items():
            pose_bone = arm_obj.pose.bones.get(bone_name)
            # Fuzzy matching in case AI capitalized wrong
            if not pose_bone:
                for b in arm_obj.pose.bones:
                    if b.name.lower() == bone_name.lower():
                        pose_bone = b
                        break
                        
            if pose_bone:
                pose_bone.rotation_mode = 'XYZ'
                pose_bone.rotation_euler = [math.radians(r) for r in rot_deg]
                pose_bone.keyframe_insert(data_path="rotation_euler", frame=frame_num)

    # Inject AAA Pipeline Physics
    apply_aaa_physics_and_micro_motions(arm_obj, "{style}")

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.frame_end = 60

    # Export
    bpy.ops.export_scene.fbx(
        filepath="{safe_fbx_out}",
        use_selection=False,
        apply_unit_scale=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
        bake_anim=True,
        bake_anim_use_all_bones=True,
        bake_anim_step=2.0 if "{style}" == "anime" else 1.0 # Bakes on 2s for Anime!
    )
    
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_out}")
    print("OMNIMATRIX_BLENDER_SUCCESS")
except Exception as e:
    print(f"OMNIMATRIX_BLENDER_ERROR: {{str(e)}}")
    sys.exit(1)
"""
        script_path = os.path.join(self.module_h_dir, "temp_puppeteer_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(blender_script)
        return script_path

    def execute_batch_animation(self):
        self.log("System Initializing...", "INFO")

        # RULE 7: ATOMIC HANDSHAKE
        state = {}
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                try: state = json.load(f)
                except: pass
                
        if state.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{state.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        self.scrub_workspace()
        config = self.load_global_config()
        blender_executable = config.get("blender_executable", "blender")

        if not os.path.exists(self.input_rig_blueprint):
            self.log("Agent 58 Blueprint missing. Cannot proceed.", "FATAL")
            sys.exit(1)

        with open(self.input_rig_blueprint, "r", encoding="utf-8") as f:
            master_rig_blueprint = json.load(f)

        master_motion_blueprint = {}

        for scene_name, rig_data in master_rig_blueprint.items():
            fbx_in_path = rig_data.get("rigged_fbx", "")
            if not fbx_in_path or not os.path.exists(fbx_in_path):
                continue

            char_name = f"Char_{scene_name}"
            bone_count = rig_data.get("bone_count", 15)
            
            target_action = self._get_scene_action(scene_name)
            
            self.log(f"--- Animating Scene: {scene_name} | Action: '{target_action}' ---", "INFO")

            fbx_out_path = os.path.join(self.outputs_dir, f"{char_name}_animated.fbx")

            # Core AI Logic
            keyframes = self._query_omni_motion(char_name, bone_count, target_action, config)
            
            # Actionable Abstraction
            script_path = self._generate_blender_animation_script(fbx_in_path, fbx_out_path, keyframes, config)

            self.log(f"Applying AI Keyframes + MAPPA Physics to {char_name}...", "INFO")
            command = [blender_executable, "-b", "-P", script_path]
            
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout and os.path.exists(fbx_out_path):
                    self.log(f"Animation Exported successfully: {char_name}_animated.fbx", "SUCCESS")
                    
                    master_motion_blueprint[scene_name] = {
                        "animated_fbx": fbx_out_path,
                        "animated_blend": fbx_out_path.replace(".fbx", ".blend"),
                        "motion_frames_generated": len(keyframes),
                        "material": rig_data.get("material", ""),
                        "texture": rig_data.get("texture", "")
                    }
                else:
                    self.log(f"Blender failed. Log: {result.stdout[-300:]}", "ERROR")
            except Exception as e:
                self.log(f"Subprocess failed. Is Blender in system PATH? {str(e)}", "CRITICAL")
            
            if os.path.exists(script_path):
                os.remove(script_path)

        with open(self.output_motion_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_motion_blueprint, f, indent=4)

        # RULE 7: ATOMIC HANDSHAKE (Advance State)
        state["last_active_agent"] = self.agent_name
        # Heading to VFX and Lighting Compositor!
        state["next_agent"] = "Ai_Agent_60_Omni_VFX_And_Compositor"
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)

        self.log(f"Omni Animation Pipeline Complete! Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    animator = AiAgent59OmniMotionPuppeteerDirector()
    animator.execute_batch_animation()

# ==============================================================================
# END OF FILE
# ==============================================================================
