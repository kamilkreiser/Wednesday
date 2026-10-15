VERDICT: PASS (round 1 of 2) for PR #1556 head 67b763305a0b3c70f652868c350e294883995543 - no blocker, no major; 0 HIGH / 0 MEDIUM / 1 LOW / 3 INFO. Merge only on Wednesday's head-bound GO; nothing deploys.
sha256/16 (this file minus line 2): 505522a0a9c5dccd

# Gate B - PR #1556 (KS-1543 part 1 of 2), tier 2 through-code

Gate seat: Opus QA gate, 2026-10-15. Clone: /private/tmp/claude-501/gateB1556-r1/clone (`git clone --shared` of the checkout, fetched from origin with the checkout's own deploy-key sshCommand). Scripts: /private/tmp/claude-501/gateB1556-r1/scripts/. Raw logs and vitest JSON: `evidence/` beside this file.

## Refs (re-read by me)
- `ls-remote`: refs/pull/1556/head = 67b763305a0b3c70f652868c350e294883995543, develop = 0bb4f17ca5010baa3ad9d91b790522e87b8c9dc1 (read at start and again before the merge prediction; it had not moved).
- develop 0bb4f17ca IS an ancestor of the head (`merge-base --is-ancestor`, rc 0); merge-base(develop, head) = 0bb4f17ca.
- develop..head = 7b7d40329 (the patch, parent 53b429ed6) + 67b763305 (merge of develop 0bb4f17ca). The patch 7b7d40329 and develop..head are the same text apart from hunk offsets (+9 lines from the merge): the merge brought in no extra change.

## FOUND / TESTED / HOW

### 1. Diff by hunk - PASS
`git diff develop head`: 2 files, +49/-2.
- verification.ts:661 `} catch (_err) {` -> `} catch {`; verification.ts:1503 `} catch (err: any) {` -> `} catch {`. Nothing else in the product changed. The comment bodies (661-664 "Network/timeout - fall through...", 1504 "Ignore DB errors...") are unchanged context lines.
- Behaviour: the same. An optional catch binding (ES2019) catches exactly what the named binding caught. Neither body read the binding (ESLint said "defined but never used" on both before the change). tsconfig target ES2022 emits it natively; `tsc -p tsconfig.json --noEmit` at head rc 0, 0 errors.
- The second file is the new test, +47/-0. No other file is touched.

### 2. Red first, then green, plus ESLint before and after - PASS, the author's numbers confirmed
- RED (develop's verification.ts in the head tree, run via `npm --prefix <clone>/services/api-gateway run test -- run <file>`): 4 tests, 2 failed / 2 passed. C1 failed with `expected '} catch (_err) {' to be '} catch {'`, C2 with `expected '} catch (err: any) {' ...`. Both controls passed.
- GREEN (head): 4/4 passed.
- ESLint, ESLint Node API, the repo's flat config. The resolved config's rule is `no-unused-vars [warn, {argsIgnorePattern ^_, varsIgnorePattern ^_, ignoreRestSiblings}]`, with no caughtErrorsIgnorePattern, as the brief says.
  - before (develop file): 0 errors, 5 warnings. `@typescript-eslint/no-unused-vars` x4 at 661:16 `_err`, 1068:19 `body`, 1503:16 `err`, 1579:14 `err`, and `no-useless-assignment` x1 at 1187:11.
  - after (head): 0 errors, 3 warnings: 1068:19, 1187:11, 1579:14. Exactly 661 and 1503 are gone, and nothing new appeared.

### 3. Robustness of the new test - PASS (one LOW, three INFO)
- **Anchor reworded** (control: "Network/timeout" -> "Network or timeout"): C1 fails cleanly with `expected -1 to be greater than 0` from the `expect(at).toBeGreaterThan(0)` guard. It does not pass vacuously.
- **Anchor body line deleted** (mutant M2, the 1504 comment removed): C2 fails the same way, cleanly.
- **File moved** (verification.ts moved aside): C1 and C2 fail with ENOENT from readFileSync, and the 0-errors control fails with ESLint's "No files matching ... were found". 3 of 4 fail, so nothing goes green silently.
- **Comment-only control** (one comment line inserted at line 2, so every line shifts by +1): 4/4 green. The cells find their catch by the anchor, not by a hard-coded line number.
- **Anchor uniqueness**: each anchor string occurs exactly once in the file (asserted by my mutator). `findIndex` takes the first match, so a future duplicate would bind to the first one (INFO-2).
- **Config pickup / cwd**: ESLint 10 resolves `eslint.config.*` upward from the linted FILE, not from `cwd`. Linting the head file with cwd = Blockchain/Dev, = services/api-gateway, and = /private/tmp gave identical results (same rule config, the same 3 warnings). So `new ESLint({ cwd: DEV })` is correct but not what makes it work (INFO-1). Control: the same file copied outside the repo tree throws `Could not find config file.`, so a missing config fails loudly and cannot produce an empty-messages green.
- **Is the messages assertion live?** In every mutant the exact-text pin `toBe('} catch {')` fires first, so `expect(messages).toEqual([])` never got to decide a result (INFO-3). Probe: I removed the two text pins from a working-tree copy of the test and linted develop's file. C1 and C2 both failed with `expected [ Array(1) ] to deeply equal []`. So the line arithmetic (`m.line === at`, where `at` is the 0-based index of the anchor, which equals the 1-based number of the catch line above it) is right, and the assertion is live, not vacuous.
- **Planted-binding control (cell 3)**: `lintText` with `filePath: FILE` reports `@typescript-eslint/no-unused-vars` for `catch (_e)`. This proves the rule applies to that path and that underscore names are not exempt for caught errors.
- **Runtime**: about 0.46 s for the file (C1 377 ms, which includes the first lintFiles; C2 43 ms; C3 2 ms; C4 34 ms). The 60 s per-cell timeouts are generous but harmless.
- **LOW-1**: ks1543-five-pre-existing-eslint-warnings-in.test.ts:26 and :32. The two product cells are titled "RED KS-1543 C1/C2" but are green at head. This is a naming convention only (the title records "red before the fix"). It does not affect results. Rename if the repo convention asks for it.

### 4. Whole api-gateway suite + tsc on a program that includes the test - PASS
- Full suite at head (`npm --prefix <clone>/services/api-gateway run test -- run`, json reporter): 119 files, 1157 tests, 1157 passed, 0 failed, 0 skipped, 13 s. The ks1543 file is in the run.
- `tsc -p tsconfig.test.json` (noEmit, includes src/__tests__): 662 program files (`--listFilesOnly`), and both the ks1543 test file and routes/verification.ts are in the list. Head: 35 errors. develop tree (develop verification.ts, new test moved aside): 35 errors. The error SET is identical once line:col is stripped, and there are 0 errors in the ks1543 file or in verification.ts. The 35 are older ones in csrf.test.ts, rateLimitEnforce.test.ts, ks1165-*, notifications.test.ts and others.
- Planted-error control: one TS2322 line appended to the ks1543 test file -> 37 errors (TS2322 + TS6133 at ks1543...test.ts(49,7)). The file really is type-checked. Restored with `git checkout --`, and `git status` was clean afterwards.
- Leg 16 ratchet (`scripts/preflight/test-types-ratchet.sh services/api-gateway`): "tsc examined 154 files, 119 of them under __tests__; 35 errors: 35 in the baseline, 0 new; 0 stale" -> OK, rc 0. Planted control (a type error appended to the test file) -> FAIL, rc 1. Restored.

### 5. Mutants + comment-only control - all killed, controls behave
| run | change | ESLint warnings | result |
|---|---|---|---|
| M1 | 661 binding restored, `catch (_err)` | 4 | C1 FAIL (text pin) - killed |
| M1b | 1503 binding restored, `catch (err: any)` | 4 | C2 FAIL (text pin) - killed |
| M2 | catch-body line 1504 (the anchor comment) deleted | 3 | C2 FAIL (anchor -1) - killed |
| M2b | non-anchor body line 663 ("remains honest...") deleted | 3 | 4/4 green - survives, as expected: the test pins the catch form, not the comment prose; the diff review in item 1 covers the bodies |
| M3 | 661 `catch (_err) { void _err;` (binding used, lint-clean) | 3 | C1 FAIL (text pin) - killed |
| CTRL | comment-only line inserted at line 2 (shift +1) | 3 | 4/4 green - control holds |
| CTRL | anchor 661 reworded | 3 | C1 FAIL cleanly (anchor -1) |
| CTRL | verification.ts moved | n/a | 3/4 FAIL, ENOENT / no files matching |
After every run, `git checkout --` restored the file and `git status --short` was empty.

### 6. Merge prediction on the live tip - PASS, clean
- Live develop re-read just before this step: 0bb4f17ca (unchanged). It is an ancestor of the head, so the merge is a fast-forward or trivial merge. `git merge-tree --write-tree develop head` rc 0, tree afc9fa6b5b99..., which equals the head's own tree.
- Planted conflicting control: a scratch commit on the tip changing 661 to `catch (_e)` -> merge-tree rc 1, `CONFLICT (content): Merge conflict in .../verification.ts`. The predictor can fire.
- Overlap: I fetched PR heads #1540-#1559. Two touch verification.ts relative to their merge-base with develop: #1556 (this one, the positive control) and #1554 (KS-1542, verification.ts:147-159, `shown` formatting). #1554's post-image blob 8b63b676f is develop's current verification.ts blob, so its content is already on develop. merge-tree of #1554-head x #1556-head in either order is rc 0 with tree afc9fa6b5b99..., the same tree. No pending overlap.

## NOT tested
- ESLint over the whole tree or the other services. Only routes/verification.ts was linted. The other three warnings (1068, 1187, 1579) are part 2 and were not examined.
- CI on GitHub, Docker/e2e, any deployed environment, the frontend, and other services' suites.
- Runtime behaviour of the two catch paths under a real network/DB failure (no live anchor service or DB). The equivalence rests on language semantics plus "binding unused", not on an exercised failure.
- Whether the PR is open or mergeable on GitHub (no GitHub API read). The merge prediction is local merge-tree only.

## Severities
- HIGH: none. MEDIUM: none.
- LOW-1: src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts:26,:32. The "RED ..." titles are on cells that are green at head (naming only).
- INFO-1: test file :13 `new ESLint({ cwd: DEV })`. cwd does not drive config lookup under ESLint 10 (file-relative lookup). It is harmless, and the outside-tree control shows a missing config throws.
- INFO-2: test file :18 `findIndex` binds to the first anchor match. Both anchors are unique today. A future duplicate comment would silently pick the first one.
- INFO-3: test file :29 and :35 `expect(messages).toEqual([])` is shadowed by the exact-text pin in every realistic mutant. The probe shows it is live (it fires on develop's file once the pins are stripped). It is belt-and-braces, not vacuous.

## Hygiene
No write verb in !CODING (only `ls-remote` there). No push, no GitHub/Linear writes, no Docker. Nothing deleted. npm/vitest ran with `npm --prefix <clone>/Blockchain/Dev/services/api-gateway`. One deviation: `npm ci --ignore-scripts` + the `packages/shared` build ran with `--prefix <clone>/Blockchain/Dev`, because api-gateway is a workspace member whose ESLint config and dependencies resolve from the Dev root. It ran inside the clone only, the same pattern as gate A. /Volumes/DevMASTER/WEDNESDAY/node_modules was checked absent after every step script.
