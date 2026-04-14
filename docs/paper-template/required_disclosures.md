# Required Disclosures for Papers Reporting TERRA Results

If you use TERRA evaluation results in a published paper, conference submission, or preprint, you must disclose the following information.  This ensures that readers can assess the comparability of your results and reproduce your evaluation.

---

## Mandatory Disclosures

These fields must appear either in the main text, a caption, or a clearly labelled supplementary section.

### 1. Benchmark Version

State the exact TERRA version:

> *"All results use TERRA v2.0 \cite{terra2025}."*

Without a version number, results cannot be compared across papers.

### 2. Build Variant

State which task variant was used:

> *"Canonical build variant."*  or  *"Parametric build variant."*

Do not mix variants within a single TSS or CLI value.

### 3. Morphology Track

State the robot's morphology track:

> *"Humanoid track."*  or  *"Quadruped track."*

### 4. Measurement Methods for Each Metric

For every metric in Table 1, state which measurement method was used using the codes defined in `docs/measurement-protocol.md`:

| Metric | Method Code |
|--------|------------|
| success | `mocap` / `robot_proprioception` / `manual_video` |
| completion_time_s | `mocap` / `robot_proprioception` |
| extra_support_contacts | `mocap` / `pressure_plate` / `robot_proprioception` |
| recovery_steps | `mocap` / `robot_proprioception` |
| foot_placement_error_mm | `mocap` / `pressure_plate` / `overhead_camera` |
| energy_proxy | `mocap` / `robot_proprioception` / `unavailable` |

At minimum, disclose the method for foot_placement_error_mm and energy_proxy — these are the most method-sensitive metrics.

### 5. Number of Trials

State how many trials were averaged for each task score:

> *"Each task score is the mean of N trials."*

TERRA does not prescribe a minimum N, but single-trial results should be clearly identified as such.

### 6. Physical Setup Deviations

If your apparatus deviates from the TERRA specification in any way, state the deviation explicitly:

> *"The T8 slip insert was omitted; T8 was run with the mismatch insert only."*
> *"Ambient illumination was 180 lux (below the 300 lux lower bound) due to laboratory constraints."*

---

## Strongly Recommended Disclosures

These are not required but substantially improve reproducibility:

- Friction coefficient (measured value and measurement method) for at least the primary walking surface
- Camera calibration reprojection error (if overhead camera used for foot placement)
- Ambient illumination in lux (at task surface)
- Robot software/firmware version or commit hash
- Whether the robot was permitted any familiarization trials before scored evaluation

---

## What You Must NOT Do

- Do not report a TSS or CLI that mixes tasks run under different build variants
- Do not report `energy_proxy` as 0.0 when it was not measured — use -1.0 to indicate unavailability
- Do not compare TSS values across MAJOR benchmark versions without explicitly noting the version difference
- Do not cherry-pick the best trial out of multiple runs unless the paper clearly states that a best-of-N selection was made

---

## Citing TERRA

Include the following citation in your references:

```bibtex
@misc{terra2025,
  title        = {{TERRA}: Terrain-Engaged Robot Reasoning Assessment},
  author       = {{TERRA Benchmark Contributors}},
  year         = {2025},
  howpublished = {\url{https://github.com/your-org/terra-benchmark}},
  note         = {Benchmark version 2.0}
}
```

See `docs/paper-template/terra.bib` for additional citation entries.
