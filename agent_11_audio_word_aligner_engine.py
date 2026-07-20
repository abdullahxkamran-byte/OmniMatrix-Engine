import os
import sys
import json
import re

class OmniMatrixWordAlignerEngine:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 11: audio_word_aligner_engine"
        self.workspace_dir = workspace_dir
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        """Loads the central OmniMatrix state."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Run previous modules first.", "ERROR")
            sys.exit(1)
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_matrix_state(self, state_data):
        """Updates the central OmniMatrix state with precise word alignments."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4)
        self.log("OmniMatrix state successfully updated with word-level subtitle alignments.")

    def _calculate_word_weights(self, text):
        """
        Advanced algorithm to calculate the weight (time duration) of each word.
        Accounts for character length and adds logical pauses for punctuation.
        """
        words_raw = text.split()
        word_data = []
        total_weight = 0.0

        for idx, word in enumerate(words_raw):
            clean_word = re.sub(r"[^\w']", "", word)
            base_weight = len(clean_word) if len(clean_word) > 0 else 1.0
            
            # Add extra weight (pause duration) if the word contains punctuation
            pause_weight = 0.0
            if word.endswith(",") or word.endswith(";"):
                pause_weight = 2.5  # Short pause
            elif word.endswith(".") or word.endswith("!") or word.endswith("?"):
                pause_weight = 5.0  # Long pause

            total_word_weight = base_weight + pause_weight
            total_weight += total_word_weight
            
            word_data.append({
                "word_index": idx + 1,
                "text_raw": word,
                "text_clean": clean_word,
                "weight": total_word_weight,
                "has_pause": pause_weight > 0
            })

        return word_data, total_weight

    def execute_alignment(self):
        state = self._load_matrix_state()
        
        # Verify Pipeline Sequence
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        # Note: Bypassing strict pipeline check here to allow independent testing if needed, 
        # but logging the intended flow.
        if target_agent and target_agent != "Agent_11":
            self.log(f"Pipeline sync note: System expected {target_agent}, but executing {self.agent_name}.")

        audio_module = state.get("module_b_audio", {})
        audio_timeline = audio_module.get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("No audio timeline found. Ensure Agent 09 has generated audio assets.", "ERROR")
            return

        self.log(f"Starting mathematical word-alignment calibration for {len(audio_timeline)} frames...")

        for frame in audio_timeline:
            f_idx = frame.get("frame_index", 1)
            text = frame.get("spoken_voiceover", "").strip()
            
            # Fetch the exact duration calculated by Agent 09 (or estimate if missing)
            total_duration = frame.get("audio_duration_seconds", 0.0)
            if total_duration == 0.0:
                # Fallback estimation (roughly 140 words per minute)
                total_duration = max((len(text.split()) / 140.0) * 60.0, 1.5)

            # Apply Agent 10's speed modifiers if they exist
            speed_multiplier = frame.get("audio_effects_processing", {}).get("delivery_speed_multiplier", 1.0)
            adjusted_duration = total_duration / speed_multiplier

            if not text:
                frame["words_alignment"] = []
                continue

            word_weights_data, total_weight = self._calculate_word_weights(text)
            
            if total_weight == 0:
                total_weight = 1.0

            word_alignments = []
            current_time = 0.0

            for w_data in word_weights_data:
                # Calculate exact seconds this word occupies based on its weight ratio
                duration_ratio = w_data["weight"] / total_weight
                word_duration = adjusted_duration * duration_ratio
                
                word_end_time = current_time + word_duration

                word_alignments.append({
                    "word_index": w_data["word_index"],
                    "word": w_data["text_clean"],
                    "start_time": round(current_time, 3),
                    "end_time": round(word_end_time, 3),
                    "duration": round(word_duration, 3)
                })
                
                current_time = word_end_time

            # Inject the calculated alignment back into the frame
            frame["words_alignment"] = word_alignments
            self.log(f"Frame {f_idx} aligned successfully. Total words: {len(word_alignments)}.")

        # Finalize and update state
        state["module_b_audio"]["words_aligned"] = True
        state["module_b_audio"]["audio_timeline"] = audio_timeline
        
        # OmniMatrix Handshake
        state["pipeline_status"]["last_active_agent"] = "Agent_11"
        state["pipeline_status"]["next_agent"] = "Agent_12"
        
        self._save_matrix_state(state)
        self.log("Alignment complete! Subtitle coordinates generated. Handoff to Agent 12.")

if __name__ == "__main__":
    aligner = OmniMatrixWordAlignerEngine()
    aligner.execute_alignment()
    print("\n--- OMNIMATRIX VOCAL MODULE B: AGENT 11 COMPLETE ---")
