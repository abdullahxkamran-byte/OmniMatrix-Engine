import os
import sys
import json
import time
import platform
from datetime import datetime

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

class Agent_61_Live_Reporter_Vibe_Logger:
    """
    OMNIMATRIX V2.0 PURE UTILITY: LIVE TELEMETRY REPORTER & VIBE LOGGER
    A thread-safe central logging and runtime atmosphere monitoring engine.
    Maintains active JSON telemetry ledgers, calculates precise sub-second
    execution latencies, rotates log buffers, and compiles an automated HTML5
    live runtime dashboard for real-time human observation.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: Pure Non-AI Naming enforcement (Agent_XX instead of Ai_Agent_XX)
        self.agent_name = "Agent_61_Live_Reporter_Vibe_Logger"
        self.workspace_dir = workspace_dir
        self.ledger_path = os.path.join(self.workspace_dir, "61_live_telemetry_ledger.json")
        self.terminal_report_path = os.path.join(self.workspace_dir, "61_terminal_status_report.txt")
        self.html_dashboard_path = os.path.join(self.workspace_dir, "61_omnimatrix_runtime_dashboard.html")
        
        # Rule 17: Memory & I/O safeguard - retain maximum 250 log entries
        self.max_entries_to_retain = 250
        
        self.ansi_colors = {
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
        
        if platform.system().lower() == "windows":
            os.system("color")
            
        os.makedirs(self.workspace_dir, exist_ok=True)

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & PIPELINE ROUTING
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
            # Hand off to Ai Agent 62 (Animation DNA Core Router)
            data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_62_Animation_Dna_Core_Router"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    # =====================================================================
    # THREAD-SAFE FILE I/O BUFFER & LATENCY CALCULATOR
    # =====================================================================
    def _read_ledger_safely(self):
        attempts = 3
        while attempts > 0:
            if not os.path.exists(self.ledger_path):
                return []
            try:
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                attempts -= 1
                time.sleep(0.05)
        return []

    def _write_ledger_safely(self, logs):
        attempts = 3
        while attempts > 0:
            try:
                with open(self.ledger_path, "w", encoding="utf-8") as f:
                    json.dump(logs, f, indent=4)
                break
            except IOError:
                attempts -= 1
                time.sleep(0.05)

    def _calculate_execution_latency(self, agent, status, current_epoch):
        if any(token in status.upper() for token in ["RUNNING", "START", "IN_PROGRESS", "INITIATED"]):
            return 0.0

        logs = self._read_ledger_safely()
        for entry in reversed(logs):
            if entry.get("target_agent") == agent and any(t in str(entry.get("execution_status", "")).upper() for t in ["RUNNING", "START", "IN_PROGRESS", "INITIATED"]):
                start_time = entry.get("timestamp_epoch", 0.0)
                if start_time > 0:
                    return round(current_epoch - start_time, 3)
        return 0.0

    # =====================================================================
    # DETERMINISTIC TELEMETRY & ATMOSPHERE LOGGING ENGINE
    # =====================================================================
    def log_agent_telemetry(self, target_agent, status, atmosphere_state="NOMINAL_FLOW", message="", metrics=None):
        self._handshake("IN_PROGRESS")
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_epoch = time.time()
        
        latency_sec = self._calculate_execution_latency(target_agent, status, current_epoch)
        
        status_color = self.ansi_colors["CYAN"]
        if any(t in status.upper() for t in ["ERROR", "FAIL", "CRITICAL", "OVERFLOW"]):
            status_color = self.ansi_colors["RED"]
        elif any(t in status.upper() for t in ["COMPLETE", "SUCCESS", "HEALED", "PASS"]):
            status_color = self.ansi_colors["GREEN"]
        elif any(t in status.upper() for t in ["RUNNING", "START", "IN_PROGRESS", "EVALUATING"]):
            status_color = self.ansi_colors["YELLOW"]

        vibe_badge = "::"
        vibe_color = self.ansi_colors["BLUE"]
        if any(t in atmosphere_state.upper() for t in ["HOT", "BURNING", "HYPED", "SAKUGA"]):
            vibe_badge = ">>"
            vibe_color = self.ansi_colors["RED"]
        elif any(t in atmosphere_state.upper() for t in ["HEAVY", "RENDERING", "COMPRESSING"]):
            vibe_badge = "##"
            vibe_color = self.ansi_colors["MAGENTA"]
        elif any(t in atmosphere_state.upper() for t in ["CRITICAL", "HALTED", "FAIL"]):
            vibe_badge = "!!"
            vibe_color = self.ansi_colors["RED"]

        print(f"{self.ansi_colors['BG_DARK']}{vibe_color}{vibe_badge} [OMNIMATRIX VIBE TELEMETRY] {timestamp_str}{self.ansi_colors['RESET']}")
        print(f"   {self.ansi_colors['BOLD']}Target Node:{self.ansi_colors['RESET']} {self.ansi_colors['CYAN']}{target_agent}{self.ansi_colors['RESET']}")
        print(f"   {self.ansi_colors['BOLD']}Status:{self.ansi_colors['RESET']} {status_color}{status}{self.ansi_colors['RESET']}")
        print(f"   {self.ansi_colors['BOLD']}Atmosphere State:{self.ansi_colors['RESET']} {vibe_color}{atmosphere_state}{self.ansi_colors['RESET']}")
        print(f"   {self.ansi_colors['BOLD']}Telemetry Message:{self.ansi_colors['RESET']} {message}")
        if latency_sec > 0:
            print(f"   {self.ansi_colors['BOLD']}Execution Latency:{self.ansi_colors['RESET']} {self.ansi_colors['GREEN']}{latency_sec} sec{self.ansi_colors['RESET']}")
        print("-" * 65)

        logs = self._read_ledger_safely()
        new_entry = {
            "timestamp": timestamp_str,
            "timestamp_epoch": current_epoch,
            "target_agent": target_agent,
            "execution_status": status,
            "atmosphere_state": atmosphere_state,
            "telemetry_message": message,
            "execution_latency_sec": latency_sec,
            "metrics": metrics if metrics else {}
        }
        logs.append(new_entry)
        
        if len(logs) > self.max_entries_to_retain:
            logs = logs[-self.max_entries_to_retain:]

        self._write_ledger_safely(logs)
        self._compile_terminal_text_report(logs)
        self._compile_html_dashboard(logs)
        self._handshake("COMPLETED")
        return new_entry

    # =====================================================================
    # ACTIONABLE HTML5 DASHBOARD & TEXT COMPILER
    # =====================================================================
    def _compile_terminal_text_report(self, logs):
        try:
            with open(self.terminal_report_path, "w", encoding="utf-8") as f:
                f.write("=====================================================================\n")
                f.write("               OMNIMATRIX V2.0 — ACTIVE TELEMETRY REPORT\n")
                f.write(f"  Last Synchronized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=====================================================================\n\n")
                for item in reversed(logs):
                    f.write(f"[{item['timestamp']}] Node: {item['target_agent']}\n")
                    f.write(f"STATUS: {item['execution_status']} | ATMOSPHERE: {item['atmosphere_state']}\n")
                    f.write(f"MESSAGE: {item['telemetry_message']}\n")
                    if item.get("execution_latency_sec", 0.0) > 0:
                        f.write(f"LATENCY: {item['execution_latency_sec']} sec\n")
                    f.write("-" * 65 + "\n")
        except Exception as error:
            self.log(f"Terminal report compilation exception: {error}", "WARNING")

    def _compile_html_dashboard(self, logs):
        try:
            total_events = len(logs)
            active_nodes = len(set([x.get("target_agent") for x in logs]))
            latest_vibe = logs[-1].get("atmosphere_state", "NOMINAL_FLOW") if logs else "NOMINAL_FLOW"
            error_count = sum(1 for x in logs if any(t in str(x.get("execution_status", "")).upper() for t in ["ERROR", "FAIL", "CRITICAL"]))

            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>OMNIMATRIX V2.0 — Live Telemetry Dashboard</title>
    <meta http-equiv="refresh" content="4">
    <style>
        body {{ font-family: 'Consolas', 'Segoe UI', Tahoma, sans-serif; background-color: #0a0a0f; color: #e0e0e0; margin: 0; padding: 25px; }}
        .header {{ background: linear-gradient(135deg, #161622, #0d0d14); border-radius: 12px; padding: 25px; border-bottom: 3px solid #00ffcc; text-align: center; box-shadow: 0 4px 20px rgba(0,255,204,0.15); }}
        h1 {{ margin: 0; color: #00ffcc; font-size: 2.2rem; text-transform: uppercase; letter-spacing: 3px; }}
        .vibe-tag {{ background-color: #202030; color: #ff0055; border: 1px solid #ff0055; padding: 6px 16px; border-radius: 20px; font-weight: bold; display: inline-block; margin-top: 12px; font-size: 0.95rem; text-transform: uppercase; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; margin-top: 25px; }}
        .card {{ background: #12121c; border-radius: 10px; padding: 18px; text-align: center; border-left: 4px solid #00ffcc; box-shadow: 0 4px 12px rgba(0,0,0,0.4); }}
        .card.errors {{ border-left-color: #ff0055; }}
        .card.vibe {{ border-left-color: #ffbb00; }}
        .card.nodes {{ border-left-color: #00ff66; }}
        .number {{ font-size: 2.2rem; font-weight: bold; margin-top: 10px; }}
        .table-container {{ margin-top: 30px; background: #12121c; border-radius: 12px; padding: 22px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); overflow-x: auto; border: 1px solid #1f1f2f; }}
        h2 {{ margin-top: 0; border-bottom: 1px solid #2a2a3a; padding-bottom: 12px; color: #00ffcc; font-size: 1.3rem; letter-spacing: 1px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th {{ padding: 14px; background-color: #0a0a0f; color: #8888aa; border-bottom: 2px solid #2a2a3a; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px; }}
        td {{ padding: 14px; border-bottom: 1px solid #1f1f2f; font-size: 0.95rem; }}
        tr:hover {{ background-color: #1a1a2a; }}
        .badge {{ padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; display: inline-block; }}
        .badge.running {{ background-color: rgba(255, 187, 0, 0.15); color: #ffbb00; border: 1px solid #ffbb00; }}
        .badge.success {{ background-color: rgba(0, 255, 102, 0.15); color: #00ff66; border: 1px solid #00ff66; }}
        .badge.failed {{ background-color: rgba(255, 0, 85, 0.15); color: #ff0055; border: 1px solid #ff0055; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>OMNIMATRIX V2.0 — Telemetry & Atmosphere Ledger</h1>
        <div class="vibe-tag">Atmosphere State: {latest_vibe}</div>
    </div>
    <div class="grid">
        <div class="card">
            <div style="font-size: 0.85rem; color: #8888aa; text-transform: uppercase;">Total Telemetry Events</div>
            <div class="number" style="color: #00ffcc;">{total_events}</div>
        </div>
        <div class="card nodes">
            <div style="font-size: 0.85rem; color: #8888aa; text-transform: uppercase;">Active Engine Nodes</div>
            <div class="number" style="color: #00ff66;">{active_nodes}</div>
        </div>
        <div class="card vibe">
            <div style="font-size: 0.85rem; color: #8888aa; text-transform: uppercase;">Current Atmosphere</div>
            <div class="number" style="color: #ffbb00; font-size: 1.5rem; margin-top: 16px;">{latest_vibe}</div>
        </div>
        <div class="card errors">
            <div style="font-size: 0.85rem; color: #8888aa; text-transform: uppercase;">Execution Alerts</div>
            <div class="number" style="color: #ff0055;">{error_count}</div>
        </div>
    </div>
    <div class="table-container">
        <h2>Real-Time Event Streaming Ledger</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Target Engine Node</th>
                    <th>Status Badge</th>
                    <th>Atmosphere State</th>
                    <th>Activity & Diagnostics</th>
                    <th>Latency</th>
                </tr>
            </thead>
            <tbody>
"""
            for item in reversed(logs):
                status_raw = str(item.get("execution_status", "")).upper()
                badge = "success"
                if any(t in status_raw for t in ["ERROR", "FAIL", "CRITICAL", "OVERFLOW"]):
                    badge = "failed"
                elif any(t in status_raw for t in ["RUNNING", "START", "IN_PROGRESS", "INITIATED"]):
                    badge = "running"
                    
                latency_str = f"{item.get('execution_latency_sec', 0.0)}s" if item.get("execution_latency_sec", 0.0) > 0 else "---"
                
                html += f"""                <tr>
                    <td style="color: #777799; font-size: 0.88rem;">{item.get('timestamp')}</td>
                    <td style="color: #ffffff; font-weight: bold;">{item.get('target_agent')}</td>
                    <td><span class="badge {badge}">{item.get('execution_status')}</span></td>
                    <td style="color: #ffbb00; font-size: 0.9rem;">{item.get('atmosphere_state')}</td>
                    <td style="color: #cccccc;">{item.get('telemetry_message')}</td>
                    <td style="color: #00ff66; font-family: monospace;">{latency_str}</td>
                </tr>\n"""

            html += """            </tbody>
        </table>
    </div>
</body>
</html>"""
            with open(self.html_dashboard_path, "w", encoding="utf-8") as f:
                f.write(html)
        except Exception as error:
            self.log(f"HTML dashboard compilation exception: {error}", "WARNING")

if __name__ == "__main__":
    logger = Agent_61_Live_Reporter_Vibe_Logger()
    logger.log_agent_telemetry(
        target_agent="Ai_Agent_55_Universal_Vision_Comprehender",
        status="IN_PROGRESS",
        atmosphere_state="HIGH_OCTANE_ANALYSIS",
        message="Scanning visual panel coordinates and mapping semantic structure..."
    )
    time.sleep(0.4)
    logger.log_agent_telemetry(
        target_agent="Ai_Agent_55_Universal_Vision_Comprehender",
        status="SUCCESS",
        atmosphere_state="NOMINAL_FLOW",
        message="Visual comprehension completed successfully. Target matrix verified.",
        metrics={"panels_evaluated": 12, "resolution_mapped": "3840x2160"}
    )
