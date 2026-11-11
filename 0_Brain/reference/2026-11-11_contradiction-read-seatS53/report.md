# Contradiction read: 2026-11-11_seatS53_board.md (read-only reviewer, 2026-11-11)
Result: no SELF-CHECK line; heading present once; no 'Spark OFF', no stale develop presented as current, no PR 2156 described as open, no B 159 count. 11 findings below, 4 of them need an edit before stamping (F1, F3, F4, F6).

## 1. Internal contradictions
F1 L4 "Four jobs, in this order. (0) FIRST: ARM THE MERGE WAITER ... (1) ... (2) ... (3) ... (4)" lists FIVE (0 to 4). Replace "Four jobs" with "Five jobs".
F2 L21 "and the four for item 4: G303-2156-7 ..., G304-2156-2 ..., G306-2167-1 ..., G306-2168-1 ..., G307-2170-1" names FIVE. Replace "the four for item 4" with "the five for item 4".
F4 L114 "k. **Not filed by you:** gate 278 (PR 2118's KS-2127 beyond item a), gates 283, 285 to 290, ... PR 1360 is Seat B 115th's row." and L116 "k. **Not filed by you:** gate 278 (... beyond item 1a), ... gate 305 (Wednesday's GO rules no filing), ... KS-1825 got no write and stays OPEN". Two items labelled k with different content (item a vs 1a; L116 adds gate 305 and KS-1825; L114 adds PR 1360). Delete L114 and its blank L115; append to L116 "PR 1360 is Seat B 115th's row."
F5 L124 "KS-1821 (queue item 2's ONE close or ONE comment, nothing else), KS-1819 (queue item 3: card text in your record folder only ...)" and "KS-1995 (except the PR 2138 filing's own read-and-decide in item 1h)". Those are S 52nd's old queue numbers; this brief's queue item 2 is the ROUTING table and item 3 is Todo/Backlog; the PR 2138 filing is item 4h. Replace with "KS-1821 (S 51st's one comment fdfa5741; nothing else)", "KS-1819 (card text in your record folder only, no ticket write)", "item 4h".
F8 L141 (6) "item 4a to 4c are OWED NOW ... so do them FIRST among the writes once the ANSWER releases them, ahead of the triage's first write" versus L4/L83/L96 order (triage is item 1, filings item 4, BLUF "in this order"). Replace L4's "(4) THE POST-MERGE FILINGS" lead with "(4) THE POST-MERGE FILINGS, whose 4a to 4c are the FIRST writes once the ANSWER releases writes, ahead of triage writes", or drop soft spot (6)'s ordering.
F9 L90 "(KS-2058 on the HELD list; ...)" but the HELD lists (L123 to L125) do not name KS-2058 (only "the KS-2058 pointer" in L116). Replace with "KS-2058 is a lane/pointer key: row HELD, no write" and add KS-2058 to L124, or state it is in partition_s52.txt if verified.
F10 L90 "the likelier closes are the 'Left open: a live check is owed' rows (KS-1176, ...)" then "classify them (c) KAM-CARD or CLAUDE-BUILD ... and do not hold the queue on them": calls them likelier closes yet routes them to no close. Replace "the likelier closes" with "the likeliest eventual closes (after the sweep)".

## 2. Contradictions with the FACTS
F3 Seat R 95th brief EXISTS now (2026-11-11_seatR95_raise.md; launched 14:18). Stale sentences:
 L4 "(the drafter's `ls` at 14:2x found NEITHER file yet: both are being drafted beside this one; read them when they exist ...)"
 L70 "NOT YOURS, by path (neither file existed at the drafter's `ls` at 14:2x ..."
 L141 (8) "names paths that did not exist at the drafter's read."
 L153 "Seat B 132nd brief and Seat R 95th brief do NOT exist yet (ls returned no such file for both)"
 L319 "The B 132nd and R 95th briefs (do not exist yet)."
 Replace: "R 95th's brief exists (launched 14:18; read it, write nothing on any key it owns); B 132nd's brief is still being drafted (not on disk at the review, 14:2x)". L153/L319 likewise split per seat.
F11 L308-L309 treat the 238 as an unclassified pool and say it is UNMEASURED whether any started ticket's PRs all merged. Wednesday's census now exists: 238 = A 73 (>=1 open PR) + B 161 (all PRs merged/closed, incl. 2 B+D) + C 4 (no PR attached); 229 In Progress, 6 In Review, 3 Blocked; 472 PRs measured (summary.md, with its 161 correction; census.tsv beside it). Add to L83: "Wednesday's census (0_Brain/reference/2026-11-11_ks-inprogress-census/summary.md and census.tsv) gives A 73 / B 161 / C 4 by attachment only; B is a candidate-Done list, verify at source; PRs only in text are unseen." Counts L6/L158 (781, 499, 229/6/3, 39, 4, 1) agree with each other and with the 238 and 39 facts.

## 3. Instructions a seat could not follow
F6 L130 names tools that do not exist under those names: `tools/mail_read_s50.py` (re-key to `_s51`), `pr_heads_s50.py` (re-key `_s51`), `allow_tool_s50.py close AUTO KEY` (re-keyed `_s51`), `close_s50.py`, `pool8_s50.py`. REC52/tools holds `_s52` files only (mail_read_s52.py, pr_heads_s52.py, allow_tool_s52.py, close_s52.py, pool_s52.py; no pool8 anywhere); this brief's target suffix is `_s53` (L81). Replace with "`mail_read_s53.py`, `pr_heads_s53.py`, `allow_tool_s53.py`, `close_s53.py`, `pool_s53.py` (re-keyed from the `_s52` files)"; L94 "the pool tools `pool8`" becomes "`pool_s53.py`".
F7 L94 "Use S 52nd's earlier batches as inputs where they exist (`REC51/drafts/backlog_batch_09_s51.md` ...)": the file is S 51st's. Replace "S 52nd's earlier batches" with "S 51st's batch 9".
F12 L18 `gl.sh lines SHA PATH A B` and `file_one`: no `REC52/tools/gl.sh` (it is `REC52/tools/examples/gl.sh`) and no `file_one` binary (it is `file_one_s52.sh` plus `file_ticket_s52.py`). Replace "`gl.sh lines`" with "`REC52/tools/examples/gl.sh lines`" at first use and name `file_one_s52.sh`.
F13 L81 job (0) "FIRST, at boot, before any other work" arms `REC/tools/merge_waiter_s53.py`, which exists only after the READ FIRST 1 re-key (and L19 requires the preflight copy as the first call). Add: "after the preflight copy (call 1) and the kit re-key (READ FIRST 1)".
Not-yet-existing by design (not a fault): REC dir 2026-11-11_seatS-53rd/, ROUTING_2026-11-11.md (seat creates them); 2026-11-11_seatB132_merge.md (being drafted).

## 4. SELF-CHECK and heading
Lines beginning 'SELF-CHECK:': 0 (grep -c '^SELF-CHECK:' = 0). Heading '## RULED BY KAM, NOT YET IN AN ARTEFACT': exactly 1 (L26).

## Coverage
Lines read: 319 of 319 (wc -l 319; Read chunks 1-60, 61-110, 111-155, 156-195, 196-235, 236-277, 278-319). Commission (18 lines) and census summary (33 lines) read whole.
Paths checked: about 122 (39 absolute /Volumes/DevMASTER paths extracted by grep; 32 REC52 relative files and tools; 26 briefs_staged mails by name plus 5 S45 and 4 S46 glob matches; 13 gate verdicts + ready_mail_g34.txt; 3 learnings; decision_queue.sh; cockpit.sh; preflight file; S44/S45 drafts; REC51 batch 9; REC50 HANDOVER). Missing: 3 only by design (REC dir, ROUTING file, seatB132_merge.md) plus the two name mismatches in F6/F12 (tools/gl.sh, `file_one`) and the `_s50`/`pool8` names. Model-routing lines 97 and 98 confirmed (C7, C8; 'board seat' count 0). history.md: 'Seat S 53' 0, 'Seat S 52' 1 (as the brief says).
