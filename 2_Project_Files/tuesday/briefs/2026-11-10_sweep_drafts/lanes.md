# HPSM-POC agent lanes: what agents can do NOW (drafted 2026-11-10 for Tuesday)

Marks: MEASURED = the drafter read it from an instrument named beside it. RELAYED = taken from the task text or a ticket and not re-read. UNMEASURED = not checked.

## BLUF

- **6 lanes, 33 tickets, plus the 5 tonight follow-ups (a to e).** 4 code lanes (L1 web UI, L2 web server and lib, L3 API, L4 CI and tooling), 1 documents lane (L5), 1 records lane (L6, Jira and CLARIFICATIONS only, no code).

| Lane | Tickets | Count |
|---|---|---|
| L1 web UI | 439, 357, 405, 399, 431, 408, 323 (+ follow-up d, after PR #297 merges) | 7 |
| L2 web server and lib | 234, 235, 228, 343 (+ follow-up c) | 4 |
| L3 API | 99, 315, 226, 436, 428, 322 (+ follow-up b) | 6 |
| L4 CI and tooling | 352, 356 (+ follow-up a) | 2 |
| L5 documents (drafts, nothing sent) | 169, 170, 171, 173, 174, 175, 176 | 7 |
| L6 records | 109, 318, 271, 368, 370, 372, 383 (+ follow-up e, both parts) | 7 |

- **Census (MEASURED).** Jira REST `search/jql`, `project = HPSMPOC AND ( statusCategory != Done ) ORDER BY key ASC`, `maxResults=100`: page 1 = 100 issues (isLast False), page 2 = 44 issues (isLast True); **total 144** (141 Backlog, 3 In Progress; 133 Task, 10 Epic, 1 Sub-task). Capped query paginated to its end by the `nextPageToken` until `isLast`. Control: the API user's own display name was read (`/myself`), so the auth path works and the 144 are not a silent empty result.
- **Assignee (MEASURED).** 133 unassigned, 11 assigned to Kamil Kreiser. The token's own account (`/myself`) is Kamil Kreiser, so he IS the board account: no ticket is assigned to a different human, and none is excluded on that ground.
- **Excluded: 111 of 144**, every one classified (script `classify.py` asserts 144 of 144 classified, 0 left):

| Bucket | Count | Keys | Why |
|---|---|---|---|
| Phase-2 catalogue | 13 | HPSMPOC-448..460 | Explicitly not to be built now (filed 2026-11-09, B1386) |
| Epics | 9 | 1, 10, 18, 23, 30, 38, 45, 50, 56 | Containers, no work of their own |
| Needs HP, Paul or an HP tool | 23 | 82-86, 92, 94, 96, 97, 162-168, 181, 191, 220, 240-242, 259 | HP answers or access, or HP-tool integration (this phase builds none; next-phase items are stored and architected only) |
| Needs a product-owner ruling, words or SME content | 42 | 5, 6, 12, 16, 19-21, 31, 35, 37, 44, 46, 51, 55, 87, 90, 91, 100, 117, 172, 178, 180, 203, 237, 246, 257, 324, 390-396, 401, 406, 409, 410, 417, 420, 432, 438 | A decision, wording that is the product owner's, or Datasec SME content |
| Deploy or hosted/UAT host | 18 | 24, 29, 57, 58, 60-64, 126, 193, 196, 207, 224, 303, 304, 309, 362 | Needs a deploy, Azure, Entra or a hosted measurement |
| Seed-plan tasks, state unverified | 5 | 11, 14, 47, 48, 52 | Original 2026-09-23 plan rows; cannot tell from the ticket whether they are built (UNMEASURED); see L6 |
| Waits on others | 1 | 389 | "After all lanes merge", plus screenshots for the product owner |

  (The HP row's key list is the 23 keys 82, 83, 84, 85, 86, 92, 94, 96, 97, 162, 163, 164, 165, 166, 167, 168, 181, 191, 220, 240, 241, 242, 259.)
- **The backlog is stale in places (MEASURED at fa401da9, the main named by `git ls-remote origin refs/heads/main` = `fa401da9f7bdab21c46ad9717c964433a2d22650`).** At least 109, 318, 228 (N-2 and N-4), 399 (B908-4), 323 (B478-2) and 271 (SDK pin) already have their fix on main (details in L6 and the tables). Every code seat therefore starts with a **read of the ticket's cited lines at main**; if the fix is already there, the seat reports "closed with evidence" to L6 and does not re-build it.
- **Disjoint by path (MEASURED).** `disjoint_check.py` (beside this file) tests 1491 tracked paths of main plus 259 synthetic new-file probes (one per existing directory) against each code lane's include/exclude globs: **0 paths owned by two lanes**; a control that adds a second owner for `web/src/lib/**` fires 46 overlaps (so the check can fail). 61 paths are owned by no lane (for example `web/package.json`, `global.json`, `.tools/`): nobody touches them in this sweep. L5 and L6 live in the analysis tree (`1_Project_Definition/`) and the Jira site, a different root from the four code lanes; they share no path with each other.
- **Local checkout is stale.** `.tools/b1380/repo` has `origin/main` = `2075486b` and no `fa401da9` object (`git cat-file -t` fails in all 7 local clones); all main reads here are `gh api -X GET contents/<path>?ref=fa401da9...` (GH_CONFIG_DIR of the project). Seats must work from a fresh clone of main, not from those clones.

## Rules every lane carries

- Branch from main (`fa401da9` or later), push only your own branch, Tuesday lands through CodeQL (never bypass or dismiss).
- Own only the paths in your section; anything else you need: STOP and report.
- Run the project's CI predicates for the jobs your files feed (below). In `ci.yml` a step printing "SKIPPED" (typecheck, unit tests, infra) is NOT a pass.
- PRIOR-WORK CHECK first (grep the repo and `JQL project = HPSMPOC AND ( text ~ "..." )`). No message to any human. Jira writes: L6 only. Never delete (quarantine). This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only.

CI predicates (from `.github/workflows/ci.yml` at fa401da9, MEASURED by reading the file):
- `web-build`: `npm audit --omit=dev --audit-level=high`; `node scripts/audit-dev.mjs`; lint; `npm run typecheck`; build; `node scripts/e2e.mjs --check-shards` (the shard plan runs every Playwright test exactly once).
- `web-unit`: `npm test` (vitest). `web-e2e (<shard>)`: `node scripts/e2e.mjs --shard "$SHARD"`.
- `api`: `dotnet test HpsmPoc.slnx -c Release --no-build` plus "the 10 Azurite tests ran and passed, by name". `api on SQL Server (<part>)` shards and the roll-up job `api on SQL Server`: the same tests on SQL Server (HPSM-POC API test rows ask "does it run on SQL Server as CI does?").
- `infra`: `bash infra/scripts/validate.sh`; every tracked `*.sh` passes `bash -n` and shellcheck 0.11.0; infra python tests (`infra/tests/test_*.py`).
- `secrets` (gitleaks, full history) and `dependency review` must stay green.

---

## L1 web UI (7 tickets + follow-up d)

**Owns:** `web/src/components/**`, `web/src/app/**`, `web/src/content/**`, `web/src/server/mock/**` (except `web/src/server/mock/customer-name.test.ts`, L4), `web/src/styles/**`, `web/src/assets/**`, `web/e2e/shell-sidebar.spec.ts`, `web/e2e/playbook-feedback-pill.spec.ts`.
**NOT yours:** other `web/e2e/**` (L4); `web/src/server/**` except mock, `web/src/api/**`, `web/src/lib/**`, `web/src/instrumentation.ts`, `web/src/proxy*` (L2); `api/**` (L3); `.github`, `infra`, `scripts`, `web/scripts` (L4); `web/package*.json`, config files (nobody).
**Checks:** web-build (lint, typecheck, build), web-unit (vitest for each touched component), web-e2e for the touched specs, `a11y.spec.ts` and `responsive.spec.ts` shards unchanged green (read-only for you; run them).
**Size:** M in total (each ticket S).

| Ticket | Summary | Type / status | Files (main fa401da9) | Size | State at main and why agent-actionable |
|---|---|---|---|---|---|
| HPSMPOC-439 | Engagement overview: a linked single-line title sits 20 px above its detail line | Task / Backlog | `web/src/components/customer/EngagementOverview.tsx` (Link `inline-flex min-h-11 items-start` at the activity title and Next milestone rows, MEASURED lines 221 and 241 by grep) | S | Still as the ticket says (MEASURED). A look-only fix; the gate says no word needed. The gate's two tried shapes were declined, so the seat must pick a third and measure 460-row spacing |
| HPSMPOC-357 | Customer page scrolls sideways at 360 px (374) from the stage badge | Task / Backlog | `web/src/components/customer/**` stage badge (file unnamed by the gate; UNMEASURED which; `whitespace-nowrap` also at `CustomerManagement.tsx:61,344`, not the badge) | S | Layout only; done-when is a program (scrollWidth equals viewport at 360) |
| HPSMPOC-405 | Fixed Feedback pill sits over a list page's only row button at 768x1024 | Task / Backlog | `web/src/components/feedback/FeedbackPill.module.css`, `web/e2e/playbook-feedback-pill.spec.ts` | S | `FeedbackPill.room.test.tsx` exists at main, so it may be partly fixed (UNMEASURED); verify first |
| HPSMPOC-399 | After PR #240: items B908-4, -6, -7, -8 | Task / Backlog | `CustomerManagement.tsx`, `web/e2e/shell-sidebar.spec.ts`, sidebar CSS under `web/src/components/shell/` | S-M | **B908-4 is fixed at main**: the row menu is `fixed` positioned (`CustomerManagement.tsx:107-120`, MEASURED), so it no longer clips. Open: -6 (test row measures before the table renders; same class as follow-up a), -7 (6 px at 390 under wide letter spacing), -8 (focus ring crosses the accent band) |
| HPSMPOC-431 | Documents tab at 360/375 px: readiness sentence in a 50 px column | Task / Backlog | `web/src/components/customer/DocumentGeneration.tsx:145` | S | Main now has `min-w-0 flex-1 not-empty:basis-60` there (MEASURED), i.e. probably fixed; verify at 360/375 and report "closed with evidence" or finish |
| HPSMPOC-408 | Remediation register after PR #257: items 1 and 3 | Task / Backlog | the register's `checkEntry` (under `web/src/components/screens/` or `web/src/lib/`; UNMEASURED which; if it is under `web/src/lib/` STOP, that is L2's) | S | Item 1: treat zero-width, braille blank and BOM as blank, with a pin row (the gate's own fix shape). Item 2 needs real sentences = the product owner's words: **not in this lane**; item 3 is storage pins |
| HPSMPOC-323 | Web and mock side of the customer and comment refusals | Task / Backlog | `web/src/api/client.ts:317-320` is L2's; this lane takes the mock shape (`web/src/server/mock/**`) and the edge-trim in `FeedbackButton.tsx` and `CustomerManagement.tsx` | S | B478-2 (a 400 shows the API's words) is **fixed at main** (`client.ts:318` comment, MEASURED). Open: B478-4 mock shape, B478-5 edge characters (`*.edgeTrim.test.tsx` exist, so verify) |
| follow-up (d) | Walkthrough step 10 caveat wording (gate finding B1390-1) | n/a | `web/src/content/walkthrough/steps.ts:130` | S | **Only after PR #297 merges.** MEASURED: PR #297 is open, not merged, head `60639d15`; `steps.ts` does not exist at main (404) and has 249 lines on the PR head, where line 130 is the `caveat:` of the report step ("...On the laptop sample the report waits for the approved narrative; do not promise that wait for every customer."). The finding text itself is RELAYED |

## L2 web server and lib (4 tickets + follow-up c)

**Owns:** `web/src/server/**` except `mock/**`, `web/src/api/**`, `web/src/lib/**`, `web/src/data/**`, `web/src/design/**`, `web/src/instrumentation.ts`, `web/src/proxy*`.
**NOT yours:** `web/src/components/**`, `web/src/app/**`, `web/src/content/**`, `web/src/server/mock/**` (L1); `web/e2e/**`, `web/scripts/**`, `web/src/e2e-runner*` (L4); `api/**` (L3).
**Checks:** web-build, web-unit (`bff*.test.ts`, `auth/*.test.ts`, `lib/*.test.ts`); `bff.ts` changes also run the e2e shards that call the BFF.
**Size:** M.

| Ticket | Summary | Type / status | Files | Size | State and why agent-actionable |
|---|---|---|---|---|---|
| HPSMPOC-234 | Web-side warm-up after a start | Task / Backlog (assignee board account) | `web/src/server/auth/warmup.ts`, `web/src/instrumentation.ts`, `web/src/server/bff.ts` | M | `auth/warmup.ts` and `signin-warmup.test.ts` exist at main (MEASURED by path), so part may be built; read first. The code half is agent work (a start-up GET with no session and no non-GET, with a test). Closing needs the hosted measurement (HPSMPOC-309, excluded): the seat ends at "code merged, ticket stays open" |
| HPSMPOC-235 | BFF to API connections: keep them open longer | Task / Backlog | `web/src/server/bff.ts`, `bff.keepalive.test.ts` | S-M | `bff.keepalive.test.ts` exists at main, so this may be built (UNMEASURED); read first, same closing rule as 234 |
| HPSMPOC-228 | B176 gate notes on B175 (site timing) N-2..N-9 | Task / Backlog | `web/src/server/bff.ts` | S-M | **N-2 (dead readiness regex) and N-4 (lowercase route segments) are fixed at main**: `NAMED_WRITES` has four entries and none is readiness; `routeTemplate` keeps only `ROUTE_WORDS` (`bff.ts:161-165,275-277`, MEASURED). N-3 (R11 guard blind to the dispatcher timer) sits in an infra or API test that I could not locate (UNMEASURED): not in any lane, report if found. Open: refresh fan-out, warm-up log level, words, stale comment |
| HPSMPOC-343 | Which fields does the API refuse for the browser sites in session.ts, override.ts, action-plan.ts | Task / Backlog | read-only: `web/src/lib/session.ts`, `web/src/lib/override.ts`, `web/src/components/partner/action-plan.ts` against `api/.../Requests.cs:146,221,224` | S | A read-only trace; the output is a table file handed to L6 for the Jira comment; no code change. (action-plan.ts is under L1's directory: read it, never edit it) |
| follow-up (c) | `web/src/lib/dates.test.ts` fails on Node 26 ICU ('Jul' vs 'July') | n/a | `web/src/lib/dates.test.ts` (the 'July' expectation at line 36 MEASURED; `dates.ts` formats) | S | Local only (RELAYED: I did not run Node 26; the repo's pinned node is the CI node). Fix by making the assertion independent of the ICU short-month spelling or by pinning the formatter, and prove on Node 24 (`.tools/node24`) and Node 26 |

## L3 API (6 tickets + follow-up b)

**Owns:** `api/**` except `api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs` (L4, ticket 352).
**NOT yours:** all `web/**`, `.github/**`, `infra/**`, `scripts/**` (L1, L2, L4); migrations are frozen unless the ticket says otherwise: do not add one.
**Checks:** `dotnet test HpsmPoc.slnx -c Release` AND the SQL Server run as CI does (api-sqlserver-shard parts and the roll-up). A change that passes SQLite and fails SQL Server is red.
**Size:** M-L.

| Ticket | Summary | Type / status | Files | Size | State and why agent-actionable |
|---|---|---|---|---|---|
| HPSMPOC-99 | QA gate's open notes N-4, N-7, N-8, N-9 (feedback) | Task / Backlog | `api/src/HpsmPoc.Modules.Feedback/**` | S | N-7 (lease-lost branch logged and audited) looks built: `FeedbackDispatcher.cs:201,256-259` log and audit it (MEASURED); verify the fake-clock lease test exists. N-8 (invisible-only comment residue): verify at the comment endpoint, then fix. N-4 needs the product owner's route ruling and N-9 needs hosted scale-out: leave both |
| HPSMPOC-315 | Feedback test `Hpsmpoc214Tests.N1(200,400,"sent")` read the wrong lease-lost note (1 in 60 shard runs) | Task / Backlog | `api/tests/HpsmPoc.Modules.Feedback.Tests/Hpsmpoc214Tests.cs:329`, `FeedbackDispatcher.cs:255-261` | M | Cause unmeasured (RELAYED). Agent-actionable: reproduce under load on SQL Server, find whether the product text or the test's ordering is wrong, then fix with a test that fails first |
| HPSMPOC-226 | Feedback attachments follow-ups | Task / Backlog (board account) | `api/tests/**` for the export test | S | Per its own 2026-10-19 refresh only "the optional N-9 pin (the export test asserts file names only)" is agent work; B177 N-1 is words (not in this sweep) |
| HPSMPOC-436 | Offline template: finding explanation of zero findings is written with zero paragraphs and refused | Task / Backlog | `api/src/HpsmPoc.Modules.Reporting/Narrative/Providers.cs:53` | S-M | Still true at main (`Select` over `input.Findings`, MEASURED). First measure whether any endpoint can ask for zero findings (the gate did not), then fix the template or the validator rule |
| HPSMPOC-428 | During a database wake the API answered one read with HTTP 500 at 29.5 s | Task / Backlog | `api/src/**` data-access configuration | M-L | `EnableRetryOnFailure` count in the 6 fetched API files = 0 (no positive control: it is a wider question than those files; UNMEASURED repo-wide). The fix shape (a transient-retry and connect budget longer than a wake) is code; prove it with a SQL Server fault-injection test, not a hosted wake. If the seat cannot prove it offline, it stops at the test |
| HPSMPOC-322 | Grouped executive summary findings B477-5..8 | Task / Backlog | `api/src/HpsmPoc.Modules.Reporting/Narrative/Providers.cs`, `NarrativePipeline.cs`, `NarrativeOutputValidator.cs` | S-M | The grouped summary IS on main (`SharedActions.Partition` at `Providers.cs:73-76`, MEASURED), so the ticket's "branch b467 only" is stale. B477-5 to -7 are code/validator; B477-8 is wording (leave it) |
| follow-up (b) | `ShowcaseSummaryTests` answered 500 once under load | n/a | `api/tests/HpsmPoc.Api.Tests/Assessment/ShowcaseSummaryTests.cs` (4 `[Fact]` tests, first at line 31, MEASURED) | M | Cause UNMEASURED. Seat: loop the class under CPU load on SQL Server and SQLite, capture the 500's problem body and log, then root-cause; no fix without a failing reproduction. Overlaps nothing in L4 |

## L4 CI and tooling (2 tickets + follow-up a)

**Owns:** `.github/**`, `infra/**`, `scripts/**`, `web/scripts/**`, `web/e2e/**` except the two L1 specs, `web/src/e2e-runner*.test.ts`, `web/src/audit-dev.test.ts`, `web/src/standalone.test.ts`, `web/src/web-settings.test.ts`, `web/src/productName.test.tsx`, `api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs`, `web/src/server/mock/customer-name.test.ts`.
**NOT yours:** `web/src/components/**`, `web/e2e/shell-sidebar.spec.ts`, `web/e2e/playbook-feedback-pill.spec.ts`, `web/src/server/mock/**` otherwise (L1); `web/src/server/**`, `web/src/lib/**` (L2); the rest of `api/**` (L3).
**Checks:** `infra` job (`validate.sh`, shellcheck, `python3 -m pytest infra/tests` as CI runs it), `web-build` (`--check-shards` must still say every test runs exactly once), `web-e2e` shards that contain a touched spec, and the shard the changed test lives in run 5 times under load (the follow-up a failure only shows under load).
**Size:** M.

| Ticket | Summary | Type / status | Files | Size | State and why agent-actionable |
|---|---|---|---|---|---|
| follow-up (a) | `web/e2e/html-layout.spec.ts` T06 and T09 count the dashboard table head before data renders | n/a | `web/e2e/html-layout.spec.ts` | S | Verified at source (MEASURED): T06 (line 130) and T09 (line 174) call `frame(page, "/home", mainOnly)`, and `mainOnly` waits only for `main#main h1` (line 38); the style reads `main th[scope=col]` and `main span[data-tone=info]` straight after. Other frames wait on the data (`dashboardReady`, `findingsReady`, `homeReady`). Fix: a `ready` that waits for the head or pill element's data (as `homeReady` does), then the style read; same fix for HPSMPOC-399 B908-6 is L1's file. Prove with 5 runs under load |
| HPSMPOC-352 | After PR #212: edge-space cells over a plain held name, two raw-slice rows in e2e-runner tests, ciMatrix and a YAML comment | Task / Backlog | `Hpsmpoc178CustomerNameTests.cs:512-552`, `web/src/server/mock/customer-name.test.ts:335-360`, `web/src/e2e-runner.test.ts`, `web/scripts/e2e.mjs:90-93` | M | Test-only and tooling-only; the gate gives mutants X12b/Xm12b that must go red. Spans three trees, which is why the two customer-name test files are carved out to this lane |
| HPSMPOC-356 | `test_ci_workflow.py` after PR #221: docstrings, Unicode white space, line-break characters | Task / Backlog | `infra/tests/test_ci_workflow.py` | S | Test-only; no workflow line changes |


## L5 documents (7 tickets; drafts only, nothing goes to HP)

**Owns (analysis tree, `1_Project_Definition/`):** `Governance/stage-gates/**`, `Deliverables/**`, `Architecture/2026-11-10_*` (new files), `Demo/**`.
**NOT yours:** `CLARIFICATIONS.md`, `Briefs/**` (L6); any code path; anything in `Source_Documents/` (HP material).
**Checks:** none of the code CI jobs. Each draft is marked DRAFT, every claim carries its provenance, no verbatim SOW text, no name of HP staff, no send.
**Size:** M-L in total.

| Ticket | Summary | Files | Size | Agent part |
|---|---|---|---|---|
| HPSMPOC-171 | Testing evidence and known limitations | `Deliverables/2026-11-10_testing-evidence/` | L | Collect suite results from the gate STATUS files and `*_evidence` folders, re-point the acceptance matrix, list open defects with severity from this very census. The frozen build does not exist yet, so mark it "as at <sha>" |
| HPSMPOC-173 | Phase 2 backlog document | `Deliverables/2026-11-10_phase2-backlog/` | M | Draft from HPSMPOC-448..460, 92, 96 and the excluded next-phase tickets; priorities are Kam's, so the draft proposes an order and says so |
| HPSMPOC-169 | Re-base the stage-gate pack and CR log on the signed SOW | `Governance/stage-gates/**` | M | Mechanical re-base to the signed dates and clauses (the ticket lists them); the signed SOW is a git-ignored local file |
| HPSMPOC-170 | Deployment and administration guide | `Deliverables/2026-11-10_admin-guide/` | M | The administration half (users, roles, rulesets, demo reset, feedback route, data-subject requests, backups) can be written from the code; the deploy half is marked UNVERIFIED until a walk-through on UAT |
| HPSMPOC-174 | Weekly status report to HP | `Deliverables/2026-11-10_weekly-report-template/` | S | Template and an hours record format only; hours data is Kam's; sending is his |
| HPSMPOC-175 | AI tools: record of tools and versions | `Deliverables/2026-11-10_ai-tools-record/` | S | The list and versions can be drafted; the two CONFIRM placeholders stay open (tenant, no-training) because they need Kam and HP |
| HPSMPOC-176 | Privacy documents (Datasec is Data Controller) | `Architecture/2026-11-10_privacy-update-draft.md` | M | Update drafts of the RoPA, DPIA-lite, retention and privacy notice; the controller contact is a labelled PLACEHOLDER until Kam confirms |

## L6 records (Jira and CLARIFICATIONS only, no code)

**Owns:** Jira project HPSMPOC (comments and transitions on the listed keys), `1_Project_Definition/CLARIFICATIONS.md`, `1_Project_Definition/Briefs/2026-11-09_B1387_STATUS.md` (an appended correction, never an edit of the old line).
**NOT yours:** every code path, `Deliverables/**`, `Governance/**` (L5). Lands its own records branch; Tuesday does not write a ref in the project repo.
**Checks:** read-back from Jira after each write (status, comment present), a `git diff` showing only the intended files, the highest `### C-` heading read on records main before choosing the number.
**Size:** S-M.

| Item | What | Evidence |
|---|---|---|
| HPSMPOC-109 | Close: O-2 is built | `ci.yml:593-609` "shell scripts (bash -n + shellcheck, every tracked *.sh)", shellcheck 0.11.0 pinned (MEASURED: `shellcheck` occurs 14 times in the file, `actions/checkout` 9 as the positive control). O-1 (delivery proof on route A) is still open and needs a ruling: move it to its own ticket, do not close it silently |
| HPSMPOC-318 | Reconcile | main holds `Slack_is_pinned_to_the_accepted_1200_ms` (`RequestTimingLogTests.cs:183`, MEASURED); the floor-moved finding is accepted in text. Record that and ask for close or decline |
| HPSMPOC-271 | Reconcile; ruling stays open | `ci.yml` now installs the SDK by `global-json-file: global.json`, and `global.json` pins 10.0.401 with `rollForward latestFeature` (MEASURED at fa401da9), so the ticket's floating-channel premise is overtaken. The Pkcs-pin owner and cadence is a ruling: record the pin and ask. An optional early-warning test would live in `api/tests/` (L3) and is not part of this sweep |
| HPSMPOC-368, 372 | Close or move: built | PR #240 (368) and PR #252 (372) are merged per tickets 399 and 406 (RELAYED from those tickets; check the PR state with `gh api -X GET`) |
| HPSMPOC-370, 383 | Close or move: built | B1386's own status says the links "point at built work with a stale Backlog status" (RELAYED, `Briefs/2026-11-09_B1386_STATUS.md`) |
| Follow-up (e1) | File the PROPOSED C-ENTRY into CLARIFICATIONS | The entry is `Briefs/2026-11-09_B1386_STATUS.md` heading line 134, `### C-312` at line 137, end line 148 (line numbers printed by grep -n; the task text said ~133-148). The B1386 file says the number is a proposal: highest heading read there was C-311 on a local ref, so **read records main first and renumber if C-312 is taken** |
| Follow-up (e2) | Correct the B1387 count | `Briefs/2026-11-09_B1387_STATUS.md:29` (MEASURED, line printed) is the "Old-wording count after the change ... 0" line. That a 1-hit existed there is RELAYED: a GitHub code search for the phrase returned fuzzy matches, not an exact count, so I did not confirm the 1. The records seat must re-count with `/usr/bin/grep -rn` at the pinned sha and a positive control, then append the correction |
| Hand-ins | Take the L2 trace of HPSMPOC-343 and the "closed with evidence" reports of the code lanes | Post each as a Jira comment with its instrument |
| Unverified seed tasks | HPSMPOC-11, 14, 47, 48, 52 | Check each against the code and the plan rows; if built, propose the transition; if not, leave. These are reads, not builds |

## Not in any lane (so nothing is lost)

- 228 N-3 (R11 guard location unknown), 271 owner/cadence ruling and its optional early-warning test, 99 N-4 and N-9, 224 (telemetry: needs a package in both trees and a deploy to prove; revisit once L2 and L3 land), 389 (after all lanes merge), and every excluded ticket above.
- The 61 unowned paths: nobody touches them in this sweep.

## How this was measured (instruments)

- Census: `jira.py` (scratchpad), Jira REST GET only, token read in-process, never printed. Class counts: `classify.py`.
- Main: `git ls-remote origin refs/heads/main` (read verb) = fa401da9; file contents and the 1491-path tree by `gh api -X GET` (tree `truncated: False`).
- Disjointness: `disjoint_check.py` in this directory (rerun: `python3 -I disjoint_check.py <paths.txt>`).
- Not run by me (not allowed): any build, test, deploy, `az`, `ssh`, `docker`. So no code claim here is "passes"; each is "reads as" at fa401da9.
