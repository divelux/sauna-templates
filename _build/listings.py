#!/usr/bin/env python3
"""Writes LISTING.md and README.md into every template folder and README.md into templates/. Checks the limits:
title <= 60 characters, short description <= 160, full description 150-220 words with one or two links."""
import os
import re

import tcommon as T

LICENSE = ("CC BY 4.0 (Creative Commons Attribution 4.0 International). Credit: DIVELUX, https://diveluxsaunahat.com\n"
           "The DIVELUX name and logo are © DIVELUX Inc. and are not covered by the license.")
BANNED = ["delve", "elevate", "unlock", "seamless", "game-changer", "tapestry", "realm", "embark", "testament", "boost",
          "detox", "toxins", "cure", "heals", "burns fat", "immune", "amazon", "best seller", "wet the hat", "soak"]
OPEN = "Opens in Excel, Google Sheets, Numbers and LibreOffice."

P = {}

P["home-sauna-build-budget"] = dict(
    name="Home Sauna Build Budget", kind="Spreadsheet (.xlsx) + CSV",
    title="Home Sauna Build Budget Spreadsheet (Free Template)",
    short="Free budget spreadsheet for building a home sauna: 50 cost lines in 13 categories, planned vs actual, contingency, paid and owed, and a chart.",
    full="""A home sauna build has more line items than most people expect. The heater is the obvious one; the permit, the vapor barrier, the door hardware and the electrician get forgotten. This spreadsheet lists them all.

The Budget sheet has 50 ready cost lines in 13 categories, from planning and permits through structure, insulation, interior wood, benches, door and glass, heater and stones, controls, electrical, ventilation, lighting and accessories to labor and delivery. For each line you type what you plan to pay, what it really cost, and whether it is paid. The sheet shows the difference and marks every line that went over.

The Summary sheet adds it up: planned and actual by category, a contingency cushion you set yourself, what is left, what is paid and still owed, plus a bar chart.

- Empty template and a filled-in example (sample numbers, not a quote)
- CSV with the full list of cost lines
- Drop-down lists, input checks, prints on US Letter

The file contains no price guidance: get real quotes. Electrical work belongs to a licensed electrician, and the heater manual decides the wiring.

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna tools: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna, home sauna, sauna build, sauna budget, DIY sauna, budget template, cost tracker, construction budget, Excel template, Google Sheets template",
    files=[("home-sauna-build-budget.xlsx", "the empty template: Budget, Summary (with chart), How to use"),
           ("home-sauna-build-budget-example.xlsx", "the same file filled in with sample numbers (not a quote)"),
           ("home-sauna-build-budget.csv", "the 50 cost lines with their categories, for Notion, Airtable or your own sheet"),
           ("preview.png", "rendering of the example file: Budget and Summary sheets"), ("README.md", "this file")],
    readme="""## How to use

1. Open `home-sauna-build-budget.xlsx`. On the **Budget** sheet every line is one cost. Reword lines, clear the ones you do not need, add your own in the empty rows. Pick the category from the drop-down.
2. Type what you expect to pay in **Planned**. When you buy or get an invoice, type the amount in **Actual** and set **Paid?** to Yes once it is paid.
3. Open **Summary** for totals by category, the contingency cushion, what is left, what is still owed, and the chart. The only cell to type in there is the contingency rate (10% is a placeholder).

`home-sauna-build-budget-example.xlsx` shows the file at work. Its numbers are round samples for a small indoor sauna. They are not prices and not a quote.

## Sheets and formulas

| Sheet | What it does |
|---|---|
| Budget | 70 rows: Category, Item, Planned, Actual, Difference, Paid?, Vendor / notes. `Difference = Actual - Planned`, shown only when Actual has a number; lines over plan turn orange. A total row under the header. |
| Summary | Planned, Actual and Over / under for each of the 13 categories (`SUMIF` on the Budget sheet), share spent, contingency amount (`planned total x rate`), budget with contingency, left in budget, paid so far, still to pay, contingency left. A bar chart of planned against actual. |
| How to use | The steps above, inside the file. |

The formulas were recalculated outside Excel with the Python package `formulas` and compared with an independent calculation; see `../_build/build_templates.py`.

## Good to know

- The file gives no price guidance. Prices depend on your region, the room and the materials: get real quotes.
- Electrical work: a licensed electrician and the permit your city requires. Heater, clearances and wiring: follow the manufacturer's manual.
- For a first idea of heater size, see the [Sauna Heater Sizing Sheet](../sauna-heater-sizing-sheet/) or the [online calculator](https://divelux.github.io/sauna-heater-calculator/).
- Other currencies: select the money columns and change the number format.""")

P["sauna-heater-sizing-sheet"] = dict(
    name="Sauna Heater Sizing Sheet", kind="Spreadsheet (.xlsx) + CSV",
    title="Sauna Heater Sizing Sheet: kW Calculator Spreadsheet",
    short="Free spreadsheet that sizes a sauna heater from room size, glass and stone area and log walls, using Harvia and HUUM published rules. Feet or meters.",
    full="""How big a heater does this room need? The answer is a short calculation that heater makers publish in their manuals. This spreadsheet does it for you and shows every step.

Type the inside size of the hot room in feet and inches or in meters, the area of glass and of stone, tile or brick with no insulation behind it, and whether the inside walls are bare log. Pick electric or wood-burning. The sheet returns:

- room volume and calculated volume, in m³ and cu ft
- for an electric heater, a power range in kW: 1 kW per 50 cu ft at the low end, 1 kW per m³ at the high end
- for a wood-burning stove, the calculated volume to shop by
- the same room under three published rules side by side (Harvia, HUUM, HUUM's North American sheet)

A second sheet runs the manufacturers' own worked examples through the same formulas, and a Sources sheet links to every document the factors come from.

This is a rule-of-thumb estimate. Always confirm with the heater manufacturer and a licensed electrician, and follow the manufacturer's manual. Infrared cabins are not covered.

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna tools: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna heater, heater sizing, kW calculator, sauna build, home sauna, electric sauna heater, wood sauna stove, Harvia, HUUM, Excel template",
    files=[("sauna-heater-sizing-sheet.xlsx", "the workbook: Calculator, Examples, Sources, How to use"),
           ("sauna-heater-sizing-sheet-examples.csv", "the six worked examples with inputs and results"),
           ("preview.png", "rendering of the Calculator, Examples and Sources sheets"), ("README.md", "this file")],
    readme="""> **Always confirm with the heater manufacturer and a licensed electrician.** This is a rule-of-thumb estimate. It cannot see your insulation, vents, climate or wiring. Follow the manufacturer's manual: the manual of the heater you buy has the final say on room volume, clearances, breaker and wire size.

## How to use

1. Open `sauna-heater-sizing-sheet.xlsx`. The **Calculator** sheet opens with a sample room (6 x 5 x 7 ft with a 12 sq ft glass door). Replace it with yours.
2. Choose the units: `ft` (feet and inches) or `m` (meters). Type length, width and ceiling height measured inside the hot room.
3. Add the area of uninsulated glass, and of stone, tile, brick or concrete with no insulation behind it. Say whether the inside walls are bare log. Pick Electric or Wood-burning.
4. Read the result. The Input check line tells you if a number is missing or out of range (rooms from 0.9 to 6 m a side, ceilings from 1.7 to 3 m, the same limits as the online calculator).

## The rules in the cells

The sheet uses the same rules as the DIVELUX [Sauna Heater Size Calculator](https://divelux.github.io/sauna-heater-calculator/). Every factor comes from a heater maker's published guidance:

| Step | Formula | Source |
|---|---|---|
| Room volume | length x width x height | |
| Cold surfaces | + 1.2 m³ for each m² of uninsulated glass, stone, tile, brick or concrete | Harvia |
| Log walls | room volume x 1.5 if the inside walls are bare log | Harvia |
| Calculated volume | room volume x (1.5 if log) + 1.2 x uninsulated area | Harvia |
| Power, high end | 1 kW per m³ of calculated volume | Harvia, HUUM |
| Power, low end | 1 kW per 50 cu ft (1.416 m³) | retail shortcut; equals Harvia's example of about 8.5 m³ at a minimum of 6 kW |
| Wood-burning stove | calculated volume only: wood stoves are rated by room volume | Harvia |
| Side by side | HUUM: 1 m³ per m². HUUM North American sheet: 4.92 cu ft per sq ft (1.5 m³ per m²). No HUUM figure for a log room | HUUM |

Conversion constants: 1 ft = 0.3048 m, 1 m³ = 35.3147 cu ft, 1 m² = 10.7639 sq ft.

## Sheets

| Sheet | What it does |
|---|---|
| Calculator | Inputs, result, the three-rule comparison, a note when glass and stone are 30% or more of the calculated volume |
| Examples | The manufacturers' worked examples through the same formulas: Harvia L30 manual (10 m³ + glass door, "about 12 m³": 11.9), Harvia wood stove guide (13.77 m³), HUUM article (11.88 m³), Harvia support (about 8.5 m³, minimum 6 kW) |
| Sources | Links to the Harvia and HUUM documents, checked in November 2026 |
| How to use | The method in plain words |

## Checks

`../_build/build_templates.py` recalculates the workbook with the Python package `formulas` and compares the Examples sheet with `heater.js` of the online calculator and with the published results. The sample room gives 210 cu ft, a calculated volume of 7.3 m³ (257 cu ft) and 5.1 to 7.3 kW, the same as the calculator.

## What it does not know

Insulation quality, vents, outdoor temperature, stone mass, altitude, and your home's wiring. Infrared cabins are sized differently and are not covered.""")

P["sauna-cleaning-rota"] = dict(
    name="Sauna Cleaning Rota for gyms and spas", kind="Spreadsheet (.xlsx) + CSV",
    title="Sauna Cleaning Rota for Gyms and Spas (Free Template)",
    short="Free cleaning rota for a gym, spa or club sauna: daily tasks by day with initials, weekly to yearly tasks with next-due dates, and a maintenance log.",
    full="""A shared sauna stays pleasant when the small jobs are done every day and somebody can see that they were done. This rota is for the staff of a gym, spa, hotel or club.

Three working sheets:

- Daily: one landscape page per sauna per week. Sixteen opening, through-the-day and closing tasks down the side, Monday to Sunday across the top. Staff initial each task; the sheet counts them and shows how complete the week is.
- Periodic: weekly, monthly, quarterly and yearly tasks. Type the date a task was last done; the next due date and a status (OK, Due, Not logged) calculate themselves.
- Log: a line for every repair, stone change or inspection, with room for a signature on the printed copy.

Every task can be reworded, and there are empty rows for your own. An example file shows a filled-in week. A CSV lists all 32 tasks with their frequency.

The tasks are general upkeep practice. Cleaning products follow your facility's policy and the product label; heater, stones and controls follow the manufacturer's manual; electrical work is for a licensed electrician; local health codes come first.

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna tools: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna cleaning, cleaning rota, cleaning schedule, gym sauna, spa operations, facility checklist, housekeeping log, maintenance log, Excel template, Google Sheets template",
    files=[("sauna-cleaning-rota.xlsx", "the empty template: Daily, Periodic, Log, How to use"),
           ("sauna-cleaning-rota-example.xlsx", "the same file with one sample week and sample dates (made-up names)"),
           ("sauna-cleaning-rota-tasks.csv", "all 32 tasks with frequency, for another system"),
           ("preview.png", "rendering of the example file: Daily and Periodic sheets"), ("README.md", "this file")],
    readme="""## How to use

1. **Daily** sheet: one copy per sauna per week. Type the facility, the room and the Monday the week starts on; the dates fill in. Put the name of the person on duty under each day.
2. When a task is done, the person who did it types their initials in that day's cell, or writes them by hand on a printed copy. The sheet prints on one landscape US Letter page for a clipboard by the door.
3. **Periodic** sheet: type the date in *Last done* and the initials. *Next due* and *Status* calculate themselves from today's date.
4. **Log** sheet: one line for anything worth a record. Print it and sign in the last column if your facility needs a signature.

`sauna-cleaning-rota-example.xlsx` shows a filled-in week. The names are made up, and its "Today" cell holds a fixed date so the example always looks the same.

## Sheets and formulas

| Sheet | What it does |
|---|---|
| Daily | 16 tasks in three groups (Opening, Through the day, Closing) by 7 days. Dates = week start + 0…6. *Done* = `COUNTA` of the initialed cells for each day; *Week complete* = all initialed cells / 112. |
| Periodic | 16 tasks plus 6 empty rows. *Every (days)*: Weekly 7, Monthly 30, Quarterly 91, Yearly 365. *Next due* = Last done + Every. *Status*: "Not logged" with no date, "Due" when Next due is before today (`TODAY()`), otherwise "OK". "Due" shows in orange. |
| Log | Date, Time, Area (drop-down), What was done, Done by, Checked by (signature), Notes. 40 rows. |
| How to use | The steps above, inside the file. |

The formulas were recalculated outside Excel with the Python package `formulas` and compared with an independent calculation; see `../_build/build_templates.py`.

## Good to know

- The task lists are a starting point built from general upkeep practice. Rewrite them to match your rooms and your health department's rules, which come first.
- Cleaning products and dilution: per your facility's policy and the product label. Avoid harsh chemicals on bare wood.
- Heater, stones and controls: follow the heater manufacturer's manual. Electrical inspection and repair: a licensed electrician.
- For a home sauna, see the printable [Sauna Care and Cleaning Schedule](../../printables/sauna-care-cleaning-schedule/).""")

P["sauna-booking-log"] = dict(
    name="Sauna Booking Log for clubs", kind="Spreadsheet (.xlsx) + CSV",
    title="Sauna Booking Log for Clubs (Free Spreadsheet)",
    short="Free booking log for a sauna club: date, slot, name, guests, paid yes/no. Shows seats left, flags overbooked slots and sums each day. Names only.",
    full="""A small sauna club does not need booking software to know who is coming on Saturday. It needs one sheet that everyone fills in the same way, and quick answers: is there room in this slot, and has this booking been paid?

- Bookings: one line per booking with the date, a slot from a drop-down, a name, the number of guests, paid yes or no, the amount and a note. A Seats left column counts every booking for the same date and slot and turns orange when a slot is overbooked.
- Summary: type a date and see that day slot by slot: capacity, booked seats, seats left, bookings, unpaid bookings and money received. Below it, the seven days from that date and the totals of the whole log.
- Settings: your own session times and the seats in each, up to 12 slots.

The log is built to hold a name and nothing more about a person. No phone numbers, no emails, no health notes: a first name and an initial is enough.

Included: the empty template, an example file with made-up bookings, and a CSV with the column headings.

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna tools: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna club, booking log, reservation sheet, booking template, community sauna, sauna sessions, capacity tracker, Excel template, Google Sheets template, club admin",
    files=[("sauna-booking-log.xlsx", "the empty template: Bookings, Summary, Settings, How to use"),
           ("sauna-booking-log-example.xlsx", "the same file with 14 made-up bookings over two days, one slot overbooked on purpose"),
           ("sauna-booking-log.csv", "the column headings and two example rows, for another system"),
           ("preview.png", "rendering of the example file: Bookings and Summary sheets"), ("README.md", "this file")],
    readme="""## How to use

1. **Settings** sheet: type your session times in the *Slot* column and the number of seats for each. Up to 12 slots. The times and the capacity of 8 in the file are placeholders.
2. **Bookings** sheet: one line per booking. Type the date, pick the slot from the drop-down, type a name and the number of guests. Set *Paid?* to Yes when it is paid and type the amount.
3. *Seats left* shows the free seats in that date and slot after every booking on the sheet is counted. Below zero it turns orange: the slot is overbooked.
4. **Summary** sheet: type a date in the white cell to see that day slot by slot and the seven days that start there.

`sauna-booking-log-example.xlsx` shows the file at work. The names and amounts are made up.

## Personal data

The log is meant to hold a name and nothing else about a person. Do not record phone numbers, emails, addresses, health details or card numbers in it; a first name and an initial is enough. If you need contact details, keep them in the system your club already uses for member data.

## Sheets and formulas

| Sheet | What it does |
|---|---|
| Bookings | 200 rows: Date, Slot, Name, Guests, Paid?, Amount, Note, Seats left. `Seats left = capacity of the slot - guests booked for the same date and slot`. |
| Summary | For the chosen date, per slot: Capacity, Booked seats, Seats left, Bookings, Unpaid, Received, and a day total. The same figures per day for seven days. Totals of the whole log. |
| Settings | Club name, 12 slot names with their capacity. Feeds the drop-down and the Summary. |
| How to use | The steps above, inside the file. |

The counting formulas use `SUMPRODUCT` with plain `=` tests on date and slot instead of `SUMIFS`, so a slot name such as `8:00 AM` is matched exactly as written and is never re-read as a time. An empty *Paid?* cell counts as unpaid.

The formulas were recalculated outside Excel with the Python package `formulas` and compared with an independent calculation; see `../_build/build_templates.py`.

## Good to know

- A cancelled booking: delete the line, or set Guests to 0 and write the reason in Note.
- A new month or season: save a copy of the file and clear the white cells on the Bookings sheet.
- Other currencies: select the Amount cells and change the number format.""")

P["notion-home-sauna-upkeep-costs"] = dict(
    name="Notion: Home sauna: upkeep and costs", kind="Notion build notes (.md) + 2 CSV",
    title="Home Sauna: Upkeep and Costs (Notion Template)",
    short="Free Notion template for home sauna owners: an upkeep task list with next-due dates and a cost log with totals by category and month. CSVs included.",
    full="""Owning a sauna comes with two small bookkeeping jobs: remembering what needs doing and when, and knowing what the sauna costs to run. This Notion template keeps both on one page.

Upkeep tasks is a database of 22 jobs, from the five-minute routine after every session to the yearly ones: restacking the stones, an electrician's check, sweeping the chimney of a wood stove. Each task has a frequency, an area and a last-done date. A formula works out the next due date and a status, so a "Due" view shows only what needs attention. Other views: a checklist for after every session, a board by area, a calendar.

Costs is a simple log: item, date, category (electricity, firewood, stones, parts and repairs, cleaning supplies, accessories, professional service), amount and vendor, with a sum at the bottom and views by category and by month.

What you get:

- notion-template.md: step-by-step build notes with every property, formula and view
- upkeep-tasks.csv and costs.csv, ready for Notion's CSV import
- a layout mockup of the finished page

The tasks are general upkeep guidance. Your heater manufacturer's manual comes first, and electrical work is for a licensed electrician.

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna tools: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="Notion template, home sauna, sauna maintenance, upkeep tracker, home maintenance, cost tracker, expense log, checklist, sauna care, household",
    files=[("notion-template.md", "how to build the page: properties, formulas, views, texts"),
           ("upkeep-tasks.csv", "22 upkeep tasks with frequency, interval in days, area and notes"),
           ("costs.csv", "the cost log columns with four sample rows (made-up amounts; delete them)"),
           ("preview.png", "layout mockup of the page, drawn from the two CSVs; not a Notion screenshot"), ("README.md", "this file")],
    readme="""## What is here

Nothing in this folder is a published Notion page yet. It holds everything needed to build one in about ten minutes:

1. Follow `notion-template.md`: create the page and two databases, **Upkeep tasks** and **Costs**.
2. Import `upkeep-tasks.csv` and `costs.csv` with *Merge with CSV*, then set the property types and paste the formulas from the notes.
3. Add the views, delete the `Example:` cost rows, publish with "Allow duplicate as template" and submit the link.

`preview.png` is a layout mockup drawn from the two CSVs in our own style. It is not a screenshot of Notion; replace it with a real screenshot once the page exists.

## Structure

| Database | Properties | Views |
|---|---|---|
| Upkeep tasks | Task, Frequency, Interval (days), Area, Who, Last done, Next due (formula), Status (formula), Notes | All tasks, After every session, Due, By area, Calendar, For a professional |
| Costs | Item, Date, Category, Amount, Vendor, Task (relation, optional), Month (formula), Year (formula), Notes | All costs, By category, By month, This year |

Formulas: `Next due = dateAdd(Last done, Interval (days), "days")`; `Status` is "Every session", "Not logged", "Due" or "OK"; `Month = formatDate(Date, "YYYY-MM")`. They are written for Notion's current formula syntax and have not been run in a live workspace from here: test them once after pasting.

## Good to know

- The 22 tasks are the generally accepted home-sauna routine, the same list as the printable [Sauna Care and Cleaning Schedule](../../printables/sauna-care-cleaning-schedule/). Saunas, heaters and local codes differ: follow the manufacturer's manual for your heater, and leave electrical work to a licensed electrician.
- The amounts in `costs.csv` are made-up sample numbers, not prices.
- Prefer a spreadsheet? The CSVs open in Excel and Google Sheets as they are.""")

ORDER = ["home-sauna-build-budget", "sauna-heater-sizing-sheet", "sauna-cleaning-rota", "sauna-booking-log", "notion-home-sauna-upkeep-costs"]


def main():
    bad = 0
    for slug in ORDER:
        p = P[slug]
        d = os.path.join(T.ROOT, slug)
        names = [f for f, _ in p["files"]]
        words = len(re.findall(r"[A-Za-zÀ-ÿ0-9°'’\-]+", p["full"]))
        links = re.findall(r"https://diveluxsaunahat\.com\S*", p["full"])
        text = (p["full"] + p["short"] + p["title"]).lower()
        checks = [(len(p["title"]) <= 60, f"title {len(p['title'])} chars"), (len(p["short"]) <= 160, f"short {len(p['short'])} chars"),
                  (150 <= words <= 220, f"full {words} words"), (1 <= len(links) <= 2, f"{len(links)} links"),
                  (all(os.path.exists(os.path.join(d, f)) for f in names if f != "README.md"), "a listed file is missing"),
                  (not [b for b in BANNED if b in text], "banned word: " + ", ".join(b for b in BANNED if b in text))]
        missing = sorted(set(os.listdir(d)) - set(names) - {"LISTING.md", "README.md"})
        status = "OK" if all(ok for ok, _ in checks) and not missing else "!!"
        bad += status != "OK"
        print(f"{status} {slug}: title {len(p['title'])}, short {len(p['short'])}, full {words} words, {len(links)} links",
              [m for ok, m in checks if not ok], ("unlisted files: " + ", ".join(missing)) if missing else "")
        files = "\n".join(f"- `{f}`" for f in names)
        with open(os.path.join(d, "LISTING.md"), "w", encoding="utf-8") as f:
            f.write(f"""# LISTING: {p['name']}

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
- Format: {p['kind']}{'. ' + OPEN if 'xlsx' in p['kind'] else ''}
- Language: English (en-US) · Version 1.0 · 2026-11
- Price: free
""")
        table = "\n".join(f"| [`{f}`]({f}) | {what} |" for f, what in p["files"] if f != "README.md")
        intro = p["full"].split("\n\n")[0]
        with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as f:
            f.write(f"""# {p['title'].split(' (')[0].split(':')[0] if slug != 'notion-home-sauna-upkeep-costs' else 'Home sauna: upkeep and costs (Notion template)'}

{p['short']}

Made by [DIVELUX]({T.SITE}), makers of handmade wool sauna hats. More free sauna tools: {T.TOOLS}

![Preview](preview.png)

## Files

| File | What it is |
|---|---|
{table}

{p['readme']}

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Free to use, share and adapt. Credit DIVELUX with a link to {T.SITE}.
The DIVELUX name and logo are © DIVELUX Inc. and are not covered by the license.
""")
    rows = "\n".join(
        f"| {i} | [{P[s]['name']}]({s}/) | ![{P[s]['name']}]({s}/preview.png) | {P[s]['kind']} | "
        + "<br>".join(f"[`{f}`]({s}/{f})" for f, _ in P[s]["files"] if f not in ("preview.png", "README.md")) + " |"
        for i, s in enumerate(ORDER, 1))
    with open(os.path.join(T.ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"""# Free sauna spreadsheet and Notion templates

Five free templates for people who build, own or run a sauna. Four are spreadsheets that open in Excel, Google Sheets,
Numbers and LibreOffice; one is a Notion page with its import files. Every folder has the template, a CSV, a `preview.png`,
a `README.md` and a `LISTING.md` with ready-to-paste title, descriptions, tags and license. Free to use and share under CC BY 4.0.

Made by DIVELUX, makers of wool sauna hats: {T.SITE} ·
more free tools: {T.TOOLS}

| # | Template | Preview | Format | Files |
|---|---|---|---|---|
{rows}

## Using the spreadsheets

- White cells are for typing. Gray cells calculate themselves; leave them alone.
- Each workbook has a "How to use" sheet. Files ending in `-example.xlsx` show the template filled in with sample data (made-up names and numbers).
- Google Sheets: upload the `.xlsx` to Google Drive, open it, then File → Save as Google Sheets. Check the drop-downs once after the conversion (and the chart in the budget file).
- The fonts named in the files are Bricolage Grotesque and Inter (SIL Open Font License 1.1). Without them installed, your spreadsheet program picks a default font and everything still works.
- Every sheet is set up to print on US Letter.

## License

{LICENSE}

Every sheet carries the credit line "{T.CREDIT}" with a link. Please keep it when you share or adapt the files.

## Rebuilding

Sources live in `_build/`. `python3 _build/build_templates.py` writes the workbooks and CSVs with openpyxl, recalculates every
workbook with the Python package `formulas` and fails on any Excel error value, compares the key totals with an independent
calculation (the heater sheet also against `heater.js` of the online calculator and the manufacturers' worked examples), and draws
the previews with Playwright (one Chromium at a time, under `flock /tmp/freebies-chromium.lock`). `--no-preview` skips the images.
`python3 _build/listings.py` rewrites the LISTING.md and README.md files and checks the length limits.

The previews are renderings of the real workbook cells, not screenshots of Excel. The Notion preview is a layout mockup.

General information: not professional, electrical or medical advice. Electrical work is for a licensed electrician; for heaters,
follow the manufacturer's manual.
""")
    print("listing problems:", bad)
    return bad


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
