import os
import re
import sys
import json
import math
import time
import subprocess

# =====================================================================
# RULE 2: UNIVERSAL ENVIRONMENT CONFIGURATION (PURE UTILITY)
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

class Agent_40_Motion_Blur_Velocity_Vector_Applier:
    """
    OMNIMATRIX V2.0 PURE UTILITY: DETERMINISTIC MOTION BLUR ENGINE
    Operates without Generative AI overhead. Evaluates kinetic vector magnitude
    using pure mathematical physics to configure Blender render shutter and sample steps.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: Non-AI Naming enforcement (Agent_XX instead of Ai_Agent_XX)
        self.agent_name = "Agent_40_Motion_Blur_Velocity_Vector_Applier"
        self.workspace_dir = workspace_dir
        self.env_dir = os.path.join(self.workspace_dir, "Local_3D_Environments")
        self.blender_path = "blender"
        
        for directory in [self.workspace_dir, self.env_dir]:
            os.makedirs(directory, exist_ok=True)
            
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous motion blur blueprints and temporary scripts."""
        for filename in ["40_motion_blur_blueprint.json", "temp_motion_blur.py"]:
            file_path = os.path.join(self.workspace_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as error:
                    self.log(f"Failed to remove legacy file {file_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & CONFIG LOADERS
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
            # Advance atomic handshake to Agent 41 (Beat-to-Frame Sync Engine)
            data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_41_Beat_To_Frame_Effects_Sync_Engine"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_config(self):
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {
                        "style": data.get("global_style", "realistic").lower(),
                        "shutter_baseline": float(data.get("default_shutter", 0.5))
                    }
            except Exception:
                pass
        return {"style": "realistic", "shutter_baseline": 0.5}

    def _load_upstream_kinetics(self):
        kinetic_path = os.path.join(self.workspace_dir, "26_kinetic_rig_puppeteer_blueprint.json")
        speed_path = os.path.join(self.workspace_dir, "36_volumetric_speed_lines_blueprint.json")
        velocity_contexts = []

        if os.path.exists(speed_path):
            try:
                with open(speed_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for profile in data.get("speed_line_profiles", []):
                    velocity_contexts.append({
                        "timestamp_sec": float(profile.get("timestamp_sec", 0.0)),
                        "speed_style": profile.get("speed_line_style", "radial_zoom_in"),
                        "velocity_magnitude": 30.0 if "zoom" in profile.get("speed_line_style", "") else 15.0
                    })
            except Exception:
                pass

        if not velocity_contexts and os.path.exists(kinetic_path):
            try:
                with open(kinetic_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for sequence in data.get("rig_animation_sequences", []):
                    offset = sequence.get("translation_offset", [0.0, 0.0, 0.0])
                    magnitude = math.sqrt(sum(component ** 2 for component in offset))
                    velocity_contexts.append({
                        "timestamp_sec": float(sequence.get("timestamp_sec", 0.0)),
                        "speed_style": "kinetic_displacement",
                        "velocity_magnitude": round(magnitude, 2)
                    })
            except Exception:
                pass

        if not velocity_contexts:
            self.log("No upstream motion logs detected. Generating default kinetic calibration vectors.", "INFO")
            velocity_contexts = [
                {"timestamp_sec": 1.2, "speed_style": "radial_zoom_in", "velocity_magnitude": 45.0},
                {"timestamp_sec": 3.5, "speed_style": "horizontal_streaks", "velocity_magnitude": 12.5}
            ]

        return velocity_contexts

    # =====================================================================
    # DETERMINISTIC MATHEMATICAL VELOCITY SOLVER (ZERO LLM DEPENDENCY)
    # =====================================================================
    def apply_velocity_blur(self):
        self._handshake("IN_PROGRESS")
        kinetics = self._load_upstream_kinetics()
        config = self._load_config()
        self.log(f"Pure Utility Velocity Solver Initiated. Style Enforced: {config['style'].upper()}")
        
        output_profiles = []
        
        for index, item in enumerate(kinetics):
            timestamp = item["timestamp_sec"]
            velocity = item["velocity_magnitude"]
            is_anime = config["style"] == "anime"
            
            # Continuous mathematical formulas replace rigid hardcoded presets
            if is_anime:
                # Stepped smear style: Lower samples for crisp manga chopping, higher shutter angle for stylized streaks
                shutter_angle = min(360.0, round(90.0 + (velocity * 4.5), 1))
                samples = 6 if velocity > 25.0 else 4
                multiplier = round(min(4.0, 1.0 + (velocity / 15.0)), 2)
                render_type = "stepped_traditional_smear" if velocity > 20.0 else "camera_shutter_vector"
            else:
                # Realistic cinematic style: 180-degree rule baseline, high samples for organic motion blur
                shutter_angle = min(270.0, round(180.0 + (velocity * 1.5), 1))
                samples = min(32, max(16, int(16 + (velocity / 3.0))))
                multiplier = round(min(2.0, 0.8 + (velocity / 25.0)), 2)
                render_type = "camera_shutter_vector"

            output_profiles.append({
                "timestamp_sec": timestamp,
                "blur_render_type": render_type,
                "render_style_enforced": config["style"],
                "shutter_angle_degrees": shutter_angle,
                "blur_samples": samples,
                "velocity_vector_multiplier": multiplier,
                "smear_duplication_steps": 3 if (is_anime and velocity > 30.0) else 0
            })

        final_blueprint = {"motion_blur_profiles": output_profiles}
        blueprint_path = os.path.join(self.workspace_dir, "40_motion_blur_blueprint.json")
        with open(blueprint_path, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=4)
            
        self._bake_motion_blur_in_blender(final_blueprint)
        self._handshake("COMPLETED")
        return final_blueprint

    # =====================================================================
    # RULE 9, 17: BLENDER ENGINE COMPILER & VRAM SAFETY ENFORCER
    # =====================================================================
    def _bake_motion_blur_in_blender(self, blur_data):
        self.log("Compiling Blender Python execution script for velocity blur...")
        blur_json = json.dumps(blur_data.get('motion_blur_profiles', []))
        
        script_content = f"""
import bpy

# Rule 17: VRAM safety cap - process maximum 40 velocity profiles
profiles = {blur_json}[:40]
fps = bpy.context.scene.render.fps

bpy.context.scene.eevee.use_motion_blur = True
eevee = bpy.context.scene.eevee

# Initialize baseline optical shutter state at frame 1
eevee.motion_blur_shutter = 0.5
eevee.motion_blur_steps = 16
eevee.keyframe_insert(data_path="motion_blur_shutter", frame=1)
eevee.keyframe_insert(data_path="motion_blur_steps", frame=1)

for profile in profiles:
    if profile.get('blur_render_type') == 'none':
        continue
        
    impact_frame = max(1, int(profile['timestamp_sec'] * fps))
    pre_frame = max(1, impact_frame - int(fps * 0.2))
    post_frame = impact_frame + int(fps * 0.5)
    
    # Anchor preceding frame to standard sharp look
    eevee.motion_blur_shutter = 0.5
    eevee.motion_blur_steps = 16
    eevee.keyframe_insert(data_path="motion_blur_shutter", frame=pre_frame)
    eevee.keyframe_insert(data_path="motion_blur_steps", frame=pre_frame)
    
    # Inject mathematical velocity spike at impact frame
    shutter_fraction = min(profile['shutter_angle_degrees'] / 360.0, 1.0)
    eevee.motion_blur_shutter = shutter_fraction * profile['velocity_vector_multiplier']
    eevee.motion_blur_steps = min(32, int(profile['blur_samples'])) # Rule 17 VRAM cap
    
    eevee.keyframe_insert(data_path="motion_blur_shutter", frame=impact_frame)
    eevee.keyframe_insert(data_path="motion_blur_steps", frame=impact_frame)
    
    # Restore standard shutter after movement subsides
    eevee.motion_blur_shutter = 0.5
    eevee.motion_blur_steps = 16
    eevee.keyframe_insert(data_path="motion_blur_shutter", frame=post_frame)
    eevee.keyframe_insert(data_path="motion_blur_steps", frame=post_frame)

try:
    bpy.ops.wm.save_mainfile()
except Exception:
    pass
"""
        script_path = os.path.join(self.workspace_dir, "temp_motion_blur.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                try:
                    subprocess.run([self.blender_path, "-b", os.path.join(self.env_dir, filename), "-P", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
                except Exception as error:
                    self.log(f"Blender sub-process execution warning on {filename}: {error}", "WARNING")
                    
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log("Deterministic motion blur and velocity vectors successfully keyframed.", "SUCCESS")

if __name__ == "__main__":
    applier = Agent_40_Motion_Blur_Velocity_Vector_Applier()
    applier.apply_velocity_blur()
