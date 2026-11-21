#!/usr/bin/env python3
"""P069 Sauna booking app UI kit: six phone screens (390 x 844) + components + design tokens.

Outputs in templates/sauna-booking-app-ui-kit/:
  screens/<nn>-<name>.svg   one SVG per screen, imports into Figma as a frame
  sauna-booking-ui-kit-sheet.svg   every screen + the component board + color and type specimens
  png/<nn>-<name>.png (2x), sheet.png, preview.png
  tokens.json   W3C design tokens format ($value / $type), works with Tokens Studio
All text is real <text> (Bricolage Grotesque / Inter) so it stays editable after import.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w3s_common as S  # noqa: E402

SLUG = "sauna-booking-app-ui-kit"
OUT = os.path.join(S.ROOT, SLUG)
SW, SH = 390, 844
MX = 16

# ------------------------------------------------------------------ tokens
C = {
    "bg": "#f6f3ee", "surface": "#fffdf9", "surface-2": "#efe9df", "ink": "#1b1512", "ink-2": "#3d332c",
    "muted": "#6f655c", "line": "#e3ddd3", "border": "#857a6f", "accent": "#f0762e", "on-accent": "#1b1512",
    "inverse": "#1b1512", "on-inverse": "#f6f3ee", "success-bg": "#e4efe3", "success": "#2f6b3f",
    "warning-bg": "#fbe3cf", "warning": "#7a3a0c", "neutral-bg": "#ebe6de", "neutral": "#5c534b",
    "danger": "#b3261e", "disabled-bg": "#e3ddd3", "disabled": "#6f655c", "wood": "#d9b683",
}
TYPE = {  # name: (kind, size, line height, weight)
    "display-l": ("display", 32, 36, 700), "display-m": ("display", 28, 32, 700), "title": ("display", 20, 26, 700),
    "body": ("text", 16, 24, 400), "body-strong": ("semi", 16, 24, 600), "label": ("semi", 14, 20, 600),
    "caption": ("text", 13, 18, 400), "button": ("semi", 16, 20, 600), "overline": ("semi", 12, 16, 600),
}
RADIUS = {"sm": 6, "pill": 999}
SPACE = [4, 8, 12, 16, 20, 24, 32, 40, 48]
SIZE = {"touch-target": 44, "button-height": 52, "tab-bar-height": 83, "screen-width": 390, "screen-height": 844}

# text pairs actually used, checked for WCAG contrast (4.5:1 text, 3:1 large text and UI parts)
PAIRS = [("ink", "bg", 4.5), ("ink", "surface", 4.5), ("ink-2", "surface", 4.5), ("muted", "bg", 4.5),
         ("muted", "surface", 4.5), ("muted", "surface-2", 4.5), ("on-accent", "accent", 4.5),
         ("on-inverse", "inverse", 4.5), ("success", "success-bg", 4.5), ("warning", "warning-bg", 4.5),
         ("neutral", "neutral-bg", 4.5), ("danger", "surface", 4.5), ("border", "surface", 3.0),
         ("border", "bg", 3.0), ("ink", "surface-2", 4.5), ("accent", "inverse", 3.0)]


def T(tid, x, y, text, style, fill=None, align="start", w=None):
    kind, size, lh, _ = TYPE[style]
    w = w or (S.width(text, size, kind) / .985 + 4)
    if align == "middle" and w is None:
        pass
    m, _ = S.svg_text(tid, x, y, w, text, size, kind, fill or C["ink"], lh / size, align, maxlines=None)
    return m


def T1(tid, x, y, text, style, fill=None, align="start"):
    """Single line. x is the left edge, the centre or the right edge, like text-anchor."""
    kind, size, lh, _ = TYPE[style]
    w = S.width(text, size, kind) / .985 + 4
    x0 = {"start": x, "middle": x - w / 2, "end": x - w}[align]
    m, _ = S.svg_text(tid, x0, y, w, text, size, kind, fill or C["ink"], lh / size, align, maxlines=1)
    return m


def rect(x, y, w, h, fill, r=0, stroke=None, sw=1, rid=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    i = f' id="{rid}"' if rid else ""
    return f'<rect{i} x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"{st}/>'


def g(gid, *parts):
    return f'<g id="{gid}">' + "".join(parts) + "</g>"


# ------------------------------------------------------------------ small icons (24 px, stroked)
def ico(name, x, y, color, s=24):
    k = s / 24
    d = {
        "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/>',
        "ticket": '<path d="M4 6.5h16v3.2a2.3 2.3 0 0 0 0 4.6v3.2H4v-3.2a2.3 2.3 0 0 0 0-4.6z"/><path d="M14 7v10" stroke-dasharray="1.6 2"/>',
        "user": '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c.9-3.9 3.9-6 7.5-6s6.6 2.1 7.5 6"/>',
        "chev-r": '<path d="M9.5 6l6 6-6 6"/>', "chev-l": '<path d="M14.5 6l-6 6 6 6"/>',
        "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
        "check": '<path d="M5.5 12.5l4.2 4.2 8.8-9.4"/>', "minus": '<path d="M6 12h12"/>', "plus": '<path d="M6 12h12M12 6v12"/>',
        "people": '<circle cx="9" cy="9" r="3.2"/><path d="M3.5 19c.7-3.2 3-5 5.5-5s4.8 1.8 5.5 5"/><circle cx="16.5" cy="8.5" r="2.6"/><path d="M15.5 13.6c2.4.1 4.4 1.8 5 4.9"/>',
        "drop": '<path d="M12 3.5c3.2 4.2 5.5 7.4 5.5 10.2a5.5 5.5 0 0 1-11 0c0-2.8 2.3-6 5.5-10.2z"/>',
        "flame": '<path d="M12 3c.6 3.4 4.8 5.1 4.8 10a4.8 4.8 0 0 1-9.6 0c0-2.3 1.1-3.8 2.2-5 .2 1.6 1 2.4 1.8 2.8C10.6 7.9 11 5.2 12 3z"/>',
        "bell": '<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 1.5h-15z"/><path d="M10 20.5h4"/>',
        "card": '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3 9.5h18M6.5 15h4"/>',
        "help": '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.6a2.5 2.5 0 1 1 3.4 2.3c-.7.3-1 .8-1 1.5v.6"/><path d="M12 16.8v.2"/>',
        "out": '<path d="M14 4.5H6.5v15H14M10.5 12H20M16.5 8.5 20 12l-3.5 3.5"/>',
        "cal-plus": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4M12 12.5v5M9.5 15h5"/>',
    }[name]
    return (f'<g transform="translate({x:g} {y:g}) scale({k:g})" fill="none" stroke="{color}" stroke-width="{1.8 / k * k:g}" '
            f'stroke-linecap="round" stroke-linejoin="round">{d}</g>')


# ------------------------------------------------------------------ components
def status_bar(dark=False):
    c = C["ink"]
    return g("status-bar", T1("status-time", 30, 14, "9:41", "label", c),
             f'<g transform="translate(300 18)" fill="{c}"><rect x="0" y="7" width="3" height="5" rx="1"/><rect x="5" y="5" width="3" height="7" rx="1"/>'
             f'<rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="1" width="3" height="11" rx="1"/>'
             f'<rect x="26" y="0.5" width="24" height="12" rx="3.5" fill="none" stroke="{c}" stroke-opacity=".5"/>'
             f'<rect x="28" y="2.5" width="17" height="8" rx="2"/><rect x="51.5" y="4.5" width="1.6" height="4" rx=".8" opacity=".5"/></g>')


def home_indicator():
    return rect(SW / 2 - 67, SH - 13, 134, 5, C["ink"], 2.5, rid="home-indicator")


def button(bid, x, y, w, label, kind="primary", icon=None):
    h = 52
    bg, fg, st = {"primary": (C["accent"], C["on-accent"], None), "secondary": (C["surface"], C["ink"], C["ink"]),
                  "ghost": ("none", C["ink"], None), "disabled": (C["disabled-bg"], C["disabled"], None),
                  "inverse": (C["inverse"], C["on-inverse"], None)}[kind]
    parts = [rect(x, y, w, h, bg, RADIUS["sm"], st, 1.5 if st else 1)]
    lw = S.width(label, 16, "semi")
    if icon:
        ix = x + w / 2 - (lw + 32) / 2
        parts.append(ico(icon, ix, y + 14, fg))
        parts.append(T1(bid + "-label", ix + 32, y + 16, label, "button", fg))
    else:
        parts.append(T1(bid + "-label", x + w / 2, y + 16, label, "button", fg, "middle"))
    if kind == "ghost":
        parts.append(f'<path d="M{x + w / 2 - lw / 2:.1f} {y + 37}h{lw:.1f}" stroke="{fg}" stroke-width="1.5"/>')
    return g(bid, *parts)


def badge(bid, x, y, label, kind="success", align="start"):
    bg, fg = {"success": (C["success-bg"], C["success"]), "warning": (C["warning-bg"], C["warning"]),
              "neutral": (C["neutral-bg"], C["neutral"]), "inverse": (C["inverse"], C["on-inverse"]),
              "outline": ("none", C["ink"])}[kind]
    w = S.width(label, 12, "semi") + 20
    x0 = x - w if align == "end" else x
    st = C["border"] if kind == "outline" else None
    return g(bid, rect(x0, y, w, 24, bg, 12, st), T1(bid + "-label", x0 + w / 2, y + 4, label, "overline", fg, "middle"))


def slot_card(cid, x, y, w, time, sub, state, tag=None):
    """state: available (n spots) / few (n left) / full."""
    h = 84
    full = state[0] == "full"
    parts = [rect(x, y, w, h, C["surface"] if not full else C["surface-2"], RADIUS["sm"], C["line"])]
    tc = C["ink"] if not full else C["muted"]
    parts.append(T1(cid + "-time", x + 16, y + 16, time, "body-strong", tc))
    parts.append(T1(cid + "-sub", x + 16, y + 44, sub, "caption", C["muted"]))
    if tag:
        tw = S.width(time, 16, "semi")
        parts.append(badge(cid + "-tag", x + 16 + tw + 10, y + 16, tag, "outline"))
    n = state[1] if len(state) > 1 else 0
    lab, kind = {"available": (f"{n} spots", "success"), "few": (f"{n} left", "warning"),
                 "full": ("Full", "neutral")}[state[0]]
    parts.append(badge(cid + "-badge", x + w - 44, y + 30, lab, kind, "end"))
    parts.append(ico("chev-r", x + w - 36, y + 30, C["muted"]))
    return g(cid, *parts)


DAYS = [("Mon", 8), ("Tue", 9), ("Wed", 10), ("Thu", 11), ("Fri", 12), ("Sat", 13), ("Sun", 14)]


def day_chips(x, y, sel=1, closed=(0,)):
    parts = []
    cw, gap = 46, 6
    for i, (d, n) in enumerate(DAYS):
        cx = x + i * (cw + gap)
        if i == sel:
            bg, fg, st = C["inverse"], C["on-inverse"], None
        elif i in closed:
            bg, fg, st = C["surface-2"], C["muted"], None
        else:
            bg, fg, st = C["surface"], C["ink"], C["line"]
        parts.append(g(f"chip-{d.lower()}", rect(cx, y, cw, 64, bg, RADIUS["sm"], st),
                       T1(f"chip-{d.lower()}-day", cx + cw / 2, y + 10, d, "caption", fg if i == sel else C["muted"] if i not in closed else C["muted"], "middle"),
                       T1(f"chip-{d.lower()}-date", cx + cw / 2, y + 30, str(n), "title", fg, "middle")))
    return g("day-chips", *parts)


def tab_bar(active=0):
    y = SH - 83
    parts = [rect(0, y, SW, 83, C["surface"]), f'<path d="M0 {y}H{SW}" stroke="{C["line"]}"/>']
    tabs = [("Book", "calendar"), ("My bookings", "ticket"), ("Profile", "user")]
    tw = SW / 3
    for i, (lab, ic) in enumerate(tabs):
        cx = tw * i + tw / 2
        col = C["ink"] if i == active else C["muted"]
        parts.append(g(f"tab-{lab.lower().replace(' ', '-')}", rect(tw * i, y, tw, 56, "none"), ico(ic, cx - 12, y + 9, col),
                       T1(f"tab-{i}-label", cx, y + 34, lab, "overline", col, "middle")))
        if i == active:
            parts.append(rect(cx - 14, y + 1, 28, 3, C["accent"], 1.5, rid="tab-active-marker"))
    return g("tab-bar", *parts, home_indicator())


def field(fid, x, y, w, label, value, state="default", placeholder=False, help_=None):
    parts = [T1(fid + "-label", x, y, label, "label", C["ink"])]
    stc, sw = {"default": (C["border"], 1), "focus": (C["ink"], 2), "error": (C["danger"], 2)}[state]
    parts.append(rect(x, y + 26, w, 48, C["surface"], RADIUS["sm"], stc, sw))
    parts.append(T1(fid + "-value", x + 14, y + 38, value, "body", C["muted"] if placeholder else C["ink"]))
    if state == "focus":
        vw = S.width(value, 16, "text")
        parts.append(rect(x + 15 + vw, y + 39, 1.5, 22, C["ink"]))
    if help_:
        parts.append(T1(fid + "-help", x, y + 80, help_, "caption", C["danger"] if state == "error" else C["muted"]))
    return g(fid, *parts)


def stepper(sid, x, y, value):
    return g(sid, rect(x, y, 44, 44, C["surface"], RADIUS["sm"], C["border"]), ico("minus", x + 10, y + 10, C["ink"]),
             T1(sid + "-value", x + 72, y + 10, str(value), "body-strong", C["ink"], "middle"),
             rect(x + 100, y, 44, 44, C["surface"], RADIUS["sm"], C["border"]), ico("plus", x + 110, y + 10, C["ink"]))


def toggle(tid, x, y, on=True):
    return g(tid, rect(x, y, 52, 32, C["inverse"] if on else C["surface-2"], 16, None if on else C["border"]),
             f'<circle cx="{x + (36 if on else 16)}" cy="{y + 16}" r="12" fill="{C["on-inverse"] if on else C["surface"]}"'
             f'{"" if on else " stroke=" + chr(34) + C["border"] + chr(34)}/>')


def segmented(x, y, w, items, sel=0):
    parts = [rect(x, y, w, 44, C["surface-2"], RADIUS["sm"])]
    sw = (w - 8) / len(items)
    for i, it in enumerate(items):
        sx = x + 4 + i * sw
        if i == sel:
            parts.append(rect(sx, y + 4, sw, 36, C["surface"], RADIUS["sm"] - 2, C["line"]))
        parts.append(T1(f"seg-{it.lower()}", sx + sw / 2, y + 12, it, "label", C["ink"] if i == sel else C["muted"], "middle"))
    return g("segmented-control", *parts)


def header(title, kicker=None, back=False):
    parts = []
    y = 60
    if back:
        parts.append(g("back-button", rect(MX - 6, 52, 44, 44, "none"), ico("chev-l", MX + 4, 62, C["ink"])))
        y = 104
    if kicker:
        parts.append(T1("header-kicker", MX, y, kicker, "label", C["muted"]))
        y += 24
    parts.append(T1("header-title", MX, y, title, "display-m", C["ink"]))
    return g("header", *parts), y + 32


def screen(sid, label, *parts, bg=None):
    return dict(id=sid, label=label, body=rect(0, 0, SW, SH, bg or C["bg"], rid="background") + status_bar() + "".join(parts))


# ------------------------------------------------------------------ screens
def screens():
    out = []
    w = SW - 2 * MX
    # 1 slots
    hd, y = header("Book a session", "Your Sauna Club")
    cards = [("4:00–5:30 pm", "Sauna + cold plunge · 90 min", ("available", 8), None),
             ("5:30–7:00 pm", "Sauna + cold plunge · 90 min", ("few", 2), None),
             ("7:00–8:30 pm", "Sauna + cold plunge · 90 min", ("full",), "Aufguss"),
             ("8:30–10:00 pm", "Sauna + cold plunge · 90 min", ("available", 10), None)]
    cy = y + 140
    cc = [slot_card(f"slot-{i + 1}", MX, cy + i * 96, w, *c) for i, c in enumerate(cards)]
    out.append(screen("screen-01-slots", "Slots by day", hd, day_chips(MX, y + 18),
                      T1("section-label", MX, cy - 30, "Tuesday, Dec 9 · Evening", "label", C["ink-2"]), *cc, tab_bar(0)))

    # 2 booking a slot
    hd, y = header("Evening sauna", None, back=True)
    det_y = y + 44
    rows = [("clock", "90 minutes"), ("flame", "Sauna, cold plunge and tea"), ("people", "Up to 12 people")]
    det = [rect(MX, det_y, w, 152, C["surface"], RADIUS["sm"], C["line"])]
    for i, (ic, txt) in enumerate(rows):
        ry = det_y + 16 + i * 40
        det.append(ico(ic, MX + 16, ry + 2, C["ink-2"]))
        det.append(T1(f"detail-{i + 1}", MX + 52, ry + 2, txt, "body", C["ink"]))
    det.append(badge("detail-spots", MX + w - 16, det_y + 18, "2 left", "warning", "end"))
    gy = det_y + 176
    form = [T1("guests-label", MX, gy + 12, "Guests", "body-strong"), stepper("guests", MX + w - 144, gy, 1),
            field("field-name", MX, gy + 68, w, "Name", "Alex", "focus"),
            field("field-email", MX, gy + 160, w, "Email", "alex@example.com", "default", True),
            T("note", MX, gy + 252, "Bring two towels and a water bottle.", "caption", C["muted"], w=w)]
    bar_y = SH - 118
    bottom = [rect(0, bar_y, SW, 118, C["surface"]), f'<path d="M0 {bar_y}H{SW}" stroke="{C["line"]}"/>',
              T1("price", MX, bar_y + 18, "$25", "title"), T1("price-note", MX, bar_y + 46, "per person", "caption", C["muted"]),
              button("book-button", MX + 130, bar_y + 16, w - 130, "Book · $25"), home_indicator()]
    out.append(screen("screen-02-booking", "Book a slot", hd,
                      T1("slot-when", MX, y + 6, "Tue, Dec 9 · 5:30–7:00 pm", "body", C["ink-2"]),
                      g("details-card", *det), g("booking-form", *form), g("bottom-bar", *bottom)))

    # 3 confirmation
    cy = 150
    conf = [f'<circle id="success-circle" cx="{SW / 2}" cy="{cy + 40}" r="40" fill="{C["inverse"]}"/>',
            ico("check", SW / 2 - 20, cy + 20, C["on-inverse"], 40),
            T1("conf-title", SW / 2, cy + 104, "You’re booked", "display-l", C["ink"], "middle"),
            T1("conf-sub", SW / 2, cy + 148, "We sent the details to alex@example.com.", "body", C["ink-2"], "middle")]
    sy = cy + 200
    summ = [rect(MX, sy, w, 224, C["surface"], RADIUS["sm"], C["line"])]
    for i, (k, v) in enumerate([("Session", "Evening sauna"), ("Date", "Tue, Dec 9"), ("Time", "5:30–7:00 pm"),
                                ("Guests", "1"), ("Booking code", "SC-0000")]):
        ry = sy + 14 + i * 42
        summ.append(T1(f"sum-{i}-k", MX + 16, ry + 6, k, "body", C["muted"]))
        summ.append(T1(f"sum-{i}-v", MX + w - 16, ry + 6, v, "body-strong", C["ink"], "end"))
        if i < 4:
            summ.append(f'<path d="M{MX + 16} {ry + 41}H{MX + w - 16}" stroke="{C["line"]}"/>')
    by = SH - 190
    out.append(screen("screen-03-confirmation", "Booking confirmed", *conf, g("summary-card", *summ),
                      button("calendar-button", MX, by, w, "Add to calendar", "secondary", "cal-plus"),
                      button("done-button", MX, by + 64, w, "Done"),
                      T1("conf-note", SW / 2, by + 132, "You can cancel from My bookings.", "caption", C["muted"], "middle"),
                      home_indicator()))

    # 4 my bookings
    hd, y = header("My bookings")
    seg = segmented(MX, y + 18, w, ["Upcoming", "Past"])
    lst = []
    items = [("Tue", "9", "Evening sauna", "5:30–7:00 pm · 1 guest", None),
             ("Fri", "12", "Aufguss evening", "7:00–8:30 pm · 2 guests", "Aufguss")]
    for i, (dw, dn, ttl, sub, tag) in enumerate(items):
        ly = y + 86 + i * 128
        lst.append(g(f"booking-{i + 1}", rect(MX, ly, w, 116, C["surface"], RADIUS["sm"], C["line"]),
                     rect(MX + 16, ly + 16, 56, 64, C["surface-2"], RADIUS["sm"]),
                     T1(f"booking-{i + 1}-dow", MX + 44, ly + 24, dw, "caption", C["muted"], "middle"),
                     T1(f"booking-{i + 1}-day", MX + 44, ly + 42, dn, "title", C["ink"], "middle"),
                     T1(f"booking-{i + 1}-title", MX + 88, ly + 18, ttl, "body-strong"),
                     T1(f"booking-{i + 1}-sub", MX + 88, ly + 44, sub, "caption", C["muted"]),
                     *( [badge(f"booking-{i + 1}-tag", MX + 88, ly + 70, tag, "outline")] if tag else []),
                     g(f"booking-{i + 1}-cancel", rect(MX + w - 96, ly + 64, 84, 44, "none"),
                       T1(f"booking-{i + 1}-cancel-label", MX + w - 16, ly + 76, "Cancel", "label", C["danger"], "end"))))
    out.append(screen("screen-04-my-bookings", "My bookings", hd, seg, *lst, tab_bar(1)))

    # 5 profile
    hd, y = header("Profile")
    py = y + 20
    prof = [f'<circle cx="{MX + 32}" cy="{py + 32}" r="32" fill="{C["surface-2"]}"/>',
            T1("avatar-initial", MX + 32, py + 16, "A", "title", C["ink"], "middle"),
            T1("profile-name", MX + 80, py + 8, "Alex", "title"),
            T1("profile-email", MX + 80, py + 36, "alex@example.com", "caption", C["muted"])]
    my = py + 88
    pass_card = [rect(MX, my, w, 120, C["inverse"], RADIUS["sm"]),
                 T1("pass-kicker", MX + 16, my + 16, "Membership", "overline", C["on-inverse"]),
                 T1("pass-name", MX + 16, my + 36, "10-session pass", "title", C["on-inverse"]),
                 T1("pass-left", MX + w - 16, my + 40, "7 of 10 left", "label", C["on-inverse"], "end"),
                 rect(MX + 16, my + 84, w - 32, 8, "#4a3426", 4), rect(MX + 16, my + 84, (w - 32) * .7, 8, C["accent"], 4)]
    sy = my + 144
    rows = [("bell", "Reminders", "toggle"), ("card", "Payment methods", "chev"), ("help", "Help and house rules", "chev"),
            ("out", "Sign out", None)]
    st = []
    for i, (ic, lab, end) in enumerate(rows):
        ry = sy + i * 56
        st.append(g(f"setting-{i + 1}", rect(MX, ry, w, 56, "none"), ico(ic, MX, ry + 16, C["ink-2"]),
                    T1(f"setting-{i + 1}-label", MX + 40, ry + 16, lab, "body"),
                    toggle(f"setting-{i + 1}-toggle", MX + w - 52, ry + 12) if end == "toggle" else
                    (ico("chev-r", MX + w - 24, ry + 16, C["muted"]) if end == "chev" else ""),
                    f'<path d="M{MX + 40} {ry + 56}H{MX + w}" stroke="{C["line"]}"/>' if i < 3 else ""))
    out.append(screen("screen-05-profile", "Profile and membership", hd, g("profile-head", *prof), g("pass-card", *pass_card),
                      g("settings", *st), tab_bar(2)))

    # 6 empty state
    hd, y = header("My bookings")
    seg = segmented(MX, y + 18, w, ["Upcoming", "Past"])
    ey = y + 110
    out.append(screen("screen-06-empty", "Empty state", hd, seg,
                      S.illustration("bucket-and-ladle", SW / 2 - 100, ey, 200, "empty-illustration"),
                      T1("empty-title", SW / 2, ey + 220, "No bookings yet", "title", C["ink"], "middle"),
                      T("empty-text", 32, ey + 254, "Pick a session and it will show up here.", "body", C["ink-2"], "middle", w=SW - 64),
                      button("find-button", 64, ey + 310, SW - 128, "Find a session"), tab_bar(1)))
    return out


# ------------------------------------------------------------------ component board
def board(x0, y0):
    """Returns (markup, width, height)."""
    p = []
    col = lambda i: x0 + i * 440

    def head(i, y, txt):
        p.append(T1(f"board-head-{txt.lower().replace(' ', '-')}", col(i), y, txt, "title", C["ink"]))

    # buttons
    head(0, y0, "Buttons")
    for i, k in enumerate(["primary", "secondary", "ghost", "disabled", "inverse"]):
        p.append(button(f"button-{k}", col(0), y0 + 44 + i * 68, 300, {"primary": "Book · $25", "secondary": "Add to calendar",
                                                                       "ghost": "View rules", "disabled": "Full",
                                                                       "inverse": "Join waitlist"}[k], k))
        p.append(T1(f"button-{k}-name", col(0) + 316, y0 + 60 + i * 68, k, "caption", C["muted"]))
    # badges + chips + stepper + toggles
    head(1, y0, "Badges and controls")
    for i, (lab, k) in enumerate([("8 spots", "success"), ("2 left", "warning"), ("Full", "neutral"), ("Aufguss", "outline"), ("Member", "inverse")]):
        p.append(badge(f"badge-{k}", col(1) + i * 80, y0 + 48, lab, k))
    p.append(g("day-chip-states", *[g(f"chip-state-{n}", rect(col(1) + j * 58, y0 + 96, 46, 64, bg, RADIUS["sm"], st),
                                       T1(f"chip-state-{n}-d", col(1) + j * 58 + 23, y0 + 106, "Tue", "caption", fc if n == "selected" else C["muted"], "middle"),
                                       T1(f"chip-state-{n}-n", col(1) + j * 58 + 23, y0 + 126, "9", "title", fc, "middle"))
                                     for j, (n, bg, fc, st) in enumerate([("default", C["surface"], C["ink"], C["line"]),
                                                                          ("selected", C["inverse"], C["on-inverse"], None),
                                                                          ("closed", C["surface-2"], C["muted"], None)])]))
    p.append(T1("chip-states-note", col(1) + 182, y0 + 116, "Day chip: default, selected, closed", "caption", C["muted"]))
    p.append(stepper("stepper", col(1), y0 + 184, 2))
    p.append(toggle("toggle-on", col(1) + 176, y0 + 190, True))
    p.append(toggle("toggle-off", col(1) + 244, y0 + 190, False))
    p.append(segmented(col(1), y0 + 252, 300, ["Upcoming", "Past"]))
    # inputs
    head(2, y0, "Inputs")
    p.append(field("input-default", col(2), y0 + 44, 300, "Email", "alex@example.com", "default", True))
    p.append(field("input-focus", col(2), y0 + 134, 300, "Name", "Alex", "focus"))
    p.append(field("input-error", col(2), y0 + 224, 300, "Phone", "555 01", "error", help_="Enter a full phone number."))
    # slot cards
    y1 = y0 + 430
    head(0, y1, "Slot cards")
    for i, (st, tag) in enumerate([(("available", 8), None), (("few", 2), None), (("full",), "Aufguss")]):
        p.append(slot_card(f"slot-card-{st[0]}", col(0) + i * 440, y1 + 44, 358, "5:30–7:00 pm", "Sauna + cold plunge · 90 min", st, tag))
    # tab bar sample
    y2 = y1 + 160
    head(0, y2, "Tab bar")
    p.append(f'<g id="tab-bar-sample" transform="translate({col(0)} {y2 + 44 - (SH - 83)})">{tab_bar(0)}</g>')
    # colors
    left_end = y2 + 44 + 83
    y3 = y0
    RX = x0 + 1440
    p.append(T1("board-head-color-tokens", RX, y3, "Color tokens", "title", C["ink"]))
    for i, (k, v) in enumerate(C.items()):
        cx, cy = RX + (i % 7) * 175, y3 + 44 + (i // 7) * 84
        p.append(g(f"swatch-{k}", rect(cx, cy, 44, 44, v, RADIUS["sm"], C["line"]),
                   T1(f"swatch-{k}-name", cx + 54, cy + 2, k, "label", C["ink"]),
                   T1(f"swatch-{k}-hex", cx + 54, cy + 22, v, "caption", C["muted"])))
    rows = -(-len(C) // 7)
    # type
    y4 = y3 + 44 + rows * 84 + 30
    p.append(T1("board-head-type", RX, y4, "Type", "title", C["ink"]))
    yy = y4 + 44
    for k, (kind, size, lh, wt) in TYPE.items():
        fam = "Bricolage Grotesque" if kind == "display" else "Inter"
        p.append(T1(f"type-{k}", RX, yy, "Evening sauna, 5:30 pm", k, C["ink"]))
        p.append(T1(f"type-{k}-spec", RX + 520, yy + max(0, (lh - 18) / 2), f"{k} · {fam} {wt} · {size}/{lh}", "caption", C["muted"]))
        yy += lh + 14
    return "".join(p), 2660, max(yy, left_end) - y0


def tokens():
    def col(v):
        return {"$type": "color", "$value": v}
    t = {"color": {k: col(v) for k, v in C.items()},
         "font": {"family": {"display": {"$type": "fontFamily", "$value": ["Bricolage Grotesque", "Arial Narrow", "sans-serif"]},
                             "body": {"$type": "fontFamily", "$value": ["Inter", "Arial", "sans-serif"]}}},
         "typography": {}, "radius": {k: {"$type": "dimension", "$value": f"{v}px"} for k, v in RADIUS.items()},
         "space": {str(v): {"$type": "dimension", "$value": f"{v}px"} for v in SPACE},
         "size": {k: {"$type": "dimension", "$value": f"{v}px"} for k, v in SIZE.items()},
         "$description": "Sauna booking app UI kit by DIVELUX (https://diveluxsaunahat.com), CC BY 4.0. "
                         "Format: W3C Design Tokens Community Group draft ($value / $type)."}
    for k, (kind, size, lh, wt) in TYPE.items():
        t["typography"][k] = {"$type": "typography", "$value": {
            "fontFamily": "{font.family.display}" if kind == "display" else "{font.family.body}",
            "fontWeight": wt, "fontSize": f"{size}px", "lineHeight": f"{lh}px", "letterSpacing": "0px"}}
    return t


def wrap_svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<title>{S.esc(title)}</title>{body}</svg>')


def main():
    for d in ("screens", "png"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    bad = 0
    for a, b, need in PAIRS:
        r = S.contrast(C[a], C[b])
        ok = r >= need
        bad += not ok
        print(f"contrast {a:10} on {b:11} {r:5.2f}:1 (needs {need}) {'OK' if ok else 'FAIL'}")
    if bad:
        raise SystemExit("contrast failures")
    scr = screens()
    from PIL import Image
    for s in scr:
        svg = wrap_svg(SW, SH, s["body"], f'{s["label"]} — sauna booking app UI kit by DIVELUX (CC BY 4.0)')
        S.write(os.path.join(OUT, "screens", s["id"].replace("screen-", "") + ".svg"), svg)
        png = os.path.join(OUT, "png", s["id"].replace("screen-", "") + ".png")
        S.render(svg, png, zoom=2)
        Image.open(png).convert("RGB").save(png, optimize=True)
    # sheet
    pad, gap = 80, 64
    top = 230
    W = pad * 2 + len(scr) * SW + (len(scr) - 1) * gap
    parts = [rect(0, 0, 1, 1, "none")]
    parts.append(T1("sheet-title", pad, 70, "Sauna booking app UI kit", "display-l", C["ink"]))
    parts.append(T1("sheet-sub", pad, 118, "Six screens at 390 × 844, components and tokens. Fonts: Bricolage Grotesque and Inter. "
                                            "Sample data only: replace names, times and prices with your own.", "body", C["ink-2"]))
    parts.append(T1("sheet-credit", W - pad, 78, "UI kit by DIVELUX · diveluxsaunahat.com · CC BY 4.0", "caption", C["muted"], "end"))
    for i, s in enumerate(scr):
        x = pad + i * (SW + gap)
        parts.append(T1(f"label-{s['id']}", x, top - 40, f"{i + 1:02d} {s['label']}", "label", C["ink-2"]))
        parts.append(f'<g id="{s["id"]}" transform="translate({x} {top})">{s["body"]}'
                     f'<rect width="{SW}" height="{SH}" fill="none" stroke="{C["line"]}"/></g>')
    by = top + SH + 110
    bm, bw, bh = board(pad, by)
    parts.append(f'<path d="M{pad} {by - 50}H{W - pad}" stroke="{C["ink"]}" stroke-width="2"/>')
    parts.append(g("components", bm))
    H = by + bh + 80
    sheet = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}">'
             f'<title>Sauna booking app UI kit by DIVELUX (CC BY 4.0)</title>'
             f'<rect id="sheet-background" width="{W}" height="{H:.0f}" fill="{C["surface-2"]}"/>' + "".join(parts) + "</svg>")
    S.write(os.path.join(OUT, "sauna-booking-ui-kit-sheet.svg"), sheet)
    S.render(sheet, os.path.join(OUT, "png", "sheet.png"))
    Image.open(os.path.join(OUT, "png", "sheet.png")).convert("RGB").save(os.path.join(OUT, "png", "sheet.png"), optimize=True)
    # preview: first four screens, 2x, on the sheet color
    ims = [Image.open(os.path.join(OUT, "png", s["id"].replace("screen-", "") + ".png")) for s in scr[:4]]
    pw, ph, gg = 390, 844, 40
    pv = Image.new("RGB", (4 * pw + 5 * gg, ph + 2 * gg), C["surface-2"])
    for i, im in enumerate(ims):
        pv.paste(im.resize((pw, ph), Image.LANCZOS), (gg + i * (pw + gg), gg))
    pv.save(os.path.join(OUT, "preview.png"), optimize=True)
    json.dump(tokens(), open(os.path.join(OUT, "tokens.json"), "w"), indent=2)
    print("sheet", W, round(H))


if __name__ == "__main__":
    main()
