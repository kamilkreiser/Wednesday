# Gate — Secuura Platform K PR #1474 (KS-884, pre-push base selection)

**Verdict: GO WITH NOTE** on head `302d8d0815df452590d4609e5431acb333fd1543` (tree `2e53e7af4523d6ff43d94ec1e04a198c97a2793d`).
Independent Opus QA gate, 2026-10-12. Read-only on the Secuura repo: own clone (`--no-hardlinks`, origin removed) in scratchpad; develop fetched read-only into `refs/gate/develop`; every push went to bare repos under my scratchpad. No PR comment, no board write, no push to any real remote.

## What I ran (my own runs)

1. **Diff shape.** One commit on `29434e554e70`, 2 files (`.githooks/pre-push` M, `Blockchain/Dev/scripts/__tests__/ks884_pre_push_tag_named_develop.test.sh` A), +160/-5. The Spark patch applies cleanly to the parent. The resulting hook is **byte-identical** to the PR hook (blob `6f2e834d6d…` both). The test file is the only delta: a header note plus S4/S10 (`evidence/test_delta.diff`).
   **Merge prediction:** develop is now `524db0ce64da` (5 commits ahead, none touching `.githooks`, `__tests__` or `systemTest/scripts`). `merge-tree` is clean and the merged hook equals the PR hook. On the predicted merge commit (`evidence/merged.sha`), every suite that references the hook passes: ks884 8/0, pre_push_hook_base 28/0, current_develop 4/0, fixture_guard 6/0, base_leg_comment 4/0, stack_legs_comment 4/0, preflight_deps 56/0, check_stack_safety_hook_env 5/0.
2. **Extended test.** The new hook gets **8 pass / 0 fail**. The old hook gets 5 pass / **3 fail**: the tag cell, S4 and S10.
   **Single-edit reverts:** reverting the `_refs` list reddens only the tag cell. Reverting `--is-ancestor` reddens only S4. Reverting the stale `_refs` reddens only S10. Reverting `--verify` or `!=` stays 8/0, which is the stated M1/M2/M5 red and M3/M4 green.
3. **Existing suites.** pre_push_hook_base is 28/0 on both old and new. pre_push_hook_current_develop is 4/0 on both. The runner population is 80 at the base and **81** at the head and the merge. `--check-unreached` is OK on all three.
4. **F's harness** (run from a copy). S0–S11 match F's tables row for row, old and new. S12 RAN on both. F's archived tables have only 12 rows: S12 is in the harness but not in the saved files.
   **My scenarios** (old vs new; 28 rows; `evidence/mine_{OLD,NEW,FIX}.txt`):
   - **Identical in both:** a dev change only through the 2nd parent of a merge with a tag on the merge; local develop far ahead; upstream present; ALLOW_FORCE force-push (RAN); force without ALLOW_FORCE (REFUSED, as the control); rename into Blockchain/Dev; deletion; `develop-x`; remote named `gh` (dev RAN, docs SKIP); packed refs; linked worktree; shallow `--depth 1` (dev RAN, docs SKIP); detached HEAD; a local *branch* named `origin/develop`.
   - **Fixed by the PR:** M3 and M17 (a tag `develop` on the dev commit inside the branch, origin/develop absent). Old SKIPS here, new RUNS (KS-854).
   - **Controls:** every SKIP has a matching RAN control in the same setup (M3c, M12/M12d, M13/M13d, M15/M15d).

## Defects

1. **Minor: a new false-skip path.** `.githooks/pre-push:176` (and `:166`) still pass `refs/heads/develop` to `rev-parse`, and `rev-parse` interprets the name rather than reading it literally. When the branch is absent, `refs/tags/refs/heads/develop` satisfies it. A porcelain `git tag refs/heads/develop` creates one. With origin/develop also absent, the **new hook SKIPS a real Blockchain/Dev change where the old one ran KS-854** (M4, M4g). The trigger is contrived (a tag literally named `refs/heads/develop`, plus a clone without origin/develop). M4f, the same thing for `refs/remotes/origin/develop`, already skipped in the old hook.
   **Fix:** `git show-ref --verify --quiet "$_ref" || continue` at :176. I tested this in scratch: M4/M4f/M4g RAN, no other row changed, and the suites stay 8/0, 28/0 and 4/0 (`evidence/pre-push.fixcand`).
2. **Minor:** `.githooks/pre-push:167-169` still use the bare `origin/develop`, but the commit message says the KS-991 test is now fully qualified. S10 goes green because the tag drives KS-991. A branch named `origin/develop` makes the hook run when it does not need to (M4d). I found no false skip from this.
3. **Minor (claim):** the commit message says the old bug "does not hide a change". That is false: M3 and M17 hide one in the old hook. The fix is worth more than stated.

## Pre-existing (same in old and new; not this PR; ticket separately)

- `:80` and `:184`: the default rename detection in `git diff --name-only` hides a rename **out of** Blockchain/Dev, so the push skips (M9). `--no-renames` shows the deleted path.
- `:80` and `:136`: the hook diffs `HEAD`, not the pushed sha. Pushing a dev branch while a docs branch is checked out skips (M18).
