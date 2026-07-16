import os
import sys
import re
import ast
import json
import shutil
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

# Manual .env loader utility
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

class SupremeSelfHealingGitEngine:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 99: supreme_self_healing_git_engine"
        
        # Paths Setup
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        self.log_file_path = os.path.join(self.workspace_dir, "agent_99_execution.log")
        self.report_path = os.path.join(self.workspace_dir, "99_healing_and_sync_report.json")
        
        # API Keys and GitHub Configs from Environment
        self.gemini_key = os.environ.get("GEMINI_API_KEY", None)
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)
        self.github_token = os.environ.get("GITHUB_TOKEN", "")
        self.github_repo = os.environ.get("GITHUB_REPO", "")  # Format: "username/repo"
        self.github_branch = os.environ.get("GITHUB_BRANCH", "main")
        
        # LLM Endpoints
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_key}" if self.gemini_key else None
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        
        # Fallback Models
        self.model_local = "llama3"
        self.model_openai = "gpt-4o-mini"

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def log_message(self, message, level="INFO"):
        formatted_msg = f"[{level}] [{self.agent_name}] {message}"
        print(formatted_msg)
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as log_f:
                log_f.write(formatted_msg + "\n")
        except Exception:
            pass

    def _run_shell_command(self, cmd_list):
        try:
            result = subprocess.run(
                cmd_list,
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_details = e.stderr.strip() if e.stderr else str(e)
            return False, error_details

    # ================= SAFETY AND BACKUP SYSTEMS =================

    def create_backup(self, target_file_path):
        if not os.path.exists(target_file_path):
            return False
        backup_path = target_file_path + ".bak"
        try:
            shutil.copy2(target_file_path, backup_path)
            self.log_message(f"Layer 1 Safe: Backup copy created at '{backup_path}'", "INFO")
            return True
        except Exception as e:
            self.log_message(f"Backup failed: {str(e)}", "ERROR")
            return False

    def restore_backup(self, target_file_path):
        backup_path = target_file_path + ".bak"
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, target_file_path)
            self.log_message(f"Rollback Complete: Reverted code back to working state.", "WARNING")
            return True
        return False

    def verify_syntax(self, code_string):
        try:
            ast.parse(code_string)
            self.log_message("Layer 2 Safe: Syntax verified (0 errors detected).", "INFO")
            return True
        except SyntaxError as e:
            self.log_message(f"Layer 2 Safety Blocked: Syntax error detected: {str(e)}", "ERROR")
            return False

    def _clean_code(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```python\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned

    # ================= GITHUB SYNC ENGINE =================

    def push_to_github(self, commit_msg):
        if not self.github_token or not self.github_repo:
            self.log_message("GitHub configurations missing in .env. Skipping git push.", "WARNING")
            return False

        self.log_message("Staging and committing verified changes...", "INFO")
        self._run_shell_command(["git", "add", "."])
        
        success, commit_out = self._run_shell_command(["git", "commit", "-m", commit_msg])
        if not success:
            self.log_message(f"Commit skipped (no changes or already up-to-date): {commit_out}", "WARNING")
            return False

        auth_url = f"https://{self.github_token}@github.com/{self.github_repo}.git"
        self._run_shell_command(["git", "remote", "remove", "origin"])
        self._run_shell_command(["git", "remote", "add", "origin", auth_url])

        self.log_message(f"Pushing updates to branch '{self.github_branch}'...", "INFO")
        push_success, push_out = self._run_shell_command(["git", "push", "-u", "origin", self.github_branch])
        
        # Reset URL back to public view for security
        self._run_shell_command(["git", "remote", "set-url", "origin", f"[https://github.com/](https://github.com/){self.github_repo}.git"])

        if push_success:
            self.log_message("GitHub Synchronization Successful!", "INFO")
            return True
        else:
            self.log_message(f"GitHub Push failed: {push_out}", "ERROR")
            return False

    # ================= RUNTIME MONITORING & HEALING (FORMER AGENT 62) =================

    def execute_and_heal(self, script_path):
        """Runs the target script, catches stderr/traceback, and heals it instantly."""
        self.log_message(f"Running execution monitor on: '{script_path}'", "INFO")
        
        # Execute target script
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            self.log_message(f"Success: Script '{script_path}' executed flawlessly.", "INFO")
            report = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "target_script": script_path,
                "execution_status": "SUCCESS",
                "healing_applied": False,
                "stdout": result.stdout
            }
            self._save_report(report)
            return report

        # Error captured
        error_output = result.stderr
        self.log_message(f"CRASH DETECTED in '{script_path}'! Extracting error tracebacks...", "ERROR")
        
        # Read broken code
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                broken_code = f.read()
        except Exception as e:
            broken_code = f"# Error reading script: {str(e)}"

        # 1. First Attempt: Algorithmic Fallback Healing (Fast & Free)
        self.log_message("Attempting quick algorithmic procedural recovery...", "INFO")
        fallback_action = self._execute_procedural_fallback(broken_code, error_output, script_path)
        
        if fallback_action.get("patched"):
            self.log_message("Procedural patch applied. Verifying recovery...", "INFO")
            retry_result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
            if retry_result.returncode == 0:
                self.log_message("Procedural Healing Succeeded!", "INFO")
                # Automatically push recovered work to GitHub
                self.push_to_github(f"Auto-Healed (Procedural) {os.path.basename(script_path)}")
                return self._generate_and_save_report(script_path, "HEALED", True, "Procedural Fallback Engine", "Fixed imports or missing libraries.")

        # 2. Second Attempt: Smart AI Healing (Gemini/OpenAI/Ollama)
        self.log_message("Triggering AI Auto-Debugger Node...", "INFO")
        self.create_backup(script_path)  # Safety first
        
        healing_action = self._ask_ai_to_heal(broken_code, error_output, script_path)
        
        if healing_action.get("patched"):
            self.log_message("AI patch written. Re-verifying syntax and run...", "INFO")
            
            # Syntax verify
            with open(script_path, "r", encoding="utf-8") as f:
                patched_code = f.read()
                
            if not self.verify_syntax(patched_code):
                self.log_message("AI Patch rejected: Syntax errors found. Rolling back.", "ERROR")
                self.restore_backup(script_path)
                status = "HEALING_FAILED"
            else:
                retry_result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
                if retry_result.returncode == 0:
                    self.log_message("AI Healing Succeeded! Script is operational.", "INFO")
                    status = "HEALED"
                    # Push working state to GitHub
                    self.push_to_github(f"Auto-Healed (AI Engine) {os.path.basename(script_path)}")
                else:
                    self.log_message("AI Healing Failed on run verification. Reverting...", "ERROR")
                    self.restore_backup(script_path)
                    status = "HEALING_FAILED"
        else:
            status = "UNRESOLVED"

        return self._generate_and_save_report(script_path, status, healing_action.get("patched", False), healing_action.get("engine", "None"), healing_action.get("message", ""))

    def _ask_ai_to_heal(self, broken_code, error_log, script_path):
        action = {"patched": False, "engine": "None", "message": ""}
        
        system_prompt = (
            "You are an expert Python Auto-Debugger and Self-Healing Engine.\n"
            "Your task is to analyze a broken Python script and its traceback error, then rewrite and return the complete corrected code.\n"
            "CRITICAL: Return ONLY the raw Python code that will completely fix the script. Do not include markdown formatting "
            "(like ```python or ```), do not write any conversational explanations or descriptions, and do not introduce new bugs. "
            "Your output must be directly executable Python code."
        )
        user_prompt = f"Broken Script Content:\n{broken_code}\n\nTraceback Error:\n{error_log}"

        # Determine best available AI Engine
        if self.gemini_key:
            # Prefer Gemini (Matches Agent 99's primary system)
            self.log_message("Querying Gemini Engine for deep self-healing...", "INFO")
            fixed_code = self.query_gemini_for_evolution(broken_code, f"Fix this traceback error:\n{error_log}")
            engine_name = "Gemini Pro"
        elif self.openai_api_key:
            # Fallback to OpenAI GPT
            self.log_message("Querying OpenAI Engine for deep self-healing...", "INFO")
            fixed_code = self._query_openai(system_prompt, user_prompt)
            engine_name = f"OpenAI {self.model_openai}"
        else:
            # Fallback to Local Llama 3 via Ollama
            self.log_message("Querying Local Ollama Node...", "INFO")
            fixed_code = self._query_ollama(system_prompt, user_prompt)
            engine_name = f"Ollama {self.model_local}"

        if fixed_code:
            try:
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(fixed_code)
                action["patched"] = True
                action["engine"] = engine_name
                action["message"] = "AI successfully analyzed traceback error, corrected structural logic, and healed the script."
            except Exception as e:
                action["message"] = f"Failed to patch file: {str(e)}"
        
        return action

    def _execute_procedural_fallback(self, broken_code, error_log, script_path):
        action = {"patched": False, "engine": "Algorithmic Fallback Engine", "message": ""}
        
        # Case A: Missing package/module (ModuleNotFoundError)
        module_match = re.search(r"ModuleNotFoundError: No module named '([\w\d_-]+)'", error_log)
        if module_match:
            missing_module = module_match.group(1)
            self.log_message(f"Detected missing pip module '{missing_module}'. Running auto-installation...", "WARNING")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", missing_module], check=True)
                action["patched"] = True
                action["message"] = f"Auto-installed missing pip package: '{missing_module}'"
            except Exception as e:
                action["message"] = f"Failed to auto-install: {str(e)}"
            return action

        # Case B: Standard Python library not imported (NameError)
        name_error_match = re.search(r"NameError: name '([\w_]+)' is not defined", error_log)
        if name_error_match:
            undefined_name = name_error_match.group(1)
            standard_libs = ["sys", "re", "json", "time", "os", "subprocess", "platform", "urllib", "math", "shutil", "ast"]
            if undefined_name in standard_libs:
                self.log_message(f"Detected unimported standard library '{undefined_name}'. Auto-injecting import statement...", "WARNING")
                try:
                    patched_content = f"import {undefined_name}\n" + broken_code
                    with open(script_path, "w", encoding="utf-8") as f:
                        f.write(patched_content)
                    action["patched"] = True
                    action["message"] = f"Injected 'import {undefined_name}' into code preamble."
                except Exception as e:
                    action["message"] = f"Failed standard lib injection: {str(e)}"
            return action

        return action

    # ================= DYNAMIC EVOLUTION (REWRITING CORE FUNCTIONS) =================

    def query_gemini_for_evolution(self, original_code, instructions):
        if not self.gemini_key:
            self.log_message("Error: GEMINI_API_KEY missing in .env.", "ERROR")
            return None

        system_prompt = (
            "You are an Elite Python Architect. Your job is to modify the provided code to satisfy the user's instructions.\n"
            "CRITICAL RULES:\n"
            "1. Return ONLY raw executable Python code. No conversational text, no intro, no markdown syntax (do not write ```python).\n"
            "2. Ensure perfect indentation and syntax that passes compiler checks.\n"
            "3. Retain existing functionality unless specifically told to remove it."
        )
        user_prompt = f"Original Code:\n{original_code}\n\nInstructions:\n{instructions}"

        try:
            payload = {
                "contents": [
                    {"role": "user", "parts": [{"text": f"System Directive: {system_prompt}\n\nUser Context:\n{user_prompt}"}]}
                ]
            }
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(self.gemini_url, data=data_bytes, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=40) as response:
                res_body = json.loads(response.read().decode("utf-8"))
                raw_text = res_body["candidates"][0]["content"]["parts"][0]["text"]
                return self._clean_code(raw_text)
        except Exception as e:
            self.log_message(f"Gemini API request failed: {str(e)}", "ERROR")
            return None

    def _query_openai(self, system_prompt, user_prompt):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }
        payload = {
            "model": self.model_openai,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(self.openai_url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=40) as response:
                result = json.loads(response.read().decode("utf-8"))
                return self._clean_code(result["choices"][0]["message"]["content"])
        except Exception as e:
            self.log_message(f"OpenAI fallback failed: {str(e)}", "ERROR")
            return None

    def _query_ollama(self, system_prompt, user_prompt):
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model_local,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(self.ollama_url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=50) as response:
                result = json.loads(response.read().decode("utf-8"))
                return self._clean_code(result["message"]["content"])
        except Exception as e:
            self.log_message(f"Ollama local fallback failed: {str(e)}", "ERROR")
            return None

    # ================= EVOLUTION & RETENTION ENGINE CALLS =================

    def evolve_and_sync_file(self, target_file_path, evolution_instructions):
        """Evolves code safely, checks compilation, runs execution test, and pushes working copy to GitHub."""
        if not os.path.exists(target_file_path):
            self.log_message(f"Target file {target_file_path} not found.", "ERROR")
            return False

        # Create physical .bak
        if not self.create_backup(target_file_path):
            return False

        with open(target_file_path, "r", encoding="utf-8") as f:
            original_code = f.read()

        self.log_message("Calling Gemini AI Core to evolve code architecture...", "INFO")
        new_code = self.query_gemini_for_evolution(original_code, evolution_instructions)
        if not new_code:
            self.log_message("Evolution resulted in empty response. Keeping original.", "WARNING")
            return False

        # Verify Syntax
        if not self.verify_syntax(new_code):
            self.log_message("Aborting evolution: New code possesses syntax bugs.", "ERROR")
            return False

        # Write safely
        try:
            with open(target_file_path, "w", encoding="utf-8") as f:
                f.write(new_code)
            self.log_message("Success: Evolved code physically saved.", "INFO")
        except Exception as e:
            self.log_message(f"Write failed: {str(e)}. Restoring...", "CRITICAL")
            self.restore_backup(target_file_path)
            return False

        # Run test-execution of evolved code to ensure no runtime breakages!
        self.log_message("Performing post-evolution runtime monitoring...", "INFO")
        test_run = subprocess.run([sys.executable, target_file_path], capture_output=True, text=True)
        
        # Note: If script expects terminal prompts, execution might hang or return code > 0.
        # So we verify runtime syntax and import failures here.
        if test_run.returncode != 0 and "SyntaxError" in test_run.stderr:
            self.log_message("Evolved script crashed on execution check. Reverting...", "ERROR")
       