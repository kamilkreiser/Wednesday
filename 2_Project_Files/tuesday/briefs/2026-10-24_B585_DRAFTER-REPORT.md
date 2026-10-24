# B585 drafter report (SEAT-M14, MPS lane M2, Sonnet builder, row C2, tier 1 gate after)

Drafted 2026-10-24 about 14:50-15:25 AEDT, read-only. Brief: `2026-10-24_B585_SEAT-M14_mps-store-engine-hardening-m2.md` (116 lines; 8 lines carry the four-underscore pattern, lines 95-101 and 116; non-ASCII bytes 0 by `python3 -I`) plus a byte-identical `.pre-stamp` (`cmp` same).

## Reads (how)
- Sweep `0_Brain/projects_index/2026-10-24_datasec-completable-tickets-1500.md` (lines 1, 25-76, 179): lane M2 table and lane M1 table.
- Template B565 brief (whole) and its drafter report (head); B573 brief (Stamp, heavy-slot and NuGet-home lines).
- Jira GET (credentials by name, in-process, never printed): MPSCALC-323, -324, -326, -327, each whole. All Backlog, `tier-1`, 0 comments, updated 09:10-09:11 today.
- Gate STATUS files by grep and line reads: `B552_STATUS.md` (findings B552-2 and B552-3, FACTs, mutants Q13/S7/S8/S9) and `B575_STATUS.md` (lines 1, 14-15, 37, 60-63, 102-105, 118: the findings are carried and the files read only).
- Code at main `05c598f3...` via `gh api -X GET contents?ref=<sha>` (raw), saved to the drafter's scratchpad and read whole: `ActiveSources.cs` (127 lines), `Program.cs` (138), `QuoteCalculator.cs` (628, lines 55-100), `ReferenceStoreDocument.cs` (126), `SourceDocumentChecks.cs` (1-150, 290-350 and grep), `Records.cs` (grep), `StoreLoadRows.Faults.cs` (120), `QuoteEndpoints.cs` (1286-1360). **The local clone does NOT hold the object** (`git cat-file -t 05c598f3...` fails), so no `git show` was possible and fetch is forbidden; the brief orders one explicit-refspec fetch as the seat's Step 0.
- `ls-remote origin refs/heads/main` = `05c598f3cd8eb4d36f10e31d9a4effa013d4a717` (equals the sha you named).
- `gh api` commits per path (last commits of the four source files), `matching-refs/heads/b` (no `b58*` ref, no `b585`), tree listing (717 paths), `tmux list-panes` (`%0 tuesday`, `%1 fleet-monitor`), `ls .tools` (no `b585*`, no `heavy-slot-*`), `uptime` (load1 2.78 at 15:09).
- `gh auth status` under the MPS config reads `kamilDatasec` (logged in, active).

## Fact counts run (on the drafter's saved copies, control `zzz-no-such-string-7f3a` = 0)
`return new FixedActiveSources(null);` 4; `UnauthorizedAccessException or IOException` 1; `AddSingleton<IActiveSources>` 1 (Program.cs); `AfterEngineRead` 2; `ex is ArgumentException or FormatException` 1; `poolQty[x.Device.TierPool]` 2; `internal static IResult BodyRefused(JsonException ex)` 1. Not run against the git object (absent).

## Ports (how)
Python scan of `tuesday/briefs/2026-10-23_*` and `2026-10-24_*` for 9300-9999 tokens and ranges, then a word-boundary grep for `933[0-9]`: 0 files (control `932[0-9]`: 3 files). Range hits such as 9200-9399 and 9300-9399 are lsof scan statements in B578/B580/B581 reports, not allocations; the allocated blocks are 9300-9309 (B580, B581), 9310-9319 (B581), 9320-9329 (B582). `lsof -nP -iTCP:9330-9339 -sTCP:LISTEN` empty (rc 1); a `127.0.0.1:9330` bind control was listed and, after it exited, freed (rc 1). **First free block from 9330: 9330-9339.** Another drafter running now could pick the same block: Tuesday re-checks at the stamp.

## Decisions I made (Tuesday strikes any at the stamp)
1. **Gate tier 1 (Opus).** -323 changes when the store file is read (a store read path); -326/-327 change what the load refuses (503 where a 500 or a contract-breaking 200 answered). Tier 2 would only fit -324.
2. **-323:** keep the operator line; `Load` returns, for a CannotOpen outcome, a source that tries the load again on the next read (lock, no clock/timer), keeps the first success, logs the existing line on the first fault only (the existing "exactly 1 warning" row at `StoreLoadRows.Faults.cs:105-118` stays green). `NoStore` and `Unreadable` stay until restart (their lines say "imported again"); reported FOR TUESDAY, not built. Program.cs unchanged.
3. **-326 and -327 share one refusal point**: `ActiveSourceSet.From`, reached by BOTH the file store (`Load` -> `EngineRead`) and the governed lifecycle (`SourceDocumentChecks.Run` calls `EngineRead` last and turns null into the existing `REFERENCE_DATA_REJECTED` / `DATA-IMP-002` issue). So the fix needs no new word and no change to QuoteCalculator.cs (the sweep listed it as the path for -326; the commission is to refuse at load, "refusal, not default"). The checks must run before any dereference, because `NullReferenceException` is not in `IsDocumentFault` (`SourceDocumentChecks.cs:326-327`) and would escape as a 500. The seat chooses an explicit list vs a `NullabilityInfoContext` walk; the legitimately nullable members (`CompatibilityBasis`, `ConstraintNote`, `Note`, care pack `DeviceSku`) must stay loadable.
4. **-324 is test-only and last.** All four survivors are reachable by a row: S7/S8/S9 through the existing internal seam `AfterEngineRead` (an exception thrown inside `Load`'s `try`; an `IOException` with a sentinel message for S9, since the platform sharing-violation text differs); Q13 by a unit row with a synthetic `JsonException` on `BodyRefused` (internal static). The gate called Q13 "unreachable through the API"; a unit row reaches it. The "reachable from the Api test project" claim for the seam is UNMEASURED.
5. **Partition:** Yours = `ActiveSources.cs`, optionally `ReferenceStoreDocument.cs` (default byte-equal), and NEW test files only. NOT YOURS (M1, from the sweep and tickets): `QuoteEndpoints.cs`, `PurchaseValidation.cs`, `Dtos.cs`, `PriceAudit.cs`, feedback sources, `docs/API.md`, `docs/api/openapi.json`, `web/src/api/generated/**`, feedback screens, `QuoteInputHardening.*.cs`, `QuoteApiTests*.cs`, `CLARIFICATIONS.md`, `BACKLOG.md`; plus M3/M4 paths and every Engine file. If the governed path needs `src/MpsCalc.Import/Validation/**` (validator throwing on a null before `EngineRead`), the seat STOPs with one question.
6. The sweep says 0 open PRs; my own `pulls?state=open` call failed on an unquoted `?` (zsh), so that figure is RELAYED, and the brief tells the seat to quote the URL.

## What I could not measure (and the brief says so)
No build/test/mutant/probe/fetch. Not measured: whether `ReferenceDocumentValidator.Validate` throws on a null member (not read); whether `AfterEngineRead` is visible to the Api test project; whether `FileShare.None` makes the open fail on Linux CI; the gate's 188-case member list (the seat derives its own census); the contract-check helper in the Api tests (the seat finds it); the model id (relayed from B565); Jira since 14:5x.

## What the reviewer checks first
1. Reading 2 (log once, retry on next read, no timer) and reading 1 (CannotOpen only; NoStore/Unreadable deferred).
2. Reading 3 and the explicit-list vs nullability-walk freedom, with the census program as the coverage proof.
3. Whether -324 should wait for M1-322 landing (the brief lets it run last, re-reads `BodyRefused`, and STOPs only if a row would need a `QuoteEndpoints.cs` edit).
4. Tier 1 for the gate.

## Files written (and nothing else)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B585_SEAT-M14_mps-store-engine-hardening-m2.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B585_SEAT-M14_mps-store-engine-hardening-m2.md.pre-stamp`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B585_DRAFTER-REPORT.md`
(Scratch copies of the fetched source files are in the session scratchpad only.)
