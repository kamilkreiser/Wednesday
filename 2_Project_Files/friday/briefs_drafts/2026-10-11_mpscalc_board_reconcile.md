# MPSCALC board reconcile: Datasec / MPS Commercial Calculator, 2026-10-11

**Drafted by:** read-only screening assistant for Friday. **Writes made:** this file only. Nothing was written to Jira, GitHub or the project.
**Sources read:** Jira search/jql (89 issues, every comment); GitHub PR list; `git ls-remote` and `log`/`show`/`grep` at `db8edfd`;
records branch `records/b30` (`CLARIFICATIONS.md` C-01 to C-13, `BACKLOG.md`; this is the newest records branch, and b12, b21 and b25 are its ancestors);
`00_QUESTIONS_FOR_KAM.md`; Briefs B16, B17, B26, B28, B30, B31, B32 and B33 (brief and STATUS files).

## BLUF
- **main = `db8edfd` = what the hosted site runs.** `ls-remote` shows refs/heads/main at `db8edfd5…`, and B33 STATUS:179 reads
  `DEPLOYED: db8edfd5082e49f9a1a1b3c23feeb02b36834b21 live-check 0`. PRs #1–#24 are all closed: 22 were merged, and #17 and #19 were
  superseded by #18 and #20. No PR is open. So **every shipped item is in main and deployed, and BUILT-NOT-DEPLOYED = 0.**
- **The board looks out of step for a reason:** 50 of its tasks are spec-level work packages (§-wide FR lists). The 30+ rounds
  moved most of them forward, but closed few of them in full. Seat comments on the tickets say "advances, not Done" many times,
  correctly.
- **Counts over the 87 open issues:**

| Disposition | Count | Keys |
|---|---|---|
| SHIPPED | **8** | 21, 22, 37, 38, 39, 56, 86, 89 |
| BUILT-NOT-DEPLOYED | **0** | none |
| ANSWERED | **0** | none (67 and 71 are already Done; every other question is only part-ruled) |
| OPEN-A | **37** | 26 tasks + 11 epics |
| OPEN-K | **36** | 20 questions + 12 tasks + 4 epics |
| OPEN-OTHER | **0** | none (golden values are the Pricing Owner's, but Kam names that person first: Q-09) |
| STALE / SUPERSEDED | **0** | none for certain (66 and 84 are close-candidates; see the notes) |
| UNSURE | **6** | 18, 20, 51, 52, 54, 57 (probably mostly shipped; not proposed for Done) |

- **Proposed moves to Done: 8 keys** (the SHIPPED rows). There are no other confident closes.
- Epic rule used here: an epic stays open while any child is open. It is OPEN-A if any child is OPEN-A, and OPEN-K otherwise.

## Reconcile table
Evidence abbreviations: **dep** = in main `db8edfd`, which is deployed (B33). PR numbers are GitHub PRs on `datasecau/MPS-Commercial-Calculator`.

| Key | Summary (≤ 70) | Disposition | Evidence |
|---|---|---|---|
| MPSCALC-1 | Epic: WP0 mobilisation & solution design | OPEN-A | Children 16 and 17 are open |
| MPSCALC-2 | Epic: Calculation service & workbook parity | OPEN-K | Children 19, 23, 24 and 25 wait on Q-09, Q-10 and Q-12; 21 and 22 are shipped |
| MPSCALC-3 | Epic: Shell, Dashboard & Guided Discovery | OPEN-A | Children 26–29 are open |
| MPSCALC-4 | Epic: Recommendation engine & Recommended Devices | OPEN-K | Children 30 and 31 need Q-14 (MPSCALC-80) |
| MPSCALC-5 | Epic: Fleet Workspace | OPEN-A | Children 32–34 are open |
| MPSCALC-6 | Epic: Hardware options & hardware BOM | OPEN-A | Purchase BOM shipped (#15, #16, dep); children 35 and 36 are open |
| MPSCALC-7 | Epic: Software configuration & software BOM | OPEN-A | 37–39 shipped; 40 is open |
| MPSCALC-8 | Epic: Price & Optimise | OPEN-A | Purchase pricing shipped (#15, dep); children 41–43 are open |
| MPSCALC-9 | Epic: Review, approval & immutable versions | OPEN-A | 44 and 46 are open; 45 is OPEN-K |
| MPSCALC-10 | Epic: Export & customer-safe outputs | OPEN-A | Children 47–49 are open |
| MPSCALC-11 | Epic: Administration & source governance | OPEN-A | 50 and 53 are open; 89 shipped |
| MPSCALC-12 | Epic: Security, roles & audit | OPEN-A | 56 shipped; 55 is open; 54 and 57 are UNSURE |
| MPSCALC-13 | Epic: Templates, reports, layout preview (appendix) | OPEN-K | 58–60 are unscheduled appendix scope |
| MPSCALC-14 | Epic: Platform, quality & delivery | OPEN-A | 61, 63, 64 and 65 are open; 62 is OPEN-K |
| MPSCALC-15 | Epic: Questions for Kam | OPEN-K | 20 child questions are open |
| MPSCALC-16 | Solution Design Pack (D01) | OPEN-A | Only ADR-001 and the registers exist; no D01 pack. Agents can draft it from the code as built |
| MPSCALC-17 | Decision log for the spec's open decisions (§30) | OPEN-A | CLARIFICATIONS and the Q register exist, but no one table maps the ten §30 decisions (UNSURE whether CLARIFICATIONS is enough) |
| MPSCALC-18 | Calculation rule catalogue (D05) | UNSURE | `docs/ENGINE.md` rule map R/B/S/X → code (dep). The rounding column waits on Q-12. Could close as SHIPPED after a human check |
| MPSCALC-19 | Golden calculation test suite | OPEN-K | ENGINE.md: every Excel expected value is "UNMEASURED". The Pricing Owner (Q-09) must produce them |
| MPSCALC-20 | Tier qualification by pricebook pool | UNSURE | R-03 in `QuoteCalculator.AppliedTier` (#1, dep). But a rental tier override has no reason or audit: PriceAudit covers purchase only (`QuoteEndpoints.cs:157`) |
| MPSCALC-21 | Configured capital, cost CPP, recommended/applied sell | SHIPPED | R-04…R-15 in `QuoteCalculator.FleetLineResult` (#1 7be7e37, dep); differential replica test |
| MPSCALC-22 | Finance annuity and recommended base | SHIPPED | R-09 `MonthlyFinance` and R-10 (#1 7be7e37, dep); 50-digit cross-check |
| MPSCALC-23 | Monthly cost, revenue, GP, GP%, contract value, GST | OPEN-K | Code shipped (R-17…R-22, #1, dep). The ticket asks to confirm the escalation step convention: Q-12 is open (C-09 ruled one part only) |
| MPSCALC-24 | Decimal arithmetic, rounding, calculation versioning | OPEN-K | Decimal maths and CalculationId shipped (dep). `RoundingPolicy.Unset` is waiting on Q-12 |
| MPSCALC-25 | Shared validation model and status codes | OPEN-K | `Issue(Severity, Code, Message, Target, Rule)` (dep) has no `canException`. Exception policy is Q-10 |
| MPSCALC-26 | Global application shell and design tokens | OPEN-A | Shell with Entra and banner shipped (#7, #12, dep). Left: left nav, stepper, accessibility (ticket comments 10-09, 10-10) |
| MPSCALC-27 | Autosave, offline/error states, optimistic concurrency | OPEN-A | Revision/STALE_REVISION and the file store shipped (#6). `autosave`/`debounce` give 0 hits in `web/src` at db8edfd |
| MPSCALC-28 | Dashboard quote work queue | OPEN-A | List and New quote form shipped (#6, #7, #24). Left: groups, filters, "my queue" (ownership now exists, C-12) |
| MPSCALC-29 | Guided Discovery cards, defaults, conditional questions | OPEN-A | Only the short New quote form (type, term, customer; #24) exists. No discovery cards |
| MPSCALC-30 | Rule-based device recommendation engine | OPEN-K | Not built. Thresholds and capability data are Q-14 (MPSCALC-80) |
| MPSCALC-31 | Recommended Devices screen, search and compare | OPEN-K | Depends on 30 and Q-14. Only the picker search exists (#7, #24) |
| MPSCALC-32 | Fleet grid: lines, sites, quantities, volumes | OPEN-A | Grid shipped (#7, dep). Left: bulk actions, import, governed sites, duplicate confirmation (comment 10-09) |
| MPSCALC-33 | Tier/base/click overrides with permission, reason, audit | OPEN-A | Purchase reason and audit shipped (B17 A-2, #15). Rental fleet overrides have permission only, with no reason or audit |
| MPSCALC-34 | Line status, grouped totals, sticky summary, debounce | OPEN-A | No debounce in web. Sticky summary and grouped totals not seen (UNSURE how much of it exists) |
| MPSCALC-35 | Hardware compatibility and option validation service | OPEN-K | Engine blocks incompatible and over-max options at calculation (B-04…B-09, dep), and #24 adds the G-3 purchase fit warning. Left: 42 inferred records W-12 (Q-11, MPSCALC-77) |
| MPSCALC-36 | Hardware drawer and generated hardware BOM | OPEN-A | Drawer, BOM and purchase BOM editor shipped (#7, #16, dep). Left: BOM editing rules, accessory dependencies |
| MPSCALC-37 | Software term-SKU resolution on term change | SHIPPED | S-01/S-02 in `QuoteCalculator.SoftwareLine` (#1, dep). The term resolves on every calculation, and there is no manual SKU selector |
| MPSCALC-38 | Software monthly sell/cost and quantity basis | SHIPPED | S-03/S-04 (#1, dep). W-04 ruled C-10 (keep parity and the flag), with no code change |
| MPSCALC-39 | Authentication-baseline dependency rule | SHIPPED | S-05 "AUTH MANAGER REQUIRED" in `WorkbookRules.cs` (#1, dep); golden-case 6 synthetic coverage |
| MPSCALC-40 | Software drawer, software BOM, expiry metadata | OPEN-A | Drawer and BOM shipped (#7). Left: expiry shown in the UI, dependency prompts (comment 10-09) |
| MPSCALC-41 | Commercial outcome cards and rate/base controls | OPEN-A | Cards shipped (#7, dep). Left: rate/base controls in the price view |
| MPSCALC-42 | Issues & Opportunities, Jump to Fix, What Changed | OPEN-A | Issues list and What changed shipped (#7). Left: Jump to Fix, opportunities |
| MPSCALC-43 | Recalculation states and calculation-failure handling | OPEN-A | Stale notice (#7) and the G-5 failed-recalculation fix (#23). Per-surface "Recalculating" is UNSURE |
| MPSCALC-44 | Readiness checklist and full validation on Review | OPEN-A | Submit refuses Blocking issues (API, #5). No Review-screen checklist with Jump to Fix seen (UNSURE) |
| MPSCALC-45 | Submit, approve, reject with immutable snapshots | OPEN-K | API and UI shipped (#5, #6, #7, #11, dep); C-12 bars self-approval. Left: approval routing and thresholds (Q-10, MPSCALC-76) |
| MPSCALC-46 | Post-approval versions, duplication, supersession | OPEN-A | new-version and Superseded shipped (#5). There is no duplicate route (the route list at `QuoteEndpoints.cs:41-55`) |
| MPSCALC-47 | Server-owned field registry and allow-list mapping | OPEN-A | `ProposalAllowList` shipped (#6, #15). Left: a general registry for every export |
| MPSCALC-48 | Customer Proposal and Customer BOM from snapshots | OPEN-A | Proposal from the approved snapshot shipped (#6, #18, #20, dep). Format ruled (C-13 card format = a, print-to-PDF). No customer BOM output yet |
| MPSCALC-49 | Internal Handover, Commercial Snapshot, export history | OPEN-A | DRAFT watermark shipped (#18, #20). No handover output, internal snapshot export or export history |
| MPSCALC-50 | Source version lifecycle and atomic activation | OPEN-A | Not built (BACKLOG: "activation = restart the API on a new store file") |
| MPSCALC-51 | Import and row-level validation per source type | UNSURE | Row-level validation shipped (#3 774b82d; comment 10-01). Not seen: W-13 supplies CPP at import, FR-ADM admin upload |
| MPSCALC-52 | Load the workbook's datasets as first source versions | UNSURE | Imported and live (#3; hosted reference MATCH, B33). But the ticket says "activate only after Pricing Owner review", which never happened (Q-09) |
| MPSCALC-53 | Administration console (role-separated) | OPEN-A | Inventory screen shipped (#16, dep). No sources, templates or audit admin |
| MPSCALC-54 | Role and permission model enforced server-side | UNSURE | Four Entra app roles enforced (#11, dep); I-2 ruled (C-13 price-edit = a). The spec names six roles; only four exist |
| MPSCALC-55 | Audit event trail | OPEN-A | Price and inventory audit shipped (#15). No lifecycle or source-governance events (FR-REV-007) |
| MPSCALC-56 | Authentication (Entra ID SSO) | SHIPPED | API (#11 9fe66dc) and web (#12 98d829f); hosted behind Entra since #10 (B14 A-7 comment); dep |
| MPSCALC-57 | Customer-safe leakage and security tests | UNSURE | Extensive tests in both auth modes (#6, #11, #15, #18, dep). Each new export (48, 49) will need its own |
| MPSCALC-58 | Template Library and Template Designer | OPEN-K | Not built. Appendix scope, unscheduled; template wording waits on decision #4 |
| MPSCALC-59 | Reports Dashboard and Quote Performance | OPEN-K | Not built. Appendix scope, unscheduled |
| MPSCALC-60 | Customer Quote Layout Preview | OPEN-K | ProposalPage preview exists (#18). The spec preview is appendix scope, unscheduled |
| MPSCALC-61 | Repository, CI/CD, CodeQL and security scanning | OPEN-A | CI build-only (#10) and CodeQL on 3 languages (C-11). No dependency scanning or DAST (`.github` holds ci.yml only); the org setting is Friday's |
| MPSCALC-62 | Hosting, environments and infrastructure-as-code | OPEN-K | One showcase environment, deployed (#10, B33). Dev/Test/UAT/Prod and backup need Kam's go (Azure cost) |
| MPSCALC-63 | NFR: accessibility, locale, performance, observability | OPEN-A | No WCAG audit, p95 measurement or structured-log work recorded. Scale is Q-17 |
| MPSCALC-64 | Test strategy: unit, API, UI, e2e and UAT | OPEN-A | Unit, API, Vitest and Playwright layers exist. Left: a11y tests and the UAT plan; the pricing-team UAT follows Q-09 |
| MPSCALC-65 | Documentation and handover (D12–D14, App D) | OPEN-A | API, ENGINE, IMPORTER and DEMO docs exist. No admin, pricing or approver guides; `docs/DEMO.md:14,60,75` is still stale on the footer (B21-3) |
| MPSCALC-66 | Q-00 The rest of your 30 Sep note | OPEN-K | Q register: OPEN. Close-candidate as stale: Kam has ruled 30+ cards since |
| MPSCALC-68 | Q-02 Partner product model | OPEN-K | Deferred by C-05 ("partners later") |
| MPSCALC-69 | Q-03 Brand and ownership: HP Solutions Centre | OPEN-K | Kam's logo and hero are in use (B16 A-5). HP brand use is not ruled (B26 §6) |
| MPSCALC-70 | Q-04 Who builds it and by when? | OPEN-K | No ruling; agents build de facto |
| MPSCALC-72 | Q-06 Relation to HPSM | OPEN-K | OPEN |
| MPSCALC-73 | Q-07 Relation to Datasec's commercial platform (D11) | OPEN-K | OPEN |
| MPSCALC-74 | Q-08 Price books: refresh cadence and permission | OPEN-K | Validity ruled (C-07) and edit permission ruled (C-13). Open: cadence, BID permission, P-04 |
| MPSCALC-75 | Q-09 Pricing Owner, Pricing SME and approvers | OPEN-K | OPEN. The B31 approver account is a test identity, not this ruling |
| MPSCALC-76 | Q-10 Approval thresholds and exception policy | OPEN-K | Self-approval ruled (C-12). Thresholds and exceptions are open |
| MPSCALC-77 | Q-11 Workbook defects: fix or keep for parity? | OPEN-K | W-04 ruled (C-10). W-01, W-12, W-08 and W-10 are open |
| MPSCALC-78 | Q-12 Escalation and rounding conventions | OPEN-K | HP Buy rounding ruled (C-09). Escalation and money/CPP decimal places are open |
| MPSCALC-79 | Q-13 Service costs and service levels | OPEN-K | OPEN. Care packs are manual items by default (#13, B17), which is not a ruling |
| MPSCALC-80 | Q-14 Device recommendation rules and data | OPEN-K | OPEN |
| MPSCALC-81 | Q-15 Output formats, draft wording, sharing | OPEN-K | Format and footer ruled (C-13; B16 A-4: print-to-PDF, ex-GST, approved = "Commercial in confidence"). The sharing integration is not ruled, so this is a close-candidate |
| MPSCALC-82 | Q-16 Retention and audit periods | OPEN-K | OPEN |
| MPSCALC-83 | Q-17 Fleet size and concurrency | OPEN-K | OPEN |
| MPSCALC-84 | Q-18 Technology stack | OPEN-K | The build runs on the spec default (.NET 10 + React), but Kam has not confirmed it. Close-candidate as superseded by the build |
| MPSCALC-85 | Q-19 Re-send the Developer Specification file | OPEN-K | OPEN (BACKLOG: the .docx is truncated) |
| MPSCALC-86 | Currency model: AUD only in release 1 | SHIPPED | ADR-001; `CurrencyRegistry.Release1` (#1 7be7e37, dep); C-04 |
| MPSCALC-87 | Q-20 FX rates for non-AUD quotes | OPEN-K | OPEN; needed only for a second currency |
| MPSCALC-88 | Q-21 Next currencies, tax, rounding per currency | OPEN-K | OPEN; needed only for a second currency |
| MPSCALC-89 | Source import rules from the price-book register | SHIPPED | Every rule built (comment 10-01, b03/importer) and merged as #3 774b82d. Hosted reference.json MATCH (B33). The 10-01 comment's "not Done until merged" condition is now met |

## Proposed transitions, for a seat to apply later (move to Done, comment first, read back)
Each comment is one line. None quotes a price.
- **MPSCALC-21:** `Reconcile 2026-10-11: SHIPPED. R-04…R-15 in QuoteCalculator.FleetLineResult, PR #1 (7be7e37), in main db8edfd, deployed (B33 STATUS: DEPLOYED db8edfd live-check 0).`
- **MPSCALC-22:** `Reconcile 2026-10-11: SHIPPED. Annuity R-09 (MonthlyFinance) and recommended base R-10, PR #1 (7be7e37), in main db8edfd, deployed (B33).`
- **MPSCALC-37:** `Reconcile 2026-10-11: SHIPPED. Term-SKU resolution S-01/S-02 (QuoteCalculator.SoftwareLine), PR #1, in main db8edfd, deployed (B33).`
- **MPSCALC-38:** `Reconcile 2026-10-11: SHIPPED. Software sell/cost S-03/S-04, PR #1; margin treatment ruled C-10 (parity, keep MARGIN REVIEW); in main db8edfd, deployed (B33).`
- **MPSCALC-39:** `Reconcile 2026-10-11: SHIPPED. AUTH MANAGER REQUIRED rule S-05 (WorkbookRules), PR #1, in main db8edfd, deployed (B33).`
- **MPSCALC-56:** `Reconcile 2026-10-11: SHIPPED. Entra SSO API PR #11 (9fe66dc) + web PR #12 (98d829f); hosted showcase signs in with Entra (B14 ADDENDUM-7); in main db8edfd, deployed (B33).`
- **MPSCALC-86:** `Reconcile 2026-10-11: SHIPPED. Currency model per ADR-001, AUD only (CurrencyRegistry.Release1), PR #1 (7be7e37), in main db8edfd, deployed (B33). FX and next currencies stay on MPSCALC-87/-88.`
- **MPSCALC-89:** `Reconcile 2026-10-11: SHIPPED. Importer rules merged as PR #3 (774b82d), so the "not Done until merged" condition of the 2026-10-01 comment is met; hosted reference store read-back MATCH (B33).`

**Not proposed: the six UNSURE rows (18, 20, 51, 52, 54, 57).** A human check could close 18, 51 and 57. 20 and 54 have a known
gap each, and 52 has a "Pricing Owner review before activation" condition that was never met.
**Kam one-tap close-candidates (OPEN-K; ask him, do not close):** 66 (stale), 81 (only sharing integration left) and
84 (the stack is de facto chosen).

## OPEN-A: file-disjoint lanes
The contract (`docs/api/openapi.json`, `docs/API.md`, `web/src/api/generated/**`) and `src/MpsCalc.Api/Program.cs` are shared
by every API change. So **only one API-plus-contract lane runs at a time**. A1 runs first and A2 rebases on it. The other lanes
are disjoint from each other and from A1.

| Lane | Keys | Files (main write set) | Notes |
|---|---|---|---|
| **A1: API quote lifecycle & audit** (Seat A) | 46 (duplicate), 55 (lifecycle audit events), 33 (rental override reason + audit, API half), 47 (general field registry), 49 (export-history API half) | `src/MpsCalc.Api/Quotes/{QuoteEndpoints,QuoteStore,QuoteFileStore,PriceAudit,Proposal}.cs`, contract | Retention periods are Q-16; record the default and do not decide it |
| **A2: Source lifecycle & admin API** (after A1) | 50, 53 (API half) | `src/MpsCalc.Api/Sources/**`, new admin endpoints, contract | `src/MpsCalc.Import/**` is frozen. Activation must keep the B27-H1 HOLD on store paths |
| **A3: Overlay store residue** (Seat A, can run beside A1) | *not on the board:* BACKLOG B27-H1…H4 (H1 lifts the hosted-path HOLD) | `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs`, `tests/…/OverlayGateFindingsTests.cs` | Suggest Jira keys. Disjoint from A1 only if A1 leaves `Inventory/` alone |
| **B1: Shell, dashboard, discovery** (Seat B) | 26, 28, 29 | `web/src/components/Shell.tsx`, `web/src/screens/{Dashboard,NewQuoteForm}.tsx`, a new Discovery screen | 29's defaults: workbook defaults. Service costs stay Q-13 |
| **B2: Quote editing screens** (Seat B2, or after B1) | 27, 32, 34, 36, 40, 41, 42, 43 (+ BACKLOG B32-J7 test, B32-J6 390 px) | `web/src/screens/{QuoteScreen,FleetGrid,PriceView,saveDraft}.*`, `web/src/screens/bom/**` | The UI half of 33 lands here after A1 |
| **B3: Review checklist** | 44 | `web/src/screens/Lifecycle.tsx` (+ test) | Jump to Fix wiring touches QuoteScreen: hand it to B2 or sequence after it |
| **C: Proposal & exports (web)** | 48 (customer BOM), 49 (handover / commercial snapshot outputs, web half) | `web/src/proposal/**`, `web/src/screens/ProposalPage.tsx` | Needs A1's registry (47) for bindings, so start it after A1 merges |
| **D: Platform & docs** (Seat C) | 61, 65, 64 (a11y + UAT plan), 63 (measure-first: a11y and p95 audit, no product edits) | `.github/**`, `docs/{DEMO,ENGINE,IMPORTER}.md`, new `docs/guides/**`, `web/e2e/**` (new a11y specs only) | 61's dependency scanning is an org setting (Friday/Kam). Also fix B21-3 (the DEMO.md footer) and BACKLOG B31-ENTRA5 (`scripts/entra_apps.py`) here |
| **R: Records only** (Friday or a records seat) | 16 (D01 pack), 17 (§30 decision table) | `1_Project_Definition/**` on a records branch | No code-repo write |

## Notes and caveats
- **Kam rulings missing from CLARIFICATIONS.** The three 2026-10-11 card rulings (accessory fit = b, markup precedence = b,
  New quote form = a; B30 brief AUTHORITY) have no C-number in `records/b30`, whose file ends at C-13. The B31 approver-account
  name ruling is also not recorded. A records seat should add them (C-14 onward) before these tickets cite them.
- The OPEN-A/OPEN-K split on partial tasks is this reader's judgement of what blocks the **remainder**. Shipped parts are cited
  in each row so a seat can comment progress without closing.
- Unpinned: whether Kam saw and accepted the B28/B30 NEW WORDS on the hosted site before relying on them. This does not change
  any disposition here.
- Root-main records are behind `records/b30`: the working copy of `CLARIFICATIONS.md` ends at C-11. Read the branch, not the
  working copy.
