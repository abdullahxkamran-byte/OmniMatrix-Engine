import os
import sys
import json

class SrtSubtitleCompiler:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 13: srt_subtitle_compiler"
        self.workspace_dir = workspace_dir

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_precision_timestamps(self):
        """
        Loads global millisecond timestamps from Stage 12.
        Falls back to manual bypass if upstream files are missing.
        """
        input_path = os.path.join(self.workspace_dir, "12_precision_timestamps.json")
        if os.path.exists(input_path):
            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Stage 12 timestamps loaded from '{input_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: File read error ({str(e)}). Activating fallback compiler.")

        print(f"[{self.agent_name}] Workspace Alert: Upstream timing database is missing. Compiling mock data.")
        return {
            "precision_timeline": [
                {
                    "frame_index": 1,
                    "srt_frame_start": "00:00:00,000",
                    "srt_frame_end": "00:00:03,500",
                    "spoken_voiceover": "Unleash your true hidden inner power",
                    "aligned_words": [
                        {"word": "Unleash", "srt_format_start": "00:00:00,000", "srt_format_end": "00:00:00,800"},
                        {"word": "your", "srt_format_start": "00:00:00,800", "srt_format_end": "00:00:01,200"},
                        {"word": "true", "srt_format_start": "00:00:01,200", "srt_format_end": "00:00:01,800"},
                        {"word": "hidden", "srt_format_start": "00:00:01,800", "srt_format_end": "00:00:02,400"},
                        {"word": "inner", "srt_format_start": "00:00:02,400", "srt_format_end": "00:00:02,900"},
                        {"word": "power", "srt_format_start": "00:00:02,900", "srt_format_end": "00:00:03,500"}
                    ]
                }
            ]
        }

    def _write_srt_file(self, blocks, file_path):
        """
        Procedurally writes SRT blocks in strict formatting sequence:
        Index
        HH:MM:SS,mmm --> HH:MM:SS,mmm
        Subtitle text
        [empty line]
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for idx, block in enumerate(blocks):
                    f.write(f"{idx + 1}\n")
                    f.write(f"{block['start']} --> {block['end']}\n")
                    f.write(f"{block['text']}\n\n")
            print(f"[{self.agent_name}] Success: Subtitles written to '{file_path}'")
            return True
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to write file: {str(e)}")
            return False

    def compile_subtitles(self):
        """
        Orchestrates compiling both Standard and Rapid-Fire high-impact Subtitle sequences.
        """
        timing_data = self._load_precision_timestamps()
        timeline = timing_data.get("precision_timeline", [])

        standard_blocks = []
        rapid_fire_blocks = []

        print(f"[{self.agent_name}] Running Subtitle compiler engines...")

        for frame in timeline:
            f_idx = frame.get("frame_index", 1)
            f_start = frame.get("srt_frame_start", "00:00:00,000")
            f_end = frame.get("srt_frame_end", "00:00:01,000")
            full_voiceover = frame.get("spoken_voiceover", "").strip()

            # Style 1: Standard Frame Block
            if full_voiceover:
                standard_blocks.append({
                    "start": f_start,
                    "end": f_end,
                    "text": full_voiceover
                })

            # Style 2: Rapid-Fire (Word-by-Word) Block
            words = frame.get("aligned_words", [])
            for word_item in words:
                word_text = word_item.get("word", "").strip()
                # Clean word and convert to UPPERCASE for professional aggressive phonk impact!
                uppercase_word = word_text.upper() 
                
                if uppercase_word:
                    rapid_fire_blocks.append({
                        "start": word_item.get("srt_format_start", f_start),
                        "end": word_item.get("srt_format_end", f_end),
                        "text": uppercase_word
                    })

        # Save both files physically to the workspace
        standard_path = os.path.join(self.workspace_dir, "13_standard_subtitles.srt")
        rapid_path = os.path.join(self.workspace_dir, "13_rapid_fire_subtitles.srt")

        self._write_srt_file(standard_blocks, standard_path)
        self._write_srt_file(rapid_fire_blocks, rapid_path)

        output_metadata = {
            "agent_executed": self.agent_name,
            "standard_srt_path": standard_path,
            "rapid_fire_srt_path": rapid_path,
            "total_standard_segments": len(standard_blocks),
            "total_rapid_fire_words": len(rapid_fire_blocks)
        }

        # Save manifest record
        manifest_path = os.path.join(self.workspace_dir, "13_srt_compiler_output.json")
        try:
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(output_metadata, f, indent=4)
            print(f"[{self.agent_name}] Manifest registered: '{manifest_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error saving manifest record: {str(e)}")

        return output_metadata

if __name__ == "__main__":
    compiler = SrtSubtitleCompiler()
    output = compiler.compile_subtitles()
    
    print("\n--- Z-NET AUDIO ENGINE: AGENT 13 COMPLETED ---")
    print(f"Standard SRT Blocks: {output['total_standard_segments']}")
    print(f"Rapid-Fire (Shorts Style) SRT Words: {output['total_rapid_fire_words']}")
    print("All subtitles mapped with millisecond boundaries!")
    print("-----------------------------------------------")
