"""Track management guidance vs. actual results, and results vs. consensus, to measure credibility and bias.

1. Management guidance vs actual (from kpi_extract output):
   NCLH: next-quarter Net Yield (cc) guidance vs. reported Net Yield (cc) one quarter later.
2. Consensus EPS surprise history (yfinance earnings dates: estimate vs reported) for any ticker.

Output: data/processed/<T>_guidance_history.csv, data/processed/<T>_eps_surprises.csv

Usage: python guidance_history.py [TICKER ...]
"""

import sys

import pandas as pd
import yfinance as yf

from common import PROCESSED

GUIDE_PAIRS = {"NCLH": ("guide_net_yield_nextq_cc", "net_yield_yoy_cc")}
COVID = (pd.Timestamp("2020-01-01"), pd.Timestamp("2023-12-31"))


def guidance_vs_actual(ticker):
    if ticker not in GUIDE_PAIRS:
        return None
    g_k, a_k = GUIDE_PAIRS[ticker]
    k = pd.read_csv(PROCESSED / f"{ticker}_kpis.csv", parse_dates=["period_end", "released"])
    g = k[k.kpi == g_k].set_index("period_end")["value"].sort_index()
    a = k[k.kpi == a_k].set_index("period_end")["value"].sort_index()
    rows = []
    for end, guide in g.items():
        nxt = a[a.index > end]
        if len(nxt) and (nxt.index[0] - end).days < 120:
            rows.append({"guided_at_period": end, "target_period": nxt.index[0], "guide": guide, "actual": nxt.iloc[0],
                         "beat_pts": (nxt.iloc[0] - guide) * 100})
    df = pd.DataFrame(rows)
    df = df[~df["target_period"].between(*COVID)]
    df.to_csv(PROCESSED / f"{ticker}_guidance_history.csv", index=False)
    return df


def eps_surprises(ticker):
    e = yf.Ticker(ticker).get_earnings_dates(limit=60)
    if e is None or e.empty:
        return None
    e = e.dropna(subset=["Reported EPS"]).copy()
    e["surprise_pct"] = e["Reported EPS"] / e["EPS Estimate"] - 1
    e.to_csv(PROCESSED / f"{ticker}_eps_surprises.csv")
    return e


def main():
    for t in sys.argv[1:] or ["NCLH", "SBUX", "CPRT"]:
        g = guidance_vs_actual(t)
        if g is not None and len(g):
            print(f"{t} guidance vs actual (next-Q, pts): n={len(g)}, mean beat {g.beat_pts.mean():+.2f}, "
                  f"hit rate {(g.beat_pts >= 0).mean():.0%}, last 6:")
            print(g.tail(6).round(4).to_string(index=False))
        e = eps_surprises(t)
        if e is not None:
            recent = e.head(12)
            print(f"{t} EPS vs consensus: last {len(recent)} qtrs beat rate {(recent['surprise_pct'] > 0).mean():.0%}, "
                  f"median surprise {recent['surprise_pct'].median():+.1%}, latest {e.index[0].date()}")


if __name__ == "__main__":
    main()
