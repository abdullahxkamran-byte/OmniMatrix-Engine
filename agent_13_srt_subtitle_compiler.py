import os
import sys
import json

class Agent_13_SRT_Subtitle_Compiler:
    def __init__(self):
        self.agent_name = "Agent_13_SRT_Subtitle_Compiler"

    def _format_time_ass(self, seconds_val: float) -> str:
        seconds_val = max(0.0, seconds_val)
        hours = int(seconds_val // 3600)
        minutes = int((seconds_val % 3600) // 60)
        seconds = int(seconds_val % 60)
        centiseconds = int(round((seconds_val % 1) * 100))
        if centiseconds >= 100:
            seconds += 1
            centiseconds -= 100
            if seconds >= 60:
                minutes += 1
                seconds -= 60
                if minutes >= 60:
                    hours += 1
                    minutes -= 60
        return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

    def _chunk_words(self, words_list: list, max_words=6) -> list:
        chunks = []
        current_chunk = []
        for word in words_list:
            current_chunk.append(word)
            raw_text = word.get("word_raw", "")
            if len(current_chunk) >= max_words or raw_text.endswith((".", "?", "!", ",")):
                chunks.append(current_chunk)
                current_chunk = []
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")

        if target_agent and "13" not in target_agent and target_agent != self.agent_name:
            print(f"[{self.agent_name}] Execution skipped. Target: {target_agent}", flush=True)
            return state

        workspace_dir = state.get("workspace_dir", "")
        if not workspace_dir:
            workspace_dir = state.get("state_file_path", "")
            if workspace_dir:
                workspace_dir = os.path.dirname(workspace_dir)
            else:
                raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: workspace_dir missing.")

        export_dir = os.path.join(workspace_dir, "exports", "subtitles")
        os.makedirs(export_dir, exist_ok=True)

        for existing_file in os.listdir(export_dir):
            file_path = os.path.join(export_dir, existing_file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"[{self.agent_name}] Idempotency sweep executed. Legacy subtitles purged.", flush=True)

        runtime_data = state.setdefault("runtime_data", {})
        module_audio = runtime_data.get("module_b_audio", {})
        
        global_timeline = module_audio.get("agent_12_global_timestamps", [])
        if not global_timeline:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: 'agent_12_global_timestamps' missing.")

        global_config = state.get("global_config", {})
        medium = global_config.get("medium", "Default")
        karaoke_color = "&H0000FFFF"

        long_form_blocks = []
        rapid_fire_blocks = []
        ass_dialogue_lines = []

        lf_idx = 1
        rf_idx = 1

        print(f"[{self.agent_name}] Compiling SRT & ASS subtitles for {len(global_timeline)} synchronized frames...", flush=True)

        for frame in global_timeline:
            f_srt_start = frame.get("srt_frame_start", "00:00:00,000")
            f_srt_end = frame.get("srt_frame_end", "00:00:01,000")
            
            words_align = frame.get("words_global_alignment", [])
            spoken_words = [w for w in words_align if not w.get("is_tag", False)]

            if not spoken_words:
                continue

            chunked_words = self._chunk_words(spoken_words, max_words=6)
            for chunk in chunked_words:
                if not chunk:
                    continue
                c_start = chunk[0].get("srt_start", f_srt_start)
                c_end = chunk[-1].get("srt_end", f_srt_end)
                c_text = " ".join([w.get("word_clean", "") for w in chunk]).strip()
                
                long_form_blocks.append(f"{lf_idx}\n{c_start} --> {c_end}\n{c_text}\n\n")
                lf_idx += 1

            for word_item in spoken_words:
                w_start = word_item.get("srt_start", f_srt_start)
                w_end = word_item.get("srt_end", f_srt_end)
                w_text = word_item.get("word_clean", "").strip().upper()
                
                if w_text:
                    rapid_fire_blocks.append(f"{rf_idx}\n{w_start} --> {w_end}\n{w_text}\n\n")
                    rf_idx += 1

            ass_start = self._format_time_ass(frame.get("global_frame_start_sec", 0.0))
            ass_end = self._format_time_ass(frame.get("global_frame_end_sec", 1.0))
            
            karaoke_text = ""
            for w in spoken_words:
                duration_sec = w.get("global_end_sec", 0.0) - w.get("global_start_sec", 0.0)
                centiseconds = int(max(1.0, round(duration_sec * 100)))
                clean_word = w.get("word_clean", "").strip().upper()
                karaoke_text += f"{{\\k{centiseconds}}}{clean_word} "
            
            if karaoke_text.strip():
                ass_dialogue_lines.append(f"Dialogue: 0,{ass_start},{ass_end},Default,,0,0,0,,{karaoke_text.strip()}\n")

        long_form_path = os.path.join(export_dir, "long_form_cinematic.srt")
        short_form_path = os.path.join(export_dir, "short_form_rapid.srt")
        karaoke_ass_path = os.path.join(export_dir, "karaoke_dynamic.ass")

        with open(long_form_path, "w", encoding="utf-8") as f:
            f.writelines(long_form_blocks)

        with open(short_form_path, "w", encoding="utf-8") as f:
            f.writelines(rapid_fire_blocks)

        ass_header = (
            "[Script Info]\n"
            "Title: OmniMatrix Kinetic Subtitles\n"
            "ScriptType: v4.00+\n"
            "WrapStyle: 0\n"
            "ScaledBorderAndShadow: yes\n"
            "YCbCr Matrix: None\n\n"
            "[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: Default,Arial,48,{karaoke_color},&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n"
            "[Events]\n"
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        )
        with open(karaoke_ass_path, "w", encoding="utf-8") as f:
            f.write(ass_header)
            f.writelines(ass_dialogue_lines)

        module_audio["agent_13_subtitle_assets"] = {
            "long_form_srt": long_form_path,
            "short_form_srt": short_form_path,
            "karaoke_ass": karaoke_ass_path
        }

        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] SRT & True ASS Karaoke subtitles exported to: {export_dir}", flush=True)
        return state
