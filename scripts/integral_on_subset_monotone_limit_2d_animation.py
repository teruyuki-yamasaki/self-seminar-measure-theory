#!/usr/bin/env python3
"""Visualize monotone simple-function approximation on measurable subsets in 2D."""

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
from matplotlib.colors import Normalize
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


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
    "jump": "#d95f5f",
}

OUTDIR = Path("figures/measure/animations/integral_on_subset_monotone_limit_2d")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "integral_on_subset_monotone_limit_2d.gif"

FRAME_DURATION = 1.0
GIF_LOOP = 0
N_VALUES = [1, 2, 3, 4]
SUBSET_SPECS = [
    {
        "name": "E^(1)",
        "rectangles": [(0.06, 0.08, 0.28, 0.34), (0.36, 0.18, 0.34, 0.44), (0.78, 0.58, 0.16, 0.24)],
    },
    {
        "name": "E^(2)",
        "rectangles": [(0.10, 0.62, 0.34, 0.22), (0.40, 0.10, 0.22, 0.32), (0.68, 0.32, 0.24, 0.40)],
    },
    {
        "name": "E^(3)",
        "rectangles": [(0.04, 0.16, 0.20, 0.22), (0.28, 0.34, 0.48, 0.24), (0.72, 0.72, 0.20, 0.16)],
    },
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


def f(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    z = np.zeros_like(x, dtype=float)

    r1 = (x < 0.32) & (y < 0.58)
    r2 = (x >= 0.32) & (y < 0.58) & (x + y < 0.98)
    r3 = (y >= 0.58) & (x + y < 0.98)
    r4 = x + y >= 0.98

    if np.any(r1):
        xr = x[r1] / 0.32
        yr = y[r1] / 0.58
        z[r1] = 0.24 + 0.16 * np.sin(1.1 * np.pi * xr + 0.2) ** 2 + 0.08 * np.cos(2.8 * np.pi * yr - 0.3) ** 2
    if np.any(r2):
        xr = (x[r2] - 0.32) / 0.68
        yr = y[r2] / 0.58
        z[r2] = 0.70 + 0.18 * np.sin(1.2 * np.pi * xr + 0.1) ** 2 + 0.06 * np.sin(3.6 * np.pi * yr)
    if np.any(r3):
        xr = x[r3]
        yr = (y[r3] - 0.58) / 0.42
        z[r3] = 0.48 + 0.12 * np.cos(1.5 * np.pi * xr - 0.4) ** 2 + 0.08 * np.sin(3.4 * np.pi * yr + 0.2)
    if np.any(r4):
        s = np.clip((x[r4] + y[r4] - 0.98) / 1.02, 0.0, 1.0)
        z[r4] = 0.90 + 0.16 * np.sin(1.3 * np.pi * s + 0.1) ** 2 + 0.04 * np.cos(7.0 * np.pi * s)

    return np.clip(z, 0.10, 1.18)


def phi(values: np.ndarray, n: int) -> np.ndarray:
    scale = 2**n
    return np.floor(scale * values) / scale


def subset_mask(x: np.ndarray, y: np.ndarray, rectangles: list[tuple[float, float, float, float]]) -> np.ndarray:
    mask = np.zeros_like(x, dtype=bool)
    for x0, y0, w, h in rectangles:
        mask |= (x0 <= x) & (x <= x0 + w) & (y0 <= y) & (y <= y0 + h)
    return mask


def integral_on_subset(values: np.ndarray, mask: np.ndarray, cell_area: float) -> float:
    return float(np.sum(np.where(mask, values, 0.0)) * cell_area)


def draw_surface(ax: plt.Axes, x: np.ndarray, y: np.ndarray, z: np.ndarray, mask: np.ndarray, title: str) -> None:
    facecolors = np.empty(z.shape + (4,), dtype=float)
    facecolors[:] = matplotlib.colors.to_rgba(COLORS["paper"], 0.0)
    cmap = plt.get_cmap("YlOrRd")
    norm = Normalize(vmin=float(np.min(z)), vmax=float(np.max(z)))
    mapped = cmap(norm(z))
    facecolors[mask] = mapped[mask]

    ax.plot_surface(x, y, z, facecolors=facecolors, linewidth=0.0, antialiased=True, shade=False)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_zlim(0.0, 1.24)
    ax.view_init(elev=28, azim=-55)
    ax.set_xlabel("x", labelpad=8)
    ax.set_ylabel("y", labelpad=8)
    ax.set_zlabel("height", labelpad=8)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_zticks([0.0, 0.5, 1.0])
    ax.xaxis.pane.set_facecolor(matplotlib.colors.to_rgba(COLORS["paper"], 1.0))
    ax.yaxis.pane.set_facecolor(matplotlib.colors.to_rgba(COLORS["paper"], 1.0))
    ax.zaxis.pane.set_facecolor(matplotlib.colors.to_rgba(COLORS["paper"], 1.0))
    ax.xaxis._axinfo["grid"]["color"] = COLORS["grid"]
    ax.yaxis._axinfo["grid"]["color"] = COLORS["grid"]
    ax.zaxis._axinfo["grid"]["color"] = COLORS["grid"]
    ax.set_title(title, fontsize=13, pad=8)


def draw_frame(
    save_path: Path,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    subset: np.ndarray,
    subset_spec: dict[str, object],
    n: int,
    cell_area: float,
) -> None:
    phi_n = phi(z, n)
    phi_np1 = phi(z, n + 1)

    int_f = integral_on_subset(z, subset, cell_area)
    int_phi_n = integral_on_subset(phi_n, subset, cell_area)
    int_phi_np1 = integral_on_subset(phi_np1, subset, cell_area)
    gap_n = int_f - int_phi_n
    gap_np1 = int_f - int_phi_np1

    fig = plt.figure(figsize=(14.5, 8.9))
    ax_domain = fig.add_axes([0.05, 0.51, 0.32, 0.36])
    ax_phi = fig.add_axes([0.39, 0.49, 0.28, 0.38], projection="3d")
    ax_f = fig.add_axes([0.68, 0.49, 0.28, 0.38], projection="3d")
    ax_bar = fig.add_axes([0.07, 0.13, 0.26, 0.24])
    ax_formula = fig.add_axes([0.39, 0.10, 0.56, 0.25])

    domain_cmap = plt.get_cmap("viridis")
    ax_domain.imshow(z, origin="lower", extent=[0, 1, 0, 1], cmap=domain_cmap, aspect="equal")
    subset_overlay = np.zeros((*subset.shape, 4), dtype=float)
    subset_overlay[subset] = matplotlib.colors.to_rgba(COLORS["subset"], 0.34)
    ax_domain.imshow(subset_overlay, origin="lower", extent=[0, 1, 0, 1], aspect="equal")
    ax_domain.axvline(0.32, color=COLORS["jump"], lw=1.1, ls="--", alpha=0.85)
    ax_domain.axhline(0.58, color=COLORS["jump"], lw=1.1, ls="--", alpha=0.85)
    diag_x = np.linspace(0.0, 0.98, 300)
    diag_y = 0.98 - diag_x
    ax_domain.plot(diag_x, diag_y, color=COLORS["jump"], lw=1.1, ls="--", alpha=0.85)
    for x0, y0, w, h in subset_spec["rectangles"]:  # type: ignore[index]
        ax_domain.add_patch(Rectangle((x0, y0), w, h, fill=False, edgecolor=COLORS["subset_edge"], lw=1.5))
    ax_domain.set_xlim(0.0, 1.0)
    ax_domain.set_ylim(0.0, 1.0)
    ax_domain.set_xticks(np.linspace(0.0, 1.0, 6))
    ax_domain.set_yticks(np.linspace(0.0, 1.0, 6))
    ax_domain.grid(color=COLORS["grid"], lw=0.7, alpha=0.55)
    ax_domain.set_xlabel("x")
    ax_domain.set_ylabel("y")
    ax_domain.set_title(rf"2D domain with $E={subset_spec['name']}$ highlighted", fontsize=14, pad=10)

    draw_surface(ax_phi, x, y, phi_n, subset, rf"$\phi_n$ on $E$,  n={n}$")
    draw_surface(ax_f, x, y, z, subset, r"$f$ on $E$")

    ax_bar.bar(
        [rf"$\int_E \phi_n$", rf"$\int_E \phi_{{n+1}}$", r"$\int_E f$"],
        [int_phi_n, int_phi_np1, int_f],
        color=[COLORS["phi_n"], COLORS["phi_np1"], COLORS["f"]],
        alpha=0.85,
    )
    ax_bar.set_ylim(0.0, int_f * 1.12)
    ax_bar.grid(axis="y", color=COLORS["grid"], lw=0.8, alpha=0.7)
    ax_bar.set_ylabel("integral")
    ax_bar.set_title(r"$\int_E \phi_n \uparrow \int_E f$", fontsize=14, pad=8)
    ax_bar.text(
        0.04,
        0.96,
        rf"$\int_E f-\int_E \phi_n \approx {gap_n:.4f}$" + "\n" + rf"$\int_E f-\int_E \phi_{{n+1}} \approx {gap_np1:.4f}$",
        transform=ax_bar.transAxes,
        va="top",
        fontsize=10.5,
        color=COLORS["ink"],
        bbox={"boxstyle": "round, pad=0.18", "facecolor": COLORS["paper"], "edgecolor": COLORS["grid"], "alpha": 0.90},
    )

    ax_formula.axis("off")
    ax_formula.text(0.00, 0.86, r"$f\geq 0, \ \phi_n\uparrow f$ on $X=[0, 1]^2$", fontsize=16, color=COLORS["ink"])
    ax_formula.text(0.00, 0.64, r"$\mathbf{1}_E\phi_n \uparrow \mathbf{1}_E f$ だから, 単調収束定理より", fontsize=13.0, color=COLORS["muted"])
    ax_formula.text(0.00, 0.42, r"$\int_E f(x, y)\, m(dx\, dy)=\lim_{n\to\infty}\int_E \phi_n(x, y)\, m(dx\, dy)$", fontsize=14.2, color=COLORS["f"])
    ax_formula.text(0.00, 0.20, r"ここでは $E$ を切り替えながら, 不連続線をまたぐ場合でも同じ極限が成り立つことを見る.", fontsize=12.4, color=COLORS["ink"])
    ax_formula.text(0.00, 0.02, rf"current set: ${subset_spec['name']}$,  next frame keeps the same $E$ and refines the dyadic heights", fontsize=12.0, color=COLORS["muted"])

    fig.suptitle("2D version: monotone simple-function approximation on measurable subsets", fontsize=20, y=0.975)
    fig.text(
        0.50,
        0.04,
        r"左上は 2 次元の可測関数と部分集合 $E$，右の 2 枚は $E$ 上に制限した $\phi_n$ と $f$ の高さである. $E$ が不連続線を含んでも, 積分値は下から単調に $\int_E f$ に近づく.",
        ha="center",
        fontsize=11.8,
        color=COLORS["muted"],
    )
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def build_animation() -> None:
    setup_style()
    ensure_dirs()

    xs = np.linspace(0.0, 1.0, 120)
    ys = np.linspace(0.0, 1.0, 120)
    x, y = np.meshgrid(xs, ys)
    z = f(x, y)
    cell_area = (xs[1] - xs[0]) * (ys[1] - ys[0])

    frame_paths: list[Path] = []
    frame_index = 0
    for subset_spec in SUBSET_SPECS:
        subset = subset_mask(x, y, subset_spec["rectangles"])  # type: ignore[index]
        for n in N_VALUES:
            frame_path = FRAMES_DIR / f"frame_{frame_index:03d}.png"
            draw_frame(frame_path, x, y, z, subset, subset_spec, n, cell_area)
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
