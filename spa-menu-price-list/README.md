# Spa and Sauna Menu and Price List

Free editable spa and sauna menu: sessions, treatments, add-ons and memberships with prices. US Letter, A4, a 1080 x 1350 post and Figma-ready SVG.

![Spa and Sauna Menu and Price List](preview.png)

## Files

- `spa-menu-price-list.html`
- `spa-menu-price-list-letter.pdf`
- `spa-menu-price-list-a4.pdf`
- `spa-menu-price-list-post.png`
- `spa-menu-price-list-letter.svg`
- `spa-menu-price-list-a4.svg`
- `spa-menu-price-list-post.svg`
- `preview.png`
- `LICENSE`

## Edit in your browser

1. Open `spa-menu-price-list.html` in Chrome, Edge, Firefox or Safari. Nothing is loaded from the internet: the fonts are inside the file.
2. Click any text and type. Hover a menu line to show **Remove**; **+ Add line** under a section adds one. The club name in the header and in the footer change together.
3. Pick the size in the dark bar at the top, then **Print / Save PDF**. In the print dialog: scale 100% (actual size),
   margins None, background graphics on.
4. Your edits are saved in this browser only (local storage), never uploaded. **Reset** brings back the sample text.
   To keep or share a finished version, save it as a PDF.

Sizes: `?size=letter` (default), `?size=a4`, `?size=post` (1080 × 1350 px). You can also add the size to the address by hand, for example `spa-menu-price-list.html?size=letter`.

## Printing

Print on heavy matte paper or card stock. For a table menu, print on both sides of one sheet or laminate it.

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
The stove illustration comes from the DIVELUX Sauna Illustrations set (CC BY 4.0).

You may use, change and print these templates for your business, including for commercial use. Please keep the small
credit line ("Template by DIVELUX · diveluxsaunahat.com · CC BY 4.0") or credit DIVELUX somewhere reasonable, such as your website.

## Rebuilding

The files are built by `templates/_build/w3_build.py` (writes the HTML, renders PDFs, PNGs and SVGs with one headless Chromium,
compares every SVG with the page pixel by pixel and runs an editing test) and `templates/_build/w3_listings.py` (this README and LISTING.md).
