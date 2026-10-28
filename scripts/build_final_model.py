"""Build final/Margin_Callers.xlsx: final competition model (CPRT short), live formulas, no cell fills.

Mechanics identical to scenario_engine.cprt_quarters and cprt_framework_b (verified by verify_final_model.py).
Factual hygiene: no carrier identity, no unsourced synergy figure, no proprietary-data claims; team estimates labelled.
Style: white background, navy titles/headers, blue inputs, black formulas, green cross-sheet links, red negatives.
"""

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter

import scenario_engine as se
from common import ROOT

# ------------------------------------------------------------------ style
FN = "Arial"
NAVY, BLUE, GREEN, BLACK, GRAY = "17365D", "0000FF", "00703C", "000000", "8C96A5"
F_TITLE = Font(name=FN, size=14, bold=True, color=NAVY)
F_SUB = Font(name=FN, size=9, color=BLACK)
F_SEC = Font(name=FN, size=10, bold=True, color=NAVY)
F_HDR = Font(name=FN, size=9, bold=True, color=NAVY)
F_BODY = Font(name=FN, size=9, color=BLACK)
F_BOLD = Font(name=FN, size=9, bold=True, color=BLACK)
F_IN = Font(name=FN, size=9, color=BLUE)
F_LINK = Font(name=FN, size=9, color=GREEN)
F_LINKB = Font(name=FN, size=9, bold=True, color=GREEN)
F_NOTE = Font(name=FN, size=8, italic=True, color=BLACK)
SEC_LINE = Border(bottom=Side(style="medium", color=NAVY))
HDR_LINE = Border(bottom=Side(style="thin", color=NAVY))
ROW_LINE = Border(bottom=Side(style="hair", color=GRAY))
BOX = Side(style="thin", color=GRAY)

USD = '$#,##0.00_);[Red]($#,##0.00);"-"_)'
USDM = '#,##0.0_);[Red](#,##0.0);"-"_)'
PCT = '0.0%_);[Red](0.0%);"-"_)'
PCT2 = '0.00%_);[Red](0.00%);"-"_)'
MULT = '0.0"x"_);[Red](0.0"x");"-"_)'
NUM1 = '#,##0.0_);[Red](#,##0.0);"-"_)'
NUM2 = '0.00_);[Red](0.00);"-"_)'
PCTS = '+0.0%;[Red]-0.0%;"-"'

wb = Workbook()
wb.properties.creator = "Margin Callers"
wb.properties.lastModifiedBy = "Margin Callers"
wb.properties.title = "Margin Callers - CPRT Short model"


def ws_setup(ws, widths):
    ws.sheet_view.showGridLines = False
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = F_TITLE
    if sub:
        ws["A2"] = sub
        ws["A2"].font = F_SUB


def section(ws, row, text, ncols):
    ws.cell(row, 1, text).font = F_SEC
    for c in range(1, ncols + 1):
        ws.cell(row, c).border = SEC_LINE


def header(ws, row, labels, start=1, align_right_from=2):
    for i, lab in enumerate(labels):
        c = ws.cell(row, start + i, lab)
        c.font = F_HDR
        c.border = HDR_LINE
        c.alignment = Alignment(horizontal="left" if i < align_right_from - 1 else "right", wrap_text=True, vertical="bottom")


def put(ws, ref, v, fmt=None, font=F_BODY, wrap=False, align=None, border=None):
    ws[ref] = v
    ws[ref].font = font
    if fmt:
        ws[ref].number_format = fmt
    if wrap or align:
        ws[ref].alignment = Alignment(wrap_text=wrap, vertical="top", horizontal=align)
    if border:
        ws[ref].border = border
    return ws[ref]


def link_font(formula):
    return F_LINK if "!" in formula and formula.startswith("=") and not any(op in formula[1:] for op in "+-*/(") else F_BODY


# ================================================================== Inputs
I = wb.active
I.title = "Inputs"
ws_setup(I, {"A": 60, "B": 11, "C": 8, "D": 20, "E": 92})
title(I, "Inputs", "Blue = hard-coded input. Every input carries a source type and a pointer to the Sources sheet (row comments add detail).")
section(I, 4, "Market, capital structure and tax", 5)
header(I, 5, ["Input", "Value", "Units", "Source type", "Source / basis"], align_right_from=2)
I["C5"].alignment = Alignment(horizontal="center"); I["D5"].alignment = Alignment(horizontal="left"); I["E5"].alignment = Alignment(horizontal="left")
INP = [
    ("price", "Share price (10/1/26 close)", 27.29, USD, "$/sh", "Secondary market data", "Yahoo Finance daily close, 10/1/26 (Sources row 20)"),
    ("shares", "Diluted shares", 940.0, NUM1, "m", "Primary + team", "Q3-FY26 10-Q diluted WASO 942.8m; ~926m outstanding after buybacks; 940m used (Sources rows 3, 21)"),
    ("tax", "Effective tax rate", 0.195, PCT, "%", "Primary-derived", "FY26 10-K: tax $354.6m / pre-tax $1,835.0m = 19.3% (Sources row 4)"),
    ("cash0", "Cash + restricted cash + HTM securities, 7/31/26", 4.49, NUM2, "$bn", "Primary", "FY26 10-K: $1,907.9m cash, equivalents & restricted + $2,581.9m HTM (Sources row 5)"),
    ("cash1", "Cash + securities at horizon (FY27 year-end, post-ACV)", 3.50, NUM2, "$bn", "Team estimate", "$4.49bn − $1.90bn ACV + ~$0.91bn retained FCF (≈72% of FY26 FCF $1.27bn); each ±$0.2bn ≈ ±$0.21/sh"),
    ("int26", "FY26 interest income", 181.9, USDM, "$m", "Primary", "FY26 10-K segment note: interest income $181.9m (Sources row 7)"),
    ("intq1", "Interest income per quarter before ACV close", 38.0, USDM, "$m", "Team estimate", "Q3/Q4-FY26 actual $38.8m / $39.6m; cash before the ACV payment"),
]
row = 6
NM = {}
for key, lab, v, f, u, st, src in INP:
    I.cell(row, 1, lab).font = F_BODY
    put(I, f"B{row}", v, f, F_IN)
    put(I, f"C{row}", u, align="center")
    put(I, f"D{row}", st)
    put(I, f"E{row}", src, wrap=True)
    I[f"B{row}"].comment = Comment(f"{st}: {src}", "Margin Callers")
    for c in range(1, 6):
        I.cell(row, c).border = ROW_LINE
    NM[key] = f"Inputs!$B${row}"
    row += 1

section(I, row + 1, "Cost of equity", 5)
header(I, row + 2, ["Input", "Value", "Units", "Source type", "Source / basis"])
row += 3
COE_IN = [
    ("rf", "10-year U.S. Treasury yield (risk-free)", 0.0524, PCT2, "%", "Primary", "U.S. Treasury Daily Par Yield Curve, 10Y on 10/01/2026 = 5.24% (Sources row 15)"),
    ("beta", "Equity beta", 0.90, NUM2, "x", "Team estimate", "Weekly regression of CPRT on SPY, Jul-2023 to Sep-2026 = 0.89 (team calculation); Yahoo 1.03 shown in Sensitivity"),
    ("erp", "Equity risk premium", 0.05, PCT, "%", "Team estimate", "Conventional 5% US ERP"),
    ("gT", "Terminal growth", 0.03, PCT, "%", "Team estimate", "Long-run nominal growth assumption"),
    ("rf_stress", "Rate-cut stress: 10-year yield", 0.035, PCT2, "%", "Team estimate", "Stress case only (10Y back to 3.5%)"),
]
for key, lab, v, f, u, st, src in COE_IN:
    I.cell(row, 1, lab).font = F_BODY
    put(I, f"B{row}", v, f, F_IN)
    put(I, f"C{row}", u, align="center")
    put(I, f"D{row}", st)
    put(I, f"E{row}", src, wrap=True)
    I[f"B{row}"].comment = Comment(f"{st}: {src}", "Margin Callers")
    for c in range(1, 6):
        I.cell(row, c).border = ROW_LINE
    NM[key] = f"Inputs!$B${row}"
    row += 1
I.cell(row, 1, "Cost of equity = risk-free + beta × ERP").font = F_BOLD
put(I, f"B{row}", f"={NM['rf']}+{NM['beta']}*{NM['erp']}", PCT2, F_BOLD)
put(I, f"E{row}", "CAPM: 5.24% + 0.90 × 5.0% = 9.74%", wrap=True)
NM["coe"] = f"Inputs!$B${row}"
row += 1
I.cell(row, 1, "Stress cost of equity = stress risk-free + beta × ERP").font = F_BODY
put(I, f"B{row}", f"={NM['rf_stress']}+{NM['beta']}*{NM['erp']}", PCT2)
NM["coe_stress"] = f"Inputs!$B${row}"
row += 2

section(I, row, "Operating structure (KPI model)", 5)
header(I, row + 1, ["Input", "Value", "Units", "Source type", "Source / basis"])
row += 2
OPS = [
    ("sins", "U.S. insurance share of U.S. units", 0.76, PCT, "%", "Team estimate",
     "10-K: insurers supplied 79% of vehicles company-wide; U.S. mix set slightly lower given U.S. dealer/BluCar volume"),
    ("fix", "Fixed share of U.S. facility costs (does not flex with units near term)", 0.55, PCT, "%", "Team estimate",
     "Q4-FY26: U.S. facility costs +7.7% while U.S. units −5.7% (call) → majority fixed in the short run"),
    ("nonins", "U.S. non-insurance unit growth", 0.03, PCT, "%", "Team estimate", "Q4-FY26 U.S. non-insurance +0.2%, dealer units +5.8% (call)"),
    ("goth", "U.S. vehicle gross profit and G&A growth", 0.05, PCT, "%", "Team estimate", "FY26 U.S. G&A +3.7% (10-K segment note); ongoing investment"),
    ("gint", "International operating income and revenue growth", 0.10, PCT, "%", "Team estimate", "FY26 international op. income +8.2%; Q4 international revenue +11.7% (10-K, call)"),
]
for key, lab, v, f, u, st, src in OPS:
    I.cell(row, 1, lab).font = F_BODY
    put(I, f"B{row}", v, f, F_IN)
    put(I, f"C{row}", u, align="center")
    put(I, f"D{row}", st)
    put(I, f"E{row}", src, wrap=True)
    I[f"B{row}"].comment = Comment(f"{st}: {src}", "Margin Callers")
    for c in range(1, 6):
        I.cell(row, c).border = ROW_LINE
    NM[key] = f"Inputs!$B${row}"
    row += 1
row += 1

section(I, row, "FY26 quarterly segment actuals ($m) — Primary: 10-Qs Q1-Q3 FY26; Q4 = FY26 10-K less nine months", 5)
header(I, row + 1, ["Line ($m unless stated)", "Q1 Aug-Oct", "Q2 Nov-Jan", "Q3 Feb-Apr", "Q4 May-Jul"])
row += 2
INTL_REV = [202.4, 200.1, 234.2, 222.0]  # international service + vehicle sales revenue, FY26 quarters ($m)
SEGS = [("us_service", "U.S. service revenue"), ("us_vehicle", "U.S. vehicle sales"), ("us_facility", "U.S. facility operations"),
        ("us_cogs_vehicle", "U.S. cost of vehicle sales"), ("us_ga", "U.S. G&A"), ("intl_oi", "International operating income"),
        ("intl_rev", "International revenue (service + vehicle sales)"), ("interest", "Interest income")]
SEG = {}
for key, lab in SEGS:
    I.cell(row, 1, lab).font = F_BODY
    vals = INTL_REV if key == "intl_rev" else se.CPRT_FY26[key]
    for q in range(4):
        put(I, f"{get_column_letter(2 + q)}{row}", vals[q], USDM, F_IN)
    for c in range(1, 6):
        I.cell(row, c).border = ROW_LINE
    SEG[key] = row
    row += 1
I.cell(row, 1, "Share of lost-customer run-rate loss already reflected in FY26 quarter").font = F_BODY
for q in range(4):
    put(I, f"{get_column_letter(2 + q)}{row}", se.CPRT_LOSS_IN_BASE[q], PCT, F_IN)
I[f"E{row}"].comment = Comment("Team estimate: RB Global said the volume transitioned over the 90 days to 8/4/26, so ~60% of the "
                               "run-rate loss is assumed already in Q4-FY26 (May-Jul).", "Margin Callers")
for c in range(1, 6):
    I.cell(row, c).border = ROW_LINE
SEG["lib"] = row
row += 1
put(I, f"A{row + 1}", "Reported FY26 diluted EPS by quarter (calibration check, Checks sheet)", font=F_BODY)
for q, v in enumerate([0.41, 0.36, 0.43, 0.35]):
    put(I, f"{get_column_letter(2 + q)}{row + 1}", v, USD, F_IN)
SEG["eps26"] = row + 1
I.freeze_panes = "B6"

# ================================================================== Scenarios
S = wb.create_sheet("Scenarios")
ws_setup(S, {"A": 54, "B": 24, "C": 24, "D": 24, "E": 24})
title(S, "Scenarios", "Four economic worlds: what the market believes → KPIs → earnings → justified multiple. Blue = team estimate.")
WN = ["W1 Loss deepens", "W2 FY27 trough / FY28 normalizes", "W3 Cycle turns / ACV improves", "W4 Street right / share recapture"]
section(S, 4, "Scenario drivers (all team estimates; basis in narrative row and Sources)", 5)
header(S, 5, ["Driver"] + WN)
W4 = dict(u=0.03, loss=-0.05, rpu=0.05, fixed=0.04, acv_amort=10, acv_op=0, int_q=28)
worlds = [se.CPRT_WORLDS["bear"], se.CPRT_WORLDS["base"], se.CPRT_WORLDS["bull"], W4]
extra = [(0.20, 0.04, 0.03, 0.15), (0.45, 0.12, 0.06, 0.20), (0.20, 0.18, 0.09, 0.25), (0.15, 0.15, 0.10, 0.25)]
PR = [("u", "Underlying U.S. insurance unit growth, ex lost customer", PCT),
      ("loss", "Lost-customer run-rate loss (pts of U.S. insurance units)", PCT),
      ("rpu", "Revenue per unit growth", PCT),
      ("fixed", "Fixed facility cost growth", PCT),
      ("acv_amort", "ACV acquired-intangible amortization per quarter ($m)", USDM),
      ("acv_op", "ACV operating income per quarter ($m)", USDM),
      ("int_q", "Interest income per quarter after ACV close ($m)", USDM)]
P = {}
r = 6
for key, lab, f in PR:
    S.cell(r, 1, lab).font = F_BODY
    for j, w in enumerate(worlds):
        put(S, f"{get_column_letter(2 + j)}{r}", w[key], f, F_IN, align="right")
    for c in range(1, 6):
        S.cell(r, c).border = ROW_LINE
    P[key] = r
    r += 1
for k, (key, lab, f) in enumerate([("prob", "Probability", PCT), ("g28", "FY28 EPS growth", PCT),
                                    ("g5", "EPS growth, 5 years after FY28", PCT), ("roic", "Incremental ROIC", PCT)]):
    S.cell(r, 1, lab).font = F_BODY
    for j in range(4):
        put(S, f"{get_column_letter(2 + j)}{r}", extra[j][k], f, F_IN, align="right")
    for c in range(1, 6):
        S.cell(r, c).border = ROW_LINE
    P[key] = r
    r += 1
S.cell(r, 1, "Probability check (must equal 100%)").font = F_BOLD
put(S, f"B{r}", f"=SUM(B{P['prob']}:E{P['prob']})", PCT, F_BOLD, align="right")
P["probcheck"] = r
r += 2
section(S, r, "Narrative and evidence (short; sources on Sources sheet)", 5)
NARR = ["Loss broadens; ASP softens (Manheim −0.4% y/y mid-Sep, Cox); OpEx/car stays high (+12.7% in Q4, call).",
        "Lost-customer volume runs at full rate Q1-Q3 and laps in Q4 (Copart Q4 call; RB Global Q2 call). Costs +7% fixed. ACV per model.",
        "Ex-customer insurance units +3% (Q4 ex-customer +2.3%, call); record 23.3% total-loss frequency (call).",
        "Share recapture offsets most of the lost volume; published FY27 consensus roughly delivered. Team scenario based on public data only."]
for j, t in enumerate(NARR):
    put(S, f"{get_column_letter(2 + j)}{r + 1}", t, font=F_BODY, wrap=True)
S.row_dimensions[r + 1].height = 92
S.freeze_panes = "B6"

# ================================================================== EPS build
E = wb.create_sheet("EPS_Build")
ws_setup(E, {"A": 52, "B": 12, "C": 12, "D": 12, "E": 12, "F": 12})
title(E, "FY27 EPS build (Aug-26 to Jul-27), $m unless stated",
      "Chain: lost-customer impact → U.S. insurance units → U.S. service revenue → operating income → EPS. "
      "ACV consolidated from Q2 (close expected mid-Oct-26). Ex-ACV and GAAP-with-ACV kept separate.")
LINES = [
    ("loss", "Lost-customer impact vs FY26 quarter (pts)", PCT),
    ("ins", "U.S. insurance units y/y", PCT),
    ("units", "U.S. units y/y", PCT),
    ("svc", "U.S. service revenue ($m)", USDM),
    ("vrev", "U.S. vehicle sales ($m)", USDM),
    ("vgp", "U.S. vehicle gross profit ($m)", USDM),
    ("fac", "U.S. facility operations ($m)", USDM),
    ("ga", "U.S. G&A ($m)", USDM),
    ("usoi", "U.S. operating income ($m)", USDM),
    ("usm", "U.S. operating margin", PCT),
    ("ioi", "International operating income ($m)", USDM),
    ("irev", "International revenue ($m)", USDM),
    ("cm", "Consolidated operating margin, ex-ACV", PCT),
    ("int_x", "Interest income, ex-ACV case ($m)", USDM),
    ("eps_x", "EPS ex-ACV (operating thesis)", USD),
    ("acv", "ACV pre-tax: operating income − amortization ($m)", USDM),
    ("int_g", "Interest income after ACV cash outflow ($m)", USDM),
    ("eps_g", "GAAP EPS incl. ACV", USD),
]
BLOCK = len(LINES) + 4
EPSX, EPSG, Q1X, QX_ROWS = {}, {}, {}, {}
for j in range(4):
    top = 4 + j * BLOCK
    wc = get_column_letter(2 + j)
    section(E, top, WN[j], 6)
    header(E, top + 1, ["Line", "Q1 Aug-Oct", "Q2 Nov-Jan", "Q3 Feb-Apr", "Q4 May-Jul", "FY27"])
    R = {key: top + 2 + k for k, (key, _, _) in enumerate(LINES)}
    for key, lab, f in LINES:
        E.cell(R[key], 1, lab).font = F_BOLD if key in ("eps_x", "eps_g") else F_BODY
        for c in range(1, 7):
            E.cell(R[key], c).border = ROW_LINE
    for q in range(4):
        c = get_column_letter(2 + q)
        s_ = lambda k: f"Scenarios!${wc}${P[k]}"
        g = lambda k: f"Inputs!{c}${SEG[k]}"
        cell = lambda k: f"{c}{R[k]}"
        F = {
            "loss": f"={s_('loss')}*(1-{g('lib')})",
            "ins": f"={s_('u')}+{cell('loss')}",
            "units": f"={NM['sins']}*{cell('ins')}+(1-{NM['sins']})*{NM['nonins']}",
            "svc": f"={g('us_service')}*(1+{cell('units')})*(1+{s_('rpu')})",
            "vrev": f"={g('us_vehicle')}*(1+{NM['goth']})",
            "vgp": f"=({g('us_vehicle')}-{g('us_cogs_vehicle')})*(1+{NM['goth']})",
            "fac": f"={g('us_facility')}*{NM['fix']}*(1+{s_('fixed')})+{g('us_facility')}*(1-{NM['fix']})*(1+{cell('units')})",
            "ga": f"={g('us_ga')}*(1+{NM['goth']})",
            "usoi": f"={cell('svc')}+{cell('vgp')}-{cell('fac')}-{cell('ga')}",
            "usm": f"={cell('usoi')}/({cell('svc')}+{cell('vrev')})",
            "ioi": f"={g('intl_oi')}*(1+{NM['gint']})",
            "irev": f"={g('intl_rev')}*(1+{NM['gint']})",
            "cm": f"=({cell('usoi')}+{cell('ioi')})/({cell('svc')}+{cell('vrev')}+{cell('irev')})",
            "int_x": f"={NM['intq1']}",
            "eps_x": f"=({cell('usoi')}+{cell('ioi')}+{cell('int_x')})*(1-{NM['tax']})/{NM['shares']}",
            "acv": "=0" if q == 0 else f"={s_('acv_op')}-{s_('acv_amort')}",
            "int_g": f"={NM['intq1']}" if q == 0 else f"={s_('int_q')}",
            "eps_g": f"=({cell('usoi')}+{cell('ioi')}+{cell('acv')}+{cell('int_g')})*(1-{NM['tax']})/{NM['shares']}",
        }
        for key, f, in F.items():
            fmt = next(x[2] for x in LINES if x[0] == key)
            put(E, cell(key), f, fmt, F_BOLD if key in ("eps_x", "eps_g") else F_BODY)
    for key in ("svc", "vrev", "fac", "ga", "usoi", "ioi", "irev", "int_x", "eps_x", "acv", "int_g", "eps_g"):
        fmt = next(x[2] for x in LINES if x[0] == key)
        put(E, f"F{R[key]}", f"=SUM(B{R[key]}:E{R[key]})", fmt, F_BOLD)
    put(E, f"F{R['usm']}", f"=F{R['usoi']}/(F{R['svc']}+F{R['vrev']})", PCT, F_BOLD)
    put(E, f"F{R['cm']}", f"=(F{R['usoi']}+F{R['ioi']})/(F{R['svc']}+F{R['vrev']}+F{R['irev']})", PCT, F_BOLD)
    EPSX[j], EPSG[j] = f"EPS_Build!$F${R['eps_x']}", f"EPS_Build!$F${R['eps_g']}"
    QX_ROWS[j] = R
E.freeze_panes = "B4"

# ================================================================== Valuation
V = wb.create_sheet("Valuation")
ws_setup(V, {"A": 58, "B": 19, "C": 19, "D": 19, "E": 19})
title(V, "Valuation: justified P/E by scenario → value per share at the Sep-27 horizon",
      "Scenario P/E is derived from growth, incremental ROIC and cost of equity rather than manually selected headline multiples. "
      "Two-stage: 5 years at g with payout (1 − g/ROIC), then a Gordon terminal; applied to FY28 ex-interest EPS; net cash added.")
V.merge_cells("A2:E2")
V["A2"].font = F_NOTE
V["A2"].alignment = Alignment(wrap_text=True, vertical="top")
section(V, 4, "Scenario valuation", 5)
header(V, 5, ["Line"] + WN)
VL = [("prob", "Probability", PCT), ("eps27g", "FY27 GAAP EPS incl. ACV ($/sh)", USD), ("eps27x", "FY27 EPS ex-ACV ($/sh)", USD),
      ("eps28", "FY28 EPS ($/sh)", USD), ("intps", "After-tax interest per share, FY28 ($/sh)", USD),
      ("eps28x", "FY28 ex-interest EPS ($/sh)", USD), ("g", "EPS growth, 5 years after FY28", PCT), ("roic", "Incremental ROIC", PCT),
      ("r", "Cost of equity (Inputs)", PCT2), ("gt", "Terminal growth (Inputs)", PCT),
      ("pv5", "PV of 5-year distributions per $1 of NTM EPS", NUM2), ("pvt", "PV of terminal value per $1 of NTM EPS", NUM2),
      ("jpe", "Justified ex-cash P/E", MULT), ("cash", "Net cash per share at horizon ($/sh)", USD),
      ("val", "Value per share, Sep-27 ($/sh)", USD), ("ret", "Stock return vs reference price", PCT),
      ("sret", "Short return", PCT), ("tpe", "Implied total P/E on FY28 EPS", MULT)]
VR = {k: 6 + i for i, (k, _, _) in enumerate(VL)}
for k, lab, _ in VL:
    V.cell(VR[k], 1, lab).font = F_BOLD if k in ("val", "ret", "sret", "jpe") else F_BODY
    for c in range(1, 6):
        V.cell(VR[k], c).border = ROW_LINE
for j in range(4):
    c = get_column_letter(2 + j)
    ref = lambda k: f"{c}{VR[k]}"
    g, ro, r_ = ref("g"), ref("roic"), ref("r")
    pv5 = "+".join(f"(1+{g})^{t - 1}*(1-{g}/{ro})/(1+{r_})^{t}" for t in range(1, 6))
    FV = {
        "prob": f"=Scenarios!{c}{P['prob']}", "eps27g": f"={EPSG[j]}", "eps27x": f"={EPSX[j]}",
        "eps28": f"={ref('eps27g')}*(1+Scenarios!{c}{P['g28']})",
        "intps": f"=Scenarios!{c}{P['int_q']}*4*(1-{NM['tax']})/{NM['shares']}",
        "eps28x": f"={ref('eps28')}-{ref('intps')}", "g": f"=Scenarios!{c}{P['g5']}", "roic": f"=Scenarios!{c}{P['roic']}",
        "r": f"={NM['coe']}", "gt": f"={NM['gT']}", "pv5": f"={pv5}",
        "pvt": f"=(1+{g})^5*(1-{ref('gt')}/{ro})/({r_}-{ref('gt')})/(1+{r_})^5",
        "jpe": f"={ref('pv5')}+{ref('pvt')}", "cash": f"={NM['cash1']}*1000/{NM['shares']}",
        "val": f"={ref('jpe')}*{ref('eps28x')}+{ref('cash')}", "ret": f"={ref('val')}/{NM['price']}-1",
        "sret": f"=-{ref('ret')}", "tpe": f"={ref('val')}/{ref('eps28')}",
    }
    for k, f in FV.items():
        fmt = next(x[2] for x in VL if x[0] == k)
        put(V, ref(k), f, fmt, link_font(f) if k not in ("val", "ret", "sret", "jpe") else F_BOLD, align="right")
r0 = 6 + len(VL) + 1
section(V, r0, "Probability-weighted result and downside", 5)
OUT = [
    ("pw", "Probability-weighted value ($/sh)", f"=SUMPRODUCT(B{VR['prob']}:E{VR['prob']},B{VR['val']}:E{VR['val']})", USD),
    ("pwret", "Probability-weighted stock return", f"=B{r0 + 1}/{NM['price']}-1", PCT),
    ("esr", "Expected short return", f"=-B{r0 + 2}", PCT),
    ("base", "Base-case (W2) value ($/sh)", f"=C{VR['val']}", USD),
    ("baseret", "Base-case (W2) stock return", f"=C{VR['ret']}", PCT),
    ("w4loss", "W4 adverse-case short loss (W4 stock return)", f"=E{VR['ret']}", PCT),
]
VO = {}
for i, (k, lab, f, fmt) in enumerate(OUT, start=1):
    V.cell(r0 + i, 1, lab).font = F_BOLD
    put(V, f"B{r0 + i}", f, fmt, F_BOLD, align="right")
    for c in range(1, 3):
        V.cell(r0 + i, c).border = ROW_LINE
    VO[k] = f"Valuation!$B${r0 + i}"
rs = r0 + len(OUT) + 2
section(V, rs, "Rate-cut stress: W3 economics with the 10-year yield at 3.5% (more severe than W4)", 5)
gS, roS, rS = f"C{rs + 2}", f"C{rs + 3}", f"C{rs + 4}"
STRESS = [("W3 FY28 ex-interest EPS ($/sh)", f"=D{VR['eps28x']}", USD), ("EPS growth (W3)", f"=D{VR['g']}", PCT),
          ("Incremental ROIC (W3)", f"=D{VR['roic']}", PCT), ("Stress cost of equity (Inputs)", f"={NM['coe_stress']}", PCT2)]
for i, (lab, f, fmt) in enumerate(STRESS, start=1):
    V.cell(rs + i, 1, lab).font = F_BODY
    put(V, f"C{rs + i}", f, fmt, link_font(f), align="right")
pv5s = "+".join(f"(1+{gS})^{t - 1}*(1-{gS}/{roS})/(1+{rS})^{t}" for t in range(1, 6))
V.cell(rs + 5, 1, "Stress justified ex-cash P/E").font = F_BODY
put(V, f"C{rs + 5}", f"={pv5s}+(1+{gS})^5*(1-{NM['gT']}/{roS})/({rS}-{NM['gT']})/(1+{rS})^5", MULT, align="right")
V.cell(rs + 6, 1, "Stress value per share ($/sh)").font = F_BOLD
put(V, f"C{rs + 6}", f"=C{rs + 5}*C{rs + 1}+D{VR['cash']}", USD, F_BOLD, align="right")
V.cell(rs + 7, 1, "Rate-cut stress short loss (stock return)").font = F_BOLD
put(V, f"C{rs + 7}", f"=C{rs + 6}/{NM['price']}-1", PCT, F_BOLD, align="right")
VO["stress"] = f"Valuation!$C${rs + 7}"
VO["stressval"] = f"Valuation!$C${rs + 6}"
re_ = rs + 9
section(V, re_, "EPS-only check: today's market multiple held constant; only EPS changes", 5)
V.cell(re_ + 1, 1, "Market ex-cash, ex-interest NTM P/E on S&P Global FY27 $1.62").font = F_BODY
put(V, f"B{re_ + 1}", f"=({NM['price']}-{NM['cash0']}*1000/{NM['shares']})/(Consensus!C9-{NM['int26']}*0.6*(1-{NM['tax']})/{NM['shares']})",
    MULT, align="right")
V.cell(re_ + 2, 1, "Stock return, EPS-only").font = F_BODY
for j in range(4):
    c = get_column_letter(2 + j)
    put(V, f"{c}{re_ + 2}", f"=($B${re_ + 1}*{c}{VR['eps28x']}+{c}{VR['cash']})/{NM['price']}-1", PCT, align="right")
V.cell(re_ + 3, 1, "Expected short return, EPS-only (no multiple change)").font = F_BOLD
put(V, f"B{re_ + 3}", f"=-SUMPRODUCT(B{VR['prob']}:E{VR['prob']},B{re_ + 2}:E{re_ + 2})", PCT, F_BOLD, align="right")
VO["epsonly"] = f"Valuation!$B${re_ + 3}"
V.freeze_panes = "B6"

# ================================================================== Sensitivity
T = wb.create_sheet("Sensitivity")
ws_setup(T, {"A": 46, "B": 18, "C": 20, "D": 44})
title(T, "Sensitivity of the expected short return (live)", "Cost of equity is the dominant valuation sensitivity; it is shown in full so risk is not understated.")
section(T, 4, "Cost-of-equity shift (all four worlds revalued)", 4)
header(T, 5, ["Shift to cost of equity", "Cost of equity", "Expected short return"])
for k, shf in enumerate([-0.01, -0.005, 0.0, 0.005, 0.01]):
    rr = 6 + k
    put(T, f"A{rr}", shf, PCTS, F_IN)
    put(T, f"B{rr}", f"={NM['coe']}+A{rr}", PCT2, align="right")
    terms = []
    for j in range(4):
        c = get_column_letter(2 + j)
        g, ro, r_ = f"Valuation!{c}{VR['g']}", f"Valuation!{c}{VR['roic']}", f"$B{rr}"
        pv5 = "+".join(f"(1+{g})^{t - 1}*(1-{g}/{ro})/(1+{r_})^{t}" for t in range(1, 6))
        tv = f"(1+{g})^5*(1-{NM['gT']}/{ro})/({r_}-{NM['gT']})/(1+{r_})^5"
        terms.append(f"Valuation!{c}{VR['prob']}*((({pv5}+{tv})*Valuation!{c}{VR['eps28x']}+Valuation!{c}{VR['cash']})/{NM['price']}-1)")
    put(T, f"C{rr}", "=-(" + "+".join(terms) + ")", PCT, F_BOLD if shf == 0 else F_BODY, align="right")
    for c in range(1, 4):
        T.cell(rr, c).border = ROW_LINE
section(T, 12, "Probability shifts (scenario values unchanged)", 4)
header(T, 13, ["Probability set (W1 / W2 / W3 / W4)", "Expected short return", "", "Note"])
for k, (lab, ps, note) in enumerate([("Base 20 / 45 / 20 / 15", (0.20, 0.45, 0.20, 0.15), "Governing"),
                                     ("Bearish tilt 30 / 45 / 15 / 10", (0.30, 0.45, 0.15, 0.10), "More weight to loss broadening"),
                                     ("Bullish tilt 15 / 40 / 25 / 20", (0.15, 0.40, 0.25, 0.20), "More weight to recovery")]):
    rr = 14 + k
    put(T, f"A{rr}", lab)
    put(T, f"B{rr}", "=-(" + "+".join(f"{p}*Valuation!{get_column_letter(2 + j)}{VR['ret']}" for j, p in enumerate(ps)) + ")",
        PCT, align="right")
    put(T, f"D{rr}", note)
    for c in range(1, 5):
        T.cell(rr, c).border = ROW_LINE
section(T, 18, "Beta cross-check", 4)
put(T, "A19", "Beta 1.03 (Yahoo, secondary) instead of 0.90: cost of equity")
put(T, "B19", f"={NM['rf']}+1.03*{NM['erp']}", PCT2, align="right")
put(T, "D19", "Equivalent to a +65bp shift in the table above (short return rises)")
section(T, 21, "Downside reference (from Valuation)", 4)
put(T, "A22", "W4 adverse-case short loss")
put(T, "B22", f"={VO['w4loss']}", PCT, F_LINK, align="right")
put(T, "A23", "Rate-cut stress (10Y to 3.5%) short loss")
put(T, "B23", f"={VO['stress']}", PCT, F_LINK, align="right")

# ================================================================== Consensus
C = wb.create_sheet("Consensus")
ws_setup(C, {"A": 50, "B": 15, "C": 11, "D": 7, "E": 11, "F": 11, "G": 72})
title(C, "Consensus (secondary sources) and our estimates")
section(C, 3, "Published consensus — kept separate by provider", 7)
header(C, 4, ["Provider / period", "Date pulled", "EPS ($/sh)", "n", "Low", "High", "Basis / note"])
CONS = [
    ("Zacks: Q1 FY27 (Oct-26)", "10/1/26", 0.41, 4, 0.38, 0.43, "Via Nasdaq; quarterly consensus"),
    ("Zacks: Q2 FY27 (Jan-27)", "10/1/26", 0.37, 4, 0.36, 0.39, ""),
    ("Zacks: Q3 FY27 (Apr-27)", "10/1/26", 0.45, 4, 0.43, 0.47, ""),
    ("Zacks: Q4 FY27 (Jul-27)", "10/1/26", 0.41, 4, 0.38, 0.44, ""),
    ("S&P Global MI via StockAnalysis: FY27 (Jul-27)", "updated 9/25/26", 1.62, 9, 1.56, 1.67,
     "Pre-close consensus; public aggregate does not disclose exact ACV accounting treatment. We compare our ex-ACV estimate to isolate the operating thesis."),
    ("Zacks: FY27 (Jul-27)", "10/1/26", 1.65, 5, 1.57, 1.70, ""),
    ("Zacks: FY28 (Jul-28)", "10/1/26", 1.81, 5, 1.72, 1.88, ""),
    ("Yahoo Finance: FY27 (staleness cross-check only; not used)", "10/1/26", 1.75, 8, 1.62, 1.83,
     "Not used to govern the pitch: includes pre-print estimates (30 days earlier $1.85); its quarterly row was a stale Q4-FY26 estimate."),
]
for i, row_ in enumerate(CONS, start=5):
    for k, v in enumerate(row_):
        cell = C.cell(i, 1 + k, v)
        cell.font = F_IN if isinstance(v, (int, float)) else F_BODY
        if k in (2, 4, 5):
            cell.number_format = USD
        if k == 6:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        for cc in range(1, 8):
            C.cell(i, cc).border = ROW_LINE
section(C, 14, "Our estimates vs consensus (base world W2)", 7)
header(C, 15, ["Comparison", "Ours ($/sh)", "Consensus", "Gap", "", "", "Note"])
R2 = QX_ROWS[1]
GAPS = [
    ("Q1 FY27 EPS vs Zacks", f"=EPS_Build!B{R2['eps_x']}", "=C5", "Q1 has no ACV P&L (close expected mid-Oct)"),
    ("Q2 FY27 EPS ex-ACV vs Zacks", f"=EPS_Build!C{R2['eps_x']}", "=C6", ""),
    ("FY27 EPS ex-ACV vs S&P Global", f"={EPSX[1]}", "=C9", "Operating thesis comparison"),
    ("FY27 EPS ex-ACV vs Zacks", f"={EPSX[1]}", "=C10", ""),
    ("FY27 GAAP EPS incl. modeled ACV vs S&P Global", f"={EPSG[1]}", "=C9", "Team ACV estimate: GAAP incl. amortization & forgone interest; company guides EPS-neutral in first full year"),
    ("FY28 EPS vs Zacks", f"=Valuation!C{VR['eps28']}", "=C11", ""),
]
for i, (lab, ours, cons, note) in enumerate(GAPS, start=16):
    put(C, f"A{i}", lab)
    put(C, f"B{i}", ours, USD, link_font(ours), align="right")
    put(C, f"C{i}", cons, USD, align="right")
    put(C, f"D{i}", f"=B{i}/C{i}-1", PCT, F_BOLD, align="right")
    put(C, f"G{i}", note, wrap=True)
    for cc in range(1, 8):
        C.cell(i, cc).border = ROW_LINE
C.freeze_panes = "A5"

# ================================================================== Catalysts
K = wb.create_sheet("Catalysts")
ws_setup(K, {"A": 24, "B": 30, "C": 64, "D": 26, "E": 32})
title(K, "Catalyst path and falsification")
section(K, 3, "Catalysts (3-12 month horizon; planned exit after Q2 FY27)", 5)
header(K, 4, ["Date", "Event", "What investors learn", "Supports", "Source"])
CAT = [
    ("Oct 7, 2026", "ACV tender offer expiry (extended)", "Whether a majority tenders (47.8% at 9/30); timing of ACV consolidation",
     "Neutral / secondary", "Schedule TO-T/A filed 10/1/26 (SEC)"),
    ("Oct 13, 2026", "HSR waiting period expiry (refiled 9/28)", "Whether antitrust review extends (Second Request)",
     "Neutral / secondary", "Schedule TO-T/A filed 9/29/26 (SEC)"),
    ("Early Nov 2026 (estimated)", "RB Global Q3-26", "First full-quarter read-through on IAA automotive units after its partner expansion",
     "Short if IAA units strong", "RB Global Q2-26 call (transcript)"),
    ("Mid-Nov 2026 (estimated)", "CPRT Q1 FY27 results",
     "First full quarter reflecting the lost-customer volume impact; key read-throughs are U.S. insurance units, OpEx/car and U.S. operating margin.",
     "Primary discovery event", "Team estimate of timing"),
    ("Mid-Feb 2027 (estimated)", "CPRT Q2 FY27 results",
     "Second full quarter of lost volume plus initial ACV GAAP contribution if the transaction closes on schedule. Planned exit.",
     "Short; planned exit", "Team estimate of timing"),
]
for i, row_ in enumerate(CAT, start=5):
    for k, v in enumerate(row_):
        put(K, f"{get_column_letter(1 + k)}{i}", v, wrap=True)
    for cc in range(1, 6):
        K.cell(i, cc).border = ROW_LINE
    K.row_dimensions[i].height = 38
section(K, 11, "Falsification thresholds (Q1 FY27) - exit and reassess if any is met", 5)
header(K, 12, ["KPI", "Threshold", "Our base (W2, Q1)", "", "Basis"])
FALS = [("U.S. insurance units y/y", -0.06, f"=EPS_Build!B{R2['ins']}", "Better than −6% means the lost volume is being offset"),
        ("Consolidated operating margin, ex-ACV", 0.36, f"=EPS_Build!B{R2['cm']}", "≥36% means cost absorption is not happening (yr-ago Q1 37%)"),
        ("OpEx per car growth y/y", 0.03, None, "≤ +3% means fast cost cuts (Q4-FY26 +12.7%)")]
for i, (lab, thr, base, basis) in enumerate(FALS, start=13):
    put(K, f"A{i}", lab)
    put(K, f"B{i}", thr, PCT, F_IN, align="right")
    if base:
        put(K, f"C{i}", base, PCT, F_LINK, align="right")
    put(K, f"E{i}", basis, wrap=True)
    for cc in range(1, 6):
        K.cell(i, cc).border = ROW_LINE

# ================================================================== Sources
Z = wb.create_sheet("Sources")
ws_setup(Z, {"A": 5, "B": 40, "C": 34, "D": 44, "E": 20, "F": 14, "G": 50})
title(Z, "Sources: audit ledger", "Source types: Primary | Secondary consensus | Secondary transcript | Secondary market data | Team estimate")
header(Z, 4, ["No.", "Datapoint", "Value", "Source", "Source type", "Date", "Notes"])
SRC = [
    ("FY26 revenue, segment P&L, Q4 derivation", "Revenue $4.67bn; U.S. service $3,388m", "Copart FY26 Form 10-K, segment note", "Primary", "9/29/26", "Q4 = FY less Q1-Q3 10-Qs"),
    ("FY26 quarterly segment data (Q1-Q3)", "See Inputs", "Copart Form 10-Q filings, Q1-Q3 FY26", "Primary", "11/24/25; 3/3/26; 5/29/26", ""),
    ("Diluted shares", "942.8m (Q3 FY26)", "Copart Q3 FY26 Form 10-Q (XBRL)", "Primary", "5/29/26", "Model uses 940m"),
    ("Effective tax rate", "19.3%", "Copart FY26 Form 10-K", "Primary", "9/29/26", "Model uses 19.5%"),
    ("Cash, equivalents, restricted cash + HTM securities", "$1,907.9m + $2,581.9m = $4.49bn", "Copart FY26 Form 10-K, balance sheet / cash flow", "Primary", "9/29/26", ""),
    ("Operating cash flow; capex", "$1,604.5m; $337.4m", "Copart FY26 Form 10-K, cash flow statement", "Primary", "9/29/26", "FY26 FCF $1.27bn"),
    ("Interest income FY26", "$181.9m", "Copart FY26 Form 10-K, segment note", "Primary", "9/29/26", ""),
    ("Q4 FY26 revenue / diluted EPS", "$1.152bn / $0.35", "Copart Form 8-K Ex. 99.1 (earnings release)", "Primary", "9/10/26", ""),
    ("Q4 U.S. insurance units; ex-one-customer growth", "−7.5%; +2.3%", "Copart Q4 FY26 earnings call", "Secondary transcript", "9/10/26", "Third-party transcription of company call"),
    ("OpEx per car; total-loss frequency", "+12.7%; 23.3%", "Copart Q4 FY26 earnings call", "Secondary transcript", "9/10/26", ""),
    ("RB Global partner expansion", "All 50 states; volume transitioned over prior 90 days", "RB Global Q2-26 earnings call", "Secondary transcript", "8/4/26", "Carrier identity not disclosed; not used in formulas"),
    ("ACV transaction", "$10.50/sh cash; ~$1.9bn equity value", "Copart Form 8-K Ex. 99.1 (deal release); Schedule TO-T", "Primary", "9/10/26; 9/17/26", ""),
    ("ACV EPS guidance (company)", "Neutral on EPS in first full year; accretive FY28 and beyond; near-term cost and revenue synergies expected", "Copart Form 8-K Ex. 99.1 / 99.2", "Primary", "9/10/26", "Model's GAAP dilution is a team estimate (amortization, forgone interest)"),
    ("ACV tender status", "47.78% tendered; expiry extended to 10/7/26", "Schedule TO-T/A", "Primary", "10/1/26", ""),
    ("HSR status", "Refiled 9/28; waiting period expected to expire 10/13/26", "Schedule TO-T/A", "Primary", "9/29/26", ""),
    ("ACV TTM financials", "Revenue $801m; operating loss −$57m", "ACV Auctions Forms 10-Q / 10-K (XBRL)", "Primary", "through Q2-26", ""),
    ("10-year Treasury yield", "5.24%", "U.S. Treasury Daily Par Yield Curve Rates", "Primary", "10/1/26", ""),
    ("Manheim Used Vehicle Value Index", "−0.4% y/y, mid-September", "Cox Automotive (via press summary)", "Secondary market data", "Sep 2026", "Qualitative support only; not in formulas"),
    ("Consensus EPS (quarterly, FY27, FY28)", "See Consensus sheet", "Zacks via Nasdaq", "Secondary consensus", "10/1/26", ""),
    ("Share price", "$27.29", "Yahoo Finance daily close", "Secondary market data", "10/1/26", ""),
    ("Shares outstanding", "~926m", "S&P Global MI via StockAnalysis", "Secondary consensus", "10/1/26", "Cross-check only"),
    ("Consensus EPS FY27", "$1.62 (n=9)", "S&P Global Market Intelligence via StockAnalysis", "Secondary consensus", "updated 9/25/26", "Exact ACV treatment not disclosed"),
    ("Consensus EPS FY27 (cross-check)", "$1.75 (n=8)", "Yahoo Finance", "Secondary consensus", "10/1/26", "Staleness cross-check only; not used"),
    ("Sell-side commentary", "Loss 'temporary'; further near-term declines", "HSBC note as reported by Investing.com", "Secondary consensus", "9/17/26", "Context only; not in formulas"),
    ("Scenario drivers, probabilities, ROIC, growth", "See Scenarios", "Team model", "Team estimate", "10/1/26", ""),
    ("U.S. insurance share 76%; fixed cost share 55%; non-ins +3%; G&A/vehicle +5%; intl +10%", "See Inputs", "Team model (basis on Inputs)", "Team estimate", "10/1/26", ""),
    ("Beta 0.90; ERP 5%; terminal growth 3%; horizon cash $3.5bn", "See Inputs", "Team model (basis on Inputs)", "Team estimate", "10/1/26", ""),
    ("Post-miss event study", "+4.6% to +6.9% 3M excess after large misses", "Team backtest (point-in-time)", "Team estimate", "10/1/26", "Basis for the planned exit after Q2"),
]
for i, row_ in enumerate(SRC, start=5):
    put(Z, f"A{i}", i - 4)
    for k, v in enumerate(row_):
        put(Z, f"{get_column_letter(2 + k)}{i}", v, wrap=True)
    for cc in range(1, 8):
        Z.cell(i, cc).border = ROW_LINE
Z.freeze_panes = "A5"

# ================================================================== Checks
X = wb.create_sheet("Checks")
ws_setup(X, {"A": 56, "B": 12, "C": 12, "D": 12, "E": 12, "F": 12})
title(X, "Model checks")
section(X, 3, "Calibration: zero-growth replay of FY26 vs reported diluted EPS", 6)
header(X, 4, ["Quarter", "Q1", "Q2", "Q3", "Q4", "FY26"])
put(X, "A5", "Model replay ($/sh)")
put(X, "A6", "Reported ($/sh)")
put(X, "A7", "Difference ($/sh)")
for q in range(4):
    c = get_column_letter(2 + q)
    g = lambda k: f"Inputs!{c}${SEG[k]}"
    us = f"({g('us_service')}+{g('us_vehicle')}-{g('us_cogs_vehicle')}-{g('us_facility')}-{g('us_ga')})"
    put(X, f"{c}5", f"=({us}+{g('intl_oi')}+{g('interest')})*(1-{NM['tax']})/{NM['shares']}", USD, align="right")
    put(X, f"{c}6", f"=Inputs!{c}${SEG['eps26']}", USD, F_LINK, align="right")
    put(X, f"{c}7", f"={c}5-{c}6", USD, align="right")
for rr in (5, 6, 7):
    put(X, f"F{rr}", f"=SUM(B{rr}:E{rr})", USD, F_BOLD, align="right")
put(X, "A8", "Unmodeled other income / FX and non-controlling interest explain the small difference.", font=F_NOTE)
section(X, 10, "Integrity", 6)
put(X, "A11", "Scenario probabilities sum to 100%")
put(X, "B11", f'=IF(ABS(Scenarios!B{P["probcheck"]}-1)<0.0001,"OK","CHECK")', align="right")
put(X, "A12", "Cost of equity exceeds terminal growth (valuation defined)")
put(X, "B12", f'=IF({NM["coe_stress"]}>{NM["gT"]},"OK","CHECK")', align="right")

# ================================================================== Summary (first)
M = wb.create_sheet("Summary", 0)
ws_setup(M, {"A": 46, "B": 13, "C": 13, "D": 17, "E": 13, "F": 13, "G": 13, "H": 13, "I": 3})
put(M, "A1", "Copart (NASDAQ: CPRT) — SHORT", font=F_TITLE)
put(M, "A2", "Margin Callers", font=Font(name=FN, size=10, bold=True, color=NAVY))
put(M, "A3", "Horizon: Q1 FY27 through Q2 FY27 / planned exit after Q2", font=F_BODY)
section(M, 5, "Thesis", 8)
M.merge_cells("A6:H7")
put(M, "A6", "The Street knows Copart lost a large insurance customer. Our disagreement is the magnitude and timing of the FY27 "
             "earnings impact: we model Q1 FY27 EPS of ~$0.36 and FY27 EPS of ~$1.43 ex-ACV versus ~$0.41 and ~$1.62-$1.65 "
             "published consensus.", wrap=True)
M.row_dimensions[6].height = 22
M.row_dimensions[7].height = 22
section(M, 9, "Return profile", 8)
KP = [("Reference price (10/1/26)", f"={NM['price']}", USD),
      ("Base-case value (W2)", f"={VO['base']}", USD),
      ("Probability-weighted value", f"={VO['pw']}", USD),
      ("Expected short return", f"={VO['esr']}", PCT),
      ("Expected short return, EPS-only (no multiple change)", f"={VO['epsonly']}", PCT),
      ("W4 adverse-case short loss", f"={VO['w4loss']}", PCT),
      ("Rate-cut stress (10Y to 3.5%): short loss", f"={VO['stress']}", PCT)]
for i, (lab, f, fmt) in enumerate(KP, start=10):
    put(M, f"A{i}", lab, font=F_BOLD if "Expected short return" == lab else F_BODY)
    put(M, f"B{i}", f, fmt, F_LINKB if lab == "Expected short return" else F_LINK, align="right")
    for c in range(1, 3):
        M.cell(i, c).border = ROW_LINE
put(M, "D10", "EPS: ours vs consensus", font=F_HDR)
for c, lab in zip("DEFG", ["Period (ex-ACV)", "Ours", "Consensus", "Gap"]):
    put(M, f"{c}11", lab, font=F_HDR, border=HDR_LINE, align="left" if c == "D" else "right")
EPSROWS = [("Q1 FY27 vs Zacks", "Consensus!B16", "Consensus!C16", "Consensus!D16"),
           ("FY27 vs S&P Global", "Consensus!B18", "Consensus!C18", "Consensus!D18"),
           ("FY27 vs Zacks", "Consensus!B19", "Consensus!C19", "Consensus!D19")]
for i, (lab, a, b, d) in enumerate(EPSROWS, start=12):
    put(M, f"D{i}", lab)
    put(M, f"E{i}", f"={a}", USD, F_LINK, align="right")
    put(M, f"F{i}", f"={b}", USD, F_LINK, align="right")
    put(M, f"G{i}", f"={d}", PCT, F_LINK, align="right")
    for c in "DEFG":
        M[f"{c}{i}"].border = ROW_LINE
section(M, 18, "Scenarios (Valuation sheet)", 8)
for c, lab in zip("ABCDEFGH", ["World", "Probability", "FY27 EPS ex-ACV", "FY27 GAAP EPS", "FY28 EPS", "Justified P/E", "Value ($/sh)", "Short return"]):
    put(M, f"{c}19", lab, font=F_HDR, border=HDR_LINE, align="left" if c == "A" else "right")
for j in range(4):
    rr = 20 + j
    vc = get_column_letter(2 + j)
    put(M, f"A{rr}", WN[j])
    for c, key, fmt in zip("BCDEFGH", ["prob", "eps27x", "eps27g", "eps28", "jpe", "val", "sret"], [PCT, USD, USD, USD, MULT, USD, PCT]):
        put(M, f"{c}{rr}", f"=Valuation!{vc}{VR[key]}", fmt, F_LINK, align="right")
    for c in "ABCDEFGH":
        M[f"{c}{rr}"].border = ROW_LINE
put(M, "A24", "Probability-weighted", font=F_BOLD)
put(M, "G24", f"={VO['pw']}", USD, F_LINKB, align="right")
put(M, "H24", f"={VO['esr']}", PCT, F_LINKB, align="right")
put(M, "A25", "Scenario P/E is derived from growth, incremental ROIC and cost of equity rather than manually selected headline multiples.", font=F_NOTE)
section(M, 27, "Catalysts and falsification", 8)
CF = [("Mid-Nov 2026 (estimated)", "Q1 FY27: first full quarter reflecting the lost-customer volume impact (U.S. insurance units, OpEx/car, U.S. operating margin)."),
      ("Mid-Feb 2027 (estimated)", "Q2 FY27: second full quarter of lost volume plus initial ACV GAAP contribution if the deal closes on schedule. Planned exit."),
      ("Falsification (Q1 FY27)", "Exit if U.S. insurance units are better than −6% y/y, consolidated operating margin ≥36%, or OpEx/car growth ≤ +3% (Catalysts sheet).")]
for i, (a, b) in enumerate(CF, start=28):
    put(M, f"A{i}", a, font=F_BOLD)
    M.merge_cells(f"B{i}:H{i}")
    put(M, f"B{i}", b, wrap=True)
    M.row_dimensions[i].height = 24
    for c in "ABCDEFGH":
        M[f"{c}{i}"].border = Border(left=BOX if c == "A" else None, right=BOX if c == "H" else None,
                                    top=BOX if i == 28 else None, bottom=BOX if i == 30 else None)
put(M, "A32", "Colour key: blue = input; black = formula; green = link to another sheet; red = negative.", font=F_NOTE)

# ------------------------------------------------------------------ Summary charts (data linked; placed right of tables)
from math import ceil

from openpyxl.worksheet.views import Selection

from openpyxl.chart.axis import ChartLines
from openpyxl.chart.marker import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.text import RichText
from openpyxl.chart.title import Title
from openpyxl.chart.text import Text
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.text import CharacterProperties, Font as DFont, Paragraph, ParagraphProperties, RegularTextRun

put(M, "A34", "Chart data: FY27 quarterly EPS ($/sh), linked to Consensus and EPS_Build", font=F_SEC)
for c in range(1, 4):
    M.cell(34, c).border = SEC_LINE
for c, lab in zip("ABC", ["Quarter", "Zacks consensus", "Our ex-ACV estimate"]):
    put(M, f"{c}35", lab, font=F_HDR, border=HDR_LINE, align="left" if c == "A" else "right")
for q in range(4):
    rr = 36 + q
    put(M, f"A{rr}", ["Q1", "Q2", "Q3", "Q4"][q], border=ROW_LINE)
    put(M, f"B{rr}", f"=Consensus!C{5 + q}", USD, F_LINK, align="right", border=ROW_LINE)
    put(M, f"C{rr}", f"=EPS_Build!{get_column_letter(2 + q)}{R2['eps_x']}", USD, F_LINK, align="right", border=ROW_LINE)


def _rich(size=800, bold=False, color="000000"):
    cp = CharacterProperties(latin=DFont(typeface=FN), sz=size, b=bold, solidFill=color)
    return RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), endParaRPr=cp)])


def _title(text, size=1000):
    cp = CharacterProperties(latin=DFont(typeface=FN), sz=size, b=True, solidFill=NAVY)
    t = Title(tx=Text(rich=RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), r=[RegularTextRun(rPr=cp, t=text)])])))
    t.overlay = False
    return t


def _clean(ch):
    ch.roundedCorners = False
    ch.graphical_properties = GraphicalProperties(solidFill="FFFFFF", ln=LineProperties(solidFill="D9D9D9", w=6350))
    ch.plot_area.graphicalProperties = GraphicalProperties(noFill=True, ln=LineProperties(noFill=True))
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.x_axis.txPr = _rich()
    ch.y_axis.txPr = _rich()
    ch.x_axis.majorGridlines = None
    ch.x_axis.graphicalProperties = GraphicalProperties(ln=LineProperties(solidFill="808080", w=6350))
    ch.y_axis.graphicalProperties = GraphicalProperties(ln=LineProperties(noFill=True))


# Chart 1: clustered columns, consensus (navy) vs ours (dark red); light horizontal gridlines only
ch1 = BarChart()
ch1.type = "col"
ch1.grouping = "clustered"
ch1.title = _title("FY27 Quarterly EPS: Consensus vs Margin Callers")
ch1.add_data(Reference(M, min_col=2, max_col=3, min_row=35, max_row=39), titles_from_data=True)
ch1.set_categories(Reference(M, min_col=1, min_row=36, max_row=39))
_clean(ch1)
ch1.y_axis.numFmt = "$0.00"
ch1.y_axis.scaling.min = 0
ch1.y_axis.scaling.max = 0.5
ch1.y_axis.majorUnit = 0.1
ch1.y_axis.majorGridlines = ChartLines(spPr=GraphicalProperties(ln=LineProperties(solidFill="E3E3E3", w=6350)))
ch1.series[0].graphicalProperties = GraphicalProperties(solidFill="17365D", ln=LineProperties(noFill=True))
ch1.series[1].graphicalProperties = GraphicalProperties(solidFill="9B2C2C", ln=LineProperties(noFill=True))
ch1.gapWidth = 80
ch1.legend.position = "b"
ch1.legend.overlay = False
ch1.legend.txPr = _rich()
ch1.height, ch1.width = 7.4, 15.0
M.add_chart(ch1, "J5")

# Chart 2: horizontal bars of scenario value (single series; W1/W2 navy, W3/W4 gray); labels at bar ends
ch2 = BarChart()
ch2.type = "bar"
ch2.grouping = "clustered"
ch2.title = _title("Scenario Value per Share")
ch2.add_data(Reference(M, min_col=7, min_row=20, max_row=23), titles_from_data=False)
ch2.set_categories(Reference(M, min_col=1, min_row=20, max_row=23))
_clean(ch2)
ch2.legend = None
ch2.x_axis.scaling.orientation = "maxMin"          # W1 at top
ch2.y_axis.crosses = "max"                          # value axis at bottom when categories are reversed
ch2.y_axis.scaling.min = 0
ch2.y_axis.scaling.max = 35
ch2.y_axis.majorUnit = 5
ch2.y_axis.numFmt = "$0"
ch2.y_axis.majorGridlines = None
ch2.y_axis.title = _title("Value per share ($); current price $27.29", size=800)
s2 = ch2.series[0]
s2.graphicalProperties = GraphicalProperties(solidFill="17365D", ln=LineProperties(noFill=True))
for idx, col in enumerate(["17365D", "17365D", "8C96A5", "8C96A5"]):
    pt = DataPoint(idx=idx)
    pt.graphicalProperties = GraphicalProperties(solidFill=col, ln=LineProperties(noFill=True))
    s2.dPt.append(pt)
s2.dLbls = DataLabelList()
s2.dLbls.showVal = True
s2.dLbls.showSerName = s2.dLbls.showCatName = s2.dLbls.showLegendKey = s2.dLbls.showPercent = False
s2.dLbls.position = "outEnd"
s2.dLbls.numFmt = "$0.00"
s2.dLbls.txPr = _rich(size=800, bold=True)
ch2.gapWidth = 60
ch2.height, ch2.width = 7.4, 15.0
M.add_chart(ch2, "J21")
M.column_dimensions["I"].width = 3

# ================================================================== global visual pass (styling only)
THIN_ROW = Border(bottom=Side(style="thin", color="D9D9D9"))
FREEZE = {"Summary": None, "Inputs": "A6", "Scenarios": None, "EPS_Build": "A4", "Valuation": "A5", "Sensitivity": None,
          "Consensus": None, "Catalysts": None, "Sources": "A4", "Checks": None}
CENTER_COLS = {"Inputs": {"C"}}
TOP_CELLS = {("Valuation", "A2"), ("EPS_Build", "A2")}
RIGHT_TEXT_COLS = {"Consensus": {"B"}, "Sources": {"F"}}


def _width(ws, col_letter):
    return ws.column_dimensions[col_letter].width or 8.43


def _is_hdr(c):
    b = c.border.bottom
    return c.value is not None and c.font.b and b is not None and b.style == "thin" and b.color is not None and str(b.color.rgb).endswith("17365D")


# pre-pass: wrap long notes / labels so nothing is clipped (no cell moves)
E.merge_cells("A2:F2")
E["A2"].alignment = Alignment(wrap_text=True, vertical="top")
I.column_dimensions["E"].width = 64
I.column_dimensions["C"].width = 10
for rr in range(6, I.max_row + 1):
    if isinstance(I.cell(rr, 5).value, str):
        I.cell(rr, 5).alignment = Alignment(horizontal="left", wrap_text=True)
for rr in range(5, T.max_row + 1):
    if isinstance(T.cell(rr, 4).value, str):
        T.cell(rr, 4).alignment = Alignment(horizontal="left", wrap_text=True)
for rr in range(13, K.max_row + 1):
    if isinstance(K.cell(rr, 1).value, str):
        K.cell(rr, 1).alignment = Alignment(horizontal="left", wrap_text=True)
# Valuation key output rows: bold with top and bottom rules (no fill)
KEY_RULE = Side(style="thin", color="8C96A5")
for rr in range(6, V.max_row + 1):
    if V.cell(rr, 1).font.b and V.cell(rr, 1).value and V.cell(rr, 1).border.bottom.color is not None             and V.cell(rr, 1).border.bottom.style != "medium":
        for cc in range(1, 6):
            if V.cell(rr, cc).value is not None or cc == 1:
                V.cell(rr, cc).border = Border(top=KEY_RULE, bottom=KEY_RULE)
# Checks: thin gray rules on header, replay, reported, difference and integrity rows
for rr in (5, 6, 7, 11, 12):
    for cc in range(1, 7):
        X.cell(rr, cc).border = Border(bottom=Side(style="thin", color="D9D9D9"))

for ws in wb.worksheets:
    # replace hair rules with thin light-gray rules (borders only; never fills)
    for row in ws.iter_rows():
        for c in row:
            b = c.border
            if b is not None and b.bottom is not None and b.bottom.style == "hair":
                c.border = Border(left=b.left, right=b.right, top=b.top, bottom=Side(style="thin", color="D9D9D9"))
            # alignment: numbers / formulas right, text left (keep explicit centre / wrap)
            if c.value is None:
                continue
            al = c.alignment
            col = c.column_letter
            is_num = isinstance(c.value, (int, float)) or (isinstance(c.value, str) and c.value.startswith("="))
            if col in CENTER_COLS.get(ws.title, set()) and c.row > 5 and not is_num and len(str(c.value)) <= 8:
                horiz = "center"
            elif col in RIGHT_TEXT_COLS.get(ws.title, set()) and c.row > 4:
                horiz = "right"
            elif al.horizontal in ("center", "right") and not is_num:
                horiz = al.horizontal
            else:
                horiz = "right" if is_num else "left"
            vert = "top" if (ws.title, c.coordinate) in TOP_CELLS else ("bottom" if _is_hdr(c) else "center")
            c.alignment = Alignment(horizontal=horiz, vertical=vert, wrap_text=al.wrap_text)
    # row heights: fit wrapped text (Arial 9 ≈ 1.15 characters per width unit, 12pt per line)
    merged = {}
    for rng in ws.merged_cells.ranges:
        w = sum(_width(ws, get_column_letter(cc)) for cc in range(rng.min_col, rng.max_col + 1))
        merged[(rng.min_row, rng.min_col)] = (w, rng.max_row - rng.min_row + 1)
    for r in range(1, ws.max_row + 1):
        lines_needed = 1
        for cc in range(1, ws.max_column + 1):
            cell = ws.cell(r, cc)
            if isinstance(cell.value, str) and cell.alignment.wrap_text and not cell.value.startswith("="):
                w, nrows = merged.get((r, cc), (_width(ws, get_column_letter(cc)), 1))
                lines_needed = max(lines_needed, ceil(ceil(len(cell.value) / (w * 1.3)) / nrows))
        if lines_needed > 1:
            ws.row_dimensions[r].height = 12.5 * lines_needed + 3
        elif ws.row_dimensions[r].height and ws.row_dimensions[r].height > 16 and r > 3:
            ws.row_dimensions[r].height = None
    # panes: top-row freezes only; no split panes, no frozen columns
    ws.sheet_view.pane = None
    ws.sheet_view.selection = [Selection(activeCell="A1", sqref="A1")]
    ws.freeze_panes = FREEZE[ws.title]
    if FREEZE[ws.title]:
        ws.sheet_view.selection = [Selection(pane="bottomLeft", activeCell=FREEZE[ws.title], sqref=FREEZE[ws.title])]
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 100
    # print area = used model area only
    last_col = "H" if ws.title == "Summary" else get_column_letter(ws.max_column)
    ws.print_area = f"A1:{last_col}{ws.max_row}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

# headers sit over their data: alignment copied from the first populated cell below
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if not _is_hdr(c) or (ws.title == "Summary" and c.row == 35):
                continue
            for rr in range(c.row + 1, min(c.row + 4, ws.max_row + 1)):
                below = ws.cell(rr, c.column)
                if below.value is not None:
                    c.alignment = Alignment(horizontal=below.alignment.horizontal, vertical="bottom", wrap_text=c.alignment.wrap_text)
                    break
# Scenarios narrative row: row label, top-aligned text, closing rule
NR = P["probcheck"] + 3
S.cell(NR, 1, "What each world assumes (evidence)").font = F_BODY
for cc in range(1, 6):
    cl = S.cell(NR, cc)
    cl.alignment = Alignment(horizontal="left", vertical="top", wrap_text=cc > 1)
    cl.border = Border(bottom=Side(style="thin", color="D9D9D9"))
S.row_dimensions[NR].height = 66

# light horizontal rule under every table row that has none (rows with a label and at least one value)
def _bottom(c):
    b = c.border.bottom
    return b is not None and b.style is not None
for ws in wb.worksheets:
    if ws.title == "Summary":
        continue
    ext = ws.max_column
    for r in range(4, ws.max_row + 1):
        a1 = ws.cell(r, 1)
        if a1.value is None or _bottom(a1) or a1.font.i or (a1.font.sz or 9) > 10:
            continue
        if not any(ws.cell(r, cc).value is not None for cc in range(2, ext + 1)):
            continue
        for cc in range(1, ext + 1):
            cl = ws.cell(r, cc)
            if not _bottom(cl):
                b = cl.border
                cl.border = Border(left=b.left, right=b.right, top=b.top, bottom=Side(style="thin", color="D9D9D9"))

# Summary: two-line headers where labels are longer than the numeric columns; catalyst labels top-aligned
for rr in (19, 35):
    M.row_dimensions[rr].height = 25
    for cc in range(1, 9):
        cl = M.cell(rr, cc)
        if cl.value is not None:
            cl.alignment = Alignment(horizontal=cl.alignment.horizontal, vertical="bottom", wrap_text=True)
for rr in (28, 29, 30):
    M.cell(rr, 1).alignment = Alignment(horizontal="left", vertical="top")
    M.cell(rr, 2).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
# Checks: FY26 total column bold with a left rule
for rr in range(4, 8):
    b = X.cell(rr, 6).border
    X.cell(rr, 6).border = Border(left=Side(style="thin", color="8C96A5"), top=b.top, bottom=b.bottom)
    if X.cell(rr, 6).value is not None:
        X.cell(rr, 6).font = Font(name=FN, size=9, bold=True, color=X.cell(rr, 6).font.color)
# Summary print area includes the charts (J:R)
M.print_area = f"A1:R{M.max_row}"
wb.active = 0

out = ROOT / "final" / "Margin_Callers.xlsx"
wb.save(out)
print("saved", out)
