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
                    # Universal Uppercase Fix for API Keys
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class KineticRigPuppeteerAnimator:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 26: aaa_kinetic_rig_puppeteer"
        
        # Directories
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments") # Modifies existing _stage.blend files
        self.output_blueprint = os.path.join(self.workspace_dir, "26_animation_blueprint.json")
        self.blender_path = blender_path
        
        # GEMINI API INTEGRATION
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.workspace_dir, self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_action(self, scene_name):
        """Loads the action description and overall vibe (OMNI UNIVERSAL)."""
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {
            "visual_style": "omni_neutral",
            "vibe_genre": "General",
            "action_description": "Character standing and waving happily."
        }
        
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "omni_neutral")
                    context["vibe_genre"] = data.get("genre_vibe", "General")
                    context["action_description"] = data.get("action_description", "Character performs a standard idle action.")
            except Exception as e:
                self.log_message(f"Script parse warning: {str(e)}", "WARNING")
                
        return context

    def _clean_json_response(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
        return cleaned

    def _query_animator_brain(self, scene_name, context):
        self.log_message(f"Calculating Kinetic Rig Vectors for '{scene_name}'...", "INFO")
        
        if not self.gemini_api_key:
            self.log_message("No Gemini API Key found. Using fallback pose.", "WARNING")
            return self._fallback_animation(context)

        ai_prompt = (
            f"You are the Lead 3D Animator (Omni-Universal) for Z-NET Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style/Genre: {context['visual_style']} / {context['vibe_genre']}\n"
            f"Action Required: {context['action_description']}\n\n"
            "Design the skeletal bone rotations (in degrees) for a standard humanoid rig (mixamorig) to execute this action.\n"
            "If style is Anime, use 'CONSTANT' interpolation. If style is Realistic/Pixar, use 'BEZIER'.\n"
            "Return EXACTLY 1 raw JSON object containing:\n"
            "{\n"
            "  \"target_frame\": 24,\n"
            "  \"interpolation_type\": \"BEZIER\",\n"
            "  \"root_translation\": [0.0, 1.5, 0.0],\n"
            "  \"bone_rotations\": {\n"
            "    \"mixamorig:Hips\": [0, 0, 0],\n"
            "    \"mixamorig:Spine\": [15, 0, 0],\n"
            "    \"mixamorig:RightArm\": [45, 0, 20],\n"
            "    \"mixamorig:LeftArm\": [-10, 0, 0],\n"
            "    \"mixamorig:RightLeg\": [10, 0, 0],\n"
            "    \"mixamorig:LeftLeg\": [-5, 0, 0]\n"
            "  },\n"
            "  \"animation_rationale\": \"Joyful jumping wave suited for the bright vibe.\"\n"
            "}"
        )

        try:
            # NATIVE GEMINI JSON PAYLOAD
            payload = {
                "contents": [{"parts": [{"text": ai_prompt}]}], 
                "generationConfig": {"responseMimeType": "application/json"}
            }
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                cleaned = self._clean_json_response(res_text)
                return json.loads(cleaned)
        except Exception as e:
            self.log_message(f"Gemini API Route Failed: {str(e)}. Using fallback pose.", "WARNING")
            return self._fallback_animation(context)

    def _fallback_animation(self, context):
        return {
            "target_frame": 24, "interpolation_type": "BEZIER", "root_translation": [0.0, 0.0, 0.0],
            "bone_rotations": {
                "mixamorig:Spine": [5, 0, 0], "mixamorig:RightArm": [20, 0, 0], "mixamorig:LeftArm": [20, 0, 0]
            },
            "animation_rationale": "Omni-neutral fallback idle pose."
        }

    def _generate_blender_script(self, blend_file_path, anim_data):
        """Python script to manipulate the Armature and insert keyframes."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy
import math

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    # 1. Find ALL Character Armatures (Rigs) for multi-character support
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
            
    if not armatures:
        print("WARNING: No Armature found in scene. Cannot apply animation.")
    else:
        frame_num = {anim_data.get('target_frame', 24)}
        interp_mode = "{anim_data.get('interpolation_type', 'BEZIER')}"
        root_trans = {anim_data.get('root_translation', [0,0,0])}
        bone_rotations = {anim_data.get('bone_rotations', {{}})}
        
        for armature in armatures:
            # 2. Enter Pose Mode
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')
            
            # 3. Apply Root Translation (Hips/Root Bone)
            armature.location = (root_trans[0], root_trans[1], root_trans[2])
            armature.keyframe_insert(data_path="location", frame=frame_num)

            # 4. Apply Bone Rotations
            for bone_name, rot_degrees in bone_rotations.items():
                if bone_name in armature.pose.bones:
                    pb = armature.pose.bones[bone_name]
                    pb.rotation_mode = 'XYZ'
                    # Convert degrees to radians safely
                    pb.rotation_euler = (math.radians(rot_degrees[0]), math.radians(rot_degrees[1]), math.radians(rot_degrees[2]))
                    pb.keyframe_insert(data_path="rotation_euler", frame=frame_num)
            
            # 5. Set Interpolation Mode (Anime 'CONSTANT' vs Real 'BEZIER')
            if armature.animation_data and armature.animation_data.action:
                for fcurve in armature.animation_data.action.fcurves:
                    for kf in fcurve.keyframe_points:
                        kf.interpolation = interp_mode

            bpy.ops.object.mode_set(mode='OBJECT')
            
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS: Kinetic Rig Animation successfully baked into timeline.")

except Exception as e:
    print(f"ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_animator_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_stage_animations(self):
        self.log_message("Waking up Omni-Universal Rig Puppeteer...", "INFO")
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                self.log_message(f"--- Animating Stage: {scene_name} ---", "INFO")
                
                context = self._load_upstream_action(scene_name)
                anim_data = self._query_animator_brain(scene_name, context)
                
                self.log_message(f"AI Decision: Applying '{anim_data.get('animation_rationale', 'Default')}' | Interpolation: {anim_data.get('interpolation_type', 'BEZIER')}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, anim_data)
                
                self.log_message("Executing Headless Blender to inject Keyframes...", "INFO")
                command = [self.blender_path, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        self.log_message(f"Animation successfully injected into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = anim_data
                    else:
                        self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 26 Pipeline Complete. Characters are now posed and animated dynamically.", "INFO")

if __name__ == "__main__":
    animator = KineticRigPuppeteerAnimator()
    animator.process_stage_animations()
