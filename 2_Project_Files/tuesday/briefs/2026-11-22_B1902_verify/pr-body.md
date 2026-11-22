## What changes

Tests only. Nothing is deployed and no product byte changes. One file: `web/src/screens/QuoteScreen.autosave.test.tsx` (+32 -0), two cells added at the end of the describe `autosave: the minimum gap between saves (MPSCALC-314)`.

**MPSCALC-429.**
- **G15**: an explicit save made 5 seconds into a gap starts a gap of its own, so the next autosave waits until 10 seconds after that save (no third request one millisecond before, exactly one at that time).
- **G16**: a second save request restarts the running gap timer instead of starting another (the timer count stays 1 through the new gap and is 0 when it ends).

## Who decides

The ticket says "no product byte changes and no word of the product owner is needed". The design choices (where the cells sit, their names, one commit) are the coordinator's, not the product owner's.

## Checked

Cells in the file 30 before, 32 after; the whole web run 1734 before, 1736 after, 0 failed (149 files). Each cell is red under the one-line change that removes its behaviour and green on the current code: an explicit save that arms no gap turns G15 and G16 red (base: 30 of 30 stay green); a re-arm that does not clear the running timer turns G15, G16 and the existing G5 red (at base only G5 is red). `eslint .`, `tsc -b` and the file alone pass. The diff equals the frozen edit byte for byte; one path changed.

## Not tested

Hosted CI and CodeQL (they decide on this pull request). Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
