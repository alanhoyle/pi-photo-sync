#!/usr/bin/env python3
"""
E-paper display driver for Waveshare 2.13" Touch E-Paper HAT (V2/V4).

Usage (called by the hook script):
  epaper_display.py status  LINE1 [LINE2]
  epaper_display.py error   LINE1 [LINE2]
  epaper_display.py done    LINE1 [LINE2]

Install dependencies:
  pip3 install waveshare-epaper pillow RPi.GPIO spidev
"""

import sys
import textwrap

try:
    from waveshare_epd import epd2in13_V4 as epd_module
    from PIL import Image, ImageDraw, ImageFont
    HAS_DISPLAY = True
except ImportError:
    HAS_DISPLAY = False


FONT_SIZE_LARGE = 18
FONT_SIZE_SMALL = 14

MODE_ICONS = {
    "status": "",
    "error":  "!",
    "done":   "OK",
}


def render(mode: str, line1: str, line2: str = "") -> None:
    if not HAS_DISPLAY:
        print(f"[epaper] {mode}: {line1} {line2}", file=sys.stderr)
        return

    epd = epd_module.EPD()
    epd.init()

    image = Image.new("1", (epd.width, epd.height), 255)  # landscape
    draw = ImageDraw.Draw(image)

    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_SIZE_LARGE)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE_SMALL)
    except OSError:
        font_large = ImageFont.load_default()
        font_small = font_large

    icon = MODE_ICONS.get(mode, "")
    max_chars = 22

    draw.rectangle([0, 0, epd.width, FONT_SIZE_LARGE + 4], fill=0)
    header = f"{icon} {line1}" if icon else line1
    draw.text((4, 2), header[:max_chars], font=font_large, fill=255)

    if line2:
        y = FONT_SIZE_LARGE + 8
        for chunk in textwrap.wrap(line2, max_chars):
            draw.text((4, y), chunk, font=font_small, fill=0)
            y += FONT_SIZE_SMALL + 2

    epd.display(epd.getbuffer(image))
    epd.sleep()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <status|error|done> LINE1 [LINE2]")
        sys.exit(1)

    mode_arg = sys.argv[1]
    l1 = sys.argv[2]
    l2 = sys.argv[3] if len(sys.argv) > 3 else ""
    render(mode_arg, l1, l2)
