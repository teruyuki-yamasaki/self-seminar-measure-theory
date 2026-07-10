#!/usr/bin/env python3
"""Conceptual animation for covering rational points in [0, 1] by tiny intervals."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path
import shutil

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
    "irrational": "#2c7fb8",
    "cover": "#f0b45a",
    "cover_edge": "#a85b00",
    "point": "#c03a2b",
    "old_point": "#7b241c",
    "grid": "#c8d1dc",
    "gap": "#d95f5f",
}

OUTDIR = Path("figures/measure/animations/rational_measure_zero")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "rational_measure_zero.gif"

EPSILON = 0.24
N_STEPS = 10
FRAME_DURATION = 1.0
GIF_LOOP = 0
EPSILON_STAGES = [0.24, 0.15, 0.09, 0.045]


@dataclass(frozen=True)
class CoverInterval:
    x0: float
    length: float

    @property
    def x1(self) -> float:
        return self.x0 + self.length


@dataclass(frozen=True)
class RationalPoint:
    x: float
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


def rational_axis(max_denominator: int = 30) -> list[tuple[int, int]]:
    vals: list[tuple[int, int]] = []
    for q in range(1, max_denominator + 1):
        for p in range(q + 1):
            if gcd(p, q) == 1:
                vals.append((p, q))
    vals.sort(key=lambda item: (item[1], item[0]))
    return vals


def rational_points(limit: int = 320) -> list[RationalPoint]:
    rng = np.random.default_rng(11)
    items: list[RationalPoint] = []
    for p, q in rational_axis():
        x = p / q
        roughness = rng.uniform(0.0, 0.03)
        items.append(
            RationalPoint(
                x=x,
                label=f"${p}/{q}$" if q != 1 else f"${p}$",
                complexity=q,
                center_distance=abs(x - 0.5) + roughness,
                edge_distance=min(x, 1.0 - x),
            )
        )

    items.sort(key=lambda item: (item.complexity, item.center_distance, -item.edge_distance, item.x))
    unique: list[RationalPoint] = []
    seen: set[float] = set()
    for point in items:
        key = round(point.x, 12)
        if key in seen:
            continue
        seen.add(key)
        unique.append(point)
        if len(unique) >= limit:
            break
    return unique


def point_is_covered(x: float, covers: list[CoverInterval]) -> bool:
    return any(interval.x0 <= x <= interval.x1 for interval in covers)


def choose_next_point(
    candidates: list[RationalPoint], covers: list[CoverInterval], chosen_points: list[RationalPoint]
) -> RationalPoint:
    uncovered = [point for point in candidates if not point_is_covered(point.x, covers)]
    if not uncovered:
        raise RuntimeError("Ran out of rational point candidates.")

    if not chosen_points:
        central = [point for point in uncovered if 0.18 <= point.x <= 0.82]
        pool = central if central else uncovered
        return min(pool, key=lambda point: (point.center_distance, -point.edge_distance, point.complexity))

    central_pool = [point for point in uncovered if point.edge_distance >= 0.12]
    if len(central_pool) < 40:
        central_pool = [point for point in uncovered if point.edge_distance >= 0.08]
    if len(central_pool) < 20:
        central_pool = uncovered

    pool = sorted(
        central_pool,
        key=lambda point: (0.42 * point.center_distance - 0.28 * point.edge_distance + 0.02 * point.complexity, point.x),
    )[:120]

    def spacing_score(point: RationalPoint) -> tuple[float, float, float, int]:
        min_dist = min(abs(point.x - old.x) for old in chosen_points)
        return (min_dist, point.edge_distance, -point.center_distance, -point.complexity)

    return max(pool, key=spacing_score)


def intervals_overlap(a: CoverInterval, b: CoverInterval) -> bool:
    return not (a.x1 <= b.x0 or b.x1 <= a.x0)


def make_cover_interval(
    point: RationalPoint, k: int, covers: list[CoverInterval], epsilon: float, rng: np.random.Generator
) -> CoverInterval:
    length_bound = 0.72 * epsilon / (2**k)
    if covers:
        length_bound = min(length_bound, 0.5 * covers[-1].length)

    center_shift = rng.uniform(-0.08, 0.08) * length_bound
    scale = 1.0
    while True:
        length = length_bound * scale
        x0 = np.clip(point.x - length / 2 + center_shift, 0.0, 1.0 - length)
        candidate = CoverInterval(float(x0), float(length))
        if all(not intervals_overlap(candidate, interval) for interval in covers):
            return candidate
        scale *= 0.72
        if scale < 1e-3:
            tiny = 1e-4
            x0 = np.clip(point.x - tiny / 2, 0.0, 1.0 - tiny)
            return CoverInterval(float(x0), tiny)


def length_bound_sum(covers: list[CoverInterval]) -> float:
    return sum(interval.length for interval in covers)


def irrational_dots(seed: int = 7, count: int = 2600) -> np.ndarray:
    rng = np.random.default_rng(seed)
    xs = rng.uniform(0.0, 1.0, size=count)
    ys = rng.uniform(0.18, 0.82, size=count)
    return np.column_stack([xs, ys])


def draw_frame(
    save_path: Path,
    *,
    covers: list[CoverInterval],
    old_points: list[float | RationalPoint],
    current_point: float | RationalPoint | None,
    dots: np.ndarray,
    length_history: list[float],
    epsilon: float,
    y_max: float,
    title: str,
    lines: list[str],
) -> None:
    def point_x_label(point: float | RationalPoint) -> tuple[float, str]:
        if isinstance(point, RationalPoint):
            return point.x, point.label
        return point, ""

    fig = plt.figure(figsize=(10.8, 10.8))
    ax_line = fig.add_axes([0.08, 0.56, 0.84, 0.30])
    ax_graph = fig.add_axes([0.12, 0.11, 0.76, 0.28])

    ax_line.scatter(dots[:, 0], dots[:, 1], s=3.0, color=COLORS["irrational"], alpha=0.28, linewidths=0, zorder=0)
    ax_line.plot([0, 1], [0.5, 0.5], color=COLORS["ink"], lw=2.0, zorder=1)
    for tick in np.linspace(0.0, 1.0, 6):
        ax_line.plot([tick, tick], [0.47, 0.53], color=COLORS["ink"], lw=1.0, zorder=1)
        ax_line.text(tick, 0.42, f"{tick:.1f}", ha="center", va="top", fontsize=11, color=COLORS["muted"])

    for interval in covers:
        ax_line.add_patch(
            Rectangle(
                (interval.x0, 0.32),
                interval.length,
                0.36,
                facecolor=COLORS["cover"],
                edgecolor=COLORS["cover_edge"],
                lw=0.9,
                alpha=0.44,
                zorder=2,
            )
        )

    if old_points:
        converted = [point_x_label(point) for point in old_points]
        xs = [p[0] for p in converted]
        ax_line.scatter(xs, [0.5] * len(xs), s=30, color=COLORS["old_point"], zorder=3)

    if current_point is not None:
        px, plabel = point_x_label(current_point)
        ax_line.scatter([px], [0.5], s=88, color=COLORS["point"], zorder=4)
        ax_line.annotate(
            plabel or r"$r_k$",
            xy=(px, 0.53),
            xytext=(min(max(px + 0.08, 0.12), 0.88), 0.92),
            fontsize=12,
            color=COLORS["point"],
            ha="center",
            arrowprops=dict(arrowstyle="->", color=COLORS["point"], lw=1.2),
        )

    ax_line.set_xlim(0, 1)
    ax_line.set_ylim(0.08, 0.98)
    ax_line.set_xticks([])
    ax_line.set_yticks([])
    ax_line.set_title(r"$[0, 1] \setminus \mathbb{Q}$ の直観", fontsize=17, pad=12)
    ax_line.set_xlabel("x", fontsize=18, labelpad=8)

    levels = list(range(len(length_history)))
    ax_graph.plot(levels, length_history, color=COLORS["cover_edge"], marker="o", lw=2.3, label="被覆長の上界")
    ax_graph.axhline(epsilon, color=COLORS["gap"], lw=1.8, ls="--", label=rf"$\varepsilon={epsilon:.3f}$")
    ax_graph.fill_between(levels, 0.0, length_history, color=COLORS["cover"], alpha=0.18)
    ax_graph.set_xlim(-0.2, N_STEPS + 0.2)
    ax_graph.set_ylim(0.0, y_max)
    ax_graph.set_xticks(range(0, N_STEPS + 1))
    ax_graph.set_xlabel("段階")
    ax_graph.set_ylabel("長さの上界")
    ax_graph.set_title("被覆長の上界", fontsize=16, pad=10)
    ax_graph.legend(loc="upper right", frameon=False)
    ax_graph.text(
        0.03,
        0.95,
        "\n".join(lines),
        transform=ax_graph.transAxes,
        va="top",
        fontsize=11,
        bbox=dict(boxstyle="round, pad=0.35", facecolor="white", edgecolor=COLORS["grid"]),
    )

    fig.suptitle(title, fontsize=18, y=0.96)
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    rng = np.random.default_rng(19)
    candidates = rational_points()
    dots = irrational_dots()
    covers: list[CoverInterval] = []
    chosen_points: list[RationalPoint] = []
    length_history = [0.0]
    frame_index = 0
    y_max = EPSILON * 1.18

    def save(**kwargs) -> None:
        nonlocal frame_index
        path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
        draw_frame(path, **kwargs)
        frame_index += 1

    save(
        covers=[],
        old_points=[],
        current_point=None,
        dots=dots,
        length_history=length_history,
        epsilon=EPSILON,
        y_max=y_max,
        title=r"$[0, 1]$ から有理点全体を取り除いた図形を考える",
        lines=[
            r"赤点: 有理点の代表列 $(r_k)$",
            r"橙区間: 各 $r_k$ を含む小区間 $I_k$",
            r"目標: $\sum |I_k| < \varepsilon$",
        ],
    )

    for k in range(1, N_STEPS + 1):
        point = choose_next_point(candidates, covers, chosen_points)
        save(
            covers=covers.copy(),
            old_points=chosen_points.copy(),
            current_point=point,
            dots=dots,
            length_history=length_history,
            epsilon=EPSILON,
            y_max=y_max,
            title=f"段階 {k}: まだ覆われていない有理点を 1 つ選ぶ",
            lines=[
                r"未被覆の有理点はまだ残る",
                rf"この点を $r_{{{k}}}$ とする",
                r"次に $r_k$ を含む小区間 $I_k$ を置く",
            ],
        )

        interval = make_cover_interval(point, k, covers, EPSILON, rng)
        covers.append(interval)
        chosen_points.append(point)
        length_history.append(length_bound_sum(covers))

        save(
            covers=covers.copy(),
            old_points=chosen_points.copy(),
            current_point=None,
            dots=dots,
            length_history=length_history,
            epsilon=EPSILON,
            y_max=y_max,
            title=f"段階 {k}: 小区間で有理点を覆う",
            lines=[
                rf"$|I_{{{k}}}| = {interval.length:.4f}$",
                rf"$|I_{{{k}}}| < \varepsilon / 2^{{{k}}} = {EPSILON / (2 ** k):.4f}$",
                rf"$\sum_{{j=1}}^{{{k}}} |I_j| \leq {length_history[-1]:.4f}$",
            ],
        )

    save(
        covers=covers.copy(),
        old_points=chosen_points.copy(),
        current_point=None,
        dots=dots,
        length_history=length_history,
        epsilon=EPSILON,
        y_max=y_max,
        title=r"有理点全体は短い全長で覆え, 残りはほとんど全部",
        lines=[
            r"$\mathbb{Q} \cap [0, 1] \subset \bigcup_{k=1}^{\infty} I_k$",
            rf"$\sum |I_k| < \varepsilon = {EPSILON:.2f}$",
            r"したがって無理数点の部分は",
            r"長さ 1 をもつと考えられる",
        ],
    )

    for epsilon in EPSILON_STAGES[1:]:
        stage_rng = np.random.default_rng(19)
        stage_covers: list[CoverInterval] = []
        stage_history = [0.0]
        for k, point in enumerate(chosen_points, start=1):
            interval = make_cover_interval(point, k, stage_covers, epsilon, stage_rng)
            stage_covers.append(interval)
            stage_history.append(length_bound_sum(stage_covers))

        save(
            covers=stage_covers,
            old_points=chosen_points.copy(),
            current_point=None,
            dots=dots,
            length_history=stage_history,
            epsilon=epsilon,
            y_max=y_max,
            title=r"$\varepsilon$ をさらに小さくしても同様に被覆できる",
            lines=[
                rf"$\varepsilon = {epsilon:.3f}$",
                rf"$\sum_{{j=1}}^{{{N_STEPS}}} |I_j| \leq {stage_history[-1]:.4f}$",
                r"$\varepsilon$ を小さくすると,",
                r"区間も被覆長の上界も一緒に縮む",
            ],
        )

    frame_paths = sorted(FRAMES_DIR.glob("frame_*.png"))
    gif_frames = [Image.open(path).convert("P", palette=Image.Palette.ADAPTIVE) for path in frame_paths]
    gif_frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=gif_frames[1:],
        duration=int(FRAME_DURATION * 1000),
        loop=GIF_LOOP,
        disposal=2,
    )
    print(f"Saved GIF to: {GIF_PATH.resolve()}")
    print(f"Saved frames to: {FRAMES_DIR.resolve()}")


if __name__ == "__main__":
    build_animation()
