from __future__ import annotations

from dataclasses import dataclass

from .models import Observation


@dataclass(frozen=True)
class ReflexConfig:
    contrast_threshold: float = 0.35
    motion_threshold: float = 0.30


class VisualReflex:
    """Simplified engineering model for detecting visual change.

    This is not a biological reconstruction. It converts normalized signals
    into an Observation that later layers can interpret.
    """

    def __init__(self, config: ReflexConfig | None = None) -> None:
        self.config = config or ReflexConfig()

    def observe(
        self,
        contrast_change: float,
        motion_magnitude: float,
        direction: float | None = None,
        source: str = "synthetic",
    ) -> Observation:
        observation = Observation(
            contrast_change=contrast_change,
            motion_magnitude=motion_magnitude,
            direction=direction,
            source=source,
        )
        metadata = {
            "contrast_triggered": contrast_change >= self.config.contrast_threshold,
            "motion_triggered": motion_magnitude >= self.config.motion_threshold,
        }
        return Observation(
            contrast_change=observation.contrast_change,
            motion_magnitude=observation.motion_magnitude,
            direction=observation.direction,
            source=observation.source,
            timestamp=observation.timestamp,
            metadata=metadata,
        )
