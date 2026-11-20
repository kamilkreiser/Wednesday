# FOR-RECORDS (B1805, round 1: GO WITH FINDINGS @ 5261774 on root main 53fcad7)

Fold: `git merge --ff-only records/b1801` into root `main` by the records seat only (GO WITH FINDINGS has no Blocker or Major; parent of the commit equals main 53fcad7b11231ea8db6551b377a84734c6c28346). Re-check `main` is still that sha first; if it moved, the two folder paths are new, so a non-ff merge needs a fresh look.

## C-entry facts
- Lane CW-1 (PCOMP-29, L0-1), C104 (B1801): `Content/2026-11-20_sample-crosswalk/` (sample-crosswalk.json 135671 bytes, sha256 d3434b54b62bc177...; README.md 3490 bytes, f3ad71545f70832a...), commit 52617740477a5e8621cf66b34fa8458b0b1c15fb on `records/b1801`. PR 85 head pinned 851057291ffb019baee6c3c51a50d7b8833f5b3a; seven sources sha-checked.
- 132 rows; 11 absent (M008 M037 M038 M050 M080 M089 M098 M106 M109 M111 M130); M106 has no SM item; M080 and M106 no vendor item; 143 items listed (125 with rows, 18 without), 376 sub-settings (8 named by rows), 137 map entries (130 on rows, 7 not), 123 registry controls (116 on rows, 7 not). Independently re-derived: 0 differing rows; JSON byte-reproduced.
- Authority: C-90 (ids and names, no help text) and C-100. The Q-03/Q-04 "HP-internal identifiers" question is NOT concluded. Internal records, ships nowhere.
- Gate: G2, round 1: GO WITH FINDINGS (F1 to F9 in VERDICT.md; none blocks).

## BACKLOG row 328 state
Records-built, gate GO WITH FINDINGS, folded (once the records seat folds). Not done: CW-2 reads it; Q-03/Q-04 open.

## PCOMP-29 comment (facts for the records seat to post; this gate wrote nothing to Jira)
Crosswalk built and gated: path, commit, counts above, flags (14) and the open questions below. Ticket was Backlog, 0 comments at 20:02.

## Kit wording to correct in any successor
- CK10: "no 40-character window of any sensitive string" must say catalogue `id` values (item, sub-setting, category) are excluded and everything else is kept; and say a failed check ends `STOPPED: NEEDS TUESDAY` even when the cause is explained (F2).
- FACT 4: of the 48 catalogue strings of 40+ chars, 45 are text and 3 are sub-setting ids (42, 44, 48 chars); not "names and category paths".
- The commission's evidence file `step2_jira.txt` is `runs/step1_jira.txt`.
- Flag definitions: decide whether a map-held item (M008, UQ-008 on M007) is "from the seed alone" (F3); add how the map's `how` is shown (F4); say whether `map_controls` is per entry or a set (F6).

## Open questions, decided by nobody
1. Are SM item and sub-setting ids "HP-internal identifiers" (Q-04)? 2. May `category_ids` (CamelCase ids carrying label words) stay in a records file? 3. Carry vendor names (C-90 permits)? 4. M106's question to the reviewer (PCOMP-94 Q-P1; the send is the product owner's). 5. Whether SM-PLFtpServer (a catalogue-only map entry on no row) belongs to M080 (seed names none; no name equality). 6. Whether the builder's untracked evidence folder (F8) stays as is.
