STARTABLE: YES (after the stamp; Q-1 and Q-3 are the soft cautions)

# B1229 drafter report -- SEAT-R159 (MPS records for MPS #155 / MPSCALC-359 and the two test-gap survivors of gate B1213)

Clocks (`date`): rules, template and gate files read from 19:2x; API and Jira reads 19:22:32 to 19:26:13 AEDT; final print 19:27:48 AEDT (Tue 3 Nov 2026). Kit: `briefs/2026-11-03_B1229_SEAT-R159_mps-records-359.md`, 71 lines (`wc -l`), 0 non-ASCII (python), 9 lines holding four underscores (8 slot lines + last line; control: `grep -c -F`). Slots file: 9 keys, all four underscores. No `.pre-stamp` written (the brief asked for three files; the coordinator makes it at stamp).

## BLUF
Two Jira writes: ONE test-only ticket for both gaps (or a hit comment) and ONE record comment on MPSCALC-359; no move (359 stays Backlog). One C-entry (C-91), BACKLOG rows, history, JIRA.md section; 0 transitions.

## Facts re-measured (instrument + control)
- Code main = `0d656f90...` (`gh api -X GET git/ref/heads/main`). `pulls/155`: merged true, base main, 3 commits, 5 files, +323 -7; control `pulls/99999` 404. `commits/0d656f90`: ONE parent `5a483a90...`; tree `43c57151...`; message ends "(#155)". `compare 5a483a90...main`: ahead 1, behind 0 (main IS the squash). merged_at 2026-11-03T08:03:06Z = 19:03:06 AEDT (`TZ=Australia/Sydney date -r`).
- The LOCAL checkout `2_Project_Files` does NOT have the object (`cat-file -t 0d656f90`: not a valid object name; its main stops at "Source validity (#2)"). I did not fetch. All squash facts are from the API (so the "git log" verification you asked for was done through `gh api`, read-only).
- Test blob head `e296f5b7` last commit (1 path) = squash blob `dbf741f3`; control base blob `fe5010d2` differs. Checks: 8 check-runs `completed success` by name; `ci` push run 41600428712 `completed success` attempt 1; `Push on main` success.
- Pointers at the squash (`contents?ref=` raw, `grep -n`): PurchaseCalculator.cs :583 (the `x is not null` guard), :398 (`input.Sections.First`), :321 (DUPLICATE SECTION); PurchaseRecomputation.cs :54; ENGINE.md :171 (X-45, silent on which copy). Both gate-cited lines (:583, :398) hold at the squash.
- Gate files (`grep -n`): B1213_STATUS :1 verdict, :97 GY1, :103 GY7, :124/:125 the two Majors, :126-:129 Notes, :119 record sentence, :135; residue.md :13-29; card-input.txt :4, :10.
- Root: main = HEAD = `d1f4b3c0`; CLARIFICATIONS 2526 lines, 91 headings, highest C-90 at :2517; `### C-91` 0 on the tree and on 63 of 63 branches (controls C-90 on 2, C-89 on 3). BACKLOG 4914, JIRA.md 585, history 1360. `.tools/b1229`, wt, lock, branch absent. df 351 GiB.
- Jira (project `j1211` helper, GET only, heartbeat patched out in scratchpad scripts): 381 issues, Done 144, Backlog 237, highest -381, sum check holds; MPSCALC-359 Backlog, 4 labels, one comment 40716; `B1229` 0 (control `B1196` 6). Symbol searches: `SitesWithDevices` 0; `ComponentQuantityRuleTests` 362/361/360/359/253; `PerSite` seven keys.
- Ports 9900-9999: 0. Word-boundary scan of 154 non-`.pre-` SEAT kits (11-02, 11-03) for R159, MPS-R159, b1229, B1229: 0 each (control R157: 3). Panes: tuesday, HPSM-POC-G325, HPSM-POC-G324, NexusAI-G323, fleet-monitor; no MPS-R pane.
- Model: `model-routing.md:98` C8 Sonnet first; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` default opus (level inside the quotes).

## D-decisions
- D-1: ONE ticket, not two. Reason: both gaps are rows in the one file `ComponentQuantityRuleTests.cs`, tests only, no product byte; the gate's fix shape (residue.md :24-29) and the card (card-input :4, "one ticket") treat them as one follow-up; one builder commit and one re-run of plants GY1 and GY7 proves both. They are not separate fixes. Caveat written in the kit: gap 2's rows pin today's "first copy" reading; if the product owner picks another copy that is a product change and its own ticket.
- D-2: The open product question ("which copy of a repeated section counts") sits in the ticket as a stated question, in the comment and C-entry as "not answered", and in `[B1229-OPEN-1]`; nowhere answered.
- D-3: No move and no C-79 application: gate record sentence :119 and your handover say 359 stays open.
- D-4: Mechanics copy from `.tools/b1196` (the only create-capable j) narrowed to 1 create + 1 comment, MAX_WRITES 2, no transition; read `.tools/b1211` for the narrowed form. Comment written after the ticket reads back, naming its key.
- D-5: Comment, C-entry, BACKLOG and history follow R157's strict word ban; the ticket follows MPSCALC-378's form (prefix `[B1213-1]`, "records seat", "lane and tier"), as R152's tickets did.
- D-6: C-entry heading carries "ticketed" shape of C-88; the review's NO GO verdict is stated as the review's and not regraded.

## Q-questions for Tuesday
- Q-1: Does the stricter R157 word ban also apply to the ticket body? Default: no (ticket follows MPSCALC-378's form, which names the records pass and "lane and tier").
- Q-2: Finding frame: the kit limits finding ids to those B1213_STATUS prints (B1213-1..6, B1207-1..5 and -7..12); B1207-6 is not named there. Default: out of frame, the seat says so.
- Q-3: Should 359's four clauses being 4 of 4 MET (:116-:118) prompt a Done move under C-79? Default: no, stays Backlog per :119 and your handover.
- Q-4: Ticket title prefix `[B1213-1]` (B1196 used `[B1186-R2]` = gate id + finding). Default: as written.

## UNMEASURED
Code-scanning count on the squash; symbol-search hits read whole (the seat does it); the new key (predicted MPSCALC-382); whether the ruling changed after your relay; the hosted state; index counts after the seat's write; B1207 ids not printed by B1213_STATUS.

## Outside-the-fences disclosure
None breached. Reads: DRAFTER_RULES, the four B1211 files, B1196 kit (grep and pre-stamp slices), B1211 STATUS tail and header, B1213 STATUS/residue/card-input, CLARIFICATIONS/BACKLOG/JIRA/history lines, `.tools/b1196` and `.tools/b1211` file names and helper headers/code (read only), `gh api -X GET` under the MPS `GH_CONFIG_DIR`, Jira GET via `j1211` from three scratch scripts in the session scratchpad (no write; heartbeat patched out so no file was written under `.tools`), raw copies of 4 squash files into the scratchpad. No `decision_queue.sh`, no `fleet/briefs_staged`, no scoreboard, no `_ledger.md`. Two Bash calls were refused by hooks (a `cd`, and zsh word-splitting) and re-run clean.
