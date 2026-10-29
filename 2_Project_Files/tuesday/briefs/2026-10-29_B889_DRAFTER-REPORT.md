STARTABLE: YES (main bdb9c170c5f6ac14cd2073e703bd719159f286a1, one open PR #138 on two files outside both paths, ports 9760-9769 free, no b889 branch, jest lock queue empty at 11:39; lands BEFORE B890)

# B889 drafter report (kit for Datasec/NexusAI-M54, NexusAI RD-899, lane N1)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B889_SEAT-M54_nexusai-rd899-write-probe-cell.md` (113 lines; 9 four-underscore lines = eight Stamp slots plus the last line; 0 `@X@` tokens; 0 non-ASCII bytes; no person's name). Model Sonnet `claude-sonnet-5-5`, routing row C2 (line 92), gate G2 tier 2 round 1 of 2 with the full plain verify.

## BLUF
- One new cell J (a probe write that throws a code: resolver and constructor read the directory as unusable with that code, and the probe descriptor is closed exactly once) in the existing rd891 file, plus a one-word widening of cell G (`'ENOSPC'` added to its code array). Red-first: G green under GM6 before the widening, red after; J green at main, red under GM11 and GX2. Counts 5223 to 5224, suites 310, regenerated once by the project's rule. No product byte.
- Measured at main: rd891 test blob `0e54575e` (590 lines, 11 jest tests), `backend/jsonStorage.js` `bba3742b` (probe lines 402-418, write at 407, close at 409, unlink catch 414-416), counts blob `38c0ae66` (5223 / 310), 310 test files by the trees API. PR #138 (`static/js/index.js`, `__tests__/fixtures/rd200-js-brand-debt.json`) shares nothing; the MAIN-MOVED rule is written into the kit.

## D (decisions I made in the kit)
- D-1: widen G with ENOSPC rather than reword its title (only the widening reddens GM6; the ticket allows either). This is the one deviation from "additions only": exactly two removed lines (G's FAIL comment word on line 419 and its array on line 429), stated as Done (b).
- D-2: J loops `['ENOSPC', 'EIO']` inside its one `test(`; the close count reuses cell I's descriptor-reuse rule; the write spy is local, throws only on a recorded probe descriptor and forgets it at its close (the temp-file writer near line 495 also calls `writeSync`).
- D-3: J is a new `describe` appended at the end of the file plus one header line; `isWritable` not driven (B865-5), mode not pinned (B865-3), file removal after a failed write not asserted (D8).
- D-4: a predicted 12-test by 15-mutant matrix is in the kit and marked as prediction; the seat replaces it with received figures.

## Q (each with its default, all taken in the kit)
- Q-1: widen G by ENOSPC, or reword the title? Default: widen.
- Q-2: J one code or a loop? Default: loop ENOSPC and EIO inside the one test (count stays +1).
- Q-3: allow the two removed lines in G, given B855 was additions only? Default: yes, exactly those two.
- Q-4: ports 9760-9769, pane `Datasec/NexusAI-M54` (no kit names M54 or M55; live panes: wednesday, fleet-monitor, HPSM-POC-H51, NexusAI-G197).
- Q-5: gate tier 2 round 1 of 2 plus the full verify. Default: taken.
- Q-6: order: this lane lands first and owns the counts file; B890 follows (it needs the counts file only if it adds a cell).

## Corrections to the sweep (section 3, N1)
- None to paths or counts: 590 lines, 11 tests, counts 5223 / 310 and `_updated` 2026-10-27T16:10:11.756Z, probe lines 402-418, all confirmed at `bdb9c170`. Sweep says "the ticket reads it as 11 cells"; it is 11 jest tests (8 `test(` plus a 3-row `test.each`). Cell G is at lines 418-492 (array at 429), H 494, I 551.

## Unmeasured
Every red/green (nothing was run); whether `openSync` `mock.results` plus a local `writeSync` spy carry what J needs; the constructor's warning code text for ENOSPC and EIO; each mutant on Linux node 24; CodeQL on the new head; the Jira quoted-phrase search also returns RD-892 (not read by me, kit tells the seat to read it); text searches on the board are fuzzy (218 hits on `write-test`).
