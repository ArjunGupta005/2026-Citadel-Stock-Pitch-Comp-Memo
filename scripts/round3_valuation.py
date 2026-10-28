"""Round-3 valuation of the FROZEN cards in thesis/round3/01_frozen_hypothesis_cards.md.

Runs only after the cards were hashed (03_research_log.md). Does not edit the cards.
For each card: KPI-driven bear / base / bull worlds -> EPS (or EBITDA / FCF) -> multiple -> target -> return.
Applies the LOCKED rules unchanged: R1 (gap vs consensus), R5 (base gain >= 2.0x adverse loss AND EV >= +10%,
25/50/25), R8 (share of the move from the multiple). Backtests are a kill check only: post-earnings-reaction drift
in the card's holding direction at -3/-5/-7% (or +3/+5/+7%) thresholds; a robust opposite sign (all three thresholds,
n >= 8 at the central one) is flagged as R4 contradiction. Positive small-n results are not counted as support.

Output: thesis/round3/02_valuation.md
"""

import numpy as np
import pandas as pd

import backtest as bt
from common import PROCESSED, ROOT, prices

W = {"bear": 0.25, "base": 0.50, "bull": 0.25}
L = []
FX_USD_PER_EUR = 1 / 0.8756  # SPOT 6-K Q2-26 close rate


def p(s=""):
    L.append(s)
    print(s)


def table(rows, cols):
    p("| " + " | ".join(cols) + " |")
    p("|" + "---|" * len(cols))
    for r in rows:
        p("| " + " | ".join(f"{r[c]:.3f}" if isinstance(r[c], (float, np.floating)) else str(r[c]) for c in cols) + " |")


def r5(ret, side):
    gain = side * ret["base"]
    adverse = side * (ret["bear"] if side > 0 else ret["bull"])
    ev = side * sum(W[k] * ret[k] for k in W)
    ratio = gain / -adverse if adverse < 0 else np.inf
    return ratio, ev, "PASS" if (ratio >= 2.0 and ev >= 0.10) else "FAIL"


def r8(base_target, price, eps_now, eps_h, mult_now, mult_h):
    tot = np.log(base_target / price)
    m = np.log(mult_h / mult_now)
    return m / tot if abs(tot) > 1e-9 else np.nan


def drift_check(ticker, side):
    """Post-earnings-reaction drift in the holding direction. side -1: after negative reactions; +1: after positive."""
    r = pd.read_csv(PROCESSED / "earnings_reactions.csv", parse_dates=["date"])
    r = r[r.ticker == ticker]
    spy = prices("SPY")["Close"]
    out = []
    for thr in (0.03, 0.05, 0.07):
        sel = r[(r.excess <= -thr)] if side < 0 else r[(r.excess >= thr)]
        dates = [d for d in sel["date"] if not (bt.COVID[0] <= d <= bt.COVID[1])]
        df = bt.fwd_excess(ticker, spy, dates)
        row = {"thr": f"{'-' if side < 0 else '+'}{thr:.0%}", "n": len(df)}
        for h in ("3M", "6M"):
            x = df[h].dropna() if h in df else pd.Series(dtype=float)
            row[f"{h}_mean"] = x.mean() if len(x) else np.nan
            row[f"{h}_n"] = len(x)
        out.append(row)
    d = pd.DataFrame(out)
    central_n = d.loc[1, "3M_n"]
    opposite = {h: all((v * side) < 0 for v in d[f"{h}_mean"].dropna()) and d[f"{h}_mean"].notna().sum() == 3
                for h in ("3M", "6M")}
    verdict = "ROBUST CONTRADICTION (R4)" if (any(opposite.values()) and central_n >= 8) else "no robust contradiction"
    return d, verdict


def card(cid, ticker, side, price, worlds, eps_fn, cons, horizon_fn, mult_now, unit="EPS"):
    p(f"## {cid} ({'LONG' if side > 0 else 'SHORT'} {ticker}, price ${price:.2f})")
    rows = []
    for k, w in worlds.items():
        x = eps_fn(w)
        h_metric, mult, target = horizon_fn(w, x)
        rows.append({"world": k, **{kk: vv for kk, vv in w.items() if not kk.startswith("_")}, f"FY27_{unit}": x,
                     "horizon_metric": h_metric, "multiple": mult, "target": target, "return": target / price - 1, "prob": W[k]})
    cols = list(rows[0].keys())
    table(rows, cols)
    ret = {r["world"]: r["return"] for r in rows}
    ratio, ev, v = r5(ret, side)
    base = next(r for r in rows if r["world"] == "base")
    gap = base[f"FY27_{unit}"] / cons - 1 if cons else np.nan
    share_mult = r8(base["target"], price, None, None, mult_now, base["multiple"])
    p(f"- Consensus FY27 {unit}: {cons} → base gap {gap:+.1%} (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)")
    p(f"- R5: ratio {ratio:.2f}x, EV {ev:+.1%} → **{v}**")
    p(f"- R8: share of base-case move from the multiple: {share_mult:.0%} (fails if > 50%)" if np.isfinite(share_mult) else "- R8: n/a")
    d, verdict = drift_check(ticker, side)
    p(f"- Kill check (post-reaction drift, holding direction, vs SPY): {verdict}")
    p("  " + "; ".join(f"{r.thr}: n={r.n}, 3M {r['3M_mean']:+.1%}, 6M {r['6M_mean']:+.1%}" for _, r in d.iterrows()))
    p()
    return dict(card=cid, ticker=ticker, side="LONG" if side > 0 else "SHORT", gap=gap, ratio=ratio, ev=ev, R5=v,
                R8=share_mult, R4=verdict, bear=ret["bear"], base=ret["base"], bull=ret["bull"])


# ------------------------------------------------------------------ ADBE (FY = Dec-Nov; non-GAAP; horizon NTM ≈ FY28)
ADBE_FY26 = dict(rev=26.60, margin=0.45, tax=0.18, shares=400.9)  # calibrates to FY26 EPS 24.48
ADBE_W = {
    # g = FY27 revenue growth (tracks the ARR target), m = non-GAAP op margin, s = avg share-count change,
    # g28 = FY28 EPS growth, pe = NTM P/E. Anchors: today 8.7x NTM; own trailing GAAP P/E at the 1st pctile (13.1x vs 50x median).
    "bear": dict(g=0.065, m=0.44, s=-0.050, g28=0.08, pe=7.0),
    "base": dict(g=0.085, m=0.45, s=-0.065, g28=0.11, pe=8.7),
    "bull": dict(g=0.100, m=0.455, s=-0.075, g28=0.14, pe=11.0),
}


def adbe_eps(w):
    return ADBE_FY26["rev"] * (1 + w["g"]) * w["m"] * (1 - ADBE_FY26["tax"]) * 1000 / (ADBE_FY26["shares"] * (1 + w["s"]))


def adbe_h(w, e):
    e28 = e * (1 + w["g28"])
    return e28, w["pe"], e28 * w["pe"]


# ------------------------------------------------------------------ ABNB (calendar FY; GAAP; ~600m diluted shares)
ABNB_FY26 = dict(rev=14.17, take=0.134, nm=0.225, shares=600.0)
ABNB_W = {
    # gbv = GBV growth, dt = take-rate change (pts), nm = net margin, g28, pe. Anchors: today 25.9x NTM; trailing 35.6x (58th pctile, short history).
    "bear": dict(gbv=0.10, dt=-0.003, nm=0.215, g28=0.09, pe=21.0),
    "base": dict(gbv=0.115, dt=0.000, nm=0.225, g28=0.12, pe=24.0),
    "bull": dict(gbv=0.13, dt=0.001, nm=0.235, g28=0.15, pe=28.0),
}


def abnb_eps(w):
    rev = ABNB_FY26["rev"] * (1 + w["gbv"]) * (ABNB_FY26["take"] + w["dt"]) / ABNB_FY26["take"]
    return rev * w["nm"] * 1000 / (ABNB_FY26["shares"] * 0.96)


def abnb_h(w, e):
    e28 = e * (1 + w["g28"])
    return e28, w["pe"], e28 * w["pe"]


# ------------------------------------------------------------------ SPOT (EUR; calendar FY)
SPOT_FY26 = dict(rev=19.53, fin=0.35, tax=0.20, shares=210.0)
SPOT_W = {
    # g = revenue growth, gm = gross margin, opex = opex % revenue, g28, pe (on USD-converted EPS). Today 28.1x NTM.
    "bear": dict(g=0.13, gm=0.332, opex=0.176, g28=0.18, pe=23.0),
    "base": dict(g=0.14, gm=0.340, opex=0.172, g28=0.22, pe=27.0),
    "bull": dict(g=0.15, gm=0.348, opex=0.166, g28=0.25, pe=31.0),
}


def spot_eps(w):
    rev = SPOT_FY26["rev"] * (1 + w["g"])
    oi = rev * (w["gm"] - w["opex"])
    return (oi + SPOT_FY26["fin"]) * (1 - SPOT_FY26["tax"]) * 1000 / SPOT_FY26["shares"]


def spot_h(w, e):
    e28 = e * (1 + w["g28"])
    return e28, w["pe"], e28 * FX_USD_PER_EUR * w["pe"]


# ------------------------------------------------------------------ GEV (EV/EBITDA on 2028E; Street FY27 revenue already $52.8bn)
GEV = dict(shares=262.0, net_cash_ye27=18.0)
GEV_W = {
    # rev28 ($bn), m28 = adj. EBITDA margin, ev = EV/EBITDA on 2028E. Today EV $245bn / base 2028E EBITDA $11.6bn ≈ 21x.
    "bear": dict(rev28=54.0, m28=0.18, ev=17.0),
    "base": dict(rev28=58.0, m28=0.20, ev=21.0),
    "bull": dict(rev28=62.0, m28=0.22, ev=24.0),
}


def gev_ebitda(w):
    return w["rev28"] * w["m28"]


def gev_h(w, e):
    eq = e * w["ev"] + GEV["net_cash_ye27"]
    return e, w["ev"], eq * 1000 / GEV["shares"]


# GEV-2: equity priced on FY27 FCF at today's P/FCF (market cap $263bn / FY26 FCF guide midpoint $12bn ≈ 21.9x)
GEV2_W = {
    "bear": dict(fcf27=13.0, pfcf=21.9),   # bear for the STOCK? no: for a short, "bull" world = deposits keep surging
    "base": dict(fcf27=10.0, pfcf=21.9),
    "bull": dict(fcf27=14.0, pfcf=23.0),
}
# Re-label so 'bear' = worst for the stock (thesis-confirming world for a short)
GEV2_W = {"bear": dict(fcf27=8.0, pfcf=19.0), "base": dict(fcf27=10.5, pfcf=21.9), "bull": dict(fcf27=13.5, pfcf=21.9)}


def gev2_fcf(w):
    return w["fcf27"]


def gev2_h(w, f):
    return f, w["pfcf"], f * w["pfcf"] * 1000 / GEV["shares"]


def main():
    p("# Round 3 — Valuation of the frozen cards (scripts/round3_valuation.py)")
    p()
    p("Cards frozen before this file was generated (SHA-256 in 03_research_log.md). Locked rules unchanged. "
      "Worlds are economic worlds shared by every card on the same stock; each card is tested in its own direction.")
    p()
    res = []
    for cid, side in (("ADBE-1", -1), ("ADBE-2", +1)):
        res.append(card(cid, "ADBE", side, 241.28, ADBE_W, adbe_eps, 27.67, adbe_h, 8.7))
    res.append(card("ABNB-1", "ABNB", -1, 160.47, ABNB_W, abnb_eps, 6.24, abnb_h, 25.9))
    res.append(card("SPOT-1", "SPOT", -1, 491.40, SPOT_W, spot_eps, 15.41, spot_h, 28.1))
    p("GEV note: Street FY27 revenue ($52.8bn) already exceeds management's 2028 target ($52bn), so the base world "
      "assumes a raise to about $58bn. A 'raise' alone is consensus-confirming (R10 risk).")
    res.append(card("GEV-1", "GEV", +1, 987.45, GEV_W, gev_ebitda, None, gev_h, 21.0, unit="2028_EBITDA_bn"))
    p("GEV-2 note: FCF changes from customer deposits do not change EPS or EBITDA. The only price channel is the market "
      "capitalising FCF (P/FCF). That is a multiple / narrative channel by construction.")
    res.append(card("GEV-2", "GEV", -1, 987.45, GEV2_W, gev2_fcf, 12.0, gev2_h, 21.9, unit="FCF_bn"))
    s = pd.DataFrame(res)
    s.to_csv(ROOT / "thesis" / "round3" / "valuation_summary.csv", index=False)
    p("## Summary")
    table(s.to_dict("records"), ["card", "side", "gap", "bear", "base", "bull", "ratio", "ev", "R5", "R8", "R4"])
    (ROOT / "thesis" / "round3" / "02_valuation.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()


# ================================================================== construction v2 (Round-1-consistent)
# Correction made after the first run, applied identically to every card: each card's BASE world = the card's frozen
# "expected if true" central values, with the multiple held at today's NTM level (as in Round 1); bear/bull are the
# adverse/favorable worlds around it. The shared-world run above is kept for transparency.
V2 = {
    "ADBE-1": ("ADBE", -1, 241.28, adbe_eps, adbe_h, 27.67, 8.7, {
        "bear": dict(g=0.060, m=0.440, s=-0.050, g28=0.07, pe=7.0),
        "base": dict(g=0.075, m=0.445, s=-0.065, g28=0.08, pe=8.7),   # FY27 ARR target ≤8% (card)
        "bull": dict(g=0.100, m=0.455, s=-0.075, g28=0.14, pe=11.0)}),
    "ADBE-2": ("ADBE", +1, 241.28, adbe_eps, adbe_h, 27.67, 8.7, {
        "bear": dict(g=0.065, m=0.440, s=-0.040, g28=0.07, pe=7.0),
        "base": dict(g=0.080, m=0.450, s=-0.070, g28=0.12, pe=8.7),   # buyback ≥6-7%/yr, EPS ≥ +12% (card)
        "bull": dict(g=0.100, m=0.455, s=-0.080, g28=0.14, pe=11.0)}),
    "ABNB-1": ("ABNB", -1, 160.47, abnb_eps, abnb_h, 6.24, 25.9, {
        "bear": dict(gbv=0.095, dt=-0.004, nm=0.210, g28=0.08, pe=21.0),
        "base": dict(gbv=0.110, dt=-0.003, nm=0.220, g28=0.10, pe=25.9),  # take rate down ~30bp (card)
        "bull": dict(gbv=0.130, dt=0.001, nm=0.235, g28=0.15, pe=29.0)}),
    "SPOT-1": ("SPOT", -1, 491.40, spot_eps, spot_h, 15.41, 28.1, {
        "bear": dict(g=0.125, gm=0.330, opex=0.178, g28=0.16, pe=23.0),
        "base": dict(g=0.140, gm=0.333, opex=0.174, g28=0.18, pe=28.1),  # GM plateau ~33.3% (card)
        "bull": dict(g=0.150, gm=0.348, opex=0.166, g28=0.25, pe=32.0)}),
    "GEV-1": ("GEV", +1, 987.45, gev_ebitda, gev_h, None, 21.1, {
        "bear": dict(rev28=52.0, m28=0.20, ev=18.0),    # targets merely reaffirmed (card: false)
        "base": dict(rev28=60.0, m28=0.21, ev=21.1),    # raise beyond the Street path (card: true)
        "bull": dict(rev28=64.0, m28=0.22, ev=24.0)}),
    "GEV-2": ("GEV", -1, 987.45, gev2_fcf, gev2_h, 12.0, 21.9, {
        "bear": dict(fcf27=7.0, pfcf=19.0),
        "base": dict(fcf27=9.0, pfcf=21.9),             # FY27 FCF guide below $12bn (card)
        "bull": dict(fcf27=13.5, pfcf=21.9)}),
}


def main_v2():
    global L
    L = []
    p("# Round 3 — Valuation v2 (each card's base = its frozen 'expected if true' case; multiple held at today's NTM)")
    p()
    res = []
    for cid, (tk, side, px, fn, hfn, cons, mnow, worlds) in V2.items():
        unit = "2028_EBITDA_bn" if cid == "GEV-1" else ("FCF_bn" if cid == "GEV-2" else "EPS")
        res.append(card(cid, tk, side, px, worlds, fn, cons, hfn, mnow, unit=unit))
    s = pd.DataFrame(res)
    s.to_csv(ROOT / "thesis" / "round3" / "valuation_summary_v2.csv", index=False)
    p("## Summary (v2)")
    table(s.to_dict("records"), ["card", "side", "gap", "bear", "base", "bull", "ratio", "ev", "R5", "R8", "R4"])
    (ROOT / "thesis" / "round3" / "02b_valuation_v2.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main_v2()
