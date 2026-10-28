"""Fetch earnings call transcripts and compare consecutive calls.

For each pair (prior, latest) it reports:
  - topic-term frequency per 10k words (ticker-specific vocab) and the change
  - phrases (2-3 grams) new in the latest call / dropped since the prior call
  - tone: Loughran-McDonald-style negative / uncertainty / positive word rates
  - every forward-looking sentence that contains a number (guidance-like statements)

Sources: Motley Fool (div.article-body) or MarketBeat (#transcriptPresentation).
Output: data/transcripts/<T>_<label>.txt and data/processed/<T>_transcript_compare.md

Usage: python transcript_compare.py [TICKER ...]
"""

import re
import sys
from collections import Counter

import requests
from bs4 import BeautifulSoup

from common import PROCESSED, TRANSCRIPTS

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
FOOL = "https://www.fool.com/earnings/call-transcripts"
MB = "https://www.marketbeat.com/earnings/reports"

# Ordered oldest -> newest per ticker.
SOURCES = {
    "NCLH": [("Q1-2026", f"{MB}/2026-5-4-norwegian-cruise-line-holdings-ltd-stock/"),
             ("Q2-2026", f"{MB}/2026-7-30-norwegian-cruise-line-holdings-ltd-stock/")],
    "CPRT": [("Q2-FY2026", f"{FOOL}/2026/05/21/copart-cprt-q2-2026-earnings-transcript/"),
             ("Q3-FY2026", f"{FOOL}/2026/05/25/copart-cprt-q3-2026-earnings-transcript/"),
             ("Q4-FY2026", f"{FOOL}/2026/09/11/copart-cprt-q4-2026-earnings-call-transcript/")],
    "SBUX": [("Q2-FY2026", f"{FOOL}/2026/04/28/starbucks-sbux-q2-2026-earnings-transcript/"),
             ("Q3-FY2026", f"{FOOL}/2026/08/07/starbucks-sbux-q3-2026-earnings-call-transcript/")],
    "ABNB": [("Q1-2026", f"{FOOL}/2026/05/07/airbnb-abnb-q1-2026-earnings-call-transcript/"),
             ("Q2-2026", f"{FOOL}/2026/08/13/airbnb-abnb-q2-2026-earnings-call-transcript/")],
    "ADBE": [("Q2-FY2026", f"{FOOL}/2026/06/11/adobe-adbe-q2-2026-earnings-transcript/"),
             ("Q3-FY2026", f"{FOOL}/2026/09/11/adobe-adbe-q3-2026-earnings-call-transcript/")],
    "SPOT": [("Q1-2026", f"{FOOL}/2026/04/28/spotify-spot-q1-2026-earnings-transcript/"),
             ("Q2-2026", f"{FOOL}/2026/08/11/spotify-spot-q2-2026-earnings-call-transcript/")],
    "NKE": [("Q4-FY2026", f"{MB}/2026-6-30-nike-inc-stock/"),
            ("Q1-FY2027", f"{MB}/2026-10-1-nike-inc-stock/")],
    "EXPE": [("Q2-2026", f"{FOOL}/2026/08/12/expedia-expe-q2-2026-earnings-call-transcript/")],
    # Peers / read-across
    "CCL": [("Q3-2026", f"{FOOL}/2026/09/30/carnival-ccl-q3-2026-earnings-call-transcript/")],
    "RBA": [("Q2-2026", f"{FOOL}/2026/08/11/rb-global-rba-q2-2026-earnings-call-transcript/")],
}

TOPICS = {
    "NCLH": ["yield", "booking", "booked position", "pricing", "close-in", "europe", "caribbean", "alaska", "great stirrup",
             "middle east", "fuel", "cost", "savings", "leverage", "2027", "demand", "onboard", "occupancy", "marketing",
             "execution", "consumer", "discount"],
    "CPRT": ["unit", "insurance", "total loss", "frequency", "severity", "asp", "average selling", "self-pay",
             "uninsured", "coverage", "inventory", "acv", "dealer", "blu", "purple wave", "international", "market share",
             "catastroph", "hurricane", "interest income", "margin", "competition", "iaa"],
    "ABNB": ["nights", "adr", "average daily rate", "take rate", "hotel", "experiences", "services", "margin", "ebitda",
             "marketing", "ai", "regulation", "fx", "booking window", "u.s.", "latin america", "asia", "outlook", "2027", "invest"],
    "ADBE": ["arr", "firefly", "ai-first", "creative cloud", "acrobat", "express", "seat", "pricing", "freemium", "mau",
             "enterprise", "gen studio", "competition", "canva", "openai", "google", "margin", "2027", "buyback", "retention"],
    "SPOT": ["subscriber", "mau", "arpu", "price", "gross margin", "label", "podcast", "audiobook", "advertising", "churn",
             "operating income", "social charges", "invest", "ai", "2027", "superfan", "marketing"],
    "NKE": ["wholesale", "direct", "digital", "china", "sportswear", "jordan", "running", "gross margin", "tariff",
            "inventory", "promotion", "pace", "savings", "converse", "north america", "emea", "fiscal '28", "2028", "guidance"],
    "SBUX": ["comp", "transaction", "ticket", "back to starbucks", "green apron", "labor", "margin", "throughput",
             "mobile order", "china", "value", "coffee", "tariff", "cold", "protein", "rewards", "2027", "investment",
             "promotion", "dairy", "inflation"],
}

NEG = set("""decline declined declines decrease decreased weak weaker weakness soft softer softness pressure pressured
headwind headwinds challenge challenges challenging difficult disappoint disappointing loss losses lower below miss
missed negative deteriorate deteriorated deterioration slowdown slower slow concern concerns risk risks volatile volatility
uncertain uncertainty adverse unfavorable cut cuts reduced reduce""".split())
UNC = set("""may might could possibly perhaps uncertain uncertainty unclear depend depends depending approximately
roughly believe assume assumption anticipate variable fluctuate fluctuations unpredictable""".split())
POS = set("""strong stronger strength improve improved improvement improving growth grew increase increased record
accelerate accelerated accelerating momentum outperform outperformed beat exceeded exceed favorable confident
confidence robust healthy encouraging encouraged progress gain gains positive better best""".split())
FWD = re.compile(r"\b(expect|expects|expected|guidance|outlook|anticipate|forecast|going forward|next year|2027|"
                 r"full year|fourth quarter|third quarter|first quarter|target|plan to|will be)\b", re.I)
STOP = set("the a an and or of to in on for with that this is are was were be been we our you it as at by from have has "
           "had i they their them its so but not do does did can will would there what which about into over than then just "
           "very also more some like think know going really yeah okay well thank thanks".split())


def fetch(url):
    html = requests.get(url, headers=UA, timeout=30).text
    s = BeautifulSoup(html, "lxml")
    body = s.select_one("#transcriptPresentation") or s.select_one("div.article-body") or s.body
    return re.sub(r"\n{2,}", "\n", body.get_text("\n", strip=True))


def load(ticker, label, url):
    path = TRANSCRIPTS / f"{ticker}_{label}.txt"
    if not path.exists():
        TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
        path.write_text(fetch(url), encoding="utf-8")
    return path.read_text(encoding="utf-8")


def words(text):
    return re.findall(r"[a-z][a-z\-']+", text.lower())


def ngrams(ws, n):
    return Counter(" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1))


def tone(ws):
    n = len(ws) / 1e4
    return {k: sum(w in v for w in ws) / n for k, v in (("negative", NEG), ("uncertainty", UNC), ("positive", POS))}


def topic_rates(text, topics):
    t, n = text.lower(), len(words(text)) / 1e4
    return {k: t.count(k) / n for k in topics}


def guidance_sentences(text):
    sents = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    return [s.strip() for s in sents if FWD.search(s) and re.search(r"\d", s) and 40 < len(s) < 500]


def distinctive(ws_new, ws_old, n, min_count=3):
    a, b = ngrams(ws_new, n), ngrams(ws_old, n)
    out = [(g, c) for g, c in a.items() if c >= min_count and b.get(g, 0) == 0
           and g.split()[0] not in STOP and g.split()[-1] not in STOP]
    return sorted(out, key=lambda x: -x[1])[:25]


def compare(ticker):
    texts = [(lbl, load(ticker, lbl, url)) for lbl, url in SOURCES[ticker]]
    lines = [f"# {ticker} transcript comparison", ""]
    if len(texts) < 2:
        lbl, t = texts[0]
        lines += [f"Single transcript ({lbl}); forward-looking numeric statements:", ""]
        lines += [f"- {s}" for s in guidance_sentences(t)]
        return "\n".join(lines)
    (l0, t0), (l1, t1) = texts[-2], texts[-1]
    w0, w1 = words(t0), words(t1)
    lines += [f"Prior: **{l0}** ({len(w0):,} words) | Latest: **{l1}** ({len(w1):,} words)", "",
              "## Tone (per 10k words)", "", "| Measure | Prior | Latest | Change |", "|---|---|---|---|"]
    a, b = tone(w0), tone(w1)
    lines += [f"| {k} | {a[k]:.0f} | {b[k]:.0f} | {b[k] - a[k]:+.0f} |" for k in a]
    if ticker in TOPICS:
        a, b = topic_rates(t0, TOPICS[ticker]), topic_rates(t1, TOPICS[ticker])
        lines += ["", "## Topic emphasis (mentions per 10k words)", "", "| Topic | Prior | Latest | Change |", "|---|---|---|---|"]
        for k in sorted(a, key=lambda k: -abs(b[k] - a[k])):
            lines.append(f"| {k} | {a[k]:.1f} | {b[k]:.1f} | {b[k] - a[k]:+.1f} |")
    for n in (2, 3):
        lines += ["", f"## New {n}-grams in latest call (>=3 uses, absent in prior)", ""]
        lines += [f"- {g} ({c})" for g, c in distinctive(w1, w0, n)]
        lines += ["", f"## Dropped {n}-grams (>=3 uses in prior, absent in latest)", ""]
        lines += [f"- {g} ({c})" for g, c in distinctive(w0, w1, n)]
    for lbl, t in ((l0, t0), (l1, t1)):
        lines += ["", f"## Forward-looking numeric statements: {lbl}", ""]
        lines += [f"- {s}" for s in guidance_sentences(t)]
    return "\n".join(lines)


def main():
    for t in sys.argv[1:] or list(SOURCES):
        out = PROCESSED / f"{t}_transcript_compare.md"
        out.write_text(compare(t), encoding="utf-8")
        print(t, "->", out.name, out.stat().st_size // 1000, "KB")


if __name__ == "__main__":
    main()
