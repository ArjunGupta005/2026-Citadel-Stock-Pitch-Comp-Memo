# 2026 Citadel Stock Pitch Comp & Memo

**Team Margin Callers: Copart (NASDAQ: CPRT), SHORT**

The final deliverables are the two-page pitch memo ([`MarginCallers.pdf`](MarginCallers.pdf)) and the
supporting financial model ([`MarginCallers.xlsx`](MarginCallers.xlsx)). Everything else in this repo is the
research process that produced them.

## Thesis

The Street knows Copart lost a large insurance customer, which moved most of its units to RB Global's IAA.
We think consensus underestimates how large and how early the FY27 earnings impact will be.

| | Consensus | Our estimate |
|---|---|---|
| Q1-FY27 EPS | $0.41 (Zacks) | **$0.37** |
| FY27 EPS (ex-ACV) | $1.62–$1.65 | **$1.45** |

- **Reference price:** $27.29 (10/1/26 close).
- **Valuation:** a base-case value of **$23.10** (15% downside) and a probability-weighted value of **$24.52**, an expected short return of about 10%.
- **Horizon:** Q1-FY27 through Q2-FY27, with exit planned for mid-February 2027. The Q1 and Q2 prints are the discovery window.

This is a timing call on a discrete FY27 earnings hole, not a call on business quality. A post-earnings-reaction
study (2004–26) showed CPRT tends to *recover* after large negative reactions, so the position is sized to the
discovery window rather than run as a 12-month structural short.

## Method

The process was pre-registered to keep the idea selection honest:

1. **Locked rules first.** The judging rubric (`00`), PM questions (`01`, SHA-256 hashed) and numeric restart
   criteria (`04`) were all fixed before any data was pulled.
2. **Screen.** An 8-name universe (ABNB, ADBE, CPRT, GEV, NCLH, NKE, SBUX, SPOT) was built from SEC EDGAR XBRL and
   8-K earnings releases. Each name was scored on 8 equal-weight criteria in `02_candidate_scorecard.xlsx`.
3. **Deep dives.** Earnings calls, 10-K/10-Q filings and peer calls were read for the top three names. That work produced
   16 years of point-in-time KPIs (`kpi_extract.py`) and guidance history.
4. **Hypotheses and evidence.** 11 hypotheses were written and evidence was stacked for and against each
   (`thesis/`). Rejected rounds are kept in `thesis/rejected/`, and `03_research_log.md` records why each was dropped.
5. **Scenario engine.** A KPI-driven model (CPRT: units × revenue per unit with fixed costs) backs out Street-implied
   KPIs and compares them with our own (`scenario_engine.py`).
6. **Event studies.** Point-in-time post-earnings drift and market-condition tests (`backtest.py`, `market_condition_test.py`)
   showed CPRT is about 73% idiosyncratic.
7. **Valuation.** The model values CPRT at the exit date as the PV of distributions plus a terminal value at a 9.74% cost
   of equity, plus net cash. The payout is tied to growth and ROIC, so P/E is an output rather than an input. Four
   probability-weighted scenarios run from "loss deepens" to "Street is right".
8. **Independent audit.** The Excel model is fully recalculated and checked against an independent Python reference
   (`verify_final_model_v4.py`, `cprt_model_v4.py`). The memo text is also cross-checked number-by-number against the
   model (`audit_v4_consistency.py`). See `audit/` and `final/QA_report_v4.md`.

## Repo layout

| Path | Contents |
|---|---|
| `MarginCallers.pdf` / `.xlsx` | Final submitted memo and model |
| `final/` | HTML source of the final memo, QA report and rendered page check |
| `00`–`04_*.md` | Locked framework, PM questions, scorecard, research log and restart criteria |
| `candidates/<TICKER>/` | Per-name investigation notes and catalyst maps |
| `thesis/` | Hypotheses, evidence stacks and rejected rounds |
| `framework_B/` | Second-framework checks (CPRT consensus reconciliation, GEV reverse DCF) |
| `audit/` | Backtest, scenario and valuation audits |
| `scripts/` | Data pulls, screening, scenario engine, backtests, model and memo builders, and verification |
| `data/` | Processed KPIs, valuation history, comps and market data |

Raw SEC filings and call transcripts aren't included. Run `scripts/sec_pull.py` to download the filings again,
and set `SEC_USER_AGENT` to your own contact string as SEC requires.

## Disclaimer

This is a student competition submission, not investment advice.
