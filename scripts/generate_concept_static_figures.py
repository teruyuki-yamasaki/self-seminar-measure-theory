#!/usr/bin/env python3
"""Generate static concept figures for slides that are mostly textual."""

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
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle


OUTDIR = Path("figures/measure/static/concepts")

COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#d7dde6",
    "blue": "#2f6fed",
    "cyan": "#2cb4c8",
    "green": "#3aa76d",
    "yellow": "#f2b84b",
    "orange": "#e68a3f",
    "red": "#e85d5d",
    "purple": "#7b61ff",
    "panel": "#ffffff",
}


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


def save(fig: plt.Figure, name: str) -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTDIR / name, dpi=180, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def canvas(title: str, subtitle: str | None = None, *, figsize: tuple[float, float] = (9.6, 6.1)) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.text(0.35, 5.65, title, fontsize=22, weight="bold", ha="left", va="top")
    if subtitle:
        ax.text(0.35, 5.18, subtitle, fontsize=12.5, color=COLORS["muted"], ha="left", va="top")
    return fig, ax


def arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], color: str = COLORS["muted"], lw: float = 2.0) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=lw,
            color=color,
            shrinkA=6,
            shrinkB=6,
        )
    )


def card(ax: plt.Axes, xy: tuple[float, float], w: float, h: float, label: str, *, color: str = COLORS["blue"], fs: float = 13.5) -> None:
    x, y = xy
    ax.add_patch(Rectangle((x, y), w, h, facecolor=COLORS["panel"], edgecolor=color, lw=1.8, joinstyle="round"))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=COLORS["ink"], weight="bold")


def draw_finite_to_countable_shift() -> None:
    fig, ax = canvas("有限から可算へ", "測度論への本質的な移行点")
    for i, x in enumerate([0.8, 1.6, 2.4]):
        ax.add_patch(Rectangle((x, 2.35), 0.65, 0.9, facecolor=COLORS["yellow"], edgecolor=COLORS["ink"], lw=1.0, alpha=0.75))
    ax.text(1.9, 1.75, "有限個の基本図形", ha="center", fontsize=13.5, weight="bold")
    ax.text(1.9, 1.35, "Jordan 的近似", ha="center", fontsize=11.5, color=COLORS["muted"])
    arrow(ax, (3.4, 2.8), (5.1, 2.8), COLORS["blue"], 2.5)
    rng = np.random.default_rng(3)
    for idx in range(36):
        x = 5.7 + rng.random() * 3.2
        y = 1.3 + rng.random() * 2.8
        w = 0.15 + rng.random() * 0.25
        h = 0.08 + rng.random() * 0.22
        ax.add_patch(Rectangle((x, y), w, h, facecolor=COLORS["cyan"], edgecolor=COLORS["blue"], lw=0.45, alpha=0.45))
        if idx in {7, 15, 28}:
            ax.text(x + w / 2, y + h + 0.08, rf"$I_{{{idx + 1}}}$", fontsize=8.5, ha="center", color=COLORS["blue"])
    ax.text(7.35, 1.75, "可算個の被覆", ha="center", fontsize=13.5, weight="bold")
    ax.text(7.35, 1.35, "Lebesgue 外測度", ha="center", fontsize=11.5, color=COLORS["muted"])
    save(fig, "finite_to_countable_shift.png")


def draw_dct_condition_map() -> None:
    fig, ax = canvas("優収束定理の条件", "点wise 収束だけでなく, 質量の逃げを止める")
    xs = np.linspace(0.7, 5.0, 250)
    g = 3.7 - 0.7 * (xs - 2.8) ** 2
    g = np.maximum(g, 0.9)
    ax.fill_between(xs, 1.25, g, color=COLORS["cyan"], alpha=0.20)
    ax.plot(xs, g, color=COLORS["blue"], lw=2.8, label=r"$g$")
    for amp, color in [(1.0, COLORS["green"]), (0.76, COLORS["yellow"]), (0.52, COLORS["orange"])]:
        y = 1.25 + amp * (g - 1.25) * (0.72 + 0.12 * np.sin(5 * xs))
        ax.plot(xs, y, color=color, lw=2.0)
    ax.text(2.85, 4.15, r"$|f_n|\leq g,\quad g\in L^1$", ha="center", fontsize=16, weight="bold", color=COLORS["blue"])
    card(ax, (6.0, 3.55), 3.0, 0.75, "a.e. 収束", color=COLORS["green"])
    card(ax, (6.0, 2.55), 3.0, 0.75, "可積分な支配", color=COLORS["blue"])
    arrow(ax, (7.5, 2.45), (7.5, 1.45), COLORS["muted"])
    card(ax, (5.7, 0.55), 3.6, 0.8, r"$\int f_n\,d\mu\to\int f\,d\mu$", color=COLORS["purple"], fs=14)
    save(fig, "dominated_convergence_conditions.png")


def draw_half_open_interval_volume() -> None:
    fig, ax = plt.subplots(figsize=(10.6, 5.5))
    fig.patch.set_facecolor(COLORS["paper"])
    ax.set_facecolor(COLORS["paper"])
    ax.set_xlim(0, 9.2)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    x0, y0, w, h = 1.1, 1.45, 5.6, 3.0
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=COLORS["cyan"], edgecolor=COLORS["ink"], lw=2.0, alpha=0.28))
    ax.plot([x0, x0 + w], [y0, y0], color=COLORS["ink"], lw=2.2)
    ax.plot([x0, x0], [y0, y0 + h], color=COLORS["ink"], lw=2.2)
    ax.plot([x0 + w, x0 + w], [y0, y0 + h], color=COLORS["red"], lw=2.2, ls="--")
    ax.plot([x0, x0 + w], [y0 + h, y0 + h], color=COLORS["red"], lw=2.2, ls="--")
    ax.text(x0 + w / 2, y0 - 0.42, r"$[a_1,b_1)$", ha="center", fontsize=15)
    ax.text(x0 - 0.35, y0 + h / 2, r"$[a_2,b_2)$", ha="right", va="center", rotation=90, fontsize=15)
    ax.text(
        x0 + w / 2,
        y0 + h / 2,
        r"$m(I):=\prod_{k=1}^N(b_k-a_k)$",
        ha="center",
        va="center",
        fontsize=18,
        weight="bold",
        bbox={"boxstyle": "round,pad=0.28", "facecolor": COLORS["panel"], "edgecolor": "none", "alpha": 0.92},
    )
    ax.text(7.5, 3.55, "含む境界", fontsize=12.5, weight="bold", color=COLORS["ink"])
    ax.plot([7.2, 8.3], [3.25, 3.25], color=COLORS["ink"], lw=2.2)
    ax.text(7.5, 2.45, "含まない境界", fontsize=12.5, weight="bold", color=COLORS["red"])
    ax.plot([7.2, 8.3], [2.15, 2.15], color=COLORS["red"], lw=2.2, ls="--")
    save(fig, "half_open_interval_volume.png")


def draw_classical_area_convergence() -> None:
    fig, ax = canvas("古典的面積概念", "有限個の基本図形を増やし, 面積近似が極限へ近づく", figsize=(12.2, 7.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.2)

    left_center = np.array([3.1, 4.8])
    right_center = np.array([8.95, 4.8])
    radius = 1.52
    t = np.linspace(0, 2 * np.pi, 500)

    def regular_vertices(n: int, *, start_angle: float = np.pi / 2) -> np.ndarray:
        angles = start_angle + np.linspace(0, 2 * np.pi, n, endpoint=False)
        return np.c_[np.cos(angles), np.sin(angles)]

    def polygon_area(n: int) -> float:
        return 0.5 * n * np.sin(2 * np.pi / n)

    def rectangle_approx_area(strip_count: int) -> float:
        edges = np.linspace(-1, 1, strip_count + 1)
        total = 0.0
        for left, right in zip(edges[:-1], edges[1:]):
            height = 2 * np.sqrt(max(0.0, 1 - max(left * left, right * right)))
            total += (right - left) * height
        return total

    ax.text(left_center[0], 6.33, "円板を多角形で近似", ha="center", fontsize=15.5, weight="bold")
    ax.text(right_center[0], 6.33, "円板を長方形で近似", ha="center", fontsize=15.5, weight="bold")

    for center in [left_center, right_center]:
        ax.add_patch(Circle(tuple(center), radius, facecolor="#f7fbff", edgecolor=COLORS["blue"], lw=2.0, alpha=0.95))

    poly_colors = [COLORS["cyan"], COLORS["yellow"], COLORS["orange"]]
    poly_ns = [6, 12, 24]
    poly_old = regular_vertices(poly_ns[0])
    ax.add_patch(
        Polygon(left_center + radius * poly_old, closed=True, facecolor=poly_colors[0], edgecolor=COLORS["ink"], lw=1.0, alpha=0.62)
    )
    for idx, (n, color) in enumerate(zip(poly_ns[1:], poly_colors[1:]), start=1):
        poly_new = regular_vertices(n)
        tri_alpha = 0.72 if idx == 1 else 0.55
        for k in range(len(poly_old)):
            v_old = poly_old[k]
            w_left = poly_new[(2 * k - 1) % len(poly_new)]
            w_right = poly_new[(2 * k + 1) % len(poly_new)]
            tri = np.vstack([v_old, w_left, w_right])
            ax.add_patch(
                Polygon(left_center + radius * tri, closed=True, facecolor=color, edgecolor=COLORS["ink"], lw=0.65, alpha=tri_alpha)
            )
        poly_old = poly_new
    ax.plot(left_center[0] + radius * np.cos(t), left_center[1] + radius * np.sin(t), color=COLORS["blue"], lw=2.0)
    ax.text(left_center[0], 3.02, "隙間の扇形を三角形で刻んで足す", ha="center", fontsize=11.8, color=COLORS["muted"])

    rect_levels = [4, 8, 16]
    rect_colors = [COLORS["cyan"], COLORS["yellow"], COLORS["orange"]]
    previous = set()
    for strip_count, color in zip(rect_levels, rect_colors):
        edges = np.linspace(-1, 1, strip_count + 1)
        current = set()
        for left, right in zip(edges[:-1], edges[1:]):
            current.add((round(float(left), 6), round(float(right), 6)))
            key = (round(float(left), 6), round(float(right), 6))
            if key in previous:
                continue
            height = 2 * np.sqrt(max(0.0, 1 - max(left * left, right * right)))
            x = right_center[0] + radius * left
            y = right_center[1] - radius * height / 2
            w = radius * (right - left)
            h = radius * height
            ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor=COLORS["ink"], lw=0.55, alpha=0.62))
        previous = current
    ax.plot(right_center[0] + radius * np.cos(t), right_center[1] + radius * np.sin(t), color=COLORS["blue"], lw=2.0)
    ax.text(right_center[0], 3.02, "細分した長方形を追加して内側から埋める", ha="center", fontsize=11.8, color=COLORS["muted"])

    def draw_number_line(x0: float, x1: float, y: float, values: list[float], labels: list[str], limit_label: str) -> None:
        xmin = values[0] - 0.18
        xmax = np.pi + 0.16
        ax.plot([x0, x1], [y, y], color=COLORS["ink"], lw=1.4)
        for tick, lab in [(xmin, "0"), (np.pi, limit_label)]:
            px = x0 + (tick - xmin) / (xmax - xmin) * (x1 - x0)
            ax.plot([px, px], [y - 0.10, y + 0.10], color=COLORS["ink"], lw=1.2)
            ax.text(px, y - 0.28, lab, ha="center", va="top", fontsize=11.2)
        for i, (value, label) in enumerate(zip(values, labels)):
            px = x0 + (value - xmin) / (xmax - xmin) * (x1 - x0)
            color = poly_colors[min(i, len(poly_colors) - 1)]
            ax.plot([px, px], [y - 0.16, y + 0.16], color=color, lw=2.4)
            ax.scatter([px], [y], s=34, color=color, edgecolors=COLORS["ink"], linewidths=0.45, zorder=5)
            ax.text(px, y + 0.28, label, ha="center", va="bottom", fontsize=10.6, color=COLORS["ink"])
        limit_px = x0 + (np.pi - xmin) / (xmax - xmin) * (x1 - x0)
        ax.plot([limit_px, limit_px], [y - 0.22, y + 0.44], color=COLORS["red"], lw=1.8, ls="--")
        ax.text((x0 + x1) / 2, y - 0.62, "step ごとの近似面積が同じ極限へ集まる", ha="center", fontsize=11.2, color=COLORS["muted"])

    poly_values = [polygon_area(n) for n in [6, 12, 24, 48]]
    rect_values = [rectangle_approx_area(n) for n in [4, 8, 16, 32]]
    draw_number_line(0.9, 5.25, 1.65, poly_values, [r"$P_1$", r"$P_2$", r"$P_3$", r"$P_4$"], r"$\pi r^2$")
    draw_number_line(6.75, 11.1, 1.65, rect_values, [r"$R_1$", r"$R_2$", r"$R_3$", r"$R_4$"], r"$\pi r^2$")

    save(fig, "classical_area_coverings.png")


def draw_finite_additivity_blocks() -> None:
    fig, ax = canvas("有限加法性", "互いに素なら, 全体の大きさは部分の和")
    blocks = [
        (0.9, 1.45, 1.8, 2.5, COLORS["blue"], r"$E_1$"),
        (2.7, 1.45, 1.3, 1.4, COLORS["green"], r"$E_2$"),
        (4.0, 1.45, 1.9, 3.0, COLORS["yellow"], r"$E_3$"),
    ]
    for x, y, w, h, color, label in blocks:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor=COLORS["ink"], lw=1.4, alpha=0.42))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=17, weight="bold")
    arrow(ax, (6.25, 2.9), (7.2, 2.9), COLORS["muted"])
    ax.text(8.1, 3.25, r"$m(E_1\cup E_2\cup E_3)$", fontsize=15, ha="center", weight="bold")
    ax.text(8.1, 2.55, r"$=m(E_1)+m(E_2)+m(E_3)$", fontsize=15, ha="center", color=COLORS["blue"], weight="bold")
    ax.text(3.4, 0.85, "有限個に分ける限り, 足し算が壊れない", ha="center", fontsize=12.5, color=COLORS["muted"])
    save(fig, "finite_additivity_blocks.png")


def draw_jordan_inner_outer_static() -> None:
    fig, ax = canvas("Jordan 内測度と外測度", "内側から詰め, 外側から覆う")
    t = np.linspace(0, 2 * np.pi, 260)
    x = 3.1 + 1.55 * np.cos(t) + 0.25 * np.cos(3 * t)
    y = 2.75 + 1.15 * np.sin(t) + 0.18 * np.sin(2 * t)
    ax.add_patch(Polygon(np.c_[x, y], closed=True, facecolor="#e9f6ef", edgecolor=COLORS["green"], lw=2.2))
    for px, py in [(2.0, 2.1), (2.65, 2.1), (3.3, 2.1), (2.3, 2.75), (2.95, 2.75), (3.6, 2.75)]:
        ax.add_patch(Rectangle((px, py), 0.55, 0.45, facecolor=COLORS["green"], edgecolor=COLORS["ink"], lw=0.8, alpha=0.45))
    for px, py in [(1.5, 1.65), (2.1, 1.65), (2.7, 1.65), (3.3, 1.65), (3.9, 1.65), (1.5, 2.25), (4.1, 2.25), (1.8, 3.25), (3.6, 3.25)]:
        ax.add_patch(Rectangle((px, py), 0.58, 0.52, facecolor="none", edgecolor=COLORS["blue"], lw=1.1, ls="--"))
    ax.text(1.4, 4.65, r"$J_*(A)$: 内側近似", fontsize=13.5, color=COLORS["green"], weight="bold")
    ax.text(5.0, 4.65, r"$J^*(A)$: 外側近似", fontsize=13.5, color=COLORS["blue"], weight="bold")
    ax.text(7.4, 2.95, r"$J_*(A)=J^*(A)$", fontsize=16, ha="center", weight="bold")
    ax.text(7.4, 2.35, "なら Jordan 可測", fontsize=13, ha="center", color=COLORS["muted"])
    save(fig, "jordan_inner_outer_static.png")


def draw_countable_cover_plan() -> None:
    fig, ax = canvas("可算被覆", "集合を区間列で外側から覆う")
    rng = np.random.default_rng(12)
    pts = rng.normal(loc=(3.4, 2.7), scale=(1.0, 0.75), size=(70, 2))
    pts = pts[(pts[:, 0] > 1.0) & (pts[:, 0] < 5.7) & (pts[:, 1] > 1.1) & (pts[:, 1] < 4.4)]
    ax.scatter(pts[:, 0], pts[:, 1], s=18, color=COLORS["ink"], alpha=0.75)
    for i, (x, y, w, h) in enumerate([(1.4, 1.4, 1.8, 1.0), (2.7, 2.0, 1.9, 1.2), (3.8, 3.0, 1.4, 0.9), (1.9, 3.0, 1.5, 0.8), (4.6, 1.6, 0.9, 0.7)]):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=COLORS["cyan"], edgecolor=COLORS["blue"], lw=1.4, alpha=0.23))
        ax.text(x + w / 2, y + h + 0.08, rf"$I_{i + 1}$", ha="center", fontsize=11, color=COLORS["blue"])
    ax.text(7.25, 3.35, r"$A\subset\bigcup_{k=1}^{\infty} I_k$", fontsize=17, ha="center", weight="bold")
    ax.text(7.25, 2.55, r"$\sum_k m(I_k)$ を小さくする", fontsize=13.5, ha="center", color=COLORS["muted"])
    save(fig, "countable_cover_plan.png")


def draw_outer_measure_infimum() -> None:
    fig, ax = canvas("外測度は被覆コストの下限", "任意集合に定義できる代わりに, まずは劣加法性まで")
    heights = [3.6, 2.8, 2.25, 2.05]
    labels = ["粗い被覆", "細かい被覆", "より良い被覆", "下限"]
    for i, (h, label) in enumerate(zip(heights, labels)):
        x = 1.0 + i * 1.75
        ax.add_patch(Rectangle((x, 1.2), 0.75, h, facecolor=COLORS["blue"], edgecolor=COLORS["ink"], lw=1.0, alpha=0.35))
        ax.text(x + 0.38, 0.83, label, ha="center", fontsize=10.5)
        ax.text(x + 0.38, 1.35 + h, rf"$\sum m(I_k)$", ha="center", fontsize=10.5, color=COLORS["blue"])
    ax.axhline(3.25, xmin=0.08, xmax=0.78, color=COLORS["red"], lw=2.0, ls="--")
    ax.text(8.1, 3.25, r"$\mu^*(A)$", va="center", fontsize=17, color=COLORS["red"], weight="bold")
    ax.text(5.1, 5.0, "すべての可算被覆の中で最小限の外側コストを見る", ha="center", fontsize=12.5, color=COLORS["muted"])
    save(fig, "outer_measure_infimum.png")


def draw_measurable_cut_zero_set() -> None:
    fig, ax = canvas("零集合は可測", "測度 0 の側を切り出しても外測度は変わらない")
    ax.add_patch(Rectangle((1.1, 1.25), 5.0, 3.2, facecolor="#eef4ff", edgecolor=COLORS["blue"], lw=1.6))
    ax.text(3.6, 4.65, r"任意の集合 $A$", ha="center", fontsize=14, color=COLORS["blue"], weight="bold")
    rng = np.random.default_rng(7)
    xs = 1.5 + rng.random(20) * 4.2
    ys = 1.55 + rng.random(20) * 2.55
    ax.scatter(xs, ys, s=22, color=COLORS["red"], zorder=4)
    ax.text(6.6, 3.65, r"$E$: 零集合", fontsize=15, color=COLORS["red"], weight="bold")
    ax.text(6.6, 2.95, r"$\Gamma(E)=0$", fontsize=15, color=COLORS["red"])
    ax.text(6.6, 2.15, r"$\Gamma(A\cap E)=0$", fontsize=15, color=COLORS["ink"])
    ax.text(3.6, 0.75, r"$A=(A\cap E)\cup(A\cap E^c)$", ha="center", fontsize=15)
    save(fig, "measurable_cut_zero_set.png")


def draw_caratheodory_theorem_pipeline() -> None:
    fig, ax = canvas("Carathéodory の定理", "外測度から可算加法族と測度を取り出す")
    card(ax, (0.75, 3.1), 2.1, 1.0, "外測度\n$\\Gamma$", color=COLORS["blue"])
    card(ax, (3.95, 3.1), 2.3, 1.0, "可測集合族\n$\\mathfrak{M}_\\Gamma$", color=COLORS["green"])
    card(ax, (7.35, 3.1), 2.0, 1.0, "測度\n$\\Gamma|_{\\mathfrak{M}}$", color=COLORS["purple"])
    arrow(ax, (2.9, 3.6), (3.85, 3.6), COLORS["muted"])
    arrow(ax, (6.3, 3.6), (7.25, 3.6), COLORS["muted"])
    ax.text(3.4, 4.25, "切断条件で選ぶ", ha="center", fontsize=11.5, color=COLORS["muted"])
    ax.text(6.85, 4.25, "制限する", ha="center", fontsize=11.5, color=COLORS["muted"])
    ax.text(5.1, 1.9, "結果: 可算和に閉じ, 互いに素な可算和で加法的", ha="center", fontsize=13, weight="bold")
    save(fig, "caratheodory_theorem_pipeline.png")


def draw_lebesgue_measure_restriction() -> None:
    fig, ax = canvas("Lebesgue 測度は外測度の制限", "任意集合上の外測度から, 良い集合だけを選ぶ")
    ax.add_patch(Circle((3.0, 2.8), 1.75, facecolor=COLORS["cyan"], edgecolor=COLORS["blue"], lw=2.0, alpha=0.22))
    ax.add_patch(Circle((3.0, 2.8), 0.9, facecolor=COLORS["green"], edgecolor=COLORS["green"], lw=2.0, alpha=0.32))
    ax.text(3.0, 4.75, r"$\mathcal{P}(\mathbb{R}^N)$", ha="center", fontsize=15, color=COLORS["blue"], weight="bold")
    ax.text(3.0, 2.8, r"$\mathfrak{M}_{\mu^*}$", ha="center", va="center", fontsize=16, color=COLORS["green"], weight="bold")
    arrow(ax, (4.75, 2.8), (6.2, 2.8), COLORS["muted"])
    ax.text(7.8, 3.15, r"$\mu=\mu^*|_{\mathfrak{M}_{\mu^*}}$", ha="center", fontsize=18, weight="bold")
    ax.text(7.8, 2.45, "可測集合に制限して測度になる", ha="center", fontsize=12.5, color=COLORS["muted"])
    save(fig, "lebesgue_measure_restriction.png")


def draw_sigma_algebra_closure() -> None:
    fig, ax = canvas("可算加法族", "補集合と可算和に閉じる集合の言語")
    card(ax, (0.75, 3.25), 2.0, 0.85, r"$A\in\mathfrak{B}$", color=COLORS["blue"])
    card(ax, (4.0, 3.25), 2.0, 0.85, r"$A^c\in\mathfrak{B}$", color=COLORS["green"])
    card(ax, (7.05, 3.25), 2.1, 0.85, r"$\bigcup_n A_n\in\mathfrak{B}$", color=COLORS["purple"])
    arrow(ax, (2.85, 3.68), (3.9, 3.68), COLORS["muted"])
    arrow(ax, (6.1, 3.68), (6.95, 3.68), COLORS["muted"])
    for i in range(6):
        ax.add_patch(Circle((2.0 + 0.22 * i, 1.8 + 0.18 * (i % 2)), 0.28, facecolor=COLORS["blue"], edgecolor=COLORS["ink"], alpha=0.25))
    for i in range(6):
        ax.add_patch(Circle((7.0 + 0.28 * i, 1.7 + 0.15 * (i % 3)), 0.26, facecolor=COLORS["purple"], edgecolor=COLORS["ink"], alpha=0.25))
    ax.text(5.0, 1.05, "有限回だけでなく, 可算回の操作まで閉じる", ha="center", fontsize=13, color=COLORS["muted"])
    save(fig, "sigma_algebra_closure.png")


def draw_measure_additivity_partition() -> None:
    fig, ax = canvas("測度の可算加法性", "互いに素な部分の和が全体の大きさ")
    widths = [1.2, 0.9, 1.55, 0.75, 1.0]
    x = 1.0
    colors = [COLORS["blue"], COLORS["green"], COLORS["yellow"], COLORS["orange"], COLORS["purple"]]
    for i, (w, color) in enumerate(zip(widths, colors)):
        ax.add_patch(Rectangle((x, 1.8), w, 2.1, facecolor=color, edgecolor=COLORS["ink"], lw=1.0, alpha=0.42))
        ax.text(x + w / 2, 2.85, rf"$A_{i+1}$", ha="center", fontsize=14, weight="bold")
        x += w
    ax.text(3.7, 4.35, "互いに素", ha="center", fontsize=12.5, color=COLORS["muted"])
    ax.text(7.5, 3.55, r"$\mu(\cup_n A_n)$", ha="center", fontsize=18, weight="bold")
    ax.text(7.5, 2.65, r"$=\sum_n\mu(A_n)$", ha="center", fontsize=18, color=COLORS["blue"], weight="bold")
    save(fig, "measure_additivity_partition.png")


def draw_measure_space_examples() -> None:
    fig, ax = canvas("測度空間の例", "空間・測れる集合・測度を入れ替えて使う")
    card(ax, (0.65, 3.15), 2.6, 1.15, "Lebesgue\n空間", color=COLORS["blue"])
    card(ax, (3.7, 3.15), 2.6, 1.15, "Borel\n測度空間", color=COLORS["green"])
    card(ax, (6.75, 3.15), 2.6, 1.15, "確率\n空間", color=COLORS["purple"])
    ax.text(1.95, 2.35, r"$(\mathbb{R}^N,\mathfrak{M},\mu)$", ha="center", fontsize=12.5)
    ax.text(5.0, 2.35, r"$(\mathbb{R}^N,\mathfrak{B},\mu)$", ha="center", fontsize=12.5)
    ax.text(8.05, 2.35, r"$(\Omega,\mathfrak{B},P)$", ha="center", fontsize=12.5)
    ax.text(5.0, 1.35, "同じ公理で, 幾何・解析・確率を扱う", ha="center", fontsize=13, color=COLORS["muted"])
    save(fig, "measure_space_examples.png")


def draw_null_set_ae() -> None:
    fig, ax = canvas("零集合と a.e.", "測度 0 の例外を無視して同じと見る")
    xs = np.linspace(0.8, 8.8, 320)
    y = 2.8 + 0.65 * np.sin(1.2 * xs)
    ax.plot(xs, y, color=COLORS["blue"], lw=2.7, label=r"$f$")
    ax.plot(xs, y, color=COLORS["green"], lw=1.6, ls="--", label=r"$g$")
    exc = np.array([2.0, 4.2, 7.4])
    ey = 2.8 + 0.65 * np.sin(1.2 * exc)
    ax.scatter(exc, ey + np.array([0.9, -0.75, 0.55]), s=70, color=COLORS["red"], zorder=5)
    for x, y0 in zip(exc, ey):
        ax.plot([x, x], [y0 - 0.8, y0 + 0.9], color=COLORS["red"], lw=1.0, alpha=0.45)
    ax.text(5.0, 1.15, r"例外集合 $N$ の測度が 0 なら $f=g$ a.e.", ha="center", fontsize=15, weight="bold")
    save(fig, "null_set_ae.png")


def draw_indicator_function_set() -> None:
    fig, ax = canvas("定義函数", "集合を 0/1 の函数として見る")
    ax.add_patch(Rectangle((1.0, 1.1), 3.6, 3.3, facecolor="#f7fbff", edgecolor=COLORS["ink"], lw=1.2))
    ax.add_patch(Circle((2.8, 2.75), 0.95, facecolor=COLORS["blue"], edgecolor=COLORS["blue"], alpha=0.35))
    ax.text(2.8, 2.75, r"$E$", ha="center", va="center", fontsize=18, weight="bold")
    arrow(ax, (4.9, 2.75), (5.9, 2.75), COLORS["muted"])
    ax.plot([6.3, 9.1], [1.35, 1.35], color=COLORS["ink"], lw=1.2)
    ax.plot([6.3, 6.3], [1.35, 4.4], color=COLORS["ink"], lw=1.2)
    ax.hlines(3.7, 6.45, 7.55, color=COLORS["blue"], lw=4)
    ax.hlines(1.55, 7.6, 9.0, color=COLORS["muted"], lw=4)
    ax.text(6.1, 3.7, "1", ha="right", va="center", fontsize=12)
    ax.text(6.1, 1.55, "0", ha="right", va="center", fontsize=12)
    ax.text(7.75, 4.05, r"$\mathbf{1}_E(x)$", ha="center", fontsize=15, weight="bold")
    save(fig, "indicator_function_set.png")


def draw_simple_function_algebra() -> None:
    fig, ax = canvas("単函数の計算規則", "集合の足し算から函数の線形性へ")
    for i, (x, h, color) in enumerate([(1.0, 1.2, COLORS["blue"]), (2.3, 2.0, COLORS["green"]), (3.7, 0.9, COLORS["yellow"])]):
        ax.add_patch(Rectangle((x, 1.25), 1.0, h, facecolor=color, edgecolor=COLORS["ink"], lw=1.0, alpha=0.42))
        ax.text(x + 0.5, 1.0, rf"$E_{i+1}$", ha="center", fontsize=12)
    arrow(ax, (5.0, 2.5), (6.2, 2.5), COLORS["muted"])
    ax.text(7.7, 3.15, r"$\varphi=\sum a_k\mathbf{1}_{E_k}$", ha="center", fontsize=17, weight="bold")
    ax.text(7.7, 2.35, r"$\int\varphi\,d\mu=\sum a_k\mu(E_k)$", ha="center", fontsize=15, color=COLORS["blue"], weight="bold")
    ax.text(7.7, 1.55, "線形性・単調性がここから始まる", ha="center", fontsize=12.5, color=COLORS["muted"])
    save(fig, "simple_function_algebra.png")


def draw_nonnegative_integral_sup() -> None:
    fig, ax = canvas("非負可測函数の積分", "下からの単函数近似の上限")
    xs = np.linspace(0.8, 5.2, 300)
    f = 1.2 + 2.0 * np.exp(-0.6 * (xs - 3.0) ** 2) + 0.25 * np.sin(4 * xs)
    ax.plot(xs, f, color=COLORS["ink"], lw=2.6)
    for n, color in [(3, COLORS["yellow"]), (5, COLORS["green"]), (8, COLORS["blue"])]:
        edges = np.linspace(xs.min(), xs.max(), n + 1)
        for l, r in zip(edges[:-1], edges[1:]):
            mask = (xs >= l) & (xs <= r)
            h = f[mask].min()
            ax.add_patch(Rectangle((l, 1.0), r - l, h - 1.0, facecolor=color, edgecolor=color, alpha=0.12))
    ax.text(7.2, 3.45, r"$\int f\,d\mu$", fontsize=18, ha="center", weight="bold")
    ax.text(7.2, 2.72, r"$=\sup_{\varphi\leq f}\int\varphi\,d\mu$", fontsize=16, ha="center", color=COLORS["blue"], weight="bold")
    ax.text(3.0, 0.62, "単函数を細かくして下から近づける", fontsize=12.5, ha="center", color=COLORS["muted"])
    save(fig, "nonnegative_integral_sup.png")


def draw_positive_negative_parts() -> None:
    fig, ax = canvas("正部分と負部分", "一般の函数を非負函数二つへ分ける")
    xs = np.linspace(0.8, 8.8, 350)
    y = 0.8 * np.sin(1.8 * xs) + 0.35 * np.cos(0.8 * xs)
    base = 2.85
    ax.axhline(base, color=COLORS["ink"], lw=1.2)
    ax.plot(xs, base + y, color=COLORS["ink"], lw=2.5)
    ax.fill_between(xs, base, base + np.maximum(y, 0), color=COLORS["blue"], alpha=0.32, label=r"$f^+$")
    ax.fill_between(xs, base, base + np.minimum(y, 0), color=COLORS["red"], alpha=0.32, label=r"$f^-$")
    ax.text(2.0, 4.25, r"$f^+$", color=COLORS["blue"], fontsize=16, weight="bold")
    ax.text(5.7, 1.7, r"$f^-$", color=COLORS["red"], fontsize=16, weight="bold")
    ax.text(7.4, 4.3, r"$f=f^+-f^-$", fontsize=16, weight="bold")
    ax.text(7.4, 3.7, r"$|f|=f^++f^-$", fontsize=16, color=COLORS["blue"], weight="bold")
    save(fig, "positive_negative_parts.png")


def draw_l1_equivalence() -> None:
    fig, ax = canvas("$L^1$ と a.e. 同一視", "ノルム 0 は点ごとの 0 ではなく, a.e. で 0")
    xs = np.linspace(0.8, 8.8, 260)
    ax.axhline(2.75, color=COLORS["ink"], lw=1.2)
    ax.plot(xs, np.full_like(xs, 2.75), color=COLORS["blue"], lw=2.5)
    for x, h in [(2.0, 1.0), (4.1, 0.7), (6.9, 1.2)]:
        ax.vlines(x, 2.75, 2.75 + h, color=COLORS["red"], lw=3.0)
        ax.scatter([x], [2.75 + h], s=60, color=COLORS["red"], zorder=5)
    ax.text(5.0, 4.65, "点では値が違っても", ha="center", fontsize=13, color=COLORS["muted"])
    ax.text(5.0, 1.55, r"$\int |f-g|\,d\mu=0 \Longleftrightarrow f=g\ \mu\mathrm{-a.e.}$", ha="center", fontsize=17, weight="bold")
    save(fig, "l1_ae_equivalence.png")


def draw_fatou_liminf() -> None:
    fig, ax = canvas("Fatou の補題", "下側の極限は積分の liminf で押さえられる")
    xs = np.linspace(0.8, 5.3, 240)
    curves = []
    for k, color in enumerate([COLORS["yellow"], COLORS["green"], COLORS["cyan"], COLORS["blue"]]):
        y = 1.4 + 1.25 * np.exp(-0.55 * (xs - (2.3 + 0.28 * k)) ** 2) + 0.18 * np.sin((k + 2) * xs)
        curves.append(y)
        ax.plot(xs, y, color=color, lw=1.6, alpha=0.78)
    lower = np.minimum.reduce(curves)
    ax.fill_between(xs, 1.0, lower, color=COLORS["purple"], alpha=0.18)
    ax.plot(xs, lower, color=COLORS["purple"], lw=3.0)
    ax.text(3.1, 4.45, r"$\liminf f_n$", color=COLORS["purple"], fontsize=16, weight="bold")
    ax.text(7.25, 3.35, r"$\int \liminf f_n\,d\mu$", ha="center", fontsize=16, weight="bold")
    ax.text(7.25, 2.65, r"$\leq \liminf \int f_n\,d\mu$", ha="center", fontsize=16, color=COLORS["blue"], weight="bold")
    save(fig, "fatou_liminf.png")


def draw_measure_comparison_two_weights() -> None:
    fig, ax = canvas("二つの測度を比べる", "同じ集合でも, 測度により重みが違う")
    x = np.linspace(0.8, 8.8, 300)
    mu = 1.2 + 0.12 * np.sin(3 * x)
    nu = 1.2 + 1.6 * np.exp(-0.65 * (x - 5.1) ** 2)
    ax.fill_between(x, 1.0, mu, color=COLORS["blue"], alpha=0.25)
    ax.plot(x, mu, color=COLORS["blue"], lw=2.4)
    ax.fill_between(x, 1.0, nu, color=COLORS["orange"], alpha=0.25)
    ax.plot(x, nu, color=COLORS["orange"], lw=2.4)
    ax.text(2.0, 1.55, r"$\mu$: 基準の測度", color=COLORS["blue"], fontsize=13.5, weight="bold")
    ax.text(6.2, 3.55, r"$\nu$: 重み付き測度", color=COLORS["orange"], fontsize=13.5, weight="bold")
    ax.text(5.0, 0.55, "Radon-Nikodym の定理は, この重みを函数として表す", ha="center", fontsize=12.5, color=COLORS["muted"])
    save(fig, "measure_comparison_two_weights.png")


def draw_absolute_continuity_nulls() -> None:
    fig, ax = canvas("絶対連続性", r"$\mu$ で見えない集合は, $\nu$ でも見えない")
    ax.add_patch(Circle((2.8, 2.9), 1.7, facecolor=COLORS["blue"], edgecolor=COLORS["blue"], alpha=0.20, lw=2.0))
    ax.add_patch(Circle((2.8, 2.9), 0.55, facecolor=COLORS["paper"], edgecolor=COLORS["red"], lw=2.0, ls="--"))
    ax.text(2.8, 2.9, r"$N$", ha="center", va="center", fontsize=16, color=COLORS["red"], weight="bold")
    arrow(ax, (4.7, 2.9), (5.85, 2.9), COLORS["muted"])
    ax.text(7.45, 3.35, r"$\mu(N)=0$", ha="center", fontsize=17, color=COLORS["blue"], weight="bold")
    ax.text(7.45, 2.55, r"$\Longrightarrow\ \nu(N)=0$", ha="center", fontsize=17, color=COLORS["orange"], weight="bold")
    ax.text(5.0, 1.05, r"$\nu\ll\mu$", ha="center", fontsize=18, weight="bold")
    save(fig, "absolute_continuity_nulls.png")


def draw_rn_density_transform() -> None:
    fig, ax = canvas("Radon-Nikodym 微分", "測度変更を密度函数による重み付けとして読む")
    x = np.linspace(0.9, 5.2, 260)
    h = 1.05 + 1.0 * np.exp(-0.9 * (x - 3.2) ** 2) + 0.12 * np.sin(4 * x)
    ax.fill_between(x, 1.0, h, color=COLORS["green"], alpha=0.28)
    ax.plot(x, h, color=COLORS["green"], lw=2.8)
    ax.text(3.05, 4.05, r"$h=\frac{d\nu}{d\mu}$", ha="center", fontsize=18, color=COLORS["green"], weight="bold")
    arrow(ax, (5.5, 2.75), (6.35, 2.75), COLORS["muted"])
    ax.text(7.85, 3.25, r"$\nu(A)=\int_A h\,d\mu$", ha="center", fontsize=17, weight="bold")
    ax.text(7.85, 2.45, r"$\int f\,d\nu=\int f h\,d\mu$", ha="center", fontsize=16, color=COLORS["blue"], weight="bold")
    save(fig, "rn_density_transform.png")


def main() -> None:
    setup_style()
    draw_finite_to_countable_shift()
    draw_dct_condition_map()
    draw_half_open_interval_volume()
    draw_classical_area_convergence()
    draw_finite_additivity_blocks()
    draw_jordan_inner_outer_static()
    draw_countable_cover_plan()
    draw_outer_measure_infimum()
    draw_measurable_cut_zero_set()
    draw_caratheodory_theorem_pipeline()
    draw_lebesgue_measure_restriction()
    draw_sigma_algebra_closure()
    draw_measure_additivity_partition()
    draw_measure_space_examples()
    draw_null_set_ae()
    draw_indicator_function_set()
    draw_simple_function_algebra()
    draw_nonnegative_integral_sup()
    draw_positive_negative_parts()
    draw_l1_equivalence()
    draw_fatou_liminf()
    draw_measure_comparison_two_weights()
    draw_absolute_continuity_nulls()
    draw_rn_density_transform()
    print(f"Generated {len(list(OUTDIR.glob('*.png')))} concept figures in {OUTDIR}")


if __name__ == "__main__":
    main()
