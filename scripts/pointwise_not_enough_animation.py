from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont


OUTPUT_GIF = Path(
    "figures/measure/animations/pointwise_not_enough/gif/"
    "pointwise_not_enough.gif"
)

CANVAS_W = 980
CANVAS_H = 520
FRAME_DURATION_MS = 1100
LOOP = 0

PLOT_BOX = (80, 95, 630, 410)
INFO_BOX = (680, 105, 935, 390)

N_VALUES = [1, 2, 4, 8, 16, 32]
Y_MAX = 34.0


def load_font(size: int, bold: bool = False):
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
        font_path = Path(path)
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size)

    return ImageFont.load_default()


FONT_TITLE = load_font(28, bold=True)
FONT_SUBTITLE = load_font(19, bold=True)
FONT_BODY = load_font(16)
FONT_SMALL = load_font(13)


def centered_text(draw, xy: Tuple[int, int], text: str, font, fill) -> None:
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
    else:
        width, height = draw.textsize(text, font=font)

    draw.text((xy[0] - width / 2, xy[1] - height / 2), text, font=font, fill=fill)


def map_point(x: float, y: float) -> Tuple[int, int]:
    x0, y0, x1, y1 = PLOT_BOX
    px = int(x0 + x * (x1 - x0))
    py = int(y1 - (y / Y_MAX) * (y1 - y0))
    return px, py


def draw_axes(draw) -> None:
    x0, y0, x1, y1 = PLOT_BOX
    draw.line((x0, y1, x1, y1), fill=(40, 40, 40), width=2)
    draw.line((x0, y0, x0, y1), fill=(40, 40, 40), width=2)

    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        px, py = map_point(t, 0.0)
        draw.line((px, py, px, py + 7), fill=(40, 40, 40), width=1)
        centered_text(draw, (px, py + 22), f"{t:g}", FONT_SMALL, (40, 40, 40))

    for y in [0, 8, 16, 24, 32]:
        px, py = map_point(0.0, float(y))
        draw.line((px - 7, py, px, py), fill=(40, 40, 40), width=1)
        centered_text(draw, (px - 24, py), str(y), FONT_SMALL, (40, 40, 40))

    centered_text(draw, ((x0 + x1) // 2, y1 + 48), "x", FONT_BODY, (40, 40, 40))
    centered_text(draw, (x0 - 44, y0 - 8), "f_n(x)", FONT_BODY, (40, 40, 40))


def draw_function(draw, n: int) -> None:
    left = map_point(0.0, 0.0)
    right = map_point(1.0 / n, float(n))
    base_right = map_point(1.0 / n, 0.0)

    draw.rectangle(
        (left[0], right[1], base_right[0], left[1]),
        fill=(39, 122, 184, 180),
        outline=(18, 76, 122),
        width=2,
    )

    x1 = map_point(1.0 / n, 0.0)[0]
    draw.line((x1, PLOT_BOX[3], x1, right[1]), fill=(18, 76, 122), width=2)
    draw.line((left[0], right[1], x1, right[1]), fill=(18, 76, 122), width=2)


def draw_info(draw, n: int) -> None:
    x0, y0, x1, y1 = INFO_BOX
    draw.rectangle(
        (x0, y0, x1, y1),
        outline=(170, 170, 170),
        width=2,
        fill=(252, 252, 250),
    )

    centered_text(draw, ((x0 + x1) // 2, y0 + 28), f"n = {n}", FONT_SUBTITLE, (20, 20, 20))

    lines = [
        "台",
        f"(0, 1/n) = (0, {1.0 / n:.5f})",
        "",
        "高さ",
        f"n = {n}",
        "",
        "面積",
        "n · (1/n) = 1",
        "",
        "各点での挙動",
        "各 x > 0 は十分大きい n で",
        "(0, 1/n) の外に出る",
    ]

    y = y0 + 68
    for line in lines:
        centered_text(draw, ((x0 + x1) // 2, y), line, FONT_BODY, (35, 35, 35))
        y += 28


def render_frame(n: int) -> Image.Image:
    image = Image.new("RGBA", (CANVAS_W, CANVAS_H), (249, 249, 247, 255))
    draw = ImageDraw.Draw(image)

    centered_text(
        draw,
        (CANVAS_W // 2, 30),
        "各点収束だけでは積分を制御できない",
        FONT_TITLE,
        (20, 20, 20),
    )
    centered_text(
        draw,
        (CANVAS_W // 2, 62),
        "f_n(x) = n  (0 < x < 1/n),  それ以外では 0",
        FONT_SUBTITLE,
        (30, 30, 30),
    )

    draw_axes(draw)
    draw_function(draw, n)
    draw_info(draw, n)

    centered_text(
        draw,
        (CANVAS_W // 2, 472),
        "山は細く高くなるが, 面積は常に 1 のまま",
        FONT_BODY,
        (40, 40, 40),
    )
    centered_text(
        draw,
        (CANVAS_W // 2, 496),
        "したがって f_n(x) -> 0 各点収束でも, ∫_0^1 f_n dμ = 1",
        FONT_BODY,
        (40, 40, 40),
    )

    return image.convert("P", palette=Image.ADAPTIVE)


def main() -> None:
    OUTPUT_GIF.parent.mkdir(parents=True, exist_ok=True)
    frames: List[Image.Image] = [render_frame(n) for n in N_VALUES]
    frames[0].save(
        OUTPUT_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=LOOP,
        optimize=False,
    )
    print(f"Saved: {OUTPUT_GIF.resolve()}")


if __name__ == "__main__":
    main()
