import os
import sys
import json

class OmniMatrixSrtSubtitleCompiler:
    def __init__(self, workspace_dir="znet_workspace", export_dir="znet_exports/subtitles"):
        self.agent_name = "Agent 13: srt_subtitle_compiler"
        self.workspace_dir = workspace_dir
        self.export_dir = export_dir
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        """Loads the central OmniMatrix state."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Upstream modules must run first.", "ERROR")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        """Updates the central OmniMatrix state with subtitle paths."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("OmniMatrix state successfully updated with subtitle metadata.")

    def _write_srt_file(self, blocks, file_path):
        """
        Writes standard SubRip Text (.srt) format.
        Format: Index -> Start Time --> End Time -> Text
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for idx, block in enumerate(blocks):
                    f.write(f"{idx + 1}\n")
                    f.write(f"{block['start']} --> {block['end']}\n")
                    f.write(f"{block['text']}\n\n")
            self.log(f"Subtitles written successfully to '{file_path}'")
            return True
        except Exception as e:
            self.log(f"Failed to write SRT file: {str(e)}", "ERROR")
            return False

    def execute_compilation(self):
        state = self._load_matrix_state()
        
        # Verify Pipeline Sequence
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent and target_agent != "Agent_13":
            self.log(f"Pipeline sequence mismatch. Expected {target_agent}, but running {self.agent_name}. Proceeding anyway for testing.", "WARNING")

        audio_module = state.get("module_b_audio", {})
        audio_timeline = audio_module.get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("Audio timeline is empty. Cannot compile subtitles.", "ERROR")
            return

        self.log("Compiling Standard and Rapid-Fire SRT subtitles from precision timestamps...")

        standard_blocks = []
        rapid_fire_blocks = []

        for frame in audio_timeline:
            timing_data = frame.get("global_timing", {})
            f_start = timing_data.get("srt_frame_start", "00:00:00,000")
            f_end = timing_data.get("srt_frame_end", "00:00:01,000")
            full_voiceover = frame.get("spoken_voiceover", "").strip()

            # Compile Standard Subtitles (Full sentence per frame)
            if full_voiceover:
                standard_blocks.append({
                    "start": f_start,
                    "end": f_end,
                    "text": full_voiceover
                })

            # Compile Rapid-Fire Subtitles (Word by Word for Shorts/Reels style)
            words = frame.get("words_alignment", [])
            for word_item in words:
                word_text = word_item.get("word", "").strip()
                uppercase_word = word_text.upper()
                
                if uppercase_word:
                    rapid_fire_blocks.append({
                        "start": word_item.get("srt_start", f_start),
                        "end": word_item.get("srt_end", f_end),
                        "text": uppercase_word
                    })

        standard_path = os.path.join(self.export_dir, "standard_subtitles.srt")
        rapid_path = os.path.join(self.export_dir, "rapid_fire_subtitles.srt")

        self._write_srt_file(standard_blocks, standard_path)
        self._write_srt_file(rapid_fire_blocks, rapid_path)

        # Update OmniMatrix State with physical paths for FFmpeg to use later
        state["module_b_audio"]["subtitle_assets"] = {
            "standard_srt_path": standard_path,
            "rapid_fire_srt_path": rapid_path,
            "total_standard_segments": len(standard_blocks),
            "total_rapid_fire_words": len(rapid_fire_blocks)
        }
        
        # OmniMatrix Pipeline Handshake
        state["pipeline_status"]["last_active_agent"] = "Agent_13"
        state["pipeline_status"]["next_agent"] = "Ai_Agent_14"
        
        self._save_matrix_state(state)
        self.log("Module B - Subtitle Compilation Complete. Handoff to Ai Agent 14.")

if __name__ == "__main__":
    compiler = OmniMatrixSrtSubtitleCompiler()
    compiler.execute_compilation()
    print("\n--- OMNIMATRIX MODULE B: AGENT 13 COMPLETE ---")
