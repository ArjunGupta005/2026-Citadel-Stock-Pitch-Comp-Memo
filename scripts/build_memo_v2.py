"""Build final/MarginCallers_StockPitch_v2.html from the v1 memo source; every changed number is taken from
Margin_Callers_v2.xlsx (verified against cprt_model_v2.py). The v1 HTML/PDF are left unchanged."""
from common import ROOT

src = ROOT / "final" / "MarginCallers_StockPitch.html"
dst = ROOT / "final" / "MarginCallers_StockPitch_v2.html"
s = src.read_text(encoding="utf-8")
R = [
    ('<div class="sub"><b>Horizon:</b> Q1-FY27 through Q2-FY27 (~4-5 months) &nbsp;|&nbsp; <b>Reference price:</b> $27.29 (10/1/26 close)</div>',
     '<div class="sub"><b>Horizon:</b> Q1-FY27 through Q2-FY27; planned exit and valuation date mid-Feb 2027 &nbsp;|&nbsp; <b>Reference price:</b> $27.29 (10/1/26 close)</div>'),
    ('We model Q1 EPS of <b>$0.36</b> and FY27 EPS of <b>$1.43 ex-ACV</b>', 'We model Q1 EPS of <b>$0.37</b> and FY27 EPS of <b>$1.45 ex-ACV</b>'),
    ('<div class="kpi"><b>$23.10</b><span>Base-case value<br>15% stock downside</span></div>',
     '<div class="kpi"><b>$23.60</b><span>Base-case value (mid-Feb 27)<br>13.5% stock downside</span></div>'),
    ('<div class="kpi"><b>$24.61</b><span>Probability-weighted value<br>+9.8% expected short return</span></div>',
     '<div class="kpi"><b>$24.98</b><span>Probability-weighted value<br>+8.5% expected short return</span></div>'),
    ('<div class="kpi"><b>$0.36</b><span>Q1-FY27E EPS<br>vs $0.41 Zacks</span></div>', '<div class="kpi"><b>$0.37</b><span>Q1-FY27E EPS<br>vs $0.41 Zacks</span></div>'),
    ('<div class="kpi"><b>$1.43</b><span>FY27E EPS ex-ACV<br>vs $1.62-$1.65 Street</span></div>',
     '<div class="kpi"><b>$1.45</b><span>FY27E EPS ex-ACV<br>vs $1.62-$1.65 published</span></div>'),
    ('Copart operates the largest online salvage-vehicle auction platform, with', 'Copart is a global leader in online salvage-vehicle auctions, with'),
    ('management cited a record <b>23.3%</b> in Q2, with repair costs', 'management cited a record second-quarter <b>23.3%</b> total-loss frequency, with repair costs'),
    ('management said they would have been <b>+2.3%</b> excluding one lost customer. RB Global separately disclosed a major automotive-insurance partner '
     'expanding to all 50 states and integrating substantial incremental volume across 30 states within 90 days.',
     'management said they would have been <b>+2.3%</b> excluding one lost customer, a <b>9.8-point</b> drag. RB Global separately disclosed a major '
     'automotive-insurance partner expanding to all 50 states, with volume transitioned over roughly the prior 90 days.'),
    ('<td><b>Full run-rate through Q1-Q3 FY27</b>; ~13pt drag to U.S. insurance units in base case</td>',
     '<td><b>Full run-rate through Q1-Q3 FY27</b>: ~13pt drag in base case, of which 9.8pt (~75%) already showed in Q4 FY26</td>'),
    ('<td><b>$0.36</b> (-11%)</td>', '<td><b>$0.37</b> (-10%)</td>'),
    ('<td><b>$1.43 ex-ACV</b>; $1.35 including modeled ACV dilution</td>', '<td><b>$1.45 ex-ACV</b> (-10% / -12%); $1.38 including modeled ACV dilution</td>'),
    ('the lost-customer line in our FY27 bridge is approximately <b>$0.19/share</b>, nearly matching the gap between our $1.43 ex-ACV estimate and $1.62 S&P Global consensus.',
     'the lost-customer line in our FY27 bridge is approximately <b>$0.23/share</b>; after pricing and share-count tailwinds, our $1.45 ex-ACV estimate is still '
     '<b>$0.17</b> below the $1.62 published FY27 consensus.'),
    ('<p><b>What is already priced in:</b>', '<p><b>What is already known / widely discussed:</b>'),
    ('Q2 provides a second read and the first meaningful GAAP view of ACV if the transaction closes on schedule.',
     'Q2 provides a second read and the first GAAP view of ACV (the company guides closing by calendar year-end 2026).'),
    ('<p><b>Holding-period discipline:</b> our historical event study shows CPRT often rebounds after large negative earnings reactions.',
     '<p><b>Holding-period discipline:</b> our post-earnings-reaction study (2004-26) shows CPRT averaged +4.6% to +6.9% 3-month excess returns after large negative reactions.'),
    ('S&P Global MI via StockAnalysis (updated 9/25/26); Zacks (10/1/26).',
     'S&amp;P Global MI via StockAnalysis (updated 9/25/26); Zacks (10/2/26). SEC accession numbers: model Sources sheet.'),
    ('<p>We value CPRT on FY28E because FY28 is the next-twelve-month earnings base near our planned Q2 exit. Each scenario uses a fundamentals-linked justified '
     'P/E based on growth, ROIC and cost of equity; net cash is added separately. This avoids relying on an arbitrary headline multiple.</p>',
     '<p>We value CPRT at our <b>planned exit, mid-February 2027</b> (after Q2 FY27). Year-1 earnings are NTM ex-interest EPS (Q3 FY27 + Q4 FY27 + Q1 FY28 + '
     'Q2 FY28); year 2 completes the FY28 recovery. Value is the PV of distributions (payout 1 - g/ROIC) and a terminal value at a 9.74% cost of equity, plus '
     'net cash at that date, so the P/E is an output. FY28 EPS = standalone CPRT + an explicit ACV contribution (W2 +$0.02, consistent with FY28 accretion guidance).</p>'),
    ('<tr><th>Scenario</th><th class="right">p</th><th class="right">FY27 EPS</th><th class="right">FY28 EPS</th><th class="right">P/E</th><th class="right">Value</th>'
     '<th class="right">Stock rtn.</th><th class="right">Short rtn.</th></tr>',
     '<tr><th>Scenario</th><th class="right">p</th><th class="right">FY27 ex-ACV</th><th class="right">FY27 GAAP</th><th class="right">FY28 EPS</th>'
     '<th class="right">NTM EPS</th><th class="right">P/E</th><th class="right">Value</th><th class="right">Short rtn.</th></tr>'),
    ('<tr><td>W1 Loss deepens / costs persist</td><td class="right">20%</td><td class="right">$1.16</td><td class="right">$1.20</td><td class="right">11.9x</td>'
     '<td class="right">$17.12</td><td class="right neg">-37%</td><td class="right pos">+37%</td></tr>',
     '<tr><td>W1 Loss deepens / costs persist</td><td class="right">20%</td><td class="right">$1.28</td><td class="right">$1.18</td><td class="right">$1.33</td>'
     '<td class="right">$1.15</td><td class="right">12.7x</td><td class="right">$17.85</td><td class="right pos">+34.6%</td></tr>'),
    ('<tr><td><b>W2 FY27 trough -> FY28 normalizes</b></td><td class="right"><b>45%</b></td><td class="right"><b>$1.35</b></td><td class="right"><b>$1.51</b></td>'
     '<td class="right"><b>13.6x</b></td><td class="right"><b>$23.10</b></td><td class="right neg"><b>-15%</b></td><td class="right pos"><b>+15%</b></td></tr>',
     '<tr><td><b>W2 FY27 trough -> FY28 normalizes</b></td><td class="right"><b>45%</b></td><td class="right"><b>$1.45</b></td><td class="right"><b>$1.38</b></td>'
     '<td class="right"><b>$1.63</b></td><td class="right"><b>$1.40</b></td><td class="right"><b>14.5x</b></td><td class="right"><b>$23.60</b></td>'
     '<td class="right pos"><b>+13.5%</b></td></tr>'),
    ('<tr><td>W3 Cycle turns / ACV helps</td><td class="right">20%</td><td class="right">$1.53</td><td class="right">$1.80</td><td class="right">15.5x</td>'
     '<td class="right">$30.20</td><td class="right pos">+11%</td><td class="right neg">-11%</td></tr>',
     '<tr><td>W3 Cycle turns / ACV helps</td><td class="right">20%</td><td class="right">$1.61</td><td class="right">$1.57</td><td class="right">$1.92</td>'
     '<td class="right">$1.63</td><td class="right">16.6x</td><td class="right">$30.24</td><td class="right neg">-10.8%</td></tr>'),
    ('<tr><td>W4 Street right / share recapture</td><td class="right">15%</td><td class="right">$1.61</td><td class="right">$1.85</td><td class="right">16.0x</td>'
     '<td class="right">$31.70</td><td class="right pos">+16%</td><td class="right neg">-16%</td></tr>',
     '<tr><td>W4 Street right / share recapture</td><td class="right">15%</td><td class="right">$1.71</td><td class="right">$1.66</td><td class="right">$1.96</td>'
     '<td class="right">$1.70</td><td class="right">16.7x</td><td class="right">$31.62</td><td class="right neg">-15.9%</td></tr>'),
    ('<tr><td><b>Probability-weighted</b></td><td></td><td></td><td></td><td></td><td class="right"><b>$24.61</b></td><td class="right neg"><b>-9.8%</b></td>'
     '<td class="right pos"><b>+9.8%</b></td></tr>',
     '<tr><td><b>Probability-weighted</b> (team scenario probabilities)</td><td></td><td></td><td></td><td></td><td></td><td></td>'
     '<td class="right"><b>$24.98</b></td><td class="right pos"><b>+8.5%</b></td></tr>'),
    ('<p class="small"><b>Base-case bridge:</b> FY26 EPS $1.55 -> lost-customer impact ($0.19) -> underlying/non-insurance growth +$0.02 -> revenue/unit +$0.09 '
     '-> fixed-facility costs ($0.05) -> other +$0.01 = <b>$1.43 ex-ACV</b>; modeled ACV dilution brings GAAP EPS to <b>$1.35</b>.</p>',
     '<p class="small"><b>Base-case bridge:</b> FY26 EPS $1.55 -> share count / interest +$0.05 -> lost-customer impact ($0.23) -> underlying/non-insurance '
     'growth +$0.03 -> revenue/unit +$0.10 -> fixed-facility costs ($0.05) -> other +$0.01 = <b>$1.45 ex-ACV</b>; modeled ACV (close mid-Q2) brings GAAP EPS '
     'to <b>$1.38</b>. Key sensitivities: a 10 / 16pt run-rate drag moves W2 value to $24.42 / $22.77; a 0.5pt lower cost of equity cuts the expected short '
     'return to +1.6%.</p>'),
    ('<tr><td>Oct 7 / 13</td><td>ACV tender / HSR</td><td>Confirms whether closing remains on schedule; secondary to the core short thesis.</td></tr>',
     '<tr><td>Oct 7 / 13</td><td>ACV tender / HSR</td><td>Tender and regulatory milestones, not a close date; the company guides closing by calendar '
     'year-end 2026. Secondary to the ex-ACV thesis.</td></tr>'),
    ('<td>Second full quarter of lost volume and first meaningful GAAP read on ACV if the deal closes. <b>Planned exit.</b></td>',
     '<td>Second full quarter of lost volume and first GAAP read on ACV (model assumes closing during Q2 FY27). <b>Planned exit and valuation date.</b></td>'),
    ('Our Q1 EPS is ~$0.05 below Zacks and our FY27 ex-ACV EPS is ~$0.19-$0.22 below published FY27 consensus.',
     'Our Q1 EPS is ~$0.04 below Zacks and our FY27 ex-ACV EPS is ~$0.17-$0.20 below published FY27 consensus.'),
    ('<td>We limit the holding period to Q1/Q2. A 3.5% 10-year rate stress produces a materially larger loss than W4.</td>',
     '<td>We limit the holding period to Q1/Q2. A 3.5% 10-year stress implies a <b>48.8%</b> loss vs 15.9% in W4.</td>'),
    ('<td>Reduces one secondary FY27 headwind.</td><td>Core thesis is evaluated <b>ex-ACV</b>; acquisition accounting is kept separate.</td>',
     '<td>Moves FY27 GAAP EPS by about -$0.01 to +$0.005.</td><td>Core thesis is evaluated <b>ex-ACV</b>; close timing does not change the mid-Feb value.</td>'),
    ('<tr><td><b>Short is crowded / rebound after miss</b></td><td>Our event study shows CPRT often rebounds after large negative earnings reactions.</td>',
     '<tr><td><b>Short is crowded / rebound after a large negative reaction</b></td><td>Our post-earnings-reaction study shows positive 3-month excess drift '
     'after large negative reactions (n = 8-21).</td>'),
    ('<b>Strategy / market view:</b> we are not underwriting permanent impairment; we expect FY27 estimates to reset before normalization in FY28.',
     '<b>Strategy / market view:</b> we are not underwriting permanent impairment; we expect FY27 estimates to reset before normalization in FY28. Valued at our '
     'mid-Feb 2027 exit, the probability-weighted value is <b>$24.98</b> (+8.5% expected short return; W2 $23.60), with a 15.9% W4 loss and a 48.8% rate-cut stress loss.'),
    ('team model and event study.', 'team model and post-earnings-reaction study.'),
    ('<title>Margin Callers - CPRT Short</title>', '<title>Margin Callers - CPRT Short (v2)</title>'),
]
for a, b in R:
    assert a in s, a[:90]
    s = s.replace(a, b)
dst.write_text(s, encoding="utf-8")
print("wrote", dst)
