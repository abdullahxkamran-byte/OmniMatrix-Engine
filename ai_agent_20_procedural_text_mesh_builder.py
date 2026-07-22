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

class UniversalAutonomousTextMeshBuilder:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 20: universal_autonomous_3d_typography_director"
        
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.output_dir = os.path.join(local_library_dir, "3d_text_assets")
        self.output_blueprint = os.path.join(self.output_dir, "20_autonomous_text_blueprint.json")
        self.blender_path = blender_path
        
        # GEMINI API INTEGRATION RESTORED!
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.output_dir, self.workspace_dir]:
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

    def _load_upstream_context(self):
        text_nodes = []
        if not os.path.exists(self.script_dir):
            self.log_message(f"Upstream script directory not found at {self.script_dir}. Deploying fallback hooks.", "WARNING")
            return self._get_fallback_text_nodes()

        for filename in os.listdir(self.script_dir):
            if filename.endswith("_matrix_state.json"):
                filepath = os.path.join(self.script_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        text_nodes.append({
                            "scene_name": filename.replace("_matrix_state.json", ""),
                            "dialogue_or_lyrics": data.get("dialogue", ""),
                            "action_context": data.get("action_description", "Standard action"),
                            "vibe_genre": data.get("genre_vibe", "Unknown")
                        })
                except Exception as e:
                    self.log_message(f"Error reading upstream script {filename}: {str(e)}", "ERROR")

        if not text_nodes:
             text_nodes = self._get_fallback_text_nodes()
        return text_nodes
        
    def _get_fallback_text_nodes(self):
        return [
            {"scene_name": "test_short_hook", "dialogue_or_lyrics": "Wait till the end!", "action_context": "Fast paced commentary video hook", "vibe_genre": "YouTube Shorts"},
            {"scene_name": "test_song_lyric", "dialogue_or_lyrics": "I walk alone...", "action_context": "Slow camera pan across a dark street", "vibe_genre": "Dark Cinematic Music"}
        ]

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

    def _query_autonomous_typography_brain(self, context, style):
        self.log_message(f"Querying AI Brain for scene: '{context['scene_name']}'...", "INFO")

        system_prompt = (
            f"You are the Lead 3D Typography Director. The project style is: '{style.upper()}'.\n"
            f"Decide the exact geometry, placement, and visual shader vibe for the text to appear on screen based on the following context:\n"
            f"Dialogue: {context['dialogue_or_lyrics']}\n"
            f"Action/Vibe: {context['action_context']} | {context['vibe_genre']}\n"
            "If style is REALISTIC: Use 'metallic_pbr', 'holographic_glow', or 'cinematic_matte'. High extrusion/bevel. Position Z offset around -2.0 for subtitles.\n"
            "If style is ANIME: Use 'cel_shaded_neon', 'manga_impact_flat', or 'sharp_toon'. Zero bevel, sharp flat extrusion, bright RGB colors.\n"
            "Return EXACTLY 1 raw JSON object containing:\n"
            "- 'text_content': string (the exact words, or 'NONE' if no text is needed).\n"
            "- 'render_style_enforced': string (must match global style).\n"
            "- 'material_vibe': string (choose from the style lists above).\n"
            "- 'extrusion_depth': float (range 0.05 to 0.4).\n"
            "- 'bevel_depth': float (range 0.0 to 0.08).\n"
            "- 'letter_spacing': float (range 0.8 to 1.5).\n"
            "- 'position_offset_xyz': array of 3 floats [X, Y, Z].\n"
            "- 'color_rgb': array of 3 floats [R, G, B].\n"
            "Output strictly valid JSON with no markdown backticks."
        )

        if self.gemini_api_key:
            try:
                # GEMINI NATIVE JSON PAYLOAD
                payload = {
                    "contents": [{"parts": [{"text": system_prompt}]}], 
                    "generationConfig": {"responseMimeType": "application/json"}
                }
                req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=60) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                    cleaned = self._clean_json_response(res_text)
                    return json.loads(cleaned)
            except Exception as e:
                self.log_message(f"Gemini API Route Failed: {str(e)}. Directing procedural text fallback.", "WARNING")

        return self._get_fallback_design(context, style)

    def _get_fallback_design(self, context, style):
        text = context.get('dialogue_or_lyrics', 'MISSING_TEXT')
        if style == "realistic":
            return {
                "text_content": text,
                "render_style_enforced": "realistic",
                "material_vibe": "metallic_pbr" if "action" in context.get('action_context', '').lower() else "cinematic_matte",
                "extrusion_depth": 0.25,
                "bevel_depth": 0.04,
                "letter_spacing": 1.1,
                "position_offset_xyz": [0.0, 0.0, -1.5],
                "color_rgb": [0.9, 0.9, 0.9]
            }
        else:
            return {
                "text_content": text,
                "render_style_enforced": "anime",
                "material_vibe": "manga_impact_flat" if "action" in context.get('action_context', '').lower() else "cel_shaded_neon",
                "extrusion_depth": 0.1,
                "bevel_depth": 0.0,
                "letter_spacing": 1.0,
                "position_offset_xyz": [0.0, 0.0, -1.0],
                "color_rgb": [1.0, 0.8, 0.1]
            }

    def _generate_blender_script(self, text_design, out_blend_path):
        safe_blend_path = out_blend_path.replace("\\", "/")
        
        script_content = f"""
import bpy
import json
import math

design = {json.dumps(text_design)}
fps = bpy.context.scene.render.fps

try:
    # --- 1. CLEANUP SCENE ---
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # --- 2. GENERATE 3D TEXT GEOMETRY ---
    font_curve = bpy.data.curves.new(type="FONT", name="Auto_Text_Curve")
    font_curve.body = design.get('text_content', 'TEXT')
    font_curve.align_x = 'CENTER'
    font_curve.align_y = 'CENTER'
    
    font_curve.extrude = float(design.get('extrusion_depth', 0.2))
    font_curve.bevel_depth = float(design.get('bevel_depth', 0.02))
    font_curve.bevel_resolution = 6
    font_curve.space_character = float(design.get('letter_spacing', 1.0))

    font_obj = bpy.data.objects.new("OMNIMATRIX_3D_Text", font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    
    pos = tuple(design.get('position_offset_xyz', [0.0, 0.0, 0.0]))
    font_obj.location = pos
    
    # --- 3. UNIVERSAL SHADER SYSTEM ---
    mat = bpy.data.materials.new(name="AutoText_Material")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    
    out_node = nt.nodes.new('ShaderNodeOutputMaterial')
    vibe = design.get('material_vibe', 'cinematic_matte').lower()
    style = design.get('render_style_enforced', 'realistic').lower()
    color = tuple(design.get('color_rgb', [1.0, 1.0, 1.0])) + (1.0,)
    
    if style == 'realistic':
        bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.inputs['Base Color'].default_value = color
        
        if 'metallic' in vibe:
            bsdf.inputs['Metallic'].default_value = 1.0
            bsdf.inputs['Roughness'].default_value = 0.2
        elif 'holo' in vibe or 'glow' in vibe:
            bsdf.inputs['Emission Strength'].default_value = 5.0
            bsdf.inputs['Emission Color'].default_value = color
            bsdf.inputs['Alpha'].default_value = 0.8
            mat.blend_method = 'BLEND'
        else:
            bsdf.inputs['Roughness'].default_value = 0.8
            
        nt.links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
        
    else:
        # Anime Cel Shaded / Flat Impact
        mat.blend_method = 'OPAQUE'
        if 'neon' in vibe or 'glow' in vibe:
            emit = nt.nodes.new('ShaderNodeEmission')
            emit.inputs['Color'].default_value = color
            emit.inputs['Strength'].default_value = 15.0
            nt.links.new(emit.outputs['Emission'], out_node.inputs['Surface'])
        else:
            # Hard Flat Toon Shader
            bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Specular IOR Level'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 1.0
            nt.links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
            
            # Anime Freestyle Outline Edge (simulated via Solidify in execution stage if needed)

    font_obj.data.materials.append(mat)

    # --- 4. KEYFRAME ANIMATION (POP-UP) ---
    spawn_frame = 1 # Asset starts at frame 1, timeline manages instantiation
    
    # Scale Pop Animation
    font_obj.scale = (0.01, 0.01, 0.01)
    font_obj.keyframe_insert(data_path="scale", frame=spawn_frame)
    
    pop_duration = 10 if style == 'anime' else 25 # Anime snaps faster
    font_obj.scale = (1.1, 1.1, 1.1)
    font_obj.keyframe_insert(data_path="scale", frame=spawn_frame + int(pop_duration * 0.7))
    
    font_obj.scale = (1.0, 1.0, 1.0)
    font_obj.keyframe_insert(data_path="scale", frame=spawn_frame + pop_duration)
    
    # Ensure interpolation is correct
    if font_obj.animation_data and font_obj.animation_data.action:
        for fc in font_obj.animation_data.action.fcurves:
            for kf in fc.keyframe_points:
                kf.interpolation = 'BEZIER' if style == 'realistic' else 'BACK' # Overshoot pop for anime

    # --- 5. SAVE & EXPORT ---
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS")

except Exception as e:
    print(f"ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_text_forge_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def build_text_meshes(self):
        global_style = self._load_master_config()
        self.log_message(f"Waking up Universal Typography Brain (Style: {global_style.upper()})...", "INFO")
        
        nodes = self._load_upstream_context()
        master_blueprint = {}

        for node in nodes:
            scene_name = node["scene_name"]
            
            design = self._query_autonomous_typography_brain(node, global_style)
            
            if not design.get("text_content") or design.get("text_content").upper() == "NONE":
                self.log_message(f"[{scene_name}] AI decided no 3D text is needed.", "INFO")
                continue
                
            self.log_message(f"[{scene_name}] Forging '{design.get('material_vibe', 'default')}' text: '{design['text_content']}'", "INFO")
            
            out_blend_path = os.path.join(self.output_dir, f"{scene_name}_text.blend")
            script_path = self._generate_blender_script(design, out_blend_path)
            
            command = [self.blender_path, "-b", "-P", script_path]
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0 and os.path.exists(out_blend_path):
                    self.log_message(f"Asset Verified: {scene_name}_text.blend", "SUCCESS")
                    master_blueprint[scene_name] = {
                        "text_blend": out_blend_path,
                        "ai_design_decisions": design
                    }
                else:
                    self.log_message(f"Blender build failed: {result.stdout[-250:]}", "ERROR")
            except Exception as e:
                self.log_message(f"Subprocess Execution failed: {str(e)}", "CRITICAL")
                
            if os.path.exists(script_path):
                os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
        
        self.log_message("Universal 3D Typography Pipeline Complete.", "INFO")

if __name__ == "__main__":
    builder = UniversalAutonomousTextMeshBuilder()
    builder.build_text_meshes()
