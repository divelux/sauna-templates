"""P067 Sauna club membership card: CR80 (85.6 x 54 mm) with 3 mm bleed (document 91.6 x 60 mm), front and back,
plus 10-up sheets on A4 and US Letter with cut marks (front sheet + back sheet for long-edge duplex).
Club name, card type and valid-thru are shared by every card (data-sync); each card on a sheet has its own
member name and number. Rows on a sheet touch each other: the design only uses vertical bands near the
top and bottom edges, so a cut a little off the line still looks right."""
import os

import w3_common as W
from w3_common import ed, esc

SLUG = "sauna-club-membership-card"
TITLE = "Sauna Club Membership Card"
DESC = "Editable sauna club membership card: CR80 85.6 x 54 mm with bleed, front and back with a 10-visit punch grid, plus 10-up print sheets for A4 and US Letter."
SIZES = {
    "card": W.size("Card 85.6 × 54 mm + bleed", "91.6mm", "60mm"),
    "a4": W.size("10 per A4 sheet", "210mm", "297mm"),
    "letter": W.size("10 per Letter sheet", "8.5in", "11in"),
}
TW, TH, BL, GUT = 85.6, 54.0, 3.0, 8.0
SHEET = {"a4": (210.0, 297.0), "letter": (215.9, 279.4)}

CSS = """
.card{position:relative;width:91.6mm;height:60mm;background:var(--paper);overflow:hidden;flex:none}
.cardpg{width:91.6mm;height:60mm}
.front .band{position:absolute;left:0;top:0;bottom:0;width:27mm;background:var(--night)}
.front .ico{position:absolute;left:7.6mm;top:8.4mm;width:12mm;height:12mm;color:var(--paper)}
.front .nolab{position:absolute;left:6mm;top:39.5mm;font-size:1.9mm;line-height:1;color:#c9bfb3}
.front .no{position:absolute;left:6mm;top:42.6mm;width:19mm;font-family:var(--display);font-weight:700;font-size:4.4mm;line-height:1.1;color:var(--paper);white-space:nowrap;font-variant-numeric:tabular-nums lining-nums}
.front .main{position:absolute;left:31mm;right:6mm;top:6.6mm;bottom:6mm;display:flex;flex-direction:column}
.front .club{font-family:var(--display);font-weight:700;font-size:4.9mm;line-height:1.05;letter-spacing:-.01em;white-space:nowrap}
.front .kind{display:flex;align-items:center;gap:1.4mm;margin-top:1.3mm;font-size:2.1mm;line-height:1;color:var(--muted)}
.front .kind i{width:1.7mm;height:1.7mm;border-radius:50%;background:var(--ember);flex:none}
.front .lab{display:block;font-size:1.75mm;line-height:1;color:var(--muted);margin-bottom:.9mm}
.front .who{margin-top:7.4mm}
.front .name{display:block;font-family:var(--display);font-weight:600;font-size:3.9mm;line-height:1.15;border-bottom:.25mm solid var(--ink);padding-bottom:.9mm;white-space:nowrap;min-height:5.5mm}
.front .row{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:auto}
.front .val{display:block;font-family:var(--display);font-weight:600;font-size:2.9mm;line-height:1.15;white-space:nowrap}
.back .band{position:absolute;right:0;top:0;bottom:0;width:9mm;background:var(--wood)}
.back .main{position:absolute;left:6mm;right:14mm;top:6.4mm;bottom:5.6mm;display:flex;flex-direction:column}
.back .hd{display:flex;justify-content:space-between;align-items:baseline;gap:2mm}
.back .tt{font-family:var(--display);font-weight:700;font-size:3.5mm;line-height:1}
.back .hint{font-size:1.8mm;color:var(--muted);white-space:nowrap}
.back .punch{display:grid;grid-template-columns:repeat(5,7mm);gap:2.2mm 3.6mm;margin-top:3mm}
.back .punch span{width:7mm;height:7mm;border:.25mm solid var(--ink-2);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.9mm;color:var(--muted);font-variant-numeric:tabular-nums}
.back .sig{display:flex;align-items:flex-end;gap:1.5mm;margin-top:auto;font-size:1.8mm;color:var(--muted)}
.back .sig i{flex:1;border-bottom:.2mm solid var(--ink-2);height:4mm}
.back .contact{font-size:1.9mm;line-height:1.3;color:var(--ink-2);margin-top:1.6mm;white-space:nowrap}
.back .credit{font-size:1.45mm;margin-top:.7mm}
.sheet{background:#fff;position:relative}
.slot{position:absolute;width:91.6mm;height:54mm;overflow:hidden}
.slot .card{position:absolute;left:0;top:-3mm}
.mk{position:absolute;background:var(--ink)}
.sheet .how{position:absolute;font-size:2.2mm;line-height:1.3;color:var(--muted);white-space:nowrap}
.sheet .how b{color:var(--ink);font-weight:600}
.cardpg,.sheet{display:none}
html.size-card .cardpg{display:block}
html.size-a4 .sheet.a4,html.size-letter .sheet.letter{display:block}
"""


def front(i, single=False):
    no = f"{i:04d}"
    return f"""<div class="card front" data-name="card-front">
<div class="band"></div>{W.icon("sauna-hat", label="icon")}
<span class="nolab">Member no.</span>{ed("span", "member-no", no, "no", sync=f"m{i}-no")}
<div class="main">
{ed("p", "club-name", "Your Sauna Club", "club", sync="club")}
<p class="kind"><i></i>{ed("span", "card-title", "Membership card", sync="ctitle")}</p>
<div class="who"><span class="lab">Member</span>{ed("span", "member-name", "Member Name", "name", sync=f"m{i}-name")}</div>
<div class="row"><div><span class="lab">Type</span>{ed("span", "card-type", "Monthly", "val", sync="type")}</div>
<div><span class="lab">Valid thru</span>{ed("span", "valid-thru", "12 / 2027", "val", sync="valid")}</div></div>
</div></div>"""


def back():
    circles = "".join(f"<span>{n}</span>" for n in range(1, 11))
    return f"""<div class="card back" data-name="card-back">
<div class="band"></div>
<div class="main">
<div class="hd">{ed("p", "punch-title", "Visits", "tt", sync="ptitle")}{ed("p", "punch-hint", "One mark per visit", "hint", sync="phint")}</div>
<div class="punch" data-name="punch-grid">{circles}</div>
<p class="sig"><span>Signature</span><i></i></p>
{ed("p", "contact", "yoursaunaclub.com · (000) 000-0000", "contact", sync="contact")}
{W.credit()}
</div></div>"""


def mm(v):
    return f"{v:.2f}mm"


def sheet(paper, side):
    pw, ph = SHEET[paper]
    mx = (pw - (2 * TW + GUT)) / 2
    my = (ph - 5 * TH) / 2
    cols = [mx, mx + TW + GUT]
    slots = ""
    for r in range(5):
        for c in range(2):
            i = r * 2 + c + 1
            cc = c if side == "front" else 1 - c  # long-edge duplex: the back of card i sits mirrored
            slots += f'<div class="slot" style="left:{mm(cols[cc] - BL)};top:{mm(my + r * TH)}">{front(i) if side == "front" else back()}</div>'
    marks = ""
    xs = [mx, mx + TW, mx + TW + GUT, mx + 2 * TW + GUT]
    ys = [my + r * TH for r in range(6)]
    t = 0.2
    top0 = max(0.6, my - 6)
    for x in xs:
        for y0, y1 in ((top0, my - 1.2), (ph - my + 1.2, ph - top0)):
            marks += f'<i class="mk" style="left:{mm(x - t / 2)};top:{mm(y0)};width:{mm(t)};height:{mm(y1 - y0)}"></i>'
    for y in ys:
        for x0, x1 in ((mx - 8, mx - 1.5), (pw - mx + 1.5, pw - mx + 8)):
            marks += f'<i class="mk" style="left:{mm(x0)};top:{mm(y - t / 2)};width:{mm(x1 - x0)};height:{mm(t)}"></i>'
    side_note = ("Front sheet. Print at 100% (actual size) on card stock." if side == "front"
                 else "Back sheet. Print on the back of the front sheet, flip on the long edge.")
    how = ""
    if my >= 9:
        how = f'<p class="how" style="left:{mm(mx)};top:{mm(max(1.5, top0 - 5))}"><b>{TITLE}</b> · {side_note}</p>'
    else:  # US Letter has only about 5 mm above and below the cards: put the note in the side margin
        how = ""
    return f'<main class="page sheet {paper}" data-name="sheet-{paper}-{side}">{marks}{slots}{how}</main>'


def build():
    d = os.path.join(W.ROOT, SLUG)
    html = os.path.join(d, SLUG + ".html")
    body = (f'<main class="page cardpg" data-name="front">{front(1, True)}</main>\n<main class="page cardpg" data-name="back">{back()}</main>\n'
            + sheet("a4", "front") + sheet("a4", "back") + sheet("letter", "front") + sheet("letter", "back"))
    W.write(html, W.doc("dvx-member-card-v1", TITLE, DESC, SIZES, "card", CSS, body,
                        note="Club name, type and dates change on every card at once; each card on a sheet has its own name and number."))
    jobs = []
    for key, s in SIZES.items():
        base = f"{SLUG}-{key}" if key != "card" else f"{SLUG}-cr80"
        if key == "card":
            png = [os.path.join(d, base + "-front.png"), os.path.join(d, base + "-back.png")]
            svg = [os.path.join(d, base + "-front.svg"), os.path.join(d, base + "-back.svg")]
        else:
            png = [f"/tmp/w3/{base}-front.png", f"/tmp/w3/{base}-back.png"]
            svg = [os.path.join(d, base + "-sheet-front.svg"), os.path.join(d, base + "-sheet-back.svg")]
        jobs.append(dict(id=base, html=html, query=f"size={key}", size=s, title=f"{TITLE} ({s['label']})",
                         pdf=os.path.join(d, base + ".pdf"), png=png, svg=svg, scale=6 if key == "card" else 1.5))
    jobs.append(dict(id=SLUG + "-edit-card", kind="edit", html=html, query="size=card", size=SIZES["card"], sync="club"))
    jobs.append(dict(id=SLUG + "-edit-sheet", kind="edit", html=html, query="size=letter", size=SIZES["letter"], sync="type"))
    return dict(slug=SLUG, jobs=jobs, preview=[os.path.join(d, f"{SLUG}-cr80-front.png"), os.path.join(d, f"{SLUG}-cr80-back.png"),
                                               f"/tmp/w3/{SLUG}-letter-front.png"])
