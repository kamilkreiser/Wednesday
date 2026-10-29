STARTABLE: YES (main bdb9c170c5f6ac14cd2073e703bd719159f286a1, one path, no open PR or live branch on it, ports 9770-9779 free, no b890 branch; heavy storm file: runs alone under the jest lock, FIFO behind B889 or a gate is a wait)

# B890 drafter report (kit for Datasec/NexusAI-M55, NexusAI RD-900, lane N2)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B890_SEAT-M55_nexusai-rd900-tamper-double-field.md` (110 lines; 9 four-underscore lines = eight Stamp slots plus the last line; 0 `@X@` tokens; 0 non-ASCII bytes; no person's name). Model Sonnet `claude-sonnet-5-5`, row C2, gate G2 tier 2 round 1 of 2 with the full plain verify.

## BLUF
- One test file, region 359-397 of `__tests__/rd407-concurrent-settings-writers.test.js` (blob `885e5cf1`, 686 lines), NO new cell, so no count moves (37 jest tests, pair 5223 / 310 untouched). The cell counts a refusal only when it carries the product's `STORE_UNREADABLE` code AND the same storm's sampler saw a torn store; red under GM6 (the ticket's double), GM6c (same text plus the forged code), GM5, GM3; green on the committed double. Red-first: the unedited cell is run under GM6 and GM6c (green, the finding) before any edit.
- If a cell is unavoidable: kit rule `CELL ADDED`, one regeneration on its own base, Tuesday lands B889 first and resolves the counts-only conflict by C-57 (new head, new gate). Default is to STOP and ask.

## D (decisions I made in the kit)
- D-1: the helper is NOT touched (see Corrections). D-2: agreement is per storm, summed over the four copies (the same sum the cell already computes). D-3: `thrown` stays printed, uncounted. D-4: mutants live in the helper's tamper branch (clone only, hash-restored), recipes re-derived from helper lines 49-64 and the gate's GM1-GM9 table. D-5: tamper controls T0-T3 on the new lines (T0 old cell stays green under GM6/GM6c; T1 code clause alone; T2 agreement alone under GM6c; T3 neither). D-6: 6 whole-file plus 16 isolated green runs, counters via a temporary stderr print that must be absent from the commit.

## Q (each with its default, all taken in the kit)
- Q-1: helper change, or use the `code` it already reports? Default: no helper byte (a new `fs` read there is a CodeQL-sensitive sink; the file carries the RD-873 alert history).
- Q-2: match message only, or code plus message plus agreement? Default: code plus message plus agreement.
- Q-3: a new cell allowed? Default: no; only under the `CELL ADDED` rule above.
- Q-4: ports 9770-9779, pane `Datasec/NexusAI-M55` (free at the read). Q-5: gate tier 2 round 1 of 2. Q-6: order: B889 lands first.

## Corrections to the sweep (section 3, N2) and the ticket
1. The cell is not "lines 363 to 396": the `describe` is 363, the `test(` 370, the FAIL comment 371-377, the loop 383-394, the `expect` 395-396, close 397-398; the constant `TORN_STORE_REFUSAL` is line 361.
2. The sweep lists the helper under YOURS and the ticket says "make the helper report a distinguishing field": the helper already reports it (`code: e.code || null`, helper line 88), and the product sets `STORE_UNREADABLE` at `backend/jsonStorage.js:3264`. The refusal text is built at 3247-3248 and 3262-3263.
3. Honest limit written into the kit: an agreed refusal needs `torn` above 0, and `torn` is already a term of `detected`, so the refusals term cannot flip the verdict alone; the verdict rests on the sampler.

## Unmeasured
Every red/green (nothing was run); whether `torn` is above 0 on the hosted Linux runner, node 24 (the old assertion passed there and could have been carried by a refusal; if the hosted `Build` reads this cell red, that is a finding, not a loosening); CodeQL on the new head; the raw `test(` line count (15 by the gate, 17 by my regex; jest's 37 titles decide).
