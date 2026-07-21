import os
import sys
import json
import re
import math
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
                    os.environ[key.strip()] = val.strip()

load_env_file()

class AutonomousUniversalAutoRigger:
    # 1. Storage Optimization: Separate Temp (Drive) and Assets (Local)
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 58: Autonomous Universal Auto-Rigger"
        
        # Upstream Inputs (From Drive)
        self.vision_outputs_dir = os.path.join(drive_temp_dir, "outputs")
        self.meshes_dir = os.path.join(drive_temp_dir, "3d_meshes")
        self.input_blueprint_path = os.path.join(self.meshes_dir, "56_master_mesh_blueprint.json")
        
        # Outputs (Going to Local Hard Drive!)
        self.rig_dir = os.path.join(local_library_dir, "rigged_assets")
        self.output_rig_blueprint = os.path.join(self.rig_dir, "58_master_rig_blueprint.json")
        
        # Blender Executable Path
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [drive_temp_dir, self.rig_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _analyze_mesh_bounds(self, mesh_path):
        """Calculates exact 3D limits of the mesh to guide the AI for bone placement."""
        default_bounds = {"min_x": -1, "max_x": 1, "min_y": -1, "max_y": 1, "min_z": 0, "max_z": 2}
        if not os.path.exists(mesh_path):
            return default_bounds

        try:
            x_coords, y_coords, z_coords = [], [], []
            with open(mesh_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("v "):
                        parts = line.split()
                        if len(parts) >= 4:
                            x_coords.append(float(parts[1]))
                            y_coords.append(float(parts[2]))
                            z_coords.append(float(parts[3]))

            if not z_coords:
                return default_bounds

            return {
                "min_x": min(x_coords), "max_x": max(x_coords),
                "min_y": min(y_coords), "max_y": max(y_coords),
                "min_z": min(z_coords), "max_z": max(z_coords),
                "height": abs(max(z_coords) - min(z_coords)),
                "width": abs(max(x_coords) - min(x_coords))
            }
        except Exception as e:
            self.log_message(f"Error parsing mesh dimensions: {str(e)}", "WARNING")
            return default_bounds

    def _get_fallback_biped_rig(self, bounds):
        """Offline fallback if AI API fails. Now includes Weapon Socket and Jaw."""
        z_min = bounds["min_z"]
        height = bounds["height"]
        root_z = z_min + (height * 0.5)
        spine_z = z_min + (height * 0.7)
        head_z = z_min + (height * 0.9)
        
        return [
            {"name": "Root", "parent": None, "head": [0, 0, z_min], "tail": [0, 0, root_z]},
            {"name": "Spine", "parent": "Root", "head": [0, 0, root_z], "tail": [0, 0, spine_z]},
            {"name": "NeckHead", "parent": "Spine", "head": [0, 0, spine_z], "tail": [0, 0, head_z]},
            
            # 2. Facial Rigging Fallback
            {"name": "Jaw", "parent": "NeckHead", "head": [0, -0.1, head_z - 0.05], "tail": [0, -0.2, head_z - 0.1]},
            
            {"name": "Arm_L", "parent": "Spine", "head": [0.2, 0, spine_z], "tail": [0.8, 0, spine_z]},
            {"name": "Arm_R", "parent": "Spine", "head": [-0.2, 0, spine_z], "tail": [-0.8, 0, spine_z]},
            
            # 3. Weapon Socket Fallback (Attached to Right Arm/Hand)
            {"name": "Weapon_Socket", "parent": "Arm_R", "head": [-0.8, 0, spine_z], "tail": [-0.8, -0.2, spine_z]},
            
            {"name": "Leg_L", "parent": "Root", "head": [0.2, 0, root_z], "tail": [0.2, 0, z_min]},
            {"name": "Leg_R", "parent": "Root", "head": [-0.2, 0, root_z], "tail": [-0.2, 0, z_min]}
        ]

    def _generate_custom_bone_hierarchy(self, char_name, bg_desc, bounds):
        """Asks Gemini to create a custom anatomical bone structure."""
        if not self.gemini_api_key:
            self.log_message("No Gemini API key found. Using fallback AAA rig.", "WARNING")
            return self._get_fallback_biped_rig(bounds)

        prompt = (
            "You are an Expert AAA 3D Technical Director and Rigger.\n"
            f"Character Name: {char_name}\n"
            f"Context/Description: {bg_desc}\n"
            f"Mesh Physical Bounds: X[{bounds['min_x']:.2f} to {bounds['max_x']:.2f}], "
            f"Y[{bounds['min_y']:.2f} to {bounds['max_y']:.2f}], Z[{bounds['min_z']:.2f} to {bounds['max_z']:.2f}].\n\n"
            "Create a custom bone hierarchy for this specific character. "
            "If it's an animal, make quadruped bones. If it's a character with 4 arms (like Sukuna) or tails, include bones for them.\n\n"
            "CRITICAL AAA REQUIREMENTS:\n"
            "1. FACIAL RIGGING: You MUST include a 'Jaw' bone and 'Eye_L' / 'Eye_R' bones parented to the Head for facial expressions.\n"
            "2. WEAPON SOCKET: You MUST include a 'Weapon_Socket' bone parented to the dominant hand/arm for prop attachments.\n\n"
            "ALL bone coordinates (head and tail [x,y,z]) MUST strictly stay within the Mesh Physical Bounds provided.\n"
            "Return ONLY raw JSON, without markdown formatting. Format exactly like this:\n"
            "{\n"
            "  \"bones\": [\n"
            "    {\"name\": \"Root\", \"parent\": null, \"head\": [0.0, 0.0, 0.1], \"tail\": [0.0, 0.0, 0.5]}\n"
            "  ]\n"
            "}"
        )

        try:
            payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                
                rig_data = json.loads(res_text)
                self.log_message(f"AI successfully generated custom AAA anatomy for {char_name}.", "INFO")
                return rig_data.get("bones", self._get_fallback_biped_rig(bounds))
        except Exception as e:
            self.log_message(f"AI Rig Generation failed: {str(e)}. Using fallback AAA rig.", "ERROR")
            return self._get_fallback_biped_rig(bounds)

    def _generate_blender_rig_script(self, mesh_path, fbx_out_path, bone_data):
        """Generates a Blender python script that builds the skeleton."""
        safe_mesh_path = mesh_path.replace("\\", "/")
        safe_fbx_path = fbx_out_path.replace("\\", "/")
        safe_blend_path = safe_fbx_path.replace(".fbx", ".blend") # Saving .blend for manual tweaks
        
        bones_json = json.dumps(bone_data)

        blender_script = f"""
import bpy
import json
import sys

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

try:
    clear_scene()

    mesh_path = "{safe_mesh_path}"
    try:
        bpy.ops.wm.obj_import(filepath=mesh_path)
    except AttributeError:
        bpy.ops.import_scene.obj(filepath=mesh_path)

    mesh_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            mesh_obj = obj
            break

    if not mesh_obj:
        raise ValueError("No mesh found after import.")

    bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
    armature_obj = bpy.context.active_object
    armature_obj.name = "Custom_AI_Rig"
    armature = armature_obj.data
    
    for bone in armature.edit_bones:
        armature.edit_bones.remove(bone)

    bone_data = json.loads('''{bones_json}''')
    edit_bones_dict = {{}}

    for b_info in bone_data:
        b_name = b_info.get("name", "Bone")
        eb = armature.edit_bones.new(b_name)
        eb.head = b_info.get("head", (0, 0, 0))
        eb.tail = b_info.get("tail", (0, 0, 1))
        edit_bones_dict[b_name] = eb

    for b_info in bone_data:
        parent_name = b_info.get("parent")
        if parent_name and parent_name in edit_bones_dict:
            child_bone = edit_bones_dict[b_info["name"]]
            child_bone.parent = edit_bones_dict[parent_name]
            child_bone.use_connect = False

    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    armature_obj.select_set(True)
    bpy.context.view_layer.objects.active = armature_obj

    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    bpy.ops.export_scene.fbx(
        filepath="{safe_fbx_path}",
        use_selection=False,
        apply_unit_scale=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
        armature_nodetype='NULL'
    )
    
    # Save Blend file in Local Storage for maximum editability
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    
    print("SUCCESS")
except Exception as e:
    print("ERROR:", str(e))
    sys.exit(1)
"""
        script_path = os.path.join("temp_blender_rig_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(blender_script)
        return script_path

    def execute_batch_rigging(self):
        self.log_message("Initializing Universal Skeleton Auto-Rigger Engine...", "INFO")
        
        if not os.path.exists(self.input_blueprint_path):
            self.log_message("Agent 56 Blueprint missing. Cannot proceed.", "ERROR")
            return

        with open(self.input_blueprint_path, "r", encoding="utf-8") as f:
            master_mesh_blueprint = json.load(f)

        master_rig_blueprint = {}
        rigged_memory = {}

        for scene_name, mesh_data in master_mesh_blueprint.items():
            obj_path = mesh_data.get("mesh", "")
            if not obj_path or not os.path.exists(obj_path):
                continue

            vision_json_path = os.path.join(self.vision_outputs_dir, f"{scene_name}_vision.json")
            char_name = "Unknown"
            bg_desc = ""
            
            # Smart Environment Bypass: If no characters, skip rigging entirely!
            if os.path.exists(vision_json_path):
                with open(vision_json_path, "r", encoding="utf-8") as vf:
                    v_data = json.load(vf)
                    if v_data.get("pipeline_mode") == "Environment":
                        self.log_message(f"Skipping rigging for {scene_name} (Environment Only).", "INFO")
                        continue
                    char_name = v_data.get("character_name", "Unknown").replace(" ", "_")
                    bg_desc = v_data.get("background_description", "")

            self.log_message(f"--- Rigging Sequence: {scene_name} | Target: {char_name} ---", "INFO")

            if mesh_data.get("is_reused", False) and char_name in rigged_memory:
                self.log_message(f"Smart Bypass: Linking existing rig for {char_name}", "INFO")
                master_rig_blueprint[scene_name] = rigged_memory[char_name]
                continue

            # Outputting strictly to Local Drive!
            fbx_out_path = os.path.join(self.rig_dir, f"{char_name}_rigged.fbx")

            bounds = self._analyze_mesh_bounds(obj_path)
            bone_data = self._generate_custom_bone_hierarchy(char_name, bg_desc, bounds)
            script_path = self._generate_blender_rig_script(obj_path, fbx_out_path, bone_data)

            self.log_message(f"Binding skeleton to {char_name} using Headless Blender...", "INFO")
            command = [self.blender_path, "-b", "-P", script_path]
            
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0 and os.path.exists(fbx_out_path):
                    self.log_message(f"Exported successfully to LOCAL DRIVE: {char_name}_rigged.fbx", "INFO")
                    
                    rig_info = {
                        "rigged_fbx": fbx_out_path,
                        "rigged_blend": fbx_out_path.replace(".fbx", ".blend"),
                        "bone_count": len(bone_data),
                        "material": mesh_data.get("material", ""),
                        "texture": mesh_data.get("texture", "")
                    }
                    rigged_memory[char_name] = rig_info
                    master_rig_blueprint[scene_name] = rig_info
                else:
                    self.log_message(f"Blender failed. Log: {result.stdout[-300:]}", "ERROR")
            except Exception as e:
                self.log_message(f"Subprocess failed. Is Blender in system PATH? {str(e)}", "CRITICAL")
            
            if os.path.exists(script_path):
                os.remove(script_path)

        with open(self.output_rig_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_rig_blueprint, f, indent=4)

        self.log_message("Universal Auto-Rigging Pipeline Complete!", "INFO")

if __name__ == "__main__":
    rigger = AutonomousUniversalAutoRigger()
    rigger.execute_batch_rigging()
