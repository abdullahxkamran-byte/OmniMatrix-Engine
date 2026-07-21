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

class OmniMatrixPhysicsBaker:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 33: OmniMatrix Physics Cloth & Hair Baker"
        
        # Directories
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.env_dir, "33_omni_physics_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_context(self, scene_name):
        """Loads visual style and kinetic movement data"""
        context = {
            "visual_style": "anime",
            "action_intensity": "high", # e.g., combat, idle, running
            "start_frame": 1,
            "end_frame": 72
        }
        
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "anime")
                    context["action_intensity"] = data.get("action_intensity", "high")
            except:
                pass
                
        return context

    def _query_physics_brain(self, scene_name, context):
        if not self.gemini_api_key:
            return self._fallback_physics(context)

        ai_prompt = (
            f"You are the Lead 3D Physics Technical Director for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Action Intensity: {context['action_intensity']}\n\n"
            "Calculate the cloth, hair, and wind physics parameters for Blender based on the visual style.\n"
            "- If style is 'anime', cloth should be stiff (high bending), hair spring tension high, and wind highly directional/dramatic.\n"
            "- If style is 'realistic', cloth should be soft (low bending, high damping), wind natural with noise.\n"
            "Output MUST be raw JSON exactly like this:\n"
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
            payload = {"contents": [{"parts": [{"text": ai_prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                return json.loads(res_text)
        except Exception as e:
            self.log_message(f"AI Physics Brain failed: {str(e)}. Triggering fallback.", "WARNING")
            return self._fallback_physics(context)

    def _fallback_physics(self, context):
        is_anime = "anime" in context["visual_style"].lower()
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

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    phys_data = json.loads('''{json.dumps(phys_data)}''')
    
    start_f = {start_frame}
    end_f = {end_frame}
    
    bpy.context.scene.frame_start = start_f
    bpy.context.scene.frame_end = end_f
    bpy.context.scene.gravity[2] = -9.81 * phys_data.get("gravity_scale", 1.0)
    
    # 1. Create/Update Wind Force Field
    wind_obj = bpy.data.objects.get("Omni_Wind")
    if not wind_obj:
        bpy.ops.object.effector_add(type='WIND', enter_editmode=False, align='WORLD', location=(0, -5, 2))
        wind_obj = bpy.context.active_object
        wind_obj.name = "Omni_Wind"
    
    wind_obj.field.strength = phys_data.get("wind_strength", 1000.0)
    wind_obj.field.noise = phys_data.get("wind_noise", 1.0)
    
    dir_vec = phys_data.get("wind_direction", [0,1,0])
    # Basic rotation based on vector (simplified)
    wind_obj.rotation_euler = (dir_vec[0], dir_vec[1], dir_vec[2])

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
                
        # Check Hair/Particle Systems
        for ps in obj.particle_systems:
            if ps.settings.type == 'HAIR' and ps.settings.use_hair_dynamics:
                ps.settings.hair_dynamics.pin_stiffness = phys_data.get("hair_stiffness", 1.0)
                
                # Apply Frame Limits to Point Cache
                ps.point_cache.frame_start = start_f
                ps.point_cache.frame_end = end_f

    # 3. VRAM SAFEGUARD BAKE COMMAND
    print("Starting Global Physics Bake (Max 72 Frames)...")
    bpy.ops.ptcache.free_bake_all()
    bpy.ops.ptcache.bake_all(bake=True)
    print("Physics Baking Completed Successfully.")
                                
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_physics_script.py")
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
                
                self.log_message(f"--- Simulating Physics for: {scene_name} | Style: {context['visual_style']} ---", "INFO")
                
                phys_data = self._query_physics_brain(scene_name, context)
                script_path = self._generate_blender_script(blend_file_path, phys_data, context)
                
                # Run Headless Blender
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_message(f"Physics baked and saved safely for {filename} (Max 72 Frames).", "INFO")
                        master_blueprint[scene_name] = phys_data
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 33 Pipeline Complete. Cloth and Hair are now dynamically baked!", "INFO")

if __name__ == "__main__":
    baker = OmniMatrixPhysicsBaker()
    baker.execute_baking_pipeline()
