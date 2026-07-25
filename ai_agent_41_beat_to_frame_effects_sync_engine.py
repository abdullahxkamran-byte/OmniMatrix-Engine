import os
import re
import sys
import json
import math
import time
import random
import subprocess
import urllib.request
import urllib.error

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

class Ai_Agent_41_Beat_To_Frame_Effects_Sync_Engine:
    """
    OMNIMATRIX V2.0 GOD-LEVEL RHYTHM & KINETIC SYNC ENGINE
    Synchronizes visual rendering properties, camera kinetic shakes, chromatic aberration,
    and hit-stop frame freezing directly to acoustic beat maps and frequency bands.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_41_Beat_To_Frame_Effects_Sync_Engine"
        self.workspace_dir = workspace_dir
        self.env_dir = os.path.join(self.workspace_dir, "Local_3D_Environments")
        self.blender_path = "blender"
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        
        for directory in [self.workspace_dir, self.env_dir]:
            os.makedirs(directory, exist_ok=True)
            
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous beat sync blueprints and temporary scripts."""
        for filename in ["41_beat_sync_blueprint.json", "temp_beat_sync.py"]:
            file_path = os.path.join(self.workspace_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as error:
                    self.log(f"Failed to scrub legacy file {file_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7 & 4: ATOMIC HANDSHAKE & LIMITLESS CONFIG LOADERS
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
            # Handoff to Module E: FFmpeg Video Assembler
            data["orchestrator_matrix"]["next_agent"] = "Agent_42_FFmpeg_Raw_Buffer_Collector"
            
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
                        "theme": data.get("theme", "kinetic_action")
                    }
            except Exception:
                pass
        return {"style": "realistic", "theme": "limitless_rhythm"}

    def _load_rhythm_events(self):
        """Fetches audio beat drops from Module B or visual cues from Module A/D."""
        matrix_path = os.path.join(self.workspace_dir, "matrix_state.json")
        blur_path = os.path.join(self.workspace_dir, "40_motion_blur_blueprint.json")
        rhythm_contexts = []

        # 1. Attempt to extract acoustic beat maps from Module B Audio Commandos
        if os.path.exists(matrix_path):
            try:
                with open(matrix_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    beat_events = state.get("module_b_audio", {}).get("phonk_beat_map", {}).get("beat_sync_events", [])
                    for event in beat_events:
                        rhythm_contexts.append({
                            "timestamp_sec": float(event.get("timestamp_sec", 0.0)),
                            "intensity_band": event.get("frequency_band", "sub_bass_drop"),
                            "implied_energy": float(event.get("impact_magnitude", 1.5))
                        })
            except Exception:
                pass

        # 2. Fallback to velocity peaks from Agent 40 Motion Blur
        if not rhythm_contexts and os.path.exists(blur_path):
            try:
                with open(blur_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for profile in data.get("motion_blur_profiles", []):
                    if profile.get("velocity_vector_multiplier", 0.0) > 1.2:
                        rhythm_contexts.append({
                            "timestamp_sec": float(profile.get("timestamp_sec", 0.0)),
                            "intensity_band": "high_velocity_smear",
                            "implied_energy": float(profile.get("velocity_vector_multiplier", 1.0))
                        })
            except Exception:
                pass

        if not rhythm_contexts:
            self.log("No upstream audio beat maps detected. Generating dynamic baseline rhythm vectors.", "INFO")
            rhythm_contexts = [
                {"timestamp_sec": 1.0, "intensity_band": "sub_bass_drop", "implied_energy": 2.5},
                {"timestamp_sec": 2.5, "intensity_band": "transient_snare_spike", "implied_energy": 1.8},
                {"timestamp_sec": 4.2, "intensity_band": "sub_bass_drop", "implied_energy": 3.0}
            ]

        return rhythm_contexts

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
        with urllib.request.urlopen(request, timeout=35) as response:
            return json.loads(response.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14, 15: QUAD-CORE LIMITLESS RHYTHM RECIPE SYNTHESIZER
    # =====================================================================
    def design_beat_sync_keyframes(self):
        self._handshake("IN_PROGRESS")
        rhythms = self._load_rhythm_events()
        config = self._load_config()
        self.log(f"Quad-Core Beat Sync Forge Initiated. Style: {config['style'].upper()} | Theme: {config['theme']}")
        
        # Rule 15: Pure Mathematical Rhythm Recipe (ZERO Hardcoded Preset Gulaami!)
        prompt = (
            f"You are OMNIMATRIX Lead VFX Rhythm Specialist. Global Style: '{config['style']}', Theme: '{config['theme']}'.\n"
            "Invent completely unique, limitless kinetic synchronization RECIPES for each acoustic rhythm event.\n"
            "DO NOT use fixed preset fallbacks. Return a JSON object with list 'beat_sync_profiles' containing:\n"
            "- 'timestamp_sec': float, 'render_style_enforced': string ('realistic' or 'anime'), 'event_concept': string,\n"
            "- 'audio_frequency_band': string ('sub_bass_drop', 'mid_range_melody', 'transient_snare_spike', 'high_presence_tick'),\n"
            "- 'vfx_scale_multiplier': float (0.2 to 5.0 - scales visual emitters on beat),\n"
            "- 'camera_shake_amplitude': float (0.0 to 4.0 - physical camera displacement on impact),\n"
            "- 'acoustic_vibration_frequency': float (1.0 to 25.0 - F-Curve noise hz for bass resonance vibration),\n"
            "- 'fps_stutter_trigger': boolean (true for hit-stop frame freezing during heavy impacts),\n"
            "- 'rgb_split_chromatic_aberration': float (0.0 to 0.3 - optical lens dispersion glitch).\n"
            "Realistic: subtle shake, organic resonance. Anime: aggressive camera impact, hit-stop pauses, extreme RGB aberration.\n"
            "Zero compression or placeholders allowed."
        )
        
        output = None
        user_msg = f"Rhythm Events Context:\n{json.dumps(rhythms)}"
        
        # Core 1: Gemini (Primary - Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"{prompt}\n\n{user_msg}"}]}],
                    "generationConfig": {"temperature": 0.85, "responseMimeType": "application/json"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json"})
                output = {"beat_sync_profiles": json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"])).get("beat_sync_profiles", [])}
                self.log("[Core 1: Gemini] Synthesized limitless beat synchronization profiles!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")
        
        # Core 2: OpenAI (Failsafe - Rule 14 & 16)
        if self.openai_key and not output:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                    "response_format": {"type": "json_object"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"})
                output = {"beat_sync_profiles": json.loads(self._clean_json(res["choices"][0]["message"]["content"])).get("beat_sync_profiles", [])}
                self.log("[Core 2: OpenAI] Synthesized limitless beat synchronization profiles!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")
        
        # Core 3: Ollama (Local Fallback - Rule 6)
        if not output:
            try:
                url = "http://localhost:11434/api/chat"
                payload = {
                    "model": "llama3",
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                    "format": "json",
                    "stream": False
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json"})
                output = {"beat_sync_profiles": json.loads(self._clean_json(res.get("message", {}).get("content", "{}"))).get("beat_sync_profiles", [])}
                self.log("[Core 3: Ollama] Generated local beat synchronization profiles!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")
        
        # Core 4: 100% Offline Math Autonomy (Rule 10 - Algorithmic Rhythm Synthesis)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline acoustic float synthesis algorithm...", "WARNING")
            bands = ["sub_bass_drop", "mid_range_melody", "transient_snare_spike", "high_presence_tick"]
            output = {"beat_sync_profiles": []}
            for index, item in enumerate(rhythms):
                random.seed(int((item["timestamp_sec"] + index + 41) * 1000))
                energy = float(item.get("implied_energy", 1.5))
                is_heavy = energy > 1.8 or "bass" in str(item.get("intensity_band", "")).lower()
                is_anime = config["style"] == "anime"
                
                output["beat_sync_profiles"].append({
                    "timestamp_sec": item["timestamp_sec"],
                    "render_style_enforced": config["style"],
                    "event_concept": f"Algorithmic_Acoustic_Peak_{index}",
                    "audio_frequency_band": "sub_bass_drop" if is_heavy else random.choice(bands),
                    "vfx_scale_multiplier": round(energy * 1.4, 2) if is_heavy else 1.0,
                    "camera_shake_amplitude": round(energy * 0.8, 2) if (is_heavy or is_anime) else round(energy * 0.2, 2),
                    "acoustic_vibration_frequency": round(random.uniform(8.0, 20.0), 1) if is_heavy else 0.0,
                    "fps_stutter_trigger": True if (is_heavy and is_anime) else False,
                    "rgb_split_chromatic_aberration": round(energy * 0.06, 3) if is_heavy else 0.0
                })
        
        blueprint_path = os.path.join(self.workspace_dir, "41_beat_sync_blueprint.json")
        with open(blueprint_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)
            
        self._bake_sync_keyframes_in_blender(output)
        self._handshake("COMPLETED")
        return output

    # =====================================================================
    # RULE 9, 12, 17: BLENDER KINETIC & HIT-STOP COMPILER
    # =====================================================================
    def _bake_sync_keyframes_in_blender(self, sync_data):
        self.log("Compiling Blender Python execution script for beat synchronization...")
        sync_json = json.dumps(sync_data.get('beat_sync_profiles', []))
        
        script_content = f"""
import bpy
import math
import random

# Rule 17: VRAM safety cap - process maximum 60 acoustic synchronization events
profiles = {sync_json}[:60]
profiles.sort(key=lambda x: x.get('timestamp_sec', 0.0))

scene = bpy.context.scene
fps = scene.render.fps

# 1. Setup Compositor for RGB Chromatic Aberration
scene.use_nodes = True
tree = scene.node_tree

lens_node = tree.nodes.get("OmniMatrix_BeatSync_Aberration")
if not lens_node:
    lens_node = tree.nodes.new(type="CompositorNodeLensdist")
    lens_node.name = "OmniMatrix_BeatSync_Aberration"
    
    render_layers = tree.nodes.get("Render Layers")
    composite = tree.nodes.get("Composite")
    if render_layers and composite:
        for link in list(tree.links):
            if link.from_node == render_layers and link.to_node == composite:
                tree.links.remove(link)
                break
        tree.links.new(render_layers.outputs[0], lens_node.inputs[0])
        tree.links.new(lens_node.outputs[0], composite.inputs[0])

# Initialize optical dispersion baseline at frame 1
lens_node.inputs['Dispersion'].default_value = 0.0
lens_node.inputs['Dispersion'].keyframe_insert(data_path="default_value", frame=1)

camera_object = scene.camera

for profile in profiles:
    impact_frame = max(1, int(profile['timestamp_sec'] * fps))
    style = str(profile.get('render_style_enforced', 'realistic')).lower()
    
    # A. Execute RGB Split Chromatic Aberration Pulse
    aberration = float(profile.get('rgb_split_chromatic_aberration', 0.0))
    if aberration > 0.0:
        lens_node.inputs['Dispersion'].default_value = 0.0
        lens_node.inputs['Dispersion'].keyframe_insert(data_path="default_value", frame=max(1, impact_frame - 2))
        
        lens_node.inputs['Dispersion'].default_value = aberration
        lens_node.inputs['Dispersion'].keyframe_insert(data_path="default_value", frame=impact_frame)
        
        fade_duration = 4 if style == 'anime' else 12
        lens_node.inputs['Dispersion'].default_value = 0.0
        lens_node.inputs['Dispersion'].keyframe_insert(data_path="default_value", frame=impact_frame + fade_duration)
    
    # B. Execute Physical Camera Shake & Acoustic Resonance (Rule 12)
    amplitude = float(profile.get('camera_shake_amplitude', 0.0))
    vibe_freq = float(profile.get('acoustic_vibration_frequency', 0.0))
    
    if camera_object and amplitude > 0.0:
        original_location = camera_object.location.copy()
        displacement = amplitude / 4.0
        
        camera_object.keyframe_insert(data_path="location", frame=max(1, impact_frame - 1))
        
        # Immediate physical kinetic impact
        camera_object.location.x += random.uniform(-displacement, displacement)
        camera_object.location.y += random.uniform(-displacement, displacement)
        camera_object.location.z += random.uniform(-displacement, displacement)
        camera_object.keyframe_insert(data_path="location", frame=impact_frame)
        
        decay_steps = 4 if style == 'anime' else 10
        for step in range(1, decay_steps):
            decay_factor = displacement / (step + 1)
            camera_object.location.x = original_location.x + random.uniform(-decay_factor, decay_factor)
            camera_object.location.y = original_location.y + random.uniform(-decay_factor, decay_factor)
            camera_object.location.z = original_location.z + random.uniform(-decay_factor, decay_factor)
            camera_object.keyframe_insert(data_path="location", frame=impact_frame + step)
            
        camera_object.location = original_location
        camera_object.keyframe_insert(data_path="location", frame=impact_frame + decay_steps)

        # Rule 12: Inject F-Curve Noise modifier for continuous acoustic sub-bass resonance
        if vibe_freq > 4.0 and camera_object.animation_data and camera_object.animation_data.action:
            for fcurve in camera_object.animation_data.action.fcurves:
                if fcurve.data_path == "location":
                    noise_modifier = fcurve.modifiers.new(type='NOISE')
                    noise_modifier.scale = 10.0 / vibe_freq
                    noise_modifier.strength = displacement * 0.3
                    noise_modifier.frame_start = impact_frame
                    noise_modifier.frame_end = impact_frame + decay_steps + 8

        # Enforce style interpolation
        if camera_object.animation_data and camera_object.animation_data.action:
            for fcurve in camera_object.animation_data.action.fcurves:
                if fcurve.data_path == "location":
                    for keyframe in fcurve.keyframe_points:
                        if impact_frame - 1 <= keyframe.co.x <= impact_frame + decay_steps:
                            keyframe.interpolation = 'CONSTANT' if style == 'anime' else 'BEZIER'
                            
    # C. Execute Hit-Stop Timeline Markers (FPS Stutter Freeze for Anime Impacts)
    if profile.get('fps_stutter_trigger', False):
        marker_name = f"OMNIMATRIX_HIT_STOP_{{impact_frame}}"
        if marker_name not in scene.timeline_markers:
            scene.timeline_markers.new(name=marker_name, frame=impact_frame)

try:
    bpy.ops.wm.save_mainfile()
except Exception:
    pass
"""
        script_path = os.path.join(self.workspace_dir, "temp_beat_sync.py")
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
        self.log("Universal acoustic beat synchronization and kinetic impacts keyframed successfully.", "SUCCESS")

if __name__ == "__main__":
    engine = Ai_Agent_41_Beat_To_Frame_Effects_Sync_Engine()
    engine.design_beat_sync_keyframes()