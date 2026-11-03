# QA GATE 160: Secuura Platform K PR 1977 (KS-1868, auth db pool + Redis session), TIER 1, round 1

**Verdict: GO WITH NOTES. Nothing has to be fixed before merge. MERGE: no HOLD-FOR-KAM, because no head cell is more permissive than base with an ordinary Error.**

The class bar holds at all four changed sites. I ran 15 value kinds (plus 2 more in a later run), on both arrival paths for the session store and both db sites, under both the development and production logger formats, with the real auth winston logger. For every one of those runs, head ends in exactly the state base reaches for an ordinary Error. That holds across 150 of 150 head cells in the main matrix and 16 of 16 in the extra-kinds run.

On the TIER 1 flag:
- When a hostile value reaches the Redis listener, head now sets `redisAvailable = false`. That is the same value an ordinary Error gives at base.
- getSession, createSession, password change, password reset, the refresh denylist, the login lockout and health then end in the same state as the ordinary-Error reference, in every cell.
- At base, the same hostile values **crash the process**: Node's default behaviour applies, because auth registers no `uncaughtException` handler. The "flag stuck true" state the author describes exists only if something keeps the process alive.
- In that state (measured with a catch-all handler), base is **more** permissive than head: the password change and reset gates read the flag as true and go on to the write. Head removes that state. It adds none.

Every figure the author gave matched when I measured it again. My full-suite runs were cleaner than the author's: 0 failures and 0 skips at both versions, where the author reported ks949 failures and load timeouts. 9 of 26 mutants survive. All 9 are LOW test gaps or equivalent mutants (G160-F5).

Subject:
- Head `ccbca31cfa49b7d1b222a62853924764ab998990`, which equals Wednesday's pin, fetched by this gate from GitHub `refs/pull/1977/head` into its own `git clone --shared` (`repo/`).
- PR parent and build base `f7b4a7173010a407864ecb7ab92814824f9cb4b6`; develop `66cbe4e52d5afadc9d13ca141200026cc68d5095`.
- Host Node v26.8.1, typescript 5.9.3 (clone).
- The product and test bytes equal the held Spark passes O87-P2 and O87-P7. I compared the changed lines per file and all 4 are EQUAL (`logs/spark_bytes.log`).

## Answer to the TIER 1 question (Redis listener flips the availability flag)

**Who writes `redisAvailable`:**
- `__setRedisForTesting` (test only).
- `initRedisSession` on success (:55).
- The `error` listener (:67), which the PR changes.
- The `ready` listener (:75).
- The init catch (:87), which the PR changes.

**Who reads it, through `isRedisAvailable` / `getRedisClient`:**
- Every function in session.ts.
- `refreshDenylist` (fails closed on a null client).
- `accountLockout` via `getRedisClient` in `routes/auth.ts:350` and `passwordLoginGate.ts:231/382` (fails OPEN on a null client).
- `oauthState`: store throws and consume refuses, so it fails closed.
- `routes/users.ts:1003/1038` and `routes/auth.ts:885/926`: password change and reset answer 503 before the write.
- `routes/health.ts:28`: degraded.

**Measured end state, from `logs/matrix_all.tsv` and `logs/summary.txt`.** These are the reference cells, base + ordinary Error, Redis down. The listener path and the connect path are identical in development and production:

| | base, ordinary Error | head, every one of 15 (+2) kinds | positive control: Redis up, flag true |
|---|---|---|---|
| process | alive | alive | alive |
| flag | false | false | true |
| getSession(stored live session) | null | null | **ACCEPTED** |
| createSession | throws "Redis is not available" | same | created |
| password change / reset gate | 503 | 503 | **proceeds to write** |
| refresh denylist, revoked jti J1 / fresh jti J2 | true / true (fail closed) | true / true | true / **false** |
| lockout for a locked (email, ip) | **false (fail OPEN)** | false | **true** |
| health | degraded | degraded | client present |

- **Head more permissive than base-with-ordinary-Error:** 0 cells. I checked this with `harness/summarise.js`, which flags any head cell where a session is accepted, a revoked jti is honoured, or a password write proceeds. The positive-control column shows that each of those three states can be detected.
- **Base with hostile values, Node default (no handler):**
  - At the listener, the process dies (exit 1) for 7 of 15 kinds in development: null, undefined, revokedProxy, messageGetterThrows, bigintMessage, messageToJSONThrows, messageIsRevokedProxy. Production gives 6 of 15 (no bigintMessage, because winston's production json format serialises a BigInt).
  - Through the connect catch, `initRedisSession` rejects, and index.ts:309-314 would `process.exit(1)`. This happens for 5 of 15 kinds in development and 4 of 15 in production.
  - Cyclic messages add 2 more dead or rejecting cells in development only.
- **Base with a catch-all `uncaughtException` handler (`survive` mode, counterfactual):**
  - Those same kinds leave the flag **true** while the client is down.
  - getSession and createSession throw "Connection is closed.", and the denylist throws, so the refresh route takes its error path (read).
  - The lockout returns false through its own catch.
  - The **password change/reset gate proceeds to the write**, and then the KS-1692 post-write mapping fires (read). That state is more permissive than the reference, and **head eliminates it**.

**Plain answer for Kam:** this PR does not open anything. For hostile values it turns "auth process crashes, or with a handler sits flag-true and lets password writes through" into "auth keeps running in exactly the degraded state an ordinary Redis error already gives". That degraded state includes the PRE-EXISTING lockout fail-open (G160-F3), which is unchanged by this PR.

## Findings

**G160-F1 (INFO, positive): class bar holds at all four sites, 17 kinds x 4 paths x 2 logger formats.**
- FOUND: Head equals base-with-ordinary-Error in 150 of 150 matrix cells and 16 of 16 extra-kind cells. The listener returns, the flag ends the same, init and initDb resolve, all 26 DDLs are attempted and logged, and exactly one line is logged with text. The logged text for each kind is:
  - getter throws, revoked Proxy, or message toString throws: `'unreadable thrown value'`
  - Symbol message: `"Symbol(g160)"`
  - BigInt message: `"10"`
  - toJSON-throws or cyclic message: `"[object Object]"`
  - null, undefined, or a non-Error value: `error` omitted, as base does for an ordinary non-Error
- FOUND: Base exposure (Node default):

  | Site | development | production |
  |---|---|---|
  | pool listener, dies | 7/15 | 6/15 |
  | Redis listener, dies | 7/15 | 6/15 |
  | connect catch, rejects | 5/15 | 4/15 |
  | migration catch, rejects | 5/15 | 2/15 (debug lines are not formatted at the production log level, so only the read-throws kinds fail) |

  This is consistent with the author's 6/12 and 4/12, and wider.
- TESTED: `harness/cell.js` and `harness/run_matrix.js` (304 cells, 6 in parallel) → `logs/matrix_all.{json,tsv}`. Extra kinds (cyclicMessage, numberMessage, 32 cells) → `logs/extra_kinds.log`.
- HOW:
  - The real base and head `db.ts`, `services/session.ts`, `utils/logger.ts`, `services/refreshDenylist.ts` and `services/accountLockout.ts` were extracted by blob (blob shas in the commands that extracted them, re-checked by hash-object after each swap) and transpiled verbatim (`harness/transpile.js`).
  - Only `ioredis`, `pg` and `@secuura/shared` are replaced, through a `Module._load` stub. Winston is the real one, resolved from the auth install.
  - The stub client is an EventEmitter. It emits `error` from `setImmediate`, outside any caller's try, and re-throws to the event loop as a socket callback would. From that moment every command rejects ("Connection is closed.").
  - The boot rejection mirrors index.ts:309-314.
  - Positive controls: the base dead and reject cells, and the `up` cells, where the session is ACCEPTED, the lockout is true and the password write proceeds.

**G160-F2 (INFO, TIER 1): the flag flip is base-ordinary-equivalent; no fail-open. MERGE.**
- FOUND: as in the table above. There are 0 head cells more permissive than the reference, and the instrument can detect each permissive state.
- FOUND: the author's "flag stays true" is accurate only with a handler. Under Node's default it is a process exit (`DEAD`, exit 1, in the `default` mode rows). The author marked this as read-not-run; I measured it. It does not change the verdict.
- TESTED and HOW: `default` and `survive` modes of the same cell; `logs/summary.txt`.

**G160-F3 (MEDIUM, PRE-EXISTING, base = head, not caused by this PR): the login lockout fails OPEN whenever the session store is unavailable.**
- FOUND: In every flag-false cell, at base with an ordinary Error and at head, `isLockedOut` returns **false** for an (email, ip) whose lockout key is set. With Redis up it returns true. accountLockout.ts:87 returns false for a null client, and :92 returns false on a Redis error. Its header calls this the deliberate availability choice, with the per-IP rate limiter as the first line.
- FOUND (read, not run): in the login route (`routes/auth.ts` ~348-365), the lockout check comes before `verifyPassword`, and `createSession` comes after it. During an outage a wrong password gets InvalidCredentials, while a right one reaches `createSession`, which throws.
  - So the lockout is off, and the two outcomes differ, which can serve as a password-correctness oracle during an outage.
  - `recordFailure` is also a no-op, so failures during the outage never count.
  - Whether the route maps the createSession throw to a status distinguishable from 401 was not driven.
- TESTED: the recorder's `lockoutLockedVictim` column, plus a read of the callers.
- This is for Kam to rule on if he wants to revisit it. It is not merge-blocking for this PR.

**G160-F4 (INFO, stale wording, untouched by the PR): the "in-memory session fallback" wording is false.**
- FOUND: there is no in-memory session store. The wording appears at:
  - session.ts:86 (the log line, still emitted at head)
  - health.ts:30 (`'Redis not connected (using in-memory fallback)'`)
  - index.ts:9, :172 (`sessions: 'Redis (with in-memory fallback)'`), :255 (comment)
  - the PR's **new** test file `ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts`. Its header comment says the throwing init catch makes init reject "instead of falling back to the in-memory sessions". It also pins the stale text as the `INIT` constant, so a wording fix will need a matching test edit.
- FOUND: The PR's flow and cheat fragments state correctly that the wording is stale.
- TESTED: grep at head (`git grep` over auth src).
- HOW: read.

**G160-F5 (LOW, test gap): 17 of 26 mutants killed by the PR's tests, and 9 survive.**
- Survivors:
  - **P1, M1, L1, C1** (`err?.message` → `err.message`): the tests have no null/undefined cell at any site. The recorder shows only a text difference: null and undefined are caught and logged as `'unreadable thrown value'` instead of being omitted. The state is unchanged and the class bar still holds.
  - **P5, M5, L5, C5** (drop the `m === null` branch): this would log `"null"` for a message that is `null`. Neither the tests nor my recorder has a null-message kind, so **my instrument could not fire on these**. The ctl_base run showed the recorder can detect differences in general, but not this specific one. Not proven either way. Text only.
  - **C6** (delete `redisAvailable = false` in the init catch): equivalent. The flag is initialised to false and only becomes true after connect and ping succeed. A throw from `logger.info` at :56 would be the only path; not exercised.
- Killed, as positive controls for the tests: X2 (no coercion), X3 (fallback re-reads err), X4 (template literal), X6/X7 (raw err to the logger), and **L6 (listener no longer sets the flag false), which the recorder flagged in 30 of 30 cells**.
- TESTED: `harness/mutants.py` → `logs/mutants.json` and `logs/mutants.out`. Each mutant is one exact replace, anchored to its site (the target is asserted to lie within 700 chars of the anchor). It then runs the PR's two test files (vitest, cwd = auth) and the 30 recorder cells for that site against a transpile of the mutated file (`harness/build_mut/<id>`). The file is restored by `git checkout --` with the blob sha asserted.
- Recorder controls: the unmutated head build gives 0 differences on the listener and migrate paths, and the base build gives 22 and 9 (`build_mut/ctl_head`, `ctl_base`).
- Nice-to-have: add a null cell and a null-message cell.

**G160-F6 (INFO, reachability, read only): real ioredis and pg emit Error objects.**
- FOUND: ioredis 5.11.1 emits `error` from the socket error handler (`event_handler.js:219-222`), from connect callbacks (`Redis.js:132-139`) and from `select` rejections. All of these carry net or parser Errors, and `silentEmit` passes the value through unchanged. I did not show that a hostile value can reach the listener in production. The guards are still correct.
- TESTED and HOW: read only.

**G160-F7 (INFO, pre-existing, read only): residual unguarded reads in the touched file and at boot.**
- FOUND:
  - `db.ts:204`: `probeDb`'s catch returns `err?.message` unguarded. A hostile probe failure would reject `initDb` (exit 1 at boot) or the background retry timer (unhandled rejection).
  - `index.ts:310`: logs `{ error: err }` raw. In the base-reject cells it logged `{"error":{}}`. Unhandled rejections there were not seen in my cells.
- Both are outside this PR. They belong to the other KS-1868 sites.

**G160-F8 (INFO, pre-existing, read only): the connect-catch path never attaches the `ready` or `error` listeners.**
- FOUND: if Redis is down at boot, the init catch leaves `redis` set and the flag false, and the `ready` listener (:74) was never attached. The flag therefore cannot return to true without a restart, even if ioredis later connects.
- This is the same at base and head. I did not verify whether ioredis reconnects after a failed `lazyConnect` connect. Possibly a KS-617 cousin; it needs a run before anyone acts on it.

**G160-F9 (INFO, merge-tree): clean, exactly the PR's paths.**
- FOUND: `git merge-tree --write-tree 66cbe4e ccbca31` gives rc 0 and tree `72ea88e9`. The merged tree differs from develop in exactly the PR's 6 paths. The merge-base is f7b4a71.
- FOUND: base..develop touches 9 files, none under services/auth and none of the fragments. Head and the merged tree have 0 differences under services/auth.
- Control: base..develop does touch 5 service paths, so the overlap grep could match.
- TESTED: `logs/merge-tree.log`.

## Figures (re-measured; author's figure in brackets)

| Item | Result | Author |
|---|---|---|
| Red-first (base db.ts + session.ts, new tests) | db 5/9 failed, session 5/9 failed, all by AssertionError; the 4+4 controls green | [5/9, 5/9 by assertion] match |
| New tests at head | 18/18 (9+9) | [18] match |
| Auth vitest, base f7b4a71 | 133 files / 1561 tests, 1561 pass, rc 0 | [133/1561; 1502 pass, 3 fail, 56 skipped under load] totals match, my run fully green |
| Auth vitest, head | 135 files / 1579 tests, 1579 pass, rc 0 | [135/1579, 1577 pass] totals match, my run fully green |
| Test-types ratchet (auth, check.cjs) | base 184 files (133 tests) 42 errors, 0 new, 0 stale, rc 0; head 186 (135) 42/0/0, rc 0; planted TS2322 in session.ts gave rc 1, "1 new" | [42/42, 0 new, 184→186, planted fails] match |
| tsc, service tsconfig, head | 0 errors | n/a |
| eslint, the 4 changed .ts at head | 0 errors, 0 warnings; base product files 0/0; planted `debugger` + unused const gave rc 1 (no-debugger error, no-unused-vars warning) | [0/0, planted] match |
| docs-fragments check, head | rc 0, "lint clean, render passes html_docs_check" | n/a |
| docs-fragments, planted unclosed `<div>` | flow rc 1, cheat rc 1; rc 0 after restore | [planted] match |
| Recorder | 304 + 32 cells; head = reference in 166 of 166 | [12 values x 2 paths, all 24 hold] holds, wider |
| Mutants | 26 run: 17 killed by tests, 9 survived (F5) | n/a |
| Spark bytes | O87-P2 and O87-P7 changed lines EQUAL to the PR in all 4 files | [byte for byte] match |
| Install | `npm ci --ignore-scripts` rc 0, 1798 packages; packages/shared built, rc 0 | n/a |

Notes on the figures:
- **Named re-run:** the first full-suite run (`logs/suites_full.out`) used `vitest --root` with the cwd outside auth. Both versions then failed 2 ks1467 cells on an ENOENT for a cwd-relative path, and head also had 1 ks949 STACK_TRACE_ERROR. That run is discarded as an instrument error. The re-run with cwd = services/auth (`harness/vt.js`; `logs/suites_full_rerun_cwd.out`, `logs/suites_red_rerun_cwd.out`) gives the figures above. Red-first was identical in both runs.
- The docs-fragments cheat ADVISORY at committed line 6235 is pre-existing.

## NOT TESTED

- Node 24 or any LTS Node (host v26.8.1 throughout).
- A real Redis or Postgres, or a real ioredis or pg client emitting a hostile value (F6 is read only).
- A booted auth service, or any HTTP route. These were read, not driven:
  - the 401 from `authenticate`
  - the 503s in users.ts and auth.ts
  - the refresh route's handling of a denylist throw
  - the login status for createSession throwing during an outage (F3 oracle)
  - OAuth state store and consume (read only; not in the recorder)
- The actual `process.exit(1)` in index.ts. The recorder mirrors the `.catch` and records `wouldExit1`.
- Whether ioredis reconnects after a failed lazy connect (F8).
- A null-message kind (F5: the X5 survivors could not fire in my recorder).
- The four platform suites; any deploy.
- docs-fragments `check` on the merged tree, and `check --committed`.
- The other KS-1868 sites.

## Housekeeping

- Every write stayed in this workdir: `repo/`, `harness/`, `scripts/`, `logs/`, `evidence/` (the author's file, untouched).
- The clone is at the PR head `ccbca31cf`. `git status` is clean, and the db.ts and session.ts blobs were verified after every swap.
- The Blockchain checkout was touched only by read verbs. The GitHub fetch used the project deploy key through a per-command `GIT_SSH_COMMAND`, inside this clone only. The clone's origin URL was set to GitHub inside the clone.
- No files were deleted. Mutant builds are kept under `harness/build_mut/`.
- All background jobs have finished, and `ps` shows no process with `gate160` in its command line.
