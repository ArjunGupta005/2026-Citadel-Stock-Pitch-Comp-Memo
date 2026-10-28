"""Build final/MarginCallers_StockPitch_v3.html from the v2 memo source (surgical v3 QA wording/arithmetic fixes).
Numbers come from Margin_Callers_v3.xlsx (bridge: Sensitivity sheet 'Bridge as displayed in the memo'). v2 files untouched."""
from common import ROOT

src = ROOT / "final" / "MarginCallers_StockPitch_v2.html"
dst = ROOT / "final" / "MarginCallers_StockPitch_v3.html"
s = src.read_text(encoding="utf-8")
R = [
    # 7. location count: primary 10-K (Item 2) = 286 operating facilities
    ("with more than 275 locations, more than 4 million vehicles", "with 286 operating facilities, more than 4 million vehicles"),
    # 2. RB Global wording
    ("RB Global separately disclosed a major automotive-insurance partner expanding to all 50 states, with volume transitioned over roughly the prior 90 days.",
     "RB Global said incremental volume from its largest automotive-insurance partner had been transitioning over roughly the prior 90 days as of Aug. 4, "
     "following expansion to all 50 states."),
    # 5. bridge arithmetic + lost-customer line
    ("the lost-customer line in our FY27 bridge is approximately <b>$0.23/share</b>; after pricing and share-count tailwinds,",
     "the lost-customer line in our FY27 bridge is approximately <b>$0.19/share</b>; after pricing tailwinds and fixed-cost deleverage,"),
    ("FY26 EPS $1.55 -> share count / interest +$0.05 -> lost-customer impact ($0.23) -> underlying/non-insurance growth +$0.03 -> revenue/unit +$0.10 "
     "-> fixed-facility costs ($0.05) -> other +$0.01 = <b>$1.45 ex-ACV</b>",
     "FY26 EPS $1.55 -> share count / interest / other +$0.01 -> lost-customer impact ($0.19) -> underlying/non-insurance growth +$0.03 -> "
     "revenue/unit +$0.10 -> fixed-facility costs ($0.05) = <b>$1.45 ex-ACV</b>"),
    # 3 + 10. market view
    ("<p><b>What is already known / widely discussed:</b> the customer loss, near-term margin pressure, an eventual cycle recovery, and some ACV dilution are all known. "
     "The stock has already de-rated materially.</p>",
     "<p><b>What is already known / widely discussed:</b> the lost customer, near-term margin pressure, an eventual cycle recovery, and the ACV acquisition / "
     "near-term integration economics. The stock has already de-rated materially (~18x trailing P/E vs a ~35x 2021-26 median).</p>"),
    # team-estimate label on modeled ACV dilution
    ("$1.38 including modeled ACV dilution</td>", "$1.38 including modeled ACV dilution (team estimate)</td>"),
    # 1. remove crowding claim
    ("<tr><td><b>Short is crowded / rebound after a large negative reaction</b></td>",
     "<tr><td><b>Post-earnings rebound after a large negative reaction</b></td>"),
    # 6. gross short returns
    ("a 0.5pt lower cost of equity cuts the expected short return to +1.6%.</p>",
     "a 0.5pt lower cost of equity cuts the expected short return to +1.6%. Short returns are gross of borrow, financing and transaction costs.</p>"),
    ("<title>Margin Callers - CPRT Short (v2)</title>", "<title>Margin Callers - CPRT Short (v3)</title>"),
]
for a, b in R:
    assert a in s, a[:90]
    s = s.replace(a, b)
dst.write_text(s, encoding="utf-8")
print("wrote", dst)
