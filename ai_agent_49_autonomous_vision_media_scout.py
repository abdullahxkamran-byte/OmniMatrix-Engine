import os
import re
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

# Manual .env loader utility
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

class AutonomousVisionMediaScout:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 49: autonomous_vision_media_scout"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        # API Keys from environment
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)
        self.pexels_api_key = os.environ.get("PEXELS_API_KEY", None)
        self.pixabay_api_key = os.environ.get("PIXABAY_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _scan_workspace_assets(self):
        potential_files = []
        check_paths = [
            os.path.join(self.workspace_dir, "48_final_denoised_clean.mp4"),
            os.path.join(self.workspace_dir, "47_super_resolved_4k_video.mp4"),
            os.path.join(self.workspace_dir, "45_final_compressed_output.mp4"),
            os.path.join(self.workspace_dir, "44_gpu_accelerated_output.mp4")
        ]

        for path in check_paths:
            if os.path.exists(path):
                potential_files.append(path)
                
        return potential_files

    def _load_storyboard_data(self):
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        scenes_data = []

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for panel in data.get("storyboard_panels", []):
                    scenes_data.append({
                        "timestamp_sec": panel.get("timestamp_sec", 0.0),
                        "description": panel.get("panel_description", ""),
                        "mood": panel.get("emotional_tone", "Action/Cinematic")
                    })
            except Exception:
                pass

        if not scenes_data:
            scenes_data = [
                {"timestamp_sec": 1.5, "description": "dark anime background with storm clouds and lightning", "mood": "HYPED_CLIMAX"},
                {"timestamp_sec": 4.2, "description": "cinematic retro neon city street raining at night", "mood": "EPIC_REVEAL"},
                {"timestamp_sec": 7.8, "description": "glowing stars celestial galaxy deep space background", "mood": "COOL_NIGHT_AESTHETIC"}
            ]

        return scenes_data

    def search_and_download_stock_video(self, query, filename_prefix="scouted_stock"):
        """Scouts and downloads background stock video footage from Pexels or Pixabay APIs."""
        safe_query = urllib.parse.quote(query)
        downloaded_file_path = None
        
        # Step 1: Try Pexels API
        if self.pexels_api_key:
            print(f"[{self.agent_name}] Querying Pexels Video API for query: '{query}'")
            url = f"https://api.pexels.com/videos/search?query={safe_query}&per_page=1"
            req = urllib.request.Request(url)
            req.add_header("Authorization", self.pexels_api_key)
            try:
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    videos = res_data.get("videos", [])
                    if videos:
                        video_files = videos[0].get("video_files", [])
                        # Select best resolution file
                        best_video = None
                        for vf in video_files:
                            if vf.get("quality") == "hd" or vf.get("width", 0) >= 1280:
                                best_video = vf
                                break
                        if not best_video and video_files:
                            best_video = video_files[0]
                            
                        if best_video:
                            video_url = best_video.get("link")
                            downloaded_file_path = self._download_file(video_url, f"{filename_prefix}_{safe_query[:20]}.mp4")
                            if downloaded_file_path:
                                print(f"[{self.agent_name}] Successfully downloaded asset from Pexels: {downloaded_file_path}")
                                return downloaded_file_path
            except Exception as e:
                print(f"[{self.agent_name}] Pexels API query failed or timed out: {str(e)}")

        # Step 2: Try Pixabay API as robust fallback
        if self.pixabay_api_key and not downloaded_file_path:
            print(f"[{self.agent_name}] Querying Pixabay Video API for query: '{query}'")
            url = f"https://pixabay.com/api/videos/?key={self.pixabay_api_key}&q={safe_query}&per_page=3"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    hits = res_data.get("hits", [])
                    if hits:
                        video_url = hits[0].get("videos", {}).get("medium", {}).get("url")
                        if not video_url:
                            video_url = hits[0].get("videos", {}).get("small", {}).get("url")
                        if video_url:
                            downloaded_file_path = self._download_file(video_url, f"{filename_prefix}_{safe_query[:20]}.mp4")
                            if downloaded_file_path:
                                print(f"[{self.agent_name}] Successfully downloaded asset from Pixabay: {downloaded_file_path}")
                                return downloaded_file_path
            except Exception as e:
                print(f"[{self.agent_name}] Pixabay API query failed or timed out: {str(e)}")

        print(f"[{self.agent_name}] No stock asset matches found online or API keys missing for query: '{query}'")
        return None

    def _download_file(self, url, filename):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Error downloading file: {str(e)}")
            return None

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

    def _save_to_workspace(self, data, filename="49_media_scout_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Media scout blueprint saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Error saving media scout data: {str(e)}")
            return None

    def analyze_and_scout_media(self):
        assets = self._scan_workspace_assets()
        scenes = self._load_storyboard_data()
        
        print(f"[{self.agent_name}] AI Computer Vision Scout online. Analyzing visual data structure...")

        # If no local videos exist, scout background footage dynamically
        scouted_stock_paths = []
        if not assets:
            print(f"[{self.agent_name}] No local video assets found. Starting dynamic stock video search...")
            for scene in scenes[:2]: # Search top 2 scene descriptions to avoid high rate limits
                description = scene.get("description", "")
                # Extract key noun phrases or use full scene description
                search_query = " ".join(description.split()[:4])  # Get first 4 words for clean search results
                downloaded_clip = self.search_and_download_stock_video(search_query)
                if downloaded_clip:
                    scouted_stock_paths.append(downloaded_clip)

        system_prompt = (
            "You are an advanced AI Video Content Specialist and Autonomous Media Scout.\n"
            "Your job is to analyze the available video files and storyboard data to detect, scout, and predict the exact timestamps of the most visually stunning, high-energy, and 'clickable' frames (Hero Frames) to be extracted for high-CTR thumbnails and promotional cards.\n"
            "Output a raw JSON object with the key 'scouted_frames' containing a list of objects with these parameters:\n"
            "- 'timestamp_sec': float (the scouted timestamp in seconds).\n"
            "- 'scout_score': float (rating of frame from 0.0 to 1.0 based on epic-level potential).\n"
            "- 'visual_description': string (what the visual content is predicted to contain).\n"
            "- 'potential_use_case': string (e.g., 'Primary Thumbnail Focus', 'TikTok Hook Preview', 'Community Post Banner').\n"
            "- 'color_dominance_prediction': string (e.g., 'Neon blue aura with high contrast dark background', 'Golden sparks with high shadow depth').\n"
            "Format your output STRICTLY as a raw JSON object. Do not output conversational text or backticks."
        )

        user_content = (
            f"Available Video Assets found in Workspace: {assets}\n"
            f"Scouted Online Stock Background Assets: {scouted_stock_paths}\n"
            f"Storyboard Scenes to scout:\n{json.dumps(scenes, indent=2)}"
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
                    {"role": "user", "content": user_content}
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
                    {"role": "user", "content": user_content}
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
                    "target_video_scouted": assets[0] if assets else "none",
                    "scouted_stock_assets": scouted_stock_paths,
                    "scouted_frames": structured_output.get("scouted_frames", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] AI scouting logic bypassed: {str(e)}. Triggering procedural vision algorithm.")
            return self._execute_procedural_fallback(assets, scenes, scouted_stock_paths)

    def _execute_procedural_fallback(self, assets, scenes, stock_paths):
        scouted_frames = []
        for scene in scenes:
            ts = scene.get("timestamp_sec", 1.0)
            mood = str(scene.get("mood", "")).upper()
            desc = scene.get("description", "")
            
            if "CLIMAX" in mood or "HYPED" in mood:
                score = 0.98
                use_case = "Primary Thumbnail Focus"
                colors = "Dynamic high-contrast warm glow and cold shadow clash"
            elif "REVEAL" in mood or "EPIC" in mood:
                score = 0.92
                use_case = "TikTok Hook Preview"
                colors = "Dramatic face-lighting with deep neon elements"
            else:
                score = 0.85
                use_case = "Community Post Banner"
                colors = "Cinematic atmospheric sky tones"

            scouted_frames.append({
                "timestamp_sec": ts,
                "scout_score": score,
                "visual_description": f"Extracted visual frame containing: {desc}",
                "potential_use_case": use_case,
                "color_dominance_prediction": colors
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Vision Fallback)",
            "target_video_scouted": assets[0] if assets else "none",
            "scouted_stock_assets": stock_paths,
            "scouted_frames": scouted_frames
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    scout = AutonomousVisionMediaScout()
    result = scout.analyze_and_scout_media()
    
    print("\n--- Z-NET AUTONOMOUS VISION SCOUT: AGENT 49 COMPLETE ---")
    print(f"Target Video Scanned: '{result.get('target_video_scouted', 'N/A')}'")
    print(f"Downloaded Background Stock Clips: {result.get('scouted_stock_assets', [])}")
    print(f"Total High-CTR Frames scouted and locked: {len(result.get('scouted_frames', []))}")
    for frame in result.get("scouted_frames", []):
        print(f"  Timestamp: {frame['timestamp_sec']}s | Score: {frame['scout_score']} -> {frame['potential_use_case']}")
        print(f"  Description: {frame['visual_description']}")
    print("---------------------------------------------------------")
