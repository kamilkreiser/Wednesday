GATE B1464: GO WITH FINDINGS @ 4aff7ec on main 6b0c5f2

Tier 2 (one test file, no product word). Gate run 2026-11-10 in a private clone under the session scratchpad (push URL set invalid, nothing pushed, no PR, no hosted HTTP, no listener started).

## Steps and measurements (all MEASURED by me, own programs)

1. Refs. `git ls-remote` of `b1464/hpsmpoc-walkthrough-instruction-row` = 4aff7ec4c13e02cb6aa767242bf90b029adf574a = READY sha. Main read now = 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb (unchanged). `git diff --name-only main hd` = exactly 1 path, `web/src/content/walkthrough/steps.test.ts` (1 of 1 inside OWNS). Overlap with PR #304 (13 files, web/src/components/**, web/src/server/mock/**) = 0; with PR #305 (8 files, api/**) = 0 (refs/pull/304/head d49be88, refs/pull/305/head 792c78f read over git, not the REST API; positive control for the overlap method: the method listed all 13 and 8 files). `git merge-tree --write-tree` of each of the two PR heads with this head: clean (exit 0).
2. Merge. `git merge-tree --write-tree main hd` exit 0, tree f58a810 = tree of hd exactly (main is the parent of the head), so merge = main plus the head blob (fa3bc40b for steps.test.ts). Branch is one commit on main 6b0c5f2: merges clean on current main.
3. CI by program, main vs head (web-unit = `npm test` = `vitest run`, ci.yml web-unit job; JSON reporter, each in its own worktree, same node_modules copy):
   - main 6b0c5f2: 285 files, 4187 tests, 4187 passed, 0 failed, 0 skipped.
   - head 4aff7ec: 285 files, 4187 tests, 4187 passed, 0 failed, 0 skipped. Merge tree = head tree, so merge = head.
   - By name: 1 test renamed (the row retitled), 0 other added, 0 other removed, 0 status changes. So the web-unit counts differ by nothing but the row's title (no new `it` rows; the new assertions live inside the one row).
   - web-build lint (`eslint --max-warnings=0`) exit 0; typecheck (`next typegen && tsc --noEmit`) exit 0 at head. `npm run build` not run: a `.test.ts` is outside the Next build graph (derived from the 1-path diff).
   - Hidden characters: `infra/tests/test_hidden_characters.py` (scans every tracked file) at head: 14 tests OK. Firing plant: a U+200B appended to the head's `steps.test.ts` in my worktree turns it FAILED (exit 1, "steps.test.ts:168:5 U+200B ZERO WIDTH SPACE"); restored, worktree clean.
   - No e2e spec, script or workflow reads `steps.test.ts`: `git grep -l -F steps.test` over web/e2e, web/scripts, .github, web/package.json = 0 (control on same method: `walkthrough/steps` in web/e2e = 2). ci.yml has no deploy job (header: "No deploy job"); the repo has no deploy-demo workflow; a merge triggers the ci.yml main run only (it keeps deploy packages, deploys nothing).
4. Red without the fix. Real steps.ts copy in my worktree with `Then <form> now.` inserted at the start of the first caveat, and again at the start of the first cue; new row vs main's old row (old test file from `git show main:`):
   - Baselines (no plant): old passed, new passed.
   - approve it / approve your plan / score it / score this / saving / submit / "Submit" / "do not save the plan": old PASSED (misses), new FAILED, in a caveat and in a cue (16 of 16).
   - score the / approve the / save: old failed, new failed (control: the harness can read red).
   - Mutants of the new row (one change per run): drop each of the 7 objects from `score` (7), from `approve` (7), each of the 6 verb alternatives (6), drop the `i` flag on score and on approve (2), exemption widened to `do not save`, exemption emptied, exemption as case-insensitive regex strip (3): all 25 FAILED. Unmutated control passes.
   - Three extra mutants stayed green (see findings F1).
5. Closed lines: none claimed (HPSMPOC-466 STILL OPEN at main: main's row is the old three patterns and the `\bdo not save\b` exemption, seen in the diff's removed lines).
6. Probes. My own parse of steps.ts at head: 14 `id:` steps, 14 string cue fields, 8 string caveat fields (the 15th `cue:` token is the interface line). Widened patterns + exact exemption read 0 over all 22 fields. Without the exemption, step 6's cue reads 1 hit (so the exemption is load-bearing and appears in exactly 1 cue). Exemption is `split(EXEMPT).join("")` with `EXEMPT = "View only: do not save an answer"`: exact and case-sensitive; `Do not save the plan.`, `View only: do not save the plan.` and `<EXEMPT>. Then save it.` each = 1 hit (asserted in the row). Boundaries, regex run on probe strings: `approve each`, `scoring it`, `approved`, `saved`, `autosave`, `submitted`, `score:`, `rescore it`, `the score is` = 0 hits (not forms the ticket names; the builder stated these limits); `save-as`, `Save.`, `approve<newline>it`, `approve  it`, `score a point` = hit. No `steps.ts` word touched.
7. Scans over the 26 added lines and the commit message: Cf characters 0 (control with U+200B fires), non-ASCII 0, ban list (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite) 0 with control `_by_Kam_ _by_Inch_` firing, uuids 0, URLs 0, token/secret/password words 0, long base64 runs 0, hosts 0; B-numbers/seat ids in the message 0. CodeQL pre-scan over added lines: `new RegExp(` 0, `RegExp(` 0, `.replace(` 0, `$&` hand-escape 0, innerHTML / dangerouslySetInnerHTML 0, child_process 0, exec/eval 0 (each pattern fires on a control string). The row uses only regex literals and `String.split/join`; no RegExp built from a variable.
8. Claims in the builder's STATUS (graded):
   - One file changed, 26 insertions 7 deletions: TRUE (I count 26 added lines).
   - Head sha = ls-remote: TRUE.
   - 0 shipped hits over 14 cues and 8 caveats: TRUE (own parse).
   - Every planted form turns the row red, cue and caveat: TRUE (my run, 16 of 16 forms-in-places for the six ticket forms plus extras).
   - All 23 mutants red: TRUE for the 23 it lists (my 25 also all red); but the claim "no mutant stayed green" holds only for its own table, see F1.
   - web-unit main = head = 285/4187/4187/0/0: TRUE. 1 rename, 0 status changes: TRUE.
   - Lint, typecheck exit 0: TRUE. infra hidden-characters 14 OK: TRUE.
   - Old row is green on the six new forms: TRUE.
   - `\s+` also catches a double space or line break: TRUE as regex behaviour (probe), but NOT SHOWN by any assertion in the row (F1).
9. Tier: S8 is tier 2; no security-shaped issue found.

## Findings

| # | Sev | Finding |
|---|---|---|
| F1 | Minor | Three extra mutants of the new row stay green: dropping the `i` flag on the verb pattern (no planted capitalised `Save`/`Submit`), dropping the left `\b` of `score` (no planted `rescore it`), and `\s+` replaced by one space (no planted double space or line break). The ticket's required forms and every per-alternative mutant are pinned; these three are extra hardening, not asked for. |
| F2 | Minor | Builder's STATUS says the preflight 0-count on PR files had no separate positive control; mine had (13 and 8 files listed). Informational. |
| F3 | Minor | The builder ran vitest from the wrong directory once and wrote about 45 cache files into the git-ignored `node_modules/.vitest-cache` at the project root; disclosed in its STATUS, no tracked file affected, nothing on the branch. Not part of the change. |
| F4 | Info | Commit author metadata is the repo's usual identity (295 of the last 300 commits on main) and is not an added line or message text. Node here is v26, CI uses 24; lint, typecheck and vitest are green regardless. |
| F5 | Info | Web-unit counts do not differ by "new rows": no row was added, only the one row retitled (the brief said "new rows only"; the difference is zero, which is within it). |

No Blocker. No Major. Merge is clean and equals main plus the head blob.

## NOT RUN
CodeQL (hosted; Tuesday lands through it), every other hosted CI job: web-build audit and `npm run build`, web-e2e shards, api jobs, api-sqlserver, infra bicep/shellcheck/validate.sh, secrets, dependency-review. No docker, no database, no ports. PR #304 and #305 were not run, only diffed. `npm ci` was not rerun (node_modules copied from the builder's clone; package.json and lock unchanged by the head: empty diff).
