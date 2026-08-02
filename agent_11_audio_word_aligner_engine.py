import os
import re
import sys
import json
import subprocess

class Agent_11_Audio_Word_Aligner_Engine:
    def __init__(self):
        self.agent_name = "Agent_11_Audio_Word_Aligner_Engine"

    def _get_audio_duration(self, file_path: str) -> float:
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=15
            )
            return float(result.stdout.strip())
        except Exception:
            return 0.0

    def _get_acoustic_speech_chunks(self, file_path: str, total_duration: float) -> list:
        chunks = []
        try:
            result = subprocess.run(
                ["ffmpeg", "-i", file_path, "-af", "silencedetect=noise=-35dB:d=0.4", "-f", "null", "-"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30
            )
            output = result.stdout
            silence_starts = [float(x) for x in re.findall(r"silence_start: ([\d\.]+)", output)]
            silence_ends = [float(x) for x in re.findall(r"silence_end: ([\d\.]+)", output)]
            
            current_time = 0.0
            for i in range(len(silence_starts)):
                if silence_starts[i] > current_time:
                    chunks.append({"start": current_time, "end": silence_starts[i]})
                if i < len(silence_ends):
                    current_time = silence_ends[i]
            
            if current_time < total_duration:
                chunks.append({"start": current_time, "end": total_duration})
                
        except Exception:
            pass
            
        if not chunks:
            chunks = [{"start": 0.0, "end": max(total_duration, 1.0)}]
        return chunks

    def _calculate_vowel_syllable_weight(self, word: str) -> float:
        clean_word = re.sub(r"[^\w]", "", word.lower())
        if not clean_word:
            return 0.5
        vowel_groups = len(re.findall(r'[aeiouy]+', clean_word))
        syllables = max(1, vowel_groups)
        return float(syllables) + (len(clean_word) * 0.05)

    def _tokenize_text(self, text: str) -> list:
        raw_tokens = re.findall(r"\[.*?\]|\(.*?\)|[^\s]+", text)
        tokens = []
        for token in raw_tokens:
            is_tag = bool(re.match(r"^\[.*\]$|^\(.*\)$", token))
            pause_weight = 0.0
            if not is_tag:
                if token.endswith(",") or token.endswith(";"):
                    pause_weight = 1.5
                elif token.endswith(".") or token.endswith("!") or token.endswith("?"):
                    pause_weight = 2.5
            
            base_weight = 1.5 if is_tag else self._calculate_vowel_syllable_weight(token)
            
            tokens.append({
                "raw_text": token,
                "clean_text": re.sub(r"[^\w']", "", token) if not is_tag else token,
                "is_tag": is_tag,
                "weight": base_weight + pause_weight,
                "pause_padding": pause_weight
            })
        return tokens

    def _align_words_to_chunks(self, tokens: list, chunks: list, total_duration: float) -> list:
        if not tokens:
            return []
            
        total_weight = sum(t["weight"] for t in tokens)
        word_alignments = []
        
        current_chunk_idx = 0
        current_time = chunks[0]["start"]
        
        for i, token in enumerate(tokens):
            proportion = token["weight"] / total_weight
            word_duration = round(total_duration * proportion, 3)
            
            chunk_end = chunks[current_chunk_idx]["end"]
            
            if current_time + word_duration > chunk_end and current_chunk_idx < len(chunks) - 1:
                current_chunk_idx += 1
                current_time = chunks[current_chunk_idx]["start"]
                
            start_time = round(current_time, 3)
            end_time = round(start_time + word_duration, 3)
            
            word_alignments.append({
                "word_index": i + 1,
                "word_raw": token["raw_text"],
                "word_clean": token["clean_text"],
                "is_tag": token["is_tag"],
                "start_time": start_time,
                "end_time": end_time,
                "duration": word_duration
            })
            
            current_time = end_time

        return word_alignments

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")

        if target_agent and "11" not in target_agent and target_agent != self.agent_name:
            print(f"[{self.agent_name}] Execution skipped. Queue targeted to: {target_agent}", flush=True)
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

        audio_files = module_audio.get("agent_10_audio_files", [])
        emotion_matrix = module_audio.get("agent_09_audio_emotions", [])

        if not audio_files:
            raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: 'agent_10_audio_files' missing.")

        if "agent_11_word_alignment" in module_audio:
            del module_audio["agent_11_word_alignment"]
            print(f"[{self.agent_name}] Idempotency sweep executed. Legacy alignment purged.", flush=True)

        emotion_map = {f.get("frame_index"): f.get("tagged_voiceover", "") for f in emotion_matrix}
        aligned_frames_output = []

        print(f"[{self.agent_name}] Executing Advanced Acoustic Syllable Alignment for {len(audio_files)} frames...", flush=True)

        for audio_entry in audio_files:
            idx = audio_entry.get("frame_index", 1)
            file_path = audio_entry.get("file_path", "")
            character = audio_entry.get("character_voice", "Narrator")

            raw_text = emotion_map.get(idx, "")
            
            actual_duration = audio_entry.get("duration_seconds", 0.0)
            if actual_duration <= 0.0 and os.path.exists(file_path):
                actual_duration = self._get_audio_duration(file_path)

            if actual_duration == 0.0:
                print(f"[{self.agent_name}] Warning: Frame {idx} audio duration is 0. Mathematical approximation triggered.", flush=True)
                actual_duration = max((len(raw_text.split()) / 2.5), 1.0)

            tokens = self._tokenize_text(raw_text)
            acoustic_chunks = self._get_acoustic_speech_chunks(file_path, actual_duration)
            
            word_timestamps = self._align_words_to_chunks(tokens, acoustic_chunks, actual_duration)

            aligned_frames_output.append({
                "frame_index": idx,
                "character_voice": character,
                "audio_file_path": file_path,
                "total_duration_seconds": actual_duration,
                "total_tokens": len(tokens),
                "word_alignments": word_timestamps
            })

        module_audio["agent_11_word_alignment"] = aligned_frames_output

        pipeline_status = state.setdefault("pipeline_status", {})
        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Acoustic Alignment matrix locked successfully.", flush=True)
        return state
