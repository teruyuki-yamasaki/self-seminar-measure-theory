#!/usr/bin/env python3
"""Animate simple functions on a finite partition of a 2D rectangle."""

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
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#c8d1dc",
    "base": "#7ea6d9",
    "accent": "#d97706",
    "highlight": "#d95f5f",
    "shadow": "#4b6f9f",
}

OUTDIR = Path("figures/measure/animations/simple_function_examples_2d")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "simple_function_examples_2d.gif"

FRAME_DURATION = 0.95
GIF_LOOP = 0


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


def frame_specs() -> list[dict[str, object]]:
    return [
        {
            "title": "例1: 2×2 分割",
            "x_edges": np.array([0.0, 0.9, 2.0]),
            "y_edges": np.array([0.0, 1.0, 2.0]),
            "heights": np.array([[0.40, 0.85], [1.00, 0.55]]),
        },
        {
            "title": "例2: x方向を細分",
            "x_edges": np.array([0.0, 0.6, 1.4, 2.0]),
            "y_edges": np.array([0.0, 1.0, 2.0]),
            "heights": np.array([[0.35, 0.72], [0.92, 1.08], [0.64, 0.48]]),
        },
        {
            "title": "例3: y方向も細分",
            "x_edges": np.array([0.0, 0.6, 1.4, 2.0]),
            "y_edges": np.array([0.0, 0.7, 1.4, 2.0]),
            "heights": np.array([[0.24, 0.60, 0.92], [0.84, 1.12, 0.78], [0.52, 0.70, 0.40]]),
        },
        {
            "title": "例4: 長方形ごとに高さを割当てる",
            "x_edges": np.array([0.0, 0.5, 1.0, 1.55, 2.0]),
            "y_edges": np.array([0.0, 0.9, 1.55, 2.0]),
            "heights": np.array(
                [
                    [0.20, 0.54, 0.88],
                    [0.68, 0.95, 0.72],
                    [0.42, 1.10, 0.58],
                    [0.76, 0.62, 0.30],
                ]
            ),
        },
        {
            "title": "例5: 単函数積分は長方形の体積和",
            "x_edges": np.array([0.0, 0.5, 1.0, 1.55, 2.0]),
            "y_edges": np.array([0.0, 0.9, 1.55, 2.0]),
            "heights": np.array(
                [
                    [0.20, 0.54, 0.88],
                    [0.68, 0.95, 0.72],
                    [0.42, 1.10, 0.58],
                    [0.76, 0.62, 0.30],
                ]
            ),
            "focus": (2, 1),
        },
    ]


def cell_color(height: float, max_height: float) -> tuple[float, float, float, float]:
    t = 0.25 + 0.75 * height / max_height
    return plt.get_cmap("YlOrRd")(t)


def cuboid_faces(x0: float, x1: float, y0: float, y1: float, h: float) -> list[list[tuple[float, float, float]]]:
    return [
        [(x0, y0, 0.0), (x1, y0, 0.0), (x1, y1, 0.0), (x0, y1, 0.0)],
        [(x0, y0, h), (x1, y0, h), (x1, y1, h), (x0, y1, h)],
        [(x0, y0, 0.0), (x1, y0, 0.0), (x1, y0, h), (x0, y0, h)],
        [(x1, y0, 0.0), (x1, y1, 0.0), (x1, y1, h), (x1, y0, h)],
        [(x1, y1, 0.0), (x0, y1, 0.0), (x0, y1, h), (x1, y1, h)],
        [(x0, y1, 0.0), (x0, y0, 0.0), (x0, y0, h), (x0, y1, h)],
    ]


def draw_3d_panel(ax: plt.Axes, spec: dict[str, object]) -> None:
    x_edges = np.asarray(spec["x_edges"], dtype=float)
    y_edges = np.asarray(spec["y_edges"], dtype=float)
    heights = np.asarray(spec["heights"], dtype=float)
    focus = spec.get("focus")
    max_height = float(np.max(heights))

    for i, (x0, x1) in enumerate(zip(x_edges[:-1], x_edges[1:])):
        for j, (y0, y1) in enumerate(zip(y_edges[:-1], y_edges[1:])):
            h = float(heights[i, j])
            rgba = list(cell_color(h, max_height))
            edge = COLORS["shadow"]
            alpha = 0.72
            if focus == (i, j):
                rgba = list(matplotlib.colors.to_rgba(COLORS["highlight"]))
                edge = COLORS["highlight"]
                alpha = 0.88
            rgba[3] = alpha
            faces = cuboid_faces(x0, x1, y0, y1, h)
            ax.add_collection3d(
                Poly3DCollection(
                    faces,
                    facecolors=rgba,
                    edgecolors=edge,
                    linewidths=0.8,
                )
            )
            ax.text(
                0.5 * (x0 + x1),
                0.5 * (y0 + y1),
                h + 0.05,
                rf"$a_{{{i+1}, {j+1}}}$",
                ha="center",
                va="bottom",
                fontsize=10.5,
                color=COLORS["ink"],
            )

    ax.set_xlim(x_edges[0], x_edges[-1])
    ax.set_ylim(y_edges[0], y_edges[-1])
    ax.set_zlim(0.0, max_height + 0.22)
    ax.view_init(elev=29, azim=-55)
    ax.set_xlabel("x", labelpad=8)
    ax.set_ylabel("y", labelpad=8)
    ax.set_zlabel(r"$\varphi(x, y)$", labelpad=8)
    ax.set_xticks(x_edges)
    ax.set_yticks(y_edges)
    ax.set_zticks(np.linspace(0.0, max_height, 5))
    ax.xaxis.pane.set_facecolor(matplotlib.colors.to_rgba(COLORS["paper"], 1.0))
    ax.yaxis.pane.set_facecolor(matplotlib.colors.to_rgba(COLORS["paper"], 1.0))
    ax.zaxis.pane.set_facecolor(matplotlib.colors.to_rgba(COLORS["paper"], 1.0))
    ax.xaxis._axinfo["grid"]["color"] = COLORS["grid"]
    ax.yaxis._axinfo["grid"]["color"] = COLORS["grid"]
    ax.zaxis._axinfo["grid"]["color"] = COLORS["grid"]
    ax.set_title(r"曲面ではなく, 各長方形で一定値をとる", fontsize=15, pad=12)


def draw_partition_panel(ax: plt.Axes, spec: dict[str, object]) -> None:
    x_edges = np.asarray(spec["x_edges"], dtype=float)
    y_edges = np.asarray(spec["y_edges"], dtype=float)
    heights = np.asarray(spec["heights"], dtype=float)
    focus = spec.get("focus")
    max_height = float(np.max(heights))

    for i, (x0, x1) in enumerate(zip(x_edges[:-1], x_edges[1:])):
        for j, (y0, y1) in enumerate(zip(y_edges[:-1], y_edges[1:])):
            h = float(heights[i, j])
            area = (x1 - x0) * (y1 - y0)
            color = cell_color(h, max_height)
            edge = COLORS["shadow"]
            lw = 1.0
            alpha = 0.42
            if focus == (i, j):
                color = matplotlib.colors.to_rgba(COLORS["highlight"], 0.55)
                edge = COLORS["highlight"]
                lw = 2.0
                alpha = 0.65
            ax.add_patch(
                Rectangle(
                    (x0, y0),
                    x1 - x0,
                    y1 - y0,
                    facecolor=color,
                    edgecolor=edge,
                    lw=lw,
                    alpha=alpha,
                )
            )
            ax.text(
                0.5 * (x0 + x1),
                0.5 * (y0 + y1) + 0.12,
                rf"$A_{{{i+1}, {j+1}}}$",
                ha="center",
                va="center",
                fontsize=10.5,
                color=COLORS["ink"],
            )
            label = rf"$\mu(A_{{{i+1}, {j+1}}})={area:.2f}$" if focus == (i, j) else rf"${area:.2f}$"
            ax.text(
                0.5 * (x0 + x1),
                0.5 * (y0 + y1) - 0.08,
                label,
                ha="center",
                va="center",
                fontsize=9.7,
                color=COLORS["muted"],
            )

    ax.set_xlim(x_edges[0], x_edges[-1])
    ax.set_ylim(y_edges[0], y_edges[-1])
    ax.set_aspect("equal")
    ax.set_xticks(x_edges)
    ax.set_yticks(y_edges)
    ax.grid(color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(r"底面では有限分割 $\{A_{ij}\}$ が見える", fontsize=15, pad=10)


def draw_formula_panel(ax: plt.Axes, spec: dict[str, object]) -> None:
    heights = np.asarray(spec["heights"], dtype=float)
    x_edges = np.asarray(spec["x_edges"], dtype=float)
    y_edges = np.asarray(spec["y_edges"], dtype=float)
    focus = spec.get("focus")

    terms: list[str] = []
    focus_text = ""
    for i, (x0, x1) in enumerate(zip(x_edges[:-1], x_edges[1:])):
        for j, (y0, y1) in enumerate(zip(y_edges[:-1], y_edges[1:])):
            area = (x1 - x0) * (y1 - y0)
            h = float(heights[i, j])
            if focus == (i, j):
                focus_text = rf"$a_{{{i+1}, {j+1}}}\mu(A_{{{i+1}, {j+1}}}) = {h:.2f}\times {area:.2f} = {h * area:.2f}$"
            if len(terms) < 3:
                terms.append(rf"{h:.2f}\times {area:.2f}")

    approx_integral = float(
        np.sum(heights * np.diff(x_edges)[:, None] * np.diff(y_edges)[None, :])
    )

    ax.axis("off")
    ax.text(
        0.02,
        0.85,
        r"$\varphi(x,y)=\sum_{i,j} a_{ij}\mathbf{1}_{A_{ij}}(x,y)$",
        fontsize=16,
        color=COLORS["ink"],
    )
    ax.text(
        0.02,
        0.58,
        r"$\int_X \varphi(x,y)\, d\mu = \sum_{i,j} a_{ij}\mu(A_{ij})$",
        fontsize=16,
        color=COLORS["accent"],
    )
    ax.text(
        0.02,
        0.36,
        " + ".join(terms) + (" + ..." if heights.size > len(terms) else ""),
        fontsize=11.8,
        color=COLORS["muted"],
    )
    ax.text(
        0.02,
        0.16,
        rf"この例では体積和はおよそ ${approx_integral:.2f}$",
        fontsize=13,
        color=COLORS["ink"],
    )
    if focus_text:
        ax.text(
            0.02,
            -0.02,
            focus_text,
            fontsize=12.8,
            color=COLORS["highlight"],
        )


def draw_frame(save_path: Path, spec: dict[str, object]) -> None:
    fig = plt.figure(figsize=(14.2, 8.4))
    ax_3d = fig.add_axes([0.05, 0.18, 0.50, 0.66], projection="3d")
    ax_partition = fig.add_axes([0.61, 0.34, 0.31, 0.41])
    ax_formula = fig.add_axes([0.58, 0.08, 0.36, 0.18])

    draw_3d_panel(ax_3d, spec)
    draw_partition_panel(ax_partition, spec)
    draw_formula_panel(ax_formula, spec)

    fig.suptitle("2 次元の単函数: 各小長方形で一定値をとる階段状の函数", fontsize=21, y=0.97)
    fig.text(0.5, 0.89, str(spec["title"]), ha="center", fontsize=15, color=COLORS["ink"])
    fig.text(
        0.5,
        0.03,
        "定義域を有限個の可測集合に分割し, 各部分集合で定数値を与えると 2 次元の単函数になる. 積分は各値と測度の積の総和で与えられる.",
        ha="center",
        fontsize=11.7,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    frame_paths: list[Path] = []
    for frame_index, spec in enumerate(frame_specs()):
        frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(frame_path, spec)
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
