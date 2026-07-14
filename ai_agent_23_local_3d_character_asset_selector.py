import os
import re
import sys
import json
import urllib.request
import urllib.error

class Local3DCharacterAssetSelector:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 23: local_3d_character_asset_selector"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        # Hamari local 3D assets directory jahan saare 3D characters store hote hain
        self.local_assets_dir = os.path.join(self.workspace_dir, "local_3d_library")
        
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        if not os.path.exists(self.local_assets_dir):
            os.makedirs(self.local_assets_dir)
            # Creating dummy database files for demonstration
            self._create_mock_local_library()

    def _create_mock_local_library(self):
        # Mock database banata hai taake system bina kisi real file ke bhi testing me behave kare
        mock_library = {
            "characters": [
                {"id": "char_001", "name": "Gojo Satoru", "file_path": "anime_gojo_unmasked.blend", "tags": ["male", "silver hair", "blue eyes", "sorcerer", "modern clothing"]},
                {"id": "char_002", "name": "Sasuke Uchiha", "file_path": "ninja_sasuke_susanoo.fbx", "tags": ["male", "black hair", "sharingan", "sword", "ninja"]},
                {"id": "char_003", "name": "Cyber Samurai", "file_path": "cyber_samurai_heavy.obj", "tags": ["robot", "armor", "neon lights", "sword", "futuristic"]}
            ]
        }
        db_path = os.path.join(self.local_assets_dir, "asset_database_manifest.json")
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(mock_library, f, indent=4)
        print(f"[{self.agent_name}] Local Asset Database created at '{db_path}'")

    def _load_upstream_storyboard(self):
        # Visual Storyboard se character demands ko scan karta hai
        storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        demanded_characters = []

        if os.path.exists(storyboard_path):
            try:
                with open(storyboard_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for panel in data.get("storyboard_panels", []):
                    desc = panel.get("visual_prompt", "")
                    demanded_characters.append({
                        "timestamp_sec": panel.get("timestamp_sec", 0.0),
                        "required_description": desc
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Storyboard load warning: {str(e)}")

        if not demanded_characters:
            print(f"[{self.agent_name}] Workspace Alert: Storyboard missing. Using script demand profiles.")
            demanded_characters = [
                {"timestamp_sec": 0.0, "required_description": "Gojo Satoru stands under a starry sky with his blindfold off"},
                {"timestamp_sec": 5.0, "required_description": "A mysterious ninja warrior activates his dark energy sword"}
            ]

        return demanded_characters

    def _load_local_db_manifest(self):
        # Local library manifest load karta hai matching check karne ke liye
        db_path = os.path.join(self.local_assets_dir, "asset_database_manifest.json")
        if os.path.exists(db_path):
            try:
                with open(db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"characters": []}

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

    def _save_to_workspace(self, data, filename="23_character_asset_selector_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Selected character asset blueprints saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save selection state: {str(e)}")
            return None

    def select_character_assets(self):
        demands = self._load_upstream_storyboard()
        local_db = self._load_local_db_manifest()
        
        print(f"[{self.agent_name}] AI Matching Engine active. Semantic scans initiated over {len(local_db['characters'])} local assets...")

        system_prompt = (
            "You are an AI 3D Technical Lead and Character Supervisor.\n"
            "Your task is to analyze character descriptions from a video script and match them against a local database of 3D assets (.blend, .fbx, .obj).\n"
            "If a local asset matches well semantically, map it. "
            "If NO local asset matches (e.g. the description is completely different or asks for a non-existent character), "
            "set 'generate_new_asset' to true so downstream generative engines know to build it.\n"
            "Output exactly 1 selection match for each dynamic segment inside a list named 'character_allocations' with these keys:\n"
            "- 'timestamp_sec': float matching the trigger timestamp.\n"
            "- 'demanded_description': string matching the visual prompt input.\n"
            "- 'matched_local_asset_id': string representing the matched asset ID (or 'NONE' if no match exists).\n"
            "- 'matched_file_name': string representing the file name (or 'NONE' if no match exists).\n"
            "- 'generate_new_asset': boolean (true if no local match is found and we must generate it from scratch, false otherwise).\n"
            "- 'confidence_score': float (scale from 0.0 to 1.0; 1.0 means perfect match, 0.0 means completely new).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'character_allocations'. "
            "Do not write conversational sentences, explanations, code blocks or backticks. Return valid JSON only."
        )

        user_prompt = (
            f"Local Character Database Manifest:\n{json.dumps(local_db, indent=2)}\n\n"
            f"Demanded Script Characters:\n{json.dumps(demands, indent=2)}"
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
                    {"role": "user", "content": user_prompt}
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
                    {"role": "user", "content": user_prompt}
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
                    "character_allocations": structured_output.get("character_allocations", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Triggering semantic local matching logic.")
            return self._execute_procedural_fallback(demands, local_db)

    def _execute_procedural_fallback(self, demands, local_db):
        # Semantic string matching math in case LLM is offline
        allocations = []
        for d in demands:
            desc_lower = d.get("required_description", "").lower()
            ts = float(d.get("timestamp_sec", 0.0))
            
            best_match = None
            best_score = 0.0
            
            for asset in local_db.get("characters", []):
                # Calculate matching tags
                name_parts = asset.get("name", "").lower().split()
                matches = sum(1 for part in name_parts if part in desc_lower)
                matches += sum(1 for tag in asset.get("tags", []) if tag in desc_lower)
                
                score = matches / max(1, len(name_parts) + len(asset.get("tags", [])))
                if score > best_score:
                    best_score = score
                    best_match = asset

            # Threshold for local matching
            if best_match and best_score > 0.15:
                allocations.append({
                    "timestamp_sec": ts,
                    "demanded_description": d.get("required_description"),
                    "matched_local_asset_id": best_match["id"],
                    "matched_file_name": best_match["file_path"],
                    "generate_new_asset": False,
                    "confidence_score": round(best_score, 2)
                })
            else:
                # Flag to generate as it doesn't exist locally!
                allocations.append({
                    "timestamp_sec": ts,
                    "demanded_description": d.get("required_description"),
                    "matched_local_asset_id": "NONE",
                    "matched_file_name": "NONE",
                    "generate_new_asset": True,
                    "confidence_score": 0.0
                })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural AI Match Fallback)",
            "character_allocations": allocations
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    selector = Local3DCharacterAssetSelector()
    output = selector.select_character_assets()
    
    print("\n--- Z-NET BLENDER ENGINE: AGENT 23 CHARACTER SELECTION COMPLETE ---")
    print(f"Total Character tracks mapped: {len(output['character_allocations'])}")
    for alloc in output["character_allocations"]:
        status = "GENERATIVE ACTION REQUIRED" if alloc["generate_new_asset"] else f"MATCHED LOCAL ({alloc['matched_file_name']})"
        print(f"Time: {alloc['timestamp_sec']}s | Demand: '{alloc['demanded_description'][:40]}...' | Status: {status}")
    print("-------------------------------------------------------------------")
