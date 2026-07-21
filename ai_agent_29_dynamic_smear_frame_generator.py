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

class OmniMatrixMotionDynamicsDirector:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 29: OmniMatrix Motion & Smear Director"
        
        # Directories
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.env_dir, "29_motion_dynamics_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_context(self, scene_name):
        """Load visual style and high-speed motion data."""
        context = {
            "visual_style": "omni_neutral",
            "action_description": "Standard movement",
            "fast_motion_frame": 0
        }
        
        # Load Style Context
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "omni_neutral")
                    context["action_description"] = data.get("action_description", "")
            except:
                pass

        # Load Animation Keys (to find fast movement frames)
        anim_file = os.path.join(self.env_dir, "26_animation_blueprint.json")
        if os.path.exists(anim_file):
            try:
                with open(anim_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        # Guessing the target frame based on puppet action
                        context["fast_motion_frame"] = data[scene_name].get("target_frame", 24)
            except:
                pass

        return context

    def _query_motion_brain(self, scene_name, context):
        """Ask Gemini to decide between Realistic Motion Blur or Anime Smear Frames."""
        if not self.gemini_api_key:
            return self._fallback_motion()

        ai_prompt = (
            f"You are the Motion Dynamics Technical Director for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Action: {context['action_description']}\n\n"
            "Decide how to render high-speed motion based on the visual style.\n"
            "- Realistic/Cinematic: Use 'realistic_blur', high shutter speed, NO mesh stretching.\n"
            "- Anime/Cartoon: Use 'stylized_smear', high stretch factor, ghost trails.\n"
            "Return ONLY raw JSON:\n"
            "{\n"
            "  \"motion_handling_mode\": \"stylized_smear\",\n"
            "  \"target_frame\": " + str(context['fast_motion_frame']) + ",\n"
            "  \"camera_shutter_speed\": 0.5,\n"
            "  \"motion_blur_steps\": 8,\n"
            "  \"mesh_stretch_factor\": 2.5,\n"
            "  \"ghost_trail_count\": 3,\n"
            "  \"rationale\": \"Anime style requires exaggerated mesh stretching for fast sword slashes.\"\n"
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
            self.log_message(f"AI Motion Director failed: {str(e)}. Using fallback.", "WARNING")
            return self._fallback_motion(context["fast_motion_frame"])

    def _fallback_motion(self, frame=24):
        return {
            "motion_handling_mode": "realistic_blur", "target_frame": frame,
            "camera_shutter_speed": 0.5, "motion_blur_steps": 4,
            "mesh_stretch_factor": 0.0, "ghost_trail_count": 0,
            "rationale": "Universal default motion blur."
        }

    def _generate_blender_script(self, blend_file_path, motion_data):
        """Python script to inject Motion Blur and Smear Deformations into Blender."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    mode = "{motion_data.get('motion_handling_mode', 'realistic_blur')}"
    target_frame = {motion_data.get('target_frame', 24)}
    shutter = {motion_data.get('camera_shutter_speed', 0.5)}
    steps = {motion_data.get('motion_blur_steps', 4)}
    stretch_factor = {motion_data.get('mesh_stretch_factor', 0.0)}

    # 1. Universal Camera Motion Blur Setup
    bpy.context.scene.render.use_motion_blur = True
    bpy.context.scene.render.motion_blur_shutter = shutter
    
    # Eevee specific blur settings
    if hasattr(bpy.context.scene.eevee, "use_motion_blur"):
        bpy.context.scene.eevee.use_motion_blur = True
        bpy.context.scene.eevee.motion_blur_steps = steps

    # 2. Anime-Style Smear Deformation (If Stylized)
    if mode == "stylized_smear" and stretch_factor > 0:
        # Find character meshes (Assumed to be children of Armature)
        char_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.parent and obj.parent.type == 'ARMATURE']
        
        for mesh in char_meshes:
            # Add Simple Deform (Stretch) Modifier
            mod = mesh.modifiers.new(name="Omni_Smear_Stretch", type='SIMPLE_DEFORM')
            mod.deform_method = 'STRETCH'
            
            # Keyframe the stretch so it only happens at the exact frame of movement
            mod.factor = 0.0
            mod.keyframe_insert(data_path="factor", frame=target_frame - 1)
            
            mod.factor = stretch_factor
            mod.keyframe_insert(data_path="factor", frame=target_frame)
            
            mod.factor = 0.0
            mod.keyframe_insert(data_path="factor", frame=target_frame + 2)

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS: OmniMatrix Motion Dynamics (Blur/Smear) injected successfully.")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_motion_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_motion_dynamics(self):
        self.log_message("Initializing OmniMatrix Motion Dynamics Director...", "INFO")
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_context(scene_name)
                
                self.log_message(f"--- Processing Motion for: {scene_name} ---", "INFO")
                motion_data = self._query_motion_brain(scene_name, context)
                
                self.log_message(f"AI Decision: {motion_data['rationale']} | Mode: {motion_data['motion_handling_mode']}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, motion_data)
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_message(f"Motion Dynamics applied to {filename}", "INFO")
                        master_blueprint[scene_name] = motion_data
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 29 Pipeline Complete. Speed and Motion are now Omni-Optimized.", "INFO")

if __name__ == "__main__":
    director = OmniMatrixMotionDynamicsDirector()
    director.process_motion_dynamics()
