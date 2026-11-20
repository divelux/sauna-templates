"""16. Sauna Booking Log for clubs: bookings by date and slot, seats left, paid yes/no, a day summary.
The log holds a name and nothing else about a person."""
import csv
import datetime as dt
import os

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment

import tcommon as T

SLUG = "sauna-booking-log"
FIRST, LAST = 6, 205          # booking rows
S_FIRST, S_LAST = 6, 17       # slot rows on Settings (12 slots)
MONEY = '$#,##0.00'
SLOTS = ["8:00 AM", "9:30 AM", "11:00 AM", "12:30 PM", "2:00 PM", "3:30 PM", "5:00 PM", "6:30 PM", "8:00 PM"]
CAPACITY = 8                  # placeholder: set your own on the Settings sheet
PRIVACY = ("Name only. Do not record phone numbers, emails, addresses, health details or card numbers in this file. "
           "A first name and an initial is enough.")

HOWTO = [
    ("h", "How to use this booking log"),
    ("p", "1. Settings sheet: type your session times in the Slot column, exactly as you want them to appear, and the number of seats for each. Up to 12 slots. The times and the capacity in the file are placeholders."),
    ("p", "2. Bookings sheet: one line per booking. Type the date, pick the slot from the drop-down, type a name and the number of guests. Set Paid? to Yes when the booking is paid and type the amount."),
    ("p", "3. Seats left shows the free seats in that date and slot after every booking on the sheet is counted. It turns orange and bold below zero: the slot is overbooked."),
    ("p", "4. Summary sheet: type a date in the white cell to see that day slot by slot (seats booked, seats left, bookings, unpaid, money received) and the seven days that start there."),
    ("p", "5. A new month or season: save a copy of the file and clear the white cells on the Bookings sheet. The sheet holds 200 bookings."),
    ("h", "Personal data"),
    ("p", PRIVACY + " If you need contact details, keep them in the system your club already uses for member data."),
    ("h", "What the gray cells do"),
    ("p", "Bookings, Seats left = the slot's capacity from Settings - all guests booked for the same date and slot."),
    ("p", "Summary: every figure adds up the Bookings lines that match the date and the slot (SUMPRODUCT, so a slot name such as 8:00 AM is matched exactly as written). Received adds the Amount of lines marked Paid. Unpaid = bookings - bookings marked Paid; an empty Paid? cell counts as unpaid."),
    ("h", "Good to know"),
    ("p", "A cancelled booking: delete the line, or set Guests to 0 and write the reason in Note. Slot names must match the Settings sheet exactly, so pick them from the drop-down."),
    ("p", "Other currencies: select the Amount cells and change the number format."),
    ("p", "Free to use, share and adapt under CC BY 4.0. Made by DIVELUX, makers of handmade wool sauna hats, Irvine, California."),
    ("l", T.SITE),
    ("l", T.TOOLS),
]

EX_DAY = dt.date(2027, 1, 9)
D2 = dt.date(2027, 1, 10)
EXAMPLE = [  # date, slot, name, guests, paid, amount, note   (made-up names)
    (EX_DAY, "8:00 AM", "Alex P.", 2, "Yes", 40, ""),
    (EX_DAY, "8:00 AM", "Maria", 1, "Yes", 20, ""),
    (EX_DAY, "9:30 AM", "Sam T.", 4, "Yes", 80, "Birthday group"),
    (EX_DAY, "9:30 AM", "Lena", 2, "No", None, "Pays at the desk"),
    (EX_DAY, "11:00 AM", "Chris W.", 3, "Yes", 60, ""),
    (EX_DAY, "5:00 PM", "Dana", 2, "Yes", 40, ""),
    (EX_DAY, "5:00 PM", "Omar R.", 4, "Yes", 80, ""),
    (EX_DAY, "5:00 PM", "Kim", 2, "No", None, ""),
    (EX_DAY, "6:30 PM", "Nora B.", 6, "Yes", 120, "Team outing"),
    (EX_DAY, "6:30 PM", "Jo", 3, "No", None, "Over capacity: move one guest"),
    (EX_DAY, "8:00 PM", "Pat", 1, "Yes", 20, ""),
    (D2, "9:30 AM", "Alex P.", 2, "Yes", 40, ""),
    (D2, "11:00 AM", "Rita", 5, "Yes", 100, ""),
    (D2, "5:00 PM", "Sam T.", 2, "No", None, ""),
]


def settings(wb):
    ws = wb.create_sheet("Settings")
    T.setup(ws, 26, [22, 18, 52])
    T.title(ws, "Settings", "Your session times and seats. The Bookings drop-down and the Summary read from here.")
    T.label(ws["A3"], "Club name", bold=True)
    T.inp(ws["B3"], align="left"); ws.merge_cells("B3:C3"); T.inp(ws["C3"], align="left")
    T.head_row(ws, S_FIRST - 1, ["Slot", "Capacity (seats)"], height=24)
    T.label(ws.cell(S_FIRST - 1, 3, "Placeholders: type your own times and seats. Up to 12 slots."), size=9, color=T.MUTED, italic=True)
    for i, r in enumerate(range(S_FIRST, S_LAST + 1)):
        ws.row_dimensions[r].height = 20
        T.inp(ws.cell(r, 1, SLOTS[i] if i < len(SLOTS) else None), "@")
        T.inp(ws.cell(r, 2, CAPACITY if i < len(SLOTS) else None), "0")
    T.dv(ws, "whole", f"B{S_FIRST}:B{S_LAST}", operator="between", formula1="1", formula2="500", errorTitle="Capacity",
         error="Enter a whole number of seats, 1 to 500.", promptTitle="Capacity", prompt="Seats in this slot.")
    T.note(ws, S_LAST + 2, "Write each slot as text, for example 8:00 AM or Morning. Rename a slot before you take bookings for it: old bookings keep the old name.")
    T.credit(ws, S_LAST + 4)
    T.page(ws, f"A1:C{S_LAST + 4}", margin=0.5)
    return ws


def bookings(wb, example):
    ws = wb.active
    ws.title = "Bookings"
    T.setup(ws, LAST + 6, [14, 14, 24, 9, 9, 13, 36, 12])
    T.title(ws, "Sauna Booking Log", "One line per booking. Type in the white cells. Seats left calculates itself.")
    T.label(ws["A3"], PRIVACY, size=9, bold=True, color=T.INK)
    ws.row_dimensions[4].height = 6
    T.head_row(ws, FIRST - 1, ["Date", "Slot", "Name", "Guests", "Paid?", "Amount", "Note", "Seats left"])
    for r in range(FIRST, LAST + 1):
        ws.row_dimensions[r].height = 18
        T.inp(ws.cell(r, 1), "ddd, mmm d")
        T.inp(ws.cell(r, 2), "@")
        T.inp(ws.cell(r, 3), align="left")
        T.inp(ws.cell(r, 4), "0")
        T.inp(ws.cell(r, 5))
        T.inp(ws.cell(r, 6), MONEY)
        T.inp(ws.cell(r, 7), align="left")
        # SUMPRODUCT with plain "=" tests: slot names such as "8:00 AM" are compared as they are written,
        # never re-read as a time the way SUMIFS criteria can be.
        T.calc(ws.cell(r, 8, f'=IF(OR(NOT(ISNUMBER(A{r})),B{r}=""),"",'
                             f'SUMPRODUCT((Settings!$A${S_FIRST}:$A${S_LAST}=B{r})*Settings!$B${S_FIRST}:$B${S_LAST})'
                             f'-SUMPRODUCT(($A${FIRST}:$A${LAST}=A{r})*($B${FIRST}:$B${LAST}=B{r})*$D${FIRST}:$D${LAST}))'), "0", color=T.INK2)
    if example:
        for i, row in enumerate(EXAMPLE):
            for c, v in enumerate(row, start=1):
                if v not in (None, ""):
                    ws.cell(FIRST + i, c, v)
    T.note(ws, LAST + 2, PRIVACY)
    T.credit(ws, LAST + 4)
    rng = lambda col: f"{col}{FIRST}:{col}{LAST}"
    T.dv(ws, "date", rng("A"), operator="greaterThan", formula1="36526", errorTitle="Date", error="Enter a date, for example 1/9/2027.",
         promptTitle="Date", prompt="Date of the session.")
    T.dv(ws, "list", rng("B"), formula1=f"=Settings!$A${S_FIRST}:$A${S_LAST}", errorTitle="Slot", error="Pick a slot from the list. Slots are set on the Settings sheet.",
         promptTitle="Slot", prompt="Pick from the list.")
    T.dv(ws, "whole", rng("D"), operator="between", formula1="0", formula2="500", errorTitle="Guests", error="Enter a whole number of guests.",
         promptTitle="Guests", prompt="How many seats this booking takes.")
    T.dv(ws, "list", rng("E"), formula1='"Yes,No"', errorTitle="Paid?", error="Pick Yes or No.", promptTitle="Paid?", prompt="Yes once the booking is paid.")
    T.dv(ws, "decimal", rng("F"), operator="greaterThanOrEqual", formula1="0", errorTitle="Amount", error="Enter the amount received, 0 or more.",
         promptTitle="Amount", prompt="Money received for this booking.")
    T.dv(ws, "textLength", rng("C"), operator="lessThanOrEqual", formula1="40", errorTitle="Name", error="Keep it to a name: 40 characters at most.",
         promptTitle="Name", prompt="A name only. No phone, email or other personal details.")
    ws.conditional_formatting.add(rng("H"), CellIsRule(operator="lessThan", formula=["0"], font=T.font(10, True, T.EMBER)))
    ws.freeze_panes = f"A{FIRST}"
    T.page(ws, f"A1:H{LAST + 4}", fit_height=0)
    ws.print_title_rows = f"{FIRST - 1}:{FIRST - 1}"
    return ws


def summary(wb, example):
    ws = wb.create_sheet("Summary")
    T.setup(ws, 44, [20, 13, 13, 13, 12, 12, 14])
    T.title(ws, "Summary", "Type a date in the white cell. Everything else is calculated from the Bookings and Settings sheets.")
    T.label(ws["A3"], "Show date", bold=True)
    T.inp(ws["B3"], "ddd, mmm d, yyyy", bold=True)
    ws.merge_cells("B3:C3"); T.inp(ws["C3"])
    if example:
        ws["B3"] = EX_DAY
    ws.row_dimensions[3].height = 22
    T.head_row(ws, 5, ["Slot", "Capacity", "Booked seats", "Seats left", "Bookings", "Unpaid", "Received"])
    BD, BS, BG, BP, BA = (f"Bookings!${c}${FIRST}:${c}${LAST}" for c in "ABDEF")
    n = S_LAST - S_FIRST + 1
    for i in range(n):
        r = 6 + i
        sr = S_FIRST + i
        ws.row_dimensions[r].height = 19
        has = f'AND(A{r}<>"",ISNUMBER($B$3))'
        T.calc(ws.cell(r, 1, f'=IF(Settings!A{sr}="","",Settings!A{sr})'), color=T.INK, bold=True)
        T.calc(ws.cell(r, 2, f'=IF(A{r}="","",Settings!B{sr})'), "0", color=T.INK2)
        T.calc(ws.cell(r, 3, f'=IF({has},SUMPRODUCT(({BD}=$B$3)*({BS}=A{r})*{BG}),"")'), "0", color=T.INK2)
        T.calc(ws.cell(r, 4, f'=IF({has},B{r}-C{r},"")'), "0", color=T.INK, bold=True)
        T.calc(ws.cell(r, 5, f'=IF({has},SUMPRODUCT(({BD}=$B$3)*({BS}=A{r})),"")'), "0", color=T.INK2)
        T.calc(ws.cell(r, 6, f'=IF({has},E{r}-SUMPRODUCT(({BD}=$B$3)*({BS}=A{r})*({BP}="Yes")),"")'), "0", color=T.INK2)
        T.calc(ws.cell(r, 7, f'=IF({has},SUMPRODUCT(({BD}=$B$3)*({BS}=A{r})*({BP}="Yes")*{BA}),"")'), MONEY, color=T.INK2)
    tot = 6 + n
    T.calc(ws.cell(tot, 1, "Day total"), align="left", bold=True, color=T.INK)
    for col, fmt in zip("BCDEFG", ["0"] * 5 + [MONEY]):
        T.calc(ws[f"{col}{tot}"], fmt, bold=True, color=T.INK).value = f"=SUM({col}6:{col}{tot - 1})"
    ws.row_dimensions[tot].height = 21
    w0 = tot + 3
    T.section(ws, w0 - 1, "Seven days from that date")
    T.head_row(ws, w0, ["Date", "Capacity", "Booked seats", "Seats left", "Bookings", "Unpaid", "Received"])
    for i in range(7):
        r = w0 + 1 + i
        ws.row_dimensions[r].height = 19
        T.calc(ws.cell(r, 1, f'=IF(ISNUMBER($B$3),$B$3+{i},"")'), "ddd, mmm d", color=T.INK, bold=True)
        T.calc(ws.cell(r, 2, f'=IF(A{r}="","",SUM(Settings!$B${S_FIRST}:$B${S_LAST}))'), "0", color=T.INK2)
        T.calc(ws.cell(r, 3, f'=IF(A{r}="","",SUMPRODUCT(({BD}=A{r})*{BG}))'), "0", color=T.INK2)
        T.calc(ws.cell(r, 4, f'=IF(A{r}="","",B{r}-C{r})'), "0", color=T.INK, bold=True)
        T.calc(ws.cell(r, 5, f'=IF(A{r}="","",SUMPRODUCT(({BD}=A{r})*1))'), "0", color=T.INK2)
        T.calc(ws.cell(r, 6, f'=IF(A{r}="","",E{r}-SUMPRODUCT(({BD}=A{r})*({BP}="Yes")))'), "0", color=T.INK2)
        T.calc(ws.cell(r, 7, f'=IF(A{r}="","",SUMPRODUCT(({BD}=A{r})*({BP}="Yes")*{BA}))'), MONEY, color=T.INK2)
    a0 = w0 + 10
    T.section(ws, a0 - 1, "Whole log")
    allrows = [
        ("Bookings on the sheet", f"=COUNT({BD})", "0"),
        ("Guests booked", f"=SUM({BG})", "0"),
        ("Bookings marked paid", f'=COUNTIF({BP},"Yes")', "0"),
        ("Bookings not paid yet", f'=COUNT({BD})-COUNTIF({BP},"Yes")', "0"),
        ("Money received", f'=SUMPRODUCT(({BP}="Yes")*{BA})', MONEY),
    ]
    for i, (lab, f, fmt) in enumerate(allrows):
        r = a0 + i
        ws.row_dimensions[r].height = 22
        T.label(ws.cell(r, 1, lab), size=11, boxed=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
        T.label(ws.cell(r, 2), boxed=True)
        T.calc(ws.cell(r, 3, f), fmt, align="right", size=12, bold=True, color=T.INK)
    end = a0 + len(allrows) + 1
    T.note(ws, end, "Seats left below zero means the slot is overbooked. Unpaid counts every booking whose Paid? cell is not Yes.")
    T.credit(ws, end + 2)
    T.dv(ws, "date", "B3", operator="greaterThan", formula1="36526", errorTitle="Date", error="Enter a date, for example 1/9/2027.",
         promptTitle="Show date", prompt="The day you want to see.")
    ws.conditional_formatting.add(f"D6:D{tot}", CellIsRule(operator="lessThan", formula=["0"], font=T.font(10, True, T.EMBER)))
    ws.conditional_formatting.add(f"D{w0 + 1}:D{w0 + 7}", CellIsRule(operator="lessThan", formula=["0"], font=T.font(10, True, T.EMBER)))
    T.page(ws, f"A1:G{end + 2}", margin=0.5)
    return ws


def build(path, example=False):
    wb = Workbook()
    bookings(wb, example)
    summary(wb, example)
    settings(wb)
    T.howto(wb, HOWTO)
    T.props(wb, "Sauna Booking Log for Clubs", "Booking log with slots, seats left and paid status for a sauna club.")
    wb.save(path)


def main():
    d = os.path.join(T.ROOT, SLUG)
    os.makedirs(d, exist_ok=True)
    build(os.path.join(d, SLUG + ".xlsx"))
    build(os.path.join(d, SLUG + "-example.xlsx"), example=True)
    with open(os.path.join(d, SLUG + ".csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Slot", "Name", "Guests", "Paid", "Amount", "Note"])
        w.writerow(["2027-01-09", "8:00 AM", "Alex P.", 2, "Yes", "40.00", "Example row: delete it"])
        w.writerow(["2027-01-09", "9:30 AM", "Lena", 2, "No", "", "Example row: delete it"])
    return [os.path.join(d, SLUG + ".xlsx"), os.path.join(d, SLUG + "-example.xlsx")]


if __name__ == "__main__":
    print(main())
