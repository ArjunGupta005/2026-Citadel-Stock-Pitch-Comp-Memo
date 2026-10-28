# GEV under Framework B — Deposit / FCF investigation and verdict

**Date:** 2026-10-01 (late evening ET). **Framework:** `framework_B/05_framework_B_locked.md` (SHA-256 `6c005f7a…12ea`). Framework A results unchanged.
**Direction assumed going in:** none.
**Scripts:** `scripts/gev_fcf_decomposition.py`, `scripts/gev_reverse_dcf.py`. **Data:** `framework_B/gev_fcf_decomposition.csv`, `framework_B/gev_reverse_dcf.md`.

## 1. Quarterly FCF rebuilt from operating components (SEC XBRL, first-filed, YTD differenced; $bn)

| Quarter | Op. income (GAAP) | OCF | Capex | **FCF** | **Δ contract liabilities (deposits)** | Δ inventory | Δ receivables | **FCF ex-deposits** |
|---|---|---|---|---|---|---|---|---|
| Q1-25 | 0.04 | 1.16 | 0.19 | 0.98 | 1.12 | 0.43 | −0.92 | −0.15 |
| Q2-25 | 0.38 | 0.37 | 0.17 | 0.19 | 0.74 | 0.45 | −0.11 | −0.54 |
| Q3-25 | 0.37 | 0.98 | 0.25 | 0.73 | 0.56 | 0.16 | 0.47 | 0.17 |
| Q4-25 | 0.60 | 2.48 | 0.67 | 1.81 | **5.60** | 0.39 | 2.49 | −3.79 |
| Q1-26 | 0.18 | 5.19 | 0.40 | 4.79 | **5.57** | 0.93 | −0.61 | −0.78 |
| Q2-26 | 0.65 | 5.49 | 0.39 | 5.11 | **8.12** | 0.81 | 1.45 | −3.02 |

Integrity check: the cash-flow Δ contract liabilities matches the balance-sheet change within about $0.1bn in 5 of 6 quarters (Q1-26 gap $0.4bn, consistent with the Prolec GE consolidation).

## 2. Deposit contribution and normalized FCF (TTM Q3-25 to Q2-26)

| Measure | $bn |
|---|---|
| Reported FCF | 12.44 |
| Δ contract liabilities (customer deposits) | **19.85 (160% of FCF)** |
| N1: FCF with zero incremental deposits | **−7.42** |
| N3: FCF ex-deposits, net of inventory / contract assets they fund | −4.95 |
| N2: earnings-based steady-state FCF (FY26 adj. EBITDA ~$6.0bn, D&A ~$1.0bn, capex ~$1.5bn, 21% tax, zero working capital) | ≈ 3.45, vs the FY26 guide of $12bn → **~71% of guided FY26 FCF is working capital / deposits** |

**Factually, deposits do materially inflate reported FCF.** Without them, GEV's FCF would currently be negative.

## 3. Do investors understand it? Is GEV valued on FCF?

| Test | Finding | Source |
|---|---|---|
| Is the deposit effect disclosed? | **Yes, explicitly.** 10-Q MD&A: operating cash up "primarily driven by… contract liabilities and current deferred income of $11.8 billion, primarily due to higher down payments on orders and slot reservation agreements"; H1 working capital inflow $11.7bn, of which $13.7bn from contract liabilities. | GEV 10-Q Q2-26 (primary) |
| Is it discussed by the market? | **Yes.** Secondary commentary: strong FCF "driven by working capital timing, not yet by GAAP earnings leverage… tied to the timing of customer prepayments." | Press / sell-side summaries (secondary) |
| What metric drives valuation? | **EV/EBITDA and forward P/E**, not FCF. Sell-side revisions are framed in adjusted EBITDA (Mizuho cut 2026 EBITDA to $6.5bn; Evercore 2-7% above consensus on EBITDA through 2028; 2028 consensus EBITDA ~$12.9bn). | Investing.com analyst notes (secondary) |

## 4. What today's price embeds (reverse-engineered)
- EV $254bn ($267bn if deposit-funded cash is treated as customer money rather than excess cash).
- EV / consensus EBITDA: **2026 39.1x | 2027 26.8x | 2028 19.6x.**
- Reverse DCF (9% WACC; consensus EBITDA to 2028; then a 13x mature exit): the price requires **~15% EBITDA CAGR in 2029-2033** (2033 EBITDA ≈ $26bn, i.e. ≈ $120bn revenue at a 22% margin vs FY27 consensus of $52.8bn). Sensitivity: 11x exit → 18.7%; 15x exit → 12.5%.
- If the consensus path is delivered and the stock compounds at 9%, it would still trade at ~22.7x 2028 EBITDA at end-2028.

## 5. Verdict on the deposit / FCF hypothesis
**KILL under Framework B (gate B1, and your explicit kill condition).** The deposit effect is real and large, but:
1. **Investors already understand it.** The company states it plainly in the 10-Q and the press repeats it.
2. **The stock is not valued on FCF.** Consensus and price targets are built on EBITDA / P/E, which deposits do not change.
So an "FCF is inflated" thesis has no channel for the market to "come around" (B2): the information is already public and does not enter the valuation metric. **No directional thesis is generated from this work.**

## 6. What survives (facts, not a thesis)
- The real question in GEV's price is **duration**: the stock embeds delivery of a doubling of EBITDA by 2028 (to ~$12.9bn) *plus* about 15% EBITDA growth for five more years.
- Any future GEV thesis under Framework B would have to be about that duration (gas-turbine cycle length, slot conversion and pricing beyond 2028, the Electrification and Wind mix). It would need its own pre-valuation card, consensus evidence for 2029+ expectations, and a dated catalyst (e.g. the December investor update). **That work has not been done and is not implied here.**
- Q&A defense value: if a judge or another team argues GEV's FCF yield, the decomposition above is a precise, sourced rebuttal.
