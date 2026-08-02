import os
import sys
import json

class Agent_12_Precision_Timestamp_Generator:
    def __init__(self):
        self.agent_name = "Agent_12_Precision_Timestamp_Generator"

    def _format_time_srt(self, seconds_val: float) -> str:
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

    def _calculate_kinetic_gap(self, kinetic_framing: str) -> float:
        framing_lower = kinetic_framing.lower()
        if any(keyword in framing_lower for keyword in ["fast", "action", "combat", "rapid", "hyper"]):
            return 0.05
        elif any(keyword in framing_lower for keyword in ["slow", "dramatic", "cinematic", "sad", "tension"]):
            return 0.60
        else:
            return 0.25

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")

        if target_agent and "12" not in target_agent and target_agent != self.agent_name:
            print(f"[{self.agent_name}] Execution skipped. Target: {target_agent}", flush=True)
            return state

        workspace_dir = state.get("workspace_dir", "")
        if not workspace_dir:
            workspace_dir = state.get("state_file_path", "")
            if workspace_dir:
                workspace_dir = os.path.dirname(workspace_dir)
            else:
                raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: workspace_dir missing.")

        runtime_data = state.setdefault("runtime_data", {})
        module_audio = runtime_data.setdefault("module_b_audio", {})

        aligned_frames = module_audio.get("agent_11_word_alignment", [])
        if not aligned_frames:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: 'agent_11_word_alignment' missing. Agent 11 must run first.")

        if "agent_12_global_timestamps" in module_audio:
            del module_audio["agent_12_global_timestamps"]
            print(f"[{self.agent_name}] Idempotency sweep executed. Legacy timestamps purged.", flush=True)

        global_config = state.get("global_config", {})
        kinetic_framing = global_config.get("kinetic_framing", "Normal")
        inter_frame_gap = self._calculate_kinetic_gap(kinetic_framing)

        print(f"[{self.agent_name}] Base Kinetic Framing detected: '{kinetic_framing}'. Inter-frame gap set to {inter_frame_gap}s.", flush=True)

        global_cumulative_offset = 0.0
        global_timeline = []
        ffmpeg_concat_lines = []

        print(f"[{self.agent_name}] Mapping absolute global timeline for {len(aligned_frames)} frames...", flush=True)

        for frame in aligned_frames:
            idx = frame.get("frame_index", 1)
            char = frame.get("character_voice", "Narrator")
            file_path = frame.get("audio_file_path", "")
            duration = float(frame.get("total_duration_seconds", 0.0))
            words = frame.get("word_alignments", [])

            global_start = global_cumulative_offset
            global_end = global_cumulative_offset + duration

            ffmpeg_concat_lines.append(f"file '{file_path}'")
            ffmpeg_concat_lines.append(f"outpoint {duration}")
            
            if inter_frame_gap > 0.0:
                ffmpeg_concat_lines.append(f"file 'anullsrc=r=44100:cl=stereo'")
                ffmpeg_concat_lines.append(f"outpoint {inter_frame_gap}")

            global_words = []
            for w_meta in words:
                local_start = float(w_meta.get("start_time", 0.0))
                local_end = float(w_meta.get("end_time", 0.0))

                glob_w_start = global_start + local_start
                glob_w_end = global_start + local_end

                global_words.append({
                    "word_index": w_meta.get("word_index", 0),
                    "word_raw": w_meta.get("word_raw", ""),
                    "word_clean": w_meta.get("word_clean", ""),
                    "is_tag": w_meta.get("is_tag", False),
                    "local_start_sec": local_start,
                    "local_end_sec": local_end,
                    "global_start_sec": round(glob_w_start, 3),
                    "global_end_sec": round(glob_w_end, 3),
                    "srt_start": self._format_time_srt(glob_w_start),
                    "srt_end": self._format_time_srt(glob_w_end)
                })

            global_timeline.append({
                "frame_index": idx,
                "character_voice": char,
                "audio_file_path": file_path,
                "global_frame_start_sec": round(global_start, 3),
                "global_frame_end_sec": round(global_end, 3),
                "srt_frame_start": self._format_time_srt(global_start),
                "srt_frame_end": self._format_time_srt(global_end),
                "words_global_alignment": global_words
            })

            global_cumulative_offset = global_end + inter_frame_gap

        module_audio["agent_12_global_timestamps"] = global_timeline
        module_audio["agent_12_ffmpeg_concat_string"] = "\n".join(ffmpeg_concat_lines)

        pipeline_status = state.setdefault("pipeline_status", {})
        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Global precision timeline locked! Total Video Audio Length: {self._format_time_srt(global_cumulative_offset)}", flush=True)
        return state
