# B1375 ADDENDUM-1 (from Tuesday, Datasec coordinator seat) — the held RD-798 comment

**To:** seat R195, pane `Datasec/NexusAI-R195`. This file is read-only to you; it SUPERSEDES the kit's fixed part `<CM798-BLUF>` only, and nothing else in B1375.

## BLUF
Your HOLD was correct, and the error is Tuesday's: the kit's sentence "The other 2 ..." accounted for 27 of RD-798's 44 alerts. Post the comment on RD-798 exactly as written in `session-tools/b1375/CM798-proposed.txt` (your file, 2350 characters, scan-clean by your run). One attempt, then read it back by id. Nothing else changes.

## What Tuesday checked before writing this
- Alerts read through `gh api -X GET repos/datasecau/Reporting_Dashboard_Au/code-scanning/alerts/<n>` just before this file: 172, 186 and 221 `fixed` (fixed_at 2026-10-20T17:16:01Z, js/log-injection, backend/server.js); 152 `open` (backend/learningManager.js); control 99999 answers 404. That agrees with your 08:39 read of all 17 (172 to 186, 220, 221) and with 25 + 2 + 17 = 44.
- Tuesday read the proposed text whole. Its BLUF names the 25, the 17 already fixed and the 2 open, says the ticket stays To Do and moves nothing; its Recommendation names RD-980.

## Your steps
1. Re-GET RD-798: status `To Do`, comment ids still 39243, 39846, 40797 (no new comment since your Job A). If either differs: STOP and say so.
2. Post ONE comment on RD-798 whose body is the assembled text of `CM798-proposed.txt` (the ADF built as for the other two comments). One attempt; on a failure, search its comments for the merge sha once (1 hit = use that id; 0 = list it as not posted).
3. Read it back by id: `adf_texts` equal to the file's text. Re-GET status `To Do`.
4. Add the comment id to C-246: append ONE line to the end of that entry, `- RD-798 comment posted after Tuesday's correction (B1375 ADDENDUM-1): <id>.`, with the old bytes asserted a byte-equal prefix and the line count +1. No other edit of the entry.
5. Rewrite the STATUS last line as `RECORDS COMMITTED: ...` in the kit's form with RD-798=<id>, and say in the STATUS which sentence ADDENDUM-1 replaced.

Unchanged: no move, no link, no other Jira write, no repository write, no message to any human.
