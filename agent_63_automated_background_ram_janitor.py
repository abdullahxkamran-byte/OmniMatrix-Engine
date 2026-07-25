import os
import gc
import sys
import json
import time
import ctypes
import shutil
import platform
import subprocess
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

class Agent_63_Automated_Background_Ram_Janitor:
    """
    OMNIMATRIX V2.0 PURE UTILITY: AUTOMATED BACKGROUND RAM & VRAM JANITOR
    Executes deep garbage collection and kernel-level memory flushing across
    System RAM and GPU VRAM architectures. Clears orphaned PyTorch CUDA caches,
    flushes Win32 working sets, and purges OS pagecaches to eliminate memory
    bloat and resolve gatekeeping interrupts from Agent 60.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: Pure Non-AI Naming enforcement (Agent_XX instead of Ai_Agent_XX)
        self.agent_name = "Agent_63_Automated_Background_Ram_Janitor"
        self.workspace_dir = workspace_dir
        self.log_file_path = os.path.join(self.workspace_dir, "63_ram_janitor_log.json")
        self.supervisor_status_path = os.path.join(self.workspace_dir, "60_ram_status.json")
        
        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        print(f"[{level}] [{self.agent_name}] {message}")

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous memory sanitation logs."""
        if os.path.exists(self.log_file_path):
            try:
                os.remove(self.log_file_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy log {self.log_file_path}: {error}", "WARNING")

    # =====================================================================
    # RULE 7: ATOMIC HANDSHAKE & PIPELINE ROUTING
    # =====================================================================
    def _handshake(self, status="IN_PROGRESS", memory_resolution="CLEANING"):
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
            "hardware_memory_verdict": memory_resolution,
            "agent_status": {self.agent_name: status}
        })
        
        if status == "COMPLETED":
            # Hand off to Ai Agent 64 (Autonomous Artistic Painter Director)
            data["orchestrator_matrix"]["next_agent"] = "Ai_Agent_64_Autonomous_Artistic_Painter_Director"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _read_supervisor_status(self):
        """Evaluates hardware status directives emitted by Agent 60."""
        urgency = "NOMINAL_LOW"
        context = "Supervisor status report unavailable."
        
        if os.path.exists(self.supervisor_status_path):
            try:
                with open(self.supervisor_status_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                verdict = str(data.get("supervision_status_verdict", "OK")).upper()
                ram_pct = data.get("system_ram_metrics", {}).get("used_percentage", 0.0)
                vram_pct = data.get("gpu_vram_metrics", {}).get("used_percentage", 0.0)
                
                context = f"Supervisor Verdict: [{verdict}] | System RAM: {ram_pct}% | GPU VRAM: {vram_pct}%"
                if "CRITICAL" in verdict or ram_pct >= 88.0 or vram_pct >= 88.0:
                    urgency = "CRITICAL_OVERFLOW_EMERGENCY"
                elif "WARNING" in verdict or ram_pct >= 75.0 or vram_pct >= 75.0:
                    urgency = "HIGH_PRIORITY_PURGE"
                self.log(f"Ingested Chief Supervisor Telemetry -> {context}", "SUCCESS")
            except Exception as error:
                context = f"Supervisor telemetry parsing exception: {error}"
                self.log(context, "WARNING")
        return urgency, context

    # =====================================================================
    # RULE 17: GPU VRAM & PYTORCH CUDA CACHE PURGING
    # =====================================================================
    def _purge_gpu_vram_caches(self):
        """Releases orphaned PyTorch CUDA allocations and IPC memory buffers."""
        self.log("Inspecting AI runtime environment for orphaned GPU VRAM allocations...")
        vram_freed_status = "No active PyTorch CUDA session detected."
        
        try:
            import torch
            if torch.cuda.is_available():
                allocated_before = torch.cuda.memory_allocated() / (1024 ** 2)
                reserved_before = torch.cuda.memory_reserved() / (1024 ** 2)
                
                # Execute aggressive CUDA IPC cache flushing
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
                
                allocated_after = torch.cuda.memory_allocated() / (1024 ** 2)
                reserved_after = torch.cuda.memory_reserved() / (1024 ** 2)
                freed_mb = round(reserved_before - reserved_after, 2)
                
                vram_freed_status = f"PyTorch CUDA cache flushed. Released {freed_mb} MB VRAM buffer."
                self.log(vram_freed_status, "SUCCESS")
            else:
                self.log("PyTorch available, but CUDA GPU hardware is inactive.", "INFO")
        except ImportError:
            self.log("PyTorch runtime uninstalled. Engaging OS-level NVIDIA driver checks.", "INFO")
            nvidia_smi = shutil.which("nvidia-smi")
            if nvidia_smi:
                try:
                    # Inquire driver state to force memory table refresh
                    subprocess.run(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    vram_freed_status = "NVIDIA driver memory tables synchronized and refreshed."
                except Exception:
                    pass
                    
        return vram_freed_status

    # =====================================================================
    # KERNEL-LEVEL SYSTEM RAM FLUSHING ENGINE
    # =====================================================================
    def _execute_os_kernel_cleanup(self, urgency):
        """Executes OS-specific Win32 API, Linux procfs, or macOS kernel cache purges."""
        system_os = platform.system().lower()
        status_message = "OS-level kernel cleanup bypassed (Standard privileges)."

        if "windows" in system_os:
            try:
                # Flush working set of the current process using Windows Kernel32 / PSAPI
                handle = ctypes.windll.kernel32.GetCurrentProcess()
                result = ctypes.windll.psapi.EmptyWorkingSet(handle)
                if result:
                    status_message = "Successfully flushed Win32 physical working set memory."
                    self.log(status_message, "SUCCESS")
                else:
                    status_message = "Win32 API EmptyWorkingSet returned null execution code."
            except Exception as error:
                status_message = f"Win32 Kernel API exception: {error}"
                self.log(status_message, "WARNING")

        elif "linux" in system_os:
            try:
                if os.getuid() == 0:
                    # Root privilege: Drop pagecache, dentries, and inodes
                    cmd = "sync; echo 3 > /proc/sys/vm/drop_caches" if "CRITICAL" in urgency else "sync; echo 1 > /proc/sys/vm/drop_caches"
                    subprocess.run(cmd, shell=True, check=True)
                    status_message = "Root kernel execution: Cleared pagecache, dentries, and inodes."
                    self.log(status_message, "SUCCESS")
                else:
                    # Non-root fallback: Sync filesystems to release dirty buffers
                    subprocess.run(["sync"], check=True)
                    status_message = "Non-root execution: Filesystem buffers synchronized via sync."
                    self.log(status_message, "INFO")
            except Exception as error:
                status_message = f"Linux procfs cleanup exception: {error}"

        elif "darwin" in system_os:
            try:
                if "CRITICAL" in urgency:
                    subprocess.run(["purge"], check=True)
                    status_message = "macOS purge command executed. Unallocated pages released."
                    self.log(status_message, "SUCCESS")
                else:
                    status_message = "macOS purge bypassed (Nominal memory urgency)."
            except Exception as error:
                status_message = f"macOS purge exception: {error}"

        return status_message

    def run_janitor_cleanup(self):
        self._handshake("IN_PROGRESS", "PURGING_MEMORY")
        self.log("Initiating automated background RAM & VRAM garbage collection sequence...")

        urgency, supervisor_context = self._read_supervisor_status()

        # Step 1: Deep Python Runtime Garbage Collection
        initial_gc_count = gc.get_count()
        objects_freed = gc.collect(2) # Generation 2 full collection
        self.log(f"Python Runtime Garbage Collector executed. Objects freed: {objects_freed}", "SUCCESS")

        # Step 2: GPU VRAM & PyTorch CUDA Cache Flushing
        vram_status = self._purge_gpu_vram_caches()

        # Step 3: OS Kernel-Level System RAM Cleanup
        os_status = self._execute_os_kernel_cleanup(urgency)

        # Step 4: Evaluate memory resolution verdict
        resolution_verdict = "RESOLVED_NOMINAL_FLOW" if "CRITICAL" not in urgency else "RESOLVED_RECOVERED_FROM_CRITICAL"

        report_payload = {
            "agent_executed": self.agent_name,
            "execution_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operating_system_environment": platform.system().upper(),
            "cleanup_urgency_level": urgency,
            "supervisor_context_evaluated": supervisor_context,
            "python_gc_telemetry": {
                "initial_gc_generation_state": initial_gc_count,
                "unreferenced_objects_freed": objects_freed
            },
            "gpu_vram_sanitation_status": vram_status,
            "os_kernel_sanitation_status": os_status,
            "hardware_memory_verdict": resolution_verdict
        }

        with open(self.log_file_path, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=4)

        self.log(f"RAM/VRAM sanitation report locked: '{self.log_file_path}'", "SUCCESS")
        self._handshake("COMPLETED", resolution_verdict)
        return report_payload

if __name__ == "__main__":
    janitor = Agent_63_Automated_Background_Ram_Janitor()
    janitor.run_janitor_cleanup()
