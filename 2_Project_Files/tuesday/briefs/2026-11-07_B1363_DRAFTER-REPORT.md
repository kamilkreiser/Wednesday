STARTABLE: YES (complete and dry-checked; three things are Tuesday's at the stamp: Q-1 on tickets versus notes for the Minors, Q-2 on findings 9 to 12, and the model/slot defaults)

# B1363 drafter report (seat R190, NexusAI records, Sonnet), drafted 2026-11-07 06:05 to 06:25 AEDT

## BLUF
- Kit `2026-11-07_B1363_SEAT-R190_nexusai-records-tickets.md` (ASCII, 12 four-underscore lines in the `.pre-stamp` copy, counted by `/usr/bin/grep -c -E '_{4}'`), its `.pre-stamp` (byte-equal), `2026-11-07_B1363_slots.json` (12 keys, no `@SEAT@`, clocks `@NOW@`, READ-WHOLE `PENDING`). 8 ticket candidates (TA, TB, TC1 to TC3, TM1 to TM3), 1 comment (RD-928), 1 CLARIFICATIONS entry (C-245, section 81), 1 HISTORY entry on `records/b1363`. 23 of 23 findings of the two landed reviews accounted for. Model: Sonnet, `model-routing.md:110` row G3 (tier 3, no gate), `models_latest.json:23` `claude-sonnet-5-5`. Ports: none.
- **The morning sweep's sentence is wrong, as you suspected, and the truth is worse.** Check 1 said the code "takes the getAllSessions fallback". Source at main `fab4fa41` (raw `backend/server.js` 3508 to 3510): both branches are `typeof` guards, and `jsonStorage.js` defines neither method (`deleteSessionsForUser` 0 hits, `getAllSessions` 0 hits, case-insensitive; control `deleteUserSessions` 1 at `:4066`). So **neither branch runs**: no session is ended, no log, no error. TA says so, marked DERIVED FROM SOURCE, NOT RUN.

## Facts re-measured (instrument, time, control)
- Main `fab4fa4108159dc1ca03c3968c4d7cbe9a721250` at 06:10:52 and again 06:20:04 (`gh api -X GET commits/main --jq .sha`); open PRs 1 (180). PR 178: merged, `merge_commit_sha` `993be21a...`, 2 parents `5690d842,7c5f1a39`, 7 files, closed `2026-11-06T13:01:11Z`. PR 179: merged, `fab4fa41...`, parents `993be21a,a8c66074`, 4 files, closed `2026-11-06T16:40:39Z` (`pulls/N` and `commits/<sha>`, 06:09 to 06:10). Both are genuine two-parent merge commits (the squash worry is not borne out).
- Board: `search` pulled **967 issues** in 10 pages at 06:10:23 to 06:10:27 with description and comments (`b774lib.search`, `python3 -I`); controls RD-798 and RD-923 present, planted `@@NOPE@@zz` 0. AND-set counts: `deleteSessionsForUser` 0, `deleteUserSessions` 0, `requireAuth`+`is_active` 0, `setQuickQuestions` 0, `rd913`+flaky 0, `confirm-clarification` 0, `conversationSessions` 0, `generateBusinessHoursReport` 0, `UNUSUAL_TIME|off-hours` 0, `zz-b1344-none` 0, `gateInHandler` 0, `shell-layout.spec` 0. Hits read and judged not the subject: `session`+`deactivat` 8 (container revisions), `rollback`+`simpledb` 3, `Job_Start_Time` 4 (RD-695 is a neighbour). A caveat: `fields=comment` on the search returns the comments the API gives per issue; I did not re-fetch any issue's comments past that (UNMEASURED beyond it).
- RD-928 To Do, 0 comments; RD-970, RD-971 To Do, 0 comments; RD-798/799/800/936 To Do (read only).
- `HISTORY.md` at main (raw, 9914 lines): B1353 heading at `:9846` once; **no** `#178`, `#179`, `993be21`, `fab4fa4`, `RD-970`, `RD-971` (one unrelated hit at `:8434`). `CLARIFICATIONS.md` tail: C-244 (B1353 seat), 2571 lines; so the next entry is C-245, section 81.
- Pointers: 43 of 43 re-printed by program (raw files at `fab4fa41`, each quoted string asserted a substring of its line, `chk.py` in the drafter scratchpad); `backend/server.js` blob `3a548f44...` equals the contents-API sha. All Jira text parts: 0 non-ASCII, classes gate/seat/brief/coordinator, `B<n>`, `R/G/N...<n>`, at-sign, percent, `C-<n>`, names, branch tokens all 0 (the first run caught the word "gate" in TM2; reworded). Summary lengths printed: TA 148, TB 184, TC1 162, TC2 161, TC3 135, TM1 114, TM2 142, TM3 165 (all under 255, with `{L_...}` filled at 4 characters; no summary has a placeholder).
- Callers: `server.js` has 1 hit for `setQuickQuestions` (`:20435`, `jsonStorage.`), so the simpleDb method has no server caller; **the GitHub code-search index is unreliable** (it returned 0 for `conversationSessions` while `server.js` has 1 hit), so the kit never uses it as proof of absence.
- Live panes at 06:20:04: `Datasec/NexusAI-N110`, `Datasec/HPSM-POC-H134`. N110's kit: Yours line `:90`, NOT-yours row `:91` names `HISTORY.md` and `CLARIFICATIONS.md`, `:11` forbids Jira writes. N110 changes one line of `backend/server.js` (`:3169`), so pointers may shift by 0; the kit re-derives.
- Model: `awk NR==110` printed the G3 row ("Tier 3: backlog or citation fixes, ticket hygiene, comment corrections ... No gate"); `awk NR==92` is the C2 build row. `models_latest.json:23` `"model_id": "claude-sonnet-5-5"`. `brief_seat.sh:24` defaults to opus; the launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Ports: no block assigned; `lsof -nP -iTCP:9490-9499 -sTCP:LISTEN | wc -l` printed 0 at 06:13. I did not do the word-boundary scan of other SEAT kits for a block because the kit needs no port.

## D-decisions (mine, for Tuesday to strike)
- D-1: 8 candidates, not 5. Beyond A, B, C1 to C3 I added TM1, TM2, TM3 (the Minors B1351-1, B1351-2, B1358-2), because `NexusAI/CLAUDE.md` says a finding gets a ticket and a Minor with a concrete committed-file defect is not a Note. TM3 rests on the reviewer's counts only (I read the header lines and the VENDOR line, not the counts).
- D-2: the kit does not record B1359 or B1360 findings (not landed). B1359's two product facts and its `conversationSessions` row became TC1 to TC3 as asked. Line 227 of the B1359 STATUS is the source of TC1 and TC2; TC3 rests on its table row `:163` plus my source read.
- D-3: TA carries `security` only, no `roles-ui-2026-11`, so the morning sweep's exclusion does not hide it (Q-4).
- D-4: HISTORY and CLARIFICATIONS both written (CLARIFICATIONS holds the one-line Notes; HISTORY counts them), following the B1353 pattern.
- D-5: TC1 counts the second site `:19984` as the same pattern in the same function and says so; one ticket per defect holds (it is one defect, two sites).
- D-6: TC2 and TC1 are Low; TA and TB Medium (TB can turn any lane red at random; TA is security-shaped). Neither above Medium.

## Q-questions for Tuesday (each with a default)
- Q-1: Minors as tickets or as notes? **Default: tickets for B1351-1, B1351-2, B1358-2 (searched), B1358-6 recorded only (already ruled Minor).** If you want notes only, set TM1 to TM3 aside and the cap drops to 5.
- Q-2: the request named B1358-2 to -8; the review has -9 to -12 too (`:160-163`). **Default: include them (23 of 23).**
- Q-3: the search rule is the B1353 rule (local AND-sets, 300-character context). **Default: keep.**
- Q-4: `roles-ui-2026-11` on TA? **Default: no.**
- Q-5: the landing PR for `records/b1363` is yours to open; the commit subject and body avoid the word "merge" and the kit asserts it. **Default: as written.**

## UNMEASURED
- The B1351 and B1358 findings' own facts (TM1 to TM3, TB's rates) are relayed from the STATUS files and not re-run; TM2's two row positions are read, their tokens are not.
- The `deploy-demo.yml` path rule is relayed from the previous pass (`:30`), not re-read today; Job A re-reads it.
- Hosted CodeQL on main at the two merge commits: not read (the kit lists it as open).
- Whether another file defines `conversationSessions` or the two session methods at run time: only `server.js`, `jsonStorage.js`, `simpleDb.js` were read.
- The Jira comment bodies of older tickets beyond what `search` returns inline.

## Outside the fences
Nothing written outside the four files above and the session scratchpad (`pull.py`, `board.json`, `raw/`, `chk.py`, `hist.md`). No decision-queue access, no `briefs_staged`, no ledger, no WEDNESDAY/FRIDAY tree. Git in the project repo: none (all reads by `gh api -X GET`). One slip: two early shell commands carried `cd` and were refused by the hook; nothing ran. `gh api -X GET search/code` was used three times; it is a GET on the repository's code index, not a hosted host.
