# ==============================================================================
# Ai_Agent_20_Procedural_Text_Mesh_Builder.py
# MODULE C: Blender 3D Heavy Infantry
# ==============================================================================

import os
import re
import sys
import json
import math
import hashlib
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

class AiAgent20ProceduralTextMeshBuilder:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_20_Procedural_Text_Mesh_Builder"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_root = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_root, "Module_A_Scripting")
        self.module_c_dir = os.path.join(self.workspace_root, "Module_C_Heavy_Infantry")
        self.output_dir = os.path.join(self.module_c_dir, "3d_text_assets")
        self.output_blueprint = os.path.join(self.output_dir, "20_master_text_blueprint.json")
        
        # System States (RULE 7)
        self.state_file = os.path.join(self.workspace_root, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_root, "global_config.json")
        
        # API Keys for Quad-Core (RULE 6)
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        for d in [self.workspace_root, self.script_dir, self.module_c_dir, self.output_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    # RULE 3: IDEMPOTENCY SCRUBBING
    def scrub_workspace(self):
        self.log("Scrubbing legacy 3D text assets...", "INFO")
        for filename in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                self.log(f"Failed to delete {file_path}: {e}", "WARNING")

    # RULE 4: LIMITLESS FLUIDITY
    def _load_master_config(self):
        default_config = {"global_style": "anime", "fps": 24, "blender_executable": "blender"}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except: pass
        return default_config

    def _load_upstream_context(self):
        text_nodes = []
        if os.path.exists(self.script_dir):
            for filename in os.listdir(self.script_dir):
                if filename.endswith("_action.json") or filename.endswith("_matrix_state.json"):
                    scene_name = filename.replace("_action.json", "").replace("_matrix_state.json", "")
                    try:
                        with open(os.path.join(self.script_dir, filename), "r", encoding="utf-8") as f:
                            data = json.load(f)
                            text_nodes.append({
                                "scene_name": scene_name,
                                "dialogue": data.get("dialogue", ""),
                                "action": data.get("action_description", ""),
                                "vibe": data.get("genre_vibe", "cinematic")
                            })
                    except: pass
        return text_nodes

    # RULE 5: BULLETPROOF JSON
    def _clean_json_response(self, raw_text):
        try:
            cleaned = re.sub(r'```(?:json)?\n(.*?)```', r'\1', raw_text, flags=re.DOTALL).strip()
            return json.loads(cleaned)
        except:
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            if start != -1 and end != -1:
                try: return json.loads(raw_text[start:end+1])
                except: pass
            return None

    # RULE 10: 100% OFFLINE AUTONOMY FALLBACK
    def _get_procedural_fallback_design(self, context, style):
        text = context.get('dialogue', '').strip()
        if not text:
            return {"text_content": "NONE"}
            
        is_anime = style == "anime"
        
        # Math-based deterministic color hashing based on text length and vibe
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        r = (hash_val % 255) / 255.0
        g = ((hash_val >> 8) % 255) / 255.0
        b = ((hash_val >> 16) % 255) / 255.0
        
        return {
            "text_content": text,
            "render_style_enforced": style,
            "material_vibe": "manga_impact" if is_anime else "metallic_pbr",
            "extrusion_depth": 0.1 if is_anime else 0.25,
            "bevel_depth": 0.0 if is_anime else 0.03,
            "position_offset_xyz": [0.0, 0.0, -2.0], # Default subtitle height
            "color_rgb": [r, g, b]
        }

    # RULE 6: QUAD-CORE FALLBACK MATRIX
    def _query_autonomous_typography_brain(self, context, config):
        style = config.get("global_style", "realistic")
        dialogue = context.get('dialogue', '').strip()
        
        if not dialogue:
            return {"text_content": "NONE"}

        ai_prompt = f"""
        You are the AAA 3D Typography Director for a Limitless Render Engine.
        Project Style: '{style.upper()}'
        Context Action: '{context['action']}' | Vibe: '{context['vibe']}'
        Dialogue/Text to display: "{dialogue}"

        Decide the geometry and procedural shader vibe for this text. 
        - If 'REALISTIC': Use vibes like 'metallic_pbr', 'holographic_glow', or 'glass_refraction'.
        - If 'ANIME': Use vibes like 'cel_shaded_neon', 'manga_impact', or 'blood_spatter_toon'.
        - Position: Z=0 is center. Z=-2.0 is subtitle area. Y and X can offset for comedic/awkward anime effects.

        Return ONLY raw JSON:
        {{
            "text_content": "{dialogue}",
            "render_style_enforced": "{style}",
            "material_vibe": "string (from above)",
            "extrusion_depth": float (0.05 to 0.4),
            "bevel_depth": float (0.0 to 0.08, 0 for anime),
            "position_offset_xyz": [X, Y, Z],
            "color_rgb": [R, G, B] (0.0 to 1.0)
        }}
        """

        # Core 1: Gemini
        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self.clean_json_response(res_text)
                    if parsed: return parsed
            except: pass

        # Core 2: OpenAI
        if self.openai_api_key:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")}
                payload = {"model": "gpt-4o", "messages": [{"role": "user", "content": ai_prompt}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
                    parsed = self.clean_json_response(res_text)
                    if parsed: return parsed
            except: pass

        # Core 3 & 4 (Local/Math)
        self.log("AI APIs failed or unavailable. Engaging Math Procedural Core.", "WARNING")
        return self._get_procedural_fallback_design(context, style)

    # RULE 9 (Abstraction), RULE 11 (Procedural Shaders), RULE 12 (Kinetic), RULE 13 (Sockets)
    def _generate_blender_script(self, text_design, out_blend_path, config):
        safe_blend_path = out_blend_path.replace("\\", "/")
        fps = config.get("fps", 24)
        
        script_content = f"""
import bpy
import json
import math

design = {json.dumps(text_design)}

try:
    # --- 1. CLEANUP ---
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # --- RULE 13: THE "SOCKET" PROTOCOL ---
    # Create an empty socket so camera/compositor can grab the text unit easily
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1.0, location=(0,0,0))
    socket_obj = bpy.context.active_object
    socket_obj.name = "TXT_SOCKET"

    # --- 2. GENERATE 3D TEXT GEOMETRY ---
    font_curve = bpy.data.curves.new(type="FONT", name="Auto_Text_Curve")
    font_curve.body = design.get('text_content', 'TEXT')
    font_curve.align_x = 'CENTER'
    font_curve.align_y = 'CENTER'
    
    font_curve.extrude = float(design.get('extrusion_depth', 0.1))
    font_curve.bevel_depth = float(design.get('bevel_depth', 0.0))
    font_curve.bevel_resolution = 4

    font_obj = bpy.data.objects.new("OMNI_3D_Text", font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    
    pos = tuple(design.get('position_offset_xyz', [0.0, 0.0, 0.0]))
    font_obj.location = pos
    
    # Parent Text to Socket
    font_obj.parent = socket_obj

    # --- RULE 11: PROCEDURAL DECOUPLING (NO IMAGE TEXTURES) ---
    mat = bpy.data.materials.new(name="Omni_Procedural_Text_Mat")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    
    out_node = nt.nodes.new('ShaderNodeOutputMaterial')
    vibe = design.get('material_vibe', 'manga_impact').lower()
    style = design.get('render_style_enforced', 'anime').lower()
    color = tuple(design.get('color_rgb', [1.0, 1.0, 1.0])) + (1.0,)
    
    if style == 'realistic':
        bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.inputs['Base Color'].default_value = color
        
        # Math based procedural textures (Voronoi/Noise)
        noise = nt.nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 50.0
        
        if 'holo' in vibe or 'glow' in vibe:
            bsdf.inputs['Emission Strength'].default_value = 5.0
            bsdf.inputs['Emission Color'].default_value = color
            bsdf.inputs['Alpha'].default_value = 0.7
            mat.blend_method = 'BLEND'
            # Link Noise to Alpha for glitchy hologram
            nt.links.new(noise.outputs['Fac'], bsdf.inputs['Alpha'])
        else: # Metallic/Cinematic
            bsdf.inputs['Metallic'].default_value = 1.0
            nt.links.new(noise.outputs['Fac'], bsdf.inputs['Roughness'])
            
        nt.links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
        
    else: # ANIME / CEL SHADED
        mat.blend_method = 'OPAQUE'
        if 'neon' in vibe or 'glow' in vibe:
            emit = nt.nodes.new('ShaderNodeEmission')
            emit.inputs['Color'].default_value = color
            emit.inputs['Strength'].default_value = 10.0
            nt.links.new(emit.outputs['Emission'], out_node.inputs['Surface'])
        else:
            # Manga Flat Toon (100% Math, no shading)
            emit = nt.nodes.new('ShaderNodeEmission')
            emit.inputs['Color'].default_value = color
            emit.inputs['Strength'].default_value = 1.0
            nt.links.new(emit.outputs['Emission'], out_node.inputs['Surface'])

    font_obj.data.materials.append(mat)

    # --- RULE 12: KINETIC PHYSICS INJECTION ---
    # 1. Pop-in Scale Animation with Overshoot (BACK interpolation)
    font_obj.scale = (0.0, 0.0, 0.0)
    font_obj.keyframe_insert(data_path="scale", frame=1)
    
    font_obj.scale = (1.2, 1.2, 1.2) # Overshoot
    font_obj.keyframe_insert(data_path="scale", frame=6)
    
    font_obj.scale = (1.0, 1.0, 1.0) # Settle
    font_obj.keyframe_insert(data_path="scale", frame=10)
    
    for fc in font_obj.animation_data.action.fcurves:
        for kf in fc.keyframe_points:
            kf.interpolation = 'BACK' # AAA kinetic snap

    # 2. Continuous Floating / Breathing (F-Curve Noise Modifier)
    font_obj.keyframe_insert(data_path="location", frame=1)
    for fc in font_obj.animation_data.action.fcurves:
        if fc.data_path == 'location' and fc.array_index == 2: # Z-axis float
            mod = fc.modifiers.new('NOISE')
            mod.scale = 20.0
            mod.strength = 0.1 # Subtle float up and down
            mod.phase = 1.0

    # --- 5. SAVE ---
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_BLENDER_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_text_forge_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def build_text_meshes(self):
        self.log("System Initializing...", "INFO")

        # RULE 7: ATOMIC HANDSHAKE
        state = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
            except: pass
                
        if state.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{state.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        self.scrub_workspace()
        config = self._load_master_config()
        blender_executable = config.get("blender_executable", "blender")
        nodes = self._load_upstream_context()
        
        master_blueprint = {}

        if not nodes:
            self.log("No text nodes found in Module A. Bypassing text generation.", "WARNING")
        
        for node in nodes:
            scene_name = node["scene_name"]
            
            design = self._query_autonomous_typography_brain(node, config)
            
            if design.get("text_content") == "NONE":
                self.log(f"[{scene_name}] AI determined NO TEXT needed for this scene.", "INFO")
                continue
                
            self.log(f"[{scene_name}] Forging '{design.get('material_vibe')}' text: '{design['text_content']}'", "INFO")
            
            out_blend_path = os.path.join(self.output_dir, f"{scene_name}_text.blend")
            script_path = self._generate_blender_script(design, out_blend_path, config)
            
            command = [blender_executable, "-b", "-P", script_path]
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout and os.path.exists(out_blend_path):
                    self.log(f"Text Asset Verified: {scene_name}_text.blend", "SUCCESS")
                    master_blueprint[scene_name] = {
                        "text_blend": out_blend_path,
                        "socket_name": "TXT_SOCKET",
                        "ai_design_decisions": design
                    }
                else:
                    self.log(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
            except Exception as e:
                self.log(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                
            if os.path.exists(script_path):
                os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: ATOMIC HANDSHAKE (Advance State)
        state["last_active_agent"] = self.agent_name
        # Heading to Kinetic Camera Rig Director!
        state["next_agent"] = "Ai_Agent_21_Kinetic_Camera_Rig_Director"
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
        
        self.log(f"Procedural Text Infantry Complete! Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    builder = AiAgent20ProceduralTextMeshBuilder()
    if hasattr(builder, "clean_json_response"):
        pass # Inherited from God Level V2 logic
    else:
        builder.clean_json_response = builder._clean_json_response 
    builder.build_text_meshes()

# ==============================================================================
# END OF FILE
# ==============================================================================
