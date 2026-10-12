# Delta gate: Secuura Platform K PR #1474 (KS-884)

**Verdict: GO WITH NOTE** on head `651209dc7ecf6af055baec8a19826c7e262ca9ef` (tree `00e0a70c22fd2859729332efd823ece994434b7f`).
This is an independent Opus delta gate, run 2026-10-12. The head matches `refs/pull/1474/head` on origin (checked with ls-remote).

I did not touch the Secuura repo. I made my own clone (`--no-hardlinks`, origin removed) in my scratchpad. I fetched develop read-only into `refs/gate/develop` of that clone. Every push went to a bare repo in my scratchpad.

## 1. Delta shape: confirmed
- There is one commit on `302d8d081`. It changes 2 files, +32/-1 (`evidence/delta.diff`).
- `.githooks/pre-push:176` changes from `rev-parse --verify` to `show-ref --verify`. That is the only hook change, and the mode is still 100755.
- The test adds the S13 header lines and the S13 cell, which has two checks: a precondition and the behaviour.
- The hook is equivalent to the fix candidate from my previous gate. The only difference is a redundant `>/dev/null 2>&1`.
- **Merge prediction:** develop is now `a28ed5d8`, 13 commits ahead. None of those commits touches `.githooks`, `__tests__` or `systemTest/scripts`. `merge-tree` is clean, and the merged hook blob and test blob are identical to the PR's.

## 2. Tests (my runs)
- ks884: the **head hook passes 10 / 0**. The **302d8d081 hook passes 9 / 1, and only the S13 behaviour check fails**, so reverting the one line turns only S13 red. The old (29434e5) hook passes 7 / 3: the tag cell, S4 and S10 fail, and S13 passes.
- The other suites give the same result on the head hook and the 302d8d081 hook:

  | Suite | Result |
  |---|---|
  | pre_push_hook_base | 28/0 |
  | pre_push_hook_current_develop | 4/0 |
  | fixture_guard | 6/0 |
  | base_leg_comment | 4/0 |
  | stack_legs_comment | 4/0 |

## 3. False-skip battery: 53 scenarios, comparing old, 302d8d081 and head
Full tables are in `evidence/mine_*.txt`.

The 28 scenarios from my previous gate:
- **M4 and M4g now RUN.** They were the false skip in 302d8d081.
- **M4f now RUNS.** Both the old hook and 302d8d081 skipped it.
- **No scenario got less safe than the old hook.** M13d (off-history tag, docs only) was SKIP-correct in 302d8d081, and the old hook over-ran it. That is the KS-884 bug itself.

The 25 new scenarios:
- **A tag with the same name as a branch (N1, N1b, N1c, N1d):**
  - The change runs in all three dev scenarios.
  - N1b was a false skip in the old hook.
  - When a branch `develop` and a tag `refs/heads/develop` both exist, the branch wins.
  - N1d is a docs-only control and correctly skips.
- **Packed refs (N2, N2d, N2h):** show-ref reads packed-refs. The packed hijack tag (N2h) now runs; 302d8d081 skipped it.
- **Symbolic refs (N3, N3d, N3x, N3r):**
  - show-ref accepts a symref and follows it.
  - A dangling symref plus a hijack tag (N3x) now runs; 302d8d081 skipped it.
- **A tag named `origin/develop` and nothing else (N4, N4b, N4c):** all three RUN. The old hook skipped all three.
- **A branch literally named `refs/heads/develop` (N4d):** RUNS now; 302d8d081 skipped it.
- **Shallow clone with a hijack tag (N6):** RUNS now; 302d8d081 skipped it.
- **Worktree (N7, N7d):** correct.
- **Reftable with a hijack tag (N9):** RUNS now; 302d8d081 skipped it.
- **Push from a bare repo (N8):** refused in all three hooks, because the gate is not found there. It fails closed.

Every case where 302d8d081 falsely skipped now runs. There is **no new false skip**.

The remaining skips are the same in all three hooks and are not caused by this PR:
- M9 (rename out of Blockchain/Dev) and M18 (pushing a branch that is not checked out) are already ticketed.
- N10 is new information, not a defect of this PR. A branch `DEVELOP` on APFS, which is case-insensitive, is read as `develop` by all three hooks.

## 4. The KS-991 residual claim (`.githooks/pre-push:166-169`)

"It cannot hide a change" **is defensible only with a qualifier.** When KS-991 fires, the loop reads only the exact `refs/remotes/origin/develop`, checked with show-ref. So the hook skips only if nothing under Blockchain/Dev differs from the real origin/develop. If the real origin/develop is missing, KS-854 runs instead.

The sentence "**The effect is extra preflight runs only**" is **false** and must be softened:
- **N5:** a tag `origin/develop` makes KS-991 fire for a local develop that diverged from origin/develop, and the push SKIPS.
- **N5c**, the same setup without the tag, RUNS.
- The old hook behaves the same way in both cases.
- The change it drops is already on the real origin/develop.

Suggested wording: "it can add or remove a run, but it cannot hide a change that is not already on refs/remotes/origin/develop."

## Defects
1. **Minor (wording):** in commit `651209dc`, Correction 1 of the message says "extra preflight runs only". That is contradicted by N5 against N5c. The code is not affected. Correct it in the PR text or the squash message.

There is no Major defect.
