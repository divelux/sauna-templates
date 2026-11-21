"""Shared pieces for the wave 3 screen templates (social stories, booking UI kit, club website).

- Palette and contrast check (WCAG 2.x relative luminance)
- Text measuring and wrapping with the real font files (fontTools, via gfxlib)
- SVG text that stays editable in Figma: real <text> elements, font-family "Bricolage Grotesque" / "Inter"
- render(): SVG -> PNG with resvg; only for the render the display family name is mapped to the name stored
  inside the static TTF we have (the SVG files themselves keep the public family name)

License of the templates: CC BY 4.0 (stories, UI kit) / MIT (website code) - DIVELUX, https://diveluxsaunahat.com
"""
import base64
import html
import os
import re
import sys

sys.path.insert(0, "/root/divelux/freebies/gfx/_tools")
import gfxlib as G  # noqa: E402

ROOT = "/root/divelux/freebies/templates"
SITE = "https://diveluxsaunahat.com"
TOOLS = "https://diveluxsaunahat.com/pages/sauna-tools"
WOFF = "/root/divelux/freebies/printables/_build/fonts"
ILLU = "/root/divelux/freebies/gfx/sauna-illustrations/svg"
ICONS = "/root/divelux/freebies/gfx/sauna-icons-filled/svg"

PAL = dict(G.PAL)
PAL.update({"card": "#fffdf9", "ink2": "#3d332c", "line2": "#b9afa2", "t1": "#f0a877", "t2": "#f5c7a0",
            "t3": "#f8dfc6", "t4": "#fbf1e5", "night2": "#2a1b13", "nightline": "#4a3426", "nightmuted": "#c9b9a8"})

DISPLAY = "'Bricolage Grotesque', 'Arial Narrow', Arial, sans-serif"
BODY = "Inter, Arial, sans-serif"
KIND = {"display": (DISPLAY, 700), "text": (BODY, 400), "semi": (BODY, 600)}

esc = lambda s: html.escape(str(s), quote=True)


def write(path, text, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, encoding=None if "b" in mode else "utf-8") as f:
        f.write(text)


# ---------- contrast ----------
def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexc):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---------- text ----------
def width(text, size, kind="text", tracking=0.0):
    return G.text_width(text, size, kind, tracking)


def wrap(text, size, maxw, kind="text", tracking=0.0):
    """Greedy word wrap with the real glyph widths. '\n' forces a break."""
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if line and width(t, size, kind, tracking) > maxw:
                out.append(line)
                line = w
            else:
                line = t
        out.append(line)
    return out


_MET = {}


def metrics(kind):
    """(ascent, descent) in em, from hhea, as browsers use them for the line box."""
    if kind not in _MET:
        t = G._font(kind)[0]
        upm = t["head"].unitsPerEm
        _MET[kind] = (t["hhea"].ascent / upm, -t["hhea"].descent / upm)
    return _MET[kind]


def first_baseline(kind, size, lh):
    """Baseline of the first line inside a CSS line box of height size*lh (half-leading model)."""
    a, d = metrics(kind)
    return (size * lh - (a + d) * size) / 2 + a * size


def svg_text(tid, x, y, w, text, size, kind="text", fill="#1b1512", lh=1.25, align="start", tracking=0.0,
             maxlines=None):
    """A wrapped block of real SVG text. (x, y) is the top-left of the block, w its width.
    Returns (markup, height)."""
    fam, wt = KIND[kind]
    lines = wrap(text, size, w * 0.985, kind, tracking)
    if maxlines and len(lines) > maxlines:
        raise SystemExit(f"text block {tid} needs {len(lines)} lines, max {maxlines}: {text!r}")
    for ln_ in lines:
        if width(ln_, size, kind, tracking) > w + 0.5:
            raise SystemExit(f"text block {tid}: '{ln_}' is wider than {w}")
    ax = {"start": x, "middle": x + w / 2, "end": x + w}[align]
    b0 = y + first_baseline(kind, size, lh)
    ls = f' letter-spacing="{tracking * size:.2f}"' if tracking else ""
    tsp = "".join(f'<tspan x="{ax:g}" y="{b0 + i * size * lh:.1f}">{esc(t)}</tspan>' for i, t in enumerate(lines))
    anchor = "" if align == "start" else f' text-anchor="{align}"'
    m = (f'<text id="{tid}" font-family="{DISPLAY if kind == "display" else BODY}" font-weight="{wt}" '
         f'font-size="{size:g}" fill="{fill}"{anchor}{ls}>{tsp}</text>')
    return m, len(lines) * size * lh


# ---------- art ----------
def illustration(name, x, y, size, gid=None):
    """One of the DIVELUX Sauna Illustrations (600x600, CC BY 4.0), placed as a group."""
    s = open(os.path.join(ILLU, name + ".svg"), encoding="utf-8").read()
    inner = s[s.index(">") + 1:s.rindex("</svg>")]
    inner = re.sub(r"<title>.*?</title>", "", inner)
    return f'<g id="{gid or "art-" + name}" transform="translate({x:g} {y:g}) scale({size / 600:g})">{inner}</g>'


def icon(name, x, y, size, color, gid=None):
    """One of the DIVELUX filled sauna icons (24 px grid, CC BY 4.0)."""
    s = open(os.path.join(ICONS, name + ".svg"), encoding="utf-8").read()
    inner = re.sub(r"<title>.*?</title>", "", s[s.index(">") + 1:s.rindex("</svg>")])
    return (f'<g id="{gid or "icon-" + name}" transform="translate({x:g} {y:g}) scale({size / 24:g})" '
            f'fill="{color}">{inner}</g>')


def render(svg, out=None, **kw):
    """PNG via resvg. Our only display TTF is stored as 'Bricolage Grotesque 96pt ExtraBold' (Bold)."""
    svg = svg.replace("'Bricolage Grotesque'", "'Bricolage Grotesque 96pt ExtraBold'")
    return G.render(svg, out, **kw)


# ---------- web fonts ----------
def face(fam, name, weight, extra="", url=None):
    p = os.path.join(WOFF, name + ".woff2")
    rng = open(p + ".range").read().strip()
    src = url or ("data:font/woff2;base64," + base64.b64encode(open(p, "rb").read()).decode())
    return (f'@font-face{{font-family:"{fam}";src:url({src}) format("woff2");font-weight:{weight};{extra}'
            f"font-display:swap;unicode-range:{rng}}}")


def font_css(urls=None):
    """Bricolage Grotesque (variable wght/wdth/opsz) + Inter (variable wght), Latin subset, SIL OFL 1.1.
    urls: dict name -> relative URL to link the files instead of embedding them."""
    u = urls or {}
    return "\n".join([
        face("Bricolage Grotesque", "BricolageGrotesque-latin", "200 800", "font-stretch:75% 100%;",
             u.get("BricolageGrotesque-latin")),
        face("Inter", "Inter-latin", "100 900", "", u.get("Inter-latin")),
    ])
