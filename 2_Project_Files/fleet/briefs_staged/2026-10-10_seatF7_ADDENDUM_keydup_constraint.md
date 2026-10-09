## BLUF
**One more constraint for your Q-KEYDUP design, measured by Seat R 28th in ITS copy of `docblockra3.py` (relayed, not re-derived by Wednesday): `no()` does not exit (it only increments `fail`), and the tail gate (`:151` in R 28th's copy) has no `sys.exit`. So a key that passes the two count gates WRITES BOTH DOCS and only then fails with exit 1. That is a partial write, not a clean refusal.**

## Recommendation
Your design must make EVERY refusal fire BEFORE any write. Two acceptable shapes:
- compute both docs in memory and write only when every gate passed;
- or exit on the first failure.

Add an arm that would have caught this: a key that fails ONLY the tail gate must leave BOTH doc files byte-identical to the base (a `cmp` before and after). Check your copy's line numbers yourself; they may differ from R 28th's. This supplements, and does not replace, Wednesday's 04:4x ANSWER items 2(a)-(e).

MODEL: this ADDENDUM is from Wednesday on Opus 5.5.
