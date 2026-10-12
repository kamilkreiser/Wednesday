# QA gate: Secuura Platform K PR #1504 (KS-1090 R2-2)

- Head: `a8be00f8c6ddd7dc51883c9d86a9db69685678de` (confirmed from the bundle; one commit, parent `037575399cba`, 4 files +59/-1)
- Base gated: real `origin/develop` = `6b978ca38442be9b8e54f176da9738cef430ee99` (includes V's leg 16). Merge with head is clean (merge commit `3e6508b2` in my scratch clone, diff vs develop = the same 4 files, +59/-1).
- Gate: Sonnet tier, independent. Scratch clones only, nothing written to !CODING, no Docker, no push, no real hook.

## VERDICT: GO WITH NOTE

Every number and every tamper the author claimed reproduces exactly; I found no Major issue, only that the ratchet shares auth's count-only blind spots and that, as decided, only the package script and the new cell guard the gateway.

## By my runs

Environment note: the clone has no install, so I built a node_modules shell that links the project's installed dependencies and points the workspace links (@secuura/*) at my tree. A first attempt that pointed @secuura/shared at the project checkout's older shared package gave 2 false TS2307 "NEW" errors (see Finding 3); after fixing that, everything below is on the corrected shell.

1. Config: `services/api-gateway/tsconfig.test.json` is byte-identical to auth's (`diff` rc 0). It extends `./tsconfig.json`, sets noEmit, `include src/**/*`, `exclude node_modules, dist`. The product `tsconfig.json` is unchanged and still excludes `src/__tests__`; `tsc --noEmit -p tsconfig.json` rc 0. All 113 files under `src/__tests__` are `.ts` and there are no `*.test.*` files elsewhere in the service (find, with the result 113 as a positive control), so nothing is outside the include except `vitest.setup.ts` at the service root (Note 4).
2. Checker on head: `tsc examined 148 files, 113 of them under __tests__; 35 errors: 35 in the baseline, 0 new; 0 stale` rc 0, 3.2 s wall (5 s user, matches the author's 2.6-3.2 s). Baseline recount by awk: 14 entries, 35 errors, 13 distinct files; TS2345 20, TS7006 6, TS18046 6, TS2322 2, TS2571 1. Matches the claim. Auth on the same head: 42 in baseline, 0 new, rc 0.
3. Gate cell: ks1090 file 1 passed (2 files matched my filter incl. an existing one, 5 tests, all green). Red control: baseline entry removed, the cell fails with the checker output as the assertion message naming `notifications.test.ts(179,24) TS7006` x3.
4. Gateway full suite on head: 113 files / 1086 tests passed (80 s CPU, 9 s wall). The same on the merged tree: 113 / 1086 passed. Auth ks1000 cell on merged: 7/7 passed.
5. eslint on the new test file: rc 0; positive control (a `var` file) rc 1, so the linter was live. tsc product config rc 0.
6. `npm run check:test-types` on the merged tree: runs auth then gateway, both 0 new / 0 stale, rc 0, 6 s wall.
7. Leg 16 on the merged tree (with the install precondition met): `bash scripts/preflight/test-types-ratchet.sh` (default, auth only) rc 0, "OK - 1 service(s)"; with `services/auth services/api-gateway` rc 0, "OK - 2". V's suite `scripts/__tests__/preflight_test_types_ratchet_leg.test.sh`: 23 passed, 0 failed (it pins `typecheck-tests: auth` and ` 0 new` from the checker; both still hold). The new root script is not called by leg 16 (leg 16 calls check.cjs directly), so it changes nothing for leg 16. `git grep check:test-types` finds only package.json and a CLAUDE.md sentence; no other consumer.
8. Tampers (head tree, restored after each, final control rc 0). Author's, 5 re-run, all EXACT:
   - planted TS2322 in a clean test: rc 1, names file and TS2322.
   - baseline entry deleted: rc 1, 3 NEW named.
   - stale entry: rc 1, STALE named.
   - count raised (10 to 11): rc 1, STALE "baseline 11, now 10".
   - count lowered (10 to 9): rc 1, 1 NEW with the 10 csrf errors listed (wording lists all 10 occurrences, fine).
   - tests excluded: rc 2, "NONE under __tests__".
   - include narrowed to one file: the checker alone rc 1 (13 STALE); with a baseline also narrowed it would not trip, which is what the cell's `> 100` floor is for.
   Mine, 8:
   - NEW test file `zz_new_gate.test.ts` with TS2322: rc 1, named (examined 149/114).
   - TS2345 (a code already in the baseline) in a different, new file: rc 1, named. Codes are keyed per file, so no cross-file laundering.
   - Baseline fingerprint moved to another file with the same counts (notifications TS7006 3 -> csrf TS7006 3): rc 1, 3 NEW plus 1 STALE.
   - Wrong tsconfig (`--tsconfig tsconfig.json`, the product one): rc 2, "examined 35 files and NONE under __tests__".
   - `--init` on the existing baseline: rc 2, "exists: use --update", baseline byte-unchanged.
   - Baseline file deleted, then planted error: rc 1 (36 new). Then `--init`: rc 0 and writes the planted error into the baseline silently (see Finding 2).
   - One error suppressed with `// @ts-ignore` plus one new TS2345 in the same file (count equal): rc 0, NOT caught (Finding 1).
   - `// @ts-nocheck` plus a planted error in a file with no baseline entry: rc 0, NOT caught (Finding 1).

## Findings

**Major: none.**

**Minor**

1. Count-only keying has two blind spots the claim ("can only shrink") does not mention: (a) fix one error and add another of the same code in the same file = same count, passes (tamper M); (b) `// @ts-ignore`, `// @ts-expect-error` or `// @ts-nocheck` hides errors; a file with no baseline entry can be silenced wholesale (tamper N); a file with entries goes STALE and is caught. These are the KS-1000 mechanism's properties and equally true of auth, so they are not new in this PR, but "a baseline that can only shrink" is stronger than what the mechanism guarantees. Evidence: runs M and N above.
2. `--init` is the one path that grows a baseline silently. It only works if the baseline file is absent, so it needs a visible deletion/re-add in the diff, but no check compares the baseline against develop. The reviewer's eye on the baseline diff is the only guard (the same holds for hand-editing a count up; the header says "Never edit a count up" and nothing enforces it).
3. The checker's result depends on the workspace packages being built to the right revision. With `@secuura/shared` resolving to an older install whose `dist` and package `exports` lacked `documents/default-type`, the gateway checker reported 2 "NEW" TS2307 errors (`routes/verification.ts(20,39)`, `services/enforcement.ts(10,39)`) and failed rc 1. That is a false red caused by the environment, not by the PR. leg 16's `deps-present.sh` checks tsx and `packages/shared/node_modules/@types/node` only, not shared's `dist`, so a stale build would read as a new test-type error. It fails safe (red, never a false green) and the error text is clear, so Minor.
4. `npm run check:test-types` is `auth && gateway`: if auth is red, the gateway is never run, so a developer sees one service at a time. Leg 16 deliberately does not short-circuit; the root script does. Cosmetic.

**Note**

1. As decided (not gated): leg 16's default list is `services/auth` only. After this PR the only things that protect the gateway are `npm run check:test-types` (manual) and the gate cell inside the gateway suite. Anyone who pushes without running the gateway suite is not stopped. Adding `services/api-gateway` to the default is one line and I verified it passes today (rc 0, "OK - 2"); V's leg-16 suite does not pin the default list beyond `services/auth` being in it, so a separate PR must also update the check "the default service is services/auth" in `preflight_test_types_ratchet_leg.test.sh` (it asserts the output contains `typecheck-tests: auth` and ` 0 new`, which would still hold, so it may not need a change).
2. CLAUDE.md (Blockchain root, ~line 388) says "`npm run check:test-types` runs it alone ... Only `services/auth` is gated today." After this PR the script runs two services while leg 16 gates one; the sentence is still true for the push gate but now easy to misread. A doc touch in the follow-up PR.
3. The cell's floor `> 100` against 113 files leaves a margin of 12 files that could be dropped (e.g. via an `exclude`) with no failure if their baseline entries are not affected. It is a coarse floor, as the author describes; it is correct today.
4. `vitest.setup.ts` (service root, outside `src/`) is not in the include, so it is not type-checked. Matches the product tsconfig's reach, not a regression.
5. The baseline header text says "KS-1000 ratchet" (it is the checker's own `--init` output), not KS-1090; harmless.
6. Timing: +3 s per `check:test-types` run and about +3-5 s in the gateway suite (the cell spawns tsc). Acceptable.
7. Wording item confirmed: this head was pushed before leg 16 existed; I ran leg 16 and its suite against the merged tree, both green. I did not run the real pre-push hook.

## NOT tested

- The real pre-push hook against any remote (forbidden); full preflight legs 1-15 on the merged tree (only leg 16 and its suite, plus deps-present).
- The services/originate half (the PR's other ticket half; not in this PR).
- Behaviour on a clean `npm ci` install (my tree used a linked shell of the project's existing install; the one real difference found is Finding 3).
- Windows/Linux, other Node versions (ran on Node 24.7, macOS). CI (Actions is retired).
- Any Docker, runtime, Kintsugi, demo or production behaviour. No GitHub or ticket writes.
- Whether `tsc` output ordering/line format changes across TypeScript versions (the checker parses `file(line,col): error TSxxxx`); only the installed version was used.
