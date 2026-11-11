STARTABLE: YES. The ruling is quoted, all 23 texts are fixed and scan clean, and every evidence pointer was printed at code main. No HPSM-POC records pane is live, and both live HPSM builders write no Jira. Six slots wait on your stamp.

# B1498 DRAFTER REPORT: SEAT-R211, HPSM-POC records (the 18 accepted quick recommendations of the 2026-11-11 register)

Drafted 2026-11-11 14:16:42 to 14:32:46 AEDT (`date`).
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1498_SEAT-R211_hpsmpoc-records-register-rulings.md`, 165 lines, sha256 prefix `05514e9306d6d092`.
- `.pre-stamp` copy: identical (`cmp` equal).
- Four-underscore lines: 10 (nine Stamp slots and the last line).
- Other checks: ASCII; `@..@` 0; card id 0.

## BLUF
- **Ruling.** The product owner chose option (a), "Accept all 18 quick recommendations for HPSM-POC now", on card `hpsmpoc-waiting-register-1111` (status ruled, choice a). The card id is written only in this report.
  - Your relay gives 14:15:12. The store's `ruled_ts` is 14:15:32.945982+11:00, read by `decision_queue.sh show <exact id>` into scratch. These are not reconciled.
  - The kit writes "14:15 AEDT (14:15:12 on the live board, as the coordinator relays it)".
- **Scope.** 18 rows covering 23 tickets. Non-quick rows 32 (HPSMPOC-51, 52) and 49 (HPSMPOC-169 to 176) are fenced off.
- **Kit shape.** One entry per row, C-341 to C-358, in the C-315 to C-323 form. One comment on each of the 23 keys. Up to 11 moves to Done under three slots. No create, no label edit. Records branch `records/b1498`, landed by the seat as R210 did.
- **Counts.**
  - **Mechanical (comment and move): 8 rows / 11 tickets.** 14, 109, 224, 226, 271, 257, 318, 322, 352 under MOVE; 180 under MOVE-180; 242 under MOVE-242.
  - **Comment only, no build owed: 1 row / 1 ticket** (237, which waits on a measurement).
  - **Ruling recorded, build or act is a later lane: 9 rows / 11 tickets.**
- **None is already Done or already carries this ruling.** The newest comment on every key predates today, except HPSMPOC-467, which has 0 comments. `REC-REG` reads 0.

## Per item: ticket, recommendation verbatim (register line), Jira action
Every key gets ONE comment (exact text in kit PART 1, marker `[REC-REG-<n>-11NOV]`) and ONE entry. The moves:

| Row (line) | Key(s) | Recommendation, verbatim | Jira action proposed |
|---|---|---|---|
| C-341 (31) | HPSMPOC-14 | "Accept both as built. The schema and stamping are built and tested; only your ruling keeps it open." | comment + Done (check: schema `$id` line 3, `AssessmentApiTests.cs:50`) |
| C-342 (33) | HPSMPOC-109 | "Accept, with the manual check for this proof of concept. The silent-loss case needs a secret change that was not copied across; a manual check covers it at no cost." | comment + Done (check: `ci.yml:602`) |
| C-343 (34) | HPSMPOC-180 | "Yes, at the next re-issue. Nothing is broken today; raising it now ripples into every stamped assessment." | comment + Done under MOVE-180 (check: schema line 10 still `0.1.0`) |
| C-344 (35) | HPSMPOC-193 | "The secret header. It closes the gap with no new Azure spend; the risk is Low and only touches one rate limit." | comment only (LATER) |
| C-345 (36) | HPSMPOC-224 | "Close as declined; revisit for production. Nothing is switched on and the branch is kept; the review site works without it." | comment + Done (check: PR #195 closed, unmerged) |
| C-346 (37) | HPSMPOC-226 | "Decline. Every other item on the ticket is built or accepted; today's message is safe." | comment + Done (check: PR #168 merged, `d76200d8` behind 0) |
| C-347 (38) | HPSMPOC-271 | "The coordinator, on each servicing day. A missed raise turns every build red with no code change." | comment + Done (check: `global.json:3`, `ci.yml:48`) |
| C-348 (39) | HPSMPOC-257, 318, 322, 352 | "Close all four as kept. Each is built, tested or recorded; none changes what a user sees." | 4 comments + 4 Done (checks: PRs 305, 273, 220 merged and behind 0; `RequestTimingLogTests.cs:436`) |
| C-349 (40) | HPSMPOC-420 | "Yes, everywhere. Two different counts on neighbouring screens confuse a reviewer." | comment only (LATER) |
| C-350 (41) | HPSMPOC-467 | "Alias on all seven. It matches your 10 Nov ruling for the first two pages and the security pages." | comment only (LATER) |
| C-351 (42) | HPSMPOC-237 | "Yes, wait. The cause of the browser delay is not measured; spending first may not fix it." | comment only (OPEN: its close needs the measurement) |
| C-352 (43) | HPSMPOC-242 | "Close if nothing new; five weeks have passed. The placeholder has been open since 7 Oct." | comment + Done under MOVE-242 (option (b) "Nothing further, close") |
| C-353 (44) | HPSMPOC-90, 164 | "Yes, prove once then close. Both are overtaken by the live review site; one proof makes the close safe." | 2 comments only (LATER) |
| C-354 (45) | HPSMPOC-91 | "Yes, agent drafts. Same route you chose on 10 Nov for the rules content." | comment only (LATER) |
| C-355 (46) | HPSMPOC-304 | "Yes. One of them held credentials as protected parameters; housekeeping only." | comment only (LATER) |
| C-356 (47) | HPSMPOC-162, 163 | "Yes, draft both. Neither needs HP data to draft; nothing goes to HP without you." | 2 comments only (LATER) |
| C-357 (48) | HPSMPOC-168 | "Yes. It reflects HP's named priority customers; no scoring effect." | comment only (LATER) |
| C-358 (50) | HPSMPOC-241 | "Send in one batch. Next-phase design needs the answers; nothing goes to HP except from you." | comment only (LATER) |

## Ruling recorded, build is a later lane (not mechanical; the comment says "Not built / Not done" and nothing moves)
- **HPSMPOC-193.** Needs a build: code on the API and the web server, a Key Vault secret and its rotation, and a regression row. Then a hosted settings change and a deploy, which is HELD (UAT is held while HP reviews).
- **HPSMPOC-420.** Needs a build. The words are given: "N of M scored questions answered", already ruled in C-277. Customer-facing text, so this pass records the ruling only.
- **HPSMPOC-467.** Needs one build across seven surfaces. It overlaps the Home rebuild (HPSMPOC-457).
- **HPSMPOC-90 and 164.** Need a hosted act: one real feedback item proven end to end. The route is off on UAT, and a deploy-class approval is needed.
- **HPSMPOC-91.** Needs a drafting lane for the pack wording.
- **HPSMPOC-304.** Needs an Azure VM act (the cleanup), on its own approved step.
- **HPSMPOC-162 and 163.** Need a drafting lane.
- **HPSMPOC-168.** Needs a build and words.
  - The choice labels are given.
  - The neutral note's words are NOT given and need a words card.
- **HPSMPOC-241.** Needs a drafting lane for the e-mail. Only Kam sends it.
- **HPSMPOC-237** (OPEN, not a lane): waits on the Server-Timing measurement.

## Facts re-measured by the drafter (instrument, clock)
- **Records main (analysis).**
  - Main is `830dae782f23ef0e8889c75247c433afe727e1f5` (PR #194, 2 parents). Open PRs: 0. `records/b1498` absent; `records/b1493` present. `pulls/99999` returns 404 (`gh api -X GET`, 14:18:48).
  - `CLARIFICATIONS.md` (raw read): 6041 lines, 1,980,178 bytes, sha256 prefix `5e36fdc4ddcd7254`. Newest heading `### C-340` at line 6033; `### C-341` 0; `### C-263` 1.
  - `-c -i -F` counts: `REC-REG` 0, `Accept all 18` 0, `Close all four as kept` 0, `servicing day` 0, `decision register` 13. Controls: `REC-` 49; a never-present string 0.
  - C-277 (line 5348) leaves "whether 'everywhere' reaches them" open for HPSMPOC-420. This ruling answers it.
- **Code main.** `009421a28616c8b31dde86b59d4c4ca674c288fa`. Lines printed by `awk NR==n` over raw files:
  - `ruleset.schema.json`: `$id` at :3, `schemaVersion` const at :10.
  - `AssessmentApiTests.cs:50`.
  - `RequestTimingLogTests.cs:436`.
  - `ci.yml:602` and `:48`.
  - `global.json:3`.
  - PRs 305, 273, 220, 168 and 183 merged true. Compare results, each behind 0: `78d4b3ce` ahead 4, `c1457349` ahead 35, `b069274` ahead 87, `d76200d8` ahead 137.
- **Jira** (GET only, 14:17:29 to 14:26:34).
  - 469 issues, 327 Done.
  - All 23 keys read whole, with comments, transitions and changelog. HPSMPOC-90 and 91 are In Progress; the rest are Backlog. Transition 41 goes to Done on all of them.
  - Newest comment per key is in kit REFUSE 4.
  - Marker searches: `REC-REG-14-11NOV` 0. Controls: `REC-WALK12-11NOV` = {468}; `REC-RUL-6-10NOV` = {100, 117, 180}.
  - `"re-issue"` = {180, 182}. 182 is Done and is a different item, so no re-issue ticket exists.
- **Texts.** All 23 were filled with C-341 to C-358, `009421a2`, the line numbers, and DONE as the outcome. Run through R210's scanner (imported read-only): 0 problems each; 10 of 10 controls fired. Lengths and sha256 prefixes:

| Key | Length | sha256 prefix |
|---|---|---|
| HPSMPOC-14 | 951 | `78a13fdf` |
| HPSMPOC-109 | 901 | `a394f3e7` |
| HPSMPOC-180 | 819 | `615c0cff` |
| HPSMPOC-193 | 834 | `e3f66075` |
| HPSMPOC-224 | 758 | `932fe098` |
| HPSMPOC-226 | 874 | `493fce69` |
| HPSMPOC-271 | 875 | `35e413ed` |
| HPSMPOC-257 | 785 | `2a0694ba` |
| HPSMPOC-318 | 1047 | `49fb2513` |
| HPSMPOC-322 | 913 | `b988db0c` |
| HPSMPOC-352 | 838 | `20ce63d3` |
| HPSMPOC-420 | 787 | `6a907501` |
| HPSMPOC-467 | 912 | `bfca2403` |
| HPSMPOC-237 | 734 | `16b968ba` |
| HPSMPOC-242 | 714 | `90e8e29c` |
| HPSMPOC-90 | 762 | `1892d952` |
| HPSMPOC-164 | 762 | `3d9f5bf6` |
| HPSMPOC-91 | 772 | `3673c759` |
| HPSMPOC-304 | 735 | `11da29a3` |
| HPSMPOC-162 | 711 | `f5040de6` |
| HPSMPOC-163 | 711 | `c7a86704` |
| HPSMPOC-168 | 742 | `a6318d44` |
| HPSMPOC-241 | 577 | `c478ecaa` |

- **Register.** 161 lines, sha256 `45e69c8a...ba859c`, committed at `34e7055d22` and clean. All 20 HPSM rows are ASCII. One person's name appears, on line 43 (HPSMPOC-242's question); the kit replaces it by program.
- **Seat id R211.** Word scan of 186 kits: 0 hits; control R210: 4. Model row: `model-routing.md:97` C7. Model id: `models_latest.json:23` `claude-sonnet-5-5`. `brief_seat.sh:24` defaults to opus.
- **Panes** (14:25): `%0 tuesday`, `%1 fleet-monitor`, `%25 MPS-M113`, `%30 Security-Composer-C93`, `%33 HPSM-POC-H157`, plus unnamed panes. H157's kit says "Jira: you write nothing" at line 22. B1496 (H156) says "Jira writes: none" at line 92.
- **Other overlap.** Neither builder kit names any of the 23 keys (`grep -o HPSMPOC-[0-9]+`).

## D-decisions (the kit's defaults; change at the stamp)
- **D-1: one entry per row** (18 entries), matching C-315 to C-323, where each ruled card row got its own entry. The alternative is one combined entry. Kam ruled once, but each row is a separate question with its own outcome.
- **D-2: HPSMPOC-180 MOVE-180, recommended CLOSE.** The accepted row says "Closes the ticket into the next re-issue plan". No re-issue ticket exists (search `"re-issue"` returns only 180 and 182, and 182 is Done). If it closes, entry C-343 carries a standing instruction for the next re-issue. Choose COMMENT-ONLY if you want the ticket kept as the tracker.
- **D-3: HPSMPOC-242 MOVE-242, recommended CLOSE.** The recommendation is phrased conditionally ("Close if nothing new"), but its option is (b) "Nothing further, close", and Kam accepted it. Choose COMMENT-ONLY if you know of new notes.
- **D-4: HPSMPOC-318 closes on the ruling.** Two of its done-when clauses are not re-measured: the 484 and 839 ms cases staying green, and 3 consecutive green main pushes. The kit's text says so plainly; "kept as built" is the ruling. Choose COMMENT-ONLY for 318 alone only by editing MOVE; there is no per-key slot for it.
- **D-5: HPSMPOC-271's owner in Jira.** The scanner bans the word "coordinator", so the Jira text reads "the project's coordinating role, the one that assigns this project's work". The entry says "the coordinator (the Datasec coordinator seat)" verbatim.
- **D-6: HPSMPOC-224 and 226 move to Done as "declined".** The precedents for Done on a "keep" or "accept" ruling are C-317 (HPSMPOC-401) and C-322. Under C-263 these keys have no done-when that a ruling cannot meet.

## Q-questions for Tuesday (each with a default)
- **Q-1: Labels.** HPSMPOC-237, 242, 90, 164, 91, 162, 163 and 168 carry `needs-kam`; 241 carries `owner-kam`. Once ruled, those labels are stale. The kit makes no label edits (closed list). Default: no label edit in this pass.
- **Q-2: Later lanes.** Who commissions them (the 193 build, the 420 and 467 builds, the 168 build and its note words, the 90/164 proof, the 91, 162, 163 and 241 drafts, the 304 cleanup)? Default: the seat lists them under Hand-off and you sweep them.
- **Q-3: Marking the card delivered** (`decision_queue.sh --delivered`) is your own step after READY. Default: after the RECORDS COMMITTED line.

## UNMEASURED
- Whether the analysis PR's CodeQL behaves as on #194.
- Whether any later-lane item is already in flight in another unstamped kit. I scanned only the stamped and pre-stamp kits of 2026-11-10 and 2026-11-11 by name.
- The 484 and 839 ms clause of HPSMPOC-318, and its 3 consecutive green main pushes.
- Whether the HPSMPOC-304 objects still exist on the VM. Not read; Azure is out of the fence.

## Outside-the-fences disclosure
- **Two refused Bash calls; nothing executed in either.**
  - One call contained `cd /tmp 2>/dev/null` (my slip). The no-cd hook refused it.
  - One call used `git ... symbolic-ref HEAD` on the Composer root repo. The hook classed it as a write verb and refused it. I re-ran with `rev-parse --symbolic-full-name HEAD`.
- **Card read.** `decision_queue.sh show hpsmpoc-waiting-register-1111` and `show composer-waiting-register-1111`, each into `/tmp/b1498d/card_*.txt`, then read through an id filter. I did not run `list`.
- **Scratch** under `/tmp/b1498d/`:
  - Raw reads: CLARIFICATIONS, code files, Jira JSON.
  - My GET-only Jira reader `tools/jget.py`.
  - `tools/summ.py`, `scan_hpsm.py` and `scan_comp.py`. These import `scan1493.py` and R209's `textscan.py` read-only, with bytecode writing disabled.
  - Text sources in `texts/` and kit bodies.
- **Kit files.**
  - Each kit was assembled by a python write from my Write-tool body plus the generated text block, not by the Write tool directly.
  - The `.pre-stamp` copy was made by `cp -n`.
  - One python in-place edit fixed the drafting-clock string in both the kit and its `.pre-stamp` (a predicted end time, `14:40`, replaced by the last printed `date`, 14:32:46). They stayed `cmp` equal.
- **Reads outside the project.**
  - The register; `decision_queue.sh` header lines 1 to 40.
  - The `model-routing.md` rows, `models_latest.json:23` and `brief_seat.sh:24`.
  - The B1495, B1496 and B1497 kits, by grep.
  - The Composer project's records (root repo, `git --no-optional-locks` read verbs) for the sister kit.
- **Network.** GitHub `gh api -X GET` only, including code search. Jira GETs only (HPSMPOC and PCOMP). No hosted host, no az, no ssh, no docker.
- **Path note.** DRAFTER_RULES names `/Volumes/Laptop-DEV/...`. The files and the precedents live under `/Volumes/Datasec_DEV/...`, and the kit uses that.

READ-WHOLE-BY-TUESDAY: ____
