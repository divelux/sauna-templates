# Sauna Club Story Templates

Eight story templates for saunas, bathhouses and sauna clubs, 1080 × 1920 px.
Made by DIVELUX, makers of wool sauna hats — https://diveluxsaunahat.com · more free tools: https://diveluxsaunahat.com/pages/sauna-tools

| # | Story | Files |
|---|---|---|
| 1 | Session announcement | `svg/01-session-announcement.svg` · `png/01-session-announcement.png` |
| 2 | Sauna rules | `svg/02-sauna-rules.svg` · `png/02-sauna-rules.png` |
| 3 | Aufguss tonight | `svg/03-aufguss-tonight.svg` · `png/03-aufguss-tonight.png` |
| 4 | Weekly schedule | `svg/04-weekly-schedule.svg` · `png/04-weekly-schedule.png` |
| 5 | First time? What to bring | `svg/05-first-time-what-to-bring.svg` · `png/05-first-time-what-to-bring.png` |
| 6 | Cold plunge open | `svg/06-cold-plunge-open.svg` · `png/06-cold-plunge-open.png` |
| 7 | Your guest's words | `svg/07-guest-words.svg` · `png/07-guest-words.png` |
| 8 | Members-only event | `svg/08-members-only-event.svg` · `png/08-members-only-event.png` |

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
