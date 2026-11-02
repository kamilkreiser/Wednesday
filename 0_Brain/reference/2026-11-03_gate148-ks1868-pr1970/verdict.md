# QA gate 148 (TIER 1, Opus, round 1, RESUMED): Secuura PR 1970, KS-1868 api-gateway middleware

**Verdict: GO WITH NOTES. Fail-open question: HOLD-FOR-KAM (do not merge until Kam rules on the card). The measurement does not block the PR itself.**

- Subject: PR 1970 (Refs KS-1868), head `b078c7f49095e60c91324dc914b3cc3a6d20cba4`, build base `4d1ab2cb6574e2b221353ac3a1de56d515711aaf`. Author Seat R 76th, raised by Seat R 77th.
- Head pin re-read by `ls-remote` at resume (2026-11-02 22:34:19Z): `refs/pull/1970/head` = b078c7f4 (unchanged since gate start 22:12:35Z). develop = `4deb2fc10b7d852194183c08e86e2ecacb7231db`.
- Resume note: the first gate-148 agent died at ~09:2x AEDT. On resume no process from it was running (ps and lsof: nothing with this workdir in its command line or cwd). Its probe matrix, suites, static checks, mutants and ratchet had all finished. Each has a `.done` marker, rc lines, and an sha-verified restore. I re-read every script and log and accept them, with two exceptions. (a) The `bf_arm` rows in `probe.jsonl` planted the lockout under the wrong key (`secuura:bf:`, while the guard reads `secuura:gateway:bf:`), so their "planted=401" is not a valid measurement. The corrected re-run is `probe_bfarm2.jsonl` and is the one used below. (b) The merge-tree was against develop ddd770ca, so I recomputed it onto 4deb2fc1. I also added a merged-tree run (see the merge-tree section) and a check that the docs advisory was already present before this PR.

## Answer to the gate questions

**Q1, the class bar: MET at all four changed catches.** With an unreadable thrown value, head behaves exactly as base does with an ordinary Error, in status, headers, request reach, limiter counter and log shape. The only difference is the `error` text: it reads `unreadable thrown value`, or `Symbol(s)` where the old code printed `boom`.

**Q2, fail-open.** Two sites are already fail-open for an ordinary Error at base and stay so at head (pre-existing): the brute-force guard and the limiter header-write. This PR NEWLY makes those same two sites fail open for unreadable values, where base failed closed by accident:
- Brute-force guard: at base the request hung with no answer and an unhandled rejection was raised.
- Limiter header-write: at base the request got a 500 through errorHandler.

This PR also CLOSES one fail-open. The limiter's Redis-error path at base let an uncounted request through for unreadable values; at head the degraded ceiling holds. In practice, nothing in production can throw an unreadable value at the two newly-open sites:
- ioredis and Node's `res.setHeader` throw real Error instances.
- The gateway brute-force guard is never armed: no production code writes its key.

The new fail-open is therefore a change in behaviour on paths no real dependency drives. It is not a new hole that can be exploited. It is still a fail-closed → fail-open change at two sites, and that is exactly the KS-1256 class Kam ruled on, so it goes to Kam.

## Findings

### G148-F1: class bar met at all four catches (PASS)
- **FOUND:** Head with an unreadable value equals base with an ordinary Error at every site:
  - **bf (security.ts:194):** 200 `{helper:false}` and one `[BruteForce] Redis error, allowing request` line, for revokedProxy, getterThrows, msgNullProto and msgSymbol, at head in test and production modes.
  - **rl_redis (logDegraded):** `[200,429,429]`, remaining `0,0,0`, handler reached once, one DEGRADED warn line.
  - **rl_hdr (rateLimitEnforce.ts:297):** `[200,200,200]`, no X-RateLimit headers, handler reached 3 times, the counter in Redis at 3, three error lines.
  - **audit (audit.ts:332):** post and post2 both 200, two warn lines each carrying `path:/api/things`, zero unhandled rejections.

  At head, no cell produced an unhandled rejection, an uncaught exception or a shutdown.
- **TESTED:** 78-row probe matrix: base/head × 4 cells × 7 value kinds (none, ordinary, plainString, revokedProxy, getterThrows, msgNullProto, msgSymbol), plus the bf_arm, rl_hdr_committed and rl_hdr_badmeta cells, plus 16 production-mode cells.
- **HOW:** `scripts/probe_child.ts` loads the REAL security.ts, rateLimitEnforce.ts, audit.ts, services/redis.ts, winston logger, errorHandler and the @secuura/shared unhandledRejection handler (mode survive), behind a real express server reached with real HTTP. `ioredis` is replaced by a single-Map stand-in that can reject with the cell's value, and the audit DB query is replaced. Base is a byte-copy of 4d1ab2cb's three files, swapped in at module resolution. Controls:
  - The `none` cells show the limiter refusing (`[200,429,429]`) and the guard attaching its helper.
  - The base hostile cells DO fire (unhandled rejections at bf and audit, 500s at rl_hdr, an uncounted request at rl_redis). This shows the instrument can see a divergence.

### G148-F2: two sites NEWLY fail open for unreadable values (MEDIUM, approval-class → Kam)
- **FOUND:**
  - **rl_hdr (header-write throws):** base revokedProxy/getterThrows gives `[500,500,500]` and the handler is reached 0 times. Head gives `[200,200,200]` and the handler is reached 3 times: unlimited, the same as base with an ordinary Error.
  - **bf (Redis read throws):** base revokedProxy/getterThrows gives status 0 (no answer, socket hung until the client's 1.5s abort) plus an UNHANDLED REJECTION. Head gives 200 and the request goes downstream.
  - **bf, with a lockout planted under the guard's real key (`secuura:gateway:bf:127.0.0.1`):**
    - no fault: 429 (positive control);
    - with an ordinary Redis Error: 401, so the lockout is bypassed at base AND head (pre-existing);
    - with revokedProxy: base gives 0 (hung), head gives 401 (bypassed).
  - msgNullProto and msgSymbol were already fail-open at base (they did not throw there).
- **TESTED:** `probe.jsonl` (bf, rl_hdr in test and production) and `probe_bfarm2.jsonl` (planted lockout, base and head).
- **HOW:** Same harness as F1. Base's closed outcome for these values is accidental: the catch itself throws, so the async middleware rejects and reaches `next(err)` → 500 (rl_hdr), or the async guard's rejection is never handled → the socket hangs (bf). It is not a deliberate refusal.

### G148-F3: in practice the new fail-open cannot be reached from production dependencies (INFO, the premise of the card)
- **FOUND:**
  - The gateway brute-force guard never arms. In production code nothing calls `req.bruteForce.recordFailure` or writes `secuura:gateway:bf:*`; `git grep` on pr1970 finds the writer only inside security.ts's own helper. Twelve failed logins (downstream 401) leave zero bf keys at base and head. The real lockout lives in the auth service (`services/auth/src/services/accountLockout.ts`, `passwordLoginGate.ts`), which this PR does not touch.
  - The limiter header-write's real throwers are Node's own `ERR_HTTP_HEADERS_SENT` and `ERR_INVALID_CHAR`. Both are ordinary Errors and fail open at BASE already. Measured: `rl_hdr_committed` gives `[202,202,202]` and `rl_hdr_badmeta` (connector `rateLimit: '1\n'`) gives `[200,200,200]` unlimited, at base and head alike.
- **TESTED:** bf_arm cells; `git grep -n -E 'BruteForceData|gateway:bf|recordFailure\('` over services and packages; rl_hdr_committed and rl_hdr_badmeta cells.
- **HOW:** Positive control for "the guard would enforce if armed": the planted lockout returned 429. The grep's positive control is that it does find the definition sites and the auth service's own recordFailure callers.

### G148-F4: pre-existing fail-open for ordinary Errors, NOT introduced by this PR (MEDIUM, pre-existing, for Kam's KS-1256 context)
- **FOUND:** Base and head are identical here:
  - The guard lets a login through on any Redis error, including through a live lockout (401 instead of 429).
  - The limiter lets a machine caller through unlimited whenever writing the headers or the 429 throws.
  - In particular, a connector record whose `rateLimit` holds a header-invalid string (`'1\n'`) makes that connector permanently unlimited. That is reachable through data, not through a fault.
- **TESTED:** bf ordinary, bf_arm2, rl_hdr ordinary/plainString, rl_hdr_badmeta, at base and head.
- **HOW:** As F1/F2. Not fixed here and not in scope for KS-1868. It deserves its own ticket if KS-1256 (fail closed) applies to it.

### G148-F5: the PR's tests pin the fail-open behaviour (LOW)
- **FOUND:** The mutant that makes the guard fail CLOSED (503 instead of `next()`) and the one that makes the header-write fail closed (503) are both KILLED, by the control cells C1/C2 and C3/C4. A future KS-1256-style fail-closed fix will have to change these tests deliberately. They encode "fail open" as the expected behaviour.
- **TESTED:** Mutants M6 bf and M6 rl_hdr (`logs/mutant_bf_M6.log`, `logs/mutant_rl_hdr_M6.log`).
- **HOW:** `scripts/mutants.py` changes product code only, never the tests, and sha256-restores after each run.

### G148-F6: rl_redis, a fail-open CLOSED by this PR (POSITIVE)
- **FOUND:** At base, a revokedProxy or getterThrows Redis rejection makes `logDegraded` throw inside the try. Control falls to the fallback catch, `outcome = null`, and the request goes through uncounted (`[200,200,429]`, handler reached 2 times). Head gives `[200,429,429]`, the same as an ordinary Error.
- **TESTED:** rl_redis × 7 values × base/head, plus production mode.
- **HOW:** As F1.

### G148-F7: one unguarded thrown-value read remains in a changed file (LOW, residual, cannot be reached)
- **FOUND:** In rateLimitEnforce.ts, the `fallbackErr` catch (in-memory fallback ALSO failed) still reads `fallbackErr instanceof Error ? fallbackErr.message : String(fallbackErr)` without a guard. At head, the only things that can throw into it are `logDegraded` (now guarded) and `countInMemory` (pure arithmetic), so no unreadable value can reach it. The READY mail already discloses "the other KS-1868 sites" as not covered.
- **TESTED:** Source read of pr1970 rateLimitEnforce.ts lines 268–290. Not exercised dynamically.
- **HOW:** Read.

### G148-F8: the READY mail's measured claims match the gate's own measurement (INFO)
- **FOUND:** The following all match the gate's runs:
  - red-first counts: 4/8 audit, 4/8 bf, 6/10 rl;
  - api-gateway 143 files / 1471 tests → 146 / 1497, all passing;
  - ratchet 25/25/0 new;
  - eslint 0/0;
  - the base/head outcomes for every cell in the fail-open table (bf base hostile = no answer; rl_hdr base hostile = rejected; rl_redis base hostile = second request uncounted; audit base hostile = no log line).

  The gate closed the READY's two stated gaps: it ran the real winston logger and it compared base against head.
- **TESTED/HOW:** The logs listed under Figures.

## Figures
- **Suites (vitest 4.1.12, `--root` api-gateway):**
  - head, new files: 3 files / 26 tests pass;
  - head, whole service: 146 files / 1497 tests pass, rc 0;
  - base product + base tests (new files held out): 143 / 1471 pass, rc 0;
  - red-first (new tests on base product): audit 4 failed / 8, brute-force 4 failed / 8, rate-limit 6 failed / 10.

  Every product file was sha-restored OK.
- **Mutants:** 28 run, 28 KILLED, 0 SURVIVED. Seven per site (bf, rl_log, rl_hdr, audit): M0 revert to the unguarded read, M1 inner try dropped, M2 always the constant, M3 no String(), M4 inner catch rethrows, M5 different constant text, M6 a site mutation (bf/rl_hdr fail-closed 503, rl_log ceiling dropped, audit log drops path). Every kill came from an AssertionError, not a timeout, and every restore was OK. Table: `logs/mutants_table.log`.
- **tsc / ratchet:** typecheck-tests ratchet at head examines 182 files, 25 errors, all 25 in the baseline, 0 new, 0 stale, rc 0. At base it examines 179 files, 25/25, 0 new, rc 0. The tsconfig.test set of 25 errors has the same file list at base and head. Service `tsc --noEmit` at head: 0 errors.
- **eslint:** 0 problems on head's 3 product + 3 test files, and 0 on base's product files. Positive control: a planted file with an unused variable and a `debugger` statement gave 2 problems, rc 1. The planted file is quarantined in `logs/_quarantine/`.
- **docs-fragments check:** OK, rc 0 (flow 117 legacy + 112 new, cheat 112 + 112). Positive controls: an unclosed `<div>` planted in each PR fragment gave FAIL rc 1 (flow and cheat separately), and both restores were sha-OK. The one cheat ADVISORY (committed page vs render at line 6235, a pmatrix table) is PRE-EXISTING: it repeats identically with the PR's two fragments held out (`logs/frag_check_without_pr_fragments.log`, 111 new), and neither PR fragment contains a pmatrix table.

## Merge-tree onto develop 4deb2fc1
**CLEAN, and the merge changes exactly the PR's own paths.**
- develop moved from 4d1ab2cb to 4deb2fc1: 8 commits and 48 paths. The overlap with the PR's 8 paths is 0.
- `git merge-tree --write-tree 4deb2fc1 b078c7f4` → rc 0, tree `d66accd0c08c91c50c30019178d4cfe010920ed6`. The diff of the merged tree against develop touches exactly the PR's 8 paths, and every merged blob equals the head blob.
- None of security.ts, rateLimitEnforce.ts or audit.ts changed on develop since the merge base. Script: `scripts/mergetree_r2.sh`; log: `logs/merge_tree_r2.log`.
- Positive control, run with `git merge-file` on scratchpad copies: develop's security.ts with the PR's own line edited differently → conflicts=1, so the instrument fires. The real develop file → conflicts=0, with output byte-equal to head.
- develop's only api-gateway changes are `services/redis.ts` (KS-1868 Redis listener and connect catch) and its new test. I overlaid both onto the head checkout to stand in for the merged service:
  - whole api-gateway suite: **147 files / 1506 tests pass, rc 0**;
  - merged probe cells (`logs/probe_merged.jsonl`): bf revokedProxy/getterThrows 200; rl_hdr ordinary/revokedProxy/getterThrows `[200,200,200]`; rl_redis all three `[200,429,429]`; audit all 200 with the expected warn lines; bf_arm planted 429, then ordinary 401, then revokedProxy 401. These are the same outcomes as at head.
  - The merged `bf ordinary` cell hit the probe's 25 s watchdog once. Its output stops after the Redis init lines, before any request was sent. It passed 3 of 3 re-runs (200, `{helper:false}`, one log line; `logs/probe_merged_bf_ordinary_rerun.*`). I read it as a one-off harness start-up stall, not product behaviour; it is not proven.
  - The first overlay attempt's probes died with tsx IPC `listen EINVAL` because the pipe path under the scratchpad TMPDIR was too long. That attempt is quarantined in `logs/_quarantine/merged_attempt1/` and was re-run with the default TMPDIR.

  Every overlay was sha-restored, and `git status` shows 0 lines.

## NOT TESTED
- A real Redis, a booted gateway (index.ts wiring), and the auth service's own lockout. The guard and limiter were mounted directly on express. The limiter sat behind a stand-in for `authenticateToken` that calls it exactly as `continueThroughLimiter` does.
- Node 24 or any LTS release. Every run used host Node v26.
- Multiple replicas. The rl_redis degraded path was run as one process, so "limit × replicas" was not measured.
- The hung-socket cost at base for bf (how long a production socket hangs, and the server timeout). The probe client aborted at 1.5 s.
- `shutdowns` stayed empty in every cell, with no positive control: mode `survive` never calls shutdown, so that zero shows only that survive mode was honoured. A mode-`exit` run was not done.
- The four platform suites and the PR's pre-push hook legs 3, 4 and 8 (the READY mail's PREFLIGHT INCOMPLETE). The gate did not run them.
- The other KS-1868 sites outside these three files, and the residual read in F7 was not exercised dynamically.
- Whether production connector records can actually hold a header-invalid `rateLimit` (F4): not checked against schema or data.
