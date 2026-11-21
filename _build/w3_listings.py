#!/usr/bin/env python3
"""Wave 3 design templates: writes LISTING.md and README.md into the four folders (P064, P066, P067, P068).
Limits: title <= 60 characters, short description <= 160, full description 150-220 words, one or two links."""
import os
import re
import subprocess

import w3_common as W

FOOT = ("Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com\n"
        "More free sauna templates and tools: https://diveluxsaunahat.com/pages/sauna-tools")
LICENSE = ("CC BY 4.0 (Creative Commons Attribution 4.0 International). Credit: DIVELUX, https://diveluxsaunahat.com\n"
           "The DIVELUX name and logo are © DIVELUX Inc. and are not covered by the license. "
           "Fonts: Bricolage Grotesque and Inter (SIL Open Font License 1.1).")
BANNED = ["detox", "toxin", "cure", "burns fat", "best seller", "amazon", "soak", "wet the hat", "damp", "rating", " review"]

FIGMA = """## Figma and other design apps

Every size also comes as a plain SVG made from the same layout:

1. In Figma, drag the `.svg` file onto the canvas (or File → Import). Illustrator, Inkscape, Affinity and Penpot open it too.
2. Text stays live text in **Bricolage Grotesque** and **Inter**. Both are free Google Fonts and are built into Figma;
   for desktop apps, install them from fonts.google.com.
3. Layers are grouped and named after the fields (`club-name`, `date`, `item-price` …). Each line of a paragraph is its own
   text layer, so rewrap long paragraphs by hand or join the lines into one text box.
4. Sizes are in pixels at 96 per inch (the CSS pixel), so a US Letter page is 816 × 1056."""

EDIT = """## Edit in your browser

1. Open `{html}` in Chrome, Edge, Firefox or Safari. Nothing is loaded from the internet: the fonts are inside the file.
2. Click any text and type. {extra}
3. Pick the size in the dark bar at the top, then **Print / Save PDF**. In the print dialog: scale 100% (actual size),
   margins None, background graphics on.
4. Your edits are saved in this browser only (local storage), never uploaded. **Reset** brings back the sample text.
   To keep or share a finished version, save it as a PDF."""

P = {}

P["spa-menu-price-list"] = dict(
    name="Spa and Sauna Menu and Price List", fmt="Editable HTML + PDF (Letter, A4) + PNG 1080 × 1350 + Figma SVG",
    title="Spa and Sauna Menu and Price List (Editable Template)",
    short="Free editable spa and sauna menu: sessions, treatments, add-ons and memberships with prices. US Letter, A4, a 1080 x 1350 post and Figma-ready SVG.",
    full=f"""A clean menu and price list for a sauna, spa, bathhouse or wellness studio. Change the name, the services and the prices right in your browser, then print it or save it as a PDF.

The sample menu has four sections, each with a name, a short note and a price on a dotted leader line:

- Sauna: day pass, private sauna, sauna and cold plunge, Aufguss session
- Treatments: birch whisk session, body scrub, massage
- Add-ons: towel and robe, flip-flops, herbal tea, a felt sauna hat
- Memberships: 10-visit card and monthly membership

A Good to know box holds five house notes, and the footer has your address, phone and website. Every line can be edited, removed or added. All prices read $00, so nothing goes out with a made-up number.

What is in the folder:

- One editable HTML file with three sizes: US Letter, A4 and 1080 x 1350 for social posts and screens
- Print-ready PDFs for Letter and A4, and a 1080 x 1350 PNG
- An SVG for each size with live text and named layers, for Figma, Illustrator or Inkscape

No account, no app, no internet needed.

{FOOT}""",
    tags="spa menu template, sauna price list, editable menu, price list template, wellness studio, bathhouse, spa signage, Figma template, printable menu, sauna business",
    files=["spa-menu-price-list.html", "spa-menu-price-list-letter.pdf", "spa-menu-price-list-a4.pdf", "spa-menu-price-list-post.png",
           "spa-menu-price-list-letter.svg", "spa-menu-price-list-a4.svg", "spa-menu-price-list-post.svg", "preview.png", "README.md", "LICENSE"],
    meta="Editable HTML; PDF US Letter (8.5 × 11 in) and A4; PNG and SVG 1080 × 1350; SVG for Letter and A4",
    sizes="`?size=letter` (default), `?size=a4`, `?size=post` (1080 × 1350 px)",
    extra="Hover a menu line to show **Remove**; **+ Add line** under a section adds one. The club name in the header and in the footer change together.",
    printing="Print on heavy matte paper or card stock. For a table menu, print on both sides of one sheet or laminate it.",
    art="The stove illustration comes from the DIVELUX Sauna Illustrations set (CC BY 4.0).")

P["aufguss-schedule-board"] = dict(
    name="Aufguss Schedule Board", fmt="Editable HTML + PDF (A3, Tabloid) + 1920 × 1080 TV screen + Figma SVG",
    title="Aufguss Schedule Board: Print and Lobby TV Template",
    short="Free editable Aufguss schedule for saunas and spas: times, sessions, scents, sauna masters and rooms. A3 and Tabloid posters plus a 1920 x 1080 lobby TV screen.",
    full=f"""Aufguss is the guided sauna round where a sauna master pours water, often scented, on the hot stones and moves the heat through the room with a towel. Guests want to know what is on tonight and when. This board tells them.

The print board lists six sessions in a clear table: time, session name with a short note, scent, heat (mild, medium or strong), sauna master, room and length. A row of three house notes runs along the bottom: come a little early, leave whenever you need to, cool down and rest.

The TV version is made for a screen in the lobby: the next session in large type on the left, the whole evening on the right. The two share their fields, so a time you change on the poster also changes on the screen. A Full screen button fills the TV.

Included:

- One editable HTML file: A3, Tabloid (11 x 17 in) and TV 1920 x 1080
- Print-ready A3 and Tabloid PDFs and a 1920 x 1080 PNG
- SVG for each size with live text and named layers, ready for Figma

Session names, scents and times are samples; the sauna master's name reads Name.

{FOOT}""",
    tags="Aufguss, sauna schedule, sauna master, spa signage, lobby TV screen, digital signage, bathhouse, sauna events, Figma template, printable poster",
    files=["aufguss-schedule-board.html", "aufguss-schedule-board-a3.pdf", "aufguss-schedule-board-tabloid.pdf", "aufguss-schedule-board-tv.png",
           "aufguss-schedule-board-a3.svg", "aufguss-schedule-board-tabloid.svg", "aufguss-schedule-board-tv.svg", "preview.png", "README.md", "LICENSE"],
    meta="Editable HTML; PDF A3 (297 × 420 mm) and Tabloid (11 × 17 in); PNG and SVG 1920 × 1080; SVG for A3 and Tabloid",
    sizes="`?size=a3` (default), `?size=tabloid` (11 × 17 in), `?size=tv` (1920 × 1080 px)",
    extra="The print board and the TV screen share their fields: change a time in one and it changes in the other. Leave a row empty if you run fewer sessions.",
    printing="A3 and Tabloid print on large-format office printers or at any copy shop. Keep paper out of the hot room: hang the board in the lobby or the changing room, or laminate it.\n\n"
             "**TV:** open the file with `?size=tv` on the computer or stick plugged into the screen and press **Full screen**. "
             "The page is static: update the times when the program changes.",
    art="No illustrations; type and color only.")

P["sauna-club-membership-card"] = dict(
    name="Sauna Club Membership Card", fmt="Editable HTML + PDF (CR80 with bleed, 10-up A4 and Letter) + Figma SVG",
    title="Sauna Club Membership Card Template (CR80, 10-Up)",
    short="Free editable membership card for a sauna club: credit-card size with bleed, a 10-visit punch grid on the back, and 10-up print sheets for A4 and US Letter.",
    full=f"""A simple membership card for a sauna club, bathhouse or gym spa, in the same size as a credit card (CR80, 85.6 x 54 mm).

The front has your club name, the member's name and number, the card type (monthly, 10 visits, annual) and a valid-thru date. The back has a punch grid of ten numbered circles, a signature line and your website and phone.

Two ways to print:

- At a print shop: a two-page PDF, front and back, with 3 mm bleed all around
- At home or in the office: sheets of ten cards on A4 or US Letter with cut marks, a front sheet and a back sheet for two-sided printing

On the sheets every card has its own name and number, while the club name, card type and date change on all ten cards at once. Edit everything in your browser and save it as a PDF; no design app needed.

Also included: an SVG for each layout with live text and named layers, ready for Figma or Illustrator.

The bands run vertically and text stays clear of the edges, so a slightly crooked cut still looks neat.

{FOOT}""",
    tags="membership card template, sauna club, punch card, loyalty card, CR80 card, business card sheet, gym membership, bathhouse, Figma template, printable card",
    files=["sauna-club-membership-card.html", "sauna-club-membership-card-cr80.pdf", "sauna-club-membership-card-a4.pdf", "sauna-club-membership-card-letter.pdf",
           "sauna-club-membership-card-cr80-front.png", "sauna-club-membership-card-cr80-back.png",
           "sauna-club-membership-card-cr80-front.svg", "sauna-club-membership-card-cr80-back.svg",
           "sauna-club-membership-card-a4-sheet-front.svg", "sauna-club-membership-card-a4-sheet-back.svg",
           "sauna-club-membership-card-letter-sheet-front.svg", "sauna-club-membership-card-letter-sheet-back.svg", "preview.png", "README.md", "LICENSE"],
    meta="Editable HTML; PDF card 91.6 × 60 mm (85.6 × 54 mm + 3 mm bleed), 2 pages; PDF 10-up A4 and US Letter, front + back; SVG and PNG",
    sizes="`?size=card` (default: one card with bleed, front and back), `?size=a4` and `?size=letter` (ten per sheet)",
    extra="Club name, card title, type, valid-thru, punch-grid text and contact line are shared by all cards; member name and number are per card.",
    printing="""- **Print shop:** send `sauna-club-membership-card-cr80.pdf`. Page 1 is the front, page 2 the back, each 91.6 × 60 mm:
  the 85.6 × 54 mm card (CR80, the credit-card size of ISO/IEC 7810 ID-1) plus 3 mm bleed on every side.
  Keep your own text at least 3 mm inside the trim line.
- **At home:** print the sheet PDF on card stock at 100%. Page 1 is the front sheet, page 2 the back sheet: print two-sided,
  flip on the long edge. Print a test on plain paper first and hold it against a window to check that front and back line up.
- Cut along the marks. The rows touch each other, so one straight cut separates two rows. On US Letter the marks above and
  below the cards sit only about 5 mm from the edge; if your printer clips them, use the side marks.
- To punch the circles use a small hole punch, a pen or a stamp.""",
    art="The hat icon comes from the DIVELUX Sauna Icons (filled) set (CC BY 4.0).")

P["sauna-event-poster"] = dict(
    name="Sauna Event Poster", fmt="Editable HTML, 3 layouts + PDF (Letter, A3) + PNG 1080 × 1350 + Figma SVG",
    title="Sauna Event Poster Template: 3 Editable Layouts",
    short="Free editable sauna event posters: Aufguss night, sauna and cold plunge social, open house. US Letter and A3 to print, 1080 x 1350 posts, Figma-ready SVG.",
    full=f"""Three posters for the events a sauna club, spa or community sauna runs most often. Type your details in the browser, then print or post.

The layouts:

- Aufguss night: a dark poster with a glowing stove, a short description of the evening, the date, what to bring and a box for a ticket QR code
- Sauna and cold plunge social: cool water blue on top, big type below, with time, place and price in one row and a box for an RSVP code
- Open house: warm wood tones, a cabin by the lake and a timetable for the afternoon, from doors open to the last round

Each layout has a fine-print line for your own notes, such as age limits or the usual advice to ask a doctor first if you are pregnant or have a health condition. Every detail on the samples is a placeholder, including the $00 prices.

In the folder:

- One editable HTML file with all three layouts in US Letter, A3 and 1080 x 1350
- Print-ready PDFs for Letter and A3 and PNG posts
- An SVG for every layout and size with live text and named layers, ready for Figma

{FOOT}""",
    tags="sauna event poster, event flyer template, Aufguss night, cold plunge social, open house poster, community sauna, spa events, Figma template, printable poster, social media post",
    files=["sauna-event-poster.html"] + [f"sauna-event-poster-{l}-{s}.{e}" for l in ("aufguss", "social", "open")
                                         for s, e in (("letter", "pdf"), ("a3", "pdf"), ("post", "png"), ("letter", "svg"), ("a3", "svg"), ("post", "svg"))]
          + ["preview.png", "README.md", "LICENSE"],
    meta="Editable HTML with 3 layouts; PDF US Letter and A3 (297 × 420 mm); PNG and SVG 1080 × 1350; SVG for Letter and A3",
    sizes="`?size=letter` (default), `?size=a3`, `?size=post` (1080 × 1350 px); layouts `?layout=aufguss`, `?layout=social`, `?layout=open`",
    extra="Choose the layout and the size in the top bar. The club name is shared by the three layouts; in the open house timetable, hover a line to remove it or use **+ Add line**.",
    printing="Letter prints on any office printer; A3 on large-format printers or at a copy shop. Replace the dashed QR box with your own code: print the poster, then stick the code on, or swap the box for the code in the SVG.",
    art="Illustrations from the DIVELUX Sauna Illustrations set (CC BY 4.0): sauna stove, cold plunge tub, lakeside sauna.")


def readme(slug, p):
    files = "\n".join(f"- `{f}`" for f in p["files"] if f not in ("README.md",))
    return f"""# {p['name']}

{p['short']}

![{p['name']}](preview.png)

## Files

{files}

{EDIT.format(html=slug + '.html', extra=p['extra'])}

Sizes: {p['sizes']}. You can also add the size to the address by hand, for example `{slug}.html?size={p['sizes'].split('`')[1].split('=')[1]}`.

## Printing

{p['printing']}

{FIGMA}

## Sample text

Every name, date, time and price in the files is a placeholder ("Your Sauna Club", "$00", "Name"). Replace them before you print.
Health notes are kept general; check any wording you add with your own rules and local requirements.

## Credits and license

Template by DIVELUX, makers of wool sauna hats: {W.SITE} · more free tools: {W.TOOLS}

{LICENSE}
{p['art']}

You may use, change and print these templates for your business, including for commercial use. Please keep the small
credit line ("Template by DIVELUX · diveluxsaunahat.com · CC BY 4.0") or credit DIVELUX somewhere reasonable, such as your website.

## Rebuilding

The files are built by `templates/_build/w3_build.py` (writes the HTML, renders PDFs, PNGs and SVGs with one headless Chromium,
compares every SVG with the page pixel by pixel and runs an editing test) and `templates/_build/w3_listings.py` (this README and LISTING.md).
"""


def listing(slug, p):
    files = "\n".join(f"- `{f}`" for f in p["files"])
    return f"""# LISTING: {p['name']}

## Title (max 60 characters)
{p['title']}

## Short description (max 160 characters)
{p['short']}

## Full description
{p['full']}

## Tags
{p['tags']}

## License
{LICENSE}

## Files
{files}

## Metadata
- Author / publisher: DIVELUX
- Format: {p['meta']}
- Language: English (en-US) · Version 1.0 · 2026-11
- Price: free
"""


def main():
    bad = 0
    for slug, p in P.items():
        d = os.path.join(W.ROOT, slug)
        if not os.path.exists(os.path.join(d, "LICENSE")):
            subprocess.run(["python3", "/root/divelux/freebies/gfx/_tools/mklicense.py", d, p["name"], "Template"], check=True)
        W.write(os.path.join(d, "README.md"), readme(slug, p))
        W.write(os.path.join(d, "LISTING.md"), listing(slug, p))
        words = len(re.findall(r"[A-Za-zÀ-ÿ0-9°'’\-]+", re.sub(r"https?://\S+", "URL", p["full"])))
        links = re.findall(r"https://diveluxsaunahat\.com\S*", p["full"])
        text = (p["full"] + p["short"] + p["title"]).lower()
        probs = []
        if len(p["title"]) > 60: probs.append(f"title {len(p['title'])}")
        if len(p["short"]) > 160: probs.append(f"short {len(p['short'])}")
        if not 150 <= words <= 220: probs.append(f"words {words}")
        if not 1 <= len(links) <= 2: probs.append(f"links {len(links)}")
        probs += [f"banned '{b}'" for b in BANNED if b in text]
        missing = [f for f in p["files"] if not os.path.exists(os.path.join(d, f))]
        extra = sorted(set(os.listdir(d)) - set(p["files"]) - {"LISTING.md"})
        if missing: probs.append("missing " + ", ".join(missing))
        if extra: probs.append("unlisted " + ", ".join(extra))
        bad += bool(probs)
        print(f"{'OK' if not probs else '!!'} {slug}: title {len(p['title'])}, short {len(p['short'])}, {words} words, {len(links)} links", probs)
    print("problems:", bad)


if __name__ == "__main__":
    main()
