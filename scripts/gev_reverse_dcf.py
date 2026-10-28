"""GEV: normalized FCF variants and reverse-engineering of the operating assumptions embedded in the share price.

Inputs (pulled 2026-10-01): price $987.45; market cap $263.0bn; debt $3.7bn; cash $12.7bn (Yahoo, secondary).
Consensus EBITDA path (secondary, press-reported sell-side): 2026 ~$6.5bn (Mizuho), 2028 ~$12.94bn, 2027 = 2028/1.3637.
Company: FY26 FCF guide $11.5-12.5bn; adj. EBITDA margin 12-14%; capex plan ~$6bn 2025-28.
"""

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from common import ROOT

d = pd.read_csv(ROOT / "framework_B" / "gev_fcf_decomposition.csv", index_col=0, parse_dates=True)
ttm = d.loc["2025-07-01":"2026-06-30"].sum(numeric_only=True)
L = []


def p(s=""):
    L.append(s)
    print(s)


p("# GEV — Normalized FCF and reverse-engineered expectations (scripts/gev_reverse_dcf.py)")
p()
p("## TTM (Q3-25 to Q2-26), $bn, from SEC XBRL (YTD cash flows differenced)")
n1 = ttm["fcf"] - ttm["d_contract_liab"]
n3 = ttm["fcf"] - (ttm["d_contract_liab"] - ttm["d_inventory"] - ttm["d_contract_asset"])
p(f"- Reported FCF {ttm['fcf']:.2f}; change in contract liabilities (deposits) {ttm['d_contract_liab']:.2f} "
  f"({ttm['d_contract_liab'] / ttm['fcf']:.0%} of FCF)")
p(f"- N1: FCF with zero incremental deposits = {n1:.2f}")
p(f"- N3: FCF excluding deposits net of the inventory / contract assets they fund = {n3:.2f}")
ebitda26, da, capex, tax = 6.0, 1.0, 1.5, 0.21
n2 = (ebitda26 - da) * (1 - tax) + da - capex
p(f"- N2: earnings-based steady-state FCF (FY26 adj. EBITDA ~${ebitda26}bn at a 13% margin; D&A ~${da}bn; capex ~${capex}bn/yr; "
  f"21% tax; zero working capital) ≈ {n2:.2f} vs the FY26 FCF guide of 12.0 → about {1 - n2 / 12:.0%} of guided FY26 FCF is working capital / deposits")
p()
price, mcap, debt, cash, sh = 987.45, 263.0, 3.7, 12.7, 266.3
ev = mcap + debt - cash
ev_dep = mcap + debt  # if cash is treated as customer money (backed by $40bn of contract liabilities), not excess
e26, e28 = 6.5, 12.94
e27 = e28 / 1.3637
p("## What the price embeds")
p(f"- EV ${ev:.1f}bn (${ev_dep:.1f}bn if deposit-funded cash is not treated as excess)")
p(f"- EV / consensus EBITDA: 2026 {ev / e26:.1f}x | 2027 {ev / e27:.1f}x | 2028 {ev / e28:.1f}x")

wacc, g_term, mature_mult = 0.09, 0.03, 13.0


def ufcf(e):
    return (e - da * (e / e26) ** 0.5) * (1 - tax) + da * (e / e26) ** 0.5 - max(capex, 0.12 * e * 0.15)


def pv_path(g_post, years_post=5):
    """EV = PV of UFCF 2026Q4-2028 on the consensus path, then EBITDA grows g_post for years_post years,
    then a terminal value at a mature 13x EBITDA."""
    path = [e26 * 0.25, e27, e28]
    t = [0.125, 0.75, 1.75]
    e = e28
    for k in range(years_post):
        e *= 1 + g_post
        path.append(e)
        t.append(2.75 + k)
    pv = sum(ufcf(x) / (1 + wacc) ** tt for x, tt in zip(path, t))
    tv = path[-1] * mature_mult / (1 + wacc) ** t[-1]
    return pv + tv, path[-1]


g = brentq(lambda x: pv_path(x)[0] - ev, -0.2, 0.6)
v, e33 = pv_path(g)
p(f"- Reverse DCF (WACC {wacc:.0%}, consensus EBITDA through 2028, then 5 years of growth, then a {mature_mult:.0f}x mature exit): "
  f"the price requires **2029-2033 EBITDA CAGR of {g:.1%}**, i.e. 2033 EBITDA ≈ ${e33:.1f}bn "
  f"(≈ ${e33 / 0.22:.0f}bn revenue at a 22% margin vs FY27 consensus revenue of $52.8bn)")
for alt in (11.0, 15.0):
    mature_mult = alt
    ga = brentq(lambda x: pv_path(x)[0] - ev, -0.2, 0.6)
    p(f"  - with a {alt:.0f}x exit: required CAGR {ga:.1%}")
mature_mult = 13.0
p(f"- Implied end-2028 EV/EBITDA if the 2026-28 consensus path is delivered and the stock compounds at 9%: "
  f"{(ev * 1.09 ** 2.25 - sum(ufcf(x) for x in (e26 * 0.25, e27, e28))) / e28:.1f}x 2028 EBITDA")
(ROOT / "framework_B" / "gev_reverse_dcf.md").write_text("\n".join(L), encoding="utf-8")
