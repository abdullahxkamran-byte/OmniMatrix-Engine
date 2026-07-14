import os
import re
import sys
import json
import urllib.request
import urllib.error

class ProceduralEnvironmentFractureEngine:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 30: procedural_environment_fracture_engine"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_collisions(self):
        # Collision Sentinel (Agent 27) se dynamic impact points aur force map karta hai
        collision_path = os.path.join(self.workspace_dir, "27_mesh_collision_blueprint.json")
        active_impacts = []

        if os.path.exists(collision_path):
            try:
                with open(collision_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for ev in data.get("collision_resolution_events", []):
                    # Hum sirf heavy impacts ko target karenge jo tabaahi macha sakein
                    if ev.get("has_collision_conflict", False) and ev.get("impact_force_magnitude", 0.0) > 15.0:
                        active_impacts.append({
                            "timestamp_sec": ev.get("timestamp_sec", 0.0),
                            "impact_point": ev.get("impact_point_coordinates", [0.0, 0.0, 0.0]),
                            "force": ev.get("impact_force_magnitude", 15.0)
                        })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream collision data load warning: {str(e)}")

        # Fallback agar collision map empty ya missing ho
        if not active_impacts:
            print(f"[{self.agent_name}] Workspace Alert: No heavy collision data. Injecting default destruction anchor.")
            active_impacts = [
                {"timestamp_sec": 4.5, "impact_point": [0.0, 1.5, 0.0], "force": 45.0}
            ]

        return active_impacts

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

    def _save_to_workspace(self, data, filename="30_environment_fracture_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Fracture configurations saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save fracture blueprint: {str(e)}")
            return None

    def design_procedural_fracture(self):
        impacts = self._load_upstream_collisions()
        print(f"[{self.agent_name}] Destruction Engine active. Calculating cell fracture cuts and debris physics...")

        system_prompt = (
            "You are a master Technical Director specialized in procedural environmental destruction and physics simulation for anime.\n"
            "Your job is to generate parameters for Blender's Cell Fracture modifier and physics rigid bodies based on impact points.\n"
            "For each heavy impact point, design exactly 1 destruction config block inside a list named 'fracture_events' with these keys:\n"
            "- 'timestamp_sec': float matching the impact time.\n"
            "- 'fracture_center_xyz': array of 3 floats representing the impact epicenter.\n"
            "- 'crack_pattern_type': string (choose from: 'radial_spiderweb' for punches, 'linear_split' for sword slashes, 'shattered_crust' for craters).\n"
            "- 'shatter_chunk_count': integer (defines how many mesh pieces are cut; scale from 15 for dry small impacts to 150 for massive ground-cratering attacks).\n"
            "- 'fracture_radius_meters': float (impact blast range scale; from 0.5 to 6.5 meters).\n"
            "- 'debris_mass_kg': float representing physical mass of individual chunks to define gravity weight (scale from 1.0 to 25.0 kg).\n"
            "- 'has_secondary_smoke_particles': boolean (set to true if the impact force is above 30.0 for extra anime smoke puff style).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'fracture_events'. "
            "Do not write conversational text, markdown blocks, or backticks. Return pure JSON only."
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
                    {"role": "user", "content": f"Active Impact Logs:\n{json.dumps(impacts, indent=2)}"}
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
                    {"role": "user", "content": f"Active Impact Logs:\n{json.dumps(impacts, indent=2)}"}
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
                    "fracture_events": structured_output.get("fracture_events", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Network Exception: {str(e)}. Running procedural fracture physics math.")
            return self._execute_procedural_fallback(impacts)

    def _execute_procedural_fallback(self, impacts):
        # Precise algorithmic destruction physics to divide static environments based on collision vectors
        events = []
        for imp in impacts:
            ts = float(imp.get("timestamp_sec", 0.0))
            pt = imp.get("impact_point", [0.0, 0.0, 0.0])
            force = float(imp.get("force", 15.0))

            # Scale destruction dynamically based on force magnitude
            if force > 35.0:
                pattern = "shattered_crust" # Extreme ground crater
                chunks = 110
                radius = 4.2
                mass = 18.5
                smoke = True
            elif force > 20.0:
                pattern = "radial_spiderweb" # Classic wall cracked
                chunks = 55
                radius = 2.0
                mass = 8.0
                smoke = True
            else:
                pattern = "linear_split" # Clean sword slash split
                chunks = 20
                radius = 0.8
                mass = 2.0
                smoke = False

            events.append({
                "timestamp_sec": ts,
                "fracture_center_xyz": pt,
                "crack_pattern_type": pattern,
                "shatter_chunk_count": chunks,
                "fracture_radius_meters": radius,
                "debris_mass_kg": mass,
                "has_secondary_smoke_particles": smoke
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Fracture Fallback)",
            "fracture_events": events
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    fracturer = ProceduralEnvironmentFractureEngine()
    output = fracturer.design_procedural_fracture()
    
    print("\n--- Z-NET DESTRUCTION ENGINE: AGENT 30 FRACTURE GENERATION COMPLETE ---")
    print(f"Environmental fracture events programmed: {len(output['fracture_events'])}")
    for event in output["fracture_events"]:
        print(f"Time: {event['timestamp_sec']}s | Type: '{event['crack_pattern_type']}' | Center: {event['fracture_center_xyz']}")
        print(f"Cut Fragments: {event['shatter_chunk_count']} | Blast Radius: {event['fracture_radius_meters']}m | Physics Mass: {event['debris_mass_kg']}kg | Smoke: {event['has_secondary_smoke_particles']}")
    print("-------------------------------------------------------------------------")
