#!/usr/bin/env python3
"""Prepend each GIF's final frame so PDF export shows the completed state."""

from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path
import tempfile
import sys
from typing import NamedTuple

from PIL import Image, ImageChops, ImageSequence


DEFAULT_TARGET = Path("figures/measure/animations")
MARKER = b"prepend-gif-final-frame-v1"


class GifBlocks(NamedTuple):
    header_end: int
    first_frame_start: int
    first_image_start: int
    trailer_start: int
    global_color_table: bytes


def resolve_gif_paths(paths: list[Path]) -> list[Path]:
    gif_paths: list[Path] = []
    for path in paths:
        if path.is_dir():
            gif_paths.extend(sorted(path.rglob("*.gif")))
        elif path.is_file() and path.suffix.lower() == ".gif":
            gif_paths.append(path)
        else:
            raise FileNotFoundError(f"GIF path not found: {path}")
    return sorted(set(gif_paths))


def frame_to_rgba(frame: Image.Image) -> Image.Image:
    return frame.copy().convert("RGBA")


def frames_match(left: Image.Image, right: Image.Image) -> bool:
    if left.size != right.size:
        return False
    return ImageChops.difference(left, right).getbbox() is None


def color_table_size(packed: int) -> int:
    return 3 * (2 ** ((packed & 0b00000111) + 1))


def sub_blocks_end(data: bytes, start: int) -> int:
    pos = start
    while True:
        if pos >= len(data):
            raise ValueError("Unexpected end of GIF sub-blocks")
        size = data[pos]
        pos += 1
        if size == 0:
            return pos
        pos += size


def extension_end(data: bytes, start: int) -> int:
    if start + 2 > len(data) or data[start] != 0x21:
        raise ValueError("Expected GIF extension block")
    return sub_blocks_end(data, start + 2)


def image_end(data: bytes, start: int) -> int:
    if start + 10 > len(data) or data[start] != 0x2C:
        raise ValueError("Expected GIF image descriptor")
    packed = data[start + 9]
    pos = start + 10
    if packed & 0b10000000:
        pos += color_table_size(packed)
    pos += 1
    return sub_blocks_end(data, pos)


def parse_gif_blocks(data: bytes) -> GifBlocks:
    if data[:6] not in (b"GIF87a", b"GIF89a"):
        raise ValueError("Not a GIF file")
    if len(data) < 14:
        raise ValueError("GIF file is too short")

    pos = 13
    global_color_table = b""
    packed = data[10]
    if packed & 0b10000000:
        table_size = color_table_size(packed)
        global_color_table = data[pos : pos + table_size]
        pos += table_size
    header_end = pos

    first_frame_start = None
    first_image_start = None
    pending_graphic_control = None

    while pos < len(data):
        block_type = data[pos]
        if block_type == 0x3B:
            break
        if block_type == 0x21:
            label = data[pos + 1]
            block_end = extension_end(data, pos)
            if label == 0xF9:
                pending_graphic_control = pos
            pos = block_end
            continue
        if block_type == 0x2C:
            first_frame_start = pending_graphic_control if pending_graphic_control is not None else pos
            first_image_start = pos
            break
        raise ValueError(f"Unsupported GIF block 0x{block_type:02x} at byte {pos}")

    if first_frame_start is None or first_image_start is None:
        raise ValueError("No image frame found in GIF")

    pos = first_image_start
    while pos < len(data):
        block_type = data[pos]
        if block_type == 0x3B:
            return GifBlocks(header_end, first_frame_start, first_image_start, pos, global_color_table)
        if block_type == 0x21:
            pos = extension_end(data, pos)
            continue
        if block_type == 0x2C:
            pos = image_end(data, pos)
            continue
        raise ValueError(f"Unsupported GIF block 0x{block_type:02x} at byte {pos}")

    raise ValueError("GIF trailer not found")


def marker_comment() -> bytes:
    chunks = []
    for start in range(0, len(MARKER), 255):
        chunk = MARKER[start : start + 255]
        chunks.append(bytes([len(chunk)]) + chunk)
    return b"\x21\xFE" + b"".join(chunks) + b"\x00"


def has_marker(data: bytes) -> bool:
    return MARKER in data


def read_gif(path: Path):
    with Image.open(path) as source:
        default_duration = int(source.info.get("duration", 100))
        frames = []
        durations = []

        for frame in ImageSequence.Iterator(source):
            frames.append(frame.copy())
            durations.append(int(frame.info.get("duration", default_duration)))

    if not frames:
        raise ValueError(f"No frames found: {path}")

    return frames, durations


def frame_block_from_single_frame_gif(frame: Image.Image, duration_ms: int) -> bytes:
    buffer = BytesIO()
    frame.save(buffer, format="GIF", save_all=True, duration=duration_ms, disposal=2, optimize=True)
    data = buffer.getvalue()
    blocks = parse_gif_blocks(data)
    frame_block = bytearray(data[blocks.first_frame_start : blocks.trailer_start])
    image_offset = blocks.first_image_start - blocks.first_frame_start

    if blocks.global_color_table and not frame_block[image_offset + 9] & 0b10000000:
        color_count = len(blocks.global_color_table) // 3
        table_bits = color_count.bit_length() - 2
        frame_block[image_offset + 9] = (frame_block[image_offset + 9] | 0b10000000) & 0b11111000 | table_bits
        frame_block[image_offset + 10 : image_offset + 10] = blocks.global_color_table

    return bytes(frame_block)


def save_gif(path: Path, data: bytes, blocks: GifBlocks, frame_block: bytes) -> None:
    stat = path.stat()
    updated_data = data[: blocks.first_frame_start] + marker_comment() + frame_block + data[blocks.first_frame_start :]

    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".gif", delete=False) as temp_file:
        temp_path = Path(temp_file.name)

    try:
        temp_path.write_bytes(updated_data)
        temp_path.chmod(stat.st_mode)
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def prepend_last_frame(path: Path, *, dry_run: bool = False) -> str:
    data = path.read_bytes()
    blocks = parse_gif_blocks(data)
    frames, durations = read_gif(path)
    if has_marker(data) or frames_match(frame_to_rgba(frames[0]), frame_to_rgba(frames[-1])):
        return "skipped"

    frame_block = frame_block_from_single_frame_gif(frames[-1], durations[-1])

    if not dry_run:
        save_gif(path, data, blocks, frame_block)

    return "updated"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepend each GIF's final frame so static PDF export captures the completed animation state."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[DEFAULT_TARGET],
        help=f"GIF files or directories to process. Defaults to {DEFAULT_TARGET}.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report changes without modifying GIF files.")
    argv = sys.argv[1:]
    if argv and argv[0] == "--":
        argv = argv[1:]
    args = parser.parse_args(argv)

    gif_paths = resolve_gif_paths(args.paths)
    counts = {"updated": 0, "skipped": 0}

    for gif_path in gif_paths:
        result = prepend_last_frame(gif_path, dry_run=args.dry_run)
        counts[result] += 1
        print(f"{result}: {gif_path}")

    mode = "dry-run" if args.dry_run else "write"
    print(f"{mode}: {counts['updated']} updated, {counts['skipped']} skipped, {len(gif_paths)} total")


if __name__ == "__main__":
    main()
