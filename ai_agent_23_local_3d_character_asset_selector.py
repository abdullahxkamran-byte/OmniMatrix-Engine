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

class Universal3DCharacterAssetSelector:
    def __init__(self, workspace_dir="OmniMatrix_Workspace", local_library_dir="D:/OmniMatrix_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 23: universal_character_asset_placer"
        
        self.workspace_dir = workspace_dir
        self.script_dir = os.path.join(self.workspace_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments")
        
        self.char_lib_dir = os.path.join(local_library_dir, "3d_characters")
        self.manifest_path = os.path.join(self.char_lib_dir, "character_manifest.json")
        
        self.output_blueprint = os.path.join(self.workspace_dir, "23_universal_character_placements.json")
        self.blender_path = blender_path
        
        # GEMINI API INTEGRATION RESTORED!
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.workspace_dir, self.script_dir, self.env_dir, self.char_lib_dir]:
            if not os.path.exists(d):
                os.makedirs(d)
                
        self._ensure_manifest_exists()

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
                self.log_message(f"Master config read warning: {str(e)}", "WARNING")
        return "realistic"

    def _ensure_manifest_exists(self):
        if not os.path.exists(self.manifest_path):
            mock_data = {
                "characters": [
                    {"id": "char_001", "name": "Goku", "file_name": "ch_goku.blend", "tags": ["anime", "fighter", "saiyan", "dbz"]},
                    {"id": "char_002", "name": "Naruto", "file_name": "ch_naruto.blend", "tags": ["anime", "ninja", "shinobi", "action"]},
                    {"id": "char_003", "name": "Gojo Satoru", "file_name": "ch_gojo.blend", "tags": ["anime", "blindfold", "tall", "sorcerer"]},
                    {"id": "char_004", "name": "Killua", "file_name": "ch_killua.blend", "tags": ["anime", "assassin", "lightning", "hunter"]},
                    {"id": "char_005", "name": "Sasuke", "file_name": "ch_sasuke.blend", "tags": ["anime", "ninja", "dark", "sword"]}
                ]
            }
            with open(self.manifest_path, "w", encoding="utf-8") as f:
                json.dump(mock_data, f, indent=4)
            
            for char in mock_data["characters"]:
                dummy_path = os.path.join(self.char_lib_dir, char["file_name"])
                if not os.path.exists(dummy_path):
                    with open(dummy_path, "w") as f:
                        f.write("OMNIMATRIX DUMMY BLEND FILE")

    def _load_character_demands(self, scene_name):
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        demand = "Main protagonist standing in the center"
        
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    demand = data.get("character_details", data.get("action_description", demand))
            except Exception as e:
                self.log_message(f"Script parse error: {str(e)}", "WARNING")
        return demand

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

    def _query_ai_matcher(self, scene_name, demand, manifest, style):
        self.log_message(f"Matching Asset via Gemini for '{scene_name}' (Style: {style.upper()})...", "INFO")
        
        if not self.gemini_api_key:
            self.log_message("No Gemini API Key found. Using fallback.", "WARNING")
            return self._fallback_matcher(manifest)

        ai_prompt = (
            f"You are the AAA 3D Asset Supervisor. Project Style: '{style.upper()}'.\n"
            f"Scene Name: {scene_name}\n"
            f"Character Demand from Script: {demand}\n\n"
            f"Local Assets Database: {json.dumps(manifest['characters'])}\n\n"
            "CRITICAL: Match the character name STRICTLY. Do not hallucinate characters.\n"
            "If the exact character is missing, set 'generate_new_asset' to true.\n"
            "Return EXACTLY 1 raw JSON object:\n"
            "{\n"
            "  \"matched_id\": \"char_xyz\" or \"NONE\",\n"
            "  \"matched_file\": \"ch_name.blend\" or \"NONE\",\n"
            "  \"confidence\": 0.99,\n"
            "  \"generate_new_asset\": false,\n"
            "  \"reason\": \"Character name perfectly matched the demand.\"\n"
            "}"
        )

        try:
            # Using Gemini's native JSON enforcement
            payload = {
                "contents": [{"parts": [{"text": ai_prompt}]}], 
                "generationConfig": {"responseMimeType": "application/json"}
            }
            req = urllib.request.Request(self.gemini_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as response:
                res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
                cleaned = self._clean_json_response(res_text)
                return json.loads(cleaned)
        except Exception as e:
            self.log_message(f"Gemini API Failed: {str(e)}. Using fallback.", "WARNING")

        return self._fallback_matcher(manifest)

    def _fallback_matcher(self, manifest):
        char = manifest["characters"][0] if manifest["characters"] else {"id": "NONE", "file_name": "NONE"}
        return {
            "matched_id": char["id"], "matched_file": char.get("file_name", "NONE"),
            "confidence": 1.0, "generate_new_asset": False, "reason": "Procedural Fallback match"
        }

    def _generate_blender_script(self, target_stage_blend, character_blend_path, style):
        safe_stage = target_stage_blend.replace("\\", "/")
        safe_char = character_blend_path.replace("\\", "/")
        
        script_content = f"""
import bpy
import os

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_stage}")

    char_path = "{safe_char}"
    tracker = bpy.data.objects.get("OMNIMATRIX_Focus_Target")
    
    # Clean previous characters if agent is re-run
    for obj in bpy.data.objects:
        if obj.name.startswith("OMNI_CHAR_"):
            bpy.data.objects.remove(obj, do_unlink=True)
            
    is_dummy = not os.path.exists(char_path) or "OMNIMATRIX" in open(char_path, 'r', errors='ignore').read(25)

    if is_dummy:
        print("WARNING: Using Procedural Proxy Mannequin.")
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2.0, location=(0, 0, 1.0))
        body = bpy.context.active_object
        body.name = "OMNI_CHAR_Proxy_Body"
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(0, 0, 2.4))
        head = bpy.context.active_object
        head.name = "OMNI_CHAR_Proxy_Head"
        head.parent = body
        
        mat = bpy.data.materials.new(name="Proxy_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if '{style}' == 'anime':
            bsdf.inputs['Base Color'].default_value = (1.0, 0.0, 0.5, 1.0) 
            bsdf.inputs['Roughness'].default_value = 1.0
        else:
            bsdf.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0) 
            bsdf.inputs['Metallic'].default_value = 1.0
        body.data.materials.append(mat)
        head.data.materials.append(mat)
        
        if tracker:
            tracker.location = head.location
            tracker.parent = head
            
    else:
        # AAA APPEND LOGIC: Collections Priority
        appended = False
        with bpy.data.libraries.load(char_path, link=False) as (data_from, data_to):
            col_names = [c for c in data_from.collections if c.startswith("COL_CH_") or c.startswith("CH_")]
            if col_names:
                data_to.collections = col_names
                appended = True
            else:
                obj_names = [o for o in data_from.objects if o.startswith("CH_") or o.startswith("Rig")]
                data_to.objects = obj_names
                appended = True

        if appended:
            for col in data_to.collections:
                if col.name not in bpy.context.scene.collection.children:
                    bpy.context.scene.collection.children.link(col)
                    
            for obj in data_to.objects:
                if obj and obj.name not in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.link(obj)
                    
            rig = None
            for obj in bpy.context.scene.objects:
                if obj.type == 'ARMATURE' and ("Rig" in obj.name or "CH_" in obj.name):
                    rig = obj
                    break
                    
            if rig and tracker:
                tracker.location = (rig.location.x, rig.location.y, rig.location.z + 1.6)
                
        print("SUCCESS: Character Rig integrated.")

    bpy.ops.wm.save_as_mainfile(filepath="{safe_stage}")

except Exception as e:
    print(f"FAILED TO APPEND CHARACTER: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.workspace_dir, "temp_append_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def place_characters_in_stages(self):
        global_style = self._load_master_config()
        self.log_message(f"Initializing Universal Asset Selector [{global_style.upper()}]...", "INFO")
        
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        master_blueprint = {}
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                demand = self._load_character_demands(scene_name)
                match = self._query_ai_matcher(scene_name, demand, manifest, global_style)
                
                if match.get("generate_new_asset", False):
                    self.log_message(f"[{scene_name}] Asset Missing Locally. Handing over to Module H.", "WARNING")
                    master_blueprint[scene_name] = {"status": "Awaiting Module H Generation", "demand": demand}
                    continue
                
                self.log_message(f"[{scene_name}] Selected '{match.get('matched_file')}'", "INFO")
                char_blend_path = os.path.join(self.char_lib_dir, match.get("matched_file", ""))
                
                script_path = self._generate_blender_script(blend_file_path, char_blend_path, global_style)
                
                command = [self.blender_path, "-b", "-P", script_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0 and "SUCCESS" in result.stdout:
                        self.log_message(f"Character successfully injected into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = match
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Universal Character Integration Complete.", "INFO")

if __name__ == "__main__":
    selector = Universal3DCharacterAssetSelector()
    selector.place_characters_in_stages()
