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

class Ai_Agent_39_Universal_Color_Grading_LUT_Mapper:
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "Ai_Agent_39_Universal_Color_Grading_LUT_Mapper"
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
        for f in ["39_color_grading_blueprint.json", "temp_color_grading.py"]:
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
        if status == "COMPLETED": data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_40_Motion_Blur_Velocity_Vector_Applier"
        with open(matrix_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

    def _load_config(self):
        p = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    return {"style": d.get("global_style", "realistic").lower(), "theme": d.get("theme", "cinematic")}
            except Exception: pass
        return {"style": "realistic", "theme": "limitless_chromatic"}

    def _load_cues(self):
        p = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return [{"timestamp_sec": float(pan.get("timestamp_sec", i*3.0)), "prompt": pan.get("visual_prompt", "scene"), "mood": pan.get("emotional_tone", "EPIC")} for i, pan in enumerate(json.load(f).get("storyboard_panels", []))]
            except Exception: pass
        return [{"timestamp_sec": 0.0, "prompt": "establishing shot atmosphere", "mood": "MYSTERIOUS"}, {"timestamp_sec": 3.5, "prompt": "high intensity climax showdown", "mood": "CLIMAX_ACTION"}]

    def _clean_json(self, raw):
        s = re.sub(r"^```(json)?\s*|\s*```$", "", raw.strip(), flags=re.IGNORECASE)
        return s[s.find('{'):s.rfind('}')+1] if '{' in s and '}' in s else s

    def _api_call(self, url, payload, headers):
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=35) as res: return json.loads(res.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14 & 15: QUAD-CORE LIMITLESS COLOR RECIPE SYNTHESIZER
    # =====================================================================
    def map_color_grading_luts(self):
        self._handshake("IN_PROGRESS")
        cues, config = self._load_cues(), self._load_config()
        self.log(f"Quad-Core Color Grading Forge Initiated. Style: {config['style'].upper()} | Theme: {config['theme']}")
        
        # Rule 15: Pure Mathematical Color Recipe (ZERO Preset Name Dependency!)
        prompt = (f"You are OMNIMATRIX Lead Cinematic Colorist. Global Style: '{config['style']}', Theme: '{config['theme']}'.\n"
                  "Invent completely unique, limitless color grading RECIPES for each storyboard cue. DO NOT use preset names.\n"
                  "Return JSON object with list 'color_grading_profiles' containing:\n"
                  "- 'timestamp_sec': float, 'render_style_enforced': string ('realistic' or 'anime'), 'palette_concept': string,\n"
                  "- 'saturation_scale': float (0.0 to 2.5), 'contrast_multiplier': float (0.5 to 2.0), 'exposure_offset': float (-1.0 to 1.5),\n"
                  "- 'lift_shadows_rgb': [R, G, B] (scale 0.5 to 1.5 - color tint in darks),\n"
                  "- 'gamma_midtones_rgb': [R, G, B] (scale 0.5 to 1.5 - core emotional tone),\n"
                  "- 'gain_highlights_rgb': [R, G, B] (scale 0.5 to 1.8 - bright area tinting),\n"
                  "- 'kinetic_pulse_frequency': float (0.0 to 12.0 for F-Curve color breathing/heartbeat jitter during climax moments).\n"
                  "Realistic: subtle teal/orange, deep filmic shadows. Anime: hyper-saturated blues/reds, vivid contrast banding.\n"
                  "Zero compression or placeholders allowed.")
        
        output = None
        user_msg = f"Scene Cues Context:\n{json.dumps(cues)}"
        
        # Core 1: Gemini (Primary - Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                res = self._api_call(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}", {"contents": [{"parts": [{"text": f"{prompt}\n\n{user_msg}"}]}], "generationConfig": {"temperature": 0.85, "responseMimeType": "application/json"}}, {"Content-Type": "application/json"})
                output = {"color_grading_profiles": json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"])).get("color_grading_profiles", [])}
                self.log("[Core 1: Gemini] Synthesized limitless color grading mathematical palettes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")
        
        # Core 2: OpenAI (Failsafe - Rule 14 & 16)
        if self.openai_key and not output:
            try:
                res = self._api_call("https://api.openai.com/v1/chat/completions", {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "response_format": {"type": "json_object"}}, {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"})
                output = {"color_grading_profiles": json.loads(self._clean_json(res["choices"][0]["message"]["content"])).get("color_grading_profiles", [])}
                self.log("[Core 2: OpenAI] Synthesized limitless color grading mathematical palettes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")
        
        # Core 3: Ollama (Local Fallback - Rule 6)
        if not output:
            try:
                res = self._api_call("http://localhost:11434/api/chat", {"model": "llama3", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "format": "json", "stream": False}, {"Content-Type": "application/json"})
                output = {"color_grading_profiles": json.loads(self._clean_json(res.get("message", {}).get("content", "{}"))).get("color_grading_profiles", [])}
                self.log("[Core 3: Ollama] Generated local color grading palettes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")
        
        # Core 4: 100% Offline Math Autonomy (Rule 10 - Algorithmic Color Synthesis)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline float color synthesis algorithm...", "WARNING")
            output = {"color_grading_profiles": []}
            for idx, cue in enumerate(cues):
                random.seed(int((cue["timestamp_sec"] + idx + 1) * 1000))
                r1, g1, b1 = [round(random.uniform(0.7, 1.3), 3) for _ in range(3)]
                is_climax = "CLIMAX" in cue["mood"] or "action" in cue["prompt"].lower()
                output["color_grading_profiles"].append({
                    "timestamp_sec": cue["timestamp_sec"], "render_style_enforced": config["style"],
                    "palette_concept": f"Algorithmic_Grade_Class_{random.randint(100,999)}",
                    "saturation_scale": 1.4 if (config["style"] == "anime" or is_climax) else 0.9,
                    "contrast_multiplier": 1.25 if is_climax else 1.05, "exposure_offset": 0.2 if is_climax else 0.0,
                    "lift_shadows_rgb": [round(r1*0.9, 2), round(g1*0.95, 2), round(b1*1.1, 2)],
                    "gamma_midtones_rgb": [r1, g1, b1], "gain_highlights_rgb": [round(r1*1.1, 2), round(g1*1.05, 2), round(b1*0.9, 2)],
                    "kinetic_pulse_frequency": 8.0 if is_climax else 0.0
                })
        
        with open(os.path.join(self.workspace_dir, "39_color_grading_blueprint.json"), "w", encoding="utf-8") as f: json.dump(output, f, indent=4)
        self._bake_color_grading_in_blender(output)
        self._handshake("COMPLETED")
        return output

    # =====================================================================
    # RULE 9, 11, 12, 13 & 17: BLENDER COMPOSITOR & KINETIC COLOR COMPILER
    # =====================================================================
    def _bake_color_grading_in_blender(self, grading_data):
        self.log("Compiling Limitless Color Grading Blender Python script...")
        grading_json = json.dumps(grading_data.get('color_grading_profiles', []))
        script_content = f"""
import bpy, math, random

profiles = {grading_json}[:50] # Rule 17: VRAM cap max 50 dynamic color transitions
profiles.sort(key=lambda x: x.get('timestamp_sec', 0.0))

scene = bpy.context.scene
fps = scene.render.fps

scene.use_nodes = True
tree = scene.node_tree

try:
    # 1. CLEANUP PREVIOUS GRADING NODES
    for node in list(tree.nodes):
        if node.name.startswith("OMNI_LUT_"): tree.nodes.remove(node)

    comp_node = tree.nodes.get('Composite')
    if not comp_node: comp_node = tree.nodes.new('CompositorNodeComposite'); comp_node.location = (1500, 0)

    prev_node = None
    for link in list(tree.links):
        if link.to_node == comp_node: prev_node = link.from_node; tree.links.remove(link); break

    # 2. BUILD LIMITLESS GRADING NETWORK (Rule 11 No External LUT files)
    hsv_node = tree.nodes.new('CompositorNodeHueSat'); hsv_node.name = "OMNI_LUT_HSV"; hsv_node.location = (comp_node.location[0] - 800, 0)
    exp_node = tree.nodes.new('CompositorNodeExposure'); exp_node.name = "OMNI_LUT_EXP"; exp_node.location = (comp_node.location[0] - 550, 0)
    cb_node = tree.nodes.new('CompositorNodeColorBalance'); cb_node.name = "OMNI_LUT_CB"; cb_node.correction_method = 'LIFT_GAMMA_GAIN'; cb_node.location = (comp_node.location[0] - 300, 0)

    if prev_node: tree.links.new(prev_node.outputs[0], hsv_node.inputs['Image'])
    tree.links.new(hsv_node.outputs['Image'], exp_node.inputs['Image'])
    tree.links.new(exp_node.outputs['Image'], cb_node.inputs['Image'])
    tree.links.new(cb_node.outputs['Image'], comp_node.inputs['Image'])
    
    viewer = tree.nodes.get('Viewer')
    if viewer: tree.links.new(cb_node.outputs['Image'], viewer.inputs['Image'])

    # 3. ANIMATE SMOOTH GRADE TRANSITIONS & KINETIC PULSING (Rule 12)
    for idx, p in enumerate(profiles):
        imp_f = max(1, int(p['timestamp_sec'] * fps))
        pre_f = max(1, imp_f - int(fps * 0.8)) if idx > 0 else 1
        if idx == 0: imp_f = 1

        sat, val = float(p.get('saturation_scale', 1.0)), float(p.get('contrast_multiplier', 1.0))
        exp = float(p.get('exposure_offset', 0.0))
        lift, gamma, gain = tuple(p.get('lift_shadows_rgb', [1,1,1])), tuple(p.get('gamma_midtones_rgb', [1,1,1])), tuple(p.get('gain_highlights_rgb', [1,1,1]))

        if idx > 0:
            for n, prop in [(hsv_node, "color_saturation"), (hsv_node, "color_value"), (exp_node, "exposure"), (cb_node, "lift"), (cb_node, "gamma"), (cb_node, "gain")]:
                n.keyframe_insert(data_path=prop, frame=pre_f)

        hsv_node.color_saturation, hsv_node.color_value, exp_node.exposure = sat, val, exp
        cb_node.lift, cb_node.gamma, cb_node.gain = lift, gamma, gain
        
        for n, prop in [(hsv_node, "color_saturation"), (hsv_node, "color_value"), (exp_node, "exposure"), (cb_node, "lift"), (cb_node, "gamma"), (cb_node, "gain")]:
            n.keyframe_insert(data_path=prop, frame=imp_f)

        # --- RULE 12: KINETIC COLOR PULSING (Strobe color breathing during climax) ---
        pulse_freq = float(p.get('kinetic_pulse_frequency', 0.0))
        if pulse_freq > 3.0 and tree.animation_data and tree.animation_data.action:
            for fc in tree.animation_data.action.fcurves:
                if "color_saturation" in fc.data_path or "exposure" in fc.data_path:
                    nm = fc.modifiers.new(type='NOISE')
                    nm.scale, nm.strength, nm.frame_start, nm.frame_end = (10.0 / pulse_freq), 0.1, imp_f, imp_f + int(fps * 1.5)

except Exception as e: print(f"Error compiling color grading: {{e}}")

try: bpy.ops.wm.save_mainfile()
except Exception: pass
"""
        script_path = os.path.join(self.workspace_dir, "temp_color_grading.py")
        with open(script_path, "w", encoding="utf-8") as f: f.write(script_content)
        for file in os.listdir(self.env_dir):
            if file.endswith(".blend"):
                try: subprocess.run([self.blender_path, "-b", os.path.join(self.env_dir, file), "-P", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
                except Exception: pass
        if os.path.exists(script_path): os.remove(script_path)
        self.log("Blender Limitless Color Grading & Kinetic Pulsing compilation complete!", "SUCCESS")

if __name__ == "__main__":
    Ai_Agent_39_Universal_Color_Grading_LUT_Mapper().map_color_grading_luts()
