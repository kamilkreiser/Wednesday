# QA GATE 157: Secuura Platform K PR 1974 (KS-1868, billing db.ts), TIER 1, round 1

**Verdict: GO WITH NOTES. Nothing has to be fixed before merge. No fail-open question for Kam arises from this PR.**

The class bar holds at both sites. I ran 15 value kinds x 3 paths x 2 NODE_ENVs with billing's REAL `utils/logger.ts` (production redaction included), one process per cell, with Node's default crash behaviour left on. For all 90 cells, head ends in the same state as base does for an ordinary Error: the process stays up, the flag is true, initDb returns true, and the logged type is a string or absent. With the PRODUCTION hook (the real `loadChargeEventsFromDb`), head equals base exactly in 60 of 60 cells, because the changed catch is never reached with an unreadable value. The changed lines in production are defence in depth (F3).

Base exposure is wider than the author's figures. The pool listener crashes base for 7 of 15 kinds (author: 4 of 9). initDb rejects at boot for 5 of 15 (author: 2 of 9). The author does not mention that the recovery-retry path crashes the base process (unhandled rejection) for the same 5 kinds. The extra kinds are BigInt, a message whose toJSON throws, and a getter returning a revoked Proxy. They break the real logger's `JSON.stringify`, not the `.message` read.

Every figure the author gave matched when I measured it again. Two mutants survive, both LOW (F4), the same pair as gate 156.

Subject: PR 1974 head `35f1842fa7dee22125ce5fa3ba0dafcc5e32d713` (matches the pin), parent `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6`. This gate fetched it from GitHub `refs/pull/1974/head` into its own `git clone --shared` (`repo/`), using the project deploy key through a per-command `GIT_SSH_COMMAND`, inside the clone only. db.ts blobs: base `0f15dc241`, head `3f2d24d48`. Host Node v26.8.1, not Node 24.

## Answer to the TIER 1 money question (availability flag)

**Writers of `dbAvailable`:** only `probeDb` (db.ts:98-107) and `closeDb` (:177). The PR changes neither. The diff is exactly two hunks; each computes a `reason` string inside a try and passes it to `logger.error`.

**Readers, outside tests** (`git grep isDbAvailable|dbAvailable` over billing src, plus every importer of `./db`):
- chargeable-events.ts:
  - `ensureTable` (:56)
  - `loadChargeEventsFromDb`, the cache warm and the onReady hook (:113)
  - `createChargeEvent` INSERT (:165)
  - `processChargeEvent` (:208)
  - usage summary (:357)
  - `generateBillingReport` (:518)
- routes/webhooks.ts:
  - `claimEvent` (:62): with the flag false it throws `ClaimUnavailableError`, so the delivery is refused with a 503 and Stripe redelivers.
  - `/webhooks/replay` (:291): with the flag false it answers 503.
- Other importers of db: `creditGrants.ts` imports only `query`; `index.ts` imports only `initDb`/`closeDb`.

**Does head report AVAILABLE, or keep serving, where base would have stopped?** Yes, in two places:
- **Pool listener.** For BigInt, toJSON-throws, getter-throws and message-is-revoked-Proxy (plus null, undefined and revoked Proxy, which real pg-pool cannot deliver; see F5), base DIED with an uncaught exception from the listener. Head keeps serving with the flag true.
- **Recovery retry.** When the DB comes up late and the hook throws one of the 5 kinds, base DIED with an unhandled rejection from the retry timer (billing installs no handler; shared's `setupGracefulShutdown` has no consumer). Head keeps serving with the flag true.

At boot, base did not die either: initDb rejected, and `startup().catch` logged a misleading "running in degraded mode" warn while the flag was in fact true. Head resolves true.

In every case the head outcome is identical, cell for cell, to what base has always done for an ORDINARY Error: flag true, process up, one error line. The pool listener never un-flags. Boot work failing never un-flags; that is the KS-382 design ("Boot work failing must not un-flag an otherwise reachable DB").

**So there is no new fail-open relative to the ordinary-Error contract.** The only thing that changes is that a process crash (and an ACA restart, with a fresh re-probe) no longer happens. Kam would rule only if he wanted the KS-382 / pool-listener design itself revisited, and that is pre-existing.

**Money paths:** I read the money paths that touch db.ts:
- `DEFAULT_PRICING`, the amount in `createChargeEvent`, processChargeEvent, the usage/report totals
- the webhook claim and replay gates
- creditGrants' `query` import

I also confirmed that no other file in billing src imports `./db` (routes/billing.ts and services/stripeService do not). db.ts exports the same names at base and head, and the changed lines' only output is a log string. So no Stripe, credit or invoice path can read anything the change produces. I did not read every Stripe call line by line. The changed lines' only output is a log string. With the flag true, every one of those paths re-queries the DB per call, at head exactly as at base for an ordinary Error. **No amount, price, credit, invoice, Stripe call or webhook path behaves differently at head vs base for any value kind.**

**The author's gate question, the charge-events cache warm:** `loadChargeEventsFromDb` catches its own failures (:125). For an unreadable value, its catch's `err?.message` read, or the logger's `JSON.stringify`, throws an ORDINARY TypeError. So the hook either resolves or rejects with a readable TypeError, never with the unreadable value. With the real warm as the hook, head equals base exactly in all 60 cells (F3).

## Findings

**G157-F1 (INFO, positive): class bar holds at both sites, 15 kinds x 3 paths x 2 envs, with the real logger.**
- FOUND: Head behaves like base-with-ordinaryError in 90 of 90 cells (pool / hookBoot / hookRecovery x test / production): exit 0, alive, flag true. At boot, initDb resolves true. The same level and message line is logged, and the logged `error` is a string or absent. Head died in 0 of 150 head cells.
- FOUND: At base, in both envs:
  - The pool listener crashes the process (exit 1) for 7 kinds: null, undefined, revokedProxy, messageGetterThrows, bigintMessage, messageToJSONThrows, messageIsRevokedProxy.
  - The recovery retry crashes it (unhandled rejection) for 5 kinds: revokedProxy, messageGetterThrows, bigintMessage, messageToJSONThrows, messageIsRevokedProxy.
  - At boot, initDb REJECTS for the same 5 kinds, but `startup().catch` absorbs it with a misleading "degraded mode" warn. Process alive, flag true.
- FOUND: Production redaction still applies. An email-like message logs `***REDACTED***` at both sites (positive control: the redaction fired). The real logger threw in no head cell.
- TESTED: `harness/cell.js` and `harness/run_matrix.js` → `logs/matrix.tsv`, `logs/matrix.json`, `logs/matrix_verdict.json`. 300 child processes in total.
- HOW:
  - The real base and head db.ts blobs (hash-object verified) and the real `utils/logger.ts` were transpiled verbatim with the clone's typescript. Only `pg` and `@secuura/shared` were replaced, through `Module._load`. NODE_ENV was set before the logger loaded.
  - The stub Pool is an EventEmitter that emits 'error' from setImmediate, outside any caller's try, as pg-pool does.
  - The boot paths mirror index.ts:217-226 exactly: `startup()` awaits initDb, then `.catch` logs with the real logger.
  - hookRecovery fails the first probe and lets the retry (1 s) succeed.
  - The judge compares each head cell mechanically with the base ordinaryError cell of the same site and env.
  - Controls: base crash cells exit 1 with a stack in stderr. The ordinaryError, plainString, number42 and emailMessage cells are green at both versions.

**G157-F2 (INFO): log text differs from base for some kinds; the logged type and the outcome do not.**
- FOUND: Head writes the following, where base dropped the value, logged a raw object, or crashed:
  - `"Symbol(g157)"` for a Symbol message
  - `"10"` for BigInt
  - `"[object Object]"` for a toJSON-throws message
  - the constant for a message whose toString throws
- FOUND: Head is no worse for redaction. At base a non-string message was logged as a raw nested object, which `redactValue` (strings only, top-level only) never redacts. Head coerces it to a string first, so the email check now applies to it.
- TESTED and HOW: same matrix, log columns. Read `utils/logger.ts:34-49`.

**G157-F3 (INFO, scope): with the production hook, the ready-hook guard is defence in depth; a sibling KS-1868 site remains in chargeable-events.ts.**
- FOUND: The real `loadChargeEventsFromDb` never lets an unreadable value reach `runDbReadyHook`. Its catch, and `ensureTable`'s catch (:61), read `err?.message` unguarded and hand it to the logger. For the hostile kinds those reads throw an ordinary TypeError, so:
  - `ensureTable`'s "Failed to ensure" line is lost, and the COUNT check is skipped.
  - One warn line carries the TypeError text instead of the value.
- FOUND: That behaviour is identical at base and head: 60 of 60 hookReal cells are exact, log text included. It is not money-affecting: the warm only ensures the table and counts rows. But it is still a KS-1868 catch, and so are the other `err?.message` catches in chargeable-events.ts (:179, and the processChargeEvent, usage and report catches). I suggest a follow-up item; it does not belong in this PR.
- TESTED: the hookRealBoot and hookRealRecovery sites in the matrix (pool query throws the value for CREATE TABLE and COUNT). I compared head and base exactly with a node one-liner: 60 same, 0 differ.

**G157-F4 (LOW, test gap): 2 of 12 mutants survive. The PR's test has no null/undefined cell at either site and never asserts `isDbAvailable()`.**
- FOUND: P1 and H1 (`err?.message` → `err.message`) pass both the new test (9/9) and the full billing suite (377/377). Under the mutant, a null or undefined value logs `'unreadable thrown value'` instead of omitting `error`. It still does not crash, so the class bar holds either way.
- FOUND: The listener-null case is exactly the one that crashes base, and no cell covers it.
- TESTED: `harness/mutants.py` → `logs/mutants.json`, `logs/mutants.out`. Each mutant is applied as one exact replace of the Nth occurrence, then the new test file and the full billing vitest suite run, then db.ts is restored by `git checkout --` with the blob sha asserted.
- HOW: 10 of 12 killed:
  - P2/H2: String() dropped
  - P3/H3: constant changed
  - P4/H4: null passthrough dropped
  - P5/H5: catch rethrows
  - P6/H6: log line removed
- Nice-to-have, not merge-blocking: a `null` cell at the pool listener and an `isDbAvailable()` assert after each cell.

**G157-F5 (INFO, reachability, pre-existing): in real pg, null, undefined and revoked Proxy cannot reach the pool listener.**
- FOUND: pg-pool 3.13.0 `makeIdleListener` runs `err.client = client` before `pool.emit('error', ...)`, so for those values pg-pool throws first. The client is `_remove`d before the emit, so the listener has no state to protect; it only logs.
- FOUND: The kinds that can arrive are getter-throws, BigInt, toJSON-throws and message-is-revoked-Proxy. All four crash base, and head guards all four.
- TESTED: read only (`node_modules/pg-pool/index.js:51-63`, pg 8.20.0).
- HOW: not run against a real pg client.

**G157-F6 (LOW, docs accuracy): the fragment pair and the READY undercount base exposure and omit the recovery crash.**
- FOUND: The flow fragment says the listener threw for "4 of 9 kinds" and initDb rejected for "2 of 9". Measured with the real logger, it is 7 and 5 of 15. The three extra kinds fail inside the logger's JSON.stringify, which the held test cannot see because it stubs the logger.
- FOUND: Neither text says that at base the KS-377 recovery retry turned the rejection into an unhandled rejection that killed the process. Nor does either say that at boot `startup().catch` absorbed it with a misleading "degraded mode" warn.
- FOUND: The test header says "console.log replaced by a plain recording function", but the test mocks `../utils/logger`.
- Wording only, not merge-blocking. The head behaviour claims in both fragments are correct.

**G157-F7 (INFO, merge-tree): clean onto develop 66cbe4e, exactly the 4 paths.**
- FOUND: `git merge-tree --write-tree` is clean:
  - onto 4deb2fc → tree `ed2708e2`
  - onto 66cbe4e → tree `2bd81be6`
- FOUND: Against each develop, the merged tree differs in exactly the PR's 4 paths. base..develop touches 32 files, none under services/billing, packages/shared, Dev/shared or any package(-lock).json. Between head and the 66cbe4e merge tree there are 0 differences under billing, shared and the lockfiles.
- TESTED and HOW: `scripts/mt.sh` → `logs/merge-tree.log`.

## Figures (re-measured; author's figure in brackets)

| Item | Result | Author |
|---|---|---|
| Red-first (base db.ts + new test) | 5 of 9 failed, all `AssertionError`: R1 `{threw:true}`, R2/R5 `'<symbol>'`, R3/R4 `{ok:false}`. C1-C4 green, rc 1, 0 timeouts | [5/9 by assertion, 4 controls] match |
| New test at head | 9/9 | [9/9] match |
| Billing vitest, base | 19 files / 368 tests, rc 0 | [19/368] match |
| Billing vitest, head | 20 files / 377 tests, rc 0 | [20/377] match |
| tsc, service tsconfig | 0 errors at base and head | [0/0] match |
| tsc, tests included | 18 at base (19 test files) and 18 at head (20 test files). The location-stripped error sets are identical. None in db.ts or the new test | [18/18 same set] match |
| eslint, db.ts + new test | 0 errors, 0 warnings, rc 0. Base db.ts also clean | [rc 0, planted rc 1] match |
| docs-fragments check | rc 0, "lint clean, render passes html_docs_check" | [rc 0, planted rc 1] match |
| Mutants | 12 run: 10 killed, 2 survived (P1, H1) | n/a |
| Recorder matrix | 300 cells. Head: 150/150 alive, 90/90 synthetic cells equal to ordinary. Base: pool 7/15 dead, recovery 5/15 dead, boot 5/15 initDb rejects (alive), per env | [ALL HOLD; 4/9 and 2/9 base] holds, base wider |
| Install | `npm ci --ignore-scripts` rc 0, 1798 packages (`logs/npm_ci.log`); packages/shared built rc 0 | n/a |

Notes on the figures:
- Vitest's JSON `numTotalTestSuites` counts describe blocks too (80/78). The file counts above come from `testResults.length`.
- tsc: the positive control was a planted TS2322 in db.ts. It was caught by both configs: service rc 2 with 1 error, tests-included 19 errors. The tests-included config is `harness/tsconfig.tests.json`.
- eslint: the planted `debugger;` plus an unused const gave rc 1 (no-debugger error, no-unused-vars warning). Restored by sha.
- docs-fragments: the planted unclosed `<div>` gave rc 1 in the flow fragment and rc 1 in the cheat fragment. Restored by checkout; rc 0 after. The cheat ADVISORY at committed line 6235 is pre-existing and was seen at gate 156.
- The lockfile at head is identical to develop 66cbe4e's, and `npm ci` did not fail.

## NOT TESTED

- Node 24 (host v26.8.1 throughout).
- A real Postgres, or a real pg client emitting through pg-pool's idle path. F5 is read, not run.
- A booted billing service, any HTTP route, a Stripe call or webhook over HTTP. The money-path answer is by reading code plus the flag measured in the recorder.
- The four platform suites; whole-repo CI; any deploy.
- `LOG_LEVEL` set (the cells run at the default `info`; at `LOG_LEVEL` above error nothing is logged at either version).
- docs-fragments `check` on the merged tree, and `check --committed`.
- Mutants were judged by vitest only; the recorder was not re-run per mutant.
- Multi-tenancy pools (`getTenantPool`/TenantPoolManager). They are not touched by the PR, and their listeners live in shared.

## Housekeeping

- Every write stayed in this workdir: `repo/`, `harness/`, `scripts/`, `logs/`.
- The clone is at the PR head, `git status` is clean, and the db.ts blob (`3f2d24d48`) was verified after every swap.
- All runs were foreground and have finished. `ps` shows no process with this workdir in its command line, and `logs/cwd` is empty. The one background `find` I started (to locate the READY) was stopped.
- I did not touch the Blockchain checkout beyond `clone --shared` (a read) and read verbs. Its 18-line `git status` is pre-existing and not mine.
