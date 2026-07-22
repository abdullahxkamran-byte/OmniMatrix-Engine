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

class OmniMatrixPhysicsBaker:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 33: aaa_physics_cloth_hair_baker"
        
        # Directories
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.workspace_dir, "33_omni_physics_blueprint.json")
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
        """Loads visual style and kinetic movement data"""
        context = {
            "visual_style": "anime",
            "action_intensity": "high", 
            "start_frame": 1,
            "end_frame": 72
        }
        
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "anime").lower()
                    context["action_intensity"] = data.get("action_intensity", "high")
            except Exception as e:
                self.log_message(f"Style context parse error: {str(e)}", "WARNING")
                
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

    def _query_physics_brain(self, scene_name, context):
        self.log_message(f"Calculating Physics Damping & Wind Vectors for '{scene_name}'...", "INFO")

        if not self.gemini_api_key:
            self.log_message("No Gemini API Key found. Using fallback physics setup.", "WARNING")
            return self._fallback_physics(context)

        ai_prompt = (
            f"You are the Lead 3D Physics Technical Director for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Action Intensity: {context['action_intensity']}\n\n"
            "Calculate the cloth, hair, and wind physics parameters for Blender based on the visual style.\n"
            "- If style is 'anime', cloth should be stiff (high bending), hair spring tension high, and wind highly directional/dramatic.\n"
            "- If style is 'realistic', cloth should be soft (low bending, high damping), wind natural with noise.\n"
            "Output EXACTLY 1 raw JSON object containing:\n"
            "{\n"
            "  \"wind_strength\": 1500.0,\n"
            "  \"wind_noise\": 2.5,\n"
            "  \"wind_direction\": [1.0, -1.0, 0.2],\n"
            "  \"cloth_bending_stiffness\": 1.5,\n"
            "  \"cloth_damping\": 5.0,\n"
            "  \"hair_stiffness\": 0.8,\n"
            "  \"gravity_scale\": 0.8\n"
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
            self.log_message(f"AI Physics Brain failed: {str(e)}. Triggering fallback.", "WARNING")
            return self._fallback_physics(context)

    def _fallback_physics(self, context):
        is_anime = "anime" in context["visual_style"]
        return {
            "wind_strength": 2000.0 if is_anime else 500.0,
            "wind_noise": 5.0 if is_anime else 1.2,
            "wind_direction": [1.0, 0.0, 0.5],
            "cloth_bending_stiffness": 5.0 if is_anime else 0.5,
            "cloth_damping": 2.0 if is_anime else 8.0,
            "hair_stiffness": 1.5 if is_anime else 0.4,
            "gravity_scale": 0.5 if is_anime else 1.0 # Anime has floaty gravity
        }

    def _generate_blender_script(self, blend_file_path, phys_data, context):
        """Generates Blender script to apply physics limits, wind, and BAKE caches safely."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        # Safegaurd: Absolute limit on baking frames to prevent VRAM explosion
        start_frame = int(context.get("start_frame", 1))
        end_frame = min(int(context.get("end_frame", 72)), start_frame + 72)
        
        script_content = f"""
import bpy
import json
import mathutils

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    phys_data = json.loads('''{json.dumps(phys_data)}''')
    
    start_f = {start_frame}
    end_f = {end_frame}
    
    bpy.context.scene.frame_start = start_f
    bpy.context.scene.frame_end = end_f
    
    # Set gravity multiplier safely
    bpy.context.scene.use_gravity = True
    bpy.context.scene.gravity[2] = -9.81 * phys_data.get("gravity_scale", 1.0)
    
    # 1. Create/Update Wind Force Field (Idempotent cleanup)
    wind_obj = bpy.data.objects.get("OMNI_Wind")
    if wind_obj:
        bpy.data.objects.remove(wind_obj, do_unlink=True)
        
    bpy.ops.object.effector_add(type='WIND', enter_editmode=False, align='WORLD', location=(0, -5, 2))
    wind_obj = bpy.context.active_object
    wind_obj.name = "OMNI_Wind"
    
    wind_obj.field.strength = phys_data.get("wind_strength", 1000.0)
    wind_obj.field.noise = phys_data.get("wind_noise", 1.0)
    
    dir_vec = phys_data.get("wind_direction", [0,1,0])
    # Convert direction vector to euler rotation
    vec = mathutils.Vector((dir_vec[0], dir_vec[1], dir_vec[2]))
    wind_obj.rotation_euler = vec.to_track_quat('Z', 'Y').to_euler()

    # 2. Iterate through objects to find Cloth & Particle Systems
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    for obj in meshes:
        # Check Cloth Modifiers
        for mod in obj.modifiers:
            if mod.type == 'CLOTH':
                mod.settings.bending_stiffness = phys_data.get("cloth_bending_stiffness", 1.0)
                mod.settings.damping = phys_data.get("cloth_damping", 5.0)
                
                # Apply Frame Limits to Point Cache
                mod.point_cache.frame_start = start_f
                mod.point_cache.frame_end = end_f
                
                # STRICT CACHE CLEANUP BEFORE BAKE
                bpy.context.view_layer.objects.active = obj
                bpy.ops.ptcache.free_bake({"point_cache": mod.point_cache})
                
        # Check Hair/Particle Systems
        for ps in obj.particle_systems:
            if ps.settings.type == 'HAIR' and ps.settings.use_hair_dynamics:
                ps.settings.hair_dynamics.pin_stiffness = phys_data.get("hair_stiffness", 1.0)
                
                # Apply Frame Limits to Point Cache
                ps.point_cache.frame_start = start_f
                ps.point_cache.frame_end = end_f
                
                # STRICT CACHE CLEANUP BEFORE BAKE
                bpy.context.view_layer.objects.active = obj
                bpy.ops.ptcache.free_bake({"point_cache": ps.point_cache})

    # 3. VRAM SAFEGUARD BAKE COMMAND
    print("Starting Global Physics Bake (Max 72 Frames)...")
    bpy.ops.ptcache.bake_all(bake=True)
    print("Physics Baking Completed Successfully.")
                                
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")

except Exception as e:
    print(f"ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_physics_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_baking_pipeline(self):
        self.log_message("Initializing OmniMatrix Physics Baker...", "INFO")
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_context(scene_name)
                
                self.log_message(f"--- Simulating Physics for: {scene_name} | Style: {context['visual_style'].upper()} ---", "INFO")
                
                phys_data = self._query_physics_brain(scene_name, context)
                script_path = self._generate_blender_script(blend_file_path, phys_data, context)
                
                # Run Headless Blender
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "Completed Successfully" in result.stdout:
                        self.log_message(f"Physics baked and saved safely for {filename} (Max 72 Frames).", "SUCCESS")
                        master_blueprint[scene_name] = phys_data
                    else:
                        self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 33 Pipeline Complete. Cloth and Hair are now dynamically baked!", "INFO")

if __name__ == "__main__":
    baker = OmniMatrixPhysicsBaker()
    baker.execute_baking_pipeline()
