"""Phase 3: write 02_candidate_scorecard.xlsx from screen data + documented scores."""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from common import PROCESSED, ROOT

QUAL = {
    "ABNB": ("Nights & Seats Booked, ADR, GBV, take rate, Adj. EBITDA margin",
             "Can nights growth hold ~10%+ (hotels, services, AI product) or is 2026 a peak? MS: low-DD nights already priced.",
             "Discretionary travel / consumer; FX (USD); regulation of STR in key cities"),
    "ADBE": ("Total Adobe ARR, customer-group subscription revenue, RPO/cRPO, AI-first ARR, MAU",
             "Is gen-AI eroding Creative Cloud seats/pricing (terminal value) vs. AI monetization? New CEO Dec 1.",
             "Enterprise IT budgets; FX; low macro beta to consumer"),
    "CPRT": ("Global/US insurance units, ASP, revenue per unit, total loss frequency, inventory",
             "Is unit decline cyclical (fewer claims, coverage pullback) or structural (share loss/ADAS)? ASP vs volume.",
             "Used-car prices (Manheim), miles driven, auto insurance affordability, rates (interest income on cash)"),
    "GEV": ("Orders, backlog/RPO, gas GW slots, segment EBITDA margin, FCF",
            "Cyclical turbine upcycle vs. secular compounder; how much of 2028-30 is priced at 39x fwd P/E.",
            "Power demand / data-center capex, rates (long-duration multiple), policy (IRA, wind)"),
    "NCLH": ("Net Yield (cc), Adj. NCC ex-fuel per capacity day, occupancy, capacity days, net leverage",
             "Is NCL-brand yield weakness company-specific & fixable (GSC, revenue mgmt) or structural? Has 2027 reset enough?",
             "Consumer discretionary, fuel, Middle East/geopolitics, rates (5.3x net leverage), Caribbean pricing"),
    "NKE": ("Revenue by geo/channel, NIKE Direct & Digital, gross margin, inventory, Converse",
            "Turnaround timing: when do wholesale gains offset Direct/China declines; GM recovery vs promotions & tariffs.",
            "Consumer, China, tariffs (IEEPA refunds), FX"),
    "SBUX": ("Comparable sales (transactions/ticket) by region, store count, non-GAAP op margin",
             "Is +8% comp / Back-to-Starbucks durable and is 30x P/E already pricing FY27 margin recovery?",
             "Consumer spending, coffee/dairy input costs, labor, China JV"),
    "SPOT": ("MAU, Premium subs, ARPU, gross margin, operating income, FCF",
             "Margin expansion vs. EUR 200M AI/marketing reinvestment; label economics capping GM; pricing power.",
             "FX (EUR reporting/USD trading), consumer subscription churn; low cyclicality"),
}

CRITERIA = ["Data observability", "KPI transparency", "Potential consensus disagreement", "Catalyst visibility",
            "Ability to model", "Risk/reward asymmetry", "Availability of historical data", "Industry complexity (5 = simple)"]

# (score, rationale) per criterion. Anchored on screen.csv / screen_proxies.csv where possible.
SCORES = {
    "ABNB": [(4, "AirDNA/web/app traffic, hotel peers"), (5, "Nights, ADR, GBV reported & guided"),
             (3, "EPS disp 0.41; tgt disp 0.46 (low); debate is nights growth, MS says priced"),
             (4, "Q3 11/05; Q4 Feb w/ 2027 outlook"), (5, "Nights x ADR x take rate"),
             (3, "P/S 30th pctile; 26x fwd P/E; +32% 52w"), (3, "6.5 yrs, COVID-distorted"), (4, "Simple marketplace")],
    "ADBE": [(3, "Seats not disclosed; alt data noisy"), (3, "ARR metric redefined; no unit KPI"),
             (3, "EPS disp only 0.12 -> Street agrees on EPS; fight is terminal value (multiple) -> R8 risk"),
             (4, "Q4 + FY27 guide 12/09; CEO starts 12/01"), (4, "ARR -> revenue -> margin straightforward"),
             (4, "P/S 19th pctile; 8.7x fwd P/E"), (5, "18 yrs"), (2, "AI disruption hard to falsify in 12m")],
    "CPRT": [(4, "Manheim monthly, CCC total-loss data, RB Global/IAA peer"), (3, "Units/ASP mostly in call, not tabled"),
             (4, "EPS disp 0.12 but tgt disp 0.77; cyclical vs structural units is a clean fight; FY1 EPS -5.4% 90d"),
             (4, "Q1 FY27 ~11/19; RBA early Nov; Manheim monthly"), (4, "Units x revenue/unit"),
             (3, "15.6x fwd P/E (decade low) but P/S 45th pctile on 17y; -39% 52w"), (5, "17 yrs incl. 2008, 2020"),
             (5, "Simple two-sided auction")],
    "GEV": [(4, "Orders/backlog/GW slots disclosed"), (4, "Segment KPIs clear"),
            (2, "Disagreement is the multiple, not near-term EPS"), (4, "Q3 10/28; investor update"),
            (2, "3 segments, wind losses, Prolec, long-cycle accounting"), (2, "P/S 80th pctile; 62x EBITDA"),
            (1, "3.5 yrs since spin"), (2, "Long-cycle industrial")],
    "NCLH": [(4, "Cruise pricing trackers, RCL/CCL read-across, fuel"),
             (5, "Net yield, NCC ex-fuel, capacity, occupancy guided quarterly"),
             (5, "EPS disp 0.44, tgt disp 0.94, 23% short, FY1 EPS -18% in 90d"),
             (5, "Q3 11/04 w/ 2027 color; RCL/CCL prints; Q4 Feb 2027 guide; GSC opened 9/04"),
             (5, "Capacity x yield - NCC - fuel; leverage explicit"),
             (4, "P/S 0th pctile (all-time low); 5.3x lev = fat tails both ways"),
             (4, "14.5 yrs (COVID gap)"), (4, "Well-understood unit economics")],
    "NKE": [(3, "Sell-through mostly proprietary"), (4, "Geo x channel, GM, inventory; tariff-refund noise"),
            (4, "EPS disp 0.82, tgt disp 1.56 (highest); but fight is timing"),
            (3, "Q1 reports 10/01 (resolves before pitch); next ~Dec"), (4, "Geo x channel build"),
            (4, "P/S 6th pctile; 12-yr low"), (5, "18 yrs"), (3, "Tariffs/IEEPA refunds, FX, China, channel mix")],
    "SBUX": [(5, "Foot-traffic & card data"), (5, "Comps split into transactions/ticket by region"),
             (3, "EPS disp 0.14 -> Street converged after raise"), (4, "Q4 + FY27 guide 10/28"),
             (4, "China JV deconsolidation complicates comps"), (2, "P/S 65th pctile; 30x P/E after re-rating"),
             (5, "17.75 yrs"), (4, "Simple unit economics")],
    "SPOT": [(3, "App data for MAU"), (5, "MAU, subs, ARPU, GM guided"), (3, "Moderate: reinvestment vs margin"),
             (4, "Q3 10/22 (3 wks); Q4 Feb"), (5, "Subs x ARPU"), (3, "28x fwd P/E; -31% 52w"),
             (2, "No quarterly XBRL (6-K filer); manual history"), (3, "Label economics, FX, social charges")],
}

PCT_ROWS = {"Rev growth last Q y/y", "Cons. rev growth FY0", "Cons. rev growth FY1", "Op margin last Q",
            "Op margin yr-ago Q", "Last earnings 2d excess vs SPY", "Avg abs earnings move (8Q)",
            "FY1 EPS revision 90d", "Short % float", "52w perf", "P/S percentile vs own history"}


def main():
    s = pd.read_csv(PROCESSED / "screen.csv").set_index("ticker")
    p = pd.read_csv(PROCESSED / "screen_proxies.csv").set_index("ticker")
    hdr_font, hdr_fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F3864")
    wrap = Alignment(wrap_text=True, vertical="top")
    wb = Workbook()

    ws = wb.active
    ws.title = "Scorecard"
    ws.append(["Ticker"] + CRITERIA + ["Total", "Rank", "Advance?"])
    for i, t in enumerate(SCORES, 2):
        ws.cell(i, 1, t)
        for j, (sc, _) in enumerate(SCORES[t], 2):
            ws.cell(i, j, sc).font = Font(color="0000FF")
        ws.cell(i, 10, f"=SUM(B{i}:I{i})")
        # Tie-break on consensus disagreement (col D): an edge requires disagreement.
        ws.cell(i, 11, f'=RANK(J{i},$J$2:$J$9)+COUNTIFS($J$2:$J$9,J{i},$D$2:$D$9,">"&D{i})')
        ws.cell(i, 12, f'=IF(K{i}<=3,"ADVANCE","drop")')
    ws.cell(11, 1, "Scale 1-5, 5 = most favourable to a falsifiable edge. Equal weights. Ties broken by "
                   "'Potential consensus disagreement'. Not a 'which stock do I like' score. "
                   "Rationale for every score on the 'Rationale' tab.")

    r = wb.create_sheet("Rationale")
    r.append(["Ticker"] + CRITERIA)
    for t, sc in SCORES.items():
        r.append([t] + [f"{a} - {b}" for a, b in sc])

    d = wb.create_sheet("Screen data")
    fields = [("Price", "price"), ("Mkt cap ($bn)", "mkt_cap_bn"), ("EV ($bn)", "ev_bn"), ("Fwd P/E (NTM)", "fwd_pe"),
              ("EV/EBITDA (LTM)", "ev_ebitda_ltm"), ("EV/Sales (LTM)", "ev_sales_ltm"),
              ("EV/Sales (next FY cons.)", "ev_sales_fy1"), ("Rev growth last Q y/y", "rev_yoy_lastQ"),
              ("Cons. rev growth FY0", "rev_growth_fy0_cons"), ("Cons. rev growth FY1", "rev_growth_fy1_cons"),
              ("Op margin last Q", "op_margin_lastQ"), ("Op margin yr-ago Q", "op_margin_yrago"),
              ("Last earnings date", "last_er_date"), ("Last earnings 2d excess vs SPY", "last_er_excess_2d"),
              ("Avg abs earnings move (8Q)", "avg_abs_er_move_8q"), ("Next earnings date", "next_er_date"),
              ("FY1 EPS revision 90d", "fy1_eps_rev_90d"), ("# analysts", "n_analysts"), ("Mean target", "target_mean"),
              ("Short % float", "short_pct_float"), ("52w perf", "perf_52w")]
    d.append(["Metric"] + list(s.index))
    for label, f in fields:
        d.append([label] + [s.loc[t, f] for t in s.index])
    for label, f in [("FY1 EPS est. dispersion (hi-lo)/avg", "est_dispersion_fy1"),
                     ("Target dispersion (hi-lo)/mean", "tgt_dispersion"),
                     ("P/S percentile vs own history", "ps_pctile_own_hist"), ("Years quarterly XBRL", "years_qtr_hist"),
                     ("Earnings move / normal 2d move", "er_move_ratio")]:
        d.append([label] + [p.loc[t, f] for t in s.index])
    for label, idx in [("Key reported KPIs", 0), ("Primary debate", 1), ("Main macro exposure", 2)]:
        d.append([label] + [QUAL[t][idx] for t in s.index])
    d.append([])
    d.append(["Source: yfinance (prices, consensus, multiples) as of 2026-10-01; SEC EDGAR XBRL + 8-K/6-K filing dates; "
              "screen.py, screen_proxies.py. P/S percentile uses current share count (approximate)."])

    for sh in wb.worksheets:
        for c in sh[1]:
            c.font, c.fill = hdr_font, hdr_fill
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        sh.row_dimensions[1].height = 45
        for col in range(1, sh.max_column + 1):
            sh.column_dimensions[get_column_letter(col)].width = 34 if sh.title != "Scorecard" else 14
        for row in sh.iter_rows(min_row=2):
            pct = sh.title == "Screen data" and row[0].value in PCT_ROWS
            for c in row:
                c.alignment = wrap
                if isinstance(c.value, float):
                    c.number_format = "0.0%" if pct else "0.00"
    wb.save(ROOT / "02_candidate_scorecard.xlsx")

    tot = {t: sum(a for a, _ in sc) for t, sc in SCORES.items()}
    dis = {t: SCORES[t][2][0] for t in SCORES}
    for t in sorted(tot, key=lambda t: (-tot[t], -dis[t])):
        print(t, tot[t], "disagreement", dis[t])


if __name__ == "__main__":
    main()
