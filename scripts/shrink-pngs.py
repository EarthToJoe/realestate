"""Shrinks screenshot PNGs in place to a 256-colour palette (about a quarter of the size; text stays sharp), so the
committed screen sets stay small.   uv run --no-project --with pillow python3 scripts/shrink-pngs.py DIR"""
import sys
from pathlib import Path

from PIL import Image

total = [0, 0]
for p in sorted(Path(sys.argv[1]).glob("*.png")):
    before = p.stat().st_size
    im = Image.open(p).convert("RGB")
    im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(p, optimize=True)
    total[0] += before
    total[1] += p.stat().st_size
print(f"{total[0] / 1e6:.1f} MB -> {total[1] / 1e6:.1f} MB")
