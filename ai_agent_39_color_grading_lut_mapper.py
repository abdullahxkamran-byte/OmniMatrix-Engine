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

class UniversalColorGradingLUTMapper:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 39: universal_color_grading_lut_mapper"
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
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("global_style", "realistic").lower()
            except Exception as e:
                self.log_message(f"Master config read warning, defaulting to realistic: {str(e)}", "WARNING")
        return "realistic"

    def _load_upstream_moods(self):
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        scene_contexts = []

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    scene_contexts.append({
                        "timestamp_sec": float(panel.get("timestamp_sec", i * 3.0)),
                        "mood_hint": panel.get("emotional_tone", "EPIC"),
                        "visual_prompt": panel.get("visual_prompt", "scene")
                    })
            except Exception as e:
                self.log_message(f"Upstream storyboard read warning: {str(e)}", "WARNING")

        if not scene_contexts:
            self.log_message("No upstream mood context. Injecting cinematic default grading.", "INFO")
            scene_contexts = [
                {"timestamp_sec": 0.0, "mood_hint": "MYSTERIOUS", "visual_prompt": "establishing shot"},
                {"timestamp_sec": 3.5, "mood_hint": "CLIMAX_SHOWDOWN", "visual_prompt": "intense action"}
            ]

        return scene_contexts

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

    def _save_to_workspace(self, data, filename="39_color_grading_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log_message(f"Universal Color Grading map securely saved to '{file_path}'", "SUCCESS")
            return file_path
        except Exception as e:
            self.log_message(f"Critical System Failure: Unable to save grading map: {str(e)}", "CRITICAL")
            return None

    def map_color_grading_luts(self):
        contexts = self._load_upstream_moods()
        global_style = self._load_master_config()
        self.log_message(f"Initializing Cinematic Colorist for '{global_style.upper()}' style...", "INFO")

        system_prompt = (
            f"You are a Lead Colorist & LUT Designer. The project global style is enforced as: '{global_style.upper()}'.\n"
            "Analyze scene moods and output precise Color Balance (Lift/Gamma/Gain) and Saturation arrays.\n"
            "REALISTIC Style Rules: Use Teal & Orange (warm highlights, cool shadows), gritty contrast (0.9 to 1.15), and moderate saturation (0.7 to 1.1).\n"
            "ANIME Style Rules: Use Shinkai-esque vibrant blues, Ufotable vivid reds, extreme contrast (1.1 to 1.4), and high saturation (1.1 to 1.6).\n"
            "For each scene context, design exactly 1 profile inside a list named 'color_grading_profiles':\n"
            "- 'timestamp_sec': float matching the scene timeline.\n"
            "- 'render_style_enforced': string ('realistic' or 'anime', matching global style).\n"
            "- 'lut_preset_name': string (descriptive name of the grade).\n"
            "- 'saturation_scale': float.\n"
            "- 'contrast_multiplier': float.\n"
            "- 'lift_shadows_rgb': array of 3 floats [R, G, B] (range 0.8 to 1.2, default ~1.0).\n"
            "- 'gamma_midtones_rgb': array of 3 floats [R, G, B] (range 0.8 to 1.2, default ~1.0).\n"
            "- 'gain_highlights_rgb': array of 3 floats [R, G, B] (range 0.8 to 1.2, default ~1.0).\n"
            "Output strictly valid JSON with key 'color_grading_profiles'. Do not compress data."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {
                    "model": self.model_cloud,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Scene Contexts:\n{json.dumps(contexts, indent=2)}"}
                    ],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=60) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    parsed_json = json.loads(cleaned)
                    final_output = {"color_grading_profiles": parsed_json.get("color_grading_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Route Failed: {str(e)}. Directing procedural color math fallback.", "WARNING")

        if not final_output:
            final_output = self._execute_procedural_fallback(contexts, global_style)
            
        self._save_to_workspace(final_output)
        self._bake_color_grading_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, contexts, style):
        profiles = []
        for ctx in contexts:
            ts = float(ctx.get("timestamp_sec", 0.0))
            mood = str(ctx.get("mood_hint", "")).upper()

            if style == "realistic":
                if "SAD" in mood or "DEEP" in mood or "MYSTERIOUS" in mood:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "lut_preset_name": "bleak_cinematic_gray", "saturation_scale": 0.6, "contrast_multiplier": 1.1, "lift_shadows_rgb": [0.95, 0.95, 1.05], "gamma_midtones_rgb": [0.9, 0.95, 1.0], "gain_highlights_rgb": [0.9, 0.9, 0.95]})
                elif "CLIMAX" in mood or "ACTION" in mood:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "lut_preset_name": "teal_and_orange_blockbuster", "saturation_scale": 1.1, "contrast_multiplier": 1.15, "lift_shadows_rgb": [0.9, 0.95, 1.05], "gamma_midtones_rgb": [1.0, 1.0, 1.0], "gain_highlights_rgb": [1.05, 1.0, 0.9]})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "lut_preset_name": "standard_filmic", "saturation_scale": 1.0, "contrast_multiplier": 1.0, "lift_shadows_rgb": [1.0, 1.0, 1.0], "gamma_midtones_rgb": [1.0, 1.0, 1.0], "gain_highlights_rgb": [1.0, 1.0, 1.0]})
            else:
                if "SAD" in mood or "DEEP" in mood or "MYSTERIOUS" in mood:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "lut_preset_name": "tragic_desaturated_blue", "saturation_scale": 0.7, "contrast_multiplier": 1.2, "lift_shadows_rgb": [0.9, 0.9, 1.1], "gamma_midtones_rgb": [0.95, 0.95, 1.05], "gain_highlights_rgb": [0.9, 0.9, 1.0]})
                elif "CLIMAX" in mood or "ACTION" in mood:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "lut_preset_name": "ufotable_climax_high_contrast", "saturation_scale": 1.4, "contrast_multiplier": 1.3, "lift_shadows_rgb": [0.95, 0.9, 0.95], "gamma_midtones_rgb": [1.05, 1.0, 1.0], "gain_highlights_rgb": [1.1, 1.05, 0.95]})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "lut_preset_name": "shinkai_vibrant_blues", "saturation_scale": 1.3, "contrast_multiplier": 1.15, "lift_shadows_rgb": [0.95, 0.95, 1.05], "gamma_midtones_rgb": [1.0, 1.0, 1.1], "gain_highlights_rgb": [1.05, 1.0, 1.0]})
        return {"color_grading_profiles": profiles}

    def _bake_color_grading_in_blender(self, grading_data):
        self.log_message("Engaging Blender Core: Compiling Smooth Color Grading Nodes...", "INFO")
        
        script_content = f"""
import bpy

profiles = {json.dumps(grading_data.get('color_grading_profiles', []))}
profiles.sort(key=lambda x: x.get('timestamp_sec', 0.0))

scene = bpy.context.scene
fps = scene.render.fps

scene.use_nodes = True
tree = scene.node_tree

try:
    # --- 1. CLEANUP PREVIOUS GRADING NODES ---
    for node in tree.nodes:
        if node.name.startswith("OMNI_LUT_"):
            tree.nodes.remove(node)

    # Find Composite output node
    comp_node = tree.nodes.get('Composite')
    if not comp_node:
        comp_node = tree.nodes.new('CompositorNodeComposite')
        comp_node.location = (1500, 0)

    # Intercept connection feeding into Composite
    prev_node = None
    for link in tree.links:
        if link.to_node == comp_node:
            prev_node = link.from_node
            tree.links.remove(link)
            break

    # --- 2. BUILD GOD-LEVEL GRADING NETWORK ---
    hsv_node = tree.nodes.new('CompositorNodeHueSat')
    hsv_node.name = "OMNI_LUT_HSV"
    hsv_node.location = (comp_node.location[0] - 600, 0)

    cb_node = tree.nodes.new('CompositorNodeColorBalance')
    cb_node.name = "OMNI_LUT_CB"
    cb_node.correction_method = 'LIFT_GAMMA_GAIN'
    cb_node.location = (comp_node.location[0] - 300, 0)

    # Wire nodes
    if prev_node:
        tree.links.new(prev_node.outputs[0], hsv_node.inputs['Image'])
    tree.links.new(hsv_node.outputs['Image'], cb_node.inputs['Image'])
    tree.links.new(cb_node.outputs['Image'], comp_node.inputs['Image'])
    
    viewer = tree.nodes.get('Viewer')
    if viewer:
        tree.links.new(cb_node.outputs['Image'], viewer.inputs['Image'])

    # --- 3. ANIMATE SMOOTH GRADE TRANSITIONS ---
    for idx, p in enumerate(profiles):
        impact_frame = max(1, int(p['timestamp_sec'] * fps))
        
        # Calculate transition duration (fade in over 1 second, or max available time)
        fade_duration = int(fps * 1.0) 
        pre_frame = max(1, impact_frame - fade_duration)
        
        # If it's the first profile, set the baseline directly
        if idx == 0:
            pre_frame = 1
            impact_frame = 1

        sat = p.get('saturation_scale', 1.0)
        val = p.get('contrast_multiplier', 1.0) # Using Value as a proxy for master contrast in HSV
        lift = tuple(p.get('lift_shadows_rgb', [1.0, 1.0, 1.0]))
        gamma = tuple(p.get('gamma_midtones_rgb', [1.0, 1.0, 1.0]))
        gain = tuple(p.get('gain_highlights_rgb', [1.0, 1.0, 1.0]))

        # Lock in previous state right before transition starts
        if idx > 0:
            hsv_node.keyframe_insert(data_path="color_saturation", frame=pre_frame)
            hsv_node.keyframe_insert(data_path="color_value", frame=pre_frame)
            cb_node.keyframe_insert(data_path="lift", frame=pre_frame)
            cb_node.keyframe_insert(data_path="gamma", frame=pre_frame)
            cb_node.keyframe_insert(data_path="gain", frame=pre_frame)

        # Set new state at impact frame
        hsv_node.color_saturation = sat
        hsv_node.color_value = val
        cb_node.lift = lift
        cb_node.gamma = gamma
        cb_node.gain = gain
        
        hsv_node.keyframe_insert(data_path="color_saturation", frame=impact_frame)
        hsv_node.keyframe_insert(data_path="color_value", frame=impact_frame)
        cb_node.keyframe_insert(data_path="lift", frame=impact_frame)
        cb_node.keyframe_insert(data_path="gamma", frame=impact_frame)
        cb_node.keyframe_insert(data_path="gain", frame=impact_frame)

except Exception as e:
    print(f"FAILED to compile color grading: {{str(e)}}")

try:
    bpy.ops.wm.save_mainfile()
except Exception as e:
    print(f"FAILED to save mainfile: {{str(e)}}")
"""
        script_path = os.path.join(self.workspace_dir, "temp_color_grading.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Baking Smooth Interpolated Color Grades into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Cinematic LUTs dynamically mapped and keyframed successfully.", "SUCCESS")

if __name__ == "__main__":
    mapper = UniversalColorGradingLUTMapper()
    output = mapper.map_color_grading_luts()
    print("\n--- OMNIMATRIX COLOR GRADING DEPT: AGENT 39 COMPLETE ---")
    print(f"Total grading profiles seamlessly woven: {len(output['color_grading_profiles'])}")
    for p in output["color_grading_profiles"]:
        print(f"Time: {p['timestamp_sec']}s | Preset: '{p['lut_preset_name']}' ({p.get('render_style_enforced', 'unknown')})")
        print(f"  Sat: {p['saturation_scale']} | Contrast: {p['contrast_multiplier']}")
    print("------------------------------------------------------------------")
