# 03 — Research Log

Append-only. One dated entry per session. Record what was looked at, what changed your mind, and what was rejected and why.

---

## 2026-10-01 — Project setup

- Phase 0: `00_judging_framework.md` created and locked (grading only).
- Phase 1: `01_pm_questions_locked.md` pre-registered and locked.
  - SHA-256: `082b89c6802046051aa2e570fb8575badf4572cd12a22dbacfcede298bde4116`
  - Verify later with: `sha256sum 01_pm_questions_locked.md`
- Phase 2: Folder structure built. Candidate universe: ABNB, ADBE, CPRT, GEV, NCLH, NKE, SBUX, SPOT.
- Team name: TBD (rename `model/TeamName.xlsx` and `memo/TeamName.pdf` once decided).

---

<!-- Template for new entries:
## YYYY-MM-DD — <topic>
- Sources:
- Findings:
- Changed my view on:
- Rejected / parked:
- Next:
-->

## 2026-10-01 — Phase 15 pre-registration (done before Phase 3)

- `04_restart_criteria_locked.md` locked with numeric thresholds before any data was pulled.
  - SHA-256: `3d61a6092aafd40636b23429e8e5309c42d55cf0e387b7f9889ad06dca7b414c`

## 2026-10-01 — Phase 3 light screen

- Scripts: `sec_pull.py` (filings + XBRL + earnings dates), `filing_parser.py`, `screen.py`, `screen_proxies.py`, `build_scorecard.py`.
- Data: yfinance (price, multiples, consensus, revisions), SEC EDGAR (XBRL, 8-K 2.02 / SPOT 6-K deck dates).
- Read latest earnings release for all 8 names + news search for the live debate.
- Scores (8 criteria, 1-5, equal weight; rationale per cell in `02_candidate_scorecard.xlsx`):
  NCLH 36 | CPRT 32 | SBUX 32 | ABNB 31 | NKE 30 | ADBE 28 | SPOT 28 | GEV 21
- **Advance: NCLH, CPRT, SBUX** (CPRT/SBUX tie at 32, both within top 3).
- Notable rejections:
  - GEV: only 3.5y history, disagreement is the multiple not EPS (would trip R8).
  - ADBE: Street EPS dispersion only 0.12 -> disagreement is terminal value / multiple (R8 risk).
  - NKE: reports Q1 FY27 tonight (10/01), so the nearest catalyst resolves before the pitch; noisy tariff refunds.
  - SPOT: no quarterly XBRL (6-K filer) -> historical test needs hand-built data.
  - ABNB: close miss (31); debate is well understood (MS: low-DD nights priced).

## 2026-10-01 — Phases 4-6

- Phase 4: read 2 calls + latest 10-Q/10-K + release (+ peer calls: CCL Q3-26, RBA Q2-26) for NCLH, CPRT, SBUX.
  Output: `candidates/<T>/phase4_investigation.md`. Scripts: `transcript_compare.py`, `kpi_extract.py` (16y point-in-time KPIs from releases), `guidance_history.py`.
  - Data fix: guidance ranges ("3.8-4.3%") were parsed as negatives; fixed and re-run.
  - Data caveat: CPRT XBRL EPS is pre-split for older periods; NCLH 2020-23 yields are vs 2019 (excluded).
- New facts found: NCLH 8-K 9/30 (Q3 beat; FY27 net interest $860-880m vs ~$705m FY26; $950m 8.75% notes);
  SBUX 8-K 9/24 (250 NA closures, $300m charges); CPRT: Progressive moved ~90% of units to IAA (ramp May-Jul 2026), ACV $1.9bn cash deal, Adair back as CEO.
- Phase 5: 11 hypotheses in `thesis/phase5_hypotheses.md` (10 numerically ready; S-C not ready).
- Phase 6: evidence stacks in `thesis/phase6_evidence.md`. Strongest net evidence: C-A (CPRT short-leaning). NCLH contested. SBUX small magnitude.
  N-C dropped as information lag (R10); N-D deprioritized (R8). Direction NOT yet decided.

## 2026-10-01 — Phases 7-12, Round 1 → RESTART

- Phase 7: `scenario_engine.py` (KPI-driven: CPRT units x RPU w/ fixed costs; NCLH capacity x yield - NCC - fuel; SBUX comp x margin).
  Street-implied KPIs: CPRT Q1 US ins. units ~-5% (ours -12%); NCLH FY27 yield ~+2.2% (ours +1%); SBUX FY27 margin 13.5% (ours 13.0%).
- Phase 8: `backtest.py` (point-in-time event studies). CPRT post-miss drift +6% 3M (n=13) contradicts short drift; NCLH post-miss
  underperforms peers -5%/-7% (3M/6M, p<0.05). Most single-name tests underpowered (n<8).
- Phase 9: `catalyst_analysis.py` → candidates/<T>/catalyst_map.md. R3 passes for all three.
- Phase 10: `market_condition_test.py`. NCLH R²=0.65 (sector β 0.93) = largely a sector bet; CPRT 73% idiosyncratic.
- Phase 11: `valuation_history.py` (fixed: non-additive share counts, NCLH debt tags), `comps_analysis.py`.
  CPRT P/E 7th pctile, below RBA; NCLH EV/EBITDA 8.7x vs CCL 7.8x with 2x the leverage.
- Phase 12: all hypotheses fail R5 (both directions). See `thesis/rejected/round1_phase12_selection.md`.
- **Decision: restart at Phase 3 with ABNB, NKE (next-ranked), then ADBE/SPOT.**

## 2026-10-01 (evening) — Round 2 triage

- ABNB, ADBE, SPOT fail R1/R5 at triage; GEV not advanced (see `thesis/rejected/round2_triage.md`).
- NKE reported today: FY27 adj. EPS guide $1.15-1.35 vs cons. $1.66; revenue down HSD; Pace $2.5bn savings; after hours -4%.
  Consensus will reset; call transcript not yet posted. ~1:1 on today's numbers. Pending.
- CPRT defined-risk expression (Jan-27 27.5/22.5 put spread) is borderline on R5: 1.4x-2.2x depending on fill.
- Open decision for the user: how to proceed when every candidate fails the pre-registered R5 hurdle.

## 2026-10-01 (late) — Independent audit (no new ideas; no rule changes)

- Errors found and corrected: (E1) Yahoo CPRT `0q` = Q4-FY26 (period end 2026-07-31), not Q1-FY27 → Q1-implied-units claim withdrawn;
  (E2) CPRT gap restated like-for-like (ex-ACV -12% to -18%, not -23%); (E3) 2014 XBRL share-count scale error fixed in valuation_history.py
  (CPRT P/E percentile 2nd, not 7th).
- New scripts: audit_scenarios.py, audit_valuation.py, audit_backtest.py. Output: audit/AUDIT_REPORT.md and audit/*.md.
- Classification: CPRT KILL (R5, R4); NKE REWORK (consensus and transcript not yet available); NCLH KILL (R5, sector bet).
- **No passing thesis for the Oct 2 preliminary under the locked rules.** Memo not started.

## 2026-10-01 (late) — Round 3: new orthogonal hypotheses (ADBE, SBUX, ABNB, SPOT, GEV only)

- Pre-valuation cards written and FROZEN before any valuation: `thesis/round3/01_frozen_hypothesis_cards.md`
  - SHA-256: `75d12718e31bc082d2484d6c82423cf2eb27c704bb0a9951cceeb7ca64618e8b`
- 6 live cards (ADBE-1 short, ADBE-2 long, ABNB-1 short, SPOT-1 short, GEV-1 long, GEV-2 short); SBUX-1 (Japan sale) killed at definition (not modelable).
- Valuation run AFTER freeze (`scripts/round3_valuation.py`): shared-world run (02_valuation.md) found biased against shorts;
  governing per-card construction as in Round 1 (02b_valuation_v2.md). All 6 live cards FAIL locked rules (R5; plus R1/R8/R10 where noted).
  Shorts ADBE-1 / ABNB-1 / SPOT-1 have POSITIVE thesis-true base returns (buyback/growth compounding at a constant multiple).
  GEV-2 closest (1.67x, EV +20.5%) but R8 fails on an EPS basis (deposits are not earnings).
- Conclusion: `thesis/round3/03_conclusions.md`. No new hypothesis passes. Frozen card hash re-verified unchanged.

## 2026-10-01 (late evening) — Framework B created (separate; Framework A results preserved unchanged)

- `framework_B/05_framework_B_locked.md` (Citadel judging criteria + Q&A guidance; no fixed ratio gate). SHA-256: `6c005f7a605a319bf181b61ec9b58c64dd2294731396a2e0dc2d1f14cb4212ea`
- First application: GEV only, direction not assumed. Question: do customer deposits inflate FCF, and is GEV valued on FCF?
- GEV (Framework B): FCF rebuilt from XBRL. TTM deposits (Δ contract liabilities) $19.85bn = 160% of $12.44bn FCF; FCF ex-deposits -$7.4bn;
  earnings-based FCF ~$3.5bn (~71% of the FY26 guide is working capital). BUT the effect is disclosed in the 10-Q MD&A and discussed publicly, and the
  sell-side values GEV on EV/EBITDA and P/E → deposit/FCF hypothesis KILLED (B1). Reverse DCF: price embeds 2028 EBITDA ~$12.9bn + ~15%
  EBITDA CAGR 2029-33. No directional thesis generated. See framework_B/GEV_framework_B_verdict.md.
- CPRT (Framework B, separate; Framework A unchanged): Street reconstructed (JPM OW $40 on cycle turn + share-gain scraping; HSBC Hold, ACV -3% FY27/+4% FY28;
  Baird/Freedom cuts). Price ≈ fundamental value only if Street EPS is right (implied 5-6% growth at CoE 9.7%). Variant = magnitude (FY27 EPS -15 to -21%).
  Four-world distribution: short EV +9.8% (range +5.8% to +21%), max plausible short loss +16% (W4), rate stress +48%; base ~98% EPS-driven.
  VERDICT: REWORK. Pre-registered resolution: terminal Q1-FY27 consensus ≥ $0.385 AND FY27 ex-ACV ≥ $1.62 → PASS (short, close after Q2);
  Q1 ≤ $0.370 or FY27 ≤ $1.50 or estimates already model US ins. units ≤ -10% → KILL; in between → KILL.
- NKE: consensus not reset as of 17:37 ET (FY27 $1.663, no post-guide revisions). On hold.

## 2026-10-01 (night) — CPRT Framework B final: consensus reconciled → PASS (short)

- Reconciliation: Yahoo FY27 $1.75 (n=8) is stale-mixed (30d-ago $1.85 pre-print; FY26 base includes a stale Q4 estimate).
  S&P Global (StockAnalysis, updated 9/25): FY27 $1.62 ($1.56-1.67, n=9), revenue $4.8bn → excludes ACV.
  Zacks (Nasdaq API, pulled 10/1): Q1-FY27 $0.41 (n=4, $0.38-0.43), Q2 $0.37, FY27 $1.65 (n=5), FY28 $1.81. User-cited Q1 ~$0.395 not verifiable (likely Yahoo's stale Q4 row).
- Scenario logic and probabilities unchanged. Short EV on $1.62 basis: +9.8% (full bridge), +7.6% (EPS-only, no multiple change); max plausible loss +16%.
- Pre-registered rule: Q1 0.41 ≥ 0.385 AND FY27 ex-ACV 1.62 ≥ 1.62 (at threshold) → PASS. Short, close after Q2-FY27. Memo construction begun.
- Deliverables v1: model/TeamName.xlsx (live formulas; recalculated with `formulas` engine, EPS matches Python in all 4 worlds;
  short EV +9.8%, EPS-only +7.6%, base PT $23.10, max loss +16%; CoE sensitivity −4.5% at −100bp) and memo/TeamName.pdf (2 pages, blinded).
  Memo claims re-verified against the model (fixes: sensitivity range, post-miss "~75%" not "every", buyback effect, KPI sensitivity $0.016, implied growth ~9%).

## 2026-10-02 — Final submission QA (team: Margin Callers)

- Final files: final/Margin_Callers.xlsx, final/MarginCallers_StockPitch.pdf (from team HTML; tab removed, KPI text black).
- Corrections: carrier identity removed; $209m and JPM claims removed; official ACV wording (8-K Ex. 99.1); cash input 4.7→4.49bn (10-K);
  Treasury 10Y 5.24% verified; memo Ex. 99.2→99.1, $24.62→$24.61, Q1 gap −12%→−11%, falsifier → consolidated margin.
- Recalculation: no errors; EPS matches Python in all worlds; short EV +9.8% unchanged. QA report: final/QA_report.md.

## 2026-10-02 - Visual-only cleanup of Margin_Callers.xlsx
Styling, panes, charts and print setup only. Cell-by-cell diff vs prior model: 0 formula/value changes outside the Summary chart-data block (moved from K3:M15 to A34:C39) and Catalysts A11 (em dash to hyphen). Outputs re-verified ($24.61 PW, +9.8%). Final file saved via Excel with personal-info removal; author "Margin Callers".

## 2026-10-02 - Substantive correction pass (v2)
Valuation moved to mid-Feb 2027 on NTM (Q3 FY27-Q2 FY28) with explicit year-2 recovery; FY28 = standalone + explicit ACV (W1 0 / W2 +0.02 / W3 +0.04 / W4 +0.02); ACV close pro-rated (50% of Q2); Q4 FY26 drag set to reported 9.8pt (W2 13pt => 75% in base, replacing 60%); shares 932m (was 940m, which favoured the short); calibration on FY26 quarterly shares. Probabilities unchanged. ESR +9.8% -> +8.5%, PW $24.61 -> $24.98. Verdict: SUBMIT WITH CAVEAT. v1 files untouched; v2 files: Margin_Callers_v2.xlsx / .pdf.

## 2026-10-02 - V3 surgical QA pass
Wording fixes (crowding claim removed; RB Global transition wording; ACV known-items wording; 286 facilities from 10-K Item 2); EPS bridge corrected (v2 bridge put the Q4 base-drag reversal inside "share count/interest": now +$0.01 / lost customer ($0.19), sums exactly at $0.01); DOJ AML row, gross-returns and constant-horizon-cash notes added. Outputs unchanged (PW $24.98, ESR +8.5%). Verdict READY FOR FINAL AUDIT.

## 2026-10-02 - V4 pass
Year-specific explicit payout (y1 payout 31-40%; normalized 60-80%): W1/W2/W3/W4 $17.34/$23.10/$29.78/$31.30, PW $24.52, ESR +10.2%, W4 loss 14.7%, stress 47.1%. Event study full sample (incl. COVID) governs; still positive (+4.5% to +6.3% 3M, n 9-22). Copart Q4 call facts upgraded to Primary (SEC SC TO-C Ex. 99.2, 0001193125-26-388383). ACV guidance discrepancy, ACV net cash (+$37.3m), Zacks as-of 10/1 documented. 4 linked charts. Status: READY FOR INDEPENDENT FINAL AUDIT.
