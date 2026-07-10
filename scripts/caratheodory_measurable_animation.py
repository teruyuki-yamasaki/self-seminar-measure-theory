#!/usr/bin/env python3
"""Visualize Carathéodory measurability with three overlapping test sets."""

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
    "e_edge": "#8d4f16",
    "green": "#4c9f70",
    "green_edge": "#2c6e49",
    "orange": "#f0b45a",
    "orange_edge": "#a85b00",
    "overlap": "#d95f5f",
    "grid": "#c8d1dc",
}

OUTDIR = Path("figures/measure/animations/caratheodory_measurable")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "caratheodory_measurable.gif"

LEVELS = 10
FRAME_DURATION = 1.0
GIF_LOOP = 0
DISPLAY_RESOLUTION = 280
CLASSIFY_RESOLUTION = 240


@dataclass(frozen=True)
class Cell:
    x0: float
    x1: float
    y0: float
    y1: float


@dataclass
class Step:
    level: int
    green_cells: list[Cell]
    orange_cells: list[Cell]
    overlap_cells: list[Cell]
    green_cover_area: float
    orange_cover_area: float
    overlap_area: float
    rhs_gap: float


@dataclass(frozen=True)
class Pattern:
    name: str
    e_curve: np.ndarray
    s_mask: np.ndarray
    e_mask: np.ndarray
    a_mask: np.ndarray
    b_mask: np.ndarray
    display_a: np.ndarray
    display_b: np.ndarray
    e_area: float
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
    radius = 0.34 * (
        1.0
        + 0.25 * np.cos(5 * theta + phase)
        + 0.10 * np.cos(3 * theta - 0.7 * phase)
        + 0.06 * np.sin(7 * theta + 0.5 * phase)
    )
    radius = np.clip(radius, 0.16, None)
    x = 0.5 + 1.06 * radius * np.cos(theta)
    y = 0.5 + 0.92 * radius * np.sin(theta)
    points = np.column_stack([x, y])
    return np.vstack([points, points[0]])


def star_curve(
    center: tuple[float, float],
    base_radius: float,
    angle_deg: float,
    *,
    n_arms: int,
    arm_strength: float,
    skew: float,
    n_points: int = 480,
) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    phi = theta + np.deg2rad(angle_deg)
    radius = base_radius * (
        1.0
        + arm_strength * np.cos(n_arms * phi)
        + 0.12 * np.cos((n_arms - 1) * phi + skew)
        + 0.08 * np.sin((n_arms + 2) * phi - 0.6 * skew)
    )
    radius = np.clip(radius, 0.42 * base_radius, None)
    x_local = 1.06 * radius * np.cos(theta)
    y_local = 0.88 * radius * np.sin(theta)
    ct = np.cos(np.deg2rad(angle_deg))
    st = np.sin(np.deg2rad(angle_deg))
    xr = center[0] + ct * x_local - st * y_local
    yr = center[1] + st * x_local + ct * y_local
    pts = np.column_stack([xr, yr])
    return np.vstack([pts, pts[0]])


def ellipse_curve(center: tuple[float, float], axes: tuple[float, float], angle_deg: float, n_points: int = 420) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    ct = np.cos(np.deg2rad(angle_deg))
    st = np.sin(np.deg2rad(angle_deg))
    x = axes[0] * np.cos(theta)
    y = axes[1] * np.sin(theta)
    xr = center[0] + ct * x - st * y
    yr = center[1] + st * x + ct * y
    pts = np.column_stack([xr, yr])
    return np.vstack([pts, pts[0]])


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


def initial_cell(e_mask: np.ndarray) -> Cell:
    ys, xs = np.where(e_mask)
    resolution = e_mask.shape[0]
    pad = 3
    x0 = max(0, xs.min() - pad) / resolution
    x1 = min(resolution, xs.max() + pad + 1) / resolution
    y0 = max(0, ys.min() - pad) / resolution
    y1 = min(resolution, ys.max() + pad + 1) / resolution
    return Cell(x0, x1, y0, y1)


def build_steps(a_mask: np.ndarray, b_mask: np.ndarray, e_mask: np.ndarray, levels: int, seed: int) -> list[Step]:
    rng = np.random.default_rng(seed)
    active_cells = [initial_cell(e_mask)]
    steps: list[Step] = []
    e_area = float(np.mean(e_mask))

    for level in range(levels + 1):
        green_cells: list[Cell] = []
        orange_cells: list[Cell] = []
        overlap_cells: list[Cell] = []
        next_cells: list[Cell] = []

        for cell in active_cells:
            view_a = cell_mask_view(cell, a_mask)
            view_b = cell_mask_view(cell, b_mask)
            any_a = bool(np.any(view_a))
            any_b = bool(np.any(view_b))

            if not any_a and not any_b:
                continue

            if any_a and any_b:
                overlap_cells.append(cell)
                if level < levels:
                    next_cells.extend(subdivide(cell, rng))
                else:
                    next_cells.append(cell)
                continue

            if any_a:
                green_cells.append(cell)
                if level < levels and not bool(np.all(view_a)):
                    next_cells.extend(subdivide(cell, rng))
                else:
                    next_cells.append(cell)
                continue

            orange_cells.append(cell)
            if level < levels and not bool(np.all(view_b)):
                next_cells.extend(subdivide(cell, rng))
            else:
                next_cells.append(cell)

        overlap_area = sum(area(cell) for cell in overlap_cells)
        green_cover = sum(area(cell) for cell in green_cells) + overlap_area
        orange_cover = sum(area(cell) for cell in orange_cells) + overlap_area
        steps.append(
            Step(
                level=level,
                green_cells=green_cells,
                orange_cells=orange_cells,
                overlap_cells=overlap_cells,
                green_cover_area=green_cover,
                orange_cover_area=orange_cover,
                overlap_area=overlap_area,
                rhs_gap=(green_cover + orange_cover - e_area) / e_area,
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


def draw_pattern_top(ax: plt.Axes, s_curve: np.ndarray, pattern: Pattern) -> None:
    ax.imshow(patterned_rgba(pattern.display_b, COLORS["orange"], "dots", 0.72), origin="lower", extent=(0, 1, 0, 1), interpolation="nearest")
    ax.imshow(patterned_rgba(pattern.display_a, COLORS["green"], "hatch", 0.6), origin="lower", extent=(0, 1, 0, 1), interpolation="nearest")
    ax.plot(s_curve[:, 0], s_curve[:, 1], color=COLORS["s_edge"], lw=2.0)
    ax.plot(pattern.e_curve[:, 0], pattern.e_curve[:, 1], color=COLORS["e_edge"], lw=1.9, ls=(0, (5, 3)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(pattern.name, fontsize=14, pad=8)


def draw_cells(ax: plt.Axes, cells: list[Cell], face: str, edge: str, alpha: float) -> None:
    for cell in cells:
        ax.add_patch(
            Rectangle(
                (cell.x0, cell.y0),
                cell.x1 - cell.x0,
                cell.y1 - cell.y0,
                facecolor=face,
                edgecolor=edge,
                lw=0.7,
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


def draw_pattern_middle(ax: plt.Axes, s_curve: np.ndarray, pattern: Pattern, step: Step) -> None:
    ax.imshow(patterned_rgba(pattern.display_b, COLORS["orange"], "dots", 0.12), origin="lower", extent=(0, 1, 0, 1), interpolation="nearest")
    ax.imshow(patterned_rgba(pattern.display_a, COLORS["green"], "hatch", 0.14), origin="lower", extent=(0, 1, 0, 1), interpolation="nearest")

    draw_cells(ax, step.orange_cells, COLORS["orange"], COLORS["orange_edge"], 0.28)
    draw_cells(ax, step.green_cells, COLORS["green"], COLORS["green_edge"], 0.34)
    draw_cells(ax, step.overlap_cells, COLORS["orange"], COLORS["orange_edge"], 0.22)
    draw_cells(ax, step.overlap_cells, COLORS["green"], COLORS["green_edge"], 0.26)
    green_mask = cells_to_mask(step.green_cells + step.overlap_cells, DISPLAY_RESOLUTION)
    orange_mask = cells_to_mask(step.orange_cells + step.overlap_cells, DISPLAY_RESOLUTION)
    draw_mask_outline(ax, green_mask, COLORS["green_edge"], 2.8)
    draw_mask_outline(ax, orange_mask, COLORS["orange_edge"], 2.8)

    ax.plot(s_curve[:, 0], s_curve[:, 1], color=COLORS["s_edge"], lw=1.7)
    ax.plot(pattern.e_curve[:, 0], pattern.e_curve[:, 1], color=COLORS["e_edge"], lw=1.6, ls=(0, (5, 3)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(pattern.name, fontsize=12, pad=8)


def draw_pattern_graph(ax: plt.Axes, pattern: Pattern, level: int) -> None:
    steps = pattern.steps[: level + 1]
    xs = list(range(len(steps)))
    green = np.array([step.green_cover_area / pattern.e_area for step in steps])
    orange = np.array([step.orange_cover_area / pattern.e_area for step in steps])
    orange_lower = np.maximum(0.0, 1.0 - orange)
    overlap_upper = np.minimum(green, 1.0)
    band_thickness = np.maximum(0.0, overlap_upper - orange_lower)

    ax.fill_between(xs, 0.0, green, color=COLORS["green"], alpha=0.28, label=r"$E\cap S$ 被覆")
    ax.plot(xs, green, color=COLORS["green_edge"], lw=2.2, marker="o")

    ax.fill_between(xs, orange_lower, 1.0, color=COLORS["orange"], alpha=0.28, label=r"$E\cap S^c$ 被覆")
    ax.plot(xs, orange_lower, color=COLORS["orange_edge"], lw=2.2, marker="o")

    mask = overlap_upper > orange_lower
    if np.any(mask):
        ax.fill_between(xs, orange_lower, overlap_upper, where=mask, color=COLORS["overlap"], alpha=0.24, label="重なり帯")

    ax.set_xlim(-0.15, LEVELS + 0.15)
    ax.set_ylim(0.0, 1.08)
    ax.set_xticks(range(0, LEVELS + 1))
    ax.set_yticks(np.linspace(0.0, 1.0, 6))
    ax.set_title(rf"正規化被覆の収束  |  重なり帯 {band_thickness[-1]:.4f}", fontsize=12, pad=8)
    ax.set_xlabel("段階")
    ax.set_ylabel("正規化面積")
    ax.grid(axis="y", color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax.legend(loc="upper right", fontsize=9, frameon=False)


def build_patterns(s_curve: np.ndarray) -> list[Pattern]:
    e_specs = [
        ("重なり A", (0.78, 0.55), (0.29, 0.22), 10.0),
        ("重なり B", (0.40, 0.47), (0.56, 0.20), 36.0),
        ("重なり C", (0.68, 0.74), (0.33, 0.23), -14.0),
    ]

    s_mask = build_mask(s_curve, CLASSIFY_RESOLUTION)
    display_s = build_mask(s_curve, DISPLAY_RESOLUTION)
    patterns: list[Pattern] = []

    for idx, (name, center, axes, angle) in enumerate(e_specs):
        curve = ellipse_curve(center, axes, angle)
        e_mask = build_mask(curve, CLASSIFY_RESOLUTION)
        display_e = build_mask(curve, DISPLAY_RESOLUTION)
        a_mask = s_mask & e_mask
        b_mask = (~s_mask) & e_mask

        if not np.any(a_mask) or not np.any(b_mask):
            raise RuntimeError(f"{name} does not create both overlap parts.")

        steps = build_steps(a_mask, b_mask, e_mask, LEVELS, seed=80 + idx)
        display_a = display_s & display_e
        display_b = (~display_s) & display_e
        e_area = float(np.mean(e_mask))
        patterns.append(
            Pattern(
                name=name,
                e_curve=curve,
                s_mask=s_mask,
                e_mask=e_mask,
                a_mask=a_mask,
                b_mask=b_mask,
                display_a=display_a,
                display_b=display_b,
                e_area=e_area,
                steps=steps,
            )
        )

    return patterns


def draw_intro_frame(save_path: Path, s_curve: np.ndarray, patterns: list[Pattern]) -> None:
    fig = plt.figure(figsize=(16.8, 10.8))
    axes_top = [fig.add_axes([0.02 + 0.327 * i, 0.49, 0.31, 0.41]) for i in range(3)]
    axes_bottom = [fig.add_axes([0.04 + 0.32 * i, 0.09, 0.29, 0.28]) for i in range(3)]

    for ax, pattern in zip(axes_top, patterns):
        draw_pattern_top(ax, s_curve, pattern)

    for ax in axes_bottom:
        ax.set_xlim(-0.15, LEVELS + 0.15)
        ax.set_ylim(0.0, 1.08)
        ax.set_xticks(range(0, LEVELS + 1))
        ax.set_yticks(np.linspace(0.0, 1.0, 6))
        ax.set_xlabel("段階")
        ax.set_ylabel("正規化面積")
        ax.grid(axis="y", color=COLORS["grid"], lw=0.8, alpha=0.7)
        ax.set_title("正規化被覆の収束  |  導入", fontsize=12, pad=8)

    fig.suptitle(
        rf"Carathéodory の可測条件の直観  $\Gamma(E)=\Gamma(E\cap S)+\Gamma(E\cap S^c)$",
        fontsize=21,
        y=0.95,
    )
    fig.text(0.5, 0.445, r"導入: ヒトデ型の $S$ と, それに交わる 3 つの楕円形 $E$ を考える", ha="center", fontsize=15)
    fig.text(0.5, 0.03, r"斜線が $E\cap S$, 点々が $E\cap S^c$. 下段は緑を 0 から, 橙を 1 から描き, 重なり帯の縮小を見る.", ha="center", fontsize=14, color=COLORS["muted"])
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def draw_frame(save_path: Path, s_curve: np.ndarray, patterns: list[Pattern], level: int) -> None:
    fig = plt.figure(figsize=(16.8, 10.8))
    axes_top = [fig.add_axes([0.02 + 0.327 * i, 0.49, 0.31, 0.41]) for i in range(3)]
    axes_bottom = [fig.add_axes([0.04 + 0.32 * i, 0.09, 0.29, 0.28]) for i in range(3)]

    for ax, pattern in zip(axes_top, patterns):
        draw_pattern_middle(ax, s_curve, pattern, pattern.steps[level])

    for ax, pattern in zip(axes_bottom, patterns):
        draw_pattern_graph(ax, pattern, level)

    fig.text(0.5, 0.445, r"上段: $E\cap S$ の外側近似を緑, $E\cap S^c$ の外側近似を橙の長方形で表示", ha="center", fontsize=13, color=COLORS["muted"])
    fig.suptitle(
        rf"Carathéodory の可測条件の直観  $\Gamma(E)=\Gamma(E\cap S)+\Gamma(E\cap S^c)$",
        fontsize=20,
        y=0.96,
    )
    fig.text(
        0.5,
        0.03,
        rf"段階 {level}: 下段では面積 $m(E)=1$ に正規化し, 緑を 0 から, 橙を 1 から描いて重なり帯が 0 に近づく様子を示す",
        ha="center",
        fontsize=14,
    )
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    s_curve = random_closed_curve(13)
    patterns = build_patterns(s_curve)

    draw_intro_frame(FRAMES_DIR / "frame_000.png", s_curve, patterns)

    for level in range(LEVELS + 1):
        draw_frame(FRAMES_DIR / f"frame_{level + 1:03d}.png", s_curve, patterns, level)

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
