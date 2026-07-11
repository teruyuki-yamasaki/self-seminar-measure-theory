#!/usr/bin/env python3
"""Rewrite caption bands for the rational density zoom GIFs."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageSequence


COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
}

FONT_REGULAR = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
FONT_BOLD = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"

FRAME_DURATION_MS = 150
GIF_LOOP = 0
try:
    ADAPTIVE_PALETTE = Image.Palette.ADAPTIVE
except AttributeError:
    ADAPTIVE_PALETTE = Image.ADAPTIVE


ANIMATIONS = (
    {
        "gif_path": Path("figures/measure/animations/rational_density_zoom_centered/gif/rational_density_zoom_centered.gif"),
        "title": "有理点だけを含む小正方形は取れない",
        "description": (
            "赤い正方形は, 有理点集合 A の内側近似の候補である.\n"
            "しかしどれほど小さくしても無理数が入り込むので, 正方形全体を A の中に入れることはできない."
        ),
    },
    {
        "gif_path": Path("figures/measure/animations/rational_density_zoom/gif/rational_density_zoom.gif"),
        "title": "無理数点だけを含む小正方形も取れない",
        "description": (
            "赤い正方形は, 有理点を避けて A^c の内側に入れたい候補である.\n"
            "しかしどの小正方形にも有理点が残るので, 正方形全体を A^c の中に入れることはできない."
        ),
    },
)


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size=size)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    try:
        box = draw.textbbox((0, 0), text, font=font)
        return box[2] - box[0], box[3] - box[1]
    except AttributeError:
        return draw.textsize(text, font=font)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    if "\n" in text:
        lines: list[str] = []
        for part in text.splitlines():
            lines.extend(wrap_text(draw, part, font, max_width))
        return lines
    if not text:
        return [""]

    words = text.split(" ")
    lines = [words[0]]
    for word in words[1:]:
        trial = f"{lines[-1]} {word}"
        width, _ = text_size(draw, trial, font)
        if width <= max_width:
            lines[-1] = trial
        else:
            lines.append(word)
    return lines


def fit_wrapped_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    max_width: int,
    max_lines: int,
    start_size: int,
    min_size: int,
    bold: bool = False,
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(start_size, min_size - 1, -2):
        font = load_font(size, bold=bold)
        lines = wrap_text(draw, text, font, max_width)
        if len(lines) <= max_lines and all(text_size(draw, line, font)[0] <= max_width for line in lines):
            return font, lines
    font = load_font(min_size, bold=bold)
    return font, wrap_text(draw, text, font, max_width)


def draw_centered_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    font: ImageFont.FreeTypeFont,
    *,
    center_x: int,
    top: int,
    area_height: int,
    fill: str,
    line_gap: int,
) -> None:
    heights = [text_size(draw, line, font)[1] for line in lines]
    total_height = sum(heights) + line_gap * (len(lines) - 1)
    y = top + (area_height - total_height) / 2
    for line, height in zip(lines, heights):
        width, _ = text_size(draw, line, font)
        draw.text((center_x - width / 2, y), line, font=font, fill=fill)
        y += height + line_gap


def rewrite_frame_text(image: Image.Image, title: str, description: str) -> Image.Image:
    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image)
    width, height = image.size
    paper = COLORS["paper"]

    title_top = 0
    title_height = 140
    desc_height = 240
    desc_top = height - desc_height

    draw.rectangle((0, title_top, width, title_top + title_height), fill=paper)
    draw.rectangle((0, desc_top, width, height), fill=paper)

    title_font, title_lines = fit_wrapped_font(
        draw,
        title,
        max_width=int(width * 0.92),
        max_lines=2,
        start_size=54,
        min_size=38,
        bold=False,
    )
    desc_font, desc_lines = fit_wrapped_font(
        draw,
        description,
        max_width=int(width * 0.82),
        max_lines=3,
        start_size=28,
        min_size=22,
        bold=False,
    )

    draw_centered_lines(
        draw,
        title_lines,
        title_font,
        center_x=width // 2,
        top=title_top + 10,
        area_height=title_height - 10,
        fill=COLORS["ink"],
        line_gap=8,
    )
    draw_centered_lines(
        draw,
        desc_lines,
        desc_font,
        center_x=width // 2,
        top=desc_top + 12,
        area_height=desc_height - 18,
        fill=COLORS["muted"],
        line_gap=6,
    )
    return image


def rebuild_gif(gif_path: Path, title: str, description: str) -> None:
    with Image.open(gif_path) as source:
        images = []
        for frame in ImageSequence.Iterator(source):
            rewritten = rewrite_frame_text(frame.copy(), title, description)
            images.append(rewritten.convert("P", palette=ADAPTIVE_PALETTE))
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=FRAME_DURATION_MS,
        loop=GIF_LOOP,
        disposal=2,
    )


def main() -> None:
    for animation in ANIMATIONS:
        rebuild_gif(animation["gif_path"], animation["title"], animation["description"])
        print(f"Updated captions: {animation['gif_path']}")


if __name__ == "__main__":
    main()
