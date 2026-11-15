# Drafter notes: Seat K 25th merge brief (2026-11-15 21:5x to 22:08 AEDT)

Output: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatK25_merge.md` (49,840 bytes). Everything scratch is in `_work/` of this folder (clone `c25`, scripts `heads25.py trees25.py stack25.py gates25.py linear25.py shift25.py assemble.py`, shifted kit `kit25/`, scratch `scratch/`, worktrees `wt_dev wt_head wt_merged`). Nothing was written under `!CODING`; no `cd`, no `rm`; Linear and GitHub read-only.

## What was measured (each at source)
- develop `6af62b9ac556` = PR 2234's squash (API branches + pulls/2234 + own clone), tree `2608a2bbd10c` = the GO's expected tree. 58 queue rows (K 24th's 59 minus 2234): all open, heads equal to `queue_k24.json` (58/58, also equal to fetched `refs/pull/N/head`), the order equals K 24th's FINAL 'Remaining order (58 rows)'.
- Trees on the live develop: 58/58 rc 0 same tree both orders; 58/58 planted controls rc 1 both orders; unrelated control rc 0; 10/10 stacked pairs; the same 7 shared-path rows as K 24th (numbers one lower).
- Gate scan: 58/58 by head sha, 46/58 by own-PR GO line, 0 NO GO (same 12 multi-PR verdicts as K 24th's list).
- Linear: 60 ids (59 queue + KS-1914) all In Progress; KS-2125 has no comments.
- Re-key `k24 -> k25`: set 38 / 95 / 33 = 166 (K 24th's was 150), counts per step in the brief, sed cross-check 166/166, syntax 0 bad, matcher 761/761, no-P1 756/761 (5 MISMATCH), bare-rule 754/755 with 8 duplicates, own-seat mutant 761/762. UNION-AUTO arms on the shifted tool 11 PASS 0 FAIL, two mutants caught.
- Row 1 (PR 2237) docs-fragments check, run by the drafter on scratch sparse worktrees: develop 252 / head 246 / develop+PR 253 new each, rc 0 on all, planted unclosed div rc 1, restore sha-equal.

## Findings Wednesday should know
1. `8967de8k245` becomes `8967de8k255` (5 files); NEW trap class found: hyphen-glued `seat-k24` (86 occurrences in 32 files, git identities and hash seeds) and `k24-` (15 files); `K24PLANT` (3). All declared, none repaired.
2. K 24th's brief had no Python-leg need for this queue: no queued PR touches a `.py` or `systemTest/schemathesis` path, so the pytest model is carried by reference only. Its loop-variable bug is in `suite_chain_2234_k24.sh` and `legs_2234_k24.sh` (`lw()` on `i`); fixed form in `repin_2234_k24.sh` (`k`).
3. K 24th's HANDOVER FINAL heading says 'written ~10:58Z = 21:58' but the file mtime is 21:53:12 (an estimate); its wrap mail and history entry exist (21:54).
4. R 120th's staged answer grants an overlap on `certifications.ts` (PR 2160, row 30) and carries a Kam 21:03:48 KS-1699 line: asked in RULINGS 4 and 6.
5. GitHub `mergeable_state` is `unstable` on all 58 (K 24th's brief had `unknown`).

## Not done / judgement calls
- The commission asked for 'the 59-row table ... by section': read lines 77 to 137 of K 24th's brief and rebuilt the table from `queue_k24.json` plus live data; the Linear column moved from the table to PROVENANCE (size budget); the files +/- column dropped (equal to K 24th's, stated in BLUF 3).
- The brief is 49.8 KB, just under the 50 KB line; trimming was done on K 24th's carried prose, not on measurements.
- Wednesday's own ls-remote (the commission's statement of develop) was not re-run (the drafter has no deploy key in its shell); the pins are the API and an HTTPS fetch.

## UNMEASURED
- Any suite, install, tsc, eslint, vitest, pytest or ruff run (only the docs-fragments check, matcher self-tests, UNION-AUTO arms and mutants were run).
- The live floor (B 182nd, R 120th, T 25th, Q 1st taken from the commission), B 182nd's matcher and REC, decisions.json and Kam's cards.
- Running any re-keyed tool beyond syntax / matcher / arms; the cost of the 166-file re-key; row 3 onward forecasts; the by-name vitest cell for PR 2139 on today's develop.
- Whether K 24th's FINAL block changes after Wednesday's re-stamp; check-run counts (403, not retried); the pre-push hook; PR 2237's expected tree (the drafter's own merge-tree result only).
