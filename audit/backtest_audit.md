# Backtest audit (scripts/audit_backtest.py)

## Bias controls
- **Look-ahead:** each signal is dated by the public release / SEC filing date (`kpi_extract`: 8-K date; `xbrl_quarterly`: `filed`). Returns start at the close of the first trading day *after* that date (`backtest.fwd_excess`, searchsorted side='right').
- **Revisions:** `xbrl_quarterly` keeps the FIRST-filed value per period (later restatements and comparatives are ignored); release KPIs are parsed from the original 8-K exhibit text.
- **Known residual issues:** (i) XBRL filed dates trail the earnings release by 2-6 weeks, so margin signals are late (conservative, not look-ahead); (ii) 2-day earnings-miss signals use close(t+1), so they are only known at that close, and the window starts there; (iii) COVID window Feb-2020 to Jun-2023 excluded; (iv) overlapping 6M windows inflate t-stats.
- **Threshold selection:** round-number thresholds were written into `backtest.py` before results were run. This audit adds ±1 step perturbations; nothing was chosen ex post.

## Timestamp alignment sample
| Signal | Info public (release / filing date) | Return window starts (close of) |
|---|---|---|
| CPRT margin contraction | 10-Q/10-K filed 2024-09-30 | 2024-10-01 |
| CPRT margin contraction | 10-Q/10-K filed 2024-11-26 | 2024-11-27 |
| CPRT margin contraction | 10-Q/10-K filed 2026-09-29 | 2026-09-30 |
| NCLH earnings miss | 8-K 2016-05-10; reaction measured close(t-1)→close(t+1) | 2016-05-11 (= t+1 close, after reaction known) |
| NCLH earnings miss | 8-K 2015-11-03; reaction measured close(t-1)→close(t+1) | 2015-11-04 (= t+1 close, after reaction known) |
| CPRT earnings miss | 8-K 2005-12-05; reaction measured close(t-1)→close(t+1) | 2005-12-06 (= t+1 close, after reaction known) |
| CPRT earnings miss | 8-K 2004-09-15; reaction measured close(t-1)→close(t+1) | 2004-09-16 (= t+1 close, after reaction known) |

## Results by threshold (excess returns; thesis-direction hit rate)
| family | threshold | bench | n | 1M_mean | 1M_median | 1M_std | 1M_hit | 1M_p | 3M_mean | 3M_median | 3M_std | 3M_hit | 3M_p | 6M_mean | 6M_median | 6M_std | 6M_hit | 6M_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CPRT margin contraction (bp) | 0.020 | SPY | 10 | -0.014 | -0.023 | 0.044 | 0.778 | 0.375 | -0.011 | -0.027 | 0.110 | 0.556 | 0.771 | 0.030 | -0.002 | 0.180 | 0.556 | 0.630 |
| CPRT margin contraction (bp) | 0.020 | sector | 10 | 0.004 | -0.003 | 0.033 | 0.556 | 0.752 | -0.001 | -0.030 | 0.098 | 0.667 | 0.968 | 0.021 | 0.007 | 0.183 | 0.444 | 0.736 |
| CPRT margin contraction (bp) | 0.030 | SPY | 7 | -0.035 | -0.027 | 0.024 | 1.000 | 0.016 | -0.049 | -0.062 | 0.078 | 0.667 | 0.190 | -0.050 | -0.057 | 0.112 | 0.833 | 0.324 |
| CPRT margin contraction (bp) | 0.030 | sector | 7 | -0.015 | -0.007 | 0.022 | 0.833 | 0.170 | -0.028 | -0.041 | 0.081 | 0.833 | 0.439 | -0.052 | -0.062 | 0.123 | 0.667 | 0.349 |
| CPRT margin contraction (bp) | 0.040 | SPY | 6 | -0.028 | -0.027 | 0.018 | 1.000 | 0.028 | -0.036 | -0.027 | 0.080 | 0.600 | 0.376 | -0.020 | -0.026 | 0.095 | 0.800 | 0.658 |
| CPRT margin contraction (bp) | 0.040 | sector | 6 | -0.015 | -0.004 | 0.025 | 0.800 | 0.239 | -0.019 | -0.030 | 0.087 | 0.800 | 0.649 | -0.021 | -0.023 | 0.108 | 0.600 | 0.691 |
| CPRT earnings miss (2d excess) | -0.030 | SPY | 22 | -0.004 | -0.002 | 0.057 | 0.524 | 0.761 | 0.046 | 0.033 | 0.121 | 0.286 | 0.097 | 0.036 | 0.055 | 0.171 | 0.286 | 0.343 |
| CPRT earnings miss (2d excess) | -0.030 | sector | 22 | -0.003 | -0.006 | 0.051 | 0.619 | 0.779 | 0.048 | 0.032 | 0.108 | 0.333 | 0.056 | 0.035 | 0.048 | 0.167 | 0.381 | 0.354 |
| CPRT earnings miss (2d excess) | -0.050 | SPY | 13 | -0.010 | -0.012 | 0.068 | 0.583 | 0.627 | 0.060 | 0.067 | 0.135 | 0.250 | 0.153 | 0.044 | 0.059 | 0.159 | 0.167 | 0.357 |
| CPRT earnings miss (2d excess) | -0.050 | sector | 13 | -0.006 | -0.009 | 0.065 | 0.667 | 0.752 | 0.061 | 0.048 | 0.122 | 0.250 | 0.113 | 0.044 | 0.049 | 0.155 | 0.333 | 0.348 |
| CPRT earnings miss (2d excess) | -0.070 | SPY | 8 | -0.018 | -0.011 | 0.072 | 0.500 | 0.497 | 0.069 | 0.053 | 0.162 | 0.250 | 0.271 | 0.042 | 0.071 | 0.198 | 0.250 | 0.568 |
| CPRT earnings miss (2d excess) | -0.070 | sector | 8 | -0.014 | -0.009 | 0.062 | 0.750 | 0.532 | 0.066 | 0.041 | 0.144 | 0.250 | 0.235 | 0.035 | 0.049 | 0.182 | 0.250 | 0.604 |
| NCLH guide decel (pts) | 0.010 | SPY | 7 | -0.006 | -0.007 | 0.083 | 0.571 | 0.848 | -0.068 | -0.036 | 0.142 | 0.833 | 0.296 | -0.076 | -0.145 | 0.317 | 0.800 | 0.620 |
| NCLH guide decel (pts) | 0.010 | sector | 7 | -0.003 | 0.007 | 0.037 | 0.429 | 0.842 | 0.001 | 0.008 | 0.089 | 0.500 | 0.985 | 0.009 | 0.067 | 0.126 | 0.400 | 0.878 |
| NCLH guide decel (pts) | 0.020 | SPY | 6 | -0.004 | 0.013 | 0.091 | 0.500 | 0.921 | -0.043 | -0.012 | 0.144 | 0.800 | 0.539 | -0.055 | -0.138 | 0.362 | 0.750 | 0.780 |
| NCLH guide decel (pts) | 0.020 | sector | 6 | 0.007 | 0.008 | 0.028 | 0.333 | 0.567 | 0.014 | 0.040 | 0.092 | 0.400 | 0.744 | 0.049 | 0.083 | 0.102 | 0.250 | 0.403 |
| NCLH guide decel (pts) | 0.030 | SPY | 4 | -0.025 | -0.011 | 0.103 | 0.500 | 0.664 | -0.112 | -0.060 | 0.136 | 1.000 | 0.290 | -0.025 | -0.132 | 0.438 | 0.667 | 0.929 |
| NCLH guide decel (pts) | 0.030 | sector | 4 | -0.008 | -0.007 | 0.020 | 0.500 | 0.463 | -0.029 | -0.025 | 0.092 | 0.667 | 0.644 | 0.022 | 0.067 | 0.105 | 0.333 | 0.748 |
| NCLH earnings miss (2d excess) | -0.030 | SPY | 20 | -0.008 | -0.017 | 0.095 | 0.650 | 0.721 | -0.014 | -0.035 | 0.212 | 0.526 | 0.772 | -0.009 | -0.067 | 0.243 | 0.556 | 0.871 |
| NCLH earnings miss (2d excess) | -0.030 | sector | 20 | 0.001 | 0.002 | 0.070 | 0.500 | 0.953 | -0.024 | -0.019 | 0.085 | 0.737 | 0.235 | -0.040 | -0.032 | 0.095 | 0.556 | 0.093 |
| NCLH earnings miss (2d excess) | -0.050 | SPY | 14 | -0.015 | -0.031 | 0.106 | 0.643 | 0.615 | 0.007 | 0.055 | 0.229 | 0.462 | 0.909 | 0.017 | -0.021 | 0.268 | 0.500 | 0.830 |
| NCLH earnings miss (2d excess) | -0.050 | sector | 14 | -0.019 | -0.010 | 0.059 | 0.571 | 0.248 | -0.051 | -0.032 | 0.076 | 0.846 | 0.032 | -0.073 | -0.083 | 0.093 | 0.667 | 0.020 |
| NCLH earnings miss (2d excess) | -0.070 | SPY | 10 | -0.035 | -0.031 | 0.076 | 0.600 | 0.178 | -0.018 | -0.060 | 0.234 | 0.556 | 0.822 | -0.008 | -0.070 | 0.270 | 0.500 | 0.939 |
| NCLH earnings miss (2d excess) | -0.070 | sector | 10 | -0.014 | 0.002 | 0.066 | 0.500 | 0.511 | -0.054 | -0.054 | 0.089 | 0.778 | 0.106 | -0.071 | -0.083 | 0.102 | 0.625 | 0.091 |
| NKE earnings miss (2d excess) | -0.030 | SPY | 17 | -0.019 | -0.010 | 0.058 | 0.706 | 0.182 | -0.043 | -0.045 | 0.106 | 0.706 | 0.117 | -0.069 | -0.077 | 0.169 | 0.647 | 0.110 |
| NKE earnings miss (2d excess) | -0.030 | sector | 17 | -0.011 | -0.013 | 0.056 | 0.588 | 0.422 | -0.040 | -0.028 | 0.096 | 0.588 | 0.101 | -0.068 | -0.052 | 0.128 | 0.706 | 0.044 |
| NKE earnings miss (2d excess) | -0.050 | SPY | 14 | -0.019 | -0.015 | 0.061 | 0.714 | 0.274 | -0.034 | -0.026 | 0.112 | 0.643 | 0.279 | -0.074 | -0.077 | 0.186 | 0.571 | 0.159 |
| NKE earnings miss (2d excess) | -0.050 | sector | 14 | -0.008 | -0.006 | 0.060 | 0.500 | 0.616 | -0.032 | 0.003 | 0.101 | 0.500 | 0.265 | -0.071 | -0.097 | 0.141 | 0.643 | 0.083 |
| NKE earnings miss (2d excess) | -0.070 | SPY | 9 | -0.009 | -0.009 | 0.068 | 0.667 | 0.697 | -0.015 | -0.006 | 0.125 | 0.556 | 0.726 | -0.072 | -0.077 | 0.220 | 0.556 | 0.355 |
| NKE earnings miss (2d excess) | -0.070 | sector | 9 | -0.002 | -0.019 | 0.060 | 0.556 | 0.905 | -0.010 | 0.013 | 0.083 | 0.444 | 0.734 | -0.060 | -0.046 | 0.151 | 0.667 | 0.269 |
| SBUX margin expansion (bp) | 0.020 | SPY | 9 | -0.002 | 0.002 | 0.064 | 0.556 | 0.942 | 0.011 | -0.006 | 0.116 | 0.444 | 0.774 | 0.060 | 0.095 | 0.187 | 0.778 | 0.362 |
| SBUX margin expansion (bp) | 0.020 | sector | 9 | -0.018 | -0.028 | 0.068 | 0.444 | 0.456 | 0.003 | 0.016 | 0.079 | 0.556 | 0.920 | 0.055 | 0.075 | 0.135 | 0.889 | 0.256 |
| SBUX margin expansion (bp) | 0.030 | SPY | 7 | 0.010 | 0.007 | 0.069 | 0.714 | 0.726 | 0.030 | 0.095 | 0.126 | 0.571 | 0.550 | 0.064 | 0.095 | 0.213 | 0.857 | 0.455 |
| SBUX margin expansion (bp) | 0.030 | sector | 7 | -0.008 | 0.018 | 0.074 | 0.571 | 0.798 | 0.011 | 0.028 | 0.089 | 0.714 | 0.744 | 0.055 | 0.080 | 0.155 | 0.857 | 0.382 |
| SBUX margin expansion (bp) | 0.040 | SPY | 6 | 0.032 | 0.027 | 0.037 | 0.833 | 0.088 | 0.068 | 0.099 | 0.083 | 0.667 | 0.101 | 0.140 | 0.114 | 0.080 | 1.000 | 0.008 |
| SBUX margin expansion (bp) | 0.040 | sector | 6 | 0.017 | 0.021 | 0.040 | 0.667 | 0.347 | 0.040 | 0.038 | 0.049 | 0.833 | 0.101 | 0.110 | 0.095 | 0.063 | 1.000 | 0.008 |