import os
import sys
import json

class ScriptFileFormatter:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 08: script_file_formatter"
        self.workspace_dir = workspace_dir

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_stage_data(self):
        """
        Loads clean scripts from Stage 6 (Word Guard) and aesthetic styles
        from Stage 7 (Dark Phonk Vibe). If missing, executes universal safe state.
        """
        guard_path = os.path.join(self.workspace_dir, "06_word_count_guard.json")
        phonk_path = os.path.join(self.workspace_dir, "07_dark_phonk_vibe.json")

        guard_data = {}
        phonk_data = {}

        # Attempt to load Stage 6 audited scripts
        if os.path.exists(guard_path):
            try:
                with open(guard_path, "r", encoding="utf-8") as f:
                    guard_data = json.load(f)
                print(f"[{self.agent_name}] Loaded Stage 6 data successfully.")
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Cannot read Stage 6 file: {str(e)}")

        # Attempt to load Stage 7 aesthetic data
        if os.path.exists(phonk_path):
            try:
                with open(phonk_path, "r", encoding="utf-8") as f:
                    phonk_data = json.load(f)
                print(f"[{self.agent_name}] Loaded Stage 7 data successfully.")
            except Exception as e:
                print(f"[{self.agent_name}] Warning: Cannot read Stage 7 file: {str(e)}")

        return guard_data, phonk_data

    def _generate_fallback_timeline(self):
        """
        Generates a basic structured timeline when upstream database states are missing.
        """
        print(f"[{self.agent_name}] Workspace Alert: Upstream files missing. Creating clean baseline script.")
        return [
            {
                "frame_index": 1,
                "duration_seconds": 4.0,
                "spoken_voiceover": "Unleash the supreme dark power within yourself!",
                "visual_style_prompt": "Cinematic high-contrast dark silhouette, heavy grain, neon red backlight.",
                "camera_shake_intensity": 0.8,
                "bass_drop_sync": True,
                "ambient_glitch_rate": 0.3,
                "color_palette_hex": ["#000000", "#ff0000", "#ffffff"]
            }
        ]

    def format_master_files(self):
        """
        Compiles, aligns indexes, and outputs clean production files (JSON and TXT preview).
        """
        guard_data, phonk_data = self._load_stage_data()
        
        topic = guard_data.get("source_topic", phonk_data.get("source_topic", "General Anime Target"))
        guard_frames = guard_data.get("timeline_frames", [])
        phonk_frames = phonk_data.get("phonk_frames", [])

        master_timeline = []

        # If both streams are empty, activate dynamic backup engine
        if not guard_frames and not phonk_frames:
            master_timeline = self._generate_fallback_timeline()
        else:
            # Map Phonk vibes directly to correct timestamp frames
            phonk_map = {item["frame_index"]: item for item in phonk_frames}
            
            for idx, frame in enumerate(guard_frames):
                f_idx = frame.get("frame_index", idx + 1)
                phonk_meta = phonk_map.get(f_idx, {})

                master_timeline.append({
                    "frame_index": f_idx,
                    "duration_seconds": frame.get("duration_seconds", 3.0),
                    "spoken_voiceover": frame.get("optimized_voiceover", frame.get("spoken_voiceover", "")),
                    "visual_style_prompt": phonk_meta.get("visual_style_prompt", "High-contrast dark cinematic aesthetic."),
                    "camera_shake_intensity": phonk_meta.get("camera_shake_intensity", 0.3),
                    "bass_drop_sync": phonk_meta.get("bass_drop_sync", False),
                    "ambient_glitch_rate": phonk_meta.get("ambient_glitch_rate", 0.1),
                    "color_palette_hex": phonk_meta.get("color_palette_hex", ["#000000", "#ffffff"])
                })

        # Save Final Structured JSON
        output_json = {
            "source_topic": topic,
            "agent_executed": self.agent_name,
            "total_frames": len(master_timeline),
            "master_timeline": master_timeline
        }

        json_path = os.path.join(self.workspace_dir, "08_final_master_script.json")
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(output_json, f, indent=4)
            print(f"[{self.agent_name}] Master JSON written to '{json_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing JSON: {str(e)}")

        # Save Readable TXT Preview for the Editor
        txt_path = os.path.join(self.workspace_dir, "08_final_script_preview.txt")
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"=== MASTER VIDEO SCRIPT PREVIEW ===\n")
                f.write(f"Topic: {topic}\n")
                f.write(f"Total Video Frames: {len(master_timeline)}\n")
                f.write(f"====================================\n\n")

                for frame in master_timeline:
                    f_write_block = (
                        f"Frame {frame['frame_index']} | Duration: {frame['duration_seconds']}s\n"
                        f"  [Voiceover]: \"{frame['spoken_voiceover']}\"\n"
                        f"  [VFX Style]: {frame['visual_style_prompt']}\n"
                        f"  [Colors]: {', '.join(frame['color_palette_hex'])}\n"
                        f"  [Pacing Notes]: Shake: {frame['camera_shake_intensity']}x, Glitch: {int(frame['ambient_glitch_rate']*100)}%, Bass Drop Sync: {frame['bass_drop_sync']}\n"
                        f"----------------------------------------------------------------------\n"
                    )
                    f.write(f_write_block)
            print(f"[{self.agent_name}] Text script preview saved to '{txt_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing Preview Text file: {str(e)}")

        return output_json

if __name__ == "__main__":
    formatter = ScriptFileFormatter()
    output = formatter.format_master_files()
    
    print("\n--- Z-NET CORE UTILITY: AGENT 08 SCRIPT FORMATTER COMPLETED ---")
    print(f"Timeline populated with {len(output['master_timeline'])} frames.")
    print("-----------------------------------------------------------------")
