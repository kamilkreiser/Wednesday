# Review of brief_S56.md (Seat S 56th board brief), independent reviewer, 2026-11-11

Read whole: brief_S56.md (270 lines, 132827 bytes), notes.md, commission.md, and the four S 55th ANSWERs (plan, ks174, ks174_relation, status1). The S 55th brief (357 lines, 145212 bytes) was read only by heading list and one grep, not line by line; its text is judged here only through what S 56's brief says it copied. No Linear, GitHub, mail or board call was made. No claim below was checked against live state; every finding is a document-internal check.

## VERDICT: STAMPABLE WITH CHANGES

No instruction writes on a Peter or Stuart ticket or moves one. The N-3 correction, the KS-1509 condition and the KS-2055 single-comment rule are all present. The problems are: stale or dangling cross-references that could make the seat re-do or mis-route a write (findings 1 to 5), a gap in the B 133rd and B 134th partition (6), two provenance holes (10, 11), and a size and reading load that is the real cost to the seat's window (13).

---

## Findings

### 1. KS-1402 and KS-1785 held lines still read as live (CONTRADICTION, MEDIUM)
- Line 149: "KS-1402 (left OPEN; only queue item 2(b)'s ONE filing)". Item 2b in THIS brief is the KS-2055 comment. The KS-1402 filing it meant is done (KS-2165, line 127), and lines 127 and 145 say KS-1402 takes no write. A seat reading line 149 alone could think a KS-1402 write is allowed.
  Change: replace with "KS-1402 (left OPEN; its filing is KS-2165, DONE; no write)".
- Line 148: "KS-1785 takes ONLY the item 4b comment". That comment is cf303a8b, already posted (line 1, line 149 "DONE; nothing more"). Line 148 reads as a standing permission.
  Change: "KS-1785: the item 4b comment cf303a8b is DONE; no write".

### 2. "Item 3" means two things, and "ruling 6" and "RULED block 8" point at nothing (CONTRADICTION, MEDIUM)
- Line 4 BLUF (1) says the 13 filings are "item 3 below, carried unchanged". In this brief the filings are queue item 1 (sub-items 3a to 3k, lettering kept from S 55th) and queue item 3 is KS-1509 (line 115). Line 94 repeats "item 3 below"; line 94 also says "re-run the item-3 terms" and "item-2 and item-5 terms", all S 55th numbering, unexplained.
  Change: in lines 4, 94 and 95 say "queue item 1 (S 55th's item 3, sub-items 3a to 3k)"; rename the S 55th references "S 55th's item 3".
- Line 49: "'as many agents as it takes' is ruling 6 above". This brief's RULED BY WEDNESDAY block has items 1 to 5; no ruling 6. The cap is in line 142.
  Change: "see SUB-AGENTS below".
- Lines 89 and 149: "RULED block 8 above" and "RULED block 8". No block 8 exists in this brief (S 55th's numbering). The rule is item 1(a) of the Wednesday block (line 38).
  Change: cite "RULED BY WEDNESDAY item 1(a)".

### 3. BLUF states two rulings without their conditions (MEDIUM)
- Line 4 (2): "gate 210 N-3 gets ONE facts comment on KS-1176 (OPEN)". The CLOSED or archived fallback (file ONE Low ticket) is in lines 40 and 112 but not in the BLUF. Acceptable only because the BLUF says "(OPEN)" as a fact at 16:3x.
- Line 4 (3): "KS-1509: close Done under the running-build rule". The ruling is conditional: close only if the ask does not include fixing stored-zero rows (lines 41, 115). A seat that acts on the BLUF line alone skips the condition.
  Change: line 4 (3) to "KS-1509: close Done ONLY IF its ask does not include fixing rows already stored with 0 (else PARTIAL(c), no write)". Line 4 (2) append "if KS-1176 has closed since, file ONE Low instead (item 2a)".

### 4. Item 4 of the checklist: N-3 and KS-1509 content (PASS with two changes)
- N-3 cites 204f3bdd and not c90bfc2c, and says comment on KS-1176 (open), at lines 4, 40, 112 and 159(2). c90bfc2c appears only as "NOT" or as the correction. PASS.
- Fallback body (line 112): if KS-1176 is closed the seat files a ticket with "the same body", but that body says "this comment adds", "this ticket's own round-2 record" and "Comment 204f3bdd on this ticket". Those words are false in a new ticket. LOW-MEDIUM.
  Change: add "(for a ticket, rewrite 'this comment' and 'this ticket's' as 'KS-1176's')".
- Line 112 draft body states "PR 1014 round 2 made reachable through `documentType || type`" and the four gateway code names. Neither has a source line in the brief or notes. They presumably come from KS-1176 comment 204f3bdd or the drafter's read of the spec, but nothing says so. LOW.
  Change: in the pre-write list add "confirm `documentType || type` and the four codes in the body against comment 204f3bdd and the spec lines before posting; drop any you cannot".
- KS-1509 condition "close only if the ask does not include stored-zero rows": present at lines 41 and 115 (and flips on any stored-row ask in its three comments). PASS apart from the BLUF (finding 3).
- Heal sites through `toBlockHeight`: named as unverified and put on the seat (lines 41, 115, 267). PASS.
- Kintsugi base from Seat D 60th: flagged as not re-read at lines 28 and 269, but the KS-1509 action chain at line 115 does not tell the seat to re-read D 60th's HANDOVER, nor to check that a newer `*seatD-*` folder or a newer kintsugi revision does not exist. Lines 28 and 41 ask only for the ancestry re-run. MEDIUM.
  Change: in line 115 add "first re-read Seat D 60th's HANDOVER for the kintsugi revision (and `ls -d` for a newer D seat); quote the sha you actually used in `--build-evidence`".
- Count mismatch left unreconciled: line 41 quotes the ticket's Recommendation as "change these five", then says "The seven sites at the tip". LOW.
  Change: one clause, "five in the ask plus the two former heal sites = seven", or ask the seat to reconcile.

### 5. KS-2055 comment is not only the ruling (MEDIUM)
Line 20 and line 145 say ONE comment and nothing else; line 113 posts it. PASS on count. But the DRAFT BODY (line 113) goes beyond recording Kam's ruling: "Not decided here: ... who builds it; Wednesday assigns the build" (an internal coordination statement on a client-visible board that Kam did not rule), a restatement of the card's default "text only, trimmed", "Half 1 ... merged as PR 2113", and a handler read. It also puts the card id `secuura-ks2055-...` and the coordinator's name on a board Peter and Stuart read.
  Change: trim the body to (a) Kam's ruling with card id, the 1000 figure and the board time, (b) the two source lines at the tip, (c) "No state, assignee or field changed; no build started". Delete "Wednesday assigns the build" and the PR 2113 paragraph or keep PR 2113 only as a fact read from the ticket. If left as is, label it a deliberate addition so Wednesday approves it byte for byte (C7, line 9).

### 6. Partition gaps (MEDIUM)
- No mention anywhere of a B 134th merge seat, and B 133rd is described only as live and merging (line 17: plan confirmed 16:14, first row 8x). If B 133rd is wrapping and a B 134th is coming (as the request to me states), the brief has the wrong live-seat picture and does not say that the B table key list may pass to B 134th. A grep for "B 134" found zero hits (positive control: "B 133" matches line 17).
  Change: add one line: "B 133rd is wrapping; a B 134th merge seat follows with the same queue table; hold every key in either seat's table".
- HELD cannot be executed from the brief. Lines 124, 145 and 147 make "every key of a B 133rd table row" HELD, but the brief gives the seat only a partial list (lines 17, rows 8n to 8t and some PRs) and the B 133rd brief is 360526 bytes. Nothing tells the seat how to derive the full key list cheaply, and reading that file whole would cost about 90k tokens. MEDIUM.
  Change: tell the seat to extract only the table's key column with a grep of the row cells (the method the drafter used), or have Wednesday supply the key list in the stamp mail.
- What the brief does well: Linear only and never a repo is stated (line 1 "no code, no repo write", line 88); R 96th row 0 is the audit-baseline entry (lines 18, 45) and KS-2164 takes no comment from S 56th; build lanes A and B keys are listed as not yours with UNSTAMPED and "read by head -c 6000 only"; B 133rd's row cells are labelled "by the drafter's grep ... NOT read whole". File lists are not asserted as fact. One imprecision: "no repo write" sits beside instructions to write history.md, the vault daily note and `REC/` (lines 14, 34, 156). They are project-history and vault writes, not the product repo.
  Change: line 1 "no write to `2_Project_Files` (the product repo)".

### 7. Peter and Stuart rules (checklist item 2): no violation, two gaps (LOW-MEDIUM)
- No instruction writes on, moves, or comments on a Peter or Stuart ticket. Lines 42, 124, 138 and 145 list all 8 Stuart and 10 Peter non-archived tickets as report-only; `HUMAN_OK` stays empty (line 33(b)). The two item-2 comments name nobody. PASS.
- KS-1807: line 38(c) says it is "also his [Stuart's] but not started", yet Stuart's non-archived total is 8 (line 169, line 145: KS-61, 101, 135, 139, 188, 239, 441, 1366) and does not include KS-1807, and KS-1807 has no provenance line. Either KS-1807 is Stuart's and the count of 8 is wrong, or the assignee claim is stale. MEDIUM, because the count drives the skip list.
  Change: read KS-1807's assignee (add a provenance line) and fix line 38(c) or the count in lines 6, 42, 145 and 169.
- KS-1175: line 120 says "requester Stuart"; KS-591 and KS-665 have Peter's newest comments. Only KS-591 gets the byte-round warning in line 120. A close or comment on KS-1175, KS-663 (Peter's 2026-09-08 comment, line 118) or KS-665 whose comment names Stuart or Peter needs the byte round (lines 77 and 9).
  Change: add to line 117 "any comment or closing comment on KS-591, KS-663, KS-665, KS-1175 that names Peter or Stuart goes through the byte round; treat a Stuart-requested ticket as Stuart's until Wednesday says otherwise".

### 8. Contradictory wording about the ROUTING file (LOW)
Line 4: "appending to S 55th's ROUTING file (a new file that carries it)" versus line 32: "a NEW file that CARRIES that file's rows by tag, never an edit of it".
  Change: line 4 "starting a new ROUTING file that carries S 55th's rows".

### 9. Stale re-key name and a clock slip (LOW)
- Line 95: `REC/tools/run_search_s55.sh` "re-keyed from `REC53/tools/run_search_s53.sh`". All other tools are `_s56`; this would run an `_s55` name in S 56's kit. Change to `run_search_s56.sh`.
- Line 1: "WRAPPED about 16:4x AEDT 2026-11-11 = 05:3xZ". 16:4x AEDT (UTC+11) is 05:4xZ; the mail wrap at 05:33Z is 16:33 AEDT. Change to "about 16:3x AEDT = 05:3xZ".
- Line 14: "`Seat S 54` expecting 1" has no drafter count behind it (only the S 55 and S 56 counts are in notes B). Change to "expecting 1 (not measured by the drafter)".
- Line 4 pace order versus Wednesday's status1 ANSWER pace order (screens' rows first, then filings, then KS-1509): the brief's order differs (filings, N-3, KS-1509, verify). That ANSWER was to S 55th and the commission order governs, but the brief never says the old order is superseded. LOW. Change: one clause "this order replaces the status1 pace order".

### 10. Provenance: queued or acted-on tickets with no `KS | source | read date` line (MEDIUM)
Every ticket in queue items 1 to 3 and the Todo list has a line (checked against lines 170 to 252: the 39 Todo keys all present, 14 filing-linked keys present). Missing for keys the brief names as work or write targets:
- KS-1959, KS-1343, KS-915 (line 122, "still owed", SPARK rows; the `credentialRepo.ts` lines 98, 370, 459 and `db.ts` line 102 have no source in the brief).
- KS-1807, KS-441, KS-1366 (Stuart's, line 38 and 145), KS-101, KS-139, KS-239 (assignee claims rest on the census line 169 only).
- KS-1845's cited "KS-1882" and the "four other kyc routes" (line 119), KS-2098 (line 6 and 32, 'drift').
- The ten gate verdict files behind filings 3a to 3j (lines 95 to 107) have no PROVENANCE line and the brief itself says "re-opened by S 52nd's and S 53rd's drafters, NOT by this one" (line 95; notes C12 repeats it). The only verdict read is gate 210 N-3 (line 257).
  Change: add `KS-n | source | read date` lines for the keys above, marked "not read by the drafter" where true; add one PROVENANCE line stating the ten verdicts were copied from S 55th's brief unread, so the seat reads each finding whole in the filing action (line 95 already says so).
- Also unsourced: Seat D 60th's `6c9a593df4ab` (line 28, 254, 269, flagged by the brief), B 133rd's and the build lanes' key lists (partial, flagged), the S 55th HANDOVER claim "76 entries" (ls count, fine).

### 11. Searches before filing (checklist item 8): mostly PASS; gaps in named terms (LOW-MEDIUM)
- Nothing commissions a deletion, deploy or merge. "Never delete" is stated (line 88). Every filing in item 1 is "after a board search" (line 94, 95); 2a re-runs its search before the comment or the fallback ticket. 3d asks and writes nothing. PASS.
- Named search terms exist for 3a, 3c, 3f, 3g, 3h, 3j(partial) but not for 3b (logger.warn / processExport), 3e (`[[:punct:]]?`, docker exec), 3i, or the 3j G296 items. Line 95 relies on the REC53 term files (22 terms) that may not cover them.
  Change: list one symbol term per filing, or add "a filing whose term is not in the w1 or w2 files gets its own search first".
- KS-1509 close and the KS-663 and KS-1845 closes: line 73 (S 47th's ANSWER) requires a board search before any CLOSE NOW and naming it in the closing comment; item 3 (line 115) and item 4 omit it, and the close tool needs `--followup` keys that only a search or the ticket read will supply. LOW-MEDIUM.
  Change: add "board search by `toBlockHeight`, `blockHeight` and 'stored with 0' named in the closing comment" to line 115.

### 12. Smaller checks (INFO, no change)
- Counts agree: 503+213+39+6+3+4+1 = 769; Backlog by priority 240+160+81+22 = 503; started 222; open 764; 13 owed PRs, 10 filings; S 54th closes 11 and held 17; S 55th ROUTING 18+76+73+59+14+6 = 246; Peter 10; Stuart 8; build-lane keys 4 and 2; U 23rd keys 6; all stated the same each time they recur.
- Superseded KS-174 duplicate ruling is labelled SUPERSEDED (line 39) and stated as Canceled by path (d) everywhere else (lines 1, 27, 145). The `close_dup` caveat about archived survivors (line 33(d)) is consistent.
- KS-2164: no S 56 comment (lines 45, 145). Consistent with the R 96th draft per notes.
- The card timestamps (16:29:26, 16:29:47 versus ruled_ts 16:29:43, 16:30:23) are explained in lines 45, 46 and 159(7): consistent.

### 13. Pace and size (checklist item 7)
The brief is 132 KB, about 38k tokens, roughly 3.8 percent of a 1M window, so the brief alone does not explain a 23 percent boot. Reading load, in order of cost, is what does: line 32 "THE ROUTING FILE, whole" (99578 bytes, about 25k tokens), the S 55th HANDOVER (12.5 KB), four mails, S 55th's history entry, and the 76-entry tool tree. The brief copies S 55th's text in these blocks (bytes by my `sed | wc -c` of line ranges):
- Lines 63 to 89, "RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE": 14.4 KB. Almost all are delivered or spent rulings (S 41st to S 52nd answers); the live rules are in lines 77, 84, 85, 86 (waiter) and 89. Skippable: about 10 KB.
- Lines 53 to 61, delivered Kam cards and old grants: about 3 KB skippable (keep the 2026-11-06 and 2026-10-10 grants and the 14:0x quote).
- Lines 161 to 262, PROVENANCE: 35 KB, a third of the brief. The 100 ticket header lines are one long sentence each, near identical; the Todo block alone is 13.5 KB. The seat re-reads every ticket and re-runs the census anyway. Compress to a table (key | state | priority | assignee | comments | PRs | read) and keep full lines only for the write targets (KS-1176, 1509, 2055, 174, 458, 2164, 2165, 1391): saves about 20 KB.
- Lines 144 to 149 (HELD paragraphs) repeat the same keys across five paragraphs and again in lines 18 and 19 and the soft spots (line 159): about 3 KB saved by one deduplicated list.
- Line 159 "soft spots" repeats lines 40 to 42 and 17 to 19: about 3.5 KB.
- Lines 152 and 153 "Findings carried": 5.5 KB of tool tips repeated in two paragraphs; keep about 2.5 KB. Saves about 3 KB.
- Lines 94 to 108, filing findings: 13.5 KB copied from S 55th. Needed once, but 3k and the closing sentence of line 95 (the long verdict-path list) are repeated narrative; save about 1 KB.
Estimate: about 40 to 45 KB (about a third) could be skipped or removed with no rule lost, about 11k tokens, about 1.1 percent of the window. The larger saving is behavioural: change line 32 to read ROUTING by key lookup and tag (grep the rows needed) instead of whole, and make the HANDOVER read "FINAL block first, rest on demand", worth about 2.5 to 3 percent. Recommend both before the stamp, since the seat's budget is 55 percent and it booted S 55th at 23.

### 14. Items checked and found PASS
- Check 2: no write on Peter or Stuart ticket; no unruled comment to a human.
- Check 4: N-3 correct; KS-1509 condition present; both unverified items named (see finding 4 for the D 60th gap).
- Check 5: one KS-2055 comment, card id and choice b, 1000 characters (see finding 5 for trimming).
- Check 6: partly (finding 6).
- Check 8: no deletion, deploy or merge commissioned; filings after search (finding 11).

## Recommended change list (ordered)
1. Lines 148, 149: remove the stale KS-1785 and KS-1402 permissions (finding 1).
2. Lines 4, 49, 89, 94, 95, 149: fix the item numbering and dangling references (finding 2).
3. Line 4: add the conditions to BLUF (2) and (3) (finding 3).
4. Line 112 fallback wording; line 115 add the D 60th re-read and the closing board search; line 41 reconcile five versus seven (finding 4, 11).
5. Line 113: trim the KS-2055 body to the ruling and sources (finding 5).
6. Lines 16 to 19: add B 134th and the cheap key-list method for B 133rd's table (finding 6).
7. Line 38(c), 117: fix the KS-1807 count and add byte-round reminders (finding 7).
8. Provenance gaps (finding 10); the six small items (findings 8, 9).
9. Cut the size per finding 13 and make the ROUTING read key-based.
