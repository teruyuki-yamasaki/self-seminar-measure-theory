#!/usr/bin/env python3
"""Animate monotone increasing simple-function approximation to a nonnegative measurable function."""

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
    "f": "#1f4b7f",
    "sn": "#d97706",
    "snp1": "#c2410c",
    "zoom": "#4c9f70",
}

OUTDIR = Path("figures/measure/animations/monotone_simple_approximation")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "monotone_simple_approximation.gif"

FRAME_DURATION = 0.65
GIF_LOOP = 0
N_VALUES = [1, 2, 3, 4, 5]


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


def raw_f(x: np.ndarray) -> np.ndarray:
    return (
        0.08
        + 0.85 * np.exp(-18 * (x - 0.28) ** 2)
        + 0.52 * np.exp(-42 * (x - 0.74) ** 2)
        + 0.06 * np.sin(5 * np.pi * x - 0.3)
    )


def f(x: np.ndarray) -> np.ndarray:
    ref_x = np.linspace(0.0, 1.0, 4000)
    ref_raw = raw_f(ref_x)
    raw_min = float(np.min(ref_raw))
    raw_max = float(np.max(ref_raw))
    return 0.04 + 1.02 * (raw_f(x) - raw_min) / (raw_max - raw_min)


def simple_approx(values: np.ndarray, n: int) -> np.ndarray:
    scale = 2**n
    return np.floor(scale * values) / scale


def draw_value_panel(ax: plt.Axes, probe_y: float, n: int) -> None:
    probe_sn = float(simple_approx(np.array([probe_y]), n)[0])
    probe_snp1 = float(simple_approx(np.array([probe_y]), n + 1)[0])
    levels_n = np.arange(0, int(np.ceil((2**n) * 1.02)) + 1) / 2**n
    levels_np1 = np.arange(0, int(np.ceil((2 ** (n + 1)) * 1.02)) + 1) / 2 ** (n + 1)

    x_n = 0.28
    x_np1 = 0.67
    span = 0.15

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.04)
    ax.axvline(x_n, color=COLORS["ink"], lw=2.0)
    ax.axvline(x_np1, color=COLORS["ink"], lw=2.0)

    for level in levels_n:
        ax.hlines(level, x_n, x_n + span, color=COLORS["sn"], lw=0.9, alpha=0.60)
    for level in levels_np1:
        ax.hlines(level, x_np1, x_np1 + span, color=COLORS["snp1"], lw=0.8, alpha=0.52)

    ax.add_patch(Rectangle((x_n + 0.02, probe_sn), span - 0.04, probe_y - probe_sn, facecolor=COLORS["sn"], alpha=0.18, edgecolor="none"))
    ax.add_patch(Rectangle((x_np1 + 0.02, probe_snp1), span - 0.04, probe_y - probe_snp1, facecolor=COLORS["snp1"], alpha=0.18, edgecolor="none"))

    ax.text(x_n + 0.5 * span, 1.01, rf"$2^{n}$ 等分", ha="center", va="bottom", fontsize=12.0, color=COLORS["sn"])
    ax.text(x_np1 + 0.5 * span, 1.01, rf"$2^{{{n+1}}}$ 等分", ha="center", va="bottom", fontsize=12.0, color=COLORS["snp1"])
    ax.text(x_n + span + 0.035, probe_sn, rf"${int(np.floor((2**n) * probe_y))}/2^{n}$", ha="left", va="center", fontsize=10.8, color=COLORS["sn"])
    ax.text(x_np1 + span + 0.035, probe_snp1, rf"${int(np.floor((2 ** (n+1)) * probe_y))}/2^{{{n+1}}}$", ha="left", va="center", fontsize=10.8, color=COLORS["snp1"])
    ax.text(x_n + 0.5 * span, 0.5 * (probe_sn + probe_y), r"$f-\varphi_n$", ha="center", va="center", fontsize=11.5, color=COLORS["sn"])
    ax.text(x_np1 + 0.5 * span, 0.5 * (probe_snp1 + probe_y), r"$f-\varphi_{n+1}$", ha="center", va="center", fontsize=11.5, color=COLORS["snp1"])

    ax.set_xticks([])
    ax.set_yticks(np.linspace(0.0, 1.0, 6))
    ax.grid(axis="y", color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_ylabel("値域の刻み")
    ax.set_title("値方向の細分", fontsize=14, pad=8)


def draw_frame(save_path: Path, x: np.ndarray, y: np.ndarray, n: int) -> None:
    sn = simple_approx(y, n)
    snp1 = simple_approx(y, n + 1)

    zoom_left, zoom_right = 0.18, 0.36
    zoom_mask = (zoom_left <= x) & (x <= zoom_right)
    zoom_x = x[zoom_mask]
    zoom_y = y[zoom_mask]
    zoom_sn = sn[zoom_mask]
    zoom_snp1 = snp1[zoom_mask]

    fig = plt.figure(figsize=(14.5, 8.8))
    ax_main = fig.add_axes([0.08, 0.54, 0.84, 0.34])
    ax_zoom = fig.add_axes([0.08, 0.13, 0.58, 0.28])
    ax_value = fig.add_axes([0.72, 0.13, 0.20, 0.28])

    ax_main.plot(x, y, color=COLORS["f"], lw=2.8, label=r"$f$")
    ax_main.step(x, sn, where="post", color=COLORS["sn"], lw=2.0, label=rf"$\varphi_n=\lfloor 2^{n}f\rfloor/2^{n}$")
    ax_main.step(x, snp1, where="post", color=COLORS["snp1"], lw=2.0, label=rf"$\varphi_{{n+1}}=\lfloor 2^{{{n+1}}}f\rfloor/2^{{{n+1}}}$")
    ax_main.add_patch(
        Rectangle(
            (zoom_left, 0.0),
            zoom_right - zoom_left,
            1.1,
            facecolor=COLORS["zoom"],
            edgecolor=COLORS["zoom"],
            alpha=0.08,
            lw=1.6,
        )
    )
    ax_main.set_xlim(0.0, 1.0)
    ax_main.set_ylim(0.0, 1.1)
    ax_main.set_xticks(np.linspace(0.0, 1.0, 6))
    ax_main.set_yticks(np.linspace(0.0, 1.0, 6))
    ax_main.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_main.set_xlabel("x")
    ax_main.set_ylabel("値")
    ax_main.legend(loc="upper right", frameon=False, fontsize=11)
    ax_main.set_title(r"全体像:  $0\leq \varphi_n \leq \varphi_{n+1} \leq f$ で, $\varphi_n \nearrow f$", fontsize=16, pad=10)

    ax_zoom.plot(zoom_x, zoom_y, color=COLORS["f"], lw=2.8)
    ax_zoom.step(zoom_x, zoom_sn, where="post", color=COLORS["sn"], lw=2.2)
    ax_zoom.step(zoom_x, zoom_snp1, where="post", color=COLORS["snp1"], lw=2.2)
    levels_n = np.arange(0, int(np.ceil(2**n * zoom_y.max())) + 1) / 2**n
    levels_np1 = np.arange(0, int(np.ceil(2 ** (n + 1) * zoom_y.max())) + 1) / 2 ** (n + 1)
    for level in levels_n:
        ax_zoom.axhline(level, color=COLORS["sn"], lw=0.6, alpha=0.20, zorder=0)
    for level in levels_np1:
        ax_zoom.axhline(level, color=COLORS["snp1"], lw=0.4, alpha=0.15, zorder=0)
    ax_zoom.set_xlim(zoom_left, zoom_right)
    ax_zoom.set_ylim(max(0.0, zoom_y.min() - 0.05), min(1.1, zoom_y.max() + 0.08))
    ax_zoom.set_xticks(np.linspace(zoom_left, zoom_right, 5))
    ax_zoom.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_zoom.set_xlabel("x")
    ax_zoom.set_ylabel("値")
    ax_zoom.set_title(rf"拡大図:  $n={n}$ から $n+1$ へ進むと, 高さの刻みがさらに細かくなって近似が改善する", fontsize=15, pad=10)

    probe_x = 0.242
    probe_y = float(f(np.array([probe_x]))[0])
    probe_sn = float(simple_approx(np.array([probe_y]), n)[0])
    probe_snp1 = float(simple_approx(np.array([probe_y]), n + 1)[0])
    ax_zoom.vlines(probe_x, probe_sn, probe_y, color=COLORS["sn"], lw=2.0, alpha=0.9)
    ax_zoom.vlines(probe_x + 0.004, probe_snp1, probe_y, color=COLORS["snp1"], lw=2.0, alpha=0.9)
    ax_zoom.text(probe_x + 0.007, probe_y + 0.012, r"$f(x)$", color=COLORS["f"], fontsize=12)
    ax_zoom.text(probe_x - 0.016, probe_sn - 0.020, rf"${int(np.floor((2**n) * probe_y))}/2^{n}$", color=COLORS["sn"], fontsize=11)
    ax_zoom.text(probe_x + 0.010, probe_snp1 - 0.020, rf"${int(np.floor((2 ** (n+1)) * probe_y))}/2^{{{n+1}}}$", color=COLORS["snp1"], fontsize=11)

    draw_value_panel(ax_value, probe_y, n)

    fig.suptitle("非負可測函数は, 非負単函数増加列で下から近似できる", fontsize=22, y=0.975)
    fig.text(
        0.5,
        0.04,
        rf"ここでは $\varphi_n(x)=\lfloor 2^n f(x)\rfloor/2^n$ を用いる.  いまは $n={n}$ を表示しており, $n$ を増やすほど値域の刻みが細かくなって $\varphi_n(x)\nearrow f(x)$ となる.",
        ha="center",
        fontsize=12.5,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    x = np.linspace(0.0, 1.0, 2400)
    y = f(x)

    frame_paths: list[Path] = []
    for frame_index, n in enumerate(N_VALUES):
        frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(frame_path, x, y, n)
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
