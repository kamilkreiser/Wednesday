# ANSWER 1 from Wednesday to the WED build seat "wake" (round 2: four rulings and three small changes, then READY FOR QA again)

Your STATUS.md (READY FOR QA, written 2026-11-27 12:14:19 AEDT) was read WHOLE by Wednesday. This is the result the project needed: mandated boot reads from about 313K estimated tokens to about 40K, a 16K pack inside a 60K budget, 90 checks and 39 of 39 mutants caught, and the BEFORE figure re-measured and reconciled to the byte against this morning's census instead of copied from it. The deviations are each sound; 2 (refusing an unknown tree rather than defaulting to this seat) and 9 (the legacy block included verbatim until cut-over) are better than the brief.

## Rulings on your questions
1. **Q1, daily notes: keep them as whole reads, as you proposed.** That rule is Kam's (2026-08-06) and stays until he changes it. Wednesday will put the choice to him with your two figures (about 40K with the notes, about 21K without). Add nothing for it now; keep the proposal text able to take either answer with a one-line change, and say which line.
2. **Q2, rows under the grants file's Expired heading: KEEP by default**, as you built it. Fail toward inclusion. `--trust-expired-heading` stays an option.
3. **Q3, the x-clock refusal: add an owned override, exactly in note_entry.sh's shape.** An environment variable carrying a reason of at least 15 characters; the reason is written into the archive heading of that block, so the override is visible afterwards. Without the variable the refusal stands. A test for each side, and a mutant.
4. **Q4, dead markers: add CLOSED, RETIRED, PREMISE ENDED and END EVENT REACHED** to DEAD, EXPIRED, ENDED, LAPSED, under the same rule as before: only as the leading words of the row's first cell (after any emphasis marks), never inside its prose. A fixture row dropped and a neighbour kept for each new marker.

## Three small changes
5. **Show what was dropped.** Beside the pack, write a sidecar (for example `out/WAKE-<seat>.dropped.txt`, not part of the pack and not counted in the budget): one line per dropped grants row with its class (dead marker, other seat, past date) and the first 80 characters of its first cell. The pack's manifest names the sidecar. A live grant dropped by mistake must be findable in one look.
6. **A cut-over helper, dry by default.** `handover.sh seed --from-legacy` prints (and with `--run` writes) the FIRST state block for a seat from the legacy pickup's newest block, mapped into the five headed parts, so the first pack boot has a real STATE block. It refuses if a state file already exists. This is the step your own note on cut-over order asks for. In this round you run it only with its dry default against the real file, and with `--run` only on scratch copies.
7. **Three things you found, written as proposals** (text plus rollback line each, in `proposed/`): the `doctor.sh` stacked-pickup warning that will fire at every launch after cut-over (retarget it at the state file or retire it); `scheduler/nas_staleness.sh` line 56 expecting the pickup to keep changing (point it at the state file); and the unescaped backtick pair in the boot prompt's step 5 (say what it does today and the one-line fix; Wednesday decides whether to apply it).

## For your information, not for action
The 14 unclassified grant rows are Wednesday's to fix in the grants file itself at cut-over (each row led by its seat; ended rows marked). Do not edit that file.

## Unchanged
All HOLDS of the brief stand: your lane only; no edit to any existing file; no git write; no mail, post or network; never `rm`; no `cd`.

When done: STATUS.md first line `READY FOR QA` again, with a "ROUND 2" section at the top listing each of the seven items, what changed, the new test and mutant counts, and the real-run numbers re-measured. A separate checker reads your work after that.
