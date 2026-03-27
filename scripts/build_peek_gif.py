#!/usr/bin/env python3
"""Build assets/banners/profile-peek-banner.gif from profile-peek-banner.png (subtle vertical bob)."""
from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PNG = ROOT / "assets" / "banners" / "profile-peek-banner.png"
GIF = ROOT / "assets" / "banners" / "profile-peek-banner.gif"


def main() -> None:
    if not PNG.exists():
        print(f"missing {PNG}", file=sys.stderr)
        sys.exit(1)
    img = Image.open(PNG).convert("RGBA")
    tw = 480
    img = img.resize((tw, int(img.height * tw / img.width)), Image.Resampling.LANCZOS)
    w, h = img.size
    px = img.crop((0, 0, 1, 1)).getpixel((0, 0))
    bg = (px[0], px[1], px[2], 255) if isinstance(px, tuple) and len(px) >= 3 else (15, 23, 42, 255)
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
