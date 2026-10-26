# Gate round 1: PR #1708 (KS-1728) and PR #1709 (KS-1554). Tier-2 findings-only, row G2

Gate agent: claude-sonnet-5-5. Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate_r1708_v1709_20261026/` (repo, merged worktrees `m1708`, `m1709`, `dev`, logs). Nothing pushed, commented or edited anywhere.

## Pins and ls-remote readings
| ref | pin | start 19:45:38 AEDT | end 19:59:40 AEDT |
|---|---|---|---|
| develop | e9e32b76b0483b65eb94cffdcf09da0c9ea46ce2 | same | same |
| #1708 head | a6bb564a9bf53f7d310adc4a4af672783c9ffd3e | same | same |
| #1709 head | f1abd08594ecdc76fee9731be32459fc3f8ecd5f | same | same |

Nothing moved. Merge-bases: #1708 on fee13f25d574, #1709 on 1f2ec373bdad. Merged trees are `git commit-tree` of `merge-tree --write-tree` (parents develop + head): m1708 = 8e724d3b1f65, m1709 = 3139e4183d13.

## BLUF
| PR | ticket | head | verdict | one line |
|---|---|---|---|---|
| #1708 | KS-1728 | a6bb564a9bf5 | GO WITH NOTES | Exactly 4 lines/3 files, grading unchanged, counts identical, every line red-proofed; 3 sibling lines left (consistent with the stated scope); does not explain the 3 refusals and says so. |
| #1709 | KS-1554 | f1abd08594ec | GO WITH NOTES | 5-service ratchet green on merged tree, planted violations go red naming the file, leg suite 39 to 43, vitest 361 unchanged; the 6-vs-2 error discrepancy is unexplained; CLAUDE.md:399 is now stale (ruled). |

Merge order: **#1708 first, then #1709** (no file overlap, any order merges clean; #1708 is tiny and removes a flake class from suites #1709's pre-push runs; no dependency either way).

Both together: `merge-tree` of pr1708+pr1709 gives the same tree 84717fce9a28 in both orders, rc 0, no conflicts. File overlap between the PRs: 0 (f1708.txt vs f1709.txt, `comm -12` empty). Files develop moved since each merge-base overlap neither PR (0 and 0).

---
## PR #1708 (KS-1728)

### FOUND
- **Note** The diff against merge-base fee13f25d574 is exactly 3 files, +4/-4, the four lines named. Lines read at the head:
  - `check_shared_relink.test.sh:49` `if [ -n "$want_out" ] && ! grep -qF -- "$want_out" <<<"$out"; then` (was `! printf '%s' "$out" | grep -qF -- "$want_out"`). Same `-qF --`, same pattern, same negation, same branch (the "WRONG rule fired" FAIL).
  - `ks1355_slot_blind_launchers.test.sh:68` `saw() { if grep -qF -- "$1" <<<"$2"; then echo yes; else echo no; fi; }` Same flags, same yes/no branches.
  - `preflight_deps.test.sh:443` `elif grep -q "could not derive the pre-push hook's own control" <<<"$out"; then verdict='HOOKCTL-REFUSED'` and `:444` `elif grep -q 'de-slotted .* variable' <<<"$out"; then`. Patterns and flags byte-identical; position in the elif chain unchanged.
- **Note** Semantic difference: a here-string appends a trailing newline that `printf '%s'` did not. For line-oriented grep with no `-x`/`$`-sensitive empty-string cases, that does not change a match. No pattern in the four lines is anchored on end-of-input.
- **Minor** Untouched neighbours in the same chain, same exposure under `set -uo pipefail` (`preflight_deps.test.sh:24`): `:441` `if   printf '%s' "$out" | grep -q 'step header .* disagrees with TOTAL_LEGS'; then verdict='HEADER-MISMATCH'`, `:442` `elif printf '%s' "$out" | grep -q 'could not measure what'; then verdict='DESLOT-REFUSED'`, `:453` `if [ "$prc" -eq 0 ] && printf '%s' "$out" | grep -q 'PREFLIGHT PASSED\|Nothing failed'; then verdict='SUITES-GREEN'`. Leaving them is consistent with the commit message ("the four observed lines only ... including preflight_deps.test.sh:441, 442 and 453 in the same elif chain") and the ticket census, but it leaves one elif chain with two pipe forms. Same class at 441/442 would mis-grade to a later branch. Not a defect of this PR; a follow-up decision for Wednesday.
- **Note** Honesty clause holds. I read the **commit message** (`git log fee13f25d574..pr1708`, commit 1f1a2bba5), not the PR body: `gh` has no login in this session (`gh auth status`: "You are not logged into any GitHub hosts"). The message says: "So this does NOT reproduce the three observed refusals, whose captured output was about 2.8 KB." Builder's mail says the body is "read back identical" to it; unverified by me. Body not read.

### TESTED
- bash 3.2.57 (`/bin/bash`), develop e9e32b76b048 vs merged tree m1708. `bash -n` rc 0 on all three, both trees. 0 occurrences of "Broken pipe" in all 6 runs.

| suite | develop | merged #1708 |
|---|---|---|
| check_shared_relink | 112 passed, 0 failed, 0 skipped | 112/0/0 |
| ks1355_slot_blind_launchers | 23 passed, 0 failed | 23/0 |
| preflight_deps | 61 passed, 0 failed | 61/0 |

- Red-proof (each edit one line in the merged worktree, run the one suite, restore with git checkout; sha256 before == after, `git status` 0 lines each time):
  - A `check_shared_relink.test.sh:115` expectation `"final stage has NO"` to `"...NOPE"`: 111 passed, 1 failed, only `FAIL: A: no re-link in the final stage fails (exit correct, WRONG rule fired ...)`. Grades line 49.
  - B1 `ks1355...:81` `'localhost:6982/'` to `'localhost:6982ZZ/'`: 22/1, only the slot-2 gateway cell (saw hit branch).
  - B2 `ks1355...:82` expected `"no"` to `"yes"`: 22/1, only the "no longer names slot 1's gateway" cell (saw miss branch).
  - C1 `preflight_deps.test.sh:516` `HOOKCTL-REFUSED/1` to `HOOKCTL-REFUSEDX/1`: 60/1, only "a hook with no derivable control REFUSES". Grades line 443.
  - C2 `:471` `SUITES-GREEN/0` to `SUITES-GREENX/0`: 60/1, only "leg 14: suites green -> preflight passes". Reaches through line 444.
  - Extra, corrupting the matcher itself: `:444` pattern + `ZZ`: 58/3 (three leg-14 cells red); `:443` string + `ZZ`: 59/2 (the two HOOKCTL cells). So both here-string lines are load-bearing.
  - Controls: in every run the other cells stayed green (the counts above are total minus the one expected). A plain mutation attempt with a wrong line number (A at 114) failed its own assert and the suite stayed 112/0/0, confirming the unmutated state prints green.
- Form level (my own re-measure, bash 3.2.57, `set -uo pipefail`, 100 loops each, match on first line, multi-line output): 200,008 bytes: old `printf|grep -q` mis-graded a match 100/100, here-string 0/100. 2.8 KB: old 0/100. Matches the builder's claim; the 2.8 KB tell does not reproduce.

### NOT TESTED
Other bash versions. The other ~146 sites. Preflight/pre-push legs. Suites under high load (my load1 was 2 to 5). Whether the three observed refusals are explained (the PR does not claim it).

---
## PR #1709 (KS-1554)

### FOUND
- **Note** Census confirmed: `git diff --stat 1f2ec373bdad pr1709` = 12 files, +67/-29 and 3 commits (6b06447e9, ea5bceb22, f1abd0859). Files: `CLAUDE.md`; `Blockchain/Dev/package.json`; `scripts/__tests__/ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh`; `.../ks1527_ratchet_leg_stub_cells_catch_a_mutated_leg.test.sh`; `.../preflight_test_types_ratchet_leg.test.sh`; `scripts/preflight/test-types-ratchet.sh`; `scripts/typecheck-tests/baseline-security.txt`; `.../baseline-m365-integration.txt`; `services/security/tsconfig.test.json`; `services/m365-integration/tsconfig.test.json`; `services/security/src/__tests__/ks952-rate-limit-scope-route.test.ts`; `.../ks952-rate-limit-scope.test.ts`.
- **Note** CLAUDE.md changes only at 398, 400, 403 (`git diff -U0`):
  - 398 old `...Leg 16 gates \`services/auth\`, \`services/api-gateway\` and \`services/vc-issuer\` (the script's default list; vc-issuer` new `...gates \`services/auth\`, \`services/api-gateway\`, \`services/vc-issuer\`, \`services/security\` and \`services/m365-integration\` (the script's default list; vc-issuer`
  - 400 old `\`npm run check:test-types\` runs the same three (KS-1090, KS-1351), each against...` new `...runs the same five (KS-1090, KS-1351, KS-1554), each against...`
  - 403 old `a PR that deletes an auth, api-gateway or vc-issuer test file` new `a PR that deletes an auth, api-gateway, vc-issuer, security or m365-integration test file`
- **Minor** `CLAUDE.md:399` (left as ruled, KS-1551) now reads `added by KS-1351 item 3 with an EMPTY baseline, so any type error in its tests is new), and`. It says vc-issuer is the empty-baseline service; security and m365 are now also empty. Stale after merge until KS-1551 lands. No other stale "three" phrasing found in tracked text (`git grep` for "all three checkers", "3 service(s)", "three services").
- **Note** The two product-adjacent edits are test-only and match the ticket's two fixes: `ks952-rate-limit-scope-route.test.ts:249` `expect(((await res.json()) as { error?: { code?: string } })?.error?.code).toBe('FORBIDDEN');`; `ks952-rate-limit-scope.test.ts` replaces `dirname(fileURLToPath(import.meta.url))` with `resolve(__dirname, '../../../../docs/openapi/secuura-api.yaml')`. Both files' tests run green (security vitest below).
- **Note** `package.json:44` `check:test-types` gains `&& ... services/security && ... services/m365-integration`; `test-types-ratchet.sh:47` default list gains both. The two tsconfig.test.json files are identical to each other (`extends ./tsconfig.json`, `noEmit`, `include src/**/*`, `exclude node_modules, dist`). Baselines contain only the comment header and `examined-test-files 40` / `26`; examined counts printed by the checker match (security: 52 files, 40 under `__tests__`; m365: 36, 26).
- **Note** Empty-baseline honesty (item 4): I could not reproduce 6. See HOW.

### TESTED
- Ratchet leg on merged tree m1709: last line `OK — 5 service(s) type-check against their baseline.` (develop control: `OK — 3 service(s)`). security `0 errors: 0 in the baseline`, m365 `0 errors ... 0 new`.
- Red-proof (merged tree, `const __v: number = 'x';` appended; restored with git checkout; sha256 equal; status 0 lines):
  - security, in `services/security/src/__tests__/ks952-rate-limit-scope.test.ts` (sha 72ff8d1de915...): unplanted control checker rc 0, leg rc 0. Planted: checker rc 1 naming `ks952-rate-limit-scope.test.ts(402,7): TS2322 ... / TS6133`, leg rc 1 `FAIL — services/security: ...`. After restore sha equal, leg `OK — 5 service(s)`.
  - m365, in `services/m365-integration/src/__tests__/db.retry.test.ts` (sha c690eff80288...): control rc 0/0. Planted: checker rc 1 naming `db.retry.test.ts(178,7): TS2322 / TS6133`, leg rc 1 `FAIL — services/m365-integration`. Restored equal, leg OK.
- Leg suite `preflight_test_types_ratchet_leg`: develop 39 passed 0 failed; merged 43 passed 0 failed (builder's 39 to 43 confirmed). ks1513 suite 5/0 and ks1527 suite 4/0 on both trees; the two edited meta-suites pass at the head (the builder's refusal reason is resolved).
- services/security vitest, unit only (`vitest run --exclude '**/*.integration.test.ts'`): develop 33 files / 361 tests passed, merged 33 / 361 passed. 7 `*.integration.test.ts` files exist in `src/__tests__` (control for the exclusion) and were NOT RUN (need a DB).
- merge-tree: see top.

### HOW (and one disclosed harness fault)
- Install: the cache clone keeps no private install, so I linked `node_modules` from the main Secuura checkout. My first ratchet runs failed (leg 36/3 on develop, 39/4 on merged) with `TS2305 ... has no exported member 'isProvisioningCapable'/'isScopedAdminRole'`: the borrowed `@secuura/shared` symlink resolved into the main checkout's stale `packages/shared/dist`. That was my harness, not either PR. Fix: private `node_modules` dir with symlinks plus a copy of `@secuura/` (relative links resolve in the worktree), and `tsc` build of `packages/shared` in each worktree. All numbers above come after that fix. Both fresh-clone results (ks1513 "no install" cells) are consistent with the builder's first-push note.
- Wednesday's mail on shared `$TMPDIR` `ks1487-leg.*` deletions (Seat V, ~08:49 to 08:53Z = 19:49 to 19:53 AEDT): my first leg-suite and meta-suite runs ran inside that window, and all three passed (43/0, 5/0, 4/0) with no missing-path message. I re-ran all three with a private `TMPDIR` (`.../tmp.GTXm` in my workspace) as a precaution: 43/0, 5/0, 4/0 again. No result changed.
- A red-proof slip of mine, corrected: my first red-proof script used a git path relative to the wrong directory, so the restore did not apply. I restored both files with the correct paths, confirmed sha256 equal to the pre-plant values (72ff8d1de915..., c690eff80288...) and 0 status lines, then re-ran the whole red-proof cleanly (results above).
- Item 4 (the 6 errors): ticket comment of 2026-10-13 lists 2 ks952 errors plus 4 TS2741 `keepAliveTimeoutBuffer` at `ks698r1-route-heals-poisoned-key.test.ts:86`, `ks952-rate-limit-scope-route.test.ts:77`, `ks976a-...:61`, `ks976b-...:52`, attributed to `@types/node` 26.1.0 (root) vs 20.19.43 (service). On develop e9e32b76b048 with the install at exactly those versions (verified in `package.json`: root 26.1.0, security 20.19.43, packages/shared 20.19.43), `tsc` over four shapes read: (1) scratch config in the service dir, `exclude: []`, `types: ["node"]`: 2 errors (TS2339 :249, TS1343 :313); (2) same without `types`: 2; (3) same with `typeRoots` at `../../node_modules/@types`: 2; (4) positive control, planted `zz_gate_plant.test.ts`: reported 1 time. TS2741 count: 0 in all. Also 0 on the enrolled config of the merged tree. Cannot say why the 2026-10-13 run saw 6 (possibly an install that had two `@types/node` copies in one program). The ratchet would therefore not red-light on those four today; but if the double-`@types/node` condition returns, security's baseline of 0 will turn red on all four sites.

### NOT TESTED
The 7 security `*.integration.test.ts` (DB needed); m365-integration's own vitest suite; image builds; Node 24 (only v26.8.1 here); the full shell-suite runner and pre-push hook; CI; the PR body of #1709 (no `gh` login; I read the diff and the Linear ticket comments, KS-1554, read-only).

## Decisions for Wednesday
1. Whether to follow up #1708 with the three untouched sites (preflight_deps.test.sh:441, 442, 453) or leave them (builder and ticket scope says leave).
2. CLAUDE.md:399 stays stale until KS-1551 lands; confirm that is acceptable between merges.
3. PR bodies were not read via GitHub (no `gh` auth); the #1708 honesty clause was checked on the commit message only.

## Addendum: re-run after the upgraded TMPDIR disclosure (Seat V mail 09:00Z)
Seat V likely deleted up to two of my live temp dirs (ks1487-leg.lJGLbY, ks1487-leg.QOlgYW) around 08:50 to 08:53Z (19:50 to 19:53 AEDT). My first ratchet-leg, leg-suite, meta-suite and red-proof runs (19:50 to 19:57 AEDT) overlapped or sat close to that window, so they are **superseded**. The results quoted in the #1709 section are from these re-runs, each under a private `TMPDIR` inside my workspace (`tmp.GTXm` at 19:58, `tmp.n5uK` at 20:00:48), all after 08:54Z:
- ratchet leg direct run: `OK — 5 service(s) type-check against their baseline.`
- `preflight_test_types_ratchet_leg` 43 passed 0 failed; `ks1513_...` 5/0; `ks1527_...` 4/0 (the ks1487 and ks1520 cells live in the leg suite).
- red-proof security and m365: control rc 0/0; planted checker rc 1 and leg rc 1 naming the file; restored, sha256 equal (72ff8d1de915..., c690eff80288...), 0 status lines; leg OK after.
Every re-run matched the earlier run, so no verdict changed. The #1708 suites and services/security vitest do not touch `ks1487-leg.*` and ran outside the window or are unaffected (vitest was run at 19:58, after it).
