# QA gate: Secuura Platform K PR #1509 (KS-1237, row X-MSG-MEMBER, tier 2 test-only)

- Head: `d77e513cfd18b0216692e3c6a6562a21deef6a29`. Bundle sha256/16 `9e6a881bce8d2fb1`; `git bundle verify`: "The bundle requires this ref: 88c348375bd3083e0d9bef191f610ca9289c59ab"; `list-heads` = `d77e513c... refs/heads/feature/ks-1237-...`.
- Base: develop `88c348375bd3083e0d9bef191f610ca9289c59ab`. Real current tip (`git ls-remote origin refs/heads/develop`, read-only): `36f0f56f3698af70a75b8c663df028539da200b7` (= builder's #1507 tip; head is 1 commit behind it).
- How I got the tree: scratch clone `scratchpad/g1509/repo` (local clone of an earlier gate's scratch clone), `git fetch <bundle> d77e513c...`, read-only fetch of develop, detached worktrees `g1509/merged` (tip 36f0f56f + `git merge --no-ff` of the head) and `g1509/base` (88c34837). node_modules in both worktrees are SYMLINKS to the project's installed `2_Project_Files/Blockchain/Dev/node_modules` (and per-service ones), as earlier gates did; `packages/shared` rebuilt in each worktree (`tsc` rc 0, 29 dist entries). Caches written through those symlinks by vitest/tsc were not measured. Nothing written under `!CODING` except that. Scripts in `scratchpad/g1509/tools/`.

## VERDICT: GO

MSG1 reproduces everything claimed: 11/11 on head, 10/10 on base, 114 files / 1101 tests on the merged tree, 13 of 13 message/registration mutants (8 builder-shape + 5 own) red on exactly the predicted cell, and the guard is a single emit site whose message MSG1 pins by full-string equality for typed and untyped bodies.
Only Minor/Note findings (the cell pins one non-array shape; a gutted cell body would survive), none blocking a test-only PR.

## By my runs

**1. Bundle / diff / merge / tree.**
- `git log --oneline 88c348375..d77e513cf` = one commit, "KS-1237: pin the refusal message of a non-array connector allow-list". `git merge-base 88c348375 d77e513cf` = `88c348375bd3083e0d9bef191f610ca9289c59ab`.
- `git diff --stat 88c348375 d77e513cf`: "1 file changed, 10 insertions(+), 1 deletion(-)"; `--name-only` prints only `Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts`. No product line, config or CLAUDE.md.
- Builder's `pr1509_full.diff` (sha256/16 `b7c9dcd4522e37c9`) vs `git diff` of the head: `cmp` differs at char 275 (the `index` line, abbreviated hash length 7 vs 9); with `sed 's/^index .*//'` on both, `diff` prints nothing and "diff identical modulo index line". Applying `pr1509_full.diff` to the pristine base worktree (`git apply --index` then `write-tree`) = `f3dbcf51e2a9fe9d9fd482e76e35635c98b80833` = head tree `git rev-parse d77e513cf^{tree}` (builder's f3dbcf51e2a9: match).
- `git log 88c348375..36f0f56f3` = 1 commit ("KS-1090: preflight leg 16 also gates the api-gateway test-file ratchet"), files: `scripts/__tests__/preflight_test_types_ratchet_leg.test.sh`, `scripts/preflight/test-types-ratchet.sh`, `CLAUDE.md`: disjoint from the PR's one file.
- `git merge-tree --write-tree 36f0f56f3 d77e513cf` = `1f54e0b9ad986c31c2bbee2e1f5d80a81e4a6f2f`, rc 0; the real `git merge --no-ff` in the `merged` worktree: "Merge made by the 'ort' strategy", tree `1f54e0b9ad986c31c2bbee2e1f5d80a81e4a6f2f` (builder's prediction 1f54e0b9ad98: match). `git status --short | grep -v '^??'` prints nothing after all my runs (rc 1), i.e. no tracked file left modified (the `??` lines are the node_modules symlinks, which the unfiltered `git status` printed).

**2. The guard.**
- `git grep -n "refusing until it is corrected" 88c348375bd3` finds 3 lines: `routes/verification.ts:1298` and `services/health.ts:67` (both "Connector allow-list container is malformed; ...") and `routes/verification.ts:1308` ("Connector document-type allow-list is not a list; refusing until it is corrected"). `git grep -i "is not a list" -- Blockchain` on the merged tree: product = `verification.ts:1308` only (the other two hits are the test file).
- `Blockchain/Dev/services/api-gateway/src/routes/verification.ts:1306-1309`: `const rawAllowedTypes = connectorConfig.allowedDocumentTypes; if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !Array.isArray(rawAllowedTypes)) { res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector document-type allow-list is not a list; refusing until it is corrected' } }); return; }`. It runs before `body.documentType` is read (line 1319 `requestedType`), so typed and untyped bodies get the same fixed string. That is the single emit site of the non-array-allow-list refusal; MSG1's literal equals it character for character (the message test passes, and 1-char/whitespace/case mutants of it go red, section 4).
- Other related sites, none emitting this refusal: 1298 and `health.ts:67` (container malformed, a different failure), 1292 area 503 (read thrown), 1322-1324 (type not permitted, array lists), `routes/admin.ts:1136-1139` (write-time 400 for non-array allowedDocumentTypes). MSG1 reaches line 1308 only, which is the only site in scope.
- Builder's claim "existing cells assert status and code for other shapes but not the message": `grep -n message` in the test file on the merged tree shows `message` only at lines 254-259 (MSG1) and 300 (the array-list refusal "...not permitted to register document type..." cell, a different message), and 308 (a RAN name). The three NON_ARRAYS cells, the string-vs-DOCUMENT cell and AL1 assert `[status, error.code, ...]` only. Confirmed.

**3. Runs.**
- Head (merged tree), the file: `Test Files 1 passed (1) / Tests 11 passed (11)`. Base worktree, same file: `Tests 10 passed (10)`. (Builder: 11/11 and 10/10.)
- Full api-gateway suite on the merged tree (`npx vitest run` in services/api-gateway): `Test Files 114 passed (114) / Tests 1101 passed (1101)`. (Builder: 114 / 1101.)

**4. Mutants** (script `tools/mut.py`, run on the merged tree; each applied alone; red set read from `--reporter=json` failed assertions and compared by EQUALITY with the predicted set; control with no mutation: red = {} of 11). Every line below also printed `sha256/16 before = after` (product `verification.ts` `b82b86a9d8038c57`, test file `26f64442b290c132`), "restored-identical", and 0 MISMATCH.
- Builder's shapes (re-implemented by me; I did not have the builder's mutant files, so the exact brief tamper is a stand-in for P1 = message names the caller's own type via `body.documentType`): P1 red = {MSG1} EXACT; P2 (message names the resolved type) {MSG1} EXACT; P3 empty message {MSG1} EXACT; P4 tail trimmed ("...is not a list") {MSG1} EXACT; P5 untyped-only wrong {MSG1} EXACT; P6 typed-only wrong {MSG1} EXACT; R1 COMPLETENESS entry removed {COMPLETENESS} EXACT; R2 MSG1's `RAN.add` removed {COMPLETENESS} EXACT.
- My own: M1 one char (`list;` -> `list,`) {MSG1} EXACT; M2 whitespace only (`is  not`) {MSG1} EXACT; M3 trailing space {MSG1} EXACT; M4 case (`connector`) {MSG1} EXACT; R3 `RAN.add('non-array message clazz')` (entry present, add on a different name) {COMPLETENESS} EXACT.
- Status/code asserted: M6 status 403 -> 400 on the guard line: red = MSG1 + AL1 + the 4 older non-array cells; M7 code `FORBIDDEN` -> `FORBIDDEN2` on that line: same 6 red. So MSG1 goes red on status and code too (it is red among them; the older cells co-fail so not "alone", as expected).
- Survivors (green, red = {}): M5 guard returns the right message only for a STRING allow-list and the container message for any other non-array: 11/11 green, i.e. MSG1 does not see non-string shapes (Minor 1). R4 MSG1's body gutted by `return;` before its assertion, RAN.add kept: 11/11 green (Note 3).

**5. Right reason.** MSG1 uses `toEqual([403,'FORBIDDEN',message,403,'FORBIDDEN',message])` where `message` is the whole 80-character string: full equality, not a substring/regex. Green on the unmodified product (section 3) and red on 10 distinct product changes of the message, including the 1-char, whitespace-only and case ones (section 4). It also asserts `status` and `error.code`. Typed and untyped halves are each pinned (P5 and P6 each red alone, M-series each red). Not a vacuous-substring pass.

**6. Test-type ratchet and lint** (merged tree, `npm run check:test-types` from `Blockchain/Dev`, rc 0):
- `typecheck-tests: auth ... tsc examined 144 files, 93 of them under __tests__; 42 errors: 42 in the baseline, 0 new; 0 stale baseline entries.`
- `typecheck-tests: api-gateway ... tsc examined 149 files, 114 of them under __tests__; 35 errors: 35 in the baseline, 0 new; 0 stale baseline entries.` So on the gateway: examined 149, in baseline 35, new 0, stale 0 (the builder's figures, and the gate leg 16 now actually covers).
- `npx eslint <file>` rc 0, no output. Planted-`debugger;` control: `313:1 error Unexpected 'debugger' statement no-debugger`, rc 1; file restored via `git checkout`, sha256/16 `26f64442b290c132` before = after.

**7. Other.**
- `grep -niE "\.(only|skip|todo|runIf|skipIf|concurrent)\b|\bxit\b|\bxdescribe\b|\bif \("` on the file: only two hits, both inside the harness (line 120 `if (req.url === ...)`, 149 `if (principal.authMethod ...)`), none in a cell; 9 `it(` lines (control, 8 literal + the NON_ARRAYS loop = 11 tests). No `.only`, no skip, no conditional around `RAN.add`. Registered names printed: 8 `RAN.add` calls (one a template over 3 labels) = the 10 COMPLETENESS entries; the list is compared with `toEqual` on sorted arrays, so an extra or missing name goes red (R1-R3).
- Test titles: no duplicates (`MSG1` title unique; `sort | uniq -d` count 0).
- State: `connectorAllowedTypes` is reset by `afterEach` to ABSENT for both describes holding it; `principal` is set at the top of each `createDocumentWithBody`; MSG1 sets its own allow-list. With `--sequence.shuffle` seeds 1-5 on the head: 4 green, seed 3 red with only COMPLETENESS failing (it needs the earlier cells to have run). The same seed 3 on the BASE worktree: `Tests 1 failed | 9 passed (10)`, COMPLETENESS alone. So that order dependence is pre-existing, not introduced. No shuffle/sequence option in `services/api-gateway/vitest.config.ts` (grep rc 1), so the default order is file order. `-t MSG1` alone: 1 passed, 10 skipped (COMPLETENESS is skipped, not failed).

## Findings

**Major**: none.

**Minor**
1. `...ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts:254-260` (MSG1): pins the message for the string allow-list `'SSD_DOCUMENT'` only. Mutant M5 (the right message for a string, the container-malformed message for any other non-array) leaves 11/11 green. The product has one emit site today so the risk is low, and the builder stated it ("one shape pins it"); it is a real limit of what the cell proves. A loop over `NON_ARRAYS` (+ the array-like) inside MSG1 would close it.

**Note**
2. `verification.ts:1308` is the only emit site, but `services/health.ts:76` (`allowedDocumentTypes: connectorConfig.allowedDocumentTypes || []`) hands a non-array stored value back to the connector unchanged; out of scope for this test-only row and not tested by it (I did not run it; read-only observation).
3. A cell whose body is gutted before its `expect` (R4: `return;` ahead of the assertions, `RAN.add` kept) stays green: COMPLETENESS only proves the `RAN.add` line ran. Same property as every older cell in the file; not new in this PR. `expect.hasAssertions()` would close it.
4. COMPLETENESS depends on cells having run earlier in the file (fails under `--sequence.shuffle --sequence.seed=3` on base and head alike). Pre-existing.
5. Hook gap the builder disclosed: leg 16 on the branch cut from 88c3483 printed the AUTH-only line. The merged-tree check above (gateway 149 examined / 35 baseline / 0 new / 0 stale, rc 0) is what covers it now.
6. In P1 I used a stand-in for "the brief's tamper" (message built from `body.documentType`), since I did not have the brief; the builder's P1 may differ in text, and the test result for any message other than the exact literal is the same red (M1-M4 cover one-character changes).

## Not measured

- Schemathesis, Akto, Playwright, k6, the pre-push preflight legs 1-16, CI, GitHub PR body/mergeability.
- The other services' suites, and a run of leg 16 itself (I ran its `check:test-types` command directly).
- Whether vite/tsc wrote cache files through the node_modules symlinks into the project install.
- Any non-string non-array shape against the real guard for MSG1 (only the string is in the cell); other shapes' messages (object, array-like, empty string) were not asserted by any cell and I did not measure them beyond reading line 1306-1309.
- Anything on other OS/Node versions than the host's.
