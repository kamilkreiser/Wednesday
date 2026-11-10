# B1486 DRAFTER REPORT: Composer records kit R207 (the follow-ups of B1475)

Drafted 2026-11-11 07:22 to 07:35 AEDT by a read-only Agent-tool drafter. Nothing was written in the Composer folder, in Jira or on GitHub.

## BLUF
- **Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1486_SEAT-R207_composer-records-1111.md`. It has 102 lines and sha256 `716b8be5645d1e0bf688443055d567c11fc7be6dce0792341e8a3f5a32fe7479`. The `.pre-stamp` copy is identical (`cmp` rc 0). It has 15 slots plus the last line, so 16 four-underscore runs.
- **Shape:** it touches at most three Jira keys (PCOMP-113, PCOMP-62, PCOMP-114). Each key is on the list only if its slot puts it there. The comment texts are written into the kit word for word, so Tuesday approves the exact bytes (row C7). The seat checks every fact in a text at source before it posts. If a fact does not match, the seat stops; it never rewords. The records are one C-134 entry, one `JIRA.md` bullet and one history entry. The BACKLOG pointer fix uses the form slot ROW-FORM picks. It is one commit and one `--no-ff` merge. Level is Sonnet.
- **Every slot default is the safe choice.** If Tuesday stamps nothing beyond the clocks, the seat fixes the two pointers in C-134 only and touches no Jira key.
- **The six decisions for Tuesday and my recommendations:**
  1. **PCOMP-113: MOVE.** Kam's 15:51 ruling (option c) is the ticket's third Done-when option. The option text on the card itself said "PCOMP-113 closes on your ruling". The two remaining clauses are met because nothing was changed.
  2. **The run ruling: ACCEPT** C91's capped run, read at main. The ruling must name its two departures from the ticket's wording: no run at the base, and the busy loops ran inside the container.
  3. **PCOMP-62: MOVE.** Its own row #422 names the coordinator's ruling as a way to close it.
  4. **PCOMP-114: comment only (ROW428 = NONE).** Accepting the run meets clause (1). But row #428, which asks whether the clock change is an acceptable fix, is Kam's to rule and is still open. Comment 40667 and C-119 both list it as open beside clause (1). If you want it closed, that is a card for Kam, not a stamp.
  5. **MINOR-1: rule it accepted after the fact, no rework.** Suggested text is under D5.
  6. **ROW-FORM: APPEND**, so the corrected pointer sits in the row where people read it. **REC-MERGE: MERGE**, as in the previous pass.
- **On (e): no by-name re-run of the 18 and 8 cells is owed.** I recommend not commissioning one now (reasons under D7).
- **On (f): every other R205 FOR TUESDAY item is OUT** (list under D8).

## What I measured (instrument and clock)
| Fact | Instrument, clock |
|---|---|
| Review file `2026-11-10_B1423_verify/VERDICT.md` (157 lines, sha256 `c9bc86f9...a5cb`, mtime 2026-11-10 07:20:46): Findings heading at `:143`; MINOR-1 at `:145` (sub-lines `:146`-`:147`); MINOR-2 at `:148`; MINOR-3 at `:149`; MINOR-4 at `:150` (items `:151`-`:153`); `:154` blank; Landing at `:155` | `cat -n`, `grep -n -i`, control `GO WITH FINDINGS` = 1; 07:23:07 |
| So row #476 should cite `:150` (not `:154`) and row #477 should cite `:145`-`:149` (not `:143`-`:152`). R205 is right. C-131's "`:143` to `:154`" covers the section plus one blank line; it is harmless and I left it | same |
| Rows #476 and #477 are at `BACKLOG.md:472` and `:473`; the highest row is #478 at `:474` | `grep -n`; 07:2x |
| Root records repo: main `094247e3`, no remote, nothing staged, the four record files clean, `records/b1486` absent (control: `records/b1475` resolves), C-133 at `:2541` is the highest entry, `JIRA.md` newest bullet B1475 at `:51` | `git --no-optional-locks`, `grep -c`; 07:28:07 |
| Code main is `c684e808`, unchanged since R205; open PRs #91, #86, #85 unchanged; PR #121's squash tree `f3c4bd4e` equals its reviewed head `b399bbfb`'s tree | `gh api -X GET` (control `pulls/9999` 404); 07:28:14 and 07:31:45 |
| `61b3a0c2...main`: 1 commit, which changes only `DEPLOY.md` and the two db test files. The blobs of `performance.test.ts` (`6a22aea3`) and `b116-s10-verify-dom.test.tsx` (`1cb63350`) are equal at `61b3a0c2`, `c684e808` and main. `f3cd568e...main` touches neither file (control `d70edf70...main` touches one) | `gh api` compare and contents; 07:28-07:31 |
| Jira, live: PCOMP-113/114/62 in Backlog with 1/2/4 comments (newest 40960/40961/40962) and 0 changelog entries; PCOMP-120/121 Done; transition 41 goes to Done | python `-I` GET (token never printed; scan of the output for `token` = 0); control PCOMP-9999 404; 07:24:01 |
| Done-whens quoted live (in the kit). PCOMP-113 offers three options, the third being "the product owner accepts them as unnamed", then "the 15 rows stay green; no product byte changes". Comment 40667 on PCOMP-114 says "Open: clause (1) and the ruling on row #428" | same |
| "The 15 rows" means the rows of `b778` at PR #105 | `B918_STATUS.md:1` ("b778 15 of 15"), `:250` |
| PR #121's review shows both db files at 170/170 at main and head | `B1422_verify/VERDICT.md:8` |
| C91's evidence: `DECISION_P-c.txt` `c0619a16...`, `fullnode_table.txt` `00975249...` (22 lines: 10 capped runs plus quiet, each with `owned rows 10 red 0`), `premise_table.txt` `3bf20aac...`, `compare_fullnode_quiet_vs_cap.txt` `c230c305...`, STATUS `18012ab5...` | `shasum -a 256`, `cat`; 07:2x |
| The decision store has card `composer-pcomp113-pin-paragraph-1110` as ruled c, `ruled_ts` 15:52:52+11:00, `delivered` null. Option c's detail: "No new operator words. The test still refuses all four; PCOMP-113 closes on your ruling." | python `-I` over `decisions.json` |
| No card in the store mentions PCOMP-114, PCOMP-62, row #428, row #422 or `npm ci` for Composer (0 of 1,333) | python regex over `decisions.json` |
| Seat id R207 is free across all 7 Datasec `Briefs/` folders and Tuesday's `briefs/` (control R205 = 1 and 2). No Composer pane exists (3 panes in all). No listener on 9400-9439. load1 8.80 | `ls`, `tmux list-panes`, `lsof`, `uptime`; 07:28:37 |
| Pointers the kit cites: `brief_seat.sh:24`, `models_latest.json:23`, `model-routing.md:97/98/110`, `status_watch.sh:56` (matches `READY B<digits>`) | `grep -n` |
| The kit's five Jira texts (including the two derived variants) are all ASCII and score 0 on names, internal words, seat codes, work numbers and paths. The one exception is `DEPLOY.md`, a repository file name the rule allows. All controls fire: `_by_Kam_`, `Tuesday`, `gate`, `B1486`, `C91`, `R207`, `C-134`, `product owner`. The clean control reads 0. Each derived-variant anchor occurs exactly once | python `-I` over the kit; 07:34 |

## What I could NOT measure
- **Whether C91's run is right.** I read its tables and hashes, but nobody has reviewed it and I re-ran nothing. Accepting it is a ruling, not a measurement.
- **Whether `DEPLOY.md` (the one file that differs between C91's tree and main) affects any row in the node chain.** I derived that it does not: the two owned files are byte-equal, and the C93 kit (`:51`, RELAYED) says the vitest workspace excludes `packages/db/test/**`. I did not run it.
- **The exact pane name of the HPSM R206 seat** (it is not launched yet).
- **Which time is right for Kam's tap.** The daily note and comment 40960 say 15:51; the store's `ruled_ts` says 15:52:52. It is probably the reconcile time, but I did not check.
- **Whether the 18 and 8 named cells still pass at main.** The cell list exists (`Briefs/2026-11-02_B1161_evidence/runs/ana.json`, 9,508 records with ids such as `Y3b-op-at38-L080`), and the generators are in `programs/`. Whether the strings regenerate exactly: UNMEASURED.
- **Anything hosted or deployed.**

## Open decisions for Tuesday (each with my recommendation and its evidence)
**D1. Slot PCOMP-113: MOVE.**
- The Done-when's third option is "the product owner accepts them as unnamed". Kam picked c, "Leave the paragraph as it is (recommended)". The option's detail on the card itself told him "PCOMP-113 closes on your ruling".
- "The 15 rows stay green": nothing changed. The pin paragraph is byte-equal (R205 measured it, and the kit re-checks it). The b778 file read 170/170 in the PR #121 review, at a head whose tree equals main.
- "No product byte": nothing was built.
- C-133's Forbid only covered the B1475 pass. C-134 records the new reading without editing C-133.
- After READY, Tuesday's own step: `decision_queue.sh --delivered` for the card (it is still `delivered: null`).
- Q-1 asks you to confirm "15:51".

**D2. Slot EVIDENCE-RULING: ACCEPT (your s264 lean, `NEXT-PICKUP-TUESDAY.md:75`).**
- *For:* the run is complete and has controls. The harness was proven able to fail: 1 ms timeouts went red 10 of 10. The capped runs have the same row sets as the quiet run. The evidence files are on disk with hashes the kit pins. Both test files are byte-equal at main today. Row #422 itself offers "the coordinator's ruling" as a way to close it.
- *Against:* no review has read it. Every earlier move in this project rests on a gate's cells. It also departs from the tickets' wording twice:
  - PCOMP-62 asks for "head and base", and the base was not run.
  - The busy loops ran inside the container, not on the host (comment 40359 draws that line).
- The kit makes an ACCEPT stamp name all three points (main as the head, no base, loops in the container) and refuses a vaguer one.
- Suggested slot text: `ACCEPT 2026-11-11 at <hh:mm>: the coordinator accepts the recorded capped run of 2026-11-10 at main 61b3a0c2 as the evidence for PCOMP-114 clause (1) and PCOMP-62 clause (2); main 61b3a0c2 stands as the head, no run at the base is required because the fix is on main and the base is the defect, and the busy loops inside the 2-CPU container stand for the ticket's busy loops.`

**D3. Slot MOVE-62: MOVE.** With D2 accepted, both clauses are met: clause (1) by comments 40345 and 40359 plus `untilVerdictBanner` at `:80`, clause (2) by the ruling. Row #422 names that route. Nothing else is open on this ticket.

**D4. Slot ROW428: NONE (so PCOMP-114 is commented, not moved).**
- Comment 40667 and C-119 list two open items: clause (1) and "the ruling on row #428". Row #428 says "NOT RULED, awaiting the product owner".
- C91's own FOR TUESDAY (`B1421_STATUS.md`, PCOMP-114 bullet) agrees: "The ticket still cannot be moved to Done without the product owner's ruling on row #428".
- No card exists for it (0 of 1,333).
- If you want PCOMP-114 closed, it takes one card to Kam: "PR #110 changed the clock to thread CPU time instead of raising the timeout; accept that as the fix?" Recommended answer: yes. Default if untapped: it stays open.
- Once he rules, his words go into ROW428 and the kit posts TEXT-114-MOVED.

**D5. Slot MINOR-1: rule it accepted after the fact, no rework.**
- What ran was the project's own CI install (`npm ci --ignore-scripts` from the lockfile, `scripts/ci.sh:116`, RELAYED from `B1423_STATUS.md:164`).
- The volume had no build cache at all (`:62`), so "cached layer, else STOP" could not be met on it.
- The review reproduced every number offline. PR #119 is landed.
- Suggested slot text: `MINOR-1 accepted, no rework: the step that ran was the project's own CI install from the lockfile with scripts off, the volume had no build cache to use, and the review reproduced every number with no network; MINOR-2 and MINOR-3 are count slips in a finished report that the review corrected: no action.`
- Outside this kit, a template change for you: future builder kits on a fresh volume should say up front what happens when no cache exists. C91 used a guard that kills the build if `npm ci` prints a run-time line (`B1421_STATUS.md`, J1c), which is the better rule.

**D6. Slot ROW-FORM: APPEND; slot REC-MERGE: MERGE.**
- The wrong pointer is in rows #476 and #477, where a reader looks.
- The project already has the form: rows #422 and #428 each carry an appended "Update <date> (C-n): ..." sentence.
- The kit's check removes the inserted sentence and requires byte equality with the old line, and requires every other line unchanged.
- With `NONE` (the default), C-134 alone carries the correction, as in the B1475 "nothing is edited" form. That is safe, but the rows stay wrong where people read them.

**D7. (e) By-name re-run of PCOMP-120's 18 cells and PCOMP-121's 8 cells: not owed by this kit; I recommend not commissioning one now.**
- A records seat runs no test.
- Both moves already say in Jira and in C-132 that the cells were not re-run by name, and the moves can be reversed.
- The cells' class is pinned by rows R13 (`:877`, including the writer-direct case at 1,000 pages) and R12 (`:812`), and the review probed 2,288 renders.
- Nothing is deployed.
- Neither review re-ran them (the PR #120 builder said the strings were not available, `B1420_STATUS.md:44`, `:233`). The cell ids are in fact kept in `B1161_evidence/runs/ana.json`, with the generators in `programs/`.
- So if you ever want the moves to rest on the clauses' literal words, a small tier-2 test kit can run them. The reason to buy it would be PCOMP-120's long-document cells (6 of the 18, 9 to 1,000 pages). I see no reason to spend on it today.

**D8. (f) Everything else in R205's FOR TUESDAY: OUT, each with its reason.**
- PCOMP-12: no Done-when. Writing one is your call and nobody asked (Q-2, default no).
- PCOMP-23 and PCOMP-123: they wait on PR #85 or a second render pass.
- PCOMP-98: clause (4) needs a fresh-seed run, which is builder work.
- PCOMP-116: its last verdict is NO GO, and PR #121 does not touch line 203.
- PCOMP-117: Done. R205's Correction 5 (its stale "line 769") is moot.
- Rows #473 to #475: NOT RULED, and no ruling is pending.
- The Dependabot PRs, PR #85 and the 23 alerts: not records work.
- R205's one `cd /tmp` slip: disclosed, nothing owed.

## Notes on the kit's form (differences from B1475)
- **The texts are fixed in the kit, not composed by the seat.** This satisfies "exact Jira text" and row C7. The seat may only fill in two times from the stamp. A wrong fact is a STOP, never a rewording.
- **The seat-code ban (`C91`, `R207`, `C-134`) must be case-sensitive.** Run case-insensitively, it hits the sha `c684e808`. R205 hit the same trap with `B` followed by digits against `b778`.
- **The seat may copy R205's scanner and Jira scripts** (`.tools/b1475/scripts/`, read-only) into `.tools/b1486/scripts/`. This saves the rebuild R205 had to do.
- **READY target is 60 minutes** (B1475 had 90), because this pass has at most 3 writes.
