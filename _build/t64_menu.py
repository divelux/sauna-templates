"""P064 Spa menu and price list: one editable HTML, US Letter + A4 print, 1080 x 1350 for social posts and screens.
Every service, price and line of text is a sample placeholder; prices are $00 on purpose."""
import os

import w3_common as W
from w3_common import ed, esc

SLUG = "spa-menu-price-list"
TITLE = "Spa and Sauna Menu and Price List"
DESC = "Editable spa and sauna menu and price list template: sauna sessions, treatments, add-ons, memberships and house notes. US Letter, A4 and 1080 x 1350."
SIZES = {
    "letter": W.size("US Letter", "8.5in", "11in"),
    "a4": W.size("A4", "210mm", "297mm"),
    "post": W.size("1080 × 1350 post", "1080px", "1350px", pdf=False),
}

SECTIONS = [
    ("sauna", "Sauna", "per person unless noted", [
        ("Shared sauna, day pass", "Sauna, cold plunge and lounge, all day.", "$00"),
        ("Private sauna, 60 min", "The whole room for up to four guests. Towels included.", "$00"),
        ("Sauna and cold plunge, 90 min", "Rounds of heat and cold at your own pace.", "$00"),
        ("Aufguss session", "A guided steam round with a sauna master, about 15 minutes.", "$00"),
    ]),
    ("treatments", "Treatments", "book at the front desk", [
        ("Birch whisk session, 30 min", "Whisking with fresh or dried birch whisks in the warm room.", "$00"),
        ("Body scrub, 30 min", "A salt or sugar scrub, rinsed off before the next round.", "$00"),
        ("Massage, 60 min", "Ask about our therapists and times.", "$00"),
    ]),
    ("addons", "Add-ons", "for any visit", [
        ("Towel and robe", "Fresh set for the day.", "$00"),
        ("Flip-flops", "Yours to keep.", "$00"),
        ("Pot of herbal tea", "Served in the lounge.", "$00"),
        ("Wool felt sauna hat", "To keep, in several colors.", "$00"),
    ]),
    ("members", "Memberships", "valid for one person", [
        ("10-visit card", "Ten day passes, use them any day.", "$00"),
        ("Monthly membership", "Unlimited day passes for 30 days.", "$00"),
    ]),
]
NOTES = [
    "Shower before your first round.",
    "Sit or lie on a towel on the benches.",
    "Drink water between rounds.",
    "Leave the heat whenever you need to.",
    "Children are welcome with an adult.",
]

CSS = """
.page{padding:6.2u 6.4u 3.2u}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:4u;flex:none}
.top .k{font-family:var(--body);font-weight:600;font-size:1.5u;color:var(--muted)}
.top .hours{font-size:1.5u;line-height:1.4;color:var(--ink-2);text-align:right;min-width:20u}
.mast{display:grid;grid-template-columns:1fr 17u;gap:3u;align-items:end;margin-top:1.6u;flex:none}
.mast h1{font-family:var(--display);font-weight:800;font-size:8.6u;line-height:.92;letter-spacing:-.025em}
.mast .tag{font-family:var(--display);font-weight:500;font-size:2.15u;line-height:1.3;color:var(--ink-2);margin-top:1.4u;max-width:52u}
.mast svg{width:17u;height:17u;margin-bottom:-.6u}
.rule{height:.3u;background:var(--ink);margin:2.4u 0 0;flex:none}
.cols{display:grid;grid-template-columns:1fr 1fr;column-gap:5.4u;flex:1;min-height:0;padding-top:2.6u}
.col{display:flex;flex-direction:column;gap:3.1u;min-width:0}
.sec header{display:flex;justify-content:space-between;align-items:baseline;gap:2u;border-bottom:.12u solid var(--line-2);padding-bottom:.7u;margin-bottom:.4u}
.sec h2{font-family:var(--display);font-weight:700;font-size:3.1u;line-height:1;letter-spacing:-.012em}
.sec header p{font-size:1.3u;color:var(--muted);white-space:nowrap}
.sec ul{display:flex;flex-direction:column}
.it{padding:1.05u 0 .95u;border-bottom:.1u solid var(--line)}
.it:last-child{border-bottom:0}
.it .row{display:flex;align-items:baseline;gap:1u}
.it .n{font-family:var(--display);font-weight:600;font-size:1.95u;line-height:1.2;letter-spacing:-.005em;min-width:4u}
.it .lead{flex:1;border-bottom:.16u dotted var(--line-2);min-width:2u;transform:translateY(-.35u)}
.it .p{font-family:var(--display);font-weight:700;font-size:1.95u;line-height:1.2;min-width:3u;text-align:right;white-space:nowrap}
.it .x{font-size:1.42u;line-height:1.38;color:var(--muted);margin-top:.25u;padding-right:6u}
.note{background:var(--paper-2);border-radius:var(--r);padding:2.1u 2.3u 2.2u}
.note h2{font-family:var(--display);font-weight:700;font-size:2.3u;line-height:1;margin-bottom:1.1u}
.note li{display:flex;align-items:center;gap:1.3u;padding:.42u 0;font-size:1.45u;line-height:1.35;color:var(--ink-2)}
.note li i{flex:none;width:.8u;height:.8u;border-radius:50%;background:var(--ember);transform:translateY(-.05u)}
.bottom{display:flex;flex-direction:column;align-items:stretch;gap:1u;border-top:.3u solid var(--ink);padding-top:1.5u;margin-top:2.2u;flex:none}
.bottom .contact{display:flex;flex-wrap:wrap;gap:.4u 2.6u;font-size:1.5u;color:var(--ink-2)}
.bottom .credit{text-align:right}
.bottom .contact b{font-family:var(--display);font-weight:700;color:var(--ink)}
.bottom .credit{font-size:1.05u}
html.size-a4 .col{gap:4.6u}
html.size-a4 .it{padding:1.65u 0 1.5u}
html.size-a4 .cols{padding-top:3.4u}
"""


def item(n, x, p):
    return (f'<li class="it" data-item>'
            f'<div class="row">{ed("span", "item-name", esc(n), "n")}<i class="lead"></i>{ed("span", "item-price", esc(p), "p")}</div>'
            f'{ed("p", "item-note", esc(x), "x")}</li>')


def section(key, title, sub, items):
    rows = "".join(item(*i) for i in items)
    return (f'<section class="sec" data-name="section-{key}"><header>{ed("h2", "section-title", esc(title))}'
            f'{ed("p", "section-note", esc(sub))}</header><ul data-list>{rows}</ul></section>')


def body():
    s = {k: section(k, t, sub, it) for k, t, sub, it in SECTIONS}
    notes = "".join(f'<li data-item><i></i>{ed("span", "note-line", esc(n))}</li>' for n in NOTES)
    return f"""<main class="page">
<div class="top">{ed("p", "kicker", "Spa &amp; sauna menu", "k")}{ed("p", "hours", "Open daily 7 am – 10 pm<br>Last entry 9 pm", "hours", multi=True)}</div>
<div class="mast"><div>{ed("h1", "club-name", "Your Sauna Club", sync="club")}{ed("p", "tagline", "Wood-fired sauna, cold plunge and a quiet lounge.", "tag")}</div>
{W.art("sauna-stove", label="illustration")}</div>
<div class="rule"></div>
<div class="cols">
<div class="col">{s["sauna"]}{s["treatments"]}</div>
<div class="col">{s["addons"]}{s["members"]}
<aside class="note" data-name="house-notes">{ed("h2", "notes-title", "Good to know")}<ul data-list>{notes}</ul></aside></div>
</div>
<div class="bottom"><div class="contact" data-name="contact">{ed("b", "contact-name", "Your Sauna Club", sync="club")}{ed("span", "address", "123 Main Street, Your Town")}{ed("span", "phone", "(000) 000-0000")}{ed("span", "website", "yoursaunaclub.com")}</div>
{W.credit()}</div>
</main>"""


def build():
    d = os.path.join(W.ROOT, SLUG)
    html = os.path.join(d, SLUG + ".html")
    W.write(html, W.doc("dvx-spa-menu-v1", TITLE, DESC, SIZES, "letter", CSS, body(),
                        note="Hover a line to remove it; “+ Add line” adds one."))
    jobs = []
    for k, s in SIZES.items():
        base = f"{SLUG}-{k}"
        jobs.append(dict(id=base, html=html, query=f"size={k}", size=s, title=f"{TITLE} ({s['label']})",
                         pdf=os.path.join(d, base + ".pdf") if s["pdf"] else None,
                         png=[os.path.join(d, base + ".png")] if k == "post" else [f"/tmp/w3/{base}.png"],
                         svg=[os.path.join(d, base + ".svg")], scale=1 if k == "post" else 1.5))
    jobs.append(dict(id=SLUG + "-edit", kind="edit", html=html, query="size=letter", size=SIZES["letter"]))
    return dict(slug=SLUG, jobs=jobs, preview=[f"/tmp/w3/{SLUG}-letter.png", os.path.join(d, SLUG + "-post.png")])
