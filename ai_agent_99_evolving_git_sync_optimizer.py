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

class EvolvingGitSyncOptimizer:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 99: evolving_git_sync_optimizer"
        
        # Paths Setup
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
        self.workspace_dir = os.path.join(self.base_dir, workspace_dir)
        self.log_file_path = os.path.join(self.workspace_dir, "agent_99_execution.log")
        
        # Load API keys and GitHub Configs from .env
        self.api_keys = self._load_env_keys()
        self.gemini_key = self.api_keys.get("GEMINI_API_KEY", None)
        self.github_token = self.api_keys.get("GITHUB_TOKEN", "")
        self.github_repo = self.api_keys.get("GITHUB_REPO", "")  # Format: "username/repo"
        self.github_branch = self.api_keys.get("GITHUB_BRANCH", "main")
        
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_key}" if self.gemini_key else None

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

    def _load_env_keys(self):
        keys = {}
        env_path = ".env"
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            keys[k.strip()] = v.strip().strip('"').strip("'")
            except Exception as e:
                print(f"[{self.agent_name}] Failed to parse .env: {str(e)}")
        return keys

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

    # ================= LAYER 1 & 2 SAFETY SYSTEM =================

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
            self.log_message(f"Layer 2 Safety Blocked: Syntax error in new code: {str(e)}", "ERROR")
            return False

    def _clean_code(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```python\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned

    # ================= GEMINI EVOLUTION ENGINE =================

    def query_gemini_for_evolution(self, original_code, instructions):
        if not self.gemini_key:
            self.log_message("Error: GEMINI_API_KEY missing in .env. Evolution cannot proceed.", "ERROR")
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
            req = urllib.request.Request(
                self.gemini_url,
                data=data_bytes,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=40) as response:
                res_body = json.loads(response.read().decode("utf-8"))
                raw_text = res_body["candidates"][0]["content"]["parts"][0]["text"]
                return self._clean_code(raw_text)
        except Exception as e:
            self.log_message(f"Gemini API request failed: {str(e)}", "ERROR")
            return None

    # ================= GITHUB SYNC ENGINE =================

    def push_to_github(self, commit_msg):
        if not self.github_token or not self.github_repo:
            self.log_message("GitHub configurations missing in .env. Skipping push.", "WARNING")
            return False

        self.log_message("Staging and committing verified changes...", "INFO")
        self._run_shell_command(["git", "add", "."])
        
        success, commit_out = self._run_shell_command(["git", "commit", "-m", commit_msg])
        if not success:
            self.log_message(f"Commit failed (possibly no changes to commit): {commit_out}", "WARNING")
            return False

        # Authenticate URL dynamically
        auth_url = f"https://{self.github_token}@github.com/{self.github_repo}.git"
        self._run_shell_command(["git", "remote", "remove", "origin"])
        self._run_shell_command(["git", "remote", "add", "origin", auth_url])

        self.log_message(f"Pushing updates to branch '{self.github_branch}'...", "INFO")
        push_success, push_out = self._run_shell_command(["git", "push", "-u", "origin", self.github_branch])
        
        # Clean up config URL for safety
        self._run_shell_command(["git", "remote", "set-url", "origin", f"https://github.com/{self.github_repo}.git"])

        if push_success:
            self.log_message("GitHub Synchronization Successful!", "INFO")
            return True
        else:
            self.log_message(f"GitHub Push failed: {push_out}", "ERROR")
            return False

    # ================= CORE EXECUTION PIPELINE =================

    def evolve_and_sync_file(self, target_file_path, evolution_instructions):
        """First evolves code safely, and if verified, pushes to remote GitHub repository."""
        if not os.path.exists(target_file_path):
            self.log_message(f"File {target_file_path} not found.", "ERROR")
            return False

        # 1. Create physical backup copy (.bak)
        if not self.create_backup(target_file_path):
            return False

        # Read original content
        with open(target_file_path, "r", encoding="utf-8") as f:
            original_code = f.read()

        # 2. Get modified code from Gemini
        self.log_message("Querying Gemini to rewrite and improve code...", "INFO")
        new_code = self.query_gemini_for_evolution(original_code, evolution_instructions)
        if not new_code:
            self.log_message("No code received. Keeping original file.", "WARNING")
            return False

        # 3. Verify syntax structure of new code
        if not self.verify_syntax(new_code):
            self.log_message("Rejecting new code due to syntax issues. File is untouched.", "ERROR")
            return False

        # 4. Overwrite file and check again
        try:
            with open(target_file_path, "w", encoding="utf-8") as f:
                f.write(new_code)
            self.log_message("New code written successfully.", "INFO")
        except Exception as e:
            self.log_message(f"Write failed: {str(e)}. Restoring from backup...", "CRITICAL")
            self.restore_backup(target_file_path)
            return False

        # 5. Automatically push to GitHub since changes were successful
        commit_message = f"Auto-Evolved {os.path.basename(target_file_path)} on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        self.push_to_github(commit_message)
        return True

if __name__ == "__main__":
    # Test Run
    sync_agent = EvolvingGitSyncOptimizer()
    print("--- Z-NET EVOLUTION & GIT ENGINE ACTIVE ---")
    
    # Aap isse kisi bhi target file ko change aur push karne ke liye bol sakte hain
    # Example: sync_agent.evolve_and_sync_file("ai_agent_65_supreme_creative_script_conductor.py", "Add a print statement for debug.")
