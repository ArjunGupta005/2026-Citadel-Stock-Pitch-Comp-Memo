# CPRT valuation-history audit (scripts/audit_valuation.py)

Splits (yfinance): 1999-01-29 2:1, 2000-01-25 2:1, 2002-01-22 1.5:1, 2012-03-29 2:1, 2017-04-11 2:1, 2022-11-04 2:1, 2023-08-22 2:1
- TTM EPS around 2012-03-29: 0.164 → 0.164 (no split-sized jump = adjusted correctly)
- TTM EPS around 2017-04-11: 0.415 → 0.415 (no split-sized jump = adjusted correctly)
- TTM EPS around 2022-11-04: 1.130 → 1.130 (no split-sized jump = adjusted correctly)
- TTM EPS around 2023-08-22: 1.193 → 1.193 (no split-sized jump = adjusted correctly)

Point-in-time XBRL EPS history starts 2011-12-12 (pre-2009 EPS not in XBRL).
Trailing GAAP P/E today: 17.6x (price $27.29 / TTM EPS $1.55)

| Window start | Percentile of today's trailing P/E | Min | Median |
|---|---|---|---|
| 2010 | 2% | 16.5x | 26.7x |
| 2012 | 2% | 16.5x | 26.8x |
| 2015 | 2% | 16.5x | 30.6x |
| 2018 | 1% | 16.5x | 34.2x |
| 2021 | 2% | 16.5x | 35.2x |

Ex-cash, ex-interest P/E today: 16.0x (cash+securities $4.7bn; after-tax interest = 10% of TTM net income). Percentile since 2012: 1%.
Year-end interest share of net income: 2014: 0%, 2015: 0%, 2016: -6%, 2017: 2%, 2018: -4%, 2019: 1%, 2020: 0%, 2021: 0%, 2022: 0%, 2023: 2%, 2024: 9%, 2025: 9%, 2026: 10%

- Forward P/E on Street FY27 $1.75: 15.6x → percentile of perfect-foresight forward P/E 2012-2025: 7% (median 24.4x)
- Forward P/E on our base FY27 $1.35: 20.2x → percentile of perfect-foresight forward P/E 2012-2025: 23% (median 24.4x)
- Forward P/E on our ex-ACV FY27 $1.43: 19.0x → percentile of perfect-foresight forward P/E 2012-2025: 18% (median 24.4x)

| Fiscal year-end | TTM op margin | 10y UST | Trailing P/E (year-end) |
|---|---|---|---|
| FY2012 | 30.7% | 1.49% | 20.4x |
| FY2013 | 27.0% | 2.59% | 22.0x |
| FY2014 | 23.6% | 2.56% | 23.1x |
| FY2015 | 30.1% | 2.20% | 20.0x |
| FY2016 | 32.0% | 1.46% | 24.0x |
| FY2017 | 31.9% | 2.29% | 20.7x |
| FY2018 | 32.4% | 2.96% | 33.1x |
| FY2019 | 35.1% | 2.02% | 34.6x |
| FY2020 | 37.0% | 0.54% | 36.1x |
| FY2021 | 42.2% | 1.24% | 40.2x |
| FY2022 | 39.3% | 2.64% | 24.3x |
| FY2023 | 38.4% | 3.96% | 33.7x |
| FY2024 | 37.1% | 4.11% | 36.6x |
| FY2025 | 36.5% | 4.36% | 28.1x |
| FY2026 | 35.4% | 4.74% | 17.5x |