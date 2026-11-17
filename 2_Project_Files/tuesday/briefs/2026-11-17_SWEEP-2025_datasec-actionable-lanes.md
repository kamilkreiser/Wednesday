# SWEEP-2025: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-17 evening)

Written by a read-only sweep drafter from 20:21 to about 20:40 AEDT (`date` read 20:21:01 at start, 20:29:28 near the end). Form copied from `2026-11-17_SWEEP-0600_datasec-actionable-lanes.md`, updated to what landed today: MPS #209; NexusAI #210 to #214; HPSM #331 and the UAT deploy. Fences kept: no Jira write, no GitHub write, no push, no mail, no `az`, no `cd`, no deploy, no token printed, no `decision_queue.sh list`. Scratch (open and Done dumps, alert list, tree list, copied and new GET-only scripts `jqdump.py`, `jdesc.py`, `jcom.py`, `rg.sh`, `bc.sh`) is in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s286/sweep2025/`.

## BLUF

**11 buildable keys in 8 lanes on 3 projects: HPSM-POC 2 keys (2 lanes), MPS 2 keys (2 lanes), NexusAI 7 keys (4 lanes), Composer 0, Vision 0 (paused).** The keys: HPSMPOC-507, 508; MPSCALC-410, 207; RD-995, 994, 1002, 734, 729, 730, 689. Everything the 06:00 sweep proposed has landed except RD-995 and RD-994. New buildable work since the morning came from the three records passes of today (MPSCALC-410, HPSMPOC-507/508, RD-1002) and from a read of the test-tail keys the morning carried unread (RD-734, 729, 730, 689, MPSCALC-207).

Recommended order (section 9): 1 NX-R (RD-995), 2 M-D3 then M-I (MPSCALC-410, then 207), 3 H-D (HPSMPOC-508), 4 NX-T3 (RD-1002, 734, 729, 730), then H-T, NX-A, NX-C. Lanes 1 to 3 are in three different repositories and can run together (machine-load rule: one waiter, load1 < 7); lane 4 waits for lane 1 (the NexusAI jest lock is one holder at a time).

### Board census (measured)

Counts are `board_count.sh jira` through `bc.sh`, JQL `project = <KEY> AND ( ... )`. Every line printed `limit was 5001, so this is a real count and not a cap`. The same sets were dumped with the GET-only `jqdump.py` (pages of 100; `unique` equalled `rows` in all eight dumps; HPSM 2 and 4 pages, MPS 2 and 3, Composer 1 and 1, NexusAI 9 and 2). Control that can fail: open + Done = created since 2000 in all four: HPSM 148 + 360 = 508; MPS 165 + 245 = 410; Composer 81 + 48 = 129; NexusAI 868 + 129 = 997.

| project | open now | open at 06:00 sweep | change by `comm` of the key lists | by status (measured) | buildable keys | lanes |
|---|---|---|---|---|---|---|
| HPSM-POC (HPSMPOC) | 148 | 146 | HPSMPOC-507, 508 new; none gone | 145 Backlog, 3 In Progress (87, 90, 91) | 2 | 2 |
| Security Composer (PCOMP) | 81 | 81 | none | 81 Backlog | 0 | 0 |
| MPS Calculator (MPSCALC) | 165 | 165 | MPSCALC-390 Done; MPSCALC-410 new | 165 Backlog | 2 | 2 |
| NexusAI (RD) | 869 (re-measured 20:31; 868 at the first dump 20:2x) | 868 | RD-804 Done; RD-1001 and RD-1002 new (RD-1002 filed about 20:21, after the first dump; the 20:31 re-dump adds it, key list `rerun/rd_open2.tsv`) | To Do 363, Testing 290, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 (at 20:31) | 7 | 4 |
| Vision Sales Portal | not re-swept | 16 (06:00) | none known | paused | 0 | 0 |

Note on NexusAI: the first dump (868 open; To Do 365, Testing 287) ran before the records pass filed RD-1002 and before RD-998, 996 and 985 moved to Testing; the re-run at 20:31 reads 869 open (To Do 363, Testing 290) with controls: 869 + 129 Done = 998 created, and `comm` against the first key list prints only RD-1002 as new. The 06:00 total was 868; RD-804 left (Done) and RD-1001 and RD-1002 joined, which is 868 - 1 + 2 = 869.

Origin state (all `gh api -X GET` under each project's own `GH_CONFIG_DIR`): HPSM-POC code main `b81793d1` (#331, 2026-11-17T00:47:10Z), 0 open PRs; MPS `125f7a52` (#209, 2026-11-16T19:37:28Z), 0 open PRs; Composer `b4681297` (#130, unchanged), 1 open: draft #85 (HOLD K6); NexusAI `e3720686` (#214, 2026-11-17T08:31:47Z), **1 open PR: #215 `records/b1669-history` (HISTORY.md only; Records seat R260 is idle waiting on the #214 Build)**. Control: `state=closed` printed each project's latest merges (HPSM #331, #330, #329; MPS #209 to #205; NexusAI #214 to #210). **NexusAI code scanning on main `e3720686`: 22 open alerts** (every row's `commit_sha` is `e3720686`, 22 of 22; the list is under 100 rows so one page; it was 33 at 06:00 and 7 were dismissed today on the product owner's word). By file: `backend/server.js` 13 (user-controlled-bypass x10, http-to-file-access 1, missing-token-validation 2), `emailService.js` 2, `entraProvisioning.js` 2 (#145, #146), `jsonStorage.js` 2, `incidents.js` 2, `tests/uat-run.js` 1 (list in `rd_alerts_open.tsv`). Never dismiss an alert.

Standing line for every HPSM kit: this phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only; nothing deploys.

### Lane table

| lane | project | keys | owns (code repository paths) | model row, gate | size |
|---|---|---|---|---|---|
| H-T | HPSM | HPSMPOC-507 | `web/src/components/customer/remediation-store.test.ts` (one row in the `startingOwner` block, line 454 onward) | Sonnet, L6 (line 85), G2 (line 109) | S |
| H-D | HPSM | HPSMPOC-508 | `web/package.json` (line 20) and `web/package-lock.json` only | Sonnet, L3 (line 82), G2 (line 109) | S to M |
| M-D3 | MPS | MPSCALC-410 | `docs/API.md` (lines 706 to 707 only) | Sonnet, C2 (line 92), G2 (line 109) | S |
| M-I | MPS | MPSCALC-207 clause 3 | `src/MpsCalc.Import/PriceBookImporter.cs` (line 150, one literal) and any test that pins that text (read first) | Sonnet, L1 (line 80), G2 (line 109) | S |
| NX-R | NexusAI | RD-995 | `docs/ROLE-CAPABILITIES.md` (row at line 137), `backend/services/capabilities.js` (entry at line 227, also line 174), files the project's inventory command regenerates (names UNMEASURED) | Sonnet, C2 (line 92), G1 (line 108) by default | S |
| NX-T3 | NexusAI | RD-1002, RD-734, RD-729, RD-730 (read first) | four existing test files: `__tests__/rd969-three-routes-empty-request.test.js`, `__tests__/rd638-export-always-ends.test.js`, `__tests__/rd648-harness-boot-residuals.test.js`, `__tests__/handover-gate-table.test.js`; `scripts/verify-expected-counts.json` | Sonnet, L6 (line 85), G2 (line 109); RD-1002 alone is G3 (line 110) | M |
| NX-A | NexusAI | RD-994 | `backend/server.js` (`auditLog` call sites only; `function auditLog` at line 305), one NEW test file, counts file | Opus, C3 (line 93), G1 (line 108) | L |
| NX-C | NexusAI | RD-689 | `backend/server.js` (comments only, around lines 832 and 1030), `backend/services/schedulers/healthSweeperScheduler.js` (comment at line 22), `__tests__/rd385-shipped-root-markdown-identifiers.test.js` (delete its 5 REVIEWED entries), counts file | Sonnet, L3 (line 82), G2 (line 109) | S |

Model ids from `0_Brain/dashboard/data/models_latest.json` (printed today): Opus `claude-opus-5-5` (line 17), Sonnet `claude-sonnet-5-5` (line 23). Rows from `fleet/specs/model-routing.md`, line numbers printed today by `awk NR`: L1 line 80, L3 line 82, L6 line 85, C2 line 92, C3 line 93, G1 line 108, G2 line 109, G3 line 110. Spark is not this seat's (pickup top), so the L-rows run on Sonnet (the "esc" column) with the Sonnet gate as shown. Ports: none requested (HPSM and MPS kits use their own slot rules; NexusAI lanes use the slot rule of their kit).

## 1. HPSM-POC (HPSMPOC): 2 buildable, 2 lanes

Open 148 (145 Backlog, 3 In Progress: 87, 90, 91, Kam-owned C-30 items). Main `b81793d1`, 0 open PRs, UAT deployed today (D67). New since 06:00: HPSMPOC-507 (Low, test) and HPSMPOC-508 (Medium, Dependabot), both filed by records pass R259; HPSMPOC-482 got a comment (a further sighting at the same assertion; it stays a diagnosis ticket).

### Buildable now

- **H-T: HPSMPOC-507** (lone-surrogate row). At main, `startingOwner` is `remediation-store.ts:58` to `:72`; the loop compares at `:68`; `OWNER_MAX = 100` at `:18`; the test block starts at `remediation-store.test.ts:454` (all printed today). The ticket's own proposed default is "pin the current result with one row (tests only; no product line changes)"; the expected value is the decision, so the builder uses the default and writes it in the row's title. One file, one row, red-first by planting the opposite expectation. Not under the HTML phase hold (the customer remediation register is not one of the 21 HTML keys; control: 0 of the seven keys here appear in `hpsm_html_all.tsv`).
- **H-D: HPSMPOC-508** (`next` 16.4.2 to 16.4.5 or later in the 16.4 line, GHSA-mfr8-8qww-v76h, medium; Dependabot alerts 10 and 11; `web/package.json:20` reads `"next": "16.4.2"`, printed today). The ticket's own recommendation and proposed default is exactly this change: `web/package.json` and the lock only, no code, then the whole web suite, a build and the end-to-end checks; "accepts nothing and approves no upgrade" beyond the default. Lands to main only; **nothing deploys** (the deploy round is the owner's card). The builder first confirms the target version exists on the registry and records the one-time build notice the ticket mentions. The ticket says the app uses neither `use cache` nor `unstable_cache` (DERIVED, not measured): the builder greps for both before building.

### Excluded (HPSM-POC), with the reason

- **HTML phase** (Kam and Paul decide; Decision Document of 2026-11-10): 21 keys from `fleet/state/s279/sweep1925/hpsm_html_all.tsv` (file holds 21 rows); all 21 are open now (counted: 21 of 21 in today's open set). HPSMPOC-467 (Demo alias on the Home pipeline table; ruled "Alias on all seven", six built in #317) is excluded with them: its last surface overlaps the planned Home rebuild HPSMPOC-457, per its own 11-11 and 11-12 comments.
- **Held or awaiting the product owner:** 480, 481, 469, 483, 471 to 479 (13 keys, all open now; HPSMPOC-478 waits for an upstream release, and 477 is "held for later" by its title).
- **Deploy round and HP-tool integrations:** 497, 498, 499 (travel with the deploy card, which is Tuesday's), 117, 126, 234, 235, 303, 362 (hosted-demo measurements and deploy-time items), 237 (money question for Kam).
- **Not code lanes:** 500, 501, 502 (outside the repository), 503 and 482 (a diagnosis; "find the cause first"), 470 points 2, 4, 5 (layout calls), 506 (accepted as built: "Proposed default if nobody objects: no change"), 91, 162, 163 (draft documents).
- **Residue that needs a decision, not a build:** HPSMPOC-356 (what remains of `infra/tests/test_ci_workflow.py`: the unread step bodies and inputs are "neither commissioned nor recorded as not wanted", comment 41123; a card, section 10). HPSMPOC-99 (N-4 is Kam's, N-9 waits for a scale-out). HPSMPOC-323 (three PRs landed; records residue only).
- **Awaiting HP (reviewer feedback):** 486, 493 and the 12 `awaiting-hp` keys: words from HP, excluded.
- In Progress 87, 90, 91: Kam-owned C-30 items, not agent work.

## 2. Security Composer (PCOMP): 0 buildable

Open 81, all Backlog, key set identical to 06:00 (`comm` prints nothing in either direction). Main `b4681297`. Draft PR #85 (HOLD K6) stays held; 19 keys carry the `held` label behind it and the L0 to L9 sample-policy-document content keys (PCOMP-29 to 61) are the same content release. "No Guided work until you turn it back on": PCOMP-75 and any Guided-screen key stay excluded. Read today (not carried): PCOMP-66 (a test-only path in `secrets.ts`, "product edit DEFERRED" by coordinator ruling), PCOMP-67 (its test is on the PR #85 branch, not on main), PCOMP-64 (records only, no code effect), PCOMP-12 (PR #119 landed the build; record only), PCOMP-11 (needs a contract change and two new words), PCOMP-9 (design call), PCOMP-93, 10, 18, 25, 28 (the demo VM: hosted). PCOMP-128 item 2 and PCOMP-129 stay words for the product owner (carried). PCOMP-52 (built, PR #84), 74, 80, 81 (records only), 46 and 94 (`needs-kam`): carried excluded.

## 3. MPS Calculator (MPSCALC): 2 buildable, 2 lanes

Open 165, all Backlog. Left since 06:00: MPSCALC-390 (Done, M-D2 landed as #209: the comment at `PurchasePageEstimate.cs:10` now says "X-33 (the row of that id in docs/ENGINE.md)", printed today). New: MPSCALC-410. Main `125f7a52`, 0 open PRs. Pricebook values are confidential: none appears here.

### Buildable now

**M-D3: MPSCALC-410** (docs only, one file). `docs/API.md:706` to `:707` says "every source version id is unique, within the document and across every governed version that did not fail" (printed today). The code is `SourceDocumentChecks.cs:406` to `:407`: `CountsAsDuplicate` is true for every state except Draft, Failed Validation and Expired (printed today). Per the ticket: replace the clause with words that name the states (Validating, Active, Superseded, and a state word the code does not know count; Draft, Failed Validation, Expired do not), each sentence read against the code and its rows first. **The ticket names `docs/api/openapi.json:751` (same clause) and leaves to the coordinator whether it changes; the pickup says "Ask Kam on the next MPS card whether openapi.json:751 changes with MPSCALC-410".** So this lane owns `docs/API.md` only until that is answered; if the answer is yes, the contract file is changed by the project's own tool and the generated header is regenerated by `scripts/sync-contract.mjs` (the builder checks whether it exists at main: the path `scripts/sync-contract.mjs` returned HTTP 404 from the `contents` API at the repository root today, so the tool lives elsewhere; read first).

**M-I: MPSCALC-207 clause 3** (one literal). The 2026-11-15 evidence run (the 2026-11-15 records note, comment 41231 on the ticket for MPSCALC-333; the 207 note is in the ticket's comments) met clauses 1 and 4 and found clause 3 short by one literal: the words "any mapped model sheet" are not in the PANEL-BLOCK lineage note at `src/MpsCalc.Import/PriceBookImporter.cs:150` (printed today; the string is on that one line, and ends "...compatibility basis \"{PanelBlockBasis}\")."). Pickup carries it as "MPSCALC-207 PANEL-BLOCK lineage note (B1408 ANSWER-1 row)": not dropped, not held. **Read first:** the string is written into the price-book store's lineage, so a test or golden file may pin the exact text; if one does, the lane edits that pin in the same commit; if a stored artifact must be regenerated, the lane STOPS and asks (that is a data change, not a comment). Size S.

### Not counted (conditional)

- **MPSCALC-195 residue:** NOT a lane today. The pickup (line 65 region, the #209 summary) says "MPSCALC-195 stays open (clause 3 words + engine-target sentence text not on record)". Clause 3 ("(whole seconds, at least 1)" at `docs/API.md:768`, lane H's text verbatim or the parenthesis recorded as agreed) has no agreement on record; clause 5 (the target sentence at `:587`, "it is a what-if only") was accepted by the product owner on 2026-11-11 but the accepted sentence's text is not in the ticket (comment 41070 says "the drafted engine-target sentence is accepted" without quoting it). A card candidate (section 10).
- **MPSCALC-333:** clauses 1 to 4b are all MET by committed rows (comments 40929 and 41231); what is owed is "a stamped reading or a fresh independent review of clauses 1 to 3 at main". That is a records and review job, not a build. Not counted.
- **BACKLOG row [B1649-OWED-3]** (stub observations of #207) unchanged: no ticket, so no lane (carried, question 2 of the morning, default no ticket).
- **MPSCALC-200** (importer coverage table) and **233, 123** (a refusal sentence users see): carried, not launched.

### Excluded (MPSCALC), with the reason

- **By the commission and rulings:** MPSCALC-369 (a record, not a Done), 163 (four counted group runs: a measurement), 372 (needs the deploy card), 407 item 3 (contract wording "Never refused" is the owner's words).
- **Words or contract names awaited:** 194 (the product owner accepted "Tell the user"; the new words wait for him), 169 (a contract field name needs its own approval card; C-68), 118 (not proposed again: the coordinator's judgement of 11-06), 110 (a design rule owed; the ticket stays open because long text can still print two pages), 139 (axe: a new dependency is a decision), 316 (`needs-ruling`).
- **Hosted or deploy:** 223, 224 (hosted runtime and runbooks), 395 (the showcase seed identity's expired client secret: a credential on a hosted site).
- **Held or card-bound** (carried, each key open now): 135, 364, 189, 121, 130, 78, 120, 402, 222, 103, 226, 123, 124 (PR #171 and #175 landed in part; the open residue was not re-read), 288, 237, 236, 158, 223.
- **The `lane-v` family:** 48 open keys carry a `lane-v*` label (measured now by label match; the morning wrote 42, a different counting rule that I did not reconcile; 2 of the 48 also carry `question-for-kam` or `needs-ruling`). They are feature builds from the v13 pack (new screens, new words): not a one-seat lane; the morning's candidate-pool classifier question still stands (section 10). The 22 keys labelled `question-for-kam` or `needs-ruling` (11 + 11, counted) are the product owner's.
- **The seed epics and tasks** (`spec-seed`, `plan-E01` to `plan-E14`, 68 keys with `mpscalc-seed-2026-09-30`): plan headings and build-plan tasks, not agent tickets.

## 4. NexusAI (RD): 4 lanes (7 keys), one seat at a time

Open 869 (To Do 363, Testing 290; measured 20:31). Main `e3720686`; open PR #215 (records, HISTORY.md only). Done today and not re-proposed: RD-771, RD-805's emailService-side dismissals (seven alerts dismissed on the product owner's word: 143, 144, 147, 148, 149, 150 and 142; RD-804 Done), RD-999 (#212), RD-998, RD-985, RD-996 (#214; each comment says it moves to Testing, and the board shows Testing for all three). RD-1001 was filed (the records working copy's stale `core.sshCommand`).

### Excluded first
- **RD-1001** (stale `core.sshCommand` on a volume that is not mounted): a configuration write "belongs to the launcher or an owner, not to a records pass". Tuesday runs the launcher once and reads the value back; not a seat lane.
- **RD-999** (Testing, landed), **RD-810** (alert #151 `tests/uat-run.js`: ruled "stays"), **RD-805** (To Do: alerts #145 and #146 in `entraProvisioning.js` stay open; "nothing is decided for them"; dismissal is the product owner's call, C-190).
- **RD-1000** (POST /api/chat has no length bound): "the product owner chooses the bound"; edits `backend/server.js`. A card candidate.
- **RD-768** (alerts #112, #113 insecure temporary file; mode 0600 clears both but "a file mode change is visible to the product"): carried held; edits `jsonStorage.js` and `emailService.js`.
- **RD-405** (SCIM mapping edits): item 2 was measured true today (comment, 15:20) with "No decision is needed from the reader", but the fix makes a SCIM save refuse mappings it accepts now, which needs a new refusal sentence (words) and touches a provisioning route; carried as conditional, not counted. Item 6 is a two-line test-hygiene fix in `__tests__/rd388-provisioning-concurrency.test.js` that could ride NX-T3 if Tuesday wants it (not counted).
- **RD-763, 764, 806** (13 `server.js` alert rows; design judgements, RD-806's build is RD-994), **RD-807** (Testing: alerts #73, #74 `incidents.js` still open; zero hits in pickup and daily note, unchanged from the morning), **RD-997** (design decision on `server.js`), **RD-820** (needs a seam), **RD-983** (landed in #208; its note asks only a verification and a move), **RD-930, 931** (HELD), **RD-605** (the remaining Node 20 pins are in `deploy-demo.yml:58` and `deploy.yml:92`, and the `runs-on` pin is a decision; those are the deploy workflows under the demo hold), **RD-731** (13 of 14 suites done; the fourteenth is named for RD-576), **RD-757 and RD-740** (flaky cells with undetermined causes: a measurement), **RD-984 and RD-742** (dev-only, no patched release), **RD-725, 572, 570, 539, 534, 530** (test-tool guard strength; larger and unread beyond the first lines; carried as the test tail), RD-117, 188, 989, 990 and 927 (roles and routes: held for rulings), 610, 612, 622, 644, 433, 893 part 2, 896, 974, 975, 702, 636, 522, 966, 932: held for rulings or words, carried.
- **The erasure family** (RD-744, 745, 750, 824) is row C4, Opus, never a Sonnet kit.
- **The demo hold (C-224):** nothing deploys. Testing (290) and Release Ready (199) are not work. The 7 Put on Hold keys (RD-743, 104, 93, 41, 33, 32, 18) and In Progress 8 (RD-662, 643, 450, 432, 431, 427, 81, 49) are marketplace, operations and demo items: excluded. 253 To Do keys carry the `operations` label (counted); the ones read today are listed here, the rest were not opened and are not counted.

### Buildable now

**NX-R: role table row** (RD-995; the product owner's 2026-11-16 ruling on RD-992, "Keep its own check", card ruled choice a). At main `e3720686`: `docs/ROLE-CAPABILITIES.md:137` reads "... any signed-in session (anonymous refused; viewer reaches the handler 400); handler gate: none" for `POST /api/feedback/:id/coordinator-action`; `backend/services/capabilities.js` lists it at `:174` and `:227` (printed today). The change: the row note says the route answers 403 unless the request comes from the loopback address or carries the shared header value, that no page calls it, and that the product owner chose to keep it; the route leaves the pending list at `:227`. The builder first reads what each list means (the comment says the census test recomputes the pending set and fails on drift) and runs the project's inventory command. Behaviour does not change; the note is developer text. Gate G1 by default (the file is the role table; the morning's question 5, default G1).

**NX-T3: test tail** (RD-1002, RD-734, RD-729, RD-730). Four existing test files, no product file, one counts file.
- **RD-1002** (filed today by the records pass): the header of `__tests__/rd969-three-routes-empty-request.test.js` says "Seven cells" (line 12) and the index (lines 23 to 26) lacks H6, H7, H8; the file holds 11 cells. Comment lines only; the file stays at 11 cells, all green; "no cell count that goes stale again".
- **RD-734:** `__tests__/rd638-export-always-ends.test.js:103` says "h.stop() (SIGTERM grace then SIGKILL, 5 s each)" and `:107` sets `E2_STOP_MS = 10000` (both printed today); the ticket (batch-9 gate B-F1) says `h.stop()` waits 20 s (the gate measured 24,042 ms). The builder re-measures the 20 s before changing the constant and the comment (that number is the ticket's, not run here).
- **RD-729:** the harness boot deadline term has no cell; the file is `__tests__/rd648-harness-boot-residuals.test.js` (exists at main, tree list). A new cell, red-first by the gate's M-flat mutant.
- **RD-730 (read first):** `__tests__/handover-gate-table.test.js` exists; the code that holds `shaFormatProblems` and `gateRows()` was not located here (UNMEASURED: it may be a product or tooling file). If it is outside `__tests__/`, RD-730 leaves the lane.
No words, no migration. The 06:00 NX-T2 kit rule "an edit of an existing test is a STOP" belonged to the NX-P seat's kit, not to this one.

**NX-A: audit entry field checks** (RD-994, Opus, row C3). Built on the product owner's ruling `nexusai-audit-details-size-cap-1116` (choice b, "Check each entry type's fields instead"). Owns the `auditLog` call sites in `backend/server.js` (`function auditLog(action, details, req = null)` at `:305`; `auditLog(` matches 49 lines in the file at main, of which the ticket counts 48 sites: census first), one NEW test file, the counts file. Per the ticket: state each kind's fields, types and length limit, check where the entry is built, red-first one over-long and one wrong-type cell per kind. **How an over-long value is shown must be the same for every kind; if that needs the product owner's word the seat asks on the ticket.** Shares `backend/server.js` with RD-1000 (waiting) and NX-C: those must not run beside it.

**NX-C: stale comments** (RD-689, three shipped comments carry a demo revision name and the retired 4.x VM address). Printed today: `backend/server.js:832` holds a comment naming a Container Apps revision (`...csp-ro revision`); `backend/services/schedulers/healthSweeperScheduler.js:22` holds the retired VM address in a comment (the value is not repeated here). The ticket's `:767` and `:1030` have moved (the file grew); the builder finds each by text. The 10-05 ticket comment says the 5 REVIEWED entries of `__tests__/rd385-shipped-root-markdown-identifiers.test.js` must be deleted in the same change (the wider stale guard RD-708 landed). Runs after NX-A because both edit `backend/server.js`.

**Order and contention.** All four share `scripts/verify-expected-counts.json` and the single jest lock. One NexusAI seat at a time, each on the main the previous landing left; open PR #215 (HISTORY.md only) lands first or the seat rebases. Order: NX-R, NX-T3, NX-A, NX-C.

## 5. Vision Sales Portal: excluded whole, not re-swept

Not re-read tonight (read-only sweep; the 06:00 sweep measured 16 Backlog, main `6dbffdf3`, four Dependabot PRs). The 2026-09-29 pause stands (lesson `2026-10-12_boot-sweeps-all-feedback-repositories.md`: lifted for QuickQuote FEEDBACK work only) and the product is production. Not swept by the commission: myPKI, CypherKey, Lead_Bot.

## 6. Pickup and daily-note check (held and dropped)

Greps over `NEXT-PICKUP-TUESDAY.md` and `daily_tuesday/2026-11-17.md`, by key: HPSMPOC-507 and 508 (named only as filed by R259; no hold), MPSCALC-410 (the pickup's one instruction: ask Kam about `openapi.json:751`), MPSCALC-195 (stays open; words not on record), MPSCALC-207 (carried as the PANEL-BLOCK lineage note), RD-994 and RD-995 (named as lanes NX-A and NX-R by the 06:00 sweep; no hold), RD-1002 (To Do; the stale rd969 header), RD-405 (a slot note saying item 2 already names the gap: no duplicate ticket), RD-730 and RD-731 (named in an old HANDOVER, "next RD-730" in B1431, not a hold). RD-689, 734, 729: zero hits in either file. Zero hits is zero of this instrument: the positive controls (RD-994 returned hits in both files; MPSCALC-410 hit four times) fired. No DROPPED or HELD line sits on a lane key. The 11-17 14:44 card note ("no. that was only an instruction to Friday... You and wednesday can continue as planned") means no restriction on new agents applies to Tuesday.

## 7. WAITING ON KAM (items for the next cards)

Open cards on the store were not enumerated (`list` is never used). Items named in this sweep as needing the product owner or Kam: HPSM: the HTML phase (21), 13 held, 356 residue, 237; MPS: 22 labelled `question-for-kam` / `needs-ruling`, plus 195 clause 3, 169, 194, 407 item 3; Composer: PCOMP-128, 129, 46, 94 and the Guided hold; NexusAI: RD-1000 (the bound), RD-768 (file mode), RD-805 alerts 145 and 146, the 15 keys carrying a `needs-decision` / `needs-kam` / `kam-decision` / `needs-ruling` / `owner-kam` label (counted); Vision: the pause. Not counted: words inside ticket bodies not read.

## 8. Disjointness check (by path)

- **HPSM:** H-T (`remediation-store.test.ts`) and H-D (`web/package.json`, `web/package-lock.json`) share no file. Both are in `web/`, so each runs the web suite on its own head; the lock change does not touch H-T's file. No HPSM pane live (pickup: no pane live).
- **MPS:** M-D3 (`docs/API.md`) and M-I (`PriceBookImporter.cs` plus a pinning test if one exists) share no file. If M-D3's openapi branch opens, `docs/api/openapi.json` and `web/src/api/generated/**` join M-D3 only. Serial in one seat is fine.
- **NexusAI:** NX-R (`docs/ROLE-CAPABILITIES.md`, `capabilities.js`, regenerated inventory), NX-T3 (four `__tests__` files), NX-A (`server.js` audit sites, one new test), NX-C (`server.js` comments, `healthSweeperScheduler.js`, `rd385` test). Path-disjoint except NX-A and NX-C on `server.js` (serial, NX-C second) and the shared counts file and jest lock (one seat at a time). NX-R's change to the committed inventory matters to any lane that runs `role-capability-inventory.js --check`: it compares to the committed file at each lane's own base. The records PR #215 changes `HISTORY.md` only.
- **Across projects:** three different repositories, different `GH_CONFIG_DIR`, different Jira projects: no shared file. Only the machine-load rule couples them.

## 9. Recommended order

1. **NX-R** (RD-995; S): smallest NexusAI lane; ruled; no lock holder now (R260 is a records seat and idle).
2. **M-D3, then M-I** (MPSCALC-410, then 207; S, S): one MPS seat, serial, docs then one literal; ask Kam the openapi.json:751 question on the next MPS card in parallel (the lane does not wait for it).
3. **H-D** (HPSMPOC-508; S to M): highest value of the small lanes (a published advisory against the pinned framework), one repository, no deploy.
4. **NX-T3** (RD-1002, 734, 729, 730; M): waits for NX-R to land (jest lock, counts file).
Then **H-T** (HPSMPOC-507; S), **NX-A** (RD-994; L, Opus; after NX-T3), **NX-C** (RD-689; after NX-A). Lanes 1 to 3 may run together if load1 < 7; one waiter on each project's lock.

## 10. Card candidates (one line each: question and recommended default)

1. **MPSCALC-410 / openapi.json:751:** does the contract file's same clause change with `docs/API.md`? Default: yes, change it in step through the project's own regeneration tool (the contract must not say what the docs no longer say); M-D3 starts docs-only without waiting.
2. **MPSCALC-195 clause 3 and the engine-target sentence:** record the added parenthesis "(whole seconds, at least 1)" as agreed, and paste the accepted engine-target sentence text on the ticket? Default: yes, record as agreed (it states the code's behaviour), and name the decision-register file that holds the sentence.
3. **RD-1000, the chat message bound:** which length? Default (mine, unmeasured as a limit; the ticket measures 506 to 622 ms at 1,000,000 characters): refuse a chat message over 100,000 characters with the existing error shape, and a route body limit well under 50 MB; the product owner may pick another number.
4. **HPSMPOC-356 residue:** commission the unread workflow step bodies and inputs of `test_ci_workflow.py`, or record them as not wanted? Default: record as not wanted (bumps of a hash, tag or digest are deliberately no edit; the bounded part landed in #311).
5. **RD-805 alerts #145 and #146** (`entraProvisioning.js`, a GUID check guards them, code scanning still reports): dismiss as intended or leave open? Default: leave open (the ticket says nothing is decided; dismissal is the product owner's call).
6. **HPSMPOC-507** (small): keep the 100-unit result with a lone surrogate last, or end before it? Default: keep and pin (the ticket's default; Tuesday may approve this without a card).
7. Carried unchanged: RD-768 file mode (default leave; rides with any `jsonStorage.js` lane), the 48 `lane-v` MPS keys (default leave; commission a read-first classifier after the NexusAI lanes), Vision pause (default leave).

## Method and disclosures

- Instruments: `jqdump.py` (GET-only; credentials read in-process from each project's own `4_Credentials/.env` by variable name, never printed) for eight board dumps and four `updated >= "2026-11-17 05:50"` dumps; `bc.sh` (wrapper of `board_count.sh jira`) for eight counts; `jdesc.py` and `jcom.py` (GET-only) for ticket bodies and comments: HPSMPOC-482, 507, 508, 356, 323, 99, 467, 506, 478; MPSCALC-410, 195, 207, 333, 194, 169, 118, 124, 110, 223; PCOMP-66, 67, 64, 12, 11, 9; RD-1001, 1002, 1000, 805, 995, 994, 807, 985, 998, 996, 983, 734, 730, 729, 757, 731, 740, 572, 570, 539, 605, 689, 854, 725, 405, 768. `rg.sh` (one file at a time through `gh api -X GET repos/<repo>/contents/<path>` at main) for every "printed today" line; `gh api -X GET` for mains, `pulls` and `code-scanning/alerts` and one git-tree list (`rd_tree.txt`), each under its project's own `GH_CONFIG_DIR`. Scripts were copied from `fleet/state/s285/sweep0600/`; `jcom.py` is new (GET-only).
- Not measured: whether any pane currently holds a ticket here (no pane list read; the 20:21 daily note names R260 only); which files the NexusAI inventory command regenerates; where `shaFormatProblems` lives (RD-730); whether a test pins the PANEL-BLOCK lineage text (MPSCALC-207); the 20 s of `h.stop()` (RD-734, the ticket's number); whether `next` 16.4.5 exists on the registry (HPSMPOC-508); the bodies of the 253 `operations` To Do keys beyond those listed, the 48 `lane-v` keys, and the NexusAI `qa-gate-finding` and `b1341` keys beyond the test-tail sample; any live feedback store (not read, as at 06:00); Vision (not re-swept). The reconciliation of the 06:00 "42 lane-v keys" with the 48 label matches counted now.
- Correction note: a first draft of this file carried an interim tally and a muddled RD-1002 explanation; both were rewritten after the 20:31 re-measurement above (the BLUF and the census row now agree with `rerun/`).
- Outside the one-output-file rule: the scratch folder named at the top. No `decision_queue.sh list`, no WEDNESDAY, FRIDAY, Secuura tree read, no ledger file read, no mail, no hosted HTTP, no `az`. Hooks refused or advised four times (a `cd`, a `=====` echo word, a `$R` word-split, a grep-into-cut advisory); each was fixed by rewriting the command. One grep pattern hit a regex repetition limit and one ran past two minutes (a catastrophic pattern); both were abandoned and redone with plain patterns. Clocks come from `date`.

READ-WHOLE-BY-TUESDAY: ____
