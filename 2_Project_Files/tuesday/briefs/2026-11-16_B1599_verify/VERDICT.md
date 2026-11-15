GATE B1599: GO WITH FINDINGS @ 99a2b0c on main 33fc239

Gate G2 on Opus, round 1 of 2. Datasec / HPSM-POC, repo datasecau/HPSM-POC. Clocks run from 05:44 to 06:18 AEDT on 2026-11-16 (`date`). Every run was in the gate's own clone and worktrees under the session scratchpad. The push URL was set to INVALID-NO-PUSH and nothing was pushed.

## Refs
- `git ls-remote` at 05:4x and again at 06:18: the branch b1599/hpsmpoc-forwardedproof-race = 99a2b0c51b365bd7f657dcfc47a31d430fbd86be (equal to READY). Main = 33fc2395eaf0d1baf5a505b7276b423031c9b0b7 (equal to the commission) at both reads. `gh api -X GET branches/main` gave the same main.
- Ahead/behind main: 1 / 0. Open PRs: 0 at the start and 0 at the end (control: `state=all&per_page=1` -> 324).
- `git merge-tree --write-tree main head` = 7c6bddbf..., equal to the head's own tree (clean; main plus the head blob).
- Author and committer are both the configured project identity. One trailer.

## Findings
| # | Row | Ruling | Evidence |
|---|---|---|---|
| 1 | Diagnosis: test defect, not a product race | CONFIRMED: TEST | Read at main: ForwardedProofGate.cs (whole). It holds only `ForwardedClientAddress forwarded`, decides on `context.Request.Headers` at :19-22 and keeps no field of its own. ForwardedClientAddress.cs is a sealed record (:32): `ProofDigest` is private init-only (:53), and Networks/Proxies are arrays built once in Read (:57-78). Program.cs:43-50 reads it once and runs PostConfigure on the options (once per options instance, not per request). :134 adds the gate with that one instance; :136 runs `UseForwardedHeaders(forwarded.MiddlewareOptions())`, a new options object built once at pipeline build. No product line assigns `RemoteIpAddress`, and there is no non-readonly static in api/src (git grep; control: RemoteIpAddress hits 2 files). The only shared mutable product state between requests is the follow-up rate limiter (FollowUpLink.cs:265-285). It is keyed BY the per-request address that `ClientAddress(...)` computes (:87-96, pure) and never feeds back into it. The test's shared state is `Watch.Seen`, one singleton IStartupFilter per factory (test :291), written after `await nextMiddleware` (main :271/:273) and read right after SendAsync. Measured: (i) the forcing test's `Assert.False(reading.IsCompleted)` holds 10/10 while the filter is held, which is direct proof that SendAsync returned before the pipeline finished; (ii) main's reds show only `(False, null)` (not yet written) or `(False, "198.51.100.7")` (the previous request's right answer), never an address no request produced; (iii) a scratch PRODUCT mutant (the gate keeps X-Forwarded-For on any value) fails the FIXED test 5/5 at :165. So a real misattribution still fails the fixed test, and head's 20/20, Hosting 3/3 and SQL 3/3 greens mean the product attributes correctly. No product path that could attribute a wrong client address was found. |
| 2 | Scope | PASS | `git diff --name-only main head` = exactly api/tests/HpsmPoc.Api.Tests/Hosting/ForwardedProofTests.cs (40+/6-). No product file. The 40 added lines hold 0 of Skip, Retry, Thread.Sleep, Task.Delay, [Collection or DisableParallelization (control: the plant diff reads 1). The three original assertions are byte-identical apart from `api.Watched` -> `await api.WatchedAsync()` (program compare: SAME x3; a planted changed literal reads DIFF). The tuple written is byte-identical to main's `Seen = (...)` expression, at the same place after the pipeline. Hang guard: `ReadAsync().AsTask().WaitAsync(30 s)` can only throw TimeoutException. A pass needs a real value equal to the expected one. Measured by mutant C (the write removed): the target test goes red in 31 s with `System.TimeoutException` at :277. It is not green and does not hang. |
| 3a | Target alone 20x at main | 11 of 20 RED | 9 at :165 `Actual: Tuple (False, "198.51.100.7")`, 2 at :163 `Actual: Tuple (False, null)`; load1 6.25-7.12 |
| 3b | 250 ms plant after `await nextMiddleware(context)` at main | 10 of 10 RED | All at :163 `Actual: Tuple (False, null)`; load1 7.47-7.99 |
| 3c | Forcing test, red form (head's hook, reading the field) | 10 of 10 RED | All at :178 `Actual: Tuple (False, null)`, about 2 s each, no hang. Built as main + the builder's red.diff. The hook lines (`Hold`, `HoldAfterPipeline`, `if (Hold is { } hold) await hold.Task;`, try/finally) are byte-identical to head's added lines (program compare SAME x6, control DIFF). |
| 3d | Head: forcing x10, target x20, both under the plant x10 | ALL GREEN | forcing 10/10; target 20/20; plant at head: target 10/10 (duration 2 s, so the delay was live), forcing 10/10 |
| 3e | Hosting. group x3 at head | GREEN 3/3 | 221/221 each (main 1x: 220/220, so +1 is the forcing test) |
| 3f | api-assessment SQL Server part x3 at head, as ci.yml:251-252 runs it, with the judge of ci.yml:278-310 extracted by program | GREEN 3/3 | Each run: dotnet rc 0, judge rc 0, outcomes {'Passed': 1486}, 4 named tests Passed, 325 `hpsmpoc%` databases (floor 100), password in log 0. Judge control: the same trx with one outcome planted Failed -> rc 1. Pinned images by digest, `--pull never`, 127.0.0.1:10190/10191, g1599-mssql / g1599-azurite removed by name (0 left). |
| 4 | Forcing test: non-vacuous, no hang, deterministic | PASS, with Minor F1 | Non-vacuous: red form 10/10 red (3c). Mutant A (hook no-op) fails 10/10 at :180 `IsCompleted` True, so the test also proves that its own hold holds. Deterministic: IsCompleted must be false while the hold is unreleased, because the write comes only after `await hold.Task`; 30/30 green across head and head+plant. No hang: mutant D (no SetResult) goes red in 31 s via the guard, and finally releases the hold. |
| 5 | CodeQL | Hand rows 0 | Over the 40 added lines: regex built from input, Process.Start, file/console/log writes, file mode, innerHTML/Html.Raw, raw SQL, catch-all, weak hash, Random: 0 (case-insensitive; control in the same file `TaskCompletionSource` = 2). Sensitive-name row: 1 hit, `Token(...)`, a call to the file's existing synthetic-token helper (:243). It is not a new identifier and not a new sink. `CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof` |
| 6 | PR text | WRITTEN | pr-title.txt, pr-body.txt, squash-subject.txt, squash-body.txt, landing.txt (head-pinned squash at 99a2b0c5...). |
| 7 | Scans | PASS | Names (ban list plus the project identity's user name), underscore-aware, over the added lines, the commit message and the builder's PR files: 0 (control `_by_Kam_`/`_by_Waite_` = 2). Fleet ids over the added lines and the message: 0. Secrets, tenant ids, hosts: 0 (control 1). Non-ASCII on the added lines: 0 (controls U+00A0/U+202E = 2). infra test_hidden_characters.py: 14 OK at main and at head (control: a planted U+202E -> FAILED). |
| 8 | Deploy | NONE | ci.yml is the only workflow (push main / pull_request / dispatch). ci.yml:1-3 says "No deploy job"; it keeps deploy packages only. A merge triggers build and test only. |
| F1 | Minor | Forcing-test hang hazard (future) | If a later TestServer made SendAsync wait for the whole pipeline, `await Open(...)` at :178 would wait on the held filter forever, and the try/finally could not release it (nothing in the try resumes). Today this does not happen (measured above). The builder disclosed it. Optional follow-up: guard that one Open with the same 30 s WaitAsync. Not blocking. |
| F2 | Minor | The builder's evidence pr-body.md names the branch (contains the work number) | Not used. The gate's pr-body.txt replaces it and names no branch. |
| F3 | Minor | The head commit's trailer names the builder model | The squash body replaces the message; squash-body.txt carries the gate's own trailer. |

## Builder STATUS claims (graded)
- The change is one file, the green.diff equals the pushed diff, and there is one commit on 33fc2395: TRUE (cmp equal).
- Main moved 243400dd -> 33fc2395 with no owned path touched: TRUE as far as the head's parent and its one-path diff go. The intermediate move was not re-measured.
- Base target alone 13 of 20 red at the current main: NOT CONTRADICTED. The gate read 11 of 20 with the same two shapes; the rate depends on timing.
- Plant at base 10/10 red `(False, null)`; red form 10/10 red; head forcing 10/10, target 20/20, plant at head 10/10 + 10/10: TRUE (reproduced).
- Hosting 221/221 at head: TRUE (gate 3 runs; builder claimed 5).
- SQL part at head bad == 0, 1486 passed, 325 DBs: TRUE (gate 3 of 3, identical numbers).
- The whole `api` predicate 4174 passed: NOT SHOWN to the gate (not run here; hosted CI is the proof).
- infra 325 OK: NOT SHOWN in full (the gate ran the hidden-characters test only: 14 OK at both).
- CodeQL csharp cannot extract on arm64: TRUE (consistent with the standard brief).

## NOT RUN
- CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof.
- The whole `api` predicate (`dotnet test HpsmPoc.slnx`, ci.yml:87) and the api-other-and-feedback part: they do not read differently for this change beyond what was run. Hosted CI is the proof.
- The full infra unittest discover and validate.sh (only the repo-wide hidden-characters scan was run).
- Jira: no ticket exists. A records pass will file it and cite the PR.

## Resources
Containers g1599-mssql and g1599-azurite were started per run on 10190/10191 and removed by name (0 left). 10190-10199 is free at the end (0 listeners; unfiltered 12). The clone, worktrees and logs are under the session scratchpad only. Nothing was written to the HPSM-POC project folder or HOME. No push, PR, Jira, mail, board or az. The only hosted reads were gh api -X GET and git fetch/ls-remote.
