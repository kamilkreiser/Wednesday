# Gate verdict: Secuura Platform K PR #1522 (KS-1512 option A), SONNET tier 2

**VERDICT: GO WITH NOTE.** Majors: 0. Minors: 3 (+1 nit). Nothing in the diff is wrong; the notes are an overclaim in the code comment/PR text about "never hangs", and one untested guard.

Gated 2026-10-13 ~05:1x-05:30 AEDT. Findings only; nothing in any project was written (see "Boundaries kept").

## 1. Head under test and how obtained

- PR head `119d362050666949e8b564dd3c175b5661f237a5` (asserted equal to the commissioned sha: `git rev-parse pr1522` printed exactly that). develop `425ad3e00ae40ddbce6ead62c127c610e2e67a16` (asserted equal).
- Obtained: `git clone --shared` of the project checkout into my scratchpad, then `git fetch origin refs/pull/1522/head:pr1522 develop:dev` in that clone, using the project's `core.sshCommand` / `remote.origin.url` (read, not changed in the project). No write verb was run in the project checkout.
- Diff `dev...pr1522` (git diff --stat): 2 files, +344 -10 (K's claim confirmed): `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` (46 lines changed) and the new test `.../src/__tests__/ks1512-platform-audit-log-pages-the-upstream-past-its-200-clamp.test.ts` (308). Note `merge-base(dev, pr1522)` is `250596098fa9`, not 425ad3e0: the branch was cut from an older develop.
- Landing tree: `git cherry-pick 499f11964fc0 119d36205...` onto `dev` (425ad3e0) gives commit `83e1675f6`, tree **`2703f08c1ad0`** (matches K's stated landing tree exactly; control: an independent cherry-pick by me reproduced the tree id).
- Environment disclosure: node_modules came from the project checkout by symlink; `@secuura/shared` was rebuilt (`tsc`) inside my clone. **My first suite run was wrong** (19 failures, all `Missing "./documents/default-type" specifier in "@secuura/shared"`): the project checkout's node_modules resolved `@secuura/shared` to the project's stale `dist`, which is 3 commits behind origin/develop. That was my harness, not the PR; I rebuilt shared in the clone, rebuilt the `@secuura` links to point inside the clone, and re-ran everything. All numbers below are from the corrected run. Evidence of the bad run is not kept (superseded; the retraction is this paragraph).

## 2. Ruling, item by item (FOUND = read in the diff / TESTED = ran / HOW)

All line numbers are `platform.ts` at the PR head.

| Ruling item | Found in code | Tested |
|---|---|---|
| One budget = the existing per-call timeout | `:402` `const deadline = Date.now() + UPSTREAM_TIMEOUT_MS` (`:128`, env `PLATFORM_UPSTREAM_TIMEOUT_MS`, default 8000). No new constant for time; the only new constant is the window size 200 (`UPSTREAM_AUDIT_WINDOW`), which mirrors the upstream's own clamp and is not a budget/cap | Mutants M2, M3, M5, M8 (below) all redden |
| Each window's timeout = min(8000, remaining) | `:415` `Math.min(UPSTREAM_TIMEOUT_MS, remaining)` passed as `fetchWithTimeout`'s 3rd arg (existing parameter, `:143-147`) | M1 (timeout not cut) reddens H and L |
| No window starts once nothing is left | `:407` `if (remaining <= 0) throw ...` before the request is built | **Only partly pinned**: mutant M9 (guard removed) survives all 18 cells; see Minor 2. Behaviour on the real code is correct (probe P3: upstream saw exactly 1 request) |
| Spent budget DISCARDS the platform half, never a partial page | `platformEntries` / `platformTotal` are assigned only after the loop (`:424-425`); any throw inside lands in the existing empty `catch` | M4a (break, keep partial) reddens M; M4b (partial kept on failure) reddens F, H, L, M |
| Single-window page behaves as the old route | `want = min(200, overfetch)`, `offset = 0` gives the same request as before (`limit=overfetch&offset=0`); first-window parse: `total` and the entries fallback produce the old `platformEntries`/`platformTotal` | cells "one window" (`limit=50&offset=0` -> exactly `[{50,0}]`), "exactly 200", K1, K2, first-window-fails; and probe P2 on develop vs landing: both 200/50 rows/total 600/3.0 s, 1 request |

## 3. What the caller sees on a degrade (K's identity claim)

- Read from the code: on any throw (timeout, HTTP-level failure with unparseable body, destroyed socket, non-list later window, spent budget) the `catch` is the same empty catch as before, so `platformEntries = []`, `platformTotal = 0`; the response is `res.json({ entries: paginated, total: platformTotal + appTotal })` unchanged, status 200, rows = audit_logs rows only, total = audit_logs total. **Confirmed identical to the old failed-window path.**
- Tested: cells F (500 and socket destroy on window 2), H, L, M and K2 compare against an `appOnly()` oracle with status 200. Probe P5/P3 also return `200, n=25, total=340` (app-only) after a stall.
- Non-degraded path: headers, ordering (`sort` by `created_at` desc), `slice(offset, offset+limit)`, and the app-side query (`LIMIT overfetch`) are untouched by the diff (read: the diff touches only the platform-fetch block and one constant). The one intended change is that for `limit+offset > 200` the platform half now contributes more than 200 rows (that is the ticket). `total` was already `platformTotal + appTotal`; it is now consistent with the rows served. I did not run a develop-vs-landing wire diff on the non-degraded path (probe P3 differs by design: develop has no budget so it serves the stalled body, total 640, while landing degrades, total 340); the evidence for "nothing else changed" is the code read plus the oracle-based cells A/B/C/D/E/G, all green on landing and (per K, and per the fact A and B are named RED) red on develop.

## 4. Real-time cells and flake

- Instrument: `vitest run --reporter=json` per-test `duration`, new test file only.
- 6 clean runs: 6/6 green, 18/18 each. Durations (ms) across the 6 runs: H 2004-2011, I 1605-1613, L 2003-2005, M 2204-2205, K1 1502-1507, K2 2003-2006. Spread <= 11 ms.
- 4 stressed runs (84 `yes` CPU-spin processes on a 28-core machine, 3x oversubscribed; started then 2 s settle): 4/4 green, same durations (H 2004-2009, I 1606-1617, L 2003-2004, M 2203-2206, K1 1503-1505, K2 2003-2004). Worst jitter seen 17 ms.
- Control for "the stress was real": weak. The load average I sampled 2 s after launch (4.4) still lagged and I did not re-sample under load, and the durations barely moved. So the claim is "no flake observed in 10 runs, 4 under 3x CPU oversubscription", not "robust under all load".
- Margins: lower side (a completing page must finish before the budget): cell I 1605 vs 2000 = ~395 ms; K1 1504 vs 2000 = ~496 ms. Upper side (degrade must not take longer than budget + 900): observed 2004-2011 vs 2900. K's "400 ms margins" confirmed. The worst jitter seen is ~17 ms, ~23x smaller than the tightest margin. **Adequate for CI as written; a fake-timer form is not required**, though the file adds ~11 s of wall time to the suite (tests 11.42 s of 12.3 s in the single-file run) and a CI box 10x slower in timer scheduling than this one would break cell I first (it would go red, not silently green).
- Gateway suite twice on each tree (full `vitest run`, JSON reporter): develop 117 files / 1128 tests / 1128 passed / 0 failed, twice; landing 118 files / 1146 / 1146 / 0 failed, twice. Delta = +1 file, +18 tests = the new file. Zero flakes in 4 full-suite runs.
  - Control that this instrument could fail: my first (broken-env) runs reported 19 failures on both trees; the instrument reads failures.

## 5. Landing tree: lint, tsc, test-types

- `npx eslint src` (api-gateway): landing 35 problems (0 errors, 35 warnings); develop 35 problems (0 errors, 35 warnings). Same.
- `npx tsc --noEmit -p tsconfig.json`: landing rc 0; develop rc 0.
- `node scripts/typecheck-tests/check.cjs services/api-gateway`: landing "153 files, 118 under __tests__; 35 errors: 35 in the baseline, 0 new; 0 stale"; develop "152 files, 117 under __tests__; 35 in baseline, 0 new". Same baseline.
- Controls: appending a type error to `platform.ts` made tsc exit 2 (TS2322 + TS6133); appending `debugger` made eslint exit 1 (2 errors). Both instruments can fail. Controls were reverted (`git checkout --`), clone tree clean.
- Not run: `check:test-types` for `services/auth` (the root script runs both; PR touches gateway only).

## 6. Mutants (killed by me, on the landing tree)

Method: python mutator with `assert source.count(anchor) == 1`, `assert mutated != original` and a post-write marker check ("landed=True" below), then `vitest run` on the new file, JSON reporter; source restored after each. Control: no-mutation run = 18/18 green.

| Mutant | Reddens |
|---|---|
| M1 per-window timeout not cut (`Math.min(...)` -> `UPSTREAM_TIMEOUT_MS`) | H, L (2 red) |
| M2 no budget (`deadline = now + 1e9`) | H, L, M |
| M3 half budget (`UPSTREAM_TIMEOUT_MS / 2`) | I, K1 (the controls that a good page is not cut) |
| M4a spent budget `break`s (keeps partial) | M |
| M4b partial rows kept after a failure | F, H, L, M |
| M5 budget resets per window | H, L, M |
| M6 window size 199 | C, D, E, "exactly 200" |
| M7 `total` ignored in the stop rule | G |
| M8 budget doubled | H, L, M |
| **M9 `remaining <= 0` guard removed** | **none: survives (18/18 green)** |
| CONTROL no mutation | none |

K's four named budget mutants (per-window timeout not cut, no budget, half budget, keep partial rows) are all killed; the reddening cells are different cells per mutant, as K said. Read-why check: each red above is an assertion failure in the named cell (the JSON `failureMessages` were from the cell's own `expect`, not a parse/throw; I did not paste each message). M9 is the one gap, see Minor 2. M4a is killed only by cell M.

## 7. K's residual (stalled body) and what the PR did to it

- Read `fetchWithTimeout` (`:143-160`): `setTimeout(abort)` is cleared in `finally` as soon as `fetch()` resolves, which is at **response headers**. `r.json()` (`:416`) is awaited outside any timer. **Confirmed.**
- It is wider than K stated ("last window"): it applies to **every** window, because the budget is only consulted at the top of the loop. Measured (stub holds back the BODY after flushing headers; budget 2000 ms; instrument: wall time around the HTTP call, test-file copy in my scratch clone with a body-delay hook):
  - P5: first (non-last) window body stalled 8 s on a deep page -> response after **8014 ms**, 200, 25 rows, total 340 (app only: discarded correctly, but only after the whole stall).
  - P4: last window body stalled 8 s (2-window page) -> **8006 ms**, 200, platform rows served in full (n=100, total 600).
  - P1: last window body at 1.5x budget (3.0 s) -> **3021 ms**, 200, platform rows served (n=100). I.e. a spent budget does NOT discard when the overrun is in the last window's body: the platform half is kept and returned late.
  - P2 (the old single-request shape, on BOTH develop and landing): body at 1.5x budget -> 3004 / 3002 ms, served in full on both trees.
- Verdict on the residual: **the same as before, not worse** (old route: one request, body unbounded; new route: same per window, and a stalled body can no longer be waited on repeatedly across many windows beyond the first stall plus the budget check, so the worst case is one stall, not 26). **Not better**: the code comment at `:401` says a slow upstream "never hangs" the page, which is true for slow responses and false for a stalled body. See Minor 1.

## 8. Other diff review (item 7)

- Error handling: all failure modes still fall to the single empty `catch` (`:425`+). A later window that is "not a list" is deliberately thrown (`if (collected.length > 0 && !Array.isArray(...)) throw`), a first non-list window stays an empty first window (same as old). Bounded loop: each iteration either adds at least one row or breaks (`rowsInWindow.length === 0`), at most `overfetch` (<= 5200) iterations, 26 when the upstream honours 200; wall-bounded by the budget except for body stalls (item 7).
- Env read at module load: `UPSTREAM_TIMEOUT_MS` is the pre-existing `:128` constant; the PR adds no new env read. A garbage value gives NaN: `deadline` NaN, `remaining <= 0` false, `Math.min(NaN, NaN)` = NaN, `setTimeout(NaN)` fires ~immediately, so every window is aborted -> the same degrade as before (the old default argument is the same NaN). `PLATFORM_UPSTREAM_TIMEOUT_MS=0`: guard throws before any request; the old route aborted at ~0 ms. Equivalent. Not executed (code reading only).
- Logging: the PR adds no logging; the swallowed `UpstreamTimeoutError` message carries the upstream URL without query string and is discarded by the empty catch. No tokens or tenant data are logged or emitted by the diff. (`authHeaders(req)` is unchanged.)
- Cost: a deep page now issues up to 26 sequential upstream requests per call instead of 1 (bounded by the existing KS-5 offset clamp and 8 s budget). That is the intended trade; there is no rate/amplification control beyond the budget. Not load-tested.

## 9. Findings

**Minor 1 (severity: low; the stalled-body residual is wider than disclosed and the comment overclaims).**
- Where: `platform.ts:401` (comment "never hangs it"), `:416` (`await r.json()` outside any timer), `:143-158` (`clearTimeout` at headers).
- Oracle: Purpose/Explainability (the ruling and the code comment say the budget bounds the page).
- Reproducing shape: upstream sends headers, then stalls the body 8 s -> caller waits 8014 ms (P5, any window) / 8006 ms (P4, last window); with a never-ending body, the request never returns (not run to infinity; would need a harness timeout).
- Same as the pre-PR route (P2 on develop). Not a regression.
- Minimal fix (owner's call; Wednesday should decide whether it is in scope for this ticket): bound the body read by the remaining budget, e.g. keep the `AbortController` live until after `r.json()` in the audit-log block, or `Promise.race` the body read against a `remaining` timer; at minimum, soften the comment at `:401` to say "slow responses", and record the body-stall caveat (and that it applies to every window, not only the last) in the ticket. Regression test to add: the P5 shape with a stalled body in a non-last window must degrade within budget + margin.

**Minor 2 (severity: low; test gap, behaviour correct).** The "no window starts once nothing is left" guard (`:407`) is not pinned by any cell. Mutant M9 (guard removed) leaves 18/18 green; with it removed the upstream receives a second request that is aborted at once (probe P3: `upstreamCalls` 2 vs 1). Fix shape: in cell M add `expect(calls.length).toBe(1)` (the stub already records calls); regression test described in prose only, not written.

**Minor 3 (severity: low; ruling-literal gap, needs Wednesday's reading).** When the overrun happens in the LAST window's body (or the last window simply answers after the deadline), the platform half is kept and served late (P1: 3021 ms with 100 platform rows, budget 2000 ms). Wednesday's ruling says "when it is spent, the platform half is DISCARDED". Today the discard is applied only when another window would be needed. If the ruling is to hold literally, a post-loop `if (Date.now() >= deadline) throw` would discard a late final result (it would not bound time, see Minor 1). If the intent is "bounded and never partial", the current behaviour is arguably fine (rows are complete, never partial). Flagged as a ruling-interpretation question, not a defect.

**Nit.** Test cell G's second assertion (`calls.every(... || c.offset === 200 || === 100 || === 0)`, test file line 214) cannot fail for any plausible offset; the first assertion (`r.ids` equals the oracle) is the real check and M7 shows it works.

## 10. What was NOT tested (Rule 2)

- No live server, box, or real tenant-provisioning; the upstream is the test's own stub on 127.0.0.1 (it mimics the real clamp as the test file's comment says; I did not re-read `services/tenant-provisioning/src/index.ts` to confirm the clamp and `total` semantics, so that is assumed from the comments).
- Concurrency across windows: rows inserted/deleted between windows shift offsets (duplicate or skipped row at a window boundary); offset-paging race is inherent in the design and was neither tested nor reported by K.
- Never-ending body (infinite hang) not run; only 8 s stalls.
- Memory/latency under 26-window pages with real payload sizes; no k6/load test.
- `limit`/`offset` validation (KS-1359) and the KS-5 clamp: read, not changed by the diff, not re-tested.
- Auth/role matrix of `/api/platform/audit-log` (super_admin): unchanged by the diff; the test stubs auth.
- The push hook's 13/16 legs and K's "red-first 3 of 18 red (H, L, M)": I did not rebuild the pre-fix tree, so red-first is K's claim. (I note H, L, M are the cells that M1/M2/M5 mutants reddened, which is consistent but not the same test.)
- `services/auth` test-types, other services, frontend: not touched by the PR, not run.
- The whole-repo test suite, other than the api-gateway package.
- Real-timer margins under non-macOS CI hardware or Docker CPU limits.
- Behaviour with garbage / zero `PLATFORM_UPSTREAM_TIMEOUT_MS` (code reading only).

## 11. Evidence files (this folder)

`ev_new_run1-6.json` (clean repeat runs), `ev_stress_run1-4.json` (stressed), `ev_dev_suite1-2.json` and `ev_land_suite1-2.json` (+ `.log`) (full gateway suite), `ev_lint_tsc.log` (eslint/tsc/test-types + controls), `ev_mutants.log` and `ev_mut_*.json` (mutant runs), `ev_probes.log` (body-stall probes P1-P5).

Boundaries kept: no write verb in the project checkout or any other project; the clone, probe test file, mutants and temporary stress processes lived in the session scratchpad; the CPU-spin processes were killed (`pgrep -x yes` = 0 afterwards); no push, no GitHub/Linear write; the only network contact was the commissioned `git fetch` of `refs/pull/1522/head` and `develop` over the project's deploy key. No secrets appear in this file.
