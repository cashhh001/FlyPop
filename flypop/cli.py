from __future__ import annotations

import argparse

from .bridge import DryRunRobot, run_step
from .decision import BoundedDecisionPolicy
from .memory import EventMemory
from .reflex import VisualReflex


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the FlyPop dry-run demo")
    parser.add_argument("--log", default=None, help="optional JSONL decision log path")
    args = parser.parse_args()

    reflex = VisualReflex()
    policy = BoundedDecisionPolicy(EventMemory())
    robot = DryRunRobot()
    logger = None
    if args.log:
        from .bridge import DecisionLogger
        logger = DecisionLogger(args.log)

    samples = [
        (0.05, 0.05, 0.0),
        (0.82, 0.25, -35.0),
        (0.82, 0.25, -35.0),
        (0.20, 0.78, 90.0),
    ]
    for contrast, motion, direction in samples:
        observation = reflex.observe(contrast, motion, direction)
        decision, outcome = run_step(observation, policy, robot, logger)
        print(f"observation={contrast:.2f}/{motion:.2f} -> action={decision.action.value} "
              f"confidence={decision.confidence:.2f} uncertainty={decision.uncertainty} "
              f"outcome={outcome.note}")


if __name__ == "__main__":
    main()
