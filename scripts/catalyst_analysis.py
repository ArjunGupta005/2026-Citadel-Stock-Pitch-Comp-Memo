"""Catalyst map per candidate: Date | Event | Our expectation | Street expectation | What changes | What investors learn
that they do not already know, plus the historical move size for that event type.

Catalyst strength is graded:
  strong = discrete, dated, reports the thesis KPI, and the answer is not already public
  medium = dated but the KPI is indirect, or partly anticipated
  weak   = undated, vague, or already widely anticipated

Output: candidates/<T>/catalyst_map.md

Usage: python catalyst_analysis.py [TICKER ...]
"""

import sys

import pandas as pd

from common import PROCESSED, ROOT

CATALYSTS = {
    "CPRT": [
        ("2026-10-07", "ACV tender offer expiry (extended; 47.8% tendered at 9/30)", "Majority tendered; closes after HSR",
         "Closes by CY-end", "Cash out ~$1.9bn; interest income falls", "Little: timing only", "weak"),
        ("2026-10-13", "HSR waiting period ends (refiled 9/28) / possible Second Request",
         "~70% clears; Second Request is a tail", "Assumes clean close",
         "Second Request → delay, deal uncertainty", "Whether antitrust scrutiny is real", "medium"),
        ("2026-11-05", "RB Global Q3-26 (IAA units, Progressive run-rate)", "IAA auto units +10%+; 'full quarter' of the partner",
         "IAA share gains continue", "Read-across sizes Copart's loss", "Run-rate size of the share shift", "medium"),
        ("2026-11-19", "CPRT Q1-FY27 results (Aug-Oct)", "US insurance units ~-12%; EPS ~$0.36",
         "EPS $0.397 (-3%); implies US ins. ~-5%", "FY27 estimates cut 10-20%",
         "First full quarter of the Progressive loss; cost/car trend under Adair", "strong"),
        ("2027-02-19", "CPRT Q2-FY27 + first ACV consolidation", "ACV GAAP-dilutive ~-$0.02/qtr", "ACV ~neutral",
         "GAAP EPS bridge incl. amortization", "Purchase-price allocation; ACV losses inside CPRT", "strong"),
        ("2027-05-20", "CPRT Q3-FY27", "Units still ~-10%", "—", "Last quarter before lapping", "Underlying cycle ex-loss", "medium"),
        ("2027-09-09", "CPRT Q4-FY27 (laps Progressive)", "Units turn ~flat", "Growth resumes",
         "Bull-case catalyst (lapping)", "Whether growth resumes", "medium (12-month edge)"),
    ],
    "NCLH": [
        ("2026-10-28", "RCL Q3-26 + 2027 color", "Strong; record 2027", "Strong", "Industry tide; Caribbean pricing",
         "Caribbean pricing into 2027", "medium"),
        ("2026-11-04", "NCLH Q3-26 results (pre-announced beat) + early 2027 color",
         "Yield ~-8% (beat -8.9%); 1H27 negative reiterated", "Q3 EPS $0.90", "Shape of the 2027 booked position",
         "2027 booked position vs 60-65% target; base-loading effect", "medium (Q3 beat known)"),
        ("2026-12-19", "CCL Q4-26 + 2027 guide", "Caribbean pricing pressure visible?", "Strong", "Read-across",
         "Industry 2027 yield guide", "medium"),
        ("2027-02-26", "NCLH Q4-26 + FY27 guidance", "FY27 Net Yield ~0 to +1% cc", "Implied ~+2% (new interest)",
         "FY27 EPS reset", "First FY27 yield guide: the thesis KPI", "strong"),
        ("2027-05-01", "NCLH Q1-27", "Yield negative (worst quarter)", "—", "Trough print", "Q1 trough depth", "medium"),
        ("2027-07-30", "NCLH Q2-27 + 2H27 visibility", "2H27 inflection or not", "Inflection",
         "Bull vs bear resolution", "Whether base-loading works", "strong"),
    ],
    "SBUX": [
        ("2026-10-29", "SBUX Q4-FY26 + FY27 guidance", "FY27 margin guide ~12.5-13.5%", "EPS $3.12 (~13.5% margin)",
         "FY27 reset", "FY27 margin path incl. modernization costs", "strong"),
        ("2027-01-27", "SBUX Q1-FY27", "Comp ~+4%", "—", "Lapping +4% comp", "Durability of transactions", "medium"),
        ("2027-04-28", "SBUX Q2-FY27", "Comp laps +7%", "—", "Harder comparison", "Comp durability", "medium"),
    ],
}


def event_move(ticker):
    r = pd.read_csv(PROCESSED / "earnings_reactions.csv", parse_dates=["date"])
    r = r[(r.ticker == ticker) & (r.date >= "2015-01-01")]
    return r["excess"].abs().median(), r["excess"].abs().quantile(0.8), len(r)


def main():
    for t in sys.argv[1:] or CATALYSTS:
        med, p80, n = event_move(t)
        lines = [f"# {t} — Catalyst map", "",
                 f"Historical earnings-day move (2-day excess vs SPY, since 2015, n={n}): median |move| {med:.1%}, 80th pct {p80:.1%}.", "",
                 "| Date | Event | Our expectation | Street expectation | What changes | What investors learn that they do not already know | Strength |",
                 "|---|---|---|---|---|---|---|"]
        for c in CATALYSTS[t]:
            lines.append("| " + " | ".join(c) + " |")
        strong_in_window = [c for c in CATALYSTS[t] if c[6] == "strong" and c[0] <= "2027-09-30"]
        lines += ["", f"Strong catalysts inside the 2026-10-01 → 2027-09-30 window: {len(strong_in_window)} "
                      f"(first: {strong_in_window[0][0] if strong_in_window else 'none'}). R3 {'passes' if strong_in_window else 'FAILS'}."]
        out = ROOT / "candidates" / t / "catalyst_map.md"
        out.write_text("\n".join(lines), encoding="utf-8")
        print(t, f"median move {med:.1%}", f"strong catalysts: {len(strong_in_window)}", "->", out.name)


if __name__ == "__main__":
    main()
