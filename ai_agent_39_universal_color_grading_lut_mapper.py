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

class Ai_Agent_39_Universal_Color_Grading_LUT_Mapper:
    """
    OMNIMATRIX V2.0 AI UTILITY: HYBRID COLOR GRADING ENGINE
    Operates as a high-speed deterministic mathematical colorist by default,
    with an embedded Generative AI core for synthesizing complex alien color vectors.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "Ai_Agent_39_Universal_Color_Grading_LUT_Mapper"
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
        """Rule 3: Idempotency scrubbing of previous color grading maps and temporary scripts."""
        for filename in ["39_color_grading_blueprint.json", "temp_color_grading.py"]:
            file_path = os.path.join(self.workspace_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    self.log(f"Failed to scrub legacy file {file_path}: {e}", "WARNING")

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
            # Hand off to Agent 40 (Pure Non-AI Utility for Motion Blur & Velocity Vectors)
            data["orchestrator_matrix"]["next_agent"] = "Agent_40_Motion_Blur_Velocity_Vector_Applier"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.log(f"Atomic handshake sync error: {e}", "ERROR")

    def _load_config(self):
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {
                        "style": data.get("global_style", "realistic").lower(),
                        "theme": data.get("theme", "cinematic")
                    }
            except Exception:
                pass
        return {"style": "realistic", "theme": "limitless_chromatic"}

    def _load_storyboard_cues(self):
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [
                        {
                            "timestamp_sec": float(panel.get("timestamp_sec", index * 3.0)),
                            "prompt": panel.get("visual_prompt", "scene atmosphere"),
                            "mood": panel.get("emotional_tone", "EPIC"),
                            "requires_ai_synthesis": panel.get("complex_color_override", False)
                        }
                        for index, panel in enumerate(data.get("storyboard_panels", []))
                    ]
            except Exception:
                pass
        return [
            {"timestamp_sec": 0.0, "prompt": "establishing shot atmosphere", "mood": "MYSTERIOUS", "requires_ai_synthesis": False},
            {"timestamp_sec": 3.5, "prompt": "high intensity climax showdown", "mood": "CLIMAX_ACTION", "requires_ai_synthesis": True}
        ]

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
    # RULE 6, 14, 15: HYBRID AI UTILITY COLOR PALETTE SYNTHESIZER
    # =====================================================================
    def execute_color_utility(self):
        self._handshake("IN_PROGRESS")
        cues = self._load_storyboard_cues()
        config = self._load_config()
        self.log(f"AI Utility Color Grading Forge Initiated. Style: {config['style'].upper()} | Theme: {config['theme']}")
        
        output_profiles = []
        cues_needing_ai = []
        
        # 1. FAST DETERMINISTIC MATH PATH (80% Utility Efficiency)
        for index, cue in enumerate(cues):
            is_climax = "CLIMAX" in cue["mood"].upper() or "action" in cue["prompt"].lower()
            is_complex_alien = "alien" in cue["prompt"].lower() or "void" in cue["prompt"].lower() or cue.get("requires_ai_synthesis", False)
            
            if is_complex_alien:
                cues_needing_ai.append(cue)
                continue
                
            # Instant mathematical synthesis without cloud latency
            random.seed(int((cue["timestamp_sec"] + index + 1) * 1000))
            r_base, g_base, b_base = [round(random.uniform(0.8, 1.2), 3) for _ in range(3)]
            
            if config["style"] == "anime":
                sat_val = 1.35 if is_climax else 1.15
                con_val = 1.25 if is_climax else 1.1
                lift_rgb = [round(r_base * 0.95, 3), round(g_base * 0.9, 3), round(b_base * 1.1, 3)]
                gain_rgb = [round(r_base * 1.15, 3), round(g_base * 1.05, 3), round(b_base * 0.95, 3)]
            else:
                sat_val = 1.1 if is_climax else 0.95
                con_val = 1.15 if is_climax else 1.02
                lift_rgb = [round(r_base * 0.9, 3), round(g_base * 0.95, 3), round(b_base * 1.05, 3)]
                gain_rgb = [round(r_base * 1.08, 3), round(g_base * 1.02, 3), round(b_base * 0.92, 3)]

            output_profiles.append({
                "timestamp_sec": cue["timestamp_sec"],
                "render_style_enforced": config["style"],
                "palette_concept": f"Deterministic_Math_Grade_{index}",
                "saturation_scale": sat_val,
                "contrast_multiplier": con_val,
                "exposure_offset": 0.2 if is_climax else 0.0,
                "lift_shadows_rgb": lift_rgb,
                "gamma_midtones_rgb": [r_base, g_base, b_base],
                "gain_highlights_rgb": gain_rgb,
                "kinetic_pulse_frequency": 10.0 if is_climax else 0.0
            })

        # 2. GENERATIVE AI PATH (20% Complex Synthesis - Quad-Core Failsafe)
        if cues_needing_ai:
            self.log(f"Complex color override detected for {len(cues_needing_ai)} cues. Engaging Generative LLM Cores...", "STATUS")
            ai_profiles = self._synthesize_ai_palettes(cues_needing_ai, config)
            output_profiles.extend(ai_profiles)
            
        # Sort by timeline sequence
        output_profiles.sort(key=lambda x: x.get("timestamp_sec", 0.0))
        final_blueprint = {"color_grading_profiles": output_profiles}
        
        blueprint_path = os.path.join(self.workspace_dir, "39_color_grading_blueprint.json")
        with open(blueprint_path, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=4)
            
        self._bake_color_grading_in_blender(final_blueprint)
        self._handshake("COMPLETED")
        return final_blueprint

    def _synthesize_ai_palettes(self, cues_list, config):
        """Rule 15: Limitless floating RGB vector generation via Generative AI."""
        prompt = (
            f"You are OMNIMATRIX Lead Cinematic Colorist. Global Style: '{config['style']}', Theme: '{config['theme']}'.\n"
            "Invent completely unique, limitless mathematical color grading RECIPES for each provided storyboard cue.\n"
            "DO NOT use preset names. Return a JSON object with list 'color_grading_profiles' containing:\n"
            "- 'timestamp_sec': float, 'render_style_enforced': string ('realistic' or 'anime'), 'palette_concept': string,\n"
            "- 'saturation_scale': float (0.0 to 2.5), 'contrast_multiplier': float (0.5 to 2.0), 'exposure_offset': float (-1.0 to 1.5),\n"
            "- 'lift_shadows_rgb': [R, G, B] (scale 0.5 to 1.5 - color tint in dark areas),\n"
            "- 'gamma_midtones_rgb': [R, G, B] (scale 0.5 to 1.5 - core emotional tone),\n"
            "- 'gain_highlights_rgb': [R, G, B] (scale 0.5 to 1.8 - bright area tinting),\n"
            "- 'kinetic_pulse_frequency': float (0.0 to 12.0 for F-Curve color breathing jitter during action climaxes).\n"
            "Zero compression or placeholders allowed."
        )
        user_msg = f"Complex Cues Context:\n{json.dumps(cues_list)}"
        output = None

        # Core 1: Gemini (Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"{prompt}\n\n{user_msg}"}]}],
                    "generationConfig": {"temperature": 0.88, "responseMimeType": "application/json"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"])).get("color_grading_profiles", [])
                self.log("[Core 1: Gemini] Synthesized generative color palettes!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")

        # Core 2: OpenAI (Rule 14 & 16)
        if self.openai_key and not output:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                    "response_format": {"type": "json_object"}
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_key}"})
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"])).get("color_grading_profiles", [])
                self.log("[Core 2: OpenAI] Synthesized generative color palettes!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")

        # Core 3: Ollama Local Fallback
        if not output:
            try:
                url = "http://localhost:11434/api/chat"
                payload = {
                    "model": "llama3",
                    "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
                    "format": "json",
                    "stream": False
                }
                res = self._api_call(url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res.get("message", {}).get("content", "{}"))).get("color_grading_profiles", [])
                self.log("[Core 3: Ollama] Generated local color palettes!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: Algorithmic Math Fallback
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline float color synthesis for complex cues...", "WARNING")
            output = []
            for index, cue in enumerate(cues_list):
                random.seed(int((cue["timestamp_sec"] + index + 99) * 1000))
                r, g, b = [round(random.uniform(0.6, 1.4), 3) for _ in range(3)]
                output.append({
                    "timestamp_sec": cue["timestamp_sec"],
                    "render_style_enforced": config["style"],
                    "palette_concept": f"Offline_Math_Fallback_{index}",
                    "saturation_scale": 1.4 if config["style"] == "anime" else 0.9,
                    "contrast_multiplier": 1.2,
                    "exposure_offset": 0.1,
                    "lift_shadows_rgb": [round(r * 0.9, 2), round(g * 0.95, 2), round(b * 1.1, 2)],
                    "gamma_midtones_rgb": [r, g, b],
                    "gain_highlights_rgb": [round(r * 1.1, 2), round(g * 1.05, 2), round(b * 0.9, 2)],
                    "kinetic_pulse_frequency": 8.0 if "CLIMAX" in cue["mood"].upper() else 0.0
                })
        return output

    # =====================================================================
    # RULE 9, 11, 12, 17: ACTIONABLE BLENDER PYTHON COMPOSITOR COMPILER
    # =====================================================================
    def _bake_color_grading_in_blender(self, grading_data):
        self.log("Compiling Limitless Color Grading Blender Python script...")
        grading_json = json.dumps(grading_data.get('color_grading_profiles', []))
        
        script_content = f"""
import bpy
import math
import random

# Rule 17: VRAM safety cap - process maximum 50 color grading transitions
profiles = {grading_json}[:50]
profiles.sort(key=lambda x: x.get('timestamp_sec', 0.0))

scene = bpy.context.scene
fps = scene.render.fps

scene.use_nodes = True
tree = scene.node_tree

try:
    # 1. Clean legacy color grading nodes
    for node in list(tree.nodes):
        if node.name.startswith("OMNI_LUT_"):
            tree.nodes.remove(node)

    comp_node = tree.nodes.get('Composite')
    if not comp_node:
        comp_node = tree.nodes.new('CompositorNodeComposite')
        comp_node.location = (1500, 0)

    previous_node = None
    for link in list(tree.links):
        if link.to_node == comp_node:
            previous_node = link.from_node
            tree.links.remove(link)
            break

    # 2. Build mathematical color grading network (Rule 11: No external LUT files)
    hsv_node = tree.nodes.new('CompositorNodeHueSat')
    hsv_node.name = "OMNI_LUT_HSV"
    hsv_node.location = (comp_node.location[0] - 800, 0)
    
    exp_node = tree.nodes.new('CompositorNodeExposure')
    exp_node.name = "OMNI_LUT_EXP"
    exp_node.location = (comp_node.location[0] - 550, 0)
    
    cb_node = tree.nodes.new('CompositorNodeColorBalance')
    cb_node.name = "OMNI_LUT_CB"
    cb_node.correction_method = 'LIFT_GAMMA_GAIN'
    cb_node.location = (comp_node.location[0] - 300, 0)

    if previous_node:
        tree.links.new(previous_node.outputs[0], hsv_node.inputs['Image'])
    tree.links.new(hsv_node.outputs['Image'], exp_node.inputs['Image'])
    tree.links.new(exp_node.outputs['Image'], cb_node.inputs['Image'])
    tree.links.new(cb_node.outputs['Image'], comp_node.inputs['Image'])
    
    viewer = tree.nodes.get('Viewer')
    if viewer:
        tree.links.new(cb_node.outputs['Image'], viewer.inputs['Image'])

    # 3. Animate color transitions and inject kinetic pulsing (Rule 12)
    for index, profile in enumerate(profiles):
        impact_frame = max(1, int(profile['timestamp_sec'] * fps))
        pre_frame = max(1, impact_frame - int(fps * 0.8)) if index > 0 else 1
        if index == 0:
            impact_frame = 1

        sat_val = float(profile.get('saturation_scale', 1.0))
        con_val = float(profile.get('contrast_multiplier', 1.0))
        exp_val = float(profile.get('exposure_offset', 0.0))
        lift_rgb = tuple(profile.get('lift_shadows_rgb', [1.0, 1.0, 1.0]))
        gamma_rgb = tuple(profile.get('gamma_midtones_rgb', [1.0, 1.0, 1.0]))
        gain_rgb = tuple(profile.get('gain_highlights_rgb', [1.0, 1.0, 1.0]))

        if index > 0:
            for node, prop in [(hsv_node, "color_saturation"), (hsv_node, "color_value"), (exp_node, "exposure"), (cb_node, "lift"), (cb_node, "gamma"), (cb_node, "gain")]:
                node.keyframe_insert(data_path=prop, frame=pre_frame)

        hsv_node.color_saturation = sat_val
        hsv_node.color_value = con_val
        exp_node.exposure = exp_val
        cb_node.lift = lift_rgb
        cb_node.gamma = gamma_rgb
        cb_node.gain = gain_rgb
        
        for node, prop in [(hsv_node, "color_saturation"), (hsv_node, "color_value"), (exp_node, "exposure"), (cb_node, "lift"), (cb_node, "gamma"), (cb_node, "gain")]:
            node.keyframe_insert(data_path=prop, frame=impact_frame)

        # Rule 12: Kinetic Color Pulsing (Strobe color breathing during action climax)
        pulse_frequency = float(profile.get('kinetic_pulse_frequency', 0.0))
        if pulse_frequency > 3.0 and tree.animation_data and tree.animation_data.action:
            for fcurve in tree.animation_data.action.fcurves:
                if "color_saturation" in fcurve.data_path or "exposure" in fcurve.data_path:
                    noise_mod = fcurve.modifiers.new(type='NOISE')
                    noise_mod.scale = 10.0 / pulse_frequency
                    noise_mod.strength = 0.1
                    noise_mod.frame_start = impact_frame
                    noise_mod.frame_end = impact_frame + int(fps * 1.5)

except Exception as e:
    print(f"Error compiling compositor color grading: {{e}}")

try:
    bpy.ops.wm.save_mainfile()
except Exception:
    pass
"""
        script_path = os.path.join(self.workspace_dir, "temp_color_grading.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                try:
                    subprocess.run([self.blender_path, "-b", os.path.join(self.env_dir, filename), "-P", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
                except Exception as e:
                    self.log(f"Blender execution warning on {filename}: {e}", "WARNING")
                    
        if os.path.exists(script_path):
            os.remove(script_path)
        self.log("Blender AI Utility Color Grading compilation complete!", "SUCCESS")

if __name__ == "__main__":
    mapper = Ai_Agent_39_Universal_Color_Grading_LUT_Mapper()
    mapper.execute_color_utility()
