from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import json, os, time
from datetime import datetime

@dataclass
class AgentLogger:
    run_dir: str = field(default_factory=lambda: os.path.join("logs", "agent_runs", datetime.now().strftime("%Y%m%d_%H%M%S")))

    def __post_init__(self):
        os.makedirs(self.run_dir, exist_ok=True)
        self.log_path = os.path.join(self.run_dir, "events.jsonl")

    def log(self, *, agent: str, event: str, payload: Dict[str, Any], rationale_summary: Optional[str] = None):
        """
        We record structured steps, inputs, outputs, and a brief rationale summary.
        We intentionally avoid verbatim chain-of-thought; this is an action/decision trace safe for sharing.
        """
        entry = {
            "ts": time.time(),
            "agent": agent,
            "event": event,
            "rationale_summary": rationale_summary or "",
            "payload": payload,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

@dataclass
class Agent:
    name: str
    logger: AgentLogger

    def log(self, event: str, payload: Dict[str, Any], rationale_summary: Optional[str] = None):
        self.logger.log(agent=self.name, event=event, payload=payload, rationale_summary=rationale_summary)

    def run(self, *args, **kwargs):
        raise NotImplementedError







