
import math
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont


# ============================================================
# Output / animation settings
# ============================================================
GRAPH_GIF = Path(
    "figures/measure/animations/outer_measure_quadtree_late_stages/gif/"
    "outer_measure_quadtree_late_stages.gif"
)
COVER_ONLY_GIF = Path(
    "figures/measure/animations/outer_measure_quadtree_late_stages/gif/"
    "outer_measure_quadtree_late_stages_cover_only.gif"
)

GRAPH_CANVAS_W = 980
GRAPH_CANVAS_H = 520
COVER_CANVAS_W = 720
COVER_CANVAS_H = 520
FRAME_DURATION_MS = 950
LOOP = 0

GRAPH_COVER_BOX = (35, 85, 525, 475)
COVER_ONLY_BOX = (45, 70, 675, 455)
GRAPH_BOX = (585, 105, 940, 430)
GRAPH_COVER_VIEW = (0.08, 0.12, 0.92, 0.80)
GRAPH_COVER_TITLE_Y = 58
COVER_ONLY_VIEW = (0.08, 0.12, 0.92, 0.84)
COVER_ONLY_CROP_BOX = (58, 8, 662, 468)

# Interior tiles remain fairly coarse, while boundary tiles are refined.
INTERIOR_DEPTH = 3
STAGE_BOUNDARY_DEPTHS = [4, 5, 6, 7, 8, 9]
BASE_EXPANSIONS = [0.090, 0.055, 0.032, 0.018, 0.009, 0.0035]
IRREGULARITY_SCALES = [1.10, 0.85, 0.55, 0.32, 0.14, 0.04]


# ============================================================
# Font helpers
# ============================================================
def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
        if bold
        else "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc"
        if bold
        else "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
        if bold
        else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]

    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


FONT_TITLE = load_font(25, bold=True)
FONT_SUBTITLE = load_font(17, bold=True)
FONT_BODY = load_font(15)
FONT_SMALL = load_font(12)
FONT_A = load_font(24, bold=True)


# ============================================================
# Set A
# ============================================================
def make_set_A(n: int = 1600) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)

    radius = (
        0.30
        + 0.055 * np.sin(3.0 * theta + 0.35)
        + 0.031 * np.sin(5.0 * theta - 0.75)
        + 0.018 * np.cos(8.0 * theta)
    )

    x = 0.50 + 1.03 * radius * np.cos(theta)
    y = 0.50 + 0.88 * radius * np.sin(theta)

    return np.column_stack([x, y])


A_POINTS = make_set_A()
A_MIN_X = float(np.min(A_POINTS[:, 0]))
A_MAX_X = float(np.max(A_POINTS[:, 0]))
A_MIN_Y = float(np.min(A_POINTS[:, 1]))
A_MAX_Y = float(np.max(A_POINTS[:, 1]))
ROOT_MARGIN = 0.035


def polygon_area(points: np.ndarray) -> float:
    x = points[:, 0]
    y = points[:, 1]

    return 0.5 * abs(
        np.dot(x, np.roll(y, -1))
        - np.dot(y, np.roll(x, -1))
    )


AREA_A = polygon_area(A_POINTS)


# ============================================================
# Raster mask for fast geometric tests
# ============================================================
MASK_SIZE = 1000

mask_image = Image.new("1", (MASK_SIZE, MASK_SIZE), 0)
mask_draw = ImageDraw.Draw(mask_image)

mask_polygon = [
    (
        int(float(x) * (MASK_SIZE - 1)),
        int((1.0 - float(y)) * (MASK_SIZE - 1)),
    )
    for x, y in A_POINTS
]

mask_draw.polygon(mask_polygon, fill=1)
A_MASK = np.asarray(mask_image, dtype=bool)


# ============================================================
# Quadtree cells
# ============================================================
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


def stable_unit(tag: str) -> float:
    value = 0

    for ch in tag:
        value = (131 * value + ord(ch)) % 104729

    return value / 104729.0


def mask_window(cell: Cell) -> np.ndarray:
    ix0 = max(0, min(MASK_SIZE - 1, int(math.floor(cell.x0 * MASK_SIZE))))
    ix1 = max(ix0 + 1, min(MASK_SIZE, int(math.ceil(cell.x1 * MASK_SIZE))))

    iy0 = max(
        0,
        min(
            MASK_SIZE - 1,
            int(math.floor((1.0 - cell.y1) * MASK_SIZE)),
        ),
    )
    iy1 = max(
        iy0 + 1,
        min(
            MASK_SIZE,
            int(math.ceil((1.0 - cell.y0) * MASK_SIZE)),
        ),
    )

    return A_MASK[iy0:iy1, ix0:ix1]


def classify_cell(cell: Cell) -> str:
    """
    Return one of:
      - "outside": no part of A lies in the cell
      - "inside": the sampled cell is fully contained in A
      - "boundary": the cell intersects the boundary of A
    """
    window = mask_window(cell)

    if window.size == 0 or not window.any():
        return "outside"

    if window.all():
        return "inside"

    return "boundary"


def fill_ratio(cell: Cell) -> float:
    window = mask_window(cell)

    if window.size == 0:
        return 0.0

    return float(np.mean(window))


def split_cell(cell: Cell) -> List[Cell]:
    rx = 0.34 + 0.32 * stable_unit(cell.path + "x")
    ry = 0.34 + 0.32 * stable_unit(cell.path + "y")

    xm = cell.x0 + rx * cell.width
    ym = cell.y0 + ry * cell.height
    d = cell.depth + 1

    return [
        Cell(cell.x0, cell.y0, xm, ym, d, cell.path + "0"),
        Cell(xm, cell.y0, cell.x1, ym, d, cell.path + "1"),
        Cell(cell.x0, ym, xm, cell.y1, d, cell.path + "2"),
        Cell(xm, ym, cell.x1, cell.y1, d, cell.path + "3"),
    ]


def build_cover(
    boundary_depth: int,
    expansion: float,
    irregularity: float,
) -> Tuple[List[Tuple[float, float, float, float]], float]:
    root = Cell(
        max(0.0, A_MIN_X - ROOT_MARGIN),
        max(0.0, A_MIN_Y - ROOT_MARGIN),
        min(1.0, A_MAX_X + ROOT_MARGIN),
        min(1.0, A_MAX_Y + ROOT_MARGIN),
        0,
        "",
    )
    queue = [root]
    leaves: List[Cell] = []

    while queue:
        cell = queue.pop()
        classification = classify_cell(cell)

        if classification == "outside":
            continue

        ratio = fill_ratio(cell)
        target_depth = (
            boundary_depth
            if classification == "boundary"
            else INTERIOR_DEPTH
        )

        if classification == "boundary":
            if ratio < 0.22:
                target_depth += 1
            if ratio < 0.10:
                target_depth += 1

        if cell.depth < target_depth:
            queue.extend(split_cell(cell))
            continue

        leaves.append(cell)

    rectangles: List[Tuple[float, float, float, float]] = []

    for cell in leaves:
        left_extra = expansion * (
            1.0 + irregularity * stable_unit(cell.path + "L")
        )
        right_extra = expansion * (
            1.0 + irregularity * stable_unit(cell.path + "R")
        )
        lower_extra = expansion * (
            1.0 + irregularity * stable_unit(cell.path + "D")
        )
        upper_extra = expansion * (
            1.0 + irregularity * stable_unit(cell.path + "U")
        )

        rectangles.append(
            (
                cell.x0 - left_extra,
                cell.y0 - lower_extra,
                cell.x1 + right_extra,
                cell.y1 + upper_extra,
            )
        )

    area_sum = sum(
        (x1 - x0) * (y1 - y0)
        for x0, y0, x1, y1 in rectangles
    )

    return rectangles, area_sum


# ============================================================
# Build all completed covers
# ============================================================
COVERS: List[List[Tuple[float, float, float, float]]] = []
RAW_AREAS: List[float] = []

for boundary_depth, expansion, irregularity in zip(
    STAGE_BOUNDARY_DEPTHS,
    BASE_EXPANSIONS,
    IRREGULARITY_SCALES,
):
    rectangles, area_sum = build_cover(
        boundary_depth=boundary_depth,
        expansion=expansion,
        irregularity=irregularity,
    )

    COVERS.append(rectangles)
    RAW_AREAS.append(area_sum)


# ============================================================
# Drawing helpers
# ============================================================
def map_point(
    x: float,
    y: float,
    box: Tuple[int, int, int, int],
    view: Tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0),
) -> Tuple[int, int]:
    x0, y0, x1, y1 = box
    vx0, vy0, vx1, vy1 = view
    x_ratio = (x - vx0) / (vx1 - vx0)
    y_ratio = (y - vy0) / (vy1 - vy0)

    return (
        int(x0 + x_ratio * (x1 - x0)),
        int(y1 - y_ratio * (y1 - y0)),
    )


def map_rect(
    rect: Tuple[float, float, float, float],
    box: Tuple[int, int, int, int],
    view: Tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0),
) -> Tuple[int, int, int, int]:
    x0, y0, x1, y1 = rect

    p0 = map_point(x0, y1, box, view)
    p1 = map_point(x1, y0, box, view)

    bx0, by0, bx1, by1 = box

    return (
        max(bx0, min(bx1, p0[0])),
        max(by0, min(by1, p0[1])),
        max(bx0, min(bx1, p1[0])),
        max(by0, min(by1, p1[1])),
    )


def centered_text(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: Tuple[int, int, int],
) -> None:
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
    else:
        width, height = draw.textsize(text, font=font)

    draw.text(
        (xy[0] - width / 2, xy[1] - height / 2),
        text,
        font=font,
        fill=fill,
    )


def draw_rich_text(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    runs: List[Tuple[str, ImageFont.FreeTypeFont, Tuple[int, int, int], int]],
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


def mu_star_a_runs(
    fill: Tuple[int, int, int],
) -> List[Tuple[str, ImageFont.FreeTypeFont, Tuple[int, int, int], int]]:
    return [
        ("μ", FONT_BODY, fill, 0),
        ("*", FONT_SMALL, fill, -7),
        ("(A)", FONT_BODY, fill, 0),
    ]


def graph_title_runs(
    fill: Tuple[int, int, int],
) -> List[Tuple[str, ImageFont.FreeTypeFont, Tuple[int, int, int], int]]:
    return [
        ("被覆和 ", FONT_SUBTITLE, fill, 0),
        ("Σ m(I", FONT_SUBTITLE, fill, 0),
        ("k", FONT_SMALL, fill, 6),
        (") が μ", FONT_SUBTITLE, fill, 0),
        ("*", FONT_SMALL, fill, -7),
        ("(A) に近づく", FONT_SUBTITLE, fill, 0),
    ]


def draw_cover_scene(
    image: Image.Image,
    box: Tuple[int, int, int, int],
    rectangles: List[Tuple[float, float, float, float]],
    stage: int,
    canvas_w: int,
    view: Tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0),
    title_y: int = 35,
) -> Image.Image:
    draw = ImageDraw.Draw(image)
    a_pixels = [
        map_point(float(x), float(y), box, view)
        for x, y in A_POINTS
    ]

    centered_text(
        draw,
        ((box[0] + box[2]) // 2, title_y),
        (
            f"段階 {stage + 1}: 境界深さ {STAGE_BOUNDARY_DEPTHS[stage]}, "
            f"被覆長方形 {len(rectangles)} 個"
        ),
        FONT_SUBTITLE,
        (30, 30, 30),
    )

    draw.polygon(
        a_pixels,
        fill=(205, 205, 205, 255),
        outline=(0, 0, 0, 255),
    )

    centered_text(
        draw,
        (
            (box[0] + box[2]) // 2,
            (box[1] + box[3]) // 2,
        ),
        "A",
        FONT_A,
        (0, 0, 0),
    )

    for rect in rectangles:
        rect_layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )
        rect_draw = ImageDraw.Draw(rect_layer)
        rect_draw.rectangle(
            map_rect(rect, box, view),
            fill=(31, 119, 180, 56),
            outline=(15, 70, 125, 150),
            width=1,
        )
        image = Image.alpha_composite(image, rect_layer)

    draw = ImageDraw.Draw(image)
    draw.line(
        a_pixels + [a_pixels[0]],
        fill=(0, 0, 0, 255),
        width=3,
    )

    return image


def draw_graph(
    draw: ImageDraw.ImageDraw,
    stage: int,
) -> None:
    x0, y0, x1, y1 = GRAPH_BOX

    draw.line((x0, y1, x1, y1), fill=(40, 40, 40), width=2)
    draw.line((x0, y0, x0, y1), fill=(40, 40, 40), width=2)

    lower = AREA_A * 0.985
    upper = max(RAW_AREAS) * 1.015

    def graph_x(i: int) -> int:
        return int(
            x0
            + 28
            + i * (x1 - x0 - 56) / (len(STAGE_BOUNDARY_DEPTHS) - 1)
        )

    def graph_y(value: float) -> int:
        ratio = (value - lower) / (upper - lower)

        return int(
            y1
            - 20
            - ratio * (y1 - y0 - 42)
        )

    target_y = graph_y(AREA_A)

    draw.line(
        (x0, target_y, x1, target_y),
        fill=(105, 105, 105),
        width=2,
    )

    draw_rich_text(draw, (x0 + 7, target_y - 20), mu_star_a_runs((75, 75, 75)))

    points = [
        (graph_x(i), graph_y(RAW_AREAS[i]))
        for i in range(stage + 1)
    ]

    if len(points) > 1:
        draw.line(
            points,
            fill=(31, 119, 180),
            width=4,
        )

    for px, py in points:
        draw.ellipse(
            (px - 5, py - 5, px + 5, py + 5),
            fill=(31, 119, 180),
        )

    for i in range(len(STAGE_BOUNDARY_DEPTHS)):
        px = graph_x(i)

        draw.line(
            (px, y1, px, y1 + 5),
            fill=(40, 40, 40),
            width=1,
        )

        centered_text(
            draw,
            (px, y1 + 19),
            str(i + 1),
            FONT_SMALL,
            (40, 40, 40),
        )

    centered_text(
        draw,
        ((x0 + x1) // 2, y1 + 48),
        "境界細分の段階",
        FONT_BODY,
        (40, 40, 40),
    )

    draw_rich_text(
        draw,
        ((x0 + x1) // 2, y0 - 24),
        graph_title_runs((25, 25, 25)),
        centered=True,
    )


# ============================================================
# Render completed-cover frames
# ============================================================
graph_frames: List[Image.Image] = []
cover_frames: List[Image.Image] = []
cover_rgba_frames: List[Image.Image] = []

for stage, rectangles in enumerate(COVERS):
    graph_image = Image.new(
        "RGBA",
        (GRAPH_CANVAS_W, GRAPH_CANVAS_H),
        (249, 249, 247, 255),
    )
    graph_image = draw_cover_scene(
        graph_image,
        GRAPH_COVER_BOX,
        rectangles,
        stage,
        GRAPH_CANVAS_W,
        view=GRAPH_COVER_VIEW,
        title_y=GRAPH_COVER_TITLE_Y,
    )
    graph_draw = ImageDraw.Draw(graph_image)
    draw_graph(graph_draw, stage)

    excess = RAW_AREAS[stage] - AREA_A
    label_x = 218
    label_y = 486
    graph_draw.text(
        (label_x, label_y),
        f"被覆和 = {RAW_AREAS[stage]:.6f}   ",
        font=FONT_BODY,
        fill=(35, 35, 35),
    )
    end_x = draw_rich_text(
        graph_draw,
        (label_x + 180, label_y),
        mu_star_a_runs((35, 35, 35)),
    )
    graph_draw.text(
        (end_x + 4, label_y),
        f"からの超過 = {excess:.6f}",
        font=FONT_BODY,
        fill=(35, 35, 35),
    )

    graph_frames.append(
        graph_image.convert(
            "P",
            palette=Image.ADAPTIVE,
        )
    )

    cover_image = Image.new(
        "RGBA",
        (COVER_CANVAS_W, COVER_CANVAS_H),
        (249, 249, 247, 255),
    )
    cover_image = draw_cover_scene(
        cover_image,
        COVER_ONLY_BOX,
        rectangles,
        stage,
        COVER_CANVAS_W,
        view=COVER_ONLY_VIEW,
    )
    cover_rgba_frames.append(cover_image)

cover_frames = [
    image.crop(COVER_ONLY_CROP_BOX).convert(
        "P",
        palette=Image.ADAPTIVE,
    )
    for image in cover_rgba_frames
]
cover_frames = [cover_frames[-1].copy(), *cover_frames]


GRAPH_GIF.parent.mkdir(parents=True, exist_ok=True)

graph_frames[0].save(
    GRAPH_GIF,
    save_all=True,
    append_images=graph_frames[1:],
    duration=FRAME_DURATION_MS,
    loop=LOOP,
    optimize=False,
)

cover_frames[0].save(
    COVER_ONLY_GIF,
    save_all=True,
    append_images=cover_frames[1:],
    duration=FRAME_DURATION_MS,
    loop=LOOP,
    optimize=False,
)

print(f"Saved: {GRAPH_GIF.resolve()}")
print(f"Saved: {COVER_ONLY_GIF.resolve()}")
print(f"Area(A): {AREA_A:.8f}")
print("Raw cover sums:")
for i, value in enumerate(RAW_AREAS, start=1):
    print(f"  stage {i}: {value:.8f}")
