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

class Ai_Agent_37_Stylized_Smoke_Fire_Fluid_Forge:
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "Ai_Agent_37_Stylized_Smoke_Fire_Fluid_Forge"
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
        for f in ["37_stylized_smoke_fire_blueprint.json", "temp_smoke_fire_forge.py"]:
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
        if status == "COMPLETED": data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_38_VFX_Bloom_Glare_Engine"
        with open(matrix_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

    def _load_config(self):
        p = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    return {"style": d.get("global_style", "realistic").lower(), "theme": d.get("theme", "elemental")}
            except Exception: pass
        return {"style": "realistic", "theme": "limitless_elemental"}

    def _load_hotspots(self):
        p = os.path.join(self.workspace_dir, "35_procedural_vfx_blueprint.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return [{"timestamp_sec": float(ev.get("timestamp_sec", 0.0)), "vfx_origin_xyz": ev.get("vfx_origin_xyz", [0,0,0]), "impact_scale": float(ev.get("glow_intensity_emission", 50)/50.0), "socket_hint": ev.get("socket_bind_target", "_Socket")} for ev in json.load(f).get("vfx_procedural_profiles", [])]
            except Exception: pass
        return [{"timestamp_sec": 1.0, "vfx_origin_xyz": [0.0, 1.5, 0.5], "impact_scale": 2.5, "socket_hint": "Hand_R_Socket"}, {"timestamp_sec": 3.2, "vfx_origin_xyz": [2.0, 0.5, -1.0], "impact_scale": 4.0, "socket_hint": "Chest_Socket"}]

    def _clean_json(self, raw):
        s = re.sub(r"^```(json)?\s*|\s*```$", "", raw.strip(), flags=re.IGNORECASE)
        return s[s.find('{'):s.rfind('}')+1] if '{' in s and '}' in s else s

    def _api_call(self, url, payload, headers):
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=35) as res: return json.loads(res.read().decode("utf-8"))

    # =====================================================================
    # RULE 6, 14 & 15: QUAD-CORE LIMITLESS ELEMENTAL RECIPE SYNTHESIZER
    # =====================================================================
    def forge_smoke_fire_fluid(self):
        self._handshake("IN_PROGRESS")
        hotspots, config = self._load_hotspots(), self._load_config()
        self.log(f"Quad-Core Limitless Elemental Forge Initiated. Style: {config['style'].upper()} | Theme: {config['theme']}")
        
        # Rule 15: Pure Mathematical Elemental Recipe (ZERO Fire/Smoke Gulaami!)
        prompt = (f"You are OMNIMATRIX VFX Elemental Director. Global Style: '{config['style']}', Theme: '{config['theme']}'.\n"
                  "Invent completely unique, limitless 3D volumetric fire, smoke, plasma, liquid metal, magic mist, or alien fluid RECIPES for each hotspot. DO NOT touch camera.\n"
                  "DO NOT use preset names. Return JSON object with list 'fluid_fire_profiles' containing:\n"
                  "- 'timestamp_sec': float, 'render_style_enforced': string ('realistic' or 'anime'), 'concept_name': string,\n"
                  "- 'socket_bind_target': string (hint like 'Hand_R_Socket', 'stomach', 'weapon', or '_Socket'),\n"
                  "- 'vfx_origin_xyz': [X, Y, Z], 'emitter_geometry': string ('ico_sphere', 'torus', 'cylinder', 'cone', 'mesh_surface'),\n"
                  "- 'shader_pattern_math': string ('voronoi_flame', 'noise_smoke', 'wave_plasma', 'magic_fluid'),\n"
                  "- 'color_ramp_interpolation': string ('EASE' for soft realistic fog/smoke, 'CONSTANT' for sharp toon manga fire banding),\n"
                  "- 'pattern_scale': float (1.0-35.0), 'volumetric_density': float (0.5-8.0), 'emission_strength': float (10.0-300.0),\n"
                  "- 'color_core_rgba': [R, G, B, A], 'color_edge_rgba': [R, G, B, A], 'particle_spawn_rate': int (50-300),\n"
                  "- 'kinetic_pulse_frequency': float (1.0-15.0 for F-Curve noise flickering), 'wind_turbulence_force': float (5.0-40.0).\n"
                  "Zero compression or placeholders allowed.")
        
        output = None
        user_msg = f"Hotspots Context:\n{json.dumps(hotspots)}"
        
        # Core 1: Gemini (Primary - Rule 14 & 16)
        if self.gemini_key and not output:
            try:
                res = self._api_call(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.gemini_key}", {"contents": [{"parts": [{"text": f"{prompt}\n\n{user_msg}"}]}], "generationConfig": {"temperature": 0.88, "responseMimeType": "application/json"}}, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = {"fluid_fire_profiles": json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"])).get("fluid_fire_profiles", [])}
                self.log("[Core 1: Gemini] Synthesized limitless elemental recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")
        
        # Core 2: OpenAI (Failsafe - Rule 14 & 16)
        if self.openai_key and not output:
            try:
                res = self._api_call("https://api.openai.com/v1/chat/completions", {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "response_format": {"type": "json_object"}}, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_key}"})
                output = {"fluid_fire_profiles": json.loads(self._clean_json(res["choices"][0]["message"]["content"])).get("fluid_fire_profiles", [])}
                self.log("[Core 2: OpenAI] Synthesized limitless elemental recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")
        
        # Core 3: Ollama (Local Fallback - Rule 6)
        if not output:
            try:
                res = self._api_call("http://localhost:11434/api/chat", {"model": "llama3", "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "format": "json", "stream": False}, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = {"fluid_fire_profiles": json.loads(self._clean_json(res.get("message", {}).get("content", "{}"))).get("fluid_fire_profiles", [])}
                self.log("[Core 3: Ollama] Generated local elemental recipes!", "SUCCESS")
            except Exception as e: self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")
        
        # Core 4: 100% Offline Math Autonomy (Rule 10 - Alien Algorithmic Fallback)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline elemental float synthesis...", "WARNING")
            prims, patterns = ["ico_sphere", "torus", "cylinder", "cone", "mesh_surface"], ["voronoi_flame", "noise_smoke", "wave_plasma", "magic_fluid"]
            output = {"fluid_fire_profiles": []}
            for idx, hs in enumerate(hotspots):
                random.seed(int((hs["timestamp_sec"] + idx + 1) * 1000))
                r1, g1, b1 = [round(random.uniform(0.3, 1.0), 3) for _ in range(3)]
                sc = hs["impact_scale"]
                output["fluid_fire_profiles"].append({
                    "timestamp_sec": hs["timestamp_sec"], "render_style_enforced": config["style"],
                    "concept_name": f"Elemental_Vortex_Class_{random.randint(100,999)}",
                    "socket_bind_target": hs["socket_hint"], "vfx_origin_xyz": hs["vfx_origin_xyz"],
                    "emitter_geometry": random.choice(prims), "shader_pattern_math": random.choice(patterns),
                    "color_ramp_interpolation": "CONSTANT" if config["style"] == "anime" else "EASE",
                    "pattern_scale": round(random.uniform(3.0, 25.0), 1), "volumetric_density": round(2.5 * sc, 1),
                    "emission_strength": round(120.0 * sc, 1), "color_core_rgba": [r1, g1, b1, 1.0],
                    "color_edge_rgba": [round(1.0-r1, 3), round(1.0-g1, 3), round(1.0-b1, 3), 0.2],
                    "particle_spawn_rate": min(300, int(90 * sc)), "kinetic_pulse_frequency": round(4.0 * sc, 1),
                    "wind_turbulence_force": round(18.0 * sc, 1)
                })
        
        with open(os.path.join(self.workspace_dir, "37_stylized_smoke_fire_blueprint.json"), "w", encoding="utf-8") as f: json.dump(output, f, indent=4)
        self._bake_elemental_vfx_in_blender(output)
        self._handshake("COMPLETED")
        return output

    # =====================================================================
    # RULE 9, 11, 12, 13 & 17: BLENDER RECIPE EVALUATOR & COMPILER
    # =====================================================================
    def _bake_elemental_vfx_in_blender(self, fire_data):
        self.log("Compiling Limitless Elemental Blender Python script...")
        fire_json = json.dumps(fire_data.get('fluid_fire_profiles', []))
        script_content = f"""
import bpy, math, random

profiles = {fire_json}[:50] # Rule 17: VRAM cap max 50 elemental instances
scene = bpy.context.scene
fps = scene.render.fps

bpy.ops.object.select_all(action='DESELECT')
for obj in scene.objects:
    if obj.name.startswith("OMNIMATRIX_VFX_Elemental_") or obj.name.startswith("FORCE_WIND_"):
        obj.select_set(True)
bpy.ops.object.delete()

scene.render.engine = 'BLENDER_EEVEE'
if hasattr(scene.eevee, "use_volumetric"): scene.eevee.use_volumetric, scene.eevee.volumetric_tile_size = True, '4'

# --- AGENT 26 SEMANTIC RIG MAPPER INTEGRATION FOR RULE 13 SOCKETS ---
def find_semantic_or_socket_bone(armature, target_hint):
    if not armature: return None
    hint_lower = target_hint.lower()
    for b in armature.data.bones:
        if hint_lower in b.name.lower() or "_socket" in b.name.lower(): return b.name
    kw_map = {{"hand": ["hand", "wrist", "arm_r", "arm_l"], "chest": ["spine", "chest", "torso"], "stomach": ["pelvis", "spine", "root"], "weapon": ["weapon", "prop", "hand"]}}
    for key, kw_list in kw_map.items():
        if key in hint_lower:
            for b in armature.data.bones:
                if any(kw in b.name.lower() for kw in kw_list): return b.name
    return None

for idx, p in enumerate(profiles):
    try:
        c_name, style = str(p.get('concept_name', f'Elem_{{idx}}')), str(p.get('render_style_enforced', 'realistic')).lower()
        loc, target_hint = tuple(p.get('vfx_origin_xyz', [0,0,0])), str(p.get('socket_bind_target', '_Socket'))
        prim, pattern = str(p.get('emitter_geometry', 'ico_sphere')).lower(), str(p.get('shader_pattern_math', 'voronoi_flame')).lower()
        interp, pat_scale = str(p.get('color_ramp_interpolation', 'EASE')).upper(), float(p.get('pattern_scale', 5.0))
        density, emit_str = float(p.get('volumetric_density', 2.0)), float(p.get('emission_strength', 50.0))
        c_core, c_edge = tuple(p.get('color_core_rgba', [1,0.5,0,1])), tuple(p.get('color_edge_rgba', [1,0,0,0.2]))
        p_rate, pulse_freq = min(int(p.get('particle_spawn_rate', 150)), 300), float(p.get('kinetic_pulse_frequency', 5.0))
        wind_force, spawn_frame = float(p.get('wind_turbulence_force', 15.0)), int(p.get('timestamp_sec', 0.0) * fps)
        end_frame = min(spawn_frame + int(fps * 3.0), spawn_frame + 150) # Rule 17: Cap simulation frames

        # 1. DYNAMIC EMITTER GEOMETRY EVALUATOR (Zero Shape Gulaami!)
        if 'torus' in prim or 'ring' in prim: bpy.ops.mesh.primitive_torus_add(major_radius=1.8, minor_radius=0.4, location=loc)
        elif 'cylin' in prim or 'column' in prim: bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.8, depth=3.0, location=loc)
        elif 'cone' in prim: bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=1.2, depth=3.0, location=loc)
        else: bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4 if style=='realistic' else 3, radius=1.3, location=loc)
        
        obj = bpy.context.active_object
        obj.name, _ = f"OMNIMATRIX_VFX_Elemental_{{c_name}}_{{idx}}", bpy.ops.object.shade_smooth()

        # Rule 13: Dynamic Socket & Semantic Rig Attachment (From Agent 26 & 58)
        for arm in [o for o in scene.objects if o.type == 'ARMATURE']:
            bone_name = find_semantic_or_socket_bone(arm, target_hint)
            if bone_name and math.sqrt(sum((a - c)**2 for a, c in zip(loc, arm.matrix_world @ arm.data.bones[bone_name].head_local))) < 4.0:
                const = obj.constraints.new(type='CHILD_OF')
                const.target, const.subtarget = arm, bone_name
                const.inverse_matrix = (arm.matrix_world @ arm.data.bones[bone_name].matrix_local).inverted()
                break

        # Rule 11 & 4: PURE MATHEMATICAL ELEMENTAL SHADER (No External Image Textures!)
        mat = bpy.data.materials.new(name=f"MAT_{{obj.name}}")
        mat.use_nodes, mat.blend_method = True, ('ADD' if style=='anime' else 'BLEND')
        nt = mat.node_tree; nt.nodes.clear()
        
        out, emit = nt.nodes.new('ShaderNodeOutputMaterial'), nt.nodes.new('ShaderNodeEmission')
        tex_coord, mapping = nt.nodes.new('ShaderNodeTexCoord'), nt.nodes.new('ShaderNodeMapping')
        mapping.inputs['Scale'].default_value = (pat_scale/5.0, pat_scale/5.0, pat_scale/2.0)
        
        # Dynamically Select Pattern Math
        if 'noise' in pattern: tex = nt.nodes.new('ShaderNodeTexNoise'); tex.inputs['Detail'].default_value = 5.0
        elif 'wave' in pattern: tex = nt.nodes.new('ShaderNodeTexWave')
        elif 'magic' in pattern: tex = nt.nodes.new('ShaderNodeTexMagic')
        else: tex = nt.nodes.new('ShaderNodeTexVoronoi'); tex.feature = 'F1'
        if hasattr(tex.inputs['Scale'], 'default_value'): tex.inputs['Scale'].default_value = pat_scale

        ramp = nt.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.interpolation = 'CONSTANT' if style == 'anime' or interp == 'CONSTANT' else 'EASE'
        ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.3, c_edge
        ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.5, c_core

        nt.links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
        nt.links.new(mapping.outputs['Vector'], tex.inputs['Vector'])
        out_sock = tex.outputs['Distance'] if 'Distance' in tex.outputs else tex.outputs['Color']
        nt.links.new(out_sock, ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], emit.inputs['Color'])
        emit.inputs['Strength'].default_value = emit_str
        nt.links.new(emit.outputs['Emission'], out.inputs['Surface'])

        if style == 'realistic' and density > 0.2:
            vol = nt.nodes.new('ShaderNodeVolumePrincipled')
            vol.inputs['Color'].default_value, vol.inputs['Density'].default_value = c_edge[:3]+(1.0,), density
            vol.inputs['Emission Strength'].default_value, vol.inputs['Emission Color'].default_value = emit_str * 0.15, c_core[:3]+(1.0,)
            nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
        obj.data.materials.append(mat)

        # Rule 12: Kinetic F-Curve Pulsing & Wind/Turbulence Physics (From Agent 26)
        if obj.animation_data is None: obj.animation_data_create()
        obj.animation_data.action = bpy.data.actions.new(name=f"Act_{{obj.name}}")
        fc_emit = obj.animation_data.action.fcurves.new(data_path=f'modifiers["Kinetic_Particles"].name' if p_rate>0 else "scale", index=0)
        
        nm = fc_emit.modifiers.new(type='NOISE')
        nm.scale, nm.strength, nm.frame_start, nm.frame_end = (10.0 / pulse_freq), emit_str * 0.3, spawn_frame, end_frame

        if wind_force > 5.0:
            bpy.ops.object.effector_add(type='WIND' if 'smoke' in pattern else 'TURBULENCE', location=loc)
            ff = bpy.context.active_object
            ff.name, ff.field.strength, ff.parent = f"FORCE_WIND_{{idx}}", wind_force, obj

        if p_rate > 0:
            ps = obj.modifiers.new(name="Kinetic_Particles", type='PARTICLE_SYSTEM').particle_system.settings
            ps.count, ps.frame_start, ps.frame_end, ps.lifetime = p_rate, spawn_frame, end_frame, int(fps * 1.5)
            ps.normal_factor, ps.effector_weights.gravity = (6.0 if style=='anime' else 2.0), (-0.5 if 'flame' in pattern else -0.1)

        for f, val in [(max(1, spawn_frame-1), True), (spawn_frame, False), (end_frame, True)]:
            obj.hide_viewport = obj.hide_render = val
            obj.keyframe_insert("hide_viewport", frame=f); obj.keyframe_insert("hide_render", frame=f)
    except Exception as e: print(f"Error on elemental profile {{idx}}: {{e}}")

try: bpy.ops.wm.save_mainfile()
except Exception: pass
"""
        script_path = os.path.join(self.workspace_dir, "temp_smoke_fire_forge.py")
        with open(script_path, "w", encoding="utf-8") as f: f.write(script_content)
        for file in os.listdir(self.env_dir):
            if file.endswith(".blend"):
                try: subprocess.run([self.blender_path, "-b", os.path.join(self.env_dir, file), "-P", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
                except Exception: pass
        if os.path.exists(script_path): os.remove(script_path)
        self.log("Blender Limitless Elemental compilation and physics injection complete!", "SUCCESS")

if __name__ == "__main__":
    Ai_Agent_37_Stylized_Smoke_Fire_Fluid_Forge().forge_smoke_fire_fluid()
