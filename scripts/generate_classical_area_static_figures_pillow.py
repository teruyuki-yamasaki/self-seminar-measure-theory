#!/usr/bin/env python3
"""Generate the classical area concept figures without matplotlib."""

from __future__ import annotations

from math import cos, pi, sin, sqrt
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTDIR = Path("figures/measure/static/concepts")

COLORS = {
    "paper": "#fbfaf7",
    "ink": "#17212b",
    "muted": "#5f6c7b",
    "blue": "#2f6fed",
    "cyan": "#2cb4c8",
    "green": "#3aa76d",
    "yellow": "#f2b84b",
    "orange": "#e68a3f",
    "red": "#e85d5d",
    "panel": "#ffffff",
}

FONT_REGULAR = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
FONT_BOLD = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_MATH = "/System/Library/Fonts/Supplemental/STIXGeneral.otf"


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size=size)


def hex_rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def center_text(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, font: ImageFont.FreeTypeFont, fill: str) -> None:
    try:
        box = draw.textbbox((0, 0), text, font=font)
        w = box[2] - box[0]
        h = box[3] - box[1]
    except AttributeError:
        w, h = draw.textsize(text, font=font)
    draw.text((xy[0] - w / 2, xy[1] - h / 2), text, font=font, fill=fill)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    try:
        box = draw.textbbox((0, 0), text, font=font)
        return box[2] - box[0], box[3] - box[1]
    except AttributeError:
        return draw.textsize(text, font=font)


def draw_symbol_with_subscript(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    symbol: str,
    sub: str,
    font: ImageFont.FreeTypeFont,
    subfont: ImageFont.FreeTypeFont,
    fill: str,
    *,
    sub_dx: float = -2,
    sub_dy: float = 28,
) -> float:
    draw.text((x, y), symbol, font=font, fill=fill)
    sym_w, _ = text_size(draw, symbol, font)
    draw.text((x + sym_w + sub_dx, y + sub_dy), sub, font=subfont, fill=fill)
    sub_w, _ = text_size(draw, sub, subfont)
    return x + sym_w + max(sub_w + sub_dx, 0)


def draw_axis_interval_label(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    primary_index: str,
    font: ImageFont.FreeTypeFont,
    subfont: ImageFont.FreeTypeFont,
    fill: str,
) -> None:
    parts = ["[", "a", ",", "b", ")"]
    part_widths = [text_size(draw, part, font)[0] for part in parts]
    digit_width = text_size(draw, primary_index, subfont)[0]
    total_width = sum(part_widths) + 2 * digit_width - 4
    x = center[0] - total_width / 2
    y = center[1] - text_size(draw, "[a,b)", font)[1] / 2

    draw.text((x, y), "[", font=font, fill=fill)
    x += part_widths[0]
    x = draw_symbol_with_subscript(draw, x, y, "a", primary_index, font, subfont, fill)
    draw.text((x, y), ",", font=font, fill=fill)
    x += part_widths[2]
    x = draw_symbol_with_subscript(draw, x, y, "b", primary_index, font, subfont, fill)
    draw.text((x, y), ")", font=font, fill=fill)


def draw_interval_block_decomposition() -> None:
    width, height = 2320, 980
    img = Image.new("RGBA", (width, height), COLORS["paper"])
    draw = ImageDraw.Draw(img)
    title = load_font(52, bold=True)
    subtitle = load_font(28)
    section = load_font(30, bold=True)
    note = load_font(22)
    formula = load_font(28, bold=True)
    formula_sub = load_font(18)
    block_label = load_font(26, bold=True)
    block_sub = load_font(18)

    draw.text((60, 34), "区間塊", font=title, fill=COLORS["ink"])
    draw.text((60, 106), "同じ集合 E でも, 長方形の取り方や細分の仕方は一通りではない", font=subtitle, fill=COLORS["muted"])

    panels = [
        (55, 210, 455, 770),
        (620, 210, 1020, 770),
        (1185, 210, 1585, 770),
        (1750, 210, 2150, 770),
    ]
    fill_color = hex_rgba(COLORS["cyan"], 78)

    # A rectilinear shape that has two short rectangle decompositions.
    x_edges = [0.0, 0.20, 0.45, 0.72, 1.0]
    y_edges = [0.0, 0.26, 0.58, 1.0]
    filled_cells = {
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1), (3, 1),
        (1, 2), (2, 2), (3, 2),
    }

    def to_px(panel: tuple[int, int, int, int], x: float, y: float) -> tuple[float, float]:
        left, top, right, bottom = panel
        return (left + x * (right - left), bottom - y * (bottom - top))

    def cell_rect(panel: tuple[int, int, int, int], ix: int, iy: int) -> tuple[float, float, float, float]:
        x0, y1 = to_px(panel, x_edges[ix], y_edges[iy])
        x1, y0 = to_px(panel, x_edges[ix + 1], y_edges[iy + 1])
        return x0, y0, x1, y1

    def draw_base_shape(panel: tuple[int, int, int, int]) -> None:
        for ix, iy in filled_cells:
            draw.rectangle(cell_rect(panel, ix, iy), fill=fill_color)

    def draw_outer_boundary(panel: tuple[int, int, int, int], width_px: int = 4) -> None:
        for ix, iy in filled_cells:
            x0, y0, x1, y1 = cell_rect(panel, ix, iy)
            if (ix - 1, iy) not in filled_cells:
                draw.line((x0, y0, x0, y1), fill=COLORS["ink"], width=width_px)
            if (ix + 1, iy) not in filled_cells:
                draw.line((x1, y0, x1, y1), fill=COLORS["ink"], width=width_px)
            if (ix, iy - 1) not in filled_cells:
                draw.line((x0, y1, x1, y1), fill=COLORS["ink"], width=width_px)
            if (ix, iy + 1) not in filled_cells:
                draw.line((x0, y0, x1, y0), fill=COLORS["ink"], width=width_px)

    def draw_partition_lines(panel: tuple[int, int, int, int], segments: list[tuple[tuple[float, float], tuple[float, float]]]) -> None:
        for start, end in segments:
            x0, y0 = to_px(panel, start[0], start[1])
            x1, y1 = to_px(panel, end[0], end[1])
            draw.line((x0, y0, x1, y1), fill=COLORS["blue"], width=3)

    def draw_panel_label(panel: tuple[int, int, int, int], title_text: str) -> None:
        cx = (panel[0] + panel[2]) / 2
        center_text(draw, (cx, 182), title_text, section, COLORS["ink"])

    def draw_centered_symbol_with_subscript(
        center: tuple[float, float],
        symbol: str,
        sub: str,
        font: ImageFont.FreeTypeFont,
        subfont: ImageFont.FreeTypeFont,
        fill: str,
    ) -> None:
        sym_w, sym_h = text_size(draw, symbol, font)
        sub_w, _ = text_size(draw, sub, subfont)
        total_w = sym_w + sub_w - 2
        x = center[0] - total_w / 2
        y = center[1] - sym_h / 2
        draw_symbol_with_subscript(draw, x, y, symbol, sub, font, subfont, fill, sub_dx=-2, sub_dy=20)

    def term_width(letter: str, index: str) -> float:
        prefix_w, _ = text_size(draw, "m(", formula)
        sym_w, _ = text_size(draw, letter, formula)
        sub_w, _ = text_size(draw, index, formula_sub)
        suffix_w, _ = text_size(draw, ")", formula)
        return prefix_w + sym_w + sub_w - 2 + suffix_w

    def draw_measure_term(x: float, y: float, letter: str, index: str, fill: str) -> float:
        draw.text((x, y), "m(", font=formula, fill=fill)
        x += text_size(draw, "m(", formula)[0]
        x = draw_symbol_with_subscript(draw, x, y, letter, index, formula, formula_sub, fill, sub_dx=-2, sub_dy=22)
        draw.text((x, y), ")", font=formula, fill=fill)
        x += text_size(draw, ")", formula)[0]
        return x

    def draw_decomposition_formula(center: tuple[float, float], prefix: str, letter: str, indices: list[str], *, ellipsis: bool = False) -> None:
        pieces: list[tuple[str, str | None]] = [(prefix, None)]
        if ellipsis:
            pieces.append((letter, indices[0]))
            pieces.append(("+ ... +", None))
            pieces.append((letter, indices[-1]))
        else:
            for idx, index in enumerate(indices):
                pieces.append((letter, index))
                if idx < len(indices) - 1:
                    pieces.append(("+", None))

        widths: list[float] = []
        for text, sub in pieces:
            if sub is None:
                widths.append(text_size(draw, text, formula)[0])
            else:
                sym_w, _ = text_size(draw, text, formula)
                sub_w, _ = text_size(draw, sub, formula_sub)
                widths.append(sym_w + sub_w - 2)
        total_w = sum(widths) + 10 * (len(widths) - 1)
        x = center[0] - total_w / 2
        y = center[1] - text_size(draw, prefix, formula)[1] / 2

        for (text, sub), width in zip(pieces, widths):
            if sub is None:
                draw.text((x, y), text, font=formula, fill=COLORS["blue"])
            else:
                draw_symbol_with_subscript(draw, x, y, text, sub, formula, formula_sub, COLORS["blue"], sub_dx=-2, sub_dy=22)
            x += width + 10

    def draw_measure_equals_sum(center: tuple[float, float], prefix: str, groups: list[tuple[str, list[str], bool]]) -> None:
        prefix_w, _ = text_size(draw, prefix, formula)
        eq_w, _ = text_size(draw, "=", formula)
        plus_w, _ = text_size(draw, "+", formula)
        total_w = prefix_w + 14
        for gidx, (letter, terms, ellipsis) in enumerate(groups):
            if ellipsis:
                total_w += term_width(letter, terms[0]) + text_size(draw, "+ ... +", formula)[0] + term_width(letter, terms[-1]) + 20
            else:
                total_w += sum(term_width(letter, idx) for idx in terms) + plus_w * (len(terms) - 1) + 14 * (len(terms) - 1)
            if gidx < len(groups) - 1:
                total_w += 24 + eq_w + 24
        x = center[0] - total_w / 2
        y = center[1] - text_size(draw, prefix, formula)[1] / 2

        draw.text((x, y), prefix, font=formula, fill=COLORS["blue"])
        x += prefix_w + 14
        for gidx, (letter, terms, ellipsis) in enumerate(groups):
            if ellipsis:
                x = draw_measure_term(x, y, letter, terms[0], COLORS["blue"])
                draw.text((x + 6, y), "+ ... +", font=formula, fill=COLORS["blue"])
                x += text_size(draw, "+ ... +", formula)[0] + 10
                x = draw_measure_term(x, y, letter, terms[-1], COLORS["blue"])
            else:
                for idx, index in enumerate(terms):
                    x = draw_measure_term(x, y, letter, index, COLORS["blue"])
                    if idx < len(terms) - 1:
                        draw.text((x + 6, y), "+", font=formula, fill=COLORS["blue"])
                        x += plus_w + 14
            if gidx < len(groups) - 1:
                draw.text((x + 10, y), "=", font=formula, fill=COLORS["blue"])
                x += eq_w + 34

    def draw_set_equals_sum(center: tuple[float, float], groups: list[tuple[str, list[str], bool]]) -> None:
        prefix_w, _ = text_size(draw, "E =", formula)
        eq_w, _ = text_size(draw, "=", formula)
        plus_w, _ = text_size(draw, "+", formula)
        total_w = prefix_w + 14
        for gidx, (letter, terms, ellipsis) in enumerate(groups):
            if ellipsis:
                sym_w, _ = text_size(draw, letter, formula)
                total_w += (sym_w + text_size(draw, terms[0], formula_sub)[0] - 2)
                total_w += text_size(draw, "+ ... +", formula)[0]
                total_w += (sym_w + text_size(draw, terms[-1], formula_sub)[0] - 2) + 20
            else:
                for idx in terms:
                    sym_w, _ = text_size(draw, letter, formula)
                    total_w += sym_w + text_size(draw, idx, formula_sub)[0] - 2
                total_w += plus_w * (len(terms) - 1) + 14 * (len(terms) - 1)
            if gidx < len(groups) - 1:
                total_w += 24 + eq_w + 24
        x = center[0] - total_w / 2
        y = center[1] - text_size(draw, "E =", formula)[1] / 2

        draw.text((x, y), "E =", font=formula, fill=COLORS["blue"])
        x += prefix_w + 14
        for gidx, (letter, terms, ellipsis) in enumerate(groups):
            if ellipsis:
                x = draw_symbol_with_subscript(draw, x, y, letter, terms[0], formula, formula_sub, COLORS["blue"], sub_dx=-2, sub_dy=22)
                draw.text((x + 6, y), "+ ... +", font=formula, fill=COLORS["blue"])
                x += text_size(draw, "+ ... +", formula)[0] + 10
                x = draw_symbol_with_subscript(draw, x, y, letter, terms[-1], formula, formula_sub, COLORS["blue"], sub_dx=-2, sub_dy=22)
            else:
                for idx, index in enumerate(terms):
                    x = draw_symbol_with_subscript(draw, x, y, letter, index, formula, formula_sub, COLORS["blue"], sub_dx=-2, sub_dy=22)
                    if idx < len(terms) - 1:
                        draw.text((x + 6, y), "+", font=formula, fill=COLORS["blue"])
                        x += plus_w + 14
            if gidx < len(groups) - 1:
                draw.text((x + 10, y), "=", font=formula, fill=COLORS["blue"])
                x += eq_w + 34

    coarse_segments = [
        ((0.0, 0.26), (0.72, 0.26)),
        ((0.20, 0.58), (1.0, 0.58)),
    ]
    alt_segments = [
        ((0.20, 0.0), (0.20, 0.58)),
        ((0.45, 0.0), (0.45, 1.0)),
        ((0.72, 0.26), (0.72, 1.0)),
    ]
    common_segments = [
        ((0.0, 0.26), (0.72, 0.26)),
        ((0.20, 0.58), (1.0, 0.58)),
        ((0.20, 0.0), (0.20, 0.58)),
        ((0.45, 0.0), (0.45, 1.0)),
        ((0.72, 0.26), (0.72, 1.0)),
    ]

    for panel in panels:
        draw.rectangle(panel, fill=COLORS["panel"], outline="#d7dde6", width=2)
        draw_base_shape(panel)
        draw_outer_boundary(panel)

    draw_panel_label(panels[0], "集合 E")
    center_text(draw, ((panels[0][0] + panels[0][2]) / 2, (panels[0][1] + panels[0][3]) / 2), "E", load_font(44, bold=True), COLORS["ink"])
    center_text(draw, ((panels[0][0] + panels[0][2]) / 2, 814), "同じ輪郭を持つ区間塊", note, COLORS["muted"])

    draw_partition_lines(panels[1], coarse_segments)
    draw_panel_label(panels[1], "分割 1")
    coarse_centers = [
        ((0.36, 0.13), "I", "1"),
        ((0.50, 0.42), "I", "2"),
        ((0.60, 0.79), "I", "3"),
    ]
    for (cx, cy), sym, sub in coarse_centers:
        px, py = to_px(panels[1], cx, cy)
        draw_centered_symbol_with_subscript((px, py), sym, sub, block_label, block_sub, COLORS["ink"])
    center_text(draw, ((panels[1][0] + panels[1][2]) / 2, 842), "横方向にまとめた長方形の直和", note, COLORS["muted"])

    draw_partition_lines(panels[2], alt_segments)
    draw_panel_label(panels[2], "分割 2")
    fine_centers = [
        ((0.10, 0.29), "J", "1"),
        ((0.32, 0.50), "J", "2"),
        ((0.59, 0.50), "J", "3"),
        ((0.86, 0.66), "J", "4"),
    ]
    for (cx, cy), sym, sub in fine_centers:
        px, py = to_px(panels[2], cx, cy)
        draw_centered_symbol_with_subscript((px, py), sym, sub, block_label, block_sub, COLORS["ink"])
    center_text(draw, ((panels[2][0] + panels[2][2]) / 2, 842), "縦方向にまとめた長方形の直和", note, COLORS["muted"])

    draw_partition_lines(panels[3], common_segments)
    draw_panel_label(panels[3], "分割 3")
    common_label = load_font(20, bold=True)
    common_sub = load_font(14)
    common_centers = [
        ((0.10, 0.13), "K", "1"),
        ((0.32, 0.13), "K", "2"),
        ((0.58, 0.13), "K", "3"),
        ((0.10, 0.42), "K", "4"),
        ((0.32, 0.42), "K", "5"),
        ((0.58, 0.42), "K", "6"),
        ((0.86, 0.42), "K", "7"),
        ((0.32, 0.79), "K", "8"),
        ((0.58, 0.79), "K", "9"),
        ((0.86, 0.79), "K", "10"),
    ]
    for (cx, cy), sym, sub in common_centers:
        px, py = to_px(panels[3], cx, cy)
        draw_centered_symbol_with_subscript((px, py), sym, sub, common_label, common_sub, COLORS["ink"])
    center_text(draw, ((panels[3][0] + panels[3][2]) / 2, 842), "分割 1 と 2 の共通細分", note, COLORS["muted"])

    draw_set_equals_sum((width / 2, 894), [("I", ["1", "2", "3"], False), ("J", ["1", "2", "3", "4"], False), ("K", ["1", "10"], True)])
    draw_measure_equals_sum((width / 2, 932), "m(E) =", [("I", ["1", "2", "3"], False), ("J", ["1", "2", "3", "4"], False), ("K", ["1", "10"], True)])

    OUTDIR.mkdir(parents=True, exist_ok=True)
    img.save(OUTDIR / "interval_block_decomposition.png")


def dashed_line(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], fill: str, width: int, dash: int = 12, gap: int = 8) -> None:
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0
    length = max((dx * dx + dy * dy) ** 0.5, 1.0)
    ux = dx / length
    uy = dy / length
    pos = 0.0
    while pos < length:
        seg_end = min(pos + dash, length)
        draw.line((x0 + ux * pos, y0 + uy * pos, x0 + ux * seg_end, y0 + uy * seg_end), fill=fill, width=width)
        pos += dash + gap


def regular_polygon(center: tuple[float, float], radius: float, n: int, *, start_angle: float = -pi / 2) -> list[tuple[float, float]]:
    return [
        (
            center[0] + radius * cos(start_angle + 2 * pi * k / n),
            center[1] + radius * sin(start_angle + 2 * pi * k / n),
        )
        for k in range(n)
    ]


def polygon_area(n: int) -> float:
    return 0.5 * n * sin(2 * pi / n)


def rectangle_area(strip_count: int) -> float:
    edges = [-1 + 2 * i / strip_count for i in range(strip_count + 1)]
    total = 0.0
    for left, right in zip(edges[:-1], edges[1:]):
        height = 2 * sqrt(max(0.0, 1 - max(left * left, right * right)))
        total += (right - left) * height
    return total


def draw_number_line(draw: ImageDraw.ImageDraw, x0: int, x1: int, y: int, values: list[float], labels: list[str], limit_label: str, colors: list[str]) -> None:
    xmin = values[0] - 0.18
    xmax = pi + 0.16
    draw.line((x0, y, x1, y), fill=COLORS["ink"], width=4)

    def map_x(value: float) -> float:
        return x0 + (value - xmin) / (xmax - xmin) * (x1 - x0)

    regular = load_font(22)
    bold = load_font(22, bold=True)
    last_px: float | None = None
    for idx, (value, label, color) in enumerate(zip(values, labels, colors)):
        px = map_x(value)
        draw.line((px, y - 18, px, y + 18), fill=color, width=5)
        draw.ellipse((px - 6, y - 6, px + 6, y + 6), fill=color, outline=COLORS["ink"], width=1)
        label_y = y - 42
        if last_px is not None and px - last_px < 86:
            label_y -= 26 if idx % 2 else 0
        center_text(draw, (px, label_y), label, regular, COLORS["ink"])
        last_px = px

    for tick, label in [(xmin, "0"), (pi, limit_label)]:
        px = map_x(tick)
        draw.line((px, y - 12, px, y + 12), fill=COLORS["ink"], width=3)
        center_text(draw, (px, y + 78), label, regular, COLORS["ink"])

    px = map_x(pi)
    dashed_line(draw, (px, y - 36), (px, y + 56), COLORS["red"], 3)
    center_text(draw, ((x0 + x1) / 2, y + 126), "段階ごとの近似面積が同じ極限へ集まる", bold, COLORS["muted"])


def draw_half_open_interval_volume() -> None:
    width, height = 1404, 910
    img = Image.new("RGBA", (width, height), COLORS["paper"])
    draw = ImageDraw.Draw(img)
    title = load_font(52, bold=True)
    subtitle = load_font(28)
    regular = load_font(36)
    formula = ImageFont.truetype(FONT_MATH, size=46)
    formula_small = ImageFont.truetype(FONT_MATH, size=24)
    legend = load_font(32, bold=True)

    draw.text((60, 36), "半開区間と体積", font=title, fill=COLORS["ink"])
    draw.text((60, 112), "境界の重複を避けて基本図形を分割する", font=subtitle, fill=COLORS["muted"])

    x0, y0, w, h = 140, 250, 790, 420
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overdraw = ImageDraw.Draw(overlay)
    overdraw.rectangle((x0, y0, x0 + w, y0 + h), fill=hex_rgba(COLORS["cyan"], 72), outline=COLORS["ink"], width=4)
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    draw.line((x0, y0 + h, x0 + w, y0 + h), fill=COLORS["ink"], width=5)
    draw.line((x0, y0, x0, y0 + h), fill=COLORS["ink"], width=5)
    dashed_line(draw, (x0 + w, y0), (x0 + w, y0 + h), COLORS["red"], 5)
    dashed_line(draw, (x0, y0), (x0 + w, y0), COLORS["red"], 5)

    def draw_formula(center_x: float, center_y: float) -> None:
        main_parts = ["m(I)=", "∏", "(", "b", "-", "a", ")"]
        main_widths = [text_size(draw, part, formula)[0] for part in main_parts]
        sub_k_width = text_size(draw, "k", formula_small)[0]
        under_width = text_size(draw, "k=1", formula_small)[0]
        over_width = text_size(draw, "N", formula_small)[0]
        total_width = (
            main_widths[0]
            + 10
            + main_widths[1]
            + 10
            + main_widths[2]
            + main_widths[3]
            + sub_k_width
            + 8
            + main_widths[4]
            + 8
            + main_widths[5]
            + sub_k_width
            + main_widths[6]
        )
        x = center_x - total_width / 2
        y = center_y - text_size(draw, "m(I)=∏(b-a)", formula)[1] / 2

        draw.text((x, y), "m(I)=", font=formula, fill=COLORS["ink"])
        x += main_widths[0] + 10

        prod_x = x
        draw.text((prod_x, y), "∏", font=formula, fill=COLORS["ink"])
        prod_w = main_widths[1]
        draw.text((prod_x + (prod_w - over_width) / 2, y - 14), "N", font=formula_small, fill=COLORS["ink"])
        draw.text((prod_x + (prod_w - under_width) / 2, y + 48), "k=1", font=formula_small, fill=COLORS["ink"])
        x += prod_w + 10

        draw.text((x, y), "(", font=formula, fill=COLORS["ink"])
        x += main_widths[2]

        x = draw_symbol_with_subscript(draw, x, y, "b", "k", formula, formula_small, COLORS["ink"], sub_dy=30)
        x += 8

        draw.text((x, y), "-", font=formula, fill=COLORS["ink"])
        x += main_widths[4] + 8

        x = draw_symbol_with_subscript(draw, x, y, "a", "k", formula, formula_small, COLORS["ink"], sub_dy=30)

        draw.text((x, y), ")", font=formula, fill=COLORS["ink"])

    draw.rectangle((x0 + 215, y0 + 165, x0 + w - 215, y0 + h - 165), fill=hex_rgba(COLORS["panel"], 232))
    draw_formula(x0 + w / 2, y0 + h / 2)

    axis_sub = load_font(24)
    draw_axis_interval_label(draw, (x0 + w / 2, y0 + h + 56), "1", regular, axis_sub, COLORS["ink"])
    draw_axis_interval_label(draw, (x0 - 62, y0 + h / 2), "2", regular, axis_sub, COLORS["ink"])

    draw.text((1015, 350), "含む境界", font=legend, fill=COLORS["ink"])
    draw.line((1000, 410, 1160, 410), fill=COLORS["ink"], width=5)
    draw.text((1015, 505), "含まない境界", font=legend, fill=COLORS["red"])
    dashed_line(draw, (1000, 565), (1160, 565), COLORS["red"], 5)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    img.save(OUTDIR / "half_open_interval_volume.png")


def draw_classical_area_coverings() -> None:
    width, height = 1800, 1160
    img = Image.new("RGBA", (width, height), COLORS["paper"])
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    odraw = ImageDraw.Draw(overlay)

    title = load_font(56, bold=True)
    subtitle = load_font(30)
    section = load_font(34, bold=True)
    note = load_font(24)
    small = load_font(22)

    draw.text((76, 42), "古典的面積概念", font=title, fill=COLORS["ink"])
    draw.text((76, 122), "有限個の基本図形を増やし, 面積近似が極限へ近づく", font=subtitle, fill=COLORS["muted"])

    left_center = (470, 470)
    right_center = (1325, 470)
    radius = 235

    for center in [left_center, right_center]:
        odraw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill=hex_rgba("#f7fbff", 255), outline=COLORS["blue"], width=5)

    base_poly = regular_polygon(left_center, radius, 4, start_angle=-pi / 4)
    odraw.polygon(base_poly, fill=hex_rgba(COLORS["cyan"], 155), outline=COLORS["ink"])
    prev = regular_polygon(left_center, radius, 4, start_angle=-pi / 4)
    prev_n = 4
    for next_n, color, alpha in [(8, COLORS["yellow"], 190), (16, COLORS["orange"], 150)]:
        nxt = regular_polygon(left_center, radius, next_n, start_angle=-pi / 4)
        # Add one outward isosceles triangle on each edge of the previous regular polygon.
        # The apex is the midpoint vertex of the refined regular polygon on the same circumcircle.
        for k in range(prev_n):
            tri = [
                prev[k],
                prev[(k + 1) % prev_n],
                nxt[2 * k + 1],
            ]
            odraw.polygon(tri, fill=hex_rgba(color, alpha), outline=COLORS["ink"])
        prev = nxt
        prev_n = next_n

    s = 1 / sqrt(2)

    def draw_normalized_rect(x0: float, y0: float, x1: float, y1: float, color: str, alpha: int) -> None:
        odraw.rectangle(
            (
                right_center[0] + radius * x0,
                right_center[1] - radius * y1,
                right_center[0] + radius * x1,
                right_center[1] - radius * y0,
            ),
            fill=hex_rgba(color, alpha),
            outline=COLORS["ink"],
            width=2,
        )

    def cap_height(a: float, b: float) -> float:
        return sqrt(max(0.0, 1 - max(a * a, b * b)))

    draw_normalized_rect(-s, -s, s, s, COLORS["cyan"], 160)

    a1 = 0.34
    top1 = cap_height(-a1, a1)
    for y0, y1 in [(s, top1), (-top1, -s)]:
        draw_normalized_rect(-a1, y0, a1, y1, COLORS["yellow"], 185)
    for x0, x1 in [(s, top1), (-top1, -s)]:
        draw_normalized_rect(x0, -a1, x1, a1, COLORS["yellow"], 185)

    a2 = 0.57
    side_intervals = [(-a2, -a1), (a1, a2)]
    for left, right in side_intervals:
        top = cap_height(left, right)
        draw_normalized_rect(left, s, right, top, COLORS["orange"], 145)
        draw_normalized_rect(left, -top, right, -s, COLORS["orange"], 145)
        draw_normalized_rect(s, left, top, right, COLORS["orange"], 145)
        draw_normalized_rect(-top, left, -s, right, COLORS["orange"], 145)

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    draw.ellipse((left_center[0] - radius, left_center[1] - radius, left_center[0] + radius, left_center[1] + radius), outline=COLORS["blue"], width=5)
    draw.ellipse((right_center[0] - radius, right_center[1] - radius, right_center[0] + radius, right_center[1] + radius), outline=COLORS["blue"], width=5)

    center_text(draw, (left_center[0], 235), "円板を多角形で近似", section, COLORS["ink"])
    center_text(draw, (right_center[0], 235), "円板を長方形で近似", section, COLORS["ink"])
    center_text(draw, (left_center[0], 750), "正方形の各辺に二等辺三角形を足して 8 角形へ進む", note, COLORS["muted"])
    center_text(draw, (right_center[0], 750), "正方形の外側の 4 つの隙間へ長方形を順に追加する", note, COLORS["muted"])

    poly_values = [polygon_area(n) for n in [4, 8, 16]]
    rect_values = [
        (2 * s) * (2 * s),
        (2 * s) * (2 * s) + 4 * (2 * a1) * (top1 - s),
        (2 * s) * (2 * s) + 4 * (2 * a1) * (top1 - s) + 8 * (a2 - a1) * (cap_height(a1, a2) - s),
    ]
    line_colors = [COLORS["cyan"], COLORS["yellow"], COLORS["orange"]]
    draw_number_line(draw, 120, 815, 860, poly_values, ["P1", "P2", "P3"], "πr²", line_colors)
    draw_number_line(draw, 985, 1680, 860, rect_values, ["R1", "R2", "R3"], "πr²", line_colors)

    center_text(draw, (left_center[0], 1026), "正 n 角形の列", small, COLORS["ink"])
    center_text(draw, (right_center[0], 1026), "長方形近似の列", small, COLORS["ink"])

    OUTDIR.mkdir(parents=True, exist_ok=True)
    img.save(OUTDIR / "classical_area_coverings.png")


def main() -> None:
    draw_half_open_interval_volume()
    draw_interval_block_decomposition()
    draw_classical_area_coverings()
    print(f"Generated figures in {OUTDIR}")


if __name__ == "__main__":
    main()
