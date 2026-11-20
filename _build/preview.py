"""Draws preview.png for every template: the real workbook cells (values recalculated with `formulas`,
styles read with openpyxl) laid out as HTML and photographed with one headless Chromium under the shared lock.
The previews are renderings of the files, not screenshots of Excel."""
import base64
import csv
import datetime as dt
import html
import json
import os
import subprocess

import openpyxl
from openpyxl.utils import get_column_letter, range_boundaries
from PIL import Image

import tcommon as T
from recalc import recalc

FONTS = "/root/divelux/freebies/printables/_build/fonts"
TMP = "/tmp/tpl-preview"
EPOCH = dt.datetime(1899, 12, 30)
esc = lambda s: html.escape(str(s), quote=True)


def face(fam, name, weight, extra=""):
    p = os.path.join(FONTS, name + ".woff2")
    rng = open(p + ".range").read().strip()
    b = base64.b64encode(open(p, "rb").read()).decode()
    return (f'@font-face{{font-family:"{fam}";src:url(data:font/woff2;base64,{b}) format("woff2");font-weight:{weight};{extra}'
            f"font-display:block;unicode-range:{rng}}}")


CSS = "\n".join([
    face("Bricolage Grotesque", "BricolageGrotesque-latin", "200 800", "font-stretch:75% 100%;"),
    face("Inter", "Inter-latin", "100 900"), face("Inter", "Inter-latin-ext", "100 900"),
]) + """
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#cfc9c0;font-family:Inter,Arial,sans-serif;color:#1b1512}
#shot{display:inline-flex;gap:24px;padding:24px;align-items:flex-start;background:#cfc9c0}
.win{background:#f6f3ee;box-shadow:0 2px 14px rgba(27,21,18,.22);position:relative;overflow:hidden}
.tabs{display:flex;gap:2px;padding:0 10px;background:#e3ddd3;border-top:1px solid #b9afa2;height:30px;align-items:flex-end}
.tabs span{font-size:12px;padding:6px 14px 7px;color:#6f655c;white-space:nowrap}
.tabs span.on{background:#f6f3ee;color:#1b1512;font-weight:600;border:1px solid #b9afa2;border-top:0;border-radius:0 0 5px 5px;margin-top:-1px}
.sheet{position:relative;padding:14px 16px 14px}
table{border-collapse:collapse;table-layout:fixed}
td{padding:0 4px;overflow:visible;white-space:nowrap;line-height:1.15}
td>div{position:relative;z-index:1}
td.wrap{white-space:normal}
td.clip{overflow:hidden}
.chart{position:absolute;background:#fff;border:1px solid #d9d9d9}
"""


def fmt(v, nf):
    if v is None or v == "":
        return ""
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    nf = nf or "General"
    is_date = any(t in nf for t in ("mmm", "yy", "ddd")) and "@" not in nf
    if isinstance(v, (dt.datetime, dt.date)) or (is_date and isinstance(v, (int, float))):
        d = v if isinstance(v, (dt.datetime, dt.date)) else EPOCH + dt.timedelta(days=float(v))
        out = nf.replace("ddd", "%a").replace("mmm", "%b").replace("yyyy", "%Y").replace("d", "%-d").replace("%-%-d", "%a")
        out = out.replace("%a", "\x01").replace("%b", "\x02").replace("%Y", "\x03").replace("%-d", "\x04")
        return out.replace("\x01", d.strftime("%a")).replace("\x02", d.strftime("%b")).replace("\x03", d.strftime("%Y")).replace("\x04", str(d.day))
    if isinstance(v, str):
        return v
    if nf.startswith("$"):
        dec = 2 if ".00" in nf else 0
        s = f"{abs(v):,.{dec}f}"
        return ("-" if round(v, dec) < 0 else "") + "$" + s
    if nf.endswith("%"):
        return f"{v * 100:.0f}%"
    if nf in ("0", "0.0", "0.00", "0.000"):
        return f"{v:.{len(nf) - 2 if '.' in nf else 0}f}"
    if "#" in nf and "." in nf:                      # 0.### / 0.0##
        lo = nf.split(".")[1].count("0")
        s = f"{v:.{len(nf.split('.')[1])}f}".rstrip("0")
        intp, _, frac = s.partition(".")
        return intp + ("." + frac.ljust(lo, "0") if (frac or lo) else "")
    if isinstance(v, float):
        return f"{v:.10g}"
    return str(v)


def sheet_html(path, sheet, values, max_row, max_col, cf=None, chart=None, zoom=1.0):
    """cf: {(row, col): css} extra styles standing in for conditional formatting. chart: (row, svg, w, h)."""
    wb = openpyxl.load_workbook(path)
    ws = wb[sheet]
    vals = values[sheet.upper()]
    merged, covered = {}, set()
    for m in ws.merged_cells.ranges:
        c0, r0, c1, r1 = range_boundaries(str(m))
        merged[(r0, c0)] = (r1 - r0 + 1, c1 - c0 + 1)
        covered |= {(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)} - {(r0, c0)}
    cf = dict(cf or {})
    for rng, rules in ws.conditional_formatting._cf_rules.items():      # cellIs rules: evaluate on the computed values
        for rule in rules:
            if rule.type != "cellIs" or rule.dxf is None or rule.dxf.font is None:
                continue
            ref = rule.formula[0].strip('"')
            for area in str(rng.sqref).split():
                c0, r0, c1, r1 = range_boundaries(area)
                for r in range(r0, min(r1, max_row) + 1):
                    for c in range(c0, min(c1, max_col) + 1):
                        v = vals.get(ws.cell(r, c).coordinate)
                        try:
                            hit = {"greaterThan": lambda: v > float(ref), "lessThan": lambda: v < float(ref),
                                   "greaterThanOrEqual": lambda: v >= float(ref), "equal": lambda: str(v) == ref}[rule.operator]()
                        except (TypeError, ValueError):
                            hit = False
                        if hit and not isinstance(v, bool) and v is not None:
                            cf[(r, c)] = f"color:#{rule.dxf.font.color.rgb[-6:]};font-weight:700"
    widths = [round((ws.column_dimensions[get_column_letter(c)].width or 8.43) * 7 + 5) for c in range(1, max_col + 1)]
    heights = [round((ws.row_dimensions[r].height or 15) * 96 / 72) for r in range(1, max_row + 1)]
    out = [f'<table style="width:{sum(widths)}px"><colgroup>' + "".join(f'<col style="width:{w}px">' for w in widths) + "</colgroup>"]
    for r in range(1, max_row + 1):
        out.append(f'<tr style="height:{heights[r - 1]}px">')
        for c in range(1, max_col + 1):
            if (r, c) in covered:
                continue
            cell = ws.cell(r, c)
            v = vals.get(cell.coordinate)
            if v is None and not (isinstance(cell.value, str) and cell.value.startswith("=")):
                v = cell.value
            text = fmt(v, cell.number_format)
            f, a = cell.font, cell.alignment
            st = []
            if cell.fill and cell.fill.fill_type == "solid":
                st.append(f"background:#{cell.fill.start_color.rgb[-6:]}")
            if cell.border and cell.border.left and cell.border.left.style:
                st.append(f"border:1px solid #{T.LINE}")
            fam = "'Bricolage Grotesque'" if f.name == T.HEAD_FONT else "Inter"
            st.append(f"font-family:{fam},Arial,sans-serif;font-size:{f.sz or 11}pt")
            if f.b:
                st.append("font-weight:700" if f.name != T.HEAD_FONT else "font-weight:800")
            if f.i:
                st.append("font-style:italic")
            if f.u:
                st.append("text-decoration:underline")
            if f.color is not None and isinstance(f.color.rgb, str):
                st.append(f"color:#{f.color.rgb[-6:]}")
            h = a.horizontal or ("right" if isinstance(v, (int, float)) and not isinstance(v, bool) else "left")
            st.append(f"text-align:{h}")
            st.append(f"vertical-align:{ {'center': 'middle', 'top': 'top'}.get(a.vertical, 'bottom')}")
            if cf and (r, c) in cf:
                st.append(cf[(r, c)])
            span = ""
            if (r, c) in merged:
                rs, cs = merged[(r, c)]
                span = (f' rowspan="{rs}"' if rs > 1 else "") + (f' colspan="{cs}"' if cs > 1 else "")
            cls = "wrap" if a.wrap_text else ("clip" if (cell.border and cell.border.left and cell.border.left.style) else "")
            out.append(f'<td{span} class="{cls}" style="{";".join(st)}"><div>{esc(text)}</div></td>')
        out.append("</tr>")
    out.append("</table>")
    ch = ""
    if chart:
        row, svg, w, h = chart
        top = 14 + sum(heights[:row - 1])
        ch = f'<div class="chart" style="left:16px;top:{top}px;width:{w}px;height:{h}px">{svg}</div>'
    tabs = "".join(f'<span class="{"on" if n == sheet else ""}">{esc(n)}</span>' for n in wb.sheetnames)
    return f'<div class="win" style="zoom:{zoom}"><div class="sheet">{"".join(out)}{ch}</div><div class="tabs">{tabs}</div></div>'


def bar_chart_svg(cats, planned, actual, w, h, title):
    """Stand-in for the workbook's bar chart, drawn from the same Summary cells."""
    left, right, top, bottom = 205, 24, 40, 62
    n = len(cats)
    mx = max(planned + actual + [1])
    step = 10 ** (len(str(int(mx))) - 1)
    step = step / 2 if mx / step < 4 else step
    top_v = step * -(-mx // step)
    pw, ph = w - left - right, h - top - bottom
    band = ph / n
    bh = band * 0.31
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif">',
           f'<text x="{w / 2}" y="24" text-anchor="middle" font-size="14" fill="#3d332c">{esc(title)}</text>']
    k = 0
    while k * step <= top_v + 1e-9:
        x = left + pw * (k * step) / top_v
        out.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + ph}" stroke="#d9d9d9"/>')
        out.append(f'<text x="{x:.1f}" y="{top + ph + 16}" text-anchor="middle" font-size="10" fill="#595959">${k * step:,.0f}</text>')
        k += 1
    for i, cat in enumerate(cats):
        y = top + band * i + band / 2
        out.append(f'<text x="{left - 8}" y="{y + 3.5:.1f}" text-anchor="end" font-size="10.5" fill="#595959">{esc(cat)}</text>')
        out.append(f'<rect x="{left}" y="{y - bh:.1f}" width="{pw * planned[i] / top_v:.1f}" height="{bh:.1f}" fill="#{T.TAN}"/>')
        out.append(f'<rect x="{left}" y="{y:.1f}" width="{pw * actual[i] / top_v:.1f}" height="{bh:.1f}" fill="#{T.WOOD}"/>')
    lx = w / 2 - 80
    out.append(f'<rect x="{lx}" y="{h - 22}" width="10" height="10" fill="#{T.TAN}"/><text x="{lx + 15}" y="{h - 13}" font-size="11" fill="#595959">Planned</text>')
    out.append(f'<rect x="{lx + 85}" y="{h - 22}" width="10" height="10" fill="#{T.WOOD}"/><text x="{lx + 100}" y="{h - 13}" font-size="11" fill="#595959">Actual</text>')
    out.append("</svg>")
    return "".join(out)


def page(body):
    return f'<!doctype html><html lang="en-US"><head><meta charset="utf-8"><title>preview</title><style>{CSS}</style></head><body><div id="shot">{body}</div></body></html>'


def shoot(jobs, max_width=1800):
    """jobs: [(html_text, png_path)]. One Chromium for all, under the shared lock."""
    os.makedirs(TMP, exist_ok=True)
    spec = []
    for i, (text, png) in enumerate(jobs):
        p = os.path.join(TMP, f"p{i}.html")
        open(p, "w", encoding="utf-8").write(text)
        spec.append(dict(html=p, png=png))
    json.dump(spec, open(os.path.join(TMP, "jobs.json"), "w"))
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(f"NODE_PATH=/opt/carmax/node_modules flock /tmp/freebies-chromium.lock node {here}/shoot.js {TMP}/jobs.json",
                   shell=True, check=True)
    for _, png in jobs:
        im = Image.open(png).convert("RGB")
        if im.width > max_width:
            im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
        im.save(png, optimize=True)
        print(os.path.relpath(png, T.ROOT), im.size, os.path.getsize(png) // 1024, "KB")
