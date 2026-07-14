import os
import sys
import json
import urllib.request
import urllib.error

class GenerativeMotionPuppeteerAnimator:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 59: generative_motion_puppeteer_animator"
        self.workspace_dir = workspace_dir
        
        # Upstream Inputs
        self.input_rig_blueprint = os.path.join(self.workspace_dir, "58_rig_blueprint.json")
        
        # Outputs
        self.output_motion_blueprint = os.path.join(self.workspace_dir, "59_motion_blueprint.json")
        self.output_blender_anim_script = os.path.join(self.workspace_dir, "59_blender_animate.py")
        
        # [SECURE] No hardcoded keys. Clean environmental loading.
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def generate_motion_sequence(self):
        print(f"[{self.agent_name}] Initializing AI Generative Animation Sequence...")
        
        # Default target anime emotion setup
        action_style = "ANIME_CLIMAX_ACTION"

        ai_prompt_instructions = (
            "You are a Senior 3D Animator. Create a dynamic animation sequence for a humanoid character armature.\n"
            f"Action Style: {action_style}.\n"
            "Generate rotational keyframe data (euler angles in degrees) for bones: 'Root', 'Spine', 'Arm_L', 'Arm_R'.\n"
            "Return ONLY a valid JSON object without any markdown wrapping, code blocks, or backticks. Format:\n"
            "{\n"
            "  \"keyframes\": [\n"
            "    {\n"
            "      \"frame\": 1,\n"
            "      \"bones\": {\n"
            "        \"Spine\": [0.0, 0.0, 0.0],\n"
            "        \"Arm_L\": [0.0, 45.0, 0.0],\n"
            "        \"Arm_R\": [0.0, -45.0, 0.0]\n"
            "      }\n"
            "    },\n"
            "    {\n"
            "      \"frame\": 20,\n"
            "      \"bones\": {\n"
            "        \"Spine\": [10.0, 0.0, 0.0],\n"
            "        \"Arm_L\": [30.0, 90.0, -10.0],\n"
            "        \"Arm_R\": [-30.0, -90.0, 10.0]\n"
            "      }\n"
            "    }\n"
            "  ]\n"
            "}"
        )

        motion_data = None

        if self.gemini_api_key:
            print(f"[{self.agent_name}] Fetching frame-by-frame action curves from Gemini Cloud...")
            try:
                payload = {
                    "contents": [{
                        "parts": [{"text": ai_prompt_instructions}]
                    }],
                    "generationConfig": {
                        "responseMimeType": "application/json"
                    }
                }
                data_bytes = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    self.gemini_url, 
                    data=data_bytes, 
                    headers={"Content-Type": "application/json"}
                )

                with urllib.request.urlopen(req, timeout=15) as response:
                    res_body = response.read().decode("utf-8")
                    raw_response = json.loads(res_body)
                    raw_text = raw_response["candidates"][0]["content"]["parts"][0]["text"]
                    motion_data = json.loads(raw_text.strip())
                    print(f"[{self.agent_name}] Success: Generative motion paths compiled successfully.")
            except Exception as e:
                print(f"[{self.agent_name}] Cloud motion bypass ({str(e)}). Building native cyclical idle animation...")
                motion_data = self._get_procedural_motion()
        else:
            print(f"[{self.agent_name}] Running offline. Compiling math-based procedural motion loop...")
            motion_data = self._get_procedural_motion()

        # Save Motion Blueprint JSON
        self._save_motion_blueprint(motion_data)

        # Build Blender automation sequence
        self._generate_blender_animation_script(motion_data)

        return motion_data

    def _get_procedural_motion(self):
        # Generates a dynamic combat preparation idle loop (breathe and ready stance)
        return {
            "keyframes": [
                {
                    "frame": 1,
                    "bones": {
                        "Spine": [0.0, 0.0, 0.0],
                        "Arm_L": [15.0, 45.0, 0.0],
                        "Arm_R": [-15.0, -45.0, 0.0]
                    }
                },
                {
                    "frame": 15,
                    "bones": {
                        "Spine": [5.0, 0.0, -2.0], # Breath down, slightly hunched
                        "Arm_L": [20.0, 60.0, -5.0],
                        "Arm_R": [-10.0, -35.0, 5.0]
                    }
                },
                {
                    "frame": 30,
                    "bones": {
                        "Spine": [0.0, 0.0, 0.0], # Return to base frame for loop
                        "Arm_L": [15.0, 45.0, 0.0],
                        "Arm_R": [-15.0, -45.0, 0.0]
                    }
                }
            ]
        }

    def _generate_blender_animation_script(self, motion_cfg):
        kf_list = motion_cfg.get("keyframes", [])
        
        script_content = f"""# ==========================================
# Blender Motion Keyframe Puppeteer (Z-NET Agent 59)
# Run this inside Blender Scripting Workspace!
# ==========================================
import bpy
import math

# Target the active character armature
armature_name = "Character_Armature"
arm_obj = bpy.data.objects.get(armature_name)

if arm_obj:
    # Switch to Pose Mode to register rotations
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')
    
    # 1. Clear pre-existing animations
    arm_obj.animation_data_clear()
    
    # Keyframe Data Injection
    keyframes_data = {kf_list}
    
    # 2. Iterate through keyframes and inject rot values
    for kf in keyframes_data:
        frame_num = kf["frame"]
        bpy.context.scene.frame_set(frame_num)
        
        for bone_name, rotation_deg in kf["bones"].items():
            pose_bone = arm_obj.pose.bones.get(bone_name)
            if pose_bone:
                # Set rotation mode to Euler
                pose_bone.rotation_mode = 'XYZ'
                # Convert degrees to radians
                pose_bone.rotation_euler = [math.radians(r) for r in rotation_deg]
                # Insert keyframe rotation curve
                pose_bone.keyframe_insert(data_path="rotation_euler", frame=frame_num)
                
    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Generative Motion Keyframes applied! Press spacebar in Blender to play!")
else:
    print("Warning: Rig armature 'Character_Armature' not found in current Blender scene.")
"""
        with open(self.output_blender_anim_script, "w", encoding="utf-8") as f:
            f.write(script_content)
        print(f"[{self.agent_name}] Success: Motion Puppeteer Blender automation ready at '{self.output_blender_anim_script}'")

    def _save_motion_blueprint(self, data):
        with open(self.output_motion_blueprint, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[{self.agent_name}] Animation motion sequences written to '{self.output_motion_blueprint}'")

if __name__ == "__main__":
    puppeteer = GenerativeMotionPuppeteerAnimator()
    puppeteer.generate_motion_sequence()
