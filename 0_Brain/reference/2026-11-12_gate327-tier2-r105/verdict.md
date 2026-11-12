PR 2203: GO WITH NOTES · PR 2206: GO WITH NOTES (heads 67baaef2f105 / 36c0b86b3dd0; tier 2)

Gate 327, tier 2 (Sonnet), one session, 2026-11-12 about 12:57 to 13:20 AEDT. Findings only: nothing pushed, commented, mailed, merged or written to Linear. Every write verb, install, build and test ran under `scratch/` of this folder (`scratch/repo` fresh clone, `scratch/wt` worktree; `npm ci --ignore-scripts`; `packages/shared` built there so `@secuura/shared` resolves). The project checkout was only touched by an accidental READ (see NOT TESTED, item 1). Node v26.8.1.

## Pins (`scratch/pins_start.txt` 12:58:19, `scratch/pins_end.txt` 13:15:18)
- develop 1247e1af3c203d369d01b4d574de377adeec4b98, PR 2203 head 67baaef2f105c4fcf03bd66660d91fb990be7d2d, PR 2206 head 36c0b86b3dd0d634c635f72e1a854872f56f5a4d: all three equal the commission and UNMOVED start to end.
- PR 2203: ONE commit, merge-base 697f422f1a39. PR 2206: ONE commit, merge-base 088fa84da10c. `git merge-tree --write-tree origin/develop pNNNN` (own merge-bases): 2203 rc 0 tree 63598e665758; 2206 rc 0 tree 29889af05f1d. Both clean.
- `git diff --stat <base> origin/develop` on each row's own paths is EMPTY (develop did not touch any path of either row since the cut), so checking a row's files out of its head onto develop's tree is the merge tree for these paths. I tested that way.

## Scope (numstat at the cut)
- 2203: `services/transfer/src/index.ts` 1/1, the ks2055 test 18/0. Two files, +19 -1. Equals the READY.
- 2206: the ks1990 test 10/0. One file, +10. Equals the READY. No product source changed in either PR (index.ts line 427 is a comment, Q1).

## Q1. PR 2203 comment-only: PROVEN, and the comment is true
- `git diff` hunk is the single line 427. Emit by my own build (`scratch/emit.sh`, `tsc -p services/transfer/tsconfig.json`, the whole service, 11 .js files):
  - with `--removeComments`: `diff -r emit/develop/nocomm emit/head/nocomm` rc 0 (identical); `index.js` sha256 69043f1939fe0d65... at both.
  - with comments kept: `diff -r` shows exactly one line (index.js 309), the comment text. So the PR changes the emit by that comment only.
  - Positive control (planted non-comment change `.max(1000)` -> `.max(1001)` at line 429, `emit/planted`): `diff -r` rc 1, the one differing line is `reason: zod_1.z.string().trim().max(1001).nullish()`. Restored (`cmp` against the saved bytes equal; tree status clean).
- Is the new comment false anywhere? Sentence by sentence against the code at head: "optional, a string, trimmed, at most 1000 characters" = `z.string().trim().max(1000).nullish()` (index.ts:429); "absent, null or empty records 'Cancelled by user'" = `reason || 'Cancelled by user'` (index.ts:964, `git grep` at p2203). "Kam's ruling 2026-11-11 set the 1000-character bound only": the vault daily note `daily/2026-11-11.md` line 64 reads "KAM 16:29-16:30 ... KS-2055 = b (1000 chars)". That supports "the bound". I did not read the card's options a/b, so "only" rests on the daily note's wording and on the seat's own G312 reading (see G327-2203-3).

## Q2. PR 2203 cells R7 and R8
- Whole transfer suite (`npm --prefix .../services/transfer test` = `vitest run`, no path argument; the run header names the service root): develop 18 files, 481 of 481; head 18 files, 483 of 483 (`out/transfer_develop.txt`, `out/transfer_head2203.txt`). Proof it is the whole suite: `find services/transfer/src -path '*/__tests__/*' -name '*.test.ts'` = 18 files and vitest's include is that glob; the summary says "18 passed (18)". Matches the seat's 481 -> 483.
- ks2055 file at head: 12 of 12 green (R7, R8 and the ten existing cells), `out/ks2055_head.txt`.
- Mutants on `index.ts:429`, file restored byte for byte (sha256 asserted equal), `scratch/mut2203.py`, `out/mut2203.txt`:
  - M0 unmutated control 12/12.
  - M1 the seat's plant `z.coerce.string().max(1000).trim().nullish()`: 4 of 12 fail: R2, R3, R7, R8. Reproduces the seat's "4 of 12".
  - M2 own, trim after the bound (`z.string().max(1000).trim().nullish()`, gate 312's T4): only R7 fails.
  - M3 own, boolean allowed (`.nullish().or(z.boolean())`): only R8 fails. M4 own, array allowed (`z.union([...string, z.array(z.string())]).nullish()`): only R8 fails. M5 own, zero allowed (`.or(z.literal(0))`): only R8 fails.
  - M6 own, no trim: R5, R6, R7 fail. M7 own, bound 1001: R1 and R4 fail (existing cells; control that the file still guards the bound).
- Do R7/R8 test what the ticket names? Yes. The cell comments cite G312-2182-3 (trim before bound) and G312-2182-4 (boolean, zero, array); `verdict.md` of gate 312 lines 113-114 define those items exactly so (`0_Brain/reference/2026-11-12_gate312-tier2-pr2179-2182/verdict.md`). Each of R7's and R8's four values is individually killed (M2 for R7; M3/M4/M5 each kill R8 alone).

## Q3. PR 2206 cell R6
- Whole originate suite under JEST (`npm --prefix .../services/originate test` = `jest`, no argument): develop **221 suites, 2,598 of 2,598**; head **221 suites, 2,599 of 2,599** (`out/originate_develop.txt`, `out/originate_head2206.txt`). The seat's counts reproduce. How I know it is the whole suite, not a path filter: (a) the package script is bare `jest` and jest prints "Ran all test suites." (a filtered run prints "Ran all test suites matching ..."); (b) `find services/originate/src -name '*.test.ts'` = 249, `-name '*.integration.test.ts'` = 28, 249 - 28 = 221, and jest.config's `testPathIgnorePatterns` excludes exactly the integration files; (c) `/usr/bin/grep -c '^PASS '` of the log = 221 and `'^FAIL '` = 0. Load1 was 10.9 to 18.9 during these legs (above the 8 rule; results green, see NOT TESTED).
- Mutants on `adminConfig.ts:2163` (`scratch/mut2206.py`, `mut2206b.py`; jest run of the ks1990 file only; file restored, sha equal; `out/mut2206.txt`, `out/mut2206b.txt`):
  - M0 control 12/12.
  - M1 gate 195's g1 `created === 0` -> `created < 2`: 1 of 12 fails, only R6.
  - M2 own, drop the created condition (`failed > 0`): R2, R4, R6 fail.
  - M3 own, `created < failed && failed > 0`: only R6 fails. M4 own, `(created === 0 || failed > 12) && failed > 0`: only R6 fails. M7 own, `created < 3`: only R6 fails.
  - M8 own, `created < 14`: R2, R4, R6 fail. M5 own, never 500: R1, R3, R5, L1 fail, R6 does not (R6 pins the 200 side only, as designed). M6 own, `created === 0` alone: control C2 fails, R6 does not.
  So R6 is the only cell that sees any threshold above 1 created. R6 is green at the head (12/12; whole suite 2,599).

## Q4. tsc with tests
- originate, scratch config extending the service's tsconfig with the tests included, `types node,jest` (`services/originate/tsconfig.gate.json`): **4 error lines at the head and 4 at develop, the identical lines** (diff rc 0): TS2300 `EmailModule` and TS2451 `saved` in `ks1937-email-service-logs-never-carry-the-recipient-address.test.ts`, and the same pair in `ks488-smtp-opt-in.test.ts`. 0 in the touched ks1990 file. Positive control: the grep for `error TS` finds those 4 in the same log. Equal at both: pre-existing, a filing note.
- transfer (`tsconfig.gate.json` with `vitest/globals`, `rootDir ../..`): rc 0, 0 errors at develop and at head (`out/tsc_transfer_*.txt`). The seat's "0 errors" reproduces. (My first attempt with `rootDir ./src` printed 4 TS6059 rootDir errors at both develop and head; that was my config, not the code.)

## Q5. Census (GraphQL, `scratch/census_gql.py`, every PR's files paged to totalCount and asserted)
101 open PRs, 449 file rows (the seat's was 99 / 435 at its cut; two newer PRs). Control `services/api-gateway/src/index.ts` -> [2125] FIRED; planted absent path -> []. Per path: transfer `index.ts` -> [2203]; the ks2055 test -> [2203]; the ks1990 test -> [2206]; `adminConfig.ts` -> [2087, 2158]. No shared path with any other open PR for either row. For the two adminConfig.ts PRs I read their hunks against their merge-bases (`git diff -U0`): 2087 head 954af815c7b7, one hunk +993,10 in `/api-keys`; 2158 head 74364b18dcf4, hunks 620 to 699 in `/dashboard`. Neither is in the `seed-demo-users` handler (line ~2100-2175), and neither touches the ks1990 test (name-only grep 0). Read-path overlap with line 2163: none.

## Q6. PR bodies (live, GraphQL, `scratch/prbody2203.txt`, `prbody2206.txt`)
- Both OPEN, not draft, base develop, MERGEABLE, heads equal the pins, `closingIssuesReferences` totalCount 0, one commit and one comment each. Closing-word scan with a python regex over each whole body: the only hits are "closing it is the board seat's call" (2203, a negation of acting) and "no closing word" (both); no `close(s|d)/fix(es|ed)/resolve(s|d)` before an issue key.
- Every `Refs` in 2203 is followed by KS-2169 (title, heading, two prose mentions); every `Refs` in 2206 is followed by KS-2005. 2206 names KS-1990, KS-1727 and KS-1739 without a `Refs` before them (the seat's slip (b) is fixed in the live body). Positive control: the same scan finds the `Refs KS-2005`/`Refs KS-2169` hits.
- I did not read Linear, so the attachment fact (the seat says exactly KS-2005) is not checked by me.

## Findings
- **G327-2203-1 (Info): comment-only change proven by my own build, with a planted control that changes the emit** (Q1). The new comment is true to the code and to the vault record of the ruling.
- **G327-2203-2 (Note): the cells are pins, not regressions.** The Spark gate's "BASE product code" run (head's test file against develop's product code) is 12 of 12, as it must be: the behaviour already shipped in PR 2182 and this PR only adds cells. Their titles start `RED` but they are green at develop; the red evidence is the mutants above (M1 to M5), which kill them. A reader of the file should read RED as "red against a wrong implementation".
- **G327-2203-3 (Note): "set the 1000-character bound only" rests on one daily-note line.** `daily/2026-11-11.md` records "KS-2055 = b (1000 chars)" and the card id `secuura-ks2055-cancel-reason-length-bound-1111`; I did not open the card text to confirm the options a and b did not also mention trim or type. The claim is plausible and not contradicted by anything I read; the comment is a credit line, not behaviour.
- **G327-2203-4 (Info): coverage limits that remain open, as the PR body says.** R7 pads with spaces only (no tab/newline/other Unicode whitespace) and R8 pins status 400 and no state change for four values (not the JSON-array request body, nor null-like strings); G312-2182-1, -2, -5 and the array body stay open per the body. Not defects of this PR.
- **G327-2206-1 (Info): R6 proven red against g1 and against five mutants of my own, green at the head, and the only cell that kills a created-threshold above 1** (Q3).
- **G327-2206-2 (Info, filing note): tsc with the test files reads 4 errors in `ks1937` and `ks488` at develop and at the head alike** (Q4). The repo's hook leg 16 baseline covers 5 services, not originate (the seat's finding c); a candidate for a board item, not this PR.
- **G327-2206-3 (Info): the PR's own measurements reproduced**: whole originate 221 suites 2,598 -> 2,599 (jest, whole-suite proof above), 12/12 file, g1 red-first (only R6), tsc 4 errors in two untouched files, census paths. Not reproduced by me: eslint (rc 0 / 29 warnings), docs-fragments, the pre-push hook, the Linear comment.
- **G327-2206-4 (Info): kit trap R105-F1 confirmed in principle**: the seat's note that `run` appended to a jest script reads as a path filter is consistent with what I saw: my first, hand-rolled filtered vitest call with `npm exec` ran from the wrong directory and collected 255 files (see NOT TESTED 1). Use the binary with `--root` and an explicit path for a filtered run, and `npm test` bare for the whole suite.

## NOT TESTED
1. One of my own filtered vitest calls (`npm --prefix X exec -- vitest run src/__tests__/ks2055`) ran from `/Volumes/DevMASTER/WEDNESDAY` as its working directory and collected 255 test files from other trees (quarantine copies and, through a symlink, the Secuura project checkout's transfer tests). It was a read-only run (tests only), I discarded its output, and then re-ran correctly with `vitest --root`. I have not checked whether vitest left any cache in those trees.
2. The pre-push hook and its 16 legs, eslint, docs-fragments (the seat says no fragment pair on either row), any database, Docker, stack, box, CI run, the four platform suites, another Node line or OS.
3. Linear: the comment, the attachment, the ticket text (so the Spark ran without ticket text).
4. Load: whole-suite legs ran at load1 10.9 to 18.9, above the 8 rule; all passed, so no flakiness was observed, but a timing-sensitive cell would not be excluded.
5. A merge of the two PRs with every other open PR (only paths, plus the two adminConfig.ts PRs by hunks); the seat's own 2203 comment-only hash `5ff9a5733b9cae4a` (my sha differs because I built the whole service with the repo's tsconfig; my claim is develop vs head equality).
6. A real merge commit: I tested by `merge-tree` (clean) and by checking each row's files onto develop's tree, valid because develop has not touched those paths.

## Spark (test-digest standard, then the shadow review; one request at a time)
- **Digests** (`scratch/digest/*`, raw logs kept in `scratch/out/`): transfer develop CHECKED PASS (366 B raw, 1.9 s), transfer head CHECKED PASS with delta (tests_passed 481->483), originate develop CHECKED PASS (41,243 B raw -> 1,105 B, 20.2 s), originate head CHECKED PASS with delta (2598->2599; 714 B, 16.1 s). All four statuses CHECKED; the counts equal my own reads. One Spark anomaly line (console log warnings in the originate logs) is true and harmless.
- **Gate (deterministic half)**, work dirs in the session scratchpad: 2203 targeted test on HEAD 12/12, on BASE product code 12/12 (expected, G327-2203-2); 2206 HEAD 12/12, BASE 12/12 (same reason). Diff stats 2 files +19 -1 and 1 file +10.
- **Review**, `spark_review.py --pr-body-file`, ticket text NOT supplied (`MISSING: ticket text`): 
  - PR 2203: verdict GO WITH NOTES, 8 findings, all Note, `comment_sentences_overstated` = []. Attempt 1 aborted on repetition, attempt 2 valid, `salvaged_partial` false. 
  - PR 2206: verdict GO WITH NOTES, 4 Note findings, valid on attempt 1. `comment_sentences_overstated` has three entries (the g1 red-first claim, the whole-suite 2,599 claim, the type-check claim): they flag the PR body's measurements as not in the gate's facts.json, not as false.
- **Recall against mine**: same verdict as mine on both. Of my substantive notes (2203-2 pins green at base, 2203-3 single-source ruling, 2203-4 coverage, 2206-2 pre-existing tsc, 2206-4 kit trap) it found none; the 2206-2 item is the one it touched indirectly (it names the type-check claim as unmeasured and says no more). Recall about 0 of 5 substantive; it also did not look into the comment's truth (its `comment_sentences_overstated` for 2203 is empty, which agrees with Q1).
- **False or wrong claims**: none fabricated. Its notes are true statements about what the gate's facts.json holds, and every claim it flags as unmeasured I measured independently and the PR bodies' numbers held. Wrong-flavour noise: finding 4 on 2203 contains the garbled text "483 tests on head)Skip"; its note that the PR "claims the JSON-array request body still answers 400 under the plant" is a reading of the body that I did not check (the array body stays an open item in the body). Reliability note: 2203's first attempt aborted on a repeated finding (22.9 k prompt tokens).
- Files: facts at `scratch/facts2203.json`, `scratch/facts2206.json`; reviews `scratch/review2203.json`, `scratch/review2206.json`; stdout/stderr copies `scratch/gate*_std*.txt`, `scratch/review*_std*.txt`.
