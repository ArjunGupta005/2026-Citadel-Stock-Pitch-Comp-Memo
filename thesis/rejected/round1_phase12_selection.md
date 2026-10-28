# Round 1 — Phase 12 selection and restart decision (2026-10-01)

Finalists: NCLH, CPRT, SBUX. Hypotheses from `thesis/phase5_hypotheses.md`.
Scores 1-5 (5 = best). Asymmetry and downside use the anchored scenario engine (`scripts/scenario_engine.py`, multiples anchored in `valuation_history.py` + `comps_analysis.py`).

## Ranking

| Hyp. | Magnitude | Evidence | Falsifiability | Catalyst | Model conf. | Val. asymmetry | Downside cont. | Data | 3-12m fit | **Total /45** |
|---|---|---|---|---|---|---|---|---|---|---|
| **C-A** CPRT short | 5 (-23% FY27 EPS) | 4 | 5 (Q1 US ins. units) | 5 (11/19) | 3 | 1 (P/E 7th pctile, < RBA) | 2 (bull +39%) | 3 | 5 | **33** |
| N-B NCLH long | 2 | 3 | 5 | 4 | 4 | 3 | 1 (bear -82%) | 5 | 4 | 31 |
| S-B SBUX long | 1 | 3 | 4 | 5 | 4 | 2 | 2 | 5 | 5 | 31 |
| N-A NCLH short | 3 (-13%) | 2 | 5 | 4 | 4 | 2 | 1 (bull +147%, 23% SI) | 5 | 4 | 30 |
| S-A SBUX short | 1 (-4%) | 1 (refuted, see below) | 4 | 5 | 4 | 2 | 2 | 5 | 5 | 29 |
| C-B CPRT long | 2 | 3 | 4 | 2 (Sep-27 edge) | 3 | 3 | 2 | 3 | 2 | 24 |

## Restart criteria applied to the top-ranked (C-A), then the next ones

| Criterion | C-A CPRT short | N-B NCLH long | S-B SBUX long |
|---|---|---|---|
| R1 disagreement ≥5% | pass (-23%) | pass (-13%; but EPS *below* Street) | **FAIL** (-4.4%) |
| R2 quantified | pass | pass | pass |
| R3 catalyst ≤12m | pass | pass | pass |
| R4 backtest | margin-contraction signal unsupported (n=7, same sign); **post-miss drift CONTRADICTS (n=13, +6% at 3M)** | post-miss drift vs peers supports N-A, i.e. contradicts N-B | n/a |
| **R5 risk/reward** | **FAIL**: base +11.3% / adverse -38.8% = 0.29x; EV +5.5% | **FAIL**: 0.21x (bear -82%); EV +25% | **FAIL**: 0.09x; EV +1% |
| R8 multiple-driven | pass (price change mostly from EPS) | pass | n/a |
| R10 anticipated | pass (cons. moved ~23% of the way) | — | — |

**Decision: every finalist hypothesis trips at least one pre-registered restart criterion (R5 for all). Per `04_restart_criteria_locked.md`, restart at Phase 3 with the next-ranked names (ABNB 31, NKE 30, then ADBE/SPOT 28).**

## What was learned (kept for the red team and for Round 2)
1. **CPRT:** the EPS variant is real and well-evidenced. The Progressive loss runs at a full rate of about -13pt of US insurance units in Q1-Q3 FY27. Street Q1 implies about -5% vs our about -12%. ACV is GAAP-loss-making. Manheim has turned negative. **But the stock already trades at the 7th percentile of its own P/E history and below RBA.** Historically CPRT recovers after big misses (+6% 3M drift, n=13). Being right on EPS does not give 2:1 asymmetry. *If CPRT falls to ~$20-21 (≈14-15x our FY28E), the long side (C-B) should be re-examined.*
2. **NCLH:** a levered (6x) sector bet. Factors explain R²=0.65 (cruise sector β 0.93), so it fails the "company thesis vs macro bet" test. Equity outcomes run from -82% to +147%, and downside cannot be contained.
3. **SBUX:** S-A was refuted by our own evidence. IEEPA refunds net to about zero for FY26 and FY27 carries no IEEPA tariffs; China deconsolidation is margin-accretive; coffee is -20% y/y. The Street's +180bp FY27 margin is plausible. No disagreement ≥5%.

## Files
- Hypotheses: `thesis/phase5_hypotheses.md`; evidence: `thesis/phase6_evidence.md`
- Models: `data/processed/<T>_scenarios.csv`; backtests: `data/processed/backtest_summary.csv`
- Catalysts: `candidates/<T>/catalyst_map.md`; macro: `data/processed/market_condition_test.csv`; comps: `data/comps/<T>_comps.csv`
