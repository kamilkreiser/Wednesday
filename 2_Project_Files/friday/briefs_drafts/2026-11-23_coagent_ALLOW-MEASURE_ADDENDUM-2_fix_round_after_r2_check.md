This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-23_coagent_ALLOW-MEASURE_brief.md`. Seat ALLOW-MEASURE only.

# ALLOW-MEASURE ADDENDUM 2: the second check says NO GO at `379ceaaa54aeac59ea4cb5d24f074ef336a1e9eb` for two Majors; a fix round of words and one file removal; NO model run

**Read the verdict WHOLE first:** `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_ALLOW_MEASURE_r2_verdict.md` (204 lines; READ-ONLY; its scripts and outputs are in `m1_review/gate_allow_measure_r2_tests/`). Friday has read it whole. What it CONFIRMED stands and is not to be touched: M8 (its own separate run agrees: a dialog for both calls in the auto mode, each call waits, the reason shown for Bash and not for Write), M10, the M1-fresh-ctl correction, the re-redaction (14 files changed only by the two new rules), the run count (17 of 20), and every notes-round item.

**Two things Friday withdraws by name, because you were right and the check says so:**
- ADDENDUM 1's "the command line is in 1 and 2 frames": WITHDRAWN. Your count, 2 and 4, is right (the check's own re-count); the first verdict miscounted and Friday copied it. Your text stays.
- ADDENDUM 1's proposed evidence for "the sandbox was off" (0 lines containing "sandbox" in the debug logs): WITHDRAWN. It cannot tell on from off, as you showed. Your replacement evidence stays.

## RULED BY FRIDAY: the fix list (CLOSED; anything else you think needs changing is a `STOP Q1`, not an edit)

**F-A (Major): the compiled file.** `spikes/U-B1-hook-allow-silent/__pycache__/redact.cpython-314.pyc` was added in `379ceaa` and holds the plain path of its source file.
1. Take the `__pycache__` folder out of the branch with a new commit (`git rm --cached` plus MOVING the folder into your scratch folder `coagent/worktrees/tools/tmp/am/_side_effects/`; nothing is deleted from disk; if the move crosses a filesystem, copy, compare, and leave the original where it is, saying so: do not repeat the socket slip).
2. Keep Python from writing it again in this folder: run your scripts with `python3 -B`, and add `__pycache__/` to a `.gitignore` INSIDE the spike folder (not the repository's root file: that is outside your owned paths).
3. NO history rewrite and no force-push: `379ceaa` keeps the file. The repository is private. Add ONE line to your existing BACKLOG entry or a new one saying that commit `379ceaa` of this branch holds a compiled file with a workspace path, to be covered by the sweep before any publication. (The check notes that main already carries plain paths of the same kind in 113 files; do not touch those.)
4. Widen your names scan so this cannot recur: every COMMITTED file of the spike folder read as BYTES, binaries included, with a planted binary file as its positive control (the check's `qa2_scan.py` shows one way; write your own or adapt it, and say which). Print its output in STATUS.

**F-B (Major): M9 says MEASURED for what the captures do not show.** The check's evidence, which Friday accepts: the record you read as "review context sent" also follows the Bash call in `raw/M1-fresh-ctl` and `raw/M8-fresh-ctl`, whose debug logs say the classifier was SKIPPED; the control's 331 ms is shorter than those skipped calls; no positive review line exists in M9-fresh-ctl's debug log; and in the hook case the other record is on the Bash message too.
1. In RESULT.md's two M9 rows: "Reviewed, then allowed" and "the hook decided before the reviewer" become REASONED (from the permission-modes page's decision order plus the missing "Skipping" line), and are worded as such. State in the rows: the context record also follows skipped Bash calls and is absent only under a hook allow; the request record is on the hook case's message too. Keep MEASURED only for what a capture shows: the debug lines, the decision times, the record counts, no dialog, the file created.
2. R9, BACKLOG entry 5 and `docs/M0-OUTCOMES.md` reworded to match. The sentence Friday wants to be true everywhere this result is stated: "M9 shows our allow decides Claude Code's local permission step in the auto mode; whether it outranks the server-side reviewer is unmeasured, for a reviewer that approves as for one that would refuse." Remove "the reviewer approved it in the control" wherever it stands as a fact.
3. Your UNVERIFIED list: item 1 becomes that sentence's second half.
4. Commit `review_map.py` (the program that made every committed `review_map.txt`) beside `collect.sh`, after your scan has read it (N-2).

**F-C (Minor):** every remaining sentence that says or implies no review happened in the auto mode says "no LOCAL classifier request" instead, and the "NOT run" lines point at M9 and its limit: RESULT "facts met on the way"; M0-OUTCOMES "(it sent no request in these runs)" and "Whether a hook allow beats a classifier review or deny: NOT run"; BACKLOG entry 5's title and its "The two calls tried skipped the classifier".

**F-D (Minor):** the builtin-modules line says what the excerpts show: 4 to 6 builtin plugin modules per session (the debug line "Registered 0 hooks from N plugins"), the same N within each case and control pair. Count them yourself from the committed excerpts and give the table of N per run in STATUS.

**Notes, all four to be done:** N-1 (the raw file count in RESULT's redaction line: the number at your new head, counted); N-3 (cases.md: under the sandbox the probe's own `ls` was refused; the mode bits come from the runner's `tty_record.txt`); N-4 (R10 and the M0-OUTCOMES M10 line: "closes that one route; other routes were not tried"). N-5 is NOT to be done.

## Rules of this round
- **NO model run.** Your ceiling of 20 stands unused beyond the 17; nothing in this list needs a run. If you believe one does, that is `STOP Q1`.
- Owned paths as before: the spike folder and pure appends to `BACKLOG.md` and `docs/M0-OUTCOMES.md` against main (the check's prefix test: the main file is a byte-for-byte prefix of yours; keep it so; rewording your OWN appended lines is fine).
- For every changed sentence give OLD and NEW in STATUS, as you did for ADDENDUM 1.
- Then `git fetch origin`; if `origin/main` has moved (another lane, `w-gate-test`, may merge before you and appends to the same two documents), merge it INTO your branch (never rebase), keep both sides' lines, and say so.
- Checks to print in STATUS at the new head: the name list against `379ceaa` and against main; product diff 0 bytes; the byte scan with its control; `redact.py selftest`; the meaning check unchanged; settings checksums unchanged (no run was made, so say that instead of a sitting).
- Last two lines of STATUS: the full head sha, then `READY FOR QA ALLOW-MEASURE r3` (or `STOP Q1`). ONE short check of this round follows; this is the lane's third check and Friday will not order a fourth without the owner.

After ANY context compaction, re-read the brief, both addenda and your STATUS whole before writing anything more.
