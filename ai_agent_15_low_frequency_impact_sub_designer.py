import os
import re
import sys
import json
import urllib.request
import urllib.error

class LowFrequencyImpactSubDesigner:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 15: low_frequency_impact_sub_designer"
        self.workspace_dir = workspace_dir
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_previous_stage(self):
        """
        Loads the beat sync events database from Stage 14.
        If missing, prompts the user to input dynamic target parameters manually.
        """
        input_path = os.path.join(self.workspace_dir, "14_phonk_beat_drop_map.json")
        if os.path.exists(input_path):
            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Stage 14 beat sync map loaded from '{input_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: File read error ({str(e)}). Switching to manual timeline.")

        print(f"[{self.agent_name}] Workspace Alert: Upstream beat drop map is missing.")
        user_input = input("Enter a dynamic target BPM to calculate sub-bass sweeps: ").strip()
        bpm_val = 130
        if user_input:
            try:
                bpm_val = int(user_input)
            except ValueError:
                pass

        return {
            "target_bpm": bpm_val,
            "beat_sync_events": [
                {
                    "timestamp_sec": 0.0,
                    "event_type": "bass-drop-flash",
                    "impact_intensity": 0.95,
                    "editor_action_note": "Initial impact spot."
                }
            ]
        }

    def _clean_json_response(self, raw_text):
        """
        Strips backticks, code wrappers, and LLM text to isolate raw JSON objects.
        """
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
            
        return cleaned

    def _save_to_workspace(self, data, filename="15_low_frequency_sub_design.json"):
        """
        Saves calculated sub-bass synthesis configurations physically to workspace.
        """
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Sub-bass synthesizer config written to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save state files: {str(e)}")
            return None

    def design_sub_impacts(self):
        """
        Processes rhythmic timeline data to construct precise DSP sub-bass synthesis blueprints.
        """
        input_data = self._load_previous_stage()
        bpm = input_data.get("target_bpm", 130)
        events = input_data.get("beat_sync_events", [])

        # Filter heavy events (bass drops) that require structural low-end physical energy
        target_triggers = [ev for ev in events if ev.get("event_type") in ["bass-drop-flash", "sub-bass-zoom"]]
        if not target_triggers and events:
            # If no major drops are labeled, target the highest intensity events
            sorted_events = sorted(events, key=lambda x: x.get("impact_intensity", 0.0), reverse=True)
            target_triggers = sorted_events[:2]

        print(f"[{self.agent_name}] Synthesis Engine active. Designing sub-bass drops matching rhythm BPM: {bpm}")

        system_prompt = (
            "You are an expert low-frequency sound synthesizer and audio DSP engineer. "
            "Your job is to analyze video beat events and design precise low-frequency sub-bass impacts (sweeps and booms) "
            "to create a bone-shattering bass-drop effect.\n"
            "For each trigger event, output exactly 1 sub-bass synthesis profile inside a list named 'sub_profiles' with these parameters:\n"
            "- 'timestamp_sec': float matching the trigger event timestamp.\n"
            "- 'start_frequency_hz': integer representing the initial frequency of the pitch sweep (choose between 60 and 90 Hz).\n"
            "- 'end_frequency_hz': integer representing the ending frequency of the sweep (choose between 24 and 35 Hz for sub-bass rumble).\n"
            "- 'sweep_duration_seconds': float representing decay length (choose between 0.8 and 2.2 seconds).\n"
            "- 'waveform_type': string designating synthesis model (choose only from: 'pure-sine', 'saturated-triangle', 'glitch-square').\n"
            "- 'target_gain_db': float value representing signal level (scale from -6.0 to 0.0 dB based on impact intensity).\n"
            "- 'rumble_reverb_decay': float representing room resonance length (scale from 0.0 to 0.50 seconds).\n"
            "Format your output STRICTLY as a raw JSON object containing the list key 'sub_profiles'. "
            "Do not include conversational introductions, code block formatting tags, or warnings. Output only valid JSON."
        )

        user_prompt = (
            f"Target Track Tempo: {bpm} BPM\n"
            f"Active Impact Points:\n{json.dumps(target_triggers, indent=2)}"
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
                    "target_bpm": bpm,
                    "agent_executed": self.agent_name,
                    "sub_profiles": structured_output.get("sub_profiles", [])
                }
                
                self._save_to_workspace(final_output)
                return final_output

        except Exception as e:
            print(f"[{self.agent_name}] Connectivity/Parsing Exception: {str(e)}. Triggering procedural synthesizer fallback.")
            return self._execute_procedural_fallback(bpm, target_triggers)

    def _execute_procedural_fallback(self, bpm, target_triggers):
        """
        Calculates mathematical low-frequency DSP synthesizer variables 
        procedurally without external LLM dependencies.
        """
        profiles = []
        for trig in target_triggers:
            ts = float(trig.get("timestamp_sec", 0.0))
            intensity = float(trig.get("impact_intensity", 0.8))

            # Sub-bass mapping math based on intensity
            start_freq = int(60 + (intensity * 25))    # 60Hz to 85Hz
            end_freq = int(24 + ((1.0 - intensity) * 8)) # 24Hz to 32Hz
            decay = round(0.8 + (intensity * 1.2), 2)    # 0.8s to 2.0s duration
            gain = round(-6.0 + (intensity * 6.0), 1)    # -6.0dB to 0.0dB peak
            
            # Sub-bass shape assignment
            if intensity > 0.85:
                waveform = "saturated-triangle" # Extra harmonics to cut through mobile phone speakers
                reverb = 0.40
            else:
                waveform = "pure-sine" # Clean sub rumble
                reverb = 0.20

            profiles.append({
                "timestamp_sec": ts,
                "start_frequency_hz": start_freq,
                "end_frequency_hz": end_freq,
                "sweep_duration_seconds": decay,
                "waveform_type": waveform,
                "target_gain_db": gain,
                "rumble_reverb_decay": reverb
            })

        fallback_output = {
            "target_bpm": bpm,
            "agent_executed": f"{self.agent_name} (Procedural Synthesis Mode)",
            "sub_profiles": profiles
        }
        self._save_to_workspace(fallback_output)
        return fallback_output

if __name__ == "__main__":
    designer = LowFrequencyImpactSubDesigner()
    output = designer.design_sub_impacts()
    
    print("\n--- Z-NET AUDIO ENGINE: AGENT 15 SUB-BASS BLUEPRINT COMPLETED ---")
    print(f"Track tempo synced at: {output['target_bpm']} BPM")
    print(f"Calculated Sub-Bass sweeps synthesized: {len(output['sub_profiles'])}")
    if output["sub_profiles"]:
        sample = output["sub_profiles"][0]
        print(f"Sample Sweep Point: {sample['timestamp_sec']}s | {sample['start_frequency_hz']}Hz -> {sample['end_frequency_hz']}Hz in {sample['sweep_duration_seconds']}s ({sample['waveform_type']})")
    print("------------------------------------------------------------------")
