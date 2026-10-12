# Gate verdict: Secuura Platform K PR #1514 (KS-1519), tier 2 (Sonnet, test-only)

- Head under test: c2676012cab6ea21319a2b37a41ca436aaff372f (fetched refs/pull/1514/head, equals the stated sha exactly)
- Base: 629349dac602fa39087e934d4b77e52b18afbc94 (parent of head, one commit)
- Develop now: 551dc9808aee1c89d217cd662628c17ef8ad3a0e (`git ls-remote origin refs/heads/develop`, read by me)
- Tree: scratch clone (`git clone --shared`, fetch of the PR ref and develop with the project's core.sshCommand), `git archive` of Blockchain/Dev plus root CLAUDE.md (the file's last REAL cell reads it) for head and for base, node_modules shell of symlinks to the main checkout's deps (read-only), @secuura/* links relative so they resolve inside the scratch tree, packages/shared built (tsc rc 0) in each tree. Blob of the test file in the extracted tree = 0b7b712a (same as the PR blob). Nothing written inside !CODING.

## VERDICT: GO WITH NOTE

Majors: 0. Minors: 3 (all about the guard and call-site protection, none a defect in what the PR claims).

## Findings

Major: none. No converted cell is weakened (12/12 at least as strict, mechanical read plus control below).

Minor 1 (guard is narrow, attack point 1 confirmed): test file L524-530, `shape = /expect\(\[[^\]]*\.status[^\]]*\.out/`. It catches only a single-line array with status BEFORE out. Measured NOT caught, all 35/35 green: (a) object shape `expect({ status: r.status, out: r.out }).toEqual({...})` (M1); (b) reversed array `expect([r.out, r.status])` (G_reversed_array); (c) the array split over several lines (G_multiline). The control that the matcher fires on the forbidden shape is real (G_oldshape_control: guard red at the planted line). Acceptable for a test-only PR whose guard names the shape the ticket named; the regression it can miss is a future cell written in an object or multi-line form, which would again put status+output in one compared value and bring back the "expected [ 1, ...(1) ] to deeply equal" headline. Suggest (non-blocking): also forbid `.status` and `.out` inside one `expect(` call across newlines, e.g. scan joined text with `/expect\(\s*[\[{][^)]*\.status[^)]*\.out|expect\(\s*[\[{][^)]*\.out[^)]*\.status/s`.

Minor 2 (helper tests do not protect call sites, attack point 2 in a different form): the six KS-1519 cells test `expectRun` itself, not that each of the 12 call sites still passes a real predicate. A call site weakened later (REAL gate cell reduced to `expect(r.status, r.out).toBe(0)`, mutant M3) stays green 35/35. Not introduced by this PR (the pre-PR cell had the same exposure) and the REAL cell keeps a separate regex on the examined-file count, so only the summary-string predicate would be lost. Note only.

Minor 3 (claim wording, not a defect): the PR's own helper doc comment and ticket premise are accurate as narrowed ("red names neither file nor code" is true for the JSON reporter, headline and long outputs). I did not re-measure the "7-line diff hunk shows 3 of 40 planted errors" figure (see NOT TESTED).

Observation, not a finding: dropping an expectation inside the helper leaves an unused parameter, a NEW TS6133 in this file, which the REAL cell reports (the file is inside the ratchet's own scope). Reproduced: T1 and T2 each go red on 2 cells, not 1. Builder's explanation for T3/T4 first mismatching is consistent with what I saw.

## Topology (job 1)
- `git diff --stat 629349da..c2676012`: 1 file changed, 81 insertions, 12 deletions, the ks1000 test file only.
- Develop changes since 629349da (`git diff --name-only`): 6 files: Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh, Blockchain/Dev/scripts/preflight/test-types-ratchet.sh, four under Blockchain/Dev/services/security/src. Overlap with the PR's one file: EMPTY (count 0; positive control: the PR file appears in its own diff list, count 1 on the ks1000 name).
- `git merge-tree --write-tree develop 1514`: exit 0 (clean), tree 9c974b10e376ef0fcd4ff06bdea18fe65410860e = the prediction exactly.
- merge-base(1514, develop) = 629349dac602.

## The 12-cell equivalence read (job 2)
Method: (a) read each old/new pair by eye from the diff; (b) a script (scratchpad `equiv.py`/`equiv2.py`) parses the 12 old `expect([run.status, run.out, ...]).toEqual([n, expect.stringContaining|stringMatching(x), ...])` lines from the BASE file and the 12 `expectRun(...)` calls from the HEAD file and compares run variable, exact status literal, predicate kind and argument verbatim, third values (each must exist as a separate `expect(<same expr>, msg).toBe(<same expected>)` within 3 lines) and label. 12 old, 12 new, 0 flags.

| # | base L | head L | status | output predicate | extra value | verdict |
|---|---|---|---|---|---|---|
| 1 | 76 init() | 88 | 0 = 0 | contains 'wrote' = same | none | equal |
| 2 | 157 REAL gate | 169 | 0 = 0 | contains '0 new; 0 stale baseline entries' = same | none | equal |
| 3 | 220 CONTROL stub | 232 | 0 = 0 | contains '1 in the baseline, 0 new' = same | label kept | equal |
| 4 | 329 roots loop | 341 | 0 = 0 | contains '...0 new; 0 stale baseline entries' = same | old compared `dir` to itself (tautology); now only in the label, nothing lost | equal |
| 5 | 338 unrelated edit | 350 | 0 = 0 | contains = same | none | equal |
| 6 | 362 twoFloors | 374 | 2 = 2 | regex `/baseline\.txt:\d+:.*examined-test-files/s` = same (stringMatching == toMatch) | none | equal |
| 7 | 365 dup | 377 | 2 = 2 | regex `/...duplicate/s` = same | none | equal |
| 8 | 376 CRLF | 388 | 0 = 0 | contains = same | none | equal |
| 9 | 400 --init refuses | 412 | 1 = 1 | contains '--init refuses' = same | `fs.existsSync(bl(initDir))` false -> separate `.toBe(false)` | equal |
| 10 | 405 --rekey refuses | 418 | 1 = 1 | contains '--rekey refuses' = same | baseline file == `legacy` -> separate `.toBe(legacy)` | equal |
| 11 | 412 --update refuses | 426 | 1 = 1 | contains '--update refuses' = same | baseline file == `before` -> separate `.toBe(before)` | equal |
| 12 | 450 hoisted run b | 465 | 0 = 0 | contains = same | none | equal |

Edge semantics checked: `toContain` on a string is substring like `stringContaining`; `toMatch(regex)` is `regex.test` like `stringMatching`; `toBe` on a number/string is as strict as `toEqual`; a null status fails `toBe(n)`. Cells 10/11: the old array evaluated the file read before asserting; the new one asserts status first, then reads; the failure set is the same.

CONTROL for the read: I planted 5 weakenings in a copy of the head file (cell 6 status 2->1, cell 1 predicate 'wrote'->'wrot', cell 7 regex `duplicate`->`duplicat`, cell 9 existsSync assertion deleted, cell 10 `.toBe(legacy)` -> `.toBeDefined()`); the script flagged exactly those 5 (cells 1, 6, 7, 9, 10), 0 false flags on the real head.

## What I ran (results)
All via node wrappers that chdir; every mutation was in the scratch tree, with the file restored and sha256 (or git blob hash) compared after each run (all `restored_sha_ok=True`; head test file blob = 0b7b712a, check.cjs blob = 937a01db, both equal the PR tree after all mutants).

1. Head file: 35 passed / 35 (default reporter). Base file (helper-less): 29 / 29. (Without root CLAUDE.md in the extracted tree one limits cell fails by ENOENT; with it, green: harness artefact, fixed.)
2. Red-first (job 3): head file with `expectRun` rewritten to the OLD behaviour (`expect([r.status, r.out]).toEqual([status, ...])`) = 29 passed / 6 failed: the 4 message cells + the guard (L81 named) = the claimed 5, plus the REAL gate cell (my rewrite leaves `label`/`message` unused: a new TS6133 in this file, so the REAL cell reports it). Its headline was exactly "expected [ 1, …(1) ] to deeply equal [ +0, StringContaining{…} ]", the defect the PR fixes. Then head = 35/35.
3. Tampers redone (job 4), red sets (cells that failed), against 35 total:
   - T1 drop helper status expectation: 33/35; REAL cell (TS6133) + "wrong STATUS alone" cell
   - T2 drop helper output expectation: 33/35; REAL cell + "missing SUMMARY alone" cell
   - T3 message = label only (output removed): 31/35; the 4 RED message cells
   - T4 message = first 5 lines: 34/35; only the "WHOLE output (12 errors)" cell
   - T5 output expectation -> toBeDefined: 34/35; only "missing SUMMARY alone"
   - M2 (mine) status expectation -> toBeDefined: 34/35; only "wrong STATUS alone"
   - M3 (mine) output expectation dropped in the REAL gate cell: 35/35 GREEN (not caught; Minor 2)
   - M1 (mine) object-shape comparison in init(): 35/35 GREEN (not caught; Minor 1)
   - G_reversed_array, G_multiline (mine): 35/35 GREEN (Minor 1); G_oldshape_control (positive control): guard red at the planted line, 34/35
   - Three-value cells individually (attack point 4), tampering check.cjs so the refusal still happens but also writes: C_init_writes -> only the refusal cell red, message "--init must write nothing: expected true to be false"; C_rekey_writes -> only that cell, "--rekey must leave the baseline as it was: expected 'x\n' to be 'src/__tests__/b.test.ts TS2322 1\n'"; C_update_writes -> same cell, "--update must leave the baseline as it was". Also status 1->2 in the --init refusal (cell red: "expected 2 to be 1", with the checker output in the message) and the text 'refuses'->'declines' for --update and --rekey (red, output shown). All three extra assertions are alive and fail at their own message.
4. Real red message (job 5): planted `export const zzPlanted: number = 'x';` in a copy of auth.integration.test.ts (blob restored, sha equal), ran the REAL cell: default reporter shows the checker's "NEW type errors (not in the baseline): src/__tests__/auth.integration.test.ts(1637,14): TS2322: Type 'string' is not assignable to type 'number'." in the failure text; JSON reporter failureMessages[0] carries the same lines (file, line, TS code) followed by ": expected 1 to be +0 // Object.is equality"; tap and dot reporters each contain TS2322 (count 1). Positive control for the greps: the same files show the planted string.
5. Guard `__filename` (job 6): the CJS auth package (no "type" field): a probe test (`.test.ts`) and an ESM `.test.mts` probe each read `fs.readFileSync(__filename)` and assert its own content = 2 passed. With `"type": "module"` temporarily set in services/auth/package.json (restored, sha equal): probes + the real guard cell = 3 passed. vitest/vite-node injects `__filename`/`__dirname` in both module systems, as it already does for `__dirname` used 5 times in this file.
6. Auth suite in full (head): 93 files, 1024 tests, 1024 passed, 0 failed, 0 pending (JSON reporter; one run). Matches the claim.
7. `check:test-types` (both halves, run as the script does): auth `42 errors: 42 in the baseline, 0 new; 0 stale`, 93 of 144 files under __tests__, rc 0; api-gateway `35 in the baseline, 0 new; 0 stale`, rc 0.
8. ESLint on the file (services/auth cwd): rc 0, no output. No positive control run for ESLint (see NOT TESTED).
9. `tsc --noEmit -p .` in services/auth: rc 0.

## NOT TESTED
- The file and suite on the MERGED tree (develop 551dc980 + PR): only merge-tree cleanliness, tree hash and path disjointness were measured; no run on the merged tree.
- The claim "a short output in text reporters shows 3 of 40 planted errors in a 7-line diff hunk": not re-measured (only the headline and JSON effect, via the old-helper variant).
- ESLint has no positive control (a known-bad file) from me; rc 0 on empty output only.
- Other services, platform suites, the push hook / preflight (13/16 legs claimed), the preflight leg-16 script test, CI. Auth suite ran once (no flake repeat). api-gateway vitest suite not run (only its ratchet).
- Builder's other 5 tampers (their exact list was not given); I redid 5 of the claimed 10-style helper tampers plus the 3 per-cell tampers plus 4 of my own.
- Scratch leftovers (cannot delete by rule): zz-probe-fn.test.ts/.mts in the scratch auth tree only; no effect on any repo.
