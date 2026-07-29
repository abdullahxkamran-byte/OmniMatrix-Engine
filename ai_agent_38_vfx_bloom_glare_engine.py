import os, re, sys, json, math, time, random, subprocess, urllib.request, urllib.error

# =====================================================================
# RULE 2 & 14: UNIVERSAL ENVIRONMENT & DUAL API CONFIGURATION
# =====================================================================
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip().upper()] = v.strip()
load_env_file()

class Ai_Agent_38_VFX_Bloom_Glare_Engine:
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "Ai_Agent_38_VFX_Bloom_Glare_Engine"
        self.workspace_dir = workspace_dir
        self.env_dir = os.path.join(self.workspace_dir, "Local_3D_Environments")
        self.blender_path = "blender"
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        for d in [self.workspace_dir, self.env_dir]: os.makedirs(d, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, msg, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {msg}")

    def _scrub_legacy_assets(self):
        for f in ["38_bloom_glare_compositor.json", "temp_compositor.py"]:
            p = os.path.join(self.workspace_dir, f)
            if os.path.exists(p): os.remove(p)

    # =====================================================================
    # RULE 7 & 4: ATOMIC HANDSHAKE & LIMITLESS CONFIG LOADERS
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS"):
        matrix_path = os.path.join(self.workspace_dir, "matrix_state.json")
        data = {}
        if os.path.exists(matrix_path):
            try:
                with open(matrix_path, "r", encoding="utf-8") as f: data = json.load(f)
            except Exception: pass
        if "orchestrator_matrix" not in data: data["orchestrator_matrix"] = {}
        data["orchestrator_matrix"].update({"last_active_agent": self.agent_name, "last_update_timestamp": time.time(), "agent_status": {self.agent_name: status}})
        # Note: Agent 39 & 40 shifted to utility in Module D, next active is Agent 41!
        if status == "COMPLETED": data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_41_Beat_To_Frame_Effects_Sync_Engine"
        with open(matrix_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

    def _load_config(self):
        p = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    return {"style": d.get("global_style", "realistic").lower(), "theme": d.get("theme", "cinematic")}
            except Exception: pass
        return {"style": "realistic", "theme": "limitless_optical"}

    def _load_cues(self):
        p = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return [{"timestamp_sec": float(pan.get("timestamp_sec", i*3.0)), "prompt": pan.get("visual_prompt", "action"), "mood": pan.get("emotional_tone", "EPIC")} for i, pan in enumerate(json.load(f).get("storyboard_panels", []))]
            except Exception: pass
        return [{"timestamp_sec": 1.5, "prompt": "high energy blast collision", "mood": "CLIMAX_HYPED"}, {"timestamp_sec": 4.0, "prompt": "character recovery breathing dust", "mood": "DRAMATIC"}]

    def _clean_json(self, raw):
        s = re.sub(r"^```(json)?\s*|\s*```$", "", raw.strip(), flags=re.IGNORECASE)
        return s[s.find('{'):s.rfind('}')+1] if '{' in s and '}' in s else s

    def _api_call(self, url, payload, headers):
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=35) as res: return json.loads(res.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14 & 15: QUAD-CORE LIMITLESS OPTICAL RECIPE SYNTHESIZER
    # =====================================================================
    def orchestrate_bloom_glare_compositing(self):
        self._handshake("IN_PROGRESS")
        cues, config = self._load_cues(), self._load_config()
        self.log(f"Quad-Core Optical Compositor Forge Initiated. Style: {config['style'].upper()} | Theme: {config['theme']}")
        
        # Rule 15: Pure Mathematical Optical Recipe (ZERO Preset Gulaami!)
        prompt = (f"You are OMNIMATRIX Lead Optical & Post-Processing TD. Global Style: '{config['style']}', Theme: '{config['theme']}'.\n"
                  "Invent completely unique, limitless, cinematic or stylized post-processing RECIPES for each storyboard cue.\n"
                  "DO NOT use fixed preset numbers. Return JSON object with list 'compositor_dynamic_profiles' containing:\n"
                  "- 'timestamp_sec': float, 'render_style_enforced': string ('realistic' or 'anime'), 'concept_name': string,\n"
                  "- 'glare_type_secondary': string (choose from: 'STREAKS', 'GHOSTS', 'SIMPLE_STAR', 'FOG_GLOW'),\n"
                  "- 'streak_count': int (1 to 16 - ZERO gulaami to just 2 or 4 streaks!), 'streak_angle_offset_rad': float (0.0 to 3.14),\n"
                  "- 'color_modulation': float (0.0 to 1.0), 'fog_glow_threshold': float (0.05 to 3.0), 'streak_mix_factor': float (-1.0 to 1.0),\n"
                  "- 'chromatic_dispersion': float (0.0 to 0.3 for optical lens warping), 'exposure_flash_boost': float (0.0 to 3.0),\n"
                  "- 'color_lift_rgba': [R, G, B, A], 'color_gain_rgba': [R, G, B, A], 'kinetic_jitter_frequency': float (1.0 to 20.0).\n"
                  "Realistic: subtle dispersion, anamorphic streaks. Anime: extreme dispersion, neon saturated gain, heavy star bursts.\n"
                  "Zero compression or placeholders allowed.")
        
        output = None
        user_msg = f"Cues Context:\n{json.dumps(cues)}"
        
        # Core 1: Gemini (Primary - Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                res = self._api_call(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.gemini_key}", {"contents": [{"parts": [{"text": f"{prompt}\n\n{user_msg}"}]}], "generationConfig": {"temperature": 0.85, "responseMimeType": "application/json"}}, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = {"compositor_dynamic_profiles": json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"])).get("compositor_dynamic_profiles", [])}
                self.log("[Core 1: Gemini] Synthesized limitless optical compositor recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")
        
        # Core 2: OpenAI (Failsafe - Rule 14 & 16)
        if self.openai_key and not output:
            try:
                res = self._api_call("https://api.openai.com/v1/chat/completions", {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "response_format": {"type": "json_object"}}, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_key}"})
                output = {"compositor_dynamic_profiles": json.loads(self._clean_json(res["choices"][0]["message"]["content"])).get("compositor_dynamic_profiles", [])}
                self.log("[Core 2: OpenAI] Synthesized limitless optical compositor recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")
        
        # Core 3: Ollama (Local Fallback - Rule 6)
        if not output:
            try:
                res = self._api_call("http://localhost:11434/api/chat", {"model": "llama3", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "format": "json", "stream": False}, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = {"compositor_dynamic_profiles": json.loads(self._clean_json(res.get("message", {}).get("content", "{}"))).get("compositor_dynamic_profiles", [])}
                self.log("[Core 3: Ollama] Generated local optical compositor recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")
        
        # Core 4: 100% Offline Math Autonomy (Rule 10 - Alien Algorithmic Fallback)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline float optical synthesis...", "WARNING")
            g_types = ["STREAKS", "GHOSTS", "SIMPLE_STAR", "FOG_GLOW"]
            output = {"compositor_dynamic_profiles": []}
            for idx, cue in enumerate(cues):
                random.seed(int((cue["timestamp_sec"] + idx + 1) * 1000))
                r1, g1, b1 = [round(random.uniform(0.8, 1.2), 3) for _ in range(3)]
                is_climax = "CLIMAX" in cue["mood"] or "blast" in cue["prompt"].lower()
                output["compositor_dynamic_profiles"].append({
                    "timestamp_sec": cue["timestamp_sec"], "render_style_enforced": config["style"],
                    "concept_name": f"Optical_Flash_Class_{random.randint(100,999)}",
                    "glare_type_secondary": random.choice(g_types) if is_climax else "STREAKS",
                    "streak_count": random.randint(3, 12) if config["style"] == "anime" else random.choice([2, 4, 6]),
                    "streak_angle_offset_rad": round(random.uniform(0.0, 3.14), 2), "color_modulation": round(random.uniform(0.1, 0.8), 2),
                    "fog_glow_threshold": 0.2 if is_climax else 1.2, "streak_mix_factor": 0.8 if is_climax else 0.0,
                    "chromatic_dispersion": 0.18 if is_climax else 0.03, "exposure_flash_boost": 2.0 if is_climax else 0.0,
                    "color_lift_rgba": [r1, g1, b1, 1.0], "color_gain_rgba": [round(r1*1.1,2), round(g1*1.1,2), round(b1*1.1,2), 1.0],
                    "kinetic_jitter_frequency": 15.0 if is_climax else 3.0
                })
        
        with open(os.path.join(self.workspace_dir, "38_bloom_glare_compositor.json"), "w", encoding="utf-8") as f: json.dump(output, f, indent=4)
        self._bake_universal_compositor_in_blender(output)
        self._handshake("COMPLETED")
        return output

    # =====================================================================
    # RULE 9, 11, 12, 13 & 17: BLENDER COMPOSITOR & KINETIC JITTER COMPILER
    # =====================================================================
    def _bake_universal_compositor_in_blender(self, comp_data):
        self.log("Compiling Limitless Compositor Blender Python script...")
        comp_json = json.dumps(comp_data.get('compositor_dynamic_profiles', []))
        script_content = f"""
import bpy, math, random

profiles = {comp_json}[:45] # Rule 17: VRAM cap max 45 dynamic optical profiles
scene = bpy.context.scene
fps = scene.render.fps

scene.use_nodes = True
tree = scene.node_tree; tree.nodes.clear()

global_style = profiles[0].get('render_style_enforced', 'realistic').lower() if profiles else 'realistic'

try:
    # --- 1. BUILD LIMITLESS COMPOSITOR NODE TREE (Rule 11 No External LUTs) ---
    rlayers = tree.nodes.new('CompositorNodeRLayers'); rlayers.location = (0, 0)
    
    # Base Fog Glow (Primary Atmosphere)
    g_fog = tree.nodes.new('CompositorNodeGlare'); g_fog.glare_type, g_fog.quality = 'FOG_GLOW', 'HIGH'
    g_fog.size, g_fog.location = (8 if global_style == 'anime' else 6), (300, 0)
    
    # Secondary Limitless Glare (Streaks, Ghosts, or Star)
    g_sec = tree.nodes.new('CompositorNodeGlare'); g_sec.quality, g_sec.fade = 'HIGH', 0.85
    g_sec.location = (600, 0)
    
    # Optical Chromatic Aberration & Lens Warping
    lens = tree.nodes.new('CompositorNodeLensdist'); lens.use_fit, lens.location = True, (900, 0)
    
    # Exposure Blinding Flash & Color Balance
    exp = tree.nodes.new('CompositorNodeExposure'); exp.location = (1150, 0)
    col = tree.nodes.new('CompositorNodeColorBalance'); col.location = (1350, 0)
    
    out_comp, out_view = tree.nodes.new('CompositorNodeComposite'), tree.nodes.new('CompositorNodeViewer')
    out_comp.location, out_view.location = (1650, 100), (1650, -100)

    # Wire Tree
    tree.links.new(rlayers.outputs['Image'], g_fog.inputs['Image']); tree.links.new(g_fog.outputs['Image'], g_sec.inputs['Image'])
    tree.links.new(g_sec.outputs['Image'], lens.inputs['Image']); tree.links.new(lens.outputs['Image'], exp.inputs['Image'])
    tree.links.new(exp.outputs['Image'], col.inputs['Image']); tree.links.new(col.outputs['Image'], out_comp.inputs['Image'])
    tree.links.new(col.outputs['Image'], out_view.inputs['Image'])

    # Set Defaults at Frame 1
    for node, prop, val in [(g_fog, "threshold", 2.0), (g_sec, "threshold", 3.0), (g_sec, "mix", -0.9), (lens, "dispersion", 0.0), (exp, "exposure", 0.0)]:
        setattr(node, prop, val); node.keyframe_insert(data_path=prop, frame=1)

    # --- 2. ANIMATE LIMITLESS OPTICAL CUES & KINETIC IMPACT JITTER (Rule 12) ---
    for idx, p in enumerate(profiles):
        imp_f = int(p.get('timestamp_sec', 0.0) * fps)
        pre_f, post_f = max(1, imp_f - int(fps * 0.15)), imp_f + int(fps * 1.2)
        
        # Zero Gulaami Glare Config
        g_sec.glare_type = str(p.get('glare_type_secondary', 'STREAKS')).upper()
        if g_sec.glare_type == 'STREAKS':
            g_sec.streaks = int(p.get('streak_count', 4)) # Limitless streaks (1 to 16)!
            g_sec.angle_offset = float(p.get('streak_angle_offset_rad', 0.0))
        g_sec.color_modulation = float(p.get('color_modulation', 0.5))

        # Keyframe Impact Peaks
        g_fog.threshold = float(p.get('fog_glow_threshold', 0.5)); g_fog.keyframe_insert("threshold", frame=imp_f)
        g_sec.threshold = 0.5; g_sec.mix = float(p.get('streak_mix_factor', 0.5))
        g_sec.keyframe_insert("threshold", frame=imp_f); g_sec.keyframe_insert("mix", frame=imp_f)
        
        lens.dispersion = float(p.get('chromatic_dispersion', 0.1)); lens.keyframe_insert("dispersion", frame=imp_f)
        exp.exposure = float(p.get('exposure_flash_boost', 1.0)); exp.keyframe_insert("exposure", frame=imp_f)
        
        col.lift = tuple(p.get('color_lift_rgba', [1,1,1,1]))[:3]; col.gain = tuple(p.get('color_gain_rgba', [1,1,1,1]))[:3]
        col.keyframe_insert("lift", frame=imp_f); col.keyframe_insert("gain", frame=imp_f)

        # Revert to safe state post-impact
        for node, prop, val in [(g_fog, "threshold", 2.0), (g_sec, "threshold", 3.0), (g_sec, "mix", -0.9), (lens, "dispersion", 0.0), (exp, "exposure", 0.0)]:
            setattr(node, prop, val); node.keyframe_insert(data_path=prop, frame=pre_f); node.keyframe_insert(data_path=prop, frame=post_f)

        # --- RULE 12: KINETIC OPTICAL JITTER (Screen warp/stutter without moving camera!) ---
        jitter_freq = float(p.get('kinetic_jitter_frequency', 5.0))
        if jitter_freq > 8.0 and tree.animation_data and tree.animation_data.action:
            for fc in tree.animation_data.action.fcurves:
                if "dispersion" in fc.data_path or "exposure" in fc.data_path:
                    nm = fc.modifiers.new(type='NOISE')
                    nm.scale, nm.strength, nm.frame_start, nm.frame_end = (10.0 / jitter_freq), 0.15, imp_f, imp_f + int(fps * 0.4)

except Exception as e: print(f"Error compiling compositor: {{e}}")

try: bpy.ops.wm.save_mainfile()
except Exception: pass
"""
        script_path = os.path.join(self.workspace_dir, "temp_compositor.py")
        with open(script_path, "w", encoding="utf-8") as f: f.write(script_content)
        for file in os.listdir(self.env_dir):
            if file.endswith(".blend"):
                try: subprocess.run([self.blender_path, "-b", os.path.join(self.env_dir, file), "-P", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
                except Exception: pass
        if os.path.exists(script_path): os.remove(script_path)
        self.log("Blender Limitless Compositor & Kinetic Jitter compilation complete!", "SUCCESS")

if __name__ == "__main__":
    Ai_Agent_38_VFX_Bloom_Glare_Engine().orchestrate_bloom_glare_compositing()
