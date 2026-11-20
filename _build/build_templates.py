#!/usr/bin/env python3
"""Builds the DIVELUX spreadsheet and Notion templates.   Usage: python3 build_templates.py [--no-preview]

Steps: write the .xlsx / .csv / notion-template.md files -> recalculate every workbook with the `formulas` package and
fail on any Excel error value -> compare the key totals with an independent calculation in Python (and, for the heater
sheet, with ../../tools/sauna-heater-calculator/heater.js) -> reopen every file with openpyxl -> draw preview.png
(one Chromium, under flock /tmp/freebies-chromium.lock).
Needs: pip install openpyxl formulas pillow; Node with Playwright for the previews.
"""
import datetime as dt
import json
import os
import subprocess
import sys

import openpyxl

import preview as P
import t13_budget as B
import t14_heater as H
import t15_rota as R
import t16_booking as K
import t17_notion as N
import tcommon as T
from recalc import errors_in, recalc

EPOCH = dt.date(1899, 12, 30)
serial = lambda d: (d - EPOCH).days
problems = []


def check(ok, what):
    if not ok:
        problems.append(what)
        print("   !!", what)


def near(a, b, tol=1e-6):
    return isinstance(a, (int, float)) and abs(a - b) <= tol


def recalc_all(paths):
    out = {}
    for p in paths:
        v = recalc(p)
        bad = errors_in(v)
        wb = openpyxl.load_workbook(p)          # reopens cleanly
        n = sum(1 for ws in wb.worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("="))
        for ws in wb.worksheets:                 # every sheet carries the credit line with a live link
            creds = [c for row in ws.iter_rows() for c in row if c.value == T.CREDIT]
            check(creds and creds[0].hyperlink and creds[0].hyperlink.target == T.SITE, f"{os.path.basename(p)} / {ws.title}: credit line or link missing")
        print(f"{os.path.relpath(p, T.ROOT)}: {len(wb.sheetnames)} sheets, {n} formulas, {len(bad)} errors, {os.path.getsize(p) // 1024} KB")
        for b in bad:
            check(False, f"{os.path.basename(p)}: {b}")
        out[p] = v
    return out


def check_budget(vals, example):
    s, b = vals["SUMMARY"], vals["BUDGET"]
    lines = [(cat, B.EXAMPLE.get(item)) for cat, item in B.LINES] if example else []
    tot = B.S_FIRST + len(B.CATS)
    for i, cat in enumerate(B.CAT_NAMES):
        mine = [e for c, e in lines if c == cat and e]
        planned = sum(e[0] for e in mine)
        actual = sum(e[1] for e in mine if e[1] is not None)
        diff = sum(e[1] - e[0] for e in mine if e[1] is not None)
        r = B.S_FIRST + i
        check(near(s.get(f"B{r}", 0), planned) and near(s.get(f"C{r}", 0), actual) and near(s.get(f"D{r}", 0), diff), f"budget {cat}: totals differ")
    allv = [e for _, e in lines if e]
    planned = sum(e[0] for e in allv); actual = sum(e[1] for e in allv if e[1] is not None)
    over = sum(e[1] - e[0] for e in allv if e[1] is not None)
    paid = sum(e[1] for e in allv if e[1] is not None and e[2] == "Yes")
    r0 = tot + 3
    want = {f"B{tot}": planned, f"C{tot}": actual, f"D{tot}": over, f"B{r0 + 1}": planned * 0.1, f"B{r0 + 2}": planned * 1.1, f"B{r0 + 3}": actual,
            f"B{r0 + 4}": planned * 1.1 - actual, f"B{r0 + 5}": paid, f"B{r0 + 6}": actual - paid, f"B{r0 + 7}": planned * 0.1 - max(0, over)}
    for ref, w in want.items():
        check(near(s.get(ref, 0), w), f"budget Summary!{ref}: {s.get(ref)} != {w}")
    check(near(b.get("C6", 0), planned) and near(b.get("D6", 0), actual) and near(b.get("E6", 0), over), "budget total row differs")
    return dict(planned=planned, actual=actual, over=over, paid=paid)


def check_heater(vals):
    c, e = vals["CALCULATOR"], vals["EXAMPLES"]
    js = os.path.join(os.path.dirname(T.ROOT), "tools", "sauna-heater-calculator", "heater.js")
    rows = [dict(length=L, width=W, height=Hh, glass=g, masonry=s, log=log == "Yes", heater="electric" if heater == "Electric" else "wood")
            for _, _, L, W, Hh, g, s, log, heater, _ in H.EXAMPLES]
    code = f"const H=require({json.dumps(js)});console.log(JSON.stringify({json.dumps(rows)}.map(r=>H.calc(r))))"
    ref = json.loads(subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True).stdout)
    r1 = lambda v, n=1: None if v is None or v == "n/a" else round(v + 1e-12, n)
    for i, (ex, j) in enumerate(zip(H.EXAMPLES, ref)):
        r = 5 + i
        py = H.py_calc(ex[2], ex[3], ex[4], ex[5], ex[6], ex[7] == "Yes", ex[8] == "Electric")
        got = dict(vol=e[f"J{r}"], calc=e[f"K{r}"], huum=e[f"L{r}"], na=e[f"M{r}"], lo=e[f"N{r}"], hi=e[f"O{r}"])
        check(j["ok"], f"heater example {ex[0]}: heater.js rejected the room")
        check(near(got["vol"], py["volume_m3"], 1e-9) and near(got["calc"], py["calc_m3"], 1e-9), f"heater example {ex[0]}: sheet vs Python")
        check(r1(got["calc"]) == j["calcVolumeM3"] and r1(got["vol"], 2) == j["volumeM3"], f"heater example {ex[0]}: calculated volume vs heater.js")
        check(r1(got["huum"]) == j["byRule"]["huum"] and r1(got["na"]) == j["byRule"]["huumNA"], f"heater example {ex[0]}: HUUM figures vs heater.js")
        kw = j["kw"] or {"low": None, "high": None}
        check(r1(got["lo"]) == kw["low"] and r1(got["hi"]) == kw["high"], f"heater example {ex[0]}: kW vs heater.js ({got['lo']}, {got['hi']} / {kw})")
    # the published results quoted in the README of the calculator
    check(round(e["K6"], 1) == 11.9 and round(e["K7"], 2) == 13.77 and round(e["L8"], 2) == 11.88 and round(e["N9"], 1) == 6.0 and round(e["O9"], 1) == 8.5,
          "heater: a manufacturer's worked example is not reproduced")
    # Calculator sheet with its sample room in feet = README call: 210 cu ft, 7.3 m³, 257 cu ft, 5.1 to 7.3 kW
    check(c["B14"] == "OK" and round(c["C18"]) == 210 and round(c["B22"], 1) == 7.3 and round(c["C22"]) == 257 and round(c["B23"], 1) == 5.1
          and round(c["B24"], 1) == 7.3, "heater Calculator: sample room does not give 210 cu ft / 7.3 m³ / 257 cu ft / 5.1-7.3 kW")
    check(near(c["B30"], j0 := ref[0]["byRule"]["huum"], 0.05) and near(c["B31"], ref[0]["byRule"]["huumNA"], 0.05), "heater Calculator: three-rule table")
    return ref


def heater_variants():
    """The Calculator sheet in other states: meters, log walls, wood stove, bad input. Each is saved to /tmp, recalculated, compared."""
    cases = [
        (dict(B5="m", B7=2.0, B8=2.5, B9=2.3, B10=1.89, B11=0, B12="No", B13="Wood-burning"), dict(B22=13.768, B23="n/a", B24="n/a", B14="OK")),
        (dict(B5="m", B7=2, B8=2, B9=2, B10=1, B11=0, B12="Yes", B13="Electric"), dict(B22=13.2, B24=13.2, B30="n/a", B31="n/a", B14="OK")),
        (dict(B5="ft", B7=6, C7=6, B8=5, B9=7, B10=12, B11=8, B12="No", B13="Electric"),
         dict(B22=(6.5 * 5 * 7) / H.CUFT_PER_M3 * (H.CUFT_PER_M3 * H.M_PER_FT ** 3) + (20 / H.SQFT_PER_M2) * 1.2)),
        (dict(B5="ft", B7=2, B8=5, B9=7, B10=0, B11=0, B12="No", B13="Electric"), dict(B22=None, B23=None, F14=False)),
        (dict(B5="m", B7=2, B8=2, B9=2, B10=30, B11=0, B12="No", B13="Electric"), dict(B22=None, F14=False)),
    ]
    src = os.path.join(T.ROOT, H.SLUG, H.SLUG + ".xlsx")
    for i, (inp, want) in enumerate(cases):
        wb = openpyxl.load_workbook(src)
        ws = wb["Calculator"]
        ws["C7"] = None
        for ref, v in inp.items():
            ws[ref] = v
        tmp = f"/tmp/tpl-heater-case{i}.xlsx"
        wb.save(tmp)
        v = recalc(tmp)
        check(not errors_in(v), f"heater case {i}: error values {errors_in(v)[:3]}")
        c = v["CALCULATOR"]
        for ref, w in want.items():
            g = c.get(ref)
            ok = (g is None or g == "") if w is None else (near(g, w, 1e-3) if isinstance(w, float) else g == w)
            check(ok, f"heater case {i}: {ref} = {g!r}, expected {w!r}")
        os.remove(tmp)
    print(f"heater sheet: {len(cases)} extra input cases checked (meters, log walls, wood stove, feet + inches, out-of-range input)")


def check_rota(vals, example):
    d, p = vals["DAILY"], vals["PERIODIC"]
    first = 9
    done_row = first + R.N_DAILY + 1
    if example:
        counts = [R.N_DAILY - sum(1 for (day, _) in R.EX_SKIP if day == i) if i < R.EX_FILLED else 0 for i in range(7)]
        got = [d.get(f"{c}{done_row}") for c in "CDEFGHI"]
        check(got == counts, f"rota Daily done counts {got} != {counts}")
        check(near(d["I4"], sum(counts) / (7 * R.N_DAILY)), "rota week complete")
        check([d.get(f"{c}7") for c in "CDEFGHI"] == [serial(R.EX_START) + i for i in range(7)], "rota dates")
        for i, (task, freq, _) in enumerate(R.PERIODIC):
            r = R.P_FIRST + i
            if i in R.EX_PERIODIC:
                due = R.EX_PERIODIC[i][0] + dt.timedelta(days=R.EVERY[freq])
                check(p.get(f"F{r}") == serial(due) and p.get(f"G{r}") == ("Due" if due < R.EX_TODAY else "OK"), f"rota Periodic row {r}: next due / status")
            else:
                check(p.get(f"G{r}") == "Not logged" and p.get(f"F{r}") in (None, ""), f"rota Periodic row {r}: should be Not logged")
    else:
        check(d.get("I4") == 0 and all(d.get(f"{c}{done_row}") == 0 for c in "CDEFGHI"), "rota template: counts should be 0")
        check(all(p.get(f"G{R.P_FIRST + i}") == "Not logged" for i in range(len(R.PERIODIC))), "rota template: status")
        check(p.get("B3") == serial(dt.date.today()), "rota template: TODAY()")


def check_booking(vals, example):
    s, b = vals["SUMMARY"], vals["BOOKINGS"]
    ex = K.EXAMPLE if example else []
    n = K.S_LAST - K.S_FIRST + 1
    day = [e for e in ex if e[0] == K.EX_DAY]
    for i, slot in enumerate(K.SLOTS):
        r = 6 + i
        mine = [e for e in day if e[1] == slot]
        want = [slot, K.CAPACITY, sum(e[3] for e in mine), K.CAPACITY - sum(e[3] for e in mine), len(mine),
                sum(1 for e in mine if e[4] != "Yes"), sum(e[5] or 0 for e in mine if e[4] == "Yes")] if example else [slot, K.CAPACITY]
        got = [s.get(f"{c}{r}") for c in "ABCDEFG"][:len(want)]
        check(got == want, f"booking Summary row {r}: {got} != {want}")
    tot = 6 + n
    if example:
        check([s.get(f"{c}{tot}") for c in "BCDEFG"] == [K.CAPACITY * len(K.SLOTS), sum(e[3] for e in day), K.CAPACITY * len(K.SLOTS) - sum(e[3] for e in day),
                                                        len(day), sum(1 for e in day if e[4] != "Yes"), sum(e[5] or 0 for e in day if e[4] == "Yes")], "booking day total")
        for i in range(7):
            r = tot + 4 + i
            dd = K.EX_DAY + dt.timedelta(days=i)
            mine = [e for e in ex if e[0] == dd]
            want = [serial(dd), K.CAPACITY * len(K.SLOTS), sum(e[3] for e in mine), K.CAPACITY * len(K.SLOTS) - sum(e[3] for e in mine), len(mine),
                    sum(1 for e in mine if e[4] != "Yes"), sum(e[5] or 0 for e in mine if e[4] == "Yes")]
            check([s.get(f"{c}{r}") for c in "ABCDEFG"] == want, f"booking week row {r}")
        for i, e in enumerate(ex):
            left = K.CAPACITY - sum(x[3] for x in ex if x[0] == e[0] and x[1] == e[1])
            check(b.get(f"H{K.FIRST + i}") == left, f"booking Seats left row {K.FIRST + i}")
    a0 = tot + 13
    want = [len(ex), sum(e[3] for e in ex), sum(1 for e in ex if e[4] == "Yes"), sum(1 for e in ex if e[4] != "Yes"), sum(e[5] or 0 for e in ex if e[4] == "Yes")]
    check([s.get(f"C{a0 + i}") for i in range(5)] == want, f"booking whole-log block {[s.get(f'C{a0 + i}') for i in range(5)]} != {want}")


def previews(calc):
    bd = os.path.join(T.ROOT, B.SLUG, B.SLUG + "-example.xlsx")
    v = calc[bd]
    tot = B.S_FIRST + len(B.CATS)
    planned = [v["SUMMARY"].get(f"B{r}", 0) for r in range(B.S_FIRST, tot)]
    actual = [v["SUMMARY"].get(f"C{r}", 0) for r in range(B.S_FIRST, tot)]
    chart_row = tot + 3 + 8 + 1
    svg = P.bar_chart_svg(B.CAT_NAMES, planned, actual, 640, 500, "Planned and actual by category")
    jobs = [(P.page(P.sheet_html(bd, "Budget", v, 45, 7, zoom=0.86) + P.sheet_html(bd, "Summary", v, chart_row + 27, 5, chart=(chart_row, svg, 640, 500), zoom=0.86)),
             os.path.join(T.ROOT, B.SLUG, "preview.png"))]
    hp = os.path.join(T.ROOT, H.SLUG, H.SLUG + ".xlsx")
    v = calc[hp]
    jobs.append((P.page(P.sheet_html(hp, "Calculator", v, 40, 5) + '<div style="display:flex;flex-direction:column;gap:24px;align-items:flex-start">'
                        + P.sheet_html(hp, "Examples", v, 15, 16, zoom=0.74) + P.sheet_html(hp, "Sources", v, 36, 1, zoom=0.86) + "</div>"),
                 os.path.join(T.ROOT, H.SLUG, "preview.png")))
    rp = os.path.join(T.ROOT, R.SLUG, R.SLUG + "-example.xlsx")
    v = calc[rp]
    jobs.append((P.page(P.sheet_html(rp, "Daily", v, 9 + R.N_DAILY + 6, 9) + P.sheet_html(rp, "Periodic", v, R.P_LAST + 4, 8, zoom=0.8)),
                 os.path.join(T.ROOT, R.SLUG, "preview.png")))
    kp = os.path.join(T.ROOT, K.SLUG, K.SLUG + "-example.xlsx")
    v = calc[kp]
    jobs.append((P.page(P.sheet_html(kp, "Bookings", v, 30, 8) + P.sheet_html(kp, "Summary", v, 42, 7)),
                 os.path.join(T.ROOT, K.SLUG, "preview.png")))
    jobs.append((P.page(N.mock_html()).replace("</style>", N.MOCK_CSS + "</style>", 1), os.path.join(T.ROOT, N.SLUG, "preview.png")))
    P.shoot(jobs)


def main():
    paths = B.main() + H.main() + R.main() + K.main()
    N.main()
    calc = recalc_all(paths)
    for p in paths:
        ex = p.endswith("-example.xlsx")
        if B.SLUG in p:
            t = check_budget(calc[p], ex)
            if ex:
                print(f"   budget example: planned ${t['planned']:,}, actual ${t['actual']:,}, net overrun ${t['over']:,}, paid ${t['paid']:,} (matches Python)")
        elif H.SLUG in p:
            check_heater(calc[p])
            print("   heater examples match heater.js and the manufacturers' published results")
        elif R.SLUG in p:
            check_rota(calc[p], ex)
        elif K.SLUG in p:
            check_booking(calc[p], ex)
    heater_variants()
    if "--no-preview" not in sys.argv:
        previews(calc)
    print("problems:", len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
