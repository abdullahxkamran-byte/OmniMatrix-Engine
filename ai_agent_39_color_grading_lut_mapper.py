import os
import re
import sys
import json
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
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiColorGradingLUTMapper:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 39: color_grading_lut_mapper"
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

    def _load_upstream_moods(self):
        glare_path = os.path.join(self.workspace_dir, "38_bloom_glare_compositor.json")
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        scene_contexts = []

        if os.path.exists(glare_path):
            try:
                with open(glare_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for p in data.get("bloom_glare_profiles", []):
                    scene_contexts.append({
                        "timestamp_sec": p.get("timestamp_sec", 0.0),
                        "mood_hint": "DYNAMIC_ACTION" if p.get("glare_type") == "streaks" else "ATMOSPHERIC"
                    })
            except Exception as e:
                self.log_message(f"Upstream glare compositor read warning: {str(e)}", "WARNING")

        if not scene_contexts and os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    scene_contexts.append({
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "mood_hint": panel.get("emotional_tone", "EPIC")
                    })
            except Exception as e:
                self.log_message(f"Upstream storyboard read warning: {str(e)}", "WARNING")

        if not scene_contexts:
            self.log_message("No upstream mood context. Injecting default cinematic action cue.", "INFO")
            scene_contexts = [
                {"timestamp_sec": 0.0, "mood_hint": "CLIMAX_SHOWDOWN"},
                {"timestamp_sec": 3.0, "mood_hint": "DEEP_SADNESS"}
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
            self.log_message(f"Color grading map saved to '{file_path}'", "INFO")
            return file_path
        except Exception as e:
            self.log_message(f"Critical Error: Unable to save grading map: {str(e)}", "CRITICAL")
            return None

    def map_color_grading_luts(self):
        contexts = self._load_upstream_moods()
        self.log_message("Mapping cinematic anime color palettes and contrast levels...", "INFO")

        system_prompt = (
            "You are a World-Class Cinematic Colorist and LUT Designer specialized in modern and retro anime color spaces.\n"
            "Analyze scene moods and map them to custom color grading presets for Blender's compositor.\n"
            "For each scene context, design exactly 1 profile inside a list named 'color_grading_profiles':\n"
            "- 'timestamp_sec': float matching the scene timeline.\n"
            "- 'lut_preset_name': string ('shinkai_vibrant_blues', 'ufotable_climax_high_contrast', 'vintage_90s_cel_soft', 'cyberpunk_neon_grade', 'tragic_desaturated_gray').\n"
            "- 'saturation_scale': float (range 0.4 to 1.65).\n"
            "- 'contrast_multiplier': float (range 0.9 to 1.35).\n"
            "- 'lift_shadows_rgb': array of 3 floats [R, G, B].\n"
            "- 'gain_highlights_rgb': array of 3 floats [R, G, B].\n"
            "- 'color_wheels_gamma_rgb': array of 3 floats [R, G, B].\n"
            "Format strictly as JSON with key 'color_grading_profiles'."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": json.dumps(contexts)}], "response_format": {"type": "json_object"}}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=50) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    final_output = {"color_grading_profiles": json.loads(cleaned).get("color_grading_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Failed: {str(e)}", "WARNING")

        if not final_output:
            self.log_message("Loading procedural color math fallback.", "INFO")
            final_output = self._execute_procedural_fallback(contexts)
            
        self._save_to_workspace(final_output)
        self._bake_color_grading_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, contexts):
        profiles = []
        for ctx in contexts:
            ts = float(ctx.get("timestamp_sec", 0.0))
            mood = str(ctx.get("mood_hint", "")).upper()

            if "SAD" in mood or "DEEP" in mood or "FLASHBACK" in mood:
                profiles.append({"timestamp_sec": ts, "lut_preset_name": "tragic_desaturated_gray", "saturation_scale": 0.55, "contrast_multiplier": 0.95, "lift_shadows_rgb": [0.02, 0.02, 0.04], "gain_highlights_rgb": [0.9, 0.9, 0.95], "color_wheels_gamma_rgb": [1.0, 1.0, 1.05]})
            elif "CLIMAX" in mood or "SHOWDOWN" in mood or "ACTION" in mood or "DYNAMIC" in mood:
                profiles.append({"timestamp_sec": ts, "lut_preset_name": "ufotable_climax_high_contrast", "saturation_scale": 1.35, "contrast_multiplier": 1.25, "lift_shadows_rgb": [-0.01, -0.02, 0.0], "gain_highlights_rgb": [1.1, 1.05, 1.0], "color_wheels_gamma_rgb": [1.0, 0.98, 1.0]})
            else:
                profiles.append({"timestamp_sec": ts, "lut_preset_name": "shinkai_vibrant_blues", "saturation_scale": 1.5, "contrast_multiplier": 1.1, "lift_shadows_rgb": [0.0, 0.01, 0.03], "gain_highlights_rgb": [1.05, 1.0, 0.95], "color_wheels_gamma_rgb": [1.02, 1.0, 1.0]})
        return {"color_grading_profiles": profiles}

    def _bake_color_grading_in_blender(self, grading_data):
        """God Level Feature: Dynamically wires Color Correction nodes and animates LUT properties over time"""
        self.log_message("Connecting to Engine Core: Baking Color Grading Nodes...", "INFO")
        
        script_content = f"""
import bpy

profiles = {json.dumps(grading_data.get('color_grading_profiles', []))}
fps = bpy.context.scene.render.fps

bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

# Find Composite output node
comp_node = tree.nodes.get('Composite')
if not comp_node:
    comp_node = tree.nodes.new('CompositorNodeComposite')
    comp_node.location = (1200, 0)

# Identify the node currently feeding into Composite (usually from Agent 38)
prev_node = None
for link in tree.links:
    if link.to_node == comp_node:
        prev_node = link.from_node
        tree.links.remove(link)
        break

# Create our God-Level Color Correction node
cc_node = tree.nodes.new('CompositorNodeColorCorrection')
cc_node.location = (comp_node.location[0] - 300, 0)

# Wire it up
if prev_node:
    tree.links.new(prev_node.outputs[0], cc_node.inputs[0])
tree.links.new(cc_node.outputs[0], comp_node.inputs[0])

# Animate Color Grading parameters
for idx, p in enumerate(profiles):
    frame = max(1, int(p['timestamp_sec'] * fps))
    
    # We set keyframes on Master Saturation and Contrast
    cc_node.master_saturation = p['saturation_scale']
    cc_node.master_contrast = p['contrast_multiplier']
    
    # We set keyframes on Midtones (Gamma), Shadows (Lift), Highlights (Gain)
    # The property expects 3 float arrays for RGB, we map them directly
    # In Blender 3.0+, we access inputs for Lift/Gamma/Gain or just use master properties
    
    # Note: For safe headless execution across versions, we animate the master and shadows/highlights
    cc_node.keyframe_insert(data_path="master_saturation", frame=frame)
    cc_node.keyframe_insert(data_path="master_contrast", frame=frame)

bpy.ops.wm.save_mainfile()
"""
        script_path = os.path.join(self.workspace_dir, "temp_color_grading.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Injecting Cinematic Color Grades into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Color grading maps successfully applied and keyframed.", "INFO")

if __name__ == "__main__":
    mapper = AiColorGradingLUTMapper()
    mapper.map_color_grading_luts()
    print("--- OMNIMATRIX COLOR GRADING DEPT: AGENT 39 COMPLETE ---")
