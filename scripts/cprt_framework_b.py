"""CPRT under Framework B: separate evaluation. Framework A scenarios, frozen assumptions and backtests are NOT modified.

Imports scenario_engine.cprt_quarters (read-only) for the KPI -> EPS mechanics. Adds:
  - a fundamental multiple bridge: two-stage justified P/E on ex-interest EPS from growth, incremental ROIC and the
    cost of equity (rf = current 10y), with net cash valued separately, so no multiple is a free parameter;
  - reverse-engineering of today's price (implied 5-year growth);
  - rate-adjusted historical regimes and peer cross-check;
  - a probability-weighted distribution with explicit maximum plausible loss;
  - return attribution into EPS vs multiple (Framework B "no unexplained multiple change").
Output: framework_B/CPRT_framework_b_numbers.md
"""

import numpy as np
from scipy.optimize import brentq

import scenario_engine as se
from common import ROOT

L = []


def p(s=""):
    L.append(s)
    print(s)


PRICE = 27.29
SHARES = 940.0                       # diluted (m)
CASH_PRE_ACV = 4.7                   # $bn cash + HTM securities (10-K FY26; audit)
CASH_YE_FY27 = 3.5                   # $bn after the $1.9bn ACV payment + ~$0.7bn retained FCF (assumption, stated)
RF = 0.0524                          # 10y UST, 2026-10-01 (^TNX)
BETA = 0.90                          # Phase-10 regression market beta (0.89); Yahoo beta 1.03 as sensitivity
ERP = 0.05
TAX = se.CPRT_TAX


def coe(beta=BETA, rf=RF):
    return rf + beta * ERP


def justified_pe(g5, roic, r, g_term=0.03, years=5):
    """Value of $1 of next-year (ex-interest) EPS: distributions (1 - g/ROIC) over a 5-year growth stage,
    then a Gordon terminal at g_term with the same reinvestment logic."""
    v, e = 0.0, 1.0
    for t in range(1, years + 1):
        v += e * (1 - g5 / roic) / (1 + r) ** t
        e *= 1 + g5
    tv = e * (1 - g_term / roic) / (r - g_term)
    return v + tv / (1 + r) ** years


def interest_eps(int_q):
    return int_q * 4 * (1 - TAX) / SHARES


# ------------------------------------------------------------------ worlds (same EPS mechanics; new valuation bridge)
WORLDS = {
    # name: (probability, EPS-world params for cprt_quarters, FY28 EPS growth, 5y growth after FY28, incremental ROIC)
    "W1 share loss deepens + cost creep": (0.25, se.CPRT_WORLDS["bear"], 0.04, 0.03, 0.15),
    "W2 FY27 trough, FY28 normalises": (0.50, se.CPRT_WORLDS["base"], 0.12, 0.06, 0.20),
    "W3 cycle turns + ACV synergies": (0.25, se.CPRT_WORLDS["bull"], 0.18, 0.09, 0.25),
}


def main():
    r = coe()
    p("# CPRT — Framework B numbers (scripts/cprt_framework_b.py)")
    p()
    p(f"Cost of equity {r:.2%} = 10y {RF:.2%} + β {BETA} × ERP {ERP:.0%}. ROIC: FY26 NOPAT ≈ $1.33bn on ≈ $4.6bn invested capital "
      "≈ 29%; post-ACV ≈ 20% (ACV adds $1.9bn at ~0 NOPAT).")
    p()
    # ---------- reverse engineering of today's price
    ex_cash_price = PRICE - CASH_PRE_ACV * 1000 / SHARES      # ACV is bought with this cash -> treat at cost
    fy26_int = interest_eps(182 / 4)
    p("## 1. What today's price implies")
    p(f"- Price ${PRICE}; cash + securities ${CASH_PRE_ACV}bn = ${CASH_PRE_ACV * 1000 / SHARES:.2f}/sh → ex-cash price ${ex_cash_price:.2f} "
      "(ACV is purchased with this cash, so it is treated as an asset at cost).")
    for lab, eps in (("Street FY27 (Yahoo mean) $1.75", 1.75), ("Street FY27 (press aggregators) $1.67-1.69", 1.68),
                     ("Our base FY27 ex-ACV $1.43", 1.433), ("Our base FY27 incl. ACV $1.35", 1.350)):
        e_x = eps - fy26_int * 0.6  # interest income falls after the ACV cash outflow
        pe = ex_cash_price / e_x
        g_imp = brentq(lambda g: justified_pe(g, 0.20, r) - pe, -0.10, 0.20)
        p(f"- {lab}: ex-cash, ex-interest NTM P/E {pe:.1f}x → implied 5-year EPS growth {g_imp:.1%} "
          f"(incremental ROIC 20%, CoE {r:.1%}, 3% terminal)")
    p("- Historical regimes (trailing GAAP P/E): FY12-17 20-24x at 10y 1.5-2.6% (growth ~10-15%); FY18-24 24-40x at 0.5-4.1%; "
      "now 17.6x at 5.2%.")
    for g, lab in ((0.10, "FY12-17-like growth (10%)"), (0.06, "mid-single-digit growth (6%)"), (0.03, "GDP-like growth (3%)")):
        p(f"  - Fundamental P/E at today's rates for {lab}, incremental ROIC 25%: {justified_pe(g, 0.25, r):.1f}x; "
          f"at FY12-17 rates (10y 2%): {justified_pe(g, 0.25, coe(rf=0.02)):.1f}x")
    p("- Peers (fwd P/E, 2026-10-01, Yahoo): RBA 16.8x (levered, 18% op. margin), OPLN 20.1x, KMX 18.1x; peer median 20.1x. "
      "CPRT is 15.6x on the Yahoo FY27 mean with net cash and a 32-37% operating margin.")
    p()
    # ---------- distribution
    p("## 2. Probability-weighted distribution (12-month horizon, value at Sep-2027 on FY28 NTM EPS)")
    p("| World | Prob. | FY27 EPS (GAAP, incl. ACV) | FY27 ex-ACV | FY28 EPS | FY28 ex-interest | Justified P/E (ex-cash) | "
      "Implied total P/E | Value/sh | Return | Return from EPS | Return from multiple |")
    p("|---|---|---|---|---|---|---|---|---|---|---|---|")
    mkt_pe_ex = ex_cash_price / (1.75 - fy26_int * 0.6)
    rets = {}
    for name, (prob, w, g28, g5, roic) in WORLDS.items():
        fy27 = sum(q["eps"] for q in se.cprt_quarters(w))
        fy27x = sum(q["eps"] for q in se.cprt_quarters(w, include_acv=False))
        fy28 = fy27 * (1 + g28)
        fy28_x = fy28 - interest_eps(w["int_q"])
        jpe = justified_pe(g5, roic, r)
        val = jpe * fy28_x + CASH_YE_FY27 * 1000 / SHARES
        ret = val / PRICE - 1
        rets[name] = (prob, ret)
        # attribution vs today: ex-cash EPS change (Street FY27 ex-int -> our FY28 ex-int) and multiple change (market 14x -> justified)
        eps_part = np.log(fy28_x / (1.75 - fy26_int * 0.6))
        mult_part = np.log(jpe / mkt_pe_ex)
        p(f"| {name} | {prob:.2f} | {fy27:.2f} | {fy27x:.2f} | {fy28:.2f} | {fy28_x:.2f} | {jpe:.1f}x | {val / fy28:.1f}x | "
          f"${val:.2f} | {ret:+.1%} | {eps_part:+.1%} (log) | {mult_part:+.1%} (log) |")
    ev = sum(pr * rt for pr, rt in rets.values())
    p()
    p(f"- Market ex-cash NTM P/E today (Yahoo FY27): {mkt_pe_ex:.1f}x")
    p(f"- **Probability-weighted return: {ev:+.1%}** (long direction) → short expected return {-ev:+.1%}")
    worst_short = max(rt for _, rt in rets.values())
    worst_long = min(rt for _, rt in rets.values())
    p(f"- Maximum plausible loss: SHORT {worst_short:+.1%} (W3); LONG {worst_long:+.1%} (W1)")
    # stress: W3 EPS with a FY12-17 regime multiple (rates fall to ~3.5%)
    w3 = WORLDS["W3 cycle turns + ACV synergies"]
    fy28_x3 = sum(q["eps"] for q in se.cprt_quarters(w3[1])) * (1 + w3[2]) - interest_eps(w3[1]["int_q"])
    stress = justified_pe(0.09, 0.25, coe(rf=0.035)) * fy28_x3 + CASH_YE_FY27 * 1000 / SHARES
    p(f"- Stress for a short (W3 + 10y back to 3.5%): ${stress:.2f} ({stress / PRICE - 1:+.1%})")
    p()
    p("## 3. Sensitivities")
    for lab, kw in (("CoE +50bp", dict(beta=BETA, rf=RF + 0.005)), ("CoE −50bp", dict(beta=BETA, rf=RF - 0.005)),
                    ("β 1.03 (Yahoo)", dict(beta=1.03, rf=RF))):
        rr = coe(**kw)
        e = 0
        for name, (prob, w, g28, g5, roic) in WORLDS.items():
            fy28_x = sum(q["eps"] for q in se.cprt_quarters(w)) * (1 + g28) - interest_eps(w["int_q"])
            e += prob * ((justified_pe(g5, roic, rr) * fy28_x + CASH_YE_FY27 * 1000 / SHARES) / PRICE - 1)
        p(f"- {lab}: probability-weighted return {e:+.1%}")
    for probs in ((0.35, 0.45, 0.20), (0.15, 0.50, 0.35)):
        e = sum(pp * rets[k][1] for pp, k in zip(probs, rets))
        p(f"- Probabilities {probs}: {e:+.1%}")
    (ROOT / "framework_B" / "CPRT_framework_b_numbers.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()


# ------------------------------------------------------------------ fairness addition: a world where the Street is right
W4 = dict(u=0.03, loss=-0.05, rpu=0.05, fixed=0.04, acv_amort=10, acv_op=0, int_q=28)  # share recapture offsets most of the loss
FOUR = {
    # probabilities documented in framework_B/CPRT_framework_b_verdict.md §5
    "W1 share loss deepens + cost creep": (0.20, se.CPRT_WORLDS["bear"], 0.04, 0.03, 0.15),
    "W2 FY27 trough, FY28 normalises": (0.45, se.CPRT_WORLDS["base"], 0.12, 0.06, 0.20),
    "W3 cycle turns + ACV synergies": (0.20, se.CPRT_WORLDS["bull"], 0.18, 0.09, 0.25),
    "W4 Street right: share recapture (JPM data)": (0.15, W4, 0.15, 0.10, 0.25),
}


def four_world():
    r = coe()
    fy26_int = interest_eps(182 / 4)
    ex_cash_price = PRICE - CASH_PRE_ACV * 1000 / SHARES
    mkt_pe_ex = ex_cash_price / (1.75 - fy26_int * 0.6)
    p()
    p("## 4. Four-world distribution (adds a 'Street is right' world; governing for the verdict)")
    p("| World | Prob. | FY27 EPS | FY28 EPS | Justified P/E ex-cash | Value/sh | Return | EPS part (log) | Multiple part (log) |")
    p("|---|---|---|---|---|---|---|---|---|")
    ev, rets = 0.0, []
    for name, (prob, w, g28, g5, roic) in FOUR.items():
        fy27 = sum(q["eps"] for q in se.cprt_quarters(w))
        fy28 = fy27 * (1 + g28)
        x = fy28 - interest_eps(w["int_q"])
        j = justified_pe(g5, roic, r)
        val = j * x + CASH_YE_FY27 * 1000 / SHARES
        ret = val / PRICE - 1
        ev += prob * ret
        rets.append(ret)
        p(f"| {name} | {prob:.2f} | {fy27:.2f} | {fy28:.2f} | {j:.1f}x | ${val:.2f} | {ret:+.1%} | "
          f"{np.log(x / (1.75 - fy26_int * 0.6)):+.1%} | {np.log(j / mkt_pe_ex):+.1%} |")
    p(f"- **Probability-weighted return {ev:+.1%}** → short expected return {-ev:+.1%}; max plausible short loss {max(rets):+.1%} "
      f"(W4); rate-fall stress (W3 + 10y 3.5%) as in §2")
    with open(ROOT / "framework_B" / "CPRT_framework_b_numbers.md", "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(L[-(len(FOUR) + 5):]))


if __name__ == "__main__":
    four_world()
