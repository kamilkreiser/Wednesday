# KS-888 validate: Spark brief + golden (POST /api/keys/validate refuses with 503 when the key's usage save fails, and never answers valid)

Written 18:20 AEST 2026-09-28 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and PR #1322's state were only READ, by `build_input.sh`), mailed nobody and wrote nothing under `!CODING/`. Every git write verb ran in `scratchpad/ks888rv/base`, a `cp -a` copy of the carve drafter's `scratchpad/carve_base`. The original was only read: HEAD `d9ce1403` and porcelain 0 were verified before the copy, and its porcelain was 0 again after the final builder run.

- **Ruling:** Kam ruled KS-888 "b - Fix all three routes" (2026-09-28 06:58). The mint shipped as #1322. The card `secuura-ks888-revoke-validate-on-failed-save` went unanswered, and its DEFAULT (option a) applies from 18:00. For validate that means: when the save fails, REFUSE with 503. Fail closed: never answer valid.
- **Split:** this is one of two briefs. Its sibling is `../KS-888-revoke/`, whose README gives the reason for the split. **The two apply in either order (measured, below).**
- **Base:** develop `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`. That is the local clone's HEAD; `ls-remote` was refused because this seat has no Secuura SSH identity.
- **Shape:** the validate call opts in with `{ rethrow: true }` inside the handler's OWN `try`, because the handler takes no `next`. The catch logs one line and answers `503 SERVICE_UNAVAILABLE`, `success: false`, with no `data`, whatever the fault class. The mint's 503/500 classifier is deliberately NOT used here: the default says 503.
- **Edit points (3):**
  - `index.ts:1354-1355`: the validate save.
  - The test `describe` at `:98`, which says "revoke and validate are unchanged". It is renamed to a title that is true in either order.
  - The mint test's control C3 (`:130-136`), which asserted the OLD `200 valid: true` and would go red under this fix. C3 becomes red cell V4, and V1 x3, V2 and V3 are inserted before it.
  - Both test edits are in the mint's own test file, modified in place (`test_file=` pin).

## Files
- `KS-888.md` is the brief (21,076 chars).
- `KS-888.golden.diff` is the golden, sha256 `fa407fcc7ce9…`: 2 files, 43 `+` lines, 9 `-` lines.
- **Fence rebuild:** a diff rebuilt from the brief's two fences is IDENTICAL to the golden (`cmp`). The comparator control (a one-token mutation) printed DIFFER.
- **Char lint of `+` lines:** 0 contain a backslash, a backtick, a double quote or a non-ASCII character. There are 0 blank context lines.
- **One new shape:** the `-` line for `:1355` is whitespace-only (two spaces).

## Measured (scratch copy at d9ce1403; vitest 4.1.10, node 24.7.0)

| step | result |
|---|---|
| `git apply --check` / `patch -p1 -F0 --dry-run` at the tip | rc 0 / rc 0 |
| test hunks ALONE at the tip (RED) | **4 failed / 10 passed / 14**: exactly V1 x3 and V4, by ASSERTION. Each got `status: 200, valid: true` where 503 was expected. 0 Unhandled. |
| golden applied (GREEN) | **14 / 14**, 0 Unhandled |
| security suite | tip **26 files / 265 / 0 failed**; golden **26 / 270 / 0**; both siblings **26 / 275 / 0**; 0 Unhandled in each |
| `tsc --noEmit -p services/security` | rc 0 at the tip, with the golden, and with both |
| tsc incl. tests (temp tsconfig) | rc 2 in every state, the same 2 pre-existing ks952 errors, none in the changed files |
| eslint (run from `Blockchain/Dev`) | rc 0 in every state. Control: planted `var` + `debugger` gave rc 1. |

**Mint and happy paths unchanged:**
- The mint cells A1, A2 x3, A3, C1 and C4 are green in every state.
- V2 (a validate whose save lands answers 200 valid, and the INSERT was issued) is green before and after.
- V3 (no database: 200 valid from memory) is green before and after.
- With both goldens applied, only `index.ts:333-334`, `:1286-1287` and `:1354-1355` change, so the mint route (`:1046-1186`) is untouched.

**Arms.** The golden test was run against a variant `index.ts` each time. The golden was restored and checked with `cmp` after each arm.

| arm | result |
|---|---|
| `{ rethrow: true }` with NO `try` (the r2 shape) | **4 failed by TimeoutError + vitest "Unhandled Errors"** (the grep counted 7 lines). This reproduces the crash, and it is the positive control for the "0 Unhandled" figures. |
| fail open (the 503 made dead, so the handler falls through to 200 valid) | 4 failed: V1 x3, V4 |
| opt-in dropped (tamper) | 4 failed: V1 x3, V4 |

**Either order with KS-888-revoke:** each golden applies STRICT at the tip, and each still applies STRICT after the other, in both orders. Both orders give a byte-identical `index.ts` and test file (`cmp`). With both applied, the ks888 file is 19/19 and the suite is 26 / 275 / 0.

## build_input: rc 0
```
NIGHT_EXCERPT_TRIGGER_BYTES=60000 NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/carve_base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-validate bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-888 <out>/input.json product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts test_file=Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts line=1354 ctx=65536 started_ok=mint-merged-1322_revoke-validate-thirds-carved-by-card-default-1800
```
What the build printed:
- `prompt source: WEDNESDAY BRIEF …/KS-888-validate/KS-888.md (21076 chars)`.
- Red cells `['RED KS-888 V1', 'RED KS-888 V4']`.
- 37 expected `+` lines (A3c). All 37 are in the golden.
- `test_file` pinned, modified in place.
- The excerpt has 7 regions, including `1223-1398`.
- The input is 109,519 B, about **27.3K prompt tokens** (about 38.3K left).

## The round command (NOT run)
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/carve/round_d9ce1403.sh KS-888-VALIDATE KS-888 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-validate 60000 product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts test_file=Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts line=1354 ctx=65536 started_ok=mint-merged-1322_revoke-validate-thirds-carved-by-card-default-1800
```
**Round counter:** this is the first brief for the validate route. One rebrief is allowed, then it goes to the cloud.

**Order:** the round script clones the SOURCE at `d9ce1403`, so each round is graded alone against the tip, which is what the either-order proof covers. If one lands first, the other's golden still applies strict (measured). But its hunk headers are then off by the first one's line delta: +15 in `index.ts`, and +25 in the test file for revoke-first. The A2a anchor check would need the new base.

## UNMEASURED / doubts for Wednesday
1. **`started_ok=` is your assertion, not mine.** KS-888 is In Progress. Confirm that no live lane holds validate.
2. **Fail-closed is an outage lever.** A persistent structural save fault (e.g. migration drift, SQLSTATE 42703 on `svc_api_keys`) now refuses EVERY active `sk_*` key. That happens because the gateway treats any non-2xx as invalid (`api-gateway/src/middleware/auth.ts:228`). A transient fault locks that key out for 30 s, the gateway's negative cache (`auth.ts:229`). Today, the same faults answer `valid: true`. This is the default as written. It was read in the code, not driven through the gateway. **Kam may want to see this before it ships.**
3. **The default says 503 for EVERY failure class**, so a structural 42703 answers 503, not 500. This follows the wording exactly. If the mint's 503/500 split was meant, V4 and one line change.
4. **The in-memory usage bump is not rolled back** on a failed save (`lastUsedAt`, `usageCount`, `:1352-1353`). The default is silent on this.
5. **The test file's header comment (`:5-7`) goes stale** after both briefs land. It is owed as a one-line follow-up (see the revoke README).
6. **The whitespace-only `-` line (`:1355`) is unmeasured on the Spark.** Lenient apply would cover it (an accommodation).
7. There was no real Postgres. `check:openapi` was not run, and no 503 is declared for validate.
8. **Scope:** closes the validate third. With #1322 and KS-888-revoke, it covers all three routes Kam named.
