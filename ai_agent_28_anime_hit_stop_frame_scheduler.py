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
                    # Universal Uppercase API Keys
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class OmniMatrixHitStopScheduler:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 28: aaa_hitstop_time_remapper"
        
        # Directories
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.workspace_dir, "28_time_remap_blueprint.json")
        self.blender_path = blender_path
        
        # GEMINI API INTEGRATION
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.workspace_dir, self.script_dir, self.env_dir]:
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
            except Exception as e:
                self.log_message(f"Style context parse error: {str(e)}", "WARNING")

        # 2. Load Collision Data (from Agent 27)
        collision_file = os.path.join(self.workspace_dir, "27_collision_blueprint.json")
        if os.path.exists(collision_file):
            try:
                with open(collision_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        scene_data = data[scene_name]
                        context["has_impact"] = scene_data.get("has_major_impact", False)
                        context["impact_frame"] = scene_data.get("impact_frame", 0)
            except Exception as e:
                self.log_message(f"Collision data read error: {str(e)}", "WARNING")
                
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

    def _query_time_director(self, scene_name, context):
        if not context["has_impact"]:
            return self._fallback_schedule(False)

        self.log_message(f"Calculating Hit-Stop & Time-Remap vectors for '{scene_name}'...", "INFO")

        if not self.gemini_api_key:
            self.log_message("No Gemini API Key found. Using fallback schedule.", "WARNING")
            return self._fallback_schedule(True, context["impact_frame"])

        ai_prompt = (
            f"You are the Lead Editor and Time Remapping Director for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Impact Frame: {context['impact_frame']}\n\n"
            "An impact has been detected. Determine the time dilation and camera shake needed based on the style.\n"
            "- If style is 'anime', use a sharp freeze (hit-stop), heavy zoom, and fast shake.\n"
            "- If style is 'realistic' or 'cinematic', use a speed-ramp (slow-mo), moderate zoom, and subtle bass-shake.\n"
            "- If style is 'pixar/cartoon', use a bouncy, elastic impact without too much violence.\n"
            "Return EXACTLY 1 raw JSON object containing:\n"
            "{\n"
            f"  \"impact_frame\": {context['impact_frame']},\n"
            "  \"freeze_duration_frames\": 6,\n"
            "  \"time_scale_factor\": 0.1,\n"
            "  \"camera_zoom_amplitude\": 0.5,\n"
            "  \"camera_shake_strength\": 15.0,\n"
            "  \"vfx_flash_style\": \"color_dodge_flash\",\n"
            "  \"director_notes\": \"Applied a heavy impact slow-mo ramp.\"\n"
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

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

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
                        # Clean up existing NOISE modifiers to prevent stacking on re-runs
                        for mod in fcurve.modifiers:
                            if mod.type == 'NOISE':
                                fcurve.modifiers.remove(mod)

                        # Add new Noise Modifier
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
        print("SUCCESS: No major impact detected for this scene. Proceeding normally.")

except Exception as e:
    print(f"ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_hitstop_script.py")
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
                    
                    self.log_message(f"AI Decision: {time_data.get('director_notes', 'Applied Hit-Stop')} (Shake: {time_data.get('camera_shake_strength')})", "INFO")
                    
                    script_path = self._generate_blender_script(blend_file_path, time_data)
                    
                    command = [self.blender_path, "-b", "-P", script_path]
                    try:
                        result = subprocess.run(command, capture_output=True, text=True)
                        if result.returncode == 0 and "SUCCESS" in result.stdout:
                            self.log_message(f"Time Dilation & Shake applied to {filename}", "SUCCESS")
                            master_blueprint[scene_name] = time_data
                        else:
                            self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
                    except Exception as e:
                        self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                        
                    if os.path.exists(script_path):
                        os.remove(script_path)
                else:
                    self.log_message(f"[{scene_name}] No major impacts. Skipping Time-Remap.", "INFO")
                    master_blueprint[scene_name] = self._fallback_schedule(False)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 28 Pipeline Complete. Impacts are now cinematically styled.", "INFO")

if __name__ == "__main__":
    scheduler = OmniMatrixHitStopScheduler()
    scheduler.process_hit_stops()
