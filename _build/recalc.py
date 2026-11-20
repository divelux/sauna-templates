"""Recalculates a workbook with the `formulas` package (no Excel needed) and returns the computed values."""
import contextlib
import io
import os
import shutil
import tempfile

import formulas
import openpyxl

ERRORS = ("#REF!", "#NAME?", "#DIV/0!", "#VALUE!", "#N/A", "#NUM!", "#NULL!")


def recalc(path):
    """-> {SHEET NAME (upper case): {"A1": value}}; raises if formulas cannot compile a cell."""
    tmp = tempfile.mkdtemp(prefix="tpl-calc-")
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            xl = formulas.ExcelModel().loads(path).finish()
            xl.calculate()
            xl.write(dirpath=tmp)
        wb = openpyxl.load_workbook(os.path.join(tmp, os.listdir(tmp)[0]))
        out = {}
        for ws in wb.worksheets:
            out[ws.title.upper()] = {c.coordinate: c.value for row in ws.iter_rows() for c in row if c.value is not None}
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def errors_in(values):
    bad = []
    for sheet, cells in values.items():
        for ref, v in cells.items():
            if isinstance(v, str) and any(e in v for e in ERRORS):
                bad.append(f"{sheet}!{ref} = {v}")
    return bad
