"""P066 Aufguss schedule board: editable HTML; A3 and Tabloid (11 x 17 in) to print, 1920 x 1080 for a lobby TV.
The print board and the TV screen share their fields (data-sync), so a time typed in one shows in the other.
Session names, scents and times are samples; 'Name' marks the sauna master's name."""
import os

import w3_common as W
from w3_common import ed, esc

SLUG = "aufguss-schedule-board"
TITLE = "Aufguss Schedule Board"
DESC = "Editable Aufguss schedule board for saunas and spas: times, session names, scents, sauna masters and rooms. A3 and Tabloid to print, 1920 x 1080 for a lobby TV."
SIZES = {
    "a3": W.size("A3 print", "297mm", "420mm"),
    "tabloid": W.size("Tabloid 11 × 17 in", "11in", "17in"),
    "tv": W.size("TV 1920 × 1080", "1920px", "1080px", pdf=False),
}
ROWS = [
    ("4:00 pm", "Welcome round", "A gentle start", "Eucalyptus", "Mild", "Name", "Main sauna", "10 min"),
    ("5:00 pm", "Birch forest", "Fresh birch whisks on the stones", "Birch and pine", "Medium", "Name", "Main sauna", "12 min"),
    ("6:00 pm", "Citrus", "Three rounds of steam", "Orange and lemon", "Medium", "Name", "Garden sauna", "12 min"),
    ("7:00 pm", "Mint and ice", "Ice on the stones", "Peppermint", "Strong", "Name", "Main sauna", "15 min"),
    ("8:00 pm", "Lavender evening", "Slow towel waves", "Lavender", "Mild", "Name", "Garden sauna", "12 min"),
    ("9:00 pm", "Silent round", "No talking, no music", "No scent", "Mild", "Name", "Main sauna", "10 min"),
]
HOW = [
    ("Come a little early", "Take your seat about five minutes before the start. The door closes when the session begins."),
    ("Leave whenever you need to", "If it gets too hot, step out quietly. Nobody has to stay to the end."),
    ("Cool down and rest", "Fresh air, a cool shower and a drink of water before your next round."),
]

CSS = """
.pt{padding:5.2u 5.6u 2.6u}
.pt .top{display:flex;justify-content:space-between;align-items:baseline;gap:4u;flex:none}
.pt .club{font-family:var(--display);font-weight:700;font-size:2.6u;line-height:1.1}
.pt .date{display:flex;align-items:center;gap:1.2u;font-family:var(--display);font-weight:600;font-size:2.3u;color:var(--ink-2)}
.pt .date i{width:1.2u;height:1.2u;border-radius:50%;background:var(--ember);flex:none}
.pt h1{font-family:var(--display);font-weight:800;font-size:12.4u;line-height:.9;letter-spacing:-.03em;margin-top:3.2u}
.pt .sub{font-family:var(--display);font-weight:500;font-size:2.35u;line-height:1.32;color:var(--ink-2);margin-top:1.8u;max-width:70u}
.pt table{width:100%;border-collapse:collapse;table-layout:fixed;margin-top:4u}
.pt th{background:var(--ink);color:var(--paper);font-family:var(--body);font-weight:600;font-size:1.35u;text-align:left;padding:1.1u 1u;line-height:1.1;white-space:nowrap}
.pt td{padding:0 1u;vertical-align:middle;border-bottom:.12u solid var(--line-2);font-size:1.6u;line-height:1.3;color:var(--ink-2)}
.pt tbody tr{height:var(--rowh)}
.pt tbody tr:nth-child(even) td{background:var(--paper-2)}
.pt td.t{font-family:var(--display);font-weight:700;font-size:2.8u;line-height:1;color:var(--ink);white-space:nowrap;font-variant-numeric:lining-nums}
.pt td .n{display:block;font-family:var(--display);font-weight:700;font-size:2.45u;line-height:1.1;color:var(--ink)}
.pt td .x{display:block;font-size:1.4u;color:var(--muted);margin-top:.35u}
.pt td.h span{display:inline-block;border:.14u solid var(--ink-2);border-radius:99u;padding:.3u 1u;font-size:1.3u;font-weight:600;color:var(--ink)}
.pt .how{display:grid;grid-template-columns:repeat(3,1fr);gap:3.4u;margin-top:auto;border-top:.3u solid var(--ink);padding-top:2.1u;flex:none}
.pt .how b{display:block;font-family:var(--display);font-weight:700;font-size:1.95u;line-height:1.15;margin-bottom:.6u}
.pt .how p{font-size:1.45u;line-height:1.4;color:var(--ink-2)}
.pt .foot{display:flex;justify-content:space-between;align-items:baseline;gap:3u;margin-top:2.4u;flex:none;font-size:1.3u;color:var(--muted)}
.pt .credit{font-size:1.05u}
html{--rowh:12.2u}
html.size-tabloid{--rowh:13.8u}
.tv{display:none}
html.size-tv .pt{display:none}
html.size-tv .tv{display:grid}
.tv{grid-template-columns:38u 1fr;background:var(--night);color:var(--paper)}
.tv .now{background:var(--night-2);padding:3.4u 3u 2.4u;display:flex;flex-direction:column;min-width:0}
.tv .club{font-family:var(--display);font-weight:700;font-size:1.5u;line-height:1.1;color:var(--paper)}
.tv .date{font-size:1.05u;color:#c9bfb3;margin-top:.45u}
.tv .chip{align-self:flex-start;margin-top:5.2u;background:var(--ember);color:var(--ink);font-family:var(--display);font-weight:700;font-size:1.15u;line-height:1;padding:.55u 1u;border-radius:var(--r)}
.tv .big{font-family:var(--display);font-weight:800;font-size:8.2u;line-height:.9;letter-spacing:-.03em;margin-top:1.4u;white-space:nowrap}
.tv .nn{font-family:var(--display);font-weight:700;font-size:2.9u;line-height:1.05;margin-top:1.6u}
.tv .meta{display:grid;grid-template-columns:auto 1fr;gap:.5u 1.4u;margin-top:2.2u;font-size:1.12u;line-height:1.3}
.tv .meta dt{color:#c9bfb3}
.tv .meta dd{margin:0;color:var(--paper);font-weight:600}
.tv .rule{margin-top:auto;border-top:.08u solid #5a4a3e;padding-top:1.1u;font-size:.95u;line-height:1.4;color:#c9bfb3}
.tv .list{padding:3.4u 3.4u 2.4u;display:flex;flex-direction:column;min-width:0}
.tv h1{font-family:var(--display);font-weight:800;font-size:3.6u;line-height:1;letter-spacing:-.02em}
.tv ol{margin-top:2.2u;display:flex;flex-direction:column}
.tv li{display:grid;grid-template-columns:9.5u 1fr 14u 8u;align-items:center;gap:1.6u;height:5.3u;border-top:.08u solid #5a4a3e}
.tv li:last-child{border-bottom:.08u solid #5a4a3e}
.tv li .t{font-family:var(--display);font-weight:700;font-size:2.1u;line-height:1;white-space:nowrap}
.tv li .n{font-family:var(--display);font-weight:600;font-size:1.7u;line-height:1.1;min-width:0}
.tv li .s{font-size:1.05u;color:#c9bfb3;min-width:0}
.tv li .r{font-size:1.05u;color:#c9bfb3;text-align:right;white-space:nowrap}
.tv .credit{margin-top:auto;font-size:.62u;color:#8f8277;text-align:right}
"""


def k(i, f):
    return f"s{i}-{f}"


def board_print():
    rows = ""
    for i, (t, n, x, sc, h, m, room, mins) in enumerate(ROWS, 1):
        rows += (f"<tr>"
                 f'<td class="t">{ed("span", "time", esc(t), sync=k(i, "time"))}</td>'
                 f'<td>{ed("span", "session", esc(n), "n", sync=k(i, "name"))}{ed("span", "session-note", esc(x), "x", sync=k(i, "note"))}</td>'
                 f'<td>{ed("span", "scent", esc(sc), sync=k(i, "scent"))}</td>'
                 f'<td class="h">{ed("span", "heat", esc(h), sync=k(i, "heat"))}</td>'
                 f'<td>{ed("span", "sauna-master", esc(m), sync=k(i, "master"))}</td>'
                 f'<td>{ed("span", "room", esc(room), sync=k(i, "room"))}</td>'
                 f'<td>{ed("span", "length", esc(mins), sync=k(i, "len"))}</td></tr>')
    how = "".join(f'<div data-name="how-{j}">{ed("b", "how-title", esc(a))}{ed("p", "how-text", esc(b), multi=True)}</div>'
                  for j, (a, b) in enumerate(HOW, 1))
    return f"""<main class="page pt">
<div class="top">{ed("p", "club-name", "Your Sauna Club", "club", sync="club")}<p class="date"><i></i>{ed("span", "date", "Saturday, December 5", sync="date")}</p></div>
{ed("h1", "title", "Aufguss tonight", sync="title")}
{ed("p", "intro", "Guided steam sessions with our sauna masters. Water and scent go on the hot stones, and a towel moves the heat around the room.", "sub", multi=True)}
<table data-name="schedule"><colgroup><col style="width:15%"><col style="width:26%"><col style="width:15%"><col style="width:10%"><col style="width:12%"><col style="width:13%"><col style="width:9%"></colgroup>
<thead><tr><th>Time</th><th>Session</th><th>Scent</th><th>Heat</th><th>Sauna master</th><th>Room</th><th>Length</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="how">{how}</div>
<div class="foot">{ed("p", "footer-note", "Schedule may change on the day. Ask at the front desk.")}{W.credit()}</div>
</main>"""


def board_tv():
    t, n, x, sc, h, m, room, mins = ROWS[0]
    items = ""
    for i, r in enumerate(ROWS, 1):
        items += (f'<li data-name="row-{i}">{ed("span", "time", esc(r[0]), "t", sync=k(i, "time"))}'
                  f'<span style="min-width:0">{ed("span", "session", esc(r[1]), "n", sync=k(i, "name"))}</span>'
                  f'{ed("span", "scent", esc(r[3]), "s", sync=k(i, "scent"))}{ed("span", "room", esc(r[6]), "r", sync=k(i, "room"))}</li>')
    return f"""<main class="page tv">
<section class="now" data-name="next-panel">
{ed("p", "club-name", "Your Sauna Club", "club", sync="club")}{ed("p", "date", "Saturday, December 5", "date", sync="date")}
{ed("p", "next-label", "Next Aufguss", "chip")}
{ed("p", "next-time", esc(t), "big", sync=k(1, "time"))}
{ed("p", "next-name", esc(n), "nn", sync=k(1, "name"))}
<dl class="meta"><dt>Scent</dt>{ed("dd", "next-scent", esc(sc), sync=k(1, "scent"))}<dt>Heat</dt>{ed("dd", "next-heat", esc(h), sync=k(1, "heat"))}<dt>Room</dt>{ed("dd", "next-room", esc(room), sync=k(1, "room"))}<dt>Length</dt>{ed("dd", "next-length", esc(mins), sync=k(1, "len"))}</dl>
{ed("p", "tv-rule", "The door closes when a session starts. Leave whenever you need to.", "rule", multi=True)}
</section>
<section class="list" data-name="schedule">
{ed("h1", "title", "Aufguss tonight", sync="title")}
<ol>{items}</ol>
{W.credit()}
</section>
</main>"""


def build():
    d = os.path.join(W.ROOT, SLUG)
    html = os.path.join(d, SLUG + ".html")
    W.write(html, W.doc("dvx-aufguss-board-v1", TITLE, DESC, SIZES, "a3", CSS, board_print() + "\n" + board_tv(),
                        note="Print board and TV screen share their fields.", extra_buttons='<button type="button" id="b-full">Full screen</button>'))
    jobs = []
    for key, s in SIZES.items():
        base = f"{SLUG}-{key}"
        jobs.append(dict(id=base, html=html, query=f"size={key}", size=s, title=f"{TITLE} ({s['label']})",
                         pdf=os.path.join(d, base + ".pdf") if s["pdf"] else None,
                         png=[os.path.join(d, base + ".png")] if key == "tv" else [f"/tmp/w3/{base}.png"],
                         svg=[os.path.join(d, base + ".svg")], scale=1))
    jobs.append(dict(id=SLUG + "-edit", kind="edit", html=html, query="size=a3", size=SIZES["a3"], sync="s1-time"))
    jobs.append(dict(id=SLUG + "-edit-tv", kind="edit", html=html, query="size=tv", size=SIZES["tv"], sync="club"))
    return dict(slug=SLUG, jobs=jobs, preview=[f"/tmp/w3/{SLUG}-a3.png", os.path.join(d, SLUG + "-tv.png")])
