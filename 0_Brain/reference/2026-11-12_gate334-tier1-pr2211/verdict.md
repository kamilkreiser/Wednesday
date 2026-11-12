PR 2211: GO WITH NOTES (at head c0e112d6bc3e; tier 1; round 1)

Gate 334, tier 1 (Opus), one session, 2026-11-12 06:47Z to 07:00Z (17:47 to 18:00 AEDT). Findings only: nothing fixed, posted, mailed, pushed, merged, or written to Linear, GitHub or a board.

Where things ran:
- Every write verb ran in my own clone `scratch/repo` (fresh `git clone --filter=blob:none`, sparse checkout, `scratch/setup.sh`; the clone's `core.sshCommand` is the project deploy key so lazy blob fetches work). Fetch and merge-tree ran only there.
- `node_modules`: read-only symlinks, as gates 331/332 did. The root `Blockchain/Dev/node_modules` and `packages/shared/dist` point to gate 313's `r2` install (express 4.22.3, vitest 4.1.12, tsc 5.9.3). r2's commit 1c5ca4bb36c0 differs from the head in `package-lock.json` only by the removal of nodemon and its deps (not used by kyc), and in one shared test file. No kyc-local `node_modules` was linked.
- In the shared Secuura checkout I ran read verbs only (`ls-remote`, `GIT_OPTIONAL_LOCKS=0`).
- Every file I changed in the clone was restored and checked by blob: index.ts `d08288dc55ca`, the ks1931 test `52bc61a64d5b`. The probe test was moved aside (`scratch/aside/zzprobe-gate334.test.ts.ran`). `git status` in the clone shows only the two symlinks.
- Vitest ran with `cwd` = the kyc package via python `subprocess` (`scratch/whole.py`, `scratch/probe.py`). tsc ran by absolute path with `-p` naming the config. Nothing ran from the WEDNESDAY working directory.
- Machine: Node v26.8.1 (NOT the LTS line), macOS arm64. load1 stayed between 1.8 and 3.8 for every run (all under 8).
- Spark: tunnel UP. Digest STANDARD and the shadow review both ran. The shadow work dir is in the session scratchpad (`spark_work_2211`) because `spark_gate.sh` refuses paths under WEDNESDAY (gates 329/332 precedent); copies are in `scratch/spark/`.

## Pins

| when | develop | refs/pull/2211/head |
|---|---|---|
| start, 06:47:32Z (`scratch/pins_start.txt`) | acee38da1ce7e9e94d4ec3186bb512b1794c7cb9 (= commission) | c0e112d6bc3e7cc74f3111ceacb42b0e1489be83 (= commission) |
| end, 06:59:56Z (`scratch/pins_end.txt`) | unchanged | unchanged |

Neither pin moved.

**Shape:** one commit c0e112d6, parent cea1cdc2b07d. `merge-base(origin/develop, head)` = `merge-base(head, origin/develop)` = cea1cdc2b07d; `rev-list develop..head` = 1. GraphQL: OPEN, not draft, base develop, headRefOid = pin, 1 commit, 2 files, +155 -2, MERGEABLE.

**Merge-tree:** `merge-tree --write-tree origin/develop p2211` rc 0, tree 039bce2b81a9 (`out/merge_tree.txt`).
- develop to merged: exactly the PR's 2 files, +151 -0 and +4 -2.
- head to merged: exactly develop's 3 moved api-gateway files (+132, +2 -1, +9).
- **Control that develop's lines survive:** each of develop's 3 moved files has a merged blob equal to develop's and different from the head's: ks1952 test 3d71b749ef5e (absent at head), ks466 test 181531e33d30 (head d1886821402d), routes/verification.ts c12c71c753c0 (head a5e55ac8b59a). The PR's 2 files have merged blobs equal to the head's (d08288dc55ca, 52bc61a64d5b).
- The develop move (cea1cdc2 to acee38da) touches 3 api-gateway files only; kyc's index.ts blob is cdd06301fb1a at both develop commits. The seat's MOVE claim is verified.

## Summary

The change does what the row says, and the measurements confirm it:
- Exactly two callers of `dbGetVerificationsByUser`; only the cascade passes `true`; the GET route's behaviour is unchanged.
- R1/R2 are red at develop and green at head; the whole kyc suite is 90 + 4 = 94/94.
- The new throw fires before any DELETE, so nothing is half-erased by it.
- Both entry points surface the failure:
  - the bus handler rejects, so the bus retries 3 times and then dead-letters;
  - the DELETE route does not answer, and the kyc process exits.

The new behaviour is not strictly "more erasure" than develop's. A deterministic per-row decode failure now blocks the whole erasure, where develop deleted every `user_id` row (G334-2211-1). It is never silent.

Statement 2 is measured true and is pre-existing. This PR makes it fire on more inputs (G334-2211-2). No Major.

## Q1. Correctness: callers and mutants

**Callers at head** (`git grep` over the whole `Blockchain/` tree at p2211, the sparse checkout's full content):
- `index.ts:223`: the definition (`throwOnError = false`).
- `index.ts:392`: `dbDeleteUserData` passes `true`.
- `index.ts:823`: `GET /api/kyc/user/:userId` passes nothing, so the default is `false`.
- Every other hit is a comment or a test (migration 035's comment, the ks1868 and ks1931 test headers).

Controls:
- `dbGetVerificationsByUser(` counts 3 at both develop and head (definition + 2 calls).
- A planted absent name gives `git grep` rc 1.
- No service outside kyc names the helper or the cascade.

`dbDeleteUserData`'s callers are `index.ts:1226` (the DELETE route) and `index.ts:1325`. The latter passes it to `startUserErasedSubscriber`, the user.erased bus consumer at `userErasedSubscriber.ts:36`. I found no admin path or other consumer.

**GET caller unchanged:** at both builds the probe gives `200` with `verifications: []` on every failure scenario (read error, DEK reject, malformed row). C2 and the ks1868 GET cells pin it (M4 and M5 below).

**Red first / green** (whole suite, `out/t_redfirst_develop.log`): with index.ts set to develop's blob cdd06301 and the test kept, the result is 2 failed (R1, R2: `expected [ …(3) ] to have a length of +0 but got 3`) and 92 passed, rc 1. The head gives 94/94, rc 0.

**Mutants** (whole kyc suite each; `scratch/mkmut.py`, `scratch/mut/*.ts`, `out/t_mut_*.log`):

| mutant | result | killed by |
|---|---|---|
| M1 cascade passes `false` (develop's call) | 2 failed | R1, R2 |
| **M2 throw moved before the log line** | **0 failed, SURVIVES** | none: the logger is mocked to a no-op, so no cell checks the cascade-path log |
| M3a outer `.catch(() => [])` in the cascade (continue) | 2 failed | R1, R2 |
| M3b outer try/catch in the cascade, `return 0` (stop, answer 200 with 0) | 2 failed | R1, R2 (status 200) |
| M4 default flipped to `throwOnError = true` | 4 failed | ks1868 GET C1, R1, R2 and ks1931 C2 |
| M5 GET route passes `true` | 4 failed | same 4 |
| **M6 `throw new Error(...)` in place of `throw err`** | **0 failed, SURVIVES** | equivalent for behaviour; only the bus-side error text changes |
| M7 inverted (`if (!throwOnError)`) | 6 failed | the 4 GET cells + R1, R2 |

The commission's four mutants: M1, M3 (both shapes) and M4 are killed; M2 survives (G334-2211-3).

## Q2. What the cascade does on the new throw

Order in `dbDeleteUserData` (index.ts:374-414):
1. `isDbAvailable()` false: return 0.
2. **`dbGetVerificationsByUser(userId, true)`**. The new throw fires here.
3. Delete images by id (only if the id set is non-empty).
4. Delete images by user_id.
5. Delete consents.
6. Delete verifications.
7. `subjectDeks.evict`.

The read is the first database statement, so on the new throw **nothing has been deleted**. Measured by the probe: 0 DELETE statements in S1, S2 and S3 at head. There is no half-erasure from this throw. Half-erasure on a failing DELETE (S4: the first DELETE ran, the rest did not) is unchanged and identical at both builds.

**Probe** (`scratch/probe/zzprobe-gate334.test.ts`, run through `scratch/probe.py`; raw `out/probe_head.json` and `out/probe_develop.json`). It uses the ks1931 harness, plus rows for the read, a DEK resolve that can reject, a recording logger, and the real `startUserErasedSubscriber` with a stand-in bus that captures the handler. Each scenario was driven through the DELETE route, the GET route and the bus handler:

| scenario | develop: DELETE route | develop: bus handler | head: DELETE route | head: bus handler |
|---|---|---|---|---|
| S0 control, read OK, legacy image ids | 200, 4 DELETEs | resolves (ack), 4 DELETEs | 200, 4 DELETEs | resolves, 4 DELETEs |
| S1 the SELECT rejects | **200 "All KYC data … deleted", 3 DELETEs** | **resolves (ack), 3 DELETEs** | NO ANSWER, 0 DELETEs, 1 unhandled rejection | **rejects** ("db down"), 0 DELETEs |
| S2 a row's DEK resolve rejects (unwrap failure) | 200, 3 DELETEs | resolves, 3 DELETEs | NO ANSWER, 0 DELETEs, unhandled | rejects, 0 DELETEs |
| S3 a legacy plaintext `documents` that is not JSON | 200, 3 DELETEs | resolves, 3 DELETEs | NO ANSWER, 0 DELETEs, unhandled | rejects, 0 DELETEs |
| S4 the first DELETE rejects | NO ANSWER, 1 DELETE, unhandled | rejects, 1 DELETE | identical | identical |

At head the helper's error line is written on S1-S3 on both paths.

**Do the callers surface it?**
- **Bus consumer:** the handler catches, logs `[cascade] user.erased handler failed`, and rethrows. The shared bus (`packages/shared/src/events/index.ts:181-211`) retries the handler 3 times back to back, then writes the event to the `dead-letter` stream and acks it. The handler rejection was measured; the retry and dead-letter steps are from reading the code. The failure surfaces; it is not swallowed.
- **DELETE route:** it is not answered, and the rejection is unhandled (Q3).
- No admin path or queue consumer other than these two exists.

**Strictly safer than develop?** Not in every case, but never silently:
- **S1 transient read failure** (the ticket's case): develop answered 200 / acked while legacy-by-id images could survive. Head deletes nothing and says so. When the database recovers, a bus retry (immediate, 3 attempts) or a repeated DELETE completes the erasure. This is the improvement.
- **S2/S3 deterministic per-row failure:** develop deleted every `user_id` row (images by user_id, consents, verifications). If every image carries `user_id`, which is migration 035's backfill claim, develop's erasure was complete. Head deletes nothing; the bus dead-letters after 3 attempts and every retry fails the same way. **Head erases less here, but loudly** (error log, a dead-letter entry, an unanswered request). See G334-2211-1.
  - Reachability on the bus path: originate destroys the DEK (`gdprService.ts:930`) before it publishes user.erased (`:963`). After that, `getDek` returns null for a destroyed key (`subjectDek.ts:128`) and does not throw. So S2 is reachable there only through a pii_subject_keys SELECT failure, which is transient.
  - The deterministic residue is S3-type data: legacy plaintext `documents`, or a `checks` string that is not JSON. `parseJsonb` runs outside rowToVerification's inner try blocks.
  - On the direct DELETE route (live key), S2 is also reachable through an unwrap failure (keyring misconfiguration).

## Q3. Body statement 2 (the DELETE route has no try block)

Measured at head:
- Real app in vitest (probe and R1/R2): the request gets **no answer** within the deadline. The rejection reaches `unhandledRejection` (probe S1-S3: 1 each). The registered shared `errorHandler` is never reached, because Express 4.22.3 does not forward an async handler's rejection.
- **Process exit:** kyc registers no `unhandledRejection` listener (no hit in `services/kyc/src`, and `setupGracefulShutdown` has no live consumer per `packages/shared/src/index.ts:22`). A stand-alone probe (`scratch/probe/exit_probe.cjs`) used Express 4.22.3 and Node v26.8.1 with the same route shape and a 4-arg error handler registered. For both an Error and a revoked-Proxy thrown value, **the process exits with code 1 before any response** (`EXIT code=1 after 20ms`). The OK control answered 200 and exited 0.
  - For the revoked Proxy, Node's own rejection printer throws a TypeError, and the process still exits 1.

**Pre-existing:** yes. At develop, S4 (a failing DELETE) gives the identical unanswered and unhandled result.

**Does this PR change how often it fires?** Yes:
- At develop, a read failure was swallowed. The route then crashed only if a DELETE also failed: a full outage did that, a blip or a poison row did not.
- At head, every read failure reaches the unguarded route: transient SELECT failures and per-row decode failures (S1-S3).
- For S3-type data the crash is deterministic and repeats on every DELETE call for that user.

Who can reach the route: the gateway proxies `/api/kyc` with `authenticateToken(true)` only (`proxy.ts:1161`), and kyc adds only `jwtAuthenticate()` (`index.ts:602`). No ownership check was found (G334-2211-4).

Graded **Minor** (G334-2211-2): pre-existing, stated by the body as unchanged, and the body's "Notes for the gate" does say a failed read "now reaches it as a rejection". The consequence (a process exit, repeatable for a poison row) is not stated in that note. A try/catch forwarding to `next(err)` is the follow-up.

## Q4. Suite and controls

| run | load1 | files | tests | rc |
|---|---|---|---|---|
| head (`whole_head`) | 2.13 | 17 passed | 94 / 94 | 0 |
| red first, index.ts = develop cdd06301 (`redfirst_develop`) | 2.03 | 1 failed / 17 | 2 failed (R1, R2) / 94 | 1 |
| planted failing cell appended to ks1931 (`planted_cell`) | 3.20 | 1 failed / 17 | 1 failed / 95 | 1 |
| 8 mutants (table above) | 1.82-3.79 | | | |

- **Whole-ness:** the head JSON report's 17 file names are set-equal to a walk of `src/**/*.test.ts` (17); numTotalTests 94, success true. The package script is a bare `vitest run`, so this is the script. Develop's 90 = 94 - 4 new; the red-first run shows 92 passed including C1 and C2.
- **tsc:**
  - `tsc --noEmit -p services/kyc/tsconfig.json` (tests excluded, as the service config does): rc 0, 0 lines.
  - With the test files, through a scratch config extending the service's (`scratch/tsc/tsconfig.tests.json`): rc 0, 0 lines. It needed `declaration: false`, because the symlinked install gives TS2742 "not portable" otherwise (an artefact of my setup, not of the PR).
  - Planted type error in the ks1931 test: rc 2 (TS2322 + TS6133).
  - Both files were restored by blob.
- **Digest STANDARD** (`digest.py --kind vitest`, Spark UP):
  - whole_head: CHECKED PASS (raw rc 0).
  - redfirst_develop: CHECKED FAIL, the 2 right names (raw rc 1).
  - planted_cell: CHECKED FAIL (raw rc 1).
  - mut_M2: CHECKED PASS (raw rc 0).
  - Every digest verdict agrees with its raw rc. No run was rc 1 with all green, so G331-2209-5's blind spot was not exercised.

## Q5. Census

`scratch/census_gql.py`: 101 open PRs, 444 file rows, every PR's files paged and asserted against totalCount. Raw rows are in `scratch/census_rows_gql.tsv`.

| path | open PRs |
|---|---|
| `services/kyc/src/index.ts` | [2211] |
| `…/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts` | [2211] |
| `services/kyc/src/userErasedSubscriber.ts` (the other caller) | [] |
| anything under `services/kyc/` | [575, 649, 2211]; 575 and 649 touch `services/kyc/package.json` only |

- **Positive control:** `services/auth/src/routes/users.ts` gives [2075, 2201], so it fired.
- **Negative control:** an absent path gives [].
- No other open PR touches either PR path.

## Q6. PR body

Read through GraphQL (`scratch/prbody2211.txt`, 9,078 chars).
- **Tier-1 statement:** first, bold: "TIER 1: product bytes change inside kyc, in the GDPR erasure path…". Present.
- **The behaviour change:** statement 1 is true as measured (S1).
  - The body says the helper caught "every database or decrypt error". It does not say that a per-row decode failure now blocks the whole erasure where develop completed the `user_id` deletes (G334-2211-1).
  - "Every other caller keeps the empty list" is true (Q1).
  - The `isDbAvailable` nuance is true.
- **Statement 2:** true as measured (Q3). "Real database failure and a bus retry: UNMEASURED" is honest. This gate drove the real subscriber handler with a stand-in bus (it rejects), but not a real bus or a real database.
- **Line numbers:** the body cites develop's lines (821, 1223); at head they are 823 and 1226. The body names them as develop's, so this is correct as written.
- **Refs only:** the title and subject say `Refs KS-1931`, and closingIssuesReferences is 0. A closing-word regex (close/fix/resolve forms followed by a key or #N) finds 0 hits in the body; the control line `Fixes KS-1` gives 1.
- **NO-PAIR:** the literal is present.
- **The Linear URL** is present.

## Spark shadow review (calibration row only, not the verdict)

Driver `scratch/spark_run.sh`. One attempt, 71.5 s, `valid: true`, `missing_inputs: ["ticket text"]`.

**Deterministic half:**
- head c0e112d6 (tip), merge-base cea1cdc2, base tip acee38da.
- Diff: 2 files, +155 -2.
- Targeted on the HEAD (ks1931 + ks1868 GET): 7 passed / 0 failed.
- On the BASE product code: 5 passed / 2 failed.
- All of this equals mine.

**Spark verdict: NO GO** (2 Major, 1 Minor, 4 Notes).
1. **Major, "widens the blast radius … no ownership/tenant filter":**
   - Half wrong: the PR narrows deletion (head deletes less on failure, never more).
   - The ownership observation is real but pre-existing and outside the diff (my G334-2211-4).
   - Its evidence quote was flagged not found in the input.
2. **Major, the process-exit claim "stated as fact" while the real database is UNMEASURED:** misframed. The body attributes it to a stand-in probe. I reproduced the exit (Q3).
3. **Minor, "C1 asserts 3 DELETEs but only two run":** wrong. With no rows the id-delete is skipped, and the user_id images, consents and verifications deletes make 3. Measured: C1 passes, and probe S0 shows 4 with legacy ids.
4. **Notes:** stand-in database permissiveness (true, and stated by the body); no template siblings; counts add up; ticket text missing.

**Recall against this gate's findings:**
- G334-2211-2 (frequency of the route crash): partial hit inside Major 1, with the wrong framing.
- G334-2211-4: partial hit.
- G334-2211-1 and G334-2211-3: missed.

**False positives:** 2 (Major 2 and the Minor). Its verdict is two grades from mine.

## Findings

- **G334-2211-1 (Note): a deterministic per-row decode failure now blocks the whole erasure.**
  - What happens: `dbGetVerificationsByUser`'s try covers the SELECT and the per-row `rowToVerification`, so the new throw also fires when one row cannot be decoded. Two measured causes:
    - a DEK resolve that rejects (S2);
    - a legacy plaintext `documents` value that is not JSON (S3).
  - The difference from develop:
    - develop: deleted every `user_id` row, answered 200 and acked;
    - head: deletes nothing; the bus retries 3 times, then dead-letters; the route crashes.
  - When every image carries `user_id` (035's backfill claim), develop's erasure was complete and head's is stuck until someone repairs the row. It is loud (log line, dead-letter entry, unanswered request), never silent.
  - On the bus path the DEK case is reachable only transiently (the DEK is destroyed before the event, and `getDek` returns null for a destroyed key). The deterministic residue is malformed legacy plaintext.
  - The body does not state this case. It is consistent with the cascade's own documented contract ("failures THROW so the event bus retries and dead-letters"), so it is a design consequence, not a defect.
  - Possible follow-up: collect legacy ids from raw rows, or skip and log only the unreadable row, so one poison row cannot block the rest.
- **G334-2211-2 (Minor, pre-existing, frequency raised): the DELETE route crash now also fires on read failures.**
  - The defect itself (no try block, so the request goes unanswered, the error handler is bypassed, and the kyc process exits 1) is measured and pre-existing, identical at develop (S4).
  - This PR routes every read failure to it, including deterministic ones (S3). So one DELETE call for a user with a poison row exits kyc on every attempt.
  - Not a merge blocker. Ticketable follow-up: wrap the route in try/catch with `next(err)`.
- **G334-2211-3 (Note, test gap): what the cells do not pin.**
  - M2 (throw before the log line) survives: no cell observes the cascade-path log, because the logger is a no-op.
  - M6 (re-wrapping the error) survives; it is behaviour-equivalent.
  - R1/R2 count unhandled rejections in `h.unhandled` but never assert the count.
  - No cell drives the user.erased subscriber path (this gate's probe did: the handler rejects at head and acks at develop).
  - No cell covers a per-row decode failure (G334-2211-1).
- **G334-2211-4 (Info, pre-existing, outside the diff, from reading the code only): no ownership check on the KYC user routes.**
  - `DELETE /api/kyc/user/:userId/data` and `GET /api/kyc/user/:userId` carry no ownership or role check beyond `jwtAuthenticate()`: kyc `index.ts:602`, and the gateway `proxy.ts:1161` with `authenticateToken(true)` only.
  - Read literally, any authenticated caller can erase or read another user's KYC data. Not measured; it may already be on KS-486's register. Wednesday to route.
- **G334-2211-5 (Info, pre-existing, stated by the body):** with `isDbAvailable()` false the cascade returns 0, and the route answers 200 "All KYC data for user has been deleted." Unchanged.
- **G334-2211-6 (Info, gate conduct):**
  - node_modules symlinked from gate 313's r2 install (lock differs by nodemon only).
  - Node 26 (not LTS).
  - tsc with tests needed `declaration: false` because of the symlinks.
  - The Spark work dir was in the session scratchpad.
  - All load1 readings were under 8.

No Major. One Minor (pre-existing, frequency raised). The fix is correct for its ticket and stops the silent half-erasure. G334-2211-1 and -2 are ticketable follow-ups, not merge blockers.

## NOT TESTED

- A real Postgres failure, a real Redis event bus, the retry loop and the dead-letter write. The bus handler was driven directly with a stand-in bus; retry and dead-letter are from reading `events/index.ts`.
- The real kyc process exiting. The exit was measured in a stand-alone Express 4.22.3 probe of the same route shape, not by booting kyc's `index.ts` with a stand-in database.
- The originate erasure flow end to end (DEK destroy, then publish), and the kyc DEK cache across the 5-minute TTL.
- The ownership gap in G334-2211-4 (reading only).
- Node 24; a fresh `npm ci` at the head (symlinked installs were used); eslint (kyc has no lint script); docs-fragments; `npm run audit:gate`; the pre-push hook and its legs; the four platform suites.
- The merged tree 039bce2b was not itself run through the suite. Develop's moved files are api-gateway only.
- Linear: the KS-1931 ticket text and the seat's comment 9785e394 were not read.
- The seat's worktree `worktrees/s-r109-ks1931`. My evidence is the pushed head.
