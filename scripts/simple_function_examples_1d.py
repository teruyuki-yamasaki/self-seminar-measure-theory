#!/usr/bin/env python3
"""Generate static examples of simple functions on finite partitions of [a, b]."""

from __future__ import annotations

import os
from pathlib import Path
import tempfile

_CACHE_ROOT = Path(tempfile.gettempdir()) / "math_measure_animation_cache"
(_CACHE_ROOT / "matplotlib").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(_CACHE_ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(_CACHE_ROOT / "matplotlib"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#c8d1dc",
    "palette": ["#79aee8", "#8bc89f", "#f0b45a", "#d97b7b", "#8a73d6", "#66bdb2"],
}

OUTDIR = Path("figures/measure/static")
OUTPATH = OUTDIR / "simple_function_examples_1d.png"


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


def example_specs() -> list[dict[str, object]]:
    return [
        {
            "title": r"例1: 3 分割",
            "edges": np.array([0.0, 0.9, 2.2, 3.0]),
            "values": np.array([0.4, 1.1, 0.7]),
            "labels": [r"$A_1$", r"$A_2$", r"$A_3$"],
        },
        {
            "title": r"例2: 4 分割",
            "edges": np.array([-1.0, -0.3, 0.4, 1.5, 2.0]),
            "values": np.array([1.2, 0.3, 0.9, 1.4]),
            "labels": [r"$A_1$", r"$A_2$", r"$A_3$", r"$A_4$"],
        },
        {
            "title": r"例3: 5 分割",
            "edges": np.array([1.0, 1.3, 1.9, 2.8, 3.4, 4.0]),
            "values": np.array([0.5, 1.3, 0.6, 1.0, 0.2]),
            "labels": [r"$A_1$", r"$A_2$", r"$A_3$", r"$A_4$", r"$A_5$"],
        },
    ]


def draw_example(ax_step: plt.Axes, spec: dict[str, object], palette_offset: int) -> None:
    edges = np.asarray(spec["edges"], dtype=float)
    values = np.asarray(spec["values"], dtype=float)
    labels = list(spec["labels"])
    colors = [COLORS["palette"][(palette_offset + i) % len(COLORS["palette"])] for i in range(len(values))]

    x_left = float(edges[0])
    x_right = float(edges[-1])

    for idx, (left, right, value, label) in enumerate(zip(edges[:-1], edges[1:], values, labels)):
        color = colors[idx]
        width = right - left
        ax_step.add_patch(
            Rectangle(
                (left, 0.0),
                width,
                value,
                facecolor=color,
                edgecolor=COLORS["ink"],
                lw=1.0,
                alpha=0.38,
                zorder=2,
            )
        )
        ax_step.hlines(value, left, right, color=color, lw=4.0, zorder=3)
        ax_step.vlines([left, right], 0.0, value, color=color, lw=1.2, alpha=0.75, zorder=3)
        ax_step.text(0.5 * (left + right), value + 0.06, rf"$a_{idx+1}$", ha="center", va="bottom", fontsize=11.5, color=color)
        ax_step.text(
            0.5 * (left + right),
            max(0.08, 0.12 * value),
            label,
            ha="center",
            va="center",
            fontsize=12,
            color=COLORS["ink"],
            zorder=4,
        )
        ax_step.annotate(
            "",
            xy=(left, 0.03),
            xytext=(right, 0.03),
            arrowprops={"arrowstyle": "<->", "color": color, "lw": 1.4},
            annotation_clip=False,
        )
        ax_step.text(
            0.5 * (left + right),
            0.01,
            rf"$\mu(A_{idx+1})={width:.2f}$",
            ha="center",
            va="top",
            fontsize=10.5,
            color=color,
            clip_on=False,
        )

    ax_step.set_xlim(x_left, x_right)
    ax_step.set_ylim(0.0, max(values) + 0.35)
    ax_step.set_xticks(edges)
    ax_step.set_yticks(np.linspace(0.0, max(values), 4))
    ax_step.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_step.set_ylabel(r"$\varphi(x)$")
    ax_step.set_title(spec["title"], fontsize=14, pad=8)
    ax_step.text(
        0.56,
        0.83,
        rf"$\varphi(x)=\sum_{{i=1}}^n a_i \mathbf{{1}}_{{A_i}}(x)$",
        transform=ax_step.transAxes,
        ha="center",
        va="top",
        fontsize=11.0,
        color=COLORS["muted"],
    )
    ax_step.set_xlabel(r"幅が測度 $\mu(A_i)$ を表す区間分割")


def build_image() -> None:
    setup_style()
    OUTDIR.mkdir(parents=True, exist_ok=True)

    specs = example_specs()
    fig = plt.figure(figsize=(14.0, 9.6))

    top = 0.93
    left = 0.08
    width = 0.84
    block_height = 0.24
    gap = 0.055

    for idx, spec in enumerate(specs):
        y_base = top - idx * (block_height + gap) - block_height
        ax_step = fig.add_axes([left, y_base, width, 0.20])
        draw_example(ax_step, spec, palette_offset=2 * idx)

    fig.suptitle("単函数の例: 区間 $[a, b]$ の有限分割ごとに定数値を割り当てる", fontsize=22, y=0.98)
    fig.text(
        0.5,
        0.028,
        r"各長方形で, 高さが係数 $a_i$, 幅が測度 $\mu(A_i)$ を表し, 面積 $a_i\mu(A_i)$ が単函数積分の各項に対応する.",
        ha="center",
        fontsize=12.5,
        color=COLORS["muted"],
    )
    fig.savefig(OUTPATH, dpi=180)
    plt.close(fig)
    print(f"Saved image to: {OUTPATH.resolve()}")


if __name__ == "__main__":
    build_image()
