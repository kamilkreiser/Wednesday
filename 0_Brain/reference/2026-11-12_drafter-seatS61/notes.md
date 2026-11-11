# notes.md: drafter notes for brief_S61.md (2026-11-12 ~04:2x AEDT)

Contradictions and departures:
1. Commission item 7 says S 60th's eligible file holds "122 eligible after KS-1444"; the file `evidence/eligible_p4_s60.txt` actually has 144 lines (the boot list). I rebuilt: 144 minus keys with a ROUTING row (361 distinct) = 122, first KS-1481. Agrees with the HANDOVER. The brief tells the seat to rebuild it.
2. Commission says 417 ROUTING rows: confirmed by `grep -o -i` prefix count (a first plain grep returned 417 too). 361 distinct keys (S 60th's 383 rows held 339; S 60th added 34 rows).
3. No-write set: S 60th's brief said 107 + 2; its HANDOVER and partition file say 109. Brief uses 109 (wc -l 109) and tells the seat to rebuild and compare.
4. The commission names 17 waiter PRs; the brief lists their heads from S 60th's HANDOVER (not re-read at the API by the drafter; no API read taken).
5. S 59th brief line refs: only lines 15, 17, 19, 32, 85-88, 111 spot-read (file is 449 lines). Other refs carried from S 60th's brief unverified; stated in soft spots and UNMEASURED.
6. Live-seat facts: commission item 6 says FLOOR is Wednesday's. Brief carries `FLOOR: <Wednesday fills at stamp>` as a literal line and a hedged live-seat paragraph from S 60th's measure (R 101st %83 rows 45-47; A 19th; B 142nd). The commission-named staged files A19_answer_ks1513 and A19_ruled_develop were not used (other lane).
7. KS-961 is quoted in a routed item; no ticket read, provenance says so.
8. No Linear census taken by the drafter: no ticket state facts are asserted from the board.
9. Dual-use ordinal: S 60th's history ordinal counts now S 60: 1, S 61: 0.
