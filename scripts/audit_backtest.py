"""Backtest audit: threshold perturbations, dispersion, sector-adjusted results, timestamp alignment.

Uses the point-in-time signal and return functions from backtest.py unchanged.
Output: audit/backtest_audit.md and data/processed/backtest_robustness.csv
"""

import numpy as np
import pandas as pd
from scipy import stats

import backtest as bt
from common import PROCESSED, ROOT, prices

L = []


def p(s=""):
    L.append(s)
    print(s)


def stats_row(family, thr, bench, df, sign):
    r = {"family": family, "threshold": thr, "bench": bench, "n": len(df)}
    for h in bt.HORIZONS:
        x = df[h].dropna() if h in df else pd.Series(dtype=float)
        r[f"{h}_n"] = len(x)
        if len(x) >= 3:
            r[f"{h}_mean"], r[f"{h}_median"], r[f"{h}_std"] = x.mean(), x.median(), x.std()
            r[f"{h}_hit"] = (np.sign(x) == sign).mean()
            r[f"{h}_p"] = stats.ttest_1samp(x, 0).pvalue
    return r


def run():
    spy = prices("SPY")["Close"]
    sector = {"CPRT": prices("XLI", refresh=True)["Close"], "NCLH": bt.peer_basket(["RCL", "CCL"]),
              "SBUX": prices("XLY")["Close"], "NKE": prices("XLY")["Close"]}
    fams = [
        ("CPRT margin contraction (bp)", "CPRT", -1, [0.02, 0.03, 0.04], lambda t: bt.margin_change_dates("CPRT", t, -1)),
        ("CPRT earnings miss (2d excess)", "CPRT", -1, [-0.03, -0.05, -0.07], lambda t: bt.earnings_miss_dates("CPRT", t)),
        ("NCLH guide decel (pts)", "NCLH", -1, [0.01, 0.02, 0.03], None),
        ("NCLH earnings miss (2d excess)", "NCLH", -1, [-0.03, -0.05, -0.07], lambda t: bt.earnings_miss_dates("NCLH", t)),
        ("NKE earnings miss (2d excess)", "NKE", -1, [-0.03, -0.05, -0.07], lambda t: bt.earnings_miss_dates("NKE", t)),
        ("SBUX margin expansion (bp)", "SBUX", +1, [0.02, 0.03, 0.04], lambda t: bt.margin_change_dates("SBUX", t, +1)),
    ]
    rows = []
    for fam, tk, sign, grid, fn in fams:
        for thr in grid:
            if fn is None:  # NCLH guide decel with variable gap
                k = pd.read_csv(PROCESSED / "NCLH_kpis.csv", parse_dates=["period_end", "released"])
                g = k[k.kpi == "guide_net_yield_nextq_cc"].set_index("released")["value"]
                a = k[k.kpi == "net_yield_yoy_cc"].set_index("released")["value"]
                both = pd.concat([g, a], axis=1, keys=["g", "a"]).dropna()
                dates = [d for d in both[both["g"] <= both["a"] - thr].index if not (bt.COVID[0] <= d <= bt.COVID[1])]
            else:
                dates = fn(thr)
            dates = sorted(set(dates))
            for bname, b in (("SPY", spy), ("sector", sector[tk])):
                df = bt.fwd_excess(tk, b, dates)
                rows.append(stats_row(fam, thr, bname, df, sign))
    return pd.DataFrame(rows)


def timestamps():
    """Show signal date vs first return date for a sample of events (alignment check)."""
    p("## Timestamp alignment sample")
    p("| Signal | Info public (release / filing date) | Return window starts (close of) |")
    p("|---|---|---|")
    px = prices("CPRT")["Close"]
    for d in bt.margin_change_dates("CPRT", 0.03, -1)[-3:]:
        i = px.index.searchsorted(pd.Timestamp(d), side="right")
        p(f"| CPRT margin contraction | 10-Q/10-K filed {pd.Timestamp(d).date()} | {px.index[i].date()} |")
    r = pd.read_csv(PROCESSED / "earnings_reactions.csv", parse_dates=["date"])
    for tk in ("NCLH", "CPRT"):
        for d in r[(r.ticker == tk) & (r.excess <= -0.05)]["date"].tail(2):
            i = px.index.searchsorted(d, side="right")
            p(f"| {tk} earnings miss | 8-K {d.date()}; reaction measured close(t-1)→close(t+1) | {px.index[i].date()} (= t+1 close, after reaction known) |")
    p()


def main():
    p("# Backtest audit (scripts/audit_backtest.py)")
    p()
    p("## Bias controls")
    p("- **Look-ahead:** each signal is dated by the public release / SEC filing date (`kpi_extract`: 8-K date; "
      "`xbrl_quarterly`: `filed`). Returns start at the close of the first trading day *after* that date "
      "(`backtest.fwd_excess`, searchsorted side='right').")
    p("- **Revisions:** `xbrl_quarterly` keeps the FIRST-filed value per period (later restatements and comparatives are ignored); "
      "release KPIs are parsed from the original 8-K exhibit text.")
    p("- **Known residual issues:** (i) XBRL filed dates trail the earnings release by 2-6 weeks, so margin signals are late "
      "(conservative, not look-ahead); (ii) 2-day earnings-miss signals use close(t+1), so they are only known at that close, and "
      "the window starts there; (iii) COVID window Feb-2020 to Jun-2023 excluded; (iv) overlapping 6M windows inflate t-stats.")
    p("- **Threshold selection:** round-number thresholds were written into `backtest.py` before results were run. "
      "This audit adds ±1 step perturbations; nothing was chosen ex post.")
    p()
    timestamps()
    df = run()
    df.to_csv(PROCESSED / "backtest_robustness.csv", index=False)
    p("## Results by threshold (excess returns; thesis-direction hit rate)")
    cols = ["family", "threshold", "bench", "n"]
    for h in ("1M", "3M", "6M"):
        cols += [f"{h}_mean", f"{h}_median", f"{h}_std", f"{h}_hit", f"{h}_p"]
    d = df[[c for c in cols if c in df]]
    p("| " + " | ".join(d.columns) + " |")
    p("|" + "---|" * len(d.columns))
    for _, r in d.iterrows():
        p("| " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in r.values) + " |")
    (ROOT / "audit").mkdir(exist_ok=True)
    (ROOT / "audit" / "backtest_audit.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
