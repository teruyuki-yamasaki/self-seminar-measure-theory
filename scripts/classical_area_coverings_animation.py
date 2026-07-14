#!/usr/bin/env python3
"""Generate an animated version of the classical area approximation figure."""

from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTDIR = Path("figures/measure/animations/classical_area_coverings")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "classical_area_coverings.gif"

CANVAS = (1600, 820)
FRAME_DURATION_MS = 1000
LOOP = 0
POLYGON_STAGES = [4, 6, 8, 12, 16, 24]
RECT_STAGE_COUNT = len(POLYGON_STAGES)
INSCRIBED_SQUARE_HALF = 1 / math.sqrt(2)
GAP_INTERVAL_EDGES = [0.0, 0.28, 0.48, 0.62, 0.69, INSCRIBED_SQUARE_HALF]

COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "blue": "#2f6fed",
    "cyan": "#2cb4c8",
    "shape": "#2cb4c8",
    "shape_edge": "#17212b",
    "red": "#e85d5d",
    "panel": "#ffffff",
    "grid": "#d9e0e8",
}


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc" if bold else "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


FONT_HEADING = load_font(30, bold=True)
FONT_BODY = load_font(22)
FONT_SMALL = load_font(18)


def hex_rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    try:
        box = draw.textbbox((0, 0), text, font=font)
        return box[2] - box[0], box[3] - box[1]
    except AttributeError:
        return draw.textsize(text, font=font)


def centered_text(draw: ImageDraw.ImageDraw, center: tuple[float, float], text: str, font: ImageFont.FreeTypeFont, fill: str) -> None:
    w, h = text_size(draw, text, font)
    draw.text((center[0] - w / 2, center[1] - h / 2), text, font=font, fill=fill)


def regular_polygon(center: tuple[float, float], radius: float, n: int, *, start_angle: float = -math.pi / 2) -> list[tuple[float, float]]:
    return [
        (
            center[0] + radius * math.cos(start_angle + 2 * math.pi * k / n),
            center[1] + radius * math.sin(start_angle + 2 * math.pi * k / n),
        )
        for k in range(n)
    ]


def polygon_area_ratio(n: int) -> float:
    return 0.5 * n * math.sin(2 * math.pi / n) / math.pi


def cap_height(left: float, right: float) -> float:
    return math.sqrt(max(0.0, 1.0 - max(left * left, right * right)))


def gap_intervals(stage_index: int) -> list[tuple[float, float]]:
    return list(zip(GAP_INTERVAL_EDGES[:-1], GAP_INTERVAL_EDGES[1:]))[:stage_index]


def symmetric_intervals(left: float, right: float) -> list[tuple[float, float]]:
    if abs(left) < 1e-12:
        return [(-right, right)]
    return [(-right, -left), (left, right)]


def rectangle_gap_area_ratio(stage_index: int) -> float:
    s = INSCRIBED_SQUARE_HALF
    total = (2 * s) ** 2
    for left, right in gap_intervals(stage_index):
        top = cap_height(left, right)
        if top <= s:
            continue
        # Four symmetric top/bottom rectangles and four symmetric left/right rectangles.
        total += 8 * (right - left) * (top - s)
    return total / math.pi


def draw_panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], heading: str) -> None:
    try:
        draw.rounded_rectangle(box, radius=12, fill=COLORS["panel"], outline="#d9e0e8", width=2)
    except AttributeError:
        draw.rectangle(box, fill=COLORS["panel"], outline="#d9e0e8")
    centered_text(draw, ((box[0] + box[2]) / 2, box[1] + 36), heading, FONT_HEADING, COLORS["ink"])


def draw_polygon_approx(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int, n: int) -> None:
    draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill="#f7fbff", outline=COLORS["blue"], width=5)
    poly = regular_polygon(center, radius, n, start_angle=-math.pi / 2)
    draw.polygon(poly, fill=hex_rgba(COLORS["shape"], 180), outline=COLORS["shape_edge"])
    draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), outline=COLORS["blue"], width=5)
    centered_text(draw, (center[0], center[1] + radius + 45), f"正 {n} 角形", FONT_BODY, COLORS["ink"])


def draw_rectangle_approx(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int, stage_index: int) -> None:
    draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill="#f7fbff", outline=COLORS["blue"], width=5)
    s = INSCRIBED_SQUARE_HALF

    def rect_from_unit(x0: float, y0: float, x1: float, y1: float) -> tuple[float, float, float, float]:
        return (
            center[0] + radius * x0,
            center[1] - radius * y1,
            center[0] + radius * x1,
            center[1] - radius * y0,
        )

    fill = hex_rgba(COLORS["shape"], 180)
    draw.rectangle(rect_from_unit(-s, -s, s, s), fill=fill, outline=COLORS["shape_edge"], width=2)

    for left, right in gap_intervals(stage_index):
        top = cap_height(left, right)
        if top <= s:
            continue
        intervals = symmetric_intervals(left, right)
        for x0, x1 in intervals:
            draw.rectangle(rect_from_unit(x0, s, x1, top), fill=fill, outline=COLORS["shape_edge"], width=2)
            draw.rectangle(rect_from_unit(x0, -top, x1, -s), fill=fill, outline=COLORS["shape_edge"], width=2)
        for y0, y1 in intervals:
            draw.rectangle(rect_from_unit(s, y0, top, y1), fill=fill, outline=COLORS["shape_edge"], width=2)
            draw.rectangle(rect_from_unit(-top, y0, -s, y1), fill=fill, outline=COLORS["shape_edge"], width=2)

    draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), outline=COLORS["blue"], width=5)
    label = "内接正方形" if stage_index == 0 else f"隙間への追加 {stage_index}"
    centered_text(draw, (center[0], center[1] + radius + 45), label, FONT_BODY, COLORS["ink"])


def draw_axis(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], values: list[float], labels: list[str]) -> None:
    x0, y, x1 = box[0] + 60, box[3] - 72, box[2] - 60
    draw.line((x0, y, x1, y), fill=COLORS["ink"], width=3)
    draw.line((x1, y, x1 - 12, y - 7), fill=COLORS["ink"], width=3)
    draw.line((x1, y, x1 - 12, y + 7), fill=COLORS["ink"], width=3)
    minv, maxv = 0.55, 1.02

    def mx(value: float) -> float:
        return x0 + (x1 - x0 - 18) * (value - minv) / (maxv - minv)

    limit_x = mx(1.0)
    draw.line((limit_x, y - 35, limit_x, y + 35), fill=COLORS["red"], width=3)
    centered_text(draw, (limit_x, y + 54), "円の面積", FONT_SMALL, COLORS["red"])
    last_index = len(values) - 1
    for index, (value, label) in enumerate(zip(values, labels)):
        px = mx(value)
        radius = 7 if index == last_index else 5
        fill = COLORS["blue"] if index == last_index else "#8eb1ec"
        draw.ellipse((px - radius, y - radius, px + radius, y + radius), fill=fill, outline=COLORS["ink"])
        if index == last_index:
            centered_text(draw, (px, y - 30), label, FONT_SMALL, COLORS["ink"])
    centered_text(draw, ((x0 + x1) / 2, y + 100), "近似面積が極限へ近づく", FONT_SMALL, COLORS["muted"])


def draw_frame(stage_index: int) -> Image.Image:
    image = Image.new("RGBA", CANVAS, COLORS["paper"])
    draw = ImageDraw.Draw(image)
    left = (54, 48, 768, 770)
    right = (832, 48, 1546, 770)
    draw_panel(draw, left, "内接多角形による近似")
    draw_panel(draw, right, "長方形和による近似")
    n = POLYGON_STAGES[stage_index]
    draw_polygon_approx(draw, (411, 330), 218, n)
    draw_rectangle_approx(draw, (1189, 330), 218, stage_index)
    poly_values = [polygon_area_ratio(k) for k in POLYGON_STAGES[: stage_index + 1]]
    strip_values = [rectangle_gap_area_ratio(k) for k in range(stage_index + 1)]
    labels = [f"{k + 1}" for k in range(stage_index + 1)]
    draw_axis(draw, left, poly_values, labels)
    draw_axis(draw, right, strip_values, labels)
    centered_text(draw, (CANVAS[0] / 2, 798), "有限個の基本図形を増やし, 面積を極限で定める", FONT_BODY, COLORS["ink"])
    return image


def build_animation() -> None:
    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    frames: list[Image.Image] = []
    for stage_index in range(RECT_STAGE_COUNT):
        frame = draw_frame(stage_index)
        frame.save(FRAMES_DIR / f"frame_{stage_index:03d}.png")
        frames.append(frame.convert("P", palette=Image.ADAPTIVE))
    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=LOOP,
        disposal=2,
        optimize=False,
    )
    print(f"Saved GIF to: {GIF_PATH.resolve()}")


if __name__ == "__main__":
    build_animation()
