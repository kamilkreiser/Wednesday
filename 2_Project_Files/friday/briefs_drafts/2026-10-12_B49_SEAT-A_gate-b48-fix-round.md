From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to friday-laptop-agent@agentmail.to. This project has no mail key, so your STATUS file is your wrap.
# BRIEF B49 · SEAT-A: FIX ROUND for gate B48 (G-F1 Major, plus the Minors and Notes Friday reopens) on top of `b46/home-dashboard`
**Written:** 2026-10-12 16:50 AEDT (draft). **Fired:** @NOW@. **Pane:** `Datasec/MPS-A`. Your commission is the newest file in `Briefs/` whose name contains `_SEAT-A_`.
(The draft writer checked the launcher. `Launch_Claude.command:107` takes the seat letter from a pane name that matches `*MPS*-?`. Line `:111` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". At drafting (16:44 AEDT), `ls -t Briefs | grep _SEAT-A_` printed `2026-10-12_B46_SEAT-A_home-dashboard-build.md` first; its seat is closed (`B46_STATUS.md` last line `READY FOR GATE: b46/home-dashboard 0c74086a…`). This file replaces it.)
**Seat:** Seat A, a Claude build seat. One branch, red-first. **QA tier 1** throughout: G-F1 is a role-scope rule on a figures read, and the figures read is an Administrator-visible aggregate.
**Round:** FIX ROUND. This is **round 2 of 2** under Kam's two-NO-GO cap (lane: Home dashboard; B48 was round 1, `B48_STATUS.md:1`). The next gate is a **deltas gate** over `0c74086...<your head>`. **If it says NO GO, Friday ships what is closed and tickets the rest; there is no round 3.** So close each row completely, or list it as NOT DONE. Never leave a row half-done.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B49_STATUS.md`. Its **last line** is exactly one of these:
- `READY FOR GATE: b49/gate-b48-fix-round <sha>`, where `<sha>` is the full 40-hex SHA read back by `git ls-remote origin refs/heads/b49/gate-b48-fix-round` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.

## FIRST STEP (before anything else, Friday's order)
**Re-read B48's STATUS and take every finding in its FINAL form.**
- At drafting (16:45 AEDT) `Briefs/2026-10-12_B48_STATUS.md` was **364 lines**, its last line `READY FOR REVIEW` (`:364`), with `overall: NO GO` (`:16`, `:362`) and `B46 0c74086: NO GO`: one Major, G-F1 (`:7`, `:359`). Findings G-F1…G-F7 are at `:206-244`, Notes G-N1…G-N12 at `:246-258`, the mutant table at `:170-203`.
- **"Final" means:** the last line is `READY FOR REVIEW`; `## Findings` and `## Notes` are complete; every item named in `## Verdict lines` is defined. If any of these fails: **STOP: NEEDS FRIDAY**.
- `wc -l` it and diff against the cites here. If a quoted line changed, record each change in PRIOR-WORK CHECK; where the final text changes a quote below, the final text wins. **If a new Blocker or Major appears, STOP: NEEDS FRIDAY.**

## AUTHORITY
- **Gate B48** (`Briefs/2026-10-12_B48_STATUS.md`, Seat E, round 1 of 2) gave `B46 0c74086: NO GO`, `overall: NO GO`: **G-F1 Major**; G-F2, G-F3, G-F4, G-F5, G-F6, G-F7 Minor; Notes G-N1…G-N12.
- **Friday reopens these rows and rules on each one (ROWS below), so the seat does not ask:** G-F1, G-F2 (option 1), G-F3, G-F5 (Friday names B49 the owner), G-F6, G-F7, G-N9, G-N6.
- **Everything else from B48 is NOT YOURS THIS ROUND** (table below). Moving a row from NOT YOURS to yours is **STOP: NEEDS FRIDAY**. You may move one of your rows to NOT DONE only with a measured reason in STATUS.
- B46 is **not merged**. Main is still `b28c95eb` (see Base). This round builds on B46's head, not on main.
- These stand unchanged: Kam's D-1…D-7 rulings (B46 brief `:14-21`), the approved NEW WORDS §A (B46 brief `:22`), C-12 (no self-approval), I-2 (act-as only narrows), Q-09 (synthetic price sets only), the SITE HOLD and the P-1 HOLD (HOLDS).
- **Fix shapes marked "the gate proposes" are the gate's; verify before building.** If you build something else, say why in STATUS.

## READ WHOLE FIRST (all inside this project)
- The project `CLAUDE.md`; records `main` `1_Project_Definition/CLARIFICATIONS.md` (C-12).
- **`Briefs/2026-10-12_B48_STATUS.md` in full**, in particular `## Findings` (`:205-244`), `## Notes` (`:246-258`), the hand-count table (`:86-107`), the mutant table (`:170-203`), the e2e lines (`:12`, `:235-241`). Its evidence: `Briefs/2026-10-12_B48_evidence/` (`b48-click-live.json`, `b48-mut48.json`, `b48-mutprobe48.json`, `b48-fail48.json`).
- `Briefs/2026-10-12_B46_SEAT-A_home-dashboard-build.md` (241 lines; Item 2 `:91-94`, H-13 `:127`, H-16 `:130`, H-17 `:132`, H-22 `:137`, FIGURES AND CAPTIONS `:159-171`) and `Briefs/2026-10-12_B46_STATUS.md` (298 lines).
- The approved mock, records `1_Project_Definition/Design/2026-10-12_home-dashboard/` (`home-mockup.html`, `home-mockup.css`, `NEW_WORDS.md`, `renders/`): the spec for every word you touch.
- **The gate's instruments, read-only. Copy them into `.tools/qa-B49/`; never run them in place:** `.tools/qa-B48/tools/mut48.py` (anchors G8 `:25`, G9 `:26`, G17 `:32`), `model48.py`, `probe48.py`, `build48.py`, `age48.py`, `click48.mjs`, `fail48.mjs`, `ui48.mjs`, `b48lib.mjs`, `apictl48.sh`, `env48.sh`, `e2eall48.sh`, `words48.py`, `checkwords48.py`, `leak48.py`, `leakscan.py`, `qalib.py`. The gate's DST test file is quarantined at `.tools/_quarantine/2026-10-12_B48_gate-dst-test-file/` (`Gate48DstTests-control.cs`, `-G7.cs`, `-G8.cs`): read it for shape; never move it.

## Base and branch
- **Base: B46 head = `0c74086a9c23e485f71dc0c7e0f80d33a4c1b317`** (tree `5efdeca4e2c25af550a4cd0d94971b7c736324b7`, `B48_STATUS.md:33`). Main = `b28c95eb0f73ed0ce7ae410791feefc8b1a059ea`; `rev-list --left-right --count b28c95eb...0c74086` = `0 8` (B48 `:15`): B46 is a fast-forward of main with 8 commits.
  - Friday's `ls-remote` at ~15:16 AEDT, and the draft writer's at 16:44 AEDT, both printed `0c74086a9c23e485f71dc0c7e0f80d33a4c1b317 refs/heads/b46/home-dashboard` and `b28c95eb0f73ed0ce7ae410791feefc8b1a059ea refs/heads/main`, and no `b49` branch.
- **Branch: a new branch `b49/gate-b48-fix-round` cut from `0c74086`.** B46's 8 commits stay; your fixes go on top. Do not add commits to `b46/…` (the ref gate B48 pinned stays untouched). The deltas gate diffs `0c74086...<your head>`; Friday's PR from `b49/…` carries B46's 8 commits plus yours.
- **Step 0 (re-pin):** `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/b46/home-dashboard refs/heads/main 'refs/heads/b49*'`.
  - `0c74086…` and `b28c95eb…` and no `b49` → proceed.
  - `b46/…` moved, a `b49*` branch exists, or main moved and `git diff --name-only b28c95eb <main>` touches your write set → **STOP: NEEDS FRIDAY**. Never rebase on your own.
- Worktree: `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B49'` (`chmod 700`), `worktree add -b b49/gate-b48-fix-round … 0c74086`. Base measures in `.tools/wt-B49-base`, detached at `0c74086`. Tampers in `.tools/wt-B49-mut` (detached at your head; `git status` clean after each).
- The draft writer read every `file:line` below with `git show 0c74086:<path>`. Re-check each one at your base before you edit, and list any that moved.
- **Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.** The Datasec org requires CodeQL.

## Ports
**6640–6649** (API 6640, web 6643 by default). B46's range (`B46…md:57`); B46's seat is closed. **Friday reassigns 6640–6649 to B49**, overriding "never use a port named in an earlier brief" for this range only.
- `lsof -nP -iTCP:6640-6649 -sTCP:LISTEN` at 16:44 AEDT printed nothing (rc 1): **0 listeners**. **Check again with `lsof` before every bind**; on any listener you did not start, **STOP: NEEDS FRIDAY** (do not move ranges).
- Gate B48 used 6650–6659 (`B48_STATUS.md:347`). Never touch it, nor any other port named in an earlier brief or STATUS (e.g. 5080, 5173, 5183, 6620–6629, 6660–6699, 6750–6919). Never edit a shared config default.

## Write set (B46's files that the rows need, and nothing else)
- API: `src/MpsCalc.Api/Quotes/QuoteFigures.cs`; `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` (the `Figures` handler `:636-669` only); `docs/API.md` and `docs/api/openapi.json` (only the descriptions a row makes false); `tests/MpsCalc.Api.Tests/**` (`QuoteApiTests.Home.cs` and new files).
- Web: `web/src/screens/Dashboard.tsx`; `web/src/screens/Home.test.tsx` (and `Dashboard.test.tsx` only if a row forces it); `web/src/api/stub/stubApi.ts` (its figures mirror the server's, `:218-239`); `web/e2e/b46-home.spec.ts`; `web/e2e/b30.spec.ts` (**the G-13 test `:55-…` only**, Row 4); `web/src/api/generated/**`, regenerated **only** by `web/scripts/sync-contract.mjs`, as its own `contract:` commit.
- List every modified pre-existing test in STATUS, before → after, with the reason. **One is foreseen:** `QuoteApiTests.Home.cs:587-592` `B46_2_red_a_pricing_analyst_gets_both_awaiting_figures` asserts `awaitingApproval` = 2 with the comment "Seller: all submitted (scope all)"; Row 2 makes that the analyst's own Submitted.

**Frozen** (diff must be empty; for each one, a need is **STOP: NEEDS FRIDAY**):
- `src/MpsCalc.Api/Contracts/Dtos.cs` (no DTO shape change this round; see Row 8);
- `src/MpsCalc.Api/Quotes/**` except the two files above, including `QuoteFileStore.cs` (G-N10), `QuoteStore.cs`, `QuoteEvents.cs`, `PricingPolicy.cs`, `Proposal.cs`, `PriceAudit.cs`; `src/MpsCalc.Api/Auth/**` incl. `CallerResolver.cs` (G-N2); `src/MpsCalc.Api/Program.cs`;
- `web/src/screens/QuoteList.tsx` (G-N4), `web/src/app/router.ts` (G-N3), `web/src/screens/Lifecycle.tsx` (G-N11), `web/src/styles.css` (G-N8), `web/src/components/**`, `web/src/auth/**` incl. `pricePolicy.ts`, `web/src/proposal/**`, `web/playwright.config.ts`, every other `web/e2e/*.spec.ts`;
- `src/MpsCalc.Engine/**`, `src/MpsCalc.Import/**`, `src/MpsCalc.Api/Inventory/**`, `src/MpsCalc.Api/Sources/**`, `infra/**`, `scripts/**`, `.github/**`, root build files, `docs/{DEMO,ENGINE,IMPORTER}.md`.

If origin carries another seat's branch, newer than your base, that touches your write set: **STOP: NEEDS FRIDAY**.

## Tier 1 (all rows)
- **No GP, margin, cost, CPP, capital or target-GP value** reaches the list, the figures or the DOM, for any role. The figures stay **aggregates only**: no row, quote id, customer or owner (B46 `:93`). B46's planted-member controls (A3, A5) must still go RED.
- **Role scope on the server.** `awaitingMyApproval` exists only for a caller that holds Approver **after act-as** (I-2 only narrows): Seller+Approver acting as Seller gets no `awaitingMyApproval`; Administrator alone gets none; Approver without Seller still gets 400 `SCOPE_MINE_NEEDS_SELLER` for `scope=mine`. Re-run the gate's authZ cells for `/figures` (B48 `:63-78`, copy of `probe48.py`): 0 widening.
- **C-12 stands:** `awaitingMyApproval` never counts the caller's own quote (it counts `callerCan.approve`).
- **No price, total or applied percent moves** on any fixture (full engine + API suites). The outcome write is untouched by this round.
- **The I-2 matrix is byte-for-byte unchanged:** `git diff 0c74086 -- web/src/auth/pricePolicy.ts src/MpsCalc.Api/Quotes/PricingPolicy.cs` is empty; `RoleMatrixTests` and `PricingPolicyTests` green.

## PRIOR-WORK CHECK (record before you change anything; re-read each at `0c74086`)
- **Suites at `0c74086`, as measured by B46 and settled by B48** (B46 `:54-63`, B48 `:59`, `:270`): .NET Release `--no-incremental` **0 warnings**; Engine 235, Import 72, API **834** (= 1141); `dotnet list package --vulnerable --include-transitive` 0; vitest **358/358** (52 files); e2e (B48 `:12`, `:236`, `:240`): **stub** 2 failed (`smoke:13`, `b30:55`), **live** 10 failed (`smoke:13` + 9 `b46-home`). Re-measure all of it at your base. Do not trust these numbers.
- **The figures handler** (`QuoteEndpoints.cs:636-669`): `scope=mine` keeps only `f.IsMine` facts (`:662`) **before** `QuoteFigures.Figures` runs (`:668`).
- **The figures rules** (`QuoteFigures.cs:140-166`): `awaitingApproval` = Submitted over the scoped facts (`:163`); `awaitingMyApproval` = `CallerCan.Approve` over the scoped facts (`:164`). FY start `local.Month >= 7` (`:121`); closed figures `o.At >= StartOf(from)` (`:150`); follow-up `now - when > TimeSpan.FromDays(FollowUpDays)` (`:89`).
- **The stub mirrors them** (`stubApi.ts:218-239`): `inScope` (`:219`), `awaitingApproval` `:237`, `awaitingMyApproval` `:238`; the `figuresOmit` seam `:242-250`, `:328-330`.
- **Home** (`Dashboard.tsx`): `mine = seller && query.scope !== 'all'` (`:329`), `getQuoteFigures(scope)` (`:353`); tile 6 Approver href unscoped `{ status: 'submitted', canApprove: 'true' }` (`:93`); tile 6 Seller href `{ ...scope, status: 'submitted' }` (`:98`); the failing tile (`:144-162`) always prints "The other figures are not affected." (`:153`); `failed = figuresFailed || figures[t.key] === undefined` (`:450`); tile 2 `{figure.count} quotes` (`:174`); hint `{due.length} quotes need follow-up` (`:212`); days `Math.floor((loadedAt - Date.parse(r.approvedAt)) / DAY)` (`:244`) with `loadedAt = Date.now()` at list load (`:366`); the figures' `asOf` drives the stamp (`:418`).
- **The list body carries no `asOf`:** `QuoteListDto(IReadOnlyList<QuoteSummaryDto> Quotes)` (`Dtos.cs:408`); the figures body does (`QuoteFiguresDto`, `Dtos.cs:427`).
- **Docs that describe the rules you change:** `docs/API.md:423-424` ("`awaitingApproval` (a Seller: Submitted, in scope) and `awaitingMyApproval` (an Approver: `callerCan.approve`)"); `docs/api/openapi.json:1165` ("Seller only: Submitted quotes in scope."), `:1166` ("Approver only: quotes the caller may approve now."), and the `getQuoteFigures` description at `:164`.
- **e2e:** `b30.spec.ts:56` opens `/#/`; `:66` expects h1 "Quotes"; New quote is clicked at `:47`; the skip pattern is `:57-58`. `b46-home.spec.ts` (330 lines) has no skip; its `open()` asserts "API STUB ON" (`:31`; B48 `:240`). **`QuoteList.tsx` has no "New quote" button** (`git grep -c 'New quote' 0c74086 -- web/src/screens/QuoteList.tsx` → 0; `Dashboard.tsx` → 2).
- **The gate's three unguarded mutants** (B48 `:194-195`, `:203`; anchors `mut48.py:25`, `:26`, `:32`):
  - **G8** FY start `local.Month >= 7` → `local.Month > 7` (`QuoteFigures.cs:121`): API suite **0/834** RED; caught only by the gate's DST table (the 1 Jul roll, 1/8).
  - **G9** closed `o.At >= StartOf(from)` → `>` (`QuoteFigures.cs:150`): **0/834**; caught only by the gate's hand count (an outcome at exactly 30 Sep 14:00:00Z = 00:00 1 Oct AEST; 7/13 rows).
  - **G17** `awaitingMyApproval` = every Submitted, self-approval ignored (`QuoteFigures.cs:164`): **0/834**; caught only by the gate's analyst hand count (2/13 rows).

## ROWS (one commit per row, red test first; a contract sync is its own commit)

### Row 1 · G-F1 · Major · a Seller+Approver's "Awaiting my approval" is 0 by construction in My quotes
- **Finding, verbatim (B48 `:206`, `:208`):** *"a Seller+Approver's "Awaiting my approval" is 0 by construction in My quotes, and its list shows the quotes"*; *"The API keeps only the caller's own quotes for `scope=mine` (`QuoteEndpoints.cs:662`), and `awaitingMyApproval` counts `callerCan.approve` over those (`QuoteFigures.cs:164`). C-12 forbids approving your own quote, so the figure is always 0."* Measured: 0 against 4 (all four roles: 0 against 5), 3/3 runs; 2/60 tile clicks.
- **Friday's ruling (the gate's fix shape, `:214`; B46 brief Item 2 `:92` "Approver callers always get all quotes"):** `awaitingMyApproval` is an **Approver figure**. Count it over **every quote the caller may approve, whatever `scope` says.** Keep `scope` for the Seller figures (`provided`, `outOpen`, `followUpDue`, `closedMonth`, `closedYtd`, `awaitingApproval`).
  - Shape: the handler (`:656-668`) keeps every fact; `QuoteFigures.Figures` takes both the full set and the scoped set (or the handler computes `awaitingMyApproval` over the full set). Still only when `caller.Is(Roles.Approver)` after act-as. Mirror it in `stubApi.ts:238`.
  - Update `docs/API.md:424` and `openapi.json:1166` (and `:164` if it says otherwise) to say so; `contract:` sync commit; every changed line in NEW WORDS.
- **Red-first cell:**
  - **API test (the gate's regression, `:215`):** for a Seller+Approver, `GET /quotes/figures?scope=mine` `awaitingMyApproval.count` == the row count of `GET /quotes?status=submitted&canApprove=true` (and `valueExTax` == the rows' sum). The store must hold ≥ 1 quote another Seller submitted, so the count is > 0. Also for all four roles `scope=mine`, and `scope=all` unchanged. Both modes (DevStub and Entra), as B46's tests run.
  - **Browser check:** tile 6 equals its list for the **pricing-analyst persona** (`web/src/auth/dev/devPersonas.ts:14-16`, id `analyst`): a Home.test (vitest) and a `b46-home.spec.ts` stub-mode step that reads tile 6's number, opens its link and counts the rows. The stub's synthetic rows must give the analyst ≥ 1 approvable quote (measure; if 0, add one synthetic stub row and say so).
  - **RED at `0c74086`** (0 vs n); give `RED n/m`. **GREEN at head.**
  - **Tampered back RED:** restore the scope narrowing for `awaitingMyApproval`.
  - **Probe:** copies of `click48.mjs` (live, synthetic store) → **60/60** tile = list; `probe48.py` hand count 13/13 rows (with the Seller+Approver `mine` row now 4, all four `mine` now 5).

### Row 2 · G-F2 · Minor · Seller tile 6 under All quotes says "My quotes submitted…" but counts everyone's
- **Finding, verbatim (B48 `:217`, `:219`):** *"Seller A `scope=all` `awaitingApproval` = 5 (all Submitted) while their own Submitted = 3. The definition stays "My quotes submitted and waiting for an Approver."*
- **Friday's ruling: option 1.** The Seller's tile 6 counts the **caller's own Submitted quotes in BOTH scopes**, so the existing words stay true. **No new words.** Server `QuoteFigures.cs:163` (own = `IsMine`, identity, never `ownerName`; pre-owner quotes are nobody's) and the stub `stubApi.ts:237`.
  - **Consequence the draft writer found (verify):** tile 6's Seller href is `{ ...scope, status: 'submitted' }` (`Dashboard.tsx:98`), so under All quotes it opens `#/quotes?status=submitted`, which lists **everyone's** Submitted: the tile would then disagree with its list (the gate's click-through FAIL condition, B48 `:56`). **Default: tile 6's Seller href keeps `scope=mine&status=submitted` in both scopes** (no new words; a one-tile change to H-13's "scope=all drops `scope=mine&`", B46 `:127`). Record it under "Fix shape chosen" as a deviation from H-13 for Friday.
  - Update `docs/API.md:423` and `openapi.json:1165` ("Submitted quotes in scope" becomes false); NEW WORDS.
- **Red-first cell:** API test: a Seller with `scope=all` gets `awaitingApproval.count` == their own Submitted (gate: 3, not 5) and == the rows of the list tile 6 opens; `scope=mine` unchanged. Browser: tile 6 under All quotes == its list. RED at base; GREEN at head; tamper (count every Submitted under `scope=all`) RED. Modify `QuoteApiTests.Home.cs:587-592` (foreseen above), before → after.

### Row 3 · G-F3 · Minor · one failed figures read fails every tile, each saying "The other figures are not affected."
- **Finding, verbatim (B48 `:222`, `:225`):** *"on the real API one failed figures read fails every tile, each saying "The other figures are not affected."*; Seller 6/6, Approver 6/6, Admin 5/5.
- **Friday's ruling:** when the **whole** figures read fails (`figuresFailed`, `Dashboard.tsx:355`), **no tile carries "The other figures are not affected."** Show the existing error state without that sentence. This removes a sentence and adds no word. **Keep the per-tile sentence only where a single tile genuinely fails alone** (`figures !== null && figures[key] === undefined`, `:450`; the stub seam, H-16).
- **Red-first cell:** vitest: figures 500 → 0 tiles with the sentence, the other error words ("—", "Could not load this figure.", Retry) still there, follow-up and queue still render; one figure missing → that tile only, with the sentence. e2e stub (B46's H-16 step) stays green. Probe: copy of `fail48.mjs` live: 0/17 tiles carry it (Seller 6, Approver 6, Admin 5). RED at base; tamper (sentence back on whole fail) RED.

### Row 4 · G-F5 · Minor · `web/e2e/b30.spec.ts:66` red at head (stub)
- **Finding, verbatim (B48 `:236`):** *"Expects h1 "Quotes" at `#/`; head shows "Home"."*
- **Friday's ruling: B49 owns it.** Update the G-13 test to open `#/quotes` for its "Quotes" heading (the Quotes list moved; Home is now `#/`); do not expect "Quotes" at `#/`.
  - **Constraint the draft writer found:** New quote exists on Home only (`Dashboard.tsx:424-427`; `QuoteList.tsx` 0 hits), and the test clicks it (`b30.spec.ts:47`). **Default shape:** keep the form opened from `/#/`; at `:66` assert the page it returns to is h1 **"Home"**; add one step that opens `/#/quotes` and asserts h1 **"Quotes"**. The rest of G-13 is unchanged. If that shape cannot pass, **STOP: NEEDS FRIDAY**.
- **Cell:** stub e2e `b30:55` RED at base, GREEN at head; live mode stays skipped unless the B30 synthetic store is served (`:58`).

### Row 5 · G-F6 · Minor · `b46-home.spec.ts` has no live-mode skip
- **Finding, verbatim (B48 `:240`):** *"The full e2e in live mode (`VITE_MPSCALC_API_STUB=0`) gives 9/9 b46 tests red ("API STUB ON" not visible)."*
- **Ruling:** `test.skip(!stub, …)` in each b46 test (or one `beforeEach`), as `b30.spec.ts:57-58` does (detect stub by "API STUB ON"). The reason text says the spec is stub-only (synthetic data). That includes every test this round adds to the spec.
- **Cell:** live run: every b46 test **skipped, not failed** (count = the spec's tests); stub run: all pass. Tamper (skip removed) → live run reds again.

### Row 6 · G-F7 · Minor · "1 quotes need follow-up"
- **Finding, verbatim (B48 `:244`):** *"hint went "2 quotes need follow-up" → "1 quotes need follow-up". Same pattern on "n quotes" in tile 2."*
- **Ruling:** correct plurals wherever B46 builds an "n quotes" string: **"1 quote"**, **"n quotes"** (0 stays plural). The draft writer found two (`git grep` over B46's web diff): tile 2 `{figure.count} quotes · AUD ex GST` (`Dashboard.tsx:174`) and the hint `{due.length} quotes need follow-up` (`:212`; the singular takes the verb too: **"1 quote needs follow-up"**). Grep again; list every string you change, old → new, under NEW WORDS as **a grammar correction of declared words** (§A). Other count nouns ("n months", "n days", "Showing n of n drafts") are **not in this row**.
- **Cell:** vitest for 0, 1, 2 on both strings. RED at base; tamper (plural always) RED.

### Row 7 · G-N9 · Note · three gate mutants that B46's suite does not catch
- **Finding, verbatim (B48 `:255`):** *"B46's suite stays green for G8 (FY month `>` 7), G9 (period start `>`) and G17 (self-approval ignored in `awaitingMyApproval`)."* (Mutants described in PRIOR-WORK CHECK.)
- **Ruling: add the three guards the gate asked for**, as API tests with the test clock (`_host.Clock.Now`, as `QuoteApiTests.Home.cs:445-474`):
  1. **Fixed-clock July test (the financial-year roll):** `now` on a July day (e.g. 1 Jul 2026 and a mid-July day, Sydney): `closedYtd.periodStart` = `2026-07-01`; a win on 1 Jul counts in YTD, a win on 30 Jun does not. Must go RED on **G8**.
  2. **Exact-period-boundary outcome test:** an outcome recorded at exactly the month's start (00:00:00 1 Oct AEST = 30 Sep 14:00:00Z) counts in `closedMonth`; one a second earlier does not. Must go RED on **G9**.
  3. **Seller+Approver figures test:** Row 1's test. Must go RED on **G17** (self-approval counted): the analyst's own Submitted quote must not be in `awaitingMyApproval`.
- **Red-proof each:** apply G8, G9 and G17 from a copy of `mut48.py` to your head, full API suite, `RED n/m` each, sha256 restore. **G17's anchor (`mut48.py:32`) is the line Row 1 rewrites:** re-anchor it to the same meaning (count every Submitted in place of `callerCan.approve`) and say so. Also re-run the gate's other 14 mutants (`mut48.py`) and B46's 10 sampled (B48 `:171-183`): each still RED, re-anchored where a row moved its text, with counts reconciled.

### Row 8 · G-N6 · Note · "14 days" under "more than 14 days ago"
- **Finding, verbatim (B48 `:252`):** *"The follow-up "Days since approved" is `floor((browser now − approvedAt)/day)` (`Dashboard.tsx:244`). A quote due at 14 d + 1 min shows "14 days" under "more than 14 days ago" … It uses the browser clock, not `asOf`."*
- **Ruling:** compute the days display **the same way the server decides follow-up**: elapsed > 14 × 24 h from `approvedAt`, measured against the **server's `asOf`**, never the browser clock. So **no due row ever reads "14 days"** (or less) under "more than 14 days ago". Words unchanged ("n days").
  - **The draft writer's arithmetic (verify):** `ceil(elapsed / 24 h) > 14` exactly when `elapsed > 14 × 24 h`, so a `ceil` count agrees with the server's rule where `floor` does not (14 d + 1 min → 15).
  - **The clock:** the list body has no `asOf` (`Dtos.cs:408`, frozen). **Default:** use the figures response's `asOf` already on the page (`Dashboard.tsx:418`). When the figures read failed (no `asOf`), the days cell stays empty (the existing empty value, `:244`), never a browser-clock number. State in STATUS the residual skew between the two reads (the list decides `followUpDue` at its own `now`).
  - **If the fix needs any new word, or an `asOf` member on the list body (a `Dtos.cs` change): STOP: NEEDS FRIDAY** and list the words or the member instead of building them.
- **Cell:** vitest with a fixed `asOf`: a row at 14 d + 1 min shows "15 days"; 20 d exactly shows "20 days"; the browser clock moved by ±2 days changes nothing; figures failed → empty cell. RED at base; tamper (back to `floor` on `Date.now()`) RED.

## NOT YOURS THIS ROUND (Friday carries them to Kam or a later lane; do not touch, do not widen)
| Item (B48 line) | Why not this round |
|---|---|
| **G-F4** (`:231-233`) server `detail` texts + 3 `aria-label`s | Kam's NEW WORDS card (Friday). Do not reword, map or remove them. |
| **G-N1** (`:247`) unknown list parameter now 400 | Declared; no caller sends a query. |
| **G-N2** (`:248`) Entra display-name collapse | Pre-existing rule in `CallerResolver.cs:122` (frozen). Friday's hosted count. |
| **G-N3** (`:249`) router drops the whole query | `router.ts` frozen; a choice for Kam. |
| **G-N4** (`:250`) "Deals closed" label with no period word | `QuoteList.tsx` frozen; words for Kam. |
| **G-N5** (`:251`) Q-7 effect on closed values | By rule (Q-7). |
| **G-N7** (`:253`) failed save answers an empty body / developer page | Pre-existing. |
| **G-N8** (`:254`) main bottom padding 48 vs 32 | `styles.css` frozen. |
| **G-N10** (`:256`) load accepts an outcome on a Draft / unknown snapshot | `QuoteFileStore.cs` frozen. |
| **G-N11** (`:257`) stale tab keeps the control after 409 | `Lifecycle.tsx` frozen. |
| **G-N12** (`:258`) ≤600px rules change every screen, for the better | Informational. |
List them in STATUS under `## For the records seat` (one line each, as above). **Write no records commit and no `BACKLOG.md` row this round:** Friday's records seat does them from your STATUS.

## NEW WORDS (verbatim; Friday shows Kam before any deploy)
- Every user-visible or API-visible string this round adds, changes or removes goes in STATUS under `## NEW WORDS`, old → new, with `file:line` (or JSON path) at your head: Row 6's plurals (a grammar correction of declared §A words); Row 3's removed sentence (in the whole-read-failed state only); Row 2's tile 6 href (not a word, but list it); every changed line of `docs/API.md` and every changed `openapi.json` description (Rows 1 and 2). **No generic row.** **Target: 0 new words.**
- Run copies of `words48.py` / `checkwords48.py` over `0c74086...<head>`: every extracted string appears in your table (count = count); a planted undeclared string is flagged.

## Test Evidence (run each command as `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head (`wt-B49-base` at `0c74086`, `wt-B49`):**
  - .NET: a Release build `--no-incremental` with **0 warnings**; the full suite with **Engine, Import and API counts** each; `dotnet list package --vulnerable --include-transitive` 0.
  - web: `npm ci`, `lint`, `typecheck`, the full vitest `test` (count and files), `build`.
  - **The FULL Playwright suite in stub mode AND in live mode** (live = DevStub API on your ports with a synthetic store only; mask money cells), base and head: passed / failed / skipped per spec, **each failure named**. Expected at head: stub fails only `smoke:13` (pre-existing); live fails only `smoke:13`, every `b46-home` test skipped. Report `smoke:13` as pre-existing, not yours.
  - **Contract:** `sync-contract.mjs` once per contract commit; `contract.test.ts` green; the `generated/**` diff is exactly the changed descriptions plus the SOURCE header.
  - Reconcile every count change by test name (`--list-tests`, `comm`).
- **Red-proof table, one line per conjunct:** the term, the tamper, `RED n/m` on the full suite (API or vitest or e2e), and the sha256 restore. It covers Rows 1, 2, 3, 6, 8 (their tampers), Row 5 (skip removed), and Row 7 (G8, G9, G17 now RED on the suite, plus the gate's other 14 and B46's 10 sampled).
- **Probes** (copies; synthetic stores under `wt-B49/.local/b49-*`, since DevStub refuses a store outside `<work tree>/.local/`, B48 `:322`; your ports; DevStub, plus Entra-fake for the `/figures` authZ cells): `probe48.py` hand count 13/13 rows and authZ 0 widening; `click48.mjs` 60/60; `fail48.mjs` 0 tiles with the sentence on a whole failure.
- **I-2:** `RoleMatrixTests` and `PricingPolicyTests` green; the policy files sha-identical to base.
- **Leak + secret scan** over `git diff 0c74086...HEAD` and `git log --format=%B 0c74086..HEAD`, copies of `leak48.py` and its list builders. Counts only, each class with a planted control that fired. Never print the avoid list. Classify the commit author line **from commit metadata alone, as B48 did (`:332`)**.
- **No frozen change:** `git diff --numstat 0c74086 -- <frozen list above>` is empty.
- Evidence goes in `Briefs/2026-10-12_B49_evidence/` (folder 0700, files 0600). Tools and logs go in `.tools/qa-B49/` (0700).

## FOUND / TESTED / HOW / NOT TESTED
For each row, a four-line block in STATUS: **FOUND** at base, citing `file:line`; **TESTED** (file and test name, red-first counts); **HOW** (instrument and ratios); **NOT TESTED** (what is left, and why).

## STATUS sections
- BLUF, one line per row (DONE / NOT DONE);
- PRIOR-WORK CHECK (every cite re-read at base, which moved, and the B48 line-count diff);
- Base read (step 0 pins, verbatim);
- Commits;
- Test Evidence (the base vs head table, including the full Playwright suite in both modes);
- Red-proof table;
- Tier-1 conditions;
- FOUND / TESTED / HOW / NOT TESTED, per row;
- Fix shape chosen per row (the ruling's, or another, and why), including Row 2's href and Row 8's clock;
- Modified pre-existing tests (before → after, and why);
- NEW WORDS (verbatim);
- UNMEASURED;
- `## NOT DONE / NOT COVERED`, as prominent as the evidence;
- `## For the records seat` (NOT YOURS rows, and any NOT DONE row);
- needs-Friday (Jira draft lines only; Jira writes are Friday's);
- Leak + secret scan;
- processes started and stopped;
- worktrees and files left;
- Push (the command and the read-back, verbatim).

## Time-box
**About 2 h.** If you run short, finish in this order: **Row 1 (G-F1)** with Row 7's Seller+Approver guard, Row 7's other two guards, Row 2, Row 3, Row 8, Row 6, Row 5, Row 4. List what is left as **NOT DONE**, never half-built. Remember there is no round 3.

## UNMEASURED (by the draft writer, each with its closing instrument)
- Suite counts at `0c74086` on this run: closes with your base run.
- Whether the stub's synthetic rows give the analyst ≥ 1 approvable quote (`stubApi.ts:109-123`, `:166`): closes with your Row 1 browser test at base.
- Whether `ceil` against the figures' `asOf` passes every follow-up row in the gate's aged store (B48 `:87`): closes with your Row 8 vitest and a live read of the aged copy.
- CodeQL and CI for your head: Friday reads them on the PR. CI does not run Playwright (B48 `:236`, `:311`).
- Ports 6640–6649 at firing: free at 16:44 AEDT. Re-check with `lsof` before every bind.

## HOLDS
- Datasec only. No other client's names, tickets or paths.
- **CodeQL policy:** push your branch only; never push to main; never dismiss an alert; never ask for a bypass. **Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main.**
- **No deploy, no PR, no Jira write, no `history.md`** (Friday's records seat does those). No Azure write, no setting change, nothing sent to any human, no hosted read.
  - **P-1 HOLD** (records `BACKLOG.md` `## Holds on the hosted site`, B39): before any hosted deploy, the hosted repeated-`lineNumber` count first. This round deploys nothing and does not run P-1.
- **Never open `4_Credentials/.env`.** Not for the leak scan either (see Test Evidence).
- **Q-09:** synthetic price sets and synthetic quote stores only; never a real price book. **SITE HOLD:** none of the four store path settings changes.
- No pricing rule change. No price, total or applied percent moves on any fixture.
- **No real client data anywhere** (code, tests, fixtures, screenshots, commit messages, STATUS). Counts only.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-12_B49_<what>/` (0700), and say so. **Never edit a running script;** write a new file instead.
- **Own worktree and own ports.**
  - Allowed: `fetch`, `worktree add`, and commits and one push on `b49/gate-b48-fix-round`.
  - Never `checkout` or `switch` in `2_Project_Files` or the project root. **Never `gc`, `prune`, `reset`, `worktree remove`, `branch -D` or force-push.** Never push to `b46/…`.
  - Other seats' worktrees and QA folders (`wt-B46*`, `wt-B47*`, `wt-B48*`, `qa-B46/`, `qa-B48/`) are read-only. Copy from them.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY, and read back `lsof -nP -iTCP:6640-6649 -sTCP:LISTEN` → 0. `caffeinate`, the shared `VBCSCompiler` and any listener outside 6640–6649 are not yours.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`. Build with `UseSharedCompilation=false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero needs a positive control that fired.
- **Writes:** only your STATUS, your evidence folder, `.tools/qa-B49/`, your worktrees, and your branch.

## End
The last line of `Briefs/2026-10-12_B49_STATUS.md` is exactly one of these:
- `READY FOR GATE: b49/gate-b48-fix-round <sha>`, where `<sha>` is the full SHA read back by `git ls-remote origin refs/heads/b49/gate-b48-fix-round` in the same action as the push (one push, of this branch only);
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.
