import os
import re
import sys
import json
import time
import urllib.request
import urllib.error
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class UniversalStoryArcArchitect:
    def __init__(self, state_file_path="matrix_state.json"):
        self.agent_name = "Ai Agent 05: story_arc_structural_architect"
        self.state_file = state_file_path
        
        # Network Resilience
        self.max_retries = 3
        self.retry_delay = 3
        
        # API Keys Initialization
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Setup Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                generation_config={"response_mime_type": "application/json"}
            )
            
        # OpenAI/Ollama Setup
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model_openai = "gpt-4o-mini"
        self.model_local = "llama3"

    def _log_info(self, message):
        print(f"[{self.agent_name}] INFO: {message}")

    def _log_error(self, message):
        print(f"[{self.agent_name}] ERROR: {message}", file=sys.stderr)

    def _read_state(self):
        if not os.path.exists(self.state_file):
            self._log_error("Critical Error: matrix_state.json not found.")
            sys.exit(1)
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self._log_error(f"Failed to read state file: {str(e)}")
            sys.exit(1)

    def _write_state(self, state_data):
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=4)
        except Exception as e:
            self._log_error(f"Failed to persist state: {str(e)}")

    def _clean_json_response(self, raw_text):
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned = cleaned[start_idx:end_idx + 1]
        return cleaned

    def _build_universal_prompt(self, topic, content_format, tension_data):
        """Dynamically architects the arc phases based on the OmniMatrix video format."""
        
        base_system = (
            "You are a master of short-form storytelling dynamics and cinematic pacing. "
            "Analyze the provided tension timeline and subject matter to structure a high-density, "
            "multi-stage story arc mapped out chronologically.\n"
            "Output must STRICTLY be a raw JSON object containing a list named 'arc_phases'.\n"
            "Each phase object must contain these exact keys:\n"
            "- 'phase_index': integer representing execution order (1, 2, 3...)\n"
            "- 'phase_name': string designating the arc level (e.g., 'The Hook', 'The Build', 'The Climax')\n"
            "- 'target_duration_ratio': float representing percentage of total runtime (must sum to 1.0 overall. e.g., 0.20 for 20%)\n"
            "- 'pacing_frequency': string description of edit speed (e.g., 'rapid-fire-cuts', 'atmospheric-draw')\n"
            "- 'audience_psychology_goal': string representing viewer mental state (e.g., 'shocked-confusion', 'absolute-payoff').\n"
        )

        user_context = (
            f"Topic: '{topic}'\n"
            f"Tension Map (from Agent 04):\n{json.dumps(tension_data, indent=2)}\n\n"
        )

        # Dynamic arc structures based on format
        if content_format == "cinematic_movie":
            mode_rules = (
                "MODE: CINEMATIC MOVIE EPISODE\n"
                "Structure into exactly 4 classic cinematic phases: 1. Setup (Incite), 2. Confrontation (Complicate), 3. Climax (High Action/Tension), 4. Resolution (Resolve/Cliffhanger).\n"
            )
        elif content_format == "casual_commentary":
            mode_rules = (
                "MODE: CASUAL CREATOR COMMENTARY\n"
                "Structure into exactly 3 creator phases: 1. The Context (Intro/Reaction), 2. The Deep Dive (Analysis/Joke), 3. The Verdict (Conclusion/Outro).\n"
            )
        else:
            mode_rules = (
                "MODE: AGGRESSIVE VIRAL EXPLAINER\n"
                "Structure into exactly 3 hyper-retaining phases: 1. The Disruption (Pattern-Interrupt Hook), 2. The Core Truth (Fast-paced evidence), 3. The Loop (Mind-bending conclusion that makes them rewatch).\n"
            )

        return base_system + mode_rules, user_context

    def _call_ai_engine(self, system_prompt, user_prompt):
        """Tri-Core Brain: Gemini -> OpenAI -> Ollama"""
        
        if self.gemini_api_key:
            self._log_info("Routing to Priority 1: Google Gemini (1.5 Flash)")
            try:
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini_model.generate_content(full_prompt)
                return json.loads(self._clean_json_response(response.text))
            except Exception as e:
                self._log_error(f"Gemini API failed: {str(e)}. Fallback to Priority 2...")

        if self.openai_api_key:
            self._log_info("Routing to Priority 2: OpenAI (GPT-4o-mini)")
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.openai_api_key}"
                }
                payload = {
                    "model": self.model_openai,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(self.openai_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=45) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    return json.loads(self._clean_json_response(result["choices"][0]["message"]["content"]))
            except Exception as e:
                self._log_error(f"OpenAI API failed: {str(e)}. Fallback to Priority 3...")

        self._log_info("Routing to Priority 3: Local Engine (Ollama)")
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": self.model_local,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "format": "json"
            }
            req = urllib.request.Request(self.ollama_url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=50) as response:
                result = json.loads(response.read().decode("utf-8"))
                return json.loads(self._clean_json_response(result["message"]["content"]))
        except Exception as e:
            self._log_error(f"Local Ollama failed: {str(e)}.")
            return None

    def _execute_procedural_fallback(self, content_format):
        """Generates a perfect mathematical structural breakdown if all APIs are offline."""
        self._log_info("Triggering Procedural Arc Architect Logic.")
        
        if content_format == "cinematic_movie":
            phases = [
                {"phase_index": 1, "phase_name": "Setup", "target_duration_ratio": 0.20, "pacing_frequency": "atmospheric-draw", "audience_psychology_goal": "curious-immersion"},
                {"phase_index": 2, "phase_name": "Confrontation", "target_duration_ratio": 0.40, "pacing_frequency": "building-momentum", "audience_psychology_goal": "rising-anxiety"},
                {"phase_index": 3, "phase_name": "Climax", "target_duration_ratio": 0.25, "pacing_frequency": "rapid-fire-cuts", "audience_psychology_goal": "adrenaline-peak"},
                {"phase_index": 4, "phase_name": "Resolution", "target_duration_ratio": 0.15, "pacing_frequency": "rhythmic-slowdown", "audience_psychology_goal": "satisfaction-or-cliffhanger"}
            ]
        elif content_format == "casual_commentary":
            phases = [
                {"phase_index": 1, "phase_name": "The Context", "target_duration_ratio": 0.25, "pacing_frequency": "jump-cut-intro", "audience_psychology_goal": "relatable-agreement"},
                {"phase_index": 2, "phase_name": "The Deep Dive", "target_duration_ratio": 0.50, "pacing_frequency": "steady-analysis", "audience_psychology_goal": "humorous-enlightenment"},
                {"phase_index": 3, "phase_name": "The Verdict", "target_duration_ratio": 0.25, "pacing_frequency": "punchline-outro", "audience_psychology_goal": "amused-satisfaction"}
            ]
        else:
            # Viral Explainer
            phases = [
                {"phase_index": 1, "phase_name": "The Disruption", "target_duration_ratio": 0.15, "pacing_frequency": "hyper-fast-glitch", "audience_psychology_goal": "shocked-attention"},
                {"phase_index": 2, "phase_name": "The Core Truth", "target_duration_ratio": 0.70, "pacing_frequency": "relentless-evidence-drop", "audience_psychology_goal": "mind-blown-realization"},
                {"phase_index": 3, "phase_name": "The Loop", "target_duration_ratio": 0.15, "pacing_frequency": "sudden-cut-to-black", "audience_psychology_goal": "compulsive-rewatch"}
            ]

        return {"arc_phases": phases}

    def execute(self):
        state = self._read_state()
        
        # Pipeline Gate Check
        target_agent = state.get("pipeline_status", {}).get("next_agent", "")
        if target_agent != "Ai_Agent_05":
            self._log_info(f"Pipeline queue targeted to '{target_agent}'. Execution suspended.")
            return False

        topic = state.get("runtime_data", {}).get("core_topic", "")
        content_format = state.get("global_config", {}).get("content_format", "explainer")
        
        # Pull Tension Data from Agent 04
        agent_04_data = state.get("runtime_data", {}).get("module_a_scripting", {}).get("agent_04_tension_peaks", {})
        tension_data = agent_04_data.get("tension_timeline", [])

        if not tension_data:
            self._log_error("Critical Error: Tension data missing from Agent 04.")
            return False

        self._log_info(f"Architecting Story Arc for format: {content_format.upper()}")

        system_prompt, user_prompt = self._build_universal_prompt(topic, content_format, tension_data)
        
        generated_data = None
        for attempt in range(1, self.max_retries + 1):
            parsed_json = self._call_ai_engine(system_prompt, user_prompt)
            if parsed_json and "arc_phases" in parsed_json:
                generated_data = parsed_json
                self._log_info(f"Success! Built {len(generated_data['arc_phases'])} Arc Phases.")
                break
            else:
                self._log_error("Invalid response format. Retrying...")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        if not generated_data:
            self._log_error("All models failed. Applying Procedural Arc Fallback.")
            generated_data = self._execute_procedural_fallback(content_format)
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_05_Fallback"
        else:
            state["pipeline_status"]["last_active_agent"] = "Ai_Agent_05"

        # Save Output to Module A Scripting Memory
        state["runtime_data"]["module_a_scripting"]["agent_05_story_arc"] = generated_data
        
        # STRICT HANDSHAKE PROTOCOL: Hand over to Agent 06
        state["pipeline_status"]["next_agent"] = "Agent_06"
        self._write_state(state)
        
        self._log_info("Arc Structure Locked! Pipeline handed over to Agent 06: word_count_guard_utility.")
        return True

if __name__ == "__main__":
    architect = UniversalStoryArcArchitect()
    architect.execute()
