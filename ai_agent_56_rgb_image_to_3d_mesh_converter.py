import os
import sys
import json
import urllib.request
import shutil
import glob

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

try:
    from gradio_client import Client
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False

class RgbImageTo3dMeshConverter:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 56: Smart Batch 3D Converter"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        self.inputs_dir = os.path.join(self.workspace_dir, "outputs")
        self.outputs_dir = os.path.join(self.workspace_dir, "3d_meshes") 
        self.output_blueprint_path = os.path.join(self.outputs_dir, "56_master_mesh_blueprint.json")
        
        self.hf_token = os.environ.get("HF_TOKEN", os.environ.get("HF_API_KEY", None))
        
        # 3D Model Library Memory for Smart Bypass
        self.model_library = {} 

        for d in [self.workspace_dir, self.inputs_dir, self.outputs_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _normalize_mesh_coordinates(self, mesh_path):
        """Centers the 3D model on 0,0,0 and scales it properly."""
        if not os.path.exists(mesh_path):
            return

        self.log_message(f"Normalizing coordinates for: {os.path.basename(mesh_path)}", "INFO")
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
            
            cx = (min(xs) + max(xs)) / 2.0
            cy = (min(ys) + max(ys)) / 2.0
            cz = (min(zs) + max(zs)) / 2.0
            
            max_dim = max(max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs))
            scale_factor = 1.0 if max_dim == 0 else (1.5 / max_dim)

            normalized_vertices = []
            for v in vertices:
                nx = (v[0] - cx) * scale_factor
                ny = (v[1] - cy) * scale_factor
                nz = (v[2] - cz) * scale_factor
                normalized_vertices.append((nx, ny, nz))

            with open(mesh_path, "w", encoding="utf-8") as f:
                f.write("# Z-Net Auto-Normalized Mesh\n")
                for nv in normalized_vertices:
                    f.write(f"v {nv[0]:.6f} {nv[1]:.6f} {nv[2]:.6f}\n")
                for line in other_lines:
                    f.write(line)
                    
        except Exception as e:
            self.log_message(f"Failed to normalize mesh: {str(e)}", "ERROR")

    def _generate_local_fallback_mesh(self, out_path):
        """Creates a basic cube mesh if everything fails."""
        vertices = [
            (-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5),
            (-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5)
        ]
        faces = [
            (1,2,3), (1,3,4), (5,8,7), (5,7,6), (1,5,6), (1,6,2),
            (2,6,7), (2,7,3), (3,7,8), (3,8,4), (5,1,4), (5,4,8)
        ]
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("# Z-Net Offline Fallback Geometry\n")
                for v in vertices: f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
                for face in faces: f.write(f"f {face[0]} {face[1]} {face[2]}\n")
            self.log_message("Local fallback geometry created.", "INFO")
        except Exception as e:
            self.log_message(f"Critical error writing local core geometry: {str(e)}", "CRITICAL")

    def _process_single_character(self, image_path, char_name):
        mesh_out = os.path.join(self.outputs_dir, f"{char_name}_mesh.obj")
        mtl_out = os.path.join(self.outputs_dir, f"{char_name}_mesh.mtl")
        tex_out = os.path.join(self.outputs_dir, f"{char_name}_texture.png")
        
        success = False
        if GRADIO_AVAILABLE and self.hf_token:
            self.log_message(f"Connecting to TripoSR API for: {char_name}", "INFO")
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
                self.log_message(f"TripoSR API failed: {str(e)}", "WARNING")

        if not success:
            self.log_message("Online API failed or unavailable. Generating local fallback...", "WARNING")
            self._generate_local_fallback_mesh(mesh_out)
        
        self._normalize_mesh_coordinates(mesh_out)
        return {"mesh": mesh_out, "material": mtl_out if os.path.exists(mtl_out) else "", "texture": tex_out if os.path.exists(tex_out) else ""}

    def execute_batch_conversion(self):
        self.log_message("Starting Smart Batch 3D Generation Pipeline...", "INFO")
        
        json_files = sorted(glob.glob(os.path.join(self.inputs_dir, "*_vision.json")))
        if not json_files:
            self.log_message("No vision JSON files found. Run Agent 55 first.", "ERROR")
            return

        master_blueprint = {}

        for json_path in json_files:
            base_scene_name = os.path.basename(json_path).replace("_vision.json", "")
            char_image_path = os.path.join(self.inputs_dir, f"{base_scene_name}_02_character.png")
            
            try:
                with open(json_path, "r") as jf:
                    vision_data = json.load(jf)
            except Exception as e:
                self.log_message(f"Error reading {json_path}: {str(e)}. Skipping.", "ERROR")
                continue
            
            char_name = vision_data.get("character_name", f"Unknown_{base_scene_name}").replace(" ", "_")
            is_new_character = vision_data.get("is_new_character", True)

            self.log_message(f"\n--- Scene: {base_scene_name} | Character: {char_name} ---", "INFO")

            # SMART BYPASS LOGIC
            if not is_new_character and char_name in self.model_library:
                self.log_message(f"Smart Bypass Active. Reusing 3D model for: {char_name}.", "INFO")
                master_blueprint[base_scene_name] = dict(self.model_library[char_name])
                master_blueprint[base_scene_name]["is_reused"] = True
            else:
                if os.path.exists(char_image_path):
                    self.log_message(f"Generating new 3D mesh for {char_name}...", "INFO")
                    assets = self._process_single_character(char_image_path, char_name)
                    
                    self.model_library[char_name] = assets
                    master_blueprint[base_scene_name] = dict(assets)
                    master_blueprint[base_scene_name]["is_reused"] = False
                else:
                    self.log_message(f"Character image not found for {base_scene_name}", "ERROR")

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
        
        self.log_message("Batch conversion complete! Blueprint saved.", "INFO")

if __name__ == "__main__":
    converter = RgbImageTo3dMeshConverter()
    converter.execute_batch_conversion()
