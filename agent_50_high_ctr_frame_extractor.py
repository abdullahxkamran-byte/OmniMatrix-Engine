import os
import sys
import json
import subprocess
import shutil

class HighCtrFrameExtractor:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 50: high_ctr_frame_extractor"
        self.workspace_dir = workspace_dir
        self.scout_blueprint_path = os.path.join(self.workspace_dir, "49_media_scout_blueprint.json")
        self.output_frames_dir = os.path.join(self.workspace_dir, "extracted_ctr_frames")

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        if not os.path.exists(self.output_frames_dir):
            os.makedirs(self.output_frames_dir)

    def _load_scouted_timestamps(self):
        # Agent 49 ke blueprint se video file path aur scouted timestamps load karta hai
        video_path = os.path.join(self.workspace_dir, "48_final_denoised_clean.mp4")
        timestamps = []

        if os.path.exists(self.scout_blueprint_path):
            try:
                with open(self.scout_blueprint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                video_path = data.get("target_video_scouted", video_path)
                for frame in data.get("scouted_frames", []):
                    timestamps.append({
                        "time": float(frame.get("timestamp_sec", 0.0)),
                        "use_case": frame.get("potential_use_case", "General Frame")
                    })
            except Exception as e:
                print(f"[{self.agent_name}] Error reading scouted blueprint: {str(e)}")

        # Fallback frames list agar upstream blueprint khali ho ya missing ho
        if not timestamps:
            print(f"[{self.agent_name}] No scouted timestamps found. Using standard default timestamps.")
            timestamps = [
                {"time": 1.5, "use_case": "Primary Thumbnail Focus"},
                {"time": 4.2, "use_case": "TikTok Hook Preview"}
            ]

        # Safety check agar physical video system me sach me nahi hai to mock set karein
        if not os.path.exists(video_path):
            # Check for alternative render outputs
            alternatives = [
                os.path.join(self.workspace_dir, "47_super_resolved_4k_video.mp4"),
                os.path.join(self.workspace_dir, "44_gpu_accelerated_output.mp4")
            ]
            for alt in alternatives:
                if os.path.exists(alt):
                    video_path = alt
                    break

        return video_path, timestamps

    def extract_frames(self):
        print(f"[{self.agent_name}] Initializing high precision frame extractor...")
        video_path, timestamps = self._load_scouted_timestamps()
        
        extracted_files = []
        ffmpeg_path = shutil.which("ffmpeg")

        print(f"[{self.agent_name}] Extracting {len(timestamps)} high-CTR frames from video: '{video_path}'")

        for idx, ts_info in enumerate(timestamps):
            timestamp = ts_info["time"]
            use_case = ts_info["use_case"]
            
            # Format output name cleanly based on timestamp and use case
            safe_use_case = use_case.lower().replace(" ", "_")
            output_png = os.path.join(self.output_frames_dir, f"frame_{idx+1}_{safe_use_case}_{timestamp}s.png")

            # FFmpeg exact frame seek and draw command
            # -ss before -i ensures lighting-fast seek times
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(timestamp),
                "-i", video_path,
                "-vframes", "1",
                "-q:v", "2",  # High quality jpeg/png rendering
                output_png
            ]

            print(f"[{self.agent_name}] Extraction command frame {idx+1}: {' '.join(cmd)}")

            if not ffmpeg_path or not os.path.exists(video_path):
                print(f"[{self.agent_name}] Dry-run simulation. Successfully tracked frame extraction placeholder: {output_png}")
                extracted_files.append({
                    "frame_index": idx + 1,
                    "target_timestamp": timestamp,
                    "use_case": use_case,
                    "saved_path": output_png,
                    "status": "DRY_RUN_SUCCESS"
                })
                continue

            try:
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                print(f"[{self.agent_name}] Extracted frame successfully saved to {output_png}")
                extracted_files.append({
                    "frame_index": idx + 1,
                    "target_timestamp": timestamp,
                    "use_case": use_case,
                    "saved_path": output_png,
                    "status": "SUCCESS"
                })
            except subprocess.CalledProcessError as e:
                print(f"[{self.agent_name}] FFmpeg error extraction failed for timestamp {timestamp}s: {e.stderr}")
                extracted_files.append({
                    "frame_index": idx + 1,
                    "target_timestamp": timestamp,
                    "use_case": use_case,
                    "saved_path": output_png,
                    "status": f"FAILED: {str(e.stderr)}"
                })

        # Save results in output blueprint
        final_blueprint = {
            "agent_executed": self.agent_name,
            "source_video_used": video_path,
            "extracted_frames_metrics": extracted_files
        }
        self._save_blueprint(final_blueprint)
        return final_blueprint

    def _save_blueprint(self, data, filename="50_extracted_frames_blueprint.json"):
        file_path = os.path.join(self.workspace_dir, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Blueprint logs saved to '{file_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Failed to save extraction logs: {str(e)}")

if __name__ == "__main__":
    extractor = HighCtrFrameExtractor()
    result = extractor.extract_frames()
    
    print("\n--- Z-NET HIGH-CTR FRAME EXTRACTOR: AGENT 50 COMPLETE ---")
    print(f"Total processed extraction frames: {len(result['extracted_frames_metrics'])}")
    for item in result["extracted_frames_metrics"]:
        print(f"  Frame {item['frame_index']} | Time: {item['target_timestamp']}s | Use-Case: {item['use_case']}")
        print(f"    Output Path: '{item['saved_path']}' -> Status: {item['status']}")
    print("---------------------------------------------------------")
