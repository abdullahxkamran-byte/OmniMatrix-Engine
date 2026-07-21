import os
import re
import sys
import json
import subprocess
import urllib.request
import urllib.error

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiBeatToFrameEffectsSyncEngine:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 41: beat_to_frame_effects_sync_engine"
        self.workspace_dir = workspace_dir
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        self.blender_path = blender_path
        
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        for d in [self.workspace_dir, self.env_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_master_config(self):
        """God Level Upgrade: Checks Master Project Style (Realistic vs Anime)"""
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("global_style", "realistic").lower()
            except Exception as e:
                self.log_message(f"Master config read warning: {str(e)}", "WARNING")
        return "realistic"

    def _load_upstream_data(self):
        blur_path = os.path.join(self.workspace_dir, "40_motion_blur_blueprint.json")
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        rhythm_contexts = []

        if os.path.exists(blur_path):
            try:
                with open(blur_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for profile in data.get("motion_blur_profiles", []):
                    rhythm_contexts.append({
                        "timestamp_sec": profile.get("timestamp_sec", 0.0),
                        "implied_speed": "high_intensity" if profile.get("velocity_vector_multiplier", 0.0) > 2.0 else "ambient"
                    })
            except Exception as e:
                self.log_message(f"Upstream motion blur read warning: {str(e)}", "WARNING")

        if not rhythm_contexts and os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    rhythm_contexts.append({
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "implied_speed": "high_intensity" if "climax" in panel.get("emotional_tone", "").lower() else "ambient"
                    })
            except Exception as e:
                self.log_message(f"Upstream storyboard read warning: {str(e)}", "WARNING")

        if not rhythm_contexts:
            self.log_message("No visual timeline context found. Injecting standard 130 BPM action beats.", "INFO")
            rhythm_contexts = [
                {"timestamp_sec": 0.46, "implied_speed": "ambient"},
                {"timestamp_sec": 0.92, "implied_speed": "high_intensity"},
                {"timestamp_sec": 1.38, "implied_speed": "ambient"},
                {"timestamp_sec": 1.84, "implied_speed": "high_intensity"}
            ]

        return rhythm_contexts

    def _clean_json_response(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
        return cleaned

    def _save_to_workspace(self, data, filename="41_beat_sync_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log_message(f"Beat-to-frame sync blueprint saved to '{file_path}'", "INFO")
            return file_path
        except Exception as e:
            self.log_message(f"Critical Error: Unable to save sync blueprint: {str(e)}", "CRITICAL")
            return None

    def design_beat_sync_keyframes(self):
        rhythm_points = self._load_upstream_data()
        global_style = self._load_master_config()
        self.log_message(f"Sync Engine active. Mapping dynamic keys for '{global_style.upper()}' style...", "INFO")

        system_prompt = (
            f"You are an elite Video Editor and Music Sync Specialist. The project global style is enforced as: '{global_style.upper()}'.\n"
            "Your job is to match visual render properties directly with audio frequencies and beats.\n"
            "If style is REALISTIC: Use smooth camera shake amplitudes (0.1 to 0.5), disable stutter triggers, and keep chromatic aberration subtle (<0.05).\n"
            "If style is ANIME: Use high camera shake (0.8 to 1.8), enable stutter triggers for hit-stops, and use intense chromatic aberration (0.05 to 0.15).\n"
            "For each rhythm timestamp, generate exactly 1 sync configuration inside a list named 'beat_sync_profiles':\n"
            "- 'timestamp_sec': float matching the frame execution.\n"
            "- 'render_style_enforced': string (must match the global style).\n"
            "- 'audio_frequency_band': string ('sub_bass_drop', 'mid_range_melody', 'high_presence_tick').\n"
            "- 'vfx_scale_multiplier': float (range 0.5 to 2.5).\n"
            "- 'camera_shake_amplitude': float (instantly offsets camera position to simulate impacts).\n"
            "- 'fps_stutter_trigger': boolean (true for hit-stops/pauses).\n"
            "- 'rgb_split_chromatic_aberration': float (separates RGB channels for impact glitches).\n"
            "Format strictly as JSON with key 'beat_sync_profiles'."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {
                    "model": self.model_cloud,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Rhythm Points Logs:\n{json.dumps(rhythm_points, indent=2)}"}
                    ],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=50) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    final_output = {"beat_sync_profiles": json.loads(cleaned).get("beat_sync_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Failed: {str(e)}", "WARNING")

        if not final_output:
            self.log_message("Resolving procedural beat tracker fallback.", "INFO")
            final_output = self._execute_procedural_fallback(rhythm_points, global_style)
            
        self._save_to_workspace(final_output)
        self._bake_sync_keyframes_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, rhythm_points, style):
        profiles = []
        for rp in rhythm_points:
            ts = float(rp.get("timestamp_sec", 0.0))
            intensity_hint = str(rp.get("implied_speed", "")).lower()

            if style == "realistic":
                if "high" in intensity_hint:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "audio_frequency_band": "sub_bass_drop", "vfx_scale_multiplier": 1.5, "camera_shake_amplitude": 0.4, "fps_stutter_trigger": False, "rgb_split_chromatic_aberration": 0.03})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "audio_frequency_band": "high_presence_tick", "vfx_scale_multiplier": 1.0, "camera_shake_amplitude": 0.0, "fps_stutter_trigger": False, "rgb_split_chromatic_aberration": 0.0})
            else:
                if "high" in intensity_hint:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "audio_frequency_band": "sub_bass_drop", "vfx_scale_multiplier": 2.2, "camera_shake_amplitude": 1.4, "fps_stutter_trigger": True, "rgb_split_chromatic_aberration": 0.12})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "audio_frequency_band": "high_presence_tick", "vfx_scale_multiplier": 1.0, "camera_shake_amplitude": 0.0, "fps_stutter_trigger": False, "rgb_split_chromatic_aberration": 0.01})
                    
        return {"beat_sync_profiles": profiles}

    def _bake_sync_keyframes_in_blender(self, sync_data):
        """God Level Feature: Dynamically wires Compositor nodes, manipulates physical camera properties, and injects Hit-Stop timeline markers"""
        self.log_message("Connecting to Engine Core: Baking Beat-Sync Keyframes and Compositing Nodes...", "INFO")
        
        script_content = f"""
import bpy
import random

profiles = {json.dumps(sync_data.get('beat_sync_profiles', []))}
scene = bpy.context.scene
fps = scene.render.fps

# 1. Setup Compositor for RGB Split (Chromatic Aberration)
scene.use_nodes = True
tree = scene.node_tree

lens_node = tree.nodes.get("OmniMatrix_BeatSync_Aberration")
if not lens_node:
    lens_node = tree.nodes.new(type="CompositorNodeLensdist")
    lens_node.name = "OmniMatrix_BeatSync_Aberration"
    
    # Attempt automatic wiring if standard nodes exist
    render_layers = tree.nodes.get("Render Layers")
    composite = tree.nodes.get("Composite")
    if render_layers and composite:
        for link in tree.links:
            if link.from_node == render_layers and link.to_node == composite:
                tree.links.remove(link)
                break
        tree.links.new(render_layers.outputs[0], lens_node.inputs[0])
        tree.links.new(lens_node.outputs[0], composite.inputs[0])

# Initialize baseline for Lens Node
lens_node.inputs['Dispersion'].default_value = 0.0
lens_node.inputs['Dispersion'].keyframe_insert(data_path="default_value", frame=1)

cam = scene.camera

for p in profiles:
    impact_frame = int(p['timestamp_sec'] * fps)
    style = p.get('render_style_enforced', 'realistic').lower()
    
    # A. Execute RGB Split Compositor Animation
    if p['rgb_split_chromatic_aberration'] > 0:
        lens_node.inputs['Dispersion'].default_value = 0.0
        lens_node.inputs['Dispersion'].keyframe_insert(data_path="default_value", frame=max(1, impact_frame - 2))
        
        lens_node.inputs['Dispersion'].default_value = p['rgb_split_chromatic_aberration']
        lens_node.inputs['Dispersion'].keyframe_insert(data_path="default_value", frame=impact_frame)
        
        # Realistic fades out slowly, Anime snaps back quickly
        fade_frames = 5 if style == 'anime' else 15
        lens_node.inputs['Dispersion'].default_value = 0.0
        lens_node.inputs['Dispersion'].keyframe_insert(data_path="default_value", frame=impact_frame + fade_frames)
    
    # B. Execute Physical Camera Shake (Procedural Displacement)
    if cam and p['camera_shake_amplitude'] > 0:
        orig_loc = cam.location.copy()
        amp = p['camera_shake_amplitude'] / 5.0 # Scale to Blender units
        
        cam.keyframe_insert(data_path="location", frame=max(1, impact_frame - 1))
        
        # Hard Impact Position
        cam.location.x += random.uniform(-amp, amp)
        cam.location.y += random.uniform(-amp, amp)
        cam.location.z += random.uniform(-amp, amp)
        cam.keyframe_insert(data_path="location", frame=impact_frame)
        
        decay_frames = 4 if style == 'anime' else 12
        for i in range(1, decay_frames):
            decay = amp / (i + 1)
            cam.location.x = orig_loc.x + random.uniform(-decay, decay)
            cam.location.y = orig_loc.y + random.uniform(-decay, decay)
            cam.location.z = orig_loc.z + random.uniform(-decay, decay)
            cam.keyframe_insert(data_path="location", frame=impact_frame + i)
            
        cam.location = orig_loc
        cam.keyframe_insert(data_path="location", frame=impact_frame + decay_frames)

        # Force Interpolation Type based on Style
        if cam.animation_data and cam.animation_data.action:
            for fc in cam.animation_data.action.fcurves:
                if fc.data_path == "location":
                    for kf in fc.keyframe_points:
                        if impact_frame - 1 <= kf.co.x <= impact_frame + decay_frames:
                            kf.interpolation = 'CONSTANT' if style == 'anime' else 'BEZIER'
                            
    # C. Execute FPS Stutter / Hit-Stop Timeline Markers
    if p.get('fps_stutter_trigger', False):
        marker_name = f"OMNIMATRIX_HIT_STOP_{impact_frame}"
        if marker_name not in scene.timeline_markers:
            scene.timeline_markers.new(name=marker_name, frame=impact_frame)

bpy.ops.wm.save_mainfile()
"""
        script_path = os.path.join(self.workspace_dir, "temp_beat_sync.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Injecting Rhythm Sync into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Universal Beat-Sync Engine processing complete.", "INFO")

if __name__ == "__main__":
    sync_engine = AiBeatToFrameEffectsSyncEngine()
    output = sync_engine.design_beat_sync_keyframes()
    
    print("\n--- OMNIMATRIX RHYTHM COMPOSITOR: AGENT 41 COMPLETE ---")
    print(f"Total rhythm frames synchronized: {len(output['beat_sync_profiles'])}")
    for p in output["beat_sync_profiles"]:
        print(f"Time: {p['timestamp_sec']}s | Band: '{p['audio_frequency_band']}' ({p.get('render_style_enforced', 'unknown')})")
        print(f"  Camera Shake: {p['camera_shake_amplitude']} | Hit-Stop Trigger: {p['fps_stutter_trigger']}")
        print(f"  RGB Aberration: {p['rgb_split_chromatic_aberration']}")
    print("------------------------------------------------------------")
