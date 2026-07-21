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

class GenerativeMotionPuppeteerAnimator:
    # 1. Local Assets & 5TB Drive Split Strategy
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 59: AAA Generative Motion Puppeteer"
        
        # Upstream Inputs
        self.vision_outputs_dir = os.path.join(drive_temp_dir, "outputs")
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts") # Module A Matrix State
        
        self.inputs_dir = os.path.join(local_library_dir, "rigged_assets")
        self.input_rig_blueprint = os.path.join(self.inputs_dir, "58_master_rig_blueprint.json")
        
        # Outputs (Going straight to Fast Local Drive)
        self.outputs_dir = os.path.join(local_library_dir, "animated_assets")
        self.output_motion_blueprint = os.path.join(self.outputs_dir, "59_master_motion_blueprint.json")
        
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [drive_temp_dir, self.inputs_dir, self.outputs_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _get_scene_action(self, scene_name):
        """Fetches the actual script/action defined by Module A (e.g., 'Gojo unleashes hollow purple')"""
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            with open(script_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("action_description", "Idle battle stance breathing heavily.")
        return "Idle battle stance breathing heavily."

    def _query_gemini_motion(self, char_name, bone_count, action_script):
        """Asks AI to generate realistic, physics-based keyframes based on the SCRIPT."""
        if not self.gemini_api_key:
            return self._get_procedural_fallback_motion()

        prompt = (
            f"You are a Senior AAA 3D Animator. Create a dynamic, REALISTIC 60-frame animation loop for '{char_name}'.\n"
            f"The character has a custom rig with {bone_count} bones. \n"
            f"CRITICAL TARGET ACTION: '{action_script}'\n\n"
            "ANIMATION PRINCIPLES REQUIRED:\n"
            "1. Weight & Momentum: Motions must not feel robotic. Include Anticipation (winding up) before the main action.\n"
            "2. Facial Expressions: If 'Jaw' or 'Eye' bones exist, rotate them to match the emotion of the action.\n"
            "3. Secondary Motion: The spine must react to limb movements.\n\n"
            "Return ONLY raw JSON, no markdown formatting. Output rotational Euler angles (in degrees) for key bones.\n"
            "Format exactly like this:\n"
            "{\n"
            "  \"keyframes\": [\n"
            "    {\"frame\": 1, \"bones\": {\"Root\": [0,0,0], \"Spine\": [5,0,0], \"Arm_R\": [10,-45,10], \"Jaw\": [5,0,0]}}\n"
            "  ]\n"
            "}"
        )

        try:
            payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                return json.loads(res_text).get("keyframes", self._get_procedural_fallback_motion()["keyframes"])
        except Exception as e:
            self.log_message(f"AI Motion Generator failed: {str(e)}. Using fallback.", "WARNING")
            return self._get_procedural_fallback_motion()["keyframes"]

    def _get_procedural_fallback_motion(self):
        """A realistic breathing/idle loop with secondary motions."""
        return {
            "keyframes": [
                {"frame": 1, "bones": {"Root": [0,0,0], "Spine": [0,0,0], "Arm_L": [10,25,0], "Arm_R": [10,-25,0], "Jaw": [0,0,0]}},
                {"frame": 30, "bones": {"Root": [0,0,0], "Spine": [3,0,0], "Arm_L": [12,28,0], "Arm_R": [12,-28,0], "Jaw": [2,0,0]}},
                {"frame": 60, "bones": {"Root": [0,0,0], "Spine": [0,0,0], "Arm_L": [10,25,0], "Arm_R": [10,-25,0], "Jaw": [0,0,0]}}
            ]
        }

    def _generate_blender_animation_script(self, fbx_in_path, fbx_out_path, keyframes_data):
        """Creates the internal python script for Blender to apply keyframes, Bezier Physics, and Micro-Motions."""
        safe_fbx_in = fbx_in_path.replace("\\", "/")
        safe_fbx_out = fbx_out_path.replace("\\", "/")
        safe_blend_out = safe_fbx_out.replace(".fbx", ".blend")
        kf_json = json.dumps(keyframes_data)

        blender_script = f"""
import bpy
import json
import math
import sys

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def apply_aaa_physics_and_micro_motions(arm_obj):
    if not arm_obj.animation_data or not arm_obj.animation_data.action:
        return
    
    for fcurve in arm_obj.animation_data.action.fcurves:
        # 1. AAA Curve Smoothing (Weight & Momentum)
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'BEZIER'
            kf.easing = 'AUTO'
            
        # 2. Procedural Micro-Motions (Breathing/Twitching)
        if "Spine" in fcurve.data_path or "Arm" in fcurve.data_path or "Finger" in fcurve.data_path:
            mod = fcurve.modifiers.new('NOISE')
            mod.scale = 20.0
            mod.strength = 0.05
            mod.phase = 1.0

try:
    clear_scene()

    bpy.ops.import_scene.fbx(filepath="{safe_fbx_in}")

    arm_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            arm_obj = obj
            break

    if not arm_obj:
        raise ValueError("No Armature found in FBX file.")

    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    arm_obj.animation_data_clear()

    keyframes_data = json.loads('''{kf_json}''')

    for kf in keyframes_data:
        frame_num = kf.get("frame", 1)
        bpy.context.scene.frame_set(frame_num)
        
        for bone_name, rot_deg in kf.get("bones", {{}}).items():
            pose_bone = arm_obj.pose.bones.get(bone_name)
            if pose_bone:
                pose_bone.rotation_mode = 'XYZ'
                pose_bone.rotation_euler = [math.radians(r) for r in rot_deg]
                pose_bone.keyframe_insert(data_path="rotation_euler", frame=frame_num)

    apply_aaa_physics_and_micro_motions(arm_obj)

    bpy.ops.object.mode_set(mode='OBJECT')

    # Export Animated FBX
    bpy.ops.export_scene.fbx(
        filepath="{safe_fbx_out}",
        use_selection=False,
        apply_unit_scale=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
        bake_anim=True,
        bake_anim_use_all_bones=True,
        bake_anim_step=1.0
    )
    
    # Export Editable Blend File (Local)
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_out}")
    
    print("SUCCESS")
except Exception as e:
    print("ERROR:", str(e))
    sys.exit(1)
"""
        script_path = os.path.join("temp_animator_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(blender_script)
        return script_path

    def execute_batch_animation(self):
        self.log_message("Initializing AAA Generative Puppeteer...", "INFO")

        if not os.path.exists(self.input_rig_blueprint):
            self.log_message("Agent 58 Blueprint missing. Cannot proceed.", "ERROR")
            return

        with open(self.input_rig_blueprint, "r", encoding="utf-8") as f:
            master_rig_blueprint = json.load(f)

        master_motion_blueprint = {}

        for scene_name, rig_data in master_rig_blueprint.items():
            fbx_in_path = rig_data.get("rigged_fbx", "")
            if not fbx_in_path or not os.path.exists(fbx_in_path):
                continue

            # Check if this scene was an Environment Only bypass
            vision_json_path = os.path.join(self.vision_outputs_dir, f"{scene_name}_vision.json")
            if os.path.exists(vision_json_path):
                with open(vision_json_path, "r", encoding="utf-8") as vf:
                    if json.load(vf).get("pipeline_mode") == "Environment":
                        self.log_message(f"Skipping Animation for {scene_name} (Environment Only).", "INFO")
                        continue

            char_name = os.path.basename(fbx_in_path).replace("_rigged.fbx", "")
            bone_count = rig_data.get("bone_count", 10)
            
            # Fetch specific action script
            target_action = self._get_scene_action(scene_name)
            
            self.log_message(f"--- Animating Scene: {scene_name} | Target: {char_name} ---", "INFO")
            self.log_message(f"Action Script: '{target_action}'", "INFO")

            fbx_out_path = os.path.join(self.outputs_dir, f"{char_name}_animated.fbx")

            keyframes = self._query_gemini_motion(char_name, bone_count, target_action)
            script_path = self._generate_blender_animation_script(fbx_in_path, fbx_out_path, keyframes)

            self.log_message(f"Applying AI Keyframes and Physics to {char_name}...", "INFO")
            command = [self.blender_path, "-b", "-P", script_path]
            
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0 and os.path.exists(fbx_out_path):
                    self.log_message(f"Animation Exported to LOCAL DRIVE: {char_name}_animated.fbx", "INFO")
                    
                    master_motion_blueprint[scene_name] = {
                        "animated_fbx": fbx_out_path,
                        "animated_blend": fbx_out_path.replace(".fbx", ".blend"),
                        "motion_frames_generated": len(keyframes),
                        "material": rig_data.get("material", ""),
                        "texture": rig_data.get("texture", "")
                    }
                else:
                    self.log_message(f"Blender failed. Log: {result.stdout[-300:]}", "ERROR")
            except Exception as e:
                self.log_message(f"Subprocess failed. Is Blender in system PATH? {str(e)}", "CRITICAL")
            
            if os.path.exists(script_path):
                os.remove(script_path)

        with open(self.output_motion_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_motion_blueprint, f, indent=4)

        self.log_message("Puppeteer Animation Pipeline Complete!", "INFO")

if __name__ == "__main__":
    animator = GenerativeMotionPuppeteerAnimator()
    animator.execute_batch_animation()
