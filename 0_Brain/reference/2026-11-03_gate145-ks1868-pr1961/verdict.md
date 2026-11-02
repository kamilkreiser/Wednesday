# QA Gate 145 verdict: Secuura/Distributed_Secuura PR 1961 (KS-1868, originate errorTrackingService.ts getRecentErrors catch + lifecyclePayloadCodec.ts decrypt catch), TIER 1, round 1

## BLUF
**Q1 (GDPR erasure): NOT SHREDDED.** A lifecycle row skipped by the erasure sweep stays readable to anyone holding the platform keyring after the erasure completes. Step 11 destroys only the subject's own key (DEK), and these payloads are not encrypted under it: `encodeLifecyclePayload` uses `encryptField`, the platform-wide `v<N>:` keyring (lifecyclePayloadCodec.ts:34-38). This is **NOT a new outcome.** At base, an ORDINARY decrypt error already leaves the same row in the same state: same ciphertext, the email still in it, and the platform keyring still decrypts it. Head's unreadable-value after-state equals that state in every column (measured, table in section 3). So this is exactly the class bar ("unreadable now behaves like ordinary"). The gap itself is pre-existing (G145-F1).
**Verdict: GO WITH NOTES. Nothing has to be fixed before merge.**
Every figure the author gives re-measured:
- red first: 3/7 + 4/8, all by assertion
- originate suite: 200/2334 -> 202/2349, all pass
- tsc with tests: 0 -> 0
- eslint: 0 problems
- merge-tree: clean onto develop 4d1ab2cb

Q2 is confirmed and is pre-existing. It is only reachable through a message that no known driver produces, and only in the non-production log format (G145-F3).
Host Node v26.8.1 throughout. Nothing was measured on Node 24.

## Heads
- START (logs/head_start.log, 19:13:42Z): PR head `e5e0be51f21d76a10d6d2ceb9f94394b76d60df2` (= the pin), develop `4d1ab2cb6574e2b221353ac3a1de56d515711aaf` (= the commission's NOW). Merge-base `2d3b3bb3d386`; 1 commit.
- END (logs/head_end.log, 19:24:19Z): both unchanged. The clone's HEAD is `e5e0be51`, `git status` is clean, no `zz_g145_*` file is left in the tree (the probe, recorder and planted files are in logs/_quarantine). Product files were sha256-restored after every swap (suites_restore, probes_restore, probes2_restore, static_restore, tsc_summary, mutants restore=True x18).
- **PR body not read through the API** (this seat has no gh login). I used the author's READY mail (evidence/r76_pr1961_ready.txt) and the body draft `drafts/pr3/body.md` in Seat R 75th's history folder (read only).

## 1. Diffstat (logs/diffstat.log, three-dot)
6 files, **+316/-2**, exactly as declared:
- errorTrackingService.ts 7/1
- lifecyclePayloadCodec.ts 7/1
- two new jest files, 123 + 129
- flow fragment 28, cheat fragment 22

Nothing outside the declared paths.

## 2. The hunks (logs/product_diff.log)
- **Query** (errorTrackingService.ts:140): `- logger.error('Failed to query errors', { error: err instanceof Error ? err.message : String(err) });` becomes `+ let reason; try { reason = err instanceof Error ? err.message : String(err); } catch { reason = 'unreadable thrown value'; } logger.error(..., { error: reason });`. **No coercion of a readable message.**
- **Codec** (lifecyclePayloadCodec.ts:55): the same guard, but **with `String(...)`** around the whole expression, then `logger.error('lifecycle payload decrypt failed', { eventId, error: reason })`.
- What does NOT change: the empty answer `{ errors: [], total: 0 }`, the `payloadUnavailable` marker, the JSON.parse fallback, trackError, and every caller, gdprService.ts included (the PR does not touch it).

## 3. Behaviour

### Q1: the GDPR erasure path, traced at the head (READ), then RUN
`executeErasure` (gdprService.ts:562) -> `runWithPlatformScope(executeErasureImpl)` (:581). `executeErasureImpl` (:584-942), in order:
| step | line | what |
|---|---|---|
| 1 | 592 | DELETE share_records (sharer) |
| 2 | 598 | DELETE charge_events |
| 3 | 611 | certification_events actor rows: details allow-listed |
| 4 | 625 | audit_logs anonymised |
| 5 | 634 | DELETE document_access |
| 5b | 647 | action_provenance pseudonymised |
| 5c | 662-672 | subject email resolved from `users.email` through `readPii` (a `d1:` value decrypts under the subject DEK) |
| **5d** | **682-701** | `SELECT id, payload FROM document_lifecycle_events` (all rows), then per row `decodeLifecyclePayload` (**:688**), then `if (decoded.payloadUnavailable === true) continue;` (**:690**), then eraseEmailDeep, re-encode, UPDATE. Only rewritten rows are counted in the deletion log (:701) |
| 5e | 710-728 | shares |
| 5f/5g | 737-760 | recipient copies |
| 6 / 6b | 776 / 801 | documents |
| 7 / 8 / 9 | 829 / 843 / 849 | sessions / refresh tokens / consents |
| 10 | 870 | users row anonymised (email -> `deleted_<id>@anonymized.local`) |
| **11** | **893-894** | `subjectDeks.destroyDek(userId)`: NULLs the wrapped DEK in `pii_subject_keys` (shared subjectDek.ts:138-160). It is **the subject's DEK only** |
| 12 | 899 | DSR marked completed |
| 13 | 902-935 | USER_ERASED fan-out |
| outer catch | 938-941 | `success: false` |

**Which key encrypts the skipped row:** the platform keyring. `encodeLifecyclePayload` calls `encryptField` (shared encryptedField.ts:318: `getActive()`, master key `v<N>`, AAD `document_lifecycle_events.payload.<eventId>`). The codec header says so itself ("encrypted at rest with the platform keyring"). The shared module's own comment (encryptedField.ts ~:385) says the `v<N>:` format "makes single-subject erasure impossible to guarantee in backups (there is no per-subject key to destroy)". Step 11 therefore cannot shred a lifecycle payload: no lifecycle payload depends on the subject DEK.

**RUN** (scripts/probe_g145.test.ts; logs/probe/erasure_*.json, logs/erasure_table.log; 10 runs, all rc 0).
What runs for real:
- `executeErasure`
- the real codec at base and head
- the real `SubjectDekProvider` (wrap, unwrap, destroy)
- the real AES-GCM `encryptField`/`decryptField`/`encryptFieldWithDek` with keys generated in-process (test data)
- the real winston logger

What is replaced:
- `../db`: an in-memory stand-in that answers each SQL the erasure issues and records the writes
- `../events`: records the publish
- `decryptField`: wrapped ONLY in the hostile modes, so that it throws the hostile value for row E2's context

Data:
- `users.email` is a `d1:` ciphertext under the subject DEK
- E1 is a lifecycle row holding the email, which decrypts
- E2 is the "failing" row, holding the email:
  - `ordinary`: E2 is encrypted under platform key v2, and v2 is not loaded during the erasure, so the real decryptField throws its real Error
  - `revokedProxy` / `getterThrows` / `nullProto`: the decrypt of E2 throws that value
  - `none`: control

After the erasure, the probe registers the WHOLE platform keyring (v1 + v2) and tries E2.
| ver | mode | outcome | DSR completed | user row anonymised | subject DEK destroyed | E2 rewritten | E2 decrypts with platform keyring | E2 still holds the subject email |
|---|---|---|---|---|---|---|---|---|
| base | none | success | yes | yes | yes | yes | yes | no |
| **base** | **ordinary** | **success** | yes | yes | yes | **no** | **yes** | **YES** |
| base | revokedProxy / getterThrows / nullProto | **success false** ("Erasure failed") | **no** | **no** | **no** (subject DEK live) | no | yes | YES |
| head | none | success | yes | yes | yes | yes | yes | no |
| head | ordinary | success | yes | yes | yes | no | yes | YES |
| **head** | **revokedProxy / getterThrows / nullProto** | **success** | yes | yes | yes | **no** | **yes** | **YES** |

Head hostile = base ordinary = head ordinary, in every column. The one log line at :55 carries the event id and `"unreadable thrown value"`. The deletion log does not mention E2, and the erasure logs `Erasure completed`.

**Answer to Q1: NOT SHREDDED.** After a completed erasure at the head, the skipped row's personal data is still recoverable by any holder of the platform keyring, including from backups. Step 11 does not touch it, because its key is the platform key, not the per-subject DEK. The subject-DEK control behaves as designed: after step 11 `getDek` returns null.
**Is it new? No.** Base's ordinary-decrypt-error path already produces exactly this after-state (row 2 of the table). What the PR changes is only the hostile case. At base, the hostile case:
- aborts the whole erasure: `success:false`, the DSR not completed, the user row not anonymised, the subject DEK left alive
- is **not atomic**: E1 (earlier in the loop) and steps 1-5c had already been written (measured; base revokedProxy shows E1 rewritten)

At head, the hostile case lands in the ordinary state. Base's "retryable" state is also not a real remedy for a deterministic failure, because the retry hits the same row and aborts again (READ). The new state is quiet where the old one was loud (G145-F1).
Retry (READ, as the author says): `payloadUnavailable` is read only at :690. A second erasure resolves `subjectEmail` at 5c from a users row that step 10 already set to `deleted_<id>@anonymized.local` (plaintext, so readPii returns it as is), so it cannot match the address in E2. Nothing else re-visits the row. A later decrypt of E2 by `listLifecycleEvents` (lifecycleEventRepo.ts:138, tenant-scoped document listing) would show the email to whoever can list that document's events. That happens at base too, after an ordinary error.

### Q2: BigInt message at getRecentErrors (RUN, real logger; logs/rec_table.log)
Confirmed: an Error whose `message` is a BigInt makes `getRecentErrors` **reject** with `TypeError: Do not know how to serialize a BigInt`, **at base and at head, identically**.
- **It happens only in the non-production format.** The dev printf calls `JSON.stringify(meta)`. With `NODE_ENV=production` (winston `json()`, safe-stable-stringify) the same cell **resolves** at base and head: the console shows `"error":"10"`, and the file transports drop the field, because `keepFileFields` keeps only a string `error`.
- The codec's coercing guard turns the same value into `"10"` at head; at base it threw in dev.

Classification: **pre-existing** (the PR does not change the query cell's behaviour), not caused by the PR. **Reachability:**
- the query catch receives what `prisma.$queryRaw` rejects with, and Prisma/pg errors carry string messages (READ, not measured against a live driver)
- production uses the json format, which does not throw
- reachable only in development/test with a synthetic error

Follow-up: G145-F3.

### Q3: the class question per site (RUN, real winston logger, dev AND production format, 17 values x 2 sites x base/head)
| value | query base | query head | decode base | decode head |
|---|---|---|---|---|
| ordinary Error / string / 42 / undefined / null / Symbol thrown / BigInt thrown | empty list, line | SAME | marker, line | SAME |
| revoked Proxy / getPrototypeOf trap throws / message getter throws / null-prototype object / throwing toString | **REJECTS** (the read throws in the catch) | empty list, `"unreadable thrown value"` | **THROWS** (in erasure: aborts, see Q1; in listing: fails the whole list) | marker, constant |
| Error message is a Symbol | `{}` (field dropped by JSON) | SAME | field dropped | `"Symbol(m)"` |
| Error message is a BigInt | **rejects (dev)** / resolves (prod) | SAME | **throws (dev)** / `"10"` (prod) | `"10"` both |
| Error message 42 | `error:42` | SAME | `error:42` | `"42"` |
| Error message undefined | field absent | SAME | field absent | `"undefined"` |
| Error message is a null-prototype object | `{"error":{}}` | SAME | `{"error":{}}` | constant |
- **Unreadable after-state == ordinary after-state at both sites, in both formats.** That is the bar, and it is met.
- Persisted state: the query site has none. The decode site's effect on persisted state is the erasure row decision in Q1 (skip vs abort).
- Production log files were written by the real logger to **logs/child_cwd/logs/{combined,error}.log in this workdir** (jest was spawned with cwd there, see scripts/jest.js). Wednesday's `/Volumes/DevMASTER/WEDNESDAY/logs/combined.log` was not touched: its mtime is 06:01 local, before this gate started at 06:13 local (G144-F7 avoided).

## 4. Re-measure
- **Red first** (base products, the two new files; logs/red_base_new.log): **7 failed | 8 passed (15)**. Query R1-R3, codec R1-R4; every failure is an `expect` mismatch, 0 timeouts, 0 suite errors. As claimed (3/7, 4/8).
- **Head, new files only:** 15/15 pass (logs/head_new.log).
- **Whole originate suite** (jest, `-c`/`--rootDir` anchored, cwd = workdir): base without the new files **200 suites / 2334 pass, rc 0**; head **202 / 2349, rc 0**. +2 files, +15 cells, nothing else moved. As claimed.
- **tsc including tests.** Originate has no tsconfig.test.json, so I used scripts/tsconfig.tests.json, which extends the service tsconfig with src/** (tests included) and `types: [jest, node]`.
  - head **0 errors** (298 files, 232 under __tests__, both PR test files listed)
  - base **0** (296 files, 230)
  - planted test file: **1 error TS2322**, as planted
  - service `tsc --noEmit`: 0

  My first run (logs/tsc_summary_run1_TS2688.log) failed on TS2688 for `bcryptjs`/`cron` from typeRoots auto-inclusion. That was a harness error, not the PR, and it is fixed in the rerun. Originate is not a ratchet-gated service (no baseline file), as the author says.
- **eslint** (originate's own flat config, cwd originate): 4 changed files, **0 problems, rc 0**; base product files rc 0; planted `debugger` + unused file: rc 1, 1 error + 1 warning.
- **docs-fragments `check`:** rc 0, "lint clean, render passes" (107 new). Planted defects, each one rc 1 with a finding naming this file:
  - flow: unclosed div
  - flow: `<!--n-->.` removed from the h2
  - cheat: unclosed div
  - cheat: `</table>` corrupted

  Each was sha256-restored; rc 0 after (logs/frag_summary.log).

## 5. Mutants (scripts/mutants.py; product only, the new test file for that site, sha256-restored after each; logs/mutants_table.log)
18 mutants: **17 killed, 1 survived.**
| mutant | query | codec |
|---|---|---|
| M0 revert to base | KILLED R1-R3 | KILLED R1-R4 |
| M1 inner catch rethrows | KILLED R1-R3 | KILLED R1-R3 |
| M2 constant always | KILLED C1-C4 | KILLED C1-C4 R4 |
| M3 wrong fallback text | KILLED R1-R3 | KILLED R1-R3 |
| M4 log dropped / String() dropped (codec) | KILLED all | KILLED R3 R4 |
| M5 log drops `error` | KILLED, but by **suite compile error**, not a cell | KILLED, same |
| M6 codec: log drops eventId | | KILLED C1 R1-R4 |
| M7 query: instanceof -> message-presence / codec: marker -> `{}` | KILLED R2 | KILLED all |
| M8 query: rethrow instead of empty list / codec: marker -> rethrow (base's abort shape) | KILLED all | KILLED all |
| **M6 query: coerce with `String()` for all** | **SURVIVED** | |
- The two branches that decide the erasure (marker vs `{}`, marker vs rethrow) are pinned at the codec.
- The surviving query mutant is the coercion the query site LACKS. No query cell has a non-string readable message (the Q2 BigInt/Symbol/42 cases), so nothing pins either choice. The mutant is the fix G145-F3 recommends.
- M5's kills are compile-level (the now-unused `reason` under ts-jest); C1 would also catch it by reading.

## 6. merge-tree (scripts/mergetree.sh, logs/merge_tree.log)
- Onto develop `4d1ab2cb6574`, as read at start and at end: **rc 0**, tree `ec7692fe`. The merged-vs-develop paths == the 6 PR paths, and both product blobs in the merged tree == the head blobs (`2c174399`, `ef5476b1`).
- The five squashes since base: 4307ac87 (1956), cc33e702 (1953, zod), 0bd5e7bf (1957), 35d23ac6 (1958), 4d1ab2cb (1959). **PR-path overlap: 0.**
- 1953 (zod 3.25.76 -> 4.6.7) touched originate's `package.json` (`zod ^3.22.4 -> ^4.6.7`), `package-lock.json`, `src/index.ts` (zod3-compat import), and **`routes/gdpr.ts` and `routes/systemErrors.ts`**, which are the callers of `executeErasure` and `getRecentErrors`. In both routes the change only wraps request-validation issues in `zod3Issues(...)`; neither touches the call into the PR's functions.
- **Does the PR depend on zod? No:** the two product files and the modules they import (logger, erasureMarker, @secuura/shared crypto) name no zod (git grep rc 1; positive control: 13 originate src files name zod). The other four squashes touch no originate path.
- Suites were NOT re-run on the merged tree (that would need a fresh install for zod 4).

## 7. Kam's ks1346 rule (log type and field NAMES, never values)
- No new log line. The two existing lines keep message, level and keys (`error`, and `eventId` at the codec).
- The constant `'unreadable thrown value'` is a type statement: compliant.
- A readable message is logged as before (base practice, pre-existing for the class). For the codec it is crypto/keyring error text (e.g. "PII ciphertext was encrypted with key v2, which is not loaded…", "Unsupported state or unable to authenticate data"); no plaintext or key bytes are formed into it. The query site gets Prisma/pg error text.
- Codec coercion: a non-string message now becomes a string (`Symbol(desc)`, digits, `"undefined"`). Because `keepFileFields` keeps only a STRING `error`, those values now **also reach the production log files**, where base dropped them. That is the same content class as a string message, set in-process, and no secret carrier is known. Compliant (info, G145-F4).
- `eventId` is a row uuid, not PII. The erasure log lines carry `userId` (pre-existing, unchanged).

## 8. Notes for the PR body
- **G145-F1 (recommended follow-up, HIGH priority for data protection, pre-existing, MEASURED)** The KS-537 lifecycle payloads are encrypted under the platform keyring, not the subject DEK. Any row that step 5d skips keeps the subject's email recoverable by any holder of the platform keyring, in live data and in backups, after an erasure that reports `success: true`. The case was already reachable at base through an ORDINARY decrypt error (measured: a key version not loaded). The deletion log and the DSR record say nothing about it; the only trace is one error line with the event id. This PR routes the unreadable-value case into the same state, which is the class's stated bar, so it is not a merge block. The difference is that the old hostile path was loud (success false, DSR open), while the new one is quiet. Suggested shape for a separate ticket:
  - (a) count skipped rows, and do not mark the DSR plainly `completed` while any remain (record them in the deletion log as `skipped` with the event ids); and/or
  - (b) move lifecycle payloads to the subject-DEK (`d1:`) envelope, so that step 11 shreds them, as the KS-291 design does for users/consents/DSRs.
- **G145-F2 (recommended, docs)** Add one sentence to the body and to the flow fragment section 3: "The skipped row is NOT crypto-shredded by step 11: lifecycle payloads are under the platform keyring (`encryptField`), and step 11 destroys only the subject DEK. Measured by the gate: the row still decrypts with the platform keyring after a completed erasure, at base after an ordinary decrypt error and at head after an unreadable one." Also note that base's hostile abort was not atomic: earlier rows and steps 1-5c were already written.
- **G145-F3 (recommended follow-up, test gap + pre-existing)** At the query site, an Error with a BigInt message still rejects `getRecentErrors` at base and head, in the non-production log format only (production json resolves). It is not reachable from a Prisma/pg error (string messages; read, not measured). Query mutant M6 survives because no cell has a non-string readable message. Fix shape for the coercing follow-up Wednesday already holds: `reason = String(err instanceof Error ? err.message : err);`, plus a cell with an Error whose message is `10n`.
- **G145-F4 (INFO)** The codec now logs a Symbol / number / BigInt / undefined message as text, and the production log files now keep it (they dropped non-string `error` before). The author disclosed the Symbol and cyclic cases; the file-transport consequence is added here.
- **G145-F5 (INFO, measured)** The author's figures all re-measure:
  - red first 3/7 + 4/8 by assertion
  - originate 200/2334 -> 202/2349
  - tsc with tests 0 -> 0
  - eslint 0
  - fragments check with planted defects rc 1
  - "an ordinary decrypt error already skips the same way at base": confirmed by RUN, not only by reading
- **G145-F6 (INFO, harness hygiene)** Every jest run here was spawned with cwd = `<workdir>/logs/child_cwd`. The production-mode recorder's log files landed in `logs/child_cwd/logs/`. Wednesday's `/logs/combined.log` was not written by this gate.

## 9. NOT TESTED
- the live PR body via API (no gh login)
- a real Postgres/Prisma client: the erasure ran against an in-memory SQL stand-in that answers by statement prefix, so the real SQL semantics of the other steps are not exercised
- a real Key Vault / production keyring: keys were generated in-process
- whether a real decrypt ever throws an unreadable value: none is known; Node crypto throws Errors
- the HTTP routes (`POST /api/gdpr/erasure/:userId`, `executeErasureByExternalRef`, `/api/system-errors`) and a booted service
- a second erasure run against the same subject (the retry reasoning is READ)
- `listLifecycleEvents` (read only)
- backups
- suites, tsc and fragments on the merged tree
- the four platform suites
- CI and the pre-push hook
- Node 24
- Spark shadow review (not requested)
- gate 90's verdict, which the common commission names as the template: I used gate 144's as the nearest TIER 1 model, per the assignment

## Processes
Every background run I started has finished: npm ci + shared build, the suites, the probes (twice, the first erasure leg failing on an unused import in my probe), the static checks + mutants, the tsc rerun, and four Monitor/until waiters. `ps` shows no process with this workdir in its command line.
