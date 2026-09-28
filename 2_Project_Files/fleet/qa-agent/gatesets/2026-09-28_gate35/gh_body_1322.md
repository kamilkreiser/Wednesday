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

