"""Phase 10: is the thesis a company call or a macro bet in disguise?

Weekly returns (post-COVID window, Jul-2023 onward) regressed on:
  MKT  SPY return
  RATE change in 10y Treasury yield (^TNX, in pct points)
  OIL  USO return
  CRED HYG return (credit / recession-odds proxy)
  CONS XLY - SPY (consumer discretionary vs market)
  SECT peer-basket return minus SPY (sector multiple / narrative)
Reports betas, R^2 (share of variance macro explains; the rest is idiosyncratic = company-specific)
and the implied stock move under the Phase-10 shocks.

Usage: python market_condition_test.py [TICKER ...]
"""

import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm

from common import PROCESSED, prices

PEERS = {"NCLH": ["RCL", "CCL"], "CPRT": ["RBA"], "SBUX": ["MCD", "CMG", "YUM"]}
SHOCKS = {  # factor moves defining each world
    "rates +100bp": {"RATE": 1.0},
    "rates -100bp": {"RATE": -1.0},
    "recession odds rise (SPY -15%, HYG -5%)": {"MKT": -0.15, "CRED": -0.05},
    "consumer weakens (XLY -10% vs SPY)": {"CONS": -0.10},
    "sector multiples compress (peers -15% vs SPY)": {"SECT": -0.15},
    "oil +30%": {"OIL": 0.30},
}


def weekly(t):
    return prices(t)["Close"].resample("W-FRI").last()


def factors(ticker):
    spy = weekly("SPY")
    f = pd.DataFrame({
        "MKT": spy.pct_change(),
        "RATE": weekly("^TNX").diff() / 10 if weekly("^TNX").max() > 20 else weekly("^TNX").diff(),
        "OIL": weekly("USO").pct_change(),
        "CRED": weekly("HYG").pct_change(),
        "CONS": weekly("XLY").pct_change() - spy.pct_change(),
    })
    peer = pd.concat([weekly(p).pct_change() for p in PEERS[ticker]], axis=1).mean(axis=1)
    f["SECT"] = peer - f["MKT"]
    return f


def run(ticker):
    for t in ["SPY", "^TNX", "USO", "HYG", "XLY"] + PEERS[ticker]:
        prices(t, refresh=not (PROCESSED.parent / "market" / f"{t}.csv").exists())
    y = weekly(ticker).pct_change().rename("y")
    X = factors(ticker)
    d = pd.concat([y, X], axis=1).loc["2023-07-01":].dropna()
    m = sm.OLS(d["y"], sm.add_constant(d.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    # Macro-only R^2 (excluding the sector factor) vs with sector
    m_macro = sm.OLS(d["y"], sm.add_constant(d[["MKT", "RATE", "OIL", "CRED", "CONS"]])).fit()
    res = {"ticker": ticker, "n_weeks": len(d), "R2_all": m.rsquared, "R2_macro_only": m_macro.rsquared,
           "idiosyncratic_share": 1 - m.rsquared}
    for k in X.columns:
        res[f"beta_{k}"], res[f"t_{k}"] = m.params[k], m.tvalues[k]
    for name, shock in SHOCKS.items():
        res[name] = sum(m.params[k] * v for k, v in shock.items())
    return res


def main():
    rows = [run(t) for t in (sys.argv[1:] or list(PEERS))]
    df = pd.DataFrame(rows).set_index("ticker").T
    df.to_csv(PROCESSED / "market_condition_test.csv")
    pd.set_option("display.width", 200)
    print(df.round(3).to_string())


if __name__ == "__main__":
    main()
