# QA Gate 147 verdict: Secuura/Distributed_Secuura PR 1963 (KS-1868, kyc + wallet-connector `userErasedSubscriber.ts` handler-failed catch, Spark O86-P3 + O86-P4), TIER 1, round 1

## BLUF
**Verdict: GO WITH NOTES. Nothing has to be fixed before merge.**

**Q1 (erasure outcome): head's after-state for an unreadable value is IDENTICAL to base's after-state for an ordinary Error.** I ran the real handler and the real bus loop with only the DB (and the bus's Redis client) replaced. The two are the same in:
- attempts (3)
- which rows are erased, and in what order
- what is left
- the dead-letter entry (one `xadd` to `secuura:events:dead-letter`, `error` = `Failed after 3 attempts`, the raw event, then `xack`)

Only two things differ from base, and both are intended:
- **Logs:** head writes one `handler failed` line per failed attempt with `"unreadable thrown value"`. Base wrote none.
- **Rethrow identity:** head rethrows the original value. Base rethrew the TypeError or Error that the read threw. The bus never reads the value (READ, and RUN: same attempts and same dead-letter for every identity).

**This PR adds no new outcome.**

**Separately, there is a HIGH pre-existing finding (G147-F1, MEASURED): a failed cascade leaves the erasure silently incomplete in that service.** Nobody is told. There is:
- no dead-letter consumer anywhere in the tree
- no retry job
- no update to the DSR, which originate marks `completed` at step 12, BEFORE the fan-out at step 13

kyc's delete is four separate statements with no transaction, so a failure part-way leaves a partial erasure:
- fails at the consents delete: images are gone, but `svc_kyc_consents` (ip_address, user_agent) and `svc_kyc_verifications` stay
- fails at the verifications delete: the verification row stays (provider ids, scores, risk level, `documents`/`review_notes` ciphertext)

wallet-connector leaves every `svc_wallet_sessions` row for the subject's address.

The author's numbers re-measure exactly:
- red first: 3/6 + 3/6, all by assertion
- kyc 84 -> 90 and wallet-connector 70 -> 76, all pass
- tsc with tests: kyc 0 -> 0, wallet-connector 1 -> 1 (the same pre-existing TS6133)
- eslint: 0
- fragments: clean, and each planted defect is caught

Mutants: **22/22 killed.** merge-tree is clean onto develop `2f9f7db3` (as read at start) and onto `26955bf1` (develop moved during the gate). Host Node v26.8.1 throughout; nothing was measured on Node 24.

## Heads
- START (logs/head_start.log, 2026-11-02T19:46:25Z):
  - PR head `8d0e6b054c5c157cf6100104cb630836f4210ae5` (= the pin)
  - develop `2f9f7db313b3423bfe3199bed076e992d2bfe2a3` (= the commission's NOW)
  - merge-base `4d1ab2cb6574e2b221353ac3a1de56d515711aaf`
  - 1 commit
- END (logs/head_end.log, 20:00:13Z):
  - PR head unchanged, at `8d0e6b05`
  - **develop MOVED to `26955bf1b828`** (0b381018 = PR 1961 originate, 26955bf1 = transfer approval workflow). Neither touches a path of this PR, kyc, wallet-connector or `packages/shared/src/events`. merge-tree was re-run onto it (section 6).
  - The clone's HEAD is `8d0e6b05`, `git status` is clean (0 lines), and no `zz_g147_*` file is in the tree. Probe and planted files are in logs/_quarantine/.
- The clone has push disabled (`no_push_qa_gate`).
- **PR body not read through the API** (this seat has no gh login). I used the READY mail (evidence/r76_pr1963_ready.txt) and the PR's own flow/cheat fragments.

## 1. Diffstat (logs/diffstat.log, three-dot)
6 files, **+314/-2**, exactly as declared:
- the kyc and wallet-connector `userErasedSubscriber.ts`, 8/1 each
- two new vitest files, 124 each
- the flow and cheat fragments, 25 each

Nothing outside the declared paths.

## 2. The hunks (logs/product_diff.log)
The change is identical in both files. Base:
- `- error: err?.message,` inside the `log('error', '[cascade] user.erased handler failed', {...})` argument

Head:
- `+ let reason; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; }`
- `+ error: reason,`

What does NOT change:
- `throw err` (same statement)
- the success path and the `userId`/`dsrId` keys
- the `subscriber loop terminated` catch (still `err?.message`, deliberately untouched)
- the bus (`packages/shared`), `dbDeleteUserData`, and the wallet DELETE

undefined and null messages pass through unchanged, so the field is still absent or null as at base.

## 3. Behaviour (the key question)

### Q1: erasure outcome. RUN at base and head, with only the DB replaced
**Probe** (scripts/zz_g147_kyc_probe.test.ts, scripts/zz_g147_wc_probe.test.ts, scripts/probes.sh; logs/probe_run1/*.jsonl; tables logs/probe_table_compact.log and logs/probe_table.log; all 6 runs rc 0, 37 + 19×2 cells each).

What runs for real:
- **kyc:** the REAL `index.ts` imported whole. That means the real `dbDeleteUserData` (index.ts:372-408), the real `log` (index.ts:529, `console.log(JSON.stringify(...))`) and the real subscriber wired at index.ts:1323.
- **wallet-connector:** the REAL `server.ts`, with the subscriber wired at server.ts:322 and the real winston logger in its dev AND its production format. The output was read after the format, at the Console transport.
- **Both:** the REAL shared `EventBus` (compiled `@secuura/shared` dist). It is constructed for real, its private Redis client is swapped for a recording fake, and the real `subscribe()` loop runs: retry ×3, `xadd` dead-letter, `xack`.

What is replaced:
- `../db`: an in-memory table store that answers the erasure SQL and records every statement
- the Redis client
- `../subjectDeks` (kyc; records `evict`)
- express `listen`
- `initDb` never settles

A thin wrapper around the handler records what the bus receives (`Object.is` with the thrown value). It rethrows unchanged.

Test data:
- kyc subject: one verification (legacy plaintext `documents` naming 2 legacy image ids), 3 images (2 legacy with no user_id, 1 post-035 with user_id) and 1 consent (ip_address, user_agent)
- wallet: 2 sessions on the subject address
- a second user's rows as a control: never touched in any cell

Failure points:
- kyc: images-by-id, consents and verifications, each failing on every attempt, plus consents failing once
- wallet: the DELETE failing always, and failing once

Thrown values: ordinary Error, string, null, BigInt thrown, revoked Proxy, message getter throws, message BigInt, message Symbol, message object `{email}`.

**Order of the kyc erasure** (READ, and confirmed by the recorded statements):
1. SELECT verifications (to collect legacy image ids)
2. DELETE images by id
3. DELETE images by user_id
4. DELETE consents
5. DELETE verifications
6. `subjectDeks.evict`

**There is no transaction.** Each attempt re-runs the whole sequence; it is idempotent.

**kyc results** (left = subject rows left after the dead-letter, as images/consents/verifications):
| fail point | value | base | head |
|---|---|---|---|
| none | ordinary Error | 1 attempt, acked, left 0/0/0, evict 1 | same |
| images-by-id always | ordinary Error | 3 attempts, DL 1, **left 3/1/1**, evict 0, 3 lines with message | same |
| consents always | ordinary Error | 3 attempts, DL 1, **left 0/1/1** (images already gone) | same |
| verifications always | ordinary Error | 3 attempts, DL 1, **left 0/0/1** (consents already gone) | same |
| consents once | ordinary Error | 2 attempts, completes, left 0/0/0 | same |
| any point | revokedProxy / getterThrows | same attempts/DL/rows as ordinary; bus receives **a different error** (TypeError / the getter's Error); **0 lines** | same attempts/DL/rows; bus receives the **original**; 1 line per attempt, `"unreadable thrown value"` |
| any point | message BigInt | same rows; bus receives **a TypeError** (`JSON.stringify` threw inside the catch); 0 lines | original; `"10"` |
| any point | message Symbol | same; field dropped | same rows; `"Symbol(ks1868)"` |
| any point | message object `{email}` | same rows; **the line logs `{"email":"subject@example.test"}`** | same rows; `"[object Object]"` |
| any point | string / null / BigInt thrown | field absent | same |

**wallet-connector results** (dev and production format):
- every value: `delete-always` gives 3 attempts, DL 1, **both subject sessions left**
- `delete-once` gives 2 attempts and completes
- the other user's session is never touched
- identity and log differences as in kyc
- **one difference by format:** in production format (winston `json()`, safe-stable-stringify), a BigInt message already logged `"10"` at base and the original was rethrown. The author's "base rethrew a different error for a BigInt message" holds for kyc and for wallet-connector's dev format only.

**Answer: identical? YES.** For both services, every failure point and both formats:
- head, unreadable = base, ordinary Error, in attempt count, rows erased and their order, rows left, dead-letter count and content, and ack
- the log shape matches too: one line per failed attempt with the `error` field set, where base logged nothing for the unreadable value

The only differences are the intended ones: the line now exists (with the constant), and the bus receives the original value.

**What is left unerased after the dead-letter** (pre-existing, G147-F1). By schema (migrations/002 :474-533, :813-820) plus the measured rows:
- **kyc, failing at images-by-id:** everything. That is the ID-document image rows (`data` on legacy rows), the consent (`ip_address`, `user_agent`, timestamps) and the verification (`provider_application_id`, `provider_check_id`, `liveness_score`, `overall_score`, `risk_level`, `status`, `review_notes`, `documents`).
  - `documents`/`review_notes` written as `d1:` are under the subject DEK, which originate destroys at step 11, so those two columns are crypto-shredded.
  - **Legacy `v<N>:` rows are under the platform keyring and stay decryptable** (the same class as KS-1953 / G145-F1).
  - The other columns are plaintext.
- **kyc, failing at consents:** the consent and verification stay.
- **kyc, failing at verifications:** the verification stays.
- **wallet-connector:** every `svc_wallet_sessions` row for the address (address, wallet_type, connected_at), all plaintext.

**Who is told: nobody** (READ):
- The bus acks and writes the dead-letter (`packages/shared/src/events/index.ts:194-213`).
- `git grep` over services/packages/scripts/deploy/docs finds **no reader of `secuura:events:dead-letter`**. The only `xreadgroup` is the bus's own loop on the subscribed types.
- Originate's `executeErasureImpl` marks the DSR `completed` at step 12 (gdprService.ts:899) and then publishes `user.erased` fire-and-forget at step 13 (:925). Nothing comes back.
- The only traces are the `handler failed` log lines (none at base for an unreadable value) and the dead-letter entry.

**Retries (READ):** the 3 attempts run back to back, with no delay (`while (attempts < maxAttempts && !handled)`, :184-192). A transient DB failure that outlasts three round trips dead-letters the erasure for good. Measured: a single failure recovers on attempt 2.

**KS-1953 interaction:** none. kyc and wallet-connector do not touch `document_lifecycle_events`. Both only consume the step-13 event, which originate publishes after step 11 whatever the lifecycle rows' state. The legacy `v<N>:` kyc rows are the same platform-keyring class, and are noted in G147-F1.

### Q2: Kam's ks1346 rule on the changed line (RUN with the real loggers; READ for reachability)
**Neither service has a file transport:**
- kyc: `console.log` JSON
- wallet-connector: winston Console only, in both formats

So no log file is written. logs/child_cwd is empty after every run, and Wednesday's `/Volumes/DevMASTER/WEDNESDAY/logs/combined.log` has mtime 06:01 local, before this gate started at ~06:45 local.

The one changed field is `error`:
- **ordinary Error:** the message as before (pg/driver error text; the same at base).
- **unreadable value:** the constant, a type statement, which complies.
- **non-string message:** now `String(m)`.
  - **For an object message this REMOVES a value leak.** Base serialised the object's fields WITH their values (measured: `{"email":"subject@example.test"}` in kyc and in both wallet formats); head logs `"[object Object]"`.
  - It newly logs a Symbol's description, a BigInt's digits, and whatever a custom `toString`/array join returns. An array's values were already logged at base as JSON.

**Reachability (READ):** the thrown value comes from `pg` through `query`, and pg errors carry string messages, with values in `detail`, which is not logged. `dbGetVerificationsByUser` and the decrypt helpers catch their own errors. So no changed line logs a value that could carry the erased subject's personal data from a real driver.

Pre-existing and unchanged: the same line carries `userId` and `dsrId`, and wallet's success line carries `walletAddress`.

**Compliant.** The object-message change is a small improvement that the author did not list (G147-F5).

### Q3: rethrow identity. RUN plus READ
- At base, for an unreadable value (and for a BigInt message in kyc / wallet-dev), the bus receives the TypeError or getter Error raised INSIDE the catch. At head it receives the original (`Object.is` true in every head cell).
- **The only consumer of the rejection is the bus's `catch { attempts++; }`.** It binds no variable, and the measured attempts and dead-letter are identical across identities.
- The handler is an inline closure passed only to `bus.subscribe` (callers: kyc index.ts:1323, wallet server.ts:322).
- The outer `.catch` on `subscribe()` fires only if the loop itself rejects, never on a handler rejection.
- Nothing upstream depends on the original value.

## 4. Re-measure
- **Red first** (base product, the new file): kyc **3 failed | 3 passed (6)**, wallet-connector **3 | 3 (6)**. R1-R3 in each, every one an `AssertionError`: R1/R2 on `same: false`, R3 on `'<symbol>'`. There were 0 timeouts (logs/*_red_base_new.log).
- **Head, new files:** 6/6 + 6/6.
- **Whole suites** (vitest `--root` anchored, cwd = logs/child_cwd):

  | service | base (without the new file) | head |
  |---|---|---|
  | kyc | **15 files / 84 tests** | **16 / 90** |
  | wallet-connector | **10 / 70** | **11 / 76** |

  All pass, rc 0. +1 file and +6 cells per service, nothing else moved, as claimed. I saw no load timeout on this host.
- **tsc including tests** (scripts/tsconfig.tests.<svc>.json: service tsconfig plus `src/**` with tests, `types: [node]`):
  - kyc: head **0** (16 test files, the PR file listed), base **0**, planted **1 TS2322**
  - wallet-connector: head **1**, base **1** (the same pre-existing `cardano-cip30.test.ts(8,32) TS6133`), planted **2** (+TS2322)
  - service `tsc --noEmit`: 0 / 0
- **eslint** (each service's cwd, root flat config):
  - product + new test file: rc 0 in both services
  - base product: rc 0
  - planted `debugger` + unused file: rc 1, 1 error + 1 warning, in both services
- **docs-fragments `check`:** rc 0 ("lint clean, render passes"; 2 ADVISORY render-range lines, not findings). Planted defects each gave rc 1 with a finding naming this file:
  - flow, unclosed div
  - flow, h2 without `<!--n-->.`
  - cheat, unclosed div
  - cheat, `</table>` corrupted

  Each was sha256-restored, rc 0 after (logs/frag_summary.log).

## 5. Mutants (scripts/mutants.py; product only, that service's new test file, sha256-restored after each; logs/mutants_table.log)
**22 mutants, 22 KILLED, all by assertion.**

| mutant | kyc | wallet-connector |
|---|---|---|
| M0 revert to base | R1-R3 | R1-R3 |
| M1 inner catch rethrows | R1 R2 | R1 R2 |
| M2 constant always | C1-C3 R3 | C1-C3 R3 |
| M3 wrong fallback text | R1 R2 | R1 R2 |
| M4 failure line dropped | all | all |
| M5 `error` field dropped | C1 C3 R1-R3 | same |
| M6 `String()` dropped | R3 | R3 |
| M7 undefined/null passthrough dropped | C2 | C2 |
| M8 rethrow a new Error (identity) | all | all |
| **M9 rethrow dropped (bus would ack a failed erasure as handled)** | all | all |
| **M10 swallow only when unreadable** | R1 R2 | R1 R2 |

The two mutants that would change the ERASURE outcome (M9, M10: the handler resolving, so the bus acks with no dead-letter) are pinned at function level.

## 6. merge-tree (scripts/mergetree.sh)
- Onto develop **`2f9f7db3`, as read at start** (logs/merge_tree.log): **rc 0**, tree `0a2b08e3`. The merged-vs-develop paths == the 6 PR paths, and both product blobs in the merged tree == the head blobs (`90503219`, `c31f288b`). The only squash since base (2f9f7db3, PR 1960, api-gateway redis.ts) overlaps 0 PR paths.
- Onto develop **`26955bf1`, as moved during the gate** (logs/merge_tree_develop_end.log): **rc 0**, tree `349645f6`, the same 6 paths and the same blobs. 0b381018 and 26955bf1 touch originate and transfer only; neither touches kyc, wallet-connector or the shared bus.
- Suites were not re-run on a merged tree.

## 7. Kam's ks1346 rule
No new log line, and the message, level and keys are unchanged. Every changed value complies (see Q2): the constant is a type statement, the readable message is as at base, and the object message is now `"[object Object]"` where base logged its field values.

## 8. Notes for the PR body
- **G147-F1 (HIGH, PRE-EXISTING, MEASURED; not caused by this PR, not a merge block): a failed kyc or wallet-connector `user.erased` cascade leaves the erasure silently incomplete.**
  - After 3 back-to-back attempts the bus dead-letters with a constant text and acks.
  - Nothing reads the dead-letter stream; no retry job exists.
  - The DSR was already marked `completed` (gdprService.ts step 12, before the step-13 publish).
  - kyc's four DELETEs are not in a transaction, so a mid-sequence failure leaves a partial erasure. Measured, by failure point:
    - images-by-id: everything stays
    - consents: consent (IP, user agent) + verification stay
    - verifications: the verification stays
  - wallet-connector leaves every session row for the address.
  - What stays is plaintext columns plus any legacy `v<N>:` kyc ciphertext (platform keyring, still decryptable); `d1:` columns are shredded by step 11.
  - Base's ordinary Error already produced exactly this; this PR only makes the unreadable case the same.

  Suggested ticket: (a) a dead-letter consumer or alarm that reopens or flags the DSR per service; (b) a backoff between attempts, or a re-delivery schedule instead of 3 immediate tries; (c) wrap kyc's deletes in `transaction()` (db.ts already has one) so a failure leaves all-or-nothing; (d) record per-service cascade completion against the DSR.
- **G147-F2 (recommended, docs):** the fragment says the bus behaviour is "read, not run". This gate RAN the real `EventBus.subscribe` loop with only Redis and the DB replaced; the PR may cite it. Suggested sentence for the flow fragment section .2: "Measured by the QA gate with the real bus loop: for every failure point the unreadable value gives the same 3 attempts, the same rows erased and left, and the same dead-letter entry as an ordinary Error at base; a failed cascade leaves the subject's rows in that service and nothing reports it to the DSR (pre-existing, G147-F1)."
- **G147-F3 (INFO, pre-existing, READ):** kyc `dbDeleteUserData` returns 0 when `isDbAvailable()` is false (index.ts:373). The handler then logs `handled` and the bus acks: an erasure silently skipped with no dead-letter. wallet-connector's handler never evicts `memConnectedWallets`, so in-memory sessions for the address persist until restart.
- **G147-F4 (INFO, pre-existing, READ):** the `user.erased` stream entry (userId, dsrId, performedBy, walletAddress) is acked but never deleted (no XDEL/MAXLEN in `publish`). A dead-letter copies the raw event into `secuura:events:dead-letter`. So the subject's wallet address persists in Redis after an erasure, whether it succeeded or not.
- **G147-F5 (INFO, logging, measured):** the author lists 42 and Symbol as the readable-value changes. Also changed:
  - an **object message** was logged WITH its field values at base (measured `{"email":...}`) and is now `"[object Object]"`, a ks1346 improvement
  - a custom `toString` or array message is now logged as its string form
  - a BigInt message in wallet-connector's production format was already `"10"` at base, with the original rethrown

  None of these is reachable from a pg error (string messages).
- **G147-F6 (INFO, measured):** every author figure re-measures:
  - red 3/6 + 3/6 by assertion
  - kyc 84 -> 90, wallet-connector 70 -> 76
  - tsc 0 -> 0 and 1 -> 1
  - eslint 0
  - fragments clean, with planted defects caught
- **G147-F7 (INFO, harness):** every vitest run was spawned with cwd = `<workdir>/logs/child_cwd`. Neither service's logger writes files, and child_cwd is empty. Nothing was written to Wednesday's tree (no `node_modules/.vite`, and `/logs/combined.log` mtime predates the gate). Develop moved from `2f9f7db3` to `26955bf1` during the gate; the head did not move, and merge-tree is clean onto both.

## 9. NOT TESTED
- the live PR body via the API (no gh login)
- a real Redis: the stream, consumer group, PEL, redelivery after a crash between attempts and `xack`, and NOGROUP recovery
- a real Postgres: the real SQL semantics, the FK `ON DELETE CASCADE` (modelled), and the in-band timing of the 3 attempts
- a booted service, and the HTTP admin path `DELETE` at kyc index.ts:1224, which calls `dbDeleteUserData` directly
- originate's publish side end to end
- the auth, m365 and other `user.erased` subscribers (not in this PR)
- the `subscriber loop terminated` catches (not changed)
- the `isDbAvailable()==false` path (READ)
- backups
- suites, tsc and fragments on the merged tree
- the four platform suites
- CI and the pre-push hook
- Node 24 or any LTS Node
- Spark shadow review (not requested)

## Processes
Every run I started has finished:
- npm ci + shared build (background)
- probes.sh (moved to the background by the harness; completed rc 0)
- suites.sh, static2.sh, mutants.py, mergetree.sh ×2

`ps` shows no process with this workdir in its command line.
