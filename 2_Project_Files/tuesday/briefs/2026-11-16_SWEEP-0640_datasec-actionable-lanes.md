# SWEEP-0640: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-16 morning)

Written by a read-only in-session sweeper from 06:42 to about 06:50 AEDT (`date` read 06:42:57 at start, 06:47:01 near the end). Trigger: the product owner's "keep going with the tickets" (06:2x), commission `2026-11-16_WAVE-0640_COMMISSION.md`. Template: `2026-11-15_SWEEP-1925_datasec-actionable-lanes.md`; its lane membership is re-measured below where this sweep says "read today", carried where it says "carried". Fences: DRAFTER_RULES.md (its `/Volumes/Laptop-DEV/` paths read as `/Volumes/Datasec_DEV/`). No Jira write, no git or GitHub write, no hosted HTTP, no `cd`, no token printed, no ledger file read, no `decision_queue.sh` call, no Artifact tool. Scratch (open-set dumps, `ctx2.py`, alert list, NexusAI tree) is in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s280/sweep0640/`.

## BLUF

Board census (instrument: SWEEP-0535's GET-only `jqdump.py` from `fleet/state/s275/sweep/`, Jira REST `search/jql`, paginated to `isLast`, JQL `project = <KEY> AND ( ... )`). Control that can fail: open (`statusCategory != Done`) + Done must equal the full count by `created >= "2000-01-01"`, and it did in all four (146 + 347 = 493; 177 + 228 = 405; 80 + 48 = 128; 860 + 126 = 986).

| project | open now | open at SWEEP-1925 | change | actionable keys (read today) | lanes |
|---|---|---|---|---|---|
| HPSM-POC (HPSMPOC) | 146 | 146 | none (set identical by `comm`) | 3 (484, 482, 470 points 3 and 4) | 3 |
| MPS Commercial Calculator (MPSCALC) | 177 | 179 | 331 and 341 Done (records seat, last night) | 13 | 4 |
| Security Composer (PCOMP) | 80 | 80 | none | 1 (128 item 2) | 1 |
| NexusAI (RD) | 860 | 860 | none (set identical by `comm`); counts by status identical (To Do 382, Testing 262, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2) | 21 | 4 |

Why the open sets did not move: every ticket whose change landed last night is waiting for its records pass (B1600 to B1602), so Jira still shows it open. They are excluded here (section 5). What is left to build is mostly hygiene, test pins, docs, CodeQL baseline and one measurement; nothing a client tester sees. That is a finding, not an omission.

Origin state (all `gh api -X GET`, each project's own `GH_CONFIG_DIR`): **0 open pull requests on HPSM-POC, MPS and NexusAI; Composer has only draft #85 (HOLD K6, untouched since 2026-10-21)**. No branch is in flight on any of the four (DELTA 1187: the only live seat was B1599 H171, and its PR #325 is merged on main, so no lane below collides with a pushed branch). Mains: HPSM-POC `678a1153` (2026-11-15T19:43Z, #325), MPS `5e800095` (#199), Composer `b4681297` (#130), NexusAI `d1152289` (#205). Control: the same `pulls` call with `state=closed` printed last night's merges (HPSM #318 to #325, MPS #192 to #199, Composer #125 to #130, NexusAI #198 to #205).

Lanes to launch, ranked security and correctness first, then the one measurement, then hygiene:

1. **NX-S1, NexusAI `backend/server.js` security slice** (RD-830, 711, 762, 770, 772, 773, plus the server.js lines of 765, 766, 769, 806). Opus, row C3 (model-routing.md line 93), gate G1 (line 108). 29 of the 63 open code-scanning alerts on main are in server.js.
2. **NX-S2, NexusAI storage-family CodeQL** (RD-767, 768, 421, plus the non-server.js lines of 765, 766, 769, 806). Opus, C3, G1.
3. **NX-P, NexusAI CodeQL periphery** (RD-805 minus emailService, RD-771). Opus, C3, G1.
4. **PC-C, Composer DEPLOY.md measurement** (PCOMP-128 item 2: measure 0022's Route B on a throwaway database). Sonnet, C2 (line 92), G3 (line 110).
5. **M-S, M-E, M-D, M-T** (MPS: stub pins, 390 px e2e measurement, developer docs, test stability). All Sonnet, G2 or G3.
6. **H-1, H-2, H-3** (HPSM: one start-up log line, one flaky test, one emoji cut). Sonnet, G2 or G3.
7. **NX-T, NexusAI test pins** (RD-987, 985, 986, 983, 820, 810). Sonnet, row L6 (line 85), G2 (line 109).

Model ids from `0_Brain/dashboard/data/models_latest.json` (checked 2026-11-16 06:00 +1100): Sonnet `claude-sonnet-5-5` (line 23), Opus `claude-opus-5-5` (line 17). Rows from `fleet/specs/model-routing.md`, lines printed today: L6 line 85, C2 line 92, C3 line 93, C4 line 94, G1 line 108, G2 line 109, G3 line 110.

Standing line for every HPSM kit: this phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only; nothing deploys.

## 1. HPSM-POC (HPSMPOC)

Open 146 = SWEEP-1925's 146, identical key set. Main `678a1153`; no open PR; the four feedback lanes (#321 to #324) and the ForwardedProof test fix (#325, touched only `api/tests/HpsmPoc.Api.Tests/Hosting/ForwardedProofTests.cs`) are on main. #324 changed 16 files; none is `Program.cs` (compare list printed), so SWEEP-1925's "Program.cs is shared-risk with lane N" is resolved.

### Buildable now (3)

| key | what | files (main `678a1153`, printed today) | size | words / migration |
|---|---|---|---|---|
| HPSMPOC-484 | One start-up warning when `FollowUp:TrustedProxies` names a proxy and `ForwardedHeaders:Proof` is unset (the follow-up link silently stops believing X-Forwarded-For; ticket says no effect today, the hosted list is empty). Still absent from `Program.cs`: lines 128-131 hold the two existing warnings, line 134 the gate. | `api/src/HpsmPoc.Api/Program.cs:128-134`, `api/tests/HpsmPoc.Api.Tests/Hosting/ForwardedProofTests.cs` | S | An operator log line, not a customer word: builder copies the shape at :130-131 and swaps the section name; any other phrasing STOP. No migration. |
| HPSMPOC-482 | Timing flake: `Only_a_first_login_that_timed_out_is_retried` failed once on the SQL Server shard (ticket: failed at `HostedDemoRobustnessTests.cs:788`, called from :755). Test is at :711, helper `OnSqlServerAsync` at :771 (printed today). Ticket says find the cause first, loosen no bound, propose no number. | `api/tests/HpsmPoc.Api.Tests/Assessment/HostedDemoRobustnessTests.cs` | M | No words, no migration. Must run on SQL Server as CI does. Not the ForwardedProof flake (that one was #325). |
| HPSMPOC-470, points 3 and 4 only | (3) `startingOwner` walks code points (`for (const ch of trimmed)`, `remediation-store.ts:61`, function at :56) and so cuts inside an emoji sequence; (4) one SQL Server migration timeout seen once: diagnose, add a test or record "not reproducible". Point 1 is built (#319). Points 2 and 5 are layout calls, "not decided": out. | point 3: `web/src/components/customer/remediation-store.ts` and its test; point 4: a NEW test file under `api/tests/` (the file is UNMEASURED) | S | No words (cosmetic cut), no migration. |

### Lanes (HPSM-POC)

- **H-1 start-up warning** (484): owns `api/src/HpsmPoc.Api/Program.cs`, `api/tests/HpsmPoc.Api.Tests/Hosting/ForwardedProofTests.cs`. Sonnet, row C2 (line 92), gate G2 (line 109). Drafter rule 8: the `infra` job's repo-wide scans run in the gate whatever paths changed.
- **H-2 SQL Server flake and migration timeout** (482, 470 point 4): owns `api/tests/HpsmPoc.Api.Tests/Assessment/HostedDemoRobustnessTests.cs` and one new test file for point 4. Sonnet, row L6 (line 85), G2. Diagnosis first; "not reproducible" is an allowed ending for point 4 and is a comment, not a build.
- **H-3 emoji cut** (470 point 3): owns `web/src/components/customer/remediation-store.ts` and `remediation-store.test.ts`. Sonnet, row C2, G3 (line 110).

### Excluded (HPSM-POC)

- Landed last night, records owed (B1600): the HPSM feedback-lane tickets of #321 to #325 and the ForwardedProof defect ticket (it cites #325); 485, 487 (descriptions still say "awaiting words"), 489 (does not quote the sentences), 486, 488, 490, 491, 492, 493 and 168 are in the records or hold lists of the pickup and are not re-listed.
- Held or awaiting the product owner: **HPSMPOC-480** (pickup line 337 and 342: "HPSMPOC-480/-481 await the product owner"; SWEEP-1925 listed it conditional on "default (a)", and that default was never given), **481**, 471 to 479 (messaging held or "gather"; 478 waits on an upstream release, 477 a held text pass), **483** and **469** (need a ruling).
- HTML phase (Kam and Paul decide): the 21 keys 368, 370, 390, 392, 393, 394, 396, 449 to 460, 463, 464 (read from SWEEP-1925's `hpsm_html_all.tsv`; none of 484, 482, 470 is in it, control 0 of 3).
- HP-tool integrations and the HPSM deploy round (the deploy card is Tuesday's, pending the product owner's word): carried classes, none touched.
- HPSMPOC-91, 162, 163 (draft documents in the analysis repository): zero hits in the pickup and both notes (control: 484 returned hits in the same read). They are documents, not code, and 162 and 163 say "DRAFT for HP vetting": out of this sweep.

## 2. Security Composer (PCOMP)

Open 80, all Backlog, identical key set. Main `b4681297`. Draft PR #85 (`b330/sm316-content-catalogue`, "HOLD K6") is `mergeable_state` clean, base `308b7aa6`, last updated 2026-10-21; its held state blocks the 24 keys carried from SWEEP-0535 (31 to 37, 39, 44, 45, 47 to 51, 53 to 58, 60, 66, 67). PCOMP-75 (Guided hold) is DROPPED (today's 11-15 note: lane B dropped twice).

### Buildable now (1)

| key | what | files | size | lane | model |
|---|---|---|---|---|---|
| PCOMP-128, item 2 only | `DEPLOY.md:360` still reads "**UNMEASURED for 0022.** Prefer Route A." (printed today at main; the lines before it, :355, call the 0022 `--clean` addition "expected and not run"). Measure it the way B1569 measured 0023, 0026 and 0027 (PR #129): a throwaway database, one-step restore, ledger rows read back; then write what was measured. Items 3 and 4 are on main (#129). Item 5 (the 0020 roll-forward line) needs approved wording: out. The planner line at :693 is kept out by the ticket. | `DEPLOY.md` only | S to M | PC-C | Sonnet, row C2 (line 92), G3 (line 110). Needs local docker for the throwaway database (seat, not a drafter); no host, no deploy. |

### Excluded (PCOMP)

- PCOMP-123 and 23 (both edit `document-pdf.ts` and `pdf-fit.ts`, which held PR #85 touches): blocked by the held PR; zero hits for 123 in the pickup or notes. PCOMP-52 is already built on main (PR #84, pickup line 126) and is a records matter; 74, 80, 81 are records-only per SWEEP-0535. 46 and 94 wait on the product owner; PCOMP-75 DROPPED.
- All other classes carried from SWEEP-0535 unchanged (open set identical): 4 epics, 19 `held`-label, 9 ruling or words, 15 not agent work, 2 stale (41, 42). No Composer lane has a migration or a new word in it.

## 3. MPS Commercial Calculator (MPSCALC)

Open 177 (SWEEP-1925: 179). Left the open set: MPSCALC-331 and MPSCALC-341 (Done, records seat last night; `comm` of the two key lists, no key is new). Main `5e800095`; no open PR. The `#196` (fleetLineId) landing that SWEEP-1925 told M-4 to wait for is on main (`58320ea0`), so the docs lane is released. Pricebook values are confidential: none appears here.

### Buildable now (13 keys, 4 lanes)

**M-S dev-stub pins** (404, 405). Owns `web/src/api/stub/**` only.
- 404: the stub's `holdCopy` (`web/src/api/stub/purchaseQuotes.ts:265`, header comment :259-263) copies a draft the server's Duplicate would refuse for a caller without internal-metrics (403 `INTERNAL_INPUT_FORBIDDEN`, `MANUAL_ITEM_FORBIDDEN`, `PRICE_EDIT_FORBIDDEN`, docs/API.md:436-439 per ticket); its rows at `stubApi.test.ts:690` onward use the Seller. Make the stub refuse as the server does; move the rows to the Pricing analyst; keep a Seller row for hidden inputs a Seller cannot send.
- 405: no row pins that the stub's answer to an update of a held rental quote hides hidden inputs (`stubApi.ts:349` calls `draftForCaller`, printed today); add the row, red when the answer is built from the stored draft.
- Size S to M. Sonnet, row L6 (line 85), G2. No words, no migration.

**M-E 390 px e2e measurement and axe** (111, 185, 139). Owns `web/e2e/**` (new spec files only), `web/playwright.config.ts`, `web/package.json` and its lock file (139 adds a dev dependency; `web/package.json` line 29 pins `@playwright/test` 1.63.0 and line 19 has the `e2e` script, printed today).
- 111 (Proposal page at 390 px) and 185 (quote screen and dashboard at 390 px): the fixes merged (PR #48 and PR #68 per the tickets' comments); the clauses read NOT MET only because the 390 px e2e has never run on the merged state. This lane runs it and records what it printed; if a screen is wider than 390 px the builder STOPs and reports, because the screen files (`web/src/screens/**`, `web/src/proposal/**`) are not owned here.
- 139 (info hints): clause 4 only, the axe check on the hints; adds a dev dependency, no word; clause 5 is the product owner's and out.
- Size M. Sonnet, row L6, G2. Disjoint from M-S (stub) and M-T (two test files).

**M-D developer docs** (390, 200, 371, 394 firm; 195 and 316 re-read first). Owns `docs/ENGINE.md`, `docs/IMPORTER.md`, `docs/API.md`, `docs/api/openapi.json` (the last only if regenerated by the project's own tool, never hand-edited). Serial inside one seat.
- 390: `ENGINE.md` rows X-33 (:160) and X-46 (:173), plus the test comment that points to a status record. 200: `IMPORTER.md` coverage table (:127 holds the "262" care rows), counts only, no values. 371: three template-store sentences in `docs/API.md` (developer-only; the product owner's 2026-11-11 ruling leaves developer-only docs out of his word review, and approves only a customer-visible sentence). 394: the source-version-id sentence in the validate paragraph (`API.md:704` says only "every source version id is unique"); the builder of #184 drafted one, quoted in the ticket.
- 195 and 316: the product owner accepted both on 2026-11-11 14:34 ("Accept all four. Each brings text into line with what the product does"). On main today `API.md:438` already carries "at most 100 UTF-16 code units (an emoji counts as two)" and the negative-input text at `API.md:83-87` already cites MPSCALC-105, so part of each ticket looks built (UNMEASURED which of 195's seven items remain: the builder re-reads each against main and may end with a records-only close).
- Size M. Sonnet, G3 (line 110) for the text, G2 if `openapi.json` is regenerated.

**M-T test stability** (369, 163). Owns `web/src/screens/bom/PurchaseBomEditor.test.tsx`, `web/src/screens/bom/PriceReason.test.tsx` (369) and the overlay concurrency test files under `tests/MpsCalc.Api.Tests/**` (163; file names UNMEASURED: the builder greps for the Busy-bound and burst tests). 369: more counted whole-suite runs (19 of 20 clean last time; the clause stays unmet until a loop above load 7 is counted). 163: tests only, a measurement under load. Sonnet, row L6, G2. Low value; launch after the others.

### Conditional, not counted

- MPSCALC-233 and 123 (clone refused when its typed reference exists; bound on concurrent feedback uploads): each needs a refusal sentence the user sees; buildable only if an existing refusal line is reused, else NEEDS-WORD. 233 is `lane-v0`, not HTML phase.

### Excluded (MPSCALC), with the reason

- Landed last night, records owed (B1601): 128, 229, 99, 397, 398 (Done by the Done rule), 349 (measured and confirmed), 150 (done as built), 224 (built, open for its host read, stale needs-ruling label), B1593 gate F1-F4, B1594 residue (fsevents, 17 e2e skips), B1596 round-3 Minors. 195 is NOT in that list, which is why it appears in M-D.
- HELD or card-bound (grep of pickup and both notes, each key): **135** (pickup line 889: "MPSCALC-135 held; lane (a) to ticket"), **364** (pickup line 2078: its card waits for a seat's local request), **189** (pickup lines 530 and 550: the U+212A/U+212B/U+0345 decisions are owed as a card), **121** (pickup line 612: in the `mpscalc-two-words-questions-1111` card), **130** (same card), **78** (label `question-for-kam`), **120** (a ruling: "rule it or retire the field's meaning"), **402** (needs the product owner's word on wording), 222, 103, 226 (stop words pending).
- HTML phase (Kam and Paul decide; labels `lane-v1` to `lane-v11`, 42 keys read from the open set today): includes 297 (`lane-v1`), 251 (`lane-v3`). `lane-v0` (6 keys: 369, 316, 288, 237, 236, 233) is not the HTML phase; 288, 237, 236 are ruling or words items and are not listed.
- 158 (last comment records "NO GO round 2 of 2" on its gate): carried excluded. 223 lives in the analysis repository, not a code lane. SWEEP-0535 classes carried: contract-name or words tickets, 15 epics, 42 spec-seed umbrellas, 8 questions for Kam.

## 4. NexusAI (RD)

Open 860, identical key set to SWEEP-1925. Main `d1152289`; no open PR. #204 (RD-988, 926, 888) and #205 (RD-456, 492, 808, 475, 560, 481) are landed and excluded; their tickets stay open for the records seat (B1602). Open code-scanning alerts on main = **63** (`gh api -X GET repos/datasecau/Reporting_Dashboard_Au/code-scanning/alerts` with `state=open`, `ref=refs/heads/main`, `--paginate`; 64 before #204 and #205; control: `state=fixed` returned 188 rows, more than one 100-row page, so pagination fires). By file: `backend/server.js` 29, `jsonStorage.js` 6, `services/emailService.js` 5, `queryPreprocessor.js` 4, `static/js/settings.js` 2, `static/js/index.js` 2, `routes/entraProvisioning.js` 2, `marketplaceStore.js` 2, `incidents.js` 2, and one each in `tests/uat-run.js`, `validators.js`, `ticketStore.js`, `services/entraGroupGate.js`, `mondayClient.js`, `marketplace-api.js`, `intentRouter.js`, `costCentreMap.js`, `azureLogAnalytics.js` (sum 63; list in `rd_alerts_open.tsv`). Never dismiss an alert; the check that can fail is main's analysis after the merge (drafter rule), not the PR head.

### Lane NX-S1: `backend/server.js` (one seat owns the file; Opus, row C3 line 93, gate G1 line 108)

Keys and where (main `d1152289`, printed today): **RD-830** (non-GUID `workspaceId` stored by the data-source writers and queried at `:17103` and `:17284`; ticket cites `lawWriteRefusal()` as the writer-side check; if the fix needs a file other than server.js, STOP and sequence after NX-S2); **RD-711** (SIGTERM during the 60 s interval audit flush tears `audit-buffer.json`: `flushAuditBufferToDisk` at `:372-377`, interval at `:22533`, shutdown flush at `:22536`; serialise the two); **RD-762** (js/missing-rate-limiting x7, alerts at 1613, 1620, 2879, 2895, 2900, 2905, 14428); **RD-770** (`apiEndpoint.includes('openai.com')`, ticket line :6049; alert js/incomplete-url-substring-sanitization at :6119); **RD-772** (js/incomplete-sanitization, alert :11327); **RD-773** (js/loop-bound-injection, alert :7811). Plus the server.js lines only of **765** (the email-regex alerts at 3476 and 8341 and others), **766** (polynomial-redos at 10442, 11523, 12214), **769** (remote-property-injection at :15090), **806** (http-to-file at :389). Those four tickets close only after NX-S2 has done their other files.
- Read first, not counted: RD-763 (missing-token-validation x2, alerts 1424 and 1442) and RD-764 (user-controlled-bypass x10, alerts 2953 to 3481 and 16663; login, OAuth and AI-skip guards): both are design judgements; the builder reads and STOPs if a choice is a product or security-design decision.
- Words: none intended; refusals reuse an existing answer; a new user-visible sentence is STOP. Migration: none.

### Lane NX-S2: storage family (Opus, C3, G1)

Owns `backend/jsonStorage.js` (alerts :263 and :307 file-system-race, :491 http-to-file, :2600 insecure-temp, :4054 and :4061 property injection), `backend/services/emailService.js` (:168, :387, :393), `backend/costCentreMap.js` (:72), `backend/queryPreprocessor.js` (:155, :157, :167, :168), `backend/intentRouter.js` (:90), `backend/ticketStore.js` (:63), `backend/validators.js` (:280), `backend/marketplaceStore.js` (:118, :146), `backend/incidents.js` (:91, :93). Keys: **RD-767** (file-system race, check-then-use on `costCentreMap.js:72` and the `.machine-id` writes), **RD-768** (insecure temporary files, `emailService.js:168` and the jsonStorage temp writes), **RD-421** (`.machine-id` written outside the directory when `DATA_DIR` is unset), plus the non-server.js lines of 765, 766, 769, 806 and the `emailService.js` lines of RD-805. UNMEASURED: which alert maps to which ticket beyond the ticket titles (the mapping above is by title and file only).

### Lane NX-P: CodeQL periphery (Opus, C3, G1)

Owns `backend/marketplace-api.js`, `backend/mondayClient.js`, `backend/routes/entraProvisioning.js`, `backend/services/entraGroupGate.js`, `backend/azureLogAnalytics.js`, `static/js/index.js`, `static/js/settings.js`. Keys: **RD-805** (js/file-access-to-http x8, medium: stored config sent to its own service; its `emailService.js` alerts go to NX-S2) and **RD-771** (js/incomplete-url-substring-sanitization, `IS_PRODUCTION` decided by `hostname.includes()`, alerts at `index.js:10`, `:11`, `settings.js:10`, `:11`). 805's alerts are "stored config sent to its own service": the builder reads each before changing anything; a likely intended behaviour is a finding to report, never a dismissal.

### Lane NX-T: test pins and tooling (Sonnet, row L6 line 85, gate G2 line 109)

Owns `__tests__/**` and `tests/uat-run.js`. Six keys read today:
- RD-987: a cell that posts business hours to a seeded server and asserts the five stored agent preference values are byte-equal (`__tests__/rd691-agent-settings-routes-retired.test.js` exists on main, or a small new file).
- RD-985: cells for `POST /api/settings/business-hours` with no body and an array body, each 400 and the settings file byte-identical (model: `__tests__/rd969-three-routes-empty-request.test.js`, exists on main).
- RD-986: `__tests__/rd436-r4-enforce-stamp-and-status.test.js:101` calls `.slice` on `dep.currentLog`, a record object (line printed today).
- RD-983: harness follow-ups; the harness is `__tests__/helpers/rd395-server-harness.js` (`bootServer` at :83, exported at :214; located today, SWEEP-1925 left it UNMEASURED).
- RD-820: no cell guards `validateConditionWithAI`'s own AI-off gate (`aiGate.assertEnabled`); title read today, body not.
- RD-810: js/file-access-to-http in `tests/uat-run.js` (alert at :43, printed today; the runner sends its own fixture, likely intended: read first, fix not dismiss).
- No words, no migration. Disjoint from every landed file (no open branch).
- Carried by title only (titles printed today, bodies not read, not counted): the SWEEP-0535 lane-T tail 730, 749, 729, 757, 734, 345, 352, 355, 378, 379, 384, 134, 249, 353, 394, 397, 580, 586, 348, 668, 829, 320, 387, 426, 539, 566, 572, 595, 597, 599, 600, 623, 726, 980. Some are scripts or JIRA.md, not `__tests__`: a builder's PRIOR WORK check decides each, and none goes into a lane before its body is read. RD-947 (Roles UI risk model) and RD-918 (Dockerfile base image) are left out.

### Conditional and excluded (NexusAI)

- Conditional, not counted: **RD-930 and 931** (Roles UI permission core). The field-grant ruling is in ("Viewer keeps them", 2026-11-15 13:48), but pickup line 807 still lists them HELD for rulings, and line 250 says they "wait on RD-929's build" with a first slice narrowed to RD-932; whether #197's capability table satisfies that is not re-read here. Opus, C3, G1, Large; Tuesday decides.
- Landed last night, records owed (B1602): RD-988, 926, 888, 456, 492, 808, 475, 560, 481 (Done rule), RD-189 (duplicate of RD-733), RD-117 and 188 (next NX-F1 slice, real-browser CSP check first; they will touch login and first-run files, never `index.js` or `settings.js` as far as measured, UNMEASURED), the rd452 "addition B" timing-flake ticket (gate B1598 F1), rd-721 needs an absolute href (gate B1595 F3), the coordinator-action route decision (RD-988's own text), stale comments rd465:164-166 and rd486:267, pointer :634 to :647.
- Held, ruling or words (pickup, notes and SWEEP-1925, carried): RD-989 (hide or disable or show the refusal), 610, 612, 622, 644, 433, 893 part 2, 896, 974, 975, 702, 636, 522, 966 (stays open for the product owner), 990, 932 (audit half landed, the rest is 930 and 931).
- Carried unchanged and not re-read (SWEEP-1925, still To Do): NX-B backend periphery 804, 455, 744, 745, 750, 824, 728, 577, 578 (744, 745, 750, 824 are the erasure family: row C4 line 94, Opus, never a Sonnet kit; 805 moved to NX-P); NX-F2 dashboard and css (144, 164, 175, 222, 349, 220, 259, 261, 483, 613, 832, 835, 861, 512, 513, 515, 145); NX-F1's remaining eight (176, 371, 373, 151, 416, 540, 687, 396). Not counted.
- Testing and Release Ready (461 keys) are not work.

## 5. Disjointness check (by lane ownership, stated per lane above)

Within each project the lanes own disjoint paths. HPSM: H-1 (`Program.cs`, `ForwardedProofTests.cs`), H-2 (`HostedDemoRobustnessTests.cs`, one new api test file), H-3 (`remediation-store.ts` and its test). MPS: M-S (`web/src/api/stub/**`), M-E (`web/e2e/**` new specs, `web/playwright.config.ts`, `web/package.json` and lock), M-D (`docs/ENGINE.md`, `IMPORTER.md`, `API.md`, `api/openapi.json`), M-T (two named `web/src/screens/bom` test files; overlay tests under `tests/MpsCalc.Api.Tests/**`). Composer: PC-C (`DEPLOY.md`). NexusAI: NX-S1 (`backend/server.js`), NX-S2 (the nine storage-family files), NX-P (five backend periphery files, `static/js/index.js`, `static/js/settings.js`), NX-T (`__tests__/**`, `tests/uat-run.js`).
Exceptions, stated in the lane text: NexusAI tickets 765, 766, 769, 806 and 805 span two lanes by file, so each lane works its own files and the ticket closes only when both have; RD-830 may need a file outside server.js, in which case it waits for NX-S2. No lane touches a file of any open PR (there is none outside Composer's held #85, whose files are `document-pdf.ts`, `pdf-fit.ts`, `document.ts`, `policy-document.ts`, none in PC-C). Records seats (B1600 to B1602) write the analysis or root records repositories and Jira, never a code path of these lanes. I did not run a program over file sets; the claim rests on the named paths and is each builder's PRIOR WORK check to re-confirm at pickup.

## 6. Questions for Tuesday (each with a default)

1. HPSMPOC-480 and 481: the pickup says they "await the product owner". Default: stay out (no H-3 deploy-script lane).
2. RD-930 and 931: has the 13:48 field-grant ruling released them? Default: no lane today; ask the NexusAI records seat to print whether #197's capability table is the "RD-929 build" the 10:2x note waits on.
3. MPS M-D: 195 and 316 look partly built on main. Default: launch M-D with them as "re-read first"; a records-only close is an acceptable ending.
4. NexusAI lane count: NX-S1, NX-S2 and NX-P are all Opus on a security surface and all queue behind the gate seat. Default: launch NX-S1 and NX-T first, NX-S2 next, NX-P last.
5. MPSCALC-233 and 123: reuse an existing refusal line, or card the new words? Default: neither is launched; card only if the product owner wants them.

## Method and disclosures

- Instruments: `jqdump.py` (GET-only, credentials read in-process from each project's own `4_Credentials/.env`, never printed; read by header) for the twelve board dumps, plus `jdesc.py`, `rg.sh` (one file at a time through `gh api -X GET repos/<repo>/contents/<path>` at `main`) from `fleet/state/s279/sweep1925/`, and one new GET-free helper written here, `ctx2.py` (whole pickup plus the 11-15 and 11-16 notes, per key, with hold or drop windows). `gh` ran only as `gh api -X GET`, each under its project's own `GH_CONFIG_DIR`. The NexusAI origin tree (`git/trees/main?recursive=1`) printed `truncated=false`, 1085 paths.
- Held and dropped check: ran `ctx2.py` over every candidate key before listing it. Hits and what they said: HPSMPOC-484 (records-created only), 482 and 470 (landing or records mentions only), 480 (awaits the product owner: moved to excluded); MPSCALC-135, 364, 189, 121, 130 (held or card-bound: moved to excluded), 404 and 405 (records-created only), 369, 123 (older mentions only); PCOMP-128 (landed items 3 and 4), PCOMP-75 (dropped); RD-930 and 931 (held, see above), RD-987 (records-created), RD-765 (older mention). Zero-hit keys are zero of this instrument: its positive controls fired on HPSMPOC-484 (3 hits), MPSCALC-404 (3), MPSCALC-402 (5), RD-930 (5).
- Not measured: whether any pane currently holds a ticket here (no pane list read; DELTA 1187 names none live after B1599); per-alert ticket mapping for NexusAI; the Jira bodies of the carried NexusAI keys; every line number marked UNMEASURED above. Line pointers were printed from `main` today by `rg.sh` or the API; those marked "ticket" are the ticket's own and not re-read.
- Outside the one-output-file rule: the scratch folder named at the top (open-set dumps for the four boards, `*_old.k` and `*_open.k` key lists, `ctx2.py`, `rd_alerts_open.tsv`, `tree_rd.txt`). No `decision_queue.sh`, no WEDNESDAY, FRIDAY, Secuura or non-Datasec tree read, no ledger file read.

READ-WHOLE-BY-TUESDAY: ____
