from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from .models import Action, Decision, MemoryEvent, Observation, Outcome


class RobotAdapter(Protocol):
    def execute(self, action: Action) -> Outcome: ...


class DryRunRobot:
    """Safe adapter that records intent and never contacts hardware."""

    def execute(self, action: Action) -> Outcome:
        if action is Action.STOP:
            return Outcome(success=True, useful_information=True, note="dry-run stop")
        return Outcome(success=None, useful_information=True, note=f"dry-run action: {action.value}")


class DecisionLogger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, observation: Observation, decision: Decision, outcome: Outcome) -> None:
        payload = {
            "observation": {
                "contrast_change": observation.contrast_change,
                "motion_magnitude": observation.motion_magnitude,
                "direction": observation.direction,
                "source": observation.source,
                "timestamp": observation.timestamp,
                "metadata": observation.metadata,
            },
            "decision": {
                "action": decision.action.value,
                "confidence": decision.confidence,
                "uncertainty": decision.uncertainty,
                "reasons": decision.reasons,
            },
            "outcome": {
                "success": outcome.success,
                "blocked": outcome.blocked,
                "collision": outcome.collision,
                "useful_information": outcome.useful_information,
                "note": outcome.note,
            },
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def run_step(
    observation: Observation,
    policy,
    adapter: RobotAdapter,
    logger: DecisionLogger | None = None,
) -> tuple[Decision, Outcome]:
    decision = policy.choose(observation)
    outcome = adapter.execute(decision.action)
    policy.memory.add(MemoryEvent(observation, decision, outcome))
    if logger:
        logger.write(observation, decision, outcome)
    return decision, outcome
