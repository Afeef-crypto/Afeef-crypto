#!/usr/bin/env python3
"""Build assets/banners/profile-peek-banner.gif from profile-peek-banner.png (subtle vertical bob).

Recolors teal/cyan sky and blue lower band to a black + dark red gradient, and maps the
navy shirt to burgundy, before the bob animation. Warm skin tones are left unchanged.
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
_TEAL_DIST = 58
_BOT_LUM = 52
_BOT_BLUE_SLACK = 28


def _warm_skin(r: int, g: int, b: int) -> bool:
    """Avoid recoloring skin / warm tones (pixel art uses orange/peach)."""
    return r >= 90 and r >= b - 40 and (r - b) < 95


def _bright_cyan(r: int, g: int, b: int) -> bool:
    return g > 88 and b > 88 and r < 92


def _cool_blue(r: int, g: int, b: int) -> bool:
    """Navy shirt, teal variants, and blue-tinted shadows — but not warm skin."""
    if _warm_skin(r, g, b):
        return False
    return (b > r + 2) and (b > g - 42) and r < 145 and b > 36


def _backdrop_rgb(y: int, h: int) -> tuple[int, int, int]:
    t = y / max(h - 1, 1)
    return (int(4 + t * 24), int(2 + t * 16), int(3 + t * 14))


def _shirt_rgb(r: int, g: int, b: int, y: int, h: int) -> tuple[int, int, int]:
    """Dark navy / blue garment → deep burgundy (preserve rough brightness)."""
    lum = (r + g + b) / 3.0
    depth = min(1.35, max(0.35, lum / 88.0))
    ty = (y - int(0.38 * h)) / max(int(0.38 * h), 1)
    tr = int(55 + depth * 95 + ty * 18)
    tg = int(6 + depth * 22)
    tb = int(8 + depth * 22)
    return (min(220, tr), min(90, tg), min(70, tb))


def _recolor_theme_rgba(img: Image.Image) -> Image.Image:
    """Teal/cyan sky, blue lower band, and navy shirt → black/red theme."""
    w, h = img.size
    pix = img.load()
    y_band = max(1, int(0.50 * h))
    x0, x1 = int(0.22 * w), int(0.78 * w)
    y_sh0, y_sh1 = int(0.38 * h), int(0.76 * h)
    href, gref, bref = _REF_TEAL
    for y in range(h):
        br, bg, bb = _backdrop_rgb(y, h)
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a < 8:
                continue
            if _warm_skin(r, g, b):
                continue
            lum = (r + g + b) / 3.0
            d_teal = math.sqrt((r - href) ** 2 + (g - gref) ** 2 + (b - bref) ** 2)
            is_teal = d_teal < _TEAL_DIST
            is_lower_band = y > y_band and lum < _BOT_LUM and b >= r - _BOT_BLUE_SLACK
            is_cyan = _bright_cyan(r, g, b)
            cool_b = _cool_blue(r, g, b)
            in_shirt = x0 <= x <= x1 and y_sh0 <= y <= y_sh1

            # Torso navy (often also "dark"): must win over lower_band backdrop.
            if in_shirt and cool_b and not is_cyan and not is_teal:
                sr, sg, sb = _shirt_rgb(r, g, b, y, h)
                pix[x, y] = (sr, sg, sb, a)
            elif is_teal or is_cyan or is_lower_band or cool_b:
                pix[x, y] = (br, bg, bb, a)
    return img


def main() -> None:
    if not PNG.exists():
        print(f"missing {PNG}", file=sys.stderr)
        sys.exit(1)
    img = Image.open(PNG).convert("RGBA")
    tw = 480
    img = img.resize((tw, int(img.height * tw / img.width)), Image.Resampling.LANCZOS)
    img = _recolor_theme_rgba(img)
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
    q0 = frames[0].quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    quantized = [q0] + [f.quantize(palette=q0) for f in frames[1:]]
    quantized[0].save(GIF, save_all=True, append_images=quantized[1:], duration=90, loop=0, optimize=True)
    print(f"[ok] {GIF} ({GIF.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
