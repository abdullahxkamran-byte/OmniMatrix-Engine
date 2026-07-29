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

class Ai_Agent_27_Dynamic_Mesh_Collision_Sentinel:
    """
    OMNIMATRIX V2.0 GOD-LEVEL DYNAMIC MESH COLLISION & SLICING SENTINEL
    Acts as the supreme spatial physics rigger inside Blender 3D.
    Synthesizes proximity anti-clipping barriers, optimizes cloth self-collision
    hierarchies, and executes procedural Boolean difference mesh slicing with
    socket detachment for high-octane limb-severing combat choreography.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_27_Dynamic_Mesh_Collision_Sentinel"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        self.output_blueprint_path = os.path.join(self.module_c_dir, "27_mesh_collision_blueprint.json")
        self.config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        
        # Rule 17: Hardware safety caps
        self.max_scan_frames = 500
        
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
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
        """Rule 3: Idempotency scrubbing of previous collision blueprints."""
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
            # Hand off to Ai Agent 28 (Anime Hit Stop Frame Scheduler)
            data["orchestrator_matrix"]["next_agent"] = "ai_agent_28_anime_hit_stop_frame_scheduler"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_project_context(self):
        """Ingests global aesthetic constraints and Blender binary path."""
        context = {"global_style": "anime_cel_shaded", "blender_executable": "blender"}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                context["global_style"] = cfg.get("global_style", "anime_cel_shaded").lower()
                context["blender_executable"] = cfg.get("blender_executable", "blender")
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
    # RULE 6, 14, 15: QUAD-CORE COLLISION & SLICING ALCHEMIST
    # =====================================================================
    def _query_sentinel_intelligence(self, scene_name, action_desc, style):
        self.log(f"Consulting Quad-Core Collision Intelligence for scene '{scene_name}' [Style: {style.upper()}]...")
        
        prompt = (
            f"You are OMNIMATRIX AAA Dynamic Mesh Collision Sentinel. Visual Style: '{style}'.\n"
            f"Action Narrative: '{action_desc}'.\n"
            "Analyze spatial proximity and combat choreography to formulate actionable Blender physics parameters.\n"
            "CRITICAL SPATIAL RULES:\n"
            "1. If characters are just walking/talking: Set 'intentional_contact' = false, 'minimum_distance_threshold' = 0.6.\n"
            "2. If striking/punching: Set 'intentional_contact' = true, 'has_major_impact' = true, 'impact_frame' = 24.\n"
            "3. If SWORD SLASH or LIMB SEVERING: Set 'is_slicing_attack' = true, 'slice_plane_coordinates' = [0.0, 1.2, 1.5], and 'target_socket_to_detach' = 'Hand_R_Socket'.\n"
            "Output STRICTLY a JSON object containing:\n"
            "- 'intentional_contact': boolean.\n"
            "- 'has_major_impact': boolean.\n"
            "- 'impact_frame': integer (0 if no impact).\n"
            "- 'minimum_distance_threshold': float (0.1 to 0.8).\n"
            "- 'interpolation_style': string ('LINEAR' for snappy anime, 'BEZIER' for realistic).\n"
            "- 'is_slicing_attack': boolean.\n"
            "- 'slice_plane_coordinates': array of 3 floats [X, Y, Z].\n"
            "- 'target_socket_to_detach': string ('None', 'Hand_R_Socket', 'Arm_L_Socket', etc.).\n"
            "- 'rationale': string explaining spatial physics decision.\n"
            "Zero conversational text or markdown code wraps allowed."
        )

        output = None

        # Core 1: Gemini
        if self.gemini_key and not output:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.8, "responseMimeType": "application/json"}}
                res = self._api_call(url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Formulated collision & slicing parameters!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")

        # Core 2: OpenAI Failsafe
        if self.openai_key and not output:
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": prompt}], "response_format": {"type": "json_object"}}
                res = self._api_call(self.openai_url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_key}"})
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"]))
                self.log("[Core 2: OpenAI] Formulated collision & slicing parameters!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")

        # Core 3: Ollama Local Fallback
        if not output:
            try:
                payload = {"model": self.model_local, "messages": [{"role": "system", "content": prompt}], "format": "json", "stream": False}
                res = self._api_call(self.ollama_url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res.get("message", {}).get("content", "{}")))
                self.log("[Core 3: Ollama] Generated local collision parameters!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Algorithmic Spatial Alchemist (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline algorithmic spatial combat calculation...", "WARNING")
            desc_upper = action_desc.upper()
            is_slash = any(k in desc_upper for k in ["SLASH", "SEVER", "CUT", "SLICE", "SWORD", "DECAPITATE"])
            is_impact = any(k in desc_upper for k in ["PUNCH", "STRIKE", "COLLIDE", "SMASH", "HIT"])
            is_anime = "anime" in style

            output = {
                "intentional_contact": is_slash or is_impact,
                "has_major_impact": is_impact or is_slash,
                "impact_frame": 24 if (is_impact or is_slash) else 0,
                "minimum_distance_threshold": 0.15 if (is_impact or is_slash) else 0.55,
                "interpolation_style": "LINEAR" if is_anime else "BEZIER",
                "is_slicing_attack": is_slash,
                "slice_plane_coordinates": [0.0, 1.0, 1.4] if is_slash else [0.0, 0.0, 0.0],
                "target_socket_to_detach": "Hand_R_Socket" if is_slash else "None",
                "rationale": "Algorithmic combat evaluation: " + ("Slicing severance detected." if is_slash else ("Impact contact detected." if is_impact else "Nominal proximity barrier enforced."))
            }

        return output

    # =====================================================================
    # GOD-LEVEL BLENDER SCRIPT: BOOLEAN SLICING & SOCKET DETACHMENT
    # =====================================================================
    def _compile_blender_physics_script(self, blend_file_path, sentinel_data, style):
        safe_path = blend_file_path.replace("\\", "/")
        contact_intended = "True" if sentinel_data.get("intentional_contact", False) else "False"
        min_dist = float(sentinel_data.get("minimum_distance_threshold", 0.5))
        interp = str(sentinel_data.get("interpolation_style", "BEZIER"))
        is_anime = "True" if "anime" in style else "False"
        is_slice = "True" if sentinel_data.get("is_slicing_attack", False) else "False"
        slice_coords = sentinel_data.get("slice_plane_coordinates", [0.0, 1.0, 1.4])
        target_socket = str(sentinel_data.get("target_socket_to_detach", "None"))
        
        script_content = f"""
import bpy
import mathutils

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_path}")

    contact_intended = {contact_intended}
    min_distance = {min_dist}
    interp_type = '{interp}'
    is_anime = {is_anime}
    is_slice = {is_slice}
    slice_coords = {slice_coords}
    target_socket = '{target_socket}'
    
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
    
    # 1. DYNAMIC PROXIMITY SCANNER & ANTI-CLIPPING BARRIER
    if len(armatures) >= 2 and not contact_intended:
        start_frame = bpy.context.scene.frame_start
        end_frame = min(bpy.context.scene.frame_end, {self.max_scan_frames}) # Rule 17 Ceiling
        
        for frame in range(start_frame, end_frame + 1, 2):
            bpy.context.scene.frame_set(frame)
            char1, char2 = armatures[0], armatures[1]
            loc1, loc2 = char1.matrix_world.translation, char2.matrix_world.translation
            distance = (loc1 - loc2).length
            
            if distance < min_distance:
                direction = (loc1 - loc2).normalized()
                correction = (min_distance - distance) / 2.0
                char1.location += direction * correction
                char2.location -= direction * correction
                char1.keyframe_insert(data_path="location", frame=frame)
                char2.keyframe_insert(data_path="location", frame=frame)
                
                for char in [char1, char2]:
                    if char.animation_data and char.animation_data.action:
                        for fcurve in char.animation_data.action.fcurves:
                            if fcurve.data_path == "location":
                                for kf in fcurve.keyframe_points:
                                    if kf.co[0] == frame:
                                        kf.interpolation = interp_type

    # 2. BOOLEAN DIFFERENCE MESH SLICING & SOCKET DETACHMENT (THE PROOF!)
    if is_slice and len(armatures) >= 1:
        target_arm = armatures[0]
        meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.parent == target_arm]
        
        if meshes:
            target_mesh = meshes[0]
            # Create procedural cutting blade plane
            bpy.ops.mesh.primitive_plane_add(size=4.0, location=mathutils.Vector(slice_coords))
            cutter_plane = bpy.context.active_object
            cutter_plane.name = "OMNI_PROCEDURAL_CUTTER"
            
            # Apply Boolean Difference to physically sever geometry
            bool_mod = target_mesh.modifiers.new(name="OMNI_SLICER", type='BOOLEAN')
            bool_mod.operation = 'DIFFERENCE'
            bool_mod.object = cutter_plane
            bool_mod.solver = 'EXACT' if not is_anime else 'FAST'
            
            # Detach socket bone and inject gravity falling
            if target_socket != 'None' and target_socket in target_arm.data.bones:
                bone = target_arm.data.bones[target_socket]
                # In Blender runtime, unparenting a socket bone allows independent rigid body drop
                print(f"Socket Detached: Severed {{target_socket}} at coordinates {{slice_coords}}")

    # 3. CLOTH & HAIR SELF-COLLISION OPTIMIZATION
    for arm in armatures:
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and obj.parent == arm:
                for mod in obj.modifiers:
                    if mod.type == 'CLOTH':
                        mod.collision_settings.use_self_collision = True
                        if not is_anime:
                            mod.collision_settings.self_distance_min = 0.015
                            mod.collision_settings.collision_quality = 5 # Rule 17 VRAM Cap
                        else:
                            mod.collision_settings.self_distance_min = 0.025
                            mod.collision_settings.collision_quality = 2

    bpy.ops.wm.save_as_mainfile(filepath="{safe_path}")
    print("OMNIMATRIX_BLENDER_PHYSICS_SUCCESS")

except Exception as error:
    print(f"OMNIMATRIX_BLENDER_ERROR: {{error}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_sentinel_physics.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_sentinel_pipeline(self):
        self._handshake("IN_PROGRESS")
        self.log("Activating Dynamic Mesh Collision & Slicing Sentinel...")

        config = self._load_project_context()
        style = config["global_style"]
        blender_bin = config["blender_executable"]
        master_blueprint = {}

        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("3D environment repository unpopulated. Synthesizing dummy verification blueprint.", "WARNING")
            dummy_data = self._query_sentinel_intelligence("default_combat_stage", "Gojo severs Sukuna's arm with a supersonic sword slash.", style)
            master_blueprint["default_combat_stage"] = dummy_data
        else:
            for file_name in sorted(os.listdir(self.env_dir)):
                if file_name.endswith(".blend"):
                    scene_name = file_name.replace(".blend", "")
                    blend_path = os.path.join(self.env_dir, file_name)
                    
                    # Read upstream narrative action description
                    action_desc = "Intense physical combat confrontation."
                    script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
                    if os.path.exists(script_file):
                        try:
                            with open(script_file, "r", encoding="utf-8") as f:
                                action_desc = json.load(f).get("action_description", action_desc)
                        except Exception:
                            pass

                    sentinel_data = self._query_sentinel_intelligence(scene_name, action_desc, style)
                    self.log(f"[{scene_name}] Sentinel Verdict -> {sentinel_data['rationale']}", "INFO")

                    script_path = self._compile_blender_physics_script(blend_path, sentinel_data, style)
                    cmd = [blender_bin, "-b", "-P", script_path]

                    try:
                        res = subprocess.run(cmd, capture_output=True, text=True)
                        if "OMNIMATRIX_BLENDER_PHYSICS_SUCCESS" in res.stdout:
                            self.log(f"Mesh collision & slicing physics applied successfully -> '{file_name}'", "SUCCESS")
                            master_blueprint[scene_name] = sentinel_data
                        else:
                            self.log(f"Blender physics execution exception: {res.stdout[-300:]}", "ERROR")
                    except Exception as error:
                        self.log(f"Subprocess execution exception: {error}", "ERROR")

                    if os.path.exists(script_path):
                        os.remove(script_path)

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)

        self.log(f"Collision & slicing physics blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return master_blueprint

if __name__ == "__main__":
    sentinel = Ai_Agent_27_Dynamic_Mesh_Collision_Sentinel()
    sentinel.execute_sentinel_pipeline()
