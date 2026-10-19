VERDICT: GO at head c336de8312211a188f22a41b63e68df8046bb293 (tier 2 delta, round 2 of 2; landing tree 9a3a5619e806511f2861ced32ae1aacc2a3cb8c7 on develop 722e07f19cee; 0 blockers, 4 notes)

Gate Z1 (re-run after the 17:31 reboot), tier 2 delta, Sonnet. Round 1 = X1 GO at 009749ed2565. Findings only; no fixes, no GitHub/Linear writes, nothing under !CODING (own clone in scratch, `z1r/repo`).

## Live refs (re-read by ls-remote at start and again before this verdict, identical both times)
- PR head `refs/pull/1613/head` = `c336de8312211a188f22a41b63e68df8046bb293`
- develop = `722e07f19cee683ea037930e601e380a9491f7b5`

## Q1 delta exactly as claimed: PASS
- `git diff --stat 009749ed2565 c336de831221`: 2 files, +60/-8: `routes/platform.ts` (+12) and `__tests__/ks1195-register-connector-mints-the-ruled-rate-limit.test.ts`. The platform.ts diff is the const + doc comment (+11 lines) and the single mint line `rateLimitWindow: CONNECTOR_RATE_LIMIT_WINDOW_SECONDS,` (value 3600).
- `git diff --stat origin/develop...pr1613`: exactly the same 2 files, 398 insertions, 0 deletions. `log origin/develop..pr1613` = 2 commits (8046b1fc7, c336de831) plus the merge 009749ed2.

## Q2 3600 accepted, stored, reaches the limiter: PASS
- Bound: `services/security/src/index.ts:667` `rateLimitWindow: z.number().int().min(60).max(86400).default(3600)` inside `createApiKeySchema` (:655), parsed at :1163. 3600 is inside [60, 86400]. (Same bound in `security.openapi.ts:309`.)
- Stored: `index.ts:1373` `rateLimitWindow: data.rateLimitWindow` into the key record; persisted via the `rate_limit_window` column (:421 column list, :436 `k.rateLimitWindow`).
- Returned by validate: `index.ts:1917` `rateLimitWindow: apiKey.rateLimitWindow`.
- Gateway: `middleware/auth.ts:249` reads `data.rateLimitWindow || 60` (the 60 is a fallback only if validate omitted it; it does not), carried onto req.user at :403, used at `middleware/rateLimitEnforce.ts:184` `windowMs = (user.rateLimitWindow || DEFAULT_MACHINE_RATE_WINDOW) * 1000`.
- NOT run: the security service itself or a live mint (no stack, no Docker). This is a read-trace plus the gateway's stub-based cells.

## Q3 controls and window cells fail when they should: PASS
Instrument: the PR's own test file, vitest 4.1.10, on the PR head tree. Base: 21/21. Positive control for "red is visible": every mutation below produced a red, and each was reverted (`git checkout --`) and base re-read as 21/21.
- W1 (window 3600 -> 60): 2 failed / 19 passed = WINDOW and ROTATE-WINDOW.
- W2 (mint line removed): 2 failed / 19 passed = WINDOW and ROTATE-WINDOW.
- Re-register (no rotate) path made to PATCH `/api/keys/...` with `{rateLimitWindow:3600}` only (no rate): CONTROL-1 red (1 failed / 20).
- Same with `{rateLimit:9999}` only: CONTROL-1 red. With both fields: CONTROL-1 red.
- Window-only body sent to a NON-key URL (`/api/other`) so only the `carriesCeiling` window arm can catch it: CONTROL-1 red (1/20), so the widened arm does real work.
- Window arm dropped from `carriesCeiling` (test-only edit, no prod mutation): CONTROL-2 red (1/20), CONTROL-1 stays green. This confirms the author's "1 / 20" and that CONTROL-2 is what guards the predicate.
- NOT run: eslint on the two files; the author's red-first run of the new test file against the round-1 platform.ts (2/19 claimed); push preflight.

## Q4 landing: PASS
- `git merge-tree --write-tree 722e07f19cee c336de831221` = `9a3a5619e806511f2861ced32ae1aacc2a3cb8c7`, rc 0, no conflicts: matches the author's prediction.
- Instrument control: the same command on the round-1 head 009749ed2565 = `db51b5bb4c807cadbacd08720e530a87a6e90509`, identical to X1's recorded landing tree.
- On that tree (scratch commit-tree, no ref, nothing pushed): api-gateway suite `vitest run` = 117 files passed, 1153 tests passed, 0 failed = the author's numbers.
- `tsc -p services/api-gateway --noEmit` on the landing tree: rc 0, empty output. Positive control: a planted `const zz: number = 'x'` gave rc 2 and TS2322; reverted.
- NOT run: other services' suites, the repo-wide typecheck/baseline of the preflight, deploy or post-deploy `X-RateLimit-Limit: 3000` check.

## Notes (none blocking)
1. Environment, not PR: a first run of the target file showed 7 failures (502s) because my clone's node_modules symlinks resolved `@secuura/shared` to the project's older built dist (missing `decideProvisionerRegistration`). Rebuilt `packages/shared` from the clone's own source and re-pointed `@secuura/*`; the earlier 1002-test run (40 failed files, same cause) is discarded. All reported numbers are from the corrected environment.
2. CONTROL-1 on its own reds for any `/api/keys` call by URL, so a window-only PATCH to the key surface is caught by the URL assertion first; the `carriesCeiling` window arm is guarded by the non-key-URL case above and by CONTROL-2. Fine as designed.
3. The control widening beyond "two lines + cells" is the one the author flagged. I find it justified (arm drop reds CONTROL-2) and recommend keeping it.
4. Heads must be re-read at the merge: this verdict is pinned to c336de831221 on develop 722e07f19cee; if either moves, the landing tree needs re-measuring.
a6554cb563be18111b644f44e600816b9b1e7aa1227a127daf5c3fbfad737ae2
