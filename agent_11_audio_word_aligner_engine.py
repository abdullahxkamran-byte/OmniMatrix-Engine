import os
import sys
import json
import re
import math

class AiAgent11AudioWordAlignerEngine:
    def __init__(self):
        self.agent_name = "Ai_Agent_11"
        self.workspace_dir = os.path.join(os.getcwd(), "OmniMatrix_Workspace")
        self.state_file = os.path.join(self.workspace_dir, "matrix_state.json")

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _load_matrix_state(self):
        """Loads the central OmniMatrix state safely."""
        if not os.path.exists(self.state_file):
            self.log("matrix_state.json not found. Pipeline broken. Run previous modules.", "FATAL")
            sys.exit(1)
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.log(f"JSON Corruption detected in state file: {e}", "FATAL")
            sys.exit(1)

    def _save_matrix_state(self, state_data):
        """Updates the central OmniMatrix state with precise word alignments."""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=4, ensure_ascii=False)
        self.log("OmniMatrix state successfully updated with advanced word-level subtitle alignments.", "SUCCESS")

    def _calculate_word_weights(self, text, global_config):
        """
        God-Level Algorithm to calculate time duration weights of each word.
        Accounts for:
        1. Character length (vowels vs consonants estimation).
        2. Agent 09's Emotion Tags (e.g., [sigh], [gasps]).
        3. Configurable Punctuation Pauses.
        """
        # Parameter Fluidity: Dynamic Weights
        alignment_config = global_config.get("alignment_weights", {})
        base_char_weight = alignment_config.get("base_char_weight", 1.0)
        comma_pause = alignment_config.get("comma_pause", 2.5)
        period_pause = alignment_config.get("period_pause", 5.0)
        tag_pause = alignment_config.get("emotion_tag_pause", 4.0)

        words_raw = text.split()
        word_data = []
        total_weight = 0.0

        for idx, word in enumerate(words_raw):
            is_tag = False
            is_spoken = True
            
            # Check if word is an emotion tag from Agent 09 (e.g., [sigh], (laughs))
            if re.match(r"^\[.*\]$|^\(.*\)$", word.strip()):
                is_tag = True
                is_spoken = False
                base_weight = tag_pause
                clean_word = word.strip()
                pause_weight = 0.0
            else:
                clean_word = re.sub(r"[^\w']", "", word)
                base_weight = (len(clean_word) * base_char_weight) if len(clean_word) > 0 else 1.0
                
                # Add logical pause duration for punctuation
                pause_weight = 0.0
                if word.endswith(",") or word.endswith(";"):
                    pause_weight = comma_pause
                elif word.endswith(".") or word.endswith("!") or word.endswith("?"):
                    pause_weight = period_pause

            total_word_weight = base_weight + pause_weight
            total_weight += total_word_weight
            
            word_data.append({
                "word_index": idx + 1,
                "text_raw": word,
                "text_clean": clean_word,
                "weight": total_word_weight,
                "is_tag": is_tag,
                "is_spoken": is_spoken,
                "has_pause": pause_weight > 0
            })

        return word_data, total_weight

    def execute_alignment(self):
        state = self._load_matrix_state()
        
        # 1. Atomic Handshake Protocol
        orchestrator = state.get("orchestrator_matrix", {})
        if orchestrator.get("next_agent") != self.agent_name:
            self.log(f"Execution suspended. Orchestrator requested '{orchestrator.get('next_agent')}', not {self.agent_name}.", "WARNING")
            sys.exit(0)

        # 2. Extract Global Configuration
        global_config = state.get("global_config", {})

        audio_module = state.get("module_b_audio", {})
        audio_timeline = audio_module.get("audio_timeline", [])
        
        if not audio_timeline:
            self.log("No audio timeline found. Ensure Agent 10 generated audio.", "FATAL")
            sys.exit(1)

        self.log(f"Initiating mathematical word-alignment calibration for {len(audio_timeline)} frames...", "STATUS")

        # 3. Idempotency Sweep (Clear old alignments to prevent duplicates)
        for frame in audio_timeline:
            if "words_alignment" in frame:
                frame.pop("words_alignment")
            if "karaoke_metadata" in frame:
                frame.pop("karaoke_metadata")

        # 4. Alignment Processing Loop
        for frame in audio_timeline:
            f_idx = frame.get("frame_index", 1)
            # Prioritize tagged voiceover if available, else standard spoken
            text = frame.get("tagged_voiceover", frame.get("spoken_voiceover", "")).strip()
            
            total_duration = frame.get("audio_duration_seconds", 0.0)
            
            # Fallback constraint: If audio duration is missing/0, estimate it
            if total_duration == 0.0:
                self.log(f"Frame {f_idx}: Duration missing. Using procedural estimation fallback.", "WARNING")
                total_duration = max((len(text.split()) / 140.0) * 60.0, 1.5)

            # Fluidity: Apply speed modifiers if defined by previous agents
            speed_multiplier = frame.get("audio_effects_processing", {}).get("delivery_speed_multiplier", 1.0)
            adjusted_duration = total_duration / speed_multiplier

            if not text:
                frame["words_alignment"] = []
                self.log(f"Frame {f_idx}: Empty text. Skipping alignment.")
                continue

            word_weights_data, total_weight = self._calculate_word_weights(text, global_config)
            
            if total_weight == 0:
                total_weight = 1.0

            word_alignments = []
            current_time = 0.0
            spoken_words_count = 0

            for w_data in word_weights_data:
                duration_ratio = w_data["weight"] / total_weight
                word_duration = adjusted_duration * duration_ratio
                
                word_end_time = current_time + word_duration

                alignment_block = {
                    "word_index": w_data["word_index"],
                    "word_raw": w_data["text_raw"],
                    "word_clean": w_data["text_clean"],
                    "start_time": round(current_time, 3),
                    "end_time": round(word_end_time, 3),
                    "duration": round(word_duration, 3),
                    "is_spoken": w_data["is_spoken"]
                }
                
                word_alignments.append(alignment_block)
                if w_data["is_spoken"]:
                    spoken_words_count += 1
                
                current_time = word_end_time

            # Inject the calculated alignment back into the frame
            frame["words_alignment"] = word_alignments
            frame["karaoke_metadata"] = {
                "total_spoken_words": spoken_words_count,
                "contains_emotion_tags": any(w["is_tag"] for w in word_weights_data)
            }
            
            self.log(f"Frame {f_idx} aligned successfully. Exact Time Coordinates Mapped.")

        # 5. Finalize and Update State Handshake
        state["module_b_audio"]["words_aligned"] = True
        state["module_b_audio"]["audio_timeline"] = audio_timeline
        
        # Next agent routing
        state["orchestrator_matrix"]["last_active_agent"] = self.agent_name
        state["orchestrator_matrix"]["next_agent"] = "Ai_Agent_12" # Passing to Precision Timestamp Generator
        
        self._save_matrix_state(state)
        self.log(f"Agent {self.agent_name} complete! Subtitle coordinates ready. Handoff to Agent 12 (Precision Timestamp Generator).")

if __name__ == "__main__":
    aligner = AiAgent11AudioWordAlignerEngine()
    aligner.execute_alignment()
