#!/usr/bin/env python3
"""Forward zoom animation showing density of rational points in nested squares."""

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
from matplotlib.patches import Rectangle


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#c8d1dc",
    "point": "#2458a6",
    "square": "#d94f4f",
}

STAGE_COUNT = 1
SHRINK_FRAMES = 5
ZOOM_FRAMES = 10
FRAME_DURATION = 0.15
GIF_LOOP = 0
VISIBLE_DIVISIONS = 6


@dataclass(frozen=True)
class Square:
    x0: float
    x1: float
    y0: float
    y1: float

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def center(self) -> tuple[float, float]:
        return (0.5 * (self.x0 + self.x1), 0.5 * (self.y0 + self.y1))


@dataclass(frozen=True)
class Variant:
    name: str
    stem: str
    centered: bool
    divisions: int
    point_size_current: float
    point_size_next: float
    shrink_fraction: float
    title: str
    description: str


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


def ensure_dirs(outdir: Path) -> tuple[Path, Path]:
    if outdir.exists():
        shutil.rmtree(outdir)
    frames_dir = outdir / "frames"
    gif_dir = outdir / "gif"
    frames_dir.mkdir(parents=True, exist_ok=True)
    gif_dir.mkdir(parents=True, exist_ok=True)
    return frames_dir, gif_dir


def ease_in_out(t: float) -> float:
    return 3.0 * t * t - 2.0 * t * t * t


def interpolate_square(a: Square, b: Square, t: float) -> Square:
    return Square(
        (1.0 - t) * a.x0 + t * b.x0,
        (1.0 - t) * a.x1 + t * b.x1,
        (1.0 - t) * a.y0 + t * b.y0,
        (1.0 - t) * a.y1 + t * b.y1,
    )


def initial_view() -> Square:
    return Square(0.0, 1.0, 0.0, 1.0)


def centered_square(view: Square, side_fraction: float) -> Square:
    side = side_fraction * view.width
    cx, cy = view.center
    half = 0.5 * side
    return Square(cx - half, cx + half, cy - half, cy + half)


def grid_points(view: Square, divisions: int, *, centered: bool) -> np.ndarray:
    step = view.width / divisions
    if centered:
        offsets = np.arange(divisions) - 0.5 * (divisions - 1)
        cx, cy = view.center
        xs = cx + offsets * step
        ys = cy + offsets * step
    else:
        xs = view.x0 + 0.5 * step + np.arange(divisions) * step
        ys = view.y0 + 0.5 * step + np.arange(divisions) * step
    xx, yy = np.meshgrid(xs, ys)
    return np.column_stack([xx.ravel(), yy.ravel()])


def lattice_points_with_step(view: Square, *, step: float, anchor_x: float, anchor_y: float) -> np.ndarray:
    eps = 1e-9 * max(view.width, 1.0)

    start_ix = int(np.ceil((view.x0 - anchor_x - eps) / step))
    end_ix = int(np.floor((view.x1 - anchor_x + eps) / step))
    start_iy = int(np.ceil((view.y0 - anchor_y - eps) / step))
    end_iy = int(np.floor((view.y1 - anchor_y + eps) / step))

    xs = anchor_x + np.arange(start_ix, end_ix + 1) * step
    ys = anchor_y + np.arange(start_iy, end_iy + 1) * step
    xx, yy = np.meshgrid(xs, ys)
    return np.column_stack([xx.ravel(), yy.ravel()])


def points_in_view(points: np.ndarray, square: Square) -> np.ndarray:
    if points.size == 0:
        return points
    eps = 1e-9 * max(square.width, 1.0)
    mask = (
        (points[:, 0] >= square.x0 - eps)
        & (points[:, 0] <= square.x1 + eps)
        & (points[:, 1] >= square.y0 - eps)
        & (points[:, 1] <= square.y1 + eps)
    )
    return points[mask]


def draw_lattice_grid(ax: plt.Axes, square: Square, grid_points_visible: np.ndarray) -> None:
    if grid_points_visible.size == 0:
        ticks = np.linspace(square.x0, square.x1, 5)
        xs = ticks
        ys = ticks
    else:
        xs = np.unique(np.round(grid_points_visible[:, 0], 10))
        ys = np.unique(np.round(grid_points_visible[:, 1], 10))

    ax.set_xticks(xs)
    ax.set_yticks(ys)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=6, width=1.0)
    ax.grid(color=COLORS["grid"], lw=0.95, alpha=0.72)


def draw_frame(
    save_path: Path,
    *,
    camera: Square,
    display_squares: list[tuple[Square, float, float]],
    current_points: np.ndarray,
    next_points: np.ndarray,
    next_alpha: float,
    title: str,
    description: str,
    point_size_current: float,
    point_size_next: float,
) -> None:
    fig = plt.figure(figsize=(9.6, 9.6))
    ax = fig.add_axes([0.09, 0.20, 0.84, 0.71])

    if current_points.size:
        ax.scatter(current_points[:, 0], current_points[:, 1], s=point_size_current, color=COLORS["point"], alpha=0.92, linewidths=0, zorder=2)
    if next_points.size and next_alpha > 0.0:
        ax.scatter(next_points[:, 0], next_points[:, 1], s=point_size_next, color=COLORS["point"], alpha=next_alpha, linewidths=0, zorder=3)

    for square, alpha, linewidth in display_squares:
        ax.add_patch(
            Rectangle(
                (square.x0, square.y0),
                square.width,
                square.width,
                fill=False,
                edgecolor=COLORS["square"],
                lw=linewidth,
                alpha=alpha,
                zorder=4,
            )
        )
    

    ax.set_xlim(camera.x0, camera.x1)
    ax.set_ylim(camera.y0, camera.y1)
    ax.set_aspect("equal")
    visible_points = [points_in_view(current_points, camera)]
    if next_alpha > 0.0:
        visible_points.append(points_in_view(next_points, camera))
    grid_points_visible = np.vstack([pts for pts in visible_points if pts.size]) if any(pts.size for pts in visible_points) else np.empty((0, 2))
    draw_lattice_grid(ax, camera, grid_points_visible)
    ax.set_xlabel("x", fontsize=16)
    ax.set_ylabel("y", fontsize=16)

    fig.suptitle(title, fontsize=23, y=0.975)
    fig.text(
        0.5,
        0.075,
        description,
        ha="center",
        va="bottom",
        fontsize=13,
        linespacing=1.35,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation(variant: Variant) -> None:
    setup_style()
    outdir = Path("figures/measure/animations") / variant.stem
    frames_dir, gif_dir = ensure_dirs(outdir)
    gif_path = gif_dir / f"{variant.stem}.gif"

    frame_paths: list[Path] = []
    frame_index = 0
    view = initial_view()

    for stage in range(STAGE_COUNT):
        current_points = grid_points(view, variant.divisions, centered=variant.centered)
        next_view = centered_square(view, variant.shrink_fraction)
        next_points = grid_points(next_view, variant.divisions, centered=variant.centered)
        for local_frame in range(SHRINK_FRAMES):
            t = ease_in_out(local_frame / max(1, SHRINK_FRAMES - 1))
            display_square = interpolate_square(view, next_view, t)
            frame_path = frames_dir / f"frame_{frame_index:03d}.png"
            draw_frame(
                frame_path,
                camera=view,
                display_squares=[(display_square, 1.0, 3.2)],
                current_points=current_points,
                next_points=np.empty((0, 2)),
                next_alpha=0.0,
                title=variant.title,
                description=variant.description,
                point_size_current=variant.point_size_current,
                point_size_next=variant.point_size_next,
            )
            frame_paths.append(frame_path)
            frame_index += 1

        for local_frame in range(ZOOM_FRAMES):
            t = ease_in_out(local_frame / max(1, ZOOM_FRAMES - 1))
            camera = interpolate_square(view, next_view, t)
            fade = max(0.0, (t - 0.52) / 0.48)
            frame_path = frames_dir / f"frame_{frame_index:03d}.png"
            draw_frame(
                frame_path,
                camera=camera,
                display_squares=[(next_view, 1.0, 3.2)],
                current_points=current_points,
                next_points=next_points,
                next_alpha=min(1.0, 0.02 + 0.98 * fade) if fade > 0.0 else 0.0,
                title=variant.title,
                description=variant.description,
                point_size_current=variant.point_size_current,
                point_size_next=variant.point_size_next,
            )
            frame_paths.append(frame_path)
            frame_index += 1

        view = next_view

    images = [Image.open(path).convert("P", palette=Image.Palette.ADAPTIVE) for path in frame_paths]
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=int(FRAME_DURATION * 1000),
        loop=GIF_LOOP,
        disposal=2,
    )
    print(f"Saved GIF to: {gif_path.resolve()}")
    print(f"Saved frames to: {frames_dir.resolve()}")


if __name__ == "__main__":
    build_animation(
        Variant(
            name="offset",
            stem="rational_density_zoom",
            centered=False,
            divisions=VISIBLE_DIVISIONS,
            point_size_current=34,
            point_size_next=28,
            shrink_fraction=0.80 / VISIBLE_DIVISIONS,
            title="有理点を避けたつもりの正方形にも, 有理点は残る",
            description="赤い正方形は, いま見えている有理点を避ける候補である.\nしかし拡大すると, その内部にも再び有理点が現れる. したがって $A^c$ に含まれる小正方形は取れない.",
        )
    )
    build_animation(
        Variant(
            name="centered",
            stem="rational_density_zoom_centered",
            centered=True,
            divisions=VISIBLE_DIVISIONS + 1,
            point_size_current=68,
            point_size_next=46,
            shrink_fraction=0.018,
            title="有理点のまわりに正方形を置いても, 無理数は避けられない",
            description="赤い正方形は, 有理点集合 $A$ の内側近似の候補である.\nしかしどの小正方形にも無理数が含まれるので, 正方形全体を $A$ の中に入れることはできない.",
        )
    )
