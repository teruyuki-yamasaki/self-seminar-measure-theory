#!/usr/bin/env python3
"""Generate a GIF for Lebesgue inner measure via complement covers."""

from __future__ import annotations

from pathlib import Path
import shutil

import lebesgue_inner_outer_overlap_animation as base
from PIL import Image, ImageDraw


OUTDIR = Path("figures/measure/animations/lebesgue_inner_measure")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "lebesgue_inner_measure.gif"

CANVAS_W = base.CANVAS_W
CANVAS_H = base.CANVAS_H
FRAME_DURATION_MS = 1000
LOOP = 0

PAPER = base.PAPER
INK = base.INK
MUTED = base.MUTED
GRID = base.GRID
I_EDGE = base.I_EDGE
COMPLEMENT_FILL = base.COMPLEMENT_FILL
COMPLEMENT_EDGE = base.COMPLEMENT_EDGE
A_FILL = base.A_FILL
A_EDGE = base.A_EDGE
SET_A_FILL = (108, 169, 126, 190)
SET_A_EDGE = (31, 87, 53, 230)

LEFT_BOX = (52, 96, 666, 534)
PANEL_BOX = (704, 116, 1040, 508)


def ensure_dirs() -> None:
    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)


def map_point(x: float, y: float) -> tuple[int, int]:
    x0, y0, x1, y1 = LEFT_BOX
    return int(x0 + x * (x1 - x0)), int(y1 - y * (y1 - y0))


def map_rect(rect: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = rect
    p0 = map_point(x0, y1)
    p1 = map_point(x1, y0)
    return p0[0], p0[1], p1[0], p1[1]


A_PIXELS = [map_point(float(x), float(y)) for x, y in base.A_POINTS]
I_PIXELS = map_rect(base.I_RECT)


def centered_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font, fill) -> None:
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
    else:
        width, height = draw.textsize(text, font=font)
    draw.text((xy[0] - width / 2, xy[1] - height / 2), text, font=font, fill=fill)


def draw_rich_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    runs: list[tuple[str, object, tuple[int, int, int, int], int]],
    centered: bool = False,
) -> float:
    boxes = []
    for text, font, _fill, _dy in runs:
        if hasattr(draw, "textbbox"):
            boxes.append(draw.textbbox((0, 0), text, font=font))
        else:
            width, height = draw.textsize(text, font=font)
            boxes.append((0, 0, width, height))
    total_width = sum(box[2] - box[0] for box in boxes)
    top = min(dy + box[1] for box, (_text, _font, _fill, dy) in zip(boxes, runs))
    bottom = max(dy + box[3] for box, (_text, _font, _fill, dy) in zip(boxes, runs))
    x = xy[0] - total_width / 2 if centered else xy[0]
    y = xy[1] - (top + bottom) / 2 if centered else xy[1]

    for (text, font, fill, dy), box in zip(runs, boxes):
        draw.text((x, y + dy), text, font=font, fill=fill)
        x += box[2] - box[0]
    return x


def inner_measure_formula_runs(fill=INK) -> list[tuple[str, object, tuple[int, int, int, int], int]]:
    return [
        ("μ", base.FONT_BODY, fill, 0),
        ("*", base.FONT_SMALL, fill, 7),
        ("(A; I)=m(I)-μ", base.FONT_BODY, fill, 0),
        ("*", base.FONT_SMALL, fill, -7),
        ("(I∩A", base.FONT_BODY, fill, 0),
        ("c", base.FONT_SMALL, fill, -7),
        (")", base.FONT_BODY, fill, 0),
    ]


def graph_title_runs(fill=INK) -> list[tuple[str, object, tuple[int, int, int, int], int]]:
    return [
        ("m(I)-C", base.FONT_BODY, fill, 0),
        ("n", base.FONT_SMALL, fill, 7),
        (" → μ", base.FONT_BODY, fill, 0),
        ("*", base.FONT_SMALL, fill, 7),
        ("(A; I)", base.FONT_BODY, fill, 0),
    ]


def draw_dashed_rect(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], fill, width: int = 3) -> None:
    x0, y0, x1, y1 = rect
    dash = 13
    gap = 7

    def line(start: tuple[int, int], end: tuple[int, int]) -> None:
        sx, sy = start
        ex, ey = end
        length = ((ex - sx) ** 2 + (ey - sy) ** 2) ** 0.5
        if length == 0:
            return
        ux = (ex - sx) / length
        uy = (ey - sy) / length
        pos = 0.0
        while pos < length:
            next_pos = min(length, pos + dash)
            draw.line((sx + ux * pos, sy + uy * pos, sx + ux * next_pos, sy + uy * next_pos), fill=fill, width=width)
            pos += dash + gap

    line((x0, y0), (x1, y0))
    line((x1, y0), (x1, y1))
    line((x1, y1), (x0, y1))
    line((x0, y1), (x0, y0))


def rect_area(rect: tuple[float, float, float, float]) -> float:
    x0, y0, x1, y1 = rect
    return max(0.0, x1 - x0) * max(0.0, y1 - y0)


def draw_complement_cover(image: Image.Image, rects: list[tuple[float, float, float, float]]) -> Image.Image:
    for rect in rects:
        layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        draw.rectangle(map_rect(rect), fill=COMPLEMENT_FILL, outline=COMPLEMENT_EDGE, width=1)
        image = Image.alpha_composite(image, layer)
    return image


def stage_values() -> tuple[list[float], float, float]:
    j_area = rect_area(base.I_RECT)
    inner_values = [stage.inner_area for stage in base.STAGES]
    return inner_values, base.AREA_A, j_area


def draw_graph(draw: ImageDraw.ImageDraw, stage_index: int) -> None:
    x0, y0, x1, y1 = PANEL_BOX
    inner_values, limit_value, j_area = stage_values()
    max_y = max(j_area, limit_value) * 1.05
    min_y = 0.0

    draw.rectangle((x0, y0, x1, y1), outline=GRID, width=1, fill=(255, 255, 255, 150))

    plot_x0 = x0 + 48
    plot_y0 = y0 + 58
    plot_x1 = x1 - 24
    plot_y1 = y1 - 54

    for i in range(5):
        y = int(plot_y1 - i * (plot_y1 - plot_y0) / 4)
        draw.line((plot_x0, y, plot_x1, y), fill=GRID, width=1)

    draw.line((plot_x0, plot_y1, plot_x1, plot_y1), fill=INK, width=2)
    draw.line((plot_x0, plot_y0, plot_x0, plot_y1), fill=INK, width=2)

    def gx(index: int) -> int:
        return int(plot_x0 + index * (plot_x1 - plot_x0) / (len(base.STAGES) - 1))

    def gy(value: float) -> int:
        return int(plot_y1 - (value - min_y) / (max_y - min_y) * (plot_y1 - plot_y0))

    visible = range(stage_index + 1)
    inner_points = [(gx(i), gy(inner_values[i])) for i in visible]

    limit_y = gy(limit_value)
    draw.line((plot_x0, limit_y, plot_x1, limit_y), fill=MUTED, width=2)
    if len(inner_points) > 1:
        draw.line(inner_points, fill=A_EDGE, width=4)

    for point in inner_points:
        x, y = point
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=A_EDGE)

    for i in range(len(base.STAGES)):
        x = gx(i)
        draw.line((x, plot_y1, x, plot_y1 + 5), fill=MUTED, width=1)

    draw_rich_text(draw, ((plot_x0 + plot_x1) // 2, y0 + 20), graph_title_runs(INK), centered=True)
    draw.rectangle((plot_x0 + 4, y0 + 38, plot_x0 + 22, y0 + 50), fill=SET_A_FILL, outline=SET_A_EDGE)
    draw_rich_text(
        draw,
        (plot_x0 + 30, y0 + 34),
        [
            ("m(I)-C", base.FONT_SMALL, INK, 0),
            ("n", base.FONT_SMALL, INK, 5),
        ],
    )
    draw.line((plot_x0 + 132, y0 + 44, plot_x0 + 154, y0 + 44), fill=MUTED, width=2)
    draw_rich_text(
        draw,
        (plot_x0 + 162, y0 + 34),
        [
            ("μ", base.FONT_SMALL, INK, 0),
            ("*", base.FONT_SMALL, INK, 5),
            ("(A; I)", base.FONT_SMALL, INK, 0),
        ],
    )
    centered_text(draw, ((plot_x0 + plot_x1) // 2, plot_y1 + 32), "細分段階", base.FONT_SMALL, MUTED)


def draw_frame(stage_index: int) -> Image.Image:
    stage = base.STAGES[stage_index]

    image = Image.new("RGBA", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(image)

    centered_text(draw, (CANVAS_W // 2, 34), "Lebesgue 内測度: 補集合を外側から覆う", base.FONT_TITLE, INK)
    draw_rich_text(draw, (CANVAS_W // 2, 68), inner_measure_formula_runs(MUTED), centered=True)
    draw.rectangle(LEFT_BOX, outline=(176, 184, 194, 255), width=1)
    draw.polygon(A_PIXELS, fill=SET_A_FILL, outline=SET_A_EDGE)
    image = draw_complement_cover(image, stage.c_cover_rects)
    draw = ImageDraw.Draw(image)
    draw_dashed_rect(draw, I_PIXELS, I_EDGE)
    draw.line(A_PIXELS + [A_PIXELS[0]], fill=SET_A_EDGE, width=4)

    ix0, iy0, _ix1, _iy1 = I_PIXELS
    draw.text((ix0 + 9, iy0 + 8), "I", font=base.FONT_SUBTITLE, fill=I_EDGE)
    centered_text(draw, ((LEFT_BOX[0] + LEFT_BOX[2]) // 2, (LEFT_BOX[1] + LEFT_BOX[3]) // 2), "A", base.FONT_LABEL, (0, 0, 0, 210))

    legend_y = 560
    draw_dashed_rect(draw, (68, legend_y, 94, legend_y + 16), I_EDGE, width=2)
    draw.text((104, legend_y - 3), "I", font=base.FONT_SMALL, fill=INK)
    draw.rectangle((160, legend_y, 184, legend_y + 16), fill=SET_A_FILL, outline=SET_A_EDGE)
    draw.text((194, legend_y - 3), "A", font=base.FONT_SMALL, fill=INK)
    draw.rectangle((245, legend_y, 269, legend_y + 16), fill=COMPLEMENT_FILL, outline=COMPLEMENT_EDGE)
    end_x = draw_rich_text(
        draw,
        (279, legend_y - 3),
        [
            ("I∩A", base.FONT_SMALL, INK, 0),
            ("c", base.FONT_SMALL, INK, -5),
        ],
    )
    draw.text((end_x + 4, legend_y - 3), "の外側被覆", font=base.FONT_SMALL, fill=INK)

    draw_graph(draw, stage_index)
    return image


def build_animation() -> None:
    ensure_dirs()
    frames: list[Image.Image] = []
    for index in range(len(base.STAGES)):
        frame = draw_frame(index)
        frame.save(FRAMES_DIR / f"frame_{index:03d}.png")
        frames.append(frame.convert("P", palette=Image.ADAPTIVE))

    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=LOOP,
        disposal=2,
    )
    print(f"Saved GIF to: {GIF_PATH.resolve()}")
    print(f"Saved frames to: {FRAMES_DIR.resolve()}")


if __name__ == "__main__":
    build_animation()
