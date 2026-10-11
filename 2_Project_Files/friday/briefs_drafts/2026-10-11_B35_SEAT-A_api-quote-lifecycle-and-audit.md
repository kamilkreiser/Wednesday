From Friday (laptop seat), Datasec / MPS Commercial Calculator
# BRIEF B35 · SEAT-A — lane A1, API quote lifecycle and audit: duplicate (46), lifecycle audit events (55), rental override audit (33, API half), export field registry (47), export history (49, API half)
**Written:** ~16:5x AEDT 2026-10-11 (draft; Friday times it at firing). **Pane:** `Datasec/MPS-A`. Your commission is the newest file in `Briefs/` containing `_SEAT-A_`.
(Launcher check, read by the draft writer: `Launch_Claude.command:107` takes the seat letter from a pane name matching `*MPS*-?`, and `:111` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". The newest `_SEAT-A_` file at drafting is `2026-10-10_B25_SEAT-A_overlay-gate-findings.md` and its ADDENDUM-1; this file supersedes them. No MPS pane is live (`tmux list-panes -a`: 0 MPS names).)
**Seat:** Seat A (Claude build seat), one branch, red-first. **Lane A1, tier 1** throughout.
**Report:** `1_Project_Definition/Briefs/2026-10-11_B35_STATUS.md`. No mail key in this project, so your STATUS file is the wrap.
Its last line is exactly one of:
- `READY FOR GATE — <branch> @ <sha>`, with the head SHA read back by `git ls-remote` in the same action as the push;
- `STOPPED: NEEDS FRIDAY` and one question.

## AUTHORITY
- **Friday commissions lane A1** from the board reconcile of 2026-10-11 (Friday's drafts, `2026-10-11_mpscalc_board_reconcile.md`). The rows you need are quoted below. These are spec tasks already on the board (OPEN-A: agent-buildable, no Kam ruling needed for the slice below).
- **Q-16 (MPSCALC-82) is OPEN:** *"Retention and audit periods. How long are quotes, source versions, exports and audit events kept?"* (`00_QUESTIONS_FOR_KAM.md:27` on `records/b30`). **Do not decide it.** Record the default below and build nothing that deletes or expires.
- C-12 (no self-approval, owner-only edits) and the I-2 price-edit matrix (C-13, card `mpscalc-price-edit-permissions-1010` = a) stand unchanged.

## READ WHOLE FIRST
- The project `CLAUDE.md`, `1_Project_Definition/CLARIFICATIONS.md` (read it on `records/b30`: `git show records/b30:1_Project_Definition/CLARIFICATIONS.md`; the root copy ends at C-11), and `Questions_and_Answers/00_QUESTIONS_FOR_KAM.md`.
- `Briefs/2026-10-11_B30_SEAT-B_…md` and `2026-10-11_B30_STATUS.md` (the newest tier-1 shape, red-proof harness, contract sync rule, allow-list guard).
- `Briefs/2026-10-10_B17_*` ADDENDUM-2 (how the purchase price audit was built: `PriceAudit`, `PRICE_REASON_REQUIRED`).

## Base and branch
- **Base: origin main, measured by you.** Friday's read at ~16:4x AEDT: `friday_as.sh datasec gh api repos/datasecau/MPS-Commercial-Calculator/commits/main` → `db8edfd5082e49f9a1a1b3c23feeb02b36834b21`, tree `8a74f1c9d12f8499b77b24d33a7ef706756af6da`, "B30: accessory fit, markup before calculating, New quote form (Kam's rulings 2026-10-11) (#24)". `git ls-remote origin refs/heads/main` agreed; local `origin/main` = `db8edfd` (`rev-parse`).
- **First action:** `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/main`.
  - `db8edfd…`: proceed.
  - A descendant of `db8edfd`: list `git diff --name-only db8edfd <main>`. If it touches any path in your write set, **STOP: NEEDS FRIDAY**. Otherwise base on it and say so.
  - Anything else: **STOP: NEEDS FRIDAY**. Never rebase on your own.
- Branch `b35/api-quote-lifecycle-audit`, in a fresh worktree `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B35'` (`chmod 700`); base measures in `.tools/wt-B35-base` (detached at your base).
- Every `file:line` below was read by the draft writer at `db8edfd` with `git show db8edfd:<path>` / `git grep … db8edfd` (`--no-optional-locks`). Re-check each at your base before you edit, and list any that moved.
- **Push the branch only.** Friday opens the PR. He merges after CodeQL, the checks and a QA gate.

## Ports
**6620–6629** (API 6620, web 6623 by default). Friday checked at ~16:4x: `lsof -nP -iTCP -sTCP:LISTEN` shows 5000, 7000, 7768, 42050 and ports at 49152 or above only (0 listeners in 6600–6799); `grep -rhoE '\b6[5-7][0-9]{2}\b' Briefs/` names 6581, 6590, 6593, 6599 and 6600–6609 only (0 in 6610–6799). B34 (Seat R) holds 6640–6649 and binds nothing. Check that yours are free before you bind. Never use 5080/5173 or any port named in an earlier brief or STATUS. Playwright and run-demo find your ports through env. Never edit a shared config default.

## Lanes and write set (per the reconcile)
The reconcile, verbatim: *"The contract (`docs/api/openapi.json`, `docs/API.md`, `web/src/api/generated/**`) and `src/MpsCalc.Api/Program.cs` are shared by every API change. So **only one API-plus-contract lane runs at a time**. A1 runs first and A2 rebases on it."*

**Your write set:**
- `src/MpsCalc.Api/Quotes/{QuoteEndpoints,QuoteStore,QuoteFileStore,PriceAudit,Proposal}.cs`;
- new files under `src/MpsCalc.Api/Quotes/` (for example an audit-event or export-registry type);
- `docs/API.md`, `docs/api/openapi.json`;
- `web/src/api/generated/**`, regenerated **only** by `web/scripts/sync-contract.mjs`, never by hand;
- new and existing test files under `tests/MpsCalc.Api.Tests/` (modified pre-existing tests are listed in STATUS, before → after, why).

**Not in the reconcile's write set, so Friday rules at firing (until then a need for either is `STOP: NEEDS FRIDAY`):**
- `src/MpsCalc.Api/Contracts/Dtos.cs`: **UNFROZEN by Friday at firing** (A1 is the only API-plus-contract lane running; the new DTO fields live here).
- `src/MpsCalc.Api/Program.cs` (101 lines at `db8edfd`; shared): **UNFROZEN by Friday at firing** for endpoint registration only; keep the diff minimal and name every line.

**Frozen:** `src/MpsCalc.Engine/**`, `src/MpsCalc.Import/**`, `src/MpsCalc.Api/Inventory/**` (lane A3 may run beside you only if A1 leaves it alone), `src/MpsCalc.Api/Sources/**` (lane A2), `web/src/**` except `generated/**`, `infra/**`, `scripts/**`, `.github/**`, the root build files.
- If origin carries another seat's open branch, newer than your base, that touches your write set: **STOP: NEEDS FRIDAY**.

## Tier 1 (all items)
- red proof one conjunct at a time;
- the I-2 matrix is byte-for-byte unchanged and proved so (`git diff <base> -- web/src/auth/pricePolicy.ts src/MpsCalc.Api/Quotes/PricingPolicy.cs` empty; `RoleMatrixTests`, `PricingPolicyTests` green);
- no internal value is ever derived in the browser;
- **no price, total or applied percent changes on any existing fixture**, and **the proposal output is byte-for-byte unchanged** on every existing proposal test fixture (prove it: serialise before/after);
- every new DTO property is classified in `ProposalAllowList.Sources` (the `QuoteApiTests.Showcase.cs` guard must see it, as B30 did for `LineMarkupDto`);
- nothing new prints on the proposal; a Seller without internal metrics sees no new internal field.

## PRIOR-WORK CHECK
Before you replace or reword anything, record what existed and why. At least:
- **Routes** (`QuoteEndpoints.cs:41-55`): create, get, patch draft, calculate, submit, approve, reject, `new-version`, snapshots, admin sources, list, proposal, catalogue ×3. **There is no duplicate route** (the reconcile's row 46). `NewVersion` is at `:413`; the older approved version becomes `Superseded` at `:355` (FR-REV-013). Jira comment 38784 (B03): *"Duplication is not built."*
- **Purchase price audit** (`PriceAudit.cs`, 88 lines, B17 ADDENDUM-2): `Diff` covers sections (markup, rebate), manual items, BOM lines (pricing method, sell override, manual lines) and click rates (mono, colour, ink, supplies). The reason is required at `QuoteEndpoints.cs:157-167` (`PRICE_REASON_REQUIRED`), bounded by `PriceAudit.MaxReason` (500). It is frozen into each snapshot (`:297`) and shown only with internal metrics (`:657`).
- **Rental fleet overrides are not audited:** `FleetLineDto` (`Dtos.cs:37`) carries `TierOverride`, `BaseChargeOverride`, `MonoClickOverride`, `ColourClickOverride` (`:45-48`); `PriceAudit.Diff` reads none of them. Range checks are at `QuoteEndpoints.cs:910-912`. The reconcile, row 33: *"Rental fleet overrides have permission only, with no reason or audit."* Row 20 adds: *"a rental tier override has no reason or audit: PriceAudit covers purchase only (`QuoteEndpoints.cs:157`)"*.
- **The web sends a reason only when given one:** `web/src/api/client.ts:132` sends `reason` only if non-empty (`:59` comment: "required by the server when a purchase edit changes an audited price field"). Measure whether any rental screen can supply one (`git grep -n -i reason <base> -- web/src/screens/FleetGrid.tsx`) before you make it required (see item 3).
- **Allow-list** (`Proposal.cs:23` `ProposalAllowList`; `SourceTypes` `:33`; `Sources` `:45`): classifies every field of the types the projection reads (Proposal / Internal / NotShown). Jira comment 39263 (B09): *"Left: the general field registry for all exports (customer BOM export, internal workbook export, templates), the admin-maintained registry, and per-field labels."*
- **Proposal** (`GetProposal`, `QuoteEndpoints.cs:505`): records nothing when it is generated (no export history). DRAFT watermark and footer are web-side (B16; Jira comment 39310).
- **Inventory audit** exists in `Inventory/InventoryEndpoints.cs` (19 `audit` hits at `db8edfd`). It is frozen for you: do not merge it into the new events.

## ITEMS (in this order; red test first for each; one commit per item, contract sync as its own commit as in B30)

### 1. MPSCALC-46: duplicate a quote (NARROWING)
**Ticket** (read by the draft writer, Jira `GET`): *"A material post-approval edit creates a linked new Draft that needs reapproval; duplicates never copy approval state; superseded versions stay retained and marked."* Spec FR-REV-012, 013, FR-DB-008.
**Reconcile row:** OPEN-A, *"new-version and Superseded shipped (#5). There is no duplicate route."*
**This round closes (NARROWING):** the duplicate half only. New-version and supersession already shipped; "old approved version stays exportable until replacement approval" (FR-EXP-012) is not re-proved here.
- `POST /api/v1/quotes/{quoteId}/duplicate` creates a **new quote** (new id, version 1, `Draft`, fresh revision) from the source quote's current version's **draft**.
- It **never copies**: status, approval or rejection state, approver, snapshots, `RejectionReason`, or the source's price audit. The copy's audit starts with its own created entries, as `Create` does (`QuoteEndpoints.cs:82-86`).
- Owner: the caller. Who may: the same roles as `Create` (`Roles.Seller`) **and** the caller may read the source. Internal inputs follow the I-2 rule exactly as `Create`'s `InternalInputs` check: a caller without internal metrics duplicating a quote with internal inputs gets the same refusal `Create` gives. (Default by the draft writer; say in STATUS if the code points another way.)
- It records a lifecycle event on both quotes (item 2): `duplicated-to` and `duplicated-from`, with the other quote's id.

### 2. MPSCALC-55: lifecycle audit events (NARROWING)
**Ticket:** *"Record quote lifecycle, commercial, configuration and source-governance events with actor, role, time, version, before/after or reason and calculation/source refs."* Spec §23.2, FR-REV-007, NFR-DATA-002.
**Reconcile row:** OPEN-A, *"Price and inventory audit shipped (#15). No lifecycle or source-governance events (FR-REV-007)."*
**This round closes (NARROWING):** **quote lifecycle events only.** Source-governance events are lane A2's (`Sources/**`, frozen). Inventory events stay where they are.
- One append-only, server-written list per quote. Events at least: created, draft updated, calculated, submitted, approved, rejected, new version, duplicated (from/to), proposal generated (item 5).
- Each event: kind, UTC time, actor (caller id and effective persona, as `PriceAudit` entries record them), the caller's role(s), version number, and where they exist: reason, calculation id, snapshot id, revision.
- The client can never write it (a PATCH carrying it is refused or ignored, like `PriceAudit`; pin which). It survives a restart (`QuoteFileStore`; prove it as `QuotePersistenceTests` does).
- **Visibility (default by the draft writer, for Friday's gate):** classified **Internal** (`I`): returned only to a caller with internal metrics, never on the proposal, never to a Seller-only caller.
- **Retention, Q-16 default (record it; do not decide it):** *events are kept for the life of the quote file; nothing is pruned, expired or deleted.* Write that sentence in `API.md` beside the field, marked "default pending Q-16 (MPSCALC-82)". Build no deletion, TTL or cap.

### 3. MPSCALC-33, API half: rental override reason and audit (NARROWING)
**Ticket:** *"Allow authorised positive overrides of tier, base and mono/colour click rates, each with reason and audit event; mono and colour stay separate fields."* FR-FLT-008..010, SEC-RBAC-003; register R-13..R-15.
**Reconcile row:** OPEN-A, *"Purchase reason and audit shipped (B17 A-2, #15). Rental fleet overrides have permission only, with no reason or audit."* Lane B2 carries the UI half.
**This round closes (NARROWING):** the server audit of the four rental override fields. The UI half and the permission model are not touched.
- `PriceAudit.Diff` (or a sibling) adds one entry per changed `tierOverride`, `baseChargeOverride`, `monoClickOverride`, `colourClickOverride`, per fleet line, with who, when, field, old → new, reason. Mono and colour stay separate entries.
- **Required reason, gated by a measure:** if the rental web flow can send a reason today (PRIOR-WORK), require it (`PRICE_REASON_REQUIRED`, as purchase). **If it cannot, do not require it this round:** record the entry with no reason, and list "rental reason required" as **NOT DONE**, for B2's UI half. Any existing web or e2e test going red because of this item is a tier-1 failure.
- No rental price, total or tier moves on any fixture (the engine is frozen; prove the rental suites green and unchanged).

### 4. MPSCALC-47: server-owned field registry for exports (NARROWING)
**Ticket:** *"Classify every exportable field CUSTOMER_SAFE / INTERNAL_ONLY / ADMIN_ONLY and bind templates only through the registry; customer outputs may bind only customer-safe fields."* §27.1, App C, FR-EXP-006, 007.
**Reconcile row:** OPEN-A, *"`ProposalAllowList` shipped (#6, #15). Left: a general registry for every export."*
**This round closes (NARROWING):** one server-owned registry that classifies every field of every type an export reads, into the ticket's three classes, and that the proposal binds through. The admin-maintained registry, templates and per-field labels are not built.
- The existing `Proposal / Internal / NotShown` classes map onto the three classes; say how (`NotShown` is the one to argue). Keep `ProposalAllowList`'s guarantees: the two existing classification tests still fail on an unclassified or unlisted field.
- A test that binding an INTERNAL_ONLY or ADMIN_ONLY field to a customer output fails (the ticket's *"attempts to map internal fields to customer templates fail"*).
- The proposal output is byte-for-byte unchanged (Tier 1).

### 5. MPSCALC-49, API half: export history (NARROWING)
**Ticket:** *"Role-restricted internal outputs; each export card states included/excluded field classes; authorised draft export is watermarked and audited; every generation records time, version and user."* FR-EXP-003..005, 008, 011; draft wording subject to Q-15.
**Reconcile row:** OPEN-A, *"DRAFT watermark shipped (#18, #20). No handover output, internal snapshot export or export history."*
**This round closes (NARROWING):** "every generation records time, version and user" for the one export that exists (the proposal). Handover, the commercial snapshot export and export cards are lane C (web) and later.
- Every successful `GET …/proposal` appends a `proposal-generated` event (item 2) with time, version, user, and whether the version was a draft or approved. A refused call records nothing.
- State in STATUS that this makes a GET write, and how it behaves under concurrent generations (no lost event, no revision bump that would make a seller's open draft go STALE_REVISION). Prove the latter.
- Retention as item 2 (Q-16 default).

## Test Evidence (each run with `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head:** re-measure the base in `wt-B35-base`. B30 reported web 325/325 and .NET 885/885 at its round-1 head `cad7abd`, not at `db8edfd`: do not trust those numbers.
  - web: `npm ci`, `lint`, `typecheck`, the full `test` suite, `build`;
  - .NET: the full suite, a Release build `--no-incremental` with 0 warnings, and 0 vulnerable packages.
- **Contract:** `sync-contract.mjs` once per contract commit. `web/src/api/contract.test.ts` green. The diff of `web/src/api/generated/**` is exactly the new paths, fields and schemas, plus the SOURCE header.
- **Red-proof table:** per item: the term, the tamper, `RED n/m` on the full suite, the restore checked by sha256. After every restore, touch the file and build `--no-incremental`. At least these tampers must go RED:
  - 46: copy the approval state (or the snapshots, or the rejection reason) onto the duplicate; skip the read check on the source; let a non-internal caller duplicate internal inputs;
  - 55: drop one lifecycle event kind; let a PATCH write the events; classify the events `P`; send them without internal metrics; lose them on restart;
  - 33: skip one of the four override fields; merge mono and colour into one entry; (if required) accept a rental override change with no reason;
  - 47: classify one internal field CUSTOMER_SAFE; let the proposal bind outside the registry;
  - 49: skip the event on a draft proposal; record an event on a refused call; bump the revision on generation.
- **Playwright** (stub and live, synthetic data only; mask money cells): no new screen is in scope. Run the full suites to prove nothing user-visible moved. `smoke.spec.ts` failing in stub mode, and live against a synthetic store, is pre-existing (B28/B30 Deferred). Report it; do not count it as yours.
  - Evidence goes in `Briefs/2026-10-11_B35_evidence/` (folder 0700; files 0600).
- **B17 leak + secret scan** over `git diff origin/main...HEAD` and `git log --format=%B origin/main..HEAD`: counts only, with a planted control that fired. Never print the avoid list.
- **No infra change:** `git diff --numstat <base> -- infra scripts .github src/MpsCalc.Engine src/MpsCalc.Import src/MpsCalc.Api/Inventory src/MpsCalc.Api/Sources` is empty.

## NEW WORDS (verbatim; Friday shows Kam before any deploy)
Every user-visible or API-visible string you add or change goes in STATUS: old → new, with `file:line` at your head. That includes problem `code`s and messages, event `kind` names, and any audit `reason` text the server writes (such as a created-entry reason for the duplicate). Keep the words plain and short. Never copy wording from the example document.

## FOUND / TESTED / HOW / NOT TESTED
For each item, a four-line block in STATUS:
- **FOUND:** what you found at base (cite `file:line`);
- **TESTED:** the tests that pin the new behaviour (file and name), red-first counts;
- **HOW:** the instrument (suite, tamper, read-back), with ratios;
- **NOT TESTED:** what is left, and why.

## STATUS sections
- BLUF;
- PRIOR-WORK CHECK;
- Commits;
- Test Evidence;
- Red-proof table;
- Tier-1 conditions;
- FOUND / TESTED / HOW / NOT TESTED (per item);
- Modified pre-existing tests (before → after, why);
- NEW WORDS;
- UNMEASURED;
- `## NOT DONE / NOT COVERED`, as prominent as the evidence (each NARROWING remainder by ticket);
- needs-Friday (Jira comments are Friday's: give him one draft line per ticket, "advances, not Done");
- Leak + secret scan;
- processes started / stopped;
- worktrees and files left.

## Time-box
**About 3 h.** If you run short, finish in this order: 46, 55, 33, 49, 47 (49 rides on 55's events; 47 is the widest refactor). List what is left as **NOT DONE**, never half-merged. Each item is its own commit.

## UNMEASURED (by the draft writer)
- **Whether `Contracts/Dtos.cs` and `Program.cs` are unfrozen** for B35: Friday rules at firing.
- **Whether the rental web flow can send a reason** (item 3's gate): measure at base.
- **Test counts at `db8edfd`** (the seat measures them).
- **Whether another seat holds an open branch on the contract** at firing. At drafting, `ls-remote` lists no branch newer than `b30/card-defaults` (`cad7abd`, merged as #24) and no open PR (the reconcile: PRs #1–#24 all closed).
- **Ports 6620–6629 at firing:** free at ~16:4x (lsof); re-check before you bind.

## HOLDS
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert; never ask for a bypass.
- No deploy, no Azure write, no setting change; nothing to any human.
- Never delete; quarantine.
  - Quarantine to `.tools/_quarantine/2026-10-11_B35_<what>/` (0700) and say so.
  - Never edit a running script.
- SITE HOLD: none of the four store path settings changes; ReferenceStorePath stays a regular file.
- No pricing rule changes. No price, total or applied percent moves on any fixture.
- **No real client data anywhere.** The price books and the example quote are CONFIDENTIAL; report counts only. That covers code, tests, fixtures, screenshots, commit messages and STATUS. Price-book values never leave `.local/pricebooks/`.
- **Own worktree and own ports.**
  - Allowed: `fetch`, `worktree add`, commits and pushes on your own branch.
  - Never `checkout` or `switch` in `2_Project_Files`.
  - Never `gc`, `prune`, `worktree remove`, `branch -D` or force-push.
  - No merge, no Jira write.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate` and the shared `VBCSCompiler` are Friday's.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`. Build with `UseSharedCompilation=false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero has a positive control that fired.
- **Records:** write only your STATUS and your evidence folder. `CLAUDE.md`, `BACKLOG.md`, `history.md` and Jira are Friday's.

## End
The last line of `Briefs/2026-10-11_B35_STATUS.md` is one of these:
- `READY FOR GATE — b35/api-quote-lifecycle-audit @ <sha>`, with `<sha>` read back by `git ls-remote` in the same action as the push;
- `STOPPED: NEEDS FRIDAY` and one question.
