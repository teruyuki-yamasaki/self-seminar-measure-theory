#!/usr/bin/env python3
"""Visualize the Lebesgue inner measure of rational points in the unit square."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
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
from matplotlib.patches import Rectangle


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#c8d1dc",
    "outer_fill": "#69a7ff",
    "outer_edge": "#2458a6",
    "cover_fill": "#f5c07a",
    "cover_edge": "#b76500",
    "point": "#c23b30",
    "inner_zero": "#2b8a57",
}

OUTDIR = Path("figures/measure/animations/rational_inner_measure")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "rational_inner_measure.gif"

FRAME_DURATION = 1.0
GIF_LOOP = 0
LEVELS = 6
DISPLAY_COUNT = 8
EPSILONS = [0.32, 0.16, 0.08, 0.04, 0.02, 0.01]


@dataclass(frozen=True)
class RationalPoint:
    x: float
    y: float
    complexity: int
    center_distance: float
    edge_distance: float


@dataclass(frozen=True)
class CoverSquare:
    x0: float
    y0: float
    side: float
    area_bound: float


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


def rational_axis(max_denominator: int = 12) -> list[tuple[int, int]]:
    vals: list[tuple[int, int]] = []
    for q in range(1, max_denominator + 1):
        for p in range(q + 1):
            if gcd(p, q) == 1:
                vals.append((p, q))
    vals.sort(key=lambda item: (item[1], item[0]))
    return vals


def rational_points(limit: int = 220) -> list[RationalPoint]:
    axis = rational_axis()
    rng = np.random.default_rng(41)
    items: list[RationalPoint] = []
    for px, qx in axis:
        for py, qy in axis:
            x = px / qx
            y = py / qy
            items.append(
                RationalPoint(
                    x=x,
                    y=y,
                    complexity=qx + qy,
                    center_distance=(x - 0.5) ** 2 + (y - 0.5) ** 2 + rng.uniform(0.0, 0.03),
                    edge_distance=min(x, 1.0 - x, y, 1.0 - y),
                )
            )
    items.sort(key=lambda item: (item.complexity, item.center_distance, -item.edge_distance, item.x, item.y))
    unique: list[RationalPoint] = []
    seen: set[tuple[float, float]] = set()
    for point in items:
        key = (round(point.x, 12), round(point.y, 12))
        if key in seen:
            continue
        seen.add(key)
        unique.append(point)
        if len(unique) >= limit:
            break
    return unique


def choose_display_points(candidates: list[RationalPoint], count: int) -> list[RationalPoint]:
    chosen: list[RationalPoint] = []
    remaining = list(candidates)

    while remaining and len(chosen) < count:
        if not chosen:
            point = min(remaining, key=lambda item: (item.center_distance, -item.edge_distance, item.complexity))
        else:
            central_pool = [point for point in remaining if point.edge_distance >= 0.14]
            if len(central_pool) < 40:
                central_pool = [point for point in remaining if point.edge_distance >= 0.10]
            if len(central_pool) < 20:
                central_pool = remaining

            pool = sorted(
                central_pool,
                key=lambda point: (0.45 * point.center_distance - 0.35 * point.edge_distance + 0.02 * point.complexity, point.x, point.y),
            )[:140]

            def spacing_score(point: RationalPoint) -> tuple[float, float, float, int]:
                min_dist = min((point.x - old.x) ** 2 + (point.y - old.y) ** 2 for old in chosen)
                return (min_dist, point.edge_distance, -point.center_distance, -point.complexity)

            point = max(pool, key=spacing_score)

        chosen.append(point)
        remaining = [item for item in remaining if item is not point]

    return chosen


def cover_squares(points: list[RationalPoint], epsilon: float) -> list[CoverSquare]:
    squares: list[CoverSquare] = []
    for index, point in enumerate(points, start=1):
        area = 0.72 * epsilon / (2**index)
        side = float(np.sqrt(area))
        x0 = float(np.clip(point.x - 0.5 * side, 0.0, 1.0 - side))
        y0 = float(np.clip(point.y - 0.5 * side, 0.0, 1.0 - side))
        squares.append(CoverSquare(x0=x0, y0=y0, side=side, area_bound=side * side))
    return squares


def draw_outer_grid(ax: plt.Axes, level: int) -> None:
    m = 2**level
    xs = np.linspace(0.0, 1.0, m + 1)
    for x in xs:
        ax.plot([x, x], [0.0, 1.0], color=COLORS["outer_edge"], lw=0.5, alpha=0.42, zorder=2)
        ax.plot([0.0, 1.0], [x, x], color=COLORS["outer_edge"], lw=0.5, alpha=0.42, zorder=2)


def draw_frame(
    save_path: Path,
    *,
    frame_index: int,
    level: int,
    displayed_points: list[RationalPoint],
    squares: list[CoverSquare],
    epsilon_history: list[float],
    shown_cover_area_history: list[float],
    complement_outer_history: list[float],
    inner_history: list[float],
) -> None:
    fig = plt.figure(figsize=(12.8, 7.2))
    ax_square = fig.add_axes([0.06, 0.14, 0.42, 0.72])
    ax_graph = fig.add_axes([0.56, 0.14, 0.38, 0.72])

    ax_square.add_patch(
        Rectangle((0.0, 0.0), 1.0, 1.0, facecolor=COLORS["outer_fill"], edgecolor=COLORS["outer_edge"], lw=3.0, alpha=0.18, zorder=0)
    )
    draw_outer_grid(ax_square, level)

    for square in squares:
        ax_square.add_patch(
            Rectangle(
                (square.x0, square.y0),
                square.side,
                square.side,
                facecolor=COLORS["cover_fill"],
                edgecolor=COLORS["cover_edge"],
                lw=0.8,
                alpha=0.38,
                zorder=3,
            )
        )

    if displayed_points:
        xs = [point.x for point in displayed_points]
        ys = [point.y for point in displayed_points]
        ax_square.scatter(xs, ys, s=28, color=COLORS["point"], linewidths=0, zorder=4)

    ax_square.set_xlim(0.0, 1.0)
    ax_square.set_ylim(0.0, 1.0)
    ax_square.set_aspect("equal")
    ax_square.set_xticks([])
    ax_square.set_yticks([])
    ax_square.set_title(
        rf"$I=[0, 1]^2,\ A=\mathbb{{Q}}^2\cap I$ に対する $A$ の被覆と $I \cap A^c$ の外側近似  $(2^{{{level}}}\times 2^{{{level}}})$",
        fontsize=13,
    )
    ax_square.text(
        0.02,
        0.98,
        "$I\\cap A^c$ は各タイルに点を含むので\n"
        + rf"$\mu^*(I \cap A^c)$ の近似は各段階で常に $1$",
        transform=ax_square.transAxes,
        va="top",
        fontsize=11,
        color=COLORS["outer_edge"],
        bbox={"boxstyle": "round, pad=0.22", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.92},
    )
    ax_square.text(
        0.02,
        0.06,
        "橙は可算被覆の最初の数項だけを図示\n"
        + rf"$k$ 番目の長方形の面積を $\varepsilon_n/2^k$ 以下に取れば, 被覆和は $<\varepsilon_n$",
        transform=ax_square.transAxes,
        va="bottom",
        fontsize=10.2,
        color=COLORS["cover_edge"],
        bbox={"boxstyle": "round, pad=0.22", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.92},
    )

    stages = np.arange(1, frame_index + 2)
    ax_graph.plot(stages, complement_outer_history, color=COLORS["outer_edge"], lw=2.6, marker="o", label=r"$\mu^*(I \cap A^c)=1$")
    ax_graph.plot(stages, epsilon_history, color=COLORS["cover_edge"], lw=2.4, marker="o", label=r"$\mu^*(A) \leq \varepsilon_n$")
    ax_graph.plot(stages, shown_cover_area_history, color=COLORS["cover_fill"], lw=1.8, marker="o", label=r"図示した被覆和 $<\varepsilon_n$")
    ax_graph.plot(stages, inner_history, color=COLORS["inner_zero"], lw=2.2, marker="o", label=r"$\mu_*(A; I)=1-1=0$")
    ax_graph.axhline(1.0, color=COLORS["outer_edge"], lw=1.0, alpha=0.35)
    ax_graph.axhline(0.0, color=COLORS["inner_zero"], lw=1.0, alpha=0.35)
    ax_graph.set_xlim(0.7, LEVELS + 0.3)
    ax_graph.set_ylim(-0.04, 1.08)
    ax_graph.set_xticks(np.arange(1, LEVELS + 1))
    ax_graph.set_yticks(np.linspace(0.0, 1.0, 6))
    ax_graph.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_graph.set_xlabel("近似段階")
    ax_graph.set_ylabel("面積")
    ax_graph.legend(loc="upper right", frameon=False, fontsize=10)
    ax_graph.set_title(r"青は $\mu^*(I \cap A^c)=1$, 橙は $\mu^*(A)$ の上界 $\varepsilon_n \to 0$", fontsize=13)
    ax_graph.text(
        0.04,
        0.14,
        rf"$m(I)=1$" "\n"
        + rf"$\mu^*(I \cap A^c)=1$" "\n"
        + rf"$\mu^*(A)=0$" "\n"
        + rf"$\mu_*(A; I)=0$",
        transform=ax_graph.transAxes,
        fontsize=11,
        color=COLORS["ink"],
        bbox={"boxstyle": "round, pad=0.28", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.92},
    )

    fig.suptitle(
        r"有理点集合:  $\mu^*(A)=0$ かつ  $\mu_*(A; I)=m(I)-\mu^*(I \cap A^c)=0$",
        fontsize=19,
        y=0.96,
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    all_points = rational_points()
    frame_paths: list[Path] = []
    epsilon_history: list[float] = []
    shown_cover_area_history: list[float] = []
    complement_outer_history: list[float] = []
    inner_history: list[float] = []
    displayed_points = choose_display_points(all_points, DISPLAY_COUNT)

    for frame_index, epsilon in enumerate(EPSILONS):
        level = frame_index + 1
        squares = cover_squares(displayed_points, epsilon)
        epsilon_history.append(epsilon)
        shown_cover_area_history.append(sum(square.area_bound for square in squares))
        complement_outer_history.append(1.0)
        inner_history.append(0.0)
        frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(
            frame_path,
            frame_index=frame_index,
            level=level,
            displayed_points=displayed_points,
            squares=squares,
            epsilon_history=epsilon_history,
            shown_cover_area_history=shown_cover_area_history,
            complement_outer_history=complement_outer_history,
            inner_history=inner_history,
        )
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
