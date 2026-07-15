#!/usr/bin/env python3
"""Generate a GIF showing Lebesgue inner/outer approximations via complement covers."""

from __future__ import annotations

import math
import shutil
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


OUTDIR = Path("figures/measure/animations/lebesgue_inner_outer_overlap")
FRAMES_DIR = OUTDIR / "frames"
GIF_DIR = OUTDIR / "gif"
GIF_PATH = GIF_DIR / "lebesgue_inner_outer_overlap.gif"

CANVAS_W = 1080
CANVAS_H = 640
FRAME_DURATION_MS = 1000
LOOP = 0

LEFT_BOX = (42, 92, 650, 540)
GRAPH_BOX = (715, 130, 1035, 475)

MASK_SIZE = 900
STAGE_DEPTHS = [2, 3, 4, 5, 6, 7, 8]
EXPANSIONS = [0.170, 0.055, 0.036, 0.024, 0.015, 0.009, 0.004]

PAPER = (250, 249, 246, 255)
INK = (24, 32, 42, 255)
MUTED = (87, 99, 115, 255)
GRID = (204, 213, 224, 255)
A_FILL = (226, 226, 222, 255)
A_EDGE = (23, 30, 38, 255)
I_EDGE = (137, 78, 24, 235)
OUTER_FILL = (54, 132, 214, 32)
OUTER_EDGE = (28, 91, 158, 150)
COMPLEMENT_FILL = (241, 147, 74, 55)
COMPLEMENT_EDGE = (191, 94, 42, 125)
OVERLAP_FILL = (198, 61, 127, 115)
INNER_FILL = (93, 169, 112, 178)
INNER_EDGE = (38, 113, 65, 210)
AREA_LINE = (86, 86, 86, 255)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    japanese_candidates: list[str] = []
    for font_dir in (Path("/System/Library/Fonts"), Path("/System/Library/Fonts/Supplemental"), Path("/Library/Fonts")):
        if not font_dir.exists():
            continue
        for path in font_dir.glob("*"):
            name = path.name
            if any(token in name for token in ("ヒラ", "Hiragino", "AppleGothic", "NotoSansCJK")):
                japanese_candidates.append(str(path))

    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
        if bold
        else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in japanese_candidates + candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


FONT_TITLE = load_font(26, True)
FONT_SUBTITLE = load_font(17, True)
FONT_BODY = load_font(15)
FONT_SMALL = load_font(12)
FONT_LABEL = load_font(24, True)


@dataclass(frozen=True)
class Cell:
    x0: float
    y0: float
    x1: float
    y1: float
    depth: int
    path: str

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    @property
    def area(self) -> float:
        return self.width * self.height


@dataclass(frozen=True)
class Stage:
    depth: int
    inner_cells: list[Cell]
    complement_cells: list[Cell]
    boundary_cells: list[Cell]
    outer_cells: list[Cell]
    a_cover_rects: list[tuple[float, float, float, float]]
    c_cover_rects: list[tuple[float, float, float, float]]
    inner_area: float
    outer_area: float
    uncertainty_area: float


def make_set_a(n: int = 1500) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    radius = (
        0.305
        + 0.052 * np.sin(3.0 * theta + 0.45)
        + 0.030 * np.sin(5.0 * theta - 0.65)
        + 0.020 * np.cos(8.0 * theta + 0.20)
    )
    x = 0.50 + 1.02 * radius * np.cos(theta)
    y = 0.50 + 0.88 * radius * np.sin(theta)
    return np.column_stack([x, y])


A_POINTS = make_set_a()
A_MIN_X = float(np.min(A_POINTS[:, 0]))
A_MAX_X = float(np.max(A_POINTS[:, 0]))
A_MIN_Y = float(np.min(A_POINTS[:, 1]))
A_MAX_Y = float(np.max(A_POINTS[:, 1]))
I_RECT = (
    max(0.0, A_MIN_X - 0.05),
    max(0.0, A_MIN_Y - 0.05),
    min(1.0, A_MAX_X + 0.05),
    min(1.0, A_MAX_Y + 0.05),
)


def polygon_area(points: np.ndarray) -> float:
    x = points[:, 0]
    y = points[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


AREA_A = polygon_area(A_POINTS)


def build_mask() -> np.ndarray:
    image = Image.new("1", (MASK_SIZE, MASK_SIZE), 0)
    draw = ImageDraw.Draw(image)
    polygon = [
        (int(float(x) * (MASK_SIZE - 1)), int((1.0 - float(y)) * (MASK_SIZE - 1)))
        for x, y in A_POINTS
    ]
    draw.polygon(polygon, fill=1)
    return np.asarray(image, dtype=bool)


A_MASK = build_mask()


def stable_unit(tag: str) -> float:
    value = 0
    for ch in tag:
        value = (131 * value + ord(ch)) % 104729
    return value / 104729.0


def mask_window(cell: Cell) -> np.ndarray:
    ix0 = max(0, min(MASK_SIZE - 1, int(math.floor(cell.x0 * MASK_SIZE))))
    ix1 = max(ix0 + 1, min(MASK_SIZE, int(math.ceil(cell.x1 * MASK_SIZE))))
    iy0 = max(0, min(MASK_SIZE - 1, int(math.floor((1.0 - cell.y1) * MASK_SIZE))))
    iy1 = max(iy0 + 1, min(MASK_SIZE, int(math.ceil((1.0 - cell.y0) * MASK_SIZE))))
    return A_MASK[iy0:iy1, ix0:ix1]


def classify(cell: Cell) -> str:
    window = mask_window(cell)
    if window.size == 0 or not window.any():
        return "outside"
    if window.all():
        return "inside"
    return "boundary"


def split_cell(cell: Cell) -> list[Cell]:
    rx = 0.40 + 0.20 * stable_unit(cell.path + "x")
    ry = 0.40 + 0.20 * stable_unit(cell.path + "y")
    xm = cell.x0 + rx * cell.width
    ym = cell.y0 + ry * cell.height
    d = cell.depth + 1
    return [
        Cell(cell.x0, cell.y0, xm, ym, d, cell.path + "0"),
        Cell(xm, cell.y0, cell.x1, ym, d, cell.path + "1"),
        Cell(cell.x0, ym, xm, cell.y1, d, cell.path + "2"),
        Cell(xm, ym, cell.x1, cell.y1, d, cell.path + "3"),
    ]


def expanded_rect(cell: Cell, expansion: float, tag: str) -> tuple[float, float, float, float]:
    left = expansion * (0.55 + 0.90 * stable_unit(cell.path + tag + "L"))
    right = expansion * (0.55 + 0.90 * stable_unit(cell.path + tag + "R"))
    lower = expansion * (0.55 + 0.90 * stable_unit(cell.path + tag + "D"))
    upper = expansion * (0.55 + 0.90 * stable_unit(cell.path + tag + "U"))
    return (
        max(0.0, cell.x0 - left),
        max(0.0, cell.y0 - lower),
        min(1.0, cell.x1 + right),
        min(1.0, cell.y1 + upper),
    )


def build_stage(depth: int, expansion: float) -> Stage:
    root = Cell(
        I_RECT[0],
        I_RECT[1],
        I_RECT[2],
        I_RECT[3],
        0,
        "",
    )
    queue = [root]
    leaves: list[Cell] = []

    while queue:
        cell = queue.pop()
        kind = classify(cell)
        if cell.depth < depth and kind == "boundary":
            queue.extend(split_cell(cell))
            continue
        leaves.append(cell)

    inner_cells = [cell for cell in leaves if classify(cell) == "inside"]
    complement_cells = [cell for cell in leaves if classify(cell) == "outside"]
    boundary_cells = [cell for cell in leaves if classify(cell) == "boundary"]
    outer_cells = inner_cells + boundary_cells
    a_cover_rects = [expanded_rect(cell, expansion, "A") for cell in outer_cells]
    c_cover_rects = [expanded_rect(cell, expansion, "C") for cell in complement_cells + boundary_cells]
    inner_area = sum(cell.area for cell in inner_cells)
    outer_area = sum(cell.area for cell in outer_cells)
    uncertainty_area = sum(cell.area for cell in boundary_cells)
    return Stage(
        depth,
        inner_cells,
        complement_cells,
        boundary_cells,
        outer_cells,
        a_cover_rects,
        c_cover_rects,
        inner_area,
        outer_area,
        uncertainty_area,
    )


STAGES = [build_stage(depth, expansion) for depth, expansion in zip(STAGE_DEPTHS, EXPANSIONS)]


def ensure_dirs() -> None:
    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)


def map_point(x: float, y: float, box: tuple[int, int, int, int]) -> tuple[int, int]:
    x0, y0, x1, y1 = box
    return int(x0 + x * (x1 - x0)), int(y1 - y * (y1 - y0))


def map_rect(rect: tuple[float, float, float, float], box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = rect
    p0 = map_point(x0, y1, box)
    p1 = map_point(x1, y0, box)
    return p0[0], p0[1], p1[0], p1[1]


A_PIXELS = [map_point(float(x), float(y), LEFT_BOX) for x, y in A_POINTS]


def centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int] | tuple[int, int, int],
) -> None:
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
    else:
        width, height = draw.textsize(text, font=font)
    draw.text((xy[0] - width / 2, xy[1] - height / 2), text, font=font, fill=fill)


def draw_inner_cells(image: Image.Image, cells: list[Cell]) -> Image.Image:
    layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for cell in cells:
        rect = map_rect((cell.x0, cell.y0, cell.x1, cell.y1), LEFT_BOX)
        draw.rectangle(rect, fill=INNER_FILL, outline=INNER_EDGE, width=1)
    return Image.alpha_composite(image, layer)


def draw_cells(
    image: Image.Image,
    cells: list[Cell],
    fill: tuple[int, int, int, int],
    outline: tuple[int, int, int, int],
    width: int = 1,
) -> Image.Image:
    for cell in cells:
        layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        rect = map_rect((cell.x0, cell.y0, cell.x1, cell.y1), LEFT_BOX)
        draw.rectangle(rect, fill=fill, outline=outline, width=width)
        image = Image.alpha_composite(image, layer)
    return image


def draw_rect_cover(
    image: Image.Image,
    rects: list[tuple[float, float, float, float]],
    fill: tuple[int, int, int, int],
    outline: tuple[int, int, int, int],
    width: int = 1,
) -> Image.Image:
    for rect in rects:
        layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        draw.rectangle(map_rect(rect, LEFT_BOX), fill=fill, outline=outline, width=width)
        image = Image.alpha_composite(image, layer)
    return image


def rects_to_count(rects: list[tuple[float, float, float, float]]) -> np.ndarray:
    x0, y0, x1, y1 = LEFT_BOX
    width = x1 - x0
    height = y1 - y0
    count = np.zeros((height, width), dtype=np.uint16)
    for rect in rects:
        rx0, ry0, rx1, ry1 = map_rect(rect, LEFT_BOX)
        rx0 = max(x0, min(x1 - 1, rx0)) - x0
        rx1 = max(x0 + 1, min(x1, rx1)) - x0
        ry0 = max(y0, min(y1 - 1, ry0)) - y0
        ry1 = max(y0 + 1, min(y1, ry1)) - y0
        count[ry0:ry1, rx0:rx1] += 1
    return count


def draw_cover_overlap(
    image: Image.Image,
    a_rects: list[tuple[float, float, float, float]],
    c_rects: list[tuple[float, float, float, float]],
) -> Image.Image:
    x0, y0, x1, y1 = LEFT_BOX
    a_count = rects_to_count(a_rects)
    c_count = rects_to_count(c_rects)
    mask = (a_count > 0) & (c_count > 0)
    rgba = np.zeros((y1 - y0, x1 - x0, 4), dtype=np.uint8)
    rgba[..., 0] = OVERLAP_FILL[0]
    rgba[..., 1] = OVERLAP_FILL[1]
    rgba[..., 2] = OVERLAP_FILL[2]
    rgba[..., 3] = np.where(mask, OVERLAP_FILL[3], 0).astype(np.uint8)
    layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    layer.paste(Image.fromarray(rgba, "RGBA"), (x0, y0))
    return Image.alpha_composite(image, layer)


def draw_cell_outlines(
    image: Image.Image,
    cells: list[Cell],
    outline: tuple[int, int, int, int],
    width: int = 1,
) -> Image.Image:
    layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for cell in cells:
        rect = map_rect((cell.x0, cell.y0, cell.x1, cell.y1), LEFT_BOX)
        draw.rectangle(rect, fill=(0, 0, 0, 0), outline=outline, width=width)
    return Image.alpha_composite(image, layer)


def draw_dashed_rect(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    fill: tuple[int, int, int, int],
    width: int = 3,
    dash: int = 12,
    gap: int = 7,
) -> None:
    x0, y0, x1, y1 = rect

    def dashed_line(start: tuple[int, int], end: tuple[int, int]) -> None:
        sx, sy = start
        ex, ey = end
        length = math.hypot(ex - sx, ey - sy)
        if length == 0:
            return
        ux = (ex - sx) / length
        uy = (ey - sy) / length
        pos = 0.0
        while pos < length:
            next_pos = min(length, pos + dash)
            draw.line(
                (
                    sx + ux * pos,
                    sy + uy * pos,
                    sx + ux * next_pos,
                    sy + uy * next_pos,
                ),
                fill=fill,
                width=width,
            )
            pos += dash + gap

    dashed_line((x0, y0), (x1, y0))
    dashed_line((x1, y0), (x1, y1))
    dashed_line((x1, y1), (x0, y1))
    dashed_line((x0, y1), (x0, y0))


def draw_graph(draw: ImageDraw.ImageDraw, stage_index: int) -> None:
    x0, y0, x1, y1 = GRAPH_BOX
    draw.line((x0, y1, x1, y1), fill=INK, width=2)
    draw.line((x0, y0, x0, y1), fill=INK, width=2)

    values = [stage.outer_area for stage in STAGES] + [stage.inner_area for stage in STAGES] + [AREA_A]
    lower = 0.0
    upper = max(values) * 1.05

    def gx(i: int) -> int:
        return int(x0 + 25 + i * (x1 - x0 - 50) / (len(STAGES) - 1))

    def gy(value: float) -> int:
        return int(y1 - 20 - (value - lower) / (upper - lower) * (y1 - y0 - 42))

    for ratio in np.linspace(0.0, 1.0, 5):
        y = int(y1 - 20 - ratio * (y1 - y0 - 42))
        draw.line((x0, y, x1, y), fill=GRID, width=1)

    area_y = gy(AREA_A)
    draw.line((x0, area_y, x1, area_y), fill=AREA_LINE, width=2)
    draw.text((x0 + 7, area_y - 20), "真の面積 A", font=FONT_SMALL, fill=AREA_LINE)

    visible = STAGES[: stage_index + 1]
    outer_points = [(gx(i), gy(stage.outer_area)) for i, stage in enumerate(visible)]
    inner_points = [(gx(i), gy(stage.inner_area)) for i, stage in enumerate(visible)]

    if len(outer_points) > 1:
        draw.line(outer_points, fill=(31, 105, 179, 255), width=4)
        draw.line(inner_points, fill=(49, 137, 82, 255), width=4)

    for px, py in outer_points:
        draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(31, 105, 179, 255))
    for px, py in inner_points:
        draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(49, 137, 82, 255))

    for i in range(len(STAGES)):
        px = gx(i)
        draw.line((px, y1, px, y1 + 5), fill=INK, width=1)
        centered_text(draw, (px, y1 + 18), str(i + 1), FONT_SMALL, INK)

    centered_text(draw, ((x0 + x1) // 2, y1 + 48), "細分段階", FONT_BODY, INK)
    centered_text(draw, ((x0 + x1) // 2, y0 - 28), "外側の大きさと内側の大きさが近づく", FONT_SUBTITLE, INK)

    draw.rectangle((x0 + 18, y0 + 18, x0 + 38, y0 + 30), fill=(31, 105, 179, 255))
    draw.text((x0 + 46, y0 + 13), "A の外側被覆", font=FONT_SMALL, fill=INK)
    draw.rectangle((x0 + 18, y0 + 42, x0 + 38, y0 + 54), fill=(49, 137, 82, 255))
    draw.text((x0 + 46, y0 + 37), "I から (I∩A^c) の被覆を除いた部分", font=FONT_SMALL, fill=INK)


def draw_legend(draw: ImageDraw.ImageDraw) -> None:
    x = 62
    y = 555
    draw_dashed_rect(draw, (x, y, x + 22, y + 14), I_EDGE, width=2, dash=7, gap=4)
    draw.text((x + 30, y - 3), r"I", font=FONT_SMALL, fill=INK)
    draw.rectangle((x + 70, y, x + 92, y + 14), fill=OUTER_FILL, outline=OUTER_EDGE)
    draw.text((x + 100, y - 3), r"A の外側被覆", font=FONT_SMALL, fill=INK)
    draw.rectangle((x + 245, y, x + 267, y + 14), fill=COMPLEMENT_FILL, outline=COMPLEMENT_EDGE)
    draw.text((x + 275, y - 3), r"I∩A^c の外側被覆", font=FONT_SMALL, fill=INK)
    draw.rectangle((x + 475, y, x + 497, y + 14), fill=OVERLAP_FILL)
    draw.text((x + 505, y - 3), "被覆の重なり", font=FONT_SMALL, fill=INK)
    draw.rectangle((x + 620, y, x + 642, y + 14), fill=INNER_FILL, outline=INNER_EDGE)
    draw.text((x + 650, y - 3), r"I から (I∩A^c) の外側被覆を除いた部分", font=FONT_SMALL, fill=INK)


def draw_frame(stage_index: int) -> Image.Image:
    stage = STAGES[stage_index]
    image = Image.new("RGBA", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(image)

    centered_text(draw, (CANVAS_W // 2, 32), "Lebesgue 内測度と外測度の対応", FONT_TITLE, INK)
    centered_text(
        draw,
        ((LEFT_BOX[0] + LEFT_BOX[2]) // 2, 68),
        f"段階 {stage_index + 1}: 細分の深さ {stage.depth}, 境界セル {len(stage.boundary_cells)} 個",
        FONT_SUBTITLE,
        INK,
    )

    draw.rectangle(LEFT_BOX, outline=(176, 184, 194, 255), width=1)
    draw.polygon(A_PIXELS, fill=A_FILL, outline=A_EDGE)
    image = draw_inner_cells(image, stage.inner_cells)
    image = draw_rect_cover(image, stage.c_cover_rects, COMPLEMENT_FILL, COMPLEMENT_EDGE, width=1)
    image = draw_rect_cover(image, stage.a_cover_rects, OUTER_FILL, OUTER_EDGE, width=1)
    image = draw_cover_overlap(image, stage.a_cover_rects, stage.c_cover_rects)
    image = draw_cell_outlines(image, stage.outer_cells, OUTER_EDGE, width=1)
    draw = ImageDraw.Draw(image)
    draw_dashed_rect(draw, map_rect(I_RECT, LEFT_BOX), I_EDGE, width=3, dash=13, gap=7)
    ix0, iy0, ix1, iy1 = map_rect(I_RECT, LEFT_BOX)
    draw.text((ix0 + 8, iy0 + 7), "I", font=FONT_SUBTITLE, fill=I_EDGE)
    draw.line(A_PIXELS + [A_PIXELS[0]], fill=A_EDGE, width=3)

    centered_text(
        draw,
        ((LEFT_BOX[0] + LEFT_BOX[2]) // 2, (LEFT_BOX[1] + LEFT_BOX[3]) // 2),
        "A",
        FONT_LABEL,
        (0, 0, 0, 205),
    )
    draw_legend(draw)
    draw_graph(draw, stage_index)

    gap = stage.outer_area - stage.inner_area
    centered_text(
        draw,
        (CANVAS_W // 2, 610),
        (
            f"内側 m(I)-μ*(I∩A^c) = {stage.inner_area:.5f}   "
            f"A の面積 = {AREA_A:.5f}   "
            f"外側 μ*(A) の近似 = {stage.outer_area:.5f}   "
            f"被覆の重なり = {stage.uncertainty_area:.5f}   "
            f"差 = {gap:.5f}"
        ),
        FONT_BODY,
        MUTED,
    )
    return image


def build_animation() -> None:
    ensure_dirs()
    frames: list[Image.Image] = []
    for index in range(len(STAGES)):
        frame = draw_frame(index)
        frame_path = FRAMES_DIR / f"frame_{index:03d}.png"
        frame.save(frame_path)
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
    print(f"Saved frames to: {FRAMES_DIR.resolve()}")


if __name__ == "__main__":
    build_animation()
