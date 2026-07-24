# ==============================================================================
# Ai_Agent_21_Kinetic_Camera_Rig_Director.py
# MODULE C: Blender 3D Heavy Infantry
# ==============================================================================

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

class AiAgent21KineticCameraRigDirector:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_21_Kinetic_Camera_Rig_Director"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_root = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_root, "Module_A_Scripting")
        self.audio_dir = os.path.join(self.workspace_root, "Module_B_Audio")
        self.module_c_dir = os.path.join(self.workspace_root, "Module_C_Heavy_Infantry")
        
        # Taking Environments from Agent 57 (Module H - 3D World Forge)
        self.env_dir = os.path.join(self.workspace_root, "Module_H_Generative", "3d_environments")
        self.output_blueprint = os.path.join(self.module_c_dir, "21_master_camera_blueprint.json")
        
        # System States (RULE 7)
        self.state_file = os.path.join(self.workspace_root, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_root, "global_config.json")
        
        # API Keys for Quad-Core (RULE 6)
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        for d in [self.workspace_root, self.script_dir, self.audio_dir, self.module_c_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    # RULE 4: LIMITLESS FLUIDITY
    def _load_master_config(self):
        default_config = {
            "global_style": "anime", 
            "fps": 24, 
            "blender_executable": "blender",
            "aspect_ratio": "9:16" # For Shorts/TikTok default
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except: pass
        return default_config

    def _load_upstream_sync_data(self, scene_name):
        sync_triggers = []
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        beat_file = os.path.join(self.audio_dir, "14_phonk_beat_drop_map.json")
        
        # Load Narrative Tension
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    sync_triggers.append({"timestamp_sec": 0.0, "event_type": "scene_start", "action": data.get("action_description", "Establishing shot")})
                    if "tension_peak" in data:
                        sync_triggers.append({"timestamp_sec": float(data["tension_peak"]), "event_type": "action_peak", "action": "Main dynamic action"})
            except: pass

        # Load Audio Beat Drops for Shake Impacts
        if os.path.exists(beat_file):
            try:
                with open(beat_file, "r", encoding="utf-8") as f:
                    b_data = json.load(f)
                for drop in b_data.get("beat_drops", []):
                    sync_triggers.append({
                        "timestamp_sec": drop.get("timestamp_sec", 1.5), 
                        "event_type": "beat_drop_impact", 
                        "action": "Massive screen shake impact"
                    })
            except: pass

        sync_triggers = sorted(sync_triggers, key=lambda x: x["timestamp_sec"])
        if not sync_triggers:
            sync_triggers = [
                {"timestamp_sec": 0.0, "event_type": "intro_pan", "action": "Look around"},
                {"timestamp_sec": 2.0, "event_type": "beat_drop_impact", "action": "Explosion"}
            ]
        return sync_triggers

    # RULE 5: BULLETPROOF JSON
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

    # RULE 10: PROCEDURAL FALLBACK
    def _get_procedural_fallback_keyframes(self, triggers, style):
        keyframes = []
        for trigger in triggers:
            ts = float(trigger.get("timestamp_sec", 0.0))
            event = str(trigger.get("event_type", "")).lower()

            if style == "realistic":
                focal, fstop, loc = 35.0, 1.8, [0.0, -5.0, 1.5]
                shake = 0.2 if "beat_drop" in event else 0.0
                roll = 0.0
            else: # Anime/Dynamic
                focal, fstop, loc = 18.0, 4.0, [1.0, -3.0, 1.0]
                shake = 1.8 if "beat_drop" in event else 0.0
                roll = 15.0 if "action" in event else 0.0 # Dutch angle

            keyframes.append({
                "timestamp_sec": ts,
                "focal_length_mm": focal,
                "camera_location_offset": loc,
                "focus_target_location": [0.0, 0.0, 1.0],
                "screen_shake_amplitude": shake,
                "camera_roll_degrees": roll,
                "dof_aperture_fstop": fstop
            })
        return keyframes

    # RULE 6: QUAD-CORE FALLBACK
    def _query_camera_brain(self, scene_name, triggers, config):
        style = config.get("global_style", "realistic")
        self.log(f"Calculating AAA Camera trajectories for '{scene_name}' [{style.upper()}]...", "INFO")
        
        system_prompt = f"""
        You are a AAA Cinematographer. Style: '{style.upper()}'.
        Design a kinetic camera sequence based on these timing triggers: {json.dumps(triggers)}
        
        RULES:
        - REALISTIC: Natural focal lengths (35-50mm), low aperture (f/1.8), smooth dollys, zero roll.
        - ANIME/SAKUGA: Extreme wide angles (18-24mm), dynamic Dutch Angles (camera_roll_degrees: -20 to 20), massive shakes on 'beat_drop_impact'.
        
        Return exactly 1 JSON object with the key 'camera_keyframe_data' containing a list of keyframes.
        Each keyframe MUST have:
        - 'timestamp_sec' (float)
        - 'focal_length_mm' (float)
        - 'camera_location_offset' ([X, Y, Z] float array)
        - 'focus_target_location' ([X, Y, Z] float array)
        - 'screen_shake_amplitude' (float, 0.0 for none, 1.0+ for big hits)
        - 'camera_roll_degrees' (float, for dutch angles)
        - 'dof_aperture_fstop' (float)
        """

        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": system_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self._clean_json_response(res_text)
                    if parsed and "camera_keyframe_data" in parsed: return parsed["camera_keyframe_data"]
            except: pass

        if self.openai_api_key:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
                payload = {"model": "gpt-4o", "messages": [{"role": "user", "content": system_prompt}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
                    parsed = self._clean_json_response(res_text)
                    if parsed and "camera_keyframe_data" in parsed: return parsed["camera_keyframe_data"]
            except: pass

        self.log("AI failed. Engaging Procedural Cinematographer.", "WARNING")
        return self._get_procedural_fallback_keyframes(triggers, style)

    # RULE 9 (Abstraction), RULE 12 (Kinetic Physics), RULE 13 (Sockets)
    def _generate_blender_script(self, blend_file_path, keyframes, config):
        safe_blend_path = blend_file_path.replace("\\", "/")
        fps = config.get("fps", 24)
        aspect = config.get("aspect_ratio", "9:16")
        res_x = 1080 if aspect == "9:16" else 1920
        res_y = 1920 if aspect == "9:16" else 1080
        
        kf_json = json.dumps(keyframes)

        script_content = f"""
import bpy
import json
import math
import random

# --- 0. LOAD SCENE ---
try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")
except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{e}}")
    import sys
    sys.exit(1)

scene = bpy.context.scene
scene.render.fps = {fps}
scene.render.resolution_x = {res_x}
scene.render.resolution_y = {res_y}

# --- 1. CLEANUP OLD CAMERAS ---
for obj in bpy.data.objects:
    if "OMNIMATRIX_Cam" in obj.name or "OMNIMATRIX_Focus" in obj.name:
        bpy.data.objects.remove(obj, do_unlink=True)

# --- 2. 4-TIER AAA KINETIC RIG ---
# Tier 1: Focus Target
bpy.ops.object.empty_add(type='SPHERE', radius=0.2, location=(0, 0, 1))
tracker = bpy.context.active_object
tracker.name = "OMNIMATRIX_Focus_Target"

# Tier 2: Movement Root Dolly
bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.5, location=(0, -5, 1))
cam_root = bpy.context.active_object
cam_root.name = "OMNIMATRIX_Cam_Root"

# Tier 3: Shake & Roll Rig
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

# Connect Focus & DoF
track_constraint = cam_obj.constraints.new('TRACK_TO')
track_constraint.target = tracker
track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
track_constraint.up_axis = 'UP_Y'

cam_data.dof.use_dof = True
cam_data.dof.focus_object = tracker

# --- RULE 13: SOCKET PROTOCOL AUTO-TRACKING ---
# If a character or text socket exists, gently parent the focus target to it dynamically
socket_target = None
if "CHAR_SOCKET" in bpy.data.objects:
    socket_target = bpy.data.objects["CHAR_SOCKET"]
elif "TXT_SOCKET" in bpy.data.objects:
    socket_target = bpy.data.objects["TXT_SOCKET"]

if socket_target:
    copy_loc = tracker.constraints.new('COPY_LOCATION')
    copy_loc.target = socket_target
    copy_loc.influence = 0.5 # Blend between AI coords and socket coords

# --- 3. BAKE AI KEYFRAMES ---
kf_data = json.loads('''{kf_json}''')

shake_rig.location = (0,0,0)
shake_rig.rotation_euler = (0,0,0)

for kf in kf_data:
    frame = max(1, int(kf["timestamp_sec"] * {fps}))
    
    # Root Loc
    r_loc = kf.get("camera_location_offset", [0, -5, 1])
    cam_root.location = (r_loc[0], r_loc[1], r_loc[2])
    cam_root.keyframe_insert(data_path="location", frame=frame)
    
    # Focus Loc
    f_loc = kf.get("focus_target_location", [0, 0, 1])
    tracker.location = (f_loc[0], f_loc[1], f_loc[2])
    tracker.keyframe_insert(data_path="location", frame=frame)
    
    # Lens & DoF
    cam_data.lens = kf.get("focal_length_mm", 35.0)
    cam_data.keyframe_insert(data_path="lens", frame=frame)
    cam_data.dof.aperture_fstop = kf.get("dof_aperture_fstop", 2.8)
    cam_data.keyframe_insert(data_path="dof.aperture_fstop", frame=frame)
    
    # Dutch Angle (Roll)
    roll_rad = math.radians(kf.get("camera_roll_degrees", 0.0))
    shake_rig.rotation_euler[2] = roll_rad # Z-axis of shake rig affects roll
    shake_rig.keyframe_insert(data_path="rotation_euler", index=2, frame=frame)

    # Hard-Baked Screen Shake on Beats
    shake_amp = kf.get("screen_shake_amplitude", 0.0)
    if shake_amp > 0.2:
        shake_frames = int({fps} * 0.4) # Shake lasts 0.4s
        for i in range(shake_frames):
            sf = frame + i
            falloff = 1.0 - (i / float(shake_frames))
            current_amp = shake_amp * falloff * 0.1
            shake_rig.location = (random.uniform(-current_amp, current_amp), 
                                  random.uniform(-current_amp, current_amp), 
                                  random.uniform(-current_amp, current_amp))
            shake_rig.keyframe_insert(data_path="location", frame=sf)
        shake_rig.location = (0,0,0)
        shake_rig.keyframe_insert(data_path="location", frame=frame + shake_frames + 1)

# --- 4. ORGANIC HANDHELD NOISE (RULE 12) ---
# Give the camera root a subtle ambient breathing effect
cam_root.keyframe_insert(data_path="location", frame=1)
if cam_root.animation_data and cam_root.animation_data.action:
    for fc in cam_root.animation_data.action.fcurves:
        if fc.data_path == 'location':
            mod = fc.modifiers.new('NOISE')
            mod.scale = 50.0
            mod.strength = 0.05 # Very subtle breathing
            
            # Smooth out AI keyframes
            for kfp in fc.keyframe_points:
                kfp.interpolation = 'BEZIER'
                kfp.easing = 'EASE_IN_OUT'

try:
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")
except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_camera_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def design_camera_keyframes(self):
        self.log("Initializing Kinetic Camera Matrix...", "INFO")

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
        blender_executable = config.get("blender_executable", "blender")
        
        master_blueprint = {}
        
        # Ensure we have environments to attach cameras to
        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("No 3D environments found. Camera Director waiting...", "WARNING")
            sys.exit(0)
            
        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                scene_name = filename.replace("_stage.blend", "").replace(".blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                triggers = self._load_upstream_sync_data(scene_name)
                keyframes = self._query_camera_brain(scene_name, triggers, config)
                
                script_path = self._generate_blender_script(blend_file_path, keyframes, config)
                
                command = [blender_executable, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                        self.log(f"God-Level Camera Rig injected into: {filename}", "SUCCESS")
                        master_blueprint[scene_name] = {"keyframes": keyframes}
                    else:
                        self.log(f"Blender failed: {result.stdout[-250:]}", "ERROR")
                except Exception as e:
                    self.log(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: ATOMIC HANDSHAKE (Advance State)
        state["last_active_agent"] = self.agent_name
        # Heading to Atmospheric Lighting Shader Baker!
        state["next_agent"] = "Ai_Agent_22_Atmospheric_Lighting_Shader_Baker"
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
        
        self.log(f"Kinetic Camera Pipeline Complete! Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    director = AiAgent21KineticCameraRigDirector()
    director.design_camera_keyframes()

# ==============================================================================
# END OF FILE
# ==============================================================================
