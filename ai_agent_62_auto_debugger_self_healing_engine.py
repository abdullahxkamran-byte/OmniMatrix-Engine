import os
import sys
import re
import json
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

class AiAutoDebuggerSelfHealingEngine:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Ai Agent 62: auto_debugger_self_healing_engine"
        self.workspace_dir = workspace_dir
        self.report_path = os.path.join(self.workspace_dir, "62_healing_report.json")
        
        self.ollama_url = "http://localhost:11434/api/chat"
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.model_local = "llama3"
        self.model_cloud = "gpt-4o-mini"
        
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def execute_and_heal(self, script_path):
        print(f"[{self.agent_name}] Running execution on target: '{script_path}'...")
        
        # Target script ko run kiya ja raha hai
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[{self.agent_name}] Success: Script executed flawlessly.")
            report = {
                "agent": self.agent_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "target_script": script_path,
                "execution_status": "SUCCESS",
                "healing_applied": False,
                "stdout": result.stdout,
                "stderr": ""
            }
            self._save_report(report)
            return report

        # Error analyze aur extract kiya ja raha hai
        error_output = result.stderr
        print(f"[{self.agent_name}] Error detected during execution! Fetching original code and traceback...")
        
        # Target script ka content read karte hain taaki AI ko context de sakein
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                broken_code = f.read()
        except Exception as e:
            broken_code = f"# Error reading script: {str(e)}"

        # AI (LLM) Engine trigger karke healing process start karte hain
        healing_action = self._ask_ai_to_heal(broken_code, error_output, script_path)
        
        # Agar AI ne patch/fixed code successfully apply kiya hai, toh re-verify karenge
        if healing_action.get("patched"):
            print(f"[{self.agent_name}] AI Patch applied to script. Re-running script to verify healing...")
            retry_result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
            if retry_result.returncode == 0:
                print(f"[{self.agent_name}] AI Healing Succeeded! Script is now working fine.")
                status = "HEALED"
                error_output = ""
            else:
                print(f"[{self.agent_name}] AI Healing Failed on verification. Script still raising errors.")
                status = "HEALING_FAILED"
                error_output = retry_result.stderr
        else:
            status = "UNRESOLVED"

        report = {
            "agent": self.agent_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_script": script_path,
            "execution_status": status,
            "healing_applied": healing_action.get("patched", False),
            "ai_engine_used": healing_action.get("engine", "None"),
            "details_applied": healing_action.get("message", "No healing applied"),
            "stderr": error_output
        }
        self._save_report(report)
        return report

    def _clean_ai_code(self, raw_text):
        # AI code se markdown blocks aur unnecessary symbols clean karta hai
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```python\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned

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

        # LLM integration setup (Cloud API or Local)
        if self.openai_api_key:
            print(f"[{self.agent_name}] Querying Cloud AI Node [{self.model_cloud}] for healing...")
            url = self.openai_url
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            payload = {
                "model": self.model_cloud,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            engine_name = f"OpenAI {self.model_cloud}"
        else:
            print(f"[{self.agent_name}] Querying Local AI Node [{self.model_local}] via Ollama...")
            url = self.ollama_url
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": self.model_local,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False
            }
            engine_name = f"Ollama {self.model_local}"

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            
            with urllib.request.urlopen(req, timeout=40) as response:
                result = json.loads(response.read().decode("utf-8"))
                
                if self.openai_api_key:
                    raw_ai_code = result["choices"][0]["message"]["content"]
                else:
                    raw_ai_code = result["message"]["content"]

                fixed_code = self._clean_ai_code(raw_ai_code)
                
                # Dynamic file patching
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(fixed_code)
                
                action["patched"] = True
                action["engine"] = engine_name
                action["message"] = "AI successfully analyzed the error, rewrote, and auto-healed the script code."
                return action

        except Exception as e:
            print(f"[{self.agent_name}] Connection Exception: {str(e)}. Proceeding to algorithmic fallback...")
            return self._execute_procedural_fallback(broken_code, error_log, script_path)

    def _execute_procedural_fallback(self, broken_code, error_log, script_path):
        action = {"patched": False, "engine": "Algorithmic Fallback Engine", "message": ""}
        
        # Missing standard module checking
        module_match = re.search(r"ModuleNotFoundError: No module named '([\w\d_-]+)'", error_log)
        if module_match:
            missing_module = module_match.group(1)
            print(f"[{self.agent_name}] [Fallback] Installing missing module: '{missing_module}'...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", missing_module], check=True)
                action["patched"] = True
                action["message"] = f"Fallback installed missing module: '{missing_module}'"
            except Exception as e:
                action["message"] = f"Fallback failed to install module: {str(e)}"
            return action

        # Missing basic import checking
        name_error_match = re.search(r"NameError: name '([\w_]+)' is not defined", error_log)
        if name_error_match:
            undefined_name = name_error_match.group(1)
            standard_libs = ["sys", "re", "json", "time", "os", "subprocess", "platform", "urllib", "math"]
            if undefined_name in standard_libs:
                print(f"[{self.agent_name}] [Fallback] Injecting 'import {undefined_name}' statement...")
                try:
                    patched_content = f"import {undefined_name}\n" + broken_code
                    with open(script_path, "w", encoding="utf-8") as f:
                        f.write(patched_content)
                    action["patched"] = True
                    action["message"] = f"Fallback injected core import: 'import {undefined_name}'"
                except Exception as e:
                    action["message"] = f"Fallback failed to modify script: {str(e)}"
            return action

        return action

    def _save_report(self, data):
        try:
            with open(self.report_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[{self.agent_name}] Error writing report: {str(e)}")

if __name__ == "__main__":
    monitor = AiAutoDebuggerSelfHealingEngine()
    
    # AI debug flow ko test karne ke liye temporary broken python script write karte hain
    broken_test_path = "broken_temp_test.py"
    with open(broken_test_path, "w") as f:
        f.write("""# Broken script has undefined function and syntax logic
platform_name = sys.platform
print(f"Running platform: {platform_name}")
""")

    print("--- TESTING AI AUTO HEALING ENGINE ---")
    healing_report = monitor.execute_and_heal(broken_test_path)
    
    print("\n--- HEALING REPORT RESULT ---")
    print(json.dumps(healing_report, indent=4))
    
    # Cleanup broken test file
    if os.path.exists(broken_test_path):
        os.remove(broken_test_path)
