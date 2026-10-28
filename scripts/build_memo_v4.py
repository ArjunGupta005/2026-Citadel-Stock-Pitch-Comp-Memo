"""Build final/MarginCallers_StockPitch_v4.html from the v3 memo (v4: year-specific payout outputs, full-sample event study,
SEC-filed transcript sourcing, Zacks as-of date). Numbers from Margin_Callers_v4.xlsx. v2/v3 files untouched."""
from common import ROOT

src = ROOT / "final" / "MarginCallers_StockPitch_v3.html"
dst = ROOT / "final" / "MarginCallers_StockPitch_v4.html"
s = src.read_text(encoding="utf-8")
R = [
    ('<div class="kpi"><b>$23.60</b><span>Base-case value (mid-Feb 27)<br>13.5% stock downside</span></div>',
     '<div class="kpi"><b>$23.10</b><span>Base-case value (mid-Feb 27)<br>15.3% stock downside</span></div>'),
    ('<div class="kpi"><b>$24.98</b><span>Probability-weighted value<br>+8.5% expected short return</span></div>',
     '<div class="kpi"><b>$24.52</b><span>Probability-weighted value<br>+10.2% expected short return</span></div>'),
    ('our post-earnings-reaction study (2004-26) shows CPRT averaged +4.6% to +6.9% 3-month excess returns after large negative reactions.',
     'our post-earnings-reaction study (full sample 2004-26, n = 9-22) shows CPRT averaged +4.5% to +6.3% 3-month excess returns after large negative reactions.'),
    ('Copart Q4-FY26 earnings release, SEC 8-K Ex. 99.1, and earnings call (9/10/26)',
     'Copart Q4-FY26 earnings release (SEC 8-K Ex. 99.1) and earnings-call transcript (SEC Schedule TO-C Ex. 99.2)'),
    ('Zacks (10/2/26). SEC accession numbers: model Sources sheet.', 'Zacks (as of 10/1/26; re-verified 10/2/26). SEC accession numbers: model Sources sheet.'),
    ('Value is the PV of distributions (payout 1 - g/ROIC) and a terminal value at a 9.74% cost of equity, plus net cash at that date, so the P/E is an output.',
     'Value is the PV of distributions and a terminal value at a 9.74% cost of equity, plus net cash at that date, so the P/E is an output; the year-1 '
     'payout is linked to modeled recovery growth (1 - g1/ROIC) and the normalized payout (1 - g/ROIC) applies thereafter.'),
    ('<td class="right">12.7x</td><td class="right">$17.85</td><td class="right pos">+34.6%</td>',
     '<td class="right">12.2x</td><td class="right">$17.34</td><td class="right pos">+36.5%</td>'),
    ('<td class="right"><b>14.5x</b></td><td class="right"><b>$23.60</b></td><td class="right pos"><b>+13.5%</b></td>',
     '<td class="right"><b>14.2x</b></td><td class="right"><b>$23.10</b></td><td class="right pos"><b>+15.3%</b></td>'),
    ('<td class="right">16.6x</td><td class="right">$30.24</td><td class="right neg">-10.8%</td>',
     '<td class="right">16.3x</td><td class="right">$29.78</td><td class="right neg">-9.1%</td>'),
    ('<td class="right">16.7x</td><td class="right">$31.62</td><td class="right neg">-15.9%</td>',
     '<td class="right">16.5x</td><td class="right">$31.30</td><td class="right neg">-14.7%</td>'),
    ('<td class="right"><b>$24.98</b></td><td class="right pos"><b>+8.5%</b></td>', '<td class="right"><b>$24.52</b></td><td class="right pos"><b>+10.2%</b></td>'),
    ('a 10 / 16pt run-rate drag moves W2 value to $24.42 / $22.77; a 0.5pt lower cost of equity cuts the expected short return to +1.6%.',
     'a 10 / 16pt run-rate drag moves W2 value to $23.92 / $22.29; a 0.5pt lower cost of equity cuts the expected short return to +3.3% (1pt: -4.7%).'),
    ('A 3.5% 10-year stress implies a <b>48.8%</b> loss vs 15.9% in W4.', 'A 3.5% 10-year stress implies a <b>47.1%</b> loss vs 14.7% in W4.'),
    ('after large negative reactions (n = 8-21).</td>', 'after large negative reactions (full sample, n = 9-22).</td>'),
    ('the probability-weighted value is <b>$24.98</b> (+8.5% expected short return; W2 $23.60), with a 15.9% W4 loss and a 48.8% rate-cut stress loss.',
     'the probability-weighted value is <b>$24.52</b> (+10.2% expected short return; W2 $23.10), with a 14.7% W4 loss and a 47.1% rate-cut stress loss.'),
    ('<title>Margin Callers - CPRT Short (v3)</title>', '<title>Margin Callers - CPRT Short (v4)</title>'),
]
for a, b in R:
    assert a in s, a[:90]
    s = s.replace(a, b)
dst.write_text(s, encoding="utf-8")
print("wrote", dst)
