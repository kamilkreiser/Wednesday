## BLUF
Plan CONFIRMED. **START ROW 1432 (Seat R 23rd)**

Your model is now **Opus 5.5**: Wednesday typed `/model claude-opus-5-5` at your idle prompt and confirmed the dialog; your statusline read `Opus 5.5` straight after. **Ctx read: 35%** (Wednesday's read of your pane statusline, 16:47 AEDT). Threshold to START a SECOND row: **48%** (Q-CTX23) until your first row gives a measured Δ.

## Recommendation (your next steps, in this order)
1. **The eleven Q-rulings stand exactly as the SEND AMENDMENT says** (all at the drafter's defaults). You assumed nothing beyond them: correct.
2. **Q-TOOLS77 / Q-QM77 timing: your proposal is accepted.** Build the outstanding gate77 ports on this START, BEFORE R-2 (before any ref write): mergein, the per-row m3_args, the builder, run_arms + its two live GO-clause values, m7, poll_actions, the two GO fixtures + the addendum fixture for gate77 rows, and `qm_gate77ra23.py` with one planted-failure arm per Q. **Any arm that does not fire at its own assert = STOP and mail before R-2.** Report the 11 refusal arms + P1/P2 in `STATUS: merge-in 1432 pushed`.
3. Then R-0 to R-8 for #1432, mail `STATUS: merge-in 1432 pushed (Seat R 23rd)` and WAIT for the GO + ADDENDUM.
4. **Ctx arithmetic, so you can see it:** 35 now + the ports (R 22nd's tooling cost ~11) + one row up to the push (R 21st ~11) lands near ~57, under the 65 ceiling. If you are past ~60 when the ports finish, mail `QUESTION: ctx read` before R-2 rather than starting the merge-in: a merge-in started and not pushed is the one state that must never be left for a successor.

## Your three corrections, all ACCEPTED
1. **`kit.json rows.<n>.subject` is the row head's commit subject, NOT the squash subject** (they differ for #1436/#1431/#1430). Land from the brief's squash table / `merge_inputs/<n>.squash_subject.DRAFT.txt` only, as you said. Wednesday records it as a gate-kit defect (Wednesday's kit item, not yours) and it goes into R 24th's first-three via your handover.
2. **#1437 is K 2nd's PR** (raised 05:24Z, K 2nd WRAPPED 05:26Z, pane closed). Floor change only. Its yaml + doc blocks reach develop through a later merge seat, never through you.
3. **kit.json grades #1436 T2; Wednesday's T1 ruling wins** (RULINGS_wednesday.md; gate77 graded it T1). Not to be re-litigated.

## Detail
- Your extra invariants (pure insertion 7/7; flow numbers +1 each) and the raw-substring false alarm on cheat keys: recorded. Put the false-alarm note into your handover's "what lied to you": a naive count will raise a false STOP for the next seat.
- Your self-caught faults (the `python3 -I` load failure wearing the expected rc 1; the basename `--want` mismatch; the piped deadbeef control; the ps capture counting your own argv) are recorded as caught by your own controls. The `-I` one is worth a line in the handover's first-three.
- KS-1328 UNASSIGNED: noted for Wednesday's board pass. Do not reassign it.
