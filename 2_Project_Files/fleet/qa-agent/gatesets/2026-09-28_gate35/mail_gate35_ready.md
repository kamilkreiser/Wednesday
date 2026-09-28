# CAPTURE for gate35 (QA/Secuura-batch1321) — 2026-09-28T04:24:37Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (a listing would mark mail seen). Each PR's seat claims are captured from its
PR BODY, its COMMIT MESSAGES (over its develop merge-base) and the Seat B 37th records below, each verbatim with its TEXT_SHA256.

## #1321 KS-1348 (Seat B 37th (local-model patch, the Spark: KS-1348 r3 — originate utils/logger.ts keeps r2's Console redaction and adds a keepFileFields allow-list on both production File transports + a NEW ks1348 allow-list cell; replaces the CLOSED #1310), T1) — head 52c96db4cf495c4438ad989473ffb0bfe5ab5be3

#1321 ticket line: #1321 is KS-1348.

### PR BODY (gh_body_1321.md) TEXT_SHA256 2001e5edb1a31b0178c575b8f99064b3ea9cc42d9058aac9b1097114cc74fb0d

#1321 KS-1348: allow-list the originate production file log format to named safe fields
head 52c96db4cf495c4438ad989473ffb0bfe5ab5be3

## BLUF
The originate **production log files** stop receiving arbitrary metadata. Both File transports now
format through a `keepFileFields` allow-list, so a line holds only named safe fields. The Console
keeps the key-suffix redaction from #1310 unchanged.

**This PR REPLACES #1310**, which is open and was a NO GO: its redaction left a nested Error's
enumerable secrets and 16 unnamed secret/PII keys reaching both log files. Round 3 of the class,
authorised by Kam's ruling below. `Refs KS-1348` — not `Closes`; the ticket move is the gate's call.

## Kam's ruling, quoted
> Third attempt: allow-list the file format

(live board 2026-09-28 06:58 AEST, card `secuura-ks1348-r2-files-still-leak-allowlist`, option a.
The files record only named safe fields; redaction stays on the Console.)

## What changed
`services/originate/src/utils/logger.ts` — 2 hunks, **+41 / −2**:
- a `keepFileFields` allow-list format, and `format: combine(keepFileFields(), json())` on **both**
  File transports;
- `redactSecrets()` added last in the logger-level `combine`.

The allow-list is `timestamp, level, service, message, requestId, method, path, statusCode`, each
only when it is a string or a number, plus `error` when it is a string. Everything else is dropped.

New: `services/originate/src/__tests__/ks1348-production-file-logs-allow-list.test.ts`, **+203**.

## Test Evidence

**Touched:** `services/originate/src/utils/logger.ts` · the new test file. Nothing else.

**RAN — every figure measured in my own worktree at base `54f37d6399bd`, none copied:**

| what | result |
|---|---|
| `git apply --check --whitespace=error` at `54f37d63` | rc 0. A mutated-context control on `logger.ts:42` is **refused, rc 1** |
| **red, test-only** (product byte-identical to `HEAD`, blob `ca9a27ef13a4`) | **5 failed / 11**, by assertion: **A1 ×2, A3 ×2, B1** — and the 6 controls A0 ×2, A2, A4, A5, C1 green |
| **green, patched** | **11 / 11** |
| **whole originate suite, BASELINE at `54f37d63`** | **88 suites / 1041 tests / 0 failed / 0 pending** |
| **whole originate suite, PATCHED** | **89 suites / 1052 tests / 0 failed / 0 pending** |
| delta | **+1 suite, +11 tests** — exactly this PR's new file, so "no new red" is a measured delta, not a bare `0 failed` |
| `tsc` over a program **proven** to contain the new cell | rc 0, 0 errors. Same program at base with the cell held aside: rc 0, 0 errors. Program census: new cell 1, `logger.ts` 1, bogus-name control 0 |
| `eslint` on both changed files | rc 0 |

**The arm that proves the leak half discriminates** — the golden test run against **#1310's own
`logger.ts`** (blob `7706a8f6`, installed from `2cd351fad72d`): **4 failed — A1 ×2, A3 ×2, with B1
GREEN.** So the file-leak cells red against a logger that redacts the Console but still leaks into
the files, and B1 confirms the Console redaction is retained. The golden was restored afterwards and
its blob verified equal (`6b28e36519ac`), so no reported figure rests on the tamper run.

Two-stage apply check: applying the test half then the product half yields files **byte-identical**
(sha256) to applying the whole canonical patch in a clean scratch tree.

**NOT RUN / NOT COVERED — read this list, it is the point of the block:**
- 🔴 **The production log FILES no longer receive `userId`, `documentId` (27 uses in originate's
  logger calls), `ip` or `stack`.** That is what "closed world" means, and it is a deliberate
  consequence of the ruling, not an oversight. `middleware/errorHandler.ts` keeps `message`,
  `statusCode`, `path`, `method`; its `userId` and `ip` are dropped.
- **The Console is unchanged from #1310.** A nested Error and the unnamed keys still reach stdout,
  as they did at base. Redaction under development is unruled and carries over.
- A **string** `error` still reaches the files (gate33 W-3). That belongs to the KS 1346 remainder,
  not here.
- **No real fail500 route was driven** through the real logger — the test calls `logger.error` /
  `logger.info` directly. stdout itself was not read; B1 reads the line the Console transport
  formats at its `log` call.
- **No baseline delta for anything but originate.** No other service suite was run.
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6) were **not** run.
- **The push gate has no LINT leg**; the eslint figure above is me running the package's own lint by
  hand, and implies nothing about a CI lint pass.
- No Postgres, no local stack, nothing deployed.

**Migrations + config:** none. No migration, no schema change, no env var, no config file, no
OpenAPI change.

## Why replace rather than amend #1310
#1310's `logger.ts` is byte-identical to the r2 golden's product (`cmp`), and the arm above shows
that file still fails A1 and A3. The fix shape Kam ruled changes the transport *format*, not the
redaction predicate, so it is a different edit to the same two places — raised fresh against
`develop` rather than pushed onto a branch the gate already judged.

Refs KS-1348


🤖 Generated with [Claude Code](https://claude.com/claude-code)



### EVERY COMMIT MESSAGE IN THE CHAIN over 54f37d6399bd5eeb62a4c75220f42c106fad4b4a (oldest first) TEXT_SHA256 fa577a50da0b4c250cff13ac7022168d6282441229ccde1d6fdab8e9dc6f0f37

--- commit 52c96db4cf495c4438ad989473ffb0bfe5ab5be3
KS-1348: allow-list the originate production file log format to named safe fields

Both File transports now format through a keepFileFields allow-list, so a production
log line holds only named safe fields. The Console keeps the key-suffix redaction
unchanged. Replaces #1310, whose redaction left a nested Error's enumerable secrets
and 16 unnamed secret/PII keys reaching both log files.

Kam's ruling, live board 2026-09-28 06:58 AEST, card
secuura-ks1348-r2-files-still-leak-allowlist, option a: "Third attempt: allow-list
the file format."

Refs KS-1348

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-37th/raise/s-b37-ks1348r3-52c96db4cf49-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-37th/raise/s-b37-ks1348r3-52c96db4cf49-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-28T03:44:50Z PUSH START",
 "end": "2026-09-28T03:51:14Z push rc=0"
}
```

## #1322 KS-888 (Seat B 37th (local-model patch, the Spark: KS-888 mint — security index.ts gives dbSaveApiKey an opt-in { rethrow }; POST /api/keys drops the unsaved key and answers 503 / 500 with no key material + a NEW ks888 cell; revoke and validate UNCHANGED), T1) — head 4e8e11bdefd257e2cf1de48df2b68b8075f84b89

#1322 ticket line: #1322 is KS-888.

### PR BODY (gh_body_1322.md) TEXT_SHA256 ff5171ab457948927940fd7d14be7dc620db0000943428063de209564197c318

#1322 KS-888: a mint whose key save fails issues no key and answers 503 or 500
head 4e8e11bdefd257e2cf1de48df2b68b8075f84b89

## BLUF
`POST /api/keys` stops answering **201 with a key that was never stored**. `dbSaveApiKey` gains an
**opt-in** `{ rethrow }`, the mint opts in, and on a failed save the mint drops the in-memory copy and
answers **503 SERVICE_UNAVAILABLE** for an infrastructure fault or **500 INTERNAL_ERROR** otherwise —
**with no key material in the response**.

**This PR is the mint route only.** `Refs KS-888` — not `Closes`. Revoke and validate are unchanged
and remain open on the ticket under a separate card that is still with Kam.

## Kam's ruling, quoted
> Fix all three routes

(live board 2026-09-28 06:58 AEST, card `secuura-ks888-failed-key-save-design`, option b.)
**Mint is this PR.** Revoke and validate follow from card
`secuura-ks888-revoke-validate-on-failed-save`, which is OPEN and not yet ruled — so this PR
deliberately delivers one of the three, and says so rather than implying the ruling is discharged.

## What changed
`services/security/src/index.ts` — 3 hunks, **+22 / −5**:
- `dbSaveApiKey(k, opts: { rethrow?: boolean } = {})` — the swallow stays the default;
- `if (opts.rethrow) throw err;` inside the existing catch;
- the mint calls `dbSaveApiKey(apiKey, { rethrow: true })` in a `try`, and on failure
  `memApiKeys.delete(apiKey.id)` then answers `503`/`500` with a fixed message.

**Why opt-in and not a plain re-throw:** revoke and validate call the same helper from handlers that
take no `next`, so an unconditional throw becomes an unhandled rejection and those routes stop
answering. That is measured below, not assumed.

New: `services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts`, **+145**.

## Test Evidence

**Touched:** `services/security/src/index.ts` · the new test file. Nothing else.

**RAN — every figure measured in my own worktree at base `54f37d6399bd`:**

| what | result |
|---|---|
| `git apply --check --whitespace=error` at `54f37d63` | rc 0. A mutated-context control on `index.ts:288` is **refused, rc 1** |
| **red, test-only** (product blob verified == `HEAD`'s `7f9fe526c0e6`) | **5 failed / 9**, by assertion: **A1, A2 ×3, A3** — with controls **C1–C4 green** and **0** unhandled |
| **green, patched** | **9 / 9**, 0 unhandled |
| **whole security suite, BASELINE at `54f37d63`** | **25 files / 256 tests / 0 failed / 0 pending** |
| **whole security suite, PATCHED** | **26 files / 265 tests / 0 failed / 0 pending**, 0 unhandled |
| delta | **+1 file, +9 tests** — exactly this PR's new file, so "no new red" is a measured delta, not a bare `0 failed` |
| `tsc` over a program **proven** to contain the new cell | 2 errors, **both pre-existing `ks952-*`** (a TS2339 and a TS1343). The **identical** 2 errors appear at base with the cell held aside — `diff` of the two sorted error sets is empty. **0** errors name either changed file. Census: cell 1, `index.ts` 1, bogus-name control 0 |
| `eslint` on both changed files | rc 0 |

**The arm that proves the opt-in design is load-bearing** — the **ticket-shaped fix** (an
unconditional re-throw for SQLSTATE 42/23/22, i.e. for *every* caller) run against this PR's own test
file: **6 failed / 3 passed — A2 ×3, A3, and C2 + C3**, with **A1 green**. C2 and C3 fail with
`TimeoutError: The operation was aborted due to timeout` and vitest reports
**"caught 2 unhandled errors during the test run"**: revoke and validate never answer. So the
narrower opt-in is what keeps those two routes alive. The golden was restored afterwards and its blob
verified equal (`550e1b240cd5`), so no reported figure rests on the arm.

⚠ **Reporter caveat worth recording:** with `--reporter=json` that arm shows **0** occurrences of
"unhandled" — the JSON reporter does not emit the unhandled-errors banner. The 2 are only visible
under the default reporter. A count taken from JSON output would read 0 and look clean.

Two-stage apply check: test half then product half yields files **byte-identical** (sha256) to
applying the whole canonical patch in a clean scratch tree.

**NOT RUN / NOT COVERED:**
- **Mint route only.** Revoke and validate keep the log-only swallow; still open on the ticket via
  card `secuura-ks888-revoke-validate-on-failed-save`, pending Kam.
- 🔴 **Transient faults now REFUSE the mint (503).** The ticket's own original fix shape kept
  SQLSTATE 08/57 log-only. This follows the KS 1194 contract Kam ruled, where every failed save is
  refused and only the status differs — **that is Wednesday's reading of the contract, stated as a
  reading, not as Kam's words.** If he meant structural-only, this is a one-line narrowing.
- **With no database at all (`isDbAvailable()` false) the mint still answers 201 from memory** (C4),
  as KS 1194 kept its memory-only path. This PR does not change that.
- **No real Postgres.** The fault is planted at the mocked `query`. The gateway's handling of a 503
  from the mint was not read.
- **`check:openapi` was not run**, and the newly reachable 503 is not declared in the spec.
- **Co-file:** `services/security/src/index.ts` is shared with #1319 (KS 908), which is **MERGED**.
  This PR is based on `54f37d63`, which already contains it; #1319 was not touched. Measured: no
  **open** PR touches this file.
- **`services/security` has no `lint` script at all** — the eslint figure above is me invoking eslint
  directly, and implies nothing about a package or CI lint pass. The push gate has no LINT leg.
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6) were not run. Nothing
  deployed.

**Migrations + config:** none. No migration, no schema change, no env var, no config file. No
OpenAPI change (see the 503 note above).

Refs KS-888


🤖 Generated with [Claude Code](https://claude.com/claude-code)



### EVERY COMMIT MESSAGE IN THE CHAIN over 54f37d6399bd5eeb62a4c75220f42c106fad4b4a (oldest first) TEXT_SHA256 7dd7f2c2968091838a92fad4672ebab1c90d8beaf27c1dbb2ce0f219e89afd5e

--- commit 4e8e11bdefd257e2cf1de48df2b68b8075f84b89
KS-888: a mint whose key save fails issues no key and answers 503 or 500

dbSaveApiKey gains an opt-in { rethrow } and the mint opts in. On a failed save the
mint drops the in-memory copy and answers 503 SERVICE_UNAVAILABLE for an
infrastructure fault or 500 INTERNAL_ERROR otherwise, with no key material in the
response. POST /api/keys no longer answers 201 with a key that was never stored.

Opt-in rather than an unconditional re-throw: revoke and validate call the same
helper from handlers that take no next, so a plain throw leaves them unanswered.
Measured - the ticket-shaped fix fails those two cells with a timeout and two
unhandled rejections.

Mint route only. Revoke and validate follow from a separate card still pending.

Kam's ruling, live board 2026-09-28 06:58 AEST, card
secuura-ks888-failed-key-save-design, option b: "Fix all three routes."

Refs KS-888

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-37th/raise/s-b37-ks888mint-4e8e11bdefd2-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-37th/raise/s-b37-ks888mint-4e8e11bdefd2-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-28T04:02:12Z PUSH START",
 "end": "2026-09-28T04:07:53Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-37th/raise/s-b37-ks1348r3-52c96db4cf49-stubs.txt TEXT_SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-37th/raise/s-b37-ks888mint-4e8e11bdefd2-stubs.txt TEXT_SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855



