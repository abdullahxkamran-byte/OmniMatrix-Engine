import os
import re
import sys
import json
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
                    # Force environment variables to uppercase for consistency
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class Local3DCharacterAssetSelector:
    def __init__(self, drive_temp_dir="G:/My Drive/ZNET_Temp", local_library_dir="D:/ZNET_Local_Assets", blender_path="blender"):
        self.agent_name = "Ai Agent 23: AAA Character Asset Placer"
        
        # Upstream Inputs
        self.script_dir = os.path.join(drive_temp_dir, "module_a_scripts")
        self.env_dir = os.path.join(local_library_dir, "3d_environments") # Modifies existing _stage.blend files
        
        # Local Asset Library
        self.char_lib_dir = os.path.join(local_library_dir, "3d_characters")
        self.manifest_path = os.path.join(self.char_lib_dir, "character_manifest.json")
        
        # Output Log
        self.output_blueprint = os.path.join(self.env_dir, "23_character_placements.json")
        self.blender_path = blender_path
        
        # Fixed API Key casing issue!
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        for d in [self.script_dir, self.env_dir, self.char_lib_dir]:
            if not os.path.exists(d):
                os.makedirs(d)
                
        self._ensure_manifest_exists()

    def log_message(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _ensure_manifest_exists(self):
        """Creates a manifest if the local library is empty."""
        if not os.path.exists(self.manifest_path):
            mock_data = {
                "characters": [
                    {"id": "char_001", "name": "Gojo Satoru", "file_name": "ch_gojo.blend", "tags": ["anime", "blindfold", "tall", "sorcerer"]},
                    {"id": "char_002", "name": "Cyber Ninja", "file_name": "ch_cyberninja.blend", "tags": ["sci-fi", "armor", "sword", "dark"]},
                    {"id": "char_003", "name": "Zack Snyder Hero", "file_name": "ch_grittyhero.blend", "tags": ["realistic", "cape", "gritty", "muscular"]}
                ]
            }
            with open(self.manifest_path, "w", encoding="utf-8") as f:
                json.dump(mock_data, f, indent=4)
            
            # Create dummy .blend files so the script doesn't crash during testing
            for char in mock_data["characters"]:
                dummy_path = os.path.join(self.char_lib_dir, char["file_name"])
                if not os.path.exists(dummy_path):
                    with open(dummy_path, "w") as f:
                        f.write("DUMMY BLEND FILE")

    def _load_character_demands(self, scene_name):
        """Finds what characters the script actually needs for this scene."""
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

    def _query_ai_matcher(self, scene_name, demand, manifest):
        """Asks Gemini to semantically match the script's demand with our local offline database."""
        if not self.gemini_api_key:
            return self._fallback_matcher(manifest)

        ai_prompt = (
            f"You are the AAA 3D Asset Supervisor.\n"
            f"Scene Name: {scene_name}\n"
            f"Character Demand from Script: {demand}\n\n"
            f"Local Assets Database: {json.dumps(manifest['characters'])}\n\n"
            "Find the BEST matching character from the database. If none match properly, set 'generate_new_asset' to true.\n"
            "Return ONLY raw JSON:\n"
            "{\n"
            "  \"matched_id\": \"char_001\",\n"
            "  \"matched_file\": \"ch_gojo.blend\",\n"
            "  \"confidence\": 0.95,\n"
            "  \"generate_new_asset\": false,\n"
            "  \"reason\": \"Character name perfectly matches the script.\"\n"
            "}"
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
            self.log_message(f"AI Matching failed: {str(e)}. Using fallback.", "WARNING")
            return self._fallback_matcher(manifest)

    def _fallback_matcher(self, manifest):
        char = manifest["characters"][0] if manifest["characters"] else {"id": "NONE", "file_name": "NONE"}
        return {
            "matched_id": char["id"], "matched_file": char.get("file_name", "NONE"),
            "confidence": 1.0, "generate_new_asset": False, "reason": "Fallback match"
        }

    def _generate_blender_script(self, target_stage_blend, character_blend_path):
        """Blender Python script to append the character object into the lit stage."""
        safe_stage = target_stage_blend.replace("\\", "/")
        safe_char = character_blend_path.replace("\\", "/")
        
        script_content = f"""
import bpy
import os

try:
    # Open the existing Stage (Lit by Agent 22)
    bpy.ops.wm.open_mainfile(filepath="{safe_stage}")

    # Path to the character file
    char_path = "{safe_char}"
    
    if not os.path.exists(char_path) or "DUMMY" in open(char_path, 'r', errors='ignore').read(10):
        print("WARNING: Character file is a dummy or missing. Appending a procedural proxy.")
        # Create Proxy Dummy
        bpy.ops.mesh.primitive_monkey_add(size=2, location=(0,0,1))
        monkey = bpy.context.active_object
        monkey.name = "AAA_Character_Proxy"
        
        # Track camera to proxy
        tracker = bpy.data.objects.get("Focus_Tracker")
        if tracker:
            tracker.location = monkey.location
    else:
        # APPEND LOGIC: Fetch objects from the character blend file
        with bpy.data.libraries.load(char_path, link=False) as (data_from, data_to):
            # Load all objects that start with 'CH_' or 'Rig_' (standard AAA naming conventions)
            data_to.objects = [name for name in data_from.objects if name.startswith("CH_") or name.startswith("Rig")]
            
            # If nothing matched standard naming, just grab everything
            if not data_to.objects:
                data_to.objects = data_from.objects

        # Link appended objects into the current scene
        for obj in data_to.objects:
            if obj is not None and obj.name not in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.link(obj)

        print("SUCCESS: Character successfully appended into the scene.")

    # Save the updated stage file
    bpy.ops.wm.save_as_mainfile(filepath="{safe_stage}")

except Exception as e:
    print("ERROR:", str(e))
    import sys
    sys.exit(1)
"""
        script_path = os.path.join("temp_append_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def place_characters_in_stages(self):
        self.log_message("Initializing AI Character Selector & Placer...", "INFO")
        
        with open(self.manifest_path, "r") as f:
            manifest = json.load(f)
            
        master_blueprint = {}
        
        # Go through each Stage file generated previously
        for filename in os.listdir(self.env_dir):
            if filename.endswith("_stage.blend"):
                scene_name = filename.replace("_stage.blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                self.log_message(f"--- Locating Actor for Scene: {scene_name} ---", "INFO")
                
                demand = self._load_character_demands(scene_name)
                match = self._query_ai_matcher(scene_name, demand, manifest)
                
                self.log_message(f"AI Decision: Selected '{match['matched_file']}' (Reason: {match['reason']})", "INFO")
                
                if match["generate_new_asset"]:
                    self.log_message("WARNING: Asset missing locally. Module H (Asset Factory) must generate this later.", "WARNING")
                    master_blueprint[scene_name] = {"status": "Awaiting Generative Asset", "demand": demand}
                    continue
                
                char_blend_path = os.path.join(self.char_lib_dir, match["matched_file"])
                script_path = self._generate_blender_script(blend_file_path, char_blend_path)
                
                self.log_message("Executing Headless Blender to Append Character...", "INFO")
                command = [self.blender_path, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_message(f"Character injected into {filename}", "INFO")
                        master_blueprint[scene_name] = match
                    else:
                        self.log_message(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log_message(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        self.log_message("Character Integration Complete. Stages are now populated.", "INFO")

if __name__ == "__main__":
    selector = Local3DCharacterAssetSelector()
    selector.place_characters_in_stages()
