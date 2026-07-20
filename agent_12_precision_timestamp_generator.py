import os
import sys
import json

class OmniMatrixPrecisionTimestampGenerator:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 12: precision_timestamp_generator"
        self.workspace_dir = workspace_dir
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        """Loads the central OmniMatrix state file."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run upstream modules first.", "ERROR")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        """Saves the synchronized global timeline back to the state file."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("OmniMatrix state successfully updated with global precision timestamps.")

    def _format_time_srt(self, seconds_val):
        """
        Converts raw seconds float into standard subtitle/video editing format (HH:MM:SS,mmm).
        Essential for CapCut, Premiere Pro, and FFmpeg subtitle overlays.
        """
        hours = int(seconds_val // 3600)
        minutes = int((seconds_val % 3600) // 60)
        seconds = int(seconds_val % 60)
        milliseconds = int(round((seconds_val % 1) * 1000))
        
        # Normalize time if milliseconds round up to 1000
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

    def build_precision_timeline(self):
        state = self._load_matrix_state()
        
        audio_module = state.get("module_b_audio", {})
        if not audio_module.get("words_aligned", False):
            self.log("Word alignment data is missing. Please run Agent 11 first.", "ERROR")
            return

        audio_timeline = audio_module.get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("Audio timeline is empty.", "ERROR")
            return

        self.log(f"Synchronizing absolute global timeline for {len(audio_timeline)} frames...")

        global_cumulative_offset = 0.0

        for frame in audio_timeline:
            f_idx = frame.get("frame_index", 0)
            
            # Fetch local word alignments from Agent 11
            words_align = frame.get("words_alignment", [])
            
            # Recalculate accurate frame duration based on the last word's end time
            # This is safer than relying on estimated MP3 durations
            if words_align:
                frame_duration = words_align[-1].get("end_time", 0.0)
            else:
                frame_duration = float(frame.get("audio_duration_seconds", 0.0))

            global_start = global_cumulative_offset
            global_end = global_cumulative_offset + frame_duration

            # Inject global frame boundaries
            frame["global_timing"] = {
                "frame_start_sec": round(global_start, 3),
                "frame_end_sec": round(global_end, 3),
                "srt_frame_start": self._format_time_srt(global_start),
                "srt_frame_end": self._format_time_srt(global_end)
            }

            # Map local word timings directly onto the global absolute timeline
            for word_meta in words_align:
                local_w_start = float(word_meta.get("start_time", 0.0))
                local_w_end = float(word_meta.get("end_time", 0.0))

                glob_w_start = global_start + local_w_start
                glob_w_end = global_start + local_w_end

                word_meta["global_start_sec"] = round(glob_w_start, 3)
                word_meta["global_end_sec"] = round(glob_w_end, 3)
                word_meta["srt_start"] = self._format_time_srt(glob_w_start)
                word_meta["srt_end"] = self._format_time_srt(glob_w_end)

            # Advance the global clock for the next frame
            global_cumulative_offset = global_end
            self.log(f"Frame {f_idx} mapped: {self._format_time_srt(global_start)} --> {self._format_time_srt(global_end)}")

        # Update Master Metrics
        master_metrics = {
            "total_video_duration_sec": round(global_cumulative_offset, 3),
            "total_video_duration_srt": self._format_time_srt(global_cumulative_offset),
            "timestamps_generated": True
        }
        
        state["module_b_audio"]["master_timeline_metrics"] = master_metrics
        state["module_b_audio"]["audio_timeline"] = audio_timeline
        
        # Pipeline update
        state["pipeline_status"]["last_active_agent"] = "Agent_12"
        state["pipeline_status"]["next_agent"] = "Agent_13"
        
        self._save_matrix_state(state)
        
        self.log(f"Timeline limits synchronized: 0.000s -> {round(global_cumulative_offset, 3)}s")
        self.log("Module B Audio timeline processing complete. Ready for handoff.")

if __name__ == "__main__":
    generator = OmniMatrixPrecisionTimestampGenerator()
    generator.build_precision_timeline()
    print("\n--- OMNIMATRIX MODULE B: AGENT 12 COMPLETE ---")
