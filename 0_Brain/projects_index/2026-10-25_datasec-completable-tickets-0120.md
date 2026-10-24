BLUF: Six lanes can START TONIGHT with an empty program-computed intersection against every open PR and against each other (HPSM-POC 2, MPS 1, Composer 2, NexusAI 1; 105 lane pairs and 16 lane-vs-PR pairs checked on the firm and reserve lanes, 0 overlaps; planted controls return 1, 1, 5, 1, 1). Reserve lanes (also empty): MPS web/stub, MPS feedback triage, HPSM CI, Composer web, Composer engine/renderer, NexusAI erasure tests, NexusAI workflows.
Feedback: NO human in Jira or GitHub since 21:00 AEDT (every Jira ticket and comment is the seat account 616503; zero GitHub issue comments). One bot item: a CodeQL review comment on merged HPSM-POC PR #211 (alert #13, js/file-system-race, web/src/e2e-runner.liveApiRun.test.ts, on the PR ref); no ticket names it. Mail NOT measured.
What changed since 21:00: the three MPS PRs (#107, #108, #109), HPSM-POC #210 and #211, Composer #87, NexusAI #106 and records #109 are merged; the MPS wave-3 six are mostly NOT startable (words, a decision, or already closed by PR #102): see section 2.2.
One real overlap the program found and I held back: NexusAI RD-850/-851/-852/-854 add test cells, so they change `scripts/verify-expected-counts.json`, which open PR #67 (stale since 7 Oct) also edits. They start only when #67 is closed or merged.
Not startable and why: PCOMP-42/-44 (new governance values and enum, contract bump, migration numbering behind PCOMP-17/-14), MPSCALC-169/-290/-288 (new field or sentence, or an open design choice), RD-876 (owner decision), RD-847 (decision plus live shared tool), RD-815 (workflow that deploys the demo on push to main).

# Datasec: tickets an agent could complete now, delta refresh (read-only research, 2026-10-25, about 01:20 AEDT)

Researcher: read-only sub-agent (claude-sonnet-5-5) for Tuesday. Clock from `date`: Sun 25 Oct 2026 01:15:37 AEDT at start (= Sat 24 Oct 14:15:37 UTC), 01:24:29 AEDT at the intersection run. Wrote this one file (plus scratchpad scripts). Base and method: [[2026-10-24_datasec-completable-tickets-2100]]. Scope: HPSM-POC (HPSMPOC), MPS Commercial Calculator (MPSCALC), Security Composer (PCOMP), NexusAI (RD). Jira = GET only (`/rest/api/3/search/jql` with nextPageToken until isLast, issue and comment GETs), every JQL begins `project = <KEY> AND` (the helper wraps the rest in parentheses since the one slip noted in UNMEASURED). Credentials read in-process from each project's own `4_Credentials/.env` (variable names only: JIRA_BASE_URL or JIRA_SITE, JIRA_EMAIL, JIRA_API_TOKEN). GitHub = `gh api -X GET` under each project's own `GH_CONFIG_DIR`. Main read through `gh api` trees, contents and blobs. The only local git call was `ls-remote` / `cat-file` / `grep` against the NexusAI clone, which proved stale (it lacks bda30039), so nothing was taken from it. AEDT = UTC+11, so the window opens at 21:00 AEDT = 10:00Z on 24 Oct.

## 0. How I measured (every count names its query)

| Count | Query / command | Result |
|---|---|---|
| HPSMPOC open | `project = HPSMPOC AND statusCategory != Done`, nextPageToken until isLast | 119 rows, 2 pages (2100 file: 123) |
| MPSCALC open | `project = MPSCALC AND statusCategory != Done` | 320 rows, 4 pages (2100: 316; +4 = MPSCALC-331..-334) |
| PCOMP open | `project = PCOMP AND statusCategory != Done` | 93 rows, 1 page (2100: 93) |
| RD open | `project = RD AND statusCategory != Done` | 760 rows, 8 pages (2100: 760) |
| Created since 21:00 AEDT | `project = <K> AND created >= "2026-10-24 21:00"` | HPSMPOC 3 (-347, -348, -349), MPSCALC 4 (-331..-334), PCOMP 0, RD 0; creator of all 7 is `616503` |
| Done since 21:00 | `project = <K> AND statusCategory = Done AND statusCategoryChangedDate >= "2026-10-24 21:00"` | HPSMPOC 7 (-345, -342, -340, -338, -337, -328, -320), MPSCALC 0, PCOMP 0, RD 0 |
| Updated since 21:00 | `project = <K> AND updated >= "2026-10-24 21:00"` | HPSMPOC 12, MPSCALC 18, PCOMP 0, RD 9 |
| Control, non-zero | `project = <K> AND created >= "2026-10-21 00:00"` | HPSMPOC 45, MPSCALC 19, PCOMP 94, RD 6 (the created filter fires on every board) |
| Main shas | `repos/<repo>/commits/main` | HPSM-POC `c9927142` (13:15Z), MPS `93e1cab5` (13:11Z), Composer `e019ac3a` (10:11Z), NexusAI `bda30039` (13:05Z) |
| Open PRs | `repos/<repo>/pulls?state=open&per_page=100` | HPSM-POC 0; MPS 0; Composer #86 (vite, 2 files), #85 (draft HOLD, 57 files); NexusAI #108 (nodemailer / smtp-server, 2 files), #67 (stale, 3 files). Control: the same call returned 4 open PRs on two repos, and `state=closed` returned the merged ones below |
| Merged since 15:00 | `pulls?state=closed&sort=updated`, `updated_at >= 2026-10-24T04:00` | HPSM-POC #207, #208, #209, #210 (d1a64019), #211 (c9927142); MPS #107 (5fe35a05), #108 (9cb6d9ba), #109 (93e1cab5); Composer #87 (e019ac3a); NexusAI #107, #106 (bd28ced2), #109 (bda30039) |
| Trees | `git/trees/main?recursive=1` | HPSM-POC 1323 blobs, MPS 644, Composer 951, NexusAI 955; none truncated. Every path in a lane below exists on main unless marked NEW |
| Open PR file lists | `pulls/<n>/files`, paged | #86 2, #85 57, #108 2, #67 3 |
| Ticket text and comments | issue GET plus comment GET on 59 candidate keys | each ticket below was read in full, description and every comment |

## 1. Verification of the records seat's claims (each read at source)

| Claim | Source read | Verdict |
|---|---|---|
| MPS #107, #108, #109 merged with those shas | `pulls?state=closed` merge_commit_sha | TRUE (5fe35a05, 9cb6d9ba, 93e1cab5); all merged 24 Oct 09:58Z to 13:11Z |
| HPSM-POC #210 d1a64019, #211 c9927142 merged | same | TRUE (13:10Z, 13:15Z) |
| HPSMPOC-338, -340, -320, -345, -328, -337, -342 Done | JQL Done since 21:00 | TRUE (all seven) |
| HPSMPOC-344 open with its N-extra-spaces half | issue + comment | TRUE: PR #210 met the "two extra" alternative; the property half (three extra spaces, gate variants X12 / Xm12) is open |
| New HPSMPOC-347, -348, -349 | issue GET | TRUE, all Backlog, created by 616503 |
| Composer #87 merged e019ac3a, not deployed | `commits/main`, PR record | TRUE (10:11Z); "not deployed" is the ticket text, not probed |
| NexusAI #106 bd28ced2, records #109 bda30039 merged; #108 and #67 open | pulls | TRUE |
| MPSCALC-331..-334 new | issue GET | TRUE, labelled `mpscalc-b610` |
| MPS wave-3 six "may now be startable" | each ticket and its comments | MOSTLY NO: see 2.2 |
| Composer "gate findings B593-2, -3, -9, -10 as follow-up tickets" | `project = PCOMP AND (summary ~ "B593" OR text ~ "B593")`, 0 rows | They are NOT tickets (0 hits; control: the PCOMP board returned 94 rows for `created >= 2026-10-21`). They live in the gate file `1_Project_Definition/Briefs/2026-10-24_B593_STATUS.md` (lines 320-356). I read them there |

## 2. Per project: tickets an agent could finish now

Rules applied: no new user-facing word, no ruling from the product owner, no production touch, no path shared with an open PR or another lane. Sonnet by default; Opus where a security design or a data-destroying procedure is built. Gate tier: 1 security/data/deploy/migration, 2 tests/docs/config.

### 2.1 HPSM-POC (main `c9927142`, 0 open PRs)

| Key | Scope | Paths (all exist on main) | Why ruling-free | Model | Gate |
|---|---|---|---|---|---|
| HPSMPOC-344 (property half) | Add the three-extra-edge-space case in each table so gate variants X12 and Xm12 turn red (ticket's own Done-when says "or a property row over 1 to N") | `api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs` (HeldNameEdgeSpacedWithTwoMoreSpaces at :489), `web/src/server/mock/customer-name.test.ts` (:321-323) | test-only; comment B611 gives the exact survivors | Sonnet | 2 |
| HPSMPOC-347 | Port the Api project's "other fault with its own inner exception" rows to the Feedback project so Q11c, Qany, Qinner-nonumber, Qinner-notext turn red; the two helper copies stay untouched | `api/tests/HpsmPoc.Modules.Feedback.Tests/HostStartRetryTests.cs` | test-only (gate B607 Note) | Sonnet | 2 |
| HPSMPOC-349 | Optional trailing comma in the markerStep pattern (`e2e-runner.test.ts:812`), then read the eight raw-text rows (lines 95, 143, 367, 484, 498, 504, 514, 941) and make each comment-proof or record why not | `web/src/e2e-runner.test.ts` | test-only; the "loosening" that PR #211's brief forbade is now the Done-when | Sonnet | 2 |
| HPSMPOC-348 (conditional) | A row that reads the two audit steps' whole blocks so N1-N4 and N6 turn red | `web/src/audit-dev.test.ts`; `.github/workflows/ci.yml` read-only | test-only, but the gate marks it "candidate decision": start only if Tuesday confirms the assertion style | Sonnet | 2 |
| HPSMPOC-314 (reserve) | Rebalance the two filters of the `api-other-and-feedback` shard | `.github/workflows/ci.yml` | CI-only. The "limit 20" in the ticket is stale (30 since HPSMPOC-308) | Sonnet | 2 |
| HPSMPOC-343 (reserve) | Read-only trace of the `trim()` sites against `Requests.cs:221/224`; output is a ticket comment | read-only | the comment is a Jira write, so a records seat posts it | Sonnet | 2 |
| HPSMPOC-322 (reserve, conditional) | B477-5/-6 on a branch with no PR | `Providers.cs`, `NarrativeOutputValidator.cs` | stop if it needs a new approved sentence | Sonnet | 1 |

Excluded: HPSMPOC-339 (held on an open decision card, as instructed), -341 (decision), -346 (landed, record move only).

### 2.2 MPS Commercial Calculator (main `93e1cab5`, 0 open PRs)

The wave-3 six, each read with every comment:

| Key | Verdict | Reason |
|---|---|---|
| MPSCALC-290 | NOT startable | docs/API.md half already on main since 4c593517; the open part is the openapi.json:218 SENTENCE, "narrow the sentence" = a new word; the ticket says new words go to the words gate |
| MPSCALC-322 | NOT a build | comment B583: closed by PR #102 (gate B575: "B552-1 is CLOSED at 3723b9a"); a record move |
| MPSCALC-325 | STARTABLE (lane M-A) | four validation walks stop at no cap; main already has the pattern `MaxNullEntriesListed = 20` / `errors.Count < MaxNullEntriesListed` in `PurchaseValidation.cs`; no word |
| MPSCALC-169 | NOT startable | adds a field beside `lineMarkupsOverlayVersion` with openapi and API.md text = new contract words |
| MPSCALC-176 | STARTABLE, reserve lane | ruling present: comment B583 records two rulings on 24 Oct (11:53 and 12:00) approving the word pack; approved words are in `1_Project_Definition/Registers/2026-10-24_mps-176-feedback-triage-approved-words.md` (46 rows; file exists, 10,541 bytes). Large feature build |
| MPSCALC-288 | NOT startable | the ticket asks to "decide whether the canApprove queue should still list such a quote": an open design choice for the owner, and openapi text |

Startable:

| Key | Scope | Paths | Model | Gate |
|---|---|---|---|---|
| MPSCALC-331 | 15 shapes of a staged document answer 500; skip a null product in the term-gap check and treat a null cell link as does-not-agree so the EXISTING issue REFERENCE_DATA_REJECTED / DATA-IMP-002 answers; 15 rows, each red at the unmodified validator | `src/MpsCalc.Import/Validation/ReferenceDocumentValidator.cs` (:160, :162, :166, :203); NEW `tests/MpsCalc.Api.Tests/SourceLifecycleTests.B610GovernedNull.cs`; `src/MpsCalc.Api/Sources/SourceDocumentChecks.cs` read-only | Sonnet | 1 |
| MPSCALC-325 | cap the four walks, one row per walk | `src/MpsCalc.Api/Quotes/PurchaseValidation.cs` (:116-123), `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` (:1423, :1424, :1426, :1442-1443); NEW `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs`. Stop if a sentence must say "first 20" | Sonnet | 1 |
| MPSCALC-333 | four pins: edit-path fleet-below-limit row, not-owner sentence on calculate and submit, exact 409 and 404 detail; the B591-10 order gaps are for the coordinator to choose and are NOT taken | `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs`, `tests/MpsCalc.Api.Tests/QuoteRefusalOrderGuard.cs` (test-only; ticket label says tier-1) | Sonnet | 1 |
| MPSCALC-334 | NEW `web/src/api/stub/stubApi.test.ts`; list `mpscalc.stub.createdQuotes` in `check-bundle.mjs:31-35`; `exact: true` at `bom.spec.ts:180` | `web/src/api/stub/stubApi.test.ts` (NEW), `web/scripts/check-bundle.mjs`, `web/e2e/bom.spec.ts`; `stubApi.ts` only if the rental-update stub is taken | Sonnet | 2 |
| MPSCALC-329 (reword only) | gate B606-2: reword the header lines 13-15 (toward-zero and toward-negative-infinity flip identical rows); comment only | `tests/MpsCalc.Engine.Tests/ReconciliationContractRemainder.cs` | Sonnet | 2 |

Not taken: MPSCALC-332 (the ticket's fix is "either rule the vanished-file wording acceptable" or say the line once: a choice between a ruling and a behaviour; the row half alone is not the ticket), -330 (survivor needs a product minimum, "a product question nobody has asked"), -328, -218, -221, -313 (clause met by #109, comments B610; record moves), -321 (rows landed; the width of the rule is the owner's), -302 (Opus, reserve from the 2100 file, not re-read), -205 and -201 (not re-read tonight).

### 2.3 Security Composer (main `e019ac3a`, open PRs #86 and #85 only)

Not tickets, from the gate file B593 (lines 320-356): B593-2 (year 0000 on any `format: date` answers 500, nothing stored), B593-3 (three version-pin rows can no longer fail; two stale comments), B593-9 and B593-10 (two survivors, one db row each). B593-1 / -4 / -5 are words or ruling matters and are NOT taken; the open words card `composer-87-new-words-1024` is not touched.

| Item | Scope | Paths | Model | Gate |
|---|---|---|---|---|
| B593-2 | refuse year 0000 as 400 INVALID_REQUEST (the same answer 2027-02-30 already gets) for every `format: date` body field, before any write; red-first row on `pilot_date` and `due_date`. Fastify's ajv is built at `apps/api/src/app.ts:125` with `customOptions` | `apps/api/src/app.ts`; NEW `apps/api/test/b593-year-zero-date.db.test.ts` | Sonnet | 1 |
| B593-3 | retitle the three "pins the version" rows to what they check (or a live `not.toBe`), fix the stale comments at `openapi.test.ts:3324` and `:3430` | `packages/api-contract/src/openapi.test.ts` (rows at :3325, :3431, :3577). No sentence, no `document.ts` change | Sonnet | 2 |
| B593-9, B593-10 | one db row each: supersede a released version while changing a number expects 23514 RELEASED_VERSION_IMMUTABLE; insert `remediation = 'staged'` into `pc.attribute_override` expects 23514 | NEW files under `packages/db/test/` | Sonnet | 1 |
| PCOMP-17 | additive CHECK `~ '^[0-9a-f]{64}$'` on `policy_version.last_generate_input_hash`, migration `0026` plus a reverser | `packages/db/migrations/0026_*.sql` (NEW), `packages/db/rollback/0026_*.down.sql` (NEW), `packages/db/test/**`, `DEPLOY.md` (a 0026 section; the 0023 / 0024 / 0025 sections show the pattern, each pinned by a `b587-00NN-down.db.test.ts`) | Sonnet | 1 |
| PCOMP-14 | index on `audit_event (tenant_id, entity_type, entity_id)`, migration `0027` plus a reverser | same, `0027` | Sonnet | 1 |
| PCOMP-22 | before step 2 of the Route B two-step, check the dump is complete (`PostgreSQL database dump complete` once in a full script, 0 in a cut one); a boundary-cut test | `DEPLOY.md` (:190-206); the test the ticket calls "#290's db test" is not located on main (UNMEASURED) | Opus (a restore procedure, data-destroying if wrong) | 1 |

Held, with reason: PCOMP-42 (adds the governance values "after validation" and "controlled/staged" = new user-facing words and a contract bump; the ticket also cites the stale migration `0022`) and PCOMP-44 (enum values in `document.ts`, contract bump, "the coordinator may start it"): both share `document.ts`, `openapi.test.ts` and the migration chain with C-API / C-DB, so they go after those land. Reserve, from the 2100 file and re-read: PCOMP-62 (`apps/web/src/screens/b116-s10-verify-dom.test.tsx`), PCOMP-12 (`apps/web/src/screens/Discovery.tsx`), PCOMP-63 (comment, `packages/engine/test/s47-crf2-linear-detector.test.ts`), PCOMP-23 (change-report half only: `packages/renderers/src/change-report.ts` and its test; the policy-PDF half stays out because draft #85 changes `packages/renderers`).

### 2.4 NexusAI (main `bda30039`; open #108 and #67)

| Key | Verdict | Paths | Model | Gate |
|---|---|---|---|---|
| RD-862 | STARTABLE: delete `generateSQLFromCondition` (`backend/server.js:6393`, the only occurrence in the 22,461-line file; the sibling `generateSQLQueryForCondition` has 8 hits, so the search fires). RD-774 has landed (115a775); no caller in `server.js` and code search over the repo finds none outside it (see UNMEASURED for the search's blind spot). No count change expected | `backend/server.js` | Sonnet | 2 |
| RD-873 | STARTABLE: give alert #95 the same `.startsWith(dir)` filter as #96/#98/#99; #97 is the test double of `_replaceFile`; #116 at `rd407-concurrent-settings-writers.test.js:620`. Never dismiss; closure is read by alert number on main's analysis after landing. NO new test suite | `__tests__/erasure-reaches-every-read-location.test.js`, `__tests__/erasure-verdict-is-derived-from-failures.test.js`, `__tests__/helpers/rd407-setting-writer.js`, `__tests__/initialize-files-uses-shared-recovery-list.test.js`, `__tests__/rd407-concurrent-settings-writers.test.js` | Sonnet | 2 |
| RD-844 | STARTABLE: the rd490 guard waits for `load`, which waits for the cdnjs stylesheet; wait for `domcontentloaded` plus the banner, or abort off-host requests. The cell count must not change | `tests/e2e/open-access-banner-guard.js` (:294), `__tests__/rd490-open-access-banner-browser.test.js` | Sonnet | 2 |
| RD-850, -851, -852, -854 | HELD: each adds cells, so `scripts/verify-expected-counts.json` (`tests` and `suites` totals) changes, and open PR #67 also edits that file (the program found the overlap, section 3). Start after #67 is closed or merged. Paths when freed: `__tests__/helpers/dockerfile-stages.js`, `__tests__/rd848-no-redundant-copy.test.js`, the counts file | Sonnet | 2 |
| RD-814 | RESERVE (conditional): `permissions: contents: read` in `build.yml`, `deploy.yml` (workflow_dispatch only), `npm-audit.yml`; read each job first (an OIDC login needs `id-token`); own review | `.github/workflows/build.yml`, `deploy.yml`, `npm-audit.yml` | Sonnet | 1 |
| RD-815 | NOT tonight | `deploy-demo.yml` runs on every push to main, so landing it can deploy the demo | | |
| RD-876 | NOT startable | the ticket says "the owner decides" the ceiling | | |
| RD-847 | NOT startable | "decide the canonical lock base ... switch every seat at one moment"; the tool is in use | | |
| RD-827 | NOT tonight | "Tuesday's call"; touches shared worktree installs | | |

NexusAI lands by merge commit of the gated head, never squash.

## 3. Lanes that can START TONIGHT (6), and the intersection

One seat, one worktree, one branch per lane (a lane with several tickets does them in order, one PR each where the gate tier differs). Load rule stays: one waiter, load1 < 7. Ranked in the product owner's order: HPSM-POC, MPS, Composer, NexusAI.

| # | Lane | Tickets | Model / gate | YOURS (may edit) | NOT YOURS |
|---|---|---|---|---|---|
| 1 | HPSM-POC H-API | HPSMPOC-344 (property half), -347 | Sonnet / 2 | `api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs`; `web/src/server/mock/customer-name.test.ts`; `api/tests/HpsmPoc.Modules.Feedback.Tests/HostStartRetryTests.cs` | `web/src/e2e-runner.test.ts`, `web/src/audit-dev.test.ts`, `web/src/e2e-runner.liveApiRun.test.ts`, `.github/**`, every `api/src/**`, both `Support/HostStartRetry.cs` copies (they change together; -347 leaves them untouched) |
| 2 | HPSM-POC H-WEB | HPSMPOC-349, -348 (conditional) | Sonnet / 2 | `web/src/e2e-runner.test.ts`; `web/src/audit-dev.test.ts` | `web/scripts/e2e.mjs` and `.github/workflows/ci.yml` (read-only), `web/src/server/mock/customer-name.test.ts`, all `api/**` |
| 3 | MPS M-A | MPSCALC-331, -325, -333 | Sonnet / 1 | `src/MpsCalc.Import/Validation/ReferenceDocumentValidator.cs`; `src/MpsCalc.Api/Quotes/PurchaseValidation.cs`; `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`; `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs`; `tests/MpsCalc.Api.Tests/QuoteRefusalOrderGuard.cs`; NEW `tests/MpsCalc.Api.Tests/SourceLifecycleTests.B610GovernedNull.cs`, `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs` | `docs/API.md`, `docs/api/openapi.json`, `web/src/api/generated/**`, `src/MpsCalc.Api/Feedback/**`, `web/src/feedback/**`, `web/**` (other than as read), `tests/MpsCalc.Engine.Tests/**`, `SourceDocumentChecks.cs` (read-only) |
| 4 | Composer C-API | B593-2, B593-3 | Sonnet / 1 (B593-3 alone is 2) | `apps/api/src/app.ts`; NEW `apps/api/test/b593-year-zero-date.db.test.ts`; `packages/api-contract/src/openapi.test.ts` | `packages/api-contract/src/document.ts` and `openapi.json` (no sentence, no word), `packages/db/**`, `DEPLOY.md`, `apps/web/**`, `packages/renderers/**`, `packages/engine/**`, the four #85 files under `apps/api` (`content.test.ts`, `secrets.test.ts`, `api-running-content-release.db.test.ts`, `s43-c11-demo-capabilities.db.test.ts`) |
| 5 | Composer C-DB | B593-9, B593-10, PCOMP-17, PCOMP-14, then PCOMP-22 (Opus, last, may be split to its own seat) | Sonnet / 1 (PCOMP-22 Opus) | `packages/db/migrations/0026_*`, `packages/db/migrations/0027_*`, `packages/db/rollback/0026_*`, `0027_*`, `packages/db/test/**`, `DEPLOY.md` | `apps/**`, `packages/api-contract/**`, `packages/engine/**`, `packages/renderers/**`, `packages/content/**`, `content/**`, `apps/web/package.json`, `package-lock.json` |
| 6 | NexusAI N-HYG (three disjoint sub-lanes N-a, N-b, N-c: launch as one seat or three) | N-a RD-862; N-b RD-873; N-c RD-844 | Sonnet / 2 | N-a `backend/server.js`; N-b the five erasure test files listed in 2.4; N-c `tests/e2e/open-access-banner-guard.js`, `__tests__/rd490-open-access-banner-browser.test.js` | `package.json`, `package-lock.json` (PR #108, a QA gate is running on it), `scripts/verify-expected-counts.json` (PR #67; no cell may be added), `.github/**`, `session-tools/**`, `__tests__/helpers/dockerfile-stages.js`, `__tests__/rd848-no-redundant-copy.test.js` |

Reserve lanes (start only with capacity; all checked in the same program): M-WEB (MPSCALC-334, -329 reword: `web/src/api/stub/stubApi.ts`, `stubApi.test.ts`, `web/scripts/check-bundle.mjs`, `web/e2e/bom.spec.ts`, `tests/MpsCalc.Engine.Tests/ReconciliationContractRemainder.cs`); M-FEEDBACK (MPSCALC-176, Sonnet / 2: `src/MpsCalc.Api/Feedback/**`, `web/src/feedback/**`, `tests/MpsCalc.Api.Tests/Feedback*`, `docs/API.md`, `docs/api/openapi.json`, `web/src/api/generated/**`); H-CI (HPSMPOC-314: `.github/workflows/ci.yml`); C-WEB (PCOMP-62, -12); C-ENG (PCOMP-63, -23 change-report only); N-CI (RD-814).

### Intersection by program (script `inter.py` in the scratchpad; exact path or `**` prefix match, both directions)

Inputs: the lane path lists above (firm plus reserve, 15 lane sets) against the open PR file lists read from GitHub (#86, #85, #108, #67) and against each other.

| Check | Result |
|---|---|
| Lane x open PR, firm and reserve lanes, Composer and NexusAI (HPSM-POC and MPS have no open PRs, so 0 pairs by construction; control: both repos' closed lists were non-empty) | 16 pairs run on the final firm and reserve lanes, 0 overlaps (18 pairs with the held set) |
| Lane x lane, all lanes (firm, reserve, held) across the four projects | 105 pairs, 0 overlaps |
| HELD set RD-850/-851/-852/-854 (not a lane) x PR #67 | 1 overlap: `scripts/verify-expected-counts.json`. This is a REAL hit, the reason those four are held |

Controls that could have been non-zero, same script, same run: planted same-path (`web/src/api/stub/stubApi.ts` vs itself) returned 1; planted glob (`packages/db/test/**` vs `packages/db/test/b587-0025.db.test.ts`) returned 1; planted lane-vs-lane (M-WEB against M-WEB plus M-A) returned 5; planted `DEPLOY.md` against C-DB returned 1; planted `apps/api/src/app.ts` appended to PR #85's real api files against C-API returned 1; and PR #85's real api-path list is non-empty (four files), so the comparison had something to match. Limits: NEW file names (`QuoteWalkCaps.cs`, `SourceLifecycleTests.B610GovernedNull.cs`, `b593-year-zero-date.db.test.ts`, the 0026 / 0027 migrations) are my proposals; a builder who picks other names must stay inside the same directory; C-DB's `packages/db/test/**` glob is wide on purpose because a new migration may need an existing pin test edited. PR #85 was compared by file name (57 files); the four of them under `apps/api` and the `packages/engine`, `packages/renderers`, `packages/content`, `content/` areas are outside every Composer lane.

## 4. Record-seat candidates added since 21:00 (not lanes)

- MPS: MPSCALC-322 closed by PR #102 per comment B583 (a record move); -328, -218, -221, -313, -321 met by #109 per comments B610 (stay Backlog until the coordinator moves them).
- HPSM-POC: HPSMPOC-344's other half is met by #210; the two lines are in comment B611.
- NexusAI: RD-871 and the #106 tickets after #106 (landed bd28ced2); RD-881 (landed by #107).
- Composer: PCOMP-40, -41, -43 after #87 (landed e019ac3a); B593-2 / -3 / -9 / -10 want tickets before a brief names them (records seat).
- HPSM-POC: CodeQL alert #13 (section 5) wants a ticket if Tuesday wants it fixed in code; the alert is never to be dismissed by a builder.

## 5. FEEDBACK CHECK (per-boot duty; window opened at the 2100 file's watermark, 21:00 AEDT = 10:00Z)

BLUF: new human feedback since 21:00 AEDT: NO. Client-human response in Jira or GitHub: NO. New ticket by a non-seat account: NO. One bot comment (CodeQL on a merged PR) is reported below. Mail: NOT MEASURED.

| Signal | Query | Result | Control that could have been non-zero |
|---|---|---|---|
| New tickets | `project = <K> AND created >= "2026-10-24 21:00"` | HPSMPOC 3, MPSCALC 4, PCOMP 0, RD 0; creator of all 7 is `616503` | `created >= "2026-10-21 00:00"` returned 45 / 19 / 94 / 6, so the filter fires on each board |
| Comment authors | comment GET on every ticket `updated >= "2026-10-24 21:00"` (12 / 18 / 0 / 9 tickets), comments with a UTC timestamp `>= 2026-10-24T10:00` | HPSMPOC 9 comments, MPSCALC 14, RD 9, PCOMP 0; every author `616503`; non-seat authors 0 | the tally is non-zero on three boards, so a different author would have shown |
| GitHub issue comments | `issues/comments?since=2026-10-24T10:00:00Z` on four repos | 0 on all four | positive control `since=2026-10-20`: HPSM-POC 2 (dependabot[bot] 1, seat account 1); the other three 0 with no positive control, as in earlier sweeps |
| GitHub review comments | `pulls/comments?since=...` | HPSM-POC 1, by `github-advanced-security[bot]` on PR #211, path `web/src/e2e-runner.liveApiRun.test.ts`, "CodeQL / Potential file system race condition"; others 0 | the call returned the bot comment, so it fires |
| GitHub reviews | `pulls/<n>/reviews` on every PR updated since the window (last 15 by `updated`) | HPSM-POC #211 COMMENTED by that bot; others 0 | same call returned one |
| GitHub items touched | `issues?state=all&since=...` | HPSM-POC 2, MPS 2, Composer 1 (all the seat account), NexusAI 3 (seat account 2, dependabot[bot] 1) | |
| Code-scanning alert behind the bot comment | `code-scanning/alerts/13` | js/file-system-race, severity high, ref `refs/pull/211/head`, lines 156, created 11:44Z, not dismissed, not fixed; `code-scanning/alerts?state=open` on the default branch returned 0 | I do not know whether main's analysis has run on c9927142 yet (UNMEASURED) |
| Ticket for the alert | `project = HPSMPOC AND (text ~ "file-system-race")`, `(text ~ "liveApiRun")` | only HPSMPOC-328 and -345 (both Done) | `text ~ "code-scanning"` returned dozens of rows, so text search fires |

Not human signals: every Jira and GitHub row is the shared seat account (`616503`, the seat's GitHub account) or a bot; that account cannot separate the product owner from a seat, same caveat as the earlier files.

## FOUND

1. The 2100 plan's MPS wave-3 six turned out smaller than the records seat's note says: of -290, -322, -325, -169, -176, -288 only -325 and -176 are startable (-290 and -169 are words, -288 is a design choice, -322 is already closed by PR #102). The new -331 and -333 carry the real MPS tier-1 work tonight.
2. The Composer gate findings the brief called "tickets" (B593-2, -3, -9, -10) have no ticket. B593-2 is a genuine runtime defect (year 0000 answers 500 on `createEngagement` `due_date` too, at the base), worth briefing as the first Composer item.
3. NexusAI's test-cell tickets are blocked by one stale open PR, #67 (3 files, open since 7 Oct, no comments, mergeable state unknown): closing or merging it frees RD-850/-851/-852/-854. A decision for Tuesday, not for me.
4. RD-815 looks safe but is not: `deploy-demo.yml` triggers on push to main.
5. A CodeQL alert (#13) sits on the merged HPSM-POC PR #211 and no ticket names it.
6. HPSMPOC-314 still carries the stale "limit 20" premise (limit is 30 since HPSMPOC-308).

## UNMEASURED (said plainly)

- Mail (the coordinator inbox and the shared inbox): not read; my fences forbid mail tools. The feedback BLUF is Jira and GitHub only.
- One query slip: my first Composer search `project = PCOMP AND text ~ "year 0000" OR ...` had an unparenthesised `OR`, so Jira returned rows from boards outside the four keys. I stopped reading that output, recorded nothing from it and did not use it; every later query goes through a helper that parenthesises the clause. Nothing else outside the four keys was read.
- Main's CodeQL analysis state for HPSM-POC c9927142 (whether alert #13 exists on main), and whether RD alert #116 and the five RD-873 alerts are still open now.
- Whether PR #67 on NexusAI merges cleanly (`mergeable_state` returned unknown) and whether it is meant to be revived.
- RD-862's "no caller" proof: `backend/server.js` was read whole from the blob (22,461 lines, one occurrence, the definition); the repository code search returns 0 for the name, but that index does not hold `server.js` at all (its control name only hit other files), so I cannot claim the rest of the repo was grepped. The builder must run `git grep` on the branch.
- Code bodies: I read ticket text, gate-file findings and a few code anchors (`PurchaseValidation.cs` caps, `app.ts:125`, `DEPLOY.md` headings), not the code of each lane. Sizes are estimates.
- PCOMP-22: the db test it names ("#290") is not located on main; the script it guards is the `pg_restore` pipeline in `DEPLOY.md` and I did not find a script file.
- Whether the Feedback helper copies for HPSMPOC-347 need to change (the ticket says leave both untouched).
- MPSCALC-302, -205, -201, PCOMP-12 / -62 / -63 / -23 and HPSMPOC-322 / -343 were re-listed from the 2100 file or read briefly, not re-verified against main code tonight.
- Whether "candidate decision" on HPSMPOC-348 needs the product owner or only Tuesday.
- The 2100 file's wave-3 lists no longer matter: every wave-3 PR it assumed is merged, so lane-versus-wave checks were dropped; new test file names a builder creates cannot be checked in advance.
- Not touched on purpose: myPKI, CypherKey, Lead_Bot, VSP and QuickQuote, any hosted or production host, `az`, docker, the decision queue, `fleet_ack`, the scoreboard, `briefs_staged/`, any non-Datasec client, any git write, any Jira or GitHub write.
