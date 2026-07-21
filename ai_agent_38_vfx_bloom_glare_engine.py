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

class AiVFXBloomGlareEngine:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 38: vfx_bloom_glare_engine"
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

    def _load_upstream_data(self):
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        vfx_context = []

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    vfx_context.append({
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "visual_prompt": panel.get("visual_prompt", "battle"),
                        "mood_tone": panel.get("emotional_tone", "EPIC")
                    })
            except Exception as e:
                self.log_message(f"Storyboard load warning: {str(e)}", "WARNING")

        if not vfx_context:
            self.log_message("No upstream contextual mood logs. Proceeding with extreme action baseline.", "INFO")
            vfx_context = [
                {"timestamp_sec": 1.5, "visual_prompt": "energy blast collision", "mood_tone": "CLIMAX_HYPED"},
                {"timestamp_sec": 4.0, "visual_prompt": "character recovery breathing", "mood_tone": "DRAMATIC"}
            ]

        return vfx_context

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

    def _save_to_workspace(self, data, filename="38_bloom_glare_compositor.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.log_message(f"Compositor glare setup saved to '{file_path}'", "INFO")
            return file_path
        except Exception as e:
            self.log_message(f"Critical Error: Unable to save glare settings: {str(e)}", "CRITICAL")
            return None

    def orchestrate_bloom_glare_compositing(self):
        context = self._load_upstream_data()
        self.log_message("Querying aesthetic post-processing rules...", "INFO")

        system_prompt = (
            "You are an expert Compositing TD specialized in high-end anime post-processing, bloom filters, and anamorphic flares.\n"
            "Analyze the emotional tone and visual prompt of a shot and output precise composition nodes parameters for Blender's Compositor.\n"
            "For each shot entry, generate exactly 1 configuration in a list named 'bloom_glare_profiles':\n"
            "- 'timestamp_sec': float matching the video timeline.\n"
            "- 'glare_type': string ('fog_glow', 'streaks', 'ghosts', 'simple_star').\n"
            "- 'glare_threshold': float (range 0.1 to 2.0).\n"
            "- 'bloom_blend_factor': float (range -1.0 to 1.0).\n"
            "- 'streak_count': integer (2, 4, 6, or 8).\n"
            "- 'glare_fade_factor': float (range 0.4 to 0.95).\n"
            "- 'color_modulation_shift': array of 3 floats [R, G, B].\n"
            "Format strictly as JSON with key 'bloom_glare_profiles'."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": json.dumps(context)}], "response_format": {"type": "json_object"}}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=50) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    final_output = {"bloom_glare_profiles": json.loads(cleaned).get("bloom_glare_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Failed: {str(e)}", "WARNING")

        if not final_output:
            self.log_message("Initializing procedural lighting engine fallback.", "INFO")
            final_output = self._execute_procedural_fallback(context)
            
        self._save_to_workspace(final_output)
        self._bake_compositor_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, context):
        profiles = []
        for ctx in context:
            ts = float(ctx.get("timestamp_sec", 0.0))
            mood = str(ctx.get("mood_tone", "")).upper()
            prompt = str(ctx.get("visual_prompt", "")).lower()

            if "CLIMAX" in mood or "blast" in prompt or "HYPE" in mood:
                profiles.append({"timestamp_sec": ts, "glare_type": "streaks", "glare_threshold": 0.25, "bloom_blend_factor": 0.75, "streak_count": 4, "glare_fade_factor": 0.85, "color_modulation_shift": [0.2, 0.5, 1.0]})
            elif "DRAMATIC" in mood or "recovery" in prompt or "SAD" in mood:
                profiles.append({"timestamp_sec": ts, "glare_type": "fog_glow", "glare_threshold": 0.6, "bloom_blend_factor": 0.4, "streak_count": 4, "glare_fade_factor": 0.90, "color_modulation_shift": [1.0, 0.85, 0.75]})
            else:
                profiles.append({"timestamp_sec": ts, "glare_type": "fog_glow", "glare_threshold": 1.0, "bloom_blend_factor": 0.1, "streak_count": 4, "glare_fade_factor": 0.75, "color_modulation_shift": [1.0, 1.0, 1.0]})
        return {"bloom_glare_profiles": profiles}

    def _bake_compositor_in_blender(self, compositor_data):
        """God Level Feature: Dynamically wires and animates Blender's Compositing Node Tree"""
        self.log_message("Connecting to Engine Core: Wiring Compositor Nodes...", "INFO")
        
        script_content = f"""
import bpy

profiles = {json.dumps(compositor_data.get('bloom_glare_profiles', []))}
fps = bpy.context.scene.render.fps

# Enable Compositor Nodes
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
tree.nodes.clear()

# Create Base Nodes
render_layers = tree.nodes.new('CompositorNodeRLayers')
render_layers.location = (0, 0)

glare_node = tree.nodes.new('CompositorNodeGlare')
glare_node.location = (300, 0)

color_balance = tree.nodes.new('CompositorNodeColorBalance')
color_balance.location = (600, 0)

comp_node = tree.nodes.new('CompositorNodeComposite')
comp_node.location = (900, 0)

# Link Nodes
tree.links.new(render_layers.outputs['Image'], glare_node.inputs['Image'])
tree.links.new(glare_node.outputs['Image'], color_balance.inputs['Image'])
tree.links.new(color_balance.outputs['Image'], comp_node.inputs['Image'])

# Animate Glare based on Profiles
# We'll use the first profile as the base, and animate peaks for the others
if profiles:
    base_p = profiles[0]
    glare_node.glare_type = base_p['glare_type'].upper()
    glare_node.streaks = base_p['streak_count']
    glare_node.fade = base_p['glare_fade_factor']
    
    # Set base keyframes at frame 1
    glare_node.threshold = 2.0 # High threshold = low glow initially
    glare_node.mix = 0.0
    glare_node.keyframe_insert(data_path="threshold", frame=1)
    glare_node.keyframe_insert(data_path="mix", frame=1)

    for p in profiles:
        impact_frame = int(p['timestamp_sec'] * fps)
        
        # 5 frames before impact: neutral
        glare_node.threshold = 2.0
        glare_node.mix = 0.0
        glare_node.keyframe_insert(data_path="threshold", frame=max(1, impact_frame - 5))
        glare_node.keyframe_insert(data_path="mix", frame=max(1, impact_frame - 5))
        
        # At impact: Flash / Max Glare
        glare_node.threshold = p['glare_threshold']
        glare_node.mix = p['bloom_blend_factor']
        glare_node.keyframe_insert(data_path="threshold", frame=impact_frame)
        glare_node.keyframe_insert(data_path="mix", frame=impact_frame)
        
        # 30 frames after impact: Fade out
        glare_node.threshold = 2.0
        glare_node.mix = 0.0
        glare_node.keyframe_insert(data_path="threshold", frame=impact_frame + 30)
        glare_node.keyframe_insert(data_path="mix", frame=impact_frame + 30)
        
        # Apply tint
        color_balance.lift = tuple(p['color_modulation_shift'])

bpy.ops.wm.save_mainfile()
"""
        script_path = os.path.join(self.workspace_dir, "temp_compositor.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Baking Compositor Glare into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Cinematic Bloom and Post-Processing applied via Compositor.", "INFO")

if __name__ == "__main__":
    compositor = AiVFXBloomGlareEngine()
    compositor.orchestrate_bloom_glare_compositing()
    print("--- OMNIMATRIX COMPOSITING DEPT: AGENT 38 COMPLETE ---")
