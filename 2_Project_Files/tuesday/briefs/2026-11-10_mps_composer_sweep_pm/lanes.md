# MPS Calculator and Security Composer: completable-tickets sweep, afternoon pass (read-only)

Drafted at 2026-11-10 15:01 AEDT (`date` printed 15:00:56 in the last action before this file was written). This file supersedes `../2026-11-10_mps_composer_sweep/lanes.md` (03:13, stale: most MPS lanes and Composer C90/C93 have landed since). Drafter read only: Jira boards through each project's own `.env` read in-process by a `python3 -I -B` reader (GET only, no token printed), `gh api -X GET` under each project's `.gh-config`, `git --no-optional-locks` read verbs over the two root records repos, `tmux list-panes`, `lsof`, `ls`. No write of any kind outside the files named in the report. Code facts are read at origin: MPS main `dad902441014bda81d4eed39dc9a6bcea1439989` (`git/ref/heads/main`, 14:51), Composer main `61b3a0c21384b6c3cf755733e1b4d937a35e47a5` (`git/ref/heads/main`, 14:51). The local checkouts are stale; they were not used for code facts.

## BLUF

- **MPS Calculator: 2 build lanes, both kitted; 1 more lane named and not kitted (cap of two).** M111 (B1471): `docs/API.md` sentences and the generated-copy header line (MPSCALC-178 clause 2, the gate's two feedback sentences, the header left naming an unreachable commit), size S, docs plus two generated lines. M112 (B1472): `scripts/deploy-from-ci.sh` and its test file, the open half of MPSCALC-203 (directory mode, retry count, re-read before deploy), size M, edited and tested against fakes, never run. Named, not kitted: M113 = MPSCALC-334's three untested stub operations (`web/src/api/stub/stubApi.test.ts`, test only, size S).
- **Security Composer: 0 lanes qualify** (91 open non-epic tickets, conservation below). Four are already in flight (C91 and C92, B1421 and B1422); 7 are owed records (R205); 19 carry the `held` label and 2 `needs-kam`; 29 are sample-policy rows that depend on the L1 to L3 content release (held PR #85); the other 30 each carry a named reason (VM or hosted host, product-owner token or words, code that exists only on the held PR #85 branch, design not ruled). No kits C94 or C95 are written.
- **The records backlog is the biggest owed work on both boards.** MPS: R204's closed list holds 68 distinct open keys (the 79 keys of RECORDS-A, RECORDS-B and LANE, less 11 old body-only mentions); Jira still reads all 225 open as Backlog. Composer: 7 keys are owed (PCOMP-12, 23, 98, 116, 120, 121, 123). Both records kits (B1470 and B1475) are written beside this file.
- **Two corrections to the 03:13 sweep, measured today:** (1) its PR-title regex missed three keys named by MPS #68's title ("MPSCALC-145, -146, -148, -139, -153, -185"): MPSCALC-139, -153 and -185 are open and title-named (the sweep listed 29 title-named keys; today's regex reads 43: 14 more, namely 11 from #167 to #174 and the three of #68); (2) its R2 said PCOMP-98 and PCOMP-116 carry no comment: each carries two (PCOMP-98 ids 40202 and 40666; PCOMP-116 ids 40729 and 40769), both newest saying "Recorded; not moved".

## Instruments (every count has one; a zero is a suspect until a control fires)

- **Jira census.** Reader `python3 -I -B` (in the drafter's scratchpad, not shipped), `GET /rest/api/3/search/jql` paginated at maxResults 100 until `isLast`, JQL `project = MPSCALC AND ( statusCategory != Done ) ORDER BY created ASC` and the same with `PCOMP`. Counts: MPSCALC 225 open (210 non-epic, 15 epics, status Backlog 225), 161 Done, 386 total; PCOMP 95 open (91 non-epic, 4 epics, Backlog 95), 32 Done, 127 total. Control: the second query `project = <KEY> AND ( created >= "2000-01-01" ) ORDER BY created ASC` returned 386 and 127, equal to open plus Done; `GET /rest/api/3/myself` answered with an account id before any search.
- **GitHub census.** `gh api -X GET --paginate 'repos/<repo>/pulls?state=closed&per_page=100'`: MPS 174 closed PRs, numbers #1 to #174 (0 open: `pulls?state=open` empty); Composer 117 closed, 3 open (#85 draft HOLD, #86, #91), numbers #1 to #120. Controls: `pulls/99999` answers 404 on MPS; the Composer open call returns 3; `git/matching-refs/heads/b147` and `b1470` read 0 refs on MPS (so the kit branch names are free), `b1405` reads 1 (so the call can see a ref).
- **PR-names-a-key test.** Regex over the title and the whole body of every merged PR: `MPSCALC-<n>` plus continuation forms (`, -102`, `+ 156`); for Composer `PCOMP-<n>`. A body mention is a mention, not a completion: the records seats read PR against ticket.
- **Disjointness.** Each lane path looked up in the origin tree of the lane's repo (`git/trees/<sha>?recursive=1`, `truncated=false`; MPS 777 paths, Composer 1,038 paths). Control: a deliberately absent path (`scripts/nonexistent.sh`) reads 0; every real lane path reads 1.

## Census with conservation (every open non-epic ticket in exactly one class)

**MPSCALC, 210 open non-epic = 2 LANE + 68 RECORDS-A + 9 RECORDS-B + 37 EXCL-label + 24 EXCL-read + 70 SEED/FEATURE.**

| Class | n | Meaning | Keys |
|---|---|---|---|
| LANE | 2 | kitted build lanes this pass | 178 and 203 (M111 owns 178; M112 owns 203); 334 is M113 (named, not kitted) and sits in RECORDS-A |
| RECORDS-A | 68 | named in the title (41 open keys here, 43 with the two LANE keys) or in the body (27 more open keys) of a merged PR | see R204 (B1470) tables; body-only keys not on R204's list: 27, 28, 46, 47, 50, 53, 55, 155, 244, 245, 295 (older mentions, observations) |
| RECORDS-B | 9 | closed or held today with no commit, or not merged | 96, 135, 200, 225, 302, 324, 338, 339, 341 |
| EXCL-label | 37 | label `needs-ruling`, `question-for-kam`, `later-phase`, `phase-2` or `lane-later`: a ruling or a later phase | 68-70, 72-80, 82, 83, 85, 87, 88, 112, 113, 128, 129, 144, 149, 152, 154, 159, 181, 188, 202, 222, 224, 226, 229, 260, 261, 316, 342 |
| EXCL-read | 24 | read at source, reason below | 91, 103, 110, 114, 115, 117, 118, 120, 121, 123, 126, 130, 131, 132, 133, 161, 187, 196, 212, 217, 223, 349, 372, 383 |
| SEED/FEATURE | 70 | spec-seed rows (labels `spec-seed` or `mpscalc-seed-2026-09-30`) and the lane-V feature rows: short descriptions, new screens or governed settings, tier 1 or 2 with words and looks | not individually completable: no Done-when; 16 have no word/ruling/hosted marker in their text by regex and are named for a later read: 18, 20, 25, 29, 33, 34, 36, 40, 41, 42, 43, 44, 51, 57, 58, 64 |

EXCL-read reasons (each read from the ticket text today): 91 and 120 a rule must be chosen first; 103 rollback behaviour (product and hosted rollback); 110, 114, 130, 132 print look; 115, 117, 131 customer-facing proposal words; 118 the coordinator's 2026-11-06 comment 40793 declines it (a second implementation of the server's rounding); 121 a words call; 123 needs a setting; 126 the fix is a choice between a script poll and a runbook sentence (deploy path); 133 records-repo process; 161 new feature with words; 187 a hosted check; 196 and 217 the earlier records pass left them held on the review cap reading (comments 40451 and 40461); 212 depends on the governed-settings tickets 286 and 287; 223 and 372 deploy-side; 349 a note that waits for an SDK; 383 DATED 2026-11-12 (not before its date).

**PCOMP, 91 open non-epic = 4 IN-FLIGHT + 7 RECORDS + 19 HELD-label + 2 NEEDS-PO-label + 29 SAMPLE-POLICY-L + 30 OTHER.**

| Class | n | Keys |
|---|---|---|
| IN-FLIGHT | 4 | 62 and 114 (C91, B1421); 113 and 117 (C92, B1422) |
| RECORDS | 7 | 12 (PR #119), 23 (PR #113 earlier, PR #120 now), 120, 121, 123 (PR #120), 98 (PR #111), 116 (PR #114) |
| HELD-label | 19 | 19, 20, 68-73, 76, 79, 84-92 |
| NEEDS-PO-label | 2 | 46, 94 |
| SAMPLE-POLICY-L | 29 | 29, 31-39, 41, 42, 44, 45, 47-61: each text carries `Depends`, `Waits` or `Not started`; they build on the L1 to L3 content release held in PR #85; 59 to 61 run on the sibling project's VM |
| OTHER | 30 | reasons below |

OTHER reasons (read today): 5, 7 the reviewer's guide, sending is the product owner's; 6 ratification by subject experts; 8 rebuild of the finished examples on the demo; 9 design deferred (tolerate unknown migrations or a down convention); 10, 18, 21, 93 the demo VM; 11 not small, a contract bump; 13, 16 the Docker host; 15 Low and unmeasured; 25-28 demo overlay and registry pulls; 64 records only; 65 a note for the product owner; 66 and 67 their code (`renderedTextCredentialShapes`, the `b330-sm316-qgate` test) is on the held PR #85 branch only (origin tree at 61b3a0c2: `packages/engine/src/secrets.ts` present, the two names absent; control `DEPLOY.md` present); 74, 75, 80, 81 the remaining part is a token the product owner approves; 77 a new action with words; 78 a release signing key (ops); 82 a decision; 83 half 2 not ruled; 127 each item waits on a go or the product owner's words.

## Lanes

### M111 (B1471): docs/API.md sentences and the generated header line. Size S. Model Sonnet.
- **Tickets (read the ticket text first; it governs):** MPSCALC-178 clause 2 (the `lifecycleEvents` sentence for the body-less routes; the comment 40376 reads it NOT MET); the gate's two feedback sentences left false or short by MPS #171 (gate round 2 findings N1; they have no ticket of their own: the lane says so and does not file one); the header lines of `web/src/api/generated/SOURCE.txt` and `schema.ts` that name commit `7e9afb18` (gate B1409 F1; also item 6 of MPSCALC-195). MPSCALC-195 items 3 and 6 are read, and built only where the ticket gives the text.
- **Why actionable:** documentation and two generated header lines; no new customer-facing word (developer contract text, and the sentences are the tickets' and the gate's own); no ruling; no hosted touch.
- **Paths:** `docs/API.md`, `web/src/api/generated/SOURCE.txt`, `web/src/api/generated/schema.ts` (by the project's sync script only). Origin tree: all three present (`contents`/tree lookup, control absent path reads 0). Pointers at main `dad90244` (raw `contents`, `grep -n -F`): `docs/API.md:440` and `:441` (the `lifecycleEvents` sentence), `:738` and `:739` (the rate limit counted from stored items; `Retry-After`), `:764` and `:765` (attachments written under the store's lock; item file last); `web/src/api/generated/SOURCE.txt:2` names `7e9afb185d935fe160bc8a3cc3281f8ada3e1f8d` (`gh api commits/7e9afb18...` answers 422 "No commit found", control `commits/dad90244...` answers the sha).
- **Disjoint:** from M112 (paths below); from C91 and C92 (another repository); from R204 (a records seat that writes no code path); no open PR on MPS, no b147x ref (`matching-refs` 0).
- **Checks:** CI jobs `web` (Node 24: `ci.yml:58`; the generated copies change) and nothing else reads a docs file except the python job's `tools/demo/test/test_demo_doc.py` (read the file list; a docs change to `API.md` is not read by it: the seat proves that by `grep`).

### M112 (B1472): the open half of MPSCALC-203 in the deploy script. Size M. Model Opus (the file is the production deploy path and the subject is the confidentiality of a copy of the hosted overlay).
- **Ticket:** MPSCALC-203; the retention half and the unique copy name landed in MPS #81 (comments 39596 and 39644). Open: (1) the copy directory `"$DIR.live"` is created outside the restrictive umask (`scripts/deploy-from-ci.sh:116`, and `:160` in `check_live`); (2) the overlay read can run three times (`--retry 2` at `:110`); (3) no re-read of the overlay between the check (`:137`) and the deploy call (`:143`), where the ticket allows "the window stated in the runbook" instead. Each gets a guard row in `scripts/tests/test_deploy_pre1.py` that turns red without its fix.
- **Why actionable:** edits a script and its tests; the tests run on the fakes at `scripts/tests/fakes/az` and `curl`; the script is NEVER run against a host (no `az`, no Kudu read, no deploy); no customer-facing word; the retention ruling is already delivered. Flag for Tuesday: this is the production deploy path, so the gate is tier 1; the kit holds every hosted call and carries question Q-M112-1 (re-read in code, or a runbook sentence).
- **Paths:** `scripts/deploy-from-ci.sh`, `scripts/tests/test_deploy_pre1.py`. Not MPSCALC-126 (a design choice between a script poll and a runbook sentence; excluded above).
- **Disjoint:** from M111 (different directories; `scripts/**` against `docs/**` and `web/src/api/generated/**`); from every Composer lane (another repository).
- **Checks:** CI job `python` (`ci.yml:86`: every `scripts/tests/test_*.py` under `python3 -I`) and job `package` (`ci.yml:114`, `scripts/package.sh` reads `scripts/`).

### M113 (named, not kitted): MPSCALC-334's three untested stub operations. Size S.
`getQuoteFigures`, `recordOutcome` and `duplicateQuote` have 0 rows in `web/src/api/stub/stubApi.test.ts` (gate B1400 finding F4, measured by `grep -c` at main c5cd009; B1400 STATUS RESIDUE). Test only. Not kitted because the cap is two and M111 and M112 each close a ticket's documented open half; kit it next. Disjoint from M111 and M112 (web test file only).

### Composer: none.
Counts and reasons are in the census above. The two Composer tickets that are test-only (PCOMP-66 and PCOMP-67) name code that exists only on the held PR #85 branch (measured on the origin tree at 61b3a0c2, with controls). PCOMP-123 (size the footer by the real page count) needs `document-pdf.ts`, which PR #85 holds (the B1420 round-2 gate F3).

## Not done / UNMEASURED

- Per-ticket text of the 70 SEED/FEATURE MPS rows and the 29 SAMPLE-POLICY-L Composer rows beyond the regex markers (counts above): not read ticket by ticket.
- Machine load for running M111 and M112 beside whatever else is live: UNMEASURED (the MPS `dotnet` job is not in either lane's checks; M112 needs only python and bash, M111 needs Node 24 and `npm ci`).
- Whether MPSCALC-195 items 3 and 6 still read open: the comment 40639 reads them NOT MET at an older main; M111 re-reads.
