# Experiment plan

The first useful result is not a claim that FlyPop is intelligent. It is a reproducible comparison between simple controllers.

## Baselines

1. Random action selection.
2. Always-forward or always-search behavior, if safe in simulation.
3. Stateless reflex policy.
4. Reflex plus bounded memory.
5. Reflex plus memory plus analytical interpretation.

## Suggested metrics

- Collision count.
- Number of repeated failed actions.
- Time to recover from a blocked path.
- Useful-information events per minute.
- Stop-command latency.
- Decision confidence calibration.
- Percentage of actions with an explicit uncertainty reason.

Exact thresholds, environments, and hardware are still implementation details and must be recorded before physical evaluation.

## Experiment protocol

1. Fix the environment and lighting conditions.
2. Fix the starting position and target definition.
3. Run each controller for the same number of trials.
4. Save raw observations, decisions, outcomes, and failures as JSONL.
5. Report failures and missing data alongside successful runs.
6. Compare against the simplest baseline before changing the architecture.

## Open hypotheses

- Memory may reduce repeated attempts in visually similar blocked situations.
- A fast reflex signal may reduce the amount of scene interpretation needed before orienting.
- Explicit uncertainty may increase waiting or stopping, but could reduce unsafe actions.
- Physical embodiment may expose errors that are invisible in offline vision tests.

These are hypotheses to test, not demonstrated results.
