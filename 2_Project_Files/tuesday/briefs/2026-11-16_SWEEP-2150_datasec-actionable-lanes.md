# SWEEP-2150: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-16 night)

Written by a read-only sweep agent from 21:48 to about 21:55 AEDT (`date` read 21:48:11 at start and 21:51:56 near the end). Trigger: section SWEEP-2150 of `2026-11-16_RECORDS-1450_COMMISSION.md`, after records wave 3. Template: `2026-11-16_SWEEP-1450_datasec-actionable-lanes.md`; every lane membership below is re-measured today (open sets dumped and compared to SWEEP-1450's by `comm`; nothing carried from it except where a line says "carried"). Fences: DRAFTER_RULES.md and point 7 of the commission (no push, no PR, no Jira write, no mail, no board, no `az`, no `cd`, no deploy, no token printed, no ledger read, no Artifact tool, no `decision_queue.sh list`; one `decision_queue.sh show <exact id>`). Scratch (open and Done dumps, alert list, copied scripts) is in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s284/sweep2150/`.

## BLUF

**8 lanes, 10 buildable keys, 4 projects read.** HPSM-POC 2 lanes, Composer 0, MPS 3, NexusAI 3. Every lane is small (a test row, a docs sentence pair, a harness fix) except NX-A (RD-994, the audit-entry field checks), which is a real build on a security surface. Nothing a client tester sees; no migration; no new customer word in any lane. NexusAI's three lanes all write the counts file and the jest lock, so they run one at a time and after NX-S2 and NX-P (section 4).

Board census. Counts are printed by `fleet/board_count.sh jira` through the wrapper `bc.sh` (credentials read in-process from each project's own `.env`, never printed), JQL `project = <KEY> AND ( ... )`. The same sets were dumped with a GET-only `jqdump.py`. Control that can fail: open (`statusCategory != Done`) plus Done must equal the count by `created >= "2000-01-01"`, and it did in all four (148 + 358 = 506; 169 + 240 = 409; 81 + 48 = 129; 866 + 128 = 994). Every `board_count.sh` line printed `limit was 5001, so this is a real count and not a cap`; the dumps returned the same open numbers (148, 169, 81, 866) with unique keys equal to rows.

| project | open now | open at SWEEP-1450 | change | buildable keys (read today) | lanes |
|---|---|---|---|---|---|
| HPSM-POC (HPSMPOC) | 148 | 141 | 484, 495, 496 Done; 497 to 506 new (10) | 2 (504, 505) | 2 (H-5, H-6) |
| Security Composer (PCOMP) | 81 | 80 | 129 new (words, Minor); no key left | 0 | 0 |
| MPS Commercial Calculator (MPSCALC) | 169 | 171 | 185, 394, 404, 405, 406 Done; 407, 408, 409 new | 3 (407 items 1 and 2, 408, 409) | 3 (M-F, M-S2, M-E2) |
| NexusAI (RD) | 866 | 862 | 992 Done; 994 to 998 new | 5 (998, 985 residual, 996, 995, 994) | 3 (NX-T2, NX-R, NX-A) |

| lane | project | keys | owns (code repository paths) | model row, gate | size |
|---|---|---|---|---|---|
| H-5 | HPSM-POC | HPSMPOC-505 | `web/src/components/customer/remediation-store.test.ts` | Sonnet, L6 (line 85), G2 (line 109) | S |
| H-6 | HPSM-POC | HPSMPOC-504 | `api/src/HpsmPoc.Modules.Reporting/README.md` | Sonnet, L6, G3 (line 110) | S |
| M-F | MPS | MPSCALC-407 items 1, 2 | `tests/MpsCalc.Api.Tests/FleetLineIdTests.cs` (new rows only) | Sonnet, L6, G2 | S |
| M-S2 | MPS | MPSCALC-408 | `web/src/api/stub/purchaseQuotes.ts`, `web/src/api/stub/stubApi.test.ts` | Sonnet, C2 (line 92), G2 | S to M |
| M-E2 | MPS | MPSCALC-409 | `web/e2e/dashboard-390.spec.ts` | Sonnet, L6, G2 | S |
| NX-T2 | NexusAI | RD-998, RD-985 (residual cell), RD-996 | four existing test files (listed in section 4), `scripts/verify-expected-counts.json` | Sonnet, L6, G2 | M |
| NX-R | NexusAI | RD-995 | `docs/ROLE-CAPABILITIES.md`, `backend/services/capabilities.js` (one list entry), generated files named by the project's own command | Sonnet, C2, G1 (default; question 6) | S |
| NX-A | NexusAI | RD-994 | `backend/server.js` (auditLog call sites only), one new test file, counts file | Opus, C3 (line 93), G1 (line 108) | L |

Model ids from `0_Brain/dashboard/data/models_latest.json` (printed today): Sonnet `claude-sonnet-5-5` (line 23), Opus `claude-opus-5-5` (line 17). Rows from `fleet/specs/model-routing.md` (printed today by `awk NR==`): L6 line 85, C2 line 92, C3 line 93, G1 line 108, G2 line 109, G3 line 110. Ports: none requested by any lane except M-E2, which starts the Playwright stub web server (its gate B1635 printed port 9973 free after each run; the block is the drafter's to take from the fleet port rule, UNMEASURED here). NexusAI test lanes use the slot rule in their kit (`__tests__/helpers/test-server.js:89-93`), not a port named here.

Standing line for every HPSM kit: this phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only; nothing deploys.

Origin state (all `gh api -X GET`, each project's own `GH_CONFIG_DIR`). Mains read today: HPSM-POC code `a816fd00` (#328, merged 2026-11-16T08:35:10Z), MPS `56bfe232` (#205, 10:45:53Z), Composer `b4681297` (#130, unchanged since SWEEP-1450), NexusAI `dcac002d` (#208, 08:46:10Z). **Open pull requests: 0 on HPSM-POC, MPS and NexusAI; Composer has only draft #85 (`b330/sm316-content-catalogue`, HOLD K6).** Control: the same `pulls` call with `state=closed` printed each project's latest merges (HPSM #328, #327, #326; MPS #205, #204, #203; Composer #130; NexusAI #208, #207, #206). No branch of any lane above is known to exist (not listed by origin here: UNMEASURED beyond the PR list; every kit's PRIOR WORK check decides).

## 1. HPSM-POC (HPSMPOC)

Open 148. Left the open set since SWEEP-1450: 484, 495, 496 (Done). New: 497 to 506 (ten, all `rec-2026-11-16`, Backlog, filed by the B1613/B1629/B1637 records seats). Code main `a816fd00`, no open PR. SWEEP-1450's H-1 (484, 496), H-3 (470 point 3) and H-4 (495) all landed (#328, #327, #326), so they are consumed.

### Buildable now (2 keys, 2 lanes)

| key | what | files (main `a816fd00`, printed today by `rg.sh`) | size | words / migration |
|---|---|---|---|---|
| HPSMPOC-505 | Test gap in `startingOwner`: replacing its `break` with `continue` passes all 135 owner tests. Add one row to the `startingOwner` block: 99 letters, the joined emoji the block already uses (8 UTF-16 units), then `b`, expecting exactly the 99 letters. The `break` is at `remediation-store.ts:68` (printed today: `if (cut.length + unit.length > OWNER_MAX) break;`; the function starts at `:58`; the test block at `remediation-store.test.ts:454`, printed today). Tests only; the ticket says "no product lines change". | `web/src/components/customer/remediation-store.test.ts` (read-only: `remediation-store.ts`) | S | None. The row must pass at main and go red with `break` replaced by `continue` on a copy. |
| HPSMPOC-504 | Reporting README states 208 tests (Readiness 60, Executive report 148) at `README.md:85` and `:88` (both printed today: "208 tests. Readiness (60)", "Executive report (148)"); the ticket's one run printed 865 passed. Ticket's proposed default: drop the counts; the alternative is counts read from a run with the run's date. | `api/src/HpsmPoc.Modules.Reporting/README.md` | S | Developer text, not a customer word. Default is to drop the counts (question 1). No migration. |

The ticket text of 505 also names a second Minor (a lone surrogate that is the 100th unit) from the same review; it is not in the key's recommendation and is out unless the builder's PRIOR WORK read says otherwise.

### Lanes (HPSM-POC)

- **H-5 start-of-owner test row** (505): owns `web/src/components/customer/remediation-store.test.ts` only. Sonnet, row L6 (line 85), gate G2 (line 109). Drafter rule 8: the `infra` job's repo-wide scans run in the gate whatever paths changed.
- **H-6 Reporting README counts** (504): owns `api/src/HpsmPoc.Modules.Reporting/README.md` only. Sonnet, row L6, gate G3 (line 110). The two sentences keep what each group of tests covers.

Both lanes are one-seat sized; they are disjoint by path and may be built serially in one seat if the floor allows only one (question 2).

### Excluded (HPSM-POC), with the reason

- **HPSMPOC-506:** accepted as built by Tuesday (a malformed `FollowUp` value now stops the host at start-up; the ticket's own default is "no change"). Not a lane; a code change back would be its own decision.
- **HPSMPOC-497, 498** (deploy script and deploy shape for the review site): 497 edits `scripts/deploy-from-ci.sh` and `infra/tests/test_deploy_package.py`, and its ticket says option (a) of HPSMPOC-480 "is the same idea for a different failure"; 480 still waits on the product owner (`ctx2.py`: pickup 2, 11-15 note 1 hits; no ruling read since). 498 is "choose a deploy shape", a decision. Both are deploy-round items, which are Tuesday's card.
- **HPSMPOC-499** (review-site template lacks `ForwardedHeaders__Proof`, `HPSM_FORWARD_PROOF` and the vault item name: `infra/modules/appservice.bicep`, `infra/README.md`): buildable text, but it is an infra template that a later UAT deploy would apply, and it travels with the deploy round. Held for question 3 (default: not a lane tonight).
- **HPSMPOC-500, 501, 502:** the driver script, the instructions and the comparison tool live outside the repository ("Nothing in the repository changes", each ticket). Not code lanes.
- **HPSMPOC-503:** timing flake "not diagnosed"; the ticket says "find the cause first; propose no bound". A diagnosis under an emulated SQL Server image, not a build lane; with 482 (NO-BUILD, B1605) it is a measurement item.
- **HPSMPOC-482 and 470 points 2, 4, 5:** unchanged from SWEEP-1450 (482 and 470 point 4 NO-BUILD; points 2 and 5 are layout calls "not decided"). 470 point 3 landed (#327).
- **Held or awaiting the product owner (carried):** 480, 481, 471 to 479, 483, 469.
- **HTML phase (Kam and Paul decide):** the 21 keys carried from `fleet/state/s279/sweep1925/hpsm_html_all.tsv` (21 rows; control: 368 is in it, count 1). Checked by key today: none of 504, 505, 497 to 503, 506 is among them (each counted 0), and all 21 are still open now (`comm` printed 21).
- **HP-tool integrations** and **the HPSM deploy round:** none touched.
- HPSMPOC-91, 162, 163 (draft documents in the analysis repository): not code, out.

## 2. Security Composer (PCOMP)

Open 81 (80 at SWEEP-1450 plus one new key; `comm` against SWEEP-1450's set prints only PCOMP-129 as new and nothing as left). Main `b4681297`, draft PR #85 stays held.

### Buildable now: 0

PCOMP-129 (new, filed by the B1612 records seat) is the hint under the justification box on the Controls screen: its ticket says "words only", and "they need approved wording from the project owner first". It is the W5 hint-words item that SWEEP-1450 already named as "goes to the product owner". Not a lane. PCOMP-128 (the 0022 Route B measurement, B1606) still waits on the product owner's words.

### Excluded (PCOMP)

- PCOMP-129 (words), PCOMP-128 items 2 and 5 (words), PCOMP-75 stays DROPPED (the Guided hold, with the held mark on the ticket since B1590).
- PCOMP-123 and 23 (edit `document-pdf.ts` and `pdf-fit.ts`, which held PR #85 touches); the 24 keys of the content catalogue in held PR #85; 52 (built, PR #84); 74, 80, 81 (records only); 46 and 94 (wait on the product owner). All other classes carried from SWEEP-1450 unchanged (set identical).

## 3. MPS Commercial Calculator (MPSCALC)

Open 169. Left the open set since SWEEP-1450: 185, 394, 404, 405, 406 (Done, B1636 R250 records). New: 407 (B1611 records, filed 15:53), 408 and 409 (B1636, the Minors of #201 and #203). Main `56bfe232`, no open PR. SWEEP-1450's lanes are consumed: M-G landed #200 (406), M-S #201 (404, 405), M-D #202 (390, 394, 371, 195), M-E #203 (185), and M-T #205 (369; 163 stayed a measurement). MPSCALC-390, 371, 195 and 111 still read open because their moves are held for a later records pass (daily note 21:19 and 21:38: "371 and 111 comment only", "371/111 moves in a later pass"); they are not buildable. Pricebook values are confidential: none appears here.

### Buildable now (3 keys, 3 lanes)

**M-F fleet line id test rows** (MPSCALC-407 items 1 and 2). Owns `tests/MpsCalc.Api.Tests/FleetLineIdTests.cs` (new rows only; the ticket's acceptance says no existing row is removed or changed). Read-only: `src/MpsCalc.Api/Quotes/PriceAudit.cs` (`:250`, printed today: `pairs.Add(byId.TryGetValue(o.FleetLineId!, ...` ) and `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` (`:1672`, printed today: `foreach (bool identicalOnly in new[] { true, false })`). Item 1: a committed row that removes line 2, renumbers line 3 to 2 and changes the moved line's colour override, expecting the entries the review's probe printed, red if the pair is named by the old number. Item 2: a row red when the identical-line-first pass is removed, or record the pass as accepted-unpinned. The ticket's own measurement says the existing same-number rows stay green without that pass, and the existing removal row is `FleetLineIdTests.cs:115` (printed today). **Item 3 (the contract wording "Never refused" at `docs/API.md:284` and `openapi.json:952`) is "the product owner's words": out.** Size S. Sonnet, row L6 (line 85), gate G2. No migration, no product line.

**M-S2 dev stub follow-ups** (MPSCALC-408). Owns `web/src/api/stub/purchaseQuotes.ts` and `web/src/api/stub/stubApi.test.ts`. Items: (1) rows for control codes 31 and 159 on the typed reference, each red when its loop bound moves by one (loop printed today at `purchaseQuotes.ts:289-295`: `bad = c < 32 || (c >= 127 && c <= 159)`); (2) a row that stores an explicit null target GP and expects it to count as absent (`purchaseQuotes.ts:316`, printed today: `if (target !== undefined && target !== null) throw refusal(...)`); (3) the three refusal titles exist twice (`guarded` and `requireCopyable`, the second group at `:317-321` printed today): share them, or record one sentence that two copies are accepted. Item 3 is the only edit to a product-side stub line. Size S to M. Sonnet, row C2 (line 92) because item 3 edits a non-test file, gate G2. No words (the stub's refusal titles already exist; they are not new words), no migration.

**M-E2 dialog's own box at 390 px** (MPSCALC-409). Owns `web/e2e/dashboard-390.spec.ts` only (the form row is at `:36` and the planted control at `:44`, both printed today). Add a row that opens the New quote dialog at 390 px and checks the dialog's own box (right edge no further than the window's client width), with a planted control that widens the dialog and turns the row red; the existing five rows are unchanged. If the dialog is wider than 390 px today (UNMEASURED by the ticket), the builder STOPs and reports, because `web/src/styles.css` is not owned. Size S. Sonnet, row L6, gate G2. Starts the Playwright stub server, so it needs a port.

### Conditional, not counted

- **MPSCALC-200** (importer coverage table, `docs/IMPORTER.md`): the table at main has been reshaped since the ticket was filed (`IMPORTER.md:112-118` now shows A4 hardware 25 / 25 / 22 and A3 hardware 27 / 23 / 8; the ticket's `:112, :117 @8b74538` contradiction rows no longer print at those lines). The last Jira comment (2026-11-10) says clauses 2 and 3 stay unmet because the 15 unread A3 rows and 3 unread A4 rows are "defined as not read" but not decomposed. Whether that needs the price book (confidential; counts only) is UNMEASURED. Default: not launched; a builder reads the table against the ticket first (question 4).
- MPSCALC-233 and 123 (clone refusal sentence, upload bound): carried from SWEEP-1450, still need a refusal sentence the user sees; not launched (SWEEP-1450 question 5, unanswered).

### Excluded (MPSCALC), with the reason

- **MPSCALC-163** (four counted runs owed: a measurement, not a lane) and **MPSCALC-372** (needs the deploy card; #204 landed the setting, the infra apply is a card): excluded by the commission.
- **MPSCALC-369:** landed as #205 (`56bfe232`), its move is owed to the next MPS records pass.
- **MPSCALC-139** clause 4 (axe): Tuesday's earlier Q2 = NO (a new registry dependency is a decision); out. **MPSCALC-111** clause 4: evidence came with #203; move held for a later pass; out.
- **MPSCALC-390, 371, 195:** built in #202; moves owed; not lanes. **MPSCALC-316** carries `needs-ruling`: out.
- **Landed, records owed:** the M-T records (#205) in the next MPS records pass. **Held or card-bound** (carried from SWEEP-1450's read of the pickup and notes; this sweep re-checked only the new keys): 135, 364, 189, 121, 130, 78, 120, 402, 222, 103, 226, and 158.
- **HTML phase (Kam and Paul decide; labels `lane-v1` to `lane-v11`):** 48 open keys carry a `lane-v<digit>` label today (counted by `grep -c "lane-v[0-9]"`); none of 407, 408, 409, 200 carries one (0 of 4; control: the 48). Carried: 288, 237, 236 are ruling or words items.

## 4. NexusAI (RD)

Open 866. Left the open set since SWEEP-1450: RD-992 (Done). New: RD-994, 995, 996, 997, 998 (all `records-pass-1116`; 994 to 997 filed by B1614 at 15:28, 998 by B1638 at 21:43). Main `dcac002d`, no open PR. SWEEP-1450's NX-T lane landed as #208 (987, 986, 991, 993 moved to Testing; 983, 985, 810 comment only).

Code-scanning on main at `dcac002d`: **47 open alerts**, unchanged from `d83eab99` (#208 touched tests only). Read with `gh api -X GET repos/datasecau/Reporting_Dashboard_Au/code-scanning/alerts` `state=open`, `ref=refs/heads/main`, `--paginate`; every row's `commit_sha` reads `dcac002d` (47 of 47). Controls: `state=fixed` on the same call returned 204 rows, more than one 100-row page, so pagination fires; the analyses list for `refs/heads/main` shows a CodeQL run on `dcac002d` at 08:49:46Z with `results_count` 47 (a second analysis at 08:47:07Z for the same commit reads 0, a different language run, not read further). By file: `backend/server.js` 13, `jsonStorage.js` 6, `services/emailService.js` 5, `queryPreprocessor.js` 4, `static/js/settings.js` 2, `static/js/index.js` 2, `routes/entraProvisioning.js` 2, `marketplaceStore.js` 2, `incidents.js` 2, and one each in `tests/uat-run.js`, `validators.js`, `ticketStore.js`, `services/entraGroupGate.js`, `mondayClient.js`, `marketplace-api.js`, `intentRouter.js`, `costCentreMap.js`, `azureLogAnalytics.js` (sum 47; list in `rd_alerts_open.tsv`). Never dismiss an alert.

### Excluded first, as the commission orders

- **Lane NX-S2** (B1633 N138, LIVE: RD-765, 766, 767, 768, 769, 421) and **lane NX-P** (B1634 drafted: RD-805, 771, 804): excluded with every path they own. From their kits' `OWNS` blocks (printed today): NX-S2 `backend/queryPreprocessor.js`, `intentRouter.js`, `ticketStore.js`, `costCentreMap.js`, `jsonStorage.js`, `marketplaceStore.js`, `validators.js`, `services/emailService.js` (Part 6 only, Q3 NO), five-to-six NEW test files and `scripts/verify-expected-counts.json`; NX-P `static/js/index.js`, `static/js/settings.js`, `backend/routes/entraProvisioning.js`, two NEW test files and the counts file. Neither kit edits an existing test.
- **RD-810** (Kam's card open, `tests/uat-run.js`, alert #151): excluded by the commission.

### Lane NX-T2: test harness and pins (Sonnet, row L6 line 85, gate G2 line 109)

Owns four existing test files and the counts file; no product file. Keys read today:
- **RD-998:** `expectTamperInsideTheWindow` (`__tests__/rd452-group-config-strict-callback.test.js:430`; the strict `r.tamperedAt < r.answeredAt` is at `:432`, printed today). The file already has the counter `eventOrder` (`:82`, and `answeredOrder = ++eventOrder` at `:128`, printed today). Stamp the tamper with the counter where `tamperStore` returns its record (`:309` per the ticket), compare the two orders, add cells in the form of T1 to T4. Red-first: put the strict clock comparison back on a copy. Nothing has failed on this check (the ticket says so).
- **RD-985 residual cell:** one cell in `__tests__/rd969-three-routes-empty-request.test.js`: `POST /api/settings/business-hours` with no content type and no body, expecting 400 and the settings file byte-identical; the ticket's comment says it reads 400 at head and 500 when `isPlainRequestObject` is forced true, so it is red where H6/H7 are not. Also reword the comment above H6 (the comment starts at `:142`, printed today, and says a request with no body "is told apart from a valid one by the check alone"; the Jira comment says H6 sends a JSON content type). RD-985 stays open until this lands.
- **RD-996:** `__tests__/rd770-model-endpoint-host-match.test.js:97` (a UNIT cell that compares the table's own two columns and calls no code: make it call `hostMatchesDomain` per row, or remove it and regenerate counts; the choice is the author's) and `__tests__/rd772-773-dept-escape-and-stream-chunks.test.js:56` (reword the HOSTILE cell title to what its expectations show). Title and cell only; no product line.
- The four files are read-only to NX-S2 and NX-P (each kit adds only NEW test files and says "any edit of an existing test" is a STOP).
- Not included: **RD-983** (its acceptance item 3 is the builder's reading, not re-read by the review; the seat left it comment only), RD-987, 986, 991, 993 (Testing: not work).

### Lane NX-R: role table words and list entry (Sonnet, row C2 line 92, gate G1 line 108 by default)

RD-995 (the product owner's 2026-11-16 ruling on RD-992, "Keep its own check", read at the ticket; RD-992 is Done). Owns `docs/ROLE-CAPABILITIES.md` (row at `:137`, printed today: "any signed-in session (anonymous refused; viewer reaches the handler 400); handler gate: none") and `backend/services/capabilities.js` (the L1 pending group, the route is the third entry of `:227`, printed today). Per the ticket, read how the row note is produced before editing and regenerate whatever the project generates with its own command (names UNMEASURED: the NX-S2 and NX-P kits both run `node scripts/role-capability-inventory.js --check`, so the inventory and the census test are the instrument), keep the suite counts equal or regenerate them. The route's behaviour does not change. The gate is G1 by default because the file is the role capability table (question 6). The row note is developer text (what the route does and that the owner chose to keep the check), not a customer word.

### Lane NX-A: audit entry field checks (Opus, row C3 line 93, gate G1 line 108)

RD-994, built on the product owner's ruling. Verified at source today: `decision_queue.sh show nexusai-audit-details-size-cap-1116` prints `status: ruled`, `ruling: choice='b'` (option b: "Check each entry type's fields instead"), `ruled_ts=2026-11-16T14:29:36.991428+11:00`, and `delivered_artefact` names C-289 and "the per-entry-kind field check filed as RD-994; RD-806 commented and kept open". Owns the `auditLog` call sites in `backend/server.js` (the function is at `:305`, printed today: `function auditLog(action, details, req = null)`) and one NEW test file; counts file. Per the ticket: census all 48 `auditLog` call sites first (the ticket's author read 29 as naming a request value and did not read the other 19 one by one), state each kind's fields, types and length limit, check them where the entry is built, red-first one over-long and one wrong-type cell per kind. **How an over-long value is shown (cut and marked, or refused) must be the same for every kind; the ticket says to ask on the ticket if that needs the product owner's word (question 5).** Medium to large. Not claimed by any other lane: NX-S2 and NX-P do not edit `server.js` (NX-S2's STOP list holds `git hash-object` of `server.js` equal to BASE's). RD-806's own alerts (`server.js:390` and two other rows) are not in this lane.

### Conditional and excluded (NexusAI)

- **RD-997** (the five static pages are served by `express.static` at `server.js:2896` with no limiter): the ticket says "decide whether the limiter should also sit ahead of the static mount"; a design decision, and `server.js` is NX-A's file. Excluded (question 7).
- **RD-807** (`incidents.js:91` and `:93`, two prototype-polluting alerts still open on main, status Testing): not claimed; unchanged from SWEEP-1450 question 3.
- **RD-763 and RD-764** (13 `server.js` alert rows beyond RD-806's: design judgements), **RD-806** (card ruled b; the build is RD-994), **RD-820** (needs a seam in `server.js`; excluded as in SWEEP-1450), **RD-930 and 931** (HELD), RD-117 and 188 (first-run slice, real-browser CSP check first): not counted.
- Held, ruling or words (carried, not re-read): RD-989, 610, 612, 622, 644, 433, 893 part 2, 896, 974, 975, 702, 636, 522, 966, 990, 932. NX-B backend periphery (455, 744, 745, 750, 824, 728, 577, 578; the erasure family is row C4, Opus, never a Sonnet kit), NX-F2 dashboard and css, NX-F1's remaining eight, and the carried test-tail keys: carried unchanged, not counted.
- **The NexusAI demo hold (C-224):** nothing deploys; no lane touches a deploy. Testing and Release Ready are not work.

## 5. Disjointness check

By path, per program (a "program" here is the path list below compared by eye plus the kits' own `OWNS` blocks printed today; no code was run over file sets).

- **HPSM-POC:** H-5 `web/src/components/customer/remediation-store.test.ts`; H-6 `api/src/HpsmPoc.Modules.Reporting/README.md`. Disjoint.
- **MPS:** M-F `tests/MpsCalc.Api.Tests/FleetLineIdTests.cs`; M-S2 `web/src/api/stub/purchaseQuotes.ts` and `stubApi.test.ts`; M-E2 `web/e2e/dashboard-390.spec.ts`. Disjoint. One coupling, not an overlap: the 390 px spec runs against the stub M-S2 edits (the stub's Duplicate rules); M-S2 changes refusals and rows only, and the builders' PRIOR WORK check re-reads the spec's green at the base.
- **NexusAI, among the three new lanes:** NX-T2 (`__tests__/rd452-...`, `rd969-...`, `rd770-...`, `rd772-773-...`), NX-R (`docs/ROLE-CAPABILITIES.md`, `backend/services/capabilities.js`, files generated by the inventory command), NX-A (`backend/server.js` audit sites, one new test file). Path-disjoint. **Shared by all three, and with NX-S2 and NX-P: `scripts/verify-expected-counts.json` (each kit's commit K writes it) and the one jest lock.** So no two NexusAI seats may build or verify at once: each lane's K must be made on the base the previous lane's landing left, and the first lane to land moves main under the others (their HOLD 20 on a moved main). NX-R's change to the committed inventory also matters to any lane that runs `role-capability-inventory.js --check` (NX-S2, NX-P, NX-A): that check compares to the committed file at each lane's own base, so it stays green until a rebase.
- **NexusAI, against NX-S2 and NX-P (excluded lanes):** no new lane edits any `OWNS-B1633` or `OWNS-B1634` product path; NX-A edits `server.js`, which NX-S2 holds byte-equal and NX-P lists as "RD-806 and the other `backend/server.js` rows" left for others. NX-T2 edits four existing test files which neither kit edits.
- **Against the records seats still live or queued:** B1636 (MPS, READY), B1637 (HPSM, DONE) and B1638 (NexusAI, READY) write only the root records repositories and Jira (the MPS root `CLARIFICATIONS.md`, the HPSM analysis repository, NexusAI's `1_Project_Definition/`); every lane above writes only the project code repositories' paths above. The one open edge is B1638's held HISTORY.md and BACKLOG entry (card `nexusai-records-commit-identity-1116`): if it lands in the code repository it is a `.md` outside every NexusAI lane's owned paths (`docs/ROLE-CAPABILITIES.md` is a different file). Composer: no lane.

## 6. Questions for Tuesday (each with a default)

1. HPSMPOC-504: drop the test counts from README `:85` and `:88`, or write counts read from a run with its date? Default: drop them (the ticket's own proposed default); the sentences keep what each group covers.
2. The floor holds one seat today (N138, load1 about 6.5 at 21:47). Order of launch? Default: one seat at a time in this order, HPSM-POC first (H-5, H-6, same seat, serial), then MPS (M-F, M-S2, M-E2), then NexusAI (NX-T2, NX-R, NX-A) after NX-S2 and NX-P have landed or ended.
3. HPSMPOC-499 (review-site template and its README: three new lines, a vault item name). Launch as an Opus seat with gate G1, or hold it for the HPSM deploy round with 497 and 498? Default: hold; it is not a lane tonight.
4. MPSCALC-200: launch a read-first builder (re-read the table against the ticket; the decomposition may need the confidential price book, counts only), or leave it? Default: leave it; it is conditional and not counted.
5. NX-A: if "cut and marked" versus "refused" for an over-long audit value needs the product owner's word, the seat asks on RD-994 and does only the kinds where the answer is already the file's shape. Default: the seat does the census and the kinds that need no choice, records the rest on the ticket, and a card follows only if the choice is Kam's.
6. NX-R: gate G1 (Opus) or G2? The change removes one route from a role-capability list and changes a table row; no route answers differently. Default: G1, because the file is the role table (a security surface per the G1 row's wording); a G2 gate is the cheaper alternative if Tuesday reads it as docs only.
7. RD-997 (limiter ahead of the static mount) and RD-807 (two incidents.js alerts, status Testing): leave both out of every lane? Default: yes; 997 is a decision, and 807 stays with the NexusAI records seat's question from SWEEP-1450.
8. Counts-file contention: ask each NexusAI lane to HOLD at READY if main moved (their HOLD 20), or let NX-T2 go first because its change is the smallest? Default: NX-S2, NX-P, NX-T2, NX-R, NX-A in that order, one seat at a time, each rebasing on the previous landing.

## Method and disclosures

- Instruments: `jqdump.py` (GET-only, credentials read in-process from each project's own `4_Credentials/.env`, never printed) for eight board dumps (open and Done for four projects); `board_count.sh jira` through `bc.sh` for the eight counts (its `TOTAL=` lines printed no truncation refusal, limit 5001); `jdesc.py` (GET-only) for ticket bodies of 497 to 506, PCOMP-129, MPSCALC-407, 408, 409, 200 and RD-998, 985, 994 to 997; `rg.sh` (one file at a time through `gh api -X GET repos/<repo>/contents/<path>` at `main`) for every `file:line` marked "printed today"; `ctx2.py` (whole pickup plus the 11-15 and 11-16 notes, per key) for the held and dropped check; `gh api -X GET` for mains, `pulls` and code-scanning, each under its project's own `GH_CONFIG_DIR`. Scripts were copied from SWEEP-1450's scratch folder into this one.
- Held and dropped check: `ctx2.py` hits on the candidates were records-created or landing mentions only (HPSMPOC-504 and 505 and MPSCALC-408 and 409 and RD-998: the 11-16 note line 139, which names them as candidates; RD-985: stays OPEN with the follow-up; RD-994 to 997: the pickup's records-created line). No held or dropped mark found on any lane key. Zero-hit keys are zero of this instrument; its controls fired on HPSMPOC-470 (hits in all three sources), MPSCALC-372 (4 and 7) and RD-806 (3 and 6). `ctx2.py` printed no hold or drop line for MPSCALC-111, 200, 371 (zero hits in all three sources), so their "held" status above rests on the daily note's own lines 131 and 134, not on this tool.
- Not measured: whether any pane currently holds a ticket here (no pane list read); the remediation-store test file's `startingOwner` block beyond its first lines and its 135 rows' count; the line numbers the tickets give in files this sweep did not print (`ForwardedProofTests.cs`-class and `tamperStore` at `rd452:309`, `PriceAudit.cs` beyond `:250`); that the form's dialog is within 390 px (409's own UNMEASURED); the number of auditLog call sites (48 is RD-994's); which files the inventory command regenerates; the 21-key HPSM HTML list and the 48 `lane-v` MPS keys are from earlier sweeps and today's labels, not re-read; Composer's PR list beyond #85 and the closed list; the second CodeQL analysis at `dcac002d` with `results_count` 0 (read as another language run, not opened).
- Outside the one-output-file rule: the scratch folder named at the top (`*_open.tsv`, `*_done.tsv`, `*_open.k`, `rd_alerts_open.tsv`, `bc.sh` and the copied scripts). No `decision_queue.sh list`, no WEDNESDAY, FRIDAY, Secuura or non-Datasec tree read, no ledger file read. One `decision_queue.sh show nexusai-audit-details-size-cap-1116` (allowed, printed above); the first try at `fleet/decision_queue.sh` failed (the script is at `tools/decision_queue.sh`; nothing ran). Two hooks advised once each (a `$R` word-split refusal and the `cut` advisory); neither blocked a result read here. The daily note and pickup were read by `sed -n` and Python slices over the tracked files.

READ-WHOLE-BY-TUESDAY: ____
