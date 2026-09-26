from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import time
from typing import Any


class Action(str, Enum):
    OBSERVE = "observe"
    ORIENT = "orient"
    INVESTIGATE = "investigate"
    FOLLOW = "follow"
    SEARCH = "search"
    RETURN = "return"
    WAIT = "wait"
    STOP = "stop"


@dataclass(frozen=True)
class Observation:
    contrast_change: float
    motion_magnitude: float
    direction: float | None = None
    source: str = "synthetic"
    timestamp: float = field(default_factory=time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for value in (self.contrast_change, self.motion_magnitude):
            if not 0.0 <= value <= 1.0:
                raise ValueError("observation scores must be between 0 and 1")
        if self.direction is not None and not -180.0 <= self.direction <= 180.0:
            raise ValueError("direction must be between -180 and 180 degrees")


@dataclass(frozen=True)
class Outcome:
    success: bool | None = None
    blocked: bool = False
    collision: bool = False
    useful_information: bool = False
    note: str = ""


@dataclass(frozen=True)
class Decision:
    action: Action
    confidence: float
    uncertainty: str
    reasons: tuple[str, ...]
    observation_timestamp: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class MemoryEvent:
    observation: Observation
    decision: Decision
    outcome: Outcome | None = None
