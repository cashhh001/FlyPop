from __future__ import annotations

from .memory import EventMemory
from .models import Action, Decision, Observation


class BoundedDecisionPolicy:
    """Small deterministic policy used as a transparent baseline.

    A future analytical model can replace this policy, but it must return the
    same bounded Action vocabulary and preserve uncertainty reporting.
    """

    def __init__(self, memory: EventMemory, repeated_failure_limit: int = 2) -> None:
        self.memory = memory
        self.repeated_failure_limit = repeated_failure_limit

    def choose(self, observation: Observation) -> Decision:
        similar = self.memory.find_similar(observation)
        reasons: list[str] = []
        confidence = 0.35
        uncertainty = "limited evidence"

        if observation.metadata.get("motion_triggered"):
            reasons.append("motion exceeded reflex threshold")
        if observation.metadata.get("contrast_triggered"):
            reasons.append("contrast change exceeded reflex threshold")

        if similar is not None and similar.outcome is not None:
            if similar.outcome.collision or similar.outcome.blocked:
                reasons.append("similar observation previously led to a blocked or unsafe outcome")
                return Decision(Action.ORIENT, 0.72, "similar prior failure", tuple(reasons), observation.timestamp)
            if similar.outcome.useful_information:
                reasons.append("similar observation previously produced useful information")
                return Decision(Action.INVESTIGATE, 0.62, "prior outcome is informative", tuple(reasons), observation.timestamp)
            reasons.append("similar observation exists but its outcome is unresolved")
            return Decision(Action.WAIT, 0.44, "memory match without reliable outcome", tuple(reasons), observation.timestamp)

        if observation.motion_magnitude >= 0.7:
            reasons.append("strong motion suggests orienting before moving")
            return Decision(Action.ORIENT, 0.58, "direction or source needs confirmation", tuple(reasons), observation.timestamp)
        if observation.contrast_change >= 0.7:
            reasons.append("strong contrast change merits a closer observation")
            return Decision(Action.INVESTIGATE, 0.55, "scene interpretation is incomplete", tuple(reasons), observation.timestamp)
        if observation.motion_magnitude >= 0.3 or observation.contrast_change >= 0.35:
            reasons.append("weak or moderate change detected")
            return Decision(Action.OBSERVE, confidence, uncertainty, tuple(reasons), observation.timestamp)

        reasons.append("no meaningful change detected")
        return Decision(Action.WAIT, 0.78, "low sensory evidence", tuple(reasons), observation.timestamp)
