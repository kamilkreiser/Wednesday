# SWEEP-1925: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-15 evening)

Written by a read-only sweeper from 19:29 to about 19:45 AEDT (clock: `date` read 19:38:39 AEDT during the sweep). Trigger: the product owner's 19:25 words, "keep going with the tickets". Form copied from SWEEP-0535 (05:35 today, 14 hours stale); its lane membership is re-measured below, not carried. Fences: DRAFTER_RULES.md (its `/Volumes/Laptop-DEV/` paths read as `/Volumes/Datasec_DEV/`). No Jira write, no git or GitHub write, no hosted HTTP, no `cd`, no token printed. Scratch (helpers, TSV dumps, trees, alert list) is in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s279/sweep1925/`.

## BLUF

Board census (instrument: SWEEP-0535's own GET-only `jqdump.py`, Jira REST `search/jql`, paginated by `nextPageToken` to `isLast`, JQL `project = <KEY> AND ( ... )` with parentheses). Control that can fail: open + Done must equal the project's full count by `created >= "2000-01-01"`, and it did in all four (146 + 347 = 493; 179 + 226 = 405; 80 + 48 = 128; 860 + 126 = 986).

| project | open now | open at SWEEP-0535 | buildable now | conditional | records-only (built, Jira still open) | lanes |
|---|---|---|---|---|---|---|
| HPSM-POC (HPSMPOC) | 146 (3 In Progress, 143 Backlog) | 134 | 3 tickets (482, 484, 470 points 3 and 4) | 4 (480, and drafts 162, 163, 91) | 3 (467, 420, 193) | 3 |
| MPS Commercial Calculator (MPSCALC) | 179 (all Backlog) | 186 | 27 | 2 (233, 123) | 0 found (222/103/226 are word-bound, see excluded) | 6 |
| Security Composer (PCOMP) | 80 (all Backlog) | 81 | 1 (128, item 2 only) | 2 (123, 23) | 4 (52, 74, 80, 81) | 1 (+1 conditional) |
| NexusAI (RD) | 860 (To Do 382, Testing 262, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2) | 856 | 24 read today, plus 81 carried from SWEEP-0535 lanes and re-checked only as "still To Do" | 2 (930, 931) | 0 measured today (the 32 of SWEEP-0535 are a records seat's) | 6 |

Reading the table: "buildable now" counts tickets I read today (Jira text plus source) and that carry no product-owner word, no HP SME content, no deploy, no production touch and no hold. NexusAI's 81 "carried" keys are the SWEEP-0535 lane S/B/F1/F2/T members that are still To Do, were not individually re-read except where named below, and are listed so a builder's PRIOR WORK check can take them; they are not in the 24.

Top 6 lanes to launch, ranked security and correctness first, then client-visible, then hygiene:

1. **NX-S1, NexusAI `backend/server.js` security slice** (RD-988 first, then 888, 926, 830, 711, then the server.js CodeQL set). RD-988 is a live hole: a signed-in viewer can still re-triage a feedback item (the 11-11 ruling made write routes administrator-only; PR #200 missed this one; gate measured 200). One seat owns `server.js`; Opus for the CodeQL and 711 slices, Sonnet for 988. 64 open code-scanning alerts on main, 29 of them in server.js (measured, section 4).
2. **NX-S2, NexusAI storage-family CodeQL** (RD-767, 768, 769, 806, 421, 766 non-server.js lines): file-system race, insecure temp file, remote property injection in `jsonStorage.js`, `emailService.js`, `costCentreMap.js`, `queryPreprocessor.js`. Opus (row C3), gate G1.
3. **M-O, MPS package and sdk guard** (MPSCALC-224 patched Xml assembly in the package, 349, 397, 398): a ruled security package change plus guard rows; nothing deploys. Sonnet build, G1 for 224 (a package that reaches a host).
4. **M-W2, MPS ruled web screens** (MPSCALC-229, 128, 150): three product-owner-accepted rulings on the proposal and price screens; removal or relocation only, no new word. The only MPS lane a client tester sees.
5. **NX-F1, NexusAI first-run, login and settings pages** (RD-456 re-saving the AI step turns AI back on, 492, 475/560 truncated SRI hash, 189, 117/188, 481, 808): correctness bugs on the page a fresh customer lands on.
6. **NX-T, NexusAI test pins and tooling** (RD-987, 985, 986, 983, 810, 820): six test-only changes, each red-first, file-disjoint from every live branch.

Next: MPS M-1 stub/e2e (404, 405, 135, 297), MPS M-3 engine/importer docs, MPS M-4 API docs (after b1578 lands), HPSM H-1 small API fixes (484, 482, 470.4), PCOMP PC-C (DEPLOY.md 0022 measurement).

HPSM-POC note: every HPSM change a UAT tester would see is already live or in review (b1577 industry list; lane P b1584 F9; lane N b1585 F10; lane R b1586 F11) or in the held HTML phase. What is left to build is hygiene (a log line, a flaky test, a cosmetic cut). That is a finding, not an omission.

## 0. What is live or in review (file sets that no lane below may touch)

Origin mains (`gh api -X GET repos/<repo>/commits/main`, each project's own `GH_CONFIG_DIR`): HPSM-POC `f32b209b` (2026-11-15 05:04Z), MPSCALC `56578ac6`, PCOMP `b4681297`, NexusAI `6335717d`. Open PRs: MPSCALC #196 (b1578), PCOMP #85 (draft, "HOLD K6", updated 2026-10-21, base `308b7aa6`), NexusAI #203 (b1568); HPSM-POC 0 (b1577 and b1586 are pushed branches, 1 ahead, 0 behind `f32b209b`). Control: the same call with `state=closed` returned today's merges (HPSM #317 to #319, MPS #192 to #195, PCOMP #129 and #130, NexusAI #200 to #202).

| branch | files (compare, printed) |
|---|---|
| HPSM b1577 `hpsmpoc-168-industry-choice` (41 files) | `api/src/HpsmPoc.Api/SeedContent/{playbook-placeholder.0.7.1.content.json, snapshot-policy-aligned.0.1.3.ruleset.json}`, `api/src/HpsmPoc.Modules.Assessment/{HostedDemo/HostedDemo.cs, Showcase/ShowcaseSeeder.cs}`, 12 test files under `api/tests/` (Content061/071, HostedDemoSeedRulesetTests, HostedDemoTests, ProvenanceViewTests, ReadinessApiTests, ShowcaseSeedDraftContentTests, UatLabelTests, AudienceSectionsTests, Content071Tests, ContentCatalogTests, ReadinessContentTests), `infra/{README.md, modules/appservice.bicep, tests/test_security_baseline.py}`, `web/e2e/{playbook-profile-fields.spec.ts, playbook.ts}`, `web/scripts/client-content.mjs`, `web/src/components/customer/{ApiProfile.test.tsx, profile-values.test.ts}`, `web/src/components/playbook/SnapshotLauncher.b56.test.tsx`, `web/src/content/**` (PROVENANCE.md, audiences/client-content/content-050..071/content/deck-v3 tests, client/ and packages/ and rulesets/ JSON, registry.ts), `web/src/lib/ruleset.ts` |
| HPSM b1586 lane R (11 files) | `api/src/HpsmPoc.Modules.Reporting/{Pdf/Layout.cs, Pdf/PdfPigReportRenderer.cs, README.md, Readiness/ReadinessReportModelBuilder.cs, Report/ReportModel.cs}`, `api/tests/HpsmPoc.Api.Tests/Assessment/ContentsHeadingNameCheckTests.cs`, three `Golden/*.outline.json`, `Pdf/ContentsPageTests.cs`, `Pdf/PdfReportGoldenTests.cs` |
| HPSM lane P b1584 (per the order; branch not yet pushed: `matching-refs/heads/b1584` returned nothing) | `web/src/components/snapshot`, `web/src/lib`, `ReportModelBuilder.cs` |
| HPSM lane N b1585 (not pushed: `matching-refs/heads/b1585` returned nothing) | `NarrativeReview.cs`, `ReportingEndpoints.cs`, `Entities.cs`, `AssessmentDbContext.cs`, migrations (the tree has `Persistence/Migrations/SqlServer` and `Sqlite`), `PersonalDataEndpoints.cs`, `infra/sql/api-identity.sql`, `ApiNarrative.tsx` |
| MPS b1578 `mps-170-fleet-line-id` (PR #196; 2 ahead, 1 behind main; 12 files) | `docs/API.md`, `docs/api/openapi.json`, `src/MpsCalc.Api/Contracts/Dtos.cs`, `Quotes/{PriceAudit.cs, Proposal.cs, QuoteEndpoints.cs, QuoteFileStore.cs}`, `tests/MpsCalc.Api.Tests/{FleetLineIdStoreTests.cs, FleetLineIdTests.cs}`, `web/src/api/generated/{SOURCE.txt, openapi.snapshot.json, schema.ts}` |
| NexusAI b1568 (PR #203; 6 ahead, 0 behind; 9 files) | `__tests__/{rd490-open-access-banner-browser.test.js, rd858-testing-page-no-custom-sql.test.js}`, `scripts/verify-expected-counts.json`, `static/css/{open-access-banner.css, testing-styles.css}`, `static/js/testing.js`, `static/testing.html`, `tests/e2e/{open-access-banner-concealments.js, open-access-banner-guard.js}` |

`scripts/verify-expected-counts.json` is touched by every NexusAI branch and rebuilt by Tuesday at landing (B1587 is rebuilding b1568's); no lane below owns it.

## 1. HPSM-POC (HPSMPOC)

Open 146 = 134 at SWEEP-0535 plus 12 new (HPSMPOC-482 to 493); none left the open set. Class arithmetic (program `classes.py`): 3 buildable + 4 conditional + 3 records-only + 15 excluded by the order's list + 2 needing a ruling = 27; the other 119 are SWEEP-0535's excluded classes carried unchanged (epics, the 21 HTML-phase items, messaging held for later, HP-tool or awaiting-HP, human or SOW, hosted or deploy, records closings). Control on the HTML-phase hold: the 21 HTML-phase keys returned 21 rows by `key in (...)`, and only 1 of them (HPSMPOC-392) has a Jira update after 2026-11-11 00:00; so the phase answer is still not on the board.

### Buildable now

| key | what | files (main `f32b209b`) | size | words / migration |
|---|---|---|---|---|
| HPSMPOC-484 | One start-up warning when `FollowUp:TrustedProxies` names a proxy and `ForwardedHeaders:Proof` is unset (the follow-up link silently stops believing X-Forwarded-For); plus a test row that reads the log line. The independent review of #318 named it as an optional Minor. | `api/src/HpsmPoc.Api/Program.cs:128-134` (the two existing warnings at :128-129 and :130-131, the gate at :134), `api/tests/HpsmPoc.Api.Tests/Hosting/ForwardedProofTests.cs` | S | An operator log line, not a customer word: builder copies :130-131's shape and swaps the section name; any other phrasing STOP. No migration. Program.cs is shared-risk with lane N if N registers services: check b1585's compare at pickup. |
| HPSMPOC-482 | Timing flake: `HostedDemoSlowFirstLoginTests.Only_a_first_login_that_timed_out_is_retried` failed once on the SQL Server shard (`HostedDemoRobustnessTests.cs:788`, called from :755, helper `OnSqlServerAsync` at :771). Ticket says: find the cause first; no bound is loosened and no number is proposed. | `api/tests/HpsmPoc.Api.Tests/Assessment/HostedDemoRobustnessTests.cs` (class at :522, test at :711) | M | No words, no migration. Must run on SQL Server as CI does. |
| HPSMPOC-470 (points 3 and 4 only) | (3) `startingOwner` cuts inside an emoji sequence: it walks code points (`for (const ch of trimmed)`), not grapheme clusters; (4) one SQL Server migration timeout seen once on the squash of PR 310: diagnose, add a test or record not reproducible. Point 1 is built (#319, records owed). Points 2 and 5 are layout calls and "not decided": out. | `web/src/components/customer/remediation-store.ts:56-66` and `remediation-store.test.ts`; point 4: `api/tests/` (UNMEASURED which file) | S | No words (cosmetic cut), no migration. |

### Conditional (not counted as buildable)

- **HPSMPOC-480** (one failed Kudu upload leaves a mixed site: `scripts/deploy-from-ci.sh:68` and `:69`, two `az webapp deploy` lines under `set -euo pipefail` at :25; stub test `infra/tests/test_deploy_package.py`). The ticket "asks for a remedy to be chosen" and names its own default (a). Today's note says 470 points 2 to 5 and 480 "stay as they are". Released only by Tuesday saying "default (a)".
- **HPSMPOC-91, 162, 163** (draft documents in the analysis repository, drafts only, nothing loaded or sent). 0535 listed them as lane H-4. Today's pickup and note carry 0 hits on any of the three. 162 and 163 say "for Kam; Steve and Paul review" and "DRAFT for HP vetting": they touch HP SME content, so the order's fence excludes them unless Tuesday rules drafts are fine; 91 (collateral packs) does not carry that wording. HPSMPOC-87 is excluded by the order's list; 241 likewise (B1583 is posting its HP comment).

### Records-only (built; a records seat's Jira comment, not a build)

HPSMPOC-467 and 420 (PR #317 merged 2026-11-14 20:34Z, six surfaces and one count wording; pickup says "467/420 commented, not moved"), HPSMPOC-193 (PR #318 merged 2026-11-15 02:14Z). 470 point 1 (PR #319). 467's seventh surface (Home pipeline table) is HTML-phase and stays out.

### Lanes (HPSM-POC)

- **H-1 API small fixes** (484, 482, 470.4): owns `api/src/HpsmPoc.Api/Program.cs`, `api/tests/HpsmPoc.Api.Tests/Hosting/ForwardedProofTests.cs`, `api/tests/HpsmPoc.Api.Tests/Assessment/HostedDemoRobustnessTests.cs`. Disjoint from b1577 (it touches `HostedDemoTests.cs`, not `HostedDemoRobustnessTests.cs`), lane R (Reporting) and lane N's named files. Sonnet, row C2 (line 92) for 484 with gate G2 (line 109); 482 and 470.4 are row L6-class test work (line 85), Sonnet, G2. Drafter rule 8: the `infra` job's repo-wide scans run in the gate whatever paths changed.
- **H-2 web cosmetic** (470.3): owns `web/src/components/customer/remediation-store.ts` and its test. Disjoint from b1577 (`ApiProfile.test.tsx`, `profile-values.test.ts` only in that folder) and lane P (`components/snapshot`, `web/src/lib`). Sonnet, G3 (line 110).
- **H-3 deploy script** (480, only if released): `scripts/deploy-from-ci.sh`, `infra/tests/test_deploy_package.py`. Sonnet, G2. Builds no deploy; touches no host.

Standing line for every kit: this phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only; nothing deploys.

### Excluded (HPSM-POC; this sweep's additions to SWEEP-0535's classes)

- In flight or just done today (the order's list): 168 (b1577), 490, 491, 492, 485, 487, 488, 489, 486, 493, 241, 476, 474, 392, 87.
- Needs a ruling: 483 (the hidden server-rendered script still carries a sample customer's stored name: "decide whether to keep it or stop sending it"), 469 (fifth record without "(sample)": keep, mark or remove undecided).
- 471 to 479, 481: messaging held for later or "gather" (0535 class, unchanged). 478 waits on an upstream release. 477 is a held text pass.
- SWEEP-0535's other classes (epics 10, HTML-phase 21, HP-tool or awaiting-HP, human/SOW 20, hosted or Azure 15, records closings 8, ruling-bound 9) are carried; none changed state on the board today (open set identical apart from the 12 new keys).

## 2. Security Composer (PCOMP)

Open 80, all Backlog (3 Bug, 4 Epic, 73 Task). PCOMP-82 left the open set (Done, PR #130). Main `b4681297`; PR #129 (PCOMP-128 items 3 and 4) merged 2026-11-15. The Guided hold (CLARIFICATIONS.md COMP-2 (a), line 1298) is Kam's: nothing under it is listed; PCOMP-75 is in the order's excluded list and today's note records lane B DROPPED twice (08:13 and 16:02).

**A correction to SWEEP-0535:** PCOMP-52 (policy PDF table of contents) is listed there as buildable, "L, unblocked". It is already built on main: `packages/renderers/src/document-pdf.ts:147-157` (`tocNodes`, "B323: the contents page"), `policy-document.ts:60` (`POLICY_PDF_TOC_TITLE = "Contents"`), `:55` (`policy-document-pdf/3`), and the test file `packages/renderers/test/b323-policy-pdf-toc.test.ts` (last commit `308b7aa6`, "B323 (L6-a): policy PDF contents page with matching page numbers (#84)", 2026-10-20). Done-when is probably met; a records seat should confirm clause by clause. No build.

### Buildable now (1)

| key | what | files | size | lane | model |
|---|---|---|---|---|---|
| PCOMP-128, item 2 only | The 0022 section's Route B bullet (`DEPLOY.md:354-360`) says "expected and not run ... **UNMEASURED for 0022**". Measure it the way B1569 measured 0023/0026/0027 (a throwaway database, one-step restore, ledger rows read back), then write what was measured. Items 3 and 4 are on main (#129); item 5 (the 0020 roll-forward line 169) needs approved wording: out; line 693 (planner line) is kept out by the ticket. | `DEPLOY.md` only | S to M | PC-C | Sonnet, row C2 (line 92); G3 (docs, line 110). Needs local docker for the throwaway database; no host, no deploy. |

### Conditional (2)

- **PCOMP-123** (size the footer by the real page count: `FOOTER_LABELS` at `packages/renderers/src/change-report.ts:535` per the ticket; needs the page count in `document-pdf.ts`) and **PCOMP-23** (policy-PDF half: manifest hash line lost with long names; `document-pdf.ts`, `pdf-fit.ts`). Both edit files that held draft PR #85 touches (`document-pdf.ts`, `pdf-fit.ts`, `document.ts`, `policy-document.ts`; #85 still open, `mergeable_state` clean, last updated 2026-10-21). Today's note says lane A waits on #85. Released only if Tuesday accepts that a later #85 rebase absorbs the conflict. Same lane, serial: 123 and 23 share `document-pdf.ts`. Opus (PDF layout), G2.

### Excluded (PCOMP)

- Order's list: PCOMP-75 (Guided hold, lane B DROPPED), PCOMP-82 (Done).
- Records-only: 52 (built, above), 74, 80, 81 (their ruling's leftovers were built by PR #125 per SWEEP-0535; not re-read today).
- All other classes carried from SWEEP-0535 unchanged (the open set is identical apart from 82): 4 epics; 19 `held`-label; 2 waiting on Kam (46, 94); 9 ruling or words (9, 13, 29, 38, 65, 11 and others); 24 blocked by held PR #85 (31 to 37, 39, 44, 45, 47 to 51, 53 to 58, 60, 66, 67); 15 not agent work; 2 stale (41, 42). Class arithmetic here: 8 classified today, 72 carried.
- No Composer lane has a migration or a new word in it.

## 3. MPS Commercial Calculator (MPSCALC)

Open 179, all Backlog (164 Task, 15 Epic). Left the open set since 0535 (Done, read from the board): 91, 202, 302, 324, 325, 334, 338, 340, 396, 399 (10 keys; control: the open-set difference by program, `comm`). New open: 402, 404, 405. Main `56578ac6`; PR #196 (b1578) open. Pricebook values are confidential: none appears here.

Today's landings (PRs merged): #192 (202, 222; the deploy refuses an older package once care-pack or staging rows exist), #193 (stub and comments: 334, 396, 399), #194 (400 to 403 follow-ups), #195 (57 clause 3). Product-owner words today: five cards ruled 13:47 to 13:48, among them fleetLineId (b1578), the roll-forward stop words (approved as written), and the round-cap card for 99 (waiting).

Path correction to SWEEP-0535 (which wrote `Api.csproj`): the file is `src/MpsCalc.Api/MpsCalc.Api.csproj` (tree line 58; `/usr/bin/grep` over the origin tree).

### Buildable now (27) by lane

**M-1 web stub and e2e** (404, 405, 135, 297, 111, 185, 139, 369, 121; 9). Owns `web/e2e/**`, `web/playwright.config.ts`, `web/src/api/stub/**`, `web/src/feedback/**` for 121. Disjoint from b1578 (its web files are `web/src/api/generated/*` only; if a stub row needs the new `fleetLineId` field, sequence after b1578 lands).
- 404: dev stub Duplicate does not apply create's checks against the caller (`web/src/api/stub/purchaseQuotes.ts:265-273`, `holdCopy`; row at `stubApi.test.ts:692` per ticket, unverified line). 405: no row pins the stub's update answer hiding hidden inputs from a caller without internal-metrics (`stubApi.ts:349`, verified).
- 135 and 297: `web/e2e/smoke.spec.ts:70-73` presses Short-form; the spec is left out of CI by name (`web/playwright.config.ts:11`) because it is red on the dev stub and the no-API legs (records note 2026-11-11 22:24). 251 (sign-in leg) is not listed: ruling status for the sign-in leg is cut off in the note I read: UNMEASURED.
- 111 (clause 4: the 390 px e2e green on the merged state, NOT MET only because nothing ran it), 185 (clause 2: dashboard half at 390 px), 139 (clause 4: axe; adds a dev dependency, no word; clause 5 is the product owner's and out), 369 (needs more counted whole-suite runs: 19 of 20 clean), 121 (the browser step with a folder drop only; the one words question stays out).
- Size M. Sonnet, row L6 (line 85) for test-only pins, G2 (line 109). No words, no migration.

**M-2 ruled web screens** (229, 128, 150; 3). Owns `web/src/screens/**` except `ProposalPage.tsx` and `web/src/proposal/template/sections.ts` (229). New e2e rows go in NEW spec files, never edits to M-1's. 
- 229: print a colour rate only for a device class with estimated colour pages (`web/src/proposal/template/sections.ts:204-206` `rateMethod`; `web/src/screens/bom/DealUsageResultView.tsx:56-58` colour rate cell).
- 128: keep "Software / month" in the breakdown row only (`web/src/screens/PriceViewColumns.tsx:123`); the summary card's copy is not located: UNMEASURED, builder greps.
- 150: deal-level usage tile at the top of the usage section (`web/src/screens/bom/DealUsage.tsx`, header comment :1-3).
- Size M. Sonnet, row C2 (line 92), G2. The product owner's 2026-11-11 14:34 rulings are the words authority; removal and relocation introduce no new customer word. No migration.

**M-3 engine and importer docs** (195, 78, 390, 200; 4). Owns `docs/ENGINE.md` (390: rows X-33 at :160 and X-46 at :173), `docs/IMPORTER.md` (200: coverage table at :112-134, counts only, no values), 195 (the accepted engine-target sentence only), 78 (remove the provisional marking in the places the ticket's comment 39419 names: places not re-read: UNMEASURED). Disjoint from b1578 (it edits `docs/API.md`). Sonnet, G3 (line 110). Developer-only text written from what the code does, per the product owner's 11-11 rule.

**M-4 API docs** (316, 364, 371, 189 clause 5 with 394, 120; 6 keys). Owns `docs/API.md` (and `docs/api/openapi.json` only if regenerated, never hand-edited, for 316). **Waits on PR #196 landing**: b1578 edits `docs/API.md` and `docs/api/openapi.json`. Sonnet, G3. 316's sentence is already agreed ("at most 100 characters, an emoji counts as two"); 364 and 371 are developer-only.

**M-5 package and sdk guard** (224, 349, 397, 398; 4). Owns `src/MpsCalc.Api/MpsCalc.Api.csproj` (the Pkcs pin and the ranking target at :23-39), `scripts/tests/test_sdk_pin.py` (`all_problems` at :303) and `scripts/tests/test_sdk_pin_routes.py`. Disjoint from b1578 (no csproj, no scripts). 
- 224: ship the patched Xml assembly inside the app package as the Pkcs one is (ruled: "Ship it in the package"). A package change; it reaches a host only with a deploy on its own approval, and this lane deploys nothing. Opus for 224 (row C3, line 93: a security package surface) with gate G1 (line 108); Sonnet for 349 (a comment example needing an SDK that carries the tie: UNMEASURED), 397 and 398 (G2).
- No words, no migration.

**163** (overlay Busy bound under 20 group runs under load: a measurement in tests; `tests/MpsCalc.Api.Tests/**`; owns no product file). Sonnet, row L6. Low value: put after M-1.

### Conditional (2)

- **MPSCALC-233** (clone whose typed reference exists is refused): ruled, but the refusal answer needs a line a user sees. Buildable only if an existing refusal sentence is reused; otherwise NEEDS-WORD. `src/MpsCalc.Api/Quotes/**` is also b1578's directory (`QuoteEndpoints.cs`, `QuoteFileStore.cs`): sequence after #196.
- **MPSCALC-123** (bound on concurrent feedback uploads; streaming half is built at `FeedbackEndpoints.cs:139`, `:153`): "a limit is a new setting" and the refused answer needs words unless the existing 503 is reused. NEEDS-WORD unless the builder reuses it.

### Excluded (MPSCALC), with the reason

- Order's list: 170 (PR #196), 57 (landed #195), 331 and 341 (records kit being drafted), 99 (round-cap card waiting on Kam; default hold unmerged until 09:00 Mon 16 Nov), 333, 207; 324, 302, 325, 338, 340 are Done (not in the open set).
- NEEDS-WORD (not buildable): **402** (the four items each change a word or path of the pack the product owner approved as written; today's pickup: "need Kam's word on wording"), **222, 103, 226** (the refusal half is on main from #192; what remains is the runbook line and stop words "pending the product owner", or a re-run of the door table), **130** (printed words per page still differ from the approved mock: needs the mock folder outside the repository and a words call).
- 223 (runbooks look in the wrong log): no file in the code repo found by `/usr/bin/grep` over the origin tree for "runbook"; it lives in the analysis repository: not a code lane, UNMEASURED.
- 158 (two follow-up tests; the last comment records "NO GO round 2 of 2" on its gate): not re-read today: carried excluded.
- SWEEP-0535 classes carried (contract-name or words tickets 161, 156, 169, 368, 194, 110, 277; records-only 173, 188, 85, 395; 10 ruling or words; 9 held or hosted; 2 blocked; 5 later phase; the 33 HTML-phase `lane-v*` items; 15 epics; 42 spec-seed umbrellas; 8 questions for Kam). Class arithmetic: 41 classified today, 138 carried.

## 4. NexusAI (RD)

Open 860: To Do 382, Testing 262, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 (sum 860; Bug 407, Task 378, Story 72, Epic 3). Left To Do since 0535: RD-576, 590 (PR #202), 958, 964, 965, 968 (PR #200, now Testing). New: RD-987 to 990 (all To Do). Testing and Release Ready (461) are not work. Main `6335717d`; PR #203 open (b1568: 532, 538, 858).

Code-scanning, measured: open alerts on `main` = **64** (`gh api -X GET repos/datasecau/Reporting_Dashboard_Au/code-scanning/alerts` with `state=open`, `ref=refs/heads/main`, `--paginate`; control: `state=fixed` returned 187 rows, which exceeds one 100-row page, so pagination fires). By file: `backend/server.js` 29, `jsonStorage.js` 6, `services/emailService.js` 5, `queryPreprocessor.js` 4, `static/js/settings.js` 2, `static/js/index.js` 2, `routes/entraProvisioning.js` 2, `marketplaceStore.js` 2, `incidents.js` 2, `tests/uat-run.js` 1 (the alert is at :43 now, not :30). Never dismiss; the check that can fail is main's analysis after the merge (drafter rule).

Landed in lane S since 0535: PR #200 (RD-958, 964, 965, 966 pinned, 968: write and setup routes administrators only, `requireAdminFor` 11 to 30), PR #201 (RD-932 audit rows for every refused request, reads included). Kam's 13:48 field-grant ruling: "Viewer keeps them" (card `nexusai-field-grant-holder-1115`, option a).

### Lane NX-S1: `backend/server.js` security slice (13 buildable + 2 conditional). One seat owns `server.js` at a time; slices in order.

| slice | keys | what and where (main `6335717d`) | size | model |
|---|---|---|---|---|
| 1 | RD-988 | A signed-in viewer can still POST `/api/feedback/:id/triage` (200; rewrites clarity status and triage notes). Extend the administrator check PR #200 put ahead of the feedback router: `feedbackItemWriteGate`, `backend/server.js:22098-22108` (`app.use('/api/feedback', feedbackItemWriteGate, feedbackRoutes)`), matched case-insensitively with one optional trailing slash as the existing check does. Cells: viewer 403 on each form, administrator unchanged, open window unchanged, stored triage fields untouched. Medium. | S | Sonnet, row C3 is for security DESIGN; this is a spelled-out extension of a gate that already passed review: Sonnet row C2 (line 92), gate G1 (line 108, security surface) |
| 2 | RD-888, 926, 830 | 888: same 1,000-row limit and a defined answer to a malformed limit on the Log Analytics path of the risk-run route (ruled 11-11; the parse line is not located: UNMEASURED). 926: raw model text in the log: today's main has `logger.info('...', cleanResponse)` at `:9213` and `...substring(0,100)` at `:6226`; the ticket's old lines (6068, 6169) have moved, so the builder re-greps (UNMEASURED that these two are the ticket's sites). 830: non-GUID `workspaceId` reaches `logsClient.queryWorkspace` at `:17103` and `:17284`. | M | Sonnet, G1 |
| 3 | RD-711, then the CodeQL server.js set: 762, 765, 766 (server.js lines only), 770, 772, 773 (763 and 764 are judgement tickets: read first) | 711: a SIGTERM during the 60 s interval flush tears `audit-buffer.json`: `flushAuditBufferToDisk` at `:372-377`, interval at `:22523`, the buffer at `:342`; serialise the interval and shutdown flushes. CodeQL alerts on server.js lines include 2953 to 3481 (user-controlled-bypass x10), 3476/8341/10442/11523/12214 (polynomial-redos), 6119 (incomplete-url-substring), 7811 (loop-bound), 11327 (incomplete-sanitization), 1613 to 2905 and 14428 (missing-rate-limiting x7), 1424/1442 (missing-token-validation). | L | Opus, row C3 (line 93), G1 |
| 4 (conditional) | RD-930, 931 | The permission core (row scope, field masking, answers and exports within scope), approved as proposed on 11-11; the field-grant question is now ruled. The 10:2x drafter note says "RD-930/931 wait on RD-929's build" (929 is the capability table merged in #197); whether that is satisfied is for the drafter to re-print. Large. | L | Opus, C3, G1 |

Words: none in slices 1 to 3 (refusals reuse the existing `Admin access required` body, per the RD-989 ticket text); migration: none. Slice 4 may add a masked-field marker: if it needs a user-facing word, NEEDS-WORD.

### Lane NX-S2: storage-family CodeQL (RD-767, 768, 769, 806, 421; 766's non-server.js lines)

Owns `backend/jsonStorage.js` (alerts at :263, :307 file-system-race; :2600 insecure-temp; :491 http-to-file; :4054, :4061 prototype and property injection), `backend/services/emailService.js` (:168, :387, :393), `backend/costCentreMap.js`, `backend/queryPreprocessor.js` (:155, :157, :167, :168 polynomial-redos), `backend/intentRouter.js`, `backend/marketplaceStore.js`, `backend/incidents.js`. 769, 806 and 766 also have alerts inside `server.js` (e.g. `:389`, `:15090`): those server.js lines go to NX-S1 after slice 3, never in parallel. 421 (`.machine-id` written outside the directory when `DATA_DIR` is unset). Size L; Opus (C3), G1. No words; no migration. Alert-to-ticket mapping for 805 (file-access-to-http x8) and 808 (`static/js/first-run-setup.js:383`) is by ticket title only: UNMEASURED per alert.

### Lane NX-F1: first-run, login, settings pages (17 To Do keys re-read today by title and newest comment; 9 named)

Owns `static/login.html`, `static/first-run-setup.html`, `static/js/{first-run-setup,settings,entra-provisioning-ui}.js`. Disjoint from b1568 (`open-access-banner.*`, `testing.*`). Named, all bug fixes with no ruling needed: RD-456 (re-saving the first-run AI step always sends `aiEnabled: true`, `static/js/first-run-setup.js:387`, so AI comes back on), 492 (`#enforce-auth-card` missing: success reads as an error; the page script sets its colours at :4129-4130), 475 and 560 (`static/login.html:10`: the Bootstrap Icons SRI hash is 40 characters, `sha384-l4UPAMHG...`), 189, 117 and 188 (CSP-blocked inline styles), 481 (trailing-slash pages load no assets), 808 (`first-run-setup.js:383` `.replace(/\/$/, '/')` replaces a slash with itself). The other 8 (176, 371, 373, 151, 416, 540, 687, 396) are listed in SWEEP-0535's F1; titles read today, bodies not. Sonnet, row C2 (line 92), G2 (line 109). Words: none intended; RD-151 (inline error text) and 416 ("configuration refusals return H...") may need words: builder STOPs if a sentence is new. The SRI fix needs the correct hash from the pinned `bootstrap-icons@1.10.0` package.

### Lane NX-T: test pins and tooling (6 read today: 987, 985, 986, 983, 810, 820)

- 987: add the cell that posts business hours to a seeded server and asserts the five stored agent preference values are byte-equal before and after (`__tests__/rd691-agent-settings-routes-retired.test.js`, or a small new file).
- 985: cells for `POST /api/settings/business-hours` with no body and an array body, each 400 and the settings file byte-identical (rd969's cell H1 is the model: `__tests__/rd969-three-routes-empty-request.test.js`).
- 986: `__tests__/rd436-r4-enforce-stamp-and-status.test.js:101`, `(dep.currentLog || '').slice(-800)` throws a TypeError because `currentLog` is a record `{ label, log }`; take the record's log text.
- 983: harness follow-ups from the RD-982 review (`LOG_LEVEL` for the child set to info in `bootServer`; the control cell waits about 2 minutes to fail). Shared harness file: not located in the tree by name (`bootServer` returned no path hit): UNMEASURED.
- 810: `tests/uat-run.js` js/file-access-to-http (alert 151, now at :43; fix, not dismiss; read first, the runner sending its own fixture is likely intended).
- 820: no cell guards `validateConditionWithAI`'s own AI-off gate (`aiGate.assertEnabled`). Not re-read today beyond the title.
- Size S each. Sonnet, row L6 (line 85), gate G2. Files are all under `__tests__/` and `tests/`, disjoint from b1568's `rd490`/`rd858` test files. No words, no migration.
- Carried from SWEEP-0535 lane T (36 more To Do keys, not re-read): 730, 749, 729, 757, 734, 345, 352, 355, 378, 379, 384, 134, 249, 353, 394, 397, 580, 586, 348, 668, 829, 918, 320, 387, 426, 539, 566, 572, 595, 597, 599, 600, 623, 726, 980, 947 (947 is documents-first).

### Lane NX-B: backend periphery without `server.js` (carried, 10 To Do keys, not re-read)

RD-804, 455, 805, 744, 745, 750, 824, 728, 577, 578 (826 is on the order's excluded list and stays out). 744, 745, 750, 824 are the erasure family: row C4 (line 94), Opus, "never in a Sonnet kit". 805: a local branch `942204d1` was red per the earlier note: UNMEASURED today.

### Lane NX-F2: dashboard, css, front-end tests (carried, 21 To Do minus b1568's 532, 538, 858 = 18 keys, not re-read)

144, 164, 175, 222, 349 (the grey-text contrast ruling), 220, 259, 261, 483, 613, 832, 835, 771, 861, 512, 513, 515, 145 (last; needs the Dockerfile, lane T's). Owns `static/index.html`, `static/js/{index,admin,chart-details}.js`, `static/css/**` EXCEPT `open-access-banner.css` and `testing-styles.css` (b1568's). Sonnet, G2.

### Conditional (2) and excluded (NexusAI)

- Conditional: RD-930, 931 (slice 4 above).
- Order's list: RD-932 (audit half landed #201; the rest is 930/931), 990 (the refused request's audit row path), 576, 590, 826 (#202 and the remaining item), 532, 538, 858 (PR #203), 966 (pinned by #200; the open-mode-closes-first-run question waits for the product owner), 989 (the front-end callers: a rule must be chosen, hide or disable or show the refusal in plain words: NEEDS-WORD).
- NEEDS-WORD or NEEDS-RULING (read today): RD-610, 612, 622 (erasure/wipe alarm; 622 is "the health page shows a plain status line": words; C4 Opus), 644 (a per-deployment also-notify setting: new setting), 433 (demo data marker plus a banner: banner words), 893 part 2 and 896 (the risk-level case rule has a card from 2026-10-27; ruling not confirmed today), 974 and 975 (the fixes are "a proposal, not decided"), 702 and 636 (truthful "encrypted at rest" wording drafted for the product owner first), 522 (names scrubbed from comments: serial, last, alone, touches every lane's files).
- Records-only: the 32 keys of SWEEP-0535 (merged PRs, Jira still open) are a records seat's job; today's merges add 958/964/965/968 (Testing), 932 partial, 576/590 (Testing); not recounted here.
- Not read today: 101 To Do second-tier keys of SWEEP-0535 (title only then), and Testing and Release Ready (461).
- Class arithmetic: 129 classified today (24 + 2 + 81 + 10 + 12); 731 carried (Testing and Release Ready 461, other To Do, In Progress 8, Put on Hold 7, Declined 2, SWEEP-0535's held and not-agent classes).

## 5. Disjointness check (by lane ownership, stated per lane above)

Within a project the lanes own disjoint paths: HPSM H-1 (`Program.cs`, two named test files), H-2 (`remediation-store.ts`), H-3 (`scripts/deploy-from-ci.sh`, `infra/tests/test_deploy_package.py`); MPS M-1 (`web/e2e`, stub, feedback), M-2 (`web/src/screens` minus ProposalPage, `sections.ts`), M-3 (`docs/ENGINE.md`, `IMPORTER.md`), M-4 (`docs/API.md`, after #196), M-5 (csproj, `scripts/tests/test_sdk_pin*.py`); PCOMP `DEPLOY.md` only; NexusAI NX-S1 (`server.js` and its new cells), NX-S2 (storage family), NX-F1 (login, first-run, settings pages), NX-F2 (dashboard and css minus b1568's), NX-T (`__tests__` and `tests` pins), NX-B (periphery). Exceptions stated in the lane text: `Program.cs` with lane N (check b1585 at pickup), `docs/API.md` with b1578 (M-4 waits), `QuoteEndpoints.cs`/`QuoteFileStore.cs` with b1578 (233 waits), NX-S2 against NX-S1 on 766, 769, 806 (server.js lines go after S1). No lane touches any file in section 0's table. I did not run a program over file sets; the claim rests on the named paths and is the builder's PRIOR WORK check to re-confirm against each branch's compare at pickup.

## 6. Questions for Tuesday (each with a default)

1. HPSMPOC-480: release to H-3 with default (a)? Default: yes, release; it is a script and its stub test, no host.
2. HPSMPOC-91, 162, 163 (draft documents): does the fence "no HP SME content" cover them? Default: 91 only (it carries no "for HP vetting" wording); 162 and 163 stay out.
3. PCOMP-123 and 23 against held PR #85: accept the rebase on #85's side? Default: no; leave them waiting; PCOMP-128 item 2 is the only Composer lane.
4. RD-930 and 931: has the field-grant ruling (13:48, "Viewer keeps them") released them? Default: yes, as slice 4 of NX-S1, with the drafter re-printing whether the capability table (#197) is the "RD-929 build" its note waits on.
5. MPSCALC-233 and 123: reuse an existing refusal line, or card the new words? Default: the builder reuses an existing line; if none fits, STOP and card.
6. MPS M-4 (API docs): wait for #196 to land? Default: wait; launch M-3 and M-5 first.
7. Records passes (not code): HPSM 467, 420, 193, 470.1; PCOMP 52 (built by #84, not 0535's "buildable"), 74, 80, 81; NexusAI the 32 of 0535. Default: one records seat per project after today's wave lands.

## Method and disclosures

- Instruments: `jqdump.py` and `jqget.py` from `fleet/state/s275/sweep/` (read by header only, run GET-only; credentials read in-process from each project's own `4_Credentials/.env`, never printed), plus three new GET-only helpers written here: `jdesc.py` (description and newest three comments), `ctx.py` (windows around a key in the first 200 lines of NEXT-PICKUP-TUESDAY.md and in today's daily note), `rg.sh` (one file at a time through `gh api -X GET repos/<repo>/contents/<path>` at `main`, then `grep -n` or a line range), `classes.py` and `lanes0535.py` (set arithmetic over the dumps), all in the scratch folder. `gh` ran only as `gh api -X GET` under each project's own `GH_CONFIG_DIR`. Origin trees (`git/trees/main?recursive=1`, `truncated=false` in all four) read 1537 (HPSM), 713 (MPS), 975 (PCOMP), 1016 (NexusAI) lines including the header line.
- Held and dropped check: for each key listed buildable or conditional I ran `ctx.py` against the pickup (first 200 lines) and today's note. Hits and what they said: HPSMPOC-482/483/484, 470, 480 (landed or records mentions only, nothing dropped); MPSCALC-404/405 (records created), 99 (waiting card), 402 (needs Kam's word, hence NEEDS-WORD); PCOMP-75 and 128; RD-988/987/989/990 (records-created, "HELD none"), RD-930 (narrowed to 932), RD-966 (stays open). Zero-hit keys are zero of this instrument; its positive control fired on 404 (3 hits), 99 (4 hits), 930 (3 hits), 966 (7 hits).
- Not measured: whether any pane currently holds a ticket here (no pane list read); b1584 and b1585 file sets are the order's, because neither branch is on origin yet; per-alert ticket mapping for NexusAI; the Jira text of every NexusAI carried key; any line number marked UNMEASURED above.
- Outside the one-output-file rule: the scratch folder above (helpers, TSV dumps, `ctx_*.txt`, `rd_alerts_open.tsv`, trees, `classes.py` output) and one moved file (`_quarantine_2026-11-15/lanes0535.sh`, a mistaken first draft of a helper, quarantined not deleted). No `decision_queue.sh`, no WEDNESDAY, FRIDAY, Secuura or non-Datasec tree read, no ledger file read.

READ-WHOLE-BY-TUESDAY: ____
