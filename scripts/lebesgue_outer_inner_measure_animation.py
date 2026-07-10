#!/usr/bin/env python3
"""Visualize Lebesgue outer and inner measure approximations on a planar region."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

import matplotlib
from PIL import Image

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path as MplPath
from matplotlib.patches import Rectangle


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "s_edge": "#19486a",
    "j_edge": "#8d4f16",
    "green": "#69a7ff",
    "green_edge": "#2458a6",
    "orange": "#f5b6b6",
    "orange_edge": "#d46a6a",
    "orange_outline": "#d94f4f",
    "overlap": "#c63d7f",
    "grid": "#c8d1dc",
}

OUTDIR = Path("figures/measure/animations/lebesgue_outer_inner_measure")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "lebesgue_outer_inner_measure.gif"

LEVELS = 10
FRAME_DURATION = 1.0
GIF_LOOP = 0
DISPLAY_RESOLUTION = 320
CLASSIFY_RESOLUTION = 260


@dataclass(frozen=True)
class Cell:
    x0: float
    x1: float
    y0: float
    y1: float


@dataclass
class Step:
    level: int
    s_only_cells: list[Cell]
    c_only_cells: list[Cell]
    overlap_cells: list[Cell]
    outer_s_area: float
    outer_c_area: float
    inner_s_area: float
    overlap_area: float


@dataclass(frozen=True)
class RegionData:
    s_curve: np.ndarray
    j_rect: Cell
    s_mask: np.ndarray
    c_mask: np.ndarray
    display_j: np.ndarray
    display_s: np.ndarray
    display_c: np.ndarray
    j_area: float
    steps: list[Step]


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


def random_closed_curve(seed: int, n_points: int = 720) -> np.ndarray:
    rng = np.random.default_rng(seed)
    theta = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    phase = rng.uniform(0.0, 2.0 * np.pi)
    radius = 0.35 * (
        1.0
        + 0.20 * np.cos(5 * theta + phase)
        + 0.09 * np.cos(3 * theta - 0.7 * phase)
        + 0.08 * np.sin(7 * theta + 0.5 * phase)
    )
    radius = np.clip(radius, 0.18, None)
    x = 0.50 + 0.98 * radius * np.cos(theta)
    y = 0.50 + 0.84 * radius * np.sin(theta)
    points = np.column_stack([x, y])
    return np.vstack([points, points[0]])


def build_mask(curve: np.ndarray, resolution: int) -> np.ndarray:
    xs = np.linspace(0.0, 1.0, resolution, endpoint=False) + 0.5 / resolution
    ys = np.linspace(0.0, 1.0, resolution, endpoint=False) + 0.5 / resolution
    xx, yy = np.meshgrid(xs, ys)
    points = np.column_stack([xx.ravel(), yy.ravel()])
    return MplPath(curve).contains_points(points).reshape(resolution, resolution)


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


def area(cell: Cell) -> float:
    return (cell.x1 - cell.x0) * (cell.y1 - cell.y0)


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


def covering_rect(mask: np.ndarray, pad: int = 5) -> Cell:
    ys, xs = np.where(mask)
    resolution = mask.shape[0]
    x0 = max(0, xs.min() - pad) / resolution
    x1 = min(resolution, xs.max() + pad + 1) / resolution
    y0 = max(0, ys.min() - pad) / resolution
    y1 = min(resolution, ys.max() + pad + 1) / resolution
    return Cell(x0, x1, y0, y1)


def rect_mask(mask: np.ndarray, rect: Cell) -> np.ndarray:
    resolution = mask.shape[0]
    xs = np.linspace(0.0, 1.0, resolution, endpoint=False) + 0.5 / resolution
    ys = np.linspace(0.0, 1.0, resolution, endpoint=False) + 0.5 / resolution
    xx, yy = np.meshgrid(xs, ys)
    return (rect.x0 <= xx) & (xx <= rect.x1) & (rect.y0 <= yy) & (yy <= rect.y1)


def build_steps(s_mask: np.ndarray, c_mask: np.ndarray, j_rect: Cell, levels: int, seed: int) -> list[Step]:
    rng = np.random.default_rng(seed)
    active_cells = [j_rect]
    steps: list[Step] = []
    j_area = area(j_rect)

    for level in range(levels + 1):
        s_only_cells: list[Cell] = []
        c_only_cells: list[Cell] = []
        overlap_cells: list[Cell] = []
        next_cells: list[Cell] = []

        for cell in active_cells:
            view_s = cell_mask_view(cell, s_mask)
            view_c = cell_mask_view(cell, c_mask)
            any_s = bool(np.any(view_s))
            any_c = bool(np.any(view_c))

            if any_s and any_c:
                overlap_cells.append(cell)
                if level < levels:
                    next_cells.extend(subdivide(cell, rng))
                else:
                    next_cells.append(cell)
                continue

            if any_s:
                s_only_cells.append(cell)
                next_cells.append(cell)
                continue

            if any_c:
                c_only_cells.append(cell)
                next_cells.append(cell)

        overlap_area = sum(area(cell) for cell in overlap_cells)
        outer_s_area = sum(area(cell) for cell in s_only_cells) + overlap_area
        outer_c_area = sum(area(cell) for cell in c_only_cells) + overlap_area
        inner_s_area = j_area - outer_c_area
        steps.append(
            Step(
                level=level,
                s_only_cells=s_only_cells,
                c_only_cells=c_only_cells,
                overlap_cells=overlap_cells,
                outer_s_area=outer_s_area,
                outer_c_area=outer_c_area,
                inner_s_area=inner_s_area,
                overlap_area=outer_s_area - inner_s_area,
            )
        )
        active_cells = next_cells

    return steps


def patterned_rgba(mask: np.ndarray, color: str, mode: str, alpha: float) -> np.ndarray:
    rgb = np.array(matplotlib.colors.to_rgb(color))
    h, w = mask.shape
    yy, xx = np.indices((h, w))
    if mode == "hatch":
        pattern = ((xx + yy) % 12) < 3
    else:
        pattern = ((xx % 10 - 5) ** 2 + (yy % 10 - 5) ** 2) <= 5
    active = mask & pattern
    rgba = np.zeros((h, w, 4), dtype=float)
    rgba[..., :3] = rgb
    rgba[..., 3] = active.astype(float) * alpha
    return rgba


def draw_region_top(ax: plt.Axes, data: RegionData) -> None:
    ax.imshow(patterned_rgba(data.display_c, COLORS["orange"], "dots", 0.70), origin="lower", extent=(0, 1, 0, 1), interpolation="nearest")
    ax.imshow(patterned_rgba(data.display_s, COLORS["green"], "hatch", 0.58), origin="lower", extent=(0, 1, 0, 1), interpolation="nearest")
    ax.add_patch(
        Rectangle(
            (data.j_rect.x0, data.j_rect.y0),
            data.j_rect.x1 - data.j_rect.x0,
            data.j_rect.y1 - data.j_rect.y0,
            fill=False,
            edgecolor=COLORS["j_edge"],
            lw=2.0,
            ls=(0, (5, 3)),
        )
    )
    ax.plot(data.s_curve[:, 0], data.s_curve[:, 1], color=COLORS["s_edge"], lw=2.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(r"集合 $A$ と被覆区間 $I$", fontsize=16, pad=8)


def draw_cells(ax: plt.Axes, cells: list[Cell], face: str, edge: str, alpha: float) -> None:
    for cell in cells:
        ax.add_patch(
            Rectangle(
                (cell.x0, cell.y0),
                cell.x1 - cell.x0,
                cell.y1 - cell.y0,
                facecolor=face,
                edgecolor=edge,
                lw=1.25,
                alpha=alpha,
            )
        )


def cells_to_mask(cells: list[Cell], resolution: int) -> np.ndarray:
    mask = np.zeros((resolution, resolution), dtype=bool)
    for cell in cells:
        ix0 = edge_to_index(cell.x0, resolution)
        ix1 = edge_to_index(cell.x1, resolution)
        iy0 = edge_to_index(cell.y0, resolution)
        iy1 = edge_to_index(cell.y1, resolution)
        if ix1 <= ix0:
            ix1 = min(resolution, ix0 + 1)
        if iy1 <= iy0:
            iy1 = min(resolution, iy0 + 1)
        mask[iy0:iy1, ix0:ix1] = True
    return mask


def draw_mask_outline(ax: plt.Axes, mask: np.ndarray, color: str, lw: float) -> None:
    if not np.any(mask):
        return
    xs = np.linspace(0.0, 1.0, mask.shape[1], endpoint=False) + 0.5 / mask.shape[1]
    ys = np.linspace(0.0, 1.0, mask.shape[0], endpoint=False) + 0.5 / mask.shape[0]
    ax.contour(xs, ys, mask.astype(float), levels=[0.5], colors=[color], linewidths=lw, zorder=3.6)


def draw_region_middle(ax: plt.Axes, data: RegionData, step: Step) -> None:
    ax.imshow(patterned_rgba(data.display_c, COLORS["orange"], "dots", 0.12), origin="lower", extent=(0, 1, 0, 1), interpolation="nearest")
    ax.imshow(patterned_rgba(data.display_s, COLORS["green"], "hatch", 0.14), origin="lower", extent=(0, 1, 0, 1), interpolation="nearest")
    draw_cells(ax, step.c_only_cells, COLORS["orange"], COLORS["orange_edge"], 0.28)
    draw_cells(ax, step.s_only_cells, COLORS["green"], COLORS["green_edge"], 0.34)
    draw_cells(ax, step.overlap_cells, COLORS["orange"], COLORS["orange_edge"], 0.22)
    draw_cells(ax, step.overlap_cells, COLORS["green"], COLORS["green_edge"], 0.26)
    s_outer_mask = cells_to_mask(step.s_only_cells + step.overlap_cells, DISPLAY_RESOLUTION)
    c_outer_mask = cells_to_mask(step.c_only_cells + step.overlap_cells, DISPLAY_RESOLUTION)
    s_inner_mask = data.display_j & (~c_outer_mask)
    draw_mask_outline(ax, s_outer_mask, COLORS["green_edge"], 3.0)
    draw_mask_outline(ax, s_inner_mask, COLORS["orange_outline"], 3.0)
    ax.add_patch(
        Rectangle(
            (data.j_rect.x0, data.j_rect.y0),
            data.j_rect.x1 - data.j_rect.x0,
            data.j_rect.y1 - data.j_rect.y0,
            fill=False,
            edgecolor=COLORS["j_edge"],
            lw=1.8,
            ls=(0, (5, 3)),
        )
    )
    ax.plot(data.s_curve[:, 0], data.s_curve[:, 1], color=COLORS["s_edge"], lw=1.7)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(rf"段階 {step.level}: $A$ と $I\cap A^c$ の外側被覆", fontsize=15, pad=8)


def draw_graph(ax: plt.Axes, data: RegionData, level: int) -> None:
    steps = data.steps[: level + 1]
    xs = list(range(len(steps)))
    outer_s = np.array([step.outer_s_area / data.j_area for step in steps])
    inner_s = np.array([step.inner_s_area / data.j_area for step in steps])
    orange_lower = inner_s
    overlap_upper = outer_s
    band_thickness = np.maximum(0.0, overlap_upper - orange_lower)

    ax.fill_between(xs, 0.0, outer_s, color=COLORS["green"], alpha=0.30, label=r"$\mu^*(A)$ の外側近似")
    ax.plot(xs, outer_s, color=COLORS["green_edge"], lw=2.2, marker="o")

    ax.fill_between(xs, orange_lower, 1.0, color=COLORS["orange"], alpha=0.24, label=r"$m(I)-\mu^*(I\cap A^c)$")
    ax.plot(xs, orange_lower, color=COLORS["orange_edge"], lw=2.2, marker="o")

    mask = overlap_upper > orange_lower
    if np.any(mask):
        ax.fill_between(xs, orange_lower, overlap_upper, where=mask, color=COLORS["overlap"], alpha=0.40, label="重なり帯")

    ax.set_xlim(-0.15, LEVELS + 0.15)
    ax.set_ylim(0.0, 1.08)
    ax.set_xticks(range(0, LEVELS + 1))
    ax.set_yticks(np.linspace(0.0, 1.0, 6))
    ax.set_xlabel("段階")
    ax.set_ylabel(r"面積 / $m(I)$")
    ax.set_title(rf"外測度と内測度の近似  |  重なり帯 {band_thickness[-1]:.4f}", fontsize=15, pad=8)
    ax.grid(axis="y", color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax.legend(loc="upper right", fontsize=10, frameon=False)


def build_region(seed: int) -> RegionData:
    s_curve = random_closed_curve(seed)
    s_mask = build_mask(s_curve, CLASSIFY_RESOLUTION)
    j_rect = covering_rect(s_mask)
    j_mask = rect_mask(s_mask, j_rect)
    c_mask = j_mask & (~s_mask)

    if not np.any(c_mask):
        raise RuntimeError("Covering rectangle J must contain some complement region.")

    display_s = build_mask(s_curve, DISPLAY_RESOLUTION)
    display_j = rect_mask(display_s, Cell(j_rect.x0, j_rect.x1, j_rect.y0, j_rect.y1))
    display_c = display_j & (~display_s)
    steps = build_steps(s_mask, c_mask, j_rect, LEVELS, seed + 100)
    return RegionData(
        s_curve=s_curve,
        j_rect=j_rect,
        s_mask=s_mask,
        c_mask=c_mask,
        display_j=display_j,
        display_s=display_s & display_j,
        display_c=display_c,
        j_area=area(j_rect),
        steps=steps,
    )


def draw_intro_frame(save_path: Path, data: RegionData) -> None:
    fig = plt.figure(figsize=(14.2, 9.4))
    ax_top = fig.add_axes([0.08, 0.18, 0.40, 0.60])
    ax_graph = fig.add_axes([0.56, 0.18, 0.36, 0.60])

    draw_region_top(ax_top, data)
    ax_graph.set_xlim(-0.15, LEVELS + 0.15)
    ax_graph.set_ylim(0.0, 1.08)
    ax_graph.set_xticks(range(0, LEVELS + 1))
    ax_graph.set_yticks(np.linspace(0.0, 1.0, 6))
    ax_graph.set_xlabel("段階")
    ax_graph.set_ylabel(r"面積 / $m(I)$")
    ax_graph.grid(axis="y", color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_graph.set_title("外測度と内測度の近似  |  導入", fontsize=15, pad=8)

    fig.suptitle(
        r"Lebesgue 外測度と内測度  $\mu_*(A; I)=m(I)-\mu^*(I\cap A^c)$",
        fontsize=21,
        y=0.95,
    )
    fig.text(
        0.50,
        0.06,
        r"緑は $A$ の外側近似, 橙は $I\cap A^c$ の外側近似. 下段では $\mu_*(A; I)=m(I)-\mu^*(I\cap A^c)$ と $\mu^*(A)$ の重なり帯を見る.",
        ha="center",
        fontsize=14,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def draw_frame(save_path: Path, data: RegionData, level: int) -> None:
    fig = plt.figure(figsize=(14.2, 9.4))
    ax_top = fig.add_axes([0.08, 0.18, 0.40, 0.60])
    ax_graph = fig.add_axes([0.56, 0.18, 0.36, 0.60])

    draw_region_middle(ax_top, data, data.steps[level])
    draw_graph(ax_graph, data, level)

    fig.suptitle(
        r"Lebesgue 外測度と内測度  $\mu_*(A; I)=m(I)-\mu^*(I\cap A^c)$",
        fontsize=21,
        y=0.95,
    )
    fig.text(
        0.50,
        0.06,
        rf"段階 {level}: 右では緑が $\mu^*(A)$ の上からの近似, 橙の下端が $\mu_*(A; I)=m(I)-\mu^*(I\cap A^c)$ の下からの近似で, 重なり帯が 0 に近づく.",
        ha="center",
        fontsize=14,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()
    data = build_region(seed=19)

    draw_intro_frame(FRAMES_DIR / "frame_000.png", data)
    for level in range(LEVELS + 1):
        draw_frame(FRAMES_DIR / f"frame_{level + 1:03d}.png", data, level)

    frame_paths = sorted(FRAMES_DIR.glob("frame_*.png"))
    frames = [Image.open(path).convert("P", palette=Image.Palette.ADAPTIVE) for path in frame_paths]
    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=int(FRAME_DURATION * 1000),
        loop=GIF_LOOP,
        disposal=2,
    )
    print(f"Saved GIF to: {GIF_PATH.resolve()}")
    print(f"Saved frames to: {FRAMES_DIR.resolve()}")


if __name__ == "__main__":
    build_animation()
