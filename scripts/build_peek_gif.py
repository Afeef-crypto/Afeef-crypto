#!/usr/bin/env python3
"""Build assets/banners/profile-peek-banner.gif from profile-peek-banner.png (subtle vertical bob).

Recolors the original teal/navy backdrop to a black + dark red theme (GitHub README) before
animating, without touching face/pixels that are far from the reference sky color.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PNG = ROOT / "assets" / "banners" / "profile-peek-banner.png"
GIF = ROOT / "assets" / "banners" / "profile-peek-banner.gif"

# Reference teal sampled from the source banner top row (~cyan sky).
_REF_TEAL = (37, 211, 222)
_TEAL_DIST = 42
_BOT_LUM = 42
_BOT_BLUE_SLACK = 20


def _recolor_backdrop_rgba(img: Image.Image) -> Image.Image:
    """Replaces teal sky and dark lower band with a vertical black→crimson gradient."""
    w, h = img.size
    pix = img.load()
    y_thresh = max(1, int(0.52 * h))
    href, gref, bref = _REF_TEAL
    denom = max(h - 1, 1)
    for y in range(h):
        t = y / denom
        nr = int(5 + t * 22)
        ng = int(2 + t * 14)
        nb = int(4 + t * 16)
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a < 8:
                continue
            d_teal = math.sqrt((r - href) ** 2 + (g - gref) ** 2 + (b - bref) ** 2)
            lum = (r + g + b) / 3.0
            is_teal = d_teal < _TEAL_DIST
            is_lower_band = y > y_thresh and lum < _BOT_LUM and b >= r - _BOT_BLUE_SLACK
            if is_teal or is_lower_band:
                pix[x, y] = (nr, ng, nb, a)
    return img


def main() -> None:
    if not PNG.exists():
        print(f"missing {PNG}", file=sys.stderr)
        sys.exit(1)
    img = Image.open(PNG).convert("RGBA")
    tw = 480
    img = img.resize((tw, int(img.height * tw / img.width)), Image.Resampling.LANCZOS)
    img = _recolor_backdrop_rgba(img)
    w, h = img.size
    px = img.crop((0, 0, 1, 1)).getpixel((0, 0))
    bg = (px[0], px[1], px[2], 255) if isinstance(px, tuple) and len(px) >= 3 else (12, 5, 5, 255)
    n, amp = 10, 3
    frames = []
    for i in range(n):
        dy = int(round(amp * math.sin(2 * math.pi * i / n)))
        canvas = Image.new("RGBA", (w, h), bg)
        canvas.paste(img, (0, dy), img)
        frames.append(canvas.convert("RGB"))
    q0 = frames[0].quantize(colors=48, method=Image.Quantize.MEDIANCUT)
    quantized = [q0] + [f.quantize(palette=q0) for f in frames[1:]]
    quantized[0].save(GIF, save_all=True, append_images=quantized[1:], duration=90, loop=0, optimize=True)
    print(f"[ok] {GIF} ({GIF.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
