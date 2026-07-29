# ==============================================================================
# Ai_Agent_23_Universal_Character_Asset_Selector.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL V2.1: FULLY DYNAMIC)
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

class AiAgent23UniversalCharacterAssetSelector:
    def __init__(self):
        # RULE 8: AI vs NON-AI NAMING
        self.agent_name = "Ai_Agent_23_Dynamic_Casting_Director"
        
        # RULE 2: UNIVERSAL PATH ISOLATION
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        # Limitless Asset Library (Scans automatically, no hardcoding)
        self.char_lib_dir = os.path.join(self.workspace_dir, "Omni_Local_Assets", "3d_characters")
        self.manifest_path = os.path.join(self.char_lib_dir, "dynamic_character_manifest.json")
        self.output_blueprint = os.path.join(self.module_c_dir, "23_character_placements.json")
        
        # System States (RULE 7)
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_dir, "global_config.json")
        
        # APIs (RULE 6)
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        for d in [self.script_dir, self.env_dir, self.module_c_dir, self.char_lib_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    # LIMITLESS FEATURE: DYNAMIC FOLDER SCANNING (No Hardcoded Names)
    def _build_dynamic_manifest(self):
        chars = []
        if os.path.exists(self.char_lib_dir):
            for filename in os.listdir(self.char_lib_dir):
                if filename.endswith(".blend"):
                    # Auto-generate semantic tags from filename (e.g., ch_evil_boss_v2.blend -> [evil, boss])
                    clean_name = filename.replace(".blend", "").replace("ch_", "")
                    tags = re.findall(r'[a-zA-Z]+', clean_name.lower())
                    char_id = hashlib.md5(filename.encode()).hexdigest()[:8] # Unique ID to prevent name collisions
                    
                    chars.append({
                        "id": f"char_{char_id}",
                        "name": clean_name.replace("_", " ").title(),
                        "file_name": filename,
                        "tags": tags
                    })
        
        # Failsafe if folder is empty
        if not chars:
            chars.append({"id": "char_proxy_000", "name": "Procedural Proxy", "file_name": "dummy_proxy.blend", "tags": ["generic", "proxy", "dummy"]})
            
        manifest = {"characters": chars}
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)
        return manifest

    def _load_master_config(self):
        default_config = {"global_style": "realistic", "blender_executable": "blender"}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except: pass
        return default_config

    # MULTI-CHARACTER DEMAND PARSER
    def _load_character_demands(self, scene_name):
        script_file = os.path.join(self.script_dir, f"{scene_name}_matrix_state.json")
        # Now returns a LIST of demands for multiple characters
        demands = ["A protagonist standing in the center"]
        if os.path.exists(script_file):
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "characters_in_scene" in data and isinstance(data["characters_in_scene"], list):
                        demands = data["characters_in_scene"]
                    else:
                        demands = [data.get("action_description", demands[0])]
            except: pass
        return demands

    def _clean_json_response(self, raw_text):
        try:
            cleaned = re.sub(r'```(?:json)?\n(.*?)```', r'\1', raw_text, flags=re.DOTALL).strip()
            return json.loads(cleaned)
        except:
            start = raw_text.find("[") if "[" in raw_text else raw_text.find("{")
            end = raw_text.rfind("]") if "]" in raw_text else raw_text.rfind("}")
            if start != -1 and end != -1:
                try: return json.loads(raw_text[start:end+1])
                except: pass
            return None

    # RULE 10: OFFLINE MATH/LOGIC FALLBACK FOR MULTIPLE CHARACTERS
    def _fuzzy_fallback_matcher(self, demands, manifest):
        results = []
        for i, demand in enumerate(demands):
            demand_words = set(re.findall(r'\w+', demand.lower()))
            best_match = manifest["characters"][0]
            highest_score = -1
            
            for char in manifest.get("characters", []):
                tags_words = set([t.lower() for t in char["tags"]] + char["name"].lower().split())
                score = len(demand_words.intersection(tags_words))
                if score > highest_score:
                    highest_score = score
                    best_match = char
                    
            # Auto-spacing logic for multiple characters on X-axis
            offset_x = (i * 2.0) - ((len(demands)-1) * 1.0)
            
            results.append({
                "demand": demand,
                "matched_id": best_match["id"],
                "matched_file": best_match["file_name"],
                "generate_new_asset": (highest_score == 0),
                "spawn_offset_xyz": [offset_x, 0.0, 0.0]
            })
        return results

    # RULE 6: MULTI-ENTITY SEMANTIC AI
    def _query_ai_matcher(self, scene_name, demands, manifest, style):
        self.log(f"Consulting AAA Casting AI for '{scene_name}' (Characters: {len(demands)})...", "INFO")
        
        ai_prompt = f"""
        You are an elite Casting Director AI. Style: '{style.upper()}'.
        Scene requires the following characters: {json.dumps(demands)}
        
        Local Assets Database (Dynamically Scanned): {json.dumps(manifest['characters'])}
        
        MISSION: For EACH demanded character, match them to the most logical asset in the database. 
        If two identical characters are requested, they can use the same file. 
        Set realistic 'spawn_offset_xyz' coordinates so they aren't standing inside each other (e.g. X = -2 for char 1, X = 2 for char 2).
        
        Return exactly a JSON ARRAY of objects:
        [
            {{
                "demand": "Original string",
                "matched_id": "id from database",
                "matched_file": "exact_file_name.blend",
                "generate_new_asset": false (true ONLY if no logical match exists at all),
                "spawn_offset_xyz": [X, Y, Z]
            }}
        ]
        """

        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self._clean_json_response(res_text)
                    if isinstance(parsed, list): return parsed
            except: pass

        self.log("AI API failed or returned bad format. Engaging Offline Multi-Matcher.", "WARNING")
        return self._fuzzy_fallback_matcher(demands, manifest)

    # RULE 13 (Multi-Socket Protocol), RULE 12 (Kinetic), Collision Avoidance
    def _generate_blender_script(self, target_stage_blend, match_data, style):
        safe_stage = target_stage_blend.replace("\\", "/")
        matches_json = json.dumps(match_data)
        safe_lib_dir = self.char_lib_dir.replace("\\", "/")
        
        script_content = f"""
import bpy
import os
import json

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_stage}")

    matches = json.loads('''{matches_json}''')
    char_lib = "{safe_lib_dir}"
    focus_target = bpy.data.objects.get("OMNIMATRIX_Focus_Target")
    
    # Clean old characters safely
    for obj in bpy.data.objects:
        if obj.name.startswith("CHAR_SOCKET_") or obj.name.startswith("OMNI_CHAR_"):
            bpy.data.objects.remove(obj, do_unlink=True)
            
    head_locations = []

    for index, char_data in enumerate(matches):
        if char_data.get("generate_new_asset"):
            continue
            
        file_name = char_data.get("matched_file")
        char_path = os.path.join(char_lib, file_name)
        offset = char_data.get("spawn_offset_xyz", [0,0,0])
        
        # UNIQUE SOCKET FOR EVERY CHARACTER (Collision Protection)
        socket_name = f"CHAR_SOCKET_{{index}}"
        bpy.ops.object.empty_add(type='CUBE', radius=1.0, location=(offset[0], offset[1], offset[2]))
        socket = bpy.context.active_object
        socket.name = socket_name

        is_valid = os.path.exists(char_path) and "OMNIMATRIX DUMMY" not in open(char_path, 'r', errors='ignore').read(50)

        if not is_valid:
            print(f"Forging Procedural Proxy for Socket {{index}}")
            bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=1.6, location=(offset[0], offset[1], offset[2] + 0.8))
            body = bpy.context.active_object
            body.name = f"OMNI_CHAR_{{index}}_Body"
            body.parent = socket
            
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(offset[0], offset[1], offset[2] + 1.8))
            head = bpy.context.active_object
            head.name = f"OMNI_CHAR_{{index}}_Head"
            head.parent = body
            
            mat = bpy.data.materials.new(name=f"Proxy_Mat_{{index}}")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            bsdf.inputs['Base Color'].default_value = (0.2 * index, 0.5, 0.8 - (0.2 * index), 1.0)
            body.data.materials.append(mat)
            head.data.materials.append(mat)
            
            head_locations.append(head)
            
        else:
            # MULTI-CHARACTER APPEND LOGIC WITH NAMESPACE ISOLATION
            print(f"Appending Real Rig for Socket {{index}}...")
            pre_append_objects = set(bpy.data.objects)
            
            with bpy.data.libraries.load(char_path, link=False) as (data_from, data_to):
                # Prefer Collections, fallback to objects
                col_names = [c for c in data_from.collections if "CH_" in c or "Char" in c]
                if col_names: data_to.collections = col_names
                else: data_to.objects = [o for o in data_from.objects if o.type in ['ARMATURE', 'MESH']]

            appended_objects = []
            
            # Link Collections
            for col in data_to.collections:
                if col.name not in bpy.context.scene.collection.children:
                    bpy.context.scene.collection.children.link(col)
                    for obj in col.objects:
                        appended_objects.append(obj)
                        
            # Link standalone objects
            for obj in data_to.objects:
                if obj and obj.name not in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.link(obj)
                    appended_objects.append(obj)
            
            post_append_objects = set(bpy.data.objects) - pre_append_objects
            appended_objects.extend(list(post_append_objects))

            # Find rig and rename everything to prevent collisions (e.g., if appending 2 Gokus)
            rig = None
            for obj in set(appended_objects):
                obj.name = f"OMNI_CHAR_{{index}}_{{obj.name}}"
                if obj.type == 'ARMATURE':
                    rig = obj
                    
            if rig:
                rig.parent = socket
                rig.location = (0,0,0)
                # Head height approximation for camera target
                bpy.ops.object.empty_add(type='SPHERE', radius=0.1, location=(offset[0], offset[1], offset[2] + 1.6))
                head_proxy = bpy.context.active_object
                head_proxy.name = f"Head_Tracker_{{index}}"
                head_proxy.parent = rig
                head_locations.append(head_proxy)

    # --- CINEMATIC MULTI-TARGET FOCUS (Rule 13 Upgrade) ---
    # If there are multiple characters, camera focus should be the center point between them!
    if focus_target and head_locations:
        for c in focus_target.constraints:
            focus_target.constraints.remove(c)
            
        if len(head_locations) == 1:
            copy_loc = focus_target.constraints.new('COPY_LOCATION')
            copy_loc.target = head_locations[0]
        else:
            # Create a median point tracker for epic anime showdown shots
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
            median_empty = bpy.context.active_object
            median_empty.name = "OMNIMATRIX_Fight_Center"
            
            for head in head_locations:
                copy = median_empty.constraints.new('COPY_LOCATION')
                copy.target = head
                copy.influence = 1.0 / len(head_locations) # Distribute weight evenly
                
            copy_focus = focus_target.constraints.new('COPY_LOCATION')
            copy_focus.target = median_empty

    print("OMNIMATRIX_BLENDER_SUCCESS")
    bpy.ops.wm.save_as_mainfile(filepath="{safe_stage}")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_multi_char_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def place_characters_in_stages(self):
        self.log("Initializing Dynamic Multi-Character Casting Director...", "INFO")

        state = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
            except: pass
                
        if state.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{state.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        # 1. Dynamically read directory (No Hardcoding)
        manifest = self._build_dynamic_manifest()
        
        config = self._load_master_config()
        blender_executable = config.get("blender_executable", "blender")
        master_blueprint = {}
        
        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("No 3D environments found. Exiting...", "WARNING")
            sys.exit(0)
        
        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                scene_name = filename.replace("_stage.blend", "").replace(".blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                # 2. Get multiple character demands
                demands = self._load_character_demands(scene_name)
                
                # 3. AI Matches array of characters
                matches = self._query_ai_matcher(scene_name, demands, manifest, config.get("global_style", "realistic"))
                
                self.log(f"[{scene_name}] Forging {len(matches)} Characters into Scene...", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, matches, config)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                        self.log(f"Dynamic Cast successfully injected into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = matches
                    else:
                        self.log(f"Blender failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        state["last_active_agent"] = self.agent_name
        state["next_agent"] = "Ai_Agent_24_Kinetic_Animation_Retargeter"
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
        
        self.log(f"Dynamic Limitless Casting Complete! Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    selector = AiAgent23UniversalCharacterAssetSelector()
    selector.place_characters_in_stages()
