import os
import re
import sys
import json
import glob
import time
import shutil

# =====================================================================
# RULE 2: UNIVERSAL ENVIRONMENT CONFIGURATION (PURE UTILITY)
# =====================================================================
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip().upper()] = val.strip()

load_env_file()

class Agent_42_FFmpeg_Raw_Buffer_Collector:
    """
    OMNIMATRIX V2.0 PURE UTILITY: RAW BUFFER & STREAM COLLECTOR (SUPERCHARGED)
    Recursively scans all workspace directories for rendered visual frames and acoustic tracks,
    validates frame continuity, patches sequence gaps dynamically without blackouts,
    and constructs actionable FFmpeg concatenation demuxer files.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "Agent_42_FFmpeg_Raw_Buffer_Collector"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        
        # Primary search targets along with full recursive workspace capability
        self.render_dir = os.path.join(self.workspace_dir, "render_output")
        self.audio_dir = os.path.join(self.workspace_dir, "audio_output")
        
        for directory in [self.workspace_dir, self.render_dir, self.audio_dir]:
            os.makedirs(directory, exist_ok=True)
            
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        formatted = f"[{level}] [{self.agent_name}] {message}"
        print(formatted)

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous manifests and concat directives."""
        for filename in ["42_raw_buffer_manifest.json", "ffmpeg_concat_demuxer.txt"]:
            file_path = os.path.join(self.workspace_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as error:
                    self.log(f"Failed to scrub legacy buffer file {file_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & TIMELINE SYNCHRONIZATION
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS"):
        matrix_path = os.path.join(self.workspace_dir, "matrix_state.json")
        data = {}
        if os.path.exists(matrix_path):
            try:
                with open(matrix_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        if "orchestrator_matrix" not in data:
            data["orchestrator_matrix"] = {}
            
        data["orchestrator_matrix"].update({
            "last_active_agent": self.agent_name,
            "last_update_timestamp": time.time(),
            "agent_status": {self.agent_name: status}
        })
        
        if status == "COMPLETED":
            # Hand off to Agent 43 (Multi-Track Audio/Video Merger) in standard lowercase
            data["orchestrator_matrix"]["next_agent"] = "agent_43_multi_track_av_merger"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _load_target_fps(self):
        """Fetches synchronized timeline framerate from project configuration."""
        config_path = os.path.join(self.workspace_dir, "01_omnimatrix_project_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return float(json.load(f).get("render_fps", 24.0))
            except Exception:
                pass
        return 24.0

    def _extract_frame_index(self, filename):
        """Extracts numeric frame index from arbitrary rendering nomenclature."""
        match = re.search(r'(\d+)\.(png|jpg|jpeg|exr|tiff|webp)$', filename, re.IGNORECASE)
        return int(match.group(1)) if match else None

    # =====================================================================
    # DETERMINISTIC RECURSIVE STREAM DISCOVERY & GAP AUTO-PATCHING
    # =====================================================================
    def _scan_and_validate_visual_buffers(self, fps):
        self.log(f"Executing recursive visual buffer discovery across entire workspace: '{self.workspace_dir}'")
        valid_exts = ('.png', '.jpg', '.jpeg', '.exr', '.tiff', '.webp')
        discovered_files = []

        # Recursively search all potential output folders in workspace
        for root, dirs, files in os.walk(self.workspace_dir):
            # Ignore internal manifests or thumbnail previews if actual renders exist
            for file in files:
                if file.lower().endswith(valid_exts):
                    # Exclude non-sequence static UI assets unless they are the only frames
                    if not any(ignore_kw in file.lower() for ignore_kw in ["thumbnail", "vignette", "letterbox"]):
                        discovered_files.append(os.path.join(root, file))

        # Fallback: If only static assets exist, grab everything to ensure visual stream compilation
        if not discovered_files:
            for root, dirs, files in os.walk(self.workspace_dir):
                for file in files:
                    if file.lower().endswith(valid_exts):
                        discovered_files.append(os.path.join(root, file))

        # Rule 10: 100% Offline Autonomy fallback if workspace is completely devoid of visual files
        if not discovered_files:
            self.log("No rendered visual buffers detected anywhere in workspace. Generating FFmpeg synthetic test stream directive.", "WARNING")
            return [], [], True

        # Rule 17: VRAM/Memory cap - sort and process maximum 15,000 frames
        sorted_frames = []
        for file_path in discovered_files[:15000]:
            index = self._extract_frame_index(file_path)
            # If filename lacks sequence numbers, assign sequential fallback index based on modification time
            if index is None:
                index = int(os.path.getmtime(file_path) * 1000) % 1000000
            sorted_frames.append((index, file_path))
        
        sorted_frames.sort(key=lambda x: x[0])

        if not sorted_frames:
            return [], [], True

        start_index = sorted_frames[0][0]
        end_index = sorted_frames[-1][0]
        expected_indices = set(range(start_index, end_index + 1))
        actual_indices = set([item[0] for item in sorted_frames])
        missing_indices = sorted(list(expected_indices - actual_indices))

        if missing_indices and len(sorted_frames) > 1:
            self.log(f"Sequence discontinuity detected. Missing frame indices: {len(missing_indices)} frames. Initiating auto-patch protocol.", "WARNING")
        else:
            self.log(f"Visual stream continuity verified successfully. Total frames mapped: {len(sorted_frames)}.", "SUCCESS")

        return sorted_frames, missing_indices, False

    def _collect_audio_buffers(self):
        self.log(f"Executing recursive acoustic buffer discovery across workspace: '{self.workspace_dir}'")
        valid_exts = ('.wav', '.flac', '.mp3', '.m4a', '.aac', '.ogg')
        discovered_audio = []

        for root, dirs, files in os.walk(self.workspace_dir):
            for file in files:
                if file.lower().endswith(valid_exts):
                    discovered_audio.append(os.path.join(root, file))

        # Prioritize Module B finalized master audio mix if present
        master_mix_path = os.path.join(self.workspace_dir, "19_final_master_mix.wav")
        if os.path.exists(master_mix_path):
            self.log("Module B finalized master acoustic mix detected and prioritized.", "SUCCESS")
            if master_mix_path in discovered_audio:
                discovered_audio.remove(master_mix_path)
            discovered_audio.insert(0, master_mix_path)

        if not discovered_audio:
            self.log("No acoustic buffers found. Pipeline will assemble silent visual stream.", "WARNING")

        return discovered_audio

    # =====================================================================
    # RULE 9: ACTIONABLE FFMPEG DEMUXER COMPILER
    # =====================================================================
    def _compile_actionable_ffconcat(self, sorted_frames, missing_indices, fps):
        """
        Rule 9 & 10: Compiles an executable FFmpeg concat file. If frames are missing,
        it automatically extends the duration of the preceding valid frame to bridge gaps
        without causing rendering blackouts or demuxer crashes!
        """
        concat_file_path = os.path.join(self.workspace_dir, "ffmpeg_concat_demuxer.txt")
        frame_duration = 1.0 / fps
        missing_set = set(missing_indices)

        with open(concat_file_path, "w", encoding="utf-8") as f:
            f.write("ffconcat version 1.0\n")
            
            for i, (index, file_path) in enumerate(sorted_frames):
                safe_path = file_path.replace("\\", "/")
                f.write(f"file '{safe_path}'\n")
                
                # Check how many consecutive frames are missing right after this frame
                gap_count = 0
                check_index = index + 1
                while check_index in missing_set:
                    gap_count += 1
                    check_index += 1
                
                # Extend duration to patch the missing gap perfectly
                total_duration = frame_duration * (1 + gap_count)
                f.write(f"duration {total_duration:.6f}\n")
                
        self.log(f"Actionable FFmpeg concat demuxer compiled: '{concat_file_path}'", "SUCCESS")
        return concat_file_path

    def execute_collection(self):
        self._handshake("IN_PROGRESS")
        fps = self._load_target_fps()
        
        sorted_frames, missing_indices, is_synthetic_fallback = self._scan_and_validate_visual_buffers(fps)
        audio_buffers = self._collect_audio_buffers()

        actionable_directive = None
        if not is_synthetic_fallback and sorted_frames:
            actionable_directive = self._compile_actionable_ffconcat(sorted_frames, missing_indices, fps)
        else:
            # Rule 10: Complete offline synthetic test stream fallback for downstream assembler
            actionable_directive = f"testsrc2=size=1920x1080:rate={int(fps)}"

        manifest = {
            "agent_executed": self.agent_name,
            "execution_timestamp": time.time(),
            "stream_integrity_status": "SYNTHETIC_TEST_FALLBACK" if is_synthetic_fallback else ("AUTO_PATCHED_GAPS" if missing_indices else "CONTINUOUS_VERIFIED"),
            "target_framerate_fps": fps,
            "total_visual_frames_mapped": len(sorted_frames),
            "missing_frame_indices_count": len(missing_indices),
            "actionable_ffmpeg_directive": actionable_directive,
            "mapped_visual_stream_start": sorted_frames[0][1] if sorted_frames else None,
            "mapped_visual_stream_end": sorted_frames[-1][1] if sorted_frames else None,
            "mapped_audio_buffer_paths": audio_buffers
        }

        manifest_path = os.path.join(self.workspace_dir, "42_raw_buffer_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)
            
        self.log(f"Raw buffer collection manifest locked: '{manifest_path}'", "SUCCESS")
        self._handshake("COMPLETED")
        return manifest

if __name__ == "__main__":
    collector = Agent_42_FFmpeg_Raw_Buffer_Collector()
    collector.execute_collection()
