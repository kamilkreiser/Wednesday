# Ticket sweep 2026-10-19: Datasec HPSM-POC (Playbook POC) and Datasec Security Composer

Read-only sweep for Tuesday. Trigger: Kam, live board 11:34 AEDT, "keep going with any and all tickets for the paybook as well as the security". Read between about 11:40 and 12:30 AEDT, 2026-10-19. No HTTP to any app host or hosted site, no az, no docker, no git write verb, no Jira/gh/mail/card write.

## BLUF

| | HPSM-POC (Jira HPSMPOC) | Security Composer (BACKLOG.md) |
|---|---|---|
| Open total | **113** (110 Backlog + 3 In Progress; of 292 issues; 179 Done). Paged to `isLast=true` in 3 pages. | **112** non-terminal rows of 308 (rows #1-#318; 10 numbers absent from the file). Read from the file, not a tracker (see below). |
| A agent-actionable now | **20** | **31** (15 build/doc + 16 records-only) |
| B Kam decision / Kam action | 50 | 29 |
| C HP / Paul / client human | 19 | 4 |
| D blocked / parked | 24 (9 are epic containers) | 22 |
| T terminal in substance (stale state column) | n/a | 26 |
| Proposed A lanes | 7 (L0a, L0b, L1-L5) | 7 (CL0-CL5b) |
| In flight | Nothing. 0 open PRs, no branch for any open ticket. | Nothing. 0 open PRs. Two merged PRs (#78, #79) are NOT on the demo as of the last record (B155, 10-16). |

Lane one-liners.

HPSM-POC: L0a close-outs by evidence (-98, -148, -245, -246, -271); L0b docs refresh (-13, -171, -174); L1 tests only (-291, -227); L2 BFF form guard and timing (-288, -289, -228); L3 API Feedback (-290, -226); L4 API imports and SQLite migrations (-263, -275, -292); L5 infra and CI (-193, -155).

Composer: CL0 one records pass (16 rows); CL2 tooling (#84, #140); CL1 DEPLOY.md and rollback docs (#34, #291, #293); CL3 web CSS residue and Discovery (#75, #123, #154, #57); CL5a two db migrations (#152, #178); CL4 secret-field action and listControls (#104, #169); CL5b renderer (#158, #315).

The biggest unlock on both boards is a Kam word, not an agent: Composer has 20 rows built and merged (main `230f9fab`) that wait only for a demo deploy word; HPSM-POC has 50 rows in B, mostly Kam-reviews-a-draft, hosted-environment and wording items.

## Project 1: Datasec/HPSM-POC (Playbook POC, Jira HPSMPOC id 10588, board 606)

### Current state (provenance in brackets)

- **Last session:** B274 (Seat R7, records round 3), 2026-10-18 23:27 to about 23:55 AEDT. It posted 12 Jira comments, moved 8 tickets to Done (-286, -281, -284, -285, -283, -282, -287, -269), created -288 to -292, and wrote C-116 to C-118 on `records/b274`. The analysis repo main `47a9896e` "Records: B274" merged 2026-10-18T12:57Z (GitHub commits read 10-19). [`1_Project_Definition/Briefs/2026-10-18_B274_STATUS.md`]
- **Code repo `datasecau/HPSM-POC`:** main `befd45e7` (PR #160, merged 2026-10-18T11:05Z). Check-runs on it: 18 success + 1 skipped. Open code-scanning alerts: 0. Open Dependabot alerts: 1 (#1 braces GHSA-vfj7-8cjw-p6xm, high, no patch; the dated exception was renewed to 30 Nov by C-99 per -218's comment). Open PRs: **0** in both the code repo and the analysis repo. Branches: 176 in the code repo, newest `b267/round3-bff-counter-locks-pkcs` (merged); analysis repo newest `records/b274`.
- **Hosted:** B273 deployed `befd45e` (DEPLOYED line). The hosted API still runs .NET **10.0.12** (-268, B273). Imports are switched OFF on hosted. [B274 STATUS, -268 comment]
- **Held, and why:** imports stay off until the product owner approves the sweep reason and the 500 text (-267); .NET 10.0.13 on hosted (-268, needs the platform to move); hosted-demo tuning (-232, -234 parked by Friday's ruling 10-13; -237 is a money decision); the ruleset schema bump waits for the HP-vetted re-issue (-180); next-phase integration is design-only (-259, Kam 10-16); HP-dependent content (-47, -48, -94, -163 and the Awaiting-HP set).
- **Stale local project files (matters for any agent booting from the folder):**
  - `CLAUDE.md` Status still reads 2026-09-23 ("nothing built, no git repo yet").
  - `1_Project_Definition/CLARIFICATIONS.md` ends at C-30 (192 lines); the records repo holds C-118 (1,512 lines at C-115 per B274). `5_Project_History/history.md` newest entry is 2026-10-12 (B228); history B229 to B274 lives only in the analysis repo.
  - The real boot reading is the analysis repo (`records/*`) plus the newest `Briefs/*_STATUS.md` (B274). The folder's `BACKLOG.md` also lists W1 blockers that were since ruled (executed SOW filed C-35, event date C-36 A = 1 Dec).
- **Read:** CLAUDE.md, JIRA.md, BACKLOG.md, history.md top (B228), CLARIFICATIONS headings (C-01 to C-30 local), B274 STATUS in full, B273 name only.

### Classification

Predicate (applied to all 113 open issues, read from the paged Jira search plus each issue's last comments and links):

- **A**: no Kam decision, no human outside the team, not production, money or external comms, and the remaining work is code, tests, CI, docs or a Jira close-out by evidence that a seat may do. Deploys are never A.
- **B**: needs Kam: a ruling, a wording approval, a review/sign-off of a DRAFT, sending something, or anything on the hosted environment, Azure, a money item or production.
- **C**: needs HP, Paul Waite, the Security SME as a person, or a client human (including Awaiting-HP items).
- **D**: blocked or parked on something named, or an epic container (closes when its last child does).

Counts: A 20, B 50, C 19, D 24 = 113. Total from the paged read: 292 issues, 3 pages, last page `isLast=true`; status counts Done 179, Backlog 110, In Progress 3; types Task 276, Epic 9, Bug 6, Sub-task 1.

**A (20):** -13, -98, -148, -155, -171, -174, -193, -226, -227, -228, -245, -246, -263, -271, -275, -288, -289, -290, -291, -292.

- Important caution on five of them: PR #152 (`a6576ce`, B241 Lane 2) already built parts of -245 (N-4, N-5, N-6), -228 (N-3, N-4, N-7), -226 (N-6), -148 (N-3, C-3) and -98 ("Filter by state" on `web/src/components/feedback/AdminFeedback.tsx`). Those tickets are still Backlog with no B241 close-out comment. So -98, -148 and -245 are probably close-outs, not builds; -228 and -226 need a census of what is left before building. -246 and -271 carry merged work (PR #154; PR #159 and gate B263) and their last comments say why they were not moved to Done.

**B (50):**

- Sign-off or review of a DRAFT: -11, -12, -16, -19, -20, -31, -35, -44, -46, -51, -52, -87, -91, -162, -165, -168, -169, -170, -172, -173, -175, -176.
- Rulings: -6 (name the SME and a deputy PO), -99 (N-4: is Kam's Jira rule duplicate-checking), -100 (K10 retention, proposed 12 months), -177 and -178 (refuse invisible characters in feedback comment / customer name), -187 (the second half changes approved text), -203 and -204 (issued-report file name; PDF caption wording), -257 (file-name NFKC over-refusal), -267 (import words owed to the product owner), -241 (Kam sends the HP lab questions), -164 (HP review sessions need a build HP can open), -109 (how delivery of a feedback item is proved).
- Hosted, Azure, money, privacy: -24 (real Entra tenant sign-in in UAT), -29, -57, -58 (branch protection), -60, -61, -62 (UAT and Demo environments, freeze, rehearsal), -90 (feedback route), -126 and -196 (deploy-time measurements on hosted), -220 (stale SM-import umbrella; imports are built and switched off), -224 (telemetry on a demo HP reviewers use: privacy call), -235 (needs hosted measurement), -237 (DECISION FOR KAM, money: larger App Service plan), -268 (move hosted runtime to 10.0.13).

**C (19):** -3 (executed PO), -21 (branding source, HP sponsor), -37 (HP approval of the golden scenarios), -47, -48, -94 (HP-approved recommendation content), -82, -83, -84, -85, -86, -97, -166, -167, -181 (Awaiting HP), -163 (HP vetting of traffic-light meaning), -191 (SM integration, HP answers), -240 (re-test once an HP device is reachable), -242 (placeholder for Paul's showcase feedback; nothing written down).

**D (24):** epic containers -1, -10, -18, -23, -30, -38, -45, -50, -56 (9); -5 (date ruled 1 Dec, ticket held until the event); -14 (schema ticket, tied to -180); -55 (trial runs, blocked on -51); -63 and -64 (event-day and hypercare, not yet due); -92 and -96 (next-phase backlog, by design); -117 (audit ledger: Friday's 10-13 ruling keeps it parked); -180 (schema bump waits for the HP-vetted ruleset re-issue); -207 (start-up pair absent on the latest start; observation ticket); -218 (braces exception to 30 Nov; no upstream patch); -232 and -234 (parked by Friday 10-13); -254 (blocked on -268 hosted runtime); -259 (next-phase design only).

### Proposed lanes for class A (file-disjoint, easy to hard)

Files named from the ticket text and the merged commit file lists; "established" says how sure I am.

| Lane | Tickets | Files touched | Established? |
|---|---|---|---|
| **L0a Close-outs by evidence** | -98, -148, -245, -246, -271 | Jira comments/transitions only, plus records in the analysis repo (`CLARIFICATIONS.md`, `history.md`, Briefs). No product code. | Yes for -246 (gate B245 C4 CLOSED PASS; open only for "N-4 recorded by the next HPSM deploy seat", which B273 was) and -271 (PR #159, gate B263). For -98, -148, -245 I saw the B241 commit that built the named items but did not read their Done-when against the code; the lane must do that. |
| **L0b Docs refresh** | -13, -171, -174 | Analysis repo only: `design-pack/` (-13: check A5 of the 24 pack checks remains), `Governance/handover/` known-limitations and test-evidence index v0 (-171), `Governance/status-reports/` (weekly report drafts, DRAFT FOR KAM, nothing sent) (-174). | Paths from the tickets' last comments (B109/B110). -13's remaining gap (A5) not read. |
| **L1 Tests only** | -291, -227 | `api/tests/HpsmPoc.Api.Tests/**/PkcsInPackageTests.cs` (comment/assert at :168-171); `web/e2e/playbook-content-050-live-api.spec.ts`, `playbook-live-api.spec.ts`, `playbook-narrative-stale-live-api.spec.ts`. | Yes (named in the tickets). -227 may also want CI to run the opt-in specs: that would touch `ci.yml`, which is L5, so keep CI out of L1. |
| **L2 BFF form guard and timing** | -288, -289, -228 (remaining items) | `web/src/server/formGate.ts` and its tests (-288 tests, -289 header-line limit at `isFil*`), `web/src/server/bff.ts` (-228 remaining), `infra/tests` R11 guard (-228). | -288/-289 yes (formGate.ts:175-187, `HeadersCountLimit` 16). -228 only partly: N-3, N-4, N-7 are built; N-2, N-6, N-8, N-9 status not read. Needs a census first. |
| **L3 API Feedback module** | -290, -226 (remaining items) | `api/src/HpsmPoc.Modules.Feedback/Endpoints/FeedbackFiles.cs` (:360 catch `NotSupportedException`/`FormatException` to 400), `Delivery/FeedbackDispatcher.cs`, `api/tests/HpsmPoc.Modules.Feedback.Tests/**`. | -290 yes. -226: N-6 built; N-4, N-5, N-7, N-8 open per its description; N-3 and N-9 are "confirm as built" (POC-8 default a). Its BFF total check is done, so no `bff.ts` here. |
| **L4 API imports and SQLite migrations** | -263, -275, -292 | `api/src/HpsmPoc.Modules.Assessment/Ingest/ImportEndpoints.cs` (-263 phase 2 from :119; -275 FailAsync), `api/src/.../Persistence/Migrations/Sqlite/*` (five table-rebuild migrations, ActionPlanDiscard to ReadinessPointsNumericCheck) and `Tests/Assessment/SqliteNonTransactionalMigrationsTests`. | -263 and -275 yes (same file, sequence them). -292's exact fix is not read (the ticket says "shown safe or changed"); migrations are not frozen now per B273/B274 (no freeze note found after 10-05). |
| **L5 Infra and CI** | -193, -155 | `infra/main.bicep`, `infra/modules/appservice.bicep`, `api/src/HpsmPoc.Api/Auth/ForwardedClientAddress.cs` (-193); `.github/workflows/ci.yml` (-155 SQL Server container step with a by-name test check, as Azurite has). | -155 yes. -193's fix-shape text was cut off in my read: files beyond those named are unverified. Hardest lane: -155 must stay inside the CI time STOP line (B228 saw a 900 s line; the tip projected 899 to 988 s) and CI cost; -193 changes a live residual on hosted, so its deploy is Kam's word. |

Name-only files I could not establish: -13's A5 check, -292's final fix shape, -193's complete fix shape, the exact leftover items of -228 and -226.

### In flight (do not rebuild)

- Open PRs: none. Branches matching an open ticket id: none (branch names carry B numbers, not ticket ids; I matched by merged commit messages instead).
- Already merged but ticket still open: parts of -245, -228, -226, -148, -98 in PR #152 (`a6576ce`); -246 in PR #154 (`ce40ce07`); -271's early-warning test in PR #159 (`dff40192`); the -254 pin path (PR #155/#157) with the runtime half still open at -268. Records for B275 and later: none exist yet.

## Project 2: Datasec Security Composer (BACKLOG.md; repo `datasecau/Datasec-Security-Composer`)

### Tracker

The Composer has no Jira project (BACKLOG #4: key `PCOMP` proposed, on hold; kept parked by C-71 COMP-17). `4_Credentials/.env` holds only the demo login variables. GitHub issues are enabled but the repo shows 0 open issues. So the tracker is `BACKLOG.md` (314 lines, 308 numbered rows). Counts below come from my parse of that file, not a paged API.

### Current state

- **Last session:** B155 (Seat A), 2026-10-16: removed the demo site password gate (Caddyfile only; Kam's instruction; anyone with the link can now sign in as any demo persona). B154 the same day: "Paul cannot sign in" found to be an out-of-date guide (BACKLOG #236, held); Kam is to send Paul the sign-in instruction. [Briefs B154, B155 STATUS]
- **Code repo:** main `230f9fab` (PR #79, B152 approved words and looks, gate B153 GO WITH NOTES), preceded by `45591406` (PR #78, B149 Lane W web fixes) and `ef916ce2` (PR #77, B144, **live on the demo since C-74, 2026-10-13**). Open PRs: **0**. Open code-scanning alerts: 0; open Dependabot alerts: 0; 4 CodeQL "Analyze" check-runs success on `230f9fab` (CI proper is the local `scripts/ci.sh`, GREEN 20/20 at B152's head per its STATUS).
- **Merged but not deployed (as of B155, 10-16 about 13:00 AEDT, demo still `ef916ce2`):** everything in B149 and B152. Whether a later deploy happened I could not measure (no HTTP to the demo; no later brief in the folder).
- **Rulings that govern the board:** C-71 (2026-10-12): Kam accepted every default COMP-1 to COMP-19. The ones that matter: COMP-1 content release waits until after Paul's current review round; COMP-2 hold all Guided-only items; COMP-3 build "Start the next draft" (built, #99/#182); COMP-7 set a release signing key at the next deploy; COMP-8/9/10/17 leave or park; COMP-11 build "mark all local"; COMP-15 Sydney time on the PDF cover; COMP-16 hold demo data and Paul's guide note; COMP-18 one look card; COMP-19 approve the listed words. Cards `composer-words-comp19-b149-1013` and `composer-look-comp18-b149-1013` were both ruled a on 2026-10-14 (B152 STATUS, from `decisions.json`), and B152 built them.
- **Stale local project files:** `BACKLOG.md` top rows are right but many state columns predate B149/B152 (rows end at #318; B150 and B153 gate notes have no rows in the folder). `1_Project_Definition/CLARIFICATIONS.md` ends at C-74 (2026-10-13). `5_Project_History/history.md` newest entry 2026-10-13 (B147). Composer's records repo has no remote (B151 F-9). So any new records pass here is local-only until a remote is set.
- **Read:** CLAUDE.md, BACKLOG.md (parsed all 308 rows; read every row not terminal by its first word), history.md top, CLARIFICATIONS C-71 in full and headings to C-74, B149/B151/B152/B154/B155 STATUS tops.

### Classification

Population: the 112 rows whose state does not start with CLOSED / DEPLOYED / FIXED / DONE / SUPERSEDED / COVERED, and are not MERGED with a deploy recorded. The other 196 rows are terminal by their state text (not re-verified individually). Predicate for A to D as for project 1, plus:

- **T**: the state text begins with a stale word (RULED, READY FOR REVIEW, MERGED, BRIEFED) but the substance is finished or live; no work.
- Split of A: **A-records** (row update only, on a ruling already made) and **A-build** (code, scripts, docs).
- A built-and-merged row waiting only on a demo deploy goes to **B** (the demo is Kam's; "never deploy without Kam's word"; C-71 option a also says new words and looks go to Kam's cards before any deploy, which cards a-ruled 10-14 appear to satisfy, but that is Kam's to confirm).

Counts: T 26, A 31 (A-records 16 + A-build 15), B 29, C 4, D 22 = 112.

- **A-build (15):** #34, #57, #75, #84, #104, #123, #140, #152, #154, #158, #169, #178, #291, #293, #315.
- **A-records (16):** #66, #70 (Friday C5: keep, close), #109, #112 (stale state), #172, #173 (COMP-8 leave), #246 (C9 leave), #257, #259, #286, #287, #288 (COMP-18 accepted via the look card), #260, #285 (COMP-9 accept as built), #297 (records wording), #312 (COMP-6 keep masked, record it).
- **B (29):** built and merged, waiting on the demo deploy word (20): #42, #95, #99, #129, #131, #182, #271, #273, #277, #280, #281, #282, #284, #300, #304, #306, #307, #309, #317, #318. Other B (9): #26 (migrate guard design call), #27 and #247 (read the demo VM; Kam's), #43 (unruled contract change), #106 (release signing key at the next deploy, COMP-7), #171 (Docker network prune needs a card), #193 (half 2 unruled), #1 and #17 (Kam sends Paul's guide).
  - The mapping of #271, #273, #277, #280, #281, #284, #304, #309, #306, #307, #318 to B152's W/L rows is inferred from C-71's COMP-19/COMP-18 row lists and B152's table; not each verified against the code.
- **C (4):** #15, #253, #265 (Datasec SME ratification / Kam and Paul's check), #249 (content release APPROVED status after the SME check).
- **D (22):** Guided held (COMP-2): #30, #35, #55, #83 (End half), #223, #226, #228, #231, #240; parked (COMP-17): #4, #41, #54, #73, #101, #108; held (COMP-16): #227, #236; after Paul's review round (COMP-1 b): #252, #272; blocked on #249/#253: #215, #218; accepted limit: #316.
- **T (26):** #6, #7, #8, #9, #12, #21, #38, #61, #63, #64, #76, #78, #80, #86, #167, #189, #191, #209, #217, #225, #248, #255, #256, #276, #290, #296.

### Proposed lanes for class A (file-disjoint, easy to hard)

| Lane | Rows | Files touched | Established? |
|---|---|---|---|
| **CL0 Records pass** | the 16 A-records rows, plus refresh of the 20 B built-and-merged rows and the 26 T rows' first words | `BACKLOG.md`, `1_Project_Definition/CLARIFICATIONS.md`, `5_Project_History/history.md` (project folder only). Exception to "2-6 rows": this is one pass over one file set and cannot be split disjointly. | Yes. Records stay local until a remote exists (B151 F-9). |
| **CL2 Tooling** | #84, #140 | `scripts/up.sh`, `scripts/health-check.sh` (retry the host-side edge checks before RED); #140 the B47 evidence checker `Briefs/2026-10-03_B47_evidence/b47-check-off-guide.cjs` (strip `//` comments + self-test; not in the code repo). | Yes (tree of `230f9fab`). |
| **CL1 Deploy and rollback docs** | #34, #291, #293 | `DEPLOY.md` (repo root), `packages/db/rollback/*.down.sql`, the db test for the two-step Route B (#290's test). | DEPLOY.md and rollback paths yes; exact test file not read. Needs a seat stack (docker) to run Route B on 0020: a seat does that, I did not. |
| **CL3 Web CSS residue and Discovery** | #75, #123, #154, #57 | `apps/web/src/styles/*` and `screens-w*.css` (token residue: radii, off-token values), `apps/web/src/screens/Discovery.tsx` (`typedDraftFor`, #57 latent). | Directory yes, exact CSS files not read; #75/#123/#154 are partly deployed (radius half C-68). |
| **CL5a Two db migrations** | #152, #178 | `packages/db/migrations/0022_*.sql` (+ matching `rollback/0022*.down.sql`): index on `audit_event (tenant_id, entity_type, entity_id)`; additive CHECK on `policy_version.last_generate_input_hash`. Latest migration on main is `0021_policy_target.sql`. | Yes. One migration file for both avoids a numbering clash. |
| **CL4 Secret-field action and controls perf** | #104, #169 | `apps/web/src/screens/w2/SecretLocalValue.tsx`, `apps/web/src/screens/w3/*local-values*`, possibly `apps/api/src/secrets.ts` / `packages/engine/src/secrets.ts` (where the justification is required); #169 `apps/api/src/snapshot.ts` (measure first, "fix if it shows"). | #104's API half not read; the new "mark all local" label is NEW WORDS (Kam, before any demo deploy). |
| **CL5b Renderer** | #158, #315 | `packages/renderers/src/brand.ts`, `policy-document.ts`, `change-report.ts` (cover date in Sydney time; footer with a long target name); #158 adds a brand-profile time zone, so it also touches `packages/api-contract/**` (a contract bump) and may need a column: if so it takes migration 0023, after CL5a. | Files from the tree listing, not read in detail. Hardest lane (contract bump, PDF drift tests, golden files). |

### In flight

- Open PRs: none. Branches `b149/lane-w-web-fixes` and `b152/approved-words-and-looks` exist and are merged (#78, #79). Nothing in progress for any A row. Rows #300 and the other 19 B rows must not be rebuilt: they are already in `230f9fab`.

## What I could not measure

- The live state of both hosted sites (no HTTP allowed): whether Composer's demo now runs `230f9fab`, and any change since B273/B155.
- Composer: no paged API exists, so the 308-row parse is mine; terminal rows (196) were not individually verified; the B150/B153 gate notes are not in the folder; B152's W/L to BACKLOG row mapping for 11 rows is inferred.
- HPSM-POC: the final remaining items inside -228, -226, -245, -98, -148 after PR #152; -193's complete fix shape; whether Kam ruled anything on 10-19 morning (decision store and today's board not read). The analysis repo's branch list was read after one network timeout on the first try (the second call succeeded).
- Sixteen of the 113 HPSM-POC rows were classified from their summary and last comment only, not full descriptions: the seeded WS tickets -19, -20, -24, -29, -31, -35, -44, -46, -51, -52, -57, -58, -60, -61, -62 and -16.
