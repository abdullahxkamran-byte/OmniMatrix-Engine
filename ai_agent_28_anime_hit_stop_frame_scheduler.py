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

class Ai_Agent_28_Anime_Hit_Stop_Frame_Scheduler:
    """
    OMNIMATRIX V2.0 GOD-LEVEL ANIME HIT-STOP & TEMPORAL SCHEDULER
    Acts as the master time manipulator inside Blender 3D.
    Synthesizes MAPPA and Ufotable style hit-stop frame freezes, procedural
    F-curve time shifts, violent camera impact judder, and optical punch-in
    zooms to deliver immense kinetic weight upon combat collision events.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_28_Anime_Hit_Stop_Frame_Scheduler"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint_path = os.path.join(self.module_c_dir, "28_time_remap_blueprint.json")
        self.collision_file = os.path.join(self.module_c_dir, "27_mesh_collision_blueprint.json")
        self.config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        
        # Rule 17: Hardware safety caps
        self.max_freeze_frames = 12
        self.max_shake_amplitude = 40.0
        
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
        """Rule 3: Idempotency scrubbing of previous temporal blueprints."""
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
            # Hand off to Ai Agent 29 (Dynamic Smear Frame Generator)
            data["orchestrator_matrix"]["next_agent"] = "ai_agent_29_dynamic_smear_frame_generator"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_project_context_and_collisions(self, scene_name):
        """Ingests upstream collision coordinates and style parameters."""
        context = {
            "global_style": "anime_cel_shaded",
            "blender_executable": "blender",
            "action_description": "Nominal scene interaction.",
            "impact_frame": 0,
            "has_major_impact": False
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                context["global_style"] = cfg.get("global_style", "anime_cel_shaded").lower()
                context["blender_executable"] = cfg.get("blender_executable", "blender")
            except Exception:
                pass

        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    context["action_description"] = data.get("action_description", context["action_description"])
            except Exception:
                pass

        if os.path.exists(self.collision_file):
            try:
                with open(self.collision_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if scene_name in data:
                        scene_data = data[scene_name]
                        context["has_major_impact"] = scene_data.get("has_major_impact", scene_data.get("intentional_contact", False))
                        context["impact_frame"] = int(scene_data.get("impact_frame", 24))
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
    # RULE 6, 14, 15: QUAD-CORE TEMPORAL ALCHEMIST
    # =====================================================================
    def _query_temporal_intelligence(self, scene_name, context):
        style = context["global_style"]
        if not context["has_major_impact"]:
            return {
                "impact_frame": 0, "freeze_duration_frames": 0, "time_scale_factor": 1.0,
                "camera_zoom_amplitude": 0.0, "camera_shake_strength": 0.0,
                "rationale": "No impact collision detected. Maintaining continuous linear timeline."
            }

        self.log(f"Consulting Quad-Core Temporal Intelligence for scene '{scene_name}' [Style: {style.upper()}]...")
        
        prompt = (
            f"You are OMNIMATRIX AAA Action Editor and Keyframe Conductor. Style: '{style}'.\n"
            f"Scene Narrative: '{context['action_description']}'. Impact event mapped at Frame {context['impact_frame']}.\n"
            "Formulate temporal manipulation parameters to deliver bone-crushing combat weight.\n"
            "CRITICAL TEMPORAL RULES:\n"
            "1. If ANIME: Enforce Sakuga 'hit-stop'. Set 'freeze_duration_frames' between 6 and 12, extreme 'camera_shake_strength' (20.0 to 40.0), and aggressive 'camera_zoom_amplitude' (1.2 to 2.5).\n"
            "2. If REALISTIC: Enforce cinematic slow-motion. Set 'freeze_duration_frames' = 0, 'time_scale_factor' (0.2 to 0.4), moderate shake (5.0 to 15.0), and subtle optical zoom (0.3 to 0.6).\n"
            "Output STRICTLY a JSON object containing:\n"
            f"- 'impact_frame': integer ({context['impact_frame']}).\n"
            "- 'freeze_duration_frames': integer (0 to 12).\n"
            "- 'time_scale_factor': float (0.1 to 1.0).\n"
            "- 'camera_zoom_amplitude': float (0.0 to 3.0).\n"
            "- 'camera_shake_strength': float (0.0 to 40.0).\n"
            "- 'rationale': string explaining temporal editing decision.\n"
            "Zero conversational text or markdown code wraps allowed."
        )

        output = None

        # Core 1: Gemini
        if self.gemini_key and not output:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.82, "responseMimeType": "application/json"}}
                res = self._api_call(url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Formulated temporal hit-stop matrix!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")

        # Core 2: OpenAI Failsafe
        if self.openai_key and not output:
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": prompt}], "response_format": {"type": "json_object"}}
                res = self._api_call(self.openai_url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"})
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"]))
                self.log("[Core 2: OpenAI] Formulated temporal hit-stop matrix!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")

        # Core 3: Ollama Local Fallback
        if not output:
            try:
                payload = {"model": self.model_local, "messages": [{"role": "system", "content": prompt}], "format": "json", "stream": False}
                res = self._api_call(self.ollama_url, payload, {"Content-Type": "application/json"})
                output = json.loads(self._clean_json(res.get("message", {}).get("content", "{}")))
                self.log("[Core 3: Ollama] Generated local temporal matrix!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Algorithmic Temporal Alchemist (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline algorithmic temporal combat calculation...", "WARNING")
            is_anime = "anime" in style
            output = {
                "impact_frame": context["impact_frame"],
                "freeze_duration_frames": 8 if is_anime else 0,
                "time_scale_factor": 1.0 if is_anime else 0.25,
                "camera_zoom_amplitude": 1.8 if is_anime else 0.45,
                "camera_shake_strength": 32.0 if is_anime else 12.0,
                "rationale": "Algorithmic temporal evaluation: " + ("Sakuga hit-stop freeze enforced." if is_anime else "Cinematic optical time dilation enforced.")
            }

        # Rule 17 Safeguard: Bound maximum freeze and shake parameters
        try:
            if int(output.get("freeze_duration_frames", 0)) > self.max_freeze_frames:
                self.log(f"Safeguard Triggered: Capping freeze from {output['freeze_duration_frames']} to {self.max_freeze_frames} frames to prevent timeline lockup!", "WARNING")
                output["freeze_duration_frames"] = self.max_freeze_frames
            if float(output.get("camera_shake_strength", 0.0)) > self.max_shake_amplitude:
                output["camera_shake_strength"] = self.max_shake_amplitude
        except Exception:
            pass

        return output

    # =====================================================================
    # GOD-LEVEL BLENDER SCRIPT: F-CURVE SHIFTING & TEMPORAL RAMPING
    # =====================================================================
    def _compile_blender_temporal_script(self, blend_file_path, time_data, style):
        safe_path = blend_file_path.replace("\\", "/")
        is_anime = "True" if "anime" in style else "False"
        impact_frame = int(time_data.get("impact_frame", 0))
        freeze_frames = int(time_data.get("freeze_duration_frames", 0))
        time_scale = float(time_data.get("time_scale_factor", 1.0))
        zoom_amp = float(time_data.get("camera_zoom_amplitude", 0.0))
        shake_str = float(time_data.get("camera_shake_strength", 0.0))
        
        script_content = f"""
import bpy

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_path}")

    impact_frame = {impact_frame}
    freeze_frames = {freeze_frames}
    time_scale = {time_scale}
    zoom_amp = {zoom_amp}
    shake_str = {shake_str}
    is_anime = {is_anime}

    if impact_frame > 0:
        # --- 1. TRUE ANIME SAKUGA HIT-STOP (F-CURVE TIME SHIFT) ---
        if is_anime and freeze_frames > 0:
            print("EXECUTING SAKUGA HIT-STOP: Shifting world F-curves while preserving camera judder...")
            for obj in bpy.context.scene.objects:
                if obj.animation_data and obj.animation_data.action:
                    for fcurve in obj.animation_data.action.fcurves:
                        # Skip camera location curves so camera shake remains active during the world pause!
                        if obj.type == 'CAMERA' and fcurve.data_path == 'location':
                            continue
                            
                        # Shift all keyframes AFTER the impact point to create a true physical hold
                        for kf in fcurve.keyframe_points:
                            if kf.co[0] > impact_frame:
                                kf.co[0] += freeze_frames
                                kf.handle_left[0] += freeze_frames
                                kf.handle_right[0] += freeze_frames
                        fcurve.update()
                        
        # --- 2. CINEMATIC SLOW-MOTION RAMPING (REALISTIC PBR) ---
        elif not is_anime and time_scale < 1.0:
            print("EXECUTING REALISTIC OPTICAL TIME DILATION...")
            bpy.context.scene.render.use_simplify = False
            # Scale Blender rendering timeline FPS mapping
            bpy.context.scene.render.fps_base = 1.0 / max(0.1, time_scale)

        # --- 3. DYNAMIC OPTICAL PUNCH-IN ZOOM ---
        cam = bpy.context.scene.camera
        if cam and zoom_amp > 0:
            if not cam.data.animation_data:
                cam.data.animation_data_create()
                
            cam.data.keyframe_insert(data_path="lens", frame=max(1, impact_frame - 1))
            original_lens = cam.data.lens
            
            # Violent focal length punch-in
            cam.data.lens = original_lens + (zoom_amp * 18.0)
            cam.data.keyframe_insert(data_path="lens", frame=impact_frame)
            
            # Snap back to nominal focal length post-freeze
            cam.data.lens = original_lens
            cam.data.keyframe_insert(data_path="lens", frame=impact_frame + freeze_frames + 3)

        # --- 4. VIOLENT CAMERA IMPACT JUDDER (RESTRICTED NOISE MODIFIER) ---
        if cam and shake_str > 0:
            cam.keyframe_insert(data_path="location", frame=impact_frame)
            if cam.animation_data and cam.animation_data.action:
                for fcurve in cam.animation_data.action.fcurves:
                    if fcurve.data_path == "location":
                        # Scrub pre-existing noise modifiers
                        for mod in fcurve.modifiers:
                            if mod.type == 'NOISE':
                                fcurve.modifiers.remove(mod)
                        
                        # Inject high-frequency impact judder
                        mod = fcurve.modifiers.new('NOISE')
                        mod.strength = shake_str * 0.025
                        mod.scale = 4.5 # High frequency rapid oscillation
                        mod.use_restricted_range = True
                        mod.frame_start = impact_frame
                        mod.frame_end = impact_frame + max(freeze_frames, 12)

    bpy.ops.wm.save_as_mainfile(filepath="{safe_path}")
    print("OMNIMATRIX_BLENDER_TEMPORAL_SUCCESS")

except Exception as error:
    print(f"OMNIMATRIX_BLENDER_ERROR: {{error}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_hitstop_physics.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_temporal_pipeline(self):
        self._handshake("IN_PROGRESS")
        self.log("Activating Anime Hit-Stop & Temporal Scheduler...")

        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("3D environment repository unpopulated. Synthesizing dummy temporal verification blueprint.", "WARNING")
            dummy_ctx = {"global_style": "anime_cel_shaded", "blender_executable": "blender", "action_description": "Combat clash.", "impact_frame": 24, "has_major_impact": True}
            dummy_data = self._query_temporal_intelligence("default_combat_stage", dummy_ctx)
            master_blueprint = {"default_combat_stage": dummy_data}
        else:
            master_blueprint = {}
            for file_name in sorted(os.listdir(self.env_dir)):
                if file_name.endswith(".blend"):
                    scene_name = file_name.replace(".blend", "")
                    blend_path = os.path.join(self.env_dir, file_name)
                    
                    context = self._load_project_context_and_collisions(scene_name)
                    
                    if context["has_major_impact"]:
                        self.log(f"[{scene_name}] Impact detected at Frame {context['impact_frame']}. Calculating temporal dilation...", "INFO")
                        time_data = self._query_temporal_intelligence(scene_name, context)
                        
                        self.log(f"[{scene_name}] Temporal Verdict -> {time_data['rationale']} (Freeze: {time_data['freeze_duration_frames']} | Zoom: {time_data['camera_zoom_amplitude']})", "INFO")
                        
                        script_path = self._compile_blender_temporal_script(blend_path, time_data, context["global_style"])
                        cmd = [context["blender_executable"], "-b", "-P", script_path]

                        try:
                            res = subprocess.run(cmd, capture_output=True, text=True)
                            if "OMNIMATRIX_BLENDER_TEMPORAL_SUCCESS" in res.stdout:
                                self.log(f"Hit-stop temporal dilation & camera judder baked successfully -> '{file_name}'", "SUCCESS")
                                master_blueprint[scene_name] = time_data
                            else:
   self.log(f"Blender temporal execution exception: {res.stdout[-300:]}", "ERROR")
                        except Exception as error:
                            self.log(f"Subprocess execution exception: {error}", "ERROR")

                        if os.path.exists(script_path):
                            os.remove(script_path)
                    else:
                        self.log(f"[{scene_name}] No impact collision detected. Preserving nominal continuous timeline.", "INFO")
                        master_blueprint[scene_name] = self._query_temporal_intelligence(scene_name, context)

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)

        self.log(f"Hit-stop temporal blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return master_blueprint

if __name__ == "__main__":
    scheduler = Ai_Agent_28_Anime_Hit_Stop_Frame_Scheduler()
    scheduler.execute_temporal_pipeline()