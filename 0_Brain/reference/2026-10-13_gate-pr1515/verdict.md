# Gate verdict: Secuura Platform K PR #1515 (KS-1517), tier 2 (tooling / ratchet checker behind leg 16)

- Head under test: `eff6d0211ebc1e0ddb2a0a35211d4e3ace7e2e1d` (fetched refs/pull/1515/head, equals the stated head exactly)
- develop: `551dc9808aee1c89d217cd662628c17ef8ad3a0e` (read via `git ls-remote origin refs/heads/develop` at gate time; did not move)
- Tree: scratch clone `git clone --shared` of the Blockchain 2_Project_Files (read-only source), fetched PR head + develop with the project's core.sshCommand, `git archive` of base and head into the scratchpad, node_modules shell of symlinks to the main checkout's installed deps with the `@secuura/*` workspace links relative (so they resolve inside MY tree), `packages/shared` BUILT in each tree with tsc (rc 0, 29 dist entries). Nothing written inside !CODING.
- Author bundle cross-check: sha256/16 `c6da94d7c80f647e` matches the stated value. Head check.cjs sha256/16 `597c81dacdaf752b` matches the stated value.

## VERDICT: GO WITH NOTE

Majors: 0 against the shipped repo (one latent false-exit-2 class, L1 below, rated Minor-latent; by the literal "any reproducible false exit 2 on a healthy complete build" rule it WOULD be Major, so that is your call, see the Opus recommendation at the end).

## Findings

### Major
None against the real services or the real `@secuura/shared` package.

### Minor
- **L1 (latent false exit 2, reproduced on a COMPLETE build of a constructed package).** `check.cjs:148-155` (`mapLookup`) and `:174-175` (`fs.existsSync(path.join(pkgRoot, rel))`) treat the typesVersions target as a literal file. Three legitimate typesVersions shapes that tsc resolves cleanly (tsc rc 0, old checker rc 0) make the NEW checker exit 2 "build is stale or incomplete":
  1. trailing-`*` pattern with an extensionless target (the canonical TypeScript-docs form): `"sub/*": ["dist/sub/*"]`, build complete with `dist/sub/a.d.ts` -> "missing declaration target: dist/sub/a".
  2. same via a bare `"*": ["dist/*"]` key.
  3. a literal extensionless target `"e": ["dist/e"]` with `dist/e.d.ts` present.
  4. an array fallback where the FIRST entry is absent and the second exists: `"f": ["src/f.d.ts","dist/f.d.ts"]` (`firstString` at `:137` only ever takes the first element) -> "missing declaration target: src/f.d.ts".
  Not reachable today: `@secuura/shared` is the ONLY package in the repo with `typesVersions` and every entry is a literal key with an explicit `.d.ts` target (all 23 verified). But the first person who adds a wildcard or extensionless entry to shared's typesVersions blocks every seat's leg 16 with a message telling them the build is stale (it is not, `npm run build` will not fix it). Loud, not silent; recommended fix before that happens: try `target`, `target + '.d.ts'`, `target + '/index.d.ts'`, and accept ANY array entry that exists. The CLAUDE.md/header text says "matched literally and by a single trailing `*`", which is true of the KEY but not of the substituted TARGET.
- **L2 (imprecise 0 -> 2 flips when the build really is incomplete).** The scan is a plain regex over every .ts/.tsx/.mts/.cts under `src/` (`:104`, `:123`): a specifier inside a comment, or in a file excluded by tsconfig (`exclude: ["src/excl"]`), whose mapped declaration target is missing exits 2 although tsc passes and the old checker exited 0 (cases `scomment`, `excl` below). Requires a genuinely unbuilt declared target, so it is a "right answer for a slightly wrong reason", not a healthy-build false positive. Documented limitation in the header covers only variable-built specifiers, not comments/exclusions.
- **L3 (test gap, false-positive side).** All five of my false-positive-side mutants SURVIVE the 7 new cells (below). The suite proves the fail side (8/8 author mutants killed) and one positive control, but nothing pins: skipped-key-not-missing, no scanning of node_modules/dist, wildcard off-by-one, unresolved package skipped. Cheap to add (a `no typesVersions` cell and a wildcard cell would have caught L1 and F1/F3/F4).
- **L4 (doc overclaim, CLAUDE.md line "Leg 16's decision is unchanged either way").** True for every real-service arm measured (below), false in general: L1 and L2 shapes move leg 16 from pass (0) to fail (1). Also "tsc resolves these subpaths under Node10 through typesVersions" is true for these services only because neither tsconfig sets `moduleResolution` (commonjs default = node10); a service moved to node16/bundler would resolve via `exports` and the type target here would be the wrong map. Worth one clause.

## What I ran (all rc/values measured here)

1. **Topology.** `git diff --numstat 551dc9808aee pr1515` = `Blockchain/Dev/scripts/typecheck-tests/check.cjs 112/0`, `Blockchain/Dev/services/auth/src/__tests__/ks1000-...test.ts 109/0`, `CLAUDE.md 10/0` = exactly 3 files +231 -0. `merge-base dev pr1515` = 551dc9808aee (develop is the base; never rebased). `git merge-tree --write-tree dev pr1515` rc 0, tree f538a5d6..., clean.
2. **Real-service false-positive hunt, complete build (shared built in each tree).** base checker vs head checker, services/auth and services/api-gateway: all four rc 0; stdout identical (after path normalisation) for both services; ZERO NOTE lines printed anywhere. auth: 144 files / 93 under __tests__ / 42 errors, 42 baselined, 0 new, 0 stale. api-gateway: 150 / 115 / 35 / 35 / 0 / 0. Matches the author's figures. Every `@secuura` subpath actually imported by auth+api-gateway src: `shared` (root), `shared/crypto/jwks`, `shared/crypto/registry`, `shared/documents/default-type`, `shared/security/scopes`, `shared/vault/key-vault`, plus one fixture-string `shared/thing` in the ks1000 test (unmapped, skipped). Only `@secuura/shared` is imported anywhere in services/ and packages/ src (257 import sites), and it is the only package with typesVersions.
3. **Stale-build arms on services/api-gateway (copy of head tree, files moved aside and restored, then C re-run):**

| Arm | Hidden | New checker | Base checker |
|---|---|---|---|
| C | nothing | rc 0 | rc 0 |
| B | `dist/documents/defaultDocumentType.d.ts` | rc 2: "the @secuura/shared build is stale or incomplete, so this check CANNOT RUN", `missing declaration target: dist/documents/defaultDocumentType.d.ts (imported as '@secuura/shared/documents/default-type')`, `rebuild it:  npm run build -w @secuura/shared` | rc 1, 2 x TS7016 reported as NEW |
| D | whole `dist/documents/` | rc 2, same target + "also missing (runtime only...)" line + build command | rc 1, 2 x TS2307 as NEW |
| A | `dist/documents/defaultDocumentType.js` only | rc 0, one `note: @secuura/shared declares dist/documents/defaultDocumentType.js for '@secuura/shared/documents/default-type' and it is not built. The type check is unaffected ...` on stdout | rc 0 silent |
| C2 | restored | rc 0 | rc 0 |

4. **Tier claim, leg 16 (`scripts/preflight/test-types-ratchet.sh`; byte-identical in base and head, `cmp` clean), run three ways in the stale copy:** new checker + arm B hidden -> leg exit 1, "FAIL - services/api-gateway: the test-file type-check ratchet exited 2: the check could not run ..." with the stale-build message above it; base checker + same hidden file -> leg exit 1, "exited 1: a NEW test-file type error ...", with 2 x TS7016; new checker + complete build -> exit 0 "OK - 2 service(s)". Exit codes 1, 1, 0 as claimed; same decision, different stated cause. (check.cjs swapped base/head inside my scratch tree and restored, sha256/16 597c81dacdaf752b confirmed after.) Note the leg's exit-2 `why` text ("could not run, examined no test file, or the baseline cannot be trusted") does not mention a stale build; the lines above it do.
5. **ks1000 suite at head (vitest, services/auth):** 36 passed / 36. **Red-first:** head test file against the base checker: 4 failed | 32 passed (36); the 4 are the two RED cells, the exports-only cell, and the stale-before-baseline cell; the CONTROL, the no-@secuura cell and the unused-subpath cell pass (7 new = 4 red / 3 pass). Matches the claim.
6. **Mutants (restored byte-identical each time; final sha256/16 597c81dacdaf752b), new KS-1517 cells (7) failing per mutant:**

| Mutant | Failed of 7 |
|---|---|
| M1 never die (`if (false)`) | 3 |
| M2 declaration treated as a note | 3 |
| M3 runtime target treated as fatal | 1 |
| M4 die(1,...) instead of die(2,...) | 3 |
| M5 build command line removed | 3 |
| M6 type target read from `exports` instead of typesVersions | 4 |
| M7 judge every typesVersions key, not only imported ones | 1 |
| M8 target-naming line removed | 2 |
| **F1** unresolved/skipped key treated as missing | **0 (survives)** |
| **F2** scan node_modules/dist (skip removed) | **0 (survives)** |
| **F3** off-by-one in the `*` head slice (`slice(0,-2)`) | **0 (survives)** |
| **F4** off-by-one in the `*` match (`length > head.length`) | **0 (survives)** |
| **F5** uninstalled package treated as fatal | **0 (survives)** |

   All 8 author-side mutants killed (counts 3,1,1,3,3,4,1,2 here vs the author's different ordering; each killed). All 5 false-positive-side mutants survive: see L3.
7. **`npm run check:test-types` equivalent** (check.cjs services/auth, then services/api-gateway, from Dev): both rc 0 with the figures above. **eslint** on check.cjs: rc 0; positive control (a file `var x = ;` in the same directory) -> rc 1, so the .cjs is genuinely linted.
8. **CLAUDE.md ten lines read against measurements:** accurate on: exit 2 + message + build command; typesVersions as the type map (measured by arm B/D vs A); exports gap deliberately a note (arm A); `--update` cannot admit; `.npmrc` has `ignore-scripts=true` (line 15, verified). Overclaims: L4.

## Edge-case table (specifier / package shapes, head checker on a COMPLETE build unless noted; tsc rc and old-checker rc alongside)

| Case | New checker | tsc / old | Judgement |
|---|---|---|---|
| specifier inside `//` and `/* */` comment, mapped target exists | rc 0 | - | ok |
| specifier inside a string literal, unmapped | rc 0 | - | ok |
| `import type` / `typeof import()` (mapped subpath exists) | not rc 2 (rc 1 was my fixture's own wrong member name) | tsc error mine | ok, scanned, no false 2 |
| `export * from '@secuura/shared/security/scopes'` | rc 0 | - | ok |
| dynamic `import('@secuura/shared/crypto/jwks')` | rc 0 | - | ok |
| require inside a template literal (backticks) | rc 0 | - | ok, invisible (documented class) |
| subpath with extension `crypto/jwks.js` | rc 0 | - | skipped (no literal key) |
| deep import not in typesVersions | rc 0 | - | left to tsc, per claim |
| `'*'` in a MIDDLE position (`a/*/b`) | rc 0 | tsc rc 0 | skipped, per claim |
| package with no typesVersions, root and a subpath import | rc 0 / rc 0 | - | ok |
| `@secuura/<other>` package (not shared), healthy | rc 0 | - | ok (generic over @secuura/*) |
| trailing-`*` pattern, extensionless target, COMPLETE build | **rc 2** | tsc 0 / old 0 | **FALSE exit 2 (L1)** |
| bare `"*": ["dist/*"]`, COMPLETE build | **rc 2** | tsc 0 / old 0 | **FALSE exit 2 (L1)** |
| literal extensionless target `dist/e` (+ `e.d.ts`), COMPLETE | **rc 2** | tsc 0 / old 0 | **FALSE exit 2 (L1)** |
| literal directory target `dist/d` (+ `index.d.ts`) | rc 0 | tsc 0 | ok |
| array fallback, first entry absent, second present, COMPLETE | **rc 2** | tsc 0 / old 0 | **FALSE exit 2 (L1)** |
| comment mentioning a mapped subpath whose target is genuinely unbuilt | rc 2 | tsc 0 / old 0 | L2 (build really incomplete) |
| file excluded by tsconfig importing a mapped subpath, target genuinely unbuilt | rc 2 | tsc 0 / old 0 | L2 |

## Honest residual false-positive risk
- Shipped repo, auth + api-gateway + shared as they are today: none found; both services rc 0 identical to base with zero notes on a fresh complete build.
- The first non-literal typesVersions entry added to any `@secuura/*` package (L1) is a guaranteed fleet-wide false exit 2 until check.cjs is fixed. It is loud and attributable, and it is exactly the sort of change someone makes while adding a subpath, so I recommend fixing it in this PR or the next, not blocking the merge.
- The `main`/`types`-less or exports-absent root-import path was exercised only through fixtures, not a real package.

## Does this change a leg-16 decision?
- For every real-service state I measured: no (1,1,0 as claimed).
- For L1 and L2 shapes it DOES: pass becomes fail. The CLAUDE.md "decision is unchanged either way" is therefore too strong (L4). Recommendation: Opus re-gate the L1 mapLookup/target-resolution question (or the author's fix to it); I do not recommend holding PR #1515 for it given the shipped package cannot trigger it.

## NOT TESTED / NOT RUN
- Full services/auth vitest suite (93 files / 1025 tests twice) and the other 26 services' suites; platform suites; legs 3, 4, 8 of preflight; `--update`/`--init`/`--rekey` paths (unchanged code, not in the diff).
- The remaining 24+ services were not run through check.cjs (leg 16 gates only auth and api-gateway).
- Windows path separators; a CRLF checkout of check.cjs; moduleResolution node16/bundler services (no such service gated).
- Real `npm ci`-produced tree (offline; used symlinked deps + a tsc-built shared).
- A real git-worktree / CI container build of shared (only my scratch tsc build).
- No GitHub or Linear writes were made; the PR was not posted to.
