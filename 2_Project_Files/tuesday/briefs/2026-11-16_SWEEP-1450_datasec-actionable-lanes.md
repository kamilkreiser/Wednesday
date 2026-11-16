# SWEEP-1450: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-16 afternoon)

Written by a read-only sweep agent from 14:50 to about 15:00 AEDT (`date` read 14:50:55 at start and 14:54:23 near the end). Trigger: the product owner's "keep going with the records passes and backlog", commission section SWEEP-1450 in `2026-11-16_RECORDS-1450_COMMISSION.md`. Template: `2026-11-16_SWEEP-0640_datasec-actionable-lanes.md`; its lane membership is re-measured below where this sweep says "read today", carried where it says "carried". Fences: DRAFTER_RULES.md and point 7 of the commission (no push, no PR, no Jira write, no mail, no board, no `az`, no `cd`, no deploy, no token printed, no ledger read, no Artifact tool, no `decision_queue.sh`). Scratch (open-set dumps, alert list, `bc.sh`) is in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s282/sweep1450/`.

## BLUF

Board census. Counts are printed by `fleet/board_count.sh jira` (wrapper `bc.sh` reads each project's `.env` in-process), JQL `project = <KEY> AND ( ... )`. The same sets were dumped with a GET-only `jqdump.py` for the key lists. Control that can fail: open (`statusCategory != Done`) + Done must equal the count by `created >= "2000-01-01"`, and it did in all four (141 + 355 = 496; 171 + 235 = 406; 80 + 48 = 128; 862 + 127 = 989). `board_count.sh` printed the same open and total numbers as the dumps in all four.

| project | open now | open at SWEEP-0640 | change | actionable keys (read today) | lanes |
|---|---|---|---|---|---|
| HPSM-POC (HPSMPOC) | 141 | 146 | 485, 487 to 492 Done (records seat B1600); 495, 496 new | 4 (484, 496, 470 point 3, 495) | 3 |
| MPS Commercial Calculator (MPSCALC) | 171 | 177 | 99, 128, 150, 229, 349, 397, 398 Done (records seat B1601); 406 new | 14 | 5 |
| Security Composer (PCOMP) | 80 | 80 | none (set identical by `comm`) | 0 | 0 |
| NexusAI (RD) | 862 | 860 | 189 Done; 991, 992, 993 new | 16 | 3 |

What changed since the morning sweep, and why it matters:
- **Three of the morning's lanes were consumed.** NX-S1 landed as NexusAI #206 (merge `d83eab99`); PC-C (Composer) ran as B1604 and ended OUTCOME C (0022 Route B refuses as written; nothing edited; Composer card ruled a, "Find and test a corrected command; bring you the wording"; its measurement kit B1606 is drafted and unstamped, and the DEPLOY.md words then wait on the product owner); H-2 (HPSM) ran as B1605 and ended NO-BUILD (no branch, no commit).
- **Composer therefore has no actionable key.** That is a finding, not an omission.
- **What is left to build is mostly hygiene, test pins, docs, and the CodeQL tail in the storage and periphery files.** Nothing a client tester sees; no migration; no new word in any lane below.

Origin state (all `gh api -X GET`, each project's own `GH_CONFIG_DIR`): **0 open pull requests on HPSM-POC, MPS and NexusAI; Composer has only draft #85 (`b330/sm316-content-catalogue`, HOLD K6)**. Mains read today: HPSM-POC `678a1153` (#325, 2026-11-15T19:43Z), MPS `5e800095` (#199), Composer `b4681297` (#130), NexusAI `d83eab99` (#206, 2026-11-16T02:02Z). Control: the same `pulls` call with `state=closed` printed each project's latest merge (HPSM #325, MPS #199, Composer #130, NexusAI #206). No branch of any lane below exists.

Lanes to launch, ranked in the commission's order (HPSM-POC, MPS, Composer, NexusAI), and inside each project security and correctness first:

1. **H-1 start-up warning plus test guard** (484, 496), **H-3 emoji cut** (470 point 3), **H-4 two stale statements** (495). Sonnet, G2 or G3.
2. **M-S stub pins** (404, 405), **M-E 390 px measurement and axe** (111, 185, 139), **M-D developer docs** (390, 200, 371, 394, and 195, 316 re-read first), **M-G SDK pin guard wording** (406 items 1 and 2), **M-T test stability** (369, 163). Sonnet.
3. Composer: none.
4. **NX-S2 storage-family CodeQL** (765, 766, 767, 768, 769, 421), **NX-P periphery CodeQL** (805, 771, 804), **NX-T test pins** (987, 985, 986, 983, 991, 993, 810). NX-S2 and NX-P Opus (row C3, gate G1); NX-T Sonnet (row L6, gate G2).

Model ids from `0_Brain/dashboard/data/models_latest.json` (printed today): Sonnet `claude-sonnet-5-5` (line 23), Opus `claude-opus-5-5` (line 17). Rows from `fleet/specs/model-routing.md` (printed today by `awk NR==`): L6 line 85, C2 line 92, C3 line 93, C4 line 94, G1 line 108, G2 line 109, G3 line 110.

Standing line for every HPSM kit: this phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only; nothing deploys.

## 1. HPSM-POC (HPSMPOC)

Open 141. Left the open set since 0640: 485, 487, 488, 489, 490, 491, 492 (Done, records seat B1600, Jira dump `hpsm_done.tsv`). New: 495 and 496 (both `rec-2026-11-16`, Backlog). Main `678a1153`, no open PR.

### Buildable now (4 keys, 3 lanes)

| key | what | files (main `678a1153`, printed today by `rg.sh`) | size | words / migration |
|---|---|---|---|---|
| HPSMPOC-484 | One start-up warning when `FollowUp:TrustedProxies` names a proxy and `ForwardedHeaders:Proof` is unset. Still absent: `Program.cs:128-131` hold the two existing warnings, `:134` the gate; `grep` for `FollowUp:TrustedProxies` in `Program.cs` printed nothing (control: `ForwardedHeaders:Proof` printed `:39`). | `api/src/HpsmPoc.Api/Program.cs`, `api/tests/HpsmPoc.Api.Tests/Hosting/ForwardedProofTests.cs` | S | An operator log line, not a customer word: copy the shape at `:130-131`, swap the section name. Any other phrasing STOP. No migration. |
| HPSMPOC-496 | Optional hardening of the forwarded-proof forcing test: wrap its first request (`ForwardedProofTests.cs:178`, per the ticket) in the same 30 second wait the watch read uses (`ForwardedProofTests.cs:277`, printed today: `WaitAsync(TimeSpan.FromSeconds(30))`). The ticket says "do when the test server is next upgraded, or decline". | `api/tests/HpsmPoc.Api.Tests/Hosting/ForwardedProofTests.cs` | S | None. Same file as 484, so the same lane. |
| HPSMPOC-470, point 3 only | `startingOwner` walks code points (`for (const ch of trimmed)`, `remediation-store.ts:61`, function at `:56`, printed today) and so cuts inside an emoji sequence. Point 1 is built (#319); point 4 was H-2's and ended NO-BUILD (B1605); points 2 and 5 are layout calls, "not decided": out. | `web/src/components/customer/remediation-store.ts` and its test file | S | No words, no migration. |
| HPSMPOC-495 | Two statements now false: the Reporting README row ADR-R13 (`api/src/HpsmPoc.Modules.Reporting/README.md:76`, printed today) says the executive report's golden outlines are unchanged, and the comment at `web/src/components/snapshot/stamped-set.test.ts:17` (printed today) says Q-CS-01 is asked first. Comments and one clause only; no assertion changes. | `api/src/HpsmPoc.Modules.Reporting/README.md`, `web/src/components/snapshot/stamped-set.test.ts` | S | Developer text, not a customer word. No migration. |

### Lanes (HPSM-POC)

- **H-1 start-up warning and test guard** (484, 496): owns `api/src/HpsmPoc.Api/Program.cs`, `api/tests/HpsmPoc.Api.Tests/Hosting/ForwardedProofTests.cs`. Sonnet, row C2 (line 92), gate G2 (line 109). Drafter rule 8: the `infra` job's repo-wide scans run in the gate whatever paths changed. 496 is optional; a recorded "declined" is an allowed ending for it (see question 2).
- **H-3 emoji cut** (470 point 3): owns `web/src/components/customer/remediation-store.ts` and `remediation-store.test.ts`. Sonnet, row C2, gate G3 (line 110).
- **H-4 two stale statements** (495): owns `api/src/HpsmPoc.Modules.Reporting/README.md` and `web/src/components/snapshot/stamped-set.test.ts`. Sonnet, row L6 (line 85) for the comment, gate G3. The README clause must be re-read against the golden-outline files before it is reworded (the ticket's "moved by one page" is the ticket's, not measured here).

### Excluded (HPSM-POC), with the reason

- **HPSMPOC-482 and 470 point 4:** B1605 H172 ended NO-BUILD (STATUS-NOW: "Outcome: NO-BUILD. No branch, no commit, no push"). 482 sighting 1 reads "NOT A TEST DEFECT"; sighting 2 "NOT REPRODUCIBLE"; 470 point 4 "NOT REPRODUCIBLE without a plant". Their records and the `jira-comments.txt` post are in B1613's section, so they are not re-listed.
- **Landed or deployed, records owed (B1613):** the UAT deploy of `678a1153` (B1609), the B1610 backup-copy deletion, the B1605 verdict, the two user-guide tickets owed since 11-11.
- **Held or awaiting the product owner:** HPSMPOC-480 and 481 (pickup says they await the product owner; no ruling since), 471 to 479 (messaging held or "gather"), 483 and 469 (need a ruling), 494 (not in the open set today; read as closed or moved by the records seat, not re-opened here).
- **HTML phase (Kam and Paul decide):** the 21 keys 368, 370, 390, 392, 393, 394, 396, 449 to 460, 463, 464 carried from SWEEP-0640's read of `hpsm_html_all.tsv`; none of 484, 496, 470, 495 is among them (checked by key against that list).
- **HP-tool integrations** and **the HPSM deploy round** (UAT deploy is done; any further deploy is Tuesday's card): none touched.
- HPSMPOC-91, 162, 163 (draft documents in the analysis repository): not code, "DRAFT for HP vetting": out.

## 2. Security Composer (PCOMP)

Open 80, all Backlog, identical key set to 0640 (`comm` printed nothing either way). Main `b4681297`. Draft PR #85 stays held.

### Buildable now: 0

PCOMP-128 item 2 was the morning's only buildable key. It ran as B1604 C104 and ended **OUTCOME C**: Route B for 0022 refuses as written, nothing was edited (pickup, DELTA 1190 "UPDATE 09:0x"). The product owner ruled the card "Find and test a corrected command; bring you the wording". The corrected-command measurement kit B1606 is drafted and unstamped (`2026-11-16_B1606_SEAT-C105_composer-0022-route-b-corrected-command.md`, a measurement producing a word pack, no DEPLOY.md edit; the records commission says "in flight separately"). `DEPLOY.md:360` still reads "UNMEASURED for 0022. Prefer Route A." (printed today). Changing that sentence needs the product owner's words, so it is not actionable. Item 5 (the 0020 roll-forward line) needs approved wording: out.

### Excluded (PCOMP)

- PCOMP-123 and 23 (both edit `document-pdf.ts` and `pdf-fit.ts`, which held PR #85 touches): blocked by the held PR; the pickup reports 9 mentions of 23, none a release.
- The 24 keys carried from SWEEP-0535 (31 to 37, 39, 44, 45, 47 to 51, 53 to 58, 60, 66, 67): the content catalogue in held PR #85.
- **Composer's Guided hold:** PCOMP-75 stays DROPPED (11-15 note: lane B dropped twice). Held mark on the ticket since B1590.
- PCOMP-52 is already built on main (PR #84); 74, 80, 81 are records-only; 46 and 94 wait on the product owner; the Composer W5 hint words (B1612's ticket) go to the product owner.
- All other classes carried from SWEEP-0535 unchanged (open set identical): 4 epics, 19 `held`-label, 9 ruling or words, 15 not agent work, 2 stale (41, 42).

## 3. MPS Commercial Calculator (MPSCALC)

Open 171. Left the open set since 0640: 99, 128, 150, 229, 349, 397, 398 (Done, B1601 and its predecessors' records). New: 406 (`records-pass-1116`, Backlog; the four Minors of #199). Main `5e800095`, no open PR, so the `#196` fleetLineId docs lane stays released. Pricebook values are confidential: none appears here.

### Buildable now (14 keys, 5 lanes)

**M-S dev-stub pins** (404, 405). Owns `web/src/api/stub/**` only.
- 404: the stub's `holdCopy` (`web/src/api/stub/purchaseQuotes.ts:265`, printed today) copies a draft the server's Duplicate would refuse for a caller without internal-metrics; its rows sit in `stubApi.test.ts` (the ticket says `:692`; the file's matching comment at `:603` printed today). Make the stub refuse as the server does; move the rows to the Pricing analyst; keep a Seller row for hidden inputs a Seller cannot send.
- 405: no row pins that the stub's answer to an update of a held rental quote hides hidden inputs (`stubApi.ts:349` calls `draftForCaller`, printed today); add the row, red when the answer is built from the stored draft.
- Size S to M. Sonnet, row L6 (line 85), gate G2 (line 109). No words, no migration. Not in the held or card lists (404: records-created mention only; 405: zero hits, control 404 returned hits).

**M-E 390 px e2e measurement and axe** (111, 185, 139). Owns `web/e2e/**` (new spec files only), `web/playwright.config.ts`, `web/package.json` and its lock file (139 adds a dev dependency; `web/package.json:29` pins `@playwright/test` 1.63.0 and `:19` has the `e2e` script, both printed today).
- 111 and 185: the fixes are merged per the tickets; the clauses read NOT MET only because the 390 px e2e has never run on the merged state. The lane runs it and records what it printed. If a screen is wider than 390 px the builder STOPs and reports, because `web/src/screens/**` and `web/src/proposal/**` are not owned here.
- 139: clause 4 only (the axe check on the hints); clause 5 is the product owner's and out.
- Size M. Sonnet, row L6, gate G2.

**M-D developer docs** (390, 200, 371, 394 firm; 195 and 316 re-read first). Owns `docs/ENGINE.md`, `docs/IMPORTER.md`, `docs/API.md`, and `docs/api/openapi.json` only if the project's own tool regenerates it (never hand-edited). Serial inside one seat.
- 390: `ENGINE.md` rows X-33 (`:160`) and X-46 (`:173`), printed today. 200: `IMPORTER.md` coverage table (`:127` holds the 262 care rows, printed today), counts only, no values. 371: three template-store sentences in `docs/API.md`, developer-only. 394: the source-version-id sentence in the validate paragraph (`API.md:704`, printed today, says only "every source version id is unique").
- 195 and 316: the product owner accepted both on 2026-11-11 (carried from SWEEP-0640). `API.md:438` already carries "at most 100 UTF-16 code units (an emoji counts as two)" (printed today), so part of each ticket looks built; the builder re-reads each against main and may end with a records-only close.
- Size M. Sonnet, G3 for the text, G2 if `openapi.json` is regenerated.

**M-G SDK pin guard wording** (406 items 1 and 2). Owns `scripts/tests/test_sdk_pin.py` and `src/MpsCalc.Api/MpsCalc.Api.csproj` (comment lines only). Items from the ticket: reword the docstring at `test_sdk_pin.py:17-18` from "raise the Pkcs pin" to "raise the Pkcs or Xml pin"; extend the csproj comment at `:29` to tie the target `KeepPinnedXmlOutOfPackagePruning` (`:37`) to the Xml pin. Pointers are the ticket's, not re-read here (UNMEASURED today). Items 3 and 4 are "decide" items: the default is to name each choice in the docstring as accepted, with no strictness change (question 4). Size S. Sonnet, row C2, gate G3. The guard test rows must stay green (the ticket's acceptance names 13 and 51 rows, as the ticket says).

**M-T test stability** (369, 163). Owns `web/src/screens/bom/PurchaseBomEditor.test.tsx`, `web/src/screens/bom/PriceReason.test.tsx` (369) and the overlay concurrency test files under `tests/MpsCalc.Api.Tests/**` (163; file names UNMEASURED: the builder greps for the Busy-bound and burst tests). 369: more counted whole-suite runs; the clause stays unmet until a loop above load 7 is counted. 163: tests only, a measurement under load. Sonnet, row L6, gate G2. Low value; launch after the others.

### Conditional, not counted

- MPSCALC-233 and 123 (clone refused when its typed reference exists; bound on concurrent feedback uploads): each needs a refusal sentence the user sees; buildable only if an existing refusal line is reused, else NEEDS-WORD (question 5).

### Excluded (MPSCALC), with the reason

- **Landed, records owed (B1611):** the hosted showcase deploy of `5e800095` (B1607), the seed-secret renewal ticket, the templates-path setting ticket, MPS #196. Not re-listed.
- **Held or card-bound** (carried from 0640's read of the pickup and notes; re-checked today only for new hits, none found): 135, 364, 189, 121, 130, 78, 120, 402, 222, 103, 226.
- **HTML phase (Kam and Paul decide; labels `lane-v1` to `lane-v11`):** carried from 0640 (42 keys); `lane-v0` keys 369, 316, 233 are not the HTML phase and appear above; 288, 237, 236 are ruling or words items.
- 158 (last comment records "NO GO round 2 of 2" on its gate): excluded. 223 lives in the analysis repository. Contract-name or words tickets, epics, spec-seed umbrellas and questions for Kam: carried excluded.

## 4. NexusAI (RD)

Open 862. Left the open set: RD-189 (Done). New: RD-991, 992, 993 (`records-pass-1116`). Main `d83eab99`, no open PR.

Code-scanning on main at `d83eab99`: **47 open alerts** (was 63; `gh api -X GET repos/datasecau/Reporting_Dashboard_Au/code-scanning/alerts` with `state=open`, `ref=refs/heads/main`, `--paginate`; every row's `commit_sha` reads `d83eab99`). Controls: `state=fixed` returned 204 rows, more than one 100-row page, so pagination fires; the analyses list for `refs/heads/main` shows a CodeQL run on `d83eab99` at 2026-11-16T02:06Z with `results_count` 47. By file: `backend/server.js` 13 (was 29), `jsonStorage.js` 6, `services/emailService.js` 5, `queryPreprocessor.js` 4, `static/js/settings.js` 2, `static/js/index.js` 2, `routes/entraProvisioning.js` 2, `marketplaceStore.js` 2, `incidents.js` 2, and one each in `tests/uat-run.js`, `validators.js`, `ticketStore.js`, `services/entraGroupGate.js`, `mondayClient.js`, `marketplace-api.js`, `intentRouter.js`, `costCentreMap.js`, `azureLogAnalytics.js` (sum 47; list in `rd_alerts_open.tsv`). Never dismiss an alert.

What is left in `server.js` (13): `js/http-to-file-access` at `:390` (RD-806, which waits on the product owner's card), `js/missing-token-validation` at `:1440` and `:1458` (RD-763) and ten `js/user-controlled-bypass` rows (RD-764). 763 and 764 are design judgements: read first, never a kit. So **NX-S1 has no remaining lane**; its tickets (762, 770, 772, 773, 711, 830, and the server.js halves of 765, 766, 769) await B1614's records pass and the rule that a ticket moves only when main's alerts show it fixed. B1603's gate counted 16 alerts gone (63 to 47), matching today's read.

### Lane NX-S2: storage family (Opus, row C3 line 93, gate G1 line 108)

Owns `backend/jsonStorage.js` (alerts `:263`, `:307`, `:491`, `:2600`, `:4054`, `:4061`), `backend/services/emailService.js` (`:168`, `:387`, `:393`; the lines of 805 here go to this lane), `backend/costCentreMap.js` (`:72`), `backend/queryPreprocessor.js` (`:155`, `:157`, `:167`, `:168`), `backend/intentRouter.js` (`:90`), `backend/ticketStore.js` (`:63`), `backend/validators.js` (`:280`), `backend/marketplaceStore.js` (`:118`, `:146`). Keys, with the remaining part each (alert rows read today, mapping by ticket title and file only, UNMEASURED beyond that): **RD-765** (`ticketStore.js:63`; the server.js half landed), **RD-766** (`intentRouter.js:90`, `queryPreprocessor.js` four rows; the server.js sites landed), **RD-767** (`costCentreMap.js:72`, `jsonStorage.js:263` and `:307`), **RD-768** (`emailService.js:168` and the `jsonStorage.js` temp write now at `:2600`), **RD-769** (`jsonStorage.js:4061`, `marketplaceStore.js:118` and `:146`, `validators.js:280`; the column-mapping route landed), **RD-421** (`.machine-id` written outside the directory when `DATA_DIR` is unset). RD-806's `jsonStorage.js:491` and `emailService.js:168` lines are NOT in the lane (the card on its fix waits on the product owner). `incidents.js:91` and `:93` (RD-807, status Testing, alerts still open on main) are NOT claimed: question 3. Do not close a ticket whose alert is in another lane's file.

### Lane NX-P: CodeQL periphery (Opus, C3, G1)

Owns `backend/marketplace-api.js`, `backend/mondayClient.js`, `backend/routes/entraProvisioning.js`, `backend/services/entraGroupGate.js`, `backend/azureLogAnalytics.js`, `static/js/index.js`, `static/js/settings.js`. Keys: **RD-805** (js/file-access-to-http: `marketplace-api.js:511`, `mondayClient.js:36`, `entraProvisioning.js:613` and `:624`, `entraGroupGate.js:204`; its `emailService.js` rows go to NX-S2), **RD-771** (js/incomplete-url-substring-sanitization at `index.js:10`, `:11`, `settings.js:10`, `:11`), **RD-804** (`azureLogAnalytics.js:798`, same lines as the Testing ticket RD-761; added today: it is the one `To Do` ticket for that file). 805 and 804 are "stored config sent to its own service": the builder reads each alert before changing anything; an intended behaviour is a finding to report, never a dismissal.

### Lane NX-T: test pins and tooling (Sonnet, row L6 line 85, gate G2 line 109)

Owns `__tests__/**` and `tests/uat-run.js`. Seven keys read today:
- RD-987: a cell that posts business hours to a seeded server and asserts the five stored agent preference values are byte-equal (model `__tests__/rd691-agent-settings-routes-retired.test.js`, in the NexusAI tree listing of 0640).
- RD-985: cells for `POST /api/settings/business-hours` with no body and an array body, each 400 and the settings file byte-identical (model `__tests__/rd969-three-routes-empty-request.test.js`).
- RD-986: `__tests__/rd436-r4-enforce-stamp-and-status.test.js:101` calls `.slice` on `dep.currentLog` (line printed today: `(dep.currentLog || '').slice(-800)`).
- RD-983: harness follow-ups; `__tests__/helpers/rd395-server-harness.js:101` builds the child environment as `{ ...process.env }` (printed today), so an exported `LOG_LEVEL` reaches the child.
- **RD-991 (new):** the harness check in `__tests__/rd452-group-config-strict-callback.test.js` (the throw at `:418`, the cell `addition B: BOTH strict reads` at `:551`, both printed today) rejects an arm time equal to the answer time. Fix: accept equal, or order the two events with a counter; two new cells for the check.
- **RD-993 (new):** two stale test comments: `rd465-first-run-open-window.test.js:164-166` (printed today) and `rd486-ai-test-key-forwarding.test.js:267-268` (printed today; the body line passes `aiEnabled: true`). Comments or the test body only; the ticket says the choice between rewording and changing the body is the author's.
- RD-810: js/file-access-to-http in `tests/uat-run.js` (alert at `:43`; the ticket says `:30`; `:30` prints `timeout: 120000`). The runner sends its own fixture, likely intended: read first, fix not dismiss.
- No words, no migration. Serial inside one seat, because 983 and 991 edit shared test infrastructure.
- Carried by title only (not read, not counted): the 0535 lane-T tail (730, 749, 729, 757, 734, 345, 352, 355, 378, 379, 384, 134, 249, 353, 394, 397, 580, 586, 348, 668, 829, 320, 387, 426, 539, 566, 572, 595, 597, 599, 600, 623, 726, 980); a builder's PRIOR WORK check decides each.

### Conditional and excluded (NexusAI)

- **RD-820 (moved out of NX-T):** the ticket's own text says a direct-call cell "needs a seam": extracting `validateConditionWithAI` from `server.js` is "a product refactor of an AI path". Not a test pin; needs a product decision, so excluded (question 6).
- **RD-992:** the coordinator-action route decision; the product owner ruled "Keep its own check" and B1614 records the comment and move. Not a lane.
- **RD-806:** the audit-details size card waits on the product owner. Excluded, with `server.js:390` and the two other rows.
- **RD-763 and RD-764:** design judgements, not counted.
- **Landed #206, records owed (B1614):** RD-762, 765 (partly), 766 (partly), 769 (partly), 770, 772, 773, 711, 830; gate F2 and F4 tickets; the per-entry-kind details check ticket; the HISTORY.md and fence-dials BACKLOG note.
- **The NexusAI demo hold (C-224):** nothing deploys; no lane touches a deploy.
- **RD-930 and 931 (Roles UI permission core):** still HELD in the pickup for rulings and for the RD-929 build; the 11-15 field-grant ruling does not release them by itself (question 7).
- Held, ruling or words (carried): RD-989, 610, 612, 622, 644, 433, 893 part 2, 896, 974, 975, 702, 636, 522, 966, 990, 932.
- Carried unchanged and not re-read: NX-B backend periphery 455, 744, 745, 750, 824, 728, 577, 578 (744, 745, 750, 824 are the erasure family, row C4 line 94, Opus, never a Sonnet kit); NX-F2 dashboard and css (144, 164, 175, 222, 349, 220, 259, 261, 483, 613, 832, 835, 861, 512, 513, 515, 145); NX-F1's remaining eight (176, 371, 373, 151, 416, 540, 687, 396). RD-117 and 188 are the next first-run slice (real-browser CSP check first). Not counted.
- Testing and Release Ready are not work.

## 5. Disjointness check

Within each project the lanes own disjoint paths, stated per lane above. HPSM: H-1 (`Program.cs`, `ForwardedProofTests.cs`), H-3 (`remediation-store.ts` and its test), H-4 (Reporting README, `stamped-set.test.ts`). MPS: M-S (`web/src/api/stub/**`), M-E (`web/e2e/**`, `playwright.config.ts`, `web/package.json` and lock), M-D (`docs/ENGINE.md`, `IMPORTER.md`, `API.md`, `api/openapi.json`), M-G (`scripts/tests/test_sdk_pin.py`, the csproj comment), M-T (two `web/src/screens/bom` tests, overlay tests under `tests/MpsCalc.Api.Tests/**`). NexusAI: NX-S2 (eight storage-family files), NX-P (five backend periphery files plus `static/js/index.js` and `settings.js`), NX-T (`__tests__/**`, `tests/uat-run.js`). The only shared file between NexusAI lanes was `emailService.js`, which the sweep assigns to NX-S2 alone. Composer: no lane.

**Against the four records kits (B1611 to B1614):** each records seat writes only its own kit file, `.measured` sidecar and drafter report under `tuesday/briefs/` (the drafting stage), and then, as the seats, the project's records repositories and Jira (the MPS root records repository, the HPSM analysis repository, the Composer records, and NexusAI's records plus its Jira). Every lane above writes only code paths in the project's code repository. The paths named in the four sections of the commission (B1607 to B1610 STATUS files, `Briefs/`, EXPIRING-GRANTS.md, `jira-comments.txt`, HISTORY.md, BACKLOG) are all outside every lane's owned paths. Two edge cases: B1614's HISTORY.md and fence-dials BACKLOG note for NexusAI (its repository is not read here; if it is a file inside the code repository, it is still not under `__tests__/**`, `backend/` or `static/js/`), and B1611's "MPS #196 records" (records only). I did not run a program over file sets; the claim rests on the named paths and is each builder's PRIOR WORK check to re-confirm at pickup.

## 6. Questions for Tuesday (each with a default)

1. HPSM H-1: the ticket for 484 prescribes only a log line shaped like `Program.cs:130-131`. Default: Sonnet builds it from that shape; any other phrasing is a STOP.
2. HPSMPOC-496 is marked optional by its own ticket ("do when the test server is next upgraded, or decline"). Default: include it in H-1 (same file as 484, one seat); the seat may end it as "declined" with a one-line reason.
3. RD-807 (incidents.js, two prototype-polluting alerts still open on main at `:91` and `:93`) sits in status Testing, not To Do. Default: not claimed by any lane; ask the NexusAI records seat (B1614) whether its alerts read fixed, since they do not.
4. MPSCALC-406 items 3 and 4 ask to "decide". Default: M-G does only items 1 and 2 and records items 3 and 4 as "named in the docstring as accepted" with no strictness change; a stricter reader is not built.
5. MPSCALC-233 and 123: reuse an existing refusal line, or card the new words? Default: neither is launched; card only if the product owner wants them.
6. RD-820 needs a seam in `server.js` (extract `validateConditionWithAI`). Default: excluded from every lane; ask the product owner only if he wants that refactor.
7. RD-930 and 931: has the 11-15 field-grant ruling released them? Default: no lane today.
8. Lane order for NexusAI: NX-S2 and NX-P are both Opus on a security surface and queue behind the gate seat. Default: launch NX-T first (Sonnet, G2), then NX-S2, then NX-P last.

## Method and disclosures

- Instruments: `jqdump.py` (GET-only, credentials read in-process from each project's own `4_Credentials/.env`, never printed) for the twelve board dumps; `board_count.sh jira` through the wrapper `bc.sh` for the eight counts (its `TOTAL=` lines printed no truncation refusal, limit 5001); `jdesc.py` (GET-only) for ticket bodies of 495, 496, 484, 406, 991, 993, 820, 983; `rg.sh` (one file at a time through `gh api -X GET repos/<repo>/contents/<path>` at `main`) for every `file:line` marked "printed today"; `ctx2.py` (whole pickup plus the 11-15 and 11-16 notes, per key) for the held and dropped check. `gh` ran only as `gh api -X GET`, each under its project's own `GH_CONFIG_DIR`. Scripts were copied from earlier sweeps' scratch folders into this sweep's scratch folder; `bc.sh` is new.
- Held and dropped check: ran `ctx2.py` over every candidate key before listing it. Hits: HPSMPOC-484 (records-created only), 482 and 470 (records and landing mentions; 482 and 470 point 4 closed by B1605 NO-BUILD), 480 (awaits the product owner); MPSCALC-404 (records-created only), 405, 111, 185, 139, 200, 371, 394, 195, 316, 163 (zero hits; positive control 404 and 406 returned hits); 369 (older mentions only); 390 (pickup line 517, an old "waiting for B1527" line, whether B1527 has landed is UNMEASURED here; both tickets are still open and their lines print on main today); RD-765 (older mention), RD-771 (older staged-kit mention), RD-805 (older mentions), RD-987 (records-created only), RD-985, 986, 983, 810, 991, 993 (older or records-created mentions only), RD-806 (card waiting on the product owner); PCOMP-128 (landed items and OUTCOME C). Zero-hit keys are zero of this instrument; its controls fired on HPSMPOC-484 (3), MPSCALC-404 (3), MPSCALC-406 (2), RD-806 (9).
- Not measured: whether any pane currently holds a ticket here (no pane list read; the pickup's DELTA 1191 names no live code seat); the per-alert-to-ticket mapping for NexusAI beyond ticket titles; the Jira bodies of carried NexusAI and MPS keys not named in a "read today" line; `web/e2e/**` file names; the `test_sdk_pin.py` and csproj line numbers of 406 (the ticket's own); the number of test files each M-T and NX-T key touches. The 21-key HPSM HTML list and the 42-key MPS HTML list are carried from earlier sweeps, not re-read.
- Outside the one-output-file rule: the scratch folder named at the top (`*_open.tsv`, `*_done.tsv`, `*_total.tsv`, `*_open.k`, `*_old.k`, `rd_alerts_open.tsv`, `bc.sh` and the copied scripts). No `decision_queue.sh`, no WEDNESDAY, FRIDAY, Secuura or non-Datasec tree read, no ledger file read. Two reads of the pickup, the 11-15 and 11-16 notes were by `sed -n` and Python slices over the tracked files (the notes and pickup are in the allowed read set).

READ-WHOLE-BY-TUESDAY: ____
