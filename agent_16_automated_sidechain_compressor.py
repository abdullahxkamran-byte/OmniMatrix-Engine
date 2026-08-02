import os
import sys
import json

class Agent_16_Automated_Sidechain_Compressor:
    def __init__(self):
        self.agent_name = "Agent_16_Automated_Sidechain_Compressor"

    def _calculate_ducking_physics(self, sub_profile: dict, kinetic_framing: str) -> dict:
        gain = float(sub_profile.get("target_gain_db", -2.0))
        sweep_duration = float(sub_profile.get("sweep_duration_seconds", 1.2))

        framing_lower = kinetic_framing.lower()
        is_aggressive = any(k in framing_lower for k in ["fast", "action", "hyper", "phonk"])

        if is_aggressive:
            threshold = -35.0
            ratio = 12.0
            attack = 1.5
            ducking = -15.0 if gain > -2.0 else -10.0
            release = min(200.0, max(50.0, (sweep_duration * 1000.0) * 0.8))
            makeup_gain = 2.0
        else:
            threshold = -25.0
            ratio = 4.0
            attack = 10.0
            ducking = -8.0 if gain > -6.0 else -5.0
            release = min(600.0, max(200.0, (sweep_duration * 1000.0) * 0.6))
            makeup_gain = 0.5

        ffmpeg_sidechain = f"sidechaincompress=threshold={threshold}dB:ratio={ratio}:attack={attack}:release={release}:makeup={makeup_gain}"

        return {
            "threshold_db": threshold,
            "ratio": f"{ratio}:1",
            "attack_time_ms": round(attack, 1),
            "release_time_ms": round(release, 1),
            "ducking_depth_db": round(ducking, 1),
            "routing_target": "background_music_and_sfx",
            "ffmpeg_sidechain_filter": ffmpeg_sidechain
        }

    def _generate_vocal_rider_filter(self, kinetic_framing: str) -> str:
        framing_lower = kinetic_framing.lower()
        if any(k in framing_lower for k in ["dramatic", "cinematic", "sad"]):
            return "acompressor=threshold=-20dB:ratio=3:attack=15:release=500:makeup=1"
        else:
            return "acompressor=threshold=-15dB:ratio=2.5:attack=5:release=250:makeup=1.5"

    def execute(self, state: dict) -> dict:
        pipeline_status = state.get("pipeline_status", {})
        target_agent = pipeline_status.get("next_agent", "")

        if target_agent and "16" not in target_agent and target_agent != self.agent_name:
            print(f"[{self.agent_name}] Execution skipped. Queue targeted to: {target_agent}", flush=True)
            return state

        workspace_dir = state.get("workspace_dir", "")
        if not workspace_dir:
            workspace_dir = state.get("state_file_path", "")
            if workspace_dir:
                workspace_dir = os.path.dirname(workspace_dir)
            else:
                raise ValueError(f"[{self.agent_name}] CRITICAL ERROR: workspace_dir missing.")

        runtime_data = state.setdefault("runtime_data", {})
        module_audio = runtime_data.setdefault("module_b_audio", {})

        beat_map_data = module_audio.get("agent_14_beat_map", {})
        events = beat_map_data.get("beat_sync_events", [])

        if not events:
            print(f"[{self.agent_name}] WARNING: 'beat_sync_events' not found. Agent 14/15 required.", flush=True)
            events = []

        global_config = state.get("global_config", {})
        kinetic_framing = global_config.get("kinetic_framing", "Dynamic/Unbound")

        if "sidechain_compression_applied" in module_audio:
            module_audio.pop("sidechain_compression_applied", None)
            module_audio.pop("master_vocal_ducking_filter", None)
            for event in events:
                event.pop("sidechain_ducking_trigger", None)
            print(f"[{self.agent_name}] Idempotency sweep executed. Legacy sidechain triggers purged.", flush=True)

        print(f"[{self.agent_name}] Calculating procedural DSP sidechain physics based on '{kinetic_framing}'...", flush=True)

        processed_triggers = 0

        for event in events:
            sub_profile = event.get("sub_bass_dsp_blueprint")
            if sub_profile:
                ducking_params = self._calculate_ducking_physics(sub_profile, kinetic_framing)
                event["sidechain_ducking_trigger"] = ducking_params
                processed_triggers += 1

        vocal_rider = self._generate_vocal_rider_filter(kinetic_framing)

        module_audio["agent_14_beat_map"]["beat_sync_events"] = events
        module_audio["master_vocal_ducking_filter"] = vocal_rider
        module_audio["sidechain_compression_applied"] = True

        pipeline_status["last_active_agent"] = self.agent_name
        pipeline_status[self.agent_name] = "COMPLETED"

        state_file_path = state.get("state_file_path", "")
        if state_file_path and os.path.exists(os.path.dirname(state_file_path)):
            with open(state_file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)

        print(f"[{self.agent_name}] Success! {processed_triggers} Sidechain routing triggers & Master Vocal Rider mathematically generated.", flush=True)
        return state
