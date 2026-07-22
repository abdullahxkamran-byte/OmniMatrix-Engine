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

class DynamicMeshCollisionSentinel:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 27: aaa_dynamic_collision_sentinel"
        
        # Upstream Inputs
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments") # Modifies existing _stage.blend files
        
        # Outputs
        self.output_blueprint = os.path.join(self.workspace_dir, "27_collision_blueprint.json")
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
        """Loads scene context to understand the intensity of collisions."""
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        context = {
            "visual_style": "omni_neutral",
            "action_description": "Characters interacting"
        }
        
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["visual_style"] = data.get("visual_style", "omni_neutral")
                    context["action_description"] = data.get("action_description", "Characters interacting")
            except Exception as e:
                self.log_message(f"Script parse warning: {str(e)}", "WARNING")
                
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
        """Asks Gemini to estimate impact severity and particle styles."""
        self.log_message(f"Calculating Physics & Collision vectors for '{scene_name}'...", "INFO")
        
        if not self.gemini_api_key:
            self.log_message("No Gemini API Key found. Using fallback physics.", "WARNING")
            return self._fallback_physics()

        ai_prompt = (
            f"You are the Physics & FX Supervisor for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Action Required: {context['action_description']}\n\n"
            "Analyze the action. Does it involve high impact (sword clash, punch) or just normal movement?\n"
            "Return EXACTLY 1 raw JSON object containing:\n"
            "{\n"
            "  \"has_major_impact\": true,\n"
            "  \"impact_frame\": 24,\n"
            "  \"sparks_particle_count\": 150,\n"
            "  \"particle_style\": \"realistic_sparks\",\n"
            "  \"anti_clipping_pushback\": [0.0, -0.2, 0.0],\n"
            "  \"rationale\": \"Sword clash requires sparks and a slight pushback to prevent mesh intersection.\"\n"
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
            self.log_message(f"AI Physics Prediction failed: {str(e)}. Using fallback.", "WARNING")
            return self._fallback_physics()

    def _fallback_physics(self):
        return {
            "has_major_impact": False, "impact_frame": 0, "sparks_particle_count": 0,
            "particle_style": "none", "anti_clipping_pushback": [0.0, 0.0, 0.0],
            "rationale": "No impact detected. Routine environment setup."
        }

    def _generate_blender_script(self, blend_file_path, physics_data):
        """Python script to enable mesh collisions and particle systems in Blender."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        # Ensure boolean is properly injected into Python script
        has_impact_val = "True" if physics_data.get('has_major_impact', False) else "False"
        
        script_content = f"""
import bpy

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    has_impact = {has_impact_val}
    pushback = {physics_data.get('anti_clipping_pushback', [0,0,0])}
    impact_frame = {physics_data.get('impact_frame', 24)}
    particles = {physics_data.get('sparks_particle_count', 0)}
    
    # 1. Mesh Collision Sentinel (Anti-Clipping)
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
    
    for arm in armatures:
        # Apply slight pushback if requested by AI to prevent clipping
        if pushback != [0,0,0]:
            arm.location[0] += pushback[0]
            arm.location[1] += pushback[1]
            arm.location[2] += pushback[2]
            arm.keyframe_insert(data_path="location", frame=impact_frame)
            
    # 2. Add Rigid Body Collisions to Environment (Safe Universal Filter)
    env_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and not (obj.name.startswith("OMNI_CHAR") or obj.name.startswith("CH_"))]
    
    # Ensure Scene has Rigid Body World
    if not bpy.context.scene.rigidbody_world:
        bpy.ops.rigidbody.world_add()

    for obj in env_objects:
        if not obj.rigid_body:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.rigidbody.object_add()
            obj.rigid_body.type = 'PASSIVE' # Static environment
            obj.rigid_body.collision_shape = 'MESH'
            
    # 3. Spawn Impact Particles (If impact exists)
    if has_impact and particles > 0:
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.1, location=(0, 0, 1))
        emitter = bpy.context.active_object
        emitter.name = "OMNI_Impact_Emitter"
        
        # Sync with universal Focus Target if available
        tracker = bpy.data.objects.get("OMNIMATRIX_Focus_Target") or bpy.data.objects.get("Focus_Tracker")
        if tracker:
            emitter.location = tracker.location
            
        # Add Particle System
        bpy.ops.object.particle_system_add()
        psys = emitter.particle_systems[0]
        psets = psys.settings
        
        psets.count = particles
        psets.frame_start = impact_frame
        psets.frame_end = impact_frame + 2 # Short burst
        psets.lifetime = 15
        psets.normal_factor = 10.0 # Explosive speed
        psets.physics_type = 'NEWTON'
        psets.mass = 0.5
        
        # Hide emitter mesh
        emitter.show_instancer_for_render = False
        emitter.show_instancer_for_viewport = False

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS: OmniMatrix Physics & Collisions secured.")

except Exception as e:
    print(f"ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_physics_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def secure_mesh_collisions(self):
        self.log_message("Initializing OmniMatrix Physics Sentinel...", "INFO")
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                self.log_message(f"--- Scanning Physics for: {scene_name} ---", "INFO")
                
                context = self._load_upstream_context(scene_name)
                physics_data = self._query_physics_brain(scene_name, context)
                
                self.log_message(f"Physics AI: {physics_data.get('rationale', 'Default')} | Pushback: {physics_data.get('anti_clipping_pushback')}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, physics_data)
                
                command = [self.blender_path, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        self.log_message(f"Collisions and Impacts baked into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = physics_data
                    else:
                        self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 27 Pipeline Complete. Environment is physically secure.", "INFO")

if __name__ == "__main__":
    sentinel = DynamicMeshCollisionSentinel()
    sentinel.secure_mesh_collisions()
