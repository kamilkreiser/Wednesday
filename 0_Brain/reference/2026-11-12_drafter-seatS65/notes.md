# Drafter notes, Seat S 65th brief (2026-11-12 ~10:2x AEDT)

Output: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS65/brief_S65.md`. Copy-and-change of S 64th's stamped brief; PROVENANCE line plus one `KS-NNNN | <abs path> | read 2026-11-12` row for every KS key named (checked by script: 33 named, 33 rows, none missing); blank STAMP block at top and at the end; no SELF-CHECK line; no lesson-file names.

## What I read (whole)
commission; S 64th brief (to PROVENANCE); Wednesday's two S 64th mails; S 64th HANDOVER (FINAL block); drafts/cards_s64.md; evidence/writes_s64.tsv; faults_s64.md; wrap mail batch text; pr_state_wrap_s64.txt; search_g321_2198_s64.out and search_g319_s64.out; gate 321 verdict lines 77-82 (partly, 300-char cut).
Not read whole: ROUTING (294 KB, counted only), the gate 319 verdict, KS-1398 and other tickets (no Linear reads, none allowed).

## My own measurements (read-only)
- develop = d35f75875275158ce3b20b636b4198a4c8834968 (ls-remote): equals S 64th's HANDOVER. PR heads 2194 fef6e751bf7a, 2195 3eed5f75fa28, 2196 fed1d35ce95c, 2197 2f10c9750a90, 2198 5064d0e99dd8: all equal S 64th's wrap table. OPEN/MERGED NOT read: no merge evidence, no API read.
- ROUTING: 578 rows by `| KS-N |` prefix (matches HANDOVER), 512 distinct (matches), 293,993 B, HANDOVER 10,542 B. tools: 78 entries (`ls -A`). partition_s64: 109 lines. eligible_p3_s64: 157 lines (boot list; HANDOVER says 135 left).
- history.md: `Seat S 65` 0, `Seat S 64` 1 (positive control), `Seat S 63` 2.
- tmux at my read showed many panes (fleet windows, %0..%22), not the floor statement of the commission; floor is Wednesday's to fill at the stamp.

## Discrepancies and flags for Wednesday
1. **Tag count**: `[S 64th]` rows by my grep = 10, `[S 64th facts only]` = 14 (24), while S 64th's HANDOVER says 9 and 14 (23). The `-o` count of tagged KS rows is 23; the 24th matching line is the header (line 2). So one of "10 vs 9" is a count artefact; I put this in the brief as "recount", not as a fact.
2. **G319 finding numbering**: Wednesday's earlier ADDENDUM and S 64th text say "G319-2195-1 and -2" as one filing, while the commission names "G319-2195-1, G319-2195-3". I kept the -1 plus -3 set from the commission, with -2 to be read and identified by the seat before filing. Gate 319 verdict not read by me.
3. **Gate 322 (PR 2199)** has a verdict directory; no filing licensed in the commission; the brief says none unless stamped. Wednesday may want to add it.
4. **KS-1329/KS-1242/KS-1466**: carried as findings only (item 5), not actions, as commissioned. KS-1466 SPARK routing conditioned on reading its Not decided / Unmeasured sections.
5. **KS-1398 card**: brief instructs the seat to hand the draft to Wednesday by mail (QUESTION-class), after re-reading the ticket; Wednesday posts.
6. **G321-PRE-1 ticket question** left with Wednesday (S 64th asked, unanswered); brief says file nothing until a stamp/ADDENDUM.
7. Provenance carries KS-1090 only because the carried substitution text names it; trivial.
8. Brief drops S 64th's KS-663 byte round, S 63rd reconstruction rows, FILINGS 2 and 3 as DONE; KS-663 comment id recorded under RULED BY KAM as the card's delivery artefact. The S 64th "RULED BY KAM, NOT YET IN AN ARTEFACT" section carried verbatim in substance (card ids and rulings, Kam's two quotes); the first bullet updated with the now-existing artefact id.

## Hard limits
No cd, read-only git (ls-remote with GIT_OPTIONAL_LOCKS=0), no writes to Linear/GitHub/mail/boards, no .env values; wrote only inside the drafter-seatS65 folder. No drive drops observed.
