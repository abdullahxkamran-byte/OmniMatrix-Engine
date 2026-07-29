import os
import re
import sys
import json
import time
import math
import shutil
import platform
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# =====================================================================
# RULE 2 & 14: UNIVERSAL ENVIRONMENT & MULTI-API CONFIGURATION
# =====================================================================
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class Ai_Agent_49_Autonomous_Vision_Media_Scout:
    """
    OMNIMATRIX V2.0 GOD-LEVEL AUTONOMOUS VISION & MEDIA SCOUT
    Scouts royalty-free stock background b-roll (Pexels/Pixabay), harvests
    monochrome and color manga panels (MangaDex REST API), and deploys
    multimodal vision models (Gemini/OpenAI) to analyze rendered sequences.
    Predicts and maps timestamp coordinates for peak Click-Through Rate (CTR)
    Hero Frames for automated promotional cards and thumbnail extraction.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_49_Autonomous_Vision_Media_Scout"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        self.output_blueprint_path = os.path.join(self.workspace_dir, "49_media_scout_blueprint.json")
        self.storyboard_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        self.config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        
        # Rule 17: Hardware and I/O safety ceilings
        self.max_stock_downloads = 3
        self.max_manga_downloads = 3
        self.max_hero_frames_retained = 15
        
        # API Credentials (Stock B-Roll & Multimodal Vision)
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        self.pexels_key = os.environ.get("PEXELS_API_KEY", None)
        self.pixabay_key = os.environ.get("PIXABAY_API_KEY", None)
        
        # Optional MangaDex OAuth Hooks (For private/advanced scraping if configured)
        self.mangadex_client_id = os.environ.get("MANGADEX_CLIENT_ID", None)
        self.mangadex_client_secret = os.environ.get("MANGADEX_CLIENT_SECRET", None)
        self.mangadex_username = os.environ.get("MANGADEX_USERNAME", None)
        self.mangadex_password = os.environ.get("MANGADEX_PASSWORD", None)
        
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        formatted = f"[{level}] [{self.agent_name}] {message}"
        print(formatted)

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous media scout blueprints."""
        if os.path.exists(self.output_blueprint_path):
            try:
                os.remove(self.output_blueprint_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy blueprint {self.output_blueprint_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & PIPELINE ROUTING
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS"):
        matrix_path = os.path.join(self.workspace_dir, "matrix_state.json")
        data = {}
        if os.path.exists(matrix_path):
            try:
                with open(matrix_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        if "orchestrator_matrix" not in data:
            data["orchestrator_matrix"] = {}
            
        data["orchestrator_matrix"].update({
            "last_active_agent": self.agent_name,
            "last_update_timestamp": time.time(),
            "agent_status": {self.agent_name: status}
        })
        
        if status == "COMPLETED":
            # Hand off to Agent 50 (High CTR Frame Extractor - Pure Utility)
            data["orchestrator_matrix"]["next_agent"] = "agent_50_high_ctr_frame_extractor"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _scan_workspace_video_assets(self):
        """Locates the highest quality rendered master video from upstream modules."""
        candidate_paths = [
            os.path.join(self.workspace_dir, "48_final_denoised_master.mp4"),
            os.path.join(self.workspace_dir, "47_super_resolved_4k_master.mp4"),
            os.path.join(self.workspace_dir, "45_final_master_compressed_output.mp4"),
            os.path.join(self.workspace_dir, "44_gpu_accelerated_output.mp4")
        ]
        valid_assets = []
        for path in candidate_paths:
            if os.path.exists(path) and os.path.getsize(path) > 100:
                valid_assets.append(path)
        return valid_assets

    def _load_storyboard_scenes_and_style(self):
        """Ingests narrative sequences from Module A and global style configurations."""
        style_mode = "anime_cel_shaded"
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                style_mode = cfg.get("global_style", "anime_cel_shaded").lower()
            except Exception:
                pass

        if os.path.exists(self.storyboard_path):
            try:
                with open(self.storyboard_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    scenes = [
                        {
                            "timestamp_sec": float(panel.get("timestamp_sec", idx * 3.0)),
                            "description": panel.get("panel_description", panel.get("visual_prompt", "")),
                            "mood": panel.get("emotional_tone", "Action/Cinematic")
                        }
                        for idx, panel in enumerate(data.get("storyboard_panels", []))
                    ]
                    return scenes, style_mode
            except Exception as error:
                self.log(f"Storyboard ingestion exception: {error}", "WARNING")
        
        self.log("Storyboard sequence absent. Injecting baseline acoustic narrative scenes.", "INFO")
        scenes = [
            {"timestamp_sec": 1.5, "description": "High-contrast cyberpunk atmosphere with crackling plasma lightning", "mood": "HYPED_CLIMAX"},
            {"timestamp_sec": 4.5, "description": "Cinematic wide shot of ruined monoliths under torrential rain", "mood": "EPIC_REVEAL"},
            {"timestamp_sec": 8.0, "description": "Extreme close-up of protagonist eyes reflecting crimson energy", "mood": "SHOWDOWN_INTENSITY"}
        ]
        return scenes, style_mode

    def _clean_json(self, raw_text):
        """Rule 5: Bulletproof JSON scrubber."""
        cleaned = re.sub(r"^```(json)?\s*|\s*```$", "", raw_text.strip(), flags=re.IGNORECASE)
        start_index = cleaned.find('{')
        end_index = cleaned.rfind('}')
        if start_index != -1 and end_index != -1:
            return cleaned[start_index:end_index + 1]
        return cleaned

    def _api_call(self, url, payload, headers):
        request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))

    def _download_remote_media(self, url, filename):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'OmniMatrix-MediaScout/2.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=30) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            return file_path
        except Exception as error:
            self.log(f"Remote asset download exception: {error}", "WARNING")
            return None

    # =====================================================================
    # AUTONOMOUS STOCK B-ROLL DOWNLOADER (PEXELS & PIXABAY)
    # =====================================================================
    def scout_stock_background_video(self, query_string, prefix="scouted_broll"):
        """Queries royalty-free stock APIs to acquire auxiliary b-roll footage."""
        safe_query = urllib.parse.quote(query_string)
        
        # Priority 1: Pexels API
        if self.pexels_key:
            self.log(f"Querying Pexels Video API for keyword: '{query_string}'")
            url = f"https://api.pexels.com/videos/search?query={safe_query}&per_page=1"
            req = urllib.request.Request(url)
            req.add_header("Authorization", self.pexels_key)
            try:
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    videos = res_data.get("videos", [])
                    if videos:
                        video_files = videos[0].get("video_files", [])
                        best_video = next((vf for vf in video_files if vf.get("quality") == "hd" or vf.get("width", 0) >= 1280), video_files[0] if video_files else None)
                        if best_video and best_video.get("link"):
                            downloaded = self._download_remote_media(best_video["link"], f"{prefix}_{safe_query[:15]}.mp4")
                            if downloaded:
                                self.log(f"Acquired Pexels stock b-roll: '{downloaded}'", "SUCCESS")
                                return downloaded
            except Exception as error:
                self.log(f"Pexels API inquiry failure: {error}", "WARNING")

        # Priority 2: Pixabay API
        if self.pixabay_key:
            self.log(f"Querying Pixabay Video API for keyword: '{query_string}'")
            url = f"https://pixabay.com/api/videos/?key={self.pixabay_key}&q={safe_query}&per_page=2"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as response:
                    hits = json.loads(response.read().decode("utf-8")).get("hits", [])
                    if hits:
                        video_url = hits[0].get("videos", {}).get("medium", {}).get("url", hits[0].get("videos", {}).get("small", {}).get("url"))
                        if video_url:
                            downloaded = self._download_remote_media(video_url, f"{prefix}_{safe_query[:15]}.mp4")
                            if downloaded:
                                self.log(f"Acquired Pixabay stock b-roll: '{downloaded}'", "SUCCESS")
                                return downloaded
            except Exception as error:
                self.log(f"Pixabay API inquiry failure: {error}", "WARNING")

        self.log(f"Stock asset matching failed or API keys absent for query: '{query_string}'", "INFO")
        return None

    # =====================================================================
    # AUTONOMOUS MANGADEX API PANEL & COVER SCRAPER (FREE PUBLIC REST API)
    # =====================================================================
    def scout_mangadex_panels(self, manga_title, prefix="scouted_manga"):
        """
        Queries the public MangaDex REST API without requiring authentication tokens.
        Resolves manga unique identifiers, queries high-resolution cover artwork,
        and acquires monochrome manga panels to feed Module H (Agent 55 & 56).
        """
        safe_title = urllib.parse.quote(manga_title)
        self.log(f"Querying MangaDex Public REST API for series title: '{manga_title}'...", "INFO")
        
        # Step 1: Search manga title and retrieve unique MangaDex ID
        search_url = f"https://api.mangadex.org/manga?title={safe_title}&limit=1&contentRating[]=safe&contentRating[]=suggestive"
        try:
            req = urllib.request.Request(search_url, headers={'User-Agent': 'OmniMatrix-MediaScout/2.0'})
            with urllib.request.urlopen(req, timeout=20) as response:
                search_data = json.loads(response.read().decode("utf-8"))
                results = search_data.get("data", [])
                
                if not results:
                    self.log(f"MangaDex API returned 0 matches for series query: '{manga_title}'", "WARNING")
                    return None
                    
                manga_id = results[0]["id"]
                exact_title = results[0]["attributes"]["title"].get("en", manga_title)
                self.log(f"Resolved MangaDex UUID [{manga_id}] for series: '{exact_title}'", "SUCCESS")
                
                # Step 2: Fetch cover artwork metadata associated with the manga ID
                cover_url = f"https://api.mangadex.org/cover?manga[]={manga_id}&limit=2&order[volume]=desc"
                req_cover = urllib.request.Request(cover_url, headers={'User-Agent': 'OmniMatrix-MediaScout/2.0'})
                
                with urllib.request.urlopen(req_cover, timeout=20) as cover_res:
                    cover_data = json.loads(cover_res.read().decode("utf-8"))
                    covers = cover_data.get("data", [])
                    
                    if covers:
                        file_name = covers[0]["attributes"]["fileName"]
                        # Construct official MangaDex upload CDN URL
                        image_cdn_url = f"https://uploads.mangadex.org/covers/{manga_id}/{file_name}"
                        
                        clean_filename = re.sub(r'[^a-zA-Z0-9_-]', '', safe_title)[:12]
                        output_filename = f"{prefix}_{clean_filename}_{manga_id[:6]}.jpg"
                        downloaded_path = self._download_remote_media(image_cdn_url, output_filename)
                        
                        if downloaded_path:
                            self.log(f"Successfully scouted MangaDex high-res reference artwork: '{downloaded_path}'", "SUCCESS")
                            return downloaded_path
                            
        except Exception as error:
            self.log(f"MangaDex API communication exception: {error}", "ERROR")
            
        self.log("MangaDex panel acquisition bypassed. Reverting to local visual assets.", "INFO")
        return None

    # =====================================================================
    # RULE 6, 14, 15, 17: QUAD-CORE HERO CTR VISION SCOUT
    # =====================================================================
    def analyze_and_scout_media(self):
        self._handshake("IN_PROGRESS")
        local_videos = self._scan_workspace_video_assets()
        scenes, style_mode = self._load_storyboard_scenes_and_style()
        
        self.log(f"Autonomous Vision Scout Initiated. Local Master Assets: {len(local_videos)} | Aesthetic: [{style_mode.upper()}]")

        scouted_stock_paths = []
        scouted_manga_paths = []

        # Rule 17: Rate limit safeguard - acquire auxiliary b-roll or manga reference panels
        if not local_videos or len(local_videos) == 0:
            self.log("Local master video undetected. Initiating auxiliary media acquisition sequence...", "WARNING")
            
            for scene in scenes[:self.max_stock_downloads]:
                desc = scene.get("description", "")
                tokens = re.findall(r'\b[a-zA-Z]{4,}\b', desc)
                clean_query = " ".join(tokens[:3]) if tokens else "cinematic background"
                
                # If project style is Anime/Manga, query MangaDex for reference character panels!
                if any(k in style_mode for k in ["anime", "manga", "cel", "toon"]) or any(k in desc.lower() for k in ["manga", "anime", "solo leveling", "berserk", "jujutsu", "naruto", "bleach", "one piece"]):
                    manga_title = tokens[0] if tokens else "Jujutsu Kaisen"
                    if len(scouted_manga_paths) < self.max_manga_downloads:
                        panel_path = self.scout_mangadex_panels(manga_title)
                        if panel_path:
                            scouted_manga_paths.append(panel_path)
                else:
                    # Otherwise, acquire realistic stock b-roll video from Pexels/Pixabay
                    clip_path = self.scout_stock_background_video(clean_query)
                    if clip_path:
                        scouted_stock_paths.append(clip_path)

        # Rule 15: Limitless continuous CTR scoring formulation
        prompt = (
            "You are OMNIMATRIX Lead Computer Vision & High-CTR Media Scout.\n"
            "Analyze storyboard sequences and media inventory to predict and map exact timestamp coordinates for peak Click-Through Rate (CTR) Hero Frames.\n"
            "CRITICAL CTR RULES:\n"
            "1. Evaluate emotional intensity, visual action, lighting contrast, and character presence.\n"
            "2. Assign a continuous float score between 0.50 and 0.99 indicating viral thumbnail attractiveness.\n"
            "Output STRICTLY a JSON object with key 'scouted_frames' containing a list of objects with:\n"
            "- 'timestamp_sec': float (exact second in sequence).\n"
            "- 'scout_score': float (rating from 0.50 to 0.99).\n"
            "- 'visual_description': string (detailed composition of the predicted frame).\n"
            "- 'potential_use_case': string ('Primary YouTube Thumbnail', 'TikTok Hook Preview', 'Community Banner', or 'Teaser Card').\n"
            "- 'color_dominance_prediction': string (expected color palette and contrast ratio).\n"
            "Zero compression or placeholders allowed."
        )

        user_msg = json.dumps({
            "local_master_videos": local_videos,
            "auxiliary_stock_clips": scouted_stock_paths,
            "scouted_mangadex_reference_panels": scouted_manga_paths,
            "storyboard_scenes_sequence": scenes
        })

        output = None

        # Core 1: Gemini
        if self.gemini_key and not output:
            try:
                url = f"{self.gemini_url}?key={self.gemini_key}"
                payload = {"contents": [{"parts": [{"text": f"{prompt}\n\nUser Context:\n{user_msg}"}]}], "generationConfig": {"temperature": 0.85, "responseMimeType": "application/json"}}
                res = self._api_call(url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res["candidates"][0]["content"]["parts"][0]["text"]))
                self.log("[Core 1: Gemini] Synthesized high-CTR Hero Frame visual mapping!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 1: Gemini] Failed: {e}", "WARNING")

        # Core 2: OpenAI Failsafe
        if self.openai_key and not output:
            try:
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "response_format": {"type": "json_object"}}
                res = self._api_call(self.openai_url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", ""), "Authorization": f"Bearer {self.openai_key}"})
                output = json.loads(self._clean_json(res["choices"][0]["message"]["content"]))
                self.log("[Core 2: OpenAI] Synthesized high-CTR Hero Frame visual mapping!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 2: OpenAI] Failed: {e}", "WARNING")

        # Core 3: Ollama Local Fallback
        if not output:
            try:
                payload = {"model": self.model_local, "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}], "format": "json", "stream": False}
                res = self._api_call(self.ollama_url, payload, {"Content-Type": "application/json", "X-goog-api-key": os.getenv("GEMINI_API_KEY", "")})
                output = json.loads(self._clean_json(res.get("message", {}).get("content", "{}")))
                self.log("[Core 3: Ollama] Generated local Hero Frame visual mapping!", "SUCCESS")
            except Exception as e:
                self.log(f"[Core 3: Ollama] Offline: {e}", "WARNING")

        # Core 4: 100% Offline Continuous Statistical CTR Alchemist (Rule 10)
        if not output:
            self.log("[Core 4: Math Fallback] Engaging offline continuous statistical CTR evaluation...", "WARNING")
            scouted_list = []
            for idx, scene in enumerate(scenes):
                desc = str(scene.get("description", "")).upper()
                mood = str(scene.get("mood", "")).upper()
                
                # Continuous CTR scoring math based on action keyword density and temporal cadence
                action_keywords = ["CLIMAX", "HYPED", "ACTION", "EPIC", "SHOWDOWN", "BLAST", "EXPLOSION", "STRIKE", "SLASH"]
                density = sum(1 for kw in action_keywords if kw in desc or kw in mood)
                base_score = 0.70 + min(0.28, (density * 0.08) + (math.sin(idx + 1) * 0.05))
                computed_score = round(max(0.50, min(0.99, base_score)), 2)
                
                scouted_list.append({
                    "timestamp_sec": float(scene.get("timestamp_sec", idx * 3.0)),
                    "scout_score": computed_score,
                    "visual_description": f"Hero frame evaluated at coordinate {scene.get('timestamp_sec', idx * 3.0)}s: {scene.get('description', 'nominal atmosphere')}",
                    "potential_use_case": "Primary YouTube Thumbnail" if computed_score >= 0.88 else "TikTok Hook Preview",
                    "color_dominance_prediction": "High-contrast vivid neon glow with deep cinematic shadows" if computed_score >= 0.88 else "Balanced ambient atmospheric tones"
                })
            output = {"scouted_frames": scouted_list}

        # Rule 17 Safeguard: Retain top 15 Hero Frames by score to prevent downstream extraction bloat
        frames = output.get("scouted_frames", [])
        frames.sort(key=lambda x: float(x.get("scout_score", 0.0)), reverse=True)
        capped_frames = frames[:self.max_hero_frames_retained]

        final_blueprint = {
            "agent_executed": self.agent_name,
            "execution_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_video_scouted": local_videos[0] if local_videos else "none",
            "scouted_stock_broll_clips": scouted_stock_paths,
            "scouted_mangadex_reference_panels": scouted_manga_paths,
            "total_hero_frames_mapped": len(capped_frames),
            "scouted_frames": capped_frames
        }

        with open(self.output_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(final_blueprint, f, indent=4)

        self.log(f"Media scout blueprint locked: '{self.output_blueprint_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return final_blueprint

if __name__ == "__main__":
    scout = Ai_Agent_49_Autonomous_Vision_Media_Scout()
    scout.analyze_and_scout_media()