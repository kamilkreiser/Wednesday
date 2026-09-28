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

