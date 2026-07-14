import os
import re
import sys
import json
import urllib.request
import urllib.error

class AiVFXBloomGlareEngine:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 38: vfx_bloom_glare_engine"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_data(self):
        # Storyboard (Agent 03) se mood aur Stylized Fluids (Agent 37) se effects intensity read karta hai
        story_path = os.path.join(self.workspace_dir, "03_visual_sync_storyboarder.json")
        vfx_context = []

        if os.path.exists(story_path):
            try:
                with open(story_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for i, panel in enumerate(data.get("storyboard_panels", [])):
                    vfx_context.append({
                        "timestamp_sec": panel.get("timestamp_sec", float(i * 3.0)),
                        "visual_prompt": panel.get("visual_prompt", "battle"),
                        "mood_tone": panel.get("emotional_tone", "EPIC")
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Storyboard load warning: {str(e)}")

        # Fallback agar storyboard details accessible na hon
        if not vfx_context:
            print(f"[{self.agent_name}] Workspace Alert: No upstream contextual mood logs. Proceeding with extreme action baseline.")
            vfx_context = [
                {"timestamp_sec": 1.5, "visual_prompt": "energy blast collision", "mood_tone": "CLIMAX_HYPED"},
                {"timestamp_sec": 4.0, "visual_prompt": "character recovery breathing", "mood_tone": "DRAMATIC"}
            ]

        return vfx_context

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

    def _save_to_workspace(self, data, filename="38_bloom_glare_compositor.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Compositor glare setup saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save glare settings: {str(e)}")
            return None

    def orchestrate_bloom_glare_compositing(self):
        context = self._load_upstream_data()
        print(f"[{self.agent_name}] Bloom & Glare Engine initialized. Querying aesthetic post-processing rules...")

        system_prompt = (
            "You are an expert Compositing TD specialized in high-end anime post-processing, bloom filters, and anamorphic flares.\n"
            "Your job is to analyze the emotional tone and visual prompt of a shot and output precise composition nodes parameters for Blender's Compositor.\n"
            "For each shot entry, generate exactly 1 configuration in a list named 'bloom_glare_profiles' with these keys:\n"
            "- 'timestamp_sec': float matching the video timeline.\n"
            "- 'glare_type': string (choose from: 'fog_glow' for misty/magical scenes, 'streaks' for sharp sword slashes/light beams, 'ghosts' for heavy energetic blast reflections, 'simple_star' for retro magic points).\n"
            "- 'glare_threshold': float (brightness limit to trigger glow; range 0.1 for high sensitivity/lots of glow, to 2.0 for only super-bright areas glowing).\n"
            "- 'bloom_blend_factor': float (how much the glow merges with the original image; range -1.0 to 1.0, where 0.0 is equal mix, 0.8 is heavily glowing screen).\n"
            "- 'streak_count': integer (if glare_type is streaks/stars, number of light spikes; choose from 2, 4, 6, or 8).\n"
            "- 'glare_fade_factor': float (softness/decay of the glow streaks; range 0.4 to 0.95).\n"
            "- 'color_modulation_shift': array of 3 floats representing [R, G, B] tint scale for the glow (e.g., [1.0, 0.9, 0.8] for golden retro mood).\n"
            "Format your output STRICTLY as a raw JSON object containing only the list key 'bloom_glare_profiles'. "
            "Do not write conversational introductions, markdown code blocks, or backticks. Return valid JSON only."
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
                    {"role": "user", "content": f"Visual Mood Logs:\n{json.dumps(context, indent=2)}"}
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
                    {"role": "user", "content": f"Visual Mood Logs:\n{json.dumps(context, indent=2)}"}
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
                    "bloom_glare_profiles": structured_output.get("bloom_glare_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Initializing procedural lighting engine.")
            return self._execute_procedural_fallback(context)

    def _execute_procedural_fallback(self, context):
        # Precise algorithmic fallback translating scenes directly to stylized optical flares
        profiles = []
        for ctx in context:
            ts = float(ctx.get("timestamp_sec", 0.0))
            mood = str(ctx.get("mood_tone", "")).upper()
            prompt = str(ctx.get("visual_prompt", "")).lower()

            if "climax" in mood or "blast" in prompt or "hype" in mood:
                # Extreme energy clash triggers intense camera lens streaks
                gtype = "streaks"
                threshold = 0.25 # Highly sensitive to light emitting pixels
                blend = 0.75 # Heavy blast overexposure
                streaks = 4 # Anamorphic sci-fi laser feel
                fade = 0.85
                color = [0.2, 0.5, 1.0] # Cosmic blue glare tint
            elif "dramatic" in mood or "recovery" in prompt or "sad" in mood:
                # Cinematic warm bloom
                gtype = "fog_glow"
                threshold = 0.6
                blend = 0.4
                streaks = 4
                fade = 0.90
                color = [1.0, 0.85, 0.75] # Dreamy golden highlight tint
            else:
                # Normal scene setup
                gtype = "fog_glow"
                threshold = 1.0
                blend = 0.1
                streaks = 4
                fade = 0.75
                color = [1.0, 1.0, 1.0]

            profiles.append({
                "timestamp_sec": ts,
                "glare_type": gtype,
                "glare_threshold": threshold,
                "bloom_blend_factor": blend,
                "streak_count": streaks,
                "glare_fade_factor": fade,
                "color_modulation_shift": color
            })

        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Glare Fallback)",
            "bloom_glare_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    compositor = AiVFXBloomGlareEngine()
    output = compositor.orchestrate_bloom_glare_compositing()
    
    print("\n--- Z-NET COMPOSITING DEPT: AGENT 38 BLOOM & GLARE COMPLETE ---")
    print(f"Active optical bloom profiles designed: {len(output['bloom_glare_profiles'])}")
    for p in output["bloom_glare_profiles"]:
        print(f"Time: {p['timestamp_sec']}s | Filter: '{p['glare_type']}' | Sensitivity: {p['glare_threshold']}")
        print(f"  Blend Weight: {p['bloom_blend_factor']} | Streaks: {p['streak_count']} spikes | Color Shift: {p['color_modulation_shift']}")
    print("----------------------------------------------------------------")
