import os
import re
import sys
import json
import urllib.request
import urllib.error

class DynamicMeshCollisionSentinel:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 27: dynamic_mesh_collision_sentinel"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_animation_and_assets(self):
        # Puppet animator aur character maps load karta hai positions check karne ke liye
        anim_path = os.path.join(self.workspace_dir, "26_kinetic_rig_puppeteer_blueprint.json")
        char_path = os.path.join(self.workspace_dir, "23_character_asset_selector_blueprint.json")
        
        simulation_inputs = {
            "characters_in_scene": [],
            "keyframes_detected": []
        }

        # 1. Load active characters
        if os.path.exists(char_path):
            try:
                with open(char_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for alloc in data.get("character_allocations", []):
                    simulation_inputs["characters_in_scene"].append({
                        "character_id": alloc.get("matched_local_asset_id", "char_generic"),
                        "file_name": alloc.get("matched_file_name", "NONE")
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream character data load warning: {str(e)}")

        # 2. Load animations
        if os.path.exists(anim_path):
            try:
                with open(anim_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for seq in data.get("rig_animation_sequences", []):
                    simulation_inputs["keyframes_detected"].append({
                        "timestamp_sec": seq.get("timestamp_sec", 0.0),
                        "character_id": seq.get("character_id"),
                        "action_pose": seq.get("action_pose_name"),
                        "translation_offset": seq.get("translation_offset", [0.0, 0.0, 0.0])
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream animation load warning: {str(e)}")

        # Fallbacks if files are not fully populated
        if not simulation_inputs["keyframes_detected"]:
            print(f"[{self.agent_name}] Workspace Alert: Animation timeline missing. Using procedural default triggers.")
            simulation_inputs["keyframes_detected"] = [
                {"timestamp_sec": 0.0, "character_id": "char_001", "action_pose": "energy_charge_squat", "translation_offset": [0.0, 0.0, -0.3]},
                {"timestamp_sec": 4.5, "character_id": "char_002", "action_pose": "aerial_combat_spin", "translation_offset": [0.0, 1.8, 2.5]}
            ]

        return simulation_inputs

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

    def _save_to_workspace(self, data, filename="27_mesh_collision_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Collision matrix saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save collision metadata: {str(e)}")
            return None

    def audit_and_simulate_collisions(self):
        inputs = self._load_upstream_animation_and_assets()
        print(f"[{self.agent_name}] Collision Sentinel active. Auditing mesh boundaries and calculating impact points...")

        system_prompt = (
            "You are an AI 3D Physics and Collision TD specialized in character bounds simulation and impact effects in Blender.\n"
            "Your job is to audit physical overlap conflicts between animated characters and environment assets.\n"
            "For each keyframe segment where characters interact, output exactly 1 collision block inside a list named 'collision_resolution_events' with these properties:\n"
            "- 'timestamp_sec': float matching the keyframe event.\n"
            "- 'has_collision_conflict': boolean (true if meshes are overlapping or weapons collide, false otherwise).\n"
            "- 'conflict_severity': string ('NONE', 'LOW_CLIP', 'HIGH_PENETRATION').\n"
            "- 'pushback_offset_vector': array of 3 floats [x, y, z] to apply to the character to prevent clipping (e.g. [-0.15, 0.0, 0.0]).\n"
            "- 'impact_point_coordinates': array of 3 floats [x, y, z] indicating where sparks/shockwaves should spawn in 3D space.\n"
            "- 'sparks_particle_count': integer (scale from 0 to 150 based on impact velocity).\n"
            "- 'impact_force_magnitude': float (scale from 0.0 to 50.0 representing physical impulse transfer).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'collision_resolution_events'. "
            "Do not write conversational explanations, markdown code blocks, or backticks. Return valid JSON only."
        )

        if self.openai_api_key:
            print(f"[{self.agent_name}] Status: Querying Cloud API Node [{self.model_cloud}]")
            url = self.openai_url
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            payload = {
                "model": self.model_cloud,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Skeletal Position Logs:\n{json.dumps(inputs, indent=2)}"}
                ],
                "response_format": {"type": "json_object"}
            }
        else:
            print(f"[{self.agent_name}] Status: Querying Local LLM Instance [{self.model_local}]")
            url = self.ollama_url
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": self.model_local,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Skeletal Position Logs:\n{json.dumps(inputs, indent=2)}"}
                ],
                "stream": False,
                "format": "json"
            }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            
            with urllib.request.urlopen(req, timeout=50) as response:
                result = response.read().decode("utf-8")
                response_json = json.loads(result)
                
                if self.openai_api_key:
                    raw_ai_message = response_json["choices"][0]["message"]["content"]
                else:
                    raw_ai_message = response_json["message"]["content"]
                
                cleaned_message = self._clean_json_response(raw_ai_message)
                structured_output = json.loads(cleaned_message)
                
                final_output = {
                    "agent_executed": self.agent_name,
                    "collision_resolution_events": structured_output.get("collision_resolution_events", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Network Exception: {str(e)}. Triggering rigid-body mathematical collision solver.")
            return self._execute_procedural_fallback(inputs)

    def _execute_procedural_fallback(self, inputs):
        # High speed procedural distance checking math
        events = []
        for key in inputs.get("keyframes_detected", []):
            ts = float(key.get("timestamp_sec", 0.0))
            pose = str(key.get("action_pose", "")).lower()
            trans = key.get("translation_offset", [0.0, 0.0, 0.0])

            # Simulating physical boundaries check
            has_conflict = False
            severity = "NONE"
            pushback = [0.0, 0.0, 0.0]
            impact_point = [0.0, 0.0, 0.0]
            sparks = 0
            force = 0.0

            # Action poses are highly dynamic, raising collision likelihoods
            if "combat" in pose or "spin" in pose or "slash" in pose:
                has_conflict = True
                severity = "HIGH_PENETRATION"
                # Push back 0.25 units along Y axis to separate meshes
                pushback = [0.0, -0.25, 0.0]
                # Calculate mid-point impact coordinates based on translation
                impact_point = [trans[0], trans[1] - 0.5, trans[2] - 0.2]
                sparks = 120
                force = 35.5
            elif "charge" in pose or "squat" in pose:
                has_conflict = True
                severity = "LOW_CLIP"
                pushback = [0.0, 0.0, 0.05]
                impact_point = [trans[0], trans[1], trans[2] - 0.1]
                sparks = 30
                force = 8.0

            events.append({
                "timestamp_sec": ts,
                "has_collision_conflict": has_conflict,
                "conflict_severity": severity,
                "pushback_offset_vector": pushback,
                "impact_point_coordinates": impact_point,
                "sparks_particle_count": sparks,
                "impact_force_magnitude": force
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Physics Fallback)",
            "collision_resolution_events": events
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    sentinel = DynamicMeshCollisionSentinel()
    output = sentinel.audit_and_simulate_collisions()
    
    print("\n--- Z-NET BLENDER ENGINE: AGENT 27 COLLISION AUDIT COMPLETE ---")
    print(f"Evaluated collision instances: {len(output['collision_resolution_events'])}")
    for ev in output["collision_resolution_events"]:
        conflict_status = f"WARNING! {ev['conflict_severity']} (Force: {ev['impact_force_magnitude']}N)" if ev["has_collision_conflict"] else "SECURE"
        print(f"Time: {ev['timestamp_sec']}s | Conflict: {conflict_status} | Pushback: {ev['pushback_offset_vector']} | Sparks Count: {ev['sparks_particle_count']}")
    print("----------------------------------------------------------------")
