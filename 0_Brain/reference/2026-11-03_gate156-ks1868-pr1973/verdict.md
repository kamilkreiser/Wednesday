# QA GATE 156: Secuura Platform K PR 1973 (KS-1868, governance db.ts), TIER 1, round 1

**Verdict: GO WITH NOTES. Nothing has to be fixed before merge.**

The class bar holds at both sites. For every unreadable value I tried (13 kinds x 3 paths, one process per cell, real db.ts and real dbLog, Node's default crash behaviour left on), head ends in the same state as base does for an ordinary Error: the process stays up, the flag is true, initDb returns true, and the log line is written.

Base exposure is wider than the author's table says. At base, 7 of 13 kinds crash the process from the pool listener (the author counted 4 of 8), and 5 of 13 crash it through the ready-hook catch (the author counted 2 of 8). The extra kinds are a BigInt message, a message whose toJSON throws, and a message getter that returns a revoked Proxy. They break dbLog's JSON.stringify, not the `.message` read. Head guards all of them.

Every figure the author gave matched when I measured it again. Two mutants survive, both LOW (G156-F3).

Subject: PR 1973 head `e16104beec024d4aa2fdf78ab2d1f92631272e2f`, parent `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6`, fetched by this gate from GitHub `refs/pull/1973/head` into its own `git clone --shared` (`repo/`). Host Node v26.8.1, not Node 24.

## Answer to the TIER 1 question (availability flag)

**Who writes the flag:** `dbAvailable` is written only by `probeDb` (db.ts:115-124) and `closeDb` (:248). The PR changes neither.

**Who reads it, outside tests:**
- `getLinkedWalletAddress` (db.ts:214) throws "degraded mode" when the flag is false. Its caller `readLinkedWallet` (governanceService.ts:424) turns any throw into a 503.
- `governanceService.verifyDbReady` (:544) warns and returns when the flag is false.
- `scheduleRetry` (db.ts:127) uses it as a guard.

I found no other reader in governance src (`git grep isDbAvailable|dbAvailable`).

**Does the change make governance report AVAILABLE, or keep serving, where base would not?** For the unreadable kinds, yes: at base the process DIED (uncaught exception from the listener, or an unhandled rejection from `initDb(...).then` with no catch at index.ts:180), and at head it keeps serving with the flag true. Governance installs no `unhandledRejection` handler, so Node's default applies; I read index.ts and the shared exports to confirm. That head outcome is identical, cell for cell, to what base has always done for an ORDINARY Error:
- flag true
- initDb returns true
- the wallet read goes to SQL
- one error line is logged

So there is no new fail-open relative to the ordinary-Error contract. Not un-flagging the DB when boot work fails is the pre-existing KS-382 design ("Boot work failing must not un-flag an otherwise reachable DB"). This PR leaves that design alone. It is the thing Kam would rule on if he wanted to revisit it.

**State paths:** I found no vote, proposal, stake, quorum or participant path that reads or writes state differently at head and base, for any value kind. The changed lines compute and log a `reason` string, and nothing else. `proposalCounter` is written only by `verifyDbReady`. `verifyDbReady` catches its own failures without rethrowing, so in production the db.ts ready-hook catch only sees a throw from verifyDbReady's own logger calls.

## Findings

**G156-F1 (INFO, positive): class bar holds at both sites for 13 kinds x 3 paths; base exposure wider than the author's table.**
- FOUND: Head behaves like base-with-ordinary-Error for every kind: exit 0, alive, flagAfter true, initDb `.then` true at boot, wallet read reaches SQL, exactly one line logged.
- FOUND: At base, the pool listener crashes the process (exit 1) for 7 kinds: null, undefined, revokedProxy, messageGetterThrows, bigintMessage, messageToJSONThrows, messageIsRevokedProxy.
- FOUND: At base, the ready-hook path crashes the process at boot AND on recovery-retry for 5 kinds: revokedProxy, messageGetterThrows, bigintMessage, messageToJSONThrows, messageIsRevokedProxy.
- TESTED: `harness/cell.js` and `harness/run_matrix.js` → `logs/matrix.tsv` and `logs/matrix.json`. I ran 78 child processes: base and head, three paths (pool / hookBoot / hookRecovery), 13 kinds.
- HOW: The real base and head db.ts were extracted by blob (75d140b0b and fb610b57, verified with hash-object) and transpiled verbatim with the clone's typescript. Only `pg` and `@secuura/shared` were replaced, through a Module._load stub. The stub Pool is an EventEmitter that emits 'error' from setImmediate, which is outside any caller's try, as pg-pool does. hookBoot mirrors index.ts:180 exactly (`.then`, no catch). hookRecovery makes the first probe fail and the retry succeed. dbLog is the real one; console.log is recorded.
- Positive controls: base cells crash (exit 1, with a stack in stderr). The ordinaryError, plainString and number42 cells are green at both versions.

**G156-F2 (INFO): logged text differs from base for some kinds, never the logged type or the outcome.**
- FOUND: Head writes text where base wrote nothing useful or crashed:
  - Symbol message: head logs `"Symbol(g156)"`; base dropped it.
  - message with a throwing toString: head logs the constant; base logged `{}`.
  - BigInt: head logs `"10"`.
  - toJSON-throws message: head logs `"[object Object]"`.
- FOUND: The `level`/`message` keys are unchanged. `error` is a string, or absent when undefined/null, the same as base for an ordinary non-Error value.
- TESTED and HOW: same matrix, log column.

**G156-F3 (LOW, test gap): 2 of 12 mutants survive. The PR's tests have no null/undefined cell at either site.**
- FOUND: P2 and H2 (`err?.message` → `err.message`) pass both the new test file (9/9) and the full suite (297/297). Under that mutant a null or undefined value would log `'unreadable thrown value'` instead of omitting `error`. It still does not crash, so the class bar holds either way.
- FOUND: The test also never asserts `isDbAvailable()` after the event. The listener-null case is exactly the one that crashes base, and it is not covered (only R1/R2 cover the listener).
- TESTED: `harness/mutants.py` → `logs/mutants.json`. Each mutant is applied as a single exact replace, the PR's new test file and the full governance jest suite run, and db.ts is restored by `git checkout --` with the blob sha asserted.
- HOW: 10 of 12 killed (P1, P3-P6, H1, H3-H6). Nice-to-have, not merge-blocking: a `null` cell at the pool listener, and an `isDbAvailable()` assert.

**G156-F4 (INFO, reachability, pre-existing, out of scope): in real pg, null/undefined/revoked-Proxy cannot reach the pool listener through the idle path.**
- FOUND: pg-pool 3.13.0 `makeIdleListener` runs `err.client = client` before `pool.emit('error', ...)`. For those values pg-pool itself throws first. Also, the bad client is `_remove`d BEFORE the emit, so the listener has no state to protect; it only logs. The head guard is still correct, and it covers values that can arrive: the getter-throws, BigInt and toJSON kinds pass `err.client =`.
- TESTED: read only (`node_modules/pg-pool/index.js:51-63`, pg 8.20.0).
- HOW: not executed against a real pg client.

**G156-F5 (INFO, tooling/hygiene): the held eslint warning reproduces.**
- FOUND: There is 1 warning: an unused `eslint-disable-next-line @typescript-eslint/no-require-imports` at test line 53. That rule is not reported there under this flat config. There are 0 errors, and base db.ts is clean.
- TESTED and HOW: `harness/eslint_run.js` (ESLint API, cwd = Blockchain/Dev so the flat config applies). Positive control: `debugger;` plus an unused const planted in db.ts gave rc 1 (no-debugger error, no-unused-vars warning), restored by sha. A test-only cleanup, not merge-blocking.

**G156-F6 (INFO, merge-tree): develop moved past Wednesday's pin.**
- FOUND: develop is now `66cbe4e52d5afadc9d13ca141200026cc68d5095` (m365-integration OAuth, KS-1868), not 4deb2fc10b7d.
- FOUND: `git merge-tree --write-tree` is CLEAN onto both:
  - 4deb2fc → tree 92aa14e4
  - 66cbe4e → tree 094d55ed
- FOUND: Against each develop, the merged tree changes exactly the PR's 4 paths. base..develop touches 32 files, none under governance. Between head and the 66cbe4e merge tree there are zero differences under services/governance, packages/shared, package.json and package-lock.json.
- TESTED and HOW: `scripts/mt.sh` → `logs/merge-tree.log`.

## Figures (re-measured; author's figure in brackets)

| Item | Result | Author |
|---|---|---|
| Red-first (base db.ts + new test) | 5 of 9 failed, all by assertion: R1 `toEqual` threw:true, R2/R5 `toBe` Symbol, R3/R4 `toEqual` ok:false. C1-C4 green, rc 1, 0 timeouts | [5/9, 4 controls] match |
| New test at head | 9/9 | [9/9] match |
| Governance jest, base | 17 suites / 288 tests, rc 0 | [17/288] match |
| Governance jest, head | 18 suites / 297 tests, rc 0 | [18/297] match |
| tsc, service tsconfig | 0 errors at base and head | [0] match |
| tsc, tests included | 0 at base (17 test files) and head (18 test files) | [0] match |
| eslint, changed .ts files | 0 errors, 1 warning; planted rc 1 | [0/1, planted rc 1] match |
| docs-fragments check | rc 0, "lint clean, render passes html_docs_check" | [rc 0, planted rc 1] match |
| Mutants | 12 run: 10 killed, 2 survived (P2, H2) | n/a |
| Recorder matrix | 78 cells. Head: 39/39 alive, flag true. Base: 17 of 39 dead (7 pool, 5 hookBoot, 5 hookRecovery) | [ALL HOLD; 4/8 and 2/8 base] holds, base wider |
| Install | `npm ci --ignore-scripts` rc 0, 1798 packages (`logs/npm_ci.log`) | n/a |

Notes on the figures:
- tsc: positive control was a planted TS2322 in db.ts, caught by both configs (rc 2). The tests-included config is `harness/tsconfig.tests.json`. It needs explicit `typeRoots` and `types: [jest, node]` because it lives outside the repo; the first two attempts without them gave spurious TS2304 and TS2688 errors.
- docs-fragments: the cheat ADVISORY at committed line 6235 is pre-existing and seen at earlier gates. Planted controls: an unclosed `<div>` in the flow fragment gave rc 1, and one in the cheat fragment gave rc 1. Restored by checkout; rc 0 after.
- Install: the PR lockfile is identical to develop 66cbe4e's, so G151-F8 did not reproduce here. packages/shared was built (rc 0).

## NOT TESTED

- Node 24 (host v26.8.1 throughout).
- A real Postgres or real pg client emitting through pg-pool's idle path (F4 is read, not run).
- A booted governance service or any HTTP route (the 503 mapping at governanceService.ts:424 was read, not driven).
- The four platform suites; any deploy.
- The real `verifyDbReady` as the hook: I read it and it catches its own errors, but I did not inject a throwing logger.
- docs-fragments `check` on the merged tree (develop added fragments). The numbers are provisional by design; the check was run at PR head only.
- `check --committed`.
- Mutants were judged by jest only; the recorder was not re-run per mutant.

## Housekeeping

- Every write stayed in this workdir: `repo/`, `harness/`, `scripts/`, `logs/`.
- The clone is at the PR head, `git status` clean, and the db.ts blob was verified after every swap.
- All runs were foreground and have finished; `ps` shows no process with this workdir in its command line, and `logs/cwd` is empty.
- I did not touch the Blockchain checkout beyond read verbs. The fetch from GitHub used the project's deploy key through a per-command `GIT_SSH_COMMAND`, inside this clone only.
