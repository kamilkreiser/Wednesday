# KS-888 validate, LOG-ONLY: Spark brief + golden (TEST-ONLY pin: the tip already answers from the key and logs one line)

Written 00:02 AEST 2026-09-29 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and the state of PRs #1322 and #1327 were only READ, by `build_input.sh`), mailed nobody and wrote nothing under `!CODING/`. Every git write verb ran under `scratchpad/bw0929/`. The existing REFUSE brief `../KS-888-validate/` was read for shape only: not edited, run or overwritten.

## The finding, plainly
**At develop `0d156d12` validate ALREADY does what Kam ruled (a, 2026-09-28 20:22:15).** It calls `await dbSaveApiKey(apiKey);` with no opt-in (`index.ts:1369`). `dbSaveApiKey` logs ONE line, `logger.error('DB save API key failed', { error: err?.message })` (`:332`), and re-throws only for callers that opt in (`:336`). Only the mint (`:1141`) and revoke (`:1293`, #1327) opt in. So a failed usage write is logged and never refused. Measured at the tip:
- 200 `valid: true` with the key's own `tenantId` and `scopes`, for SQLSTATE 08006, ECONNREFUSED and a code-less pool timeout;
- exactly one error line, and neither the key nor its sha256 appears in any `logger.error` / `logger.warn` / `console.log` call;
- 0 Unhandled.

**There is no defect to fix, so there is no red at the tip, and I did not manufacture one.** What the ticket still needs under ruling a:
1. A PIN: this brief, TEST-ONLY. Red is proved by the builder's `## Tamper` (the log line gains `k.keyHash`) and by the arms below.
2. Retire the REFUSE brief `../KS-888-validate/` (Wednesday's call, not mine). Its product hunk is the exact behaviour Kam ruled out, and it reddens this pin (5 failed, measured).
3. Two neighbouring issues, reasoned rather than driven and outside the ruling: see doubts 3 and 4.

- **Security rule:** no product edit at all. It fits in one file with one hunk, far inside "one file, 3 or fewer edits", so there is no escalation to a Claude seat.
- **Base:** develop `0d156d12cc0fc45fc323397c6999898565c44c54` (tree `c0497437f34c`), `bw0929/base`, porcelain 0, `packages/shared` rebuilt.
- **Gateway premise verified at this tip:** `api-gateway/src/middleware/auth.ts:228-231` turns any non-2xx from validate into `null` plus a 30 s negative cache (`:229`), and `:234-236` does the same for `valid: false`.

## Files
- `KS-888.md` is the brief (16,078 chars), TEST-ONLY with a `## Tamper` block (`index.ts:332`).
- `KS-888.golden.diff` is the golden, sha256 `7c1ba3e06226…`: 1 file (the test), 38 `+` lines (34 non-blank), 1 `-` line (the empty `:163`, rewritten as `-`/`+` so no context line is blank, as in the revoke brief).
- **Fence rebuild:** IDENTICAL to the golden (`cmp`). Mutated control: DIFFER.
- **Char lint of `+` lines:** 0 contain a backslash, a backtick, a double quote or a non-ASCII character. 0 blank or non-ASCII context lines.

## Measured (scratch copy at 0d156d12; vitest 4.1.10, node 24.7.0)

| step | result |
|---|---|
| `git apply --check` / `patch -p1 -F0 --dry-run` at the tip | rc 0 / rc 0; applied result `cmp`-identical |
| new cells at the UNTOUCHED tip | **19 / 19 green**, 0 Unhandled (the pin holds; this is the "tip already correct" measurement) |
| under the builder's tamper (`:332` also logs `keyHash: k.keyHash`) | **1 failed / 19**: V2 only, by ASSERTION (`hash: true`) |
| security suite | tip **26 files / 270 / 0 failed**; with the pin **26 / 275 / 0**; 0 Unhandled in each |
| `tsc --noEmit -p services/security` | rc 0 at the tip and with the pin (excludes tests) |
| tsc incl. tests (temp tsconfig, `exclude: []`) | rc 2 at the tip AND with the pin: the SAME 6 pre-existing errors in other files (`ks698r1`, `ks952` x3, `ks976a`, `ks976b`), 0 in the ks888 file. Control: planted `const x: number = 'x'` in the ks888 file added TS2322. (A first attempt that inherited the tsconfig's `exclude: src/__tests__` gave rc 0 and ignored the plant; the control caught it and it was discarded.) |
| eslint (run from `Blockchain/Dev`) on `index.ts` + the ks888 test | rc 0 at the tip and with the pin. Control: planted `var` + `debugger` in the test file gave rc 1. |
| **the real Spark checker on the golden as model output** (`spark_checker.sh` after `prepare_clone.sh`) | **SPARK RESULT: PASS**, A1-A7 all PASS in test-only mode. A4 planted the tamper: 1 failed / 19, assertion red, controls green. A5: 19 / 19. A2a anchor 1/1. |

**Arms** (the pinned test file against a variant `index.ts`; the tip restored and `cmp`-checked after):

| arm | result |
|---|---|
| tamper: the log line also carries `k.keyHash` | 1 failed / 19: V2 (`hash: true`) |
| `:332` deleted (no log line) | 1 failed / 19: V2 (`errorLines: 0`) |
| a second `logger.error` after `:332` | 1 failed / 19: V2 (`errorLines: 2`) |
| **REFUSE shape** (the `../KS-888-validate/` product hunk moved to `:1368-1369`) | **5 failed / 19**: V1 x3, V2 and the existing C3, all by assertion (`status: 503`) |
| `:1369` opted in with NO `try` | 5 failed / 19 by `TimeoutError`, plus 8 vitest "Unhandled" lines (the r2 unhandled rejection) |

The happy path V3 (the usage write lands: 200 valid, one write issued) is green at the tip, with the pin, and in every arm.

## build_input: rc 0
```
NIGHT_EXCERPT_TRIGGER_BYTES=60000 NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw0929/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-validate-logonly bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-888 <out>/input.json product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts test_file=Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts line=1369 ctx=65536 started_ok=mint-1322-revoke-1327-merged_validate-third-carved-by-card-ruling-a-2026-09-28-2022
```
Output, verbatim:
```
ticket KS-888 · In Progress (started) · Medium · assignee=kamil.kreiser@secuura.ai · updated 2026-09-28T12:37:49.971Z
attached PR #1327 (Secuura/Distributed_Secuura): merged
attached PR #1322 (Secuura/Distributed_Secuura): merged
WARN state is In Progress (started) — ADMITTED by started_ok: mint-1322-revoke-1327-merged_validate-third-carved-by-card-ruling-a-2026-09-28-2022
product file PINNED: services/security/src/index.ts (ticket names 1: ['services/security/src/index.ts'])
fix shape: WEDNESDAY BRIEF (KS-888.md) — the ticket's fix-shape/decision gates are bypassed; the brief states the change and any decision → 'The exact change'
product services/security/src/index.ts (72168 B, 1643 lines) defect line 1369 [pinned (line=)]: 'await dbSaveApiKey(apiKey);'
reference test PINNED: Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts
test_file PINNED (modify in place): Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts (10244 B) — suggested_test_file = it
  named sites: no '## Where' section — checklist empty (A3b passes vacuously)
  expected '+' lines from the brief's edit blocks: 34 (A3c)
  red cells declared by the brief: 1 ['pin KS-888 V2']
  TEST-ONLY tamper from the brief: services/security/src/index.ts:332 "logger.error('DB save API key failed', { error: err?.message" -> "logger.error('DB save API key failed', { error: err?.message"
  prompt source: WEDNESDAY BRIEF /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-validate-logonly/KS-888.md (16078 chars) — the ticket description is NOT the prompt
  suggested_test_file = the brief's `## The test` File: line Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts (== the title slug)
  EXCERPTED Blockchain/Dev/services/security/src/index.ts: 72168 B / 1643 lines -> 27378 B in 4 region(s) [(1, 363), (472, 525), (1116, 1166), (1268, 1413)] (anchored lines [1, 9, 10, 11, 18, 21, 23, 35, 50, 51, 58, 60]...)
contract: key set == KS-871 input (top-level, ticket, repo)
wrote /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw0929/bi_v/input.json (98980 B; ~24642 prompt tokens at 4 B/token — num_ctx 65536 leaves ~40894 for the answer)
```
KS-888 is In Progress (#1322 and #1327 merged), so `started_ok=` is required (see doubt 1).

## The round command (NOT run)
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw0929/round_0d156d12.sh KS-888-VALIDATE-LOGONLY KS-888 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-validate-logonly 60000 product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts test_file=Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts line=1369 ctx=65536 started_ok=mint-1322-revoke-1327-merged_validate-third-carved-by-card-ruling-a-2026-09-28-2022
```
**Round counter:** first brief for validate under ruling a. One rebrief is allowed, then it goes to the cloud. **Do not queue `../KS-888-validate/` (REFUSE) as well:** the two contradict each other, and both edit the same test file.

## UNMEASURED / doubts for Wednesday
1. **`started_ok=` is my assertion.** I could not see the lanes. Confirm nobody holds KS-888 validate.
2. **The ruling conflict.** Kam's 20:22:15 tap (a, log-only) and the 20:22:48 tap on the older card (refuse 503) disagree. This brief builds a, per your default. If Kam confirms "refuse", this pin is wrong, and the REFUSE brief's golden (written at `d9ce1403`) would need moving to this tip. #1327 shifted `index.ts` by 15 lines; the product hunk re-applied at `:1368-1369` in my arm, but its test hunks were not re-checked at `0d156d12`.
3. **A hung usage write is not covered.** Validate awaits the write before answering (`:1369`). The pool bounds only connection acquisition (`db.ts:33`, `connectionTimeoutMillis: 5000`), and I found no statement timeout. The gateway's fetch (`auth.ts:223`) has no timeout. A hung INSERT therefore delays or hangs every validate: a latency path to the lockout the ruling avoids. A fire-and-forget write (`void dbSaveApiKey(apiKey)`; it cannot reject without the opt-in) would close it. That is a design change Kam did not rule on. Not measured.
4. **Validate's "usage" save also writes `is_active`.** `ON CONFLICT ... SET ... is_active = EXCLUDED.is_active` (`:316-318`). A replica whose memory still says active could write `is_active = true` over a revoke that another replica stored. The measured premise "validate's save is only the usage counter" is therefore true of what validate CHANGES, but not of what the row write ASSERTS. Reasoned from source, not driven, multi-replica. This may deserve its own card.
5. **Key material in `err.message`:** the INSERT never sends the raw key (only `key_hash`, `key_prefix`). A Postgres cast error quotes the value in the message; the only cast is `tenant_id::uuid`, which is not secret. No real Postgres was used.
6. The test file's header comment (`:5-7`) still says "Validate keeps the swallow" and names C3. That is true under ruling a, so it was left alone.
