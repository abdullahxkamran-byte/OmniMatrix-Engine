import os
import re
import sys
import json
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
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class OmniMatrixLipSyncDeformer:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 32: OmniMatrix Lip-Sync & Actor Deformer"
        
        # Directories
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.env_dir, "32_omni_lipsync_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_context(self, scene_name):
        """Loads visual style and dialogue from Master Matrix State"""
        context = {
            "visual_style": "omni_neutral",
            "dialogue_text": "Omni matrix initialization complete.",
            "start_frame": 12,
            "character_id": "char_main"
        }
        
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "omni_neutral")
                    
                    # Look for dialogue in matrix state
                    if "dialogue" in data and data["dialogue"]:
                        context["dialogue_text"] = data["dialogue"]
            except:
                pass
                
        return context

    def _query_linguistic_brain(self, scene_name, context):
        if not self.gemini_api_key:
            return self._fallback_phonemes(context)

        ai_prompt = (
            f"You are the Lead Linguistic & Facial Animator for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Dialogue: \"{context['dialogue_text']}\"\n"
            f"Start Frame: {context['start_frame']}\n\n"
            "Analyze the dialogue and break it down into phoneme frames for 3D lipsync.\n"
            "- If style is 'anime', output fewer frames (snappy mouth flaps: open, half, closed).\n"
            "- If style is 'realistic', output granular frames per syllable.\n"
            "Create a list of keyframes. For each frame, provide:\n"
            "1. 'frame_num': Integer frame number (assuming 24fps).\n"
            "2. 'syllable': The sound being made.\n"
            "3. 'viseme_A_O': Weight (0.0 to 1.0) for wide/open mouth.\n"
            "4. 'viseme_E_I': Weight (0.0 to 1.0) for wide lips.\n"
            "5. 'viseme_U': Weight (0.0 to 1.0) for puckered lips.\n"
            "6. 'viseme_BMP': Weight (0.0 to 1.0) for closed lips.\n"
            "7. 'jaw_drop': Float (0.0 to 1.0).\n"
            "Return ONLY raw JSON in this format:\n"
            "{\n"
            "  \"keyframes\": [\n"
            "    {\"frame_num\": 12, \"syllable\": \"Om\", \"viseme_A_O\": 0.8, \"viseme_E_I\": 0.0, \"viseme_U\": 0.2, \"viseme_BMP\": 0.0, \"jaw_drop\": 0.5}\n"
            "  ]\n"
            "}"
        )

        try:
            payload = {"contents": [{"parts": [{"text": ai_prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                return json.loads(res_text)
        except Exception as e:
            self.log_message(f"AI Linguistic Brain failed: {str(e)}. Triggering procedural fallback.", "WARNING")
            return self._fallback_phonemes(context)

    def _fallback_phonemes(self, context):
        start = context["start_frame"]
        words = context["dialogue_text"].split()
        frames = []
        current_frame = start
        
        for w in words:
            # Open mouth for word start
            frames.append({"frame_num": current_frame, "syllable": w, "viseme_A_O": 0.8, "viseme_E_I": 0.2, "viseme_U": 0.0, "viseme_BMP": 0.0, "jaw_drop": 0.6})
            current_frame += 4
            # Close mouth at word end
            frames.append({"frame_num": current_frame, "syllable": "-", "viseme_A_O": 0.0, "viseme_E_I": 0.0, "viseme_U": 0.0, "viseme_BMP": 1.0, "jaw_drop": 0.0})
            current_frame += 3
            
        return {"keyframes": frames}

    def _generate_blender_script(self, blend_file_path, sync_data, visual_style):
        """God-Level Blender Python Script to inject Lip Sync AND Head Bob dynamics"""
        safe_blend_path = blend_file_path.replace("\\", "/")
        frames_json = json.dumps(sync_data.get("keyframes", []))
        
        # Omnimatrix Logic: Anime gets stepped sharp keys, Real gets smooth bezier keys
        interp_type = "'CONSTANT'" if "anime" in visual_style.lower() else "'BEZIER'"
        
        script_content = f"""
import bpy
import json
import math

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    frames_data = json.loads('''{frames_json}''')
    interp_style = {interp_type}
    
    # 1. Fuzzy Name Mappings for Universal Compatibility
    shape_map = {{
        "viseme_A_O": ["viseme_a_o", "a", "o", "mouth_open", "jaw_drop", "open"],
        "viseme_E_I": ["viseme_e_i", "e", "i", "mouth_wide", "smile"],
        "viseme_U":   ["viseme_u", "u", "w", "pucker", "kiss"],
        "viseme_BMP": ["viseme_bmp", "b", "m", "p", "mouth_closed", "closed"]
    }}

    def find_shape_key(mesh_obj, logical_name):
        if not mesh_obj.data.shape_keys: return None
        target_list = shape_map.get(logical_name, [])
        for kb in mesh_obj.data.shape_keys.key_blocks:
            kb_lower = kb.name.lower()
            if any(t in kb_lower for t in target_list):
                return kb
        return None

    # 2. Find Character Mesh & Armature
    char_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.data.shape_keys]
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
    
    if char_meshes:
        for mesh in char_meshes:
            for fd in frames_data:
                f_num = fd["frame_num"]
                
                # Apply Shape Keys
                for logical_name in ["viseme_A_O", "viseme_E_I", "viseme_U", "viseme_BMP"]:
                    sk = find_shape_key(mesh, logical_name)
                    if sk:
                        sk.value = fd.get(logical_name, 0.0)
                        sk.keyframe_insert(data_path="value", frame=f_num)
                        
                        # Set Omnimatrix Interpolation (Anime vs Realistic)
                        if sk.animation_data and sk.animation_data.action:
                            fc = sk.animation_data.action.fcurves.find('key_blocks["'+sk.name+'"].value')
                            if fc:
                                for kp in fc.keyframe_points:
                                    if kp.co[0] == f_num:
                                        kp.interpolation = interp_style

    # 3. God Level: Auto Head/Neck Bobbing based on speech rhythm
    if armatures and frames_data:
        arm = armatures[0]
        # Try to find head or neck bone
        head_bone = None
        for bone_name in ["Head", "head", "Neck", "neck", "mixamorig:Head"]:
            if bone_name in arm.pose.bones:
                head_bone = arm.pose.bones[bone_name]
                break
                
        if head_bone:
            arm.animation_data_create()
            head_bone.rotation_mode = 'XYZ'
            
            for i, fd in enumerate(frames_data):
                f_num = fd["frame_num"]
                intensity = fd.get("jaw_drop", 0.0)
                
                # Create a subtle bob effect
                # If jaw opens wide (A_O), head tilts slightly up/down based on anime vs realistic
                bob_angle = (intensity * 0.05) if interp_style == 'BEZIER' else (intensity * 0.1)
                
                # Alternate direction slightly for dynamic life
                direction = 1 if i % 2 == 0 else -1
                
                original_rot = list(head_bone.rotation_euler)
                head_bone.rotation_euler[0] = original_rot[0] + (bob_angle * direction)
                
                head_bone.keyframe_insert(data_path="rotation_euler", index=0, frame=f_num)
                
                # Reset interpolation
                if arm.animation_data and arm.animation_data.action:
                    fc = arm.animation_data.action.fcurves.find('pose.bones["'+head_bone.name+'"].rotation_euler', index=0)
                    if fc:
                        for kp in fc.keyframe_points:
                            if kp.co[0] == f_num:
                                kp.interpolation = interp_style
                                
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print(f"SUCCESS: OmniMatrix Lip-Sync & Head-Bobbing applied. Interp: {{interp_style}}")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_lipsync_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_lip_sync(self):
        self.log_message("Initializing OmniMatrix Audio-Driven Actor Deformer...", "INFO")
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_context(scene_name)
                
                self.log_message(f"--- Acting Scene: {scene_name} | Dialogue: '{context['dialogue_text']}' ---", "INFO")
                
                sync_data = self._query_linguistic_brain(scene_name, context)
                
                script_path = self._generate_blender_script(blend_file_path, sync_data, context["visual_style"])
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_message(f"God-Level Lip-Sync & Micro-Movements applied to {filename}", "INFO")
                        master_blueprint[scene_name] = sync_data
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 32 Pipeline Complete. Characters are now breathing and speaking dynamically!", "INFO")

if __name__ == "__main__":
    actor = OmniMatrixLipSyncDeformer()
    actor.process_lip_sync()
