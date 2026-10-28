"""Peer comparison: growth, margins, and multiples vs. a defined comp set (saved to data/comps/).

Usage: python comps_analysis.py [TICKER ...]
"""

import sys

import pandas as pd
import yfinance as yf

from common import COMPS

COMP_SETS = {
    "CPRT": ["CPRT", "RBA", "ACVA", "OPLN", "KMX", "CVNA"],
    "NCLH": ["NCLH", "RCL", "CCL", "VIK"],
    "SBUX": ["SBUX", "MCD", "CMG", "YUM", "BROS", "QSR"],
}
FIELDS = {"price": "currentPrice", "mkt_cap_bn": "marketCap", "ev_bn": "enterpriseValue", "fwd_pe": "forwardPE",
          "ev_ebitda": "enterpriseToEbitda", "ev_sales": "enterpriseToRevenue", "rev_growth": "revenueGrowth",
          "op_margin": "operatingMargins", "net_debt_ebitda": None, "perf_52w": "52WeekChange", "short_pct": "shortPercentOfFloat"}


def row(t):
    i = yf.Ticker(t).info
    r = {k: i.get(v) for k, v in FIELDS.items() if v}
    for k in ("mkt_cap_bn", "ev_bn"):
        r[k] = (r[k] or 0) / 1e9
    ebitda = i.get("ebitda")
    debt, cash = i.get("totalDebt") or 0, i.get("totalCash") or 0
    r["net_debt_ebitda"] = (debt - cash) / ebitda if ebitda else None
    try:
        e = yf.Ticker(t).earnings_estimate
        r["eps_growth_fy1"] = e.loc["+1y", "growth"]
    except Exception:
        r["eps_growth_fy1"] = None
    return r


def main():
    COMPS.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 220)
    for t in sys.argv[1:] or COMP_SETS:
        df = pd.DataFrame({p: row(p) for p in COMP_SETS[t]}).T
        peers = df.drop(index=t).apply(pd.to_numeric, errors="coerce")
        df.loc["peer median"] = peers.median()
        df.to_csv(COMPS / f"{t}_comps.csv")
        print(f"===== {t}")
        print(df.apply(pd.to_numeric, errors="coerce").round(2).to_string())


if __name__ == "__main__":
    main()
