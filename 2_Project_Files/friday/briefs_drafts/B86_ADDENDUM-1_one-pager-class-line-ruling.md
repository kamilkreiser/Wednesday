From Friday (laptop seat), Datasec / MPS Commercial Calculator. B86 ADDENDUM-1: Friday's answer to your STOPPED: NEEDS FRIDAY (one-pager class line vs fit). It changes only step 3c; everything else in your brief stands.

## Ruling: **B** — the class line shows only when the snapshot table is NOT capped (≤ 6 packages).
- Capped quotes (> 6 packages) show the server's remainder figures (step 3b) and no class line. The full proposal (§1, §5, §11) itemises every quote by class, so nothing is lost from the customer's papers.
- Do NOT apply option A's tightening (line-height 1, the 4 pt pull into the table margin). Leave your rule as built.
- Target fit, as you measured for B: room left **51 / 46 / 83 / 8 / 3 mm** (typical / draft / small / overflow / overflow-as-draft), every shape exactly 1 A4 page on macOS and Linux. Re-measure and state it in STATUS.

## Why (for your STATUS, quote it)
A 0 mm worst case is a page break waiting for a different browser: Kam prints from his own browser, and our only pagination instrument is Chromium's `page.pdf`. B keeps R1's worst-case margin (3 mm) unchanged. The class line was Friday's own default in your brief (step 3c), not part of Kam's approved mock, so choosing where it shows is Friday's call; Friday reports it to Kam in the deploy report.

## Tests to add or adjust
- Uncapped fixture (≤ 6 packages): class line present, values = the server's `purchaseClassSubtotals` via `classRows`.
- Capped fixture (> 6 packages): NO class line; remainder row still carries the server's figures.
- Red-proof: force the class line on a capped quote in a mutant copy → the overflow-as-draft e2e prints 2 pages → RED; restore → GREEN.

Then continue to the end of your brief: suites, push (fast-forward), STATUS, last line `READY FOR GATE: b79/proposal-two-buttons <sha>`.
