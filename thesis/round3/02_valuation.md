# Round 3 — Valuation of the frozen cards (scripts/round3_valuation.py)

Cards frozen before this file was generated (SHA-256 in 03_research_log.md). Locked rules unchanged. Worlds are economic worlds shared by every card on the same stock; each card is tested in its own direction.

## ADBE-1 (SHORT ADBE, price $241.28)
| world | g | m | s | g28 | pe | FY27_EPS | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bear | 0.065 | 0.440 | -0.050 | 0.080 | 7.000 | 26.837 | 28.984 | 7.000 | 202.890 | -0.159 | 0.250 |
| base | 0.085 | 0.450 | -0.065 | 0.110 | 8.700 | 28.411 | 31.536 | 8.700 | 274.367 | 0.137 | 0.500 |
| bull | 0.100 | 0.455 | -0.075 | 0.140 | 11.000 | 29.439 | 33.560 | 11.000 | 369.164 | 0.530 | 0.250 |
- Consensus FY27 EPS: 27.67 → base gap +2.7% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio -0.26x, EV -16.1% → **FAIL**
- R8: share of base-case move from the multiple: 0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  -3%: n=20, 3M -2.3%, 6M -4.2%; -5%: n=12, 3M -4.3%, 6M -8.2%; -7%: n=9, 3M -1.5%, 6M -9.5%

## ADBE-2 (LONG ADBE, price $241.28)
| world | g | m | s | g28 | pe | FY27_EPS | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bear | 0.065 | 0.440 | -0.050 | 0.080 | 7.000 | 26.837 | 28.984 | 7.000 | 202.890 | -0.159 | 0.250 |
| base | 0.085 | 0.450 | -0.065 | 0.110 | 8.700 | 28.411 | 31.536 | 8.700 | 274.367 | 0.137 | 0.500 |
| bull | 0.100 | 0.455 | -0.075 | 0.140 | 11.000 | 29.439 | 33.560 | 11.000 | 369.164 | 0.530 | 0.250 |
- Consensus FY27 EPS: 27.67 → base gap +2.7% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio 0.86x, EV +16.1% → **FAIL**
- R8: share of base-case move from the multiple: 0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  +3%: n=30, 3M +2.5%, 6M +4.1%; +5%: n=21, 3M +2.4%, 6M +2.3%; +7%: n=12, 3M +5.4%, 6M +3.6%

## ABNB-1 (SHORT ABNB, price $160.47)
| world | gbv | dt | nm | g28 | pe | FY27_EPS | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bear | 0.100 | -0.003 | 0.215 | 0.090 | 21.000 | 5.688 | 6.200 | 21.000 | 130.194 | -0.189 | 0.250 |
| base | 0.115 | 0.000 | 0.225 | 0.120 | 24.000 | 6.172 | 6.912 | 24.000 | 165.895 | 0.034 | 0.500 |
| bull | 0.130 | 0.001 | 0.235 | 0.150 | 28.000 | 6.581 | 7.569 | 28.000 | 211.923 | 0.321 | 0.250 |
- Consensus FY27 EPS: 6.24 → base gap -1.1% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio -0.11x, EV -5.0% → **FAIL**
- R8: share of base-case move from the multiple: -229% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  -3%: n=6, 3M -2.3%, 6M -4.8%; -5%: n=5, 3M -1.2%, 6M +0.5%; -7%: n=3, 3M -6.5%, 6M -6.7%

## SPOT-1 (SHORT SPOT, price $491.40)
| world | g | gm | opex | g28 | pe | FY27_EPS | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bear | 0.130 | 0.332 | 0.176 | 0.180 | 23.000 | 14.449 | 17.049 | 23.000 | 447.846 | -0.089 | 0.250 |
| base | 0.140 | 0.340 | 0.172 | 0.220 | 27.000 | 15.582 | 19.011 | 27.000 | 586.209 | 0.193 | 0.500 |
| bull | 0.150 | 0.348 | 0.166 | 0.250 | 31.000 | 16.905 | 21.132 | 31.000 | 748.148 | 0.522 | 0.250 |
- Consensus FY27 EPS: 15.41 → base gap +1.1% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio -0.37x, EV -20.5% → **FAIL**
- R8: share of base-case move from the multiple: -23% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  -3%: n=3, 3M +8.8%, 6M +1.6%; -5%: n=3, 3M +8.8%, 6M +1.6%; -7%: n=2, 3M +17.2%, 6M +35.7%

GEV note: Street FY27 revenue ($52.8bn) already exceeds management's 2028 target ($52bn), so the base world assumes a raise to about $58bn. A 'raise' alone is consensus-confirming (R10 risk).
## GEV-1 (LONG GEV, price $987.45)
| world | rev28 | m28 | ev | FY27_2028_EBITDA_bn | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|
| bear | 54.000 | 0.180 | 17.000 | 9.720 | 9.720 | 17.000 | 699.389 | -0.292 | 0.250 |
| base | 58.000 | 0.200 | 21.000 | 11.600 | 11.600 | 21.000 | 998.473 | 0.011 | 0.500 |
| bull | 62.000 | 0.220 | 24.000 | 13.640 | 13.640 | 24.000 | 1318.168 | 0.335 | 0.250 |
- Consensus FY27 2028_EBITDA_bn: None → base gap +nan% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio 0.04x, EV +1.6% → **FAIL**
- R8: share of base-case move from the multiple: 0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  +3%: n=6, 3M +17.6%, 6M +44.0%; +5%: n=3, 3M +20.2%, 6M +35.3%; +7%: n=2, 3M -0.7%, 6M +28.9%

GEV-2 note: FCF changes from customer deposits do not change EPS or EBITDA. The only price channel is the market capitalising FCF (P/FCF). That is a multiple / narrative channel by construction.
## GEV-2 (SHORT GEV, price $987.45)
| world | fcf27 | pfcf | FY27_FCF_bn | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|
| bear | 8.000 | 19.000 | 8.000 | 8.000 | 19.000 | 580.153 | -0.412 | 0.250 |
| base | 10.500 | 21.900 | 10.500 | 10.500 | 21.900 | 877.672 | -0.111 | 0.500 |
| bull | 13.500 | 21.900 | 13.500 | 13.500 | 21.900 | 1128.435 | 0.143 | 0.250 |
- Consensus FY27 FCF_bn: 12.0 → base gap -12.5% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio 0.78x, EV +12.3% → **FAIL**
- R8: share of base-case move from the multiple: -0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  -3%: n=2, 3M +67.2%, 6M +94.4%; -5%: n=0, 3M +nan%, 6M +nan%; -7%: n=0, 3M +nan%, 6M +nan%

## Summary
| card | side | gap | bear | base | bull | ratio | ev | R5 | R8 | R4 |
|---|---|---|---|---|---|---|---|---|---|---|
| ADBE-1 | SHORT | 0.027 | -0.159 | 0.137 | 0.530 | -0.259 | -0.161 | FAIL | 0.000 | no robust contradiction |
| ADBE-2 | LONG | 0.027 | -0.159 | 0.137 | 0.530 | 0.862 | 0.161 | FAIL | 0.000 | no robust contradiction |
| ABNB-1 | SHORT | -0.011 | -0.189 | 0.034 | 0.321 | -0.105 | -0.050 | FAIL | -2.291 | no robust contradiction |
| SPOT-1 | SHORT | 0.011 | -0.089 | 0.193 | 0.522 | -0.369 | -0.205 | FAIL | -0.226 | no robust contradiction |
| GEV-1 | LONG | nan | -0.292 | 0.011 | 0.335 | 0.038 | 0.016 | FAIL | 0.000 | no robust contradiction |
| GEV-2 | SHORT | -0.125 | -0.412 | -0.111 | 0.143 | 0.779 | 0.123 | FAIL | -0.000 | no robust contradiction |