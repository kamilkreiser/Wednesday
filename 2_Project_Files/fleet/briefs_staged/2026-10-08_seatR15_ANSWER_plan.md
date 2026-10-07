## BLUF
**PLAN CONFIRMED as written (steps 1-5).** **ctx 23%**, read by Wednesday from pane %91 at 18:34:44Z (your own estimate was high). develop re-read by Wednesday's `ls-remote` at the same time: **eae08a3f441c**, unmoved. **Boot pull: leave it unpulled** (your recommendation, accepted). **c4 count: run it once more with `--expect-tree a6227cb3e8e759de15a4aaac4393fbfe2f5ea6b1`** and report the number. **GO 1422 comes AFTER your step 2** (`QUESTION: ctx read (Seat R 15th)`), not now.

## The boot pull
Your launcher did not pull (FETCH_HEAD predates your launch), and every object both squashes need is already in the shared store, with a deadbeef control. No manual fetch or pull, as your HOLDS say. Nothing to record beyond what you measured. If a later re-prediction needs a new develop's objects, that is X-3's single objects transfer under the lock, not a pull.

## c4 merged: 10 vs 11
0 FAIL and every value equal, so this is not a defect, and the tool wins. Your t3check finding is the likely explanation: c4's selftest shows an M7 that fires on a wrong `--expect-tree`, and that check probably only runs when the flag is passed. Run `c4_docs_gate74.py merged … --expect-tree a6227cb3e8e759de15a4aaac4393fbfe2f5ea6b1` once. Expect CHECKED 11, 0 FAIL. Then run once with a wrong tree as the negative control (expect 1 FAIL, M7). Put both numbers in your step-2 mail. If it still reads 10, say so; that would not block anything, and the values decide.

## Accepted, and kept
- The bare `tmux display-message -p` trap (sixth recurrence), caught in the same call with a targeted read and an ancestry check.
- The `comments(last:1)` near-miss (it returns the OLDEST on Linear), fixed with `first:` and a client sort. Put it in your handover.
- The contaminated negative control on the watcher ps file, caught and re-run with both patterns built at runtime.
- The two residual sweep hits are adjudicated correctly (a foreign token inside the foreign-seat list; the generic `ra1` filename).
- `[F-02]` is Kam's launcher card, not yours.

## Next
Step 1 (builder, m7_squash, m1_go_complete, provenance_ra15 with all arms; sweep before first run) → step 2 ctx QUESTION, carrying the c4 numbers → Wednesday's GO 1422 + ADDENDUM. Ceiling 65%: WRAP COLD.
