# Datasec sweep 18:50: completable tickets and new feedback (read-only, 2026-10-25)

Drafter: read-only sub-agent (Sonnet 5.5) for Tuesday. Clock from `date`: Sun 25 Oct 2026 18:49:36 AEDT at start, 18:53:40 AEDT at the last origin read. The feedback window opens 06:00 AEDT (= 19:00Z on 24 Oct). Base for method and for the "what already landed" comparison: `0_Brain/projects_index/2026-10-25_datasec-completable-tickets-1010.md`. Everything below was re-read from Jira and origin tonight; the 10:10 file was used only to know what to re-check.

## BLUF

1. No new human feedback since 06:00 in Jira or on GitHub (4 repos). Every Jira comment and every ticket created since 06:00 is by the one shared seat account (Jira `...1971d1`), which cannot tell the product owner from a seat; GitHub has 0 review comments and 0 non-PR issues, and 1 issue comment by the seat login (NexusAI). Mail, the NexusAI app store, QuickQuote, Vision and the HPSM Composer store were NOT read (fences).
2. 11 lanes can start now with no new word, no ruling and no production touch, in 4 repos, all disjoint from each other and from the five in-flight items: HPSM-POC 3, MPS 4, Composer 2 (+1 serial follow-on), NexusAI 3 (+1 serial follow-on). Details in LANES.
3. Open tickets (statusCategory != Done, paginated to isLast): MPSCALC 325 (all Backlog), HPSMPOC 119 (Backlog 116, In Progress 3), PCOMP 96 (all Backlog), RD 761 (To Do 360, Testing 183, Release Ready 199, In Progress 10, Put on Hold 7, Declined 2). Since the 10:10 sweep: MPSCALC +5 new (all gate residues), HPSMPOC +3 new and 3 Done, PCOMP +3, RD +1.
4. Most of the remaining backlog is NOT build work: MPS is mostly "merged work names this ticket, stays Backlog" (records), HPSM-POC is mostly SOW deliverables and "awaiting HP" or "needs-kam" tickets, Composer is the held UX list plus the L0-L9 sample-document build plan that sits behind draft PR #85, and NexusAI's 382 Testing and Release Ready tickets wait on QA or a release (a production touch).
5. Model: Sonnet for every lane except two Opus items (RD-849 log sanitiser, PCOMP-22 restore-script completeness check). Owed, not new: MPS records for #112/#114/B675/B678, Composer records for #90 (PCOMP-62/-63), #92 (PCOMP-95), #88/#89 (PCOMP-14/-17 now met by migrations 0026/0027), HPSM-POC B680 set, NexusAI #115 and the RD-814/-815/-862/-873/-777/-776 moves; the HPSM-POC `ci.yml` 391-393 lane is unblocked once B680 lands.

## State of the four repos tonight (origin, `gh api -X GET`)

| Repo | main | Open PRs (files) | Recently landed since 10:10 |
|---|---|---|---|
| MPS `MPS-Commercial-Calculator` | `a85f8bd5` (06:55Z) | #112 draft=false, 4 files: `docs/API.md`, `src/MpsCalc.Api/Quotes/PurchaseValidation.cs`, `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`, `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs` (held on the product-owner card) | #110, #113 (MPSCALC-332 row), #114 (MPSCALC-335 stub rows) |
| HPSM-POC | `4e63fc41` (06:32Z) | none | #215 (HPSMPOC-350), #216 (HPSMPOC-341/-334/-339), #217 (HPSMPOC-351) |
| Composer `Datasec-Security-Composer` | `667830ed` (01:51Z) | #92 (1 file: `apps/api/test/b626-date-rule-rows.db.test.ts`, gate live); #91 dependabot vitest bump (`package.json`, `package-lock.json`); #86 vite bump (stale since 20 Oct); #85 draft HOLD | #88, #89 (migrations 0026/0027), #90 |
| NexusAI `Reporting_Dashboard_Au` | `dbbf5881` (06:34Z) | #115 records (`HISTORY.md` only) | #112 (validators filter), #113 (RD-815 pin), #114 records |

Instrument: `pulls?state=open`, `pulls/<n>/files`, `commits/main`, `pulls?state=closed&sort=updated`. Control that could fail: `contents/tests/e2e/zz-nope.js` on NexusAI answered 404, and `contents/.../open-access-banner-guard.js` answered a body.

## HPSM-POC (HPSMPOC) - 119 open: Backlog 116, In Progress 3 (-87, -90, -91)

Frame of every census: `project = HPSMPOC AND ( statusCategory != Done )`, nextPageToken until isLast, read 18:5x AEDT. Total issues 352; negative control (`summary ~ "zzqxnonexistentphrase"`) returned 0; the same helper returned 3 for `created >= 06:00` and 48 for `created >= 2026-10-21`.

### COMPLETABLE now

| Key | Summary head | Why completable | Files it would touch | Size | Model |
|---|---|---|---|---|---|
| HPSMPOC-352 (items 1, 3, 4) | after PR #212: edge-space cells over a plain held name; two raw-slice rows in `e2e-runner.test.ts`; `ciMatrix` empty for a shard line ending in a YAML comment | Test-only and tooling-only per the ticket; no product behaviour, no word | `web/src/e2e-runner.test.ts` (lines ~543, ~911, ~933), the `e2e.mjs` `ciMatrix` (lines 90-93; path to confirm), `Hpsmpoc178CustomerNameTests.cs` and `customer-name.test.ts` (paths to confirm) | M | Sonnet |
| HPSMPOC-349 (remainder) | `e2e-runner.test.ts`: eight other rows read script/spec/config text raw | Comment 2 says the markerStep half is met by #212; the open clause is "each of the eight rows read and made comment-proof or recorded as needing neither" | `web/src/e2e-runner.test.ts` (same file as -352: ONE seat, serial) | S-M | Sonnet |
| HPSMPOC-318 | `RequestTimingLogTests`: Slack 350 to 1200 moved the detection floor unsaid | Gate rated Minor, test bound only; the doc comment must say the floor moved (comment-level change) | `api/tests/HpsmPoc.Api.Tests/Hosting/RequestTimingLogTests.cs` (~256-264) | S | Sonnet |
| HPSMPOC-343 | trace `HasControl` call sites for browser sites in `session.ts`, `override.ts`, `action-plan.ts` | Read-only trace; Done-when is a classification with its instrument; no code, no word | none in the repo (output is a Jira comment by the records seat) | S | Sonnet |
| HPSMPOC-319 (B469-2, -3 only) | HostStartRetry: a log clear no test needs; retry counter misses an unterminated last line | Test and CI-step edits, no product change. B469-5/-6 (error 1223 unproven at runtime) need a runtime measurement and are NOT in this lane | `api/tests/HpsmPoc.Modules.Feedback.Tests/Support/FeedbackApiFactory.cs` and its test, `.github/workflows/ci.yml` line ~266 | M | Sonnet |

Also unblocked but waiting: the `ci.yml` lines 391-393 comment (cites C-44 and C-99; still present on main tonight, read by `contents?ref=main`) is HPSMPOC-351 item 3, owed until B680 lands.

### BLOCKED-ON-WORDS (key + the one thing needed)
- HPSMPOC-310: the product owner's words for items 3 to 8 of the HP-reviewer walk (word pack).
- HPSMPOC-204: wording of the PDF profile caption (for-kam).
- HPSMPOC-162, -163, -165, -167, -168, -94, -91: content/offer wording (needs-kam, needs-hp-content).
- HPSMPOC-242: the placeholder has no written feedback yet (nothing to act on).

### BLOCKED-ON-RULING (key + the one thing needed)
- HPSMPOC-324: a customer name of only U+200B: accept or refuse.
- HPSMPOC-203: should an issued report keep its issue-time file name.
- HPSMPOC-257: feedback file-name fold refusing names Windows does not reserve (decision for the product owner).
- HPSMPOC-237: money (larger plan or second plan).
- HPSMPOC-271: pin owner and cadence for the floating .NET SDK, or remove the in-package route.
- HPSMPOC-228 (N-2): whether the readiness PDF GET deserves 30 s.
- HPSMPOC-352 item 2 (the 6+ and mirrored-split boundaries): the ticket calls them candidate decisions.
- HPSMPOC-177: invisible characters in a feedback comment (needs a word).

### BLOCKED on production touch or on HP (not agent-completable)
- HPSMPOC-303, -304, -309, -126, -224, -117, -196, -207, -268 (hosted demo or VM: production or HTTP to a hosted site); HPSMPOC-246 (N-4 is recorded by the next hosted deploy seat); the "awaiting HP" set (-82 to -86, -97, -166, -181) and SOW deliverables (-169 to -176).

### OWED RECORDS (not new finds)
HPSMPOC-350, -351, -341, -334, -339 and the new B677-1 ticket are in the B680 seat. Also met by merged work and still Backlog per their own comments: -311, -315, -323, -346, -187, -226, -99, -109, -292 (look-done records for the next records seat).

### NEW FEEDBACK since 06:00
- Created: HPSMPOC-350, -351, -352 (all gate residues, seat account); Done today: -344, -347, -348. No human comment. Ticket coverage: -352 covers B622-1, -2, -4, -5; B622-3 stays on -349.
- GitHub: #215, #216, #217 merged (seat); 0 issue comments, 0 review comments.

## MPS Commercial Calculator (MPSCALC) - 325 open, all Backlog

Frame: `project = MPSCALC AND ( statusCategory != Done )`, total issues 339, negative control 0, `created >= 2026-10-21` returned 24. Label census (excluding plan-/mpscalc-b labels): `needs-ruling` 23, `question-for-kam` 18, `feedback-sweep` 27, `paul-review-2026-10-16` 26, `tier-1` 94, `tier-2` 110.

### COMPLETABLE now

| Key | Summary head | Why completable | Files it would touch | Size | Model |
|---|---|---|---|---|---|
| MPSCALC-336 | Null-class refusal rows (B645-1,2,3,4: four surviving mutants, two Major) | Gate gave the fix shape: append test rows only, existing rows never edited; PR #110 already landed the product; no word | NEW or appended test file under `tests/MpsCalc.Import.Tests/**` or the `SourceLifecycleTests.GovernedNull*.cs` family (confirm); `src/MpsCalc.Import/Validation/ReferenceDocumentValidator.cs` read-only | M | Sonnet |
| MPSCALC-337 | Store first-use rows (B668-2,3,4: two mutants N6/N7 and three assertions that cannot fail) | Tests only, two new rows beside the five, the five are not edited | `tests/MpsCalc.Api.Tests/StoreFirstUseAbsent.cs`; `src/MpsCalc.Api/Sources/ActiveSources.cs` read-only | S | Sonnet |
| MPSCALC-290 | Unchanged-save sentence false for a restricted owner | The product owner approved the narrower sentence (recorded as C-67); read on origin: the old text is still on `docs/api/openapi.json` line 218, `MANUAL_ITEM_FORBIDDEN` occurs 5 times (control: a made-up string occurs 0) | `docs/api/openapi.json` line 218 only; `web/src/api/generated/openapi.snapshot.json` only if `web/scripts/sync-contract.mjs` requires it | S | Sonnet |
| MPSCALC-334 part B | `web/e2e/bom.spec.ts:180` still lacks `exact: true` (parts A and C landed in #111) | One-line spec fix; e2e is a live-API spec, not run in CI | `web/e2e/bom.spec.ts` | S | Sonnet |
| MPSCALC-310 | Endpoint use of the staff-figure strip is untested (list leak layer) | Test-only row; ticket has 0 comments, so the PRIOR-WORK CHECK must confirm it is not in main | NEW test in `tests/MpsCalc.Api.Tests/**`; `QuoteEndpoints.cs` read-only (it is in open #112) | M | Sonnet |

### Needs a PRIOR-WORK CHECK before deciding (ticket has 0 comments, product tool change)
MPSCALC-302 (`prove` says AGREE for a count-preserving tamper; per-sheet owed-set check; tier-1 product tool). Not placed in a lane.

### BLOCKED behind the in-flight PR (not a new find)
MPSCALC-325, -338 (B663-7 BOM per-line walks), -339 (B663-10 supplies-null walk): all in `PurchaseValidation.cs`, held on the product-owner card until Mon 09:00.

### BLOCKED-ON-WORDS
- MPSCALC-169 (field name and contract words for the markups source), MPSCALC-288 (new contract member and its words), MPSCALC-176 (approved 46-row register, but it shares `docs/API.md` and `docs/api/openapi.json` with -290 and #112: after they land).

### BLOCKED-ON-RULING
- The 23 `needs-ruling` tickets and 18 `question-for-kam` tickets (counted by label only, not individually read); MPSCALC-316 (quoteRef length wording).

### OWED RECORDS (not new)
MPSCALC-335 (landed by #114), -333 (met by #110, order gaps of B591-10 not claimed), -331, -329, -332, -324, -326, -327, -323, -322, -320, -319, -318, -311, -307, -292, -328, -321 and the other "merged work names this ticket" tickets stay Backlog by project rule (no ticket moves on merge); the records seat comments, no code.

### NEW FEEDBACK since 06:00
- Created: MPSCALC-335 (B643), -336 (B645), -337 (B668), -338, -339 (B663); all gate residues by the seat account. 10 comments since 06:00, all the seat account. GitHub: 0 issue comments, 0 review comments, open #112 has 0 reviews. Ticket coverage: complete (each residue has its ticket).

## Security Composer (PCOMP) - 96 open, all Backlog

Frame: `project = PCOMP AND ( statusCategory != Done )`, total issues 97, negative control 0, `created >= 2026-10-21` returned 97.

### COMPLETABLE now

| Key | Summary head | Why completable | Files it would touch | Size | Model |
|---|---|---|---|---|---|
| PCOMP-96 | Remove the internal "B587:" prefix from the API sentences of PR #87 | The product owner's 2026-10-25 ruling (C-102): approved as written minus the prefix. Read on origin: `document.ts` has 2 hits for `B587:` (control: the file reads) | `packages/api-contract/src/document.ts` (lines 172, 848), `packages/api-contract/src/openapi.json` (2802, 11236), `packages/api-contract/src/openapi.test.ts` (pins a sha256), `apps/web/src/api/schema.d.ts` (301, 1658) | M | Sonnet; STOP if the contract version must move |
| PCOMP-97 | B648-1..5 (Minor): DEPLOY.md command-guard test, 3 scanner gaps, 4 weak pins, 1 comment | Test-only per the ticket; the file exists on main (19,608 bytes) | `packages/db/test/b616-deploy-commands.db.test.ts` only | M | Sonnet |
| PCOMP-22 | Restore script cut at a statement boundary exits 0 with 0 rows restored (B115-F5) | The gate wrote the fix shape (check the dump ends with "PostgreSQL database dump complete" before step 2) and a test; no new word | `DEPLOY.md` (Route B two-step), a db test beside `b616-deploy-commands.db.test.ts` (SERIAL after PCOMP-97: same area) | M | **Opus** (a data-destroying restore path) |
| PCOMP-24 | A pending Guided start with a target can still be moved by `completeExpertSetup` (B146-N1) | Fix shape given (refuse 409 or keep the target) with a regression plant; product code, tier 1. CHECK: if the refusal needs a NEW message text it becomes BLOCKED-ON-WORDS | `apps/api/src/**` (module of `completeExpertSetup`; path to confirm) and one test | M | Sonnet |

Also landed and owed as records: PCOMP-14 (migration 0027 index) and PCOMP-17 (migration 0026 CHECK) are met by merged #89 (their own last comments say so); PCOMP-62/-63 by #90; PCOMP-95 is the gate B682 build of #92 (in flight). Dependabot #91 (vitest bump, clean) is Tuesday's landing, not a lane.

### BLOCKED behind draft PR #85 (HOLD)
PCOMP-67, PCOMP-66 (their code is on the #85 branch, not main), PCOMP-23 (footer line budget in the PDF renderer; `packages/renderers/**` is in #85), and the L0-L9 sample-document plan PCOMP-29 to -61 (30+ tickets; content release and renderer; not individually read, see UNMEASURED).

### BLOCKED-ON-WORDS
PCOMP-94 (questions for the reviewer, needs-kam), PCOMP-69 (D-006 wording), PCOMP-92, PCOMP-85, PCOMP-76, PCOMP-79, PCOMP-73, PCOMP-86 and the other `held` UX tickets (labels `held`; screen wording or look changes).

### BLOCKED-ON-RULING
PCOMP-9 (tolerate unknown recorded migrations, or a down-migration convention), PCOMP-65 (optional: a runbook line for operator power), PCOMP-46 (needs-kam), PCOMP-82 (UTC date words decision).

### NEW FEEDBACK since 06:00
Created PCOMP-95 (B626 rows), -96 (B587 prefix), -97 (B648 Minors); 2 comments, both the seat account. GitHub: 0 comments; #92 and #85 have 0 reviews. Ticket coverage: complete.

## NexusAI (RD) - 761 open: To Do 360, Testing 183, Release Ready 199, In Progress 10, Put on Hold 7, Declined 2

Frame: `project = RD AND ( statusCategory != Done )`, total issues 878, negative control 0, `created >= 2026-10-21` returned 7. Note: the two "Declined" tickets sit in a non-Done status category, so they are in the 761.

### COMPLETABLE now

| Key | Summary head | Why completable | Files it would touch | Size | Model |
|---|---|---|---|---|---|
| RD-844 | rd490 browser guard fails the push Build when cdnjs is slow | The product owner's earlier ruling (answer cdnjs with an empty stand-in in the test); still open: `open-access-banner-guard.js:294` on main reads `waitUntil: 'load'` | `tests/e2e/open-access-banner-guard.js`, `__tests__/rd490-open-access-banner-browser.test.js`; count-neutral | M | Sonnet |
| RD-882 | Input filter: three missing test cells in the #112 suite | Test-only per the ticket, no product file, no word; #112 has landed so the counts file is free | `__tests__/rd777-776-validators-input-filter.test.js`; `scripts/verify-expected-counts.json` if cells are added (UNMEASURED: the file mentions no `rd777` key on main) | S-M | Sonnet |
| RD-850 / -851 / -852 / -854 | RD-848 gate findings on the Dockerfile COPY guard (chown/chmod as text, duplicated RUN-output COPY, three clauses with no cell, two `.gitignore` files ACR never sends) | Test-helper and test cells only; they were held for the counts file, which #112 has now released | `__tests__/helpers/dockerfile-stages.js` (13,497 bytes on main), its rd848 test (path to confirm), `scripts/verify-expected-counts.json` | M | Sonnet |
| RD-843 | R8 blind spot: a count on a "CSP violation report" line is filtered out before any arm | Coverage gap in a test, no product claim | `__tests__/rd618-csp-intake-residue.test.js` | S | Sonnet |
| RD-847 | Lock tool `BASE` is hard-coded to the T9 drive | Tooling only; a one-line default fixed to the new volume; do it when no jest or docker lock is held | `session-tools/nexusai-lock.sh` (line ~79; inside the NexusAI project, outside `__tests__`) | S | Sonnet |
| RD-849 | `logSafe` passes C1 controls U+0080-U+009F raw (NEL, CSI) | `backend/logSafe.js` exists on main (2,257 bytes); fix and cells are given by the gate; no word. Security log sanitiser: Opus | `backend/logSafe.js` and its test; counts file (SERIAL after the counts-file lane) | M | **Opus** |

### Conditionally completable
RD-878 (`PUT /api/risk-conditions/:id` with a non-string `risk_level` answers 500): completable only if the refusal reuses the existing `FIELD_NOT_ACCEPTED` shape and message; a new message makes it BLOCKED-ON-WORDS. Tier 1, `backend/server.js`.

### BLOCKED-ON-WORDS
RD-876 (the "results limited" notice and "show all" button: ruled in principle, words not written), RD-872, RD-869, RD-863-family (`user-facing`), RD-840 and RD-841 (feedback #8 and #9, `needs-decision`, Release Ready).

### BLOCKED-ON-RULING
RD-858 (testing.html SQL box: remove, repurpose or keep), RD-855 (Admin AI Tuning saves settings nothing reads: wire or remove), RD-859 and RD-868 (risk-condition writers and stored KQL: security design), RD-845 (erasure-status backstop design), RD-842 (feedback #10: which fax and scan data the logs may carry).

### BLOCKED on QA or a release (a production touch)
The 183 Testing and 199 Release Ready tickets (including RD-814, -862, -873, -777, -776, -848, -846, -841): a transition is a records move, a release is a deploy.

### OWED RECORDS (not new)
NexusAI PR #115 (records, landing), RD-815 (landed by #113), RD-814/-862/-873 (landed by #111/#110), RD-777/-776 (landed by #112), RD-591 flake evidence.

### NEW FEEDBACK since 06:00
Created RD-882 (B667 finding, seat). 7 comments since 06:00, all the seat account (control: RD's first three updated tickets carry 4 comments by that same account, so the author field fires). GitHub: 1 issue comment by the seat login, 0 review comments, #115 has 0 reviews. Ticket coverage: complete.

## LANES (partition by directory; named from both sides)

Rule: a lane's YOURS paths are listed; NOT YOURS is every other lane's path plus the open-PR and live-kit paths in that repo. Repos never share a path. One seat, one worktree, one branch per lane; a heavy run starts only below load1 7 (the machine, not the paths, is the limit).

### HPSM-POC (no open PR, so no lane waits on a gate)

| Lane | Tickets | YOURS | NOT YOURS |
|---|---|---|---|
| H-E2E | HPSMPOC-352 (items 1, 3, 4), -349 remainder | `web/src/e2e-runner.test.ts`, the `e2e.mjs` ciMatrix, the customer-name test pair (`Hpsmpoc178CustomerNameTests.cs`, `customer-name.test.ts`) | `api/tests/HpsmPoc.Api.Tests/Hosting/**` (H-TIMING), `.github/workflows/ci.yml` (H-CI), the records repo (B680) |
| H-TIMING | HPSMPOC-318 | `api/tests/HpsmPoc.Api.Tests/Hosting/RequestTimingLogTests.cs` | `web/**`, `.github/**`, `api/tests/HpsmPoc.Modules.Feedback.Tests/**` |
| H-CI | HPSMPOC-319 (B469-2, -3); later HPSMPOC-351 item 3 (lines 391-393) once B680 lands | `.github/workflows/ci.yml` (line ~266 now; 391-393 later), `api/tests/HpsmPoc.Modules.Feedback.Tests/Support/FeedbackApiFactory.cs` and its test | `web/**`, `api/tests/HpsmPoc.Api.Tests/**` |
| H-TRACE (read only) | HPSMPOC-343 | no repo path; the answer is a ticket comment | everything |

### MPS (open #112 owns `docs/API.md`, `PurchaseValidation.cs`, `QuoteEndpoints.cs`, `QuoteWalkCaps.cs`)

| Lane | Tickets | YOURS | NOT YOURS |
|---|---|---|---|
| M-NULLROWS | MPSCALC-336 | test files for the null-class refusal (under `tests/MpsCalc.Import.Tests/**` or `SourceLifecycleTests.GovernedNull*.cs`, confirm) | `tests/MpsCalc.Api.Tests/StoreFirstUseAbsent.cs`, the four #112 paths, `docs/**`, `web/**` |
| M-STORE | MPSCALC-337, MPSCALC-310 | `tests/MpsCalc.Api.Tests/StoreFirstUseAbsent.cs`; a NEW staff-strip test file in `tests/MpsCalc.Api.Tests/` | `QuoteEndpoints.cs` (read-only), `ActiveSources.cs` (read-only), `QuoteWalkCaps.cs`, `docs/**` |
| M-DOC290 | MPSCALC-290 | `docs/api/openapi.json` line 218; `web/src/api/generated/openapi.snapshot.json` only if the sync script requires it | `docs/API.md` (#112), `src/**`, `tests/**`, MPSCALC-176's later work |
| M-E2E | MPSCALC-334 part B | `web/e2e/bom.spec.ts` | `web/src/**`, `web/scripts/**`, `docs/**`, `src/**` |

### Security Composer (open #92 owns `apps/api/test/b626-date-rule-rows.db.test.ts`; #85 draft owns 57 files incl. `packages/engine/**`, `packages/renderers/**`)

| Lane | Tickets | YOURS | NOT YOURS |
|---|---|---|---|
| C-PREFIX | PCOMP-96 | `packages/api-contract/src/{document.ts,openapi.json,openapi.test.ts}`, `apps/web/src/api/schema.d.ts` | `packages/db/**`, `DEPLOY.md`, `apps/api/**`, `packages/engine/**`, `packages/renderers/**` (#85) |
| C-DEPLOY | PCOMP-97, then PCOMP-22 (serial, Opus for -22) | `packages/db/test/b616-deploy-commands.db.test.ts`, `DEPLOY.md` Route B section, one new db test beside it | `packages/api-contract/**`, `apps/**`, `apps/api/test/b626-date-rule-rows.db.test.ts` (#92) |
| C-GUIDED (conditional) | PCOMP-24 | the module of `completeExpertSetup` under `apps/api/src/**` and one test (confirm path) | `packages/api-contract/**` (a new 409 code would touch the contract: then STOP and ask), `packages/db/**`, #92's file |

### NexusAI (open #115 owns `HISTORY.md`; the counts file `scripts/verify-expected-counts.json` is a single choke point)

| Lane | Tickets | YOURS | NOT YOURS |
|---|---|---|---|
| N-GUARD | RD-844 | `tests/e2e/open-access-banner-guard.js`, `__tests__/rd490-open-access-banner-browser.test.js` (count-neutral) | the counts file, `static/**`, `backend/**`, `.github/**` |
| N-COUNTS (one seat, serial) | RD-882, then RD-850/-851/-852/-854, then RD-843 | `__tests__/rd777-776-validators-input-filter.test.js`, `__tests__/helpers/dockerfile-stages.js`, the rd848 test, `__tests__/rd618-csp-intake-residue.test.js`, `scripts/verify-expected-counts.json` | `tests/e2e/**`, `backend/**`, `session-tools/**`, `HISTORY.md` |
| N-LOCK | RD-847 | `session-tools/nexusai-lock.sh` | `__tests__/**`, `backend/**`, `tests/e2e/**` |
| N-LOGSAFE (Opus, after N-COUNTS) | RD-849 | `backend/logSafe.js` and its test, the counts file | everything else; waits because it shares the counts file |

Cross-lane check, by eye only (NOT run as a program): within each repo no YOURS path appears in another lane's YOURS, except the declared shares: HPSM-POC `ci.yml` (H-CI only; H-E2E reads it), Composer `DEPLOY.md`/`b616` test (inside C-DEPLOY, serial), and the NexusAI counts file (N-COUNTS then N-LOGSAFE, serial). No lane touches a path in an open PR file list: MPS #112 (4 paths), Composer #92 (1 path), #91 (2), #85 (57, compared by name only), NexusAI #115 (1).

Suggested first wave (4 light seats, then heavy ones under load1 7): H-E2E, M-STORE, C-PREFIX, N-GUARD; with H-TIMING, M-DOC290, N-LOCK as small fillers.

## FOUND

1. Open boards, 18:5x: MPSCALC 325, HPSMPOC 119, PCOMP 96, RD 761. All four lane lists at 10:10 have moved: H-NUM, H-AUDITDEV and H-CIFILE landed as #216, #215, #217 (HPSM-POC main `4e63fc41`); M-A2 became PR #112 (held); M-STORE332 landed as #113 and M-STUBROWS as #114; C-TEST landed as #90, C-ROWS is #92 (gate B682 live), #88 and #89 landed; N-PIN landed as #113 and the validators PR #112 landed (NexusAI main `dbbf5881`).
2. Three new residue tickets were filed from today's gates and are ready lanes: MPSCALC-336/-337 (tests only) and RD-882 (tests only). PCOMP-97 is a fourth (test only).
3. Two older Composer tickets are now met by merged work (PCOMP-14, PCOMP-17 via #89) and only need a records comment; they should not be built.
4. The counts file is the NexusAI choke point again: RD-882, RD-850 to -854 and RD-849 can add cells, so they run in series in one lane after N-GUARD, which is count-neutral.
5. `ci.yml` lines 391-393 still cite record ids C-44 and C-99 on main (read at origin), so HPSMPOC-351 item 3 is real and waits only for B680.

## TESTED (controls that could fail)

- Totals: for each board, `negative control` (`summary ~ "zzqxnonexistentphrase"`) returned 0 and a broad query returned the full total (339, 352, 97, 878), so the helper can both fire and stay silent. Status sums add up: RD 360+183+199+10+7+2 = 761; HPSMPOC 116+3 = 119.
- Window queries: `created >= 06:00` returned 5, 3, 3, 1; `created >= 2026-10-21` returned 24, 48, 97, 7 on the same helper (so the date filter can fire on every board); `updated >= 06:00` returned 14, 11, 5, 8.
- Authors: all 27 comments since 06:00 are by the one seat account; the RD first-three check returned 4 comments by that account (a positive control on the author field). The MPSCALC, HPSMPOC and PCOMP first-three checks returned empty, so those three author checks have only the RD control behind them.
- GitHub comments: `issues/comments?since=2026-10-24T19:00:00Z` returned 0, 0, 0 and 1 (NexusAI, seat login); control `since=2026-09-01` returned MPS 2 (seat), HPSM-POC 5 (4 seat, 1 dependabot), Composer 3 (dependabot), NexusAI 7 (5 dependabot, 2 seat): the endpoint returns rows when rows exist.
- Origin anchors: MPS `openapi.json` line 218 old text present, `MANUAL_ITEM_FORBIDDEN` 5 hits (control 0 for a made-up string); Composer `document.ts` 2 `B587:` hits and the `b616-deploy-commands` test file 19,608 bytes; HPSM-POC `ci.yml` 391-393 read; NexusAI `open-access-banner-guard.js:294` `waitUntil: 'load'`, `logSafe.js` exists, a made-up path answers 404.

## HOW

Jira: read-only GET through the HPSM-POC helper `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/.tools/b649/jira.py` (read whole before use), importing its `api`, `adf`, `comments` functions inside `python3 -I` scripts; every JQL has the form `project = <KEY> AND ( ... )`; totals paginated with `nextPageToken` until `isLast` (asserted). GitHub: `gh api -X GET` only, each repo under its own project `GH_CONFIG_DIR`. No git command was run in any project clone.

## UNMEASURED (said plainly)

- Mail (coordinator and shared inboxes), the NexusAI in-app feedback store, QuickQuote, Vision and the HPSM Composer store: not read; the fences forbid mail, `az` and HTTP to hosted sites. "No new feedback" holds only for Jira and GitHub.
- The shared seat account (Jira `...1971d1`, one GitHub login) cannot separate the product owner from a seat; "human" here means a non-seat account, and there is none.
- File paths marked "confirm" (the HPSM-POC `e2e.mjs`, customer-name test pair; the MPS Import test directory; the NexusAI rd848 test; the Composer `completeExpertSetup` module) were inferred from ticket text and not each looked up in a tree.
- Not individually read: PCOMP L-series PCOMP-29 to -61 (30+ tickets), the MPS `needs-ruling` (23) and `question-for-kam` (18) sets, the ~360 RD To Do tickets older than 2026-10-10, and MPS tickets MPSCALC-270 to -287 (V6-V11 feature lanes, all `tier-1/2` with new screens: assumed to need words). A completable ticket may exist in those sets.
- Whether MPSCALC-310, -302 and -307 are already in main (0 or ambiguous landing comments) and whether MPSCALC-313 is met by #111/#114: PRIOR-WORK CHECK by the builder.
- Whether the NexusAI counts file needs a new cell for RD-882 and RD-843 (the file shows no `rd777` text on main), and whether RD-878's refusal can reuse an existing message.
- Run times and capacity: not measured; `load1` was not read tonight (it was 8.77 at 10:16).
- Jira timestamps were compared as printed by the API (account time zone, AEDT assumed from the creation times of tickets made this evening); the JQL window `"2026-10-25 06:00"` is interpreted by Jira in the account zone.
- The decision cards and the clarifications file were NOT read tonight (no `decision_queue.sh`); every "ruled" statement is from a ticket comment or from the 10:10 sweep file.

## Outside-the-fences disclosure

- Used the HPSM-POC Jira helper for all four projects (same site and same credentials: MPS `JIRA.md` lines 10-11 say the lines were copied from the HPSM-POC `.env`). It read the HPSM-POC `.env` in-process; I never opened or printed a `.env`. The three other projects' own helpers were listed (`find` on their `.tools`), not run.
- Listed the root of the HPSM-POC, MPS, Composer and NexusAI project folders (names only), which shows the folder name `HP Reporting and Docs` and a `.docx` SOW file name in the HPSM-POC root; neither was opened.
- Read two tool-result spill files the harness wrote under `/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.claude/projects/.../tool-results/` (my own command outputs, not credentials). They are in a `4_Credentials` path but are not `.env`.
- Read, whole, `DRAFTER_RULES.md`, the feedback-store `inventory.md`, and the Datasec 10:10 sweep file; listed (names only) the `projects_index` folder, which also shows `scoreboard*.md`, `decision_queue.md` and `entries/` file names; none was opened.
- One command was refused by a hook (an unquoted `=====` in an echo); I fixed the quoting and re-ran it. Three no-op `cat > /dev/null` lines were run by mistake and wrote nothing.
- No non-Datasec project output appeared. No Jira write, no GitHub write, no HTTP to any hosted or demo site, no mail, chat, Artifact, Docs or publish tool, no `decision_queue.sh`, no `az`, ssh or docker. I wrote only this file.

SWEEP DONE /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_SWEEP-1850_completable-and-feedback.md
