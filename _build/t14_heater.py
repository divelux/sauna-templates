"""14. Sauna Heater Sizing Sheet: the rules of the DIVELUX Sauna Heater Size Calculator as spreadsheet formulas.
Every factor comes from heater makers' published guidance (see the Sources sheet and
../../tools/sauna-heater-calculator/README.md). Nothing here is measured or invented by us."""
import csv
import os

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment

import tcommon as T

SLUG = "sauna-heater-sizing-sheet"
CALC_URL = "https://divelux.github.io/sauna-heater-calculator/"
M_PER_FT, CUFT_PER_M3, SQFT_PER_M2 = 0.3048, 35.3147, 10.7639
WARN = ("Always confirm with the heater manufacturer and a licensed electrician. This is a rule-of-thumb estimate: "
        "it cannot see your insulation, vents, climate or wiring. Follow the manufacturer's manual: the manual of the heater "
        "you buy has the final say on room volume, clearances, breaker and wire size.")

SOURCES = [
    ("Harvia support: How do I select the correct heater power?",
     "https://support.harvia.com/hc/en-gb/articles/22158995674524-How-do-I-select-the-correct-heater-power",
     "1 kW per m³; 1.2 m³ for each m² of stone, glass or similar non-insulated surface; factor 1.5 for non-insulated log walls; the example of a calculated volume of about 8.5 m³ with a minimum output of 6 kW; choose a heater with your volume near the middle of its min-max range."),
    ("Harvia support: Choosing a wood burning heater",
     "https://support.harvia.com/hc/en-gb/articles/27407591688476-Choosing-a-wood-burning-heater",
     "The same calculation for wood stoves, with the 11.5 m³ + 2.27 m³ example."),
    ("Harvia L30 electric heater manual, \"Heater output\" (copy on ManualsLib)",
     "https://www.manualslib.com/manual/2834310/Harvia-L30.html?page=6",
     "\"Add 1,2 m³ to the volume of the sauna for each non-insulated wall square meter.\" \"If the sauna room has log walls, multiply the sauna's volume by 1,5.\""),
    ("HUUM: How to dimension a sauna heater: find the proper power for your sauna",
     "https://huum.eu/how-to-dimension-a-sauna-heater-find-the-proper-power-for-your-sauna/",
     "1 kW per calculated m³; coefficient 1 for glass, log wall or other non-insulated surface; the 2 x 1.8 x 2.2 m example."),
    ("HUUM DROP user manual, EU, v6 2025 (PDF)",
     "https://huum.eu/wp-content/uploads/2022/05/H1001L02_v6_DROP_User_Manual_EU_2025_PRINT.pdf",
     "\"An additional volume of 1 m³ should be added to the sauna room for each such square meter of the wall\"; a room volume range for each model."),
    ("Sizing Your HUUM (PDF, North American sizing sheet hosted by a retailer)",
     "https://cdn.shopify.com/s/files/1/0534/1243/0022/files/Sizing-Your-HUUM-2023.pdf",
     "Cold surface square feet x 4.92 (this is 1.5 m³ per m²)."),
    ("The Sauna Place: How many kilowatts do you need for a sauna heater?",
     "https://www.saunaplace.com/blogs/blogs/how-many-kilowatts-do-you-need-for-a-sauna-heater-a-simple-sizing-guide",
     "A retailer's note on the \"1 kW per 50 cubic feet\" shortcut."),
    ("Harvia Sauna Calculator (the maker's own)", "https://www.harvia.com/en/sauna/saunas/sauna-calculator/", ""),
    ("HUUM heater calculator (the maker's own)", "https://huum.eu/calculator/", ""),
]

# Worked examples, all in meters: name, source, L, W, H, glass m², stone m², log, heater, what the source says
EXAMPLES = [
    ("Calculator default", "6 x 5 x 7 ft room, 12 sq ft glass door", 6 * M_PER_FT, 5 * M_PER_FT, 7 * M_PER_FT, 12 / SQFT_PER_M2, 0, "No", "Electric",
     "DIVELUX online calculator: 210 cu ft, 7.3 m³ (257 cu ft), 5.1 to 7.3 kW"),
    ("Harvia L30 manual", "10 m³ room with a glass door of about 0.8 x 2.0 m", 2.5, 2, 2, 1.6, 0, "No", "Electric",
     "\"about a 12 m³ sauna room\""),
    ("Harvia wood stove guide", "2.0 x 2.5 x 2.3 m, glass door 0.9 x 2.1 m", 2.0, 2.5, 2.3, 1.89, 0, "No", "Wood-burning",
     "11.5 + 2.27 = 13.77 m³"),
    ("HUUM sizing article", "2 x 1.8 x 2.2 m, glass wall 1.8 x 2.2 m", 2, 1.8, 2.2, 3.96, 0, "No", "Electric",
     "11.88 m³ by the HUUM rule"),
    ("Harvia support", "calculated volume of about 8.5 m³, nothing uninsulated", 2.5, 2, 1.7, 0, 0, "No", "Electric",
     "\"a minimum output of 6 kW\""),
    ("Log room (illustration)", "2 x 2 x 2 m bare log room, 1 m² of glass", 2, 2, 2, 1, 0, "Yes", "Electric",
     "Harvia rule: 8 x 1.5 + 1.2 = 13.2 m³; no HUUM figure for a log room"),
]

EXAMPLES = [(n, room, round(L, 4), round(W, 4), round(H, 4), round(g, 4), s, log, heater, says) for n, room, L, W, H, g, s, log, heater, says in EXAMPLES]

HOWTO = [
    ("h", "How to use this sheet"),
    ("p", "1. On the Calculator sheet choose the units: ft (feet and inches) or m (meters)."),
    ("p", "2. Type the inside size of the hot room: length, width and ceiling height. In ft mode you can split a size into feet and inches, for example 6 and 6 for 6 ft 6 in."),
    ("p", "3. Add the area of glass (door, windows) and of stone, tile, brick or concrete that has no insulation behind it, in sq ft or m² to match the units."),
    ("p", "4. Say whether the inside walls are bare log, and pick Electric or Wood-burning."),
    ("p", "5. Read the result: room volume, calculated volume and, for an electric heater, a power range in kW. For a wood-burning stove the sheet gives the calculated volume to shop by, because wood stoves are rated by room volume."),
    ("h", "How the size is worked out"),
    ("p", "Room volume = length x width x ceiling height, measured inside the hot room."),
    ("p", "Cold surfaces: glass, stone, tile, brick and concrete with no insulation behind them soak up heat. Harvia counts each square meter as 1.2 m³ of extra room volume. HUUM counts 1 m³. A North American HUUM sizing sheet counts 4.92 cu ft per sq ft, which is 1.5 m³ per m². The result uses Harvia's 1.2; the sheet shows all three."),
    ("p", "Log walls: if the inside walls are bare log, Harvia multiplies the room volume by 1.5."),
    ("p", "Calculated volume = room volume x (1.5 if log) + 1.2 x uninsulated area."),
    ("p", "Top of the power range: 1 kW per m³ of calculated volume (Harvia and HUUM). Bottom of the range: 1 kW per 50 cu ft (1.416 m³), the shortcut many North American retailers quote; it matches Harvia's own example of about 8.5 m³ at a minimum output of 6 kW."),
    ("p", "The two ends are not the same rule in different units: one cubic meter is 35.3 cu ft, so the metric rule asks for roughly 40% more power than the 50 cu ft shortcut. Manufacturers' model tables sit between the two. Check the room volume range printed for the exact model, and pick a heater with your volume near the middle of its range."),
    ("h", "What it does not know"),
    ("p", "Insulation quality, vents, outdoor temperature, stone mass, altitude, and your home's wiring. HUUM counts log walls by area instead of with a multiplier, so the sheet does not guess a HUUM figure for a log room. Infrared cabins are sized differently and are not covered."),
    ("p", WARN),
    ("h", "More"),
    ("p", "The same rules as a web page, with a link you can share:"),
    ("l", CALC_URL),
    ("p", "Free to use, share and adapt under CC BY 4.0. Made by DIVELUX, makers of handmade wool sauna hats, Irvine, California."),
    ("l", T.SITE),
    ("l", T.TOOLS),
]


def calculator(wb):
    ws = wb.active
    ws.title = "Calculator"
    T.setup(ws, 46, [62, 15, 15, 14, 15, 3])
    T.title(ws, "Sauna Heater Sizing Sheet", "Type in the white cells. Gray cells calculate themselves. The file opens with a sample room: replace it with yours.")
    T.section(ws, 4, "1. Your room")
    T.label(ws["A5"], "Units", boxed=True)
    T.inp(ws["B5"], bold=True).value = "ft"
    T.label(ws["C5"], "ft = feet and inches, m = meters", size=9, color=T.MUTED, italic=True)
    T.head_row(ws, 6, ["Inside the hot room", None, None, None, "In meters / m²"], height=22)
    ws["B6"] = '=IF($B$5="m","meters","feet")'
    ws["C6"] = '=IF($B$5="m","","inches")'
    ws["D6"] = "unit"
    dims = [("Length", 6), ("Width", 5), ("Ceiling height", 7)]
    for i, (name, default) in enumerate(dims):
        r = 7 + i
        T.label(ws.cell(r, 1, name), boxed=True)
        T.inp(ws.cell(r, 2, default), "0.###")
        T.inp(ws.cell(r, 3), "0.###")
        T.calc(ws.cell(r, 4, '=IF($B$5="m","m","ft + in")'))
        T.calc(ws.cell(r, 5, f'=IF(ISNUMBER(B{r}),IF($B$5="m",B{r},B{r}*{M_PER_FT}+IF(ISNUMBER(C{r}),C{r},0)*{M_PER_FT}/12),0)'), "0.000")
    areas = [("Glass with no insulation behind it (door, windows)", 12), ("Stone, tile, brick or concrete with no insulation behind it", 0)]
    for i, (name, default) in enumerate(areas):
        r = 10 + i
        T.label(ws.cell(r, 1, name), boxed=True)
        T.inp(ws.cell(r, 2, default), "0.###")
        T.calc(ws.cell(r, 3))
        T.calc(ws.cell(r, 4, '=IF($B$5="m","m²","sq ft")'))
        T.calc(ws.cell(r, 5, f'=IF(ISNUMBER(B{r}),IF($B$5="m",B{r},B{r}/{SQFT_PER_M2}),0)'), "0.000")
    T.label(ws["A12"], "Bare log walls inside?", boxed=True)
    T.inp(ws["B12"]).value = "No"
    T.label(ws["A13"], "Heater type", boxed=True)
    T.inp(ws["B13"]).value = "Electric"
    ws.merge_cells("B13:C13")
    T.inp(ws["C13"])
    T.label(ws["A14"], "Input check", boxed=True)
    ws.merge_cells("B14:E14")
    for col in "BCDE":
        T.calc(ws[f"{col}14"], align="left", color=T.INK)
    ws["B14"] = ('=IF(OR(NOT(ISNUMBER(B7)),NOT(ISNUMBER(B8)),NOT(ISNUMBER(B9))),"Enter the length, width and ceiling height.",'
                 'IF(OR(E7<0.9,E7>6,E8<0.9,E8>6),"Check the length and width: this sheet covers rooms from 3 ft to 19 ft 8 in (0.9 to 6 m) a side.",'
                 'IF(OR(E9<1.7,E9>3),"Check the height: this sheet covers ceilings from 5 ft 7 in to 9 ft 10 in (1.7 to 3 m).",'
                 'IF(OR(E10<0,E11<0,E10>40,E11>40),"Check the glass and stone areas.",'
                 'IF(E10+E11>2*(E7*E8+E7*E9+E8*E9),"Glass plus stone is more than the whole surface of this room. Check the areas.","OK")))))')
    ws["F14"] = '=B14="OK"'          # TRUE when the inputs can be used
    ws["F14"].font = T.font(8, color=T.PAPER)
    ws.row_dimensions[14].height = 30
    ws["B14"].alignment = Alignment(wrap_text=True, vertical="center")

    T.section(ws, 16, "2. Result")
    T.head_row(ws, 17, ["", "Metric", "US", "", ""], height=22)
    ok = "$F$14"
    res = [
        (18, "Room volume", f'=IF({ok},E7*E8*E9,"")', "0.0", f'=IF({ok},B18*{CUFT_PER_M3},"")', "0", "m³", "cu ft"),
        (19, "Uninsulated glass and stone", f'=IF({ok},E10+E11,"")', "0.00", f'=IF({ok},B19*{SQFT_PER_M2},"")', "0.0", "m²", "sq ft"),
        (20, "Log wall factor (Harvia: 1.5 for bare log walls)", '=IF(B12="Yes",1.5,1)', "0.0", None, None, "x", ""),
        (21, "Extra volume for cold surfaces (Harvia: 1.2 m³ per m²)", f'=IF({ok},B19*1.2,"")', "0.0", f'=IF({ok},B21*{CUFT_PER_M3},"")', "0", "m³", "cu ft"),
        (22, "Calculated volume", f'=IF({ok},B18*B20+B21,"")', "0.0", f'=IF({ok},B22*{CUFT_PER_M3},"")', "0", "m³", "cu ft"),
    ]
    for r, name, f1, fmt1, f2, fmt2, u1, u2 in res:
        big = r == 22
        T.label(ws.cell(r, 1, name), boxed=True, bold=big, color=T.INK if big else T.INK2)
        T.calc(ws.cell(r, 2, f1), fmt1, bold=big, color=T.INK, size=12 if big else 10)
        T.calc(ws.cell(r, 3, f2), fmt2, bold=big, color=T.INK, size=12 if big else 10)
        T.label(ws.cell(r, 4, f"{u1} | {u2}" if u2 else u1), size=9, color=T.MUTED)
        ws.row_dimensions[r].height = 24 if big else 20
    T.label(ws["A23"], "Electric heater power: low end (1 kW per 50 cu ft)", boxed=True)
    T.calc(ws["B23"], "0.0", bold=True, color=T.INK, size=12).value = f'=IF({ok},IF($B$13="Electric",C22/50,"n/a"),"")'
    T.label(ws["A24"], "Electric heater power: high end (1 kW per m³)", boxed=True)
    T.calc(ws["B24"], "0.0", bold=True, color=T.INK, size=12).value = f'=IF({ok},IF($B$13="Electric",B22*1,"n/a"),"")'
    for r in (23, 24):
        T.label(ws.cell(r, 3, "kW"), size=9, color=T.MUTED)
        ws.row_dimensions[r].height = 24
    T.label(ws["A25"], "What to shop for", boxed=True, bold=True, color=T.INK)
    ws.merge_cells("B25:E25")
    for col in "BCDE":
        T.calc(ws[f"{col}25"], align="left", color=T.INK, bold=True)
    ws["B25"] = (f'=IF({ok},IF($B$13="Electric","An electric heater of about "&ROUND(B23,1)&" to "&ROUND(B24,1)&" kW. '
                 'Check the room volume range printed for the exact model.",'
                 '"A wood-burning stove rated for a room of about "&ROUND(B22,1)&" m³ ("&ROUND(C22,0)&" cu ft). '
                 'Wood stoves are sold by room volume, not by kW."),"")')
    ws["B25"].alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[25].height = 34

    T.section(ws, 27, "3. The same room under three published rules")
    T.head_row(ws, 28, ["Rule", "m³", "cu ft", "", ""], height=22)
    rules = [
        (29, "Harvia: 1.2 m³ per m², log walls x 1.5 (used above)", f'=IF({ok},B22,"")'),
        (30, "HUUM: 1 m³ per m²", f'=IF({ok},IF($B$12="Yes","n/a",B18+B19*1),"")'),
        (31, "HUUM North American sheet: 4.92 cu ft/sq ft (1.5 m³ per m²)", f'=IF({ok},IF($B$12="Yes","n/a",B18+B19*1.5),"")'),
    ]
    for r, name, f in rules:
        T.label(ws.cell(r, 1, name), boxed=True)
        T.calc(ws.cell(r, 2, f), "0.0", color=T.INK)
        T.calc(ws.cell(r, 3, f'=IF(ISNUMBER(B{r}),B{r}*{CUFT_PER_M3},B{r})'), "0", color=T.INK)
        ws.row_dimensions[r].height = 20
    T.note(ws, 32, "HUUM counts log walls by area, not with a multiplier, so this sheet does not guess a HUUM figure for a log room (n/a).")
    ws.merge_cells("A34:E34")
    ws["A34"] = (f'=IF({ok},IF(AND(B19>0,B21/B22>=0.3),"Note: glass and stone make up "&ROUND(B21/B22*100,0)&"% of the calculated volume. '
                 'With this much uninsulated surface, ask the manufacturer before you buy.",""),"")')
    ws["A34"].font = T.font(10, True, T.EMBER)
    ws["A34"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[34].height = 28
    T.note(ws, 36, WARN, color=T.INK2, size=10, wrap_to=5, height=58)
    T.note(ws, 37, "Infrared cabins are sized differently and are not covered. Sources for every factor: see the Sources sheet.")
    c = ws["A38"]
    c.value = "Online version with a shareable link: " + CALC_URL
    c.hyperlink = CALC_URL
    c.font = T.font(9, color=T.INK2, underline="single")
    T.credit(ws, 40)

    T.dv(ws, "list", "B5", formula1='"ft,m"', errorTitle="Units", error="Pick ft or m.", promptTitle="Units", prompt="ft = feet and inches, m = meters.")
    T.dv(ws, "decimal", "B7:B9", operator="greaterThan", formula1="0", errorTitle="Size", error="Enter a number greater than 0.",
         promptTitle="Size", prompt="Measured inside the hot room. Feet or meters, to match the units.")
    T.dv(ws, "decimal", "C7:C9", operator="between", formula1="0", formula2="11.99", errorTitle="Inches", error="Enter inches from 0 to 11.99. Used only in ft mode.",
         promptTitle="Inches", prompt="Extra inches. Used only in ft mode; leave empty in m mode.")
    T.dv(ws, "decimal", "B10:B11", operator="greaterThanOrEqual", formula1="0", errorTitle="Area", error="Enter an area, 0 or more.",
         promptTitle="Area", prompt="Width x height of each uninsulated surface, added up. sq ft or m², to match the units.")
    T.dv(ws, "list", "B12", formula1='"Yes,No"', errorTitle="Log walls", error="Pick Yes or No.")
    T.dv(ws, "list", "B13", formula1='"Electric,Wood-burning"', errorTitle="Heater type", error="Pick Electric or Wood-burning.")
    # inches are not used in meter mode: gray them out
    ws.conditional_formatting.add("C7:C9", FormulaRule(formula=['$B$5="m"'], fill=T.fill(T.CALC), font=T.font(10, color=T.CALC)))
    ws.conditional_formatting.add("B14", FormulaRule(formula=['$B$14<>"OK"'], font=T.font(10, True, T.EMBER)))
    T.page(ws, "A1:E40", margin=0.5)
    return ws


def examples(wb):
    ws = wb.create_sheet("Examples")
    T.setup(ws, 20, [24, 44, 9, 9, 9, 9, 9, 8, 14, 11, 11, 11, 11, 10, 10, 46])
    T.title(ws, "Worked examples", "The manufacturers' own examples, run through the same formulas. All sizes in meters and m². Change a white cell to try another room.")
    T.head_row(ws, 4, ["Example", "Room", "Length m", "Width m", "Height m", "Glass m²", "Stone m²", "Log walls", "Heater",
                       "Room volume m³", "Calculated volume m³ (Harvia)", "HUUM rule m³", "HUUM N.A. sheet m³", "kW low", "kW high", "What the source says"], height=44, size=9)
    for i, (name, room, L, W, H, g, s, log, heater, says) in enumerate(EXAMPLES):
        r = 5 + i
        ws.row_dimensions[r].height = 32
        T.label(ws.cell(r, 1, name), boxed=True, bold=True, color=T.INK, wrap=True)
        T.label(ws.cell(r, 2, room), boxed=True, wrap=True, size=9)
        for col, v in zip(range(3, 8), (L, W, H, g, s)):
            T.inp(ws.cell(r, col, round(v, 4)), "0.0##")
        T.inp(ws.cell(r, 8, log)); T.inp(ws.cell(r, 9, heater), size=9)
        T.calc(ws.cell(r, 10, f"=C{r}*D{r}*E{r}"), "0.00", color=T.INK)
        T.calc(ws.cell(r, 11, f'=J{r}*IF(H{r}="Yes",1.5,1)+(F{r}+G{r})*1.2'), "0.00", color=T.INK, bold=True)
        T.calc(ws.cell(r, 12, f'=IF(H{r}="Yes","n/a",J{r}+(F{r}+G{r})*1)'), "0.00", color=T.INK)
        T.calc(ws.cell(r, 13, f'=IF(H{r}="Yes","n/a",J{r}+(F{r}+G{r})*1.5)'), "0.00", color=T.INK)
        T.calc(ws.cell(r, 14, f'=IF(I{r}="Electric",K{r}*{CUFT_PER_M3}/50,"n/a")'), "0.0", color=T.INK)
        T.calc(ws.cell(r, 15, f'=IF(I{r}="Electric",K{r}*1,"n/a")'), "0.0", color=T.INK)
        T.label(ws.cell(r, 16, says), boxed=True, wrap=True, size=9)
    last = 4 + len(EXAMPLES)
    T.dv(ws, "list", f"H5:H{last}", formula1='"Yes,No"', errorTitle="Log walls", error="Pick Yes or No.")
    T.dv(ws, "list", f"I5:I{last}", formula1='"Electric,Wood-burning"', errorTitle="Heater", error="Pick Electric or Wood-burning.")
    T.note(ws, last + 2, "The first row is the sample room of the Calculator sheet (6 x 5 x 7 ft, a 12 sq ft glass door) converted to meters. The last row is our own illustration of the log wall factor, not a published example.")
    T.note(ws, last + 3, "Always confirm with the heater manufacturer and a licensed electrician. Follow the manufacturer's manual.")
    T.credit(ws, last + 5)
    T.page(ws, f"A1:P{last + 5}", landscape=True)
    return ws


def sources(wb):
    ws = wb.create_sheet("Sources")
    T.setup(ws, 40, [104, 4])
    T.title(ws, "Sources", "Every factor in this file comes from a heater maker's own published guidance. All links checked in November 2026.")
    r = 4
    for name, url, what in SOURCES:
        c = ws.cell(r, 1, name)
        c.font = T.font(11, True)
        u = ws.cell(r + 1, 1, url)
        u.hyperlink = url
        u.font = T.font(9, color=T.INK2, underline="single")
        if what:
            w = ws.cell(r + 2, 1, what)
            w.font = T.font(10, color=T.INK2)
            w.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r + 2].height = 15 * (1 + len(what) // 115)
            r += 4
        else:
            r += 3
    n = ws.cell(r, 1, WARN)
    n.font = T.font(10, True)
    n.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 46
    T.credit(ws, r + 2)
    T.page(ws, f"A1:A{r + 2}", margin=0.5)
    return ws


def py_calc(L, W, H, glass=0.0, stone=0.0, log=False, electric=True):
    """Independent copy of the rules, for the CSV and the checks."""
    vol = L * W * H
    surf = glass + stone
    cv = vol * (1.5 if log else 1) + surf * 1.2
    return dict(volume_m3=vol, volume_cuft=vol * CUFT_PER_M3, calc_m3=cv, calc_cuft=cv * CUFT_PER_M3,
                huum_m3=None if log else vol + surf, huum_na_m3=None if log else vol + surf * 1.5,
                kw_low=cv * CUFT_PER_M3 / 50 if electric else None, kw_high=cv if electric else None)


def build(path):
    wb = Workbook()
    calculator(wb)
    examples(wb)
    sources(wb)
    T.howto(wb, HOWTO)
    T.props(wb, "Sauna Heater Sizing Sheet", "Sauna heater size worksheet using Harvia and HUUM published rules.")
    wb.save(path)


def main():
    d = os.path.join(T.ROOT, SLUG)
    os.makedirs(d, exist_ok=True)
    build(os.path.join(d, SLUG + ".xlsx"))
    f1 = lambda v, n=1: "n/a" if v is None else f"{v:.{n}f}"
    with open(os.path.join(d, SLUG + "-examples.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Example", "Room", "Length (m)", "Width (m)", "Height (m)", "Uninsulated glass (m2)", "Uninsulated stone (m2)", "Log walls",
                    "Heater", "Room volume (m3)", "Room volume (cu ft)", "Calculated volume, Harvia rule (m3)", "Calculated volume (cu ft)",
                    "HUUM rule (m3)", "HUUM North American sheet (m3)", "Power low (kW)", "Power high (kW)", "What the source says"])
        for name, room, L, W, H, g, s, log, heater, says in EXAMPLES:
            p = py_calc(L, W, H, g, s, log == "Yes", heater == "Electric")
            w.writerow([name, room, round(L, 4), round(W, 4), round(H, 4), round(g, 4), s, log, heater, f1(p["volume_m3"], 2), f1(p["volume_cuft"], 0),
                        f1(p["calc_m3"], 2), f1(p["calc_cuft"], 0), f1(p["huum_m3"], 2), f1(p["huum_na_m3"], 2), f1(p["kw_low"]), f1(p["kw_high"]), says])
    return [os.path.join(d, SLUG + ".xlsx")]


if __name__ == "__main__":
    print(main())
