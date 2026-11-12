# Drafter notes, Seat S 66th brief (2026-11-12 about 11:00 AEDT)

Output: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS66/brief_S66.md`, 114 lines, 32,140 bytes (limit 55 KB). Blank STAMP block, literal `PROVENANCE:` line, no SELF-CHECK line, no lesson-file names. Key coverage checked by script: every `KS-NNNN` in the body has a provenance line and every provenance key is named in the body (0 missing, 0 extra).

## Inputs read (whole)
commission.md; S 65th's stamped brief (101 lines); Wednesday's three mails to S 65th (plan, ks1398, g314); REC65 HANDOVER.md, writes_s65.tsv, faults_s65.md, cards_s65.md, mail/out_99_body.txt, pr_state_wrap_s65.txt, merge_waiter_run2.log, watch4.log, pid files.

## Method
Copy-and-change of S 65th's brief as a delta chain (S 65th -> S 64th -> S 63rd), substitutions shifted one ordinal, S 65th's spent items marked DONE, S 65th's RULED BY KAM section copied verbatim, rulings from S 65th's STAMP and mails restated in a carried-rulings bullet (the STAMP is blank), queue per the commission.

## Drafter measurements (single reads, 10:5x to 11:00 AEDT; the seat recounts)
- develop `ls-remote` = 697f422f1a394ab00454ced051f018556573837e (equals HANDOVER). Model per models_latest.json = claude-sonnet-5-5.
- `ls-remote` heads for all 22 waiter PRs plus 2194 to 2198 EQUAL S 65th's wrap table: unmoved, so no evidence of a merge since. PR 2199 head 4a0a166b95a1, PR 2200 head 911af6004275 (not in waiter set; I did not compare them to anything). PR state (OPEN/MERGED) NOT read.
- ROUTING in REC65: 618 rows by prefix, 550 distinct keys, 320,292 B. Tag counts: `[S 65th` on 41 lines (header + 40 rows); exact `[S 65th]` 23 (one is the header), `[S 65th facts only]` 18; HANDOVER says 22 + 18. Consistent once the header is excluded.
- REC65/tools `ls -A | wc -l` = 79 (S 64th's was 78; the brief says confirm). partition_s65 = 109 lines. eligible_p3_s65 = 135 lines; NEXT KEY KS-1698, then KS-1701, KS-1705 (read from that list). 97 left per HANDOVER (135 - 38), not recomputed against the board.
- history.md: `Seat S 66` 0, `Seat S 65` 1.
- Board census after S 65th: 773 = Backlog 487, In Progress 234, Todo 38, In Review 6, Blocked 3, Done 4, Duplicate 1 (from HANDOVER; sums to 773).

## Choices and flags for Wednesday
1. STAMP block left fully blank (FLOOR and Rulings lines have no value) per commission; I did not copy S 65th's floor.
2. Matcher note written as a test the seat must run: a `(Seat S 65th)` message after the S 66th stamp is its own, before is foreign.
3. Added a carried-rulings bullet (G321-PRE-1 no ticket, gate 319 -2 inside -1, gate 322 none, KS-1466 KAM-CARD already posted, KS-2169 nothing, PRs 2199/2200 outside waiter set, mail-only) because the S 65th STAMP they sat in will not be in a fresh seat's STAMP. Delete if you would rather restate them in your own STAMP.
4. Added S 65th's F2 lesson to the re-key (derive must reach the variable names REC64 and T64) and F1 (cp before Read of the preflight file); added a cost warning (35.1 points to plan mail).
5. G321 search file note: the saved search is in REC64 (S 64th's), predates PR 2189's merge; the brief says re-run it. The g319 search is likewise in REC64.
6. Carried S 64th findings (KS-1242, KS-1329, KS-1776 repro) are cited to S 65th's brief, not re-read; flagged as soft spot 7.
7. S 65th's ROUTING carries two rows each for KS-1466 and KS-1398; brief says leave both.
8. The waiter set of 22 is S 65th's list, not re-derived from the board.
9. Not independently read: ticket states, PR API states, the live floor, launcher preflight. No Linear/GitHub/mail writes; no `.env` read; no git writes; only read-only `ls-remote`.
10. Slip: first Bash call had a `cd` and a zsh `=====` token; both refused by hooks before running; nothing wrote. One directory listing printed far more than needed (read-only).
