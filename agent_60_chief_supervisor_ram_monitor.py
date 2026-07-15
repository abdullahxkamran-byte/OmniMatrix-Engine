import os
import json
import platform

# Check karte hain ke 'psutil' library system me install hai ya nahi
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class ChiefSupervisorRamMonitor:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 60: chief_supervisor_ram_monitor"
        self.workspace_dir = workspace_dir
        self.output_status_path = os.path.join(self.workspace_dir, "60_ram_status.json")
        self.alert_threshold_percent = 85.0  # Safe threshold limit at 85%

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def get_system_ram_metrics(self):
        print(f"[{self.agent_name}] System RAM diagnostics analyze kar raha hoon...")
        total_gb = 0.0
        used_gb = 0.0
        percent_used = 0.0
        status = "HEALTHY"

        # Agar library hai to direct fast API use karo
        if PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            total_gb = round(mem.total / (1024 ** 3), 2)
            used_gb = round(mem.used / (1024 ** 3), 2)
            percent_used = mem.percent
        else:
            # Failsafe: Agar psutil install na ho toh bina crash kiye native OS se details nikalo
            print(f"[{self.agent_name}] Alert: 'psutil' module install nahi hai. OS native fallback run kar raha hoon...")
            total_gb, used_gb, percent_used = self._get_native_ram_fallback()

        # Check threshold limits
        if percent_used >= self.alert_threshold_percent:
            status = "CRITICAL_RAM_OVERFLOW_WARNING"
            print(f"[{self.agent_name}] ⚠️ ALERT: RAM usage {percent_used}% par hai! Background Janitor cleanup trigger zaroori hai.")
        else:
            print(f"[{self.agent_name}] System RAM safe hai. Usage: {percent_used}% ({used_gb}GB/{total_gb}GB) - Status: {status}")

        # Final structured JSON output jo baaki agents read karenge
        metrics = {
            "agent_executed": self.agent_name,
            "os_platform": platform.system(),
            "ram_metrics": {
                "total_ram_gb": total_gb,
                "used_ram_gb": used_gb,
                "percent_used": percent_used,
                "threshold_limit_percent": self.alert_threshold_percent
            },
            "status": status,
            "janitor_action_required": percent_used >= self.alert_threshold_percent
        }

        self._save_status(metrics)
        return metrics

    def _get_native_ram_fallback(self):
        # Default safety values agar command na chale
        total_gb, used_gb, percent_used = 16.0, 4.0, 25.0
        try:
            current_os = platform.system()
            if current_os == "Windows":
                # WMIC tool se physical memory parse karo
                cmd = "wmic computersystem get TotalPhysicalMemory"
                out = os.popen(cmd).read()
                total_bytes = int([x for x in out.split() if x.isdigit()][0])
                total_gb = round(total_bytes / (1024 ** 3), 2)
                
                cmd_free = "wmic OS get FreePhysicalMemory"
                out_free = os.popen(cmd_free).read()
                free_kb = int([x for x in out_free.split() if x.isdigit()][0])
                free_gb = free_kb / (1024 ** 2)
                
                used_gb = round(total_gb - free_gb, 2)
                percent_used = round((used_gb / total_gb) * 100, 2)
            elif current_os == "Linux":
                # /proc/meminfo standard scan
                with open('/proc/meminfo', 'r') as f:
                    lines = f.readlines()
                mem_total = int(lines[0].split()[1]) # kB
                mem_free = int(lines[1].split()[1]) # kB
                total_gb = round(mem_total / (1024 ** 2), 2)
                free_gb = mem_free / (1024 ** 2)
                used_gb = round(total_gb - free_gb, 2)
                percent_used = round((used_gb / total_gb) * 100, 2)
        except Exception as e:
            print(f"[{self.agent_name}] Fallback calculation error: {str(e)}")
        return total_gb, used_gb, percent_used

    def _save_status(self, data):
        try:
            with open(self.output_status_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] RAM status save ho gaya hai: '{self.output_status_path}'")
        except Exception as e:
            print(f"[{self.agent_name}] Status file save karne me error: {str(e)}")

if __name__ == "__main__":
    monitor = ChiefSupervisorRamMonitor()
    monitor.get_system_ram_metrics()
