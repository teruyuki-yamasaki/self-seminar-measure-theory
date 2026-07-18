#!/usr/bin/env python3
"""Generate a commutative-diagram style figure for integral convergence."""

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
from matplotlib.patches import FancyArrowPatch


OUTPUT_DIR = Path("figures/measure/static/concepts")
OUTPUT_FILE = OUTPUT_DIR / "integral_commutative_diagram.png"

FIGSIZE = (9.2, 3.1)
DPI = 320
X_LIMITS = (0.0, 10.0)
Y_LIMITS = (0.0, 3.4)

INK = "#000000"
BACKGROUND = "#ffffff"

TOP_Y = 2.45
BOTTOM_Y = 0.95
LEFT_X = 1.65
RIGHT_X = 4.15
DEFINITION_X = 7.25
DEFINITION_Y = 1.72

NODE_FONT_SIZE = 25
LABEL_FONT_SIZE = 20
QUESTION_FONT_SIZE = 22
DEFINITION_FONT_SIZE = 26

ARROW_LINEWIDTH = 1.8
ARROW_MUTATION_SCALE = 17
HORIZONTAL_NODE_GAP = 0.52
VERTICAL_NODE_GAP = 0.36


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
            "mathtext.fontset": "dejavuserif",
            "figure.facecolor": BACKGROUND,
            "savefig.facecolor": BACKGROUND,
            "axes.facecolor": BACKGROUND,
            "text.color": INK,
        }
    )


def draw_arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="->",
            mutation_scale=ARROW_MUTATION_SCALE,
            linewidth=ARROW_LINEWIDTH,
            color=INK,
            shrinkA=0,
            shrinkB=0,
        )
    )


def draw_text(ax: plt.Axes, x: float, y: float, text: str, fontsize: float) -> None:
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, color=INK)


def main() -> None:
    setup_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_xlim(*X_LIMITS)
    ax.set_ylim(*Y_LIMITS)
    ax.axis("off")

    draw_text(ax, LEFT_X, TOP_Y, r"$f_n$", NODE_FONT_SIZE)
    draw_text(ax, RIGHT_X, TOP_Y, r"$f$", NODE_FONT_SIZE)
    draw_text(ax, LEFT_X, BOTTOM_Y, r"$I(f_n)$", NODE_FONT_SIZE)
    draw_text(ax, RIGHT_X, BOTTOM_Y, r"$I(f)$", NODE_FONT_SIZE)

    draw_arrow(
        ax,
        (LEFT_X + HORIZONTAL_NODE_GAP, TOP_Y),
        (RIGHT_X - HORIZONTAL_NODE_GAP, TOP_Y),
    )
    draw_arrow(
        ax,
        (LEFT_X, TOP_Y - VERTICAL_NODE_GAP),
        (LEFT_X, BOTTOM_Y + VERTICAL_NODE_GAP),
    )
    draw_arrow(
        ax,
        (RIGHT_X, TOP_Y - VERTICAL_NODE_GAP),
        (RIGHT_X, BOTTOM_Y + VERTICAL_NODE_GAP),
    )
    draw_arrow(
        ax,
        (LEFT_X + 0.78, BOTTOM_Y),
        (RIGHT_X - 0.68, BOTTOM_Y),
    )

    draw_text(ax, LEFT_X - 0.42, (TOP_Y + BOTTOM_Y) / 2, r"$I$", LABEL_FONT_SIZE)
    draw_text(ax, RIGHT_X + 0.42, (TOP_Y + BOTTOM_Y) / 2, r"$I$", LABEL_FONT_SIZE)
    draw_text(ax, (LEFT_X + RIGHT_X) / 2, BOTTOM_Y + 0.34, r"$?$", QUESTION_FONT_SIZE)

    draw_text(ax, DEFINITION_X, DEFINITION_Y, r"$I(f)=\int_X f\,d\mu$", DEFINITION_FONT_SIZE)

    fig.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
