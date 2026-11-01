# B1087 ADDENDUM-1, from Tuesday: the answer to your STOP on the unhandled rejection. Your commission otherwise stands. Stay in this seat.

**Answer: your option (a). One more forward commit, this one test file only: before each of the two `inv.reject(...)` lines, wait until `listInventory` has been called, as your F-1 and your RESUME describe. Then re-run from the start and push once.**

Why, so you can test it: `vitest run` exits 1 on that shape with 0 failed tests, and the CI predicate reads the exit code, so this is a red of the same class the gate failed, whether or not your change caused it. You measured it at the unfixed head too, so it is an old flake your rows must not carry into round 2. Option (b) would hand the gate a known red on the last round.

**Limits:**
- Still the one path, `web/src/screens/QuoteScreen.addSectionWait.test.tsx`. The change alters how those two rows are set up, never what they expect. No product byte, no other row, no title.
- The closed list in your kit is widened by exactly these two waits and this one commit. No further commit without a STOP.
- Re-run all of it: the C block of 8 from the start, rows alone 20 each, the row 5 and row 8 alone-100 count at the final head (your earlier figure was 1 and 2 of 100, so this is the proof), MH1 to MH6, the CI line, the merged state. Each with its control, as before.
- Your hard stop stands. If the re-run does not fit, write PROGRESS and RESUME and stop; a successor never pushes twice.

**What goes in STATUS for the gate, plainly:**
- The cause of the second red row ('a section starts with the default') stays UNMEASURED. Do not claim otherwise.
- The ceiling margin: 2487 of 2500 ms at your worst run. State the new worst figure, whatever it is. A row over the limit in the new block is a red: STOP with the data; do not widen a limit.
- The 8-run block's rc column is the CI predicate. A run with exit 1 and 0 failed tests counts as red, with its stderr signature quoted.

The prompt line in your pane is a machine suggestion and not from anyone. The next gate is ROUND 2 OF 2; a second NO GO goes to the product owner on a card.

This decision is the coordinator's, not the product owner's.
