PR #1552 (KS-1547) head 762d044b05c9d1943d4d857e7f99e21b5b8d7e67: GO WITH NOTE
PR #1554 (KS-1542) head 3c15af5693fa3d841182a8b4fb2258fc02f825b4: GO WITH NOTE
sha256/16 (line 3 deleted, rest hashed): a99632143f942387

# Gate A, round 1 of 2: PR #1552 + PR #1554 (Tier 2, through-code, Opus)

Gate run 2026-10-15 ~17:03-17:20 AEST. Findings only; nothing fixed, nothing pushed, nothing merged.
Live develop re-read via `git ls-remote` at start and again at the merge step: 53b429ed6b4bf4d23c0721bf573b9df1c858bc06 (both times).
PR heads from `ls-remote refs/pull/N/head` match the brief exactly.
Clone: `/private/tmp/claude-501/gateA-170314/repo` (`git clone --shared` of the Blockchain checkout, origin set to GitHub with the checkout's core.sshCommand, fetched there). Worktrees under `.../gateA-170314/wt/`. Scripts under `.../gateA-170314/scripts/`. Raw outputs: `evidence/` beside this file.

## FOUND (severity, file:line)

### PR #1552
No product defect. Every one of the 16 real leg headers gives the same result on develop and the PR. `3/` and `3/x` still abort with rc=1.
- **N1, LOW (message fidelity)**: `Blockchain/Dev/scripts/preflight/preflight.sh:225,228,231`. A non-digit denominator now prints an empty denominator in the abort text. `step "3/x"` printed `says /x` on develop and prints `says /` on the PR (the same happens for `3/+16`, `3/-16` and `3/١٦`). It still aborts, and the full header is still quoted in the same line, so this is cosmetic.
- **N2, LOW/INFO (the widening is by design, stated so it is a decision and not a surprise)**: preflight.sh:225. Every header whose denominator is 16 followed by any non-digit is now accepted: `3/16x`, `3/16.5  T`, and `3/16/17  T` (a doubled or stale denominator). All of these aborted on develop. This is what "up to the first non-digit" means. `3/16/17` is the one a reviewer might not expect.
- **N3, LOW (test gap)**: `Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh:56-68`. No cell pins the abort for an empty or non-digit denominator, which is the path every non-digit header now takes. Three mutants SURVIVED the new suite:
  - N7 (`[ "$_hdr_total" -ne "$TOTAL_LEGS" ] 2>/dev/null`) lets `3/` and `3/x` through. It also survived all 8 `preflight_*` sibling suites (pass counts unchanged), so this abort is pinned nowhere in the tree. That was already true on develop.
  - N5 (`%%[[:space:]:]*`: a list of separators instead of "non-digit") survives because the test covers only TAB and colon.
  - N4 (`%%[!1-9]*`) survives because TOTAL_LEGS=16 contains no 0. It would break a future 10/20 total.

  Suggested cells (for the author, not done here): `3/` and `3/x` abort, `3/16)` is accepted, and one case with a denominator that contains 0.

### PR #1554
No product defect against the stated goal. Every probed object shape is still REFUSED, and the arrays and plain objects in the brief print as JSON. Production reachability: `services/api-gateway/src/index.ts:898` calls `createVerificationRoutes` WITHOUT `originateForwardTimeoutMs`, so in production the refusal message can only be reached by a future wiring or by tests. That caps every message-fidelity finding below at LOW.
- **M1, LOW (information loss: the answer to the brief's Map question)**: `services/api-gateway/src/routes/verification.ts:153-155`. `Map`, `Set`, `RegExp` and `Error` all print `{}`:
  - `new Map([['ms',800]])` prints `(got {})`; develop printed `[object Map]`.
  - `new Set([800])` prints `{}`; develop printed `[object Set]`.
  - `/800/g` prints `{}`; develop printed `/800/g`.
  - `Error('x')` prints `{}`; develop printed `Error: x`.

  This loses both the type and the content, and all four collide with a plain `{}`. Does it matter for an operator-supplied config value? Barely. A config value from env, JSON or YAML cannot be a Map, Set or RegExp. The value is refused either way (fail-closed), so only the diagnostic suffers, and the production caller passes no override (index.ts:898). Severity: LOW. A strict regression in wording for RegExp and Error.
- **M2, LOW (collisions the new branch introduces)**: verification.ts:155.
  - An invalid `Date` prints `null`, the same text as a literal `null` refusal (develop: `Invalid Date`).
  - `{toJSON:()=>1}` prints `1`, the text of an ACCEPTED bound. This breaks the test's own stated invariant ("No refused bound may print what an accepted bound prints"). Develop printed `[object Object]`.
  - `{toJSON:()=>undefined}` prints `undefined` at runtime, although `shown` is typed string.
  - Boxed `new Number(1)` prints `1`. This is not new: develop printed `1` too.
- **M3, LOW (the catch cannot be reached for the case it was written for)**: verification.ts:152 runs `String(value)` BEFORE the object branch at :153. For `Object.create(null)` and a revoked Proxy, `String()` itself throws a `TypeError` that does not name `originateForwardTimeoutMs`. The value is still refused, but with the wrong message. This is pre-existing, but the new try/catch (:154-158) looks like the fix for this class and does not get the chance.
- **M4, LOW (test gap)**: `.../__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts:160-165`. Mutant M2 (catch prints `String(value)` instead of `Object.prototype.toString.call(value)`) SURVIVED. The only catch cell uses a plain-object cycle, where both spellings give `[object Object]`. A `[1n]` cell would kill it: `String([1n])` is `1` (accepted text) and the type tag is `[object Array]`. The product comment names "a BigInt inside" as a reason for the catch, but no test covers it.
- **INFO**: the message is unbounded. A 20,000-element array prints an 80 KB message on both develop and the PR. Not new.
- Improvements confirmed: `[1n]` prints `[object Array]` (develop printed `1`, the accepted text); `new String('1')` prints `"1"` (develop printed `1`); `Date(0)` prints an ISO string.

### Environment notes (not PR findings)
- `preflight_test_types_ratchet_leg.test.sh` gives 25 passed / 9 failed on develop AND on the PR in this clone. The clone has no workspace install at the worktree used for the shell suites, and the suite itself says so ("no workspace install here"). The result is identical on both sides, so the PR did not cause it.
- **Stray file I created, which needs removal by someone allowed to delete**: `/Volumes/DevMASTER/WEDNESDAY/node_modules/.vite/vitest/da39a3ee5e6b4b0d3255bfef95601890afd80709/results.json`. My first vitest invocation ran through `npm --prefix ... exec`, which kept the cwd at the WEDNESDAY root, so vitest used it as root and wrote its cache there. That invocation also collected test files under `WEDNESDAY/2_Project_Files/local-model/spark/cache/work/...`. Its output was DISCARDED as invalid, and every run cited here used `vitest run --root <api-gateway>`. Per the no-delete rule I left the file in place. doctor.sh will flag `node_modules/` as a stray root entry.

## TESTED / HOW

1. **Diff by hunk** (`evidence/pr1552_diff_vs_mergebase.patch`, `pr1554_diff_vs_mergebase.patch`):
   - #1552 against merge-base e67e0dc1 changes exactly 2 files. Product: preflight.sh +1/-1 (one hunk, :225). Test: the new ks1547 suite +73.
   - #1554 against develop 53b429ed (an ancestor of the head) changes exactly 2 files. Product: verification.ts +10/-1 (one hunk, :150-159). Test: the ks1185-f1 file +26.
   - `git diff develop...head --name-only` lists nothing else for either PR.
2. **Red-first and green at the live tip**:
   - KS-1547, run with `/bin/bash` 3.2.57, the only bash on PATH, so the suite's inner `bash` is also 3.2 (`evidence/ks1547_red_green.txt`):
     - RED (develop preflight.sh blob 5fe66358 + the new test): 4 passed, 2 failed. Both failures are the TAB and colon cells, `want "0 yes no", got "1 no yes"`: the right reason.
     - GREEN (develop merged with #1552, tree c3e27419): 6 passed, 0 failed.
   - KS-1542 (`evidence/ks1542_red_green.txt`):
     - RED (develop verification.ts blob ed8003eb + the PR test): 6 failed, 19 passed. Real assertion messages: `expected '1' to be '[1]'`, `expected '' to be '[]'`, `expected '[object Object]' to be '{}'`, `'1,2'`, `'800'`, `expected [ '1', '800' ] to deeply equal []`.
     - GREEN (PR head): 25/25.
     - These match the author's claims.
3. **#1552 header audit** (`evidence/ks1547_header_audit.txt`):
   - Method: the test's own slicing method (preflight.sh's lines from `fail=0` to the first leg), run with /bin/bash against both develop and the PR. Inputs: all 16 real `step "N/16 ..."` headers, extracted from the file. preflight.sh is the only definer of a `step()` that parses N/TOTAL, apart from a stub in the tests.
   - Results: all 16 give rc=0 on both sides. `3/` gives rc=1 on both sides, with the same message. `3/x` gives rc=1 on both sides; only the message differs (finding N1). Positive controls `3/17  T` and `3/1616  T` abort on both sides.
   - Sibling suites before and after (`evidence/ks1547_sibling_suites.txt`): 8 `preflight_*` suites plus `pre_push_hook_base_leg_comment` and `pre_push_stack_legs_comment` give identical pass/fail counts on develop and the PR. The only failing one is the environmental ratchet suite above.
   - The full in-hook runner `run-shell-suites.sh` on develop and the PR: develop gives 86 passed / 2 failed of 88. The PR (develop + #1552) gives 87 passed / 2 failed of 89; the +1 is the new ks1547 suite, green. The same two suites fail on both sides, for environmental reasons in an uninstalled worktree:
     - `ks949_main_seed_idempotence`: "packages/shared is not built ... dist/index.js missing", aborted at cell 1.
     - `preflight_test_types_ratchet_leg`: no workspace install.

     The author's in-hook 89/89 and 88/88 are consistent with this, but I did not reproduce a full green here (`evidence/shellsuites_runner_*.txt`).
4. **#1554 shapes** (`evidence/ks1542_probe_shapes.txt`):
   - Method: a tsx probe built the REAL `createVerificationRoutes` with 27 values, on the PR head and then on the develop product, with the file swapped and restored (blob checked).
   - REFUSED with the property named on BOTH sides: Date, invalid Date, Map (empty and full), Set, RegExp, nested object, boxed Number/String/Boolean, toJSON objects, a class instance, `[1n]`, a cycle, a throwing getter, `[undefined]`, Buffer, Uint8Array, Error, a 20,000-element array, and the `null` control.
   - REFUSED, but with a TypeError that does not name the property: `Object.create(null)` and a revoked Proxy (finding M3).
   - Controls `1` and `undefined`: ACCEPTED.
   - What the PR prints:

     | Value | PR prints |
     |---|---|
     | Date(0) | `"1970-01-01T00:00:00.000Z"` |
     | Map | `{}` |
     | Set | `{}` |
     | RegExp | `{}` |
     | nested `{a:{b:[1,{c:800}]}}` | `{"a":{"b":[1,{"c":800}]}}` |
   - **Invariant cell**: it reads `DISTINCT` (declared earlier in the same `describe`) plus `OBJECTS`, as intended. The DISTINCT half is LIVE: reverting the bigint `n` suffix fails the KS-1518 cells AND the new invariant cell (3 failed, `evidence/ks1542_distinct_half_liveness.txt`). It does not cover the `REFUSED` table or the shapes outside the table (finding M2).
   - **Whole api-gateway suite** (`evidence/ks1542_full_suite_tsc.txt`): PR head gives 118 files / 1153 passed. Develop gives 118 / 1146 (+7 = 5 OBJECTS cells, the invariant cell and the cycle cell). This matches the author's claim.
   - **tsc**:
     - `tsc -p tsconfig.test.json` (the program includes the test file; `--listFilesOnly` count is 1) gives 35 errors on the PR and 35 on develop. The two outputs are byte-identical, with 0 errors in the PR's files.
     - PLANTED control: a type error appended to the PR's test file gives 36 errors, reported at that file, line 204. Restored afterwards.
     - Build program `tsconfig.json`: rc=0.
     - The repo's own `scripts/preflight/test-types-ratchet.sh`: "api-gateway ... 35 in the baseline, 0 new". OK for 3 services (`evidence/ks1542_test_types_ratchet.txt`).
5. **Mutation** (`evidence/mutants.txt`, `evidence/mutant_survivors_ks1547.txt`). Each mutant was checked to land (blob changed) and the file was restored to its blob afterwards.
   - #1552 (one product hunk):
     - Comment-only control N0: 6/0, it survives as expected.
     - KILLED: N1 (`%%[[:space:]]*`, by the colon cell), N2 (`%`), N3 (no `*`).
     - SURVIVED: N4, N5, N7 (finding N3).
     - EQUIVALENT: N6 (`[^0-9]`).
   - #1554 (one product hunk):
     - Comment-only control M0: 25/25, it survives as expected.
     - KILLED: M1 (no try/catch, by the cycle cell), M3 (`Array.isArray`, by `{}`), M5 (pretty-printed JSON, 3 cells), M6 (constant in the catch), M7 (JSON only when it looks numeric, 2 cells).
     - SURVIVED: M2 (finding M4).
     - EQUIVALENT: M4 (dropping `value !== null`, because `JSON.stringify(null)` and `String(null)` are both `null`).
6. **Merge prediction** on live develop 53b429ed (`git merge-tree --write-tree`, `evidence/merge_prediction.txt`):
   - #1552 alone: clean, tree c3e27419.
   - #1554 alone: clean, tree 485618bc, which equals its head tree (develop is an ancestor).
   - 1552 then 1554, and 1554 then 1552: both clean, tree **0b5143d06f5c85a21dfac9e56edd7d6d21067c4d**, which is the author's prediction. The combined diff against develop is exactly the 4 named files (+110/-2).
   - Overlap: 0 common files. Control: a file set intersected with itself gives 2.
   - Planted conflicting control: a develop-side commit editing preflight.sh:225 and verification.ts:152. Merging it with #1552 gives rc=1, CONFLICT in preflight.sh. Merging it with #1554 gives rc=1, CONFLICT in verification.ts.

## NOT tested
- Real `preflight.sh` end to end, i.e. the pre-push gate against a live gateway and stack. That needs the stack or Docker, which the brief excludes. step() was exercised only through the product's own sliced lines.
- `bash` 5.x behaviour. Only /bin/bash 3.2 exists on this machine, and that is what the hook runs.
- api-gateway behaviour with a real override wired from env. There is no production caller (index.ts:898).
- Locale effects on `[!0-9]` beyond the default UTF-8 locale. One Arabic-Indic digit case was tested and is treated as a non-digit on both sides.
- No GitHub, Linear, Docker or remote-box action. No BLOCKED.txt was needed.
