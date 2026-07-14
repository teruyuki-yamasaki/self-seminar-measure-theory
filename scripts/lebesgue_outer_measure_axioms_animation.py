#!/usr/bin/env python3
"""Generate a Japanese GIF for the basic properties of Lebesgue outer measure."""

from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTDIR = Path("figures/measure/animations/lebesgue_outer_measure_axioms")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "lebesgue_outer_measure_axioms.gif"

CANVAS = (1680, 690)
FRAME_DURATION_MS = 950
LOOP = 0
FRAME_COUNT = 6

MEASURE_SYMBOL = "μ*"
EMPTY_SYMBOL = "∅"
SPACE_LABEL = "全体空間 R^N"
MAIN_TITLE = "ルベーグ外測度 μ* の基本性質"
NONNEG_FORMULA = "μ*(∅)=0,  0 <= μ*(A) <= ∞"
MONOTONE_FORMULA = "A が B に含まれるなら μ*(A) <= μ*(B)"
SUBADDITIVE_FORMULA = "合併の μ* <= 各集合の μ* の和"

COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "panel": "#ffffff",
    "grid": "#d9e0e8",
    "domain": "#f6eedf",
    "domain_edge": "#8d7b68",
    "blue": "#2f6fed",
    "blue_fill": "#9fc5ff",
    "green": "#2f8f5b",
    "green_fill": "#a7dbb8",
    "orange": "#b96f15",
    "orange_fill": "#f4bf72",
    "red": "#b94c4c",
    "red_fill": "#e88d8d",
    "purple": "#6e5cc4",
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


FONT_TITLE = load_font(36, bold=True)
FONT_PANEL = load_font(27, bold=True)
FONT_FORMULA = load_font(20, bold=True)
FONT_BODY = load_font(20)
FONT_SMALL = load_font(15)
FONT_LABEL = load_font(24, bold=True)


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


def blob(center: tuple[float, float], rx: float, ry: float, phase: float, n: int = 160) -> list[tuple[float, float]]:
    points = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = 1.0 + 0.12 * math.sin(3 * t + phase) + 0.08 * math.cos(5 * t - 0.7 * phase)
        points.append((center[0] + rx * r * math.cos(t), center[1] + ry * r * math.sin(t)))
    return points


def rect_for(panel: tuple[int, int, int, int], x: float, y: float, w: float, h: float) -> tuple[float, float, float, float]:
    left, top, right, bottom = panel
    return (
        left + x * (right - left),
        top + y * (bottom - top),
        left + (x + w) * (right - left),
        top + (y + h) * (bottom - top),
    )


def draw_panel_frame(draw: ImageDraw.ImageDraw, panel: tuple[int, int, int, int], title: str, formula: str) -> None:
    try:
        draw.rounded_rectangle(panel, radius=14, fill=COLORS["panel"], outline="#d9e0e8", width=2)
    except AttributeError:
        draw.rectangle(panel, fill=COLORS["panel"], outline="#d9e0e8")
    centered_text(draw, ((panel[0] + panel[2]) / 2, panel[1] + 32), title, FONT_PANEL, COLORS["ink"])
    centered_text(draw, ((panel[0] + panel[2]) / 2, panel[1] + 75), formula, FONT_FORMULA, COLORS["ink"])
    draw.ellipse(
        (panel[0] + 52, panel[1] + 105, panel[2] - 52, panel[1] + 330),
        fill=COLORS["domain"],
        outline=COLORS["domain_edge"],
        width=3,
    )
    centered_text(draw, ((panel[0] + panel[2]) / 2, panel[1] + 114), SPACE_LABEL, FONT_SMALL, COLORS["muted"])


def draw_number_line(draw: ImageDraw.ImageDraw, panel: tuple[int, int, int, int], y: int, max_value: float) -> None:
    x0 = panel[0] + 70
    x1 = panel[2] - 72
    draw.line((x0, y, x1, y), fill=COLORS["ink"], width=3)
    draw.line((x1, y, x1 - 12, y - 8), fill=COLORS["ink"], width=3)
    draw.line((x1, y, x1 - 12, y + 8), fill=COLORS["ink"], width=3)
    for i in range(5):
        x = x0 + (x1 - x0 - 18) * i / 4
        draw.line((x, y - 11, x, y + 11), fill=COLORS["ink"], width=2)
    centered_text(draw, (x0 - 18, y), "0", FONT_SMALL, COLORS["muted"])
    centered_text(draw, (x1 + 22, y), "∞", FONT_BODY, COLORS["muted"])


def measure_x(panel: tuple[int, int, int, int], y: int, value: float, max_value: float) -> tuple[float, float]:
    x0 = panel[0] + 70
    x1 = panel[2] - 90
    return (x0 + (x1 - x0) * min(value / max_value, 1.0), y)


def arrow_to_measure(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str,
    label: str,
) -> None:
    draw.line((start[0], start[1], end[0], end[1]), fill=color, width=3)
    draw.polygon([(end[0], end[1]), (end[0] - 10, end[1] - 7), (end[0] - 10, end[1] + 7)], fill=color)
    draw.ellipse((end[0] - 7, end[1] - 7, end[0] + 7, end[1] + 7), fill=color)
    centered_text(draw, (end[0], end[1] - 34), label, FONT_SMALL, color)


def draw_nonnegative(draw: ImageDraw.ImageDraw, panel: tuple[int, int, int, int], frame: int) -> None:
    draw_panel_frame(draw, panel, "非負性", NONNEG_FORMULA)
    y_line = panel[3] - 105
    draw_number_line(draw, panel, y_line, 0.75)
    measures = [0.0, 0.02, 0.13, 0.24, 0.36, 0.52]
    centers = [(0.20, 0.46), (0.32, 0.42), (0.47, 0.52), (0.64, 0.43), (0.77, 0.52), (0.58, 0.58)]
    for i, (cx, cy) in enumerate(centers):
        px = panel[0] + cx * (panel[2] - panel[0])
        py = panel[1] + cy * (panel[3] - panel[1])
        active = i == frame
        if i == 0:
            centered_text(draw, (px, py), "∅", FONT_LABEL, COLORS["muted"])
            if active:
                arrow_to_measure(draw, (px, py + 20), measure_x(panel, y_line, 0.0, 0.75), COLORS["blue"], f"{MEASURE_SYMBOL}({EMPTY_SYMBOL})")
            continue
        color = COLORS["blue"] if active else "#7da7df"
        fill = hex_rgba(COLORS["blue_fill"], 210 if active else 72)
        points = blob((px, py), 30 + i * 4, 20 + i * 3, phase=i * 0.8)
        draw.polygon(points, fill=fill, outline=color)
        if active:
            centered_text(draw, (px, py), f"A{i}", FONT_SMALL, COLORS["ink"])
            arrow_to_measure(draw, (px, py + 42), measure_x(panel, y_line, measures[i], 0.75), COLORS["blue"], f"{MEASURE_SYMBOL}(A{i})")
    centered_text(draw, ((panel[0] + panel[2]) / 2, panel[3] - 35), "空集合は 0, どの集合の外側コストも負にならない", FONT_SMALL, COLORS["muted"])


def draw_monotone(draw: ImageDraw.ImageDraw, panel: tuple[int, int, int, int], frame: int) -> None:
    draw_panel_frame(draw, panel, "単調性", MONOTONE_FORMULA)
    y_line = panel[3] - 105
    draw_number_line(draw, panel, y_line, 0.75)
    scale = 1.0 + frame * 0.055
    cx = (panel[0] + panel[2]) / 2
    cy = panel[1] + 225
    b_points = blob((cx, cy), 145 * scale, 78 * scale, phase=0.5 + frame)
    a_points = blob((cx - 22, cy + 4), 70 * scale, 39 * scale, phase=2.0 + frame)
    draw.polygon(b_points, fill=hex_rgba(COLORS["orange_fill"], 145), outline=COLORS["orange"])
    draw.polygon(a_points, fill=hex_rgba(COLORS["green_fill"], 220), outline=COLORS["green"])
    centered_text(draw, (cx - 22, cy + 4), "A", FONT_LABEL, COLORS["green"])
    centered_text(draw, (cx + 115 * scale, cy - 62 * scale), "B", FONT_LABEL, COLORS["orange"])
    arrow_to_measure(draw, (cx - 45, cy + 78), measure_x(panel, y_line, 0.17 + frame * 0.014, 0.75), COLORS["green"], f"{MEASURE_SYMBOL}(A)")
    arrow_to_measure(draw, (cx + 42, cy + 92), measure_x(panel, y_line, 0.42 + frame * 0.025, 0.75), COLORS["orange"], f"{MEASURE_SYMBOL}(B)")
    centered_text(draw, ((panel[0] + panel[2]) / 2, panel[3] - 35), "大きい集合を覆うには, 小さい集合以上の余地が必要になる", FONT_SMALL, COLORS["muted"])


def draw_subadditive(draw: ImageDraw.ImageDraw, panel: tuple[int, int, int, int], frame: int) -> None:
    draw_panel_frame(draw, panel, "可算劣加法性", SUBADDITIVE_FORMULA)
    y_line = panel[3] - 105
    draw_number_line(draw, panel, y_line, 0.95)
    centers = [(0.29, 0.47), (0.41, 0.43), (0.52, 0.49), (0.61, 0.45), (0.68, 0.50), (0.74, 0.43)]
    values = [0.11, 0.09, 0.07, 0.055, 0.04, 0.03]
    active_count = frame + 1
    for i, (cx, cy) in enumerate(centers):
        px = panel[0] + cx * (panel[2] - panel[0])
        py = panel[1] + cy * (panel[3] - panel[1])
        active = i < active_count
        points = blob((px, py), 54 - i * 3, 34 - i * 2, phase=i)
        draw.polygon(points, fill=hex_rgba(COLORS["red_fill"], 170 if active else 45), outline=COLORS["red"] if active else "#d7b6b6")
        if active:
            centered_text(draw, (px, py), f"A{i + 1}", FONT_SMALL, "#ffffff")
    union_est = [0.11, 0.18, 0.24, 0.29, 0.33, 0.36][frame]
    sum_est = sum(values[:active_count])
    centered_text(draw, (panel[0] + 182, panel[1] + 350), "合併の外測度", FONT_SMALL, COLORS["purple"])
    centered_text(draw, (panel[0] + 365, panel[1] + 350), "各外測度の和", FONT_SMALL, COLORS["red"])
    arrow_to_measure(draw, (panel[0] + 182, panel[1] + 375), measure_x(panel, y_line, union_est, 0.95), COLORS["purple"], f"{MEASURE_SYMBOL}(合併)")
    arrow_to_measure(draw, (panel[0] + 365, panel[1] + 375), measure_x(panel, y_line, sum_est, 0.95), COLORS["red"], f"{MEASURE_SYMBOL} の和")
    centered_text(draw, ((panel[0] + panel[2]) / 2, panel[3] - 35), "別々の被覆を並べれば, 合併の被覆が作れる", FONT_SMALL, COLORS["muted"])


def draw_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", CANVAS, COLORS["paper"])
    draw = ImageDraw.Draw(image)
    centered_text(draw, (CANVAS[0] / 2, 42), MAIN_TITLE, FONT_TITLE, COLORS["ink"])
    panels = [(34, 90, 542, 650), (586, 90, 1094, 650), (1138, 90, 1646, 650)]
    draw_nonnegative(draw, panels[0], frame)
    draw_monotone(draw, panels[1], frame)
    draw_subadditive(draw, panels[2], frame)
    return image


def build_animation() -> None:
    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    frames: list[Image.Image] = []
    for frame_index in range(FRAME_COUNT):
        frame = draw_frame(frame_index)
        frame.save(FRAMES_DIR / f"frame_{frame_index:03d}.png")
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
