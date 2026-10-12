# Gate verdict: Secuura Platform K PR #1523 (KS-1351 item 3, vc-issuer under the test-file type-check ratchet)

**VERDICT: GO WITH NOTE.** There are 0 Majors and 2 Minors. Neither Minor blocks the merge. Both are filed below with a fix-shape.

- **Head tested:** `ff293fa0ac7e02bf4fcfeec86b65e0b73ffb5054`. I fetched it read-only from GitHub `refs/pull/1523/head` into my own `git clone --shared` in my scratchpad, using the project's `core.sshCommand`, and asserted it with `rev-parse`. It also equals the bundle's `list-heads` (bundle sha256/16 `a44a650a7d6c29d8`, re-measured). The bundle could not be fetched directly: its prerequisites 425ad3e0 and 551dc98 are missing from the local project object store.
- **develop:** `b08ee6299e864bea2aff18f31bdd22281161c1db` (asserted). merge-base = `425ad3e0`. Since base, develop changed only 2 files, both in api-gateway (`routes/platform.ts` and the ks1512 test), so there is no overlap with the PR. `git merge-tree --write-tree` gave rc 0, tree `cf8d654e2eef`. I made a synthetic merge commit `abb762e297e3` in a worktree to measure "after merge".
- **PR diff:** 6 files, +41/-20 (`git diff --stat 425ad3e0 ff293fa0`), which matches the author's list. `check.cjs`, `preflight.sh`, the auth and api-gateway baselines and both services are untouched (empty `git diff --stat` on those paths).
- **Installs:** `npm ci --ignore-scripts` (rc 0) plus `npm run build --workspace=packages/shared` (rc 0), done separately in each of 4 linked worktrees: head, develop, merged, and a path with spaces. node_modules are not symlinked or shared.
- **Leg-16 instrument:** `harness/leg16.sh` (copied in `evidence/`). It cds to `Blockchain/Dev` and runs the verbatim preflight line `if ! run_delegated bash scripts/preflight/test-types-ratchet.sh; then fail=1; fi`. `run_delegated` and `_note_skip` are extracted from that tree's own `preflight.sh`, and the harness refuses (exit 98/99) if the call line or the helpers are not found verbatim. This is the exact call the pre-push hook reaches through `preflight.sh`. I did **not** run the other 15 legs (see NOT tested).
- **Mutation discipline:** every mutation was asserted present before the run (grep or `-e` check). Every run was restored via `git checkout` and asserted `status --porcelain` = 0.

---

## Results by brief item

### 1. Red-proof through the real leg-16 entry point: CONFIRMED
FAIL condition stated beforehand: a planted TS2322 in a vc-issuer test passes this head's leg, or reds develop's.

| Tree | Plant | leg-16 rc | Output | Evidence |
|---|---|---|---|---|
| head ff293fa0 | none | **0** | `OK — 3 service(s)`; vc-issuer `tsc examined 30 files, 17 of them under __tests__; 0 errors` | T1 |
| head ff293fa0 | `export const __gatePlant: number = "x";` in `src/__tests__/smoke.test.ts` | **1** | `src/__tests__/smoke.test.ts(16,14): TS2322 …` and `FAIL — services/vc-issuer` | T2 |
| develop b08ee629 (control) | same plant | **0** | `OK — 2 service(s)`; vc-issuer never checked | T3-wt-dev-plant |
| merged abb762e2 | none / plant | **0 / 1** | 3 services, then `FAIL — services/vc-issuer` | T3-wt-merged-* |

The develop control matters because it shows the plant really is invisible without this PR. That makes the head red a detection, not something the plant would have caused on any tree.

### 2. tsconfig.test.json scope: COMPLETE for tests; it also covers product files (intended)
- I listed tsc's `--listFiles` under `services/vc-issuer` (node_modules excluded) and diffed it against `git ls-files services/vc-issuer/src/*.ts`. Both have **30 files and are IDENTICAL** (`diff` rc 0). Of those, **17 are under `__tests__`**, which equals the 17 git-tracked test files (evidence T4-tsc-examined / T4-git-ts).
- No test file exists outside `src/__tests__`. The only `.ts` outside `src` is `vitest.config.ts`, which is not checked; auth and api-gateway handle it the same way.
- The file is byte-for-byte the same shape as auth's and api-gateway's `tsconfig.test.json` (extends `./tsconfig.json`, `include src/**/*`, removes the `src/__tests__` exclude). It inherits vc-issuer's `paths` mapping for `@secuura/shared`, which resolves correctly through the hoisted workspace link. This is proven by 0 errors after the shared build.
- **Source-file errors red too.** I planted the same TS2322 in `src/routes/status.ts` (a product file that 6 tests import), and leg-16 returned rc 1 naming `src/routes/status.ts(417,14)` (T4-head-srcplant). Because `include` is `src/**/*`, this applies to *every* vc-issuer source file, not only those reached through a test. That is intended: the leg's closing advice says "that can be a product file", and the api-gateway and auth configs are identical. See Note N1 for the doc wording.

### 3. EMPTY baseline / "floor 17": measured 0 errors at head and after merge; one hole (Minor M1)
- **What the floor means:** `examined-test-files 17` is the minimum count of examined files under `__tests__` (`check.cjs:245,257`). Fewer fails the check (T5e: one test file moved away gives `16 examined, examined-test-files 17` and rc 1). The floor does **not** rise when tests are added (T5f: 18 test files, rc 0). That limitation is documented.
- **The committed baseline is byte-identical to a fresh `check.cjs services/vc-issuer --init`** (`cmp` rc 0; `0 errors in 0 entries; examined-test-files 17`). It is therefore the tool's own output, not a hand-written file.
- **Zero existing errors means no seat is refused on arrival.** vc-issuer had 0 errors at head (T1) and 0 after merge with develop b08ee629 (T3-wt-merged-clean). The control that could have failed is the unbuilt-shared run (N2), which showed the same instrument reporting 17 vc-issuer errors when they exist.
- **Can a later push add baseline entries silently?** Yes, by a hand edit (T5i). Planting a TS2322 and appending `src/__tests__/smoke.test.ts TS2322 0a58e37d 1` to the baseline in the same change gives leg-16 rc 0. This is **pre-existing and documented-by-convention** ("Never edit a count up"); `--update` itself refuses. Hand-lowering the floor to 16 and deleting a test file also passes (T5j, pre-existing, documented). Neither is introduced by this PR. Both are visible in a PR diff.
- **Minor M1 (new exposure from the EMPTY baseline):** see Findings.

### 4. Failure modes that could wrongly block every push: none found that this PR introduces
| Shape | Result | Correct? |
|---|---|---|
| Fresh linked worktree, **no install** (T6a) | rc 0, `SKIP (advisory)`; `run_delegated` counted leg 16 as SKIPPED (`skipped_advisory=' 16'`) | Yes, as designed. Leg 1 refuses the push. |
| Install present, **`typescript` removed**, deps-present still rc 0 (T6b) | rc 1; for each of 3 services: `cannot resolve typescript/bin/tsc … run npm ci first` and `exited 2: the check could not run` | Yes. A loud "could not run", never a pass. |
| Install present, **packages/shared not built** (T6c) | rc 1, reported as **NEW type errors**: auth 39, api-gateway 20, vc-issuer 17 (all TS2307 `Cannot find module '@secuura/shared'` and cascades) | Pre-existing mislabel class. vc-issuer joins it. See N2. |
| **Path with spaces** (`…/gate dir with spaces/wt head`, own install) (T6e) | clean rc 0 (3 services); plant rc 1, naming `smoke.test.ts(16,14)` | Yes |
| **Linked worktree** | every run above was in a `git worktree add` tree | Yes |
| **Symlinked spelling** `/tmp/…` → `/private/tmp/…` (T6d) | rc 0, same counts | Yes |

### 5. Mutants
- **Drop vc-issuer from the default list** (asserted: line 47 reads `set -- services/auth services/api-gateway`). The leg suite went to **30 passed, 8 failed** (T5a), which matches the author's "8 of 38". 4 of the 8 are real-checker cells that run only with an install. Without one, the suite prints its note and the remaining 4 stub cells still red. So the mutant is caught either way.
- **Move `tsconfig.test.json` away** (T5b) gives rc 1, `no tsconfig.test.json in …/vc-issuer` and `FAIL — services/vc-issuer … exited 2: the check could not run`. Correct, and loud.
- **Move `baseline-vc-issuer.txt` away** (T5c1/T5c2) gives rc 0 in both cases. This is **Minor M1**.

### 6. Other two ratchets unchanged: CONFIRMED
At head, the leg-16 and `npm run check:test-types` runs (rc 0, T8) both give auth `42 errors: 42 in the baseline, 0 new; 0 stale` (93 tests, floor 93) and api-gateway `35 … 35 in the baseline, 0 new` (117 tests at head / 118 merged, floor 113). Both baseline files and `check.cjs` have an empty diff against base. The auth `ks1000` suite (which reads CLAUDE.md, now edited) passed 35/35, and the api-gateway `ks1090` suite passed 1/1.

### 7. CLAUDE.md and comments versus code
- CLAUDE.md:389-395 is accurate on the default list, `check:test-types` running three services, the per-service baselines, and the obligation to run `--update` on deleting a test file. T5e proves the floor refusal.
- The `package.json` `check:test-types` chain has 3 services, matching the leg's default list.
- Comment drift is filed as Minor M2, and the wording point as N1.

### Author's claims re-measured
| Claim | My measurement | Instrument |
|---|---|---|
| plant reds PR leg (rc 1, names file), passes develop (rc 0) | **confirmed** | leg16 harness, T2 / T3 |
| clean rc 0, "3 service(s)" | **confirmed** | T1 |
| dropping vc-issuer reds 8/38 | **confirmed** 30/8 | leg suite, T5a |
| leg-16 suite 38/38 | **confirmed** at head and at merged | T7 |
| check:test-types rc 0, vc-issuer 30 files / 17 tests, 0 errors | **confirmed** | `npm run check:test-types`, T8 |
| vc-issuer suite 160/160 | **confirmed**: `Tests 160 passed (160)`, 17 files | `npx vitest run` in services/vc-issuer |

Cost per push: vc-issuer adds about **1.6 s** (`/usr/bin/time -p`: real 1.59). auth took 2.77 s and api-gateway 2.87 s on the same machine, in one run each, so treat these as indicative.

---

## Findings

### Minor M1: a missing `baseline-vc-issuer.txt` is read as "empty, no floor", so deleting it is silent for vc-issuer and drops its only test-deletion guard
- **Where:** `Blockchain/Dev/scripts/typecheck-tests/check.cjs:138` (`if (!fs.existsSync(baselinePath)) return out;`, which yields floor `null`), together with `:221` (the no-floor refusal only fires when `base.exists`) and `:245` (`floorFell` is false when the floor is null). The code is pre-existing. **The exposure is new with this PR** because the vc-issuer baseline is empty.
- **Repro** (known state: head ff293fa0, install and shared built, clean tree):
  1. `mv Blockchain/Dev/scripts/typecheck-tests/baseline-vc-issuer.txt <elsewhere>`
  2. `mv Blockchain/Dev/services/vc-issuer/src/__tests__/smoke.test.ts <elsewhere>`
  3. Run leg 16. Result: **rc 0**, `tsc examined 29 files, 16 of them under __tests__; 0 errors: 0 in the baseline …` and `OK — 3 service(s)` (evidence T5-all, T5c2).
- **Expected** (oracle: Product consistency, and Purpose, since the floor exists so that "a deleted test file" fails): a vanished baseline should refuse, the same way a vanished `tsconfig.test.json` does (exit 2).
- **Control that proves this is vc-issuer-specific:** moving `baseline-auth.txt` away **is** loud (rc 1, `42 errors: 0 in the baseline, 42 new`, T5c-control-auth). auth's non-empty baseline catches the deletion by accident. vc-issuer's empty one cannot, so for vc-issuer the floor is the only guard and the deletion removes it without a word.
- **Severity: Minor.** It needs a deliberate deletion of a tracked ratchet file, which shows in any PR diff. It cannot happen by accident, and it cannot admit a type error (any error is still "new" against no baseline). Priority is for the humans to set.
- **Fix-shape:** in normal check mode (not `--init`), `check.cjs` exits 2 when the baseline is absent, for example with `no baseline at <path>: create it with --init`. Care is needed: the leg suite's stub cells and the auth ks1000 fixtures may rely on "no baseline file reads green" (the leg suite says so at its stub section: "the fixture holds no baseline file"), so those fixtures would need a floor-only baseline. An alternative is a per-service existence assertion in `test-types-ratchet.sh`.
- **Regression test the owner should add:** a leg-suite cell with a fixture service that has a `tsconfig.test.json`, a test file and **no** baseline, run with the real checker. The leg must exit 1 naming the service with an exit-2 cause. Its control cell is the same fixture with a floor-only baseline, which passes.

### Minor M2: the leg's own header still describes a two-service default
- **Where:** `Blockchain/Dev/scripts/preflight/test-types-ratchet.sh:19-20`: "(default services/auth and services/api-gateway, about 2.6 to 3.2 s each, measured)". The PR updated the Usage line at `:38` and the code at `:47`, but not this paragraph. Lines 7-8 likewise still say "services/auth's does, and so does services/api-gateway's".
- **Oracle:** Product (internal consistency between comment and code).
- **Severity: Minor** (documentation only, no behavioural effect). Fix-shape: name all three services and the measured vc-issuer cost (~1.6 s).

### Note N1: CLAUDE.md:390 says "any type error in its **tests** is new"
In fact any type error in **any vc-issuer `src` file** (product code included) reds leg 16, as T4 shows with `src/routes/status.ts`. The behaviour is intended and matches the other two services. The wording undersells it. Suggested wording: "any type error in its tests, or in source they type-check, is new".

### Note N2: pre-existing, and vc-issuer joins it: an unbuilt `packages/shared` is reported as 76 "NEW type errors"
`deps-present.sh` checks only `tsx` and shared's nested `@types/node`. It does not check `packages/shared/dist`. With dist absent, leg 16 reports auth 39 / api-gateway 20 / vc-issuer 17 **NEW** errors (TS2307), which is a false "you added type errors" (T6c). In a full preflight this is mostly unreachable, because leg 1 (`generate-openapi`) builds shared first; it only surfaces when that build fails. This PR did not introduce it. I am recording it so the class is not lost.

---

## NOT tested (Rule 2)
- **The full pre-push hook and the other 15 preflight legs.** I ran leg 16 through its verbatim `run_delegated` call with the tree's own helpers, not via `.githooks/pre-push`, `step()` or `_leg_concluded()`. The leg suite's WIRING cells (38/38) do execute the real step-16 block under the real helpers, so that wiring is covered by the suite, not by me.
- **`npm ci` with scripts** (the real postinstall). I used `--ignore-scripts` plus an explicit shared build, as earlier gates did.
- **Linux/Ubuntu VM and bash other than macOS's.** Every run was on darwin. I did not check the bash 3.2-specific path separately.
- **Other open branches that touch vc-issuer** and might carry test-file type errors that would now be refused once this merges. I measured only head, develop b08ee629 and their merge.
- **A CRLF checkout, Windows, or a non-`/private/tmp` volume** such as `/Volumes/DevMASTER` (the symlink spelling was tested only for `/tmp`).
- **Concurrency**: two pushes running leg 16 at once.
- **`--update` / `--rekey` on vc-issuer.** Unchanged code, not exercised for this service.
- **CI workflows.** I did not check whether any GitHub workflow runs `check:test-types`; no `.github` reference was found by grep, and nothing was executed in CI.

## Housekeeping
- Project checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` was only read (as the `--shared` clone source). No pushes: the push URL was set to `DISABLED`. No GitHub or Linear writes. The only network contact was a read-only `git fetch` of PR 1523 and develop from GitHub, as the brief sanctions, plus the npm registry for `npm ci`.
- Evidence logs (scratch paths redacted to `<scratch>`) and the three harness scripts are in `evidence/` beside this file.
- Time split, approximate: setup (clone, fetch, 4 installs) 35%, test design and execution 50%, investigation and writing 15%.
