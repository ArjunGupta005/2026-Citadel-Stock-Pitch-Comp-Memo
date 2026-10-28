# CPRT under Framework B — separate evaluation

**Date:** 2026-10-01 (evening ET). **Framework:** `05_framework_B_locked.md` (SHA-256 `6c005f7a…`). **Framework A results, the original CPRT scenarios, frozen assumptions and backtest outputs are unchanged**; this file only imports the KPI→EPS function read-only.
**Numbers:** `framework_B/CPRT_framework_b_numbers.md` (`scripts/cprt_framework_b.py`).
**Starting facts (corrected, from the audit):** ex-ACV FY27 EPS gap −12% to −18% vs published means; historically cheap; post-miss 3M excess returns contradict holding a short (+4.6% to +6.9%, robust to thresholds); ACV treatment uncertain; lost-customer impact real, but US insurance volume excluding that customer is positive (+2.3% in Q4-FY26).

---

## 1. What the Street actually believes

| Item | Explicit (stated by analysts / company) | Source | Inferred by us |
|---|---|---|---|
| Ratings / targets | Mostly Buy; targets $36-43 (JPM OW $40, upgraded 9/3; Barrington OP $40, upgraded post-ACV; Baird OP $38, cut from $42; Freedom Buy $36, cut from $39; HSBC Hold $36, downgraded 9/17). Mean ~$41 | Investing.com, MarketBeat, Stocktwits (secondary) | The Street sees CPRT as a temporarily depressed compounder |
| Progressive volume | HSBC: "temporary rebalancing of volumes… could take longer… further declines ahead"; "difficult 2027, limited visibility" | HSBC note via Investing.com | Direction acknowledged. Duration framed as temporary |
| Volume recovery | JPM: collision cycle turning, insurance penetration recovering, self-pay declining, used-price headwinds support total-loss frequency; **proprietary web-scraping shows share gains across several states with a certain carrier** | JPM note via MarketBeat / Motley Fool (9/3, pre-print) | JPM expects offsetting share gains, which we cannot verify |
| Margins | Freedom: "slower near-term earnings conversion" from facility and procurement costs (target cut) | Investing.com (9/14) | Margin pressure acknowledged qualitatively |
| ACV | HSBC: **−3% FY27 EPS, +4% FY28**, $209m synergies. Company: breakeven FY27, accretive FY28 | HSBC; Q4 call | Most models probably exclude ACV until close (Yahoo FY27 range $1.62-1.83 suggests mixed treatment) |
| Guidance | None (Copart does not guide) | Q4 call | — |
| Published numbers | FY27 EPS: Yahoo mean $1.75 (n=8, period end 2027-07-31; was $1.85 pre-print); press aggregators $1.66-1.69; **Q2-FY27 $0.375 (+4% y/y)**. **Q1-FY27 consensus not available from any free source** (Yahoo row stale). FY28 not found | Yahoo earningsTrend 2026-10-01; press | FY27 consensus implies **+7% to +13% EPS growth** vs FY26 $1.55 |

**Consensus belief, in one line:** *"The Progressive loss and cost pressure are real but temporary; FY27 EPS still grows high-single to low-double digits; ACV is roughly −3% FY27 / +4% FY28; the stock is cheap and recovery is coming."*

## 2. What today's price implies
- Ex-cash price $22.29 (cash + securities $4.7bn = $5.00/sh; ACV bought with that cash). On the Street FY27 mean, the ex-cash, ex-interest NTM P/E is **13.5x** (14.0x on press aggregates).
- **Fundamental bridge:** a two-stage justified P/E from growth, incremental ROIC and cost of equity. Cost of equity 9.7% = 10y 5.24% + 0.9β × 5% ERP. CPRT ROIC is ~29% pre-ACV and ~20% post. On this bridge, today's price requires **~5.6-7.3% 5-year EPS growth off Street FY27 EPS**, or **~14-16% growth off our FY27 base**.
- **Rate regime:** the same 10%-growth business is worth ~16x at today's rates and ~33x at FY12-17 rates (10y ~2%). The "cheapest-in-history P/E" is mostly a **rate artefact**: it is not cheap relative to fundamentals if Street EPS is right.
- **Peers:** RBA 16.8x (levered, 18% operating margin), OPLN 20.1x, KMX 18.1x. CPRT's discount to peers looks anomalous given net cash and 32-37% margins. That is the strongest *valuation* argument for the long.
- **Bottom line:** the price is consistent with *Street EPS + mid-single-digit growth*. It is **not** consistent with our FY27 EPS + mid-single-digit growth. Our variant is about earnings, not the multiple.

## 3. Is our variant actually new?

| Element | Already expected by the Street? | Evidence | Variant status |
|---|---|---|---|
| Progressive loss persists Q1-Q3 | **Qualitatively yes** (HSBC "further declines") | HSBC | Direction not new |
| Its EPS magnitude | **No.** Consensus FY27 implies +7-13% growth; Q2-FY27 $0.375 = +4% y/y. Our FY27 −8% ex-ACV (−13% incl.); Q2 $0.33 ex-ACV | Yahoo (period-verified); our model | **New: magnitude** |
| Margin pressure | Qualitatively yes (Freedom) | Freedom | Not new qualitatively; not reflected in estimates |
| ACV dilution | Yes, ~−3% FY27 (HSBC) | HSBC | Our GAAP −5.6% incl. amortization and lost interest: **small variant** |
| Eventual volume recovery | Yes (JPM, HSBC "temporary") | JPM, HSBC | Not a variant; our base world also recovers in FY28 |

**The variant is narrow but real:** the Street knows the *story* but has not put the *numbers* in. It survives B1 only conditionally, because the one quarter that matters (Q1-FY27) has **no verifiable consensus**. If the Q1 number already reflects the decline, the discovery mechanism disappears.

## 4. Fundamental valuation bridge (no free multiples)
Justified ex-cash P/E = two-stage value of $1 of next-year ex-interest EPS, paying out (1 − g / incremental ROIC), at a 9.7% cost of equity and 3% terminal growth. Net cash is added separately.

| World | 5-yr EPS growth after FY28 | Incremental ROIC | Why (economics) | Justified P/E (ex-cash) | Discretionary? |
|---|---|---|---|---|---|
| W1 share loss deepens + cost creep | 3% | 15% | Share loss spreads, costs keep rising, ACV dilutes returns; GDP-like growth | 11.9x | No |
| W2 FY27 trough, FY28 normalises | 6% | 20% | Loss laps, cost actions, ACV breakeven → accretive; mid-single-digit growth like FY12-17 ex-rates | 13.6x | No |
| W3 cycle turns + ACV synergies | 9% | 25% | Total-loss frequency keeps rising, ex-customer growth +3%, $209m synergies | 15.5x | No |
| W4 Street right (share recapture) | 10% | 25% | JPM share-gain data proves out | 16.0x | No |

Cross-checks: peers 16.8-20x support W3/W4 multiples; FY12-17 regime multiples (20-24x) are **not** used because rates are ~300bp higher. **One unavoidable discretionary input remains: the cost of equity.** ±50bp moves the probability-weighted return by about ±6pt (sensitivity in the numbers file).

## 5. Probability-weighted distribution (12-month value on FY28 NTM EPS; GAAP incl. ACV)

| World | Prob. | FY27 EPS | FY28 EPS | Justified P/E | Value | Return | From EPS (log) | From multiple (log) |
|---|---|---|---|---|---|---|---|---|
| W1 | 0.20 | $1.16 | $1.20 | 11.9x | $17.12 | −37.3% | −38.4% | −12.5% |
| W2 | 0.45 | $1.35 | $1.51 | 13.6x | $23.10 | −15.3% | −14.9% | +0.9% |
| W3 | 0.20 | $1.53 | $1.80 | 15.5x | $30.20 | +10.7% | +3.1% | +14.1% |
| W4 | 0.15 | $1.61 | $1.85 | 16.0x | $31.70 | +16.1% | +5.7% | +17.1% |

Probabilities and their evidence:
- **W2 45%:** RBA confirms a full-run-rate transfer, and Progressive's policies in force are +7-9%.
- **W1 20%:** Manheim is now negative, OpEx/car is +12.7%, and RBA expects "more contracts" over 3 years.
- **W3 20%:** record total-loss frequency, and ex-customer volume of +2.3%.
- **W4 15%:** JPM's unverified proprietary share-gain data.

**Results:**
- **Expected return: −9.8% for the stock → +9.8% for a short.** Range across sensitivities: +5.8% (bullish-tilted probabilities 15/40/25/20) to +21% (β 1.03).
- **Maximum plausible loss for a short: +16.1% (W4). Stress: +48% if W3 coincides with the 10y falling to 3.5%.** The short is implicitly short duration. Note, though, that the measured CPRT rate beta was small (−0.04 per 100bp, t −1.6; Phase 10).
- **The short does not depend on an unexplained multiple:** the base-world return is ~98% EPS.

## 6. Catalyst path

| Event (date) | Already known | New information | Supports | Move needed to matter |
|---|---|---|---|---|
| ACV tender expiry 10/7; HSR 10/13 (SC TO-T/A) | Terms; 47.8% tendered; HSR refiled | Second Request or not | Second Request delays dilution → mildly long | Small (<2%) |
| RBA Q3-26 (est. early Nov) | RBA gained the partner in all 50 states | IAA auto units in the first full quarter | Strong IAA units → short | Read-across only |
| **CPRT Q1-FY27 (est. 11/19; Yahoo calendar, secondary)** | Lost customer (qualitative) | **First full-quarter US insurance units, OpEx/car under Adair, operating margin** | US ins. units ≤ −10% and op. margin < 34% → short; ≥ −6% → long | CPRT's 80th-percentile earnings move is 6.7%. At a ~constant 13.5x ex-cash multiple, a **≥7-10% cut to NTM EPS** is needed for a material reaction. Our base implies FY27 consensus falls ~16-21% across Q1 + Q2 |
| **CPRT Q2-FY27 + ACV consolidation (est. mid-Feb)** | HSBC −3% dilution; company "breakeven" | Purchase-price allocation, amortization, ACV losses in GAAP EPS | GAAP dilution > 3% → short | Incremental ~2-3% EPS |
| CPRT Q3-FY27 (est. late May) | — | Last quarter before lapping | Ex-customer trend decides | — |
| CPRT Q4-FY27 (est. Sep-27) | Lapping is mechanical | Growth resumption | Long | Mostly confirms consensus |

**Backtest constraint on the trade:** after negative CPRT reactions, the stock has outperformed by ~+6% over 3M (robust at −3/−5/−7%). Under Framework B this does not kill the *discovery* (Q1/Q2), but it **does kill a passive 12-month hold**: the short's value is front-loaded into Q1-Q2 discovery and should be closed after Q2.

## 7. Opposing long pitch (same rigour)
**Thesis:** "The Street and the market are over-extrapolating one lost carrier into a structural decline; a cycle-bottom, net-cash, 35%-margin compounder is trading below a levered competitor."
1. **Volume:** ex-customer US insurance assignments +2.3% (Q4-FY26), after −4.8% ex-CAT in Q2 → the underlying cycle is turning. JPM's scraping shows carrier share gains.
2. **Total-loss economics:** total-loss frequency at a record 23.3%; severity +8.8%; repair costs +50% vs 2019; falling used prices push more repairs into totals.
3. **Valuation:** 2nd-percentile trailing P/E; below RBA (16.8x) despite net cash and ~2x the margin; Street targets $36-43 (+32-58%).
4. **ACV:** $10bn GMV, entry into dealer and whole-car liquidity, $209m synergies (HSBC); +4% FY28 accretion.
5. **History:** CPRT recovers after misses (+4.6% to +6.9% 3M excess, robust) → the market has repeatedly been wrong to extrapolate CPRT's misses.
6. **Founder back:** Adair's return, cost focus ("per car cost to go down"), and capital for buybacks.

**Long valuation:** needs W3/W4 (35% combined probability): +11% to +16%. Probability-weighted −9.8%. Max plausible long loss −37% (W1).

| Dimension | Short | Long |
|---|---|---|
| Assumptions required | Run-rate loss ≈ −13pt (consistent with the Q4 ramp math, the market-share math and RBA disclosures); costs don't fall fast | Share recapture (unverifiable JPM data) **and/or** a sharp cycle upturn **and** cost cuts, all inside FY27 |
| Catalyst clarity | Q1 + Q2 prints are discrete; **Q1 consensus unknown** | Same prints; plus the Q4-FY27 lap (12-month edge) |
| Valuation support | Price ≈ fundamental value only if Street EPS is right | "Cheap" is largely a rate artefact; the peer discount is the genuine support |
| Falsifiability | Q1 US ins. units ≥ −6% → exit | Q1 US ins. units ≤ −10% → exit |
| History | **Contradicted after misses** | **Supported** by post-miss drift |
| Expected value (our distribution) | +9.8% | −9.8% |

## 8. Framework B verdict: **REWORK**

| PASS requirement | Status |
|---|---|
| Measurable variant | ✅ FY27 EPS −15% to −21% vs Street; KPI = Q1 US insurance units |
| Material stock implication | ✅ base −15% |
| Positive probability-weighted expected return (short) | ✅ +9.8% (range +5.8% to +21%) |
| Credible 3-12 month discovery mechanism | ⚠️ Q1/Q2 prints are discrete, but **Q1-FY27 consensus cannot be verified**, so we cannot show the surprise is not already in the number |
| Explicit downside | ✅ +16% (W4); +48% rate stress |
| Clearly weaker opposing thesis | ⚠️ **Not clearly.** The long has lower EV, but it is backed by a robust historical pattern and proprietary share data we cannot refute |
| No unexplained multiple change | ✅ base ~98% EPS-driven; all multiples bridged; cost of equity disclosed as the one discretionary input |

**Why not KILL:** the short does not rely on multiple compression, the variant is in the numbers rather than the narrative, and expected value is positive under every sensitivity tested.
**Why not PASS:** two PASS conditions are unmet, and both are fixable only with data, not argument.

**Pre-registered resolution rule (set now, before looking):**
1. Obtain the **Q1-FY27 and FY27 consensus** (and whether it includes ACV) from Bloomberg / FactSet / Visible Alpha via a university terminal.
   - Q1-FY27 consensus **≥ $0.385** *and* FY27 (ex-ACV basis) **≥ $1.62** → discovery intact → **PASS** as a short, structured to close after Q2-FY27.
   - Q1-FY27 consensus **≤ $0.370** *or* FY27 ≤ $1.50 → the Street has already marked to the loss → **KILL**.
   - In between → KILL (insufficient surprise).
2. If any provider shows FY27 estimates explicitly modelling US insurance units ≤ −10%, **KILL** (variant not new).

## NKE status (per instruction, not investigated further)
Post-reset consensus **does not exist yet**: Yahoo FY27 is still $1.663 at 17:37 ET 2026-10-01, with zero post-guide revisions (pre-guide figure vs guide of $1.15-1.35). NKE is not worth time until the reset prints.
