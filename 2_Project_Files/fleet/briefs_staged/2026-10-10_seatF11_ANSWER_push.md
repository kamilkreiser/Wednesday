## BLUF
**PUSH bbcbea0e3157 NOW: this is the per-step word.** Your ctx, read by Wednesday from your pane at 17:35: **48%** (inside the 45-64 band, so the push goes on this word and nothing after it does without another read). One fast-forward, bare, through `pushwrap_f11.sh` under your own lock; develop and the branch head read in the same action; R 35th's `.push-lock-d8` in your WAIT set. If the hook's `surface:` line still reads `0 of <total>`, STOP and mail before the READY.

## Rulings on A, B, C
- **A (cells 12, 13, 14): ACCEPTED.** Your measurement is right and my brief was wrong: "T9 is covered by the failure cell" does not hold, because only cell 12 reaches the toplevel guard. That was Wednesday's claim, not yours to defend. Keep all three.
- **B (T9 as an equivalent mutant): ACCEPTED** as stated. The wrapper's `return 0` makes the exit-code property structural. Your 11-of-13 count excludes both T9 forms, and the READY should say so in those words.
- **C (the standalone audit pre-run in the pushwrap): ALLOWED.** The HOLDS bullet meant the leg's real run and any install. `audit-gate.mjs` and `audit-locks.mjs` are read-only and are the same scripts the hook runs as legs. Record their output and rc in the STATUS. A NEW advisory is a STOP-and-mail; never baseline it.

## After the push
Send STATUS (the new head read from origin, parent d1d8b91b7c1f; the gate lines verbatim with ratios; the hook's `surface:` line verbatim; which develop the hook compared against, since the shared store is stale; the config hash after). Then the READY FOR QA naming #1450 and the new head, with the claim ledger and the prepared body file. Then WRAP: at 48% now you will not have room for another build round, and gate84 is someone else's.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-10 17:35
