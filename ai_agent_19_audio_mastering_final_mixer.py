import os
import re
import sys
import json
import urllib.request
import urllib.error

class AudioMasteringFinalMixer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 19: audio_mastering_final_mixer"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_all_upstream_audio_modules(self):
        # Saare pichle audio agents ke state files ko compile karta hai final master ke liye
        stages = {
            "sidechain": "16_sidechain_compression_blueprint.json",
            "sfx": "17_sfx_alchemist_synthesizer_blueprint.json",
            "bgm_vibe": "18_bgm_vibe_matcher_blueprint.json"
        }
        
        compiled_audio_blueprint = {
            "has_sidechain": False,
            "has_sfx": False,
            "has_bgm_automation": False,
            "meta": {}
        }

        # 1. Load Sidechain Blueprint
        sc_path = os.path.join(self.workspace_dir, stages["sidechain"])
        if os.path.exists(sc_path):
            try:
                with open(sc_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                compiled_audio_blueprint["sidechain_triggers"] = data.get("compression_triggers", [])
                compiled_audio_blueprint["has_sidechain"] = True
            except Exception:
                pass

        # 2. Load SFX Synthesizer Blueprint
        sfx_path = os.path.join(self.workspace_dir, stages["sfx"])
        if os.path.exists(sfx_path):
            try:
                with open(sfx_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                compiled_audio_blueprint["synthesized_sfx"] = data.get("synthesized_sfx_parameters", [])
                compiled_audio_blueprint["has_sfx"] = True
            except Exception:
                pass

        # 3. Load BGM Vibe Automation
        bgm_path = os.path.join(self.workspace_dir, stages["bgm_vibe"])
        if os.path.exists(bgm_path):
            try:
                with open(bgm_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                compiled_audio_blueprint["bgm_segments"] = data.get("bgm_automation_segments", [])
                compiled_audio_blueprint["has_bgm_automation"] = True
            except Exception:
                pass

        return compiled_audio_blueprint

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

    def _save_to_workspace(self, data, filename="19_final_mastered_audio_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Final audio mastering blueprint saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save mastering state: {str(e)}")
            return None

    def design_final_mix_master(self):
        compiled_data = self._load_all_upstream_audio_modules()
        print(f"[{self.agent_name}] Mastering Console active. Calculating global loudness and EQ cuts...")

        system_prompt = (
            "You are a legendary audio mastering engineer specialized in optimizing phonk/bass-heavy tracks for phone speakers and headphones.\n"
            "Your job is to analyze all compiled audio parameters and output final mastering/mixing console settings "
            "to achieve maximum loudness without digital clipping (limiting at -0.1 dB or -1.0 dB True Peak).\n"
            "Output exactly 1 mastering blueprint inside a JSON structure with these keys:\n"
            "- 'target_loudness_lufs': float representing target loudness (choose between -10.0 and -6.0 LUFS for competitive mobile short platform standards).\n"
            "- 'master_true_peak_limiter_db': float (choose between -1.0 and -0.1 dB to prevent platform conversion distortion).\n"
            "- 'stereo_widening_factor': float (scale from 1.0 to 1.8; higher means wider background elements, keeping vocals dead-center).\n"
            "- 'low_cut_filter_hz': integer representing low-end rumble cleanup (choose between 20 and 35 Hz to clean sub mud).\n"
            "- 'vocal_presence_boost_db': float representing boost in high-mids (1.5kHz to 3kHz, choose between +1.0 and +3.0 dB).\n"
            "- 'glue_compressor_settings': object containing 'threshold_db' (float, -2.0 to -6.0), 'ratio' (string, '1.5:1' or '2:1'), and 'makeup_gain_db' (float).\n"
            "Format your output STRICTLY as a raw JSON object containing these master settings. "
            "No conversational talk, no markdown backticks, no code block formats. Output only valid JSON."
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
                    {"role": "user", "content": f"Compiled Audio Signal Map:\n{json.dumps(compiled_data, indent=2)}"}
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
                    {"role": "user", "content": f"Compiled Audio Signal Map:\n{json.dumps(compiled_data, indent=2)}"}
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
                    "compiled_signals_summary": {
                        "sidechain_active": compiled_data["has_sidechain"],
                        "sfx_active": compiled_data["has_sfx"],
                        "bgm_active": compiled_data["has_bgm_automation"]
                    },
                    "mastering_parameters": structured_output
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Network Exception: {str(e)}. Running procedural mastering console.")
            return self._execute_procedural_fallback(compiled_data)

    def _execute_procedural_fallback(self, compiled_data):
        # Generates industry standard mastering limits mathematically
        fallback_output = {
            "agent_executed": f"{self.agent_name} (Procedural Master Fallback)",
            "compiled_signals_summary": {
                "sidechain_active": compiled_data["has_sidechain"],
                "sfx_active": compiled_data["has_sfx"],
                "bgm_active": compiled_data["has_bgm_automation"]
            },
            "mastering_parameters": {
                "target_loudness_lufs": -8.0,
                "master_true_peak_limiter_db": -0.5,
                "stereo_widening_factor": 1.4,
                "low_cut_filter_hz": 30,
                "vocal_presence_boost_db": 1.5,
                "glue_compressor_settings": {
                    "threshold_db": -4.0,
                    "ratio": "2:1",
                    "makeup_gain_db": 2.5
                }
            }
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    mixer = AudioMasteringFinalMixer()
    output = mixer.design_final_mix_master()
    
    print("\n--- Z-NET AUDIO ENGINE: AGENT 19 MASTER COMPLETED ---")
    print(f"Compilation Scan - Sidechain: {output['compiled_signals_summary']['sidechain_active']} | SFX: {output['compiled_signals_summary']['sfx_active']} | BGM: {output['compiled_signals_summary']['bgm_active']}")
    mp = output["mastering_parameters"]
    print(f"Output Standard: {mp['target_loudness_lufs']} LUFS | Ceiling: {mp['master_true_peak_limiter_db']}dB True Peak")
    print(f"Glue EQ: High-mid vocal boost of +{mp['vocal_presence_boost_db']}dB | Low cut applied at {mp['low_cut_filter_hz']}Hz")
    print("------------------------------------------------------")
