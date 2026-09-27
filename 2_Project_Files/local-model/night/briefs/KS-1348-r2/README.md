# KS-1348 rev 2: Spark brief + golden (the ruled fix round, "Redact first, then JSON files")

Written 19:17 AEST 2026-09-27 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state and wrote nothing under `!CODING/`. Every git write verb (clone, fetch, checkout) ran in the scratchpad clone `ks1348brief/base`, which was fetched from origin develop by SSH.

- **Ruling:** Kam, live board 2026-09-27 19:06, card `secuura-ks1348-log-files-persist-secrets`, option a: "Redact first, then JSON files (recommended)".
- **Base:** develop `a24db57e65c9d0b96e8560ea7feaa0c764dee564`, confirmed by `git ls-remote` at 19:1x. `logger.ts` there is blob `ca9a27ef13a4`, the same as at `94c9c7aa`. The only changes since then are in adminConfig and webhooks, plus one test file.
- **Supersedes:** #1302 (OPEN, head `99374a3d`), which is attached to KS-1348. The raise is a FRESH PR against develop.

## Files
- `KS-1348.md` is the brief. `logger.ts` gets TWO hunks, and there is ONE new jest file of 146 lines.
- `KS-1348.golden.diff` is the golden. The diff rebuilt from the brief's fences matches it: **IDENTICAL**. Comparator controls: the same pair compared twice printed IDENTICAL, and a one-token mutation (`[REDACTED]` changed to `[REDACTE]`) printed DIFFER.

## The change (summary)
- **Hunk 1** (`@@ -42,7 +42,33 @@`). It inserts a redaction block before `:42`:
  - the regex `SENSITIVE_LOG_KEY`, which matches the END of a key, case-insensitive (password, passwd, secret, token, apikey, api_key, api-key, authorization, cookie, ssn, email, creditcard, phonenumber); this covers the `SENSITIVE_KEYS` list in packages/shared;
  - a recursive `redactLogValue` that copies and never mutates, passes Error, Date and Buffer through, and stops at depth 10 with `[TRUNCATED]`;
  - the `redactSecrets` winston format, which skips `level` and `message`.

  It also gives both File transports `format: combine(json())`.
- **Hunk 2** (`@@ -53,6 +79,7 @@`). It adds `redactSecrets(),` LAST in the logger-level `combine`. Redaction therefore runs before EVERY transport: the Console, and both files. It also runs in every environment (see the doubts below).
- There is no hunk 3, no new import, no dependency and no package.json change.
- Hunk 1 has zero leading context, because `:41` is blank. Its trailing context is non-blank. build_input's fence gates accepted it.

## Measured (scratch clone `ks1348brief/rg` at `a24db57e`, node_modules farmed by `prepare_clone.sh`, rc 0)

| step | result |
|---|---|
| `patch -p1 -F0 --dry-run` (golden on the develop blobs) | rc 0 |
| `git apply --check` | rc 0 |
| test file alone (RED) | **5 failed / 5 passed / 10**. The failures are exactly A1 x2, A3 x2 and B1, all by ASSERTION. A1 and A3 received `undefined`. B1 received the raw password sentinel. |
| golden applied (GREEN) | **10 / 10**. `logger.ts` matches the golden byte for byte. |
| `npx tsc --noEmit -p .` | rc 0 |
| `npx eslint` on logger.ts and the new test | rc 0, no output (the develop logger.ts is also rc 0) |
| whole originate suite (`npx jest`) | develop **84 suites / 983 passed**, golden **85 / 993 passed**, 0 failed. No new red. |

**Fail-ability arms** (the golden test run against variant `logger.ts` files; the golden was restored afterwards and checked with `cmp`):

| arm | failed |
|---|---|
| #1302's product (`json()` only, rebuilt from the PR diff) | 5 (A1, A3 x2 with `leaked` = all six keys, B1) |
| redaction not recursive | 5 |
| File `json()` dropped | 4 (B1 green) |
| key list without `email` | 4 |

The `+`-line lint found 0 lines with a backslash, backtick, double quote or non-ASCII. A control with a planted backslash line was flagged (count 1). There are 0 blank context lines.

## build_input: rc 0
```
NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c4dea74e-39e9-46e2-89c9-da9ac850c47f/scratchpad/ks1348brief/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1348-r2 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1348 <out>/input.json product=Blockchain/Dev/services/originate/src/utils/logger.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts line=45 ctx=65536 supersedes=1302 "started_ok=Kam-ruled-2026-09-27-19:06-card-secuura-ks1348-log-files-persist-secrets-option-a-Redact-first-then-JSON-files;fresh-PR-replaces-#1302"
```
The build output:
- the ticket is In Progress, and the first pass without `started_ok` REFUSED on that;
- #1302 is OPEN and ADMITTED by `supersedes=`;
- 26 expected `+` lines (A3c);
- red cells ['RED KS-1348 A1', 'RED KS-1348 A3', 'RED KS-1348 B1'];
- the prompt source is this brief;
- `suggested_test_file` = `ks1348-production-file-logs-redact-secrets.test.ts`;
- the contract key set is OK;
- tip `a24db57e`, input.json 32226 B, about 8025 prompt tokens.

The scratch `input.json` names a scratchpad `source_checkout`, so it must NOT be queued as is. The round seat should build its own. If the real Secuura checkout lacks `a24db57e`, a Secuura seat fetches first, or the coordinator writes `night/tip_override.txt`.

## UNMEASURED / doubts
- **No Spark round was run.** This is a brief and a golden only.
- **Dev-environment redaction.** The format sits at the logger level, so under development the colorized Console now shows `[REDACTED]` as well. packages/shared redacts in production only. The ruling says "logger-level", and the suite stayed green, but Kam has not ruled on dev logs being redacted.
- **Suffix matching** over-redacts any key ending in `token` or `secret`, such as a `csrfToken`, which is intended. It misses keys like `email_address` or `userEmails`. It ignores a string VALUE that merely contains an email (packages/shared also redacts `@`+`.` strings; this does not). The `error` / `err.message` free text is not redacted, by the ruling.
- Error instances nested in metadata pass through unredacted. An own enumerable secret property on an Error, such as an axios error's `config.headers`, is not walked. This is unchanged from develop's rendering.
- **The Console sink itself (stdout) was not captured.** B1 proves the logger-level format that feeds it.
- `tsc` with `src/__tests__` included was not run (tsconfig excludes it). ts-jest type-checked the test at run time.
- The gate's suggested extra row, a real fail500 route through the real logger, was not added. The test drives `logger.error` directly.
- **Hunk 1 has zero leading context.** This is new for a Spark brief. The KS-1346 briefs had 3 leading lines. It applies strict under both `patch -F0` and `git apply`, but whether the model reproduces a leading-context-free hunk is unmeasured.
