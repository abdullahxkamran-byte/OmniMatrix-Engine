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
                    # Universal Uppercase API Keys
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class OmniMatrixHitStopScheduler:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 28: OmniMatrix Hit-Stop & Time Remapper"
        
        # Directories
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.env_dir, "28_time_remap_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_scene_context_and_collisions(self, scene_name):
        """Loads visual style and collision data from Agent 27"""
        context = {
            "visual_style": "omni_neutral",
            "impact_frame": 0,
            "has_impact": False
        }
        
        # 1. Load Style Context
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "omni_neutral")
            except:
                pass

        # 2. Load Collision Data (from Agent 27)
        collision_file = os.path.join(self.env_dir, "27_collision_blueprint.json")
        if os.path.exists(collision_file):
            try:
                with open(collision_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        scene_data = data[scene_name]
                        context["has_impact"] = scene_data.get("has_major_impact", False)
                        context["impact_frame"] = scene_data.get("impact_frame", 0)
            except Exception as e:
                self.log_message(f"Collision data read error: {e}", "WARNING")
                
        return context

    def _query_time_director(self, scene_name, context):
        if not context["has_impact"]:
            return self._fallback_schedule(False)

        if not self.gemini_api_key:
            return self._fallback_schedule(True)

        ai_prompt = (
            f"You are the Lead Editor and Time Remapping Director for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Impact Frame: {context['impact_frame']}\n\n"
            "An impact has been detected. Determine the time dilation and camera shake needed based on the style.\n"
            "- If style is 'anime', use a sharp freeze (hit-stop), heavy zoom, and fast shake.\n"
            "- If style is 'realistic' or 'cinematic', use a speed-ramp (slow-mo), moderate zoom, and subtle bass-shake.\n"
            "- If style is 'pixar/cartoon', use a bouncy, elastic impact without too much violence.\n"
            "Return ONLY raw JSON:\n"
            "{\n"
            "  \"impact_frame\": " + str(context['impact_frame']) + ",\n"
            "  \"freeze_duration_frames\": 6,\n"
            "  \"time_scale_factor\": 0.1,\n"
            "  \"camera_zoom_amplitude\": 0.5,\n"
            "  \"camera_shake_strength\": 15.0,\n"
            "  \"vfx_flash_style\": \"color_dodge_flash\",\n"
            "  \"director_notes\": \"Applied a heavy impact slow-mo ramp.\"\n"
            "}"
        )

        try:
            payload = {"contents": [{"parts": [{"text": ai_prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                return json.loads(res_text)
        except Exception as e:
            self.log_message(f"AI Time Director failed: {str(e)}. Using fallback.", "WARNING")
            return self._fallback_schedule(True, context["impact_frame"])

    def _fallback_schedule(self, has_impact, frame=0):
        if not has_impact:
            return {
                "impact_frame": 0, "freeze_duration_frames": 0, "time_scale_factor": 1.0,
                "camera_zoom_amplitude": 0.0, "camera_shake_strength": 0.0,
                "vfx_flash_style": "none", "director_notes": "No impact, standard playback."
            }
        return {
            "impact_frame": frame, "freeze_duration_frames": 5, "time_scale_factor": 0.2,
            "camera_zoom_amplitude": 0.3, "camera_shake_strength": 10.0,
            "vfx_flash_style": "subtle_white_flash", "director_notes": "Fallback impact applied."
        }

    def _generate_blender_script(self, blend_file_path, time_data):
        """Python script to inject Camera Shake and Zoom directly into Blender via Headless Mode."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    impact_frame = {time_data.get('impact_frame', 0)}
    shake_str = {time_data.get('camera_shake_strength', 0.0)}
    zoom_amp = {time_data.get('camera_zoom_amplitude', 0.0)}
    freeze_frames = {time_data.get('freeze_duration_frames', 0)}

    if impact_frame > 0 and shake_str > 0:
        cam = bpy.context.scene.camera
        if cam:
            # 1. Apply Camera Focal Length (Zoom) Punch
            cam.data.keyframe_insert(data_path="lens", frame=impact_frame - 1)
            original_lens = cam.data.lens
            cam.data.lens = original_lens - (zoom_amp * 20) # Zoom in
            cam.data.keyframe_insert(data_path="lens", frame=impact_frame)
            cam.data.lens = original_lens # Restore
            cam.data.keyframe_insert(data_path="lens", frame=impact_frame + freeze_frames)

            # 2. Apply Camera Shake (F-Curve Noise Modifier) on Location
            cam.keyframe_insert(data_path="location", frame=impact_frame)
            
            if cam.animation_data and cam.animation_data.action:
                for fcurve in cam.animation_data.action.fcurves:
                    if fcurve.data_path == "location":
                        # Add Noise Modifier to X, Y, Z
                        mod = fcurve.modifiers.new('NOISE')
                        mod.strength = shake_str * 0.05
                        mod.scale = 2.0
                        
                        # Restrict noise ONLY to the impact duration
                        mod.use_restricted_range = True
                        mod.frame_start = impact_frame
                        mod.frame_end = impact_frame + freeze_frames

        bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
        print("SUCCESS: Camera shake and time impact markers baked into scene.")
    else:
        print("INFO: No major impact detected for this scene.")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_hitstop_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_hit_stops(self):
        self.log_message("Initializing OmniMatrix Time Remapping Director...", "INFO")
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_scene_context_and_collisions(scene_name)
                
                if context["has_impact"]:
                    self.log_message(f"--- Processing Impact for: {scene_name} ---", "INFO")
                    time_data = self._query_time_director(scene_name, context)
                    
                    self.log_message(f"AI Decision: {time_data['director_notes']} (Shake: {time_data['camera_shake_strength']}, Style: {time_data['vfx_flash_style']})", "INFO")
                    
                    script_path = self._generate_blender_script(blend_file_path, time_data)
                    
                    command = [self.blender_path, "-b", "-P", script_path]
                    try:
                        result = subprocess.run(command, capture_output=True, text=True)
                        if result.returncode == 0:
                            self.log_message(f"Time Dilation & Shake applied to {filename}", "INFO")
                            master_blueprint[scene_name] = time_data
                        else:
                            self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                    except Exception as e:
                        self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                        
                    if os.path.exists(script_path):
                        os.remove(script_path)
                else:
                    self.log_message(f"Scene '{scene_name}' has no major impacts. Skipping Time-Remap.", "INFO")
                    master_blueprint[scene_name] = self._fallback_schedule(False)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 28 Pipeline Complete. Impacts are now cinematically styled.", "INFO")

if __name__ == "__main__":
    scheduler = OmniMatrixHitStopScheduler()
    scheduler.process_hit_stops()
