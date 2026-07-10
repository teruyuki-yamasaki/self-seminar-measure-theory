#!/usr/bin/env python3
"""Visualize the three basic properties of outer measure in parallel panels."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import tempfile

_CACHE_ROOT = Path(tempfile.gettempdir()) / "math_measure_animation_cache"
(_CACHE_ROOT / "matplotlib").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(_CACHE_ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(_CACHE_ROOT / "matplotlib"))

import matplotlib
from PIL import Image

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#c8d1dc",
    "domain_fill": "#f7f1e4",
    "domain_edge": "#8d7b68",
    "c1_fill": "#79aee8",
    "c1_edge": "#2458a6",
    "c2a_fill": "#8bc89f",
    "c2a_edge": "#2c6e49",
    "c2b_fill": "#f0b45a",
    "c2b_edge": "#a85b00",
    "c3_fill": "#d97b7b",
    "c3_edge": "#9e3f3f",
    "union_fill": "#8a73d6",
    "union_edge": "#5d46ac",
    "sum_fill": "#d95f5f",
    "sum_edge": "#963434",
    "highlight": "#111111",
}

OUTDIR = Path("figures/measure/animations/caratheodory_outer_measure_axioms")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "caratheodory_outer_measure_axioms.gif"

FRAME_DURATION = 1.0
GIF_LOOP = 0
FRAME_COUNT = 6


@dataclass(frozen=True)
class Blob:
    center: tuple[float, float]
    radius_x: float
    radius_y: float
    wobble: tuple[float, float, float]
    angle: float


@dataclass(frozen=True)
class C1Case:
    label: str
    measure: float
    blob: Blob | None
    is_null: bool = False


@dataclass(frozen=True)
class C2Case:
    label_a: str
    label_b: str
    measure_a: float
    measure_b: float
    blob_a: Blob
    blob_b: Blob


@dataclass(frozen=True)
class C3Piece:
    label: str
    measure: float
    blob: Blob


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Hiragino Sans",
                "Yu Gothic",
                "Noto Sans CJK JP",
                "IPAexGothic",
                "DejaVu Sans",
            ],
            "axes.facecolor": COLORS["paper"],
            "figure.facecolor": COLORS["paper"],
            "savefig.facecolor": COLORS["paper"],
            "axes.edgecolor": COLORS["ink"],
            "xtick.color": COLORS["muted"],
            "ytick.color": COLORS["muted"],
            "text.color": COLORS["ink"],
        }
    )


def ensure_dirs() -> None:
    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)


def blob_polygon(blob: Blob, *, n_points: int = 180) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    mod = 1.0 + blob.wobble[0] * np.cos(3 * theta + blob.wobble[2]) + blob.wobble[1] * np.sin(5 * theta - 0.6 * blob.wobble[2])
    x = blob.radius_x * mod * np.cos(theta)
    y = blob.radius_y * mod * np.sin(theta)
    ct = np.cos(np.deg2rad(blob.angle))
    st = np.sin(np.deg2rad(blob.angle))
    xr = blob.center[0] + ct * x - st * y
    yr = blob.center[1] + st * x + ct * y
    return np.column_stack([xr, yr])


def draw_domain(ax: plt.Axes, *, label_y: float = 0.94) -> None:
    domain = Ellipse((0.5, 0.57), 0.82, 0.38, facecolor=COLORS["domain_fill"], edgecolor=COLORS["domain_edge"], lw=2.0, zorder=0)
    ax.add_patch(domain)
    ax.text(0.50, label_y, r"全体集合 $X$", ha="center", va="center", fontsize=13, color=COLORS["ink"], zorder=6)


def draw_number_line(ax: plt.Axes, max_value: float, *, line_y: float = 0.18) -> None:
    x0, x1 = 0.10, 0.92
    ax.plot([x0, x1], [line_y, line_y], color=COLORS["ink"], lw=1.8, zorder=1)
    ax.annotate("", xy=(x1 + 0.03, line_y), xytext=(x1, line_y), arrowprops={"arrowstyle": "->", "lw": 1.8, "color": COLORS["ink"]})
    ticks = np.linspace(0.0, max_value, 5)
    for tick in ticks:
        x = map_measure(tick, max_value)
        ax.plot([x, x], [line_y - 0.015, line_y + 0.015], color=COLORS["ink"], lw=1.0)
    ax.text(x0 - 0.03, line_y, "0", ha="right", va="center", fontsize=14, color=COLORS["muted"])
    ax.text(x1 + 0.045, line_y, r"$\infty$", ha="left", va="center", fontsize=19, color=COLORS["muted"])


def map_measure(value: float, max_value: float) -> float:
    x0, x1 = 0.10, 0.92
    return x0 + (x1 - x0) * min(value / max_value, 1.0)


def draw_blob(ax: plt.Axes, blob: Blob, *, facecolor: str, edgecolor: str, alpha: float, lw: float, zorder: int) -> np.ndarray:
    polygon = blob_polygon(blob)
    patch = Polygon(polygon, closed=True, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, lw=lw, zorder=zorder)
    ax.add_patch(patch)
    return polygon


def add_arrow_to_measure(
    ax: plt.Axes,
    start: tuple[float, float],
    value: float,
    max_value: float,
    *,
    color: str,
    label: str,
    line_y: float = 0.18,
    label_dx: float = 0.0,
    label_dy: float = 0.05,
) -> None:
    end = (map_measure(value, max_value), line_y)
    arrow = FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=11, lw=1.6, color=color, alpha=0.9, zorder=7)
    ax.add_patch(arrow)
    ax.add_patch(Circle(end, 0.014, facecolor=color, edgecolor="white", lw=0.8, zorder=8))
    if label:
        ax.text(
            end[0] + label_dx,
            line_y + label_dy,
            label,
            ha="center",
            va="bottom",
            fontsize=13.5,
            color=color,
            bbox={"boxstyle": "round, pad=0.10", "facecolor": COLORS["paper"], "edgecolor": "none", "alpha": 0.9},
            zorder=9,
        )


def c1_cases() -> list[C1Case]:
    return [
        C1Case("∅", 0.00, None),
        C1Case("N", 0.00, Blob((0.12, 0.53), 0.032, 0.020, (0.06, 0.05, 1.7), -10), True),
        C1Case("A_1", 0.12, Blob((0.28, 0.62), 0.06, 0.035, (0.10, 0.07, 0.4), -18)),
        C1Case("A_2", 0.22, Blob((0.47, 0.68), 0.08, 0.05, (0.08, 0.06, 1.1), 25)),
        C1Case("A_3", 0.33, Blob((0.68, 0.56), 0.10, 0.06, (0.09, 0.08, 1.9), -12)),
        C1Case("A_4", 0.47, Blob((0.36, 0.51), 0.12, 0.07, (0.07, 0.06, 0.7), 12)),
        C1Case("A_5", 0.61, Blob((0.62, 0.66), 0.14, 0.085, (0.08, 0.05, 2.4), -28)),
    ]


def c2_cases() -> list[C2Case]:
    return [
        C2Case("A_1", "B_1", 0.10, 0.24, Blob((0.36, 0.64), 0.05, 0.03, (0.07, 0.04, 0.2), 15), Blob((0.36, 0.64), 0.10, 0.065, (0.06, 0.05, 1.2), 15)),
        C2Case("A_2", "B_2", 0.16, 0.31, Blob((0.62, 0.61), 0.06, 0.04, (0.08, 0.05, 1.3), -20), Blob((0.62, 0.61), 0.12, 0.07, (0.07, 0.06, 1.9), -20)),
        C2Case("A_3", "B_3", 0.21, 0.43, Blob((0.46, 0.53), 0.08, 0.05, (0.06, 0.05, 2.1), 35), Blob((0.46, 0.53), 0.16, 0.095, (0.08, 0.05, 0.5), 35)),
        C2Case("A_4", "B_4", 0.14, 0.38, Blob((0.30, 0.53), 0.05, 0.04, (0.09, 0.05, 1.7), -8), Blob((0.30, 0.53), 0.145, 0.10, (0.07, 0.07, 0.4), -8)),
        C2Case("A_5", "B_5", 0.18, 0.48, Blob((0.69, 0.67), 0.07, 0.045, (0.07, 0.05, 2.6), 18), Blob((0.69, 0.67), 0.18, 0.09, (0.08, 0.06, 1.0), 18)),
        C2Case("A_6", "B_6", 0.26, 0.55, Blob((0.52, 0.62), 0.08, 0.055, (0.07, 0.05, 0.9), -10), Blob((0.52, 0.62), 0.22, 0.11, (0.07, 0.05, 2.1), -10)),
    ]


def c3_pieces() -> list[C3Piece]:
    return [
        C3Piece("A_1", 0.11, Blob((0.34, 0.63), 0.090, 0.058, (0.08, 0.05, 0.3), -18)),
        C3Piece("A_2", 0.09, Blob((0.41, 0.65), 0.075, 0.049, (0.08, 0.05, 1.0), 10)),
        C3Piece("A_3", 0.07, Blob((0.47, 0.62), 0.061, 0.041, (0.08, 0.05, 1.8), -6)),
        C3Piece("A_4", 0.055, Blob((0.51, 0.59), 0.050, 0.034, (0.08, 0.05, 2.5), 12)),
        C3Piece("A_5", 0.040, Blob((0.54, 0.61), 0.040, 0.028, (0.08, 0.05, 0.7), -14)),
        C3Piece("A_6", 0.028, Blob((0.56, 0.63), 0.032, 0.022, (0.08, 0.05, 2.9), 6)),
    ]


def draw_c1_panel(ax: plt.Axes, frame_index: int, cases: list[C1Case]) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    draw_domain(ax, label_y=0.79)
    draw_number_line(ax, 0.8)
    ax.text(0.5, 0.988, "C1  非負性", ha="center", va="top", fontsize=14, color=COLORS["ink"])
    ax.text(0.5, 0.946, r"$\Gamma(\varnothing)=0, \ 0\leq \Gamma(A)\leq \infty$", ha="center", va="top", fontsize=15.2, color=COLORS["ink"])

    for idx, case in enumerate(cases):
        if case.blob is None:
            ax.text(0.16, 0.57, r"$\varnothing$", fontsize=15, color=COLORS["muted"])
            continue
        active = idx == frame_index
        polygon = draw_blob(
            ax,
            case.blob,
            facecolor=COLORS["c1_fill"],
            edgecolor=COLORS["c1_edge"],
            alpha=0.80 if active else 0.20,
            lw=2.2 if active else 1.0,
            zorder=5 if active else 2,
        )
        if active:
            ax.text(case.blob.center[0], case.blob.center[1], rf"${case.label}$", ha="center", va="center", fontsize=12, color=COLORS["highlight"], zorder=6)
            add_arrow_to_measure(
                ax,
                (case.blob.center[0], case.blob.center[1] - 0.08),
                case.measure,
                0.8,
                color=COLORS["c1_edge"],
                label=rf"$\Gamma({case.label})$",
                label_dx=0.02,
                label_dy=0.055,
            )
        elif case.is_null:
            ax.text(case.blob.center[0], case.blob.center[1], rf"${case.label}$", ha="center", va="center", fontsize=11, color=COLORS["c1_edge"], zorder=4)

    if frame_index == 0:
        add_arrow_to_measure(ax, (0.15, 0.54), 0.0, 0.8, color=COLORS["c1_edge"], label=r"$\Gamma(\varnothing)$", label_dx=0.09, label_dy=0.055)
    if frame_index == 1:
        add_arrow_to_measure(ax, (cases[1].blob.center[0], cases[1].blob.center[1] - 0.05), 0.0, 0.8, color=COLORS["c1_edge"], label=r"$\Gamma(N)$", label_dx=0.05, label_dy=0.055)
    ax.text(0.5, 0.06, "大小の集合が非負の数へ写り, 空集合や零測度集合は 0 に写る", ha="center", va="center", fontsize=10.3, color=COLORS["muted"])


def draw_c2_panel(ax: plt.Axes, frame_index: int, cases: list[C2Case]) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    draw_domain(ax, label_y=0.79)
    draw_number_line(ax, 0.8)
    ax.text(0.5, 0.988, "C2  単調性", ha="center", va="top", fontsize=14, color=COLORS["ink"])
    ax.text(0.5, 0.946, r"$A\subset B \Rightarrow \Gamma(A)\leq \Gamma(B)$", ha="center", va="top", fontsize=15.2, color=COLORS["ink"])

    case = cases[frame_index]
    draw_blob(ax, case.blob_b, facecolor=COLORS["c2b_fill"], edgecolor=COLORS["c2b_edge"], alpha=0.38, lw=2.2, zorder=2)
    draw_blob(ax, case.blob_a, facecolor=COLORS["c2a_fill"], edgecolor=COLORS["c2a_edge"], alpha=0.82, lw=2.0, zorder=4)
    ax.text(case.blob_a.center[0], case.blob_a.center[1], rf"${case.label_a}$", ha="center", va="center", fontsize=12, color=COLORS["c2a_edge"])
    ax.text(case.blob_b.center[0] + 0.13, case.blob_b.center[1] + 0.08, rf"${case.label_b}$", ha="center", va="center", fontsize=12, color=COLORS["c2b_edge"])
    add_arrow_to_measure(
        ax,
        (case.blob_a.center[0] - 0.03, case.blob_a.center[1] - 0.08),
        case.measure_a,
        0.8,
        color=COLORS["c2a_edge"],
        label=rf"$\Gamma({case.label_a})$",
        label_dx=0.00,
        label_dy=0.055,
    )
    add_arrow_to_measure(
        ax,
        (case.blob_b.center[0] + 0.02, case.blob_b.center[1] - 0.11),
        case.measure_b,
        0.8,
        color=COLORS["c2b_edge"],
        label=rf"$\Gamma({case.label_b})$",
        label_dx=0.02,
        label_dy=0.055,
    )
    ax.text(0.5, 0.06, "包含が大きくなるほど, 対応する外測度も左へ戻らない", ha="center", va="center", fontsize=10.5, color=COLORS["muted"])


def draw_c3_panel(ax: plt.Axes, frame_index: int, pieces: list[C3Piece]) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    draw_domain(ax, label_y=0.79)
    draw_number_line(ax, 1.0)
    ax.text(0.5, 0.988, "C3  劣加法性", ha="center", va="top", fontsize=14, color=COLORS["ink"])
    ax.text(0.5, 0.946, r"$\Gamma\!\left(\bigcup_{n=1}^\infty A_n\right)\leq \sum_{n=1}^\infty \Gamma(A_n)$", ha="center", va="top", fontsize=15.2, color=COLORS["ink"])

    active_pieces = pieces[: frame_index + 1]
    union_measure = [0.11, 0.18, 0.24, 0.29, 0.33, 0.36][frame_index]
    sum_measure = sum(piece.measure for piece in active_pieces)

    for idx, piece in enumerate(pieces):
        active = idx <= frame_index
        draw_blob(
            ax,
            piece.blob,
            facecolor=COLORS["c3_fill"],
            edgecolor=COLORS["c3_edge"],
            alpha=0.55 if active else 0.12,
            lw=1.8 if active else 0.8,
            zorder=3 if active else 1,
        )
        if active:
            ax.text(piece.blob.center[0], piece.blob.center[1], rf"${piece.label}$", ha="center", va="center", fontsize=10.5, color="white", zorder=5)

    union_formula_pos = (0.33, 0.29)
    sum_formula_pos = (0.61, 0.29)
    ax.text(union_formula_pos[0], union_formula_pos[1] + 0.018, r"$\Gamma(\bigcup A_j)$", ha="center", va="center", fontsize=15, color=COLORS["union_edge"])
    ax.text(union_formula_pos[0], union_formula_pos[1] - 0.022, r"$j\leq n$", ha="center", va="center", fontsize=11.5, color=COLORS["union_edge"])
    ax.text(sum_formula_pos[0], sum_formula_pos[1] + 0.018, r"$\sum \Gamma(A_j)$", ha="center", va="center", fontsize=15, color=COLORS["sum_edge"])
    ax.text(sum_formula_pos[0], sum_formula_pos[1] - 0.022, r"$j\leq n$", ha="center", va="center", fontsize=11.5, color=COLORS["sum_edge"])
    add_arrow_to_measure(
        ax,
        (union_formula_pos[0], union_formula_pos[1] - 0.02),
        union_measure,
        1.0,
        color=COLORS["union_edge"],
        label="",
        label_dy=0.0,
    )
    add_arrow_to_measure(
        ax,
        (sum_formula_pos[0], sum_formula_pos[1] - 0.02),
        sum_measure,
        1.0,
        color=COLORS["sum_edge"],
        label="",
        label_dy=0.0,
    )
    ax.text(0.5, 0.06, "系列を足すほど和集合は増えるが, その外測度は和の総量を超えない", ha="center", va="center", fontsize=10.2, color=COLORS["muted"])


def draw_frame(save_path: Path, frame_index: int, cases_c1: list[C1Case], cases_c2: list[C2Case], pieces_c3: list[C3Piece]) -> None:
    fig = plt.figure(figsize=(16.5, 6.8))
    axes = [
        fig.add_axes([0.03, 0.08, 0.30, 0.86]),
        fig.add_axes([0.35, 0.08, 0.30, 0.86]),
        fig.add_axes([0.67, 0.08, 0.30, 0.86]),
    ]
    draw_c1_panel(axes[0], frame_index, cases_c1)
    draw_c2_panel(axes[1], frame_index, cases_c2)
    draw_c3_panel(axes[2], frame_index, pieces_c3)
    fig.suptitle(r"Carathéodory の外測度 $\Gamma$ の基本 3 条件", fontsize=22, y=0.99)
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()
    cases1 = c1_cases()
    cases2 = c2_cases()
    pieces3 = c3_pieces()

    frame_paths: list[Path] = []
    for frame_index in range(FRAME_COUNT):
        frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(frame_path, frame_index, cases1, cases2, pieces3)
        frame_paths.append(frame_path)

    images = [Image.open(path).convert("P", palette=Image.Palette.ADAPTIVE) for path in frame_paths]
    images[0].save(
        GIF_PATH,
        save_all=True,
        append_images=images[1:],
        duration=int(FRAME_DURATION * 1000),
        loop=GIF_LOOP,
        disposal=2,
    )
    print(f"Saved GIF to: {GIF_PATH.resolve()}")
    print(f"Saved frames to: {FRAMES_DIR.resolve()}")


if __name__ == "__main__":
    build_animation()
