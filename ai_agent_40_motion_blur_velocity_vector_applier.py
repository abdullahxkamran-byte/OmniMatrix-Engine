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

    def _load_master_config(self):
        # Reads the master project style (Universal Routing)
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    return json.load(f).get("global_style", "anime")
            except:
                pass
        return "realistic" # Defaulting to realistic as a safe universal baseline

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

        if not velocity_contexts:
            self.log_message("No motion data. Injecting standard action sequence vectors.", "INFO")
            velocity_contexts = [{"timestamp_sec": 1.2, "speed_style": "radial_zoom_in", "implied_velocity": 45.5}]

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
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return file_path

    def design_stylized_motion_blur(self):
        velocities = self._load_upstream_kinetics()
        global_style = self._load_master_config()
        self.log_message(f"Solving vector passes for '{global_style}' routing...", "INFO")

        system_prompt = (
            f"You are a Senior Technical Director. The project global style is '{global_style.upper()}'.\n"
            "Translate 3D physical speed into motion blur commands. If style is REALISTIC, output high samples and smooth shutter values. If ANIME, output low samples and stepped smear values.\n"
            "Generate 1 configuration inside a list named 'motion_blur_profiles':\n"
            "- 'timestamp_sec': float.\n"
            "- 'render_style_enforced': string ('realistic' or 'anime').\n"
            "- 'shutter_angle_degrees': float (Realistic usually 180.0. Anime can spike to 270.0+).\n"
            "- 'blur_samples': integer (Realistic: 16 to 32. Anime: 4 to 8).\n"
            "- 'velocity_vector_multiplier': float.\n"
            "Format strictly as JSON with key 'motion_blur_profiles'."
        )

        final_output = None
        if self.openai_api_key:
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": json.dumps(velocities)}], "response_format": {"type": "json_object"}}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=50) as response:
                    cleaned = self._clean_json_response(json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"])
                    final_output = {"motion_blur_profiles": json.loads(cleaned).get("motion_blur_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Failed: {str(e)}", "WARNING")

        if not final_output:
            final_output = self._execute_procedural_fallback(velocities, global_style)
            
        self._save_to_workspace(final_output)
        self._bake_motion_blur_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, velocities, style):
        profiles = []
        for v in velocities:
            ts = float(v.get("timestamp_sec", 0.0))
            vel = float(v.get("implied_velocity", 10.0))

            if style.lower() == "realistic":
                # Smooth, cinematic physical camera blur
                profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "shutter_angle_degrees": 180.0, "blur_samples": 32, "velocity_vector_multiplier": 1.0})
            else:
                # Stepped, choppy anime smear
                if vel > 20.0:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "shutter_angle_degrees": 270.0, "blur_samples": 6, "velocity_vector_multiplier": 2.5})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "shutter_angle_degrees": 90.0, "blur_samples": 4, "velocity_vector_multiplier": 1.0})
        return {"motion_blur_profiles": profiles}

    def _bake_motion_blur_in_blender(self, blur_data):
        self.log_message("Connecting to Engine Core: Baking Keyframed Motion Blur...", "INFO")
        
        script_content = f"""
import bpy

profiles = {json.dumps(blur_data.get('motion_blur_profiles', []))}
fps = bpy.context.scene.render.fps

bpy.context.scene.eevee.use_motion_blur = True
eevee = bpy.context.scene.eevee

for p in profiles:
    impact_frame = int(p['timestamp_sec'] * fps)
    
    shutter_fraction = min(p['shutter_angle_degrees'] / 360.0, 1.0) 
    
    # Universal Application:
    eevee.motion_blur_shutter = shutter_fraction * p['velocity_vector_multiplier']
    
    if p.get('render_style_enforced', 'anime').lower() == 'realistic':
        # HIGH SAMPLES for smooth CGI/Live-Action motion
        eevee.motion_blur_steps = 32
    else:
        # LOW SAMPLES for Stepped Anime Smear
        eevee.motion_blur_steps = p.get('blur_samples', 6)
    
    eevee.keyframe_insert(data_path="motion_blur_shutter", frame=impact_frame)
    eevee.keyframe_insert(data_path="motion_blur_steps", frame=impact_frame)

bpy.ops.wm.save_mainfile()
"""
        script_path = os.path.join(self.workspace_dir, "temp_motion_blur.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Universal motion blur applied successfully.", "INFO")

if __name__ == "__main__":
    applier = AiMotionBlurVelocityVectorApplier()
    applier.design_stylized_motion_blur()
