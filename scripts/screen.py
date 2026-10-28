"""Phase 3 light screen: valuation, growth, margins, earnings reactions, next date, consensus drift.

Output: data/processed/screen.csv and data/processed/earnings_reactions.csv
"""

import pandas as pd
import yfinance as yf

from common import PROCESSED, TICKERS, prices


def earnings_reactions(ticker, spy):
    """2-day excess return vs SPY around every earnings release: close(t+1)/close(t-1).

    The window covers both pre-market and after-close reporters.
    """
    px = prices(ticker)["Close"]
    dates = pd.to_datetime(pd.read_csv(PROCESSED / f"{ticker}_earnings_dates.csv")["filingDate"])
    out = []
    for d in dates:
        before = px.index[px.index < d]
        after = px.index[px.index > d]
        if len(before) == 0 or len(after) == 0:
            continue
        b, a = before[-1], after[0]
        r = px[a] / px[b] - 1
        rs = spy[a] / spy[b] - 1
        out.append({"ticker": ticker, "date": d.date(), "ret": r, "spy": rs, "excess": r - rs})
    return pd.DataFrame(out)


def quarterly_metrics(t):
    q = t.quarterly_income_stmt
    rev = q.loc["Total Revenue"].dropna().sort_index()
    op = q.loc["Operating Income"].reindex(rev.index)
    yoy = rev.iloc[-1] / rev.iloc[-5] - 1 if len(rev) >= 5 else None
    om = (op / rev)
    return yoy, om


def main():
    spy = prices("SPY", refresh=True)["Close"]
    rows, reactions = [], []
    for tk in TICKERS:
        prices(tk, refresh=True)
        t = yf.Ticker(tk)
        i = t.info
        re_ = earnings_reactions(tk, spy)
        reactions.append(re_)
        yoy, om = quarterly_metrics(t)
        rev_est = t.revenue_estimate
        eps_tr = t.eps_trend
        cal = t.calendar or {}
        nxt = cal.get("Earnings Date", [None])
        last = re_.iloc[0] if len(re_) else None
        rows.append({
            "ticker": tk,
            "price": i.get("currentPrice"),
            "mkt_cap_bn": i.get("marketCap", 0) / 1e9,
            "ev_bn": (i.get("enterpriseValue") or 0) / 1e9,
            "fwd_pe": i.get("forwardPE"),
            "ev_ebitda_ltm": i.get("enterpriseToEbitda"),
            "ev_sales_ltm": i.get("enterpriseToRevenue"),
            "ev_sales_fy1": (i.get("enterpriseValue") or 0) / rev_est.loc["+1y", "avg"] if rev_est is not None else None,
            "rev_yoy_lastQ": yoy,
            "rev_growth_fy0_cons": rev_est.loc["0y", "growth"] if rev_est is not None else None,
            "rev_growth_fy1_cons": rev_est.loc["+1y", "growth"] if rev_est is not None else None,
            "op_margin_lastQ": om.iloc[-1],
            "op_margin_yrago": om.iloc[-5] if len(om) >= 5 else None,
            "last_er_date": last["date"] if last is not None else None,
            "last_er_excess_2d": last["excess"] if last is not None else None,
            "avg_abs_er_move_8q": re_["excess"].head(8).abs().mean(),
            "next_er_date": nxt[0] if nxt else None,
            "fy1_eps_rev_90d": eps_tr.loc["+1y", "current"] / eps_tr.loc["+1y", "90daysAgo"] - 1 if eps_tr is not None else None,
            "n_analysts": i.get("numberOfAnalystOpinions"),
            "target_mean": i.get("targetMeanPrice"),
            "short_pct_float": i.get("shortPercentOfFloat"),
            "beta": i.get("beta"),
            "perf_52w": i.get("52WeekChange"),
        })
    df = pd.DataFrame(rows)
    df.to_csv(PROCESSED / "screen.csv", index=False)
    pd.concat(reactions).to_csv(PROCESSED / "earnings_reactions.csv", index=False)
    pd.set_option("display.width", 250)
    print(df.round(3).T.to_string())


if __name__ == "__main__":
    main()
