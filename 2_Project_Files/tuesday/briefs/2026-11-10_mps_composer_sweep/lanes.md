# MPS Calculator and Security Composer: lanes agents can run now (sweep, read-only)

Drafted at 2026-11-10 03:13:39 AEDT (`date` print in the generator run). Drafter read only: Jira boards by the project's own `.env` in-process (no token printed), `gh api -X GET` under each project's `.gh-config`, `decision_queue.sh list` (read-only), the pickup file lines for MPS/Composer. No git, board, mail, az, ssh, docker or hosted-host action. Local checkouts are stale (MPS `2_Project_Files` HEAD 7f6ca4c0 is B05; Composer 0b2fca43), so every code fact below is from origin: MPS main `31234f5f` (committed 2026-11-08T12:28:11Z), Composer main `a54250f4` (2026-11-03T20:16:17Z), both equal to the morning sweep's reads.

## BLUF

- **MPS Calculator (main 31234f5f, 0 open PRs): 10 lanes M1-M6, M8-M11 (M7 dropped: its only ticket, 194, is already named by merged PR #79), 25 fresh tickets, 17 conditional on a prior-work read.** Lanes are pairwise path-disjoint by program (section Disjointness), so all can run at once; the machine is the limit (each dotnet or web lane is a full CI-equivalent run). Size: S=5, M=4, L=1.
- **Security Composer (main a54250f4, 3 open PRs all held): 4 lanes C1-C4, 7 fresh tickets, 4 conditional.** C1 is the footer fix the 11-03 card left as a ticket; it changes a PDF look, so it builds and does not deploy.
- **OWED LANDINGS: none.** MPS: 0 open PRs (`pulls?state=open` empty; control: the same call on Composer returns 3 and `pulls?state=closed` on MPS returns #166 at the top). The last round-cap card, `mps-106-price-guard-round-cap-1106`, reads `ruled a` and `delivered: MPSCALC-386; 10 rows;` in `decision_queue.sh list`, with #166 merged 2026-11-08T12:28:11Z. Composer: the open PRs are #85 (HOLD), #86 and #91 (Dependabot, held by the product owner's 11-04 note), nothing to land. The 11 open cards on the store are none of MPS or Composer except `composer-l05-setup-card-too-1014` (settled by the product owner's 10-23 email; the pickup says do not re-raise).
- **OWED RECORDS (the real backlog here): Jira lags the merged PRs.** 29 open MPS tickets and 2 open Composer tickets are named in the TITLE of a merged PR (list in R1 and R2). Examples read at source: MPSCALC-358 (PR #150 title), -359 (#155), -377 (#151), -381 (#156), -382 (#157), -98 (#34), -178 (#47), -189 (#100), -194 (#79), -203 (#81). Some are residual-by-design (PR #155 said "MPSCALC-359 stays open for the Api and screen halves"), so each needs a read of PR against ticket, not a bulk close. A records seat per project owns it; no repo path is touched.
- **EXCLUSIONS (counts, program-made, conservation checked below):** MPS 210 open non-epic tickets: 42 in lanes, 13 records, 17 need the product owner (question-for-kam), 19 need a ruling (label), 21 explicit with a reason, 5 later phase, 35 feature lanes V0-V11 not assessed, 43 seed rows not assessed, 15 other not read. Composer 91 open non-epic: 11 in lanes, 19 held (label), 2 need the product owner or a reviewer, 20 explicit, 29 sample-policy rows not assessed, 10 other not read.
- **Dated item:** 2026-11-12 Dependabot code-scan question (MPSCALC-383 and -384 area, Composer #86/#91): excluded and untouched. MPSCALC-383 is listed as an explicit exclusion; MPSCALC-384 is Done.
- **Decision store:** `decision_queue.sh list` read OK at drafting (2026-11-10 03:13:39 AEDT). The MPS card `mps-106-price-guard-round-cap-1106` default (a) is already executed: `ruled a` @ 2026-11-08T20:31 and delivered. Nothing on the Composer side is pending a card.

## Facts every lane copies (sources)

- **Landing (both projects):** Tuesday opens and lands PRs; seats push their branch only. MPS: `--squash --match-head-commit <sha>` after hosted checks plus CodeQL (`NEXT-PICKUP-TUESDAY.md` line 32, MPS #112; MPS CLAUDE.md "Datasec CodeQL rule": "Seats push a branch only; Friday opens the PR and merges once CodeQL is green"). Composer: same squash form (`NEXT-PICKUP-TUESDAY.md` line 31, Composer #92). Not deployed either way: Composer "deploys only on Kam's card" (pickup line 24); MPS has no deploy without a brief.
- **MPS CI predicate (`.github/workflows/ci.yml` at main 31234f5f):** job `dotnet`: `dotnet build MpsCalc.slnx -c Release` then `dotnet test MpsCalc.slnx -c Release --no-build` ("0 warnings" is in the job name); job `web`: `npm ci`, `npm run lint`, `npm test`, `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist`; job `python`: every `tools/demo/test/test_*.py infra/tests/test_*.py scripts/tests/test_*.py` under `python3 -I`, one failing file fails the step; job `package`: `bash scripts/package.sh`. Pass = all four success on the PR head.
- **Composer CI predicate:** the repo has NO ci workflow (tree: no `.github` path; `actions/workflows` lists Dependabot Updates and CodeQL only; control: both calls returned). Hosted pass = CodeQL `Analyze (javascript-typescript)` and `Analyze (csharp)` success (main run at a54250f4 success on both, jobs read). The test predicate is local: `scripts/ci.sh` (secret scan, node lint/format/typecheck/build/test in the CI image with no network, db tests in a throwaway postgres, bridge tests, stack checks) which needs docker, so the seat runs it.
- **Standing for every lane kit:** PRIOR-WORK CHECK (a READY without a PRIOR WORK section is returned), because the sweep found Jira lagging merged PRs (above); no message to any human; never delete; red-first for each product change; Tuesday writes the Done-when where a ticket gives none.

## MPS Calculator lanes

### M1: Web unit-test pins (test only) (size S)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-369
- **Conditional (a merged PR names them; read the PR first):** MPSCALC-334 [#116(body), #111(body)]; MPSCALC-198 [#103(body)]
- **Owned paths:** `web/src/screens/bom/PurchaseBomEditor.test.tsx`; `web/src/screens/bom/PriceReason.test.tsx`; `web/src/screens/FleetGrid*.test.tsx`; `web/src/api/stub/stubApi.test.ts`
- **NOT yours:** web/e2e/**, web/src/feedback/**, web/src/api/generated/**, every non-test file under web/src
- **Fix shape:** 369: the five rows that time out at the 5 s default under whole-suite load: make them wait on state or give the rows a stated budget; test only, no product byte. 334 and 198: read the landed PRs first (conditional).
- **Proving checks:** web job: `npm ci`, `npm run lint`, `npm test` (from web/); no product file changes so the build step is unaffected

### M2: Playwright e2e repairs (test only) (size M)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-96, MPSCALC-135
- **Conditional (a merged PR names them; read the PR first):** MPSCALC-297 [#90(body)]
- **Owned paths:** `web/e2e/**`; `web/playwright.config.ts`
- **NOT yours:** web/src/**, web/package.json, web/package-lock.json
- **Fix shape:** 96: four stub-mode specs red as shipped (POST /api/v1/quotes 502 from the Vite proxy with no API behind it): the ticket measured that a synthetic API base turns them 3/3 green. 135: smoke.spec.ts red at :23 before the proposal; press Short-form first at :61-66 (ticket text). 297: exact nav list and the Proposal link locator (conditional: PR #90 body names it).
- **Proving checks:** e2e is NOT in CI (ticket 334 text: "e2e, which is not part of CI"); the seat runs the named specs locally 3 of 3; web job lint + `npm test` stay green; UNMEASURED whether `npm run lint` covers web/e2e

### M3: .NET test-only pins A (template isolation, care key) (size S)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-380, MPSCALC-221
- **Conditional (a merged PR names them; read the PR first):** MPSCALC-381 [#156(title)]
- **Owned paths:** `tests/MpsCalc.Api.Tests/TemplateIsolationTests.cs`; `tests/MpsCalc.Api.Tests/CareKeyPatternApiTests.cs`
- **NOT yours:** src/**, every other tests/ file
- **Fix shape:** 380: the format guard is quiet on four forms of an earlier hole; PR #156 pinned "two line-break forms" so read what remains. 221: rename or reshape the synthetic care key constant at CareKeyPatternApiTests.cs:15 so a generic-key scanner does not match it (or an allow-list entry, which would be a repo-root file: do not; rename). 381 conditional (PR #156 title names it).
- **Proving checks:** dotnet job: `dotnet build MpsCalc.slnx -c Release` (0 warnings) then `dotnet test MpsCalc.slnx -c Release --no-build`

### M4: .NET test-only pins B (governed edges, refusal order, walk survivors) (size M)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-340, MPSCALC-341, MPSCALC-324, MPSCALC-333
- **Conditional (a merged PR names them; read the PR first):** MPSCALC-310 [#99(body)]
- **Owned paths:** `tests/MpsCalc.Api.Tests/SourceLifecycleTests.GovernedNullClassEdges.cs`; `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs`; `tests/MpsCalc.Api.Tests/QuoteRefusalOrderGuard.cs`; `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs`; `tests/MpsCalc.Api.Tests/LaneM4*.cs`
- **NOT yours:** src/**, every other tests/ file (M3, M5, M6, M11 own theirs)
- **Fix shape:** 340/341: two more rows and six pins in the edges file (gate text: tests only). 324: three rows (non-document exception at store load not read as unavailable; CannotOpen operator line; last body-refusal branch). 333: the edit-path twin of the fleet-below-limit row and the other pins in QuoteRefusalOrder*.cs. New rows may go in new files named LaneM4*.cs. 310 conditional (PR #99 body names it).
- **Proving checks:** dotnet job: Release build 0 warnings + `dotnet test`; each new pin must also turn red under the ticket's named mutant (red-first)

### M5: Source lifecycle and reference-document validator (product + tests) (size M)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-331, MPSCALC-99
- **Conditional (a merged PR names them; read the PR first):** MPSCALC-189 [#100(title)]; MPSCALC-92 [#100(body)]; MPSCALC-90 [#29(body)]
- **Owned paths:** `src/MpsCalc.Api/Sources/**`; `src/MpsCalc.Import/Validation/**`; `tests/MpsCalc.Api.Tests/LaneM5*.cs`
- **NOT yours:** src/MpsCalc.Api/Quotes/**, src/MpsCalc.Api/Contracts/**, src/MpsCalc.Api/Inventory/**, tests/MpsCalc.Api.Tests/SourceLifecycleTests.GovernedNullClassEdges.cs (M4)
- **Fix shape:** 331: ReferenceDocumentValidator.cs:160/:162/:166/:203 throw on a null software product or null cell link; skip a null product in the term-gap check and treat a null link as does-not-agree (gate fix shape), so the existing REFERENCE_DATA_REJECTED refusal answers instead of 500. 99: SemaphoreSlim.WaitAsync(remaining) plus await Task.Delay(25) in the lock poll, bound counted from arrival (ticket fix shape). 189/92/90 conditional: PRs #100 and #29 name them.
- **Proving checks:** dotnet job; red-first rows for the 15 shapes in 331

### M6: Feedback backend hardening (product + tests) (size M)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-97, MPSCALC-102, MPSCALC-122, MPSCALC-124, MPSCALC-125
- **Conditional (a merged PR names them; read the PR first):** none
- **Owned paths:** `src/MpsCalc.Api/Feedback/**`; `tests/MpsCalc.Api.Tests/Feedback*.cs`
- **NOT yours:** web/src/feedback/**, src/MpsCalc.Api/Contracts/**
- **Fix shape:** 97: overlap guard gets the overlay NFC and link-follow fixes (FeedbackStore.cs RefuseOverlaps). 102: one lock scope for the StateOf read and SaveTicket (FeedbackEndpoints.cs:223/:232). 122: nosniff, no-store and the sandbox CSP at the top of Download before the role check. 124: write .bin files outside the lock, re-check the key under it. 125: Load refuses or logs a second (caller,key) and keeps the earliest by submittedAt. Left out on purpose: 121 (the unreadable-file sentence is the product owner's words call), 123 (needs a setting).
- **Proving checks:** dotnet job; one regression test per row as the ticket states

### M8: Docs and runbook sentences (size S)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-200, MPSCALC-225
- **Conditional (a merged PR names them; read the PR first):** MPSCALC-178 [#47(title)]; MPSCALC-195 [#105(body)]; MPSCALC-207 [#84(body)]
- **Owned paths:** `docs/DEMO.md`; `docs/IMPORTER.md`; `docs/ENGINE.md`; `docs/RECONCILIATION.md`; `ROOT:SETUP_RUNBOOK.md`
- **NOT yours:** docs/API.md, docs/api/openapi.json (M11), web/src/api/generated/**
- **Fix shape:** 200: IMPORTER.md:112,:117 care-row counts (262 vs 294) re-measured and the A3 (23/8) and A4 (25/22) gaps explained, counts only, from the local price-book store (never paste prices). 225: SETUP_RUNBOOK.md (project root, outside the repo) names the app client id and hosted host variables, names only. 178/195/207: conditional, PRs #47, #105, #84 name them.
- **Proving checks:** no code: CI untouched; the seat re-reads each sentence at source; python job unaffected

### M9: Infra and script follow-ups (no deploy, no az) (size S)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-119, MPSCALC-201, MPSCALC-205
- **Conditional (a merged PR names them; read the PR first):** MPSCALC-203 [#81(title)]
- **Owned paths:** `infra/tests/**`; `scripts/entra_apps.py`; `scripts/package.sh`; `scripts/tests/**`
- **NOT yours:** scripts/deploy-from-ci.sh, scripts/deploy-package.py, infra/main.bicep, infra/modules/**, .github/**
- **Fix shape:** 119: test_infra.py:4,:59 stop falling back to `az bicep build` under a no-az hold (skip is forbidden by the file's own rule: every test FAILS if no bicep, so state the BICEP env route). 201: entra_apps.py:172,:174,:356-358 look the group up before the first write; the script is edited and tested against fakes, never run against Entra. 205: package.sh:45 guard words name the fix, or package from a clean output directory.
- **Proving checks:** python job: `for t in tools/demo/test/test_*.py infra/tests/test_*.py scripts/tests/test_*.py; do python3 -I "$t"` (ci.yml lines 80-91); package job `bash scripts/package.sh "$(git rev-parse HEAD)" --out ...`

### M10: Readiness sentence and parity proof (size S)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-302
- **Conditional (a merged PR names them; read the PR first):** MPSCALC-295 [#106(body)]; MPSCALC-207 [#84(body)]
- **Owned paths:** `src/MpsCalc.Engine/Readiness/**`; `tests/MpsCalc.Engine.Tests/ReadinessTests.cs`; `src/MpsCalc.Import/Parity/**`; `tools/MpsCalc.ImportCli/**`; `tests/MpsCalc.Import.Tests/LaneM10*.cs`
- **NOT yours:** src/MpsCalc.Engine/Calculation/**, src/MpsCalc.Api/**, docs/**
- **Fix shape:** 302: ParityProof.cs:189-190 compare the (device,SKU) multiset per sheet, not counts, so a count-preserving swap reads DISAGREE. 295 (conditional): sentence only per the 10-20 coordinator ruling quoted in the ticket (raw line count stays; no behaviour change).
- **Proving checks:** dotnet job

### M11: Api contract and quote validation (product + contract copies) (size L)

- **Project / repo:** Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator
- **Fresh tickets (no merged PR names them):** MPSCALC-368, MPSCALC-378, MPSCALC-169
- **Conditional (a merged PR names them; read the PR first):** MPSCALC-358 [#150(title)]; MPSCALC-325 [no merged PR names it]; MPSCALC-338 [no merged PR names it]; MPSCALC-339 [no merged PR names it]
- **Owned paths:** `src/MpsCalc.Api/Contracts/**`; `src/MpsCalc.Api/Quotes/**`; `docs/API.md`; `docs/api/openapi.json`; `web/src/api/generated/**`; `tests/MpsCalc.Api.Tests/LaneM11*.cs`
- **NOT yours:** src/MpsCalc.Api/Sources/**, src/MpsCalc.Api/Feedback/**, tests named in M3/M4
- **Fix shape:** 368: add the purchase recurring projection to the Api result DTO, formed from the engine figures, omitted when the engine omits it, restricted like the other cost and GP members; docs/API.md and openapi.json and the generated copies move with it (web `sync-contract` script). 378: one attribute or one row (ticket offers both; the gate recorded "nothing today"). 169: a field beside lineMarkupsOverlayVersion naming the source versions. 325/338: main already carries MaxWalkEntriesListed = 20 and per-walk counters (PurchaseValidation.cs:32,:131-165, control: constant found), so first confirm the tickets are residual-free and hand them to the records lane; 339 is a measurement. 358 conditional: PR #150 title names it.
- **Proving checks:** dotnet job; web job (`npm run lint`, `npm test`) because the generated copies change; web test "snapshot equals contract, schema.ts equals generator output" is already in main (PR #147)

## Security Composer lanes

### C1: Change-report footer model (size L)

- **Project / repo:** Datasec / Security Composer, datasecau/Datasec-Security-Composer
- **Fresh tickets (no merged PR names them):** PCOMP-120, PCOMP-121, PCOMP-123
- **Conditional (a merged PR names them; read the PR first):** PCOMP-23 [no merged PR names it]
- **Owned paths:** `packages/renderers/src/change-report.ts`; `packages/renderers/src/pdf-fit.ts`; `packages/renderers/test/change-report.test.ts`
- **NOT yours:** packages/renderers/src/document-pdf.ts and every other renderer file, DEPLOY.md, packages/db/**
- **Fix shape:** 120: split the first line with the PDF writer's own line-breaking rules before the model counts rows; rows for bracket-space and tab runs (ticket text; the gate wrote it in prose, not ruled). 121: measure a tab as the writer draws it. 123: size the footer by the real page count (a measurement first; the ticket proposes no Done-when, so Tuesday writes one). 23 conditional: PR #113 changed change-report.ts after it was filed. The look (three dots) is Kam's to approve before any deploy; this lane builds and does not deploy.
- **Proving checks:** scripts/ci.sh step "node: lint, format, typecheck, build, test (--network none)" (needs docker, so run by the seat); hosted: CodeQL `Analyze (javascript-typescript)` and `Analyze (csharp)` on the PR (Composer has no ci workflow file: measured, tree has no .github path and workflows list is Dependabot + CodeQL only)

### C2: Engine timing test under CPU cap (size S)

- **Project / repo:** Datasec / Security Composer, datasecau/Datasec-Security-Composer
- **Fresh tickets (no merged PR names them):** PCOMP-114
- **Conditional (a merged PR names them; read the PR first):** PCOMP-62 [#90(body)]
- **Owned paths:** `packages/engine/test/performance.test.ts`; `apps/web/src/screens/b116-s10-verify-dom.test.tsx`
- **NOT yours:** packages/engine/src/**, apps/web/src/** other than the one test file
- **Fix shape:** 114: the median-of-7 row times out at 5000 ms in the CI image under a CPU cap; raise that row's timeout or budget, or run it outside the shared pool (gate fix shape; test only, no product byte). 62 conditional: PR #90 body names it.
- **Proving checks:** scripts/ci.sh node step; the row green in the same cells the ticket measured

### C3: DEPLOY.md and the db command-guard tests (size S)

- **Project / repo:** Datasec / Security Composer, datasecau/Datasec-Security-Composer
- **Fresh tickets (no merged PR names them):** PCOMP-113, PCOMP-117
- **Conditional (a merged PR names them; read the PR first):** PCOMP-98 [#111(title)]; PCOMP-116 [#114(title)]
- **Owned paths:** `DEPLOY.md`; `packages/db/test/b616-deploy-commands.db.test.ts`; `packages/db/test/b778-route-b-script-complete.db.test.ts`
- **NOT yours:** packages/db/migrations/**, scripts/**, any other db test
- **Fix shape:** 113: name the four remaining row 8 pins or say the paragraph names only the words (b778 row 8, title at :657). 117: say the refusal without the pg_restore version (DEPLOY.md:263 and the row title :769). 98 and 116 conditional: PRs #111 and #114 name them in their titles.
- **Proving checks:** scripts/ci.sh db step (migrations, RLS, tests in a throwaway postgres; docker) and node step; PR #118 type-checks the db test files in CI so the new rows must type-check

### C4: Expert Discovery typed sub-answer (latent) (size M)

- **Project / repo:** Datasec / Security Composer, datasecau/Datasec-Security-Composer
- **Fresh tickets (no merged PR names them):** PCOMP-12
- **Conditional (a merged PR names them; read the PR first):** none
- **Owned paths:** `apps/web/src/screens/Discovery.tsx`; `apps/web/src/screens/LaneC4*.test.tsx`
- **NOT yours:** apps/api/**, packages/api-contract/**, apps/web/src/screens/w3/**
- **Fix shape:** 12: typedDraftFor writes every declared sub-answer at the engagement level, so a device-group sub-answer cannot be answered per group (the API refuses with 400 since B30). Latent: both content releases declare 0 such sub-answers. Red-first test with the synthetic fixture's D-013, then per-group keying. The ticket says code-read only: Tuesday confirms the screen is not product-owner-look territory.
- **Proving checks:** scripts/ci.sh node step

## Records lanes (no repo path; owed work)

R1 (MPS records) and R2 (Composer records) are Jira/BACKLOG/C-entry work in the project root, not repo files; they own no repo path.

### R1: MPS records read, PR against ticket

Tickets whose merged PR title names them (Jira status Backlog at drafting; instrument: PR title regex over `pulls?state=closed&per_page=100` paginated to the end, 166 PRs, control: PR numbers run from #1 to #166 with no gap in the first/last):

MPSCALC-98 [#34]; MPSCALC-109 [#49]; MPSCALC-111 [#48]; MPSCALC-140 [#78, #74]; MPSCALC-147 [#69]; MPSCALC-150 [#73]; MPSCALC-156 [#50]; MPSCALC-157 [#50]; MPSCALC-158 [#77]; MPSCALC-160 [#97]; MPSCALC-162 [#59]; MPSCALC-163 [#58]; MPSCALC-170 [#64]; MPSCALC-173 [#47]; MPSCALC-177 [#44]; MPSCALC-178 [#47]; MPSCALC-189 [#100]; MPSCALC-194 [#79]; MPSCALC-203 [#81]; MPSCALC-254 [#133]; MPSCALC-258 [#134]; MPSCALC-269 [#145]; MPSCALC-306 [#91]; MPSCALC-358 [#150]; MPSCALC-359 [#155]; MPSCALC-371 [#148]; MPSCALC-377 [#151]; MPSCALC-381 [#156]; MPSCALC-382 [#157]

Fix shape: for each, read the PR and the ticket's Done-when; move to Done with a facts-only comment where met, comment and keep open where the PR says a half remains. Size: M. Needs Jira writes, so the kit must grant them.

### R2: Composer records read, PR against ticket

Tickets whose merged PR title names them (Jira status Backlog at drafting; instrument: PR title regex over `pulls?state=closed&per_page=100` paginated to the end, 115 PRs, control: PR numbers run from #1 to #118 with no gap in the first/last):

PCOMP-98 [#111]; PCOMP-116 [#114]

Fix shape: for each, read the PR and the ticket's Done-when; move to Done with a facts-only comment where met, comment and keep open where the PR says a half remains. Size: M. Needs Jira writes, so the kit must grant them.

## Exclusions (reasons; counts above)

**MPS explicit exclusions (read at source):**

MPSCALC-114 (product owner wants it printable? (ticket: no fix proposed)); MPSCALC-121 (words call (product owner)); MPSCALC-123 (needs a setting (coordinator call)); MPSCALC-130 (print look (product owner eyes)); MPSCALC-131 (customer-facing design decision); MPSCALC-132 (mock gap / design); MPSCALC-133 (records-repo process, no product code); MPSCALC-162 (hosted overlay read first (ticket) and PR #59 title names it); MPSCALC-163 (PR #58 title names it; under-load half stays open); MPSCALC-217 (two options (refuse boot or 503), not chosen); MPSCALC-223 (deploy-seat runbook against the hosted site); MPSCALC-288 (two designs offered, not chosen); MPSCALC-306 (layout choice (3 options), looks); MPSCALC-314 (ticket says the choice is open and unruled); MPSCALC-349 (needs an SDK that carries the tie; Note only); MPSCALC-359 (PR #155 landed the engine half; Api and screen halves wait on the 358 shape); MPSCALC-360 (needs the coordinator's confirmation first (ticket)); MPSCALC-364 (held for the product owner's word pack); MPSCALC-371 (word pack (ticket)); MPSCALC-372 (deploy-side store path); MPSCALC-383 (DATED 2026-11-12 (Dependabot code-scan question): not before its date)

Category counts: UNASSESSED seed rows 16-85 (spec seed 09-30) = 43; UNASSESSED feature lane V0-V11 (plan b308; descriptions not read) = 35; EXCL explicit = 21; EXCL needs a ruling (label) = 19; EXCL needs the product owner (question-for-kam) = 17; UNASSESSED (description not read) = 15; RECORDS: a merged PR title names it (read PR vs ticket, then move or comment) = 13; EXCL later phase = 5

**Composer explicit exclusions (read at source):**

PCOMP-9 (needs the VM / deploy); PCOMP-10 (deploy scripts live on the VM); PCOMP-11 (not small; contract bump); PCOMP-13 (environment (Docker host)); PCOMP-15 (Low, unmeasured: no defect shown); PCOMP-16 (environment (Docker host)); PCOMP-18 (found on the demo VM); PCOMP-21 (unmeasured, restore on the VM); PCOMP-25 (demo VM overlay); PCOMP-26 (registry digest risk, hosted pull); PCOMP-27 (dev volume ownership, machine state); PCOMP-28 (anonymous pull UNMEASURED hosted); PCOMP-64 (records only (Note)); PCOMP-65 (operator power Note for the product owner); PCOMP-66 (tied to held PR #85; product edit deferred); PCOMP-67 (branch of held PR #85); PCOMP-82 (decision (dates in UTC words)); PCOMP-83 (Blocker found by a seat, needs design); PCOMP-93 (demo way-back, coordinator accepted; deploy side); PCOMP-127 (each item waits on a go or the product owner's words (ticket))

Category counts: UNASSESSED sample-policy L-lane rows (seed; wait on reviewer answers per pickup line 37, RELAYED) = 29; EXCL explicit = 20; EXCL held (label) = 19; UNASSESSED (description not read) = 10; EXCL needs a ruling (label) = 2

Not assessed is not excluded: the feature lanes V0-V11 (MPS plan b308) and the Composer sample-policy L-lane rows are large; their descriptions were not read, so no claim is made about whether they need a ruling. A separate sweep should read them.

## Disjointness (program output)

Program: `build_lanes.py` beside this file. It expands each lane's owned globs against the origin tree (MPS 767 paths at main 31234f5f; Composer 1,037 at a54250f4, `truncated=false` both), then for every lane pair checks (a) a tree path matched by both, (b) literal equality, (c) nested stems when a wildcard is involved (conservative: may-overlap). Controls: a deliberately duplicated lane and a deliberately nested lane must be flagged, and every non-new glob must match at least one tree path.

| Project | Lanes | Pairs checked | Overlaps found | Globs matching 0 paths (non-new) | Control: duplicate flagged | Control: nested flagged | Ticket in 2 lanes (fresh) |
|---|---|---|---|---|---|---|---|
| MPS | 10 | 45 | 0  | 0 | True | True | none |
| Composer | 4 | 6 | 0  | 0 | True | True | none |

Conservation of the ticket census (every open non-epic ticket in exactly one class):

- MPSCALC: open non-epic 210, classified 210, classes {'UNASSESSED': 93, 'EXCL': 62, 'COND': 17, 'FRESH': 25, 'RECORDS': 13}
- PCOMP: open non-epic 91, classified 91, classes {'UNASSESSED': 39, 'EXCL': 41, 'FRESH': 7, 'COND': 4}

Limits of the proof: it proves path-disjointness of what the lanes OWN, from main's tree; it cannot see a file a seat decides to touch outside its list (the kit must say "any other path: STOP and ask"), and new files named by pattern (`LaneM4*.cs` and so on) are disjoint by their distinct stems only. M8 owns two sentences in files M11 would otherwise share (`docs/API.md`): API.md belongs to M11 alone.

## Not done / UNMEASURED

- Machine load for running up to 9 MPS lanes beside 4 Composer lanes: UNMEASURED; the dotnet job is 20 minutes on a hosted runner.
- Per-ticket readiness of the 93 UNASSESSED MPS and 39 UNASSESSED Composer rows: not read.
- Whether `npm run lint` covers `web/e2e` (M2): UNMEASURED.
- Whether the 29 title-named MPS tickets are residual-free: not read ticket-by-ticket (R1's job).

