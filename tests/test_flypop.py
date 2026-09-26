from flypop.bridge import DryRunRobot, run_step
from flypop.decision import BoundedDecisionPolicy
from flypop.memory import EventMemory
from flypop.models import Action, MemoryEvent, Outcome
from flypop.reflex import VisualReflex


def test_low_change_waits() -> None:
    observation = VisualReflex().observe(0.05, 0.05)
    decision, _ = run_step(observation, BoundedDecisionPolicy(EventMemory()), DryRunRobot())
    assert decision.action is Action.WAIT


def test_strong_motion_orients() -> None:
    observation = VisualReflex().observe(0.1, 0.9, 90)
    decision, _ = run_step(observation, BoundedDecisionPolicy(EventMemory()), DryRunRobot())
    assert decision.action is Action.ORIENT


def test_memory_reacts_to_previous_blockage() -> None:
    memory = EventMemory()
    policy = BoundedDecisionPolicy(memory)
    first = VisualReflex().observe(0.8, 0.2, -20)
    memory.add(MemoryEvent(first, policy.choose(first), Outcome(blocked=True, note="test blockage")))
    second = VisualReflex().observe(0.8, 0.2, -20)
    decision, _ = run_step(second, policy, DryRunRobot())
    assert decision.action is Action.ORIENT
