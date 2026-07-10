#!/usr/bin/env python3
"""Generate visual assets for measure and Lebesgue integral intuition."""

from __future__ import annotations

import argparse
from pathlib import Path
import zlib

import numpy as np

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


COLORS = {
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "grid": "#d7dde6",
    "blue": "#2f6fed",
    "cyan": "#2cb4c8",
    "green": "#3aa76d",
    "yellow": "#f2b84b",
    "red": "#e85d5d",
    "purple": "#7b61ff",
    "paper": "#fbfaf7",
    "panel": "#ffffff",
}

DEFAULT_GIF_DURATION_MS = 1000


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
            "axes.edgecolor": COLORS["ink"],
            "axes.labelcolor": COLORS["ink"],
            "xtick.color": COLORS["muted"],
            "ytick.color": COLORS["muted"],
            "text.color": COLORS["ink"],
            "savefig.facecolor": COLORS["paper"],
            "savefig.bbox": "tight",
            "savefig.dpi": 180,
        }
    )


def f(x: np.ndarray) -> np.ndarray:
    return 0.35 + 0.55 * np.exp(-8 * (x - 0.28) ** 2) + 0.25 * np.exp(-22 * (x - 0.72) ** 2)


def lebesgue_demo_function(x: np.ndarray) -> np.ndarray:
    raw = (
        0.20
        + 0.72 * np.exp(-70 * (x - 0.28) ** 2)
        + 0.58 * np.exp(-95 * (x - 0.73) ** 2)
        + 0.05 * np.sin(4 * np.pi * x + 0.2)
    )
    raw_min = float(np.min(raw))
    raw_max = float(np.max(raw))
    return 0.05 + 0.92 * (raw - raw_min) / (raw_max - raw_min)


def hide_numeric_tick_labels(ax: plt.Axes) -> None:
    ax.tick_params(labelbottom=False, labelleft=False)


def power_of_two_tex(power: int) -> str:
    return rf"2^{{{power}}}"


def dyadic_mesh_tex(power: int) -> str:
    return rf"1/{power_of_two_tex(power)}"


def integrate_on_unit_interval(values: np.ndarray, x: np.ndarray) -> float:
    trapezoid = getattr(np, "trapezoid", np.trapz)
    return float(trapezoid(values, x))


def static_dir(base_outdir: Path) -> Path:
    path = base_outdir / "static"
    path.mkdir(parents=True, exist_ok=True)
    return path


def animation_dir(base_outdir: Path, stem: str) -> Path:
    path = base_outdir / "animations" / stem
    path.mkdir(parents=True, exist_ok=True)
    return path


def animation_gif_path(base_outdir: Path, stem: str) -> Path:
    path = animation_dir(base_outdir, stem) / "gif"
    path.mkdir(parents=True, exist_ok=True)
    return path / f"{stem}.gif"


def save_gif(fig: plt.Figure, update, frame_count: int, path: Path, *, duration_ms: int = DEFAULT_GIF_DURATION_MS, max_width: int = 960) -> None:
    frames = []
    width, height = fig.canvas.get_width_height()
    if width > max_width:
        output_size = (max_width, round(height * max_width / width))
    else:
        output_size = (width, height)
    paper_rgb = tuple(int(COLORS["paper"].lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    no_dither = getattr(getattr(Image, "Dither", Image), "NONE", 0)
    resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.BICUBIC)

    for frame in range(frame_count):
        update(frame)
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba()).copy()
        alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
        rgb = (rgba[:, :, :3] * alpha + np.array(paper_rgb, dtype=np.float32) * (1.0 - alpha)).astype(np.uint8)
        image = Image.fromarray(rgb, mode="RGB")
        if image.size != output_size:
            image = image.resize(output_size, resample=resample)
        frames.append(image.quantize(colors=128, dither=no_dither))

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        disposal=2,
        optimize=True,
    )


def render_frame_image(fig: plt.Figure, *, max_width: int = 960) -> Image.Image:
    width, height = fig.canvas.get_width_height()
    if width > max_width:
        output_size = (max_width, round(height * max_width / width))
    else:
        output_size = (width, height)
    paper_rgb = tuple(int(COLORS["paper"].lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.BICUBIC)

    fig.canvas.draw()
    rgba = np.asarray(fig.canvas.buffer_rgba()).copy()
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    rgb = (rgba[:, :, :3] * alpha + np.array(paper_rgb, dtype=np.float32) * (1.0 - alpha)).astype(np.uint8)
    image = Image.fromarray(rgb, mode="RGB")
    if image.size != output_size:
        image = image.resize(output_size, resample=resample)
    return image


def save_keyframes(fig: plt.Figure, update, frame_count: int, outdir: Path, stem: str) -> None:
    keyframe_dir = animation_dir(outdir, stem) / "keyframes"
    keyframe_dir.mkdir(parents=True, exist_ok=True)
    frame_indexes = [
        ("start", 0),
        ("middle", frame_count // 2),
        ("end", frame_count - 1),
    ]
    for label, frame in frame_indexes:
        update(frame)
        render_frame_image(fig).save(keyframe_dir / f"{label}.png")


def interval_inf_sup(edges: np.ndarray, samples_per_interval: int = 48) -> tuple[np.ndarray, np.ndarray]:
    infima = []
    suprema = []
    for left, right in zip(edges[:-1], edges[1:]):
        xs = np.linspace(left, right, samples_per_interval)
        values = f(xs)
        infima.append(float(np.min(values)))
        suprema.append(float(np.max(values)))
    return np.array(infima), np.array(suprema)


def nested_partition_history(target_intervals: int, seed: int) -> list[np.ndarray]:
    """Build nested random partitions of [0, 1] by adding one point at a time."""

    rng = np.random.default_rng(seed)
    edges = np.array([0.0, 1.0])
    history = [edges.copy()]

    while len(edges) - 1 < target_intervals:
        widths = np.diff(edges)
        interval_index = int(np.argmax(widths))
        left, right = edges[interval_index], edges[interval_index + 1]
        split = left + rng.uniform(0.35, 0.65) * (right - left)
        edges = np.insert(edges, interval_index + 1, split)
        history.append(edges.copy())

    return history


def stable_random_tags(edges: np.ndarray, seed: int) -> np.ndarray:
    tags = []
    for left, right in zip(edges[:-1], edges[1:]):
        key = f"{seed}:{left:.14f}:{right:.14f}".encode("ascii")
        local_seed = zlib.crc32(key)
        rng = np.random.default_rng(local_seed)
        tags.append(rng.uniform(left, right))
    return np.array(tags)


def nested_value_partition_history(target_intervals: int) -> list[np.ndarray]:
    """Build nested partitions of the value axis by splitting widest intervals."""

    edges = np.array([0.0, 1.0])
    history = [edges.copy()]
    while len(edges) - 1 < target_intervals:
        widths = np.diff(edges)
        interval_index = int(np.argmax(widths))
        split = (edges[interval_index] + edges[interval_index + 1]) / 2
        edges = np.insert(edges, interval_index + 1, split)
        history.append(edges.copy())
    return history


def draw_value_partition(
    ax: plt.Axes,
    x: np.ndarray,
    y: np.ndarray,
    edges: np.ndarray,
    *,
    show_labels: bool,
) -> np.ndarray:
    y_max = 1.0
    cmap = plt.get_cmap("viridis")
    approximating_values = np.zeros_like(y)

    ax.plot(x, y, color=COLORS["ink"], lw=2.5, zorder=5)
    for k in range(len(edges) - 1):
        lower, upper = edges[k], edges[k + 1]
        if k == len(edges) - 2:
            mask = (lower <= y) & (y <= upper)
        else:
            mask = (lower <= y) & (y < upper)
        approximating_values[mask] = lower
        color = cmap(lower / y_max)
        ax.fill_between(x, 0, lower, where=mask, color=color, alpha=0.42, zorder=2)
        ax.fill_between(x, lower, upper, where=mask, color=color, alpha=0.22, zorder=1)
        ax.axhline(lower, color=color, lw=0.7, alpha=0.5, zorder=0)

        if show_labels and len(edges) <= 9 and np.any(mask):
            center_x = float(np.mean(x[mask]))
            ax.text(center_x, lower + 0.015, rf"$A_{k}$", ha="center", fontsize=10, color=COLORS["ink"])

    ax.axhline(edges[-1], color=COLORS["muted"], lw=0.7, alpha=0.35)
    ax.step(x, approximating_values, where="mid", color=COLORS["red"], lw=1.8, alpha=0.9, zorder=4)
    return approximating_values


def simple_values_for_value_partition(y: np.ndarray, edges: np.ndarray) -> np.ndarray:
    approximating_values = np.zeros_like(y)
    for k in range(len(edges) - 1):
        lower, upper = edges[k], edges[k + 1]
        if k == len(edges) - 2:
            mask = (lower <= y) & (y <= upper)
        else:
            mask = (lower <= y) & (y < upper)
        approximating_values[mask] = lower
    return approximating_values


def draw_lower_simple_function(
    ax: plt.Axes,
    x: np.ndarray,
    y: np.ndarray,
    edges: np.ndarray,
) -> np.ndarray:
    simple_values = simple_values_for_value_partition(y, edges)
    cmap = plt.get_cmap("viridis")

    ax.plot(x, y, color=COLORS["ink"], lw=2.5, zorder=5)
    for k in range(len(edges) - 1):
        lower = edges[k]
        upper = edges[k + 1]
        if k == len(edges) - 2:
            mask = (lower <= y) & (y <= upper)
        else:
            mask = (lower <= y) & (y < upper)
        if not np.any(mask):
            continue
        color = cmap(lower)
        ax.fill_between(x, 0, lower, where=mask, color=color, alpha=0.44, zorder=2)

    ax.step(x, simple_values, where="mid", color=COLORS["red"], lw=1.8, alpha=0.95, zorder=4)
    return simple_values


def draw_measure_zero(outdir: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.set_xlim(-0.04, 1.04)
    ax.set_ylim(-0.1, 1.05)
    ax.axis("off")

    ax.text(0.0, 0.98, "測度: 集合に「大きさ」を割り当てる", fontsize=22, weight="bold")
    ax.text(0.0, 0.89, "点は見える.しかし長さは 0.区間は長さを持つ.", fontsize=15, color=COLORS["muted"])

    ax.plot([0, 1], [0.55, 0.55], color=COLORS["ink"], lw=2.5)
    ax.plot([0, 0], [0.52, 0.58], color=COLORS["ink"], lw=2)
    ax.plot([1, 1], [0.52, 0.58], color=COLORS["ink"], lw=2)
    ax.text(0, 0.45, "0", ha="center", fontsize=12)
    ax.text(1, 0.45, "1", ha="center", fontsize=12)

    interval = Rectangle((0.18, 0.49), 0.54, 0.12, facecolor=COLORS["cyan"], alpha=0.45, edgecolor=COLORS["cyan"])
    ax.add_patch(interval)
    ax.text(0.45, 0.68, r"$\mu([a, b]) = b-a$", ha="center", fontsize=18, color=COLORS["cyan"])

    for pos in [0.08, 0.35, 0.79, 0.92]:
        ax.add_patch(Circle((pos, 0.55), 0.013, color=COLORS["red"], zorder=3))
    ax.text(0.79, 0.31, r"$\mu(\{x\})=0$", ha="center", fontsize=18, color=COLORS["red"])

    rng = np.random.default_rng(4)
    rational_like = np.sort(rng.uniform(0.04, 0.96, 90))
    y = 0.18 + rng.normal(0, 0.012, rational_like.size)
    ax.scatter(rational_like, y, s=8, color=COLORS["purple"], alpha=0.65)
    ax.text(0.5, 0.06, "有理数のように密に散らばる点集合も, 長さとしては 0 と見られる", ha="center", fontsize=14)

    fig.savefig(static_dir(outdir) / "measure_zero.png")
    plt.close(fig)


def draw_riemann_vs_lebesgue(outdir: Path) -> None:
    x = np.linspace(0, 1, 500)
    y = f(x)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2), sharey=True)
    fig.suptitle("Riemann積分とLebesgue積分の見方", fontsize=22, weight="bold")

    ax = axes[0]
    ax.plot(x, y, color=COLORS["ink"], lw=2.5)
    n = 12
    edges = nested_partition_history(n, seed=120)[-1]
    tags = stable_random_tags(edges, seed=120)
    mesh = np.max(np.diff(edges))
    heights = f(tags)
    for left, right, tag, height in zip(edges[:-1], edges[1:], tags, heights):
        ax.add_patch(Rectangle((left, 0), right - left, height, facecolor=COLORS["blue"], alpha=0.28, edgecolor=COLORS["blue"]))
        ax.plot(tag, height, marker="o", ms=4, color=COLORS["red"], zorder=6)
    ax.vlines(edges, 0, 1.03, color=COLORS["blue"], lw=0.7, alpha=0.35)
    ax.set_title(r"タグ付き分割  $\|\Delta\|={:.3f}$".format(mesh), fontsize=17)
    ax.text(0.5, -0.16, r"$\sum f(x_i)\Delta x_i$", transform=ax.transAxes, ha="center", fontsize=16)

    ax = axes[1]
    m = 7
    value_edges = nested_value_partition_history(m)[-1]
    draw_value_partition(ax, x, y, value_edges, show_labels=False)
    ax.set_title(r"値域の分割  $m={}$".format(m), fontsize=17)
    ax.text(0.5, -0.16, r"$\sum a_k\mu(A_k)$", transform=ax.transAxes, ha="center", fontsize=16)

    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.1)
        ax.set_xlabel("定義域")
        ax.set_ylabel("値")
        hide_numeric_tick_labels(ax)
        ax.grid(color=COLORS["grid"], lw=0.8)

    fig.savefig(static_dir(outdir) / "riemann_vs_lebesgue.png")
    plt.close(fig)


def draw_expectation_as_integral(outdir: Path) -> None:
    fig, ax = plt.subplots(figsize=(12.5, 6.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.03, 0.94, "期待値は確率測度に関するLebesgue積分", fontsize=22, weight="bold")
    ax.text(0.03, 0.87, r"$E[X]=\int_\Omega X(\omega)\, P(d\omega)$", fontsize=22)

    omega = Circle((0.27, 0.47), 0.27, facecolor="#eef5ff", edgecolor=COLORS["blue"], lw=2)
    ax.add_patch(omega)
    ax.text(0.27, 0.77, r"$\Omega$: 市場シナリオ全体", ha="center", fontsize=15, color=COLORS["blue"])

    rng = np.random.default_rng(7)
    pts = rng.normal(loc=[0.27, 0.47], scale=[0.11, 0.10], size=(42, 2))
    pts = pts[np.sum((pts - np.array([0.27, 0.47])) ** 2, axis=1) < 0.25**2]
    weights = rng.uniform(20, 140, len(pts))
    payoff = 20 + 80 * (pts[:, 0] + 0.35 * pts[:, 1])
    ax.scatter(pts[:, 0], pts[:, 1], s=weights, c=payoff, cmap="viridis", alpha=0.8, edgecolor="white", linewidth=0.8)
    ax.text(0.27, 0.13, r"点の大きさ: $P(d\omega)$", ha="center", fontsize=13)
    ax.text(0.27, 0.08, r"色: $X(\omega)$", ha="center", fontsize=13)

    ax.add_patch(FancyArrowPatch((0.55, 0.48), (0.72, 0.48), arrowstyle="->", mutation_scale=24, lw=2.2, color=COLORS["ink"]))
    ax.text(0.64, 0.55, "重み付き平均", ha="center", fontsize=14)

    ax.add_patch(Rectangle((0.76, 0.30), 0.18, 0.36, facecolor=COLORS["panel"], edgecolor=COLORS["ink"], lw=1.5))
    bars = np.array([0.18, 0.31, 0.48, 0.68, 0.82])
    for i, h in enumerate(bars):
        ax.add_patch(Rectangle((0.79 + i * 0.028, 0.34), 0.018, h * 0.25, facecolor=COLORS["green"], alpha=0.85))
    ax.text(0.85, 0.69, r"$E[X]$", ha="center", fontsize=22, weight="bold")
    ax.text(0.85, 0.25, "平均ペイオフ", ha="center", fontsize=14)

    fig.savefig(static_dir(outdir) / "expectation_as_integral.png")
    plt.close(fig)


def draw_fubini_grid(outdir: Path) -> None:
    t = np.linspace(0, 1, 80)
    w = np.linspace(0, 1, 55)
    T, W = np.meshgrid(t, w)
    z = 0.25 + 0.55 * np.exp(-5 * (T - 0.65) ** 2) + 0.25 * np.sin(4 * np.pi * T + 3 * W) ** 2

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2))
    fig.suptitle("Fubini: 時間方向とシナリオ方向の集計を交換する", fontsize=20, weight="bold")

    labels = [
        r"各シナリオで $\int_0^T X_t(\omega)\, dt$ → 平均",
        r"各時刻で $E[X_t]$ → 時間積分",
    ]
    for ax, label in zip(axes, labels):
        ax.imshow(z, origin="lower", aspect="auto", extent=[0, 1, 0, 1], cmap="YlGnBu")
        ax.set_xlabel("time $t$")
        ax.set_ylabel(r"scenario $\omega$")
        ax.set_title(label, fontsize=14)
        hide_numeric_tick_labels(ax)
        ax.grid(color="white", lw=0.6, alpha=0.5)

    for y0 in [0.2, 0.5, 0.78]:
        axes[0].plot([0.04, 0.96], [y0, y0], color=COLORS["red"], lw=3)
    for x0 in [0.22, 0.52, 0.82]:
        axes[1].plot([x0, x0], [0.05, 0.95], color=COLORS["red"], lw=3)

    fig.savefig(static_dir(outdir) / "fubini_grid.png")
    plt.close(fig)


def animate_riemann_refinement(outdir: Path, frames: int, *, write_gif: bool) -> None:
    x = np.linspace(0, 1, 600)
    y = f(x)
    target_intervals = max(90, frames + 30)
    partition_history = nested_partition_history(target_intervals, seed=3000)
    interval_counts = np.unique(np.linspace(4, target_intervals, frames, dtype=int))
    fig, ax = plt.subplots(figsize=(10, 5.8))

    def update(frame: int):
        ax.clear()
        n = int(interval_counts[min(frame, len(interval_counts) - 1)])
        edges = partition_history[n - 1]
        tags = stable_random_tags(edges, seed=3000)
        widths = np.diff(edges)
        mesh = float(np.max(widths))
        heights = f(tags)
        infima, suprema = interval_inf_sup(edges)
        lower_sum = float(np.sum(infima * widths))
        upper_sum = float(np.sum(suprema * widths))
        tagged_sum = float(np.sum(heights * widths))

        ax.plot(x, y, color=COLORS["ink"], lw=2.5)
        for left, right, tag, height, low, high in zip(edges[:-1], edges[1:], tags, heights, infima, suprema):
            width = right - left
            ax.add_patch(Rectangle((left, 0), width, low, facecolor=COLORS["blue"], alpha=0.28, edgecolor=COLORS["blue"], lw=0.55))
            ax.add_patch(Rectangle((left, low), width, high - low, facecolor=COLORS["red"], alpha=0.18, edgecolor=COLORS["red"], lw=0.45))
            ax.plot(tag, height, marker="o", ms=3.8, color=COLORS["red"], zorder=5)
        ax.vlines(edges, 0, 1.03, color=COLORS["blue"], lw=0.55, alpha=0.45)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.05)
        ax.set_title(r"Riemann積分: 下和と上和  $n={}$,  $\|\Delta\|={:.3f}$".format(n, mesh), fontsize=15)
        ax.text(
            0.02,
            0.96,
            r"$\mathcal{S}^{-}(f,\Delta)=\sum m_i(x_i-x_{i-1}), \quad \mathcal{S}^{+}(f,\Delta)=\sum M_i(x_i-x_{i-1})$",
            transform=ax.transAxes,
            va="top",
            fontsize=11.2,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )
        ax.text(
            0.02,
            0.82,
            rf"$\mathcal{{S}}^{{-}}(f,\Delta)={lower_sum:.12f}$"
            + "\n"
            + rf"$\mathcal{{S}}^{{+}}(f,\Delta)={upper_sum:.12f}$"
            + "\n"
            + rf"$\mathcal{{S}}^{{+}}-\mathcal{{S}}^{{-}}={upper_sum - lower_sum:.12f}$"
            + "\n"
            + rf"$\sum f(\xi_i)(x_i-x_{{i-1}})={tagged_sum:.12f}$",
            transform=ax.transAxes,
            va="top",
            fontsize=10.5,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        hide_numeric_tick_labels(ax)

    if write_gif:
        save_gif(fig, update, len(interval_counts), animation_gif_path(outdir, "riemann_refinement"))
    save_keyframes(fig, update, len(interval_counts), outdir, "riemann_refinement")
    plt.close(fig)


def animate_riemann_area_convergence(outdir: Path, frames: int, *, write_gif: bool) -> None:
    x = np.linspace(0, 1, 1200)
    y = f(x)
    target_integral = integrate_on_unit_interval(y, x)
    target_intervals = max(90, frames + 30)
    partition_history = nested_partition_history(target_intervals, seed=4000)
    interval_counts = np.unique(np.linspace(4, target_intervals, frames, dtype=int))
    lower_sums = []
    upper_sums = []

    for n in interval_counts:
        edges = partition_history[int(n) - 1]
        widths = np.diff(edges)
        infima, suprema = interval_inf_sup(edges, samples_per_interval=64)
        lower_sums.append(float(np.sum(infima * widths)))
        upper_sums.append(float(np.sum(suprema * widths)))

    lower_sums = np.array(lower_sums)
    upper_sums = np.array(upper_sums)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.8), gridspec_kw={"width_ratios": [1.45, 1.0]})
    ax_area, ax_conv = axes

    def update(frame: int):
        ax_area.clear()
        ax_conv.clear()
        frame_index = min(frame, len(interval_counts) - 1)
        n = int(interval_counts[frame_index])
        edges = partition_history[n - 1]
        widths = np.diff(edges)
        infima, suprema = interval_inf_sup(edges, samples_per_interval=64)
        mesh = float(np.max(widths))

        ax_area.plot(x, y, color=COLORS["ink"], lw=2.5)
        for left, width, low, high in zip(edges[:-1], widths, infima, suprema):
            ax_area.add_patch(Rectangle((left, 0), width, low, facecolor=COLORS["blue"], alpha=0.28, edgecolor=COLORS["blue"], lw=0.55))
            ax_area.add_patch(Rectangle((left, low), width, high - low, facecolor=COLORS["red"], alpha=0.18, edgecolor=COLORS["red"], lw=0.45))
        ax_area.vlines(edges, 0, 1.03, color=COLORS["blue"], lw=0.55, alpha=0.45)
        ax_area.set_xlim(0, 1)
        ax_area.set_ylim(0, 1.05)
        ax_area.set_title(r"ランダム分割での下和と上和", fontsize=15)
        ax_area.text(
            0.02,
            0.96,
            rf"$n={n}$, $\|\Delta\|={mesh:.3f}$"
            + "\n"
            + rf"$\mathcal{{S}}^{{-}}={lower_sums[frame_index]:.12f}$"
            + "\n"
            + rf"$\mathcal{{S}}^{{+}}={upper_sums[frame_index]:.12f}$",
            transform=ax_area.transAxes,
            va="top",
            fontsize=10.8,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )
        ax_area.set_xlabel("x")
        ax_area.set_ylabel("f(x)")
        hide_numeric_tick_labels(ax_area)

        shown_counts = interval_counts[: frame_index + 1]
        ax_conv.axhline(target_integral, color=COLORS["ink"], lw=1.6, ls="--", label=rf"$\int_0^1 f(x)\, dx \approx {target_integral:.6f}$")
        ax_conv.plot(interval_counts, lower_sums, color=COLORS["grid"], lw=1.0, alpha=0.75)
        ax_conv.plot(interval_counts, upper_sums, color=COLORS["grid"], lw=1.0, alpha=0.75)
        ax_conv.plot(shown_counts, lower_sums[: frame_index + 1], color=COLORS["blue"], lw=2.0, label=r"$\mathcal{S}^{-}(f,\Delta)$")
        ax_conv.plot(shown_counts, upper_sums[: frame_index + 1], color=COLORS["red"], lw=2.0, label=r"$\mathcal{S}^{+}(f,\Delta)$")
        ax_conv.scatter([n], [lower_sums[frame_index]], color=COLORS["blue"], s=38, zorder=5)
        ax_conv.scatter([n], [upper_sums[frame_index]], color=COLORS["red"], s=38, zorder=5)
        ax_conv.set_xlim(float(interval_counts[0]), float(interval_counts[-1]))
        y_min = float(np.min(lower_sums)) - 0.015
        y_max = float(np.max(upper_sums)) + 0.015
        ax_conv.set_ylim(y_min, y_max)
        ax_conv.set_title("面積の収束", fontsize=15)
        ax_conv.set_xlabel("横軸の分割数 n")
        ax_conv.set_ylabel("面積")
        hide_numeric_tick_labels(ax_conv)
        ax_conv.grid(color=COLORS["grid"], lw=0.8)
        ax_conv.legend(loc="lower right", fontsize=9.5, framealpha=0.95)
        ax_conv.text(
            0.04,
            0.92,
            rf"$\mathcal{{S}}^{{+}}-\mathcal{{S}}^{{-}}={upper_sums[frame_index] - lower_sums[frame_index]:.12f}$",
            transform=ax_conv.transAxes,
            va="top",
            fontsize=10.5,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )

    fig.suptitle("Riemann積分: ランダム分割でも下和と上和が収束する", fontsize=17, weight="bold")
    if write_gif:
        save_gif(fig, update, len(interval_counts), animation_gif_path(outdir, "riemann_area_convergence"))
    save_keyframes(fig, update, len(interval_counts), outdir, "riemann_area_convergence")
    plt.close(fig)


def animate_lebesgue_layers(outdir: Path, frames: int, *, write_gif: bool) -> None:
    x = np.linspace(0, 1, 900)
    y = lebesgue_demo_function(x)
    target_integral = integrate_on_unit_interval(y, x)
    target_intervals = max(48, frames)
    value_history = nested_value_partition_history(target_intervals)
    interval_counts = np.unique(np.linspace(3, target_intervals, frames, dtype=int))
    fig, ax = plt.subplots(figsize=(10, 5.8))

    def update(frame: int):
        ax.clear()
        m = int(interval_counts[min(frame, len(interval_counts) - 1)])
        value_edges = value_history[m - 1]
        mesh_power = int(np.floor(np.log2(m)))
        simple_values = draw_value_partition(ax, x, y, value_edges, show_labels=False)
        simple_integral = integrate_on_unit_interval(simple_values, x)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.05)
        ax.set_title(
            rf"Lebesgue積分: 値域を細分化する  $m={m}$,  $\max\Delta y={dyadic_mesh_tex(mesh_power)}$",
            fontsize=15,
        )
        ax.text(
            0.02,
            0.96,
            r"$E_k=\{x\in X:\,a_k\leq f(x)<a_{k+1}\}, \quad \varphi_m=\sum a_k\mathbf{1}_{E_k}$",
            transform=ax.transAxes,
            va="top",
            fontsize=12,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )
        ax.text(
            0.02,
            0.82,
            rf"$\int_X \varphi_m(x)\, d\mu(x) = {simple_integral:.12f}$" + "\n" + rf"$\int_X f(x)\, d\mu(x) \approx {target_integral:.12f}$",
            transform=ax.transAxes,
            va="top",
            fontsize=12,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )
        ax.set_xlabel("x")
        ax.set_ylabel("値")
        hide_numeric_tick_labels(ax)

    if write_gif:
        save_gif(fig, update, len(interval_counts), animation_gif_path(outdir, "lebesgue_layers"))
    save_keyframes(fig, update, len(interval_counts), outdir, "lebesgue_layers")
    plt.close(fig)


def animate_lebesgue_layers_powers_equal(outdir: Path, *, write_gif: bool, seconds_per_stage: float = 1.0, fps: int = 1) -> None:
    x = np.linspace(0, 1, 900)
    y = lebesgue_demo_function(x)
    target_integral = integrate_on_unit_interval(y, x)
    powers = [2**n for n in range(1, 11)]
    value_history = nested_value_partition_history(max(powers))
    frames_per_stage = max(1, round(seconds_per_stage * fps))
    interval_counts = np.repeat(powers, frames_per_stage)
    fig, ax = plt.subplots(figsize=(10, 5.8))

    def update(frame: int):
        ax.clear()
        m = int(interval_counts[min(frame, len(interval_counts) - 1)])
        value_edges = value_history[m - 1]
        simple_values = draw_value_partition(ax, x, y, value_edges, show_labels=False)
        simple_integral = integrate_on_unit_interval(simple_values, x)
        n = int(np.log2(m))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.05)
        ax.set_title(
            rf"Lebesgue積分: $m={power_of_two_tex(n)}={m}$ で値域を細分化  $\max\Delta y={dyadic_mesh_tex(n)}$",
            fontsize=15,
        )
        ax.text(
            0.02,
            0.96,
            r"$E_k=\{x\in X:\,a_k\leq f(x)<a_{k+1}\}, \quad \varphi_m=\sum a_k\mathbf{1}_{E_k}$",
            transform=ax.transAxes,
            va="top",
            fontsize=12,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )
        ax.text(
            0.02,
            0.82,
            rf"$\int_X \varphi_m(x)\, d\mu(x) = {simple_integral:.12f}$" + "\n" + rf"$\int_X f(x)\, d\mu(x) \approx {target_integral:.12f}$",
            transform=ax.transAxes,
            va="top",
            fontsize=12,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )
        ax.set_xlabel("x")
        ax.set_ylabel("値")
        hide_numeric_tick_labels(ax)

    if write_gif:
        save_gif(
            fig,
            update,
            len(interval_counts),
            animation_gif_path(outdir, "lebesgue_layers_powers_equal"),
            duration_ms=DEFAULT_GIF_DURATION_MS,
        )
    save_keyframes(fig, update, len(interval_counts), outdir, "lebesgue_layers_powers_equal")
    plt.close(fig)


def animate_lebesgue_area_convergence(outdir: Path, frames: int, *, write_gif: bool) -> None:
    x = np.linspace(0, 1, 900)
    y = lebesgue_demo_function(x)
    target_integral = integrate_on_unit_interval(y, x)
    max_power = 10
    powers = np.arange(1, max_power + 1)
    interval_counts = 2**powers
    value_history = nested_value_partition_history(int(interval_counts[-1]))
    simple_integrals = np.array(
        [
            integrate_on_unit_interval(simple_values_for_value_partition(y, value_history[int(m) - 1]), x)
            for m in interval_counts
        ]
    )
    errors = target_integral - simple_integrals
    frames_per_stage = max(1, round(frames / len(interval_counts)))
    stage_indexes = np.repeat(np.arange(len(interval_counts)), frames_per_stage)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.8), gridspec_kw={"width_ratios": [1.45, 1.0]})
    ax_area, ax_conv = axes

    def update(frame: int):
        ax_area.clear()
        ax_conv.clear()
        frame_index = int(stage_indexes[min(frame, len(stage_indexes) - 1)])
        m = int(interval_counts[frame_index])
        power = int(powers[frame_index])
        value_edges = value_history[m - 1]
        simple_values = draw_value_partition(ax_area, x, y, value_edges, show_labels=False)
        simple_integral = integrate_on_unit_interval(simple_values, x)

        ax_area.set_xlim(0, 1)
        ax_area.set_ylim(0, 1.05)
        ax_area.set_title(r"近似面積  $\int_X \varphi_m\, d\mu$", fontsize=15)
        ax_area.text(
            0.02,
            0.96,
            rf"$m={power_of_two_tex(power)}={m}$, $\max\Delta y={dyadic_mesh_tex(power)}$"
            + "\n"
            + rf"$\int_X \varphi_m(x)\, d\mu(x)={simple_integral:.12f}$",
            transform=ax_area.transAxes,
            va="top",
            fontsize=11.5,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )
        ax_area.set_xlabel("x")
        ax_area.set_ylabel("値")
        hide_numeric_tick_labels(ax_area)

        shown_powers = powers[: frame_index + 1]
        shown_integrals = simple_integrals[: frame_index + 1]
        ax_conv.axhline(target_integral, color=COLORS["ink"], lw=1.6, ls="--", label=rf"$\int_X f(x)\, d\mu(x) \approx {target_integral:.6f}$")
        ax_conv.plot(powers, simple_integrals, color=COLORS["grid"], lw=1.2, alpha=0.8)
        ax_conv.plot(shown_powers, shown_integrals, color=COLORS["blue"], lw=2.2, marker="o", ms=4.2, label=r"$\int_X \varphi_{2^{k}}\, d\mu$")
        ax_conv.scatter([power], [simple_integral], color=COLORS["red"], s=46, zorder=5)
        ax_conv.set_xlim(float(powers[0]) - 0.15, float(powers[-1]) + 0.15)
        y_min = float(np.min(simple_integrals)) - 0.015
        y_max = float(target_integral) + 0.015
        ax_conv.set_ylim(y_min, y_max)
        ax_conv.set_title("面積の収束", fontsize=15)
        ax_conv.set_xlabel(r"$k=\log_2 m$")
        ax_conv.set_xticks(powers)
        ax_conv.set_xticklabels([str(int(power)) for power in powers])
        ax_conv.set_ylabel("面積")
        hide_numeric_tick_labels(ax_conv)
        ax_conv.grid(color=COLORS["grid"], lw=0.8)
        ax_conv.legend(loc="lower right", fontsize=10, framealpha=0.95)
        ax_conv.text(
            0.04,
            0.92,
            rf"$\int_X f\, d\mu-\int_X \varphi_m\, d\mu={errors[frame_index]:.12f}$",
            transform=ax_conv.transAxes,
            va="top",
            fontsize=10.8,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.9},
        )

    fig.suptitle("Lebesgue積分: 単函数の面積が収束する様子", fontsize=17, weight="bold")
    if write_gif:
        save_gif(fig, update, len(stage_indexes), animation_gif_path(outdir, "lebesgue_area_convergence"))
    save_keyframes(fig, update, len(stage_indexes), outdir, "lebesgue_area_convergence")
    plt.close(fig)


def draw_readme_preview_gif(outdir: Path) -> None:
    x = np.linspace(0, 1, 700)
    y = lebesgue_demo_function(x)
    target_integral = integrate_on_unit_interval(y, x)
    powers = [2**n for n in range(1, 11)]
    value_history = nested_value_partition_history(max(powers))
    fig, ax = plt.subplots(figsize=(8.8, 4.8))

    def update(frame: int):
        ax.clear()
        m = powers[min(frame, len(powers) - 1)]
        value_edges = value_history[m - 1]
        simple_values = draw_lower_simple_function(ax, x, y, value_edges)
        simple_integral = integrate_on_unit_interval(simple_values, x)
        n = int(np.log2(m))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.05)
        ax.set_title(rf"Lebesgue積分: $m={power_of_two_tex(n)}={m}$", fontsize=14)
        ax.text(
            0.02,
            0.94,
            rf"$\int_X \varphi_m\, d\mu={simple_integral:.6f}$"
            + "\n"
            + rf"$\int_X f\, d\mu\approx {target_integral:.6f}$"
            + "\n"
            + rf"$\max\Delta y={dyadic_mesh_tex(n)}$",
            transform=ax.transAxes,
            va="top",
            fontsize=10,
            color=COLORS["ink"],
            bbox={"boxstyle": "round, pad=0.25", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.92},
        )
        ax.set_xlabel("x")
        ax.set_ylabel("値")
        hide_numeric_tick_labels(ax)

    save_gif(fig, update, len(powers), animation_gif_path(outdir, "readme_preview"), max_width=640)
    plt.close(fig)


def animate_fubini_order(outdir: Path, frames: int, *, write_gif: bool) -> None:
    t = np.linspace(0, 1, 70)
    w = np.linspace(0, 1, 50)
    T, W = np.meshgrid(t, w)
    z = 0.25 + 0.55 * np.exp(-5 * (T - 0.65) ** 2) + 0.25 * np.sin(4 * np.pi * T + 3 * W) ** 2
    fig, ax = plt.subplots(figsize=(9.8, 5.8))

    def update(frame: int):
        ax.clear()
        ax.imshow(z, origin="lower", aspect="auto", extent=[0, 1, 0, 1], cmap="YlGnBu")
        ax.set_xlabel("time $t$")
        ax.set_ylabel(r"scenario $\omega$")
        hide_numeric_tick_labels(ax)
        ax.grid(color="white", lw=0.5, alpha=0.45)
        half = frames // 2
        if frame < half:
            y0 = 0.08 + 0.84 * frame / max(1, half - 1)
            ax.plot([0.03, 0.97], [y0, y0], color=COLORS["red"], lw=4)
            ax.set_title(r"先に時間積分: $\int_0^T X_t(\omega)\, dt$", fontsize=15)
        else:
            x0 = 0.06 + 0.88 * (frame - half) / max(1, frames - half - 1)
            ax.plot([x0, x0], [0.04, 0.96], color=COLORS["red"], lw=4)
            ax.set_title(r"先に期待値: $E[X_t]$", fontsize=15)

    if write_gif:
        save_gif(fig, update, frames, animation_gif_path(outdir, "fubini_order"))
    save_keyframes(fig, update, frames, outdir, "fubini_order")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("figures/measure"))
    parser.add_argument("--frames", type=int, default=72)
    parser.add_argument("--with-gifs", action="store_true", help="Also generate local GIF files. GIFs are ignored by Git.")
    parser.add_argument("--skip-gifs", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_style()
    args.outdir.mkdir(parents=True, exist_ok=True)

    draw_measure_zero(args.outdir)
    draw_riemann_vs_lebesgue(args.outdir)
    draw_expectation_as_integral(args.outdir)
    draw_fubini_grid(args.outdir)
    draw_readme_preview_gif(args.outdir)

    write_gif = args.with_gifs and not args.skip_gifs
    animate_riemann_refinement(args.outdir, args.frames, write_gif=write_gif)
    animate_riemann_area_convergence(args.outdir, args.frames, write_gif=write_gif)
    animate_lebesgue_layers(args.outdir, args.frames, write_gif=write_gif)
    animate_lebesgue_layers_powers_equal(args.outdir, write_gif=write_gif)
    animate_lebesgue_area_convergence(args.outdir, args.frames, write_gif=write_gif)
    animate_fubini_order(args.outdir, args.frames, write_gif=write_gif)

    print(f"Generated assets in {args.outdir}")


if __name__ == "__main__":
    main()
