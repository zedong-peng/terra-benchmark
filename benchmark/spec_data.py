from copy import deepcopy


SCORING = {
    "alpha": 0.15,
    "beta": 0.10,
    "gamma": 0.05,
}

# TSS weights: closed-loop tasks T5 and T8 are double-weighted.
# TSS = sum(task_score * weight) / TSS_DENOMINATOR
TSS_WEIGHTS = {
    "T1": 1.0,
    "T2": 1.0,
    "T3": 1.0,
    "T4": 1.0,
    "T5": 2.0,  # closed-loop: geometry mismatch correction
    "T6": 1.0,
    "T7": 1.0,
    "T8": 2.0,  # closed-loop: recovery after disturbance
}
TSS_DENOMINATOR = 10.0  # sum of all weights: 6×1 + 2×2 = 10

# CLI: Closed-Loop Index = (T5 + T8) / (T1 + T3)
# Measures degradation under expectation violation relative to nominal locomotion.
CLI_NUMERATOR_TASKS = ["T5", "T8"]
CLI_DENOMINATOR_TASKS = ["T1", "T3"]

# Task groupings for analysis and reporting
NOMINAL_TASKS = ["T1", "T2", "T3", "T4", "T6", "T7"]
CLOSED_LOOP_TASKS = ["T5", "T8"]

TERRA_VERSION = "2.0"

COMMON_REQUIRED_LOG_FIELDS = [
    "timestamp",
    "event",
    "task_id",
    "trial_id",
]

TASK_DEFINITIONS = [
    {
        "task_id": "T1",
        "slug": "steady_walking",
        "title": "Steady Walking",
        "purpose": "Measure nominal gait stability, heading control, and single-leg support on flat terrain.",
        "dominant_primitive": "steady-state locomotion",
        "dominant_failure_mode": "gait collapse or drift under nominal walking",
        "geometry": {
            "walkway_length_mm": 3000,
            "walkway_width_mm": 600,
            "centerline_tolerance_mm": 120,
        },
        "tolerances": {
            "dimensional_mm": 3,
            "flatness_mm_per_m": 2,
        },
        "materials": {
            "surface": "sealed birch plywood or matte HDPE",
            "target_friction_coefficient": "0.60-0.75",
        },
        "start_pose": "Robot stands with both feet inside the start box, centered on the lane, pelvis yaw aligned to lane centerline.",
        "finish_condition": "Both feet fully cross the finish line without fall, external support, or leaving the lane.",
        "contact_policy": {
            "handrail_allowed": False,
            "external_support_allowed": False,
            "non_foot_ground_contacts_allowed": False,
        },
        "variants": {
            "canonical": {"description": "Straight flat walkway with no disturbances."},
            "parametric": {"description": "Start speed and finish position randomized within marked tolerances."},
            "challenge": {"description": "Subtle visual texture change introduced at midpoint without changing geometry."},
        },
        "scoring_notes": "Primary metric is success. Time and drift penalties separate stable from merely successful gait.",
        "bom_rows": [
            ["item", "quantity", "spec"],
            ["surface_panel", "2", "1500x600x18 mm birch plywood"],
            ["support_frame", "2", "6060 aluminum extrusion, 1500 mm"],
            ["alignment_tape", "1 roll", "25 mm matte vinyl tape"],
        ],
        "assembly_steps": [
            "Join two panels into a continuous 3000 mm lane and verify panel seam step is below 1 mm.",
            "Apply lane edge and centerline tape using the supplied drawing.",
            "Level the frame and verify flatness along the lane with a straightedge.",
        ],
    },
    {
        "task_id": "T2",
        "slug": "narrow_placement",
        "title": "Narrow Placement",
        "purpose": "Measure lateral balance and foot placement precision in a constrained stepping corridor.",
        "dominant_primitive": "precise foot placement",
        "dominant_failure_mode": "step placement outside the allowed corridor",
        "geometry": {
            "walkway_length_mm": 3000,
            "walkway_width_mm": 600,
            "stepping_corridor_width_mm": 220,
        },
        "tolerances": {
            "dimensional_mm": 3,
            "lateral_marking_mm": 2,
        },
        "materials": {
            "surface": "sealed birch plywood with matte lane markings",
            "target_friction_coefficient": "0.60-0.75",
        },
        "start_pose": "Robot stands centered in the corridor with feet parallel and inside the marked start box.",
        "finish_condition": "Robot reaches the end box while all stance contacts remain inside the stepping corridor.",
        "contact_policy": {
            "handrail_allowed": False,
            "external_support_allowed": False,
            "non_foot_ground_contacts_allowed": False,
        },
        "variants": {
            "canonical": {"description": "Fixed 220 mm corridor."},
            "parametric": {"description": "Corridor width may vary between 200 and 240 mm while remaining constant for a run."},
            "challenge": {"description": "A 5 degree visual skew is added to markings to test placement under misleading perspective cues."},
        },
        "scoring_notes": "Foot placement error is measured from the marked corridor centerline.",
        "bom_rows": [
            ["item", "quantity", "spec"],
            ["surface_panel", "2", "1500x600x18 mm birch plywood"],
            ["corridor_marking", "1 roll", "12 mm matte black vinyl tape"],
            ["support_frame", "2", "6060 aluminum extrusion, 1500 mm"],
        ],
        "assembly_steps": [
            "Build the flat lane as in T1.",
            "Mark the 220 mm stepping corridor relative to lane centerline with tolerance under 2 mm.",
            "Verify the start and finish boxes are centered on the corridor.",
        ],
    },
    {
        "task_id": "T3",
        "slug": "standard_ascent",
        "title": "Standard Ascent",
        "purpose": "Measure terrain height estimation, swing clearance, and upward load transfer during stair ascent.",
        "dominant_primitive": "up-step estimation and ascent",
        "dominant_failure_mode": "toe clip or unstable weight transfer on stairs",
        "geometry": {
            "stair_count": 10,
            "riser_height_mm": 170,
            "tread_depth_mm": 280,
            "clear_width_mm": 900,
            "top_landing_mm": 800,
        },
        "tolerances": {
            "dimensional_mm": 2,
            "riser_uniformity_mm": 1,
        },
        "materials": {
            "surface": "painted plywood treads with anti-slip coating",
            "target_friction_coefficient": "0.65-0.80",
        },
        "start_pose": "Robot starts 500 mm before the first riser facing the staircase centerline.",
        "finish_condition": "Both feet stably occupy the top landing after climbing all 10 steps.",
        "contact_policy": {
            "handrail_allowed": False,
            "external_support_allowed": False,
            "non_foot_ground_contacts_allowed": False,
        },
        "variants": {
            "canonical": {"description": "Uniform 10-step staircase with matte, high-contrast nosing."},
            "parametric": {"description": "Nosing color and ambient light vary while geometry remains fixed."},
            "challenge": {"description": "A low-contrast stair texture reduces visual edge saliency without changing geometry."},
        },
        "scoring_notes": "Swing-foot clearance and completion time distinguish conservative from confident ascent behavior.",
        "bom_rows": [
            ["item", "quantity", "spec"],
            ["stair_modules", "10", "900x280x170 mm modular plywood stair boxes"],
            ["landing_panel", "1", "900x800x18 mm birch plywood"],
            ["anti_slip_coating", "1", "clear polyurethane with grit additive"],
        ],
        "assembly_steps": [
            "Assemble modular stair boxes on a rigid frame and verify each riser is within 1 mm of target height.",
            "Apply high-contrast nosing tape to each tread edge.",
            "Confirm top landing is level with the tenth tread and free of lip discontinuities.",
        ],
    },
    {
        "task_id": "T4",
        "slug": "standard_descent",
        "title": "Standard Descent",
        "purpose": "Measure probing, center-of-mass control, and uncertainty handling during stair descent.",
        "dominant_primitive": "down-step control",
        "dominant_failure_mode": "over-commitment before support is confirmed on lower step",
        "geometry": {
            "stair_count": 10,
            "riser_height_mm": 170,
            "tread_depth_mm": 280,
            "clear_width_mm": 900,
            "bottom_landing_mm": 800,
        },
        "tolerances": {
            "dimensional_mm": 2,
            "riser_uniformity_mm": 1,
        },
        "materials": {
            "surface": "painted plywood treads with anti-slip coating",
            "target_friction_coefficient": "0.65-0.80",
        },
        "start_pose": "Robot starts on the top landing with both feet fully supported and pelvis aligned to stair centerline.",
        "finish_condition": "Robot reaches the bottom landing with both feet stably supported and no fall.",
        "contact_policy": {
            "handrail_allowed": False,
            "external_support_allowed": False,
            "non_foot_ground_contacts_allowed": False,
        },
        "variants": {
            "canonical": {"description": "Uniform 10-step staircase descending to a flat landing."},
            "parametric": {"description": "Ambient light and tread texture vary while geometry remains fixed."},
            "challenge": {"description": "One tread edge has reduced visual contrast to force stronger contact-based correction."},
        },
        "scoring_notes": "Recovery steps and support contacts expose uncertainty handling on descent.",
        "bom_rows": [
            ["item", "quantity", "spec"],
            ["stair_modules", "10", "900x280x170 mm modular plywood stair boxes"],
            ["landing_panel", "1", "900x800x18 mm birch plywood"],
            ["anti_slip_coating", "1", "clear polyurethane with grit additive"],
        ],
        "assembly_steps": [
            "Reuse the T3 staircase geometry and verify descent is run in the opposite direction.",
            "Ensure bottom landing is flush with the final riser.",
            "Inspect all stair nosings before each evaluation block.",
        ],
    },
    {
        "task_id": "T5",
        "slug": "height_anomaly",
        "title": "Height Anomaly",
        "purpose": "Measure online correction when one stair violates the learned cadence of an otherwise regular staircase.",
        "dominant_primitive": "geometry mismatch correction",
        "dominant_failure_mode": "failure to update swing height after expectation violation",
        "geometry": {
            "stair_count": 10,
            "nominal_riser_height_mm": 170,
            "anomalous_riser_height_mm": 210,
            "tread_depth_mm": 280,
            "clear_width_mm": 900,
            "anomaly_step_index": 6,
        },
        "tolerances": {
            "dimensional_mm": 2,
            "anomaly_height_mm": 2,
        },
        "materials": {
            "surface": "painted plywood treads with anti-slip coating",
            "target_friction_coefficient": "0.65-0.80",
        },
        "start_pose": "Robot starts 500 mm before the first riser and is not informed which step is anomalous.",
        "finish_condition": "Robot reaches the top landing while correctly traversing the anomaly and continuing without fall.",
        "contact_policy": {
            "handrail_allowed": False,
            "external_support_allowed": False,
            "non_foot_ground_contacts_allowed": False,
        },
        "variants": {
            "canonical": {"description": "Step 6 uses a 210 mm riser while all others remain 170 mm."},
            "parametric": {"description": "Exactly one riser is sampled in the 190-230 mm range and its index is hidden from the controller."},
            "challenge": {"description": "Anomaly is combined with lower visual contrast on the anomalous nosing."},
        },
        "scoring_notes": "This is the signature closed-loop task. Reward successful continuation, not just perfect nominal cadence.",
        "bom_rows": [
            ["item", "quantity", "spec"],
            ["stair_modules", "9", "900x280x170 mm modular plywood stair boxes"],
            ["anomaly_module", "1", "900x280x210 mm modular plywood stair box"],
            ["landing_panel", "1", "900x800x18 mm birch plywood"],
        ],
        "assembly_steps": [
            "Build the staircase as in T3, but replace the sixth module with the anomalous riser module.",
            "Verify that only one riser differs from the nominal geometry.",
            "For parametric mode, move or replace the anomaly before the evaluation block and log the final ground truth separately.",
        ],
    },
    {
        "task_id": "T6",
        "slug": "discrete_crossing",
        "title": "Discrete Crossing",
        "purpose": "Measure discrete step commitment, stride planning, and landing precision over a single gap.",
        "dominant_primitive": "discrete crossing decision",
        "dominant_failure_mode": "undershoot or unstable landing after a committed crossing",
        "geometry": {
            "approach_length_mm": 600,
            "gap_length_mm": 180,
            "landing_length_mm": 600,
            "walkway_width_mm": 600,
        },
        "tolerances": {
            "dimensional_mm": 2,
            "edge_straightness_mm": 1,
        },
        "materials": {
            "surface": "plywood approach and landing platforms over rigid frame",
            "target_friction_coefficient": "0.60-0.75",
        },
        "start_pose": "Robot stands with toes 300 mm before the gap edge, centered laterally.",
        "finish_condition": "Robot places both feet on the landing platform without contacting the gap interior.",
        "contact_policy": {
            "handrail_allowed": False,
            "external_support_allowed": False,
            "non_foot_ground_contacts_allowed": False,
        },
        "variants": {
            "canonical": {"description": "Fixed 180 mm gap with rigid edges."},
            "parametric": {"description": "Gap length sampled between 160 and 210 mm for each evaluation block."},
            "challenge": {"description": "A dark interior cavity increases depth uncertainty while edge geometry remains unchanged."},
        },
        "scoring_notes": "The task should penalize edge contacts even when the robot eventually reaches the landing.",
        "bom_rows": [
            ["item", "quantity", "spec"],
            ["approach_platform", "1", "600x600x18 mm plywood"],
            ["landing_platform", "1", "600x600x18 mm plywood"],
            ["frame_members", "4", "6060 aluminum extrusion, 600 mm"],
        ],
        "assembly_steps": [
            "Mount the approach and landing platforms on a rigid frame with the specified gap length between them.",
            "Measure the gap at both edges and center to ensure parallelism.",
            "Mask the interior cavity walls to avoid reflective cues.",
        ],
    },
    {
        "task_id": "T7",
        "slug": "repeated_obstacles",
        "title": "Repeated Obstacles",
        "purpose": "Measure repeated swing-foot clearance and short-horizon adaptation across several low obstacles.",
        "dominant_primitive": "sequential adaptation",
        "dominant_failure_mode": "accumulated toe clips or timing drift across obstacle sequence",
        "geometry": {
            "walkway_length_mm": 3000,
            "walkway_width_mm": 600,
            "obstacle_count": 5,
            "obstacle_height_mm": 40,
            "obstacle_thickness_mm": 20,
            "obstacle_spacing_mm": 350,
        },
        "tolerances": {
            "dimensional_mm": 2,
            "spacing_mm": 3,
        },
        "materials": {
            "surface": "flat plywood lane with removable HDPE or wood obstacle bars",
            "target_friction_coefficient": "0.60-0.75",
        },
        "start_pose": "Robot starts 400 mm before the first obstacle with stance centered on the lane.",
        "finish_condition": "Robot traverses the full obstacle series and crosses the finish line without fall.",
        "contact_policy": {
            "handrail_allowed": False,
            "external_support_allowed": False,
            "non_foot_ground_contacts_allowed": False,
        },
        "variants": {
            "canonical": {"description": "Five 40 mm obstacles spaced at 350 mm."},
            "parametric": {"description": "Obstacle spacing varies between 320 and 380 mm while keeping count fixed."},
            "challenge": {"description": "One obstacle is colored to blend with the floor, testing continued adaptation under weaker visual segmentation."},
        },
        "scoring_notes": "Repeated small contacts matter here; a single clip should not be treated the same as a fall, but it must be visible in scoring.",
        "bom_rows": [
            ["item", "quantity", "spec"],
            ["surface_panel", "2", "1500x600x18 mm birch plywood"],
            ["obstacle_bars", "5", "600x20x40 mm HDPE or hardwood bars"],
            ["mounting_guides", "10", "low-profile guides for repeatable obstacle placement"],
        ],
        "assembly_steps": [
            "Assemble the flat lane as in T1.",
            "Install placement guides so each obstacle can be repositioned repeatably.",
            "Place five bars at the prescribed spacing measured from leading edge to leading edge.",
        ],
    },
    {
        "task_id": "T8",
        "slug": "mild_recovery",
        "title": "Mild Recovery",
        "purpose": "Measure whether a robot can recover and continue after a small, controlled disturbance.",
        "dominant_primitive": "recovery after disturbance",
        "dominant_failure_mode": "inability to resume gait after slip or toe-clearance mismatch",
        "geometry": {
            "walkway_length_mm": 3000,
            "walkway_width_mm": 600,
            "disturbance_zone_length_mm": 300,
            "hidden_mismatch_height_mm": 15,
        },
        "tolerances": {
            "dimensional_mm": 2,
            "disturbance_zone_mm": 2,
        },
        "materials": {
            "surface": "flat lane with one interchangeable disturbance insert",
            "target_friction_coefficient": "0.25-0.35 in slip patch mode or nominal 0.60-0.75 in mismatch mode",
        },
        "start_pose": "Robot starts centered in lane and is not informed which disturbance insert is active.",
        "finish_condition": "Robot reaches the finish line after encountering the disturbance and resumes forward motion.",
        "contact_policy": {
            "handrail_allowed": False,
            "external_support_allowed": False,
            "non_foot_ground_contacts_allowed": False,
        },
        "variants": {
            "canonical": {"description": "One 15 mm hidden toe-clearance mismatch insert in a nominal walkway."},
            "parametric": {"description": "Either a 10-20 mm mismatch insert or a 300 mm low-friction patch is used and logged after the run."},
            "challenge": {"description": "Disturbance location shifts within a marked zone and surface texture matches the nominal floor."},
        },
        "scoring_notes": "Recovery steps and continued forward progress are the main signal; this task intentionally separates recoverable faults from terminal failures.",
        "bom_rows": [
            ["item", "quantity", "spec"],
            ["surface_panel", "2", "1500x600x18 mm birch plywood"],
            ["disturbance_insert", "1", "300x600 mm swap-in panel with 15 mm mismatch or low-friction surface"],
            ["support_frame", "2", "6060 aluminum extrusion, 1500 mm"],
        ],
        "assembly_steps": [
            "Assemble the nominal lane as in T1 with a swap-in section centered near the midpoint.",
            "Install either the hidden mismatch insert or the low-friction insert before each block.",
            "Ensure the insert perimeter is flush enough that only the intended disturbance is present.",
        ],
    },
]


BASELINE_RUNS = {
    "sim_baseline": {
        "robot": {
            "name": "AtlasSim-LocoPolicy",
            "morphology": "humanoid",
            "height_m": 1.45,
            "mass_kg": 56.0,
            "sensors": ["rgbd_head_camera", "imu", "joint_encoders", "foot_contact"],
            "controller_frequency_hz": 200,
            "compute": "1x workstation GPU for policy inference",
        },
        "notes": "Illustrative baseline with strong nominal locomotion but weaker recovery under mismatched geometry.",
        "tasks": {
            "T1": {"success": 1.0, "completion_time_s": 6.2, "extra_support_contacts": 0, "recovery_steps": 0, "foot_placement_error_mm": 18, "energy_proxy": 0.44},
            "T2": {"success": 0.95, "completion_time_s": 7.1, "extra_support_contacts": 0, "recovery_steps": 0, "foot_placement_error_mm": 24, "energy_proxy": 0.48},
            "T3": {"success": 0.92, "completion_time_s": 11.8, "extra_support_contacts": 0, "recovery_steps": 1, "foot_placement_error_mm": 22, "energy_proxy": 0.58},
            "T4": {"success": 0.88, "completion_time_s": 13.1, "extra_support_contacts": 1, "recovery_steps": 1, "foot_placement_error_mm": 26, "energy_proxy": 0.62},
            "T5": {"success": 0.62, "completion_time_s": 14.5, "extra_support_contacts": 2, "recovery_steps": 3, "foot_placement_error_mm": 41, "energy_proxy": 0.74},
            "T6": {"success": 0.81, "completion_time_s": 5.8, "extra_support_contacts": 1, "recovery_steps": 1, "foot_placement_error_mm": 20, "energy_proxy": 0.53},
            "T7": {"success": 0.77, "completion_time_s": 9.4, "extra_support_contacts": 1, "recovery_steps": 2, "foot_placement_error_mm": 29, "energy_proxy": 0.60},
            "T8": {"success": 0.58, "completion_time_s": 8.9, "extra_support_contacts": 2, "recovery_steps": 4, "foot_placement_error_mm": 38, "energy_proxy": 0.72},
        },
    },
    "real_robot_baseline": {
        "robot": {
            "name": "H1-LabBaseline",
            "morphology": "humanoid",
            "height_m": 1.72,
            "mass_kg": 70.0,
            "sensors": ["stereo_head_camera", "imu", "joint_encoders", "foot_contact"],
            "controller_frequency_hz": 250,
            "compute": "embedded x86 controller with onboard perception stack",
        },
        "notes": "Illustrative baseline with slower motion and stronger disturbance tolerance than the simulation policy.",
        "tasks": {
            "T1": {"success": 0.98, "completion_time_s": 7.4, "extra_support_contacts": 0, "recovery_steps": 0, "foot_placement_error_mm": 20, "energy_proxy": 0.49},
            "T2": {"success": 0.91, "completion_time_s": 8.8, "extra_support_contacts": 0, "recovery_steps": 1, "foot_placement_error_mm": 22, "energy_proxy": 0.51},
            "T3": {"success": 0.90, "completion_time_s": 13.6, "extra_support_contacts": 0, "recovery_steps": 1, "foot_placement_error_mm": 23, "energy_proxy": 0.61},
            "T4": {"success": 0.86, "completion_time_s": 15.0, "extra_support_contacts": 1, "recovery_steps": 2, "foot_placement_error_mm": 27, "energy_proxy": 0.66},
            "T5": {"success": 0.79, "completion_time_s": 16.1, "extra_support_contacts": 1, "recovery_steps": 2, "foot_placement_error_mm": 33, "energy_proxy": 0.69},
            "T6": {"success": 0.84, "completion_time_s": 7.0, "extra_support_contacts": 1, "recovery_steps": 1, "foot_placement_error_mm": 24, "energy_proxy": 0.56},
            "T7": {"success": 0.82, "completion_time_s": 10.7, "extra_support_contacts": 1, "recovery_steps": 2, "foot_placement_error_mm": 28, "energy_proxy": 0.63},
            "T8": {"success": 0.76, "completion_time_s": 10.4, "extra_support_contacts": 1, "recovery_steps": 2, "foot_placement_error_mm": 31, "energy_proxy": 0.68},
        },
    },
}


def task_lookup():
    return {task["task_id"]: deepcopy(task) for task in TASK_DEFINITIONS}
