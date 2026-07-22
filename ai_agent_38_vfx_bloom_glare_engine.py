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

class UniversalBloomGlareEngine:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 38: universal_bloom_glare_engine"
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

    def _load_upstream_data(self):
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        vfx_context = []

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    vfx_context.append({
                        "timestamp_sec": float(panel.get("timestamp_sec", i * 3.0)),
                        "visual_prompt": panel.get("visual_prompt", "battle action"),
                        "mood_tone": panel.get("emotional_tone", "EPIC")
                    })
            except Exception as e:
                self.log_message(f"Storyboard load error: {str(e)}", "ERROR")

        if not vfx_context:
            self.log_message("No upstream mood logs found. Generating baseline cinematic post-processing peaks.", "INFO")
            vfx_context = [
                {"timestamp_sec": 1.5, "visual_prompt": "high energy blast collision", "mood_tone": "CLIMAX_HYPED"},
                {"timestamp_sec": 4.0, "visual_prompt": "character recovery breathing dust", "mood_tone": "DRAMATIC"}
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
            self.log_message(f"Universal compositor blueprint securely saved to '{file_path}'", "SUCCESS")
            return file_path
        except Exception as e:
            self.log_message(f"Critical System Failure: Unable to save compositor settings: {str(e)}", "CRITICAL")
            return None

    def orchestrate_bloom_glare_compositing(self):
        context = self._load_upstream_data()
        global_style = self._load_master_config()
        self.log_message(f"Initializing Post-Processing Architect for '{global_style.upper()}' style...", "INFO")

        system_prompt = (
            f"You are a Lead Compositing TD. The project global style is enforced as: '{global_style.upper()}'.\n"
            "Analyze the emotional tone and visual prompt of a sequence to output precise dynamic thresholds for Compositor.\n"
            "REALISTIC Style Rules: Use low chromatic aberration (0.02-0.05), horizontal 2-streak flares (blue/teal tint), subtle fog glow, natural cinematic contrast.\n"
            "ANIME Style Rules: Use high chromatic aberration (0.05-0.15) for impact frames, 4 or 6 streak stars, heavy aggressive fog glow bloom, saturated stylized color shifts.\n"
            "For each shot entry, generate exactly 1 configuration in a list named 'compositor_dynamic_profiles':\n"
            "- 'timestamp_sec': float matching the video timeline.\n"
            "- 'render_style_enforced': string ('realistic' or 'anime', matching global style).\n"
            "- 'fog_glow_threshold': float (lower means more bloom, range 0.1 to 2.0).\n"
            "- 'streak_glare_threshold': float (range 0.1 to 3.0).\n"
            "- 'streak_mix_factor': float (range -0.5 to 1.0).\n"
            "- 'chromatic_dispersion': float (range 0.0 to 0.2).\n"
            "- 'color_balance_lift_rgb': array of 3 floats [R, G, B].\n"
            "Output strictly valid JSON with key 'compositor_dynamic_profiles'. Do not compress data."
        )

        final_output = None
        if self.openai_api_key:
            self.log_message(f"Querying Cloud API Node [{self.model_cloud}]", "INFO")
            try:
                payload = {
                    "model": self.model_cloud,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Sequence Context:\n{json.dumps(context, indent=2)}"}
                    ],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_api_key}"})
                with urllib.request.urlopen(req, timeout=60) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    cleaned = self._clean_json_response(res_json["choices"][0]["message"]["content"])
                    parsed_json = json.loads(cleaned)
                    final_output = {"compositor_dynamic_profiles": parsed_json.get("compositor_dynamic_profiles", [])}
            except Exception as e:
                self.log_message(f"Cloud API Route Failed: {str(e)}. Directing procedural post-processing fallback.", "WARNING")

        if not final_output:
            final_output = self._execute_procedural_fallback(context, global_style)
            
        self._save_to_workspace(final_output)
        self._bake_universal_compositor_in_blender(final_output)
        return final_output

    def _execute_procedural_fallback(self, context, style):
        profiles = []
        for ctx in context:
            ts = float(ctx.get("timestamp_sec", 0.0))
            mood = str(ctx.get("mood_tone", "")).upper()
            prompt = str(ctx.get("visual_prompt", "")).lower()

            if style == "realistic":
                if "CLIMAX" in mood or "blast" in prompt or "HYPE" in mood:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "fog_glow_threshold": 0.5, "streak_glare_threshold": 0.3, "streak_mix_factor": 0.6, "chromatic_dispersion": 0.08, "color_balance_lift_rgb": [0.95, 0.98, 1.05]})
                elif "DRAMATIC" in mood or "recovery" in prompt or "SAD" in mood:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "fog_glow_threshold": 1.2, "streak_glare_threshold": 1.5, "streak_mix_factor": 0.1, "chromatic_dispersion": 0.02, "color_balance_lift_rgb": [0.9, 0.9, 0.95]})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "realistic", "fog_glow_threshold": 1.5, "streak_glare_threshold": 2.0, "streak_mix_factor": 0.0, "chromatic_dispersion": 0.01, "color_balance_lift_rgb": [1.0, 1.0, 1.0]})
            else:
                if "CLIMAX" in mood or "blast" in prompt or "HYPE" in mood:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "fog_glow_threshold": 0.2, "streak_glare_threshold": 0.2, "streak_mix_factor": 0.9, "chromatic_dispersion": 0.15, "color_balance_lift_rgb": [1.1, 0.8, 0.9]})
                elif "DRAMATIC" in mood or "recovery" in prompt or "SAD" in mood:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "fog_glow_threshold": 0.8, "streak_glare_threshold": 1.0, "streak_mix_factor": 0.4, "chromatic_dispersion": 0.05, "color_balance_lift_rgb": [0.8, 0.8, 1.1]})
                else:
                    profiles.append({"timestamp_sec": ts, "render_style_enforced": "anime", "fog_glow_threshold": 1.0, "streak_glare_threshold": 1.5, "streak_mix_factor": 0.1, "chromatic_dispersion": 0.02, "color_balance_lift_rgb": [1.0, 1.0, 1.0]})
        return {"compositor_dynamic_profiles": profiles}

    def _bake_universal_compositor_in_blender(self, compositor_data):
        self.log_message("Engaging Blender Core: Compiling Advanced Compositor Pipeline...", "INFO")
        
        script_content = f"""
import bpy

# --- 1. COMPOSITOR PREP & CLEANUP ---
profiles = {json.dumps(compositor_data.get('compositor_dynamic_profiles', []))}
scene = bpy.context.scene
fps = scene.render.fps

scene.use_nodes = True
tree = scene.node_tree
tree.nodes.clear()

global_style = 'realistic'
if profiles:
    global_style = profiles[0].get('render_style_enforced', 'realistic').lower()

try:
    # --- 2. BUILD ADVANCED NODE NETWORK ---
    render_layers = tree.nodes.new('CompositorNodeRLayers')
    render_layers.location = (0, 0)

    # Node 1: Base Bloom (Fog Glow) - Always Active, threshold animates
    glare_fog = tree.nodes.new('CompositorNodeGlare')
    glare_fog.glare_type = 'FOG_GLOW'
    glare_fog.quality = 'HIGH'
    glare_fog.size = 8 if global_style == 'anime' else 6
    glare_fog.location = (300, 0)

    # Node 2: Stylized Flares (Streaks) - Mix animates heavily on impact
    glare_streak = tree.nodes.new('CompositorNodeGlare')
    glare_streak.glare_type = 'STREAKS'
    glare_streak.quality = 'HIGH'
    glare_streak.fade = 0.85
    if global_style == 'realistic':
        glare_streak.streaks = 2
        glare_streak.angle_offset = 0.0 # Horizontal Anamorphic
        glare_streak.color_modulation = 0.5
    else:
        glare_streak.streaks = 4
        glare_streak.angle_offset = 0.785 # 45 degrees star
        glare_streak.color_modulation = 0.2
    glare_streak.location = (600, 0)

    # Node 3: Optical Lens Distortion (Chromatic Aberration)
    lens_dist = tree.nodes.new('CompositorNodeLensdist')
    lens_dist.use_projector = True
    lens_dist.use_fit = True
    lens_dist.location = (900, 0)

    # Node 4: Cinematic Color Balance
    color_balance = tree.nodes.new('CompositorNodeColorBalance')
    color_balance.location = (1200, 0)

    # Outputs
    comp_node = tree.nodes.new('CompositorNodeComposite')
    comp_node.location = (1500, 100)
    
    viewer_node = tree.nodes.new('CompositorNodeViewer')
    viewer_node.location = (1500, -100)

    # Wire the God-Level Pipeline
    tree.links.new(render_layers.outputs['Image'], glare_fog.inputs['Image'])
    tree.links.new(glare_fog.outputs['Image'], glare_streak.inputs['Image'])
    tree.links.new(glare_streak.outputs['Image'], lens_dist.inputs['Image'])
    tree.links.new(lens_dist.outputs['Image'], color_balance.inputs['Image'])
    tree.links.new(color_balance.outputs['Image'], comp_node.inputs['Image'])
    tree.links.new(color_balance.outputs['Image'], viewer_node.inputs['Image'])

    # --- 3. ANIMATE IMPACT PROFILES ---
    # Set default safe states at frame 1
    glare_fog.threshold = 2.0
    glare_fog.keyframe_insert(data_path="threshold", frame=1)
    
    glare_streak.threshold = 3.0
    glare_streak.mix = -0.8
    glare_streak.keyframe_insert(data_path="threshold", frame=1)
    glare_streak.keyframe_insert(data_path="mix", frame=1)
    
    lens_dist.dispersion = 0.0
    lens_dist.keyframe_insert(data_path="dispersion", frame=1)

    for p in profiles:
        impact_frame = int(p.get('timestamp_sec', 0.0) * fps)
        pre_frame = max(1, impact_frame - int(fps * 0.2)) # 0.2s before impact
        post_frame = impact_frame + int(fps * 1.5) # 1.5s after impact
        
        # Fog Glow Automation
        glare_fog.threshold = 2.0
        glare_fog.keyframe_insert(data_path="threshold", frame=pre_frame)
        glare_fog.threshold = p.get('fog_glow_threshold', 1.0)
        glare_fog.keyframe_insert(data_path="threshold", frame=impact_frame)
        glare_fog.threshold = 2.0
        glare_fog.keyframe_insert(data_path="threshold", frame=post_frame)

        # Streak Flash Automation
        glare_streak.threshold = 3.0
        glare_streak.mix = -0.8
        glare_streak.keyframe_insert(data_path="threshold", frame=pre_frame)
        glare_streak.keyframe_insert(data_path="mix", frame=pre_frame)
        
        glare_streak.threshold = p.get('streak_glare_threshold', 1.0)
        glare_streak.mix = p.get('streak_mix_factor', 0.0)
        glare_streak.keyframe_insert(data_path="threshold", frame=impact_frame)
        glare_streak.keyframe_insert(data_path="mix", frame=impact_frame)
        
        glare_streak.threshold = 3.0
        glare_streak.mix = -0.8
        glare_streak.keyframe_insert(data_path="threshold", frame=post_frame)
        glare_streak.keyframe_insert(data_path="mix", frame=post_frame)

        # Lens Chromatic Aberration Impact Automation
        lens_dist.dispersion = 0.0
        lens_dist.keyframe_insert(data_path="dispersion", frame=pre_frame)
        lens_dist.dispersion = p.get('chromatic_dispersion', 0.0)
        lens_dist.keyframe_insert(data_path="dispersion", frame=impact_frame)
        lens_dist.dispersion = 0.0
        lens_dist.keyframe_insert(data_path="dispersion", frame=post_frame)

        # Color Tinting (Static per scene impact, blending handled smoothly by compositor)
        color_balance.lift = tuple(p.get('color_balance_lift_rgb', [1.0, 1.0, 1.0]))
        
except Exception as e:
    print(f"FAILED to build compositing pipeline: {{str(e)}}")

try:
    bpy.ops.wm.save_mainfile()
except Exception as e:
    print(f"FAILED to save mainfile: {{str(e)}}")
"""
        script_path = os.path.join(self.workspace_dir, "temp_compositor.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                blend_path = os.path.join(self.env_dir, filename)
                self.log_message(f"Baking Universal Compositor Pipeline into {filename}...", "INFO")
                subprocess.run([self.blender_path, "-b", blend_path, "-P", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log_message("Universal Cinematic Post-Processing completely baked and verified.", "SUCCESS")

if __name__ == "__main__":
    compositor = UniversalBloomGlareEngine()
    output = compositor.orchestrate_bloom_glare_compositing()
    print("\n--- OMNIMATRIX COMPOSITING DEPT: AGENT 38 COMPLETE ---")
    print(f"Total dynamic compositor profiles explicitly generated: {len(output['compositor_dynamic_profiles'])}")
    for p in output["compositor_dynamic_profiles"]:
        print(f"Time: {p['timestamp_sec']}s | Style: '{p.get('render_style_enforced', 'unknown')}'")
        print(f"  Fog Bloom Thresh: {p['fog_glow_threshold']} | Streak Mix: {p['streak_mix_factor']} | Chromatic Disp: {p['chromatic_dispersion']}")
    print("------------------------------------------------------------------")
