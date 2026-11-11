# B1514 ANSWER-1 (SEAT-M120): MPSCALC-113, keep the Administrator's single row where it already fits

From Tuesday (s269), 2026-11-11, answering FOR TUESDAY item 1 of your STATUS (READY B1514: 94fec470b9db184031f487679f7648a41f5a5b81). This file amends your kit; where they differ, this file wins.

**ANSWER: build your own alternative.** The product owner's ruling (C-106: "Yes. One tile alone on a row looks broken.") is about a lone tile. A five-tile row that already fits on one line (Administrator, 1138 to 1357 px at base) is not broken and must not become 3 + 2. So:
1. Scope the 698 to 1357 px three-across rule to the six-tile layout only (your `.kpis:has(> .kpi:nth-child(6))` shape, or an equivalent selector you prove picks exactly the six-tile case and not five).
2. For the Administrator (five tiles) add a rule ONLY over the band where the base shows 4 + 1 (your measured 918 to 1137 px), giving 3 + 2 there; every other width keeps the base layout for five tiles (one row from 1138 px up; 601 to 697 px stays [2, 2, 1] as recorded, not built).
3. Edit only YOUR OWN new Administrator rows in `web/e2e/home-tiles-fill.spec.ts` (the ones at 1317 and 1280 px now expect one row of 5; 1100 stays 3 + 2), measure the new edges by program as before, keep every row at least 40 px inside an edge, run the spec 3 of 3 in both modes, and re-run `b46-home.spec.ts`, `b100-quote-390.spec.ts`, `v1b-frame.spec.ts`, `railLayout.test.ts`, `feedback.test.ts` unedited and green.
4. Red-first: with your current rule (the one-rule version) the new Administrator rows at 1317 and 1280 must be red; with the scoped rules, green.
5. ONE forward commit on `b1514/mps-w3a-web-look-print` (plain fast-forward push of the same ref; no force), same commit rules as the kit (subject ends `(MPSCALC-113)`, one trailer, the repo's identity). Read the ref back.
6. STATUS: a section `ANSWER-1 (Tuesday)` with the before/after perRow table for six and five tiles at 600, 650, 700, 900, 1000, 1100, 1137, 1138, 1280, 1317, 1357, 1400 px; then the last line exactly `READY B1514: <sha40>`. Any failure: `STOPPED: NEEDS TUESDAY <one question>`. Then stop.
