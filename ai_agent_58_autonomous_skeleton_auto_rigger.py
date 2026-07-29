# ==============================================================================
# Ai_Agent_58_Autonomous_Skeleton_Auto_Rigger.py
# MODULE H: Omni Generative Matrix (Limitless Skeleton Builder)
# ==============================================================================

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

class AiAgent58AutonomousSkeletonAutoRigger:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_58_Autonomous_Skeleton_Auto_Rigger"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_root = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.module_h_dir = os.path.join(self.workspace_root, "Module_H_Generative")
        
        # Upstream Inputs
        self.vision_outputs_dir = os.path.join(self.module_h_dir, "outputs_vision_layers")
        self.meshes_dir = os.path.join(self.module_h_dir, "3d_meshes")
        self.input_blueprint_path = os.path.join(self.meshes_dir, "56_master_mesh_blueprint.json")
        
        # Outputs
        self.rig_dir = os.path.join(self.module_h_dir, "rigged_assets")
        self.output_rig_blueprint = os.path.join(self.rig_dir, "58_master_rig_blueprint.json")
        
        # System States
        self.state_file = os.path.join(self.workspace_root, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_root, "global_config.json")
        
        # API Keys
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        self._initialize_directories()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _initialize_directories(self):
        for d in [self.workspace_root, self.module_h_dir, self.rig_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    # RULE 3: IDEMPOTENCY SCRUBBING
    def scrub_workspace(self):
        self.log("Scrubbing legacy rigged models to ensure idempotency...", "INFO")
        for filename in os.listdir(self.rig_dir):
            file_path = os.path.join(self.rig_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                self.log(f"Failed to delete {file_path}. Reason: {e}", "WARNING")

    # RULE 4: LIMITLESS FLUIDITY
    def load_global_config(self):
        default_config = {
            "rigging_mode": "omni_limitless", # Omni_limitless automatically figures out anatomy
            "blender_executable": "blender"
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception:
                pass
        return default_config

    # RULE 5: BULLETPROOF JSON CLEANER
    def clean_json_response(self, raw_response):
        try:
            cleaned = re.sub(r'```(?:json)?\n(.*?)```', r'\1', raw_response, flags=re.DOTALL)
            cleaned = cleaned.strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            start = raw_response.find("{")
            end = raw_response.rfind("}")
            if start != -1 and end != -1:
                try: return json.loads(raw_response[start:end+1])
                except: pass
            return None

    def _analyze_mesh_bounds(self, mesh_path):
        """Calculates precise physical coordinates of the model."""
        default_bounds = {"min_x": -1.0, "max_x": 1.0, "min_y": -1.0, "max_y": 1.0, "min_z": 0.0, "max_z": 2.0}
        if not os.path.exists(mesh_path):
            return default_bounds

        try:
            xs, ys, zs = [], [], []
            with open(mesh_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("v "):
                        parts = line.split()
                        if len(parts) >= 4:
                            xs.append(float(parts[1]))
                            ys.append(float(parts[2]))
                            zs.append(float(parts[3]))

            if not zs:
                return default_bounds

            return {
                "min_x": min(xs), "max_x": max(xs),
                "min_y": min(ys), "max_y": max(ys),
                "min_z": min(zs), "max_z": max(zs),
                "height": abs(max(zs) - min(zs)),
                "width": abs(max(xs) - min(xs))
            }
        except Exception:
            return default_bounds

    # RULE 10: 100% OFFLINE AUTONOMY FALLBACK
    def _get_procedural_fallback_rig(self, bounds):
        """Fallback Math: A universal biped rig with core sockets if AI APIs fail."""
        self.log("Engaging Procedural Fallback Anatomy Generator...", "STATUS")
        z_min = bounds["min_z"]
        height = bounds["height"]
        root_z = z_min + (height * 0.5)
        spine_z = z_min + (height * 0.7)
        head_z = z_min + (height * 0.9)
        
        return [
            {"name": "Root", "parent": None, "head": [0, 0, z_min], "tail": [0, 0, root_z]},
            {"name": "Spine", "parent": "Root", "head": [0, 0, root_z], "tail": [0, 0, spine_z]},
            {"name": "NeckHead", "parent": "Spine", "head": [0, 0, spine_z], "tail": [0, 0, head_z]},
            {"name": "Jaw_Socket", "parent": "NeckHead", "head": [0, -0.1, head_z - 0.05], "tail": [0, -0.2, head_z - 0.1]},
            {"name": "Arm_L", "parent": "Spine", "head": [0.2, 0, spine_z], "tail": [0.8, 0, spine_z]},
            {"name": "Arm_R", "parent": "Spine", "head": [-0.2, 0, spine_z], "tail": [-0.8, 0, spine_z]},
            {"name": "Weapon_Socket_R", "parent": "Arm_R", "head": [-0.8, 0, spine_z], "tail": [-0.8, -0.2, spine_z]},
            {"name": "Leg_L", "parent": "Root", "head": [0.2, 0, root_z], "tail": [0.2, 0, z_min]},
            {"name": "Leg_R", "parent": "Root", "head": [-0.2, 0, root_z], "tail": [-0.2, 0, z_min]},
            {"name": "VFX_Core_Socket", "parent": "Spine", "head": [0, -0.1, spine_z-0.1], "tail": [0, -0.3, spine_z-0.1]}
        ]

    # RULE 6: QUAD-CORE FALLBACK MATRIX FOR LIMITLESS ANATOMY
    def _generate_omni_bone_hierarchy(self, char_name, vision_data, bounds):
        """
        THE LIMITLESS CORE: Instructs the AI to invent bones for ANY anatomy.
        4 Arms? Holes in stomach? Eye on hand? It will create sockets for them.
        """
        bg_desc = vision_data.get("environment_description", "")
        pose_intent = vision_data.get("pose_intent", "")
        
        ai_prompt = f"""
        You are an Expert Limitless 3D Rigger. You are rigging: {char_name}.
        Visual Context: {bg_desc} | Animation Intent: {pose_intent}
        Mesh Bounds: X[{bounds['min_x']:.2f} to {bounds['max_x']:.2f}], Y[{bounds['min_y']:.2f} to {bounds['max_y']:.2f}], Z[{bounds['min_z']:.2f} to {bounds['max_z']:.2f}].
        
        CRITICAL RULES:
        1. NO LIMITS ON ANATOMY: If the character has 4 arms, create Arm_L1, Arm_L2, etc. If it has a tail, create Tail_1, Tail_2.
        2. VFX SOCKETS: You MUST add specialized "_Socket" bones for unique features. 
           - E.g., if there's a hole in the stomach, create "Stomach_Hole_Socket". 
           - If there's an eye on the hand, create "Hand_Eye_Socket".
        3. All coordinates [x, y, z] MUST stay within the Mesh Bounds.
        
        Return ONLY valid JSON. Format:
        {{
          "bones": [
            {{"name": "Root", "parent": null, "head": [0.0, 0.0, 0.0], "tail": [0.0, 0.0, 0.5]}},
            {{"name": "Spine", "parent": "Root", "head": [0.0, 0.0, 0.5], "tail": [0.0, 0.0, 1.0]}},
            {{"name": "Extra_Arm_L", "parent": "Spine", "head": [0.1, 0, 0.8], "tail": [0.5, 0, 0.8]}}
          ]
        }}
        """

        # Core 1: Gemini
        if self.gemini_api_key:
            try:
                self.log(f"Executing Core 1 (Gemini) for Omni-Anatomy generation...", "INFO")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self.clean_json_response(res_text)
                    if parsed and "bones" in parsed: return parsed["bones"]
            except Exception as e:
                self.log(f"Core 1 Failed: {e}", "WARNING")

        # Core 2: OpenAI
        if self.openai_api_key:
            try:
                self.log("Executing Core 2 (OpenAI) for Omni-Anatomy generation...", "INFO")
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")}
                payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": ai_prompt}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
                    parsed = self.clean_json_response(res_text)
                    if parsed and "bones" in parsed: return parsed["bones"]
            except Exception as e:
                self.log(f"Core 2 Failed: {e}", "WARNING")

        # Core 3: Ollama Local
        try:
            self.log("Executing Core 3 (Ollama Local) for Omni-Anatomy...", "INFO")
            url = "http://127.0.0.1:11434/api/generate"
            payload = {"model": "llama3", "prompt": ai_prompt, "stream": False}
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
            with urllib.request.urlopen(req, timeout=20) as response:
                res_text = json.loads(response.read().decode("utf-8"))["response"]
                parsed = self.clean_json_response(res_text)
                if parsed and "bones" in parsed: return parsed["bones"]
        except Exception as e:
            self.log(f"Core 3 Failed: {e}", "WARNING")

        # Core 4: Procedural Math Fallback
        return self._get_procedural_fallback_rig(bounds)

    # RULE 9: ACTIONABLE ABSTRACTION
    def _generate_blender_rig_script(self, mesh_path, fbx_out_path, bone_data):
        safe_mesh_path = mesh_path.replace("\\", "/")
        safe_fbx_path = fbx_out_path.replace("\\", "/")
        safe_blend_path = safe_fbx_path.replace(".fbx", ".blend") 
        
        bones_json = json.dumps(bone_data)

        # Uses Advanced Envelope Weights for Omni-mesh flexibility
        blender_script = f"""
import bpy
import json
import sys

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

try:
    clear_scene()

    # 1. Import Mesh
    mesh_path = "{safe_mesh_path}"
    try: bpy.ops.wm.obj_import(filepath=mesh_path)
    except AttributeError: bpy.ops.import_scene.obj(filepath=mesh_path)

    mesh_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            mesh_obj = obj
            break

    if not mesh_obj:
        raise ValueError("No mesh found after import.")

    # 2. Build Omni-Skeleton
    bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
    armature_obj = bpy.context.active_object
    armature_obj.name = "Omni_Limitless_Rig"
    armature = armature_obj.data
    
    for bone in armature.edit_bones:
        armature.edit_bones.remove(bone)

    bone_data = json.loads('''{bones_json}''')
    edit_bones_dict = {{}}

    # Create all bones (including VFX sockets)
    for b_info in bone_data:
        b_name = b_info.get("name", "Bone")
        eb = armature.edit_bones.new(b_name)
        eb.head = b_info.get("head", (0, 0, 0))
        eb.tail = b_info.get("tail", (0, 0, 1))
        # Unique sockets shouldn't deform the mesh, just act as attach points
        if "_Socket" in b_name:
            eb.use_deform = False 
        edit_bones_dict[b_name] = eb

    # Setup Parent Hierarchy
    for b_info in bone_data:
        parent_name = b_info.get("parent")
        if parent_name and parent_name in edit_bones_dict:
            child_bone = edit_bones_dict[b_info["name"]]
            child_bone.parent = edit_bones_dict[parent_name]
            child_bone.use_connect = False

    bpy.ops.object.mode_set(mode='OBJECT')

    # 3. Smart Binding (Bone Envelopes for irregular Omni-anatomy)
    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    armature_obj.select_set(True)
    bpy.context.view_layer.objects.active = armature_obj

    bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')

    # 4. Export FBX & Blend
    bpy.ops.export_scene.fbx(
        filepath="{safe_fbx_path}",
        use_selection=False,
        apply_unit_scale=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
        armature_nodetype='NULL'
    )
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    
    print("OMNIMATRIX_BLENDER_SUCCESS")
except Exception as e:
    print(f"OMNIMATRIX_BLENDER_ERROR: {{str(e)}}")
    sys.exit(1)
"""
        script_path = os.path.join(self.module_h_dir, "temp_rig_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(blender_script)
        return script_path

    def execute_batch_rigging(self):
        self.log("System Initializing...", "INFO")
        
        # RULE 7: ATOMIC HANDSHAKE
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
        blender_executable = config.get("blender_executable", "blender")
        
        if not os.path.exists(self.input_blueprint_path):
            self.log("Agent 56 Blueprint missing. Cannot proceed.", "FATAL")
            sys.exit(1)

        with open(self.input_blueprint_path, "r", encoding="utf-8") as f:
            master_mesh_blueprint = json.load(f)

        master_rig_blueprint = {}

        for scene_name, mesh_data in master_mesh_blueprint.items():
            obj_path = mesh_data.get("mesh", "")
            if not obj_path or not os.path.exists(obj_path):
                continue

            vision_json_path = os.path.join(self.vision_outputs_dir, f"{scene_name}_blueprint.json")
            char_name = f"Char_{scene_name}"
            vision_data = {}
            
            if os.path.exists(vision_json_path):
                with open(vision_json_path, "r", encoding="utf-8") as vf:
                    vision_data = json.load(vf)

            # Check if this scene has a character to rig
            if not vision_data.get("layers", {}).get("char_layer", ""):
                self.log(f"Skipping rigging for {scene_name} (No character detected/Environment Only).", "INFO")
                continue

            self.log(f"--- Omni-Rigging Sequence: {char_name} ---", "INFO")

            fbx_out_path = os.path.join(self.rig_dir, f"{char_name}_omni_rig.fbx")

            # 1. Math Analysis
            bounds = self._analyze_mesh_bounds(obj_path)
            
            # 2. AI Limitless Hierarchy Generation
            bone_data = self._generate_omni_bone_hierarchy(char_name, vision_data, bounds)
            
            # 3. Actionable Script
            script_path = self._generate_blender_rig_script(obj_path, fbx_out_path, bone_data)

            self.log(f"Binding Omni-Skeleton to {char_name} via Headless Blender...", "INFO")
            command = [blender_executable, "-b", "-P", script_path]
            
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout and os.path.exists(fbx_out_path):
                    self.log(f"Exported successfully: {char_name}_omni_rig.fbx", "SUCCESS")
                    
                    master_rig_blueprint[scene_name] = {
                        "rigged_fbx": fbx_out_path,
                        "rigged_blend": fbx_out_path.replace(".fbx", ".blend"),
                        "bone_count": len(bone_data),
                        "material": mesh_data.get("material", ""),
                        "texture": mesh_data.get("texture", "")
                    }
                else:
                    self.log(f"Blender failed. Log: {result.stdout[-300:]}", "ERROR")
            except Exception as e:
                self.log(f"Subprocess failed. Is Blender in system PATH? {str(e)}", "CRITICAL")
            
            if os.path.exists(script_path):
                os.remove(script_path)

        with open(self.output_rig_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_rig_blueprint, f, indent=4)

        # RULE 7: ATOMIC HANDSHAKE (Advance State)
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "Ai_Agent_59_Generative_Motion_Puppeteer_Animator"
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)

        self.log(f"Limitless Auto-Rigging Complete! Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    rigger = AiAgent58AutonomousSkeletonAutoRigger()
    rigger.execute_batch_rigging()

# ==============================================================================
# END OF FILE
# ==============================================================================
