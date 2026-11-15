# Notes: DRAFTER for Seat K 31st (Secuura/Blockchain-K, MERGE seat), 2026-11-16 03:1x to 03:3x AEDT

Output brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatK31_merge.md (lean delta of K 30th's stamped brief; blank STAMP; under 50 KB). Scratch: `_work/` in this folder (clone `c31`, scripts `*31.py`, outputs `scratch/*.out`, shifted kit `kit31/`, matcher copies `scratch/m_*.py`).

## What was measured (instrument in brackets)
- develop `c7b3c2abf08c983bed5129a3f2a81b1c3a1be4a9` (PR 2243's squash, parent `d041f1a54f8f` = PR 2242's squash, tree `fd12db7cd931`); re-read 03:29, unchanged [gh api branches/develop; clone origin/develop].
- Queue: 52 rows = PR 2244 + K 30th's FINAL order (52 of 52 equal); all heads equal expected head12 at 03:2x and again 03:29 (heads31.py); mergeable_state unknown 50 / unstable 2 at 03:1x, unstable 52 at 03:29.
- Merge trees on live develop, both orders: 52 of 52 rc 0 same tree; 52 of 52 own-hunk plants rc 1/1 (40-char sha asserted); per-file plants rows 1 to 10 and 37: 29 of 29 own 1/1, unrelated 0/0 (trees31.py, ctrl31.py, ctrl31b.py); 9 stacked pairs 9 of 9 clean (stack31.py). Row 1 (PR 2244) tree `ba9c32c714aef5b6469d225d25e09aba13dc0298`; merge-base `e659170439406810d368bdebf19dd39c08abeace` vs API base `6fdba4e013b3`.
- PR 2244 carries the template's DNM sentence (count 1; PR 2243 positive control 1). K 30th's table cell was blank. The brief says so and asks Wednesday to confirm.
- Re-key (shift31.py on K 30th's set, 340 files = 57/185/98, counted 03:20, 03:22, 03:23 equal and equal to its FINAL block): table P1 1/0/0, G1 33/166/93, G4 1/0/37, G5 158/343/268, G6 37/90/98, G7 328/1103/765, N 56/185/41; sed 340 of 340; syntax 0 bad; hazards 230; bare `30th` 1129 before, 68 after; a bare rule gives 7 duplicates (781/774) and 789/790.
- Neighbour collisions a `31st` creates: `K 131st`, `K 231st`, `K 1031st`, `K 2031st`, `K 310th` all ABSENT from OTHER_SEATS (so SIX entries incl. the predecessor `K 30th`, 781 -> 787); K 30th's `K 230th` case has no analogue. The classifier reads any other named seat OTHER even without an entry, so entries are self-test cases.
- Matcher: shipped copy 796/796 rc 0; no-P1 791/796 rc 1 (5 MISMATCH); own-seat mutant 796/797 rc 1; five-entry copy 795/795 and duplicate copy 797/797 pass silently.
- K 30th WRAPPED before my read of its record finished: FINAL block present (two rows merged, r 58.0, next row PR 2244), wrap mail record present, history entry present (K 30th heading count 1, K 31st 0, K 18th 1). df 2054 GiB; load 4 to 6.
- Overlap census over 70 open PRs: none shares a path with PR 2244; PR 649 is the only other open PR under wallet-connector; PR 2245 (Seat C 40th's KS-2189 + KS-2188 kyc build, head `616c57ba4e51`) is open, not a row, shares no path with any of the 52 rows.
- Linear: 53 of 53 queue ids In Progress; first ten rows' newest comment times are in the brief's PROVENANCE.

## Slips
- Three first calls refused by hooks before running (a `cd`, a bare `=====` word, a wrong tool name) plus one mistaken Edit call on a non-existent path (failed, wrote nothing).
- `sed -i.bak31` copies left beside my `*31.py` scripts in `_work/`; one brief backup moved to `_work/scratch/brief.bak31`. Nothing removed.
- The brief first came out at 58 KB and was trimmed to under 50 KB by compressing carried text (all measurements kept).
- zsh pipeline exit codes were read from `pipestatus`/separate runs after the hook advisories; the self-test results above were taken from standalone runs written to files.

## UNMEASURED
- No install, suite, tsc, eslint or vitest run for row 1; gate 369's and W 31st's figures are read, not re-run.
- No pane read (the live floor is the commission's). Whether gate 369's findings are filed (ids not read) and whether PR 2245's gate verdict exists.
- The complete-install nested `node_modules` count; mergeable beyond two reads; CI check runs; the pre-push hook.
- UNION-AUTO on a real merge; running any re-keyed tool beyond syntax and the matcher self-test.
- Whether authors push again to PR 2244 or any queue PR after 03:29.
