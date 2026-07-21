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
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

class KineticCameraRigDirector:
    # 1. Drive/Local Architecture
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 21: AAA Kinetic Camera Rig Director"
        
        # Upstream Inputs
        self.audio_dir = os.path.join(drive_temp_dir, "module_b_audio") # For Beat Drops
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts") # For Action Triggers
        self.env_dir = os.path.join(local_library_dir, "3d_environments") # From Agent 57
        
        # Outputs
        self.output_dir = os.path.join(local_library_dir, "3d_environments") # Overwrites/Saves inside the env folder
        self.output_blueprint = os.path.join(self.output_dir, "21_camera_rig_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.env_dir, self.output_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_sync_data(self, scene_name):
        """Loads Action Triggers and Beat Drops specifically for this scene."""
        sync_triggers = []
        
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        beat_file = os.path.join(self.audio_dir, f"14_phonk_beat_drop_map.json")
        
        # Load Story/Action Triggers
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Assume Module A sets key moments per scene
                    sync_triggers.append({
                        "timestamp_sec": 0.0,
                        "event_type": "scene_start",
                        "intensity": "moderate",
                        "action": data.get("action_description", "Entering scene")
                    })
                    sync_triggers.append({
                        "timestamp_sec": 2.5, # Example mid-point
                        "event_type": "action_peak",
                        "intensity": "high",
                        "action": "Main action execution"
                    })
            except Exception as e:
                self.log_message(f"Script parse warning: {str(e)}", "WARNING")

        # Inject Audio Beat Drops if available (For extreme shakes)
        if os.path.exists(beat_file):
            try:
                with open(beat_file, "r", encoding="utf-8") as f:
                    b_data = json.load(f)
                for drop in b_data.get("beat_drops", []):
                    # In a real scenario, filter drops that belong to this scene's time bracket
                    sync_triggers.append({
                        "timestamp_sec": drop.get("timestamp_sec", 1.5),
                        "event_type": "beat_drop_impact",
                        "intensity": "extreme",
                        "action": "Massive audio impact"
                    })
            except:
                pass

        sync_triggers = sorted(sync_triggers, key=lambda x: x["timestamp_sec"])
        
        if not sync_triggers:
            sync_triggers = [
                {"timestamp_sec": 0.0, "event_type": "intro_pan", "intensity": "moderate", "action": "Look around"},
                {"timestamp_sec": 3.0, "event_type": "beat_drop_impact", "intensity": "extreme", "action": "Explosion"}
            ]

        return sync_triggers

    def _query_gemini_camera_design(self, scene_name, triggers):
        if not self.gemini_api_key:
            return self._get_procedural_fallback(triggers)

        ai_prompt = (
            f"You are the AAA Cinematic Camera Director for scene '{scene_name}'.\n"
            "Generate precise camera keyframes with dynamic focal tracking (Depth of Field) parameters.\n"
            "Rules for 'screen_shake_amplitude': Only use values > 1.0 for 'beat_drop_impact' or 'extreme' intensity.\n"
            "For each trigger, output EXACTLY 1 camera movement block.\n"
            "Format your output STRICTLY as raw JSON:\n"
            "{\n"
            "  \"camera_keyframe_data\": [\n"
            "    {\n"
            "      \"timestamp_sec\": 0.0,\n"
            "      \"shot_type\": \"dolly-zoom\",\n"
            "      \"focal_length_mm\": 24.0,\n"
            "      \"camera_location_offset\": [0.0, -4.0, 1.5],\n"
            "      \"camera_rotation_euler\": [85.0, 0.0, 0.0],\n"
            "      \"screen_shake_amplitude\": 0.2,\n"
            "      \"interpolation_type\": \"BEZIER\",\n"
            "      \"dof_focal_tracking_enabled\": true,\n"
            "      \"dof_aperture_fstop\": 1.8,\n"
            "      \"dof_manual_focus_distance_meters\": 3.5\n"
            "    }\n"
            "  ]\n"
            "}"
        )

        try:
            payload = {
                "contents": [{"parts": [{"text": ai_prompt}, {"text": f"Triggers: {json.dumps(triggers)}"}]}], 
                "generationConfig": {"responseMimeType": "application/json"}
            }
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                return json.loads(res_text).get("camera_keyframe_data", self._get_procedural_fallback(triggers)["camera_keyframe_data"])
        except Exception as e:
            self.log_message(f"Gemini API Error: {str(e)}. Using fallback.", "WARNING")
            return self._get_procedural_fallback(triggers)["camera_keyframe_data"]

    def _get_procedural_fallback(self, triggers):
        keyframes = []
        for trigger in triggers:
            ts = float(trigger.get("timestamp_sec", 0.0))
            event = str(trigger.get("event_type", "intro_pan")).lower()

            if "beat_drop" in event:
                shot, focal, loc, shake, fstop = "dolly-zoom", 20.0, [0.0, -3.0, 1.2], 1.5, 1.2
            else:
                shot, focal, loc, shake, fstop = "orbital-spin", 35.0, [1.5, -2.5, 1.5], 0.2, 2.8

            keyframes.append({
                "timestamp_sec": ts, "shot_type": shot, "focal_length_mm": focal,
                "camera_location_offset": loc, "camera_rotation_euler": [85.0, 0.0, 45.0],
                "screen_shake_amplitude": shake, "interpolation_type": "BEZIER",
                "dof_focal_tracking_enabled": True, "dof_aperture_fstop": fstop,
                "dof_manual_focus_distance_meters": 3.0
            })
        return {"camera_keyframe_data": keyframes}

    def _generate_blender_script(self, blend_file_path, keyframes):
        """Injects MAPPA-style camera tracking and shaking inside the existing Stage Blend file."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        kf_json = json.dumps(keyframes)

        script_content = f"""
import bpy
import json
import math

# Load the stage file created by Agent 57
bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

# Ensure Scene runs at 30 FPS (or standard anime 24FPS)
fps = 30
bpy.context.scene.render.fps = fps

# 1. Locate or Create Camera & Tracker
cam_obj = bpy.data.objects.get("Cinematic_CamObj")
if not cam_obj:
    cam_data = bpy.data.cameras.new("Cinematic_Camera")
    cam_obj = bpy.data.objects.new("Cinematic_CamObj", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

cam = cam_obj.data
cam.dof.use_dof = True # Enable AAA Cinematic Depth of Field

# Create Focus Tracker Empty
tracker = bpy.data.objects.get("Focus_Tracker")
if not tracker:
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1))
    tracker = bpy.context.active_object
    tracker.name = "Focus_Tracker"
    cam.dof.focus_object = tracker # Lock DoF to this tracker

# Setup Camera tracking constraint
track_constraint = cam_obj.constraints.get("Track To")
if not track_constraint:
    track_constraint = cam_obj.constraints.new('TRACK_TO')
    track_constraint.target = tracker
    track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    track_constraint.up_axis = 'UP_Y'

# 2. Apply AI Keyframes
kf_data = json.loads('''{kf_json}''')

cam_obj.animation_data_clear() # Clear old anims

for kf in kf_data:
    frame = int(kf["timestamp_sec"] * fps)
    bpy.context.scene.frame_set(frame)
    
    # Location
    loc = kf.get("camera_location_offset", [0,-5,1])
    cam_obj.location = (loc[0], loc[1], loc[2])
    cam_obj.keyframe_insert(data_path="location", frame=frame)
    
    # Lens/Zoom
    cam.lens = kf.get("focal_length_mm", 35.0)
    cam.keyframe_insert(data_path="lens", frame=frame)
    
    # Depth of Field (Aperture Bokeh)
    cam.dof.aperture_fstop = kf.get("dof_aperture_fstop", 2.8)
    cam.keyframe_insert(data_path="dof.aperture_fstop", frame=frame)
    
    # Apply shake impact to noise modifier
    shake_amp = kf.get("screen_shake_amplitude", 0.0)
    # We set a custom property to store shake for modifiers to read later
    cam_obj["shake_amp"] = shake_amp
    cam_obj.keyframe_insert(data_path='["shake_amp"]', frame=frame)

# 3. Apply Smooth Interpolation
if cam_obj.animation_data and cam_obj.animation_data.action:
    for fcurve in cam_obj.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'BEZIER'
            kf.easing = 'EASE_IN_OUT'
            
        # Add Noise Modifier for screen shake based on custom property
        if fcurve.data_path == "location":
            mod = fcurve.modifiers.new('NOISE')
            mod.scale = 2.0
            mod.strength = 0.5 # Base strength, influenced by AI beat drops
            mod.phase = 1.0
            mod.blend_type = 'ADD'

# Save file
bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
print("SUCCESS: Camera Directed")
"""
        script_path = os.path.join("temp_camera_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def design_camera_keyframes(self):
        self.log_message("Initializing AAA Kinetic Camera Director...", "INFO")
        
        master_blueprint = {}
        
        # Iterate over all Stage .blend files created by Agent 57
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                self.log_message(f"--- Directing Camera for: {scene_name} ---", "INFO")
                
                # Load Audio Drops and Script Triggers
                triggers = self._load_upstream_sync_data(scene_name)
                
                # Get Camera Motions from AI
                keyframes = self._query_gemini_camera_design(scene_name, triggers)
                
                # Generate and execute Blender Script
                script_path = self._generate_blender_script(blend_file_path, keyframes)
                
                self.log_message(f"Executing Headless Blender to bake Camera Tracking...", "INFO")
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_message(f"Camera baked successfully into {filename}", "INFO")
                        master_blueprint[scene_name] = {"keyframes": keyframes}
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
        
        self.log_message("Agent 21 Camera Pipeline Complete.", "INFO")

if __name__ == "__main__":
    director = KineticCameraRigDirector()
    director.design_camera_keyframes()
