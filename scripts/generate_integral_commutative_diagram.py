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
GENERAL_OUTPUT_FILE = OUTPUT_DIR / "integral_commutative_diagram.png"
RIEMANN_OUTPUT_FILE = OUTPUT_DIR / "integral_commutative_diagram_uniform_riemann.png"
DOMINATED_OUTPUT_FILE = OUTPUT_DIR / "integral_commutative_diagram_dominated_convergence.png"

FIGSIZE = (9.2, 3.1)
RIEMANN_FIGSIZE = (9.6, 3.2)
DPI = 320
X_LIMITS = (0.0, 10.0)
Y_LIMITS = (0.0, 3.4)

INK = "#000000"
BACKGROUND = "#ffffff"

TOP_Y = 2.45
BOTTOM_Y = 0.95
LEFT_X = 3.05
RIGHT_X = 6.95
DEFINITION_X = 7.25
DEFINITION_Y = 1.72

NODE_FONT_SIZE = 25
LABEL_FONT_SIZE = 20
QUESTION_FONT_SIZE = 22
DEFINITION_FONT_SIZE = 26
BOTTOM_LONG_FONT_SIZE = 21
ARROW_LABEL_FONT_SIZE = 15

ARROW_LINEWIDTH = 1.8
ARROW_MUTATION_SCALE = 17
HORIZONTAL_NODE_GAP = 0.52
VERTICAL_NODE_GAP = 0.36
BOTTOM_LONG_GAP = 1.48
ARROW_LABEL_Y_OFFSET = 0.42


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
            "font.sans-serif": [
                "Hiragino Sans",
                "Yu Gothic",
                "Noto Sans CJK JP",
                "IPAexGothic",
                "DejaVu Sans",
            ],
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


def draw_label(ax: plt.Axes, x: float, y: float, text: str, fontsize: float = ARROW_LABEL_FONT_SIZE) -> None:
    ax.text(x, y, text, ha="center", va="bottom", fontsize=fontsize, color=INK, family="sans-serif")


def draw_diagram(
    output_file: Path,
    *,
    top_label: str | None = None,
    show_question: bool = True,
    bottom_left: str = r"$\int_X f_n\,d\mu$",
    bottom_right: str = r"$\int_X f\,d\mu$",
    vertical_label: str = r"$\int$",
    definition: str | None = None,
    bottom_font_size: float = NODE_FONT_SIZE,
    horizontal_gap: float = HORIZONTAL_NODE_GAP,
    figsize: tuple[float, float] = FIGSIZE,
    left_x: float = LEFT_X,
    right_x: float = RIGHT_X,
    top_label_font_size: float = ARROW_LABEL_FONT_SIZE,
) -> None:
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*X_LIMITS)
    ax.set_ylim(*Y_LIMITS)
    ax.axis("off")

    draw_text(ax, left_x, TOP_Y, r"$f_n$", NODE_FONT_SIZE)
    draw_text(ax, right_x, TOP_Y, r"$f$", NODE_FONT_SIZE)
    draw_text(ax, left_x, BOTTOM_Y, bottom_left, bottom_font_size)
    draw_text(ax, right_x, BOTTOM_Y, bottom_right, bottom_font_size)

    draw_arrow(
        ax,
        (left_x + HORIZONTAL_NODE_GAP, TOP_Y),
        (right_x - HORIZONTAL_NODE_GAP, TOP_Y),
    )
    if top_label:
        draw_label(ax, (left_x + right_x) / 2, TOP_Y + ARROW_LABEL_Y_OFFSET, top_label, top_label_font_size)
    draw_arrow(
        ax,
        (left_x, TOP_Y - VERTICAL_NODE_GAP),
        (left_x, BOTTOM_Y + VERTICAL_NODE_GAP),
    )
    draw_arrow(
        ax,
        (right_x, TOP_Y - VERTICAL_NODE_GAP),
        (right_x, BOTTOM_Y + VERTICAL_NODE_GAP),
    )
    draw_arrow(
        ax,
        (left_x + horizontal_gap, BOTTOM_Y),
        (right_x - horizontal_gap, BOTTOM_Y),
    )

    draw_text(ax, left_x - 0.42, (TOP_Y + BOTTOM_Y) / 2, vertical_label, LABEL_FONT_SIZE)
    draw_text(ax, right_x + 0.42, (TOP_Y + BOTTOM_Y) / 2, vertical_label, LABEL_FONT_SIZE)
    if show_question:
        draw_text(ax, (left_x + right_x) / 2, BOTTOM_Y + 0.34, r"$?$", QUESTION_FONT_SIZE)

    if definition:
        draw_text(ax, DEFINITION_X, DEFINITION_Y, definition, DEFINITION_FONT_SIZE)

    fig.savefig(output_file, dpi=DPI, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def main() -> None:
    setup_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    draw_diagram(
        GENERAL_OUTPUT_FILE,
        bottom_font_size=BOTTOM_LONG_FONT_SIZE,
        horizontal_gap=BOTTOM_LONG_GAP,
    )
    draw_diagram(
        RIEMANN_OUTPUT_FILE,
        top_label="一様収束",
        show_question=False,
        bottom_left=r"$\int_a^b f_n(x)\,dx$",
        bottom_right=r"$\int_a^b f(x)\,dx$",
        vertical_label=r"$\int$",
        definition=None,
        bottom_font_size=BOTTOM_LONG_FONT_SIZE,
        horizontal_gap=BOTTOM_LONG_GAP,
        figsize=RIEMANN_FIGSIZE,
        left_x=2.20,
        right_x=6.30,
    )
    draw_diagram(
        DOMINATED_OUTPUT_FILE,
        top_label="概収束 + 可積分な支配",
        show_question=False,
        bottom_font_size=BOTTOM_LONG_FONT_SIZE,
        horizontal_gap=BOTTOM_LONG_GAP,
        top_label_font_size=13,
    )
    for output_file in [GENERAL_OUTPUT_FILE, RIEMANN_OUTPUT_FILE, DOMINATED_OUTPUT_FILE]:
        print(output_file)


if __name__ == "__main__":
    main()
