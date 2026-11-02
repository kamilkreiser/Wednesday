# QA Gate 103 verdict: Secuura/Distributed_Secuura PR 1921 (KS-1868, services/kyc/src/index.ts, O71-P1 dbSaveImage attestation catch :353 / O71-P2 verifyDbReady boot-probe catch :505), TIER 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Question A: I ran the real kyc app on a real loopback listener. The real `db.ts`, the real subject-DEK provider with real PII crypto, real RS256 JWT `authenticate`, the real kyc winston logger and the real shared `errorHandler` were all in place. Only the `pg` driver was replaced, by a recording Pool over in-memory tables. I ran 18 cells at base and at head: front, front+back with the BACK insert failing, and selfie; each with a control, an ordinary Error, a pg-like Error, a thrown string, a revoked Proxy and a throwing message getter. At head an unreadable value gives exactly what an ordinary Error gives: 500 `KYC_ATTESTATION_WRITE_FAILED` with the authored message, the same two log lines (with the constant in place of the message), and the same persisted state. **Persisted state is identical at base and head in every cell**: no attestation row for the failed image, no verification upsert, no document, row `pending`, liveness false, checks unchanged, no subject key minted. In front+back the front row persists for every kind and at both versions. Readable values are byte-identical at base and head. The judge script found 0 rule failures. Nothing is newly produced.
Question B: I booted the service as a **real `node` process** (tsx loader, only `pg` replaced). With an unreadable value, **base exits with code 1** after "KYC Service started" (`TypeError: Cannot perform 'get' on a proxy that has been revoked` at the `err?.message` line). **Head stays up** and logs `warn KYC DB verification query failed {"error":"unreadable thrown value"}`. An ordinary Error, a string or a plain object already logs and continues, at base and at head. So the change makes boot go on where it used to crash, and that is exactly the ordinary-Error behaviour. That is acceptable, because the crash at base was an accident of the log read and not a design.
C/E: the product diff is exactly 2 replace opcodes. The decrypt catches (:438/:457), PII init (:1293), the erasure subscriber (:1305), `dbDeleteUserData` (the GDPR cascade), `initDb().then` and the 4 ZodError prechecks are byte-identical. The five neighbouring guards from PR 1900 (96480cc6) are untouched: the constant appears 5 times at base and 7 at head. D: no new log key and no new value; at the unreadable path head logs strictly less thrown content than base.

## Heads
- START (logs/head_start.log, 02:22:27Z): `refs/pull/1921/head` = `8de72aa7cb480024d5ef469faf493e07400685ec` (as briefed), develop `04ff5262ad52...` (as briefed). Parent = merge-base `92a26320e30a...`; one commit; author Kam Kreiser, Co-Authored-By Claude Sonnet 5.5.
- END (logs/head_end.log, 02:42:28Z): PR head **unchanged** `8de72aa7`, local HEAD the same, product sha256 `51777965ea6c...` (head), working tree clean. **Develop moved** during the gate to `fcfa5dfd` (one commit: KS-1868 originate, 14 paths, all under services/originate plus two originate fragments). merge-tree was re-run against it (Q6).
- The product at develop `04ff5262` is byte-identical to the base product at `92a26320` (sha `1fe9f599a9d0...`). It is also unchanged at `fcfa5dfd`.
- Diffstat three-dot = two-dot: 5 files +410/-2. index.ts +14/-2; 2 new test files (+215, +137); 2 fragments (+22 each). Nothing outside the declared paths. This matches the READY mail.
- PR body not read (no Secuura gh auth used). I used the READY and BUILT AND PROVEN mails (evidence/) and the commit message.

## FINDINGS
- **G103-F1 (INFO, the tier-1 answer, measured)** Through the real app with only pg replaced, an unreadable value at head = an ordinary Error at head in status, body, both log lines and persisted state, for all 3 upload routes. At base it answered 500 `INTERNAL_ERROR` "An unexpected error occurred" and logged only the shared handler's line, carrying the TypeError text (or, for the getter case, the getter's own message). Persisted state at base = at head. No new outcome. (logs/probe_upload_table.log)
- **G103-F2 (INFO, measured; upgrades the PR's "read, not observed")** Real `node` boot: base + unreadable value at the boot probe gives **process exit 1** (unhandled rejection; on Node 26 the TypeError is printed). Head stays up with the constant warning. Ordinary/string/plainObject stay up at both versions. The fragment's ".3 Not run: a real boot ... read, not measured" can now quote this gate. (logs/boot_real_{base,head}.log)
- **G103-F3 (RECOMMENDED, test robustness, measured once)** Under load (load1 about 10-14), boot-probe cell C1 hit vitest's **default 5000 ms timeout** once (`5004ms`, in mutant run P1/M0, which did not touch P2's code). `bootAndSettle()` does a fresh module import plus up to 2.1 s of waiting, inside a default-timeout `it`. Fix: give the three boot cells an explicit timeout (`it(..., async () => {...}, 20_000)`). Not a merge block. Red-first and green were unaffected in my runs.
- **G103-F4 (LOW, test gap)** Mutant M6 (the readable non-Error branch `String(err)` -> `'x'`) SURVIVES at P1: no committed cell throws a readable non-Error. My route probe covers a thrown string at base and head (identical, `error: "db down (string)"`). Same gap as G90-F3. The branch is not changed by this PR.
- **G103-F5 (INFO, pre-existing, Kam's ks1346 rule)** For readable values both lines still log `err.message` verbatim, exactly as before. A real pg error on the `svc_kyc_images` INSERT (for example a constraint violation "Key (user_id)=(...)") could carry a value into the log. That is the ks1346 class, untouched by this PR, and the place for it is a ks1346 follow-up. The PR adds no key and no value. On the unreadable path, head logs the constant where base's errorHandler logged the TypeError or getter text.
- **G103-F6 (INFO, wording)** The fragment and mails say a thrown string or plain object at the boot probe logs `error: undefined`. With the real winston logger the key is dropped, and the line reads `KYC DB verification query failed {}` (measured at base and head). Same behaviour, more exact words.
- **G103-F7 (INFO)** The docs-fragments ADVISORY lines (flow 6249, cheat 6235) appear on develop alone (logs/frag_develop_now.log). They are not from this PR.
- **G103-F8 (INFO)** Develop moved to `fcfa5dfd` while this gate ran. merge-tree onto it is clean, 0 shared paths, and kyc is unchanged on develop. The PR head did not move.

## Q1. Heads + diffstat
See Heads. Paths: `services/kyc/src/index.ts`, `services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts`, `.../ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts`, `Projects Documents/fragments/{flow,cheat}/KS-1868-kyc-catches-unreadable-thrown-value.html` (logs/diffstat.log).

## Q2. The hunks (logs/product_diff.log, logs/untouched_sites.log)
- P1 :353 `logger.error('DB save image failed', { error: err instanceof Error ? err.message : String(err) });` -> `let reason: string; try { reason = err instanceof Error ? err.message : String(err); } catch { reason = 'unreadable thrown value'; }` + `logger.error('DB save image failed', { error: reason });`. The `throw new AppError(..., 500, 'KYC_ATTESTATION_WRITE_FAILED')` after it is unchanged.
- P2 :505 `logger.warn('KYC DB verification query failed', { error: err?.message });` -> the same guard with `reason = err?.message`, then `{ error: reason }`. No rethrow added.
- Unchanged: message texts, levels, keys, the AppError, `isDbAvailable` gates, the try bodies. difflib over the whole file finds exactly 2 non-equal opcodes (base 353 -> head 353-359; base 505 -> head 511-517). 1339 of 1341 base lines are equal.

## Q3. Behaviour (run, not read)
**Probe U** (scripts/probe_upload.test.ts, run by scripts/probe.sh, copied in for the run and then moved to logs/_quarantine; table by scripts/probe_table.py -> logs/probe_upload_table.log). Positive controls: `isDbAvailable: true` after the real `initDb()`, initiate 201 in every cell, and the success control 200 (front mints 1 subject key and stores encrypted documents; selfie sets liveness 0.95 and facial/liveness passed). All winston output is captured at the Console transport prototype, so both the kyc logger and the shared errorHandler logger are seen.

| cell (route / failing INSERT) | base: status, code | head: status, code | persisted (image rows / upserts after initiate / row / liveness), base = head | logs head |
|---|---|---|---|---|
| front, ordinary / pgLike / string | 500 KYC_ATTESTATION_WRITE_FAILED | same | 0 / 0 / pending / false | `DB save image failed {error:<message>}` + handler `Error occurred` (AppError) |
| front, revokedProxy / throwingGetter | **500 INTERNAL_ERROR** | 500 KYC_ATTESTATION_WRITE_FAILED | 0 / 0 / pending / false | `DB save image failed {error:"unreadable thrown value"}` + handler `Error occurred` (AppError) |
| front+back (back fails), all kinds | as the front rows | as the front rows | **1** (the front) / 0 / pending / false | as the front rows |
| selfie, all kinds | as the front rows | as the front rows | 0 / 0 / pending / **false**, checks still pending | as the front rows |

Base, unreadable: the only log line is the handler's `Error occurred {error:"Cannot perform 'getPrototypeOf' on a proxy that has been revoked"}` (or the getter's message). There is no `DB save image failed` line. Unhandled rejections: 0 in every cell at both versions. Judge: 0 rule failures (readable cells base == head in status, body, state and logs; unreadable head == ordinary head with the constant; unreadable persisted state base == head).

**Probe B** (scripts/boot_real.js + scripts/boot_preload.cjs: a real `node --import tsx` process of src/index.ts, NODE_ENV=development, PORT=0, only `pg` replaced; 8 s window per kind).

| kind | base | head |
|---|---|---|
| none | up, `KYC DB verified` | same |
| ordinary | up, warn `{"error":"db down"}` | same |
| string / plainObject | up, warn `{}` | same |
| revokedProxy | **exit 1**, TypeError at the `err?.message` line, nothing logged by the catch | up, warn `{"error":"unreadable thrown value"}` |
| throwingGetter | **exit 1** | up, warn with the constant |

Judgement on B: at head, boot carries on for an unreadable value, as it already does for every readable failure. The base crash came from the catch's own read, not from any design that intends to fail closed on a bad probe. Also, `listen` has already happened by then, so base "crashes after starting". Acceptable.

## Q4. Re-measure (Node v26.8.1, NOT Node 24)
- Head, 2 new files: **6/6** (logs/head_new_tests.log). Base product + new files: **4 failed | 2 passed**, all four by `AssertionError` (upload: `expected '{"success":false,"error":{"code":"INT…' to contain 'KYC_ATTESTATION_WRITE_FAILED'`; boot: `expected [] to have a length of 1 but got +0`). The C1 controls pass (logs/red_base_new_tests.log).
- Whole kyc suite: base without the new files **12 files 73/73**; base + new **4 failed | 75 passed (79)**; head **14 files 79/79**. Restore OK.
- tsc with the tests (scratch scripts/tsconfig.gate.json extending the service config, include src/**): head 0 errors (25 kyc files), base product + new tests 0, base pure 0 (23 files). Planted TS2322 in a new test file: rc 2, 1 error. Restored byte-identical.
- eslint (cwd services/kyc) on index.ts and the 2 new files: rc 0, 0 problems. Planted file: no-debugger error plus unused-var warning, rc 1.
- docs-fragments: clean rc 0 at head. Planted defects (flow unclosed div, flow `<!--n-->.` removed, cheat unclosed div, cheat `</table>` broken): rc 1 for each, all restored, rc 0 after. Merged tree: rc 0 ("74 new"). Develop alone: rc 0 with the same 2 ADVISORYs.

## Q5. Mutants (scripts/mutants.py; one site per run, product only, sha256 restored after every run, all `restore True`; logs/mutants_table.log)
15 runs: **14 killed, 1 survived.**

| Mutant | P1 dbSaveImage | P2 verifyDbReady |
|---|---|---|
| M0 revert the guard | KILLED R1 R2 (+ a boot C1 timeout, G103-F3) | KILLED R1 R2 |
| M1 drop the inner try | KILLED R1 R2 | KILLED R1 R2 |
| M2 constant -> re-read | KILLED R1 R2 | KILLED R1 R2 |
| M3 rethrow only when unreadable | KILLED R1 R2 | KILLED R1 R2 |
| M4 constant for all | KILLED C1 | KILLED C1 |
| M5 rethrow after log | KILLED C1 R1 R2 | KILLED C1 R1 R2 |
| M6 readable non-Error -> 'x' | **SURVIVED** (G103-F4) | n/a (no such branch) |
| M7 log removed | KILLED C1 R1 R2 | KILLED C1 R1 R2 |

Note: P1 is pinned at route level by the committed cells (they assert the HTTP body), unlike gate 90's function-level cells.

## Q6. merge-tree
- Onto `04ff5262` (the briefed develop): rc 0, tree `709026471f09...`, clean; it changes exactly the PR's 5 paths; 0 paths shared with develop's drift (analytics + billing).
- Onto `fcfa5dfd` (develop at END): rc 0, clean, exactly the 5 paths; kyc unchanged on develop (logs/merge_tree2.log).

## Q7. Kam's ks1346 rule
Both new lines keep the same key (`error`) and the same value as before for readable values. For unreadable values they log a fixed constant. No document data, image bytes, user id or new field is added. The neighbouring `log('info', 'KYC verification initiated', { userId })` is unchanged and outside this diff. Compliant for this PR. G103-F5 covers the pre-existing readable `err.message`.

## Q8. Notes for the PR body
1. G103-F1/F2: quote the gate's measurements. Route: base unreadable = 500 INTERNAL_ERROR with only the handler line; head = the ordinary bytes; persisted state identical. Real boot: base exit 1, head up.
2. G103-F3 (recommended): an explicit timeout on the three boot cells.
3. G103-F6: replace "`error: undefined`" with "`{}` (the key is dropped)".
4. G103-F5 as a ks1346 follow-up; G103-F4 optional cell (a readable non-Error throw).
No item is FIX-BEFORE-MERGE.

## Q9. NOT TESTED
A real PostgreSQL (rows are a model; the pg-like error is synthetic); the api-gateway hop; Node 24; the four platform suites; the pre-push hook (quoted only); the PR body text itself; production NODE_ENV formats (json logger, PII redaction format) for the new lines; whether any real driver ever rejects with an unreadable value (the values are synthetic, as at every KS-1868 site). The boot probe was observed for 8 s per kind, not longer.
