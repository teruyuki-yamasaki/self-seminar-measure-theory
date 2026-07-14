#!/usr/bin/env python3
"""Animate local Darboux upper and lower sums on a fixed visual interval."""

from __future__ import annotations

from pathlib import Path
import shutil

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
    "grid": "#d7dde6",
    "axis": "#8a95a3",
    "upper": "#d94f4f",
    "lower": "#2f6fed",
    "curve": "#17212b",
    "interval": "#f2b84b",
}

OUTDIR = Path("figures/measure/animations/darboux_local_zoom")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "darboux_local_zoom.gif"

CENTER = 0.537
INITIAL_HALF_WIDTH = 0.23
FINAL_HALF_WIDTH = 0.010
FRAME_DURATION_MS = 80
GIF_MAX_WIDTH = 960
ZOOM_FRAMES = 42
HOLD_START = 5
HOLD_END = 9
DISPLAY_LEFT = -1.18
DISPLAY_RIGHT = 1.18
INTERVAL_LEFT = -1.0
INTERVAL_RIGHT = 1.0


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
            "axes.labelcolor": COLORS["ink"],
            "xtick.color": COLORS["muted"],
            "ytick.color": COLORS["muted"],
            "text.color": COLORS["ink"],
        }
    )


def raw_function(x: np.ndarray) -> np.ndarray:
    return (
        0.55
        + 0.18 * np.sin(2.0 * np.pi * (1.45 * x + 0.06))
        + 0.11 * np.sin(2.0 * np.pi * (4.25 * x - 0.18))
        + 0.055 * np.cos(2.0 * np.pi * (7.10 * x + 0.21))
    )


_NORMALIZE_GRID = np.linspace(0.0, 1.0, 8192)
_RAW_VALUES = raw_function(_NORMALIZE_GRID)
_RAW_MIN = float(np.min(_RAW_VALUES))
_RAW_MAX = float(np.max(_RAW_VALUES))


def f(x: np.ndarray) -> np.ndarray:
    raw = raw_function(x)
    return 0.16 + 0.72 * (raw - _RAW_MIN) / (_RAW_MAX - _RAW_MIN)


def ease_in_out(t: float) -> float:
    return 3.0 * t * t - 2.0 * t * t * t


def half_width_at(progress: float) -> float:
    eased = ease_in_out(progress)
    zoom_ratio = FINAL_HALF_WIDTH / INITIAL_HALF_WIDTH
    return INITIAL_HALF_WIDTH * zoom_ratio**eased


def nice_tick_step(span: float, target_ticks: int = 6) -> float:
    raw = max(span / target_ticks, 1e-12)
    exponent = np.floor(np.log10(raw))
    base = raw / 10.0**exponent
    if base <= 1.5:
        nice = 1.0
    elif base <= 3.5:
        nice = 2.0
    elif base <= 7.5:
        nice = 5.0
    else:
        nice = 10.0
    return float(nice * 10.0**exponent)


def tick_label(value: float, step: float) -> str:
    if step >= 0.1:
        return f"{value:.1f}"
    if step >= 0.01:
        return f"{value:.2f}"
    return f"{value:.3f}"


def display_coordinate(x: np.ndarray | float, half_width: float) -> np.ndarray | float:
    return (x - CENTER) / half_width


def draw_ruler(ax: plt.Axes, half_width: float) -> None:
    step = nice_tick_step(2.0 * half_width * (DISPLAY_RIGHT - DISPLAY_LEFT) / 2.0)
    first = np.floor((CENTER + DISPLAY_LEFT * half_width) / step) - 1
    last = np.ceil((CENTER + DISPLAY_RIGHT * half_width) / step) + 1
    values = step * np.arange(first, last + 1)
    y0 = -0.018
    y1 = 0.0

    ax.axhline(0.0, color=COLORS["axis"], lw=1.2, zorder=1)
    for value in values:
        u = display_coordinate(float(value), half_width)
        if DISPLAY_LEFT <= u <= DISPLAY_RIGHT:
            is_center = abs(value - CENTER) < 0.5 * step
            length = 0.045 if is_center else 0.030
            ax.plot([u, u], [y0, y0 + length], color=COLORS["axis"], lw=1.1, zorder=2)
            ax.axvline(u, color=COLORS["grid"], lw=0.75, alpha=0.42, zorder=0)
            ax.text(
                u,
                y0 - 0.030,
                tick_label(float(value), step),
                ha="center",
                va="top",
                fontsize=8.8,
                color=COLORS["muted"],
            )

    ax.text(DISPLAY_RIGHT, -0.084, "x", ha="right", va="top", fontsize=12, color=COLORS["muted"])


def interval_extrema(half_width: float) -> tuple[float, float, float, float]:
    xs = np.linspace(CENTER - half_width, CENTER + half_width, 3000)
    ys = f(xs)
    min_index = int(np.argmin(ys))
    max_index = int(np.argmax(ys))
    return float(xs[min_index]), float(ys[min_index]), float(xs[max_index]), float(ys[max_index])


def draw_frame(save_path: Path, progress: float) -> None:
    half_width = half_width_at(progress)
    x_values = CENTER + half_width * np.linspace(DISPLAY_LEFT, DISPLAY_RIGHT, 1600)
    u_values = display_coordinate(x_values, half_width)
    y_values = f(x_values)
    x_min, y_min, x_max, y_max = interval_extrema(half_width)
    u_min = display_coordinate(x_min, half_width)
    u_max = display_coordinate(x_max, half_width)

    fig = plt.figure(figsize=(9.6, 5.6))
    ax = fig.add_axes([0.075, 0.17, 0.86, 0.72])

    draw_ruler(ax, half_width)

    ax.add_patch(
        Rectangle(
            (INTERVAL_LEFT, 0.0),
            INTERVAL_RIGHT - INTERVAL_LEFT,
            y_max,
            facecolor=COLORS["upper"],
            edgecolor=COLORS["upper"],
            lw=2.2,
            alpha=0.14,
            zorder=3,
        )
    )
    ax.add_patch(
        Rectangle(
            (INTERVAL_LEFT, 0.0),
            INTERVAL_RIGHT - INTERVAL_LEFT,
            y_min,
            facecolor=COLORS["lower"],
            edgecolor=COLORS["lower"],
            lw=2.2,
            alpha=0.25,
            zorder=4,
        )
    )
    ax.add_patch(
        Rectangle(
            (INTERVAL_LEFT, 0.0),
            INTERVAL_RIGHT - INTERVAL_LEFT,
            0.98,
            fill=False,
            edgecolor=COLORS["interval"],
            lw=2.4,
            alpha=0.90,
            zorder=6,
        )
    )

    ax.plot(u_values, y_values, color=COLORS["curve"], lw=3.0, zorder=7)
    ax.hlines(y_max, INTERVAL_LEFT, INTERVAL_RIGHT, color=COLORS["upper"], lw=1.7, ls=(0, (6, 4)), zorder=8)
    ax.hlines(y_min, INTERVAL_LEFT, INTERVAL_RIGHT, color=COLORS["lower"], lw=1.7, ls=(0, (6, 4)), zorder=8)
    ax.vlines([u_max, u_min], 0.0, [y_max, y_min], colors=[COLORS["upper"], COLORS["lower"]], lw=1.3, alpha=0.78, zorder=8)
    ax.scatter([u_max], [y_max], s=82, color=COLORS["upper"], edgecolor=COLORS["paper"], linewidth=1.6, zorder=9)
    ax.scatter([u_min], [y_min], s=82, color=COLORS["lower"], edgecolor=COLORS["paper"], linewidth=1.6, zorder=9)

    label_side = 1 if progress < 0.72 else -1
    ax.annotate(
        r"$M_i=\max f$",
        xy=(u_max, y_max),
        xytext=(0.18 * label_side, 0.16),
        textcoords="offset fontsize",
        fontsize=12,
        color=COLORS["upper"],
        arrowprops={"arrowstyle": "->", "color": COLORS["upper"], "lw": 1.2},
        zorder=10,
    )
    ax.annotate(
        r"$m_i=\min f$",
        xy=(u_min, y_min),
        xytext=(-0.42 * label_side, -1.45),
        textcoords="offset fontsize",
        fontsize=12,
        color=COLORS["lower"],
        arrowprops={"arrowstyle": "->", "color": COLORS["lower"], "lw": 1.2},
        zorder=10,
    )

    ax.text(
        -1.13,
        0.94,
        rf"$I_i=[c-h,c+h]$,  $h={half_width:.3f}$",
        ha="left",
        va="top",
        fontsize=11.5,
        color=COLORS["ink"],
    )
    ax.text(
        -1.13,
        0.875,
        rf"$M_i-m_i={y_max - y_min:.4f}$",
        ha="left",
        va="top",
        fontsize=11.5,
        color=COLORS["ink"],
    )
    ax.text(
        1.13,
        0.94,
        r"赤: 上和の短冊  /  青: 下和の短冊",
        ha="right",
        va="top",
        fontsize=11.2,
        color=COLORS["muted"],
    )
    ax.text(
        0.0,
        -0.12,
        "短冊の画面上の幅は固定し, 区間の中心で x 方向に拡大する",
        ha="center",
        va="top",
        fontsize=11.4,
        color=COLORS["muted"],
    )

    ax.set_xlim(DISPLAY_LEFT, DISPLAY_RIGHT)
    ax.set_ylim(-0.14, 1.02)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.suptitle("Darboux 和: 小区間を拡大すると振動が消えていく", fontsize=18, y=0.972, weight="bold")
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def frame_progress_values() -> list[float]:
    values = [0.0] * HOLD_START
    values.extend(ease_in_out(i / max(1, ZOOM_FRAMES - 1)) for i in range(ZOOM_FRAMES))
    values.extend([1.0] * HOLD_END)
    return values


def build_animation() -> None:
    setup_style()
    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)

    frame_paths: list[Path] = []
    for index, progress in enumerate(frame_progress_values()):
        frame_path = FRAMES_DIR / f"frame_{index:03d}.png"
        draw_frame(frame_path, progress)
        frame_paths.append(frame_path)

    no_dither = getattr(getattr(Image, "Dither", Image), "NONE", 0)
    resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.BICUBIC)
    frames = []
    for path in frame_paths:
        image = Image.open(path).convert("RGB")
        if image.width > GIF_MAX_WIDTH:
            image = image.resize((GIF_MAX_WIDTH, round(image.height * GIF_MAX_WIDTH / image.width)), resample=resample)
        frames.append(image.quantize(colors=128, dither=no_dither))
    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(f"Saved GIF to: {GIF_PATH.resolve()}")
    print(f"Saved frames to: {FRAMES_DIR.resolve()}")


if __name__ == "__main__":
    build_animation()
