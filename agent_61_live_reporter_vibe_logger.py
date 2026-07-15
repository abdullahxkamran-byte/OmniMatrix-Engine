import os
import sys
import json
import time
from datetime import datetime

class LiveReporterVibeLogger:
    """
    Agent 61: live_reporter_vibe_logger
    
    A robust, thread-safe central logging and vibe-reporting system.
    Maintains active telemetry logs, calculates execution latencies, rotates log files,
    and generates an automated HTML runtime dashboard for real-time human observation.
    """
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 61: live_reporter_vibe_logger"
        self.workspace_dir = workspace_dir
        self.log_file_path = os.path.join(self.workspace_dir, "61_live_vibe_log.json")
        self.readable_txt_path = os.path.join(self.workspace_dir, "vibe_terminal_report.txt")
        self.html_dashboard_path = os.path.join(self.workspace_dir, "61_live_dashboard.html")
        
        self.max_entries_to_keep = 200
        self.colors = {
            "RESET": "\033[0m",
            "CYAN": "\033[36m",
            "GREEN": "\033[32m",
            "YELLOW": "\033[33m",
            "RED": "\033[31m",
            "MAGENTA": "\033[35m",
            "BOLD": "\033[1m",
            "BG_DARK": "\033[40m",
            "BLUE": "\033[34m"
        }
        
        if os.name == 'nt':
            os.system('color')
            
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def log_agent_status(self, target_agent, status, system_vibe="CHILL", message="", extra_metrics=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_epoch = time.time()
        
        elapsed_seconds = self._calculate_latency(target_agent, status, timestamp_epoch)
        
        status_color = self.colors["CYAN"]
        if "ERROR" in status.upper() or "FAIL" in status.upper() or "CRITICAL" in status.upper():
            status_color = self.colors["RED"]
        elif "COMPLETE" in status.upper() or "SUCCESS" in status.upper() or "HEALED" in status.upper():
            status_color = self.colors["GREEN"]
        elif "RUNNING" in status.upper() or "START" in status.upper():
            status_color = self.colors["YELLOW"]

        vibe_emoji = "::"
        vibe_color = self.colors["BLUE"]
        if "HOT" in system_vibe.upper() or "BURNING" in system_vibe.upper():
            vibe_emoji = ">>"
            vibe_color = self.colors["RED"]
        elif "HEAVY" in system_vibe.upper() or "RENDERING" in system_vibe.upper():
            vibe_emoji = "##"
            vibe_color = self.colors["MAGENTA"]
        elif "CRITICAL" in system_vibe.upper():
            vibe_emoji = "!!"
            vibe_color = self.colors["RED"]

        print(f"{self.colors['BG_DARK']}{vibe_color}{vibe_emoji} [Z-NET RUNTIME VIBE MONITOR] {timestamp}{self.colors['RESET']}")
        print(f"   {self.colors['BOLD']}Agent:{self.colors['RESET']} {self.colors['CYAN']}{target_agent}{self.colors['RESET']}")
        print(f"   {self.colors['BOLD']}Status:{self.colors['RESET']} {status_color}{status}{self.colors['RESET']}")
        print(f"   {self.colors['BOLD']}Current Vibe:{self.colors['RESET']} {vibe_color}{system_vibe}{self.colors['RESET']}")
        print(f"   {self.colors['BOLD']}Message:{self.colors['RESET']} {message}")
        if elapsed_seconds > 0:
            print(f"   {self.colors['BOLD']}Elapsed Latency:{self.colors['RESET']} {self.colors['GREEN']}{elapsed_seconds:.3f} seconds{self.colors['RESET']}")
        print("-" * 60)

        logs = self._read_logs_safely()
        
        new_entry = {
            "timestamp": timestamp,
            "timestamp_epoch": timestamp_epoch,
            "agent": target_agent,
            "status": status,
            "vibe": system_vibe,
            "message": message,
            "elapsed_seconds": elapsed_seconds,
            "extra_metrics": extra_metrics if extra_metrics else {}
        }
        logs.append(new_entry)
        
        if len(logs) > self.max_entries_to_keep:
            logs = logs[-self.max_entries_to_keep:]

        self._write_logs_safely(logs)
        self._generate_readable_text_report(logs)
        self._generate_html_dashboard(logs)

        return new_entry

    def _calculate_latency(self, agent, status, current_epoch):
        if "RUNNING" in status.upper() or "START" in status.upper():
            return 0.0

        logs = self._read_logs_safely()
        for entry in reversed(logs):
            if entry.get("agent") == agent and ("RUNNING" in entry.get("status", "").upper() or "START" in entry.get("status", "").upper()):
                start_time = entry.get("timestamp_epoch", 0.0)
                if start_time > 0:
                    return current_epoch - start_time
        return 0.0

    def _read_logs_safely(self):
        attempts = 3
        while attempts > 0:
            if not os.path.exists(self.log_file_path):
                return []
            try:
                with open(self.log_file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                attempts -= 1
                time.sleep(0.1)
        return []

    def _write_logs_safely(self, logs):
        attempts = 3
        while attempts > 0:
            try:
                with open(self.log_file_path, "w", encoding="utf-8") as f:
                    json.dump(logs, f, indent=4)
                break
            except IOError:
                attempts -= 1
                time.sleep(0.1)

    def _generate_readable_text_report(self, logs):
        try:
            with open(self.readable_txt_path, "w", encoding="utf-8") as f:
                f.write("============================================================\n")
                f.write("               Z-NET PIPELINE ACTIVE REPORT\n")
                f.write(f"  Last Sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("============================================================\n\n")
                for item in reversed(logs):
                    f.write(f"[{item['timestamp']}] Agent: {item['agent']}\n")
                    f.write(f"STATUS: {item['status']} | VIBE: {item['vibe']}\n")
                    f.write(f"MESSAGE: {item['message']}\n")
                    if item.get('elapsed_seconds', 0.0) > 0:
                        f.write(f"LATENCY: {item['elapsed_seconds']:.2f} sec\n")
                    f.write("-" * 50 + "\n")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing text report: {str(e)}")

    def _generate_html_dashboard(self, logs):
        try:
            total_logs = len(logs)
            unique_agents = len(set([x.get("agent") for x in logs]))
            latest_vibe = logs[-1].get("vibe", "CHILL") if logs else "CHILL"
            errors_count = sum(1 for x in logs if "ERROR" in x.get("status", "").upper() or "FAIL" in x.get("status", "").upper())

            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Z-Net Live Vibe Dashboard</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #1e1e2e, #11111b); border-radius: 12px; padding: 25px; border-bottom: 3px solid #ff4a5a; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        h1 {{ margin: 0; color: #ff4a5a; font-size: 2.2rem; text-transform: uppercase; letter-spacing: 2px; }}
        .vibe-tag {{ background-color: #cba6f7; color: #11111b; padding: 4px 12px; border-radius: 20px; font-weight: bold; display: inline-block; margin-top: 10px; font-size: 0.9rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-top: 25px; }}
        .card {{ background: #181825; border-radius: 10px; padding: 15px; text-align: center; border-left: 5px solid #89b4fa; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }}
        .card.errors {{ border-left-color: #f38ba8; }}
        .card.vibe {{ border-left-color: #fab387; }}
        .number {{ font-size: 2rem; font-weight: bold; margin-top: 10px; }}
        .table-container {{ margin-top: 30px; background: #181825; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); overflow-x: auto; }}
        h2 {{ margin-top: 0; border-bottom: 1px solid #313244; padding-bottom: 10px; color: #f5c2e7; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th {{ padding: 12px; background-color: #11111b; color: #cdd6f4; border-bottom: 2px solid #313244; }}
        td {{ padding: 12px; border-bottom: 1px solid #313244; font-size: 0.95rem; }}
        tr:hover {{ background-color: #313244; }}
        .status-badge {{ padding: 4px 8px; border-radius: 5px; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; }}
        .status-badge.running {{ background-color: #f9e2af; color: #11111b; }}
        .status-badge.success {{ background-color: #a6e3a1; color: #11111b; }}
        .status-badge.failed {{ background-color: #f38ba8; color: #11111b; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Z-Net Engine Telemetry Dashboard</h1>
        <div class="vibe-tag">System Vibe State: {latest_vibe}</div>
    </div>
    
    <div class="grid">
        <div class="card">
            <div style="font-size: 0.9rem; color: #a6adc8;">Total Log Entries</div>
            <div class="number" style="color: #89b4fa;">{total_logs}</div>
        </div>
        <div class="card">
            <div style="font-size: 0.9rem; color: #a6adc8;">Active Engine Agents</div>
            <div class="number" style="color: #b4befe;">{unique_agents}</div>
        </div>
        <div class="card vibe">
            <div style="font-size: 0.9rem; color: #a6adc8;">System Atmosphere</div>
            <div class="number" style="color: #fab387;">{latest_vibe}</div>
        </div>
        <div class="card errors">
            <div style="font-size: 0.9rem; color: #a6adc8;">Logged Issues</div>
            <div class="number" style="color: #f38ba8;">{errors_count}</div>
        </div>
    </div>

    <div class="table-container">
        <h2>Live Event Streaming Ledger</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Agent Identity</th>
                    <th>Execution Status</th>
                    <th>Vibe Action</th>
                    <th>Activity Details</th>
                    <th>Duration (sec)</th>
                </tr>
            </thead>
            <tbody>
"""
            for entry in reversed(logs):
                status_raw = entry.get('status', '').upper()
                badge_class = "success"
                if "ERROR" in status_raw or "FAIL" in status_raw or "CRITICAL" in status_raw:
                    badge_class = "failed"
                elif "RUNNING" in status_raw or "START" in status_raw:
                    badge_class = "running"
                    
                elapsed = f"{entry.get('elapsed_seconds', 0.0):.2f}" if entry.get('elapsed_seconds', 0.0) > 0 else "N/A"
                
                html_content += f"""                <tr>
                    <td style="color: #a6adc8;">{entry.get('timestamp')}</td>
                    <td style="color: #89dceb; font-weight: bold;">{entry.get('agent')}</td>
                    <td><span class="status-badge {badge_class}">{entry.get('status')}</span></td>
                    <td style="color: #f5e0dc;">{entry.get('vibe')}</td>
                    <td style="color: #cdd6f4;">{entry.get('message')}</td>
                    <td style="color: #a6e3a1; font-weight: bold;">{elapsed}</td>
                </tr>\n"""

            html_content += """            </tbody>
        </table>
    </div>
</body>
</html>
"""
            with open(self.html_dashboard_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            print(f"[{self.agent_name}] Error during dynamic HTML generation: {str(e)}")

if __name__ == "__main__":
    logger = LiveReporterVibeLogger()
    logger.log_agent_status(
        target_agent="Agent 55: manga_panel_vision_comprehender_colorizer",
        status="RUNNING",
        system_vibe="BURNING_HOT_ACTION",
        message="Manga Panels scan karna shuru kar diya hai... Processing Panel #1"
    )
    time.sleep(1.0)
    logger.log_agent_status(
        target_agent="Agent 55: manga_panel_vision_comprehender_colorizer",
        status="COMPLETED",
        system_vibe="BURNING_HOT_ACTION",
        message="Manga Panel scan safaltapurvak complete ho gaya hai! JSON profile generated.",
        extra_metrics={"panels_processed": 1, "image_dimensions": [1080, 1920]}
    )
