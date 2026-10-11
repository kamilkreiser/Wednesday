From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to friday-laptop-agent@agentmail.to. This project has no mail key, so your STATUS file is your wrap.
# BRIEF B40 · SEAT-A: lane A2, source lifecycle and admin API: governed source versions, stage / validate / activate / rollback (MPSCALC-50), admin source API (MPSCALC-53, API half)
**Written:** @NOW@ AEDT 2026-10-12. This is a draft. Friday sets the time when he fires it. **Pane:** `Datasec/MPS-A`. Your commission is the newest file in `Briefs/` whose name contains `_SEAT-A_`.
(The draft writer checked the launcher. `Launch_Claude.command:107` takes the seat letter from a pane name that matches `*MPS*-?`. Line `:111` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". At drafting, the newest `_SEAT-A_` file was `2026-10-11_B35_SEAT-A_api-quote-lifecycle-and-audit.md` (`ls -t Briefs | grep _SEAT-A_`). This file replaces it. `tmux list-panes -a`: 0 MPS pane titles.)
**Seat:** Seat A, a Claude build seat. One branch, red-first. **QA tier 1** throughout: this lane changes which prices every new calculation uses, and adds Administrator-only API routes.
**Round:** round 1 of a new lane (the two-NO-GO cap starts fresh).
**Report:** `1_Project_Definition/Briefs/2026-10-12_B40_STATUS.md`. Its **last line** is exactly one of these:
- `READY FOR GATE: b40/source-lifecycle-admin-api <sha>`, where `<sha>` is the full 40-hex SHA read back by `git ls-remote origin refs/heads/b40/source-lifecycle-admin-api` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.

## AUTHORITY
- **Friday commissions lane A2** from the board reconcile of 2026-10-11 (Friday's drafts, `2026-10-11_mpscalc_board_reconcile.md`, `## OPEN-A: file-disjoint lanes`). Its row, verbatim: *"**A2: Source lifecycle & admin API** (after A1) | 50, 53 (API half) | `src/MpsCalc.Api/Sources/**`, new admin endpoints, contract | `src/MpsCalc.Import/**` is frozen. Activation must keep the B27-H1 HOLD on store paths"*. And: *"only one API-plus-contract lane runs at a time. A1 runs first and A2 rebases on it."*
- **Why A2 now (the draft writer's measure):** A1 is merged. B35 merged as PR #25 (`6c0ba85`) and its fix round B37 as PR #26 (`4437460`), per `git log --oneline -40 origin/main` (top two lines). No A2 work exists: `git log --oneline -40` has 0 subjects naming MPSCALC-50/-53, sources lifecycle or admin; `ls-remote` lists no `b38`…`b40` code branch. Records BACKLOG still carries the row *"Source lifecycle not built: activation = restart the API on a new store file … Why deferred: out of B03 scope (MPSCALC-50, -53)"* (`git show main:BACKLOG.md`, records `main` `564f86d`, lines 104-108). Nothing in A2 waits on a Kam ruling for the slice below (see the Q list in HOLDS).
- **Ticket keys, measured, not taken from a range:**
  - **MPSCALC-50** "Source version lifecycle and atomic activation", parent MPSCALC-11 (Jira seed log `1_Project_Definition/Registers/2026-09-30_jira-seed-log.json`, item `plan E11-T35`). Reconcile row: *"OPEN-A | Not built (BACKLOG: "activation = restart the API on a new store file")"*.
  - **MPSCALC-53** "Administration console (role-separated)", parent MPSCALC-11 (seed log item `E11-T38`). Reconcile row: *"OPEN-A | Inventory screen shipped (#16, dep). No sources, templates or audit admin"*.
  - **MPSCALC-55** advances only (its remainder): B35 STATUS `## NOT DONE / NOT COVERED` (`2026-10-11_B35_STATUS.md:320`): *"Source-governance events (lane A2)"*. It is not a lane key; it gets a progress line.
  - **The draft writer could not read Jira** (no Jira access in this seat). The ticket texts below are the spec's rows, which the tickets cite. UNMEASURED: each ticket's own description and acceptance text. Read them (Jira `GET`, read-only) before you build and list any acceptance line this brief misses.
- **Spec (the only readable copy):** `1_Project_Definition/Source_Documents/2026-09-30_from-Kam_renderings/Developer_Specification_and_SOW_v1.0_TEXT.md` lines 628-640 (FR-ADM-001…013), 924-928 (the five `/api/v1/admin/sources` routes), 1102 (DATA-IMP-002), 1136 (the regression line), 145 (the Administrator role: *"Import/validate/activate/expire/rollback source datasets … Cannot alter approved snapshot history."*).
- These stand unchanged: C-07 (current until superseded), C-12, the I-2 matrix (C-13), **Q-16 (MPSCALC-82, retention: still the default; build nothing that deletes)**, the SITE HOLD and the P-1 HOLD (both in HOLDS).

## READ WHOLE FIRST
- The project `CLAUDE.md`; `1_Project_Definition/CLARIFICATIONS.md` on records `main` (`564f86d`; it ends at C-22: `git show main:1_Project_Definition/CLARIFICATIONS.md | grep -n '^### C-'`); `Questions_and_Answers/00_QUESTIONS_FOR_KAM.md` (Q-09 `:20`, Q-10 `:21`, Q-16 `:27`).
- Records `BACKLOG.md` on `main`: `## Holds on the hosted site` (lines 16-28) and the rows `[B27-H1]` (230-246) and "Source lifecycle not built" (104-108).
- `Briefs/2026-10-11_B35_SEAT-A_…md` and `2026-10-11_B35_STATUS.md` (the A1 shape: events, registry, NEW WORDS), `2026-10-11_B37_STATUS.md` (K-5's transitive allow-list walk) and `2026-10-11_B38_STATUS.md` (the gate's findings L-1…L-4 and P-1).
- `docs/IMPORTER.md` at base (what the importer writes; `:89` lists this lane as "Not in this lane").

## Base and branch
- **Base: MPS main = `44374606f49bc5c5498ad7fbd19230de487d85c2`.**
  - The draft writer read it at 05:5x AEDT 2026-10-12 with `git -C 2_Project_Files ls-remote origin`, which printed `44374606f49bc5c5498ad7fbd19230de487d85c2 refs/heads/main` (and the same for `HEAD`).
  - `log -1 --format='%H %T %P %s'` printed tree `2c1fd884bd833bddd76ea622a05b1d2a80d5f74f`, the single parent `6c0ba857501f6568800b060d0b084950f885c9d1`, and the subject "B37: gate B36 fix round K-1..K-5 + K-7 (deltas gate B38 GO WITH NOTES) (#26)".
  - **The tree equals `f48edf0`'s** (B37's head; `log -1 --format='%H %T' f48edf0` prints tree `2c1fd884…`), so B38's `file:line` cites hold at this base. `f48edf0` is not your base: base on main.
  - Local `origin/main` is already `4437460` (`rev-parse origin/main`). Fetch anyway.
- **First action:** run `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/main`.
  - If it prints `4437460…`, proceed.
  - If it prints a descendant of `4437460`, list `git diff --name-only 4437460 <main>`. If that list touches any path in your write set, **STOP: NEEDS FRIDAY**. Otherwise base on the new main and say so.
  - If it prints anything else, **STOP: NEEDS FRIDAY**. Never rebase on your own.
- Branch `b40/source-lifecycle-admin-api`, in a fresh worktree `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B40'` (`chmod 700`). Take base measures in `.tools/wt-B40-base`, detached at your base.
- The draft writer read every `file:line` below at `4437460` with `git show 4437460:<path>` / `git grep … 4437460`. Re-check each one at your base before you edit, and list any that moved.
- **Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.** The Datasec org requires CodeQL.

## Ports
**6640–6649** (API 6640, web 6643 by default).
- The draft writer checked at 05:58 AEDT 2026-10-12: `lsof -nP -iTCP:6640-6649 -sTCP:LISTEN` printed **nothing** (rc 1): **0 listeners**.
- These ports were named once before: B34 (Seat R, records only) held them and bound nothing (`2026-10-11_B34_STATUS.md:207`: *"a listener check on 6640–6649 found **0**"*). B34 is finished (its STATUS exists). **Friday reassigns 6640–6649 to B40.** This overrides the standing line "never use any port named in an earlier brief" for this range only. B38's "never bind" list (`B38_SEAT-E…md:76`) was for B38.
- Every other port named in an earlier brief or STATUS stays off limits (for example 6900–6919, 6620–6629, 6750–6869, 5080, 5173). Check that your ports are free before you bind. Playwright and run-demo find your ports through env. Never edit a shared config default.

## Write set
- **New files** under `src/MpsCalc.Api/Sources/**` (for example a version store, a lifecycle service, admin endpoints, a governance-event type), and the existing `src/MpsCalc.Api/Sources/ActiveSources.cs`;
- `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`: **only** (a) `ListSources` (`:546-556`) and its route line (`:51`), to move or extend the admin list, and (b) the `SOURCES_UNAVAILABLE` message at `:219` if its words ("…and restart.") stop being true. Name every line;
- `src/MpsCalc.Api/Quotes/ExportFieldRegistry.cs`: **only** `AdminTypes` (`:61`), to register the new admin DTO types as ADMIN_ONLY;
- `tests/MpsCalc.Api.Tests/**`, new and existing files. List every modified pre-existing test in STATUS, before → after, with the reason;
- `docs/API.md`, `docs/api/openapi.json`;
- `web/src/api/generated/**`, regenerated **only** by `web/scripts/sync-contract.mjs`, as its own `contract:` commit, never by hand.

**Friday rules at firing** (the reconcile's write set does not name them; until Friday's line below is filled in, a need for either is `STOP: NEEDS FRIDAY`):
- `src/MpsCalc.Api/Contracts/Dtos.cs`: for the new admin DTOs only (the existing `AdminSourceDto` is at `:325-328`, `SourceListDto` at `:330`). Friday: `______`.
- `src/MpsCalc.Api/Program.cs` (101 lines at base): for the `IActiveSources` registration only (`:64-66`) and the admin route mapping. Keep the diff minimal and name every line. Friday: `______`.

**Frozen:**
- `src/MpsCalc.Engine/**`, `src/MpsCalc.Import/**` (call its public API, such as `ReferenceStore.Load` at `Store/ReferenceStore.cs:73`; never edit it);
- `src/MpsCalc.Api/Inventory/**` (lane A3 and `[B27-H1]` live there). Note: `InventoryEndpoints.cs:34` and `:182` read `IActiveSources.Current`, so activation changes what the inventory lists. Measure it (see Item 3); do not edit it;
- every other file under `src/MpsCalc.Api/Quotes/**` (including `QuoteFileStore.cs`, `QuoteStore.cs`, `Proposal.cs`, `PricingPolicy.cs`);
- `web/src/**` except `generated/**`; `infra/**`, `scripts/**`, `.github/**`, the root build files; `docs/{DEMO,ENGINE,IMPORTER}.md` (lane D's). If `IMPORTER.md:89` becomes untrue, record it for lane D (RECORDS); do not edit it.

If origin carries another seat's open branch that is newer than your base and touches your write set: **STOP: NEEDS FRIDAY**. At drafting, `ls-remote` listed no branch newer than `b37/gate-b36-fix-round` (`f48edf0`, merged as #26).

## Tier 1 (all items)
- **Red proof, one conjunct at a time.** Every item's test is red at base, green at your head, and red again when the fix is tampered back. Restore by sha256, then touch and build `--no-incremental`.
- **With the new feature off, behaviour is today's, byte for byte** (see Item 1's off switch): the full suite, the proposal bodies and the calculations equal base.
- **Approved history never moves (FR-ADM-009, spec `:636` and `:1136`):** after stage, activate and rollback, every existing snapshot, approved proposal body and stored calculation is byte-equal to before. Serialise before and after.
- **The I-2 matrix is byte-for-byte unchanged:** `git diff <base> -- web/src/auth/pricePolicy.ts src/MpsCalc.Api/Quotes/PricingPolicy.cs` is empty, and `RoleMatrixTests` and `PricingPolicyTests` are green.
- No price, total or applied percent moves on any existing fixture **under the source set that was active when it was made**.
- **No price leaves an admin route.** The existing list says "no prices" (`docs/API.md:21`); the new routes and validation summaries keep that. Import findings never carry a cell value (`src/MpsCalc.Import/ImportTypes.cs:16`). Prove it with a planted-price control.
- Only an Administrator reaches a lifecycle route (spec FR-ADM-001 `:628`: *"Seller/pricing role cannot access raw source maintenance."*). Every new route is in `RoleMatrixTests`, both auth modes.
- Every new DTO type is in `ExportFieldRegistry.AdminTypes`, and **every type reachable from `AdminTypes` is listed too** (extend B37 K-5's transitive walk to `AdminTypes`; `QuoteApiTests.ExportRegistry.cs:20-22` concatenates `AdminTypes` today but does not walk it). No exemption list: if you need one, **STOP: NEEDS FRIDAY**.

## PRIOR-WORK CHECK (record before you change anything)
- **Suites at this tree:** B37 measured **.NET 946/946** (235 + 72 + 639), Release with 0 warnings, 0 vulnerable packages, and **web 325/325** (50 files) at `f48edf0` (`2026-10-11_B37_STATUS.md:15`, `:38`, `:41`), the same tree as base. Re-measure both at your base. Do not trust these numbers.
- **Today's source model:** one reference store file, loaded once at start. `StoreFileActiveSources.Load` (`Sources/ActiveSources.cs:64-82`) reads `MpsCalc:ReferenceStorePath` into a `FixedActiveSources` (`:56-59`, a settable `Current`). `IActiveSources` (`:49-53`) has `Current` only. `ActiveSourceSet.From` (`:21-45`) makes three source infos (devices, options, software) from one store document. Registered at `Program.cs:64-66`.
- **The admin list:** `GET /api/v1/admin/sources` (`QuoteEndpoints.cs:51`, handler `:546-556`), Administrator only (`:548`), state hard-coded `"Active"` (`:554`). Contract: `docs/api/openapi.json:381`, `docs/API.md:21` and `:495`. Tests naming the route: `EntraAuthTests.cs`, `GateFindingTests.cs`, `QuoteApiTests.cs`, `RoleMatrixTests.cs:116`, `StartRefusalTests.cs` (`git grep -l admin/sources 4437460 -- tests`).
- **Who reads the active set:** calculate reads `sources.Current` once into `active` (`QuoteEndpoints.cs:217`) and answers 503 `SOURCES_UNAVAILABLE` with *"…Import the price books into the reference store (mpscalc-import) and restart."* (`:219`); the catalogue reads (`:643-703`), a read at `:770`, and the inventory (`Inventory/InventoryEndpoints.cs:34`, `:182`). Snapshots carry `SourceVersions` (`Contracts/Dtos.cs:292`); calculations carry them too (`:135`).
- **Validity states already exist in the engine:** `SOURCE EXPIRED`, `SOURCE NOT YET VALID`, `SOURCE CURRENT UNTIL SUPERSEDED` (`src/MpsCalc.Engine/Calculation/QuoteCalculator.cs:168-195`, FR-ADM-012).
- **The store path rules you must not weaken:** the hosted reference path may not sit in `wwwroot` (`Program.cs:38-42`); the overlay refuses to overlap the quote or reference store (`Program.cs:59-62`; `[B27-H1]` is the open hole in that check).
- **The registry:** `ExportFieldRegistry.AdminTypes = [typeof(AdminSourceDto)]` (`ExportFieldRegistry.cs:61`); `MayBind` lets only an Admin audience bind ADMIN_ONLY (`:67-73`).
- **Spec routes (`TEXT.md:924-928`):** `GET /api/v1/admin/sources`; `POST /api/v1/admin/sources/{type}/imports` (stage); `POST …/{versionId}/validate`; `POST …/{versionId}/activate`; `POST …/{versionId}/rollback`.

## ITEMS (in this order; red test first for each; one commit per item, contract sync as its own commit)

### 1. MPSCALC-50: a governed source-version store, with an off switch (NARROWING)
**Spec:** FR-ADM-012 (`:639`) *"Source lifecycle MUST support Draft, Validating, Active, Expired, Failed Validation and Superseded."*; FR-ADM-007 (`:634`); DATA-IMP-002 (`:1102`).
- A new, optional setting names a directory for governed source versions. **Empty (the default in every shipped appsettings) = today's behaviour exactly:** one Active set from `ReferenceStorePath`, and the lifecycle routes answer a refusal (say which status and code; NEW WORDS).
- **DevStub only this round.** In Entra (hosted) mode the setting must stay empty, or the start is refused with a message; say which you chose and why. No hosted setting is added or changed (SITE HOLD).
- The directory follows the quote store's local rule (under `<work tree>/.local/`, not tracked by git; precedent `QuotePersistence.Open`, `Program.cs:53`), is refused if it overlaps the quote store, the overlay or the reference file's directory (resolve links, including a file link: learn from `[B27-H1]`), and is written by temp-file-plus-rename.
- **The configured reference file is the first Active version, by reference.** It is **never rewritten, moved, copied over or replaced by a link**, and `ReferenceStorePath` itself never changes (SITE HOLD). Prove its sha256 is unchanged after every lifecycle step.
- State words: the spec's six, exactly. A version that has passed validation and awaits activation needs a state: say which of the six you use and why. **A seventh word: STOP: NEEDS FRIDAY.**
- It survives a restart (prove it as `QuotePersistenceTests` does): the same version is Active, and the states and events read back equal.
- **Q-16 default (record it; do not decide it):** *source versions and their events are kept for the life of the store; nothing is pruned, expired by age or deleted.* Write that sentence in `API.md`, marked "default pending Q-16 (MPSCALC-82)". Build no deletion, TTL or cap.

### 2. MPSCALC-50: stage and validate (NARROWING)
**Spec:** FR-ADM-007 *"Import MUST create a Draft/Validating source version and MUST NOT affect active quotes until activation."*; FR-ADM-008 (`:635`) row-level summary; routes `:925-926`.
- **Narrowing:** the staged unit is **one reference store document as the importer writes it** (all three source types together, as `ActiveSourceSet.From` reads them). Per-type staging (`{type}` in the spec route) and raw spreadsheet upload (FR-ADM-013) are **NOT DONE**: they need the importer split by type, and `Import/**` is frozen. Say how your route shape leaves room for `{type}` later.
- Stage → a new version id and state; validate → the store document's own checks (`ReferenceStore.Load` and the document validators) plus: duplicate version ids, a version that is already Active, an empty set. A failure → `Failed Validation` with a row-level summary that names rows and codes and **never a value** (prices, SKUs from the confidential books: counts and codes only).
- Staging and validating **never change `Current`**: a calculation during and after validation uses the old Active set (prove it with a calculation id/source-version read before and after).
- Size and shape limits on the request body (state them); an over-size or malformed body is refused with nothing stored.

### 3. MPSCALC-50: atomic activation (NARROWING)
**Spec:** FR-ADM-009 (`:636`) *"Activation MUST affect new/recalculated drafts only; approved snapshots retain original source versions."*; route `:927`.
- Activate a validated version: it becomes Active, the previous Active becomes `Superseded`, in one step. The persisted pointer is written by temp-plus-rename; `Current` is swapped once, so a calculation sees the old set or the new set, never a mix (calculate reads `Current` once at `QuoteEndpoints.cs:217`; prove it with a concurrent test).
- A crash between the file write and the swap leaves a consistent state on restart (use a seam in your own new file; no seam in frozen files).
- After activation: a recalculated draft carries the new `SourceVersions`; every approved snapshot, approved proposal and stored calculation is byte-equal to before (Tier 1).
- **Measure, do not fix,** what the inventory and the catalogue overlay do when the new set lacks a key the overlay holds (`Inventory/**` is frozen). Report the counts; any wrong output is a RECORDS row for lane A3, not a fix here.

### 4. MPSCALC-50: rollback (NARROWING)
**Spec:** FR-ADM-011 (`:638`) *"Rollback MUST reactivate a prior governed version with a full audit event."*; route `:928`.
- Rollback reactivates a chosen `Superseded` version; the current Active becomes `Superseded`. The same atomicity and approved-history proofs as Item 3.
- A `Failed Validation` or never-activated version cannot be rolled back to (refused, nothing changed).
- **Expire** (FR-ADM-010, *"according to policy"*) is **NOT DONE**: the policy is Kam's (Q-10, MPSCALC-76). The engine already blocks an expired source by date (`QuoteCalculator.cs:191`).

### 5. MPSCALC-53 (API half) + MPSCALC-55 remainder: the admin list and source-governance events (NARROWING)
**Spec:** FR-ADM-001 (`:628`); FR-ADM-002 (`:629`) *"Source lifecycle events are persisted."*; §23.2 "Source governance" (`TEXT.md:999`).
- `GET /api/v1/admin/sources` lists every governed version with its real state (not the hard-coded `"Active"` at `QuoteEndpoints.cs:554`), and filters by type and state as the spec row (`:924`) names. With the feature off, the body is byte-equal to base.
- One append-only, server-written event list for source governance: staged, validated, failed validation, activated, superseded, rolled back. Each event: kind, UTC time, actor (caller id and persona, as `QuoteEvents` records them), role(s), version id, and the prior Active id where it exists. Persisted, survives restart, ADMIN_ONLY, never client-writable.
- **Not built:** the admin console UI (lane B or later), template admin, audit admin across quotes.

## Test Evidence (run each command as `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head, in `wt-B40-base` and `wt-B40`:** .NET full suite, Release `--no-incremental` with **0 warnings**, `dotnet list package --vulnerable --include-transitive` 0; web `npm ci`, `lint`, `typecheck`, full `test`, `build`. Reconcile every count change by test name.
- **Contract:** `sync-contract.mjs` once per contract commit; `web/src/api/contract.test.ts` green; the `generated/**` diff is exactly the new paths, fields and schemas plus the SOURCE header.
- **Red-proof table, one line per conjunct:** the term, the tamper, `RED n/m` on the full suite, the sha256 restore. At least these tampers go RED:
  - 1: the off switch leaks (a lifecycle route answers with the feature off); the reference file is rewritten; an overlapping directory is accepted (file-link form too); a state is lost on restart;
  - 2: staging changes `Current`; a value appears in a validation summary; a failed version is stored as passed;
  - 3: the swap happens before the persisted write; the old Active is not marked Superseded; a snapshot or approved proposal byte moves; a Seller or Approver can activate;
  - 4: a Failed Validation version can be rolled back to; rollback records no event;
  - 5: the list still says `"Active"` for every row; an event is client-writable; events reach a non-Administrator; a new DTO type missing from `AdminTypes` passes the registry guard.
- **Probes** (synthetic stores only; copy, never run in place, any `.tools/qa-B36/` or `qa-B38/` probe you reuse) against your head API on your ports, both modes (DevStub, and Entra-fake to prove the feature stays off there): stage → validate → activate → calculate → rollback → calculate, with the reference file's sha256 and every approved proposal body read before and after.
- **Synthetic source documents only.** Build them from the importer's fixture path (the importer's own synthetic test inputs), never from `.local/pricebooks/`. Report counts.
- **Playwright** (stub and live, synthetic data; mask money cells): no screen changes, so the full suites prove nothing user-visible moved. Report the known `smoke.spec.ts` timeout (B36 N-7) as pre-existing.
- **Leak + secret scan** over `git diff <base>...HEAD` and `git log --format=%B <base>..HEAD`, using copies of B36's/B38's leak tools and list builders. Counts only, each class with a planted control that fired. Never print the avoid list.
- **No frozen change:** `git diff --numstat <base> -- infra scripts .github src/MpsCalc.Engine src/MpsCalc.Import src/MpsCalc.Api/Inventory web/src/auth/pricePolicy.ts src/MpsCalc.Api/Quotes/PricingPolicy.cs src/MpsCalc.Api/Quotes/QuoteFileStore.cs src/MpsCalc.Api/Quotes/QuoteStore.cs src/MpsCalc.Api/Quotes/Proposal.cs docs/DEMO.md docs/ENGINE.md docs/IMPORTER.md` is empty.
- Evidence goes in `Briefs/2026-10-12_B40_evidence/` (folder 0700, files 0600). Tools and logs go in `.tools/qa-B40/` (0700).

## NEW WORDS (verbatim; Friday shows Kam before any deploy)
Every user-visible or API-visible string you add or change goes in STATUS under `## NEW WORDS`: old → new, with `file:line` (or JSON path) at your head. That covers problem `code`s and messages, state words, event `kind` names, start-refusal messages, the OpenAPI `summary`/`description`/`enum` strings, every added and removed line of `docs/API.md`, and the `SOURCES_UNAVAILABLE` text if it changes. **No generic row** (B36 K-7). Run copies of B36's `words36cs.py` and `newwords36.py` over `<base>...<head>`: every extracted string appears in your table (count = count), with a planted undeclared string that the check flagged. Scan the new words against the example-document sentence list with copies of the B36 list tools, counts only: **0 hits**, with a control that fired. Never copy wording from the example document.

## RECORDS (route: a LOCAL `records/b40` branch, commit only)
- **The draft writer measured the records repo (the project root), read-only:** `git remote -v` printed **0 lines** (no remote, nothing is pushed). Records `main` = `564f86d624e0a04bf74fd326f5cf516d73d02134` ("Records: C-22 … (B39)"); `git branch -a` lists `records/b12 b21 b25 b30 b34 b37 b39`, all folded (B39 STATUS: `--no-merged` empty after its fast-forward).
- **Steps:** `git -C '<project root>' worktree add .tools/wt-B40-records -b records/b40 main`, then `chmod 700`. Commit there only. Never `checkout`, `switch`, `stash`, `merge` or `reset` in the root worktree. Never fold into `main`: that is Friday's.
- **Add rows to `BACKLOG.md` under `## Deferred problems`** in the existing row shape (Where / Symptom / Fix shape / Why deferred / Discovered), each with source and date, one commit `Records: lane A2 remainders (B40)`:
  - per-type staging and raw spreadsheet upload (FR-ADM-013; needs the importer split, `Import/**` frozen);
  - expire action (FR-ADM-010; Q-10);
  - the hosted switch-on of the version store (SITE HOLD; needs a brief that lifts it);
  - whatever Item 3's inventory/overlay measure finds (for lane A3);
  - `docs/IMPORTER.md:89` now stale, if it is (for lane D);
  - one row per item you leave NOT DONE.
- **Update, do not delete,** the "Source lifecycle not built" row (lines 104-108): append a dated line saying what B40 built and what remains. Never remove a row.
- `CLAUDE.md`, `JIRA.md`, `history.md` and Jira are Friday's. Write none of them.

## FOUND / TESTED / HOW / NOT TESTED
For each item, a four-line block in STATUS:
- **FOUND:** what you found at base, citing `file:line`;
- **TESTED:** the tests that pin the new behaviour (file and name), with red-first counts;
- **HOW:** the instrument (suite, tamper, probe or read-back), with ratios;
- **NOT TESTED:** what is left, and why.

## STATUS sections
- BLUF, with a one-line verdict per item;
- PRIOR WORK (every cite above re-read at base, and which moved; what existed and why, before you replaced it);
- Commits;
- Test Evidence;
- Red-proof table;
- Tier-1 conditions;
- FOUND / TESTED / HOW / NOT TESTED, per item;
- State-word and route choices, and why (Items 1, 2);
- Modified pre-existing tests (before → after, and why);
- NEW WORDS (verbatim);
- UNMEASURED;
- `## NOT DONE / NOT COVERED`, as prominent as the evidence (each NARROWING remainder by ticket);
- RECORDS: the `records/b40` SHA, its rows, and `git log -1`;
- needs-Friday. Jira comments are Friday's, so give him one draft line per ticket: MPSCALC-50, -53, -55, "advances, not Done";
- Leak + secret scan;
- processes started and stopped;
- worktrees and files left.

## Time-box
**About 3 h.** If you run short, finish in this order: 1, 2, 3, 5, 4 (activation without rollback is still a safe, auditable slice; rollback rides on 3's swap). List what is left as **NOT DONE**, never half-merged. Each item is its own commit.

## UNMEASURED (by the draft writer, each with its closing instrument)
- **The ticket texts of MPSCALC-50 and -53** (no Jira read here). Closes with: your Jira `GET`, read-only, before building.
- **Whether `ReferenceStore.Load` can validate without a file path** (it takes `string path`, `Store/ReferenceStore.cs:73`), so staging may need a temp file inside your version directory. Closes with: your read of `Import/Store/**` at base.
- **What the inventory and overlay do after a set swap.** Closes with: Item 3's measure.
- **The suite counts at `4437460`:** B37 measured the same tree at `f48edf0`, not this commit. Closes with: your base run.
- **CodeQL and CI on PR #26:** the draft writer cannot see them (no `gh` in this seat). Friday reads them.
- **Ports 6640–6649 at firing:** free at 05:58. Re-check with `lsof` before you bind.

## HOLDS
- Datasec only. No other client's names, tickets or paths.
- **CodeQL policy:** push your branch only; never push to main; never dismiss an alert; never ask for a bypass. Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.
- **No deploy.** No Azure write, no setting change, nothing sent to any human.
  - **P-1 HOLD (records BACKLOG `## Holds on the hosted site`, B39, lines 24-28):** main `4437460` contains B37's K-3 refusal, so **before any hosted deploy of it, the hosted quotes with repeated fleet line numbers must be counted** (the gate's P-1, *"count the hosted quote files whose fleet (any version) repeats a `lineNumber`"*). That count is UNKNOWN today. This round deploys nothing and does not run P-1: it is a separate, read-only brief.
  - A hosted MPS deploy needs Kam's card. Hosted runs `db8edfd` (C-21; BACKLOG line 28).
- **SITE HOLD (BACKLOG lines 17-22, B25 ADDENDUM-1, until `[B27-H1]` is fixed and deployed):** none of the four store path settings changes (`MpsCalc__QuoteStore__Path`, `MpsCalc__QuoteStore__HostedRoot`, `MpsCalc__CatalogueOverlay__Path`, `MpsCalc__ReferenceStorePath`); `ReferenceStorePath` stays a regular file, never a link. Activation never repoints it.
- **Kam's open questions this lane must not decide:** Q-09 (MPSCALC-75, the Pricing Owner): **never activate a real price book**, only synthetic sets (MPSCALC-52's *"activate only after Pricing Owner review"*, reconcile row 52); Q-10 (MPSCALC-76): no expiry or exception policy; Q-16 (MPSCALC-82): the retention default above.
- No pricing rule change. No price, total or applied percent moves on any fixture.
- **No real client data anywhere.** The price books and the example quote are CONFIDENTIAL: report counts only, in code, tests, fixtures, screenshots, commit messages and STATUS. Price-book values never leave `.local/pricebooks/`.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-12_B40_<what>/` (0700), and say so. **Never edit a running script**; write a new file.
- **Own worktree and own ports.** Allowed: `fetch`, `worktree add`, commits and pushes on your own branch; on records, commits on `records/b40` only (no remote). Never `checkout` or `switch` in `2_Project_Files` or the project root. **Never `gc`, `prune`, `reset`, `worktree remove`, `branch -D` or force-push.** Never touch another seat's worktree (`wt-B35*`, `wt-B36*`, `wt-B37*`, `wt-B3?-records`, `qa-B3?/` are read-only: copy from them). No merge, no Jira write.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate`, the shared `VBCSCompiler` and any listener outside 6640–6649 are not yours.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`. Build with `UseSharedCompilation=false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero needs a positive control that fired.
- **Records:** write only your STATUS, your evidence folder, `.tools/qa-B40/`, your worktrees, and `records/b40` (RECORDS).

## End
The last line of `Briefs/2026-10-12_B40_STATUS.md` is exactly one of these:
- `READY FOR GATE: b40/source-lifecycle-admin-api <sha>`, where `<sha>` is the full SHA read back by `git ls-remote origin refs/heads/b40/source-lifecycle-admin-api` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.
