# ================================================================== Inputs
I = wb.active
I.title = "Inputs"
ws_setup(I, {"A": 60, "B": 11, "C": 8, "D": 20, "E": 92})
title(I, "Inputs", "Blue = hard-coded input; black = formula; green = link. Every input carries a source type; links and SEC accession numbers are on the Sources sheet.")
NM = {}


def inp_rows(row, items):
    for key, lab, v, f, u, st, src in items:
        is_f = isinstance(v, str) and v.startswith("=")
        I.cell(row, 1, lab).font = F_BOLD if key in ("coe", "obs") else F_BODY
        put(I, f"B{row}", v, f, (F_BOLD if key in ("coe", "obs") else link_font(v)) if is_f else F_IN)
        put(I, f"C{row}", u, align="center")
        put(I, f"D{row}", st)
        put(I, f"E{row}", src, wrap=True)
        if not is_f:
            I[f"B{row}"].comment = Comment(f"{st}: {src}", "Margin Callers")
        for c in range(1, 6):
            I.cell(row, c).border = ROW_LINE
        NM[key] = f"Inputs!$B${row}"
        row += 1
    return row


def inp_section(row, text):
    section(I, row, text, 5)
    header(I, row + 1, ["Input", "Value", "Units", "Source type", "Source / basis"])
    return row + 2


row = inp_section(4, "Market, capital structure and tax")
row = inp_rows(row, [
    ("price", "Share price (10/1/26 close)", 27.29, USD, "$/sh", "Secondary market data", "Yahoo Finance daily close, 10/1/26"),
    ("shares", "Diluted shares, FY27 (no net buybacks assumed)", 932.0, NUM1, "m", "Primary + team estimate",
     "Q4 FY26 diluted WASO 932.1m (8-K Ex. 99.1, 9/10/26); 926.3m basic shares outstanding 9/25/26 (10-K cover) + ~5m dilution. "
     "No net FY27 buybacks assumed (cash committed to ACV); buyback risk (930m / 920m) and the earlier 940m tested in Sensitivity."),
    ("tax", "Effective tax rate", 0.195, PCT, "%", "Primary-derived", "FY26 10-K: tax $354.6m / pre-tax $1,835.0m = 19.3%"),
    ("cash0", "Cash + restricted cash + HTM securities, 7/31/26", 4.49, NUM2, "$bn", "Primary",
     "FY26 10-K: $1,907.9m cash, equivalents & restricted + $2,581.9m HTM"),
    ("cash_val", "Cash + securities at the valuation date (mid-Feb 2027, post-ACV)", 3.08, NUM2, "$bn", "Team estimate",
     "$4.49bn − $1.90bn ACV + ~$0.49bn retained FCF (6.5 months at ~$0.91bn/yr ≈ 72% of FY26 FCF $1.27bn); no buybacks; each ±$0.2bn ≈ ±$0.21/sh"),
    ("int26", "FY26 interest income", 181.9, USDM, "$m", "Primary", "FY26 10-K segment note: interest income $181.9m"),
    ("intq1", "Interest income per quarter before ACV close", 38.0, USDM, "$m", "Team estimate", "Q3/Q4-FY26 actual $38.8m / $39.6m; cash before the ACV payment"),
])

row = inp_section(row + 1, "ACV transaction timing")
row = inp_rows(row, [
    ("acv_frac", "Share of Q2 FY27 (Nov-Jan) with ACV consolidated", 0.50, PCT, "%", "Team estimate",
     "Model assumes closing during Q2 FY27 (base: mid-Q2, ~Dec 15); company guidance is close by calendar year-end 2026 (10-K; Q4 call). "
     "Tender (10/7) and HSR (10/13) milestones are not a close date. Early Q2 = 100%, late Q2 / CY-end = 33% (Sensitivity)."),
])

row = inp_section(row + 1, "Lost-customer run-rate reconciliation (Q4 FY26)")
REC0 = row
row = inp_rows(row, [
    ("ins_rep", "Q4 FY26 domestic insurance assignments y/y (reported)", -0.075, PCT, "%", "Secondary transcript",
     "Q4 FY26 call (9/10/26): domestic insurance assignments −7.5%; CFO: U.S. insurance volumes −7.5%"),
    ("ins_excust", "Q4 FY26 domestic insurance assignments y/y, excluding one lost customer", 0.023, PCT, "%", "Secondary transcript",
     "Q4 FY26 call: 'with the exception of 1 single customer loss domestic insurance assignments would be up 2.3%'"),
    ("obs", "Observed Q4 FY26 lost-customer drag (pts) = ex-customer − reported", "=B{0}-B{1}", PCT, "pts", "Derived",
     "+2.3% − (−7.5%) = 9.8 pts; applied as the drag already in the Q4 FY26 base (FY26 segment table below)"),
    ("w2loss", "W2 full-run-rate drag (pts of U.S. insurance units)", "=-Scenarios!$C$7", PCT, "pts", "Team estimate",
     "Option A: keep the 13-pt W2 full-run-rate estimate (Scenarios)"),
    ("w2share", "Implied share of the W2 run-rate already in Q4 FY26 = 9.8 / 13", "=B{2}/B{3}", PCT, "%", "Derived",
     "≈75%, replacing the v1 assumption of 60% (which did not reconcile: 9.8 / 13 ≠ 60%). Q1-Q3 FY27 carry the full drag; "
     "Q4 FY27 impact = (1 − run-rate) / (1 − 9.8%) − 1 in every world"),
    ("full60", "Full run-rate implied if only 60% was in Q4 FY26 = 9.8 / 0.60", "=B{2}/0.6", PCT, "pts", "Derived",
     "≈16 pts = W1. RB Global's 'probably over the last 90 days' (to 8/4/26) transition suggests ≤60% was in Copart's May-Jul quarter; "
     "W2 does not assume this. Tested in Sensitivity (10 / 13 / 16 pts)."),
])
for k in range(REC0, row):
    v = I.cell(k, 2).value
    if isinstance(v, str) and "{" in v:
        I.cell(k, 2).value = v.format(REC0, REC0 + 1, REC0 + 2, REC0 + 3)

row = inp_section(row + 1, "Cost of equity")
row = inp_rows(row, [
    ("rf", "10-year U.S. Treasury yield (risk-free)", 0.0524, PCT2, "%", "Primary", "U.S. Treasury Daily Par Yield Curve, 10Y on 10/01/2026 = 5.24%"),
    ("beta", "Equity beta", 0.90, NUM2, "x", "Team estimate",
     "Weekly regression of CPRT on SPY, Jul-2023 to Sep-2026 = 0.89 (team calculation); Yahoo 1.03 tested in Sensitivity"),
    ("erp", "Equity risk premium", 0.05, PCT, "%", "Team estimate",
     "Conventional U.S. ERP assumption; ±0.5pt ERP ≈ ±0.45pt cost of equity (Sensitivity cost-of-equity table)"),
    ("gT", "Terminal growth", 0.03, PCT, "%", "Team estimate", "≈ long-run nominal U.S. growth; well below CPRT's FY21-FY26 net-income CAGR (~9.7%)"),
    ("rf_stress", "Rate-cut stress: 10-year yield", 0.035, PCT2, "%", "Team estimate", "Stress case only (10Y back to 3.5%)"),
    ("coe", "Cost of equity = risk-free + beta × ERP", "=B{rf}+B{beta}*B{erp}", PCT2, "%", "Derived", "CAPM: 5.24% + 0.90 × 5.0% = 9.74%"),
    ("coe_stress", "Stress cost of equity = stress risk-free + beta × ERP", "=B{rf_stress}+B{beta}*B{erp}", PCT2, "%", "Derived", "3.50% + 0.90 × 5.0% = 8.00%"),
])
for k in range(row - 2, row):
    v = I.cell(k, 2).value
    I.cell(k, 2).value = v.format(**{kk: NM[kk].split("$")[-1] for kk in ("rf", "beta", "erp", "rf_stress")})

row = inp_section(row + 1, "Operating structure (KPI model)")
row = inp_rows(row, [
    ("sins", "U.S. insurance share of U.S. units", 0.76, PCT, "%", "Team estimate",
     "10-K: insurers supplied 79% of vehicles company-wide; U.S. mix set slightly lower given U.S. dealer/BluCar volume"),
    ("fix", "Fixed share of U.S. facility costs (does not flex with units near term)", 0.55, PCT, "%", "Team estimate",
     "Q4-FY26 call: U.S. facility costs +7.7% (+14.2% per unit) while U.S. units −5.7% → majority fixed in the short run; 45% / 65% in Sensitivity"),
    ("nonins", "U.S. non-insurance unit growth", 0.03, PCT, "%", "Team estimate", "Q4-FY26 U.S. non-insurance +0.2%, dealer units +5.8% (call)"),
    ("goth", "U.S. vehicle gross profit and G&A growth", 0.05, PCT, "%", "Team estimate", "FY26 U.S. G&A +3.7% (10-K segment note); ongoing investment"),
    ("gint", "International operating income and revenue growth", 0.10, PCT, "%", "Team estimate", "FY26 international op. income +8.2%; Q4 international revenue +11.7% (10-K, call)"),
])
row += 1

section(I, row, "FY26 quarterly segment actuals ($m) — Primary: 10-Qs Q1-Q3 FY26; Q4 = FY26 10-K less nine months", 5)
header(I, row + 1, ["Line ($m unless stated)", "Q1 Aug-Oct", "Q2 Nov-Jan", "Q3 Feb-Apr", "Q4 May-Jul"])
row += 2
INTL_REV = [202.4, 200.1, 234.2, 222.0]
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
I.cell(row, 1, "Lost-customer drag already in the FY26 quarter (pts)").font = F_BODY
for q in range(3):
    put(I, f"{get_column_letter(2 + q)}{row}", 0.0, PCT, F_IN)
put(I, f"E{row}", f"={NM['obs']}", PCT)
I[f"E{row}"].comment = Comment("Derived: the reported Q4 FY26 drag (9.8 pts) is in the Q4 base; Q1-Q3 FY26 preceded the loss.", "Margin Callers")
for c in range(1, 6):
    I.cell(row, c).border = ROW_LINE
SEG["lib"] = row
row += 1
I.cell(row, 1, "Reported FY26 diluted EPS by quarter ($/sh)").font = F_BODY
for q, v in enumerate([0.41, 0.36, 0.43, 0.35]):
    put(I, f"{get_column_letter(2 + q)}{row}", v, USD, F_IN)
for c in range(1, 6):
    I.cell(row, c).border = ROW_LINE
SEG["eps26"] = row
row += 1
I.cell(row, 1, "FY26 diluted weighted-average shares by quarter (m)").font = F_BODY
for q, v in enumerate([977.1, 975.1, 942.8, 932.1]):
    put(I, f"{get_column_letter(2 + q)}{row}", v, NUM1, F_IN)
I[f"B{row}"].comment = Comment("Primary: 10-Q XBRL (Q1-Q3 FY26) and Q4 FY26 8-K Ex. 99.1.", "Margin Callers")
for c in range(1, 6):
    I.cell(row, c).border = ROW_LINE
SEG["sh26"] = row

# ================================================================== Scenarios
S = wb.create_sheet("Scenarios")
ws_setup(S, {"A": 54, "B": 24, "C": 24, "D": 24, "E": 24})
title(S, "Scenarios", "Four economic worlds: what the market believes → KPIs → earnings → value. Blue = team estimate.")
WN = ["W1 Loss deepens", "W2 FY27 trough / FY28 normalizes", "W3 Cycle turns / ACV improves", "W4 Street right / share recapture"]
section(S, 4, "Scenario drivers (all team estimates; basis in the rows below and on Sources)", 5)
header(S, 5, ["Driver"] + WN)
W4 = dict(u=0.03, loss=-0.05, rpu=0.05, fixed=0.04, acv_amort=10, acv_op=0, int_q=28)
worlds = [se.CPRT_WORLDS["bear"], se.CPRT_WORLDS["base"], se.CPRT_WORLDS["bull"], W4]
extra = [(0.00, 0.20, 0.04, 0.03, 0.15), (0.02, 0.45, 0.12, 0.06, 0.20), (0.04, 0.20, 0.18, 0.09, 0.25), (0.02, 0.15, 0.15, 0.10, 0.25)]
PR = [("u", "Underlying U.S. insurance unit growth, ex lost customer", PCT),
      ("loss", "Lost-customer full-run-rate drag (pts of U.S. insurance units)", PCT),
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
assert P["loss"] == 7  # referenced from Inputs reconciliation block
for k, (key, lab, f) in enumerate([("acv28", "FY28 ACV EPS contribution incl. amortization and forgone interest ($/sh)", USD),
                                    ("prob", "Team scenario probability", PCT), ("g28", "FY28 EPS growth (core operating, ex-ACV)", PCT),
                                    ("g5", "EPS growth, 5 years after year 2", PCT), ("roic", "Incremental ROIC", PCT)]):
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
section(S, r, "Rationale and evidence (short; sources on Sources sheet)", 5)
header(S, r + 1, ["Item"] + WN)
TXT = [
    ("What each world assumes (evidence)", [
        "Loss broadens beyond one customer; ASP softens (Manheim −0.4% y/y mid-Sep, Cox); OpEx/car stays high (+12.7% in Q4, transcript summary). 16-pt run-rate ≈ only 60% in the Q4 FY26 base.",
        "The disclosed loss runs at its full 13-pt rate Q1-Q3 FY27 and partly laps in Q4 (~75% already in the Q4 FY26 base). Fixed costs +7%. ACV per model.",
        "Ex-customer insurance units +3% (Q4 ex-customer +2.3%, call); record second-quarter 23.3% total-loss frequency (call).",
        "Share recapture offsets most of the lost volume; published FY27 consensus roughly delivered. Team scenario based on public data only."]),
    ("Probability rationale (team scenario probabilities; judgmental, not objective)", [
        "20%: plausible but not base. Requires losses beyond the one disclosed customer; management described customer relationships as strong.",
        "45%: most likely. The only disclosed loss runs at full rate until it laps in Q4 FY27; RB Global says the transfer is done; costs are largely fixed near term (Q4 facility costs +7.7% on units −5.7%).",
        "20%: record total-loss frequency, rising severity and pricing (U.S. insurance ASP +3.7%) offset the volume hole faster than we model.",
        "15%: the Street is right. Published FY27 consensus ($1.62-$1.65) implies the loss is largely absorbed; CPRT has historically rebounded after large negative reactions (Checks)."]),
    ("FY28 ACV contribution support", [
        "$0.00: accretion guidance not met in FY28.",
        "+$0.02: modestly accretive, consistent with guidance (neutral in the first full year; accretive FY28 and beyond).",
        "+$0.04: synergies arrive faster than guided.",
        "+$0.02: guidance delivered."]),
    ("5-year EPS growth (g) support", [
        "3%: pricing-only growth; no unit recovery.",
        "6%: normalized low-single-digit unit growth plus pricing; below the FY21-FY26 net-income CAGR (~9.7%).",
        "9%: close to the FY21-FY26 net-income CAGR (~9.7%).",
        "10%: historical growth resumes."]),
    ("Incremental ROIC support", [
        "15%: about half of recent core ROIC; lower utilization persists.",
        "20%: below recent core ROIC (~29-31%, FY25-FY26 NOPAT / equity ex cash & HTM), reflecting lower utilization and ACV mix.",
        "25%: still below recent core ROIC.",
        "25%: still below recent core ROIC."]),
]
rr = r + 2
for lab, texts in TXT:
    put(S, f"A{rr}", lab, wrap=True)
    for j, t in enumerate(texts):
        put(S, f"{get_column_letter(2 + j)}{rr}", t, wrap=True)
    rr += 1

# ================================================================== EPS build
E = wb.create_sheet("EPS_Build")
ws_setup(E, {"A": 52, "B": 12, "C": 12, "D": 12, "E": 12, "F": 12})
title(E, "FY27 EPS build (Aug-26 to Jul-27), $m unless stated",
      "Chain: lost-customer impact → U.S. insurance units → U.S. service revenue → operating income → EPS. "
      "Model assumes closing during Q2 FY27; company guidance is close by calendar year-end 2026. Q2 ACV P&L and interest are pro-rated "
      "by the consolidated share of Q2 (Inputs). Ex-ACV and GAAP-with-ACV kept separate.")
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
    ("core", "Core operating EPS, ex-interest, ex-ACV ($/sh)", USD),
    ("int_x", "Interest income, ex-ACV case ($m)", USDM),
    ("eps_x", "EPS ex-ACV (operating thesis)", USD),
    ("acv", "ACV pre-tax: operating income − amortization ($m)", USDM),
    ("int_g", "Interest income after ACV cash outflow ($m)", USDM),
    ("eps_g", "GAAP EPS incl. ACV", USD),
    ("acv_eps", "ACV EPS impact incl. forgone interest ($/sh)", USD),
    ("exint_g", "EPS ex-interest incl. ACV (valuation base, $/sh)", USD),
]
BOLDK = ("eps_x", "eps_g")
BLOCK = len(LINES) + 4
EPSX, EPSG, QX_ROWS = {}, {}, {}
for j in range(4):
    top = 4 + j * BLOCK
    wc = get_column_letter(2 + j)
    section(E, top, WN[j], 6)
    header(E, top + 1, ["Line", "Q1 Aug-Oct", "Q2 Nov-Jan", "Q3 Feb-Apr", "Q4 May-Jul", "FY27"])
    R = {key: top + 2 + k for k, (key, _, _) in enumerate(LINES)}
    for key, lab, f in LINES:
        E.cell(R[key], 1, lab).font = F_BOLD if key in BOLDK else F_BODY
        for c in range(1, 7):
            E.cell(R[key], c).border = ROW_LINE
    for q in range(4):
        c = get_column_letter(2 + q)
        s_ = lambda k: f"Scenarios!${wc}${P[k]}"
        g = lambda k: f"Inputs!{c}${SEG[k]}"
        cell = lambda k: f"{c}{R[k]}"
        fr = NM["acv_frac"]
        F = {
            "loss": f"=(1+{s_('loss')})/(1-{g('lib')})-1",
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
            "core": f"=({cell('usoi')}+{cell('ioi')})*(1-{NM['tax']})/{NM['shares']}",
            "int_x": f"={NM['intq1']}",
            "eps_x": f"=({cell('usoi')}+{cell('ioi')}+{cell('int_x')})*(1-{NM['tax']})/{NM['shares']}",
            "acv": ["=0", f"={fr}*({s_('acv_op')}-{s_('acv_amort')})", f"={s_('acv_op')}-{s_('acv_amort')}", f"={s_('acv_op')}-{s_('acv_amort')}"][q],
            "int_g": [f"={NM['intq1']}", f"={fr}*{s_('int_q')}+(1-{fr})*{NM['intq1']}", f"={s_('int_q')}", f"={s_('int_q')}"][q],
            "eps_g": f"=({cell('usoi')}+{cell('ioi')}+{cell('acv')}+{cell('int_g')})*(1-{NM['tax']})/{NM['shares']}",
            "acv_eps": f"={cell('eps_g')}-{cell('eps_x')}",
            "exint_g": f"=({cell('usoi')}+{cell('ioi')}+{cell('acv')})*(1-{NM['tax']})/{NM['shares']}",
        }
        for key, f in F.items():
            fmt = next(x[2] for x in LINES if x[0] == key)
            put(E, cell(key), f, fmt, F_BOLD if key in BOLDK else F_BODY)
    for key in ("svc", "vrev", "fac", "ga", "usoi", "ioi", "irev", "core", "int_x", "eps_x", "acv", "int_g", "eps_g", "acv_eps", "exint_g"):
        fmt = next(x[2] for x in LINES if x[0] == key)
        put(E, f"F{R[key]}", f"=SUM(B{R[key]}:E{R[key]})", fmt, F_BOLD)
    put(E, f"F{R['usm']}", f"=F{R['usoi']}/(F{R['svc']}+F{R['vrev']})", PCT, F_BOLD)
    put(E, f"F{R['cm']}", f"=(F{R['usoi']}+F{R['ioi']})/(F{R['svc']}+F{R['vrev']}+F{R['irev']})", PCT, F_BOLD)
    EPSX[j], EPSG[j] = f"EPS_Build!$F${R['eps_x']}", f"EPS_Build!$F${R['eps_g']}"
    QX_ROWS[j] = R


def vexc_f(e1, e2, g, ro, r_, gt):
    """Ex-cash value: payout (1-g/ROIC) on year-1 (NTM) and year-2 earnings, years 3-5 at g, Gordon terminal."""
    po = f"(1-{g}/{ro})"
    pv = (f"{po}*({e1}/(1+{r_})+{e2}/(1+{r_})^2+{e2}*(1+{g})/(1+{r_})^3+{e2}*(1+{g})^2/(1+{r_})^4"
          f"+{e2}*(1+{g})^3/(1+{r_})^5)")
    tv = f"{e2}*(1+{g})^4*(1-{gt}/{ro})/({r_}-{gt})/(1+{r_})^5"
    return pv, tv


# ================================================================== Valuation
V = wb.create_sheet("Valuation")
ws_setup(V, {"A": 58, "B": 19, "C": 19, "D": 19, "E": 19})
title(V, "Valuation at the planned exit: mid-February 2027 (after Q2 FY27 results)",
      "Value = PV of distributions (payout 1 − g/ROIC) from year-1 (NTM) and year-2 earnings, years 3-5 at g and a Gordon terminal, "
      "discounted at the cost of equity; ex-interest earnings, with net cash at the valuation date added. Justified P/E = ex-cash value / NTM EPS "
      "(derived from growth, ROIC and cost of equity, not selected).")
V.merge_cells("A2:E2")
V["A2"].font = F_NOTE
V["A2"].alignment = Alignment(wrap_text=True, vertical="top")
put(V, "A3", "Valuation date: mid-February 2027, following Q2 FY27 results", font=F_BOLD)
V.merge_cells("A4:E4")
put(V, "A4", "Forward earnings basis: NTM = Q3 FY27 + Q4 FY27 (modeled, incl. ACV) + Q1 FY28 + Q2 FY28 (each = the matching FY27 quarter's "
             "core operating EPS × (1 + FY28 growth) + ¼ of the FY28 ACV contribution ex-interest); ex-interest. Year 2 = Q3 FY28 - Q2 FY29.",
    font=F_NOTE, wrap=True)
VR = {}


def vblock(top, title_, lines):
    section(V, top, title_, 5)
    header(V, top + 1, ["Line"] + WN)
    for i, (k, lab, fmt) in enumerate(lines):
        VR[k] = top + 2 + i
        V.cell(VR[k], 1, lab).font = F_BOLD if k in VBOLD else F_BODY
        for c in range(1, 6):
            V.cell(VR[k], c).border = ROW_LINE
    return top + 2 + len(lines) + 1


VBOLD = ("eps27x", "eps27g", "fy28", "ntm", "vexc", "jpe", "val", "ret", "sret")
VL1 = [("prob", "Team scenario probability", PCT), ("eps27x", "FY27 EPS ex-ACV ($/sh)", USD), ("acv27", "FY27 modeled ACV impact ($/sh)", USD),
       ("eps27g", "FY27 GAAP EPS incl. ACV ($/sh)", USD), ("fy28sa", "FY28 standalone CPRT EPS before ACV ($/sh)", USD),
       ("acv28", "FY28 ACV contribution ($/sh, team estimate)", USD), ("fy28", "FY28 EPS incl. ACV ($/sh)", USD)]
VL2 = [("q3", "Q3 FY27 (Feb-Apr 27) ex-interest EPS incl. ACV", USD), ("q4", "Q4 FY27 (May-Jul 27) ex-interest EPS incl. ACV", USD),
       ("acvq", "FY28 ACV contribution ex-interest, per quarter", USD), ("q1n", "Q1 FY28 (Aug-Oct 27) ex-interest EPS", USD),
       ("q2n", "Q2 FY28 (Nov 27-Jan 28) ex-interest EPS", USD), ("ntm", "NTM ex-interest EPS at mid-Feb 2027 (year 1)", USD),
       ("ntm2", "Year 2 ex-interest EPS (Q3 FY28 - Q2 FY29)", USD), ("y2g", "Year-2 growth (FY28 recovery completes)", PCT)]
VL3 = [("g", "EPS growth, years 3-5 and terminal fade start (g)", PCT), ("roic", "Incremental ROIC", PCT), ("r", "Cost of equity (Inputs)", PCT2),
       ("gt", "Terminal growth (Inputs)", PCT), ("po", "Payout = 1 − g / ROIC", PCT), ("pv5", "PV of years 1-5 distributions ($/sh)", USD),
       ("pvt", "PV of terminal value ($/sh)", USD), ("vexc", "Ex-cash equity value ($/sh)", USD), ("jpe", "Justified ex-cash P/E on NTM EPS", MULT),
       ("cash", "Net cash per share at the valuation date ($/sh)", USD), ("val", "Value per share, mid-Feb 2027 ($/sh)", USD),
       ("ret", "Stock return vs reference price", PCT), ("sret", "Short return", PCT),
       ("ntmint", "NTM after-tax interest per share ($/sh)", USD), ("tpe", "Implied total P/E on NTM EPS incl. interest", MULT)]
nxt = vblock(6, "EPS by world: FY27 and FY28 (FY28 = standalone + explicit ACV)", VL1)
nxt = vblock(nxt + 1, "Forward earnings bridge at the valuation date (ex-interest, $/sh)", VL2)
nxt = vblock(nxt + 1, "Valuation", VL3)
for j in range(4):
    c = get_column_letter(2 + j)
    ref = lambda k: f"{c}{VR[k]}"
    sc = lambda k: f"Scenarios!{c}${P[k]}"
    R = QX_ROWS[j]
    eb = lambda k, q: f"EPS_Build!{get_column_letter(2 + q)}{R[k]}"
    t_sh = f"(1-{NM['tax']})/{NM['shares']}"
    pv, tv = vexc_f(ref("ntm"), ref("ntm2"), ref("g"), ref("roic"), ref("r"), ref("gt"))
    FV = {
        "prob": f"={sc('prob')}", "eps27x": f"={EPSX[j]}", "acv27": f"=EPS_Build!F{R['acv_eps']}", "eps27g": f"={EPSG[j]}",
        "fy28sa": f"=EPS_Build!F{R['core']}*(1+{sc('g28')})+{NM['intq1']}*4*{t_sh}",
        "acv28": f"={sc('acv28')}", "fy28": f"={ref('fy28sa')}+{ref('acv28')}",
        "q3": f"={eb('exint_g', 2)}", "q4": f"={eb('exint_g', 3)}",
        "acvq": f"=({sc('acv28')}+({NM['intq1']}-{sc('int_q')})*4*{t_sh})/4",
        "q1n": f"={eb('core', 0)}*(1+{sc('g28')})+{ref('acvq')}", "q2n": f"={eb('core', 1)}*(1+{sc('g28')})+{ref('acvq')}",
        "ntm": f"={ref('q3')}+{ref('q4')}+{ref('q1n')}+{ref('q2n')}",
        "ntm2": f"=({eb('core', 2)}+{eb('core', 3)})*(1+{sc('g28')})+2*{ref('acvq')}+({ref('q1n')}+{ref('q2n')})*(1+{sc('g5')})",
        "y2g": f"={ref('ntm2')}/{ref('ntm')}-1",
        "g": f"={sc('g5')}", "roic": f"={sc('roic')}", "r": f"={NM['coe']}", "gt": f"={NM['gT']}",
        "po": f"=1-{ref('g')}/{ref('roic')}", "pv5": f"={pv}", "pvt": f"={tv}", "vexc": f"={ref('pv5')}+{ref('pvt')}",
        "jpe": f"={ref('vexc')}/{ref('ntm')}", "cash": f"={NM['cash_val']}*1000/{NM['shares']}",
        "val": f"={ref('vexc')}+{ref('cash')}", "ret": f"={ref('val')}/{NM['price']}-1", "sret": f"=-{ref('ret')}",
        "ntmint": f"={sc('int_q')}*4*{t_sh}", "tpe": f"={ref('val')}/({ref('ntm')}+{ref('ntmint')})",
    }
    for k, f in FV.items():
        fmt = next(x[2] for x in VL1 + VL2 + VL3 if x[0] == k)
        put(V, ref(k), f, fmt, F_BOLD if k in VBOLD else link_font(f), align="right")
r0 = nxt + 1
section(V, r0, "Probability-weighted result and downside", 5)
OUT = [
    ("pw", "Probability-weighted value ($/sh)", f"=SUMPRODUCT(B{VR['prob']}:E{VR['prob']},B{VR['val']}:E{VR['val']})", USD),
    ("pwret", "Probability-weighted (expected) stock return", f"=B{r0 + 1}/{NM['price']}-1", PCT),
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
STRESS = [("W3 NTM ex-interest EPS ($/sh)", f"=D{VR['ntm']}", USD), ("W3 year-2 ex-interest EPS ($/sh)", f"=D{VR['ntm2']}", USD),
          ("EPS growth (W3)", f"=D{VR['g']}", PCT), ("Incremental ROIC (W3)", f"=D{VR['roic']}", PCT),
          ("Stress cost of equity (Inputs)", f"={NM['coe_stress']}", PCT2)]
for i, (lab, f, fmt) in enumerate(STRESS, start=1):
    V.cell(rs + i, 1, lab).font = F_BODY
    put(V, f"B{rs + i}", f, fmt, link_font(f), align="right")
e1, e2, gS, roS, rS = (f"B{rs + k}" for k in range(1, 6))
pvS, tvS = vexc_f(e1, e2, gS, roS, rS, NM["gT"])
V.cell(rs + 6, 1, "Stress ex-cash value ($/sh)").font = F_BODY
put(V, f"B{rs + 6}", f"={pvS}+{tvS}", USD, align="right")
V.cell(rs + 7, 1, "Stress value per share ($/sh)").font = F_BOLD
put(V, f"B{rs + 7}", f"=B{rs + 6}+D{VR['cash']}", USD, F_BOLD, align="right")
V.cell(rs + 8, 1, "Rate-cut stress short loss (stock return)").font = F_BOLD
put(V, f"B{rs + 8}", f"=B{rs + 7}/{NM['price']}-1", PCT, F_BOLD, align="right")
VO["stress"] = f"Valuation!$B${rs + 8}"
VO["stressval"] = f"Valuation!$B${rs + 7}"
re_ = rs + 10
section(V, re_, "EPS-only check: today's market multiple held constant; only EPS changes", 5)
V.cell(re_ + 1, 1, "Market ex-cash, ex-interest NTM P/E on published FY27 consensus $1.62").font = F_BODY
put(V, f"B{re_ + 1}", f"=({NM['price']}-{NM['cash0']}*1000/{NM['shares']})/(Consensus!C9-{NM['int26']}*0.6*(1-{NM['tax']})/{NM['shares']})",
    MULT, align="right")
V.cell(re_ + 2, 1, "Stock return, EPS-only (market P/E × our NTM + cash)").font = F_BODY
for j in range(4):
    c = get_column_letter(2 + j)
    put(V, f"{c}{re_ + 2}", f"=($B${re_ + 1}*{c}{VR['ntm']}+{c}{VR['cash']})/{NM['price']}-1", PCT, align="right")
V.cell(re_ + 3, 1, "Expected short return, EPS-only (no multiple change)").font = F_BOLD
put(V, f"B{re_ + 3}", f"=-SUMPRODUCT(B{VR['prob']}:E{VR['prob']},B{re_ + 2}:E{re_ + 2})", PCT, F_BOLD, align="right")
VO["epsonly"] = f"Valuation!$B${re_ + 3}"


def val_formula(c, r_="", e1d="", e2d=""):
    """Value per share for world column c with optional cost of equity override and EPS deltas."""
    v = lambda k: f"Valuation!${c}${VR[k]}"
    pv, tv = vexc_f(f"({v('ntm')}{e1d})", f"({v('ntm2')}{e2d})", v("g"), v("roic"), r_ or v("r"), v("gt"))
    return f"({pv}+{tv}+{v('cash')})"


# ================================================================== Sensitivity
T = wb.create_sheet("Sensitivity")
ws_setup(T, {"A": 50, **{get_column_letter(k): 12 for k in range(2, 14)}})
title(T, "Sensitivity (live formulas)", "Operating drivers first (lost-customer drag × fixed cost share), then valuation, ACV and share-count risks.")
TS = {}


def tsec(row, text, hdr):
    section(T, row, text, max(len(hdr), 6))
    header(T, row + 1, hdr)
    return row + 2


# W2 engine rows are written at the bottom; positions fixed first
ENG_CASES = [("drag", L, F_, 932.0) for L in (-0.10, -0.13, -0.16) for F_ in (0.45, 0.55, 0.65)] + \
            [("shares", -0.13, 0.55, n) for n in (940.0, 932.0, 930.0, 920.0)]
row = 4
row = tsec(row, "Key operating sensitivity: lost-customer drag × fixed facility cost share (W2; all other drivers unchanged)",
           ["Run-rate drag \\ fixed share", "45%", "55%", "65%"])
MAT0 = row
row += 3 * 5
row = tsec(row, "Lost-customer drag (W2, fixed share 55%)", ["Full-run-rate drag", "Q1 FY27 EPS", "FY27 EPS ex-ACV", "Base-case value", "Short return"])
DRAG0 = row
row += 4
row = tsec(row, "Diluted shares / buyback risk (W2; buybacks at $27.29 funded from cash, interest forgone)",
           ["Diluted shares (m)", "Q1 FY27 EPS", "FY27 EPS ex-ACV", "Base-case value", "Short return"])
SH0 = row
row += 5
row = tsec(row, "Cost-of-equity shift (all four worlds revalued)", ["Cost-of-equity shift", "Shift", "Cost of equity", "Base-case value", "Expected short return"])
for k, shf in enumerate([-0.01, -0.005, 0.0, 0.005, 0.01]):
    rr = row + k
    put(T, f"A{rr}", f"Cost of equity {shf * 100:+.1f}pt" if shf else "Cost of equity (base)")
    put(T, f"B{rr}", shf, PCTS, F_IN, align="right")
    put(T, f"C{rr}", f"={NM['coe']}+B{rr}", PCT2, align="right")
    put(T, f"D{rr}", "=" + val_formula("C", r_=f"$C{rr}"), USD, align="right")
    terms = [f"Valuation!{get_column_letter(2 + j)}{VR['prob']}*({val_formula(get_column_letter(2 + j), r_=f'$C{rr}')}/{NM['price']}-1)" for j in range(4)]
    put(T, f"E{rr}", "=-(" + "+".join(terms) + ")", PCT, F_BOLD if shf == 0 else F_BODY, align="right")
row += 6
row = tsec(row, "FY28 ACV EPS contribution (applied to all worlds)", ["FY28 ACV contribution ($/sh)", "−$0.04", "$0.00", "+$0.02", "+$0.04"])
ACVS = [-0.04, 0.0, 0.02, 0.04]
labs = ["W2 FY28 EPS incl. ACV ($/sh)", "Base-case (W2) value ($/sh)", "Expected short return"]
for i, lab in enumerate(labs):
    put(T, f"A{row + i}", lab)
for k, cval in enumerate(ACVS):
    col = get_column_letter(2 + k)
    d = lambda c: f"({cval}-Valuation!${c}${VR['acv28']})"
    put(T, f"{col}{row}", f"=Valuation!$C${VR['fy28sa']}+{cval}", USD, align="right")
    put(T, f"{col}{row + 1}", "=" + val_formula("C", e1d=f"+{d('C')}/2", e2d=f"+{d('C')}/2*(2+Valuation!$C${VR['g']})"), USD, align="right")
    terms = []
    for j in range(4):
        c = get_column_letter(2 + j)
        terms.append(f"Valuation!{c}{VR['prob']}*({val_formula(c, e1d=f'+{d(c)}/2', e2d=f'+{d(c)}/2*(2+Valuation!${c}${VR[chr(103)]})')}/{NM['price']}-1)")
    put(T, f"{col}{row + 2}", "=-(" + "+".join(terms) + ")", PCT, align="right")
put(T, f"A{row + 3}", "FY28 ACV changes NTM through Q1-Q2 FY28 (half) and year 2 in full. Base: W1 $0.00, W2 +$0.02, W3 +$0.04, W4 +$0.02.", font=F_NOTE)
row += 5
row = tsec(row, "ACV closing date (W2 FY27 GAAP EPS; ex-ACV thesis unaffected)",
           ["Closing timing", "Share of Q2 consolidated", "FY27 GAAP EPS", "vs model base", "Value impact"])
q2full = (f"((Scenarios!$C${P['acv_op']}-Scenarios!$C${P['acv_amort']})+(Scenarios!$C${P['int_q']}-{NM['intq1']}))"
          f"*(1-{NM['tax']})/{NM['shares']}")
for k, (lab, fr) in enumerate([("Early Q2 (~Nov 1, 2026)", 1.0), ("Mid Q2 (~Dec 15, 2026; model base)", 0.5),
                               ("Late Q2 / calendar year-end (~Dec 31, 2026)", 1 / 3)]):
    rr = row + k
    put(T, f"A{rr}", lab)
    put(T, f"B{rr}", fr, PCT, F_IN, align="right")
    put(T, f"C{rr}", f"=Valuation!$C${VR['eps27g']}+(B{rr}-{NM['acv_frac']})*{q2full}", USD, align="right")
    put(T, f"D{rr}", f"=C{rr}-Valuation!$C${VR['eps27g']}", USD, align="right")
    put(T, f"E{rr}", "None", align="right")
put(T, f"A{row + 3}", "Model assumes closing during Q2 FY27; company guidance is close by calendar year-end 2026. Q3 onward is fully consolidated in all cases, "
                      "so the mid-Feb valuation is unaffected.", font=F_NOTE)
row += 5
row = tsec(row, "Probability shifts (scenario values unchanged)", ["Probability set (W1 / W2 / W3 / W4)", "Expected short return", "", "", "Note"])
for k, (lab, ps, note) in enumerate([("Base 20 / 45 / 20 / 15", (0.20, 0.45, 0.20, 0.15), "Governing"),
                                     ("Bearish tilt 30 / 45 / 15 / 10", (0.30, 0.45, 0.15, 0.10), "More weight to loss broadening"),
                                     ("Bullish tilt 15 / 40 / 25 / 20", (0.15, 0.40, 0.25, 0.20), "More weight to recovery")]):
    rr = row + k
    put(T, f"A{rr}", lab)
    put(T, f"B{rr}", "=-(" + "+".join(f"{p}*Valuation!{get_column_letter(2 + j)}{VR['ret']}" for j, p in enumerate(ps)) + ")", PCT, align="right")
    put(T, f"E{rr}", note)
row += 4
row = tsec(row, "Beta cross-check", ["Item", "Cost of equity", "Base-case value", "Exp. short return", "Note"])
put(T, f"A{row}", "Beta 1.03 (Yahoo, secondary) instead of 0.90")
put(T, f"B{row}", f"={NM['rf']}+1.03*{NM['erp']}", PCT2, align="right")
put(T, f"C{row}", "=" + val_formula("C", r_=f"$B{row}"), USD, align="right")
terms = [f"Valuation!{get_column_letter(2 + j)}{VR['prob']}*({val_formula(get_column_letter(2 + j), r_=f'$B{row}')}/{NM['price']}-1)" for j in range(4)]
put(T, f"D{row}", "=-(" + "+".join(terms) + ")", PCT, align="right")
put(T, f"E{row}", "Higher beta raises the cost of equity (short return rises)")
row += 2
row = tsec(row, "Downside reference (from Valuation)", ["Item", "Value"])
put(T, f"A{row}", "W4 adverse-case short loss")
put(T, f"B{row}", f"={VO['w4loss']}", PCT, F_LINK, align="right")
put(T, f"A{row + 1}", "Rate-cut stress (10Y to 3.5%) short loss")
put(T, f"B{row + 1}", f"={VO['stress']}", PCT, F_LINK, align="right")
row += 3

# ---- W2 operating sensitivity engine (transparent replay of EPS_Build W2 with changed drivers)
row = tsec(row, "W2 sensitivity engine: replay of EPS_Build W2 with the drivers in blue changed (feeds the tables above)",
           ["Case", "Run-rate drag", "Fixed share", "Shares (m)", "Core Q1", "Core Q2", "Core Q3", "Core Q4",
            "Q1 EPS ex-ACV", "FY27 EPS ex-ACV", "NTM ex-int", "Year 2 ex-int", "Value ($/sh)"])
ENG0 = row
sc2 = lambda k: f"Scenarios!$C${P[k]}"
for i, (kind, L, F_, N) in enumerate(ENG_CASES):
    rr = ENG0 + i
    put(T, f"A{rr}", f"Drag {-L:.0%}, fixed {F_:.0%}" if kind == "drag" else f"Shares {N:.0f}m")
    put(T, f"B{rr}", L, PCT, F_IN, align="right")
    put(T, f"C{rr}", F_, PCT, F_IN, align="right")
    put(T, f"D{rr}", N, NUM1, F_IN, align="right")
    for q in range(4):
        c = get_column_letter(2 + q)
        g = lambda k: f"Inputs!${c}${SEG[k]}"
        imp = f"((1+$B{rr})/(1-{g('lib')})-1)"
        units = f"({NM['sins']}*({sc2('u')}+{imp})+(1-{NM['sins']})*{NM['nonins']})"
        usoi = (f"({g('us_service')}*(1+{units})*(1+{sc2('rpu')})+({g('us_vehicle')}-{g('us_cogs_vehicle')})*(1+{NM['goth']})"
                f"-({g('us_facility')}*$C{rr}*(1+{sc2('fixed')})+{g('us_facility')}*(1-$C{rr})*(1+{units}))-{g('us_ga')}*(1+{NM['goth']}))")
        put(T, f"{get_column_letter(5 + q)}{rr}", f"=({usoi}+{g('intl_oi')}*(1+{NM['gint']}))*(1-{NM['tax']})/$D{rr}", USD, align="right")
    t_sh = f"(1-{NM['tax']})/$D{rr}"
    dI = f"(-({NM['shares']}-$D{rr})*{NM['price']}*({NM['intq1']}*4/({NM['cash0']}*1000))/4)"
    put(T, f"I{rr}", f"=E{rr}+({NM['intq1']}+{dI})*{t_sh}", USD, align="right")
    put(T, f"J{rr}", f"=SUM(E{rr}:H{rr})+4*({NM['intq1']}+{dI})*{t_sh}", USD, align="right")
    acvq = f"(({sc2('acv28')}+({NM['intq1']}-{sc2('int_q')})*4*{t_sh})/4)"
    acvq3 = f"({sc2('acv_op')}-{sc2('acv_amort')})*{t_sh}"
    q1n, q2n = f"(E{rr}*(1+{sc2('g28')})+{acvq})", f"(F{rr}*(1+{sc2('g28')})+{acvq})"
    put(T, f"K{rr}", f"=G{rr}+H{rr}+2*{acvq3}+{q1n}+{q2n}", USD, align="right")
    put(T, f"L{rr}", f"=(G{rr}+H{rr})*(1+{sc2('g28')})+2*{acvq}+({q1n}+{q2n})*(1+{sc2('g5')})", USD, align="right")
    pv, tv = vexc_f(f"K{rr}", f"L{rr}", f"Valuation!$C${VR['g']}", f"Valuation!$C${VR['roic']}", f"Valuation!$C${VR['r']}", f"Valuation!$C${VR['gt']}")
    cashc = f"({NM['cash_val']}-({NM['shares']}-$D{rr})*{NM['price']}/1000)*1000/$D{rr}"
    put(T, f"M{rr}", f"={pv}+{tv}+{cashc}", USD, F_BOLD, align="right")
ENG = {(kind, L, F_, N): ENG0 + i for i, (kind, L, F_, N) in enumerate(ENG_CASES)}
# fill matrices
for m, (lab, col) in enumerate([("Q1 FY27 EPS ex-ACV ($/sh)", "I"), ("FY27 EPS ex-ACV ($/sh)", "J"), ("Base-case (W2) value ($/sh)", "M")]):
    top = MAT0 + m * 5
    put(T, f"A{top}", lab, font=F_BOLD)
    for i, L in enumerate((-0.10, -0.13, -0.16)):
        put(T, f"A{top + 1 + i}", f"{-L:.0%} pts drag" + (" (W2 base)" if L == -0.13 else ""))
        for k, F_ in enumerate((0.45, 0.55, 0.65)):
            put(T, f"{get_column_letter(2 + k)}{top + 1 + i}", f"={col}{ENG[('drag', L, F_, 932.0)]}", USD,
                F_BOLD if (L == -0.13 and F_ == 0.55) else F_BODY, align="right")
for i, L in enumerate((-0.10, -0.13, -0.16)):
    rr = DRAG0 + i
    e = ENG[("drag", L, 0.55, 932.0)]
    put(T, f"A{rr}", f"{-L:.0%} pts" + (" (W2 base)" if L == -0.13 else (" (≈ W3 run-rate)" if L == -0.10 else " (≈ 60%-in-Q4 implied; W1)")))
    put(T, f"B{rr}", f"=I{e}", USD, align="right")
    put(T, f"C{rr}", f"=J{e}", USD, align="right")
    put(T, f"D{rr}", f"=M{e}", USD, F_BOLD if L == -0.13 else F_BODY, align="right")
    put(T, f"E{rr}", f"=-(D{rr}/{NM['price']}-1)", PCT, align="right")
for i, N in enumerate((940.0, 932.0, 930.0, 920.0)):
    rr = SH0 + i
    e = ENG[("shares", -0.13, 0.55, N)]
    put(T, f"A{rr}", f"{N:.0f}m" + {940.0: " (v1 assumption)", 932.0: " (model: Q4 FY26 diluted WASO)", 930.0: " (modest buybacks)", 920.0: " (accelerated buybacks)"}[N])
    put(T, f"B{rr}", f"=I{e}", USD, align="right")
    put(T, f"C{rr}", f"=J{e}", USD, align="right")
    put(T, f"D{rr}", f"=M{e}", USD, F_BOLD if N == 932.0 else F_BODY, align="right")
    put(T, f"E{rr}", f"=-(D{rr}/{NM['price']}-1)", PCT, align="right")
TS["eng_base"] = f"Sensitivity!$M${ENG[('drag', -0.13, 0.55, 932.0)]}"
TS["eng_base_fy27"] = f"Sensitivity!$J${ENG[('drag', -0.13, 0.55, 932.0)]}"

# ================================================================== Consensus
C = wb.create_sheet("Consensus")
ws_setup(C, {"A": 50, "B": 15, "C": 11, "D": 7, "E": 11, "F": 11, "G": 72})
title(C, "Consensus (secondary sources) and our estimates")
section(C, 3, "Published consensus — kept separate by provider (re-verified 10/2/26)", 7)
header(C, 4, ["Provider / period", "Date pulled", "EPS ($/sh)", "n", "Low", "High", "Basis / note"])
CONS = [
    ("Zacks: Q1 FY27 (Oct-26)", "10/2/26", 0.41, 4, 0.38, 0.43, "Via Nasdaq (Zacks); quarterly consensus; unchanged vs 10/1/26 pull"),
    ("Zacks: Q2 FY27 (Jan-27)", "10/2/26", 0.37, 4, 0.36, 0.39, ""),
    ("Zacks: Q3 FY27 (Apr-27)", "10/2/26", 0.45, 4, 0.43, 0.47, ""),
    ("Zacks: Q4 FY27 (Jul-27)", "10/2/26", 0.41, 4, 0.38, 0.44, ""),
    ("S&P Global MI via StockAnalysis: published FY27 EPS consensus (Jul-27)", "updated 9/25/26", 1.62, 9, 1.56, 1.67,
     "Published FY27 EPS consensus. Public aggregate does not disclose exact ACV accounting treatment; we compare our ex-ACV estimate to isolate the core operating thesis."),
    ("Zacks: FY27 (Jul-27)", "10/2/26", 1.65, 5, 1.57, 1.70, "Published FY27 EPS consensus; ACV treatment not disclosed"),
    ("Zacks: FY28 (Jul-28)", "10/2/26", 1.81, 5, 1.72, 1.88, ""),
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
    ("Q1 FY27 EPS vs Zacks", f"=EPS_Build!B{R2['eps_x']}", "=C5", "Q1 (Aug-Oct) precedes any ACV consolidation"),
    ("Q2 FY27 EPS ex-ACV vs Zacks", f"=EPS_Build!C{R2['eps_x']}", "=C6", ""),
    ("FY27 EPS ex-ACV vs published FY27 consensus (S&P Global)", f"={EPSX[1]}", "=C9", "Core operating thesis comparison"),
    ("FY27 EPS ex-ACV vs Zacks FY27", f"={EPSX[1]}", "=C10", ""),
    ("FY27 GAAP EPS incl. modeled ACV vs S&P Global", f"={EPSG[1]}", "=C9",
     "Team ACV estimate (amortization, forgone interest, close mid-Q2); company guides EPS-neutral in the first full year"),
    ("FY28 EPS incl. ACV vs Zacks FY28", f"=Valuation!C{VR['fy28']}", "=C11", "FY28 = standalone + explicit ACV contribution"),
]
for i, (lab, ours, cons, note) in enumerate(GAPS, start=16):
    put(C, f"A{i}", lab)
    put(C, f"B{i}", ours, USD, link_font(ours), align="right")
    put(C, f"C{i}", cons, USD, align="right")
    put(C, f"D{i}", f"=B{i}/C{i}-1", PCT, F_BOLD, align="right")
    put(C, f"G{i}", note, wrap=True)
    for cc in range(1, 8):
        C.cell(i, cc).border = ROW_LINE

# ================================================================== Catalysts
K = wb.create_sheet("Catalysts")
ws_setup(K, {"A": 24, "B": 30, "C": 64, "D": 26, "E": 32})
title(K, "Catalyst path and falsification")
section(K, 3, "Catalysts (3-12 month horizon; planned exit and valuation date mid-Feb 2027, after Q2 FY27)", 5)
header(K, 4, ["Date", "Event", "What investors learn", "Supports", "Source"])
CAT = [
    ("Oct 7, 2026", "ACV tender offer expiry (extended)", "Whether a majority tenders (47.8% at 9/30). A tender result is not the close; company guides close by CY-end 2026.",
     "Neutral / secondary", "Schedule TO-T/A filed 10/1/26 (SEC)"),
    ("Oct 13, 2026", "HSR waiting period expiry (refiled 9/28)", "Whether antitrust review extends (Second Request). Not a close date.",
     "Neutral / secondary", "Schedule TO-T/A filed 9/29/26 (SEC)"),
    ("Early Nov 2026 (estimated)", "RB Global Q3-26", "First full-quarter read-through on IAA automotive units after its partner expansion",
     "Short if IAA units strong", "RB Global Q2-26 call (secondary transcript)"),
    ("Mid-Nov 2026 (estimated)", "CPRT Q1 FY27 results",
     "First full quarter of the lost-customer volume at its full run-rate; key read-throughs are U.S. insurance units, OpEx/car and U.S. operating margin.",
     "Primary discovery event", "Team estimate of timing"),
    ("Mid-Feb 2027 (estimated)", "CPRT Q2 FY27 results",
     "Second full quarter of lost volume plus the first ACV GAAP contribution (model assumes closing during Q2 FY27; company guidance is close by calendar year-end 2026). Planned exit and valuation date.",
     "Short; planned exit", "Team estimate of timing"),
]
for i, row_ in enumerate(CAT, start=5):
    for k, v in enumerate(row_):
        put(K, f"{get_column_letter(1 + k)}{i}", v, wrap=True)
    for cc in range(1, 6):
        K.cell(i, cc).border = ROW_LINE
section(K, 11, "Falsification thresholds (Q1 FY27) - exit and reassess if any is met", 5)
header(K, 12, ["KPI", "Threshold", "Our base (W2, Q1)", "", "Basis"])
FALS = [("U.S. insurance units y/y", -0.06, f"=EPS_Build!B{R2['ins']}", "Better than −6% means the lost volume is being offset"),
        ("Consolidated operating margin, ex-ACV", 0.36, f"=EPS_Build!B{R2['cm']}", "≥36% means cost absorption is not happening (yr-ago Q1 37%)"),
        ("OpEx per car growth y/y", 0.03, None, "≤ +3% means fast cost cuts (Q4-FY26 +12.7%, transcript summary; U.S. facility cost per unit +14.2%, CFO)")]
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
ws_setup(Z, {"A": 5, "B": 34, "C": 30, "D": 34, "E": 18, "F": 13, "G": 50, "H": 38})
title(Z, "Sources: audit ledger", "Source types: Primary | Secondary consensus | Secondary transcript | Secondary market data | Derived | Team estimate. "
                                 "SEC links: https://www.sec.gov/Archives/edgar/data/<CIK>/<accession without dashes>/ (CPRT CIK 900075; ACV CIK 1637873).")
header(Z, 4, ["No.", "Datapoint", "Value", "Source", "Source type", "Date", "Link / SEC accession", "Notes"])
SEC = "https://www.sec.gov/Archives/edgar/data/"
SRC = [
    ("FY26 revenue, segment P&L, Q4 derivation", "Revenue $4.67bn; U.S. service $3,388m", "Copart FY26 Form 10-K, segment note", "Primary", "9/29/26",
     f"10-K, accession 0001193125-26-405731: {SEC}900075/000119312526405731/cprt-20260731.htm", "Q4 = FY less Q1-Q3 10-Qs"),
    ("FY26 quarterly segment data (Q1-Q3)", "See Inputs", "Copart Form 10-Q filings, Q1-Q3 FY26", "Primary", "11/24/25; 3/3/26; 5/29/26",
     "10-Q accessions 0001193125-25-291660; 0001193125-26-088593; 0001193125-26-245578", ""),
    ("Diluted weighted-average shares", "932.1m (Q4 FY26); 956.9m (FY26); Q1-Q3 977.1m / 975.1m / 942.8m", "Copart Q4 FY26 earnings release (8-K Ex. 99.1); 10-Q XBRL",
     "Primary", "9/10/26", f"8-K, accession 0001193125-26-387902: {SEC}900075/000119312526387902/cprt-ex99_1.htm", "Model uses 932m (v1 used 940m)"),
    ("Shares outstanding; FY26 buybacks", "926.3m (9/25/26); 43.4m shares / $1.63bn repurchased in FY26; 282m authorized remaining",
     "Copart FY26 Form 10-K (cover; Item 5; MD&A)", "Primary", "9/29/26", "10-K, accession 0001193125-26-405731", "Buyback risk in Sensitivity"),
    ("Effective tax rate", "19.3%", "Copart FY26 Form 10-K", "Primary", "9/29/26", "10-K, accession 0001193125-26-405731", "Model uses 19.5%"),
    ("Cash, equivalents, restricted cash + HTM securities", "$1,907.9m + $2,581.9m = $4.49bn", "Copart FY26 Form 10-K, balance sheet", "Primary", "9/29/26",
     "10-K, accession 0001193125-26-405731", ""),
    ("Operating cash flow; capex", "$1,604.5m; $337.4m", "Copart FY26 Form 10-K, cash flow statement", "Primary", "9/29/26", "10-K, accession 0001193125-26-405731", "FY26 FCF $1.27bn"),
    ("Interest income FY26", "$181.9m", "Copart FY26 Form 10-K, segment note", "Primary", "9/29/26", "10-K, accession 0001193125-26-405731", ""),
    ("Q4 FY26 revenue / diluted EPS; equity", "$1.152bn / $0.35; equity $9,097m", "Copart Form 8-K Ex. 99.1 (earnings release)", "Primary", "9/10/26",
     "8-K, accession 0001193125-26-387902", ""),
    ("Q4 domestic insurance assignments; ex-one-customer", "−7.5%; +2.3%", "Copart Q4 FY26 earnings call (transcript)", "Secondary transcript", "9/10/26",
     "The Motley Fool transcript (fool.com/earnings/call-transcripts); official webcast replay: copart.com/investorrelations", "Basis of the 9.8-pt drag (Inputs)"),
    ("OpEx per car; U.S. facility costs; total-loss frequency", "+12.7%; +7.7% (+14.2% per unit); 23.3% (record second quarter, CY Q2-26)",
     "Copart Q4 FY26 earnings call (transcript)", "Secondary transcript", "9/10/26",
     "The Motley Fool transcript; official webcast replay: copart.com/investorrelations", "+12.7% is from the transcript's takeaway summary; +14.2% is the CFO's per-unit figure"),
    ("ACV close timing and EPS effect (management)", "Close by end of calendar year 2026; breakeven in the first year, accretive FY28",
     "Copart FY26 Form 10-K (Note 19; MD&A); Q4 FY26 call", "Primary", "9/29/26; 9/10/26", "10-K, accession 0001193125-26-405731; call per row 10", ""),
    ("RB Global partner expansion", "All 50 states; volume transitioned 'probably over the last 90 days'", "RB Global Q2-26 earnings call (transcript)", "Secondary transcript",
     "8/4/26", "The Motley Fool transcript; RB Global IR: investor.rbglobal.com", "Carrier identity not disclosed; not used in formulas"),
    ("ACV transaction", "$10.50/sh cash; ~$1.9bn equity value", "Copart Form 8-K (deal announcement, Ex. 99.1); Schedule TO-T", "Primary", "9/10/26; 9/17/26",
     "8-K accession 0001193125-26-388064; SC TO-T accession 0001193125-26-393827", ""),
    ("ACV EPS guidance (company)", "Neutral on EPS in the first full year; accretive FY28 and beyond", "Copart Form 8-K Ex. 99.1 (deal release)", "Primary", "9/10/26",
     "8-K, accession 0001193125-26-388064", "FY27 GAAP dilution and FY28 contribution are team estimates"),
    ("ACV tender status", "47.78% tendered; expiry extended to 10/7/26", "Schedule TO-T/A", "Primary", "10/1/26", "SC TO-T/A, accession 0001193125-26-409871", ""),
    ("HSR status", "Refiled 9/28; waiting period expected to expire 10/13/26", "Schedule TO-T/A", "Primary", "9/29/26", "SC TO-T/A, accession 0001193125-26-406039", ""),
    ("ACV TTM financials", "Revenue $801m; operating loss −$57m (TTM to Q2-26)", "ACV Auctions Form 10-K (FY25) and Form 10-Q (Q2-26), XBRL", "Primary", "2/23/26; 8/10/26",
     "ACV 10-K accession 0001637873-26-000011; 10-Q accession 0001637873-26-000034", ""),
    ("10-year Treasury yield", "5.24%", "U.S. Treasury Daily Par Yield Curve Rates", "Primary", "10/1/26",
     "home.treasury.gov/resource-center/data-chart-center/interest-rates (Daily Treasury Par Yield Curve Rates, 2026)", ""),
    ("Manheim Used Vehicle Value Index", "−0.4% y/y, mid-September", "Cox Automotive, Manheim mid-month release", "Secondary market data", "Sep 2026",
     "coxautoinc.com/market-insights (Manheim Used Vehicle Value Index)", "Qualitative support only; not in formulas"),
    ("Consensus EPS (quarterly, FY27, FY28)", "See Consensus sheet", "Zacks via Nasdaq", "Secondary consensus", "10/2/26",
     "nasdaq.com/market-activity/stocks/cprt/earnings (data: api.nasdaq.com/api/analyst/CPRT/earnings-forecast)", "Unchanged vs 10/1/26"),
    ("Share price", "$27.29", "Yahoo Finance daily close", "Secondary market data", "10/1/26", "finance.yahoo.com/quote/CPRT/history", ""),
    ("Published FY27 EPS consensus", "$1.62 (n=9; range $1.56-$1.67)", "S&P Global Market Intelligence via StockAnalysis", "Secondary consensus", "updated 9/25/26",
     "stockanalysis.com/stocks/cprt/forecast/ (verified 10/2/26)", "Exact ACV treatment not disclosed"),
    ("Consensus EPS FY27 (cross-check)", "$1.75 (n=8)", "Yahoo Finance", "Secondary consensus", "10/1/26", "finance.yahoo.com/quote/CPRT/analysis", "Staleness cross-check only; not used"),
    ("Sell-side commentary", "Loss 'temporary'; further near-term declines", "HSBC note as reported by Investing.com", "Secondary consensus", "9/17/26",
     "Investing.com news summary of the HSBC note (named secondary source)", "Context only; not in formulas"),
    ("Core ROIC; net-income CAGR", "~29% (FY26), ~31% (FY25); FY21-FY26 CAGR ~9.7%", "Team calculation from 10-K / 8-K data and SEC XBRL", "Derived", "10/2/26",
     "data.sec.gov/api/xbrl/companyfacts/CIK0000900075.json", "ROIC = operating income × (1 − tax) / (equity − cash − HTM)"),
    ("Scenario drivers, probabilities, ROIC, growth, FY28 ACV", "See Scenarios", "Team model", "Team estimate", "10/2/26", "This workbook (Scenarios)", "Rationale rows on Scenarios"),
    ("Operating structure; horizon cash", "See Inputs", "Team model (basis on Inputs)", "Team estimate", "10/2/26", "This workbook (Inputs)", ""),
    ("Beta 0.90; ERP 5%; terminal growth 3%", "See Inputs", "Team model (basis on Inputs)", "Team estimate", "10/2/26", "This workbook (Inputs)", ""),
    ("Post-earnings-reaction study", "3M excess +4.6% / +6.0% / +6.9% (n = 21 / 12 / 8)", "Team backtest (point-in-time)", "Team estimate", "10/2/26",
     "This workbook (Checks: study design and results)", "Basis for the planned exit after Q2"),
]
for i, row_ in enumerate(SRC, start=5):
    put(Z, f"A{i}", i - 4)
    for k, v in enumerate(row_):
        put(Z, f"{get_column_letter(2 + k)}{i}", v, wrap=True)
    for cc in range(1, 9):
        Z.cell(i, cc).border = ROW_LINE

# ================================================================== Checks
X = wb.create_sheet("Checks")
ws_setup(X, {"A": 56, "B": 12, "C": 12, "D": 12, "E": 12, "F": 12, "G": 12})
title(X, "Model checks")
section(X, 3, "Calibration: zero-growth replay of FY26 vs reported diluted EPS (FY26 quarterly diluted shares)", 6)
header(X, 4, ["Quarter", "Q1", "Q2", "Q3", "Q4", "FY26"])
put(X, "A5", "Model replay ($/sh)")
put(X, "A6", "Reported ($/sh)")
put(X, "A7", "Difference ($/sh)")
for q in range(4):
    c = get_column_letter(2 + q)
    g = lambda k: f"Inputs!{c}${SEG[k]}"
    us = f"({g('us_service')}+{g('us_vehicle')}-{g('us_cogs_vehicle')}-{g('us_facility')}-{g('us_ga')})"
    put(X, f"{c}5", f"=({us}+{g('intl_oi')}+{g('interest')})*(1-{NM['tax']})/{g('sh26')}", USD, align="right")
    put(X, f"{c}6", f"=Inputs!{c}${SEG['eps26']}", USD, F_LINK, align="right")
    put(X, f"{c}7", f"={c}5-{c}6", USD, align="right")
for rr in (5, 6, 7):
    put(X, f"F{rr}", f"=SUM(B{rr}:E{rr})", USD, F_BOLD, align="right")
put(X, "A8", "Model excludes certain other income / FX / NCI items; the FY26 replay differs from reported EPS by the amount shown in F7.", font=F_NOTE)
section(X, 10, "Integrity", 6)
CHK = [
    ("Scenario probabilities sum to 100%", f'=IF(ABS(Scenarios!B{P["probcheck"]}-1)<0.0001,"OK","CHECK")'),
    ("Cost of equity exceeds terminal growth, base and stress", f'=IF(AND({NM["coe"]}>{NM["gT"]},{NM["coe_stress"]}>{NM["gT"]}),"OK","CHECK")'),
    ("Sensitivity engine base case = Valuation W2 value", f'=IF(ABS({TS["eng_base"]}-Valuation!C{VR["val"]})<0.000001,"OK","CHECK")'),
    ("Sensitivity engine base FY27 EPS = EPS_Build W2", f'=IF(ABS({TS["eng_base_fy27"]}-{EPSX[1]})<0.000001,"OK","CHECK")'),
    ("FY27 GAAP EPS = ex-ACV EPS + ACV impact (all worlds)",
     '=IF(' + "+".join(f'ABS(Valuation!{get_column_letter(2 + j)}{VR["eps27g"]}-Valuation!{get_column_letter(2 + j)}{VR["eps27x"]}-Valuation!{get_column_letter(2 + j)}{VR["acv27"]})' for j in range(4)) + '<0.000001,"OK","CHECK")'),
    ("Lost-customer reconciliation: W2 share in Q4 FY26 base between 0% and 100%", f'=IF(AND({NM["w2share"]}>0,{NM["w2share"]}<=1),"OK","CHECK")'),
    ("ACV consolidated share of Q2 between 0% and 100%", f'=IF(AND({NM["acv_frac"]}>=0,{NM["acv_frac"]}<=1),"OK","CHECK")'),
]
for i, (lab, f) in enumerate(CHK, start=11):
    put(X, f"A{i}", lab)
    put(X, f"B{i}", f, align="right")
ev = 11 + len(CHK) + 1
section(X, ev, "Post-earnings-reaction study (holding-period discipline)", 6)
EVD = [
    ("Sample period", "CPRT earnings releases Sep 2004 - Sep 2026 (89 releases); Feb 2020 - Jun 2023 excluded (COVID distortions)"),
    ("Event definition", "2-day excess reaction vs SPY, close(t+1) / close(t−1), around the earnings-release 8-K date; a price reaction, not an EPS miss vs consensus"),
    ("Thresholds tested", "Excess reaction ≤ −3%, ≤ −5%, ≤ −7%"),
    ("Benchmark / forward window", "SPY; excess return from the close of day t+1 over 21 / 63 / 126 trading days (1M / 3M / 6M)"),
    ("Source", "Team backtest (scripts/backtest.py); prices: Yahoo Finance; dates: SEC 8-K filing dates"),
]
for i, (a, b) in enumerate(EVD, start=ev + 1):
    put(X, f"A{i}", a)
    put(X, f"B{i}", b)
er = ev + len(EVD) + 2
header(X, er, ["Threshold (2-day excess)", "Events", "n (with 3M)", "1M mean", "3M mean", "3M median", "3M % > 0"])
EVR = [("≤ −3%", 22, 21, -0.004, 0.046, 0.033, 0.71), ("≤ −5%", 13, 12, -0.010, 0.060, 0.067, 0.75), ("≤ −7%", 8, 8, -0.018, 0.069, 0.053, 0.75)]
for i, row_ in enumerate(EVR, start=er + 1):
    put(X, f"A{i}", row_[0])
    put(X, f"B{i}", row_[1], "0", F_IN, align="right")
    put(X, f"C{i}", row_[2], "0", F_IN, align="right")
    for k, v in enumerate(row_[3:]):
        put(X, f"{get_column_letter(4 + k)}{i}", v, PCT, F_IN, align="right")
put(X, f"A{er + 4}", "6M mean excess: +3.6% / +4.4% / +4.2%. Positive 3M drift after large negative reactions argues against holding the short past Q2.", font=F_NOTE)
