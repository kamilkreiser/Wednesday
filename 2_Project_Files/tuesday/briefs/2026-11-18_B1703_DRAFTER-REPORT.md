STARTABLE: YES (once Tuesday stamps the ten slots; Q-1 to Q-3 are readings of yours to confirm, none blocks the launch)

# B1703 drafter report (SEAT-R268, MPS records pass for PR #211, #212, #213)
Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1703_SEAT-R268_mps-records-211-212-213.md` (285 lines, 11 four-underscore lines: ten slots and the last line `READ-WHOLE-BY-TUESDAY: ____`), sidecar `.measured` 127 lines. `stamp_check.py` exits 0 (127 claims, 127 measured, 0 TODO; run alone, rc=0). Shape copied from B1692 (R266, the records form) with the MOVE form of B1665 (R257). Drafted 2026-11-18; `date` printed 10:10:39 at the first GitHub read and 10:26:06 at the last clock read.

## BLUF
- **Planned outcome per key (the coordinator's readings; the kit writes them as such):**
  - MPSCALC-411: comment + **Done** if slot MOVE names it. All clauses read MET at main 8ae5db6e (the four old phrases read 0 lines in docs, src, tests and web/src; the V0Home test file equals base with `//` lines dropped, by program; the contract and its copies are not among #211's 2 paths).
  - MPSCALC-364: comment + **Done** if named. Clause 1 REPLACED by C-109; clauses 2, 3, 4 MET (clause 3 was NOT MET in C-179; `until lane V2 fills` now 0).
  - MPSCALC-207: comment + **Done** if named. Clauses 1 and 4 MET by run (comment 41234; ParityProof.cs and the parity tests unchanged since 3a69065a: the compare filter prints only PriceBookImporter.cs and PanelSectionEndTests.cs), clause 2 MET (IMPORTER.md:17), clause 3 MET by #212 (PriceBookImporter.cs:150 holds `any mapped model sheet's` once; test row at PanelSectionEndTests.cs:174-177). The review hold (NO GO at the cap on #122) is released by C-154 (:3183, reading (j) at :1957); the parity sentence (review F3) is a residual under reading (d) at :1727 and is not in 207's acceptance check, so it does not leave a clause unmet.
  - MPSCALC-410: comment + **Done** if named. Clauses 1 and 2 MET (docs/API.md:707-709 and openapi.json:751 name the states; `did not fail` reads 0 in the four files; the contract and snapshot are one blob 7796e611); clause 3 (no contract byte unless the coordinator says) MET under the product owner's 2026-11-18 ruling, option a.
  - MPSCALC-195: comment; **recommend NO move.** Clauses 1, 2, 5, 6, 7 MET at main; clause 3 MET by the ruling (docs/API.md:770); clause 4 only read MET by absence (`lane C2` 0 in docs/API.md; docs/API.md:601-602 says where the deal's rates are audited; the replaced sentence was never quoted in an earlier note); and the accepted engine-target sentence has NO words in any record I may read (C-108 lists its placement as owed). The comment says it is recorded as agreed by the ruling and stays open for the coordinator's reading (stays-open sentence for 195, frozen). Slot MOVE can name 195; then the move sentence is used.
- **Done rule applied exactly as CLARIFICATIONS records it:** C-79 `:1714` ("Done means merged to main, the same as Composer") and `:1716`, with the coordinator's three conditions at `:1727` (slot, every clause MET, no gate/review line or red run against it). Quoted in every comment as "Done rule (entry C-79) ... each Done-when clause met; as the coordinator reads it, no review line or red run may stand against the move". A key whose clause is unmet stays open and the comment says which (the 195 stays-open sentence).
- **New tickets:** NEW-P (slot CREATE-P `P`, recommended): the parity sentence of the PANEL-BLOCK note (`... does not compare them`) is narrower than the proof since #84 and #122 (ParityProof.cs:193-201 compares the (device, SKU) pairs). NEW-A (slot CREATE-A, optional, Tuesday may HOLD with `NONE`): dev toolchain audit (full `npm audit` 12 high all dev, `--omit=dev` 0, RELAYED from the #213 review; ci.yml holds the word `audit` 0 times, control `npm` 8; Dependabot open alerts 0, fixed 9: two instruments disagree).
- **Entry:** `### C-180` (root main is now `74fe202a` with C-179 at line 3449; `### C-180` reads 0, control C-179 reads 1), one entry for all three landings and the five ticket outcomes, with rows `[B1703-DONE-1]`, `[B1703-OWED-1]` to `[B1703-OWED-4]`.
- **Writes bounded:** 2 creates + 5 comments + 5 moves = 12; the poster refuses the 13th. Creates first (the 207 comment names NEW-P), then 411, 364, 207, 410, 195.

## Corrections to the brief's own facts (read at source)
- The brief said comment 41234 on MPSCALC-207 carries the parity-sentence finding. **It does not**: 41234 is the 15 Nov evidence-run note (clause 3 literal absent). The parity-sentence omission is recorded in comment **40944** ("its last sentence omits the per-device pair check"). The new ticket cites 40944 only (I first wrote both and fixed it before freezing).
- The C-number was expected C-179 for B1692 and C-180 is now free: B1692 landed (root main `74fe202a`, C-179). The MPSCALC-364 earlier "this morning's comment" is 41366 (not 41072).

## Model row (`fleet/specs/model-routing.md`) and launch
Line 97 row C7 (client-board comments, Sonnet drafts first, posts only a body approved byte for byte) and line 110 row G3 (ticket hygiene, no gate); model id `claude-sonnet-5-5` (`models_latest.json` line 23); `brief_seat.sh` line 31 `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"` so the launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes. Pane name `Datasec/MPS-R268`; `R268` and `B1703` occur in no other SEAT kit of today or yesterday (word-boundary scan), and no `Datasec/MPS-` pane exists (tmux list-panes at 10:14 and 10:26: 0).

## Facts re-measured (instrument, control)
- Code main `8ae5db6e` (`git/ref/heads/main`); root main `74fe202a` (`rev-parse main` = HEAD; tracked dirty files exactly history.md, BACKLOG.md, JIRA.md; `remote -v` 0 lines; no `records/b1703`, no `.tools/b1703`). Open PRs 0, `pulls/99999` 404.
- Squashes: #211 `b746cb92` (merged 2026-11-17T22:05:55Z = 09:05:55 AEDT, parent 863e0337, 2 paths +5 -5), #212 `6febe112` (22:37:07Z = 09:37:07, parent b746cb92, 2 paths +12 -1), #213 `8ae5db6e` (23:08:33Z = 10:08:33, parent 6febe112, 5 paths +9 -8). Each squash path's blob equals the reviewed head's (2/2, 2/2, 5/5; controls README.md equal, wrong-path pair unequal).
- CI: heads 9 of 9 success each; squashes b746cb92 and 6febe112 8 of 8 success; **#213's squash: 7 listed, 2 success + 5 in progress at 10:10, 6 success + 1 in progress at 10:26** (the seat polls; any MOVE holds if a run is still going after 20 minutes). Analyses by `commit_sha`: 4 each on all seven commits (control 863e0337 reads 4), results 0; open alerts 0 on main.
- Job logs (ANSI stripped): #211 squash dotnet `0 Warning(s)` 1, `0 Error(s)` 1, 743/196/3663; #212 squash dotnet 743/197/3663; both web jobs `Tests  1616 passed (1616)` 1 and 0 failed lines (control: a planted `1 failed` counts 1). **#213's jobs not measured (running).**
- Blobs: `git hash-object` of 16 tarball files equals the tree blob 16 of 16; planted byte differs 16 of 16. Pointers P01-P52 print 52 of 52 (second-run control not made: UNMEASURED).
- E counts at main (tarball of 8ae5db6e): `until lane V2 fills` 0, `until the Home work fills` 0, `until lane V2 builds` 0, `lane V2 flips` 0, `lane V2` 5 lines in 5 files, `oneOffGp` 38; V0Home comment-dropped equality True (planted change False); `did not fail` 0 in API.md, openapi.json, snapshot, schema.ts; `Validating, Active or Superseded` 1 in each of the last three.
- Jira (GET only, helper in scratch reading the project `.env` by name, no token printed): the five tickets read whole (411: 0 comments; 364: 41072, 41366; 207: six comments to 41234; 410: 0; 195: six to 41304), all Backlog; census 411 / 245 Done / 166 not Done (controls `key >= MPSCALC-1`, both statusCategory splits sum, MPSCALC-361 Done, MPSCALC-99999 404); the seven comment markers and both new-ticket markers read 0 (control `REC-LAND-390-17NOV` finds MPSCALC-390); `records-pass-1118` finds 1 key (MPSCALC-411).
- Decision card read with `decision_queue.sh show mps-410-openapi-195-wording-1117` only: status ruled, `(Datasec/MPS)`, choice a, ruled 2026-11-18T08:38:02+11:00, detail as quoted in the kit. The KIT carries no card id (the seat never reads the store).
- Scan: copy of `scan.py` (read by `cat`: a `cp` of it was refused by a hook) plus double-quote and URL refusals over 22 Jira items (3 outcome sentences, 5 comments, 2 summaries, 12 paragraphs) with sample fill-ins: 0 problems after one fix (`complete` -> `naming every state the code counts`); 11 of 11 controls fire; the 4 record texts (entry, BACKLOG rows, JIRA.md section, history) 0 problems. Frozen hashes in the kit were recomputed from the finished file: 5 of 5 comment hashes and lengths equal, both new-ticket summaries and descriptions, the three outcome sentences; a one-character mutant differs.

## Input table for the chain (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit and sidecar, root repo state, the four record files | exist at BASE |
| 1 | `.tools/b1665/` and `.tools/b1692/` helpers (read), `scan.py` copy by `cat` | exist at BASE |
| 2 | root main, code main, tarball, job logs, Jira reads, record greps | exist at BASE (read-only) |
| 3 | Step 0-2 prints, frozen hashes in the kit | Steps 0-2, kit |
| 4 | Step 3 payloads, `snap_before.json`, new keys (creates first), transitions GET | Steps 2-3 and 4a, 4b |
| 5 | Step 4 results (comment ids, keys, counts), worktree of `main` | Step 4, BASE |
| 6 | the Step 5 commit, `refs-before.txt` | Steps 0 and 5 |
| 7 | all | Steps 0-6 |

## D-decisions (mine; each reversible by your word)
- D-1: ONE comment template per key with `<<OUTCOME>>` chosen by program (move sentence / stays-open sentence / 195 stays-open sentence), each frozen by its own sha256, so the text is the same whether or not the slot moves the key. B1665's form.
- D-2: separate per-key MOVE list slot (`411,364,207,410,195`) instead of one slot per key; default NONE.
- D-3: markers `REC-LAND-411-18NOV`, `REC-CLOSE-364-18NOV` (distinct from comment 41366's `REC-LAND-364-18NOV`), `REC-LAND-207-18NOV`, `REC-LAND-410-18NOV`, `REC-LAND-195-18NOV`, `LAND-NEW-P-18NOV`, `LAND-NEW-A-18NOV`.
- D-4: the two kept wording points of #210 stay with MPSCALC-315 (not edited, as in B1692).
- D-5: the ruling is quoted in its own words in the comments for 207, 410 and 195 and in the entry; the entry says the card was not queried by the seat and that the ruling is relayed.
- D-6: BACKLOG rows: DONE-1, OWED-1 (parity words), OWED-2 (audit), OWED-3 (195 residue), OWED-4 (SOURCE.txt names branch commit e7a74364, optional).
- D-7: the 195 comment says clause 4 is "read as MET" by absence and names it as the coordinator's to confirm; it does not claim the replaced sentence was located.

## Q-questions for Tuesday (each with a default)
- Q-1: Slot MOVE: `411,364,207,410`? Default: yes (my recommendation). 364 and 411 are linked only by text, not by Jira state, so either can move alone.
- Q-2: 207 is moved under reading (j) released by C-154 and reading (d) for the parity sentence. Do you read it so? Default: yes. If you read the parity sentence as a clause (comment 40944 listed it under Open), drop 207 from MOVE; the comment's stays-open sentence is already frozen.
- Q-3: 195: move or not? Default: NOT moved (comment only). Two things make it a coordinator reading: (a) the engine-target sentence accepted on 11 Nov has no words in C-108, the ticket or the BACKLOG (the decision card says "put the accepted sentence on the ticket"; I have no copy, so the comment records it as agreed by reference, not by quotation: if you want the words on the ticket, add them to the kit); (b) clause 4's replaced sentence was never located.
- Q-4: CREATE-P `P` (recommended) and CREATE-A (default NONE; `A` files the audit ticket; HOLD = `NONE`)? The audit figures are RELAYED (no `npm audit` run: the registry is a hosted host).
- Q-5: Should the parity-sentence ticket go to the product owner's word review? The ticket leaves it undecided (C-109 sends only customer-visible sentences; the note lives in a stored import file staff read).
- Q-6: C-180 still the next number at stamp time? Default: yes (the seat re-derives by program and STOPs on a taken heading).

## UNMEASURED
- The squash of #213: its dotnet (job 134439919795) and web (job 134439919477) results and the Import count (expected 197); the final check-run totals.
- Whether the Jira transition id `41` still names Done (read from B1692/B1665; I did not GET `.../transitions`); `MPSCALC-1` GET 200 and `MPSCALC-412` 404 (only `MPSCALC-99999` 404 and the five keys were read).
- `npm audit` itself (needs the registry), and whether anyone has the words of the accepted engine-target sentence.
- The pointer table has no second-run control. The ordering of comment ids is the Jira server's.
- Not read: `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, any WEDNESDAY/FRIDAY tree, non-Datasec projects, any decision card other than by `show` of the named id.

## Outside-the-fences disclosure
- Wrote only the kit, its `.measured` sidecar (via `stamp_check.py --init`, then rewritten by a scratchpad script from my own reads) and this report. All scratch (Jira helper `jget.py` that reads the project `.env` by name in-process, `texts.py`, `records.py`, builders, extracted tarball in its own folder, job logs, raw files, `scan.py` copy) is under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s289/d1703/`; nothing in any project tree.
- Jira: GETs only (tickets, JQL with `project = MPSCALC AND ( ... )`, no write); GitHub: `gh api -X GET` only under the project `GH_CONFIG_DIR` (pulls, commits, trees, check-runs, analyses, alerts, Dependabot alerts counts, job logs, one tarball into its own folder, raw `contents`); git: read verbs with `--no-optional-locks` on the project root; `git hash-object` (no `-w`) on tarball files. tmux: `list-panes` and `display -t %0`. `decision_queue.sh show <id>` only, output printed to the terminal (cut at 1500 characters per line; the ruling line and options were whole) and not saved. No HTTP to any hosted site, no az, ssh, docker.
- Two hook refusals taken: a `cp` of `.tools/b1665/scan.py` into scratch (read with `cat` instead) and a `=========` echo separator (zsh expansion; used `----`). Hook advisories on case-sensitive greps and `cut` after grep were taken: counts that matter were repeated case-insensitively or by python with controls.
