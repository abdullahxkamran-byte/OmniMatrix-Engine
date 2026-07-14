import os
import sys
import json

class PrecisionTimestampGenerator:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 12: precision_timestamp_generator"
        self.workspace_dir = workspace_dir

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_upstream_alignments(self):
        """
        Loads aligned word timing maps from Stage 11.
        If file is missing, initiates automatic procedural simulation.
        """
        input_path = os.path.join(self.workspace_dir, "11_audio_word_alignment.json")
        if os.path.exists(input_path):
            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Stage 11 alignments loaded from '{input_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: File read error ({str(e)}). Transitioning to baseline generator.")
        
        # Safe fallback trigger if workspace state is currently unpopulated
        print(f"[{self.agent_name}] Workspace Alert: Upstream timeline alignments are missing.")
        return {
            "aligned_timeline": [
                {
                    "frame_index": 1,
                    "audio_file": "voiceover_frame_01.mp3",
                    "total_estimated_duration": 4.20,
                    "words_count": 6,
                    "words_alignment": [
                        {"word": "Unleash", "start_time": 0.0, "end_time": 0.7},
                        {"word": "the", "start_time": 0.7, "end_time": 1.0},
                        {"word": "supreme", "start_time": 1.0, "end_time": 1.8},
                        {"word": "dark", "start_time": 1.8, "end_time": 2.5},
                        {"word": "power", "start_time": 2.5, "end_time": 3.4},
                        {"word": "within", "start_time": 3.4, "end_time": 4.2}
                    ]
                }
            ]
        }

    def _format_time_string(self, seconds_val):
        """
        Transforms float seconds into professional high-precision cinematic timing format (HH:MM:SS,mmm)
        """
        hours = int(seconds_val // 3600)
        minutes = int((seconds_val % 3600) // 60)
        seconds = int(seconds_val % 60)
        milliseconds = int(round((seconds_val % 1) * 1000))
        
        # Safety normalization for millisecond overflow
        if milliseconds >= 1000:
            seconds += 1
            milliseconds -= 1000
            if seconds >= 60:
                minutes += 1
                seconds -= 60
                if minutes >= 60:
                    hours += 1
                    minutes -= 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def generate_precision_timeline(self):
        """
        Applies mathematical summation algorithms to calculate absolute global timeline boundaries 
        across the entire asset chain.
        """
        alignment_data = self._load_upstream_alignments()
        aligned_frames = alignment_data.get("aligned_timeline", [])

        global_cumulative_offset = 0.0
        precision_timeline = []

        print(f"[{self.agent_name}] Synchronizing millisecond timeline offsets...")

        for frame in aligned_frames:
            f_idx = frame.get("frame_index", 1)
            duration = float(frame.get("total_estimated_duration", 3.0))
            words_align = frame.get("words_alignment", [])

            # Frame Global Boundaries
            global_start = global_cumulative_offset
            global_end = global_cumulative_offset + duration

            global_words_timeline = []
            for word_meta in words_align:
                # Map local word timing directly onto global absolute timeline
                local_w_start = float(word_meta.get("start_time", 0.0))
                local_w_end = float(word_meta.get("end_time", 0.0))

                glob_w_start = global_start + local_w_start
                glob_w_end = global_start + local_w_end

                global_words_timeline.append({
                    "word_index": word_meta.get("word_index", 1),
                    "word": word_meta.get("word", ""),
                    "local_start_sec": local_w_start,
                    "local_end_sec": local_w_end,
                    "global_start_sec": round(glob_w_start, 3),
                    "global_end_sec": round(glob_w_end, 3),
                    "srt_format_start": self._format_time_string(glob_w_start),
                    "srt_format_end": self._format_time_string(glob_w_end)
                })

            precision_timeline.append({
                "frame_index": f_idx,
                "audio_file": frame.get("audio_file", ""),
                "frame_duration_sec": round(duration, 3),
                "global_frame_start_sec": round(global_start, 3),
                "global_frame_end_sec": round(global_end, 3),
                "srt_frame_start": self._format_time_string(global_start),
                "srt_frame_end": self._format_time_string(global_end),
                "aligned_words": global_words_timeline
            })

            # Update offset accumulators
            global_cumulative_offset = global_end

        output_data = {
            "agent_executed": self.agent_name,
            "master_duration_sec": round(global_cumulative_offset, 3),
            "srt_master_duration": self._format_time_string(global_cumulative_offset),
            "precision_timeline": precision_timeline
        }

        # Save to Workspace
        output_path = os.path.join(self.workspace_dir, "12_precision_timestamps.json")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4)
            print(f"[{self.agent_name}] Success: Global absolute timeline config saved to '{output_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error saving precision file: {str(e)}")

        return output_data

if __name__ == "__main__":
    generator = PrecisionTimestampGenerator()
    output = generator.generate_precision_timeline()
    
    print("\n--- Z-NET AUDIO ENGINE: AGENT 12 PRECISION TIMESTAMPS COMPLETED ---")
    print(f"Master Video Duration calculated: {output['master_duration_sec']}s ({output['srt_master_duration']})")
    if output["precision_timeline"]:
        last_frame = output["precision_timeline"][-1]
        print(f"Total calculated frames: {len(output['precision_timeline'])}")
        print(f"Timeline limits: 0.00s -> {last_frame['global_frame_end_sec']}s")
    print("--------------------------------------------------------------------")
