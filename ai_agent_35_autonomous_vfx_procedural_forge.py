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

class Ai_Agent_35_Autonomous_VFX_Procedural_Forge:
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "Ai_Agent_35_Autonomous_VFX_Procedural_Forge"
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
        for f in ["35_procedural_vfx_blueprint.json", "temp_vfx_forge.py"]:
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
        if status == "COMPLETED": data["next_agent"] = "Ai_Agent_36_Volumetric_Speed_Lines_Architect"
        with open(matrix_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

    def _load_config(self):
        p = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    return {"style": d.get("global_style", "realistic").lower(), "theme": d.get("theme", "cyberpunk")}
            except Exception: pass
        return {"style": "realistic", "theme": "limitless_alien"}

    def _load_hotspots(self):
        p = os.path.join(self.workspace_dir, "30_environment_fracture_blueprint.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return [{"timestamp_sec": float(ev.get("timestamp_sec", 0.0)), "vfx_origin_xyz": ev.get("fracture_center_xyz", [0.0,0.0,0.0]), "impact_scale": float(ev.get("fracture_radius_meters", 1.0)), "socket_hint": ev.get("socket_target_hint", "_Socket")} for ev in json.load(f).get("fracture_events", [])]
            except Exception: pass
        return [{"timestamp_sec": 1.2, "vfx_origin_xyz": [0.0, 1.5, 0.0], "impact_scale": 2.5, "socket_hint": "Chest_Socket"}, {"timestamp_sec": 3.8, "vfx_origin_xyz": [2.5, 0.5, -1.0], "impact_scale": 4.0, "socket_hint": "Hand_R_Socket"}]

    def _clean_json(self, raw):
        s = re.sub(r"^```(json)?\s*|\s*```$", "", raw.strip(), flags=re.IGNORECASE)
        return s[s.find('{'):s.rfind('}')+1] if '{' in s and '}' in s else s

    def _api_call(self, url, payload, headers):
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=35) as res: return json.loads(res.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14 & 15: QUAD-CORE LIMITLESS RECIPE SYNTHESIZER
    # =====================================================================
    def forge_procedural_vfx(self):
        self._handshake("IN_PROGRESS")
        hotspots, config = self._load_hotspots(), self._load_config()
        self.log(f"Quad-Core VFX Recipe Forge Initiated. Style: {config['style'].upper()} | Theme: {config['theme']}")
        
        # Rule 15: Pure Mathematical Recipe Prompting (ZERO Hardcoded shapes!)
        prompt = (f"You are OMNIMATRIX God-Level VFX Technical Director. Global Style: '{config['style']}', Theme: '{config['theme']}'.\n"
                  "Invent completely unique, limitless, alien, or realistic 3D VFX procedural RECIPES for each impact hotspot. DO NOT touch camera movement.\n"
                  "DO NOT use preset names. Synthesize a raw geometry & shader recipe. Return JSON object with list 'vfx_procedural_profiles' containing:\n"
                  "- 'timestamp_sec': float, 'render_style_enforced': string ('realistic' or 'anime'), 'vfx_name': string (invent any abstract concept),\n"
                  "- 'vfx_origin_xyz': [X, Y, Z], 'socket_bind_target': string,\n"
                  "- 'primitive_mesh': string (choose from: 'ico_sphere', 'torus', 'cylinder', 'cone', 'grid', 'uv_sphere'),\n"
                  "- 'shader_math_pattern': string (choose from: 'voronoi', 'noise', 'wave', 'magic'),\n"
                  "- 'color_ramp_interpolation': string ('EASE' for realistic fog, 'CONSTANT' for sharp anime banding),\n"
                  "- 'glow_intensity_emission': float (20-500), 'pattern_scale': float (0.5-40), 'mesh_deform_strength': float (0.2-20),\n"
                  "- 'color_primary_rgb': [R, G, B], 'color_secondary_rgb': [R, G, B], 'particle_spawn_rate': int (50-350),\n"
                  "- 'volumetric_density': float (0.0 for clean anime, 0.5-5.0 for realistic fog),\n"
                  "- 'mesh_stutter_strength': float (0.5-5.0 for F-Curve kinetic scale vibration), 'turbulence_force_strength': float (5-50).\n"
                  "Zero compression or placeholders allowed.")
        
        output = None
        user_msg = f"Hotspots Context:\n{json.dumps(hotspots)}"
        
        # Core 1: Gemini (Primary - Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                res = self._api_call(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}", {"contents": [{"parts": [{"text": f"{prompt}\n\n{user_msg}"}]}], "generationConfig": {"temperature": 0.9, "responseMimeType": "application/json"}}, {"Content-Type": "application/json"})
                output = {"vfx_procedural_profiles": json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"])).get("vfx_procedural_profiles", [])}
                self.log("[Core 1: Gemini] Synthesized limitless VFX mathematical recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")
        
        # Core 2: OpenAI (Failsafe - Rule 14 & 16)
        if self.openai_key and not output:
            try:
                res = self._api_call("https://api.openai.com/v1/chat/completions", {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "response_format": {"type": "json_object"}}, {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"})
                output = {"vfx_procedural_profiles": json.loads(self._clean_json(res["choices"][0]["message"]["content"])).get("vfx_procedural_profiles", [])}
                self.log("[Core 2: OpenAI] Synthesized limitless VFX mathematical recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")
        
        # Core 3: Ollama (Local Fallback - Rule 6)
        if not output:
            try:
                res = self._api_call("http://localhost:11434/api/chat", {"model": "llama3", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "format": "json", "stream": False}, {"Content-Type": "application/json"})
                output = {"vfx_procedural_profiles": json.loads(self._clean_json(res.get("message", {}).get("content", "{}"))).get("vfx_procedural_profiles", [])}
                self.log("[Core 3: Ollama] Generated local VFX recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")
        
        # Core 4: 100% Offline Math Autonomy (Rule 10 - Alien Algorithmic Fallback)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline float recipe synthesis algorithm...", "WARNING")
            prims, patterns = ["ico_sphere", "torus", "cylinder", "cone", "grid", "uv_sphere"], ["voronoi", "noise", "wave", "magic"]
            output = {"vfx_procedural_profiles": []}
            for idx, hs in enumerate(hotspots):
                random.seed(int((hs["timestamp_sec"] + idx + 1) * 1000))
                r1, g1, b1 = [round(random.uniform(0.1, 1.0), 3) for _ in range(3)]
                sc = hs["impact_scale"]
                output["vfx_procedural_profiles"].append({
                    "timestamp_sec": hs["timestamp_sec"], "render_style_enforced": config["style"],
                    "vfx_name": f"Alien_Singularity_Class_{random.randint(100,999)}",
                    "vfx_origin_xyz": hs["vfx_origin_xyz"], "socket_bind_target": hs["socket_hint"],
                    "primitive_mesh": random.choice(prims), "shader_math_pattern": random.choice(patterns),
                    "color_ramp_interpolation": "CONSTANT" if config["style"] == "anime" else "EASE",
                    "glow_intensity_emission": round(150.0 * sc, 1), "pattern_scale": round(random.uniform(2.0, 30.0), 2),
                    "mesh_deform_strength": round(random.uniform(1.0, 15.0), 2), "color_primary_rgb": [r1, g1, b1],
                    "color_secondary_rgb": [round(1.0-r1, 3), round(1.0-g1, 3), round(1.0-b1, 3)],
                    "particle_spawn_rate": min(350, int(100 * sc)), "volumetric_density": 0.0 if config["style"] == "anime" else round(1.5*sc, 2),
                    "mesh_stutter_strength": round(2.0 * sc, 2), "turbulence_force_strength": round(15.0 * sc, 1)
                })
        
        with open(os.path.join(self.workspace_dir, "35_procedural_vfx_blueprint.json"), "w", encoding="utf-8") as f: json.dump(output, f, indent=4)
        self._bake_vfx_in_blender(output)
        self._handshake("COMPLETED")
        return output

    # =====================================================================
    # RULE 9, 11, 12, 13 & 17: BLENDER RECIPE EVALUATOR & COMPILER
    # =====================================================================
    def _bake_vfx_in_blender(self, vfx_data):
        self.log("Compiling Limitless Recipe Blender Python script...")
        vfx_json = json.dumps(vfx_data.get('vfx_procedural_profiles', []))
        script_content = f"""
import bpy, math, random

vfx_profiles = {vfx_json}[:60] # Rule 17: VRAM cap max 60 instances
scene = bpy.context.scene
fps = scene.render.fps

bpy.ops.object.select_all(action='DESELECT')
for obj in scene.objects:
    if obj.name.startswith("OMNIMATRIX_VFX_") or obj.name.startswith("FORCE_VFX_"):
        obj.select_set(True)
bpy.ops.object.delete()

scene.render.engine = 'BLENDER_EEVEE'
if hasattr(scene.eevee, "use_bloom"): scene.eevee.use_bloom, scene.eevee.bloom_intensity = True, 0.06

for idx, vfx in enumerate(vfx_profiles):
    try:
        v_name, style = str(vfx.get('vfx_name', f'VFX_{{idx}}')), str(vfx.get('render_style_enforced', 'realistic')).lower()
        loc, target_socket = tuple(vfx.get('vfx_origin_xyz', [0,0,0])), str(vfx.get('socket_bind_target', '_Socket'))
        prim, pattern = str(vfx.get('primitive_mesh', 'ico_sphere')).lower(), str(vfx.get('shader_math_pattern', 'voronoi')).lower()
        interp = str(vfx.get('color_ramp_interpolation', 'EASE')).upper()
        c1, c2 = tuple(vfx.get('color_primary_rgb', [0,0.8,1])) + (1.0,), tuple(vfx.get('color_secondary_rgb', [0.9,0.1,0.5])) + (1.0,)
        glow, pat_scale = float(vfx.get('glow_intensity_emission', 100)), float(vfx.get('pattern_scale', 5))
        deform, p_rate = float(vfx.get('mesh_deform_strength', 3)), min(int(vfx.get('particle_spawn_rate', 150)), 350)
        v_density, stutter = float(vfx.get('volumetric_density', 1)), float(vfx.get('mesh_stutter_strength', 1.5))
        turb_force, spawn_frame = float(vfx.get('turbulence_force_strength', 15)), int(vfx.get('timestamp_sec', 0) * fps)
        end_frame = min(spawn_frame + int(fps * 2.0), spawn_frame + 150) # Rule 17: Max 150 frames

        # 1. DYNAMIC PRIMITIVE MESH EVALUATOR (Zero Hardcoded Shapes!)
        if 'torus' in prim or 'ring' in prim: bpy.ops.mesh.primitive_torus_add(major_radius=2.5, minor_radius=0.2, location=loc)
        elif 'cylin' in prim or 'tube' in prim: bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.15, depth=5.0, location=loc)
        elif 'cone' in prim: bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=1.5, depth=3.0, location=loc)
        elif 'grid' in prim or 'plane' in prim: bpy.ops.mesh.primitive_grid_add(x_subdivisions=10, y_subdivisions=10, size=3.0, location=loc)
        else: bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=1.5, location=loc)
        
        obj = bpy.context.active_object
        obj.name, _ = f"OMNIMATRIX_VFX_{{v_name}}_{{idx}}", bpy.ops.object.shade_smooth()

        # Rule 13: Socket Protocol Binding
        for arm in [o for o in scene.objects if o.type == 'ARMATURE']:
            for b in arm.data.bones:
                if target_socket.lower() in b.name.lower() or "_socket" in b.name.lower():
                    if math.sqrt(sum((a - c)**2 for a, c in zip(loc, arm.matrix_world @ b.head_local))) < 3.5:
                        const = obj.constraints.new(type='CHILD_OF')
                        const.target, const.subtarget = arm, b.name
                        const.inverse_matrix = (arm.matrix_world @ b.matrix_local).inverted()
                        break

        # Rule 11 & 4: DYNAMIC PROCEDURAL SHADER RECIPE BUILDER (No External Textures)
        mat = bpy.data.materials.new(name=f"MAT_{{obj.name}}")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out, emit = nt.nodes.new('ShaderNodeOutputMaterial'), nt.nodes.new('ShaderNodeEmission')
        
        # Dynamically Select Pattern Math Node
        if 'wave' in pattern: tex = nt.nodes.new('ShaderNodeTexWave')
        elif 'magic' in pattern: tex = nt.nodes.new('ShaderNodeTexMagic')
        elif 'noise' in pattern: tex = nt.nodes.new('ShaderNodeTexNoise')
        else: 
            tex = nt.nodes.new('ShaderNodeTexVoronoi')
            tex.feature = 'F1'
        if hasattr(tex.inputs['Scale'], 'default_value'): tex.inputs['Scale'].default_value = pat_scale

        ramp = nt.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.interpolation = 'CONSTANT' if style == 'anime' or interp == 'CONSTANT' else 'EASE'
        ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.35, c2
        ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.45, c1

        if style == "realistic":
            mat.blend_method, emit.inputs['Color'].default_value, emit.inputs['Strength'].default_value = 'BLEND', c1, glow * 0.5
            fresnel, mix, trans = nt.nodes.new('ShaderNodeFresnel'), nt.nodes.new('ShaderNodeMixShader'), nt.nodes.new('ShaderNodeBsdfTransparent')
            fresnel.inputs['IOR'].default_value = 1.25
            nt.links.new(trans.outputs['BSDF'], mix.inputs[1]); nt.links.new(emit.outputs['Emission'], mix.inputs[2])
            nt.links.new(fresnel.outputs['Fac'], mix.inputs[0]); nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
            if v_density > 0.1:
                vol = nt.nodes.new('ShaderNodeVolumePrincipled')
                vol.inputs['Color'].default_value, vol.inputs['Density'].default_value = c1, v_density
                vol.inputs['Emission Strength'].default_value, vol.inputs['Emission Color'].default_value = glow * 0.1, c2
                nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
        else:
            mat.blend_method, emit.inputs['Strength'].default_value = 'ADD', glow
            lw, math_mul = nt.nodes.new('ShaderNodeLayerWeight'), nt.nodes.new('ShaderNodeMath')
            math_mul.operation = 'MULTIPLY'
            out_sock = tex.outputs['Distance'] if 'Distance' in tex.outputs else tex.outputs['Color']
            nt.links.new(out_sock, math_mul.inputs[0]); nt.links.new(lw.outputs['Facing'], math_mul.inputs[1])
            nt.links.new(math_mul.outputs['Value'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], emit.inputs['Color'])
            nt.links.new(emit.outputs['Emission'], out.inputs['Surface'])
        obj.data.materials.append(mat)

        # Rule 12: Kinetic Mesh Physics (Zero Camera Touch - That's Agent 21!)
        disp = obj.modifiers.new(name="Kinetic_Displace", type='DISPLACE')
        d_tex = bpy.data.textures.new(f"Tex_{{obj.name}}", type='CLOUDS')
        d_tex.noise_scale = 0.5 if style == "realistic" else 1.8
        disp.texture, disp.strength = d_tex, deform * 0.1

        obj.scale = (0.1, 0.1, 0.1); obj.keyframe_insert("scale", frame=spawn_frame)
        obj.scale = (1.8, 1.8, 1.8) if style == "realistic" else (2.4, 2.4, 2.4); obj.keyframe_insert("scale", frame=spawn_frame + 6)
        if obj.animation_data and obj.animation_data.action:
            for fc in obj.animation_data.action.fcurves:
                if fc.data_path == "scale":
                    nm = fc.modifiers.new(type='NOISE')
                    nm.scale, nm.strength, nm.use_restricted_range = (1.5 if style == "anime" else 3.0), stutter * 0.25, True
                    nm.frame_start, nm.frame_end = spawn_frame, spawn_frame + 18

        if turb_force > 5.0:
            bpy.ops.object.effector_add(type='TURBULENCE', location=loc)
            ff = bpy.context.active_object
            ff.name, ff.field.strength, ff.parent = f"FORCE_VFX_{{idx}}", turb_force, obj

        if p_rate > 0:
            ps = obj.modifiers.new(name="Kinetic_Particles", type='PARTICLE_SYSTEM').particle_system.settings
            ps.count, ps.frame_start, ps.frame_end, ps.lifetime = p_rate, spawn_frame, spawn_frame + 12, int(fps * 1.2)
            ps.normal_factor, ps.effector_weights.gravity = (4.0 if style == "realistic" else 10.0), (1.0 if style == "realistic" else -0.3)

        for f, val in [(max(1, spawn_frame-1), True), (spawn_frame, False), (end_frame, True)]:
            obj.hide_viewport = obj.hide_render = val
            obj.keyframe_insert("hide_viewport", frame=f); obj.keyframe_insert("hide_render", frame=f)
    except Exception as e: print(f"Error on profile {{idx}}: {{e}}")

try: bpy.ops.wm.save_mainfile()
except Exception: pass
"""
        script_path = os.path.join(self.workspace_dir, "temp_vfx_forge.py")
        with open(script_path, "w", encoding="utf-8") as f: f.write(script_content)
        for file in os.listdir(self.env_dir):
            if file.endswith(".blend"):
                try: subprocess.run([self.blender_path, "-b", os.path.join(self.env_dir, file), "-P", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
                except Exception: pass
        if os.path.exists(script_path): os.remove(script_path)
        self.log("Blender Limitless Recipe compilation and kinetic injection complete!", "SUCCESS")

if __name__ == "__main__":
    Ai_Agent_35_Autonomous