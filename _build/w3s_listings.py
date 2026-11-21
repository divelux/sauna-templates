#!/usr/bin/env python3
"""Writes LISTING.md, README.md and LICENSE for the wave 3 screen templates
(sauna-club-social-stories, sauna-booking-app-ui-kit, sauna-club-website) and checks the listing limits:
title <= 60, short <= 160, full description 150-220 words with 1-2 links to diveluxsaunahat.com."""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w3s_common as S  # noqa: E402

FOOT = ("Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com\n"
        "More free sauna tools: https://diveluxsaunahat.com/pages/sauna-tools")
CC = ("CC BY 4.0 (Creative Commons Attribution 4.0 International). Credit: DIVELUX, https://diveluxsaunahat.com\n"
      "The DIVELUX name and logo are © DIVELUX Inc. and are not covered by the license. "
      "Fonts named in the files: Bricolage Grotesque and Inter (SIL Open Font License 1.1, free on Google Fonts).")
BANNED = ["soak", "wet the hat", "damp", "detox", "toxin", "burn fat", "best seller", "cure", "amazon", "generated"]

P = {}

P["sauna-club-social-stories"] = dict(
    name="Sauna club social stories", fmt="8 stories, 1080 × 1920: SVG + PNG + editable HTML",
    title="Sauna Club Story Templates (8 Editable, 1080x1920)",
    short="Eight free story templates for sauna clubs and spas: sessions, rules, Aufguss night, schedule, cold plunge, events. SVG, PNG and an editable HTML file.",
    full=f"""Eight story templates for saunas, bathhouses and sauna clubs, sized 1080 x 1920 for Instagram and Facebook stories or WhatsApp Status.

The set:

- Session announcement with a Book button
- Sauna rules
- Aufguss tonight: three rounds, scents and the sauna master's name
- This week at the sauna
- First time? What to bring
- The cold plunge is open
- Your guest's words: an empty quote frame for a real guest's words, shared with permission. The set has no sample reviews.
- Members-only event

Every story comes three ways. SVG files with live text and named layers open in Figma, Illustrator and Inkscape. PNG files are ready to post. One HTML file lets you click any text, type your own and save every story as a PDF page or a screenshot, with nothing to install.

Text stays inside a safe zone 250 px from the top and bottom, so app buttons do not cover it. The drawings come from our free Sauna Illustrations set. Fonts: Bricolage Grotesque and Inter, both free on Google Fonts.

{FOOT}""",
    tags="instagram story template, sauna, sauna club, spa marketing, social media templates, figma template, svg template, aufguss, bathhouse, editable story",
    license=CC,
    files=["sauna-club-stories.html", "svg/ (8 SVG files)", "png/ (8 PNG files, 1080 x 1920)", "preview.png", "README.md", "LICENSE"],
    meta="SVG (live text, named groups), PNG 1080 x 1920, HTML (editable in the browser, prints one 1080 x 1920 page per story); 8 stories")

P["sauna-booking-app-ui-kit"] = dict(
    name="Sauna booking app UI kit", fmt="6 screens (390 × 844) + components: SVG + PNG + tokens.json",
    title="Sauna Booking App UI Kit (Figma-Ready SVG + Tokens)",
    short="Free UI kit for a sauna or spa booking app: six phone screens, a component board and design tokens. Live-text SVG for Figma, PNG and tokens.json.",
    full=f"""A small, complete UI kit for a sauna or bathhouse booking app. It follows the path a guest takes: pick a day, pick a slot, book it, see the confirmation and find it later under My bookings.

Six screens at 390 x 844:

- Slots by day, with available, few-left and full states
- Book a slot: details, guest count, name and email
- Booking confirmed
- My bookings
- Profile with a membership pass and settings
- Empty state

The component board has buttons (primary, secondary, ghost, disabled, inverse), badges, day chips, slot cards, inputs in default, focus and error states, a stepper, toggles, a segmented control and the tab bar. tokens.json holds colors, type styles, radii and spacing in the W3C design tokens format, ready for Tokens Studio.

Everything is plain SVG with live text, so it drops straight into Figma, Penpot or Illustrator. Text colors pass WCAG AA contrast and tap targets are at least 44 px. All data is sample data: Your Sauna Club, Alex, $25.

{FOOT}""",
    tags="ui kit, figma ui kit, booking app, mobile app design, sauna, spa app, design tokens, svg, app screens, wellness app",
    license=CC,
    files=["sauna-booking-ui-kit-sheet.svg", "screens/ (6 SVG files, 390 x 844)", "png/ (6 screens at 2x + sheet.png)", "tokens.json",
           "preview.png", "README.md", "LICENSE"],
    meta="SVG (live text, named groups), PNG, JSON design tokens; 6 screens + component board")

P["sauna-club-website"] = dict(
    name="Sauna club website template", fmt="One-page HTML + CSS, no dependencies (MIT)",
    title="Sauna Club Website Template (HTML + CSS, MIT)",
    short="Free one-page website for a sauna club or bathhouse: schedule, prices, house rules, visit info and FAQ. Plain HTML and CSS, no scripts, MIT license.",
    full=f"""A one-page website template for a sauna club, bathhouse or small public sauna. Plain HTML and CSS: no framework, no build step, no scripts and no outside requests. Open index.html, change the text, then upload the folder to any static host.

Sections:

- Header with the club name and a Book button
- Hero with a short pitch, three key facts and an illustration
- This week's sessions as a real table, with Aufguss and women-only tags
- Prices: single session, 10-session pass and membership
- House rules with a short health note
- Visit and book: address, phone, email, hours and a map placeholder
- FAQ with questions that open and close without any code
- Footer

Accessibility is built in: one H1, a skip link, landmarks, visible focus, 44 px tap targets, AA color contrast and support for reduced motion. We checked it at 375, 390, 768 and 1280 px wide with no sideways scrolling. Colors, fonts and widths sit in CSS variables at the top of styles.css.

Code under the MIT License. The fonts (Bricolage Grotesque, Inter) are included under the SIL Open Font License.

{FOOT}""",
    tags="website template, html template, sauna, spa website, one page template, static site, css template, accessible template, bathhouse, mit license",
    license=("Code (HTML, CSS): MIT License, © 2026 DIVELUX — see LICENSE. The footer credit can be removed.\n"
             "assets/lakeside-sauna.svg: from DIVELUX Sauna Illustrations, CC BY 4.0. "
             "Fonts in fonts/: SIL Open Font License 1.1 (fonts/OFL.txt). The DIVELUX name is not covered by the license."),
    files=["index.html", "styles.css", "assets/ (mark.svg, favicon.svg, lakeside-sauna.svg)",
           "fonts/ (bricolage-grotesque-latin.woff2, inter-latin.woff2, OFL.txt)", "preview.png", "README.md", "LICENSE"],
    meta="HTML5 + CSS, no JavaScript, about 200 KB with fonts; tested at 375, 390, 768 and 1280 px")

README = {}
README["sauna-club-social-stories"] = """# Sauna Club Story Templates

Eight story templates for saunas, bathhouses and sauna clubs, 1080 × 1920 px.
Made by DIVELUX, makers of wool sauna hats — https://diveluxsaunahat.com · more free tools: https://diveluxsaunahat.com/pages/sauna-tools

| # | Story | Files |
|---|---|---|
{rows}

## Three ways to edit

**In the browser (no install).** Open `sauna-club-stories.html` in Chrome, Edge, Safari or Firefox. Click any text and type.
Your text is saved in that browser only (localStorage), so it is still there next time. "Reset text" brings back the template text.
To export, either choose *View: 100%* and take a screenshot of one story, or press *Print / Save as PDF*: each story prints as one
1080 × 1920 page. Longer text wraps and pushes the lines below it down, so keep headlines short.

**In Figma, Penpot, Illustrator or Inkscape.** Drag a file from `svg/` onto the canvas. The text is live text in Bricolage Grotesque
(Bold) and Inter (Regular, SemiBold); install them from Google Fonts if your app does not have them. Layers have readable names
(`background`, `art`, `text`, `main-title`, `cta`, `credit` …). SVG has no automatic line wrap: each line is its own line of text.

**As images.** The PNG files in `png/` are ready to post.

Canva can place the SVG or PNG as an image, but its text will not be editable there; type your text in the browser file first.

## Safe zones

Story apps draw the profile row at the top and the reply bar at the bottom. All text sits at least 250 px from the top and the bottom
edge. "Show safe zones" in the HTML file shades those strips. The small credit line at the very bottom sits in the bottom strip on purpose.

## The guest quote story

Story 7 is a frame, not a review. Put in only a real guest's own words, with their permission, and do not change their meaning.
Made-up or edited reviews are misleading to your guests (and in the US the FTC treats fake reviews as deceptive advertising).

## Colors

Paper `#f6f3ee`, card `#fffdf9`, ink `#1b1512`, second ink `#3d332c`, muted `#6f655c`, night `#1c110b`, accent `#f0762e` (buttons and
small markers only), water `#a9c3c8`. The drawings come from DIVELUX Sauna Illustrations (CC BY 4.0).

## Rebuilding

`python3 ../_build/t65_stories.py` rebuilds the SVG, PNG, HTML and preview from one description per story (needs `resvg-py` and `fontTools`).

## License

CC BY 4.0. Credit line: "Templates by DIVELUX — diveluxsaunahat.com". The credit can go in your post caption or bio link; you may
delete the small credit line on the stories. The DIVELUX name and logo are not covered by the license.
"""

README["sauna-booking-app-ui-kit"] = """# Sauna Booking App UI Kit

Six phone screens (390 × 844), a component board and design tokens for a sauna or bathhouse booking app.
Made by DIVELUX, makers of wool sauna hats — https://diveluxsaunahat.com · more free tools: https://diveluxsaunahat.com/pages/sauna-tools

![Screens](preview.png)

## What is inside

| File | What it is |
|---|---|
| `sauna-booking-ui-kit-sheet.svg` | Everything on one board: the six screens, buttons, badges, day chips, slot cards, inputs, stepper, toggles, segmented control, tab bar, color and type specimens |
| `screens/01-slots.svg` … `06-empty.svg` | One SVG per screen, 390 × 844 |
| `png/` | The screens at 2x (780 × 1688) and `sheet.png` |
| `tokens.json` | Colors, type styles, radii, spacing and sizes in the W3C design tokens format (`$value` / `$type`) |

Screens: 01 slots by day · 02 book a slot · 03 booking confirmed · 04 my bookings · 05 profile and membership · 06 empty state.

## Import into Figma

1. Install the fonts if you work offline: Bricolage Grotesque and Inter (both on Google Fonts; Figma in the browser has them already).
2. Drag `sauna-booking-ui-kit-sheet.svg` or the files in `screens/` onto the canvas. Each SVG becomes a frame; group names
   (`tab-bar`, `slot-2`, `book-button`, `field-email` …) become layer names, and the text stays editable.
3. To reuse a piece, select its group and choose *Create component*. The shapes are plain vectors, not auto layout, so add auto
   layout where you want it.
4. Tokens: open the Tokens Studio for Figma plugin, choose the W3C DTCG format and load `tokens.json`, or copy the values by hand.

Penpot and Illustrator import the same SVG files.

## Accessibility notes

Text and background pairs used in the kit, checked with the WCAG 2 formula:

| Text | Background | Ratio |
|---|---|---|
{contrast}

Input borders and other UI edges are at least 3:1. Tap targets (buttons, tabs, chips, stepper, cancel links) are at least 44 × 44 px.
Disabled controls are not required to meet contrast, but the disabled color here still reads.

## Sample data

Club name, person, dates, times, prices and the booking code are placeholders. Replace them with your own.

## Rebuilding

`python3 ../_build/t69_uikit.py` rebuilds everything (needs `resvg-py` and `fontTools`) and stops if a contrast pair fails.

## License

CC BY 4.0. Credit line: "UI kit by DIVELUX — diveluxsaunahat.com". The empty-state drawing is from DIVELUX Sauna Illustrations (CC BY 4.0).
The DIVELUX name and logo are not covered by the license.
"""

README["sauna-club-website"] = """# Sauna Club Website Template

A one-page website for a sauna club, bathhouse or small public sauna. Plain HTML and CSS: no framework, no build step,
no JavaScript and no requests to other servers.
Made by DIVELUX, makers of wool sauna hats — https://diveluxsaunahat.com · more free tools: https://diveluxsaunahat.com/pages/sauna-tools

![Desktop and phone](preview.png)

## Files

```
index.html       the page
styles.css       all styles; colors, fonts and widths are variables in :root at the top
assets/          mark.svg (logo placeholder), favicon.svg, lakeside-sauna.svg (illustration)
fonts/           Bricolage Grotesque and Inter, Latin subset, woff2 + OFL.txt
```

## Make it yours

1. Open `index.html` in a text editor. Every name, address, phone number, time and price is sample text: search for
   "Your Sauna Club", "Your Town", "123 Example Road", "555", "example.com" and "$" and replace them.
2. Booking: the Book buttons point to the Visit section. If you use a booking service, put its link in the two `href="#visit"`
   buttons.
3. Map: replace the dashed "Map goes here" box with a map image and a link to your map listing.
4. Colors: change the variables at the top of `styles.css`. Keep `--accent` for the main button only and check that text on it
   stays readable (dark text on the default orange is 6.3:1).
5. Logo: replace `assets/mark.svg` and `assets/favicon.svg`.
6. Upload the folder to any static host (GitHub Pages, Netlify, Cloudflare Pages, your own server).

The health note under the house rules is general guidance. Keep a note like it, and follow your local rules for public saunas.

## What we checked

- Widths 375, 390, 768 and 1280 px in Chromium: no sideways scrolling (the schedule table scrolls inside its own box on phones)
- One `h1`, headings in order, `header` / `nav` / `main` / `footer` landmarks, `lang="en-US"`
- Skip link is the first thing you reach with Tab; focus is always visible
- Images have alt text; links and buttons are at least 44 px tall
- Text contrast at least 4.5:1 everywhere (most pairs 10:1 or more)
- `prefers-reduced-motion` turns off smooth scrolling and transitions
- No console errors, no outside requests

## Credit

The footer says "Website template by DIVELUX". The MIT License lets you remove it. If you keep it, thank you.

## License

Code (HTML, CSS): MIT License, see `LICENSE`. `assets/lakeside-sauna.svg` comes from DIVELUX Sauna Illustrations (CC BY 4.0).
Fonts: SIL Open Font License 1.1 (`fonts/OFL.txt`). The DIVELUX name is not covered by any of these licenses.
"""

MIT = """MIT License

Copyright (c) 2026 DIVELUX (https://diveluxsaunahat.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

--------------------------------------------------------------------------------
Not covered by the MIT License above:

assets/lakeside-sauna.svg  From "Sauna Illustrations" by DIVELUX, licensed CC BY 4.0
                           (https://creativecommons.org/licenses/by/4.0/). Credit: Illustrations by DIVELUX — diveluxsaunahat.com
fonts/*.woff2              Bricolage Grotesque and Inter, SIL Open Font License 1.1, see fonts/OFL.txt
The DIVELUX name.
"""


def main():
    import json
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    st = json.load(open("/tmp/w3s-stories.json"))
    rows = "\n".join(f"| {s['n']} | {s['label']} | `svg/{s['file']}.svg` · `png/{s['file']}.png` |" for s in st)
    import t69_uikit as U
    contrast = "\n".join(f"| {a} `{U.C[a]}` | {b} `{U.C[b]}` | {S.contrast(U.C[a], U.C[b]):.1f}:1 |" for a, b, need in U.PAIRS if need >= 4.5)
    bad = 0
    for slug, p in P.items():
        d = os.path.join(S.ROOT, slug)
        words = len(re.findall(r"[A-Za-z0-9öÖ'’\-]+", re.sub(r"https?://\S+", "URL", p["full"])))
        links = re.findall(r"https://diveluxsaunahat\.com\S*", p["full"])
        text = (p["title"] + p["short"] + p["full"]).lower()
        probs = []
        if len(p["title"]) > 60: probs.append(f"title {len(p['title'])}")
        if len(p["short"]) > 160: probs.append(f"short {len(p['short'])}")
        if not 150 <= words <= 220: probs.append(f"words {words}")
        if not 1 <= len(links) <= 2: probs.append(f"links {len(links)}")
        probs += [f"banned {b}" for b in BANNED if b in text]
        bad += bool(probs)
        print(f"{slug}: title {len(p['title'])}, short {len(p['short'])}, words {words}, links {len(links)}", probs or "OK")
        files = "\n".join(f"- `{f}`" for f in p["files"])
        S.write(os.path.join(d, "LISTING.md"), f"""# LISTING: {p['name']}

## Title (max 60 characters)
{p['title']}

## Short description (max 160 characters)
{p['short']}

## Full description
{p['full']}

## Tags
{p['tags']}

## License
{p['license']}

## Files
{files}

## Metadata
- Author / publisher: DIVELUX
- Format: {p['meta']}
- Language: English (en-US) · Version 1.0 · 2026-11
- Price: free
""")
        rd = README[slug].replace("{rows}", rows).replace("{contrast}", contrast)
        S.write(os.path.join(d, "README.md"), rd)
        if slug == "sauna-club-website":
            S.write(os.path.join(d, "LICENSE"), MIT)
        else:
            name = "Sauna Club Story Templates" if "stories" in slug else "Sauna Booking App UI Kit"
            noun = "Templates" if "stories" in slug else "UI kit"
            subprocess.run([sys.executable, "/root/divelux/freebies/gfx/_tools/mklicense.py", d, name, noun], check=True,
                           stdout=subprocess.DEVNULL)
    r = subprocess.run([sys.executable, "/root/divelux/freebies/gfx/_tools/check_listing.py"] +
                       [os.path.join(S.ROOT, s) for s in P])
    if bad or r.returncode:
        raise SystemExit("listing problems")


if __name__ == "__main__":
    main()
