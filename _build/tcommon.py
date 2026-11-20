"""Shared pieces for the DIVELUX spreadsheet templates: palette, cell styles, page setup, credit line.
Needs: pip install openpyxl.   License of the templates: CC BY 4.0 - DIVELUX, https://diveluxsaunahat.com
"""
import os

from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://diveluxsaunahat.com"
TOOLS = "https://diveluxsaunahat.com/pages/sauna-tools"
CREDIT = "Made by DIVELUX, makers of wool sauna hats — diveluxsaunahat.com"
PAPER, CARD, CALC, INK, INK2, MUTED, LINE, WOOD, TAN, EMBER = (
    "F6F3EE", "FFFFFF", "EFEAE2", "1B1512", "3D332C", "6F655C", "E3DDD3", "2A1B13", "C99B6C", "F0762E")
HEAD_FONT, BODY_FONT = "Bricolage Grotesque", "Inter"

thin = Side(style="thin", color=LINE)
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)


def fill(c):
    return PatternFill("solid", start_color=c, end_color=c)


def font(size=10, bold=False, color=INK, head=False, italic=False, underline=None):
    return Font(name=HEAD_FONT if head else BODY_FONT, size=size, bold=bold, color=color, italic=italic, underline=underline)


def setup(ws, rows, widths):
    """Paper background, no grid lines, column widths."""
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = w
    for r in range(1, rows + 1):
        for c in range(1, len(widths) + 1):
            ws.cell(r, c).fill = fill(PAPER)


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = font(22, True, head=True)
    ws.row_dimensions[1].height = 34
    if sub:
        ws["A2"] = sub
        ws["A2"].font = font(10, color=MUTED)
        ws["A2"].alignment = Alignment(vertical="top")
        ws.row_dimensions[2].height = 22


def head_row(ws, row, labels, c0=1, height=30, size=10):
    for i, h in enumerate(labels):
        c = ws.cell(row, c0 + i, h)
        c.font = font(size, True, "FFFFFF")
        c.fill = fill(WOOD)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = height


def inp(c, fmt=None, align="center", wrap=False, size=10, bold=False):
    """White cell the user types in."""
    c.fill = fill(CARD); c.border = BOX
    c.font = font(size, bold)
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if fmt:
        c.number_format = fmt
    return c


def calc(c, fmt=None, align="center", size=10, bold=False, color=MUTED, wrap=False):
    """Gray cell that calculates itself."""
    c.fill = fill(CALC); c.border = BOX
    c.font = font(size, bold, color)
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if fmt:
        c.number_format = fmt
    return c


def label(c, text=None, size=10, bold=False, color=INK2, wrap=False, align="left", boxed=False, italic=False):
    if text is not None:
        c.value = text
    c.font = font(size, bold, color, italic=italic)
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if boxed:
        c.fill = fill(CARD); c.border = BOX
    return c


def section(ws, row, text, size=14):
    c = ws.cell(row, 1, text)
    c.font = font(size, True, head=True)
    c.alignment = Alignment(vertical="bottom")
    ws.row_dimensions[row].height = 28
    return c


def note(ws, row, text, col=1, color=MUTED, size=9, wrap_to=None, height=None):
    c = ws.cell(row, col, text)
    c.font = font(size, color=color)
    if wrap_to:
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=wrap_to)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if height:
            ws.row_dimensions[row].height = height
    return c


def credit(ws, row, col=1):
    c = ws.cell(row, col, CREDIT)
    c.font = font(9, color=INK2)
    c.hyperlink = SITE
    return c


def page(ws, area, landscape=False, fit_height=1, margin=0.4):
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = fit_height
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = area
    ws.page_margins.left = ws.page_margins.right = margin
    ws.page_margins.top = ws.page_margins.bottom = margin
    ws.print_options.horizontalCentered = True


def dv(ws, kind, rng, **kw):
    v = DataValidation(type=kind, allow_blank=True, showErrorMessage=True, showInputMessage=bool(kw.get("prompt")), **kw)
    ws.add_data_validation(v)
    v.add(rng)
    return v


def howto(wb, items, name="How to use", width=104):
    """items: ('h', heading) | ('p', paragraph) | ('l', url)."""
    ws = wb.create_sheet(name)
    setup(ws, len(items) + 6, [width, 4])
    r = 1
    for kind, text in items:
        c = ws.cell(r, 1, text)
        if kind == "h":
            c.font = font(20 if r == 1 else 14, True, head=True)
            ws.row_dimensions[r].height = 34 if r == 1 else 30
            c.alignment = Alignment(vertical="bottom")
        elif kind == "l":
            c.hyperlink = text
            c.font = font(11, underline="single")
            ws.row_dimensions[r].height = 18
        else:
            c.font = font(11, color=INK2)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r].height = 17 * (1 + len(text) // (width + 4))
        r += 1
    credit(ws, r + 1)
    page(ws, f"A1:A{r + 1}", margin=0.5)
    return ws


def props(wb, title_, what):
    wb.properties.creator = "DIVELUX"
    wb.properties.title = title_
    wb.properties.description = f"{what} Free template by DIVELUX - https://diveluxsaunahat.com - CC BY 4.0"
    wb.properties.keywords = "sauna, DIVELUX, template"
