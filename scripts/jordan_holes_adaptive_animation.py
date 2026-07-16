#!/usr/bin/env python3
"""Adaptive Jordan area animation for planar regions with several holes."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import shutil

import matplotlib
from PIL import Image

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path as MplPath
from matplotlib.patches import Polygon, Rectangle
from matplotlib.ticker import MaxNLocator

GIF_LOOP = 0
FRAME_DURATION_MS = 1000


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "region_fill": "#d8e6f2",
    "region_edge": "#19486a",
    "inner": "#4c9f70",
    "outer": "#f0b45a",
    "dots": "#19486a",
    "grid": "#c8d1dc",
    "gap": "#d95f5f",
}


@dataclass(frozen=True)
class Cell:
    x0: float
    x1: float
    y0: float
    y1: float


@dataclass
class Step:
    level: int
    inner_cells: list[Cell]
    boundary_cells: list[Cell]
    inner_area: float
    outer_area: float


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


def polygon_area(points: np.ndarray) -> float:
    x = points[:, 0]
    y = points[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def random_star_curve(
    rng: np.random.Generator,
    center: tuple[float, float],
    base_radius: float,
    n_points: int = 360,
    amp_scale: float = 1.0,
) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    radius = np.ones_like(theta)
    for freq in range(2, 6):
        amplitude = amp_scale * rng.uniform(0.02, 0.08) / freq
        phase = rng.uniform(0.0, 2.0 * np.pi)
        radius += amplitude * np.cos(freq * theta + phase)
    radius = base_radius * (0.84 + 0.32 * (radius - radius.min()) / (radius.max() - radius.min()))
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    points = np.column_stack([x, y])
    return np.vstack([points, points[0]])


def build_region(seed: int, holes: int) -> tuple[np.ndarray, list[np.ndarray], float]:
    rng = np.random.default_rng(seed)
    outer = random_star_curve(rng, center=(0.5, 0.5), base_radius=0.38, amp_scale=1.3)

    hole_centers = [(0.34, 0.38), (0.63, 0.36), (0.42, 0.66), (0.67, 0.62)]
    hole_radii = [0.075, 0.062, 0.07, 0.055]
    holes_curves = [
        random_star_curve(rng, center=center, base_radius=radius, amp_scale=0.8)
        for center, radius in zip(hole_centers[:holes], hole_radii[:holes])
    ]
    exact_area = polygon_area(outer[:-1]) - sum(polygon_area(hole[:-1]) for hole in holes_curves)
    return outer, holes_curves, exact_area


def build_mask(outer: np.ndarray, holes: list[np.ndarray], resolution: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs = np.linspace(0.0, 1.0, resolution, endpoint=False) + 0.5 / resolution
    ys = np.linspace(0.0, 1.0, resolution, endpoint=False) + 0.5 / resolution
    xx, yy = np.meshgrid(xs, ys)
    points = np.column_stack([xx.ravel(), yy.ravel()])
    mask = MplPath(outer).contains_points(points).reshape(resolution, resolution)
    for hole in holes:
        mask &= ~MplPath(hole).contains_points(points).reshape(resolution, resolution)
    return mask, xx, yy


def sample_split_point(left: float, right: float, rng: np.random.Generator) -> float:
    midpoint = 0.5 * (left + right)
    sigma = 0.18 * (right - left)
    split = rng.normal(loc=midpoint, scale=sigma)
    margin = 0.12 * (right - left)
    return float(np.clip(split, left + margin, right - margin))


def subdivide(cell: Cell, rng: np.random.Generator) -> list[Cell]:
    x_mid = sample_split_point(cell.x0, cell.x1, rng)
    y_mid = sample_split_point(cell.y0, cell.y1, rng)
    return [
        Cell(cell.x0, x_mid, cell.y0, y_mid),
        Cell(x_mid, cell.x1, cell.y0, y_mid),
        Cell(cell.x0, x_mid, y_mid, cell.y1),
        Cell(x_mid, cell.x1, y_mid, cell.y1),
    ]


def edge_to_index(value: float, resolution: int) -> int:
    idx = int(np.floor(value * resolution))
    return max(0, min(resolution, idx))


def cell_mask_view(cell: Cell, mask: np.ndarray) -> np.ndarray:
    resolution = mask.shape[0]
    ix0 = edge_to_index(cell.x0, resolution)
    ix1 = edge_to_index(cell.x1, resolution)
    iy0 = edge_to_index(cell.y0, resolution)
    iy1 = edge_to_index(cell.y1, resolution)
    if ix1 <= ix0:
        ix1 = min(resolution, ix0 + 1)
    if iy1 <= iy0:
        iy1 = min(resolution, iy0 + 1)
    return mask[iy0:iy1, ix0:ix1]


def area(cell: Cell) -> float:
    return (cell.x1 - cell.x0) * (cell.y1 - cell.y0)


def build_steps(mask: np.ndarray, levels: int, seed: int) -> list[Step]:
    rng = np.random.default_rng(seed + 10)
    active_cells = [Cell(0.0, 1.0, 0.0, 1.0)]
    steps: list[Step] = []

    for level in range(levels + 1):
        inner_cells: list[Cell] = []
        boundary_cells: list[Cell] = []
        next_cells: list[Cell] = []

        for cell in active_cells:
            view = cell_mask_view(cell, mask)
            if view.size == 0:
                continue

            region_any = bool(np.any(view))
            region_all = bool(np.all(view))
            if region_all:
                inner_cells.append(cell)
                next_cells.append(cell)
            elif region_any:
                boundary_cells.append(cell)
                if level < levels:
                    next_cells.extend(subdivide(cell, rng))
                else:
                    next_cells.append(cell)

        inner_area = sum(area(cell) for cell in inner_cells)
        outer_area = inner_area + sum(area(cell) for cell in boundary_cells)
        steps.append(
            Step(
                level=level,
                inner_cells=inner_cells,
                boundary_cells=boundary_cells,
                inner_area=inner_area,
                outer_area=outer_area,
            )
        )
        active_cells = next_cells

    return steps


def interior_dots(mask: np.ndarray, xx: np.ndarray, yy: np.ndarray, *, seed: int, count: int = 1800) -> tuple[np.ndarray, np.ndarray]:
    points = np.column_stack([xx[mask], yy[mask]])
    if points.size == 0:
        return np.array([]), np.array([])
    rng = np.random.default_rng(seed)
    take = min(count, len(points))
    idx = rng.choice(len(points), size=take, replace=False)
    chosen = points[idx]
    return chosen[:, 0], chosen[:, 1]


def draw_step(
    step: Step,
    steps: list[Step],
    outer: np.ndarray,
    holes: list[np.ndarray],
    exact_area: float,
    dots_x: np.ndarray,
    dots_y: np.ndarray,
    save_path: Path,
) -> None:
    fig = plt.figure(figsize=(12.8, 6.9))
    ax_shape = fig.add_axes([0.06, 0.14, 0.44, 0.72])
    ax_area = fig.add_axes([0.58, 0.14, 0.36, 0.72])

    ax_shape.add_patch(
        Polygon(outer[:-1], closed=True, facecolor=COLORS["region_fill"], edgecolor=COLORS["region_edge"], lw=2.2, alpha=0.10, zorder=0)
    )
    ax_shape.scatter(dots_x, dots_y, s=3.2, color=COLORS["dots"], alpha=0.42, linewidths=0, zorder=0.5)

    for cell in step.boundary_cells:
        ax_shape.add_patch(
            Rectangle(
                (cell.x0, cell.y0),
                cell.x1 - cell.x0,
                cell.y1 - cell.y0,
                facecolor=COLORS["outer"],
                edgecolor=COLORS["grid"],
                lw=0.6,
                alpha=0.42,
                zorder=1.5,
            )
        )
    for cell in step.inner_cells:
        ax_shape.add_patch(
            Rectangle(
                (cell.x0, cell.y0),
                cell.x1 - cell.x0,
                cell.y1 - cell.y0,
                facecolor=COLORS["inner"],
                edgecolor=COLORS["grid"],
                lw=0.4,
                alpha=0.82,
                zorder=2,
            )
        )

    ax_shape.plot(outer[:, 0], outer[:, 1], color=COLORS["region_edge"], lw=2.2, zorder=3)
    for hole in holes:
        ax_shape.plot(hole[:, 0], hole[:, 1], color=COLORS["region_edge"], lw=1.8, zorder=3)

    ax_shape.set_xlim(0, 1)
    ax_shape.set_ylim(0, 1)
    ax_shape.set_aspect("equal")
    ax_shape.set_xlabel("x", fontsize=18)
    ax_shape.set_ylabel("y", fontsize=18)
    ax_shape.set_title("穴あき図形と内外近似の長方形", fontsize=16, pad=12)

    levels = [item.level for item in steps]
    inner_values = [item.inner_area for item in steps]
    outer_values = [item.outer_area for item in steps]
    boundary_counts = [len(item.boundary_cells) for item in steps]
    shown = step.level + 1

    ax_area.plot(levels[:shown], inner_values[:shown], color=COLORS["inner"], marker="o", lw=2.4, label="内側近似")
    ax_area.plot(levels[:shown], outer_values[:shown], color=COLORS["outer"], marker="o", lw=2.4, label="外側近似")
    ax_area.axhline(exact_area, color=COLORS["region_edge"], lw=1.8, ls="--", label="真の面積")
    ax_area.fill_between(levels[:shown], inner_values[:shown], outer_values[:shown], color=COLORS["gap"], alpha=0.12)
    ax_area.set_xticks(levels)
    ax_area.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax_area.set_xlim(min(levels) - 0.2, max(levels) + 0.2)
    margin = max(0.015, 0.18 * (max(outer_values) - min(inner_values)))
    ax_area.set_ylim(min(inner_values) - margin, max(outer_values) + margin)
    ax_area.set_xlabel("細分段階")
    ax_area.set_ylabel("面積")
    ax_area.set_title("内外近似の収束", fontsize=16, pad=12)
    ax_area.legend(loc="lower right", frameon=False)
    ax_area.text(
        0.03,
        0.97,
        "\n".join(
            [
                rf"分割段階: $P_{{{step.level}}}$",
                rf"境界セル数 = {boundary_counts[step.level]}",
                rf"内側近似 = {step.inner_area:.4f}",
                rf"外側近似 = {step.outer_area:.4f}",
                rf"差 = {step.outer_area - step.inner_area:.4f}",
            ]
        ),
        transform=ax_area.transAxes,
        va="top",
        fontsize=11,
        bbox=dict(boxstyle="round, pad=0.35", facecolor="white", edgecolor=COLORS["grid"]),
    )

    fig.suptitle("Jordan 測度: 穴の境界も含めて外側近似と内側近似が収束する", fontsize=18, y=0.96)
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def render_animation(
    outdir: Path,
    *,
    seed: int,
    levels: int,
    holes: int,
    resolution: int,
    duration: float,
) -> None:
    if outdir.exists():
        shutil.rmtree(outdir)
    ensure_dir(outdir)
    frames_dir = outdir / "frames"
    gif_dir = outdir / "gif"
    ensure_dir(frames_dir)
    ensure_dir(gif_dir)

    outer, holes_curves, exact_area = build_region(seed, holes)
    mask, xx, yy = build_mask(outer, holes_curves, resolution)
    steps = build_steps(mask, levels, seed)
    dots_x, dots_y = interior_dots(mask, xx, yy, seed=seed + 100)

    frame_paths = []
    for step in steps:
        frame_path = frames_dir / f"frame_{step.level:03d}.png"
        draw_step(step, steps, outer, holes_curves, exact_area, dots_x, dots_y, frame_path)
        frame_paths.append(frame_path)

    gif_path = gif_dir / "jordan_holes_adaptive.gif"
    frames = [Image.open(path).convert("P", palette=Image.ADAPTIVE) for path in frame_paths]
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=GIF_LOOP,
        disposal=2,
    )
    print(f"Saved GIF to: {gif_path.resolve()}")
    print(f"Saved frames to: {frames_dir.resolve()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an adaptive Jordan area animation for regions with holes.")
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--levels", type=int, default=10)
    parser.add_argument("--holes", type=int, default=4, choices=[3, 4])
    parser.add_argument("--resolution", type=int, default=360)
    parser.add_argument("--duration", type=float, default=1.0)
    parser.add_argument("--outdir", type=Path, default=Path("figures/measure/animations/jordan_holes_adaptive"))
    return parser.parse_args()


def main() -> None:
    setup_style()
    args = parse_args()
    render_animation(
        args.outdir,
        seed=args.seed,
        levels=args.levels,
        holes=args.holes,
        resolution=args.resolution,
        duration=args.duration,
    )


if __name__ == "__main__":
    main()
