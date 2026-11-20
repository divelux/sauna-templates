"""17. Notion: "Home sauna: upkeep and costs". Writes the two import CSVs and notion-template.md, and the mockup for preview.png.
Upkeep tasks are the generally accepted home-sauna routine (the same list as the printable Sauna Care and Cleaning Schedule)."""
import csv
import os

import tcommon as T

SLUG = "notion-home-sauna-upkeep-costs"
NAME = "Home sauna: upkeep and costs"
CALLOUT = ("Tick off upkeep in the first table, log what the sauna costs in the second. General upkeep guidance: "
           "your heater manufacturer's manual comes first, and electrical work is for a licensed electrician.")
AREAS = ["Room", "Benches", "Floor", "Door", "Vents", "Heater", "Electrical", "Lighting", "Accessories", "Safety"]
FREQS = ["After every session", "Weekly", "Monthly", "Yearly"]
COST_CATS = ["Electricity", "Firewood", "Stones", "Parts and repairs", "Cleaning supplies", "Accessories", "Professional service", "Other"]

TASKS = [  # task, frequency, interval days, area, who, notes
    ("Prop the door and open the vent so the room can dry", "After every session", "", "Room", "Me", ""),
    ("Wipe sweat off the benches with a clean cloth and plain water", "After every session", "", "Benches", "Me", ""),
    ("Empty the bucket and hang up the ladle", "After every session", "", "Accessories", "Me", ""),
    ("Take towels, seat covers and hats out to air dry", "After every session", "", "Accessories", "Me", ""),
    ("Lift floor mats or duckboards so the floor dries", "After every session", "", "Floor", "Me", ""),
    ("Check that the heater is off and nothing is left on or near it", "After every session", "", "Heater", "Me", ""),
    ("Sweep or vacuum the floor, then mop it with a mild cleaner", "Weekly", 7, "Floor", "Me", "Or every few sessions."),
    ("Wash benches and backrests with warm water and a soft brush", "Weekly", 7, "Benches", "Me", "No bleach, no ammonia on the wood."),
    ("Rinse the bucket and ladle and let them dry", "Weekly", 7, "Accessories", "Me", ""),
    ("Clean the glass door", "Weekly", 7, "Door", "Me", "Spray the cloth, not the wood."),
    ("Wash seat towels and bench covers", "Weekly", 7, "Accessories", "Me", ""),
    ("Look over the benches for stains and rough spots; sand lightly with fine sandpaper", "Monthly", 30, "Benches", "Me", ""),
    ("Check that the door opens and closes easily; tighten loose hinges and handles", "Monthly", 30, "Door", "Me", ""),
    ("Clear dust from the air vents", "Monthly", 30, "Vents", "Me", ""),
    ("Check the heater guard, benches and backrests for anything loose", "Monthly", 30, "Benches", "Me", ""),
    ("Check the light, its cover and the thermometer", "Monthly", 30, "Lighting", "Me", ""),
    ("Take the stones out, discard cracked or crumbling ones, rinse the rest and restack loosely", "Yearly", 365, "Heater", "Me",
     "Stone type and timing: follow your heater manufacturer's manual."),
    ("Have the wiring, controls and heating elements checked", "Yearly", 365, "Electrical", "Professional", "A licensed electrician."),
    ("Wood stove: have the chimney and flue swept and inspected", "Yearly", 365, "Heater", "Professional", "Follow your stove manufacturer's manual."),
    ("Deep-clean the benches and sand worn spots", "Yearly", 365, "Benches", "Me", "Treat wood only with products made for sauna interiors."),
    ("Check the floor drain, the door seal and, outdoors, the roof and cladding", "Yearly", 365, "Room", "Me", ""),
    ("Test smoke and carbon monoxide alarms near the sauna", "Yearly", 365, "Safety", "Me", ""),
]
TASK_HEAD = ["Task", "Frequency", "Interval (days)", "Area", "Who", "Last done", "Notes"]
COSTS = [  # sample rows, clearly marked; amounts are placeholders, not prices
    ("Example: box of sauna stones", "2027-01-10", "Stones", 45, "", "Sample row with a made-up amount. Delete it."),
    ("Example: electrician's yearly check", "2027-02-03", "Professional service", 180, "", "Sample row with a made-up amount. Delete it."),
    ("Example: bench cleaner", "2027-02-14", "Cleaning supplies", 16, "", "Sample row with a made-up amount. Delete it."),
    ("Example: firewood", "2027-03-01", "Firewood", 120, "", "Sample row with a made-up amount. Delete it."),
]
COST_HEAD = ["Item", "Date", "Category", "Amount", "Vendor", "Notes"]

MD = f"""# Notion template: {NAME}

How to build the template by hand in about ten minutes, so it can be shared as a public page and submitted to the Notion Template Gallery. Nothing here is published yet. The formulas below follow Notion's current formula syntax; test them once in your workspace after you paste them.

The page has two databases: **Upkeep tasks** (what to do and when it is next due) and **Costs** (what the sauna costs to run and maintain).

## 1. Create the page

1. New page. Title: `{NAME}`. Icon: any sauna, fire or wood icon. Cover: a plain warm color or a wood photo.
2. Under the title, add a callout with this text:
   > {CALLOUT}
3. Add a heading `Upkeep tasks`, type `/table` and choose **Table view → New database**. Name the database `Upkeep tasks`.
4. Add a heading `Costs` below it and create a second database the same way. Name it `Costs`.

## 2. Import the rows (fastest way)

- In the `Upkeep tasks` database menu (`•••`) choose **Merge with CSV** and pick `upkeep-tasks.csv`. This creates {len(TASKS)} tasks and all the columns.
- In the `Costs` database menu choose **Merge with CSV** and pick `costs.csv`. It brings the columns and {len(COSTS)} sample rows whose names start with `Example:`. Delete the sample rows before you share the page.

Then set the property types below. (Or skip the CSVs and add the properties by hand.)

## 3. Properties: Upkeep tasks

| Property | Type | Settings |
|---|---|---|
| Task | Title | from the CSV |
| Frequency | Select | Options: {", ".join(FREQS)} |
| Interval (days) | Number | 7, 30 or 365; empty for "After every session" |
| Area | Select | Options: {", ".join(AREAS)} |
| Who | Select | Options: Me, Professional |
| Last done | Date | the date you last finished the task |
| Next due | Formula | see below |
| Status | Formula | see below |
| Notes | Text | |

**Next due**

```
dateAdd(prop("Last done"), prop("Interval (days)"), "days")
```

It stays empty until `Last done` has a date, and for tasks with no interval.

**Status**

```
if(empty(prop("Interval (days)")), "Every session", if(empty(prop("Last done")), "Not logged", if(dateAdd(prop("Last done"), prop("Interval (days)"), "days") < now(), "Due", "OK")))
```

## 4. Properties: Costs

| Property | Type | Settings |
|---|---|---|
| Item | Title | what you paid for |
| Date | Date | |
| Category | Select | Options: {", ".join(COST_CATS)} |
| Amount | Number | Number format: US dollar (or your currency) |
| Vendor | Text | |
| Task | Relation | optional: relate to `Upkeep tasks`, for costs that belong to a task (new stones, the electrician's visit) |
| Month | Formula | see below |
| Year | Formula | see below |
| Notes | Text | |

**Month**

```
formatDate(prop("Date"), "YYYY-MM")
```

**Year**

```
formatDate(prop("Date"), "YYYY")
```

## 5. Totals row

Hover under the last row of each table and set **Calculate**:

| Database | Column | Calculate |
|---|---|---|
| Upkeep tasks | Task | Count all |
| Costs | Amount | Sum |
| Costs | Item | Count all |

## 6. Views

**Upkeep tasks**

| View | Type | Setup |
|---|---|---|
| All tasks | Table | Group by: Frequency. Sort: Next due ascending. |
| After every session | List | Filter: Frequency is "After every session". Show: Task only. A five-minute checklist. |
| Due | Table | Filter: Status is "Due" or Status is "Not logged". Sort: Next due ascending. Show: Task, Frequency, Last done, Next due. |
| By area | Board | Group by: Area. Card preview: none. Show: Frequency, Status. |
| Calendar | Calendar | By: Next due. |
| For a professional | Table | Filter: Who is "Professional". |

**Costs**

| View | Type | Setup |
|---|---|---|
| All costs | Table | Sort: Date descending. Totals row: Amount = Sum. |
| By category | Board | Group by: Category. Board column calculation: Sum of Amount. |
| By month | Table | Group by: Month. Each group shows its Sum of Amount. |
| This year | Table | Filter: Date is within "This year". Totals row: Amount = Sum. |

## 7. "Done today" button (optional)

Inside the `Upkeep tasks` database add a **Button** property named `Done today`. Action: **Edit property → Last done → Today**. One click moves the task's next due date forward.

## 8. Text for the bottom of the page

> **How to use.** When you finish a task, set `Last done` to today (or press `Done today`). `Next due` and `Status` update on their own. After each purchase or service visit, add a row to `Costs`; the totals row and the By month view show what the sauna costs to run.
>
> General upkeep guidance for stove-heated home saunas. Saunas, heaters and local codes differ: follow the manufacturer's manual for your heater, use only products made for sauna interiors on the wood, and leave electrical work to a licensed electrician.
>
> Made by DIVELUX, makers of handmade wool sauna hats: [diveluxsaunahat.com]({T.SITE}). More free sauna tools: [diveluxsaunahat.com/pages/sauna-tools]({T.TOOLS})

## 9. Publish and submit

1. Delete the `Example:` rows in `Costs` and clear every `Last done` date.
2. **Share → Publish → Publish to web**, and turn on **Allow duplicate as template**.
3. Submit the public link through the Notion template submission form (a Notion creator profile is required). Use the title, description and tags from `LISTING.md`, and a screenshot of the page as the cover. `preview.png` in this folder is a layout mockup, not a Notion screenshot; replace it with a real screenshot once the page exists.
"""


def main():
    d = os.path.join(T.ROOT, SLUG)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "upkeep-tasks.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(TASK_HEAD)
        for task, freq, days, area, who, memo in TASKS:
            w.writerow([task, freq, days, area, who, "", memo])
    with open(os.path.join(d, "costs.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COST_HEAD)
        for row in COSTS:
            w.writerow(row)
    with open(os.path.join(d, "notion-template.md"), "w", encoding="utf-8") as f:
        f.write(MD)
    return []


def mock_html():
    """Layout mockup of the Notion page, drawn from the same rows as the CSVs."""
    import html
    e = lambda s: html.escape(str(s))
    tag = lambda s, c="#ede8df": f'<span class="tag" style="background:{c}">{e(s)}</span>'
    fc = {"After every session": "#f8dfc6", "Weekly": "#f5c7a0", "Monthly": "#ede8df", "Yearly": "#e3ddd3"}
    picks = [0, 1, 5, 6, 7, 9, 11, 13, 16, 17, 18, 21]
    trs = ""
    for i in picks:
        task, freq, days, area, who, memo = TASKS[i]
        status = "Every session" if days == "" else "Not logged"
        trs += (f"<tr><td class='t'>{e(task)}</td><td>{tag(freq, fc[freq])}</td><td class='n'>{days}</td><td>{tag(area)}</td>"
                f"<td>{tag(who)}</td><td class='m'></td><td class='m'></td><td class='m'>{status}</td></tr>")
    crs = ""
    for item, date, cat, amount, vendor, memo in COSTS:
        crs += (f"<tr><td class='t'>{e(item)}</td><td>{e(date)}</td><td>{tag(cat)}</td><td class='n'>${amount:,.2f}</td>"
                f"<td class='m'>{e(date[:7])}</td><td class='m'>{e(memo)}</td></tr>")
    total = sum(r[3] for r in COSTS)
    views1 = "".join(f'<span class="{"on" if k == 0 else ""}">{v}</span>' for k, v in enumerate(
        ["All tasks", "After every session", "Due", "By area", "Calendar", "For a professional"]))
    views2 = "".join(f'<span class="{"on" if k == 0 else ""}">{v}</span>' for k, v in enumerate(["All costs", "By category", "By month", "This year"]))
    return f"""<div class="np">
<div class="cap">Layout mockup of the Notion page, drawn from upkeep-tasks.csv and costs.csv. Not a Notion screenshot.</div>
<h1>{e(NAME)}</h1>
<div class="callout"><i></i><p>{e(CALLOUT)}</p></div>
<h2>Upkeep tasks</h2><div class="views">{views1}</div>
<table><thead><tr><th style="width:34%">Task</th><th>Frequency</th><th>Interval (days)</th><th>Area</th><th>Who</th><th>Last done</th><th>Next due</th><th>Status</th></tr></thead>
<tbody>{trs}</tbody><tfoot><tr><td class="m">Count {len(TASKS)} · {len(picks)} shown here</td><td colspan="7"></td></tr></tfoot></table>
<h2>Costs</h2><div class="views">{views2}</div>
<table><thead><tr><th style="width:30%">Item</th><th>Date</th><th>Category</th><th>Amount</th><th>Month</th><th>Notes</th></tr></thead>
<tbody>{crs}</tbody><tfoot><tr><td class="m">Count {len(COSTS)}</td><td></td><td></td><td class="n"><b>Sum ${total:,.2f}</b></td><td colspan="2"></td></tr></tfoot></table>
<p class="foot">Made by DIVELUX, makers of wool sauna hats — diveluxsaunahat.com</p>
</div>"""


MOCK_CSS = """
.np{width:1240px;background:#fffdf9;padding:30px 54px 34px;box-shadow:0 2px 14px rgba(27,21,18,.22);font-size:13px;color:#1b1512}
.np .cap{font-size:11px;color:#6f655c;border:1px dashed #b9afa2;border-radius:6px;padding:5px 10px;display:inline-block;margin-bottom:18px}
.np h1{font-family:"Bricolage Grotesque",Arial,sans-serif;font-weight:800;font-size:38px;letter-spacing:-.015em;margin:0 0 14px;line-height:1.05}
.np h2{font-family:"Bricolage Grotesque",Arial,sans-serif;font-weight:700;font-size:21px;margin:24px 0 6px}
.np .callout{display:flex;gap:12px;background:#f6f3ee;border-radius:6px;padding:13px 16px;align-items:flex-start}
.np .callout i{flex:none;width:10px;height:10px;border-radius:50%;background:#f0762e;margin-top:5px}
.np .callout p{margin:0;font-size:13.5px;line-height:1.45;color:#3d332c}
.np .views{display:flex;gap:4px;border-bottom:1px solid #dcd4c8;margin-bottom:0}
.np .views span{padding:6px 10px;font-size:12.5px;color:#6f655c}
.np .views span.on{color:#1b1512;font-weight:600;border-bottom:2px solid #1b1512}
.np table{width:100%;border-collapse:collapse;table-layout:auto}
.np th{font-weight:500;font-size:12px;color:#6f655c;text-align:left;padding:7px 8px;border-bottom:1px solid #dcd4c8;border-right:1px solid #ede8df;white-space:nowrap}
.np td{padding:6px 8px;border-bottom:1px solid #ede8df;border-right:1px solid #ede8df;white-space:normal;line-height:1.3;font-size:12.5px;vertical-align:top;overflow:hidden}
.np td:last-child,.np th:last-child{border-right:0}
.np td.t{font-weight:600}
.np td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.np td.m{color:#6f655c}
.np tfoot td{border-bottom:0;font-size:11.5px}
.np .tag{display:inline-block;border-radius:4px;padding:1px 7px;font-size:11.5px;white-space:nowrap;color:#3d332c}
.np .foot{margin:22px 0 0;font-size:11px;color:#6f655c}
"""

if __name__ == "__main__":
    main()
