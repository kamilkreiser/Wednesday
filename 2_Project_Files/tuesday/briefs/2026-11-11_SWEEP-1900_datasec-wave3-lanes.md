# SWEEP-1900: Datasec wave-3 lanes, tickets agents can build tonight (read-only sweep, 2026-11-11, reads 18:5x to 19:1x AEDT)

Successor to `2026-11-11_SWEEP-1326_datasec-actionable-lanes.md` (read whole; its method and exclusions still apply unless this file says they changed). Written by a read-only sweeper: no Jira write, no git write, no PR, no message. One output file. Scratch only in `/private/tmp/sweep1900/`.

## BLUF

The biggest change since 13:26 is not code, it is rulings. At 14:15 (Composer, 7 recommendations), 14:34 (MPS Calculator, 29 recommendations; NexusAI, 17 recommendations) the product owner accepted the decision registers' recommendations. Each ticket carries a comment saying "ruling recorded; not moved; the work is queued as its own change". Many tickets the 13:26 sweep excluded as "needs ruling" are therefore buildable now. HPSM-POC, in contrast, is nearly drained: its 13:26 lanes are all built (merged or in open PRs #309/#312).

Launch now, in this order (all file-disjoint from each other and from every live lane kit or open PR, except where a conflict is named):

1. **MPS lane W3-A, ruled look and print fixes (Sonnet, M):** MPSCALC-131 (site cards AA, AB), 112 (singular "and 1 more rate"), 113 (home tiles three across), 110 (one-pager held to one page by tighter limits, no new words without the product owner). Files `web/src/proposal/RentalDocument.tsx`, `OnePager.tsx`, `one-pager.css`, `web/src/styles.css`, `web/e2e/home-tiles-fill.spec.ts`; none is touched by branch b1502 (L1, 18 files) or any other live lane. Why first: rulings are quoted and exact, no hosted/deploy involvement, no shared lock, and it is the only MPS web lane free of b1502.
2. **MPS lane W3-B, Api rulings without contract change (Sonnet, M):** MPSCALC-229 (colour rate only for classes with colour pages), 189 (duplicate source id rule, remaining clauses 4-5), 91 (refuse to start when a reference-only store loses its registry). Files `src/MpsCalc.Api/Quotes/Proposal.cs`, `src/MpsCalc.Api/Sources/SourceDocumentChecks.cs` and the Sources store, their tests. Disjoint from L3 (validation tests) and L4 (`docs/ENGINE.md`).
3. **MPS lane W3-C, contract-text and clone/archive (Sonnet build, tier-1 gate, L):** docs first (MPSCALC-316, 120, 364, 371: `docs/API.md`, `docs/api/openapi.json`, generated web types, ruled to be corrected from what the code does, no word review for developer-only text), then code (233 clone refuses an existing reference, 161 archive a quote). One seat because all share `docs/API.md` and `openapi.json`.
4. **Composer (PCOMP) lanes W3-B and W3-C, two small seats or one (Sonnet, S each):** B = PCOMP-74, 80, 81 style leftovers (ruled today: one new named value for the white, round shapes stay, code-style font on the withdrawn setting key), CSS only. C = PCOMP-128 (stale `DEPLOY.md` Route B lines; measured results are in the ticket; 0022 needs a throwaway-database measurement). Disjoint from each other and from held PR #85.
5. **NexusAI lanes F1 and F2 (+B and T), static front end first (Sonnet):** all the 13:26 keys re-checked still To Do and the anchors still open on main `ef068ea0`; F2 gains four ruled items (RD-175, 349 contrast; RD-532 banner above overlay; RD-858 remove the SQL box). They can START now (reading, red-first cells) but every full verify queues on the jest lock behind the B1484 chain (three rows still to land: archive, revoke, l1 after the open smtp PR #193). Lane S still cannot start.

Do NOT launch yet (each has a named gate): MPS deploy-refusal lane D (MPSCALC-103/222/226/202/224) until M119 (L5) lands, because it shares `scripts/deploy-package.py`/`test_deploy_pre1.py`; MPS PriceView/usage items (128, 150) and L1 residue until b1502 lands (shared `PriceView.tsx`, `PurchaseBomEditor.tsx`); Composer PDF lane (PCOMP-23, 123, 52, 82) is in direct file conflict with held draft PR #85; NexusAI lane S.

HPSM-POC: no build seat is worth launching (2 low-value items, both with a caveat). The useful HPSM work is a records pass for #310/#311 (and for #309/#312 when they merge).

Counts (instrument `search/jql`, predicate `project = <KEY> AND ( statusCategory != Done )`, paginated to the last page, key set de-duplicated): HPSMPOC 131 (was 140), PCOMP 81 (was 89), MPSCALC 196 (was 214), RD 851 (was 853). Details in Method.

---

## 1. HPSM-POC (Jira HPSMPOC)

Open: 131 (128 Backlog, 3 In Progress; 120 Task, 10 Epic, 1 Sub-task). Origin main `448dc395` (2026-11-11T07:39Z). Open PRs (`gh api -X GET repos/datasecau/HPSM-POC/pulls?state=open`): #309 (11 files: `ApiSteps.tsx`, `FindingDetail.tsx`, `PlaybookShell.tsx`, `steps.ts` and their tests, one e2e), #312 (4 files: `remediation-store.ts`, `RoadmapScreen.tsx`, tests). Merged since 13:26: #310 (Pkcs pin), #311 (shell look fixes, focus-ring radius, CI-reader pins; 7 files).

What the 13:26 lanes became, read from the lane STATUS files in the project's `1_Project_Definition/Briefs/`:
- H-A (B1497) = PR #309: HPSMPOC-461, 432, 409 item 2, 468 (the step 12 title). CLOSED-WITH-EVIDENCE as already met on main: 439, 357 (mock half), 399 clauses B908-4 and B908-7.
- H-C (B1496) = PR #312: HPSMPOC-408 part (a) only. 228 N-5 and 436 were found already on main (PRs 298 and 302): not work.
- H-B and H-D (B1503) = merged PR #311: 406 item 4, 465, 462 (focus-ring), 356 B734-6. 356 B734-9 closed with evidence.
- NEW-1 became HPSMPOC-468 (in #309); NEW-2 became HPSMPOC-469 (the diagnosis was in the B1497 kit; not a PR file, so it is a decision item for the owner: kept, marked or removed).

### Actionable now (2 low-value items)

| key | short title | why actionable | size | files (confirmed on main by tree read) | conflicts | lane |
|---|---|---|---|---|---|---|
| HPSMPOC-405 | Fixed Feedback pill sits over a list page's only row button at 768 x 1024 | The 2026-11-02 record says the Customers and Workspace lists were fixed at full scroll only; not-at-full-scroll overlap measured open (1386 px squared at 768x1024). B1503 did not touch it. CAVEAT: the ticket says "which fix is built is a scope call"; the pill's place was ruled (entry C-42). Default: build only a shell safe area (room), pill stays where it is. | S | `web/src/components/shell/AppShell*.tsx`, `web/src/components/feedback/FeedbackButton.tsx`, `FeedbackPill.module.css` | none with #309/#312 (neither touches shell or feedback) | H-F |
| HPSMPOC-356 | `test_ci_workflow.py` residue after B734-6 | Test-only; B1503 bounded B734-6 and listed what is still unread (`GITHUB_ENV` appends in `run` bodies, `if:` conditions, `runs-on`, `with:` values). Diminishing return: each added pin is a reader row; no defect is known. | S | `infra/tests/test_ci_workflow.py` | none; drafter rule 8 (the infra job runs in the gate) | H-F |

H-F = one seat, 405 then 356 (Sonnet, S, pairs with a records seat). My recommendation: skip 356 unless a seat is idle.

### Excluded (summarised; the 13:26 classes still hold)
- Built and waiting on PR landing: 461, 432, 409, 468 (#309); 408 part (a) (#312; part (b) needs the owner's words).
- Held for the product owner (do not list): every item of the v2.1 HTML phase decision document: 448 to 460, 463, 464, 368, 370, 390, 392, 393, 394, 396, plus 457 and the partner dashboard rebuild items; 406 items 2, 3, 5 (item 5 "waits for a ruling" by its own text); 228 N-7 second half (words); 420, 467, 469 (decision per surface / kept-marked-removed).
- HP-tool integration or HP-owned: 82-86, 97, 166, 167, 181, 241, 191, 220, 240, 47, 48, 94, 46, 259, 92, 96, 173, 162-165, 168.
- Deploy, hosted measurement, VM: 126, 196, 207, 234, 235, 309, 303, 428, 362, 304, 57, 60, 62-64.
- Rulings or SOW paperwork: unchanged from 13:26.
- Records closings with no build left (a records seat must verify): 99, 178, 431, 323, 343, 315 (CI re-run of the SQL Server shard is NOT RUN), 117 and 100 (updated 2026-11-11 07:46Z already).
- Epics: 1, 10, 18, 23, 30, 38, 45, 50, 56, 448.
- Per-class counts for today's 131: UNMEASURED (no program assigned each key to one class this time; the 13:26 per-class program covered the 140 then open). Spot reads only.

### Records owed (HPSM)
Landed #310 and #311 are not on the tickets (Jira `updated` stamps: 462 and 465 11-10; 406, 399 11-04; 356 10-27; 439 11-03; 357 11-01; 228 11-06; 436 11-03). Owed on the Jira/records side: 462, 465, 406 item 4, 356 (B734-6, B734-9), plus the closed-with-evidence set from B1496/B1497/B1503 STATUS (439, 357, 399 B908-4/-7, 228 N-5, 436). #309 and #312 add 461, 432, 409, 468 and 408(a) after they merge. #310 names HPSMPOC-254/271 in its kit (neither is in today's open set).

---

## 2. Security Composer (Jira PCOMP)

Open: 81 (all Backlog; 74 Task, 4 Epic, 3 Bug). Origin main `879facda` (PR #124 merged 17:36 AEDT). Open PRs: #85 (draft HOLD K6, 57 files incl. `packages/renderers/src/document-pdf.ts`, `pdf-fit.ts`, `document.ts`, `policy-document.ts`, `test/b59-policy-pdf-cover.test.ts`), #86 and #91 (Dependabot). No lane seat in flight (B1495, B1504, B1506 delivered; their PRs #122, #123, #124 merged).
Rulings, from `CLARIFICATIONS.md` C-140 to C-145 (newest last in this file): 2026-11-11 14:15 "Accept all 7 quick recommendations" (PCOMP-11, 52, 98, 116, 127, 74, 80, 81 comments) and 16:31 rulings (PCOMP-21, 77, 15).

### Actionable now

| key | short title | why actionable | size | files | conflicts | lane |
|---|---|---|---|---|---|---|
| PCOMP-74 | Hard-coded white to one named style value; round shapes (50%, 999px) stay | Ruled 14:15: "the white literals become one new named style value, approved by this note". Radius half already done. Own change, own review. | S | `apps/web/src/styles/app.css` (`#ffffff` literals; radius lines 441.. already tokenised) | shares the new value with 80 | W3-B |
| PCOMP-80 | Same named value in the Expert screens | Ruled 14:15: same named value; round shapes stay | S | `apps/web/src/styles/screens-w1.css` (`.w1-disc`, `.w1-icon-disc`), `screens-w2.css` | 74 (define the value once; 74 first) | W3-B |
| PCOMP-81 | Withdrawn-list setting key in the code-style font (S9) | Ruled 14:15: uses the code-style font "as the register above it does"; frame half already closed | S | the S9 withdrawn-list rule in `apps/web/src/styles/` (exact file not named in the ticket text I read: builder locates; UNMEASURED) | none | W3-B |
| PCOMP-128 | `DEPLOY.md` lines outside the 0020/0024/0025 sections still say Route B "as above" or UNMEASURED | Created today by the records seat for exactly this lane; C-143 and C-144 "permit the lane on row #479". Items (3) 0023 (lines 401-403) and (4) 0026/0027 (lines 626-627, 673-674) have measured results in the ticket; item (2) 0022 needs its own throwaway-database measurement before words change. The F1 grammar line (169) "needs approved wording": leave it. | S to M | `DEPLOY.md` (exists on main), maybe a test under `scripts/` for the guide checker | none (no open PR touches it) | W3-C |
| PCOMP-11 | "Asked under <item>" pointer for a shared question | Ruled 14:15 (a) "Yes, build it". Build needs a contract change; the two new words go to the words card BEFORE they ship (C-140 forbids shipping them). Build on a branch, land only after the words are approved. | L | engine questionnaire table (path not read: UNMEASURED), `packages/api-contract/src/document.ts`, `apps/api`, Expert screens in `apps/web` | `packages/engine/src/index.ts` is in PR #85's file list; possible overlap | W3-D (Opus) |
| PCOMP-52 | Table of contents for the policy PDF, heading "Contents" | Ruled 14:15: the word is approved; build is its own change, template bump `policy-document-pdf/3` | L | `packages/renderers/src/document-pdf.ts`, `pdf-fit.ts`, template | DIRECT conflict with PR #85 and with 23, 123, 82 | lane A (PDF) |
| PCOMP-23 | Policy PDF drops the manifest hash line with long names (change-report half merged in #120) | Unchanged from 13:26; comment 40721 closing clauses | M | `document-pdf.ts`, `pdf-fit.ts`, renderer test | PR #85; 52, 123, 82 | lane A |
| PCOMP-123 | Size the footer by the real page count | Unchanged; needs the page count in `document-pdf.ts` | M | `change-report.ts` (`FOOTER_LABELS`, line 535), `document-pdf.ts`, `pdf-fit.ts` | PR #85; 23 | lane A |
| PCOMP-82 | Cover date in Sydney time set on the brand profile | Ruled C-71 COMP-15 (a); looks unbuilt (UNMEASURED on main) | L | migration + rollback in `packages/db/migrations` (latest on main is 0027), `api-contract`, brand profile in `apps/api`, `document-pdf.ts` cover | PR #85 including its `b59-policy-pdf-cover.test.ts`: worst overlap | lane A, last |

### Lanes (PCOMP)
- **W3-B, style leftovers:** 74 then 80 then 81. Sonnet, S. CSS only; measure contrast/pixels before and after, nothing deploys. Gate tier 2 (G2).
- **W3-C, deploy-guide corrections:** 128 items (3), (4), then (2) after a throwaway-database measurement (heavy lock per the 13:26 lane C). Sonnet, S to M. Gate tier 2.
- **W3-D, "Asked under":** 11. Opus (contract change on a data surface; C3-class caution), L. Starts now only as a branch; the two new words are a card for the product owner first.
- **Lane A, PDF:** 23, 123, 52, 82 (in that order, 82 last). Opus (layout needs independent measurement; migration is deploy-bearing). All four collide with held draft PR #85. Tuesday's call. Default: land the small PDF PRs first and let #85 rebase (it is a draft on hold); do not start 82.

### Excluded (PCOMP, summarised)
- Done since 13:26 (absent from today's open set, checked against the dump): 21, 26, 27, 77, 15, 98, 116, 127, 114, as recorded in C-142 to C-145.
- Held label and waits-for-held-PR #85 (19 `held`; 4 epics; L1 to L9 sample-document chain 29-61 that feeds the held loader): unchanged from 13:26. PCOMP-75(b) is "held with the Guided work" by its own record (B1495 STATUS line 81, 122): excluded.
- Waits on the owner or a ruling (unchanged from 13:26): 46, 94 (`needs-kam`), 9, 13, 29, 38, 65, and the remaining ruling-bound keys of the 13:26 list.
- Not agent work or superseded: 5-8, 10, 16, 18, 25, 28, 59, 61, 64, 78, 93.
- Per-class counts for today's 81: UNMEASURED (not assigned by program this time).

### Records owed (PCOMP)
Composer is current through C-145: #120 (recorded), #123 (C-143), #124 (C-144), #122 named inside C-145 but C-143 notes it "not recorded as a landing". Owed: a landing entry for #122 (squash `b14467e2`), and a decision on PCOMP-23/123 comments that say "ruling whether Done not made". PCOMP-128 is the new ticket for W3-C.

---

## 3. MPS Commercial Calculator (Jira MPSCALC)

Open: 196 (all Backlog; 180 Task, 15 Epic, 1 Bug). Origin main `acd6aec0` (#176 and #177 merged 18:10 and 18:23 AEDT). Open PRs: none (`pulls?state=open` returned empty; control: the same call on the other three repos returned rows). Live branches (compare main...branch): `b1502/mps-web-e2e-print` (ahead 8, 18 files, under review), `b1511/mps-lane-l4-engine-docs` (ahead 2, `docs/ENGINE.md` only), `b1494/mps-api-stores` (ahead 6, merged as #176, leftover), `b1508/mps-pkcs-pin` (merged as #177). Seats building now: M117 (L3: `PurchaseValidation` tests, `ReferenceDocumentValidator` tests, importer prove tests), M119 (L5: `scripts/deploy-from-ci.sh`, `scripts/lib/kudu.sh`, fakes, `entra_apps.py`, `tools/demo/*`, `infra/*`, `Api.csproj`). Held for the owner, not listed: MPSCALC-160 clause 6, MPSCALC-130 word-set clause, MPSCALC-331, MPSCALC-200.

Rulings: C-102 to C-130 in `CLARIFICATIONS.md` (all "2026-11-11 14:34 ... accepted all 29 quick recommendations"; each ticket carries a "Records note" comment). The "Work owed" line of each entry was read; where it says "any new user-facing words go to the product owner first" the build must not invent words.

### Actionable now (the ruled set, plus 13:26 residue)

| key (MPSCALC-) | short title | why actionable | size | files (exist on main, tree read) | conflicts | lane |
|---|---|---|---|---|---|---|
| 131 | Site cards past 26 sites print `[` and `\` | Ruled C-107 "AA, AB, ..."; still open on main: `RentalDocument.tsx:40` is `String.fromCharCode(65 + i)` (grep with positive control: `export` count 1) | S | `web/src/proposal/RentalDocument.tsx`, a 28-site row | none | W3-A |
| 112 | "and 1 more rates" | Ruled C-108: singular of the approved words; still open: `OnePager.tsx:37` `moreRates` | S | `web/src/proposal/OnePager.tsx` + test | 110 | W3-A |
| 113 | Home tiles three across at mid widths | Ruled C-106; `styles.css:159` `.kpis` is still `auto-fit minmax(210px, 1fr)` | S | `web/src/styles.css`, `web/e2e/home-tiles-fill.spec.ts` | b1502 does not touch either (its 18 files listed in Method) | W3-A |
| 110 | One-pager always one A4 page | Ruled C-104 "tighter limits"; limits and a print check; any new words go to the owner first | M | `web/src/proposal/OnePager.tsx` (caps at :6), `one-pager.css` | 112 same file | W3-A |
| 229 | Colour rate only for classes with colour pages | Ruled C-112; `Proposal.cs:525-526` | M | `src/MpsCalc.Api/Quotes/Proposal.cs`, its tests | L4 is `ENGINE.md` only; the 160 clause-6 hazard lives in `PricingPolicy.cs`/`QuoteEndpoints.cs`: do not touch | W3-B |
| 189 | Duplicate rule: ids differing by case/Unicode form; unknown state word | Ruled C-117 "same id, refuse"; clauses 4-5 unmet; main already has `OrdinalIgnoreCase` (lines 85-86) and a deny-list of three states (:267) so read what remains first | M | `src/MpsCalc.Api/Sources/SourceDocumentChecks.cs`, tests, a docs sentence | docs sentence in `docs/API.md` waits for lane C | W3-B |
| 91 | Reference-only store that loses `registry.json` re-initialises silently | Ruled C-124 "refuse to start"; "its words and its test row" (refusal text is a new word: send it to the owner as a draft, do not ship an invented one) | M | `src/MpsCalc.Api/Sources/*` store start-up, tests in `tests/MpsCalc.Api.Tests/Infrastructure/SourceStores.cs` | L2 landed (#176) in the same area: read PRIOR WORK first | W3-B |
| 316 | `quoteRef` "at most 100 characters; an emoji counts as two" in the remaining places | Ruled C-108; places listed in comment 40472 | S | `docs/API.md`, contract text, `openapi.json` | lane C order | W3-C |
| 120 | Contract `info.version` rule | Ruled C-125: practice becomes the rule; own short section in `docs/API.md` | S | `docs/API.md`, `docs/api/openapi.json` | W3-C | W3-C |
| 364 | Published sentences say no row carries the four staff list columns | Ruled C-109 (b): developer-only text corrected from the code without word review; a customer-visible sentence goes to the owner | S | `docs/API.md:367-368`, `openapi.json:1409`, `web/src/api/generated/openapi.snapshot.json`, `schema.ts`, `Dtos.cs:461` comment | W3-C | W3-C |
| 371 | Three false/short template-store sentences | Ruled C-109 (b), same rule | S | `docs/API.md:863-868` | W3-C | W3-C |
| 233 | Clone refuses an existing reference | Ruled C-119 "refuse"; clauses 1-2 unmet (main derives `-COPY`, `QuoteEndpoints.cs` Duplicate :501) | M | `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`, `QuoteStore.cs`, `Dtos.cs`, `docs/api/openapi.json`, `web/src/api/generated/**` | `stubApi.test.ts` (b1502 adds duplicateQuote rows): trivial overlap | W3-C |
| 161 | Archive a quote (hidden from lists, kept on disk) | Ruled C-115 "archive" with K-16 defaults in the ticket | L | `QuoteEndpoints.cs`, `QuoteStore.cs`, `web/src/screens/QuoteList.tsx`, contract | 233 same files: sequence | W3-C |
| 103 + 222 + 226 | Roll-forward-only rule; deploy refuses an older package once care packs/staging rows exist | Ruled C-102 (a) both. The M119 kit names these as "NOT this lane, do not pre-empt, sequence after this lane lands" | L | `scripts/deploy-package.py`, runbook line | M119 | W3-D, AFTER L5 |
| 202 | Widen the pre-deploy check to every overlay form the app refuses at start-up | Ruled C-103; "must land before the first hosted price overlay exists" | M | `scripts/deploy-package.py` `pre1`, `scripts/tests/test_deploy_pre1.py` | M119's 203 owns that test file | W3-D, AFTER L5 |
| 224 | Ship the patched Xml assembly in the package | Ruled C-126; PR #177 (Pkcs pin) just landed: read whether it already carries it (UNMEASURED); records seat R216 is reading #176/#177 | S to M | `src/MpsCalc.Api/Api.csproj` | M119 touches the same csproj comment (349) | W3-D, AFTER L5 |
| 128 | Rental price screen keeps the breakdown row only | Ruled C-111; `PriceView.tsx:128` still has the `Software / month` card | S | `web/src/screens/PriceView.tsx`, `web/src/components/PriceBreakdown.tsx:59` | b1502 EDITS `PriceView.tsx` | W3-E, AFTER b1502 |
| 150 | Deal-level usage tile at the top of the usage section | Ruled C-113 for placement only; other points of comment 40409 not settled | M | purchase usage section (b1502 edits `PurchaseBomEditor.tsx`, `PriceViewColumns.tsx`) | b1502 | W3-E, AFTER b1502 |
| 195, 78 | Engine-target sentence into the engine docs (195 only that clause); remove "provisional" marking in the places comment 39419 names (78) | Ruled C-108 and C-130 | S | `docs/ENGINE.md` | b1511 EDITS `docs/ENGINE.md` | W3-F, AFTER b1511 lands |
| 334 item 4, 121 e2e folder-drop, 369 re-run | L1 residue | b1502 STATUS RESIDUE lists them | M | `web/e2e/**`, `web/src/api/stub/*` | b1502 | W3-G, AFTER b1502 |

### Lanes (MPSCALC, file-disjoint with the order)
- **W3-A** (web look/print): 131, 112, 113, 110. Sonnet, M. Gate G2 (tests/CSS); 110 includes a print check (page count).
- **W3-B** (Api rulings, no contract change): 229, 189, 91. Sonnet, M. Each has a red-first cell. Gate G2; 91 is start-up safety: tier-1 gate if the seat touches the refusal path.
- **W3-C** (docs/contract then code): 316, 120, 364, 371 (docs), then 233, 161 (code). Sonnet, L. One seat, one openapi regeneration. Gate G1/G2 by file.
- **W3-D** (deploy refusal, after L5): 202, then 103/222/226, then 224. Opus for 103/222/226 (deploy-path rule that hides data), Sonnet for 202. Nothing deploys, no `az`.
- **W3-E** (after b1502 lands): 128, 150. Sonnet.
- **W3-F** (after b1511 lands): 195, 78 (docs). Sonnet.
- **W3-G** (after b1502 lands): 334 item 4, 121 e2e, 369. Sonnet.

Model per `fleet/specs/model-routing.md` section 4: C2 (multi-file build, Sonnet), C3/C4 (Opus where the surface is auth/data), G1/G2 gates. Datasec has no local tier (P4).

### Excluded (MPSCALC, summarised)
- Still need words or a name approved by the owner before they can be built or shipped: 368 (hide six figures; the field name is proposed for approval first, clause 6 of comment 40935 waits; also entangled with 160 clause 6, held), 169 (field name approved only "as proposed": name still comes to the owner, C-116), 156 (rental credit: new field, contract change and new words to the owner first), 194 (the sentence goes to the owner before it ships), 85 (the owner sends the spec file), and the other open clauses of 195 (comment 40990).
- Moved to Done by today's rulings (gone from the open set): 114, 115, 117, 132, 109, 295, 342, 380, 381, 382, 383, 68, 72, 73, 87, 88, 70, 77.
- Everything excluded at 13:26 for deploy, hosted data, large features, v13.4.1 `lane-v*` HTML pack (the 13:26 reading caveat stands: 237, 284-287, 258, 358-360 would be server-side candidates if the hold covers only HPSM), and spec-seed umbrellas: unchanged.
- Already in a live lane or open branch: 135, 96, 297, 251, 57, 111, 185, 139, 198, 377, 130 style half (b1502); 147, 158, 196, 160 (b1511); 324, 325, 338, 339, 333, 331, 340, 341, 207, 302 (M117); 126, 203, 119, 201, 223, 173, 349 (M119); 98, 99, 122, 123, 163, 217 (landed #176).
- Per-class counts for today's 196: UNMEASURED.

### Records owed (MPS)
R216 (B1513 kit, untracked in this repo's status) is queued for #176 and #177: tickets 98, 99, 122, 123, 217, 124, 224 and the 14:34 rulings. After b1502 and b1511 land: 135, 96, 297, 251, 57, 111, 198, 334, 377, 121, 130 (style half), 147, 196, 158. Jira `updated` for 98 (11-06), 99/122 (11-10) shows no landing comment from #176 yet. The "Records note" comments for the 29 rulings are already on the tickets.

---

## 4. NexusAI (Jira RD, repo `datasecau/Reporting_Dashboard_Au`)

Open: 851 (To Do 389, Testing 246, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2; 406 Bug, 370 Task, 72 Story, 3 Epic). Origin main `ef068ea0` (2026-11-11T06:25Z). Delta from the 13:26 main `0ab365b1`: 7 commits, 6 files: `scripts/csp-convert.py`, `scripts/refactor-inline-styles.js`, `__tests__/rd970-...`, `rd971-...`, `rd407-r2-missing-mid-swap.test.js`, `scripts/verify-expected-counts.json` (PRs #190 CI Node 24, #191 RD-407, #192 RD-970/971). No file under `static/` or `backend/` changed, so the 13:26 anchors hold: `static/login.html` bootstrap-icons SRI still `sha384-l4UPAMHGzl7zwogLW4nOwaU2I5bg6fST3wzBSRBD` (40 characters; `integrity=` count 2 as control); `static/index.html` `role="tablist"` 0, `tab-button` 10 (control).

Open PR: #193 (`rd412-smtp-route`/RD-720: 3 files, `__tests__/rd412-smtp-route.test.js`, `rd720-...`, `verify-expected-counts.json`). Chain remaining after it (B1484 order): row 8 archive (RD-731, 15 `__tests__` files), row 9 revoke (RD-972/976), row 10 l1 (RD-929/977/978); the two other `b1480` stack branches (viewer-write-gates RD-958/793; setup-column-mapping RD-967) also edit `backend/server.js` (3 of the unique 18 files across the four b1480 branches are server.js, jsonStorage.js, role-capabilities.json). The `b1492` branch (RD-407 r2) is merged (#191).

Jest lock: base `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017`; at 19:07 its listing shows `queue-docker`, `queue-jest` (empty), `released`; WHO HOLDS IT now: UNMEASURED (the B1484 kit read it held by a gate at 02:30Z). Kit budget is about 65 minutes of lock per landing row; three rows remain, so roughly three hours of FIFO ahead of a new waiter if the chain keeps going.

### Actionable now: 13:26 lanes re-verified, plus the 14:34 rulings (17 recommendations accepted, each with a "Ruling recorded; not moved" comment)

All 13:26 lane keys were rechecked against today's dump: 22 lane-S keys, 12 lane-B, 17 F1, 18 F2 and 35 T keys are all `To Do` (program `rdcheck.py`; control: the printed status Counter sums to 851). Newly buildable by ruling:

| key | short title | why actionable | size | files (exist on main) | needs jest lock | lane |
|---|---|---|---|---|---|---|
| RD-175 | White toner text on light track, both modes | Ruled: fix in both modes ("Yes to both") | S | `static/css/dark-mode.css`, `static/css/index-styles.css` | yes (test cell + full verify) | F2 |
| RD-349 | `#7f8c8d` on three more selectors; JS-created KPI label `.metric-card .metric-label` | Ruled: same contrast ruling, measured against each ground | S to M | `static/css/*`, `static/js/index.js` | yes | F2 |
| RD-532 | `#loadingOverlay` covers the open-site banner 3-6.5 s | Ruled: banner stacks above the overlay | S | `static/index.html`, css | yes | F2 |
| RD-858 | Remove the dead SQL box on `testing.html` | Ruled: remove; cells that depend on it rewritten, not deleted | S | `static/testing.html`, the `__tests__` cells that read it | yes | F2 |
| RD-759 third shape | CSP intake refuses `data:` addresses carrying an at-sign | Ruled: refuse (the other two shapes not ruled) | S | `backend/services/cspReport.js` (touched by merged #186) | yes | B |
| RD-810 | CodeQL js/file-access-to-http in `tests/uat-run.js:30` | Ruled: fix, red first, never dismiss | S | `tests/uat-run.js` | yes | T |
| RD-578 | `AzureADManager` reads `KEY_VAULT_NAME`: sign-in init always throws on marketplace deploys | Ruled: "fixed and reviewed on its own, own red proof" (changes AUTH behaviour) | M | `backend/azure-ad.js` | yes | B2 (Opus, own PR) |
| RD-577 | Key Vault status reads `KEY_VAULT_NAME` instead of `KEYVAULT_NAME` | Ruled: status read only | S | `backend/server.js` (:631, :642, :17733) | yes | S |
| RD-888 | Log Analytics path of the risk run: 1,000-row ceiling and a defined malformed-limit answer | Ruled | S | `backend/server.js`, `backend/azureLogAnalytics.js` | yes | S |
| RD-433 | `SEED_DEMO_DATA` also needs a demo-only marker; synthetic-data banner | Ruled; banner words are new and go to the owner BEFORE shipping | M | `backend/seedDemoData.js`, `backend/server.js` | yes | S (build, words held) |
| RD-610, 612, 622 | Keep sign-in settings out of erasure; wipe alarm stays until acknowledged; plain health line | All three ruled; the acknowledge wording and health line words are new, to the owner first | L | `backend/dataErasure.js`, health route in `backend/server.js` | yes | B2 (Opus, C4: data-destroying path; read-only measurement first) |
| RD-644 | Per-deployment "also notify" address for in-app feedback (empty by default) | Ruled | M | settings + feedback route in `backend/server.js`, `static/settings.html`/`js/settings.js` (labels are new words) | yes | S, after F1 for settings.js |
| RD-522 | Scrub names of people and internal agents from code comments in the shipped image | Ruled; "a scripted clean-up with its own review and an image-content check" | L, cross-cutting | `backend/**`, `static/**`, `scripts/**` | yes | Z, run LAST, alone |
| RD-636, 702 | Truthful "encrypted at rest" wording | Ruled "agent drafts"; the drafted words go to the owner before any edit. Not buildable tonight (draft only). RD-702 has a measure-first step. | draft only | `static/first-run-setup.html` (:1849, :162) | n/a | none |

The rest of the 13:26 table stands unchanged (lanes S, B, F1, F2, T with their keys, orders and conflicts; see SWEEP-1326 section 4). Re-confirmed here only: the four CDN/ARIA/SRI anchors above; main delta touches none of those files.

### Lanes (NexusAI) and lock need

| lane | owns | keys (13:26 order, plus today's) | model | can start before the chain finishes? |
|---|---|---|---|---|
| F2 | `static/index.html`, `static/testing.html`, `static/js/{index,admin,chart-details}.js`, `static/css/**`, `tests/e2e/**` | 144, 164/175/222, 349, 261/259/220, 483/613/832, 532, 858, 835, 771, 861, banner-guard cells; 145 last | Sonnet (Opus gate not needed for CSS; tier 2) | YES to start (static only, no `server.js`/`jsonStorage.js`); every full-suite verify queues on the jest lock |
| F1 | `static/{login,first-run-setup,settings}.html`, `static/js/{first-run-setup,settings,entra-provisioning-ui}.js` | 475/560, 189, 456, 492, 117/188/176, 481, 808, 371/373, polish | Sonnet | YES (same lock caveat). Do not edit `scripts/refactor-inline-styles.js` |
| B | `backend/**` except `server.js`, `jsonStorage.js`, `simpleDb.js`, `intentRouter.js`, `queryPreprocessor.js`, `ticketStore.js`, `costCentreMap.js`, `docs/role-capabilities.json` | 804, 798 remainder, 455+805, 744, 745, 750, 824, 728, the four local branches (576, 590, 826, 805), 759 third shape | Sonnet; Opus for RD-744 | YES (no chain file touched; lock caveat) |
| B2 | `backend/azure-ad.js`, `backend/dataErasure.js`, the sentinel/alarm module | 578 (own PR), 610/612/622 | Opus (C3 and C4 rows) | 578 yes; 610/612/622 the health-line part touches `server.js`: after the chain |
| T | `scripts/**`, `.github/**`, `docs/**` (less role-capabilities), `__tests__/**` not named elsewhere, `tests/uat-run.js`, `Dockerfile`, `package.json` | finish 730/749/729, 757, 810, small residues, 134; RD-980 waits for the revoke branch | Sonnet | YES, but `__tests__/rd798/rd799` and `verify-expected-counts.json` are chain files |
| S | `backend/server.js` and friends | 13:26 order plus 577, 888, 433, 644 | Opus for the CodeQL set and RD-711; Sonnet for the rest | NO. Rows 9 and 10 and the two b1480 stack branches edit `server.js`, `jsonStorage.js` and `docs/role-capabilities.json`. Start after the chain lands or stack on `2a584f7` |
| Z | everything | 522 | Sonnet with an image-content check | NO. After all lanes land |

Every NexusAI lane needs the jest lock for its full-suite verify (builders can write and run red cells but the project's gate is the full suite). So "can start before the chain finishes" means: start building now, expect the full verify to wait behind up to three more chain rows. UNMEASURED whether single-file targeted runs are exempt from the lock.

### Excluded (NexusAI, summarised; unchanged from 13:26 unless noted)
- In the chain or live branch: RD-720 (PR #193), 731, 972/976, 929/977/978, 958/793, 967. No longer chain (merged): RD-970/971 (#192), RD-407 (#191).
- Moved to Done by today's rulings: RD-514, 883.
- Ruled but words first: RD-636, 702 (drafts), 433/612/622/610 banner and wording (build, ship held), 644 labels.
- Held/needs ruling: 930, 931, 932, 964, 965, 966, 968, 958 part 3, 146, 400, 401, 842 (feature requests; their `updated` stamps are 2026-11-11 but the comment read for 146, 400, 401, 842 shows no ruling text: UNMEASURED).
- Not agent work, marketplace/Partner Center, Jira admin, process tooling, customer-test, roles UI chain 937-957: unchanged.
- In Progress, owned by another seat or human: RD-49, 81, 450, 643, 662, 427, 431, 432 (stale plans).
- Not individually read: the 445 Testing and Release Ready tickets (UNMEASURED beyond status counts); about 85 To Do tickets classified by title only at 13:26 (still so).

### Records owed (NexusAI)
Merged since the 13:26 start and not yet reflected on the tickets (Jira statuses all `To Do`, `updated` stamps older than the landing): #186 (RD-759 shapes 1 and 2, RD-796), #187 (RD-962, 963), #188 (RD-979), #189 (RD-798, partly), #190 (RD-605, 544), #191 (RD-407, Release Ready), #192 (RD-970, 971). The B1500 (R213) records kit names RD-544, 605, 720, 731, 970, 971, 979, 407, 798, 759, so a seat may already cover part of this; UNMEASURED. Chain PR #193 (RD-720) when it lands.

---

## Questions for Tuesday (each with a default)

1. Composer PDF lane vs held draft PR #85: default is to land small PDF PRs first (23, 123) and let #85 rebase; do not start 82 (cover date + migration).
2. MPS W3-D deploy refusal: default is to hold until M119 (L5) READY because both own `test_deploy_pre1.py`.
3. NexusAI: default is to launch F2 and F1 now and B and T when a seat is free; S and Z stay down until the chain lands.
4. HPSM-405: scope call as the ticket says. Default: build the shell safe area only, leave the pill where C-42 put it.
5. Words that must go to the owner before any of these ship: Composer PCOMP-11 (two words); MPS 91, 110 (if any), 194, 368 (field name), 169 (field name), 156; NexusAI 433, 612, 622, 636, 644 (settings labels), 702.

## Method and disclosures

- Jira instrument: a small Python script in `/private/tmp/sweep1900/jq.py` (GET only, `search/jql` with `nextPageToken`, 0.25 s apart; credentials read in-process from each project's `4_Credentials/.env`, never printed, never on argv). JQL: `project = <KEY> AND ( statusCategory != Done )` (parentheses carried). Totals and pages: HPSMPOC 131 (2 pages), PCOMP 81 (1), MPSCALC 196 (2), RD 851 (9); each total equals its de-duplicated key count (control inside the script). Tickets read individually (description + newest comment) are those named in this file; everything else is read by summary and label only.
- GitHub: `gh api -X GET` under each project's own `GH_CONFIG_DIR`; open PRs, closed-merged PRs (12 newest per repo), branches (`branches?per_page=100 --paginate`, totals: HPSM-POC 327, Composer 196, MPS 201, NexusAI 456), `compare main...branch`, and full recursive tree reads for file existence (HPSM 1806 paths, Composer 1043, MPS 781, NexusAI 1054). File-content greps were run on the decoded file with a positive control in the same step (counts printed beside the zero/hit).
- Local reads: `CLARIFICATIONS.md` of Composer (C-140 to C-145 read in full), MPS (C-102 to C-130 read for settled/owed lines), the MPS/Composer/HPSM lane STATUS files, the lane kits B1494 to B1512 (key lists by program `kitgrep.py`), the NexusAI B1484 kit, `model-routing.md`, `DRAFTER_RULES.md`.
- NOT READ / UNMEASURED: HPSM-POC `CLARIFICATIONS.md` (the local analysis-repo copy ends at C-30, 2026-09-29; later HPSM rulings were taken from ticket comments and STATUS files); NexusAI `CLARIFICATIONS.md` (not opened; rulings taken from the "Ruling recorded" comments on 23 tickets); per-class exclusion counts for all four projects (not assigned by program today); the 445 NexusAI Testing and Release Ready tickets; PR CI states of #309, #312, #193 (taken from the order text); who holds the NexusAI jest lock now; whether #177 already carries MPSCALC-224; the exact CSS file for PCOMP-81; the engine questionnaire path for PCOMP-11.
- Not touched: Secuura, `.local/`, real price stores, `fleet/briefs_staged/`, the ledgers, `decision_queue.sh`; no hosted, UAT or production host; no `az`, `ssh`, `docker`; no `cd`.
- Boundary hazards noted for the lane kits: MPS pricing money values never enter a kit or ticket text; HPSM kits carry the standing line "This phase builds no integration with HP tools"; the drafter-rules file still names `/Volumes/Laptop-DEV` where this drive is `/Volumes/Datasec_DEV`.
- Scratch left in `/private/tmp/sweep1900/` (JSON dumps, decoded single files, tree lists, three scripts). Nothing in any project folder.
- READ-WHOLE-BY-TUESDAY: ____
