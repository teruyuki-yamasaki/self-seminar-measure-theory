#!/usr/bin/env python3
"""Conceptual animation for outer approximation of rational points in [0, 1]^2."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, sqrt
from pathlib import Path
import shutil

import imageio
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "irrational": "#2c7fb8",
    "cover": "#f0b45a",
    "cover_edge": "#a85b00",
    "point": "#c03a2b",
    "old_point": "#7b241c",
    "grid": "#c8d1dc",
    "gap": "#d95f5f",
}

OUTDIR = Path("figures/measure/animations/rational_points_outer_approx")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "rational_points_outer_approx.gif"

EPSILON = 0.08
N_STEPS = 10
FRAME_DURATION = 0.5
GIF_LOOP = 0
RESOLUTION = 220
EPSILON_STAGES = [0.08, 0.05, 0.03, 0.015]


@dataclass(frozen=True)
class CoverRect:
    x0: float
    y0: float
    width: float
    height: float
    area_bound: float


@dataclass(frozen=True)
class RationalPoint:
    x: float
    y: float
    label: str
    complexity: int
    center_distance: float
    edge_distance: float


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


def rational_axis(max_denominator: int = 9) -> list[tuple[int, int]]:
    vals: list[tuple[int, int]] = []
    for q in range(1, max_denominator + 1):
        for p in range(q + 1):
            if gcd(p, q) == 1:
                vals.append((p, q))
    vals.sort(key=lambda item: (item[1], item[0]))
    return vals


def rational_points(limit: int = 400) -> list[RationalPoint]:
    axis = rational_axis()
    rng = np.random.default_rng(23)
    items: list[RationalPoint] = []
    for px, qx in axis:
        for py, qy in axis:
            x = px / qx
            y = py / qy
            center_distance = (x - 0.5) ** 2 + (y - 0.5) ** 2
            roughness = rng.uniform(0.0, 0.06)
            items.append(
                RationalPoint(
                    x=x,
                    y=y,
                    label=rf"$({px}/{qx}, {py}/{qy})$",
                    complexity=qx + qy,
                    center_distance=center_distance + roughness,
                    edge_distance=min(x, 1.0 - x, y, 1.0 - y),
                )
            )
    items.sort(key=lambda item: (item.complexity, item.center_distance, -item.edge_distance, item.x, item.y))
    unique: list[RationalPoint] = []
    seen: set[tuple[float, float]] = set()
    for point in items:
        key = (round(point.x, 12), round(point.y, 12))
        if key in seen:
            continue
        seen.add(key)
        unique.append(point)
        if len(unique) >= limit:
            break
    return unique


def point_is_covered(point: tuple[float, float], covers: list[CoverRect]) -> bool:
    x, y = point
    return any(rect.x0 <= x <= rect.x0 + rect.width and rect.y0 <= y <= rect.y0 + rect.height for rect in covers)


def choose_next_point(candidates: list[RationalPoint], covers: list[CoverRect], chosen_points: list[RationalPoint]) -> RationalPoint:
    uncovered = [point for point in candidates if not point_is_covered((point.x, point.y), covers)]
    if not uncovered:
        raise RuntimeError("Ran out of rational point candidates.")

    if not chosen_points:
        return min(uncovered, key=lambda point: (point.center_distance, -point.edge_distance, point.complexity))

    central_pool = [point for point in uncovered if point.edge_distance >= 0.14]
    if len(central_pool) < 40:
        central_pool = [point for point in uncovered if point.edge_distance >= 0.10]
    if len(central_pool) < 20:
        central_pool = uncovered

    pool = sorted(
        central_pool,
        key=lambda point: (0.45 * point.center_distance - 0.35 * point.edge_distance + 0.02 * point.complexity, point.x, point.y),
    )[:140]

    def spacing_score(point: RationalPoint) -> tuple[float, float, float, int]:
        min_dist = min((point.x - old.x) ** 2 + (point.y - old.y) ** 2 for old in chosen_points)
        return (min_dist, point.edge_distance, -point.center_distance, -point.complexity)

    return max(pool, key=spacing_score)


def rects_overlap(a: CoverRect, b: CoverRect) -> bool:
    return not (
        a.x0 + a.width <= b.x0
        or b.x0 + b.width <= a.x0
        or a.y0 + a.height <= b.y0
        or b.y0 + b.height <= a.y0
    )


def make_cover_rect(point: RationalPoint, k: int, rng: np.random.Generator, covers: list[CoverRect], epsilon: float) -> CoverRect:
    x, y = point.x, point.y
    area_bound = 0.72 * epsilon / (2 ** k)
    if covers:
        area_bound = min(area_bound, 0.5 * covers[-1].area_bound)
    aspect = rng.uniform(0.65, 1.55)
    scale = 1.0

    while True:
        width = min(sqrt(area_bound * aspect) * scale, 0.9)
        height = min(area_bound / max(width, 1e-12) * scale, 0.9)
        x0 = np.clip(x - width / 2, 0.0, 1.0 - width)
        y0 = np.clip(y - height / 2, 0.0, 1.0 - height)
        candidate = CoverRect(x0=float(x0), y0=float(y0), width=float(width), height=float(height), area_bound=float(width * height))
        if all(not rects_overlap(candidate, rect) for rect in covers):
            return candidate
        scale *= 0.72
        if scale < 1e-3:
            tiny = 1e-4
            candidate = CoverRect(x0=max(0.0, min(1.0 - tiny, x - tiny / 2)), y0=max(0.0, min(1.0 - tiny, y - tiny / 2)), width=tiny, height=tiny, area_bound=tiny * tiny)
            return candidate


def area_bound_sum(covers: list[CoverRect]) -> float:
    return sum(rect.area_bound for rect in covers)


def irrational_dots(seed: int = 5, count: int = 2200) -> np.ndarray:
    rng = np.random.default_rng(seed)
    points = rng.uniform(0.0, 1.0, size=(count, 2))
    return points


def draw_frame(
    save_path: Path,
    *,
    covers: list[CoverRect],
    old_points: list[tuple[float, float, str] | RationalPoint],
    current_point: tuple[float, float, str] | RationalPoint | None,
    dots: np.ndarray,
    area_history: list[float],
    epsilon: float,
    y_max: float,
    title: str,
    lines: list[str],
) -> None:
    def point_xy_label(point: tuple[float, float, str] | RationalPoint) -> tuple[float, float, str]:
        if isinstance(point, RationalPoint):
            return point.x, point.y, point.label
        return point

    fig = plt.figure(figsize=(7.2, 8.4))
    ax_square = fig.add_axes([0.19, 0.48, 0.62, 0.47])
    ax_area = fig.add_axes([0.12, 0.12, 0.80, 0.28])

    ax_square.scatter(dots[:, 0], dots[:, 1], s=3.0, color=COLORS["irrational"], alpha=0.32, linewidths=0, zorder=0)
    for rect in covers:
        ax_square.add_patch(
            Rectangle(
                (rect.x0, rect.y0),
                rect.width,
                rect.height,
                facecolor=COLORS["cover"],
                edgecolor=COLORS["cover_edge"],
                lw=0.9,
                alpha=0.42,
                zorder=1,
            )
        )

    if old_points:
        converted = [point_xy_label(point) for point in old_points]
        xs = [p[0] for p in converted]
        ys = [p[1] for p in converted]
        ax_square.scatter(xs, ys, s=28, color=COLORS["old_point"], zorder=2)
    if current_point is not None:
        px, py, plabel = point_xy_label(current_point)
        ax_square.scatter([px], [py], s=80, color=COLORS["point"], zorder=3)
        ax_square.annotate(
            plabel,
            xy=(px, py),
            xytext=(min(px + 0.08, 0.9), min(py + 0.08, 0.92)),
            fontsize=11,
            color=COLORS["point"],
            arrowprops=dict(arrowstyle="->", color=COLORS["point"], lw=1.2),
        )

    ax_square.set_xlim(0, 1)
    ax_square.set_ylim(0, 1)
    ax_square.set_aspect("equal")
    ax_square.set_xlabel("")
    ax_square.set_ylabel("")
    ax_square.tick_params(axis="both", labelsize=9)

    levels = list(range(len(area_history)))
    ax_area.plot(levels, area_history, color=COLORS["cover_edge"], marker="o", lw=2.3, label="長方形面積の上界")
    ax_area.axhline(epsilon, color=COLORS["gap"], lw=1.8, ls="--", label=rf"$\varepsilon={epsilon:.3f}$")
    ax_area.fill_between(levels, 0.0, area_history, color=COLORS["cover"], alpha=0.18)
    ax_area.set_xlim(-0.2, N_STEPS + 0.2)
    ax_area.set_ylim(0.0, y_max)
    ax_area.set_xticks(range(0, N_STEPS + 1))
    ax_area.set_xlabel("段階", fontsize=11)
    ax_area.set_ylabel("面積の上界", fontsize=11)
    ax_area.tick_params(axis="both", labelsize=9)
    ax_area.legend(loc="lower right", fontsize=8.5, frameon=False)

    ax_area.text(
        0.03,
        0.97,
        "\n".join(lines),
        transform=ax_area.transAxes,
        va="top",
        fontsize=8.5,
        bbox=dict(boxstyle="round, pad=0.35", facecolor="white", edgecolor=COLORS["grid"]),
    )

    fig.suptitle(title, fontsize=12.5, y=0.985)
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    rng = np.random.default_rng(17)
    candidates = rational_points()
    dots = irrational_dots()
    covers: list[CoverRect] = []
    chosen_points: list[RationalPoint] = []
    area_history = [0.0]
    images = []
    frame_index = 0
    y_max = EPSILON * 1.18

    def save(**kwargs) -> None:
        nonlocal frame_index
        path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(path, **kwargs)
        images.append(imageio.imread(path))
        frame_index += 1

    save(
        covers=[],
        old_points=[],
        current_point=None,
        dots=dots,
        area_history=area_history,
        epsilon=EPSILON,
        y_max=y_max,
        title=r"$[0, 1]^2$ 内の有理点集合 $\mathbb{Q}^2 \cap [0, 1]^2$ を考える",
        lines=[
            r"赤点: 有理点の代表列 $(r_k)$",
            r"橙長方形: 各 $r_k$ を含む小長方形 $R_k$",
            r"目標: 外側近似 $\bigcup R_k$ の面積を $\varepsilon$ 未満にする",
        ],
    )

    for k in range(1, N_STEPS + 1):
        point = choose_next_point(candidates, covers, chosen_points)
        save(
            covers=covers.copy(),
            old_points=[(p.x, p.y, p.label) for p in chosen_points],
            current_point=(point.x, point.y, point.label),
            dots=dots,
            area_history=area_history,
            epsilon=EPSILON,
            y_max=y_max,
            title=f"段階 {k}: まだ外側近似に入っていない有理点を 1 つ選ぶ",
            lines=[
                r"未被覆の有理点はまだ残る",
                rf"この点を $r_{{{k}}}$ とする",
                r"次に $r_k$ を含む小長方形 $R_k$ を置く",
            ],
        )

        rect = make_cover_rect(point, k, rng, covers, EPSILON)
        covers.append(rect)
        chosen_points.append(point)
        area_history.append(area_bound_sum(covers))

        save(
            covers=covers.copy(),
            old_points=[(p.x, p.y, p.label) for p in chosen_points],
            current_point=None,
            dots=dots,
            area_history=area_history,
            epsilon=EPSILON,
            y_max=y_max,
            title=f"段階 {k}: 小長方形を足して外側近似を更新する",
            lines=[
                rf"$|R_{{{k}}}| = {rect.area_bound:.4f}$",
                rf"$|R_{{{k}}}| < \varepsilon / 2^{{{k}}} = {EPSILON / (2 ** k):.4f}$",
                rf"$\sum_{{j=1}}^{{{k}}} |R_j| \leq {area_history[-1]:.4f}$",
            ],
        )

    save(
        covers=covers.copy(),
        old_points=chosen_points.copy(),
        current_point=None,
        dots=dots,
        area_history=area_history,
        epsilon=EPSILON,
        y_max=y_max,
        title=r"有理点集合は任意に小さい面積の外側近似で覆える",
        lines=[
            r"$\mathbb{Q}^2 \cap [0, 1]^2 \subset \bigcup_{k=1}^{\infty} R_k$",
            rf"$\sum |R_k| < \varepsilon = {EPSILON:.2f}$",
            r"したがって有理点集合の外側測度は 0",
            r"被覆面積の上界は 0 へ近づけられる",
        ],
    )

    for epsilon in EPSILON_STAGES[1:]:
        stage_rng = np.random.default_rng(17)
        stage_covers: list[CoverRect] = []
        stage_history = [0.0]
        for k, point in enumerate(chosen_points, start=1):
            rect = make_cover_rect(point, k, stage_rng, stage_covers, epsilon)
            stage_covers.append(rect)
            stage_history.append(area_bound_sum(stage_covers))

        save(
            covers=stage_covers,
            old_points=chosen_points,
            current_point=None,
            dots=dots,
            area_history=stage_history,
            epsilon=epsilon,
            y_max=y_max,
            title=r"$\varepsilon$ をさらに小さくしても外側近似は同様に作れる",
            lines=[
                rf"$\varepsilon = {epsilon:.3f}$",
                rf"$\sum_{{j=1}}^{{{N_STEPS}}} |R_j| \leq {stage_history[-1]:.4f}$",
                r"$\varepsilon$ を小さくすると,",
                r"長方形も被覆面積の上界も一緒に縮む",
            ],
        )

    imageio.mimsave(GIF_PATH, images, duration=FRAME_DURATION, loop=GIF_LOOP)
    print(f"Saved GIF to: {GIF_PATH.resolve()}")
    print(f"Saved frames to: {FRAMES_DIR.resolve()}")


if __name__ == "__main__":
    build_animation()
