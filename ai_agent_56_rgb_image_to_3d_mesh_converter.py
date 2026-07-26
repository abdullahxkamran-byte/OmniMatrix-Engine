import os
import re
import sys
import glob
import json
import time
import shutil
import platform
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

# Attempt importing local image processing libraries
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Attempt importing Gradio client for 100% FREE Hugging Face 3D AI inference
try:
    from gradio_client import Client, file
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False

# =====================================================================
# RULE 2 & 14: UNIVERSAL ENVIRONMENT & ZERO-BUDGET API CONFIGURATION
# =====================================================================
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class Ai_Agent_56_RGB_Image_To_3D_Mesh_Converter:
    """
    OMNIMATRIX V2.0 GOD-LEVEL RGB IMAGE TO 3D MESH CONVERTER (ZERO-BUDGET EDITION)
    Acts as the master 3D asset alchemist and geometry synthesizer.
    Ingests transparent 2D character layers from Agent 55, deploying 100% FREE
    Hugging Face Spaces (TripoSR / InstantMesh via gradio_client) to reconstruct
    full 3D OBJ/FBX meshes without commercial API costs. Synthesizes mathematical
    2.5D UV-mapped billboards during offline fallbacks and normalizes geometry.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "Ai_Agent_56_RGB_Image_To_3D_Mesh_Converter"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        self.module_h_dir = os.path.join(self.workspace_dir, "Module_H_Generative")
        self.inputs_dir = os.path.join(self.module_h_dir, "outputs_vision_layers")
        self.outputs_dir = os.path.join(self.module_h_dir, "3d_meshes")
        
        self.state_path = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        self.output_blueprint_path = os.path.join(self.outputs_dir, "56_master_mesh_blueprint.json")
        self.blender_script_path = os.path.join(self.outputs_dir, "56_actionable_blender_import.py")
        
        self.max_texture_dimension_px = 2048
        self.max_model_scale_units = 1.5
        
        self.hf_token = os.environ.get("HF_TOKEN", os.environ.get("HF_API_KEY", None))
        self.model_library_registry = {}

        for directory in [self.workspace_dir, self.module_h_dir, self.inputs_dir, self.outputs_dir]:
            os.makedirs(directory, exist_ok=True)
            
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        formatted = f"[{level}] [{self.agent_name}] {message}"
        print(formatted)

    def _scrub_legacy_assets(self):
        if os.path.exists(self.outputs_dir):
            for file_name in os.listdir(self.outputs_dir):
                file_path = os.path.join(self.outputs_dir, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as error:
                    self.log(f"Failed to scrub legacy 3D mesh asset {file_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & PIPELINE ROUTING
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS", blueprint_manifest=None):
        matrix_path = os.path.join(self.workspace_dir, "matrix_state.json")
        data = {}
        if os.path.exists(matrix_path):
            try:
                with open(matrix_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        if "orchestrator_matrix" not in data:
            data["orchestrator_matrix"] = {}
            
        data["orchestrator_matrix"].update({
            "last_active_agent": self.agent_name,
            "last_update_timestamp": time.time(),
            "agent_status": {self.agent_name: status}
        })
        if blueprint_manifest:
            data["orchestrator_matrix"]["Module_H_Mesh_Registry"] = blueprint_manifest
            
        if status == "COMPLETED":
            data["orchestrator_matrix"]["next_agent"] = "ai_agent_57_dynamic_2d_panel_to_3d_world_forge"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_global_config(self):
        default_config = {"mesh_generation_mode": "auto", "target_style": "anime_cel_shaded"}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except Exception:
                pass
        return default_config

    # =====================================================================
    # MATHEMATICAL GEOMETRY NORMALIZATION ENGINE (RULE 17 SAFEGUARD)
    # =====================================================================
    def _normalize_mesh_coordinates(self, mesh_path):
        if not os.path.exists(mesh_path) or not os.path.isfile(mesh_path):
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

            xs, ys, zs = [v[0] for v in vertices], [v[1] for v in vertices], [v[2] for v in vertices]
            cx, cy, cz = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0, (min(zs) + max(zs)) / 2.0
            max_dim = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
            scale_factor = 1.0 if max_dim == 0 else (self.max_model_scale_units / max_dim)

            normalized_vertices = [
                ((v[0] - cx) * scale_factor, (v[1] - cy) * scale_factor, (v[2] - cz) * scale_factor)
                for v in vertices
            ]

            with open(mesh_path, "w", encoding="utf-8") as f:
                f.write("# OMNIMATRIX V2.0 Auto-Normalized 3D Mesh Geometry\n")
                for nv in normalized_vertices:
                    f.write(f"v {nv[0]:.6f} {nv[1]:.6f} {nv[2]:.6f}\n")
                for line in other_lines:
                    f.write(line)
            self.log(f"Normalized 3D mesh geometry: centered origin and scaled to {self.max_model_scale_units} units.", "SUCCESS")
        except Exception as error:
            self.log(f"Mesh geometry normalization exception: {error}", "ERROR")

    # =====================================================================
    # RULE 10: 100% OFFLINE PROCEDURAL 2.5D BILLBOARD ALCHEMIST (ZERO COST)
    # =====================================================================
    def _generate_procedural_25d_billboard(self, image_path, obj_path, mtl_path, tex_path):
        self.log("Engaging Offline Procedural Alchemist: Synthesizing 2.5D UV-mapped billboard (0$ Cost)...", "WARNING")
        
        width_ratio, height_ratio = 1.0, 1.0
        
        if PIL_AVAILABLE and os.path.exists(image_path) and os.path.isfile(image_path):
            try:
                img = Image.open(image_path)
                if max(img.size) > self.max_texture_dimension_px:
                    img.thumbnail((self.max_texture_dimension_px, self.max_texture_dimension_px), Image.Resampling.LANCZOS)
                img.save(tex_path, "PNG")
                w, h = img.size
                if w > h:
                    height_ratio = h / float(w)
                else:
                    width_ratio = w / float(h)
            except Exception as error:
                self.log(f"PIL texture processing exception: {error}", "WARNING")
                shutil.copy(image_path, tex_path)
        else:
            if os.path.exists(image_path) and os.path.isfile(image_path):
                shutil.copy(image_path, tex_path)

        try:
            hw, hh = (width_ratio * self.max_model_scale_units) / 2.0, (height_ratio * self.max_model_scale_units) / 2.0
            with open(obj_path, "w", encoding="utf-8") as f:
                f.write(f"mtllib {os.path.basename(mtl_path)}\n")
                f.write("o OmniMatrix_Procedural_Billboard\n")
                f.write(f"v {-hw:.4f} {-hh:.4f} 0.0000\n")
                f.write(f"v {hw:.4f} {-hh:.4f} 0.0000\n")
                f.write(f"v {hw:.4f} {hh:.4f} 0.0000\n")
                f.write(f"v {-hw:.4f} {hh:.4f} 0.0000\n")
                f.write("vt 0.0000 0.0000\nvt 1.0000 0.0000\nvt 1.0000 1.0000\nvt 0.0000 1.0000\n")
                f.write("vn 0.0000 0.0000 1.0000\n")
                f.write("usemtl Material_Billboard_Alpha\n")
                f.write("f 1/1/1 2/2/1 3/3/1 4/4/1\n")
        except Exception as error:
            self.log(f"Billboard OBJ compilation exception: {error}", "ERROR")

        try:
            with open(mtl_path, "w", encoding="utf-8") as f:
                f.write("newmtl Material_Billboard_Alpha\n")
                f.write("Ka 1.000 1.000 1.000\nKd 1.000 1.000 1.000\nKs 0.000 0.000 0.000\n")
                f.write(f"map_Kd {os.path.basename(tex_path)}\n")
                f.write(f"map_d {os.path.basename(tex_path)}\n")
        except Exception as error:
            self.log(f"Billboard MTL compilation exception: {error}", "ERROR")

    # =====================================================================
    # RULE 6, 14, 16: ZERO-BUDGET HUGGINGFACE FREE 3D GENERATION MATRIX
    # =====================================================================
    def _process_single_character_mesh(self, image_path, char_name, config):
        mesh_out = os.path.join(self.outputs_dir, f"{char_name}_mesh.obj")
        mtl_out = os.path.join(self.outputs_dir, f"{char_name}_mesh.mtl")
        tex_out = os.path.join(self.outputs_dir, f"{char_name}_texture.png")
        
        mode = config.get("mesh_generation_mode", "auto")
        success = False

        if mode == "2.5D_billboard":
            self.log(f"Configuration enforced 2.5D billboard generation for '{char_name}'.", "INFO")
            self._generate_procedural_25d_billboard(image_path, mesh_out, mtl_out, tex_out)
            return {"mesh_obj_path": mesh_out, "material_mtl_path": mtl_out, "texture_png_path": tex_out}

        # Core 1: 100% FREE Hugging Face TripoSR Space via Gradio Client
        if GRADIO_AVAILABLE and mode in ["auto", "full_3d"] and not success and os.path.exists(image_path) and os.path.isfile(image_path):
            self.log(f"Executing Core 1 (FREE HuggingFace TripoSR Space) for '{char_name}'...", "INFO")
            try:
                client = Client("stabilityai/TripoSR", hf_token=self.hf_token)
                result = client.predict(image=file(image_path), api_name="/generate_3d")
                
                if isinstance(result, (list, tuple)):
                    for temp_file in result:
                        temp_str = str(temp_file)
                        if temp_str.endswith('.obj'):
                            shutil.copy(temp_str, mesh_out)
                        elif temp_str.endswith('.mtl'):
                            shutil.copy(temp_str, mtl_out)
                        elif temp_str.endswith('.png'):
                            shutil.copy(temp_str, tex_out)
                    success = True
                    self.log(f"FREE HuggingFace TripoSR 3D reconstruction successful for '{char_name}'!", "SUCCESS")
            except Exception as error:
                self.log(f"FREE TripoSR Space inference exception: {error}. Routing to Core 2...", "WARNING")

        # Core 2: 100% FREE Hugging Face InstantMesh Space via Gradio Client
        if GRADIO_AVAILABLE and mode in ["auto", "full_3d"] and not success and os.path.exists(image_path) and os.path.isfile(image_path):
            self.log(f"Executing Core 2 (FREE HuggingFace InstantMesh Space) for '{char_name}'...", "INFO")
            try:
                client = Client("TencentARC/InstantMesh", hf_token=self.hf_token)
                result = client.predict(image=file(image_path), api_name="/generate_obj")
                
                if isinstance(result, (list, tuple)) or isinstance(result, str):
                    temp_files = result if isinstance(result, (list, tuple)) else [result]
                    for temp_file in temp_files:
                        temp_str = str(temp_file)
                        if temp_str.endswith('.obj'):
                            shutil.copy(temp_str, mesh_out)
                        elif temp_str.endswith('.mtl'):
                            shutil.copy(temp_str, mtl_out)
                        elif temp_str.endswith('.png'):
                            shutil.copy(temp_str, tex_out)
                    success = True
                    self.log(f"FREE HuggingFace InstantMesh 3D reconstruction successful for '{char_name}'!", "SUCCESS")
            except Exception as error:
                self.log(f"FREE InstantMesh Space inference exception: {error}. Routing to Core 3...", "WARNING")

        # Core 3: 100% Offline Procedural 2.5D Billboard Alchemist (Rule 10)
        if not success:
            self.log(f"Free online 3D AI spaces busy/offline. Engaging Core 3 (0$ Cost 2.5D Billboard) for '{char_name}'...", "WARNING")
            self._generate_procedural_25d_billboard(image_path, mesh_out, mtl_out, tex_out)
        else:
            self._normalize_mesh_coordinates(mesh_out)
            
        return {
            "mesh_obj_path": mesh_out if os.path.exists(mesh_out) else "",
            "material_mtl_path": mtl_out if os.path.exists(mtl_out) else "",
            "texture_png_path": tex_out if os.path.exists(tex_out) else ""
        }

    # =====================================================================
    # RULE 9: ACTIONABLE BLENDER IMPORTER COMPILER
    # =====================================================================
    def _compile_actionable_blender_script(self, master_blueprint):
        script_content = [
            "import bpy",
            "import os",
            "",
            "# OMNIMATRIX V2.0 Actionable Abstraction: Automated 3D Mesh & Billboard Importer",
            "def clear_scene_geometry():",
            "    bpy.ops.wm.read_factory_settings(use_empty=True)",
            "",
            "def import_obj_asset(filepath, target_name, shader_mode='toon_shader'):",
            "    if not os.path.exists(filepath):",
            "        return",
            "    bpy.ops.import_scene.obj(filepath=filepath)",
            "    imported_objs = bpy.context.selected_objects",
            "    if not imported_objs:",
            "        return",
            "    obj = imported_objs[0]",
            "    obj.name = target_name",
            "    for mat_slot in obj.material_slots:",
            "        if mat_slot.material:",
            "            mat_slot.material.blend_method = 'HASHED'",
            "            mat_slot.material.shadow_method = 'HASHED'",
            "            if shader_mode == 'toon_shader' and mat_slot.material.node_tree:",
            "                for node in mat_slot.material.node_tree.nodes:",
            "                    if node.type == 'BSDF_PRINCIPLED':",
            "                        node.inputs['Roughness'].default_value = 0.95",
            "                        node.inputs['Specular IOR Level'].default_value = 0.05",
            "",
            "clear_scene_geometry()"
        ]

        for scene_name, data in master_blueprint.items():
            mesh_path = data.get("mesh_obj_path", "")
            blender_hints = data.get("blender_3d_blueprint", {})
            shader_type = blender_hints.get("shader_type", "toon_shader")
            
            if mesh_path:
                safe_path = mesh_path.replace("\\", "/")
                script_content.append(f"import_obj_asset('{safe_path}', '{scene_name}_character_mesh', '{shader_type}')")

        with open(self.blender_script_path, "w", encoding="utf-8") as f:
            f.write("\n".join(script_content))
            
        self.log(f"Actionable Blender import script compiled: '{self.blender_script_path}'", "SUCCESS")

    def execute_conversion_pipeline(self):
        self._handshake("IN_PROGRESS")
        self.log("Activating RGB Image to 3D Mesh Converter & Alchemist (Zero-Budget)...")
        
        config = self._load_global_config()
        json_files = sorted(glob.glob(os.path.join(self.inputs_dir, "*_vision_manifest.json")))
        
        if not json_files:
            self.log(f"No vision manifests detected in '{self.inputs_dir}'. Synthesizing dummy verification mesh.", "WARNING")
            dummy_out = self._process_single_character_mesh("dummy_path.png", "Char_scene_001", config)
            master_blueprint = {"scene_001": dummy_out}
            master_blueprint["scene_001"]["is_reused_from_cache"] = False
            master_blueprint["scene_001"]["blender_3d_blueprint"] = {"shader_type": "toon_shader", "camera_fov": 50}
        else:
            master_blueprint = {}
            for json_path in json_files:
                try:
                    with open(json_path, "r", encoding="utf-8") as jf:
                        vision_data = json.load(jf)
                except Exception as error:
                    self.log(f"Failed reading manifest {json_path}: {error}", "ERROR")
                    continue
                
                base_scene_name = os.path.basename(json_path).replace("_vision_manifest.json", "")
                layers = vision_data.get("layers", {})
                char_image_path = layers.get("character_layer_png", "")
                
                if not char_image_path or not os.path.exists(char_image_path) or not os.path.isfile(char_image_path):
                    self.log(f"Character sprite layer absent for '{base_scene_name}'. Bypassing 3D conversion.", "INFO")
                    continue

                char_name = f"Char_{base_scene_name}"
                self.log(f"--- Converting Visual Layer to 3D Geometry: '{char_name}' ---", "INFO")

                if char_name in self.model_library_registry:
                    self.log(f"Smart Bypass Active: Reusing cached 3D geometry for '{char_name}'.", "INFO")
                    master_blueprint[base_scene_name] = dict(self.model_library_registry[char_name])
                    master_blueprint[base_scene_name]["is_reused_from_cache"] = True
                else:
                    assets = self._process_single_character_mesh(char_image_path, char_name, config)
                    self.model_library_registry[char_name] = assets
                    master_blueprint[base_scene_name] = dict(assets)
                    master_blueprint[base_scene_name]["is_reused_from_cache"] = False
                
                master_blueprint[base_scene_name]["blender_3d_blueprint"] = vision_data.get("blender_3d_blueprint", {})

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self._compile_actionable_blender_script(master_blueprint)
        self._handshake("COMPLETED", master_blueprint)
        self.log("RGB Image to 3D Mesh Conversion Concluded Flawlessly! Zero Budget Spent!", "SUCCESS")
        return master_blueprint

if __name__ == "__main__":
    converter = Ai_Agent_56_RGB_Image_To_3D_Mesh_Converter()
    converter.execute_conversion_pipeline()