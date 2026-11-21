#!/usr/bin/env python3
"""preview.png for the sauna club website: the desktop page top (1280 px) next to the phone view (390 px).
Input: screenshots written by w3s_check70.js into the folder given as the first argument (default /tmp/w3s70)."""
import os
import sys
from PIL import Image, ImageDraw

src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/w3s70"
out = "/root/divelux/freebies/templates/sauna-club-website/preview.png"
d = Image.open(os.path.join(src, "site-1280.png")).convert("RGB").crop((0, 0, 1280, 1700))
m = Image.open(os.path.join(src, "site-390.png")).convert("RGB").crop((0, 0, 390, 1700))
k = 0.75
d = d.resize((int(1280 * k), int(1700 * k)), Image.LANCZOS)
m = m.resize((int(390 * k), int(1700 * k)), Image.LANCZOS)
g = 40
W, H = g * 3 + d.width + m.width, g * 2 + d.height
sheet = Image.new("RGB", (W, H), "#e3ddd3")
dr = ImageDraw.Draw(sheet)
for (x, im) in ((g, d), (g * 2 + d.width, m)):
    dr.rectangle((x - 1, g - 1, x + im.width, g + im.height), outline="#b9afa2")
    sheet.paste(im, (x, g))
sheet.save(out, optimize=True)
print(out, sheet.size)
