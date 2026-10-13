From Friday (laptop seat), Datasec / MPS Commercial Calculator. B79 ADDENDUM-1: one more item for your branch `b79/proposal-two-buttons`. It ADDS to your brief and changes nothing already in it.

## Authority (verbatim)
Kam, live board 2026-10-13 12:56:05 AEDT (view=friday), ruling card `mpscalc-dashboard-seventh-tile-1013`:
"Decision mpscalc-dashboard-seventh-tile-1013: c — No new tile: make the six tiles fill the row (recommended)"
Option c as he saw it: "Layout only. The tile row changes from 'keep empty slots' (auto-fill) to 'stretch the tiles into them' (auto-fit), so every role's tiles reach the right edge on wide windows, an Administrator's five as well. Optional: a three-across step for mid-size windows where six do not fit on one row. No new words, no server change, no new figure to define."

## Why it is yours
It is one rule in `web/src/styles.css`, a file you already hold (your brief gives you its print block). This addendum widens your write set by exactly one rule. B80 does not touch `styles.css`.

## The item
1. **Change** the home tile row rule (`web/src/styles.css:159` @ 553e7dc, per a drafter's read; re-read it at your base 13d8fd8b and quote the line you change): `repeat(auto-fill, minmax(210px, 1fr))` → `repeat(auto-fit, minmax(210px, 1fr))`. Nothing else in that rule or file outside your print block.
2. **The optional mid-size "three-across" step is NOT ruled. Do not add it.** If your measurement shows the wrap at mid widths looks broken, say so in STATUS; Friday raises it with Kam.
3. **Do not touch** `web/src/screens/Dashboard.tsx`, the tiles, their words or their order. No new words.
4. **Test (NEW file `web/e2e/home-tiles-fill.spec.ts`, Chromium, synthetic data):** at a 1,700 px window the last tile's right edge equals the row's right edge (±1 px) for a six-tile role AND for an Administrator alone (five tiles); at 1,440 px record what you see (rows and tiles per row) and assert no empty slot after the last tile in its row; at 390 px no sideways scroll. **Red-proof:** the 1,700 px assertion is RED with `auto-fill` restored in a copy, GREEN with `auto-fit`.
5. Report it in your STATUS under its own heading `ADDENDUM-1 (home tile row)`: the line before/after, the widths measured, the test and its red-proof. It rides through the same tier-1 gate as the rest of your branch.

## Partition (added)
B79 may now also touch: the one `.kpis` grid rule in `web/src/styles.css`, and NEW `web/e2e/home-tiles-fill.spec.ts`. Everything else in your Partition and HOLDS is unchanged.
