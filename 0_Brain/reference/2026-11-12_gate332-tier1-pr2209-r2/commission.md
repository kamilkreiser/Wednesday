# Gate 332, TIER 1 (Opus; routing v1.0 tier-1 row: an AUTH product change — the breached-password check used by register, reset and change-password). PR 2209 (KS-2021) ROUND 2 of 2 under the cap (round 1 = gate 331, GO WITH NOTES at 2db221d43ad8, Minor fail-open -> fix round). Seat R 108th's fix round. Commissioned 2026-11-12 ~16:55 AEDT by the 16:49 Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate331-tier1-pr2209/commission.md`. READ gate 331's `verdict.md` (same parent folder) WHOLE first: its corpus, its mutants, its G331-2209-N findings. This round re-measures the same questions on the new head; do not re-derive what is unchanged, prove it is unchanged.

Pins (Wednesday's `git ls-remote origin` 16:54:23 AEDT; RE-READ at start and end, and say if either moved): develop cea1cdc2b07db6516ff4d9594472666e764a6a6b; refs/pull/2209/head 2eca13ad7e8cb65d190f660b3b289d36f4d5475c (its parent is round 1's head 2db221d43ad8b06a58a6c890c75758b94434ae56; the PR is cut on develop 581296f039b4, and develop has since moved by PR 2203 + PR 2206, 3 files, which the seat says touch neither PR file — verify). Merge-tree onto develop with each side's own merge-base, plus a control that develop's lines survive.

READY (read whole; reproduce, do not trust): `ready_r108_ks2021_r2_mail.txt` in THIS folder.

What the round claims (from the READY, unverified by Wednesday): password.ts head line 178 `if (hashSuffix === suffix && Number(countText) > 0) return true;` becomes `if (hashSuffix === suffix && countText?.trim() !== '0') return true;` — fail-CLOSED: a malformed count for the user's own suffix REFUSES (as at develop), only an exact 0 is skipped. New cells R3 (red at 2db221d43ad8, 5 failed) and C4 (kills mutant M3). Whole services/auth suite 1850/1850 at head. PR body updated: the behaviour-change paragraph replaced, literal NO-PAIR present, the fetch-failure path stated as UNCHANGED (fails open at develop).

Questions:
1. **The fail-closed shape:** on gate 331's corpus (`SUFFIX:`, `SUFFIX:abc`, `SUFFIX: 3`, `SUFFIX:3\r`, `SUFFIX`, `SUFFIX:0`, `SUFFIX: 0 `, `SUFFIX:00`, `SUFFIX:0\r`, real counts >= 1, other suffixes, case variants) — what does the head return for each, against develop and round 1? Is the ONLY behaviour change versus develop the padding row (exact count 0 for the own suffix) no longer refusing? Name every input where head differs from develop. Is `00` / `0.0` / `-0` handled as the author intends, and does the PR body say so?
2. **Cells:** R3 red at 2db221d43ad8 and green at head; C4 kills M3; add your own mutants (drop `?.`, drop `.trim()`, `=== '0'` inverted, `!= 0` numeric) and report survivors.
3. **Optional chain:** confirm a row with no colon cannot throw into the catch (which allows) — measure it.
4. **No other change:** diff 2db221d43ad8..2eca13ad7e8c is exactly the two files the READY names; nothing in callers (routes/auth.ts register/reset, routes/users.ts change-password) moved.
5. **Suite and controls:** reproduce the whole services/auth vitest suite at head (or the declared files + password-service tests if load forbids; say which), red-first by reverting password.ts only, and a planted control that must fail.
6. **PR body:** tier-1 statement, the new behaviour stated truly, Refs only, no closing word, NO-PAIR present; gate 331's G331-2209-N items: which are closed by this round, which carried.
7. **Census:** open PRs touching the two paths (with a control).

Cap: this is round 2 of 2. If NO GO: say which instance is closed and which residue remains, as a ticketable list — no round 3 without Kam's word.

Spark: the test-digest STANDARD (`2_Project_Files/local-model/digest/digest.py`) on any long log, raw logs kept. NOTE the known digest bug G331-2209-5 (an rc-1-all-green run reads PASS): read the raw rc yourself beside any digest. Spark shadow review: run `2_Project_Files/local-model/gate/spark_gate.sh` / `spark_review.py` as a SHADOW if the tunnel is UP (the Spark now serves Nemotron-3.5-Super-VL); its output is a calibration row only, never the verdict.

OUTPUT: `verdict.md` in THIS folder. First line: 'PR 2209: GO / GO WITH NOTES / NO GO (at head 2eca13ad7e8c; tier 1; round 2 of 2)'. Findings G332-2209-N, graded (Major / Minor / Note / Info). NOT TESTED section. If your Write is refused, return the text in full.

Constraints: exactly gate 331's. Read-only on the project checkout and on every worktree (clone into `scratch/` in THIS folder for any write verb; installs only there, `--ignore-scripts`). Every npm/npx/vitest/tsc invocation names its directory explicitly and never runs from the WEDNESDAY working directory. No push, no comment, no ticket write, no merge, no mail. Never `cd`. No call to the real HIBP API from a test. Load: whole-suite runs at load1 < 8. If DevMASTER drops, wait, re-read what you wrote, then resume.
