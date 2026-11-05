GO WITH NOTES

# QA GATE 196: Secuura/Blockchain KS-911 + KS-912 (tier 1, findings only)

Gate date: 2026-11-05. Subject hashes checked first and again at the end. They were unchanged both times:
- `Launch_Claude.command` = `4f519a6b631623221f64b0dfc61321c3dbf6378f463e9f60dcb8f42022cd42c2` (live)
- `Launch_Claude.seats.test.sh` = `b93b2c838e8766a8dc2b72e24d2f6fab21f9b912772e52328d43996414f18888`
- `Launch_Claude.command.pre-ks911` = `9609c8453da8d7743a4b3ed2a94db6b09bef588c29f83e57b16255963a0929f1`

## BLUF

The KS-911 scope (F1, F2) and the KS-912 scope (F3, F4, F6) are complete in the file that runs today, and I checked each one against the source with its own control. The suite passes 18/0 on the live launcher, with 8 launcher runs printed. I ran it once, under /bin/bash 3.2.57, in a fresh copy of the seat's sandbox. I rebuilt the shipped hash `932a2cc3…f55c` myself: I put the `.pre-ks911` TURN-END line back into `.pre-0914-keepalive`, and the result matched. As a control, the unmodified file does not match. The three later edits (keepalive, nofetch, model) do not touch the 23 KS-911 lines. The notes below are outside the tickets' named scope. None of them invalidates a claim.

## Findings

- **G196-F1 (Low, outside the named scope).** The redirect-ordering defect fixed by KS-911 F2 still exists elsewhere in the same launcher.
  - Line 91: `printf … > "$PREFLIGHT_LOG" 2>/dev/null || PREFLIGHT_LOG="/dev/null"` puts the redirect after the target. Measured under /bin/bash with a non-writable directory (chmod 555): it prints 1 line, `…/log: Permission denied`. The writable control prints nothing. Evidence: `work/l91/err_ro.txt` and `work/l91/err_ok.txt`.
  - Lines 95, 624 and 691 use the same `>> "$PREFLIGHT_LOG" 2>/dev/null` form. Line 691 arrived with the 10-27 model edit, after KS-911 had fixed this exact pattern. Those three lines are quiet in practice, because line 91 falls back to /dev/null.
  - KS-911 named only :292 and :295, so this does not break KS-911. It is a candidate for a follow-up ticket.
  - Location: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/Launch_Claude.command:91,95,624,691`.
- **G196-F2 (Info, test coverage).** The KS-911 regression text says "registry *directory* is unwritable". CASE 6 instead uses an existing read-only *file* in a writable directory.
  - The seat's reason holds: only the read-only file reaches both write sites, while an unwritable path reaches only the append.
  - The unwritable-path fixture is therefore not in the suite. I covered it outside the suite, and the live file prints 0 error lines where the old file printed 2 (table below).
  - Location: suite lines 246-272.
- **G196-F3 (Info, outside scope).** If the registry file is unreadable (for example chmod 000), `done < "$SEAT_FILE"` at live line 299 would print a shell error, because `-f` passes but the read fails. I found this by reading the code and did not run it. Neither ticket covers it.
- **G196-F4 (Info, not a KS-912 claim).** CASE 3 (a recycled pid) still checks only the count and the step text. It never checks that the entry left the file, which is the same gap F4 closed for CASE 2. KS-912 named only CASE 2.

Seat candidates, recorded as INFO and not as findings:
- **Orphan `sleep 300`: confirmed.** Suite line 222 spawns `sh -c 'sleep 300; :'`, and `cleanup` at line 40 kills only that wrapper, so its `sleep` child is left with ppid 1. My single run left pid 7165. I killed it by recorded pid (`run/orphan_before_kill.txt`).
- **The S2 TURN-END edit has no `.pre-` copy.** True. The rebuild makes up for it.
- **Boot-sync pull.** This is a step in the seat's own prompt, not something the script runs. It does not affect these tickets.
- **The seat ran the suite in place at the live project root.** Its own trap restored the preflight log. That is the seat's choice, not part of this scope.
- **Housekeeping.** My run copy at `run/ws/…/2_Project_Files/.git` is an embedded git directory inside the WEDNESDAY repo, so keep `run/` out of any `git add`. I deleted nothing (house rule).

## TESTED

| check | result | control |
|---|---|---|
| Subject hashes (start and end) | all 3 match | n/a |
| Shipped hash rebuild (`work/S2_rebuilt.txt`) | `932a2cc3…f55c`, 37,076 B | unmodified `.pre-0914-keepalive` = `9b301721…`, which does not match |
| `.pre-ks911` to rebuilt S2 | 23 changed lines | ticket says 23 |
| `.pre-ks911` to live diff, read by eye | KS-911 hunks intact at 244, 246-253, 300-307, 310, 380. The other hunks are only keepalive (130/135), nofetch (359-363/373), TURN-END (555) and model (653-708) | n/a |
| F1: "the test extracts here" / "SEAT REGISTRY — BEGIN" (case-insensitive) | live 0 / 0 | `.pre-ks911` 1 / 1 |
| F1: does the suite reference the sentinels? | 0 refs to `KS-907 SEAT REGISTRY` | 2 refs to `SECUURA_LAUNCH_DRY_RUN=1` (lines 10 and 69) |
| F2: live :307/:310 against pre :292/:295, read-only file | live 0 error lines / pre 2 ("Permission denied" ×2), rc 0 | writable file: both silent, and the live form still wrote `x\|y` and `pid\|z` |
| F2: unwritable path (parent is a file) | live 0 / pre 2 ("Not a directory" ×2) | `BASH_VERSION=3.2.57(1)-release` printed in every fixture (`work/f2/out_*`) |
| F3 | `LAUNCH_RUNS=0` at line 53, incremented inside `run_launcher` at line 65, printed at line 291. 8 call sites: 98, 133, 169, 199, 224, 238, 262, 277 | old label at the old line used `$((pass+fail))` (diff) |
| F4 | presence check at line 148 (`grep -q "^$LIVE_PID\|"`), absence check at line 181 (`! grep -q "^$DEAD_PID\|"`) | tamper `21a1ec04…` differs from rebuilt S2 in exactly one line, :307 becomes `: "$SEAT_KEPT"`. The dead entry therefore stays in the file and line 181 must FAIL, while the old count/pull cell (170) still passes. Seat output `suite_tamper_newsuite.out` shows exactly this (17/1), and the old suite shows 14/0 |
| F6 | `grep -qc`: suite 0 | `.pre-ks912` 1. The replacement at line 107 uses `grep -q … && echo YES \|\| echo NO` |
| Suite run (mine, once) | **18 passed / 0 failed, "after 8 launcher runs"**, rc 0 | `.git/config` md5 `f88c6ac4…` and preflight md5 `5686ebd3…` identical before and after (`run/md5_before.txt`, `run/md5_after.txt`) |

## NOT TESTED

- Red-proofs 1 and 2 (`.pre-ks911` + new suite = 17/1; tamper + new/old suite = 17/1 and 14/0). The brief allowed one suite run, so I checked these by reading the source and the tamper diff, plus the seat's `evidence/suite_*.out`.
- The `exec claude` line and the model edit's `SEAT_MODEL` allow-list. Both are outside this scope.
- Anything at the live project root, any real launch, and other projects' launcher copies.
- G196-F3 was found by reading only.

## HOW

- Linear: read-only GraphQL with `python3 -I` (`linear_read.py`). The key was read from `.env` and never printed. Output is in `tickets_ks911_ks912.json`. I read the scope, the 09-06 BUILT comments and the seat's comments `6eb48533` and `f2f4c4db`.
- Suite run:
  - I copied the seat's `work/sandbox/ws` to `run/ws` and overwrote its launcher and suite with fresh copies of the live files (hash-verified: `run/hashes_used.txt`).
  - I ran it with `env PATH=/bin:/usr/bin:… TMPDIR=run/tmp /bin/bash …/Launch_Claude.seats.test.sh`.
  - The sandbox has no `Extranet` sibling, so the KS-148 git pin did not run against any real repo.
  - Output is in `run/suite_live.out` and `.err`; the `.err` file holds only bash's "Terminated" job notices from cleanup.
- F2 fixtures: the exact lines were pulled with `sed -n` from both files and sourced under `/bin/bash` (`work/f2/`).
- Nothing under `!CODING/` was edited, moved or deleted. No board writes, no mail, no git write verbs.
