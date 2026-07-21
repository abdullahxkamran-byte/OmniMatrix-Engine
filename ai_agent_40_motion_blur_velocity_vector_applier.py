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

class AiMotionBlurVelocityVectorApplier:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 40: motion_blur_velocity_vector_applier"
        self.workspace_dir = workspace_dir
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        self.blender_path = blender_path
        
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        for d in [self.workspace_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_kinetics(self):
        kinetic_path = os.path.join(self.workspace_dir, "26_kinetic_rig_puppeteer_blueprint.json")
        speed_path = os.path.join(self.workspace_dir, "36_volumetric_speed_lines_blueprint.json")
        velocity_contexts = []

        if os.path.exists(speed_path):
            try:
                with open(speed_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for profile in data.get("speed_line_profiles", []):
                    velocity_contexts.append({
                        "timestamp_sec": profile.get("timestamp_sec", 0.0),
                        "speed_style": profile.get("speed_line_style", "radial_zoom_in"),
                        "implied_velocity": 25.0 if "zoom" in profile.get("speed_line_style", "") else 12.0
                    })
            except Exception as e:
                self.log_message(f"Speed lines blueprint read warning: {str(e)}", "WARNING")

        if not velocity_contexts and os.path.exists(kinetic_path):
            try:
                with open(kinetic_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for seq in data.get("rig_animation_sequences", []):
                    offset = seq.get("translation_offset", [0.0, 0.0, 0.0])
                    speed_magnitude = (offset[0]**2 + offset[1]**2 + offset[2]**2)**0.5
                    velocity_contexts.append({
                        "timestamp_sec": seq.get("timestamp_sec", 0.0),
                        "speed_style": "kinetic_displacement",
                        "implied_velocity": round(speed_magnitude, 2)
                    })
            except Exception as e:
                self.log_message(f"Kinetic rig blueprint read warning: {str(e)}", "WARNING")

        if not velocity_contexts:
            self.log_message("No motion data. Injecting standard action sequence vectors.", "INFO")
            velocity_contexts = [
                {"timestamp_sec": 1.2, "speed_style": "radial_zoom_in", "implied_velocity": 45.5},
                {"timestamp_sec": 3.5, "speed_style": "horizontal_streaks", "implied_velocity": 8.2}
            ]

        return velocity_contexts

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

    def _save_to_workspace(self, data, filename="40_motion_blur_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log_message(f"Motion blur parameters saved to '{file_path}'", "INFO")
            return file_path
        except Exception as e:
            self.log_message(f"Critical Error: Unable to save blur blueprint: {str(e)}", "CRITICAL")
            return None

    def design_stylized_motion_blur(self):
        velocities = self._load_upstream_kinetics()
        self.log_message("Solving vector passes and hand-drawn smear values...", "INFO")

        system_prompt = (
            "You are a Senior Technical Director specialized in anime-style motion smears and shutter angle styling.\n"
            "Translate 3D physical speed into stylized, traditional-looking motion blur commands.\n"
            "For each movement entry, generate exactly 1 configuration inside a list named 'motion_blur_profiles':\n"
            "- 'timestamp_sec': float matching the video timestamp.\n"
            "- 'blur_render_type': string ('stepped_traditional_smear', 'camera_shutter_vector', 'background_only_haze', 'none').\n"
            "- 'shutter_angle_degrees': float (range 45.0 to 360.0. Higher means longer blur).\n"
            "- 'blur_samples': integer (For anime 'stepped' feel, keep low: 4 to 8. For smooth, use 16).\n"
            "- 'velocity_vector_multiplier': float (range 0.1 to 4.5).\n"
            "- 'smear_duplication_steps': integer (range 0 to 5).\n"
            "Format strictly as JSON with key 'motion_blur_profiles'."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": json.dumps(velocities)}], "response_format": {"type": "json_object"}}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=50) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    final_output = {"motion_blur_profiles": json.loads(cleaned).get("motion_blur_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Failed: {str(e)}", "WARNING")

        if not final_output:
            self.log_message("Resolving procedural velocity blur fallback.", "INFO")
            final_output = self._execute_procedural_fallback(velocities)
            
        self._save_to_workspace(final_output)
        self._bake_motion_blur_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, velocities):
        profiles = []
        for v in velocities:
            ts = float(v.get("timestamp_sec", 0.0))
            style_hint = str(v.get("speed_style", "")).lower()
            velocity = float(v.get("implied_velocity", 10.0))

            if velocity > 35.0:
                profiles.append({"timestamp_sec": ts, "blur_render_type": "stepped_traditional_smear", "shutter_angle_degrees": 270.0, "blur_samples": 6, "velocity_vector_multiplier": 3.5, "smear_duplication_steps": 3})
            elif "zoom" in style_hint:
                profiles.append({"timestamp_sec": ts, "blur_render_type": "background_only_haze", "shutter_angle_degrees": 180.0, "blur_samples": 12, "velocity_vector_multiplier": 1.8, "smear_duplication_steps": 0})
            elif velocity > 5.0:
                profiles.append({"timestamp_sec": ts, "blur_render_type": "camera_shutter_vector", "shutter_angle_degrees": 90.0, "blur_samples": 16, "velocity_vector_multiplier": 1.0, "smear_duplication_steps": 0})
            else:
                profiles.append({"timestamp_sec": ts, "blur_render_type": "none", "shutter_angle_degrees": 0.0, "blur_samples": 0, "velocity_vector_multiplier": 0.0, "smear_duplication_steps": 0})
        return {"motion_blur_profiles": profiles}

    def _bake_motion_blur_in_blender(self, blur_data):
        """God Level Feature: Animates EEVEE/Cycles native motion blur for anime smear effects"""
        self.log_message("Connecting to Engine Core: Baking Keyframed Motion Blur...", "INFO")
        
        script_content = f"""
import bpy

profiles = {json.dumps(blur_data.get('motion_blur_profiles', []))}
fps = bpy.context.scene.render.fps

# Enable Motion Blur in Render Engine
bpy.context.scene.eevee.use_motion_blur = True
eevee = bpy.context.scene.eevee

# Set Base State (No Blur/Normal Blur) at frame 1
eevee.motion_blur_shutter = 0.5  # Standard 180-degree equivalent
eevee.motion_blur_steps = 8
eevee.keyframe_insert(data_path="motion_blur_shutter", frame=1)
eevee.keyframe_insert(data_path="motion_blur_steps", frame=1)

for p in profiles:
    if p['blur_render_type'] == 'none':
        continue
        
    impact_frame = int(p['timestamp_sec'] * fps)
    
    # 3 frames before movement: keep it sharp/normal
    eevee.motion_blur_shutter = 0.5
    eevee.motion_blur_steps = 8
    eevee.keyframe_insert(data_path="motion_blur_shutter", frame=max(1, impact_frame - 3))
    eevee.keyframe_insert(data_path="motion_blur_steps", frame=max(1, impact_frame - 3))
    
    # At impact/movement frame: Spike the blur for that anime smear
    # Convert degrees (e.g. 270) to fraction of a frame (270/360 = 0.75)
    shutter_fraction = min(p['shutter_angle_degrees'] / 360.0, 1.0) 
    
    eevee.motion_blur_shutter = shutter_fraction * p['velocity_vector_multiplier']
    eevee.motion_blur_steps = p['blur_samples'] # Low samples = anime choppiness
    
    eevee.keyframe_insert(data_path="motion_blur_shutter", frame=impact_frame)
    eevee.keyframe_insert(data_path="motion_blur_steps", frame=impact_frame)
    
    # Reset to normal 10 frames after action
    eevee.motion_blur_shutter = 0.5
    eevee.motion_blur_steps = 8
    eevee.keyframe_insert(data_path="motion_blur_shutter", frame=impact_frame + 10)
    eevee.keyframe_insert(data_path="motion_blur_steps", frame=impact_frame + 10)

bpy.ops.wm.save_mainfile()
"""
        script_path = os.path.join(self.workspace_dir, "temp_motion_blur.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Injecting Dynamic Motion Smears into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Anime style motion blur keyframed successfully.", "INFO")

if __name__ == "__main__":
    applier = AiMotionBlurVelocityVectorApplier()
    applier.design_stylized_motion_blur()
    print("--- OMNIMATRIX MOTION BLUR DEPT: AGENT 40 COMPLETE ---")
