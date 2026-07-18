#!/usr/bin/env python3
"""Visualize uniform convergence as functions trapped in shrinking epsilon bands."""

from __future__ import annotations

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


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#c8d1dc",
    "limit": "#2b8a57",
    "band": "#88c998",
    "band_edge": "#2b8a57",
    "tail_0": "#1f4b7f",
    "tail_1": "#2c7fb8",
    "tail_2": "#4f8fcf",
}

OUTDIR = Path("figures/measure/animations/uniform_convergence_band")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "uniform_convergence_band.gif"

FRAME_DURATION = 1.0
GIF_LOOP = 0
EPSILONS = [0.22, 0.14, 0.09, 0.055, 0.032, 0.018]
TAIL_COUNT = 3


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


def limit_function(x: np.ndarray) -> np.ndarray:
    y = (
        0.48
        + 0.20 * np.sin(1.5 * np.pi * x - 0.15)
        + 0.10 * np.sin(4.2 * np.pi * x + 0.45)
        + 0.055 * np.cos(8.0 * np.pi * x - 0.3)
    )
    return np.clip(y, 0.16, 0.84)


def oscillating_tail(x: np.ndarray, epsilon: float, phase: float, frequency: float) -> np.ndarray:
    envelope = 0.82 * epsilon * (0.55 + 0.45 * np.sin(np.pi * x) ** 2)
    wave = np.sin(frequency * np.pi * x + phase) + 0.35 * np.sin((frequency + 3.0) * np.pi * x - 0.7 * phase)
    wave /= 1.35
    return np.clip(limit_function(x) + envelope * wave, 0.0, 1.0)


def draw_frame(save_path: Path, frame_index: int, epsilon: float) -> None:
    x = np.linspace(0.0, 1.0, 1600)
    f = limit_function(x)
    colors = [COLORS["tail_0"], COLORS["tail_1"], COLORS["tail_2"]]
    tail_indices = [frame_index * TAIL_COUNT + offset + 1 for offset in range(TAIL_COUNT)]
    tails = [
        oscillating_tail(x, epsilon, phase=0.75 * idx + 0.6 * frame_index, frequency=5.0 + 2.0 * idx)
        for idx in range(TAIL_COUNT)
    ]

    fig = plt.figure(figsize=(10.8, 5.2))
    ax = fig.add_axes([0.075, 0.17, 0.88, 0.66])

    ax.fill_between(x, f - epsilon, f + epsilon, color=COLORS["band"], alpha=0.22, zorder=0)
    ax.plot(x, f + epsilon, color=COLORS["band_edge"], lw=1.4, ls="--", alpha=0.70)
    ax.plot(x, f - epsilon, color=COLORS["band_edge"], lw=1.4, ls="--", alpha=0.70)
    ax.plot(x, f, color=COLORS["limit"], lw=3.0, label=r"$f$")

    for n, tail, color in zip(tail_indices, tails, colors):
        ax.plot(x, tail, color=color, lw=2.0, alpha=0.95, label=rf"$f_{{n+{n}}}$")

    ax.text(
        0.02,
        0.95,
        rf"$|f_n(x)-f(x)|<\varepsilon$ for all $x$    $\varepsilon={epsilon:.3f}$",
        transform=ax.transAxes,
        va="top",
        fontsize=12.0,
        color=COLORS["band_edge"],
        bbox={"boxstyle": "round, pad=0.24", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.94},
    )
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel("値")
    ax.set_title(r"同じ $\varepsilon$-帯が全ての点 $x$ で同時に効く", fontsize=16, pad=10)
    ax.grid(color=COLORS["grid"], lw=0.8, alpha=0.65)
    ax.legend(loc="upper right", frameon=False, fontsize=10.5)

    fig.suptitle("一様収束のイメージ: 函数列全体が細い帯の中へ入る", fontsize=18, y=0.965)
    fig.savefig(save_path, dpi=160)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    frame_paths: list[Path] = []
    for idx, epsilon in enumerate(EPSILONS):
        frame_path = FRAMES_DIR / f"frame_{idx:03d}.png"
        draw_frame(frame_path, idx, epsilon)
        frame_paths.append(frame_path)

    adaptive_palette = getattr(getattr(Image, "Palette", Image), "ADAPTIVE", Image.ADAPTIVE)
    frames = [Image.open(path).convert("P", palette=adaptive_palette) for path in frame_paths]
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
