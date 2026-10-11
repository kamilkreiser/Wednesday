From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to.

# BRIEF B202 (SEAT B): HPSM-POC — attribution KEYS in the data model (no revenue) + a "Preview: next phase" dashboard of Paul's five metrics for Tuesday's HP review
**From:** Friday, 12:59 2026-10-11. **Seat:** Datasec/HPSM-POC-B (newest `Briefs/` file containing `_SEAT-B_`). Report `Briefs/2026-10-11_B202_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · NEW WORDS · Records). Last line `READY FOR GATE` (head via ls-remote) or `STOPPED: NEEDS FRIDAY` + one question.
**Tier 1** (changes the data model: new columns/table + migration on both providers). A QA gate follows; then Kam sees screenshots; then Friday deploys. **Deploy is NOT in this brief.**

## AUTHORITY (Kam's rulings on Friday's board, verbatim: chosen option label + detail, with ruled_ts)
- `hpsmpoc-tuesday-dashboard-vs-next-phase-1011` → **(b) "Preview plus the keys"**: *"As (a), and the engagement id, partner id and revenue category added to the data model now (no revenue yet)."* — where (a) is *"A separate page labelled 'Preview: next phase', on seeded data; no new data model; real attribution stays next phase."* Ruled 2026-10-11T12:54:08+11:00. **This card is the governing ruling: it resolves the two below.**
- `hpsmpoc-attribution-demo-tuesday-1011` → **(c) "A live dashboard on seeded data"**: *"More work, and breaks the freeze."* Ruled 2026-10-11T12:50:47+11:00.
- `hpsmpoc-attribution-phase-1011` → **(a) "Next phase; roadmap now"**: *"The map becomes the roadmap entry; nothing built."* Ruled 2026-10-11T12:51:21+11:00. (Superseded in part by the governing card: the keys and the preview are built now; real attribution, revenue and HP data stay next phase.)
- `hpsmpoc-revenue-source-1011` → **(b) "Partners report their own wins"**: *"Easy to build, low trust as a measure of influence."* Ruled 2026-10-11T12:50:22+11:00.
- `hpsmpoc-customer-names-alias-1011` → **(a) "Keep names; alias wherever data leaves the partner"**: *"ORG-nnnnn on anything HP or an export sees."* Ruled 2026-10-11T12:50:18+11:00.
- `hpsmpoc-ranges-vs-exact-1011` → **(a) "Keep exact, show ranges to HP"**: *"Derive ranges for anything HP sees; cheap, loses nothing."* Ruled 2026-10-11T12:49:38+11:00.
- `hpsmpoc-industry-prioritise-1011` → **(a) "Display only for now"**: *"As built; revisit after HP's review."* Ruled 2026-10-11T12:51:24+11:00. (So: the preview MAY show industry as a column/filter; it must not change any score or priority.)
- `hpsmpoc-device-identifiers-1011` → **(b) "Drop or hash identifiers at import"**: *"Keep firmware version, model and counts; before any real customer upload."* Ruled 2026-10-11T12:50:15+11:00. **Seat D builds this (B203), not you.**

**Inputs (read first, in this project):** `Analysis/2026-10-11_hp-attribution-and-erd-map.md` (§2 Paul's five metrics, the attribution-key table, K-1…K-7); `Briefs/2026-10-11_B200_STATUS.md`. The HP forwards in git-ignored `Source_Documents/2026-10-11_hp-feedback-steve-inch/` are **HP CONFIDENTIAL**: you may read them in this seat; nothing from them goes into the code repo except the five metric names as UI labels (Kam ruled to show them) — no other wording, and no HP person's name anywhere in code, seed or screen.

## BASE (stacked)
- Branch **`b202/attribution-preview`** from **`b200/industry-field` @ `f18359b70060f2035238025ece0518966a356185`** — stacked because B200 and B202 both change the data model/contract. B200 is in QA gate B201 now; **if B201 asks for fixes, Friday re-bases B202** — keep your commits small and topic-separated so a re-base is mechanical.
- **STOP if `ls-remote` shows `b200/industry-field` ≠ `f18359b` or `main` ≠ `a50b22d7b1c51121f68235d02ccd0efeb97d058e`** at start or before push.
- Worktree `.tools/wt-b202`; scratch `.tools/b202/`; every code-repo ref write (fetch, worktree add, commit, push) under the shared lock `.tools/.git-lock` (copy `.tools/b201/lock.sh` to `.tools/b202/`; never remove another seat's lock).
- **Ports: 6660–6669 only** (all free at 2026-10-11 draft time; re-check with `lsof` before binding).

## PRIOR-WORK CHECK (cite file:line at f18359b in PRIOR WORK; Friday's read-only pointers below)
- **Data model:** `api/src/HpsmPoc.Modules.Assessment/Persistence/Entities.cs` — `AppUser` :12-24 (`EntraTenantId` :15 is the nearest thing to a partner org), `Customer` :26-46 (`StaffSize` :32, `PrinterCount` :34, `Synthetic` :35, `OwnerUserId` :36, `SeedKey` :37), `AssessmentRecord` :61-94, `UsageEventRow` :274, `ActionPlanRow` :300. `Persistence/AssessmentDbContext.cs` — DbSets :14-45, `Customer` config :124 (note `ck_customer_synthetic "synthetic = 1"`), `AssessmentRecord` :175, `UsageEventRow` :532. Migrations: `Persistence/Migrations/SqlServer/` and `/Sqlite/` (newest pair `*_ImportStore`, 20261006111224/111227; both `*ModelSnapshot.cs`).
- **Reporting module / metrics:** `Endpoints/ReportingEndpoints.cs:536-548` (`MetricsSummary`, the closest pattern for a dashboard read: one computation, roles Admin/Consultant/Demo); route `AssessmentModule.cs:255` (`/metrics/summary`, policy `Roles.MetricsSummaryPolicy`, `Identity/Caller.cs:29`, policy roles `AssessmentModule.cs:153`). Calculator `api/src/HpsmPoc.Modules.Reporting/Metrics/MetricsCalculator.cs`.
- **Navigation:** `web/src/components/shell/GlobalNav.tsx` — `NavItem` :19, `METRICS_ROLES` :23, `MAIN_NAV` :25-35 (`/revenue` "Revenue" :32 = the ILLUSTRATIVE calculator; `/metrics` "Automation metrics" :33). Tests `GlobalNav.test.ts`, `AppShell.*.test.tsx`.
- **Dashboard pattern:** `web/src/app/(app)/metrics/page.tsx`; `web/src/components/screens/MetricsDashboardScreen.tsx` (172 lines; summary `<dl>` :43, run table :78-96, load :118, role gate :159-167); `web/src/lib/metrics-dashboard.ts` (+ `.seeded.test.ts`).
- **Mock (offline parity):** `web/src/server/mock/api.ts:175` (`metricsSummaryRoute`), `web/src/server/mock/metrics-summary.ts` (+ test validating every 200 against the merged contract).
- **Seeding:** `api/src/HpsmPoc.Modules.Assessment/Showcase/ShowcaseSeeder.cs` (532 lines; `SeedKey = "showcase-v1"` :62, `ShowcaseOrigin "showcase seed (SYNTHETIC)"` :68, the four sample customers :95-108); `api/src/HpsmPoc.Api/Showcase/ShowcaseStartup.cs`; hosted demo seed `api/src/HpsmPoc.Modules.Assessment/HostedDemo/HostedDemo.cs:35` (`DemoSeedOptions`) + `api/src/HpsmPoc.Api/HostedDemo/HostedDemoStartup.cs`; wiring `api/src/HpsmPoc.Api/Program.cs:27-33`.
- **Contract:** `api/tests/HpsmPoc.Api.Tests/Contract/openapi.yaml` (0.15.0-draft after B200) ↔ byte-identical `web/contract/design-pack/api/openapi.yaml` + `openapi.merged.json`; `web/src/api/schema.gen.ts` (`gen:api`); `web/src/api/contract-drift.test.ts`; `Contract/PROVENANCE.md`, `web/contract/SOURCES.md`.
- **Synthetic banner precedent:** `web/src/components/shell/DemoNotice.tsx` (one banner per page, C-27 b).
- **Revenue calculator** `web/src/components/partner/revenue-model.ts:2` says *"ILLUSTRATIVE … never HP's financial model"*: **do not use it, or anything HP marks Restricted, as a source of seeded figures.**

## BUILD (red-first per behaviour; SQLite AND SQL Server)
1. **The attribution KEYS, no revenue** (as the map's key table proposes):
   - **Engagement id** — an opaque `ENG-<uuid v7>` that spans a customer's assessments across phases (the map: "add an engagement id, or define engagement = customer + first assessment"). Pick one, say why.
   - **Partner id** — an opaque partner-organisation id (e.g. `PTR-<uuid v7>`), carried where the map points (per user's tenant or per customer owner). **Not HP's partner id** (unknown scheme, next phase): name the column so a later HP id can sit beside it.
   - **Revenue category** — an enum of Paul's four: Hardware · Supplies · Solutions/Software · Services (DB check constraint + contract enum).
   - Nullable/additive; existing rows back-fill safely or stay null (state which). **Migration pair for BOTH providers, generated, up AND down, run on a copy of realistic data** (the showcase seed) on SQLite and on a fresh local SQL Server 2022 container on your port range; prove it is SQL Server (DB count / `@@VERSION` in the log, password masked).
   - No change to scoring, findings, reports, PDF bytes or any existing export (diff the result/PDF hashes base vs head on the seed).
2. **Partner-reported win record** (revenue-source ruling b) — **build it ONLY if the preview cannot read real keys without it.** Note: revenue category needs a row to live on, so a minimal read-only table of SEEDED wins (engagement id, partner id, masked customer, activity date, category, amount, `synthetic` flag with a `= 1` check constraint like `ck_customer_synthetic`) may be the minimum. **No create/edit endpoint or form for wins** — partner entry of wins is next phase. State in BLUF which you chose and why. If neither shape works without a write path, STOP.
3. **The page "Preview: next phase"** — a separate route (e.g. under `/metrics/…`), its own nav entry whose label contains "Preview" (roles as `METRICS_ROLES` unless you find a reason; say it), and a page title/eyebrow carrying the exact words **"Preview: next phase"**:
   - **Security Assessments Created** — from REAL data (`assessment.created_at`), by period, attributed by engagement / partner.
   - **Hardware / Supplies / Solutions-Software / Services Revenue Influenced** — from SEEDED, clearly **synthetic** data only; attribution by engagement, partner and revenue category.
   - **Customers shown only as aliases `ORG-nnnnn`** on this page and anything it exports (names-alias a). The alias must be **stable** (not recomputed from row order per request); choose stored vs derived and say why. No customer name in the endpoint body either (test it).
   - **Size and device counts as RANGES** derived from the exact `staff_size` / `printer_count` (ranges a); exact values stay stored and are never in this endpoint's body (test it). Range edges are NEW WORDS.
   - **Synthetic marking in the data AND on screen:** every seeded revenue row flagged synthetic in the DB; the page shows a persistent label (e.g. "SAMPLE: synthetic figures, not HP data") beside every revenue figure, not just once; seed key/origin marked SYNTHETIC like `ShowcaseOrigin`.
   - Seeded via the existing seed paths (showcase, and the hosted-demo seed so Friday can deploy it later) — **dev/demo only; the seed must refuse to run where the existing seeders refuse.**
   - Mock route + contract-validated test, so the page runs offline; Playwright at 1280 and 390; a11y spec on the page.
   - Contract: additive bump (0.16.0-draft) with a changelog paragraph; both copies byte-identical; `gen:api`.
4. **Screenshots** for Kam (mock build, 1440 + one phone): the page with the "Preview: next phase" label and the SAMPLE marks visible; the nav entry.

## FILE PARTITION
- **Yours:** the files above (data model, migrations, contract copies, reporting endpoint/module route, seeders, GlobalNav, new page/screen/lib, mock), plus their tests.
- **NOT yours — Seat D (B203, branch `b203/import-minimise` from main):** `api/src/HpsmPoc.Modules.Assessment/Ingest/*` (ImportReader, ImportEndpoints, ImportEvidence, Csv) and `api/tests/HpsmPoc.Api.Tests/Imports/**`, `api/tests/HpsmPoc.Modules.Assessment.Tests/Ingest/**`, worktree `.tools/wt-b203`, scratch `.tools/b203/`, ports 6670–6679. Do not edit the import tables' config in `AssessmentDbContext.cs` (~:270-370) or `ImportEntities.cs`.
- **NOT yours — Seat C (B201 QA gate on `b200/industry-field`):** `.tools/wt-C`, `.tools/b201/`, `Briefs/2026-10-11_B201_*`, its containers `b201-mssql-head-1` (127.0.0.1:6673) and `b201-azurite` (:6674). Never stop, reuse or remove them.
- **B200's own files** (Seat A, done; in the gate): only touch them where your feature needs it, and list each such touch in HOW so Friday's re-base is predictable.

## HOLDS
- No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool — Claude seats, subagents, the product's model, Ornith or the Spark — without HP's written approval (signed SOW §4.1.4(c)).
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert.
- No deploy, no Azure, no setting change; nothing to HP or any human.
- Never delete; quarantine.
- Never print a secret.
- Scoring/priorities unchanged (industry ruling a). No real revenue, no HP data feed, no HP partner id. No AI narrative touches the preview.

## REPORT
`Briefs/2026-10-11_B202_STATUS.md`: BLUF (which win-record choice and why; alias + range choices) · FOUND · TESTED (red-first logs, full API suite SQLite, SQL Server classes, vitest, typecheck, lint, build, Playwright, mutants, migration up/down both providers, base-vs-head result/PDF hash diff) · HOW (commits; every B200 file touched) · NOT TESTED · PRIOR WORK (file:line at f18359b) · **NEW WORDS** (table: string · where · why — nav label, page title, SAMPLE label, metric labels, range edges, category labels, alias format, API errors, contract changelog) · Records (evidence `Briefs/2026-10-11_B202_evidence/`, containers left, worktree). Last line `READY FOR GATE` + `b202/attribution-preview` head via ls-remote, or `STOPPED: NEEDS FRIDAY` + one question.

## FRIDAY'S RULING (on the drafter's conflict note)
The five metric NAMES (Security Assessments Created; Hardware / Supplies / Solutions-Software / Services Revenue Influenced) may appear as on-screen labels: Kam ruled a dashboard showing Paul's five metrics, and the names are generic business categories. **No other text from the HP-confidential forwards goes into the code repo** (no quotes, no ERD prose, no names of HP people); the forwards stay in git-ignored Source_Documents only.
