# Citadel Pitch: Independent Pipeline Audit

**Prepared:** 2026-10-01 (evening), before the Oct 2 preliminary submission. **Status: audit complete. No memo writing has started.**
**Locked rules unchanged:** `04_restart_criteria_locked.md` (SHA-256 `3d61a609…b414c`, logged before any data pull). R5 = base gain ≥ 2.0× adverse loss **and** probability-weighted return ≥ +10%, 25/50/25 weights.
**Top 3 audited:** CPRT, NKE, NCLH (ranked by Phase-12 score; NKE added per your instruction as the only name whose information set changed today).

> **Bottom line: no current thesis passes.** CPRT is KILLED (R5 fail + R4 contradiction). NCLH is KILLED (R5 fail in both directions; mostly a levered sector bet). NKE is REWORK: the consensus reset and transcript needed to define a variant do not exist yet, and it cannot be completed by Oct 2. The audit found three errors in my earlier work, listed in §0. All three made CPRT look *better* than it is.

---

## 0. Errors found by this audit (corrected in code and data)

| # | Error | Effect | Fix |
|---|---|---|---|
| E1 | **"CPRT Q1-FY27 consensus $0.397" was wrong.** Yahoo's `0q` row has period end **2026-07-31**: the stale estimate for Q4-FY26, which already printed $0.35 on 9/10. Yahoo's CPRT feed has not rolled forward since the print. | The claim "Street implies Q1 US insurance units −5% vs our −12%" was invalid. | Withdrawn. Re-done on the correctly dated Q2-FY27 row (period end 2027-01-31) in `scenario_engine.py` / `audit_scenarios.py`. |
| E2 | **"Street FY27 EPS 23% too high" overstated the like-for-like gap.** Our $1.35 includes ACV GAAP losses, amortization and forgone interest; most Street models probably exclude ACV until close. | Like-for-like (ex-ACV) gap is **−18% vs Yahoo mean, −12% vs Yahoo low, −14% to −15% vs press aggregators**. | §3 shows every variant. |
| E3 | **CPRT P/E history contained 185 corrupt days (2014).** Copart's 2014 10-Q XBRL tagged diluted shares in thousands (131,486 vs 131.5m), which gave P/E ≈ 0.03x. | The percentile was mis-stated (7th; correct value is **2nd**). The fix makes CPRT look *cheaper*, which hurts the short. | Scale-error guard added to `valuation_history.py`; all downstream files re-run. |

---

## 1. Candidate scorecard: all 8 names

Prices 2026-10-01 close (NKE: $33.69 after hours, post-release). "Adverse" = bear world for a long, bull world for a short. Rows marked *triage* used lighter Phase 4 work (`thesis/rejected/round2_triage.md`). Full models: `data/processed/<T>_scenarios.csv`, `audit/scenario_audit.md`.

| Rank | Name | Direction tested | Variant perception | Key KPI | 3-12m catalyst | Base | Adverse loss | EV | Reward/risk | Verdict & exact reason |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CPRT | Short (long also) | The Progressive volume loss (about −13pt of US insurance units) runs at full rate through Q1-Q3 FY27 and is not fully in estimates | US insurance units y/y | Q1-FY27 print (est. 11/19); ACV close and first consolidation (Q2, est. Feb) | −11.3% (short gains 11.3%) | −38.8% (bull re-rate to 21x) | +5.5% | 0.29x | **KILL.** R5 fails (0.29x, EV +5.5%). R4: post-miss drift is +6.0% at 3M (n=13), opposite sign, robust to thresholds |
| 2 | NKE | Long & short | Undefined: the guide reset today; post-reset consensus not yet observable | Revenue (geo × channel), GM | Q2-FY27 (est. mid-Dec) | +21.7% (long, triage) | −19.9% | +21.7% | 1.09x | **REWORK.** R1/R2 cannot be evaluated: consensus is stale (pulled 16:45 ET, no post-guide revisions) and the call transcript is not yet published. Triage R5 1.09x fails anyway. Post-miss drift is negative (6M −7%, n=14) |
| 3 | NCLH | Long & short | Market prices a structural problem (long) vs FY27 yield recovery over-estimated (short) | FY27 Net Yield | FY27 guide (est. late Feb-27) | Long +17.3% / short −17.3% | Long −82.3% / short −146.9% | Long +24.8% | Long 0.21x / short <0 | **KILL.** R5 fails both ways. Factor R² 0.65 (cruise sector β 0.93) = sector bet. Leverage >6x makes the bear case near-wipeout |
| 4 | SBUX | Long & short | None ≥5%: Street FY27 margin of +180bp is supported (China deconsolidation, no IEEPA tariffs, coffee −20%) | NA operating margin | FY27 guide 10/29 | +2.1% | −23.5% | +1.1% | 0.09x | **KILL.** R1 fails (−4.4% EPS gap); R5 fails |
| 5 | ADBE | Long & short (*triage*) | Net new ARR −36% y/y → ARR growth slows, but the EPS gap is only about 3% | Net new ARR | Q4 + FY27 guide (est. 12/9); CEO change 12/1 | +7.3% | −17.1% | +11.5% | 0.43x | **KILL.** R1 (EPS gap <5%); R5 ratio fails |
| 6 | ABNB | Long & short (*triage*) | Only variant: FX tailwind (Q2 +17% reported vs +13% ex-FX) fades in 2027 = macro bet | Nights booked | Q3 print (est. 11/5) | +4.7% | −19.0% | +4.5% | 0.25x | **KILL.** R1; R5; Phase-10 macro-bet test |
| 7 | SPOT | Long & short (*triage*) | No measurable gap; no quarterly XBRL history | Subs × ARPU, GM | Q3 print (est. 10/22) | −1.1% | short: −30.2% | ≈0% | <0.1x | **KILL.** R1; R5 |
| 8 | GEV | — | Disagreement is about the multiple, not EPS; 3.5 years of history | Orders / backlog | Q3 print (est. 10/28) | — | — | — | — | **KILL.** Not advanced in Phase 3 (R8 risk; no backtest history) |

---

## 2. Top-3 thesis summaries

### CPRT: Short (KILL)
- **One line:** The market has de-rated Copart for slowing volume but has not marked FY27 EPS to the full-run-rate loss of Progressive's salvage volume.
- **Consensus:** FY27 (Aug-26 to Jul-27) EPS $1.75 mean (Yahoo, n=8; range $1.62-1.83). Press aggregators $1.66-1.69. Q2-FY27 $0.375 (+4% y/y).
- **We believe:** FY27 GAAP EPS $1.43 ex-ACV ($1.35 incl.). Q2-FY27 $0.33 ex-ACV.
- **Numerical evidence:**
  - Q4-FY26 US insurance units −7.5%, versus +2.3% excluding one customer.
  - RB Global on 8/4: its largest partner was expanded to all 50 states, with volume "transitioning over the last 90 days".
  - Progressive auto policies in force +7-9% y/y (August).
  - Q4 operating margin 32.0% vs 36.7%; OpEx/car +12.7%.
  - Manheim index −0.4% y/y in mid-September, its first negative reading of 2026.
  - ACV TTM operating loss −$57m; $1.9bn cash consideration.
- **KPI:** US insurance units y/y (disclosed on calls only). OpEx/car.
- **Catalysts:** see §8.
- **Valuation (P/E on FY28E):**

  | World | FY28E EPS | Multiple | Price | Return |
  |---|---|---|---|---|
  | Bear | $1.20 | 14x | $16.85 | −38% |
  | Base | $1.51 | 16x | $24.20 | −11% |
  | Bull | $1.80 | 21x | $37.89 | +39% |

- **Strongest opposite side:**
  - Underlying insurance volume excluding the lost customer has turned positive.
  - Total-loss frequency is at a record 23.3%, with severity +8.8%.
  - The stock is at the 2nd percentile of its trailing P/E since 2011 and below RBA (16.8x).
  - CPRT historically **recovers after misses** (+4.6% to +6.9% 3M excess at every threshold).
- **Falsified if:** Q1-FY27 US insurance units are better than −6%; or OpEx/car growth is ≤ +3%; or ACV is GAAP-neutral by Q2.

### NKE: Undetermined (REWORK)
- **One line:** No thesis yet. Today's guide (FY27 adjusted EPS $1.15-1.35 vs $1.66 pre-guide consensus; revenue down high-single digits) reset the debate, and a variant must be measured against post-reset consensus, which does not exist yet.
- **Consensus:** FY27 (Jun-26 to May-27) $1.66, but **stale** (no revision since the release). FY28 $2.10, also stale.
- **We believe:** No independent estimate. The guide implies Q2-Q4 revenue about −9% (vs Q1 −4%) and Q2-Q4 EPS about −30% y/y.
- **Evidence for each side:**
  - *Guide may be conservative:* new CFO (8/17), a $2.5bn "Pace" savings program, Q1 EPS beat ($0.48 vs $0.44), GM +60bp.
  - *Real deterioration:* June guide was "flattish earnings" → now about −20%; retail slowed from mid-April; Converse −28%; China and Jordan "repositioning".
  - *History:* post-miss drift is negative at every threshold (6M −6% to −7%; n=9-17).
- **Catalysts:** Q2-FY27 (est. mid-Dec). Pace milestones.
- **Valuation (triage, P/E on FY28E, vs $33.69 after hours):**

  | World | FY28E EPS | Multiple | Price | Return |
  |---|---|---|---|---|
  | Bear | $1.35 | 20x | $27 | −20% |
  | Base | $1.70 | 24x | $41 | +22% |
  | Bull | $2.05 | 27x | $55 | +63% |

- **Strongest opposite side (to a long):** management has cut guidance repeatedly. Each prior reset (FY25, June-26 → Oct-26) was followed by further cuts and lower prices.
- **Falsified (long) if:** Q2 revenue decline is worse than −10% or gross margin is down y/y.

### NCLH: Long or short (KILL)
- **One line:** Either the market prices NCL's self-inflicted demand problem as permanent (long), or the Street still over-estimates the 2027 yield recovery (short).
- **Consensus:** FY27 adjusted EPS $1.67 (n=26; $1.22-1.95). With the new $870m interest guide, that implies about +2.2% FY27 yield.
- **We believe:** About +1% yield; adjusted EPS $1.46 (−12.7%).
- **Evidence:**
  - Management: 1H27 yields negative, "2028 first normalized year".
  - 8-K of 9/30: FY27 net interest $860-880m vs ~$705m; $950m notes at 8.75%.
  - CCL: "June was an inflection point"; 2027 50% booked at record pricing.
  - NCLH beats its next-quarter yield guide 79% of the time.
- **KPI:** FY27 Net Yield (constant currency).
- **Valuation (EV/EBITDA on FY28E, net debt $15.3bn):**

  | World | Multiple | Price | Return |
  |---|---|---|---|
  | Bear | 7.0x | $2.59 | −82% |
  | Base | 8.0x | $17.17 | +17% |
  | Bull | 9.5x | $36.15 | +147% |

- **Strongest opposite side (to either direction):** the equity is a roughly 6x levered option on industry yields. 65% of its variance is explained by market and sector factors.
- **Falsified:** for the short, if the FY27 guide is ≥ +2%; for the long, if the FY27 guide is ≤ 0% or net leverage is ≥ 6.5x.

---

## 3. Consensus integrity audit

Provider: Yahoo Finance `earningsTrend` (secondary market data), pulled **2026-10-01 16:45 ET** via `yfinance`, raw period end dates verified. Yahoo publishes the mean only (no median). Primary sources for company numbers are SEC filings.

| Claim | Fiscal period (verified end date) | Consensus (mean) | Low / High / n | Updated after latest earnings? | Our estimate | Gap | Alignment check |
|---|---|---|---|---|---|---|---|
| **"CPRT Street EPS ~23% too high"** | FY27, ending 2027-07-31 | $1.7506 | $1.619 / $1.83 / 8 | Partly: was $1.851 on 9/1 (pre-print) → $1.751 now. The provider's FY26 base of $1.58 ≠ reported $1.55 (stale Q4 estimate inside) | $1.350 GAAP incl. ACV; **$1.433 ex-ACV** | **−22.9% incl. / −18.2% ex-ACV.** vs low −11.5% ex; vs press $1.66-1.69 −13.7% to −15.2% ex | Fiscal: ✓ Aug-Jul. Shares: 940m model vs 943m Q3 diluted (XBRL) / ~927m outstanding ✓. Tax: 19.5% vs 17-21% recent ✓. Basis: GAAP (Copart reports GAAP only) ✓. **ACV treatment in Street models: unknown ⚠.** Model calibration: FY26 replay $1.571 vs $1.55 actual (+1.4%) |
| CPRT Q1-FY27 = $0.397 | **Invalid.** Row period end is 2026-07-31 (Q4-FY26, actual $0.35) | — | — | Stale | — | — | **Withdrawn (E1)** |
| CPRT Q2-FY27 | ending 2027-01-31 | $0.3745 | $0.36 / $0.40 / 8 | Yes (was $0.387 30d ago) | $0.302 incl. / $0.329 ex-ACV | −19.4% / −12.1% | Same as above |
| NKE FY27 | ending 2027-05-31 | $1.6626 | $1.296 / $1.96 / 35 | **No.** Pulled after release with no post-release revisions | Guide: adjusted $1.15-1.35 (excludes ~$0.15 Pace charges) | Guide mid vs consensus −24.8% | Basis ⚠: provider's FY26 base of $2.10 is GAAP including a $0.52 one-time IEEPA refund (underlying $1.58). Consensus may mix GAAP and adjusted |
| NKE FY28 | ending 2028-05-31 | $2.1029 | $1.50 / $3.22 / 35 | No | n/a | n/a | Stale |
| NCLH FY27 | ending 2027-12-31 | $1.670 | $1.22 / $1.95 / 26 | Partly ($1.692 7d ago; cannot tell which analysts include the 9/30 interest guide) | $1.457 adjusted | −12.7% | Basis: company "Adjusted EPS" ✓. Shares 462m vs 464m FY26 guide ✓. Tax ~1% ✓. Calibration: model FY26 EBITDA $2,545m vs guide ~$2,500m (+1.8%; flatters our EPS by ~$0.10) |
| SBUX FY27 | ending 2027-09-30 | $3.12 | $2.95 / $3.40 / 33 | Yes (up from $3.01) | $2.98 | −4.4% | Non-GAAP ✓; 1.14bn shares; 23.5% tax |

**Conclusion on the headline claim:** CPRT's FY27 consensus is thin (n=8) and partly stale, and its period base doesn't match reported GAAP. The defensible statement is: *"our ex-ACV FY27 GAAP EPS is 12-18% below the range of published consensus means; 23% only if ACV is included in ours and excluded from theirs."*

---

## 4. Risk/reward construction audit

Full tables (KPIs → revenue → margins → EPS → multiple → target → return → probability → EV) are in `audit/scenario_audit.md`. Summary:

**CPRT (FY27 GAAP; 940m shares; 19.5% tax; weights 25/50/25)**

| World | US ins. units Q1-Q3 | RPU | Fixed-cost growth | US rev. (ex-intl) | Op. income ex-ACV | FY27 EPS (ex-ACV) | FY28 EPS | P/E | Target | Return |
|---|---|---|---|---|---|---|---|---|---|---|
| Bear | −18% | +2.0% | +10% | $3,509m | $1,331m | $1.16 ($1.27) | $1.20 | 14x | $16.85 | −38.3% |
| Base | −12% | +3.5% | +7% | $3,703m | $1,521m | $1.35 ($1.43) | $1.51 | 16x | $24.20 | −11.3% |
| Bull | −7% | +5.0% | +4% | $3,873m | $1,693m | $1.53 ($1.58) | $1.80 | 21x | $37.89 | +38.8% |

**Coherence assessment:**
- EPS paths are internally consistent: each world moves units, price, cost and ACV in the same direction.
- **The asymmetry is driven by the multiple, not by EPS.** Holding the multiple at today's ~15.6x in every world gives short R5 = 3.6x and EV +14%. At a bull multiple of ≥17x the short fails.
- The 21x bull multiple was chosen before results (own-history 25th percentile, near the peer median). A regression of CPRT's P/E on subsequent EPS growth (2012-2025) has **no explanatory power** (R² 0.01). So *all* the multiples are judgment, not estimates.
- Re-choosing the bull multiple now would be post-hoc. **The locked result stands: FAIL.**

**NCLH (FY27 adjusted; 462m shares; $870m interest)**

| World | Capacity | Yield | NCC | Fuel | Net revenue | EBITDA (margin) | EPS | EV/EBITDA | Net debt | Target | Return |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bear | +5% | −2% | +2% | +10% | $7,726m | $2,357m (30.5%) | $0.69 | 7.0x | $15.8bn | $2.59 | −82.3% |
| Base | +5% | +1% | +1% | 0% | $7,963m | $2,714m (34.1%) | $1.46 | 8.0x | $15.3bn | $17.17 | +17.3% |
| Bull | +5% | +3% | −0.5% | −10% | $8,121m | $3,014m (37.1%) | $2.11 | 9.5x | $14.8bn | $36.15 | +146.9% |

**Coherence:** both tails stack four adverse (or favorable) assumptions at once, which exaggerates both tails symmetrically. That doesn't rescue either direction: the long fails on its −82% tail, and the short fails because its base case is a gain for the long.

**SBUX** (`data/processed/SBUX_scenarios.csv`):

| World | NA comp | Op. margin | P/E | EPS | Target | Return |
|---|---|---|---|---|---|---|
| Bear | +2% | 12.2% | 24x | $2.70 | $72.6 | −23.5% |
| Base | +4% | 13.0% | 29x | $2.98 | $96.9 | +2.1% |
| Bull | +6% | 13.8% | 32x | $3.27 | $117.3 | +23.6% |

Bear and bull are roughly symmetric, so there is no edge in either direction.

**NKE** (triage, not a full model): bear $27 / base $41 / bull $55, as in §2.

---

## 5. Breakeven diagnostics (hurdle unchanged; diagnostic only)

| Candidate | Required for 2.0x given today's adverse case | Required adverse floor given today's base case | EV shortfall | Required catalyst reaction |
|---|---|---|---|---|
| CPRT short | Base price $6.10 (−78%), i.e. FY28 EPS $0.38 at 16x or a 4.0x multiple: **not economically plausible** | Bull-case price ≤ $28.83 (+5.7%), i.e. no re-rating above ~16x even if volume recovers | 4.5pt | Base needs −11% cumulative through the Q1/Q2 prints, about 3.6× the median earnings-day move (3.1%). History then shows a +6% 3M rebound after misses |
| NCLH long | Base price $38.74 (+165%) | Bear-case floor ≥ $13.37 (−8.6%). Incompatible with >6x leverage: a 1x lower EV multiple alone moves equity about −40% | none (EV +24.8%) | Not applicable: the bear tail is structural |
| NKE long (triage) | Base price $47.2 (+40%), i.e. FY28 EPS $1.97 at 24x (+16% vs our triage base) | Bear-case floor ≥ $30.10 (−10.6%) vs $27 | none (EV +21.7%) | Q2 revenue decline must come in better than the guide's implied −9%, with no further cut |

---

## 6. Valuation-history audit: CPRT "near cheapest-ever P/E"

Source: `audit/valuation_audit.md`, `scripts/audit_valuation.py`.

| Check | Finding |
|---|---|
| Stock splits | 2:1 in 2012, 2017, 2022 and 2023. TTM EPS shows no jump across any split date → prices and EPS are split-adjusted consistently ✓ |
| Data defect | 2014 XBRL share-count scale error (E3) fixed. Corrected percentile is the **2nd** since 2011 (previously 7th) |
| Trailing vs forward | Trailing GAAP 17.6x = 2nd percentile. Forward on Street $1.75 = 15.6x = 7th percentile of perfect-foresight forward P/E (2012-25). **On our ex-ACV $1.43 = 19.0x = 18th percentile; on $1.35 = 20.2x = 23rd** |
| GAAP vs adjusted | Copart reports GAAP only; no adjusted series exists. Comparison is like-for-like ✓ |
| Interest income | After-tax interest is 10% of TTM net income (vs ~0% through 2023). Ex-cash, ex-interest P/E 16.0x (1st percentile). Cheapness survives the adjustment |
| Rate regime | The 10-year yield is 4.74%, the highest of the sample. The 30-40x years (FY18-24) were 0.5-4% rates with 15-20% EPS growth. In FY12-17 (1.5-2.6% rates, lower growth) CPRT traded at **20-24x** |
| Margin regime | TTM operating margin 35.4%, vs 24-32% in FY12-17 and a 42% FY21 peak. Current EPS sits on above-history margins that are now falling (Q4 32.0%). Not trough earnings |
| Business mix | International (~19% of revenue), non-insurance (~25% of units) and, from Q2-FY27, ACV (dealer marketplace, loss-making). The mix is broadening, so older multiples are only partly comparable |

**Verdict:** the cheapness is **real on the reported numbers but partly misleading**. On forward EPS that already embeds the volume loss, CPRT trades at about 19-20x, roughly the low end of its 2012-2017 range and an appropriate multiple for a no-growth year in a 4.7% rate regime. That cuts both ways: it weakens the "valuation support" bull argument, but it also removes the "de-rating still to come" leg a short needs. Neither direction gets a 2:1 skew from valuation.

---

## 7. Backtest audit

Code: `scripts/backtest.py` (signals, returns), `scripts/audit_backtest.py` (perturbations). Outputs: `data/processed/backtest_summary.csv`, `data/processed/backtest_robustness.csv`, `audit/backtest_audit.md`.

| Control | Status |
|---|---|
| Look-ahead | Signals are dated by the 8-K / SEC `filed` date; returns start at the close of the first trading day *after*. Sample alignment is shown in `audit/backtest_audit.md` ✓ |
| Revised data | `xbrl_quarterly` keeps the first-filed value per period; KPIs are parsed from the original 8-K text ✓ |
| Timestamp alignment | XBRL filed dates trail releases by 2-6 weeks (conservative). 2-day miss signals start at the t+1 close, when the reaction is known ✓ |
| Thresholds | Round numbers fixed in code before results; ±1 step perturbations tested here ✓ |
| Known limits | Small n (4-22); overlapping windows; single-name tests; COVID excluded; no historical consensus, so no revision-based signals |

| Signal (thesis direction) | Thresholds | n | 3M mean (excess, SPY / sector) | 6M mean | Hit rate 3M | Robust? | Real-time knowable? |
|---|---|---|---|---|---|---|---|
| CPRT margin contraction (short) | 200 / 300 / 400bp | 10 / 7 / 6 | −1.1% / −4.9% / −3.6% (sector −0.1% / −2.8% / −1.9%) | +3.0% / −5.0% / −2.0% | 56-83% | **No:** sign flips at 200bp; nothing significant at 3M/6M | Yes (10-Q date) |
| CPRT post-miss (short) | −3% / −5% / −7% | 22 / 13 / 8 | **+4.6% / +6.0% / +6.9%** (sector +4.8% / +6.1% / +6.6%) | +3.5% to +4.4% | 25-33% | **Yes, robustly contradicts** a held short (p 0.06-0.27) | Yes |
| NCLH post-miss vs peers (short) | −3% / −5% / −7% | 20 / 14 / 10 | −2.4% / −5.1% / −5.4% | −4.0% / −7.3% / −7.1% | 74-85% | Same sign throughout; significant only at −5% | Yes |
| NCLH guide deceleration (short) | 1 / 2 / 3pt | 7 / 6 / 4 | vs peers +0.1% / +1.4% / −2.9% | mixed | 40-67% | **No** (n<8; sign flips) | Yes |
| NKE post-miss (short) | −3% / −5% / −7% | 17 / 14 / 9 | −4.3% / −3.4% / −1.5% | **−6.9% / −7.4% / −7.2%** | 56-71% | Same sign throughout; p 0.04-0.36 | Yes |
| SBUX margin expansion (long) | 200 / 300 / 400bp | 9 / 7 / 6 | +1.1% / +3.0% / +6.8% | +6.0% / +6.4% / +14.0% | 44-67% | Same sign; significant only at 400bp (n=6) | Yes |

**Answer:** CPRT's margin-contraction signal would have been knowable in real time but **does not survive small parameter changes**. The robust CPRT finding argues *against* the short. The NKE post-miss signal is the most stable result in the set, and it argues against an immediate NKE long.

---

## 8. Catalyst audit: known vs. new

| Name | Catalyst | Date | Already known / expected | Genuinely new information | Strength |
|---|---|---|---|---|---|
| CPRT | ACV tender expiry | 10/7 (SC TO-T/A) | Deal terms and price | Only whether ≥50% tender (47.8% at 9/30) | Weak |
| CPRT | HSR waiting period | 10/13 (SC TO-T/A) | Pull-and-refile on 9/28 | Whether the FTC issues a Second Request | Medium |
| CPRT | Q1-FY27 results | est. 11/19 (Yahoo calendar; secondary) | The lost customer (HSBC downgrade, press) | **Run-rate size** of the unit loss; OpEx/car under Adair; first post-loss margin | Strong |
| CPRT | Q2-FY27 + ACV consolidation | est. mid-Feb | ACV is loss-making | Purchase-price allocation, GAAP dilution | Strong |
| CPRT | Q4-FY27 (lapping) | est. Sep-27 | Lapping is mechanical | Little: mostly confirms consensus | Weak, at the 12-month edge |
| NKE | Q2-FY27 results | est. mid-Dec | FY27 guide (today) | Whether the guide's implied Q2-Q4 −9% revenue is conservative; Pace savings cadence | Strong, but the variant is undefined |
| NCLH | Q3-26 results | 11/4 (Yahoo calendar) | Beat pre-announced 9/30 | 2027 booked-position color | Weak / medium |
| NCLH | RCL Q3 / CCL Q4 | est. late Oct / mid-Dec | Industry strong (CCL 9/29) | Caribbean 2027 pricing | Medium |
| NCLH | Q4-26 + FY27 guide | est. late Feb-27 | 1H27 negative (guided) | First FY27 yield and EPS guide | Strong |

---

## 9. Source ledger (critical data points for the top 3)

**P** = primary (SEC / company). **S** = secondary (market data, press). All pulled 2026-10-01 unless noted.

| Metric | Value | Type | Source document / date | Section | Local file |
|---|---|---|---|---|---|
| CPRT Q4-FY26 revenue / EPS | $1.152bn / $0.35 diluted | P | 8-K EX-99.1, 2026-09-10 | Income statement | `data/filings/CPRT/8-K_2026-09-10_cprt-ex99_1.htm` |
| CPRT FY26 segment results (US/Intl service revenue, facility, G&A, operating income) | US service $3,388m; Intl $581m; operating income $1,653m | P | 10-K FYE 2026-07-31, filed 2026-09-29 | Segment note | `data/processed/text/CPRT/10-K_2026-09-29_cprt-20260731.txt` |
| CPRT quarterly segment data FY24-26 | see `scenario_engine.CPRT_FY26` | P | 10-Qs filed 2023-11-21 to 2026-05-29 | Segment note | `data/filings/CPRT/10-Q_*` |
| CPRT diluted shares / tax | 942.8m (Q3); 17-21% | P | XBRL companyfacts | WeightedAverageNumberOfDilutedSharesOutstanding | `data/raw/CPRT/companyfacts.json` |
| CPRT US insurance units Q2/Q3/Q4-FY26 | −10.7% / −4.2% / −7.5% (+2.3% ex one customer) | P (call) | Earnings calls 2026-02-19, 05-21, 09-10 | Prepared remarks | `data/transcripts/CPRT_*.txt` (Motley Fool transcription) |
| CPRT OpEx/car, ASP, RPU | +12.7%; +3.5%; +5.4% | P (call) | Q4-FY26 call, 2026-09-10 | CEO/CFO remarks | `data/transcripts/CPRT_Q4-FY2026.txt` |
| Copart–ACV deal | $10.50/sh cash, ~$1.9bn; close by CY-end | P | 8-K 2026-09-10; 10-K | Item 1.01; subsequent events | SEC |
| ACV tender / HSR | 47.78% tendered; extended to 10/7; HSR refiled 9/28, expires 10/13 | P | SC TO-T/A 2026-09-29, 2026-10-01 | Amendment items | SEC |
| ACV financials | TTM revenue $801m; operating loss −$57m | P | ACVA XBRL (10-Qs to Q2-26) | Income statement | `data/raw/ACVA/companyfacts.json` |
| RB Global partner expansion | "all 50 states… last 90 days" | P (peer call) | RBA Q2-26 call, 2026-08-04 | Prepared remarks, Q&A | `data/transcripts/RBA_Q2-2026.txt` |
| Progressive policies in force | Direct auto +9%, agency auto +7% | P (PGR) | PGR August-2026 monthly release, 2026-09-18 | Policies in force | press summary (StockTitan) |
| Manheim index | −0.4% y/y mid-September | S | Cox Automotive, mid-Sep 2026 | Index | web |
| "IAA ~90% of Progressive units" | ~90% | S (unverified) | Transportation Today / substack | — | web: treat as unconfirmed |
| CPRT consensus | FY27 $1.7506 (n=8); Q2 $0.3745 | S | Yahoo earningsTrend, 2026-10-01 16:45 ET | — | §3 |
| CPRT P/E history | 17.6x trailing, 2nd pct | derived | prices (yfinance) + XBRL | — | `data/processed/CPRT_valuation_history.csv` |
| NKE Q1-FY27 | revenue $11.2bn (−4%); EPS $0.48; GM 42.8% | P | 8-K EX-99.1, 2026-10-01 | Highlights | `data/processed/text/NKE/8-K_2026-10-01_q1fy27exhibit991er.txt` |
| NKE FY27 outlook | revenue −HSD; adj. EPS $1.15-1.35 (excl. ~$0.15 Pace) | P | same | Outlook | same |
| NKE FY26 underlying EPS | $1.58 (ex $0.52 IEEPA) | P (call) | Q4-FY26 call, 2026-06-30 | CFO remarks | `data/transcripts/NKE_Q4-FY2026.txt` |
| NKE consensus | FY27 $1.6626 (n=35), not updated post-release | S | Yahoo, 2026-10-01 16:45 ET | — | §3 |
| NKE after-hours price | $33.69 (−4.2%) | S | Yahoo, 2026-10-01 | — | — |
| NCLH Q2-26 KPIs and FY26 guide | yield −2.6% cc; FY ~−5.0%; EBITDA ~$2.5bn; adj. EPS ~$1.50; interest ~$705m | P | 8-K EX-99.1, 2026-07-30 | Guidance table | `data/processed/text/NCLH/8-K_2026-07-30_exh_991.txt` |
| NCLH FY27 net interest | $860-880m | P | 8-K Item 7.01, 2026-09-30 | Item 7.01 | `data/filings/NCLH/8-K_0001104659-26-112116_*` |
| NCLC notes | $950m, 8.75%, due 2031 | P | NCLC press release, 2026-09-30 | — | GlobeNewswire |
| NCLH 2027 commentary | 1H27 negative; 2028 normalized | P (call) | Q2-26 call, 2026-07-30 | CFO Q&A | `data/transcripts/NCLH_Q2-2026.txt` (MarketBeat) |
| NCLH guidance record | beat next-Q yield guide 15/19 | derived | 8-K history 2013-26 | — | `data/processed/NCLH_guidance_history.csv` |
| CCL demand read-across | "June was an inflection point"; 2027 50% booked | P (peer call) | CCL Q3-26 call, 2026-09-29 | Prepared remarks | `data/transcripts/CCL_Q3-2026.txt` |
| NCLH consensus | FY27 $1.670 (n=26) | S | Yahoo, 2026-10-01 16:45 ET | — | §3 |

---

## 10. Final classification

| Candidate | Classification | Concrete reason |
|---|---|---|
| **CPRT (short)** | **KILL** | The EPS variant is real (ex-ACV FY27 −12% to −18% vs published means). But under the locked scenarios R5 fails (0.29x; EV +5.5%), and R4 is triggered: post-miss 3M excess is +4.6% to +6.9% at every threshold, opposite to a held short (n ≥ 8). Passing would require changing scenario multiples after seeing results. |
| **NKE (either direction)** | **REWORK** | Today's reset invalidated consensus; the post-reset consensus and the call transcript are not yet available, so R1/R2 cannot be evaluated. The triage long fails R5 (1.09x), and the post-miss drift (6M about −7%, robust) argues against a near-term long. Cannot be completed honestly by Oct 2. |
| **NCLH (either direction)** | **KILL** | R5 fails both ways (long 0.21x with a −82% bear tail; short loses in the base case). R² 0.65 to market and sector: a levered sector bet, not a company thesis (Phase 10). |

**There is no passing thesis for the Oct 2 preliminary submission under the locked rules.** If a submission is mandatory, that is your call, and it should be made with this audit disclosed rather than by loosening the hurdle. I have not started a memo.

---

## Files for independent review (copied to `audit/export/`)
`02_candidate_scorecard.xlsx` (new sheet "Audit final ranking") · `03_research_log.md` · `04_restart_criteria_locked.md` · `scripts/scenario_engine.py` · `scripts/backtest.py` · `scripts/valuation_history.py` · `scripts/catalyst_analysis.py` · `scripts/audit_scenarios.py` · `scripts/audit_backtest.py` · `scripts/audit_valuation.py` · `audit/*.md` · `candidates/{CPRT,NCLH,NKE}/*` · `thesis/rejected/*`
