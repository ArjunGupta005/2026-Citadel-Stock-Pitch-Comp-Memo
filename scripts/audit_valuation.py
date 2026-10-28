"""Audit of the CPRT "near cheapest-ever P/E" claim.

Checks: splits, start-date sensitivity of the percentile, trailing vs (perfect-foresight) forward P/E,
GAAP vs ex-cash/ex-interest earnings, margin regime, interest-rate regime and interest income share of EPS.
Output: audit/valuation_audit.md
"""

import numpy as np
import pandas as pd
import yfinance as yf

from common import PROCESSED, ROOT, prices, xbrl_quarterly
from valuation_history import instant

L = []


def p(s=""):
    L.append(s)
    print(s)


def main():
    v = pd.read_csv(PROCESSED / "CPRT_valuation_history.csv", index_col=0, parse_dates=True)
    p("# CPRT valuation-history audit (scripts/audit_valuation.py)")
    p()
    s = yf.Ticker("CPRT").splits
    p(f"Splits (yfinance): {', '.join(f'{d.date()} {r:g}:1' for d, r in s.items())}")
    # continuity check around split dates: TTM EPS should not jump by the split ratio
    for d in s.index.tz_localize(None):
        w = v["ttm_eps"].loc[d - pd.Timedelta(days=10): d + pd.Timedelta(days=10)].dropna()
        if len(w):
            p(f"- TTM EPS around {d.date()}: {w.iloc[0]:.3f} → {w.iloc[-1]:.3f} (no split-sized jump = adjusted correctly)")
    p()
    first = v["ttm_eps"].first_valid_index()
    p(f"Point-in-time XBRL EPS history starts {first.date()} (pre-2009 EPS not in XBRL).")
    pe = v["pe"].where((v["pe"] > 0) & (v["pe"] < 100)).dropna()
    now = pe.iloc[-1]
    p(f"Trailing GAAP P/E today: {now:.1f}x (price ${v['price'].iloc[-1]:.2f} / TTM EPS ${v['ttm_eps'].iloc[-1]:.2f})")
    p()
    p("| Window start | Percentile of today's trailing P/E | Min | Median |")
    p("|---|---|---|---|")
    for start in ("2010", "2012", "2015", "2018", "2021"):
        x = pe.loc[start:]
        p(f"| {start} | {(x < now).mean():.0%} | {x.min():.1f}x | {x.median():.1f}x |")
    p()
    # Ex-cash, ex-interest P/E (removes the rate-driven part of EPS and the cash pile)
    ii = xbrl_quarterly("CPRT", ["InvestmentIncomeInterest", "InterestIncomeOther", "InterestRevenueExpenseNet",
                                 "InvestmentIncomeInterestAndDividend", "InterestIncomeExpenseNonoperatingNet"])
    ni = xbrl_quarterly("CPRT", ["NetIncomeLoss"])
    cash = instant("CPRT", ["CashAndCashEquivalentsAtCarryingValue"])["val"]
    htm = instant("CPRT", ["HeldToMaturitySecuritiesCurrent", "DebtSecuritiesHeldToMaturityAmortizedCostAfterAllowanceForCreditLoss",
                           "HeldToMaturitySecurities", "ShortTermInvestments"])["val"]
    f = pd.DataFrame({"ni": ni["val"], "ii": ii["val"].reindex(ni.index).fillna(0), "filed": ni["filed"]})
    f["ttm_ni"], f["ttm_ii"] = f["ni"].rolling(4).sum(), f["ii"].rolling(4).sum()
    f["cash"] = cash.reindex(f.index).ffill().fillna(0) + htm.reindex(f.index).fillna(0)
    f["ii_share"] = f["ttm_ii"] * 0.8 / f["ttm_ni"]
    f = f.dropna(subset=["ttm_ni"]).set_index("filed").sort_index()
    d = pd.merge_asof(v[["price", "sh_adj"]], f[["ttm_ni", "ttm_ii", "cash", "ii_share"]], left_index=True, right_index=True)
    d["mcap"] = d["price"] * d["sh_adj"]
    d["pe_gaap"] = d["mcap"] / d["ttm_ni"]
    d["pe_ex_cash"] = (d["mcap"] - d["cash"]) / (d["ttm_ni"] - d["ttm_ii"] * 0.8)
    x = d.loc["2012":].dropna(subset=["pe_ex_cash"])
    x = x[(x.pe_ex_cash > 0) & (x.pe_ex_cash < 100)]
    nowx = x["pe_ex_cash"].iloc[-1]
    p(f"Ex-cash, ex-interest P/E today: {nowx:.1f}x (cash+securities ${d['cash'].iloc[-1] / 1e9:.1f}bn; "
      f"after-tax interest = {d['ii_share'].iloc[-1]:.0%} of TTM net income). Percentile since 2012: {(x.pe_ex_cash < nowx).mean():.0%}.")
    p("Year-end interest share of net income: " + ", ".join(
        f"{y}: {d['ii_share'].loc[str(y)].dropna().iloc[-1]:.0%}" for y in range(2014, 2027) if len(d['ii_share'].loc[str(y)].dropna())))
    p()
    # perfect-foresight forward P/E: price / EPS actually earned over the next 12 months (uses future data; descriptive only)
    m = v.resample("ME").last()
    m["pf_fwd_pe"] = m["price"] / m["ttm_eps"].shift(-12)
    pf = m.loc["2012":"2025-07", "pf_fwd_pe"].replace([np.inf, -np.inf], np.nan).dropna()
    for lab, e in (("Street FY27 $1.75", 1.75), ("our base FY27 $1.35", 1.35), ("our ex-ACV FY27 $1.43", 1.433)):
        fpe = v["price"].iloc[-1] / e
        p(f"- Forward P/E on {lab}: {fpe:.1f}x → percentile of perfect-foresight forward P/E 2012-2025: {(pf < fpe).mean():.0%} "
          f"(median {pf.median():.1f}x)")
    p()
    # margin and rate regimes
    rev = xbrl_quarterly("CPRT", ["Revenues", "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"])
    oi = xbrl_quarterly("CPRT", ["OperatingIncomeLoss"])
    om = (oi["val"].rolling(4).sum() / rev["val"].rolling(4).sum()).dropna()
    tnx = prices("^TNX")["Close"]
    tnx = tnx / 10 if tnx.max() > 20 else tnx
    p("| Fiscal year-end | TTM op margin | 10y UST | Trailing P/E (year-end) |")
    p("|---|---|---|---|")
    for y in range(2012, 2027):
        e = pd.Timestamp(f"{y}-07-31")
        omv = om[om.index <= e]
        pev = pe[pe.index <= e + pd.Timedelta(days=60)]
        t = tnx[tnx.index <= e]
        if len(omv) and len(pev) and len(t):
            p(f"| FY{y} | {omv.iloc[-1]:.1%} | {t.iloc[-1]:.2f}% | {pev.iloc[-1]:.1f}x |")
    (ROOT / "audit").mkdir(exist_ok=True)
    (ROOT / "audit" / "valuation_audit.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
