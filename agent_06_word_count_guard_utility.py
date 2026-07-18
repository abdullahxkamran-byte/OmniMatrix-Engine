import os
import re
import sys
import json

class WordCountGuardUtility:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 06: word_count_guard_utility"
        self.workspace_dir = workspace_dir
        # Energetic short-form target: 2.5 words per second (WPS)
        self.target_words_per_second = 2.5 

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _load_previous_stage(self):
        """
        Loads upstream visual storyboard from Stage 3. If absent, 
        prompts the user to enter a custom script manually.
        """
        input_file_path = os.path.join(self.workspace_dir, "03_visual_storyboard.json")
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[{self.agent_name}] Success: Stage 3 storyboard loaded from '{input_file_path}'")
                return data
            except Exception as e:
                print(f"[{self.agent_name}] Warning: File read error ({str(e)}). Transitioning to manual input.")
        
        # Interactive fallback prompt if workspace has no active upstream data
        print(f"[{self.agent_name}] Pipeline Gap: Upstream data file '{input_file_path}' is missing.")
        user_input = input("Enter a raw voiceover script line to verify and compress: ").strip()
        if not user_input:
            print("[System Error] Empty input block. Halting utility.")
            sys.exit(1)
            
        return {
            "source_topic": "Manual Formatting",
            "storyboard_frames": [
                {
                    "frame_index": 1,
                    "timestamp_start": 0.0,
                    "timestamp_end": 4.0,
                    "spoken_voiceover": user_input
                }
            ]
        }

    def _programmatic_compress(self, text, max_words):
        """
        A 100% programmatic text compression engine. 
        Filters out non-essential filler words, adjectives, and adverbs first.
        If it still exceeds the limit, it performs a clean mathematical slice.
        """
        words = text.strip().split()
        if len(words) <= max_words:
            return " ".join(words)

        # High priority non-essential/filler words to strip first for concise narration
        filler_dictionary = {
            "absolutely", "actually", "basically", "completely", "extremely", "literally",
            "seriously", "truly", "very", "highly", "fully", "totally", "definitely", 
            "surely", "probably", "perhaps", "maybe", "really", "quite", "just", 
            "simply", "merely", "rather", "somewhat", "slightly", "somehow", "indeed", 
            "furthermore", "moreover", "essentially", "ultimately", "basically",
            "the", "a", "an", "and", "but", "or", "so", "yet", "for"
        }

        filtered_words = []
        removed_count = 0
        needed_removals = len(words) - max_words

        # Step 1: Strip common filler words to preserve primary nouns, actions, and verbs
        for word in words:
            cleaned_word = re.sub(r"[^\w]", "", word).lower()
            if cleaned_word in filler_dictionary and removed_count < needed_removals:
                removed_count += 1
                continue
            filtered_words.append(word)

        # Step 2: Hard-limit programmatic slicing if text is still too long
        if len(filtered_words) > max_words:
            filtered_words = filtered_words[:max_words]
            # Ensure the final truncated word ends cleanly
            if filtered_words:
                filtered_words[-1] = re.sub(r"[^\w]$", "", filtered_words[-1]) + "!"

        return " ".join(filtered_words)

    def _save_to_workspace(self, data, filename="06_word_count_guard.json"):
        """
        Persists the audited and cleaned storyboard to the workspace directory.
        """
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Success: Programmatic audit data saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"[{self.agent_name}] Critical Error: Unable to save state files: {str(e)}")
            return None

    def run_guard_utility(self):
        """
        Calculates maximum allowed words per frame based on time allocations,
        audits the script, and applies 100% deterministic compression rules.
        """
        input_data = self._load_previous_stage()
        topic = input_data.get("source_topic", "Dynamic Task")
        frames = input_data.get("storyboard_frames", [])

        print(f"[{self.agent_name}] Running programmatic pacing audit for: '{topic}'")

        audit_queue = []
        optimization_applied = False

        for frame in frames:
            f_idx = frame.get("frame_index", 1)
            start = float(frame.get("timestamp_start", 0.0))
            end = float(frame.get("timestamp_end", start + 3.0)) # Fallback 3s duration
            duration = max(end - start, 1.0)
            voiceover = frame.get("spoken_voiceover", "").strip()

            word_count = len(voiceover.split())
            max_recommended_words = int(duration * self.target_words_per_second)
            
            # Mathematical evaluation
            pacing_status = "safe"
            optimized_text = voiceover

            if word_count > max_recommended_words:
                pacing_status = "optimized_safe"
                optimized_text = self._programmatic_compress(voiceover, max_recommended_words)
                optimization_applied = True
                print(f"[{self.agent_name}] Frame {f_idx}: Truncated '{voiceover}' -> '{optimized_text}'")

            audit_queue.append({
                "frame_index": f_idx,
                "duration_seconds": round(duration, 2),
                "original_word_count": word_count,
                "max_recommended_words": max_recommended_words,
                "calculated_wps": round(len(optimized_text.split()) / duration, 2),
                "pacing_status": pacing_status,
                "spoken_voiceover": voiceover,
                "optimized_voiceover": optimized_text
            })

        final_output = {
            "source_topic": topic,
            "agent_executed": self.agent_name,
            "pacing_audited": True,
            "optimization_applied": optimization_applied,
            "timeline_frames": audit_queue
        }

        self._save_to_workspace(final_output)
        return final_output

if __name__ == "__main__":
    guard = WordCountGuardUtility()
    output = guard.run_guard_utility()
    
    print("\n--- Z-NET CORE UTILITY: AGeNT 06 PROGRAMMATIC COMPRESSION COMPLETED ---")
    print(json.dumps(output, indent=4))
    print("------------------------------------------------------------------------")
