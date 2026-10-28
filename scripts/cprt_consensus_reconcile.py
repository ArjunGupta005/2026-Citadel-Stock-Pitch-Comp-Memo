"""CPRT Framework B: consensus reconciliation and side-by-side expected returns under two consensus datasets.
Scenario logic, worlds and probabilities are imported unchanged from cprt_framework_b.FOUR.
Two valuation readings per dataset:
  (a) Full bridge: justified P/E per world (unchanged; independent of consensus)
  (b) EPS-only: today's market ex-cash, ex-interest NTM multiple on that dataset's FY27 held constant; only EPS changes
      (this isolates "does the short work without any multiple compression?")
"""
import numpy as np
import scenario_engine as se
import cprt_framework_b as fb
from common import ROOT

L = []
def p(s=""):
    L.append(s); print(s)

DATASETS = {
    "Yahoo (stale-mixed) FY27 $1.75": dict(fy27=1.75, q1=None, q2=0.3745),
    "S&P Global FY27 $1.62 / Zacks Q1 $0.41": dict(fy27=1.62, q1=0.41, q2=0.37),
}
cash_now = fb.CASH_PRE_ACV * 1000 / fb.SHARES
ex_cash_price = fb.PRICE - cash_now
int_adj = fb.interest_eps(182 / 4) * 0.6
r = fb.coe()

base_w = se.CPRT_WORLDS["base"]
q1_ours = se.cprt_quarters(base_w, include_acv=False)[0]["eps"]
q2_ours_x = se.cprt_quarters(base_w, include_acv=False)[1]["eps"]
fy27_x = sum(q["eps"] for q in se.cprt_quarters(base_w, include_acv=False))
p("# CPRT — consensus reconciliation and side-by-side distribution (scripts/cprt_consensus_reconcile.py)")
p()
p("## Gaps vs each dataset (ACV-excluded basis; S&P revenue $4.8bn confirms its FY27 excludes ACV)")
p("| Dataset | Q1-FY27 cons. | Our Q1 | Gap | Q2 cons. | Our Q2 ex-ACV | Gap | FY27 cons. | Our FY27 ex-ACV | Gap |")
p("|---|---|---|---|---|---|---|---|---|---|")
for k, d in DATASETS.items():
    q1g = f"{q1_ours / d['q1'] - 1:+.1%}" if d["q1"] else "n/a"
    p(f"| {k} | {d['q1'] or 'n/a'} | {q1_ours:.3f} | {q1g} | {d['q2']} | {q2_ours_x:.3f} | {q2_ours_x / d['q2'] - 1:+.1%} | "
      f"{d['fy27']} | {fy27_x:.3f} | {fy27_x / d['fy27'] - 1:+.1%} |")
p()
for k, d in DATASETS.items():
    mkt_pe = ex_cash_price / (d["fy27"] - int_adj)
    p(f"## {k}: market ex-cash, ex-interest NTM P/E = {mkt_pe:.1f}x")
    p("| World | Prob. | FY28 ex-int EPS | (a) Full-bridge value | (a) Return | (b) EPS-only value | (b) Return | Multiple part of (a), log |")
    p("|---|---|---|---|---|---|---|---|")
    eva = evb = 0
    ra, rb = [], []
    for name, (prob, w, g28, g5, roic) in fb.FOUR.items():
        fy28_x = sum(q["eps"] for q in se.cprt_quarters(w)) * (1 + g28) - fb.interest_eps(w["int_q"])
        cash_h = fb.CASH_YE_FY27 * 1000 / fb.SHARES
        va = fb.justified_pe(g5, roic, r) * fy28_x + cash_h
        vb = mkt_pe * fy28_x + cash_h
        a, b = va / fb.PRICE - 1, vb / fb.PRICE - 1
        eva += prob * a; evb += prob * b; ra.append(a); rb.append(b)
        p(f"| {name} | {prob:.2f} | {fy28_x:.2f} | ${va:.2f} | {a:+.1%} | ${vb:.2f} | {b:+.1%} | {np.log(fb.justified_pe(g5, roic, r) / mkt_pe):+.1%} |")
    p(f"- **Short expected return: (a) full bridge {-eva:+.1%}; (b) EPS-only, no multiple change {-evb:+.1%}**")
    p(f"- Max plausible short loss: (a) {max(ra):+.1%}; (b) {max(rb):+.1%}")
    p()
(ROOT / "framework_B" / "CPRT_consensus_reconciliation.md").write_text("\n".join(L), encoding="utf-8")
