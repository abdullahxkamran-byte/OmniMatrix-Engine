import os
import sys
import gc
import json
import ctypes
import platform
import subprocess
from datetime import datetime

class AutomatedBackgroundRamJanitor:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 63: automated_background_ram_janitor"
        self.workspace_dir = workspace_dir
        self.log_file_path = os.path.join(self.workspace_dir, "63_ram_janitor_log.json")
        self.ram_status_path = os.path.join(self.workspace_dir, "60_ram_status.json")

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def run_janitor_cleanup(self):
        print(f"[{self.agent_name}] Starting automated background RAM cleanup pipeline...")
        
        # Step 1: Force Python Garbage Collection
        initial_gc_count = gc.get_count()
        objects_freed = gc.collect()
        print(f"[{self.agent_name}] Python Garbage Collector executed. Objects freed: {objects_freed}")

        # Step 2: Read RAM status from Agent 60 if available
        ram_status_context = "No previous RAM report found."
        cleanup_urgency = "LOW"
        if os.path.exists(self.ram_status_path):
            try:
                with open(self.ram_status_path, "r", encoding="utf-8") as f:
                    status_data = json.load(f)
                used_pct = status_data.get("metrics", {}).get("used_percentage", 0.0)
                status = status_data.get("status", "OK")
                ram_status_context = f"Detected {used_pct}% RAM usage with status: {status}"
                
                if status == "CRITICAL":
                    cleanup_urgency = "CRITICAL"
                elif status == "WARNING":
                    cleanup_urgency = "HIGH"
            except Exception as e:
                ram_status_context = f"Error reading Agent 60 status: {str(e)}"

        print(f"[{self.agent_name}] Current RAM Context: {ram_status_context}")

        # Step 3: Platform specific system RAM release
        system_platform = platform.system().lower()
        platform_cleanup_status = "Skipped (No high-level permission)"

        if "windows" in system_platform:
            # Empty working set of current process using Windows API
            try:
                # Get current process handle
                handle = ctypes.windll.kernel32.GetCurrentProcess()
                # Call EmptyWorkingSet from psapi.dll
                # This minimizes physical memory usage of our workspace process
                result = ctypes.windll.psapi.EmptyWorkingSet(handle)
                if result:
                    platform_cleanup_status = "Successfully flushed current process working set using Win32 API."
                else:
                    platform_cleanup_status = "Win32 API EmptyWorkingSet failed to execute."
            except Exception as e:
                platform_cleanup_status = f"Windows API cleanup exception: {str(e)}"

        elif "linux" in system_platform:
            # Sync disks and free memory caches if running as root
            if os.getuid() == 0:
                try:
                    # Clear pagecache, dentries, and inodes
                    subprocess.run("sync; echo 3 > /proc/sys/vm/drop_caches", shell=True, check=True)
                    platform_cleanup_status = "Root execution: Successfully cleared pagecache, dentries, and inodes."
                except Exception as e:
                    platform_cleanup_status = f"Failed to drop Linux caches: {str(e)}"
            else:
                platform_cleanup_status = "Linux cache clearing skipped: Script is not running with sudo/root privileges."

        elif "darwin" in system_platform:
            # Purge memory cache on macOS
            try:
                subprocess.run(["purge"], check=True)
                platform_cleanup_status = "macOS purge command executed successfully."
            except Exception as e:
                platform_cleanup_status = f"macOS purge failed: {str(e)}"

        # Step 4: Finalize and log cleanup results
        cleanup_report = {
            "agent": self.agent_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cleanup_urgency": cleanup_urgency,
            "gc_stats": {
                "initial_gc_state": initial_gc_count,
                "objects_collected": objects_freed
            },
            "system_context_read": ram_status_context,
            "platform_action_taken": platform_cleanup_status
        }

        self._save_log(cleanup_report)
        print(f"[{self.agent_name}] RAM cleanup successfully complete. Report written to workspace.")
        return cleanup_report

    def _save_log(self, data):
        try:
            with open(self.log_file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[{self.agent_name}] Error writing janitor log: {str(e)}")

if __name__ == "__main__":
    janitor = AutomatedBackgroundRamJanitor()
    report = janitor.run_janitor_cleanup()
    print("\n--- Z-NET RAM JANITOR REPORT ---")
    print(f"Time:          {report['timestamp']}")
    print(f"Urgency Level: {report['cleanup_urgency']}")
    print(f"Python GC:     Freed {report['gc_stats']['objects_collected']} unreferenced objects")
    print(f"OS Action:     {report['platform_action_taken']}")
    print("--------------------------------")
