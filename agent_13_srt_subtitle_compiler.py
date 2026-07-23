import os
import sys
import json

class Agent13SrtSubtitleCompiler:
    def __init__(self):
        self.agent_name = "Agent_13"
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.export_dir = os.path.join(self.workspace_dir, "Exports", "Subtitles")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Upstream modules must run first.", "FATAL")
            sys.exit(1)
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.log(f"JSON Corruption detected: {e}", "FATAL")
            sys.exit(1)

    def _save_matrix_state(self, state_data):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4, ensure_ascii=False)
        self.log("OmniMatrix state successfully updated with universal subtitle paths.", "SUCCESS")

    def _write_srt_file(self, blocks, file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for idx, block in enumerate(blocks):
                    f.write(f"{idx + 1}\n")
                    f.write(f"{block['start']} --> {block['end']}\n")
                    f.write(f"{block['text']}\n\n")
            self.log(f"Subtitles written successfully: {os.path.basename(file_path)}")
            return True
        except Exception as e:
            self.log(f"Failed to write SRT file: {str(e)}", "ERROR")
            return False

    def _chunk_words_for_long_form(self, words_list, max_words_per_line=6):
        """
        [LONG-FORM FEATURE]
        Chunks a long list of words into readable Netflix/YouTube standard lines.
        Ensures long paragraphs don't clutter the screen.
        """
        chunks = []
        current_chunk = []
        
        for word in words_list:
            current_chunk.append(word)
            # Break chunk if max words reached OR if the word has a natural pause (punctuation)
            if len(current_chunk) >= max_words_per_line or word.get("word_raw", "").endswith((".", "?", "!", ",")):
                chunks.append(current_chunk)
                current_chunk = []
                
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

    def execute_compilation(self):
        state = self._load_matrix_state()
        
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator expected '{orchestrator.get('next_agent')}'.", "WARNING")
            sys.exit(0)

        global_config = state.get("global_config", {})
        karaoke_color = global_config.get("subtitle_settings", {}).get("karaoke_highlight_color", "#FFFF00")

        audio_module = state.get("module_b_audio", {})
        audio_timeline = audio_module.get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("Audio timeline is empty.", "FATAL")
            sys.exit(1)

        self.log(f"Compiling Universal SRTs (Long-Form Cinematic & Short-Form Rapid) for {len(audio_timeline)} frames...", "STATUS")

        long_form_blocks = []
        rapid_fire_blocks = []
        karaoke_blocks = []

        for frame in audio_timeline:
            timing_data = frame.get("global_timing", {})
            f_start = timing_data.get("srt_frame_start", "00:00:00,000")
            f_end = timing_data.get("srt_frame_end", "00:00:01,000")
            
            words_align = frame.get("words_alignment", [])
            spoken_words = [w for w in words_align if w.get("is_spoken", True)]
            
            if not spoken_words:
                continue

            # --- 1. Long-Form Cinematic Subtitles (Smart Chunking) ---
            chunked_words = self._chunk_words_for_long_form(spoken_words, max_words_per_line=6)
            for chunk in chunked_words:
                if not chunk: continue
                chunk_start = chunk[0].get("srt_start", f_start)
                chunk_end = chunk[-1].get("srt_end", f_end)
                chunk_text = " ".join([w.get("word_raw", "") for w in chunk]).strip()
                
                long_form_blocks.append({
                    "start": chunk_start,
                    "end": chunk_end,
                    "text": chunk_text
                })

            # --- 2. Short-Form Rapid-Fire Subtitles (Word by Word) ---
            for word_item in spoken_words:
                word_text = word_item.get("word_clean", word_item.get("word_raw", "")).strip()
                uppercase_word = word_text.upper()
                
                if uppercase_word:
                    rapid_fire_blocks.append({
                        "start": word_item.get("srt_start", f_start),
                        "end": word_item.get("srt_end", f_end),
                        "text": uppercase_word
                    })

            # --- 3. Dynamic Karaoke (For stylized edits) ---
            for i, target_word in enumerate(spoken_words):
                karaoke_text_parts = []
                for j, w in enumerate(spoken_words):
                    base_word = w.get("word_raw", "")
                    if i == j:
                        karaoke_text_parts.append(f"<font color=\"{karaoke_color}\"><b>{base_word.upper()}</b></font>")
                    else:
                        karaoke_text_parts.append(base_word)
                
                karaoke_blocks.append({
                    "start": target_word.get("srt_start", f_start),
                    "end": target_word.get("srt_end", f_end),
                    "text": " ".join(karaoke_text_parts)
                })

        # File paths setup
        long_form_path = os.path.join(self.export_dir, "long_form_cinematic.srt")
        short_form_path = os.path.join(self.export_dir, "short_form_rapid.srt")
        karaoke_path = os.path.join(self.export_dir, "karaoke_dynamic.srt")

        # Generate all variations
        self._write_srt_file(long_form_blocks, long_form_path)
        self._write_srt_file(rapid_fire_blocks, short_form_path)
        self._write_srt_file(karaoke_blocks, karaoke_path)

        # Update state
        state["module_b_audio"]["subtitle_assets"] = {
            "long_form_srt": long_form_path,
            "short_form_srt": short_form_path,
            "karaoke_srt": karaoke_path
        }
        
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        # Ai Agent 14 DOES need an AI Brain to analyze beat drops logically
        state["orchestrator_matrix"]["next_agent"] = "Ai_Agent_14" 
        
        self._save_matrix_state(state)
        self.log(f"Universal Subtitles Ready! Handoff to Ai_Agent_14 (Phonk Beat Drop Analyzer).")

if __name__ == "__main__":
    compiler = Agent13SrtSubtitleCompiler()
    compiler.execute_compilation()
