VERDICT: GO WITH NOTE (head 91809ebe6b8cb8e0cb7b836440c9d9b705283be7, base/live develop e67e0dc1916b954a53c40db68ea81f0f905de641; round 1 of 2)
SHA256/16: 6aad7fad2eeccd01

# Gate: PR 1553 (KS-1605 item 5, ks884 fixture cure), Tier 2, through-code, test-only

Gate seat: Opus subagent commissioned by Wednesday, 2026-10-15. Findings only, nothing fixed.
Clone: `git clone --shared` of `!CODING/Secuura/Blockchain/2_Project_Files` into this session's scratchpad. All fetches, checkouts, worktrees, merge-trees and test runs happened there. Nothing in `!CODING` was written to; the only verb run there was `ls-remote` (plus reads). No push, no GitHub or Linear writes, no Docker, no remote box.
Runner shape: the same as `Blockchain/Dev/scripts/run-shell-suites.sh:360` (`bash "$REPO_ROOT/$rel"`, stdin `</dev/null`), run as `/bin/bash` 3.2.57 from the clone's repo root. TMPDIR is `/tmp/g1553` (UUID-free). git is 2.51.0.
Raw outputs are in `evidence/` (diff, 78+ run logs with summaries, mutant hooks, scripts).

## FOUND

| # | Severity | Where | Finding |
|---|---|---|---|
| F1 | Info (the cure holds) | test.sh:113, :128 | The cure works. FIXED arm: 0/20 any-red. UNFIXED (develop) arm, interleaved with it: 15/20 any-red. FIXED stays 10/0 even when every commit is forced into ONE second (5/5). Under the same forcing, UNFIXED goes red 5/5 on both S4 and S10. |
| F2 | Note (comment accuracy, non-blocking) | test.sh:128 | The S10 comment says "must differ from the S4 commit". Measured with pinned dates, the unfixed S10 commit is byte-identical to BOTH S4's commit and cell 1's (`eceba002…` in all three clones, see `evidence/runs/enum_pinned.txt`). The fix separates it from both, so the code is right and only the comment undersells it. The two commits together close the three-way collision; either one alone would leave a pair. |
| F3 | Info (residual collision, harmless) | test.sh:59, :106/:111, :106/:126 | The three `side` commits (`commit-tree`, tag develop in fresh, tag develop in stale_tag, tag origin/develop in stale_origin_tag) are still byte-identical within a second (`97fa86e5…` all three under pinned dates). They are never pushed and live only as local tags, so `for-each-ref --contains` in pre-push:120 never sees them. Pinned-date runs prove no effect: FIXED 10/0 5/5. |
| F4 | Info (latent class, suggestion only) | the whole file | The cure is "distinct content per cell". Nothing stops a future cell from reusing `echo more >> docs/readme.md` off origin/develop with message "docs only", which would bring the race back. A cheap permanent guard would be one CI arm run with `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` pinned. That arm turns any such collision deterministic (it is the control used here). It is out of scope for this PR. |

No Blocker, Major or Minor findings.

## TESTED / HOW

### 1. Diff by hunk
`git diff origin/develop...origin/pr1553` touches ONE file, `Blockchain/Dev/scripts/__tests__/ks884_pre_push_tag_named_develop.test.sh`, +2/-2 (`evidence/01_diff.txt`).
- 84779019e changes only :128 (S10): `echo more` becomes `echo s10-distinct` plus the K10 comment. This matches K10's tested-fix line in `5_Project_History/2026-10-13_seatK-10th/measurements/ks884_S10_finding.txt:45`.
- 91809ebe6 changes only :113 (S4): `echo more` becomes `echo s4-distinct` plus the R45 comment.
- No product or hook file changed. `.githooks/pre-push` has blob `b63a7a46dd647cac14199e81694321f12e422005` on both develop and the PR head, and `git diff --quiet` reports it identical.

### 2. Reproduction, interleaved (`evidence/runs/loop_summary.txt`)
20 FIXED and 20 UNFIXED runs, strictly alternating F,U,F,U…, each 2-3 s. UNFIXED is the develop worktree.

| Arm | Runs | Tally printed | DEAD | S4 red | S10 red | any-red |
|---|---|---|---|---|---|---|
| FIXED (PR head) | 20 | 20 | 0 | 0 | 0 | **0/20** |
| UNFIXED (develop) | 20 | 20 | 0 | 4 | 11 | **15/20** |

Controls that could have fired:
- The UNFIXED arm in the same loop is the known-red arm, and it went red.
- **Pinned-date arm** (`GIT_AUTHOR_DATE=GIT_COMMITTER_DATE=@1700000000`, 5+5 interleaved, `pinned_summary.txt`): UNFIXED 5/5 red (S4 and S10 both, `landed=1 ks991=0 preflight-ran=0`, which is the pre-push:120 `onremote` skip). FIXED 5/5 at 10/0.
- **Dead-run detector control** (`dead_control_summary.txt`): `HOOK_SH=/nonexistent` gives rc=2, no tally, and is classified DEAD. The detector can fire, and fired 0 times in the 70 real runs.

### 3. Pairwise collision table (the S13 question)
Every commit the file builds was enumerated from the kept `$WORK` of an instrumented copy run with dates pinned to one second (worst case), for both arms (`evidence/runs/enum_pinned.txt`, `scripts/enum.sh`). The copy's only change is that the trap prints `$WORK` and does not remove it. Identity is t / t@t.t throughout (`GIT_CONFIG_GLOBAL=/dev/null`, repo config).
Measured fact that corrects a natural assumption: the seed's `main` and `develop` are the SAME commit (`dev change`, f6fd269). The seed commits on main, and `branch -f develop` moves develop there. So S13's parent `main` is origin/develop, not init.

| Cell | Line | Parent | Tree change | Message | Pushed? |
|---|---|---|---|---|---|
| A seed init | :44 | none | base | init | yes (origin/develop~1) |
| B seed dev | :47 | A | file.txt +more | dev change | yes (main=develop) |
| C side tag (fresh) | :59 | A | none (A's tree) | side | no (local tag) |
| D cell 1 docs/tagged | :63-65 | B | docs +more | docs only | yes |
| E cell 2 feat/tagged | :74-76 | B | file.txt +more | dev change on the branch | yes |
| F S4 side tag | :106/:111 | A | none (A's tree) | side | no |
| G S4 docs/stale | :112-114 | B | docs +s4-distinct (was +more) | docs only | yes |
| H S10 side tag | :106/:126 | A | none (A's tree) | side | no |
| I S10 docs/stale10 | :127-129 | B | docs +s10-distinct (was +more) | docs only | yes |
| J S13 dev | :162-164 | B (=main) | file.txt +more | dev change | tag only (refs/tags/refs/heads/develop) |
| K S13 docs on top | :166-167 | J | docs +more | docs on top | yes |

Pairs that can produce one SHA within one second, i.e. same parent, same tree and same message:
- **UNFIXED: D=G=I.** Same parent B, same tree 42a2344, same message. Measured as one SHA eceba002 in fresh, stale_tag and stale_origin_tag. This is the defect: G and I are cloned after D (and G) are pushed, so pre-push:120 finds the tip inside `refs/remotes/origin/docs/tagged` and skips judging altogether.
- **FIXED:** D, G and I have three distinct trees (42a2344 / 695f372 / 362b0f6). **No pushed pair collides.**
- **C=F=H (both arms).** Same SHA 97fa86e5. Harmless (F3): the tags are local and never pushed, and they are never a pushed tip.
- **S13 (J, K):** J has the same parent and tree as E (d414cb2) but a different message ("dev change" vs "dev change on the branch"). J also differs from B in parent and tree. K's tree differs from D's because file.txt differs, and K's message is unique. **S13 cannot collide with any cell**, measured as distinct SHAs under pinned dates. All other pairs differ in at least one of parent, tree or message, by construction.
- Pinned-date runs make every same-second collision happen. FIXED still reads 10/0 5/5, so no remaining collision affects any assertion.

### 4. Do the fixed cells still test what their names say? (`mutation_summary.txt`, `mutation_diffs.txt`, `mutant_hooks/`)
Each mutation was applied to a COPY of the PR head's hook in the scratchpad and run with `HOOK_SH=` against the FIXED suite: 3 normal runs plus 2 pinned-date runs, so the result cannot be a collision artefact.

| Mutant | Edit (pre-push line) | Expected | Got (5/5 each) |
|---|---|---|---|
| M_S4 | :237 `--is-ancestor refs/heads/develop` becomes bare `develop` (the tag captures it) | S4 red only | S4 FAIL `ks991=0 preflight-ran=1`, S10 ok, 9/1 |
| M_S10 | :241 `_refs='origin/develop'` (bare) + :244 `show-ref --verify` becomes `rev-parse --verify` | S10 red, S4 green (S13 red collateral, as it pins :244) | S10 FAIL `ks991=1 preflight-ran=1`, S4 ok, S13 FAIL, 8/2 |
| M_S10b | :241 `_refs='origin/develop'` only | both red (show-ref rejects the bare name, so KS-854 runs unconditionally) | S4+S10 FAIL, 8/2 |
| CTRL_comment | comment line inserted after :242 | 10/0 | 10/0 |

The mutants fail with `preflight-ran=1`, not the collision signature `ks991=0 preflight-ran=0`. That shows the fixed cells now reach the hook's base-selection branch (KS-991 skip, fully-qualified `_refs`) and are not short-circuited by the `onremote` skip at :120. Each cell is pinned by an edit to the hook line its name describes.

### 5. Merge prediction (`evidence/runs/merge.txt`, `scripts/merge.sh`)
- Live develop, re-read by `ls-remote` at 2026-10-15T05:43:56Z: `e67e0dc19…`, which equals the merge-base. The PR head re-read is `91809ebe6…`.
- Develop has 0 commits since the base, so the overlap set is empty and the merge is a fast-forward. `merge-tree --write-tree` gives rc=0 and tree c3d86e33, which equals the PR head's tree.
- Planted conflict control: a fake develop commit editing :113 differently gives `CONFLICT (content)` with rc=1. The overlap check can fire.
- Planted non-overlap control: a fake develop commit touching another file merges clean with rc=0.

## NOT tested
- The full `run-shell-suites.sh` (the author's 88/88 in-hook claim) and an in-hook push run. Only this one suite was run, standalone in the runner's shape.
- The author's 40-run cell-1-tip == S4-tip probe was not repeated as such. It is superseded by the pinned-date enumeration, which shows the D=G=I identity directly.
- Linux / dash / CI shells. Only macOS /bin/bash 3.2.57 and git 2.51.0 were used.
- Behaviour across a real second boundary in the middle of a cell. The pinned and unpinned arms bound both extremes.

## Merge note
Merge only on Wednesday's head-bound GO for 91809ebe6b8cb8e0cb7b836440c9d9b705283be7. Nothing deploys. F2 and F4 are optional follow-ups, not conditions.
