from pathlib import Path
import os
import textwrap
import xml.etree.ElementTree as ET

from benchmark.spec_data import TASK_DEFINITIONS

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TASKS_DIR = ROOT / "tasks"
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


def add_box(ax, x, y, w, h, title, lines, fc, ec="#1f2937"):
    rect = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + 0.15, y + h - 0.22, title, fontsize=14, fontweight="bold", color="#111827")
    for i, line in enumerate(lines):
        ax.text(x + 0.18, y + h - 0.55 - 0.22 * i, line, fontsize=9.8, color="#1f2937")


def add_arrow(ax, x1, y1, x2, y2, color="#374151"):
    arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14, linewidth=1.6, color=color)
    ax.add_patch(arrow)


def render_overview():
    ASSETS.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"figure.facecolor": "#fbf7ef", "axes.facecolor": "#fbf7ef", "font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.text(0.5, 7.45, "Embodied Mobility Benchmark", fontsize=24, fontweight="bold", color="#111827")
    ax.text(0.5, 7.05, "A physical benchmark for humanoid locomotion built around movement primitives, not demo scenes.", fontsize=12.5, color="#374151")
    add_box(ax, 0.6, 5.35, 3.2, 1.25, "Closed-Loop Hypothesis", ["Vision estimates terrain.", "Body feedback corrects online.", "Disturbance recovery matters."], "#dbeafe")
    add_box(ax, 5.05, 5.35, 3.45, 1.25, "Movement Primitives", ["Steady gait, placement, ascent, descent,", "mismatch correction, crossing,", "adaptation, recovery"], "#dcfce7")
    add_box(ax, 9.6, 5.35, 3.1, 1.25, "Physical Standardization", ["CAD, drawings, BOM, tolerances,", "surface specs, calibration,", "scoring"], "#fde68a")
    add_arrow(ax, 3.85, 5.98, 4.85, 5.98)
    add_arrow(ax, 8.55, 5.98, 9.45, 5.98)
    colors = ["#f8d7da", "#f8d7da", "#fce7f3", "#fce7f3", "#e9d5ff", "#ddd6fe", "#d1fae5", "#fed7aa"]
    start_x, y, w, h, gap = 0.45, 2.65, 1.45, 1.25, 0.15
    for i, (task, color) in enumerate(zip(TASK_DEFINITIONS, colors)):
        x = start_x + i * (w + gap)
        rect = Rectangle((x, y), w, h, facecolor=color, edgecolor="#1f2937", linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + 0.1, y + 0.83, task["task_id"], fontsize=11.5, fontweight="bold", color="#111827")
        words = task["title"].split()
        if len(words) <= 2:
            ax.text(x + 0.1, y + 0.43, " ".join(words), fontsize=9.1, color="#1f2937")
        else:
            ax.text(x + 0.1, y + 0.54, " ".join(words[:2]), fontsize=9.1, color="#1f2937")
            ax.text(x + 0.1, y + 0.28, " ".join(words[2:]), fontsize=9.1, color="#1f2937")
    ax.text(0.8, 4.45, "Eight core tasks", fontsize=16, fontweight="bold", color="#111827")
    ax.text(0.8, 4.12, "Each task targets one dominant failure mode and one dominant movement primitive.", fontsize=10.8, color="#374151")
    add_arrow(ax, 6.95, 5.25, 6.95, 4.55)
    add_arrow(ax, 6.95, 2.55, 6.95, 1.95)
    add_box(ax, 3.1, 0.45, 7.7, 1.0, "Measured outputs", ["Success rate | time | extra contacts | recovery steps | foot placement error | energy proxy"], "#e5e7eb")
    out = ASSETS / "benchmark-overview.png"
    fig.savefig(out, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return out


def render_task_svg(task, out_path):
    width = 960
    height = 320
    root = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width=str(width), height=str(height), viewBox=f"0 0 {width} {height}")
    ET.SubElement(root, "rect", x="0", y="0", width=str(width), height=str(height), fill="#fbf7ef")
    ET.SubElement(root, "text", x="40", y="50", fill="#111827", style="font-size:30px;font-weight:700;font-family:Arial").text = f'{task["task_id"]}: {task["title"]}'
    ET.SubElement(root, "text", x="40", y="82", fill="#374151", style="font-size:16px;font-family:Arial").text = task["dominant_primitive"]
    ET.SubElement(root, "rect", x="40", y="120", width="880", height="120", rx="12", fill="#ffffff", stroke="#1f2937", **{"stroke-width": "2"})
    geom_lines = [f"{key.replace('_', ' ')}: {value}" for key, value in task["geometry"].items()]
    wrap_lines = []
    for line in geom_lines:
        wrap_lines.extend(textwrap.wrap(line, width=52))
    for i, line in enumerate(wrap_lines[:6]):
        ET.SubElement(root, "text", x="70", y=str(160 + i * 24), fill="#1f2937", style="font-size:18px;font-family:Arial").text = line
    ET.SubElement(root, "text", x="40", y="282", fill="#374151", style="font-size:15px;font-family:Arial").text = f'Failure mode: {task["dominant_failure_mode"]}'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(out_path, encoding="utf-8", xml_declaration=True)


def render_all():
    generated = [render_overview()]
    for task in TASK_DEFINITIONS:
        slug = f'{task["task_id"]}_{task["slug"]}'
        out_path = TASKS_DIR / slug / "drawings" / "layout.svg"
        render_task_svg(task, out_path)
        generated.append(out_path)
    return generated


def main(argv=None):
    argv = argv or []
    command = argv[0] if argv else "render"
    if command != "render":
        raise SystemExit("Usage: python3 -m benchmark.assets render")
    for path in render_all():
        print(path)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
