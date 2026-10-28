"""Objective proxies used to anchor Phase 3 scorecard scores.

- est_dispersion: (high - low) / avg of next-FY EPS estimates -> room for a variant view
- tgt_dispersion: (high - low) / mean analyst target -> how contested the stock is
- ps_pctile: current EV/Sales-ish (price/sales) percentile vs own history -> asymmetry
- years_hist: years of quarterly XBRL revenue -> historical-test depth
- er_move_ratio: avg abs 2d earnings move / avg abs 2d non-earnings move -> how much earnings (catalysts) move the stock
"""

import numpy as np
import pandas as pd
import yfinance as yf

from common import PROCESSED, REVENUE_TAGS, TICKERS, prices, xbrl_quarterly

def main():
    rows = []
    reac = pd.read_csv(PROCESSED / "earnings_reactions.csv")
    for tk in TICKERS:
        t = yf.Ticker(tk)
        ee = t.earnings_estimate
        tg = t.analyst_price_targets or {}
        px = prices(tk)["Close"]
        rev = xbrl_quarterly(tk, REVENUE_TAGS)["val"]
        ttm = rev.rolling(4).sum().dropna()
        shares = t.info.get("sharesOutstanding")
        # Price/TTM-sales percentile using current share count (approximation; flags extremes only).
        ps_hist = []
        for d, v in ttm.items():
            p = px[px.index <= d + pd.Timedelta(days=45)]
            if len(p):
                ps_hist.append(p.iloc[-1] * shares / v)
        ps_now = px.iloc[-1] * shares / ttm.iloc[-1] if len(ttm) else np.nan
        pct = (np.array(ps_hist) < ps_now).mean() if ps_hist else np.nan
        r = reac[reac.ticker == tk]
        dr = px.pct_change(2).abs()
        rows.append({
            "ticker": tk,
            "est_dispersion_fy1": (ee.loc["+1y", "high"] - ee.loc["+1y", "low"]) / ee.loc["+1y", "avg"],
            "tgt_dispersion": (tg.get("high", np.nan) - tg.get("low", np.nan)) / tg.get("mean", np.nan),
            "tgt_low": tg.get("low"), "tgt_high": tg.get("high"),
            "ps_now": ps_now, "ps_pctile_own_hist": pct,
            "years_qtr_hist": len(rev) / 4,
            "n_earnings_events": len(r),
            "er_move_ratio": r["excess"].abs().head(12).mean() / dr.tail(750).mean(),
        })
    df = pd.DataFrame(rows)
    df.to_csv(PROCESSED / "screen_proxies.csv", index=False)
    print(df.round(3).to_string())


if __name__ == "__main__":
    main()
