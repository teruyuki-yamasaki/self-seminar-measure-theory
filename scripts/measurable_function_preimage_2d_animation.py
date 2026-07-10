#!/usr/bin/env python3
"""Visualize preimages of value intervals for a measurable function on a 2D domain."""

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
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#c8d1dc",
    "surface": "#7ea6d9",
    "surface_shadow": "#5c86bc",
    "band": "#f0b45a",
    "band_edge": "#a85b00",
    "preimage_fill": "#d95f5f",
    "preimage_edge": "#963434",
}

OUTDIR = Path("figures/measure/animations/measurable_function_preimage_2d")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "measurable_function_preimage_2d.gif"

FRAME_DURATION = 0.15
GIF_LOOP = 0
FRAMES_PER_SEGMENT = 8


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


def f(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    raw = (
        0.10
        + 0.84 * np.exp(-4.6 * ((x + 0.75) ** 2 + 1.5 * (y + 0.20) ** 2))
        + 0.70 * np.exp(-5.8 * ((x - 0.65) ** 2 + 1.2 * (y - 0.35) ** 2))
        + 0.28 * np.exp(-9.0 * ((x - 0.05) ** 2 + (y + 0.85) ** 2))
        + 0.08 * np.sin(2.4 * x - 1.2 * y)
    )
    raw_min = float(np.min(raw))
    raw_max = float(np.max(raw))
    return 0.04 + 1.02 * (raw - raw_min) / (raw_max - raw_min)


def interval_pairs() -> list[tuple[float, float]]:
    return [
        (0.10, 0.24),
        (0.20, 0.36),
        (0.34, 0.50),
        (0.48, 0.66),
        (0.62, 0.80),
        (0.22, 0.70),
        (0.72, 0.92),
        (0.40, 0.90),
    ]


def ease_in_out(t: float) -> float:
    return 3.0 * t * t - 2.0 * t * t * t


def interpolated_pairs() -> list[tuple[float, float]]:
    anchors = interval_pairs()
    pairs: list[tuple[float, float]] = []
    for start, end in zip(anchors[:-1], anchors[1:]):
        for frame in range(FRAMES_PER_SEGMENT):
            t = ease_in_out(frame / FRAMES_PER_SEGMENT)
            alpha = (1.0 - t) * start[0] + t * end[0]
            beta = (1.0 - t) * start[1] + t * end[1]
            pairs.append((alpha, beta))
    pairs.append(anchors[-1])
    return pairs


def draw_frame(save_path: Path, x: np.ndarray, y: np.ndarray, z: np.ndarray, alpha: float, beta: float) -> None:
    mask = (alpha <= z) & (z < beta)
    z_floor = np.zeros_like(z)

    fig = plt.figure(figsize=(12.8, 8.2))
    ax = fig.add_axes([0.04, 0.12, 0.72, 0.72], projection="3d")
    ax_side = fig.add_axes([0.80, 0.23, 0.15, 0.50])

    base_colors = np.empty(z.shape + (4,), dtype=float)
    base_colors[:] = matplotlib.colors.to_rgba(COLORS["surface"], 0.36)
    highlight = np.array(matplotlib.colors.to_rgba(COLORS["preimage_fill"], 0.82))
    surface_colors = base_colors.copy()
    surface_colors[mask] = highlight

    ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=surface_colors, linewidth=0.0, antialiased=True, shade=False, zorder=3)

    plane_colors = np.empty(z.shape + (4,), dtype=float)
    plane_colors[:] = matplotlib.colors.to_rgba(COLORS["paper"], 0.0)
    plane_colors[mask] = matplotlib.colors.to_rgba(COLORS["preimage_fill"], 0.72)
    ax.plot_surface(x, y, z_floor, rstride=1, cstride=1, facecolors=plane_colors, linewidth=0.0, antialiased=False, shade=False, zorder=1)

    # Two horizontal reference levels for the chosen value interval.
    ax.contour(x, y, z, levels=[alpha, beta], zdir="z", offset=0.0, colors=[COLORS["band_edge"], COLORS["band_edge"]], linewidths=1.1, alpha=0.85)
    band_plane = [
        (x.min(), y.max() + 0.22, alpha),
        (x.max(), y.max() + 0.22, alpha),
        (x.max(), y.max() + 0.22, beta),
        (x.min(), y.max() + 0.22, beta),
    ]
    ax.add_collection3d(
        Poly3DCollection(
            [band_plane],
            facecolors=matplotlib.colors.to_rgba(COLORS["band"], 0.28),
            edgecolors="none",
            zorder=2,
        )
    )
    ax.plot([x.min(), x.max()], [y.max() + 0.22, y.max() + 0.22], [alpha, alpha], color=COLORS["band_edge"], lw=1.8, alpha=0.85)
    ax.plot([x.min(), x.max()], [y.max() + 0.22, y.max() + 0.22], [beta, beta], color=COLORS["band_edge"], lw=1.8, alpha=0.85)

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    ax.set_zlim(0.0, 1.1)
    ax.view_init(elev=31, azim=-55)
    ax.set_xlabel("x", labelpad=10)
    ax.set_ylabel("y", labelpad=10)
    ax.set_zlabel("f(x, y)", labelpad=8)
    ax.set_xticks(np.linspace(-2.0, 2.0, 5))
    ax.set_yticks(np.linspace(-2.0, 2.0, 5))
    ax.set_zticks(np.linspace(0.0, 1.0, 6))
    ax.xaxis.pane.set_facecolor(matplotlib.colors.to_rgba(COLORS["paper"], 1.0))
    ax.yaxis.pane.set_facecolor(matplotlib.colors.to_rgba(COLORS["paper"], 1.0))
    ax.zaxis.pane.set_facecolor(matplotlib.colors.to_rgba(COLORS["paper"], 1.0))
    ax.xaxis._axinfo["grid"]["color"] = COLORS["grid"]
    ax.yaxis._axinfo["grid"]["color"] = COLORS["grid"]
    ax.zaxis._axinfo["grid"]["color"] = COLORS["grid"]
    ax.text2D(
        0.02,
        0.84,
        rf"$[\alpha, \beta)= [{alpha:.2f}, \, {beta:.2f})$",
        transform=ax.transAxes,
        fontsize=13,
        color=COLORS["band_edge"],
        bbox={"boxstyle": "round, pad=0.20", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.92},
    )
    ax.text2D(
        0.02,
        0.05,
        "赤い面片: 曲面上で $f(x, y)\\in[\\alpha, \\beta)$\n赤い底面領域: その逆像 $f^{-1}([\\alpha, \\beta))$",
        transform=ax.transAxes,
        fontsize=11.5,
        color=COLORS["muted"],
    )

    # Side panel showing the interval in the value axis.
    ax_side.set_xlim(0.0, 1.0)
    ax_side.set_ylim(0.0, 1.02)
    ax_side.axvline(0.38, color=COLORS["ink"], lw=2.0)
    ax_side.axhspan(alpha, beta, xmin=0.38, xmax=0.88, color=COLORS["band"], alpha=0.24)
    ax_side.axhline(alpha, color=COLORS["band_edge"], lw=1.4, alpha=0.85)
    ax_side.axhline(beta, color=COLORS["band_edge"], lw=1.4, alpha=0.85)
    ax_side.text(0.46, alpha, r"$\alpha$", ha="left", va="center", fontsize=13, color=COLORS["band_edge"])
    ax_side.text(0.46, beta, r"$\beta$", ha="left", va="center", fontsize=13, color=COLORS["band_edge"])
    ax_side.text(0.62, 0.5 * (alpha + beta), r"$[\alpha, \beta)$", ha="center", va="center", fontsize=14, color=COLORS["band_edge"])
    ax_side.set_xticks([])
    ax_side.set_yticks(np.linspace(0.0, 1.0, 6))
    ax_side.set_ylabel("値域")
    ax_side.spines["top"].set_visible(False)
    ax_side.spines["right"].set_visible(False)
    ax_side.spines["bottom"].set_visible(False)
    ax_side.grid(axis="y", color=COLORS["grid"], lw=0.8, alpha=0.6)
    ax_side.set_title("選んだ値域区間", fontsize=13, pad=10)

    fig.suptitle("2 次元の可測函数でも, 半開区間の逆像は定義域側の可測集合になる", fontsize=20, y=0.975)
    fig.text(
        0.40,
        0.875,
        r"曲面 $z=f(x, y)$ に値域の帯 $[\alpha, \beta)$ を当てると, 底面に逆像 $f^{-1}([\alpha, \beta))$ が現れる",
        ha="center",
        fontsize=14,
        color=COLORS["ink"],
    )
    fig.text(
        0.50,
        0.04,
        "各フレームでは 1 組の $[\\alpha, \\beta)$ を選び, その高さ帯に入る曲面部分と, 底面上の逆像領域を同時に強調している.",
        ha="center",
        fontsize=11.3,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    xs = np.linspace(-2.2, 2.2, 140)
    ys = np.linspace(-2.2, 2.2, 140)
    x, y = np.meshgrid(xs, ys)
    z = f(x, y)

    frame_paths: list[Path] = []
    for frame_index, (alpha, beta) in enumerate(interpolated_pairs()):
        frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(frame_path, x, y, z, alpha, beta)
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
