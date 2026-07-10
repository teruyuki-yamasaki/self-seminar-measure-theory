#!/usr/bin/env python3
"""Visualize preimages of value intervals for a measurable function on R."""

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
from matplotlib.patches import Rectangle


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#c8d1dc",
    "curve": "#1f4b7f",
    "band": "#f0b45a",
    "band_edge": "#a85b00",
    "preimage_fill": "#d95f5f",
    "preimage_edge": "#963434",
    "axis_fill": "#f7f1e4",
}

OUTDIR = Path("figures/measure/animations/measurable_function_preimage_1d")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "measurable_function_preimage_1d.gif"

FRAME_DURATION = 1.0
GIF_LOOP = 0
FRAME_COUNT = 8


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


def f(x: np.ndarray) -> np.ndarray:
    raw = (
        0.12
        + 0.62 * np.exp(-38 * (x + 1.05) ** 2)
        + 0.88 * np.exp(-20 * (x - 0.20) ** 2)
        + 0.54 * np.exp(-26 * (x - 1.15) ** 2)
        + 0.06 * np.sin(3.6 * x - 0.4)
    )
    raw_min = float(np.min(raw))
    raw_max = float(np.max(raw))
    return 0.04 + 1.02 * (raw - raw_min) / (raw_max - raw_min)


def interval_pairs() -> list[tuple[float, float]]:
    return [
        (0.14, 0.32),
        (0.30, 0.48),
        (0.44, 0.64),
        (0.58, 0.76),
        (0.22, 0.72),
        (0.70, 0.92),
        (0.36, 0.88),
        (0.08, 0.20),
    ]


def preimage_intervals(x: np.ndarray, y: np.ndarray, alpha: float, beta: float) -> list[tuple[float, float]]:
    mask = (alpha <= y) & (y < beta)
    intervals: list[tuple[float, float]] = []
    if not np.any(mask):
        return intervals

    idx = np.where(mask)[0]
    start = idx[0]
    prev = idx[0]
    for current in idx[1:]:
        if current != prev + 1:
            intervals.append((x[start], x[prev]))
            start = current
        prev = current
    intervals.append((x[start], x[prev]))
    return intervals


def draw_frame(save_path: Path, frame_index: int, x: np.ndarray, y: np.ndarray, alpha: float, beta: float) -> None:
    intervals = preimage_intervals(x, y, alpha, beta)
    mask = (alpha <= y) & (y < beta)

    fig = plt.figure(figsize=(12.8, 7.4))
    ax_graph = fig.add_axes([0.09, 0.45, 0.84, 0.42])
    ax_line = fig.add_axes([0.09, 0.12, 0.84, 0.18])

    ax_graph.axhspan(alpha, beta, color=COLORS["band"], alpha=0.16, zorder=1)
    ax_graph.plot(x, y, color=COLORS["curve"], lw=2.8, zorder=4)
    for left, right in intervals:
        interval_mask = (left <= x) & (x <= right)
        ax_graph.plot(x[interval_mask], y[interval_mask], color=COLORS["preimage_edge"], lw=3.6, zorder=5)

    for left, right in intervals:
        ax_graph.add_patch(
            Rectangle(
                (left, 0.0),
                right - left,
                beta,
                facecolor=COLORS["preimage_fill"],
                edgecolor="none",
                alpha=0.12,
                zorder=2,
            )
        )

    ax_graph.set_xlim(x[0], x[-1])
    ax_graph.set_ylim(0.0, 1.1)
    ax_graph.set_xticks(np.linspace(-2.0, 2.0, 5))
    ax_graph.set_yticks(np.linspace(0.0, 1.0, 6))
    ax_graph.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_graph.set_xlabel("x")
    ax_graph.set_ylabel("y")
    ax_graph.set_title(r"値域の区間 $[\alpha, \beta)$ を選ぶと, 逆像 $f^{-1}([\alpha, \beta))$ が $x$ 軸上の可測集合として現れる", fontsize=15)

    ax_graph.text(
        0.02,
        0.95,
        rf"$[\alpha, \beta)= [{alpha:.2f}, \, {beta:.2f})$",
        transform=ax_graph.transAxes,
        va="top",
        fontsize=13,
        color=COLORS["band_edge"],
        bbox={"boxstyle": "round, pad=0.20", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.92},
    )

    ax_graph.text(
        1.02,
        alpha,
        r"$\alpha$",
        transform=ax_graph.get_yaxis_transform(),
        ha="left",
        va="center",
        fontsize=12,
        color=COLORS["band_edge"],
    )
    ax_graph.text(
        1.02,
        beta,
        r"$\beta$",
        transform=ax_graph.get_yaxis_transform(),
        ha="left",
        va="center",
        fontsize=12,
        color=COLORS["band_edge"],
    )

    ax_line.set_xlim(x[0], x[-1])
    ax_line.set_ylim(-0.12, 0.22)
    ax_line.axhline(0.0, color=COLORS["ink"], lw=2.0)
    ax_line.add_patch(Rectangle((x[0], -0.055), x[-1] - x[0], 0.11, facecolor=COLORS["axis_fill"], edgecolor="none", alpha=0.55, zorder=0))

    for left, right in intervals:
        ax_line.add_patch(
            Rectangle(
                (left, -0.055),
                right - left,
                0.11,
                facecolor=COLORS["preimage_fill"],
                edgecolor=COLORS["preimage_edge"],
                lw=1.0,
                alpha=0.60,
                zorder=2,
            )
        )

    ax_line.set_xticks(np.linspace(-2.0, 2.0, 5))
    ax_line.set_yticks([])
    ax_line.grid(axis="x", color=COLORS["grid"], lw=0.8, alpha=0.6)
    ax_line.spines["left"].set_visible(False)
    ax_line.spines["right"].set_visible(False)
    ax_line.spines["top"].set_visible(False)
    ax_line.set_xlabel("x")
    ax_line.set_title(r"逆像 $f^{-1}([\alpha, \beta))$", fontsize=15, pad=12)

    if intervals:
        interval_text = " ∪ ".join([rf"[{left:.2f}, \, {right:.2f}]" for left, right in intervals[:4]])
        if len(intervals) > 4:
            interval_text += r" \cup \cdots"
    else:
        interval_text = r"\varnothing"
    ax_line.text(
        0.5,
        0.88,
        rf"$f^{{-1}}([\alpha, \beta)) = {interval_text}$",
        transform=ax_line.transAxes,
        ha="center",
        va="center",
        fontsize=12.5,
        color=COLORS["preimage_edge"],
    )

    fig.suptitle("可測函数では, 値域の半開区間の逆像が定義域側で可測集合になる", fontsize=20, y=0.96)
    fig.text(
        0.5,
        0.045,
        "各フレームでは 1 組の $[\\alpha, \\beta)$ を選び, その帯に入るグラフ部分を赤くし, 同じ $x$ の集まりを下の実数軸へ写している.",
        ha="center",
        fontsize=11.3,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    x = np.linspace(-2.2, 2.2, 2200)
    y = f(x)
    pairs = interval_pairs()

    frame_paths: list[Path] = []
    for frame_index, (alpha, beta) in enumerate(pairs):
        frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(frame_path, frame_index, x, y, alpha, beta)
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
