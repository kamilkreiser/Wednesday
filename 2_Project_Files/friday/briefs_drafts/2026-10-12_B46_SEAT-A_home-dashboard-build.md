From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to friday-laptop-agent@agentmail.to. This project has no mail key, so your STATUS file is your wrap.
# BRIEF B46 · SEAT-A: build the Home screen Kam approved (the B45 mockup): figures on top, Needs follow-up, work queue; quote-list fields, a figures read, a Won/Lost outcome; filtered Quotes routes
**Written:** @NOW@ AEDT 2026-10-12. This is a draft. Friday sets the time when he fires it. **Pane:** `Datasec/MPS-A`. Your commission is the newest file in `Briefs/` whose name contains `_SEAT-A_`.
(Launcher check, from B45's brief header: `Launch_Claude.command:107` takes the seat letter from a pane name matching `*MPS*-?`; `:111` makes the commission "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". At drafting the newest `_SEAT-A_` file is `2026-10-12_B45_SEAT-A_home-dashboard-mockup.md` (`ls -t Briefs | grep -i _SEAT-A_`), finished: `B45_STATUS.md` last line `MOCKUP READY: … (records main @ 222c73eb…)`. This file replaces it.)
**Seat:** Seat A, a Claude build seat. One branch, red-first. **QA tier 1** throughout (new API fields, a write endpoint, a role-scope change).
**Round:** round 1 of a new lane (the two-NO-GO cap starts fresh).
**Report:** `1_Project_Definition/Briefs/2026-10-12_B46_STATUS.md`. Its **last line** is exactly one of:
- `READY FOR GATE: b46/home-dashboard <sha>`, where `<sha>` is the full 40-hex SHA read back by `git ls-remote origin refs/heads/b46/home-dashboard` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.

## AUTHORITY
- **Kam's ask, verbatim** (live board 2026-10-12 11:54:31, quoted in `Briefs/2026-10-12_B45_SEAT-A_home-dashboard-mockup.md`, `## AUTHORITY`): *"Please create a proper Home Screen for the MPS calculator. Make the dashboard a single view that provides a snapshot or key metrics - Quotes provided and an ability to click through, total value of quotes out, quotes past a certain time range requiring follow up, deals closed this month and Year to date. … let me know once you have a mockup and once its live"*
- **Kam's ruling on card `mpscalc-home-dashboard-mockup-1012`** (live board 2026-10-12 13:11:14): **a, "Approve the mockup with all the defaults"**. At 13:11:34: *"please deploy as soon as its ready"* (the deploy is a SEPARATE seat after gate + merge; not this brief).
- **The defaults Kam approved (verbatim from the card's BLUF), now RULINGS for this build:**
  - D-1 Quotes provided = Approved quotes.
  - D-2 Value = rental contract value plus purchase total, ex GST.
  - D-3 Follow-up after 14 days.
  - D-4 Year to date = financial year from 1 July.
  - D-5 Add a Won/Lost outcome that the quote's owner or an Approver records.
  - D-6 Administrators see the figures too.
  - D-7 Figures on top, work queue below.
- **The NEW WORDS are approved with the defaults** (Kam's a). Ship `NEW_WORDS.md` §A as written; every change is listed in `## NEW WORDS` below and in your STATUS.
- **Spec tension, settled by D-7:** spec FR-DB-001 (pricing work queue, not analytics-first) vs Kam's newer request (`B45 brief`, `## AUTHORITY`, third bullet). Figures on top, work queue below.

## THE SPEC IS THE RATIFIED MOCK: BOTH HALVES
A ratified mock has two halves: **what the page SAYS** (its words, figures and captions) and **what the page IS** (its layout, shape, order and behaviour). Both are the spec. The gate checks both, against the numbered properties below.
- Mock files (records `main` `222c73eb14bd1e8606501ef1ab0995de0603cd64`; folder `1_Project_Definition/Design/2026-10-12_home-dashboard/`): `home-mockup.html` (236 lines), `home-mockup.css` (162 lines), `tokens.md`, `NEW_WORDS.md`, `renders/` (6 PNGs), `checks/`, `pack.html`, the PDF.
- Renders (width × height, sha256 prefix, measured by the draft writer with `sips` / `shasum -a 256`): `home-seller-1440` 1440×1186 `cb419f07b7fe`; `home-seller-390` 390×3551 `a21159d48b9d`; `home-approver-1440` 1440×1225 `cf958ee726f0`; `home-approver-390` 390×3644 `90ad3431838b`; `home-admin-1440` 1440×399 `203d42b82fbc`; `home-admin-390` 390×491 `4927e998c449`.
- **NOT shipped (mock-only, `NEW_WORDS.md` §B):** the `MOCKUP B45 · View as:` bar; the yellow SAMPLE ribbon; every `SAMPLE` tag; every `needs:` marker (10 distinct); the footnote "Mockup, brief B45, 12 Oct 2026. Money: …"; every `Sample …` name and `Q-SAMPLE-10nn` ref. **The real fields below replace every `needs:` marker.** The mock-only tokens `--sample-bg`, `--sample-ink`, `--needs-line` (`tokens.md` §3) are therefore NOT added to `styles.css`.

## READ WHOLE FIRST (all inside this project; read nothing outside it)
- The project `CLAUDE.md`; records `main` `1_Project_Definition/CLARIFICATIONS.md` (C-04 AUD `:47`, C-12 ownership / no self-approval / GST `:168`).
- The whole mock folder above, and `Briefs/2026-10-12_B45_SEAT-A_home-dashboard-mockup.md` (its `## MPS DATA` and `## ROLES` sections are the data map) and `Briefs/2026-10-12_B45_STATUS.md`.
- On code base (`git show b28c95eb:<path>`): `web/src/screens/Dashboard.tsx` (121 lines), `web/src/components/Shell.tsx`, `web/src/app/router.ts` (44), `web/src/format/decimal.ts` (`formatMoney` `:43-46`), `web/src/styles.css` (`.cards` `:100-105`), `web/src/screens/QuoteScreen.tsx`, `web/src/screens/Lifecycle.tsx`, `web/src/api/client.ts` (`listQuotes` `:56`, `:129`), `web/src/api/stub/stubApi.ts` (`:86`), `web/playwright.config.ts`; `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` (`ListQuotes` `:549-567`, `Approve` `:340-372`, `CallerCan` `:876-886`, `QuoteReaders` `:24`), `QuoteStore.cs` (`VersionStatus` `:8-14`, `QuoteState`), `QuoteEvents.cs`, `QuoteFileStore.cs`, `Proposal.cs` (`:255-275`, `:340-450`), `Contracts/Dtos.cs` (`QuoteSummaryDto` `:368-369`, `CallerCanDto` `:372`, `ProposalDto` `:395-425`, `QuoteModeDto` `:471-475`, `QuoteEventDto` `:878-880`), `Infrastructure/ApiJson.cs` (decimals as exact strings `:8-9`, `:30-37`), `docs/API.md` (`## Rules the API enforces` `:40-52`), `docs/api/openapi.json` (`/api/v1/quotes` `:52`).
- `Briefs/2026-10-11_B35_SEAT-A_…md` + `B35_STATUS.md` (the lane-A1 event shape you copy for the outcome audit) and `2026-10-11_B37_STATUS.md` (K-1: events kept only when the save succeeds).

## PRIOR WORK (measured by the draft writer at `b28c95eb`; re-read each cite at your base and list any that moved)
- **Today's `#/` is the "Quotes" page, `Dashboard.tsx`.** Title "Quotes" (`:56`, `:71`); section `aria-label="Quotes"` (`:54`, `:69`). It is the B08 work queue (`:1`): ONE table, columns **Quote ref · Customer · Status · Version · Updated** (`:92-98`); quote ref links to the quote screen (`:105`), `(no ref)` when blank; status badge `badge-<status>` (`:109`); Updated = `toLocaleString('en-AU')` (`:112`). Buttons **Refresh** (`:73`) and, Seller only, **New quote** (`:74-78`), which opens `NewQuoteForm` (`:81`). "Loading…" (`:84`), "No quotes yet." (`:86`). **No tiles, no groups/tabs, no filters, no search, no values, no owner, no term, no device count.**
- An identity with neither Seller nor Approver (e.g. Administrator only) gets **no list call** and sees "Your roles do not include quotes." plus "Open the inventory" (`:10-12`, `:52-66`).
- Shell: brand links `#/` (`Shell.tsx:18`); nav = **Quotes** (`:22`, → `#/`) and, by role, **Inventory** (`:23`).
- Router: routes `dashboard`, `inventory`, `quote`, `proposal` (`router.ts:3-7`); **no query strings** (`parseRoute` `:9-17` matches whole paths; anything else falls back to `dashboard`).
- List API `GET /api/v1/quotes` (`QuoteEndpoints.cs:51`, `:549-567`): Seller or Approver (`QuoteReaders` `:24`); one row per quote from `q.Current`; ordered `updatedAt` desc then `quoteId`. Row `QuoteSummaryDto(QuoteId, QuoteRef, Customer, Status, VersionId, VersionNumber, UpdatedAt, CallerCan?, OwnerName?)` (`Dtos.cs:368-369`). **No value, no approved date, no owner id / mine flag, no outcome, no term, no device count.** No query parameters.
- No outcome state: B45 brief measured `won` 0, `Won/Lost` 0 (whole-word, `src web/src docs` at `b28c95eb`). `QuoteEvents.Kinds` has no outcome kind (`QuoteEvents.cs:27-28`).
- Built tile shape `.cards` uses `minmax(170px, 1fr)` (`styles.css:100`); **the mock uses `minmax(210px, 1fr)` (`home-mockup.css:93`): the mock wins.**
- `web/playwright.config.ts` sets `screenshot: 'off'` because suites run against the REAL local price store ("brief: confidentiality"). Your screenshots therefore come from a separate B46 spec in **stub mode / synthetic data only** (see Test Evidence).

## Base and branch
- **Base: MPS code main = `b28c95eb0f73ed0ce7ae410791feefc8b1a059ea`.** Read by the draft writer at 13:17 AEDT with `git -C 2_Project_Files ls-remote origin main` → `b28c95eb0f73ed0ce7ae410791feefc8b1a059ea refs/heads/main`. `log -1 --format='%H %T %P'` → tree `2826f02744a28e7ffd5689bd1885e2b03cad68b6`, parent `44374606f49bc5c5498ad7fbd19230de487d85c2` (PR #27, "Lane A2: source version lifecycle + admin API …"). Local `2_Project_Files` HEAD is `7f6ca4c` (not main): read by sha, never by working tree. `ls-remote origin 'refs/heads/b46*'` → 0 lines.
- **First action:** `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/main`.
  - prints `b28c95eb…` → proceed;
  - prints a descendant → `git diff --name-only b28c95eb <main>`; if it touches your write set, **STOP: NEEDS FRIDAY**; otherwise base on the new main and say so;
  - anything else → **STOP: NEEDS FRIDAY**. Never rebase on your own.
- Branch **`b46/home-dashboard`** in a fresh worktree `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B46'` (`chmod 700`); base measures in `.tools/wt-B46-base`, detached at base.
- **Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.** The Datasec org requires CodeQL (`.github/workflows/ci.yml:5`: CodeQL is the org default setup, not a CI job).

## Ports
- **6640–6649** (API 6640, web 6643 by default; Playwright and run-demo find them through env: `MPSCALC_WEB_PORT` `vite.config.ts:12`, `MPSCALC_API_ORIGIN` `:22`, `MPSCALC_E2E_BASE_URL` `playwright.config.ts:12`). Last held by B42 (`B42_SEAT-B…md:52-53`), whose seat is closed (`B42_STATUS.md` last line `READY FOR GATE: b42/gate-b41-fix-round ab8fdf1…`; merged in PR #27). **Friday reassigns 6640–6649 to B46**, overriding "never use a port named in an earlier brief" for this range only.
- Draft writer's check at 13:15 AEDT: `lsof -nP -iTCP:6640-6649 -sTCP:LISTEN` printed nothing (rc 1): **0 listeners**. Re-check before every bind; on any listener, **STOP: NEEDS FRIDAY** (do not move ranges).
- Every other port named in an earlier brief or STATUS stays off limits (e.g. 5080, 5173, 5183, 6650–6659, 6660–6699, 6750–6869, 6900–6919). Never edit a shared config default.

## Write set
- API: `src/MpsCalc.Api/Contracts/Dtos.cs`; `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`; `QuoteStore.cs` (the outcome on `QuoteState` only); `QuoteFileStore.cs` (persist the outcome; old files read as "no outcome"); `QuoteEvents.cs` (one new kind); a new `src/MpsCalc.Api/Quotes/QuoteFigures.cs` if you want the rules in one place; `docs/api/openapi.json`; `docs/API.md`; `tests/MpsCalc.Api.Tests/**` (new file `QuoteApiTests.Home.cs`).
- Web: `web/src/app/router.ts`; `web/src/components/Shell.tsx`; `web/src/screens/Dashboard.tsx` (becomes Home; rename allowed, say so); a new `web/src/screens/QuoteList.tsx`; `web/src/screens/QuoteScreen.tsx` / `Lifecycle.tsx` (the Record outcome action only); `web/src/api/client.ts`, `types.ts`, `stub/stubApi.ts` (+ synthetic stub rows); `web/src/styles.css`; `web/src/api/generated/**` (only via `sync-contract.mjs`); tests beside each; a new `web/e2e/b46-home.spec.ts`.
- **Frozen** (diff must be empty): `src/MpsCalc.Engine/**`, `src/MpsCalc.Import/**`, `src/MpsCalc.Api/Inventory/**`, `src/MpsCalc.Api/Sources/**`, `src/MpsCalc.Api/Quotes/PricingPolicy.cs`, `Proposal.cs`, `PriceAudit.cs`, `web/src/auth/pricePolicy.ts`, `web/src/proposal/**`, `web/playwright.config.ts`, `infra/**`, `scripts/**`, `.github/**`, root build files, `docs/{DEMO,ENGINE,IMPORTER}.md`.

## Tier 1 (all items)
- **No GP, margin, cost, CPP, capital or target-GP value** reaches the list, the figures read or the Home page, for any role (FR-DB-010; spec `…_TEXT.md:220`). The only money added is the customer-safe sell values the proposal already gives every quote role. Prove it with a planted-field control per DTO (a planted `cost`/`gp`/`margin` member must turn a test RED).
- **The approved snapshot never changes.** Recording an outcome writes the quote's own state and one event; it never writes a snapshot, a version, a revision or `updatedAt`. Prove snapshot bytes and approved `/proposal` bodies byte-equal before/after.
- **Role scope is enforced on the server**, never only hidden in the UI (403 tested per role).
- **Events kept only when the save succeeds** (B37 K-1 pattern: `QuoteEvents.UnlessSaved`, `QuoteEvents.cs` `UnlessSaved`).
- **C-12 stands:** approve/reject self-rules unchanged; `X-MpsCalc-Act-As` cannot get round any outcome rule (identity decides "owner").

## DATA MODEL vs MOCK (settled here; each line is the rule you build)
- **M-1 "Quotes provided" (D-1):** current version status `Approved` (`QuoteStore.cs:8-14`; list status is the current version's, `QuoteEndpoints.cs:559-561`). Superseded versions do not count. A quote that got a new Draft version after approval shows Draft and drops out (B45 STATUS UNMEASURED item 4; ship the literal rule; say the count it affects in your probe).
- **M-2 Value (D-2), `valueExTax`:** the quote's priced total ex GST from the snapshot / calculation for its current status: **rental → `PortfolioDto.ContractValueExTax`; purchase → `PurchaseResultDto.PurchaseTotalExTax`**. A quote is one mode (`QuoteModeDto` Rental | Purchase, `Dtos.cs:471-475`), so "rental contract value plus purchase total" is the sum over quotes. **TRAP: never add the proposal's `contractValueExTax` to its `purchaseTotalExTax`** — for a purchase quote the proposal sets `ContractValueExTax = p.PurchaseTotalExTax` (`Proposal.cs:436`), so that sum double-counts. Source per status: Approved → approved snapshot; Submitted → submitted snapshot; Draft → latest calculation only if it matches the current revision (the `/proposal` 409 rule); otherwise absent ("Not calculated").
- **M-3 `approvedAt`:** `CreatedAt` of the current version's approved snapshot (`Approve` sets it, `QuoteEndpoints.cs:361`; `v.ApprovedSnapshotId` `:368`). Present only when current status is Approved.
- **M-4 `isMine`:** `q.Owner == caller.User` (identity, not act-as; `QuoteStore.cs` `QuoteState.Owner`). `ownerName` is not unique, so never match on it. Pre-owner quotes (Owner null) are nobody's.
- **M-5 Outcome (D-5):** `outcome` = `won` | `lost` (absent = open), `outcomeAt`, `outcomeByName` (display name, never an e-mail or id, as `ownerName` `QuoteStore.cs` `OwnerName`), held on `QuoteState` (not on a version), persisted in the quote file. Recordable only when the current version is Approved and no outcome exists yet. **Changing or clearing an outcome is NOT in scope** (409; see Doubts).
- **M-6 Follow-up due (D-3):** current Approved, no outcome, `approvedAt` more than **14** days before now. One server constant (`FollowUpDays = 14`); not a setting.
- **M-7 Periods (D-4):** "This month" = `outcomeAt` in the current calendar month; "Year to date" = `outcomeAt` on or after **1 July** of the current Australian financial year (on 12 Oct 2026: since 1 July 2026). Day/month boundaries in **Australia/Sydney** (draft writer's default; see Doubts). Deals closed count **Won**; Lost is shown beside it (B45 STATUS, `## The five metrics`, last line).
- **M-8 Groups (FR-DB-003):** Drafts = current Draft without a rejection reason; Awaiting approval = current Submitted; Rejected = current Draft **with** `RejectionReason` (reject sets it, `QuoteEndpoints.cs:418`; the draft writer found no line that clears it: `git grep -n -i "RejectionReason ="` → `:418`, `:736`, `QuoteFileStore.cs:426` only — re-measure); Recently approved = current Approved with `approvedAt` within the last **14** days (draft writer's default; see Doubts).
- **M-9 Work-queue fields (FR-DB-004; the mock's `needs: on the quote list` on Term, Devices, Monthly value, `home-mockup.html:103`):** `termMonths` (`draft.Assumptions.TermMonths`), `deviceCount` (rental: sum of fleet quantities; purchase: the purchase result's `DeviceCount`, `Dtos.cs:420`), `monthlyValueExTax` (rental: `PortfolioDto.MonthlyCharge`; **purchase: absent**, cell shows "—"; same source rule as M-2).

## ITEMS (in this order; red test first for each; one commit per item; contract sync its own commit)
### 1. API: quote-list fields + filtered-list query params
- `QuoteSummaryDto` gains optional members: `valueExTax`, `monthlyValueExTax`, `termMonths`, `deviceCount`, `approvedAt`, `isMine`, `outcome`, `outcomeAt`, `outcomeByName`, `group` (`drafts` | `submitted` | `rejected` | `approved`), `followUpDue` (bool). `CallerCanDto` gains `recordOutcome` (M-5 + Item 3's rule). Decimals as exact strings (`ApiJson.cs:30-37`).
- `GET /api/v1/quotes` query params (all optional, AND-ed; unknown value → 400 with a fixed code): `scope=mine|all`, `status=draft|submitted|approved`, `outcome=open|won|lost`, `followup=due`, `period=month|ytd` (with `outcome`), `canApprove=true`, `group=drafts|submitted|rejected|approved`, `q=` (customer or quote ref, case-insensitive contains), `owner=` (display name, exact). No params = today's body plus the new members (backward-compatible; existing list tests stay green unmodified).
- Roles unchanged on the list: Seller or Approver; Administrator alone still 403 (`docs/API.md:41-42`).
- Update the `listQuotes` description in `openapi.json` and `docs/API.md`: it now carries the customer-safe sell totals above, still **no cost, GP or margin** (today's text: "Carries no price, cost, calculation or snapshot content for any role", B45 brief `## MPS DATA`). Old → new words in NEW WORDS.

### 2. API: the figures read (D-6)
- `GET /api/v1/quotes/figures?scope=mine|all` (new). Roles: **Seller, Approver or Administrator.** `scope=mine` needs Seller (else 400). Administrator-only and Approver callers always get all quotes. Body: one object per figure, each `{ count, valueExTax }` (+ `won`, `lost` on the two closed figures): `provided`, `outOpen` (Approved, no outcome), `followUpDue`, `closedMonth`, `closedYtd`, `awaitingApproval` (Seller: my Submitted) and `awaitingMyApproval` (Approver: rows with `callerCan.approve`), plus `asOf` (the "Updated" stamp), `followUpDays` (14), `periodStart` per closed figure.
- **Aggregates only: no row, no quote id, no customer, no owner** (an Administrator sees figures, not quotes). Planted-field control: a planted `quoteId`/`customer` member turns a test RED.
- Why this endpoint (draft writer): an Administrator-only caller cannot read the list (403, `docs/API.md:41-42`), so D-6 needs a read that carries figures only. Opening the list to Administrators would show them every quote row, wider than D-6.

### 3. API: record an outcome (D-5)
- `POST /api/v1/quotes/{quoteId}/outcome`, body `{ "outcome": "won" | "lost" }`. Allowed: the quote's **owner** (`q.Owner == caller.User`) **or any caller holding Approver**. Administrator-only, other Sellers, no role → 403 (fixed code, e.g. `OUTCOME_FORBIDDEN`). Pre-owner quote → Approver only. Not current Approved → 409 (e.g. `OUTCOME_NOT_APPROVED`); outcome exists → 409 (e.g. `OUTCOME_ALREADY_RECORDED`); unknown quote → 404; bad body → 400. Name your codes in NEW WORDS.
- **Audit as a server event, like lane A1:** one new `QuoteEvents` kind **`outcome-recorded`** (added to `Kinds` and the contract enum), recorded with `QuoteEvents.Record` (`at`, `By` = caller id, persona, current `versionNumber`) and the outcome word, inside `QuoteEvents.UnlessSaved` (B37 K-1). Returned with the other events (internal-metrics only, unchanged). A refused call records nothing; a call whose save fails records nothing (tamper-tested).
- Writes `QuoteState` outcome fields + the event and saves the quote. Never touches a version, snapshot, revision or `updatedAt` (Tier 1).

### 4. Web: Home page as drawn (properties H-1…H-38 below), Shell nav, router
- `#/` renders Home; `#/?scope=…&group=…` drive the scope switch and the queue tab. Nav **Home · Quotes · Inventory** (Inventory by role as today). Figures from Item 2; follow-up list and queue from Item 1.
- Keep today's behaviour that is not drawn away: Refresh reloads everything; New quote opens `NewQuoteForm` (Seller only).

### 5. Web: filtered Quotes list routes
- `#/quotes` (all the caller may see) and `#/quotes?<params>` with exactly the Item 1 params the tile hrefs use (H-13). The page is **not drawn in the mock**: build it from drawn parts only — heading "Quotes" (built word), the work-queue table (H-26…H-28 columns/actions), the search + Owner filter + Clear filters row (H-25), and under the heading the **approved tile label** of the filter that led there (e.g. "Needs follow-up"). No new words. A filter value the router does not know → the unfiltered list (never a blank page). `#/quotes/{id}` and `#/quotes/{id}/proposal` keep matching first.

### 6. Web: the Record outcome action
- On the follow-up row (H-21) and on the quote screen when `callerCan.recordOutcome`. Choose **Won** or **Lost** and confirm; on success the row leaves the follow-up list and the figures refresh. The control is **not drawn**: reuse the reject-reason pattern of `Lifecycle.tsx` and only approved/built words (Record outcome, Won, Lost, and a built Cancel if one exists — grep it). Show a recorded outcome on the quote screen as a badge Won/Lost with date (en-AU) and `outcomeByName`. Any word you cannot avoid adding → NEW WORDS as **UNDRAWN**, for Friday to show Kam before deploy.

## MEASURED LAYOUT PROPERTIES (the mock's "what the page IS"; each is a Playwright or unit assertion)
Sources: `home-mockup.html` (`html:`), `home-mockup.css` (`css:`), renders. Seller = `#seller` frame, Approver = `#approver`, Admin = `#admin`.
**Shell and head**
- H-1 Order top-down: classification banner → header (brand, nav, signed-in + Sign out) → main. No SAMPLE ribbon, no mock bar (`html:13-23`; mock-only `html:11`, `:22`).
- H-2 Nav, Seller/Approver: **Home · Quotes · Inventory**, Home `aria-current="page"` on `#/`, Quotes → `#/quotes` (`html:16`, `:118`). Admin-only: **Home · Inventory** (`html:217`). Active link: 2px bottom border `--brand-ink`, bold (`css:65-66`).
- H-3 Page head: h1 **Home**; under it the stamp "Updated h:mm am, d Mon yyyy" (`html:25`, e.g. "Updated 11:58 am, 12 Oct 2026"), from the figures' `asOf`. Right: **Refresh**, then **New quote** (primary) for Seller only (`html:26`; Approver `html:128` Refresh only). Head is flex, space-between, align flex-end (`css:73`).
- H-4 Scope switch, **Seller only**, below the head: segmented "**My quotes** | **All quotes**", default My quotes (`aria-current="true"`, accent fill), links `#/?scope=mine` / `#/?scope=all` (`html:28`; `css:86-90`). Approver: none (`html:126-130`).
**Tiles (figures on top)**
- H-5 Grid: `grid-template-columns: repeat(auto-fill, minmax(210px, 1fr))`, gap 10px, margin 12px 0 (`css:93`). **At 1440: 6 tiles in ONE row** (render `home-seller-1440`; arithmetic: main 1440 − 2×24 padding `css:71` = 1392; ⌊(1392+10)/220⌋ = 6).
- H-6 At 390 (≤600px): **1 column**, one tile per row (`css:147`, `:151`).
- H-7 Tile shape: surface background, 1px `--line` border, **4px left border** in the tone colour, radius 8px, padding 12px, vertical flex gap 4px (`css:94`). Tones: tiles 1–2 info (`--accent`), tile 3 warn (`--warn-line` = `#e0a400`, `styles.css:103`), tiles 4–5 good (`--ok-ink`), Approver tile 6 warn, Seller tile 6 info→ drawn only in error state (see H-16) — build Seller tile 6 as **info** (UNMEASURED in the mock; say so). Hover `--hover-bg` (`css:95-99`).
- H-8 Tile anatomy, top to bottom: label row (label link left) → period switch (tiles 4–5 only) → big number → value line → won·lost line (tiles 4–5 only) → one-line definition → "**View quotes →**" pinned to the bottom (`margin-top:auto`) (`html:31-38`; `css:100-107`). Tiles in one row share a height (grid stretch; render).
- H-9 **The whole tile is one link** (`.kpi-link::after { inset:0 }`); the period switch and Retry sit above it (z-index 1) and work on their own (`css:102`, `:108`).
- H-10 Big number 1.9rem bold tabular (`css:103`). **Tile 2 inverts:** the big number is the money (1.6rem, `css:111`) and the line under it is "**n quotes** · AUD ex GST" (`html:41-42`).
- H-11 Value line (tiles 1, 3, 4, 5, Approver 6): "**$x** AUD ex GST" — money via `formatMoney` (`decimal.ts:44`), "AUD ex GST" muted 0.8rem normal weight (`html:34`; `css:104-105`).
- H-12 Tile order: 1 **Quotes provided** · 2 **Total value of quotes out** · 3 **Needs follow-up** · 4 **Deals closed** (This month selected) · 5 **Deals closed** (Year to date selected) · 6 Seller **Awaiting approval** / Approver **Awaiting my approval** (`html:31-85`, `:131-184`).
- H-13 Tile hrefs (Seller in scope=mine; Approver and scope=all drop `scope=mine&`): 1 `#/quotes?scope=mine&status=approved` · 2 `…&status=approved&outcome=open` · 3 `#/quotes?scope=mine&followup=due` · 4 `…&outcome=won&period=month` · 5 `…&outcome=won&period=ytd` · 6 Seller `#/quotes?scope=mine&status=submitted` / Approver `#/quotes?status=submitted&canApprove=true` (`html:32,40,48,57,67,78,178`).
- H-14 Period switch on tiles 4 and 5: segmented "**This month** | **Year to date**", 0.75rem, aligned left; tile 4 has This month on, tile 5 has Year to date on; each link goes to its own filtered list (`html:58`, `:68`; `css:109-110`).
- H-15 Won·lost line: "**n won** · n lost", muted 0.8rem, "n won" in `--ok-ink` 600 (`html:61`; `css:114-115`).
- H-16 **Failing-tile state** (any one figure that fails): background `--bad-bg`, border `--error-line` (`#f2c3c5`, `styles.css:84`), left border `--bad-ink`; big number "**—**" with `aria-label="Not available"` in `--bad-ink`; then "**Could not load this figure.**" (`--bad-ink`, 0.85rem); "**The other figures are not affected.**"; a **Retry** button; then the tile's definition; then "View quotes →" (`html:77-85`; `css:99`, `:112-113`). The other tiles, the follow-up list and the queue still render.
**Needs follow-up list**
- H-17 Below the tiles: a panel (surface, 1px border, radius 8, padding 14px 16px, margin 12px 0, `css:118`). Head row: h2 "**Needs follow-up**" left; hint "**n quotes need follow-up**" right, `--warn-ink` 600 (`html:88`; `css:119-120`).
- H-18 Lead line, small muted: "**Approved more than 14 days ago, with no Won or Lost outcome. Oldest first.**" (`html:89`).
- H-19 Columns, in order: **Quote ref** (link to the quote) · **Customer** · **Owner** · **Approved** (dd/mm/yyyy) · **Days since approved** (right, `--warn-ink` bold, "n days") · **Value (AUD ex GST)** (right) · action (header screen-reader-only "Action") (`html:91-92`; `css:126`).
- H-20 Rows oldest `approvedAt` first (`html:89`; sample 45 → 27 → 18 days, `html:92`).
- H-21 Row action, primary button: Seller "**Record outcome**" (when `callerCan.recordOutcome`, else "Open"); Approver "**Open**" (`html:92`, `:191`).
- H-22 At most **5 rows**; when there are more, "**Show all n →**" links `#/quotes?followup=due` (Approver: 5 rows of 6, `html:191-192`). With 0 due quotes: UNDRAWN — keep the panel with the hint "0 quotes need follow-up" and no table (say so).
**Work queue**
- H-23 Below the follow-up panel: a panel, h2 "**Work queue**"; tabs **Drafts · Awaiting approval · Rejected · Recently approved**, each with a count pill (`html:97`; `css:135-137`). Selected tab: 3px `--accent` bottom border, `--hover-bg` background, accent bold text, `aria-current="true"` (`css:138`). Tab links `#/?scope=…&group=drafts|submitted|rejected|approved`.
- H-24 Default tab: Seller **Drafts** (`html:97`); Approver **Awaiting approval** (`html:196`). Seller+Approver: Awaiting approval (draft writer's default; see Doubts).
- H-25 Filter row: search input placeholder "**Search customer or quote ref**" (flex 1, min 200px, `css:140`); **Owner** select "**All owners**" + owner names (Approver `html:199`; Seller only in scope=all — UNDRAWN, say so); "**Clear filters**" button (`html:98-101`, `:197-201`).
- H-26 Columns, in order: **Customer** · **Quote ref** (link) · **Owner** · **Term** ("n months") · **Devices** (right) · **Monthly value (AUD ex GST)** (right; muted "**Not calculated**" when absent) · **Status** (badge) · **Last updated** (`toLocaleString('en-AU')`, e.g. "12/10/2026, 10:41:15 am") · action (sr-only "Action") (`html:103-104`). Note: Customer first here, Quote ref first in the follow-up list.
- H-27 Row action: Draft → "**Continue**"; Submitted (for an Approver who may approve) → "**Review**" (`html:104`, `:203`). Rejected / Recently approved rows: UNDRAWN — "Open" (approved word #34).
- H-28 Foot: muted "**Showing n of n <group>**" left (e.g. "Showing 4 of 4 drafts", "Showing 3 of 3 awaiting approval"); right link "**All my quotes →**" (`#/quotes?scope=mine`, Seller mine) or "**All quotes →**" (`#/quotes`) (`html:106`, `:205`; `css:141`).
**Phone (390)**
- H-29 No horizontal page scroll: `scrollWidth ≤ clientWidth` (mock measured 390/390 for all three panels, `checks/render_and_measure.out.json`; control fired at 616).
- H-30 Tables become cards: `thead` hidden; each row a bordered card (radius 8, padding 6px 10px, margin 8px 0); each cell a flex row, caption from `data-label` left (muted 0.8rem), value right; action cell right-aligned with no caption (`css:154-161`).
- H-31 Card captions = column names (follow-up: Quote ref, Customer, Owner, Approved, Days since approved, Value (AUD ex GST); queue: Customer, Quote ref, Owner, Term, Devices, **Monthly value** (short form, `html:104`), Status, Last updated) (`html:92`, `:104`).
- H-32 Main padding 12px 16px 24px; header side padding 16px; header-right drops its auto margin; page-head actions full width; search input full width (`css:148-153`).
**Roles**
- H-33 Seller: scope switch, New quote, figures default **My quotes**, tile 6 Awaiting approval, follow-up action Record outcome, queue opens on Drafts (B45 STATUS `## Roles panels`; `html:10-111`).
- H-34 Approver: no scope switch, all quotes, tile 6 **Awaiting my approval** ("Submitted quotes you may approve (not your own)."), follow-up action Open, queue opens on Awaiting approval with Owner filter (`html:112-210`).
- H-35 **Administrator only — CHANGED from the mock by D-6.** The mock drew "Your roles do not include quotes." + "Open the inventory" (`html:225-230`). Build: nav Home · Inventory; h1 Home + stamp; Refresh; **tiles 1–5 for all quotes** (tile 6 has no meaning without a quote role: omitted); tiles are **not links** and carry no "View quotes →" (the admin cannot open quotes); **no follow-up list, no work queue**. Words: none new (see NEW WORDS).
**Look**
- H-36 Colours: only tokens already in `styles.css` (`tokens.md` §1) and the 5 raw values it already holds (`tokens.md` §2: `#e8eef7` `:77`, `#e0a400` `:103`, `#fafbfc` `:72`, `#f2c3c5` `:84`, `#f0f5fc` `:123`). **0 new hex values** (check with a copy of `checks/checks_acd.py` (a) over your `styles.css` diff, planted control). Light theme only.
- H-37 Font as built: `system-ui…`, 14px base; tabular figures on numbers (`tokens.md` §4).
- H-38 Money AUD ex GST via `formatMoney` everywhere on the page; no `Intl` currency formatting; no GP/margin/cost anywhere (`home-mockup.html:108-109` states it; FR-DB-010).

## FIGURES AND CAPTIONS (the mock's "what the page SAYS"; ship exactly; `{}` = live value)
- Tile 1: label **Quotes provided** · big `{count}` · `{$value} AUD ex GST` · def "**Quotes whose current version is Approved (final proposal).**" (`html:32-35`)
- Tile 2: **Total value of quotes out** · big `{$value}` · "`{n}` quotes · AUD ex GST" · def "**Approved, no Won or Lost outcome yet. Rental contract value plus purchase total.**" (`html:40-43`)
- Tile 3: **Needs follow-up** · `{count}` · `{$value} AUD ex GST` · def "**Approved more than 14 days ago, no outcome yet.**" (`html:48-51`)
- Tile 4: **Deals closed** · [This month | Year to date] · `{won count}` · `{$won value} AUD ex GST` · "`{n}` won · `{n}` lost" · def "**Quotes marked Won in `{Month yyyy}`.**" (e.g. "October 2026", `html:57-62`)
- Tile 5: **Deals closed** · [This month | Year to date] · `{won count}` · `{$won value} AUD ex GST` · "`{n}` won · `{n}` lost" · def **CHANGED** → "**Quotes marked Won since 1 July `{yyyy}`.**" (`html:72` drew the calendar/FY alternative; D-4 picks FY)
- Tile 6 Seller: **Awaiting approval** · `{count}` · `{$value} AUD ex GST` (drawn only in error state; value line as tile 1) · def "**My quotes submitted and waiting for an Approver.**" (`html:78-83`)
- Tile 6 Approver: **Awaiting my approval** · `{count}` · `{$value} AUD ex GST` · def "**Submitted quotes you may approve (not your own).**" (`html:178-181`)
- Every tile foot: **View quotes →** (not on Administrator tiles, H-35). Error state: **—** · **Could not load this figure.** · **The other figures are not affected.** · **Retry**.
- Head: **Home** · **Updated `{h:mm am, d Mon yyyy}`** · **Refresh** · **New quote** · **My quotes** · **All quotes**.
- Follow-up: **Needs follow-up** · **`{n}` quotes need follow-up** · lead (H-18) · columns (H-19) · **`{n}` days** · **Record outcome** / **Open** · **Show all `{n}` →**.
- Queue: **Work queue** · tabs (H-23) with counts · **Search customer or quote ref** · **All owners** · **Clear filters** · columns (H-26) · **`{n}` months** · **Not calculated** · **Continue** / **Review** · **Showing `{n}` of `{n}` `{group}`** · **All my quotes →** / **All quotes →**.
- Status badges as built: Draft · Submitted · Approved (`css:127-130` = `styles.css:76-79`).

## Test Evidence (run each command as `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head** (in `wt-B46-base` and `wt-B46`): .NET full suite Release `--no-incremental`, **0 warnings**, `dotnet list package --vulnerable --include-transitive` 0; web `npm ci`, `lint`, `typecheck`, full `test`, `build`. Reconcile every count change by test name.
- **Contract:** `sync-contract.mjs` once per contract commit; `web/src/api/contract.test.ts` green; the `generated/**` diff is exactly the new paths, fields, enum value and schemas plus the SOURCE header.
- **Red-first, per item:** each new test fails at base (or on the item's parent commit) and passes at head; report `RED n/m → GREEN`.
- **Red-proof table, one line per conjunct (tamper → RED on the full suite → sha256 restore).** At least: (1) value double-counts a purchase quote (M-2 trap); `isMine` matched by `ownerName`; a cost/GP/margin member planted on `QuoteSummaryDto`; a filter param ignored; (2) an Administrator figure body carries a quote id or customer; scope=mine accepted without Seller; YTD starts 1 January; follow-up uses 13 or 15 days; (3) a non-owner Seller records an outcome; an Administrator-only caller records one; act-as gets round the owner rule; an outcome on a non-Approved quote; a second outcome; the event is missing; the event survives a failed save; the snapshot or `updatedAt` moves; (4–6) H-5 grid not 6 columns at 1440; H-6 not 1 at 390; tile order swapped; a tile href wrong; one figure failing blanks the page; follow-up shows 6 rows; queue column order changed; page scrolls sideways at 390; a `needs:` or `SAMPLE` string ships.
- **Playwright** (`web/e2e/b46-home.spec.ts`, **stub mode, synthetic stub data only**; never the real price store): at **1440×900 and 390×844**, for Seller, Approver and Administrator-only: assert **every H-property** that is measurable in the DOM (computed `grid-template-columns` track count, tile order by label text, hrefs, tab order + default, column headers in order, ≤5 follow-up rows + "Show all", `thead` hidden and `data-label` captions at 390, `scrollWidth ≤ clientWidth`, failing-tile state with the others rendered, Admin H-35), plus every caption in FIGURES AND CAPTIONS. Report `n/N properties asserted` and list any H-number you could not assert and why.
- **Screenshots of the built page beside the mock's renders:** from that spec only (explicit `page.screenshot`, not the shared config), synthetic data, the same six views as `renders/` (seller/approver/admin × 1440/390), full page, into `Briefs/2026-10-12_B46_evidence/` as `2026-10-12_b46-home-<role>-<width>.png`, plus one side-by-side sheet per view (mock render left, built right). State width × height and sha256 for each.
- **NEW WORDS diff:** run a copy of `checks/new_words.py` over the built page's visible strings vs `NEW_WORDS.md` §A + §C. Expected: **only the listed changes below**; anything else is a finding. Planted control: one undeclared string must be flagged.
- **Live probe** (DevStub, your ports, synthetic quotes created through the API): create → calculate → submit → approve (rental and purchase) → figures and list read → record outcome (owner; Approver; refused for other Seller and Administrator) → figures read. Report every figure against a hand count.
- **Leak + secret scan** over `git diff <base>...HEAD` and `git log --format=%B <base>..HEAD` with copies of B36/B38 tools (counts only, planted control per class). **No frozen change:** `git diff --numstat <base> -- <frozen list above>` empty.
- Evidence → `Briefs/2026-10-12_B46_evidence/` (0700 folder, 0600 files); tools/logs → `.tools/qa-B46/` (0700).

## NEW WORDS (verbatim; Friday shows Kam before any deploy)
Approved with D-1…D-7: `NEW_WORDS.md` §A, all 46 rows. **Changes the draft writer measured (each needs no further ruling unless marked):**
- §A #19 "Quotes marked Won since 1 January 2026 (or 1 July 2026, if financial year)." → "**Quotes marked Won since 1 July 2026.**" (year live) — follows D-4.
- §A #6, #10, #12, #13: unchanged (D-1, D-2, D-3 match the drawn defaults).
- Administrator view: "Your roles do not include quotes." / "Open the inventory" (built words, `Dashboard.tsx:58`, `:61`) **no longer shown to an Administrator-only identity** (D-6); still shown to an identity with no API role, if one can reach the page (measure).
- Removed (mock-only, §B): mock bar, SAMPLE ribbon/tags, all `needs:` markers, B45 footnote.
- API words (problem codes, `outcome-recorded`, enum values, OpenAPI summaries/descriptions, every `docs/API.md` line added/removed, the changed `listQuotes` description): listed old → new with `file:line`.
- Any word the undrawn parts force (Item 5 list page, Item 6 outcome control, H-22 empty state): listed as **UNDRAWN**. Target: 0.
Run copies of B36's `words36cs.py` / `newwords36.py` over `<base>...<head>`: every extracted string appears in your table (count = count), planted undeclared string flagged.

## DOUBTS (the draft writer's; build the stated default, and list each in STATUS needs-Friday)
- **Q-1 Recently approved window:** not in Kam's defaults or the mock. Default **14 days** (M-8).
- **Q-2 Changing an outcome** recorded in error: not ruled. Default: not possible (409); a later round adds it if Kam wants.
- **Q-3 Time zone** for month/FY/days: not ruled. Default **Australia/Sydney**.
- **Q-4 Purchase quotes** in the work queue: no monthly value (shows "—"); term shown as stored. Mock draws rental-like rows only.
- **Q-5 Seller+Approver** (Pricing analyst persona, `devPersonas.ts:10-30`): not drawn. Default: scope switch + New quote (Seller) AND tile 6 = Awaiting my approval, queue opens on Awaiting approval.
- **Q-6 Admin view (H-35)** is built from D-6, not drawn; tiles non-clickable is the draft writer's reading.
- **Q-7 A new version after Approved/Won:** the quote drops out of "provided" (M-1) while keeping its outcome (M-5). Measure how many synthetic/hosted cases this affects; do not change the rule.

## FOUND / TESTED / HOW / NOT TESTED
For each item, a four-line block in STATUS (FOUND citing `file:line` at base; TESTED with red-first counts; HOW with ratios; NOT TESTED and why).

## STATUS sections
BLUF (one-line verdict per item) · **PRIOR WORK** (every cite above re-read at base; which moved; today's `#/` "Quotes" page and what it shows, before you replaced it) · Base read · Commits · Test Evidence · Red-proof table · Tier-1 conditions · FOUND/TESTED/HOW/NOT TESTED per item · **H-property table (H-1…H-38: asserted / not asserted, test name)** · Figures and captions check · Screenshots (paths, sizes, sha256, side-by-side sheets) · NEW WORDS (verbatim) + the diff result · Modified pre-existing tests (before → after, why) · UNMEASURED · `## NOT DONE / NOT COVERED` · RECORDS · needs-Friday (Q-1…Q-7 + Jira draft lines; Jira writes are Friday's) · Leak + secret scan · processes started/stopped · worktrees and files left.

## RECORDS (local `records/b46` branch, commit only)
Records repo = the project root (no remote). `main` = `222c73eb14bd1e8606501ef1ab0995de0603cd64` (`git rev-parse main`, 13:1x AEDT; tracked status 0 lines). `git -C '<project root>' worktree add .tools/wt-B46-records -b records/b46 main` (`chmod 700`). Add `BACKLOG.md` `## Deferred problems` rows (existing shape) for: change-an-outcome (Q-2), FR-DB-003 "Ready to Export" tab (B45 NOT DONE), FR-DB-008 Duplicate on the queue, and any NOT DONE item. One commit `Records: home dashboard remainders (B46)`. **Never fold into `main`** (Friday's).

## Time-box
**About 4 h.** If short, finish in this order: 1, 3, 2, 4, 6, 5. List the rest as NOT DONE, never half-merged.

## UNMEASURED (by the draft writer, each with its closing instrument)
- Suite counts at `b28c95eb`. Closes with: your base run.
- Whether any path clears `RejectionReason` or copies it into a new version (M-8). Closes with: your read of `QuoteEndpoints.cs` `NewVersion` / `Duplicate` at base.
- Whether a "Cancel" word is built (Item 6). Closes with: `git grep -i -w -c Cancel <base> -- 'web/src/*.tsx'`.
- Real figures on the hosted site (pre-owner quotes, quotes without a calculation). Not this round (no hosted read).
- CodeQL and CI results: Friday reads them on the PR.
- Ports 6640–6649 at firing: free at 13:15. Re-check before you bind.

## HOLDS
- Datasec only. No other client's names, tickets or paths. Vision Sales Portal: nothing read, nothing copied (the mock already took layout ideas only).
- **CodeQL policy:** push your branch only; never push to main; never dismiss an alert; never ask for a bypass. **Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.**
- **No deploy in this brief.** No Azure write, no setting change, nothing sent to any human, no Jira write. After the gate and merge, a **separate deploy seat** runs, with the **P-1 hosted count first** (records `BACKLOG.md` `## Holds on the hosted site`, the B39 HOLD: *"count the hosted quote files whose fleet (any version) repeats a `lineNumber`"*; count UNKNOWN today). Hosted runs `db8edfd` (C-21).
- **SITE HOLD** (BACKLOG `## Holds on the hosted site`, first bullet): none of the four store path settings changes.
- **Q-09:** never activate or show a real price book; every fixture, probe and screenshot is synthetic.
- No pricing rule change: no price, total or applied percent moves on any fixture (full engine + API suites prove it).
- **No real client data anywhere** (code, tests, fixtures, screenshots, commit messages, STATUS). Counts only.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-12_B46_<what>/` (0700). Never edit a running script.
- **Own worktree and own ports.** Allowed: `fetch`, `worktree add`, commits and pushes on your own branch; records commits on `records/b46` only. Never `checkout`/`switch` in `2_Project_Files` or the project root. Never `gc`, `prune`, `reset`, `worktree remove`, `branch -D` or force-push. Other seats' worktrees and `qa-B4?/` are read-only (copy from them).
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate`, the shared `VBCSCompiler` and any listener outside 6640–6649 are not yours.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`; `UseSharedCompilation=false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero needs a positive control that fired.

## End
The last line of `Briefs/2026-10-12_B46_STATUS.md` is exactly one of:
- `READY FOR GATE: b46/home-dashboard <sha>` — with the six screenshots + side-by-side sheets in `Briefs/2026-10-12_B46_evidence/` and the NEW WORDS diff result (expected: only the listed changes) stated in STATUS;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.
