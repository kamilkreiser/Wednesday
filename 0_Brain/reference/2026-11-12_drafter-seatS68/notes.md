# notes.md: drafter notes for brief_S68.md (Seat S 68th, Secuura/Blockchain-S, board)

Method: copy-and-change of S 67th's stamped brief (read whole, both pages), plus Wednesday's S67 answer_plan and the 01:34Z answer_s67_next, S 67th's HANDOVER, wrap mail (out_99), faults_s67, cards_s67, the gate 325 verdict (whole), gate 321 and 319 finding lines, the B 150th commission (RULING paragraph), Seat A 25th's READY mail item 11. No Linear, GitHub API, mail or board access; only read-only `git ls-remote` and `cat-file -t` (GIT_OPTIONAL_LOCKS=0, via `-C`) on the shared checkout. No cd anywhere (one bare `=====` word slipped into a Bash call and the hook refused it; nothing ran, I re-ran without it).

## What changed from S 67th's brief
- Ordinals shifted one; REC/REC67/REC66/REC65/REC64 re-pointed; chain to read is now five briefs (S 67, 66, 65, 64, 63) because the 63rd holds QUOTA RULES and FIRST MOVES; STAMP block blank (three empty bullets); no SELF-CHECK line; no lesson-file names.
- RULED BY KAM section carried verbatim (the four bullets of S 67th's stamped brief).
- Queue: 0 wake paths (waiter now over the 22-PR set plus 2204 and 2157); 1 p-none from KS-1083 (22 eligible) with KS-2177 as a row, no write; 2 ON MERGE: (a) gate 321 3b/3c, (b) gate 319, (c) carried PR-gated filings, (d) PR 2204 -> ONE KS-1952 comment with ruling G325-2204-1 (verbatim from the B 150th commission file), (e) gate 325's two candidate filings; 3 S 67th's findings carried (keys as in the commission); matcher note re-keyed (suffix-less mail = UNSURE, act only if body line 1 names your seat).
- Kit re-key note: REC66/T66 -> REC67/T67 pairs, drop the two zero-count watch_inbox pairs up front, comment ALLOWED {KS-1728} spent, rename the p3next/p3g aids (S 67th HANDOVER 7a, F2 to F6).

## Facts measured by the drafter (starting facts only)
- ROUTING (REC67): 783 rows, 715 distinct keys, 426,895 B; `[S 67th` 110 lines, `[S 67th]` 77, facts-only 33 (header explains the +1: 76 + 33 = 109 rows, agrees with the HANDOVER). HANDOVER 9,702 B. Tools `ls -A | wc -l` = 78. Partition 109 lines. writes_s67.tsv 2 lines (header + KS-1728). history.md: `Seat S 67` 1, `Seat S 68` 0.
- Eligible set by S 67th's predicates (python3 -I over board_all_after_s67.json, 776 issues, plus REC67 ROUTING and partition_s67.txt; NOT the live board): p-none **22** = KS-1083 .. KS-1744 (equals the HANDOVER's 22, lowest KS-1083; all 22 Backlog p-none in the file, none in a ROUTING row, partition or Peter/Stuart); p3 1 (KS-2177); p1 0, p2 0, p4 0. Backlog by priority in that file: p3 234, p4 150, p2 80, none 22 (sum 486 = the log's Backlog).
- develop `ls-remote` = `1247e1af3c203d369d01b4d574de377adeec4b98` (PR 2202 squash per HANDOVER), 12:49 AEDT; the shared checkout lacks that object. All 29 PR heads (22 waiter + 2194, 2196, 2184, 2185, 2200, 2201, 2202) equal S 67th's boot table by diff; also 2204 `25ad80bc8298`, 2157 `1a8e6dd8ef97`, 2205 `06fbdf9906d0`. No PR state read (no API).
- Outlook add-in: `documentType: metadata.contentType || 'application/octet-stream'` at api.ts line 118 in gate 325's clone (blob 35c5e444 identical at 088fa84d and 25ad80bc); NOT read at develop 1247e1af3c20.
- Gate finding line numbers re-read: gate 321 verdict 77 to 82 (-1 at 78, -3 at 80); gate 319 verdict -1 to -3 at 89 to 91 (-4 at 92); gate 325 verdict Q8 246 to 254, Findings 255 to 283, NOT TESTED 284 to 291.

## Judgement calls for Wednesday to rule at the stamp
1. PR 2204 is not in S 67th's 22-PR waiter set; I told the seat to add it (and read PR 2157's state) because 2d/2e fire on its merge. Rule otherwise if the merge lane's MERGED mail is your trigger.
2. Item 2d: I added a guard the commission does not state: if PR 2157 already reads MERGED when 2204 merges, the carrier sentence is not licensed as written, so QUESTION and no comment. Also the comment needs an S68-D allow-list edit citing your STAMP (restate 2d there) or the seat QUESTIONs.
3. Item 2e(i) (catalogue validation OFF on both boxes): a board seat has no box access, so the brief makes it a QUESTION, as the commission says. 2e(ii): severity and form left as a QUESTION in the plan (the commission names none).
4. The 01:34Z ANSWER is cited at its scratchpad path (session-local); if the successor cannot read it, the brief points to HANDOVER FINAL for the same content. Consider copying it to briefs_staged at the stamp.
5. The commission's matcher note says only that suffix-less mail is UNSURE; I did NOT repeat S 67th's D75 late-answer rule, and told the seat to read the inbox by hand for any `(Seat S 67th)` mail after 01:45Z. Restate in the STAMP if you want the D75 re-key.
6. Chain depth: five briefs to read (S 67th's cost 33.6 points to plan mail, about 19 in reading); I did not flatten it (size cap, no new lessons).
7. After p-none (23 rows, about 3 to 5 points at S 67th's 0.14 to 0.19 a row) the seat will have nothing due unless something merges; the brief tells it to STATUS and QUESTION rather than invent work.

## Not done / limits
- No live board, PR-state, tmux or mail reads. S 66th's 6a-6h and S 65th's list are not re-read; the brief points to the S 67th brief's items 6 and 7 for them rather than relisting their keys (size). S 66th/65th card-draft key lists are likewise referred to by file.
- Checks run: all 88 distinct KS keys in the brief have a PROVENANCE line with an absolute path; one literal `PROVENANCE:` line; no SELF-CHECK; no lesson names; no `cd` or bare-equals word. Provenance for keys carried from S 67th's brief cites that brief's path (its PROVENANCE names the original). Extra files in the folder: body.md, prov.md (build intermediates; nothing deleted).
