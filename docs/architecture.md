# FlyPop architecture

## Design boundary

FlyPop separates five things that are often collapsed into one vague claim of intelligence:

1. Live observation - what the sensors currently report.
2. Memory - selected records of previous observations and outcomes.
3. Inference - an interpretation of the available evidence.
4. Uncertainty - what remains unresolved.
5. Confirmed action - one bounded instruction passed to the robot adapter.

The code in this repository makes those boundaries explicit in `models.py`.

## Reflex layer

`VisualReflex` accepts normalized contrast and motion values and produces an `Observation`. This is a simplified engineering layer inspired by biological visual reflexes. It should not be described as a simulated fly brain or as a complete connectome implementation.

A future camera adapter can replace the synthetic input while preserving the same observation contract.

## Memory

`EventMemory` is bounded and intentionally lossy. It stores relevant observation-decision-outcome events and performs a simple similarity check. This is a baseline for testing whether context changes action selection; it is not episodic memory in the biological sense.

## Analytical layer

`BoundedDecisionPolicy` is a transparent deterministic baseline. A future model-backed analytical layer may use an external model, but it must preserve:

- The fixed action vocabulary.
- Explicit uncertainty.
- A dry-run mode.
- No direct motor or torque commands.
- Decision logging.

## Physical execution

The robot adapter is a boundary. In the current implementation, `DryRunRobot` never contacts hardware. A platform-specific adapter must be added only after the exact robot API, speed limits, obstacle behavior, and emergency-stop path are documented and tested.
