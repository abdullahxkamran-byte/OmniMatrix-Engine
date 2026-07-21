import os
import sys
import json
import re
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
                    os.environ[key.strip()] = val.strip()

load_env_file()

class AutonomousTextMeshBuilder:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 20: Autonomous 3D Typography Director"
        
        # Upstream Inputs (Reads script, audio vibe, and context)
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        
        # Outputs
        self.output_dir = os.path.join(local_library_dir, "3d_text_assets")
        self.output_blueprint = os.path.join(self.output_dir, "20_autonomous_text_blueprint.json")
        self.blender_path = blender_path
        
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.output_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_upstream_context(self):
        """Gathers all available scene context so the AI can make an autonomous decision."""
        text_nodes = []
        if not os.path.exists(self.script_dir):
            return text_nodes

        for filename in os.listdir(self.script_dir):
            if filename.endswith("_matrix_state.json"):
                filepath = os.path.join(self.script_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        text_nodes.append({
                            "scene_name": filename.replace("_matrix_state.json", ""),
                            "dialogue_or_lyrics": data.get("dialogue", ""),
                            "action_context": data.get("action_description", ""),
                            "vibe_genre": data.get("genre_vibe", "Unknown") # E.g., Phonk, Sad, Action, Commentary
                        })
                except Exception as e:
                    self.log_message(f"Error reading {filename}: {e}", "WARNING")

        # Fallback for testing if no upstream data exists
        if not text_nodes:
             text_nodes = [
                 {"scene_name": "test_short_hook", "dialogue_or_lyrics": "Wait till the end!", "action_context": "Fast paced commentary video hook", "vibe_genre": "YouTube Shorts / High Retention"},
                 {"scene_name": "test_song_lyric", "dialogue_or_lyrics": "I walk alone...", "action_context": "Slow camera pan across a dark street", "vibe_genre": "Dark Cinematic Music"}
             ]
        return text_nodes

    def _query_autonomous_typography_brain(self, context):
        """Gives Gemini full freedom to design the 3D text based on the vibe and context."""
        if not self.gemini_api_key:
            return self._get_fallback_design()

        ai_prompt = (
            f"You are the Autonomous 3D Typography Director for a AAA Video Engine.\n"
            f"Analyze the following scene context and decide the BEST way to render 3D text for it.\n"
            f"Scene Name: {context['scene_name']}\n"
            f"Dialogue/Lyrics: {context['dialogue_or_lyrics']}\n"
            f"Action/Context: {context['action_context']}\n"
            f"Vibe/Genre: {context['vibe_genre']}\n\n"
            "Decide the text style. Is it a massive 'Retention Hook' for Shorts? A sleek '3D Lyric' for a song? A '3D Subtitle'? Or an 'Anime SFX'?\n"
            "Return ONLY raw JSON. Format exactly like this:\n"
            "{\n"
            "  \"text_content\": \"The exact words to display\",\n"
            "  \"style_type\": \"Retention_Hook\",\n"
            "  \"extrusion_depth\": 0.35,\n"
            "  \"bevel_depth\": 0.04,\n"
            "  \"letter_spacing\": 1.0,\n"
            "  \"alignment\": \"CENTER\",\n"
            "  \"position_offset\": [0.0, 0.0, 0.0],\n" 
            "  \"material_vibe\": \"Neon_Glow\" \n"
            "}\n"
            "Note: Use position_offset [0, -2, 0] for subtitles, [0, 0, 0] for center hooks. material_vibe can be: Neon_Glow, Metallic, Matte, Bold_Color."
        )

        try:
            payload = {"contents": [{"parts": [{"text": ai_prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                res_text = re.sub(r'^```json', '', res_text, flags=re.IGNORECASE)
                res_text = re.sub(r'```$', '', res_text).strip()
                return json.loads(res_text)
        except Exception as e:
            self.log_message(f"AI Decision failed ({str(e)}). Using fallback.", "WARNING")
            return self._get_fallback_design()

    def _get_fallback_design(self):
        return {
            "text_content": "TEXT MISSING",
            "style_type": "Fallback",
            "extrusion_depth": 0.2,
            "bevel_depth": 0.02,
            "letter_spacing": 1.0,
            "alignment": "CENTER",
            "position_offset": [0.0, 0.0, 0.0],
            "material_vibe": "Matte"
        }

    def _generate_blender_script(self, text_design, out_blend_path):
        """Translates the AI's creative decision into procedural Blender geometry & shaders."""
        safe_blend_path = out_blend_path.replace("\\", "/")
        pos = text_design.get('position_offset', [0, 0, 0])
        mat_vibe = text_design.get('material_vibe', 'Matte')
        
        script_content = f"""
import bpy

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

try:
    clear_scene()

    # 1. Create 3D Text Curve
    font_curve = bpy.data.curves.new(type="FONT", name="Auto_Text_Curve")
    font_curve.body = "{text_design.get('text_content', 'TEXT')}"
    font_curve.align_x = '{text_design.get('alignment', 'CENTER')}'
    font_curve.align_y = 'CENTER'
    
    # 2. Apply AI Geometry Decisions
    font_curve.extrude = {text_design.get('extrusion_depth', 0.2)}
    font_curve.bevel_depth = {text_design.get('bevel_depth', 0.02)}
    font_curve.bevel_resolution = 6
    font_curve.space_character = {text_design.get('letter_spacing', 1.0)}

    font_obj = bpy.data.objects.new("Procedural_3D_Text", font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    font_obj.location = ({pos[0]}, {pos[1]}, {pos[2]})
    
    # 3. Autonomous Material Engine
    mat = bpy.data.materials.new(name="AutoText_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    vibe = "{mat_vibe}"
    
    if bsdf:
        if "Neon" in vibe or "Glow" in vibe:
            bsdf.inputs['Emission'].default_value = (0.0, 0.8, 1.0, 1.0) # Cyan Glow
            bsdf.inputs['Emission Strength'].default_value = 8.0
            bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
        elif "Metallic" in vibe:
            bsdf.inputs['Metallic'].default_value = 1.0
            bsdf.inputs['Roughness'].default_value = 0.2
            bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0) # Silver/Chrome
        elif "Bold" in vibe:
            bsdf.inputs['Base Color'].default_value = (1.0, 0.8, 0.0, 1.0) # Warning Yellow
            bsdf.inputs['Roughness'].default_value = 0.4
        else:
            bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0) # Clean White Matte

    font_obj.data.materials.append(mat)

    # 4. Save the Asset
    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("SUCCESS")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_text_forge_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def build_text_meshes(self):
        self.log_message("Waking up Autonomous Typography Brain...", "INFO")
        
        nodes = self._load_upstream_context()
        master_blueprint = {}

        for node in nodes:
            scene_name = node["scene_name"]
            self.log_message(f"Analyzing Vibe for: {scene_name} ({node['vibe_genre']})", "INFO")
            
            # AI Decides the text style
            design = self._query_autonomous_typography_brain(node)
            
            if not design.get("text_content") or design.get("text_content").upper() == "NONE":
                self.log_message("AI decided no 3D text is needed here.", "INFO")
                continue
                
            style = design.get('style_type', 'Default')
            self.log_message(f"AI Decision: Opted for '{style}' style text -> '{design['text_content']}'", "INFO")
            
            out_blend_path = os.path.join(self.output_dir, f"{scene_name}_text.blend")
            script_path = self._generate_blender_script(design, out_blend_path)
            
            # Execute Blender
            command = [self.blender_path, "-b", "-P", script_path]
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0 and os.path.exists(out_blend_path):
                    self.log_message(f"3D Typography saved: {scene_name}_text.blend", "INFO")
                    master_blueprint[scene_name] = {
                        "text_blend": out_blend_path,
                        "ai_design_decisions": design
                    }
                else:
                    self.log_message(f"Blender failed: {result.stdout[-200:]}", "ERROR")
            except Exception as e:
                self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                
            if os.path.exists(script_path):
                os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
        
        self.log_message("Autonomous Typography Generation Complete.", "INFO")

if __name__ == "__main__":
    builder = AutonomousTextMeshBuilder()
    builder.build_text_meshes()
