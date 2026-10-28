"""Independent Python reference for Margin_Callers_v2.xlsx (corrected model, 10/2/26).

Corrections vs v1 (see 03_research_log.md, 2026-10-02):
  1. Valuation date = mid-Feb 2027 (after Q2 FY27). Forward base = NTM ex-interest EPS:
     Q3 FY27 + Q4 FY27 (modeled, incl. ACV) + Q1 FY28 + Q2 FY28.
  2. FY28 EPS = standalone CPRT (FY27 ex-ACV core operating EPS grown at g28, plus pre-ACV interest)
     + explicit FY28 ACV EPS contribution (team estimate; company guides accretive in FY28).
  3. ACV consolidated for a fraction of Q2 FY27 (base 50% = mid-Q2); company guides close by CY-end 2026.
  4. Lost-customer drag: Q4 FY26 already reflected the reported 9.8pt drag (+2.3% ex-customer vs -7.5%).
     Q1-Q3 FY27 impact = full run-rate L; Q4 FY27 impact = (1+L)/(1-9.8%) - 1.
  7. Diluted shares 932m (Q4 FY26 diluted WASO 932.1m), not 940m.
"""

FY26 = dict(
    svc=[855.5, 819.5, 895.5, 817.8], veh=[97.1, 102.2, 107.4, 112.5], fac=[398.5, 395.4, 419.7, 420.8],
    cveh=[90.0, 96.4, 99.0, 105.7], ga=[89.2, 88.4, 93.7, 91.7], ioi=[55.7, 47.2, 73.8, 56.8],
    irev=[202.4, 200.1, 234.2, 222.0], interest=[53.5, 50.0, 38.8, 39.6])
EPS26 = [0.41, 0.36, 0.43, 0.35]

BASE = dict(price=27.29, shares=932.0, tax=0.195, cash0=4.49, cash_val=3.08, int26=181.9, intq1=38.0,
            rf=0.0524, beta=0.90, erp=0.05, gT=0.03, rf_stress=0.035,
            sins=0.76, fix=0.55, nonins=0.03, goth=0.05, gint=0.10,
            ins_rep=-0.075, ins_excust=0.023, acv_frac=0.5, cons_fy27_sp=1.62)

WORLDS = [  # name, prob, drivers
    ("W1", 0.20, dict(u=-0.02, loss=-0.16, rpu=0.02, fixed=0.10, amort=20, op=-8, int_q=22, g28=0.04, g5=0.03, roic=0.15, acv28=0.00)),
    ("W2", 0.45, dict(u=0.01, loss=-0.13, rpu=0.035, fixed=0.07, amort=15, op=-4, int_q=25, g28=0.12, g5=0.06, roic=0.20, acv28=0.02)),
    ("W3", 0.20, dict(u=0.03, loss=-0.10, rpu=0.05, fixed=0.04, amort=10, op=0, int_q=28, g28=0.18, g5=0.09, roic=0.25, acv28=0.04)),
    ("W4", 0.15, dict(u=0.03, loss=-0.05, rpu=0.05, fixed=0.04, amort=10, op=0, int_q=28, g28=0.15, g5=0.10, roic=0.25, acv28=0.02)),
]


def coe(p, rf=None):
    return (p["rf"] if rf is None else rf) + p["beta"] * p["erp"]


def justified_pe(g, roic, r, gT):
    """v1 two-stage justified P/E per $1 of year-1 earnings (kept for reference)."""
    pv5 = sum((1 + g) ** (t - 1) * (1 - g / roic) / (1 + r) ** t for t in range(1, 6))
    pvt = (1 + g) ** 5 * (1 - gT / roic) / (r - gT) / (1 + r) ** 5
    return pv5 + pvt


def value_exc(e1, e2, g, roic, r, gT):
    """Ex-cash value at the valuation date: year 1 = NTM (e1), year 2 = e2 (recovery completes),
    years 3-5 grow at g, Gordon terminal on year-6 earnings. Payout = 1 - g/ROIC."""
    po = 1 - g / roic
    e = [e1, e2] + [e2 * (1 + g) ** k for k in range(1, 4)]
    pv = sum(po * e[t] / (1 + r) ** (t + 1) for t in range(5))
    tv = e[4] * (1 + g) * (1 - gT / roic) / (r - gT) / (1 + r) ** 5
    return pv + tv


def world(w, p=BASE):
    t, sh = p["tax"], p["shares"]
    obs = p["ins_excust"] - p["ins_rep"]
    q = {k: [] for k in ("imp", "ins", "core", "eps_x", "acv", "intg", "eps_g", "usoi", "ioi", "cm")}
    for i in range(4):
        imp = w["loss"] if i < 3 else (1 + w["loss"]) / (1 - obs) - 1
        ins = w["u"] + imp
        units = p["sins"] * ins + (1 - p["sins"]) * p["nonins"]
        svc = FY26["svc"][i] * (1 + units) * (1 + w["rpu"])
        vrev = FY26["veh"][i] * (1 + p["goth"])
        vgp = (FY26["veh"][i] - FY26["cveh"][i]) * (1 + p["goth"])
        fac = FY26["fac"][i] * p["fix"] * (1 + w["fixed"]) + FY26["fac"][i] * (1 - p["fix"]) * (1 + units)
        ga = FY26["ga"][i] * (1 + p["goth"])
        usoi = svc + vgp - fac - ga
        ioi = FY26["ioi"][i] * (1 + p["gint"])
        irev = FY26["irev"][i] * (1 + p["gint"])
        frac = [0, p["acv_frac"], 1, 1][i]
        acv = frac * (w["op"] - w["amort"])
        intg = frac * w["int_q"] + (1 - frac) * p["intq1"]
        q["imp"].append(imp); q["ins"].append(ins); q["usoi"].append(usoi); q["ioi"].append(ioi)
        q["core"].append((usoi + ioi) * (1 - t) / sh)
        q["eps_x"].append((usoi + ioi + p["intq1"]) * (1 - t) / sh)
        q["acv"].append(acv); q["intg"].append(intg)
        q["eps_g"].append((usoi + ioi + acv + intg) * (1 - t) / sh)
        q["cm"].append((usoi + ioi) / (svc + vrev + irev))
    o = dict(q=q)
    o["fy27x"], o["fy27g"] = sum(q["eps_x"]), sum(q["eps_g"])
    o["acv27"] = o["fy27g"] - o["fy27x"]
    o["fy28_sa"] = sum(q["core"]) * (1 + w["g28"]) + p["intq1"] * 4 * (1 - t) / sh
    o["fy28"] = o["fy28_sa"] + w["acv28"]
    forgone = (p["intq1"] - w["int_q"]) * 4 * (1 - t) / sh
    acv_q28 = (w["acv28"] + forgone) / 4          # FY28 ACV operating contribution ex-interest, per quarter
    o["ntm_parts"] = [(q["usoi"][2] + q["ioi"][2] + q["acv"][2]) * (1 - t) / sh,
                      (q["usoi"][3] + q["ioi"][3] + q["acv"][3]) * (1 - t) / sh,
                      q["core"][0] * (1 + w["g28"]) + acv_q28,
                      q["core"][1] * (1 + w["g28"]) + acv_q28]
    o["ntm_x"] = sum(o["ntm_parts"])
    # year 2 (Q3 FY28 - Q2 FY29): H2 FY28 = H2 FY27 core grown at g28 + half the FY28 ACV contribution; H1 FY29 = H1 FY28 x (1+g5)
    h2_28 = (q["core"][2] + q["core"][3]) * (1 + w["g28"]) + 2 * acv_q28
    h1_29 = (o["ntm_parts"][2] + o["ntm_parts"][3]) * (1 + w["g5"])
    o["ntm2_x"] = h2_28 + h1_29
    o["ntm_int"] = w["int_q"] * 4 * (1 - t) / sh
    o["vexc"] = value_exc(o["ntm_x"], o["ntm2_x"], w["g5"], w["roic"], coe(p), p["gT"])
    o["jpe"] = o["vexc"] / o["ntm_x"]
    o["cash_ps"] = p["cash_val"] * 1000 / sh
    o["val"] = o["vexc"] + o["cash_ps"]
    o["ret"] = o["val"] / p["price"] - 1
    return o


def run(p=BASE, worlds=WORLDS):
    res = {n: world(w, p) for n, _, w in worlds}
    probs = {n: pr for n, pr, _ in worlds}
    pw = sum(probs[n] * res[n]["val"] for n in res)
    out = dict(res=res, pw=pw, esr=-(pw / p["price"] - 1), base=res["W2"]["val"], w4loss=res["W4"]["ret"])
    w3 = dict(worlds[2][2])
    r3 = res["W3"]
    out["stress_val"] = value_exc(r3["ntm_x"], r3["ntm2_x"], w3["g5"], w3["roic"], coe(p, p["rf_stress"]), p["gT"]) + r3["cash_ps"]
    out["stress"] = out["stress_val"] / p["price"] - 1
    sh, t = p["shares"], p["tax"]
    pe_mkt = (p["price"] - p["cash0"] * 1000 / sh) / (p["cons_fy27_sp"] - p["int26"] * 0.6 * (1 - t) / sh)
    out["pe_mkt"] = pe_mkt
    out["epsonly"] = -sum(probs[n] * ((pe_mkt * res[n]["ntm_x"] + res[n]["cash_ps"]) / p["price"] - 1) for n in res)
    return out


if __name__ == "__main__":
    o = run()
    for n, r in o["res"].items():
        print(n, "Q1x %.3f FY27x %.3f ACV27 %+.3f GAAP %.3f | FY28sa %.3f FY28 %.3f | NTMx %.3f %s NTM2 %.3f | P/E %.1f val %.2f ret %+.1f%%"
              % (r["q"]["eps_x"][0], r["fy27x"], r["acv27"], r["fy27g"], r["fy28_sa"], r["fy28"], r["ntm_x"],
                 [round(x, 3) for x in r["ntm_parts"]], r["ntm2_x"], r["jpe"], r["val"], 100 * r["ret"]))
    print("PW %.2f  ESR %+.1f%%  base %.2f  W4 loss %.1f%%  stress %.1f%% (val %.2f)  EPS-only %+.1f%%  mktPE %.1f"
          % (o["pw"], 100 * o["esr"], o["base"], 100 * o["w4loss"], 100 * o["stress"], o["stress_val"], 100 * o["epsonly"], o["pe_mkt"]))
