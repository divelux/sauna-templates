"""P068 Sauna event poster: three layouts (Aufguss night, sauna and cold plunge social, open house),
each in US Letter, A3 and 1080 x 1350. All event details are sample placeholders ($00, dates, times)."""
import os

import w3_common as W
from w3_common import ed, esc

SLUG = "sauna-event-poster"
TITLE = "Sauna Event Poster"
DESC = "Editable sauna event poster template in three layouts: Aufguss night, sauna and cold plunge social, open house. US Letter, A3 and 1080 x 1350."
SIZES = {
    "letter": W.size("US Letter", "8.5in", "11in"),
    "a3": W.size("A3", "297mm", "420mm"),
    "post": W.size("1080 × 1350 post", "1080px", "1350px", pdf=False),
}
LAYOUTS = {"aufguss": "Aufguss night", "social": "Sauna social", "open": "Open house"}

CSS = """
.page{display:none}
html.layout-aufguss .lay-aufguss,html.layout-social .lay-social,html.layout-open .lay-open{display:flex}
.club{font-family:var(--display);font-weight:700;font-size:2.5u;line-height:1.1}
.pre{font-size:1.55u;color:var(--muted);margin-top:.4u}
.chip{display:inline-flex;align-items:center;gap:1.2u;background:var(--ember);color:var(--ink);border-radius:var(--r);padding:1u 1.6u;font-family:var(--display);font-weight:700;font-size:2.4u;line-height:1;white-space:nowrap}
.when{font-family:var(--display);font-weight:600;font-size:2.4u;line-height:1.2;margin-top:1.1u}
.bring b{display:block;font-family:var(--display);font-weight:700;font-size:1.8u;margin-bottom:.6u}
.bring p{font-size:1.5u;line-height:1.4}
.qr{width:13u;height:13u;border:.2u dashed currentColor;border-radius:var(--r);display:flex;align-items:center;justify-content:center;text-align:center;font-size:1.25u;line-height:1.25;flex:none;padding:1u}
.fine{font-size:1.2u;line-height:1.4}
.credit{font-size:1.05u}

/* 1. Aufguss night: dark room, glowing stove */
.lay-aufguss{background:var(--night);color:var(--paper);padding:6u 6u 3.2u}
.lay-aufguss .pre,.lay-aufguss .fine,.lay-aufguss .credit{color:#c9bfb3}
.lay-aufguss .art{position:relative;flex:1;min-height:0;display:flex;align-items:center;justify-content:center;margin:1u 0}
.lay-aufguss .art svg{height:100%;max-height:64u;width:auto;aspect-ratio:1}
.lay-aufguss h1{font-family:var(--display);font-weight:800;font-size:13.6u;line-height:.86;letter-spacing:-.035em;margin-top:3u}
.lay-aufguss .lead{font-family:var(--display);font-weight:500;font-size:2.35u;line-height:1.32;color:#e9e1d6;margin-top:2.2u;max-width:74u}
.lay-aufguss .row{display:grid;grid-template-columns:1fr 1fr auto;gap:4u;align-items:end;border-top:.2u solid #5a4a3e;padding-top:2.4u;margin-top:3u;flex:none}
.lay-aufguss .bring p{color:#e9e1d6}
.lay-aufguss .bot{display:flex;justify-content:space-between;align-items:baseline;gap:3u;margin-top:2.4u;flex:none}

/* 2. Sauna and cold plunge social: water above, heat below */
.lay-social{background:var(--paper);padding:0}
.lay-social .sea{background:var(--water);padding:5u 6u 1.5u;display:flex;justify-content:space-between;gap:2u;align-items:flex-end;flex:1;min-height:0}
.lay-social .sea svg{height:100%;max-height:58u;width:auto;aspect-ratio:1}
.lay-social .sea .pre{color:var(--ink-2)}
.lay-social .sea .left{align-self:stretch;display:flex;flex-direction:column;justify-content:space-between;align-items:flex-start}
.lay-social .low{padding:5u 6u 3.2u;display:flex;flex-direction:column;flex:none}
.lay-social h1{font-family:var(--display);font-weight:800;font-size:10.4u;line-height:.88;letter-spacing:-.03em;margin:3u 0 3u}
.lay-social .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:3u;border-top:.3u solid var(--ink);padding-top:2.2u}
.lay-social .grid .lab{font-size:1.35u;color:var(--muted)}
.lay-social .grid .v{font-family:var(--display);font-weight:700;font-size:2.6u;line-height:1.15;margin-top:.4u}
.lay-social .lead{font-size:1.75u;line-height:1.45;color:var(--ink-2);margin-top:3u;max-width:76u}
.lay-social .row{display:grid;grid-template-columns:1fr auto;gap:4u;align-items:end;margin-top:3u}
.lay-social .fine{color:var(--muted)}
.lay-social .bot{display:flex;justify-content:space-between;align-items:baseline;gap:3u;margin-top:2.4u}

/* 3. Open house: warm wood, the cabin, a simple timetable */
.lay-open{background:var(--wood-2);padding:6u 6u 3.2u}
.lay-open .head{display:flex;justify-content:space-between;align-items:flex-start;gap:3u;flex:none}
.lay-open .art{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;margin:1.4u 0}
.lay-open .art svg{height:100%;max-height:42u;width:auto;aspect-ratio:1}
.lay-open h1{font-family:var(--display);font-weight:800;font-size:15u;line-height:.85;letter-spacing:-.035em}
.lay-open .lead{font-family:var(--display);font-weight:500;font-size:2.4u;line-height:1.3;color:var(--ink-2);margin-top:1.8u;max-width:70u}
.lay-open .tt{display:grid;grid-template-columns:1fr 1fr;gap:0 5u;margin-top:3u;border-top:.3u solid var(--ink);flex:none}
.lay-open .tt li{display:grid;grid-template-columns:11u 1fr;gap:1.4u;align-items:baseline;padding:1.2u 0;border-bottom:.12u solid rgba(27,21,18,.25)}
.lay-open .tt .t{font-family:var(--display);font-weight:700;font-size:2u;white-space:nowrap}
.lay-open .tt .x{font-size:1.55u;line-height:1.35;color:var(--ink-2)}
.lay-open .row{display:grid;grid-template-columns:1fr auto;gap:4u;align-items:end;margin-top:2.6u;flex:none}
.lay-open .fine{color:var(--ink-2)}
.lay-open .bot{display:flex;justify-content:space-between;align-items:baseline;gap:3u;margin-top:2.2u;flex:none}
.lay-open .credit{color:var(--ink-2)}
html.size-a3 .lay-open .art svg{max-height:52u}
"""


def bot(note):
    return f'<div class="bot">{ed("p", "fine-print", esc(note), "fine", multi=True)}{W.credit()}</div>'


def aufguss():
    return f"""<main class="page lay-aufguss">
<div>{ed("p", "club-name", "Your Sauna Club", "club", sync="club")}{ed("p", "presents", "presents", "pre")}</div>
{ed("h1", "title", "Aufguss Night")}
{ed("p", "lead", "Four guided steam sessions with our sauna masters: birch, citrus, mint and a silent finale. Rest and tea in the lounge between rounds.", "lead", multi=True)}
<div class="art">{W.art("sauna-stove", drop_disc=True, label="illustration")}</div>
<div class="row">
<div>{ed("p", "date", "Friday, January 15", "chip")}{ed("p", "time", "7 – 10 pm", "when")}</div>
<div class="bring">{ed("b", "bring-title", "Bring")}{ed("p", "bring-list", "Two towels, a water bottle, flip-flops and a wool sauna hat, worn dry.", multi=True)}</div>
<div class="qr" data-name="qr-placeholder">{ed("span", "qr-label", "Tickets $00<br>QR code here", multi=True)}</div>
</div>
{bot("18+ event. Sauna is not for everyone: if you are pregnant or have a health condition, ask your doctor first.")}
</main>"""


def social():
    cells = [("Time", "10 am – 1 pm", "time"), ("Place", "123 Main Street", "place"), ("Price", "Free for members", "price")]
    grid = "".join(f'<div><p class="lab">{a}</p>{ed("p", k, esc(b), "v")}</div>' for a, b, k in cells)
    return f"""<main class="page lay-social">
<div class="sea" data-name="top">
<div class="left">{ed("p", "date", "Sunday, February 7", "chip")}
<div>{ed("p", "club-name", "Your Sauna Club", "club", sync="club")}{ed("p", "presents", "invites members and friends to a", "pre")}</div></div>
{W.art("cold-plunge", drop_disc=True, label="illustration")}
</div>
<div class="low">
{ed("h1", "title", "Sauna and cold plunge social", multi=True)}
<div class="grid" data-name="details">{grid}</div>
{ed("p", "lead", "Heat, cold, rest, repeat, at your own pace. The cold plunge is optional: a cool shower works too. Warm drinks by the fire after.", "lead", multi=True)}
<div class="row"><div class="bring">{ed("b", "bring-title", "Bring")}{ed("p", "bring-list", "Swimsuit, two towels, a water bottle and warm clothes for after.", multi=True)}</div>
<div class="qr" data-name="qr-placeholder">{ed("span", "qr-label", "RSVP<br>QR code here", multi=True)}</div></div>
{bot("Guests $00. Please RSVP so we can plan the benches.")}
</div>
</main>"""


def open_house():
    tt = [("2:00 pm", "Doors open, tea and snacks"), ("2:30 pm", "Sauna tours every 30 minutes"),
          ("3:30 pm", "Short Aufguss demo"), ("4:30 pm", "Questions with the builders"),
          ("5:00 pm", "Try a round: bring a swimsuit"), ("6:00 pm", "Last round")]
    rows = "".join(f'<li data-item>{ed("span", "time", esc(a), "t")}{ed("span", "what", esc(b), "x")}</li>' for a, b in tt)
    return f"""<main class="page lay-open">
<div class="head"><div>{ed("p", "club-name", "Your Sauna Club", "club", sync="club")}{ed("p", "presents", "123 Main Street, Your Town", "pre")}</div>
{ed("p", "date", "Saturday, March 6", "chip")}</div>
<div class="art">{W.art("lakeside-sauna", label="illustration", uid="poster-cabin-clip")}</div>
{ed("h1", "title", "Open House")}
{ed("p", "lead", "Come see the new sauna, take a tour and try a round. Families welcome.", "lead", multi=True)}
<ul class="tt" data-list data-name="timetable">{rows}</ul>
<div class="row"><div class="bring">{ed("b", "bring-title", "Free entry")}{ed("p", "bring-list", "No booking needed for the tours. To try a round, book a spot at yoursaunaclub.com.", multi=True)}</div>
<div class="qr" data-name="qr-placeholder">{ed("span", "qr-label", "Website<br>QR code here", multi=True)}</div></div>
{bot("Children in the sauna only with an adult. Sauna is not for everyone: if you have a health condition, ask your doctor first.")}
</main>"""


def build():
    d = os.path.join(W.ROOT, SLUG)
    html = os.path.join(d, SLUG + ".html")
    W.write(html, W.doc("dvx-event-poster-v1", TITLE, DESC, SIZES, "letter", CSS, aufguss() + social() + open_house(),
                        layouts=LAYOUTS, default_layout="aufguss", note="Pick a layout, then a size."))
    jobs = []
    for lay in LAYOUTS:
        for key, s in SIZES.items():
            base = f"{SLUG}-{lay}-{key}"
            jobs.append(dict(id=base, html=html, query=f"size={key}&layout={lay}", size=s, title=f"{TITLE}: {LAYOUTS[lay]} ({s['label']})",
                             pdf=os.path.join(d, base + ".pdf") if s["pdf"] else None,
                             png=[os.path.join(d, base + ".png")] if key == "post" else [f"/tmp/w3/{base}.png"],
                             svg=[os.path.join(d, base + ".svg")], scale=1 if key == "post" else 1.3))
    jobs.append(dict(id=SLUG + "-edit-open", kind="edit", html=html, query="size=letter&layout=open", size=SIZES["letter"], sync="club"))
    jobs.append(dict(id=SLUG + "-edit-aufguss", kind="edit", html=html, query="size=a3&layout=aufguss", size=SIZES["a3"], sync="club"))
    return dict(slug=SLUG, jobs=jobs, preview=[f"/tmp/w3/{SLUG}-{l}-letter.png" for l in LAYOUTS])
