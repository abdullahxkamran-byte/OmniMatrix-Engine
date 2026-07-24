# ==============================================================================
# Ai_Agent_32_Omni_LipSync_Actor_Deformer.py
# MODULE C: Blender 3D Heavy Infantry - (GOD-LEVEL FACIAL & LIP-SYNC ENGINE)
# ==============================================================================

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
                    # RULE 6: UNIVERSAL UPPERCASE API KEYS
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class AiAgent32OmniLipSyncActorDeformer:
    def __init__(self):
        # RULE 8: STRICT AI NAMING
        self.agent_name = "Ai_Agent_32_Omni_LipSync_Actor_Deformer"
        
        # RULE 2: UNIVERSAL PATH ISOLATION (No Hardcoded Drives)
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.script_dir = os.path.join(self.workspace_dir, "Module_A_Scripting")
        self.env_dir = os.path.join(self.workspace_dir, "Module_H_Generative", "3d_environments")
        self.module_c_dir = os.path.join(self.workspace_dir, "Module_C_Heavy_Infantry")
        
        self.output_blueprint = os.path.join(self.module_c_dir, "32_omni_lipsync_blueprint.json")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.config_file = os.path.join(self.workspace_dir, "global_config.json")
        
        # RULE 6: DUAL API FAILSAFES
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")

        for d in [self.script_dir, self.env_dir, self.module_c_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_master_config(self):
        default_config = {"global_style": "anime", "blender_executable": "blender"}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    default_config.update(json.load(f))
            except: pass
        return default_config

    def _load_upstream_context(self, scene_name):
        """Loads dialogue, emotion, and style from Master Matrix State (Rule 7)"""
        context = {
            "dialogue_text": "Target acquired. Engaging protocol.",
            "emotion_tone": "serious",
            "start_frame": 12
        }
        
        # We read the main state file to see what script/audio generated
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "dialogue" in data and data["dialogue"]:
                        context["dialogue_text"] = data["dialogue"]
                    if "emotion" in data:
                        context["emotion_tone"] = data["emotion"]
                    if "audio_start_frame" in data:
                        context["start_frame"] = data["audio_start_frame"]
            except: pass
                
        return context

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

    def _fallback_phonemes(self, context, style):
        start = context["start_frame"]
        words = context["dialogue_text"].split()
        frames = []
        curr_frame = start
        
        for w in words:
            frames.append({
                "frame_num": curr_frame, "syllable": w, 
                "viseme_A_O": 0.8, "viseme_E_I": 0.0, "viseme_BMP": 0.0, 
                "jaw_drop": 0.7, "emotion_intensity": 0.5, "blink_trigger": False
            })
            curr_frame += 4
            frames.append({
                "frame_num": curr_frame, "syllable": "-", 
                "viseme_A_O": 0.0, "viseme_E_I": 0.0, "viseme_BMP": 1.0, 
                "jaw_drop": 0.0, "emotion_intensity": 0.5, "blink_trigger": True
            })
            curr_frame += 3
            
        return {"keyframes": frames, "overall_emotion": context["emotion_tone"]}

    # LIMITLESS LINGUISTIC & EMOTION AI
    def _query_linguistic_brain(self, scene_name, context, style):
        self.log(f"Calculating Lip-Sync, Micro-Expressions & Blinks for '{scene_name}'...", "INFO")

        ai_prompt = f"""
        You are the Lead Facial Animator for the OmniMatrix Engine.
        Dialogue: "{context['dialogue_text']}"
        Tone/Emotion: {context['emotion_tone']}
        Visual Style: {style.upper()}
        Start Frame: {context['start_frame']}
        
        MISSION:
        Break down the dialogue into phonetic frames (assuming 24fps).
        
        STYLE RULES:
        - If ANIME: Use fewer, snappier frames (2-4 frame holds). Extreme jaw drops for shouts. Less frequent blinking.
        - If REALISTIC: Use granular, smooth bezier mapping per syllable. Natural blinking (every ~3-4 seconds).
        
        Add Micro-Expressions:
        - `blink_trigger` (boolean): Set true on pauses, commas, or end of words.
        - `emotion_intensity` (float 0-1): How hard eyebrows/facial muscles react on this syllable.
        
        Return EXACTLY 1 JSON object in this format:
        {{
            "overall_emotion": "{context['emotion_tone']}",
            "keyframes": [
                {{
                    "frame_num": integer, 
                    "syllable": "string", 
                    "viseme_A_O": float (0-1), 
                    "viseme_E_I": float (0-1), 
                    "viseme_BMP": float (0-1), 
                    "jaw_drop": float (0-1),
                    "emotion_intensity": float (0-1),
                    "blink_trigger": boolean
                }}
            ]
        }}
        """

        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_api_key}"
                payload = {"contents": [{"parts": [{"text": ai_prompt}]}]}
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    res_text = json.loads(response.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = self._clean_json_response(res_text)
                    if parsed and "keyframes" in parsed:
                        return parsed
            except: pass

        return self._fallback_phonemes(context, style)

    # GOD-LEVEL BLENDER SCRIPT: ARKit COMPATIBLE & PROCEDURAL ANIMATION
    def _generate_blender_script(self, blend_file_path, sync_data, style):
        safe_blend_path = blend_file_path.replace("\\", "/")
        frames_json = json.dumps(sync_data.get("keyframes", []))
        emotion = sync_data.get("overall_emotion", "neutral")
        
        # Omnimatrix Logic: Anime gets stepped keys (flapping), Realistic gets bezier (smooth)
        interp_type = "'CONSTANT'" if "anime" in style.lower() else "'BEZIER'"
        
        script_content = f"""
import bpy
import json
import random

try:
    bpy.ops.wm.open_mainfile(filepath="{safe_blend_path}")

    frames_data = json.loads('''{frames_json}''')
    interp_style = {interp_type}
    base_emotion = "{emotion}".lower()
    
    # 1. AAA Fuzzy Mapping (Supports ARKit, VRoid, CC4, and Custom Rigs)
    shape_map = {{
        "viseme_A_O": ["viseme_a_o", "v_aa", "v_ou", "jawopen", "a", "o", "mouth_open"],
        "viseme_E_I": ["viseme_e_i", "v_ee", "v_ih", "mouthsmile", "e", "i", "smile"],
        "viseme_BMP": ["viseme_bmp", "v_bmp", "mouthclose", "b", "m", "p", "closed"],
        "blink":      ["eye_close", "blink", "eyesclosed", "blink_l", "blink_r"],
        "emo_angry":  ["angry", "browdown", "browinnerdown", "mad"],
        "emo_sad":    ["sad", "browinnerup", "sorrow"],
        "emo_happy":  ["happy", "smile", "joy"]
    }}

    def find_shape_keys(mesh_obj, logical_name):
        keys = []
        if not mesh_obj.data.shape_keys: return keys
        target_list = shape_map.get(logical_name, [])
        for kb in mesh_obj.data.shape_keys.key_blocks:
            kb_lower = kb.name.lower()
            if any(t in kb_lower for t in target_list):
                keys.append(kb)
        return keys

    # 2. TARGET IDENTIFICATION & IDEMPOTENCY SCRUBBING
    char_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.data.shape_keys]
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE']
    
    if char_meshes:
        for mesh in char_meshes:
            # Idempotency: Scrub old lip-sync and blink data to prevent layering garbage
            if mesh.data.shape_keys.animation_data and mesh.data.shape_keys.animation_data.action:
                action = mesh.data.shape_keys.animation_data.action
                for logical_name in shape_map.keys():
                    sks = find_shape_keys(mesh, logical_name)
                    for sk in sks:
                        fc = action.fcurves.find('key_blocks["'+sk.name+'"].value')
                        if fc: action.fcurves.remove(fc)

            # 3. APPLY SHAPE KEYS (Lip-Sync, Emotions, Blinks)
            for fd in frames_data:
                f_num = fd["frame_num"]
                
                # Apply Lip Sync
                for l_name in ["viseme_A_O", "viseme_E_I", "viseme_BMP"]:
                    sks = find_shape_keys(mesh, l_name)
                    for sk in sks:
                        sk.value = fd.get(l_name, 0.0)
                        sk.keyframe_insert(data_path="value", frame=f_num)
                        
                # Apply Emotion Intensity
                emo_target = f"emo_{{base_emotion}}"
                emo_sks = find_shape_keys(mesh, emo_target)
                for sk in emo_sks:
                    sk.value = fd.get("emotion_intensity", 0.5)
                    sk.keyframe_insert(data_path="value", frame=f_num)
                        
                # Procedural Blinking Logic
                if fd.get("blink_trigger", False):
                    blink_sks = find_shape_keys(mesh, "blink")
                    for sk in blink_sks:
                        sk.value = 0.0
                        sk.keyframe_insert(data_path="value", frame=f_num - 2)
                        sk.value = 1.0
                        sk.keyframe_insert(data_path="value", frame=f_num)
                        sk.value = 0.0
                        sk.keyframe_insert(data_path="value", frame=f_num + 3)

            # Set Interpolation Mode (Anime vs Realism)
            if mesh.data.shape_keys.animation_data and mesh.data.shape_keys.animation_data.action:
                for fc in mesh.data.shape_keys.animation_data.action.fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = interp_style

    # 4. MICRO-MOVEMENT: AUTO HEAD BOBBING
    if armatures and frames_data:
        arm = armatures[0]
        head_bone = None
        for b_name in ["Head", "head", "Neck", "neck", "mixamorig:Head", "DEF-spine.006"]:
            if b_name in arm.pose.bones:
                head_bone = arm.pose.bones[b_name]
                break
                
        if head_bone:
            if not arm.animation_data: arm.animation_data_create()
            head_bone.rotation_mode = 'XYZ'
            
            # Scrub old head rotation
            if arm.animation_data.action:
                fc = arm.animation_data.action.fcurves.find('pose.bones["'+head_bone.name+'"].rotation_euler', index=0)
                if fc: arm.animation_data.action.fcurves.remove(fc)
            
            base_rot_x = head_bone.rotation_euler[0]
            
            for i, fd in enumerate(frames_data):
                f_num = fd["frame_num"]
                jaw_intensity = fd.get("jaw_drop", 0.0)
                
                # Bobbing formula (Anime gets sharper nods, realistic gets subtle movement)
                multiplier = 0.15 if interp_style == "'CONSTANT'" else 0.05
                bob_angle = jaw_intensity * multiplier
                direction = 1 if i % 2 == 0 else -1
                
                head_bone.rotation_euler[0] = base_rot_x + (bob_angle * direction)
                head_bone.keyframe_insert(data_path="rotation_euler", index=0, frame=f_num)

    bpy.ops.wm.save_as_mainfile(filepath="{safe_blend_path}")
    print("OMNIMATRIX_BLENDER_SUCCESS")

except Exception as e:
    print(f"OMNIMATRIX_ERROR: {{str(e)}}")
    import sys
    sys.exit(1)
"""
        script_path = os.path.join(self.module_c_dir, "temp_lipsync_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return script_path

    def execute_pipeline(self):
        self.log("Initializing Agent 32 (Omni Lip-Sync & Actor Deformer)...", "INFO")

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

        config = self._load_master_config()
        global_style = config.get("global_style", "anime").lower()
        blender_executable = config.get("blender_executable", "blender")
        master_blueprint = {}
        
        if not os.path.exists(self.env_dir) or not os.listdir(self.env_dir):
            self.log("No 3D environments found. Exiting...", "WARNING")
            sys.exit(0)
            
        for filename in os.listdir(self.env_dir):
            if filename.endswith(".blend"):
                scene_name = filename.replace("_stage.blend", "").replace(".blend", "")
                blend_file_path = os.path.join(self.env_dir, filename)
                
                context = self._load_upstream_context(scene_name)
                self.log(f"--- Acting Scene: {scene_name} | Dialogue: '{context['dialogue_text']}' ---", "INFO")
                
                sync_data = self._query_linguistic_brain(scene_name, context, global_style)
                self.log(f"AI Linguistics: Emotion [{sync_data.get('overall_emotion')}] | Frames Analyzed: {len(sync_data.get('keyframes', []))}", "INFO")
                
                script_path = self._generate_blender_script(blend_file_path, sync_data, global_style)
                command = [blender_executable, "-b", "-P", script_path]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True)
                    if "OMNIMATRIX_BLENDER_SUCCESS" in result.stdout:
                        self.log(f"God-Level Lip-Sync & Micro-Movements baked into {filename}", "SUCCESS")
                        master_blueprint[scene_name] = sync_data
                    else:
                        self.log(f"Blender build failed: {result.stdout[-300:]}", "ERROR")
                except Exception as e:
                    self.log(f"Execution failed: {str(e)}", "CRITICAL")
                    
                if os.path.exists(script_path):
                    os.remove(script_path)

        with open(self.output_blueprint, "w", encoding="utf-8") as f:
            json.dump(master_blueprint, f, indent=4)
            
        # RULE 7: STATE UPDATE FOR THE NEXT AGENT
        state["last_active_agent"] = self.agent_name
        # After Animation & Lip-Sync, we move to Lighting!
        state["next_agent"] = "Ai_Agent_33_Cinematic_Lighting_Director" 
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
            
        self.log(f"Facial Animation Complete. Handoff to {state['next_agent']}.", "SUCCESS")

if __name__ == "__main__":
    actor = AiAgent32OmniLipSyncActorDeformer()
    actor.execute_pipeline()
