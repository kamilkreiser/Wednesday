# KS-888 revoke: Spark brief + golden (DELETE /api/keys/:id answers 503/500 when the revoke's save fails, and keeps the in-memory revoke)

Written 18:18 AEST 2026-09-28 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and PR #1322's state were only READ, by `build_input.sh`), mailed nobody and wrote nothing under `!CODING/`. Every git write verb ran in `scratchpad/ks888rv/base`, a `cp -a` copy of the carve drafter's `scratchpad/carve_base`. The original was only read: HEAD `d9ce1403` and porcelain 0 were verified before the copy, and its porcelain was 0 again after the final builder run.

- **Ruling:** Kam ruled KS-888 "b - Fix all three routes" (2026-09-28 06:58). The mint shipped as #1322. The card `secuura-ks888-revoke-validate-on-failed-save` went unanswered, and its DEFAULT (option a) applies from 18:00. For revoke that means: 503 (infrastructure fault, the mint's classifier) or 500 (anything else), and KEEP the in-memory revoke.
- **Split:** one combined brief would need 5 edit points: two route saves, one C2+C3 test hunk, the `dbSaveApiKey` comment that says "only the mint opts in", and the test `describe` that says "revoke and validate are unchanged". That is over the kit's 3.
  - A 3-point combined brief is possible only by leaving those two texts false.
  - So this is one of two briefs. Its sibling is `../KS-888-validate/`. **The two apply in either order (measured, below).**
- **Base:** develop `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`. That is the local clone's HEAD; `ls-remote` was refused because this seat has no Secuura SSH identity.
- **Shape:** the revoke call opts in with `{ rethrow: true }` inside the handler's OWN `try`, because the handler takes no `next`. The catch copies the mint's classifier line (`index.ts:1143`) byte for byte, logs one line, and answers 503/500. The in-memory `isActive = false` is already in `memApiKeys` (`dbSaveApiKey:293` sets it before the INSERT), so it is kept without any code.
- **Edit points (3):**
  - `index.ts:333-334`: the `dbSaveApiKey` comment that says "only the mint opts in", reworded so it is true in either order.
  - `index.ts:1286-1287`: the revoke save.
  - One hunk in the mint's own test file `ks888-failed-mint-save-issues-no-key.test.ts` (modified in place, `test_file=` pin). Its control C2 asserted the OLD 200 and would go red under this fix. C2 becomes red cell R4, and R1 x3, R2 and R3 are inserted before it.

## Files
- `KS-888.md` is the brief (22,553 chars).
- `KS-888.golden.diff` is the golden, sha256 `278cbc455801…`: 2 files, 48 `+` lines, 8 `-` lines.
- **Fence rebuild:** a diff rebuilt from the brief's two fences is IDENTICAL to the golden (`cmp`). The comparator control (a one-token mutation) printed DIFFER.
- **Char lint of `+` lines:** 0 contain a backslash, a backtick, a double quote or a non-ASCII character. There are 0 blank context lines.
- **One new shape:** the `-` line for `:1287` is whitespace-only (two spaces).

## Measured (scratch copy at d9ce1403; vitest 4.1.10, node 24.7.0)

| step | result |
|---|---|
| `git apply --check` / `patch -p1 -F0 --dry-run` at the tip | rc 0 / rc 0 |
| test hunk ALONE at the tip (RED) | **4 failed / 10 passed / 14**: exactly R1 x3 and R4, by ASSERTION. Each got `status: 200` where 503/500 was expected. 0 Unhandled. |
| golden applied (GREEN) | **14 / 14**, 0 Unhandled |
| security suite | tip **26 files / 265 / 0 failed**; golden **26 / 270 / 0**; both siblings **26 / 275 / 0**; 0 Unhandled in each |
| `tsc --noEmit -p services/security` | rc 0 at the tip, with the golden, and with both |
| tsc incl. tests (temp tsconfig) | rc 2 in every state, the same 2 pre-existing ks952 errors, none in the changed files |
| eslint (run from `Blockchain/Dev`) | rc 0 in every state. Control: planted `var` + `debugger` gave rc 1. The first run from outside the base path ignored every file, and that control caught it. |

**Mint and happy paths unchanged:**
- The mint cells A1, A2 x3, A3, C1 and C4 are green in every state.
- R3 (a revoke whose save lands answers 200 "API key revoked", and the INSERT was issued) is green before and after.
- With both goldens applied, a line diff against the tip changes only `index.ts:333-334`, `:1286-1287` and `:1354-1355`. The mint route (`:1046-1186`) is untouched.

**Arms.** The golden test was run against a variant `index.ts` each time. The golden was restored and checked with `cmp` after each arm.

| arm | result |
|---|---|
| `{ rethrow: true }` with NO `try` (the r2 shape) | **5 failed by TimeoutError + vitest "Unhandled Errors"** (the grep counted 8 lines). This reproduces the crash, and it is the positive control for the "0 Unhandled" figures. |
| in-memory revoke rolled back in the catch | **1 failed**: R2 only, so R2 pins the default's KEEP |
| `res.status(infra ? 503 : 500)` changed to `res.status(500)` | 3 failed: R1 x3 |
| opt-in dropped (tamper) | 4 failed: R1 x3, R4 |

**Either order with KS-888-validate:**
- Each golden applies STRICT at the tip with both instruments.
- Each still applies STRICT after the other, in both orders.
- Both orders give a byte-identical `index.ts` and test file (`cmp`).
- With both applied, the ks888 file is 19/19 and the suite is 26 / 275 / 0.
- The two test hunks meet at `:129` (`  });`), which both keep as context. No line is changed by both.

## build_input: rc 0
```
NIGHT_EXCERPT_TRIGGER_BYTES=60000 NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/carve_base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-revoke bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-888 <out>/input.json product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts test_file=Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts line=1286 ctx=65536 started_ok=mint-merged-1322_revoke-validate-thirds-carved-by-card-default-1800
```
What the build printed:
- `prompt source: WEDNESDAY BRIEF …/KS-888-revoke/KS-888.md (22553 chars)`.
- Red cells `['RED KS-888 R1', 'RED KS-888 R4']`.
- 43 expected `+` lines (A3c). All 43 are in the golden (the 5 blank `+` lines are not gated).
- `test_file` pinned, modified in place.
- The excerpt has 7 regions, which cover both edit sites (`267-380`, `1223-1398`).
- The input is 108,687 B, about **27.1K prompt tokens** (about 38.5K left).

**The builder refused once, before this rc 0.** Its first refusal was the context-as-addition gate: C2's surviving lines were written as `-` and `+`. Fixed: they are now context. Its second refusal was the state gate: **KS-888 is In Progress**. That is why the command carries `started_ok=` (see doubt 1).

## The round command (NOT run)
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/carve/round_d9ce1403.sh KS-888-REVOKE KS-888 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-revoke 60000 product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts test_file=Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts line=1286 ctx=65536 started_ok=mint-merged-1322_revoke-validate-thirds-carved-by-card-default-1800
```
**Round counter:** this is the first brief for the revoke route. One rebrief is allowed, then it goes to the cloud.

## UNMEASURED / doubts for Wednesday
1. **`started_ok=` is your assertion, not mine.** KS-888 is In Progress (#1322 merged). The pin admits the build only if no live lane holds revoke or validate. I could not see the lanes. Confirm, or drop the round.
2. **The kept revoke is per process.** Other replicas, and this one after a restart, still see the key as active in the database. The 503/500 tells the caller the revoke was not stored, and nothing retries it. That is the default as written, but it was not measured against more than one replica.
3. **This brief rewords a comment that #1322 added** (`index.ts:333-334`, inside `dbSaveApiKey`, not the mint route). The mint's CODE is byte-unchanged. If "the mint must stay unchanged" is meant to cover that comment too, drop hunk 1 and the comment goes stale ("only the mint opts in").
4. **The test file's header comment (`:5-7`) goes stale** after both briefs land. It still says revoke and validate keep the swallow, and names C2 and C3. Fixing it would be a 4th edit point in a file both briefs touch. It is owed as a one-line follow-up.
5. **The whitespace-only `-` line (`:1287`) is unmeasured on the Spark.** If the model drops the two spaces, only the checker's lenient `--ignore-whitespace` mode applies the diff (an accommodation, not a model fault).
6. There was no real Postgres; the fault is planted at the mocked `query`. The production path, where `dbGetApiKey` returns a fresh DB object, was reasoned rather than driven. `check:openapi` was not run, and no 503/500 is declared for revoke. The gateway's handling of a revoke 503/500 was not read.
7. **Scope:** closes the revoke third. Refs KS-888, and does NOT close it alone.
