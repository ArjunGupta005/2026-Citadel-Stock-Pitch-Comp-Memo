"""Create build_final_model_v3.py from build_final_model_v2.py (surgical v3 QA fixes; v2 script/files untouched)."""
from pathlib import Path

here = Path(__file__).parent
s = (here / "build_final_model_v2.py").read_text(encoding="utf-8")


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)


rep('"""Build final/Margin_Callers_v2.xlsx', '"""Build final/Margin_Callers_v3.xlsx (v3 = surgical QA fixes on v2)')
rep('out = ROOT / "final" / "Margin_Callers_v2.xlsx"', 'out = ROOT / "final" / "Margin_Callers_v3.xlsx"')

# 2. RB Global wording (Scenarios W2 rationale, Sources)
rep("RB Global says the transfer is done;", "RB Global indicated substantial incremental partner volume had been transitioning over the prior ~90 days;")
rep('("RB Global partner expansion", "All 50 states; volume transitioned \'probably over the last 90 days\'"',
    '("RB Global partner expansion", "Incremental volume from its largest automotive-insurance partner had been transitioning over roughly the prior 90 days as of Aug. 4, following expansion to all 50 states"')

# 9. Checks calibration note
rep('put(X, "A8", "Model excludes certain other income / FX / NCI items; the FY26 replay differs from reported EPS by the amount shown in F7.", font=F_NOTE)',
    'put(X, "A8", "Model excludes certain other income / FX / NCI items; FY26 replay differs from reported EPS by approximately $0.01/share (~0.4%; F7).", font=F_NOTE)')

# 6 + 13. Valuation notes (gross short returns; constant horizon cash)
rep('VO["epsonly"] = f"Valuation!$B${re_ + 3}"',
    'VO["epsonly"] = f"Valuation!$B${re_ + 3}"\n'
    'put(V, f"A{re_ + 5}", "Short returns are gross and exclude borrow fees, financing costs and transaction costs.", font=F_NOTE)\n'
    'put(V, f"A{re_ + 6}", "Horizon cash is held constant across scenarios to isolate operating differences; ±$200m of cash changes value by approximately $0.21/share.", font=F_NOTE)')
rep('put(M, "A32", "Colour key: blue = input; black = formula; green = link to another sheet; red = negative.", font=F_NOTE)',
    'put(M, "A32", "Colour key: blue = input; black = formula; green = link to another sheet; red = negative.", font=F_NOTE)\n'
    'put(M, "A26", "Short returns are gross and exclude borrow fees, financing costs and transaction costs.", font=F_NOTE)')

# 5. W2 FY27 EPS bridge (live formulas) on the Sensitivity sheet
BRIDGE = r'''
# ---- W2 FY27 EPS bridge from FY26 reported EPS (cumulative replay; feeds the memo bridge)
row = ENG0 + len(ENG_CASES) + 2
row = tsec(row, "W2 FY27 EPS bridge from FY26 reported EPS (cumulative replay of EPS_Build W2; drivers switched on in order)",
           ["Step", "Underlying u", "Run-rate drag", "Q4 base drag on", "RPU growth", "Fixed cost growth", "Non-ins. growth",
            "Veh. GP / G&A growth", "Intl growth", "FY27 EPS ex-ACV", "Step change"])
BR0 = row
STEPS = [
    ("FY26 reported diluted EPS", None),
    ("FY26 replay at FY27 share count and pre-ACV interest (zero growth)", dict()),
    ("+ lost-customer drag (13-pt run-rate, net of Q4 FY26 base)", dict(L=1, D=1)),
    ("+ underlying insurance and non-insurance unit growth", dict(L=1, D=1, U=1, G=1)),
    ("+ revenue per unit", dict(L=1, D=1, U=1, G=1, R=1)),
    ("+ fixed facility cost growth", dict(L=1, D=1, U=1, G=1, R=1, F=1)),
    ("+ international, vehicle gross profit and G&A growth (= W2)", dict(L=1, D=1, U=1, G=1, R=1, F=1, H=1, I=1)),
]
SRCREF = {"U": sc2("u"), "L": sc2("loss"), "D": "1", "R": sc2("rpu"), "F": sc2("fixed"), "G": NM["nonins"], "H": NM["goth"], "I": NM["gint"]}
for i, (lab, on) in enumerate(STEPS):
    rr = BR0 + i
    put(T, f"A{rr}", lab)
    if on is None:
        put(T, f"J{rr}", f"=SUM(Inputs!B{SEG['eps26']}:E{SEG['eps26']})", USD, F_LINK, align="right")
        continue
    for col, key in zip("BCDEFGHI", "ULDRFGHI"):
        if key in on:
            f = f"={SRCREF[key]}"
            put(T, f"{col}{rr}", f if key != "D" else 1, PCT if key != "D" else "0", F_LINK if key not in ("D",) else F_IN, align="right")
        else:
            put(T, f"{col}{rr}", 0, PCT if key != "D" else "0", F_IN, align="right")
    terms = []
    for q in range(4):
        c = get_column_letter(2 + q)
        g = lambda k: f"Inputs!${c}${SEG[k]}"
        imp = f"((1+$C{rr})/(1-{g('lib')}*$D{rr})-1)"
        units = f"({NM['sins']}*($B{rr}+{imp})+(1-{NM['sins']})*$G{rr})"
        usoi = (f"({g('us_service')}*(1+{units})*(1+$E{rr})+({g('us_vehicle')}-{g('us_cogs_vehicle')})*(1+$H{rr})"
                f"-({g('us_facility')}*{NM['fix']}*(1+$F{rr})+{g('us_facility')}*(1-{NM['fix']})*(1+{units}))-{g('us_ga')}*(1+$H{rr}))")
        terms.append(f"({usoi}+{g('intl_oi')}*(1+$I{rr}))")
    put(T, f"J{rr}", "=(" + "+".join(terms) + f"+4*{NM['intq1']})*(1-{NM['tax']})/{NM['shares']}", USD, F_BOLD if i == 6 else F_BODY, align="right")
    put(T, f"K{rr}", f"=J{rr}-J{rr - 1}", USD, align="right")
row = BR0 + len(STEPS) + 1
row = tsec(row, "Bridge as displayed in the memo ($0.01 precision; small items grouped so the displayed figures sum exactly)", ["Bridge line", "$/sh"])
BD0 = row
DISP = [("FY26 reported diluted EPS", f"=J{BR0}"), ("Share count / interest / other", f"=K{BR0 + 1}+K{BR0 + 6}"),
        ("Lost-customer impact", f"=K{BR0 + 2}"), ("Underlying / non-insurance growth", f"=K{BR0 + 3}"), ("Revenue per unit", f"=K{BR0 + 4}"),
        ("Fixed-facility costs", f"=K{BR0 + 5}"), ("FY27 EPS ex-ACV (W2)", f"=J{BR0 + 6}")]
for i, (lab, f) in enumerate(DISP):
    put(T, f"A{BD0 + i}", lab, font=F_BOLD if i in (0, 6) else F_BODY)
    put(T, f"B{BD0 + i}", f, USD, F_BOLD if i in (0, 6) else F_BODY, align="right")
TS["bridge_end"] = f"Sensitivity!$J${BR0 + 6}"
TS["bridge_disp_ok"] = "+".join(f"ROUND(Sensitivity!$B${BD0 + k},2)" for k in range(6)) + f"-ROUND(Sensitivity!$B${BD0 + 6},2)"
'''
rep('TS["eng_base_fy27"] = f"Sensitivity!$J${ENG[(\'drag\', -0.13, 0.55, 932.0)]}"\n',
    'TS["eng_base_fy27"] = f"Sensitivity!$J${ENG[(\'drag\', -0.13, 0.55, 932.0)]}"\n' + BRIDGE)
rep('''    ("Sensitivity engine base FY27 EPS = EPS_Build W2", f'=IF(ABS({TS["eng_base_fy27"]}-{EPSX[1]})<0.000001,"OK","CHECK")'),''',
    '''    ("Sensitivity engine base FY27 EPS = EPS_Build W2", f'=IF(ABS({TS["eng_base_fy27"]}-{EPSX[1]})<0.000001,"OK","CHECK")'),
    ("EPS bridge ends at EPS_Build W2 FY27 EPS ex-ACV", f'=IF(ABS({TS["bridge_end"]}-{EPSX[1]})<0.000001,"OK","CHECK")'),
    ("Displayed bridge (memo, $0.01) sums exactly", '=IF(ABS(' + TS["bridge_disp_ok"] + ')<0.0001,"OK","CHECK")'),''')

# 4 + 7. Sources: DOJ, company scale, valuation history
rep('''    ("Post-earnings-reaction study", "3M''', '''    ("DOJ AML investigation", "Ongoing investigation; potential outcome/loss not estimable", "Copart FY26 Form 10-K (Note 15 Commitments and Contingencies; Item 1A)",
     "Primary", "9/29/26", "10-K, accession 0001193125-26-405731", "Known legal/regulatory overhang; not modeled in thesis or valuation."),
    ("Company scale", "286 operating facilities; ~1 million members in 185+ countries; 4 million+ vehicles sold a year",
     "Copart FY26 Form 10-K (Item 2 Properties); 8-K Ex. 99.1 (About Copart); Q4 FY26 call", "Primary (vehicles: Secondary transcript)", "9/29/26; 9/10/26",
     "10-K accession 0001193125-26-405731; 8-K accession 0001193125-26-387902", "Memo cites 286 facilities (10-K)"),
    ("Trailing P/E and price de-rating", "~18x trailing P/E vs ~35x 2021-26 median; price −40% from 52-week high ($45.76, 10/21/25)",
     "Team calculation from Yahoo Finance prices and SEC XBRL EPS", "Derived", "10/1/26", "data.sec.gov companyfacts; finance.yahoo.com/quote/CPRT/history",
     "Supports 'the stock has already de-rated materially'"),
    ("Post-earnings-reaction study", "3M''')
(here / "build_final_model_v3.py").write_text(s, encoding="utf-8")
print("ok")
