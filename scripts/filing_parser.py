"""Parse downloaded filings into plain text (tables kept as pipe-delimited rows) in data/processed/text/<T>/.

Usage: python filing_parser.py [TICKER ...]
"""

import re
import sys

from bs4 import BeautifulSoup

from common import FILINGS, PROCESSED, TICKERS


def html_to_text(raw):
    soup = BeautifulSoup(raw, "lxml")
    for t in soup(["script", "style"]):
        t.decompose()
    for tbl in soup.find_all("table"):
        lines = []
        for tr in tbl.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
            cells = [c for c in cells if c and c not in ("$", "%", ")")]
            if cells:
                lines.append(" | ".join(cells))
        tbl.replace_with("\n[TABLE]\n" + "\n".join(lines) + "\n[/TABLE]\n")
    text = soup.get_text("\n")
    text = re.sub(r"\xa0", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def parse(ticker):
    out = PROCESSED / "text" / ticker
    out.mkdir(parents=True, exist_ok=True)
    for f in sorted((FILINGS / ticker).glob("*.htm*")):
        dest = out / (f.stem + ".txt")
        if not dest.exists():
            dest.write_text(html_to_text(f.read_bytes()), encoding="utf-8")
    return sorted(out.glob("*.txt"))


if __name__ == "__main__":
    for t in sys.argv[1:] or TICKERS:
        files = parse(t)
        print(t, [(f.name, f.stat().st_size // 1000) for f in files])
