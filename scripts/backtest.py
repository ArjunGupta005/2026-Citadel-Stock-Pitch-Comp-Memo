"""Historical signal tests: "if this signal had existed historically, what happened afterward?"

Not a trading strategy. Point-in-time only:
  - signals fire on the date the information became public (earnings-release date / XBRL filing date)
  - KPI values are as first reported (kpi_extract / xbrl_quarterly keep the first-filed value)
  - returns start the trading day AFTER the signal date (no same-day look-ahead)
Measures per event: 1M / 3M / 6M forward excess return vs benchmark, subsequent TTM EPS change
(next 4 reported quarters vs the trailing 4 at the event), and trailing-multiple change over 6M.

Signals (pre-specified before looking at outcomes):
  CPRT_margin_contraction  quarterly operating margin down >= 300bp y/y
  CPRT_cheap_and_falling   trailing P/E <= 20th pct of own prior 5y AND TTM EPS growth < 0 (value-trap test)
  NCLH_guide_decel         next-Q Net Yield guide <= last reported Net Yield - 2pt
  NCLH_fy_guide_cut        FY Net Yield guide lowered vs the prior release's FY guide
  SBUX_margin_expansion    quarterly operating margin up >= 300bp y/y (does it persist?)
  *_earnings_miss          2-day excess earnings reaction <= -5% (post-reaction drift)

Usage: python backtest.py [SIGNAL ...]
"""

import sys

import numpy as np
import pandas as pd
from scipy import stats

from common import PROCESSED, REVENUE_TAGS, prices, xbrl_quarterly

HORIZONS = {"1M": 21, "3M": 63, "6M": 126}
COVID = (pd.Timestamp("2020-02-01"), pd.Timestamp("2023-06-30"))


def fwd_excess(ticker, bench, dates):
    px, bx = prices(ticker)["Close"], bench
    rows = []
    for d in dates:
        idx = px.index.searchsorted(pd.Timestamp(d), side="right")  # first trading day after signal
        if idx >= len(px):
            continue
        r = {"date": pd.Timestamp(d)}
        for h, n in HORIZONS.items():
            if idx + n < len(px):
                a = px.iloc[idx + n] / px.iloc[idx] - 1
                b = bx.reindex(px.index).ffill().iloc[idx + n] / bx.reindex(px.index).ffill().iloc[idx] - 1
                r[h] = a - b
        rows.append(r)
    return pd.DataFrame(rows)


def eps_and_multiple(ticker, df):
    """Subsequent TTM EPS change and 6M trailing-multiple change from valuation_history."""
    path = PROCESSED / f"{ticker}_valuation_history.csv"
    if not path.exists() or df.empty:
        return df
    v = pd.read_csv(path, index_col=0, parse_dates=True)
    col = "ev_ebitda" if ticker == "NCLH" else "pe"
    out = []
    for d in df["date"]:
        i = v.index.searchsorted(d, side="right")
        j = min(i + 126, len(v) - 1)
        k = min(i + 252, len(v) - 1)
        e0, e1 = v["ttm_eps"].iloc[i] if i < len(v) else np.nan, v["ttm_eps"].iloc[k] if k > i else np.nan
        m0, m1 = v[col].iloc[i] if i < len(v) else np.nan, v[col].iloc[j] if j > i else np.nan
        out.append({"eps_chg_12m": (e1 / e0 - 1) if e0 and e0 > 0 else np.nan,
                    "multiple_chg_6m": (m1 / m0 - 1) if m0 and m0 > 0 else np.nan})
    return pd.concat([df.reset_index(drop=True), pd.DataFrame(out)], axis=1)


def summarize(name, df, thesis_sign):
    """thesis_sign = -1 if the thesis needs negative forward returns (short), +1 for long."""
    if df.empty:
        print(f"{name}: no events")
        return {}
    res = {"signal": name, "n": len(df)}
    for h in HORIZONS:
        if h not in df:
            continue
        x = df[h].dropna()
        if len(x) >= 3:
            t, p = stats.ttest_1samp(x, 0)
            res[f"{h}_mean"], res[f"{h}_median"] = x.mean(), x.median()
            res[f"{h}_hit"] = (np.sign(x) == thesis_sign).mean()
            res[f"{h}_t"], res[f"{h}_p"] = t, p
    for c in ("eps_chg_12m", "multiple_chg_6m"):
        if c in df:
            res[f"{c}_median"] = df[c].median()
    # Pre-registered R4 test: opposite sign at 3M or 6M with n >= 8 -> contradicts.
    contradict = any(res.get(f"{h}_mean", 0) * thesis_sign < 0 for h in ("3M", "6M")) and res["n"] >= 8
    unsupported = not contradict and not any(res.get(f"{h}_p", 1) < 0.10 for h in ("3M", "6M"))
    res["R4"] = "CONTRADICTS" if contradict else ("unsupported (same sign, not significant)" if unsupported else "supports")
    return res


# ---------------------------------------------------------------- signals

def margin_change_dates(ticker, threshold, direction):
    rev = xbrl_quarterly(ticker, REVENUE_TAGS)
    oi = xbrl_quarterly(ticker, ["OperatingIncomeLoss"])
    m = (oi["val"] / rev["val"]).dropna()
    chg = m - m.shift(4)
    filed = oi["filed"].reindex(chg.index)
    sel = chg <= -threshold if direction < 0 else chg >= threshold
    ev = filed[sel & chg.notna()]
    return [d for d in ev if not (COVID[0] <= d <= COVID[1])]


def cheap_and_falling_dates(ticker):
    v = pd.read_csv(PROCESSED / f"{ticker}_valuation_history.csv", index_col=0, parse_dates=True)
    pe = v["pe"].where(v["pe"] > 0)
    pct = pe.rolling(1260, min_periods=750).apply(lambda w: (w[:-1] < w[-1]).mean(), raw=True)
    eps_g = v["ttm_eps"] / v["ttm_eps"].shift(252) - 1
    cond = (pct <= 0.20) & (eps_g < 0)
    # One event per quarter: first qualifying day after each new filing (ttm_eps change)
    newq = v["ttm_eps"].ne(v["ttm_eps"].shift())
    first = cond & (newq | cond.ne(cond.shift()))
    ev = cond[first & cond].index
    ev = pd.Series(ev).groupby(pd.Series(ev).dt.to_period("Q")).first().tolist()
    return [d for d in ev if not (COVID[0] <= d <= COVID[1])]


def nclh_guide_dates(kind):
    k = pd.read_csv(PROCESSED / "NCLH_kpis.csv", parse_dates=["period_end", "released"])
    g = k[k.kpi == "guide_net_yield_nextq_cc"].set_index("released")["value"]
    a = k[k.kpi == "net_yield_yoy_cc"].set_index("released")["value"]
    fy = k[k.kpi == "guide_net_yield_fy_cc"].set_index("released")["value"].sort_index()
    if kind == "decel":
        both = pd.concat([g, a], axis=1, keys=["g", "a"]).dropna()
        ev = both[both["g"] <= both["a"] - 0.02].index
    else:
        # Compare FY guides within the same fiscal year only (Q1-Q3 releases of the year).
        fyy = fy[fy.index.month >= 4]
        prev = fyy.shift()
        same_year = fyy.index.year == pd.Series(fyy.index).shift().dt.year.values
        ev = fyy[(fyy < prev - 0.0049) & same_year].index
    return [d for d in ev if not (COVID[0] <= d <= COVID[1])]


def earnings_miss_dates(ticker, thr=-0.05):
    r = pd.read_csv(PROCESSED / "earnings_reactions.csv", parse_dates=["date"])
    r = r[(r.ticker == ticker) & (r.excess <= thr)]
    return [d for d in r["date"] if not (COVID[0] <= d <= COVID[1])]


def peer_basket(tickers):
    px = pd.concat([prices(t)["Close"] for t in tickers], axis=1).dropna(how="all")
    return (px / px.iloc[0]).mean(axis=1)


SIGNALS = {
    "CPRT_margin_contraction": ("CPRT", lambda: margin_change_dates("CPRT", 0.03, -1), -1),
    "CPRT_cheap_and_falling": ("CPRT", lambda: cheap_and_falling_dates("CPRT"), -1),
    "CPRT_earnings_miss": ("CPRT", lambda: earnings_miss_dates("CPRT"), -1),
    "NCLH_guide_decel": ("NCLH", lambda: nclh_guide_dates("decel"), -1),
    "NCLH_fy_guide_cut": ("NCLH", lambda: nclh_guide_dates("cut"), -1),
    "NCLH_earnings_miss": ("NCLH", lambda: earnings_miss_dates("NCLH"), -1),
    "SBUX_margin_expansion": ("SBUX", lambda: margin_change_dates("SBUX", 0.03, +1), +1),
    "SBUX_earnings_miss": ("SBUX", lambda: earnings_miss_dates("SBUX"), -1),
}


def main():
    spy = prices("SPY")["Close"]
    cruise = peer_basket(["RCL", "CCL"])
    names = sys.argv[1:] or list(SIGNALS)
    results = []
    for name in names:
        ticker, fn, sign = SIGNALS[name]
        dates = sorted(set(fn()))
        for bname, bench in (("SPY", spy),) + ((("RCL+CCL", cruise),) if ticker == "NCLH" else ()):
            df = eps_and_multiple(ticker, fwd_excess(ticker, bench, dates))
            df.to_csv(PROCESSED / f"backtest_{name}_{bname}.csv", index=False)
            res = summarize(f"{name} vs {bname}", df, sign)
            if res:
                results.append(res)
    out = pd.DataFrame(results)
    out.to_csv(PROCESSED / "backtest_summary.csv", index=False)
    pd.set_option("display.width", 250)
    cols = ["signal", "n"] + [c for c in out.columns if c.endswith(("_mean", "_hit", "_p"))] + \
           [c for c in out.columns if c.endswith("median") and not c[0].isdigit()] + ["R4"]
    print(out[[c for c in cols if c in out]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
