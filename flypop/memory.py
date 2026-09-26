from __future__ import annotations

from collections import deque

from .models import MemoryEvent, Observation


class EventMemory:
    """Bounded memory for comparing current observations with prior events."""

    def __init__(self, max_events: int = 100, similarity_threshold: float = 0.75) -> None:
        if max_events < 1:
            raise ValueError("max_events must be positive")
        self.events: deque[MemoryEvent] = deque(maxlen=max_events)
        self.similarity_threshold = similarity_threshold

    @staticmethod
    def similarity(a: Observation, b: Observation) -> float:
        contrast = 1.0 - abs(a.contrast_change - b.contrast_change)
        motion = 1.0 - abs(a.motion_magnitude - b.motion_magnitude)
        if a.direction is None or b.direction is None:
            direction = 0.5
        else:
            difference = abs(a.direction - b.direction)
            difference = min(difference, 360.0 - difference)
            direction = 1.0 - difference / 180.0
        return (contrast + motion + direction) / 3.0

    def find_similar(self, observation: Observation) -> MemoryEvent | None:
        candidates = [
            event for event in self.events
            if self.similarity(observation, event.observation) >= self.similarity_threshold
        ]
        return max(candidates, key=lambda event: self.similarity(observation, event.observation), default=None)

    def add(self, event: MemoryEvent) -> None:
        self.events.append(event)
