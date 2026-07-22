import os
import re
import sys
import json
import math
import random
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

class UniversalKineticCameraRigDirector:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 21: universal_kinetic_camera_rig_director"
        
        self.workspace_dir = workspace_dir
        self.audio_dir = os.path.join(self.workspace_dir, "module_b_audio")
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        self.output_blueprint = os.path.join(self.workspace_dir, "21_universal_camera_rig_blueprint.json")
        self.blender_path = blender_path
        
        # GEMINI API INTEGRATION RESTORED!
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=){self.gemini_api_key}"

        for d in [self.workspace_dir, self.audio_dir, self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_master_config(self):
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("global_style", "realistic").lower()
            except Exception as e:
                self.log_message(f"Master config read warning: {str(e)}", "WARNING")
        return "realistic"

    def _load_upstream_sync_data(self, scene_name):
        sync_triggers = []
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        beat_file = os.path.join(self.workspace_dir, "14_phonk_beat_drop_map.json")
        
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    sync_triggers.append({"timestamp_sec": 0.0, "event_type": "scene_start", "intensity": "moderate", "action": data.get("action_description", "Establishing shot")})
                    sync_triggers.append({"timestamp_sec": 3.0, "event_type": "action_peak", "intensity": "high", "action": "Main dynamic action"})
            except Exception as e:
                self.log_message(f"Script parse warning: {str(e)}", "WARNING")

        if os.path.exists(beat_file):
            try:
                with open(beat_file, "r", encoding="utf-8") as f:
                    b_data = json.load(f)
                for drop in b_data.get("beat_drops", []):
                    sync_triggers.append({"timestamp_sec": drop.get("timestamp_sec", 1.5), "event_type": "beat_drop_impact", "intensity": "extreme", "action": "Massive screen shake impact"})
            except:
                pass

        sync_triggers = sorted(sync_triggers, key=lambda x: x["timestamp_sec"])
        
        if not sync_triggers:
            sync_triggers = [
                {"timestamp_sec": 0.0, "event_type": "intro_pan", "intensity": "moderate", "action": "Look around"},
                {"timestamp_sec": 2.5, "event_type": "beat_drop_impact", "intensity": "extreme", "action": "Explosion"}
            ]
        return sync_triggers

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

    def _query_camera_brain(self, scene_name, triggers, style):
        self.log_message(f"Calculating AAA Camera trajectories for '{scene_name}' (Style: {style.upper()})...", "INFO")
        
        system_prompt = (
            f"You are the Lead Cinematographer. Project style: '{style.upper()}'.\n"
            "If REALISTIC: Use natural focal lengths (35mm-50mm), low aperture (f/1.8 for deep DoF), smooth dollys, and subtle handheld shake (amplitude < 0.3).\n"
            "If ANIME: Use extreme wide angles (18mm-24mm), deep focus (f/4.0+), dynamic dutch angles, and massive screen shakes on beat drops (amplitude 1.0 - 2.5).\n"
            "Output EXACTLY 1 raw JSON object containing 'camera_keyframe_data' (a list of keyframes based on the triggers provided).\n"
            "Required keys per keyframe:\n"
            "- 'timestamp_sec': float.\n"
            "- 'focal_length_mm': float.\n"
            "- 'camera_location_offset': [X, Y, Z].\n"
            "- 'focus_target_location': [X, Y, Z] (Where the camera looks and focuses).\n"
            "- 'screen_shake_amplitude': float (0.0 if no beat drop, >1.0 for massive impacts).\n"
            "- 'dof_aperture_fstop': float.\n"
            "Output strictly valid JSON with no backticks."
        )

        if self.gemini_api_key:
            try:
                # GEMINI NATIVE JSON PAYLOAD & PROMPT MERGE
                combined_prompt = system_prompt + "\n\nTriggers Data:\n" + json.dumps(triggers)
                payload = {
                    "contents": [{"parts": [{"text": combined_prompt}]}], 
                    "generationConfig": {"responseMimeType": "application/json"}
                }
                req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                    cleaned = self._clean_json_response(res_text)
                    return json.loads(cleaned).get("camera_keyframe_data", self._get_procedural_fallback(triggers, style))
            except Exception as e:
                self.log_message(f"Gemini API Route Failed: {str(e)}. Using procedural fallback.", "WARNING")

        return self._get_procedural_fallback(triggers, style)

    def _get_procedural_fallback(self, triggers, style):
        keyframes = []
        for trigger in triggers:
            ts = float(trigger.get("timestamp_sec", 0.0))
            event = str(trigger.get("event_type", "")).lower()

            if style == "realistic":
                focal, fstop, loc = 50.0, 1.8, [0.0, -4.0, 1.5]
                shake = 0.1 if "beat_drop" in event else 0.0
            else:
                focal, fstop, loc = 20.0, 4.5, [1.0, -3.0, 1.0]
                shake = 1.5 if "beat_drop" in event else 0.0

            keyframes.append({
                "timestamp_sec": ts,
                "focal_length_mm": focal,
                "camera_location_offset": loc,
                "focus_target_location": [0.0, 0.0, 1.0],
                "screen_shake_amplitude": shake,
                "dof_aperture_fstop": fstop
            })
        return keyframes

    def _generate_blender_script(self, blend_file_path, keyframes, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        kf_json = json.dumps(keyframes)

        script_content = f"""
import bpy
import json
import random

# Load Target Environment
try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")
except Exception as e:
    print(f"Error loading blend: {{e}}")
    import sys
    sys.exit(1)

scene = bpy.context.scene
fps = scene.render.fps

# --- 1. CLEANUP OLD CAMERAS ---
for obj in bpy.data.objects:
    if obj.name.startswith("OMNIMATRIX_Cam") or obj.name.startswith("OMNIMATRIX_Focus"):
        bpy.data.objects.remove(obj, do_unlink=True)

# --- 2. AAA 3-TIER CAMERA RIG CREATION ---
# Tier 1: Focus Target (Camera tracks this, DoF locks here)
bpy.ops.object.empty_add(type='SPHERE', radius=0.2, location=(0, 0, 1))
tracker = bpy.context.active_object
tracker.name = "OMNIMATRIX_Focus_Target"

# Tier 2: Movement Root (Handles main dolly/pan paths)
bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.5, location=(0, -5, 1))
cam_root = bpy.context.active_object
cam_root.name = "OMNIMATRIX_Cam_Root"

# Tier 3: Shake Rig (Handles procedural screen shakes)
bpy.ops.object.empty_add(type='ARROWS', radius=0.3, location=(0, 0, 0))
shake_rig = bpy.context.active_object
shake_rig.name = "OMNIMATRIX_Cam_ShakeRig"
shake_rig.parent = cam_root

# Tier 4: The Actual Camera
cam_data = bpy.data.cameras.new("OMNI_Lens")
cam_obj = bpy.data.objects.new("OMNIMATRIX_Camera", cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
cam_obj.parent = shake_rig
bpy.context.scene.camera = cam_obj

# Setup Tracking & Depth of Field
track_constraint = cam_obj.constraints.new('TRACK_TO')
track_constraint.target = tracker
track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
track_constraint.up_axis = 'UP_Y'

cam = cam_obj.data
cam.dof.use_dof = True
cam.dof.focus_object = tracker

# --- 3. BAKE AI KEYFRAMES ---
kf_data = json.loads('''{kf_json}''')

# Ensure shake rig is zeroed
shake_rig.location = (0,0,0)
shake_rig.keyframe_insert(data_path="location", frame=1)

for kf in kf_data:
    frame = max(1, int(kf["timestamp_sec"] * fps))
    
    # Animate Movement Root
    root_loc = kf.get("camera_location_offset", [0, -5, 1])
    cam_root.location = (root_loc[0], root_loc[1], root_loc[2])
    cam_root.keyframe_insert(data_path="location", frame=frame)
    
    # Animate Focus Target
    focus_loc = kf.get("focus_target_location", [0, 0, 1])
    tracker.location = (focus_loc[0], focus_loc[1], focus_loc[2])
    tracker.keyframe_insert(data_path="location", frame=frame)
    
    # Animate Lens & DoF
    cam.lens = kf.get("focal_length_mm", 35.0)
    cam.keyframe_insert(data_path="lens", frame=frame)
    
    cam.dof.aperture_fstop = kf.get("dof_aperture_fstop", 2.8)
    cam.keyframe_insert(data_path="dof.aperture_fstop", frame=frame)
    
    # --- PROCEDURAL SHAKE BAKER ---
    # Instead of broken modifiers, we hard-bake random offsets into the shake rig for the duration of the impact
    shake_amp = kf.get("screen_shake_amplitude", 0.0)
    if shake_amp > 0.2:
        shake_duration = int(fps * 0.4) # Shake lasts for 0.4 seconds
        for i in range(shake_duration):
            shake_frame = frame + i
            # Dampen the shake as it progresses
            falloff = 1.0 - (i / float(shake_duration))
            current_amp = shake_amp * falloff * 0.1 # Multiplier for blender space
            
            rx = random.uniform(-current_amp, current_amp)
            ry = random.uniform(-current_amp, current_amp)
            rz = random.uniform(-current_amp, current_amp)
            
            shake_rig.location = (rx, ry, rz)
            shake_rig.keyframe_insert(data_path="location", frame=shake_frame)
            
        # Lock back to zero after shake
        shake_rig.location = (0,0,0)
        shake_rig.keyframe_insert(data_path="location", frame=frame + shake_duration + 1)

# Smooth Interpolation for Main Rig
if cam_root.animation_data and cam_root.animation_data.action:
    for fc in cam_root.animation_data.action.fcurves:
        for kfp in fc.keyframe_points:
            kfp.interpolation = 'BEZIER'
            kfp.easing = 'EASE_IN_OUT'

try:
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS")
except Exception as e:
    print(f"FAILED TO SAVE: {{str(e)}}")
"""
        script_path = os.path.join(self.workspace_dir, "temp_camera_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def design_camera_keyframes(self):
        global_style = self._load_master_config()
        self.log_message(f"Activating AAA Kinetic Camera Director [{global_style.upper()}]...", "INFO")
        
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                triggers = self._load_upstream_sync_data(scene_name)
                keyframes = self._query_camera_brain(scene_name, triggers, global_style)
                
                script_path = self._generate_blender_script(blend_file_path, keyframes, global_style)
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        self.log_message(f"God-Level Camera Rig injected into: {filename}", "SUCCESS")
                        master_blueprint[scene_name] = {"keyframes": keyframes}
                    else:
                        self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
        
        self.log_message("Universal Camera Rig Pipeline Complete.", "INFO")

if __name__ == "__main__":
    director = UniversalKineticCameraRigDirector()
    director.design_camera_keyframes()
