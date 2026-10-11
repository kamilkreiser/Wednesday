From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to friday-laptop-agent@agentmail.to. This project has no mail key, so your STATUS file is your wrap.
# BRIEF B37 · SEAT-B: FIX ROUND for gate B36 (K-1, K-2, K-3, K-4, K-5, K-7) on MPS main
**Written:** @NOW@ AEDT 2026-10-11. This is a draft. Friday sets the time when he fires it. **Pane:** `Datasec/MPS-B`. Your commission is the newest file in `Briefs/` whose name contains `_SEAT-B_`.
(The draft writer checked the launcher. `Launch_Claude.command:107` takes the seat letter from a pane name that matches `*MPS*-?`. Line `:111` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". At drafting, the newest `_SEAT-B_` file was `2026-10-11_B30_SEAT-B_card-defaults-accessory-markup-newquote.md`. This file replaces it. `tmux list-panes -a`: 0 MPS pane titles.)
**Seat:** Seat B, a Claude build seat. One branch, red-first. **QA tier 1** throughout.
**Round:** FIX ROUND. This is **round 2 of 2** under the two-NO-GO cap, so the next gate is a **deltas gate**. Close each row completely, or list it as NOT DONE. Never leave a row half-done.
**Report:** `1_Project_Definition/Briefs/2026-10-11_B37_STATUS.md`. Its **last line** is exactly one of these:
- `READY FOR GATE: b37/gate-b36-fix-round <sha>`, where `<sha>` is the full 40-hex SHA read back by `git ls-remote origin refs/heads/b37/gate-b36-fix-round` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.

## AUTHORITY
- **Gate B36** (`Briefs/2026-10-11_B36_STATUS.md`, Seat E, round 1) gave verdict `B35 08c5f43: GO WITH NOTES`, `overall: GO WITH NOTES`. It found 0 Blocker, 0 Major, six Minors (K-1 to K-5 and K-7) and one Note (K-6). Its words: *"Friday decides what reopens."*
- **Friday reopens the six Minors: K-1, K-2, K-3, K-4, K-5 and K-7.** Do not fix K-6 or the Notes N-1 to N-10 this round. Record them (see RECORDS).
- B35's work merged as **PR #25** (squash), so it is now MPS main. This round fixes main, not the `b35/…` branch.
- These stand unchanged: C-12 (no self-approval; only the owner edits), the I-2 price-edit matrix (C-13), and Q-16 (MPSCALC-82, retention: still the default; build nothing that deletes).
- **The fix shapes below are the gate's, not Friday's.** Every row marks them *"the gate proposes; verify before building"*. If you build something else, say why in STATUS.

## READ WHOLE FIRST
- The project `CLAUDE.md`, `1_Project_Definition/CLARIFICATIONS.md` (on records `main`, `76d735c`; it holds C-14…C-21 since B34) and `Questions_and_Answers/00_QUESTIONS_FOR_KAM.md`.
- **`Briefs/2026-10-11_B36_STATUS.md` in full.** Read each of `## Findings` K-1 to K-7, Item 4 (rental), Item 5 (export history), Item 6 (registry), Item 8 (mutants) and Item 10 (NEW WORDS). Read its evidence in `Briefs/2026-10-11_B36_evidence/`: `04_scale_dev.json`, `04_rental_*.json`, `05_export_*.json`.
- `Briefs/2026-10-11_B35_SEAT-A_api-quote-lifecycle-and-audit.md` and `2026-10-11_B35_STATUS.md`, to see what was built and why.
- The gate's instruments, **read-only. Copy them; never run them in place:** `.tools/qa-B36/tools/mut36.py` (the exact texts of mutants E-04 at `:32-33` and M4 at `:53-55`), `probe_export.py`, `probe_rental.py`, `probe_scale.py`, `probe_nested.py`, `words36cs.py` and `newwords36.py`.

## Base and branch
- **Base: MPS main = `6c0ba857501f6568800b060d0b084950f885c9d1`.**
  - The draft writer read it at ~19:3x AEDT with `git -C 2_Project_Files ls-remote origin refs/heads/main`, which printed `6c0ba857501f6568800b060d0b084950f885c9d1 refs/heads/main`.
  - It was confirmed in a `git clone --shared` scratch copy after `fetch origin main`. `log -1 --format='%H %T %P %s'` printed tree `03007e3e974b705cccaf5c2e1544a278fe668664`, the single parent `db8edfd5082e49f9a1a1b3c23feeb02b36834b21`, and the subject "B35: quote duplicate, lifecycle events, rental override audit, export history, field registry (MPS lane A1) (#25)".
  - This agrees with Friday's API read (`6c0ba85`, tree `03007e3e`).
  - **The tree is the same as `08c5f43` (B35's head, the tree gate B36 measured).** So every `file:line` in B36 holds at this base. `08c5f43` is **not** an ancestor of main, because the merge was a squash. Do not base on the `b35/…` branch.
  - Your local `origin/main` is still `db8edfd` (`rev-parse origin/main`). Fetch first.
- **First action:** run `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/main`.
  - If it prints `6c0ba85…`, proceed.
  - If it prints a descendant of `6c0ba85`, list `git diff --name-only 6c0ba85 <main>`. If that list touches any path in your write set, **STOP: NEEDS FRIDAY**. Otherwise base on the new main and say so.
  - If it prints anything else, **STOP: NEEDS FRIDAY**. Never rebase on your own.
- Branch `b37/gate-b36-fix-round`, in a fresh worktree `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B37'` (`chmod 700`). Take base measures in `.tools/wt-B37-base`, detached at your base.
- The draft writer read every `file:line` below at `6c0ba85` with `git show 6c0ba85:<path>`, in the scratch clone. Re-check each one at your base before you edit, and list any that moved.
- **Push your branch only.** Friday opens the PR. He merges once CodeQL and the checks are green. The Datasec org requires CodeQL. Never push to main.

## Ports
**6900–6909** (API 6900, web 6903 by default).
- The draft writer checked at 19:35 AEDT:
  - `grep -rhoE '\b69[0-9]{2}\b' Briefs/` gives **0** hits, against a control of `\b66[0-9]{2}\b` with 116 hits.
  - No 2026-10-10 or 2026-10-11 brief or STATUS names a port in 6900–6999. The ones taken: B28/B30 6280/6283; B29 6470–6479; B30 6590–6599; B32 6600–6609; B34 6640–6649; B35 6620–6629; B36 6750–6789 and 6800–6854.
  - `lsof -nP -iTCP:6900-6909 -sTCP:LISTEN` gives 0 listeners.
- **Live listeners that are not yours, as of 19:35:** 6755, 6756, 6860–6868 (docker, node, dotnet). Never touch them.
- Check that your ports are free before you bind. Never use 5080/5173 or any port named in an earlier brief or STATUS. Playwright and run-demo find your ports through env. Never edit a shared config default.

## Write set
- `src/MpsCalc.Api/Quotes/{QuoteEndpoints,PriceAudit,QuoteEvents,Proposal,ExportFieldRegistry}.cs`;
- `src/MpsCalc.Api/Quotes/QuoteFileStore.cs` and `QuoteStore.cs`: **only** for a test seam that changes no production behaviour (K-1). The precedent is `CatalogueOverlayStore.BeforeRename`, at `Inventory/CatalogueOverlayStore.cs:119`, used by `OverlayGateFindingsTests.cs:238`. `QuoteFileStore.Write` already takes `beforeRename` (`QuoteFileStore.cs:300`, `:316`), but `SaveQuote` passes none (`:284`). Name every line you add;
- `tests/MpsCalc.Api.Tests/**`, new and existing files. List every modified pre-existing test in STATUS, before → after, with the reason;
- `docs/API.md` and `docs/api/openapi.json`, only where a fix changes documented behaviour (K-1, and K-3 if you choose the 400);
- `web/src/api/generated/**`, regenerated **only** by `web/scripts/sync-contract.mjs`, as its own `contract:` commit, never by hand.

**Frozen:**
- `src/MpsCalc.Api/Contracts/Dtos.cs`. K-5 needs no DTO change. If you find you need one: **STOP: NEEDS FRIDAY**;
- `src/MpsCalc.Api/Program.cs`;
- `src/MpsCalc.Engine/**`, `src/MpsCalc.Import/**`, `src/MpsCalc.Api/Inventory/**`, `src/MpsCalc.Api/Sources/**`;
- `web/src/**`, except `generated/**`;
- `infra/**`, `scripts/**`, `.github/**`, the root build files.

If origin carries another seat's open branch that is newer than your base and touches your write set: **STOP: NEEDS FRIDAY**. At drafting, `ls-remote` listed no branch newer than `b35/api-quote-lifecycle-audit` (`08c5f43`).

## Tier 1 (all rows)
- **Red proof, one conjunct at a time.** Every row's test is red where the row says so, green at your head, and red again when the fix is tampered back. Restore by sha256, then touch and build `--no-incremental`.
- **The I-2 matrix is byte-for-byte unchanged:** `git diff <base> -- web/src/auth/pricePolicy.ts src/MpsCalc.Api/Quotes/PricingPolicy.cs` is empty, and `RoleMatrixTests` and `PricingPolicyTests` are green.
- **The proposal output is byte-for-byte unchanged** on every existing proposal fixture. Serialise before and after. B36 measured 48/48 bodies and 17/17 calculations at this tree.
- No price, total or applied percent moves on any fixture.
- **Never normalise a stored draft** (K-2): the draft round-trip and the proposal must not change.
- No internal value is ever derived in the browser.
- A Seller without internal metrics sees no new field.
- Every new or reclassified field is in `ProposalAllowList.Sources`.

## PRIOR-WORK CHECK (record before you change anything)
- The **suites at this tree** were measured by B36 at `08c5f43`, which has the same tree:
  - .NET **934/934** (235 + 72 + 627), Release with 0 warnings, 0 vulnerable packages;
  - web **325/325** (50 files).
  - Re-measure both at your base. Do not trust these numbers.
- **The proposal GET writes:** `QuoteEndpoints.cs:598-607` (B35 item 5). `Generated` calls `QuoteEvents.Record` at `:603`, then `store.Save(q)` at `:605`. `QuoteEvents.Record` appends to `q.Events` at `QuoteEvents.cs:38`, with `sequence = q.Events.Count + 1` at `:36`.
- **Other writers record the event before saving too.** For example, PATCH records at `QuoteEndpoints.cs:180` and saves at `:181`. That is the **pre-existing B08A2-1 limit** (state in memory ahead of disk), and **it is not in this round**. K-1 is only about `proposal-generated`.
- **The rental audit:** `PriceAudit.RentalOverrides` is at `PriceAudit.cs:74-97`. It is called by create (`QuoteEndpoints.cs:84`), PATCH (`:172-176`) and duplicate (`:505`). The purchase `Diff` (`PriceAudit.cs:43-47`) shares `D` (`:123`) and `Keys` (`:120-121`).
- **The engine already blocks duplicated fleet numbers.** `QuoteCalculator.cs:170-172` raises `INVALID FLEET LINE NUMBER`, and `FleetRuleTests.cs:289` pins it. That code is frozen. `Validate` (`QuoteEndpoints.cs:929-956`) does not check uniqueness. It runs on create (`:68`), PATCH (`:119`) and **duplicate** (`:490`).
- **The test clock:** `TestClock` is at `Infrastructure/ApiHost.cs:16-21`, exposed as `_host.Clock` (`:77`). Some tests advance it (for example `QuoteApiTests.ExportHistory.cs:23`), but the concurrency test at `:80-104` does not.
- **The field guards:** `QuoteApiTests.Showcase.cs:488` (`Every_field_of_every_proposal_source_type_is_classified`), `:502` (`Every_proposal_output_field_is_on_the_allow_list_and_none_is_internal`), and `QuoteApiTests.ExportRegistry.cs:18` (`Registry_classifies_every_field_of_every_export_source_type_and_nothing_else`). All three walk only `ProposalAllowList.SourceTypes` (`Proposal.cs:35-46`).

## ROWS (one commit per row, red test first; any contract sync is its own commit)

### Row K-1 · Minor · failed proposal GET leaves a durable event (MPSCALC-49, API half)
- **Finding, verbatim (B36):** *"K-1 · Minor · a failed (500) proposal GET leaves a `proposal-generated` event that the next save makes durable"*. FOUND: *"the event is appended to the in-memory list before the save. If the save throws, the request answers 500 and no proposal is served, but the event stays in memory and is written by the quote's next successful save."*
- **Oracle (B36's FAIL condition):** *"a call that does not succeed records an event"*. Measured by the gate: `chmod 500` on `quotes/`, then one GET on an Approved quote → 500; memory held 9 events and disk 8; after one more successful GET, disk held **10**, *"including the one from the 500"*. Both modes.
- **Lines at base:**
  ```
  601	            IResult Generated(ProposalDto proposal, int revision, string? calculationId, string? snapshotId)
  602	            {
  603	                QuoteEvents.Record(q, QuoteEvents.ProposalGenerated, clock.GetUtcNow(), caller, proposal.VersionNumber, revision,
  604	                    calculationId: calculationId, snapshotId: snapshotId, isDraft: proposal.IsDraft);
  605	                store.Save(q);
  606	                return Results.Json(proposal, ApiJson.Options);
  ```
  (`src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`). The append is at `QuoteEvents.cs:38` `q.Events.Add(e);`.
- **Fix shape. The gate proposes; verify before building:** *"append the event only after the save succeeds (or remove it again in a `catch` around the save, under the same lock), so a failed generation records nothing anywhere."*
  - The draft writer's caution, which you must verify: if you append *after* the save, the event is not in the file that was saved. The catch-and-remove shape keeps one save. Prove that the sequence stays contiguous after a removal.
  - Fix only this writer. Do not change the other writers (B08A2-1).
- **Red-first cell:**
  - **Test:** a store whose quote write fails once (seam per the write set; `chmod` is fragile on CI `ubuntu-latest`, `ci.yml:32`, and when run as root). Then:
    - the GET answers 500;
    - the quote's events are unchanged **in memory** (read back through a GET by an internal-metrics caller) **and on disk** (a restart read-back as in `QuotePersistenceTests`);
    - the next successful GET adds exactly one event, and the sequence stays contiguous.
  - **RED at base** (the memory/disk count is +1).
  - **GREEN at head.**
  - **Tampered back RED:** move the `Record` back in front of `Save` with no removal.
- **Docs:** `docs/API.md:351-357` says *"A refused call (403, 404, 409) records nothing."* Add the 500 case if the words change. Any changed line goes in NEW WORDS.

### Row K-2 · Minor · a rental override re-sent with another decimal scale is audited as a change (MPSCALC-33, API half)
- **Finding, verbatim:** *"K-2 · Minor · a rental override re-sent with another decimal scale is audited as a change"*. FOUND: *"values are compared as text, and `System.Decimal` keeps its scale, so `50` and `50.00`, or `0.1` and `0.10`, differ."*
- **Oracle:** *"a spurious entry on an unchanged field"*.
  - The gate's case: a rental quote with `baseChargeOverride 50` and `monoClickOverride 0.1`, then PATCH with `"50.00"` and `"0.10"`. The gate got *"2 entries per save, expected 0"*, and 2 more on the way back.
  - The same happens with a JSON number. The UI sends the typed text (`web/src/screens/FleetGrid.tsx:128`, `onChange={(e) => set(f.lineNumber, { [k]: e.target.value })}`).
  - Evidence: `B36_evidence/04_scale_dev.json`.
- **Lines at base** (`src/MpsCalc.Api/Quotes/PriceAudit.cs`):
  ```
  78	        void Add(string field, string? o, string? n)
  79	        {
  80	            if (!string.Equals(o, n, StringComparison.Ordinal))
  ...
  92	            Add($"fleet[{n}].baseChargeOverride", D(o?.BaseChargeOverride), D(x?.BaseChargeOverride));
  93	            Add($"fleet[{n}].monoClickOverride", D(o?.MonoClickOverride), D(x?.MonoClickOverride));
  94	            Add($"fleet[{n}].colourClickOverride", D(o?.ColourClickOverride), D(x?.ColourClickOverride));
  ...
  123	    private static string? D(decimal? d) => d?.ToString(CultureInfo.InvariantCulture);
  ```
- **Fix shape. The gate proposes; verify before building:** *"compare the decimals numerically (`o == n`) before formatting, and record the normalised value; or normalise the scale once when the draft is stored."*
  - **The second option is ruled out by Tier 1:** it changes the stored draft.
  - With the first option, **say what text an entry records** for a real change. Record what the caller sent, or a normalised value, and give the reason.
- **Scope limit:**
  - **Rental only.** The gate's note: *"The purchase `Diff` uses the same `D` and compact-JSON comparisons, so a purchase sell-override re-sent as `…10` would also count as a change and ask for a reason … by code reading … not measured."*
  - Changing the purchase side changes when `PRICE_REASON_REQUIRED` fires, so it is **not this round**. Do not change `D` itself, or `Diff`'s behaviour.
  - Prove the purchase side unchanged: the purchase and PriceAudit suites are green and unchanged in count. Record the purchase half in RECORDS.
- **Red-first cell:**
  - **Test:** for each of the four overrides (tier needs no scale case; say so), re-send the same value at another scale, both as a string and as a number. Expect **0** entries. A real change on the same save still gives one entry per field.
  - **RED at base:** 2 per save.
  - **GREEN at head.**
  - **Tampered back RED:** restore the ordinal text comparison.

### Row K-3 · Minor · an override change on a second fleet line with a duplicated `lineNumber` is not audited (MPSCALC-33, API half)
- **Finding, verbatim:** *"K-3 · Minor · an override change on a second fleet line with a duplicated `lineNumber` is not audited"*. FOUND: *"two fleet lines may share a `lineNumber`; the PATCH is accepted. The audit looks at the first line with that number only."*
- **Oracle:** *"a missing entry"*.
  - The gate made line 2's number 1 (200), then changed the second line-1's `monoClickOverride`. It got *"0 entries, expected 1"*. The same change on the first line gives 1 entry.
  - The value is later recorded under the renumbering save, *"attributed to that save and its reason, not to the one that made the change"*.
- **Lines at base** (`PriceAudit.cs`):
  ```
  86	        foreach (var n in Keys(before?.Fleet, after.Fleet, f => f.LineNumber.ToString(CultureInfo.InvariantCulture)))
  87	        {
  88	            int number = int.Parse(n, CultureInfo.InvariantCulture);
  89	            var o = before?.Fleet?.FirstOrDefault(f => f.LineNumber == number);
  90	            var x = after.Fleet?.FirstOrDefault(f => f.LineNumber == number);
  ```
  `Keys` (`:120-121`) is `.Distinct(StringComparer.Ordinal)`. `Validate` is at `QuoteEndpoints.cs:929-956`, with no uniqueness check.
- **Fix shape. The gate proposes; verify before building:** *"refuse a draft whose fleet `lineNumber`s are not unique at `Validate` (400, naming the field), or key the audit by position plus number."* Measure before you choose, and write down the choice and the reason:
  - (a) **If you choose the 400:** `Validate` also runs on **duplicate** (`:490`). A stored quote that already has duplicated numbers would then refuse to duplicate (400), and would refuse every PATCH until renumbered. Count such stored quotes in your synthetic roots, and measure whether any API, web or e2e test or fixture sends duplicated fleet numbers (`git grep`). The engine code and the 400 message go in NEW WORDS. The contract description changes, so a `contract:` commit follows.
  - (b) **If you choose position-keyed matching:** the gate's N-4 and E-06 show that index matching mis-attributes removals (*"3 entries, 1 expected"*). Prove that your keying does not regress the removal case: remove a middle line without renumbering, expect 1 entry.
- **Red-first cell:**
  - **Test:** two fleet lines with the same `lineNumber`, then change the second one's override. The result is either 400 with nothing recorded and the quote unchanged (shape a), or exactly 1 entry for that change (shape b).
  - **RED at base:** 200 and 0 entries.
  - **GREEN at head.**
  - **Tampered back RED:** remove the uniqueness check (a), or restore `FirstOrDefault` (b).

### Row K-4 · Minor · the suite does not guard "a proposal GET leaves `updatedAt` unchanged" (MPSCALC-49), a surviving mutant
- **Finding, verbatim:** *"K-4 · Minor · the suite does not guard "a proposal GET leaves `updatedAt` unchanged" (frozen test clock)"*. FOUND: *"the concurrency test asserts `updatedAt` is unchanged after 24 GETs, but the host's clock does not advance, so a GET that set `UpdatedAt = clock.GetUtcNow()` would write the same instant."*
- **Oracle:** the tier-1 class *"a proposal GET that moves `updatedAt`"*.
  - The gate's mutant **E-04** (the GET sets `q.Current.UpdatedAt`, `mut36.py:32-33`): *"GREEN 934/934"* on the suite, and *"RED, 10 FAILs"* on the gate's real-clock probe (`updatedAt` moved on 9/9 GETs, and the list order moved).
  - **The code at base is correct. Only the guard is blind.**
- **Lines at base:**
  ```
  98	        Assert.Equal(open.GetProperty("updatedAt").GetDateTimeOffset(), after.GetProperty("updatedAt").GetDateTimeOffset());
  ```
  (`tests/MpsCalc.Api.Tests/QuoteApiTests.ExportHistory.cs`). The clock: `Infrastructure/ApiHost.cs:16` `internal sealed class TestClock(DateTimeOffset now) : TimeProvider`, `:77` `public TestClock Clock { get; } = new(...)`.
- **Fix shape. The gate proposes; verify before building:** *"advance `_host.Clock.Now` between the open read and the proposal GETs (and in the restart test), then assert `updatedAt` and the list order; add E-04 to the red-proof table."*
- **Red-first cell (a test gap, so the cell kills the mutant):**
  - **The test must kill E-04.** Apply E-04's exact text from `mut36.py:32-33`, copied, on your head: the new assertions go **RED**. Name the tests that turn red and give the count `RED n/m`.
  - **GREEN at base and at head without the mutant.** This is expected, because the code is right. Say so; it is not a failure of red-first.
  - **Tampered back RED:** remove the clock advance, and E-04 survives (green) again. Show that too.
  - Also assert that the **quote list order** is unchanged (`GET /quotes`), as the gate's probe did.

### Row K-5 · Minor · the export-field guards do not see a nested DTO type the projection reads (MPSCALC-47), a surviving mutant
- **Finding, verbatim:** *"K-5 · Minor · the export-field guards do not see a nested DTO type the projection reads"*. FOUND: *"the classification guards walk only the types listed in `SourceTypes`. A property whose type is a new DTO is classified as a whole; the nested type's own fields are never enumerated."*
- **Oracle:** the class *"unregistered field to a customer output"*.
  - The gate's mutant **M4** (`mut36.py:53-55`) adds `GateNestedDto(string? Text)` under `FleetLineDto.GateNested`, classified `N`, and has `Copy` read `GateNested.Text` into `Site`.
  - Result: *"GREEN 934/934"*, and a plain Seller's marker *"reaches the customer proposal in 6/6 bodies"*.
  - *"At head no such type exists … nothing leaks today; the gap is for the next change."*
- **Lines at base** (`src/MpsCalc.Api/Quotes/Proposal.cs:35-46`, `SourceTypes`):
  ```
  35	    public static IReadOnlyList<Type> SourceTypes { get; } =
  36	    [
  37	        typeof(SnapshotDto), typeof(QuoteDraftDto), typeof(AssumptionsDto), typeof(FleetLineDto), typeof(CalculationDto), typeof(TaxDto),
  ...
  45	        typeof(QuoteEventDto),
  46	    ];
  ```
  The registry is built from `Sources` at `ExportFieldRegistry.cs:118-120` (`var fields = ProposalAllowList.Sources.ToDictionary(...)`). The guard is at `QuoteApiTests.Showcase.cs:488-499`.
- **Fix shape. The gate proposes; verify before building:** *"make the guard transitive: from each source type, walk property types (and element types of lists) and require every reachable DTO type to be in `SourceTypes`; or generate `Copy`'s reads from `Bindings()`."*
- **The draft writer's measure:** by reading `Contracts/Dtos.cs` at base. **UNKNOWN exact count; your new guard run at base lists them, and that closes it.** A transitive walk is **red at base before any mutant**. At least these record types are reachable from the listed types but not in `SourceTypes`: `ServiceCostsDto` (`Dtos.cs:9`, via `AssumptionsDto.ServiceCosts` `:34`), `HardwareLineDto`, `SoftwareLineDto`, `PurchaseSectionDto`, `PurchaseBomLineDto`, `ManualItemDto`, `ClickRateDto` (and its `SuppliesDto`, `:613`), `SourceVersionDto`, `IssueDto`, `PoolDto`, `QuoteAuditEntryDto`, `SourcePriceDto`, `SuppliesResultDto` (`:719`). Enums (`QuoteModeDto`, `ItemClassDto`, …) are not DTO records. Say how your walk treats them.
  - **If you close the gap by listing those types**, classify every new field **`NotShown` (→ INTERNAL_ONLY, fail closed)**, unless it is already bound by `Proposal.Bindings()` (none are, per B36 item 6). Put the full classification table in STATUS for the gate: a classification is a reviewed judgment (N-8). The proposal stays byte-equal.
  - An **exemption list** in the guard reopens the hole for any type on it. If you need one, **STOP: NEEDS FRIDAY**.
- **Red-first cell (a test gap, so the cell kills the mutant):**
  - **RED at base:** the new transitive guard lists the reachable unlisted types.
  - **GREEN at head.**
  - **The test must kill M4.** Apply M4's exact texts from `mut36.py:53-55`, copied, on your head: the guard goes **RED** and names `GateNestedDto`.
  - **Tampered back RED:** make the walk non-transitive again, and M4 survives (green). Show that.
  - Re-run M1 (`mut36.py`, an unclassified property on `FleetLineDto`): it must stay RED.

### Row K-7 · Minor · NEW WORDS not verbatim (the process finding, carried into this round)
- **Finding, verbatim:** *"K-7 · Minor · B35's NEW WORDS table is not verbatim for the contract and API.md text"*. FOUND: *"For the contract and API.md it has one generic row … **31 OpenAPI strings added and 4 pre-existing descriptions changed** … and **70 API.md lines added, 3 removed**. They are API-visible and were not shown old → new."* HOW: *"none for the code; Friday shows Kam the verbatim list"*. B36 has already written B35's list verbatim (B36 Item 10). **Do not redo B35's words.**
- **Oracle (B36 item 10):** *"undeclared API-visible word (Minor); a word from the example (Blocker)"*.
- **What this row asks of you:**
  - **Your own `## NEW WORDS` section is verbatim and complete, with no generic row.** It covers every user-visible or API-visible string this round adds or changes: problem `code`s and messages (such as a K-3 400), the OpenAPI `summary`, `description` and `enum` strings, the added and removed lines of `docs/API.md`, and any audit `reason` text. Each one shows old → new, with `file:line` (or JSON path) at your head.
  - **Kam sees this list before any deploy. Nothing is deployed this round.** A hosted MPS deploy needs Kam's card.
- **Mechanical cell** (instead of a red test):
  - Run a copy of `words36cs.py` and `newwords36.py` over `<base>...<head>`, giving counts per class.
  - Every string the script finds appears in your NEW WORDS (count = count), and **0** rows are generic.
  - **Positive control:** plant one undeclared string in a scratch copy. The comparison must flag it. Report that it fired.
  - Scan the new words against the example-document sentence list, using copies of the B36 list tools, counts only: **0 hits**, with a control that fired.

## Test Evidence (run each command as `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head, in `wt-B37-base` and `wt-B37`:**
  - .NET: the full suite, a Release build `--no-incremental` with **0 warnings**, and `dotnet list package --vulnerable --include-transitive` with 0 vulnerable packages;
  - web: `npm ci`, `lint`, `typecheck`, the full `test` suite and `build`.
  - **Reconcile every count change:** new tests by name, and modified pre-existing tests before → after.
- **Contract:** only if K-1 or K-3 changes `openapi.json`. Run `sync-contract.mjs` once and commit the result as its own `contract:` commit. `web/src/api/contract.test.ts` must be green. The `generated/**` diff must be exactly the changed descriptions plus the SOURCE header.
- **Red-proof table, one line per conjunct:** the term, the tamper, `RED n/m` on the full suite, and the sha256 restore.
  - It includes **E-04** (K-4) and **M4** (K-5) applied by exact text, and the tampered-back fix for every row.
  - **Re-run B36's ten sampled B35 tampers** (B36 Item 8 table, B35-01 … B35-20). Each must still be RED, with the count reconciled against B36's.
  - Re-run **E-06**, **M1** and **C1** as well. E-06 is green at base (N-10). Report it, do not fix it, unless your K-3 shape (b) makes it go red. Say which.
- **Probes:** copy `probe_export.py`, `probe_rental.py` and `probe_scale.py` into `.tools/qa-B37/` and run them against your head API on your ports, both modes (DevStub and Entra-fake, as B36 did). Use synthetic stores only.
  - K-1: the read-only-directory path now leaves memory = disk, and no phantom event.
  - K-2: 0 entries on a scale change.
  - K-3: your chosen shape.
- **Proposal byte-equality:** base vs head across the same 16-quote × 3-reader shape as B36 (`probe_parity.py`, copied).
- **I-2:** `RoleMatrixTests` and `PricingPolicyTests` green, and the policy files sha-identical to base.
- **Playwright** (stub and live, synthetic data only; mask money cells): no screen changes, so run the full suites to prove that nothing user-visible moved. The `smoke.spec.ts:36` timeout is pre-existing (B36 N-7). Report it; it is not yours.
- **Leak + secret scan** over `git diff <base>...HEAD` and `git log --format=%B <base>..HEAD`, using copies of B36's `leak36.py` and its list builders. Counts only, every class with a planted control that fired. Never print the avoid list.
- **No frozen change:** `git diff --numstat <base> -- infra scripts .github src/MpsCalc.Engine src/MpsCalc.Import src/MpsCalc.Api/Inventory src/MpsCalc.Api/Sources src/MpsCalc.Api/Program.cs src/MpsCalc.Api/Contracts/Dtos.cs web/src/auth/pricePolicy.ts src/MpsCalc.Api/Quotes/PricingPolicy.cs` is empty.
- Evidence goes in `Briefs/2026-10-11_B37_evidence/` (folder 0700, files 0600). Tools and logs go in `.tools/qa-B37/` (0700).

## RECORDS (route: a LOCAL `records/b37` branch, commit only)
- **The draft writer measured the records repo (the project root), read-only:**
  - `git remote -v` printed **0 lines**: no remote, so nothing is pushed.
  - `git ls-tree main --name-only` lists `BACKLOG.md` (1 hit).
  - Records `main` = `76d735c086715167a9b15f7a1a401fa150f66f57` ("Records: fold records/b12, b21, b25, b30, b34 into main (B34)"). `rev-list --left-right --count main...records/b34` = `2 0`, and `main...records/b30` = `3 0`, so both are folded.
  - The root worktree holds untracked `Briefs/` files (`status --short`).
- **Steps:**
  - `git -C '<project root>' worktree add .tools/wt-B37-records -b records/b37 main`, then `chmod 700`. Commit here only.
  - Never `checkout`, `switch`, `stash`, `merge` or `reset` in the root worktree. Never fold into `main`. That is Friday's.
- **Add rows to `BACKLOG.md` under `## Deferred problems`,** in the existing row shape (Where / Symptom in the gate's words, quoted / Fix shape / Why deferred / Discovered), each with source and date. Use one commit, message `Records: gate B36 rows not fixed in B37 (B37)`. The rows:
  - `[B36-K6]` (Note, the API.md "refused" sentence on body-less routes);
  - `[B36-N4]` (renumbering after a middle-line removal records spurious entries);
  - `[B36-N10]` (no test removes a middle fleet line; E-06 survives), unless K-3 shape (b) kills it;
  - `[B36-K2-purchase]` (the purchase half of K-2, not measured);
  - one row per K-row you leave NOT DONE.
  - **Do not** record needs-Friday 1–3 (B36 Item 9). They are rulings for Friday, not deferred problems.
- `CLAUDE.md`, `JIRA.md`, `history.md` and Jira are Friday's. Write none of them.

## FOUND / TESTED / HOW / NOT TESTED
For each row, write a four-line block in STATUS:
- **FOUND:** what you found at base, citing `file:line`;
- **TESTED:** the tests that pin the fix (file and name), with red-first counts;
- **HOW:** the instrument (suite, tamper, mutant, probe or read-back), with ratios;
- **NOT TESTED:** what is left, and why.

## STATUS sections
- BLUF, with a one-line verdict per row;
- PRIOR-WORK CHECK (every cite above re-read at base, and which moved);
- Commits;
- Test Evidence;
- Red-proof table (with E-04, M4 and the B35 resample);
- Tier-1 conditions;
- FOUND / TESTED / HOW / NOT TESTED, per row;
- Fix shape chosen per row: the gate's or another, and why;
- Modified pre-existing tests (before → after, and why);
- K-5 classification table (if you listed types);
- NEW WORDS (K-7, verbatim);
- UNMEASURED;
- `## NOT DONE / NOT COVERED`, as prominent as the evidence;
- RECORDS: the `records/b37` SHA, its rows, and `git log -1`;
- needs-Friday. Jira comments are Friday's, so give him one draft line per ticket: MPSCALC-33, -47, -49, "advances, not Done";
- Leak + secret scan;
- processes started and stopped;
- worktrees and files left.

## Time-box
**About 2 h.** If you run short, finish in this order: K-4 (smallest; the kill of a tier-1 Blocker class), K-1, K-2, K-3, K-5 (widest), with K-7 alongside each one. List what is left as **NOT DONE**, never half-merged.

## UNMEASURED (by the draft writer, each with its closing instrument)
- **The exact list of DTO types the K-5 walk will find:** UNKNOWN, because it was read by eye from `Dtos.cs`, not run. The instrument that closes it: your guard, run at base.
- **Whether a write-failure seam exists for quote saves:** `SaveQuote` passes no `beforeRename` (`QuoteFileStore.cs:284`). UNKNOWN whether a non-seam route (directory mode) is reliable on CI. The instrument that closes it: your K-1 test, green on your machine and in CI (Friday reads CI).
- **Whether any stored synthetic quote, test or fixture carries duplicated fleet numbers** (K-3 shape a): UNKNOWN. The instrument that closes it: `git grep` and a scan of your roots.
- **The suite counts at `6c0ba85`:** B36 measured them at the same tree (`08c5f43`) but not at this commit. The instrument that closes it: your base run.
- **CodeQL and CI on the merged PR #25:** the draft writer cannot see them (no `gh`). Friday reads them.
- **Ports 6900–6909 at firing:** free at 19:35. Re-check them with `lsof` before you bind.

## HOLDS
- Datasec only. No other client's names, tickets or paths.
- **CodeQL policy:**
  - push your branch only;
  - never push to main;
  - never dismiss an alert;
  - never ask for a bypass.
  Friday opens the PR and merges after CodeQL and the checks are green.
- No deploy, no Azure write, no setting change, nothing sent to any human. A hosted deploy needs Kam's card.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-11_B37_<what>/` (0700), and say so.
- **Never edit a running script.** B36 did (its incident 1). Write a new file instead.
- **SITE HOLD (BACKLOG § Holds):**
  - none of the four store path settings changes;
  - `ReferenceStorePath` stays a regular file.
- No pricing rule change. No price, total or applied percent moves on any fixture.
- **No real client data anywhere.** The price books and the example quote are CONFIDENTIAL: report counts only. Price-book values never leave `.local/pricebooks/`.
- **Own worktree and own ports.**
  - Allowed: `fetch`, `worktree add`, and commits and pushes on your own branch. On records, commits on `records/b37` only, with no push (there is no remote).
  - Never `checkout` or `switch` in `2_Project_Files` or in the project root.
  - **Never `gc`, `prune`, `reset`, `worktree remove`, `branch -D` or force-push.** Never touch another seat's worktree: `wt-B35*`, `wt-B36*`, `wt-B3?-records`, `qa-B35/`, `qa-B36/` are read-only. Copy from them.
  - No merge, no Jira write.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate`, the shared `VBCSCompiler` and the listeners on 6755/6756/6860–6868 are not yours.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`. Build with `UseSharedCompilation=false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero needs a positive control that fired.
- **Records:** write only your STATUS, your evidence folder, `.tools/qa-B37/`, your worktrees, and `records/b37` (RECORDS).

## End
The last line of `Briefs/2026-10-11_B37_STATUS.md` is exactly one of these:
- `READY FOR GATE: b37/gate-b36-fix-round <sha>`, where `<sha>` is the full SHA read back by `git ls-remote origin refs/heads/b37/gate-b36-fix-round` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.
