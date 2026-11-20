# Notion template: Home sauna: upkeep and costs

How to build the template by hand in about ten minutes, so it can be shared as a public page and submitted to the Notion Template Gallery. Nothing here is published yet. The formulas below follow Notion's current formula syntax; test them once in your workspace after you paste them.

The page has two databases: **Upkeep tasks** (what to do and when it is next due) and **Costs** (what the sauna costs to run and maintain).

## 1. Create the page

1. New page. Title: `Home sauna: upkeep and costs`. Icon: any sauna, fire or wood icon. Cover: a plain warm color or a wood photo.
2. Under the title, add a callout with this text:
   > Tick off upkeep in the first table, log what the sauna costs in the second. General upkeep guidance: your heater manufacturer's manual comes first, and electrical work is for a licensed electrician.
3. Add a heading `Upkeep tasks`, type `/table` and choose **Table view → New database**. Name the database `Upkeep tasks`.
4. Add a heading `Costs` below it and create a second database the same way. Name it `Costs`.

## 2. Import the rows (fastest way)

- In the `Upkeep tasks` database menu (`•••`) choose **Merge with CSV** and pick `upkeep-tasks.csv`. This creates 22 tasks and all the columns.
- In the `Costs` database menu choose **Merge with CSV** and pick `costs.csv`. It brings the columns and 4 sample rows whose names start with `Example:`. Delete the sample rows before you share the page.

Then set the property types below. (Or skip the CSVs and add the properties by hand.)

## 3. Properties: Upkeep tasks

| Property | Type | Settings |
|---|---|---|
| Task | Title | from the CSV |
| Frequency | Select | Options: After every session, Weekly, Monthly, Yearly |
| Interval (days) | Number | 7, 30 or 365; empty for "After every session" |
| Area | Select | Options: Room, Benches, Floor, Door, Vents, Heater, Electrical, Lighting, Accessories, Safety |
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
| Category | Select | Options: Electricity, Firewood, Stones, Parts and repairs, Cleaning supplies, Accessories, Professional service, Other |
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
> Made by DIVELUX, makers of handmade wool sauna hats: [diveluxsaunahat.com](https://diveluxsaunahat.com). More free sauna tools: [diveluxsaunahat.com/pages/sauna-tools](https://diveluxsaunahat.com/pages/sauna-tools)

## 9. Publish and submit

1. Delete the `Example:` rows in `Costs` and clear every `Last done` date.
2. **Share → Publish → Publish to web**, and turn on **Allow duplicate as template**.
3. Submit the public link through the Notion template submission form (a Notion creator profile is required). Use the title, description and tags from `LISTING.md`, and a screenshot of the page as the cover. `preview.png` in this folder is a layout mockup, not a Notion screenshot; replace it with a real screenshot once the page exists.
