# SWEEP-1326: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-11)

Source order: Kam, live board 2026-11-11 13:25:55: "please work on tickets and backlog items for all projects". Filter: no decision from the product owner (Kam) or his deputy (Paul) needed. Written by a read-only sweeper; HPSM-POC swept by the sweeper itself, PCOMP, MPSCALC and RD by one Sonnet sub-sweeper each under the same fences (their findings are folded in below, with their own caveats kept).

## BLUF

- Board census (instrument: `jqdump` JQL `project = <KEY> AND ( statusCategory != Done )`, paginated to completion, 2026-11-11 about 13:2x): HPSMPOC 140, PCOMP 89, MPSCALC 214, RD 853 open. Every JQL carried the parentheses.
- Actionable now (judged by reading the ticket and its newest comment; "actionable" = the Done-when is buildable by an agent with no ruling, no deploy, no production touch, no HP-tool integration):
  - HPSM-POC: 14 existing tickets plus 2 new findings that have no ticket yet. Small yield: almost every other open ticket is built-and-waiting, ruling-bound, HTML-phase, or deploy/hosted-bound.
  - Security Composer (PCOMP): 9 of 89.
  - MPS Commercial Calculator (MPSCALC): 43 of 214.
  - NexusAI (RD): about 104 keys (hand count, about 87 table rows after duplicate pairs) of 391 To Do; the 445 Testing + Release Ready tickets were not read individually (UNMEASURED beyond type counts).
- Lanes proposed: HPSM 5, PCOMP 3, MPSCALC 5, NexusAI 5 = 18 lanes, file-disjoint inside each project by ownership rule. Cross-lane exceptions are named per project.
- Heaviest immediate value: NexusAI lanes F1, F2, B, T (no live-branch conflict), then MPSCALC L1/L2/L4/L5 (no open PR, no seat in flight), then PCOMP B and C. NexusAI lane S and anything touching `backend/server.js` must wait for the B1484 landing chain.
- The two new findings from today's user guide have NO ticket (checked by program, see HPSM section). Both are candidates; the "fifth customer" one has an unmeasured root cause.
- Things Tuesday must decide before launch are listed under "Questions for Tuesday" at the end.

Frame notes: all file lists come from tickets, comments and origin tree reads; every local `2_Project_Files` checkout is stale (HPSM-POC checkout 2026-09-23, PCOMP 2026-11-03, MPSCALC 2026-10-01), so each builder's PRIOR WORK check and a `git grep` on origin main must re-confirm before building. Origin mains at sweep time: HPSM-POC `009421a2` (code main as the records read it), PCOMP `c684e808`, MPSCALC `54ed7627`, NexusAI `0ab365b1` (all by `gh api -X GET`).

---

## 1. HPSM-POC (Jira HPSMPOC)

Open: 140 (jqdump COUNT; 3 In Progress, 137 Backlog). Live work: no open pull request (`gh api -X GET repos/datasecau/HPSM-POC/pulls?state=open` returned none); branches b1440, b1441, b1442, b1463, b1464 are on origin and read "diverged" from main (squash-merged style; not proven merged: UNMEASURED); seat B1491 (user guide v0.4, documents only) is the only 2026-11-11 seat touching product-adjacent files, and it writes only under `1_Project_Definition/`.

Exclusion rule applied: every ticket matching an item of the 2026-11-10 decision document (85 items D-001 to D-085, this-phase and next-phase alike) is excluded, and so is any HP-tool integration.

### Actionable (14 existing tickets)

| key | title (short) | state | why actionable now | size | files (from ticket; confirm on origin) | conflicts | lane |
|---|---|---|---|---|---|---|---|
| HPSMPOC-439 | Engagement overview: Recent activity row spacing differs for linked and plain titles | Backlog | Ticket calls it a look, "no word needed"; Done-when is equal spacing or declined | S | engagement overview component under `web/src/components/customer/` | none known | H-A |
| HPSMPOC-357 | Customer page scrolls sideways at 360 px (stage badge does not wrap) | Backlog | PR 244 did not meet the 360 px clause (records comment); CSS fix, measured by scroll width | S | customer page stage badge (`whitespace-nowrap` span) | H-A files | H-A |
| HPSMPOC-432 | Finding page 360 px: one axe scrollable-region-focusable | Backlog | Same rule as HPSMPOC-409, fix pattern already built in PR 274 for another wrapper | S | finding page overflow-x block | share a11y pattern with 409 | H-A |
| HPSMPOC-409 | Two a11y findings: item 1 built (PR 274); item 2 moderate region rule on snapshot pages still open | Backlog | Item 2 buildable; the product owner already ruled to keep the caption pattern (C-269) | S | snapshot page components | with 432 | H-A |
| HPSMPOC-461 | UAT feedback: widen snapshot tile to line up with engagement panel and Next button | Backlog | Kam's own UAT feedback; Done-when "built and merged, or declined"; layout only, no new word | S | assessment page snapshot tile | assessment page, near D-065/D-044 only by page, not by item | H-A |
| HPSMPOC-462 | UAT feedback: pill button fill does not match rounded outline | Backlog | Kam's own feedback; CSS fill/outline mismatch; the "UX/UI review" half can be scoped as its own ticket | S | shared button component / css | shell lane H-B | H-B |
| HPSMPOC-465 | UAT feedback: Training page phase buttons look like progress indicators | Backlog | Kam's own feedback, "distinct look and a separator", no words | S | `/training` page components | D-047 (Training descriptions, an HTML item) touches the same page: build only the look, nothing from D-047 | H-B |
| HPSMPOC-399 | After PR 240: remaining 2 of 4 notes (scroll test row measures before table renders; customer page 6 px wide at 390 px under wide letter spacing) | Backlog | PR 282 answered the ring and radius clause; the other clauses are test and CSS | S | e2e scroll row, customer page css | H-A (customer page css) | H-B |
| HPSMPOC-405 | Fixed Feedback pill sits over a list page's only row button at 768 x 1024 | Backlog | PR 274 built part (Customers and Workspace lists keep room); a shell-level safe area is the clean fix named by the gate | S | shell / `AppShell.tsx`, list pages | H-B shell files | H-B |
| HPSMPOC-406 | Partner Home after PR 252: items 2 to 5 (one-column order, table vs stage bars, 20 px link, link target) | Backlog | Item 1 done; items 4 and 5 (link size and target) are code-only; items 2 and 3 are layout calls, so build 4 and 5 only | S | `web/src/components/partner/PartnerDashboard.tsx` | HPSMPOC-457 and D-043 (partner dashboard rebuild, HTML phase) touch the same file: tiny edits only, or hold | H-B |
| HPSMPOC-228 | Site timing notes: N-5 (refresh fan-out: no in-flight refresh map in `entra.ts`) and N-7 second half (Retry saving button) not built | Backlog | Records check at main `eaf77b3c` (2026-11-06) lists exactly 5 of 7 built, N-5 not built, N-7 half | M | `web/src/server/auth/entra.ts`, `web/src/server/bff.ts:418`, `web/src/api/client.ts:328`, `web/src/components/snapshot/SnapshotRunner.tsx:57` | N-7 text may count as a word: build N-5 only unless words are ruled | H-C |
| HPSMPOC-436 | Offline template: finding explanation with zero findings writes zero paragraphs, refused as schema-invalid | Backlog | Reach already MEASURED yes by the records comment (route accepts an empty finding list); fix is a route refusal or a template line, each with a red-first test | S | `AssessmentModule.cs` (:252, :167-175), `ReportingEndpoints.cs` (:29-30), offline template | a refusal message is a word: reuse existing refusal wording | H-C |
| HPSMPOC-408 | Remediation register after PR 257: items 1 and 3 built (PR 265); item 2 (bare-label refusal reachable) open | Backlog | Done-when "each item built or declined"; item 2 is a code and test change | S | remediation register validation (api + web) | the ticket says "scope call not made here": build only if Tuesday treats the gate's fix shape as given | H-C |
| HPSMPOC-356 | `test_ci_workflow.py` after PR 221: B734-9 and B734-6 untouched (B734-3 built by PR 233) | Backlog | Test-only | S | `infra/tests/test_ci_workflow.py` | drafter rule 8 applies: the infra job and its repo-wide scans run in the gate | H-D |

New findings from today's user guide (no ticket exists; ticket search by program: `text ~ "Service offers"` 10 hits, none a walkthrough-title ticket; `text ~ "walkthrough"` 5 hits, none on this; the fifth-record search returned only unrelated tickets):

| id | title | why actionable | size | files | lane |
|---|---|---|---|---|---|
| NEW-1 | Walkthrough step 12 (the "offers" step) says "Service offers" while the menu says "Delivery phases" | Origin read: `web/src/content/walkthrough/steps.ts:143` title "Service offers: Assess / Implement / Optimize"; `steps.ts:212` link label already "Delivery phases"; `steps.test.ts:29` pins the old title; `ServicesHub.tsx:23-24` uses "Delivery phases"; `GlobalNav.tsx` label "Delivery phases" (user guide CHANGES_v0.4.md row 9 to 12). Fix = use the existing label; no new word. If Tuesday treats step titles as the product owner's script words, make it a card first. | S | `web/src/content/walkthrough/steps.ts`, `steps.test.ts`; check `web/e2e/playbook-partner.spec.ts` | H-E |
| NEW-2 | Consultant and Admin customer lists show a fifth customer not marked "(sample)" | Seen in the B1491 crawl (STATUS lines 148 and 170; CHANGES_v0.4.md row 4). ROOT CAUSE UNMEASURED: it may be a test record in the UAT database (a data fix, not agent work, and UAT writes are not this sweep's) or code that lets a non-seed record through. First step is read-only: find where the "(sample)" suffix is applied and whether consultant/admin lists include a user-created record. | S to M | sample marking code (`b25/sample-tag-user-customers` is the earlier branch name), customer list components | H-E |

### Lanes (HPSM-POC)

- H-A, customer workspace look and accessibility: 439, 357, 432, 409, 461. Files under `web/src/components/customer/` and the snapshot/assessment pages. Order: 357, 439, 409+432 (one a11y pattern), 461. Sonnet.
- H-B, shell, buttons, Training look, Partner Home small items: 462, 465, 399, 405, 406 (items 4 and 5). Files: shell, button component and css, `/training`, `PartnerDashboard.tsx`. Does not share files with H-A except 399's customer-page css: put the 6 px letter-spacing clause in H-A. Order: 462, 405, 465, 399, 406. Sonnet.
- H-C, server and API residues: 228 (N-5), 436, 408 (item 2). Files: BFF (`web/src/server`), `AssessmentModule.cs`, remediation register. Sonnet; API tests must pass on SQL Server as CI does (drafter rule: HPSM Api test rows ask "does it run on SQL Server as CI does?").
- H-D, infra tests: 356 only. File `infra/tests/test_ci_workflow.py`. Sonnet. Can ride one seat with H-E if load is tight.
- H-E, new findings: NEW-1 (walkthrough title) then NEW-2 (read-only diagnosis first). Files `web/src/content/walkthrough/*`, sample marking. Needs two new Jira tickets first (Jira write is Tuesday's or the kit's scope, not this sweep's).

Standing line for every kit: this phase builds no integration with HP tools; nothing deploys.

### Excluded (HPSM-POC, 126 existing tickets)

Class counts below come from a program that assigned every one of the 140 open keys to exactly one class and asserted the union equals the jqdump set (140 assigned, 0 missing, 0 extra).

- Epics, containers (10): HPSMPOC-1, 10, 18, 23, 30, 38, 45, 50, 56, 448.
- HTML phase item (21), matching the 2026-11-10 decision document: 449 to 460 (the 12 "Phase 2 first work" tickets: D-031 to D-080 groups), 463 (white menu column = D-031) and 464 (collapsible groups = D-031; both are Kam's UAT feedback but match a this-phase HTML item), 368 (sidebar and top bar = D-033/D-034), 370 (customer picker = D-033), 390 (role definitions = D-034), 392 (Good/Better/Best = D-027), 393 (framework alignment = D-076), 394 (Training principles = D-047), 396 (branding and revenue calculator inputs).
- HP-tool integration, HP-owned or waiting on HP/Kam (26): 82, 83, 84, 85, 86, 97, 166, 167, 181, 241 (awaiting HP); 191, 220, 240, 47, 48, 94, 46, 259 (HP Security Manager or other HP-tool integration, or next-phase architecture for it); 92, 96, 173 (next-phase, backlog only); 162, 163, 164, 165, 168 (content drafts for Kam, HP review).
- Needs ruling or waits on Kam or Paul (26): 14, 52, 31, 35, 37, 44, 51, 55 (SME or Kam rulings, scoring RS-03 to RS-10); 109 (O-1 delivery proof not ruled), 180 (schema bump), 193 (residual now live; settings choice), 224 (NO GO stops it by ruling), 226 (B177 N-1 words, a proposal), 246 (N-4 record, ruling), 271 (pin owner and cadence), 318 (close or decline question to product owner), 322 (B477-7 no fix shape), 352 (B622-2 candidate decisions), 420 (wording; C-277 ruled the four surfaces, the rest is wording), 467 (Demo view surfaces: decision per surface), 237 (money), 257 (feedback file names), 242 (placeholder), 90 and 91 (needs-kam).
- Deploy, hosted measurement, VM or Azure (15): 126, 196, 207, 234, 235, 309, 303, 428, 362 (hosted deploy or measurement, no hosted HTTP in this sweep and no deploy), 304 (VM cleanup only when the product owner agrees), 57 (environments), 62, 60, 64, 63 (demo freeze, hosted Playwright, hypercare, handover).
- Records-check closings, no build left (8; UNMEASURED whether each Done-when is met, a records seat must verify): 99, 178 (merged PR 187 and 189, deployed), 431 (PR 278 built the room; Done-when text read as met), 323 (PRs 197, 202, 203 landed), 343 (trace recorded; follow-on PRs landed), 117 (PR 307 migration applied on UAT), 100 (PR 307 code live on UAT; purge idle by design), 315 (PR 200 merged; the 60-run SQL Server shard was NOT RUN: a CI re-run with a stated result closes it, may be worth a records seat).
- Human-owned or SOW paperwork (20): 5, 6, 11, 12 (demo story v0, an owner-agent seed that predates the built walkthrough, UNMEASURED), 19, 20, 21, 24, 29, 58, 61, 169, 170, 171, 172, 174, 175, 176 (SOW-final documents for HP; Kam's call when), 389 (cross-page QC after all lanes merge, blocked), 395 (audience testing, gather).

---

## 2. Security Composer (Jira PCOMP)

Open: 89 (jqdump COUNT; all Backlog). Types and labels by awk over the dump: 4 epics, 19 labelled `held`, 2 labelled `needs-kam` (PCOMP-46, PCOMP-94), 9 actionable, 55 other exclusions; 9 + 80 = 89. Control: a nonexistent label returned 0; the 19 `held` matches the records seat's count in B1489 status.

Live state: no seat in flight (STATUS files B1486 and B1489 finished; read from files, not panes). Open PRs: #85 (draft, "HOLD K6", L1 SM 3.16 content catalogue; touches `packages/renderers/src/document-pdf.ts`), #86 and #91 (Dependabot). Branches b1420, b1422, b1423 exist but their PRs #120, #121, #119 merged 2026-11-10. Few PCOMP tickets carry a Done-when line, so each builder writes closing conditions as its first comment.

### Actionable (9)

| key | title (short) | state | why actionable now | size | files | conflicts | lane |
|---|---|---|---|---|---|---|---|
| PCOMP-23 | Policy PDF drops the manifest hash line with long names (change-report half merged in PR #120) | Backlog | Measured defect, closing clauses in comment 40721; no word change | M | `packages/renderers/src/document-pdf.ts`, `pdf-fit.ts`, a renderer test | PR #85 touches `document-pdf.ts`; same files as 123 and 82 | A |
| PCOMP-123 | Size the footer by the real page count (11 of 28 wide-letter footers become whole) | Backlog | Measured improvement, not built | M | `packages/renderers/src/change-report.ts` (`FOOTER_LABELS`, line 535), `document-pdf.ts`, `pdf-fit.ts` | PR #85; 23 | A |
| PCOMP-82 | Policy PDF cover date in Sydney time, set on the brand profile | Backlog | Ruled in C-71 COMP-15 (a): brand profile, Sydney time, cover only; looks unbuilt (grep on a stale ref found nothing; UNMEASURED on main) | L | new migration plus rollback in `packages/db`, `packages/api-contract/src`, brand profile in `apps/api`, `document-pdf.ts` cover | PR #85; 23 and 123; the cover label "(released, UTC)" changes, check against the ruling | A |
| PCOMP-77 | Expert controls: one "mark all local" action; no justification for a local value | Backlog | Ruled in C-71 COMP-11 (a); row #104 reads OPEN; code still holds the justification string | M | `apps/web/src/screens/w2/model.ts` and test, Expert controls screen, maybe `apps/api/src/routes/inputs.ts` | `inputs.ts` shared with 15; button label must use the ruling's own words | B |
| PCOMP-75 | End page "Still to answer" heading touches the tiles (item b) | Backlog | CSS spacing at `GuidedWizard.tsx:495-498`; (a) and (c) fixed | S | `apps/web/src/guided/GuidedWizard.tsx`, `guided.css` | held Guided tickets (73, 85, 90) edit the same area; still present on main UNMEASURED | B |
| PCOMP-15 | `listControls` rebuilds its input snapshot (8 queries) per call | Backlog | Ticket says fix only if measurement shows; a seat measures first | S to M | `apps/api/src/routes/inputs.ts`, `lifecycle.ts`, `authz.ts` | 77 on `inputs.ts` | B (after 77) |
| PCOMP-21 | Does Route B work on a database at migration 0019/0020? | Backlog | Seat-stack measurement; if it refuses, add the two-step form to DEPLOY.md. Ticket is dated: migrations now run to 0027, state what to measure now | M | `DEPLOY.md`, scratch seat stack, maybe a test under `packages/db/test` | DEPLOY.md is edited often | C |
| PCOMP-26 | Chainguard MinIO digest may vanish (risk a) | Backlog | Check that `cgr.dev/chainguard/minio@sha256:7090...` still resolves anonymously; recovery given if not | S | `scripts/ci.sh`, `compose.yaml` comment | none | C |
| PCOMP-27 | Old root-owned MinIO dev volumes refused by the uid-65532 image (risk b) | Backlog | Reproduced by B281; add a preflight or clearer failure text naming the documented recovery | S | `scripts/ci.sh` or `scripts/up.sh`, `compose.yaml:125-126` | 26 | C |

### Lanes (PCOMP)

- Lane A, PDF footer and cover: 23, 123, 82. Files `document-pdf.ts`, `pdf-fit.ts`, `change-report.ts`, brand-profile migration, `api-contract`. Order 23, 123, 82 (migration last). Opus (PDF layout needs independent measurement, migration is deploy-bearing). Needs Tuesday's conflict plan against held PR #85 before start.
- Lane B, web and API polish: 75, 77, 15. Files `apps/web/src/guided/*`, `apps/web/src/screens/w2/*`, `apps/api/src/routes/inputs.ts`. Order 75, 77, 15. Sonnet.
- Lane C, stack and deploy hygiene: 26, 27, 21. Files `scripts/ci.sh`, `scripts/up.sh`, `compose.yaml`, `DEPLOY.md`. 21 takes the heavy lock. Sonnet.

### Excluded (PCOMP, 80)

- Epics (4): PCOMP-1, 2, 3, 4.
- Held label (19): 19, 20, 68, 69, 70, 71, 72, 73, 76, 79, 84, 85, 86, 87, 88, 89, 90, 91, 92.
- Waits on Kam (2): 46 ("warn, never block" confirmation open, C-89), 94 (Kam sends the reviewer questions himself).
- Needs ruling (14): 9, 11, 13, 29, 74, 80, 81, 83, 98, 116, 127 (waits on a go; item 1 a gawk measurement is buildable once a go is given), 38 and 52 (new words need a words card), 65 (optional ruling).
- Blocked by another ticket or by held PR #85 (24): 31, 32, 33, 34, 35 (wait on 29), 36, 37, 39, 55, 56, 57, 58, 66, 67 (L1 loader on PR #85), 44, 45, 47, 48, 49, 50, 51, 53, 54, 60 (need L1 to L4 first). Note: 36, 37 and 39 data files are disjoint from the loader per C-92 and could be built on branches; excluded here because they feed the held loader. 44 (contract enums) is buildable alone but has no consumer.
- Not agent work, human or other project's VM or deploy (15): 5, 6, 7 (superseded guide), 8, 10, 12 (merged; close is coordinator's), 16, 18, 25, 28, 59, 61, 78, 93, 64 (nothing to write).
- Partly merged, stale or unclear (2): 41 (clause 2 needs held content release), 42 (likely built in migration 0025; ticket text stale, UNMEASURED).

(Counts in this exclusion list follow the sub-sweeper's own assignment; its program check was union 89 = jqdump count. Re-run the union check before relying on per-class counts.)

---

## 3. MPS Commercial Calculator (Jira MPSCALC)

Open: 214 (jqdump COUNT; all Backlog; 198 Task, 15 Epic, 1 Bug by the sub-sweeper's tally; its union of 214 keys matched the dump). Live state: no open PRs; the ten `b14*` branches are leftovers of squash-merged PRs (compare main...branch: diverged, 1 to 6 ahead, 9 behind; b14b 1 ahead, 158 behind); origin main `54ed7627` (#175, merged 2026-11-10). Only seat today R208 (records, B1488) finished with no code push. Pricebook values are confidential: no price value may enter any ticket text, lane brief or this file.

### Actionable (43)

| key (MPSCALC-) | title (short) | why actionable now | size | files | conflicts | lane |
|---|---|---|---|---|---|---|
| 135 | e2e smoke journey red | Fix shape in ticket (CSS-free modules, synthetic-store leg) | M | `web/e2e/smoke.spec.ts`, `web/playwright.config.ts`, `.github/workflows/ci.yml` | 96 and 297 wait on it; `ci.yml` with 251, 57 | L1 |
| 96 | e2e stub-mode specs red | Clause 3 needs 135's load fix plus an independent run | S | `web/e2e/b28.spec.ts`, `b30.spec.ts`, `bom.spec.ts` | after 135 | L1 |
| 297 | e2e nav and Proposal locator | Release is 135's change plus a run at both widths | S | `web/e2e/` nav and proposal specs | after 135 | L1 |
| 251 | zero uncaught errors on first load | Visits after sign-in; spec must run in CI | M | `web/e2e/` first-load spec, `ci.yml` | `ci.yml` | L1 |
| 57 | customer-safe leakage tests | Run the PDF-text leakage spec in CI | M | `ci.yml`, `web/e2e/proposal-*.spec.ts` | `ci.yml` | L1 |
| 111 | proposal 390 px scroll | Merged in #48; clause 4 needs the 390 px e2e green | S | `web/src/proposal/proposal.css`, `web/e2e/proposal-buttons.spec.ts` | `proposal.css` with 130 | L1 |
| 185 | 390 px home dashboard check | Clause 2: the home half has no check | S | `web/e2e/b100-quote-390.spec.ts` | none | L1 |
| 139 | info hints (i) button | Missing axe check (clause 4) buildable; words approval (clause 5) not, so ticket stays open | S | `web/e2e/b100-info-hints.spec.ts` | none | L1 |
| 198 | fleet grid line identity e2e | Add e2e on a stored [1,1] quote | M | `web/e2e/` fleet spec | after 135; beside 170 | L1 |
| 334 | dev stub and e2e leftovers | Stub unit tests, bundle-check key, e2e halves | M | `web/src/api/stub/`, `web/scripts/check-bundle.mjs`, `web/e2e/` | after 135 | L1 |
| 121 | feedback form wedges on an unreadable file | Fix shape given (per-add promise) | S | `web/src/feedback/attachments.ts`, `FeedbackDialog.tsx`, tests | none | L1 |
| 130 | printed proposal books inherit app table styles | Print CSS only, word sets stay equal to mock; closes duplicate B93-N2 | M | `web/src/proposal/proposal.css`, `rental-book.css`, `one-pager.css`, `styles.css` | `proposal.css` with 111 | L1 |
| 369 | web tests time out under load | Tests only; 3 of 5 clauses met; needs 20 whole-suite runs above load 7 | M | web test files | none | L1 |
| 377 | quantity audit tests | Test only | S | `web/src/screens/bom/QuantityAudit.severalDevices.test.tsx` | none | L1 |
| 170 | stable fleet line id and price audit | Needs a stable line id in the contract; check whether the contract change counts as a decision (ticket does not say a ruling is needed) | L | `src/MpsCalc.Api/Quotes/PriceAudit.cs`, `web/src/screens/bom/PriceAudit.tsx`, `docs/api/openapi.json` | 198 (same grid) | L1 |
| 122 | feedback download refusal headers | Add hosted test rows for 400/500/503 | S | `tests/MpsCalc.Api.Tests/FeedbackDownloadHeaderTests.cs` | none | L2 |
| 123 | feedback upload memory and concurrency | Build the streaming option; the setting-bound alternative is the coordinator's call | M | `src/MpsCalc.Api/Feedback/FeedbackEndpoints.cs`, `FeedbackAttachments.cs`, `FeedbackStore.cs` | after 122 | L2 |
| 99 | source lifecycle blocks a pool thread | Clause 3: count the stage wait bound from arrival | M | `src/MpsCalc.Api/Sources/SourceLifecycle.cs`, `SourceAdminEndpoints.cs`, tests | near 217 | L2 |
| 98 | overlay writer queue order test | Run both tests under the arrival-order mutant, record the run | S | `tests/MpsCalc.Api.Tests/OverlayQueueTests.B105.cs`, `CatalogueOverlayStore.cs` | 163 | L2 |
| 163 | overlay Busy bound under load | Clause 3: 20 group runs green under load | M | `Overlay*Tests`, `CatalogueOverlayStore.cs` | 98 | L2 |
| 217 | reference store loads lazily | Clause (b): repeated supply row still served; refuse start or answer 503 | M | `src/MpsCalc.Api/Sources/ActiveSources.cs`, `src/MpsCalc.Import/Store/ReferenceStoreDocument.cs`, `StoreLoadRows*.cs` | 324 tests adjacent | L2 |
| 324 | four survivors of PR #102 | Independent review running mutants S7, S8, S9 | S | `tests/MpsCalc.Api.Tests/BodyRefusedLastBranch.cs`, `StoreLoadFaultMapping*.cs` | 217 | L3 |
| 325 | draft-validation walks grow unbounded | Cap is on main; needs an independent GO review | S | `PurchaseValidation.cs` tests | 338, 339 | L3 |
| 338 | BOM per-line walks | Cap on main; red-first claim relayed twice; review | S | `PurchaseValidation.cs` tests | 325, 339 | L3 |
| 339 | supplies-null walk unmeasured | Answer-size assertion, then review | S | `PurchaseValidation.cs` tests | 325, 338 | L3 |
| 333 | draft-save refusal order pins | Clauses 1 to 3 need a fresh review; 4b an independent run | M | `QuoteEndpoints.cs` tests | none | L3 |
| 331 | governed validate server error | Residue after null guards (PR #110) | M | `src/MpsCalc.Import/Validation/ReferenceDocumentValidator.cs`, tests | 340, 341 | L3 |
| 340 | validator supply-group key | Test-only fix; review or stamped reading | S | `ReferenceDocumentValidatorSupply*Tests.cs` | 331, 341 | L3 |
| 341 | edges file assertions | Re-run the mutants independently | S | `ReferenceDocumentValidatorTests.cs` | 331, 340 | L3 |
| 207 | parity proof blind to mis-bounding | Release needs a stamped cap reading or independent GO | M | importer prove step, `PanelSectionEndTests.cs` | 302 | L3 |
| 302 | prove says AGREE for a tamper | Same release path as 207 | S | importer prove step | 207 | L3 |
| 160 | partner referral rebate default 7% | Clause 6: server half for callers without per-quote pricing rights | M | `src/MpsCalc.Api/Quotes/*`, `docs/ENGINE.md` | `ENGINE.md` with 147, 196; engine with 158 | L4 |
| 158 | supplies margin target click price | Two follow-up tests never re-run by a gate; review | M | engine and Api target tests | 160 | L4 |
| 147 | Customisation class | Clause 2b: calculation-register row in `docs/ENGINE.md` | S | `docs/ENGINE.md` | 196, 160 | L4 |
| 196 | purchase page estimates | Clause (d): register row X-33 never written | S | `docs/ENGINE.md` | 147, 160 | L4 |
| 200 | importer coverage table | Counts only from the local store, no values; whether the store holds both books UNMEASURED | S | `docs/IMPORTER.md` | none | L4 |
| 126 | deploy script rc 0 before start proven | Fake-az regression test specified in ticket | M | `scripts/deploy-from-ci.sh`, `scripts/lib/kudu.sh`, `scripts/tests/fakes/az`, `scripts/tests/test_scripts.py` | 203 | L5 |
| 203 | deploy overlay copy | Open half in `scripts/deploy-from-ci.sh`; drafted, not built | M | `scripts/deploy-from-ci.sh`, `scripts/tests/test_deploy_pre1.py` | 126 | L5 |
| 119 | infra tests az bicep fallback | PR #169 follow-up: `validate.sh`, `README.md:22` still offer the failing route | S | `infra/scripts/validate.sh`, `infra/README.md` | none | L5 |
| 201 | Entra app script follow-ups | Acceptance met; add read-back and a row | S | `scripts/entra_apps.py`, `scripts/tests/test_entra_all_roles.py` | none | L5 |
| 223 | runbooks look in the wrong log | Read the docker log, which works at both deploys; runbook path unlocated | S | deploy runbooks (UNMEASURED) | none | L5 |
| 173 | demo loader dry-run | Clause 2: dry-run mode and test; clause 1 (seed identity) is the coordinator's | M | `tools/demo/seed.py`, `tools/demo/test/test_seed.py` | none | L5 |
| 349 | Api csproj comment example | Comment-only; needs an SDK that carries the tie (UNMEASURED) | S | `src/MpsCalc.Api/Api.csproj` lines 31 to 34 | none | L5 |

### Lanes (MPSCALC)

- L1, web e2e, print CSS, web tests (15): 135, 96, 297, 251, 57, 111, 185, 139, 198, 334, 130, 121, 369, 377, 170. Files `web/e2e/**`, `playwright.config.ts`, `ci.yml`, `web/src/proposal/*.css`, `web/src/feedback`. Order 135 first, then 96, 297, 251, 57, then 111, 185, 139, 198, 334, then 130, 121, 369, 377, 170 last. 111 and 130 share `proposal.css`: one seat. If too long, split L1b = 121, 130, 369, 377. Sonnet; Opus for 170.
- L2, Api stores (6): 122, 123, 98, 163, 99, 217. Files `src/MpsCalc.Api/Feedback`, `Sources`, `Inventory/CatalogueOverlayStore.cs` and tests. Order 122, 123, 98, 163, 99, 217. Sonnet.
- L3, validation rows and independent verification (10): 325, 338, 339, 333, 324, 331, 340, 341, 207, 302. Files `PurchaseValidation` tests, `ReferenceDocumentValidator` tests, importer prove tests. Mostly test rows and verifier runs. Sonnet; Opus for the independent reviews. 217 (L2) sits beside 324 (L3) in the StoreLoad test files: sequence them.
- L4, engine and docs (5): 147, 196, 160, 158, 200. Files `docs/ENGINE.md`, `src/MpsCalc.Api/Quotes/*`. Opus for 160 and 158, Sonnet for the doc rows.
- L5, ops tooling and demo harness (7): 126, 203, 119, 201, 223, 173, 349. Files `scripts/deploy-from-ci.sh` (126 and 203 share), others disjoint. Nothing deploys; no `az` needed. Sonnet.

### Excluded (MPSCALC, 171)

Reason counts from the sub-sweeper's union check (214 = 43 + 171).
- Needs ruling or product words (45): 91, 103, 109, 110, 112, 113, 114, 115, 117, 120, 128, 129, 131, 132, 150, 153, 156, 157, 159, 161, 169, 177, 189, 194, 195, 202, 222, 226, 229, 233, 261, 288, 295, 306, 310, 314, 316, 342, 364, 368, 371, 380, 381, 382, 383.
- Held, or waits on a person, deploy or hosted data (11): 118, 124, 133, 140, 144, 155 (waits for the reviewer's staging details), 162, 187, 188, 224, 372.
- Blocked by another ticket (2): 212 (needs 286 and 287), 236 (needs 237).
- Later phase (5): 149, 152, 154, 181, 260.
- HTML phase, the unbuilt v13.4.1 `lane-v*` tickets (34): 237, 243, 244, 245, 246, 248, 258, 264, 265, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 315, 358, 359, 360. READING CAVEAT: "HTML phase" is defined for HPSM-POC in the order; the sub-sweeper found no such term in MPSCALC records and read it as the v13.4.1 HTML pack. Server-side keys 237, 284, 285, 286, 287, 258, 358, 359, 360 would be actionable if Kam's hold covers only HPSM-POC. Tuesday to confirm.
- Epics, spec-seed umbrellas, Q-questions for Kam (74): 1 to 15 (epics); spec-seed umbrellas 16, 17, 18, 19, 20, 23 to 36, 40 to 54, 55, 58, 59, 60, 62 to 65 (large features or human-owned or ruling-bound; 64 contains an accessibility remainder that could be agent work); question-for-Kam tickets 68, 69, 70, 72 to 80, 82, 83, 85, 87, 88.

---

## 4. NexusAI (Jira RD)

Open: 853 (jqdump per status: To Do 391, Testing 246, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2; sum 853). Release Ready and Testing (445) are not work (JIRA.md flow To Do, In Progress, Testing, Release Ready, Done, as read by the sub-sweeper) and were not read individually; types by program: Release Ready 118 Bug, 73 Task, 8 Story; Testing 122 Bug, 110 Task, 14 Story. All 391 To Do titles and all 17 In Progress, Put on Hold and Declined titles were read; deep reads (about 190 last comments, about 45 descriptions) are the sub-sweeper's own tally, not program-measured.

Landing chain and live branches (gh `matching-refs/heads/b14` plus `compare/main...<branch>`, 12 pushed `b14*` branches; main now `0ab365b1`, past the `849b808c` the handovers cite):
- Already merged, so their tickets are records-only: `b1431/nexusai-t-ci-actions-browser-assert` (RD-605, RD-544), `b1432/nexusai-f-overflow-settings-390-printing-820` (RD-962, RD-963), `b1432/nexusai-f-shell-layout-header` (RD-979), `b1433/nexusai-b-csp-intake-edges-and-typed-fields` (RD-759 shapes 1 and 2, RD-796), `b1433/nexusai-b-learning-manager-log-lines` (RD-798, partly).
- Unmerged, so in the chain, excluded (7 branches): `csp-tool-edge-cases` (RD-970, 971), `smtp-route-cells-standalone` (RD-720), `suites-pass-from-git-archive` (RD-731), `b1480/l1-design-inventory` (RD-929, 977, 978), `session-revocation-clarification` (RD-972, 976), `viewer-write-gates` (RD-958, 793), `setup-column-mapping` (RD-967). All diverge from main by 17 to 19 commits.
- Still open on main `0ab365b1` (program reads with controls): `static/login.html` still carries the 40-character SRI hash on bootstrap-icons (RD-475/560 real); `static/index.html` has `role="tablist"` count 0 with control `tab-button` 10 (RD-144 real); `cdn.jsdelivr.net` 4 hits in `index.html`, 3 in `settings.html` (RD-145 real); 64 open code-scanning alerts on main, the set the CodeQL-baseline tickets (RD-762 to 773, 804 to 810) describe.

Lane continuity: lane T stopped before RD-730 (three tickets built but unpushed in `.tools/b1431/wt-*` worktrees: RD-730 `0a19a33`, RD-749 `8579fac`, RD-729 `977470c`; RD-749's mutant M-B6 unbuilt because its gate report is unreadable). Lane F built through RD-962/963/979, next RD-144. Lane S next RD-969; RD-930, 931, 932, 964, 965, 966, 968 held for rulings. Lane B has four local-only built branches never given a full-suite run (RD-576, 590, 826 items 1 and 2, 805; RD-805 is a real red whose carrier gate lists `backend/routes/entraProvisioning.js` as not reviewed).

`scripts/verify-expected-counts.json` is touched by every branch and regenerated by Tuesday at landing (not repeated below).

### Actionable (about 104 keys)

Lane S, server (owns `backend/server.js` and friends). Conflicts for ALL rows: viewer-write-gates, colmap and revoke branches all touch `server.js`; stack on `2a584f7` or wait for the chain to land.

| key | title (short) | why now | size | files |
|---|---|---|---|---|
| RD-969 + 563 + 691 | Three routes 500 on empty request; agent route partial write; retire agent route | Red-first case given (400 on bad input); retiring the route makes 969's agent part moot | M | `backend/server.js` (~20397, ~20677, ~19095), `docs/role-capabilities.json` |
| RD-974 | Undated job stamped "now" in unusual-print-times | Recommendation and red-first given | S | `backend/server.js` |
| RD-975 | Business-hours report reads `created_at` first | same | S | `backend/server.js`, `backend/simpleDb.js` |
| RD-926 | AI answer logged raw (6068, 6169) | Pass through `logSafe` as PR 172 did | S | `backend/server.js` |
| RD-772, 773, 770 | CodeQL incomplete-sanitization, loop-bound, URL substring | Fix shapes given; never dismiss; CodeQL closes on merge | S each | `backend/server.js` (:11234, :7850, :6049) |
| RD-765 | CodeQL polynomial-redos (email regex) | One linear check | S | `backend/server.js`, `ticketStore.js` |
| RD-766 | CodeQL polynomial-redos x10 (AI query pipeline) | Cap query length, rewrite patterns, one cell each | M | `backend/intentRouter.js`, `queryPreprocessor.js`, `server.js` |
| RD-762 | CodeQL missing-rate-limiting x7 | Mount one page-route limiter | M | `backend/server.js` (:1557 on) |
| RD-767, 768 | CodeQL file-system-race x3, insecure-temp-file x3 | Open once and act on the descriptor; `mkdtemp` | M each | `backend/costCentreMap.js`, `jsonStorage.js`, `services/emailService.js` (`jsonStorage.js` also in the revoke branch) |
| RD-769 | CodeQL remote-property-injection x5 | Null-prototype stores plus key guard | L | `jsonStorage`, `marketplaceStore`, `server`, `validators` |
| RD-763, 764 | CodeQL missing-token-validation, user-controlled-bypass | Judgement tickets: read first, fix or record the reading for Kam; no ruling needed to start | M each | `backend/server.js` (login, OAuth, register, AI-skip) |
| RD-711 | SIGTERM tears `audit-buffer.json` (High) | Real bug, no ruling cited | M | `backend/server.js` |
| RD-830 | Non-GUID `workspaceId` stored and queried | Scope widened per Tuesday's answer | M | `backend/server.js` (~:1709, ~:17090) |
| RD-893 part 2, RD-896 | Risk-condition field checks; mixed-case `risk_level` | Part 1 landed | S each | `backend/jsonStorage.js`, `server.js` |
| RD-820 | AI-off gate has no test cell | Test only | S | `backend/server.js`, tests |

Lane B, backend periphery (no `server.js`):

| key | title (short) | why now | size | files / conflicts |
|---|---|---|---|---|
| RD-455 | SCIM mapping save refused without a new token | Real bug, measured twice | M | `backend/routes/entraProvisioning.js`, `services/entraProvisioning.js`; with RD-805 |
| RD-805 | CodeQL file-access-to-http x8 | Local branch `942204d1` is red; needs a carrier-gate review-list entry then re-run | M | five backend files |
| RD-804 | CodeQL file-access-to-http alert 142 open | 4 of 5 alerts already read fixed | S | `backend/azureLogAnalytics.js` (:798) |
| RD-798 remainder | Two log lines in `learningManager.js` (alerts 152, 153) | Rest landed in PR 182 | S | `backend/learningManager.js` (:125, :153) |
| RD-744 | Re-drive certifies "purged" after a hard-link refusal (High) | Real bug | M | `backend/dataErasure.js` |
| RD-745, 750, 824 | Erasure path normalisation, ledger duplicate, link errors | Real bugs | S to M | `backend/dataErasure.js`, `Dockerfile` (745 only; the Dockerfile is lane T's) |
| RD-728 | Golden-blob cell false-red when env vars are set | Scrub the two env vars | S | `backend/encryptionService.js`, tests |
| RD-576, 590, 826 (items 1, 2) | Built locally, red-first proven, no full-suite run | Run the full suite, push | S each | per the B1433 worktrees |

Lane F1, first-run, login, settings pages:

| key | title (short) | why now | size | files / conflicts |
|---|---|---|---|---|
| RD-475 + 560 | Login page SRI hash truncated | One fix for both; open on main | S | `static/login.html` |
| RD-117 + 188 + 176 | First-run CSP-blocked inline styles | One class-move; fix shape given | M | `static/first-run-setup.html`, `static/js/first-run-setup.js`, `static/js/entra-provisioning-ui.js`, `scripts/refactor-inline-styles.js` (the csp branch RD-970 edits that script: do not touch it) |
| RD-189 | `checkEntraStatus` null-property TypeError | Guard the lookup | S | `static/js/first-run-setup.js` (shared with 492, 456, 808) |
| RD-492 | Step-3 Enforce shows an error on success | Restore `#enforce-auth-card`; real-browser cell asked | M | `first-run-setup.html`, `first-run-setup.js` |
| RD-456 | Re-saving the AI step turns AI back on | Real bug | S | same |
| RD-481 | Trailing-slash pages load no assets | Fix relative asset paths | S | `static/login.html`, `first-run-setup.html` |
| RD-808 | CodeQL identity-replacement (no-op replace) | Both candidate forms listed | S | `first-run-setup.js` (:383) |
| RD-371, 373 | Revoke UI date, live region, focus; revoke warning covered | Live-region half is on a branch not on main (UNMEASURED if it lands) | M | `static/js/entra-provisioning-ui.js` |
| RD-151, 416, 540, 687, 396 | Inline cost errors; first-run polish; test cell; dead branch; red-flag toggle | Each has a clear fix | S to M | `static/settings.html`, `static/js/settings.js`, `first-run-setup.js`; 396 also `backend/services/riskAlertScheduler.js` |

Lane F2, dashboard, CSS, front-end tests:

| key | title (short) | why now | size | files / conflicts |
|---|---|---|---|---|
| RD-144 | Dashboard tab strip has no ARIA tab semantics | Next in lane F; open on main | M | `static/index.html`, `static/js/index.js` (with RD-351, same tab strip) |
| RD-145 | Vendor the CDN assets into the image | Open on main | L | all `static/*.html`, vendor files, `Dockerfile` (lane T's: coordinate or give T the Dockerfile edit); run last |
| RD-164, 175, 222 | Dark-mode contrast (borders, toner text, wizard chip) | Contrast numbers measured; RD-175 build the dark half only (light half needs a design choice) | S to M | `static/css/dark-mode.css`, `index-styles.css`, `first-run-setup-styles.css` |
| RD-220, 259, 261 | Dashboard console errors; brand-button fallback guard | Investigation and fix | M | `static/js/index.js`, `static/css/brand-buttons.css` |
| RD-483, 613, 832 | Banner offset; wipe alarm only on the dashboard; admin 403 logs | Small UI fixes | S each | `static/*.html`, `static/js/index.js`, `admin.js` |
| RD-835, 861 | CSV formula injection; remaining HTML-written fields | Real security hygiene | M | `static/js/index.js`, `settings.js`, `first-run-setup.js`; RD-861 after F1 |
| RD-771 | CodeQL incomplete-url-substring x4 | One hostname-suffix helper | S | `static/js/index.js`, `settings.js` (settings.js is in F1) |
| RD-512, 513, 515, 538 | Banner-guard coverage gaps | Test-only with stated red cells (RD-514 needs a decision, excluded) | S each | `tests/e2e/open-access-banner-guard.js`, `__tests__/rd490-open-access-banner-browser.test.js`; RD-515 also `first-run-setup.html` (F1) |

Lane T, tooling and tests:

| key | title (short) | state | size | files / conflicts |
|---|---|---|---|---|
| RD-730, 749, 729 | Finish built local branches | Built, unpushed; verify and push; RD-749 M-B6 blocked on its report | S each | `__tests__/handover-gate-table.test.js`, `rd684-redrive-keeps-surviving-target.test.js`, `rd648-harness-boot-residuals.test.js`, `__tests__/helpers/rd395-server-harness.js` (RD-729's harness is used by 43 suites: full verify) |
| RD-757 | Stand-in counts a foreign dial (High) | not started | M | `__tests__/helpers/test-server.js` (RD-740 shares the stand-in) |
| RD-734, 345, 352, 355, 378, 379, 384 and "395-class" tidy-ups | Test-only residues | red-first or record fixes | S each | named `__tests__` files; none touched by a live branch |
| RD-134 | Scheduler test coverage (12 schedulers) | loader blocker solved | L | `__tests__/` |
| RD-249, 353, 394, 397, 580, 586, 348, 668, 829, 918(a) | Script and CI fixes | Real bugs; RD-918(b) already answered by PR 155 | S to M | `scripts/*`, `.github/workflows/build.yml`, `Dockerfile` (397, 918): one owner |
| RD-320, 387, 426, 539, 566, 572, 595, 597, 599, 600, 623, 726 | Guard and cell residues | Test-only; RD-566's B-3 merged, B-1 and B-2 remain | S each | `__tests__/helpers/*`, named test files |
| RD-980 | Log-sink test files | WAIT for the revoke branch (it rewrites two cells in rd798/rd799) | S | `__tests__/rd798-*`, `rd799-*` |

### Lanes (NexusAI)

1. Lane S: owns `backend/server.js`, `jsonStorage.js`, `simpleDb.js`, `intentRouter.js`, `queryPreprocessor.js`, `ticketStore.js`, `costCentreMap.js`, `docs/role-capabilities.json`. Order 969/563/691, 974, 975, 926, 772, 773, 770, 765, 766, 762, 767, 768, 769, 763, 764, 711, 830, 893/896, 820. MUST wait for the B1484 chain or stack on `2a584f7`. Any new handler gate needs the inventory regenerated from a non-dot tree. Opus for the CodeQL set and RD-711, Sonnet for the rest.
2. Lane B: owns `backend/**` not in S. Order 804, 798 remainder, 455+805 together, 744, 745, 750, 824, 728, then the four local branches (576, 590, 826, 805). Sonnet; Opus for RD-744.
3. Lane F1: owns `static/{login,first-run-setup,settings}.html` and `static/js/{first-run-setup,settings,entra-provisioning-ui}.js`. Order 475/560, 189, 456, 492, 117/188/176, 481, 808, 371/373, polish. Sonnet.
4. Lane F2: owns `static/index.html`, `static/js/{index,admin,chart-details}.js`, `static/css/**`, `tests/e2e/**`. Order 144, 164/175/222, 261/259/220, 483/613/832, 835, 771, 861, banner-guard tickets; RD-145 last (needs `Dockerfile`). Sonnet.
5. Lane T: owns `scripts/**`, `.github/**`, `docs/**` (less the role-capability files), `__tests__/**` not listed above, `Dockerfile`, `package.json`. Order finish 730/749/729, 757, small residues, 134. Sonnet.

Cross-lane exceptions: RD-771 and RD-861 touch F1's `settings.js` (sequence after F1); RD-145 and RD-745/397/918 need the `Dockerfile` (lane T owns it; give the edit to T).

### Excluded (NexusAI)

- In a live lane or the landing chain: RD-970, 971 (csp-tool-edge-cases); RD-720 (smtp-route-cells-standalone); RD-731 (suites-pass-from-git-archive); RD-972, 976 (session-revocation-clarification); RD-929, 977, 978 (l1-design-inventory); RD-958, 793 (viewer-write-gates); RD-967 (setup-column-mapping); the rd407-r2 fix (B1492 pane).
- Landed on main, awaiting records only: RD-962, 963, 979, 605 (deploy-demo.yml item is a HOLD), 544, 796, 759 shapes 1 and 2, 798, 892, 893 part 1, 498 (merged at `f1319ac`), 312 (already fixed on main per lane B handover); RD-799, 800, 959, 960, 961, 973 are no longer To Do (now Testing).
- Held or needs ruling: RD-930, 931, 932 (scope model absent); 964, 965, 966, 968 (recommendation says decide); 958 part 3; 810; 433 (SEED_DEMO_DATA guard would break the demo env); 305; 583, 584 (deferred by ruling, blocked on RD-574); 674; 759 third shape (`data:` payload); 610, 612, 622 (needs-decision); 644, 858, 883, 884, 888, 522, 546, 193 (product or policy choice); 349 (brand ruling); 722; 532; 514; 911; 854 (blocked on RD-884); 908; 313; 740 (cause undetermined); 146, 400, 401, 842 (feature requests); 702, 636 (customer-facing wording).
- Roles UI chain: RD-937 to 957 (21, behind the L3 shell, held on word rows); 934, 935 (policy, no build); 933 (design-first, partner delegation); 928, 936 (landed, awaiting records).
- Not agent work: RD-6, 7, 8, 13, 20, 21, 22, 28, 29, 30, 31, 34 (epics, business, hiring, compliance, Partner Center); 50, 54, 55, 69, 76, 83 (other projects, Azure, secrets); 233, 287, 393, 449, 530, 534, 536, 562, 570, 587 (Jira admin, launcher or session tooling); 738, 739, 742, 827, 886 (process or fleet tooling); 414, 415, 467, 468, 469, 473, 507, 520, 542, 543, 552, 642, 659, 660, 661, 663, 724 (marketplace-labelled, Partner Center); 664, 666, 667, 672, 673 (customer-test items); 479, 480 (backlog-design options). Note RD-577 and 578 are marketplace-labelled but plain code bugs (`KEY_VAULT_NAME` vs `KEYVAULT_NAME`): buildable if Tuesday waives the label rule.
- In Progress, owned by another seat or human: RD-49, 81, 450, 643, 662; RD-427, 431, 432 (stale 2026-09-14 plans, whether they merged is UNMEASURED).
- Put on Hold or Declined: RD-18, 32, 33, 41, 93, 104, 743 (held); RD-300, 564 (declined).
- Not individually examined (UNMEASURED beyond type counts): 445 Testing and Release Ready tickets; about 85 To Do tickets classified from title and the lane-plan excerpt only (mostly lane T and S residues): RD-133, 236, 316, 319, 325, 331, 358, 366, 383, 398, 406, 421, 446, 457, 487, 547, 548, 582, 589, 611, 655, 688, 713, 716, 718, 725, 727, 792, 797, 806, 834, 845, 855, 859, 872, 876, 909, 914, 925, 927, 981 (RD-981 is new, not in the lane TSV). They are plausible second-tier work for lanes S and B; the builders' PRIOR WORK check settles whether each is already partly fixed.

---

## Questions for Tuesday (each with a default)

1. HPSM NEW-1: is a walkthrough step title Kam's script word (needs a card) or a label that follows the menu? Default: treat as following the existing menu label "Delivery phases", no new word.
2. HPSM NEW-2: the fifth unmarked record may be UAT data. Default: lane H-E starts with a read-only diagnosis and reports; no UAT write.
3. MPSCALC: does the HTML-phase hold cover MPSCALC's `lane-v*` tickets? Default: yes, excluded as above; the nine server-side keys (237, 284, 285, 286, 287, 258, 358, 359, 360) are the first to release if the answer is no.
4. PCOMP lane A vs held PR #85 (both touch `document-pdf.ts`): sequence after #85 or accept a rebase. Default: start with PCOMP-123 and PCOMP-23 on a branch and rebase when #85 moves.
5. NexusAI lane S waits for the B1484 chain. Default: start B, F1, F2, T now; S after the chain lands.
6. HPSM records seat: whether to run a records-check pass over the eight "no build left" tickets (99, 178, 431, 323, 343, 117, 100, 315). Default: yes, one records kit.

## Method and disclosures

- Instruments: `jqdump` and `jqget` (Python, Jira REST `search/jql` and `issue`, GET only, 0.25 s apart, credentials read in-process from each project's `4_Credentials/.env`, never printed); `gh api -X GET` under each project's own `GH_CONFIG_DIR`; `git --no-optional-locks` read verbs; `/usr/bin/grep`.
- HPSM-POC: the three-way ticket search for the new findings used `text ~` queries (stemmed, so broad); origin file reads for NEW-1 were `gh api -X GET repos/datasecau/HPSM-POC/contents/<path>` with a grep over the decoded text (hits at the lines named; positive control: "Delivery phases" hit in `ServicesHub.tsx`).
- Outside the one-output-file rule: two helper scripts were written to `/tmp` (`jqdump.py`, `jqget.py`) and some scratch files by sub-sweepers under `/tmp`; none in any project folder, no git ref, no Jira write, no GitHub write. They are removed at the end of this sweep except any a sub-sweeper left (named in its report: `/tmp/pc_open.txt`, `jqv.sh`, `mps_open.txt`, `mps_tree.txt`, `/tmp/ra/`).
- The drafter rules file names `/Volumes/Laptop-DEV`; this drive is `/Volumes/Datasec_DEV`.
- READ-WHOLE-BY-TUESDAY: ____
