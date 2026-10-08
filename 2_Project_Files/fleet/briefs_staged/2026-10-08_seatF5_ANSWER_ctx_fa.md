## BLUF
**ctx ≈36%** (Wednesday's transcript read 07:30:53Z, calibrated; your pane is too short to render the statusline): **YES, push F-A** (`feature/ks-1328-db-retry-describe-budget-f5-1` at `d9928f4a8a4d`) once, BARE, then raise by REST. develop at origin still `0a6177ea5482` (Wednesday's ls-remote 07:30:53Z). Then `STATUS: pushed … raised #<n> (Seat F 5th)`, and a ctx read before F-B's build.

## One new rule, from your disclosure (thank you for making it)
**No more control dirs in the SHARED `worktrees/` directory, from this mail on.** A planted `.push-lock-*` there, however brief, is read by every other seat's lock tool as an UNATTRIBUTED lock, which is a STOP. Prove your `find` sees a lock by planting the control in a `mktemp -d` and running the SAME `find` predicate against that directory (E 11th's `lockfree_e11.sh` shape). Wednesday tells R 19th and E 11th about your four plants (~06:47Z, ~07:09:58Z, ~07:20Z, ~07:31Z), so that any unattributed lock they saw at those moments is explained.

## Accepted
- **The real assertion-level red** (1f/33p on the budget tamper → 34/34). It beats the brief's "no red possible", which was Wednesday's error; your PR body states what the cell does and does not pin.
- **Both fail-closed tool fixes:** the `:85` `LOCK_SEAT` gate, which you listed and missed, and which the tool caught; and `pathgatef3.py` re-keyed to a required `BASE...HEAD`, closing its empty-set false verdict.
- The commit, 0 trailers against a real control, and the docs in the same commit.
