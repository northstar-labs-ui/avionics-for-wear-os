"""Build a one-glyph TrueType font from the licensed aircraft vector.

The watch face uses this font to keep the supplied SVG artwork vector-native.
WFF v1 supports custom fonts in ``res/font`` but cannot render an arbitrary SVG
as a fixed ``PartImage`` without rasterizing it.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path


ANDROID_NS = "http://schemas.android.com/apk/res/android"
AIRCRAFT_CODEPOINT = ord("A")
UNITS_PER_EM = 1000

# The supplied silhouette is 3000 units wide. Keep a small side margin and map
# its visual nose/propeller hub to the exact center of the glyph. With a
# 170-unit PartText box this places the separate propeller at (225, 225).
SOURCE_WIDTH = 3000.0
SOURCE_HUB_Y = 1607.27
SIDE_MARGIN = 10.0
SCALE = (UNITS_PER_EM - (2.0 * SIDE_MARGIN)) / SOURCE_WIDTH
GLYPH_HUB_Y = 500.0
ASCENT = 1000
DESCENT = 0


def empty_glyph():
    return TTGlyphPen(None).glyph()


def aircraft_glyph(path_data: str):
    target = TTGlyphPen(None)
    quadratic = Cu2QuPen(target, max_err=0.5, reverse_direction=False)
    transformed = TransformPen(
        quadratic,
        (
            SCALE,
            0.0,
            0.0,
            -SCALE,
            SIDE_MARGIN,
            GLYPH_HUB_Y + (SOURCE_HUB_Y * SCALE),
        ),
    )
    parse_path(path_data, transformed)
    return target.glyph()


def read_vector_path(vector_path: Path) -> str:
    root = ET.parse(vector_path).getroot()
    path = next(
        (element for element in root.iter() if element.tag.rsplit("}", 1)[-1] == "path"),
        None,
    )
    if path is None:
        raise ValueError(f"No <path> found in {vector_path}")
    path_data = path.get("d") or path.get(f"{{{ANDROID_NS}}}pathData")
    if not path_data:
        raise ValueError(f"No SVG d or android:pathData found in {vector_path}")
    return path_data


def build_font(vector_path: Path, output_path: Path) -> None:
    glyph_order = [".notdef", "space", "A"]
    glyphs = {
        ".notdef": empty_glyph(),
        "space": empty_glyph(),
        "A": aircraft_glyph(read_vector_path(vector_path)),
    }

    font = FontBuilder(UNITS_PER_EM, isTTF=True)
    font.setupGlyphOrder(glyph_order)
    font.setupCharacterMap({0x20: "space", AIRCRAFT_CODEPOINT: "A"})
    font.setupGlyf(glyphs)
    aircraft_lsb = font.font["glyf"]["A"].xMin
    font.setupHorizontalMetrics(
        {
            ".notdef": (UNITS_PER_EM, 0),
            "space": (500, 0),
            "A": (UNITS_PER_EM, aircraft_lsb),
        }
    )
    font.setupHorizontalHeader(ascent=ASCENT, descent=-DESCENT, lineGap=0)
    font.setupNameTable(
        {
            "familyName": "Turn Coordinator Aircraft",
            "styleName": "Regular",
            "uniqueFontIdentifier": "Turn Coordinator Aircraft 1.0",
            "fullName": "Turn Coordinator Aircraft Regular",
            "psName": "TurnCoordinatorAircraft-Regular",
            "version": "Version 1.0",
        }
    )
    font.setupOS2(
        sTypoAscender=ASCENT,
        sTypoDescender=-DESCENT,
        sTypoLineGap=0,
        usWinAscent=ASCENT,
        usWinDescent=DESCENT,
        usWeightClass=400,
        usWidthClass=5,
        fsSelection=0x40,
        sxHeight=0,
        sCapHeight=1000,
    )
    font.setupPost(keepGlyphNames=False)
    font.setupMaxp()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    font.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("vector", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build_font(args.vector, args.output)


if __name__ == "__main__":
    main()
