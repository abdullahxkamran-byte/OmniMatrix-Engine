import os
import re
import sys
import json
import urllib.request
import urllib.error

class AiColorGradingLUTMapper:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 39: color_grading_lut_mapper"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_moods(self):
        # Bloom/Glare (Agent 38) ya Storyboard (Agent 03) se mood profiles load karta hai
        glare_path = os.path.join(self.workspace_dir, "38_bloom_glare_compositor.json")
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        scene_contexts = []

        # Pehle Agent 38 ke dynamic post-processing logs check karte hain
        if os.path.exists(glare_path):
            try:
                with open(glare_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for p in data.get("bloom_glare_profiles", []):
                    scene_contexts.append({
                        "timestamp_sec": p.get("timestamp_sec", 0.0),
                        "mood_hint": "DYNAMIC_ACTION" if p.get("glare_type") == "streaks" else "ATMOSPHERIC"
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream glare compositor read warning: {str(e)}")

        # Agar glare data missing ho toh storyboard se emotional tones read karte hain
        if not scene_contexts and os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    scene_contexts.append({
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "mood_hint": panel.get("emotional_tone", "EPIC")
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Upstream storyboard read warning: {str(e)}")

        # Agar workspace me kuch bhi na mile toh baseline action values inject karte hain
        if not scene_contexts:
            print(f"[{self.agent_name}] Workspace Alert: No upstream mood context. Injecting default cinematic action cue.")
            scene_contexts = [
                {"timestamp_sec": 0.0, "mood_hint": "CLIMAX_SHOWDOWN"},
                {"timestamp_sec": 3.0, "mood_hint": "DEEP_SADNESS"}
            ]

        return scene_contexts

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

    def _save_to_workspace(self, data, filename="39_color_grading_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Color grading map saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save grading map: {str(e)}")
            return None

    def map_color_grading_luts(self):
        contexts = self._load_upstream_moods()
        print(f"[{self.agent_name}] Color Grading Engine active. Mapping cinematic anime color palettes and contrast levels...")

        system_prompt = (
            "You are a World-Class Cinematic Colorist and LUT Designer specialized in modern and retro anime color spaces.\n"
            "Your job is to analyze scene moods and map them to custom color grading presets and Lift/Gamma/Gain math for Blender's compositor.\n"
            "For each scene context, design exactly 1 color grading profile inside a list named 'color_grading_profiles' with these parameters:\n"
            "- 'timestamp_sec': float matching the scene timeline.\n"
            "- 'lut_preset_name': string (choose from: 'shinkai_vibrant_blues' for magical skies, 'ufotable_climax_high_contrast' for dark intense fights, 'vintage_90s_cel_soft' for nostalgic retro look, 'cyberpunk_neon_grade' for heavy magenta/teal tones, 'tragic_desaturated_gray' for sad flashbacks).\n"
            "- 'saturation_scale': float (how saturated the colors are; range 0.4 for flashback to 1.65 for high energy).\n"
            "- 'contrast_multiplier': float (dynamic range contrast adjustment; range 0.9 to 1.35).\n"
            "- 'lift_shadows_rgb': array of 3 floats representing [R, G, B] shadow offsets (e.g., [0.0, 0.02, 0.05] for slightly faded, cool-blue shadows).\n"
            "- 'gain_highlights_rgb': array of 3 floats representing [R, G, B] highlights offset (e.g., [1.05, 1.0, 0.95] for warm golden highlights).\n"
            "- 'color_wheels_gamma_rgb': array of 3 floats representing midtones [R, G, B] (default [1.0, 1.0, 1.0]).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'color_grading_profiles'. "
            "Do not write conversational descriptions, markdown code blocks, or backticks. Return valid JSON only."
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
                    {"role": "user", "content": f"Scene Context Logs:\n{json.dumps(contexts, indent=2)}"}
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
                    {"role": "user", "content": f"Scene Context Logs:\n{json.dumps(contexts, indent=2)}"}
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
                    "color_grading_profiles": structured_output.get("color_grading_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Loading procedural color math fallback.")
            return self._execute_procedural_fallback(contexts)

    def _execute_procedural_fallback(self, contexts):
        # Precise algorithmic fallback parsing emotional keys and applying custom color science
        profiles = []
        for ctx in contexts:
            ts = float(ctx.get("timestamp_sec", 0.0))
            mood = str(ctx.get("mood_hint", "")).upper()

            if "SAD" in mood or "DEEP" in mood or "FLASHBACK" in mood:
                # Tragic/Sad scene: Desaturated, moody cool-blue shadows
                preset = "tragic_desaturated_gray"
                sat = 0.55
                contrast = 0.95
                lift = [0.02, 0.02, 0.04]
                gain = [0.9, 0.9, 0.95]
                gamma = [1.0, 1.0, 1.05]
            elif "CLIMAX" in mood or "SHOWDOWN" in mood or "ACTION" in mood or "DYNAMIC" in mood:
                # High contrast combat scene: Deep blacks and dynamic highlights (Ufotable style)
                preset = "ufotable_climax_high_contrast"
                sat = 1.35
                contrast = 1.25
                lift = [-0.01, -0.02, 0.0]
                gain = [1.1, 1.05, 1.0]
                gamma = [1.0, 0.98, 1.0]
            else:
                # Beautiful, vibrant sky/outdoor look (Shinkai style)
                preset = "shinkai_vibrant_blues"
                sat = 1.5
                contrast = 1.1
                lift = [0.0, 0.01, 0.03]
                gain = [1.05, 1.0, 0.95]
                gamma = [1.02, 1.0, 1.0]

            profiles.append({
                "timestamp_sec": ts,
                "lut_preset_name": preset,
                "saturation_scale": sat,
                "contrast_multiplier": contrast,
                "lift_shadows_rgb": lift,
                "gain_highlights_rgb": gain,
                "color_wheels_gamma_rgb": gamma
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Color Fallback)",
            "color_grading_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    mapper = AiColorGradingLUTMapper()
    output = mapper.map_color_grading_luts()
    
    print("\n--- Z-NET COLOR GRADING DEPT: AGENT 39 LUT MAPPER COMPLETE ---")
    print(f"Total dynamic color profiles mapped: {len(output['color_grading_profiles'])}")
    for profile in output["color_grading_profiles"]:
        print(f"Time: {profile['timestamp_sec']}s | LUT Preset: '{profile['lut_preset_name']}'")
        print(f"  Saturation: {profile['saturation_scale']} | Contrast: {profile['contrast_multiplier']}")
        print(f"  Shadow Lift: {profile['lift_shadows_rgb']} | Highlight Gain: {profile['gain_highlights_rgb']}")
    print("----------------------------------------------------------------")
