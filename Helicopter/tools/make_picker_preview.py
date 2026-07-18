"""Create the picker PNG from a Pixel Watch 3 screen capture.

Wear OS can draw an ongoing-activity icon over the bottom of a live watch-face
capture. The dial is rotationally symmetric outside radius 180, so this script
repairs only that small outer sector from the equivalent 3-o'clock sector and
then scales the physical 456 px capture to the 450 px WFF design size.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    image = Image.open(args.input).convert("RGBA")
    if image.width != image.height:
        raise ValueError("Expected a square watch screenshot")

    size = image.width
    center = size / 2

    # Rotating clockwise maps the unobstructed 3-o'clock rail onto 6 o'clock.
    repaired_source = image.transpose(Image.Transpose.ROTATE_270)
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice((0, 0, size - 1, size - 1), 81, 99, fill=255)

    inner_radius = size * (180 / 456)
    draw.ellipse(
        (
            center - inner_radius,
            center - inner_radius,
            center + inner_radius,
            center + inner_radius,
        ),
        fill=0,
    )

    image.paste(repaired_source, (0, 0), mask)
    image = image.resize((450, 450), Image.Resampling.LANCZOS)

    # Android picker previews are most interoperable as ordinary RGBA PNGs.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
