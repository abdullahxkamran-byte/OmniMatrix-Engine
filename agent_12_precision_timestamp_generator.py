import os
import sys
import json

class AiAgent12PrecisionTimestampGenerator:
    def __init__(self):
        self.agent_name = "Ai_Agent_12"
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        """Loads the central OmniMatrix state safely with strict JSON validation."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run upstream modules first.", "FATAL")
            sys.exit(1)
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.log(f"JSON Corruption detected: {e}", "FATAL")
            sys.exit(1)

    def _save_matrix_state(self, state_data):
        """Saves the synchronized global timeline back to the state file idempotently."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4, ensure_ascii=False)
        self.log("OmniMatrix state successfully updated with global precision timestamps.", "SUCCESS")

    def _format_time_srt(self, seconds_val):
        """
        Converts raw seconds float into standard subtitle/video editing format (HH:MM:SS,mmm).
        Essential for seamless import into advanced editing suites.
        """
        # Ensure time doesn't go negative
        seconds_val = max(0.0, seconds_val)
        
        hours = int(seconds_val // 3600)
        minutes = int((seconds_val % 3600) // 60)
        seconds = int(seconds_val % 60)
        milliseconds = int(round((seconds_val % 1) * 1000))
        
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
        
        # 1. Atomic Handshake Protocol
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{orchestrator.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        # 2. Extract Global Configuration for Fluidity
        global_config = state.get("global_config", {})
        # Optional padding between frames for natural transitions (default 0.0)
        frame_gap_padding = global_config.get("timeline_settings", {}).get("inter_frame_gap_sec", 0.0)
        # Enable anti-overlap micro-adjustment for NLE software compatibility
        enable_anti_overlap = global_config.get("timeline_settings", {}).get("srt_anti_overlap", True)

        audio_module = state.get("module_b_audio", {})
        if not audio_module.get("words_aligned", False):
            self.log("Word alignment data is missing. Please run Agent 11 first.", "FATAL")
            sys.exit(1)

        audio_timeline = audio_module.get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("Audio timeline is empty.", "FATAL")
            sys.exit(1)

        self.log(f"Synchronizing absolute global timeline for {len(audio_timeline)} frames...", "STATUS")

        # 3. Idempotency Sweep & Timeline Processing
        global_cumulative_offset = 0.0

        for frame in audio_timeline:
            f_idx = frame.get("frame_index", 0)
            words_align = frame.get("words_alignment", [])
            
            # Scrub previous ghost data
            if "global_timing" in frame:
                del frame["global_timing"]
                
            for word_meta in words_align:
                word_meta.pop("global_start_sec", None)
                word_meta.pop("global_end_sec", None)
                word_meta.pop("srt_start", None)
                word_meta.pop("srt_end", None)

            # Recalculate frame duration
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

            # Map local word timings onto the global absolute timeline
            for i, word_meta in enumerate(words_align):
                local_w_start = float(word_meta.get("start_time", 0.0))
                local_w_end = float(word_meta.get("end_time", 0.0))

                glob_w_start = global_start + local_w_start
                glob_w_end = global_start + local_w_end

                # Anti-Overlap Logic: Subtract 1 millisecond from end time to prevent software rendering flicker
                if enable_anti_overlap and i < len(words_align) - 1:
                    glob_w_end -= 0.001

                word_meta["global_start_sec"] = round(glob_w_start, 3)
                word_meta["global_end_sec"] = round(glob_w_end, 3)
                word_meta["srt_start"] = self._format_time_srt(glob_w_start)
                word_meta["srt_end"] = self._format_time_srt(glob_w_end)

            # Advance the global clock for the next frame, adding any requested padding
            global_cumulative_offset = global_end + frame_gap_padding
            self.log(f"Frame {f_idx} globally mapped: {self._format_time_srt(global_start)} --> {self._format_time_srt(global_end)}")

        # 4. Update Master Metrics
        master_metrics = {
            "total_video_duration_sec": round(global_cumulative_offset, 3),
            "total_video_duration_srt": self._format_time_srt(global_cumulative_offset),
            "timestamps_generated": True
        }
        
        state["module_b_audio"]["master_timeline_metrics"] = master_metrics
        state["module_b_audio"]["audio_timeline"] = audio_timeline
        
        # 5. Handshake Routing
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        state["orchestrator_matrix"]["next_agent"] = "Ai_Agent_13" # Passing to SRT Subtitle Compiler
        
        self._save_matrix_state(state)
        
        self.log(f"Timeline limits synchronized: 0.000s -> {round(global_cumulative_offset, 3)}s", "INFO")
        self.log(f"Agent {self.agent_name} complete! Handoff to Agent 13 (SRT Compiler).")

if __name__ == "__main__":
    generator = AiAgent12PrecisionTimestampGenerator()
    generator.build_precision_timeline()
