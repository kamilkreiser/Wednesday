From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to friday-laptop-agent@agentmail.to. This project has no mail key, so your STATUS file is your wrap.
# BRIEF B54 · SEAT-F: catalogue overlay store residue: gate B27 H-1…H-4 and the load-sensitive burst test (B37-G1-LOAD / B38-N6)
**Written:** @NOW@ AEDT 2026-10-12. This is a draft. Friday sets the time when he fires it. **Pane:** `Datasec/MPS-F`. Your commission is the newest file in `Briefs/` whose name contains `_SEAT-F_`.
(Launcher check. `Launch_Claude.command:107` takes the seat letter from a pane name that matches `*MPS*-?`. `:111` makes the commission "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". The launcher states the rule in the prompt; it does not pick the file itself. At drafting (19:2x AEDT), `ls Briefs | grep -i -c _SEAT-F_` printed **0**, so this is the first Seat F brief in this project.)
**Seat:** Seat F, a Claude build seat. One branch, red-first. **QA tier 1** throughout. H-1 is a path-safety refusal on a store that holds sell prices, and it is the code half of lifting the hosted SITE HOLD. H-3 changes how the overlay's writer lock waits.
**Round:** round 1 of a new lane (lane A3, named in the 2026-10-11 reconcile). The two-NO-GO cap starts fresh.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B54_STATUS.md`. Its **last line** is exactly one of these:
- `READY FOR GATE: b54/overlay-store-residue <sha>`, where `<sha>` is the full 40-hex SHA read back by `git ls-remote origin refs/heads/b54/overlay-store-residue` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.

## AUTHORITY
- **Kam, terminal to Friday, 2026-10-12 ~18:4x AEDT, verbatim:** *"keep going and keep rolling out agents to work through all tickets and items for MPS Calculator, Security Controls creation tool and HPSM POC"*. This brief is part of the MPS share. The other two projects are not yours.
- Records `BACKLOG.md` rows `[B27-H1]`…`[B27-H4]` say *"The residue is ticketed for its own round."* `[B27-H1]` adds: *"**The site HOLD above applies until this is fixed and deployed.**"* This brief fixes H-1. **It does not deploy, and it does not lift the hold.** A later brief does both.
- `[B37-G1-LOAD]` gives two fix shapes and says *"(not decided)"*. **Friday's default** is the second: *"assert 'every writer either 201 or a clean 503 with nothing changed' plus the existing no-loss / no-duplicate checks"*. That makes the test assert the contract, not more than it. Keep the product's 5 s bound. List this default in STATUS needs-Friday.

## PRIOR-WORK CHECK (do this first; report it in STATUS `## PRIOR WORK`)
Re-read each item at base and record whether it is **still open, already closed, or moved**, with `file:line`. If an item is already closed at base, do not rebuild it; say so.
- `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs`:
  - `:86` `DefaultLockTimeout` 5 s; `:116` `LockTimeout`.
  - `:151-158` `OpenHosted`: it compares the directory of the **configured** reference path, and nothing calls `ResolveLinkTarget`. Check with `git grep -n ResolveLinkTarget b28c95eb -- src/MpsCalc.Api/Inventory`; it printed 0 at drafting.
  - `:184-211` `RefuseOverlap`; `:251-255` `WellFormed` (null checks only); `:285-301` `Mutate` / `_lock.TryEnter(LockTimeout)`; `:344-367` `TakeFileLock` / `Thread.Sleep(25)`.
- `src/MpsCalc.Api/Inventory/InventoryEndpoints.cs:99` (`overlay.Mutate(…)`, the only product caller), `:28-34` and `:182` (reads of `IActiveSources`).
- `tests/MpsCalc.Api.Tests/OverlayGateFindingsTests.cs:367-387` (`G1_a_burst_across_two_hosts_loses_and_duplicates_nothing`, `:381`).
- Read whole:
  - `Briefs/2026-10-10_B27_STATUS.md` (H-1…H-4: FOUND, HOW and the regression shapes);
  - `B25` and `B22` STATUS (the overlay's G-1…G-4 and its persistence design);
  - `B37_evidence/08_g1-burst-5x.txt` and `B38_STATUS.md` `## Notes` N-6;
  - the records `BACKLOG.md` rows named above, plus `[B40-R4]` (**for information only: not this lane's**);
  - the project `CLAUDE.md` and records-main `CLARIFICATIONS.md` (C-19: the restart proof waits on Kam's test).
- Search for prior work: `git log --all --oneline -i --grep='H-1\|H-3\|H-4\|overlay'`. List the hits.

## Base and branch
- **Base: MPS code main = `b28c95eb0f73ed0ce7ae410791feefc8b1a059ea`**, read by the draft writer at 19:1x AEDT with `git -C 2_Project_Files ls-remote origin`. `Inventory/**` is byte-identical from `42d6eca` (B25, PR #22) to base. Verify this with `git diff --stat 42d6eca b28c95eb -- src/MpsCalc.Api/Inventory`; if it is not empty, list what moved.
- **First action:** `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/main`.
  - If it prints `b28c95eb…`, proceed.
  - If it prints a descendant (b49 or b47 may land while you work), run `git diff --name-only b28c95eb <main> -- src/MpsCalc.Api/Inventory tests/MpsCalc.Api.Tests/Overlay* tests/MpsCalc.Api.Tests/InventoryApiTests.cs`. If that prints anything, **STOP: NEEDS FRIDAY**. If it prints nothing, stay on `b28c95eb` and say so.
  - Anything else: **STOP: NEEDS FRIDAY**. Never rebase on your own.
- Branch **`b54/overlay-store-residue`** in a fresh worktree `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B54'` (`chmod 700`). Take base measurements in `.tools/wt-B54-base`, detached at base. At drafting, `ls-remote origin 'refs/heads/b54*'` printed 0 lines.
- **Push your branch only, and read it back.** **Friday opens the PR and lands it once CodeQL and the checks are green. Never push an unscanned commit to main.** **No PR from you.**

## Ports
- **6680–6689.** **Friday assigns this range to B54**, overriding "never use a port named in an earlier brief" for this range only.
- The draft writer's check at 19:22 AEDT: `lsof -nP -iTCP:6670-6689 -sTCP:LISTEN` printed nothing (rc 1), so **0 listeners**. **Run `lsof` again before every bind.** On any listener in your range, **STOP: NEEDS FRIDAY**; do not move ranges.
- Pass ports through env; never edit a shared config default. Most tests here are in-process and need no port.

## Write set (PATHS; nothing outside it)
- `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs`, `src/MpsCalc.Api/Inventory/InventoryEndpoints.cs`
- `tests/MpsCalc.Api.Tests/OverlayGateFindingsTests.cs`, `OverlayHostedStoreTests.cs`, `OverlayRestartTests.cs`, `InventoryApiTests.cs`
- a new file `tests/MpsCalc.Api.Tests/OverlayResidueTests.B54.cs`
- **7 paths.** Friday checked that this set is disjoint from the three in-flight sets with `comm -12`; every intersection was 0 (`friday/briefs_drafts/2026-10-12_mpscalc_lanes_1919.md`):
  - **b49** `main...b49/gate-b48-fix-round` (37 files);
  - **b47** `main...b47/feedback-pill` (31 files);
  - **the one-pager build** (`ProposalPage`, `ProposalDocument`, `proposal.css`, `Lifecycle.tsx`, `router.ts`, their tests, `Proposal.cs`, `QuoteEvents.cs`, `Dtos.cs`, `web/src/api/generated/**`);
  - and from **lane B53** (`Sources/**` and its tests).
- **FROZEN (the diff must be empty):**
  - **`src/MpsCalc.Api/Program.cs`** (b47 owns it). Its uses `:60-62` (`Open`, `OpenHosted`), `:76-83` (`PlatformModesWarning`, `StrayTempFiles`) keep their signatures. **`CatalogueOverlayStore.PathKey` and `FileName`/`LockFileName` keep their names and values**: `Sources/SourceLifecycle.cs:118` reads `PathKey`.
  - `src/MpsCalc.Api/Sources/**` (lane B53), `Quotes/**`, `Contracts/**`, `Feedback/**`, `Infrastructure/**`.
  - `src/MpsCalc.Engine/**`, **`src/MpsCalc.Import/**`** (H-4 must not edit `ReferenceStore.JsonOptions`; use options local to the overlay file).
  - **`docs/API.md`, `docs/api/openapi.json`, `web/**`** (the contract and its generated outputs are shared).
  - `tests/…/Infrastructure/**`, `EntraAuthTests.cs`, every other test file, `*.csproj`; `infra/**`, `scripts/**`, `.github/**`, `docs/*.md`.
- **If an item needs a frozen file** (for example a response code the contract does not list), do not touch it. Mark the arm **NOT DONE: BLOCKED-BY-FILES (<file>, <owner>)** and go on.

## ITEMS (in this order; red test first for each; one commit per item)
### 1. B27-H1: a reference path that is a file link into the overlay directory is refused
- Do B27's HOW:
  - resolve the reference file's **final target** (`new FileInfo(path).ResolveLinkTarget(returnFinalTarget: true)`, or `RealPath` of the parent plus a link check on the last component);
  - run `RefuseOverlap` on that target's directory **as well as** the configured one;
  - **Friday's default:** do **not** refuse a reference path just because it is a link, since a link to a genuinely different directory still opens.
- Tests (B27's three):
  - (a) a file link `<HR>/pbf/reference.json` → `<HR>/ov/reference.json`: the start is refused, the words name the reference directory, and nothing is written beside the real file;
  - (b) the same with a case change in the link target, on the case-insensitive temp volume (as B25 G-4 did);
  - (c) a file link to a genuinely different directory: it opens.
- Also: a link chain (link → link → file in overlay dir) is refused; a dangling reference link is refused in words, not with a stack.
- **This does not lift the SITE HOLD.** The hold lifts only after deploy, by a later brief.

### 2. B27-H4: malformed overlay.json forms are refused at start and while running
- Extend `WellFormed` to every non-nullable audit field (`By`, `Key`, `Field`, `Reason`) and refuse an `ItemClass` outside the enum (`Enum.IsDefined`). Either do that, or deserialize **this file only** with options that set `RespectNullableAnnotations = true` and a `JsonStringEnumConverter` with `allowIntegerValues: false`. **Never edit `ReferenceStore.JsonOptions`** (`src/MpsCalc.Import` is frozen).
- Tests, for each of B27's 4 forms:
  - an audit entry with `by: null`;
  - one with `by`, `key`, `field` and `reason` null;
  - one with `by` absent;
  - a manual row with `itemClass: 99`.
- Each form must give `Start refused` at boot with the file byte-unchanged.
- **While running (the file is newer):** answer 503 only on routes whose contract already lists 503: `GET /api/v1/inventory`, `POST …/manual-items`, `PATCH …/{key}` (`openapi.json` responses, read only). **`GET /api/v1/inventory/audit` lists no 503.** If B27's "audit → 503" arm needs one, mark that arm **NOT DONE: BLOCKED-BY-FILES (`docs/api/openapi.json`, shared)** and say what audit answers today.
- Every arm leaves the file byte-unchanged, and the next write persists no null and no 99.

### 3. B27-H3: waiting writers never starve the pool; the Busy bound holds at 64 waiting
- Do B27's HOW:
  - async waits: `SemaphoreSlim.WaitAsync(timeout)` for the writer turn, and `await Task.Delay` between lock-file attempts, so `Mutate` becomes async. Update its only product caller, `InventoryEndpoints.cs:99`, and the test callers (`InventoryApiTests.cs:416-417`, `OverlayGateFindingsTests.cs:60`, `OverlayHostedStoreTests.cs:67`). A sync wrapper used only by tests is allowed if you say so;
  - **start the arrival clock at request entry**, not in `Mutate`;
  - optional cap: beyond N waiting writers, answer Busy at once. Name N and why.
- The answer stays the documented 503 Busy (`OVERLAY_UNAVAILABLE`, nothing changed). **No new code or status.**
- Regression (B27): `overlay.lock` is held by another handle. **64 concurrent PATCHes all answer Busy within the bound plus a stated margin**, and a `GET /api/v1/inventory/audit` meanwhile takes **< 100 ms**. Repeat at 16 and 32. Report max/median per run, as ratios. At base, B27 measured 64/64 late (max 15.02 s) and a 9.5 s read.

### 4. B27-H2 + B37-G1-LOAD (+ B38-N6): the burst test asserts the contract
- **Friday's default:** in `G1_a_burst_across_two_hosts_loses_and_duplicates_nothing`, assert that every writer gets either **201, or a clean 503 with nothing changed**. Then assert, over the 201s: overlay versions contiguous, none twice, none lost, and the audit sequence equal to the 201 count. **Keep the product's 5 s `LockTimeout`.**
- Regression: **20 consecutive green runs** of the group, alone. Then run it under parallel load from a second **synthetic** suite run in your worktree (state the load average from `uptime` before and after). Report n/20 under load.
- A tamper that drops one 201 write (the persistence step skipped) must still turn the test RED. The test must not become vacuous: assert at least one 201 in every run.

## Test Evidence (run each command as `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head** (in `wt-B54-base` and `wt-B54`):
  - .NET full suite, Release `--no-incremental`, **0 warnings**;
  - `dotnet list package --vulnerable --include-transitive` 0;
  - reconcile every count change by test name;
  - `git diff --numstat <base> -- web` empty.
- **Red-first, per item:** each new test fails at base (or the item's parent commit) and passes at head. Report `RED n/m → GREEN`.
- **Red-proof table, one line per conjunct** (tamper → RED on the full suite → sha256 restore). At least:
  1. final-target resolution removed; the case-insensitive compare made ordinal;
  2. each of the 4 `WellFormed` / enum checks removed, one at a time;
  3. `Thread.Sleep`/`TryEnter` restored; the arrival clock moved back into `Mutate`;
  4. the "at least one 201" check removed; a lost write.
- **Live probe** (DevStub, your ports, a **synthetic** reference file and overlay dir under `.tools/qa-B54/`):
  - start with H-1's link layouts (refused / opens);
  - one manual row, one price edit, a restart: the overlay version and audit are kept (B22's behaviour unchanged);
  - the 64-writer measurement against the running process.
- **Leak + secret scan** over `git diff <base>...HEAD` and `git log --format=%B <base>..HEAD` with copies of the B36/B38 tools (counts only, planted control per class that fires).
- **No frozen change:** `git diff --numstat <base> -- <frozen list>` empty (paste it).
- **Processes:** every process you started (pid, port, cwd) and its stop. **0 left at READY.**
- Evidence → `Briefs/2026-10-12_B54_evidence/` (0700 folder, 0600 files); tools/logs → `.tools/qa-B54/` (0700).

## NEW WORDS (Friday shows Kam before any deploy)
Every new or changed visible string, old → new, verbatim, with `file:line`: start refusals, problem `detail`s, log templates. Run copies of `words36cs.py` / `newwords36.py` over `<base>...<head>`: count = count, and a planted undeclared string must be flagged.

## STATUS sections
- BLUF (one line per item)
- **PRIOR WORK**
- Base read; Commits
- Test Evidence; Red-proof table; Tier-1 conditions
- FOUND / TESTED / HOW / NOT TESTED per item
- the H-3 timing table (16/32/64 waiting: n late / N, max, median, read time)
- NEW WORDS; Modified pre-existing tests (before → after, why)
- UNMEASURED
- `## NOT DONE / NOT COVERED`
- RECORDS
- needs-Friday:
  - the H-1 "links allowed" default;
  - the G1 assertion default;
  - the H-3 cap;
  - every BLOCKED-BY-FILES arm;
  - one line for Friday: "H-1 fixed on branch; the SITE HOLD stays until a deploy brief";
  - Jira draft lines (Jira writes are Friday's).
- Leak + secret scan; processes; worktrees and files left

## RECORDS (local `records/b54` branch, commit only)
- `git -C '<project root>' worktree add .tools/wt-B54-records -b records/b54 main` (`chmod 700`).
- `BACKLOG.md` `## Deferred problems`: add new rows for each NOT DONE arm and each new residue. **Edit no existing row**; Friday folds the closes.
- One commit, `Records: overlay store residue remainders (B54)`. **Never fold into `main`.**

## Time-box
**About 3–4 h.** If short, finish in this order: 1, 2, 4, 3. List the rest as NOT DONE, never half-merged.

## UNMEASURED (by the draft writer, each with its closing instrument)
- Suite counts at `b28c95eb`: closes with your base run.
- Whether `ResolveLinkTarget(returnFinalTarget: true)` resolves a link whose target differs only in case on the temp volume: closes with arm 1(b).
- Whether the H-3 change moves any existing overlay test's timing bound: closes with your base-vs-head reconcile.
- CodeQL and CI: Friday reads them on the PR.

## HOLDS
- Datasec only. No other client's names, tickets or paths.
- **CodeQL policy:** push your branch only; never push to main; never dismiss an alert; never ask for a bypass. **No PR.**
- **No deploy.** No Azure command, no app-setting change, nothing sent to any human, **no Jira write**.
- **SITE HOLD** (records `BACKLOG.md` `## Holds on the hosted site`): none of the four store path settings changes. `MpsCalc:ReferenceStorePath` stays a regular file on the hosted site. Fixing H-1 on a branch **does not lift it**.
- **P-1 / B38 L-2 HOLD:** no hosted deploy of a main that contains K-3 until the hosted repeated-line-number count is recorded. This brief deploys nothing.
- **Q-09:** never open, activate or show a real price book. Every reference file, overlay and probe is **synthetic**. Never open `.local/pricebooks/` or anything under it.
- No pricing rule change: no price, total or applied percent moves on any fixture (full engine + API suites).
- **Never open `4_Credentials/.env`.** No secrets anywhere.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-12_B54_<what>/` (0700). Never edit a running script.
- **No `5_Project_History/history.md` entry** (Friday's).
- **Own worktree and own ports.**
  - Allowed: `fetch`, `worktree add`, commits and pushes on your own branch; records commits on `records/b54` only.
  - Never `checkout`/`switch` in `2_Project_Files` or the project root.
  - Never `gc`, `prune`, `reset`, `worktree remove`, `branch -D` or force-push.
  - Other seats' worktrees (`wt-B49`, `wt-B47`, `wt-B53`, …) are read-only.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate`, the shared `VBCSCompiler` and any listener outside 6680–6689 are not yours.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`; `UseSharedCompilation=false`; `-nodeReuse:false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero needs a positive control that fired. The H-3 and burst timings run while lane B53 may also be building: state the load average with every timing.

## End
The last line of `Briefs/2026-10-12_B54_STATUS.md` is exactly one of:
- `READY FOR GATE: b54/overlay-store-residue <sha>`
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.
