import os
import re
import sys
import ast
import json
import time
import shutil
import platform
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

# Attempt importing Google Gemini SDK for deep code evolution
try:
    import google.generativeai as genai
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False

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

class Ai_Agent_99_Evolving_Git_Sync_Optimizer:
    """
    OMNIMATRIX V2.0 GOD-LEVEL EVOLVING GIT SYNC & AUTO-HEALING ENGINE
    Acts as the autonomous cloud guardian and code stability sentinel.
    Monitors runtime execution tracebacks, deploys a 2-Layer AST syntax shield,
    executes quad-core AI debuggers, auto-injects missing dependencies, and
    pushes stable, self-healed production releases to remote GitHub repositories.
    """
    def __init__(self, workspace_dir="OmniMatrix_Workspace"):
        # Rule 8: AI vs Non-AI Naming enforcement
        self.agent_name = "Ai_Agent_99_Evolving_Git_Sync_Optimizer"
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        self.log_file_path = os.path.join(self.workspace_dir, "99_execution_telemetry.log")
        self.report_path = os.path.join(self.workspace_dir, "99_healing_and_sync_manifest.json")
        
        # Cloud and Repository Credentials
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_key = os.environ.get("OPENAI_API_KEY", None)
        self.github_token = os.environ.get("GITHUB_TOKEN", "")
        self.github_repo = os.environ.get("GITHUB_REPO", "")
        self.github_branch = os.environ.get("GITHUB_BRANCH", "main")
        
        if GEMINI_SDK_AVAILABLE and self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"

        os.makedirs(self.workspace_dir, exist_ok=True)
        self._scrub_legacy_assets()

    def log(self, message, level="INFO"):
        formatted = f"[{level}] [{self.agent_name}] {message}"
        print(formatted)
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")
        except Exception:
            pass

    def _scrub_legacy_assets(self):
        """Rule 3: Idempotency scrubbing of previous healing manifests."""
        if os.path.exists(self.report_path):
            try:
                os.remove(self.report_path)
            except Exception as error:
                self.log(f"Failed to scrub legacy manifest {self.report_path}: {error}", "WARNING")

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
            # Hand off to Agent 00 (Universal Pipeline Orchestrator - Master Traffic Boss)
            data["orchestrator_matrix"]["next_agent"] = "Agent_00_Universal_Pipeline_Orchestrator"
            
        try:
            with open(matrix_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            self.log(f"Atomic handshake synchronization failure: {error}", "ERROR")

    def _run_shell_command(self, cmd_list):
        try:
            result = subprocess.run(cmd_list, cwd=self.base_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as error:
            return False, error.stderr.strip() if error.stderr else str(error)

    # =====================================================================
    # 2-LAYER SAFETY SHIELD & AST VERIFICATION ENGINE
    # =====================================================================
    def create_backup(self, target_file_path):
        if not os.path.exists(target_file_path):
            return False
        backup_path = target_file_path + ".bak"
        try:
            shutil.copy2(target_file_path, backup_path)
            self.log(f"Layer 1 Shield Active: Physical backup compiled at '{backup_path}'", "SUCCESS")
            return True
        except Exception as error:
            self.log(f"Physical backup creation failure: {error}", "ERROR")
            return False

    def restore_backup(self, target_file_path):
        backup_path = target_file_path + ".bak"
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, target_file_path)
            self.log("Rollback Executed: Reverted script architecture back to verified stable state.", "WARNING")
            return True
        return False

    def verify_syntax(self, code_string):
        try:
            ast.parse(code_string)
            self.log("Layer 2 Shield Active: AST compiler verification passed (0 syntax bugs).", "SUCCESS")
            return True
        except SyntaxError as error:
            self.log(f"Layer 2 Shield Blocked: AST compiler exception detected: {error}", "ERROR")
            return False

    def _clean_code(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```python\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned

    def _save_report(self, report_data):
        try:
            with open(self.report_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=4)
            self.log(f"Execution telemetry manifest locked: '{self.report_path}'", "SUCCESS")
        except Exception as error:
            self.log(f"Failed to write healing manifest: {error}", "ERROR")

    # =====================================================================
    # AUTONOMOUS GITHUB CLOUD SYNCHRONIZATION ENGINE
    # =====================================================================
    def push_to_github(self, commit_msg):
        if not self.github_token or not self.github_repo:
            self.log("GitHub credentials absent from environment. Bypassing cloud synchronization.", "WARNING")
            return False

        self.log("Staging and committing verified production releases...", "INFO")
        self._run_shell_command(["git", "add", "."])
        
        success, commit_out = self._run_shell_command(["git", "commit", "-m", commit_msg])
        if not success:
            self.log(f"Commit bypassed (Repository already synchronized): {commit_out}", "INFO")
            return False

        auth_url = f"https://{self.github_token}@github.com/{self.github_repo}.git"
        self._run_shell_command(["git", "remote", "remove", "origin"])
        self._run_shell_command(["git", "remote", "add", "origin", auth_url])

        self.log(f"Pushing stable release to remote branch '{self.github_branch}'...", "INFO")
        push_success, push_out = self._run_shell_command(["git", "push", "-u", "origin", self.github_branch])
        
        self._run_shell_command(["git", "remote", "set-url", "origin", f"[https://github.com/](https://github.com/){self.github_repo}.git"])

        if push_success:
            self.log("Autonomous GitHub synchronization completed successfully!", "SUCCESS")
            return True
        else:
            self.log(f"Remote cloud push exception: {push_out}", "ERROR")
            return False

    # =====================================================================
    # RULE 10: PROCEDURAL REGEX ALCHEMIST (OFFLINE FALLBACK)
    # =====================================================================
    def _execute_procedural_fallback(self, broken_code, error_log, script_path):
        action = {"patched": False, "engine": "Procedural Regex Alchemist", "message": ""}
        
        module_match = re.search(r"ModuleNotFoundError: No module named '([\w\d_-]+)'", error_log)
        if module_match:
            missing_pkg = module_match.group(1)
            self.log(f"Identified absent package '{missing_pkg}'. Engaging automated pip installation...", "WARNING")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", missing_pkg], check=True)
                action["patched"] = True
                action["message"] = f"Auto-installed absent Python library: '{missing_pkg}'"
            except Exception as error:
                action["message"] = f"Automated package installation exception: {error}"
            return action

        name_match = re.search(r"NameError: name '([\w_]+)' is not defined", error_log)
        if name_match:
            undefined_name = name_match.group(1)
            standard_libs = ["sys", "re", "json", "time", "os", "subprocess", "platform", "urllib", "math", "shutil", "ast"]
            if undefined_name in standard_libs:
                self.log(f"Identified unimported standard library '{undefined_name}'. Auto-injecting...", "WARNING")
                try:
                    patched_content = f"import {undefined_name}\n" + broken_code
                    with open(script_path, "w", encoding="utf-8") as f:
                        f.write(patched_content)
                    action["patched"] = True
                    action["message"] = f"Injected 'import {undefined_name}' into code preamble."
                except Exception as error:
                    action["message"] = f"Standard library injection exception: {error}"
            return action

        return action

    # =====================================================================
    # RULE 6, 14, 16: QUAD-CORE AI AUTO-DEBUGGER
    # =====================================================================
    def _ask_ai_to_heal(self, broken_code, error_log, script_path):
        action = {"patched": False, "engine": "None", "message": ""}
        system_prompt = (
            "You are an Elite Python Auto-Debugger and Self-Healing Engine.\n"
            "Analyze a broken Python script and its traceback error, then rewrite and return the complete corrected code.\n"
            "CRITICAL RULES:\n"
            "1. Return ONLY raw executable Python code. Do not include markdown formatting (```python).\n"
            "2. Do not write conversational text or explanations.\n"
            "3. Ensure perfect indentation and zero syntax regressions."
        )
        user_prompt = f"Broken Script Content:\n{broken_code}\n\nTraceback Error:\n{error_log}"

        fixed_code = None
        engine_name = "None"

        # Core 1: Gemini SDK
        if GEMINI_SDK_AVAILABLE and self.gemini_key and not fixed_code:
            try:
                model = genai.GenerativeModel("gemini-1.5-pro")
                res = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
                fixed_code = self._clean_code(res.text)
                engine_name = "Google Gemini SDK Pro"
            except Exception as e:
                self.log(f"[Core 1: Gemini] Debugger exception: {e}", "WARNING")

        # Core 2: OpenAI Failsafe
        if self.openai_key and not fixed_code:
            try:
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.openai_key}"}
                payload = {"model": self.model_cloud, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]}
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=45) as response:
                    fixed_code = self._clean_code(json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"])
                    engine_name = f"OpenAI {self.model_cloud}"
            except Exception as e:
                self.log(f"[Core 2: OpenAI] Debugger exception: {e}", "WARNING")

        # Core 3: Ollama Local Fallback
        if not fixed_code:
            try:
                headers = {"Content-Type": "application/json"}
                payload = {"model": self.model_local, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "stream": False}
                req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=50) as response:
                    fixed_code = self._clean_code(json.loads(response.read().decode("utf-8"))["message"]["content"])
                    engine_name = f"Ollama {self.model_local}"
            except Exception as e:
                self.log(f"[Core 3: Ollama] Debugger exception: {e}", "WARNING")

        if fixed_code:
            try:
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(fixed_code)
                action["patched"] = True
                action["engine"] = engine_name
                action["message"] = "AI Core successfully compiled and applied script repairs."
            except Exception as e:
                action["message"] = f"Failed to save patched script: {e}"

        return action

    def execute_and_heal(self, script_path):
        self._handshake("IN_PROGRESS")
        self.log(f"Initiating autonomous runtime supervision on target node: '{script_path}'")
        
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            self.log(f"Execution Verification Cycle (Attempt {attempt}/{max_attempts})...", "INFO")
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log(f"Verification Successful: Script '{script_path}' executed flawlessly.", "SUCCESS")
                report = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "target_script": script_path,
                    "execution_status": "SUCCESS",
                    "healing_applied": (attempt > 1),
                    "stdout_trace": result.stdout.strip()
                }
                self._save_report(report)
                if attempt > 1:
                    self.push_to_github(f"Autonomous Self-Healed Stable Release: {os.path.basename(script_path)}")
                self._handshake("COMPLETED")
                return report

            error_output = result.stderr
            self.log(f"RUNTIME EXCEPTION DETECTED in '{script_path}'! Engaging Self-Healing Matrix...", "ERROR")
            
            try:
                with open(script_path, "r", encoding="utf-8") as f:
                    broken_code = f.read()
            except Exception as e:
                broken_code = f"# Error reading target script: {e}"

            # Step 1: Procedural Algorithmic Recovery
            if attempt == 1:
                self.log("Attempting instantaneous algorithmic procedural recovery...", "INFO")
                fallback_action = self._execute_procedural_fallback(broken_code, error_output, script_path)
                if fallback_action.get("patched"):
                    continue

            # Step 2: Quad-Core AI Self-Healing Architecture
            self.log(f"Engaging Quad-Core AI Auto-Debugger Node (Cycle {attempt})...", "INFO")
            self.create_backup(script_path)
            
            healing_action = self._ask_ai_to_heal(broken_code, error_output, script_path)
            
            if healing_action.get("patched"):
                with open(script_path, "r", encoding="utf-8") as f:
                    patched_code = f.read()
                if not self.verify_syntax(patched_code):
                    self.log("AI patch rejected by Layer 2 AST Shield (Syntax errors present). Rolling back.", "ERROR")
                    self.restore_backup(script_path)
            else:
                self.log("AI Debugger Core exhausted without resolving runtime exception.", "CRITICAL")
                break

        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_script": script_path,
            "execution_status": "HEALING_FAILED_EXHAUSTED",
            "healing_applied": True,
            "diagnostic_message": "Maximum recovery cycles reached without achieving stability."
        }
        self._save_report(report)
        self._handshake("COMPLETED")
        return report

if __name__ == "__main__":
    sentinel = Ai_Agent_99_Evolving_Git_Sync_Optimizer()
    print("--- OMNIMATRIX V2.0: AGENT 99 CLOUD SENTINEL COMPLETE ---")
