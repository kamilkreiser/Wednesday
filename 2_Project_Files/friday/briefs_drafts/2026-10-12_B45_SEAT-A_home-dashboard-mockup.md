From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies to friday-laptop-agent@agentmail.to (no mail key in this project: your STATUS file is the wrap).
# BRIEF B45 · SEAT-A: Home screen MOCKUP (design records only, no product code): a one-page KPI home for the calculator, rendered to PNG at 1440 and 390 plus a one-page PDF pack for Kam
**Written:** @NOW@. **Pane:** `Datasec/MPS-A`. Your commission is the newest file in `Briefs/` containing `_SEAT-A_`.
(Launcher check, read by the draft writer: `Launch_Claude.command:107` sets `SEAT` from a pane name matching `*MPS*-?`; `:111` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". At drafting the newest `_SEAT-A_` file is `2026-10-12_B40_SEAT-A_source-lifecycle-admin-api.md`, finished: `B40_STATUS.md` last line `READY FOR GATE: b40/source-lifecycle-admin-api 70c8172…`, merged in PR #27.)
**Seat:** Seat A (Claude design seat). **MOCKUP ONLY.** One static HTML/CSS mock, its PNGs, one PDF, a tokens list, a words list, your STATUS. Nothing in `2_Project_Files` changes.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B45_STATUS.md`. Its last line is exactly one of:
- `MOCKUP READY: 1_Project_Definition/Design/2026-10-12_home-dashboard/2026-10-12_MPS-home-mockup_FOR-KAM.pdf` (records main @ `<sha>`);
- `STOPPED: NEEDS FRIDAY` and ONE question.

## AUTHORITY
- **Kam, verbatim** (live board 2026-10-12 11:54:31, view=friday): *"Please create a proper Home Screen for the MPS calculator.  Make the dashboard a single view that provides a snapshot or key metrics - Quotes provided and an ability to click through, total value of quotes out, quotes past a certain time range requiring follow up, deals closed this month and Year to date.  Look at the vision_Sales_Portal for inspiration but improve where you can.  Do this as a priority please and let me know once you have a mockup and once its live"*
- **This round is the mockup.** Kam approves it before any build. Friday tells Kam "mockup ready" from your STATUS; you tell no human anything.
- **Spec tension, carried, not decided by you:** spec FR-DB-001 *"The Dashboard MUST be a pricing work queue rather than an analytics-first dashboard."* and FR-DB-003 (groups Drafts, Awaiting Approval, Rejected, Recently Approved, Ready to Export) (`Source_Documents/2026-09-30_from-Kam_renderings/Developer_Specification_and_SOW_v1.0_TEXT.md:211`, `:213`). Kam's request is newer and asks for metrics. **The mock therefore puts the KPI strip on top and keeps a work queue below it** (Friday's default), and the PDF says so in one line for Kam to overrule.

## READ WHOLE FIRST (all inside this project; you read no other project)
- The project `CLAUDE.md`; `1_Project_Definition/CLARIFICATIONS.md` on records `main` (C-04 AUD `:47`, C-05 internal users `:62`, C-12 ownership `:168`).
- On code `origin/main` (`git -C 2_Project_Files show b28c95eb:<path>`, read verbs only): `web/src/styles.css` (150 lines, whole), `web/src/screens/Dashboard.tsx` (121), `web/src/components/Shell.tsx`, `web/src/app/router.ts` (44), `web/src/format/decimal.ts` (`formatMoney` `:43-44`, AUD).
- Spec §5 (design system, `…_TEXT.md:159-172`), §6 Dashboard (`:197-220`), Reports (`:695-712`) and its two reference images `Source_Documents/2026-09-30_from-Kam_renderings/spec_media/media/image1.png` (Dashboard) and `image13.png` (Reports Dashboard). Layout ideas only.

## STYLE RULE (hard): style guides are never mixed
A palette is a client's / product's identity. **Vision Sales Portal's colours, logo, fonts, icon set and brand tokens are NOT used, copied or approximated.** The ideas below are layout and behaviour only. The calculator has its own look:
- **Source of truth = the live app's tokens, `web/src/styles.css:1-19` on `b28c95eb`:** `--bg #f4f6f9`, `--surface #ffffff`, `--text #1b2430`, `--muted #5d6b7c`, `--line #dde3ea`, `--brand #0b3a6f`, `--brand-ink #ffffff`, `--accent #1565c0`, `--ok-bg/--ok-ink #e6f4ea/#1e6b34`, `--warn-bg/--warn-ink #fff4e0/#8a5300`, `--bad-bg/--bad-ink #fdecea/#a4262c`, `--banner-bg/--banner-ink #7a1f1f/#ffffff`, `--internal-bg #f3effb`; font `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif` (`:19`), 14 px base (`:20`).
- Existing raw hexes outside tokens (measured): `.badge-draft` `#e8eef7` (`:77`), `.card.warn` `#e0a400` (`:103`). Existing tile shape to reuse: `.cards / .card / .card-value / .card-label` (`:100-105`); badges `:76-79`.
- **Not sources:** the spec's token table (`…_TEXT.md:163-172`, e.g. navy `#0B2E4F`: differs from the built `--brand`; reference only), and `web/src/proposal/proposal.css` `--pd-*` (`:6-12`: the customer proposal document's palette, not app chrome).
- **Write the token list FIRST** (`tokens.md`, ITEM 1): every colour in the mock resolves to a `styles.css` token or a listed raw hex above; anything else (e.g. the "needs a ruling" marker, the SAMPLE ribbon) is a **NEW token, named and marked NEW for Kam**, built from an existing value where possible. A check (ITEM 4) proves no other hex appears in the mock.
- **Dark theme: none exists** (`grep -c -i 'prefers-color-scheme\|data-theme'` on `styles.css` = **0**). Render **light only**; do not invent a dark theme.

## PRIOR WORK (measured by the draft writer)
- **A home already exists: `Dashboard.tsx`, titled "Quotes"** (`:56`, `:71`), routed as `#/` (`router.ts:4`, `:16`, `:21-22`; `App.tsx:17`). It is the B08 work queue (MPSCALC-28 UI half, `:1`): one table, columns Quote ref · Customer · Status · Version · Updated (`:92-98`), Refresh and (Seller only) New quote (`:73-78`), a link per quote ref to the quote screen (`:105`). **No tiles, no groups, no filters, no search, no values, no owner column.** An identity with neither Seller nor Approver (e.g. Administrator only) gets no list call and a "Your roles do not include quotes." line plus an inventory link (`:10-12`, `:52-66`).
- The shell nav calls this page **"Quotes"** (`Shell.tsx:22`); the brand link also goes to it (`:18`). Nav holds Quotes and (by role) Inventory only.
- FR-DB-003 groups, FR-DB-004 row fields (owner, term, device count, monthly value), FR-DB-005 filters: **not built** (absent from `Dashboard.tsx`).
- Open defect on this page: `[B32-J6]` page-level horizontal scroll at 390 px on the quote screen and dashboard (records `main:BACKLOG.md:312-319`). **The 390 mock must not scroll sideways** (ITEM 4 measures it).

## VISION INSPIRATION (studied by the draft writer, read-only; Vision `2_Project_Files` HEAD `ef5a9c0`, `public/pro/dashboard.html` + `public/pro/js/pro-dashboard.js`)
Take (layout/behaviour only):
- **KPI strip of six count tiles** with tone variants (neutral / warn / good): Open opportunities, Active quotes, Awaiting approval, Quotes expiring ≤ 7d, PoCs in flight, Reminders due ≤ 7d (`dashboard.html:15-21`).
- **"Needs actioning" list**, one row per item with an Open button, ordered by kind: approval → overdue reminder → expiring quote → stale lead (`pro-dashboard.js:78-120`, order `:113`), with a count hint ("N items need attention", `:116-117`). This is the shape for Kam's follow-up metric.
- **Tabbed pipeline table** (Tracker / Quotes / Reminders) with customer search and a stage filter whose options follow the live data (`dashboard.html:36-53`; `pro-dashboard.js:156-162`); the Quotes tab columns Quote # · Customer · Scenario · Total · Status · Valid until · Owner (`dashboard.html:70`).
- **"Coming up, next 14 days" rail** (`dashboard.html:90-91`) and **pipeline-by-stage bars**, sorted by count (`pro-dashboard.js:143-150`).
- **One call feeds the whole page** (`server/routes/pro.js:23` "GET /api/pro/overview: everything the PRO dashboard needs in one call") and an "updated HH:MM" stamp (`pro-dashboard.js:57`).
Improve (each one appears in the mock):
1. **Tiles are not clickable**: plain `<div class="kpi">` (`dashboard.html:16-21`), 0 click handlers on `.kpi` in `pro-dashboard.js`. **MPS: every tile is a link to the filtered quote list** (Kam: "an ability to click through").
2. **Counts only, no money, no period**: no tile carries a value and there is no month / year toggle (KPI fill `pro-dashboard.js:51-56`). **MPS: value under each count; a This month / Year to date switch on the closed tiles.**
3. **US money by default**: `Intl.NumberFormat('en-US', … currency: cur || 'USD')` (`pro-dashboard.js:232`). **MPS: AUD, ex GST, via `formatMoney` (C-04).**
4. **One failure blanks the page**: a non-OK overview call replaces every panel with "Overview API unavailable." (`pro-dashboard.js:43-46`). **MPS: each tile has its own unknown/error state** (show one tile in that state in the mock).

## MPS DATA: what a quote holds today (code main, measured)
`git -C 2_Project_Files ls-remote origin main` = **`b28c95eb0f73ed0ce7ae410791feefc8b1a059ea`** (PR #27, parent `44374606`). Local `HEAD` is `7f6ca4c` (not main): read by sha, never by working tree.
- **Statuses:** server `VersionStatus` = Draft, Submitted, Approved, Superseded (`src/MpsCalc.Api/Quotes/QuoteStore.cs:8-14`). The list and quote show the current version's status, enum Draft | Submitted | Approved (`docs/api/openapi.json` `QuoteSummary.status`, `Quote.status`). Reject returns a version to Draft (`openapi.json` `rejectQuote` summary).
- **No outcome state:** whole-word, case-insensitive counts over `src web/src docs` at `b28c95eb`: `won` **0**, `Won/Lost` **0**, `lost` **1** (not a quote outcome); `closed` 13 and `expired` 30 all name schema/fail-closed/source expiry, none a quote. Control `Approved` = **49**. **Nothing records a won, lost or closed deal.**
- **List endpoint:** `GET /api/v1/quotes` (operationId `listQuotes`): Seller or Approver; one row per quote, current version, ordered by updatedAt desc; **"Carries no price, cost, calculation or snapshot content for any role. Release 1 lists every quote: ownership is open (gate B04 F-12; Q-10)."** Row (`QuoteSummary`): `quoteId`, `quoteRef`, `customer`, `status`, `versionId`, `versionNumber`, `updatedAt`, `callerCan`, `ownerName` (display name; absent on pre-owner quotes). **No created, submitted, approved or sent date; no value; no owner id.**
- **Per quote:** `GET /api/v1/quotes/{id}`: adds `termMonths`, `currency`, `submittedSnapshotId`, `approvedSnapshotId`, `rejectionReason`, `versions[]` (with Superseded), `lifecycleEvents` (kinds created, submitted, approved, rejected, new-version, proposal-generated…, each with `at`) **sent only with internal-metrics** and only on quotes since B35 (`openapi.json` `Quote.lifecycleEvents`).
- **Value:** `GET /api/v1/quotes/{id}/proposal` (Seller or Approver, same body for every role, customer-safe): `monthlyChargeExTax/IncTax`, `contractValueExTax/IncTax` (rental), `purchaseTotalExTax/IncTax` (purchase), `quoteMode`, `snapshotDate`, `validityDays`, `isDraft`; **409 PROPOSAL_NOT_AVAILABLE** with no current calculation. Approved date: `Snapshot.createdAt` (`GET /api/v1/snapshots/{id}`; `Contracts/Dtos.cs:315`).
- `validityDays` (1–365) is **"stored and shown, not enforced"** (`docs/API.md:153`; `Dtos.cs:76`).

## THE FIVE METRICS (draft writer's mapping; the mock labels each tile with its row's marker)
| # | Kam's metric | Today | Needs | Marker on the tile |
|---|---|---|---|---|
| 1 | Quotes provided + click-through | **Count computable** from `listQuotes` (`status`). Click-through to one quote exists (`router.ts:26`). | **Ruling:** "provided" = current version Approved (proposal final, `isDraft` false)? The app has no "sent to customer" act. **New:** a filtered-list route (router has no query, `:9-17`), e.g. `#/quotes?status=…`. | `SAMPLE` + `needs: Kam's ruling on "provided" (Approved, or a new Sent step)` |
| 2 | Total value of quotes out | **Not from the list** (no price on `listQuotes`). Per quote via `/proposal` (N calls; 409 when uncalculated). | **New field:** a value on the list row, e.g. `QuoteSummary.valueExTax` + `valueBasis` (contract \| purchase), or one summary endpoint. **Ruling:** which value (rental contract value = monthly × term, or monthly) and which statuses count as "out". Default proposed: ex GST, rental contract value + purchase total, statuses Approved (and not closed). | `needs: a value on the quote list + Kam's ruling on which value` |
| 3 | Past a time range, needs follow-up | **Not computable from the list** (only `updatedAt`). Approved date exists per quote (snapshot `createdAt`; `approved` event, internal-metrics only). | **New field:** `approvedAt` (or `sentAt` if a Sent step is ruled) on the list row. **Ruling:** the threshold. **Default proposed: 14 days since approved, configurable** (Vision's rail is 14 days; validity is not enforced, so it is not the trigger). | `needs: Kam's choice of days (default 14)` |
| 4 | Deals closed this month | **Not computable**: no won/lost/closed state (counts above). | **New:** an outcome on a quote, `outcome` = Open \| Won \| Lost, `outcomeAt`, who set it, and an action to set it (Seller owner? Approver?). | `needs: a Won/Lost outcome on a quote (Kam's ruling)` |
| 5 | Deals closed year to date | As 4. | As 4, plus **ruling:** calendar year or Australian financial year (from 1 July). | `needs: a Won/Lost outcome on a quote (Kam's ruling)` + `needs: calendar or financial year` |

## ROLES (from the role model, measured)
- Quote reads need **Seller or Approver**; Administrator alone gets 403 (`docs/API.md:42-43`); the page already gives that identity no list (`Dashboard.tsx:10-12`). Personas: Seller · Approver · Pricing analyst (Seller+Approver+internal-metrics) · Administrator · Administrator+Pricing analyst (`web/src/auth/dev/devPersonas.ts:10-30`).
- Ownership: owner = creator; edit/calculate/submit owner only; approve/reject refuse owner and submitter (`docs/API.md:44-50`). The list is open to every quote role (`listQuotes`), and carries `ownerName`, not an owner id; `callerCan.approve` marks rows this caller may approve.
- **Mock, three panels (Friday's default, Kam to confirm):** **Seller**: tiles default to **My quotes** with an All switch (needs a "mine" flag on the row: **new field**, e.g. `QuoteSummary.isMine`; `ownerName` is not unique); **Approver**: all quotes plus an **Awaiting my approval** tile (from `callerCan.approve`, computable today); **Administrator only**: no quote tiles (today's rule); the mock shows the current fallback line and marks `needs: Kam's ruling if Administrators should see the metrics`.
- **No GP, margin or cost on any tile** (spec FR-DB-010 `:220`, FR-RPT-005 `:708`); the values used are the proposal's customer-safe ones.

## ITEMS
**Records route (measured):** `BACKLOG.md` lives at the project root, so the records repo is the **project-root** git repo; `.git/config` has **0** remotes: **commit only, push nothing**. Records `main` = **`38efff2f5d993ea0b9520938c7c59dec7123e5a8`** (B44's fold, `B44_STATUS.md` last line); tracked status clean (0 lines, `--untracked-files=no`). `1_Project_Definition/Design/` does not exist yet. Work in a worktree: `git -C <root> worktree add .tools/wt-B45-design -b records/b45 main` (`chmod 700`).
1. **`tokens.md`** first: every colour and font the mock uses, each → its `styles.css` token and line, or NEW (name, value, why). Commit.
2. **`home-mockup.html`** + `home-mockup.css` (static, no script, no external URL, no web font, no image from Vision). One page:
   - Shell as built (brand bar `--brand`, nav). Page title and nav word for Kam: propose **Home** (nav: Home · Quotes · Inventory); list it as a NEW word.
   - **KPI strip, five Kam tiles + Awaiting my approval**, each a link (show `href` targets in the PDF notes): count, AUD value ex GST, one-line definition; This month / Year to date switch on tiles 4–5; each marker from the table above as a visible small tag; one tile shown in its unknown/error state.
   - **Needs follow-up list** (Vision's "Needs actioning" shape): quote ref, customer, owner, days since approved, value, one primary action.
   - **Work queue below** (FR-DB-003 groups as tabs or headings: Drafts · Awaiting approval · Rejected · Recently approved), columns per FR-DB-004 where data exists; mark owner/term/device count/value columns `needs:` where the list lacks them.
   - Role switcher shown as three static panels or three renders (Seller, Approver, Administrator only).
   - **Every number is fake and visibly marked SAMPLE** (a ribbon on the page and the word SAMPLE on each tile); synthetic customers only (e.g. "Sample Customer A"); no real customer, person or price-book value.
3. **Renders** with the installed browser, no install, bind nothing (file:// only): `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --screenshot=<png> --window-size=<w>,<h> file://…` at **1440** and **390** wide, one per role panel that differs; light only. Then **one PDF page** for Kam (`--print-to-pdf`, or an HTML pack page holding the 1440 Seller render, the 390 render, the five-metric marker table, the new words, and the one-line FR-DB-001 note) at `2026-10-12_MPS-home-mockup_FOR-KAM.pdf`. If Chrome is absent or fails, **STOP: NEEDS FRIDAY** (do not install anything).
4. **Checks:** (a) colour check: extract every `#hex`/`rgb()` from the mock files; each is in `tokens.md` (ratio, with a planted off-palette hex as a control that fires); (b) 390 px: `scrollWidth ≤ clientWidth` via a headless `--dump-dom` of a tiny inline measurement or an equivalent you state, with a control (a 600 px element) that fires; (c) SAMPLE present on every tile (count / tiles); (d) no Vision asset: `grep -i -c` for `vision`, `bootstrap-icons`, `bi bi-`, `cp-` in the mock = 0, control on a file that contains one.
5. **`NEW_WORDS.md`**: every user-visible word or phrase on the mock that is not already in the built UI (grep `web/src` at `b28c95eb`, `-i`, to prove it is new), as a table: word · where · why; Kam approves these.
6. Commit all files under `1_Project_Definition/Design/2026-10-12_home-dashboard/` on `records/b45` (message `Design: MPS home screen mockup for Kam (B45)`), then fold: if root tracked status is clean and `main` is an ancestor of `records/b45`, `git -C <root> merge --ff-only records/b45`; otherwise `merge --no-ff -m "Records: fold records/b45 (B45)"`; any conflict: `merge --abort`, **STOP: NEEDS FRIDAY**. Read back `git rev-parse main` and `ls-tree main -- 1_Project_Definition/Design/2026-10-12_home-dashboard/`.

## STATUS sections
BLUF · prior work as you found it · tokens (count resolved / NEW) · the five-metric table as rendered (marker per tile) · roles panels · Vision ideas used and the four improvements, each with where it shows · renders (path, width, height, sha256) · PDF (path, pages = 1, sha256) · checks (a)–(d) with ratios and controls · NEW words count · records (branch, commit, fold, `main` before/after) · UNMEASURED · NOT DONE · needs-Friday · processes started/stopped.

## UNMEASURED (by the draft writer)
- Whether headless Chrome renders in this seat's shell (the app bundle is present at `/Applications/Google Chrome.app`; not run).
- How many hosted quotes lack an owner, events or a calculation (affects real tile numbers later, not this mock).
- Whether "Superseded" history should count toward "provided" (a quote revising after approval shows Draft on the list).

## HOLDS
- Datasec only; no other client's names or files. **You read nothing outside this project**: every Vision fact you need is above.
- **No product code:** `2_Project_Files` read verbs only (no checkout, branch, commit, push, `npm install`). No deploy, no Azure, no setting change. **P-1 hosted hold unchanged** (records `BACKLOG.md` `## Holds on the hosted site`, `:16`); hosted stays `db8edfd` (C-21). **Q-09 unchanged: never activate or show a real price book**; every figure is SAMPLE.
- **Nothing to any human**; no Jira write this round. Push nothing (records repo has no remote).
- Own worktree `.tools/wt-B45-design` only. Never delete; quarantine to `.tools/_quarantine/2026-10-12_B45_<what>/`. Bind no port. Kill only what you started, by PID.
- The mock is a picture: no `<script>`, no form that posts, no link outside the file.

## End
The last line of `Briefs/2026-10-12_B45_STATUS.md` is exactly one of:
- `MOCKUP READY: <pdf path>` (records main @ `<sha>`);
- `STOPPED: NEEDS FRIDAY` and ONE question.
