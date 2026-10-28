"""Audit of the scenario engine: calibration, full world builds, consensus-gap decomposition,
multiple sensitivity, evidence-based multiple anchor and breakeven diagnostics.

Locked hurdle (04_restart_criteria_locked.md R5, NOT changed here): base gain / adverse loss >= 2.0x AND
probability-weighted return >= +10% in the thesis direction, weights 25/50/25 (bear/base/bull).

Output: audit/scenario_audit.md

Usage: python audit_scenarios.py
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

import scenario_engine as se
from common import PROCESSED, ROOT

W = se.WEIGHTS
LINES = []


def p(s=""):
    LINES.append(s)
    print(s)


def r5(returns, side):
    """returns: dict world -> stock return. side +1 long, -1 short."""
    gain = side * returns["base"]
    adverse = side * (returns["bear"] if side > 0 else returns["bull"])
    ev = side * sum(W[k] * returns[k] for k in W)
    ratio = gain / -adverse if adverse < 0 else np.inf
    ok = ratio >= 2.0 and ev >= 0.10
    return ratio, ev, "PASS" if ok else "FAIL"


def table(df):
    p("| " + " | ".join([df.index.name or ""] + [str(c) for c in df.columns]) + " |")
    p("|" + "---|" * (len(df.columns) + 1))
    for i, row in df.iterrows():
        cells = []
        for v in row:
            cells.append(f"{v:.3f}" if isinstance(v, (float, np.floating)) else str(v))
        p(f"| {i} | " + " | ".join(cells) + " |")


# ------------------------------------------------------------------ CPRT
def cprt_audit():
    p("## CPRT")
    cal = se.cprt_quarters(se.CPRT_WORLDS["base"], calibrate=True)
    actual = [0.41, 0.36, 0.43, 0.35]
    p("### Calibration: zero-growth FY26 replay vs reported GAAP diluted EPS (10-Q / 10-K)")
    c = pd.DataFrame({"model": [r["eps"] for r in cal], "reported": actual}, index=["Q1", "Q2", "Q3", "Q4"])
    c["error"] = c["model"] - c["reported"]
    c.index.name = "FY26"
    table(c)
    p(f"FY26 model {c['model'].sum():.3f} vs reported 1.55; error {c['model'].sum() - 1.55:+.3f} "
      "(other income/FX and non-controlling interest are not modelled).")
    p()
    rows = []
    for name, w in se.CPRT_WORLDS.items():
        qs = se.cprt_quarters(w)
        x = se.cprt_quarters(w, include_acv=False)
        rev = sum(r["us_service"] + r["us_vehicle_rev"] for r in qs)
        oi = sum(r["us_oi"] + r["intl_oi"] for r in qs)
        fy27, fy27x = sum(r["eps"] for r in qs), sum(r["eps"] for r in x)
        fy28 = fy27 * (1 + w["g28"])
        tgt = fy28 * w["pe"]
        rows.append(dict(world=name, US_ins_units_Q1_Q3=w["u"] + w["loss"], RPU=w["rpu"], fixed_cost_g=w["fixed"],
                         US_rev_ex_intl_m=rev, op_income_ex_ACV_m=oi, FY27_EPS=fy27, FY27_EPS_exACV=fy27x,
                         FY28_EPS=fy28, PE=w["pe"], target=tgt, ret=tgt / se.PRICE["CPRT"] - 1, prob=W[name]))
    df = pd.DataFrame(rows).set_index("world")
    p("### World builds (FY27 = Aug-26 to Jul-27; GAAP; 940m diluted shares; 19.5% tax)")
    table(df)
    ret = df["ret"].to_dict()
    for side, lab in ((-1, "SHORT"), (1, "LONG")):
        ratio, ev, v = r5(ret, side)
        p(f"- {lab}: R5 ratio {ratio:.2f}x, EV {ev:+.1%} → **{v}**")
    p()
    # consensus gap, by provider value and with/without ACV
    p("### Consensus gap (FY27 EPS)")
    base, basex = df.loc["base", "FY27_EPS"], df.loc["base", "FY27_EPS_exACV"]
    g = []
    for src, v in (("Yahoo mean (n=8, pulled 2026-10-01)", 1.75062), ("Yahoo low", 1.61919), ("Yahoo high", 1.83),
                   ("Secondary aggregator mean (press)", 1.69), ("Secondary (Barchart, press)", 1.66)):
        g.append(dict(source=src, consensus=v, our_incl_ACV=base, gap_incl=base / v - 1, our_ex_ACV=basex, gap_ex=basex / v - 1))
    gg = pd.DataFrame(g).set_index("source")
    table(gg)
    p()
    # Q2 check against the only correctly-dated quarterly estimate
    q2 = se.cprt_quarters(se.CPRT_WORLDS["base"])[1]["eps"]
    q2x = se.cprt_quarters(se.CPRT_WORLDS["base"], include_acv=False)[1]["eps"]
    p(f"Q2-FY27 (Nov-Jan): Street $0.375 (period end 2027-01-31) vs our base ${q2:.3f} incl. ACV ({q2 / 0.37454 - 1:+.1%}), "
      f"${q2x:.3f} ex-ACV ({q2x / 0.37454 - 1:+.1%}).")
    _, implied = se.cprt()
    for k, v in implied.items():
        p(f"- {k}: {v:+.1%}")
    p()
    # multiple sensitivity: what if the multiple is held at today's level in every world?
    p("### Multiple sensitivity (diagnostic; the locked worlds are unchanged)")
    sens = []
    for bull_pe in (15.6, 17, 18, 19, 20, 21):
        r = {k: df.loc[k, "FY28_EPS"] * (bull_pe if k == "bull" else df.loc[k, "PE"]) / se.PRICE["CPRT"] - 1 for k in W}
        ratio, ev, v = r5(r, -1)
        sens.append(dict(bull_PE=bull_pe, bull_ret=r["bull"], short_ratio=ratio, short_EV=ev, verdict=v))
    s = pd.DataFrame(sens).set_index("bull_PE")
    table(s)
    p()
    return df


def cprt_multiple_anchor():
    """Evidence for the bull multiple: historical trailing P/E vs the EPS growth that actually followed (in-sample)."""
    v = pd.read_csv(PROCESSED / "CPRT_valuation_history.csv", index_col=0, parse_dates=True)
    m = v.resample("ME").last()
    m["fwd_eps_g"] = m["ttm_eps"].shift(-12) / m["ttm_eps"] - 1
    d = m.loc["2012":, ["pe", "fwd_eps_g"]].dropna()
    d = d[(d.pe > 0) & (d.pe < 80)]
    fit = sm.OLS(d["pe"], sm.add_constant(d["fwd_eps_g"])).fit()
    p("### Evidence anchor for CPRT multiples: trailing P/E regressed on realized next-12m EPS growth (monthly, 2012-2025)")
    p(f"P/E = {fit.params['const']:.1f} + {fit.params['fwd_eps_g']:.1f} x growth (R² {fit.rsquared:.2f}, n={len(d)}; "
      "overlapping months, descriptive only).")
    for g in (0.04, 0.12, 0.18):
        p(f"- growth {g:.0%} → fitted P/E {fit.params['const'] + fit.params['fwd_eps_g'] * g:.1f}x")
    p("These fitted multiples come from a 2012-2025 regime of 10-20% EPS growth and zero-to-low rates. "
      "They are an upper reference, not a forecast.")
    p()


# ------------------------------------------------------------------ NCLH
def nclh_audit():
    p("## NCLH")
    calib, _ = se.nclh_fy27(dict(cap=0, ny=0, ncc=0, fuel=0))
    p(f"Calibration: model FY26 EBITDA ${calib:,.0f}m vs guide ~$2,500m ({calib / 2500 - 1:+.1%}). "
      "The model is ~1.8% high, so it slightly flatters EPS (~$0.10).")
    rows = []
    for name, w in se.NCLH_WORLDS.items():
        e, eps = se.nclh_fy27(w)
        cd = se.NCLH_FY26["cd"] * (1 + w["cap"])
        agm = se.NCLH_FY26["net_yield"] * (1 + w["ny"]) * cd
        e28 = e * (1 + w["g28"])
        tgt = (e28 * w["ev_mult"] / 1000 - w["nd"]) * 1000 / se.NCLH_SHARES
        rows.append(dict(world=name, capacity_g=w["cap"], net_yield_g=w["ny"], ncc_g=w["ncc"], fuel_px_g=w["fuel"],
                         net_rev_m=agm, EBITDA_m=e, EBITDA_margin_on_net_rev=e / agm, FY27_adjEPS=eps,
                         EV_EBITDA=w["ev_mult"], net_debt_bn=w["nd"], target=tgt, ret=tgt / se.PRICE["NCLH"] - 1, prob=W[name]))
    df = pd.DataFrame(rows).set_index("world")
    p("### World builds (FY27 = calendar 2027; adjusted EPS; 462m shares; interest $870m per 8-K 9/30)")
    table(df)
    ret = df["ret"].to_dict()
    for side, lab in ((1, "LONG"), (-1, "SHORT")):
        ratio, ev, v = r5(ret, side)
        p(f"- {lab}: R5 ratio {ratio:.2f}x, EV {ev:+.1%} → **{v}**")
    p(f"- Gap: our base FY27 adj. EPS {df.loc['base', 'FY27_adjEPS']:.2f} vs Street 1.67 ({df.loc['base', 'FY27_adjEPS'] / 1.67 - 1:+.1%}).")
    p()
    return df


# ------------------------------------------------------------------ breakeven
def breakeven(name, price, df, side, eps_col, mult_col, conv=None):
    """What would have to change for R5 to pass (diagnostic; hurdle unchanged).

    conv: function (eps, multiple) -> price. Defaults to eps * multiple.
    """
    conv = conv or (lambda e, m: e * m)
    ret = df["ret"].to_dict()
    adverse_key = "bear" if side > 0 else "bull"
    adverse = side * ret[adverse_key]
    base = side * ret["base"]
    p(f"### Breakeven diagnostics: {name} {'LONG' if side > 0 else 'SHORT'} (hurdle unchanged)")
    req_gain = 2 * max(-adverse, 0)
    req_price = price * (1 + side * req_gain)
    be, bm = df.loc["base", eps_col], df.loc["base", mult_col]
    p(f"- Required base-case price for 2.0x with today's adverse case ({adverse:+.1%}): ${req_price:.2f} "
      f"({side * req_gain:+.1%} vs base ${df.loc['base', 'target']:.2f})")
    if conv is None or True:
        if name != "NCLH":
            p(f"- Required base EPS at base multiple {bm:.1f}x: ${req_price / bm:.3f} (vs ${be:.3f}; {req_price / bm / be - 1:+.1%})")
            p(f"- Required base multiple at base EPS ${be:.3f}: {req_price / be:.1f}x (vs {bm:.1f}x)")
    p(f"- Required adverse-case floor for 2.0x with today's base case ({base:+.1%}): adverse loss ≤ {base / 2:.1%} "
      f"→ adverse price {'≤' if side < 0 else '≥'} ${price * (1 - side * base / 2):.2f} (vs ${df.loc[adverse_key, 'target']:.2f})")
    # EV requirement
    ev_now = side * sum(W[k] * ret[k] for k in W)
    p(f"- EV now {ev_now:+.1%}; requirement +10%: shortfall {max(0.10 - ev_now, 0):.1%} of probability-weighted return")
    p()


def main():
    p("# Scenario construction audit (generated by scripts/audit_scenarios.py)")
    p()
    c = cprt_audit()
    cprt_multiple_anchor()
    n = nclh_audit()
    breakeven("CPRT", se.PRICE["CPRT"], c, -1, "FY28_EPS", "PE")
    breakeven("NCLH", se.PRICE["NCLH"], n, +1, "FY27_adjEPS", "EV_EBITDA")
    out = ROOT / "audit" / "scenario_audit.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(LINES), encoding="utf-8")


if __name__ == "__main__":
    main()
