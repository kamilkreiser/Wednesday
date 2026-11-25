# SWEEP-0446: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-26 early morning)

Commissioned by Tuesday (s328) from `2026-11-26_SWEEP-0446_COMMISSION.md`; drafter rules `DRAFTER_RULES.md` read whole first; form copied from `2026-11-11_SWEEP-1326_datasec-actionable-lanes.md` (read whole), baseline `2026-11-25_SWEEP-0600` (read: BLUF, ranked lanes, MPS and Composer sections). Written Thu 26 Nov 2026 04:57:11 AEDT (printed by `date`; per-section clocks are the sub-sweepers' own `date` prints). **HPSM-POC was not read, counted or listed (Kam's hold to the end of 2026-12-10); myPKI, CypherKey and Lead_Bot skipped.** OXPd was swept by the sweeper itself; NexusAI, MPS Calculator and Security Composer by one Sonnet sub-sweeper each under the same fences, their section kept below with their own UNMEASURED lists. Their scratch is under `fleet/state/s328/sweep0446/` (`sec_RD.md`, `sec_MPSCALC.md`, `sec_PCOMP.md`, `sec_OXPD2.md`, the Jira dumps `RD.tsv`, `OXPD2.tsv`, `MPSCALC.tsv`, `PCOMP.tsv`, the read-only helper `jq.py`).

## BLUF

| project | open (instrument: Jira `search/jql`, GET, every page, each JQL `project = <KEY> AND ( statusCategory != Done )`) | actionable now | lanes |
|---|---|---|---|
| NexusAI (RD) | **911**: To Do 369, Testing 326, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 (sum 911) | **79 To Do keys** (about 30 re-read today; the rest carried from the 11-24 tables, flagged "carried"); RD-1044 and RD-1045 both actionable | 4: 1 server, 2 backend periphery, 3 static front end, 4 tests/scripts/CI/Dockerfile |
| OXPd 2 (OXPD2 + BACKLOG.md owed list) | **59** Jira (Backlog 57, In Progress 2: nearly all questions, Kam actions or umbrellas); **100 open owed lines of 147** | **42 owed lines** in 4 code lanes (A 8, B 11, C 12, D 11) plus **32 records lines** in one records lane; rows 3 and 4 device runs are NOT in it (Kam's word first) | 4 code + 1 records |
| MPS Calculator (MPSCALC) | **166**, all Backlog (15 Epic, 151 Task) | **6** (233, 316, 120, 195, 135, 297). **Differs from the 11-24 and 11-25 sweeps (0)**: see its section | 2 |
| Security Composer (PCOMP) | **75**, all Backlog | **1** (PCOMP-23, policy PDF footer; a judgement call, 0 if its residue is read as an owner ruling) | 1 |

Main shas at sweep time (`gh api -X GET`, each under the project's own `GH_CONFIG_DIR`): NexusAI `e789995a` (RD-1037 landed; PR 259 then records PR 260), OXPd `8757daa6` (row 4 landed), MPS `56f508a7`, Composer `d06508f8`. Open pull requests: 0 in all four repositories. No seat is live (NEXT-PICKUP DELTA 1470).

Reading of "actionable": no new word of Kam's, no ruling, no client human, no production touch, no device run, no money, no external message, not already built, no HELD/DROPPED line in the pickup or the 11-25 and 11-26 daily notes. Composer: building and landing code is allowed; **any deploy of a changed content release is refused until Kam's own card** (DRAFTER_RULES line 99; main now holds `release-demo` `5db37614` and `release-draft` `5679855b`, read by the Composer sub-sweeper).

Suggested wave order (one seat per project at a time, NexusAI one jest lock): OXPd lane A then B (no shared path, both Opus per `OXPd_2/CLAUDE.md:7`); NexusAI lane 4 head (RD-1044, RD-983, RD-1045, RD-1043: read today) and lane 1 (RD-893, RD-1009); MPS lane L1 then L2; Composer PCOMP-23 last.

Frame notes: every project's local `2_Project_Files` checkout was stale or on another branch (NexusAI HEAD 2026-09-08, MPS on `b03/api`, Composer 103 behind), so all file reads are `gh api -X GET .../contents/<path>?ref=<sha>`. The OXPd owed list carries line pointers written at older mains; those cited here were re-measured at `8757daa6` and several drifted (named in the OXPd section).

---

## 1. NexusAI (Jira RD, repo `datasecau/Reporting_Dashboard_Au`)

Written Thu 26 Nov 2026 04:54:38 AEDT (program `date`). Sub-sweeper (Sonnet). Baseline: SWEEP-0600 (11-25) NexusAI section, re-screened against today board and origin main.

### 1. Census
- JQL: `project = RD AND ( statusCategory != Done )`, instrument: helper `jq.py dump` (pre-dumped RD.tsv, 911 rows, read by program).
- Total 911. Per status (program count of RD.tsv): To Do 369, Testing 326, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2.
- Testing and Release Ready are not work: counted, not read. To Do 369: every title read; descriptions plus newest comments read for the keys named in section 3 as read today (about 30 tickets; the rest of the actionable set is carried from the SWEEP-1110 tables whose stamps are unchanged since 11-24 and is marked "carried").
- Origin: main = `e789995a809096b5ee79ac708358cafb6a5f7eb5` (gh api commits/main). The local checkout 2_Project_Files is STALE (HEAD cd2b5439, 2026-09-08; origin objects absent; its ls-remote also fails on the unmounted deploy key), so every line number below was read from origin e789995a via gh raw contents, not the local tree. Open PRs: none. Pushed heads: 520; the 13 `b14xx` branches: 11 are ahead 0 (merged: b1431 x4, b1432 x2, b1433 x2, l1-design-inventory, session-revocation-clarification, rd407-r2) and 2 are DIVERGED, unmerged, dormant since 2026-11-10: `b1480/nexusai-s-setup-column-mapping` (ahead 12, behind 293, RD-967) and `b1480/nexusai-s-viewer-write-gates` (ahead 7, behind 293, RD-958/793, not To Do). Other heads are `wip/*` (66), `records/*` (55), old `rd-*` and `*-history-docs` branches, not measured one by one (UNMEASURED whether any carries unmerged work).
- Authority (NexusAI CLAUDE.md): Tuesday may authorise merges, demo/dev deploys, ticket moves; production, money, external comms, irreversible need Kam. Review gate before any deploy; `npm run verify` verdict line only; Opus not required by the project file for this repo (CLAUDE.md names no model). C-224 demo/deploy hold stands (no deploy from any lane below); RD-1035 DROPPED by Kam.

### 2. Landed or in flight since the 11-25 baseline
- Landed and now Testing (verified in RD.tsv): RD-974 (Testing), RD-975 (Testing), RD-1017 (Testing), RD-1037 (Testing), RD-1039 (Testing). RD-1040 (PR 254) and RD-1021, 1026, 1034 are not on the open To Do list. Main moved 11149d3f -> 5ba5ca37 (PR 259, RD-1037) -> e789995a (PR 260, records).
- RD-1017 re-read at origin: `AUDIT_ACTIONS.SETTINGS_CHANGE` now defined at server.js:460 (was missing), used at 17388 and 17638: landed.
- In Progress (8, board only): RD-49, RD-81, RD-427, RD-431, RD-432, RD-450, RD-643, RD-662. Not read; owned elsewhere.
- Nothing is in an open PR. The only unmerged pushed work found is the two diverged branches above.

### 3. Actionable (To Do, buildable now with no new word of Kam)
Sizes: S under 1.5 h, M 1.5 to 4 h, L more. "carried" means taken from the SWEEP-1110 tables (stamp unchanged), files per lane ownership, not re-read at e789995a today. `scripts/verify-expected-counts.json` is regenerated by Tuesday at landing and is not listed.

#### Lane 1 (server)
| key | title (short) | why actionable now | size | files | conflicts / notes |
|---|---|---|---|---|---|
| RD-820 | validateConditionWithAI's own AI-off gate (aiGate.assertEnabled) is guarded by no cell: its onl | AI-off gate in validateConditionWithAI (server.js ~5926) has no cell: extract to a module with injected deps, cell + mutant; leave the Azure/Ollama body oddity out | M | backend/server.js (~5926, ~6969) + one new backend module + 1 test |  |
| RD-893 | PUT /api/risk-conditions/:id leaves its other fields unchecked (condition_text, is_active and e | type checks on condition_text, is_active, email_recipients in the PUT still absent (PUT at server.js 21684-21712 checks only risk_level; PR 131 landed the lower-casing); nonstring condition_text would throw in generateKQLQueryForCondition | S | backend/server.js (~21684-21712) + 1 new test |  |
| RD-1009 | The final error handler sends the thrown or parser text in the development setting for a body n | dev-setting final handler echoes parser/thrown text: build ONLY the early 400 on POST /api/chat/stream (server.js 7878-7879, RD-1007 shape); the parse-error handler choice is a decision, leave out | S | backend/server.js (~7878) + 1 test |  |
| RD-1010 | 30 route handlers still read their fields from the request body with one unchecked line, so a b | 30 handlers still destructure req.body unchecked (list in ticket, server.js 3099, 3684, 4142, 4199, 7056, 7191, 7879, 14874, 15236, 17789, 15558, 16333 ...): census over HTTP first, then early check keeping the field-read line byte-identical; the 400-vs-403 order for a group is one decision: take the route own existing answer, record the question | M | backend/server.js (many regions) + census script/tests |  |

#### Lane 2 (backend periphery)
| key | title (short) | why actionable now | size | files | conflicts / notes |
|---|---|---|---|---|---|
| RD-455 | SCIM provisioning: saving a group-mapping change without generating a new bearer token is refus | SCIM mapping save refused without a new token (400 INVALID_SCIM_TOKEN): real bug measured twice | M | backend/routes/entraProvisioning.js, backend/services/entraProvisioning.js |  |
| RD-728 | RD-628 G2 false-red when MACHINE_ID or WEBSITE_SITE_NAME is set in the runner env: scrub them;  | golden-blob cell false-red when MACHINE_ID/WEBSITE_SITE_NAME set: scrub the two env vars | S | backend/encryptionService.js test side + tests |  |
| RD-744 | RD-685 C-F1: after a hard-link refusal, a changed or deleted inode on our name lets the LIVE re | re-drive certifies purged after a hard-link refusal (High) | M | backend/dataErasure.js |  |
| RD-745 | RD-685 C-F2/C-F3: a non-normalised DATA_DIR (trailing slash or ./data) makes two of our own nam | non-normalised DATA_DIR makes two names refuse each other | S-M | backend/dataErasure.js; its Dockerfile part goes to lane T |  |
| RD-750 | RD-684 B-P1: one erasure ledger record lists the re-created feedback.json in BOTH filesPurged a | ledger record lists feedback.json in both filesPurged and filesFailed | S | backend/dataErasure.js |  |
| RD-759 | CSP intake: userinfo still kept for a leading U+00A0/U+2028/U+FEFF, an @ only as %40, and data: | third shape: data: addresses with an at-sign; product owner ruling 2026-11-11 (ticket comment 41051) is to REFUSE them, build owed; 2 shapes landed in PR 186 | S | backend/services/cspReport.js + 1 test |  |
| RD-824 | RD-640 L-A5: a store/copy link failing EACCES, EPERM or ENOTDIR keeps the erasure purged_incomp | store/copy link failing EACCES/EPERM/ENOTDIR keeps purged_incomplete forever | S-M | backend/dataErasure.js |  |
| RD-981 | setQuickQuestions in simpleDb.js: INSERTs queued behind a failing INSERT can still run after th | setQuickQuestions late-INSERT race after ROLLBACK (1-3 in 20 trials): red-first cell with a null first row, then sequence the INSERTs; reviewer asks whether any caller reaches production: record it | S-M | backend/simpleDb.js + 1 test |  |
| RD-1023 | The SCIM router writes two audit entries with the router-relative path, scim_rate_limited and s | two SCIM audit rows carry router-relative path (scimProvisioning.js 119 scim_rate_limited, 155 scim_auth_failed) | S | backend/services/scimProvisioning.js + 1 test |  |

#### Lane 3 (static front end)
| key | title (short) | why actionable now | size | files | conflicts / notes |
|---|---|---|---|---|---|
| RD-1014 | Values from outside are still written into the page as HTML or into quote-unsafe attributes aft | outside values still written as HTML/quote-unsafe attributes after RD-861 (scan file names, print-log users...) | M | static/js/index.js, settings.js, first-run-setup.js; after 1016, runs last of the HTML ones |  |
| RD-1015 | RD-835 residue: four CSV writers still write numeric cells (sheets, pages, size) without the he | 4 CSV writers write numeric cells without the helper (index.js 5874, 5915 show esc() on text but not on numbers; csvCell defined at 124) | S | static/js/index.js |  |
| RD-1016 | static/js/settings.js defines escapeHtml twice (lines 93 and 2440) and the page uses the second | settings.js defines escapeHtml twice (lines 93 and 2440) and the page uses the second, which lets arrays/objects through | S | static/js/settings.js; BEFORE RD-1014 |  |
| RD-1038 | On the dashboard's anomalies tab the High Risk label reads 3 point 96 and 4 point 46 to 1 in da | High Risk label colour: source found now: static/css/index-styles.css:1310 .risk-high { color: #e74c3c }; reads 3.96/4.46 dark, 3.82 light vs 4.5; coupling: light baseline bound to the 982-row dataset; pick a brand-palette token | S | static/css/index-styles.css (1310), static/css/dark-mode.css, contrast baselines |  |
| RD-117 | first-run-setup applies a CSP-blocked inline style — error on every load of the page a fresh cu | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | first-run-setup.html, js/first-run-setup.js |  |
| RD-144 | Dashboard tab strip has no tablist/tab/tabpanel semantics — WCAG 4.1.2 (SUS-10, pre-existing) | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | static/index.html, js/index.js (with 351) |  |
| RD-145 | All vendor CSS/JS loads from cdn.jsdelivr.net — in an egress-filtered tenant every icon disappe | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | all static/*.html + vendor files + Dockerfile (give the Dockerfile edit to lane T); run LAST |  |
| RD-151 | Cost settings errors are shown as a page banner and the server's actionable `details` is discar | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | settings.html, js/settings.js |  |
| RD-164 | Dark mode's neutral card border #3a3a5a on #1e1e3f is 1.47:1 — below the 3:1 that the tinted va | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | static/css/dark-mode.css |  |
| RD-176 | Provisioning mode cards paint their ground from JS inline styles, so the dark fix has to win by | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | js/entra-provisioning-ui.js, css |  |
| RD-188 | The first-run wizard violates the product's own CSP ~20 times per session — a style the product | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | first-run-setup.html/js (same class-move as 117) |  |
| RD-220 | P11-07: console errors on every dashboard load, four families — three /api/normalized/* 503s, a | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | js/index.js |  |
| RD-222 | The wizard's ACTIVE step-number chip is white on a translucent-white composite at 3.74:1 in LIG | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | static/css/first-run-setup-styles.css |  |
| RD-259 | index.html reports 9 console errors on load (index-offline.html 1) — logged by QA pass 13b and  | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | js/index.js, index-offline.js |  |
| RD-261 | brand-buttons.css is a single point of failure for the brand — if it fails to load, all 42 .btn | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | static/css/brand-buttons.css |  |
| RD-351 | .tab-button has no project focus style — the UA default focus ring is now blue on a blue-adjace | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | static/css/index-styles.css |  |
| RD-371 | RD-148 round-1 residuals F-4/F-5/F-6: revoke UI shows an unlabelled local-time date, has no liv | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | js/entra-provisioning-ui.js |  |
| RD-373 | N-3 + N-5: the still-live revoke warning is partly covered by the Feedback widget, and the revo | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | js/entra-provisioning-ui.js |  |
| RD-396 | RD-150 residue (gate F-2, F-3): red_flag_enabled stored as '' or 0 renders the Settings toggle  | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | js/settings.js (937) AND backend/services/riskAlertScheduler.js (the only backend file in this lane: lane B must not touch it) |  |
| RD-416 | First-run polish: opening User Access throws a page error (first-run-setup.js:3517), the page o | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | js/first-run-setup.js (3517), first-run-setup-styles.css |  |
| RD-483 | The open-access banner sits 24px (admin.html) and 32px (legal.html) below the top of the page i | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | static/admin.html, legal.html |  |
| RD-512 | RD-490 banner guard does not check the dark theme: the open-site banner's visibility and ink ar | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | tests/e2e/open-access-banner-guard.js |  |
| RD-513 | RD-490 banner guard measures one viewport (1366x900): phone-width concealment of the open-site  | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | tests/e2e/open-access-banner-guard.js |  |
| RD-515 | RD-490 banner guard does not cover the inline first-run open-site note (.nx-open-access-banner- | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | tests/e2e + first-run-setup.html (after F1 items) |  |
| RD-540 | The PRECONDITION cell in rd465-first-run-open-window.test.js passes with the entire page script | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | __tests__/rd465-first-run-open-window.test.js |  |
| RD-613 | The storage-wiped alarm banner renders only on the dashboard: Settings, admin pages and first-r | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | static/js/*.js (alarm banner on other pages) |  |
| RD-687 | First-run's danger status branches are unreachable: no caller passes 'error' to the data-source | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | js/first-run-setup.js |  |
| RD-832 | admin.html logs two '403 (Forbidden)' resource loads in open mode on a fresh install; the URLs  | carried from SWEEP-1110 table, not re-read today (stamp unchanged since 11-24) | S-M | static/js/admin.js |  |

#### Lane 4 (tests, scripts, CI, Dockerfile)
| key | title (short) | why actionable now | size | files | conflicts / notes |
|---|---|---|---|---|---|
| RD-983 | Test harness follow-ups from the independent review of the RD-982 change: a LOG_LEVEL of warn o | harness follow-ups: LOG_LEVEL warn/error makes bootServer refuse every boot; cell B2 waits ~2 min (give it a ~20 s boot timeout); read at harness line 101 child env copy | S | __tests__/helpers/rd395-server-harness.js + its test |  |
| RD-1043 | Test gap: nothing pins that an undated job stays out of the week bucket, or that the off-hours  | test-only gap after RD-974 landed: two cells (undated job out of the week bucket; off-hours item needs >10 dated jobs: server.js 20350 and 20430 read as ticket says); red-first by mutation | S | __tests__/ one test file (new or the RD-974 file); NO server.js edit |  |
| RD-1044 | scripts/qa-surface-up.sh first-boot block: a failed first attempt leaves a log file in the data | qa-surface-up.sh first-boot block, 3 faults, read at origin e789995a lines 243-256: log file inside the data folder (FIRST_BOOT_LOG line 244) so a retry skips the sentinel; a /tmp/ path exits 13 (state test line 248 accepts only first-boot, jsonStorage.js 1557 reads /tmp/ as ephemeral); no cell pins the state test. Fix shapes and acceptance in ticket | S-M | scripts/qa-surface-up.sh + 1 test file (RD-1037 test file or new) |  |
| RD-1045 | Test files that boot the server on a hosted Linux runner put their data folder under /tmp/, whe | server-booting tests under /tmp/ on a Linux runner: harness mkdtemp at __tests__/helpers/rd395-server-harness.js:85 uses os.tmpdir(); first a census (TMPDIR=/tmp, RUNNER_TEMP persistent), then a persistent root option or one shared helper; candidates named in ticket (rd525 helper, customer-data-lists-agree, rd421 ...) | M | __tests__/helpers/rd395-server-harness.js, __tests__/helpers/persistent-temp-root.js, the named test files; same file as 983: one owner, 983 first |  |
| RD-134 | All 12 schedulers had zero test coverage because requiring any scheduler under jest crashes at  | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-249 | qa-surface-up.sh races itself on node_modules when two surfaces are stood at the SAME head — th | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-320 | The erasure write-guard's corpus and runtime patch set are both vocabularies: three of four cor | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-345 | RD-340 residues from the round-3 gate: F21 the header + limits block still specify the round-2  | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-348 | CI's gate depends on python3 and nothing declares it — RD-339's wrapper drives tests/test_norma | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-352 | RD-341 QA-F4: four callee shapes yield neither a row nor a verdict - the label guard's docstrin | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-353 | The launcher's Jira banner reports the PAGE CAP as a count: in-progress reads 100 where the tru | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-355 | RD-341 QA-R2-F1: the label guard's second declared limit is over-general - it says an object-li | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-378 | The F-2 census's write detector follows a const/let declarator but not an assignment, a compute | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-379 | The scheduler-vocabulary test's env restore is justified by a cross-file leak risk that jest's  | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-384 | RD-376 gate findings F-1..F-5, all RECORD-LEVEL: the 'exactly two ways' reconciliation claim is | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-387 | RD-293 gate residue: the new seed warning has no guard, near-miss SEED_DEMO_DATA values are sti | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-394 | RD-382 residue (gate F-1..F-4): JIRA.md's normalised recipes fail from the project root; the JI | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-397 | RD-327 residue (gate N-1, P-1): build-commit-sha.sh calls a tree clean with plain git status -- | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile (Dockerfile owned here) |  |
| RD-426 | Three suites fail under heavy machine load and pass alone: setup-rate-limit-allowance, erasure- | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-539 | The RD-490 round-1 mutation harness cannot be reused as-is: 5 of its 15 anchors no longer exist | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-566 | RD-561 gate residue (B-1..B-3): 'no env opt-out' has no cell; guard refuses -w2/--max-workers=2 | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-572 | RD-568 residue: auth-gate-fail-closed leaks a legacy machine-id into the shared worker HOME; ga | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-580 | RD-342's gitleaks preflight has never run: the launcher reads preflight-gitleaks.sh from the st | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-586 | jira-query.sh --count returns a real-looking 0 (exit 0) for a status NAME that does not exist - | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-595 | rd523 and rd545 now require an RFC1918 interface on the test host and bind stand-ins on its rea | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-597 | NEW-1's guard 3 cannot distinguish a connection refusal from an accept-then-reset: the openai S | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-599 | RD-518 r3 H-01: the ANONYMOUS cell in rd518-r3-health-detail-decision measures a 401, not a red | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-600 | RD-518 r3 H-02: the precondition cell reads roles via /api/auth/check, which bypasses the middl | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-623 | RD-524 gate-3 polish F-A3/F-A4/F-A6: READY overstated 'every M1 red behavioural', no cell for t | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-668 | Under jest the Key Vault SDK cannot load ('@azure/keyvault-keys not installed (Unexpected token | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-726 | RD-696 cell 5 reds with EINVAL on a long TMPDIR (socket path over 104 bytes), and the 250 ms ex | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-757 | RD-591 g3: a FOREIGN connect-write-close dial reads 'vanished' and is COUNTED in a positive-arr | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-810 | CodeQL baseline (test code, medium): js/file-access-to-http in tests/uat-run.js:30 - a file-rea | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-829 | Gate 14 findings for RD-430 + RD-694 item 4: the manifest _about's '147 occurrences' total is f | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-918 | RD-913 follow-up: sqlite3 6 arrives through an install script that npm 11.19 warns about on eve | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile (Dockerfile owned here) |  |
| RD-1018 | The committed cells for RD-445 mock the token library, so a weakened verification (the audience | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-1024 | RD-1011 and RD-1012 residue: no committed cell counts the stored-source read for a refused call | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |
| RD-1027 | RD-1008 residue: no committed cell turns red when only one of the five route-side class checks  | carried from SWEEP-1110 table NX-T, not re-read today (stamp unchanged) | S | scripts/*, __tests__/*, .github, Dockerfile |  |

### 4. Lanes (at most 4, file-disjoint, by value)

1. **Lane 1, server (value: security/correctness, one owner of the hot file).** Owns `backend/server.js` only (plus new backend modules it extracts, plus one new test file per key). Order: RD-893, RD-1009, RD-1010 (census first), RD-820. Must NOT touch: `backend/services/*`, `backend/dataErasure.js`, `backend/simpleDb.js`, `static/**`, `scripts/**`, `__tests__/helpers/**`. Opus-class review for RD-1010 (30 routes). No deploy.
2. **Lane 2, backend periphery.** Owns `backend/routes/entraProvisioning.js`, `backend/services/entraProvisioning.js`, `backend/services/scimProvisioning.js`, `backend/services/cspReport.js`, `backend/dataErasure.js`, `backend/encryptionService.js`, `backend/simpleDb.js`. Order: RD-1023, RD-759, RD-455, RD-744, RD-745 (Dockerfile part to lane 4), RD-750, RD-824, RD-728, RD-981. Must NOT touch `backend/server.js`, `backend/services/riskAlertScheduler.js` (lane 3 owns that one line of backend for RD-396), static, Dockerfile.
3. **Lane 3, static front end (F1 + F2 + X merged, sequenced).** Owns `static/**` (html, js, css), `tests/e2e/**`, and `backend/services/riskAlertScheduler.js` for RD-396 only. Order: RD-1038, RD-1016, then first-run items (RD-117/188/176, 416, 687, 540, 371/373, 151, 396), then dashboard items (RD-144/351, 164, 222, 220/259/261, 483/613/832, 512/513/515), then RD-1014 and RD-1015, RD-145 LAST (needs the Dockerfile edit from lane 4). Must NOT touch `backend/**` (except the one scheduler file), `scripts/**`, `__tests__/helpers/**`.
4. **Lane 4, tests, scripts, CI, Dockerfile.** Owns `scripts/**`, `.github/**`, `Dockerfile`, `docker/**`, `package.json`, `__tests__/**` (all test files and helpers except the new per-key test file each of lanes 1-3 adds, and the e2e folder), `docs/**`. Order: RD-1044, RD-983, RD-1045 (983 and 1045 share the harness file: one owner, 983 first), RD-1043, then carried NX-T keys. Must NOT touch `backend/**`, `static/**`.
Cross-lane: lanes 1-3 each add new test files under `__tests__/` named for their key: that is additive, no shared file. Only shared path is `scripts/verify-expected-counts.json` (Tuesday regenerates). One jest lock: run lanes one seat at a time per project rule, ordering 1, 4, 2, 3 or by value as above.

### 5. Notes on the named candidates
- **RD-1044** (Bug, Low): ACTIONABLE, lane 4. Read whole; lines confirmed at origin e789995a `scripts/qa-surface-up.sh` 243-256. No ruling needed; fix shapes proposed in the ticket.
- **RD-1045** (Task, Low): ACTIONABLE, lane 4, but first step is a census (printed list of boot folders) before the change; same helper file as RD-983.
- **RD-1043**: actionable test-only. **RD-1042**: EXCLUDED, text-or-test choice is a product choice. **RD-1041**: EXCLUDED, which fields each role may read is undecided; same family as the plain data-source routes that wait on Kam card.
- RD-893: the type-check half is buildable; its Log Analytics measurement (1) needs a stand with a workspace, leave it out. RD-896: measure-only, needs a data copy from the product owner: excluded. RD-892 part (b): product owner question: excluded.
- RD-578: EXCLUDED, server.js:769 comment says the unset name is DELIBERATE and correcting it changes what a Marketplace deploy does (ruling).
- Greps on daily notes 2026-11-25 and 2026-11-26 (program, whole lines, positive control RD-1037 = 13 hits): no HELD, DROPPED, ruling or in-flight line names any actionable key in section 3 other than RD-1014 (a records line about overlap with RD-1039, landed) .

### 6. Excluded (one class per line; every key listed)
- **needs a ruling or word of the product owner (named question in the daily notes or the ticket)** (38): RD-193, RD-305, RD-313, RD-433, RD-522, RD-546, RD-578, RD-583, RD-584, RD-610, RD-612, RD-622, RD-636, RD-644, RD-702, RD-763, RD-764, RD-768, RD-805, RD-840, RD-858, RD-876, RD-884, RD-892, RD-896, RD-925, RD-927, RD-989, RD-997, RD-1006, RD-1019, RD-1020, RD-1022, RD-1025, RD-1028, RD-1029, RD-1041, RD-1042
- **dropped by Kam** (1): RD-1035
- **in flight in a pushed unmerged branch (b1480/nexusai-s-setup-column-mapping 12 ahead, 293 behind)** (1): RD-967
- **landed on main per the 11-25 sweep, records only (board still To Do)** (22): RD-312, RD-498, RD-538, RD-544, RD-563, RD-577, RD-605, RD-729, RD-731, RD-796, RD-798, RD-826, RD-929, RD-962, RD-963, RD-969, RD-970, RD-972, RD-977, RD-978, RD-979, RD-1036
- **Roles UI chain (label roles-ui-2026-11: behind the shell, word packs, design-first)** (30): RD-928, RD-930, RD-931, RD-932, RD-933, RD-934, RD-935, RD-936, RD-937, RD-938, RD-939, RD-940, RD-941, RD-942, RD-943, RD-944, RD-945, RD-946, RD-947, RD-948, RD-949, RD-950, RD-951, RD-952, RD-953, RD-954, RD-955, RD-956, RD-957, RD-966
- **not agent work: epic, business, compliance, Azure and secrets, Jira admin or session and launcher tooling, feature request, dated, customer-test, Partner Center** (61): RD-6, RD-7, RD-8, RD-13, RD-20, RD-21, RD-22, RD-28, RD-29, RD-30, RD-31, RD-34, RD-50, RD-54, RD-55, RD-83, RD-146, RD-233, RD-287, RD-400, RD-401, RD-414, RD-415, RD-449, RD-467, RD-468, RD-469, RD-473, RD-479, RD-480, RD-507, RD-520, RD-530, RD-534, RD-536, RD-542, RD-543, RD-552, RD-562, RD-570, RD-587, RD-642, RD-659, RD-660, RD-661, RD-663, RD-664, RD-666, RD-667, RD-672, RD-673, RD-724, RD-738, RD-739, RD-742, RD-827, RD-842, RD-886, RD-984, RD-1001, RD-1004
- **operations / QA-gate-finding residue: read by title and label only, NOT screened for actionability, UNMEASURED** (132): RD-69, RD-76, RD-132, RD-133, RD-152, RD-154, RD-156, RD-162, RD-178, RD-221, RD-231, RD-234, RD-235, RD-236, RD-252, RD-262, RD-268, RD-276, RD-280, RD-285, RD-289, RD-316, RD-317, RD-319, RD-325, RD-326, RD-328, RD-331, RD-344, RD-346, RD-350, RD-356, RD-357, RD-358, RD-359, RD-360, RD-364, RD-366, RD-370, RD-375, RD-380, RD-383, RD-386, RD-389, RD-390, RD-392, RD-393, RD-398, RD-405, RD-406, RD-420, RD-421, RD-422, RD-434, RD-439, RD-440, RD-445, RD-446, RD-457, RD-458, RD-478, RD-482, RD-484, RD-485, RD-487, RD-488, RD-489, RD-493, RD-496, RD-500, RD-502, RD-504, RD-509, RD-511, RD-517, RD-519, RD-532, RD-537, RD-547, RD-548, RD-550, RD-551, RD-553, RD-556, RD-557, RD-565, RD-569, RD-581, RD-582, RD-588, RD-589, RD-596, RD-598, RD-611, RD-620, RD-621, RD-632, RD-633, RD-634, RD-635, RD-637, RD-650, RD-654, RD-655, RD-674, RD-688, RD-712, RD-713, RD-714, RD-715, RD-716, RD-718, RD-722, RD-725, RD-727, RD-740, RD-746, RD-748, RD-758, RD-792, RD-797, RD-834, RD-845, RD-854, RD-855, RD-859, RD-872, RD-901, RD-908, RD-909, RD-911, RD-914
- **needs a ruling (label needs-decision or kam)** (1): RD-368
- **brand-palette residue (labelled brand; read by title and label only, UNMEASURED; plausible later test/css lane work)** (10): RD-676, RD-677, RD-678, RD-679, RD-680, RD-701, RD-704, RD-752, RD-753, RD-754
- **CodeQL baseline (held per 11-25 sweep for the open ones; read by title only, UNMEASURED)** (1): RD-806

### 7. Other statuses (counted; keys are on the board list)
- Testing (326): 326 keys, not read (not work)
- Release Ready (199): 199 keys, not read (not work)
- In Progress (8): RD-49, RD-81, RD-427, RD-431, RD-432, RD-450, RD-643, RD-662
- Put on Hold (7): RD-18, RD-32, RD-33, RD-41, RD-93, RD-104, RD-743
- Declined (2): RD-300, RD-564

### 8. Program check against RD.tsv
- RD.tsv rows 911. Assigned: actionable To Do 79 + excluded To Do 290 + Testing/Release Ready/In Progress/Hold/Declined 535 = 904, plus 7 keys named in an excluded class but already past To Do (listed next line) = 911, equal to the RD.tsv rows.
- Missing (in RD.tsv, unassigned): 0 []. Extra (named in my lists but NOT on the open board): [].
- Keys named in an excluded class that are on the board but not To Do (counted under their status, not as To Do): [796, 798, 840, 962, 963, 979, 1036].
- Actionable per lane: Lane 1 (server) 4, Lane 2 (backend periphery) 9, Lane 3 (static front end) 28, Lane 4 (tests, scripts, CI, Dockerfile) 38. Total 79.
- UNMEASURED: the 132 operations residue keys plus the 10 brand and 1 CodeQL residue keys (section 6 last classes) beyond title and label; whether the 66 wip/* and old rd-* branches carry unmerged work; the carried keys files against e789995a (only the ones in section 5/3 with line numbers were re-read); demo/prod state (no host contacted).


## 2. OXPd 2 (Jira OXPD2; the work list is the owed list in BACKLOG.md)


Census (instrument: `jq.py dump` over Jira REST `search/jql`, GET only, JQL `project = OXPD2 AND ( statusCategory != Done )`, paginated to the end, total **59**: Backlog 57, In Progress 2; read Thu 26 Nov 2026 04:53:20 AEDT). Control: the dump holds 59 unique keys. OXPD2 is a Jira board of question, action and umbrella tickets: **the build work is the 147-line owed list in `OXPd_2/BACKLOG.md`** (instrument: awk over the lines `N. - [ ]` and `N. - [x]`: **100 open, 47 ticked, 147 numbered, none missing**; the first 8 owed lines are of 2026-11-20, 145 to 147 new today from PR 53). Origin main `8757daa6c48d1f6764460d378ce3c15863b383df` (`gh api -X GET repos/datasecau/OXPd_2/branches/main`, read Thu 26 Nov 2026 04:53:20 AEDT); open pull requests: **0** (`pulls?state=open` empty); 55 branches on origin, the `b20xx` ones are squash-merged leftovers (not proven by compare: UNMEASURED); no seat live (NEXT-PICKUP DELTA 1470).

Rules read from `OXPd_2/CLAUDE.md`: every agent on the newest **Opus** (line 7); a seat pushes a BRANCH only, Tuesday opens the PR and lands by SQUASH pinned to the reviewed head with `--match-head-commit` (lines 55-57 and 82); toolchain `.tools/dotnet` 10.0.404 project-local (line 83), a seat never downloads one; nothing under `Source_Documents/` is committed; no Azure outside `oxpd2-dev-rg`; no word to HP or any person; secrets by location only. **No device run is in this sweep**: first-run row 3 (PR 52) and row 4 (PR 53, landed 04:09 today) are built and NOT run on the printer; row 4 needs Kam's word first (CLARIFICATIONS 1088, C-84), owed 118 is tied to the test-button lane.

**Line pointers.** The BACKLOG pointers were written at earlier mains and several have drifted at `8757daa6` (measured: `Oxpd1Writer.cs:131/167/274/538`, `Oxpd1Client.cs:44`, `Oxpd1Command.cs:597/786` no longer hold the cited text). Pointers printed below are re-measured at `8757daa6` by `gh api -X GET .../contents/<path>?ref=8757daa6` plus a regex over the decoded text (control: `LabFiles.cs:414-419` and `Oxpd1Soap.cs:174,252` match the backlog text); every builder re-locates by symbol, never by the backlog line.

#### Actionable now: three code lanes, one guard lane, one records lane (agent work, no device, no ruling, no HP, no tenant)

Every row below is an OWED-LIST item; its fix shape is in the item ("the coordinator's choice" items name Tuesday as the chooser, not Kam: Tuesday states the choice in the kit). Sizes are the sweeper's estimate (S under 1 h, M 1-3 h, L longer), not measured.

**Lane OX-A, the OXPd 1.x client (owns `src/Datasec.Suite.Adapters.Oxpd1/**` and `tests/Datasec.Suite.Adapters.Oxpd1.Tests/**` and that module's README; must not touch `src/Datasec.Suite.Lab/**`).** The first four are one family: .NET `IsNullOrWhiteSpace` taken for XML white space.

| owed | what | files (measured at `8757daa6`) | size |
|---|---|---|---|
| 133 | OXPd 1.x client (after pull request 51): the sync echo's reader takes a no-break space or other non-ASCII whit | `Oxpd1Soap.cs:252` (`ReadTextAnswer`, `IsNullOrWhiteSpace` in the text-besides test) | S |
| 143 | OXPd 1.x client (after pull request 52): the CA store reader takes a no-break space or other non-ASCII white s | `Oxpd1Writer.cs` CA store reader (text beside the entries) | S |
| 146 | OXPd 1.x client (after pull request 53): the top-level button records reader takes a no-break space or other n | `Oxpd1Writer.cs:756-757` `OnlyElements` (called at 642, 648, 720, 726) | S |
| 126 | Lab tool oxpd1 (after pull request 48): five answers to IsServiceEnabled that HP's schema refuses are still re | `Oxpd1Soap.cs:174` (`TextOnly` counts elements and attributes, not text nodes) | M |
| 134 | OXPd 1.x client and lab (after pull request 51): the echo's callback reader passes callback bodies HP's schema | `Oxpd1Echo.cs:212` `CallbackMessage`; two README sentences (one is in the Lab README: cross-lane, see exceptions) | S |
| 93 | OXPd 1.x write client: the sign-in agent record takes an address whose user-information part is empty (an @ ri | `Oxpd1Writer.cs:188` and `:290` (`UserInfo.Length != 0`; also refuse an `@` in the authority, one more W07 row) | S |
| 85 | OXPd 1.x read client: the work after the answer's body (the parse, the mask and the record) is not under the t | `Oxpd1ClientOptions.cs:86` (narrow the `Timeout` summary to the README's words; the attribute cap is optional follow-up) | S |
| 94 | OXPd 1.x write client: the undo of a sign-in agent register is the unregister of the same id, which leaves the | `Oxpd1Writer.cs` undo of a register + README named limit (the lab half, a read before register, is lane OX-B's) | S |

Order: 133, 143, 146 (same helper, one patch family), 126, 134, 93, 85, 94. Gate G1. Tests: `tests/Datasec.Suite.Adapters.Oxpd1.Tests`.

**Lane OX-B, the lab tool `oxpd1` (owns `src/Datasec.Suite.Lab/Commands/Oxpd1/**`, `tests/Datasec.Suite.Lab.Tests/Oxpd1/**` and the Lab README; must not touch `src/Datasec.Suite.Adapters.Oxpd1/**`).**

| owed | what | files (measured at `8757daa6`) | size |
|---|---|---|---|
| 106 | Lab tool oxpd1 write: the read before a register reads the child elements of the result only, so the same id h | `Oxpd1Command.cs` read-before-register (child elements of the result only; the cited `:786-808` has drifted: relocate by symbol) | M |
| 107 | Lab tool oxpd1 write: U+FFFF in the host of --agent-service or --prompt-page passes the lab and the envelope's | `Oxpd1Command.cs` `--agent-service` / `--prompt-page` (U+FFFF; host checks at `:37` and `:416` use `Uri.CheckHostName`) | S |
| 108 | Lab tool oxpd1 undo-owed: a run folder it cannot open is counted as a folder without a list, so beside readabl | `LabFiles.cs` folder loop (an unopenable run folder printed as `nothing is owed`, exit 0) | S |
| 109 | Lab tool oxpd1 write: a host that is not ASCII is written into the envelope as typed, and a lone surrogate in  | `Oxpd1Command.cs` address options (non-ASCII host, lone surrogate) | S |
| 110 | Lab tool oxpd1 write: the agent name's length rule counts UTF-16 code units, not characters | `Oxpd1Command.cs` agent-name length rule counts UTF-16 units | S |
| 111 | Lab tool oxpd1 undo-owed: the folder and list shapes the review's probe measured beyond the six of cell U05 ha | `tests/Datasec.Suite.Lab.Tests/Oxpd1/Oxpd1WriteTests.cs` cell U05 (shapes beyond the six) | S |
| 127 | Lab tool oxpd1 (after pull request 48): a run folder behind a relative symbolic link whose target walks .. thr | `LabFiles.cs:119` `RealPath` (relative link target walking `..` through another link) | M |
| 135 | Lab tool oxpd1 echo (after pull request 51): a --callback-host that makes the callback address longer than 256 | `Oxpd1EchoVerb.cs:125` `--callback-host` (:126 `CheckHostName`; callback address built at :334 may exceed 256 characters) | S |
| 136 | Lab tool oxpd1 echo (after pull request 51): a --delay-ms longer than the callback wait (async) or the time-ou | `Oxpd1EchoVerb.cs:117` `--delay-ms` vs the callback wait and time-out | S |
| 142 | Lab tool oxpd1 write (after pull request 52): the certificate file's 64 KiB bound reads the size of the path i | `LabFiles.cs:242-243` certificate file bound reads the path's own size (`new FileInfo`, :249 read) | S |
| 145 | Lab tool oxpd1 undo-owed (after pull request 53): the family of a write is chosen with a default arm that puts | `LabFiles.cs:414-419` `Family` default arm `_ => "button"` (name the two button kinds, default arm throws, one mapping cell) | S |

Order: 108, 111, 145, 142, 110, 109, 107, 135, 136, 127, 106. One file (`Oxpd1Command.cs`) carries 106, 107, 109, 110: one seat. Gate G1.

**Lane OX-C, the other modules' hygiene (owns `src/Datasec.Suite.Server/README.md`, `src/Datasec.Suite.Jobs.Transport/**`, `src/Datasec.Suite.Adapters.Oxpd2/DeviceAuth/**`, `src/Datasec.Suite.Graph/**`, `src/Datasec.Suite.UniversalPrint/**`, `src/Datasec.Suite.Identity/README.md`, `tests/Datasec.Suite.{Server,Graph,UniversalPrint,Adapters.Oxpd2}.Tests/**`; touches neither A's nor B's paths).**

| owed | what | files | size |
|---|---|---|---|
| 84 | Server README: its one-header-line sentence says the answer is 401 wit | `src/Datasec.Suite.Server/README.md:21-23` one-header-line sentence says 401 where a throwing vault gives 503 | S |
| 119 | Server README: the new 503 sentence is false for a serial whose stored | `src/Datasec.Suite.Server/README.md` the new 503 sentence is false for a cached serial (same file as 84: one edit) | S |
| 120 | Jobs transport: two measured sentences carry no platform word (the cancellation sentence of its README and the | `src/Datasec.Suite.Jobs.Transport/README.md:34` and `IppTransportException.cs:13`: two measured sentences carry no platform word | S |
| 122 | Device token client: the landed CertificateRevocationCheckMode line has no effect beside the chain policy, and | `DeviceAuth/DeviceTokenClient.cs:82` (`CertificateRevocationCheckMode = NoCheck` beside the chain policy at :83) and test cell DA18 | S |
| 131 | Graph layer: GraphClient.FollowableLink compares a next link with the addresses already requested with its fra | `src/Datasec.Suite.Graph/GraphClient.cs:734` and `:647` (next link compared with its fragment) | S |
| 54 | Universal Print registration: cells the review found missing (the code is right today) | `tests/Datasec.Suite.UniversalPrint.Tests/Registration/` cells the review found missing (code right today) | M |
| 75 | Universal Print registration: no test reaches the check of a disposed answer under the registration's lock | `Registration/CloudDeviceTokenHolder.cs` test for the disposed-answer check under the lock | S |
| 55 | Universal Print registration: platform behaviour and named limits that the review measured | `src/Datasec.Suite.UniversalPrint/Registration/` README: named limits the review measured | S |
| 77 | Identity service README: its sentence on the blob maker's two catches cites two lines that the malformed-escap | `src/Datasec.Suite.Identity/README.md:35` cites two lines that moved | S |
| 137 | Tests (landed before pull request 51): a whole-solution dotnet test on macOS arm64 can hang in Datasec.Suite.S | `tests/Datasec.Suite.Server.Tests/HostRig.cs:108` `StartAsync()` and `:171` `StopAsync()` take no cancellation token: add a per-cell bound (cause UNMEASURED; seen once) | M |
| 121 | The other device-facing HTTP handlers have no chain policy, so owed item 79's fetch concern is closed for the  | `Oxpd1Client.cs:49`, `HttpIppTransport.cs:33`, `Lab/Device/DeviceChannel.cs:52` each `new SocketsHttpHandler`: the same chain policy or one README line each. CROSS-LANE (A's and Lab paths): the README-line option stays inside OX-C; the policy option waits until A and B have landed | M |
| 138 | The heavy-job runner the build lanes copy (heavy.py): at its time bound it ends dotnet test but not the test h | `.tools/b2067/gate/heavy.py` (outside the repository, the runner copy): kill the test host process group at its time bound. Tooling, not product | S |

Order: 84+119, 120, 77, 131, 122, 54, 75, 55, 137, 138, 121. Gate G1 for 122, 131, 137; G2 acceptable for README-only rows.

**Lane OX-D, repository rules, release guard and CI (owns `build/**`, `.github/workflows/ci.yml`, the repository `README.md`; no overlap with A, B or C).** Several of these may be built or part-built by PRs 49 and 6 to 11 (the owed list was not re-ticked for every clause): UNMEASURED which clauses remain, so the builder's PRIOR WORK check and a grep at main settle each before any edit.

| owed | what and files | size |
|---|---|---|
| 11 | `build/release_guard.py`: ZIP-format files only; tar/gzip not seen | S to M |
| 12 | `build/repo_rules.py` rules R1, R3, R4 read lines, not YAML | S to M |
| 16 | the `secret-scan` job of `.github/workflows/ci.yml`: own limits | S to M |
| 17 | `build/repo_rules.py` rule R5: the hash half cannot run on a runner | S to M |
| 19 | `README.md` the S1 sentence (Jira OXPD2-20) | S to M |
| 20 | `build/` a script that scans a squash message (Jira OXPD2-21) | S to M |
| 21 | `ci.yml` the second scan's own checks, planted count, speed (Jira OXPD2-22) | S to M |
| 22 | `build/repo_rules.py` and `build/tests/test_pipeline_controls.py`: rule checks still to add (Jira OXPD2-23) | S to M |
| 23 | `build/release_guard.py`: name rule, publish shapes, certificate forms (Jira OXPD2-24; PR 49 built part) | S to M |
| 27 | `ci.yml` lines 36 and 66: `actions/setup-dotnet` pin; publish folders hold `.pdb` and `web.config` | S to M |
| 129 | `build/release_guard.py:81` `BARE_BASE64_JOIN` does not take the JSON-escaped tab (measured: line 81 holds the pattern; one Limits clause or the escape plus a row and a mutant) | S to M |

Order: 129, 19, 27, 11, 20, 21, 22, 12, 17, 16, 23. Drafter rules 8 apply to the gate: the repository-wide rules scan runs in every gate. Jira OXPD2-25 (R6 open-quote refusal for two quoted values spread over lines) sits in this lane too: it is in no owed line, so the builder first measures whether it is still open (UNMEASURED).

**Lane OX-R, records (single owner of `BACKLOG.md`, `CLARIFICATIONS.md`, `SETUP_RUNBOOK.md`, `5_Project_History/history.md` and Jira comments; a records seat is the ONLY writer of these and must not run beside a lane that changes them):** 32 owed lines are record points "not yet filed" from kits and reviews, or runbook checks: 29, 33, 34, 35, 36, 39, 40, 41, 42, 44, 46, 49, 50, 56, 67, 72, 73, 76, 78, 86, 91, 97, 104, 105, 123, 125, 128, 130, 132, 139, 144, 147. Their source is each landing's kit, review and STATUS; none needs a ruling. Order: after lanes A to D land, so the new owed lines and the closings (ticks of 133, 143, 146, 126, ... ) go in one pass. Jira write for tickets OXPD2-8 to 19 (WP umbrellas: which are done is UNMEASURED) is the records kit's scope only if its stamp says JIRA WRITE.

#### Lanes disjoint by path (checked by name): A = Adapters.Oxpd1; B = Lab/Commands/Oxpd1 + Lab tests; C = Server README, Jobs.Transport, Oxpd2 DeviceAuth, Graph, UniversalPrint, Identity README, three test projects; D = build/, ci.yml, README.md; R = records files. Cross-lane exceptions: owed 134 (A edits `Oxpd1Echo.cs` and the Oxpd1 README; the one Lab README sentence goes to B after A lands); owed 121 (policy option crosses A and Lab paths: after A and B); owed 94 (A: writer undo and README; B's read-before-register is already item 106).

#### Excluded (OXPd, by class; every one of the 100 open owed lines is assigned once: 42 to lanes A to D, 32 records, 26 excluded; union check: assigned 100, missing 0, extra 0, by program)

- owed 1: needs HP tool (SPU) that may not be copied in; how a runner gets it undecided (person/HP).
- owed 2: the real CA certificate is not in the library copy at the cited path; a seat never searches the library (needs a person to supply it).
- owed 5: needs docker on a machine (hosted job is the only proof); not this seat class.
- owed 6: needs a Windows machine.
- owed 8: a person must launch the launcher.
- owed 10: needs a network-observed measurement of telemetry; not buildable as stated (UNMEASURED).
- owed 13: no symptom today; nothing to build (check only).
- owed 14: needs item 2 (the CA fingerprint) first.
- owed 15: the organisation ruleset on main: an admin setting, not agent work.
- owed 18: whether hosted minutes are billed: money question for Kam.
- owed 24: organisation default code-scanning setup: an admin setting.
- owed 25: edits the project CLAUDE.md, the coordinator's file; Tuesday writes it.
- owed 26: the launcher is the coordinator's frozen text.
- owed 28: a branch on origin: deleting is never an agent act (quarantine rule); Tuesday's.
- owed 30: a list of what no review measured: nothing to build.
- owed 31: design-document corrections: the documents pass is in the coordinator's tree.
- owed 32: facts bearing on work in flight; no build left stated (UNMEASURED whether any fix remains).
- owed 37: closed for two new members by PR 11; ListNames keeps its behaviour by design: no build.
- owed 38: open questions for the product owner: needs his word.
- owed 43: limits kept for a LATER data kit: later work.
- owed 57: work package WP4.1 stays open: the host wiring is later work.
- owed 92: design-document fact corrections owed to a documents pass in the coordinator's tree.
- owed 103: a first-run row-3 device run question: needs a device and Kam's word.
- owed 115: a Microsoft 365 tenant test: no tenant yet.
- owed 118: a device run (the M577 call back): needs the printer and, for row 4, Kam's word.
- owed 140: waits for HP's 1.9 SDK package to arrive.

Jira OXPD2 (59 open, by class): epics 3, 4, 5, 6, 7 (5); Kam actions and waits-on-a-person 56, 57, 58, 59, 60, 61, 63 (7) and the printer question 62; Workpath questions for a person, labelled `oxpd-workpath-question`: 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 40, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54 (25); reference document OXPD2-55 (waits for HP 1.9 SDK, owed 140); kit checklist OXPD2-2; master list OXPD2-1 (questions to Kam, comments only); WP umbrella tickets OXPD2-8 to 19 and CI tickets OXPD2-20 to 25 (their buildable content is the lane items above). Class counts to be re-verified by the program check in the report below.


## 3. MPS Commercial Calculator (Jira MPSCALC)


### Census
- JQL `project = MPSCALC AND ( statusCategory != Done )`, total 166 (instrument: the dump `MPSCALC.tsv`, 166 rows, 15 Epic + 151 Task, all Backlog). 11-11 sweep saw 214; 48 left the open set (Done by records passes). The 11-24 and 11-25 sweeps also read 166: same count today.
- Origin `datasecau/MPS-Commercial-Calculator` main `56f508a7` (#228, merged 2026-11-22 07:58Z). Open PRs: 0. Pushed branches: 249 besides main, all 249 compared to main by `compare/main...<b>`: all `diverged`, none with ahead_by 0, as expected for squash-merged leftovers (smallest behind = 2). No branch carries unmerged work named by an actionable key.
- The local checkout (`2_Project_Files`) is on `b03/api` at 7f6ca4c0, NOT origin main, so every code read below is `gh api .../contents/<path>?ref=main`, never the local tree.
- Pricebook values: none entered here.

### In flight / landed
- No seat in flight on MPS (NEXT-PICKUP DELTA 1469 lists none; DELTA text names MPS only as part of the standing-order sweep). Last landings: #226 to #228 (2026-11-22). MPSCALC-272 held by Kam (card `datasec-mps-mpscalc272-tiles-1124` = a).
- Pickup greps: MPS lines of NEXT-PICKUP (top 110 lines read; `grep -n MPS`), daily 2026-11-25 (2 MPSCALC lines) and 2026-11-26 (0). No DROPPED line for any key proposed. HELD lines: 272 only. The words pack for the v13.4.1 lanes was a CANDIDATE decision in SWEEP-1630 (11-19): no later line shows it carded or ruled (UNMEASURED beyond the greps; Tuesday to confirm).
- Previous sweeps (11-24, 11-25) said 0 actionable. I differ on six keys: they carried the exclusions by unchanged `updated` stamp and did not re-read tickets whose rulings of 2026-11-11 (C-104 to C-130, "Accept all 29 recommendations") left work "queued, not built". I read each ticket's description and newest comment and the code at origin main.

### Actionable (6; every one built-and-open or ruled-and-unbuilt, verified at origin main 56f508a7)
| key (MPSCALC-) | title short | why actionable now | size | files (printed from main) | conflicts | lane |
|---|---|---|---|---|---|---|
| 233 | clone refuses a typed reference that already exists | C-119: owner ruled "Refuse". `Duplicate` at `QuoteEndpoints.cs:508-545` takes `req.QuoteRef` with no existing-reference check (only CopyRef for the blank case; Validate/InRange do not look it up). Use the existing 400 BAD_REQUEST, no new contract member; the refusal sentence rides the deploy words card | M | `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` (Duplicate), `QuoteStore.cs` (lookup by ref), `tests/MpsCalc.Api.Tests/QuoteApiTests.V0Duplicate.cs`, `docs/API.md:441`, `docs/api/openapi.json:369,1036`, `web/src/api/stub/stubApi.ts` (stub Duplicate mirrors the server per C-168) | stub file with 135 (L2); openapi/API.md with 316, 120, 195 | L1 |
| 316 | quoteRef unit in the contract schema | C-108 (a): the agreed sentence goes into the remaining places. Refusal sentence done (#218, `QuoteEndpoints.cs:1436`), API.md:441 and openapi.json:369 say the unit; `openapi.json:988` and `:1036` (`quoteRef` `maxLength 100`) carry no unit. Ticket label needs-ruling is settled by C-64 and C-108 | S | `docs/api/openapi.json` (988, 1036), regenerated `web/src/api/generated/**` via `web/scripts/sync-contract.mjs` | openapi.json with 233 | L1 |
| 120 | contract info.version rule in its own section | C-125 (a) "Yes, already the practice, written down". Main `API.md` mentions the bump only inside feature sections (lines 150, 547); no section of its own (grep of `minor bump`: 2 hits, both inside feature paragraphs) | S | `docs/API.md` | API.md with 233, 195 | L1 |
| 195 | engine-target sentence into the engine docs | C-108 (a): sentence accepted 11-11; Jira comment 2026-11-18 says seven clauses read met and the sentence placement is the work owed. Sentence text is in the B158 gate evidence, not on the ticket: the builder must read `Briefs/2026-10-16_B158_STATUS.md:233` first | S | `docs/ENGINE.md` (deal usage paragraph; the X-30 row at :157), `docs/API.md:588` ("a what-if only") | API.md with 233, 120 | L1 |
| 135 | smoke journey on the dev stub and no-API legs | Review of #178: clause 2 (fix those reds) and clause 4 (green in all four legs) NOT MET; stub leg red because calculate for a held rental quote still goes to the real API (C-149 work owed); spec left out of CI by name at `playwright.config.ts:11`. Current state of the stub leg after #193 and #201 is UNMEASURED: first step is a run | M | `web/e2e/smoke.spec.ts`, `web/playwright.config.ts`, `web/src/api/stub/stubApi.ts` | stubApi.ts with 233 (do L1 first) | L2 |
| 297 | exact-nav spec and Proposal locator green on all legs | Clause 1 met; the smoke leg is green on one leg only (API on synthetic data); releases with 135 | S | `web/e2e/smoke.spec.ts`, `web/e2e/b46-home.spec.ts` | after 135 | L2 |

### Lanes
- **L1, API refusal and contract docs (233, 316, 120, 195), value 1.** Owns: `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`, `QuoteStore.cs`, `tests/MpsCalc.Api.Tests/QuoteApiTests.V0Duplicate.cs`, `docs/API.md`, `docs/ENGINE.md`, `docs/api/openapi.json`, `web/src/api/generated/**`, and the Duplicate branch of `web/src/api/stub/stubApi.ts`. Must not touch `web/e2e/**`, `playwright.config.ts`, `web/src/feedback/**`, `scripts/**`, `infra/**`. Order 233, 316, 120, 195. One seat, Sonnet; 233 is number-free, no calculation register row. Nothing deploys, branch push only (CodeQL rule in the project CLAUDE.md).
- **L2, e2e smoke journey (135, 297), value 2.** Owns: `web/e2e/smoke.spec.ts`, `web/e2e/b46-home.spec.ts`, `web/playwright.config.ts`, and the stub calculate path in `web/src/api/stub/stubApi.ts`. Must not touch anything in L1's list. Run after L1 lands because both edit `stubApi.ts`. A first step with a measurement (four legs) is part of the kit. Sonnet.
- No L3 or L4: nothing else passed the screen.

### Excluded (160 of 166 are excluded or not actionable)

- **A epics (15)**: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15.
  Reason: epics, umbrella containers.
- **B spec-seed umbrellas (42)**: 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 58, 59, 60, 62, 63, 64, 65.
  Reason: seed tasks of 2026-09-30: large features or human-owned records; their built parts are tracked by the later tickets.
- **C question-for-kam (10)**: 69, 74, 75, 76, 78, 79, 80, 82, 83, 85.
  Reason: questions only the product owner answers.
- **D needs-ruling label (10)**: 129, 144, 153, 157, 159, 177, 188, 222, 226, 261.
  Reason: label needs-ruling; no later ruling found for these in CLARIFICATIONS.
- **E later phase (5)**: 149, 152, 154, 181, 260.
  Reason: label later-phase or phase-2.
- **F held by Kam (1)**: 272.
  Reason: HELD by Kam 2026-11-24 15:24 (card datasec-mps-mpscalc272-tiles-1124 = a, hold until MPSCALC-315 figures exist).
- **G owner approval of exact words, name or design first (18)**: 110, 121, 123, 130, 139, 156, 161, 169, 194, 258, 288, 315, 358, 368, 402, 407, 424, 425.
  Reason: owner ruled the direction (C-1xx) but the exact name, sentence, setting or design is his before any contract or word change; or the ticket itself says so; 110 is also stale (short form no longer one page).
- **H lane-v words, client data or contract names (28)**: 236, 237, 243, 244, 245, 246, 248, 251, 264, 265, 268, 269, 270, 271, 273, 274, 275, 276, 277, 279, 280, 281, 282, 283, 284, 285, 286, 287.
  Reason: v13.4.1 lane-v tickets: not under the HPSM HTML hold (Tuesday 11-11), but each needs new customer or staff words (the SWEEP-1630 words-pack candidate; no ruling found in NEXT-PICKUP), or client data (284, 285), or approval values and words (286, 287), or builds on an unlanded ticket (237 on 236); 251 clause 1 sign-in leg ruled out of CI; 278 built, 424/425 hold the rest.
- **I built, open: records reading, independent run or review, or machine load, no build (22)**: 57, 118, 124, 133, 140, 155, 158, 162, 163, 170, 173, 189, 200, 223, 278, 306, 310, 333, 359, 369, 427, 431.
  Reason: the code is on main; what remains is a coordinator reading, an independent review or load-above-7 runs (163, 333), a counts-only read of the local price store (140, 200: UNMEASURED), a pre-existing decision (310 seam, 306 owner question B354-5, 118 judged not built), data from the reviewer (155), the unlocated runbook (223), the seed identity (173 clause 1), or records-repo process (133).
- **J hosted, deploy, secret, device or external (7)**: 103, 187, 224, 372, 395, 419, 421.
  Reason: hosted check or restart (187), host image (224), expired secret (395), az what-if (419), repo alert setting (421), roll-forward rule (103; the ticket door is older code refusing stored snapshots).
- **K blocked or reading unconfirmed (2)**: 212, 360.
  Reason: 212 needs 286 and 287 first; 360 usageOnly reading unconfirmed, Tuesday 2026-11-19: a read-only analyst first, then a build.

Per-ticket notes the classes do not show:
- 11-11 actionable list status today: 96, 122, 98, 99, 217 are no longer open (Done, absent from the dump). 135 and 297 stay open and are actionable above. 251 (zero errors e2e: the sign-in leg ruled out of CI, clause 1 NOT MET by ruling), 57 (clauses read met on the coordinator's reading; move waits on that reading), 121 (e2e folder-drop step plus an open words question), 123 (the concurrent-upload bound is a setting: owner's call), 163 (needs 4 more counted runs started above load 7), 333 (clauses 1 to 3 need a fresh independent review), 130 (printed words differ from the mock: owner's call), 139 (axe dependency: coordinator decision) were each re-read and stay excluded.
- 161 archive and 156 rental credit box: ruled (C-115, C-114) but each adds a contract member or field and the standing ruling cited in C-116 holds every contract change until the owner approves the exact name; not building before a name card.
- 110 is stale: the short form is now the concise document (OnePager.tsx header), "always one page" no longer describes it; the design rule is the owner's.
- 189: its clause 5 docs sentence now reads present in `API.md:714` (case and accent spelling); records only.
- 200 and 140 need a counts-only read of the local price-book store (`2_Project_Files/.local/pricebooks/` exists); not read here: UNMEASURED.
- 223: the runbook it names is not in the code repo (the host line appears in briefs and evidence files only); location UNMEASURED, so not buildable as filed.
- 427 and 431: built (#228, #226); records only.

### Check, by program (union of the Actionable table and the Excluded classes against MPSCALC.tsv)

assigned 166, tsv rows 166, missing 0, extra 0, double-assigned 0 (class counts: A=15, B=42, C=10, D=10, E=5, F=1, G=18, H=28, I=22, K=2, J=7, A=6).


### UNMEASURED
- Whether the stub and no-API legs of the smoke journey are still red after #193 and #201 (no run made; read-only).
- The exact text of the engine-target sentence (195): in a gate record, not on the ticket.
- Whether the SWEEP-1630 words pack for the v13.4.1 lanes was ever carded or ruled (no line found in the pickup greps; Tuesday knows).
- Local price-book store counts for 140 and 200; the location of the runbook for 223.
- No hosted host, Azure, ssh or docker was touched.


## 4. Security Composer (Jira PCOMP)


Measured 2026-11-26 04:53:36 AEDT (from `date`). Read-only; Jira GET and `gh api -X GET` only.

### Census
- JQL `project = PCOMP AND ( statusCategory != Done )`: total 75, all Backlog (dump PCOMP.tsv, instrument jq.py). Same as the 11-25 sweep (75). Types: 4 Epic, rest Task/Bug; 19 carry label `held`.
- Of the 11-11 list (23, 123, 82, 77, 75, 15, 21, 26, 27): 82, 77, 15, 21, 26, 27 are now Done (read back by key, pcomp_old9.tsv, with PCOMP-130 Done). 23, 123, 75 are still open; 123 and 75 are excluded below.

### In flight / landed
- Origin main (datasecau/Datasec-Security-Composer) = d06508f8a692 (PR 133, 2026-11-24T00:42Z). Local checkout HEAD 0b2fca43 is 103 behind origin: NOT trusted; all file reads below are from origin main.
- Open PRs: 0. PR 85: merged (closed, merged=true, head 2a58dc5d, 2026-11-20T21:28Z; main commit 3638da61 on document-pdf.ts).
- content/release-demo/CONTENT_HASH starts 5db37614; content/release-draft/CONTENT_HASH starts 5679855b (main). KEY RULE: any deploy of a changed content release is REFUSED without Kam's own card (DRAFTER_RULES.md line 99; the ruling-day main value was 05070f1d, so main now differs from the demo's earlier release). Code landing is allowed.
- Pushed unmerged branches: 203 branch names on origin; the per-branch compare to main was UNMEASURED (too slow, stopped). Most are squash-merged leftovers; none has an open PR.

### Actionable (1)
| key | title short | state | why actionable now | size | files | conflicts | lane |
|---|---|---|---|---|---|---|---|
| PCOMP-23 | Policy PDF footer drops the manifest hash line with long names (policy PDF half) | Backlog | Change report half merged (#113, #120). Policy PDF half is not built on main: footer text is `${brand.company_name} ${brand.product_name} | ${model.title}\nmanifest ${hash}` (policy-document.ts:835) in a width "*" column with no line budget (document-pdf.ts:187-193). Fix shape and test target given in the ticket (budget plus a test at 250 + 200 characters); no hold or ruling found in the 11-25/11-26 dailies or pickup; PR 85 conflict gone | S to M | packages/renderers/src/document-pdf.ts (footer, line 187), packages/renderers/src/policy-document.ts (line 835), a renderer test; may reuse the change-report footer line breaker (change-report.ts) | none open; no content-release file touched | A |

Differs from the 11-23 and 11-25 sweeps (they called 23 built, #119/#120): the ticket's own comments (2026-11-03, 2026-11-10) say the policy PDF half is NOT done. UNMEASURED: that the defect still reproduces on main (static read only, no render run); whether Tuesday reads "Done" as needing the 18-cell residue (rows 450-453, not ruled). If Tuesday treats the residue as owner-ruling, this is 0 actionable, consistent with the earlier sweeps. It does not need a content-release deploy to land.

### Lanes
- Lane A (only lane), value 1: PCOMP-23 policy PDF footer budget. Owns document-pdf.ts, policy-document.ts footer line, one renderer test. Must not touch content/**, any CONTENT_HASH, packages/engine, apps/web. Opus or Sonnet with an independent gate (PDF layout; byte changes to customer PDFs). Branch only, no deploy.
- No lanes B, C, D: nothing else is buildable.

### Excluded (74)
- Epics (4): 1, 2, 3, 4. epics
- Held label (19): 19, 20, 68, 69, 70, 71, 72, 73, 76, 79, 84, 85, 86, 87, 88, 89, 90, 91, 92. label `held` in the dump (reviewer-round / Guided / owner-call / words holds)
- Waits on Kam (needs-kam) (2): 46, 94. 46 "warn, never block" confirmation; 94 Kam sends the reviewer questions himself
- Needs ruling or approved words (6): 11, 36, 65, 123, 128, 129. 123 a measurement left as the owner's choice, in the owner's seven calls, not ruled; 128 items 2 and 5 need approved words and a new operator command; 129 hint words need the owner; 11 contract change plus two new words; 65 optional ruling (a Note); 36 14 fields wait for a judgement reading of the template, stays open per pickup
- Held by comment or by Tuesday (no label) (2): 66, 75. 75 comment 2026-11-15 HELD: Guided hold stands, only item (b) End page is open; 66 HELD by Tuesday (engine edit, G1, deferral not read as lapsed; 11-23 sweep Q3, 11-25 sweep)
- Blocked / reviewer-round hold / content release (L1-L9 chain) (22): 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 47, 48, 49, 50, 51, 53, 54, 55, 56, 57, 58, 60. L1-L5 content-release lanes wait on the reviewer-round hold and Kam's release card (DRAFTER_RULES line 99 refuses a changed-release deploy; main release-demo is 5db37614); 38/39 words or reviewer-held; 44 ruled HOLD (card composer-pcomp44-refusal-words-or-hold-1101 a); 53/54 and 55-58, 60 stack on L1-L4; 42 on a migration/contract chain
- Device, SM tool, deploy, VM, environment, ops, guide (15): 5, 6, 7, 8, 9, 10, 13, 16, 18, 25, 28, 59, 61, 78, 93. 5/6/7 guide and ratification; 8 rebuild examples on the new release (content-release deploy, Kam); 10, 13, 16, 18, 25, 28 VM or laptop environment; 59/60-class SM device tests need an SM tool (59, 61); 78 release signing key at next deploy; 93 VM tar.gz check; 9 operator rollback (owner call)
- Built, records only (4): 12, 41, 52, 64. 12 built #119/#120 (close is coordinator's); 41 built #87; 52 TOC built (PR 84, 308b7aa6, policy-document-pdf/3 on main, comment 2026-11-20); 64 nothing to write

Check (program, union of actionable and excluded against PCOMP.tsv): tsv=75 assigned=75 missing=[] extra=[]; actionable 1 + excluded 74 = 75.

### Re-screen against the 11-24/11-25 sweeps (their exclusions)
- PCOMP-66 HELD: still HELD by Tuesday (engine edit, G1; ticket text says deferred, ruled by the coordinator); no new ruling found. PCOMP-36 open: unchanged. PCOMP-52: stale ticket, built on main (records close only). 75: hold comment stands. 123: needs the owner's choice. 128/129: words approval needed.

### UNMEASURED
- Per-branch compare of 203 origin branches to main; reproduction of PCOMP-23 on main; main's pickup lines for 23 read only by the targeted grep (no hit for HELD/DROPPED/ruling on any proposed key); no ticket descriptions read for the 59 excluded keys beyond the 11-23/11-25 sweeps and dump summaries (carried classes); 11-26 daily has no PCOMP lines.


---

## 5. Questions for Tuesday (each with a default)

1. **MPS: six actionable against the earlier sweeps' zero.** The 11-11 owner acceptances (C-104 to C-130) left 233, 316, 120, 195 queued-and-unbuilt, and 135/297 are open with unmet clauses. Default: accept the six; start L1 (233, 316, 120, 195) as a branch only, nothing deploys; 233's refusal rides the existing 400 code (no new contract member), its customer sentence belongs to the deploy words card, not this build.
2. **PCOMP-23 (policy PDF footer).** The earlier sweeps called it built from PRs 113/120, which fixed only the change report; the ticket's own comments say the policy half is not done and no ruling or hold was found. Default: treat as actionable, Opus builder plus an independent gate, branch only; it touches no `content/**` or `CONTENT_HASH`, but customer PDF bytes change, so no deploy.
3. **NexusAI carried keys.** About 49 of the 79 keys (most of lanes 3 and 4) are carried from the 11-24 tables without a re-read at `e789995a`. Default: launch only the keys read today first (lane 1: RD-893, RD-1009, RD-1010, RD-820; lane 4: RD-1044, RD-983, RD-1045, RD-1043; lane 3: RD-1038, RD-1015, RD-1016); every carried key goes through the builder's PRIOR WORK check before an edit.
4. **NexusAI keys excluded as "needs a ruling" by the sub-sweeper** (38 keys, listed in its section 6) include RD-763, RD-764, RD-768, RD-805, RD-1041, RD-1042 that older sweeps called buildable-judgement tickets. Default: keep excluded; if Tuesday wants a read-first seat, RD-763/764 are the cheapest to open.
5. **OXPd lane D (build/CI guards).** Several owed lines (23, 129 and the OXPD2-20 to 25 tickets) may be part-built by PRs 6 to 11 and 49; which clauses remain is UNMEASURED. Default: a drafter's PRIOR WORK table first; no seat before that.
6. **OXPd device runs.** Rows 3 and 4 (built, not run) need Kam's word (CLARIFICATIONS 1088, C-84) and owed 118 is tied to the test-button lane. Default: no card now; one card when the run is near, as the pickup says.
7. **Records.** After lanes A to D land, one OXPd records seat files the new owed lines and ticks 133, 143, 146, 126 and the others; OXPD2-8 to 19 (WP umbrella tickets) status is UNMEASURED. Default: one records kit, JIRA WRITE only if its stamp says so.

## 6. Method and disclosures

- Instruments: `jq.py` (mine, Python, Jira REST `search/jql` and `issue`, GET only, 0.25 s per page, credentials read in-process from each project's `4_Credentials/.env` and never printed); `gh api -X GET` under each project's own `GH_CONFIG_DIR`; `/usr/bin/grep`, awk and Python over decoded file text. Controls: every census equals its dump's row count; every classification assigned each key or owed line once, with the union check printed by program in each section (RD 911, OXPD2 59 and 100 owed lines, MPSCALC 166, PCOMP 75; missing 0, extra 0). The OXPd owed list numbering was checked 1 to 147 with no gap (awk).
- Writes: this file; scratch under `fleet/state/s328/sweep0446/` (helpers, dumps, section drafts, `ox/` helper scripts). No Jira write, no GitHub write, no card-store call, no mail, no `decision_queue.sh`, no hosted host contacted, no az, no ssh, no docker, no test run, no `cd`. Three Sonnet sub-sweepers (general-purpose agents) read under the same fences and wrote only their section file and scratch; their own UNMEASURED lists are in their sections. HPSM-POC board not read.
- Not run: no code of any project was built or tested, so every "buildable now" is a reading at origin main plus the ticket text, not a proof; the builder's PRIOR WORK check settles each.
- OXPd section: line pointers re-measured at `8757daa6`; the owed-list class counts are the sweeper's reading of each item's Where, Symptom and Why-deferred lines (items 33, 139, 147 were added to the records class after a truncated title hid their words).
- READ-WHOLE-BY-TUESDAY: ____
