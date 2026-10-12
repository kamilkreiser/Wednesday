From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to friday-laptop-agent@agentmail.to. This project has no mail key, so your STATUS file is your wrap.
# BRIEF B53 · SEAT-D: source version store hardening: the gate-B43 residues (MPSCALC-90, -91, -92 and Q-4…Q-8), B42-L1, B42-L4 and the cross-process lock B40-R8
**Written:** @NOW@ AEDT 2026-10-12. This is a draft; Friday sets the time when he fires it. **Pane:** `Datasec/MPS-D`. Your commission is the newest file in `Briefs/` whose name contains `_SEAT-D_`.
(Launcher check: `Launch_Claude.command:107` takes the seat letter from a pane name that matches `*MPS*-?`. `:111` makes the commission "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". The launcher only states that rule in the prompt; it does not pick the file itself. At drafting (19:2x AEDT), the newest `_SEAT-D_` file was `2026-10-10_B26_SEAT-D_commercial-readiness-walkthrough.md`, found with `ls -t Briefs | grep -i _SEAT-D_`. Its ADDENDUM files `B15_SEAT-D_ADDENDUM-*` also contain `_SEAT-D_`. This file replaces them all.)
**Seat:** Seat D, a Claude build seat. One branch, red-first. **QA tier 1** throughout. Why tier 1: B43-Q5 is an information-leak class (exception text, stack frames and build paths in a response), and B40-R8 is the lock that guards which price set is Active.
**Round:** round 1 of a new lane, so the two-NO-GO cap starts fresh. Lane A2 (B40/B41/B42/B43) is closed. This lane takes the residues that its gate B43 ticketed.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B53_STATUS.md`. Its **last line** is exactly one of these:
- `READY FOR GATE: b53/source-store-hardening <sha>`, where `<sha>` is the full 40-hex SHA read back by `git ls-remote origin refs/heads/b53/source-store-hardening` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.

## AUTHORITY
- **Kam, terminal to Friday, 2026-10-12 ~18:4x AEDT, verbatim:** *"keep going and keep rolling out agents to work through all tickets and items for MPS Calculator, Security Controls creation tool and HPSM POC"*. This brief is the MPS share of that order. The other two projects are not yours.
- **Gate B43's ruling on lane A2**, verbatim (`B43_STATUS.md` BLUF, as quoted in records `BACKLOG.md`): *"No Blocker and no Major, so the closed rows ship once CodeQL is green. Each residue gets a ticket under the two-NO-GO cap."* The residues are recorded as MPSCALC-90, -91 and -92 (Jira Bugs, Low, related to MPSCALC-50), and as BACKLOG rows `[B43-Q1]`…`[B43-Q8]`, `[B42-L1]`, `[B42-L4]` and `[B40-R8]`.
- **The rule choices in this brief are Friday's defaults, not Kam's rulings** (Q-2 "what empty means", L-4 "refuse or keep last-wins"). Build the default and list each one in STATUS needs-Friday.

## PRIOR-WORK CHECK (do this first; report it in STATUS `## PRIOR WORK`)
Before any code, re-read each item below at base and record **still open / already closed / moved** with `file:line`. An item already closed at base is NOT rebuilt; say so.
- `src/MpsCalc.Api/Sources/SourceLifecycle.cs`: `:61` `_gate` (an in-process lock only), `:91` `AfterRegistryWrite`, `:137`, `:165` (`!hasRegistry && !IsEmptyStore`), `:249`/`:287`/`:339` `lock (_gate)`, `:410` the seam call, `:506-513` `ReadRegistry` (catch **excludes** `IOException`/`UnauthorizedAccessException`), `:538` `IsEmptyStore`, `:578`.
- `src/MpsCalc.Api/Sources/SourceDocumentChecks.cs`: `:117` `JsonException`, `:122`, `:127` and `:156` (the two catch-alls, `when (ex is not OutOfMemoryException)`).
- `src/MpsCalc.Api/Sources/SourceAdminEndpoints.cs`: `:17-23` (seven routes, each `.AddEndpointFilter(Backstop)`), `:28-40` (Backstop: `SOURCE_LIFECYCLE_FAILED`, logged by type name only), `:140`, `:188`, `:205-221` `ReadCapped`.
- Tests: `tests/MpsCalc.Api.Tests/SourceLifecycleTests.GateB41.cs:553-575` (the one backstop test, per Q-6).
- Read whole: `Briefs/2026-10-12_B43_STATUS.md` `### Q-1`, `### Q-2`, `### Q-3` and `## Notes` Q-4…Q-13; `B42_STATUS.md` (`:251`, `:288-291`, `:320`); `B41_STATUS.md` `## Notes` N-1, N-3, N-12; the records `BACKLOG.md` rows named above; the project `CLAUDE.md`; records-main `CLARIFICATIONS.md`; `docs/API.md` "Source lifecycle" (**read only**).
- Search for prior work on each item in any branch: `git log --all --oneline -i --grep='Q-1\|registry.json\|cross-process\|overlay.lock'`. List the hits and whether any are reusable (for example the overlay's B22 lock pattern in `Inventory/CatalogueOverlayStore.cs:344-367`, which you may **copy the shape of**, never edit).

## Base and branch
- **Base: MPS code main = `b28c95eb0f73ed0ce7ae410791feefc8b1a059ea`.** The draft writer read it at 19:1x AEDT with `git -C 2_Project_Files ls-remote origin` (`refs/heads/main`). It is PR #27 (lane A2 merged; tree `2826f027` = gated head `ab8fdf1`). The B43 line numbers above are at `ab8fdf1`, and the trees are equal, so they hold at base.
- **First action:** `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/main`.
  - It prints `b28c95eb…`: proceed.
  - It prints a descendant (B49's home dashboard or B47's feedback pill may land while you work): run `git diff --name-only b28c95eb <main> -- src/MpsCalc.Api/Sources tests/MpsCalc.Api.Tests/SourceLifecycleTests* tests/MpsCalc.Api.Tests/Infrastructure/SourceStores.cs`. If that prints anything, **STOP: NEEDS FRIDAY**. If it prints nothing, stay on `b28c95eb` and say so. Never rebase on your own.
  - It prints anything else: **STOP: NEEDS FRIDAY**.
- Branch **`b53/source-store-hardening`** in a fresh worktree `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B53'` (`chmod 700`). Base measures go in `.tools/wt-B53-base`, detached at base. `ls-remote origin 'refs/heads/b53*'` printed 0 lines at drafting.
- **Push your branch only, and read it back** (`git ls-remote origin refs/heads/b53/source-store-hardening` = your HEAD). **Friday opens the PR and lands it once CodeQL and the checks are green. Never push an unscanned commit to main.** The Datasec org requires CodeQL (`.github/workflows/ci.yml:5`). **No PR from you.**

## Ports
- **6670–6679.** **Friday assigns this range to B53.** That overrides "never use a port named in an earlier brief" for this range only. (B41's brief `:88` says 6660–6699 "is named by other non-MPS drafts".)
- The draft writer checked at 19:22 AEDT: `lsof -nP -iTCP:6670-6689 -sTCP:LISTEN` printed nothing (rc 1), so there were **0 listeners**. **Run `lsof` before every bind.** On any listener in your range, **STOP: NEEDS FRIDAY**; do not move ranges. Pass ports through env (`MPSCALC_WEB_PORT`, `MPSCALC_API_ORIGIN`); never edit a shared config default. Most of this lane needs no port: unit/in-process tests and the `ApiProcess` harness pick their own.

## Write set (PATHS; nothing outside it)
- `src/MpsCalc.Api/Sources/SourceLifecycle.cs`, `SourceDocumentChecks.cs`, `SourceAdminEndpoints.cs`, `SourceGovernance.cs` (only if a constant or state needs a home)
- `tests/MpsCalc.Api.Tests/SourceLifecycleTests*.cs` (the 11 existing files) and a new `tests/MpsCalc.Api.Tests/SourceLifecycleTests.B53.cs`
- `tests/MpsCalc.Api.Tests/Infrastructure/SourceStores.cs`. Only the source lifecycle tests use it; measured with `git grep -l SourceStores b28c95eb -- tests`.
- That is **17 paths**. Friday computed this set disjoint from the three in-flight sets with `comm -12`, every intersection 0 (`friday/briefs_drafts/2026-10-12_mpscalc_lanes_1919.md`, `## Proposed lanes`):
  - **b49** `main...b49/gate-b48-fix-round` (37 files);
  - **b47** `main...b47/feedback-pill` (31 files);
  - **the one-pager build** (`ProposalPage`, `ProposalDocument`, `proposal.css`, `Lifecycle.tsx`, `router.ts`, their tests, `Proposal.cs`, `QuoteEvents.cs`, `Dtos.cs` and `web/src/api/generated/**`).
- **FROZEN (diff must be empty; check with `git diff --numstat <base> -- <path>`):**
  - **`src/MpsCalc.Api/Program.cs`** (b47 owns it). Its call sites `:65-66` (`OpenFromConfiguration`, `StoreFileActiveSources.Load`) keep their signatures.
  - **`src/MpsCalc.Api/Sources/ActiveSources.cs`**: `IActiveSources` is read by `Inventory/` (lane B54) and `Quotes/`.
  - `src/MpsCalc.Api/Quotes/**`, `Contracts/**`, `Inventory/**`, `Feedback/**`, `Infrastructure/**`.
  - `src/MpsCalc.Engine/**`, `src/MpsCalc.Import/**`.
  - **`docs/API.md`, `docs/api/openapi.json`, `web/**`** (contract and contract-sync outputs are shared files).
  - `tests/MpsCalc.Api.Tests/Infrastructure/{ApiHost,ApiProcess,Contract,EntraHost}.cs`, `EntraAuthTests.cs`, every other test file, `*.csproj`.
  - `infra/**`, `scripts/**`, `.github/**`, `docs/{DEMO,ENGINE,IMPORTER}.md`.
- **If an item needs a frozen file** (for example a response code missing from `openapi.json`, or a log line that needs `Program.cs`): do not touch the file. Mark the item **NOT DONE: BLOCKED-BY-FILES (<file>, <owner branch>)** and go on to the next item.

## ITEMS (in this order; red test first for each; one commit per item)
### 1. MPSCALC-90 (B43 Q-1): three store shapes refuse the start in words
- Follow B43's HOW verbatim: in `ReadRegistry` and `IsEmptyStore`, catch `IOException` and `UnauthorizedAccessException` from the **read**. Refuse in words (*"…registry.json cannot be read (a link to nothing, or no permission). It is never repaired…"*), naming only the configured path, with no inner exception. Treat a non-directory `versions` as "not an empty store".
- Regression arms: (a) `registry.json` is a dangling symbolic link; (b) `registry.json` has mode 000 (skip the arm with a stated reason when running as root); (c) `versions` is a regular file. Each must assert `Start refused`, the fixed words, **no stack and no inner exception text**, and the store bytes unchanged.

### 2. MPSCALC-92 (B43 Q-3): catch-alls catch only what a document can raise
- In `SourceDocumentChecks.cs:127` (`Parse`) and `:156` (`EngineRead`), catch only `ArgumentException` (and subclasses), `FormatException`, `OverflowException`, the reader's `InvalidOperationException`, `JsonException` and `InvalidDataException`.
- On the routes, any other type reaches the existing Backstop: 500 `SOURCE_LIFECYCLE_FAILED`, logged by **type name only**.
- At start (no logger: `Program.cs` is frozen), any other type refuses the start with fixed words that name the **exception type only** and say it is not a document fault. It must never say "re-import".
- Red-proof: B43's probe P4 shape, a seam that throws `NullReferenceException` inside `EngineRead` after a successful read. On a **valid** v2, validate must answer 500 `SOURCE_LIFECYCLE_FAILED` with 1 warning or error log line naming the type, and must **not** give `Failed Validation`/`REFERENCE_DATA_REJECTED`. At start, the words must name the type and not "Re-import". Planted-value control: the document's synthetic SKU never appears in the response or the log.

### 3. MPSCALC-91 (B43 Q-2): a reference-only store that loses registry.json refuses instead of re-initialising
- **Friday's default (a rule choice, not Kam's):** B43's "dedicated start marker".
  - The first start writes a marker file in the store root (0600, temp + rename, never deleted).
  - A store with the marker but no `registry.json` **refuses** the start in words.
  - An existing store that has a registry and no marker gets the marker at its next successful start (the migration). Say this in STATUS.
- B43 Q-10 stays as measured: a `.DS_Store`-only store is still refused.
- Regression: first start → move the registry aside → start again → refused, and the Active governed id and the events are unchanged once the registry is restored. Plus every existing B41/B42/B43 start arm stays green unmodified.

### 4. B43-Q8: a registry events list with a gap or a repeat refuses the start
- At read, event sequences must be 1..n, contiguous and unique, and event ids unique. Otherwise refuse in words, naming the path only.
- Tests: a gap arm, a repeated-sequence arm and a repeated-id arm. Each must assert the refusal and that no later step can write a duplicate (B43's `after_step_ids_unique` probe, inverted).

### 5. B43-Q4: client transport faults on the stage route are a 400, not an Error
- In `ReadCapped`, answer `BadHttpRequestException` and `ConnectionResetException` as 400 `BAD_REQUEST`. The stage route's contract already lists 400 (`openapi.json`: `POST /api/v1/admin/sources/{type}/imports` → 201/400/401/403/409/413/415/500). They must write **no Error/backstop log line**.
- Test: a raw socket sends a `Content-Length` larger than the body, then closes. Assert 0 backstop lines and the store unchanged.

### 6. B43-Q5: an exception thrown during result execution answers `SOURCE_LIFECYCLE_FAILED`, not the developer exception page
- **Route-local only.** For example, a result wrapper returned by the seven handlers whose `ExecuteAsync` catches and writes the fixed problem when the response has not started. A middleware needs `Program.cs` (frozen): **if a route-local fix cannot catch it, mark Q-5 NOT DONE: BLOCKED-BY-FILES (`Program.cs`, b47)**.
- Test: a seam result that throws, in Development mode, on all 7 routes. Each answers `SOURCE_LIFECYCLE_FAILED`, and the body carries **no** exception text, stack frame or absolute path (B43 measured 14/14 cells leaking).

### 7. B43-Q6: the backstop test covers 7 routes × 4 exception types
- A theory over the seven routes × {`InvalidOperationException`, `ArgumentException`, `AggregateException`, `NullReferenceException`} via a seam (B43's HOW).
- Mutants G1 (rethrow `ArgumentException`) and G3 (filter dropped from `source-events`) must each turn it RED.

### 8. B42-L1: a throw after the registry rename leaves memory and disk agreeing
- After a failed swap, reload the registry from disk under the lock, or reorder so that nothing that can throw runs between the rename and the swap.
- Test via the existing `AfterRegistryWrite` seam: (a) a non-I/O throw → 500, then the next step's events continue the sequence with **no reused sequence and no rewound pointer**; (b) an `IOException` there → the answer must not claim "Nothing changed" when the disk changed.

### 9. B42-L4: duplicate JSON keys in a staged document
- **Friday's default (a rule choice):** **refuse.**
  - The importer never writes duplicates.
  - A raw `Utf8JsonReader` pre-scan per object, up to `MaxDocumentBytes`, answers the stage with 400, or validate with `Failed Validation`. Use whichever existing code fits (name it), and only one the contract already lists for that route.
  - The fixed words name the JSON path of the first duplicate, **never its value**.
- Tests: B42 planted variant p15 now refused; a 16 MiB document without duplicates still stages; a value-free control.

### 10. B40-R8: a cross-process lock on the source version store
- Copy the shape of the overlay's B22 pattern: an exclusive lock file in the store root (created once, 0600, never deleted), taken for every lifecycle step. **Reload `registry.json` from disk under it before each step**, and refuse a registry older than the one this process last wrote. Keep Busy behaviour bounded, as the overlay does: answer within a fixed bound with a fixed code.
- **Use only codes the contract already lists for each route** (409 or 500). A new code or status is a contract change: mark the item BLOCKED-BY-FILES.
- Tests (B41 N-3's arms, **two real API processes on one synthetic store** through the `ApiProcess` harness, read-only use):
  - two simultaneous first starts register **one** Active id;
  - an activation through A is visible to B's next read or step;
  - a stage through B **keeps** v2 and A's events (B41 measured "v2 and 4 events vanished").
  - Run the burst 20 times: 20/20 green.
- **This is the prerequisite for `[B40-R3]` (hosted switch-on). Do not build R3.**

## Test Evidence (run each command as `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head** (in `wt-B53-base` and `wt-B53`):
  - the .NET full suite, Release `--no-incremental`, **0 warnings**;
  - `dotnet list package --vulnerable --include-transitive`: 0;
  - reconcile every count change **by test name**.
  - This lane has no web change: prove it with `git diff --numstat <base> -- web` empty.
- **Red-first, per item:** each new test fails at base (or at the item's parent commit) and passes at head. Report `RED n/m → GREEN`.
- **Red-proof table, one line per conjunct** (tamper → RED on the full suite → sha256 restore). At least:
  - (1) the catch re-excludes `IOException`;
  - (2) the catch-all is restored, or the type name is dropped from the log;
  - (3) a marker present without a registry re-initialises;
  - (4) a gap is accepted;
  - (5) a transport fault is logged at Error;
  - (6) the wrapper removed on one route;
  - (7) G1 and G3;
  - (8) the reload removed;
  - (9) last-wins restored;
  - (10) the lock not taken on one step, and the reload-before-step removed.
- **Leak + secret scan** over `git diff <base>...HEAD` and `git log --format=%B <base>..HEAD`, with copies of the B36/B38/B43 tools: counts only, with a planted control per class that fires.
- **No frozen change:** `git diff --numstat <base> -- <frozen list above>` is empty. Paste the command and its 0-line output.
- **Processes:** state every process you started (pid, port, cwd) and its stop. **0 left running at READY.**
- Evidence goes in `Briefs/2026-10-12_B53_evidence/` (0700 folder, 0600 files). Tools and logs go in `.tools/qa-B53/` (0700).

## NEW WORDS (Friday shows Kam before any deploy)
List every new or changed user- or operator-visible string verbatim, old → new, with `file:line`: start refusals, problem `detail`s and log templates. All of these are operator-facing, but they still ship. Run copies of B36's `words36cs.py` / `newwords36.py` over `<base>...<head>`. Every extracted string must be in your table (count = count), and a planted undeclared string must be flagged.

## STATUS sections
- BLUF (one-line verdict per item).
- **PRIOR WORK**: each cite re-read at base, and what moved.
- Base read; commits.
- Test Evidence; the red-proof table; Tier-1 conditions.
- **FOUND / TESTED / HOW / NOT TESTED** per item: FOUND cites `file:line` at base, TESTED gives red-first counts, HOW gives ratios, NOT TESTED says why.
- NEW WORDS; modified pre-existing tests (before → after, and why); UNMEASURED.
- `## NOT DONE / NOT COVERED`, each with BLOCKED-BY-FILES or the reason.
- RECORDS.
- needs-Friday: the Q-2 marker default, the L-4 refuse default, every NOT DONE, and Jira draft lines for MPSCALC-90/91/92/50/55. Jira writes are Friday's.
- Leak + secret scan; processes started and stopped; worktrees and files left.

## RECORDS (local `records/b53` branch, commit only)
- The records repo is the project root (no remote). `git -C '<project root>' worktree add .tools/wt-B53-records -b records/b53 main` (`chmod 700`).
- Add `BACKLOG.md` `## Deferred problems` rows (existing shape) for each NOT DONE item and each new residue. **Edit no existing row.**
- One commit: `Records: source store hardening remainders (B53)`. **Never fold it into `main`** (that is Friday's job).

## Time-box
**About 4 h.** If you run short, finish in this order: 1, 2, 3, 4, 8, 5, 7, 6, 9, 10. List the rest as NOT DONE, never half-merged. Item 10 alone can take the last 1.5 h; that is expected.

## UNMEASURED (by the draft writer, each with its closing instrument)
- Suite counts at `b28c95eb`. Closes with your base run.
- Whether a route-local wrapper catches result-execution throws (Q-5). Closes with your item-6 red test.
- Whether 409 or 500 fits a Busy lock answer on each route without a contract change. Closes with your read of `openapi.json` per route (read only).
- CodeQL and CI: Friday reads them on the PR.

## HOLDS
- Datasec only. No other client's names, tickets or paths.
- **CodeQL policy:** push your branch only; never push to main; never dismiss an alert; never ask for a bypass. **No PR.**
- **No deploy.** No Azure command, no app-setting change, nothing sent to any human, **no Jira write**.
- **SITE HOLD** (records `BACKLOG.md` `## Holds on the hosted site`): none of the four store path settings changes. The source version store stays **DevStub-only and off by default**: `OpenFromConfiguration` keeps refusing a store path in Entra mode (`[B40-R3]` is not this lane).
- **P-1 / B38 L-2 HOLD:** no hosted deploy of a main that contains K-3 until the hosted repeated-line-number count is recorded. This brief deploys nothing.
- **Q-09:** never activate, stage, open or show a real price book. Every store, document, fixture and probe is **synthetic** (`SourceStores.cs` helpers). Never open `.local/pricebooks/` or any file under it.
- No pricing rule change: no price, total or applied percent moves on any fixture (the full engine and API suites prove it).
- **Never open `4_Credentials/.env`.** No secrets in code, tests, STATUS or commit messages.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-12_B53_<what>/` (0700). Never edit a running script.
- **No `5_Project_History/history.md` entry** (Friday's).
- **Own worktree and own ports.**
  - Allowed: `fetch`, `worktree add`, commits and pushes on your own branch; records commits on `records/b53` only.
  - Never `checkout`/`switch` in `2_Project_Files` or the project root.
  - Never `gc`, `prune`, `reset`, `worktree remove`, `branch -D` or force-push.
  - Other seats' worktrees (`wt-B49`, `wt-B47`, `wt-B54`, …) and `qa-B4?/` are read-only; copy from them.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate`, the shared `VBCSCompiler` and any listener outside 6670–6679 are not yours.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`; `UseSharedCompilation=false`; build with `-nodeReuse:false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero needs a positive control that fired.

## End
The last line of `Briefs/2026-10-12_B53_STATUS.md` is exactly one of:
- `READY FOR GATE: b53/source-store-hardening <sha>` (the SHA read back by `ls-remote` in the same action as the push);
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.
