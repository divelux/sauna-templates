"""15. Sauna Cleaning Rota for gyms and spas: a daily sheet for one week, periodic tasks with next-due dates, a log.
Only generally accepted upkeep steps. Product-specific steps defer to the heater manufacturer's manual,
cleaning products to the facility's policy and the product label, electrics to a licensed electrician."""
import csv
import datetime as dt
import os

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment

import tcommon as T

SLUG = "sauna-cleaning-rota"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

DAILY = [
    ("Opening", [
        "Look over benches, floor and door: clean, dry, nothing left behind",
        "Heater guard in place, nothing on or near the heater",
        "Switch the heater on as the manufacturer's manual says",
        "Thermometer reads within your posted range before guests enter",
        "Light works; door opens and closes freely",
    ]),
    ("Through the day", [
        "Walk-through, morning: pick up towels and litter, wipe wet spots",
        "Walk-through, midday: pick up towels and litter, wipe wet spots",
        "Walk-through, evening: pick up towels and litter, wipe wet spots",
        "Fresh water in the bucket (only if water on the stones is allowed)",
    ]),
    ("Closing", [
        "Switch the heater off as the manual says and check that it is off",
        "Wash benches and backrests (cleaner per facility policy and label)",
        "Sweep and mop the floor; clear the drain cover",
        "Clean the glass door and the handles",
        "Empty and rinse the bucket and ladle; hang to dry",
        "Take out used towels and mats; lift duckboards so the floor dries",
        "Prop the door open and leave the vent open so the room dries",
    ]),
]
N_DAILY = sum(len(t) for _, t in DAILY)

PERIODIC = [
    ("Scrub benches, backrests and bench undersides with a soft brush", "Weekly", "Cleaner per facility policy and product label."),
    ("Wash the walls at splash height and behind the benches", "Weekly", ""),
    ("Lift duckboards; clean the floor and the drain underneath", "Weekly", ""),
    ("Wipe dust from air vents and the light cover", "Weekly", ""),
    ("Check benches, backrests and heater guard for loose boards or fasteners", "Weekly", "Close the room until a loose part is fixed."),
    ("Check door hinges, handle and seal", "Weekly", ""),
    ("Check that rules and safety signs are posted and readable", "Weekly", ""),
    ("Inspect the stones: remove cracked or crumbling ones, restack loosely", "Monthly", "Stones and timing: follow the heater manufacturer's manual."),
    ("Sand rough or stained spots on the benches lightly", "Monthly", ""),
    ("Check thermometer, timer and controls against the manual", "Monthly", "Follow the heater manufacturer's manual."),
    ("Test the emergency call button, if fitted", "Monthly", "Per your facility's policy."),
    ("Test smoke and carbon monoxide alarms near the sauna", "Monthly", "Schedule per your fire code and facility policy."),
    ("Deep-clean benches; treat wood only with sauna-interior products", "Quarterly", ""),
    ("Review this log with the manager", "Quarterly", ""),
    ("Heater, controls and wiring inspected by a licensed electrician", "Yearly", "Or as the manufacturer and local code require."),
    ("Replace the stones as the heater manual says", "Yearly", "Heavily used rooms may need it sooner: follow the manual."),
]
EVERY = {"Weekly": 7, "Monthly": 30, "Quarterly": 91, "Yearly": 365}
P_FIRST = 6
P_LAST = P_FIRST + len(PERIODIC) + 5          # a few empty rows for your own tasks
LOG_ROWS = 40

HOWTO = [
    ("h", "How to use this rota"),
    ("p", "1. Daily sheet: one copy per sauna per week. Type the facility, the room and the Monday the week starts on; the dates fill in. Put the name of the person on duty under each day."),
    ("p", "2. When a task is done, the person who did it types their initials in that day's cell (or writes them by hand on a printed copy). The Done row counts the initialed tasks for each day, and Week complete shows the share of all cells filled."),
    ("p", "3. Periodic sheet: weekly, monthly, quarterly and yearly tasks. Type the date in Last done and the initials. Next due and Status calculate themselves from today's date. \"Due\" means the next date has passed."),
    ("p", "4. Log sheet: one line for anything worth a record: a repair, a stone change, an electrician's visit, a closed room. Print it and sign in the last column if your facility needs a signature."),
    ("p", "5. Printing: every sheet is set up for US Letter. The Daily sheet prints on one landscape page for a clipboard by the door."),
    ("h", "Change it to fit your facility"),
    ("p", "The task lists are a starting point. Rewrite any line, and add your own tasks in the empty rows of the Periodic sheet. Pick Weekly, Monthly, Quarterly or Yearly in Frequency; the sheet uses 7, 30, 91 and 365 days."),
    ("p", "Cleaning products and dilution: use what your facility's policy names, and follow the product label. Avoid harsh chemicals on bare wood."),
    ("p", "Heater, stones and controls: follow the heater manufacturer's manual. Water goes on the stones only if the heater is made for it and your rules allow it."),
    ("p", "Electrical inspection and repair: a licensed electrician. Local health and fire codes for public saunas come first where they differ from this sheet."),
    ("h", "Good to know"),
    ("p", "General upkeep guidance, not a substitute for your health department's rules or the manufacturer's instructions."),
    ("p", "Free to use, share and adapt under CC BY 4.0. Made by DIVELUX, makers of handmade wool sauna hats, Irvine, California."),
    ("l", T.SITE),
    ("l", T.TOOLS),
]

EX_START = dt.date(2027, 1, 4)           # a Monday
EX_DUTY = ["Ana K.", "Ana K.", "Jon M.", "Jon M.", "Ana K.", "Rui S.", "Rui S."]
EX_INIT = ["AK", "AK", "JM", "JM", "AK", "RS", "RS"]
EX_FILLED = 5                             # example week is filled through Friday
EX_SKIP = {(3, 8), (1, 12)}               # a couple of missed cells so the counts are not all perfect (day, task)
EX_PERIODIC = {0: (dt.date(2027, 1, 4), "AK"), 1: (dt.date(2027, 1, 4), "AK"), 2: (dt.date(2027, 1, 5), "JM"), 3: (dt.date(2027, 1, 5), "JM"),
               4: (dt.date(2026, 12, 28), "RS"), 5: (dt.date(2026, 12, 28), "RS"), 6: (dt.date(2027, 1, 4), "AK"),
               7: (dt.date(2026, 12, 14), "JM"), 8: (dt.date(2026, 12, 14), "JM"), 9: (dt.date(2026, 11, 30), "RS"),
               11: (dt.date(2026, 12, 14), "JM"), 12: (dt.date(2026, 11, 2), "AK"), 14: (dt.date(2026, 3, 16), "")}
EX_TODAY = dt.date(2027, 1, 8)
EX_LOG = [
    (dt.date(2026, 12, 14), "10:30 AM", "Stones", "Removed six cracked stones, restacked", "JM", ""),
    (dt.date(2026, 12, 28), "7:15 AM", "Benches", "Tightened two loose boards on the upper bench", "RS", ""),
    (dt.date(2027, 1, 5), "2:00 PM", "Door", "Handle screw replaced", "JM", ""),
]


def daily(wb, example):
    ws = wb.active
    ws.title = "Daily"
    T.setup(ws, N_DAILY + 22, [17, 62] + [9.5] * 7)
    T.title(ws, "Sauna Cleaning Rota", "One sheet per sauna per week. Initial each task when it is done. Gray cells calculate themselves.")
    T.label(ws["A3"], "Facility", bold=True)
    ws.merge_cells("C3:D3")
    T.label(ws["C3"], "Sauna / room", bold=True, align="right")
    T.inp(ws["B3"], align="left")
    ws.merge_cells("E3:G3")
    for col in "EFG":
        T.inp(ws[f"{col}3"], align="left")
    T.label(ws["A4"], "Week starting", bold=True)
    T.inp(ws["B4"], "ddd, mmm d, yyyy", align="left")
    T.label(ws["C4"], "type the Monday, e.g. 1/4/2027", size=9, color=T.MUTED, italic=True)
    ws.merge_cells("G4:H4")
    T.label(ws["G4"], "Week complete", bold=True, align="right")
    ws.row_dimensions[3].height = 20; ws.row_dimensions[4].height = 20
    T.head_row(ws, 6, ["When", "Task"] + DAYS, height=22)
    T.calc(ws["A7"], align="left").value = ""
    T.calc(ws["B7"], align="left", color=T.INK2).value = "Date"
    T.label(ws["A8"], "", boxed=True)
    T.label(ws["B8"], "On duty (name)", boxed=True, bold=True, color=T.INK)
    for i in range(7):
        T.calc(ws.cell(7, 3 + i, f'=IF(ISNUMBER($B$4),$B$4+{i},"")'), "mmm d", color=T.INK2, size=9)
        T.inp(ws.cell(8, 3 + i), size=9)
    r = 9
    first = r
    for group, tasks in DAILY:
        for k, t in enumerate(tasks):
            T.label(ws.cell(r, 1, group if k == 0 else ""), boxed=True, bold=True, color=T.INK, size=9)
            T.label(ws.cell(r, 2, t), boxed=True, size=9.5)
            for i in range(7):
                T.inp(ws.cell(r, 3 + i), size=9)
            ws.row_dimensions[r].height = 19
            r += 1
    last = r - 1
    T.label(ws.cell(r, 1, ""), boxed=True)
    T.label(ws.cell(r, 2, "Supervisor check (initials)"), boxed=True, bold=True, color=T.INK)
    for i in range(7):
        T.inp(ws.cell(r, 3 + i), size=9)
    sup = r
    r += 1
    T.calc(ws.cell(r, 1), align="left")
    T.calc(ws.cell(r, 2, f"Done (tasks initialed, out of {N_DAILY})"), align="left", color=T.INK2)
    for i in range(7):
        col = ws.cell(r, 3 + i).column_letter
        T.calc(ws.cell(r, 3 + i, f"=COUNTA({col}{first}:{col}{last})"), "0", color=T.INK, bold=True)
    done = r
    T.calc(ws["I4"], "0%", bold=True, color=T.INK, size=12).value = f"=SUM(C{done}:I{done})/{7 * N_DAILY}"
    T.note(ws, r + 2, "Cleaning products: per your facility's policy and the product label. Heater, stones and controls: follow the heater manufacturer's manual.")
    T.note(ws, r + 3, "Electrical inspection or repair: a licensed electrician. Local health and fire codes come first. General upkeep guidance.")
    T.credit(ws, r + 4)
    T.dv(ws, "date", "B4", operator="greaterThan", formula1="36526", errorTitle="Week starting", error="Enter a date, for example 1/4/2027.",
         promptTitle="Week starting", prompt="The Monday this sheet starts on.")
    if example:
        ws["B3"] = "Example Fitness Club"; ws["E3"] = "Men's sauna"; ws["B4"] = EX_START
        for i in range(EX_FILLED):
            ws.cell(8, 3 + i, EX_DUTY[i])
            for k in range(N_DAILY):
                if (i, k) not in EX_SKIP:
                    ws.cell(first + k, 3 + i, EX_INIT[i])
            ws.cell(sup, 3 + i, "LM")
        for i in range(EX_FILLED, 7):
            ws.cell(8, 3 + i, EX_DUTY[i])
    ws.freeze_panes = "C9"
    T.page(ws, f"A1:I{r + 4}", landscape=True)
    return ws, first, last, done


def periodic(wb, example):
    ws = wb.create_sheet("Periodic")
    T.setup(ws, P_LAST + 8, [66, 12, 9, 13, 9, 13, 11, 56])
    T.title(ws, "Weekly, monthly and yearly tasks", "Type the date in Last done. Next due and Status calculate themselves.")
    T.label(ws["A3"], "Today", bold=True, align="right")
    T.calc(ws["B3"], "mmm d, yyyy", color=T.INK).value = EX_TODAY if example else "=TODAY()"
    T.label(ws["C3"], "fixed date in this example file; the template uses =TODAY()" if example else "from your computer's clock",
            size=9, color=T.MUTED, italic=True)
    T.head_row(ws, P_FIRST - 1, ["Task", "Frequency", "Every (days)", "Last done", "Done by", "Next due", "Status", "Notes"])
    for i, r in enumerate(range(P_FIRST, P_LAST + 1)):
        task, freq, memo = PERIODIC[i] if i < len(PERIODIC) else (None, None, None)
        ws.row_dimensions[r].height = 19
        T.inp(ws.cell(r, 1, task), align="left", size=9.5)
        T.inp(ws.cell(r, 2, freq), size=9.5)
        T.calc(ws.cell(r, 3, f'=IF(B{r}="Weekly",7,IF(B{r}="Monthly",30,IF(B{r}="Quarterly",91,IF(B{r}="Yearly",365,""))))'), "0")
        T.inp(ws.cell(r, 4), "mmm d, yyyy", size=9.5)
        T.inp(ws.cell(r, 5), size=9.5)
        T.calc(ws.cell(r, 6, f'=IF(AND(ISNUMBER(D{r}),ISNUMBER(C{r})),D{r}+C{r},"")'), "mmm d, yyyy")
        T.calc(ws.cell(r, 7, f'=IF(B{r}="","",IF(NOT(ISNUMBER(D{r})),"Not logged",IF(F{r}<$B$3,"Due","OK")))'), color=T.INK2)
        T.inp(ws.cell(r, 8, memo or None), align="left", size=9)
        if example and i in EX_PERIODIC:
            d, who = EX_PERIODIC[i]
            ws.cell(r, 4, d)
            if who:
                ws.cell(r, 5, who)
            else:
                ws.cell(r, 5, "ext.")
    T.note(ws, P_LAST + 2, "Stones, heater and controls: follow the heater manufacturer's manual. Electrical work: a licensed electrician. Cleaning products: per your facility's policy and the product label.")
    T.credit(ws, P_LAST + 4)
    rng = lambda col: f"{col}{P_FIRST}:{col}{P_LAST}"
    T.dv(ws, "list", rng("B"), formula1='"Weekly,Monthly,Quarterly,Yearly"', errorTitle="Frequency", error="Pick Weekly, Monthly, Quarterly or Yearly.",
         promptTitle="Frequency", prompt="Pick from the list.")
    T.dv(ws, "date", rng("D"), operator="greaterThan", formula1="36526", errorTitle="Last done", error="Enter a date, for example 1/4/2027.",
         promptTitle="Last done", prompt="The date the task was last finished.")
    ws.conditional_formatting.add(rng("G"), CellIsRule(operator="equal", formula=['"Due"'], font=T.font(10, True, T.EMBER)))
    ws.freeze_panes = f"B{P_FIRST}"
    T.page(ws, f"A1:H{P_LAST + 4}", landscape=True)
    return ws


def log(wb, example):
    ws = wb.create_sheet("Log")
    T.setup(ws, LOG_ROWS + 10, [13, 11, 20, 52, 10, 24, 30])
    T.title(ws, "Maintenance log", "One line for anything worth a record. Sign the printed copy if your facility needs a signature.")
    T.head_row(ws, 4, ["Date", "Time", "Area", "What was done", "Done by", "Checked by (signature)", "Notes"])
    for r in range(5, 5 + LOG_ROWS):
        ws.row_dimensions[r].height = 20
        T.inp(ws.cell(r, 1), "mmm d, yyyy", size=9.5)
        T.inp(ws.cell(r, 2), size=9.5)
        for c in (3, 4, 7):
            T.inp(ws.cell(r, c), align="left", size=9.5)
        T.inp(ws.cell(r, 5), size=9.5); T.inp(ws.cell(r, 6), size=9.5)
    if example:
        for i, row in enumerate(EX_LOG):
            for c, v in enumerate(row, start=1):
                if v != "":
                    ws.cell(5 + i, c if c < 6 else c + 1, v)
    end = 5 + LOG_ROWS
    T.dv(ws, "date", f"A5:A{end - 1}", operator="greaterThan", formula1="36526", errorTitle="Date", error="Enter a date, for example 1/4/2027.")
    T.dv(ws, "list", f"C5:C{end - 1}", formula1='"Benches,Floor and drain,Door,Heater,Stones,Controls,Vents,Lighting,Signs,Other"',
         errorTitle="Area", error="Pick an area from the list, or pick Other.", promptTitle="Area", prompt="Pick from the list.")
    T.credit(ws, end + 1)
    ws.freeze_panes = "A5"
    T.page(ws, f"A1:G{end + 1}", landscape=True)
    return ws


def build(path, example=False):
    wb = Workbook()
    daily(wb, example)
    periodic(wb, example)
    log(wb, example)
    T.howto(wb, HOWTO)
    T.props(wb, "Sauna Cleaning Rota for Gyms and Spas", "Weekly cleaning rota, periodic tasks and maintenance log for a commercial sauna.")
    wb.save(path)


def main():
    d = os.path.join(T.ROOT, SLUG)
    os.makedirs(d, exist_ok=True)
    build(os.path.join(d, SLUG + ".xlsx"))
    build(os.path.join(d, SLUG + "-example.xlsx"), example=True)
    with open(os.path.join(d, SLUG + "-tasks.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Task", "Frequency", "When", "Every (days)", "Notes"])
        for group, tasks in DAILY:
            for t in tasks:
                w.writerow([t, "Daily", group, 1, ""])
        for t, freq, memo in PERIODIC:
            w.writerow([t, freq, "", EVERY[freq], memo])
    return [os.path.join(d, SLUG + ".xlsx"), os.path.join(d, SLUG + "-example.xlsx")]


if __name__ == "__main__":
    print(main())
