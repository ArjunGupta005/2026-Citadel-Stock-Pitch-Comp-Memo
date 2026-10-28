# 04 — Restart Criteria (PRE-REGISTERED, LOCKED)

**Locked:** 2026-10-01, before any candidate data was pulled.
**Rule:** Do not edit. If ANY criterion triggers on the selected thesis, the thesis is restarted
(next-ranked hypothesis is promoted, or we go back to Phase 3). Thresholds are fixed here so they
cannot be tuned to fit a result later. SHA-256 is recorded in `03_research_log.md`.

Horizon window: **2026-10-01 → 2027-09-30**.

| # | Restart if… | Operational test (numeric) |
|---|-------------|----------------------------|
| R1 | No clear consensus disagreement | Our base-case NTM EPS (or the key KPI driving it) differs from consensus by **< 5%** on EPS, **and** by **< 1 historical std-dev of that KPI's quarterly surprise**. |
| R2 | Variant cannot be quantified | The sentence "Consensus believes X. We believe Y because Z. If correct, KPI A moves to B, changing earnings by C and the stock by D" cannot be filled with numbers for X, Y, A→B, C, D. |
| R3 | Catalyst timing exceeds 12 months | No discrete catalyst inside the horizon window at which the key KPI is publicly reported/updated. |
| R4 | Backtest contradicts the thesis | The historical signal's 3M **or** 6M forward excess return (vs. SPY) has the **opposite sign** to the thesis with n ≥ 8 events. (Insignificant-but-same-sign = "unsupported", disclosed in memo, not a restart by itself.) |
| R5 | Risk/reward below threshold | Base-case upside / bear-case downside **< 2.0×**, **or** probability-weighted expected return **< +10%** in thesis direction (25/50/25 bear/base/bull unless evidence justifies other weights, documented). |
| R6 | Opposite thesis explains data better | In `red_team.md`, the opposing case scores higher on evidence fit (same rubric, scored blind of preference) on **≥ 50%** of evidence items. |
| R7 | Depends on one weak assumption | A single assumption rated "low evidence" accounts for **> 60%** of the gap between our price target and the current price. |
| R8 | PT depends on multiple expansion | **> 50%** of base-case price change comes from multiple change rather than EPS change (for a short: from multiple compression). |
| R9 | Proof data unavailable | The KPI that falsifies the thesis is not publicly reported (or reliably observable) within the horizon. |
| R10 | Catalyst already widely anticipated | Consensus estimates have already moved **≥ 75%** of the way to our number over the last 90 days, **or** the variant view is the stated majority view in recent sell-side/press coverage we can find. |
