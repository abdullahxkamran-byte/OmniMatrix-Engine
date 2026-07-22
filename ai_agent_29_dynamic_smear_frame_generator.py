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

class OmniMatrixMotionDynamicsDirector:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 29: aaa_motion_smear_director"
        
        # Directories
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.workspace_dir, "29_motion_dynamics_blueprint.json")
        self.blender_path = blender_path
        
        # GEMINI API INTEGRATION
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.workspace_dir, self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_context(self, scene_name):
        """Load visual style and high-speed motion data."""
        context = {
            "visual_style": "omni_neutral",
            "action_description": "Standard movement",
            "fast_motion_frame": 24
        }
        
        # Load Style Context
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "omni_neutral")
                    context["action_description"] = data.get("action_description", "Standard movement")
            except Exception as e:
                self.log_message(f"Style context parse error: {str(e)}", "WARNING")

        # Load Animation Keys (to find fast movement frames from Agent 26)
        anim_file = os.path.join(self.workspace_dir, "26_animation_blueprint.json")
        if os.path.exists(anim_file):
            try:
                with open(anim_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        context["fast_motion_frame"] = data[scene_name].get("target_frame", 24)
            except Exception as e:
                self.log_message(f"Animation data read error: {str(e)}", "WARNING")

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

    def _query_motion_brain(self, scene_name, context):
        """Ask Gemini to decide between Realistic Motion Blur or Anime Smear Frames."""
        self.log_message(f"Calculating Motion & Smear Vectors for '{scene_name}'...", "INFO")
        
        if not self.gemini_api_key:
            self.log_message("No Gemini API Key found. Using fallback motion blur.", "WARNING")
            return self._fallback_motion(context["fast_motion_frame"])

        ai_prompt = (
            f"You are the Motion Dynamics Technical Director for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Action: {context['action_description']}\n\n"
            "Decide how to render high-speed motion based on the visual style.\n"
            "- Realistic/Cinematic: Use 'realistic_blur', high shutter speed, NO mesh stretching.\n"
            "- Anime/Cartoon: Use 'stylized_smear', high stretch factor, ghost trails.\n"
            "Return EXACTLY 1 raw JSON object containing:\n"
            "{\n"
            "  \"motion_handling_mode\": \"stylized_smear\",\n"
            f"  \"target_frame\": {context['fast_motion_frame']},\n"
            "  \"camera_shutter_speed\": 0.5,\n"
            "  \"motion_blur_steps\": 8,\n"
            "  \"mesh_stretch_factor\": 2.5,\n"
            "  \"ghost_trail_count\": 3,\n"
            "  \"rationale\": \"Anime style requires exaggerated mesh stretching for fast sword slashes.\"\n"
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
            self.log_message(f"AI Motion Director failed: {str(e)}. Using fallback.", "WARNING")
            return self._fallback_motion(context["fast_motion_frame"])

    def _fallback_motion(self, frame=24):
        return {
            "motion_handling_mode": "realistic_blur", "target_frame": frame,
            "camera_shutter_speed": 0.5, "motion_blur_steps": 4,
            "mesh_stretch_factor": 0.0, "ghost_trail_count": 0,
            "rationale": "Universal default motion blur applied."
        }

    def _generate_blender_script(self, blend_file_path, motion_data):
        """Python script to inject Motion Blur and Smear Deformations into Blender."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    mode = "{motion_data.get('motion_handling_mode', 'realistic_blur')}"
    target_frame = {motion_data.get('target_frame', 24)}
    shutter = {motion_data.get('camera_shutter_speed', 0.5)}
    steps = {motion_data.get('motion_blur_steps', 4)}
    stretch_factor = {motion_data.get('mesh_stretch_factor', 0.0)}

    # 1. Universal Camera Motion Blur Setup
    bpy.context.scene.render.use_motion_blur = True
    bpy.context.scene.render.motion_blur_shutter = shutter
    
    # Eevee specific blur settings (Legacy Eevee check for backward compatibility)
    if hasattr(bpy.context.scene, "eevee") and hasattr(bpy.context.scene.eevee, "use_motion_blur"):
        bpy.context.scene.eevee.use_motion_blur = True
        bpy.context.scene.eevee.motion_blur_steps = steps

    # 2. Anime-Style Smear Deformation
    if mode == "stylized_smear" and stretch_factor > 0:
        # Secure Identification: MESH that is parented to an ARMATURE, or uses universal prefix
        char_meshes = [
            obj for obj in bpy.context.scene.objects 
            if obj.type == 'MESH' and ((obj.parent and obj.parent.type == 'ARMATURE') or obj.name.startswith("OMNI_CHAR"))
        ]
        
        for mesh in char_meshes:
            # Cleanup existing modifiers to prevent stacking on re-runs
            for mod in mesh.modifiers:
                if mod.name == "Omni_Smear_Stretch":
                    mesh.modifiers.remove(mod)

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
    print(f"ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_motion_script.py")
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
                
                self.log_message(f"AI Decision: {motion_data.get('rationale', 'Default')} | Mode: {motion_data.get('motion_handling_mode', 'realistic_blur')}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, motion_data)
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        self.log_message(f"Motion Dynamics applied to {filename}", "SUCCESS")
                        master_blueprint[scene_name] = motion_data
                    else:
                        self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 29 Pipeline Complete. Speed and Motion are now Omni-Optimized.", "INFO")

if __name__ == "__main__":
    director = OmniMatrixMotionDynamicsDirector()
    director.process_motion_dynamics()
