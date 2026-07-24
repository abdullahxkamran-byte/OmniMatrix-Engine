import os, re, sys, json, math, time, random, subprocess, urllib.request, urllib.error

# =====================================================================
# RULE 2 & 14: UNIVERSAL ENVIRONMENT & API CONFIGURATION
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

class Ai_Agent_36_Volumetric_Speed_Lines_Architect:
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "Ai_Agent_36_Volumetric_Speed_Lines_Architect"
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
        for f in ["36_volumetric_speed_lines_blueprint.json", "temp_speed_lines.py"]:
            p = os.path.join(self.workspace_dir, f)
            if os.path.exists(p): os.remove(p)

    # =====================================================================
    # RULE 7 & 4: ATOMIC HANDSHAKE & LIMITLESS CONFIG LOADERS
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS"):
        matrix_path = os.path.join(self.workspace_dir, "orchestrator_matrix.json")
        data = {}
        if os.path.exists(matrix_path):
            try:
                with open(matrix_path, "r", encoding="utf-8") as f: data = json.load(f)
            except Exception: pass
        data.update({"last_active_agent": self.agent_name, "last_update_timestamp": time.time(), "agent_status": {self.agent_name: status}})
        if status == "COMPLETED": data["next_agent"] = "Ai_Agent_37_Stylized_Smoke_Fire_Fluid_Forge"
        with open(matrix_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

    def _load_config(self):
        p = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    return {"style": d.get("global_style", "realistic").lower(), "theme": d.get("theme", "action")}
            except Exception: pass
        return {"style": "realistic", "theme": "kinetic_velocity"}

    def _load_velocities(self):
        p = os.path.join(self.workspace_dir, "26_kinetic_rig_puppeteer_blueprint.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return [{"timestamp_sec": float(s.get("timestamp_sec", 0.0)), "pose_name": s.get("action_pose_name", "dash"), "velocity_vector": s.get("translation_offset", [0.0, 15.0, 0.0])} for s in json.load(f).get("rig_animation_sequences", [])]
            except Exception: pass
        return [{"timestamp_sec": 1.0, "pose_name": "sonic_boost", "velocity_vector": [0.0, 25.0, 0.0]}, {"timestamp_sec": 3.5, "pose_name": "vertical_clash", "velocity_vector": [0.0, 5.0, -30.0]}]

    def _clean_json(self, raw):
        s = re.sub(r"^```(json)?\s*|\s*```$", "", raw.strip(), flags=re.IGNORECASE)
        return s[s.find('{'):s.rfind('}')+1] if '{' in s and '}' in s else s

    def _api_call(self, url, payload, headers):
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=35) as res: return json.loads(res.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14 & 15: QUAD-CORE LIMITLESS VELOCITY RECIPE SYNTHESIZER
    # =====================================================================
    def design_volumetric_speed_lines(self):
        self._handshake("IN_PROGRESS")
        vels, config = self._load_velocities(), self._load_config()
        self.log(f"Quad-Core Speed Lines Forge Initiated. Style: {config['style'].upper()} | Theme: {config['theme']}")
        
        # Rule 15: Pure Mathematical Velocity Recipe (ZERO Hardcoded shape gulaami!)
        prompt = (f"You are OMNIMATRIX VFX Velocity Director. Global Style: '{config['style']}', Theme: '{config['theme']}'.\n"
                  "Invent completely unique, limitless 3D volumetric speed line RECIPES for each kinetic vector. DO NOT touch camera animation.\n"
                  "DO NOT use preset shape names. Return JSON object with list 'speed_line_profiles' containing:\n"
                  "- 'timestamp_sec': float, 'render_style_enforced': string ('realistic' or 'anime'), 'concept_name': string,\n"
                  "- 'geometry_primitive': string (choose from: 'cylinder_tunnel', 'cone_frustum', 'plane_array', 'sphere_wrapper'),\n"
                  "- 'shader_pattern_math': string (choose from: 'voronoi_streaks', 'noise_smear', 'wave_distortion', 'magic_radial'),\n"
                  "- 'color_ramp_interpolation': string ('EASE' for soft optical blur, 'CONSTANT' for sharp toon manga banding),\n"
                  "- 'line_density_scale': float (10-100), 'line_length_meters': float (10-60), 'scroll_velocity_multiplier': float (10-50),\n"
                  "- 'opacity_alpha': float (0.1-1.0), 'emission_strength': float (2.0-150.0),\n"
                  "- 'color_primary_rgba': [R, G, B, A], 'color_secondary_rgba': [R, G, B, A],\n"
                  "- 'radial_rotation_euler_xyz': [X_rad, Y_rad, Z_rad] (camera frustum alignment angle).\n"
                  "Zero compression or placeholders allowed.")
        
        output = None
        user_msg = f"Kinetic Vectors Context:\n{json.dumps(vels)}"
        
        # Core 1: Gemini (Primary - Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                res = self._api_call(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}", {"contents": [{"parts": [{"text": f"{prompt}\n\n{user_msg}"}]}], "generationConfig": {"temperature": 0.85, "responseMimeType": "application/json"}}, {"Content-Type": "application/json"})
                output = {"speed_line_profiles": json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"])).get("speed_line_profiles", [])}
                self.log("[Core 1: Gemini] Synthesized limitless speed line recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")
        
        # Core 2: OpenAI (Failsafe - Rule 14 & 16)
        if self.openai_key and not output:
            try:
                res = self._api_call("https://api.openai.com/v1/chat/completions", {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "response_format": {"type": "json_object"}}, {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"})
                output = {"speed_line_profiles": json.loads(self._clean_json(res["choices"][0]["message"]["content"])).get("speed_line_profiles", [])}
                self.log("[Core 2: OpenAI] Synthesized limitless speed line recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")
        
        # Core 3: Ollama (Local Fallback - Rule 6)
        if not output:
            try:
                res = self._api_call("http://localhost:11434/api/chat", {"model": "llama3", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "format": "json", "stream": False}, {"Content-Type": "application/json"})
                output = {"speed_line_profiles": json.loads(self._clean_json(res.get("message", {}).get("content", "{}"))).get("speed_line_profiles", [])}
                self.log("[Core 3: Ollama] Generated local speed line recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")
        
        # Core 4: 100% Offline Math Autonomy (Rule 10 - Alien Algorithmic Fallback)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline float velocity synthesis algorithm...", "WARNING")
            prims, patterns = ["cylinder_tunnel", "cone_frustum", "plane_array", "sphere_wrapper"], ["voronoi_streaks", "noise_smear", "wave_distortion", "magic_radial"]
            output = {"speed_line_profiles": []}
            for idx, v in enumerate(vels):
                random.seed(int((v["timestamp_sec"] + idx + 1) * 1000))
                r1, g1, b1 = [round(random.uniform(0.5, 1.0), 3) for _ in range(3)]
                spd = max(abs(x) for x in v["velocity_vector"]) or 15.0
                output["speed_line_profiles"].append({
                    "timestamp_sec": v["timestamp_sec"], "render_style_enforced": config["style"],
                    "concept_name": f"Velocity_Tunnel_Class_{random.randint(100,999)}",
                    "geometry_primitive": random.choice(prims), "shader_pattern_math": random.choice(patterns),
                    "color_ramp_interpolation": "CONSTANT" if config["style"] == "anime" else "EASE",
                    "line_density_scale": round(spd * 2.0, 1), "line_length_meters": round(spd * 1.5, 1),
                    "scroll_velocity_multiplier": round(spd * 1.2, 1), "opacity_alpha": 1.0 if config["style"] == "anime" else 0.6,
                    "emission_strength": round(spd * 3.0, 1), "color_primary_rgba": [r1, g1, b1, 1.0],
                    "color_secondary_rgba": [0.0, 0.0, 0.0, 0.0], "radial_rotation_euler_xyz": [1.57, 0.0, 0.0]
                })
        
        with open(os.path.join(self.workspace_dir, "36_volumetric_speed_lines_blueprint.json"), "w", encoding="utf-8") as f: json.dump(output, f, indent=4)
        self._bake_speed_lines_in_blender(output)
        self._handshake("COMPLETED")
        return output

    # =====================================================================
    # RULE 9, 11, 12, 13 & 17: BLENDER RECIPE EVALUATOR & COMPILER
    # =====================================================================
    def _bake_speed_lines_in_blender(self, lines_data):
        self.log("Compiling Limitless Speed Lines Blender Python script...")
        lines_json = json.dumps(lines_data.get('speed_line_profiles', []))
        script_content = f"""
import bpy, math, random

profiles = {lines_json}[:40] # Rule 17: VRAM cap max 40 velocity sequences
scene = bpy.context.scene
fps = scene.render.fps

bpy.ops.object.select_all(action='DESELECT')
for obj in scene.objects:
    if obj.name.startswith("OMNIMATRIX_VFX_SpeedLines_"):
        obj.select_set(True)
bpy.ops.object.delete()

scene.render.engine = 'BLENDER_EEVEE'
cam = scene.camera
if not cam:
    bpy.ops.object.camera_add(location=(0, -10, 2), rotation=(math.radians(90), 0, 0))
    cam = bpy.context.active_object; scene.camera = cam

for idx, p in enumerate(profiles):
    try:
        c_name, style = str(p.get('concept_name', f'Speed_{{idx}}')), str(p.get('render_style_enforced', 'realistic')).lower()
        prim, pattern = str(p.get('geometry_primitive', 'cylinder_tunnel')).lower(), str(p.get('shader_pattern_math', 'voronoi_streaks')).lower()
        interp, density = str(p.get('color_ramp_interpolation', 'EASE')).upper(), float(p.get('line_density_scale', 40))
        length, scroll_spd = float(p.get('line_length_meters', 25)), float(p.get('scroll_velocity_multiplier', 20))
        alpha, emit_str = float(p.get('opacity_alpha', 0.8)), float(p.get('emission_strength', 10))
        c1 = tuple(p.get('color_primary_rgba', [1,1,1,1]))[:3] + (1.0,)
        rot_rad = tuple(p.get('radial_rotation_euler_xyz', [1.57, 0.0, 0.0]))
        spawn_frame = int(p.get('timestamp_sec', 0.0) * fps)
        dur_frames = min(int(fps * 2.0), 120) # Rule 17: Cap animation duration

        # 1. DYNAMIC VELOCITY GEOMETRY EVALUATOR (Zero Hardcoded Preset Gulaami!)
        if 'cone' in prim: bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=length/3, radius2=length/10, depth=length, location=(0,0,-length/2))
        elif 'plane' in prim or 'array' in prim: bpy.ops.mesh.primitive_plane_add(size=length, location=(0,0,-5))
        elif 'sphere' in prim: bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=length/3, location=(0,0,-length/2))
        else: bpy.ops.mesh.primitive_cylinder_add(vertices=48 if style=='realistic' else 24, radius=length/4, depth=length, location=(0,0,-length/2))
        
        obj = bpy.context.active_object
        obj.name, obj.rotation_euler = f"OMNIMATRIX_VFX_SpeedLines_{{c_name}}_{{idx}}", rot_rad
        bpy.ops.object.shade_smooth()

        # Rule 13 & 12: Parent to Camera Frustum without touching Camera Animation!
        obj.parent = cam
        obj.matrix_parent_inverse = cam.matrix_world.inverted()

        # Rule 11 & 4: PROCEDURAL VELOCITY SHADER BUILDER (No External Textures)
        mat = bpy.data.materials.new(name=f"MAT_{{obj.name}}")
        mat.use_nodes, mat.blend_method, mat.shadow_method = True, 'BLEND', 'NONE'
        nt = mat.node_tree; nt.nodes.clear()
        
        out, emit = nt.nodes.new('ShaderNodeOutputMaterial'), nt.nodes.new('ShaderNodeEmission')
        trans, mix = nt.nodes.new('ShaderNodeBsdfTransparent'), nt.nodes.new('ShaderNodeMixShader')
        emit.inputs['Color'].default_value, emit.inputs['Strength'].default_value = c1, emit_str

        tex_coord, mapping = nt.nodes.new('ShaderNodeTexCoord'), nt.nodes.new('ShaderNodeMapping')
        mapping.inputs['Scale'].default_value = (density / 5.0, 0.05, 1.0)
        
        # Dynamically Select Math Pattern
        if 'noise' in pattern: tex = nt.nodes.new('ShaderNodeTexNoise')
        elif 'wave' in pattern: tex = nt.nodes.new('ShaderNodeTexWave')
        elif 'magic' in pattern: tex = nt.nodes.new('ShaderNodeTexMagic')
        else: tex = nt.nodes.new('ShaderNodeTexVoronoi'); tex.feature = 'F1'
        
        ramp = nt.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.interpolation = 'CONSTANT' if style == 'anime' or interp == 'CONSTANT' else 'EASE'
        ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.45, (0,0,0,1)
        ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.52, (1,1,1,alpha)

        nt.links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
        nt.links.new(mapping.outputs['Vector'], tex.inputs['Vector'])
        out_sock = tex.outputs['Distance'] if 'Distance' in tex.outputs else tex.outputs['Color']
        nt.links.new(out_sock, ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], mix.inputs['Fac'])
        nt.links.new(trans.outputs['BSDF'], mix.inputs[1]); nt.links.new(emit.outputs['Emission'], mix.inputs[2])
        nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
        obj.data.materials.append(mat)

        # 3. KINETIC VELOCITY SCROLLING (Animate UV Mapping Location, NOT Camera!)
        for f, val in [(max(1, spawn_frame-1), True), (spawn_frame, False), (spawn_frame + dur_frames, True)]:
            obj.hide_viewport = obj.hide_render = val
            obj.keyframe_insert("hide_viewport", frame=f); obj.keyframe_insert("hide_render", frame=f)

        mapping.inputs['Location'].default_value[2] = 0.0
        mapping.inputs['Location'].keyframe_insert("default_value", index=2, frame=spawn_frame)
        mapping.inputs['Location'].default_value[2] = scroll_spd * 5.0
        mapping.inputs['Location'].keyframe_insert("default_value", index=2, frame=spawn_frame + dur_frames)
    except Exception as e: print(f"Error on speed line {{idx}}: {{e}}")

try: bpy.ops.wm.save_mainfile()
except Exception: pass
"""
        script_path = os.path.join(self.workspace_dir, "temp_speed_lines.py")
        with open(script_path, "w", encoding="utf-8") as f: f.write(script_content)
        for file in os.listdir(self.env_dir):
            if file.endswith(".blend"):
                try: subprocess.run([self.blender_path, "-b", os.path.join(self.env_dir, file), "-P", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
                except Exception: pass
        if os.path.exists(script_path): os.remove(script_path)
        self.log("Blender Limitless Speed Lines compilation complete!", "SUCCESS")

if __name__ == "__main__":
    Ai_Agent_36_Volumetric_Speed_Lines_Architect().design_volumetric_speed_lines()
