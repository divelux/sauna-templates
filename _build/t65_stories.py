#!/usr/bin/env python3
"""P065 Sauna club social stories: 8 story templates, 1080 x 1920.

One description per story drives three outputs, so they always match:
  svg/<n>-<name>.svg   real <text> (editable in Figma, Illustrator, Inkscape), groups with readable ids
  png/<n>-<name>.png   1080 x 1920, rendered from the SVG with resvg
  sauna-club-stories.html   all eight as editable artboards (contenteditable, saved in localStorage, print = PDF)

Layout model: a story = background + art (plain SVG shapes) + "stacks" of text items. A stack has a left x,
a width and a top (or bottom) anchor; items flow down inside it. In the SVG the flow is computed here with the
real font metrics; in the HTML the same stack is a flex column, so edited text reflows instead of overlapping.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w3s_common as S  # noqa: E402

SLUG = "sauna-club-social-stories"
OUT = os.path.join(S.ROOT, SLUG)
W, H = 1080, 1920
SAFE_TOP, SAFE_BOTTOM = 250, 250
M = 96
CW = W - 2 * M
P = S.PAL

# ---------------------------------------------------------------- item constructors


def T(tid, text, size, kind="text", fill=None, lh=1.3, gap=0, align="start", tracking=0.0):
    return dict(t="text", id=tid, text=text, size=size, kind=kind, fill=fill, lh=lh, gap=gap, align=align, tracking=tracking)


def BTN(tid, text, bg, fg, size=44, gap=0, wfull=False):
    return dict(t="btn", id=tid, text=text, size=size, bg=bg, fg=fg, gap=gap, wfull=wfull)


def ROW(tid, left, right, size=40, fill=None, line=None, gap=0, lkind="semi", rkind="text"):
    return dict(t="row", id=tid, left=left, right=right, size=size, fill=fill, line=line, gap=gap, lkind=lkind, rkind=rkind)


def CHECK(tid, text, size=40, fill=None, box=None, gap=0):
    return dict(t="check", id=tid, text=text, size=size, fill=fill, box=box, gap=gap)


def NUM(tid, n, text, size=40, fill=None, line=None, gap=0):
    return dict(t="num", id=tid, n=n, text=text, size=size, fill=fill, line=line, gap=gap)


def SP(h):
    return dict(t="space", h=h)


ROW_PAD = 22      # vertical padding of a row / numbered item
BTN_PADY, BTN_PADX = 30, 56

# ---------------------------------------------------------------- the eight stories
CLUB = "Your Sauna Club"
HANDLE = "@yoursaunaclub"


def club(fill, sub=None):
    """Top line inside the safe zone: club name + optional small label on the right."""
    items = [dict(stack="club", x=M, top=SAFE_TOP + 4, w=CW, items=[ROW("club-name", CLUB, sub or HANDLE, 32, fill, None,
                                                                         lkind="semi", rkind="text")])]
    return items


def stories():
    ink, paper, muted = P["ink"], P["paper"], P["muted"]
    night_text, night_muted = P["paper"], P["nightmuted"]
    out = []

    # 1 session announcement
    out.append(dict(
        name="session-announcement", label="Session announcement", bg=paper,
        art=[S.illustration("lakeside-sauna", 210, 330, 660, "art-lakeside-sauna")],
        stacks=club(ink, "Sauna session") + [dict(stack="main", x=M, bottom=H - SAFE_BOTTOM - 10, w=CW, items=[
            T("kicker", "This Saturday", 40, "semi", P["ink2"], gap=18),
            T("title", "Sauna Night by the Lake", 124, "display", ink, lh=.94, gap=34, tracking=-.015),
            ROW("when", "Sat, Dec 6", "6:00–9:00 pm", 44, ink, P["line2"], gap=26),
            T("details", "Wood-fired sauna, cold plunge and hot tea by the fire. Bring two towels.", 40, "text", P["ink2"], gap=44),
            BTN("cta", "Book your spot", P["ember"], ink),
        ])]))

    # 2 sauna rules
    rules = ["Shower before you go in.", "Sit on a towel, always.", "Ask before you pour water on the stones.",
             "Keep voices low. Phones stay outside.", "No alcohol before or in the sauna.",
             "Feel unwell? Leave the heat right away."]
    out.append(dict(
        name="sauna-rules", label="Sauna rules", bg=P["card"],
        art=[f'<rect id="band" x="0" y="0" width="{W}" height="{SAFE_TOP + 440}" fill="{P["paper2"]}"/>'],
        stacks=club(ink, "House rules") + [
            dict(stack="head", x=M, top=SAFE_TOP + 120, w=CW, items=[
                T("title", "Sauna rules", 168, "display", ink, lh=.92, tracking=-.02)]),
            dict(stack="list", x=M, top=SAFE_TOP + 470, w=CW, items=[
                NUM(f"rule-{i}", i, r, 46, ink, P["line"]) for i, r in enumerate(rules, 1)] + [
                SP(40), T("thanks", "Thank you for keeping this a calm, friendly place.", 38, "text", muted)])]))

    # 3 Aufguss tonight
    out.append(dict(
        name="aufguss-tonight", label="Aufguss tonight", bg=P["night"],
        art=[S.illustration("sauna-stove", 300, 300, 480, "art-sauna-stove"),
             f'<circle id="marker" cx="{M + 13}" cy="{SAFE_TOP + 546}" r="13" fill="{P["ember"]}"/>'],
        stacks=club(night_text, "Tonight") + [
            dict(stack="kick", x=M + 44, top=SAFE_TOP + 520, w=CW - 44, items=[
                T("kicker", "Steam ceremony", 40, "semi", night_text)]),
            dict(stack="main", x=M, top=SAFE_TOP + 585, w=CW, items=[
            T("title", "Aufguss tonight", 140, "display", night_text, lh=.92, gap=40, tracking=-.02),
            ROW("round-1", "7:00 pm", "Birch", 48, night_text, P["nightline"]),
            ROW("round-2", "8:00 pm", "Eucalyptus", 48, night_text, P["nightline"]),
            ROW("round-3", "9:00 pm", "Citrus", 48, night_text, P["nightline"], gap=34),
            T("master", "Sauna master: [Name]", 40, "semi", night_text, gap=18),
            T("note", "Come in five minutes early. The door stays closed during each round. Step out any time you need to.",
              36, "text", night_muted)])]))

    # 4 weekly schedule
    week = [("Mon", "Closed"), ("Tue", "4–9 pm"), ("Wed", "4–9 pm · Aufguss 7 pm"), ("Thu", "4–9 pm"),
            ("Fri", "4–10 pm · Aufguss 8 pm"), ("Sat", "9 am – 10 pm"), ("Sun", "9 am – 6 pm · Women only 9–11")]
    out.append(dict(
        name="weekly-schedule", label="Weekly schedule", bg=paper,
        art=[S.illustration("timer-and-thermometer", 690, SAFE_TOP + 40, 330, "art-timer")],
        stacks=club(ink, "Schedule") + [
            dict(stack="head", x=M, top=SAFE_TOP + 150, w=620, items=[
                T("kicker", "Dec 8–14", 40, "semi", P["ink2"], gap=16),
                T("title", "This week at the sauna", 118, "display", ink, lh=.94, tracking=-.015)]),
            dict(stack="list", x=M, top=SAFE_TOP + 560, w=CW, items=[
                ROW(f"day-{d.lower()}", d, h, 44, ink, P["line2"]) for d, h in week] + [
                SP(36), T("note", "Book online or at the front desk.", 38, "text", muted)])]))

    # 5 first time? what to bring
    bring = ["Two towels: one to sit on, one to dry off", "A water bottle", "Flip-flops",
             "A swimsuit, if your session needs one", "A wool sauna hat, worn dry"]
    out.append(dict(
        name="first-time-what-to-bring", label="First time? What to bring", bg=P["t4"],
        art=[S.illustration("towels-and-slippers", 560, SAFE_TOP + 60, 420, "art-towels")],
        stacks=club(ink, "New here?") + [
            dict(stack="head", x=M, top=SAFE_TOP + 180, w=500, items=[
                T("title", "First time? Bring these", 112, "display", ink, lh=.94, tracking=-.015)]),
            dict(stack="list", x=M, top=SAFE_TOP + 640, w=CW, items=[
                CHECK(f"bring-{i}", b, 44, ink, P["ink2"]) for i, b in enumerate(bring, 1)] + [
                SP(40), T("note", "Arrive 15 minutes early and we will show you around.", 40, "text", P["ink2"])])]))

    # 6 cold plunge open
    out.append(dict(
        name="cold-plunge-open", label="Cold plunge open", bg=paper,
        art=[f'<rect id="water-band" x="0" y="0" width="{W}" height="1010" fill="{P["water"]}"/>',
             S.illustration("cold-plunge", 170, SAFE_TOP + 90, 740, "art-cold-plunge")],
        stacks=club(ink, "Now open") + [dict(stack="main", x=M, bottom=H - SAFE_BOTTOM - 10, w=CW, items=[
            T("title", "The cold plunge is open", 118, "display", ink, lh=.94, gap=34, tracking=-.015),
            ROW("hours", "Hours", "[4–9 pm]", 44, ink, P["line2"]),
            ROW("water", "Water", "[__ °F / __ °C]", 44, ink, P["line2"], gap=30),
            T("note", "Go in slowly and keep dips short. Get out if you feel unwell.", 40, "text", P["ink2"])])]))

    # 7 guest words: placeholder only, never a made-up review
    qm = ("M0 120C0 52 34 10 92 0L100 26C66 38 52 60 50 86C76 86 96 106 96 136C96 166 72 190 44 190C16 190 0 166 0 120Z"
          "M130 120C130 52 164 10 222 0L230 26C196 38 182 60 180 86C206 86 226 106 226 136C226 166 202 190 174 190"
          "C146 190 130 166 130 120Z")
    out.append(dict(
        name="guest-words", label="Your guest's words", bg=P["paper2"],
        art=[f'<path id="quote-mark" d="{qm}" transform="translate({M} {SAFE_TOP + 170})" fill="{P["ember"]}"/>',
             S.illustration("bucket-and-ladle", 620, 1250, 400, "art-bucket")],
        stacks=club(ink, "Guest words") + [
            dict(stack="main", x=M, top=SAFE_TOP + 430, w=CW, items=[
                T("quote", "[Guest quote goes here. Use a guest's real words, shared with their permission.]",
                  84, "display", ink, lh=1.04, gap=44, tracking=-.01),
                T("who", "— [Guest first name], [month]", 42, "semi", P["ink2"])])]))

    # 8 members-only event
    out.append(dict(
        name="members-only-event", label="Members-only event", bg=P["night2"],
        art=[S.illustration("bell-hat-on-peg", 350, SAFE_TOP + 10, 380, "art-bell-hat")],
        stacks=club(night_text, "Members only") + [
            dict(stack="head", x=M, top=SAFE_TOP + 400, w=CW, items=[
                T("kicker", "For members", 40, "semi", night_muted, gap=18),
                T("title", "Members’ Evening", 124, "display", night_text, lh=.92, tracking=-.015)]),
            dict(stack="main", x=M, bottom=H - SAFE_BOTTOM - 10, w=CW, items=[
                ROW("date", "Date", "[Fri, Dec 12]", 46, night_text, P["nightline"]),
                ROW("time", "Time", "[7:00–10:00 pm]", 46, night_text, P["nightline"]),
                ROW("spots", "Spots", "[20]", 46, night_text, P["nightline"], gap=30),
                T("details", "[Aufguss rounds, cold plunge and tea. Bring a friend? Ask us first.]", 40, "text", night_muted, gap=44),
                BTN("cta", "Book now", P["ember"], ink, gap=22),
                T("link", "Link in bio", 34, "semi", night_text)])]))
    return out


# ---------------------------------------------------------------- SVG layout


def item_height(it, w):
    k = it["t"]
    if k == "text":
        lines = S.wrap(it["text"], it["size"], w * .985, it["kind"], it["tracking"])
        return len(lines) * it["size"] * it["lh"]
    if k == "btn":
        return it["size"] * 1.2 + 2 * BTN_PADY
    if k == "row":
        return it["size"] * 1.25 + 2 * ROW_PAD
    if k in ("check", "num"):
        tw = w - (it["size"] * 1.6)
        lines = S.wrap(it["text"], it["size"], tw * .985, "text")
        return len(lines) * it["size"] * 1.25 + 2 * ROW_PAD
    if k == "space":
        return it["h"]
    raise ValueError(k)


def stack_svg(st, sid):
    x, w = st["x"], st["w"]
    heights = [item_height(it, w) + it.get("gap", 0) for it in st["items"]]
    total = sum(heights)
    y = st["top"] if "top" in st else st["bottom"] - total
    parts = []
    for it, hh in zip(st["items"], heights):
        k = it["t"]
        iid = f"{sid}-{it.get('id', 'space')}"
        if k == "text":
            m, _ = S.svg_text(iid, x, y, w, it["text"], it["size"], it["kind"], it["fill"], it["lh"], it["align"], it["tracking"])
            parts.append(m)
        elif k == "btn":
            bw = w if it["wfull"] else S.width(it["text"], it["size"], "semi") + 2 * BTN_PADX
            bh = it["size"] * 1.2 + 2 * BTN_PADY
            m, _ = S.svg_text(iid + "-label", x, y + BTN_PADY, bw, it["text"], it["size"], "semi", it["fg"], 1.2, "middle")
            parts.append(f'<g id="{iid}"><rect x="{x}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="6" fill="{it["bg"]}"/>{m}</g>')
        elif k == "row":
            lw = S.width(it["left"], it["size"], it["lkind"])
            ml, _ = S.svg_text(iid + "-left", x, y + ROW_PAD, lw / .985 + 4, it["left"], it["size"], it["lkind"], it["fill"], 1.25)
            mr, _ = S.svg_text(iid + "-right", x + lw + 30, y + ROW_PAD, w - lw - 30, it["right"], it["size"], it["rkind"],
                               it["fill"], 1.25, "end", maxlines=1)
            line = (f'<path d="M{x} {y + item_height(it, w):.1f}H{x + w}" stroke="{it["line"]}" stroke-width="2"/>'
                    if it["line"] else "")
            parts.append(f'<g id="{iid}">{ml}{mr}{line}</g>')
        elif k in ("check", "num"):
            sz = it["size"]
            ind = sz * 1.6
            m, th = S.svg_text(iid + "-text", x + ind, y + ROW_PAD, w - ind, it["text"], sz, "text", it["fill"], 1.25)
            b0 = y + ROW_PAD
            if k == "check":
                bs = sz * .72
                mark = (f'<rect x="{x + 2}" y="{b0 + (sz * 1.25 - bs) / 2:.1f}" width="{bs:.1f}" height="{bs:.1f}" rx="5" '
                        f'fill="none" stroke="{it["box"]}" stroke-width="3"/>')
            else:
                mark, _ = S.svg_text(iid + "-n", x, b0, ind, str(it["n"]), sz, "display", it["fill"], 1.25)
            line = (f'<path d="M{x} {y + item_height(it, w):.1f}H{x + w}" stroke="{it["line"]}" stroke-width="2"/>'
                    if it.get("line") else "")
            parts.append(f'<g id="{iid}">{mark}{m}{line}</g>')
        y += hh
    top = st["top"] if "top" in st else st["bottom"] - total
    return f'<g id="{sid}">' + "".join(parts) + "</g>", top, top + total


CREDIT = "Template by DIVELUX · diveluxsaunahat.com"


def story_svg(s, n):
    body, boxes = [], []
    for st in s["stacks"]:
        m, t, b = stack_svg(st, st["stack"])
        body.append(m)
        boxes.append((st["stack"], t, b))
        if t < SAFE_TOP - 1 or b > H - SAFE_BOTTOM + 1:
            raise SystemExit(f"{s['name']}: stack {st['stack']} leaves the safe zone ({t:.0f}-{b:.0f})")
    ink_on = P["nightmuted"] if s["bg"] in (P["night"], P["night2"]) else P["muted"]
    credit, _ = S.svg_text("credit-removable", M, H - 92, CW, CREDIT, 22, "text", ink_on, 1.2, "middle")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<title>{S.esc(s["label"])} — sauna club story template by DIVELUX (CC BY 4.0)</title>'
           f'<rect id="background" width="{W}" height="{H}" fill="{s["bg"]}"/>'
           f'<g id="art">{"".join(s["art"])}</g>'
           f'<g id="text">{"".join(body)}</g>'
           f'<g id="credit">{credit}</g></svg>')
    return svg, boxes


# ---------------------------------------------------------------- HTML (editable)


def item_html(it, sid):
    k = it["t"]
    key = f"{sid}-{it.get('id', '')}"
    gap = f"margin-bottom:{it.get('gap', 0)}px;" if it.get("gap") else ""
    ed = lambda txt, extra="": f'<div class="ed{extra}" data-k="{key}" contenteditable="plaintext-only" spellcheck="false">{S.esc(txt)}</div>'
    if k == "text":
        fam = "d" if it["kind"] == "display" else ("s" if it["kind"] == "semi" else "b")
        st = (f'font-size:{it["size"]}px;line-height:{it["lh"]};color:{it["fill"]};{gap}'
              f'text-align:{"left" if it["align"] == "start" else "center"};'
              + (f'letter-spacing:{it["tracking"]}em;' if it["tracking"] else ""))
        return (f'<div class="it {fam}" style="{st}">' + ed(it["text"]).replace('class="ed"', 'class="ed"') + "</div>")
    if k == "btn":
        return (f'<div class="it btn" style="{gap}font-size:{it["size"]}px;background:{it["bg"]};color:{it["fg"]};'
                f'padding:{BTN_PADY}px {BTN_PADX}px">{ed(it["text"])}</div>')
    if k == "row":
        bl = f'border-bottom:2px solid {it["line"]};' if it["line"] else ""
        return (f'<div class="it row" style="{gap}{bl}font-size:{it["size"]}px;color:{it["fill"]};padding:{ROW_PAD}px 0">'
                f'<div class="ed {"s" if it["lkind"] == "semi" else "b"}" data-k="{key}-l" contenteditable="plaintext-only" spellcheck="false">{S.esc(it["left"])}</div>'
                f'<div class="ed r {"s" if it["rkind"] == "semi" else "b"}" data-k="{key}-r" contenteditable="plaintext-only" spellcheck="false">{S.esc(it["right"])}</div></div>')
    if k in ("check", "num"):
        bl = f'border-bottom:2px solid {it["line"]};' if it.get("line") else ""
        mark = (f'<span class="box" style="border-color:{it["box"]}"></span>' if k == "check"
                else f'<span class="n d">{it["n"]}</span>')
        return (f'<div class="it li" style="{gap}{bl}font-size:{it["size"]}px;color:{it["fill"]};padding:{ROW_PAD}px 0">'
                f'{mark}{ed(it["text"])}</div>')
    if k == "space":
        return f'<div class="it" style="height:{it["h"]}px"></div>'


def story_html(s, n):
    shapes = (f'<svg class="bg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">'
              f'<rect width="{W}" height="{H}" fill="{s["bg"]}"/>{"".join(s["art"])}</svg>')
    stacks = []
    for st in s["stacks"]:
        pos = f'top:{st["top"]}px' if "top" in st else f'bottom:{H - st["bottom"]}px'
        stacks.append(f'<div class="stack" style="left:{st["x"]}px;width:{st["w"]}px;{pos}">'
                      + "".join(item_html(it, f'{n}-{st["stack"]}') for it in st["items"]) + "</div>")
    dark = s["bg"] in (P["night"], P["night2"])
    credit = (f'<div class="credit" style="color:{P["nightmuted"] if dark else P["muted"]}">'
              f'Template by DIVELUX · <a href="{S.SITE}">diveluxsaunahat.com</a></div>')
    return (f'<section class="story" id="story-{n}" aria-label="Story {n}: {S.esc(s["label"])}">'
            f'<div class="art">{shapes}{"".join(stacks)}{credit}<div class="safe" aria-hidden="true"></div></div>'
            f'<p class="cap">{n}. {S.esc(s["label"])}</p></section>')


HTML_CSS = """
*{box-sizing:border-box}
html,body{margin:0}
body{background:#e9e3d9;color:#1b1512;font:16px/1.5 Inter,Arial,sans-serif}
.bar{position:relative;background:#f6f3ee;border-bottom:1px solid #b9afa2;padding:14px 24px;display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center}
.bar h1{font:700 22px/1.1 "Bricolage Grotesque",Arial,sans-serif;margin:0;flex:1 1 280px}
.bar p{margin:0;font-size:14px;color:#3d332c;flex:1 1 420px}
.bar .tools{display:flex;flex-wrap:wrap;gap:8px}
.bar button,.bar select{font:600 14px Inter,Arial,sans-serif;min-height:44px;padding:0 16px;border:1px solid #1b1512;border-radius:6px;background:#fffdf9;color:#1b1512;cursor:pointer}
.bar button.main{background:#f0762e;border-color:#f0762e}
.bar button:focus-visible,.bar select:focus-visible,.ed:focus-visible{outline:3px solid #1b1512;outline-offset:3px}
main{display:flex;flex-wrap:wrap;gap:32px;justify-content:center;padding:28px 16px 60px}
.story{margin:0}
.story .frame{width:calc(1080px * var(--z));height:calc(1920px * var(--z));overflow:hidden;box-shadow:0 2px 12px rgba(27,21,18,.25)}
.art{position:relative;width:1080px;height:1920px;overflow:hidden;transform:scale(var(--z));transform-origin:0 0}
.art .bg{position:absolute;inset:0;display:block}
.stack{position:absolute;display:flex;flex-direction:column}
.it{min-width:0}
.d{font-family:"Bricolage Grotesque",Arial,sans-serif;font-weight:700;font-variation-settings:"opsz" 12}
.s{font-family:Inter,Arial,sans-serif;font-weight:600}
.b{font-family:Inter,Arial,sans-serif;font-weight:400}
.ed{white-space:pre-wrap;overflow-wrap:anywhere;outline:none;border-radius:4px}
.ed:hover{box-shadow:0 0 0 2px rgba(240,118,46,.55)}
.btn{align-self:flex-start;border-radius:6px;font-family:Inter,Arial,sans-serif;font-weight:600;line-height:1.2;text-align:center}
.row{display:flex;justify-content:space-between;gap:30px;line-height:1.25}
.row .r{text-align:right}
.li{display:grid;grid-template-columns:1.6em 1fr;line-height:1.25;font-family:Inter,Arial,sans-serif}
.li .box{display:block;width:.72em;height:.72em;border:3px solid;border-radius:5px;margin:.265em 0 0 2px}
.li .n{line-height:1.25}
.credit{position:absolute;left:0;right:0;top:1828px;text-align:center;font:400 22px/1.2 Inter,Arial,sans-serif}
.credit a{color:inherit;text-decoration:none}
.safe{display:none;position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(rgba(240,118,46,.22),rgba(240,118,46,.22)) top/100% 250px no-repeat,
             linear-gradient(rgba(240,118,46,.22),rgba(240,118,46,.22)) bottom/100% 250px no-repeat}
body.show-safe .safe{display:block}
.cap{margin:10px 0 0;font-size:14px;color:#3d332c}
@media print{
  @page{size:1080px 1920px;margin:0}
  body{background:none}
  .bar,.cap{display:none!important}
  main{display:block;padding:0}
  .story .frame{width:1080px;height:1920px;box-shadow:none;break-after:page;page-break-after:always}
  .art{transform:none}
  .safe{display:none!important}
  .ed:hover{box-shadow:none}
}
"""

HTML_JS = """
(function(){
  var KEY='dvx-sauna-stories:';
  var eds=document.querySelectorAll('.ed');
  eds.forEach(function(el){
    var v=null; try{v=localStorage.getItem(KEY+el.dataset.k)}catch(e){}
    if(v!==null) el.textContent=v;
    el.addEventListener('input',function(){try{localStorage.setItem(KEY+el.dataset.k,el.textContent)}catch(e){}});
    el.addEventListener('paste',function(e){e.preventDefault();var t=(e.clipboardData||window.clipboardData).getData('text');document.execCommand('insertText',false,t)});
  });
  var root=document.documentElement;
  function zoom(v){root.style.setProperty('--z',v);try{localStorage.setItem(KEY+'#zoom',v)}catch(e){}}
  var sel=document.getElementById('zoom');
  var z=null; try{z=localStorage.getItem(KEY+'#zoom')}catch(e){}
  if(z){sel.value=z} zoom(sel.value); sel.addEventListener('change',function(){zoom(sel.value)});
  document.getElementById('safe').addEventListener('click',function(){
    var on=document.body.classList.toggle('show-safe');this.setAttribute('aria-pressed',on?'true':'false')});
  document.getElementById('reset').addEventListener('click',function(){
    if(!confirm('Reset all text in all eight stories to the template text?'))return;
    Object.keys(localStorage).forEach(function(k){if(k.indexOf(KEY)===0&&k!==KEY+'#zoom')localStorage.removeItem(k)});
    location.reload()});
  document.getElementById('print').addEventListener('click',function(){window.print()});
})();
"""


def build_html(sts):
    secs = []
    for n, s in enumerate(sts, 1):
        h = story_html(s, n)
        h = h.replace('<div class="art">', '<div class="frame"><div class="art">', 1).replace(
            f'<p class="cap">', '</div><p class="cap">', 1)
        secs.append(h)
    return f"""<!doctype html>
<html lang="en-US"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sauna Club Story Templates (editable) — DIVELUX</title>
<meta name="author" content="DIVELUX">
<meta name="description" content="Eight editable 1080 x 1920 story templates for a sauna club. Click any text to edit; print to PDF for one story per page.">
<style>{S.font_css()}</style>
<style>:root{{--z:.3}}{HTML_CSS}</style>
</head><body>
<header class="bar">
<h1>Sauna Club Story Templates</h1>
<p>Click any text to change it. Your text is saved in this browser only. To export: set the view to 100% and take a screenshot of one story, or use Print and save as PDF (one 1080 × 1920 page per story).</p>
<div class="tools">
<label class="sr" for="zoom" style="position:absolute;left:-9999px">View size</label>
<select id="zoom"><option value=".3">View: small</option><option value=".5">View: 50%</option><option value="1">View: 100% (1080 × 1920)</option></select>
<button id="safe" type="button" aria-pressed="false">Show safe zones</button>
<button id="reset" type="button">Reset text</button>
<button id="print" type="button" class="main">Print / Save as PDF</button>
</div>
</header>
<main>
{chr(10).join(secs)}
</main>
<script>{HTML_JS}</script>
</body></html>
"""


def main():
    os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "png"), exist_ok=True)
    sts = stories()
    report = []
    for n, s in enumerate(sts, 1):
        svg, boxes = story_svg(s, n)
        base = f"{n:02d}-{s['name']}"
        S.write(os.path.join(OUT, "svg", base + ".svg"), svg)
        png = os.path.join(OUT, "png", base + ".png")
        S.render(svg, png)
        from PIL import Image
        Image.open(png).convert("RGB").save(png, optimize=True)
        report.append(dict(story=base, stacks=[(b, round(t), round(e)) for b, t, e in boxes]))
    S.write(os.path.join(OUT, "sauna-club-stories.html"), build_html(sts))
    # preview.png: the eight PNGs on one sheet (4 x 2)
    from PIL import Image
    w, h, g = 405, 720, 30
    sheet = Image.new("RGB", (4 * w + 5 * g, 2 * h + 3 * g), P["paper2"])
    for i, s in enumerate(sts):
        im = Image.open(os.path.join(OUT, "png", f"{i + 1:02d}-{s['name']}.png")).convert("RGB").resize((w, h), Image.LANCZOS)
        sheet.paste(im, (g + (i % 4) * (w + g), g + (i // 4) * (h + g)))
    sheet.save(os.path.join(OUT, "preview.png"), optimize=True)
    for r in report:
        print(r["story"], r["stacks"])
    json.dump([dict(n=n, file=f"{n:02d}-{s['name']}", label=s["label"]) for n, s in enumerate(sts, 1)],
              open("/tmp/w3s-stories.json", "w"))


if __name__ == "__main__":
    main()
