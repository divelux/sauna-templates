# Aufguss Schedule Board

Free editable Aufguss schedule for saunas and spas: times, sessions, scents, sauna masters and rooms. A3 and Tabloid posters plus a 1920 x 1080 lobby TV screen.

![Aufguss Schedule Board](preview.png)

## Files

- `aufguss-schedule-board.html`
- `aufguss-schedule-board-a3.pdf`
- `aufguss-schedule-board-tabloid.pdf`
- `aufguss-schedule-board-tv.png`
- `aufguss-schedule-board-a3.svg`
- `aufguss-schedule-board-tabloid.svg`
- `aufguss-schedule-board-tv.svg`
- `preview.png`
- `LICENSE`

## Edit in your browser

1. Open `aufguss-schedule-board.html` in Chrome, Edge, Firefox or Safari. Nothing is loaded from the internet: the fonts are inside the file.
2. Click any text and type. The print board and the TV screen share their fields: change a time in one and it changes in the other. Leave a row empty if you run fewer sessions.
3. Pick the size in the dark bar at the top, then **Print / Save PDF**. In the print dialog: scale 100% (actual size),
   margins None, background graphics on.
4. Your edits are saved in this browser only (local storage), never uploaded. **Reset** brings back the sample text.
   To keep or share a finished version, save it as a PDF.

Sizes: `?size=a3` (default), `?size=tabloid` (11 × 17 in), `?size=tv` (1920 × 1080 px). You can also add the size to the address by hand, for example `aufguss-schedule-board.html?size=a3`.

## Printing

A3 and Tabloid print on large-format office printers or at any copy shop. Keep paper out of the hot room: hang the board in the lobby or the changing room, or laminate it.

**TV:** open the file with `?size=tv` on the computer or stick plugged into the screen and press **Full screen**. The page is static: update the times when the program changes.

## Figma and other design apps

Every size also comes as a plain SVG made from the same layout:

1. In Figma, drag the `.svg` file onto the canvas (or File → Import). Illustrator, Inkscape, Affinity and Penpot open it too.
2. Text stays live text in **Bricolage Grotesque** and **Inter**. Both are free Google Fonts and are built into Figma;
   for desktop apps, install them from fonts.google.com.
3. Layers are grouped and named after the fields (`club-name`, `date`, `item-price` …). Each line of a paragraph is its own
   text layer, so rewrap long paragraphs by hand or join the lines into one text box.
4. Sizes are in pixels at 96 per inch (the CSS pixel), so a US Letter page is 816 × 1056.

## Sample text

Every name, date, time and price in the files is a placeholder ("Your Sauna Club", "$00", "Name"). Replace them before you print.
Health notes are kept general; check any wording you add with your own rules and local requirements.

## Credits and license

Template by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com · more free tools: https://diveluxsaunahat.com/pages/sauna-tools

CC BY 4.0 (Creative Commons Attribution 4.0 International). Credit: DIVELUX, https://diveluxsaunahat.com
The DIVELUX name and logo are © DIVELUX Inc. and are not covered by the license. Fonts: Bricolage Grotesque and Inter (SIL Open Font License 1.1).
No illustrations; type and color only.

You may use, change and print these templates for your business, including for commercial use. Please keep the small
credit line ("Template by DIVELUX · diveluxsaunahat.com · CC BY 4.0") or credit DIVELUX somewhere reasonable, such as your website.

## Rebuilding

The files are built by `templates/_build/w3_build.py` (writes the HTML, renders PDFs, PNGs and SVGs with one headless Chromium,
compares every SVG with the page pixel by pixel and runs an editing test) and `templates/_build/w3_listings.py` (this README and LISTING.md).
