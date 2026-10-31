STARTABLE: YES (all three jobs; batch 2 is 15 keys by a stated test, not the relayed 16)

# B1004 drafter report (SEAT-R100, MPS records: C-79, MPS #133, batch 2), 2026-11-01

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1004_SEAT-R100_mps-records-done-rule-c-entry-133-batch2.md` (shape of the B987 kit; its stamp slots left as four underscores, 6 lines with the pattern, control: the file's own slot lines).

## BLUF
- C-number to add: **C-79** (highest at root main `e3e2871c` is C-78, 79 headings, control `### C-77 ` found once; no local `refs/heads/` entry holds a `### C-79`). Form copied from C-78 (line 1620): heading `### C-79 -- <question>? (the product owner's 2026-11-01 ruling)`, then Source / words verbatim / Settles / Delivered / Not settled / Note on order / C-scan / close. The kit writes what the rule permits and does not as the coordinator's reading, not his words.
- Keys: job 1 = 0 Jira keys; job 2 = 2 (MPSCALC-254 Done-eligible, probably held by its own "purchase group path follows MPSCALC-252" text; MPSCALC-256 comment only by instruction); job 3 = **15** (relayed 16). Total 17 comments, at most 16 moves, 33 writes cap. MPSCALC-252, -253, -255, -258, -259 excluded by name (B1000 builds 252/258/259).
- Model row: Sonnet, C8 `model-routing.md:98` (C7 `:97` for the text shapes), `claude-sonnet-5-5` (models_latest.json line 23), `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes. Ports: none.

## Facts re-measured (instrument; control)
- Card (read once, `decision_queue.sh show <exact id>` into scratch, 13 lines; the id line is the control): status ruled, choice `a`, `ruled_ts` 2026-11-01T00:20:04+11:00. **The ruling time you gave (00:18:56 AEDT, live board) differs from the store time by 68 seconds**; the kit relays 00:18:56 from the stamp and names the store time as a note. Option (a) text is "Done means merged to main, the same as Composer"; default was "Nothing moves".
- Root: `rev-parse main` = HEAD = `e3e2871c2953bf0285e079e3c82f7d2bfb54a5c8`; remote count 0; 41 local branches; `status --short` 818; numstat BACKLOG +1934, JIRA +328, `5_Project_History/history.md` +412 (history.md is under `5_Project_History/`, not the root); `.tools/.git-lock`, `.tools/b1004`, `.tools/wt-b1004-records` absent; `records/b1004` absent (rc 1). `R100` word scan of briefs: 0 files (control `B1003`: 3 files). `B1004`: 0 files.
- Code: main `5d96a3dc` (`git/ref/heads/main`), open PRs 121, 120. `pulls/133` merged, +731 -22, 9 files, 3 commits, squash `5d96a3dc`, 8 of 8 check-runs success, `compare/5d96a3dc...e027ebd0` = `behind` (so #133 is not in the hosted build); `pulls/9999` and `compare/nonsense...main` 404.
- Batch-2 PRs 55, 56, 58, 59, 60, 61, 62, 64, 65, 66, 67, 68, 69, 71, 72 (and 95, 96 for the later comments): all merged, all `ahead` of main and of `e027ebd0` (control: #132 vs `e027ebd0` = behind). Check-runs 8/8 success on all but **#59 (6 success, 1 failure)**, which carries MPSCALC-164 and -165 (the same red run B987 recorded).
- Jira (read-only urllib reader of `.env` in-process; 356 issues, 480 comments, `status`: Backlog 330, Done 26): the batch-2 test "open ticket with a comment starting `BLUF: merged to main in PR #` and ending `Records seat B164.`, not a batch-1 key" matches 36 comments, 21 in batch 1 (control: the pattern finds exactly the 21 B987 keys), so **15 keys**: MPSCALC-105, -136, -141, -147, -151, -153, -163, -164, -165, -166, -168, -170, -174, -182, -183. MPSCALC-254, -256: Backlog, 0 comments, no prior record.
- Gate lines: B980 line 1 NO GO round 1 of 2 @ 1d49328 (Blocker B980-1); B988 line 1 GO WITH FINDINGS round 2 of 2 @ 30ea76d, `VERDICT:` line 209 (B980-1 and B980-3 closed). B988 FOR TUESDAY: "MPSCALC-256 is built for rental only, the purchase part waits on MPSCALC-255"; NOT TESTED: "the purchase group path (MPSCALC-252, not built)".

## D-decisions
- D1 One branch, one commit holds C-79 and the coordinator section together (both appended to CLARIFICATIONS.md after B987's section); the three other root files stay uncommitted as every records seat before.
- D2 The key list of batch 2 is derived by the stated test and the kit says the 15-versus-16 gap openly; no guessed sixteenth.
- D3 Write cap 33 = 17 comments + 16 moves; the client allows transitions for 16 keys, never for MPSCALC-256.
- D4 Copy the narrowed scripts from `.tools/b987/` (B987's Corrections: it rewrote them instead of narrowing the B873 ones and said so); 4b uses the wildcard and full-sha queries, because the plain 8-character query is blind (B987's control).
- D5 Hosted sentence is key-specific: 14 keys "an ancestor of the hosted build (relayed)", MPSCALC-254/-256 "not in the build the project records as hosted (relayed)". The Jira comments never claim deployed.

## Q-questions for Tuesday (each with a default)
- Q-1 The sixteenth batch-2 ticket: the sweep's 16 is not reproduced (the B164 test gives 15). Default: take the 15, name the gap, no guess. (Candidates seen: MPSCALC-158, a gate-notes comment with no merged PR; MPSCALC-150, whose landing is a later pass.)
- Q-2 `CARD-REF` slot: you asked for the card id in the C-entry. Rule 7 keeps ids out of kit text and C-78 left its id out on purpose, so the kit has a stamp slot with default NONE. The id to put in it if you want it recorded is `mps-done-rule-merged-tickets-1031`. Default: NONE (follow C-78).
- Q-3 Ruling time in C-79: 00:18:56 AEDT (your relay) with the store time 00:20:04 AEDT noted. Default: as written.
- Q-4 MPSCALC-254: if the seat reads every clause MET it moves; I expect the "purchase group path follows MPSCALC-252" text to hold it. Default: the seat decides from the table; any doubt means comment only.
- Q-5 MPSCALC-165 and -174 (second landing comments on a later pass, #96): batch 2 includes them and lets the later comments count only where the #96 diff shows it. Default: keep them in batch 2.
- Q-6 TIER2-ATTEST now covers three keys (-153, -165, -183), of which only -153 is truly without a gate line. Default: YES.
- Q-7 `DONE-SLOT` default MOVE-TO-DONE, now on the ruling filed as C-79.

## UNMEASURED
No write of any kind. Not measured: the hosted state (relayed); the sixteenth ticket; the gate STATUS lines behind the batch-2 citations (landing-comment citations read, gate files not); the full Acceptance sentence of the 15 beyond what the dump shows; the cause of the 68-second time difference; M53's progress (a later landing moves code main, which the kit calls information).

## Outside-the-fences disclosure
- Wrote only the kit and this report; scratch under the session scratchpad only (`ro_dump.py`, `ro_desc.py`, `gh1.sh`, `a1-a5.py`, `g1.sh`, the dumps `d/all.json`, `d/desc.json`, `card.txt`).
- Read the project's `.tools/b987/j987.py` header and the B987 STATUS and kit (named in the brief) and `BACKLOG.md`/`JIRA.md`/`CLARIFICATIONS.md` lines named in the kit; B980 and B988 STATUS (first lines, VERDICT, FOR TUESDAY); the B1000 kit and drafter report; `model-routing.md` lines 90-100. I wrote my own Jira GET reader (urllib, GET only, token never printed) instead of invoking the project helper, as the B1000 drafter did.
- The card was read once by exact id; `decision_queue.sh list` was not run.
- Hooks refused three first commands (a `cd` twice, a bare `====` separator, an unquoted `$G` in command position); all re-issued without them. One Bash call ran `git for-each-ref` over all 41 local branches (READ verbs, `--no-optional-locks`) to prove no C-79 exists anywhere.
- Two of my own mistakes, fixed in the kit before this report: a garbled sentence about a label (now "the needs-ruling label on MPSCALC-153 stays") and an over-long seat-name control (now "the same listing finds B1003 in 3 files").
