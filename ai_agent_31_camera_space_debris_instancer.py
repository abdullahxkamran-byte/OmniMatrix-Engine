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

class OmniMatrixDebrisInstancer:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 31: OmniMatrix Camera Space Debris Instancer"
        
        # Directories
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.env_dir, "31_camera_debris_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_context(self, scene_name):
        """Loads visual style and destruction data from Agent 30"""
        context = {
            "visual_style": "omni_neutral",
            "has_destruction": False,
            "impact_frame": 0,
            "fracture_center_xyz": [0.0, 0.0, 0.0]
        }
        
        # Load Style
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "omni_neutral")
            except:
                pass

        # Load Destruction Data (Agent 30)
        dest_file = os.path.join(self.env_dir, "30_destruction_blueprint.json")
        if os.path.exists(dest_file):
            try:
                with open(dest_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        scene_data = data[scene_name]
                        context["has_destruction"] = scene_data.get("shatter_chunk_count", 0) > 0
                        context["impact_frame"] = scene_data.get("impact_frame", 0)
                        context["fracture_center_xyz"] = scene_data.get("fracture_center_xyz", [0.0, 0.0, 0.0])
            except Exception as e:
                self.log_message(f"Destruction data read error: {e}", "WARNING")
                
        return context

    def _query_debris_brain(self, scene_name, context):
        if not context["has_destruction"]:
            return self._fallback_debris(False)

        if not self.gemini_api_key:
            return self._fallback_debris(True, context)

        ai_prompt = (
            f"You are the VFX Debris TD for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Impact Frame: {context['impact_frame']}\n\n"
            "Design camera-facing particle debris based on the style.\n"
            "- 'anime': Large chunks, zero gravity (straight line to camera), high speed.\n"
            "- 'realistic': Fine dust, normal gravity (arc trajectory), medium speed.\n"
            "- LIMIT particle count to 150 max to save RAM.\n"
            "Return ONLY raw JSON:\n"
            "{\n"
            "  \"impact_frame\": " + str(context['impact_frame']) + ",\n"
            "  \"epicenter_xyz\": " + str(context['fracture_center_xyz']) + ",\n"
            "  \"debris_type\": \"heavy_chunks\",\n"
            "  \"particle_count\": 100,\n"
            "  \"velocity_towards_camera\": 25.0,\n"
            "  \"gravity_influence\": 0.0,\n"
            "  \"rationale\": \"Anime style needs chunks shooting straight at the lens without falling.\"\n"
            "}"
        )

        try:
            payload = {"contents": [{"parts": [{"text": ai_prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                output = json.loads(res_text)
                
                # HARD SAFEGUARD FOR COLAB RAM
                if output.get("particle_count", 0) > 150:
                    output["particle_count"] = 150
                return output
                
        except Exception as e:
            self.log_message(f"AI Debris Director failed: {str(e)}. Using fallback.", "WARNING")
            return self._fallback_debris(True, context)

    def _fallback_debris(self, has_impact, context=None):
        if not has_impact:
            return {
                "impact_frame": 0, "particle_count": 0, "debris_type": "none",
                "velocity_towards_camera": 0.0, "gravity_influence": 1.0, "rationale": "No impact."
            }
        return {
            "impact_frame": context.get("impact_frame", 24), "particle_count": 80, 
            "epicenter_xyz": context.get("fracture_center_xyz", [0,0,0]), "debris_type": "coarse_dust",
            "velocity_towards_camera": 15.0, "gravity_influence": 0.5, "rationale": "Fallback standard debris."
        }

    def _generate_blender_script(self, blend_file_path, debris_data):
        """Python script to generate camera-facing particle systems in Headless Blender."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy
import mathutils

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    count = {debris_data.get('particle_count', 0)}
    frame = {debris_data.get('impact_frame', 0)}
    vel = {debris_data.get('velocity_towards_camera', 0.0)}
    grav = {debris_data.get('gravity_influence', 1.0)}
    epicenter = {debris_data.get('epicenter_xyz', [0.0, 0.0, 0.0])}

    if count > 0:
        cam = bpy.context.scene.camera
        if cam:
            # 1. Create Emitter at Impact Location
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=epicenter)
            emitter = bpy.context.active_object
            emitter.name = "Omni_Debris_Emitter"
            emitter.hide_render = True # Hide emitter, only show particles
            
            # 2. Add Particle System
            bpy.ops.object.particle_system_add()
            ps = emitter.particle_systems[0]
            pset = ps.settings
            
            pset.count = count
            pset.frame_start = frame
            pset.frame_end = frame + 2 # Burst emission
            pset.lifetime = 100
            
            # 3. Calculate Vector to Camera
            cam_loc = cam.location
            emit_loc = mathutils.Vector(epicenter)
            direction = (cam_loc - emit_loc).normalized()
            
            # 4. Apply Velocity and Physics
            pset.physics_type = 'NEWTON'
            pset.normal_factor = 0.0 # Don't shoot along normals
            
            # We use an empty force field to pull particles towards camera, 
            # or simply set the emitter's velocity towards the camera.
            # Easiest way in Blender script is to rotate the emitter to face the camera 
            # and use Object Z-Velocity.
            
            rot_quat = direction.to_track_quat('Z', 'Y')
            emitter.rotation_euler = rot_quat.to_euler()
            pset.object_factor = vel # Shoot along object Z axis
            pset.factor_random = vel * 0.3 # Add chaos
            
            # 5. OmniMatrix Gravity Influence (Anime = 0, Realistic = 1)
            pset.effector_weights.gravity = grav

        bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
        print("SUCCESS: OmniMatrix Camera Debris initialized.")
    else:
        print("INFO: No debris needed for this scene.")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_debris_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_camera_debris(self):
        self.log_message("Initializing OmniMatrix Camera Debris Instancer...", "INFO")
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_context(scene_name)
                
                if context["has_destruction"]:
                    self.log_message(f"--- Processing Debris for: {scene_name} ---", "INFO")
                    debris_data = self._query_debris_brain(scene_name, context)
                    
                    self.log_message(f"AI Decision: {debris_data['rationale']} | Type: {debris_data['debris_type']} | Count: {debris_data['particle_count']}", "INFO")
                    
                    script_path = self._generate_blender_script(blend_file_path, debris_data)
                    
                    command = [self.blender_path, "-b", "-P", script_path]
                    try:
                        result = subprocess.run(command, capture_output=True, text=True)
                        if result.returncode == 0:
                            self.log_message(f"Camera Debris applied to {filename}", "INFO")
                            master_blueprint[scene_name] = debris_data
                        else:
                            self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                    except Exception as e:
                        self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                        
                    if os.path.exists(script_path):
                        os.remove(script_path)
                else:
                    self.log_message(f"Scene '{scene_name}' has no destruction. Skipping Debris.", "INFO")
                    master_blueprint[scene_name] = self._fallback_debris(False)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 31 Pipeline Complete. Debris is flying towards the lens!", "INFO")

if __name__ == "__main__":
    instancer = OmniMatrixDebrisInstancer()
    instancer.process_camera_debris()
