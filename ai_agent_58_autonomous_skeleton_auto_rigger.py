import os
import sys
import json
import urllib.request
import urllib.error

class AutonomousSkeletonAutoRigger:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 58: autonomous_skeleton_auto_rigger"
        self.workspace_dir = workspace_dir
        
        # Upstream Inputs
        self.input_mesh_path = os.path.join(self.workspace_dir, "56_3d_mesh.obj")
        
        # Outputs
        self.output_rig_blueprint = os.path.join(self.workspace_dir, "58_rig_blueprint.json")
        self.output_blender_rig_script = os.path.join(self.workspace_dir, "58_blender_rig.py")
        
        # [SECURE] No hardcoded secrets. Environment variable fallback.
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _analyze_mesh_bounds(self):
        # Mesh (.obj) read karke bounding box check karna taaki bones height aur center adjust ho sakein
        default_bounds = {"min_z": -1.0, "max_z": 1.0, "center_x": 0.0, "center_y": 0.0, "height": 2.0}
        if not os.path.exists(self.input_mesh_path):
            print(f"[{self.agent_name}] Warning: No 3D mesh found. Rigging based on default character proportions.")
            return default_bounds

        try:
            z_coords = []
            x_coords = []
            y_coords = []
            with open(self.input_mesh_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("v "):
                        parts = line.split()
                        x_coords.append(float(parts[1]))
                        y_coords.append(float(parts[2]))
                        z_coords.append(float(parts[3]))

            if not z_coords:
                return default_bounds

            min_z, max_z = min(z_coords), max(z_coords)
            return {
                "min_z": min_z,
                "max_z": max_z,
                "center_x": sum(x_coords) / len(x_coords),
                "center_y": sum(y_coords) / len(y_coords),
                "height": abs(max_z - min_z)
            }
        except Exception as e:
            print(f"[{self.agent_name}] Error parsing mesh dimensions: {str(e)}")
            return default_bounds

    def generate_rig(self):
        print(f"[{self.agent_name}] Analyzing 3D character proportions for dynamic auto-rigging...")
        bounds = self._analyze_mesh_bounds()

        ai_prompt_instructions = (
            "You are a 3D Rigging and Armature Specialist for game engines and VFX.\n"
            f"Character physical bounds: Height: {bounds['height']:.2f}, Z-Range: [{bounds['min_z']:.2f} to {bounds['max_z']:.2f}].\n"
            "Calculate optimized bone coordinate joints (Root, Spine, Neck, Head, Left_Arm, Right_Arm) in JSON format.\n"
            "Return ONLY a valid JSON object without any markdown wrapping, code blocks, or backticks. Format:\n"
            "{\n"
            "  \"bone_joints\": {\n"
            "    \"Root\": [0.0, 0.0, 0.0],\n"
            "    \"Spine\": [0.0, 0.0, 0.8],\n"
            "    \"Neck\": [0.0, 0.0, 1.4],\n"
            "    \"Head\": [0.0, 0.0, 1.7],\n"
            "    \"Left_Arm_End\": [-0.8, 0.0, 1.2],\n"
            "    \"Right_Arm_End\": [0.8, 0.0, 1.2]\n"
            "  }\n"
            "}"
        )

        bone_joints = None

        if self.gemini_api_key:
            print(f"[{self.agent_name}] Consulting Gemini AI for proportional anatomical bone scaling...")
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
                    bone_joints = json.loads(raw_text.strip()).get("bone_joints", {})
                    print(f"[{self.agent_name}] Success: AI-driven anatomical joints created successfully.")
            except Exception as e:
                print(f"[{self.agent_name}] Cloud rig setup bypassed ({str(e)}). Building procedural skeletal structure...")
                bone_joints = self._get_procedural_joints(bounds)
        else:
            print(f"[{self.agent_name}] Running offline. Executing native mathematical rigging math...")
            bone_joints = self._get_procedural_joints(bounds)

        # Build Blueprint
        rig_blueprint = {
            "agent_executed": self.agent_name,
            "proportions_analyzed": bounds,
            "joints_mapping": bone_joints
