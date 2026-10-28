"""Shared helpers: paths, SEC EDGAR access, price data cache."""

import json
import os
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
FILINGS = DATA / "filings"
MARKET = DATA / "market"
PROCESSED = DATA / "processed"
TRANSCRIPTS = DATA / "transcripts"
COMPS = DATA / "comps"

TICKERS = ["ABNB", "ADBE", "CPRT", "GEV", "NCLH", "NKE", "SBUX", "SPOT"]

# SEC requires a descriptive User-Agent; override with SEC_USER_AGENT env var.
SEC_UA = os.environ.get("SEC_USER_AGENT", "CitadelPitchResearch research@example.com")
_last_call = [0.0]


def sec_get(url, as_json=True):
    """GET from SEC with rate limiting (<10 req/s) and retries."""
    for attempt in range(4):
        wait = 0.15 - (time.time() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.time()
        r = requests.get(url, headers={"User-Agent": SEC_UA, "Accept-Encoding": "gzip, deflate"}, timeout=30)
        if r.status_code == 200:
            return r.json() if as_json else r.content
        if r.status_code in (429, 503):
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
    r.raise_for_status()


def cik_map():
    path = RAW / "company_tickers.json"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(sec_get("https://www.sec.gov/files/company_tickers.json")))
    data = json.loads(path.read_text())
    return {v["ticker"]: int(v["cik_str"]) for v in data.values()}


def load_json(path):
    return json.loads(Path(path).read_text())


def prices(ticker, refresh=False):
    """Daily adjusted close history, cached to data/market/<T>.csv."""
    import yfinance as yf

    path = MARKET / f"{ticker}.csv"
    if path.exists() and not refresh:
        return pd.read_csv(path, index_col=0, parse_dates=True)
    df = yf.Ticker(ticker).history(period="max", auto_adjust=True)
    df.index = df.index.tz_localize(None)
    MARKET.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    return df


def xbrl_quarterly(ticker, tags, taxonomy="us-gaap", additive=True):
    """Discrete quarterly series for the first XBRL tag in `tags` with data, point-in-time.

    Returns DataFrame indexed by period end with columns [val, filed]. For each period the
    FIRST-filed value is kept (as originally reported, no later restatements). Q4 is derived
    as annual minus the three reported quarters of the same fiscal year, with `filed` set to
    the 10-K filing date.
    """
    facts = load_json(RAW / ticker / "companyfacts.json")["facts"].get(taxonomy, {})
    frames = []
    for tag in tags:
        if tag not in facts:
            continue
        for unit, vals in facts[tag]["units"].items():
            df = pd.DataFrame(vals)
            if "start" not in df:
                continue
            df = df[df["form"].isin(["10-Q", "10-K", "10-Q/A", "10-K/A"])].copy()
            df["start"], df["end"], df["filed"] = (pd.to_datetime(df[c]) for c in ("start", "end", "filed"))
            df["days"] = (df["end"] - df["start"]).dt.days
            df["tag"] = tag
            frames.append(df)
    if not frames:
        return pd.DataFrame(columns=["val", "filed"])
    df = pd.concat(frames)
    # Tags can switch over time (e.g. Revenues -> RevenueFromContract...); prefer earliest filing per period.
    df = df.sort_values("filed")
    q = df[df["days"].between(80, 100)].drop_duplicates(["start", "end"], keep="first")
    a = df[df["days"].between(350, 380)].drop_duplicates(["start", "end"], keep="first")
    out = {e: (v, f) for e, v, f in zip(q["end"], q["val"], q["filed"])}
    for _, r in a.iterrows():
        inside = q[(q["start"] >= r["start"] - pd.Timedelta(days=5)) & (q["end"] <= r["end"] - pd.Timedelta(days=20))]
        if len(inside) == 3 and r["end"] not in out:
            out[r["end"]] = (r["val"] - inside["val"].sum() if additive else r["val"], r["filed"])
    res = pd.DataFrame.from_dict(out, orient="index", columns=["val", "filed"]).sort_index()
    if res.empty:
        return pd.DataFrame(columns=["val", "filed"], index=pd.DatetimeIndex([]))
    res.index = pd.to_datetime(res.index)
    # Drop duplicate quarters whose end dates differ by a few days (52/53-week calendars).
    return res[~(res.index.to_series().diff().dt.days < 60)]

REVENUE_TAGS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
                "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"]


def xbrl_ytd_quarterly(ticker, tags, taxonomy="us-gaap"):
    """Discrete quarters from year-to-date cash-flow facts (10-Q cash flows are YTD: 3M, 6M, 9M, FY).

    Keeps the first-filed value per (start, end); quarter k = YTD_k - YTD_(k-1) within the same fiscal-year start.
    Returns DataFrame [val, filed] indexed by quarter end.
    """
    facts = load_json(RAW / ticker / "companyfacts.json")["facts"].get(taxonomy, {})
    frames = []
    for tag in tags:
        if tag in facts:
            for vals in facts[tag]["units"].values():
                d = pd.DataFrame(vals)
                if "start" not in d:
                    continue
                d = d[d["form"].isin(["10-Q", "10-K"])].copy()
                for c in ("start", "end", "filed"):
                    d[c] = pd.to_datetime(d[c])
                frames.append(d)
    if not frames:
        return pd.DataFrame(columns=["val", "filed"])
    d = pd.concat(frames).sort_values("filed").drop_duplicates(["start", "end"], keep="first")
    d["days"] = (d["end"] - d["start"]).dt.days
    out = {}
    for start, g in d.groupby("start"):
        g = g.sort_values("end")
        prev = 0.0
        prev_end = None
        for _, r in g.iterrows():
            # only chain cumulative periods ~3/6/9/12 months long
            if not any(abs(r["days"] - m) <= 12 for m in (91, 182, 273, 365)):
                continue
            q = r["val"] - prev
            if prev_end is None and r["days"] > 100:
                prev, prev_end = r["val"], r["end"]  # missing earlier YTD point: cannot difference
                continue
            out[r["end"]] = (q, r["filed"])
            prev, prev_end = r["val"], r["end"]
    res = pd.DataFrame.from_dict(out, orient="index", columns=["val", "filed"]).sort_index()
    res.index = pd.to_datetime(res.index)
    return res
