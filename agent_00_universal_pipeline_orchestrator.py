import os
import sys
import json
import re
import time
import glob
import subprocess
import threading
import psutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# =====================================================================
# RULE 2 & 14: UNIVERSAL PATH ISOLATION & DUAL-CASE ENV LOADING
# =====================================================================
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key_str = key.strip()
                    val_str = val.strip().strip('"').strip("'")
                    os.environ[key_str.upper()] = val_str
                    os.environ[key_str.lower()] = val_str

load_env_file()

class Agent_00_Universal_Pipeline_Orchestrator:
    """
    OMNIMATRIX V2.0 GOD-LEVEL AGENT 00 — UNIVERSAL PIPELINE ORCHESTRATOR
    
    Architecture:
    1. Reads 68_master_task_manifest.json to get dynamic Active vs Skipped decision matrix.
    2. Runs Module A (Scripting 01-08) and Agent 68 (Task Architect).
    3. Triggers Parallel Execution Branch A (Module B Audio 09-19) AND Branch B (Module H 3D Vision 55-59).
    4. Enforces Synchronization Barrier (Waits for B and H to conclude).
    5. Dispatches post-sync stages sequentially: Module C (Blender 3D 20-34), Module D (VFX 35-41), 
       Module E (FFmpeg 42-45), Module F (RIFE 46-48), Module G (Assets 49-54).
    6. Monitored by Agent 60 (RAM Monitor) & Agent 99 (Git Guardian).
    """

    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        self.agent_name = "agent_00_universal_pipeline_orchestrator"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        os.makedirs(self.workspace_dir, exist_ok=True)

        # State Paths
        self.manifest_file = os.path.join(self.workspace_dir, "68_master_task_manifest.json")
        self.state_file = os.path.join(self.workspace_dir, "00_master_pipeline_state.json")
        self.ledger_file = os.path.join(self.workspace_dir, "matrix_state.json")
        self.guardian_script = os.path.join(self.base_dir, "ai_agent_99_evolving_git_sync_optimizer.py")

        self.execution_ledger = []
        self.lock = threading.Lock()

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] [{self.agent_name}] {message}")

    def _get_telemetry(self):
        try:
            mem = psutil.virtual_memory()
            return f"RAM: {mem.percent}% used | Avail: {mem.available / (1024**2):.1f} MB"
        except Exception:
            return "Telemetry Active"

    # =====================================================================
    # DISCOVER AGENTS FROM DISK (REGEX MATCHING)
    # =====================================================================
    def _find_agent_script(self, target_num_str):
        all_files = os.listdir(self.base_dir)
        for f in all_files:
            if f.endswith(".py") and ("agent_" in f or "ai_agent_" in f):
                if "agent_00" in f or "agent_99" in f:
                    continue
                match = re.search(r'agent_(\d+(?:_\d+)?)(?:_|\.py)', f, re.IGNORECASE)
                if match and match.group(1) == target_num_str:
                    return f
        return None

    # =====================================================================
    # SUBPROCESS WORKER EXECUTION WITH GUARDIAN FALLBACK
    # =====================================================================
    def _run_agent_script(self, script_name, agent_id):
        script_path = os.path.join(self.base_dir, script_name)
        self.log(f"Spawning Subprocess Node [{agent_id}] -> '{script_name}'")
        self.log(f"Telemetry: {self._get_telemetry()}")

        if os.path.exists(self.guardian_script):
            cmd = [sys.executable, self.guardian_script, script_path]
        else:
            cmd = [sys.executable, script_path]

        try:
            res = subprocess.run(cmd, capture_output=False, text=True, timeout=1200)
            if res.returncode == 0:
                self.log(f"SUCCESS: Agent [{agent_id}] ({script_name}) executed cleanly.", "SUCCESS")
                with self.lock:
                    self.execution_ledger.append(script_name)
                return True
            else:
                self.log(f"ERROR: Agent [{agent_id}] failed with return code {res.returncode}.", "ERROR")
                return False
        except subprocess.TimeoutExpired:
            self.log(f"TIMEOUT: Agent [{agent_id}] exceeded 20-minute execution cap.", "ERROR")
            return False
        except Exception as e:
            self.log(f"EXCEPTION: Failure executing Agent [{agent_id}]: {e}", "ERROR")
            return False

    # =====================================================================
    # TASK MANIFEST EVALUATOR
    # =====================================================================
    def _is_agent_active(self, agent_id, manifest_matrix):
        if not manifest_matrix:
            return True
        agent_info = manifest_matrix.get(agent_id, manifest_matrix.get(str(int(agent_id)) if agent_id.isdigit() else agent_id, {}))
        status = agent_info.get("status", "ACTIVE")
        if status == "SKIPPED":
            reason = agent_info.get("reason", "Disabled by task architect")
            self.log(f"SKIPPING Agent [{agent_id}]: {reason}", "INFO")
            return False
        return True

    def _execute_agent_range(self, start_num, end_num, manifest_matrix):
        for num in range(start_num, end_num + 1):
            agent_id = f"{num:02d}"
            if not self._is_agent_active(agent_id, manifest_matrix):
                continue
            script_name = self._find_agent_script(agent_id)
            if script_name:
                success = self._run_agent_script(script_name, agent_id)
                if not success:
                    self.log(f"Pipeline halt requested due to node [{agent_id}] failure.", "ERROR")
                    return False
            else:
                self.log(f"Script for Agent [{agent_id}] not found on disk. Skipping...", "WARNING")
        return True

    # =====================================================================
    # MAIN ORCHESTRATION PIPELINE
    # =====================================================================
    def execute(self):
        self.log("=====================================================================")
        self.log("ACTIVATING OMNIMATRIX V2.0 UNIVERSAL PIPELINE ORCHESTRATOR")
        self.log("=====================================================================")

        # 1. Execute Module A (Scripting & Core Concept: Agents 01 to 08)
        self.log("--- STAGE 1: MODULE A (CORE CONCEPT & SCRIPTING 01-08) ---")
        if not self._execute_agent_range(1, 8, None):
            self.log("Module A execution failed. Halting pipeline.", "CRITICAL")
            return

        # 2. Execute Agent 68 (Dynamic Task Architect) to refresh manifest
        self.log("--- STAGE 2: DYNAMIC TASK BLUEPRINTING (AGENT 68) ---")
        script_68 = self._find_agent_script("68")
        if script_68:
            self._run_agent_script(script_68, "68")

        # Read compiled manifest
        manifest_matrix = {}
        if os.path.exists(self.manifest_file):
            try:
                with open(self.manifest_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    manifest_matrix = data.get("task_matrix", {})
                    self.log(f"Master Task Manifest successfully loaded ({len(manifest_matrix)} nodes evaluated).")
            except Exception as e:
                self.log(f"Failed to read task manifest: {e}. Defaulting to full active execution.", "WARNING")

        # 3. Parallel Execution: Module B (Audio 09-19) & Module H (Generative Vision/3D 55-59)
        self.log("--- STAGE 3: ASYNCHRONOUS PARALLEL DISPATCH (MODULE B & MODULE H) ---")
        
        def run_module_b():
            self.log("Starting Branch B1: Module B (Audio Commandos 09-19)...")
            self._execute_agent_range(9, 19, manifest_matrix)

        def run_module_h():
            self.log("Starting Branch B2: Module H (Omni Generative Matrix 55-59)...")
            self._execute_agent_range(55, 59, manifest_matrix)

        with ThreadPoolExecutor(max_workers=2) as executor:
            future_b = executor.submit(run_module_b)
            future_h = executor.submit(run_module_h)
            
            # Wait for parallel execution to finish (Sync Barrier)
            future_b.result()
            future_h.result()

        self.log("SYNCHRONIZATION BARRIER CLEARED: Both Module B (Audio) and Module H (3D Assets) completed.")

        # 4. Execute Module C (Blender 3D Heavy Infantry: Agents 20 to 34)
        self.log("--- STAGE 4: MODULE C (BLENDER 3D HEAVY INFANTRY 20-34) ---")
        if not self._execute_agent_range(20, 34, manifest_matrix):
            self.log("Module C execution failed. Halting pipeline.", "CRITICAL")
            return

        # 5. Execute Module D (VFX Studio & Compositing: Agents 35 to 41)
        self.log("--- STAGE 5: MODULE D (VFX STUDIO & COMPOSITING 35-41) ---")
        if not self._execute_agent_range(35, 41, manifest_matrix):
            self.log("Module D execution failed. Halting pipeline.", "CRITICAL")
            return

        # 6. Execute Module E (FFmpeg Video Assembler: Agents 42 to 45)
        self.log("--- STAGE 6: MODULE E (FFMPEG VIDEO ASSEMBLER 42-45) ---")
        if not self._execute_agent_range(42, 45, manifest_matrix):
            self.log("Module E execution failed. Halting pipeline.", "CRITICAL")
            return

        # 7. Execute Module F (Local AI Smoothness Matrix: Agents 46 to 48)
        self.log("--- STAGE 7: MODULE F (LOCAL AI SMOOTHNESS MATRIX 46-48) ---")
        if not self._execute_agent_range(46, 48, manifest_matrix):
            self.log("Module F execution failed. Halting pipeline.", "CRITICAL")
            return

        # 8. Execute Module G (Asset Management & Presentation: Agents 49 to 54)
        self.log("--- STAGE 8: MODULE G (ASSET MANAGEMENT & PRESENTATION 49-54) ---")
        self._execute_agent_range(49, 54, manifest_matrix)

        # Final State Update
        state_payload = {
            "orchestrator_status": "COMPLETED",
            "timestamp": time.time(),
            "execution_ledger": self.execution_ledger,
            "telemetry_at_conclusion": self._get_telemetry()
        }
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state_payload, f, indent=4)

        self.log("=====================================================================")
        self.log("ALL PIPELINE MODULES & STAGES CONCLUDED SUCCESSFULLY!")
        self.log("=====================================================================\n")

if __name__ == "__main__":
    orchestrator = Agent_00_Universal_Pipeline_Orchestrator()
    orchestrator.execute()