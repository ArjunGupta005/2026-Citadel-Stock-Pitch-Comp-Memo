"""Build historical valuation multiples and where each stock trades vs. its own range.

Point-in-time: on each trading day only fundamentals already filed are used (XBRL `filed` date).
  P/E (trailing)      price / TTM diluted EPS (net income / diluted shares, split-adjusted)
  EV/EBITDA (trailing) (market cap + debt - cash) / TTM (operating income + D&A)
Also records the subsequent 12-month price return from each month-end, so we can ask
"when the multiple was at this percentile, what happened next?" (feeds Phase 8/11).

Output: data/processed/<T>_valuation_history.csv, printed summary.

Usage: python valuation_history.py [TICKER ...]
"""

import sys

import numpy as np
import pandas as pd
import yfinance as yf

from common import PROCESSED, prices, xbrl_quarterly

TAGS = {
    "net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"],
    "dil_shares": ["WeightedAverageNumberOfDilutedSharesOutstanding"],
    "op_income": ["OperatingIncomeLoss"],
    "da": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "DepreciationAmortizationAndAccretionNet"],
}


def instant(ticker, tags):
    """Balance-sheet (instant) facts, first-filed per period end."""
    from common import RAW, load_json
    facts = load_json(RAW / ticker / "companyfacts.json")["facts"]["us-gaap"]
    frames = []
    for tag in tags:
        if tag in facts:
            for vals in facts[tag]["units"].values():
                d = pd.DataFrame(vals)
                d = d[d["form"].isin(["10-Q", "10-K"])]
                frames.append(d[["end", "val", "filed"]])
    if not frames:
        return pd.DataFrame(columns=["val", "filed"])
    d = pd.concat(frames)
    d["end"], d["filed"] = pd.to_datetime(d["end"]), pd.to_datetime(d["filed"])
    return d.sort_values("filed").drop_duplicates("end").set_index("end").sort_index()


def split_factor(ticker):
    s = yf.Ticker(ticker).splits
    s.index = s.index.tz_localize(None)
    return s


def build(ticker):
    px = prices(ticker)["Close"]
    splits = split_factor(ticker)
    q = {k: xbrl_quarterly(ticker, v, additive=(k != "dil_shares")) for k, v in TAGS.items()}
    ni, sh = q["net_income"], q["dil_shares"]
    df = pd.DataFrame({"ni": ni["val"], "sh": sh["val"].reindex(ni.index), "filed": ni["filed"],
                       "oi": q["op_income"]["val"].reindex(ni.index), "da": q["da"]["val"].reindex(ni.index)}).dropna(subset=["ni"])
    # Split-adjust share counts: a split after the filing date multiplies the as-filed share count.
    def adj(row):
        later = splits[splits.index > row["filed"]]
        return row["sh"] * later.prod() if len(later) else row["sh"]
    # Filer scale errors: e.g. CPRT's 2014 10-Qs tagged diluted shares in thousands (131,486 vs 131.5m). Fewer
    # than 1m diluted shares is impossible for these issuers, so it is treated as a x1000 scale error (audit 2026-10-01).
    df["sh"] = np.where(df["sh"] < 1e6, df["sh"] * 1000, df["sh"])
    df["sh_adj"] = df.apply(adj, axis=1)
    df["ttm_ni"] = df["ni"].rolling(4).sum()
    df["ttm_ebitda"] = (df["oi"] + df["da"]).rolling(4).sum()
    df["ttm_eps"] = df["ttm_ni"] / df["sh_adj"]
    debt = instant(ticker, ["LongTermDebtNoncurrent", "LongTermDebtAndCapitalLeaseObligations"])["val"]
    debt_cur = instant(ticker, ["LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligationsCurrent", "DebtCurrent"])["val"]
    cash = instant(ticker, ["CashAndCashEquivalentsAtCarryingValue"])["val"]
    df["net_debt"] = debt.reindex(df.index).fillna(0) + debt_cur.reindex(df.index).fillna(0) - cash.reindex(df.index).fillna(0)
    # Daily: use the most recent filing available on each day.
    fund = df.dropna(subset=["ttm_eps"]).set_index("filed").sort_index()
    daily = pd.DataFrame({"price": px})
    daily = pd.merge_asof(daily, fund[["ttm_eps", "ttm_ebitda", "sh_adj", "net_debt"]], left_index=True, right_index=True)
    daily["pe"] = daily["price"] / daily["ttm_eps"].where(daily["ttm_eps"] > 0)
    daily["ev_ebitda"] = (daily["price"] * daily["sh_adj"] + daily["net_debt"]) / daily["ttm_ebitda"].where(daily["ttm_ebitda"] > 0)
    daily["fwd_ret_12m"] = daily["price"].shift(-252) / daily["price"] - 1
    daily.to_csv(PROCESSED / f"{ticker}_valuation_history.csv")
    return daily


def summarize(ticker, d, col, since="2012-01-01", exclude=None):
    s = d.loc[since:, col].replace([np.inf, -np.inf], np.nan).dropna()
    if exclude:
        s = s[~s.index.to_series().between(*exclude)]
    now = s.iloc[-1]
    m = d.loc[s.index].resample("ME").last()
    m["pct"] = m[col].rank(pct=True)
    # Forward 12m return by multiple quintile (overlapping windows; descriptive, not a test).
    m["q"] = pd.qcut(m[col], 5, labels=False, duplicates="drop")
    by_q = m.groupby("q")["fwd_ret_12m"].agg(["count", "median"])
    print(f"{ticker} {col}: now {now:.1f}x | percentile {(s < now).mean():.0%} | median {s.median():.1f}x | "
          f"10th-90th {s.quantile(.1):.1f}-{s.quantile(.9):.1f}x")
    print("   fwd 12m return by multiple quintile (0 = cheapest):", by_q.round(3).to_dict("index"))


def main():
    covid = (pd.Timestamp("2020-03-01"), pd.Timestamp("2023-06-30"))
    for t in sys.argv[1:] or ["CPRT", "NCLH", "SBUX"]:
        d = build(t)
        if t == "NCLH":
            summarize(t, d, "ev_ebitda", exclude=covid)
        else:
            summarize(t, d, "pe")


if __name__ == "__main__":
    main()
