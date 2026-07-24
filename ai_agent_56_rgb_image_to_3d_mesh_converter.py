# ==============================================================================
# Ai_Agent_56_RGB_Image_To_3D_Mesh_Converter.py
# MODULE H: Omni Generative Matrix (3D Mesh Converter)
# ==============================================================================

import os
import sys
import json
import re
import urllib.request
import shutil
import glob

# 100% OFFLINE AUTONOMY DEPENDENCIES
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# API DEPENDENCIES
try:
    from gradio_client import Client
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()


class AiAgent56RgbImageTo3dMeshConverter:
    def __init__(self):
        self.agent_name = "Ai_Agent_56"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_root = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.module_h_dir = os.path.join(self.workspace_root, "Module_H_Generative")
        self.inputs_dir = os.path.join(self.module_h_dir, "outputs_vision_layers")
        self.outputs_dir = os.path.join(self.module_h_dir, "3d_meshes")
        
        self.state_file = os.path.join(self.workspace_root, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_root, "global_config.json")
        
        self.output_blueprint_path = os.path.join(self.outputs_dir, "56_master_mesh_blueprint.json")
        self.blender_script_path = os.path.join(self.outputs_dir, "56_actionable_blender_import.py")
        
        self.hf_token = os.environ.get("HF_TOKEN", os.environ.get("HF_API_KEY", None))
        
        # Memory for Smart Bypass
        self.model_library = {} 

        self._initialize_directories()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _initialize_directories(self):
        for d in [self.workspace_root, self.module_h_dir, self.inputs_dir, self.outputs_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    # RULE 3: IDEMPOTENCY SCRUBBING
    def scrub_workspace(self):
        self.log("Scrubbing legacy 3D meshes to ensure idempotency...", "INFO")
        for filename in os.listdir(self.outputs_dir):
            file_path = os.path.join(self.outputs_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                self.log(f"Failed to delete {file_path}. Reason: {e}", "WARNING")

    # RULE 4: LIMITLESS FLUIDITY
    def load_global_config(self):
        default_config = {
            "mesh_generation_mode": "auto", # Options: auto, full_3d, 2.5D_billboard
            "target_style": "anime"
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception:
                pass
        return default_config

    def _normalize_mesh_coordinates(self, mesh_path):
        """Mathematical Utility: Centers and scales the 3D model cleanly."""
        if not os.path.exists(mesh_path):
            return

        try:
            vertices = []
            other_lines = []
            
            with open(mesh_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("v "):
                        parts = line.strip().split()
                        vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                    else:
                        other_lines.append(line)
                        
            if not vertices:
                return

            xs = [v[0] for v in vertices]
            ys = [v[1] for v in vertices]
            zs = [v[2] for v in vertices]
            
            cx, cy, cz = (min(xs)+max(xs))/2.0, (min(ys)+max(ys))/2.0, (min(zs)+max(zs))/2.0
            max_dim = max(max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs))
            scale_factor = 1.0 if max_dim == 0 else (1.5 / max_dim)

            normalized_vertices = []
            for v in vertices:
                normalized_vertices.append(((v[0]-cx)*scale_factor, (v[1]-cy)*scale_factor, (v[2]-cz)*scale_factor))

            with open(mesh_path, "w", encoding="utf-8") as f:
                f.write("# OmniMatrix Auto-Normalized Mesh\n")
                for nv in normalized_vertices:
                    f.write(f"v {nv[0]:.6f} {nv[1]:.6f} {nv[2]:.6f}\n")
                for line in other_lines:
                    f.write(line)
                    
        except Exception as e:
            self.log(f"Failed to normalize mesh: {str(e)}", "ERROR")

    # RULE 10: 100% OFFLINE AUTONOMY FALLBACK (Procedural 2.5D Billboard)
    def _generate_procedural_2_5d_billboard(self, image_path, obj_path, mtl_path, tex_path):
        """
        If APIs fail or user requests 2.5D, we don't hallucinate a broken back.
        We generate a perfectly UV-mapped flat 3D plane (cardboard cutout).
        """
        self.log("Engaging Offline Procedural Math: Generating 2.5D UV-Mapped Billboard...", "STATUS")
        
        width_ratio = 1.0
        height_ratio = 1.0
        
        if PIL_AVAILABLE and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                w, h = img.size
                img.save(tex_path, "PNG")
                if w > h:
                    height_ratio = h / w
                else:
                    width_ratio = w / h
            except Exception as e:
                self.log(f"PIL Image logic failed: {e}", "WARNING")
                shutil.copy(image_path, tex_path)
        else:
            shutil.copy(image_path, tex_path)

        # Write .OBJ (A flat plane with proper UV coordinates)
        try:
            with open(obj_path, "w", encoding="utf-8") as f:
                f.write(f"mtllib {os.path.basename(mtl_path)}\n")
                f.write("o Procedural_Billboard\n")
                # Vertices
                hw, hh = width_ratio / 2.0, height_ratio / 2.0
                f.write(f"v {-hw} {-hh} 0.0\n")
                f.write(f"v {hw} {-hh} 0.0\n")
                f.write(f"v {hw} {hh} 0.0\n")
                f.write(f"v {-hw} {hh} 0.0\n")
                # UVs
                f.write("vt 0.0 0.0\nvt 1.0 0.0\nvt 1.0 1.0\nvt 0.0 1.0\n")
                # Normals
                f.write("vn 0.0 0.0 1.0\n")
                # Faces
                f.write("usemtl Material01\n")
                f.write("f 1/1/1 2/2/1 3/3/1 4/4/1\n")
        except Exception as e:
            self.log(f"Failed writing fallback OBJ: {e}", "CRITICAL")

        # Write .MTL
        try:
            with open(mtl_path, "w", encoding="utf-8") as f:
                f.write("newmtl Material01\n")
                f.write("Ka 1.0 1.0 1.0\nKd 1.0 1.0 1.0\nKs 0.0 0.0 0.0\n")
                f.write(f"map_Kd {os.path.basename(tex_path)}\n")
                f.write(f"map_d {os.path.basename(tex_path)}\n") # Alpha transparency
        except Exception as e:
            self.log(f"Failed writing fallback MTL: {e}", "CRITICAL")

    # RULE 6: QUAD-CORE FALLBACK MATRIX FOR 3D GENERATION
    def _process_single_character(self, image_path, char_name, config):
        mesh_out = os.path.join(self.outputs_dir, f"{char_name}_mesh.obj")
        mtl_out = os.path.join(self.outputs_dir, f"{char_name}_mesh.mtl")
        tex_out = os.path.join(self.outputs_dir, f"{char_name}_texture.png")
        
        mode = config.get("mesh_generation_mode", "auto")
        success = False

        if mode == "2.5D_billboard":
            self.log(f"Config enforced 2.5D mode for {char_name}.", "INFO")
            self._generate_procedural_2_5d_billboard(image_path, mesh_out, mtl_out, tex_out)
            return {"mesh": mesh_out, "material": mtl_out, "texture": tex_out}

        # Core 2/3 Equivalent for 3D: Gradio / HuggingFace TripoSR
        if GRADIO_AVAILABLE and self.hf_token and mode in ["auto", "full_3d"]:
            self.log(f"Executing Core 2 (HuggingFace TripoSR) for: {char_name}", "INFO")
            try:
                client = Client("stabilityai/TripoSR", hf_token=self.hf_token)
                result = client.predict(image=image_path, api_name="/generate_3d")
                
                if isinstance(result, (list, tuple)):
                    for temp_file in result:
                        temp_str = str(temp_file)
                        if temp_str.endswith('.obj'): shutil.copy(temp_str, mesh_out)
                        elif temp_str.endswith('.mtl'): shutil.copy(temp_str, mtl_out)
                        elif temp_str.endswith('.png'): shutil.copy(temp_str, tex_out)
                    success = True
            except Exception as e:
                self.log(f"HuggingFace API failed: {str(e)}", "WARNING")

        # Core 4: Procedural Math Fallback
        if not success:
            self.log("Online 3D AI failed or unavailable. Engaging Core 4 (Procedural 2.5D Billboard)...", "WARNING")
            self._generate_procedural_2_5d_billboard(image_path, mesh_out, mtl_out, tex_out)
        
        if success:
            self._normalize_mesh_coordinates(mesh_out)
            
        return {
            "mesh": mesh_out if os.path.exists(mesh_out) else "",
            "material": mtl_out if os.path.exists(mtl_out) else "",
            "texture": tex_out if os.path.exists(tex_out) else ""
        }

    # RULE 9: ACTIONABLE ABSTRACTION
    def _generate_actionable_blender_script(self, master_blueprint):
        """Generates a Blender python script that imports all generated meshes instantly."""
        script_content = [
            "import bpy",
            "import os",
            "",
            "# OmniMatrix Actionable Abstraction: Auto-Mesh Importer",
            "def clear_scene():",
            "    bpy.ops.wm.read_factory_settings(use_empty=True)",
            "",
            "def import_obj(filepath, name):",
            "    if not os.path.exists(filepath): return",
            "    bpy.ops.import_scene.obj(filepath=filepath)",
            "    obj = bpy.context.selected_objects[0]",
            "    obj.name = name",
            "    # Basic shading setup",
            "    for mat_slot in obj.material_slots:",
            "        if mat_slot.material:",
            "            mat_slot.material.blend_method = 'HASHED' # Enable transparency",
            "",
            "clear_scene()"
        ]

        for scene_name, data in master_blueprint.items():
            mesh_path = data.get("mesh", "")
            if mesh_path:
                safe_path = mesh_path.replace("\\", "/")
                script_content.append(f"import_obj('{safe_path}', '{scene_name}_character')")

        with open(self.blender_script_path, "w", encoding="utf-8") as f:
            f.write("\n".join(script_content))
            
        self.log(f"Actionable Blender Script generated: {self.blender_script_path}", "SUCCESS")

    def execute_batch_conversion(self):
        self.log("System Initializing...", "INFO")
        
        # RULE 7: ATOMIC HANDSHAKE (Validation)
        state = {}
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                try: state = json.load(f)
                except: pass
                
        if state.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{state.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        self.scrub_workspace()
        config = self.load_global_config()
        
        json_files = sorted(glob.glob(os.path.join(self.inputs_dir, "*_blueprint.json")))
        if not json_files:
            self.log("No vision JSON blueprints found from Ai_Agent_55. Run it first.", "FATAL")
            sys.exit(1)

        master_blueprint = {}

        for json_path in json_files:
            try:
                with open(json_path, "r") as jf:
                    vision_data = json.load(jf)
            except Exception as e:
                self.log(f"Error reading {json_path}: {e}", "ERROR")
                continue
            
            base_scene_name = os.path.basename(json_path).replace("_blueprint.json", "")
            layers = vision_data.get("layers", {})
            char_image_path = layers.get("char_layer", "")
            
            if not char_image_path or not os.path.exists(char_image_path):
                self.log(f"No character layer extracted for {base_scene_name}. Skipping 3D mesh.", "INFO")
                continue

            char_name = f"Char_{base_scene_name}"

            self.log(f"\n--- Scene: {base_scene_name} | Converting to 3D... ---", "INFO")

            # SMART BYPASS / MEMORY REUSE
            if char_name in self.model_library:
                self.log(f"Smart Bypass Active. Reusing 3D model for: {char_name}.", "INFO")
                master_blueprint[base_scene_name] = dict(self.model_library[char_name])
                master_blueprint[base_scene_name]["is_reused"] = True
            else:
                assets = self._process_single_character(char_image_path, char_name, config)
                self.model_library[char_name] = assets
                master_blueprint[base_scene_name] = dict(assets)
                master_blueprint[base_scene_name]["is_reused"] = False
                # Pass forward Blender Shader hints from Agent 55
                master_blueprint[base_scene_name]["blender_blueprint"] = vision_data.get("blender_blueprint", {})

        # Save Final Output Blueprints
        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self._generate_actionable_blender_script(master_blueprint)
        
        # RULE 7: ATOMIC HANDSHAKE (Advance State)
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "Ai_Agent_57_Dynamic_2D_Panel_To_3D_World_Forge"
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Success! Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    converter = AiAgent56RgbImageTo3dMeshConverter()
    converter.execute_batch_conversion()

# ==============================================================================
# END OF FILE
# ==============================================================================
