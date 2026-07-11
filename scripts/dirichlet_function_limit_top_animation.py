#!/usr/bin/env python3
"""Animate convergence to the Dirichlet function with only the top panel."""

from __future__ import annotations

from math import factorial, sqrt
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
    "rational": "#c23b30",
    "irrational": "#2c7fb8",
}

OUTDIR = Path("figures/measure/animations/dirichlet_function_limit_top")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "dirichlet_function_limit_top.gif"

FRAME_DURATION = 1.0
GIF_LOOP = 0
N_VALUES = [1, 2, 3, 4, 5, 6]


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


def irrational_samples(count: int = 280) -> np.ndarray:
    phi = (1.0 + sqrt(5.0)) / 2.0
    xs = np.array([(k / phi) % 1.0 for k in range(1, count + 1)])
    ys = np.zeros_like(xs)
    return np.column_stack([xs, ys])


def stage_support_points(n: int) -> np.ndarray:
    denom = factorial(n)
    return np.linspace(0.0, 1.0, denom + 1)


def draw_frame(save_path: Path, *, stage_index: int, n_values: list[int], irrationals: np.ndarray) -> None:
    current_n = n_values[stage_index]
    support_points = stage_support_points(current_n)

    fig = plt.figure(figsize=(12.8, 5.2))
    ax_func = fig.add_axes([0.08, 0.20, 0.84, 0.46])

    ax_func.axhline(0.0, color=COLORS["irrational"], lw=2.2, alpha=0.9, zorder=1)
    ax_func.axhline(1.0, color=COLORS["rational"], lw=2.2, alpha=0.9, zorder=1)
    ax_func.scatter(
        irrationals[:, 0],
        irrationals[:, 1],
        s=7,
        color=COLORS["irrational"],
        alpha=0.24,
        linewidths=0,
        zorder=2,
    )

    ax_func.vlines(support_points, 0.0, 1.0, color=COLORS["rational"], lw=0.9, alpha=0.50, zorder=3)
    ax_func.scatter(support_points, np.ones(len(support_points)), s=22, color=COLORS["rational"], alpha=0.92, linewidths=0, zorder=4)

    ax_func.set_xlim(0.0, 1.0)
    ax_func.set_ylim(-0.08, 1.08)
    ax_func.set_xticks(np.linspace(0.0, 1.0, 6))
    ax_func.set_yticks([0.0, 1.0])
    ax_func.set_yticklabels(["0", "1"])
    ax_func.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_func.set_xlabel("x")
    ax_func.set_ylabel(r"$g_n(x)$")
    ax_func.set_title(r"固定した $n$ では $g_n(x)=1$ となる点だけが赤く立つ", fontsize=14)

    fig.suptitle(r"$g_n(x)=\mathbf{1}_{\{x\in[0,1]:\, n!x\in\mathbb{Z}\}}(x)\ \longrightarrow\ D(x)$", fontsize=17, y=0.95)
    fig.text(
        0.08,
        0.82,
        r"$g_n(x):=\lim_{k\to\infty}\cos^{2k}(n!\pi x)=\mathbf{1}_{\{x\in[0,1]:\, n!x\in\mathbb{Z}\}}(x)$",
        fontsize=13,
        color=COLORS["ink"],
    )
    fig.text(
        0.08,
        0.76,
        rf"第 {stage_index + 1} 段階では $n={current_n}$. 赤い点は $x=\frac{{m}}{{{factorial(current_n)}}}$ に対応する.",
        fontsize=11.5,
        color=COLORS["muted"],
    )
    fig.text(
        0.08,
        0.71,
        r"$n$ が大きくなるほど 1 となる点は細かく増えるが, 各段階では有限個である.",
        fontsize=11.0,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    irrationals = irrational_samples()
    frame_paths: list[Path] = []
    for stage_index in range(len(N_VALUES)):
        frame_path = FRAMES_DIR / f"frame_{stage_index:03d}.png"
        draw_frame(frame_path, stage_index=stage_index, n_values=N_VALUES, irrationals=irrationals)
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


if __name__ == "__main__":
    build_animation()
