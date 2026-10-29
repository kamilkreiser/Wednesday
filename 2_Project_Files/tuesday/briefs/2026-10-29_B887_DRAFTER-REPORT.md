# B887 drafter report (row C8, read-only, 2026-10-29 11:34-11:45 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B887_SEAT-J31_composer-pcomp108-year-underscore-rows.md` (115 lines, 9 four-underscore lines, 0 non-ASCII). Shape cloned from B857 (read whole) with the B878 ADDENDUM-1 project lock built into the copy list (`.tools/b878/scripts/heavy.sh` already carries it).

## Re-derived at main c63c38670187a98114aadee230dcf2a77bbb51aa (gh api contents/commits/compare, GET only)
- Test file blob `27ebb866e38591f3e4118eb05ac4792a037e35ab`, 279 lines, 18 `it(` lines (37 rows), 0 non-ASCII/CR/tab. `REFUSED_UNDERSCORE_YEAR` line 30, its loop lines 274-278, describe line 265-279, helper `expectDueDateRefused` lines 76-85. `app.ts` blob `2c5d5ad1...` (DATE line 105, `isStorableDate` 113-126) unchanged. Tree `6d1bda30...`.
- `compare/bdcfde7b...c63c3867` = one file, `packages/db/test/b778...`: apps/api group unchanged since PR #100 (81 files / 1529 tests is the B857 builder's count, relayed).
- Open PRs #95, #91, #86, #85: 0 exact-path, 0 app.ts hits (#95 and #85 hit the `apps/api/test/` prefix only). `b887*` and `b888*` refs: 0. Ports 9730-9739: no listener. PCOMP-108: Backlog, 0 comments.

## Q-questions for the stamp
- Q1 (round count): fresh round 1 of 2 on this PR; later residue PRs fresh unless a ruling closes the class; class (a) closed per C-109. Kit is written to the sweep's CC-A default (a), pending the card. Stamp must confirm.
- Q2 (placement): the kit puts the constant after line 30 and the new loop INSIDE the existing last describe (after line 278), not a new describe. Then the describe title at line 265, which the PR #100 gate called an overclaim (B864-1), becomes backed by four places without editing it. Alternative is a new describe at EOF as in B857.
- Q3 (lock livelock): the `ps` gate in `heavy.sh` greps for `Security Composer` plus `docker run`/`vitest`; a sibling B888 waiter's own command line could be counted by B887 and vice versa. Kit makes the seat print what the gate counts while a sibling only waits, and STOP if two waiters block each other. Tuesday may want the same line in the B888 kit.
- Q4 (tier/hard stop): G2 tier 2 kept; hard stop suggested at 4 h (not 3.5) for the shared lock.

## Corrections to the sweep
- Load: sweep said 4.98 at 11:32, "start when load1 under 7". Now 7.11 / 8.73 (11:36-11:39), so the seat will wait.
- Evidence path was not given: it is `1_Project_Definition/Briefs/2026-10-28_B864_evidence/runs/` (`c2-mutant-table.md`, `c2c-ky-route-answers.txt`), confirmed to exist.
- The ticket and gate state route answers the sweep omits: YP1 value answers 200 and stores `0027-01-01`; YP2 and YP3 values answer 500 (red as a thrown `sent()` contract violation, a kill only by the coordinator's C-108 reading, not a ruling). Kit carries this.
- Port block 9730-9739 was named in B731 (MPS, closed seat) as reserved; B706/B733/B778/B835 only mention the digits. No live claim.
- Line anchors, sha, paths, 279 lines, 37 rows: all agree with the sweep. No wrong path found.

## Unmeasured
- No vitest, container, image or mutant run. Predictions for the `b` spellings and combined edits (YP12, YP13, YP23, YP123, YP34) are reading-only.
- Gate row `KWYnD` `(\D\d{3})` is relayed as 0 red on 37 rows, which arithmetic contradicts (a `\D` first place refuses every digit-led year). Kit makes it a report-only census item, not a STOP; likely a mis-swap in the gate's table.
- Whether two Composer waiters block each other on the `ps` gate; apps/api baseline 1529 re-count; B888 kit does not exist yet (no B888 file seen), so sibling details are from the sweep.
- Pane list and loads move; Tuesday re-reads at launch.
