#1310 KS-1348: redact secrets before the originate file transports write JSON
head 2cd351fad72da3e4547a9cf5b887575239afb36f

## BLUF
Under `NODE_ENV=production`, `services/originate/src/utils/logger.ts` adds two File transports and gives
them **no format**, so every line written to `logs/error.log` and `logs/combined.log` is the literal text
`undefined`. The first attempt at this, #1302, gave the two transports `json()` alone — and the QA gate held
it, because every secret and PII field of a logged metadata object then reached both files, nested ones
included.

**The repository owner ruled on 2026-09-27: _"Redact first, then JSON files"_.**

This PR does that. A logger-level winston format replaces the **value** of any key naming a secret or PII
field with `[REDACTED]`, at any depth, **before any transport runs**; the two production File transports then
render JSON. The `message` and the error text still reach the files, which is what `fail500` exists to log.

**This replaces #1302.** #1302 is closed unmerged and nothing from it ships.

## What changes
- `services/originate/src/utils/logger.ts` (+29 / −2): a `SENSITIVE_LOG_KEY` pattern, a recursive
  `redactLogValue`, a `redactSecrets` winston format added **last** in the logger-level `combine`, and
  `format: combine(json())` on both production File transports.
- NEW `services/originate/src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts` (+146): loads the
  real module under `production` through `jest.isolateModules` with the cwd moved to a temp dir, logs one
  error carrying six sentinels, and reads back what winston actually wrote to each file.

**Two behaviour changes worth stating plainly, because neither is implied by the ticket title:**
1. **Redaction runs in EVERY environment**, not only production — the format sits at the logger level, so a
   development console now shows `[REDACTED]` too. `packages/shared` redacts in production only.
2. **Key matching is case-insensitive on the key ENDING**, so `recipientEmail` and `accessToken` match, and
   `email_address` / `userEmails` do not.

## Provenance
Patch produced by the **local model (the Spark) under a Wednesday brief**, and re-verified by this seat — the
harness's own figures are quoted below as the harness's, never as mine.

Measured here, not inherited: the READY block is **byte-identical** to the brief's golden **and** to the run's
canonical `patch.diff` (`cmp` rc 0 for both; all three sha256 `6381d31839954e36`). The READY's own header says
"golden not located — no identity claim is made"; the identity above is my measurement. Both sections apply
**strict** at the base (`git apply --check -p1`, no `--recount`, no fuzz), each with a tamper control that
fires: section 1 rc 1 on a mutated context line, section 2 rc 1 on a retargeted `+++` path
("already exists in working directory").

## Test Evidence

**Touched:** `services/originate/src/utils/logger.ts`; the new `ks1348-…-redact-secrets` cell. Base
`a24db57e65c9d0b96e8560ea7feaa0c764dee564`. Head commit +175 / −2 over exactly those two paths.

**Ran (all in this worktree, `npm ci` 1936 packages, `packages/shared` built):**

| what | result |
|---|---|
| RED — the new cell with the product hunk **out** (`logger.ts` restored to the base blob) | **5 failed / 5 passed / 10 total.** All five reds are `expect(received).toEqual(expected)` **assertion** failures, not load failures or mock crashes; all five controls green |
| GREEN — both files | **10 passed / 10 total** |
| EXTRA ARM — **#1302's own product swapped in** (json only, no redaction; blob fetched from its head at source) | the five rows go **RED**: `leaked: [password, token, apiKey, email, ssn, authorization]`, `markers: 0`. Controls stay green. This is the measured case for replacing #1302 rather than amending it |
| originate suite, `jest --runInBand`, BARE at the base | **983 passed / 983, 84 suites, 0 failed** |
| originate suite, `jest --runInBand`, PATCHED at my head | **993 passed / 993, 85 suites, 0 failed** — +10, **zero new reds** |
| `tsc --noEmit` over a program **proven to contain the new cell** | **rc 0, 0 error lines.** The package tsconfig excludes `src/__tests__`, so the default program (626 files) does **not** contain it; run through an `exclude: []` config the program is **717 files and contains the cell exactly once** (control: a filename that is not in the program counts 0) |
| `npm run lint` (`eslint src`) at the base | rc 0 — 0 errors, 22 warnings |
| `npm run lint` at my head | rc 0 — 0 errors, 22 warnings; the problem **set** is identical to the base's, line for line |
| lint control | a planted `debugger;` **in the new test file** takes lint to rc 1 with `no-debugger` at that file — so lint demonstrably sees the new cell. Restored by content, sha256 verified |

Every tamper was placed by an anchor asserted unique and restored by content with a whole-file sha256 compared
to the pre-tamper hash.

**NOT run, and why:**
- **No live stack**, so the in-hook preflight's legs 3, 4 and 8 do not run. The gate lines quoted are only the
  ones this push actually printed.
- **The Console sink itself (stdout) was not captured.** The B1 row proves the logger-level format that feeds
  it, which is one step short of reading the Console's own output.
- **No deploy of any kind.** Nothing was deployed and nothing here is deployed.

**Migrations + config:** none. No migration, no `package.json`, no `package-lock.json`, no dependency, no new
import, no environment variable.

## Not covered
From the brief's own README, carried here rather than dropped:
- **Dev-environment redaction has not been ruled on.** The ruling says "logger-level"; the consequence is that
  development console output is redacted too. Flagged, not decided.
- **Suffix matching over-redacts and under-matches.** It redacts any key ending in `token` or `secret`
  (a `csrfToken`, intentionally), and misses `email_address` or `userEmails`. It ignores a string **value**
  that merely contains an email address, which `packages/shared` does redact. The `error` free text is not
  redacted, by the ruling.
- **Error instances nested in metadata pass through unredacted** — an own enumerable secret property on an
  Error, such as an axios error's `config.headers`, is not walked. Unchanged from the base's rendering.
- **No stdout capture** (above).
- The README also listed "`tsc` with `src/__tests__` included was not run" as an open doubt. **That one is now
  discharged** — it was run here, rc 0, over a program proven to contain the cell.

One inconsistency in the source material, recorded rather than smoothed over: the README says "No Spark round
was run. This is a brief and a golden only", while the run that produced the identical `patch.diff` exists and
passed its checker 7/7. The two artefacts were written at different times; the bytes are identical either way,
which is the part that matters here.

Refs KS-1348

