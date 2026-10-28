# CPRT — Framework B numbers (scripts/cprt_framework_b.py)

Cost of equity 9.74% = 10y 5.24% + β 0.9 × ERP 5%. ROIC: FY26 NOPAT ≈ $1.33bn on ≈ $4.6bn invested capital ≈ 29%; post-ACV ≈ 20% (ACV adds $1.9bn at ~0 NOPAT).

## 1. What today's price implies
- Price $27.29; cash + securities $4.7bn = $5.00/sh → ex-cash price $22.29 (ACV is purchased with this cash, so it is treated as an asset at cost).
- Street FY27 (Yahoo mean) $1.75: ex-cash, ex-interest NTM P/E 13.5x → implied 5-year EPS growth 5.6% (incremental ROIC 20%, CoE 9.7%, 3% terminal)
- Street FY27 (press aggregators) $1.67-1.69: ex-cash, ex-interest NTM P/E 14.0x → implied 5-year EPS growth 7.3% (incremental ROIC 20%, CoE 9.7%, 3% terminal)
- Our base FY27 ex-ACV $1.43: ex-cash, ex-interest NTM P/E 16.6x → implied 5-year EPS growth 13.8% (incremental ROIC 20%, CoE 9.7%, 3% terminal)
- Our base FY27 incl. ACV $1.35: ex-cash, ex-interest NTM P/E 17.7x → implied 5-year EPS growth 16.2% (incremental ROIC 20%, CoE 9.7%, 3% terminal)
- Historical regimes (trailing GAAP P/E): FY12-17 20-24x at 10y 1.5-2.6% (growth ~10-15%); FY18-24 24-40x at 0.5-4.1%; now 17.6x at 5.2%.
  - Fundamental P/E at today's rates for FY12-17-like growth (10%), incremental ROIC 25%: 16.0x; at FY12-17 rates (10y 2%): 32.6x
  - Fundamental P/E at today's rates for mid-single-digit growth (6%), incremental ROIC 25%: 14.2x; at FY12-17 rates (10y 2%): 28.1x
  - Fundamental P/E at today's rates for GDP-like growth (3%), incremental ROIC 25%: 13.1x; at FY12-17 rates (10y 2%): 25.1x
- Peers (fwd P/E, 2026-10-01, Yahoo): RBA 16.8x (levered, 18% op. margin), OPLN 20.1x, KMX 18.1x; peer median 20.1x. CPRT is 15.6x on the Yahoo FY27 mean with net cash and a 32-37% operating margin.

## 2. Probability-weighted distribution (12-month horizon, value at Sep-2027 on FY28 NTM EPS)
| World | Prob. | FY27 EPS (GAAP, incl. ACV) | FY27 ex-ACV | FY28 EPS | FY28 ex-interest | Justified P/E (ex-cash) | Implied total P/E | Value/sh | Return | Return from EPS | Return from multiple |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1 share loss deepens + cost creep | 0.25 | 1.16 | 1.27 | 1.20 | 1.13 | 11.9x | 14.2x | $17.12 | -37.3% | -38.4% (log) | -12.5% (log) |
| W2 FY27 trough, FY28 normalises | 0.50 | 1.35 | 1.43 | 1.51 | 1.43 | 13.6x | 15.3x | $23.10 | -15.3% | -14.9% (log) | +0.9% (log) |
| W3 cycle turns + ACV synergies | 0.25 | 1.53 | 1.58 | 1.80 | 1.71 | 15.5x | 16.7x | $30.20 | +10.7% | +3.1% (log) | +14.1% (log) |

- Market ex-cash NTM P/E today (Yahoo FY27): 13.5x
- **Probability-weighted return: -14.3%** (long direction) → short expected return +14.3%
- Maximum plausible loss: SHORT +10.7% (W3); LONG -37.3% (W1)
- Stress for a short (W3 + 10y back to 3.5%): $40.36 (+47.9%)

## 3. Sensitivities
- CoE +50bp: probability-weighted return -19.6%
- CoE −50bp: probability-weighted return -8.2%
- β 1.03 (Yahoo): probability-weighted return -21.1%
- Probabilities (0.35, 0.45, 0.2): -17.8%
- Probabilities (0.15, 0.5, 0.35): -9.5%

## 4. Four-world distribution (adds a 'Street is right' world; governing for the verdict)
| World | Prob. | FY27 EPS | FY28 EPS | Justified P/E ex-cash | Value/sh | Return | EPS part (log) | Multiple part (log) |
|---|---|---|---|---|---|---|---|---|
| W1 share loss deepens + cost creep | 0.20 | 1.16 | 1.20 | 11.9x | $17.12 | -37.3% | -38.4% | -12.5% |
| W2 FY27 trough, FY28 normalises | 0.45 | 1.35 | 1.51 | 13.6x | $23.10 | -15.3% | -14.9% | +0.9% |
| W3 cycle turns + ACV synergies | 0.20 | 1.53 | 1.80 | 15.5x | $30.20 | +10.7% | +3.1% | +14.1% |
| W4 Street right: share recapture (JPM data) | 0.15 | 1.61 | 1.85 | 16.0x | $31.70 | +16.1% | +5.7% | +17.1% |
- **Probability-weighted return -9.8%** → short expected return +9.8%; max plausible short loss +16.1% (W4); rate-fall stress (W3 + 10y 3.5%) as in §2