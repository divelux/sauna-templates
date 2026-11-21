#!/usr/bin/env python3
"""Builds the wave 3 design templates. Usage: python3 w3_build.py [t64 t66 ...]  (no args = all)

1. modules write their editable HTML
2. w3_run.js (one Chromium under the shared lock) makes PDFs, PNGs and SVGs, checks overflow, runs the editing tests
3. every SVG is rendered again on its own (inline, same fonts) and compared with the page PNG pixel by pixel
4. PDF page sizes are checked with pypdf; preview.png is assembled
"""
import importlib
import json
import os
import subprocess
import sys

from PIL import Image, ImageChops, ImageStat
from pypdf import PdfReader

import w3_common as W

MODULES = ["t64_menu", "t66_board", "t67_card", "t68_poster"]
TMP = "/tmp/w3"
NODE = ("NODE_PATH=/opt/carmax/node_modules flock /tmp/freebies-chromium.lock nice -n 10 node "
        + os.path.join(os.path.dirname(os.path.abspath(__file__)), "w3_run.js"))


def run(jobs, tag):
    for j in jobs:
        s = j.pop("size", None)
        if s:
            j["vw"], j["vh"] = s["wpx"], s["hpx"]
            j["pw"], j["ph"] = s["w"], s["h"]
        if j.get("kind") == "edit":
            j["vw"], j["vh"] = 1366, 1000
    jp, rp = f"{TMP}/jobs-{tag}.json", f"{TMP}/report-{tag}.json"
    json.dump(jobs, open(jp, "w"), indent=1)
    subprocess.run(f"{NODE} {jp} {rp}", shell=True, check=True)
    return json.load(open(rp))


def svg_views(jobs):
    css = W.PC.font_css()
    out = []
    for j in jobs:
        for i, sv in enumerate(j.get("svg") or []):
            if not sv:
                continue
            ref = j["png"][i]
            name = os.path.basename(sv)[:-4]
            h = os.path.join(TMP, f"view-{name}.html")
            open(h, "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}html,body{{margin:0;background:#fff}}svg{{display:block}}</style></head>"
                               f"<body>{open(sv, encoding='utf-8').read()}</body></html>")
            out.append(dict(id="svg:" + name, kind="svgview", html=h, png=os.path.join(TMP, f"svgcheck-{name}.png"),
                            ref=ref, vw=j["vw"] + 20, vh=j["vh"] + 20, scale=j.get("scale", 1)))
    return out


def diff(a, b):
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    if A.size != B.size:
        B = B.resize(A.size)
    d = ImageChops.difference(A, B).convert("L")
    bad = sum(d.point(lambda v: 255 if v > 60 else 0).histogram()[255:])  / (A.size[0] * A.size[1])
    return round(ImageStat.Stat(d).mean[0], 2), round(100 * bad, 2)


def main():
    want = sys.argv[1:]
    os.makedirs(TMP, exist_ok=True)
    prods = [importlib.import_module(m).build() for m in MODULES if not want or any(w in m for w in want)]
    jobs = [j for p in prods for j in p["jobs"]]
    rep = run(jobs, "main")
    views = svg_views([j for j in jobs if j.get("svg")])
    rep2 = run([dict(v) for v in views], "svg")
    bad = 0
    for r in rep + rep2:
        probs = r["problems"] + r["errors"]
        extra = ""
        if "edit" in r:
            extra = f" fields={r.get('fields')} {json.dumps(r['edit'])[:200]}"
        if r["id"].startswith("svg:"):
            v = next(v for v in views if v["id"] == r["id"])
            m, pct = diff(v["ref"], v["png"])
            extra = f" svg-vs-page mean {m}, {pct}% px differ"
            if pct > 2.0:
                probs.append(f"SVG differs from page: {pct}%")
        print(("OK " if not probs else "!! ") + r["id"] + (f" pages={r['pages']}" if "pages" in r else "") + extra)
        for p in probs:
            bad += 1
            print("   ", p)
    for j in jobs:
        if j.get("pdf"):
            fix_pdf(j)
            rd = PdfReader(j["pdf"])
            sizes = {(round(float(p.mediabox.width) / 72 * 25.4, 1), round(float(p.mediabox.height) / 72 * 25.4, 1)) for p in rd.pages}
            print(f"   pdf {os.path.basename(j['pdf'])}: {len(rd.pages)} p, mm {sizes}, {os.path.getsize(j['pdf']) // 1024} KB")
    for p in prods:
        p.get("after", lambda: None)()
        make_preview(p)
    print("problems:", bad)


def fix_pdf(j):
    """Chromium rounds odd page sizes, so pages are rendered a little larger and cropped here to the exact size
    (anchored top-left, where the layout starts). Adds metadata and checks for the live credit link."""
    from pypdf import PdfWriter
    from pypdf.generic import RectangleObject
    r = PdfReader(j["pdf"])
    w = PdfWriter(clone_from=r)
    wt, ht = j["vw"] * 0.75, j["vh"] * 0.75
    links = 0
    for pg in w.pages:
        ha = float(pg.mediabox.height)
        box = RectangleObject([0, ha - ht, wt, ha])
        pg.mediabox = box
        pg.cropbox = box
        uris = [a.get_object().get("/A", {}).get("/URI") for a in pg.get("/Annots", [])]
        links += any(u and "diveluxsaunahat.com" in u for u in uris)
    if not links:
        print("   !! no live credit link in", os.path.basename(j["pdf"]))
    w.add_metadata({"/Title": j["title"], "/Author": "DIVELUX", "/Subject": "Editable template by DIVELUX. CC BY 4.0.",
                    "/Creator": "DIVELUX (https://diveluxsaunahat.com)", "/CreationDate": "D:20261121000000Z", "/ModDate": "D:20261121000000Z"})
    w.compress_identical_objects()
    with open(j["pdf"], "wb") as f:
        w.write(f)


def make_preview(p):
    ims = [Image.open(f).convert("RGB") for f in p["preview"]]
    hmax = 1100
    ims = [i.resize((round(i.width * hmax / i.height), hmax)) for i in ims]
    g = 40
    sheet = Image.new("RGB", (sum(i.width for i in ims) + g * (len(ims) + 1), hmax + 2 * g), "#cfc9c0")
    x = g
    for i in ims:
        sheet.paste(i, (x, g))
        x += i.width + g
    sheet.save(os.path.join(W.ROOT, p["slug"], "preview.png"), optimize=True)


if __name__ == "__main__":
    main()
