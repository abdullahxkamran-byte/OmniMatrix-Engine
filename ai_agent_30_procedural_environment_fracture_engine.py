import os
import re
import sys
import json
import time
import shutil
import platform
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

# =====================================================================
# RULE 2 & 14: UNIVERSAL ENVIRONMENT & DUAL API CONFIGURATION
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

class Ai_Agent_30_Procedural_Environment_Fracture_Engine:
    """
    OMNIMATRIX V2.0 GOD-LEVEL PROCEDURAL ENVIRONMENT FRACTURE ENGINE
    Acts as the supreme destruction Technical Director (TD) inside Blender 3D.
    Automates Cell Fracture voronoi tessellation, rigid body kinematic state
    transitions, explosive point force fields, and dynamic anti-gravity
    F-curve manipulations to deliver AAA cinematic structural destruction.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_30_Procedural_Environment_Fracture_Engine"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint_path = os.path.join(self.module_c_dir, "30_destruction_blueprint.json")
        self.collision_file = os.path.join(self.module_c_dir, "27_mesh_collision_blueprint.json")
        self.config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        
        # Rule 17: Hardware safety caps
        self.max_shatter_chunks = 65
        self.max_explosion_power = 10000.0
        
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"

        for directory in [self.workspace_dir, self.script_dir, self.env_dir, self.module_c_dir]:
            os.makedirs(directory, exist_ok=True)
            
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        formatted = f"[{level}] [{self.agent_name}] {message}"
        print(formatted)

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous destruction blueprints."""
        if os.path.exists(self.output_blueprint_path):
            try:
                os.remove(self.output_blueprint_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy blueprint {self.output_blueprint_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & PIPELINE ROUTING
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS"):
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
        
        if status == "COMPLETED":
            # Hand off to Ai Agent 31 (Camera Space Debris Instancer)
            data["orchestrator_matrix"]["next_agent"] = "ai_agent_31_camera_space_debris_instancer"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_project_context_and_collisions(self, scene_name):
        """Ingests upstream collision impact vectors and style parameters."""
        context = {
            "global_style": "anime_cel_shaded",
            "blender_executable": "blender",
            "has_heavy_impact": False,
            "impact_frame": 0,
            "impact_force": 0.0,
            "impact_point_xyz": [0.0, 0.0, 0.0]
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                context["global_style"] = cfg.get("global_style", "anime_cel_shaded").lower()
                context["blender_executable"] = cfg.get("blender_executable", "blender")
            except Exception:
                pass

        if os.path.exists(self.collision_file):
            try:
                with open(self.collision_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        scene_data = data[scene_name]
                        context["has_heavy_impact"] = scene_data.get("has_major_impact", False)
                        context["impact_frame"] = int(scene_data.get("impact_frame", 0))
                        
                        dist = float(scene_data.get("minimum_distance_threshold", 0.5))
                        context["impact_force"] = 120.0 if dist < 0.2 else 45.0
                        context["impact_point_xyz"] = scene_data.get("slice_plane_coordinates", [0.0, 0.0, 0.0])
            except Exception:
                pass
                
        return context

    def _clean_json(self, raw_text):
        """Rule 5: Bulletproof JSON scrubber."""
        cleaned = re.sub(r"^```(json)?\s*|\s*```$", "", raw_text.strip(), flags=re.IGNORECASE)
        start_index = cleaned.find('{')
        end_index = cleaned.rfind('}')
        if start_index != -1 and end_index != -1:
            return cleaned[start_index:end_index + 1]
        return cleaned

    def _api_call(self, url, payload, headers):
        request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14, 15: QUAD-CORE DESTRUCTION ALCHEMIST
    # =====================================================================
    def _query_destruction_intelligence(self, scene_name, context):
        style = context["global_style"]
        if not context["has_heavy_impact"]:
            return {
                "impact_frame": 0, "shatter_chunk_count": 0, "physics_behavior": "none",
                "fracture_center_xyz": [0.0, 0.0, 0.0], "debris_mass_kg": 0.0, "explosion_strength": 0.0,
                "rationale": "No heavy impact collision detected. Preserving environmental structural integrity."
            }

        self.log(f"Consulting Quad-Core Destruction Intelligence for scene '{scene_name}' [Style: {style.upper()}]...")
        
        prompt = (
            f"You are OMNIMATRIX AAA Procedural Destruction Technical Director. Style: '{style}'.\n"
            f"Impact event mapped at Frame {context['impact_frame']} with force {context['impact_force']}.\n"
            "Formulate Cell Fracture and Rigid Body physics parameters to execute structural destruction.\n"
            "CRITICAL DESTRUCTION RULES:\n"
            "1. If ANIME: Enforce 'anti_gravity_float' physics behavior, extreme 'explosion_strength' (5000.0 to 9000.0), lighter 'debris_mass_kg' (2.0 to 6.0), and moderate 'shatter_chunk_count' (25 to 40) for stylized clean silhouettes.\n"
            "2. If REALISTIC: Enforce 'heavy_gravity_crumble' behavior, moderate explosion (1500.0 to 3500.0), heavy mass (25.0 to 50.0), and dense chunk counts (45 to 65).\n"
            "Output STRICTLY a JSON object containing:\n"
            f"- 'impact_frame': integer ({context['impact_frame']}).\n"
            "- 'shatter_chunk_count': integer (10 to 65).\n"
            "- 'physics_behavior': string ('anti_gravity_float' or 'heavy_gravity_crumble').\n"
            f"- 'fracture_center_xyz': array of 3 floats ({context['impact_point_xyz']}).\n"
            "- 'debris_mass_kg': float (1.0 to 50.0).\n"
            "- 'explosion_strength': float (500.0 to 10000.0).\n"
            "- 'rationale': string explaining destruction physics decision.\n"
            "Zero conversational text or markdown code wraps allowed."
        )

        output = None

        # Core 1: Gemini
        if self.gemini_key and not output:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.85, "responseMimeType": "application/json"}}
                res = self._api_call(url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Formulated procedural destruction matrix!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")

        # Core 2: OpenAI Failsafe
        if self.openai_key and not output:
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": prompt}], "response_format": {"type": "json_object"}}
                res = self._api_call(self.openai_url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"})
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"]))
                self.log("[Core 2: OpenAI] Formulated procedural destruction matrix!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")

        # Core 3: Ollama Local Fallback
        if not output:
            try:
                payload = {"model": self.model_local, "messages": [{"role": "system", "content": prompt}], "format": "json", "stream": False}
                res = self._api_call(self.ollama_url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res.get("message", {}).get("content", "{}")))
                self.log("[Core 3: Ollama] Generated local destruction matrix!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Algorithmic Fracture Alchemist (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline algorithmic environmental destruction calculation...", "WARNING")
            is_anime = "anime" in style
            output = {
                "impact_frame": context["impact_frame"],
                "shatter_chunk_count": 35 if is_anime else 55,
                "physics_behavior": "anti_gravity_float" if is_anime else "heavy_gravity_crumble",
                "fracture_center_xyz": context["impact_point_xyz"],
                "debris_mass_kg": 4.5 if is_anime else 30.0,
                "explosion_strength": 6500.0 if is_anime else 2200.0,
                "rationale": "Algorithmic destruction evaluation: " + ("Anti-gravity floating rubble enforced." if is_anime else "Heavy gravitational crumbling enforced.")
            }

        # Rule 17 Safeguard: Bound maximum cell fracture chunk counts and explosive forces
        try:
            if int(output.get("shatter_chunk_count", 0)) > self.max_shatter_chunks:
                self.log(f"Safeguard Triggered: Capping shatter chunks from {output['shatter_chunk_count']} down to {self.max_shatter_chunks} to prevent VRAM overflow!", "WARNING")
                output["shatter_chunk_count"] = self.max_shatter_chunks
            if float(output.get("explosion_strength", 0.0)) > self.max_explosion_power:
                output["explosion_strength"] = self.max_explosion_power
            output["fracture_center_xyz"] = context["impact_point_xyz"]
        except Exception:
            pass

        return output

    # =====================================================================
    # GOD-LEVEL BLENDER SCRIPT: CELL FRACTURE & GRAVITY MANIPULATION
    # =====================================================================
    def _compile_blender_destruction_script(self, blend_file_path, dest_data, style):
        safe_path = blend_file_path.replace("\\", "/")
        chunks = int(dest_data.get("shatter_chunk_count", 0))
        frame = int(dest_data.get("impact_frame", 0))
        behavior = str(dest_data.get("physics_behavior", "none"))
        mass = float(dest_data.get("debris_mass_kg", 1.0))
        explosion_power = float(dest_data.get("explosion_strength", 0.0))
        impact_xyz = dest_data.get("fracture_center_xyz", [0.0, 0.0, 0.0])
        
        script_content = f"""
import bpy
import addon_utils

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_path}")

    chunks = {chunks}
    frame = {frame}
    behavior = "{behavior}"
    mass = {mass}
    explosion_power = {explosion_power}
    impact_xyz = {impact_xyz}

    if chunks > 0 and frame > 0:
        # 1. Safely enable Cell Fracture Addon
        if not addon_utils.check("object_fracture_cell")[0]:
            addon_utils.enable("object_fracture_cell")
            
        if not bpy.context.scene.rigidbody_world:
            bpy.ops.rigidbody.world_add()

        # 2. TARGET IDENTIFICATION (Locate floor, ground, or masonry walls)
        env_meshes = [
            obj for obj in bpy.context.scene.objects 
            if obj.type == 'MESH' 
            and not (obj.name.startswith("OMNI_CHAR") or "cell" in obj.name.lower())
            and any(k in obj.name.lower() for k in ["floor", "ground", "wall", "pillar", "monolith", "road"])
        ]
        
        if not env_meshes:
            env_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and not obj.parent and not obj.name.startswith("OMNI_")]

        if env_meshes:
            target_obj = env_meshes[0]
            bpy.context.view_layer.objects.active = target_obj
            target_obj.select_set(True)
            
            # 3. EXECUTE CELL FRACTURE TESSELLATION (Bounded by Rule 17)
            bpy.ops.object.add_fracture_cell_objects(source_limit=chunks, use_materials=True)
            target_obj.hide_render = True
            target_obj.hide_viewport = True
            
            # 4. RIGID BODY KINEMATIC STATE TRANSITION (THE PROOF!)
            bpy.ops.object.select_all(action='DESELECT')
            fractured_chunks = [obj for obj in bpy.context.scene.objects if target_obj.name + "_cell" in obj.name]
            
            for chunk in fractured_chunks:
                chunk.select_set(True)
                bpy.context.view_layer.objects.active = chunk
                
                if not chunk.rigid_body:
                    bpy.ops.rigidbody.object_add()
                
                chunk.rigid_body.mass = mass
                chunk.rigid_body.type = 'ACTIVE'
                chunk.rigid_body.collision_shape = 'CONVEX_HULL'
                chunk.rigid_body.kinematic = True # Locked prior to impact
                
                # Release physics EXACTLY on impact frame
                chunk.rigid_body.keyframe_insert(data_path="kinematic", frame=max(1, frame - 1))
                chunk.rigid_body.kinematic = False
                chunk.rigid_body.keyframe_insert(data_path="kinematic", frame=frame)
                
            # 5. INVISIBLE POINT FORCE FIELD IMPULSE
            bpy.ops.object.effector_add(type='FORCE', location=tuple(impact_xyz))
            bomb = bpy.context.active_object
            bomb.name = "OMNI_IMPACT_BOMB"
            bomb.field.shape = 'POINT'
            bomb.field.strength = 0.0
            
            bomb.field.keyframe_insert(data_path="strength", frame=max(1, frame - 1))
            bomb.field.strength = explosion_power
            bomb.field.keyframe_insert(data_path="strength", frame=frame)
            bomb.field.strength = 0.0
            bomb.field.keyframe_insert(data_path="strength", frame=frame + 2)
                
            # 6. SAKUGA ANTI-GRAVITY MANIPULATION (ANIME FLOAT PROOF!)
            scene = bpy.context.scene
            if behavior == "anti_gravity_float":
                scene.use_gravity = True
                scene.gravity[2] = -9.81
                scene.keyframe_insert(data_path="gravity", index=2, frame=max(1, frame - 1))
                
                # Zero-G upward float during sakuga freeze
                scene.gravity[2] = 2.5
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame)
                
                # Heavy slam back down to earth
                scene.gravity[2] = 2.5
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame + 28)
                scene.gravity[2] = -24.0
                scene.keyframe_insert(data_path="gravity", index=2, frame=frame + 34)

    bpy.ops.wm.save_as_mainfile(filepath="{safe_path}")
    print("OMNIMATRIX_BLENDER_DESTRUCTION_SUCCESS")

except Exception as error:
    print(f"OMNIMATRIX_BLENDER_ERROR: {{error}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_destruction_physics.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_destruction_pipeline(self):
        self._handshake("IN_PROGRESS")
        self.log("Activating Procedural Environment Fracture Engine...")

        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("3D environment repository unpopulated. Synthesizing dummy destruction verification blueprint.", "WARNING")
            dummy_ctx = {"global_style": "anime_cel_shaded", "blender_executable": "blender", "has_heavy_impact": True, "impact_frame": 24, "impact_force": 120.0, "impact_point_xyz": [0.0, 0.0, 0.0]}
            dummy_data = self._query_destruction_intelligence("default_combat_stage", dummy_ctx)
            master_blueprint = {"default_combat_stage": dummy_data}
        else:
            master_blueprint = {}
            for file_name in sorted(os.listdir(self.env_dir)):
                if file_name.endswith(".blend"):
                    scene_name = file_name.replace(".blend", "")
                    blend_path = os.path.join(self.env_dir, file_name)
                    
                    context = self._load_project_context_and_collisions(scene_name)
                    
                    if context["has_heavy_impact"]:
                        self.log(f"[{scene_name}] Heavy impact mapped at Frame {context['impact_frame']}. Executing Voronoi fracture protocol...", "INFO")
                        dest_data = self._query_destruction_intelligence(scene_name, context)
     
self.log(f"[{scene_name}] Fracture Verdict -> {dest_data['rationale']} (Chunks: {dest_data['shatter_chunk_count']} | Force: {dest_data['explosion_strength']})", "INFO")
                        
                        script_path = self._compile_blender_destruction_script(blend_path, dest_data, context["global_style"])
                        cmd = [context["blender_executable"], "-b", "-P", script_path]

                        try:
                            res = subprocess.run(cmd, capture_output=True, text=True)
                            if "OMNIMATRIX_BLENDER_DESTRUCTION_SUCCESS" in res.stdout:
                                self.log(f"God-level destruction physics baked successfully -> '{file_name}'", "SUCCESS")
                                master_blueprint[scene_name] = dest_data
                            else:
                                self.log(f"Blender destruction execution exception: {res.stdout[-300:]}", "ERROR")
                        except Exception as error:
                            self.log(f"Subprocess execution exception: {error}", "ERROR")

                        if os.path.exists(script_path):
                            os.remove(script_path)
                    else:
                        self.log(f"[{scene_name}] No heavy impacts detected. Preserving environmental structural integrity.", "INFO")
                        master_blueprint[scene_name] = self._query_destruction_intelligence(scene_name, context)

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)

        self.log(f"Destruction physics blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return master_blueprint

if __name__ == "__main__":
    engine = Ai_Agent_30_Procedural_Environment_Fracture_Engine()
    engine.execute_destruction_pipeline()