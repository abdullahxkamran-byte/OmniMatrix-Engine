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

class OmniMatrixDestructionEngine:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 30: OmniMatrix Procedural Destruction Engine"
        
        # Directories
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        # Outputs
        self.output_blueprint = os.path.join(self.env_dir, "30_destruction_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_context(self, scene_name):
        """Loads visual style and heavy collision impact data."""
        context = {
            "visual_style": "omni_neutral",
            "has_heavy_impact": False,
            "impact_frame": 0,
            "impact_force": 0.0,
            "impact_point": [0.0, 0.0, 0.0]
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
                        context["has_heavy_impact"] = scene_data.get("has_major_impact", False)
                        context["impact_frame"] = scene_data.get("impact_frame", 0)
                        # Derive a pseudo-force if not directly available
                        context["impact_force"] = 45.0 if context["has_heavy_impact"] else 0.0
                        context["impact_point"] = scene_data.get("impact_point_coordinates", [0.0, 0.0, 0.0])
            except Exception as e:
                self.log_message(f"Collision data read error: {e}", "WARNING")
                
        return context

    def _query_destruction_brain(self, scene_name, context):
        if not context["has_heavy_impact"] or context["impact_force"] < 15.0:
            return self._fallback_destruction(False)

        if not self.gemini_api_key:
            return self._fallback_destruction(True, context)

        ai_prompt = (
            f"You are the Procedural Destruction TD for the OmniMatrix Engine.\n"
            f"Scene Name: {scene_name}\n"
            f"Visual Style: {context['visual_style']}\n"
            f"Impact Force: {context['impact_force']}\n\n"
            "Determine the Blender Cell Fracture and physics settings based on the style.\n"
            "- If style is 'anime', use 'anti_gravity_float' (rocks floating up), radial chunks.\n"
            "- If style is 'realistic' or 'cinematic', use 'heavy_gravity_crumble', linear splits, realistic debris.\n"
            "- MAX CHUNK COUNT MUST NOT EXCEED 50 (to save Colab RAM).\n"
            "Return ONLY raw JSON:\n"
            "{\n"
            "  \"fracture_center_xyz\": " + str(context['impact_point']) + ",\n"
            "  \"impact_frame\": " + str(context['impact_frame']) + ",\n"
            "  \"shatter_chunk_count\": 40,\n"
            "  \"physics_behavior\": \"anti_gravity_float\",\n"
            "  \"debris_mass_kg\": 5.0,\n"
            "  \"rationale\": \"Anime style impact requires chunks to shatter and float momentarily.\"\n"
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
                if output.get("shatter_chunk_count", 0) > 50:
                    output["shatter_chunk_count"] = 50
                return output
                
        except Exception as e:
            self.log_message(f"AI Destruction Director failed: {str(e)}. Using fallback.", "WARNING")
            return self._fallback_destruction(True, context)

    def _fallback_destruction(self, has_impact, context=None):
        if not has_impact:
            return {
                "impact_frame": 0, "shatter_chunk_count": 0, "physics_behavior": "none",
                "fracture_center_xyz": [0,0,0], "debris_mass_kg": 0.0, "rationale": "No destruction needed."
            }
        return {
            "impact_frame": context.get("impact_frame", 24), "shatter_chunk_count": 30, 
            "physics_behavior": "heavy_gravity_crumble", "fracture_center_xyz": context.get("impact_point", [0,0,0]),
            "debris_mass_kg": 15.0, "rationale": "Fallback standard fracture applied."
        }

    def _generate_blender_script(self, blend_file_path, dest_data):
        """Python script to execute Cell Fracture and Rigid Body Physics Headless."""
        safe_blend_path = blend_file_path.replace("\\", "/")
        
        script_content = f"""
import bpy
import addon_utils

bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

try:
    chunks = {dest_data.get('shatter_chunk_count', 0)}
    frame = {dest_data.get('impact_frame', 0)}
    behavior = "{dest_data.get('physics_behavior', 'none')}"
    mass = {dest_data.get('debris_mass_kg', 1.0)}

    if chunks > 0:
        # 1. Enable Cell Fracture Addon
        addon_utils.enable("object_fracture_cell")
        
        # 2. Find Environment/Floor to fracture (Simplification: targeting active or largest mesh)
        env_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and not obj.name.startswith("CH_") and "Environment" in obj.name or "Floor" in obj.name]
        
        if not env_meshes:
            # Fallback: Just grab any static mesh that isn't a character
            env_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and not obj.parent]

        if env_meshes:
            target_obj = env_meshes[0]
            bpy.context.view_layer.objects.active = target_obj
            target_obj.select_set(True)
            
            # 3. Apply Cell Fracture (Limit source limit to prevent crashes)
            bpy.ops.object.add_fracture_cell_objects(source_limit=chunks, use_materials=True)
            
            # Hide original object
            target_obj.hide_render = True
            target_obj.hide_viewport = True
            
            # 4. Apply Rigid Body Dynamics
            bpy.ops.object.select_all(action='DESELECT')
            # Select all newly created fractured chunks
            fractured = [obj for obj in bpy.context.scene.objects if target_obj.name + "_cell" in obj.name]
            
            for chunk in fractured:
                chunk.select_set(True)
                bpy.context.view_layer.objects.active = chunk
                
                if not chunk.rigid_body:
                    bpy.ops.rigidbody.object_add()
                
                chunk.rigid_body.mass = mass
                chunk.rigid_body.type = 'ACTIVE'
                chunk.rigid_body.kinematic = True # Hold in place until impact
                
                # Keyframe kinematics (Release physics at impact frame)
                chunk.rigid_body.keyframe_insert(data_path="kinematic", frame=frame - 1)
                chunk.rigid_body.kinematic = False
                chunk.rigid_body.keyframe_insert(data_path="kinematic", frame=frame)
                
            # 5. OmniMatrix Stylized Physics (Anime float vs Realistic fall)
            scene = bpy.context.scene
            if behavior == "anti_gravity_float":
                # Reverse/Zero gravity at impact for floating effect
                scene.use_gravity = True
                scene.gravity[2] = -9.81
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame - 5)
                scene.gravity[2] = 1.5 # Slight float up
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame)
                scene.gravity[2] = -9.81 # Return to normal later
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame + 30)

        bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
        print("SUCCESS: OmniMatrix Procedural Destruction (Cell Fracture) baked.")
    else:
        print("INFO: No major destruction detected for this scene.")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_destruction_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def process_environment_destruction(self):
        self.log_message("Initializing OmniMatrix Procedural Destruction Engine...", "INFO")
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_context(scene_name)
                
                if context["has_heavy_impact"]:
                    self.log_message(f"--- Processing Destruction for: {scene_name} ---", "INFO")
                    dest_data = self._query_destruction_brain(scene_name, context)
                    
                    self.log_message(f"AI Decision: {dest_data['rationale']} | Physics: {dest_data['physics_behavior']} | Chunks: {dest_data['shatter_chunk_count']}", "INFO")
                    
                    script_path = self._generate_blender_script(blend_file_path, dest_data)
                    
                    command = [self.blender_path, "-b", "-P", script_path]
                    try:
                        result = subprocess.run(command, capture_output=True, text=True)
                        if result.returncode == 0:
                            self.log_message(f"Cell Fracture and Physics applied to {filename}", "INFO")
                            master_blueprint[scene_name] = dest_data
                        else:
                            self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                    except Exception as e:
                        self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                        
                    if os.path.exists(script_path):
                        os.remove(script_path)
                else:
                    self.log_message(f"Scene '{scene_name}' has no heavy impacts. Skipping Fracture.", "INFO")
                    master_blueprint[scene_name] = self._fallback_destruction(False)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Agent 30 Pipeline Complete. Environment destruction physics applied.", "INFO")

if __name__ == "__main__":
    director = OmniMatrixDestructionEngine()
    director.process_environment_destruction()
