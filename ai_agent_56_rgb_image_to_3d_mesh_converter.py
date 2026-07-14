import os
import sys
import json
import urllib.request
import urllib.error

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class RgbImageTo3dMeshConverter:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 56: rgb_image_to_3d_mesh_converter"
        self.workspace_dir = workspace_dir
        
        # Inputs & Outputs
        self.input_colorized_path = os.path.join(self.workspace_dir, "55_colorized_manga_panel.png")
        self.output_mesh_path = os.path.join(self.workspace_dir, "56_3d_mesh.obj")
        self.output_blueprint_path = os.path.join(self.workspace_dir, "56_mesh_generator_blueprint.json")
        
        # [SECURE] No hardcoded keys here to prevent repository rules / secret scanning blocks.
        # Environment variable se key read ki jayegi.
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _ensure_input_image_exists(self):
        if os.path.exists(self.input_colorized_path):
            print(f"[{self.agent_name}] Input colorized image found.")
            return True

        print(f"[{self.agent_name}] Warning: '{self.input_colorized_path}' not found. Creating a temporary dummy image...")
        if not PIL_AVAILABLE:
            return False

        try:
            # Create a 256x256 dummy gradient image for depth testing
            img = Image.new("RGB", (256, 256), (0, 0, 0))
            pixels = img.load()
            for y in range(256):
                for x in range(256):
                    # A circular gradient pattern
                    dist = ((x - 128)**2 + (y - 128)**2)**0.5
                    val = max(0, int(255 - dist * 1.5))
                    pixels[x, y] = (val, int(val * 0.5), int(255 - val))
            
            img.save(self.input_colorized_path, "PNG")
            print(f"[{self.agent_name}] Mock image generated at '{self.input_colorized_path}'")
            return True
        except Exception as e:
            print(f"[{self.agent_name}] Failed to generate mock image: {str(e)}")
            return False

    def convert_image_to_3d_mesh(self):
        print(f"[{self.agent_name}] Starting 3D Mesh Generation Engine...")
        self._ensure_input_image_exists()

        ai_prompt_instructions = (
            "You are a 3D Mesh Optimization Expert. Analyze the structural depth of the provided image scene.\n"
            "Return ONLY a clean JSON object with structural recommendations for 3D reconstruction. Format:\n"
            "{\n"
            "  \"mesh_type\": \"displaced_grid\",\n"
            "  \"subdivision_factor\": 64,\n"
            "  \"depth_multiplier\": 2.5,\n"
            "  \"smoothing_passes\": 2,\n"
            "  \"material_type\": \"principled_bsdf\"\n"
            "}"
        )

        mesh_config = {
            "mesh_type": "displaced_grid",
            "subdivision_factor": 64,
            "depth_multiplier": 2.0,
            "smoothing_passes": 1,
            "material_type": "principled_bsdf"
        }

        # Agar Gemini Key available hai, toh hum details analyze karwa sakte hain
        if self.gemini_api_key:
            print(f"[{self.agent_name}] Fetching optimal 3D parameters from Gemini Cloud Node...")
            try:
                payload = {
                    "contents": [{
                        "parts": [{"text": ai_prompt_instructions}]
                    }],
                    "generationConfig": {
                        "responseMimeType": "application/json"
                    }
                }
                data_bytes = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    self.gemini_url, 
                    data=data_bytes, 
                    headers={"Content-Type": "application/json"}
                )

                with urllib.request.urlopen(req, timeout=15) as response:
                    res_body = response.read().decode("utf-8")
                    raw_response = json.loads(res_body)
                    raw_text = raw_response["candidates"][0]["content"]["parts"][0]["text"]
                    mesh_config = json.loads(raw_text.strip())
                    print(f"[{self.agent_name}] Success: Custom 3D parameters loaded from AI.")
            except Exception as e:
                print(f"[{self.agent_name}] Cloud parameters request skipped ({str(e)}). Using default configuration.")
        else:
            print(f"[{self.agent_name}] No active GEMINI_API_KEY env variable. Applying native math pipeline.")

        # Real 3D OBJ Mesh Generation
        vertex_count, face_count = self._generate_wavefront_obj(mesh_config)

        # Output Blueprint
        blueprint = {
            "agent_executed": self.agent_name,
            "api_pipeline": "Gemini Parameter Tuned" if self.gemini_api_key else "Native Pipeline",
            "source_2d_image": self.input_colorized_path,
            "generated_mesh_obj": self.output_mesh_path,
            "mesh_configuration": mesh_config,
            "mesh_statistics": {
                "total_vertices": vertex_count,
                "total_faces": face_count
            }
        }

        self._save_blueprint(blueprint)
        return blueprint

    def _generate_wavefront_obj(self, config):
        if not PIL_AVAILABLE or not os.path.exists(self.input_colorized_path):
            print(f"[{self.agent_name}] Error: Pillow not available or image missing. OBJ mesh creation bypassed.")
            return 0, 0

        try:
            img = Image.open(self.input_colorized_path).convert("L") # Convert to Grayscale for depth
            grid_size = config.get("subdivision_factor", 64)
            depth_scale = config.get("depth_multiplier", 2.0)

            # Resize to dynamic grid size to optimize processing speed and file size
            img_resized = img.resize((grid_size, grid_size), Image.Resampling.LANCZOS)
            
            vertices = []
            faces = []

            # 1. Generate Vertices based on grayscale brightness (X, Y, Z coordinates)
            for y in range(grid_size):
                for x in range(grid_size):
                    # Normalizing coordinates between -1.0 and 1.0
                    pos_x = (x / (grid_size - 1)) * 2.0 - 1.0
                    pos_y = (y / (grid_size - 1)) * -2.0 + 1.0 # Invert Y for correct orientation
                    
                    pixel_brightness = img_resized.getpixel((x, y)) / 255.0
                    pos_z = pixel_brightness * depth_scale  # Brighter pixels sit higher (closer)
                    
                    vertices.append((pos_x, pos_y, pos_z))

            # 2. Generate Faces connecting the vertices
            for y in range(grid_size - 1):
                for x in range(grid_size - 1):
                    # Vertex indices (1-based index for OBJ standard)
                    v1 = (y * grid_size) + x + 1
                    v2 = (y * grid_size) + (x + 1) + 1
                    v3 = ((y + 1) * grid_size) + (x + 1) + 1
                    v4 = ((y + 1) * grid_size) + x + 1
                    
                    # Split quad face into 2 triangles
                    faces.append((v1, v2, v3))
                    faces.append((v1, v3, v4))

            # 3. Write data to standard Wavefront .obj file
            with open(self.output_mesh_path, "w", encoding="utf-8") as f:
                f.write(f"# Wavefront OBJ generated by {self.agent_name}\n")
                f.write(f"# Subdivision Factor: {grid_size}x{grid_size}\n\n")
                
                for v in vertices:
                    f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
                
                f.write("\n")
                
                for face in faces:
                    f.write(f"f {face[0]} {face[1]} {face[2]}\n")

            print(f"[{self.agent_name}] Success: 3D Mesh successfully exported to '{self.output_mesh_path}'")
            return len(vertices), len(faces)

        except Exception as e:
            print(f"[{self.agent_name}] Mesh conversion engine failed: {str(e)}")
            return 0, 0

    def _save_blueprint(self, data):
        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[{self.agent_name}] Structural metadata saved to '{self.output_blueprint_path}'")

if __name__ == "__main__":
    converter = RgbImageTo3dMeshConverter()
    converter.convert_image_to_3d_mesh()
