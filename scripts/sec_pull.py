"""Pull 10-K, 10-Q and 8-K filings from SEC EDGAR into data/filings/<TICKER>/.

Saves per ticker:
  data/raw/<T>/submissions.json   filing index (all forms, dates, items)
  data/raw/<T>/companyfacts.json  XBRL financial facts (as-filed values with filing dates)
  data/filings/<T>/<form>_<date>_<file>  latest 10-K, last N 10-Qs, last N earnings releases (8-K 2.02 EX-99.1)
  data/processed/<T>_earnings_dates.csv  every 8-K Item 2.02 date (earnings release dates)

Usage: python sec_pull.py [TICKER ...] [--n 4] [--er-only]
"""

import argparse
import json
import re

import pandas as pd

from common import FILINGS, PROCESSED, RAW, TICKERS, cik_map, sec_get


def filings_table(sub):
    rows = [sub["filings"]["recent"]]
    for f in sub["filings"].get("files", []):
        rows.append(sec_get(f"https://data.sec.gov/submissions/{f['name']}"))
    df = pd.concat([pd.DataFrame(r) for r in rows], ignore_index=True)
    df["filingDate"] = pd.to_datetime(df["filingDate"])
    return df.sort_values("filingDate", ascending=False)


def filing_index(cik, accession):
    """Return [(description, filename, type)] for every document in a filing."""
    acc = accession.replace("-", "")
    html = sec_get(f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{accession}-index.html", as_json=False).decode()
    docs = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
        cells = [re.sub(r"<[^>]+>|&nbsp;|iXBRL", "", c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        if len(cells) >= 4:
            docs.append((cells[1], cells[2], cells[3]))
    return docs


def is_6k_earnings(cik, accession):
    """SPOT-style 6-K earnings: an EX-99.1 shareholder deck with many slide images."""
    docs = filing_index(cik, accession)
    has_ex99 = any(t.startswith("EX-99") for _, _, t in docs)
    return has_ex99 and sum(t == "GRAPHIC" for _, _, t in docs) >= 10


def download(cik, row, ticker, want_exhibit=False):
    acc = row["accessionNumber"].replace("-", "")
    base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}"
    out = FILINGS / ticker
    out.mkdir(parents=True, exist_ok=True)
    tag = f"{row['form'].replace('/', '')}_{row['filingDate']:%Y-%m-%d}"
    if want_exhibit:
        ex = [f for _, f, t in filing_index(cik, row["accessionNumber"])
              if t.startswith("EX-99") and f.lower().endswith((".htm", ".html"))]
        if not ex:
            return None
        fname = ex[0]  # first EX-99 exhibit is the press release / shareholder deck
    else:
        fname = row["primaryDocument"]
    path = out / f"{tag}_{fname}"
    if not path.exists():
        path.write_bytes(sec_get(f"{base}/{fname}", as_json=False))
    return path


def pull(ticker, n=4, er_only=False):
    cik = cik_map()[ticker]
    raw = RAW / ticker
    raw.mkdir(parents=True, exist_ok=True)
    sub = sec_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    (raw / "submissions.json").write_text(json.dumps(sub))
    facts = sec_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
    (raw / "companyfacts.json").write_text(json.dumps(facts))

    df = filings_table(sub)
    # Foreign private issuers (SPOT) file 20-F / 6-K instead of 10-K / 10-Q / 8-K.
    annual = df[df["form"].isin(["10-K", "20-F"])].head(1)
    quarterly = df[df["form"] == "10-Q"].head(n)
    is_er = df["form"].eq("8-K") & df["items"].fillna("").str.contains("2.02")
    er = df[is_er]
    if er.empty:
        sixk = df[df["form"] == "6-K"]
        er = sixk[[is_6k_earnings(cik, a) for a in sixk["accessionNumber"]]]
        # The quarterly financial report 6-K filed the same day as the deck.
        quarterly = sixk[sixk["primaryDocument"].str.contains("6xk", case=False)].head(n)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    er[["filingDate", "form", "accessionNumber", "items"]].to_csv(PROCESSED / f"{ticker}_earnings_dates.csv", index=False)

    saved = []
    for _, r in (pd.DataFrame() if er_only else pd.concat([annual, quarterly])).iterrows():
        saved.append(download(cik, r, ticker))
    for _, r in er.head(n).iterrows():
        saved.append(download(cik, r, ticker, want_exhibit=True))
    return [p for p in saved if p]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*", default=TICKERS)
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--er-only", action="store_true", help="only download earnings-release exhibits (for history)")
    a = ap.parse_args()
    for t in a.tickers:
        paths = pull(t, a.n, a.er_only)
        print(f"{t}: {len(paths)} documents")


if __name__ == "__main__":
    main()
