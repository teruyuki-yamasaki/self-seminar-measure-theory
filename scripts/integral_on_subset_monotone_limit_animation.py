#!/usr/bin/env python3
"""Visualize monotone simple-function approximation on a measurable subset E."""

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
    "phi_n": "#d97706",
    "phi_np1": "#c2410c",
    "subset": "#88c998",
    "subset_edge": "#2b8a57",
    "bar_f": "#1f4b7f",
    "bar_phi": "#d97706",
}

OUTDIR = Path("figures/measure/animations/integral_on_subset_monotone_limit")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "integral_on_subset_monotone_limit.gif"

FRAME_DURATION = 1.0
GIF_LOOP = 0
N_VALUES = [1, 2, 3, 4, 5]
JUMPS = [0.18, 0.47, 0.78]
SUBSET_SPECS = [
    [(0.07, 0.21), (0.43, 0.68), (0.84, 0.95)],
    [(0.12, 0.29), (0.35, 0.50), (0.72, 0.90)],
    [(0.04, 0.16), (0.26, 0.61), (0.76, 0.86)],
]


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
    y = np.zeros_like(x, dtype=float)

    left = x < JUMPS[0]
    mid1 = (JUMPS[0] <= x) & (x < JUMPS[1])
    mid2 = (JUMPS[1] <= x) & (x < JUMPS[2])
    right = JUMPS[2] <= x

    if np.any(left):
        t = x[left] / JUMPS[0]
        y[left] = 0.22 + 0.18 * np.sin(1.3 * np.pi * t + 0.1) ** 2 + 0.05 * np.cos(5.4 * np.pi * t)
    if np.any(mid1):
        t = (x[mid1] - JUMPS[0]) / (JUMPS[1] - JUMPS[0])
        y[mid1] = 0.70 + 0.24 * np.sin(np.pi * t + 0.2) ** 2 + 0.06 * np.sin(4.6 * np.pi * t)
    if np.any(mid2):
        t = (x[mid2] - JUMPS[1]) / (JUMPS[2] - JUMPS[1])
        y[mid2] = 0.42 + 0.16 * np.cos(1.4 * np.pi * t - 0.3) ** 2 + 0.07 * np.sin(5.0 * np.pi * t + 0.4)
    if np.any(right):
        t = (x[right] - JUMPS[2]) / (1.0 - JUMPS[2])
        y[right] = 0.88 + 0.20 * np.sin(1.2 * np.pi * t + 0.4) ** 2 + 0.04 * np.cos(6.0 * np.pi * t)

    return np.clip(y, 0.08, 1.18)


def phi(values: np.ndarray, n: int) -> np.ndarray:
    scale = 2**n
    return np.floor(scale * values) / scale


def subset_mask(x: np.ndarray, intervals: list[tuple[float, float]]) -> np.ndarray:
    mask = np.zeros_like(x, dtype=bool)
    for left, right in intervals:
        mask |= (left <= x) & (x <= right)
    return mask


def integral_on_subset(values: np.ndarray, x: np.ndarray, mask: np.ndarray) -> float:
    trapezoid = getattr(np, "trapezoid", np.trapz)
    masked_values = np.where(mask, values, 0.0)
    return float(trapezoid(masked_values, x))


def draw_frame(
    save_path: Path,
    x: np.ndarray,
    y: np.ndarray,
    subset: np.ndarray,
    intervals: list[tuple[float, float]],
    subset_index: int,
    n: int,
) -> None:
    phi_n = phi(y, n)
    phi_np1 = phi(y, n + 1)
    jump_left_values = [float(f(np.array([jump - 1e-6]))[0]) for jump in JUMPS]
    jump_right_values = [float(f(np.array([jump + 1e-6]))[0]) for jump in JUMPS]

    int_f = integral_on_subset(y, x, subset)
    int_phi_n = integral_on_subset(phi_n, x, subset)
    int_phi_np1 = integral_on_subset(phi_np1, x, subset)
    gap_n = int_f - int_phi_n
    gap_np1 = int_f - int_phi_np1

    fig = plt.figure(figsize=(14.2, 8.8))
    ax_main = fig.add_axes([0.07, 0.50, 0.58, 0.34])
    ax_subset = fig.add_axes([0.07, 0.24, 0.58, 0.13])
    ax_bar = fig.add_axes([0.71, 0.49, 0.23, 0.25])
    ax_formula = fig.add_axes([0.68, 0.12, 0.28, 0.26])

    for left, right in intervals:
        ax_main.axvspan(left, right, color=COLORS["subset"], alpha=0.12, zorder=0)
    ax_main.fill_between(x, 0.0, y, where=subset, color=COLORS["subset"], alpha=0.18, zorder=1)
    ax_main.plot(x, y, color=COLORS["f"], lw=2.8, label=r"$f$")
    ax_main.step(x, phi_n, where="post", color=COLORS["phi_n"], lw=2.0, label=rf"$\phi_n, \ n={n}$")
    ax_main.step(x, phi_np1, where="post", color=COLORS["phi_np1"], lw=2.0, label=rf"$\phi_{{n+1}}, \ n+1={n+1}$")
    ax_main.fill_between(x, 0.0, phi_n, where=subset, color=COLORS["phi_n"], alpha=0.12, zorder=2)
    ax_main.fill_between(x, 0.0, phi_np1, where=subset, color=COLORS["phi_np1"], alpha=0.10, zorder=2)
    ax_main.scatter(JUMPS, jump_left_values, s=54, facecolors="white", edgecolors=COLORS["f"], linewidths=1.8, zorder=5)
    ax_main.scatter(JUMPS, jump_right_values, s=54, facecolors=COLORS["f"], edgecolors=COLORS["f"], linewidths=1.2, zorder=5)
    ax_main.set_xlim(0.0, 1.0)
    ax_main.set_ylim(0.0, max(1.25, float(np.max(y)) + 0.05))
    ax_main.set_xticks(np.linspace(0.0, 1.0, 6))
    ax_main.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_main.set_xlabel("x")
    ax_main.set_ylabel("値")
    ax_main.legend(loc="upper right", frameon=False, fontsize=10.8)
    ax_main.set_title(r"$0\leq \phi_n \leq \phi_{n+1}\leq f$ で, 跳びをもつ $f$ に対して色の付いた $E$ の部分だけ積分して比較する", fontsize=15, pad=10)

    ax_subset.set_xlim(0.0, 1.0)
    ax_subset.set_ylim(-0.14, 0.20)
    ax_subset.axhline(0.0, color=COLORS["ink"], lw=2.0)
    ax_subset.add_patch(Rectangle((0.0, -0.055), 1.0, 0.11, facecolor=COLORS["paper"], edgecolor="none", alpha=0.8))
    for idx, (left, right) in enumerate(intervals, start=1):
        ax_subset.add_patch(
            Rectangle(
                (left, -0.055),
                right - left,
                0.11,
                facecolor=COLORS["subset"],
                edgecolor=COLORS["subset_edge"],
                lw=1.0,
                alpha=0.55,
            )
        )
        ax_subset.text(0.5 * (left + right), 0.10, rf"$E_{idx}$", ha="center", va="bottom", fontsize=10.5, color=COLORS["subset_edge"])
    contains = []
    for jump in JUMPS:
        if any(left <= jump <= right for left, right in intervals):
            contains.append(f"{jump:.2f}")
    if contains:
        subset_note = rf"$E^{{({subset_index})}}=E_1\cup E_2\cup E_3\in\mathcal{{B}}$,  discontinuities at $x={', '.join(contains)}$ are included"
    else:
        subset_note = rf"$E^{{({subset_index})}}=E_1\cup E_2\cup E_3\in\mathcal{{B}}$"
    ax_subset.text(0.5, -0.10, subset_note, ha="center", va="top", fontsize=11.2, color=COLORS["ink"])
    ax_subset.set_xticks(np.linspace(0.0, 1.0, 6))
    ax_subset.set_yticks([])
    ax_subset.grid(axis="x", color=COLORS["grid"], lw=0.8, alpha=0.6)
    ax_subset.spines["top"].set_visible(False)
    ax_subset.spines["left"].set_visible(False)
    ax_subset.spines["right"].set_visible(False)
    ax_subset.set_xlabel(r"$X$")
    ax_subset.set_title(r"1つの可測集合 $E$ で収束を見たら, 次の可測集合へ切り替える", fontsize=14, pad=10)

    ax_bar.bar(
        [r"$\int_E \phi_n$", r"$\int_E \phi_{n+1}$", r"$\int_E f$"],
        [int_phi_n, int_phi_np1, int_f],
        color=[COLORS["bar_phi"], COLORS["phi_np1"], COLORS["bar_f"]],
        alpha=0.84,
    )
    ax_bar.set_ylim(0.0, int_f * 1.12)
    ax_bar.grid(axis="y", color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_bar.set_ylabel("積分値")
    ax_bar.set_title(r"$\int_E \phi_n \uparrow \int_E f$", fontsize=14, pad=8)
    ax_bar.text(
        0.04,
        0.96,
        rf"$\int_E f-\int_E \phi_n \approx {gap_n:.4f}$" + "\n" + rf"$\int_E f-\int_E \phi_{{n+1}} \approx {gap_np1:.4f}$",
        transform=ax_bar.transAxes,
        va="top",
        fontsize=10.6,
        color=COLORS["ink"],
        bbox={"boxstyle": "round, pad=0.18", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.90},
    )

    ax_formula.axis("off")
    ax_formula.text(
        0.00,
        0.88,
        r"$f\geq 0, \ \phi_n\uparrow f$",
        fontsize=16,
        color=COLORS["ink"],
    )
    ax_formula.text(
        0.00,
        0.66,
        r"$\int_E \phi_n\, dm \leq \int_E \phi_{n+1}\, dm \leq \int_E f\, dm$",
        fontsize=13.2,
        color=COLORS["phi_n"],
    )
    ax_formula.text(
        0.00,
        0.44,
        r"$\mathbf{1}_E\phi_n \uparrow \mathbf{1}_E f$ なので, 単調収束定理より",
        fontsize=12.6,
        color=COLORS["muted"],
    )
    ax_formula.text(
        0.00,
        0.22,
        r"$\int_E f(x)\, m(dx)=\lim_{n\to\infty}\int_E \phi_n(x)\, m(dx)$",
        fontsize=14.2,
        color=COLORS["f"],
    )
    ax_formula.text(
        0.00,
        0.02,
        r"この議論は, 今見ている $E$ が不連続点を含むかどうかに関係なく, 任意の $E\in\mathcal{B}$ に対して成り立つ.",
        fontsize=12.0,
        color=COLORS["ink"],
    )

    fig.suptitle("非負可測関数の増加単関数近似: 任意の可測集合 $E$ 上で積分極限が成り立つ", fontsize=21, y=0.972)
    fig.text(
        0.50,
        0.04,
        rf"いまは $E^{{({subset_index})}}$ 上の収束を見ているが, これが終わると別の可測集合に切り替わる. 不連続点を含む場合でも $\mathbf{{1}}_E\phi_n\uparrow \mathbf{{1}}_Ef$ に単調収束定理を適用できる.",
        ha="center",
        fontsize=12.0,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    x = np.linspace(0.0, 1.0, 2800)
    y = f(x)
    frame_paths: list[Path] = []
    frame_index = 0
    for subset_index, intervals in enumerate(SUBSET_SPECS, start=1):
        subset = subset_mask(x, intervals)
        for n in N_VALUES:
            frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
            draw_frame(frame_path, x, y, subset, intervals, subset_index, n)
            frame_paths.append(frame_path)
            frame_index += 1

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
