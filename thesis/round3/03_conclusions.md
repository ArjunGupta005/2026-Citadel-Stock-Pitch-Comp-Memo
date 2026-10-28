# Round 3 — Conclusions (generated after the frozen cards; cards unchanged)

**Process:** cards written and hashed first (`01_frozen_hypothesis_cards.md`, SHA-256 `75d12718…618e8b`). Valuation ran afterwards (`scripts/round3_valuation.py`). Locked rules unchanged. Earlier results (CPRT, NCLH, Round 1-2) untouched.

## Two valuation constructions (both reported)
1. **Shared worlds** (`02_valuation.md`): one set of economic worlds per stock. **Flaw found before concluding:** for short cards the base world is neutral rather than thesis-true, which biases against shorts.
2. **Per-card worlds, as in Round 1** (`02b_valuation_v2.md`): base = the card's frozen "expected if true" case, with the multiple held at today's NTM level. **This is the governing construction.** It is the more favorable one for the shorts, and they still fail.

## Results (v2)

| Card | Side | Thesis-true base return | Adverse | EV | R5 ratio | Gap vs consensus | Other locked tests | Classification |
|---|---|---|---|---|---|---|---|---|
| ADBE-1 Freemium masks seat decay | Short | **+8.4%** (stock rises even if the thesis is right) | +53.0% | −13.2% | <0 | EPS +0.6% | R1 fail | **KILL** |
| ADBE-2 Buyback compounding | Long | +14.8% | −17.6% | +16.5% | 0.84x | EPS +2.8% | R1 fail; R5 ratio fail | **KILL** |
| ABNB-1 Low-take-rate GBV mix | Short | **+4.3%** | +36.8% | −5.7% | <0 | EPS −5.9% | R5 fail | **KILL** |
| SPOT-1 Gross-margin plateau | Short | **+14.2%** | +57.2% | −18.2% | <0 | EPS −3.8% | R1 fail | **KILL** |
| GEV-1 Backlog duration | Long | +9.7% | −20.7% | +9.1% | 0.47x | n/a; Street FY27 revenue ($52.8bn) already above the 2028 target ($52bn) | R5 fail; R10 risk | **KILL** |
| GEV-2 FCF = customer financing | Short | −23.8% (short gains 23.8%) | +14.3% | +20.5% | 1.67x | FY27 FCF −25% vs FY26 guide | R5 ratio fail; **R8 fail on an EPS basis** (deposits don't change EPS or EBITDA, so 100% of the move is multiple) | **KILL** |
| SBUX-1 Japan stake sale | — | — | — | — | — | — | Not modelable (Japan P&L undisclosed; no dated catalyst) | **KILL at definition** |

## What the round taught (beyond pass/fail)
- **Growth-slowdown shorts on compounding businesses don't monetize at a constant multiple.** For ADBE, ABNB and SPOT the thesis-true world still has EPS rising (buybacks of 4-7% a year, double-digit growth). A short only works if the market *also* de-rates the stock, which is a narrative bet that R8 is designed to exclude.
- **GEV-2 is the most interesting structural fact found**: deposits went from $20.3bn to $40.0bn in nine months, and FY26 FCF of about 2x EBITDA is customer financing. But it is a balance-sheet timing effect, not an earnings change. The only way it moves the stock is through how the market values FCF, which fails R8 on the locked EPS definition.
- **Backtests were used only as a kill check.** No robust contradiction was found, but samples were too small to carry weight either way (ABNB n=3-6, SPOT n=2-3, GEV n=0-6, ADBE n=9-30).

## Bottom line
**No new orthogonal hypothesis passes.** Combined with the audit (`audit/AUDIT_REPORT.md`), the result across all three rounds is that no Long or Short on the 8 tickers clears the pre-registered rules at today's prices.
