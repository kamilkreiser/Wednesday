STARTABLE: YES (after Tuesday stamps S1-S7 and the last line; no kit fact is open)

# B1221 drafter report (SEAT-G321, tier-1 gate of b1206/hpsmpoc-feedback-review-held @ af6fd4c7)

## BLUF
Kit written, 57 long lines (dense; the 90-line target is met in lines, not in width). Shape follows B1198 (STATUS channel, REFUSE, RULE L, steps, severity, landing, stamp). Eleven requested judgements map to steps 2 (strings), 3 (5 outside paths), 4 (contract), 5 (authz), 6 (dispatcher), 7 (erase), 8 (Delete-on-UAT Note), 9 (migrations + SQL Server condition), 10-11 (CI-order, e2e, axe), 12 (plants), 1 and 13 (hygiene, claims).

## Facts re-measured (instrument; window 2026-11-03 about 17:00-17:20 AEDT, `date` 17:02:36 at start)
- Head `af6fd4c7...` = `gh api git/ref/heads/b1206/...` (control: the builder STATUS tail line match 1). main `f464376b...` unmoved. `compare`: ahead 1, behind 0, 35 files, 1 commit. Open PRs 0 (`pulls?state=open` length). Behind 0 means the merge tree equals the head tree; the kit makes the gate prove it, not assume.
- 35-path list printed from `compare` (`files.txt`): 29 in the builder's property plus the 5 named (`ContractTests.cs`, `UatOpenTests.cs`, `SqliteNonTransactionalMigrationsTests.cs`, `contract-drift.test.ts`, `SOURCES.md`) = 34, plus `api/src/.../README.md`, which is under the Feedback module (in property). Count to be re-derived by the seat.
- H111 branch `b1097/hpsmpoc-home-words-focus-ring` @ `f39ac80e`: 9 paths; `comm -12` with the 35 = 0; self-control `comm` of the sorted list with itself = 9 (an unsorted first try read 8, an artefact of sort order; resolved by sorting both).
- Pointers (grep -n over raw at the pin): `FeedbackModule.cs:63,:103,:169,:170-171`; openapi `:4,:2003,:2006,:2030`; `FeedbackReview.tsx:21,:24,:64`; the reused sentence at MAIN `AdminFeedback.tsx:83` (found; `FeedbackReview.tsx` is absent at main, control). Both openapi copies `cmp`-equal at the pin.
- CI (`ci.yml` at the pin, 679 lines, fetched by `gh api` raw): `on:` `:15`; `api-sqlserver-shard` `:165`; `api-sqlserver` `:353`; SQL Server pass predicate `:274-316` (all outcomes Passed, none skipped, 4 named tests per part, DB floor). No path filter, so the PR runs SQL Server.
- Ports 9740-9749: `lsof` over 9700-9709 and 9720-9799 and 9800: 0 listeners; word-bounded scan of all non-`.pre-` SEAT kits of 11-02 and 11-03 for 4-digit 9xxx: 9740-9749 absent (9739 and 9760 present around it). Control: `\b9690\b` hits B1218 (6). Live panes: tuesday, Datasec/Security-Composer-C85, Datasec/NexusAI-G320, Datasec/HPSM-POC-H111, Datasec/MPS-G318, fleet-monitor.
- Model: `models_latest.json:17` `claude-opus-5-5`; G1 `model-routing.md:108`; G-cap `:111`.
- Landing rule: `CLARIFICATIONS.md:3617` and `:3680` match 'The landing form is a head-pinned squash' (2 hits; absent-string control 0).
- Round count: no STATUS under Briefs/ is a gate of this class (the grep for 'held review|review page' hits old unrelated STATUS files; none a gate verdict on this class). Written as 0 of 2 before; the seat re-counts by program.
- `.tools/b1221` absent, `wt-b1221-*` 0; `.tools/b1198` has the four helpers.

## D-decisions
- D-1 Helpers and `node_modules` are copied from `.tools/b1198/` (it exists with `lock.sh`, `hv.sh`, `srv.sh`, `heartbeat.sh`); the builder's `.tools/b1206` is read-forbidden (its `hv.sh` was changed).
- D-2 SQL Server: docker is forbidden to every gate seat (B469/B1198 standing lines, DRAFTER_RULES fence 4). So NOT TESTED, written as a CONDITION of landing: hosted CI on the PR must be green on `api on SQL Server` (both parts). The seat also reads statically whether any new test skips on SQL Server, because a skip fails the CI predicate.
- D-3 Plant cap raised to 14 (builder 10; required list has 13 including two the builder did not run).
- D-4 `pr-title.txt` carries HPSMPOC-442 only if the last 10 merged PR titles show that convention (step 13); the squash files carry no ticket key.
- D-5 No verdict wording on the strip-like decisions: Delete-on-UAT is a Note with no recommendation.

## Q-questions for Tuesday
- Q-1 Port block 9740-9749: default accept. (9680-9689 is B1206's old block, avoided as asked.)
- Q-2 Hard stop and target are left to S5 (default: target 180, hard stop 270 minutes after the seat's Step-0 date, outer bound 22:00 AEDT).
- Q-3 Should the gate also run the existing UAT-open host check outside `UatOpenTests`? Default: yes, step 8 asks for it in-process only.

## UNMEASURED
- Whether the new tests skip on SQL Server (static read only, assigned to the seat). Hosted CI behaviour. The real UAT review copy. The 35-path census was printed but not diffed against the builder's property by a program here (the seat does it in step 1).
- The kit's `Briefs/` round-count grep was reasoned from file names only; I did not open the other STATUS files.

## Outside the fences
None. Writes: the two files only (scratch files in the session scratchpad, which is shared with other drafters; I did not touch theirs). Reads: DRAFTER_RULES, the B1198 and B1206 kits, the builder STATUS, `gh api -X GET` (compare, refs, raw ci.yml, openapi, CLARIFICATIONS, source files at the pin), `lsof`, `tmux list-panes`. No card, no ledger, no staged briefs, no fetch/pull in a project repo, no docker/az/ssh, no HTTP to a hosted host. The hook advisories about case-sensitive grep fired on my own pointer greps; each printed a positive hit, so none is a false zero.
