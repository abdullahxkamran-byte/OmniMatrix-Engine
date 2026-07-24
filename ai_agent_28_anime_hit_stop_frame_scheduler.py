# ==============================================================================
# Ai_Agent_28_Anime_Hit_Stop_Frame_Scheduler.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL TIME MANIPULATOR)
# ==============================================================================

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
                    # UNIVERSAL UPPERCASE FIX
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiAgent28AnimeHitStopFrameScheduler:
    def __init__(self):
        # RULE 8: STRICT AI NAMING
        self.agent_name = "Ai_Agent_28_Anime_Hit_Stop_Frame_Scheduler"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "28_time_remap_blueprint.json")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_dir, "global_config.json")
        self.collision_file = os.path.join(self.module_c_dir, "27_collision_blueprint.json")
        
        # RULE 6: DUAL API FAILSAFES
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

    def _load_scene_context_and_collisions(self, scene_name):
        context = {
            "action_description": "Characters in scene",
            "impact_frame": 0,
            "has_impact": False
        }
        
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["action_description"] = data.get("action_description", "Characters interacting.")
            except: pass

        if os.path.exists(self.collision_file):
            try:
                with open(self.collision_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        scene_data = data[scene_name]
                        # Support for both Agent 27's output formats
                        context["has_impact"] = scene_data.get("has_major_impact", scene_data.get("intentional_contact", False))
                        context["impact_frame"] = scene_data.get("impact_frame", 24) # Default to 24 if not explicitly set
            except: pass
                
        return context

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

    def _fallback_schedule(self, has_impact, style):
        if not has_impact:
            return {
                "impact_frame": 0, "freeze_duration_frames": 0, "time_scale_factor": 1.0,
                "camera_zoom_amplitude": 0.0, "camera_shake_strength": 0.0,
                "rationale": "No impact, linear playback."
            }
        
        is_anime = "anime" in style
        return {
            "impact_frame": 24, 
            "freeze_duration_frames": 8 if is_anime else 0, 
            "time_scale_factor": 1.0 if is_anime else 0.3,
            "camera_zoom_amplitude": 1.5 if is_anime else 0.5, 
            "camera_shake_strength": 25.0 if is_anime else 10.0,
            "rationale": "Procedural Hit-Stop Fallback."
        }

    # LIMITLESS AI TIME DIRECTOR
    def _query_time_director(self, scene_name, context, style):
        if not context["has_impact"]:
            return self._fallback_schedule(False, style)

        self.log(f"Calculating Time Remap & Sakuga Freeze for '{scene_name}'...", "INFO")

        ai_prompt = f"""
        You are the AAA Action Editor for the OmniMatrix Engine.
        Scene: '{scene_name}' | Style: '{style.upper()}' | Action: {context['action_description']}
        Impact detected around Frame {context['impact_frame']}.
        
        CRITICAL RULE:
        - If Style is ANIME: We need a Sakuga "Hit-Stop". Use a high `freeze_duration_frames` (e.g., 6 to 12 frames), extreme `camera_shake_strength` (20-40), and an aggressive `camera_zoom_amplitude` (1.0 - 2.0).
        - If Style is REALISTIC: We need a Cinematic Slow-Mo. `freeze_duration_frames` MUST be 0. Use `time_scale_factor` (e.g., 0.2) to stretch time, moderate shake (5-15), and slight zoom (0.2 - 0.5).
        
        Return ONLY valid JSON:
        {{
            "impact_frame": {context['impact_frame']},
            "freeze_duration_frames": integer,
            "time_scale_factor": float (1.0 for normal, 0.2 for slow-mo),
            "camera_zoom_amplitude": float,
            "camera_shake_strength": float,
            "rationale": "Brief reason"
        }}
        """

        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self._clean_json_response(res_text)
                    if parsed: return parsed
            except: pass

        return self._fallback_schedule(True, style)

    # GOD-LEVEL BLENDER SCRIPT: F-CURVE SPLITTING & TIME RAMPING
    def _generate_blender_script(self, blend_file_path, time_data, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        is_anime = "True" if "anime" in style or "cel" in style else "False"
        
        script_content = f"""
import bpy

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    impact_frame = {time_data.get('impact_frame', 0)}
    shake_str = {time_data.get('camera_shake_strength', 0.0)}
    zoom_amp = {time_data.get('camera_zoom_amplitude', 0.0)}
    freeze_frames = {time_data.get('freeze_duration_frames', 0)}
    time_scale = {time_data.get('time_scale_factor', 1.0)}
    is_anime = {is_anime}

    if impact_frame > 0:
        # --- 1. TRUE HIT-STOP (ANIME F-CURVE SPLIT) ---
        if is_anime and freeze_frames > 0:
            print("EXECUTING LIMITLESS ANIME HIT-STOP: Freezing the world...")
            for obj in bpy.context.scene.objects:
                if obj.animation_data and obj.animation_data.action:
                    for fcurve in obj.animation_data.action.fcurves:
                        # Skip camera location curves so camera shake still works!
                        if obj.type == 'CAMERA' and fcurve.data_path == 'location':
                            continue
                            
                        # Shift all keyframes AFTER the impact frame to create a true pause
                        for kf in fcurve.keyframe_points:
                            if kf.co[0] > impact_frame:
                                kf.co[0] += freeze_frames
                                kf.handle_left[0] += freeze_frames
                                kf.handle_right[0] += freeze_frames
                        fcurve.update()
                        
        # --- 2. CINEMATIC SLOW-MO (REALISTIC TIME MAP) ---
        elif not is_anime and time_scale < 1.0:
            print("EXECUTING REALISTIC SLOW-MO RAMP...")
            # Use Blender's Time Stretching
            bpy.context.scene.render.use_simplify = False
            # We scale the scene timeline. E.g., Map 100 frames to 300 frames.
            # In a pure python headless script, the most stable way is NLA Time Scale or FPS map.
            bpy.context.scene.render.fps_base = 1.0 / time_scale

        # --- 3. DYNAMIC CAMERA ZOOM & PUNCH ---
        cam = bpy.context.scene.camera
        if cam and zoom_amp > 0:
            if not cam.data.animation_data:
                cam.data.animation_data_create()
                
            # Keyframe Lens
            cam.data.keyframe_insert(data_path="lens", frame=impact_frame - 1)
            original_lens = cam.data.lens
            
            # Violent Punch-In
            cam.data.lens = original_lens + (zoom_amp * 15.0) 
            cam.data.keyframe_insert(data_path="lens", frame=impact_frame)
            
            # Snap back after hit-stop
            cam.data.lens = original_lens
            cam.data.keyframe_insert(data_path="lens", frame=impact_frame + freeze_frames + 2)

        # --- 4. VIOLENT CAMERA SHAKE (NOISE MODIFIER) ---
        if cam and shake_str > 0:
            cam.keyframe_insert(data_path="location", frame=impact_frame)
            if cam.animation_data and cam.animation_data.action:
                for fcurve in cam.animation_data.action.fcurves:
                    if fcurve.data_path == "location":
                        # Clear old
                        for mod in fcurve.modifiers:
                            if mod.type == 'NOISE':
                                fcurve.modifiers.remove(mod)
                        
                        # Add restricted Noise
                        mod = fcurve.modifiers.new('NOISE')
                        mod.strength = shake_str * 0.02
                        mod.scale = 5.0 # Fast judder
                        mod.use_restricted_range = True
                        mod.frame_start = impact_frame
                        mod.frame_end = impact_frame + max(freeze_frames, 10)

        bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
        print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_hitstop_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 28 (Anime Hit Stop & Time Scheduler)...", "INFO")

        # RULE 7: ATOMIC HANDSHAKE
        state = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
            except: pass

        if state.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Expected '{state.get('next_agent')}'.", "WARNING")
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
                
                context = self._load_scene_context_and_collisions(scene_name)
                
                if context["has_impact"]:
                    self.log(f"[{scene_name}] Impact Detected. Generating Temporal Matrix...", "INFO")
                    time_data = self._query_time_director(scene_name, context, global_style)
                    
                    self.log(f"AI Decision: {time_data.get('rationale', '')} (Freeze: {time_data.get('freeze_duration_frames')} | Zoom: {time_data.get('camera_zoom_amplitude')})", "INFO")
                    
                    script_path = self._generate_blender_script(blend_file_path, time_data, global_style)
                    command = [blender_executable, "-b", "-P", script_path]
                    
                    try:
                        result = subprocess.run(command, capture_output=True, text=True)
                        if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                            self.log(f"Time Dilation & Shake successfully baked into {filename}", "SUCCESS")
                            master_blueprint[scene_name] = time_data
                        else:
                            self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                    except Exception as e:
                        self.log(f"Execution failed: {str(e)}", "CRITICAL")
                        
                    if os.path.exists(script_path):
                        os.remove(script_path)
                else:
                    self.log(f"[{scene_name}] No impacts detected. Standard timeline maintained.", "INFO")
                    master_blueprint[scene_name] = self._fallback_schedule(False, global_style)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # STATE UPDATE: Trigger Smear Frames Next
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "Ai_Agent_29_Dynamic_Smear_Frame_Generator"
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Hit-Stop & Temporal Adjustments Complete. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    scheduler = AiAgent28AnimeHitStopFrameScheduler()
    scheduler.execute_pipeline()

# ==============================================================================
# END OF FILE
# ==============================================================================
