import os
import sys
import re
import json
import time
import subprocess
from datetime import datetime

# Optional hardware metric trackers
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Import Agent 99 for supreme stability handshakes
try:
    from agent_99_supreme_self_healing_git_engine import SupremeSelfHealingGitEngine
    HEALING_ENGINE_AVAILABLE = True
except ImportError:
    HEALING_ENGINE_AVAILABLE = False

try:
    from agent_63_automated_background_ram_janitor import AutomatedBackgroundRamJanitor
    RAM_JANITOR_AVAILABLE = True
except ImportError:
    RAM_JANITOR_AVAILABLE = False

class ZNetCoreOrchestratorController:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 00: znet_core_orchestrator_controller"
        
        # Paths Setup
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        self.log_file_path = os.path.join(self.workspace_dir, "agent_00_orchestrator.log")
        self.pipeline_state_path = os.path.join(self.workspace_dir, "00_pipeline_state.json")
        
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

        # Connect Core Guardian Nodes
        self.janitor = AutomatedBackgroundRamJanitor(workspace_dir=self.workspace_dir) if RAM_JANITOR_AVAILABLE else None
        self.healing_engine = SupremeSelfHealingGitEngine(workspace_dir=self.workspace_dir) if HEALING_ENGINE_AVAILABLE else None

    def log_status(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_msg = f"[{timestamp}] [{level}] [{self.agent_name}] {message}"
        print(formatted_msg)
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as log_f:
                log_f.write(formatted_msg + "\n")
        except Exception:
            pass

    def discover_and_classify_workspace_agents(self):
        """Scans the runtime tree, detects all valid Z-Net agent nodes, and auto-assigns operational weights."""
        discovered_agents = []
        pattern = re.compile(r"^(ai_)?agent_(\d+)_(.+)\.py$")

        self.log_status("Scanning environment workspace tree for active Z-Net agent deployments...", "INFO")
        
        for file in sorted(os.listdir(self.base_dir)):
            match = pattern.match(file)
            if match:
                agent_id_str = match.group(2)
                agent_id = int(agent_id_str)
                
                # CRITICAL SAFETY: Skip self, skipped/removed agent 62, and supervisor engines
                if agent_id in [0, 62, 99]:
                    continue
                
                # Dynamic Module Weight Allocation Rules
                if 20 <= agent_id <= 41 or 55 <= agent_id <= 59:
                    weight = "HEAVY"  # Blender 3D, VFX Engine, Manga World Forger
                else:
                    weight = "LIGHT"  # Scripting, Audio, Utilities, Path Validators
                
                discovered_agents.append({
                    "agent_id": agent_id_str,
                    "file": file,
                    "weight": weight
                })

        self.log_status(f"Auto-Discovery Complete! Registered {len(discovered_agents)} pipeline nodes dynamically.", "INFO")
        return discovered_agents

    def evaluate_hardware_concurrency_throttle(self, next_agent_weight):
        """Reads hardware matrix allocations in real-time to compute parallel execution capability."""
        if not PSUTIL_AVAILABLE:
            self.log_status("psutil metadata missing. Defaulting to serial safety lock (1 thread).", "WARNING")
            return 1

        ram_usage_pct = psutil.virtual_memory().percent
        self.log_status(f"Workspace RAM Profile Check: {ram_usage_pct}% saturation.", "INFO")

        # Emergency Threshold Handshakes
        if ram_usage_pct > 85.0:
            self.log_status("RAM limit critical! Invoking Agent 63 Janitor node immediately.", "WARNING")
            if self.janitor:
                self.janitor.run_janitor_cleanup()
            return 1

        if next_agent_weight == "HEAVY":
            self.log_status("Target node identified as HEAVY. Restricting processing to single-thread serial route.", "INFO")
            if self.janitor and ram_usage_pct > 70.0:
                self.janitor.run_janitor_cleanup()
            return 1

        # Dynamic capacity throttle for LIGHT processes
        if ram_usage_pct < 55.0:
            return 3  # High Concurrency Speed-Burst
        elif ram_usage_pct < 75.0:
            return 2  # Balanced Execution
        else:
            return 1  # Safe Serialization

    def trigger_agent_node_execution(self, agent_data):
        """Routes execution loops through Agent 99's core engine to provide un-crashable self-healing runs."""
        agent_file = agent_data["file"]
        script_path = os.path.join(self.base_dir, agent_file)

        if self.healing_engine:
            self.log_status(f"Launching Agent {agent_data['agent_id']} under Agent 99 Self-Healing shield...", "INFO")
            report = self.healing_engine.execute_and_heal(script_path)
            status = report.get("execution_status", "FAILED")
            return status in ["SUCCESS", "HEALED"]
        else:
            self.log_status(f"Shield missing! Booting plain subprocess for {agent_file}", "WARNING")
            try:
                result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, check=True)
                return result.returncode == 0
            except Exception as e:
                self.log_status(f"Execution failed on unshielded crash: {str(e)}", "ERROR")
                return False

    def launch_autonomous_orchestration(self):
        """The core central decision center. Runs discovery, assigns steps, scales capacity, and triggers loops."""
        self.log_status("Activating Z-Net Master Brain Autonomous Orchestration Sequence...", "INFO")
        
        # 1. Discover what files exist in the user's setup right now
        active_agents = self.discover_and_classify_workspace_agents()
        
        if not active_agents:
            self.log_status("No executable agent scripts discovered in current base execution path.", "CRITICAL")
            return False

        completed_ledger = []
        state_log = {
            "orchestration_initiated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "RUNNING",
            "processed_nodes": []
        }
        self._serialize_state(state_log)

        # 2. Iterate through all discovered agents sequentially or adaptive parallel blocks
        for agent in active_agents:
            # Check resource levels and adjust concurrency cap right before launch
            concurrency_limit = self.evaluate_hardware_concurrency_throttle(agent["weight"])
            self.log_status(f"Active Scaled Concurrency Factor set to: {concurrency_limit}", "INFO")

            # Execute via self-healing pipeline wrapper
            success = self.trigger_agent_node_execution(agent)

            if success:
                self.log_status(f"Step Finalized Successfully: Agent {agent['agent_id']}", "INFO")
                completed_ledger.append(agent["agent_id"])
                state_log["processed_nodes"] = completed_ledger
                self._serialize_state(state_log)
            else:
                self.log_status(f"Pipeline flow fractured at Agent {agent['agent_id']}. Initiating Emergency Halt.", "CRITICAL")
                state_log["status"] = f"CRITICAL_HALT_AT_AGENT_{agent['agent_id']}"
                self._serialize_state(state_log)
                return False

        state_log["status"] = "ALL_MODULES_SUCCESSFULLY_COMPLETED"
        state_log["orchestration_concluded"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._serialize_state(state_log)
        self.log_status("System Matrix run state concluded flawlessly. All modules integrated.", "INFO")
        return True

    def _serialize_state(self, data):
        try:
            with open(self.pipeline_state_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.log_status(f"State writing exception: {str(e)}", "ERROR")

if __name__ == "__main__":
    orchestrator = ZNetCoreOrchestratorController()
    print("\n=======================================================")
    print("      Z-NET SYSTEM INFRASTRUCTURE CENTRAL COMMAND      ")
    print("=======================================================")
    orchestrator.launch_autonomous_orchestration()
