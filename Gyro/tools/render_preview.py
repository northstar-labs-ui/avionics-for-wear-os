"""Render the WFF/vector sources into the sole permitted picker preview PNG source.

This script intentionally emits SVG. A headless browser rasterizes that SVG to
``res/drawable/preview.png`` so the shipped watch-face artwork remains vector.
"""

from __future__ import annotations

import html
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ANDROID_NS = "http://schemas.android.com/apk/res/android"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RES_DIR = PROJECT_ROOT / "watchface" / "src" / "main" / "res"
WATCHFACE_XML = RES_DIR / "raw" / "watchface.xml"
DRAWABLE_DIR = RES_DIR / "drawable"


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def android_attr(element: ET.Element, name: str, default: str | None = None) -> str | None:
    return element.get(f"{{{ANDROID_NS}}}{name}", element.get(name, default))


def number(value: str | None, default: float = 0.0) -> float:
    return float(value) if value is not None else default


def fmt(value: float) -> str:
    return f"{value:.5f}".rstrip("0").rstrip(".") or "0"


def color_and_opacity(value: str | None) -> tuple[str, str | None]:
    if not value:
        return "none", None
    raw = value.removeprefix("#")
    if len(raw) == 8:
        alpha = int(raw[:2], 16) / 255.0
        if alpha == 0:
            return "none", None
        return f"#{raw[2:]}", None if alpha == 1 else fmt(alpha)
    if len(raw) == 6:
        return f"#{raw}", None
    raise ValueError(f"Unsupported color: {value}")


class PreviewRenderer:
    def __init__(self, preview_time: tuple[int, int, int]) -> None:
        self.hour, self.minute, self.second = preview_time
        self.output: list[str] = []

    def emit(self, value: str) -> None:
        self.output.append(value)

    def render(self, scene: ET.Element) -> str:
        self.emit(
            '<svg xmlns="http://www.w3.org/2000/svg" width="450" height="450" '
            'viewBox="0 0 450 450" shape-rendering="geometricPrecision">'
        )
        self.emit('<rect width="450" height="450" fill="#000000"/>')
        for child in scene:
            self.render_wff_node(child)
        self.emit("</svg>")
        return "\n".join(self.output)

    def render_wff_node(self, element: ET.Element) -> None:
        tag = local_name(element.tag)
        if tag == "Group":
            self.render_group(element)
        elif tag == "PartDraw":
            self.render_part_draw(element)
        elif tag == "PartText":
            self.render_part_text(element)
        elif tag == "PartImage":
            self.render_part_image(element)
        elif tag == "AnalogClock":
            self.render_analog_clock(element)

    def box_transform(self, element: ET.Element) -> str:
        x = number(element.get("x"))
        y = number(element.get("y"))
        width = number(element.get("width"))
        height = number(element.get("height"))
        angle = number(element.get("angle"))
        pivot_x = number(element.get("pivotX"), 0.5) * width
        pivot_y = number(element.get("pivotY"), 0.5) * height
        pieces = [f"translate({fmt(x)} {fmt(y)})"]
        if angle:
            pieces.append(f"rotate({fmt(angle)} {fmt(pivot_x)} {fmt(pivot_y)})")
        return " ".join(pieces)

    def render_group(self, element: ET.Element) -> None:
        self.emit(f'<g transform="{self.box_transform(element)}">')
        for child in element:
            self.render_wff_node(child)
        self.emit("</g>")

    def render_part_draw(self, element: ET.Element) -> None:
        self.emit(f'<g transform="{self.box_transform(element)}">')
        for shape in element:
            tag = local_name(shape.tag)
            if tag == "Ellipse":
                x = number(shape.get("x"))
                y = number(shape.get("y"))
                width = number(shape.get("width"))
                height = number(shape.get("height"))
                attrs = self.wff_shape_style(shape)
                self.emit(
                    f'<ellipse cx="{fmt(x + width / 2)}" cy="{fmt(y + height / 2)}" '
                    f'rx="{fmt(width / 2)}" ry="{fmt(height / 2)}" {attrs}/>'
                )
            elif tag == "Rectangle":
                attrs = self.wff_shape_style(shape)
                self.emit(
                    f'<rect x="{shape.get("x")}" y="{shape.get("y")}" '
                    f'width="{shape.get("width")}" height="{shape.get("height")}" {attrs}/>'
                )
            elif tag == "Line":
                attrs = self.wff_shape_style(shape)
                self.emit(
                    f'<line x1="{shape.get("startX")}" y1="{shape.get("startY")}" '
                    f'x2="{shape.get("endX")}" y2="{shape.get("endY")}" {attrs}/>'
                )
        self.emit("</g>")

    def wff_shape_style(self, shape: ET.Element) -> str:
        style = next((child for child in shape if local_name(child.tag) in {"Fill", "Stroke"}), None)
        if style is None:
            return 'fill="none"'
        tag = local_name(style.tag)
        color, opacity = color_and_opacity(style.get("color"))
        if tag == "Fill":
            result = f'fill="{color}"'
            if opacity:
                result += f' fill-opacity="{opacity}"'
            return result
        result = (
            f'fill="none" stroke="{color}" stroke-width="{style.get("thickness", "1")}" '
            f'stroke-linecap="{style.get("cap", "BUTT").lower()}" '
            f'stroke-linejoin="{style.get("join", "MITER").lower()}"'
        )
        if opacity:
            result += f' stroke-opacity="{opacity}"'
        return result

    def render_part_text(self, element: ET.Element) -> None:
        text_element = next((child for child in element if local_name(child.tag) == "Text"), None)
        if text_element is None:
            return
        font = next((child for child in text_element if local_name(child.tag) == "Font"), None)
        if font is None:
            return
        x = number(element.get("x"))
        y = number(element.get("y"))
        width = number(element.get("width"))
        height = number(element.get("height"))
        align = text_element.get("align", "CENTER")
        anchor = {"START": "start", "END": "end"}.get(align, "middle")
        text_x = x if anchor == "start" else x + width if anchor == "end" else x + width / 2
        text_y = y + height / 2
        color, opacity = color_and_opacity(font.get("color", "#FFFFFFFF"))
        value = "".join(font.itertext()).strip()
        attrs = (
            f'x="{fmt(text_x)}" y="{fmt(text_y)}" text-anchor="{anchor}" '
            f'dominant-baseline="middle" font-family="Arial, sans-serif" '
            f'font-size="{font.get("size", "16")}" fill="{color}"'
        )
        if opacity:
            attrs += f' fill-opacity="{opacity}"'
        self.emit(f"<text {attrs}>{html.escape(value)}</text>")

    def render_part_image(self, element: ET.Element) -> None:
        image = next((child for child in element if local_name(child.tag) == "Image"), None)
        if image is None:
            return
        self.render_vector_resource(
            image.get("resource", ""),
            number(element.get("x")),
            number(element.get("y")),
            number(element.get("width")),
            number(element.get("height")),
        )

    def render_analog_clock(self, element: ET.Element) -> None:
        for hand in element:
            tag = local_name(hand.tag)
            if tag == "HourHand":
                angle = 30.0 * (
                    (self.hour % 12) + self.minute / 60.0 + self.second / 3600.0
                )
            elif tag == "MinuteHand":
                angle = 6.0 * (self.minute + self.second / 60.0)
            elif tag == "SecondHand":
                angle = 6.0 * self.second
            else:
                continue
            x = number(hand.get("x"))
            y = number(hand.get("y"))
            width = number(hand.get("width"))
            height = number(hand.get("height"))
            pivot_x = x + number(hand.get("pivotX"), 0.5) * width
            pivot_y = y + number(hand.get("pivotY"), 0.5) * height
            self.emit(f'<g transform="rotate({fmt(angle)} {fmt(pivot_x)} {fmt(pivot_y)})">')
            self.render_vector_resource(hand.get("resource", ""), x, y, width, height)
            self.emit("</g>")

    def render_vector_resource(
        self, resource: str, x: float, y: float, width: float, height: float
    ) -> None:
        path = DRAWABLE_DIR / f"{resource}.xml"
        root = ET.parse(path).getroot()
        viewport_width = number(android_attr(root, "viewportWidth"), width)
        viewport_height = number(android_attr(root, "viewportHeight"), height)
        self.emit(
            f'<g transform="translate({fmt(x)} {fmt(y)}) '
            f'scale({fmt(width / viewport_width)} {fmt(height / viewport_height)})">'
        )
        for child in root:
            self.render_vector_node(child)
        self.emit("</g>")

    def render_vector_node(self, element: ET.Element) -> None:
        tag = local_name(element.tag)
        if tag == "group":
            pivot_x = number(android_attr(element, "pivotX"))
            pivot_y = number(android_attr(element, "pivotY"))
            translate_x = number(android_attr(element, "translateX"))
            translate_y = number(android_attr(element, "translateY"))
            rotation = number(android_attr(element, "rotation"))
            scale_x = number(android_attr(element, "scaleX"), 1.0)
            scale_y = number(android_attr(element, "scaleY"), 1.0)
            transform = (
                f"translate({fmt(translate_x + pivot_x)} {fmt(translate_y + pivot_y)}) "
                f"rotate({fmt(rotation)}) scale({fmt(scale_x)} {fmt(scale_y)}) "
                f"translate({fmt(-pivot_x)} {fmt(-pivot_y)})"
            )
            self.emit(f'<g transform="{transform}">')
            for child in element:
                self.render_vector_node(child)
            self.emit("</g>")
        elif tag == "path":
            fill, fill_opacity = color_and_opacity(android_attr(element, "fillColor"))
            stroke, stroke_opacity = color_and_opacity(android_attr(element, "strokeColor"))
            attrs = [
                f'd="{html.escape(android_attr(element, "pathData", ""), quote=True)}"',
                f'fill="{fill}"',
            ]
            if fill_opacity:
                attrs.append(f'fill-opacity="{fill_opacity}"')
            if stroke != "none":
                attrs.extend(
                    [
                        f'stroke="{stroke}"',
                        f'stroke-width="{android_attr(element, "strokeWidth", "1")}"',
                        f'stroke-linecap="{android_attr(element, "strokeLineCap", "butt").lower()}"',
                        f'stroke-linejoin="{android_attr(element, "strokeLineJoin", "miter").lower()}"',
                    ]
                )
                if stroke_opacity:
                    attrs.append(f'stroke-opacity="{stroke_opacity}"')
            self.emit(f"<path {' '.join(attrs)}/>")


def preview_time(root: ET.Element) -> tuple[int, int, int]:
    value = "10:08:35"
    for element in root.findall("Metadata"):
        if element.get("key") == "PREVIEW_TIME":
            value = element.get("value", value)
            break
    hour, minute, second = (int(part) for part in value.split(":"))
    return hour, minute, second


def main() -> None:
    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT_ROOT / "watchface" / "build" / "preview.svg"
    root = ET.parse(WATCHFACE_XML).getroot()
    scene = root.find("Scene")
    if scene is None:
        raise RuntimeError("watchface.xml has no Scene")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(PreviewRenderer(preview_time(root)).render(scene), encoding="utf-8")
    print(destination)


if __name__ == "__main__":
    main()
