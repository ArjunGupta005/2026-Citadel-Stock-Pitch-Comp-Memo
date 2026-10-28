"""Extract company-specific KPIs from earnings releases, transcripts and XBRL, point-in-time.

Every value carries the date it became public (release / filing date) so backtests can use it
without look-ahead. Output: data/processed/<T>_kpis.csv (long format: period_end, released, kpi, value, source)

  NCLH  release tables: Net Yield ($, y/y reported & constant currency), Adj. NCC ex-fuel per capacity day,
        capacity days, occupancy, Adjusted EPS, Adjusted EBITDA; guidance table (next Q / FY)
  SBUX  release comp tables: first segment (Americas -> North America) comps / transactions / ticket;
        headline global & U.S. comps sentences
  CPRT  XBRL service revenue, vehicle sales, gross profit, interest income, EPS; transcript takeaways for units/ASP

Usage: python kpi_extract.py [TICKER ...]
"""

import re
import sys

import numpy as np
import pandas as pd

from common import PROCESSED, REVENUE_TAGS, TRANSCRIPTS, xbrl_quarterly

TEXT = PROCESSED / "text"
NUM = r"\(?-?\$?\s?[\d,]+\.?\d*\)?"


def to_num(s):
    s = s.strip().replace("$", "").replace(",", "").replace("~", "").replace("%", "").strip()
    neg = s.startswith("(") or s.startswith("-")
    s = s.strip("()-").strip()
    try:
        v = float(s)
    except ValueError:
        return np.nan
    return -v if neg else v


def row_values(line):
    return [to_num(c) for c in line.split("|")[1:] if re.search(r"\d", c)]


def releases(ticker):
    """Earnings-release text files with release date, oldest first."""
    out = []
    for f in sorted((TEXT / ticker).glob("8-K_*.txt")):
        out.append((pd.Timestamp(f.name.split("_")[1]), f.read_text(encoding="utf-8")))
    return out


def quarter_ends(ticker):
    return xbrl_quarterly(ticker, REVENUE_TAGS).index


def period_for(release_date, ends):
    """Latest fiscal quarter end before the release date."""
    prior = ends[ends < release_date]
    return prior[-1] if len(prior) else pd.NaT


def first_row(text, label, after=0):
    for m in re.finditer(rf"^{re.escape(label)}\s*\|.*$", text[after:], re.M):
        return m.group(0)
    return None


# ---------------- NCLH ----------------

def nclh(rows):
    ends = quarter_ends("NCLH")
    for d, t in releases("NCLH"):
        per = period_for(d, ends)
        add = lambda k, v, src="release": rows.append(("NCLH", per, d, k, v, src))
        # Actuals table: the "Net Yield | $ ..." row with dollar levels (current, [cc], prior, ...)
        for line in re.findall(r"^Net Yield \|.*$", t, re.M):
            v = row_values(line)
            if len(v) >= 3 and all(x > 50 for x in v[:3]):
                n3 = 3 if len(v) in (3, 6) else 4 if len(v) == 8 else 3
                cur, cc, prior = v[0], v[1], v[n3 - 1]
                add("net_yield_level", cur)
                add("net_yield_yoy_reported", cur / prior - 1)
                add("net_yield_yoy_cc", cc / prior - 1)
                break
        for label in ("Adjusted Net Cruise Cost Excluding Fuel per Capacity Day",
                      "Adjusted Net Cruise Cost excluding Fuel per Capacity Day"):
            for line in re.findall(rf"^{label} \|.*$", t, re.M):
                v = row_values(line)
                if len(v) >= 3 and all(x > 50 for x in v[:3]):
                    n3 = 3 if len(v) in (3, 6) else 4 if len(v) == 8 else 3
                    add("adj_ncc_xfuel_pcd", v[0])
                    add("adj_ncc_xfuel_yoy_cc", v[1] / v[n3 - 1] - 1)
                    break
        for line in re.findall(r"^Capacity Days \|.*$", t, re.M):
            v = row_values(line)
            if len(v) >= 2 and v[0] > 1e6:
                add("capacity_days", v[0])
                add("capacity_days_yoy", v[0] / v[-1 if len(v) == 2 else (2 if len(v) in (3, 6) else 1)] - 1)
                break
        for line in re.findall(r"^Occupancy Percentage \|.*$", t, re.M):
            v = row_values(line)
            if v:
                add("occupancy", v[0])
                break
        for line in re.findall(r"^Adjusted EPS \|.*$", t, re.M):
            v = row_values(line)
            if len(v) >= 2 and "to" not in line and "Approx" not in line:
                add("adj_eps", v[0])
                add("adj_eps_prior_year", v[1] if len(v) in (2, 4) else v[2])
                break
        # Guidance table: first "Net Yield | ..." row containing % (next quarter, FY; reported / cc)
        for line in re.findall(r"^Net Yield \|.*%.*$", t, re.M):
            cells = [c.strip() for c in line.split("|")[1:]]
            mids = []
            for c in cells:
                # Ranges are written "3.8-4.3%" or "3.0% to 4.0%": the hyphen is a range, not a sign.
                # Negatives are written in parentheses, e.g. "(8.9%)".
                nums = [float(x) for x in re.findall(r"\d+\.?\d*", c)]
                if nums:
                    sign = -1 if "(" in c else 1
                    mids.append(sign * np.mean(nums) / 100)
            if len(mids) == 4:   # Q reported, Q cc, FY reported, FY cc
                add("guide_net_yield_nextq_cc", mids[1], "release guidance")
                add("guide_net_yield_fy_cc", mids[3], "release guidance")
            elif len(mids) == 2:  # Q cc, FY cc (older format)
                add("guide_net_yield_nextq_cc", mids[0], "release guidance")
                add("guide_net_yield_fy_cc", mids[1], "release guidance")
            break
        m = re.search(r"Adjusted EPS (?:is expected to be|of) approximately \$(\d+\.\d+)", t)
        if m:
            add("guide_adj_eps_fy", float(m.group(1)), "release guidance")


# ---------------- SBUX ----------------

def sbux(rows):
    ends = quarter_ends("SBUX")
    pat = r"^(?:Change in Comparable Store Sales|Comparable Store Sales Growth)\s*(?:\(\d\))?\s*\|.*$"
    for d, t in releases("SBUX"):
        per = period_for(d, ends)
        add = lambda k, v, src="release": rows.append(("SBUX", per, d, k, v, src))
        m = re.search(pat, t, re.M)
        if m:
            seg = t[m.start():m.start() + 600]
            v = row_values(m.group(0))
            if v:
                add("na_comp", v[0] / 100)
            for k, lab in (("na_transactions", "Change in Transactions"), ("na_ticket", "Change in Ticket")):
                mm = re.search(rf"^{lab}\s*\|.*$", seg, re.M)
                if mm:
                    add(k, row_values(mm.group(0))[0] / 100)
        g = re.search(r"Global comparable store sales (increased|decreased|declined|grew|rose|were up|were down|up|down) "
                      r"(?:by )?([\d.]+)%", t, re.I)
        if g:
            add("global_comp", float(g.group(2)) / 100 * (-1 if g.group(1).lower() in ("decreased", "declined", "were down", "down") else 1))
        u = re.search(r"U\.S\. comparable store sales (increased|decreased|declined|grew|rose|were up|were down|up|down) "
                      r"(?:by )?([\d.]+)%", t, re.I)
        if u:
            add("us_comp", float(u.group(2)) / 100 * (-1 if u.group(1).lower() in ("decreased", "declined", "were down", "down") else 1))
        e = re.search(r"Non-GAAP EPS (?:of )?\$([\d.]+)", t)
        if e:
            add("non_gaap_eps", float(e.group(1)))
        om = re.search(r"Non-GAAP operating margin (?:of [\d.]+% )?(?:expanded|contracted|declined|increased|decreased)?[^.]*?to ([\d.]+)%", t)
        if om:
            add("non_gaap_op_margin", float(om.group(1)) / 100)


# ---------------- CPRT ----------------

UNIT_PATTERNS = {
    "global_units_yoy": r"Global (?:Sold )?Units\s*--\s*(Decreased|Increased|Declined|Rose|Grew|Fell)[^\d]*([\d.]+)%",
    "global_insurance_units_yoy": r"(?:Global )?Insurance Unit(?:s| Volume)\s*--\s*[^.]*?(declined|decreased|increased|grew|rose|fell|down|up)\s*([\d.]+)%",
    "us_insurance_units_yoy": r"U\.?S\.? insurance (?:units|volumes|unit volume)[^.]*?(decreased|declined|increased|grew|were down|were up|down|up)\s*([\d.]+)%",
    "global_asp_yoy": r"Global ASPs? (?:increased|rose|grew|were up)\s*([\d.]+)%",
}


def cprt(rows):
    series = {
        "revenue": REVENUE_TAGS,
        "operating_income": ["OperatingIncomeLoss"],
        "eps_diluted": ["EarningsPerShareDiluted"],
        "interest_income": ["InvestmentIncomeInterest", "InterestIncomeOther", "InterestRevenueExpenseNet",
                            "InvestmentIncomeInterestAndDividend", "InterestIncomeExpenseNonoperatingNet"],
        "cost_of_vehicle_sales": ["CostOfGoodsAndServicesSold", "CostOfGoodsSold"],
    }
    for k, tags in series.items():
        s = xbrl_quarterly("CPRT", tags)
        for end, r in s.iterrows():
            rows.append(("CPRT", end, r["filed"], k, r["val"], "xbrl"))
    ends = quarter_ends("CPRT")
    for f in sorted(TRANSCRIPTS.glob("CPRT_*.txt")):
        t = f.read_text(encoding="utf-8")
        dm = re.search(r"DATE\s*\n?\s*(?:\w+day, )?([A-Z][a-z]+\.? \d{1,2}, \d{4})", t)
        if not dm:
            continue
        d = pd.Timestamp(dm.group(1).replace("Sept.", "Sep").replace(".", ""))
        per = period_for(d, ends)
        for k, p in UNIT_PATTERNS.items():
            m = re.search(p, t, re.I)
            if m:
                g = m.groups()
                val = float(g[-1]) / 100
                if len(g) == 2 and g[0].lower() in ("decreased", "declined", "fell", "down", "were down"):
                    val = -val
                rows.append(("CPRT", per, d, k, val, f.name))


def build(ticker):
    rows = []
    {"NCLH": nclh, "SBUX": sbux, "CPRT": cprt}[ticker](rows)
    df = pd.DataFrame(rows, columns=["ticker", "period_end", "released", "kpi", "value", "source"])
    df = df.dropna(subset=["value"]).drop_duplicates(["period_end", "kpi"], keep="first").sort_values(["kpi", "period_end"])
    # Plausibility: yield/comp guidance outside +/-30% is a mis-parsed table (e.g. 2023-24 "vs. 2019" formats).
    df = df[~(df["kpi"].str.startswith("guide_net_yield") & (df["value"].abs() > 0.3))]
    df.to_csv(PROCESSED / f"{ticker}_kpis.csv", index=False)
    return df


def main():
    for t in sys.argv[1:] or ["NCLH", "SBUX", "CPRT"]:
        df = build(t)
        print(t, len(df), "rows")
        print(df.groupby("kpi")["value"].agg(["count", "first", "last"]).to_string())


if __name__ == "__main__":
    main()
