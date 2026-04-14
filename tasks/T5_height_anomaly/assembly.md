# T5 Height Anomaly

## Purpose
Measure online correction when one stair violates the learned cadence of an otherwise regular staircase.

## Assembly Steps
- Build the staircase as in T3, but replace the sixth module with the anomalous riser module.
- Verify that only one riser differs from the nominal geometry.
- For parametric mode, move or replace the anomaly before the evaluation block and log the final ground truth separately.

## Surface Guidance
- Surface: painted plywood treads with anti-slip coating
- Target friction coefficient: 0.65-0.80

## Start / Finish
- Start pose: Robot starts 500 mm before the first riser and is not informed which step is anomalous.
- Finish condition: Robot reaches the top landing while correctly traversing the anomaly and continuing without fall.
