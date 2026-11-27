# Proposal 4: doctor checks that the pack is fresh and the handover is one block

TARGET: `2_Project_Files/doctor.sh`
INSERT: the whole of `doctor_check_snippet.sh`, after the "Rules index + card current" block (the `fi` that closes the block starting `RC="$PROJECT_DIR/2_Project_Files/tools/rules_card.py"`, about line 683) and before "Weekly consolidation not lapsed".

## Reason

The launcher builds the pack in its path; doctor is the backstop, in the same shape as the two checks above the insertion point (`boot_digest.py --check`, `rules_card.py --check`). It uses doctor's own `ok` and `warn`. The seat is the one `handover.sh --where` resolves from the tree, not doctor's `_DOC_AGENT` (which defaults to wednesday on a Tuesday tree when `WED_AGENT` is unset, and would have made a Tuesday machine check the wrong seat's files; corrected in round 2). Two checks:

- `wake_pack.py --seat <seat> --check`: warns when the pack is missing a source, older than one, built on an earlier date, different from a rebuild, or over budget.
- `handover.sh check`: warns when `STATE-<seat>.md` is not one tool-written block (the header carries the block's sha256, so a block appended by hand is seen).

A seat counts as "on the pack" once its state file exists (the cut-over's first step). From then on a MISSING pack is a warning too (round 3, the checker's M3: a build that has never succeeded must have a backstop). A seat with no state file and no pack is skipped silently, so Tuesday's and Friday's doctor output does not change. The snippet never discards stderr (m7): if `handover.sh --where` refuses, doctor prints a warning with the refusal and says the two checks were not run.

Known behaviour, stated so it is not read as a fault: the pack is rebuilt only at launch. Doctor run by hand later in a session will truthfully say the pack is older than the ledger or the state file. That is a statement about the file, not about the running seat.

Tested in `tests/run.sh --groups D` (D01 to D07; D05 is a TUESDAY tree that holds the Wednesday seat's state file and must print nothing) with doctor's `ok`/`warn` stubbed; doctor itself was not run with the snippet in it.

Related: proposal 7 retargets doctor's own 2026-09-18 warning on `NEXT-PICKUP.md`.

ROLLBACK: delete the inserted block (`git revert` of the commit). Doctor is read-only; nothing else depends on these lines.
