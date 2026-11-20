"""13. Home Sauna Build Budget: line items by category, planned / actual / difference, summary and a chart."""
import csv
import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment

import tcommon as T

SLUG = "home-sauna-build-budget"
FIRST, LAST = 7, 76          # line rows on the Budget sheet
S_FIRST = 6                  # first category row on the Summary sheet
MONEY = '$#,##0;-$#,##0'

CATS = [
    ("Planning & permits", ["Design or drawings", "Building permit", "Electrical permit", "Site prep and leveling"]),
    ("Structure & framing", ["Foundation or base (pad, piers or deck)", "Framing lumber", "Exterior sheathing and cladding",
                             "Roofing (outdoor sauna)", "Subfloor and flooring", "Floor drain and waterproofing (if used)"]),
    ("Insulation & vapor barrier", ["Wall and ceiling insulation", "Foil vapor barrier", "Foil tape and fasteners"]),
    ("Interior wood", ["Wall paneling", "Ceiling paneling", "Trim and moldings", "Wood treatment made for sauna interiors (optional)"]),
    ("Benches", ["Bench boards", "Bench frames and supports", "Backrests and headrests", "Heater guard rail"]),
    ("Door & glass", ["Sauna door", "Window or glass panel", "Hinges, handle and door seal"]),
    ("Heater & stones", ["Sauna heater or stove", "Sauna stones", "Chimney and flue kit (wood stove)",
                         "Heat shields, floor protection (per the heater manual)"]),
    ("Controls", ["Control panel", "Temperature sensor", "Timer or remote control (optional)"]),
    ("Electrical (licensed electrician)", ["Licensed electrician: labor", "Breaker and disconnect", "Wire and conduit",
                                           "Panel upgrade (if needed)"]),
    ("Ventilation", ["Intake vent", "Exhaust vent", "Duct or fan (if used)"]),
    ("Lighting", ["Sauna-rated light fixtures", "Switch or dimmer"]),
    ("Accessories", ["Bucket and ladle", "Thermometer and hygrometer", "Sand timer", "Hooks and towel rack",
                     "Seat towels and sauna hats", "Smoke and carbon monoxide alarms near the sauna"]),
    ("Labor, delivery & other", ["Carpenter or contractor labor", "Delivery and freight", "Tool rental", "Waste disposal"]),
]
CAT_NAMES = [c for c, _ in CATS]
LINES = [(c, item) for c, items in CATS for item in items]

# Example file only. Round sample numbers for a small indoor sauna; they are not prices or a quote.
EXAMPLE = {
    "Design or drawings": (150, 150, "Yes", ""),
    "Building permit": (200, 185, "Yes", ""),
    "Electrical permit": (120, 120, "Yes", ""),
    "Framing lumber": (450, 510, "Yes", "Two extra studs"),
    "Subfloor and flooring": (300, 280, "Yes", ""),
    "Wall and ceiling insulation": (260, 245, "Yes", ""),
    "Foil vapor barrier": (110, 110, "Yes", ""),
    "Foil tape and fasteners": (40, 55, "Yes", ""),
    "Wall paneling": (900, 980, "Yes", ""),
    "Ceiling paneling": (300, 310, "Yes", ""),
    "Trim and moldings": (120, None, "", ""),
    "Bench boards": (420, 465, "Yes", ""),
    "Bench frames and supports": (140, 120, "Yes", ""),
    "Backrests and headrests": (90, None, "", ""),
    "Heater guard rail": (60, 60, "Yes", ""),
    "Sauna door": (650, 650, "No", "Deposit paid, balance on delivery"),
    "Hinges, handle and door seal": (0, 0, "", "Came with the door"),
    "Sauna heater or stove": (1200, 1150, "Yes", ""),
    "Sauna stones": (80, 80, "Yes", ""),
    "Control panel": (350, 350, "Yes", ""),
    "Temperature sensor": (0, 0, "", "Came with the control panel"),
    "Licensed electrician: labor": (900, 1050, "No", "Invoice due"),
    "Breaker and disconnect": (150, 160, "Yes", ""),
    "Wire and conduit": (220, 240, "Yes", ""),
    "Intake vent": (30, 30, "Yes", ""),
    "Exhaust vent": (45, 45, "Yes", ""),
    "Sauna-rated light fixtures": (120, 95, "Yes", ""),
    "Switch or dimmer": (35, None, "", ""),
    "Bucket and ladle": (60, 60, "Yes", ""),
    "Thermometer and hygrometer": (35, 30, "Yes", ""),
    "Sand timer": (20, None, "", ""),
    "Hooks and towel rack": (40, None, "", ""),
    "Seat towels and sauna hats": (90, None, "", ""),
    "Smoke and carbon monoxide alarms near the sauna": (50, 50, "Yes", ""),
    "Delivery and freight": (180, 210, "Yes", ""),
    "Waste disposal": (60, None, "", ""),
}

HOWTO = [
    ("h", "How to use this budget"),
    ("p", "1. Open the Budget sheet. Each line is one cost. The list covers the usual parts of a home sauna build; change the wording, clear lines you do not need, and add your own in the empty rows at the bottom. Pick the category from the drop-down so the line lands in the right total."),
    ("p", "2. Type what you expect to pay in Planned. Get real quotes: prices depend on your region, the size of the room and the materials you choose. This file contains no price guidance."),
    ("p", "3. When you buy or get an invoice, type the amount in Actual. Difference shows how far the line is over (+) or under (-) the plan. Set Paid? to Yes once the money has left your account."),
    ("p", "4. Open the Summary sheet for totals by category, the contingency cushion, what is paid and what is still owed, and a planned-against-actual chart."),
    ("p", "5. Contingency: on the Summary sheet, set the share of the planned total you want to hold back for surprises. The 10% in the file is a placeholder. Set the figure that fits your project."),
    ("h", "What the gray cells do"),
    ("p", "Budget: Difference = Actual - Planned, shown only when Actual has a number. The Total row adds each column."),
    ("p", "Summary: Planned and Actual add up the Budget lines of each category (SUMIF). Budget with contingency = planned total + planned total x contingency rate. Left in budget = budget with contingency - actual so far. Still to pay = actual so far - lines marked Paid. Contingency left = contingency amount - net overrun on lines that already have an actual cost."),
    ("h", "Good to know"),
    ("p", "Electrical work: plan on a licensed electrician and the permit your city requires. A sauna heater needs its own correctly sized circuit; the heater manual and your electrician decide the breaker and wire size."),
    ("p", "Heater size: follow the manufacturer's manual. For a first estimate, try the free calculator at the address below."),
    ("l", "https://divelux.github.io/sauna-heater-calculator/"),
    ("p", "Other currencies: select the money columns and change the number format. To use more lines, insert rows inside the table, not below the last row, so the totals keep covering them."),
    ("p", "Free to use, share and adapt under CC BY 4.0. Made by DIVELUX, makers of handmade wool sauna hats, Irvine, California."),
    ("l", T.SITE),
    ("l", T.TOOLS),
]


def budget_sheet(wb, example):
    ws = wb.active
    ws.title = "Budget"
    T.setup(ws, LAST + 6, [31, 52, 13, 13, 13, 9, 40])
    T.title(ws, "Home Sauna Build Budget",
            "One line per cost. Type in the white cells. Gray cells calculate themselves.")
    T.label(ws["A3"], "Project", bold=True)
    T.inp(ws["B3"], align="left")
    if example:
        ws["B3"] = "Example: small indoor sauna"
        T.label(ws["C3"], "Example numbers, not a quote. Your prices will differ.", bold=True, color=T.INK)
    else:
        T.label(ws["C3"], "name or address, optional", size=9, color=T.MUTED, italic=True)
    ws.row_dimensions[4].height = 6
    T.head_row(ws, 5, ["Category", "Item", "Planned", "Actual", "Difference", "Paid?", "Vendor / notes"])
    # Totals sit right under the header so they stay in view
    T.calc(ws["A6"], align="left", bold=True, color=T.INK).value = "Total"
    T.calc(ws["B6"], align="left", color=T.MUTED).value = "all lines"
    for col in "CD":
        T.calc(ws[f"{col}6"], MONEY, bold=True, color=T.INK).value = f"=SUM({col}{FIRST}:{col}{LAST})"
    T.calc(ws["E6"], MONEY, bold=True, color=T.INK).value = f"=SUM(E{FIRST}:E{LAST})"
    T.calc(ws["F6"]); T.calc(ws["G6"], align="left").value = "Difference: lines with an actual cost"
    ws.row_dimensions[6].height = 21
    for i, r in enumerate(range(FIRST, LAST + 1)):
        ws.row_dimensions[r].height = 18
        cat, item = LINES[i] if i < len(LINES) else (None, None)
        T.inp(ws.cell(r, 1, cat), align="left")
        T.inp(ws.cell(r, 2, item), align="left")
        T.inp(ws.cell(r, 3), MONEY)
        T.inp(ws.cell(r, 4), MONEY)
        T.calc(ws.cell(r, 5, f'=IF(ISNUMBER(D{r}),D{r}-IF(ISNUMBER(C{r}),C{r},0),"")'), MONEY)
        T.inp(ws.cell(r, 6))
        T.inp(ws.cell(r, 7), align="left")
        if example and item in EXAMPLE:
            p, a, paid, memo = EXAMPLE[item]
            ws.cell(r, 3, p)
            if a is not None:
                ws.cell(r, 4, a)
            if paid:
                ws.cell(r, 6, paid)
            if memo:
                ws.cell(r, 7, memo)
    T.note(ws, LAST + 2, "Electrical work: use a licensed electrician and the permit your city requires. Heater, clearances and wiring: follow the manufacturer's manual.")
    T.note(ws, LAST + 3, "A planning worksheet, not a quote. Get real prices from your suppliers and contractors.")
    T.credit(ws, LAST + 4)
    rng = lambda col: f"{col}{FIRST}:{col}{LAST}"
    T.dv(ws, "list", rng("A"), formula1=f"=Summary!$A${S_FIRST}:$A${S_FIRST + len(CATS) - 1}", errorTitle="Category",
         error="Pick a category from the list so the line is counted on the Summary sheet.", promptTitle="Category", prompt="Pick from the list.")
    for col, name in (("C", "Planned"), ("D", "Actual")):
        T.dv(ws, "decimal", rng(col), operator="greaterThanOrEqual", formula1="0", errorTitle=name,
             error="Enter an amount, 0 or more. No currency sign.", promptTitle=name,
             prompt="What you expect to pay." if col == "C" else "What it really cost. Leave empty until you know.")
    T.dv(ws, "list", rng("F"), formula1='"Yes,No"', errorTitle="Paid?", error="Pick Yes or No.", promptTitle="Paid?", prompt="Yes once it is paid in full.")
    ws.conditional_formatting.add(rng("E"), CellIsRule(operator="greaterThan", formula=["0"], font=T.font(10, True, T.EMBER)))
    ws.freeze_panes = "A7"
    T.page(ws, f"A1:G{LAST + 4}", fit_height=0)
    ws.print_title_rows = "5:5"
    return ws


def summary_sheet(wb):
    ws = wb.create_sheet("Summary")
    n = len(CATS)
    tot = S_FIRST + n          # total row
    T.setup(ws, tot + 36, [36, 14, 14, 14, 11, 3, 30])
    T.title(ws, "Summary", "Everything here is calculated from the Budget sheet. The only cell to type in is the contingency rate.")
    T.head_row(ws, S_FIRST - 1, ["Category", "Planned", "Actual", "Over / under", "Spent"])
    A = f"Budget!$A${FIRST}:$A${LAST}"
    for i, cat in enumerate(CAT_NAMES):
        r = S_FIRST + i
        ws.row_dimensions[r].height = 19
        T.label(ws.cell(r, 1, cat), boxed=True, color=T.INK)
        T.calc(ws.cell(r, 2, f"=SUMIF({A},A{r},Budget!$C${FIRST}:$C${LAST})"), MONEY, color=T.INK2)
        T.calc(ws.cell(r, 3, f"=SUMIF({A},A{r},Budget!$D${FIRST}:$D${LAST})"), MONEY, color=T.INK2)
        T.calc(ws.cell(r, 4, f"=SUMIF({A},A{r},Budget!$E${FIRST}:$E${LAST})"), MONEY, color=T.INK2)
        T.calc(ws.cell(r, 5, f'=IF(B{r}>0,C{r}/B{r},"")'), "0%", color=T.INK2)
    T.calc(ws.cell(tot, 1, "Total"), align="left", bold=True, color=T.INK)
    for col in "BCD":
        T.calc(ws[f"{col}{tot}"], MONEY, bold=True, color=T.INK).value = f"=SUM({col}{S_FIRST}:{col}{tot - 1})"
    T.calc(ws[f"E{tot}"], "0%", bold=True, color=T.INK).value = f'=IF(B{tot}>0,C{tot}/B{tot},"")'
    ws.row_dimensions[tot].height = 21
    T.note(ws, tot + 1, "Over / under adds the Difference column: only lines that already have an actual cost.")
    r0 = tot + 3
    rows = [
        ("Contingency rate", None, "0%", "Type your own. 10% is a placeholder."),
        ("Contingency amount", f"=B{tot}*B{r0}", MONEY, "planned total x rate"),
        ("Budget with contingency", f"=B{tot}+B{r0 + 1}", MONEY, ""),
        ("Spent so far (actual)", f"=C{tot}", MONEY, ""),
        ("Left in budget", f"=B{r0 + 2}-C{tot}", MONEY, "budget with contingency - actual"),
        ("Paid so far", f'=SUMIF(Budget!$F${FIRST}:$F${LAST},"Yes",Budget!$D${FIRST}:$D${LAST})', MONEY, "lines marked Paid? = Yes"),
        ("Still to pay", f"=C{tot}-B{r0 + 5}", MONEY, "actual - paid"),
        ("Contingency left", f"=B{r0 + 1}-MAX(0,D{tot})", MONEY, "contingency - net overrun so far"),
    ]
    for i, (lab, formula, fmt, hint) in enumerate(rows):
        r = r0 + i
        ws.row_dimensions[r].height = 22
        T.label(ws.cell(r, 1, lab), size=11, boxed=True)
        c = ws.cell(r, 2, formula if formula else 0.1)
        if formula:
            T.calc(c, fmt, align="right", size=12, bold=True, color=T.INK)
        else:
            T.inp(c, fmt, align="right", size=12, bold=True)
        if hint:
            T.label(ws.cell(r, 3, hint), size=9, color=T.MUTED, italic=True)
    T.dv(ws, "decimal", f"B{r0}", operator="between", formula1="0", formula2="1", errorTitle="Contingency rate",
         error="Enter a share between 0% and 100%, for example 10%.", promptTitle="Contingency rate",
         prompt="Share of the planned total to hold back for surprises.")
    ws.conditional_formatting.add(f"D{S_FIRST}:D{tot}", CellIsRule(operator="greaterThan", formula=["0"], font=T.font(10, True, T.EMBER)))
    chart_row = r0 + len(rows) + 1
    bar = BarChart()
    bar.type = "bar"; bar.grouping = "clustered"; bar.style = 10
    bar.title = "Planned and actual by category"
    bar.add_data(Reference(ws, min_col=2, max_col=3, min_row=S_FIRST - 1, max_row=tot - 1), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=S_FIRST, max_row=tot - 1))
    bar.height = 13.5; bar.width = 17.5
    bar.x_axis.scaling.orientation = "maxMin"     # first category on top
    bar.y_axis.crosses = "max"                    # keep the money axis at the bottom
    bar.x_axis.delete = False; bar.y_axis.delete = False
    bar.y_axis.number_format = '$#,##0'
    bar.legend.position = "b"
    bar.gapWidth = 60
    for s, color in zip(bar.series, (T.TAN, T.WOOD)):
        s.graphicalProperties.solidFill = color
        s.graphicalProperties.line.solidFill = color
    ws.add_chart(bar, f"A{chart_row}")
    end = chart_row + 28
    T.credit(ws, end)
    T.page(ws, f"A1:E{end}", margin=0.5)
    return ws, r0


def build(path, example=False):
    wb = Workbook()
    budget_sheet(wb, example)
    summary_sheet(wb)
    T.howto(wb, HOWTO)
    T.props(wb, "Home Sauna Build Budget", "Budget worksheet for building a home sauna.")
    wb.save(path)


def main():
    d = os.path.join(T.ROOT, SLUG)
    os.makedirs(d, exist_ok=True)
    build(os.path.join(d, SLUG + ".xlsx"))
    build(os.path.join(d, SLUG + "-example.xlsx"), example=True)
    with open(os.path.join(d, SLUG + ".csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Category", "Item", "Planned", "Actual", "Paid", "Vendor / notes"])
        for cat, item in LINES:
            w.writerow([cat, item, "", "", "", ""])
    return [os.path.join(d, SLUG + ".xlsx"), os.path.join(d, SLUG + "-example.xlsx")]


if __name__ == "__main__":
    print(main())
