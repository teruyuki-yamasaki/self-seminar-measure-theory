#!/usr/bin/env python3
"""Visualize Egorov's theorem with smooth approximants to a discontinuous limit."""

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
    "limit": "#2b8a57",
    "tail_0": "#1f4b7f",
    "tail_1": "#2c7fb8",
    "tail_2": "#4f8fcf",
    "band": "#88c998",
    "band_edge": "#2b8a57",
    "exception": "#d95f5f",
    "axis_fill": "#f7f1e4",
}

OUTDIR = Path("figures/measure/animations/egorov_theorem")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "egorov_theorem.gif"

FRAME_DURATION = 1.1
GIF_LOOP = 0

A = 0.0
B = 1.0
C = 1.0 / 3.0
D = 2.0 / 3.0
R_VALUES = [2, 3, 4, 5, 6]
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


def bump(u: np.ndarray) -> np.ndarray:
    out = np.zeros_like(u, dtype=float)
    mask = u > 0.0
    out[mask] = np.exp(-1.0 / u[mask])
    return out


def smooth_step(t: np.ndarray) -> np.ndarray:
    out = np.zeros_like(t, dtype=float)
    out[t >= 1.0] = 1.0
    mid = (-1.0 < t) & (t < 1.0)
    if np.any(mid):
        u = 0.5 * (t[mid] + 1.0)
        left = bump(u)
        right = bump(1.0 - u)
        out[mid] = left / (left + right)
    return out


def limit_function(x: np.ndarray) -> np.ndarray:
    y = np.zeros_like(x, dtype=float)
    left = x < C
    middle = (C <= x) & (x <= D)
    right = x > D

    if np.any(left):
        t = (x[left] - A) / (C - A)
        y[left] = (
            0.16
            + 0.08 * np.sin(1.2 * np.pi * t + 0.3)
            + 0.04 * np.sin(4.4 * np.pi * t - 0.4)
            + 0.02 * np.cos(7.0 * np.pi * t + 0.6)
        )
    if np.any(middle):
        t = (x[middle] - C) / (D - C)
        y[middle] = (
            0.58
            + 0.20 * np.sin(np.pi * t)
            + 0.11 * np.sin(3.0 * np.pi * t - 0.35)
            + 0.05 * np.cos(5.0 * np.pi * t + 0.4)
        )
    if np.any(right):
        t = (x[right] - D) / (B - D)
        y[right] = (
            0.24
            + 0.07 * np.sin(1.4 * np.pi * t + 0.2)
            + 0.05 * np.cos(3.6 * np.pi * t - 0.5)
            + 0.02 * np.sin(8.0 * np.pi * t + 0.1)
        )
    return np.clip(y, 0.0, 1.0)


def transition_width(n: int) -> float:
    return 2.0 ** (-(n + 2))


def smooth_approximant(x: np.ndarray, n: int) -> np.ndarray:
    delta = transition_width(n)
    s_c = smooth_step((x - C) / delta)
    s_d = smooth_step((x - D) / delta)

    left_mask = 1.0 - s_c
    middle_mask = s_c * (1.0 - s_d)
    right_mask = s_d

    t_left = np.clip((x - A) / (C - A), 0.0, 1.0)
    left_branch = (
        0.16
        + 0.08 * np.sin(1.2 * np.pi * t_left + 0.3)
        + 0.04 * np.sin(4.4 * np.pi * t_left - 0.4)
        + 0.02 * np.cos(7.0 * np.pi * t_left + 0.6)
    )

    t_middle = np.clip((x - C) / (D - C), 0.0, 1.0)
    middle_branch = (
        0.58
        + 0.20 * np.sin(np.pi * t_middle)
        + 0.11 * np.sin(3.0 * np.pi * t_middle - 0.35)
        + 0.05 * np.cos(5.0 * np.pi * t_middle + 0.4)
    )

    t_right = np.clip((x - D) / (B - D), 0.0, 1.0)
    right_branch = (
        0.24
        + 0.07 * np.sin(1.4 * np.pi * t_right + 0.2)
        + 0.05 * np.cos(3.6 * np.pi * t_right - 0.5)
        + 0.02 * np.sin(8.0 * np.pi * t_right + 0.1)
    )

    y = left_branch * left_mask + middle_branch * middle_mask + right_branch * right_mask
    return np.clip(y, 0.0, 1.0)


def frame_spec(r: int) -> tuple[int, float]:
    return r + 1, 2.0 ** (-r)


def draw_frame(save_path: Path, r: int) -> None:
    n_r, band = frame_spec(r)
    epsilon = transition_width(n_r)
    x = np.linspace(A, B, 5000)
    f = limit_function(x)
    tail_indices = [n_r + offset for offset in range(TAIL_COUNT)]
    tail_colors = [COLORS["tail_0"], COLORS["tail_1"], COLORS["tail_2"]]
    tails = [smooth_approximant(x, n) for n in tail_indices]
    f_left = float(limit_function(np.array([C - 1e-6]))[0])
    f_c_right = float(limit_function(np.array([C + 1e-6]))[0])
    f_d_left = float(limit_function(np.array([D - 1e-6]))[0])
    f_right = float(limit_function(np.array([D + 1e-6]))[0])

    fig = plt.figure(figsize=(14.0, 8.6))
    ax_main = fig.add_axes([0.08, 0.50, 0.84, 0.31])
    ax_domain = fig.add_axes([0.08, 0.25, 0.84, 0.13])
    ax_text = fig.add_axes([0.08, 0.08, 0.84, 0.11])

    band_lower = np.clip(f - band, 0.0, 1.0)
    band_upper = np.clip(f + band, 0.0, 1.0)
    ax_main.fill_between(x, band_lower, band_upper, color=COLORS["band"], alpha=0.20, zorder=0)

    for center in (C, D):
        ax_main.axvspan(center - epsilon, center + epsilon, color=COLORS["exception"], alpha=0.12, zorder=1)

    ax_main.plot(x, f, color=COLORS["limit"], lw=2.8, label=r"$f$")
    for n, y, color in zip(tail_indices, tails, tail_colors):
        ax_main.plot(x, y, color=color, lw=2.0, alpha=0.95, label=rf"$f_{{{n}}}$")

    ax_main.axvline(C, color=COLORS["muted"], lw=1.0, ls="--", alpha=0.8)
    ax_main.axvline(D, color=COLORS["muted"], lw=1.0, ls="--", alpha=0.8)
    ax_main.text(C, 1.06, r"$c$", ha="center", va="bottom", fontsize=11.5, color=COLORS["muted"])
    ax_main.text(D, 1.06, r"$d$", ha="center", va="bottom", fontsize=11.5, color=COLORS["muted"])
    ax_main.scatter([C, D], [f_left, f_d_left], s=56, facecolors="white", edgecolors=COLORS["limit"], linewidths=1.8, zorder=6)
    ax_main.scatter([C, D], [f_c_right, f_right], s=56, facecolors=COLORS["limit"], edgecolors=COLORS["limit"], linewidths=1.2, zorder=6)
    ax_main.text(
        0.02,
        0.95,
        rf"Egorov band: $|f_k-f|\leq 2^{{-{r}}}={band:.4f}$",
        transform=ax_main.transAxes,
        va="top",
        fontsize=12.5,
        color=COLORS["band_edge"],
        bbox={"boxstyle": "round, pad=0.20", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.92},
    )
    ax_main.set_xlim(A, B)
    ax_main.set_ylim(-0.05, 1.12)
    ax_main.set_xticks(np.linspace(A, B, 6))
    ax_main.set_yticks([0.0, 0.5, 1.0])
    ax_main.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_main.set_xlabel("x")
    ax_main.set_ylabel("値")
    ax_main.set_title(r"$k\geq n_r$ の tail は, $c, d$ の近傍を除けば極限関数 $f$ の細い帯の中に入る", fontsize=15)
    ax_main.legend(loc="upper right", frameon=False, fontsize=10.8)

    ax_domain.set_xlim(A, B)
    ax_domain.set_ylim(-0.15, 0.20)
    ax_domain.axhline(0.0, color=COLORS["ink"], lw=2.0)
    ax_domain.add_patch(
        Rectangle((A, -0.055), B - A, 0.11, facecolor=COLORS["axis_fill"], edgecolor="none", alpha=0.55)
    )
    for center in (C, D):
        ax_domain.add_patch(
            Rectangle(
                (center - epsilon, -0.055),
                2.0 * epsilon,
                0.11,
                facecolor=COLORS["exception"],
                edgecolor=COLORS["exception"],
                lw=1.0,
                alpha=0.65,
            )
        )
    ax_domain.text(C, 0.10, r"$[c-\varepsilon_r, c+\varepsilon_r]$", ha="center", va="bottom", fontsize=10.8, color=COLORS["exception"])
    ax_domain.text(D, 0.10, r"$[d-\varepsilon_r, d+\varepsilon_r]$", ha="center", va="bottom", fontsize=10.8, color=COLORS["exception"])
    ax_domain.text(
        0.50,
        -0.11,
        r"$Y_r=X\backslash E_r$ とおくと, $E_r$ は不連続点の $\varepsilon_r$ 近傍だけからなる",
        ha="center",
        va="top",
        fontsize=11.8,
        color=COLORS["ink"],
    )
    ax_domain.set_xticks(np.linspace(A, B, 6))
    ax_domain.set_yticks([])
    ax_domain.grid(axis="x", color=COLORS["grid"], lw=0.8, alpha=0.6)
    ax_domain.spines["top"].set_visible(False)
    ax_domain.spines["left"].set_visible(False)
    ax_domain.spines["right"].set_visible(False)
    ax_domain.set_xlabel(r"$X=[a, b]$")
    ax_domain.set_title(r"例外集合 $E_r$ は $m(E_r)=4\varepsilon_r\to0$ を満たす", fontsize=15, pad=12)

    ax_text.axis("off")
    ax_text.text(
        0.00,
        0.72,
        rf"$r={r}, \quad n_r={n_r}, \quad \varepsilon_r={epsilon:.4f}, \quad m(E_r)=4\varepsilon_r={4.0*epsilon:.4f}$",
        fontsize=14.5,
        color=COLORS["exception"],
    )
    ax_text.text(
        0.00,
        0.40,
        rf"$k\geq n_r$ なら, $Y_r=X\backslash E_r$ 上で $|f_k(x)-f(x)|\leq 2^{{-{r}}}$.",
        fontsize=13.0,
        color=COLORS["ink"],
    )
    ax_text.text(
        0.00,
        0.08,
        r"この例では実際には $Y_r$ 上で $f_k=f$ なので, 証明に現れる「tail が帯へ入る」という主張を, より強い形で見ている.",
        fontsize=12.0,
        color=COLORS["band_edge"],
    )

    fig.suptitle("Egorov's theorem: 滑らかな近似関数列と, 測度 0 に縮む例外集合", fontsize=20, y=0.965)
    fig.text(
        0.08,
        0.90,
        r"$f_n$ は $[a, b]$ 上の滑らかな関数で, $c, d$ の 2 点だけで跳びをもつ極限関数 $f$ に a.e. 収束する.",
        fontsize=12.0,
        color=COLORS["muted"],
    )
    fig.text(
        0.08,
        0.865,
        r"各フレームでは $r$ を固定し, 証明に現れる ``$k\geq n_r$ なら $Y_r$ 上で一様に小さい'' という tail 条件を描いている.",
        fontsize=12.0,
        color=COLORS["ink"],
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    frame_paths: list[Path] = []
    for frame_index, r in enumerate(R_VALUES):
        frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(frame_path, r)
        frame_paths.append(frame_path)

    adaptive_palette = getattr(getattr(Image, "Palette", Image), "ADAPTIVE", Image.ADAPTIVE)
    images = [Image.open(path).convert("P", palette=adaptive_palette) for path in frame_paths]
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
