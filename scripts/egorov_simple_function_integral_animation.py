#!/usr/bin/env python3
"""Visualize dyadic simple-function approximation and the Egorov effect on integrals."""

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
    "tail_0": "#d97706",
    "tail_1": "#c2410c",
    "tail_2": "#9a3412",
    "band": "#83c784",
    "band_edge": "#2b8a57",
    "exception": "#d95f5f",
    "axis_fill": "#f7f1e4",
}

OUTDIR = Path("figures/measure/animations/egorov_simple_function_integral")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "egorov_simple_function_integral.gif"

FRAME_DURATION = 1.05
GIF_LOOP = 0
N_VALUES = [1, 2, 3, 4, 5]
TAIL_COUNT = 3
X0 = 0.61
Y_CAP = 4.4


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
    return (
        0.20
        + 0.18 * np.sin(2.2 * np.pi * x + 0.2) ** 2
        + 0.12 * np.exp(-38 * (x - 0.22) ** 2)
        + 0.32 / np.sqrt(np.abs(x - X0))
    )


def simple_approx(values: np.ndarray, n: int) -> np.ndarray:
    scale = 2**n
    return np.where(values >= n, n, np.floor(scale * values) / scale)


def contiguous_intervals(mask: np.ndarray, x: np.ndarray) -> list[tuple[float, float]]:
    if not np.any(mask):
        return []
    idx = np.flatnonzero(mask)
    intervals: list[tuple[float, float]] = []
    start = idx[0]
    prev = idx[0]
    for current in idx[1:]:
        if current != prev + 1:
            intervals.append((float(x[start]), float(x[prev])))
            start = current
        prev = current
    intervals.append((float(x[start]), float(x[prev])))
    return intervals


def draw_frame(save_path: Path, n: int) -> None:
    x = np.linspace(0.0, 1.0, 5000)
    x_int = (np.arange(120000) + 0.5) / 120000.0
    y = f(x)
    y_int = f(x_int)

    tail_indices = [n + offset for offset in range(TAIL_COUNT)]
    tail_colors = [COLORS["tail_0"], COLORS["tail_1"], COLORS["tail_2"]]
    tail_values = [simple_approx(y, k) for k in tail_indices]
    tail_values_int = [simple_approx(y_int, k) for k in tail_indices]

    epsilon = 2.0 ** (-n)
    exceptional_mask = y > n
    intervals = contiguous_intervals(exceptional_mask, x)
    y_display = np.clip(y, 0.0, Y_CAP)
    band_lower = np.clip(y_display - epsilon, 0.0, Y_CAP)
    band_upper = np.clip(y_display + epsilon, 0.0, Y_CAP)
    good_mask = ~exceptional_mask

    dx = 1.0 / len(x_int)
    int_f = float(np.sum(y_int) * dx)
    int_sn = [float(np.sum(sv) * dx) for sv in tail_values_int]
    exc_mask_int = y_int > n
    int_exc = float(np.sum((y_int - tail_values_int[0]) * exc_mask_int) * dx)
    int_good = float(np.sum((y_int - tail_values_int[0]) * (~exc_mask_int)) * dx)
    exc_measure = float(np.mean(exc_mask_int))

    fig = plt.figure(figsize=(14.3, 8.8))
    ax_main = fig.add_axes([0.07, 0.50, 0.60, 0.35])
    ax_domain = fig.add_axes([0.07, 0.27, 0.60, 0.12])
    ax_formula = fig.add_axes([0.71, 0.50, 0.24, 0.35])
    ax_integral = fig.add_axes([0.71, 0.14, 0.24, 0.23])
    ax_note = fig.add_axes([0.07, 0.08, 0.60, 0.12])

    ax_main.fill_between(x, band_lower, band_upper, where=good_mask, color=COLORS["band"], alpha=0.18, zorder=0)
    for left, right in intervals:
        ax_main.axvspan(left, right, color=COLORS["exception"], alpha=0.12, zorder=1)
    ax_main.plot(x, y_display, color=COLORS["f"], lw=2.6, label=r"$f$")
    for k, values, color in zip(tail_indices, tail_values, tail_colors):
        ax_main.step(x, np.clip(values, 0.0, Y_CAP), where="post", color=color, lw=1.9, alpha=0.95, label=rf"$s_{{{k}}}$")
    ax_main.axhline(float(n), color=COLORS["exception"], lw=1.0, ls="--", alpha=0.7)
    ax_main.text(
        0.02,
        0.95,
        rf"Egorov band: $|s_k-f|\leq 2^{{-{n}}}$ on $Y_n$",
        transform=ax_main.transAxes,
        va="top",
        fontsize=12.0,
        color=COLORS["band_edge"],
        bbox={"boxstyle": "round, pad=0.18", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.92},
    )
    ax_main.text(0.98, min(0.96, n / Y_CAP + 0.02), rf"$f=n={n}$", transform=ax_main.transAxes, ha="right", va="bottom", fontsize=11.0, color=COLORS["exception"])
    ax_main.set_xlim(0.0, 1.0)
    ax_main.set_ylim(0.0, Y_CAP)
    ax_main.set_xticks(np.linspace(0.0, 1.0, 6))
    ax_main.set_yticks(np.arange(0.0, Y_CAP + 0.001, 1.0))
    ax_main.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_main.set_xlabel("x")
    ax_main.set_ylabel("値")
    ax_main.legend(loc="upper right", frameon=False, fontsize=10.5)
    ax_main.set_title(r"dyadic 単関数 $s_k$ は, $Y_n=\{f\leq n\}$ 上では tail 全体で $f$ に一様に近い", fontsize=15, pad=10)

    ax_domain.set_xlim(0.0, 1.0)
    ax_domain.set_ylim(-0.16, 0.20)
    ax_domain.axhline(0.0, color=COLORS["ink"], lw=2.0)
    ax_domain.add_patch(Rectangle((0.0, -0.055), 1.0, 0.11, facecolor=COLORS["axis_fill"], edgecolor="none", alpha=0.55))
    for left, right in intervals:
        ax_domain.add_patch(
            Rectangle((left, -0.055), right - left, 0.11, facecolor=COLORS["exception"], edgecolor=COLORS["exception"], lw=1.0, alpha=0.65)
        )
    ax_domain.text(0.5, 0.10, r"$E_n=\{x:\, f(x)>n\}$,  \quad $Y_n=X\setminus E_n$", ha="center", va="bottom", fontsize=11.4, color=COLORS["ink"])
    ax_domain.set_xticks(np.linspace(0.0, 1.0, 6))
    ax_domain.set_yticks([])
    ax_domain.grid(axis="x", color=COLORS["grid"], lw=0.8, alpha=0.6)
    ax_domain.spines["top"].set_visible(False)
    ax_domain.spines["left"].set_visible(False)
    ax_domain.spines["right"].set_visible(False)
    ax_domain.set_xlabel(r"$X=[a, b]$")
    ax_domain.set_title(r"$m(E_n)\to0$ なので, 一様収束しない部分は小さい集合へ押し込められる", fontsize=14, pad=12)

    ax_formula.axis("off")
    ax_formula.text(0.00, 0.92, rf"$s_n(x)=\sum_{{k=0}}^{{n2^n-1}}\frac{{k}}{{2^n}}\mathbf{{1}}_{{A_{{k, n}}}}(x)+n\, \mathbf{{1}}_{{\{{f\geq n\}}}}(x)$", fontsize=12.7, color=COLORS["ink"])
    ax_formula.text(0.00, 0.76, rf"$A_{{k, n}}=\{{x:\, \frac{{k}}{{2^n}}\leq f(x)<\frac{{k+1}}{{2^n}}\}}$", fontsize=12.0, color=COLORS["muted"])
    ax_formula.text(0.00, 0.54, rf"on $Y_n$:  $0\leq f-s_k\leq 2^{{-{n}}}$ for all $k\geq n$", fontsize=12.6, color=COLORS["band_edge"])
    ax_formula.text(0.00, 0.34, rf"$0\leq \int_X f-\int_X s_n = \int_{{Y_n}}(f-s_n)+\int_{{E_n}}(f-s_n)$", fontsize=12.5, color=COLORS["ink"])
    ax_formula.text(0.00, 0.16, rf"$\int_{{Y_n}}(f-s_n)\leq 2^{{-{n}}}m(X), \qquad \int_{{E_n}} f \to 0$", fontsize=12.5, color=COLORS["exception"])

    ax_integral.bar(["∫f", rf"∫s_{tail_indices[0]}", rf"∫s_{tail_indices[1]}", rf"∫s_{tail_indices[2]}"], [int_f, int_sn[0], int_sn[1], int_sn[2]], color=[COLORS["f"], COLORS["tail_0"], COLORS["tail_1"], COLORS["tail_2"]], alpha=0.80)
    ax_integral.set_ylim(0.0, max(int_f * 1.10, 1.0))
    ax_integral.grid(axis="y", color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_integral.set_ylabel("積分値")
    ax_integral.set_title("積分の収束", fontsize=14, pad=8)
    ax_integral.text(
        0.02,
        0.96,
        rf"$m(E_n)\approx {exc_measure:.4f}$" + "\n" + rf"$\int_{{Y_n}}(f-s_n)\approx {int_good:.4f}$" + "\n" + rf"$\int_{{E_n}}(f-s_n)\approx {int_exc:.4f}$",
        transform=ax_integral.transAxes,
        va="top",
        fontsize=10.5,
        color=COLORS["ink"],
        bbox={"boxstyle": "round, pad=0.20", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
    )

    ax_note.axis("off")
    ax_note.text(0.00, 0.72, r"Egorov's theorem の効果は, 収束列を ``小さい例外集合の外では一様収束'' という形で見直せることにある.", fontsize=12.2, color=COLORS["ink"])
    ax_note.text(0.00, 0.40, rf"ここでは $Y_n$ 上で tail $\{{s_k\}}_{{k\geq n}}$ が band $|s_k-f|\leq 2^{{-{n}}}$ に入り, 残りの誤差は $m(E_n)\to0$ の側へ追いやられる.", fontsize=12.0, color=COLORS["muted"])
    ax_note.text(0.00, 0.08, rf"その結果, $\int_X s_n\, dm \to \int_X f\, dm$ が図として読める.", fontsize=12.5, color=COLORS["band_edge"])

    fig.suptitle("Egorov's theorem と dyadic 単関数近似: Lebesgue 積分は単関数積分の極限で与えられる", fontsize=20, y=0.972)
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    frame_paths: list[Path] = []
    for frame_index, n in enumerate(N_VALUES):
        frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(frame_path, n)
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
