"""KPI-driven earnings models and bear / base / bull economic worlds for the finalists.

Each model is driven by the KPI that explains most of the earnings variance:
  CPRT  US insurance units (underlying cycle + Progressive loss) x revenue per unit, with fixed/variable facility costs
  NCLH  capacity days x Net Yield - NCC ex-fuel - fuel -> EBITDA -> EPS
  SBUX  NA comp + units -> revenue x non-GAAP operating margin -> EPS

For each world it reports EPS, the valuation multiple, price target and return, the share of the price change
explained by EPS vs multiple (R8), expected value, upside/downside ratio (R5), and the KPI value consensus implies.

Usage: python scenario_engine.py [TICKER ...]
"""

import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from common import PROCESSED

PRICE = {"CPRT": 27.29, "NCLH": 14.64, "SBUX": 94.88}
# Yahoo earningsTrend, pulled 2026-10-01 16:45 ET (period end dates verified in audit/consensus_integrity.md).
# CPRT FY27 = period ending 2027-07-31 (n=8); Q2FY27 = period ending 2027-01-31.
CONSENSUS = {"CPRT": {"FY27": 1.75, "Q2FY27": 0.37454}, "NCLH": {"FY27": 1.67}, "SBUX": {"FY27": 3.12}}
WEIGHTS = {"bear": 0.25, "base": 0.50, "bull": 0.25}  # pre-registered default (04_restart_criteria R5)


# ------------------------------------------------------------------ CPRT
# FY26 quarterly segment actuals ($m) from 10-Qs / 10-K (Q4 = FY - 9M). Order: Q1 (Aug-Oct) .. Q4 (May-Jul).
CPRT_FY26 = {
    "us_service": [855.5, 819.5, 895.5, 817.8], "us_vehicle": [97.1, 102.2, 107.4, 112.5],
    "us_facility": [398.5, 395.4, 419.7, 420.8], "us_cogs_vehicle": [90.0, 96.4, 99.0, 105.7],
    "us_ga": [89.2, 88.4, 93.7, 91.7],
    "intl_oi": [55.7, 47.2, 73.8, 56.8],
    "interest": [53.5, 50.0, 38.8, 39.6],
}
CPRT_SHARES = 940.0      # diluted, millions
CPRT_TAX = 0.195
CPRT_US_INS_SHARE = 0.76  # share of US units from insurance
CPRT_FIXED_SHARE = 0.55   # share of US facility cost that does not flex with units in the near term
# Fraction of the Progressive run-rate loss already in the FY26 quarter (ramp May-Jul 2026 per RBA).
CPRT_LOSS_IN_BASE = [0.0, 0.0, 0.0, 0.6]

CPRT_WORLDS = {
    #            underlying US ins growth, run-rate loss, RPU growth, fixed-cost growth, ACV amort/q, ACV op/q, interest/q post-close, FY28 EPS growth, P/E
    # P/E anchors: bear 14x (< RBA 16.8x, < own 10th pct 18x); base 16x (today's 15.6x NTM held);
    # bull 21x (~own 25th pct; ~peer median 20x)
    "bear": dict(u=-0.02, loss=-0.16, rpu=0.020, fixed=0.10, acv_amort=20, acv_op=-8, int_q=22, g28=0.04, pe=14.0),
    "base": dict(u=0.01, loss=-0.13, rpu=0.035, fixed=0.07, acv_amort=15, acv_op=-4, int_q=25, g28=0.12, pe=16.0),
    "bull": dict(u=0.03, loss=-0.10, rpu=0.050, fixed=0.04, acv_amort=10, acv_op=0, int_q=28, g28=0.18, pe=21.0),
}


def cprt_quarters(w, calibrate=False, include_acv=True):
    """Quarterly FY27 build. ACV is consolidated from Q2 (close ~mid-Oct 2026).

    calibrate=True: zero growth, FY26 interest and no ACV, which should reproduce FY26 GAAP EPS.
    include_acv=False: strips ACV operating loss, amortization and the interest forgone on its purchase price
    (for comparison with consensus models that exclude the deal).
    """
    g_other, g_intl, non_ins = (0.0, 0.0, 0.0) if calibrate else (0.05, 0.10, 0.03)
    out = []
    for q in range(4):
        incremental_loss = 0.0 if calibrate else w["loss"] * (1 - CPRT_LOSS_IN_BASE[q])
        us_ins = (0.0 if calibrate else w["u"]) + incremental_loss
        us_units = CPRT_US_INS_SHARE * us_ins + (1 - CPRT_US_INS_SHARE) * non_ins
        rpu = 0.0 if calibrate else w["rpu"]
        service = CPRT_FY26["us_service"][q] * (1 + us_units) * (1 + rpu)
        vehicle_rev = CPRT_FY26["us_vehicle"][q] * (1 + g_other)
        vehicle_gp = (CPRT_FY26["us_vehicle"][q] - CPRT_FY26["us_cogs_vehicle"][q]) * (1 + g_other)
        fac = CPRT_FY26["us_facility"][q]
        fixed = 0.0 if calibrate else w["fixed"]
        facility = fac * CPRT_FIXED_SHARE * (1 + fixed) + fac * (1 - CPRT_FIXED_SHARE) * (1 + us_units)
        ga = CPRT_FY26["us_ga"][q] * (1 + g_other)
        us_oi = service + vehicle_gp - facility - ga
        intl_oi = CPRT_FY26["intl_oi"][q] * (1 + g_intl)
        acv = 0 if (q == 0 or calibrate or not include_acv) else (w["acv_op"] - w["acv_amort"])
        if calibrate:
            interest = CPRT_FY26["interest"][q]
        elif not include_acv:
            interest = 38.0  # cash not spent on ACV: Q1 run-rate held
        else:
            interest = 38.0 if q == 0 else w["int_q"]
        pretax = us_oi + intl_oi + acv + interest
        out.append(dict(q=q + 1, us_units_yoy=us_units, us_ins_units_yoy=us_ins, us_service=service,
                        us_vehicle_rev=vehicle_rev, us_oi=us_oi, intl_oi=intl_oi, acv_pretax=acv, interest=interest,
                        pretax=pretax, eps=pretax * (1 - CPRT_TAX) / CPRT_SHARES))
    return out


def cprt_eps(w):
    return [r["eps"] for r in cprt_quarters(w)]


def cprt():
    rows = []
    for name, w in CPRT_WORLDS.items():
        q = cprt_eps(w)
        fy27 = sum(q)
        fy28 = fy27 * (1 + w["g28"])
        rows.append(dict(world=name, q1=q[0], fy27=fy27, ntm_eps_at_horizon=fy28, multiple=w["pe"], target=fy28 * w["pe"]))
    # AUDIT 2026-10-01: the earlier "Q1-FY27 consensus $0.397" was Yahoo's stale Q4-FY26 estimate (period end
    # 2026-07-31), so the Q1-implied unit back-solve was withdrawn. Back-solve on Q2-FY27 (period end 2027-01-31) instead.
    implied = brentq(lambda L: cprt_eps({**CPRT_WORLDS["base"], "loss": L})[1] - CONSENSUS["CPRT"]["Q2FY27"], -0.6, 0.4)
    return rows, {"Q2 US insurance units y/y implied by Street Q2 EPS (base costs, incl. ACV)": CPRT_WORLDS["base"]["u"] + implied,
                  "Our base Q2 US insurance units y/y": CPRT_WORLDS["base"]["u"] + CPRT_WORLDS["base"]["loss"]}


# ------------------------------------------------------------------ NCLH
NCLH_FY26 = dict(cd=26.25, net_yield=301.10 * 0.95, ncc_xfuel_pcd=161.3, fuel_mt=1.020, fuel_px=715, da=1085,
                 interest=705, ebitda=2500)
NCLH_SHARES = 462.0
NCLH_NET_DEBT_YE26 = 15.3  # $bn, ">6x" on ~$2.5bn

NCLH_WORLDS = {
    #            capacity, yield, NCC xfuel/CD, fuel px, FY28 EBITDA growth, EV/EBITDA, YE27 net debt ($bn)
    # EV/EBITDA anchors: bear 7.0x (< CCL 7.8x; credit stress); base 8.0x (today's ~7.9x on Street FY27 EBITDA held);
    # bull 9.5x (toward pre-2026 ~10x; still < RCL 13.6x)
    "bear": dict(cap=0.05, ny=-0.02, ncc=0.020, fuel=0.10, g28=0.03, ev_mult=7.0, nd=15.8),
    "base": dict(cap=0.05, ny=0.010, ncc=0.010, fuel=0.00, g28=0.07, ev_mult=8.0, nd=15.3),
    "bull": dict(cap=0.05, ny=0.030, ncc=-0.005, fuel=-0.10, g28=0.10, ev_mult=9.5, nd=14.8),
}


def nclh_fy27(w):
    cd = NCLH_FY26["cd"] * (1 + w["cap"])
    agm = NCLH_FY26["net_yield"] * (1 + w["ny"]) * cd
    ncc = NCLH_FY26["ncc_xfuel_pcd"] * (1 + w["ncc"]) * cd
    fuel = NCLH_FY26["fuel_mt"] * (1 + w["cap"] * 0.8) * NCLH_FY26["fuel_px"] * (1 + w["fuel"])
    ebitda = agm - ncc - fuel
    da = NCLH_FY26["da"] * 1.07
    ni = ebitda - da - 870 - 10
    return ebitda, ni / NCLH_SHARES


def nclh():
    rows = []
    for name, w in NCLH_WORLDS.items():
        ebitda, eps = nclh_fy27(w)
        ebitda28 = ebitda * (1 + w["g28"])
        equity = ebitda28 * w["ev_mult"] / 1000 - w["nd"]
        target = equity * 1000 / NCLH_SHARES
        rows.append(dict(world=name, fy27_ebitda=ebitda, fy27=eps, ntm_eps_at_horizon=np.nan, multiple=w["ev_mult"],
                         target=target))
    implied = brentq(lambda y: nclh_fy27({**NCLH_WORLDS["base"], "ny": y})[1] - CONSENSUS["NCLH"]["FY27"], -0.1, 0.1)
    # Same, but if the Street still carried ~$730m of interest (pre-9/30 guide)
    implied_old = brentq(lambda y: nclh_fy27({**NCLH_WORLDS["base"], "ny": y})[1] + 140 / NCLH_SHARES
                         - CONSENSUS["NCLH"]["FY27"], -0.1, 0.1)
    calib, _ = nclh_fy27(dict(cap=0, ny=0, ncc=0, fuel=0))
    return rows, {"FY27 Net Yield implied by Street EPS (new $870m interest)": implied,
                  "FY27 Net Yield implied if Street still uses ~$730m interest": implied_old,
                  "Calibration: model FY26 EBITDA ($m, guide ~2,500)": calib}


# ------------------------------------------------------------------ SBUX
SBUX_FY26 = dict(revenue=37990, margin=0.117, interest=560, tax=0.235, shares=1140)
SBUX_WORLDS = {
    #           NA comp, NA units, intl+CD growth, China-deconsolidation revenue drag, op margin, P/E
    # P/E anchors: bear 24x (de-rate toward peers 19.6x); base 29x (~today's 30x); bull 32x
    "bear": dict(comp=0.02, units=-0.01, other=0.03, china=-0.025, margin=0.122, pe=24.0),
    "base": dict(comp=0.04, units=-0.005, other=0.05, china=-0.025, margin=0.130, pe=29.0),
    "bull": dict(comp=0.06, units=0.0, other=0.07, china=-0.025, margin=0.138, pe=32.0),
}
SBUX_NA_WEIGHT = 0.78


def sbux_fy27(w):
    rev = SBUX_FY26["revenue"] * (1 + SBUX_NA_WEIGHT * (w["comp"] + w["units"]) + (1 - SBUX_NA_WEIGHT) * w["other"] + w["china"])
    eps = (rev * w["margin"] - SBUX_FY26["interest"]) * (1 - SBUX_FY26["tax"]) / SBUX_FY26["shares"]
    return rev, eps


def sbux():
    rows = []
    for name, w in SBUX_WORLDS.items():
        rev, eps = sbux_fy27(w)
        fy28 = eps * 1.12
        rows.append(dict(world=name, fy27_revenue=rev, fy27=eps, ntm_eps_at_horizon=fy28, multiple=w["pe"], target=fy28 * w["pe"]))
    implied = brentq(lambda m: sbux_fy27({**SBUX_WORLDS["base"], "margin": m})[1] - CONSENSUS["SBUX"]["FY27"], 0.05, 0.25)
    return rows, {"FY27 non-GAAP op margin implied by Street EPS (base revenue)": implied}


# ------------------------------------------------------------------ risk / reward
def summarize(ticker, rows, implied, current_multiple):
    df = pd.DataFrame(rows).set_index("world")
    p = PRICE[ticker]
    df["return"] = df["target"] / p - 1
    cons = CONSENSUS[ticker]["FY27"]
    df["eps_vs_street"] = df["fy27"] / cons - 1
    # R8 decomposition: log price change split into EPS-driven and multiple-driven parts (P/E names only).
    if "ntm_eps_at_horizon" in df and df["ntm_eps_at_horizon"].notna().all():
        eps_now = cons  # market prices Street FY27 at today's multiple
        df["from_eps"] = np.log(df["ntm_eps_at_horizon"] / eps_now)
        df["from_multiple"] = np.log(df["multiple"] / current_multiple)
        tot = df["from_eps"] + df["from_multiple"]
        df["share_from_multiple"] = df["from_multiple"] / tot.where(tot.abs() > 1e-9)
    ev = sum(WEIGHTS[w] * df.loc[w, "return"] for w in WEIGHTS)
    up, down = df.loc["bull", "return"], df.loc["bear", "return"]
    base = df.loc["base", "return"]
    out = {"expected_return_25_50_25": ev, "bull_return": up, "bear_return": down, "base_return": base,
           "LONG  R5 ratio (base gain / bear loss)": base / abs(down) if down < 0 else np.inf,
           "LONG  EV": ev,
           "SHORT R5 ratio (base gain / bull loss)": -base / up if up > 0 else np.inf,
           "SHORT EV": -ev}
    for side in ("LONG", "SHORT"):
        r = out[f"{side}  R5 ratio (base gain / bear loss)" if side == "LONG" else f"{side} R5 ratio (base gain / bull loss)"]
        e = out[f"{side}  EV" if side == "LONG" else f"{side} EV"]
        out[f"{side} R5 verdict"] = "pass" if (r >= 2.0 and e >= 0.10) else "FAIL"
    return df, {**implied, **out}


def main():
    pd.set_option("display.width", 220)
    models = {"CPRT": (cprt, 27.29 / 1.75), "NCLH": (nclh, 14.64 / 1.67), "SBUX": (sbux, 94.88 / 3.12)}
    for t in sys.argv[1:] or models:
        fn, cur_mult = models[t]
        rows, implied = fn()
        df, stats = summarize(t, rows, implied, cur_mult)
        df.to_csv(PROCESSED / f"{t}_scenarios.csv")
        print(f"===== {t} (price ${PRICE[t]}, Street FY27 EPS ${CONSENSUS[t]['FY27']})")
        print(df.round(3).to_string())
        for k, v in stats.items():
            print(f"  {k}: {v:.3f}" if isinstance(v, float) else f"  {k}: {v}")


if __name__ == "__main__":
    main()
