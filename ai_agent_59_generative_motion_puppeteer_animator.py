import os
import sys
import json
import re
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
    def __init__(self, workspace_dir="znet_workspace", blender_path="blender"):
        self.agent_name = "Ai Agent 59: Generative Motion Puppeteer"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        # Upstream Inputs
        self.inputs_dir = os.path.join(self.workspace_dir, "rigged_assets")
        self.input_rig_blueprint = os.path.join(self.inputs_dir, "58_master_rig_blueprint.json")
        
        # Outputs
        self.outputs_dir = os.path.join(self.workspace_dir, "animated_scenes")
        self.output_motion_blueprint = os.path.join(self.outputs_dir, "59_master_motion_blueprint.json")
        
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.workspace_dir, self.inputs_dir, self.outputs_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _query_gemini_motion(self, char_name, bone_count):
        """Asks AI to generate realistic keyframes for the specific character."""
        if not self.gemini_api_key:
            return self._get_procedural_fallback_motion()

        prompt = (
            f"You are a Senior AAA 3D Animator. Create a dynamic and REALISTIC 60-frame animation loop for '{char_name}'.\n"
            f"The character has a custom rig with {bone_count} bones. "
            "Focus on 'Secondary Motion': If an arm moves, the spine should slightly react. The pose must feel alive.\n"
            "Return ONLY raw JSON, no markdown formatting. Output rotational Euler angles (in degrees) for key bones.\n"
            "Format exactly like this:\n"
            "{\n"
            "  \"keyframes\": [\n"
            "    {\"frame\": 1, \"bones\": {\"Root\": [0,0,0], \"Spine\": [5,0,0], \"Arm_L\": [10,45,-10], \"Arm_R\": [10,-45,10]}},\n"
            "    {\"frame\": 30, \"bones\": {\"Root\": [0,0,0], \"Spine\": [-2,0,5], \"Arm_L\": [30,60,0], \"Arm_R\": [30,-60,0]}}\n"
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
                {"frame": 1, "bones": {"Root": [0,0,0], "Spine": [0,0,0], "Arm_L": [10,25,0], "Arm_R": [10,-25,0]}},
                {"frame": 30, "bones": {"Root": [0,0,0], "Spine": [3,0,0], "Arm_L": [12,28,0], "Arm_R": [12,-28,0]}},
                {"frame": 60, "bones": {"Root": [0,0,0], "Spine": [0,0,0], "Arm_L": [10,25,0], "Arm_R": [10,-25,0]}}
            ]
        }

    def _generate_blender_animation_script(self, fbx_in_path, fbx_out_path, keyframes_data):
        """Creates the internal python script for Blender to apply keyframes and Micro-Motions."""
        safe_fbx_in = fbx_in_path.replace("\\", "/")
        safe_fbx_out = fbx_out_path.replace("\\", "/")
        kf_json = json.dumps(keyframes_data)

        blender_script = f"""
import bpy
import json
import math
import sys

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def apply_micro_motions(arm_obj):
    # Adds subtle noise modifiers to F-Curves to simulate breathing, shivering, and realistic finger twitching.
    if not arm_obj.animation_data or not arm_obj.animation_data.action:
        return
    
    for fcurve in arm_obj.animation_data.action.fcurves:
        # Only apply breathing to Spine and tiny twitches to Arm/Fingers
        if "Spine" in fcurve.data_path or "Arm" in fcurve.data_path or "Finger" in fcurve.data_path:
            mod = fcurve.modifiers.new('NOISE')
            mod.scale = 20.0 # Slow breathing frequency
            mod.strength = 0.05 # Very subtle rotation
            mod.phase = 1.0

try:
    clear_scene()

    # 1. Import Rigged FBX
    bpy.ops.import_scene.fbx(filepath="{safe_fbx_in}")

    # Find the imported Armature
    arm_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            arm_obj = obj
            break

    if not arm_obj:
        raise ValueError("No Armature found in FBX file.")

    # 2. Setup Animation
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    arm_obj.animation_data_clear()

    keyframes_data = json.loads('''{kf_json}''')

    # 3. Apply Main Keyframes (Generated by AI)
    for kf in keyframes_data:
        frame_num = kf.get("frame", 1)
        bpy.context.scene.frame_set(frame_num)
        
        for bone_name, rot_deg in kf.get("bones", {{}}).items():
            pose_bone = arm_obj.pose.bones.get(bone_name)
            if pose_bone:
                pose_bone.rotation_mode = 'XYZ'
                pose_bone.rotation_euler = [math.radians(r) for r in rot_deg]
                pose_bone.keyframe_insert(data_path="rotation_euler", frame=frame_num)

    # 4. Apply Realistic Micro-Motions (The Magic Touch)
    apply_micro_motions(arm_obj)

    bpy.ops.object.mode_set(mode='OBJECT')

    # 5. Export Animated FBX
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
    print("SUCCESS")
except Exception as e:
    print("ERROR:", str(e))
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_animator_script.py")
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

            char_name = os.path.basename(fbx_in_path).replace("_rigged.fbx", "")
            bone_count = rig_data.get("bone_count", 10)
            
            self.log_message(f"--- Animating Scene: {scene_name} | Target: {char_name} ---", "INFO")

            # Output path for final animated asset
            fbx_out_path = os.path.join(self.outputs_dir, f"{char_name}_animated.fbx")

            # 1. Ask AI for Motion Path
            keyframes = self._query_gemini_motion(char_name, bone_count)

            # 2. Write Blender Script
            script_path = self._generate_blender_animation_script(fbx_in_path, fbx_out_path, keyframes)

            # 3. Execute Headless Blender
            self.log_message(f"Applying AI Keyframes and Micro-Motions to {char_name}...", "INFO")
            command = [self.blender_path, "-b", "-P", script_path]
            
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0 and os.path.exists(fbx_out_path):
                    self.log_message(f"Animation Exported: {char_name}_animated.fbx", "INFO")
                    
                    master_motion_blueprint[scene_name] = {
                        "animated_fbx": fbx_out_path,
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
