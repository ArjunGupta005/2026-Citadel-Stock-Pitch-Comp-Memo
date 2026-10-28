# Round 3 — Valuation v2 (each card's base = its frozen 'expected if true' case; multiple held at today's NTM)

## ADBE-1 (SHORT ADBE, price $241.28)
| world | g | m | s | g28 | pe | FY27_EPS | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bear | 0.060 | 0.440 | -0.050 | 0.070 | 7.000 | 26.711 | 28.581 | 7.000 | 200.067 | -0.171 | 0.250 |
| base | 0.075 | 0.445 | -0.065 | 0.080 | 8.700 | 27.837 | 30.064 | 8.700 | 261.553 | 0.084 | 0.500 |
| bull | 0.100 | 0.455 | -0.075 | 0.140 | 11.000 | 29.439 | 33.560 | 11.000 | 369.164 | 0.530 | 0.250 |
- Consensus FY27 EPS: 27.67 → base gap +0.6% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio -0.16x, EV -13.2% → **FAIL**
- R8: share of base-case move from the multiple: 0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  -3%: n=20, 3M -2.3%, 6M -4.2%; -5%: n=12, 3M -4.3%, 6M -8.2%; -7%: n=9, 3M -1.5%, 6M -9.5%

## ADBE-2 (LONG ADBE, price $241.28)
| world | g | m | s | g28 | pe | FY27_EPS | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bear | 0.065 | 0.440 | -0.040 | 0.070 | 7.000 | 26.558 | 28.417 | 7.000 | 198.917 | -0.176 | 0.250 |
| base | 0.080 | 0.450 | -0.070 | 0.120 | 8.700 | 28.432 | 31.844 | 8.700 | 277.045 | 0.148 | 0.500 |
| bull | 0.100 | 0.455 | -0.080 | 0.140 | 11.000 | 29.599 | 33.743 | 11.000 | 371.170 | 0.538 | 0.250 |
- Consensus FY27 EPS: 27.67 → base gap +2.8% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio 0.84x, EV +16.5% → **FAIL**
- R8: share of base-case move from the multiple: 0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  +3%: n=30, 3M +2.5%, 6M +4.1%; +5%: n=21, 3M +2.4%, 6M +2.3%; +7%: n=12, 3M +5.4%, 6M +3.6%

## ABNB-1 (SHORT ABNB, price $160.47)
| world | gbv | dt | nm | g28 | pe | FY27_EPS | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bear | 0.095 | -0.004 | 0.210 | 0.080 | 21.000 | 5.488 | 5.927 | 21.000 | 124.469 | -0.224 | 0.250 |
| base | 0.110 | -0.003 | 0.220 | 0.100 | 25.900 | 5.873 | 6.460 | 25.900 | 167.322 | 0.043 | 0.500 |
| bull | 0.130 | 0.001 | 0.235 | 0.150 | 29.000 | 6.581 | 7.569 | 29.000 | 219.492 | 0.368 | 0.250 |
- Consensus FY27 EPS: 6.24 → base gap -5.9% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio -0.12x, EV -5.7% → **FAIL**
- R8: share of base-case move from the multiple: 0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  -3%: n=6, 3M -2.3%, 6M -4.8%; -5%: n=5, 3M -1.2%, 6M +0.5%; -7%: n=3, 3M -6.5%, 6M -6.7%

## SPOT-1 (SHORT SPOT, price $491.40)
| world | g | gm | opex | g28 | pe | FY27_EPS | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bear | 0.125 | 0.330 | 0.178 | 0.160 | 23.000 | 14.056 | 16.305 | 23.000 | 428.286 | -0.128 | 0.250 |
| base | 0.140 | 0.333 | 0.174 | 0.180 | 28.100 | 14.819 | 17.487 | 28.100 | 561.182 | 0.142 | 0.500 |
| bull | 0.150 | 0.348 | 0.166 | 0.250 | 32.000 | 16.905 | 21.132 | 32.000 | 772.282 | 0.572 | 0.250 |
- Consensus FY27 EPS: 15.41 → base gap -3.8% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio -0.25x, EV -18.2% → **FAIL**
- R8: share of base-case move from the multiple: 0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  -3%: n=3, 3M +8.8%, 6M +1.6%; -5%: n=3, 3M +8.8%, 6M +1.6%; -7%: n=2, 3M +17.2%, 6M +35.7%

## GEV-1 (LONG GEV, price $987.45)
| world | rev28 | m28 | ev | FY27_2028_EBITDA_bn | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|---|
| bear | 52.000 | 0.200 | 18.000 | 10.400 | 10.400 | 18.000 | 783.206 | -0.207 | 0.250 |
| base | 60.000 | 0.210 | 21.100 | 12.600 | 12.600 | 21.100 | 1083.435 | 0.097 | 0.500 |
| bull | 64.000 | 0.220 | 24.000 | 14.080 | 14.080 | 24.000 | 1358.473 | 0.376 | 0.250 |
- Consensus FY27 2028_EBITDA_bn: None → base gap +nan% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio 0.47x, EV +9.1% → **FAIL**
- R8: share of base-case move from the multiple: 0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  +3%: n=6, 3M +17.6%, 6M +44.0%; +5%: n=3, 3M +20.2%, 6M +35.3%; +7%: n=2, 3M -0.7%, 6M +28.9%

## GEV-2 (SHORT GEV, price $987.45)
| world | fcf27 | pfcf | FY27_FCF_bn | horizon_metric | multiple | target | return | prob |
|---|---|---|---|---|---|---|---|---|
| bear | 7.000 | 19.000 | 7.000 | 7.000 | 19.000 | 507.634 | -0.486 | 0.250 |
| base | 9.000 | 21.900 | 9.000 | 9.000 | 21.900 | 752.290 | -0.238 | 0.500 |
| bull | 13.500 | 21.900 | 13.500 | 13.500 | 21.900 | 1128.435 | 0.143 | 0.250 |
- Consensus FY27 FCF_bn: 12.0 → base gap -25.0% (R1 needs |gap| ≥ 5% unless the KPI gap is ≥ 1σ)
- R5: ratio 1.67x, EV +20.5% → **FAIL**
- R8: share of base-case move from the multiple: -0% (fails if > 50%)
- Kill check (post-reaction drift, holding direction, vs SPY): no robust contradiction
  -3%: n=2, 3M +67.2%, 6M +94.4%; -5%: n=0, 3M +nan%, 6M +nan%; -7%: n=0, 3M +nan%, 6M +nan%

## Summary (v2)
| card | side | gap | bear | base | bull | ratio | ev | R5 | R8 | R4 |
|---|---|---|---|---|---|---|---|---|---|---|
| ADBE-1 | SHORT | 0.006 | -0.171 | 0.084 | 0.530 | -0.159 | -0.132 | FAIL | 0.000 | no robust contradiction |
| ADBE-2 | LONG | 0.028 | -0.176 | 0.148 | 0.538 | 0.844 | 0.165 | FAIL | 0.000 | no robust contradiction |
| ABNB-1 | SHORT | -0.059 | -0.224 | 0.043 | 0.368 | -0.116 | -0.057 | FAIL | 0.000 | no robust contradiction |
| SPOT-1 | SHORT | -0.038 | -0.128 | 0.142 | 0.572 | -0.248 | -0.182 | FAIL | 0.000 | no robust contradiction |
| GEV-1 | LONG | nan | -0.207 | 0.097 | 0.376 | 0.470 | 0.091 | FAIL | 0.000 | no robust contradiction |
| GEV-2 | SHORT | -0.250 | -0.486 | -0.238 | 0.143 | 1.668 | 0.205 | FAIL | -0.000 | no robust contradiction |